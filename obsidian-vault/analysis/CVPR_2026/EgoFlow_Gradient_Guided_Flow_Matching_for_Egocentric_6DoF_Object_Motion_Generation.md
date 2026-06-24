---
title: "EgoFlow: Gradient-Guided Flow Matching for Egocentric 6DoF Object Motion Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EgoFlow_Gradient_Guided_Flow_Matching_for_Egocentric_6DoF_Object_Motion_Generation.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Saroha_EgoFlow_Gradient-Guided_Flow_Matching_for_Egocentric_6DoF_Object_Motion_Generation_CVPR_2026_paper.html
project_link: https://abhi-rf.github.io/egoflow/
code_link: null
aliases:
- EgoFlow
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用流匹配（Flow Matching）代替扩散模型，将轨迹生成转化为确定性速度场的回归，配合混合Mamba-Transformer-Perceiver架构增强时序和跨模态建模，并在推理时通过梯度引导注入可微分物理代价（SDF碰撞惩罚、旋转方向连续性与速度平滑）来迫使生成轨迹遵守物理约束，而无需额外监督。
primary_logic: 在R9空间中学习连续流场，使轨迹生成过程本身即编码物理偏向；同时利用梯度引导在采样过程中动态优化，把数据驱动的运动先验和物理约束解耦，从而在不重训练的情况下适应新场景的障碍布局。
claims:
- 在HD-EPIC数据集上，EgoFlow将碰撞率从无引导版本的11.6%降至2.5%，相对减少约79%，证明了梯度引导对物理合理性的决定性作用。
- 混合Mamba-Transformer-Perceiver架构在消融实验中取得最优指标组合，仅3-6-3层配置即达到ADE 0.279、FDE 0.102、碰撞率2.5%，验证了不同模块协同的必要性。
- 移除场景点云或目标位置条件会使ADE/FDE显著恶化，表明局部几何与目标信息是精确轨迹的关键因素。
- HD-EPIC 上 Collision Rate (%) = EgoFlow (guided) 2.5
---

# EgoFlow: Gradient-Guided Flow Matching for Egocentric 6DoF Object Motion Generation

> [!tip] 核心洞察
> 在R9空间中学习连续流场，使轨迹生成过程本身即编码物理偏向；同时利用梯度引导在采样过程中动态优化，把数据驱动的运动先验和物理约束解耦，从而在不重训练的情况下适应新场景的障碍布局。

| 字段 | 内容 |
|------|------|
| 中文题名 | EgoFlow：面向自我中心6DoF物体运动生成的梯度引导流匹配 |
| 英文题名 | EgoFlow: Gradient-Guided Flow Matching for Egocentric 6DoF Object Motion Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Saroha_EgoFlow_Gradient-Guided_Flow_Matching_for_Egocentric_6DoF_Object_Motion_Generation_CVPR_2026_paper.html) · [Project](https://abhi-rf.github.io/egoflow/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | EgoFlow |
| Dataset | HD-EPIC, HOT3D |

> [!tip] 效果简介
> - HD-EPIC 上，Collision Rate (%) EgoFlow (guided) 2.5 vs EgoFlow (w/o guidance) 11.6 (相对减少 ~79%)；Collision Rate (%) EgoFlow (guided) 2.5 vs GIMO 23.5 (-21.0 (绝对))；ADE (m) 0.279 vs GIMO 0.285 (-0.006)。
> - HOT3D (zero-shot) 上，ADE (m) EgoFlow 0.265 vs GIMO ≈0.57 (近似) (明显降低)。

## 概述

从自我中心视频中生成物体的6自由度（6DoF）运动轨迹，是实现具身智能体在真实环境中执行操作任务的关键能力。给定一段手持相机拍摄的交互视频、一个文本指令（如“拿起桌上的手机”）以及目标位姿，系统需要预测物体在未来时刻的连续平移与旋转序列，且该序列必须同时满足空间合理性（避免穿透桌面、墙壁等障碍物）和运动平滑性（避免突变或抖动）。

现有方法——无论是基于Transformer的自回归模型（如**GIMO**，Zheng et al., ECCV 2022），还是基于扩散模型的条件生成方法（如**CHOIS**，Jiaman Li et al., ECCV 2024；**EgoScaler**，Yoshida et al., CVPR 2025）——面临一个共同瓶颈：在遮挡、快速相机运动和大规模杂乱场景下，生成的轨迹缺乏长期物理一致性，常出现穿透障碍物或不自然的位移。其根源在于，这些方法要么没有显式的物理约束，要么仅在生成后进行简单的后处理过滤，而无法在生成过程中主动推理碰撞避免与运动平滑。

**EgoFlow** 针对上述瓶颈提出了三个核心改变。第一，**用流匹配（Flow Matching）替代扩散模型**，将轨迹生成转化为在9维位姿空间 $\mathbb{R}^9$ 中学习确定性速度场，从而避免了扩散模型迭代去噪带来的效率与精度损失。第二，设计**混合Mamba-Transformer-Perceiver架构**，以三阶段方式协同建模时序动态、跨模态场景条件与轨迹细化：双向Mamba负责高效时序编码，Perceiver Transformer实现几何与语义特征的条件融合，最后再经Mamba层精细调整轨迹。第三，引入**梯度引导的物理优化采样**：在推理的每一步积分后，对预测速度执行梯度下降，显式最小化可微分碰撞代价（基于SDF的穿透惩罚）、旋转方向一致性代价和平移加速度平滑代价，迫使生成轨迹遵守物理约束而无需额外监督。

在HD-EPIC数据集上的实验表明，EgoFlow在精度与物理合理性上均显著优于基线方法。最关键的证据来自碰撞率指标：无引导版本的EgoFlow碰撞率为11.6%，而加入梯度引导后骤降至**2.5%**，相对降低约79%；相比之下，GIMO的碰撞率高达23.5%。在平均位移误差（ADE）上，EgoFlow达到0.279 m，同样优于GIMO的0.285 m。消融实验进一步证实，移除场景点云或目标位姿条件会显著恶化ADE/FDE，而去掉碰撞避免项则使碰撞率从2.5%反弹至11.6%，验证了局部几何感知与梯度引导对物理合理性的决定性作用。在跨数据集泛化测试中（HOT3D zero-shot），EgoFlow同样展现出明显优势。

EgoFlow的核心洞察在于：在 $\mathbb{R}^9$ 流空间中学习连续传输场，使轨迹生成过程本身即编码物理偏向；同时利用梯度引导在采样时动态优化，将数据驱动的运动先验与物理约束解耦，从而在不重新训练的情况下适应新场景的障碍布局。这一设计为自我中心物体运动生成提供了一条兼顾精度与物理一致性的新路径。

## 背景与动机

### 问题背景：自我中心视频中的6DoF物体运动生成

随着增强现实（AR）、虚拟现实（VR）和具身人工智能的快速发展，从头戴式设备拍摄的自我中心（egocentric）视频中理解和生成物体的三维运动轨迹，已成为一个关键且具有挑战性的研究问题。这一任务的核心目标是：**给定一段历史观测轨迹、周围三维场景信息以及任务描述（如“拿起桌上的手机”），预测物体在未来时间步的6DoF（6自由度）运动轨迹**，即同时包含三维平移和三维旋转的完整刚体运动。

与传统的固定视角轨迹预测不同，自我中心场景具有独特的复杂性。相机本身处于持续运动中，导致物体在图像平面上的表观运动是物体自身运动与相机运动的耦合结果。此外，自我中心视频通常包含大量遮挡、快速视角切换以及杂乱的家庭或工业环境，这对轨迹生成的物理合理性和长期一致性提出了极高要求。

### 现有方法缺口：物理一致性的缺失

当前主流的物体轨迹生成方法大致可分为两类：

1. **基于Transformer的自回归方法**，如 **GIMO**（Zheng et al., ECCV 2022），通过序列建模直接预测未来轨迹。这类方法虽然能够捕捉时序依赖，但缺乏对三维场景几何的显式建模，导致生成的轨迹经常穿透障碍物或与环境发生碰撞。在HD-EPIC数据集上，GIMO的碰撞率高达23.5%，意味着近四分之一的生成轨迹存在物理不可行性。

2. **基于扩散模型（Diffusion Models）的方法**，如 **CHOIS**（Jiaman Li et al., ECCV 2024）和 **EgoScaler**（Yoshida et al., CVPR 2025），通过迭代去噪过程生成轨迹。扩散模型虽然具有强大的分布建模能力，但其采样过程计算开销大，且同样缺乏对物理约束（如碰撞避免、运动平滑性）的内建机制。这些方法往往依赖后处理过滤或重新采样来减少碰撞，而非在生成过程中主动遵守物理规律。

两类方法的共同瓶颈在于：**现有方法在遮挡、快速相机运动以及大规模杂乱场景下，难以生成具有长期物理一致性的6DoF物体轨迹，尤其缺乏显式的碰撞避免与运动平滑推理，导致生成的轨迹经常穿透障碍物或出现不自然的位移。**

### 本文动机：将物理约束融入生成过程

针对上述缺口，本文提出**EgoFlow**，其核心动机在于：

- **范式转换**：用**流匹配（Flow Matching）** 替代扩散模型，将轨迹生成转化为确定性速度场的回归问题。流匹配通过学习从噪声分布到数据分布的连续传输场，天然具有更高效的采样过程和更平滑的生成轨迹。

- **架构创新**：设计**混合Mamba-Transformer-Perceiver架构**，融合双向Mamba状态空间模型的时序建模能力、Transformer的跨模态注意力机制以及Perceiver的感知压缩能力，实现对时序动态、场景几何和语义意图的联合建模。

- **物理约束注入**：在推理阶段引入**梯度引导采样**机制，通过可微分物理代价函数（基于SDF的碰撞惩罚、旋转方向连续性与速度平滑性）对每一步生成的速度场进行梯度优化，迫使轨迹遵守物理约束，而无需额外的监督信号或重新训练。

这一设计理念的核心洞察在于：**在R⁹空间中学习连续流场，使轨迹生成过程本身即编码物理偏向；同时利用梯度引导在采样过程中动态优化，把数据驱动的运动先验和物理约束解耦，从而在不重训练的情况下适应新场景的障碍布局。** 实验结果表明，EgoFlow在HD-EPIC数据集上将碰撞率从无引导版本的11.6%降至2.5%，相对减少约79%，验证了这一技术路线的有效性。

## 核心创新

EgoFlow 的核心创新并非单一模块的替换，而在于**将生成范式、序列融合架构与推理时物理约束三者协同重构**，从而系统性地解决自我中心 6DoF 物体轨迹生成中长期存在的物理不合理性问题。下面从三个关键维度展开。

### 从扩散到流匹配的范式转换

现有主流方法（如 **CHOIS**（Jiaman Li et al., ECCV 2024）与 **EgoScaler**（Yoshida et al., CVPR 2025））普遍采用扩散模型在 R⁹ 空间中逐步去噪生成轨迹。扩散模型虽然建模能力强，但其随机采样过程本质上不编码运动的方向性偏好，导致生成的轨迹容易在遮挡或稀疏观测区域出现不自然的抖动与漂移。

EgoFlow 将生成过程重新定义为**确定性流匹配**：在 R⁹ 空间中学习一个连续速度场 $v_\theta$，该速度场直接预测从噪声分布指向真实轨迹分布的方向向量。训练时，网络通过线性插值路径 $\mathbf{x}_t = (1-t) \mathbf{x}_0 + t \mathbf{x}_1$ 学习条件速度场，最小化 L1 损失：

$$\mathcal{L}_{FM} = \mathbb{E}_{t, \mathbf{x}_0, \mathbf{x}_1} \left[ \| \mathbf{v}_\theta(\mathbf{x}_t, t, \mathcal{S}) - (\mathbf{x}_1 - \mathbf{x}_0) \|_1 \right]$$

推理时仅需 20 步确定性欧拉积分即可完成生成，相比扩散模型的上百步采样，在效率与稳定性上均有本质提升。更重要的是，流匹配将“运动先验”直接编码为速度场的方向性，使生成轨迹天然具备更平滑的位移特性。

### 混合 Mamba-Transformer-Perceiver 架构

基线方法通常采用纯 Transformer（如 GIMO）或纯 Mamba 进行序列建模，难以同时高效捕获长程时序依赖与异构多模态条件之间的细粒度交互。EgoFlow 提出一种**三阶段混合架构**，将不同归纳偏置分配到最擅长的子任务上：

- **Stage 1 — 时序上下文编码**：3 层双向 Mamba 对噪声轨迹进行初步时序建模，利用状态空间模型对长序列的线性复杂度优势，高效提取运动趋势。
- **Stage 2 — 跨模态注意力融合**：6 层 Perceiver Transformer 以 Mamba 输出的时序特征为 Query，对场景条件向量 $\mathbf{u}$（融合点云几何、夹具布局、任务语义与目标位姿）进行交叉注意力，实现时序动态与空间-语义条件的深度交互。
- **Stage 3 — 轨迹细化**：3 层双向 Mamba 对融合后的特征进行二次时序精炼，输出最终的速度场预测。

这种 3-6-3 配置并非随意设计。架构消融实验（Table 4）表明，该配置在所有指标上达到最优折衷——继续增加 Transformer 或 Mamba 层数并未带来持续提升，验证了不同模块在特定阶段的协同必要性。

### 梯度引导：将物理约束注入推理过程

这是 EgoFlow 最具决定性的创新。现有方法大多缺乏显式的物理约束机制，生成轨迹的碰撞避免仅依赖数据驱动先验，在复杂场景中频繁失效（如 GIMO 的碰撞率高达 23.5%）。

EgoFlow 在推理的每个积分步引入**梯度引导优化**：对网络预测的速度 $\mathbf{v}_\theta$ 执行 50 步梯度下降，最小化一组可微分物理代价函数：

$$\mathbf{v}_\theta^{(k+1)} = \mathbf{v}_\theta^{(k)} - \alpha \nabla_{\mathbf{v}} \mathcal{I}(\mathbf{x}_t - \Delta t \cdot \mathbf{v}^{(k)})$$

其中 $\mathcal{I}$ 由三项代价加权组成：

- **碰撞代价** $\mathcal{T}_{\mathrm{coll}}$：基于场景 SDF 惩罚轨迹点进入障碍物安全距离 $\epsilon = 5\mathrm{cm}$ 以内的行为。
- **旋转一致性代价** $\mathcal{T}_{\mathrm{rot}}$：惩罚相邻帧旋转方向的突变，强制角运动平滑。
- **平移平滑代价** $\mathcal{T}_{\mathrm{vel}}$：惩罚平移加速度的范数，抑制速度突变。

这一设计的核心洞察在于**将数据驱动的运动先验与物理约束完全解耦**：流匹配网络负责生成符合数据分布的“合理”轨迹，梯度引导则在采样过程中动态修正，使轨迹适应任意新场景的障碍布局——无需重新训练，仅需提供场景的 SDF。

消融实验（Table 3）给出了决定性证据：移除碰撞代价项后，碰撞率从 2.5% 急剧上升至 11.6%，相对恶化约 4.6 倍，充分证明梯度引导对物理合理性的因果作用远大于数据驱动先验本身。

### 创新协同的因果链条

上述三个创新并非孤立存在，而是形成了一条因果链路：流匹配提供了确定性、可微分的速度场，使得梯度引导可以直接作用于速度预测之上；混合架构则确保了速度场本身已融合充分的场景几何与语义信息，使梯度修正不至于偏离任务目标。三者协同的结果是：EgoFlow 在 HD-EPIC 上以 ADE 0.279、FDE 0.102、碰撞率 2.5% 的成绩全面超越 GIMO（碰撞率 23.5%）、CHOIS 等基线，并在跨数据集零样本泛化（HOT3D）中展现出显著优势。

## 整体框架

EgoFlow 的整体 pipeline 围绕一个核心思路构建：**将 6DoF 物体轨迹生成转化为在 R⁹ 空间中的确定性流匹配问题，并通过推理阶段的梯度引导注入物理约束**。整个框架由四个关键模块串联而成，形成从多模态场景理解到物理一致轨迹输出的端到端流程。

### 输入与输出定义

系统接收以下输入：

- **观测轨迹**：历史 30% 的物体 6DoF 轨迹帧，每帧表示为 9 维向量 $\mathbf{x}_t = [\mathbf{p}_t; \mathbf{r}_t] \in \mathbb{R}^9$，其中 $\mathbf{p}_t$ 为 3D 位置，$\mathbf{r}_t$ 为 6D 连续旋转表示。
- **场景信息**：3D 点云（经 PointNet++ 编码）、场景中固定物体的包围盒（fixture bounding boxes）。
- **任务描述**：文本指令（经 CLIP 编码）与目标位姿。

输出为**未来 70% 的轨迹** $\mathbf{x}_{H+1:T} \in \mathbb{R}^{(T-H) \times 9}$，要求轨迹在到达目标的同时避免碰撞并保持运动平滑。

### 模块关系与数据流

整体流程严格按以下四阶段推进（对应 Figure 2）：

![[assets/figures/papers/paper_list_l28_https_openaccess_thecvf_com_content_CVPR2026_html_Saroha_EgoFlow_Gradien/figures/002_Figure_2.jpg]]
*Figure 2: EgoFlow overview. Given a 3D scene, a task prompt, and a task goal, our method first fuses multimodal inputs through a scene conditioning block (Sec. 3.2). The fused features are used as conditioning for trajectory generation. We use input trajectories as the source samples of our flow matching model (Sec. 3.3), which maps the generated trajectories to the target distribution, the ground-truth trajectories, through a hybrid architecture (Sec. 3.4). We integrate physical guidance at inference to ensure physical plausible and collisionfree trajectories (Sec. 3.5)*

**1. 多模态场景条件编码器（Sec 3.2）**
该模块将异构输入融合为统一的条件向量 $\mathbf{u}$，为后续轨迹生成提供场景感知。具体包括：
- **点云特征插值**：对物体中心 $\mathbf{c}_t$ 在每一历史帧通过逆距离加权从 k 近邻点云特征中插值，获得局部几何描述 $\mathbf{F}_p$（Eq. 1）。
- **夹具布局编码**：将固定物体的包围盒嵌入为 tokens，经自注意力编码空间关系得到 $\mathbf{F}_b$（Eq. 2）。
- **多模态拼接**：将观测轨迹特征 $\mathbf{F}_{traj}$、点云特征 $\mathbf{F}_p$、夹具特征 $\mathbf{F}_b$、目标位姿特征 $\mathbf{F}_{goal}$ 及语义特征 $\mathbf{F}_s$ 拼接后通过 MLP 投影为统一条件向量 $\mathbf{u}$（Eq. 3）。

**2. 流匹配速度预测网络（Sec 3.3）**
该模块是生成的核心引擎。训练时，在干净轨迹 $\mathbf{x}_1$ 与噪声 $\mathbf{x}_0$ 之间定义线性插值路径 $\mathbf{x}_t = (1-t)\mathbf{x}_0 + t\mathbf{x}_1$，网络学习预测从噪声指向数据的方向向量，损失函数为 L1 距离（Eq. 5）。推理时，从随机噪声出发，通过 20 步反向欧拉积分确定性地生成轨迹（Eq. 6）。这一范式将扩散模型的随机采样替换为确定性速度场回归，天然编码了运动先验。

**3. 混合时序-跨模态推理模块（Sec 3.4）**
该模块采用三阶段混合架构处理时序依赖与条件融合：
- **Stage 1（时序编码）**：三层双向 Mamba 对噪声轨迹进行时序建模，通过 FiLM 调制注入条件信息。
- **Stage 2（跨模态注意力）**：六层 Perceiver Transformer 使用交叉注意力将场景条件 $\mathbf{u}$ 与轨迹特征深度融合。
- **Stage 3（轨迹细化）**：再三层双向 Mamba 对融合后的特征进行时序细化，输出最终的速度预测 $\mathbf{v}_\theta$。

这种 Mamba-Transformer-Mamba 的层叠设计兼顾了长序列建模效率与跨模态融合能力，消融实验（Table 4）表明 3-6-3 配置在 ADE/FDE 和碰撞率上达到最佳折衷。

**4. 梯度引导物理优化器（Sec 3.5）**
推理时，在每个积分步对预测速度执行 50 步梯度下降（学习率 α=0.1），优化由三项可微分代价组成的复合目标（Eq. 7-11）：
- **碰撞代价 $\mathcal{T}_{coll}$**：基于 SDF 惩罚轨迹点与固定物体距离小于 ε=5cm 的情况。
- **旋转一致性代价 $\mathcal{T}_{rot}$**：惩罚相邻帧间旋转变化的突转，促进平滑角运动。
- **平移平滑代价 $\mathcal{T}_{vel}$**：惩罚平移加速度范数，抑制速度突变。

这三项代价通过加权求和构成总代价 $\mathcal{I}$，梯度直接作用于预测速度 $\mathbf{v}_\theta$，使积分后的轨迹满足物理约束。权重在不同数据集上独立微调（HD-EPIC: λ_rot=λ_vel=2.0; HOT3D: λ_rot=λ_vel=5.0），但同数据集内保持一致。

### 关键设计决策

框架的一个核心洞察在于**将数据驱动的运动先验与物理约束解耦**：流匹配网络在训练时仅学习从噪声到数据的确定性流场，不涉及任何物理代价；物理合理性完全由推理阶段的梯度引导保证。这使得模型无需重训练即可适应新场景的障碍布局——只需提供新场景的 SDF，梯度引导便会自动将轨迹推离碰撞区域。这一设计的决定性证据来自 Table 3 的引导消融：移除碰撞代价项后，碰撞率从 2.5% 急剧上升至 11.6%，相对恶化约 79%，充分验证了梯度引导对物理合理性的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l28_https_openaccess_thecvf_com_content_CVPR2026_html_Saroha_EgoFlow_Gradien/figures/001_Figure_1.jpg]]
*Figure 1: EgoFlow: a method for object trajectory generation from egocentric videos. Given a textural command and the surrounding environment, EgoFlow generates physically valid 6DOF object trajectories that respect spatial constraints across diverse environments by learning from egocentric videos*

## 核心模块与公式推导

### 3.1 问题形式化与轨迹表示

EgoFlow 将每一帧的物体位姿表示为 9 维向量，拼接 3D 平移位置与 6D 连续旋转表征：

$$\mathbf{x}_t = [\mathbf{p}_t; \mathbf{r}_t] \in \mathbb{R}^9$$

其中 $\mathbf{p}_t \in \mathbb{R}^3$ 为物体中心在相机坐标系下的位置，$\mathbf{r}_t \in \mathbb{R}^6$ 为连续 6D 旋转表示。给定前 $H$ 帧观测轨迹 $\mathbf{x}_{1:H}$ 与场景条件 $\mathcal{S}$，目标是生成未来 $T-H$ 帧轨迹 $\mathbf{x}_{H+1:T}$，使其既符合运动自然性，又避免与场景障碍物发生碰撞。实践中采用 30% 轨迹作为输入，预测剩余 70%。

### 3.2 多模态场景条件编码器

条件编码器将异构输入融合为统一的条件向量 $\mathbf{u}$，包含以下关键模块：

**点云局部几何特征插值。** 对每一观测帧 $t$，以物体定向包围盒中心 $\mathbf{c}_t$ 为查询点，在 PointNet++ 编码的场景点云特征中检索 $k$ 个最近邻点，通过逆距离加权聚合为局部几何描述：

$$\mathbf{F}_p = \sum_{t=1}^{H} \frac{\sum_{i=1}^{k} w_i(\mathbf{c}_t) \mathbf{f}_i}{\sum_{i=1}^{k} w_i(\mathbf{c}_t)}, \quad w_i(\mathbf{c}_t) = \frac{1}{|\mathbf{c}_t - \mathbf{p}_i|^2}$$

**固定障碍物布局编码。** 场景中 $M$ 个静态物体的包围盒嵌入 $\{b_k\}_{k=1}^{M}$ 通过自注意力捕获空间相互关系：

$$\mathbf{F}_b = \mathrm{SelfAttn}(\{b_k\}_{k=1}^{M})$$

**统一条件投影。** 将观测轨迹特征 $\mathbf{F}_{traj}$、点云几何特征 $\mathbf{F}_p$、目标位姿特征 $\mathbf{F}_{goal}$、夹具包围盒特征 $\mathbf{F}_g$、障碍物布局特征 $\mathbf{F}_b$ 以及任务文本 CLIP 特征 $\mathbf{F}_s$ 拼接后经 MLP 投影：

$$\mathbf{u} = \mathrm{MLP}([\mathbf{F}_{traj}, \mathbf{F}_p, \mathbf{F}_g, \mathbf{F}_b, \mathbf{F}_s, \mathbf{F}_{goal}])$$

### 3.3 流匹配速度预测

EgoFlow 采用流匹配（Flow Matching）替代扩散模型，在 $\mathbb{R}^9$ 空间中学习确定性速度场。训练时，在干净轨迹 $\mathbf{x}_1$ 与噪声样本 $\mathbf{x}_0 \sim \mathcal{N}(0, I)$ 之间定义线性插值路径：

$$\mathbf{x}_t = (1-t) \mathbf{x}_0 + t \mathbf{x}_1, \quad t \in [0,1]$$

网络 $\mathbf{v}_\theta$ 以噪声轨迹 $\mathbf{x}_t$、时间步 $t$ 和场景条件 $\mathcal{S}$ 为输入，预测从噪声指向数据的方向向量，训练损失为 L1 范数：

$$\mathcal{L}_{FM} = \mathbb{E}_{t \sim \mathcal{U}[0,1], \mathbf{x}_0, \mathbf{x}_1} [ \| \mathbf{v}_\theta(\mathbf{x}_t, t, \mathcal{S}) - (\mathbf{x}_1 - \mathbf{x}_0) \|_1 ]$$

推理时通过反向欧拉积分生成轨迹，采用 20 步离散化（$\Delta t = 1/20$）：

$$\mathbf{x}_{t-\Delta t} = \mathbf{x}_t - \Delta t \cdot \mathbf{v}_\theta(\mathbf{x}_t, t, \mathcal{S})$$

### 3.4 混合 Mamba-Transformer-Perceiver 架构

速度预测网络采用三阶段混合架构，协同建模时序动态、跨模态融合与轨迹细化：

- **Stage 1 — 时序上下文编码：** 3 层双向 Mamba 状态空间模型对噪声轨迹序列进行时序建模，通过 FiLM 调制注入条件信息，捕获长程运动依赖。
- **Stage 2 — 跨模态注意力：** 6 层 Perceiver Transformer 以可学习查询向量为瓶颈，对 Mamba 输出的时序特征与条件向量 $\mathbf{u}$ 执行交叉注意力，实现几何与语义特征的高效融合。
- **Stage 3 — 轨迹细化：** 3 层双向 Mamba 对融合后的特征进行进一步时序平滑，输出最终的逐帧速度预测。

消融实验（Table 4）表明，3-6-3 层配置在所有指标上达到最佳折衷，进一步增加层数未带来持续提升。

### 3.5 梯度引导物理优化器

推理时，在每个积分步对预测速度执行 $K=50$ 步梯度下降，注入可微分物理代价，迫使生成轨迹满足碰撞避免与运动平滑约束：

$$\mathbf{v}_\theta^{(k+1)} = \mathbf{v}_\theta^{(k)} - \alpha \nabla_{\mathbf{v}} \mathcal{I}(\mathbf{x}_t - \Delta t \cdot \mathbf{v}^{(k)})$$

其中 $\alpha=0.1$ 为步长，总代价 $\mathcal{I}$ 由三项加权组成：

**碰撞避免代价。** 基于场景 SDF 惩罚轨迹点与障碍物表面距离小于安全阈值 $\epsilon=0.05\text{m}$ 的情况：

$$\mathcal{T}_{\mathrm{coll}} = \sum_{j=H+1}^{T} \max(0, \epsilon - d(\mathbf{p}_j))$$

**旋转方向一致性代价。** 惩罚相邻帧之间旋转变化的突转，促进平滑角运动：

$$\mathcal{T}_{\mathrm{rot}} = \sum_{j=H+1}^{T-1} \left(1 - \frac{\langle \Delta \mathbf{r}_j, \Delta \mathbf{r}_{j-1} \rangle}{\|\Delta \mathbf{r}_j\| \|\Delta \mathbf{r}_{j-1}\|}\right)$$

**平移加速度平滑代价。** 惩罚平移加速度的范数，抑制速度突变：

$$\mathcal{T}_{\mathrm{vel}} = \sum_{j=H+1}^{T-2} \|\mathbf{a}_j\|, \quad \mathbf{a}_j = \mathbf{v}_{j+1} - \mathbf{v}_j$$

三项代价的权重 $\lambda_{coll}$、$\lambda_{rot}$、$\lambda_{vel}$ 按数据集独立微调：HD-EPIC 上 $\lambda_{rot}=\lambda_{vel}=2.0$，HOT3D 上 $\lambda_{rot}=\lambda_{vel}=5.0$。

### 关键设计决策与证据

梯度引导的核心价值在于将数据驱动的运动先验与物理约束解耦——网络仅在干净轨迹上以标准流匹配损失训练，无需接触碰撞或平滑性监督信号；物理合理性完全由推理时的可微分优化保证。消融实验（Table 3）提供了决定性证据：移除碰撞代价 $\mathcal{T}_{coll}$ 后，碰撞率从 **2.5%** 急剧上升至 **11.6%**，相对恶化约 79%，验证了 SDF 碰撞惩罚对物理合理性的关键作用。同时，移除场景点云或目标位姿条件会导致 ADE/FDE 显著恶化，表明局部几何与目标信息是精确轨迹预测的必要条件。

## 实验与分析

### 实验设置

**数据集。** 主实验在 **HD-EPIC** 数据集上进行，该数据集提供了以自我为中心视角的6DoF物体操作轨迹及稠密3D场景重建。跨数据集泛化实验在 **HOT3D** 上评估，模型在 Ego-Exo4D 上训练后直接测试，以考察对未见场景的零样本迁移能力。

**任务设定。** 给定前30%的观测轨迹作为历史输入，模型需预测剩余70%的未来轨迹。输入条件包括：历史轨迹、场景点云（经PointNet++编码）、固定物体包围盒、物体类别、任务文本（CLIP嵌入）以及目标位姿。

**评估指标。** 采用以下指标全面衡量轨迹质量：
- **ADE (Average Displacement Error)**：预测轨迹与真值在所有帧上的平均位置误差（m）。
- **FDE (Final Displacement Error)**：终点位置误差（m）。
- **Frechet Distance**：预测轨迹与真值之间的Frechet距离。
- **Geodesic Distance**：旋转分量的测地线距离。
- **Collision Rate (%)**：轨迹中至少有一帧与场景发生碰撞的比例，基于SDF检测，安全距离阈值 ε=5cm。

**基线方法。** 对比以下代表性基线：
- **GIMO** (Zheng et al., ECCV 2022)：基于Transformer的自回归物体轨迹生成方法。
- **CHOIS** (Jiaman Li et al., ECCV 2024)：基于条件扩散模型的人-物交互生成方法。
- **EgoScaler** (Yoshida et al., CVPR 2025)：面向自我中心物体操作的扩散模型。
- **ManiFlow**：基于流匹配的操作策略基线。

**公平性保障。** 所有方法使用相同的训练/测试划分；EgoFlow结果报告为3次运行的平均值；梯度引导的超参数（λ_rot, λ_vel）在同一数据集内保持一致；基线均采用各自论文推荐的默认配置。

### 主要定量结果

**HD-EPIC 主结果。** Table 1 展示了各方法在HD-EPIC上的全面对比。EgoFlow（含梯度引导）在几乎所有指标上取得最优或接近最优的表现：

- **位置精度**：ADE 0.279、FDE 0.102，均优于GIMO（0.285 / 0.509）及其他基线，表明流匹配的确定性生成在轨迹精度上具有优势。
- **碰撞率**：EgoFlow的碰撞率仅为 **2.5%**，远低于GIMO的23.5%（绝对降低21个百分点），相对降幅约 **79%**。这一决定性差距直接验证了梯度引导物理优化的有效性——无引导版本的碰撞率为11.6%，加入引导后进一步降至2.5%。
- **旋转质量**：Geodesic 1.141，略高于GIMO的0.725，但结合碰撞率和位置精度来看，EgoFlow在物理合理性与精度之间取得了更均衡的折衷。

**跨数据集泛化。** Table 2 展示了在HOT3D上的零样本泛化结果。EgoFlow取得ADE 0.265，显著优于GIMO（约0.57），证明混合架构与流匹配范式对场景变化具有更强的鲁棒性。梯度引导在未见场景中同样有效，碰撞率保持低位。

### 消融实验

**输入模态消融（Table 3 上部分）。** 逐一移除各输入条件，观察性能变化：
- **移除场景点云**导致ADE/FDE最大幅度的上升，验证了局部几何信息对精确位置预测的关键作用。
- **移除目标位姿条件**同样显著恶化ADE/FDE，说明目标引导对于长程轨迹的终点约束不可或缺。
- **移除物体类别或任务文本**的影响相对较小，但仍有可观测的退化，表明语义信息对运动意图的辅助作用。

**梯度引导消融（Table 3 下部分）。** 逐步移除各物理代价项：
- **移除碰撞避免项（I_coll）**后，碰撞率从2.5%急剧上升至11.6%，证明SDF碰撞惩罚是保证物理合理性的决定性因素。
- **移除旋转一致性项（I_rot）**导致旋转突变增加，Geodesic距离恶化。
- **移除速度平滑项（I_vel）**使平移轨迹出现更多抖动，Frechet距离上升。
- 三项联合使用的效果优于任意单一或两两组合，验证了物理代价之间的互补性。

**架构消融（Table 4）。** 搜索不同 Mamba-Transformer-Mamba 层数配置：
- **3-6-3配置**在所有指标上取得最佳折衷（ADE 0.279, FDE 0.102, 碰撞率2.5%）。
- 减少Transformer层数（如3-3-3）导致跨模态融合不足，ADE上升。
- 进一步增加层数（如4-8-4）未带来持续提升，表明当前配置已充分捕获时序与跨模态依赖。
- 仅使用纯Mamba或纯Transformer的变体均不如混合架构，验证了双向Mamba的时序编码能力与Perceiver Transformer的跨模态注意力之间存在协同效应。

### 定性分析

**HD-EPIC 定性对比（Figure 3）。** 在多个场景中，EgoFlow生成的轨迹（橙色）相比GIMO、CHOIS等基线更接近真值（蓝色），且路径更加平滑自然。尤其在障碍物密集的厨房场景中，EgoFlow能绕过台面、电器等固定物体到达目标，而基线方法常出现穿透障碍物或绕远路的现象。

**HOT3D 跨场景泛化（Figure 4）。** 在未见过的场景布局中，EgoFlow展现出更强的几何一致性：生成的轨迹能适应新的障碍物分布，保持物理合理性，而基线方法在零样本条件下轨迹质量明显下降。

### 失败模式与局限性

尽管EgoFlow在碰撞避免和平滑性上取得显著进展，仍存在以下局限：
1. **静态场景假设**：当前方法仅针对静态场景中的刚体轨迹生成，无法处理可变形物体或动态障碍物。
2. **开环生成**：未集成闭环感知反馈，难以适应实时的环境变化（如物体被移动）。
3. **与执行解耦**：生成的轨迹尚未与机器人操作策略耦合，需进一步连接从轨迹到关节动作的映射。
4. **旋转精度权衡**：在Geodesic距离上略逊于GIMO，表明梯度引导在旋转平滑性与精确拟合真值旋转之间存在一定的权衡，需要手动验证具体场景下的表现。

### 补充图表

![[assets/figures/papers/paper_list_l28_https_openaccess_thecvf_com_content_CVPR2026_html_Saroha_EgoFlow_Gradien/figures/003_Figure_3.jpg]]
*Figure 3: HD-Epic Qualitative Result. The trajectory in green in each image is the history followed by the respective prediction by the various baselines and the ground truth. We can see that not ony our method generates a plausible trajectory to the end goal, it also takes a rather more natural and smooth path to the target pose*

![[assets/figures/papers/paper_list_l28_https_openaccess_thecvf_com_content_CVPR2026_html_Saroha_EgoFlow_Gradien/figures/004_Figure.jpg]]
*Figure: Task Prompt: pick the cellphone on the table. Task Prompt: pick the potato masher on the table*

![[assets/figures/papers/paper_list_l28_https_openaccess_thecvf_com_content_CVPR2026_html_Saroha_EgoFlow_Gradien/figures/005_Table_2.jpg]]
*Table 2: Cross-dataset evaluation. Following the setup of [51], we compare EgoFlow against the baselines on HOT3D dataset after training on Ego-Exo4D, thus demonstrating our superior performance on unseen scenes and cross-dataset generalization*

![[assets/figures/papers/paper_list_l28_https_openaccess_thecvf_com_content_CVPR2026_html_Saroha_EgoFlow_Gradien/figures/006_Table_1.jpg]]
*Table 1: Quantitative Results: HD-EPIC We compare model performance on various metrics on the HD-EPIC dataset. We can observe that our method performs the best against the baselines, while adding guidance sampling significantly reduces its collision rate. The results are averaged over 3 runs for EgoFlow*

![[assets/figures/papers/paper_list_l28_https_openaccess_thecvf_com_content_CVPR2026_html_Saroha_EgoFlow_Gradien/figures/007_Table_3.jpg]]
*Table 3: Input and Guidance Ablation. Ablation analysis on HD-EPIC assessing input conditioning modalities (top) and gradient guidance costs (bottom)*

![[assets/figures/papers/paper_list_l28_https_openaccess_thecvf_com_content_CVPR2026_html_Saroha_EgoFlow_Gradien/figures/008_Table_4.jpg]]
*Table 4: Architecture Ablation. Study of different layer configurations (Mamba-Transformer-Mamba layers) on HD-EPIC*

## 方法谱系与知识库定位

### 生成范式演进：从扩散模型到流匹配

EgoFlow 的核心范式选择——以**流匹配（Flow Matching）**替代扩散模型——反映了生成式轨迹建模从随机微分方程向确定性传输场的转向。现有基线普遍采用扩散范式：**GIMO**（Zheng et al., ECCV 2022）使用自回归 Transformer 逐帧生成轨迹，缺乏全局概率建模；**CHOIS**（Jiaman Li et al., ECCV 2024）和 **EgoScaler**（Yoshida et al., CVPR 2025）均基于条件扩散模型，通过逐步去噪生成轨迹。扩散模型的本质瓶颈在于其随机采样过程需要大量去噪步骤，且难以在推理时注入显式物理约束而不破坏生成分布。

EgoFlow 将轨迹生成重新定义为在 $\mathbb{R}^9$ 空间中学习确定性速度场 $\mathbf{v}_\theta$，通过线性插值路径 $\mathbf{x}_t = (1-t)\mathbf{x}_0 + t\mathbf{x}_1$ 训练网络直接预测从噪声指向干净数据的方向向量（Eq. 4-5）。这一设计使得推理仅需 20 步欧拉积分（Eq. 6），远少于扩散模型的数百步采样。更关键的是，确定性速度场为**梯度引导物理优化**提供了天然接口——在每个积分步对预测速度执行 50 步梯度下降，注入可微分碰撞成本与运动平滑代价（Eq. 7-11），而无需重训练网络。这种“数据驱动先验 + 物理约束解耦”的架构，与 **ManiFlow**（基于流匹配的操作策略基线）共享范式基础，但 EgoFlow 首次将其系统性地应用于自我中心场景下的 6DoF 物体轨迹生成。

### 架构设计的谱系定位

EgoFlow 的混合 **Mamba-Transformer-Perceiver** 架构代表了序列建模与多模态融合两条技术路线的交汇。纯 Transformer 基线（如 GIMO）在长序列建模中面临二次复杂度瓶颈；纯 Mamba 基线虽能高效处理时序依赖，但在跨模态注意力方面能力有限。EgoFlow 的三阶段设计——双向 Mamba 编码时序上下文（Stage 1）、Perceiver Transformer 执行跨模态注意力融合场景条件（Stage 2）、双向 Mamba 细化轨迹特征（Stage 3）——本质上是对这两类架构的**功能性解耦与协同**。

消融实验（Table 4）验证了这一设计的必要性：3 层 Mamba-6 层 Transformer-3 层 Mamba 的配置在所有指标上达到最优折衷（ADE 0.279, FDE 0.102, 碰撞率 2.5%），进一步增加层数未带来持续提升。这表明三阶段架构已充分捕获了时序依赖与跨模态交互的关键信息，额外容量可能导致过拟合。值得注意的是，Perceiver 组件使用 FiLM 调制将条件向量 $\mathbf{u}$ 注入 Mamba 层的特征变换，这一设计借鉴了条件生成领域对自适应特征调制的研究，但在轨迹生成任务中首次与状态空间模型结合。

### 物理约束实施的技术定位

EgoFlow 的梯度引导采样机制在物理约束实施的光谱上占据独特位置。传统方法或完全依赖数据隐式学习物理规律（如 GIMO 无显式物理约束），或采用后处理过滤（如碰撞检测后剔除不可行轨迹），前者在遮挡和复杂场景下失效，后者破坏了生成分布的完整性。EgoFlow 通过三个可微分代价项——基于 SDF 的碰撞惩罚 $\mathcal{T}_{\mathrm{coll}}$（Eq. 9）、旋转方向连续性成本 $\mathcal{T}_{\mathrm{rot}}$（Eq. 10）、平移加速度平滑成本 $\mathcal{T}_{\mathrm{vel}}$（Eq. 11）——在采样过程中**动态优化**轨迹，而非简单拒绝采样。

这一设计的决定性证据来自消融实验（Table 3）：移除碰撞避免项后，碰撞率从 2.5% 急剧上升至 11.6%，相对恶化约 364%。旋转和平滑项虽对碰撞率影响较小，但单独移除任一项均导致 ADE/FDE 上升，说明它们通过约束运动平滑性间接提升了位置预测精度。与依赖强化学习或轨迹优化的物理约束方法相比，EgoFlow 的梯度引导无需额外环境交互或优化器调参，其超参数（HD-EPIC: $\lambda_{\mathrm{rot}}=\lambda_{\mathrm{vel}}=2.0$; HOT3D: $\lambda_{\mathrm{rot}}=\lambda_{\mathrm{vel}}=5.0$）仅需按数据集独立微调，在同一数据集内保持一致。

### 适用边界与局限

EgoFlow 的适用边界由其技术假设严格界定：

1. **静态场景假设**：碰撞成本基于预计算的 SDF，仅能处理固定障碍物。无法应对动态障碍物或人-物交互过程中的场景变化，这限制了其在真实人机协作场景中的应用。

2. **刚体运动假设**：轨迹表示 $\mathbf{x}_t = [\mathbf{p}_t; \mathbf{r}_t] \in \mathbb{R}^9$ 仅编码 3D 位置与 6D 连续旋转，无法描述可变形物体的形态变化或抓取过程中的物体形变。

3. **开环生成假设**：模型一次性生成完整未来轨迹（输入 30% 历史，预测剩余 70%），未集成闭环感知反馈。在真实机器人执行中，环境观测的逐步到达无法被利用来在线调整轨迹。

4. **数据分布依赖**：跨数据集泛化实验（Table 2）虽显示 EgoFlow 在 HOT3D 上优于基线（ADE 0.265 vs GIMO ≈0.57），但其性能仍受限于训练数据覆盖的场景类型与物体类别。对完全未见的环境布局，SDF 碰撞引导的可靠性取决于场景重建精度。

### 开放问题与后续方向

基于上述局限，EgoFlow 框架的扩展方向包括：

- **动态场景扩展**：如何将 SDF 碰撞成本替换为时变占用场，使梯度引导能处理移动障碍物？这可能需要引入场景流预测模块或在线重建组件。

- **可变形物体支持**：将轨迹表示从 $\mathbb{R}^9$ 扩展至包含物体关键点或隐式形状参数的高维空间，同时重新设计物理代价函数以惩罚不合理的形变。

- **闭环策略集成**：将 EgoFlow 的轨迹生成能力与机器人操作策略学习耦合，使生成的物理一致轨迹可直接作为策略的参考运动，或通过逆运动学转化为关节动作序列。这需要解决轨迹表示与动作空间之间的映射问题。

- **感知-生成联合优化**：当前框架将场景点云作为固定条件输入，未来可探索端到端地从 RGB-D 视频直接生成轨迹，使感知模块的特征提取与轨迹生成联合优化，减少中间表示的误差累积。

## 原文 PDF

![[paperPDFs/CVPR_2026/EgoFlow_Gradient_Guided_Flow_Matching_for_Egocentric_6DoF_Object_Motion_Generation.pdf]]