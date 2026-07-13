---
title: "ProjFlow: Projection Sampling with Flow Matching for Zero-Shot Exact Spatial Motion Control"
type: paper
paper_level: S
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ProjFlow_Projection_Sampling_with_Flow_Matching_for_Zero_Shot_Exact_Spatial_Motion_Control.pdf
project_link: https://akihisa-watanabe.github.io/projflow.github.io/
code_link: https://github.com/Akihisa-Watanabe/ProjFlow
aliases:
  - ProjFlow
tags:
- CVPR_2026
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 在每个流匹配采样步，使用运动学感知度量将预测的干净运动投影到线性约束集上；对于稀疏观测，引入时间衰减的伪观测机制。
primary_logic: 将多种空间运动控制任务统一为线性逆问题，通过在流匹配的ODE积分路径上施加闭合形式的投影校正，能在零样本、无内循环优化的条件下精确满足约束，同时保持运动先验的自然性；关键在于设计了编码骨骼拓扑的度量R，使校正沿运动链一致传播，避免关节孤立变动。
claims:
  - ProjFlow在骨盆控制任务上达到0.000的轨迹、位置和平均误差，是唯一实现精确约束的零样本方法。
  - 将运动学感知度量替换为欧几里得度量后，FID从0.097剧增至1.152，运动真实感严重下降。
  - ProjFlow在2D到3D重建任务中FID（平均值0.349，交叉0.168）显著优于训练类方法Sketch2Anim（0.525, 0.577），且2D重投影误差精确为0。
  - HumanML3D (pelvis trajectory control) 上 FID = 0.107
---

# ProjFlow: Projection Sampling with Flow Matching for Zero-Shot Exact Spatial Motion Control

> [!tip] 核心洞察
> 将多种空间运动控制任务统一为线性逆问题，通过在流匹配的ODE积分路径上施加闭合形式的投影校正，能在零样本、无内循环优化的条件下精确满足约束，同时保持运动先验的自然性；关键在于设计了编码骨骼拓扑的度量R，使校正沿运动链一致传播，避免关节孤立变动。

| 字段      | 内容                                                                                                                                                                                                                                                                                               |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 中文题名    | ProjFlow: 基于流匹配的投影采样实现零样本精确空间运动控制                                                                                                                                                                                                                                                                |
| 英文题名    | ProjFlow: Projection Sampling with Flow Matching for Zero-Shot Exact Spatial Motion Control                                                                                                                                                                                                      |
| 会议/期刊   | CVPR 2026                                                                                                                                                                                                                                                                                        |
| Links   | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Watanabe_ProjFlow_Projection_Sampling_with_Flow_Matching_for_Zero-Shot_Exact_Spatial_CVPR_2026_paper.html) · [Project](https://akihisa-watanabe.github.io/projflow.github.io/) · [Code](https://github.com/Akihisa-Watanabe/ProjFlow) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method  | ProjFlow                                                                                                                                                                                                                                                                                         |
| Dataset | HumanML3D                                                                                                                                                                                                                                                                                        |

> [!tip] 效果简介
> - HumanML3D (pelvis trajectory control) 上，FID 0.107 vs 0.151 (ACMDM-S-PS22 + DNO) (-0.044)。
> - HumanML3D (2D-to-3D reconstruction) 上，FID (Average) 0.349 vs 0.525 (Sketch2Anim) (-0.176)；FID (Cross) 0.168 vs 0.577 (Sketch2Anim) (-0.409)；MPJPE-2D (mm) 0.000 vs >0 (Sketch2Anim, approx.) (精确满足 vs 近似)。

## 概要

**瓶颈问题**：现有空间运动控制方法存在一个根本性矛盾——任务特定训练方法（如 OmniControl、MaskControl）虽然约束满足较好，但缺乏零样本泛化能力；推理时优化方法（如 DNO）虽无需训练，却依赖缓慢的内循环梯度优化，且只能实现软约束，无法精确满足硬性空间条件。两者均难以在保证运动自然性的同时，实现精确、高效、无需训练的约束满足。

**核心思路**：ProjFlow 将多样的空间运动控制任务统一建模为线性逆问题，在流匹配（Flow Matching）的 ODE 积分路径上，于每个采样步对预测的干净运动端点施加闭合形式的投影校正。该方法的核心创新在于设计了**运动学感知度量**（kinematics-aware metric），通过编码骨骼拓扑的图拉普拉斯矩阵，使约束修正沿运动链一致传播，避免关节孤立变动导致运动失真。

**方法定位**：ProjFlow 是一种零样本、无需训练的推理时采样器。它不修改预训练流匹配模型的权重，不执行内循环优化，而是在采样过程中以极小的额外计算代价将预测端点投影到约束集上，实现硬约束的精确满足。

**关键结果**：
- 在骨盆轨迹控制任务上，ProjFlow 达到 **0.000** 的轨迹误差、位置误差和平均误差，是唯一实现精确约束满足的零样本方法（Table 1）。
- 在 2D 到 3D 运动重建任务中，FID 显著优于训练类方法 **Sketch2Anim**（平均 FID 0.349 vs 0.525，交叉 FID 0.168 vs 0.577），且 2D 重投影误差精确为 0（Table 2）。
- 消融实验表明，将运动学感知度量替换为欧几里得度量后，FID 从 0.097 剧增至 **1.152**，验证了度量设计对运动真实感的决定性作用（Table 3）。



### 问题背景：空间运动控制的精确性与自然性困境

可控人体运动生成旨在根据给定的空间约束（如指定关节的轨迹、关键姿态、相对位置关系等）生成自然、逼真的运动序列。这一任务在动画制作、虚拟现实、人机交互等领域具有广泛的应用需求。然而，现有方法在**约束满足的精确性**与**运动自然性**之间长期存在难以调和的张力。

具体而言，空间运动控制面临的核心瓶颈是：**现有方法依赖任务特定训练或缓慢的推理优化，难以同时保证硬约束的精确满足和运动自然性，且常需内循环优化**。训练类方法（如基于ControlNet风格的空间控制器）需要针对每种约束类型重新训练或微调模型，不仅计算成本高昂，而且由于训练数据的覆盖限制，难以在零样本场景下泛化到未见过的约束组合。推理时优化方法（如基于扩散模型噪声优化的DNO）虽然避免了重新训练，但通常需要耗时的内循环迭代，且仅能实现软约束的近似满足，无法保证硬约束的精确性。

### 现有方法缺口

当前空间运动控制方法可大致分为三类，各自存在明显局限：

**训练类空间控制器**以**OmniControl**（Xie et al., ICLR 2024）和**MaskControl**（Pinyoanuntapong et al., arXiv 2024）为代表。这类方法将控制信号作为额外条件注入生成模型，通过特定任务的数据训练来学习条件映射。其根本缺陷在于：每当约束类型或受控关节发生变化，就需要重新训练，缺乏零样本迁移能力；同时，由于模型学习的是条件分布而非硬约束满足，生成的运动在约束精度上存在固有偏差。

**推理时优化方法**以**DNO**（Karunratanakul et al., CVPR 2024）为代表，通过对扩散模型的初始噪声进行梯度优化来引导生成结果逼近约束。这类方法避免了重新训练，但每次推理都需要多步迭代优化，推理速度慢；且基于梯度的引导本质上是一种软约束，无法保证精确满足，尤其在骨盆轨迹控制等需要硬约束的任务上表现不佳。

**2D到3D提升方法**以**Sketch2Anim**（Zhong et al., TOG 2025）为代表，从2D关键帧和轨迹输入重建3D运动。这类方法同样依赖任务特定训练，且2D重投影误差通常无法精确归零，导致生成的运动在视觉上偏离用户输入。

### 核心动机：统一为线性逆问题的零样本范式

ProjFlow的核心动机源于一个关键洞察：**将多种空间运动控制任务统一为线性逆问题，通过在流匹配的ODE积分路径上施加闭合形式的投影校正，能在零样本、无内循环优化的条件下精确满足约束，同时保持运动先验的自然性**。

具体而言，ProjFlow将空间约束（轨迹跟随、关键帧匹配、相对位置保持、运动修复等）统一表述为线性高斯观测模型 $\mathbf{y} = A \mathbf{x} + \boldsymbol{\epsilon}$，其中硬约束对应观测噪声协方差 $\Sigma \to 0$。在此基础上，ProjFlow在每个流匹配采样步对预测的干净运动端点施加**最小修正投影**——在精心设计的运动学感知度量下，寻找满足约束的最小修正量。这一投影具有闭合形式解，无需迭代优化，实现了高效的硬约束精确满足。

关键的创新在于**运动学感知度量**的设计：传统方法在欧几里得空间中进行投影，导致关节修正孤立传播，破坏运动链的自然协调性。ProjFlow引入编码骨骼拓扑的度量矩阵 $R = w_{\mathrm{kin}} (I_3 \otimes I_N \otimes L_{\mathrm{kin}}) + \lambda I_d$，其中 $L_{\mathrm{kin}}$ 为骨骼图拉普拉斯矩阵，惩罚相邻关节的差异。这使得修正沿运动链一致传播，避免关节孤立变动，从而在精确满足约束的同时保持运动的自然真实感。

对于稀疏观测场景（如运动修复），ProjFlow进一步引入**时间衰减的伪观测机制**：通过动态掩码控制邻域范围、自适应方差根据时间和局部曲率调整伪观测的可信度，在稀疏关键帧之间生成平滑过渡，弥补了简单硬约束在稀疏输入下的不足。

这一统一框架使得ProjFlow能够以零样本、无需训练的方式处理多种空间运动控制任务，从根本上摆脱了对任务特定训练和内循环优化的依赖。



## 核心方法与创新机理

ProjFlow 的核心创新在于将零样本空间运动控制重新定义为**线性逆问题**，并在流匹配（Flow Matching）的 ODE 积分路径上引入**闭合形式的投影校正**，从而在无需任务特定训练和内循环优化的前提下，实现对线性空间约束的**精确满足**。与现有方法相比，这一范式转换体现在三个关键维度的设计变革上。

### 从软约束到硬约束精确满足的约束注入方式

现有零样本空间控制方法普遍采用基于梯度的引导或噪声优化策略（如 **DNO**，Karunratanakul et al., CVPR 2024），这些方法将约束作为软性引力项施加于采样过程，本质上只能逼近约束而无法精确满足。训练类方法（如 **OmniControl**，Xie et al., ICLR 2024；**MaskControl**，Pinyoanuntapong et al., arXiv 2024）虽然通过任务特定训练提升了约束跟随能力，但仍存在残余误差，且丧失了零样本泛化性。

ProjFlow 改变了这一范式：在每个采样步，先利用 Tweedie 公式从当前状态 $\mathbf{x}_t$ 和预训练速度场 $v_\theta$ 预测干净运动端点：

$$\hat{\mathbf{x}}_1 = \mathbf{x}_t + (1 - t) v_\theta(\mathbf{x}_t, t)$$

随后，将该预测端点**投影**到由线性高斯观测模型 $\mathbf{y} = A \mathbf{x} + \boldsymbol{\epsilon}$ 定义的约束集上，通过求解最小修正问题：

$$\min_{\Delta \mathbf{x}_1} \frac{1}{2} \|\Delta \mathbf{x}_1\|_R^2 + \frac{1}{2} \|\mathbf{y} - A(\hat{\mathbf{x}}_1 + \Delta \mathbf{x}_1)\|_{\Sigma^{-1}}^2$$

获得闭合形式修正解：

$$\Delta \mathbf{x}_1^\star = R^{-1} A^{\top} \left( A R^{-1} A^{\top} + \Sigma \right)^{-1} (\mathbf{y} - A \hat{\mathbf{x}}_1)$$

当观测协方差 $\Sigma \to 0$ 时，该方法退化为硬约束的精确投影。实验证实了这一设计的有效性：在骨盆轨迹控制任务上，ProjFlow 是**唯一**实现轨迹误差、位置误差和平均误差均为 0.000 的零样本方法（Table 1），而基于梯度引导或噪声优化的基线方法始终存在不可消除的残余误差。

### 运动学感知度量：编码骨骼拓扑的约束传播机制

将约束注入从软约束改为硬投影后，一个关键挑战浮现：在标准欧几里得度量（即 $R = I$）下进行投影，修正量会孤立地施加于受约束关节，导致运动链上相邻关节之间出现不自然的断裂。ProjFlow 通过设计**运动学感知度量** $R$ 解决了这一问题：

$$R = w_{\mathrm{kin}} (I_3 \otimes I_N \otimes L_{\mathrm{kin}}) + \lambda I_d$$

其中 $L_{\mathrm{kin}}$ 是编码骨骼邻接关系的图拉普拉斯矩阵，惩罚相邻关节之间的修正差异；$\lambda I_d$ 保证度量矩阵的正定性。在这一度量下，投影修正沿运动学树**一致传播**——当某个关节因约束被调整时，其相邻关节也会按骨骼拓扑关系获得协调修正，从而保持运动链的自然性。

消融实验（Table 3）为这一设计提供了决定性证据：将运动学感知度量替换为标准欧几里得度量后，FID 从 0.097 剧增至 1.152，运动真实感严重退化。这表明，**度量空间的选择**是硬约束投影能否保持运动自然性的核心因果杠杆。

### 稀疏输入的伪观测机制：动态掩码与自适应方差

对于运动修复（motion inpainting）等仅给定稀疏关键帧的任务，简单的硬约束掩码（plain masking）会导致未观测帧缺乏有效引导，生成质量显著下降（FID 恶化至 0.880，Table 3）。ProjFlow 引入了**时间衰减的伪观测**机制，将稀疏硬约束扩展为稠密的软引导。

该机制包含两个协同组件：
- **动态掩码**：以时间调度半径 $\ell(t) = (1 - t) \ell_{\mathrm{max}} + t \ell_{\mathrm{min}}$ 激活已知帧周围的邻域，在采样早期提供大范围软引导，随 $t \to 1$ 逐步收缩，将控制权交还给运动先验。
- **自适应方差**：通过信任度评分 $\tilde{\pi}_n^{(t)}$ 调节伪观测的可信度，该评分融合了全局时间衰减 $\tau(t) = \tau_{\mathrm{min}} + (1 - \tau_{\mathrm{min}})(1 - t)$ 和局部曲率惩罚——在运动剧烈变化区域自动降低伪观测权重，避免平滑掉细节。

这一设计使 ProjFlow 在 2D 到 3D 运动提升任务中展现出显著优势：FID（平均值 0.349，交叉 0.168）大幅优于训练类方法 **Sketch2Anim**（Zhong et al., TOG 2025）的 0.525 和 0.577，且 2D 重投影误差精确为 0.000 mm（Table 2），在约束精度和运动自然性两个维度上同时实现了超越。

### 随机重构：保持生成多样性的必要组件

投影修正确保了约束满足，但若采用确定性重构（$\eta_t = 0$），采样过程会退化为缺乏多样性的模式坍塌——消融实验中 FID 恶化至 3.429（Table 3）。ProjFlow 通过**随机重构**步骤，在修正后的干净端点和原始噪声之间重新混合随机扰动，维持了流匹配采样的随机性，确保生成结果在满足约束的同时保持丰富的多样性。



ProjFlow 是一个无需训练的采样器，在预训练流匹配运动先验的基础上，通过在每个采样步执行**投影校正**，实现对线性空间约束的零样本精确满足。其核心思路是将多样化的空间运动控制任务统一建模为线性逆问题，并在流匹配的 ODE 积分路径上施加闭合形式的投影，从而在保持运动自然感的同时，消除约束违反。

### 统一逆问题建模

给定一个运动序列 $\mathbf{x} \in \mathbb{R}^d$（包含所有关节在所有帧的三维坐标），空间控制约束被统一表示为线性高斯观测模型：

$$\mathbf{y} = A \mathbf{x} + \boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \Sigma)$$

其中 $A$ 是线性观测矩阵，$\Sigma$ 是观测噪声协方差。**硬约束**对应 $\Sigma \to 0$（精确满足），**软约束**对应非零 $\Sigma$（允许一定偏差）。这一建模覆盖了多种任务：指定关节轨迹、固定关节间相对位置、2D 关键帧提升到 3D、运动修复（inpainting）等。

### 投影采样三步循环

在每个采样时间步 $t$，ProjFlow 执行三个有序模块（Figure 2）：

**（1）干净端点预测**  
利用流匹配网络 $v_\theta$ 预测当前状态 $\mathbf{x}_t$ 对应的干净运动端点 $\hat{\mathbf{x}}_1$：

$$\hat{\mathbf{x}}_1 = \mathbf{x}_t + (1 - t) v_\theta(\mathbf{x}_t, t)$$

这本质上是 Tweedie 公式在整流流（rectified flow）路径 $\mathbf{x}_t = (1-t)\mathbf{x}_0 + t\mathbf{x}_1$ 下的具体形式。

**（2）投影校正**  
在**运动学感知度量** $R$ 下，寻找最小修正量 $\Delta \mathbf{x}_1$，使修正后的端点满足观测模型：

$$\min_{\Delta \mathbf{x}_1} \frac{1}{2} \|\Delta \mathbf{x}_1\|_R^2 + \frac{1}{2} \|\mathbf{y} - A(\hat{\mathbf{x}}_1 + \Delta \mathbf{x}_1)\|_{\Sigma^{-1}}^2$$

该凸二次问题具有闭合形式解：

$$\Delta \mathbf{x}_1^\star = R^{-1} A^{\top} \left( A R^{-1} A^{\top} + \Sigma \right)^{-1} (\mathbf{y} - A \hat{\mathbf{x}}_1)$$

得到修正后的干净端点 $\hat{\mathbf{x}}_1^\star = \hat{\mathbf{x}}_1 + \Delta \mathbf{x}_1^\star$。

**（3）随机重构**  
将修正后的端点与原始噪声混合，重构下一时刻状态 $\mathbf{x}_{t+\Delta t}$。该步骤引入受控随机扰动，保证生成样本的多样性和运动质量——消融实验表明，若移除随机重构（$\eta_t = 0$）改用确定性重构，FID 从 0.097 恶化至 3.429。

### 运动学感知度量：约束传播的关键设计

度量矩阵 $R$ 的设计是 ProjFlow 区别于通用图像投影方法的核心创新：

$$R = w_{\mathrm{kin}} (I_3 \otimes I_N \otimes L_{\mathrm{kin}}) + \lambda I_d$$

其中 $L_{\mathrm{kin}}$ 是编码骨骼邻接关系的**图拉普拉斯矩阵**，惩罚相邻关节间的修正差异。这使得当某一关节被约束拉动时，修正量会沿运动链一致传播，避免关节孤立变动导致的不自然姿态。恒等项 $\lambda I_d$ 保证 $R$ 的正定性。消融实验证实，将 $R$ 替换为欧几里得度量（$R=I$）后，FID 从 0.097 剧增至 1.152，运动真实感严重下降。

### 运动修复的伪观测扩展

对于运动修复任务（仅有稀疏关键帧观测），直接施加硬约束会导致未观测帧缺乏引导。ProjFlow 引入**伪观测模块**（Figure 3），通过两个机制生成随时间演化的软约束：

- **动态掩码**：以观测帧为中心，激活时间邻域 $\ell(t) = (1-t)\ell_{\mathrm{max}} + t\ell_{\mathrm{min}}$，随采样进程线性收缩邻域范围，逐步减少软引导。
- **自适应方差**：结合全局时间衰减 $\tau(t)$ 和局部曲率惩罚 $s_n$，计算信任度评分 $\tilde{\pi}_n^{(t)}$，信任度越高则伪观测方差越小、吸引力越强。原始观测帧始终作为硬约束（$\Sigma \to 0$），插值生成的中间帧作为软约束。

消融实验表明，移除伪观测改用简单掩码后，FID 恶化至 0.880，验证了该模块对运动修复质量的关键作用。

### 输入输出流总结

**输入**：噪声样本 $\mathbf{x}_0 \sim \mathcal{N}(0, I)$、线性约束 $(\mathbf{y}, A, \Sigma)$、文本条件（可选）。**输出**：满足约束的干净运动序列 $\mathbf{x}_1$。整个过程无需训练、无需内循环优化，仅通过 ODE 积分路径上的投影校正即实现零样本精确控制。

### 补充图表

![[assets/figures/papers/paper_list_l970_https_openaccess_thecvf_com_content_CVPR2026_html_Watanabe_ProjFlow_Proj/figures/001_Figure_1.jpg]]
*Figure 1: ProjFlow provides a unified, zero-shot framework for exact spatial motion control. The method handles diverse applications by formulating them as linear inverse problems. Examples of applications include (a) precisely following a specified joint’s trajectory, (b) lifting 2D keypose and 2D trajectory inputs to a full 3D motion, (c) maintaining a fixed relative position between joints, and (d) generating seamlessly looped motion by matching start and end poses*



ProjFlow 的推理管线由三个核心模块串联构成，每个采样步 $t$ 依次执行：**干净端点预测**、**投影校正**、**随机重构**。对于运动修复任务，额外引入**伪观测生成模块**以处理稀疏关键帧。以下逐一展开各模块的公式与变量含义。

### 4.1 干净端点预测

给定当前状态 $\mathbf{x}_t$（整流流路径上的中间点），利用预训练的速度网络 $v_\theta$ 预测对应的干净运动端点。该步骤基于 Tweedie 公式在流匹配框架下的形式：

$$\hat{\mathbf{x}}_1 = \mathbf{x}_t + (1 - t) \, v_\theta(\mathbf{x}_t, t) \tag{5}$$

其中 $t \in [0,1]$ 为采样时间步，$\mathbf{x}_t = (1-t)\mathbf{x}_0 + t\mathbf{x}_1$ 遵循噪声到数据的直线插值路径。$\hat{\mathbf{x}}_1$ 是未经约束修正的初始干净端点估计。

### 4.2 投影校正

该模块是 ProjFlow 实现硬约束精确满足的核心机制。所有空间控制任务被统一为线性高斯观测模型：

$$\mathbf{y} = A \mathbf{x} + \boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \Sigma) \tag{4}$$

其中 $A$ 为线性观测矩阵，$\Sigma$ 为观测噪声协方差。硬约束对应 $\Sigma \to \mathbf{0}$ 的极限情形。

投影校正的目标是在运动学感知度量 $R$ 下，寻找对 $\hat{\mathbf{x}}_1$ 的最小修正量 $\Delta\mathbf{x}_1$，使修正后的端点满足观测约束。优化问题形式为：

$$\min_{\Delta\mathbf{x}_1} \; \frac{1}{2} \|\Delta\mathbf{x}_1\|_R^2 + \frac{1}{2} \|\mathbf{y} - A(\hat{\mathbf{x}}_1 + \Delta\mathbf{x}_1)\|_{\Sigma^{-1}}^2 \tag{6}$$

该凸二次问题存在闭合形式解：

$$\Delta\mathbf{x}_1^\star = R^{-1} A^{\top} \left( A R^{-1} A^{\top} + \Sigma \right)^{-1} (\mathbf{y} - A \hat{\mathbf{x}}_1) \tag{7}$$

修正后的干净端点为 $\hat{\mathbf{x}}_1^\star = \hat{\mathbf{x}}_1 + \Delta\mathbf{x}_1^\star$。

**运动学感知度量** $R$ 是区别于图像域投影方法的关键设计。其定义为：

$$R = w_{\mathrm{kin}} \, (I_3 \otimes I_N \otimes L_{\mathrm{kin}}) + \lambda I_d \tag{11}$$

其中 $L_{\mathrm{kin}}$ 为骨骼邻接关系的图拉普拉斯矩阵，惩罚相邻关节间的差异；$I_3$ 对应空间三维，$I_N$ 对应时间帧数；$\lambda I_d$ 保证度量正定性。该度量使投影修正沿运动链一致传播，避免孤立关节的突变式调整。消融实验表明，将其替换为欧几里得度量（$R=I$）后，FID 从 0.097 剧增至 1.152（Table 3），验证了运动学感知度量对保持运动自然感的决定性作用。

### 4.3 随机重构

在获得修正端点 $\hat{\mathbf{x}}_1^\star$ 后，通过随机重构步骤生成下一时刻状态 $\mathbf{x}_{t+\Delta t}$。该步骤混合原始噪声与随机扰动，避免确定性重构导致的模式坍塌——消融中移除该步骤（$\eta_t = 0$）使 FID 恶化至 3.429（Table 3）。

### 4.4 伪观测生成（运动修复专用）

对于运动修复任务，稀疏观测仅提供少量关键帧的硬约束。ProjFlow 引入**伪观测机制**，通过两个子模块为中间帧生成时间衰减的软引导：

**动态掩码**：控制伪观测的时间邻域半径，随采样进程线性收缩：
$$\ell(t) = (1 - t) \, \ell_{\mathrm{max}} + t \, \ell_{\mathrm{min}}$$

早期（$t$ 小）邻域较大以提供密集引导，后期（$t \to 1$）邻域收缩，让运动先验主导细节。

**自适应方差**：通过信任度评分 $\tilde{\pi}_n^{(t)}$ 调节伪观测的可信度：
$$\tilde{\pi}_n^{(t)} = \tau(t) \, \frac{c_0}{1 + \lambda_s \, (s_n(\hat{\mathbf{x}}_1) / s_{\mathrm{med}})^p}$$

其中 $\tau(t) = \tau_{\mathrm{min}} + (1 - \tau_{\mathrm{min}})(1 - t)$ 为全局时间衰减项，$s_n$ 为局部曲率惩罚——曲率越大的区域，伪观测信任度越低。方差由信任度导出：$\sigma_i^2(t) = r_i (1 - \pi_i) / \pi_i$。原始观测帧始终保持硬约束（方差趋零），而插值生成的伪观测以自适应方差作为软约束。消融实验中，用简单掩码替代该机制导致 FID 恶化至 0.880（Table 3）。

### 模块间数据流

每个采样步 $t$ 的完整流程（对应 Figure 2）：(1) 从 $\mathbf{x}_t$ 经速度网络预测 $\hat{\mathbf{x}}_1$；(2) 在度量 $R$ 下求解 $\Delta\mathbf{x}_1^\star$，将 $\hat{\mathbf{x}}_1$ 投影到约束集得到 $\hat{\mathbf{x}}_1^\star$；(3) 随机重构生成 $\mathbf{x}_{t+\Delta t}$。该流程无需内循环优化，在 ODE 积分路径上以闭合形式逐步施加约束校正，实现零样本的硬约束精确满足。

![[assets/figures/papers/paper_list_l970_https_openaccess_thecvf_com_content_CVPR2026_html_Watanabe_ProjFlow_Proj/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the Projection Sampling Step. At each timestep t: (1) predict the clean endpoint*

### 补充图表

![[assets/figures/papers/paper_list_l970_https_openaccess_thecvf_com_content_CVPR2026_html_Watanabe_ProjFlow_Proj/figures/003_Figure_3.jpg]]
*Figure 3: Pseudo-observations for motion inpainting. Sparse observations are interpolated to guide intermediate frames. This guidance is controlled by two mechanisms: Dynamic Masking activates a time-scheduled neighborhood, and Adaptive Variance treats original observations as hard constraints and the interpolated guides as soft constraints*



## 实验与关键发现

### 5.1 实验设置

ProjFlow 在 **HumanML3D** 数据集上进行评估，该数据集包含 14,646 个运动序列，覆盖广泛的日常人类动作。实验围绕三类核心任务展开：**骨盆轨迹控制**、**所有关节空间控制**、以及 **2D 到 3D 运动重建**。对于空间控制任务，评估覆盖五种关键帧密度（1、2、5、49、196），以系统考察方法在不同稀疏程度下的表现。

评估指标包括：
- **运动真实感**：FID（Fréchet Inception Distance）
- **约束满足精度**：轨迹误差（Traj. err.）、位置误差（Loc. err.）、平均误差（Avg. err.）
- **2D 重投影精度**：MPJPE-2D（mm）
- **文本-运动匹配度**：R-Precision、MM-Dist

对比基线涵盖三类方法：(1) **训练类空间控制器**：**OmniControl**（Xie et al., ICLR 2024）、**MaskControl/ControlMM**（Pinyoanuntapong et al., arXiv 2024）；(2) **推理时优化方法**：**DNO**（Karunratanakul et al., CVPR 2024）；(3) **训练类 2D 到 3D 提升方法**：**Sketch2Anim**（Zhong et al., TOG 2025）。ProjFlow 自身是**零样本、无需训练**的采样器，其性能依赖于预训练流匹配先验的质量，避免了因任务特定训练数据引入的偏差。

### 5.2 主要结果

#### 5.2.1 骨盆轨迹控制

Table 1 展示了骨盆轨迹控制的定量结果。ProjFlow 在所有零样本方法中取得**最佳的约束满足精度和运动真实感**：

![[assets/figures/papers/paper_list_l970_https_openaccess_thecvf_com_content_CVPR2026_html_Watanabe_ProjFlow_Proj/figures/005_Table_1.jpg]]
*Table 1: Quantitative text-conditioned motion generation with spatial control signals and upper-body editing on HumanML3D[16]. In the first section, methods are trained and evaluated solely on pelvis controls. In the middle section, methods are trained on all joints and evaluated separately on each controlled joint. Only average results are reported for brevity. We include details in the supplementary material. The last section presents upper-body editing results. bold face / underline indicates the best/2nd results*

- **约束满足**：ProjFlow 是**唯一实现精确约束满足的零样本方法**，轨迹误差、位置误差和平均误差均为 **0.0000**。相比之下，基于梯度引导或噪声优化的方法（如 DNO）仍存在微小残差违反。
- **运动真实感**：ProjFlow 的 FID 为 **0.107**，优于 DNO（ACMDM-S-PS22 + DNO）的 0.151（降低 0.044），且与训练类方法 OmniControl（0.097）和 MaskControl（0.114）处于同一水平。

这一结果的核心机制在于：ProjFlow 在每个采样步对预测的干净运动端点执行**硬投影**，直接将其映射到约束集上，而非依赖软性梯度引导。这使得约束满足成为数学上的必然，而非优化目标。

#### 5.2.2 所有关节空间控制

当控制信号扩展到所有关节时（Table 1 中部），ProjFlow 依然保持了精确的约束满足（各关节误差均为 0.0000），而训练类方法 OmniControl 和 MaskControl 虽然整体 FID 略优，但无法达到零误差。值得注意的是，训练类方法在训练时见过所有关节的控制信号，而 ProjFlow 在零样本条件下仍能实现硬约束精确满足，体现了投影机制的通用性。

#### 5.2.3 2D 到 3D 运动重建

Table 2 展示了 2D 关键帧/轨迹到 3D 运动的提升结果。ProjFlow 在运动真实感上**显著优于**训练类方法 Sketch2Anim：

![[assets/figures/papers/paper_list_l970_https_openaccess_thecvf_com_content_CVPR2026_html_Watanabe_ProjFlow_Proj/figures/007_Table_2.jpg]]
*Table 2: Quantitative analysis of ProjFlow and three baseline models proposed in Sketch2Anim [67] on the HumanML3D [16]. Evaluation metrics on motion realism, control accuracy, and text-motion match are presented. Following OmniControl [61], we report both the average error of all joints (Average) and their random combination (Cross). bold face / underline indicates the best/2nd results*

- **FID（Average）**：ProjFlow **0.349** vs Sketch2Anim 0.525（降低 0.176）
- **FID（Cross）**：ProjFlow **0.168** vs Sketch2Anim 0.577（降低 0.409）
- **MPJPE-2D**：ProjFlow 精确为 **0.000**，而 Sketch2Anim 仅能近似满足

定性结果（Figure 5）进一步印证了这一优势：给定“一个人边走边用手画心形”的文本提示和左手腕的 2D 心形轨迹，Sketch2Anim 无法精确复现心形路径（形状坍塌），且丢失了行走动作；ProjFlow 则精确跟随心形手腕轨迹，同时全程保持自然的行走姿态。

![[assets/figures/papers/paper_list_l970_https_openaccess_thecvf_com_content_CVPR2026_html_Watanabe_ProjFlow_Proj/figures/006_Figure_5.jpg]]
*Figure 5: 2D-to-3D hand-trajectory lifting with text conditioning. The input condition includes the text prompt “a person draws a heart with their hand while walking,” an initial 2D keypose, and a left-wrist 2D trajectory shaped like a heart. Sketch2Anim [67] fails to reproduce the heart path precisely, the shape collapses, and the subject does not exhibit walking motion. In contrast, ProjFlow follows the heart-shaped wrist trajectory accurately while maintaining a natural walking motion throughout the sequence*

这一优势源于 ProjFlow 将 2D 到 3D 重建也统一建模为线性逆问题——2D 观测通过相机投影矩阵 $A$ 与 3D 运动关联，投影校正直接作用于 3D 干净端点，确保 2D 重投影误差严格为零。

### 5.3 消融实验

Table 3 系统消融了 ProjFlow 的三个核心组件，揭示了每个组件对性能的因果贡献：

![[assets/figures/papers/paper_list_l970_https_openaccess_thecvf_com_content_CVPR2026_html_Watanabe_ProjFlow_Proj/figures/008_Table_3.jpg]]
*Table 3: Ablation studies of ProjFlow*

#### 5.3.1 运动学感知度量的关键作用

将运动学感知度量 $R = w_{\mathrm{kin}} (I_3 \otimes I_N \otimes L_{\mathrm{kin}}) + \lambda I_d$ 替换为标准欧几里得度量（$R=I$）后，**FID 从 0.097 急剧恶化至 1.152**，运动真实感严重下降。

这一现象揭示了 ProjFlow 设计的核心洞察：骨骼图拉普拉斯 $L_{\mathrm{kin}}$ 编码了关节间的拓扑邻接关系，使得投影修正能够**沿运动链一致传播**。当仅修正单个关节时，度量 $R$ 会惩罚相邻关节间的差异，从而将修正力分布到整个运动链上，避免关节孤立变动导致的运动不自然。欧几里得度量缺乏这种结构感知能力，导致修正后的运动出现关节错位和不协调。

#### 5.3.2 随机重构的必要性

移除随机重构步骤（设置 $\eta_t=0$，使用确定性重构）导致 **FID 恶化至 3.429**，质量和多样性均严重受损。

随机重构步骤在修正后的干净端点和原始噪声之间重新混合随机扰动，其作用是为下一采样步保留适当的探索空间。确定性重构会使采样路径过度收缩到约束流形上，剥夺了流匹配先验在无约束维度上的生成多样性。这验证了投影采样框架中“先投影、再随机化”两步设计的必要性。

#### 5.3.3 伪观测机制的有效性

在运动修复任务中，将伪观测模块替换为简单掩码（plain masking，仅对已知帧施加硬约束）导致 **FID 恶化至 0.880**。

伪观测模块的两个子机制——动态掩码（时间邻域随 $t$ 收缩）和自适应方差（基于信任度评分调整软约束强度）——协同作用，在稀疏观测间隙提供逐步减弱的软引导。简单掩码完全缺失这种中间帧引导，导致生成的运动在观测帧之间出现不连贯或坍塌。

### 5.4 失败模式与局限性分析

尽管 ProjFlow 在精确约束满足上表现优异，但仍存在以下局限性：

1. **非线性约束不支持**：当前投影框架仅适用于线性约束（$y = A x + \varepsilon$），无法处理非线性不等式约束（如“关节保持在平面以上”）。闭合形式的投影解依赖于线性观测模型的凸二次结构，扩展到非线性约束需要迭代优化，可能牺牲计算效率。

2. **极稀疏关键帧退化**：当关键帧密度极低（如仅 1-2 帧）时，尽管伪观测机制有缓解作用，生成质量仍可能下降。这是因为流匹配先验在缺乏足够观测引导时，难以准确推断长时序的运动结构。

3. **预训练先验依赖**：ProjFlow 的性能上限受限于预训练流匹配运动先验的质量。在缺乏此类模型的领域（如非人体运动、物理模拟），方法无法直接迁移。

4. **计算开销未充分讨论**：投影步骤涉及矩阵求逆 $R^{-1} A^{\top} (A R^{-1} A^{\top} + \Sigma)^{-1}$，其对高维运动序列的计算开销在论文中未详细量化。对于长时间序列或高自由度骨骼，该操作可能成为推理瓶颈。

5. **超参数敏感性**：伪观测模块包含多个超参数（$\ell_{\mathrm{max}}$、$\tau_{\mathrm{min}}$、$\lambda_s$ 等），需要针对不同任务调整以获得最佳效果，其任务无关的鲁棒默认值尚未确定。

### 补充图表

![[assets/figures/papers/paper_list_l970_https_openaccess_thecvf_com_content_CVPR2026_html_Watanabe_ProjFlow_Proj/figures/004_Figure_4.jpg]]
*Figure 4: Text-conditioned pelvis-trajectory control. Given the prompt “a person runs forward in an S-shaped path” and a pelvis control signal, we compare OmniControl [61], MaskControl [45], and ProjFlow (ours). The rendered motions and the trajectory plots both visualize the generated pelvis trajectory (orange) overlaid on the target control signal (gray dotted line)*



## 定位与知识库关联

### 1. 在空间运动控制谱系中的位置

ProjFlow 位于**零样本推理时控制**与**训练类空间控制器**的交汇地带，但其核心机制与两类方法均有本质差异。

**训练类空间控制器**将控制信号作为附加条件注入生成模型，需要针对特定任务重新训练或微调。代表性工作包括：

- **OmniControl** (Xie et al., ICLR 2024)：采用 ControlNet 风格的架构，在扩散模型的特征层嵌入空间控制信号，支持骨盆轨迹控制与全关节控制。其优势在于生成质量稳定，但约束满足是“软性”的——模型学会在条件信号附近生成运动，而非精确匹配。
- **MaskControl / ControlMM** (Pinyoanuntapong et al., arXiv 2024)：通过掩码运动生成实现空间控制，训练时将部分关节位置作为已知条件。同样面临软约束的固有限制。

**推理时优化方法**试图在不重新训练的前提下施加控制，典型代表为 **DNO** (Karunratanakul et al., CVPR 2024)：通过对扩散噪声进行梯度优化，使生成的运动逐步逼近目标约束。然而，DNO 依赖内循环迭代优化，计算开销大，且本质上仍是软约束——Table 1 显示其在骨盆控制任务上仍存在残余误差，无法达到精确的 0.0000。

ProjFlow 的定位突破在于：**将空间控制统一为线性逆问题，在流匹配的 ODE 积分路径上施加闭合形式的投影校正**。这使得它同时具备零样本（无需训练）和硬约束精确满足（误差 = 0.0000）两个特性，而此前的方法只能二选一。

### 2. 与 2D 到 3D 运动提升方法的对比

在 2D 关键帧/轨迹到 3D 运动重建任务上，ProjFlow 直接对标 **Sketch2Anim** (Zhong et al., TOG 2025)。Sketch2Anim 是训练类方法，需要学习从 2D 输入到 3D 运动的映射。ProjFlow 则将该任务视为线性逆问题（2D 投影作为观测约束），利用预训练运动先验进行零样本重建。

Table 2 的结果揭示了本质差异：ProjFlow 的 2D 重投影误差（MPJPE-2D）精确为 0.000 mm，而 Sketch2Anim 无法完全消除投影误差。更重要的是，在运动真实感指标上，ProjFlow 的 FID（Average 0.349, Cross 0.168）显著优于 Sketch2Anim（0.525, 0.577）。这表明**硬约束投影不仅没有损害运动质量，反而通过精确匹配观测，避免了训练类方法中常见的“近似偏差”对运动自然性的侵蚀**。

### 3. 方法适用边界

ProjFlow 的适用性受以下条件约束：

- **约束类型限制**：当前框架仅支持线性等式约束（包括可退化为硬约束的线性高斯观测）。对于非线性不等式约束（例如“关节保持在平面以上”、“避免自穿透”），投影步骤无法直接给出闭合形式解。这是方法的核心数学边界。
- **先验依赖**：ProjFlow 是采样器而非生成模型本身，其性能上限由预训练的流匹配运动先验决定。在缺乏高质量运动先验的领域（如非人体运动、非常规动作类型），方法无法直接迁移。
- **稀疏输入的退化**：尽管伪观测模块（动态掩码 + 自适应方差）显著缓解了稀疏关键帧问题，但当仅有一两个已知帧时，生成质量仍可能下降。Table 3 的消融实验显示，移除伪观测机制后 FID 从 0.097 恶化至 0.880，但未报告极端稀疏场景下的性能下限。

### 4. 局限与开放问题

**已确认的局限：**

1. **非线性约束无法处理**：论文明确将线性约束作为方法的前提条件。对于不等式约束、接触约束等非线性场景，闭合形式的投影不再适用。
2. **计算开销未充分讨论**：投影步骤涉及矩阵求逆 $R^{-1}$ 和 $(A R^{-1} A^\top + \Sigma)^{-1}$。对于高维运动序列（例如长时间序列、多关节全身运动），这些操作的计算复杂度未在论文中量化分析。
3. **超参数敏感性**：伪观测模块包含多个超参数（$\ell_{\text{max}}$、$\tau_{\text{min}}$、$\lambda_s$ 等），需要针对不同任务调整。论文未证明这些参数具有任务无关的鲁棒默认值。

**开放问题：**

1. **非线性扩展**：能否将投影采样框架与障碍函数法或序列二次规划结合，以处理不等式约束？这需要突破闭合形式解的限制。
2. **跨域泛化**：ProjFlow 能否与更强大的运动基模型（如基于 Transformer 的生成模型）结合？能否扩展到物理模拟、人-物交互等需要接触约束的场景？
3. **超参数自动化**：伪观测模块中的信任度评分和动态掩码参数是否可以自适应学习，而非手工设计？
4. **结构化生成任务的推广**：该方法的核心思想——在生成过程的中间表示上施加结构化约束投影——能否推广到其他结构化生成任务，如人体姿态估计、分子构象生成？这需要验证度量设计（类比运动学感知度量 $R$）在目标领域的有效性。



## 原文 PDF

![[paperPDFs/CVPR_2026/ProjFlow_Projection_Sampling_with_Flow_Matching_for_Zero_Shot_Exact_Spatial_Motion_Control.pdf]]
