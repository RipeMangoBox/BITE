---
title: A Unified Model for Egocentric Motion Reconstruction Forecasting and Generation
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/A_Unified_Model_for_Egocentric_Motion_Reconstruction_Forecasting_and_Generation.pdf
project_link: https://chaitanya100100.github.io/UniEgoMotion/
code_link: null
aliases:
- UMEMRFG
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: UniEgoMotion 通过统一的扩散模型训练框架（随机掩码条件输入模拟重建、预测和生成任务），引入预训练 DINOv2 图像编码器提取细粒度场景特征，并采用头部中心的运动表示（地板投影与残差轨迹），从根本上弥合了第一人称视觉输入与 3D 运动合成之间的鸿沟。
primary_logic: 将条件掩码策略与强视觉骨干相结合，使单一模型能够灵活适配重建、预测和生成三种任务；头部中心表示通过地板投影正则化增强了运动物理合理性，优于传统骨盆中心或全局表示。
claims:
- UniEgoMotion 在第一人称重建任务上全面超越 AvatarPoser、EgoEgo 和 EgoAllo，MPJPE 从 0.116 降至 0.100，语义相似度从 0.872 提升至 0.918，FID 从 0.043 降至 0.027。
- 在第一人称预测和生成任务中，UniEgoMotion 的足部滑移和接触指标显著优于两阶段基线，同时生成更丰富、场景合理的运动（如图 4、5 所示）。
- 使用预训练 DINOv2 编码器（细粒度特征）比 CLIP 或 EgoVideo 编码器带来明显提升，验证了场景上下文提取的重要性。
- 头部中心运动表示有效减少脚部滑移和地板穿透，相比骨盆中心表示，MPJPE 从 0.166 降至 0.100，足部接触误差从 0.028 降至 0.027。
---

# A Unified Model for Egocentric Motion Reconstruction Forecasting and Generation

> [!tip] 核心洞察
> 将条件掩码策略与强视觉骨干相结合，使单一模型能够灵活适配重建、预测和生成三种任务；头部中心表示通过地板投影正则化增强了运动物理合理性，优于传统骨盆中心或全局表示。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向第一人称运动重建、预测与生成的统一模型 |
| 英文题名 | A Unified Model for Egocentric Motion Reconstruction Forecasting and Generation |
| 会议/期刊 | ICCV 2025 |
| Links | [Project](https://chaitanya100100.github.io/UniEgoMotion/) · [paper](https://arxiv.org/abs/2508.01126) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | UniEgoMotion |
| Dataset | EE4D‑Motion |

> [!tip] 效果简介
> - EE4D‑Motion (基于 EgoExo4D 的自建第一人称视频‑运动数据集) 上，MPJPE (m) – 重建全局关节误差 0.100 vs 0.116 (AvatarPoser) (-0.016)。
> - EE4D‑Motion 上，Foot Slide – 预测足部滑移 (2‑4s) 2.60 vs 3.55 (Two‑stage) (-0.95)；Foot Slide – 生成足部滑移 (0‑2s) 2.89 vs 4.35 (Two‑stage) (-1.46)。

## 概要

第一人称 (egocentric) 运动理解在 AR/VR、人机交互与具身智能中至关重要，但现有方法普遍忽略图像中的场景语义信息，无法仅从单张第一人称图像生成或预测运动；同时，传统的骨盆中心运动表示与头戴设备输入不匹配，易引发脚部滑移和穿地等物理不合理现象。

针对上述瓶颈，**UniEgoMotion** 提出一个统一的、场景感知的扩散模型框架，其核心调控机制包括三方面：(1) **统一的条件掩码训练策略**——训练时随机将条件输入替换为可学习掩码令牌，模拟重建、预测与生成三种任务，使单一模型灵活适配不同推理场景；(2) **预训练 DINOv2 图像编码器**——提取细粒度场景上下文特征，通过交叉注意力注入 Transformer 解码器，弥补第一人称视觉与 3D 运动之间的语义鸿沟；(3) **头部中心运动表示**——将头部 SE(3) 全局变换投影至地板建立规范参考系，轨迹编码为帧间残差，体态编码为相对局部信息，从根本上增强运动物理合理性。

实验在基于 EgoExo4D 构建的 **EE4D‑Motion** 数据集上进行。在重建任务上，UniEgoMotion 全面超越 **AvatarPoser**、**EgoEgo** 和 **EgoAllo**，MPJPE 从 0.116 m 降至 0.100 m，语义相似度从 0.872 提升至 0.918，FID 从 0.043 降至 0.027。在预测与生成任务中，足部滑移和接触指标显著优于两阶段扩散基线，同时生成更丰富、场景合理的运动序列。消融实验证实，头部中心表示相较骨盆中心表示使 MPJPE 降低 0.066，DINOv2 编码器优于 CLIP 和 EgoVideo 编码器，验证了场景上下文提取与运动表示设计的关键作用。

**方法定位**：UniEgoMotion 属于条件扩散运动生成方法族，与现有第一人称运动重建/预测工作（AvatarPoser、EgoEgo、EgoAllo）相比，其差异化在于统一任务框架、强视觉骨干与头部中心运动表示的协同设计。该方法弥合了第一人称视觉输入与 3D 运动合成之间的根本性鸿沟，为后续场景‑运动交互建模和文本驱动生成奠定了基础。

### 第一人称 3D 运动理解的现实需求

头戴式摄像头（如智能眼镜、AR/VR 头显）的普及正在催生对第一人称（egocentric）3D 人体运动理解技术的迫切需求。与传统的第三人称运动捕捉不同，第一人称视角下的运动重建、预测与生成面临独特的挑战：输入信号来自佩戴者自身的视觉传感器和惯性测量单元（IMU），而非外部固定相机。这种设置使得系统必须从有限的、以自我为中心的观察中推断完整的全身 3D 运动。

具体而言，该领域涉及三个核心任务：（1）**运动重建**——从过去的第一人称视频和头戴设备轨迹中恢复准确的 3D 人体运动；（2）**运动预测**——基于观察到的过去运动，预测未来的运动序列；（3）**运动生成**——仅从单张第一人称图像出发，生成合理的未来运动。Figure 1 展示了这三类任务的典型应用场景：从单张图像生成射门动作、从过去视频预测跑动轨迹、以及从观察中重建下蹲取物的精确运动。

### 现有方法的双重瓶颈

当前第一人称运动方法存在两个根本性瓶颈，严重制约了其性能上限。

**瓶颈一：场景语义信息的系统性缺失。** 现有方法普遍忽略第一人称图像中蕴含的丰富场景上下文。**AvatarPoser** 和 **EgoEgo** 等重建方法主要依赖头戴设备的 6-DOF 轨迹信号，仅将图像作为辅助线索甚至完全忽略；而 **EgoAllo** 虽引入了图像条件，但其编码器设计未能充分提取细粒度场景特征。这使得模型在面对复杂场景时（如狭窄空间、障碍物附近）无法做出物理上合理的运动推断——例如，当佩戴者靠近墙壁时，模型可能生成穿墙的手臂动作。更关键的是，这种场景感知能力的缺失使得仅从单张第一人称图像生成运动的任务几乎不可行，因为模型缺乏推断环境约束和交互意图的视觉基础。

**瓶颈二：运动表示与输入模态的结构性错配。** 传统人体运动合成方法采用骨盆中心的运动表示——以人体骨盆为参考系描述全身运动。然而，第一人称设备的输入天然以头部为中心：头戴摄像头的位姿直接对应佩戴者头部的 6-DOF 变换，而非骨盆。这种表示层面的不匹配导致两个严重后果：（1）模型需要隐式学习头部到骨盆的复杂映射，增加了学习难度；（2）骨盆中心表示缺乏对地面约束的显式建模，容易引发脚部滑移（foot sliding）和地板穿透（floor penetration）等物理不合理现象。Figure 3 中的基线方法可视化结果清晰地展示了这些问题——AvatarPoser 和 EgoEgo 的重建结果出现明显的漂浮和穿地现象。

### 统一框架的动机与核心思路

上述瓶颈本质上源于一个更深层的架构缺陷：现有方法将重建、预测和生成视为三个独立任务，分别设计专用模型。这种分离式范式不仅效率低下，更关键的是割裂了场景理解与运动合成之间的内在联系——重建任务中习得的场景-运动关联无法迁移到生成任务中，反之亦然。

UniEgoMotion 的核心动机在于：**通过统一的扩散模型训练框架，将条件掩码策略与强视觉骨干相结合，使单一模型能够灵活适配重建、预测和生成三种任务；同时引入头部中心的运动表示，从根本上弥合第一人称视觉输入与 3D 运动合成之间的鸿沟。** 具体而言，训练时随机将条件输入（图像、轨迹）替换为可学习掩码令牌，模拟从完全观察到完全缺失的条件谱系；推理时使用掩码令牌填补缺失输入，实现单模型三任务的一致推理。在表示层面，将头部 SE(3) 变换投影至地板建立规范参考系，轨迹编码为帧间残差，体态编码为相对于该参考系的局部信息——这种设计不仅与头戴设备输入天然对齐，还通过地板投影正则化显式增强了运动的物理合理性。

## 核心方法与创新机理

UniEgoMotion 的核心创新并非单一技术点的突破，而是通过**三个相互耦合的设计变更**，系统性地解决了第一人称运动合成中长期存在的瓶颈：视觉输入与运动空间之间的语义鸿沟，以及传统运动表示与头戴设备输入之间的几何不匹配。

### 创新一：统一条件掩码训练框架

现有方法为重建、预测和生成任务分别设计独立模型，不仅增加了工程复杂度，更割裂了不同任务之间可共享的场景理解能力。UniEgoMotion 提出了一种**统一的条件扩散训练策略**：在训练过程中，随机将条件输入（第一人称图像序列 $I_{1:N}$ 或头部轨迹 $T_{1:N}$）替换为可学习的掩码令牌（learnable mask tokens），从而模拟从完整条件（重建）到完全缺失条件（生成）的两个极端。预测任务则通过扩散 inpainting 机制实现——以已知帧覆盖生成帧，保证时序一致性：

$$\hat{\boldsymbol X}_{1:N} \gets \mathrm{concat}(\boldsymbol X_{1:n}, \hat{\boldsymbol X}_{n+1:N})$$

这一设计的因果机制在于：模型被迫在同一个参数空间内学习从不同信息量条件中提取运动先验，使得场景理解能力可以在任务间迁移。当仅提供单张图像时，模型仍能调用在完整视频-轨迹条件下学到的“场景-运动”映射关系。

### 创新二：头部中心运动表示

传统运动合成方法普遍采用**骨盆中心表示**——以人体骨盆为参考系定义全局轨迹和局部姿态。然而，第一人称设备（如头戴式相机）获取的是头部运动信息，骨盆位置需要通过运动学链间接推断。这种表示与输入之间的不匹配导致两个典型失败模式：脚部滑移（foot sliding）和地板穿透（floor penetration）。

UniEgoMotion 将运动表示重构为**头部中心**的两分量分解（Figure 7）：
1. **规范轨迹**：将头部 SE(3) 全局变换中的俯仰角（pitch）、翻滚角（roll）和高度分量移除，投影至地板平面，建立稳定的规范参考系；
2. **相对体态**：各关节相对于该投影轨迹的局部信息，编码为帧间残差。

这一设计的核心洞察在于：**地板投影操作充当了隐式的物理正则化器**。通过强制轨迹在水平面上展开，模型天然地抑制了垂直方向的漂移和旋转累积误差。消融实验证实了其有效性：相比骨盆中心表示，头部中心表示将重建 MPJPE 从 0.166 降至 0.100（降幅 39.8%），足部接触误差从 0.028 降至 0.027（Table 1 消融行）。

### 创新三：预训练细粒度视觉编码器

先前方法或完全忽略第一人称图像中的场景信息，或使用轻量编码器提取粗粒度特征。UniEgoMotion 引入了**预训练 DINOv2 ViT** 作为图像编码器，通过交叉注意力机制将细粒度场景上下文注入 Transformer 解码器。

这一选择的因果逻辑在于：DINOv2 的自监督预训练使其能够捕获场景中的语义布局（如地面位置、障碍物边界、可交互物体），这些信息对于推断合理的 3D 运动至关重要。消融对比验证了这一点：将 DINOv2 替换为 CLIP 编码器，重建 FID 从 0.027 升至 0.041；替换为 EgoVideo 编码器，FID 升至 0.021（Table 1 消融行）。值得注意的是，DINOv2 的细粒度特征对生成任务尤为关键——仅从单张图像生成运动时，模型需要精确的场景几何线索来约束运动范围。

### 三个创新的协同效应

上述三个设计并非孤立生效。统一训练框架使头部中心表示和 DINOv2 编码器学到的特征在所有任务间共享；头部中心表示通过降低运动空间的学习难度，使得扩散模型能更有效地利用视觉特征；DINOv2 的强视觉表征则为掩码条件下的运动推断提供了更丰富的上下文。Table 3 的消融揭示了这种耦合关系：当移除视频输入时，语义相似度从 0.918 降至 0.878；当移除轨迹输入时，头部平移误差从 0.058 急剧升至 0.280，表明模型在缺失轨迹时被迫隐式解决视觉里程计问题，而这一能力高度依赖强视觉编码器。

### 需要人工验证的边界

分析中部分 baseline 方法（如 AvatarPoser、EgoEgo）的具体技术细节未在提供材料中充分展开，上述对比主要基于 UniEgoMotion 论文报告的数值。若需精确评估各创新点的独立贡献权重，建议对照原始 baseline 论文进行交叉验证。

UniEgoMotion 构建了一个以 Transformer 解码器为核心的条件扩散模型，将第一人称图像与头戴设备轨迹作为条件信号，统一处理运动重建、预测与生成三大任务。整体 pipeline 围绕“噪声运动→条件去噪→干净运动”的扩散范式展开，并通过随机掩码策略实现单模型多任务适配。

### 输入与输出定义

模型输入包含两类条件信号：**第一人称图像序列** $I_{1:N}$ 和**头戴设备 6-DOF 轨迹** $T_{1:N}$，其中 $N$ 为序列帧数（训练时使用 8 秒 10fps 片段，$N=80$）。输出为对应的 SMPL-X 运动参数序列 $X_{1:N}$，每帧参数包含根旋转 $R_i^r$、根平移 $t_i^r$、21 个关节的局部角度 $\theta_i$ 以及序列内共享的 10 维体型参数 $\beta_i$：

$$X_i = (R_i^r, t_i^r, \theta_i, \beta_i)$$

### 核心去噪流程

如图 2 所示，每个去噪步骤的核心计算为：给定噪声运动 $X_{1:N}^t$、扩散时间步 $t$ 和条件输入 $C$，模型 $\mathcal{M}$ 预测干净运动 $\hat{X}$：

$$\hat{\boldsymbol X} = \mathcal{M}(\boldsymbol X^t, t, \boldsymbol C; \boldsymbol \Theta)$$

前向过程按调度参数 $\bar{\alpha}_t$ 逐步加入高斯噪声：

$$q_t(\boldsymbol X^t | \boldsymbol X) = \mathcal{N}(\boldsymbol X^t; \sqrt{\bar{\alpha}_t} \boldsymbol X, (1 - \bar{\alpha}_t) \boldsymbol I)$$

训练时最小化干净运动与预测值之间的 MSE 损失：

$$\mathcal{L} = \mathbb{E}_{t \in [1, t_{max}], \boldsymbol X^t \sim q_t(\cdot | \boldsymbol X)} \left[ ||\boldsymbol X - \mathcal{M}(\boldsymbol X^t, t, \boldsymbol C)||_2^2 \right]$$

推理时从纯噪声出发，迭代执行去噪步骤直至恢复干净运动：

$$\boldsymbol X^{t-1} = \mathcal{M}(\boldsymbol X^t, t, \boldsymbol C) + \boldsymbol \epsilon_t$$

### 模块化架构

pipeline 由四个关键模块串联构成：

1. **DINOv2 图像编码器**：采用预训练 DINOv2 ViT 作为视觉骨干，从第一人称图像 $I_{1:N}$ 中提取细粒度场景上下文特征。该编码器仅微调投影网络，保留强大的预训练视觉表征能力，提取的特征通过交叉注意力注入下游 Transformer 解码器。

2. **Transformer 解码器**：以噪声运动序列 $X_{1:N}^t$ 作为输入，融合扩散时间步嵌入、轨迹特征和图像特征，预测干净运动。解码器架构相比编码器或 1D U-Net 展现出显著优势——消融实验表明，使用编码器或 1D U-Net 替代解码器会导致重建 MPJPE 上升约 0.015–0.045，验证了交叉注意力机制在条件融合中的关键作用。

3. **头部中心运动表示模块**：将 SMPL-X 参数转换为头部 SE(3) 全局变换，并通过地板投影建立规范参考系。具体而言，通过前向运动学获得头部与各关节的全局 SE(3) 变换 $(M_i^h, M_i^j)$，再将头部变换投影至地板（移除俯仰角、翻滚角和高度），得到规范轨迹 $_c M_i$。最终运动被分解为两部分：规范轨迹的帧间残差编码，以及相对于该参考系的局部体态信息。这一表示从根本上解决了传统骨盆中心表示与头戴设备输入不匹配的问题——消融实验中，头部中心表示相比骨盆中心表示将重建 MPJPE 从 0.166 降至 0.100，足部接触误差从 0.028 降至 0.027。

4. **条件掩码与任务统一模块**：训练时随机将条件输入（图像序列 $I_{1:N}$ 或轨迹 $T_{1:N}$）替换为可学习掩码令牌，模拟不同任务场景——$C = \{T_{1:N}, I_{1:N}\}$ 对应重建任务，$C = \{I_1\}$ 对应生成任务。预测任务则通过扩散 inpainting 实现：给定前 $n$ 帧观察，在去噪过程中用已知重建帧覆盖对应位置的生成帧，强制时序一致性：

   $$\hat{\boldsymbol X}_{1:N} \gets \mathrm{concat}(\boldsymbol X_{1:n}, \hat{\boldsymbol X}_{n+1:N})$$

   推理时，缺失的条件输入直接用掩码令牌替代，使单一模型无需任何结构修改即可在三种任务间灵活切换。

### 数据流总结

完整的推理数据流为：第一人称图像经 DINOv2 编码器提取场景特征，与头戴设备轨迹特征一同作为条件信号；噪声运动序列进入 Transformer 解码器，通过交叉注意力融合条件信息，经迭代去噪逐步恢复为干净运动；最终通过头部中心表示模块将预测的 SMPL-X 参数转换为物理合理的 3D 人体运动。这一端到端的条件扩散框架将场景感知、运动先验与任务统一性有机整合，为第一人称运动合成提供了完整的计算管道。

### 3.1 条件扩散模型基础

UniEgoMotion 构建在条件扩散模型框架之上。给定真实运动序列 $\boldsymbol X$，前向过程按噪声调度逐步注入高斯噪声：

$$q_t(\boldsymbol X^t | \boldsymbol X) = \mathcal{N}(\boldsymbol X^t; \sqrt{\bar{\alpha}_t} \boldsymbol X, (1 - \bar{\alpha}_t) \boldsymbol I)$$

其中 $\bar{\alpha}_t$ 控制噪声强度，$t \in [1, t_{max}]$ 为扩散时间步。模型 $\mathcal{M}$ 以噪声运动 $\boldsymbol X^t$、时间步 $t$ 和条件输入 $\boldsymbol C$ 为输入，预测干净运动 $\hat{\boldsymbol X}$：

$$\hat{\boldsymbol X} = \mathcal{M}(\boldsymbol X^t, t, \boldsymbol C; \boldsymbol \Theta)$$

训练目标为均方误差去噪损失：

$$\mathcal{L} = \mathbb{E}_{t \in [1, t_{max}], \boldsymbol X^t \sim q_t(\cdot | \boldsymbol X)} \left[ ||\boldsymbol X - \mathcal{M}(\boldsymbol X^t, t, \boldsymbol C)||_2^2 \right]$$

推理阶段通过迭代去噪采样，从纯噪声逐步恢复干净运动：

$$\boldsymbol X^{t-1} = \mathcal{M}(\boldsymbol X^t, t, \boldsymbol C) + \boldsymbol \epsilon_t$$

### 3.2 运动参数化与头部中心表示

运动序列采用 SMPL-X 参数化，第 $i$ 帧的运动参数为：

$$X_i = (R_i^r, t_i^r, \theta_i, \beta_i)$$

包含根旋转 $R_i^r$、根平移 $t_i^r$、21 个关节的局部旋转角度 $\theta_i$ 以及 10 维体型参数 $\beta_i$（序列内共享）。通过前向运动学可获得头部与各关节的 SE(3) 全局变换 $M_i^h$ 和 $M_i^j$。

核心创新在于**头部中心运动表示**：传统骨盆中心表示与头戴设备输入存在语义鸿沟，易引发脚部滑移和地板穿透。UniEgoMotion 将头部全局变换投影至地板平面（移除俯仰角、翻滚角和高度分量），建立规范参考系 $_c M_i$，进而将运动分解为两个分量：

$$(M_i^h, M_i^j) \rightarrow (_c M_i, \, _c M_i \odot M_i^h, \, _c M_i \odot M_i^j)$$

其中轨迹部分编码为帧间残差位移，体态部分编码为相对于该规范参考系的局部信息。这一分解使运动表示与第一人称设备坐标系天然对齐，并通过地板投影正则化增强物理合理性。

### 3.3 条件掩码与任务统一

UniEgoMotion 通过随机条件掩码策略实现单模型支持重建、预测、生成三任务。训练时，条件输入 $\boldsymbol C$ 被随机替换为可学习掩码令牌：

- **重建任务**：$\boldsymbol C = \{\boldsymbol T_{1:N}, \boldsymbol I_{1:N}\}$，提供完整轨迹和图像序列
- **生成任务**：$\boldsymbol C = \{\boldsymbol I_1\}$，仅提供单张第一人称图像
- **预测任务**：推理时采用扩散 inpainting，以已知帧覆盖生成帧保证时序一致性：

$$\hat{\boldsymbol X}_{1:N} \gets \mathrm{concat}(\boldsymbol X_{1:n}, \hat{\boldsymbol X}_{n+1:N})$$

训练过程中随机在重建与生成两种极端条件间切换，使模型学会在任意条件缺失下进行合理推断。

### 3.4 图像场景编码器

图像条件通过预训练 DINOv2 ViT 编码器提取细粒度场景上下文特征，仅微调投影网络。这些特征通过交叉注意力注入 Transformer 解码器，为运动合成提供场景语义约束。消融实验表明，DINOv2 编码器显著优于 CLIP 和 EgoVideo 编码器（重建 FID 从 0.041/0.021 降至 0.027），验证了细粒度视觉特征对场景感知运动建模的关键作用。

### 3.5 Transformer 解码器架构

去噪网络采用 Transformer 解码器架构，以噪声运动序列 $\boldsymbol X_{1:N}^t$ 为输入，通过自注意力建模时序依赖，交叉注意力融合轨迹特征 $\boldsymbol T_{1:N}$ 和图像特征 $\boldsymbol I_{1:N}$，并结合扩散时间步嵌入，预测干净运动序列。消融实验证实解码器架构优于编码器架构和 1D U-Net（重建 MPJPE 下降约 0.015–0.045），表明自回归形式的解码器更适合运动序列的去噪建模。

## 实验与关键发现

### 核心实验设置

UniEgoMotion 在自建的 **EE4D‑Motion** 数据集上进行统一训练与评估。该数据集源自 EgoExo4D，采用 8 秒片段、10fps 采样（N=80），训练集包含约 143K 样本，验证集 4400 样本。评估覆盖三大任务：**重建**（给定完整第一人称视频与头部轨迹）、**预测**（给定前 2 秒观察预测后 6 秒运动）和**生成**（仅给定单张第一人称图像生成 8 秒运动序列）。

评估指标包括：MPJPE（全局关节位置误差）、MPJPE‑PA（Procrustes 对齐后关节误差）、MPJPE‑H（头部对齐后关节误差）、Foot Slide（足部滑移）、Foot Contact（足部接触误差）、Semantic Similarity（语义相似度）和 FID。预测与生成任务中，MPJPE 指标分别计算未来 2–4 秒（预测）和 0–2 秒（生成）。

### 第一人称运动重建：全面超越现有方法

Table 1（上）展示了重建任务的核心定量结果。UniEgoMotion 在所有指标上均显著优于现有第一人称运动重建方法 **AvatarPoser**、**EgoEgo** 和 **EgoAllo**。关键提升包括：

![[assets/figures/papers/paper_list_l1884_A_Unified_Model_for_Egocentric_Motion_Reconstruction_Forecasting_and_Gen/figures/004_Table_1.jpg]]
*Table 1: Egocentric Motion Reconstruction: Comparison of the reconstruction capabilities of UniEgoMotion with prior works (top). Ablation on UniEgoMotion’s model design for the reconstruction task (bottom). Note that the vanilla UniEgoMotion model uses transformer decoder architecture, head-centric motion representation, and DINOv2 visual encoder*

- **MPJPE** 从 AvatarPoser 的 0.116 降至 **0.100**（降幅 13.8%），MPJPE‑PA 从 0.065 降至 **0.053**。
- **语义相似度** 从 0.872 提升至 **0.918**，FID 从 0.043 降至 **0.027**，表明重建运动在语义层面与真值更加一致，且分布更接近真实运动。
- 足部接触误差（Foot Contact）为 **0.027**，显著低于其他方法，验证了头部中心表示对物理合理性的增强效果。

Figure 3 的定性对比直观展示了差异：基线方法常出现浮空、穿地和关节定位不准等问题，而 UniEgoMotion 的重建结果与真值高度吻合。Figure 6 进一步以顶点误差热力图展示了重建精度优势。

![[assets/figures/papers/paper_list_l1884_A_Unified_Model_for_Egocentric_Motion_Reconstruction_Forecasting_and_Gen/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparison of Egocentric Reconstruction. The input egocentric images are shown on the left, with the corresponding ego-device trajectory visualized alongside the predictions. Baseline methods exhibit floating motion, floor penetration, and inaccurate joint localization, whereas UniEgoMotion generates reconstructions that closely align with the ground truth*

![[assets/figures/papers/paper_list_l1884_A_Unified_Model_for_Egocentric_Motion_Reconstruction_Forecasting_and_Gen/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative comparison of Egocentric Reconstruction, with absolute vertex errors color-coded. The input egocentric images are shown on the left, with the corresponding ego-device trajectory visualized alongside the predictions*

> **公平性说明**：EgoEgo 和 AvatarPoser 使用了从运动标注导出的“完美”头部轨迹，因此其头部跟踪误差被省略；UniEgoMotion 报告了实际头部旋转误差（0.260）和平移误差（0.058）。EgoAllo 的评估直接使用扩散模型输出，未运行后处理优化步骤。所有方法均在相同的数据划分上重新训练。

### 第一人称运动预测与生成：物理合理性与多样性双赢

Table 2 分别报告了预测（左）和生成（右）任务的定量结果。UniEgoMotion 在足部滑移和接触指标上显著优于两阶段扩散基线（Two‑stage diffusion）和 LSTM 基线：

![[assets/figures/papers/paper_list_l1884_A_Unified_Model_for_Egocentric_Motion_Reconstruction_Forecasting_and_Gen/figures/006_Table_2.jpg]]
*Table 2: The baselines and ablations are evaluated on egocentric motion forecasting (left) and generation (right). The metrics reported include J: MPJPE, J-PA: MPJPE-PA, J-H: MPJPE-H, FS: Foot Slide, FC: Foot Contact, and SS: Semantic Similarity. MPJPE metrics are computed over the first two seconds of future predictions (0-2s for generation and 2-4s for forecasting). ∗Two-stage baseline replicates the trajectory-to-motion prediction framework used in prior works on image-based motion forecasting [8] and motion generation [84]*

- **预测任务**（2–4s）：Foot Slide 从 Two‑stage 的 3.55 降至 **2.60**，LSTM 基线则高达 7.23。MPJPE 为 0.206，优于 Two‑stage 的 0.214。
- **生成任务**（0–2s）：Foot Slide 从 Two‑stage 的 4.35 降至 **2.89**，MPJPE 为 0.226。

Figure 4 的预测定性对比显示，LSTM 基线倾向于预测“平均化”的未来运动并伴随严重脚部滑移，Two‑stage 基线产生阻尼化运动，而 UniEgoMotion 成功预测了复杂动作，如蹲下修理自行车轮胎、跳萨尔萨舞、绕锥桶运球训练。Figure 5 的生成定性对比表明，UniEgoMotion 利用细粒度图像特征生成了更准确、场景合理的运动，如足球颠球、篮球投篮训练和与侧面橱柜的交互。

![[assets/figures/papers/paper_list_l1884_A_Unified_Model_for_Egocentric_Motion_Reconstruction_Forecasting_and_Gen/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison of Egocentric Forecasting for predicting future motion using the first 2 seconds of egocentric video and trajectory input. The LSTM baseline predicts an average future motion and suffers from foot sliding, while the Two-stage baseline produces damped motion. In contrast, our model successfully predicts complex motions, such as squatting down to repair a bike tire (top), performing a salsa dance (middle), and executing a dribbling drill around a dome cone (bottom)*

### 消融实验：架构选择与表示设计的因果验证

**Table 1（下）** 系统消融了 UniEgoMotion 的核心设计选择：

**1. 网络架构**：Transformer 解码器架构显著优于 Transformer 编码器（MPJPE 0.145）和 1D U‑Net（MPJPE 0.140），验证了解码器架构在条件运动扩散中的适配性。

**2. 运动表示**：头部中心表示是决定性的设计选择。将头部中心表示替换为骨盆中心表示（pelvis‑centric）后，MPJPE 从 0.100 急剧恶化至 **0.166**，足部接触误差从 0.027 升至 0.028，直接证明了头部中心表示在弥合第一人称视觉输入与 3D 运动合成之间鸿沟的核心作用（见 Section 3.5, Figure 7）。

**3. 图像编码器**：预训练 DINOv2 ViT 编码器优于 CLIP 编码器（FID 0.041）和 EgoVideo 编码器（FID 0.021），FID 降至 **0.027**。这表明细粒度场景特征对第一人称运动重建至关重要，粗粒度语义嵌入（如 CLIP）不足以捕获场景上下文。

**Table 3** 消融了条件输入的必要性：
- **移除视频输入**（w/o video）：语义相似度从 0.918 降至 0.878，FID 从 0.027 升至 0.030，表明图像场景信息对语义一致性贡献显著。
- **移除轨迹输入**（w/o trajectory）：头部平移误差从 0.058 急剧升至 **0.280**，MPJPE 从 0.100 升至 0.149。轨迹缺失时，模型被迫隐式解决视觉里程计问题，绝对定位能力大幅下降。
- 单独训练单模态变体（仅轨迹或仅视频）并未带来显著提升，验证了多模态条件联合训练的有效性。

**Table 2** 的预测/生成消融进一步确认了 DINOv2 编码器和头部中心表示在预测与生成任务中的一致增益。

### 失败模式与局限性

1. **轨迹依赖瓶颈**：当头部轨迹缺失时（仅图像生成），绝对定位误差急剧增大（Head Trans. Err. 0.280 vs 0.058），模型无法可靠推断全局位置。这是当前框架最显著的失效模式。
2. **生成任务的固有挑战**：仅从单张第一人称图像生成完整 8 秒运动序列，MPJPE 为 0.226，显著高于基于观察的重建任务（0.100）。部分场景上下文因第一人称视野受限而无法准确捕获。
3. **极端头部运动适应**：头部中心表示通过移除俯仰/翻滚角进行地板投影，在极端头部运动（如翻滚）时可能丢失关键方向信息，当前实验未覆盖此类场景。
4. **数据标注噪声**：EE4D‑Motion 的伪真值通过多视角拟合获得，复杂遮挡或远距离场景下可能存在标注噪声，影响模型在这些场景下的性能上限。
5. **推理效率**：扩散模型需要迭代去噪步骤，推理速度相对较慢，文中未探讨蒸馏或少量扩散步等加速策略。

![[assets/figures/papers/paper_list_l1884_A_Unified_Model_for_Egocentric_Motion_Reconstruction_Forecasting_and_Gen/figures/009_Table_3.jpg]]
*Table 3: Ablation on Conditioning Inputs: We evaluate UniEgoMotion in two ablation settings–without video and without trajectory input. Additionally, we train two single-modality variants of UniEgoMotion by conditioning only on trajectory or only on video*

## 定位与知识库关联

### 1. 与第一人称运动重建方法的对比与定位

UniEgoMotion 直接对标三类第一人称运动重建方法：**AvatarPoser**、**EgoEgo** 和 **EgoAllo**。这三者均依赖头戴设备的 6-DOF 轨迹与第一人称图像输入，但均未显式利用图像中的场景语义信息，且普遍采用骨盆中心的全局运动表示。UniEgoMotion 在 Table 1 的重建任务中全面超越这些基线：MPJPE 从 AvatarPoser 的 0.116 降至 0.100，语义相似度从 0.872 提升至 0.918，FID 从 0.043 降至 0.027。定性对比（Figure 3）显示，基线方法普遍存在漂浮、穿地以及关节定位不准等问题，而 UniEgoMotion 的重建结果与真值高度吻合。

关键差异点在于：
- **场景感知能力**：基线方法未使用或仅使用轻量图像编码器，UniEgoMotion 引入预训练 DINOv2 ViT 提取细粒度场景特征，通过交叉注意力注入 Transformer 解码器。
- **运动表示**：基线采用骨盆中心或头-骨盆运动链表示，UniEgoMotion 采用头部中心表示——将头部 SE(3) 变换投影至地板建立规范参考系，轨迹编码为帧间残差，体态编码为相对于该参考系的局部信息。消融实验（Table 1）证实，将头部中心表示替换为骨盆中心表示后，MPJPE 从 0.100 升至 0.166，足部接触误差从 0.027 升至 0.028。

**公平性说明**：EgoEgo 和 AvatarPoser 使用了从运动标注导出的头部轨迹而非实际 SLAM 轨迹，因此其头部跟踪误差被省略（实际为完美设计）；UniEgoMotion 报告了实际头部旋转/平移误差。EgoAllo 的评估直接使用扩散模型输出，未运行后处理优化步骤。所有方法均在相同的 EE4D-Motion 训练/验证划分上重新训练，使用相同的 8 秒 10fps 片段。

### 2. 与第一人称运动预测与生成方法的对比

在第一人称运动预测与生成任务上，UniEgoMotion 与两类基线对比：
- **任务特定 LSTM 基线**：LSTM-forecasting 顺序处理图像与轨迹特征序列预测未来运动，LSTM-generation 仅从单张图像特征生成运动。Table 2 显示 LSTM 基线在预测任务上足部滑移高达 7.23（UniEgoMotion 为 2.60），生成任务上为 4.35（UniEgoMotion 为 2.89），且倾向于预测平均运动，缺乏多样性（Figure 4、5）。
- **两阶段扩散基线**：复现了先前工作中“轨迹到运动”的预测框架。该基线在预测任务上产生阻尼运动，在生成任务上无法充分利用场景上下文。

UniEgoMotion 的统一训练策略——随机将条件输入替换为可学习掩码令牌，模拟重建与生成两个极端，预测通过扩散 inpainting 实现——使其无需为每个任务训练独立模型。在预测任务的扩散 inpainting 过程中，用已知重建帧覆盖生成帧以保证时序一致性。

### 3. 适用边界与核心局限

**强依赖惯性 SLAM 轨迹**：当轨迹输入缺失时，模型被迫隐式解决视觉里程计问题，性能急剧下降。Table 3 显示，移除轨迹输入后，头部平移误差从 0.058 升至 0.280，MPJPE 从 0.100 升至 0.244。这表明 UniEgoMotion 在纯视觉输入（无 IMU/SLAM）场景下尚不具备鲁棒定位能力。

**生成任务的固有挑战**：仅从单张第一人称图像推断完整 3D 运动序列，其绝对关节误差（MPJPE 0.226）显著高于基于观察的重建任务（0.100）。部分场景上下文可能因视野受限而无法准确捕获，尤其是遮挡严重或远距离交互场景。

**数据标注噪声**：EE4D-Motion 数据集源自 EgoExo4D，伪真值通过多视角拟合获得，复杂遮挡或远距离场景下标注可能存在噪声，可能影响模型在这些场景下的表现上限。

**缺乏显式高级语义条件**：当前框架未利用文本或动作标签等显式高级语义条件，无法直接根据文本指令生成特定动作。

### 4. 开放问题

1. **文本驱动的第一人称运动生成**：EE4D-Motion 数据集中包含 EgoExo4D 的动作叙述，如何利用这些叙述实现文本条件的第一人称运动生成？
2. **细粒度场景-运动交互建模**：能否进一步建模手-物接触或细粒度操作，超越当前的全身运动合成？
3. **极端头部运动下的表示鲁棒性**：头部中心表示在极端头部运动（如翻滚）时，移除俯仰/翻滚角是否会丢失关键信息？如何自适应地保留必要自由度？
4. **推理效率**：扩散模型推理速度相对较慢，是否有更高效的生成策略（如蒸馏、减少扩散步数）以支持实时应用？
5. **场景合理性评估指标**：除现有语义相似度外，如何定量评估生成运动的“场景合理性”？是否需要引入物理仿真验证或接触一致性等新指标？

## 原文 PDF

![[paperPDFs/ICCV_2025/A_Unified_Model_for_Egocentric_Motion_Reconstruction_Forecasting_and_Generation.pdf]]
