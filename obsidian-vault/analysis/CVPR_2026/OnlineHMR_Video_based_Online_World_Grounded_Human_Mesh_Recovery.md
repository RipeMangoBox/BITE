---
title: "OnlineHMR: Video-based Online World-Grounded Human Mesh Recovery"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/OnlineHMR_Video_based_Online_World_Grounded_Human_Mesh_Recovery.pdf
project_link: "https://tsukasane.github.io/Video-OnlineHMR/"
code_link: null
aliases:
- OnlineHMR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 关键设计包括：（1）滑动窗口训练与键值缓存推理，使相机坐标HMR具备因果在线能力；（2）基于人本的增量SLAM，通过软掩码剔除人体区域并利用EMA校正抑制相机轨迹抖动，实现在线世界对齐。
primary_logic: 将局部人体运动估计与全局轨迹恢复解耦为两个在线专家分支：相机坐标HMR利用短期时序融合与KV缓存实现因果推理，SLAM分支对人体区域施加软掩码并对相机姿态进行EMA平滑，从而在完全在线的条件下维持高保真度和时间一致性。
claims:
- OnlineHMR在3DPW和EMDB-1上的相机坐标精度（PA-MPJPE/MPJPE/PVE）与离线方法TRAM等相当，且显著优于其他在线方法。
- OnlineHMR在EMDB-2的世界坐标指标（WA-MPJPE 93.5, RTE 2.2）优于现有在线方法Human3R（WA-MPJPE 112.2, RTE 2.2），且与离线SOTA可比。
- OnlineHMR具备在线处理能力，平均延迟仅0.30秒/帧，而离线方法如SLAHMR延迟高达2435秒。
- 速度正则化损失有效降低了加速度误差和Jitter指标。
---

# OnlineHMR: Video-based Online World-Grounded Human Mesh Recovery

> [!tip] 核心洞察
> 将局部人体运动估计与全局轨迹恢复解耦为两个在线专家分支：相机坐标HMR利用短期时序融合与KV缓存实现因果推理，SLAM分支对人体区域施加软掩码并对相机姿态进行EMA平滑，从而在完全在线的条件下维持高保真度和时间一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | OnlineHMR：基于视频的在线世界坐标系人体网格恢复 |
| 英文题名 | OnlineHMR: Video-based Online World-Grounded Human Mesh Recovery |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.17355) · [Project](https://tsukasane.github.io/Video-OnlineHMR/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | OnlineHMR |
| Dataset | 3DPW, EMDB-1, EMDB-2 |

> [!tip] 效果简介
> - 3DPW (camera-coord) 上，PA-MPJPE↓ 43.7 vs 35.6 (TRAM, offline) (+8.1)。
> - EMDB-1 (camera-coord) 上，Accel↓ 9.0 vs 4.9 (TRAM, offline) (+4.1)。
> - EMDB-2 (world) 上，WA-MPJPE100↓ 93.5 vs 112.2 (Human3R, online) (-18.7)。

## 概述

从单目视频中恢复世界坐标系下的人体运动，是AR/VR、具身智能和人机交互等领域的核心需求。现有方法大多采用离线处理范式，依赖未来帧或全局优化来保证重建质量，无法满足实时交互场景的因果推理约束；少数在线方法则面临保真度不足、时间一致性差或效率低下的困境。核心瓶颈在于：如何在仅使用过去和当前信息的因果约束下，同时保证相机坐标系人体估计的准确性与时序平滑性，并消除SLAM中人体区域导致的动态干扰。

针对上述问题，本文提出 **OnlineHMR**，一个完全在线的世界坐标系人体网格恢复框架。其核心洞察是将局部人体运动估计与全局轨迹恢复解耦为两个在线专家分支：**相机坐标HMR分支**利用滑动窗口训练与键值缓存（KV Cache）机制实现因果推理，在短期时序窗口内融合空间与运动信息；**人本增量SLAM分支**则通过软人体掩码剔除动态区域，并利用指数移动平均（EMA）校正抑制相机轨迹抖动，从而在完全在线的条件下维持高保真度和时间一致性。

实验表明，OnlineHMR在相机坐标精度上与离线方法可比——3DPW上PA-MPJPE达43.7 mm（离线TRAM为35.6 mm），同时显著优于其他在线方法；在世界坐标评估中，EMDB-2上的WA-MPJPE为93.5 mm，优于在线方法Human3R（112.2 mm），且平均延迟仅0.30秒/帧，远低于离线方法SLAHMR的2435秒。速度正则化损失和软掩码策略被消融实验证实为关键设计：前者将3DPW加速度误差从8.6降至6.4，Jitter从28.1降至19.5；后者使世界坐标WA-MPJPE从119.6（无掩码）降至93.5。

方法仍存在局限：对重复纹理和动态环境敏感，SLAM易引入漂移；假设连续相机视角，无法处理突变或多相机切换；当前约3.3 FPS的运行速度尚不足以满足实时交互需求。

## 背景与动机

从单目视频中恢复三维人体运动是计算机视觉领域的核心任务之一，在虚拟现实、人机交互、运动分析等场景中具有广泛的应用需求。近年来，基于参数化人体模型（如SMPL）的人体网格恢复（Human Mesh Recovery, HMR）取得了显著进展，能够在相机坐标系下估计出较为准确的人体姿态和形状。然而，仅获得相机坐标系下的局部人体运动远不足以支撑真实世界的交互应用——要将虚拟角色或分析结果锚定于物理空间，必须同时恢复人体在世界坐标系下的全局轨迹。

### 离线方法的成熟与局限

当前世界坐标系人体网格恢复的主流方法多为离线处理范式。**TRAM**（Wang et al., ECCV 2024）、**GVHMR**（Wang et al., CVPR 2024）、**GLAMR**（Yuan et al., CVPR 2022）等方法通过对完整视频序列进行全局优化，在3DPW、EMDB等基准上取得了出色的重建精度。以**SLAHMR**（Ye et al., CVPR 2023）为代表的优化方法更进一步，通过后处理精调全局轨迹，但单段视频的处理延迟可高达数千秒。这些离线方法的根本局限在于：它们需要访问未来帧信息才能完成推理，无法满足实时交互、直播分析、在线AR等对低延迟有严格要求的应用场景。

### 在线方法的缺口与挑战

在在线设定下，系统只能利用过去和当前帧的信息进行因果推理，这带来了三重核心挑战：

1. **相机坐标估计的精度-时序权衡**：现有在线相机坐标HMR方法（如**TRACE**）虽能实现逐帧推理，但在保真度和时间一致性上明显落后于离线方法。离线方法通过双向时序融合（chunk-based）获得的平滑性和准确性，在因果约束下难以直接复现。

2. **SLAM中的动态干扰**：世界坐标系对齐依赖于SLAM系统提供的相机轨迹。然而，标准SLAM（如DROID-SLAM、MASt3R-SLAM）假设场景为静态，人体区域的运动特征会严重污染特征匹配与位姿估计，导致轨迹漂移和抖动。部分方法（如**WHAM**）将相机坐标HMR在线化，但其全局轨迹恢复仍依赖离线后处理。

3. **在线世界对齐的时效性**：现有唯一的在线世界坐标系方法**Human3R**虽支持因果推理，但其世界坐标重建质量（WA-MPJPE 112.2 mm）与离线SOTA（TRAM 76.4 mm）存在显著差距，且轨迹压缩、聚集等问题在定性结果中频繁出现。

### 本文动机

上述分析揭示了一个明确的方法缺口：**在完全在线的因果约束下，如何同时保证相机坐标系人体估计的高保真度、时间一致性，以及世界坐标系对齐的准确性？** 核心瓶颈在于——局部人体运动估计与全局相机轨迹恢复这两个子问题，在在线设定下需要被解耦为两个独立但协同的专家分支，而非沿用离线方法中“先完整估计再全局对齐”的耦合范式。

为此，本文提出**OnlineHMR**，一个完全在线的世界坐标系人体网格恢复框架。其设计思想是：将相机坐标HMR与增量SLAM构建为两个因果推理分支——前者通过滑动窗口训练与键值缓存（KV Cache）机制实现短期时序融合下的高精度人体估计，后者通过软人体掩码与EMA轨迹校正抑制动态干扰和相机抖动，最终在仅依赖历史信息的条件下实现与离线方法可比的全局重建质量。

## 核心创新

OnlineHMR 的核心创新在于将**在线因果推理**引入世界坐标系人体网格恢复，通过解耦的双分支架构与三项关键设计，在仅使用过去与当前帧的严格因果约束下，实现了与离线方法可比的精度和显著优于现有在线方法的时间一致性。

### 1. 因果在线相机坐标 HMR：滑动窗口训练与 KV 缓存推理

现有视频 HMR 方法（如 **TCMR**、**TRAM** (Wang et al., ECCV 2024)）多采用离线 chunk-based 策略，需依赖未来帧进行时序融合。OnlineHMR 将这一范式彻底改造为因果在线模式：

- **滑动窗口训练**：将输入序列切分为步长为 1 的重叠窗口，在每个窗口内通过自注意力和交叉注意力融合时空信息。窗口内最后一帧对前序帧进行交叉注意力，使模型学会从历史帧中提取运动线索，而不依赖未来信息。
- **键值缓存（KV Cache）推理**：推理时，维护一个存储前序帧特征的键值缓存。当前帧仅需与缓存中的键值进行交叉注意力计算，避免了重复编码历史帧，实现了真正的逐帧流式推理。

这一设计使相机坐标 HMR 在在线推理模式下仍能达到 **PA-MPJPE 43.7 mm**（3DPW）和 **46.0 mm**（EMDB-1），与离线方法 TRAM 的 35.6/45.7 mm 差距可控，同时显著优于其他在线方法（Table 1）。

### 2. 以人为中心的增量 SLAM：软掩码与 EMA 轨迹校正

世界坐标系对齐的核心挑战在于 SLAM 系统容易受到人体区域动态特征的干扰，导致相机轨迹估计漂移。OnlineHMR 提出了两项针对性设计：

- **软置信掩码**：对语义分割的人体区域施加膨胀和高斯模糊，生成边界渐变的软掩码，而非简单的二值硬掩码。这使 SLAM（基于 **MASt3R-SLAM**）在剔除人体动态区域的同时，保留边界附近的场景结构信息，避免硬掩码带来的信息断裂。消融实验表明，软掩码策略在 EMDB-2 上获得 **WA-MPJPE 93.5 mm**，显著优于硬掩码（112.6 mm）和无掩码（119.6 mm）方案（Table 8）。
- **EMA 轨迹校正**：对增量 SLAM 输出的相机平移施加指数移动平均平滑，并结合速度相关钳位抑制高频抖动。定性结果显示，EMA 校正明显减少了相机轨迹和世界坐标系人体平移的抖动（Figure 10）。

### 3. 时间一致性约束：速度正则化与频谱域评估

传统帧级监督缺乏显式时序约束，容易产生帧间抖动。OnlineHMR 引入了：

- **速度正则化损失**：惩罚相邻帧关节位置差异，直接优化运动平滑性。消融实验表明，该损失使 3DPW 上的加速度误差（Accel）从 8.6 降至 6.4，Jitter 指标从 28.1 降至 19.5（Table 4）。
- **频谱域抖动度量**：提出基于短时傅里叶变换（STFT）的频谱图分析方法，将运动序列变换到时间-频率域，通过频谱差异（RMSE/Corr）量化抖动程度。这为时间一致性的评估提供了比传统加速度指标更细粒度的频域视角（Eq. 15, Table 6）。

### 方法谱系与知识库定位

OnlineHMR 继承并改造了 **TRAM** 的框架，将其从离线 chunk-based 扩展为在线因果推理。在 SLAM 侧，它用增量式 MASt3R-SLAM 替代了全局优化 SLAM（如 DPVO、DROID-SLAM），并通过人本掩码策略解耦动态人体与静态场景。与现有在线世界坐标方法 **Human3R** 相比，OnlineHMR 在 EMDB-2 上的 WA-MPJPE 降低 18.7 mm（93.5 vs 112.2），且平均延迟仅 0.30 秒/帧，远低于离线方法（如 **SLAHMR** (Ye et al., CVPR 2023) 的 2435 秒、TRAM 的 115.95 秒），确立了在线世界坐标系 HMR 的新基准（Table 2, Table 3）。

## 整体框架

OnlineHMR 采用**双分支在线推理架构**，将局部人体运动估计与全局相机轨迹恢复解耦为两个并行专家分支，最终通过世界坐标对齐实现流式单目视频中的人体网格重建。

### 输入输出规范

系统接收**流式单目RGB视频**作为输入，逐帧处理。对于每一帧 $i$，输出包含两部分：

- **相机坐标系人体网格** $\mathbf{M}_i^{\mathrm{c}}$：由 SMPL 参数化模型 $\mathbf{M}_i = \mathcal{M}(\beta_i, \pmb{\theta}_i)$ 生成，其中 $\beta_i$ 为体型参数，$\pmb{\theta}_i$ 为姿态参数。
- **世界坐标系人体网格** $\mathbf{M}_i^{\mathrm{w}}$：通过相机位姿变换将相机坐标系网格投影到世界坐标系：
  $$\mathbf{M}_i^{\mathrm{w}} = \mathbf{R}(\mathbf{q}_i^{\mathrm{c}}) \cdot \mathbf{M}_i^{\mathrm{c}} + s \cdot \mathbf{t}_i^{\mathrm{c}}$$
  其中 $\mathbf{q}_i^{\mathrm{c}}$ 为相机旋转四元数，$\mathbf{t}_i^{\mathrm{c}}$ 为相机平移向量，$s$ 为度量尺度因子。

### 双分支流水线

框架由两个核心模块构成，在因果约束下协同工作：

**分支一：相机坐标系 HMR（Camera-coordinate HMR Branch）**

该分支负责从 RGB 帧中恢复相机坐标系下的高保真 SMPL 人体网格。其核心设计包括：

1. **ViT Backbone**：将每帧图像切分为 patch 并提取视觉特征。
2. **滑动窗口时序融合**：将输入序列切分为步长为 1 的重叠窗口，在每个窗口内通过注意力机制融合时空信息。当前帧的 query 与历史帧的缓存 key/value 进行交叉注意力：
   $$\mathbf{A}_{\mathrm{cross}} = \mathrm{Softmax}\left(\frac{\mathbf{q}_i \mathbf{k}_{\mathrm{prev}}^{\top}}{\sqrt{d}}\right) \mathbf{v}_{\mathrm{prev}}$$
3. **KV 缓存机制**：推理时存储先前帧提取的特征，使当前帧仅需访问缓存即可完成时序融合，无需等待未来帧，实现完全因果的在线推理。
4. **SMPL Head**：将融合后的特征 query 送入回归头，输出单帧 SMPL 姿态和体型参数。

**分支二：人本增量 SLAM（Human-centric Incremental SLAM）**

该分支负责在线估计相机在世界坐标系中的轨迹，并消除人体区域对 SLAM 的干扰：

1. **增量式 MASt3R-SLAM**：采用前端跟踪与后端图优化相结合的方式，增量输出相机位姿，避免离线方法所需的全局优化。
2. **软人体掩码**：对语义分割得到的人体区域 $C_i^h$ 进行膨胀和高斯模糊，生成软边界置信掩码 $C_i^{\mathrm{soft}}$：
   $$C_i^{\mathrm{soft}} = \frac{G_{\sigma} * (C_i^h \oplus S_k^{(n)})}{\max_p \left(G_{\sigma} * (C_i^h \oplus S_k^{(n)})\right)}$$
   该掩码以连续值而非硬边界的方式降低人体区域在 SLAM 特征匹配中的权重，避免因人体运动引入动态干扰。
3. **EMA 轨迹校正**：对 SLAM 输出的相机平移 $\mathbf{t}_i$ 应用指数移动平均平滑：
   $$\mathbf{t}_i' = \bar{\mathbf{t}}_i + \alpha \Delta \mathbf{t}_i$$
   结合速度相关钳位抑制高频抖动，提升相机轨迹的时间一致性。
4. **度量深度估计器（MoGe-V2）**：预测单帧度量深度，与 SLAM 深度图联合计算尺度因子 $s$，确保世界坐标对齐的尺度一致性。

### 在线推理流程

推理时，两个分支并行运行：相机坐标 HMR 分支利用 KV 缓存仅需当前帧和历史缓存即可输出人体网格；SLAM 分支增量更新相机位姿。最后，将相机坐标系人体网格通过当前帧的相机位姿和尺度因子变换到世界坐标系，完成在线世界坐标系人体运动恢复。整个流程的平均延迟仅为 **0.30 秒/帧**，而离线方法如 SLAHMR 平均延迟高达 2435 秒（Table 3）。

### 训练策略

训练阶段采用**滑动窗口学习**（Figure 3），将完整序列切分为重叠窗口进行监督，同时在窗口内施加**速度正则化损失** $\mathcal{L}_v$ 以惩罚相邻帧关节位置的剧烈变化，缓解推理时的时序抖动。模型在 BEDLAM、3DPW 和 H3.6M 数据集上联合训练，约 52K 迭代收敛，使用单张 Nvidia 80GB H100 GPU 完成。

### 补充图表

![[assets/figures/papers/paper_list_l1032_https_arxiv_org_abs_2603_17355/figures/001_Figure_1.jpg]]
*Figure 1: An in-the-wild example of our framework. Given a streaming monocular RGB video, our method leverages a two-branch inference to recover the world-grounded human motion in an online manner*

## 核心模块与公式推导

OnlineHMR 的核心架构由两个在线专家分支构成：**相机坐标系人体网格恢复（Camera-coordinate HMR）** 与 **以人为中心的增量式 SLAM（Human-centric Incremental SLAM）**。前者负责从流式视频中因果性地估计 SMPL 参数，后者负责在剔除人体动态干扰后增量恢复相机轨迹。两者解耦并行，最终通过世界坐标变换实现全局人体运动恢复。

### 3.1 世界坐标变换基础

SMPL 模型将姿态参数 $\pmb{\theta}_i$ 和形状参数 $\beta_i$ 映射为相机坐标系下的人体网格：

$$\mathbf{M}_i = \mathcal{M}(\beta_i, \pmb{\theta}_i)$$

其中 $\mathbf{M}_i$ 为第 $i$ 帧的顶点坐标。相机坐标系到世界坐标系的刚性变换由旋转四元数 $\mathbf{q}_i^c$、平移向量 $\mathbf{t}_i^c$ 和尺度因子 $s$ 决定：

$$\mathbf{M}_i^{\mathrm{w}} = \mathbf{R}(\mathbf{q}_i^{\mathrm{c}}) \cdot \mathbf{M}_i^{\mathrm{c}} + s \cdot \mathbf{t}_i^{\mathrm{c}}$$

该公式是双分支输出的融合接口：$\mathbf{M}_i^{\mathrm{c}}$ 由 HMR 分支提供，$\mathbf{q}_i^{\mathrm{c}}$、$\mathbf{t}_i^{\mathrm{c}}$ 和 $s$ 由 SLAM 分支与度量深度估计器联合提供。

### 3.2 相机坐标 HMR：滑动窗口训练与 KV 缓存推理

该分支的核心挑战在于：如何在仅访问过去帧的因果约束下，实现与离线方法相当的时序融合能力。

**滑动窗口训练。** 训练时将输入序列切分为步长为 1 的重叠窗口。窗口内，ViT Backbone 提取各帧图像特征后，最后一帧通过自注意力与交叉注意力融合时空信息。帧级监督损失为：

$$\mathcal{L}_f = \lambda_1 \mathcal{L}_{2D} + \lambda_2 \mathcal{L}_{3D} + \lambda_3 \mathcal{L}_{\mathrm{SMPL}} + \lambda_4 \mathcal{L}_V$$

其中 $\mathcal{L}_{2D}$、$\mathcal{L}_{3D}$、$\mathcal{L}_{\mathrm{SMPL}}$、$\mathcal{L}_V$ 分别为 2D/3D 关键点、SMPL 参数和顶点损失。

**速度正则化。** 为抑制帧间抖动，引入速度正则化损失，惩罚相邻帧关节位置差异：

$$\mathcal{L}_v = \lambda_5 \frac{\sum_{i,t} c_{i,t} \|\mathbf{p}_{i,t} - \mathbf{p}_{i,t-1}\|_2^2}{\sum_{i,t} c_{i,t} + \epsilon}$$

其中 $c_{i,t}$ 为关节置信度，$\mathbf{p}_{i,t}$ 为第 $i$ 帧第 $t$ 个关节位置。消融实验（Table 4）表明，该损失使 3DPW 上的加速度误差从 8.6 降至 6.4，Jitter 指标从 28.1 降至 19.5。

**KV 缓存推理。** 推理时，将历史帧的特征以键值对形式缓存。当前帧查询 $\mathbf{q}_i$ 与缓存的历史键 $\mathbf{k}_{\mathrm{prev}}$、值 $\mathbf{v}_{\mathrm{prev}}$ 进行交叉注意力：

$$\mathbf{A}_{\mathrm{cross}} = \mathrm{Softmax}\left(\frac{\mathbf{q}_i \mathbf{k}_{\mathrm{prev}}^{\top}}{\sqrt{d}}\right) \mathbf{v}_{\mathrm{prev}}$$

该机制使模型无需重复计算历史帧特征，在保持因果性的同时实现高效时序融合。融合后的查询特征送入 SMPL Head 回归姿态和形状参数。

### 3.3 以人为中心的增量 SLAM

SLAM 分支的核心挑战在于：人体区域是动态特征，会严重干扰视觉 SLAM 的特征匹配与位姿优化。

**软置信掩码。** 对语义分割得到的人体二值掩码 $C_i^h$，依次进行膨胀和高斯模糊，生成软边界掩码：

$$C_i^{\mathrm{soft}} = \frac{G_{\sigma} * (C_i^h \oplus S_k^{(n)})}{\max_p (G_{\sigma} * (C_i^h \oplus S_k^{(n)}))}$$

其中 $\oplus$ 为膨胀操作，$G_{\sigma}$ 为高斯核，$S_k^{(n)}$ 为结构元素。该软掩码作为置信度权重输入 MASt3R-SLAM 的前端跟踪，使 SLAM 在人体边界区域平滑降权，而非硬性剔除。消融实验（Table 8）表明，软掩码策略在 EMDB-2 上取得 WA-MPJPE 93.5，显著优于硬掩码（112.6）和无掩码（119.6）。

**度量深度与尺度恢复。** 采用 MoGe-V2 估计单帧度量深度，与 SLAM 深度图对齐计算尺度因子 $s$，解决单目 SLAM 的尺度模糊问题。

**EMA 轨迹校正。** 增量 SLAM 的相机平移易出现高频抖动。通过指数移动平均对平移进行平滑：

$$\mathbf{t}_i' = \bar{\mathbf{t}}_i + \alpha \Delta \mathbf{t}_i$$

其中 $\bar{\mathbf{t}}_i$ 为 EMA 平滑后的平移，$\Delta \mathbf{t}_i$ 为帧间位移，$\alpha$ 为与速度相关的钳位系数。定性结果（Figure 10）显示，EMA 校正明显减少了相机轨迹和世界坐标系人体平移的抖动。

### 3.4 频谱域抖动评估

为定量评估时序平滑性，提出基于短时傅里叶变换的频谱抖动表示。对运动序列 $\mathbf{y}$ 应用 STFT：

$$\mathbf{S}(i, f) = \left| \sum_{k=0}^{L-1} \mathbf{y}(k) w(k-i) e^{-j 2\pi f k / N_w} \right|$$

其中 $w$ 为窗函数，$N_w$ 为窗口长度。通过计算预测序列与真值序列的频谱差异（Figure 8），可在时间-频率域定位抖动频段。收敛模型（52K 迭代）的频谱差异显著小于未收敛模型（1K 迭代），验证了训练过程对时序一致性的改善。

### 补充图表

![[assets/figures/papers/paper_list_l1032_https_arxiv_org_abs_2603_17355/figures/003_Figure_3.jpg]]
*Figure 3: Sliding window learning pipeline. The input sequence is sliced to overlapping windows, learning spatial and temporal information fusion inside each window, and alleviate jitter effect through velocity regularization*

## 实验与分析

### 实验设置

OnlineHMR 使用 **BEDLAM**、**3DPW** 和 **H3.6M** 三个数据集联合训练，模型在约 **52K 次迭代**时收敛。训练在单张 Nvidia 80GB H100 GPU 上进行（Sec. 4.2）。评估涵盖相机坐标系与世界坐标系两个层面：相机坐标精度在 **3DPW** 和 **EMDB-1** 上测量 PA-MPJPE、MPJPE、PVE 与加速度误差（Accel）；世界坐标评估在 **EMDB-2** 上进行，指标包括 WA-MPJPE、W-MPJPE、RTE（相对平移误差，%）和 ERVE（末端根速度误差，mm/frame）。效率对比中，离线方法的平均延迟定义为 $\text{average delay} = \frac{F-1}{2 \times \text{FPS}}$，总延迟与视频长度 $F$ 线性相关。

### 相机坐标精度对比

Table 1 报告了相机坐标系 HMR 的主结果。OnlineHMR 在完全在线的因果约束下，取得了与离线方法可比甚至更优的性能：

![[assets/figures/papers/paper_list_l1032_https_arxiv_org_abs_2603_17355/figures/004_Table_1.jpg]]
*Table 1: Comparison of camera coordinates HMR results using different models on 3DPW and EMDB-1 dataset. All metrics are in mm*

- **3DPW 数据集**：OnlineHMR 的 PA-MPJPE 为 43.7 mm，MPJPE 为 69.9 mm，PVE 为 83.7 mm。作为参考，离线方法 **TRAM**（Wang et al., ECCV 2024）的 PA-MPJPE 为 35.6 mm，**GVHMR**（Wang et al., CVPR 2024）为 47.2 mm。OnlineHMR 显著优于其他在线方法（如 **TRACE**、**TCMR** 等），且与离线 SOTA 的差距控制在合理范围内。
- **EMDB-1 数据集**：OnlineHMR 的 PA-MPJPE 为 46.0 mm，MPJPE 为 74.0 mm，PVE 为 86.1 mm，与 TRAM（PA-MPJPE 45.7 mm）几乎持平，大幅领先于其他在线方法。
- **时间一致性**：在 3DPW 上 Accel 指标为 6.4 mm/frame²，优于 GVHMR（9.4）和多数离线方法，仅略逊于 TRAM（4.9）。EMDB-1 上 Accel 为 9.0 mm/frame²，仍处于在线方法中的最优水平。

**关键结论**：在仅使用过去和当前帧的因果推理条件下，OnlineHMR 的相机坐标精度和时间平滑性均达到或接近离线 chunk-based 方法的水平，验证了滑动窗口训练与 KV 缓存机制的有效性。

### 世界坐标精度对比

Table 2 展示了 EMDB-2 上的世界坐标系评估结果。OnlineHMR 在所有在线方法中表现最优：

- **WA-MPJPE**：93.5 mm，显著优于在线竞争对手 **Human3R**（112.2 mm），与离线方法 **TRAM**（76.4 mm）和 **SLAHMR**（Ye et al., CVPR 2023，84.1 mm）的差距主要源于尺度转换精度的影响。
- **RTE**：2.2%，与 Human3R 持平，表明相机轨迹恢复的准确性相当。
- **ERVE**：3.8 mm/frame，优于 Human3R（4.5），反映末端根节点速度估计更稳定。

Figure 4 和 Figure 5 提供了 EMDB-2 同一视频上 OnlineHMR 与 Human3R 的定性对比：经过世界坐标对齐后，OnlineHMR 恢复的全局人体姿态与真值更为吻合。Figure 12 的自定义舞者视频进一步显示，OnlineHMR 忠实重建了人体运动轨迹，而 Human3R 的轨迹出现压缩和聚集现象。

![[assets/figures/papers/paper_list_l1032_https_arxiv_org_abs_2603_17355/figures/006_Figure_4.jpg]]
*Figure 4: Quantitative comparison of OnlineHMR and Human3R on the same EMDB-2 video with ground truth after world coordinate alignments*

![[assets/figures/papers/paper_list_l1032_https_arxiv_org_abs_2603_17355/figures/007_Figure_5.jpg]]
*Figure 5: Quantitative comparison of OnlineHMR and Human3R on the same EMDB-2 video with ground truth after world coordinate alignments*

**关键结论**：基于人本的增量 SLAM（软掩码 + EMA 校正）使 OnlineHMR 在世界坐标恢复上大幅领先现有在线方法，同时逼近离线 SOTA 的全局形状恢复能力。

### 效率对比

Table 3 报告了世界坐标 HMR 方法的效率。OnlineHMR 的**平均延迟仅 0.30 秒/帧**，运行速度约 **3.3 FPS**。相比之下，离线优化方法 **SLAHMR** 的平均延迟高达 2435 秒，**TRAM** 为 115.95 秒，**GLAMR**（Yuan et al., CVPR 2022）为 17.31 秒。部分在线方法 **WHAM** 的相机坐标分支虽可达 20+ FPS，但其全局轨迹恢复仍依赖离线后处理。

![[assets/figures/papers/paper_list_l1032_https_arxiv_org_abs_2603_17355/figures/008_Table_3.jpg]]
*Table 3: Efficiency comparison of world coordinate HMR methods. The average delay time is presented in seconds*

**关键结论**：OnlineHMR 是首个在保持高保真度的同时实现亚秒级延迟的完全在线世界坐标 HMR 框架，满足交互应用需求。

### 消融实验

#### 速度正则化损失

Table 4 验证了速度正则化项 $\mathcal{L}_v$ 的作用。加入速度正则化后，3DPW 上的 Accel 从 8.6 降至 **6.4** mm/frame²，Jitter 指标从 28.1 降至 **19.5**，证明显式的帧间速度约束有效抑制了高频抖动。Figure 8 的频谱差异图进一步佐证：收敛模型（52K 迭代）与真值的频谱差异显著小于未充分训练的模型（1K 迭代），表明时间-频率域的对齐程度随训练改善。

![[assets/figures/papers/paper_list_l1032_https_arxiv_org_abs_2603_17355/figures/011_Table_4.jpg]]
*Table 4: The comparison of jittering effect w/ or w/o the velocity regularization*

![[assets/figures/papers/paper_list_l1032_https_arxiv_org_abs_2603_17355/figures/012_Figure_8.jpg]]
*Figure 8: Difference spectrograms computed as GT-Pred, visualizing discrepancies in the time–frequency domain. The left figure corresponds to a model trained for 1K iterations, and the right for 52K iterations. Lower values (darker/closer to zero) indicate better alignment with the ground truth. The converged model (52K) exhibits substantially reduced differences*

#### 滑动窗口尺寸

Table 7 消融了滑动窗口大小（SWS）对相机坐标指标的影响。窗口大小为 **4** 时取得最优 PA-MPJPE 和 MPJPE，但进一步增大窗口会导致 Accel 上升——更大的时序感受野虽能融合更多上下文，但也引入了过度平滑的风险，使模型对快速运动变化的响应变迟钝。

![[assets/figures/papers/paper_list_l1032_https_arxiv_org_abs_2603_17355/figures/014_Table_7.jpg]]
*Table 7: Ablation study on sliding window size (SWS)*

#### SLAM 掩码策略

Table 5 和 Table 8 分别从 SLAM 轨迹精度和世界坐标人体重建两个角度消融掩码策略。在 MASt3R-SLAM 上：

![[assets/figures/papers/paper_list_l1032_https_arxiv_org_abs_2603_17355/figures/010_Table_5.jpg]]
*Table 5: Comparison of ATE using different masking strategies for DROID-SLAM and MAST3R-SLAM. Lower is better*

- **软掩码（Soft Mask）**：WA-MPJPE 为 93.5 mm，W-MPJPE 和 RTE 均最优。
- **硬掩码（Hard Mask）**：WA-MPJPE 升至 112.6 mm，性能显著下降。
- **无掩码（Vanilla）**：WA-MPJPE 进一步恶化至 119.6 mm。

软掩码通过对人体分割区域进行膨胀和高斯模糊，生成平滑的置信度过渡带，既剔除了动态人体对 SLAM 特征匹配的干扰，又避免了硬边界截断带来的特征断裂。Table 5 的 ATE 对比表明，软掩码在 DROID-SLAM 和 MASt3R-SLAM 上均获得最低的绝对轨迹误差。

#### EMA 校正

Figure 10 的定性对比显示，启用 EMA 校正后相机轨迹和世界坐标系人体平移的抖动明显减少。EMA 通过对平移量施加指数移动平均和速度相关钳位，有效抑制了增量 SLAM 中高频噪声的累积。

![[assets/figures/papers/paper_list_l1032_https_arxiv_org_abs_2603_17355/figures/016_Figure_10.jpg]]
*Figure 10: Qualitative results w/ and w/o EMA correction on custom videos*

#### 频谱域指标

Table 6 报告了频谱域评估的 RMSE 和相关性（Corr）指标。OnlineHMR 在频谱域与真值的 RMSE 更低、相关性更高，优于 **GVHMR** 和 **TRAM**，表明其在频率维度上的运动恢复更接近真实运动模式。

### 失败模式与局限性

Figure 11 展示了典型失败案例，主要集中于以下场景：

1. **重复纹理与动态环境**：低纹理墙面、阴影变化等导致 SLAM 特征匹配失效，引入轨迹漂移。
2. **相机视角突变**：方法假设连续平滑的相机运动，无法处理镜头切换或多相机设置。
3. **小尺寸人体**：当人体在画面中占比过小时，语义分割掩码可能不完整，软掩码策略失效，导致 SLAM 仍受动态区域干扰。
4. **尺度估计误差**：W-MPJPE 指标受度量深度估计（MoGe-V2）的尺度因子 $s$ 精度影响，在深度歧义场景下可能偏大。
5. **实时性瓶颈**：当前 3.3 FPS 受限于增量 MASt3R-SLAM 的计算开销，距离实时交互（>15 FPS）仍有差距。

这些失败模式揭示了系统对 SLAM 前端质量的强依赖性，以及掩码策略在极端人体尺度下的脆弱性，为后续研究指明了改进方向。

### 补充图表

![[assets/figures/papers/paper_list_l1032_https_arxiv_org_abs_2603_17355/figures/009_Figure_6.jpg]]
*Figure 6: Visualization of multi-individual, diverse scene cases. More examples are in Suppl*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

OnlineHMR 直接继承并扩展了 **TRAM** (Wang et al., ECCV 2024) 的离线世界坐标系人体网格恢复框架。TRAM 采用分块（chunk‑based）处理，依赖未来帧的全局优化来获得高保真重建，但无法满足流式交互需求。OnlineHMR 的核心改造在于将这一范式转化为**完全在线的因果推理系统**：通过滑动窗口训练与键值缓存（KV Cache）机制，使相机坐标 HMR 分支仅依赖过去和当前信息即可完成推理，从而在保持与离线方法可比精度的同时，将平均延迟从 TRAM 的约 116 秒降至 0.30 秒/帧（Table 3）。

在世界坐标系对齐层面，OnlineHMR 与三类方法形成对照：

- **离线世界坐标系 HMR**：包括 **GLAMR** (Yuan et al., CVPR 2022)、**SLAHMR** (Ye et al., CVPR 2023)、**GVHMR** (Wang et al., CVPR 2024)、**PHMR** 等。这些方法通过全局优化或未来帧信息获得最优指标（如 TRAM 在 EMDB‑2 上 WA‑MPJPE 为 76.4），但延迟随视频长度线性增长，SLAHMR 的平均延迟高达 2435 秒，不具备在线能力。
- **部分在线方法**：**WHAM** 在相机坐标 HMR 上实现在线推理，但全局轨迹恢复仍依赖离线后处理。OnlineHMR 将两个分支均实现在线化，填补了这一空白。
- **在线世界坐标系 HMR**：**Human3R** 是当前唯一可比的在线方法。OnlineHMR 在 EMDB‑2 上的 WA‑MPJPE（93.5 vs 112.2）和 RTE（2.2 vs 2.2）均优于或持平 Human3R，同时通过软人体掩码与 EMA 轨迹校正显著抑制了相机轨迹抖动。

在相机坐标 HMR 层面，OnlineHMR 与 **TRACE**（在线）以及 **TCMR**、**GLoT**（离线 chunk‑based）等视频 HMR 方法形成竞争。Table 1 显示，OnlineHMR 在 3DPW 上 PA‑MPJPE 为 43.7，优于所有其他在线方法，与离线 TRAM（35.6）的差距主要源于因果约束下无法访问未来帧。

### 2. 适用边界与局限

OnlineHMR 的设计隐含以下适用前提与边界：

1. **连续相机视角假设**：SLAM 分支（增量式 MASt3R‑SLAM）依赖帧间连续性进行前端跟踪与后端图优化。当输入视频存在相机视角突变或多相机切换时，SLAM 的位姿估计容易失效，导致世界坐标系对齐错误。这是当前系统的主要适用边界。

2. **对重复纹理与动态环境的敏感性**：尽管软人体掩码可剔除大部分动态干扰，但在重复纹理（如纯色墙壁、棋盘格地板）或复杂动态环境（如剧烈阴影变化）中，SLAM 仍可能引入漂移。Figure 11 展示了此类失败案例，表明系统在纹理贫乏场景下的鲁棒性有限。

3. **度量尺度转换精度**：世界坐标指标 W‑MPJPE 依赖于 MoGe‑V2 估计的度量深度与 SLAM 深度图之间的尺度因子 $s$。当深度估计误差较大时，W‑MPJPE 可能偏大，不能完全反映轨迹和姿态的全局形状恢复质量。论文指出 WA‑MPJPE（对齐完整序列后评估）更能体现实际性能。

4. **人体区域较小时的掩码失效**：当人体在画面中占比过小，语义分割掩码可能不完整或缺失，导致 SLAM 无法有效剔除人体动态特征，进而引起相机轨迹抖动。

5. **实时性瓶颈**：当前系统整体 FPS 约 3.3，受限于增量 SLAM（MASt3R‑SLAM）的计算开销。这距离实时交互（>15 FPS）仍有较大差距，限制了在低延迟场景（如 VR/AR）中的直接部署。

### 3. 开放问题

论文的实验与设计留下若干值得进一步探索的方向：

- **多相机与视角突变鲁棒性**：如何增强系统对相机切换或非连续视角输入的适应能力，是扩展应用场景的关键。可能的思路包括引入全局重定位模块或与多相机标定信息融合。

- **SLAM 计算瓶颈的突破**：当前 MASt3R‑SLAM 是系统延迟的主要来源。能否通过轻量化 SLAM 前端（如稀疏特征跟踪替代稠密匹配）或异步流水线设计，将 FPS 提升至实时水平，是在线世界坐标系 HMR 走向实用的核心挑战。

- **多人场景的在线解耦**：Figure 6 展示了多人场景的初步可视化，但论文未提供多人情况下的定量评估。如何在在线约束下实现多人身份保持、轨迹解耦与个体跟踪，是后续工作的重要方向。

- **频谱域抖动指标的标准化**：论文提出的基于短时傅里叶变换的频谱抖动表示（Eq. 15）提供了比 Accel/Jitter 更细粒度的时序一致性评估。该指标能否标准化为与任务无关的通用评估协议，值得社区进一步讨论。

- **EMA 校正参数的自适应调节**：当前 EMA 平滑的参数（$\alpha$、窗口 $B$）为固定值。在不同运动速度（如行走 vs 奔跑）下，最优平滑强度可能不同。自适应调节策略有望进一步提升轨迹平滑性与运动保真度之间的平衡。

## 原文 PDF

![[paperPDFs/CVPR_2026/OnlineHMR_Video_based_Online_World_Grounded_Human_Mesh_Recovery.pdf]]