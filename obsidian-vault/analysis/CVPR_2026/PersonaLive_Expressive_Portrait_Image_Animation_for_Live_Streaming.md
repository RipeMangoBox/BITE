---
title: PersonaLive! Expressive Portrait Image Animation for Live Streaming
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PersonaLive_Expressive_Portrait_Image_Animation_for_Live_Streaming.pdf
project_link: null
code_link: "https://github.com/GVCLab/PersonaLive"
aliases:
- PEPIALS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过外观蒸馏将采样步数压缩至4步，并采用自回归微块流式生成范式消除分块冗余与曝光偏差，是实现实时低延迟流式生成的关键。
primary_logic: 人像动画中的运动与结构布局主要由最初几个去噪步确定，后续大量迭代主要用于外观细节的逐渐细化，存在冗余；因此可通过蒸馏将外观细化过程压缩为极少采样步。同时，用滑窗训练策略和历史关键帧机制消除自回归生成中的曝光偏差和误差累积，保证长视频的时序一致性。
claims:
- 去噪轨迹显示，在无需CFG的情况下，第一帧去噪步已基本确定布局和运动，后续步骤仅精细化外观（图3）
- 采用4步采样和对抗损失的外观蒸馏能够在不降低视觉质量的前提下大幅提升效率，若移除蒸馏则质量显著下降（图6）
- 滑窗训练策略是防止时序崩溃的关键，去掉后身份相似度从0.698暴跌至0.549（表2、图7）
- PersonaLive在交叉重演上的FVD/tLP优于所有扩散基线，且推理速度达到15.82 FPS，延迟仅0.253s，比现有扩散方法快7-22倍（表1）
---

# PersonaLive! Expressive Portrait Image Animation for Live Streaming

> [!tip] 核心洞察
> 人像动画中的运动与结构布局主要由最初几个去噪步确定，后续大量迭代主要用于外观细节的逐渐细化，存在冗余；因此可通过蒸馏将外观细化过程压缩为极少采样步。同时，用滑窗训练策略和历史关键帧机制消除自回归生成中的曝光偏差和误差累积，保证长视频的时序一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | PersonaLive! 面向实时流式直播的富有表现力的人像动画 |
| 英文题名 | PersonaLive! Expressive Portrait Image Animation for Live Streaming |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.11253) · [Code](https://github.com/GVCLab/PersonaLive) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PersonaLive |
| Dataset | TalkingHead-1KH, LV100, Efficiency |

> [!tip] 效果简介
> - TalkingHead-1KH (Self-Reenactment) 上，L1↓ 0.039 vs LivePortrait: 0.043 (↓9.3%)；LPIPS↓ 0.129 vs LivePortrait: 0.137 (↓5.8%)。
> - LV100 (Cross-Reenactment) 上，FVD↓ 520.6 vs LivePortrait: 557.2 (↓6.6%)；tLP↓ (×10⁻³) 12.83 vs LivePortrait: 13.51 (↓5.0%)。
> - Efficiency (H100 GPU) 上，FPS↑ 15.82 vs Megactor-Σ: 2.216 (next best diffusion after LivePortrait GAN) (7.1×)。

## 概述

**问题与瓶颈**：人像动画在直播场景中面临双重挑战——既要生成富有表现力的面部动态，又必须满足实时流式传输的严格延迟要求。现有扩散式人像动画模型（如 **X-Portrait** (Xie et al., SIGGRAPH 2024)、**Megactor-Σ** (Yang et al., AAAI 2025)、**X-NeMo** (Zhao et al., ICLR 2025)、**HunyuanPortrait** (Xu et al., CVPR 2025)）通常需要20步以上的去噪迭代，并采用分块重叠处理，导致推理延迟高、误差在块间累积，难以支撑长视频的实时生成与时间稳定性。

**核心洞察**：论文通过观察去噪轨迹发现，人像动画的运动与结构布局在最初的去噪步中已基本确定，后续大量迭代主要用于外观细节的逐步精细化，存在显著冗余（见图3）。这一观察揭示了扩散模型在人像动画任务上的效率瓶颈根源。

**方法定位**：PersonaLive 提出三阶段流水线，将这一洞察转化为实时流式生成能力：
- **混合运动控制**：采用隐式面部表征与3D隐式关键点的混合信号，同时控制精细表情与全局头部姿态。
- **外观蒸馏压缩**：通过结合MSE、LPIPS和对抗损失的外观蒸馏策略，将去噪步数从常规的20+步压缩至4步，在保持视觉质量的同时大幅提升推理效率。
- **流式生成范式**：设计自回归微块流式生成架构，配合滑窗训练策略和历史关键帧机制，消除自回归生成中的曝光偏差和时序漂移，实现低延迟、时序连贯的连续视频输出。

**主要结果**：在交叉重演基准 LV100 上，PersonaLive 以仅4步采样取得 FVD 520.6、tLP 12.83，优于扩散基线；在单张 NVIDIA H100 GPU 上推理速度达15.82 FPS，延迟仅0.253秒，相比现有扩散方法实现7–22倍加速，首次将扩散式人像动画推进到实时流式直播所需的性能区间。

## 背景与动机

### 人像动画的现实需求与技术挑战

实时人像动画旨在通过驱动信号（如另一段视频或面部运动参数）操控静态肖像照片，生成逼真且时序连贯的说话头视频。这一技术在虚拟直播、视频会议、数字人交互等场景中具有广泛的应用前景。然而，面向**实时流式直播**的人像动画对系统提出了极为苛刻的要求：不仅需要生成高质量、身份保持、表情精准的视频帧，还必须在**极低延迟**下实现**持续不间断**的长视频输出。

### 现有方法的瓶颈

当前人像动画方法主要分为两类：基于生成对抗网络（GAN）的帧式方法和基于扩散模型的方法。

**GAN方法**（如 **LivePortrait**，2024）以逐帧独立生成的方式运行，推理速度极快，但生成的肖像往往缺乏细粒度细节，面部纹理和表情精细度不足。

**扩散式方法**（如 **X-Portrait**，Xie et al., SIGGRAPH 2024；**Megactor-Σ**，Yang et al., AAAI 2025；**X-NeMo**，Zhao et al., ICLR 2025；**HunyuanPortrait**，Xu et al., CVPR 2025）能够生成更高质量、细节更丰富的人像动画，但面临两大核心瓶颈：

1. **去噪步数过多**：现有扩散模型通常需要20步以上的迭代去噪，并配合无分类器引导（CFG）以保证生成质量，导致单帧推理耗时极长。例如，X-Portrait的延迟高达14.10秒，Megactor-Σ的FPS仅为2.216，完全无法满足实时性要求。

2. **分块重叠处理的冗余与误差累积**：为生成长视频，现有方法将视频划分为固定长度片段独立生成，通过重叠帧或复用尾部帧来维持片段间一致性。这种范式不仅引入了大量冗余计算，还因片段边界的曝光偏差导致误差逐步累积，最终引发时序崩溃。

### 核心洞察与动机

PersonaLive的提出源于一个关键观察：**在人像动画的去噪过程中，运动与结构布局主要由最初几个去噪步确定，后续大量迭代主要用于外观细节的逐渐细化，存在显著的冗余**。如Figure 3所示，在无CFG的条件下，第一帧去噪步已基本确定画面的布局和运动姿态，后续步骤仅对纹理、光影等外观细节进行精细化。这一发现意味着，通过蒸馏技术将外观细化过程压缩为极少采样步，理论上可以在不牺牲视觉质量的前提下大幅降低推理延迟。

此外，为消除分块重叠带来的冗余与曝光偏差，需要设计一种**原生流式生成范式**，使模型能够在推理时持续输出干净帧，而非依赖后处理拼接。这要求训练策略能够模拟推理时的自回归过程，使模型学会纠正自身预测误差；同时需要一种机制来抑制长视频中的时序漂移。

基于以上洞察，PersonaLive以**实时流式直播**为目标，从三个层面重构人像动画管线：(1) 采用混合隐式运动信号实现富有表现力的运动控制；(2) 通过外观蒸馏将采样步数压缩至4步；(3) 提出自回归微块流式生成范式，配合滑窗训练与历史关键帧机制，实现低延迟、时序稳定的长视频生成。

## 核心创新

PersonaLive 的核心创新在于系统性地重构了扩散式人像动画的生成范式，使其从“离线高延迟”走向“实时流式”。其关键创新点可归纳为三个相互耦合的 changed slots：

### 1. 混合隐式运动控制：从 2D 关键点到隐式表情与 3D 头部解耦

现有扩散式人像动画方法（如 **X-Portrait** (Xie et al., SIGGRAPH 2024)、**Megactor-Σ** (Yang et al., AAAI 2025)）通常依赖 2D 关键点或驱动视频帧作为运动信号，难以同时精细控制面部微表情与全局头部姿态。PersonaLive 提出混合隐式运动信号，将运动控制分解为两个互补通道：

- **隐式面部表征**：用于捕获精细的面部表情动态（如眼睑、嘴角的微小变化）；
- **3D 隐式关键点**：用于控制全局头部旋转、平移与缩放，通过从驱动图像和源图像分别提取 3D 参数（$k_{c,d}, R_d, t_d, s_d$ 和 $k_{c,s}, R_s, t_s, s_s$），并将规范关键点变换至驱动姿态：

$$k_d = s_d \cdot k_{c,s} R_d + t_d$$

这种解耦设计使模型能同时实现富有表现力的局部表情控制和鲁棒的全局头部运动控制，为后续的蒸馏与流式生成奠定了运动表示基础。

### 2. 少步外观蒸馏：将去噪冗余压缩至 4 步

**瓶颈洞察**：PersonaLive 通过观察无 CFG 条件下的去噪轨迹发现，人像动画中每帧的运动与结构布局在最早的去噪步已基本确定，后续大量迭代主要用于外观细节的逐渐细化，存在显著冗余（图 3）。这一洞察揭示了扩散模型在特定任务上的计算浪费。

**创新机制**：基于上述观察，PersonaLive 提出少步外观蒸馏策略，将去噪过程压缩为 4 步紧凑采样计划 $[0, 333, 666, 999]$，并通过混合损失函数进行蒸馏训练：

$$\mathcal{L}_{distill} = \mathcal{L}_2(\hat{x}, x^{gt}) + \lambda_{lpips}\mathcal{L}_{lpips}(\hat{x}, x^{gt}) + \lambda_{adv}\mathcal{L}_{adv}(\hat{x})$$

该损失结合了像素级 MSE、感知级 LPIPS 和对抗损失，使蒸馏模型在仅 4 步采样的条件下仍能保持高视觉质量。为提升训练效率，梯度仅通过最后一步反向传播，而随机步采样确保所有中间时间步均获得监督。消融实验表明，直接减少采样步数而不进行蒸馏会导致视觉质量严重退化；加入蒸馏但移除对抗损失则使输出过于平滑、缺乏高频细节（图 6）。这一创新使 PersonaLive 无需 CFG 即可生成高质量结果，推理速度较现有扩散方法提升 7–22 倍。

### 3. 自回归微块流式生成：消除分块冗余与曝光偏差

**瓶颈洞察**：现有扩散方法采用固定长度分块独立生成，通过重叠帧或复用尾部帧保证块间一致性，导致冗余计算和误差累积，无法满足流式场景的低延迟与长视频稳定性需求。

**创新机制**：PersonaLive 提出自回归微块流式生成范式，核心设计包括：

- **微块去噪窗口**：每个去噪窗口 $\mathcal{W}_s$ 由 $N$ 个微块组成，各微块内的 $M$ 帧共享同一噪声水平，且噪声水平逐块递增（$t_1 < t_2 < \dots < t_N$）。窗口通过滑窗推进，持续输出干净帧，消除分块重叠带来的冗余计算。

- **滑窗训练策略**：训练时模拟推理的流式过程，使模型学习纠正自身预测误差而非仅依赖真值构建的噪声输入。消融实验表明，移除该策略后身份相似度（ID-SIM）从 0.698 暴跌至 0.549，FVD 升至 678.8，出现严重时序崩溃（表 2、图 7），验证了其对于消除曝光偏差和误差累积的关键作用。

- **历史关键帧机制**：基于运动相似度自动选取历史关键帧，将其外观特征作为辅助参考注入当前生成过程，以抑制衣物等无约束区域的时序漂移。运动相似度通过当前帧运动嵌入与历史运动库中所有嵌入的最小 L2 距离判定：

$$d = \min_{i=0,1,\ldots} \| m_f - m_i \|_2$$

移除该机制后，tLP 从 12.83 升至 13.27，可视化结果出现明显的时序漂移（表 2、图 7）。

### 创新点耦合关系

上述三个创新并非孤立存在，而是形成了一条因果链路：混合隐式运动控制提供了富有表现力且鲁棒的运动表示，使去噪过程的结构布局能在极早步骤确定，从而为外观蒸馏的压缩提供了可能性；而蒸馏带来的 4 步高效采样，又为微块流式生成的低延迟实时推理提供了计算基础。三者协同实现了从“高延迟分块离线生成”到“低延迟流式实时生成”的范式跃迁。

## 整体框架

PersonaLive 的完整动画生成流程可形式化为一个自回归流式映射：给定参考图像 $I_R$ 和驱动视频序列 $\{I_D^i\}_{i=1}^{S}$，模型逐帧输出动画帧 $\mathcal{A}_i$：

$$\mathcal{A}_i = \mathcal{D}\big(\mathcal{M}(I_D^i),\; \mathcal{R}(I_R)\big),\quad i=1,2,\dotsc,S$$

其中三个核心模块各司其职：**Motion Extractor ($\mathcal{M}$)** 从驱动帧提取混合运动信号，**Appearance Extractor ($\mathcal{R}$)** 从参考图像提取外观特征，**Denoising Backbone ($\mathcal{D}$)** 以这两类条件为引导完成去噪生成。整个系统通过三阶段训练流水线逐步构建，如图 2 所示。

### 阶段一：图像级混合运动训练

此阶段的目标是让模型学会在单帧层面实现富有表现力且鲁棒的运动控制。核心设计在于**混合隐式运动信号**的引入——同时使用隐式面部表征（implicit facial representations）和 3D 隐式关键点（3D implicit keypoints）。前者负责捕获精细的面部表情动态（如眼睑、嘴角的微妙变化），后者则通过从驱动图像中提取 3D 参数 $\{k_{c,d}, R_d, t_d, s_d\}$ 并施加刚体变换 $k_d = s_d \cdot k_{c,s} R_d + t_d$，实现对全局头部姿态、旋转和缩放的有效控制。这种混合策略使运动控制既具备细节表现力，又对大幅度头部运动保持鲁棒。

外观条件通过 ReferenceNet ($\mathcal{R}$) 注入：该网络与去噪骨干共享相同的预训练 Latent Diffusion U-Net 架构，从参考图像中提取多尺度外观特征，并通过空间注意力机制将其融入去噪过程，从而保持生成人像的身份一致性。

### 阶段二：少步外观蒸馏

该阶段直接针对扩散式人像动画的效率瓶颈。观察发现（图 3），在无分类器引导（CFG）的条件下，第一帧去噪步已基本确定人像的运动和结构布局，后续大量迭代主要用于逐步细化外观细节——这一过程存在显著冗余。基于此洞见，PersonaLive 提出**少步外观蒸馏策略**，将冗余的外观细化过程压缩至极紧凑的采样计划（仅 4 步，时间步为 $[0, 333, 666, 999]$）。

蒸馏训练采用混合损失函数：

$$\mathcal{L}_{distill} = \mathcal{L}_2(\hat{x}, x^{gt}) + \lambda_{lpips}\mathcal{L}_{lpips}(\hat{x}, x^{gt}) + \lambda_{adv}\mathcal{L}_{adv}(\hat{x})$$

其中 MSE 损失保证像素级重建精度，LPIPS 损失维护感知质量，对抗损失则补充高频细节以防止结果过于平滑。为兼顾训练效率，梯度仅在最后一步去噪反向传播，而随机步采样策略确保所有中间时间步在整个训练过程中均获得监督信号。蒸馏完成后，模型无需 CFG 即可在 4 步内生成高质量结果，推理效率大幅提升。

### 阶段三：微块流式视频生成

为实现真正意义上的实时直播，PersonaLive 摒弃了传统分块重叠的批处理范式，转而采用**自回归微块流式生成**架构。在每个去噪步 $s$，系统维护一个去噪窗口 $\mathcal{W}_s = \{C_s^1, C_s^2, \dots, C_s^N\}$，其中每个微块 $C_s^n$ 包含 $M$ 帧，共享同一噪声水平 $t_n$，且噪声水平逐块递增（$t_1 < t_2 < \dots < t_N$）。随着去噪步推进，窗口向前滑动，首个微块在完成全部 $N$ 步去噪后即作为干净帧输出，实现连续流式生成。

为消除自回归范式固有的曝光偏差（exposure bias），系统引入两项关键机制：

- **滑窗训练策略（Sliding Training Strategy）**：训练时模拟推理的流式过程，使模型学习在自身预测的含噪输入（而非真值构建的噪声输入）上进行去噪，从而弥合训练-推理分布差异，防止时序崩溃。
- **历史关键帧机制（Historical Keyframe Mechanism）**：基于运动嵌入的 L2 距离 $d = \min_i \|m_f - m_i\|_2$ 自动选取历史关键帧，将其外观特征作为辅助参考注入当前生成过程，有效抑制衣物、背景等无约束区域的时序漂移。

此外，首个去噪窗口的初始化采用运动插值策略（图 4），通过在驱动运动的起始段进行平滑插值来避免冷启动时的运动突变，保证流式输出从第一帧起即具备时序连贯性。

### 补充图表

![[assets/figures/papers/paper_list_l1076_https_arxiv_org_abs_2512_11253/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the three-stage pipeline of PersonaLive. (a) Image-level hybrid motion training: Learns expressive motion control using implicit facial representations and 3D implicit keypoints. (b) Fewer-step appearance distillation: Eliminates appearance redundancy in the denoising process, improving inference efficiency without compromising visual quality. (c) Micro-chunk streaming video generation: An autoregressive micro-chunk paradigm, equipped with sliding training and historical keyframes, enables low-latency and temporally coherent real-time video generation*

![[assets/figures/papers/paper_list_l1076_https_arxiv_org_abs_2512_11253/figures/001_Figure_1.jpg]]
*Figure 1: An overview of generated portraits and inference speed of PersonaLive. PersonaLive produces high-quality, temporally stable portrait animations over long sequences, while achieving real-time streaming performance with substantially lower latency than prior diffusion-based approaches*

## 核心模块与公式推导

### 3.1 流式动画的形式化定义

PersonaLive 将流式人像动画定义为一个逐帧生成过程。给定参考图像 $I_R$ 和驱动视频序列 $\{I_D^i\}_{i=1}^S$，每一帧动画 $\mathcal{A}_i$ 由去噪骨干网络 $\mathcal{D}$ 根据运动信号和外观特征生成：

$$\mathcal{A}_i = \mathcal{D} ( \mathcal{M} ( I_D^i ) , \mathcal{R} ( I_R ) ), \quad i = 1,2,\dotsc,S$$

其中 $\mathcal{M}$ 为运动提取器，负责从驱动帧中提取混合运动信号；$\mathcal{R}$ 为外观提取器，从参考图像中提取身份与纹理特征。这一形式化将运动控制与外观保持解耦，为后续三阶段流水线奠定了基础。

### 3.2 混合运动控制模块

为实现富有表现力且鲁棒的运动控制，PersonaLive 采用混合隐式信号，同时结合**隐式面部表征**与**3D隐式关键点**。

**隐式面部表征** 用于捕捉精细的面部表情动态（如嘴唇、眼睑的微妙变化），而 **3D隐式关键点** 则负责控制全局头部姿态与缩放。具体而言，通过关键点提取器 $\mathcal{E}_k$ 从驱动图像和源图像中分别提取3D参数：

$$k_{c,d}, R_d, t_d, s_d = \mathcal{E}_k ( I_D ), \quad k_{c,s}, R_s, t_s, s_s = \mathcal{E}_k ( I_R )$$

其中 $k_{c,d}$ 和 $k_{c,s}$ 分别为驱动与源图像的规范关键点坐标，$R$、$t$、$s$ 分别表示旋转矩阵、平移向量和缩放因子。驱动帧的关键点 $k_d$ 通过将源规范关键点变换至驱动姿态得到：

$$k_d = s_d \cdot k_{c,s} R_d + t_d$$

这两类信号在通道维度拼接后作为统一的运动条件输入去噪骨干网络，使得模型能够同时控制局部表情细节和全局头部运动。

### 3.3 少步外观蒸馏模块

核心洞察在于：人像动画的去噪轨迹中，运动与结构布局在最初的去噪步即已基本确定，后续大量迭代主要用于外观细节的逐步细化（见 Figure 3）。基于这一观察，PersonaLive 提出少步外观蒸馏策略，将冗余的外观细化过程压缩为紧凑的采样计划。

![[assets/figures/papers/paper_list_l1076_https_arxiv_org_abs_2512_11253/figures/003_Figure_3.jpg]]
*Figure 3: The denoising trajectory without CFG [16]*

**蒸馏目标** 采用混合损失函数，结合像素级重建、感知相似度和对抗训练：

$$\mathcal{L}_{distill} = \mathcal{L}_2 ( \hat{x}, x^{gt} ) + \lambda_{lpips} \mathcal{L}_{lpips} ( \hat{x}, x^{gt} ) + \lambda_{adv} \mathcal{L}_{adv} ( \hat{x} )$$

其中 $\hat{x}$ 为蒸馏模型的输出，$x^{gt}$ 为真实帧。$\mathcal{L}_2$ 保证像素级保真度，$\mathcal{L}_{lpips}$ 维持感知结构，$\mathcal{L}_{adv}$ 通过对抗损失恢复高频细节，避免结果过于平滑。

**训练策略**上，为降低计算开销，梯度仅通过最后一个去噪步反向传播，同时采用随机步采样确保所有中间时间步均获得监督信号。蒸馏后，模型仅需 $N=4$ 步采样（计划为 $[0, 333, 666, 999]$）且无需无分类器引导（CFG），即可生成高质量结果。

### 3.4 微块流式生成模块

为实现低延迟、时序一致的实时流式生成，PersonaLive 设计了自回归微块流式生成范式。

**去噪窗口** 在第 $s$ 个生成步，维护一个由 $N$ 个微块组成的去噪窗口 $\mathcal{W}_s$：

$$\mathcal{W}_s = \{ C_s^1, C_s^2, \dots, C_s^N \}, \quad C_s^n = \{ z_i^{t_n} \mid i=1..M \}, \quad t_1 < t_2 < \dots < t_N$$

每个微块 $C_s^n$ 包含 $M$ 个连续帧的隐变量，共享同一噪声水平 $t_n$。噪声水平沿微块递增（$t_1$ 为最小噪声，$t_N$ 为最大噪声），形成渐进式去噪结构。窗口每次滑窗推进时，最左侧已完成去噪的微块被输出为干净帧，右侧则纳入新的带噪微块，实现连续流式输出。

**滑窗训练策略** 是防止时序崩溃的核心机制。推理时模型以自回归方式生成，需基于自身先前输出预测后续帧；若训练时仅使用真实帧构造噪声输入，将导致训练-推理不匹配（曝光偏差），误差迅速累积。滑窗训练在训练阶段模拟推理的流式过程，使模型学习纠正自身预测误差。

**历史关键帧机制** 用于抑制长视频中的时序漂移。通过计算当前帧运动嵌入 $m_f$ 与历史运动库中所有嵌入的最小 $L_2$ 距离：

$$d = \min_{i=0,1,\ldots} \| m_f - m_i \|_2$$

当距离超过阈值 $\tau$ 时，当前帧被标记为关键帧，其外观特征被存入历史库并作为辅助参考注入后续生成，从而约束衣物等无运动信号区域的时序一致性。

### 补充图表

![[assets/figures/papers/paper_list_l1076_https_arxiv_org_abs_2512_11253/figures/004_Figure_4.jpg]]
*Figure 4: Motion interpolation for the first denoising window initialization*

![[assets/figures/papers/paper_list_l1076_https_arxiv_org_abs_2512_11253/figures/011_Figure_10.jpg]]
*Figure 10: The implicit 3D keypoints used in our hybrid motion control*

![[assets/figures/papers/paper_list_l1076_https_arxiv_org_abs_2512_11253/figures/012_Figure_11.jpg]]
*Figure 11: Effect of implicit 3D keypoints and facial motion embedding*

## 实验与分析

PersonaLive 在自重演（self-reenactment）、交叉重演（cross-reenactment）和推理效率三个维度上系统评估了其性能，并在消融实验中验证了外观蒸馏与微块流式生成范式中各组件的因果贡献。

### 主实验结果

**定量比较。** 表 1 汇总了 PersonaLive 与代表性基线在 TalkingHead-1KH 自重演和 LV100 交叉重演基准上的结果。在自重演任务中，PersonaLive 的 L1 误差为 0.039，LPIPS 为 0.129，均优于基于 GAN 的帧式方法 **LivePortrait**（L1 0.043，LPIPS 0.137），表明其重建精度更高。在交叉重演任务上，PersonaLive 取得 FVD 520.6 和 tLP 12.83（×10⁻³），优于 LivePortrait（FVD 557.2，tLP 13.51）及所有扩散基线（如 **Megactor-Σ**、**X-Portrait** 等），证明其长视频时序一致性与视觉质量达到最优。

**推理效率。** 所有速度测试在单张 NVIDIA H100 GPU 上进行。PersonaLive 以 15.82 FPS 的帧率和 0.253 s 的延迟实现实时流式生成，比基于扩散的次优方法 Megactor-Σ（2.216 FPS）快约 7 倍，比 X-Portrait（14.10 s 延迟）快约 55 倍，实现了 7–22 倍的加速。扩散基线均未采用分块重叠以模拟流式场景，但牺牲了跨块一致性；PersonaLive 在保持实时性的同时消除了此类冗余。

**定性比较。** 图 5 的定性比较显示，PersonaLive 仅用 4 步去噪即可生成身份保持度高、表情忠实、面部细节清晰的人像动画，视觉质量与需要 20 步以上去噪的扩散方法相当或更优。

### 消融实验

**外观蒸馏策略。** 图 6 和表 2 验证了外观蒸馏的必要性。直接使用 4 步采样而不进行蒸馏（w/o distill）会导致视觉质量严重退化；加入蒸馏但移除对抗损失（w/ distill, w/o GAN）虽能改善重建质量，但输出缺乏高频细节，显得过于平滑。完整蒸馏方案（MSE + LPIPS + 对抗损失）在 4 步采样下实现了与多步扩散相当的视觉保真度。

**滑窗训练策略。** 移除滑窗训练策略（w/o ST）是导致时序崩溃的关键因素。如表 2 所示，身份相似度 ID-SIM 从 0.698 暴跌至 0.549，FVD 从 520.6 升至 678.8。其因果机制在于：模型仅在 GT 构建的噪声输入上训练，推理时自回归生成的误差迅速累积，产生严重的曝光偏差与时间崩溃（图 7）。

**历史关键帧机制。** 移除历史关键帧机制（w/o HKM）后，tLP 从 12.83 升至 13.27，FVD 从 520.6 升至 541.5。图 7 显示，无 HKM 时衣物等无约束区域出现明显时序漂移，因为模型缺乏长期外观参考来抑制累积误差。

**微块大小。** 将微块大小从 4 减为 2 时，tLP 从 12.83 降至 12.14（时序一致性略微提升），但 ID-SIM 从 0.698 降至 0.660。这是因为时间感受野变小，模型难以充分捕捉身份相关的外观信息，体现了时序一致性与身份保持之间的权衡。

**运动阈值 τ。** 表 3 的消融表明，HKM 中的运动阈值 τ = 17 在 ID-SIM 与 tLP 之间取得最佳平衡。过小的 τ 会频繁触发关键帧更新，引入噪声外观；过大的 τ 则使关键帧更新滞后，削弱对时序漂移的抑制。

**VAE 解码器。** 表 4 的消融显示，使用时序 VAE 解码器可进一步降低 tLP，增强帧间连贯性。

### 失败模式与局限性

图 8 展示了域外肖像的失败案例。当参考图像超出训练域（如卡通角色或动物）时，模型会产生模糊或畸形的眼睛与嘴巴。这是因为混合运动信号和外观蒸馏均在真人面部数据上训练，缺乏对非真人面部结构的泛化能力。此外，当前框架未显式利用连续帧间的时间冗余，未来可进一步压缩推理延迟或支持更长的去噪窗口。

### 补充图表

![[assets/figures/papers/paper_list_l1076_https_arxiv_org_abs_2512_11253/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparisons. Numbers in red and blue indicate the best and the second-best results, respectively. tLP multiplied by 10−3. All speed measurements are conducted on a single NVIDIA H100 GPU. * LivePortrait [11] is a frame-wise method using GAN. While it runs significantly faster than diffusion-based approaches, its generated portraits often lack fine-grained details*

![[assets/figures/papers/paper_list_l1076_https_arxiv_org_abs_2512_11253/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparisons. PersonaLive achieves high-quality portrait animation using significantly fewer denoising steps, while preserving identity, expression fidelity, and facial detail*

![[assets/figures/papers/paper_list_l1076_https_arxiv_org_abs_2512_11253/figures/007_Figure_6.jpg]]
*Figure 6: Ablation on appearance distillation strategy. All results are generated using 4 denoising steps without the CFG technique*

![[assets/figures/papers/paper_list_l1076_https_arxiv_org_abs_2512_11253/figures/009_Table_2.jpg]]
*Table 2: Ablation study on micro-chunk streaming generation*

![[assets/figures/papers/paper_list_l1076_https_arxiv_org_abs_2512_11253/figures/010_Figure_7.jpg]]
*Figure 7: Ablation study on the core components of the microchunk streaming generation paradigm*

![[assets/figures/papers/paper_list_l1076_https_arxiv_org_abs_2512_11253/figures/008_Figure_8.jpg]]
*Figure 8: Failure cases. Some details of our method may fail when the given reference images are out of the training domain*

## 方法谱系与知识库定位

### 与现有工作的关系

PersonaLive 处于**扩散式人像动画**与**实时流式生成**的交汇点，其核心贡献在于将扩散模型的生成质量推向直播场景所需的低延迟约束。与现有工作的关系可从三个维度定位。

**相对于基于GAN的帧式方法。** **LivePortrait** (2024) 是该范式的典型代表，通过GAN直接回归单帧人像，推理速度极快，但生成结果缺乏细粒度细节。PersonaLive 在交叉重演场景下以 FVD 520.6 和 tLP 12.83 优于 LivePortrait 的 557.2 和 13.51（Table 1），表明扩散式生成在时序一致性和视觉保真度上具有优势，但速度差距仍存在——LivePortrait 作为帧式GAN方法天然更快，PersonaLive 的目标并非超越GAN的速度极限，而是在扩散范式内逼近实时。

**相对于扩散式人像动画方法。** 现有扩散基线包括 **X-Portrait** (Xie et al., SIGGRAPH 2024)、**Follow-your-Emoji** (2024)、**Megactor-Σ** (Yang et al., AAAI 2025)、**X-NeMo** (Zhao et al., ICLR 2025) 和 **HunyuanPortrait** (Xu et al., CVPR 2025)。这些方法的共同瓶颈在于：去噪步数通常≥20步，且长视频生成依赖分块重叠处理，导致推理延迟高和跨块误差累积。PersonaLive 通过外观蒸馏将采样压缩至4步，并采用自回归微块流式范式消除分块冗余，在单张H100 GPU上达到15.82 FPS、延迟0.253s，相比扩散基线中速度次优的 Megactor-Σ（2.216 FPS）提速约7倍，相比 X-Portrait 延迟降低约55倍（Table 1）。在质量指标上，PersonaLive 的 FVD 和 tLP 均优于所有扩散基线，验证了“少步采样+蒸馏”策略在不牺牲质量的前提下实现效率突破。

**运动控制信号的演进。** 早期方法依赖2D关键点或驱动视频帧作为运动条件，对头部姿态和微表情的解耦控制不足。PersonaLive 引入混合隐式信号——隐式面部表征用于细节表情，3D隐式关键点用于全局头部姿态与缩放——这一设计借鉴了 **X-NeMo** 的隐式面部表征和 **LivePortrait** 的3D关键点思路，但将二者融合为统一的运动控制框架，实现了更富表现力的动画生成。

### 适用边界

PersonaLive 的有效性建立在以下前提之上：

- **训练数据域限制。** 模型主要在真人面部数据集（VFHQ、NerSemble、DH-FaceVid-1K）上训练，对域外肖像（如卡通角色、动物）泛化能力不足，会产生模糊或畸形的眼睛与嘴巴（Figure 8）。这是当前扩散式人像动画方法的共性局限。
- **实时性依赖于固定微块大小。** 默认微块大小 M=4，在H100 GPU上实现实时性能。若硬件条件变化或需要更长的时序感受野，需重新权衡速度与质量。
- **未显式利用帧间时间冗余。** 当前框架对各帧独立去噪，未建模连续帧间的运动连续性或外观共享，存在进一步压缩计算的空间。

### 局限与开放问题

**已知局限。** 除域外泛化问题外，论文明确指出的局限包括：自回归微块范式未显式利用连续帧间的时间冗余，限制了推理效率的进一步提升或更长去噪窗口的使用。

**开放问题。** 从该方法出发，可延伸出以下研究问题：

1. **如何显式利用帧间时间冗余？** 连续帧在运动轨迹和外观上高度相关，引入时序条件或运动预测模块可能进一步减少每帧所需的去噪步数或噪声水平。
2. **如何提升域外肖像的泛化能力？** 当前失败案例集中在非真人面部，可能需要域适应策略或更大规模的多样化训练数据。
3. **少步蒸馏的极限在哪里？** 4步采样已取得显著加速，能否进一步压缩至2步甚至1步？这需要在蒸馏损失设计和对抗训练策略上进行更深入的探索。
4. **滑窗训练策略的通用性。** 该策略通过模拟推理时的自回归误差积累来缓解曝光偏差，这一思路是否适用于其他自回归生成任务（如文本到视频、音频生成）值得验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/PersonaLive_Expressive_Portrait_Image_Animation_for_Live_Streaming.pdf]]