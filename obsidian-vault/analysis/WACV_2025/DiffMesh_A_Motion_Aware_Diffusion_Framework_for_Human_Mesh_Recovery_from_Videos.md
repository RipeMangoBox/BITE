---
title: "DiffMesh: A Motion-Aware Diffusion Framework for Human Mesh Recovery from Videos"
type: paper
paper_level: A
venue: WACV
year: 2025
pdf_ref: paperPDFs/WACV_2025/DiffMesh_A_Motion_Aware_Diffusion_Framework_for_Human_Mesh_Recovery_from_Videos.pdf
project_link: https://zczcwh.github.io/
code_link: null
aliases:
- DiffMesh
tags:
- WACV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将帧间的人体运动模式视为扩散前向过程中的“噪声”，并在反向过程中逐步解码前一帧的特征。
primary_logic: 视频序列中相邻帧之间的前向运动类似于扩散模型中的噪声加入过程；利用这一类比，将运动建模为扩散步骤，可在保持总去噪步数为N的前提下，高效生成平滑准确的网格序列。
claims:
- DiffMesh通过将运动模式视为扩散噪声，实现了在N步内解码运动模式，而Baseline 1需要f×N步。
- 在3DPW数据集上，DiffMesh的MPJPE达到77.2 mm（ResNet50骨干），显著优于之前的视频方法GLoT（80.7 mm）。
- DiffMesh的加速度误差（ACC-ERR）相比DND降低12.8%，且仅需16帧输入（DND需32帧），表明运动平滑性显著提升。
- 通过双流Transformer架构预测运动特征和前一帧条件特征，增强了运动解码能力。
---

# DiffMesh: A Motion-Aware Diffusion Framework for Human Mesh Recovery from Videos

> [!tip] 核心洞察
> 视频序列中相邻帧之间的前向运动类似于扩散模型中的噪声加入过程；利用这一类比，将运动建模为扩散步骤，可在保持总去噪步数为N的前提下，高效生成平滑准确的网格序列。

| 字段 | 内容 |
|------|------|
| 中文题名 | DiffMesh：面向视频人体网格恢复的运动感知扩散框架 |
| 英文题名 | DiffMesh: A Motion-Aware Diffusion Framework for Human Mesh Recovery from Videos |
| 会议/期刊 | WACV 2025 |
| Links | [Project](https://zczcwh.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | DiffMesh |
| Dataset | Human3.6M, 3DPW |

> [!tip] 效果简介
> - Human3.6M 上，MPJPE (mm) 52.5 (DiffMesh, DSTformer) vs 53.8 (MotionBERT, DSTformer) (-1.3)。
> - 3DPW 上，MPJPE (mm) 77.2 (DiffMesh, ResNet50) vs 80.7 (GLoT, ResNet50) (-3.5)。
> - 3DPW (w/o 3DPW training) 上，MPJPE (mm) 88.7 (DiffMesh, ResNet50) vs 89.9 (GLoT, ResNet50) (-1.2)。

## 概要

从视频中恢复精确且时序平滑的三维人体网格是计算机视觉中的基础任务。现有基于扩散模型的方法面临一个关键瓶颈：逐帧独立扩散（Baseline 1）将总去噪步数放大为 $f \times N$，计算开销高昂且完全忽略帧间运动；而将多帧特征简单拼接后统一扩散（Baseline 2）虽将步数降至 $N$，却未能有效建模人体运动模式，导致预测结果在时间维度上不够平滑。

DiffMesh 的核心洞察在于：视频序列中相邻帧之间的前向运动，与扩散模型中逐步注入噪声的前向过程具有天然的类比关系。基于这一发现，该方法将帧间运动模式直接视为扩散前向过程中的“噪声”，并在反向过程中逐步解码前一帧的网格特征。这一设计使得 DiffMesh 在总去噪步数保持为 $N$ 的前提下，高效生成准确且平滑的网格序列，从根本上解决了计算开销与运动建模之间的矛盾。

在方法谱系上，DiffMesh 定位于视频级扩散式人体网格恢复，区别于逐帧图像扩散方法（如 DnD, ECCV 2022）和基于回归的视频方法（如 VIBE, CVPR 2020；TCMR, CVPR 2021；GLoT, CVPR 2023）。其主要结果如下：在 3DPW 数据集上，DiffMesh（ResNet50 骨干）的 MPJPE 达到 77.2 mm，优于 GLoT 的 80.7 mm；加速度误差（ACC-ERR）为 6.3 mm/s²，相比 TCMR 的 6.8 mm/s² 进一步降低，且仅需 16 帧输入即可实现比 DND（32 帧）更优的运动平滑性。在 Human3.6M 上，DiffMesh 同样取得了有竞争力的性能（MPJPE 52.5 mm）。这些结果表明，运动感知扩散框架在精度与效率之间取得了良好的平衡。



### 问题背景：视频人体网格恢复

从单目视频中恢复精确且时间一致的三维人体网格（Video-based Human Mesh Recovery, HMR）是计算机视觉中的核心挑战。该任务要求从连续帧序列中同时估计人体姿态和体型参数，其输出不仅需要在空间维度上保持关节位置的准确性，更需要在时间维度上维持运动轨迹的平滑性。早期方法如 **VIBE**（Kocabas et al., CVPR 2020）和 **TCMR**（Choi et al., CVPR 2021）通过引入时序建模模块（如GRU或自注意力）来捕捉帧间依赖，在一定程度上缓解了逐帧预测导致的时间抖动问题。然而，这些方法本质上仍属于确定性回归范式，难以对复杂运动中的多模态分布进行有效建模。

### 扩散模型在人体姿态估计中的引入与局限

近年来，扩散模型因其强大的生成能力和对复杂分布的表征优势，在二维/三维人体姿态估计领域展现出显著潜力。其基本流程如图2(a)所示：在前向过程中逐步向数据加入噪声直至达到初始分布，在反向过程中从噪声中逐步解码出目标数据。

然而，将扩散模型应用于视频HMR时面临一个关键瓶颈：现有方法要么**逐帧独立应用扩散**（本文构建的Baseline 1），要么**将多帧特征简单拼接后统一扩散**（Baseline 2）。前者的总去噪步数达到 $f \times N$（$f$ 为帧数，$N$ 为单帧扩散步数），计算开销随序列长度线性增长，且去噪过程中完全忽略帧间运动关系，导致预测的运动轨迹不平滑；后者虽将总步数压缩至 $N$，但简单的特征拼接并未真正建模人体运动模式，时间一致性同样无法保证。

### 核心洞察：运动模式与扩散噪声的类比

本文提出一个关键观察：视频序列中相邻帧之间的前向运动，与扩散模型前向过程中逐步加入噪声的机制存在本质相似性。如图2(b)所示，人体网格从第 $i$ 帧到第 $i+1$ 帧的变化由帧间运动模式 $m_i$ 驱动，这一过程可类比为扩散模型中将当前数据 $x_i$ 通过噪声扰动得到 $x_{i+1}$ 的步骤。

基于这一类比，DiffMesh提出将**帧间运动模式视为扩散前向过程中的固有“噪声”**，并在反向过程中逐步解码前一帧的特征。该设计的核心优势在于：总扩散步数保持为 $N$，但前 $f-1$ 步专门用于建模帧间运动，后续 $N-f+1$ 步达到初始分布。相比Baseline 1的 $f \times N$ 步策略，DiffMesh在计算效率上获得显著提升；相比Baseline 2的简单拼接策略，DiffMesh通过将运动建模嵌入扩散过程本身，实现了对时序依赖的深层刻画。

### 方法动机总结

DiffMesh的设计动机可归纳为三个层次：

1. **效率瓶颈突破**：避免逐帧扩散带来的 $f \times N$ 步计算开销，将总步数压缩至 $N$；
2. **运动建模内化**：不再将运动作为扩散过程的外部约束，而是将其作为扩散步骤的内在组成部分，使去噪过程天然具备运动感知能力；
3. **平滑性保障**：通过在反向过程中递归解码前一帧特征，确保生成的网格序列在时间维度上保持连贯一致的平滑运动轨迹。



## 核心方法与创新机理

DiffMesh 的核心创新在于**重新定义了扩散模型在视频人体网格恢复（HMR）中的噪声语义**：将帧间的**人体运动模式**视为扩散前向过程中的“噪声”，从而将时序建模天然地嵌入到扩散框架内部。这一设计带来了三个关键的 changed slots：

### 1. 扩散前向过程的噪声语义：从高斯噪声到运动模式

传统扩散模型（如 Baseline 1 和 Baseline 2）在前向过程中逐步向数据添加标准高斯噪声。DiffMesh 则做出了根本性的语义转换——将相邻帧之间的**前向运动模式** $m_i$ 视为扩散过程中的“特定噪声”（Section 3.3）。其前向步骤定义为：

$$x_{i+1} = \sqrt{\beta_i} \cdot x_i + \sqrt{(1 - \beta_i)} \cdot m_i$$

其中 $x_i$ 为第 $i$ 帧的网格特征，$m_i$ 为从帧 $i$ 到帧 $i+1$ 的运动模式。这一公式的因果逻辑是：**下一帧的网格特征可以表示为当前帧特征与帧间运动的扩散组合**，从而使得扩散过程本身即承载了人体运动的时序信息。这与 Baseline 1（逐帧独立加噪，运动信息完全丢失）和 Baseline 2（拼接多帧特征后统一加噪，运动模式仅通过简单拼接隐式存在）形成了本质区别。

### 2. 扩散步数与帧数的解耦：在 $N$ 步内完成运动解码

这一 changed slot 直接解决了视频扩散方法的效率瓶颈：

- **Baseline 1**（逐帧扩散）：对 $f$ 帧输入，每帧执行完整的 $N$ 步去噪，总步数为 $f \times N$，计算开销随帧数线性增长，且各帧独立去噪导致时间不一致。
- **Baseline 2**（特征拼接扩散）：将 $f$ 帧的网格特征拼接为统一特征，总步数降至 $N$，但简单拼接无法有效建模帧间运动模式。
- **DiffMesh**：通过将前 $f-1$ 步用于建模帧间运动（从 $x_1$ 逐步扩散至 $x_f$），后续 $N-f+1$ 步继续扩散至初始分布 $x_{end}$，**总步数保持为 $N$**（Section 3.3, Fig. 5）。在反向过程中，扩散网络依次解码运动模式，从 $x_f'$ 逐步恢复 $x_{f-1}', \dots, x_1'$。

这一设计的决定性证据在于：DiffMesh 在仅需 $N$ 步的条件下，同时实现了运动平滑性（ACC-ERR 相比 DND 降低 12.8%）和计算效率（仅需 16 帧输入，而 DND 需 32 帧，Section 4.4）。

### 3. 网络架构：双流 Transformer 扩散网络

为配合运动感知扩散机制，DiffMesh 引入了**双流 Transformer 架构**（Fig. 6）来执行反向去噪过程。给定当前帧的网格特征 $x_i'$ 和对应的条件特征 $c_i$，该网络同时预测两个输出：

- **预测的运动模式** $m_{i-1}$：用于计算前一帧的网格特征 $x_{i-1}'$
- **预测的前一帧条件特征** $\hat{c}_{i-1}$：为下一轮去噪提供条件输入

网络内部通过自注意力捕获网格特征和条件特征各自的依赖关系，再通过交叉注意力实现两者的融合（Fig. 6b, 6c）。这一设计与 Baseline 1/2 中使用的朴素 UNet 或原始 Transformer 相比，增强了对运动模式的条件化解码能力。

### 创新点的因果链总结

上述三个 changed slots 构成了一个紧密耦合的因果链：**运动即噪声的语义转换**（Slot 1）使得扩散过程天然承载时序信息，从而实现了**步数与帧数的解耦**（Slot 2），而**双流 Transformer**（Slot 3）则为这一新型扩散过程提供了适配的逆向解码网络。三者共同支撑了 DiffMesh 在保持 $N$ 步去噪的前提下，高效生成平滑且准确的网格序列这一核心优势。



DiffMesh 的整体架构围绕一个核心类比构建：**视频中相邻帧之间的前向运动，在机制上类似于扩散模型前向过程中逐步加入噪声**。基于这一洞见，框架将帧间的人体运动模式视为扩散前向过程中的“噪声”，从而在保持总去噪步数为 $N$ 的前提下，高效生成平滑且准确的人体网格序列。

### 输入输出流

框架接收一段包含 $f$ 帧的视频序列作为输入，目标是输出对应 $f$ 帧的人体网格序列。整个处理流程可概括为以下阶段：

1. **条件特征提取**：从输入视频帧中提取每帧的条件特征 $c_i$，为后续的扩散过程提供视觉引导。
2. **网格特征变换**：将人体网格参数映射到潜在空间中的网格特征 $x_i$，使扩散模型能够在紧凑且语义一致的表示空间中操作。
3. **运动感知前向扩散**：按照帧间运动模式 $m_i$，将第一帧的网格特征逐步扩散至最后一帧，再额外经过 $N - f + 1$ 步扩散至初始分布 $x_{end}$。这一设计使得前 $f-1$ 步自然地建模了帧间运动，而后续步数则保证了与标准扩散框架的兼容性。
4. **双流 Transformer 反向解码**：在反向过程中，扩散网络以当前帧的网格特征 $x_i'$ 和条件特征 $c_i$ 为输入，逐步预测前一帧的运动模式 $m_{i-1}$ 和前一帧的条件特征 $\hat{c}_{i-1}$，进而解码出前一帧的网格特征 $x_{i-1}'$。
5. **网格头输出**：通过 MLP 和 SMPL 人体模型，将解码后的网格特征序列转换为最终的人体网格序列。

### 模块间关系

上述模块之间的数据依赖关系由扩散模型的前向-反向机制串联。前向过程定义了从 $x_1$ 到 $x_f$ 再到 $x_{end}$ 的扩散路径，其中每一帧的网格特征由前一帧的特征和帧间运动模式共同决定：

$$x_{i+1} = \sqrt{\beta_i} \cdot x_i + \sqrt{(1 - \beta_i)} \cdot m_i$$

反向过程则沿着相反的路径逐步解码。双流 Transformer 扩散网络是反向解码的核心计算单元，其内部采用自注意力捕获网格特征和条件特征内部的依赖关系，并通过交叉注意力融合两类特征，最终同时输出预测的运动 $m_{i-1}$ 和预测的前一帧条件特征 $\hat{c}_{i-1}$。网格头作为最终的输出映射模块，将潜在空间中的网格特征解码为具有明确人体模型参数的三维网格。

### 与朴素扩散基线的关键区别

DiffMesh 的整体框架与两类朴素扩散基线形成鲜明对比：

- **Baseline 1（逐帧扩散）**：对每一帧独立应用扩散模型，总步数为 $f \times N$，计算开销大且忽略帧间运动，导致时间不一致的非平滑预测。
- **Baseline 2（特征拼接扩散）**：将多帧的网格特征拼接为统一特征进行扩散，总步数降至 $N$，但简单的拼接策略未能有效建模人体运动模式。

DiffMesh 通过将运动模式内嵌于扩散过程本身，在仅需 $N$ 步的条件下实现了对帧间运动的显式建模，从而在效率和平滑性之间取得了平衡。

### 补充图表

![[assets/figures/papers/paper_list_l1652_DiffMesh_A_Motion_Aware_Diffusion_Framework_for_Human_Mesh_Recovery_from/figures/006_Figure_5.jpg]]
*Figure 5: The architecture of DiffMesh: Our framework takes input sequence with f frames, with the objective of outputting a human mesh sequence consisting of f frames. We model the forward human motion across frames similar to the mechanism of introducing noise in the forward process. We assume that the human motion sequence will eventually reach the initial distribution within total N steps. (additional*

![[assets/figures/papers/paper_list_l1652_DiffMesh_A_Motion_Aware_Diffusion_Framework_for_Human_Mesh_Recovery_from/figures/001_Figure_1.jpg]]
*Figure 1: Different approaches of applying diffusion model for video-based HMR, the input frame f is 3 for simplicity and the number of steps is N. Here xi and ci denote the mesh and conditional features of*



### 3.1 扩散模型基础（Preliminary）

DiffMesh 建立在去噪扩散概率模型（DDPM）之上。标准扩散模型包含两个马尔可夫链：前向扩散过程与反向去噪过程。

**前向过程**逐步向数据 $x_0$ 添加高斯噪声，第 $t$ 步的转移概率为：

$$p(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1 - \beta_t} \cdot x_{t-1}, \beta_t \cdot \mathbf{I}), \quad \forall t \in \{1, \ldots, T\}$$

其中 $\beta_t$ 为预定义的方差调度参数。通过重参数化技巧，可从初始数据 $x_0$ 直接采样任意步 $t$ 的状态：

$$p(x_t | x_0) = \mathcal{N}(x_t; \sqrt{\hat{\beta}_t} \cdot x_0, (1 - \hat{\beta}_t) \cdot \mathbf{I})$$

其中 $\hat{\beta}_t = \prod_{s=1}^{t} \beta_s$ 为累积方差。

**反向过程**旨在从纯噪声 $x_T \sim \mathcal{N}(0, \mathbf{I})$ 逐步去噪恢复原始数据，其参数化高斯转移为：

$$p_\theta(x_{t-1} | x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t))$$

单步去噪采样公式为：

$$x_{t-1} = \frac{1}{\sqrt{\beta_t}} \left( x_t - \frac{1 - \beta_t}{\sqrt{1 - \hat{\beta}_t}} \epsilon_\theta(x_t, t) \right) + \sigma_t z$$

其中 $\epsilon_\theta$ 为噪声预测网络，$\sigma_t$ 为噪声标准差，$z \sim \mathcal{N}(0, \mathbf{I})$。

### 3.2 网格特征变换

DiffMesh 将人体网格参数映射到潜在空间中的**网格特征** $x_i$ 进行操作（见 Figure 3）。这一变换使得扩散模型能够在紧凑的潜在表示上建模帧间运动关系，而非直接在原始网格参数空间上操作。

![[assets/figures/papers/paper_list_l1652_DiffMesh_A_Motion_Aware_Diffusion_Framework_for_Human_Mesh_Recovery_from/figures/005_Figure_3.jpg]]
*Figure 3: Transformation between human mesh and corresponding mesh feature in the latent space*

### 3.3 运动感知前向扩散（核心创新）

DiffMesh 的核心洞察在于：视频序列中相邻帧之间的前向运动模式，与扩散模型中逐步添加噪声的机制具有天然的类比性（见 Figure 2）。

![[assets/figures/papers/paper_list_l1652_DiffMesh_A_Motion_Aware_Diffusion_Framework_for_Human_Mesh_Recovery_from/figures/002_Figure_2.jpg]]
*Figure 2: (a) The general pipeline for diffusion model. Input data is perturbed by adding noise recursively and output data is generated from the noise in the reverse process. Images are taken from [52]. (b) Human motion is involved over time in the input video sequence. Similar to the forward process in (a), the forward motion between adjacent frames resembles the process of adding noise. The mesh of the previous frame can be decoded through the reverse motion process successively*

**关键假设**：人体运动对相邻帧的网格特征（在潜在空间中）产生持续影响，这种运动模式可被概念化为一种施加于网格特征的“特定噪声”。

基于此，DiffMesh 将帧间运动模式 $m_i$ 视为前向扩散过程中的“噪声”，定义运动感知前向扩散步骤为：

$$x_{i+1} = \sqrt{\beta_i} \cdot x_i + \sqrt{1 - \beta_i} \cdot m_i \tag{Eq. 6}$$

其中：
- $x_i$：第 $i$ 帧的网格特征
- $x_{i+1}$：第 $i+1$ 帧的网格特征
- $m_i$：第 $i$ 帧到第 $i+1$ 帧的运动模式
- $\beta_i$：方差调度参数，控制当前帧特征与运动模式的混合比例

**扩散步数与帧数的关系**：对于包含 $f$ 帧的输入序列，DiffMesh 通过前 $f-1$ 步建模帧间运动（从 $x_1$ 逐步扩散至 $x_f$），再经过额外的 $N - f + 1$ 步将 $x_f$ 进一步扩散至初始分布 $x_{end}$。总扩散步数保持为 $N$，而无需像 Baseline 1 那样进行 $f \times N$ 步扩散。

### 3.4 运动感知反向去噪

在反向过程中，DiffMesh 从 $x_{end}$ 开始逐步解码，恢复各帧的网格特征。反向步骤的核心公式为：

$$x_{i-1}' = \frac{1}{\sqrt{\beta_i}} \left( x_i' - \frac{1 - \beta_i}{\sqrt{1 - \hat{\beta}_i}} \cdot \epsilon \right) + \sigma_t \tag{Eq. 7}$$

其中：
- $x_i'$：当前反向步的网格特征
- $x_{i-1}'$：解码得到的前一帧网格特征
- $\epsilon$：扩散网络预测的噪声分量（本质为运动模式 $m_{i-1}$ 的估计）
- $\hat{\beta}_i$：累积方差参数
- $\sigma_t$：噪声标准差

这一反向过程实现了“从当前帧特征 + 预测运动模式 → 前一帧特征”的逐步解码，使得运动模式在去噪过程中被显式恢复。

### 3.5 双流 Transformer 扩散网络

为实现运动感知的反向去噪，DiffMesh 设计了**双流 Transformer 架构**（见 Figure 6）：

![[assets/figures/papers/paper_list_l1652_DiffMesh_A_Motion_Aware_Diffusion_Framework_for_Human_Mesh_Recovery_from/figures/007_Figure_6.jpg]]
*Figure 6: Consequently, we utilize a transformer-based diffusion model to sequentially produce the decoded features during the reverse process. The final human mesh sequence is returned by a mesh head using SMPL [29] human body model. The structure of DN (diffusion network) is illustrated in Fig. 6*

- **输入**：当前步的网格特征 $x_i'$ 和对应的条件特征 $c_i$（从输入视频帧提取）
- **输出**：预测的运动模式 $m_{i-1}$ 和预测的前一帧条件特征 $\hat{c}_{i-1}$
- **结构**：
  - 自注意力块（Self-Attention Block）：捕获网格特征内部的依赖关系以及条件特征的上下文
  - 交叉注意力块（Cross-Attention Block）：实现网格特征与条件特征之间的信息融合
  - 符号 $\oplus$ 表示逐元素加法

该双流设计使得网络能够同时预测帧间运动模式和前一帧的条件信息，从而在反向过程中逐步解码出平滑的网格特征序列。

### 3.6 整体流程

完整的 DiffMesh 流程（见 Figure 5）可概括为：

1. **条件特征提取**：从 $f$ 帧输入视频中提取条件特征 $c_i$
2. **运动感知前向扩散**：按 Eq. 6 将 $x_1$ 经 $f-1$ 步扩散至 $x_f$，再经 $N-f+1$ 步扩散至 $x_{end}$
3. **双流 Transformer 反向去噪**：按 Eq. 7 从 $x_{end}$ 开始，逐步预测 $m_{i-1}$ 和 $\hat{c}_{i-1}$，解码出 $x_{i-1}'$
4. **网格头解码**：通过 MLP 和 SMPL 人体模型将网格特征 $x_i'$ 解码为最终的人体网格序列

### 补充图表

![[assets/figures/papers/paper_list_l1652_DiffMesh_A_Motion_Aware_Diffusion_Framework_for_Human_Mesh_Recovery_from/figures/004_Figure_4.jpg]]
*Figure 4: Two diffusion baselines for video-based HMR*



## 实验与关键发现

### 主实验结果

DiffMesh 在两个核心基准上均展现出优于现有视频方法的性能。在 **Human3.6M** 数据集上，采用 DSTformer 骨干网时，DiffMesh 的 MPJPE 达到 **52.5 mm**，相比 MotionBERT（Zhu et al., ICCV 2023）的 53.8 mm 降低了 1.3 mm（Table 2）。在 **3DPW** 数据集上，采用 ResNet50 骨干网时，DiffMesh 的 MPJPE 达到 **77.2 mm**，显著优于 GLoT（Shen et al., CVPR 2023）的 80.7 mm，降幅达 3.5 mm（Table 2）。即使在不使用 3DPW 训练集的跨域泛化设定下，DiffMesh 仍以 **88.7 mm** 的 MPJPE 优于 GLoT 的 89.9 mm（Table 3），验证了方法的泛化能力。

![[assets/figures/papers/paper_list_l1652_DiffMesh_A_Motion_Aware_Diffusion_Framework_for_Human_Mesh_Recovery_from/figures/008_Table_2.jpg]]
*Table 2: Performance comparison with SOTA video-based methods on Human3.6M and 3DPW datasets. The symbol “†” denotes the HybrIK [24] is applied for the refinement. 3DPW Training set is used during training*

![[assets/figures/papers/paper_list_l1652_DiffMesh_A_Motion_Aware_Diffusion_Framework_for_Human_Mesh_Recovery_from/figures/009_Table_3.jpg]]
*Table 3: Performance comparison with SOTA video-based methods on 3DPW without using 3DPW training set during training*

运动平滑性方面，DiffMesh 在 3DPW 上的加速度误差（ACC-ERR）为 **6.3 mm/s²**，优于 TCMR（Choi et al., CVPR 2021）的 6.8 mm/s²（Table 2）。与基于扩散的视频方法 DND（Li et al., ECCV 2022）相比，DiffMesh 仅需 **16 帧**输入（DND 需 32 帧），却实现了 ACC-ERR 降低 **12.8%** 的提升（Section 4.4），表明运动感知扩散机制能以更少帧数生成更平滑的网格序列。

### 消融实验

**运动感知扩散的有效性**：与两个朴素扩散基线对比，DiffMesh 在加速度误差上具有显著优势。Baseline 1（逐帧扩散）和 Baseline 2（特征拼接扩散）的 ACC-ERR 均高于 DiffMesh（Figure 7），验证了将帧间运动建模为扩散噪声这一设计的必要性。具体而言，在“courtyard basketball 01”序列上，DiffMesh 的 ACC-ERR 远低于 TCMR 和两个基线，展现出更强的时间一致性（Figure 7）。

**与逐帧图像方法的对比**：在 3DPW 上，DiffMesh 的 ACC-ERR 为 **6.5 mm/s²**，相比逐帧图像方法 I2L-MeshNet 的 30 mm/s² 大幅降低（Table 4），证明视频级运动建模对时间一致性的关键作用。

**推理效率**：在相同硬件平台（单卡 NVIDIA A5000，批量大小为 1）下，DiffMesh 在保持竞争力的推理时间的同时，实现了更优的重建精度（Table 4）。这得益于其将总去噪步数保持为 N（30 步），而非 Baseline 1 的 f×N 步。

### 失败模式与局限性

1. **严重遮挡场景**：DiffMesh 在严重遮挡情况下可能产生不真实的网格输出（论文自述局限性）。这是因为条件特征提取依赖于输入帧的可见信息，当人体关键部位被大面积遮挡时，双流 Transformer 预测的运动模式和条件特征可能缺乏足够的视觉证据。
2. **未见运动模式的泛化**：模型对训练集中未出现的运动模式的泛化能力有待进一步验证（论文自述开放问题）。运动感知扩散机制将帧间运动视为特定噪声模式，当测试序列的运动分布与训练集差异较大时，预测的运动特征可能偏离真实分布。

### 关键图表结论

- **Table 2**：DiffMesh 在 Human3.6M 和 3DPW 上全面超越现有视频 HMR 方法，尤其在 ResNet50 骨干网下以 77.2 mm MPJPE 刷新 3DPW 最优结果。
- **Table 4**：DiffMesh 在 ACC-ERR 指标上相比 DND 降低 12.8%，且仅需 16 帧输入，验证了运动感知扩散在效率和平滑性上的双重优势。
- **Figure 7**：在特定序列的加速度误差对比中，DiffMesh 的曲线波动幅度显著小于 TCMR 和两个基线，直观展示了运动平滑性的提升。
- **Figure 8**：在真实场景可视化中，DiffMesh 相比 GLoT 在四肢末端等关键区域（图中圆圈标注）具有更高的重建精度。

![[assets/figures/papers/paper_list_l1652_DiffMesh_A_Motion_Aware_Diffusion_Framework_for_Human_Mesh_Recovery_from/figures/010_Table_4.jpg]]
*Table 4: Reconstruction performance and inference time comparison on 3DPW dataset between our DiffMesh and previous videobased HMR methods with the same hardware platform. A single NVIDIA A5000 GPU is used with a batch size of 1 (the input of [1, num of frames, 224, 224, 3]) for fair comparison*

![[assets/figures/papers/paper_list_l1652_DiffMesh_A_Motion_Aware_Diffusion_Framework_for_Human_Mesh_Recovery_from/figures/012_Figure_7.jpg]]
*Figure 7: Acceleration error comparison of the ‘courtyard basketball 01’ sequence for TCMR [5], two baselines, and our DiffMesh*

![[assets/figures/papers/paper_list_l1652_DiffMesh_A_Motion_Aware_Diffusion_Framework_for_Human_Mesh_Recovery_from/figures/011_Figure_8.jpg]]
*Figure 8: The in-the-wild visual comparison between recent GLoT [41] with our DiffMesh. The circles highlight locations where DiffMesh is more accurate than GLoT. More examples are provided in the supplementary Sec. 4 and in demo videos*

### 补充图表

![[assets/figures/papers/paper_list_l1652_DiffMesh_A_Motion_Aware_Diffusion_Framework_for_Human_Mesh_Recovery_from/figures/003_Table_1.jpg]]
*Table 1: Comparison with previous diffusion-based human pose and mesh methods*



## 定位与知识库关联

### 1. 与现有视频HMR方法的定位关系

DiffMesh 位于视频人体网格恢复（Video-based HMR）与扩散生成模型的交叉地带。其核心贡献在于将帧间运动模式显式地建模为扩散前向过程中的“噪声”，从而在保持总去噪步数为 N 的前提下，实现时序一致的网格序列生成。这一设计使其与两类现有方法形成明确对比：

- **传统视频HMR方法**：如 **VIBE** (Kocabas et al., CVPR 2020)、**TCMR** (Choi et al., CVPR 2021)、**MPS-Net** (Wei et al., CVPR 2022)、**GLoT** (Shen et al., CVPR 2023) 和 **MotionBERT** (Zhu et al., ICCV 2023)，这些方法通过循环网络、注意力机制或预训练模型来建模时序依赖，但未将运动建模纳入扩散框架。DiffMesh 在 3DPW 数据集上以 ResNet50 骨干网达到 77.2 mm 的 MPJPE，显著优于 GLoT 的 80.7 mm，验证了运动感知扩散建模的增益。

- **扩散式人体姿态/网格方法**：DiffMesh 与现有扩散式方法（如 **DND**, Li et al., ECCV 2022）的关键区别在于运动建模方式。DND 需要 32 帧输入，而 DiffMesh 仅需 16 帧即可实现 12.8% 的加速度误差（ACC-ERR）降低，表明运动感知扩散设计在更少输入帧下仍能保证运动平滑性。

### 2. 与朴素扩散基线的对比

论文构建了两个朴素扩散基线，以隔离运动感知建模的贡献：

- **Baseline 1（逐帧扩散）**：对每一帧独立应用扩散模型，总步数为 f × N。该策略计算开销大，且去噪过程中完全忽略帧间运动，导致非平滑预测。
- **Baseline 2（特征拼接扩散）**：将多帧网格特征拼接为统一特征进行扩散，总步数降至 N，但简单的拼接操作无法有效捕获运动模式。

DiffMesh 通过将运动模式视为扩散噪声，在保持 N 步的前提下，利用前 f-1 步建模帧间运动，后续 N-f+1 步达到初始分布。Figure 7 的加速度误差对比显示，DiffMesh 的运动平滑性显著优于两个基线，验证了运动建模的必要性。

### 3. 方法谱系中的关键设计差异

| 设计维度 | Baseline 1 | Baseline 2 | DiffMesh |
|---------|-----------|-----------|----------|
| 扩散前向噪声类型 | 标准高斯噪声 | 标准高斯噪声 | 帧间运动模式 m_i |
| 总去噪步数 | f × N | N | N |
| 网络架构 | UNet/原始Transformer | UNet/原始Transformer | 双流Transformer |
| 运动建模 | 忽略 | 隐式（拼接） | 显式（前向/反向过程） |

双流Transformer架构（Figure 6）是DiffMesh的另一关键设计：通过自注意力捕获网格特征和条件特征的内部依赖，交叉注意力实现两者融合，从而在反向过程中同时预测运动模式 m_{i-1} 和前一帧条件特征 ĉ_{i-1}。

### 4. 适用边界与局限

- **输入帧数**：当前设计固定输入帧数 f=16，总步数 N=30。对于更长序列或可变帧数的场景，需要额外的序列分段或动态步数调整策略。
- **遮挡场景**：在严重遮挡下，DiffMesh 可能产生不真实的网格输出。这是因为运动感知扩散依赖连续帧间的运动模式推断，遮挡会破坏运动模式的连续性。
- **泛化能力**：模型对未见过的运动模式（如极端运动、罕见动作）的泛化能力有待进一步验证。当前实验主要在 Human3.6M 和 3DPW 等标准数据集上进行。

### 5. 开放问题

1. **长序列与可变帧数**：如何将运动感知扩散框架扩展到任意长度的视频序列？可能的方案包括滑动窗口、层次化扩散或自适应步数调度。
2. **遮挡鲁棒性**：在遮挡情况下，能否引入人体结构先验（如骨骼长度约束、关节角度限制）来约束扩散生成过程，提升网格合理性？
3. **跨任务推广**：运动感知扩散的核心思想——将时序变化建模为扩散噪声——能否推广到其他时序预测任务（如轨迹预测、动作预测）？
4. **计算效率优化**：当前 N=30 步的去噪过程是否可以通过蒸馏或步数缩减技术进一步加速，以适配实时应用场景？



## 原文 PDF

![[paperPDFs/WACV_2025/DiffMesh_A_Motion_Aware_Diffusion_Framework_for_Human_Mesh_Recovery_from_Videos.pdf]]
