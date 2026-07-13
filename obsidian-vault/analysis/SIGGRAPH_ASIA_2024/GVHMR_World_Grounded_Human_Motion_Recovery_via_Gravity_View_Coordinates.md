---
title: World-Grounded Human Motion Recovery via Gravity-View Coordinates
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2024/GVHMR_World_Grounded_Human_Motion_Recovery_via_Gravity_View_Coordinates.pdf
project_link: https://zju3dv.github.io/gvhmr
code_link: null
aliases:
- WGHMRGVC
tags:
- SIGGRAPH_ASIA_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过引入由世界重力和相机视角方向唯一确定的重力-视角（GV）坐标系，将每帧的人体方向预测转化为明确定义的目标，并利用相机相对旋转恢复全局一致运动，从而切断误差沿时间累积的路径。
primary_logic: GV坐标系使网络能够直接学习重力对齐的人体姿态，然后通过GV系统间的相对旋转（仅绕重力轴的一维旋转）将所有帧对齐到统一世界坐标系，从而在避免自回归的同时保持重力一致性。
claims:
- GVHMR在所有世界接地指标（WA-MPJPE, W-MPJPE, RTE）上均优于WHAM等现有方法，且在RICH和EMDB上表现最佳。
- 消融实验表明移除GV坐标预测（w/o IGv）会显著降低世界坐标指标，证明GV坐标是避免累积误差的关键设计。
- 随序列增长，GVHMR的全局方向误差远低于WHAM，证明其有效遏制了长期误差累积。
- "在EMDB数据集上无论是否使用FlipEval，GVHMR均优于WHAM（PA-MPJPE: 44.2 vs 49.4）。"
---

# World-Grounded Human Motion Recovery via Gravity-View Coordinates

> [!tip] 核心洞察
> GV坐标系使网络能够直接学习重力对齐的人体姿态，然后通过GV系统间的相对旋转（仅绕重力轴的一维旋转）将所有帧对齐到统一世界坐标系，从而在避免自回归的同时保持重力一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于重力-视角坐标系的世界接地人体运动恢复 |
| 英文题名 | World-Grounded Human Motion Recovery via Gravity-View Coordinates |
| 会议/期刊 | SIGGRAPH ASIA 2024 |
| Links | [Project](https://zju3dv.github.io/gvhmr) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | GVHMR |
| Dataset | RICH, EMDB, 3DPW |

> [!tip] 效果简介
> - RICH (world-grounded) 上，WA-MPJPE100 (mm) 78.8 (GVHMR w/ DPVO) vs Best prior (WHAM w/ GT Gyro) ~119.2 (-40.4)。
> - EMDB (camera-space) 上，PA-MPJPE (mm) 44.2 (GVHMR) vs 49.4 (WHAM, no FlipEval) (-5.2)。
> - 3DPW (camera-space) 上，PA-MPJPE (mm) 36.2 vs 35.9 (WHAM, slightly worse by 0.3 mm) (+0.3)。

## 概要

从单目视频中恢复世界坐标系下的人体运动，是计算机视觉与图形学中的一项核心挑战。其根本瓶颈在于：世界坐标系的定义本身存在模糊性——相机坐标系中的“上”并不等同于物理世界的重力方向，导致现有自回归方法在沿重力轴累积误差，难以保持长期运动一致性。

针对这一问题，**GVHMR**（Zhejiang University, SIGGRAPH Asia 2024）提出了一种全新的运动恢复范式。其核心洞察是：通过引入由**世界重力方向**和**相机视角方向**唯一确定的**重力-视角（Gravity-View, GV）坐标系**，将每帧的人体方向预测转化为一个明确定义的目标，再利用相邻帧GV系统间的相对旋转（仅绕重力轴的一维旋转）将所有帧对齐到统一世界坐标系，从而从根本上切断误差沿时间累积的路径。

在方法层面，GVHMR用一个融合了**旋转位置编码（RoPE）**的相对Transformer替代了传统的自回归RNN，在训练时使用短序列、推理时通过感受野受限的注意力掩码直接外推到任意长度视频。这一设计使其在保持全局一致性的同时，推理速度显著优于自回归方法——处理1430帧视频仅需约0.28秒（RTX 4090），比WHAM快约7倍。

在实验验证上，GVHMR在所有世界接地指标上均取得领先：在RICH数据集上WA-MPJPE达到78.8 mm，较先前最优方法降低约40 mm；在EMDB上无论是否使用FlipEval增强均优于WHAM。消融实验进一步证实，移除GV坐标预测会导致世界坐标指标显著恶化，而RoPE和Transformer架构对长序列泛化至关重要。随序列增长，GVHMR的全局方向误差远低于自回归方法，证明了其有效遏制长期误差累积的能力。

该方法目前聚焦单人场景，其预处理依赖2D关键点检测与相机旋转估计，在极端遮挡或快速旋转场景下仍可能受到影响。



从单目视频中恢复三维人体运动是计算机视觉与图形学领域的核心问题，其应用涵盖虚拟现实、人机交互、运动分析等场景。近年来，基于数据驱动的方法在相机空间（camera space）的人体姿态估计上取得了长足进步，但在恢复**世界接地人体运动**（world-grounded human motion）——即在一个具有物理重力参照的世界坐标系下还原人体的绝对位置与朝向——方面仍面临根本性挑战。

**核心瓶颈：世界坐标系的定义模糊性与误差累积。** 现有方法通常直接在相机坐标系下预测人体姿态，然后依赖额外的后处理或自回归（autoregressive）策略将其转换到世界坐标系。这一范式存在两个深层缺陷。其一，相机坐标系与世界坐标系之间的映射关系本身是模糊的：同一段人体运动在不同相机位姿下会呈现截然不同的投影，而单目视频无法唯一确定这一映射。其二，自回归方法（如 **WHAM**，Shin et al., CVPR 2024）逐帧预测相对旋转来恢复全局方向，这导致误差沿时间轴**持续累积**，尤其在重力方向（gravity direction）上，随着序列增长，全局朝向的漂移会急剧恶化（见 Fig. 9）。

**现有方法的缺口。** 基于优化的方法（如 **SLAHMR**，Ye et al., CVPR 2023；**PACE**，Kocabas et al., 3DV 2024）试图通过引入多模态线索和物理约束来缓解这一问题，但通常计算开销大且依赖精细的初始化。基于 SLAM 或视觉里程计的方案（如 **TRAM**，Wang et al., arXiv 2024；**WHAC**，Yin et al., arXiv 2024）则利用相机运动估计来辅助坐标系转换，但其性能高度依赖相机位姿估计的精度，在动态场景或大范围旋转下容易失效。这些方法均未从根本上解决**方向预测坐标系的定义问题**——网络学习的目标本身缺乏明确的物理参照，导致训练信号模糊。

**本文动机。** 针对上述瓶颈，本文提出一个关键洞察：如果能在网络内部建立一个**由世界重力和相机视角唯一确定的坐标系**作为方向预测的目标空间，就可以切断误差沿时间累积的路径。具体而言，重力-视角（Gravity-View, GV）坐标系将人体朝向的学习目标与物理重力对齐，使每帧的方向预测成为一个明确定义的问题；随后，通过相邻帧 GV 系统间的相对旋转（仅绕重力轴的一维旋转）即可将所有帧对齐到统一世界坐标系，从而在**避免自回归**的同时保持重力一致性。这一设计将全局运动恢复从“逐帧累积相对量”转变为“每帧独立预测绝对方向 + 帧间对齐”，从机制上消除了长期漂移的根源。



## 核心方法与创新机理

GVHMR的核心创新在于通过**重新定义人体方向预测的坐标系**，从根本上切断了单目视频中世界接地运动恢复的累积误差传播路径。该方法的三个关键创新点构成了一条完整的因果链：**GV坐标系的定义 → 全局方向的非自回归恢复 → 长序列Transformer架构的适配**。

### 创新1：重力-视角（GV）坐标系——消除方向歧义

**基线瓶颈**：现有方法（如 **WHAM**，Shin et al., CVPR 2024）在相机坐标系中预测人体方向。当相机发生俯仰或横滚运动时，同一人体姿态在相机坐标系下会呈现不同的方向表达（见 Fig. 2），导致网络需要额外学习相机运动与人体方向之间的耦合关系。更严重的是，自回归方法沿时间累积相对旋转时，重力方向（俯仰和横滚分量）的微小误差会不断放大，最终导致人体倾斜甚至漂移。

**GV坐标系的定义**：对于每一帧图像，利用**世界重力方向**和**相机视角方向**（图像平面法向量）唯一定义一个右手坐标系（见 Fig. 4）：
- y轴对齐世界重力方向
- z轴为相机视角方向在水平面上的投影
- x轴由右手定则确定

这一设计使人体方向预测目标变得明确定义且与重力自然对齐：在GV坐标系中，一个站立的人体始终呈现“直立”的姿态，无论相机如何倾斜（见 Fig. 2 对比）。

**核心洞察**：GV坐标系使网络能够直接学习重力对齐的人体姿态，而无需隐式建模相机运动。更重要的是，相邻帧GV坐标系之间的相对旋转**仅发生在绕重力轴（y轴）的一维旋转上**（见 Fig. 5），这意味着帧间对齐只需要估计一个标量角度，从根本上消除了俯仰和横滚方向的误差累积。

### 创新2：非自回归的全局方向恢复

**基线瓶颈**：WHAM等方法采用自回归策略，逐帧预测当前帧相对于前一帧的旋转增量，然后累积得到全局方向。这种方式使每一帧的预测误差都会传导至后续所有帧，导致长期序列中误差的线性累积（见 Fig. 9）。

**GVHMR的恢复策略**：GVHMR彻底摒弃了自回归。网络对**每一帧独立预测**其在GV坐标系中的方向 $\Gamma_{GV}^t$，然后利用相机相对旋转（由视觉里程计DPVO或陀螺仪提供）计算相邻帧GV系统间的相对旋转矩阵 $R_{\Delta GV}^i$，通过纯几何方式将所有帧对齐到第一帧的GV参考系：

$$\Gamma_w^t = \begin{cases} \Gamma_{GV}^0, & t=0, \\\\ \prod_{i=1}^t R_{\Delta GV}^i \cdot \Gamma_{GV}^t, & t>0. \end{cases}$$

这一设计的因果逻辑在于：**每帧的方向预测是独立的，不存在时序误差传播**；帧间对齐所需的 $R_{\Delta GV}$ 完全由相机旋转决定，不依赖人体运动预测。全局平移则通过累积根速度在世界坐标系下的投影得到（Eq. 1），同样避免了自回归的误差累积。

**证据强度**：消融实验（Tab. 3）中，移除GV坐标预测（w/o IGv）导致世界坐标指标WA-MPJPE、W-MPJPE和RTE显著恶化，直接证明了GV坐标系是避免累积误差的关键设计。Fig. 9的曲线进一步显示，随序列增长，GVHMR的全局方向误差远低于WHAM，验证了非自回归策略在遏制长期误差累积上的有效性。

### 创新3：面向长序列外推的Transformer架构

**基线瓶颈**：传统基于RNN或滑动窗口注意力的方法难以在训练短序列的情况下泛化到长序列推理。

**GVHMR的架构适配**（见 Fig. 6）：
- **旋转位置编码（RoPE）**：替代绝对位置编码，通过将相对位置信息编码为注意力分数中的旋转变换（Eq. 4-5），使模型学习的是相对时序关系而非绝对位置，从而支持训练时未见过的序列长度。
- **感受野受限的注意力掩码**：每个token只能关注前后 $L$ 帧内的token（Eq. 7），使模型在训练时学习局部时序依赖，推理时可直接应用于任意长度序列，实现长度外推。

消融实验（Tab. 3）表明，用自回归RNN替换Transformer（w/o Transformer）或移除RoPE（w/o RoPE）均会导致性能下降，验证了该架构设计对时序建模和长序列泛化的必要性。

### 创新4：基于静止概率的脚部滑动优化

作为后处理步骤，GVHMR预测每个关节的“静止概率”，识别脚部与地面接触的帧。利用这些概率作为软约束，通过CCD逆运动学求解器优化局部姿态，减少脚部滑动和抖动（Tab. 3中w/o Post-Processing的消融验证了其贡献）。这一设计将物理合理性约束融入学习框架，而非依赖独立的物理优化模块。

### 方法谱系与知识库定位

GVHMR在世界接地人体运动恢复这一任务上，与以下方法形成对比：
- **WHAM**（Shin et al., CVPR 2024）：自回归预测全局位姿，GVHMR通过GV坐标系和非自回归策略解决了其累积误差问题。
- **SLAHMR**（Ye et al., CVPR 2023）：基于优化的多线索全局运动估计，GVHMR提供了更高效的纯学习方案。
- **TRAM**（Wang et al., arXiv 2024）和 **WHAC**（Yin et al., arXiv 2024）：利用SLAM或视觉里程计进行坐标系转换，GVHMR的创新在于将坐标系定义与人体运动预测解耦，并通过GV坐标系的巧妙定义简化了帧间对齐问题。
- **HMR2.0**（Goel et al., ICCV 2023）、**VIBE**（Kocabas et al., CVPR 2020）、**TCMR**（Choi et al., CVPR 2021）：单帧或视频人体姿态估计方法，GVHMR在此基础上增加了世界接地运动恢复能力。



GVHMR的整体流水线遵循“预处理→早融合→相对Transformer→多任务MLP头→全局轨迹构建→后处理IK优化”的级联结构，如图3和图6所示。其核心设计目标是在避免自回归的前提下，直接回归整个运动序列，从而切断误差沿时间累积的路径。

### 预处理模块

给定一段单目视频，GVHMR首先沿用WHAM（Shin et al., CVPR 2024）的预处理流程，依次完成四项任务：
1. **人体边界框跟踪**：在视频帧中定位并跟踪人体区域。
2. **2D关键点检测**：在边界框内检测人体2D关键点。
3. **图像特征提取**：从裁剪后的人体区域提取视觉特征。
4. **相机相对旋转估计**：利用视觉里程计（如DPVO）或陀螺仪，估计相邻帧之间的相机相对旋转矩阵。

这一预处理阶段为后续模块提供了多模态输入，但其误差（如跟踪漂移、关键点抖动）可能向下游传导。实验表明，GVHMR对相机旋转噪声具有较强的鲁棒性：在RICH数据集上，使用GT陀螺仪与使用DPVO估计的相机旋转，得到的世界接地指标近似（Tab. 1）。

### 早融合模块

预处理产生的多模态特征（图像特征、2D关键点特征、相机旋转特征等）被投影到统一的维度空间，然后逐帧求和，形成每一帧的token表示。这种早融合策略将异构信息压缩为紧凑的时序token序列，供后续Transformer处理。

### 相对Transformer

时序token序列被送入一个基于旋转位置编码（Rotary Positional Embedding, RoPE）的Transformer网络。该网络有两个关键设计：

- **旋转位置编码（RoPE）**：将512维的token空间划分为256个二维子空间，对每个子空间施加相对位置的二维旋转。注意力分数计算为：
  $$a^{ts} = (\mathbf{W}_q f_{token}^t)^\top \mathbf{R}(\mathbf{p}^s - \mathbf{p}^t) (\mathbf{W}_k f_{token}^s)$$
  其中$\mathbf{R}(\mathbf{p})$为分块对角旋转矩阵，编码了token $s$与$t$之间的相对位置信息。这使得模型能自然地处理相对时序关系，而非依赖绝对位置编码。

- **感受野受限的注意力掩码**：每个token只能关注其前后$L$帧范围内的token：
  $$m^{ts} = \begin{cases} 0, & \text{if } -L < t-s < L, \\ -\infty, & \text{otherwise.} \end{cases}$$
  这一设计使得模型可以在短序列上训练，在长序列上推理时实现外推，同时控制注意力计算量。

### 多任务MLP头

Transformer输出的时序特征被送入多个并行的MLP头，同时预测四类信息：
1. **GV坐标系人体方向** $\Gamma_{GV}^t$：在重力-视角坐标系下的人体全局方向。
2. **根速度** $v_{root}^t$：在SMPL坐标系下的根节点速度。
3. **关节静止概率**：预定义关节（如脚部）处于静止状态的概率，用于后续IK优化。
4. **相机空间SMPL参数**：弱透视相机参数及局部姿态、形状参数。

其中，GV坐标系方向和根速度是构建世界坐标系全局运动的关键中间表示（intermediate representations）。

### 全局轨迹构建模块

这一模块是GVHMR区别于自回归方法的核心。它利用两个关键公式将每帧独立预测的中间表示转换为统一世界坐标系下的全局轨迹：

- **全局平移累积**（Eq. 1）：通过累加根速度在世界坐标系下的投影得到全局平移：
  $$\tau_w^t = \begin{cases} [0,0,0]^T, & t=0, \\ \sum_{i=0}^{t-1} \Gamma_w^i v_{root}^i, & t>0. \end{cases}$$

- **全局方向恢复**（Eq. 2）：利用相邻帧GV系统间的相对旋转矩阵$R_{\Delta GV}^i$，将每帧的GV方向对齐到第一帧的参考系：
  $$\Gamma_w^t = \begin{cases} \Gamma_{GV}^0, & t=0, \\ \prod_{i=1}^t R_{\Delta GV}^i \cdot \Gamma_{GV}^t, & t>0. \end{cases}$$

这里的核心洞察是：GV系统间的相对旋转$R_{\Delta GV}$**仅绕重力轴（y轴）发生一维旋转**（Fig. 5），因此全局方向恢复过程不会引入重力方向上的累积误差。这从根本上解决了自回归方法（如WHAM）沿重力方向误差不断累积的问题。

### 后处理IK优化

全局轨迹构建完成后，GVHMR利用预测的关节静止概率，通过CCD逆运动学求解器对脚部接触进行精化。具体而言，对于被预测为静止的关节（如脚掌），IK求解器会调整局部姿态，使其位置保持固定，从而减少脚部滑动和运动抖动。这一后处理步骤进一步提升了全局运动的物理合理性和视觉平滑度。

### 端到端效率

整个GVHMR网络（不含预处理）在RTX 4090 GPU上处理一段1430帧（约45秒）的视频仅需280毫秒，比WHAM快约7倍。这一效率优势源于其非自回归的设计——所有帧的中间表示可并行预测，全局轨迹则通过确定性的累积公式一次性构建。

### 补充图表

![[assets/figures/papers/paper_list_l1648_GVHMR_World_Grounded_Human_Motion_Recovery_via_Gravity_View_Coordinates/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the proposed framework. Given a monocular video (left), following WHAM [Shin et al. 2024], GVHMR preprocesses the video by tracking the human bounding box, detecting 2D keypoints, extracting image features, and estimating camera relative rotation using visual odometry or a gyroscope. GVHMR then fuses these features into per-frame tokens, which are processed with a relative transformer and multitask MLPs. The outputs include: (1) intermediate representations (middle), i.e. human orientation in the Gravity-View coordinate system, root velocity in the SMPL coordinate system, and the stationary probability for predefined joints; and (2) camera frame SMPL parameters (right-top). Fina...*

![[assets/figures/papers/paper_list_l1648_GVHMR_World_Grounded_Human_Motion_Recovery_via_Gravity_View_Coordinates/figures/001_Figure_1.jpg]]
*Figure 1: Overview. Given an in-the-wild monocular video, our method accurately regresses World-Grounded Human Motion: 4D human poses and shapes in a gravity-aware world coordinate system. The proposed network, excluding preprocessing (2D human tracking, feature extraction, relative camera rotation estimation), takes 280 ms to process a 1430-frame video (approximately 45 seconds) on an RTX 4090 GPU*



GVHMR 的核心架构由**预处理、早融合、相对Transformer、多任务MLP头、全局轨迹构建、后处理IK优化**六个模块级联而成（Fig. 3, Fig. 6）。其关键创新在于将人体方向预测从传统的相机坐标系迁移到**重力-视角（GV）坐标系**，并通过GV系统间的相对旋转实现无自回归的全局运动恢复。

![[assets/figures/papers/paper_list_l1648_GVHMR_World_Grounded_Human_Motion_Recovery_via_Gravity_View_Coordinates/figures/004_Figure_6.jpg]]
*Figure 6: Network architecture. The input features are fused into per-frame tokens by the early-fusion module, processed by the relative transformer, and then output by multitask MLPs as intermediate representations. The weak-camera parameter ???? is restored to the camera frame*

### 3.1 GV坐标系与全局轨迹恢复

**GV坐标系定义**：对于每一帧图像，利用世界重力方向 $\mathbf{g}$ 和相机视角方向（即像平面法向量）唯一确定一个GV坐标系（Fig. 4）。该坐标系的y轴与重力方向对齐（$\mathbf{y} = \mathbf{g}$），使得人体在该坐标系中自然保持重力对齐，消除了相机滚转和俯仰带来的姿态倾斜歧义（Fig. 2）。

**全局平移累积**：网络预测每帧在SMPL坐标系下的根节点速度 $\mathbf{v}_{root}^t$，通过世界坐标系下的方向矩阵 $\Gamma_w^i$ 将其变换到世界坐标系并逐帧累加，得到全局平移 $\tau_w^t$：

$$\tau_w^t = \begin{cases} [0,0,0]^T, & t=0, \\ \sum_{i=0}^{t-1} \Gamma_w^i \mathbf{v}_{root}^i, & t>0. \end{cases} \quad \text{(Eq. 1)}$$

**全局方向恢复**：这是方法的核心机制。网络每帧独立预测GV坐标系下的人体方向 $\Gamma_{GV}^t$。相邻帧GV系统间的相对旋转 $R_{\Delta GV}^i$ 仅绕重力轴（y轴）发生（Fig. 5），因此可以通过累积这些一维旋转将所有帧对齐到第一帧的GV参考系，得到世界坐标系方向 $\Gamma_w^t$：

$$\Gamma_w^t = \begin{cases} \Gamma_{GV}^0, & t=0, \\ \prod_{i=1}^t R_{\Delta GV}^i \cdot \Gamma_{GV}^t, & t>0. \end{cases} \quad \text{(Eq. 2)}$$

这一设计的**因果机制**在于：每帧方向预测是独立的，不存在自回归依赖；全局对齐仅依赖相机相对旋转（由视觉里程计DPVO或陀螺仪提供），误差不会沿时间累积。消融实验证实，移除GV坐标预测（w/o IGv）会导致世界坐标指标WA-MPJPE、W-MPJPE和RTE显著恶化（Tab. 3），验证了GV坐标系是切断累积误差路径的关键。

### 3.2 相对Transformer与位置编码

**早融合**：将2D关键点、图像特征、相机旋转等多模态特征投影到统一维度后逐帧求和，形成每帧的token表示 $f_{token}^t$（Fig. 6）。

**旋转位置编码（RoPE）**：为支持训练短序列、推理长序列的外推能力，GVHMR采用RoPE替代绝对位置编码。第 $t$ 个token的自注意力输出为：

$$\mathbf{o}^t = \sum_{i \in T} \mathrm{Softmax}(a^{ts})^i \mathbf{W}_v f_{token}^i \quad \text{(Eq. 3)}$$

其中注意力分数 $a^{ts}$ 融合了相对位置旋转编码：

$$a^{ts} = (\mathbf{W}_q f_{token}^t)^\top \mathbf{R}(\mathbf{p}^s - \mathbf{p}^t) (\mathbf{W}_k f_{token}^s) \quad \text{(Eq. 4)}$$

旋转矩阵 $\mathbf{R}(\mathbf{p})$ 将512维特征空间划分为256个二维子空间，对每个子空间施加由位置差编码的二维旋转：

$$\mathbf{R}(\mathbf{p}) = \begin{pmatrix} \hat{\mathbf{R}}(\alpha_1^\top \mathbf{p}) & & 0 \\ & \ddots & \\ & & \hat{\mathbf{R}}(\alpha_{256}^\top \mathbf{p}) \end{pmatrix}, \quad \hat{\mathbf{R}}(\theta)=\begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix} \quad \text{(Eq. 5)}$$

**感受野受限的注意力掩码**：为进一步保证长序列外推的稳定性，引入注意力掩码限制每个token只能关注前后 $L$ 帧内的token：

$$m^{ts} = \begin{cases} 0, & \text{if } -L < t-s < L, \\ -\infty, & \text{otherwise.} \end{cases} \quad \text{(Eq. 7)}$$

消融实验表明，移除RoPE（w/o RoPE）或用自回归RNN替换Transformer（w/o Transformer）均会导致性能下降（Tab. 3），证实了相对位置编码和时序注意力机制对长序列建模的必要性。

### 3.3 后处理IK优化

网络额外预测每个关节的**静止概率**，用于判断脚部等关节是否与地面接触。基于这些概率计算目标关节位置后，通过CCD逆运动学求解器对全局运动进行精化，减少脚部滑动和抖动。消融实验中移除后处理（w/o Post-Processing）会显著增加脚部滑动和运动不平滑度（Tab. 3, Fig. 10）。

### 补充图表

![[assets/figures/papers/paper_list_l1648_GVHMR_World_Grounded_Human_Motion_Recovery_via_Gravity_View_Coordinates/figures/005_Figure_4.jpg]]
*Figure 4: Gravity-View (GV) coordinate system, defined by the gravity direction and the camera view direction. (Refer to Sec. 3.1 for details)*

![[assets/figures/papers/paper_list_l1648_GVHMR_World_Grounded_Human_Motion_Recovery_via_Gravity_View_Coordinates/figures/006_Figure_5.jpg]]
*Figure 5: Relative rotation between two GV coordinate systems. (a) shows two adjacent GV coordinate systems and the camera view directions. (b) illustrates the relative rotation between two GV systems*

![[assets/figures/papers/paper_list_l1648_GVHMR_World_Grounded_Human_Motion_Recovery_via_Gravity_View_Coordinates/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of coordinate systems. In camera coordinates, a person may appear inclined due to the camera’s roll and pitch movement. In contrast, in GV coordinates, the person is naturally aligned with gravity*



## 实验与关键发现

### 世界接地运动恢复性能

GVHMR在世界接地指标上展现出对现有方法的显著优势。在RICH数据集上，GVHMR配合视觉里程计DPVO取得WA-MPJPE100 78.8 mm、W-MPJPE100 126.3 mm、RTE 2.4、Jitter 12.8、Foot-Sliding 3.0（Table 1）。相比之下，此前最优方法WHAM即使使用GT陀螺仪，WA-MPJPE100仍约为119.2 mm——GVHMR降低了约40.4 mm。在EMDB-2数据集上，GVHMR同样全面优于WHAM等基线方法。

![[assets/figures/papers/paper_list_l1648_GVHMR_World_Grounded_Human_Motion_Recovery_via_Gravity_View_Coordinates/figures/007_Table_1.jpg]]
*Table 1: World-grounded metrics. We evaluate the global motion quality on the RICH [Huang et al. 2022] and EMDB-2 [Kaufmann et al. 2023] dataset. Parenthesis denotes the number of joints used to compute WA-MPJPE100, W-MPJPE100 and Jitter*

**相机旋转源鲁棒性**：GVHMR在使用GT陀螺仪与使用DPVO估计的相机旋转时，世界接地指标近似（Table 1），表明方法对相机旋转噪声具有较强的鲁棒性。这一特性得益于GV坐标系将方向预测与相机运动解耦的设计。

### 相机空间运动恢复性能

在相机空间指标上，GVHMR同样达到领先水平。在3DPW数据集上取得PA-MPJPE 36.2 mm、MPJPE 55.6 mm；在RICH上取得PA-MPJPE 39.5 mm、MPJPE 66.0 mm；在EMDB-1上取得PA-MPJPE 42.7 mm、MPJPE 72.6 mm（Table 2）。值得注意的是，WHAM在3DPW的PA-MPJPE上以35.9 mm略微领先0.3 mm，但GVHMR在其余所有数据集和指标上均更优。

![[assets/figures/papers/paper_list_l1648_GVHMR_World_Grounded_Human_Motion_Recovery_via_Gravity_View_Coordinates/figures/008_Table_2.jpg]]
*Table 2: Camera-space metrics. We evaluate the camera-space motion quality on the 3DPW [von Marcard et al. 2018], RICH [Huang et al. 2022] and EMDB-1 [Kaufmann et al. 2023] datasets. ∗ denotes models trained with the 3DPW training set*

在EMDB数据集上，无论是否使用FlipEval测试时增强，GVHMR均优于WHAM（PA-MPJPE: 44.2 vs 49.4，Table 4），进一步验证了方法本身的优越性而非增强技巧的贡献。

![[assets/figures/papers/paper_list_l1648_GVHMR_World_Grounded_Human_Motion_Recovery_via_Gravity_View_Coordinates/figures/009_Table_4.jpg]]
*Table 4: Dataset and test-time-augmentation ablation on EMDB. B denotes BEDLAM [Black et al. 2023] synthetic dataset*

### 长期误差累积的遏制

Fig. 9展示了全局方向误差随序列长度的变化曲线。WHAM的自回归预测方式导致误差沿时间持续累积，序列越长误差越大；而GVHMR通过每帧独立预测GV方向、再通过仅绕重力轴的一维相对旋转进行对齐，有效切断了误差累积路径，在长序列上保持远低于WHAM的全局方向误差。这一结果直接验证了GV坐标系设计的核心动机——消除自回归带来的长期一致性退化。

### 推理效率

GVHMR在效率上同样具有显著优势。在RTX 4090 GPU上处理一段1430帧（约45秒）的视频仅需280毫秒（Fig. 1），而WHAM处理同等长度视频约需2.0秒，GVHMR速度快约7倍。这一效率优势得益于Transformer的并行推理能力，避免了自回归方法的逐帧串行计算瓶颈。

### 消融实验

Table 3在RICH数据集上系统消融了GVHMR各关键组件，揭示了以下因果机制：

- **移除GV坐标预测（w/o IGv）**：世界坐标指标WA-MPJPE、W-MPJPE和RTE均显著恶化，证明GV坐标系是避免累积误差、保证全局一致性的核心设计。
- **用自回归RNN替换Transformer（w/o Transformer）**：时序建模能力下降，导致性能降低（Fig. 10定性展示了该变体的运动质量退化）。
- **移除RoPE（w/o RoPE）或使用绝对位置编码**：削弱了长序列泛化能力，影响全局方向恢复精度。
- **不进行后处理（w/o Post-Processing）**：脚部滑动和抖动增加，运动平滑度下降（Fig. 10展示了后处理对脚部接触质量的改善）。
- **训练数据消融**：在EMDB上，去掉BEDLAM合成数据或FlipEval增强均会降低模型精度（Table 4），表明多样化训练数据对泛化能力的重要性。

### 失败模式与局限性

尽管GVHMR在整体性能上表现优异，仍存在以下局限：

1. **预处理依赖**：方法依赖外部2D关键点检测、人体跟踪和相机旋转估计模块，这些模块的误差可能传导至下游。极端场景如严重遮挡或快速旋转下，预处理质量下降可能影响最终结果。
2. **相机旋转估计退化**：在背景变化极小或完全静态的场景中，视觉里程计可能无法准确估计相机旋转，从而影响GV系统间相对旋转的计算精度。
3. **多人场景缺失**：当前方法仅针对单人场景设计，未涉及多人交互或人与场景的复杂交互。
4. **极长视频的内存限制**：虽然注意力掩码支持训练短序列、推理长序列的外推，但推理时显存占用仍与序列长度成正比，处理数小时的极长视频仍需分段进行。

### 补充图表

![[assets/figures/papers/paper_list_l1648_GVHMR_World_Grounded_Human_Motion_Recovery_via_Gravity_View_Coordinates/figures/013_Figure_9.jpg]]
*Figure 9: Global orientation error along time. WHAM [Shin et al. 2024] tends to accumulate more global orientation error as the sequence length increases, while our approach maintains a much lower error rate*

![[assets/figures/papers/paper_list_l1648_GVHMR_World_Grounded_Human_Motion_Recovery_via_Gravity_View_Coordinates/figures/014_Figure_10.jpg]]
*Figure 10: Qualitative results of ablations. Each component of our method contributes to the final results*

![[assets/figures/papers/paper_list_l1648_GVHMR_World_Grounded_Human_Motion_Recovery_via_Gravity_View_Coordinates/figures/010_Table_3.jpg]]
*Table 3: Ablation studies. We compare our method with seven variants on the RICH [Huang et al. 2022] dataset (Refer to Sec. 4.4 for details). ∗ denotes the variant that employs the sliding window*



## 定位与知识库关联

### 1. 核心瓶颈与因果机制

单目视频中恢复世界接地人体运动的核心瓶颈在于**世界坐标系定义的模糊性**。现有方法通常直接在相机坐标系中预测人体方向，然后依赖自回归方式逐帧累积相对旋转来恢复全局运动。这一范式存在根本性缺陷：相机坐标系的方向定义随相机运动而变化，缺乏稳定的几何参照，导致**重力方向的误差沿时间轴不断累积**，在长序列中尤为严重（见 Fig. 9）。

GVHMR 通过引入**重力-视角（Gravity-View, GV）坐标系**切断了这一误差累积路径。GV 坐标系由世界重力方向和相机视角方向唯一确定（Fig. 4），使网络能够直接学习重力对齐的人体姿态。其核心因果机制在于：每帧独立预测 GV 坐标系中的方向，然后通过相邻帧 GV 系统间的**相对旋转**（该旋转仅绕重力轴的一维旋转，见 Fig. 5）将所有帧对齐到统一的参考系。这一设计将原本需要自回归建模的全局方向恢复问题，转化为一个**明确定义的几何对齐问题**，从根本上避免了误差沿时间累积。

### 2. 与现有工作的关系

#### 2.1 世界接地运动恢复方法

**WHAM**（Shin et al., CVPR 2024）是 GVHMR 最直接的对比基线。WHAM 采用自回归方式在相机坐标系中预测全局位姿，其核心局限在于相机坐标系缺乏稳定的重力参照，导致长期方向误差持续累积。GVHMR 通过 GV 坐标系和 Transformer 架构同时解决了这一问题：在 RICH 数据集上，GVHMR 的 WA-MPJPE100 达到 78.8 mm，而 WHAM 使用 GT 陀螺仪的最佳结果为 119.2 mm（Tab. 1），改善幅度达 40.4 mm。

**SLAHMR**（Ye et al., CVPR 2023）和 **PACE**（Kocabas et al., 3DV 2024）属于基于优化的多线索全局运动估计框架，通常依赖 SLAM 或运动先验进行后处理优化。与这些方法相比，GVHMR 的优势在于将几何约束（GV 坐标系）直接嵌入网络学习过程，无需复杂的后处理优化即可获得全局一致的运动。

**TRAM**（Wang et al., arXiv 2024）和 **WHAC**（Yin et al., arXiv 2024）利用视觉里程计或 SLAM 恢复相机运动，然后将相机空间结果转换到世界坐标系。GVHMR 与这些方法的本质区别在于：GVHMR 在特征学习阶段就引入了重力对齐的坐标系，而非仅在输出阶段进行坐标转换。实验表明，GVHMR 对相机旋转估计的噪声具有鲁棒性——使用 GT 陀螺仪和视觉里程计（DPVO）得到的世界接地指标近似（Tab. 1）。

#### 2.2 人体姿态回归方法

在相机空间人体姿态回归方面，**HMR2.0**（Goel et al., ICCV 2023）采用 ViT 架构处理单帧图像，**VIBE**（Kocabas et al., CVPR 2020）和 **TCMR**（Choi et al., CVPR 2021）则利用时序 RNN 建模视频中的运动信息。GVHMR 的 Transformer 架构结合 RoPE 位置编码，在时序建模能力上优于 RNN 方法（消融实验 w/o Transformer 性能显著下降，Tab. 3）。在相机空间指标上，GVHMR 在 3DPW 上 PA-MPJPE 为 36.2 mm，与 WHAM 的 35.9 mm 基本持平（相差仅 0.3 mm），但在 RICH 和 EMDB 上均取得最优结果（Tab. 2）。

### 3. 适用边界与局限

#### 3.1 依赖外部预处理模块

GVHMR 依赖 2D 关键点检测、人体跟踪和相机相对旋转估计等预处理模块。尽管实验表明方法对相机旋转噪声具有鲁棒性（Tab. 1），但在**极端场景**下仍可能受影响：
- 严重遮挡导致 2D 关键点检测失败；
- 快速旋转或剧烈晃动导致视觉里程计（DPVO）估计不准确；
- 完全静态场景或大范围背景变化使相机旋转估计退化。

#### 3.2 场景与交互限制

- **仅支持单人场景**：当前方法未涉及多人交互或人与场景的复杂交互。扩展到多人场景时，GV 坐标系是否需要为每个人单独定义，如何处理互遮挡，是需要进一步研究的问题。
- **重力参考依赖**：GV 坐标系的定义依赖世界重力方向。在失重环境（如空间站）或动态平台（如运动车辆、船舶）中，重力方向的获取和稳定性面临挑战，框架的适应性需要额外验证。

#### 3.3 计算与序列长度限制

虽然通过感受野受限的注意力掩码（Eq. 7）支持训练短序列、推理长序列的外推，但推理时占用的显存仍与序列长度成正比。对于极长视频（如数小时），仍需分段处理。

#### 3.4 高动态动作的鲁棒性

后处理 IK 优化（基于 CCD 逆运动学求解器和关节静止概率）对极快运动或高动态动作（如跑酷、杂技）的鲁棒性尚未充分验证。在这些场景中，静止概率的预测可能不准确，导致脚部滑动优化效果下降。

### 4. 开放问题

1. **多人体扩展**：GV 坐标系能否扩展到多人场景？是否需要对每个人单独定义 GV 坐标系？如何处理多人互遮挡情况下的重力方向共享与个体姿态解耦？

2. **相机运动极端情况**：当相机运动包含大角度旋转或剧烈晃动时，视觉里程计估计的相机旋转误差是否会显著影响 GV 系统间的对齐精度？是否存在更鲁棒的相机旋转估计策略？

3. **非标准重力环境**：在无重力参考（失重环境）或动态平台中，GV 坐标系的定义需要如何调整？是否可以利用惯性测量单元（IMU）等其他传感器提供重力方向？

4. **高动态运动优化**：后处理 IK 优化对极快运动或高动态动作的鲁棒性如何？是否需要引入物理约束或动力学先验来增强优化稳定性？

5. **跨任务推广**：GV 坐标系的思路——通过引入稳定的几何参照消除方向歧义——能否推广到其他视觉任务？例如物体姿态估计、场景理解等需要处理方向模糊性的领域。



## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2024/GVHMR_World_Grounded_Human_Motion_Recovery_via_Gravity_View_Coordinates.pdf]]
