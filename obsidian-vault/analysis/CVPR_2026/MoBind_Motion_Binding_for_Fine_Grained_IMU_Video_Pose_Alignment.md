---
title: "MoBind: Motion Binding for Fine-Grained IMU-Video Pose Alignment"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MoBind_Motion_Binding_for_Fine_Grained_IMU_Video_Pose_Alignment.pdf
project_link: null
code_link: "https://github.com/bbvisual/MoBind"
aliases:
- MoBind
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 施加token级、身体部位级和全局级三层层次化对比约束，并显式对齐IMU与对应身体部位的骨骼运动，从而同时控制细粒度时间同步和粗粒度语义保留。
primary_logic: 通过将IMU信号对齐到由视频提取的骨骼运动（去除了无关视觉背景），并将全身运动分解为局部身体部位轨迹进行层次化对比学习（token级、部位级、全局级），可实现在多传感器配置下的精确亚秒级时间对齐，同时通过掩盖令牌预测辅助任务保留动作级语义。
claims:
- MoBind在mRi数据集上跨模态检索R@1达到0.94 (IMU→Video)和0.92 (Video→IMU)，大幅超越SyncNet (0.77/0.75)和IMU2CLIP (0.67/0.38)。
- 在时间同步任务上，MoBind在mRi上取得最低平均绝对误差0.47秒，在TotalCapture上准确率0.98，在EgoHumans上完美准确率1.00。
- 层次消融实验表明，逐步加入token级、局部级和全局级对比损失在所有任务上带来一致且显著的性能提升。
- 加上Masked Token Prediction（MTP）辅助任务后，TotalCapture上动作识别微调准确率从0.55提升至0.72，相对提升超过30%。
---

# MoBind: Motion Binding for Fine-Grained IMU-Video Pose Alignment

> [!tip] 核心洞察
> 通过将IMU信号对齐到由视频提取的骨骼运动（去除了无关视觉背景），并将全身运动分解为局部身体部位轨迹进行层次化对比学习（token级、部位级、全局级），可实现在多传感器配置下的精确亚秒级时间对齐，同时通过掩盖令牌预测辅助任务保留动作级语义。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoBind：面向细粒度IMU-视频姿态对齐的运动绑定 |
| 英文题名 | MoBind: Motion Binding for Fine-Grained IMU-Video Pose Alignment |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.19004) · [Code](https://github.com/bbvisual/MoBind) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | MoBind |
| Dataset | mRi, TotalCapture, EgoHumans |

> [!tip] 效果简介
> - mRi 上，R@1 IMU→Video 0.94 vs SyncNet 0.77 / IMU2CLIP 0.67 (+0.17 / +0.27)；R@1 Video→IMU 0.92 vs SyncNet 0.75 / IMU2CLIP 0.38 (+0.17 / +0.54)；时间同步 MAE (s) ↓ 0.47 vs SyncNet 1.89 / IMU2CLIP 4.95 (-1.42 / -4.48)。
> - TotalCapture 上，时间同步 Acc ↑ 0.98 vs SyncNet 0.89 / DeSPITE 0.27 (+0.09 / +0.71)。
> - EgoHumans 上，时间同步 Acc ↑ 1.00 vs SyncNet 0.97 / DeSPITE 0.95 (+0.03 / +0.05)。

## 概述

**问题瓶颈**：现有 IMU-视频对比学习方法仅在全局片段级别对齐，丢失亚秒级时序同步信息，无法捕捉多传感器配置下身体部位的特异性动态，导致细粒度跨模态检索和精确时间同步失败。

**核心思路**：MoBind 提出“运动绑定”范式，将 IMU 信号与视频提取的骨骼运动序列对齐，而非原始像素。通过将全身运动分解为局部身体部位轨迹，与对应 IMU 严格配对，施加三层层次化对比约束（token 级、局部部位级、全局级），同时引入掩码令牌预测辅助任务保留动作语义。

**方法定位**：相比于 IMU2CLIP（Moon et al., 2022）和 DeSPITE（Kreutz et al., 2025）等仅做全局对齐的方法，MoBind 的关键改动在于：(1) 视觉输入从 RGB 像素转为 2D 骨骼运动；(2) 对齐粒度从单一全局嵌入扩展为三层层次化对比；(3) 多传感器处理从简单拼接改为逐部位配对学习；(4) 引入 MTP 辅助任务防止细粒度对齐过拟合。

**主要结果**：在 mRi、TotalCapture 和 EgoHumans 三个数据集上，MoBind 在四项下游任务上一致超越强基线：
- 跨模态检索：mRi 上 IMU→Video R@1 达 0.94（SyncNet 0.77），Video→IMU R@1 达 0.92（IMU2CLIP 0.38）；
- 时间同步：mRi 上平均绝对误差仅 0.47 秒，TotalCapture 准确率 0.98，EgoHumans 完美准确率 1.00；
- 人员识别与动作识别同样取得最优，且层次消融和 MTP 消融实验验证了各模块的独立贡献。

**局限与开放问题**：方法依赖已知的 IMU 安装位置和外部 2D 姿态估计器，在遮挡、低光照及无约束佩戴场景下的泛化性有待验证；如何无监督发现传感器-部位对应关系、处理动态变化的传感器配置，是值得探索的方向。

## 背景与动机

### 问题背景：IMU与视觉信号的跨模态对齐需求

惯性测量单元（IMU）传感器因其低功耗、隐私友好和环境无关的特性，在可穿戴设备、增强现实和健康监测等领域得到广泛应用。IMU能够捕捉人体运动的加速度和角速度信息，而视频则提供了丰富的视觉上下文。将IMU信号与视频数据进行精确对齐，是实现跨模态检索、时间同步、人员识别和动作理解等下游任务的关键基础。

然而，IMU与视频之间存在显著的模态鸿沟：IMU记录的是附着于特定身体部位的局部运动信号，而视频则呈现包含背景、光照和外观变化的全局视觉场景。如何在这两种异质模态之间建立细粒度的对应关系，是多模态学习领域的一个重要挑战。

### 现有方法缺口：全局对齐的局限性

现有的IMU-视频对比学习方法，如**IMU2CLIP**（Moon et al., 2022）和**DeSPITE**（Kreutz et al., 2025），主要借鉴了视觉-语言领域的全局对比学习范式。这些方法将完整的IMU序列和视频片段分别编码为单一的全局嵌入向量，并在clip级别施加对比损失。这种设计存在以下结构性缺陷：

1. **丢失亚秒级时序同步信息**：全局嵌入将整个片段压缩为一个固定维度的向量，无法保留帧级或子秒级的时间对应关系。当需要精确定位IMU信号在长视频中的时间偏移时，这类方法只能依赖粗粒度的全局相似度，导致同步精度严重不足。例如，**SyncNet**（Chung & Zisserman, ACCV Workshop 2016）在mRi数据集上的时间同步平均绝对误差高达1.89秒，而IMU2CLIP更是达到4.95秒（Table 2）。

2. **忽略多传感器配置下的身体部位特异性**：在实际应用中，人体通常佩戴多个IMU传感器（如手腕、脚踝、腰部等），每个传感器捕捉的运动模式与其附着部位密切相关。现有方法要么将多传感器信号简单拼接，要么独立处理各传感器流，未能显式建模IMU与对应身体部位之间的局部运动绑定关系。这导致在部分传感器失效或传感器位置未知的场景下，模型的鲁棒性和可解释性显著下降。

3. **视觉背景噪声干扰**：直接对原始RGB像素或光流进行编码，会引入与运动无关的外观、纹理和背景信息。这些视觉噪声在对比学习过程中可能成为虚假关联的来源，削弱模型对运动本质的捕捉能力。

### 本文动机：从全局对齐到层次化运动绑定

针对上述问题，MoBind提出了一个核心洞察：**IMU与视频之间的对齐应当建立在“运动”这一共享的物理量之上，而非原始像素或信号波形**。具体而言，本文的动机源于以下三个关键设计选择：

- **以骨骼运动为桥梁**：从视频中提取2D人体骨骼运动序列，去除无关的视觉背景，使两个模态在“运动轨迹”这一共同语义空间中对齐。这从根本上避免了外观信息对运动对齐的干扰。

- **分解全身运动为局部部位轨迹**：将完整的骨骼运动按已知的IMU安装位置分解为多个身体部位的运动序列，每个IMU仅与其对应的身体部位进行配对。这种“一传感器一部位”的显式绑定，使得模型能够学习到语义上可解释的局部运动表征。

- **层次化对比约束**：在三个粒度上同时施加对比损失——token级（子秒窗口）捕获精细的时间同步，局部级（身体部位）保留传感器特异性，全局级（全身）维持动作级语义一致性。这种多层次设计确保模型既不丢失细粒度时间信息，也不牺牲粗粒度的语义理解能力。

此外，MoBind引入了一个**Masked Token Prediction（MTP）**辅助任务，在训练时随机遮蔽IMU的时间令牌并要求模型重建，以防止模型过度聚焦于细粒度对齐而丧失对动作类别语义的保留能力。消融实验表明，MTP对动作识别性能的提升至关重要——在TotalCapture数据集上，加入MTP后微调准确率从0.55跃升至0.72，相对提升超过30%（Table 6）。

综上所述，MoBind的目标是建立一个统一的IMU-视频运动绑定框架，在多个粒度上实现精确对齐，从而同时支持跨模态检索、亚秒级时间同步、身体部位定位、人员识别和动作识别等多种下游任务。

## 核心创新

MoBind的核心创新在于将IMU-视频对齐从传统的**全局clip级**提升至**层次化多粒度**，并引入**骨骼运动作为中介表示**。相对于现有基线，其关键改进可归纳为以下五个“changed slots”。

### 1. 视觉输入表示：从原始像素到骨骼运动分解

现有方法（如**IMU2CLIP**（Moon et al., 2022）、**DeSPITE**（Kreutz et al., 2025））直接对RGB像素或光流进行编码，IMU信号必须隐式地学习过滤背景、光照、纹理等与运动无关的视觉信息。MoBind将视觉输入替换为**从视频提取的2D骨骼运动序列**，并根据已知的IMU安装位置将其分解为局部身体部位轨迹。这一设计将跨模态对齐问题从“IMU↔像素”转化为“IMU↔对应身体部位运动”，**显式剥离了无关视觉背景**，使模型专注于运动动力学本身的匹配。

### 2. 对齐粒度：从单一全局嵌入到三层层次化对比

基线方法仅在全局clip级别计算对比损失（如InfoNCE），丢失了亚秒级时序同步信息。MoBind构建了**三层对齐体系**：

- **Token级（子秒窗口）**：对每个时间步的token施加双向InfoNCE，强制模型捕捉细粒度时序对应关系；
- **局部身体部位级**：每个IMU与其对应的身体部位表征进行对齐，实现传感器-部位的精确定位；
- **全局级**：聚合所有传感器信息形成全身表征，保留粗粒度动作语义。

三层损失加权联合优化（$\lambda_g=1.0$，$\lambda_l=1.0$，$\lambda_t=0.5$），使模型同时具备精确时间同步和动作语义理解能力。

### 3. 多传感器处理：从简单拼接到部位配对局部对比

现有方法通常将多IMU信号简单拼接或独立处理，忽略了不同传感器与特定身体部位之间的物理对应关系。MoBind的核心操作是**将每个IMU严格与对应的身体部位配对**，在局部对比学习中对齐每对IMU-部位的运动模式，再通过Aggregator（拼接+LayerNorm+MLP）融合为全局表征。这一设计使得模型在部分传感器失效时仍能利用剩余配对信息保持鲁棒性（见Figure 7），且优于使用全部传感器的基线方法。

### 4. 辅助任务：Masked Token Prediction保留动作语义

细粒度对齐任务可能使模型过度关注局部时序细节，削弱动作类别判别能力。MoBind引入**Masked Token Prediction（MTP）**辅助任务：在训练时随机遮蔽75%的IMU tokens，通过轻型Transformer预测被遮蔽token的原始值，使用MSE损失（$\lambda_{mtp}=0.3$）。消融实验表明，MTP对动作识别至关重要——在TotalCapture上，移除MTP导致微调准确率从0.72骤降至0.55，相对下降超过30%。

### 5. 对比损失函数：从全局InfoNCE到三层加权InfoNCE + MTP联合优化

最终损失函数为：

$$\mathcal{L} = \underbrace{\lambda_g \mathcal{L}_{\mathrm{global}} + \lambda_l \mathcal{L}_{\mathrm{local}} + \lambda_t \mathcal{L}_{\mathrm{token}}}_{\mathcal{L}_{\mathrm{align}}} + \lambda_{\mathrm{mtp}} \mathcal{L}_{\mathrm{mtp}}$$

其中每个对比项均为双向InfoNCE，分别作用于全局表征、局部身体部位表征和时间token。层次消融实验（Table 5）表明，从仅有全局对比逐步加入局部和token级对比，在检索、时间同步和动作识别三项任务上均带来一致且显著的性能提升，验证了层次化设计的因果有效性。

## 整体框架

MoBind 的整体设计围绕一个核心洞察展开：**将 IMU 信号与从视频中提取的 2D 骨骼运动序列对齐，而非与原始像素对齐**，从而剥离无关的视觉背景，聚焦于运动本身。在此基础上，框架将全身运动**分解为局部身体部位轨迹**，并将每个 IMU 传感器严格与其对应的身体部位配对，实现语义上有根基的多传感器对齐。

### 框架总览

如 Figure 2 所示，MoBind 由以下主要模块构成：

1. **IMU 编码器**：对每个 IMU 传感器信号独立编码。每个传感器流通过 1D 卷积块后接 Transformer 层处理，输出 $T$ 个时间 token 和局部表征 $\bar{\mathbf{Z}}$。

2. **姿态编码器**：采用与 IMU 编码器**完全相同的架构设计**，对每个身体部位的运动序列进行编码，同样输出 token 级和局部级表征。

3. **聚合器**：将各传感器的局部表征拼接后，经 LayerNorm 和 MLP 融合为全局表征 $\mathbf{G}$：
   $$\mathbf{G} = \mathrm{MLP}(\mathrm{LayerNorm}(\bar{\mathbf{Z}}_{\mathrm{cat}})) \in \mathbb{R}^{D'}$$

4. **层次化对比损失**：在三个粒度上同时施加双向 InfoNCE 约束——**token 级**（子秒窗口对齐）、**局部身体部位级**（每个 IMU 与其对应部位配对）、**全局级**（全身表征对齐）。总体对齐损失为三者的加权和：
   $$\mathcal{L}_{\mathrm{align}} = \lambda_{g} \mathcal{L}_{\mathrm{global}} + \lambda_{l} \mathcal{L}_{\mathrm{local}} + \lambda_{t} \mathcal{L}_{\mathrm{token}}$$
   其中权重设置为 $\lambda_g = 1.0$、$\lambda_l = 1.0$、$\lambda_t = 0.5$。

5. **掩码令牌预测**：作为仅在训练时使用的辅助任务，随机遮蔽 IMU token（遮蔽比例 $\alpha = 0.75$），通过轻型 Transformer 重建被遮蔽 token，使用 MSE 损失：
   $$\mathcal{L}_{\mathrm{mtp}} = \frac{1}{|\mathcal{M}|} \sum_{(n,t) \in \mathcal{M}} \left\| \mathbf{Z}_{n,t}^{\mathrm{pred}} - \mathbf{Z}_{n,t} \right\|_2^2$$

最终训练损失为对齐损失与 MTP 损失的加权联合优化：
$$\mathcal{L} = \mathcal{L}_{\mathrm{align}} + \lambda_{\mathrm{mtp}} \mathcal{L}_{\mathrm{mtp}}$$
其中 $\lambda_{\mathrm{mtp}} = 0.3$。

### 输入输出流

- **输入**：一段 $5$ 秒的时间窗口内，多个 IMU 传感器的运动信号 + 从对应视频中提取的 2D 骨骼运动序列（按已知安装位置分解为身体部位轨迹）。每个窗口产生 $T = 25$ 个时间 token。
- **输出**：三个层次的表征——token 级（$\mathbf{Z}_t$，用于细粒度时间对齐）、局部级（$\bar{\mathbf{Z}}$，用于身体部位配对）、全局级（$\mathbf{G}$，用于跨模态检索和语义匹配）。所有表征维度均为 $D = D' = 256$。

### 关键设计决策

与现有 IMU-视频对比学习方法的核心差异在于**对齐粒度的层次化升级**。IMU2CLIP（Moon et al., 2022）和 DeSPITE（Kreutz et al., 2025）等方法仅在全局 clip 级别对齐，丢失了亚秒级时序同步信息；SyncNet（Chung & Zisserman, ACCV Workshop 2016）虽能估计偏移但依赖相关性计算，缺乏显式的多粒度对比学习。MoBind 通过三层对齐同时控制细粒度时间同步和粗粒度语义保留，而 MTP 辅助任务则进一步防止模型在追求细粒度对齐时丢失动作类别语义——消融实验表明，移除 MTP 后 TotalCapture 上动作识别微调准确率从 $0.72$ 骤降至 $0.55$（Table 6），相对下降超过 30%。

### 补充图表

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2602_19004/figures/001_Figure_1.jpg]]
*Figure 1: Proposed framework for motion binding between IMUs and 2D pose sequence from video. Contrastive learning is applied at both the local space, aligning each IMU with its corresponding body-part, and the global space, aligning full-body representations. This representation supports several downstream tasks, including cross-modal retrieval, temporal synchronization, subject and body parts localization, and human action recognition*

## 核心模块与公式推导

### 3.1 双流模态编码器

MoBind 采用对称的双流架构，分别处理 IMU 信号和从视频中提取的 2D 骨骼运动序列。

**IMU 编码器** 对每个传感器信号独立处理。输入为 5 秒窗口的 IMU 序列（加速度计和陀螺仪共 6 通道），首先通过 1D 卷积块进行时序下采样，再送入 Transformer 层，输出该传感器对应的 $T=25$ 个时间令牌（token）序列 $\mathbf{Z} \in \mathbb{R}^{T \times D}$，以及经平均池化得到的局部表征 $\bar{\mathbf{Z}} \in \mathbb{R}^{D}$，其中 $D=256$。

**姿态编码器** 采用与 IMU 流完全相同的架构设计。关键区别在于输入：视频帧先经由外部 2D 姿态估计器（如 MMPose）提取骨骼关键点，再根据已知的 IMU 安装位置将全身运动分解为各身体部位的运动轨迹。每个身体部位的 2D 关键点坐标序列作为对应编码器的输入，同样输出时间令牌 $\mathbf{Z}$ 和局部表征 $\bar{\mathbf{Z}}$。这种“按部位分解—分别编码”的设计，使得每个 IMU 与其对应的身体部位在局部层面形成严格的一对一绑定关系。

**聚合器** 将来自 $N$ 个传感器的局部表征拼接后，通过 LayerNorm 和 MLP 融合为全局表征：

$$\mathbf{G} = \mathrm{MLP}(\mathrm{LayerNorm}(\bar{\mathbf{Z}}_{\mathrm{cat}})) \in \mathbb{R}^{D'}$$

其中 $\bar{\mathbf{Z}}_{\mathrm{cat}}$ 为所有传感器局部表征的拼接结果，$D'=256$ 为全局嵌入维度。

### 3.2 层次化对比对齐

MoBind 的核心创新在于三层粒度的对比约束，同时作用于 token 级、局部（身体部位）级和全局级。

**Token 级对比损失** 在子秒窗口粒度上对齐 IMU 令牌与对应身体部位的运动令牌。对于批次中第 $i$ 个样本的第 $t$ 个时间步，双向 InfoNCE 损失为：

$$\mathcal{L}_{\mathrm{token}}^{AB} = -\frac{1}{KT} \sum_{i=1}^{K} \sum_{t=1}^{T} \log \frac{\exp(s(\mathbf{Z}_{t}^{A,i},\mathbf{Z}_{t}^{B,i})/\tau)}{\sum_{j=1}^{T} \exp(s(\mathbf{Z}_{t}^{A,i},\mathbf{Z}_{j}^{B,i})/\tau)}$$

其中 $K$ 为批次大小，$T$ 为时间令牌数，$s(\cdot,\cdot)$ 为余弦相似度，$\tau$ 为温度系数。该损失强制同一时刻的 IMU 和姿态令牌互为正样本，同一样本内其他时刻的令牌为负样本，从而实现亚秒级时序同步。

**局部对比损失** 在身体部位粒度上对齐每个传感器的局部表征：

$$\mathcal{L}_{\mathrm{local}}^{AB} = -\frac{1}{K} \sum_{i=1}^{K} \log \frac{\exp(s(\bar{\mathbf{Z}}^{A,i},\bar{\mathbf{Z}}^{B,i})/\tau)}{\sum_{j=1}^{K} \exp(s(\bar{\mathbf{Z}}^{A,i},\bar{\mathbf{Z}}^{B,j})/\tau)}$$

此处正样本对为同一身体部位的 IMU 与姿态局部表征，负样本为批次内其他样本的对应表征。

**全局对比损失** 在全身体粒度上对齐聚合后的全局表征：

$$\mathcal{L}_{\mathrm{global}}^{AB} = -\frac{1}{K} \sum_{i=1}^{K} \log \frac{\exp(s(\mathbf{G}^{A,i},\mathbf{G}^{B,i})/\tau)}{\sum_{j=1}^{K} \exp(s(\mathbf{G}^{A,i},\mathbf{G}^{B,j})/\tau)}$$

**总体对齐损失** 为三层损失的加权和，均计算 IMU→Pose 和 Pose→IMU 两个方向：

$$\mathcal{L}_{\mathrm{align}} = \lambda_{g} \mathcal{L}_{\mathrm{global}} + \lambda_{l} \mathcal{L}_{\mathrm{local}} + \lambda_{t} \mathcal{L}_{\mathrm{token}}$$

实验设定 $\lambda_g=1.0$、$\lambda_l=1.0$、$\lambda_t=0.5$。消融实验（Table 5）证实，从仅全局对比逐步加入局部和 token 级约束，在所有下游任务上均带来一致且显著的性能提升。

### 3.3 掩码令牌预测

层次化对比损失在细粒度对齐上效果显著，但可能过度聚焦于局部时序匹配而削弱动作级语义。为此，MoBind 引入仅在训练时使用的 **掩码令牌预测（Masked Token Prediction, MTP）** 辅助任务。

具体而言，对 IMU 编码器输出的时间令牌序列，以 $\alpha=0.75$ 的比例随机遮蔽部分令牌。被遮蔽位置 $(n,t) \in \mathcal{M}$ 的令牌由一个轻型 Transformer 预测器重建，损失函数为均方误差：

$$\mathcal{L}_{\mathrm{mtp}} = \frac{1}{|\mathcal{M}|} \sum_{(n,t) \in \mathcal{M}} \left\| \mathbf{Z}_{n,t}^{\mathrm{pred}} - \mathbf{Z}_{n,t} \right\|_2^2$$

该任务迫使模型学习 IMU 信号的内在时序结构和动作语义，而非仅依赖跨模态对齐信号。消融实验（Table 6）表明，移除 MTP 后 TotalCapture 上动作识别微调准确率从 0.72 骤降至 0.55，1-NN 准确率从 0.71 降至 0.53，验证了 MTP 对保留动作类别语义的关键作用。

**最终训练损失** 为对齐损失与 MTP 损失的联合优化：

$$\mathcal{L} = \mathcal{L}_{\mathrm{align}} + \lambda_{\mathrm{mtp}} \mathcal{L}_{\mathrm{mtp}}$$

其中 $\lambda_{\mathrm{mtp}}=0.3$。

### 补充图表

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2602_19004/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed MoBind. The framework first encodes each IMU stream together with the motion of its corresponding body part, yielding token-level and local-level representations per sensor. These local representations are then aggregated across sensors to form global-level embeddings. The contrastive objective applies at all three levels. In addition, a Masked Token Prediction (MTP) module is used only during training to preserve coarse semantic structure, preventing the model from over-focusing on fine-grained alignment*

## 实验与分析

### 核心瓶颈与因果机制

现有IMU-视频对比学习方法（如**IMU2CLIP** (Moon et al., 2022)、**DeSPITE** (Kreutz et al., 2025)）仅在全局clip级别对齐，丢失了亚秒级时序同步信息，无法捕捉多传感器配置下身体部位的特异性动态，导致细粒度跨模态检索和精确时间同步失败。MoBind通过以下因果机制解决该瓶颈：

1. **视觉输入去冗余**：将IMU信号对齐到从视频提取的2D骨骼运动序列，而非原始RGB像素，去除无关视觉背景的干扰。
2. **三层层次化对比约束**：施加token级（子秒窗口）、身体部位级和全局级三层对比损失，同时控制细粒度时间同步和粗粒度语义保留。
3. **显式传感器-部位配对**：将全身运动分解为局部身体部位轨迹，每个IMU严格与对应的身体部位配对进行局部对比学习。

### 跨模态检索性能

Table 1展示了在mRi、TotalCapture和EgoHumans三个数据集上的跨模态检索结果。MoBind在所有检索方向和所有Recall@K指标上均一致超越所有基线方法。

在mRi数据集上，MoBind的IMU→Video方向R@1达到**0.94**，相比SyncNet（0.77）和IMU2CLIP（0.67）分别提升+0.17和+0.27；Video→IMU方向R@1达到**0.92**，相比SyncNet（0.75）和IMU2CLIP（0.38）分别提升+0.17和+0.54。值得注意的是，IMU2CLIP在Video→IMU方向表现极差（0.38），表明其全局对齐策略在反向检索中几乎失效，而MoBind的层次化设计在两个方向上均保持高度对称的性能。

在TotalCapture数据集上，MoBind在IMU→Video方向R@1达到**0.88**，远超DeSPITE（0.52）和IMU2CLIP（0.35）。在EgoHumans数据集上，所有方法表现均较高（R@1均>0.90），但MoBind仍以**0.97**（IMU→Video）和**0.98**（Video→IMU）取得最优。

Table 1还揭示了一个关键发现：在mRi数据集上，IMU2CLIP的R@1错误样本中**79%**的top-1冒名者属于同一动作类别，DeSPITE为76%，SyncNet为75%。这说明这些基线方法主要依赖动作类别语义进行匹配，而非真正的细粒度时序对齐——这正是MoBind通过token级对比所要解决的核心问题。

Figure 3展示了IMU→Video检索的定性结果。在mRi和EgoHumans上，MoBind不仅成功检索到ground-truth视频片段，且其他top-ranked结果在视觉上也与ground truth高度相似，表明模型学习到了鲁棒的跨模态运动表征。

### 时间同步性能

Table 2报告了时间同步任务的结果。所有模型在20秒视频上评估，随机时间偏移从[-7, 7]秒均匀采样。

在mRi数据集上，MoBind取得最低平均绝对误差**0.47秒**，而SyncNet为1.89秒，IMU2CLIP高达4.95秒。MoBind的MAE相比SyncNet降低**1.42秒**（相对降低75%），相比IMU2CLIP降低**4.48秒**（相对降低91%）。这一巨大差距直接验证了token级对齐对于亚秒级时间同步的关键作用——全局对齐方法无法分辨子秒级的时序偏移。

在TotalCapture上，MoBind的同步准确率达到**0.98**，SyncNet为0.89，DeSPITE仅为0.27。在EgoHumans上，MoBind达到完美准确率**1.00**，SyncNet为0.97，DeSPITE为0.95。

Figure 4进一步展示了逐动作的同步准确率。在EgoHumans上，MoBind在所有动作上实现**低于50毫秒**的误差；在mRi上，所有动作误差均低于1秒，即使在重复性运动和近似重复片段的挑战性场景下也保持稳定。

时间偏移估计采用加权直方图方法：将双向top-k检索的所有偏移投票聚合到加权直方图中，最终估计偏移 $\hat{\delta}$ 为累计相似度得分最高的bin：

$$\hat{\delta} = \underset{\Delta}{\arg \max} \sum_{(p,q): q-p = \Delta} D_{p,q}$$

### 身体部位定位与联合任务

Table 3报告了EgoHumans多人场景下的IMU到人识别结果。MoBind达到**0.9812**的准确率和**0.9808**的F1分数，远超VIPL（0.754/0.741）和SyncNet（0.692/0.677）。这验证了局部身体部位对比学习能够有效捕获传感器与特定身体部位的运动对应关系。

Figure 5展示了身体部位定位的定性示例，每个查询IMU信号均被准确匹配到对应的身体部位。Figure 6展示了更具挑战性的联合时间同步与空间定位场景：查询的左手腕IMU信号比视频提前6.8秒，MoBind通过加权直方图准确恢复该偏移，并同时将信号定位到正确的身体部位，展示了对动态和高度重复运动的鲁棒性。

### 动作识别性能

Table 4报告了在微调（finetuning）和1-NN设置下的动作识别结果。在mRi上，MoBind微调准确率达到**0.98**，DeSPITE为0.93，AIM为0.82。在TotalCapture上，MoBind微调准确率为**0.72**，相比DeSPITE（0.47）和AIM（0.36）分别提升+0.25和+0.36，相对提升超过53%和100%。

TotalCapture上的性能差距显著大于mRi，这是因为TotalCapture包含更多样化和复杂的动作类别，对语义保留的要求更高。MoBind的MTP辅助任务在此场景下发挥了关键作用。

### 传感器故障鲁棒性

Figure 7展示了在不同可用传感器数量下的检索性能。MoBind在使用全部传感器时性能最优，但在仅部分传感器可用时仍保持较强的检索能力，且优于使用全部传感器的基线方法。例如，仅使用2个IMU传感器时，MoBind的R@1已超过IMU2CLIP使用全部传感器的性能。这一特性对于真实部署场景中的传感器失效或佩戴不完整具有重要实际意义。

### 消融实验

**层次化对比目标消融**（Table 5）：从仅使用全局对比损失开始，逐步加入局部级和token级对比损失，在所有任务上均带来一致且显著的性能提升。具体而言：
- 仅全局对比：IMU→Video R@1为0.86，时间同步MAE为1.12秒
- 加入局部对比：R@1提升至0.91，MAE降至0.73秒
- 再加入token级对比（完整MoBind）：R@1达到0.94，MAE降至0.47秒

这验证了三个层次的对齐粒度具有互补作用：全局级保留粗粒度语义，局部级建立传感器-部位对应，token级实现细粒度时序同步。

**MTP辅助任务消融**（Table 6）：移除MTP导致动作识别性能急剧下降。在TotalCapture上，微调准确率从**0.72降至0.55**（相对下降24%），1-NN准确率从**0.71降至0.53**（相对下降25%）。在mRi上，1-NN准确率从0.93降至0.82。这表明MTP通过预测被遮盖的IMU tokens，有效保留了动作类别语义，防止模型过度聚焦于细粒度对齐而丢失粗粒度动作信息。

MTP的掩码比例设为 $\alpha=0.75$，损失函数为：

$$\mathcal{L}_{\mathrm{mtp}} = \frac{1}{|\mathcal{M}|} \sum_{(n,t) \in \mathcal{M}} \left\| \mathbf{Z}_{n,t}^{\mathrm{pred}} - \mathbf{Z}_{n,t} \right\|_2^2$$

### 失败模式与局限性

1. **传感器安装位置依赖**：MoBind假设IMU传感器的身体部位安装位置已知。在无约束佩戴场景中，若无法获取安装位置先验，身体部位定位和局部对比学习的有效性将受到严重影响。

2. **2D姿态估计误差传播**：方法依赖外部2D姿态估计器提取骨骼运动。在遮挡、低光照或快速运动模糊场景下，姿态估计误差会直接传播至对齐性能。当前实验主要在实验室数据集上进行，尚未在极端视觉退化条件下大规模验证。

3. **多人密集交互未充分验证**：EgoHumans虽包含多人场景，但极端密集交互和严重相互遮挡的情况有限，模型在此类场景下的泛化性待进一步检验。

4. **现实世界分布偏移**：训练和评估数据集均为实验室收集，与现实世界嘈杂、多变的运动分布可能存在差异。传感器采样率变化、异步IMU等实际部署问题尚未系统研究。

### 开放问题

- 是否可通过无监督方式自动发现IMU与身体部位的对应关系，消除对安装位置标注的依赖？
- 如何将框架扩展至未知或动态变化的传感器数量配置？
- MTP辅助任务是否可改进为跨模态掩码预测（同时覆盖姿态tokens），以进一步提升语义保留？
- 模型在异步IMU采样率下的鲁棒性如何？跨采样率对齐是否可行？

### 补充图表

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2602_19004/figures/003_Table_1.jpg]]
*Table 1: Cross-modal retrieval performance on the mRi, TotalCapture and EgoHumans datasets. We compare our method against prior contrastive learning baselines in both retrieval directions: IMU→Video and Video→IMU. Our method consistently outperforms all others across all ranks, demonstrating strong alignment between modalities. This superior performance is particularly critical for downstream tasks that rely on accurate similarity scores between embedded features*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2602_19004/figures/004_Figure_3.jpg]]
*Figure 3: IMU→Video retrieval results on mRi (left) and Ego-Humans (right). Each example shows the query IMU signal, its corresponding ground-truth video segment, and the top three retrieved video segments. Our method successfully retrieves the ground-truth segment, and the other top-ranked results are also visually similar to the ground truth, demonstrating robust crossmodal alignment*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2602_19004/figures/005_Table_2.jpg]]
*Table 2: Synchronization results on three datasets. All models are evaluated on 20-second videos with random temporal offsets sampled uniformly from [−7, 7] seconds. Top-k retrieval is performed with*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2602_19004/figures/006_Figure_4.jpg]]
*Figure 4: Per-action synchronization accuracy on EgoHumans (left) and mRi (right). MoBind achieves sub-50ms error on all EgoHumans actions and under 1s on all mRi actions, despite the challenges posed by repetitive movements and near-duplicate segments. Results confirm MoBind’s robustness across diverse motion types and environments*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2602_19004/figures/007_Figure_5.jpg]]
*Figure 5: Examples of body-part localization on EgoHumans. Each column shows the query IMU (top) and the predicted body part with the highest similarity score (bottom), demonstrating accurate identification of sensor placement*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2602_19004/figures/008_Figure_6.jpg]]
*Figure 6: Results for the challenging combined task of temporal synchronization and spatial localization. The query 20s IMU signal from the left wrist precedes the video by 6.8 s. MoBind accurately recovers this offset using a weighted histogram and simultaneously localizes the signal to the correct body part, demonstrating robustness to dynamic and highly repetitive motion*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2602_19004/figures/009_Table_3.jpg]]
*Table 3: IMU-to-person identification in multi-person scenes from EgoHumans. This experiment evaluates who wears the IMU sensor, and MoBind achieves the highest accuracy and F1 score*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2602_19004/figures/011_Figure_7.jpg]]
*Figure 7: Robustness to Sensor Failure. Retrieval performance (R@1 and R@5) under different sensor availability conditions. R@k measures the percentage of queries for which the groundtruth video appears within the top-k retrieved results, given the representation computed from a subset of IMU sensors. In general, using more IMUs provides a more complete motion representation and thus improves retrieval accuracy. MoBind remains highly effective even when some sensors are unavailable, demonstrating strong performance under partial sensor input and highlighting its robustness for real-world deployment*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2602_19004/figures/012_Table_5.jpg]]
*Table 5: Ablation studies on contrastive objectives on mRi. Results show consistent gains across all tasks as each contrastive level is added, highlighting the effectiveness of the hierarchical design*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2602_19004/figures/013_Table_6.jpg]]
*Table 6: Effect of Masked Token Prediction on model performance. The MTP significantly improves action recognition on both datasets, demonstrating its importance for retaining actionlevel semantics*

## 方法谱系与知识库定位

### 1. 核心瓶颈与因果机制

现有IMU-视频跨模态对齐方法的核心瓶颈在于**对齐粒度的单一性**：无论是基于对比学习的**IMU2CLIP**（Moon et al., 2022）还是基于联合嵌入的**DeSPITE**（Kreutz et al., 2025），均仅在全局clip级别进行对齐，丢失了亚秒级时序同步信息。这种粗粒度对齐无法捕捉多传感器配置下身体部位的特异性动态，导致两个关键失败模式：(1) 细粒度跨模态检索中，同一动作类内的不同片段难以区分——在mRi数据集上，IMU2CLIP的R@1错误中有79%的top-1冒名顶替者属于相同动作类；(2) 精确时间同步几乎不可能，IMU2CLIP在mRi上的时间同步平均绝对误差高达4.95秒。

MoBind通过一个**三层因果控制机制**解决上述瓶颈：(1) **表示层**——将视频输入从原始RGB像素替换为2D骨骼运动序列，剥离无关视觉背景，使模型聚焦于运动本质；(2) **对齐层**——施加token级（亚秒窗口）、身体部位级和全局级三层层次化对比约束，同时控制细粒度时间同步和粗粒度语义保留；(3) **语义保持层**——通过Masked Token Prediction（MTP）辅助任务在IMU流上执行掩码预测，防止模型过度聚焦细粒度对齐而丢失动作类别语义。这一机制在TotalCapture上的动作识别微调准确率从0.55（无MTP）提升至0.72（有MTP），相对提升超过30%。

### 2. 方法谱系中的关键设计变迁

| 设计维度 | 基线方法 | MoBind | 变迁逻辑 |
|---------|---------|--------|---------|
| **视觉输入表示** | 原始RGB像素或光流（IMU2CLIP, SyncNet） | 从视频提取的2D骨骼运动序列，按IMU安装位置分解为局部身体部位轨迹 | 消除背景、光照等运动无关因素的干扰，使跨模态对齐聚焦于运动动力学本身 |
| **对齐粒度** | 单一全局clip级嵌入（IMU2CLIP, DeSPITE） | 三层对齐：token级（子秒）、局部身体部位级、全局级，联合训练 | 全局对齐保留语义，局部和token对齐实现亚秒级时序精度，三者互补而非替代 |
| **多传感器处理** | 简单拼接或多流独立处理（SyncNet, DeSPITE） | 每个IMU严格与对应身体部位配对进行局部对比学习，再聚合为全局表示 | 利用IMU安装位置的先验知识，实现语义上有根据的多传感器对齐 |
| **辅助任务** | 无 | Masked Token Prediction（MTP），在IMU流上随机遮蔽75%的token并预测 | 施加动作级语义约束，防止层次化对比学习过度聚焦细粒度对齐而坍塌动作类别信息 |
| **时间同步机制** | 基于相关性分析的偏移估计（SyncWISE, Zhang et al., 2020） | 基于双向top-k检索投票的加权直方图估计 | 利用已学到的细粒度对齐表示直接进行窗口级匹配，无需额外优化 |

### 3. 与相关工作的关系定位

**视听同步方法的改装**：**SyncNet**（Chung & Zisserman, ACCV Workshop 2016）原为视听同步设计，通过改装用于IMU-视频时间同步。SyncNet在mRi上取得1.89秒的MAE，显著优于IMU2CLIP的4.95秒，证明其基于窗口匹配的策略比全局对比学习更适合时间同步。然而，SyncNet仍依赖原始视觉输入，在细粒度对齐上受限。MoBind通过骨骼运动表示和层次化对比学习，将MAE进一步压缩至0.47秒，相对SyncNet提升75%。

**视觉-惯性定位的关联**：**VIPL**（Sun et al., 2020）面向视觉-惯性人员定位任务，在EgoHumans上取得0.754的人员识别准确率。MoBind在该任务上达到0.9812，提升超过22个百分点。这一差距源于VIPL依赖全局特征匹配，而MoBind的身体部位级对齐天然适合区分不同个体的局部运动模式。

**对比学习范式的演进**：MoBind的层次化InfoNCE损失设计（全局λ_g=1.0，局部λ_l=1.0，token级λ_t=0.5）体现了从单层到多层对比学习的范式演进。消融实验（Table 5）验证了这一设计的必要性：从仅全局对比逐步增加局部和token级对比，在所有任务上带来一致且显著的性能提升，证明三层对齐具有互补而非冗余的关系。

### 4. 适用边界与局限

**已知安装位置的假设依赖**：MoBind假设IMU传感器的身体部位安装位置已知，这在无约束佩戴场景中可能无法满足。当传感器位置标注不可用时（如用户随意佩戴的消费级设备），模型需要额外的自动发现机制，这是当前框架的明确边界。

**外部姿态估计器的误差传播**：方法依赖外部2D姿态估计器（如MMPose）从视频提取骨骼运动，其误差会传播至对齐性能。在遮挡、低光照或快速运动场景下，姿态估计精度下降将直接影响MoBind的表示质量。论文未在严重遮挡条件下进行系统评估，这一边界需要进一步验证。

**数据集覆盖的局限**：训练和评估均在实验室收集的数据集（mRi、TotalCapture、EgoHumans）上进行，与现实世界嘈杂、多变的运动分布可能存在差异。特别是，当前框架尚未在极端多人密集交互或严重遮挡的场景下进行大规模验证，泛化性待进一步检验。

**传感器数量的固定假设**：MoBind的架构设计假设传感器数量固定且与身体部位一一对应。在动态变化的传感器配置（如随身穿戴设备数量不固定）或传感器部分失效的场景下，虽然Figure 7显示MoBind在部分传感器可用时仍保持较强性能，但架构本身未针对可变传感器数量进行显式设计。

### 5. 开放问题

1. **无监督传感器-部位对应发现**：是否可以通过无监督方式自动发现IMU与身体部位的对应关系，而无需预先标注安装位置？这将显著降低部署成本并拓展应用场景。

2. **动态传感器配置的扩展**：如何将框架扩展至未知传感器数量或动态变化的传感器配置（如用户随意佩戴的可变数量设备）？这需要架构层面的灵活性设计，而非当前的固定配对方案。

3. **极端条件下的鲁棒性**：在严重视角变化、快速运动模糊和多人相互遮挡的情况下，细粒度时间同步能否保持高精度？当前在EgoHumans上所有动作的误差均低于50ms（Figure 4），但该数据集的动作复杂度有限。

4. **跨模态掩码预测的改进**：MTP辅助任务当前仅在IMU流上执行。是否可改进为跨模态的掩码预测（例如同时覆盖姿态token），以进一步提升语义保留？这可能在动作识别任务上带来额外增益。

5. **异步采样率的鲁棒对齐**：模型在何种程度上能够处理异步IMU采样率，以及如何实现跨采样率的鲁棒对齐？当前实验使用统一的采样率设置（5秒窗口，T=25个token），实际部署中不同传感器的采样率可能不一致。

## 原文 PDF

![[paperPDFs/CVPR_2026/MoBind_Motion_Binding_for_Fine_Grained_IMU_Video_Pose_Alignment.pdf]]