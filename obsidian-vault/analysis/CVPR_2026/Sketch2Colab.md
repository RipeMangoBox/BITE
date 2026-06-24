---
title: Sketch2Colab
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Sketch2Colab.pdf
aliases:
- Sketch2Colab
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: 通过蒸馏得到的整流流学生模型配合能量引导与CTMC离散相位调度，在训练和采样过程中直接塑造数据流形来强制满足各类约束，从而大幅提升约束遵守精度和推理效率。
primary_logic: 将扩散教师蒸馏为整流流学生，并利用可微能量函数（关键帧、轨迹、接触、碰撞）的梯度以及CTMC驱动的接触/交接调度，可以实现对稀疏草图多约束的精确控制，而不依赖缓慢的后验引导。
claims:
- Differentiable energies over keyframes, trajectories, and physics-based constraints directly shape the student’s transport field, steering samples toward motions that faithfully s...
- "Removing energy guidance produces the largest drop in performance: realism and stance worsen by around 15–20%, trajectory and objectposition errors increase by roughly 25–30%, anc..."
- Disabling CTMC scheduling mainly harms temporal phasing—foot-skate and trajectory errors rise by roughly 10–20%, with anchor errors up by around 30% and penetration by about 20%.
- A CTMC-based discrete-event planner schedules touches, grasps, and handoffs, modulating the dynamics to produce crisp, well-phased human–object–human collaborations.
---

# Sketch2Colab

> [!tip] 核心洞察
> 将扩散教师蒸馏为整流流学生，并利用可微能量函数（关键帧、轨迹、接触、碰撞）的梯度以及CTMC驱动的接触/交接调度，可以实现对稀疏草图多约束的精确控制，而不依赖缓慢的后验引导。

| 字段 | 内容 |
|------|------|
| 中文题名 | Sketch2Colab：基于可控流蒸馏的草图条件多人动画生成 |
| 英文题名 | Sketch2Colab |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.02190) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Sketch2Colab |
| Dataset | CORE4D |

> [!tip] 效果简介
> - CORE4D (Average protocol, w/ text) 上，FID↓ 0.480 vs 0.623 (COLLAGE teacher) (0.143 (23%))。
> - CORE4D (Sketch-only) 上，FID↓ 0.509 vs 0.735 (COLLAGE) (0.226 (30.6%))；FID↓ 0.509 vs 1.025 (SKETCH2ANIM-INT) (0.516 (50.3%))。
> - CORE4D (Average protocol) 上，Foot-skate↓ ~24% lower than COLLAGE teacher vs COLLAGE teacher (~24%)。

## 概述

**问题瓶颈**：现有扩散模型在多实体交互场景中难以精确满足稀疏草图所施加的多重约束——包括关键帧对齐、关节轨迹跟踪、接触一致性及碰撞避免——且推理速度慢，无法在保持生成质量的同时实现对多约束的严格遵循。

**核心思路**：Sketch2Colab 将草图驱动的扩散先验蒸馏为高效的整流流（rectified flow）学生模型，并引入可微能量函数与连续时间马尔可夫链（CTMC）相位调度器，在训练和采样过程中直接塑造数据流形以强制满足各类约束，从而大幅提升约束遵守精度和推理效率。

**方法定位**：该方法处于“条件运动生成 × 可控蒸馏 × 物理感知引导”的交叉点。其冻结的扩散教师源自 **COLLAGE**（Daiya et al., ICRA 2025），而草图条件编码范式可对比 **SKETCH2ANIM-INT**（Zhong et al., TOG 2025）。Sketch2Colab 的关键改造体现在三个层面：（1）将扩散采样替换为整流流 ODE 学生采样；（2）用可微能量函数（关键帧、轨迹、接触、碰撞、物理）的梯度直接塑造学生输运场，替代仅依赖分类器自由引导的约束方式；（3）引入 CTMC 驱动的离散接触/交接相位调度，显式控制交互时序。

**主要结果**：在 CORE4D 基准上，Sketch2Colab 在仅草图条件下相较 COLLAGE 教师 FID 降低 30.6%，相较 SKETCH2ANIM-INT 降低 50.3%；同时足部滑动降低约 24%，锚点误差降低约 45%。消融实验表明，移除能量引导会造成真实感与姿态误差上升 15–20%、轨迹与物体位置误差上升 25–30%、锚点误差翻倍；禁用 CTMC 调度则主要损害时序相位，导致足部滑动和轨迹误差上升 10–20%、穿透增加约 20%。

**局限与开放问题**：当前方法的物体交互局限于 CORE4D 数据集的有限类别，且侧重人手与物体的单点交互；对重度草图噪声或自相交轨迹等极端情况仍可能出现漂移、浮空或碰撞失败。如何扩展至任意网格与物理属性、实现多人多物协同操控，以及摆脱对扩散教师先验的依赖，是后续研究的关键方向。

## 背景与动机

### 问题场景：从稀疏草图到多人交互动画

在计算机动画与具身智能的交汇处，一个核心挑战是根据稀疏的二维故事板草图生成高质量的三维多人交互运动。用户只需提供少量关键帧姿态、关节轨迹和物体掩码，系统便需自动合成符合物理规律、满足接触一致性且时序精确的多人-物体-多人（Human-Object-Human, HOH）协同动画。这类任务广泛存在于动画预演、游戏内容生成和人机交互仿真中，其本质是在高维运动流形上求解一个多重约束的生成问题。

### 现有方法的瓶颈

当前主流的扩散模型（如 **COLLAGE**, Daiya et al., ICRA 2025）虽然能够生成多样化的多实体交互运动，但在稀疏草图约束下暴露出两个结构性瓶颈：

1. **约束遵循精度不足**：扩散模型依赖分类器自由引导和条件注入（如 ControlNet）来施加控制信号，但这些机制本质上属于隐式引导，缺乏对关键帧对齐、关节轨迹跟踪、接触一致性和碰撞避免等显式几何约束的精确建模能力。当故事板仅提供稀疏快照和路径时，模型常常无法在指定时刻触发交互动作，也难以保证人手与物体的精确接触。

2. **推理效率与质量矛盾**：若采用后验引导方式（如推理时梯度修正）来改善约束遵循，则采样速度会急剧下降，且容易陷入引导强度与样本质量之间的权衡困境。这使得扩散模型难以在保持感知质量的同时实现对多约束的严格满足。

此外，现有草图驱动方法（如 **SKETCH2ANIM-INT**, Zhong et al., TOG 2025）主要面向单人运动生成，扩展到多人交互场景时缺乏对离散接触事件（触碰、抓取、交接）的显式时序调度机制，导致交互相位模糊、足部滑动和穿透问题频发。

### 核心动机

上述瓶颈指向一个根本性的方法论缺口：**如何在生成模型的训练和采样过程中，直接塑造数据流形以强制满足稀疏草图的多重约束，而非依赖缓慢的后验修正？** 这需要同时解决三个子问题：

- **连续运动与离散事件的耦合**：多人交互中的触碰、抓取、交接等事件本质上是离散状态转换，而人体运动是连续轨迹，两者必须精确对齐时序。
- **多约束能量的可微注入**：关键帧、轨迹、接触、碰撞等约束需转化为可微能量函数，并将其梯度直接嵌入生成动力学，使采样过程天然趋向约束满足。
- **推理效率保障**：能量引导不应以牺牲采样速度为代价，需在训练阶段完成约束塑造，推理时保持高效的前向 ODE 求解。

Sketch2Colab 正是在这一动机下，提出以蒸馏得到的整流流学生模型为核心，配合能量引导与 CTMC 离散相位调度，实现约束精度与推理效率的双重突破。

## 核心创新

Sketch2Colab 的核心创新在于将多约束、多实体的草图条件动画生成从“扩散采样+后验引导”的范式，重构为“整流流蒸馏+能量塑形+离散事件调度”的耦合系统。其与基线方法的本质差异可归结为三个关键维度的机制替换。

### 从扩散采样到整流流蒸馏

现有方法（如 **COLLAGE**，Daiya et al., ICRA 2025）依赖扩散模型（DDPM/DDIM）的迭代去噪采样，推理速度慢且在稀疏草图约束下难以精确收敛。Sketch2Colab 首先训练一个草图驱动的扩散教师，随后将其蒸馏为一个在潜在空间中运行的整流流学生（rectified-flow student），学生通过 ODE 采样实现快速、稳定的推理。这一替换的因果机制在于：整流流学生直接学习从噪声到数据的直线传输路径，配合蒸馏损失 $\mathcal{L}_{\mathrm{distil}}(\phi)$ 拟合冻结教师的概率流速度场 $v_{\theta}^{\mathrm{PF}}$，使得采样步数大幅减少而不牺牲生成质量。实验表明，在 CORE4D 基准上，Sketch2Colab 的 FID 相较 COLLAGE 教师降低约 23%（0.480 vs 0.623），且推理速度显著提升。

### 从条件注入到能量塑形

基线方法通常仅通过分类器自由引导和条件注入（如 ControlNet）来施加草图约束，缺乏对关键帧对齐、关节轨迹跟踪、接触一致性和碰撞避免等精细要求的显式建模。Sketch2Colab 引入了一套可微能量函数体系，包括关键帧对齐能量（3D/2D）、轨迹跟踪能量（3D/2D）、接触/间距能量以及物理约束能量（足部滑动、地面穿透、运动平滑性）。这些能量的梯度通过学习的低秩块-Toeplitz Jacobian 代理 $\mathbf{B}_{\rho}$ 从运动空间反向传播到潜在空间，形成原始空间引导向量 $\mathbf{\sigma}^{\mathrm{g}}_{\mathrm{raw}}(\mathbf{z})$，直接塑造学生传输场的方向。同时，Lyapunov 损失 $\mathcal{L}_{\mathrm{Lyap}}$ 强制学生速度场成为总势能的下降方向，确保生成轨迹向约束满足区域收敛。消融实验提供了决定性证据：移除能量引导导致真实感和姿态误差上升 15–20%，轨迹与物体位置误差上升 25–30%，锚点误差翻倍，穿透增加约 16%——这是所有消融中性能下降最剧烈的操作。

### 从隐式接触到时序显式调度

现有方法缺乏对多人-物交互中离散事件（接触、抓取、交接）时序的显式建模，模型只能隐式学习接触时机，导致接触相位模糊、交接不连贯。Sketch2Colab 引入一个基于连续时间马尔可夫链（CTMC）的轻量级离散事件规划器，通过 Kolmogorov 前向方程学习相位占有概率 $\pi_t$ 的演化，产生相位混合权重以调制整流流学生的子场。CTMC 损失 $\mathcal{L}_{\mathrm{CTMC}}(\eta)$ 强制相位占有概率满足主方程，并附加熵正则器以促进清晰的模式切换。这一设计使得接触、抓取和交接等离散事件被精确调度，从而产生时序分明的人-物-人协作运动。消融实验表明，禁用 CTMC 调度主要损害时序相位：足部滑动和轨迹误差上升 10–20%，锚点误差上升约 30%，穿透增加约 20%。Figure 5 进一步揭示了 CTMC 的因果机制：它向外推移了 F1-FMD Pareto 前沿，同时降低了碰撞率，并显著改善了接触时序校准（更低的 ECE）。

### 创新耦合的系统效应

上述三个 changed slots 并非孤立运作，而是通过联合训练总损失 $\mathcal{L}$ 形成耦合增益。能量引导提供了逐采样步的约束梯度信号，CTMC 调度器决定了不同交互相位的能量权重分配，而整流流学生则提供了高效的前向传输基底。三者协同使得 Sketch2Colab 在仅依赖稀疏故事板草图（无文本条件）的情况下，生成的多人-物运动能够严格遵循关键帧时序、关节/端点轨迹以及物体对齐与接触要求——这是现有扩散基线无法实现的控制精度。

## 整体框架

Sketch2Colab 的目标是从稀疏的故事板草图（关键帧、关节轨迹、物体掩码）和可选文本提示出发，生成包含多人与多物体的时序连贯 3D 运动序列。整个 pipeline 围绕一个核心设计展开：**将扩散教师蒸馏为整流流学生，并通过双空间能量引导与 CTMC 离散相位调度，在快速 ODE 采样过程中精确满足多重稀疏约束**。

### 输入与输出

- **输入**：用户提供 $K$ 个关键帧草图（含 2D 关节点位置）、每个关节的 2D 轨迹路径、物体掩码，以及可选的文本描述。
- **输出**：$N$ 帧的 3D 运动序列，包含 $H$ 个人体的关节位置/旋转、$O$ 个物体的 6-DoF 位姿及其锚点位置，总状态维度由 Eq. (1) 定义：
  $$D_{\mathtt{full}} = H \cdot J \cdot (3 + 6) + O \cdot (3 + 4) + \sum_{o=1}^{O} K_o \cdot 3$$

### Pipeline 六阶段

Figure 2 展示了从故事板到最终 3D 运动的完整架构，可分解为六个阶段：

![[assets/figures/papers/paper_list_l1754_Sketch2Colab/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of Sketch2Colab: storyboard→3D HOH motion (⃝1 –⃝6 ). ⃝1 The user provides sketches (keyframes, per-joint 2D paths, object masks) and an optional text prompt; ⃝2 paired 2D/3D encoders produce aligned embeddings and 3D proxies, which are fused into C; ⃝3 a PF-distilled rectified-flow student*

**① 草图编码与 3D 代理生成**  
2D/3D 对齐编码器将关键帧、轨迹和物体掩码分别映射到共享嵌入空间。2D 编码器提取草图的视觉特征，3D 编码器则生成对应的 3D 代理（如 3D 关键帧位置、轨迹点和物体锚点），为后续条件提供几何参照。对齐通过 L2 损失与对比损失实现模态不变性（Eq. (2)）：
$$\mathcal{L}_{\mathrm{align}} = \sum_{y \in \{k, \tau, o\}} \Vert \mathbf{s}_y^{\mathrm{3D}} - \mathbf{s}_y^{\mathrm{2D}} \Vert_2^2 + \lambda_c \mathcal{L}_{\mathrm{InfoNCE}}(y)$$

**② 条件融合与实体图注意力**  
对齐后的嵌入与 3D 代理被融合为统一的条件表示 $\mathcal{C}$。融合过程中，实体图注意力机制利用代理间的空间距离偏置，使信息流倾向于空间邻近的人体和物体锚点（Eq. (3)）：
$$\mathrm{Attn}_t = \mathrm{Softmax}\Big( \frac{\mathbf{Q}_t \mathbf{K}_t^{\top}}{\sqrt{d_h}} - \lambda \mathbf{D} \Big) \mathbf{V}_t$$

**③ 整流流学生 ODE 采样**  
核心生成器是一个在 VQ-VAE 潜在空间中运行的整流流学生 U-Net $v_{\phi}(\mathbf{z}, t \mid \mathcal{C})$。该学生由冻结的扩散教师蒸馏得到：教师提供概率流速度场 $v_{\theta}^{\mathrm{PF}}$（Eq. (4)），学生通过蒸馏损失（Eq. (6)）直接拟合该速度场，同时辅以整流流匹配损失（Eq. (5)）确保沿直连线方向演化。学生 U-Net 内部集成了时间门控关键帧适配器和轨迹 ControlNet 分支，用于注入草图条件。

**④ CTMC 相位调度**  
一个轻量级的连续时间马尔可夫链（CTMC）规划器在离散接触/交接状态（如触摸、抓取、传递）之间调度相位占有概率 $\pi_t$。$\pi_t$ 通过调制学生子场和接触权重，控制不同交互阶段的激活时机，使生成的接触动作清晰且时序准确。CTMC 通过 Kolmogorov 前向方程和熵正则器进行训练（Eq. (9)）。

**⑤ 双空间能量引导**  
这是约束满足的关键机制，包含两个互补的引导信号：
- **潜在锚点引导**：在潜在空间中保持整体运动一致性。
- **原始空间能量引导**：在运动空间定义可微能量函数（关键帧对齐、轨迹跟踪、接触一致性、碰撞避免、物理约束），通过学习的低秩 Toeplitz Jacobian 代理 $\mathbf{B}_{\rho}$ 将能量梯度反向传播到潜在空间（Eq. (7)）：
  $$\mathbf{\sigma}^{\mathrm{g}}_{\mathrm{raw}}(\mathbf{z}) = \mathbf{B}_{\rho} \nabla_{\mathbf{M}_{1:N}} \left( \sum_r \lambda_r E_r(\Pi(\mathbf{z})) \right)$$
  两种引导信号在 ODE 更新中联合施加，Lyapunov 损失（Eq. (8)）则强制学生速度场沿总势能的下降方向演化。

**⑥ 解码与联合优化**  
冻结的 VQ-VAE 解码器 $\mathcal{D}$ 将潜在序列解码为完整的 3D 多人/物运动序列。整个系统通过联合训练目标（Eq. (10)）端到端优化：
$$\mathcal{L} = \mathcal{L}_{\mathrm{RF}} + \lambda_{\mathrm{dist}}\mathcal{L}_{\mathrm{distill}} + \lambda_{\mathrm{Lyap}}\mathcal{L}_{\mathrm{Lyap}} + \sum_r \lambda_r \mathcal{L}_{E_r} + \lambda_{\mathrm{lat}}\mathcal{L}_{\mathrm{lat}} + \lambda_{\mathrm{CTMC}}\mathcal{L}_{\mathrm{CTMC}} + \lambda_{\mathrm{cons}}\mathcal{L}_{\mathrm{consist}}$$

### 核心因果机制

该框架的瓶颈突破在于**将约束满足从缓慢的后验引导转移到训练和采样过程中**：能量函数在训练时通过 Lyapunov 损失塑造学生的输运场方向，在采样时通过 Jacobian 代理提供实时梯度引导；CTMC 则解耦了连续运动生成与离散交互相位的调度，使两者各司其职。消融实验证实了这一设计的因果效力——移除能量引导导致真实感和姿态误差上升 15–20%，轨迹与物体位置误差上升 25–30%，锚点误差翻倍；禁用 CTMC 则使足部滑动和轨迹误差上升 10–20%，锚点误差上升约 30%。

### 与基线方法的差异

相较于主要对比基线 **COLLAGE**（Daiya et al., ICRA 2025）的纯扩散采样和无显式约束引导，Sketch2Colab 在三个关键维度上进行了替换：生成模型从扩散模型变为蒸馏整流流学生，约束实现从条件注入变为双空间能量引导，并新增了 CTMC 离散事件调度器。这些改动使其在 CORE4D 基准上实现了 FID 相对降低 23–50%、足部滑动降低约 24%、锚点误差降低约 45% 的显著提升。

### 补充图表

![[assets/figures/papers/paper_list_l1754_Sketch2Colab/figures/001_Figure_1.jpg]]
*Figure 1: Sketch-conditioned human–object–human (HOH) demonstrations with Sketch2Colab. Left→right: (a) Two people co-manipulate a table while following a sketched path; midway the model switches handling so that one character disengages and the other finishes the placement, showing that Sketch2Colab can start/stop agent motion based on joint/body trajectory cues. (b) Cooperative transport of a large box along a prescribed trajectory with on-the-fly height adjustment before placing it down. (c) A specified hand must grasp a canister and then follow a complex path. In all cases, the system is driven only by sparse storyboard keyframes (no text conditioning); the generated motions respect the keyframe...*

## 核心模块与公式推导

Sketch2Colab 的生成管线由六个核心模块串联而成，其设计围绕一个中心思想：**将冻结的扩散教师蒸馏为整流流学生，并在训练与采样过程中通过可微能量函数和 CTMC 离散调度器直接塑造数据流形**，从而在稀疏草图约束下实现精确、物理合理且高效的多人-物交互运动生成。

### 3.1 2D/3D 对齐编码器与实体图注意力

用户提供的分镜草图包含三类信息：关键帧（keyframes）、关节轨迹（trajectories）和物体掩码（object masks）。系统首先通过**成对的 2D/3D 编码器**将这些异构输入映射到共享嵌入空间，同时生成 3D 代理（proxies）用于后续条件注入。对齐损失由 L2 项和对比项构成：

$$
\mathcal{L}_{\mathrm{align}} = \sum_{y \in \{k, \tau, o\}} \Vert \mathbf{s}_y^{\mathrm{3D}} - \mathbf{s}_y^{\mathrm{2D}} \Vert_2^2 + \lambda_c \mathcal{L}_{\mathrm{InfoNCE}}(y)
$$

其中 $k$、$\tau$、$o$ 分别对应关键帧、轨迹和物体模态，$\mathbf{s}_y^{\mathrm{3D}}$ 与 $\mathbf{s}_y^{\mathrm{2D}}$ 为同一实体的 3D 和 2D 嵌入。该损失强制模态不变性，使草图的 2D 笔触与 3D 空间语义在嵌入空间中保持一致。

融合后的条件表示 $\mathcal{C}$ 进入**实体图注意力**模块，其注意力权重由实体间空间距离偏置调制：

$$
\mathrm{Attn}_t = \mathrm{Softmax}\Big( \frac{\mathbf{Q}_t \mathbf{K}_t^{\top}}{\sqrt{d_h}} - \lambda \mathbf{D} \Big) \mathbf{V}_t
$$

$\mathbf{D}$ 为实体 token 间的成对距离矩阵，$\lambda$ 控制距离惩罚强度。这一设计使信息流倾向于空间邻近的代理和物体锚点，为多人-物交互中的局部依赖建模提供归纳偏置。

### 3.2 整流流学生与概率流蒸馏

运动生成在层级式 VQ-VAE 的潜在空间中进行。完整场景状态维度定义为：

$$
D_{\mathtt{full}} = H \cdot J \cdot (3 + 6) + O \cdot (3 + 4) + \sum_{o=1}^{O} K_o \cdot 3
$$

其中 $H$ 为人数，$J$ 为关节数，$O$ 为物体数，$K_o$ 为第 $o$ 个物体的锚点数；$(3+6)$ 对应关节的 3D 位置与 6D 旋转表示，$(3+4)$ 对应物体的 3D 位置与四元数姿态。

**扩散教师**（冻结）提供概率流速度场作为蒸馏目标：

$$
v_{\theta}^{\mathrm{PF}}(\mathbf{z}_t, t \mid \mathcal{C}) = \frac{d\bar{\alpha}_t}{dt} \frac{\mathbf{z}_t - \sqrt{1-\bar{\alpha}_t} \hat{\epsilon}_{\theta}}{\sqrt{\bar{\alpha}_t}} - \frac{d(1-\bar{\alpha}_t)}{dt} \frac{\hat{\epsilon}_{\theta}}{2\sqrt{1-\bar{\alpha}_t}}
$$

该闭式速度场由教师的去噪预测 $\hat{\epsilon}_{\theta}$ 和噪声调度参数 $\bar{\alpha}_t$ 导出。

**整流流学生**（U-Net 架构，含时间门控关键帧适配器和轨迹 ControlNet 分支）同时受两个目标监督：

- **整流流匹配损失**：使学生的速度场 $\mathbf{v}_{\phi}$ 匹配噪声点 $\mathbf{z}_0$ 与数据点 $\mathbf{z}_1$ 之间的直连线方向：
  $$
  \mathcal{L}_{\mathtt{RF}}(\phi) = \mathbb{E}_{t, \mathbf{z}_0, \mathbf{z}_1} \left\| \mathbf{v}_{\phi}(\mathbf{z}_t, t \mid \mathcal{C}) - (\mathbf{z}_1 - \mathbf{z}_0) \right\|_2^2
  $$

- **概率流蒸馏损失**：使学生速度场直接拟合教师概率流速度场：
  $$
  \mathcal{L}_{\mathrm{distil}}(\phi) = \mathbb{E}_{t, \mathbf{z}_t} \Vert v_{\phi}(\mathbf{z}_t, t \mid \mathcal{C}) - v_{\theta}^{\mathrm{PF}}(\mathbf{z}_t, t \mid \mathcal{C}) \Vert_2^2
  $$

双损失联合训练使学生既继承了教师的生成质量，又获得了 ODE 采样的高效推理能力。

### 3.3 双空间能量引导

约束遵循的核心机制是**双空间引导**：潜在空间锚点保持整体一致性，原始空间能量梯度提供精确的几何约束满足。

**原始空间引导向量**通过学习的低秩、块 Toeplitz Jacobian 代理 $\mathbf{B}_{\rho}$ 将运动空间的能量梯度反向传播到潜在空间：

$$
\mathbf{\sigma}^{\mathrm{g}}_{\mathrm{raw}}(\mathbf{z}) = \mathbf{B}_{\rho} \nabla_{\mathbf{M}_{1:N}} \left( \sum_r \lambda_r E_r(\Pi(\mathbf{z})) \right)
$$

其中 $\Pi(\mathbf{z})$ 为冻结 VQ-VAE 解码器将潜在序列映射回 3D 运动，$E_r$ 为各项可微能量函数。

**能量函数族**包括：
- **关键帧对齐能量** $E_{\mathrm{key}}$：由 3D 项 $E_{\mathrm{key}}^{\mathrm{3D}}$（使用 3D 代理目标）和 2D 项 $E_{\mathrm{key}}^{\mathrm{2D}}$（含时间门控权重）组成，确保生成运动在指定时刻精确匹配草图关键帧。
- **轨迹跟踪能量**：约束指定关节的 3D/2D 运动路径与草图轨迹一致。
- **接触与间距能量**：强制手-物接触点对齐，并维持合理的交互间距。
- **物理正则能量**：包括足部滑动惩罚、地面约束和平滑项，抑制非物理伪影。

**Lyapunov 损失**进一步将能量引导融入训练目标，强制学生速度场沿总势能（显式能量 + 学习潜力）的下降方向演化：

$$
\mathcal{L}_{\mathrm{Lyap}}(\phi, \psi) = \mathbb{E}_t\left[\left( \max\{0, \nabla_{\mathbf{z}}\mathcal{V}(\mathbf{z}, t) \cdot v_{\phi}(\mathbf{z}, t) + \kappa \|\nabla_{\mathbf{z}}\mathcal{V}(\mathbf{z}, t)\|_2^2 \} \right)^2 \right]
$$

该损失确保约束满足不是后验修正，而是生成动力学的内在属性。

### 3.4 CTMC 离散相位调度器

多人-物交互涉及离散事件（触碰、抓取、交接）的精确时序编排。系统引入**连续时间马尔可夫链（CTMC）调度器**，将接触/交接状态建模为离散相位，其占有概率 $\pi_t$ 满足 Kolmogorov 前向方程：

$$
\mathcal{L}_{\mathrm{CTMC}}(\eta) = \mathbb{E}_t \left\| \frac{d\pi_t}{dt} - \pi_t Q_{\eta}(\mathbf{h}_t) \right\|_2^2 + \beta \mathrm{Var}[A_t(Q_{\eta})]
$$

其中 $Q_{\eta}(\mathbf{h}_t)$ 为学习到的速率矩阵，由当前隐状态 $\mathbf{h}_t$ 参数化；第二项为熵正则器，防止相位切换过于频繁。CTMC 输出相位混合权重，调制学生子场和接触权重，实现清晰的接触/交接时序。

### 3.5 联合训练目标

完整训练目标将所有损失统一：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{RF}} + \lambda_{\mathrm{dist}}\mathcal{L}_{\mathrm{distill}} + \lambda_{\mathrm{Lyap}}\mathcal{L}_{\mathrm{Lyap}} + \sum_r \lambda_r \mathcal{L}_{E_r} + \lambda_{\mathrm{lat}}\mathcal{L}_{\mathrm{lat}} + \lambda_{\mathrm{CTMC}}\mathcal{L}_{\mathrm{CTMC}} + \lambda_{\mathrm{cons}}\mathcal{L}_{\mathrm{consist}}
$$

各项依次为：整流流匹配、概率流蒸馏、Lyapunov 约束满足、各能量代理损失、潜在对齐、CTMC 相位学习和一致性正则。该联合目标使约束遵循能力在训练阶段即被编码进学生速度场，无需推理时的缓慢后验引导。

> **证据强度说明**：以上公式均来自论文 Sec. 3.1–3.4 的明确定义，变量含义与原文一致。消融实验（Sec. 5）证实：移除能量引导导致真实感下降 15–20%、锚点误差翻倍；禁用 CTMC 调度使足部滑动和轨迹误差上升 10–20%；这些结果直接验证了各模块的因果贡献。

## 实验与分析

### 主实验结果

Sketch2Colab 在 CORE4D 基准上进行了系统评估，采用 Average protocol 并遵循 的关键帧/轨迹二维和三维误差评估标准。Table 1 汇总了主要对比结果。

![[assets/figures/papers/paper_list_l1754_Sketch2Colab/figures/003_Table_1.jpg]]
*Table 1: CORE4D: baselines and ablations (Average protocol). R-Precision(Higher is better); lower is better otherwise. Control accuracy follows [70] with Keypose/Trajectory in 2D and 3D. Cross-protocol[70] results and InterHuman[40] Metric comparison are provided in the supplementary (Supp. Sec. S.5)*

**与扩散教师 COLLAGE 的对比。** 在带文本条件的 Average protocol 下，Sketch2Colab 的 FID 为 0.480，相比 COLLAGE 教师（Daiya et al., ICRA 2025）的 0.623 降低了 23%。更重要的是，在仅使用草图条件（无文本）的场景下，Sketch2Colab 的 FID 为 0.509，而 COLLAGE 为 0.735，降幅达 30.6%（Table 2(a)）。这表明蒸馏后的整流流学生不仅推理更快，而且在稀疏草图条件下具有更强的约束遵循能力。

**与 SKETCH2ANIM-INT 的对比。** 在草图专用场景下，SKETCH2ANIM-INT（Zhong et al., TOG 2025）——将草图驱动单人生成方法扩展至交互场景的基线——FID 高达 1.025，Sketch2Colab 的 0.509 相对降低了 50.3%。这一巨大差距揭示了单人生成方法直接迁移至多实体交互场景时的根本性不足：缺乏对多代理空间关系、接触时序和协同约束的显式建模。

**物理合理性指标。** 在足部滑动（Foot-skate）指标上，Sketch2Colab 相比 COLLAGE 教师降低约 24%；在锚点误差（Anchor-Err）上降低约 45%。这些改进直接归因于可微能量函数（接触、碰撞、地面约束）对整流流学生运输场的塑造作用——能量梯度在采样过程中持续将样本推向物理合理的流形区域。

### 消融实验

Table 1 同时报告了系统的消融实验结果，揭示了各组件的因果贡献强度。

**能量引导（Energy Guidance）是最关键的组件。** 移除能量引导导致性能出现最大幅度的退化：真实感（realism）和姿态（stance）指标恶化约 15–20%，轨迹和物体位置误差上升约 25–30%，锚点误差几乎翻倍，穿透（penetration）增加约 16%。这一结果强有力地验证了核心设计洞察：可微能量函数通过 Lyapunov 损失直接塑造学生速度场的方向，是实现稀疏草图多约束精确遵循的因果旋钮，而非可选的辅助模块。

**CTMC 相位调度器对时序相位至关重要。** 禁用 CTMC 调度主要损害时序相关指标：足部滑动和轨迹误差上升约 10–20%，锚点误差上升约 30%，穿透增加约 20%。Figure 5 进一步揭示了 CTMC 的作用机制：(a) CTMC 将 F1–FMD Pareto 前沿向外推移，同时降低碰撞率；(b) 接触时序校准显著改善（ECE 降低）；(c) 流场在离散模式转换之外保持低曲率；(d) 能量梯度在转换点附近与基础流场建设性对齐，消除了梯度冲突。这说明 CTMC 并非简单的时序开关，而是通过调制子场和接触权重，使连续流场与离散事件在相位上精确耦合。

**COLLAGE grounding 提供布局先验。** 移除 COLLAGE grounding 导致物体和锚点误差上升 20–25%，穿透增加约 12%。这表明冻结扩散教师提供的概率流速度场包含了有价值的多实体空间布局先验，蒸馏过程有效保留了这一知识。

**统一适配器优于 Parallel ControlNets。** 将统一适配器替换为 Parallel ControlNets 导致真实感、控制和交互指标全面下降 10–25%。统一适配器通过实体图注意力机制（Eq. (3)）实现了空间邻近代理间的信息流动偏置，而并行 ControlNet 架构缺乏这种跨实体的协调能力。

**轨迹条件不足以替代关键帧快照和潜在锚点。** 仅使用轨迹条件（移除关键帧快照和潜在锚点）导致关键帧和轨迹误差上升 15–35%，物体和锚点误差上升 30–60%，穿透增加约 8%。这一消融表明，潜在锚点提供的整体一致性约束与原始空间能量提供的精确几何约束之间存在互补关系——单独依赖任一方都无法满足故事板的多粒度要求。

### 噪声鲁棒性与分布外泛化

Table 2(b,c) 报告了噪声鲁棒性实验。在约 60% 的草图噪声水平下（对应 Figure 4C 的极端案例），Sketch2Colab 仍保持显著优于基线的性能，但确实出现了漂移、浮空或碰撞失败。Figure 4(C–F) 展示了这些失败模式：自相交轨迹、分布外多物体场景和稀疏约束条件下，模型可能产生不自然的代理姿态或穿透。这些限制指向了系统对预训练扩散教师先验的依赖——当草图条件严重偏离训练分布时，教师提供的概率流速度场可能指向不可靠的区域。

![[assets/figures/papers/paper_list_l1754_Sketch2Colab/figures/005_Table_2.jpg]]
*Table 2: Storyboard (sketch-only unless specified) HOH on CORE4D[67]. Noise levels ≈ 60% correspond to Fig. 4C*

![[assets/figures/papers/paper_list_l1754_Sketch2Colab/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative motion frames, trajectories, and limitations. (A,B) Sketch-only comparisons to Collage teacher on InterHuman[40] (HH) and CORE4D[67] (3+ entity OOD). (C–F) Hard cases: heavy sketch noise (≈ 60%, Tab.2 (b,c)), self-intersecting paths, and OOD multi-object / sparse-constraints causing drift, floating, or collisions*

### 推理效率

虽然论文未提供精确的推理时间对比数值，但 Abstract 明确指出整流流学生 ODE 采样实现了“fast, stable sampling”，相比扩散模型的迭代去噪过程具有本质上的效率优势。这一优势来源于：整流流 ODE 的直连线路径比扩散模型的弯曲概率流路径需要更少的积分步数即可达到相当的样本质量。

### 评估公平性说明

所有方法采用相同的评估协议（Average protocol），遵循 的关键帧/轨迹二维和三维误差评估标准，并在相同 CORE4D 数据划分上进行训练和测试。消融实验中的各变体保持除目标组件外的所有配置一致，确保因果归因的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l1754_Sketch2Colab/figures/007_Figure_5.jpg]]
*Figure 5: Impact of CTMC and energy guidance. (a) CTMC shifts the F1–FMD Pareto frontier outward while reducing collision rates. (b) Contact timing calibration improves significantly (lower ECE). (c) Flow maintains low curvature except at discrete mode transitions. (d) Energy gradient aligns constructively with base flow near transitions, eliminating gradient conflicts*

![[assets/figures/papers/paper_list_l1754_Sketch2Colab/figures/004_Figure_3.jpg]]
*Figure 3: Sketch→interaction motion: comparison of Sketch2Colab and COLLAGE (teacher) [17]. Given storyboard keyframes and joint trajectories (top), Sketch2Colab (right) generates HOH motions that closely follow the sketches, execute interaction phases at the intended times, and adhere tightly to trajectories and keyframes. In contrast, COLLAGE (teacher, middle) struggles to respect storyboard constraints such as the handover and continued motion with a single human holding the object(1st and 2nd storyboards), and fails to match fine-grained keyframe constraints (e.g., the third storyboards, where the character must lift higher while moving). Additional examples and baseline comparisons are provided...*

## 方法谱系与知识库定位

### 问题定位与核心瓶颈

现有扩散模型在多实体交互场景中面临双重困境：**稀疏草图约束的精确满足**与**推理效率**难以兼得。具体而言，当用户仅提供少量关键帧、关节轨迹和物体掩码时，模型必须同时满足关键帧对齐、关节轨迹跟踪、接触一致性、碰撞避免等多类约束，而传统扩散模型（如DDPM/DDIM）通过分类器自由引导和条件注入的方式难以在这些约束之间取得精确平衡。此外，扩散模型的多步采样机制导致推理速度缓慢，进一步限制了交互式应用场景的实用性。

Sketch2Colab的核心洞察在于：**将扩散教师蒸馏为整流流学生，并利用可微能量函数的梯度直接塑造数据流形，可以在不依赖缓慢后验引导的前提下，实现对稀疏草图多约束的精确控制**。这一思路将约束满足从“采样后修正”转变为“生成过程中引导”，从根本上改变了多约束运动生成的范式。

### 与基线工作的关系

#### 相对于COLLAGE的继承与超越

Sketch2Colab直接继承并超越了**COLLAGE**（Daiya et al., ICRA 2025）的生成框架。COLLAGE作为扩散教师，提供了层次化VQ-VAE潜在空间中的多实体运动生成先验，但其本身在草图约束遵循方面存在明显不足：定性对比（Figure 3）显示，COLLAGE在交接时机、持续运动保持和细粒度关键帧对齐方面均出现显著偏差。

Sketch2Colab对COLLAGE的改进体现在三个关键维度：

1. **生成模型层面**：将扩散模型的迭代去噪替换为整流流ODE采样，在保持样本质量的同时大幅提升推理速度（FID从0.623降至0.480，降幅23%）。
2. **约束实现层面**：引入可微能量函数（关键帧、轨迹、接触、碰撞、物理）的梯度引导，替代纯条件注入，使锚点误差降低约45%，足部滑动降低约24%。
3. **离散事件调度层面**：增加CTMC驱动的接触/交接相位调度器，显式建模交互时序，这是COLLAGE完全缺失的能力。

#### 相对于SKETCH2ANIM-INT的扩展

**SKETCH2ANIM-INT**（Zhong et al., TOG 2025）是草图驱动单人生成方法向交互场景的扩展，但其设计并未针对多实体协同进行深度优化。在CORE4D基准的草图条件下，Sketch2Colab的FID（0.509）相比SKETCH2ANIM-INT（1.025）降低50.3%，表明后者在多实体约束满足方面存在系统性不足。这一差距的根源在于：SKETCH2ANIM-INT缺乏专门的多实体注意力机制、接触调度和物理约束能量项。

#### 相对于检索式方法的优势

基于检索的运动生成方法通过匹配数据库中的运动片段来响应草图输入，其根本局限在于无法生成训练数据中未出现的交互模式。Sketch2Colab的生成式框架天然具备组合泛化能力，能够合成训练分布之外的多人-多物协同运动。

### 方法谱系中的定位

从方法谱系角度看，Sketch2Colab处于**扩散蒸馏**、**能量引导生成**和**离散-连续混合建模**三条技术路线的交汇点：

- **扩散蒸馏线**：继承自渐进式蒸馏和整流流（Rectified Flow）的工作，但首次将其应用于多实体运动生成场景，并证明了蒸馏后的ODE采样在约束遵循方面可以超越教师模型。
- **能量引导线**：借鉴了分类器引导和基于能量的生成建模思想，但创新性地采用双空间引导机制（潜在锚点+原始空间能量）和学习的低秩Toeplitz Jacobian代理，解决了从运动空间到潜在空间的梯度反向传播效率问题。
- **离散-连续混合建模线**：CTMC相位调度器受非平衡输运采样器启发，将离散事件（触碰、抓取、交接）的时序规划与连续流生成耦合，这在运动生成领域属于首创。

### 适用边界与局限

#### 数据依赖性

Sketch2Colab的物体交互能力局限于CORE4D数据集的有限类别，训练过程中依赖预定义的物体锚点和类别标签。当前设计无法直接扩展到任意网格和物理属性的物体，这限制了其在开放场景中的应用。此外，整流流学生的训练依赖于冻结的扩散教师，增加了训练管线复杂度和先验依赖。

#### 交互复杂度边界

系统当前侧重人手与物体的单点交互建模，对于多人与物体间的协同操控（如多人同时抓取同一物体并施加不同方向的力）缺乏显式支持。CTMC调度的离散状态空间设计主要针对序列化交互（触碰→抓取→交接），对于并行交互模式的表达能力有限。

#### 极端条件下的鲁棒性

如图4所示，在重度草图噪声（约60%噪声水平）、自相交轨迹或分布外稀疏约束等极端情况下，系统仍可能出现漂移、浮空或碰撞失败。这表明能量引导的局部优化机制在全局约束冲突时可能陷入次优解。

### 开放问题

基于上述局限，以下开放问题值得后续研究关注：

1. **物体表征的泛化**：如何设计灵活的物体表征（任意网格+物理属性）以突破类别限制，使系统能够处理未见过的物体几何和材质属性？

2. **多人多物协同的组合式建模**：能否通过组合式场模型（compositional field models）实现多人多物协同，而无需专门的多人多物配对数据集？这需要在实体图注意力和能量函数层面支持动态数量的交互参与者。

3. **去扩散先验的训练策略**：是否可以开发不依赖扩散教师先验的训练策略，直接从数据中学习整流流，以降低计算成本并消除教师模型的能力上限约束？

4. **分布外约束的物理一致性**：在分布外（OOD）的稀疏约束下，如何保证接触一致性与物理合理性？这可能需要更强的物理先验，如刚体动力学约束或基于强化学习的物理模拟反馈。

5. **CTMC与能量引导的推理开销优化**：当前CTMC调度和能量梯度计算增加了推理时的计算负担。是否可以设计更高效的离散调度策略或能量代理模型，在保持约束精度的同时进一步降低推理延迟？

6. **交互模式的可控粒度**：当前系统对交互的刻画停留在接触/非接触的二元状态，未来是否可以引入更细粒度的交互语义（如推、拉、抬、转等操作类型），使用户能够通过草图或自然语言精确指定交互意图？

## 原文 PDF

![[paperPDFs/CVPR_2026/Sketch2Colab.pdf]]
