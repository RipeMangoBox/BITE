---
title: "Perception-as-Control: Fine-grained Controllable Image Animation with 3D-aware Motion Representation"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/Perception_as_Control_Fine_grained_Controllable_Image_Animation_with_3D_aware_Motion_Representation.pdf
project_link: https://chen-yingjie.github.io/projects/Perception-as-Control
code_link: null
aliases:
- PAC
- Perception-as-Control
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入3D感知运动表示，将场景简化为代表关键物体部分的单位球体和代表整体空间的棋盘格世界包络，从而将相机和物体运动转化为统一、空间对齐的视觉控制信号。"
primary_logic: "通过渲染一个带有3D感知的简化场景，将相机运动映射为世界包络的透视变化，将物体运动映射为球体的位置和大小变化，能够自然地解耦并协同控制相机和物体运动，实现精确且和谐的可控视频生成。"
claims:
- "在RealEstate数据集上，本方法的FVD为52.421，显著优于CameraCtrl（178.497）和MotionCtrl（122.570）。"
- "在WebVid数据集上，本方法的FVD为161.076，优于Motion-I2V（367.524）和MOFA-Video（175.701）。"
- "消融实验表明，加入世界包络（Env）和3D单位球体（Sph）比仅用2D位置或3D球体能显著提升物体运动控制性能（ObjMC指标）。"
- "三阶段训练策略（先相机、再协同、再稠密到稀疏微调）显著优于一阶段或两阶段训练（FVD 161.076 vs 318.941/254.907）。"
---

# Perception-as-Control: Fine-grained Controllable Image Animation with 3D-aware Motion Representation

> [!tip] 核心洞察
> 通过渲染一个带有3D感知的简化场景，将相机运动映射为世界包络的透视变化，将物体运动映射为球体的位置和大小变化，能够自然地解耦并协同控制相机和物体运动，实现精确且和谐的可控视频生成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 感知即控制：基于3D感知运动表示的细粒度可控图像动画 |
| 英文题名 | Perception-as-Control: Fine-grained Controllable Image Animation with 3D-aware Motion Representation |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2501.05020) · [Project](https://chen-yingjie.github.io/projects/Perception-as-Control) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Perception-as-Control |
| Dataset | RealEstate-10K, WebVid-10M |

> [!tip] 效果简介
> - RealEstate-10K 上，FVD 为 52.421，对比 CameraCtrl: 178.497, MotionCtrl: 122.570，变化 显著降低。
> - WebVid-10M 上，FVD 为 161.076，对比 Motion-I2V: 367.524, MOFA-Video: 175.701，变化 明显优于。

## 概要

可控图像动画旨在根据用户意图驱动静态图像中的相机和物体运动，但现有方法面临一个核心瓶颈：光流、点轨迹、Plücker坐标等运动表示难以同时支持相机与物体运动的细粒度协同控制——它们要么将两类运动信号混叠注入导致冲突，要么因缺乏显式3D空间理解而无法保证运动的空间一致性。

**Perception-as-Control** 提出了一种“感知即控制”的范式转换：将运动控制问题转化为对简化3D场景的视觉感知问题。其核心思想是，将参考图像对应的场景抽象为两类3D感知基元——代表关键物体部分的**单位球体**和容纳所有物体的**世界包络**（带棋盘格纹理的单位立方体）。通过操纵这些基元并从不同视点渲染，相机运动自然映射为世界包络的透视变化，物体运动映射为球体的位置与尺度变化，从而将两类运动解耦为统一、空间对齐的视觉控制信号（Figure 2）。

该方法的关键因果机制在于：3D感知运动表示在信号层面完成了相机与物体的**空间解耦**——世界包络提供全局空间参照，单位球体提供局部物体定位，两者通过分离的轻量编码器注入扩散模型，避免了RGB层面的信号干扰（Figure 3）。配合三阶段训练策略（先训练相机控制、再引入物体协同、最后进行稠密到稀疏的微调），模型逐步习得精细的协同运动控制能力。

主要实验结论如下：
- 在RealEstate-10K相机运动控制基准上，FVD达到52.421，显著优于CameraCtrl（178.497）和MotionCtrl（122.570）（Table 1）。
- 在WebVid-10M物体运动控制基准上，FVD为161.076，明显优于Motion-I2V（367.524）和MOFA-Video（175.701）（Table 2）。
- 消融实验证实，世界包络与3D单位球体的组合是性能的关键来源：仅用2D点位置或仅用3D球体均导致物体运动控制指标显著下降（Table 3），且定性结果中缺乏深度线索会导致空间关系模糊（Figure 7）。
- 三阶段训练策略的FVD（161.076）远优于两阶段（254.907）和一阶段（318.941）训练（Table 4）。

方法的主要局限在于：单位球体简化无法表达物体旋转运动；受基座模型能力限制，对人物等复杂动作的生成效果欠佳；所用现成算法（TartanVO、SpaTracker）的精度会传导影响最终性能。

**方法定位**：Perception-as-Control属于基于扩散模型的可控视频生成方法，其运动表示与具体基座架构正交——论文在SVD版本的CameraCtrl和MotionCtrl上验证了该表示的即插即用特性。相较于CameraCtrl（仅相机控制）、MotionCtrl（相机与物体控制但信号混叠）、Motion-I2V和MOFA-Video（仅物体控制）等基线，本方法首次实现了基于统一3D感知表示的相机-物体细粒度协同控制。

图像动画——即从单张静态参考图像出发，生成一段符合用户意图的动态视频——是视觉内容生成领域的核心任务之一。其难点在于，生成过程不仅需要保持参考图像的外观一致性，还必须精确地控制场景中相机和物体的运动。近年来，基于扩散模型的视频生成方法取得了长足进步，但在运动控制粒度上仍面临显著瓶颈。

现有运动控制方法主要依赖2D光流、Plücker坐标或稀疏轨迹点作为控制信号。这些表示形式存在一个根本性缺陷：它们难以在一个统一的框架内，同时支持相机运动和物体运动的协同控制。具体而言，相机运动（如平移、旋转、变焦）与物体运动（如位移、缩放）在2D信号空间中往往相互耦合，导致控制指令之间产生冲突，最终生成的视频出现运动不协调、物体漂移或空间关系错乱等问题。例如，**CameraCtrl**（He et al., arXiv 2024）专注于相机轨迹控制，**Motion-I2V**（Shi et al., arXiv 2024）和**MOFA-Video**（Li et al., arXiv 2024）则侧重于物体运动，而**MotionCtrl**（Wang et al., arXiv 2023）虽尝试同时处理两者，但因其控制信号缺乏空间对齐性，协同效果仍不理想。

这一瓶颈的本质在于：2D控制信号丢失了场景的三维空间结构信息。当相机和物体同时运动时，2D表示无法自然地解耦“观察者视角变化”与“场景内物体移动”这两种本质上不同的运动来源。因此，要实现细粒度、无冲突的协同运动控制，关键不在于设计更复杂的控制信号注入机制，而在于重新定义运动表示本身——使其具备3D感知能力，从而在信号层面就实现相机与物体运动的自然解耦。

本文的动机正是源于这一洞察：如果我们将参考图像对应的3D场景简化为一个可操作的感知模型，并将相机和物体运动统一转化为该模型在不同视角下的视觉变化，那么运动控制问题就转化为一个“感知”问题。这种“感知即控制”的思路，使得相机运动对应于对整个场景包络的透视观察变化，物体运动对应于场景内关键部件的空间位置变化，二者在统一的3D空间中对齐，从根源上消除了控制信号层面的冲突。

## 核心方法与创新机理

本工作的核心创新在于将图像动画的可控生成问题重新定义为“感知即控制”：通过构建一个**3D感知的运动表示**，将相机运动和物体运动统一转化为空间对齐的视觉控制信号，从而实现对两者的细粒度、无冲突协同控制。

### 瓶颈突破：从2D信号到3D感知表示

现有方法依赖2D光流、Plücker坐标或稀疏轨迹等运动表示，这些信号要么无法同时支持相机与物体运动的独立控制，要么在协同控制时产生冲突。根本原因在于，2D信号缺乏对场景三维结构的显式建模，相机运动引起的透视变化与物体自身的运动在图像平面上难以解耦。

本方法的核心洞察是：将参考图像对应的3D场景简化为一个**世界包络（World Envelope）**和若干代表关键物体部分的**单位球体**。世界包络是一个带有棋盘格纹理的单位立方体，代表整体空间；单位球体则标记物体的关键部位。通过操纵这些球体并从不同视角“观察”这个简化场景，相机运动被映射为世界包络的透视变化，物体运动被映射为球体的位置和大小变化——两者在统一的3D空间中自然解耦，形成空间对齐的视觉控制信号。

### 关键Changed Slots

与基线方法相比，本工作在以下三个维度实现了根本性改变：

**1. 运动控制信号表示：从2D/隐式信号到解耦的3D感知层**

基线方法（如**CameraCtrl**（He et al., arXiv 2024）的Plücker坐标、**MotionCtrl**（Wang et al., arXiv 2023）的光流）使用单一或混合的2D运动表示，难以同时精确控制相机和物体。本方法分别渲染两个3D感知层作为控制信号：世界包络渲染图编码相机运动，单位球体投影图编码物体运动。消融实验（Table 3）证实，世界包络与3D单位球体的组合在物体运动控制指标（ObjMC）上达到23.32，显著优于仅用3D球体（29.47）和2D点位置（30.61）。

**2. 控制信号注入方式：从直接叠加到分路编码融合**

基线方法通常将运动信号直接叠加到噪声潜变量或通过单一辅助分支注入，容易造成RGB层面的信号干扰。本方法采用两个轻量编码器分别编码相机和物体控制信号，经融合模块合并后再注入U-Net去噪网络。这种分离编码策略避免了不同运动模态在像素空间的相互污染。

**3. 训练策略：从单/两阶段到三阶段课程学习**

为实现细粒度协同控制，本方法引入三阶段训练策略（Sec. 3.4）：第一阶段仅训练相机运动控制，第二阶段引入物体运动控制进行协同训练，第三阶段进行稠密到稀疏的微调以提升泛化能力。消融实验（Table 4）表明，三阶段训练的FVD为161.076，显著优于两阶段（254.907）和一阶段（318.941），验证了渐进式课程学习对复杂协同任务的关键作用。

### 方法局限性

尽管3D感知运动表示在解耦相机与物体运动方面表现出色，但将物体部分简化为单位球体意味着该表示**无法表达物体的旋转运动**。此外，整体的3D场景构建依赖于现成算法（TartanVO用于相机姿态估计、SpaTracker用于3D点跟踪），这些算法的精度直接影响控制信号的质量。对于人物动作等复杂运动，受基座模型能力限制，生成效果仍有不足。

![[assets/figures/papers/paper_list_l23_Perception_as_Control_Fine_grained_Controllable_Image_Animation_with_3D/figures/001_Figure_1.jpg]]
*Figure 1: Potential applications for Perception-as-Control. By constructing 3D-aware motion representation based on user intentions and utilizing the perception results as motion control signals, the proposed fine-grained motion-controllable image animation framework can be applied to various motion-related video synthesis tasks, such as image-based motion generation (animate image according to user instructions), and video-based motion clone (mimic the entire motions), motion transfer (relocate and rescale local motions based on semantic correspondence), local motion editing (edit fine-grained scene and object motions in user-specified regions)*

Perception-as-Control 的整体框架遵循“感知即控制”的核心思想：将用户意图解析为 3D 感知运动表示，再将该表示的渲染结果作为控制信号注入视频扩散模型，驱动图像动画生成。框架由三个关键环节构成：**数据管护流水线**（从野生视频自动构建 3D 感知运动表示）、**网络架构**（双编码器注入控制信号）、以及**三阶段训练策略**（渐进式学习协同控制）。

### 数据管护流水线

为从野生视频中获取训练所需的控制信号，框架设计了一套自动化数据管护流水线（Figure 3）。给定一段野生视频，流水线依次执行以下步骤：

1. **场景剪切与运动过滤**：使用 SceneCut 提取视频片段，并过滤无明显运动的片段。
2. **3D 点跟踪**：在每帧上采样 25×25 的网格点，使用 SpaTracker 跟踪这些关键点的 3D 位置，得到三维轨迹 $\mathbf{P} = [P^x, P^y, P^z]^T \in \mathbb{R}^{L \times N \times 3}$，其中 $L$ 为帧数，$N$ 为点数。
3. **相机姿态估计**：使用 TartanVO 从视频帧中恢复相机轨迹，得到相机内参和外参序列。
4. **3D 场景渲染**：基于跟踪结果和相机参数，构建并渲染 3D 感知运动表示——将场景简化为一个**世界包络**（带棋盘格纹理的单位立方体，代表整体空间）和若干**单位球体**（代表关键物体部分）。从指定视角渲染这些简化几何体，分别得到相机控制信号和物体控制信号。

### 网络架构

框架以 U-Net 结构的时间扩散模型为基础，通过两条独立路径注入控制信号（Figure 3）：

- **相机编码器**与**物体编码器**：两个轻量编码器分别处理相机控制信号（世界包络渲染图）和物体控制信号（单位球体投影图）。分离编码的设计旨在避免 RGB 层面的信号干扰。
- **融合模块**：将相机和物体编码器的输出合并，形成统一的运动控制信号，以加性方式注入到扩散模型的噪声潜变量中。
- **ReferenceNet**：注入参考图像以保持生成帧与输入图像的外观一致性。

### 三阶段训练策略

为实现细粒度协同运动控制，框架采用渐进式三阶段训练策略（对应 Eq. 3 的统一噪声预测损失 $\mathcal{L} = \mathbb{E}_{x_0, c_{\mathrm{img}}, c_{\mathrm{cam}}, c_{\mathrm{obj}}, t} [|| \epsilon - \epsilon_{\theta}(x_t, c_{\mathrm{img}}, c_{\mathrm{cam}}, c_{\mathrm{obj}}, t) ||_2^2]$）：

1. **阶段一（相机控制）**：仅使用相机控制信号训练，使模型学会精确的相机运动控制。
2. **阶段二（协同控制）**：同时使用相机和物体控制信号训练，建立协同运动控制能力。
3. **阶段三（稠密到稀疏微调）**：以更低学习率进行微调，提升对稀疏控制信号的泛化能力。

训练参数：阶段一和阶段二各约 20k 次迭代，学习率 $1 \times 10^{-5}$；阶段三约 50k 次迭代，学习率 $1 \times 10^{-6}$，batch size 为 1。

### 推理流程

推理时，用户意图首先被解析为 3D 感知运动表示——即操纵世界包络的视角变化来表达相机运动，操纵单位球体的位置和大小来表达物体运动。随后，框架渲染该表示并从指定视角“感知”场景，得到的视觉信号作为控制条件驱动视频扩散模型生成动画帧。这种统一的表示方式使得框架能够支持图像运动生成、视频运动克隆、运动迁移和局部运动编辑等多种应用（Figure 1）。

### 输入输出流

- **输入**：一张参考图像 + 用户指定的运动意图（相机轨迹、物体运动描述等）。
- **中间表示**：3D 感知运动表示（世界包络 + 单位球体的空间配置）。
- **控制信号**：从 3D 感知表示渲染得到的相机控制图和物体控制图。
- **输出**：与参考图像外观一致、运动符合用户意图的视频帧序列。

### 扩散模型基础

本工作基于视频扩散模型（Video Diffusion Model, VDM）构建可控图像动画框架。给定一段视频的潜变量表示 $x_0$，前向扩散过程按如下方式逐步注入高斯噪声：

$$x_t = \sqrt{\hat{\alpha}_t} x_{t-1} + \sqrt{1 - \hat{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$$

其中 $\hat{\alpha}_t$ 为累积噪声调度参数，$t$ 为扩散时间步。去噪网络 $\epsilon_\theta$ 的训练目标是最小化噪声预测的均方误差：

$$\mathcal{L}_{\theta} = \mathbb{E}_{x_0, \epsilon, \mathcal{C}, t} \left[|| \epsilon - \hat{\epsilon_{\theta}}(x_t, \mathcal{C}, t) ||_2^2\right]$$

此处 $\mathcal{C}$ 为条件信号集合，在本框架中具体包含参考图像 $c_{\mathrm{img}}$、相机控制信号 $c_{\mathrm{cam}}$ 和物体控制信号 $c_{\mathrm{obj}}$。三阶段训练的统一损失函数为：

$$\mathcal{L} = \mathbb{E}_{x_0, c_{\mathrm{img}}, c_{\mathrm{cam}}, c_{\mathrm{obj}}, t} \left[|| \epsilon - \epsilon_{\theta}(x_t, c_{\mathrm{img}}, c_{\mathrm{cam}}, c_{\mathrm{obj}}, t) ||_2^2\right]$$

### 数据管护流程（Data Curation Pipeline）

该模块负责从野生视频中自动构建3D感知运动表示，是方法的核心基础设施。流程包含四个子步骤（Fig. 3）：

1. **场景剪切与运动过滤（SceneCut & Motion Filtering）**：提取视频片段，过滤无明显运动的片段，确保训练数据包含有效运动信息。
2. **3D点跟踪（3D Point Tracking）**：使用现成工具 **SpaTracker** 在每帧的 $25 \times 25$ 网格上跟踪关键点，输出3D点跟踪结果 $\mathbf{P} = [P^x, P^y, P^z]^T \in \mathbb{R}^{L \times N \times 3}$，其中 $L$ 为帧数，$N$ 为跟踪点数量。
3. **相机姿态估计（Camera Pose Estimation）**：使用 **TartanVO** 从视频中恢复相机轨迹，获得每帧的相机外参和内参。
4. **3D场景渲染（Perceptual 3D Scene Rendering）**：基于上述结果构建并渲染3D感知运动表示，生成相机和物体控制信号。

### 3D感知运动表示

这是方法的**核心因果旋钮**。给定参考图像，将对应3D场景简化为两个可渲染的组成元素（Fig. 2）：

- **世界包络（World Envelope）**：一个带有棋盘格纹理的单位立方体，代表容纳所有物体的整体空间。相机运动被映射为从不同视点观察该包络时的透视变化。
- **单位球体（Unit Spheres）**：若干代表关键物体部分的单位球体。物体运动被映射为球体在空间中的位置和大小变化。

通过分别渲染这两个元素，相机运动（世界包络的透视变化）和物体运动（球体的位置/大小变化）被转化为统一、空间对齐的视觉信号，自然解耦了两种运动模态，避免了光流等方法中常见的冲突控制问题。

### 控制信号注入架构

框架采用双编码器设计以避免RGB层面的信号干扰（Fig. 3）：

- **相机编码器（Camera Encoder）**：轻量编码器，专门编码世界包络渲染图作为相机控制信号 $c_{\mathrm{cam}}$。
- **物体编码器（Object Encoder）**：轻量编码器，专门编码单位球体投影图作为物体控制信号 $c_{\mathrm{obj}}$。
- **融合模块（Fusion Module）**：合并两个编码器的输出，形成统一的运动控制信号，注入方式为直接叠加到噪声潜变量上。
- **ReferenceNet**：独立分支注入参考图像 $c_{\mathrm{img}}$，用于保持生成帧的外观一致性。

### 三阶段训练策略

训练分三个阶段逐步引入控制能力（Table 4 消融验证其必要性）：

1. **阶段一（相机控制训练）**：仅使用相机控制信号 $c_{\mathrm{cam}}$ 训练，约20k迭代，学习率 $1 \times 10^{-5}$。
2. **阶段二（协同控制训练）**：同时引入相机和物体控制信号，约20k迭代，学习率 $1 \times 10^{-5}$。
3. **阶段三（稠密到稀疏微调）**：逐步降低物体控制信号的稠密度（从全帧控制过渡到稀疏关键帧控制），约50k迭代，学习率 $1 \times 10^{-6}$。

消融实验表明，三阶段策略的FVD为161.076，显著优于两阶段（254.907）和一阶段（318.941）训练，验证了渐进式引入控制能力的有效性。

## 实验与关键发现

### 主要结果

**相机运动控制。** 在RealEstate-10K测试集上，Perception-as-Control取得了52.421的FVD，大幅领先于CameraCtrl（178.497）和MotionCtrl（122.570）（Table 1）。为保证公平，作者复现了CameraCtrl的16帧版本（CameraCtrl*）。定性比较（Figure 5）显示，CameraCtrl在分布外相机轨迹上会出现退化，而本方法能泛化并实现精确的相机运动控制。

![[assets/figures/papers/paper_list_l23_Perception_as_Control_Fine_grained_Controllable_Image_Animation_with_3D/figures/006_Table_1.jpg]]
*Table 1: Comparison on RealEstate test set for camera motion control. CameraCtrl* denotes the 16-frame version we reproduced. Table 2. Comparison on WebVid test set for object motion control*

**物体运动控制。** 在WebVid-10M测试集上，本方法FVD为161.076，显著优于Motion-I2V（367.524）和MOFA-Video（175.701）（Table 2）。Figure 6的定性结果表明，基于光流的方法面临控制冲突问题，且在较大物体运动下难以保持物体外观。

**协同运动控制。** Figure 4展示了细粒度协同运动控制的结果，验证了3D感知运动表示在同时处理相机和物体运动时的有效性。

### 消融实验

**运动表示的消融。** Table 3系统比较了不同运动表示方案对物体运动控制指标（ObjMC）的影响：

![[assets/figures/papers/paper_list_l23_Perception_as_Control_Fine_grained_Controllable_Image_Animation_with_3D/figures/007_Table_3.jpg]]
*Table 3: Ablation study on 3D-aware motion representation. Env denotes our world envelope and Sph denotes 3D unit spheres*

- 仅使用2D点位置：ObjMC为30.61，性能最差。Figure 7a的定性证据表明，缺少深度信息使得空间关系不清晰，损害了控制精度。
- 仅使用3D单位球体：ObjMC为29.47。Figure 7b显示，缺乏世界包络作为空间参照时，仅靠球体可能引发歧义问题。
- 世界包络（Env）结合3D单位球体（Sph）：ObjMC达到23.32，取得最佳性能，验证了两种渲染层协同提供空间对齐控制信号的必要性。

![[assets/figures/papers/paper_list_l23_Perception_as_Control_Fine_grained_Controllable_Image_Animation_with_3D/figures/011_Figure_7.jpg]]
*Figure 7: Qualitative evidence for ablation study*

**训练策略的消融。** Table 4对比了不同训练策略对FVD的影响：

![[assets/figures/papers/paper_list_l23_Perception_as_Control_Fine_grained_Controllable_Image_Animation_with_3D/figures/010_Table_4.jpg]]
*Table 4: Ablation study on the proposed training strategy*

- 单阶段训练：FVD为318.941。
- 两阶段训练：FVD为254.907。
- 三阶段训练（本方法）：FVD为161.076，性能提升显著。

三阶段策略依次进行相机控制训练、协同控制训练、稠密到稀疏微调，逐步引入控制信号复杂度，有效避免了多信号同时训练时的干扰和收敛困难。

### 失败模式与局限性

1. **物体旋转无法表示。** 将物体部分简化为单位球体本质上只能编码平移和缩放，无法表达旋转运动，限制了细粒度控制的范围。
2. **复杂运动生成质量受限。** 受基座模型能力约束，对人物动作等高度复杂的运动模式生成效果不佳，这属于模型容量层面的瓶颈。
3. **上游算法精度依赖。** 数据管护流程依赖TartanVO（相机姿态估计）和SpaTracker（3D点跟踪）等现成算法，这些算法的精度直接影响3D感知运动表示的构建质量，进而影响最终控制性能。
4. **深度估计不精确。** 深度估计不够准确时，世界包络和球体的空间定位可能产生偏差，影响场景理解的一致性。

### 关键图表结论

- **Table 1 & Table 2**：在相机和物体运动控制两个维度上，本方法均以显著优势超越现有基线，验证了3D感知运动表示作为统一控制信号的有效性。
- **Table 3**：世界包络与3D单位球体的组合是性能最优的运动表示方案，二者缺一均会导致控制精度下降。
- **Table 4**：三阶段训练策略是实现细粒度协同控制的关键，单阶段或两阶段训练均无法达到可比性能。
- **Figure 7**：提供了消融实验的定性证据，直观展示了缺少深度信息（2D点位置）和缺少空间参照（仅3D球体）时的失败模式。

### 补充图表

![[assets/figures/papers/paper_list_l23_Perception_as_Control_Fine_grained_Controllable_Image_Animation_with_3D/figures/016_Figure_13.jpg]]
*Figure 13: The frameworks of MotionCtrl++ and CameraCtrl++. (a) One-stage Training*

## 定位与知识库关联

### 与现有基线方法的关系

本工作 **Perception-as-Control** 处于可控图像动画（controllable image animation）这一研究方向，其核心贡献在于提出了一种统一的 3D 感知运动表示，以解决现有方法中相机运动与物体运动控制难以协同、细粒度控制精度不足的问题。

#### 相对于相机运动控制方法

现有相机运动控制方法主要依赖 Plücker 坐标或光流作为控制信号。**CameraCtrl**（He et al., arXiv 2024）通过 Plücker 射线嵌入实现相机轨迹控制，但在分布外（out-of-distribution）轨迹上容易出现退化。本方法将相机运动转化为对世界包络（world envelope）的透视渲染观察，使控制信号在空间上天然对齐于生成帧，从而在 RealEstate-10K 测试集上取得 FVD 52.421，显著优于 CameraCtrl 的 178.497（Table 1）。这一差距的因果机制在于：世界包络的棋盘格纹理为模型提供了显式的深度与透视线索，而 Plücker 坐标缺乏这种场景级空间参照。

#### 相对于物体运动控制方法

物体运动控制方面，**Motion-I2V**（Shi et al., arXiv 2024）使用稀疏轨迹，**MOFA-Video**（Li et al., arXiv 2024）则通过光流实现运动迁移。这些方法面临的核心瓶颈是控制信号与 RGB 生成空间之间的语义鸿沟——2D 轨迹或光流无法传达物体在三维空间中的尺度变化和遮挡关系。本方法将关键物体部分简化为 3D 单位球体，通过球体位置和投影大小的变化编码物体运动，在 WebVid-10M 测试集上 FVD 达 161.076，明显优于 Motion-I2V（367.524）和 MOFA-Video（175.701）（Table 2）。

#### 相对于协同控制方法

**MotionCtrl**（Wang et al., arXiv 2023）是少数同时支持相机和物体运动控制的方法，但其将两类信号分别处理后直接叠加，缺乏统一的 3D 空间参照，导致协同控制时出现冲突（如相机平移与物体位移的视觉不一致）。本方法通过将相机和物体运动统一渲染到同一 3D 感知场景中（世界包络 + 单位球体），从根本上消除了信号冲突——两类运动在渲染阶段就已实现空间对齐，而非在特征空间中强行融合。

### 方法适用边界

1. **物体旋转运动受限**：当前 3D 感知运动表示将物体部分简化为单位球体，仅能编码位置和尺度变化，无法表示物体的三维旋转。对于需要旋转控制的场景（如翻转、扭转物体），本方法存在原理性局限。

2. **复杂运动生成能力受基座模型制约**：本方法基于 U-Net 架构的视频扩散模型，对人物动作等高度非刚性运动生成质量有限。这是基座模型能力的上限，而非运动表示本身的问题。

3. **依赖现成算法的精度链**：数据管护流程依赖 SpaTracker（3D 点跟踪）、TartanVO（相机姿态估计）和深度估计等现成算法。这些模块的误差会沿管线传播，影响最终控制信号的精度。深度估计不够精确时，世界包络的透视渲染可能出现失真，进而影响场景理解。

4. **用户意图到运动表示的转换效率**：推理阶段需要将用户意图手动或半自动地转化为 3D 感知运动表示（球体位置、大小、相机轨迹），这一过程目前尚未自动化，在实际应用中可能构成效率瓶颈。

### 开放问题

1. **运动表示的完备性扩展**：如何将物体旋转、非刚性形变等更丰富的运动形式纳入 3D 感知运动表示框架？可能的路径包括用椭球体或可变形网格替代刚性球体，但这会显著增加表示的复杂度。

2. **与更强基座模型的结合**：若将 3D 感知运动表示与基于 DiT（Diffusion Transformer）架构或更大规模预训练的视频生成模型结合，能否突破当前在复杂人体运动上的性能瓶颈？这需要验证运动表示在不同架构中的泛化能力。

3. **3D 场景构建精度的提升**：采用更先进的 SLAM 系统（如 DROID-SLAM）或单目深度估计方法（如 Depth Anything V2）替代当前管线中的 TartanVO 和基础深度估计，是否能在不显著增加计算成本的前提下提升控制精度？

4. **自动化意图解析**：能否通过多模态大语言模型直接从自然语言指令或手绘草图自动构建 3D 感知运动表示，从而实现端到端的用户友好型运动控制？这涉及视觉-语言对齐与空间推理的交叉问题。

5. **多物体协同与交互**：当前方法通过多个单位球体表示不同物体部分，但球体之间缺乏物理约束（如碰撞、遮挡一致性）。引入物理先验或场景图约束是否能提升多物体协同运动的真实感？

## 原文 PDF

![[paperPDFs/ICCV_2025/Perception_as_Control_Fine_grained_Controllable_Image_Animation_with_3D_aware_Motion_Representation.pdf]]
