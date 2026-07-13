---
title: "InterPhys: Physics-aware Human Motion Synthesis in a Dynamic Scene"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/InterPhys_Physics_aware_Human_Motion_Synthesis_in_a_Dynamic_Scene.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Xing_InterPhys_Physics-aware_Human_Motion_Synthesis_in_a_Dynamic_Scene_CVPR_2026_paper.html
project_link: null
code_link: null
aliases:
- InterPhys
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 提出可微的连续接触力模型，结合局部表面法向和耦合的静/动摩擦，通过牛顿第三定律统一人与物体动力学，使得梯度优化能强制物理一致性。
primary_logic: 通过将接触力分解为法向阻尼弹簧和切向摩擦，并显式建模物体动力学，可以在动态场景中生成物理一致的人体运动。
claims:
- 在OMOMO数据集上，我们的方法在F1分数上达到0.80，显著优于OMOMO (0.71) 和 InterDiff (0.72) 等基线。
- 在TRUMANS数据集上，我们的方法在所有指标上均优于Trumans基线，例如HandJPE 38.00 vs 47.85，MPJPE 31.28 vs 36.20。
- 消融研究表明，去除动态一致性损失导致F1分数下降7%，证实了物理约束的重要性。
- OMOMO 上 F1 = 0.80
---

# InterPhys: Physics-aware Human Motion Synthesis in a Dynamic Scene

> [!tip] 核心洞察
> 通过将接触力分解为法向阻尼弹簧和切向摩擦，并显式建模物体动力学，可以在动态场景中生成物理一致的人体运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | InterPhys：动态场景中物理感知的人体运动合成 |
| 英文题名 | InterPhys: Physics-aware Human Motion Synthesis in a Dynamic Scene |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xing_InterPhys_Physics-aware_Human_Motion_Synthesis_in_a_Dynamic_Scene_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | InterPhys |
| Dataset | OMOMO, TRUMANS |

> [!tip] 效果简介
> - OMOMO 上，F1 0.80 vs 0.71 (OMOMO) (+0.09)。
> - TRUMANS 上，F1 0.69 vs 0.59 (+0.10)；HandJPE (cm) 38.00 vs 47.85 (-9.85)；MPJPE (cm) 31.28 vs 36.20 (-4.92)。

## 概要

动态场景中的人体运动合成要求生成的运动不仅自然，还必须符合物理规律——例如，人推动箱子时，脚与地面的接触、手与箱子的交互力必须同时满足牛顿第三定律。现有方法面临一个核心瓶颈：**缺乏准确的连续接触力模型，无法处理任意表面和动态物体，导致生成的运动出现浮空、滑动等物理不一致现象**（见 Figure 1）。

InterPhys 针对这一瓶颈提出了三个关键创新：

1.  **可微连续接触力模型**：将接触力分解为沿局部表面法向的阻尼弹簧力与切向的静/动摩擦力，使模型能泛化到任意三维表面，而非仅限于水平地面。
2.  **显式物体动力学耦合**：基于欧拉-拉格朗日方程与牛顿第三定律，显式建模动态物体的运动，确保人与物体之间的交互力始终互为反作用力。
3.  **两阶段扩散训练流程**：第一阶段预测关节力矩、接触参数与手部轨迹；第二阶段以此条件生成全身运动，并通过动态一致性损失强制满足物理方程。

在 OMOMO 和 TRUMANS 两个数据集上，InterPhys 均取得最优性能。以 OMOMO 为例，F1 分数达到 **0.80**，显著优于 OMOMO（0.71）和 InterDiff（0.72）等基线；在 TRUMANS 上，手部关节误差（HandJPE）从 47.85 cm 降至 **38.00 cm**，平均关节误差（MPJPE）从 36.20 cm 降至 **31.28 cm**。消融实验进一步证实，移除动态一致性损失会导致 F1 分数下降约 7%，验证了物理约束的核心作用。



### 问题背景：动态场景中的人-物交互运动合成

生成与动态物体和静态场景自然交互的三维人体运动，是计算机视觉与图形学中的核心挑战，直接支撑机器人学习、虚拟现实和具身智能等应用。给定一段三维物体运动轨迹和一个三维场景布局（Figure 1），任务要求合成一段物理上一致的人体运动序列，使人物同时与移动物体及静态背景环境发生合理的接触与交互。

这一问题的本质难点在于双重物理约束的耦合：人体自身的运动必须满足刚体动力学，同时人与物体、人与场景之间的接触力必须遵循牛顿第三定律——人对物体施加的力，物体必须对人施加等大反向的反作用力。忽略这种耦合，生成的运动就会出现浮空、穿透、滑动等物理不一致现象。

### 现有方法的瓶颈

近年来，基于扩散模型的运动生成方法在人物-场景交互合成上取得了显著进展，代表性工作包括 **OMOMO**（Li et al., ACM TOG 2023）、**CHOIS**（Li et al., ECCV 2024）、**InterDiff**（Xu et al., ICCV 2023）、**InterAct**（Xu et al., CVPR 2025）以及 **Trumans**（Jiang et al., CVPR 2024）。然而，这些方法在处理动态场景中的物理一致性时，面临两个根本性瓶颈。

**瓶颈一：接触力模型过于简化。** 现有方法大多采用简单的接触先验或独立正交弹簧模型来表征接触力。如 Figure 2(a) 所示，PhysPT 等工作假设接触面是静态地平面，用两个独立的正交弹簧表示接触力。这种建模方式无法推广到任意三维曲面，更无法处理动态变化的接触几何。当人物与移动物体的曲面发生交互时，简化的力模型无法正确捕捉沿局部表面法向的法向力，也无法建模切向的静摩擦与动摩擦，导致生成的接触行为物理上不可信。

**瓶颈二：物体动力学被忽略或仅作为条件。** 已有方法要么完全未显式建模物体的动力学，要么仅将物体运动作为条件信号输入生成网络。这意味着物体与人体之间的力交互是单向的——物体运动影响人体，但人体对物体的反作用力被完全忽略。这种非对称建模违背了牛顿第三定律，使得生成的运动在物理模拟器中无法复现，严重限制了其在机器人等下游任务中的可用性。

### 本文动机与核心思路

针对上述瓶颈，InterPhys 的核心动机是：**通过引入一个可微的、物理完备的连续接触力模型，并将物体动力学显式耦合到人体动力学方程中，使得基于梯度的优化能够在训练过程中强制物理一致性。**

具体而言，本文提出三个关键设计：

1. **连续接触力模型（Figure 2(b)）**：将接触力分解为沿局部表面法向的阻尼弹簧力，以及依赖于法向力的切向静摩擦和动摩擦力。该模型可推广到任意三维曲面和动态物体，更贴近真实世界的接触物理。

2. **显式物体动力学耦合**：基于欧拉-拉格朗日方程同时建模人体与物体的动力学，并通过牛顿第三定律将两者的接触力符号相反地耦合（Eq. 2 与 Eq. 3），确保人与物体之间的力交互是双向且一致的。

3. **两阶段扩散与动态一致性损失**：第一阶段预测力系数（关节力矩、接触参数、手部轨迹），第二阶段以力系数为条件生成全身运动，并通过动态一致性损失（Eq. 16）强制生成的运动满足欧拉-拉格朗日方程，消除物理残差。

通过上述设计，InterPhys 在 OMOMO 和 TRUMANS 两个数据集上均取得了最优性能，并在消融实验中验证了动态一致性损失的因果作用——去除该损失后，物体接触 F1 分数下降 7%（Table 3），直接证明了物理约束对生成质量的关键影响。



## 核心方法与创新机理

InterPhys 的核心创新在于通过**物理机理层面的三个关键设计**，解决了现有方法在动态场景中生成物理一致人体运动的根本瓶颈。

### 瓶颈与因果机制

现有方法（如 **OMOMO** (Li et al., ACM TOG 2023)、**InterDiff** (Xu et al., ICCV 2023)）在处理人物-物体交互时，面临一个共性瓶颈：缺乏准确的连续接触力模型，无法处理任意表面和动态物体，导致生成的运动出现浮空、滑动等物理不一致现象。InterPhys 的因果调节变量是一个**可微的连续接触力模型**，该模型结合局部表面法向和耦合的静/动摩擦，并通过牛顿第三定律统一人与物体动力学，使得梯度优化能够强制物理一致性。

### Changed Slot 1：接触力模型

**Baseline 做法**：现有物理感知方法（如 PhysPT）将接触力建模为两个独立的正交弹簧系统，仅适用于静态地面平面（法向始终向上），无法推广到任意 3D 表面（见 Figure 2a）。

**InterPhys 做法**：提出基于局部表面法向的阻尼弹簧与耦合静/动摩擦模型（见 Figure 2b）。具体而言：
- **法向力**建模为沿表面法向 $\\mathbf{n}(\\mathbf{x})$ 的阻尼弹簧力，弹簧刚度与阻尼系数自适应于穿透深度和法向速度（Eq. 6-7）。
- **切向力**分解为静摩擦和动摩擦，且两者均与法向力耦合：静摩擦力在相对速度较小时激活，方向由切向加速度决定（Eq. 9）；动摩擦力与法向力成线性关系，方向相反于相对速度的切向分量（Eq. 12）。
- 接触力的激活通过软门控函数实现，仅在接近表面且不过度穿透时施加力（Eq. 4），保证可微性。

这一设计使得接触力模型能够**泛化到任意几何表面和动态物体**，从根本上突破了现有方法仅适用于静态平面的限制。

### Changed Slot 2：物体动力学显式建模与耦合

**Baseline 做法**：现有方法通常未显式建模物体动力学，或仅将物体运动作为条件输入，忽略了人与物体之间的力交互约束。

**InterPhys 做法**：基于欧拉-拉格朗日方程显式建模物体动力学，并通过牛顿第三定律将其与人体动力学耦合：
- 人体动力学方程（Eq. 2）：$\\mathbf{M}_h \\ddot{\\mathbf{q}} + \\mathbf{C}_h + \\mathbf{G}_h = \\tau + \\mathbf{J}_{hs}^{\\top} \\lambda_s + \\mathbf{J}_{ho}^{\\top} \\lambda_o$
- 物体动力学方程（Eq. 3）：$\\mathbf{M}_o \\ddot{\\mathbf{q}}_o + \\mathbf{C}_o + \\mathbf{G}_o = -\\mathbf{J}_o^{\\top} \\lambda_o$

注意物体方程中接触力 $\\lambda_o$ 的符号与人体方程相反，**严格保证作用力与反作用力相等**，使得生成的运动在物理上自洽。

### Changed Slot 3：两阶段扩散训练流程

**Baseline 做法**：单阶段运动生成，直接从场景/物体条件映射到人体运动，缺乏中间物理表征的监督。

**InterPhys 做法**：设计两阶段扩散流水线（见 Figure 3）：
1. **第一阶段**：基于 Transformer 的扩散模型预测力系数（关节扭矩 $\\tau$、接触参数 $\\mathbf{A}, \\mathbf{B}$）和手部轨迹 $\\mathbf{H}$（Eq. 13）。
2. **第二阶段**：以力系数为条件，另一个扩散模型生成全身人体运动 $\\mathbf{Q}$（Eq. 15），并施加**动态一致性损失** $\\mathcal{L}_{\\mathrm{dyn}}$（Eq. 16），强制生成的运动满足欧拉-拉格朗日方程。

消融实验证实了该设计的有效性：去除动态一致性损失后，物体接触 F1 分数下降 7%（Table 3），验证了物理约束对生成质量的关键作用。



InterPhys 采用**两阶段扩散流水线**，将物理先验嵌入生成过程，实现从动态场景输入到物理一致人体运动的端到端合成。系统输入包含两部分：静态场景的三维体素占用表示 $\mathbf{S} \in \{0,1\}^{N_x \times N_y \times N_z}$，以及动态物体在 $T$ 帧内的运动 $\mathbf{O} \in \mathbb{R}^{T \times B}$（含平移与基元表示）。输出为与场景和物体交互的全身人体运动序列。

流水线由四个核心模块串联构成（Figure 3）：

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_Xing_InterPhys_Physics/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our pipeline. The input static scene S and object motion O is encode to a scene token*

1. **场景与物体编码器** —— 将静态场景 $\mathbf{S}$ 和物体运动 $\mathbf{O}$ 分别编码为场景 token $\mathbf{c}_s$ 和多个运动 token $\mathbf{c}_o$，作为后续扩散模型的条件信号。

2. **第一阶段扩散模型（力系数预测）** —— 以场景和物体 token 为条件，通过 Transformer 扩散模型预测力系数 $\hat{\mathbf{Y}}_0$，包括内部关节力矩 $\boldsymbol{\tau}$、接触参数 $\mathbf{a}, \mathbf{b}$ 以及手部轨迹 $\mathbf{H}$（Eq. 13）。这一阶段的核心作用是将物理交互的“控制信号”从原始运动生成中解耦出来。

3. **第二阶段扩散模型（运动生成）** —— 以上一阶段预测的力系数 $\hat{\mathbf{Y}}_0$ 为条件，结合场景和物体 token，生成全身人体运动 $\hat{\mathbf{Q}}_0$（Eq. 15）。该阶段采用 L1 重建损失 $\mathcal{L}_{\text{reco}}$（Eq. 14）监督预测运动与真实运动的差异。

4. **动态一致性损失** —— 在第二阶段训练时，额外施加物理约束损失 $\mathcal{L}_{\text{dyn}}$（Eq. 16），强制生成的运动满足人体欧拉-拉格朗日方程。该损失逐帧计算动力学残差：质量矩阵×加速度 + 科里奥利/离心力 + 重力 − 场景接触力 − 物体接触力 − 内部力矩，并取 L1 范数。总损失为 $\mathcal{L} = \mathcal{L}_{\text{reco}} + \lambda_{\text{dyn}} \mathcal{L}_{\text{dyn}}$（Eq. 17）。

**因果机制**：第一阶段预测的力系数直接驱动第二阶段的运动生成，而动态一致性损失则通过梯度反向传播约束整个生成过程满足牛顿力学。这种设计使得模型无需在推理时进行物理模拟，即可产出物理一致的运动——接触力模型的可微性（Sec. 3.2）是这一机制成立的关键前提。消融实验证实，移除动态一致性损失会导致 F1 分数下降 7%（Table 3），验证了物理约束对生成质量的因果贡献。

### 补充图表

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_Xing_InterPhys_Physics/figures/001_Figure_1.jpg]]
*Figure 1: Our Task. Our method takes 3D object motion and a 3D scene as input (a), to synthesize physically consistent 3D human motion interacting with both the moving object and the static background scene (b)*



InterPhys 的核心在于将物理先验显式地注入生成过程，其技术路线围绕三个关键模块展开：人体与物体的耦合动力学建模、可微的连续接触力模型，以及两阶段扩散生成流水线。

### 人体与物体耦合动力学

InterPhys 采用欧拉-拉格朗日方程对系统中的人体和动态物体进行统一建模。人体运动状态由 SMPL 模型参数定义：$\mathbf{q} = \{ \pmb{\theta}, \mathbf{R}, \mathbf{T} \} \in \mathbb{R}^{75}$，其中 $\pmb{\theta}$ 为关节姿态，$\mathbf{R}$ 为全局朝向，$\mathbf{T}$ 为全局平移。人体的动力学方程如 Eq. 2 所示：

$$\mathbf{M}_h(\mathbf{q}) \ddot{\mathbf{q}} + \mathbf{C}_h(\mathbf{q}, \dot{\mathbf{q}}) + \mathbf{G}_h(\mathbf{q}) = \tau + \mathbf{J}_{hs}^{\top} \lambda_s + \mathbf{J}_{ho}^{\top} \lambda_o$$

其中 $\mathbf{M}_h$ 为质量矩阵，$\mathbf{C}_h$ 为科里奥利力与离心力项，$\mathbf{G}_h$ 为重力项。等式右侧的驱动力由三部分构成：$\tau$ 为内部关节力矩，$\mathbf{J}_{hs}^{\top} \lambda_s$ 为静态场景对人体施加的接触力，$\mathbf{J}_{ho}^{\top} \lambda_o$ 为动态物体对人体施加的接触力，$\mathbf{J}_{hs}$ 和 $\mathbf{J}_{ho}$ 为对应的接触雅可比矩阵。

动态物体的动力学方程如 Eq. 3 所示：

$$\mathbf{M}_o(\mathbf{q}_o) \ddot{\mathbf{q}}_o + \mathbf{C}_o(\mathbf{q}_o, \dot{\mathbf{q}}_o) + \mathbf{G}_o(\mathbf{q}_o) = - \mathbf{J}_o^{\top} \boldsymbol{\lambda}_o$$

关键设计在于接触力 $\lambda_o$ 的符号与 Eq. 2 相反，这一处理直接体现了牛顿第三定律——物体对人体的作用力与人体对物体的反作用力大小相等、方向相反。这种显式的双向耦合使得系统能够自然地保持人-物交互的物理一致性，避免了现有方法中常见的浮空、滑动等伪影。

### 连续接触力模型

接触力模型是 InterPhys 最核心的技术贡献。现有方法（如 PhysPT）假设接触面为静态地平面，将接触力建模为两个独立的正交弹簧系统，无法处理任意三维表面和动态物体。InterPhys 提出了一种物理上更准确的连续接触力模型，其关键在于引入局部表面法向，并将接触力分解为法向与切向分量。

**相对位置分解**：给定接触点 $\mathbf{p}$ 和对应表面点 $\mathbf{x}$，相对位置 $\tilde{\mathbf{p}} = \mathbf{p} - \mathbf{x}$ 被分解为法向分量和切向分量：

$$\tilde{\mathbf{p}}_{\perp} = (\tilde{\mathbf{p}}^{\top} \mathbf{n}(\mathbf{x})) \mathbf{n}(\mathbf{x}), \quad \tilde{\mathbf{p}}_{\parallel} = \tilde{\mathbf{p}} - \tilde{\mathbf{p}}_{\perp}$$

其中 $\mathbf{n}(\mathbf{x})$ 为表面点 $\mathbf{x}$ 处的局部法向量。

**接触力激活函数**：为保证接触力的连续性和可微性，模型采用软门控机制，如 Eq. 4 所示：

$$\pmb{\lambda}(\mathbf{p}) = h(-\alpha(\|\tilde{\mathbf{p}}\| - d_0)) h(\beta(\tilde{\mathbf{p}}^{\top}\mathbf{n}(\mathbf{x}) + d_1)) \mathbf{f}(\mathbf{p})$$

其中 $h(\cdot)$ 为平滑阶跃函数，第一个门控在人体接近表面时激活，第二个门控在过度穿透时抑制，$d_0$ 和 $d_1$ 为阈值参数。

**法向力**：法向分量采用阻尼弹簧模型，如 Eq. 6–7 所示：

$$\mathbf{f}_{\perp}(\mathbf{p}) = k(\mathbf{p}) \mathbf{n}(\mathbf{x})$$

$$k(\mathbf{p}) = -\kappa(\|\tilde{\mathbf{p}}_{\perp}\| - d_0) - \delta(\dot{\tilde{\mathbf{p}}}^{\top}\mathbf{n}(\mathbf{x}))$$

与 PhysPT 的关键区别在于，弹簧力的方向始终沿局部表面法向 $\mathbf{n}(\mathbf{x})$，而非固定的竖直方向，这使得模型能够处理任意朝向的表面。

**切向摩擦力**：切向分量进一步细分为静摩擦和动摩擦。静摩擦力（Eq. 9）在相对速度较小时激活：

$$\mathbf{f}_s(\mathbf{p}) = h(-\gamma(\|\dot{\tilde{\mathbf{p}}}\| - v_0)) \rho \| \tilde{\mathbf{p}}_{\parallel} \| - d_0 | \mathbf{d}_{\parallel}$$

动摩擦力（Eq. 12）与法向力成线性关系，方向与相对速度的切向分量相反：

$$\mathbf{f}_k(\mathbf{p}) = -\mu \|\mathbf{f}_{\perp}(\mathbf{p})\| \frac{\dot{\tilde{\mathbf{p}}}_{\parallel}}{\|\dot{\tilde{\mathbf{p}}}_{\parallel}\|}$$

对于动态物体，动摩擦方向由净加速度（去除重力）的切向分量决定（Eq. 10）。这种耦合的静/动摩擦建模使得接触力能够正确反映真实物理行为，是 InterPhys 在动态场景中保持物理一致性的关键。

### 两阶段扩散生成流水线

InterPhys 采用两阶段 Transformer 扩散模型实现从场景和物体运动到人体运动的生成（Fig. 3）。

**场景与物体编码**：静态场景 $\mathbf{S} \in \{0, 1\}^{N_x \times N_y \times N_z}$ 通过三维体素表示，动态物体运动 $\mathbf{O} \in \mathbb{R}^{T \times B}$ 包含 $T$ 帧的平移和 BPS 特征。两者分别编码为场景 token $\mathbf{c}_s$ 和运动 token $\mathbf{c}_o$。

**第一阶段：力系数预测**（Eq. 13）：

$$\hat{\mathbf{Y}}_0 = f_{\phi}(\mathbf{Y}_n, \mathbf{c}_s, \mathbf{c}_o, n)$$

第一阶段扩散模型以场景和物体 token 为条件，从噪声 $\mathbf{Y}_n$ 中预测力系数 $\hat{\mathbf{Y}}_0$，包括内部关节力矩 $\mathbf{T}$、接触参数 $\mathbf{A}, \mathbf{B}$ 以及手部轨迹 $\mathbf{H}$。

**第二阶段：全身运动生成**（Eq. 15）：

$$\hat{\mathbf{Q}}_0 = f_{\theta}(\mathbf{Q}_n, \hat{\mathbf{Y}}_0, \mathbf{c}_s, \mathbf{c}_o, n)$$

第二阶段扩散模型以第一阶段预测的力系数为条件，从噪声人体运动 $\mathbf{Q}_n$ 中生成全身运动 $\hat{\mathbf{Q}}_0$。

**动态一致性损失**：为保证生成运动的物理合理性，InterPhys 引入了动态一致性损失（Eq. 16）：

$$\mathcal{L}_{\mathrm{dyn}} = \sum_{t=1}^{T} \| \mathbf{M}_h(\hat{\mathbf{q}}_t) \ddot{\hat{\mathbf{q}}}_t + \mathbf{C}_h(\hat{\mathbf{q}}_t, \dot{\hat{\mathbf{q}}}_t) + \mathbf{G}_h(t) - \mathbf{J}_{hs}(t)^{\top} \lambda_s(\mathbf{a}_t) - \mathbf{J}_{ho}(t)^{\top} \lambda_o(\mathbf{b}_t) - \boldsymbol{\tau}_t \|_1$$

该损失直接最小化欧拉-拉格朗日方程的残差，强制生成的运动满足物理定律。第二阶段总损失为重建损失与动态一致性损失的加权组合（Eq. 17）：

$$\mathcal{L} = \mathcal{L}_{\mathrm{reco}} + \lambda_{\mathrm{dyn}} \mathcal{L}_{\mathrm{dyn}}$$

其中 $\mathcal{L}_{\mathrm{reco}} = \mathbb{E}_{\mathbf{Q}_n, n} [ \| \hat{\mathbf{Q}}_0 - \mathbf{Q}_0 \|_1 ]$ 为标准 L1 重建损失。消融实验（Table 3）表明，去除 $\mathcal{L}_{\mathrm{dyn}}$ 后物体接触 F1 分数下降 7%，证实了物理约束对生成质量的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_Xing_InterPhys_Physics/figures/002_Figure_2.jpg]]
*Figure 2: Continous contact force model. a) The PhysPT model assumes a static ground plane and represents contact force with two independent orthogonal springs, b) Our model generalizes to arbitrary 3D surfaces by incorporating local surface normals for the normal force and explicitly modeling tangential static and kinetic friction that are dependent to the normal force, enabling physically consistent interactions in dynamic scenes*



## 实验与关键发现

### 评估设置

InterPhys 在两个代表性基准上验证其物理一致性运动生成能力：

- **OMOMO**（Li et al., ACM TOG 2023）：包含坐、抬、推等多种人-物交互序列，提供物体运动作为条件输入，评估模型在给定物体轨迹下生成合理人体运动的能力。
- **TRUMANS**（Jiang et al., CVPR 2024）：涵盖动态场景中的人-物-场景三方交互，提供更丰富的静态场景几何约束。

评估指标包括：**F1 分数**（接触精度与召回率的调和平均）、**MPJPE**（全身关节位置误差，cm）、**HandJPE**（手部关节位置误差，cm）、**Sc.Pen.**（场景穿透深度，cm）等。所有指标越低越好，F1 越高越好。

### 主实验结果

#### OMOMO 数据集

Table 1 展示了 InterPhys 与现有方法的定量对比。在 F1 分数上，InterPhys 达到 **0.80**，显著优于 OMOMO（0.71）、CHOIS（0.66）、InterDiff（0.72）和 InterAct（0.74）。这一 0.09 的 F1 提升源于连续接触力模型对任意表面法向的适应能力——基线方法的简单弹簧模型仅适用于地平面，无法在物体表面产生正确的法向约束力。

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_Xing_InterPhys_Physics/figures/004_Table_1.jpg]]
*Table 1: Comparison of methods on the OMOMO dataset. Lower is better for error metrics; higher is better for precision, recall, and F1*

Figure 4 的定性对比进一步揭示了基线方法的典型失败模式：OMOMO 生成的手部位置常偏离物体表面，导致“浮空”接触；CHOIS 和 InterDiff 虽能保持大致接触，但缺乏物理约束使得接触力方向不合理，产生滑动伪影。InterPhys 通过显式建模法向阻尼弹簧和切向摩擦，使手部在接触阶段稳定贴合物体表面。

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_Xing_InterPhys_Physics/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison on OMOMO. From left to right: object-only context, ground truth, our prediction, and predictions from OMOMO, CHOIS, InterDiff, and InterAct*

#### TRUMANS 数据集

在 TRUMANS 上的优势更为显著（Table 2）：**F1 从 0.59 提升至 0.69**（+0.10），**HandJPE 从 47.85 cm 降至 38.00 cm**（降幅 20.6%），**MPJPE 从 36.20 cm 降至 31.28 cm**（降幅 13.6%），**Sc.Pen. 从 33.48 cm 降至 21.03 cm**（降幅 37.2%）。

场景穿透的大幅降低是关键亮点。TRUMANS 涉及静态场景（如墙壁、桌面），基线 Trumans 仅将场景作为条件输入，缺乏显式物理约束，导致身体频繁穿透场景几何。InterPhys 的场景接触力 $\lambda_s$ 通过局部表面法向施加排斥力，在梯度优化中自然抑制穿透。

Figure 5 的力可视化（红色：物体→人，黄色：场景→人，橙色：关节内力）直观展示了物理一致性：当人推动物体时，红色箭头方向与物体运动方向一致，满足牛顿第三定律；当人倚靠墙壁时，黄色箭头沿墙面法向提供支撑力。

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_Xing_InterPhys_Physics/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison on Trumans. Each row shows ground truth, the Turmans baseline, and our method. Arrows illustrate estimated forces: red for forces from the dynamic object to the human, yellow for forces from the static scene to the human, and orange for internal joint forces*

### 消融实验

Table 3 和 Figure 6 报告了关键设计选择的消融结果。最核心的发现是：**去除动态一致性损失 $\mathcal{L}_{\mathrm{dyn}}$ 后，物体接触 F1 分数下降 7%**（从 0.80 降至约 0.74），同时场景穿透深度显著增加。

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_Xing_InterPhys_Physics/figures/008_Table_3.jpg]]
*Table 3: Ablation study of our method. Lower is better for error metrics; higher is better for precision, recall, and F1*

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_Xing_InterPhys_Physics/figures/007_Figure_6.jpg]]
*Figure 6: Ablation study comparison on OMOMO*

这一消融验证了物理约束在训练中的因果作用：仅靠 L1 重建损失，模型倾向于模仿训练数据中的运动模式，但缺乏对接触力方向的显式监督。动态一致性损失通过强制生成的运动满足欧拉-拉格朗日方程（Eq. 2），将接触力预测与人体动力学耦合，使得梯度反向传播时能纠正不合理的力方向。

其他消融观察包括：去除连续接触力模型中的切向摩擦分量（仅保留法向弹簧）会导致物体推动场景中手部滑动加剧；降低动态一致性损失的权重 $\lambda_{\mathrm{dyn}}$ 会线性削弱物理约束效果，但过高的权重会抑制运动多样性——论文未提供具体的权重扫描曲线，该点需手动验证。

### 失败模式与局限

尽管定量结果一致占优，InterPhys 仍存在若干可观测的失败模式：

1. **复杂旋转物体的接触稳定性**：当物体经历快速旋转时，表面法向的瞬时变化可能导致接触力方向剧烈波动，手部出现短暂“脱附”后再附着。这源于连续接触力模型的局部线性化假设——在物体角速度较大时，法向的帧间变化可能超出阻尼弹簧的响应带宽。
2. **多人/多物体场景未验证**：当前框架假设单人与单物体交互，牛顿第三定律的耦合形式（Eq. 3）可扩展至多体场景，但接触力分配和碰撞避免机制尚未定义。
3. **穿透的残余问题**：尽管 Sc.Pen. 大幅降低，21.03 cm 的绝对值仍表明存在残余穿透。这主要发生在物体与场景几何交界处，接触力激活函数（Eq. 4）的软门控设计可能在此类多表面过渡区域响应不足。

论文未提供失败案例的系统性统计分析，上述观察基于 Figure 4/5 的定性样本和消融趋势推断，部分结论需要更多定量验证。



## 定位与知识库关联

### 1. 与前驱工作的关系

InterPhys 的核心贡献在于首次将**可微的连续接触力模型**与**显式物体动力学**统一到基于扩散的人-物交互运动生成框架中。其与前驱工作的关系可从三个关键设计槽位来定位。

**接触力模型**：早期方法如 **PhysPT**（未提供完整引用，需人工核实）将接触力建模为两个独立的正交弹簧，仅适用于静态地平面。InterPhys 将接触力分解为沿局部表面法向的阻尼弹簧力（Eq. 6-7）和切向的静/动摩擦（Eq. 9, 12），并通过软门控激活函数（Eq. 4）实现连续可微，从而泛化到任意三维表面。这一设计直接解决了基线方法在动态场景中因缺乏准确接触力而导致的浮空、滑动等物理不一致问题。

**物体动力学耦合**：**OMOMO**（Li et al., ACM TOG 2023）和 **CHOIS**（Li et al., ECCV 2024）将物体运动仅作为条件输入，未显式建模物体动力学。**InterDiff**（Xu et al., ICCV 2023）引入了物理信息，但未将物体动力学与人体动力学通过牛顿第三定律耦合。InterPhys 则显式建模物体的欧拉-拉格朗日方程（Eq. 3），使接触力 $ \lambda_o $ 在人体和物体方程中符号相反，强制保持相互作用力的互逆性。

**训练流程**：与单阶段生成方法（如 **InterAct**, Xu et al., CVPR 2025）不同，InterPhys 采用两阶段扩散：第一阶段预测力系数（关节扭矩 $ \tau $、接触参数 $ A, B $ 和手部轨迹 $ H $），第二阶段以力系数为条件生成全身运动 $ Q $，并施加动态一致性损失 $ \mathcal{L}_{\mathrm{dyn}} $（Eq. 16）强制生成的运动满足欧拉-拉格朗日方程。

### 2. 适用边界

InterPhys 的适用边界由其核心假设定义：

- **场景表示**：静态场景以三维体素 $ \mathbf{S} \in \{0,1\}^{N_x \times N_y \times N_z} $ 编码，物体运动以 $ T \times B $ 维张量表示。该方法依赖已知的场景几何和物体运动轨迹，无法处理未知或部分可观的场景。
- **接触假设**：接触力模型假设人体与表面之间的接触是点接触，且法向力由阻尼弹簧近似。对于大面积软接触（如人体躺靠在沙发上）或流体交互，该模型可能不适用。
- **单物体交互**：当前框架仅支持单个刚体物体与单人交互，尚未扩展到多物体、关节工具或多人协作场景。
- **数据依赖**：方法在 OMOMO 和 TRUMANS 数据集上验证，均为受控环境下的有限类别交互。泛化到开放域场景的能力尚未验证。

### 3. 局限与开放问题

**已知局限**：论文未明确列出局限性（limitations 字段为空），但可从方法设计推断以下潜在问题：

- 两阶段扩散训练流程增加了工程复杂度，且第一阶段力系数预测的误差会传播到第二阶段。
- 动态一致性损失 $ \mathcal{L}_{\mathrm{dyn}} $ 的计算需要显式构建质量矩阵 $ \mathbf{M}_h $、科里奥利项 $ \mathbf{C}_h $ 和重力项 $ \mathbf{G}_h $，这依赖于 SMPL 人体模型的运动学链和惯性参数，对模型精度敏感。

**开放问题**（来自 verified_analysis）：

1. **多体扩展**：如何将该框架扩展到涉及多个动态物体、关节工具和多人的协作行为中？这需要重新设计接触力分配机制和物体间动力学耦合。
2. **环境多样化与不确定性**：如何适应多样化的环境上下文（如室外场景、非刚性地形），并处理观测中的不确定性（如遮挡、传感器噪声）？
3. **实时推理**：当前基于扩散的生成流程推理速度较慢，如何实现实时或近实时的物理一致运动合成，以支持交互式应用？

### 4. 知识库定位

InterPhys 位于**物理信息人物运动合成**和**人-物交互生成**的交叉点。其核心知识贡献——基于表面法向的连续接触力模型和牛顿第三定律耦合的物体动力学——为后续工作提供了可复用的物理先验模块。该框架可被视为连接纯数据驱动生成（如 InterDiff, InterAct）和全物理仿真（如强化学习中的接触动力学）的中间层，通过可微物理损失在生成质量与物理一致性之间取得平衡。



## 原文 PDF

![[paperPDFs/CVPR_2026/InterPhys_Physics_aware_Human_Motion_Synthesis_in_a_Dynamic_Scene.pdf]]
