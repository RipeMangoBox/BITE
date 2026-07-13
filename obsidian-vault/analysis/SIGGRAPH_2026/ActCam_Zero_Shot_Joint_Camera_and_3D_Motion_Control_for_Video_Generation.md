---
title: "ActCam: Zero-Shot Joint Camera and 3D Motion Control for Video Generation"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2026
pdf_ref: paperPDFs/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation.pdf
project_link: https://elkhomar.github.io/actcam/
code_link: null
aliases:
- ActCam
tags:
- SIGGRAPH_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 构造相机对齐的深度与姿态条件信号，并采用两阶段去噪调度策略（早期使用深度+姿态以锁定全局结构，后期仅使用姿态以保留高频细节）。
primary_logic: 通过从参考图像中移除静态角色以避免条件冲突，利用三维场景转移对齐角色深度，以及分阶段应用深度和姿态条件，可以在冻结的预训练模型上实现零样本的联合控制。
claims:
- 在两阶段调度中，早期使用深度+姿态、后期仅使用姿态能有效平衡相机控制和动作保真度。
- ActCam在RealisDance-Val基准上超过Uni3C，MPJPE和Sampson误差更低，VBench平均分更高。
- 移除参考角色可避免生成重复角色，场景转移的对齐能改善遮挡顺序。
- 仅使用姿态条件（N_D=0）会导致相机与角色运动模糊，而过度使用深度（N_D=1）会过度约束背景。
---

# ActCam: Zero-Shot Joint Camera and 3D Motion Control for Video Generation

> [!tip] 核心洞察
> 通过从参考图像中移除静态角色以避免条件冲突，利用三维场景转移对齐角色深度，以及分阶段应用深度和姿态条件，可以在冻结的预训练模型上实现零样本的联合控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | ActCam：视频生成中零样本联合相机与三维运动控制 |
| 英文题名 | ActCam: Zero-Shot Joint Camera and 3D Motion Control for Video Generation |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2605.06667) · [Project](https://elkhomar.github.io/actcam/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | ActCam |
| Dataset | RealisDance-Val with moving cameras |

> [!tip] 效果简介
> - RealisDance-Val with moving cameras 上，MPJPE↓ 0.2087 vs 0.2121 (-0.0034)；SE↓ 0.4546 vs 0.5665 (-0.1119)；SC↑ 0.9212 vs 0.9084 (+0.0128)。

## 概要

### 问题瓶颈

从单张参考图像生成可控视频时，现有方法通常只能独立控制角色的表演动作或相机运动，而难以在零样本条件下同时精确控制两者。其根本瓶颈在于：缺乏一种**相机对齐的多模态条件表示**，能够将角色的三维运动信号与场景的几何信号统一到目标相机视角下。当相机运动与角色运动同时变化时，仅依赖二维关键点或固定深度的条件构造方式容易产生运动歧义、遮挡错误和身份漂移。

### 核心方法定位

ActCam 是一种**纯推理时方法**，无需微调预训练视频扩散模型。它通过以下三个关键机制实现零样本联合控制：

1. **相机对齐的条件信号构造**：从参考图中移除静态角色以避免条件冲突，估计纯背景深度并恢复角色的三维运动序列，随后通过加权质心对齐将角色深度匹配到背景场景中，最后在目标相机视角下渲染深度+姿态和仅姿态两种条件信号。
2. **两阶段去噪调度策略**：在去噪过程的早期步骤（前 20% 步数）使用深度+姿态条件以锁定全局相机结构和场景几何，后期步骤切换为仅姿态条件以保留角色动作的高频细节。
3. **场景转移与深度对齐**：利用重要性加权（越靠近角色掩码边界的点权重越高）计算非角色区域的加权质心，通过仿射变换将恢复的角色深度对齐到背景深度坐标系中，从而改善遮挡顺序并减少撕裂伪影。

### 核心结论

在RealisDance-Val动态相机基准上，ActCam在运动控制精度（MPJPE ↓3.4‰）、几何一致性（SE ↓0.1119）和生成质量（VBench平均分 +0.0127）方面均超越当前最接近的联合控制基线**Uni3C**（Cao et al., arXiv 2025）。消融实验证实：仅使用姿态条件（N_D=0）会导致相机与角色运动的歧义，而全程使用深度条件（N_D=1）会过度约束背景使其静止；参考角色移除和加权场景转移分别消除了重复角色伪影和深度错位问题。在静态相机设置下，ActCam同样优于多个使用2D关键点条件的基线方法，验证了其三维感知管线的优越性。

### 方法谱系与知识库定位

ActCam 建立在预训练的图像到视频扩散模型 **VACE**（Jiang et al., arXiv 2025）之上，利用其原生支持的深度图和关键点条件能力。与现有的静态相机运动控制方法（如 **UniAnimate-DiT**（Wang et al., arXiv 2025）、**MimicMotion**（Zhang et al., ICML 2024）、**Animate-X**（Tan et al., ICLR 2024）、**Hyper-Motion**（Xu et al., arXiv 2025）、**HumanVid**（Wang et al., NeurIPS 2024）、**Wan-Animate**（Cheng et al., arXiv 2025）、**SteadyDancer**（Zhang et al., arXiv 2025）等）不同，ActCam 在推理时引入了三维场景感知的条件构造和分阶段调度策略，将相机控制与动作控制统一到同一框架下。相较于联合控制基线 **Uni3C**，ActCam 通过移除参考角色和深度对齐避免了条件信号中的静态冲突，从而在动态相机场景下获得更优的控制精度和视觉质量。



### 问题域：单图视频生成中的联合控制

从单张参考图像生成可控的人体运动视频是视觉内容创作中的核心需求。然而，现有的视频生成方法在同时控制**角色表演动作**与**相机轨迹**方面存在显著瓶颈。具体而言，大多数方法要么假设相机静止，仅关注角色动作的迁移；要么在引入相机运动时，缺乏一种将运动信号与场景几何信号统一到目标相机视角下的多模态条件表示。这种缺失导致生成结果中出现相机运动与角色运动的歧义——模型难以区分画面中的运动究竟来自相机移动还是角色自身的动作。

### 现有方法的缺口

当前主流的角色动作控制方法（如 **UniAnimate-DiT**、**VACE**、**MimicMotion**、**Animate-X** 等）通常依赖二维关键点作为条件信号，在静态相机设定下取得了可观的运动保真度。然而，当相机发生运动时，二维关键点本身并不包含相机视角信息，因此无法为生成模型提供区分相机运动与角色运动的必要线索。

在联合控制方向上，**Uni3C**（Cao et al., arXiv 2025）是目前最接近本工作设定的方法。它尝试同时处理相机与角色运动，但其条件构造方式仍存在两个关键局限：其一，条件信号未经过相机对齐处理，导致控制精度不足；其二，参考图像中的静态角色被保留在场景几何中，与动态插入的角色形成条件冲突，容易产生重复角色或遮挡错误。

### 核心瓶颈与本文动机

上述问题的本质瓶颈在于：**如何在无需训练的情况下，构造一种相机对齐的多模态条件表示，将角色运动信号与场景几何信号统一到目标相机视角下**。这一瓶颈的解决面临三个相互耦合的子问题：

1. **条件冲突**：参考图像中的静态角色若保留在深度图中，会与动态角色的深度信号冲突，导致生成结果中出现重复角色。
2. **深度对齐**：从动作视频恢复的三维角色深度需要与目标场景的背景深度在几何上对齐，否则会产生错误的遮挡顺序和撕裂伪影。
3. **控制信号的时序分配**：深度条件虽然能提供强大的相机控制，但过度使用会过度约束背景，损害运动保真度；而仅使用姿态条件则无法区分相机与角色运动。

ActCam 正是针对这一瓶颈而设计：通过移除参考角色以避免条件冲突，利用三维场景转移实现角色与背景的深度对齐，并采用两阶段去噪调度策略——早期使用深度加姿态条件以锁定全局结构，后期仅使用姿态条件以保留高频细节——从而在冻结的预训练模型上实现零样本的联合控制。



## 核心方法与创新机理

ActCam 的核心创新在于**将联合相机与三维运动控制从需要训练的范式转变为零样本推理范式**，通过在冻结的预训练视频扩散模型（VACE）上构造相机对齐的多模态条件信号，并引入两阶段去噪调度策略，实现了无需任何微调的精确联合控制。

### 创新一：相机对齐的多模态条件信号构造

现有方法（如 **Uni3C**，Cao et al., arXiv 2025）通常直接在图像空间使用二维关键点作为姿态条件，这导致相机运动与角色运动之间产生歧义——二维关键点的位移既可能来自角色动作，也可能来自相机移动。ActCam 从根本上改变了条件信号的构造方式：

- **从参考图中移除静态角色**：通过图像修复技术将参考图中的角色擦除，仅保留背景深度图 $\mathcal{D}_{\mathrm{bg}}$。这避免了原始参考角色在深度条件中留下“静态印记”，从而消除生成结果中出现重复角色的问题（见 Figure 7）。
- **三维姿态恢复与场景转移**：使用 GVHMR 从动作视频中恢复三维人体运动序列，然后通过**加权质心对齐**将角色的三维深度匹配到背景场景的深度网格中。具体而言，定义权重函数 $w(u,v) = \exp\left(-\mathrm{dist}(\mathbf{x}_{u,v}^{\mathrm{ref}}, M)\right)$（Equation 2），越靠近角色掩码边界的背景点权重越高；计算参考深度图和背景深度图在非角色区域的加权质心 $\mathbf{p}_{\mathrm{ref}}$ 和 $\mathbf{p}_{\mathrm{bg}}$（Equation 3），再通过仿射变换将角色点深度对齐到背景坐标系（Equation 4）。这种几何感知的放置策略有效改善了遮挡顺序，减少了撕裂伪影（见 Figure 8）。
- **目标相机视角渲染**：在对齐后的三维场景中，以目标相机轨迹渲染两种条件信号——深度+姿态信号和仅姿态信号，确保所有条件信息都在统一的相机坐标系下表达。

### 创新二：两阶段去噪调度策略

传统条件控制方法在整个去噪过程中使用恒定的条件信号（如始终同时施加深度和姿态条件）。ActCam 发现这种策略存在根本性矛盾：

- **全程使用深度条件（$N_D=1$）**会过度约束场景几何，导致相机运动时背景静止不动（见 Figure 5），因为深度条件强制每一帧的背景深度与参考图保持一致。
- **完全不用深度条件（$N_D=0$）**则造成相机运动与角色运动之间的严重歧义，模型无法区分二维位移的来源（见 Figure 6）。

ActCam 的解决方案是引入**两阶段条件调度**（Equation 5）：

$$c(t)_{\tau} = \begin{cases} \mathcal{R}^{C_{\tau}}(\hat{S}_{\tau}, \mathcal{D}_{\mathrm{bg}}), & \text{if } t \leq t_{\mathrm{stop}},\\ \mathcal{R}^{C_{\tau}}(\hat{S}_{\tau}), & \text{if } t > t_{\mathrm{stop}}. \end{cases}$$

在去噪的**早期高噪声阶段**（$t \leq t_{\mathrm{stop}}$），同时注入深度和姿态条件，利用深度信息锁定全局场景结构和相机视角，为后续生成提供稳固的几何框架；在**后期低噪声阶段**（$t > t_{\mathrm{stop}}$），切换到仅姿态条件，释放对背景的过度约束，使模型能够灵活生成符合角色运动的高频细节。实验表明，当深度条件占比 $N_D=0.2$（即总去噪步数的前20%）时，VBench 综合得分达到最优（见 Figure 4），在相机控制精度和运动保真度之间取得最佳平衡。

### 创新三：零样本范式下的条件冲突消解

ActCam 的三个关键设计——**角色移除、场景转移、两阶段调度**——协同解决了一个深层问题：在冻结的预训练模型中，不同条件信号之间可能产生冲突。角色移除避免了参考角色深度与动态角色深度之间的冲突；场景转移通过几何对齐消解了角色深度与背景深度之间的不一致；两阶段调度则在时间维度上解耦了结构约束与细节生成的矛盾。这三个机制共同使得 ActCam 能够在不修改模型参数的前提下，仅通过推理时的条件工程实现精确的联合控制。



ActCam 是一个纯推理时方法，保持预训练的图像到视频扩散骨干网络（VACE）固定不变，通过构造相机对齐的多模态条件信号和两阶段去噪调度，实现对角色表演动作与相机轨迹的零样本联合控制。其整体流程如图 2 所示，包含以下核心模块：

**1. 角色移除与背景深度估计**  
给定参考图像 $I_{\text{ref}}$，首先利用修复模型将参考角色从图像中移除，再对修复后的图像进行单目深度估计，得到仅包含背景的深度图 $\mathcal{D}_{\text{bg}}$。这一操作避免了参考角色在深度条件中产生静态“幽灵”角色，从而与动态角色产生条件冲突（Figure 7 消融实验验证了该步骤的必要性）。

**2. 四维运动恢复**  
从给定的表演视频 $V_{\text{act}}$ 中，使用单目三维人体运动估计器 GVHMR 恢复三维人体运动序列 $S_{\tau}$。随后，采用最小二乘刚体变换（在 $\tau=0$ 时刻将 $S_0$ 与参考图像提取的关键点对齐），将运动序列拟合到参考角色的空间位置，得到变换后的姿态序列 $\hat{S}_{\tau}$。

**3. 场景转移**  
场景转移模块负责将对齐后的角色深度融入背景三维网格中。其核心机制是：  
- 在参考深度图和背景深度图的非角色区域上，通过重要性加权函数 $w(u,v) = \exp(-\text{dist}(\mathbf{x}_{u,v}^{\text{ref}}, M))$ 计算加权质心 $\mathbf{p}_{\text{ref}}$ 和 $\mathbf{p}_{\text{bg}}$；  
- 利用质心差异对角色深度点进行仿射对齐，使角色在目标场景中的遮挡顺序和空间位置保持三维一致性。消融实验（Figure 8）表明，无场景转移会导致遮挡顺序错误和撕裂伪影，而重要性加权相比均匀加权能获得最佳对齐效果。

**4. 控制信号光栅化**  
在目标相机轨迹的每个时间步，将场景转移后的三维角色姿态和背景深度渲染为二维条件图：  
- **深度+姿态信号**：同时包含角色姿态骨骼和场景深度信息；  
- **仅姿态信号**：仅包含角色姿态骨骼，不含深度约束。

**5. 两阶段去噪调度**  
这是 ActCam 实现零样本联合控制的关键调度策略。生成过程由连续流 ODE 控制，条件信号 $c(t)_{\tau}$ 根据去噪时间步 $t$ 动态切换：
$$c(t)_{\tau} = \begin{cases} \mathcal{R}^{C_{\tau}}(\hat{S}_{\tau}, \mathcal{D}_{\text{bg}}), & \text{if } t \leq t_{\text{stop}},\\ \mathcal{R}^{C_{\tau}}(\hat{S}_{\tau}), & \text{if } t > t_{\text{stop}}. \end{cases}$$
- **早期步骤**（$t \leq t_{\text{stop}}$）：注入深度+姿态条件，利用深度信息锁定全局场景结构和相机运动，避免相机与角色运动之间的歧义；  
- **后期步骤**（$t > t_{\text{stop}}$）：切换为仅姿态条件，释放深度对高频细节的过度约束，使模型专注于保持角色动作的保真度。

消融实验（Figure 4、Figure 5、Figure 6）系统验证了该调度的必要性：$N_D=0$（全程无深度）导致相机与角色运动混淆；$N_D=1$（全程深度）过度约束背景，使相机运动时场景静止；最优截止比例 $N_D=0.2$ 在相机控制与运动保真度之间取得最佳平衡。

### 补充图表

![[assets/figures/papers/ActCam_Zero-Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation_595bf21ac5f0/figures/005_Figure_3.jpg]]
*Figure 3: User study. We compare with Uni3C on camera adherence (Camera) and motion faithfulness (Motion) with respect to the conditioning input, alongside overall visual quality (Visual). We considerably outperform Uni3C, the closest method to ours*



ActCam 是一个纯推理时方法，保持预训练 VACE 骨干网络冻结，通过精心设计的条件信号构造和调度策略实现零样本联合控制。其核心架构由五个顺序模块构成，并在生成动力学上遵循连续流 ODE 模型。

### 生成动力学建模

整个去噪生成过程被建模为由常微分方程（ODE）控制的连续流：

$$\frac{\mathrm{d}\boldsymbol{z}_t}{\mathrm{d}t} = \boldsymbol{v}_\theta(\boldsymbol{z}_t, t, C)$$

其中 $\boldsymbol{z}_t$ 表示时刻 $t$ 的潜变量状态，$\boldsymbol{v}_\theta$ 是冻结的骨干网络预测的速度场，$C$ 为条件信号。该公式是整个方法的基础框架，ActCam 的所有创新均围绕条件信号 $C$ 的构造和调度展开。

### 模块一：角色移除与背景深度估计

参考图像中静态角色的存在会导致生成结果中的角色重复（Figure 7）。ActCam 首先对参考图像进行角色修复（inpainting），移除人物后估计纯背景深度图 $\mathcal{D}_{\mathrm{bg}}$，并据此构建背景三维网格。这一步是消除条件冲突的关键前置操作。

### 模块二：四维运动恢复

从动作视频 $V_{\mathrm{act}}$ 中恢复三维人体运动序列，使用单目三维人体运动估计器 **GVHMR**（Chu et al., 2024）提取每帧的三维人体姿态 $S_{\tau}$。随后通过最小二乘刚体变换将运动序列对齐到参考角色：

$$\hat{S}_{\tau} = s \cdot R S_{\tau} + \hat{t}$$

其中 $R$ 为旋转矩阵，$s$ 为缩放因子，$\hat{t}$ 为平移向量，变换参数在 $\tau=0$ 时刻通过参考图像中提取的关键点与 $S_0$ 之间的刚体对齐估计得到。

### 模块三：场景转移

这是 ActCam 最具原创性的模块之一，解决恢复的角色深度与背景深度之间的空间对齐问题。首先定义重要性权重函数，强调靠近角色掩码边界的点：

$$w(u,v) = \exp\left(-\mathrm{dist}(\mathbf{x}_{u,v}^{\mathrm{ref}}, M)\right)$$

其中 $\mathrm{dist}(\cdot, M)$ 表示像素点到角色掩码 $M$ 的距离。基于此权重，分别计算参考深度图和背景深度图中非角色区域的加权质心：

$$\mathbf{p}_{\mathrm{ref}} = \frac{\sum_{(u,v)\notin\mathcal{M}} w(u,v) \mathbf{x}_{u,v}^{\mathrm{ref}}}{\sum_{(u,v)\notin\mathcal{M}} w(u,v)}, \qquad \mathbf{p}_{\mathrm{bg}} = \frac{\sum_{(u,v)\notin\mathcal{M}} w(u,v) \mathbf{x}_{u,v}^{\mathrm{bg}}}{\sum_{(u,v)\notin\mathcal{M}} w(u,v)}$$

最后通过仿射变换将角色点深度对齐到背景坐标系：

$$z_{\mathrm{bg}}^{\mathrm{char}} = \left(z_{\mathrm{ref}}^{\mathrm{char}} - p_{\mathrm{ref}}^z\right) \frac{p_{\mathrm{bg}}^z}{p_{\mathrm{ref}}^z} + p_{\mathrm{bg}}^z$$

该公式通过缩放和平移操作，将角色的相对深度分布映射到背景场景的深度范围内。消融实验（Figure 8）表明，若不进行场景转移（无对齐），条件信号无法保持三维一致性；均匀加权虽能改善放置，但重要性加权才能获得最优效果。

### 模块四：条件信号光栅化

在目标相机视角 $C_{\tau}$ 下，使用可微渲染器 $\mathcal{R}$ 将三维场景渲染为两类二维条件信号：
- **深度+姿态信号**：$\mathcal{R}^{C_{\tau}}(\hat{S}_{\tau}, \mathcal{D}_{\mathrm{bg}})$，同时编码场景几何和角色姿态
- **仅姿态信号**：$\mathcal{R}^{C_{\tau}}(\hat{S}_{\tau})$，仅编码角色骨架信息

### 模块五：两阶段去噪调度

这是 ActCam 实现相机与运动联合控制的核心机制。条件信号根据去噪时间步动态切换：

$$c(t)_{\tau} = \begin{cases} \mathcal{R}^{C_{\tau}}(\hat{S}_{\tau}, \mathcal{D}_{\mathrm{bg}}), & \text{if } t \leq t_{\mathrm{stop}},\\ \mathcal{R}^{C_{\tau}}(\hat{S}_{\tau}), & \text{if } t > t_{\mathrm{stop}}. \end{cases}$$

其中 $t_{\mathrm{stop}}$ 为切换阈值，论文定义比例参数 $N_D = t_{\mathrm{stop}} / T$（$T$ 为总去噪步数）。在早期高噪声阶段（$t \leq t_{\mathrm{stop}}$）使用深度+姿态信号以锁定全局结构，确保相机运动和场景几何的一致性；在后期低噪声阶段（$t > t_{\mathrm{stop}}$）切换为仅姿态信号，避免深度条件过度约束背景细节，释放模型对高频纹理和动作细节的生成能力。

消融实验（Figure 4）表明，$N_D = 0.2$ 时 VBench 得分最优。$N_D = 0$（全程无深度）会导致相机与角色运动的歧义（Figure 6），而 $N_D = 1$（全程深度）会过度约束场景，使背景在相机运动时保持静止（Figure 5）。

![[assets/figures/papers/ActCam_Zero-Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation_595bf21ac5f0/figures/009_Figure_5.jpg]]
*Figure 5: Importance of conditioning schedule. Excessive depth guidance (setting N _ { D } \ = \ 1 ) can overly constrain the scene, producing static backgrounds under camera motion (center, red circle). Instead, N _ { D } \< 1 1 allows to flexibly move the barbell to follow the human motion (right)*

### 补充图表

![[assets/figures/papers/ActCam_Zero-Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation_595bf21ac5f0/figures/001_Figure_1.jpg]]
*Figure 1: Overview. ActCam enables zero-shot joint control of acting motion and camera motion for single-image video generation from a reference image, assuming only widespread conditioning capability of the backbone model on depth and keypoints. Given a reference image, an acting video representing the desired motion, and a target per-frame camera trajectory, ActCam generates a video that preserves identity while following both motion and cinematography*



## 实验与关键发现

### 实验设置

ActCam 基于预训练的 **VACE** 图像到视频扩散模型（Jiang et al., arXiv 2025），所有实验均在推理时完成，未对骨干网络进行任何微调。评估分为两类场景：

- **移动相机（联合控制）**：使用 **RealisDance-Val** 基准，配置 4 种相机预设，每种预设选取 100 个参考片段，总计 400 个测试用例。直接对比方法为 **Uni3C**（Cao et al., arXiv 2025），这是当前唯一支持联合相机与运动控制的方法。
- **静态相机（仅运动控制）**：同样在 RealisDance-Val 上评估，使用 VBench 指标。对比方法包括 **Moore-AnimateAnyone**、**HumanVid**（Wang et al., NeurIPS 2024）、**MimicMotion**（Zhang et al., ICML 2024）、**Animate-X**（Tan et al., ICLR 2024）、**Hyper-Motion**（Xu et al., arXiv 2025）、**UniAnimate-DiT**（Wang et al., arXiv 2025）、**VACE**、**Wan-Animate**（Cheng et al., arXiv 2025）和 **SteadyDancer**（Zhang et al., arXiv 2025）。

评估指标涵盖生成质量（VBench 综合分）、控制精度（MPJPE↓）、几何一致性（SE↓）、语义一致性（SC↑）和图像质量（IQ↑），同时引入 **WorldScore**（Chen et al., 2025）评估三维一致性（3D-C）和物体控制（OC）。

### 主实验结果

#### 移动相机下的联合控制

Table 1 展示了 ActCam 与 Uni3C 在移动相机场景下的定量对比。ActCam 在所有指标上均取得领先：

![[assets/figures/papers/ActCam_Zero-Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation_595bf21ac5f0/figures/003_Table_1.jpg]]
*Table 1: Joint camera and character control. We evaluate against Uni3C both on VBench, focusing on generation quality, and assessing control quality (MPJPE) and geometric consistency (SE). We also use WorldScore [Chen et al. 2025] to evaluate the 3D consistency (3D-C) and object control (OC) of the generations. We outperform in all cases Uni3C, the closest baseline in our setup*

| 指标 | ActCam | Uni3C | 提升 |
|------|--------|-------|------|
| MPJPE↓ | 0.2087 | 0.2121 | -0.0034 |
| SE↓ | 0.4546 | 0.5665 | -0.1119 |
| SC↑ | 0.9212 | 0.9084 | +0.0128 |
| IQ↑ | 0.7212 | 0.6640 | +0.0572 |
| VBench Avg↑ | 0.8497 | 0.8370 | +0.0127 |

其中 Sampson 误差（SE）的降幅最为显著（-19.8%），表明 ActCam 在几何一致性上具有明显优势。这直接归因于 ActCam 的相机对齐深度条件——Uni3C 使用原始图像的二维深度，未考虑目标相机视角下的场景几何变化，而 ActCam 通过场景转移和相机对齐渲染，使深度信号与目标视角严格一致。

Figure 9 的定性对比进一步揭示了 Uni3C 的典型失败模式：在相机运动时，Uni3C 的角色运动出现不真实的形变，且相机控制精度不足。ActCam 则保持了角色外观和运动的一致性。

![[assets/figures/papers/ActCam_Zero-Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation_595bf21ac5f0/figures/011_Figure_9.jpg]]
*Figure 9: Comparison with Uni3C. Uni3C yields suboptimal camera control (top, middle) and unrealistic character motion (bottom). In the insets, a visualization of the control signal for both Uni3C and ActCam. Fig. 10. Different cameras. We first show the conditioning signal and ActCam results (top two rows). In the next three rows, we variate camera movements. As visible, the character appearance and motion remain consistent*

用户研究（Figure 3）从相机遵循度（Camera）、运动保真度（Motion）和整体视觉质量（Visual）三个维度对比 ActCam 与 Uni3C，ActCam 在所有维度上均显著优于 Uni3C。

#### 静态相机下的运动控制

Table 2 显示，即使在静态相机设定下，ActCam 的 VBench 综合得分也优于所有使用二维关键点作为条件的基线方法。这验证了 ActCam 的三维姿态管线（GVHMR 恢复 → 三维拟合 → 相机对齐渲染）相比传统二维关键点条件的优越性——三维表示能更完整地编码人体运动的空间信息，减少投影歧义。

![[assets/figures/papers/ActCam_Zero-Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation_595bf21ac5f0/figures/004_Table_2.jpg]]
*Table 2: Static camera comparison. We evaluate on RealisDance-Val [Zhou et al. 2025b] with a static camera using VBench [Huang et al. 2024a,b]. The improved performance of ActCam compared to alternatives using 2D keypoints as conditions advocates for the superiority of our 3D-based pipeline*

### 消融实验

#### 深度条件比例 N_D

N_D 控制两阶段调度中深度条件的持续时间比例：当去噪步数占比 ≤ N_D 时使用深度+姿态条件，之后切换为仅姿态条件。Figure 4 展示了 VBench 得分随 N_D 的变化曲线：

![[assets/figures/papers/ActCam_Zero-Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation_595bf21ac5f0/figures/007_Figure_4.jpg]]
*Figure 4: Effect of N _ { D } on VBench score. The figure shows the average VBench scores as a function of N _ { D } , where the conditioning switches from pose+depth to pose-only. Early switching under-constrains the generation, while late switching (low ?? ) can propagate depth artifacts into highfrequency details, harming results. We set an optimal N _ { D } = 0 . 2*

- **N_D = 0.2 时取得最优**，平衡了相机控制强度与运动保真度。
- N_D 过小（过早切换）导致相机约束不足，生成结果出现相机与角色运动的歧义。
- N_D 过大（过晚切换）使深度伪影传播到高频细节阶段，损害生成质量。

#### 深度条件的必要性

Figure 6 对比了 N_D = 0（全程无深度）与 N_D = 0.2 的生成效果。仅使用姿态条件时，模型无法区分相机运动与角色运动——例如，相机推进与角色向前移动会产生相似的关键点位移，导致生成结果中相机和角色运动互相混淆。引入深度条件后，背景的深度变化明确编码了相机运动信息，解除了这一歧义。

![[assets/figures/papers/ActCam_Zero-Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation_595bf21ac5f0/figures/006_Figure_6.jpg]]
*Figure 6: Importance of depth. Providing only pose information ( N _ { D } = 0 , top) for conditioning creates ambiguities between camera and character motion. Conversely, using depth yields the correct character and camera motions ( N _ { D } = 0 . 2 , bottom)*

#### 全程深度的过约束问题

Figure 5 展示了 N_D = 1（全程深度条件）的失败模式：深度条件过度约束场景几何，导致相机运动时背景保持静止，与相机运动应有的视差变化矛盾。相比之下，N_D < 1 允许后期去噪步骤仅用姿态条件精炼细节，使背景能够灵活响应相机运动。

#### 参考角色移除

Figure 7 验证了参考角色移除的必要性。若不进行修复（inpainting）而直接估计深度，参考图像中的静态角色会被编码进深度图中。生成时，该深度条件会诱导模型在目标位置再次生成该角色，导致画面中出现重复人物。移除参考角色后，深度图仅包含背景几何，避免了这一条件冲突。

![[assets/figures/papers/ActCam_Zero-Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation_595bf21ac5f0/figures/008_Figure_7.jpg]]
*Figure 7: Character removal. Without removal, the reference character is captured in the depth map, yielding duplicate subjects*

#### 场景转移中的深度对齐

Figure 8 对比了三种场景转移策略：
1. **无对齐**：直接将恢复的角色深度放入背景深度图，不进行任何调整。结果出现明显的遮挡顺序错误和撕裂伪影。
2. **均匀加权对齐**：使用均匀权重计算质心进行深度对齐，改善了角色位置，但仍存在局部深度偏移。
3. **重要性加权对齐（ActCam 采用）**：通过 $w(u,v) = \exp(-\mathrm{dist}(\mathbf{x}_{u,v}^{\mathrm{ref}}, M))$ 对靠近角色掩码边界的点赋予更高权重，使对齐更关注角色与场景的接触区域。该策略实现了最佳的深度一致性，有效消除了遮挡伪影。

![[assets/figures/papers/ActCam_Zero-Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation_595bf21ac5f0/figures/010_Figure_8.jpg]]
*Figure 8: Importance of scene transfer. Without scene transfer (No alignment), the condition does not respect 3D coherence. Uniform weighting improves placement but importance weighting (ours) is required to achieve best results. The red arrows (right column) show depth/positions offsets*

### 失败模式与局限性

综合实验与分析，ActCam 的主要失败模式和局限包括：

1. **深度估计质量依赖**：深度条件的效果高度依赖单目深度估计的精度。在极端相机视角或复杂遮挡下，深度估计误差会直接传导到生成结果，导致几何不一致。
2. **场景转移的仿射假设**：当前场景转移假设参考深度与背景深度之间仅存在仿射变换（缩放+平移）。当相机视角变化剧烈或场景存在显著透视变形时，该假设可能失效。
3. **骨干模型限制**：ActCam 要求预训练模型支持深度和关键点双重条件，目前仅在 VACE 上验证，无法直接迁移到其他架构（如 DiT）。
4. **长序列与复杂动态**：实验主要在短视频片段上进行，未充分测试长序列生成中的误差累积问题，以及多角色交互场景下的稳定性（尽管 Figure 13 展示了初步的多角色结果）。
5. **最优 N_D 的泛化性**：N_D = 0.2 的最优值是在当前实验设定下确定的，其在不同骨干模型、不同相机运动幅度下的泛化性尚需进一步验证。

![[assets/figures/papers/ActCam_Zero-Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation_595bf21ac5f0/figures/013_Figure_12.jpg]]
*Figure 12: Different scenes and different cameras. To show the flexibility of our approach, we apply the same motion to two characters in different scenes, by also varying the camera control. ActCam still renders the correct motion. Fig. 13. Multi-character results. ActCam handles multiple characters by applying the scene transfer and motion fitting independently per character*

### 补充图表

![[assets/figures/papers/ActCam_Zero-Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation_595bf21ac5f0/figures/012_Figure_11.jpg]]
*Figure 11: Different scenes. We display two outputs of ActCam showing the same motion rendered on two characters in different scenes, using the same camera controls*



## 定位与知识库关联

### 与现有工作的关系

ActCam 处于零样本视频生成控制的交叉地带，其核心设定——在冻结的预训练扩散骨干上仅通过推理时条件构造实现联合控制——使其与现有方法形成了清晰的边界。

**联合相机与运动控制基线**：最直接的可比工作是 **Uni3C** (Cao et al., arXiv 2025)，这是目前唯一同时支持相机轨迹与角色动作控制的零样本方法。ActCam 在相同的冻结 VACE 骨干上，通过构造相机对齐的深度-姿态多模态条件信号和两阶段去噪调度，在 RealisDance-Val 移动相机基准上全面超越 Uni3C：MPJPE 从 0.2121 降至 0.2087，Sampson 误差从 0.5665 降至 0.4546（Table 1）。这一差距的因果机制在于 Uni3C 使用 2D 关键点作为条件，缺乏场景几何约束，导致相机运动与角色运动之间存在歧义；ActCam 通过引入背景深度图和角色-场景深度对齐，将运动信号与场景几何信号统一到目标相机视角下，从根本上消除了这一歧义。

**静态相机运动控制基线**：在静态相机设定下，ActCam 与一系列仅关注角色运动控制的方法进行了比较，包括 **MimicMotion** (Zhang et al., ICML 2024)、**Animate-X** (Tan et al., ICLR 2024)、**HumanVid** (Wang et al., NeurIPS 2024)、**UniAnimate-DiT** (Wang et al., arXiv 2025)、**VACE** (Jiang et al., arXiv 2025)、**Hyper-Motion** (Xu et al., arXiv 2025)、**Wan-Animate** (Cheng et al., arXiv 2025)、**SteadyDancer** (Zhang et al., arXiv 2025) 以及 Moore-AnimateAnyone。ActCam 在 VBench 平均分上优于这些方法（Table 2），论文将此归因于其基于 3D 姿态的条件构造管线相比 2D 关键点方法在运动表征精度上的优势。需要指出的是，这一比较的公平性基础在于所有方法共享相同的预训练骨干或同级别的生成能力，但部分基线（如 UniAnimate-DiT）使用不同的骨干架构，直接比较的因果归因需谨慎对待。

**方法边界与适用条件**：ActCam 的有效性受限于以下前提：
1. **骨干模型能力依赖**：ActCam 要求预训练的图像到视频扩散模型必须原生支持深度图和姿态图条件。当前实现基于 VACE 骨干，若迁移到不支持这些条件类型的模型（如部分 DiT 架构），方法将无法直接应用。
2. **深度与姿态估计质量**：背景深度估计和 3D 人体运动恢复（GVHMR）的质量直接影响最终生成效果。在极端相机视角、严重遮挡或复杂光照条件下，深度估计可能出现不一致，导致场景转移失败。
3. **场景转移假设**：角色-场景深度对齐基于一个仿射变换假设（Equation 4），即参考深度与背景深度之间仅存在缩放和平移关系。在具有复杂遮挡关系、大幅视角变化或非平面场景结构的情况下，这一假设可能被违反，导致遮挡顺序错误或深度撕裂伪影。
4. **对象类别限制**：当前验证仅针对人物角色。方法的核心组件——GVHMR 人体运动恢复和 SMPL 姿态拟合——专为人体设计，尚未扩展到一般物体或动物。
5. **序列长度与场景复杂度**：实验主要在短视频片段上进行（RealisDance-Val 基准），未在更长序列或高度动态场景下进行充分压力测试。

### 局限与开放问题

**已知局限**：论文明确指出的局限包括上述骨干依赖、深度估计敏感性和场景转移假设。消融实验进一步揭示了方法的关键脆弱点：当深度条件比例 N_D 设置为 1（全程深度）时，背景被过度约束，在相机运动时产生静态背景伪影（Figure 5）；当 N_D=0（无深度）时，相机运动与角色运动之间出现歧义（Figure 6）。最优 N_D=0.2 的设定表明，方法对去噪调度参数较为敏感，需要在相机控制强度与运动保真度之间进行精细权衡。

**开放问题**：
1. **最优调度的精确参数**：论文仅给出比例 N_D=0.2，但未公开精确的截止时间步 t_stop 数值，这限制了可复现性和在其他骨干上的调参指导。
2. **移动相机评估的相机预设**：实验中使用的 4 种相机预设的具体参数（轨迹类型、速度、旋转幅度等）未详细说明，影响对方法相机控制能力的精确理解。
3. **生成分辨率与采样步数**：实验使用的具体分辨率和 ODE 求解器步数未明确报告，这些超参数直接影响生成质量和推理效率。
4. **跨骨干泛化**：ActCam 的双阶段调度策略是否可推广到其他扩散骨干（如基于 DiT 的架构）或视频扩散模型（如 SVD），仍需验证。
5. **非人物体与多人交互**：方法能否扩展到动物、一般刚体或多人交互场景，需要新的 3D 运动估计器和场景转移策略。
6. **长序列稳定性**：在更长视频生成中，深度条件的累积误差是否会导致漂移或场景崩溃，尚未探索。

### 知识库定位

ActCam 在视频生成控制的知识谱系中占据以下位置：

- **问题层级**：零样本推理时控制 → 联合相机与运动控制 → 基于 3D 几何对齐的条件构造。
- **技术路线**：区别于基于训练的方法（如 CameraCtrl、MotionCtrl 等需要微调骨干的方法），ActCam 属于纯推理时条件工程路线，与 Uni3C 共享这一范式但通过引入深度-场景几何对齐实现了质的提升。
- **核心贡献的可迁移性**：两阶段去噪调度（早期深度+姿态，后期仅姿态）是一个与骨干架构解耦的策略，理论上可迁移到任何支持深度和姿态条件的扩散模型。角色移除与场景转移的深度对齐策略同样具有通用性，只要目标场景允许合理的深度估计。
- **评估基准位置**：在 RealisDance-Val + VBench + WorldScore 的评估体系下，ActCam 在移动相机联合控制任务上建立了新的零样本基线。但该基准的覆盖范围有限（4 种相机预设、100 个参考片段），更全面的评估体系仍有待建立。



## 原文 PDF

![[paperPDFs/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation.pdf]]
