---
title: "Latent-Reframe: Enabling Camera Control for Video Diffusion Model without Training"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/Latent_Reframe_Enabling_Camera_Control_for_Video_Diffusion_Model_without_Training.pdf
project_link: null
code_link: null
aliases:
- LR
- Latent-Reframe
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在去噪过程的中途阶段，将部分去噪的潜在代码映射为时间感知3D点云，再根据目标摄像机姿态重新投影生成重帧视频，从而在采样时直接控制视角，无需微调。
primary_logic: 预训练视频扩散模型的中间潜在表示已编码足够的场景三维与外观信息；在此阶段通过时间感知点云进行潜在重帧，可实现对摄像机运动的直接控制，同时保留生成质量。
claims:
- 在定量对比中，Latent-Reframe 在 FID 和 FVD 指标上均优于 CameraCtrl，并且在旋转误差和位移误差上与 MotionCtrl 相当或更优。
- 消融实验证明，时间感知点云相比静态点云能更好地捕捉视频动态变化（如面部运动和波浪），减少伪影。
- 在 25 个去噪步骤中选择步骤 8 进行 Latent-Reframe，既保证点云重建精度，又留有足够的潜在空间修复与调和空间。
- 10 prompts + 80 RealEstate10K poses 上 FID = 60.18
---

# Latent-Reframe: Enabling Camera Control for Video Diffusion Model without Training

> [!tip] 核心洞察
> 预训练视频扩散模型的中间潜在表示已编码足够的场景三维与外观信息；在此阶段通过时间感知点云进行潜在重帧，可实现对摄像机运动的直接控制，同时保留生成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | Latent-Reframe：无需训练即可为视频扩散模型实现摄像机控制 |
| 英文题名 | Latent-Reframe: Enabling Camera Control for Video Diffusion Model without Training |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2412.06029) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Latent-Reframe |
| Dataset | 10 prompts + 80 RealEstate10K poses |

> [!tip] 效果简介
> - 10 prompts + 80 RealEstate10K poses 上，FID 60.18 vs CameraCtrl (数值未直接提供，但论文称本文方法更优)；MotionCtrl 结果相当 (显著低于 CameraCtrl)；FVD 509.11 vs CameraCtrl (更高，即更差)；MotionCtrl 结果相当 (显著低于 CameraCtrl)；TransErr 5.52 vs CameraCtrl (更高)；MotionCtrl 稍高或相当 (最低的平移误差)。

## 概要

**问题瓶颈**：现有的基于微调的摄像机控制方法（如 **MotionCtrl** (Wang et al., SIGGRAPH 2024) 和 **CameraCtrl**）需要额外的配对视频-姿态数据集进行训练，数据采集成本高且训练计算昂贵；更关键的是，微调过程会破坏预训练视频扩散模型的生成分布，导致视频质量下降。

**核心洞察**：预训练视频扩散模型的中间潜在表示已编码足够的场景三维与外观信息。在去噪过程的中途阶段，通过时间感知点云对潜在代码进行重帧（latent reframing），可直接控制摄像机运动，无需任何额外训练，同时保留生成质量。

**方法定位**：**Latent-Reframe** 是一种无需训练的摄像机控制方法，在采样阶段介入预训练扩散模型的去噪过程。其核心操作包括：(1) 从中途去噪的潜在代码中估计干净的像素视频；(2) 利用 MonST3R 提取时间感知的 3D 点云；(3) 根据目标摄像机姿态重投影生成重帧视频；(4) 通过潜在空间修复（inpainting + harmonization）处理遮挡产生的空白区域。

**主要结果**：在 10 个提示词与 80 个 RealEstate10K 姿态的基准测试中，Latent-Reframe 在 FID（60.18）和 FVD（509.11）指标上均显著优于 CameraCtrl，平移误差（5.52）为所有方法中最低，旋转误差（2.29）与 MotionCtrl 接近且优于 CameraCtrl（Table 1）。消融实验证实，时间感知点云相比静态点云能更好地捕捉动态变化（Figure 4），在 25 个去噪步骤中选择第 8 步执行重帧可在点云精度与修复效果之间取得最佳平衡（Figure 5）。

视频扩散模型在文本到视频生成领域已取得显著进展，但生成过程中的摄像机视角仍难以精确控制。用户往往希望生成的视频不仅能忠实于文本描述，还能沿着指定的摄像机轨迹（如平移、旋转或复杂组合运动）展开画面，这在电影预览、虚拟场景漫游等应用中至关重要。

现有摄像机控制方法主要依赖**微调（fine-tuning）**范式。这些方法将摄像机姿态嵌入注入扩散模型的 UNet 去噪网络，通过额外的配对视频-姿态数据集进行训练。代表性工作包括 **MotionCtrl**（Wang et al., SIGGRAPH 2024）和 **CameraCtrl**，它们能够在训练后实现一定程度的视角控制。然而，这一范式存在三个根本性瓶颈：

1. **数据采集成本高**：微调需要大量精确配对的视频与摄像机姿态数据，此类数据集的构建耗时且昂贵，限制了方法在开放场景中的可扩展性。
2. **训练计算昂贵**：对预训练视频扩散模型进行微调需要大量 GPU 资源，且每新增一种控制能力都需重新训练，难以快速适配不同需求。
3. **生成分布破坏**：微调过程不可避免地会改变预训练模型的参数分布，导致生成视频的质量下降、多样性降低，甚至产生视觉伪影——这是训练型方法的内在代价。

上述瓶颈的核心在于：**摄像机控制的实现被绑定在训练阶段**，迫使方法在控制精度与生成质量之间做出妥协。一个自然的问题是：能否绕过微调，直接在预训练模型的推理过程中注入摄像机控制？

Latent-Reframe 正是基于这一动机提出的。其核心洞察是：预训练视频扩散模型在去噪过程的中间阶段，其潜在表示已编码了足够的场景三维结构与外观信息。如果能在此时将部分去噪的潜在代码“重新取景”（reframe），使其对齐目标摄像机姿态，就能在不触碰模型参数的前提下实现视角控制。这一思路将摄像机控制从**训练时注入**转变为**采样时操作**，从根本上规避了数据依赖与分布破坏问题。

## 核心方法与创新机理

Latent-Reframe 的核心创新在于将摄像机控制从**训练时微调**迁移到**采样时潜在空间操作**，彻底消除了对配对视频-姿态数据集和额外训练计算的需求。这一转变通过两个关键的 changed slots 实现：

### 从参数注入到潜在重帧

现有训练型方法（如 **MotionCtrl**（Wang et al., SIGGRAPH 2024）和 **CameraCtrl**）的核心策略是：在训练阶段将摄像机姿态嵌入注入扩散模型的 UNet 参数中，迫使模型学习姿态条件与视频生成之间的映射。然而，这种微调范式存在根本性瓶颈：**需要昂贵的配对视频-姿态数据集，且微调过程会破坏预训练模型的生成分布，导致视频质量下降**。

Latent-Reframe 的核心洞察在于：**预训练视频扩散模型的中间潜在表示已经编码了足够的场景三维与外观信息**。基于此，方法将控制时机从训练阶段转移到采样阶段的中途——在去噪过程进行到约 1/3 时（25 步中的第 8 步），对部分去噪的潜在代码进行“重帧”（reframing），使其对齐目标摄像机轨迹。这一操作完全绕过了微调，直接利用预训练模型的推理能力实现视角控制。

### 时间感知点云：从静态到动态的 3D 桥梁

实现潜在重帧的关键技术是**时间感知 3D 点云**。方法首先利用 DDIM 公式从带噪潜在代码 $z_t$ 中估计干净的 $z_0$，经 VAE 解码恢复像素空间视频 $x_0$；随后通过 MonST3R 模型为每一帧提取点云，并在滑动窗口构建的连通图上进行全局对齐优化（Eq. 3），为每个时间步分配独立的点云表示。

与静态点云（将所有帧的点云合并为单一静态表示）不同，时间感知点云保留了视频的**时序动态信息**。消融实验（Figure 4）表明，这一设计能更好地捕捉人脸运动、波浪等动态细节，避免静态点云因时间信息丢失而产生的伪影。这构成了从“训练时注入姿态条件”到“采样时通过 3D 重投影控制视角”这一范式转变的因果纽带。

### 潜在空间修复：弥合重帧带来的遮挡缺口

重帧操作不可避免地会因视角变化产生遮挡区域（空白像素）。为此，方法引入了**潜在空间修复**机制：通过遮罩 $m$ 区分已知区域和未知区域，对已知区域施加较轻噪声（噪声水平降低 3 步），对未知区域通过 DDIM 反向去噪生成内容，再将两者混合（Eq. 4）。这一设计使得预训练扩散模型自身成为“修复器”，在保留已知区域结构的同时和谐地填补空白，无需额外的修复网络。消融实验（Figure 6）证实，降低 3 步噪声能在模糊与条带伪影之间取得最佳平衡。

综上，Latent-Reframe 的创新本质在于：**将摄像机控制从“学习条件映射”重新定义为“潜在空间中的 3D 几何操作 + 修复”**，从而在无需训练的前提下，实现了与训练型方法相当甚至更优的控制精度与生成质量。

Latent-Reframe 的整体 pipeline 围绕一个核心思想展开：**在预训练视频扩散模型的去噪过程中途，对部分去噪的潜在表示进行“重帧”（reframing），从而实现无需训练的摄像机控制**。整个框架由四个串行模块构成，形成一条从潜在代码到视角可控视频的完整推理链路。

### 输入与输出

- **输入**：一个文本提示（text prompt）和一条目标摄像机姿态轨迹（camera pose trajectory）。
- **输出**：一段既遵循文本语义、又精确跟随指定摄像机运动的高质量视频。

### 模块关系与数据流

四个模块在去噪时间线上的协作关系如下（对应 **Figure 2** 的方法总览图）：

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2412_06029/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed Latent-Reframe. In the middle of the denoising process of a pre-trained video diffusion model, we first extract time-aware 3D point cloud via a point cloud estimation model, which takes*

1. **近似干净视频估计（Approximate clean video estimation）**
   在预训练视频扩散模型的去噪过程中，选定一个中途步骤 $t$（默认 25 步中的第 8 步）。利用 DDIM 公式从当前带噪潜在代码 $z_t$ 反向估计出近似干净的潜在代码 $z_0$，再通过 VAE 解码器将其还原为像素空间视频 $x_0$。这一步为后续的三维重建提供了可用的视觉信号。

2. **时间感知点云提取（Time-aware point cloud extraction with MonST3R）**
   将像素视频序列 $x_0$ 送入 MonST3R 模型，通过滑动窗口构建帧间连通图，并在全局对齐优化目标下，为每一帧提取统一坐标系下的时间感知 3D 点云。与静态点云不同，时间感知点云为每帧分配独立的时间尺度，能够捕捉视频中的动态变化（如面部运动、波浪）。

   **全局对齐优化目标**为：
   $$P^{*} = \underset{P, \tau, s}{\arg\min} \sum_{e \in \mathcal{E}} \sum_{v \in e} \sum_{i=1}^{HW} C_{i}^{v,e} \left\| P_{i}^{v} - s_{e} \tau_{e} Q_{i}^{v,e} \right\|$$

3. **基于 3D 重投影的潜在重帧（Latent reframing via 3D reprojection）**
   根据目标摄像机姿态，对每一帧的时间感知点云进行刚体变换，再将变换后的点云重新投影为二维视频帧。这一过程直接实现了视角变换，将原始视频的摄像机运动替换为目标轨迹。

4. **潜在空间修复与和谐化（Latent rehabilitation: inpainting + harmonization）**
   重帧后因遮挡会产生空白区域。该模块首先生成一个遮罩 $m$ 标记未知区域，然后在潜在空间执行修复：已知区域通过正向扩散施加较轻噪声（默认降低 3 个噪声步骤），未知区域通过 DDIM 反向去噪生成内容，最后将两者混合。更新规则为：
   $$\begin{array}{rl} z_{t-1}^{\mathrm{known}} &\sim \sqrt{\bar{\alpha}_{t-1}} z_{0}' + \sqrt{1 - \bar{\alpha}_{t-1}} \epsilon, \quad \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I}) \\ z_{t-1}^{\mathrm{unknown}} &\sim \mathrm{DDIM}(z_{t}', t) \\ z_{t-1}' &= m \odot z_{t-1}^{\mathrm{known}} + (1 - m) \odot z_{t-1}^{\mathrm{unknown}} \end{array}$$

   修复完成后，继续执行剩余的 DDIM 去噪步骤，最终生成视角可控的视频 $x_0'$。完整推理流程见 **Algorithm 1**。

### 方法谱系与知识库定位

在摄像机可控视频生成这一问题上，现有方法主要分为两类：

- **训练型方法**：如 **MotionCtrl**（Wang et al., SIGGRAPH 2024）和 **CameraCtrl**，通过微调将摄像机姿态嵌入注入 UNet 去噪网络。这类方法需要额外的配对视频-姿态数据集，采集成本高、训练计算昂贵，且微调会破坏预训练模型的生成分布，降低视频质量。
- **无需训练的方法**：Latent-Reframe 独树一帜，通过在采样阶段对潜在代码进行几何重帧，完全避免了训练开销和分布破坏问题。其核心因果机制在于：预训练视频扩散模型的中间潜在表示已编码足够的场景三维与外观信息，在此阶段通过时间感知点云进行重帧，可直接控制摄像机运动，同时保留生成质量。

在定量对比中（**Table 1**），Latent-Reframe 在 FID（60.18）和 FVD（509.11）上均显著优于 CameraCtrl，在平移误差（TransErr 5.52）上达到最优，旋转误差（RotErr 2.29）与 MotionCtrl 接近，验证了无需训练方案的有效性。

Latent-Reframe 的核心操作发生在预训练视频扩散模型的去噪过程中途，由三个紧密耦合的模块构成：近似干净视频估计、时间感知点云提取与重帧、以及潜在空间修复。以下逐一展开其机理与关键公式。

### 1. 近似干净视频估计

在去噪步骤 $t$，模型当前持有的是带噪潜在码 $z_t$。为了在像素空间进行摄像机重投影，需要先估计出对应的干净视频帧。利用 DDIM 的反向过程公式，可从 $z_t$ 直接推导出近似的 $z_0$：

$$z_{0} \approx \frac{z_t - \sqrt{1 - \bar{\alpha}_t} \,\epsilon_\theta(z_t, t, c)}{\sqrt{\bar{\alpha}_t}}$$

其中 $\bar{\alpha}_t$ 为扩散调度中的累积信号系数，$\epsilon_\theta$ 为预训练去噪网络，$c$ 为文本条件。随后通过 VAE 解码器将 $z_0$ 映射回像素空间，得到 $x_0$。这一估计的精度直接决定了后续点云重建的质量，因此重帧步骤 $t$ 的选择至关重要。

### 2. 时间感知点云提取与重帧

将像素视频序列 $x_0$ 输入点云估计模型 **MonST3R**。MonST3R 通过滑动窗口机制为每对相邻帧输出成对的点云图。为将所有帧的点云统一到同一坐标系，论文构建了一个连通图 $\mathcal{G}(\mathcal{V}, \mathcal{E})$，并在其上求解全局对齐优化问题：

$$P^{*} = \underset{P, \tau, s}{\arg\min} \sum_{e \in \mathcal{E}} \sum_{v \in e} \sum_{i=1}^{HW} C_{i}^{v,e} \left\| P_{i}^{v} - s_{e} \tau_{e} Q_{i}^{v,e} \right\|$$

式中 $Q_{i}^{v,e}$ 为 MonST3R 输出的成对点云坐标，$C_{i}^{v,e}$ 为对应的置信度权重，$s_e$ 与 $\tau_e$ 分别为边 $e$ 上的尺度因子与相对姿态变换，$P_i^v$ 为优化后统一坐标系下的点云坐标。该优化的核心作用在于消除逐帧估计的尺度不一致与姿态漂移，为后续重投影提供几何一致的三维表示。

获得时间感知点云后，根据目标摄像机姿态对每一帧的点云进行刚体变换，再重新投影到二维图像平面，生成视角变换后的视频帧 $x_0'$。由于遮挡关系变化，$x_0'$ 中会出现无有效像素的空白区域，需由后续模块处理。

### 3. 潜在空间修复

重帧后的像素视频 $x_0'$ 经 VAE 编码器重新映射回潜在空间，得到 $z_0'$。为修复遮挡造成的空白区域，论文设计了一种在潜在空间内利用扩散模型自身进行修复的机制。

首先根据点云渲染情况生成二值遮罩 $m$，标记已知区域（有像素）与未知区域（空白）。随后对两类区域分别采样：

- **已知区域**：沿正向扩散路径，从 $z_0'$ 出发添加噪声至与当前时间步匹配的水平，即 $z_{t-1}^{\mathrm{known}} \sim \mathcal{N}(\sqrt{\bar{\alpha}_{t-1}} z_0', (1-\bar{\alpha}_{t-1})\mathbf{I})$。
- **未知区域**：通过 DDIM 反向去噪从 $z_t'$ 生成内容，即 $z_{t-1}^{\mathrm{unknown}} \sim \mathrm{DDIM}(z_t', t)$。

最终将两者按遮罩混合：

$$z_{t-1}' = m \odot z_{t-1}^{\mathrm{known}} + (1 - m) \odot z_{t-1}^{\mathrm{unknown}}$$

这一设计的因果机制在于：已知区域保留了重帧后的几何正确性，仅被施加可控噪声以与未知区域的去噪生成保持和谐；未知区域则完全由扩散模型的生成先验填补，实现内容级修复。消融实验（Figure 6）表明，将已知区域的噪声水平降低 3 个步骤（即使用 $t-3$ 而非 $t$ 对应的噪声系数）能在模糊与条带伪影之间取得最佳平衡。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2412_06029/figures/008_Figure_6.jpg]]
*Figure 6: Comparison between noise reduction steps. Reducing the noise level of the known region by 3 steps results in videos without significant blurriness or strip artifacts, reaching the best balance*

### 4. 模块间的因果链条

上述三个模块形成了一条清晰的因果链条：**去噪中途的 $z_t$ → 近似 $z_0$ → 像素视频 $x_0$ → 时间感知点云 → 目标姿态重投影 → $x_0'$ → 潜在码 $z_0'$ → 遮罩引导的潜在修复 → 继续去噪**。这一链条的核心洞察在于，预训练扩散模型的中途潜在表示已编码了足够的三维场景与外观信息，使得无需微调即可在采样阶段“劫持”去噪过程，实现对摄像机运动的直接控制。

整个流程由 Algorithm 1 以伪代码形式给出，完整描述了从初始噪声到最终视频生成的去噪时间线。关于重帧步骤 $t$ 的选择（25 步中取第 8 步）以及噪声降低步数的消融分析，详见实验部分 Figure 5 与 Figure 6。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2412_06029/figures/005_Figure_5.jpg]]
*Figure 5: Comparison between diffusion steps to apply Latent-Reframe. Using diffusion step 8 out of 25 allows for the reconstruction of high-precision point clouds while leaving enough room for latent space inpainting and harmonization*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2412_06029/figures/006_Figure_4.jpg]]
*Figure 4: Comparison between the time-aware and time-static point clouds. Time-aware point cloud can capture more temporal dynamics of the video, For instance, the motion of the human face (row 1 and 2) and wave (row 3 and 4) are more prominent using time-aware point cloud, both are marked with red bounding boxes*

## 实验与关键发现

### 主实验结果

Latent-Reframe 在 10 个文本提示与 80 条 RealEstate10K 摄像机轨迹构成的测试基准上，与两种训练型方法 **MotionCtrl**（Wang et al., SIGGRAPH 2024）和 **CameraCtrl** 进行了定量对比。评估指标涵盖视频质量（FID、FVD）和摄像机姿态精度（旋转误差 RotErr、平移误差 TransErr），结果汇总于 Table 1。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2412_06029/figures/004_Table_1.jpg]]
*Table 1: Quantitative Comparisons with training-based methods: MotionCtrl [40] and CameraCtrl [11]. Our Method outperforms CameraCtrl on both video quality and camera pose accuracy. Meanwhile, our method achieves comparable or even better results against MotionCtrl on four evaluated metrics, without training. The best and second best results are marked with bold and underline, respectively*

在视频质量方面，Latent-Reframe 的 FID 为 60.18，FVD 为 509.11，两项指标均显著优于 CameraCtrl，表明无需微调即可生成更高质量的帧序列。在摄像机姿态精度上，Latent-Reframe 的平移误差为 5.52，是所有方法中最低的；旋转误差为 2.29，与 MotionCtrl 接近且优于 CameraCtrl。综合来看，Latent-Reframe 在完全不依赖训练的条件下，取得了与训练型方法相当甚至更优的控制精度与生成质量。

为确保公平性，实验中对每种测试姿态手动调整了摄像机运动尺度，使不同方法生成的视频在视觉上具有相似的相机运动幅度；定量评价前对所有估计姿态相对于第一帧进行了归一化，并对平移尺度进行了标准化，以消除尺度差异的影响。

### 消融实验

#### 时间感知点云 vs. 静态点云

时间感知点云是 Latent-Reframe 的核心设计之一。消融实验对比了时间感知点云与将所有帧点云合并为单一静态点云的效果（Figure 4）。结果表明，时间感知点云能更好地捕捉视频中的动态变化——例如人脸运动和水面波浪的细节在时间感知版本中更加突出，而静态点云则容易丢失这些时序动态，导致生成结果出现伪影或细节模糊。

#### 重帧去噪步选择

Latent-Reframe 在去噪过程的中途执行潜在重帧，步数的选择直接影响点云重建精度与后续修复空间。实验在总共 25 个去噪步中测试了不同步数（Figure 5），发现选择第 8 步时达到最佳平衡：此时潜在代码已包含足够的场景结构信息以重建高精度点云，同时仍保留充足的去噪步数供潜在修复与和谐化操作完成内容修补。

#### 噪声降低步数

在潜在修复阶段，对已知区域施加的噪声水平是控制修复质量的关键参数。消融实验对比了将已知区域噪声降低不同步数的效果（Figure 6），结果表明降低 3 步（即使用 $t-3$ 步的噪声水平）能显著减少模糊与条带伪影，在内容一致性与生成细节之间取得最佳平衡。

#### 点云提取模型对比

点云提取模型的选择直接影响重帧的几何精度。实验将 MonST3R 与其他点云重建方法进行了对比（Figure 7），结果显示 MonST3R 在保留视频细节方面表现更优，为后续的潜在重帧和修复提供了更可靠的 3D 基础。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2412_06029/figures/007_Figure_7.jpg]]
*Figure 7: Comparison between point cloud extraction methods. MonST3R exhibits better performance in keeping fine details of the video*

### 失败模式与局限性

尽管 Latent-Reframe 在常规摄像机运动下表现良好，但论文也明确指出了若干失败模式：

- **大范围摄像机运动与极端遮挡**：当目标摄像机运动幅度较大时，重帧产生的未知遮挡区域面积过大，潜在修复可能无法生成视觉一致的填充内容，导致明显的伪影和不连贯。
- **点云估计误差传递**：MonST3R 的点云重建误差以及姿态估计算法的误差会直接传递到最终的控制精度中，降低摄像机控制的可靠性。
- **复杂动态场景鲁棒性不足**：对于极深遮挡或高度动态的场景，当前方法的鲁棒性有限，生成质量可能显著下降。

这些失败案例提示，该方法在遮挡处理与 3D 重建精度方面仍有提升空间，需要人工核验极端场景下的实际表现。

## 定位与知识库关联

### 问题脉络与训练型方法的瓶颈

视频扩散模型（如 AnimateDiff）在文本驱动生成领域取得了显著进展，但赋予用户对生成视频的摄像机视角进行精确控制，仍是一个开放挑战。现有方法主要沿着“微调注入”的路线展开：**MotionCtrl** (Wang et al., SIGGRAPH 2024) 和 **CameraCtrl** 等代表性工作，通过在预训练扩散模型的 UNet 去噪网络中注入摄像机姿态嵌入，并在额外的配对视频-姿态数据集上进行微调，来实现对摄像机运动的控制。

然而，这条路线存在一个核心瓶颈：**微调过程不仅需要高昂的配对数据采集成本和训练计算开销，更关键的是，它会不可逆地破坏预训练模型已学到的生成分布，导致生成视频的视觉质量下降。** 从知识库定位来看，Latent-Reframe 正是针对这一瓶颈，将摄像机控制从“训练时注入”的范式，迁移到了“采样时操纵”的新范式上。

### 核心差异：从微调注入到采样重帧

Latent-Reframe 与上述训练型方法在以下两个关键维度上形成了根本性差异：

| 维度 | 训练型方法 (MotionCtrl / CameraCtrl) | Latent-Reframe (本文) |
|---|---|---|
| **摄像机控制注入方式** | 训练时通过微调将摄像机姿态嵌入注入扩散模型参数 | 采样阶段中途对潜在代码进行重帧（latent reframing），通过时间感知点云和 3D 重投影直接控制视角 |
| **是否需要训练** | 需要额外的配对视频-姿态数据集进行微调 | 完全无需训练，直接应用于预训练模型推理过程 |

这一范式转换的关键洞察在于：**预训练视频扩散模型的中间潜在表示已编码足够的场景三维与外观信息。** 在去噪过程的中途阶段，将部分去噪的潜在代码映射为时间感知 3D 点云，再根据目标摄像机姿态重新投影生成重帧视频，便可在采样时直接控制视角，而无需触及模型参数。这从知识库层面将摄像机控制问题重新定义为“潜在空间几何操纵”问题，而非“模型参数适配”问题。

### 方法管线与知识贡献

Latent-Reframe 的完整管线由四个模块串联而成，每个模块在知识库中对应着特定的技术选择与贡献：

1.  **近似干净视频估计**：在指定去噪步骤 $t$，利用 DDIM 公式从带噪潜在代码 $z_t$ 中估计出干净的潜在代码 $z_0$，并通过 VAE 解码还原像素空间视频 $x_0$。这一步为后续的几何操作提供了可处理的信号空间。

2.  **时间感知点云提取**：将像素视频序列输入 MonST3R 模型，通过滑动窗口和全局对齐优化（见 Eq. 3），为每一帧提取时间感知的 3D 点云。消融实验表明（Figure 4），相比静态点云，时间感知点云能更好地捕捉视频中的动态变化（如人脸运动、波浪），减少伪影，这是该方法在动态场景下保持生成质量的关键。

3.  **潜在重帧**：根据目标摄像机姿态调整每一帧的点云，再将这些点云重新投影为二维视频帧，实现视角变换。这一步是摄像机控制的直接执行环节。

4.  **潜在空间修复**：对重帧后因遮挡产生的空白区域进行潜在修复。通过遮罩 $m$ 区分已知/未知区域，对已知区域施加较轻噪声（降低 3 个去噪步骤），引导未知区域的去噪生成（见 Eq. 4 和 Algorithm 1），实现内容修补与和谐融合。消融实验（Figure 6）证实，噪声降低 3 步能在减少模糊与条带伪影之间达到最佳平衡。

### 适用边界与局限

尽管 Latent-Reframe 在无需训练的前提下实现了与训练型方法相当甚至更优的控制精度（Table 1：FID 60.18，FVD 509.11，TransErr 5.52），其适用边界仍受以下因素制约：

-   **大范围运动与极端遮挡**：当目标摄像机运动幅度较大时，未知遮挡区域过大可能导致修复后的视频出现视觉不一致和伪影。这是“采样时重帧”范式内在的局限——重帧操作本身会创造空白区域，修复能力受限于扩散模型的先验和剩余去噪步骤的调和空间。
-   **点云估计的误差传递**：点云估计模型（如 MonST3R）和姿态估计的误差会直接传递到最终的控制精度中。消融实验（Figure 7）虽表明 MonST3R 优于其他点云重建模型，但该环节仍是整个管线的精度上限。
-   **对复杂场景动态的鲁棒性**：目前方法对极深遮挡或复杂场景动态的鲁棒性有限，未来需要进一步提升失败案例的处理能力。

### 开放问题与知识库延伸

从知识库定位来看，Latent-Reframe 开辟了“采样时几何操纵”这一新方向，其后续延伸可沿以下路径展开：

1.  **更强的几何重建基座**：能否通过更先进的点云或三维重建模型（如 DUSt3R、MASt3R 等）进一步提高控制精度和生成质量？这是对管线中几何提取模块的直接升级。
2.  **跨架构泛化**：该方法的核心思想——在去噪中途对潜在表示进行结构化操纵——是否可以推广到其他潜在扩散模型架构（如 DiT）或其他生成任务（如图像编辑、多视角合成）？
3.  **大范围遮挡的修复策略**：如何处理大范围摄像机运动或极端遮挡带来的大面积未知区域，是该方法走向实际应用需要解决的关键工程问题。

## 原文 PDF

![[paperPDFs/arxiv_2024/Latent_Reframe_Enabling_Camera_Control_for_Video_Diffusion_Model_without_Training.pdf]]
