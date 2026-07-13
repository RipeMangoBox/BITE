---
title: "WHAM: Reconstructing World-grounded Humans with Accurate 3D Motion"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/WHAM_Reconstructing_World_grounded_Humans_with_Accurate_3D_Motion.pdf
project_link: null
code_link: null
aliases:
- WWGHAM
- WHAM
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: WHAM 通过融合 2D 关键点序列的运动上下文与视频图像的视觉上下文，并结合相机角速度与接触感知轨迹细化，从而在全局坐标系中准确估计人体运动。
primary_logic: WHAM 利用大规模 AMASS 运动捕捉数据生成合成 2D 关键点序列以预训练运动编码器-解码器，再通过特征集成器融合图像上下文，并引入接触感知轨迹细化来解决足部滑动问题，实现了在线、高效且准确的全局 3D 人体运动重建。
claims:
- WHAM 在所有基准测试的每帧指标（MPJPE、PA-MPJPE、PVE）上均优于先前方法，包括单帧和视频方法。
- WHAM 在全局轨迹估计的所有指标（W-MPJPE100、RTE、Jitter、FS）上均优于现有方法。
- 消融实验表明，去除特征集成或轨迹细化会显著降低运动准确性和轨迹精度。
- WHAM 以 200 fps 的核心速度运行，显著快于基于优化的 SLAHMR（<0.1 fps）。
---

# WHAM: Reconstructing World-grounded Humans with Accurate 3D Motion

> [!tip] 核心洞察
> WHAM 利用大规模 AMASS 运动捕捉数据生成合成 2D 关键点序列以预训练运动编码器-解码器，再通过特征集成器融合图像上下文，并引入接触感知轨迹细化来解决足部滑动问题，实现了在线、高效且准确的全局 3D 人体运动重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | WHAM：重建具有精确3D运动的世界坐标系人体 |
| 英文题名 | WHAM: Reconstructing World-grounded Humans with Accurate 3D Motion |
| 会议/期刊 | CVPR 2024 |
| Links |  [paper](https://arxiv.org/abs/2312.07531)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | WHAM (World-grounded Humans with Accurate Motion) |
| Dataset | 3DPW, EMDB 2 |

> [!tip] 效果简介
> - 3DPW 上，PA-MPJPE (mm) 35.9 (WHAM ViT) vs 44.4 (HMR2.0) (-8.5)；Accel (m/s^2) 6.6 (WHAM ViT) vs 18.1 (HMR2.0) (-11.5)。
> - EMDB 2 (Global) 上，W-MPJPE100 (mm) 354.8 (WHAM w/ DPVO) vs 2231.4 (DPVO+HMR2.0) (-1876.6)；Jitter (10m/s^3) 22.5 (WHAM w/ DPVO) vs 2987.6 (TRACE) (-2965.1)；Foot Sliding (mm) 4.4 (WHAM w/ DPVO) vs 370.7 (TRACE) (-366.3)。

## 概要

从单目视频中恢复准确、平滑且世界坐标系一致的3D人体运动，是计算机视觉领域的一项长期挑战。现有方法普遍面临一个核心瓶颈：在动态相机拍摄的野外视频中，难以同时实现全局坐标系下精确的人体轨迹估计与无足部滑动的自然运动重建。基于回归的方法（如**TRACE**）往往产生不合理的足部滑动，而基于优化的方法（如**SLAHMR**）虽能改善轨迹，但计算代价极高（<0.1 fps），且整体精度仍落后于单帧方法。

WHAM（World-grounded Humans with Accurate Motion）针对这一瓶颈，提出了一种在线、高效且精确的全局3D人体运动重建框架。其核心洞察在于：通过大规模运动捕捉数据（AMASS）生成的合成2D关键点序列预训练运动编码器-解码器，使模型习得从2D到3D的“提升”能力；再通过特征集成器将运动上下文与视频图像上下文深度融合，并结合相机角速度与接触感知轨迹细化，最终在全局坐标系中输出像素对齐且无足部滑动的人体运动。

在多个野外基准测试中，WHAM取得了全面的最优结果。在3DPW数据集上，WHAM（ViT）的PA-MPJPE达到35.9 mm，较单帧SOTA方法HMR2.0降低8.5 mm，加速度误差（Accel）更是从18.1 m/s²降至6.6 m/s²。在EMDB 2的全局轨迹估计中，WHAM的W-MPJPE100仅为354.8 mm，而DPVO+HMR2.0的组合高达2231.4 mm；足部滑动指标（FS）从TRACE的370.7 mm骤降至4.4 mm，抖动量（Jitter）亦从2987.6降至22.5。消融实验证实，特征集成、2D-to-3D预训练、相机角速度以及轨迹细化四个关键组件对最终性能均有显著贡献。此外，WHAM以约200 fps的核心推理速度运行，在精度与效率之间取得了突出平衡。



从单目视频中恢复准确、平滑且世界坐标系一致的3D人体运动是计算机视觉的核心挑战之一，在AR/VR、运动分析、人机交互等领域具有广泛应用。近年来，基于单帧图像的人体姿态与形状（HPS）估计方法取得了长足进步，代表性工作如 **HMR2.0** 和 **CLIFF** 等在标准基准上实现了令人印象深刻的每帧精度。然而，这些方法逐帧独立预测，缺乏时间一致性约束，导致输出运动存在明显抖动，加速度误差（Accel）普遍高达 18–31 m/s²。

为引入时间平滑性，视频类方法如 **TCMR**、**GLoT** 等利用时序上下文建模，有效降低了加速度误差。但它们面临两个关键瓶颈：**第一**，现有视频方法在每帧精度指标（如 MPJPE、PA-MPJPE）上仍普遍弱于单帧方法，说明时间建模尚未有效转化为姿态估计精度提升；**第二**，绝大多数方法在相机坐标系中估计人体运动，当相机本身发生运动时，无法恢复人体在真实世界中的全局轨迹。

全局轨迹估计方面，**TRACE** 直接从运动特征回归全局根位移，但忽略了足部与地面的接触约束，导致严重的足部滑动（Foot Sliding 高达 370.7 mm）。**SLAHMR** 采用后优化策略，通过物理约束细化轨迹，但运行速度极慢（<0.1 fps），难以满足实时应用需求。**GLAMR** 虽能处理遮挡场景下的全局人体网格恢复，但在动态相机下的轨迹精度和足部接触合理性上仍有较大提升空间。

综合来看，现有方法的核心缺口在于：**难以在动态相机下同时实现全局坐标系中准确、平滑且无足部滑动的3D人体运动估计，且视频方法的准确率普遍低于单帧方法**。这暴露了两个深层问题：一是如何有效融合运动上下文与视觉外观信息以提升姿态估计精度，二是如何在缺乏绝对位置观测的情况下，利用足部接触等物理先验约束全局轨迹。

WHAM 正是针对上述缺口提出的解决方案。其核心动机在于：利用大规模运动捕捉数据（AMASS）生成的合成2D关键点序列预训练运动先验，再通过特征集成器融合图像上下文以提升精度，同时引入相机角速度辅助的轨迹解码与接触感知细化，从根本上解决足部滑动问题，实现在线、高效且准确的全局3D人体运动重建。



## 核心方法与创新机理

WHAM 的核心创新在于**系统性地解决了动态相机下全局人体运动重建的两个根本矛盾**：运动上下文与视觉上下文的融合，以及全局轨迹精度与足部物理一致性的协调。相较于现有方法，WHAM 在以下四个关键维度上实现了突破。

### 1. 运动-视觉双流特征集成

现有方法在特征表示上存在明显割裂：基于视频的方法（如 **TCMR**、**GLoT**）仅依赖 2D 关键点序列提取运动上下文，缺乏像素级视觉信息；而单帧方法（如 **HMR2.0**）虽利用图像特征，却无法建模时间连续性。WHAM 首次通过**特征集成器**（Feature Integrator）将两者有机融合：

$$
\hat{\phi}_m^{(t)} = \phi_m^{(t)} + F_I(\text{concat}(\phi_m^{(t)}, \phi_i^{(t)}))
$$

其中 $\phi_m^{(t)}$ 为运动编码器从 2D 关键点序列提取的运动上下文，$\phi_i^{(t)}$ 为预训练图像编码器（如 HMR2.0）的单帧外观特征。这种残差式融合设计使 WHAM 既能保持时间平滑性，又能实现像素对齐的精确重建——消融实验表明，移除特征集成后 PA-MPJPE 从 35.9 升至 44.2 mm（Table 4）。

### 2. 接触感知的全局轨迹细化

现有全局轨迹估计方法（如 **TRACE**）直接从运动特征回归根位移，完全忽略足部-地面接触约束，导致严重的足部滑动。WHAM 引入了**两阶段轨迹估计与细化机制**：

- **轨迹解码器** $D_T$ 利用运动特征 $\phi_m^{(t)}$ 和相机角速度 $\omega^{(t)}$ 初步预测全局根方向 $\Gamma_0^{(t)}$ 和自中心速度 $v_0^{(t)}$。
- **轨迹细化网络** $R_T$ 根据局部运动解码器预测的足部接触概率 $p^{(t)}$ 进行速度修正：

$$
\tilde{v}^{(t)} = v_0^{(t)} - (\Gamma_0^{(t)})^{-1} \bar{v}_f^{(t)}
$$

其中 $\bar{v}_f^{(t)}$ 为接触帧中足部相对于根的平均速度。这一机制将足部滑动（FS）从 TRACE 的 370.7 mm 降至 4.4 mm（Table 3），同时保持了轨迹精度。

### 3. 大规模合成数据驱动的两阶段训练

现有视频方法受限于真实标注数据的稀缺性。WHAM 创新性地采用**两阶段训练策略**：
- **预训练阶段**：从 AMASS 运动捕捉数据库生成大规模合成 2D 关键点序列，训练运动编码器-解码器的 2D-to-3D 提升能力。
- **微调阶段**：在有限视频数据集（3DPW、Human3.6M 等）上训练特征集成器并微调运动模块。

消融实验证实，移除 2D-to-3D 提升预训练会导致 PA-MPJPE 从 35.9 急剧上升至 60.3 mm（Table 4），证明合成数据预训练是 WHAM 高精度的关键基础。

### 4. 单向 RNN 实现高效在线推理

与 **TCMR** 等使用双向 RNN 的方法不同，WHAM 采用**单向 RNN** 架构，使其能以 200 fps 的核心速度进行在线推理，显著快于基于优化的 **SLAHMR**（<0.1 fps）。这使 WHAM 成为首个同时满足高精度、全局一致性、物理合理性和实时性要求的 3D 人体运动重建方法。



WHAM 采用在线推理架构，以视频帧序列为输入，端到端输出相机坐标系下的精确 3D 人体姿态与形状，以及世界坐标系下的全局轨迹。其核心设计遵循“运动上下文与视觉上下文融合”的理念，通过单向循环神经网络实现逐帧递归预测，避免了对未来帧的依赖，从而支持实时应用。

### 输入与预处理

WHAM 的输入包含两个并行流。第一条流是 2D 关键点序列，由预训练的 2D 关键点检测器（ViTPose）从每一帧中提取。第二条流是原始视频帧，由冻结权重的预训练图像编码器（如 HMR2.0 的主干网络）提取单帧外观特征。此外，WHAM 还利用外部 SLAM 方法（如 DPVO）或惯性测量单元（IMU）提供的相机角速度 $\omega^{(t)}$，作为全局轨迹估计的辅助信号。

### 流水线模块与数据流

WHAM 的整体流水线由七个核心模块串联构成，数据流严格遵循“运动编码→特征融合→局部解码→轨迹解码→轨迹细化”的路径（Figure 2）。

![[assets/figures/papers/paper_list_l18_WHAM_Reconstructing_World_grounded_Humans_with_Accurate_3D_Motion_motion20v2/figures/002_Figure_2.jpg]]
*Figure 2: An Overview of WHAM. WHAM takes the sequence of 2D keypoints estimated by a pretrained detector and encodes it into a motion feature. WHAM then updates the motion feature using another sequence of image features extracted from the image encoder through the feature integrator. From the updated motion feature, the Local Motion Decoder estimates 3D motion in the camera coordinate system and foot-ground contact probability. The Trajectory Decoder takes the motion feature and camera angular velocity to initially estimate the global root orientation and egocentric velocity, which are then updated through the Trajectory Refiner using the foot-ground contact. The final output of WHAM is pixel-align...*

**运动编码器 $E_M$** 接收当前帧及历史帧的 2D 关键点序列，通过单向 RNN 提取运动上下文特征 $\phi_m^{(t)}$。该特征编码了人体关节随时间变化的动态信息，是后续所有预测的基础。

**特征集成器 $F_I$** 是 WHAM 实现运动-视觉融合的关键模块。它将运动上下文 $\phi_m^{(t)}$ 与图像编码器提取的外观特征 $\phi_i^{(t)}$ 拼接后，通过残差连接生成增强的运动特征 $\hat{\phi}_m^{(t)}$。这一设计使模型既能利用 2D 关键点序列中的时序运动先验，又能从像素级视觉信息中获取精细的空间对齐线索。

**局部运动解码器 $D_M$** 从增强特征序列中预测相机坐标系下的 SMPL 参数（姿态 $\theta^{(t)}$、形状 $\beta^{(t)}$）、相机平移 $c^{(t)}$ 以及足部-地面接触概率 $p^{(t)}$。该模块同样采用单向 RNN，保证在线推理的一致性。

**轨迹解码器 $D_T$** 以运动特征 $\phi_m^{(t)}$ 和相机角速度 $\omega^{(t)}$ 为输入，初步估计全局根方向 $\Gamma_0^{(t)}$ 和自中心根速度 $v_0^{(t)}$。相机角速度的引入使模型能够区分人体自身运动与相机运动，是全局轨迹估计准确性的重要保障。

**轨迹细化网络 $R_T$** 利用局部运动解码器输出的足部接触概率 $p^{(t)}$，对初步速度进行接触感知调整。其核心思想是：当足部与地面接触时，足部在全局坐标系中的速度应趋近于零。通过从自中心速度中减去接触足部的平均速度，得到细化后的根速度 $\tilde{v}^{(t)}$，从而有效抑制足部滑动伪影。最终，全局平移 $\tau^{(t)}$ 通过累积细化后的根方向与速度计算得到。

### 训练策略

WHAM 采用两阶段训练方案（Figure 3）。第一阶段在 AMASS 运动捕捉数据集上进行 2D-to-3D 提升预训练：从 AMASS 生成合成 2D 关键点序列，训练运动编码器 $E_M$ 和局部运动解码器 $D_M$，使模型学习从 2D 关键点到 3D 姿态的映射。第二阶段在真实视频数据集（3DPW、MPI-INF-3DHP、Human3.6M、InstaVariety）上微调，引入冻结权重的图像编码器和关键点检测器，训练特征集成器 $F_I$ 并联合微调运动编码器与解码器。这种策略有效缓解了真实视频标注数据稀缺的问题，同时保留了大规模运动捕捉数据中的运动先验。

![[assets/figures/papers/paper_list_l18_WHAM_Reconstructing_World_grounded_Humans_with_Accurate_3D_Motion_motion20v2/figures/003_Figure_3.jpg]]
*Figure 3: WHAM’s Two-Stage Training Scheme. During pretaining, we generate synthetic 2D keypoint sequences from AMASS [32] and train a motion encoder and decoder on the generated data (top). We then leverage video datasets with ground truth SMPL parameters, for which there is much less data. We use the fixedweight pre-trained image encoder and keypoints detector ( ) to extract image features and 2D keypoints. In this stage, we train the feature integration network while fine-tuning the motion encoder and motion/trajectory decoders, marked (bottom)*



WHAM 采用在线推理架构，通过单向循环神经网络（RNN）对视频帧进行逐帧处理，递归地预测 SMPL 参数、相机平移和全局运动参数。其核心设计围绕三个关键模块展开：运动上下文提取、运动-图像特征融合，以及接触感知的全局轨迹估计。

### 运动编码器与局部运动解码器

运动编码器 $E_M$ 从预训练的 2D 关键点检测器（ViTPose）输出的关键点序列中提取运动上下文。给定当前帧及历史帧的 2D 关键点序列，编码器通过单向 RNN 递归更新隐藏状态，生成当前帧的运动特征 $\phi_m^{(t)}$：

$$\phi_m^{(t)} = E_M(x_{2D}^{(0)}, x_{2D}^{(1)}, ..., x_{2D}^{(t)} | h_E^{(0)})$$

其中 $x_{2D}^{(t)}$ 为第 $t$ 帧的 2D 关键点，$h_E^{(0)}$ 为编码器初始隐藏状态。单向 RNN 的设计使 WHAM 无需未来帧即可进行推理，保证了在线处理的低延迟特性（核心速度约 200 fps）。

局部运动解码器 $D_M$ 以增强后的运动特征序列为输入，同样通过单向 RNN 递归预测当前帧的 SMPL 姿态参数 $\theta^{(t)}$、体型参数 $\beta^{(t)}$、相机坐标系下的平移 $c^{(t)}$ 以及足部-地面接触概率 $p^{(t)}$：

$$(\theta^{(t)}, \beta^{(t)}, c^{(t)}, p^{(t)}) = D_M(\hat{\phi}_m^{(0)}, ..., \hat{\phi}_m^{(t)} | h_D^{(0)})$$

### 特征集成器

特征集成器 $F_I$ 是 WHAM 实现运动上下文与视觉上下文融合的关键组件。对于每一帧，预训练的图像编码器（如 HMR2.0）从 RGB 图像中提取外观特征 $\phi_i^{(t)}$。集成器将运动特征 $\phi_m^{(t)}$ 与图像特征拼接后，通过残差连接更新运动特征，生成增强的运动特征 $\hat{\phi}_m^{(t)}$：

$$\hat{\phi}_m^{(t)} = \phi_m^{(t)} + F_I(\text{concat}(\phi_m^{(t)}, \phi_i^{(t)}))$$

这一设计的核心优势在于：运动编码器从 2D 关键点序列中捕获时序运动先验，而图像特征提供像素级的外观线索（如衣物纹理、遮挡边界），两者互补使得 WHAM 在保持时序平滑性的同时，实现了像素对齐的精确 3D 姿态估计。消融实验证实，移除特征集成器会导致 PA-MPJPE 从 35.9 上升至 44.2，MPJPE 从 54.9 上升至 69.0（见 Table 4）。

### 轨迹解码器与接触感知细化

轨迹解码器 $D_T$ 负责初步估计人体的全局根方向 $\Gamma_0^{(t)}$ 和自中心速度 $v_0^{(t)}$。为增强相机运动的感知能力，WHAM 将相机角速度 $\omega^{(t)}$（由 SLAM 方法如 DPVO 或陀螺仪提供）与运动特征拼接后输入解码器：

$$(\Gamma_0^{(t)}, v_0^{(t)}) = D_T(\phi_m^{(0)}, \omega^{(0)}, ..., \phi_m^{(t)}, \omega^{(t)})$$

相机角速度的引入使轨迹解码器能够区分人体自身运动与相机运动，消融实验表明移除角速度输入会导致相对平移误差 RTE 从 6.0 上升至 10.1（见 Table 4）。

轨迹细化网络 $R_T$ 利用局部运动解码器预测的足部接触概率 $p^{(t)}$ 对自中心速度进行接触感知调整。其核心思想是：当足部与地面接触时，足部在世界坐标系中的速度应接近零。据此，网络计算足部在自中心坐标系中的期望速度 $\bar{v}_f^{(t)}$，并对初步估计的速度进行修正：

$$\tilde{v}^{(t)} = v_0^{(t)} - (\Gamma_0^{(t)})^{-1} \bar{v}_f^{(t)}$$

最终，全局平移 $\tau^{(t)}$ 通过累积细化后的根方向与速度得到：

$$\tau^{(t)} = \sum_{i=0}^{t-1} \Gamma^{(i)} v^{(i)}$$

接触感知细化显著减少了足部滑动现象：在 EMDB 2 基准上，移除该模块后足部滑动指标 FS 从 4.4 mm 上升至 6.5 mm（见 Table 4）。需要指出的是，当前接触估计仅考虑足部，无法处理手部支撑等身体其他部位的接触场景，这是 WHAM 的一个已知局限。



## 实验与关键发现

### 核心性能验证

WHAM 在多个基准数据集上全面验证了其每帧精度与全局轨迹估计能力。Table 1 报告了在 3DPW、RICH 和 EMDB 数据集上的每帧精度对比，WHAM (ViT) 在所有指标上均优于先前方法。具体而言，在 3DPW 上，WHAM 的 PA-MPJPE 达到 35.9 mm，相比单帧 SOTA 方法 HMR2.0 的 44.4 mm 降低了 8.5 mm；加速度误差 (Accel) 仅为 6.6 m/s²，远低于 HMR2.0 的 18.1 m/s²，降幅达 11.5 m/s²。这一结果直接验证了特征集成器融合运动上下文与图像上下文的有效性——仅使用图像特征的单帧方法虽然逐帧对齐能力强，但缺乏时间一致性，导致加速度误差显著偏高。

![[assets/figures/papers/paper_list_l18_WHAM_Reconstructing_World_grounded_Humans_with_Accurate_3D_Motion_motion20v2/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of state-of-the-art models on the 3DPW [49], RICH [10], and EMDB [16] datasets. Ordering of per-frame and temporal methods is done separately by descending MPJPE on EMDB (except for PACE). For testing on EMDB, we follow the protocol of EMDB 1 [16]. Parenthesis denotes the number of body joints used to compute MPJPE and PA-MPJPE, and ∗ denotes models trained with the 3DPW training set. Bold numbers denote the most accurate method in each column. Accel is in*

在全局轨迹估计方面，Table 3 展示了 EMDB 数据集上的定量结果。WHAM (w/ DPVO) 的 W-MPJPE100 为 354.8 mm，相比 DPVO+HMR2.0 组合的 2231.4 mm 降低了 1876.6 mm；轨迹抖动 (Jitter) 从 TRACE 的 2987.6 (10m/s³) 降至 22.5，降幅达 2965.1；足部滑动 (Foot Sliding) 从 TRACE 的 370.7 mm 降至 4.4 mm，降幅达 366.3 mm。这些指标的显著改善表明，接触感知轨迹细化策略有效消除了全局运动中的足部滑动伪影，而相机角速度的引入为轨迹解码器提供了关键的相机运动先验。

![[assets/figures/papers/paper_list_l18_WHAM_Reconstructing_World_grounded_Humans_with_Accurate_3D_Motion_motion20v2/figures/007_Table_3.jpg]]
*Table 3: Global motion estimation accuracy on EMDB [16]*

Figure 4 的定性对比进一步印证了定量结果：与 TCMR、GLoT 等视频方法相比，WHAM 重建的人体姿态在像素对齐精度和时序平滑性上均表现出明显优势。Figure 5 和 Figure 6 则聚焦于全局轨迹估计，显示 WHAM 在动态相机场景下能够生成与真值高度一致的全局运动路径，而 TRACE 和 SLAHMR 则出现明显的轨迹漂移和足部滑动。

![[assets/figures/papers/paper_list_l18_WHAM_Reconstructing_World_grounded_Humans_with_Accurate_3D_Motion_motion20v2/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison with previous state-of-the-art methods for 3D human pose and shape estimation. See text*

![[assets/figures/papers/paper_list_l18_WHAM_Reconstructing_World_grounded_Humans_with_Accurate_3D_Motion_motion20v2/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative comparison with TRACE [45] and SLAHMR [55] on global human motion estimation with dynamic cameras*

![[assets/figures/papers/paper_list_l18_WHAM_Reconstructing_World_grounded_Humans_with_Accurate_3D_Motion_motion20v2/figures/009_Figure_6.jpg]]
*Figure 6: Comparison of global trajectory estimation on EMDB [16]. Overall, WHAM shows better alignment to ground truth data compared to GLAMR [58], TRACE [45], and SLAHMR [55]*

### 消融实验分析

Table 4 的系统消融实验揭示了 WHAM 各核心组件的贡献机制：

![[assets/figures/papers/paper_list_l18_WHAM_Reconstructing_World_grounded_Humans_with_Accurate_3D_Motion_motion20v2/figures/010_Table_4.jpg]]
*Table 4: Ablation experiments. See text*

**特征集成器 (Feature Integrator)**：移除特征集成（w/o FI）后，PA-MPJPE 从 35.9 上升至 44.2，MPJPE 从 54.9 上升至 69.0，RTE 从 6.0 上升至 6.3。这表明单纯依赖运动上下文（2D 关键点序列）无法充分利用图像中的外观细节，导致像素对齐精度下降；而仅依赖图像特征则缺乏时间运动先验，全局轨迹估计亦受影响。

**2D-to-3D 提升预训练**：移除 AMASS 上的预训练阶段（w/o lifting）造成最严重的性能退化——PA-MPJPE 从 35.9 急剧上升至 60.3，MPJPE 从 54.9 升至 83.0。这证实了大规模运动捕捉数据生成的合成 2D 关键点序列对于学习鲁棒的 2D-to-3D 提升映射至关重要，有限的视频数据集无法提供足够的运动多样性。

**相机角速度**：移除相机角速度输入（w/o ω）导致 RTE 从 6.0 上升至 10.1，但对每帧精度影响较小。这说明相机运动信息对于区分人体自身运动与相机运动具有不可替代的作用，其缺失直接导致全局轨迹估计的严重退化。

**轨迹细化网络**：移除接触感知轨迹细化（w/o traj. ref.）后，足部滑动从 4.4 mm 上升至 6.5 mm，RTE 从 6.0 上升至 6.3。Figure 7 的定性消融对比直观展示了这一模块的作用：无细化时，人体在足部接触地面期间仍出现明显的滑移伪影，而完整的 WHAM 能够生成物理上合理的足部着地效果。

Table 2 的数据集消融实验表明，引入 BEDLAM 合成数据集进行训练可进一步提升精度，验证了数据多样性对模型泛化能力的积极影响。

![[assets/figures/papers/paper_list_l18_WHAM_Reconstructing_World_grounded_Humans_with_Accurate_3D_Motion_motion20v2/figures/006_Table_2.jpg]]
*Table 2: Dataset ablation experiments on 3DPW [49]. R denotes the use of real datasets and B denotes BEDLAM*

### 推理效率

Table 5 报告了 WHAM 各模块的逐帧计算时间。核心推理管线（不含预处理）达到约 200 fps，显著快于基于优化的 SLAHMR（<0.1 fps）。这一效率优势源于 WHAM 采用单向 RNN 实现在线推理，避免了全局优化或双向时间建模带来的计算开销。

![[assets/figures/papers/paper_list_l18_WHAM_Reconstructing_World_grounded_Humans_with_Accurate_3D_Motion_motion20v2/figures/011_Table_5.jpg]]
*Table 5: Per-frame computation time (running time) of each module in WHAM. We present this both as frames per second (fps) and milliseconds (ms)*

### 失败模式与局限性

Figure 8 展示了 WHAM 在全局运动估计中的典型失败案例。分析表明，WHAM 在以下场景中存在明显局限：

![[assets/figures/papers/paper_list_l18_WHAM_Reconstructing_World_grounded_Humans_with_Accurate_3D_Motion_motion20v2/figures/013_Figure_8.jpg]]
*Figure 8: Failure cases of WHAM in global motion estimation*

1. **未覆盖的运动模式**：当输入视频包含 AMASS 数据集中未涵盖的活动（如滑板、骑自行车）时，全局轨迹估计出现显著偏差。这是因为运动编码器在预训练阶段未学习到此类运动的 2D-to-3D 映射关系，导致运动特征质量下降，进而影响轨迹解码器的预测精度。

2. **非足部接触场景**：接触感知轨迹细化仅考虑足部与地面的接触概率，无法处理身体其他部位（如手部、膝盖）的支撑接触。在涉及手部支撑的动作中，模型可能生成物理上不合理的人体支撑姿态。这一局限源于接触概率预测仅针对足部关节设计，扩展至全身接触需要额外的标注数据和模型架构调整。

3. **部分遮挡**：训练数据的合成假设人体始终完全在视野内，导致模型对部分遮挡场景的泛化能力有限。当人体被场景物体严重遮挡时，2D 关键点检测器可能产生错误估计，进而通过运动编码器传播至整个管线。

4. **相机角速度依赖**：全局轨迹估计依赖于 SLAM 或陀螺仪提供的相机角速度。若此信息缺失或估计不准（例如在低纹理环境中 SLAM 失效），轨迹解码器的预测精度将受到影响。Table 3 中使用 DPVO 估计角速度的结果（W-MPJPE100 为 354.8）略逊于使用 GT 陀螺仪的结果（335.3），印证了这一依赖关系。

### 实验公平性说明

为确保公平比较，所有标记 ∗ 的方法（包括 WHAM）均使用了 3DPW 训练集进行训练。各基线方法均按照其原始论文的评估协议在标准基准上测试，未对测试数据进行额外微调。

### 补充图表

![[assets/figures/papers/paper_list_l18_WHAM_Reconstructing_World_grounded_Humans_with_Accurate_3D_Motion_motion20v2/figures/012_Figure_7.jpg]]
*Figure 7: Qualitative comparison between WHAM and after removal of contact-aware trajectory refinement (w/o traj. ref.)*



## 定位与知识库关联

### 问题定位与因果瓶颈

从视频中恢复三维人体姿态与运动（3D Human Pose and Shape estimation, 3D HPS）存在两条技术路线：**单帧回归方法**（如 **HMR2.0**、**CLIFF**）逐帧独立预测，精度较高但时间一致性差，表现为加速度误差（Accel）高达 18–31 m/s²；**视频时序方法**（如 **TCMR**、**GLoT**）利用时间上下文平滑运动，但全局轨迹估计能力薄弱，尤其在动态相机下无法消除足部滑动（Foot Sliding）。核心瓶颈在于：现有方法难以在**动态相机**下同时实现**全局坐标系中准确、平滑且无足部滑动的 3D 人体运动估计**，且视频方法的每帧准确率普遍低于单帧方法。

### 核心洞察与因果旋钮

WHAM 的核心洞察是：**运动上下文与视觉上下文是互补的**——2D 关键点序列蕴含强时序运动先验，但缺乏像素级空间精度；图像特征提供精确的空间对齐，但缺乏长程运动理解。WHAM 通过以下因果旋钮突破瓶颈：

1. **特征集成器（Feature Integrator）**：将运动编码器提取的运动上下文与图像编码器提取的外观特征融合，使 3D 回归同时具备时序平滑性和像素对齐精度。
2. **接触感知轨迹细化（Contact-aware Trajectory Refinement）**：利用预测的足部接触概率调整全局根速度，显式消除足部滑动。
3. **两阶段训练策略**：在大规模 AMASS 运动捕捉数据上合成 2D 关键点序列预训练运动编码器-解码器，解决视频 3D 标注数据稀缺问题。

### 在方法谱系中的位置

WHAM 位于**回归式视频 3D 人体运动重建**与**全局轨迹估计**的交汇点，其设计融合了以下谱系的优势：

| 方法谱系 | 代表工作 | 与 WHAM 的关系 |
|---|---|---|
| 单帧回归 | **HMR2.0** (CVPR 2023) | WHAM 复用其图像编码器作为视觉特征提取器，并通过特征集成弥补其缺乏时间上下文的缺陷 |
| 视频时序回归 | **TCMR** (CVPR 2021), **GLoT** (ICCV 2023) | WHAM 采用类似的时序建模思路，但使用单向 RNN 实现在线推理，并进一步扩展到全局轨迹估计 |
| 2D-to-3D Lifting | **MotionBERT** (ICCV 2023) | WHAM 借鉴从 2D 关键点序列提升到 3D 的思路，但通过 AMASS 合成数据预训练解决了 3D 标注稀缺问题 |
| 全局轨迹估计 | **TRACE** (CVPR 2023), **GLAMR** (CVPR 2022) | WHAM 在 TRACE 的回归框架上引入相机角速度辅助和接触感知细化，显著降低足部滑动和轨迹漂移 |
| 基于优化的方法 | **SLAHMR** (CVPR 2023) | WHAM 以 200 fps 的在线推理速度实现了与离线优化方法相当甚至更优的全局轨迹精度 |

### 关键设计决策与消融验证

消融实验（Table 4）揭示了各组件的因果贡献：

- **移除特征集成（w/o FI）**：PA-MPJPE 从 35.9 上升至 44.2，MPJPE 从 54.7 上升至 69.0，RTE 从 6.0 上升至 6.3。表明运动-视觉特征融合对每帧精度和轨迹精度均有实质性贡献。
- **移除 2D-to-3D 提升预训练（w/o lifting）**：PA-MPJPE 大幅上升至 60.3，MPJPE 升至 83.0。这是影响最大的单一组件，验证了 AMASS 合成数据预训练对于学习鲁棒运动先验的关键作用。
- **移除相机角速度（w/o ω）**：RTE 从 6.0 上升至 10.1，表明相机角速度为轨迹解码器提供了关键的相机运动解耦信息。
- **移除轨迹细化（w/o traj. ref.）**：足部滑动 FS 从 4.4 上升至 6.5，RTE 上升至 6.3，验证了接触感知速度调整对消除足部滑动的有效性。

### 适用边界与局限

WHAM 在以下条件下表现优越：
- 相机运动信息（角速度）可通过 SLAM（如 DPVO）或 IMU 陀螺仪获取；
- 人体运动模式在 AMASS 训练分布内（行走、跑步、站立、坐下等日常动作）；
- 人体基本完整可见于画面中。

已知局限包括：
1. **运动模式泛化**：训练数据未涵盖的活动（如滑板、骑自行车）上全局轨迹估计不佳（Figure 8 失败案例）。
2. **接触建模范围**：仅考虑足部-地面接触，无法处理手部支撑、膝盖着地等全身接触场景，可能导致物理上不合理的人体支撑。
3. **遮挡鲁棒性**：训练数据合成假设人体始终完整可见，对部分遮挡情况的泛化能力有限。
4. **相机角速度依赖**：全局轨迹估计依赖外部提供的相机角速度，若此信息缺失或不准，轨迹精度可能下降（Table 3 中 WHAM w/ DPVO 的 W-MPJPE100 为 354.8，而 w/ GT gyro 为 335.3）。

### 开放问题

1. 如何扩展运动先验以覆盖 AMASS 之外的复杂运动模式（如滑板、骑车、体操）？
2. 能否利用更丰富的场景信息（如稠密 3D 重建或单目深度估计）进一步提升全局一致性？
3. 接触感知细化能否从足部扩展到全身接触点（手、膝盖、臀部），以支持更广泛的交互场景？
4. 在完全没有相机角速度信息的情况下，WHAM 的轨迹估计能否通过纯视觉线索保持鲁棒？



## 原文 PDF

![[paperPDFs/CVPR_2024/WHAM_Reconstructing_World_grounded_Humans_with_Accurate_3D_Motion.pdf]]
