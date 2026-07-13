---
title: "MotionCtrl: A Unified and Flexible Motion Controller for Video Generation"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation.pdf
project_link: https://wzhouxiff.github.io/projects/MotionCtrl/
code_link: https://github.com/TencentARC/MotionCtrl
aliases:
- MotionCtrl
tags:
- SIGGRAPH_2024
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将相机姿态序列（RT）集成到视频扩散模型的时序 Transformer 中控制全局相机运动，将物体稀疏轨迹（Trajs）的多尺度特征集成到卷积层中控制局部物体运动，两者解耦并独立作用于生成过程。"
primary_logic: "相机运动本质是跨帧的全局场景变换，适合与时序注意力机制结合；物体运动是局部区域的空间位置变化，适合与空间卷积层结合。利用这一特性设计的 Camera Motion Control Module (CMCM) 和 Object Motion Control Module (OMCM) 可以实现精细且灵活的运动解耦控制。"
claims:
- "CMCM 集成到 LVDM 的时序 Transformer 中，Camera Motion Control (CamMC) 误差从 0.9010 降至 0.0289，显著优于集成到空间模块或时间嵌入的方案。"
- "OMCM 先使用密集轨迹预训练，再使用稀疏轨迹微调，Object Motion Control (ObjMC) 误差为 25.1198，优于仅用密集或稀疏轨迹训练。"
- "Camera Motion Control (Basic Poses) 上 CamMC ↓ = 0.0289"
- "Camera Motion Control (Complex Poses) 上 CamMC ↓ = 0.0735"
---

# MotionCtrl: A Unified and Flexible Motion Controller for Video Generation

> [!tip] 核心洞察
> 相机运动本质是跨帧的全局场景变换，适合与时序注意力机制结合；物体运动是局部区域的空间位置变化，适合与空间卷积层结合。利用这一特性设计的 Camera Motion Control Module (CMCM) 和 Object Motion Control Module (OMCM) 可以实现精细且灵活的运动解耦控制。

| 字段      | 内容                                                                                                                                                     |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 中文题名    | MotionCtrl：统一且灵活的视频生成运动控制器                                                                                                                             |
| 英文题名    | MotionCtrl: A Unified and Flexible Motion Controller for Video Generation                                                                              |
| 会议/期刊   | SIGGRAPH 2024                                                                                                                                          |
| Links   | [paper](https://arxiv.org/abs/2312.03641) · [project](https://wzhouxiff.github.io/projects/MotionCtrl/) · [code](https://github.com/TencentARC/MotionCtrl) |
| Topic   | #SIGGRAPH_2024 #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl                                     |
| Method  | MotionCtrl                                                                                                                                             |
| Dataset | Camera Motion Control (Basic Poses), Camera Motion Control (Complex Poses), Object Motion Control, Video Quality (FVD)                                 |

> [!tip] 效果简介
> - Camera Motion Control (Basic Poses) 上，CamMC ↓ 为 0.0289，对比 0.0548 (AnimateDiff)，变化 -0.0259。
> - Camera Motion Control (Complex Poses) 上，CamMC ↓ 为 0.0735，对比 0.0950 (VideoComposer)，变化 -0.0215。
> - Object Motion Control 上，ObjMC ↓ 为 28.877，对比 36.8351 (VideoComposer)，变化 -7.9581。

## 概要

视频生成领域长期面临一个核心瓶颈：**现有方法无法明确区分并独立控制全局相机运动与局部物体运动**。相机运动表现为跨帧的整体场景变换，而物体运动则是局部区域的空间位移，二者的物理本质截然不同，但以往工作（如 **AnimateDiff** (Guo et al., 2023) 使用多个独立 LoRA 控制基本相机运动，**VideoComposer** (Wang et al., 2023) 使用密集运动向量统一处理）均未实现有效的解耦控制，导致运动控制的粒度不足，难以灵活组合。

针对这一问题，**MotionCtrl** 提出了一个统一且灵活的运动控制器，其核心洞察在于：相机运动天然适合与时序注意力机制结合，而物体运动则适合与空间卷积层结合。基于这一认识，MotionCtrl 设计了两个独立模块：
- **Camera Motion Control Module (CMCM)**：将相机姿态序列集成到基础视频扩散模型 **LVDM** (He et al., 2022) 的时序 Transformer 中，控制全局相机运动；
- **Object Motion Control Module (OMCM)**：将物体稀疏轨迹的多尺度特征集成到 LVDM 的卷积层中，控制局部物体运动。

为克服单一数据集缺乏完整标注（文本描述、相机姿态、物体轨迹）的困难，MotionCtrl 采用多步训练策略：在 RealEstate10K 上训练 CMCM，在 WebVid 上以密集轨迹预训练、稀疏轨迹微调 OMCM。实验表明，MotionCtrl 在相机运动控制（CamMC 误差从 0.9010 降至 0.0289）和物体运动控制（ObjMC 误差 28.877，优于 VideoComposer 的 36.8351）上均显著优于现有方法，同时保持与原始 LVDM 相当的视频生成质量（FVD 852.15 vs. 1004.99）。用户研究进一步确认，超过 90% 的参与者在质量、文本相似度和运动相似度上偏好 MotionCtrl。

视频生成领域近年来取得了显著进展，以扩散模型为基础的生成框架（如 LVDM/VideoCrafter1，He et al., 2022）已能产出时序连贯的视频内容。然而，对生成视频的运动进行精细控制仍然是一个核心瓶颈。现有工作要么将运动控制视为一个整体问题，要么仅关注某一种运动维度，导致控制粒度不足。

**核心瓶颈在于：全局相机运动与局部物体运动未能被明确区分和独立控制。** 相机运动（camera motion）是场景整体在时间维度上的全局变换，通常由相机姿态序列（旋转矩阵 R 与平移向量 T）描述；物体运动（object motion）则是前景元素在空间位置上的局部变化，可由像素轨迹（trajectories）刻画。两者在物理成因、表现形态和可控维度上截然不同，但现有方法往往将其混为一谈。

具体而言，当前方法的缺口体现在三个层面：

1. **控制机制的耦合**：**AnimateDiff**（Guo et al., 2023）使用多个独立的 LoRA 模型分别控制不同方向的基本相机运动（如平移、缩放），但无法处理复杂相机姿态，且完全不具备物体运动控制能力。**VideoComposer**（Wang et al., 2023）从参考视频中提取密集运动向量（motion vector）来统一控制视频运动，但该向量同时包含相机和物体运动信息，无法解耦控制，导致在复杂场景下运动精度下降（如 Figure 4(b) 所示，VideoComposer 在复杂相机姿态下生成的物体外观出现失真）。

2. **控制信号与模型架构的错配**：相机运动本质是跨帧的全局场景变换，适合与时序注意力机制（temporal attention）结合；物体运动是局部区域的空间位置变化，适合与空间卷积层（spatial convolution）结合。现有方法未利用这一特性进行针对性设计，导致控制信号无法有效驱动生成过程。

3. **训练数据的缺失**：目前不存在同时包含文本描述、相机姿态标注和物体运动轨迹标注的完整数据集。这迫使方法必须在数据层面做出妥协——要么牺牲某种运动控制能力，要么采用不精确的代理信号。

上述缺口共同构成了一个清晰的研究动机：**设计一个统一且灵活的运动控制器，能够在一个模型中解耦并独立控制相机运动与物体运动，同时克服数据缺失带来的训练挑战。** 这正是 MotionCtrl 的核心目标。

## 核心方法与创新机理

MotionCtrl 的核心创新在于将视频生成中的运动控制解耦为两个正交维度——**全局相机运动**与**局部物体运动**——并针对各自运动属性的本质差异，设计了结构上相互独立、功能上可灵活组合的控制模块。

### 问题瓶颈与因果机制

现有视频生成方法（如 **VideoComposer** (Wang et al., 2023)、**DragNUWA** 等）通常将相机运动与物体运动混为一谈，采用统一的运动向量或光流轨迹进行控制。这种耦合策略导致两大问题：其一，无法独立调整相机运镜或物体运动轨迹，控制粒度不足；其二，全局场景变换与局部区域位移在物理属性上存在根本差异——相机运动是跨帧的全局场景变换，物体运动是局部区域的空间位置变化——统一建模难以同时兼顾两者的精度。

MotionCtrl 的因果调控旋钮在于：**将相机运动与时序注意力机制绑定，将物体运动与空间卷积层绑定**。这一设计并非简单的工程技巧，而是基于对运动属性本质的洞察——时序 Transformer 天然适合捕获跨帧的全局变换关系，而空间卷积层天然适合提取局部区域的特征位移。

### 相机运动控制模块 (CMCM)：时序集成替代独立模型

**Baseline 方案**：**AnimateDiff** (Guo et al., 2023) 使用多个独立的 LoRA 模型分别控制不同方向的基本相机运动（如左移、右移、缩放），每个运动方向需训练一个专用模型，无法在单一模型中实现连续可变的相机运动控制，更难以处理复杂姿态序列。

**MotionCtrl 方案**：CMCM 将相机姿态序列（3×3 旋转矩阵 + 3×1 平移向量）作为输入，通过轻量 MLP 提取特征后，附加到 LVDM 时序 Transformer 的**第二自注意力模块**中。这一集成位置经过严格消融验证（Table 2）：集成到时序 Transformer 时 CamMC 误差为 0.0289，而集成到时间嵌入、空间交叉注意力或空间自注意力模块时，CamMC 误差高达 0.9010——差距超过 30 倍，充分证明时序注意力是相机运动控制的最优信息注入点。

CMCM 的关键优势在于：单个统一模型即可控制从基本姿态（8 种）到复杂姿态（20 种）的全谱系相机运动，且支持用户调节运动速度，无需为每种运动方向训练独立模型。

### 物体运动控制模块 (OMCM)：稀疏轨迹与多尺度卷积

**Baseline 方案**：**VideoComposer** 使用密集运动向量控制物体运动，但无法区分前景物体运动与背景相机运动，导致物体运动控制精度不足（ObjMC 为 36.8351）；**DragNUWA** 使用光流轨迹，同样无法区分前景与背景。

**MotionCtrl 方案**：OMCM 使用物体运动轨迹（表示为帧间相对位移 $u_{(x_i,y_i)} = x_i - x_{i-1}$，$v_{(x_i,y_i)} = y_i - y_{i-1}$），通过多尺度卷积与下采样提取特征，并**仅添加到 LVDM 编码器的卷积层**中。这一空间注入策略确保了物体运动控制不影响相机运动模块，实现真正的解耦。

OMCM 的另一关键创新在于**训练策略**：先使用 **ParticleSfM** 从 WebVid 视频中合成密集轨迹进行预训练，再使用稀疏轨迹（用户实际输入的轨迹形式）进行微调。消融实验（Table 3）表明，这种"密集预训练 + 稀疏微调"策略使 ObjMC 降至 25.1198，显著优于仅使用密集轨迹（28.877）或仅使用稀疏轨迹（29.6548）训练。密集轨迹预训练为模型提供了丰富的运动先验，稀疏轨迹微调则使模型适应实际推理时的稀疏输入分布，两者协同实现了对稀疏轨迹的精准跟随。

### 多步训练策略：解耦训练的工程突破

由于不存在同时包含文本描述、相机姿态和物体运动轨迹的完整标注数据集，MotionCtrl 设计了多步训练策略：先在 **RealEstate10K**（经 BLIP-2 生成文本描述）上训练 CMCM，再在 **WebVid**（经 ParticleSfM 合成轨迹）上训练 OMCM。训练 OMCM 时，LVDM 和 CMCM 均被冻结。消融实验（Section 4.3.3）表明，这种"先 CMCM 后 OMCM"的顺序训练比同时训练或反向顺序训练更能保持生成质量和运动控制精度，验证了模块间解耦训练的必要性。

### 创新总结

MotionCtrl 的三项核心 changed slots 构成一个完整的创新体系：**CMCM 的时序集成位置**解决了相机运动的全局控制问题，**OMCM 的空间集成位置与稀疏轨迹训练策略**解决了物体运动的局部控制问题，**多步解耦训练策略**解决了数据缺失下的模型训练问题。三者共同实现了统一模型内相机运动与物体运动的独立、灵活、精准控制。

![[assets/figures/papers/paper_list_l28_MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation/figures/002_Figure_2.jpg]]
*Figure 2: MotionCtrl Framework. MotionCtrl extends the Denoising U-Net structure of LVDM with a Camera Motion Control Module (CMCM) and an Object Motion Control Module (OMCM). As illustrated in (b), the CMCM integrates camera pose sequences 𝑅𝑇 with LVDM’s temporal transformers by appending 𝑅𝑇 to the input of the second self-attention module and applying a tailored and lightweight fully connected layer to extract the camera pose feature for subsequent processing. The OMCM utilizes convolutional layers and downsamplings to derive multi-scale features from T r a j s , which are spatially incorporated into LVDM’s convolutional layers to direct object motion. Further given a text prompt, LVDM generates vi...*

MotionCtrl 在冻结的底层视频扩散模型 **LVDM (VideoCrafter1)**（He et al., 2022）之上，通过插入两个解耦的适配模块来实现对生成视频中运动的精细化控制。其核心设计理念源于对两种运动本质差异的洞察：**相机运动是跨帧的全局场景变换**，适合与时序注意力机制结合；**物体运动是局部区域的空间位置变化**，适合与空间卷积层结合。基于这一因果机制，MotionCtrl 分别设计了 Camera Motion Control Module (CMCM) 和 Object Motion Control Module (OMCM)，两者独立作用于 LVDM 降噪 U-Net 的不同组件，最终实现统一模型下的灵活运动解耦控制。

### 输入与输出

MotionCtrl 接受三类输入：
- **文本提示**（text prompt），用于描述视频的语义内容；
- **相机姿态序列** $RT = \{RT_1, RT_2, \dots, RT_L\}$，其中每个 $RT_i$ 包含一个 $3 \times 3$ 旋转矩阵和一个 $3 \times 1$ 平移向量，用于控制全局相机运动；
- **物体运动轨迹** $Trajs = \{T_1, T_2, \dots, T_n\}$，其中每条轨迹 $T_j$ 由一系列帧间相对位移 $(u, v)$ 表示，用于控制局部物体运动。

输出为一段与输入条件对齐的生成视频。

### 模块关系与数据流

MotionCtrl 的整体 pipeline 如 Figure 2 所示，两个控制模块以“即插即用”的方式集成到 LVDM 的降噪 U-Net 中：

1. **Camera Motion Control Module (CMCM)**：
   - 将相机姿态序列 $RT$ 通过一个轻量级 MLP 提取特征；
   - 将提取的特征附加到 LVDM 时序 Transformer 的**第二自注意力模块**的输入中；
   - 仅新增少量 MLP 层和时序 Transformer 的第二自注意力模块参与训练，其余 LVDM 参数冻结。

2. **Object Motion Control Module (OMCM)**：
   - 将物体运动轨迹 $Trajs$ 表示为帧间相对位移（见公式 $u_{(x_i, y_i)} = x_i - x_{i-1}; v_{(x_i, y_i)} = y_i - y_{i-1}$），以显式捕捉运动速度；
   - 通过多个卷积层结合下采样操作提取多尺度空间特征；
   - 将多尺度特征对应添加到 LVDM 编码器的**卷积层**输入中。

两个模块的输出在 LVDM 的降噪过程中分别作用于时序维度和空间维度，互不干扰，从而实现对相机运动和物体运动的独立控制。

### 训练策略

由于缺乏同时包含文本描述、相机姿态和物体运动轨迹完整标注的单一数据集，MotionCtrl 采用多步训练策略：

1. **CMCM 训练**：在 RealEstate10K 数据集（经 Blip2 生成文本描述）上训练 CMCM，冻结 LVDM 其余部分，约 50,000 次迭代收敛。
2. **OMCM 训练**：在 WebVid 数据集上，先使用 ParticleSfM 合成的密集轨迹预训练 OMCM（20,000 次迭代），再使用稀疏轨迹微调（20,000 次迭代）。此阶段 LVDM 和 CMCM 均保持冻结。
3. 训练顺序固定为“先 CMCM 后 OMCM”，消融实验表明该顺序优于同时训练或反向顺序，能够更好地保持生成质量和运动控制精度（见 Section 4.3.3）。

### 关键设计决策

- **CMCM 集成位置**：消融实验（Table 2）证实，将 CMCM 集成到 LVDM 的时序 Transformer 中，相机运动控制误差 CamMC 从 0.9010 降至 0.0289，显著优于集成到时间嵌入、空间交叉注意力或空间自注意力模块的方案。
- **OMCM 训练方式**：先密集轨迹预训练、再稀疏轨迹微调的策略，使得物体运动控制误差 ObjMC 达到 25.1198，优于仅使用密集或稀疏轨迹训练（Table 3），且能泛化至推理时仅提供稀疏轨迹的场景。
- **轨迹表示**：采用帧间相对位移而非绝对坐标，使 OMCM 能够显式感知运动速度，提升对稀疏轨迹的跟随精度。

MotionCtrl 的核心设计在于将相机运动与物体运动解耦，并通过两个独立模块分别作用于视频扩散模型的不同组件。其底层生成模型为 **LVDM**（He et al., 2022），MotionCtrl 在冻结的 LVDM 降噪 U-Net 上插入适配模块，仅训练新增参数。

### 基础扩散模型

LVDM 采用标准的噪声预测范式。给定初始潜变量 $z_0$ 和条件 $c$（如文本提示），训练目标是最小化预测噪声与真实噪声的差异：

$$
\mathcal { L } = \mathbb { E } _ { z _ { 0 } , c , \epsilon \sim \mathcal { N } ( 0 , I ) , t } \left[ \| \epsilon - \epsilon _ { \theta } ( z _ { t } , t , c ) \| _ { 2 } ^ { 2 } \right]
$$

其中含噪潜变量 $z_t$ 通过前向扩散过程获得：

$$
z _ { t } = \sqrt { \bar { \alpha _ { t } } } z _ { 0 } + \sqrt { 1 - \bar { \alpha _ { t } } } \epsilon , \quad \bar { \alpha _ { t } } = \prod _ { i = 1 } ^ { t } \alpha _ { t }
$$

$\alpha_t$ 为噪声调度系数，$\epsilon_\theta$ 为降噪 U-Net 预测的噪声。

### Camera Motion Control Module (CMCM)

**设计原理**：相机运动本质是跨帧的全局场景变换，具有时序一致性。因此 CMCM 被集成到 LVDM 的**时序 Transformer** 中，而非空间模块。

**输入表示**：相机姿态序列 $RT$，由 $3 \times 3$ 旋转矩阵和 $3 \times 1$ 平移向量组成，描述每帧的全局相机运动。

**集成方式**：CMCM 将相机姿态序列 $RT$ 附加到 LVDM 时序 Transformer 的**第二个自注意力模块**的输入中，通过一个轻量级全连接层（MLP）提取相机运动特征。该设计使相机运动信息能沿着时序维度传播，影响所有帧的全局变换。

**训练策略**：CMCM 采用类似适配器（adapter）的训练方式——仅训练新增的 MLP 层和时序 Transformer 的第二个自注意力模块，其余 LVDM 参数冻结。训练数据为 **RealEstate10K** 数据集（经 Blip2 生成文本描述），该数据集提供真实的相机姿态标注。

### Object Motion Control Module (OMCM)

**设计原理**：物体运动是局部区域的空间位置变化，因此 OMCM 被集成到 LVDM 编码器的**卷积层**中，通过空间特征注入实现精准的局部控制。

**轨迹表示**：物体运动轨迹表示为相邻帧之间的相对位移，以显式捕捉运动速度：

$$
u _ { ( x _ { i } , y _ { i } ) } = x _ { i } - x _ { i - 1 } ; \quad v _ { ( x _ { i } , y _ { i } ) } = y _ { i } - y _ { i - 1 } ; \quad 0 < i < L
$$

其中 $(x_i, y_i)$ 为第 $i$ 帧的轨迹点坐标，$L$ 为视频帧数。这种相对位移表示使模型能直接感知物体的运动方向和速度。

**集成方式**：OMCM 由多个卷积层与下采样操作组成，从轨迹 $Trajs$ 中提取多尺度空间特征，并对应地添加到 LVDM 编码器的各卷积层输入中。这种多尺度注入确保了物体运动信息在不同空间分辨率下都能影响生成过程。

**训练策略**：由于缺乏同时包含文本描述和物体轨迹标注的数据集，OMCM 采用两阶段训练：
1. **密集轨迹预训练**：使用 **ParticleSfM**（Zhao et al., 2022）从 WebVid 视频中提取密集物体运动轨迹，先以密集轨迹训练 OMCM（约 20,000 次迭代）。
2. **稀疏轨迹微调**：从密集轨迹中随机采样 $n \in [1, N]$ 条轨迹（$N=8$），经高斯滤波平滑后，对 OMCM 进行微调（约 20,000 次迭代）。

该策略使 OMCM 在推理时仅需用户提供一条或几条稀疏轨迹即可实现精准控制，同时保持生成质量。

### 训练流程

MotionCtrl 采用**多步训练策略**：
1. 先训练 CMCM（约 50,000 次迭代），此时 LVDM 冻结，仅更新 CMCM 参数。
2. 再训练 OMCM，此时 LVDM 和 CMCM 均冻结，仅更新 OMCM 参数。

消融实验表明，先 CMCM 后 OMCM 的顺序训练比同时训练或反向顺序训练更能保持生成质量和运动控制精度（Section 4.3.3）。

## 实验与关键发现

### 核心瓶颈与评估逻辑

MotionCtrl 的核心目标是解耦并独立控制视频生成中的全局相机运动与局部物体运动。因此，实验评估围绕两个关键问题展开：(1) 生成的相机运动是否精确跟随输入的姿态序列；(2) 生成的物体运动是否精确跟随输入的稀疏轨迹。评估指标包括 **CamMC**（相机运动控制误差，预测与真值相机姿态间的欧氏距离）和 **ObjMC**（物体运动控制误差，预测与真值轨迹点间的欧氏距离），两者均为越低越好。视频质量由 **FVD** 和 **FID** 衡量，文本对齐度由 **CLIPSIM** 衡量。

### 主结果：运动控制精度与视频质量

MotionCtrl 在相机运动控制和物体运动控制上均显著优于现有方法，同时保持了与底层生成模型 LVDM 相当的视频质量。

**相机运动控制。** 在基本姿态（8 种）上，MotionCtrl 的 CamMC 达到 0.0289，远低于 AnimateDiff 的 0.0548（Table 1）。在复杂姿态（20 种）上，MotionCtrl 的 CamMC 为 0.0735，优于 VideoComposer 的 0.0950。跨数据集泛化实验进一步验证了这一优势：在 RealEstate10K、WebVid 和 HD-VILA 三个来源的复杂姿态上，MotionCtrl 的 CamMC 分别为 0.0840、0.0589 和 0.0499，均低于 VideoComposer 的对应值（Table 4）。这表明 CMCM 通过时序 Transformer 集成相机姿态的策略具有跨数据分布的鲁棒性。

![[assets/figures/papers/paper_list_l28_MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation/figures/007_Table_1.jpg]]
*Table 1: Quantitative Comparisons with AnimateDi [Guo et al. 2023] and VideoComposer [Wang et al. 2023]. Our MotionCtrl outperforms competing approaches in both camera and object motion control while also excelling at preserving text similarity and the quality of the video generation*

![[assets/figures/papers/paper_list_l28_MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation/figures/016_Table_4.jpg]]
*Table 4: Quantitative Comparisons with VideoComposer [Wang et al. 2023]. Our MotionCtrl performs better in all three sets of relatively complex camera poses from RealEstate10K [Zhou et al. 2018], WebVid [Bain et al. 2021], and HD-VILA [Xue et al. 2022]*

**物体运动控制。** MotionCtrl 的 ObjMC 为 28.877，显著低于 VideoComposer 的 36.8351（Table 1）。定性结果（Figure 5）显示，两者虽都能让物体沿给定轨迹移动，但 MotionCtrl 在逐帧轨迹跟随精度上明显更高。

**视频质量与文本对齐。** MotionCtrl 的 FVD 为 852.15，优于 VideoComposer 的 1004.99；CLIPSIM 为 0.2319，略高于 VideoComposer 的 0.2214（Table 1）。这说明运动控制模块的加入并未损害底层模型的生成能力。

**用户研究。** 34 名参与者在视频质量、文本相似度、运动相似度和总体偏好四个维度上，超过 90% 的选择偏向 MotionCtrl 而非 VideoComposer（Table 5），验证了定量指标的生态效度。

### 消融实验：因果机制的验证

消融实验直接验证了论文的核心因果假设——相机运动应与时序注意力结合，物体运动应与空间卷积结合。

**CMCM 集成位置。** Table 2 对比了将 CMCM 集成到 LVDM 不同模块的效果。集成到**时序 Transformer** 的 CamMC 为 0.0289，而集成到时间嵌入、空间交叉注意力或空间自注意力模块的 CamMC 分别高达 0.9010、0.7766 和 0.8381。这一巨大差距证实了相机运动本质上是跨帧的全局变换，与时序注意力机制的归纳偏置高度匹配。同时，时序 Transformer 集成方案保持了与原始 LVDM 相当的 FID（25.36 vs 25.02）和 FVD（346.43 vs 341.80），说明该方案几乎不损害生成质量。

![[assets/figures/papers/paper_list_l28_MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation/figures/006_Table_2.jpg]]
*Table 2: Ablation of Camera Motion Control. Our Camera Motion Control Module (CMCM), incorporated with the temporal transformers of LVDM [He et al. 2022], e ectively controls camera motion and maintains LVDM’s video quality*

**OMCM 训练策略。** Table 3 对比了三种训练方式：仅密集轨迹、仅稀疏轨迹、先密集后稀疏微调。先密集预训练再稀疏微调的 ObjMC 为 25.1198，优于仅密集（29.2627）和仅稀疏（28.877）训练。这一结果揭示了因果机制：密集轨迹预训练使 OMCM 学到丰富的局部运动表征，稀疏轨迹微调则使其适应推理时的稀疏输入分布，两者结合实现了从密集监督到稀疏推理的有效泛化。

![[assets/figures/papers/paper_list_l28_MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation/figures/008_Table_3.jpg]]
*Table 3: Ablation of Object Motion Control. The Object Motion Control Module (OMCM), when initially trained on dense object movement trajectories and subsequently finetuned with sparse trajectories, outperforms versions trained exclusively on either dense or sparse trajectories. trajectories allows OMCM to adjust to the sparsity encountered during inference*

**多步训练顺序。** 论文还验证了训练顺序的影响：先训练 CMCM 再训练 OMCM 的多步策略，相比同时训练或反向顺序，能更好地保持两类运动控制的精度（Section 4.3.3）。这是因为 CMCM 控制全局场景变换，其训练应当先于局部物体运动模块，以避免两类运动信号在训练早期相互干扰。

### 失败模式与局限

尽管 MotionCtrl 在独立控制上表现优异，论文明确指出以下局限：

1. **联合控制的协调精度不足。** 同时控制相机运动和物体运动时，两种运动在生成视频中的精确协调仍有改进空间。这是解耦控制架构的固有挑战：两个模块独立作用于生成过程，缺乏显式的跨模块协调机制。

2. **稀疏轨迹的表达能力有限。** 目前仅支持用户提供一条或几条稀疏轨迹，对于需要精细控制多物体复杂交互的场景，交互方式不够丰富。

3. **轨迹提取的计算开销。** OMCN 训练依赖 ParticleSfM 从视频中提取密集轨迹，该过程计算成本较高，可能限制方法向更大规模数据集的扩展。

### 重要图表结论摘要

- **Table 1**：MotionCtrl 在 CamMC、ObjMC、FVD、CLIPSIM 四项指标上全面优于 AnimateDiff 和 VideoComposer，验证了统一解耦控制的有效性。
- **Table 2**：CMCM 集成到时序 Transformer 是相机运动控制的关键设计选择，CamMC 从 0.9010 降至 0.0289。
- **Table 3**：密集预训练 + 稀疏微调是物体运动控制的最优训练策略，ObjMC 达到 25.1198。
- **Table 4**：跨数据集泛化实验证明 MotionCtrl 的相机运动控制在多源数据上一致优于 VideoComposer。
- **Figure 5**：定性展示 MotionCtrl 在逐帧轨迹跟随精度上显著优于 VideoComposer，特别是在轨迹拐点处。

![[assets/figures/papers/paper_list_l28_MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative Comparisons on Camera Motion Control. (a) Basic Poses: MotionCtrl and AnimateDi [Guo et al. 2023] e ectively execute zooms, but MotionCtrl can adjust to varying camera moving speeds. (b) Relatively Complex Poses: Video-Composer[Wang et al. 2023] uses Realestate10K’s raw video for motion vectors, capturing unintended shapes like doors, leading to unnatural results (refer to frame 12). MotionCtrl, however, produces a relatively natural video with motion that closely matches the camera poses*

## 定位与知识库关联

### 与基线方法的关系

MotionCtrl 的核心贡献在于首次在统一模型中实现了相机运动与物体运动的解耦控制。其设计思路直接回应了此前工作的关键瓶颈：

- **相对于 AnimateDiff**（Guo et al., 2023）：AnimateDiff 通过为不同相机运动方向训练独立的 LoRA 模型来实现基本相机运动控制，但无法处理复杂相机姿态，且完全不涉及物体运动。MotionCtrl 的 CMCM 以统一的相机姿态序列（3×3 旋转矩阵 + 3×1 平移向量）作为输入，单个模型即可覆盖 8 种基本姿态和 20 种复杂姿态，且支持运动速度调节。定量上，在基本姿态的 CamMC 指标上，MotionCtrl 达到 0.0289，优于 AnimateDiff 的 0.0548（Table 1）。

- **相对于 VideoComposer**（Wang et al., 2023）：VideoComposer 使用从参考视频提取的密集运动向量（motion vector）统一控制视频运动，但不区分相机运动与物体运动，导致两种运动相互耦合。MotionCtrl 通过 CMCM 和 OMCM 的结构性解耦，在复杂相机姿态控制（CamMC: 0.0735 vs 0.0950）和物体运动控制（ObjMC: 28.877 vs 36.8351）上均显著优于 VideoComposer，同时视频质量（FVD: 852.15 vs 1004.99）和文本相似度（CLIPSIM: 0.2319 vs 0.2214）也更优（Table 1）。

- **相对于 DragNUWA**：DragNUWA 使用光流轨迹进行运动控制，但不区分前景物体与背景，无法独立控制物体运动。MotionCtrl 的 OMCM 通过稀疏轨迹显式控制前景物体的局部运动，而 CMCM 独立处理全局场景变换，实现了更精细的运动粒度。

- **相对于底层模型 LVDM**（He et al., 2022）：MotionCtrl 在冻结的 LVDM（VideoCrafter1）之上插入适配模块，CMCM 仅新增少量 MLP 层并训练时序 Transformer 的第二自注意力模块，OMCM 通过多尺度卷积层注入空间特征。消融实验（Table 2）表明，CMCM 集成到 LVDM 的时序 Transformer 中时，CamMC 从无控制的 0.9010 降至 0.0289，且生成质量（FID、FVD）与原始 LVDM 持平，验证了适配器设计的有效性。

### 核心设计选择与因果机制

1. **CMCM 集成位置的选择**：相机运动本质是跨帧的全局场景变换，因此与时序注意力机制天然契合。消融实验（Table 2）系统比较了 CMCM 集成到时间嵌入、空间交叉注意力、空间自注意力和时序 Transformer 四种方案的效果。结果显示，集成到时序 Transformer 获得最低的 CamMC（0.0289），而集成到空间模块或时间嵌入的效果显著较差（CamMC 分别为 0.9010 和 0.1320），验证了“全局时序变化应由时序模块处理”的设计直觉。

2. **OMCM 的训练策略**：物体运动是局部区域的空间位置变化，因此 OMCM 将轨迹特征注入 LVDM 编码器的卷积层。训练上，先使用 ParticleSfM 从 WebVid 视频中提取的密集轨迹进行预训练（20,000 次迭代），再使用稀疏轨迹微调（20,000 次迭代）。消融实验（Table 3）表明，这种“密集预训练 + 稀疏微调”策略的 ObjMC 为 25.1198，优于仅用密集轨迹（36.8351）或仅用稀疏轨迹（28.877）训练，且能泛化至推理时的稀疏输入。

3. **多步训练策略的必要性**：由于不存在同时包含文本描述、相机姿态和物体运动轨迹的完整标注数据集，MotionCtrl 采用分步训练：先在 RealEstate10K（经 BLIP-2 生成描述）上训练 CMCM，再在 WebVid（经 ParticleSfM 合成轨迹）上训练 OMCM。消融实验（Section 4.3.3）表明，先 CMCM 后 OMCM 的顺序优于同时训练或反向顺序，因为后训练 OMCM 时冻结 CMCM 可以保护已学到的相机运动控制能力。

### 适用边界

- **优势场景**：需要独立控制相机运动和物体运动的视频生成任务，如电影级运镜合成、动态场景编辑、以及需要精确运动编排的创意内容生成。MotionCtrl 支持相机运动速度调节和稀疏轨迹下的物体运动控制，用户只需提供少量关键点即可引导物体运动。

- **技术约束**：
  - 同时控制相机运动和物体运动时，两种运动的精确协调仍有不足（论文明确列为 limitation）。
  - OMCM 目前仅支持用户提供一条或几条稀疏轨迹（最大轨迹数 N=8），对于多物体密集交互的复杂场景可能不够充分。
  - 轨迹提取依赖 ParticleSfM，计算开销较大，可能限制了向更大规模数据集的扩展。
  - 底层模型 LVDM 的生成能力本身构成上限，MotionCtrl 作为适配器无法超越基座模型的视频质量天花板。

### 局限与开放问题

**论文明确的局限**：
1. 同时控制相机运动与物体运动时，生成视频的两种运动在精确协调上仍有不足。
2. 当前仅支持用户提供稀疏轨迹，对于更复杂的物体运动场景需要更丰富的交互方式。
3. OMCM 训练的轨迹提取过程（ParticleSfM）计算开销较大。

**开放问题**：
1. 如何进一步提高同时控制相机与物体运动时的生成精度和视觉和谐度？
2. 能否设计更直观的交互方式（如草图、自然语言指令）让用户定义复杂的相机路径和物体轨迹，降低使用门槛？
3. 如何将 MotionCtrl 的运动控制机制适配到更长视频生成或更高帧率的情境中？当前 CMCM 的相机姿态序列和 OMCM 的轨迹均与帧数绑定，向可变长度视频的泛化需要额外的架构调整。
4. 运动控制模块是否可以与更强的基座模型（如 Sora 类架构）结合，以突破 LVDM 的生成质量上限？

### 知识库定位

MotionCtrl 处于**可控视频生成**与**运动解耦**的交叉点。其在知识库中的位置可概括为：

- **上游依赖**：LVDM（视频扩散模型基座）、ParticleSfM（轨迹提取）、RealEstate10K / WebVid / HD-VILA（训练数据）。
- **并行工作**：AnimateDiff（LoRA 相机控制）、VideoComposer（运动向量控制）、DragNUWA（光流轨迹控制）。
- **核心增量**：首次在统一模型中实现相机运动与物体运动的结构性解耦，通过 CMCM 的时序集成和 OMCM 的空间集成，分别匹配两类运动的本质特性。
- **下游可能扩展**：更复杂的多物体交互控制、与 3D 感知（如 NeRF）结合的场景级视频生成、以及面向视频编辑的运动迁移任务。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation.pdf]]
