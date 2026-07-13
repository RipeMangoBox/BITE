---
title: "PerpetualWonder: Long-horizon Action-conditioned 4D Scene Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PerpetualWonder_Long_horizon_Action_conditioned_4D_Scene_Generation.pdf
project_link: "https://johnzhan2023.github.io/PerpetualWonder/"
code_link: null
aliases:
- PerpetualWonder
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 视觉-物理对齐粒子（VPP）表示，将每个物理粒子锚定一组高斯原语，形成双向连接。
primary_logic: 通过建立前向物理驱动和后向模型优化的闭环，利用多视图一致性约束，实现长时域动态场景的一致生成和更新。
claims:
- 消融实验表明，取消VPP表示会导致特征断裂和严重伪影（Figure 6）。
- 消融实验表明，直接多视图优化导致纹理模糊和闪烁，而渐进优化产生一致结果（Figure 7）。
- 用户研究显示，在物理合理性（80.8%偏好）和运动保真度（86.3%偏好）上，PerpetualWonder显著优于WonderPlay（Table 2）。
- 在World-Score指标上，PerpetualWonder在相机可控性和3D一致性上均取得最佳性能（Table 1）。
---

# PerpetualWonder: Long-horizon Action-conditioned 4D Scene Generation

> [!tip] 核心洞察
> 通过建立前向物理驱动和后向模型优化的闭环，利用多视图一致性约束，实现长时域动态场景的一致生成和更新。

| 字段 | 内容 |
|------|------|
| 中文题名 | PerpetualWonder：长时域动作驱动4D场景生成 |
| 英文题名 | PerpetualWonder: Long-horizon Action-conditioned 4D Scene Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.04876) · [Project](https://johnzhan2023.github.io/PerpetualWonder/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | PerpetualWonder |
| Dataset | World-Score, 2AFC 用户研究 |

> [!tip] 效果简介
> - World-Score (10个场景) 上，Camera Controllability 93.26 vs Next best (未明确给出数值，但文章声称最佳) (最佳)。
> - World-Score 上，3D Consistency 80.41 vs Next best (最佳)；Imaging Quality 66.98 vs Next best (最佳)。
> - 2AFC 用户研究 (350名参与者) 上，Physics Plausibility (偏好率) 80.8% vs WonderPlay (50% 随机) (+30.8% 超过随机)。

## 概要

### 1. 问题背景与瓶颈

从单张图像生成可交互的4D动态场景，是通向具身智能与世界模拟器的关键一步。现有混合生成模拟器（如**WonderPlay**）通常将物理状态与视觉表示分离处理：物理求解器驱动粒子运动，视觉模块独立渲染外观，二者之间缺乏显式绑定。这一架构导致**动力学误差累积**——视觉优化无法反向修正物理状态，物理驱动的视觉预测也无法保证多视角一致性，使得长时域连续交互下场景质量迅速退化。

### 2. 核心方法定位

PerpetualWonder 的核心贡献在于提出**视觉-物理对齐粒子（Visual-Physical aligned Particle, VPP）**表示，将物理粒子与高斯原语建立双向绑定关系，形成统一的视觉-物理桥梁。基于VPP，方法构建了一个**闭环生成系统**（Figure 2）：

- **前向物理传递**：物理求解器根据用户动作驱动粗动力学。
- **反向神经优化**：利用多视角视频生成模型精炼渲染结果，并通过仿真一致性损失将视觉优化信号反馈至物理状态更新。

这一闭环使场景状态在长时域动作序列中保持一致演进，解决了先前方法中视觉与物理割裂的根本问题。

### 3. 主要结果

定量与定性实验验证了方法的有效性：

- **World-Score 基准**（Table 1）：在相机可控性（93.26）、3D一致性（80.41）和成像质量（66.98）三个维度上均取得最优性能。
- **用户研究**（Table 2）：350名参与者的2AFC测试中，PerpetualWonder 在物理合理性上获得80.8%的偏好率，在运动保真度上获得86.3%的偏好率，显著超越 WonderPlay 的随机水平（50%）。
- **长时域对比**（Figure 5）：在多轮交互场景中，PerpetualWonder 保持稳定的视觉质量和物理一致性，而 WonderPlay 出现明显的动力学漂移和视觉退化。

### 4. 方法谱系与知识库定位

PerpetualWonder 处于**物理驱动的4D生成**与**可微渲染优化**的交叉地带，其方法谱系可梳理如下：

| 方法 | 物理-视觉结合方式 | 优化监督来源 | 状态更新闭环 |
|------|-------------------|-------------|-------------|
| **WonderPlay** | 物理粒子与高斯原语无显式绑定 | 单视角视频精炼 | 仅前向驱动 |
| **GEN3C** | 无物理模拟，纯相机控制视频生成 | — | — |
| **Open-Sora** | 无物理模拟，条件视频生成 | — | — |
| **PerpetualWonder** | VPP：粒子锚定高斯原语，偏移可学 | 渐进多视角优化 | 前向+反向闭环 |

相对于基线方法，PerpetualWonder 在三个关键维度上实现了结构性改进：

1. **物理-视觉绑定**：从无显式绑定变为VPP双向锚定，使每个物理粒子对应一组可学偏移的高斯原语。
2. **优化监督**：从单视角精炼升级为渐进多视角优化——先优化输入视角，再以低权重引入其他视角，最后联合优化，确保多视角一致性。
3. **闭环更新**：从仅前向物理驱动扩展为前向粗动力学→反向视觉优化→粒子位置平均更新的完整闭环，使物理状态随视觉优化同步修正。

与相关领域工作的关系：在**3D/4D生成**层面，方法继承了 Gaussian Splatting 的可微渲染框架，但将其与物理模拟深度耦合；在**世界模型**层面，区别于纯数据驱动的视频生成模型（如Open-Sora），PerpetualWonder 显式引入物理先验，在长时域交互中保持物理合理性。

### 5. 局限与开放问题

当前方法存在两个主要局限：

- **计算开销**：完整模拟循环约需16分钟（初始化~8分钟，前向<1分钟，反向~7分钟），远未达到实时交互要求。
- **未见几何残缺**：对于输入图像中未出现的物体几何（如从外进入视场的物体），方法无法完整生成（Figure S3）。

由此引出三个关键开放问题：

1. 如何在不牺牲生成质量的前提下大幅降低反向优化开销，实现实时交互式长时域模拟？
2. 如何补齐输入图像中未见的物体几何，以处理全新物体的交互？
3. 对于更复杂的多物体交互和精细材料模拟，VPP表示和优化框架是否仍然足够？

### 问题背景：长时域动作驱动4D场景生成

从单张图像生成可交互的动态3D场景是计算机视觉与图形学的核心挑战之一。给定一张静态场景图像和一系列用户指定的动作（如施加风力、点力或重力），目标是生成一个在时域上连续、物理合理且多视角一致的4D场景。这一能力对于虚拟现实、游戏内容生成和机器人仿真等应用至关重要。

### 现有方法缺口：物理-视觉解耦导致误差累积

现有方法主要分为两类。一类是纯视频生成模型（如 **Open-Sora**），它们能够根据文本或力的描述生成动态视频，但缺乏显式的物理建模，难以保证长时域交互下的物理一致性和3D几何一致性。另一类是混合生成模拟器（如 **WonderPlay**），其核心思路是将物理模拟与视觉渲染相结合：先用物理求解器生成粗动力学，再用视频生成模型精炼视觉外观。

然而，这些混合方法存在一个根本性瓶颈：**物理状态与视觉表示相互分离**。物理粒子仅用于驱动前向模拟，而视觉优化（如3D高斯精炼）并不反馈更新物理状态。这导致两个严重后果：

1. **误差累积**：每一轮动作交互后，优化后的视觉表示与物理状态之间产生偏差，该偏差在长时域交互中被逐轮放大，最终导致场景崩溃。
2. **多视角不一致**：现有方法通常仅在输入视角上进行视觉精炼，缺乏多视角约束，导致从其他视角观察时出现纹理闪烁和几何断裂。

### 本文动机：建立物理-视觉闭环

PerpetualWonder 的核心动机在于打破上述分离范式，建立一个**物理模拟与视觉优化之间的双向闭环**。其关键洞察是：如果能够将每个物理粒子与一组视觉原语（高斯原语）显式绑定，那么前向物理传递可以驱动视觉预测，而反向视觉优化也可以更新物理状态，从而在每一轮交互中消除累积误差，实现长时域一致的4D场景生成。

## 核心方法与创新机理

PerpetualWonder 的核心创新在于构建了一个**视觉-物理闭环生成系统**，从根本上解决了先前混合生成模拟器（如 **WonderPlay**）因物理状态与视觉表示分离而导致的动力学误差累积问题。该系统围绕三个紧密耦合的“changed slots”展开。

### 视觉-物理对齐粒子（VPP）表示

先前方法中，物理粒子与高斯原语之间缺乏显式绑定，视觉优化无法反向作用于物理状态。PerpetualWonder 提出了**视觉-物理对齐粒子（VPP）**，将每个物理粒子 $p_j$ 作为锚点，绑定一组 $K$ 个高斯原语。每个高斯原语 $k$ 的3D位置由可学偏移量 $\tilde{p}_{j,k}$ 决定，并通过 $\tanh$ 函数约束在粒子尺寸 $\delta$ 范围内：

$$\mu_{j,k} = p_j + \tanh(\tilde{p}_{j,k}) \cdot \delta$$

这种设计形成了物理与视觉之间的**双向桥梁**：前向物理传递驱动视觉预测，反向优化则通过更新高斯属性来修正物理状态。消融实验（Figure 6）表明，移除 VPP 而使用标准 3DGS 优化会导致动力学特征断裂、物体分裂和严重视觉伪影，验证了该表示对于维持物理-视觉一致性的关键作用。

### 渐进多视角优化策略

先前方法（如 WonderPlay）依赖单视角视频进行精炼，难以保证多视角一致性。PerpetualWonder 引入了**渐进多视角优化**：首先对输入视角进行精炼，随后以较低权重引入其他视角，最终联合优化所有视角。这一策略的核心在于利用视频生成模型（如 **GEN3C**）合成稠密环绕视图，并通过多视角一致性约束来监督场景表示的更新。消融实验（Figure 7）显示，直接使用未经精炼的多视角视频进行优化会导致纹理模糊、外观闪烁和场景表示损坏，而渐进策略则能产生一致且稳定的结果。

### 前向-反向闭环状态更新

PerpetualWonder 建立了一个**完整的闭环系统**，由三个关键阶段组成：

1. **前向物理传递**：给定当前场景状态 $\hat{S}_t$ 和用户动作 $\mathcal{A}_t$，通过物理算子 $\Phi_p$ 生成粗动力学：
   $$\hat{S}_{t+1} = \Phi_p(\hat{S}_t, \mathcal{A}_t)$$

2. **反向神经优化**：利用多视角精炼视频和仿真一致性损失 $\mathcal{L}_{\text{sim}}$ 优化场景表示。其中 $\mathcal{L}_{\text{sim}}$ 惩罚高斯原语位置偏离其对应物理粒子的程度：
   $$\mathcal{L}_{\text{sim}} = \frac{1}{T \cdot J} \sum_{t=1}^{T} \sum_{j=1}^{J} \left\| p_{j,t} - \frac{1}{K} \sum_{k=1}^{K} \mu_{j,k,t} \right\|_2^2$$

3. **闭环衔接**：将优化后的高斯位置平均值更新物理粒子，使精炼后的状态 $S_T$ 成为下一轮动作的初始状态 $S_0$，从而在长时域交互中持续修正累积误差。

这一闭环机制使得 PerpetualWonder 能够在多轮连续动作下保持物理合理性和视觉一致性。用户研究（Table 2）显示，在物理合理性上 80.8% 的参与者偏好 PerpetualWonder，在运动保真度上则达到 86.3%，显著优于 WonderPlay 的随机水平（50%）。

PerpetualWonder 的整体 pipeline 围绕一个**闭环迭代系统**构建，该系统将物理模拟与神经渲染优化交替运行，从单张图像出发生成长时域、动作驱动的 4D 场景。其核心架构可分解为以下阶段（参见 Figure 2）：

![[assets/figures/papers/paper_list_l2564_https_arxiv_org_abs_2602_04876/figures/002_Figure_2.jpg]]
*Figure 2: Overview of PerpetualWonder. Given an input image, based on the visual-physical aligned particle, we reconstruct a 3D scene from synthesized dense views. Then we iterate between a forward physics pass and a backward neural optimization. The forward pass leverages physical simulation to generate coarse scene dynamics. Then the backward optimization updates the scene according to the multi-view refined videos from the video generation model. The closed-loop system enables long-horizon actions for the final 4D scene generation. The rendered results on the right showcase the generated scene from each consecutive action*

**1. 3D 场景初始化**
给定单张输入图像，首先使用相机控制视频生成模型 **GEN3C** 合成稠密环绕视角的视频序列，随后通过 COLMAP 进行运动恢复结构（SfM）获取场景点云，并采用 3D Gaussian Splatting（3DGS）优化重建初始 3D 场景。重建完成后，对前景物体进行分割，将其与静态背景解耦，为后续的物理-视觉绑定奠定基础。

**2. 视觉-物理对齐粒子（VPP）构建**
在前景物体上，将物理粒子（physics particles）与高斯原语（Gaussian primitives）建立显式锚定关系：每个物理粒子 $p_j$ 作为一组 $K$ 个高斯原语的锚点，高斯原语的 3D 位置由粒子位置加上一个可学偏移量决定（$\mu_{j,k} = p_j + \operatorname{tanh}(\tilde{p}_{j,k}) \cdot \delta$），偏移量被约束在粒子尺寸 $\delta$ 内。这一 VPP 表示构成了物理与视觉之间的**双向桥梁**，是闭环系统的基础。

**3. 闭环模拟循环**
系统在长度为 $T$ 的时间窗口内循环执行三个关键步骤：

- **前向物理传递**：根据用户输入的动作 $\mathcal{A}_t$，利用物理求解器 $\Phi_p$ 对当前场景状态 $\hat{S}_t$ 进行步进式粗动力学计算（$\hat{S}_{t+1} = \Phi_p(\hat{S}_t, \mathcal{A}_t)$），生成整个时间窗口内的粗 4D 场景序列。

- **反向神经优化**：对前向传递产生的粗场景进行多视角渲染，利用视频生成模型对渲染结果进行精炼（refinement），然后通过**渐进多视角优化策略**——先优化输入视角，再以低权重引入其他视角，最后联合优化——来更新场景的高斯属性（颜色、不透明度、协方差等）。优化过程受像素级损失 $\mathcal{L}_{\mathrm{p}}$ 和仿真一致性损失 $\mathcal{L}_{\mathrm{sim}}$ 的联合约束，后者惩罚高斯原语位置偏离其锚定物理粒子的程度。

- **闭环闭合**：优化完成后，用精炼后的高斯原语位置均值更新对应物理粒子的位置，将时间窗口末端的状态 $S_T$ 作为下一轮动作的初始状态 $S_0$，实现跨轮次的连续交互。

**4. 输入输出流**
- **输入**：单张 RGB 图像 + 用户定义的动作序列（如全局力场、3D 点力等）。
- **输出**：支持新视角渲染的 4D 场景（3D 场景 + 时间维度），可呈现长时域、物理合理的动态交互结果。

这一闭环设计的核心优势在于：前向物理传递驱动视觉预测，而反向优化则利用多视角一致性约束修正物理状态，从而**阻断动力学误差的累积**，使长时域连续交互成为可能。消融实验证实，取消 VPP 表示会导致特征断裂和严重伪影（Figure 6），而放弃渐进多视角优化则会产生纹理模糊和外观闪烁（Figure 7）。

### 3.1 视觉-物理对齐粒子（VPP）表示

PerpetualWonder 的核心创新在于提出了一种统一的场景表示——**视觉-物理对齐粒子（Visual-Physical aligned Particle, VPP）**。该表示解决了先前混合生成模拟器（如 WonderPlay）中物理状态与视觉表示分离导致的动力学误差累积问题。VPP 的关键设计是将物理粒子与高斯原语（Gaussian primitives）建立显式的双向绑定关系。

具体而言，场景在时刻 $t$ 的状态被分解为背景和动态前景两部分：

$$\boldsymbol{S}_t = \left( \boldsymbol{B}_t, \mathcal{F}_t \right)$$

其中背景 $\boldsymbol{B}_t$ 保持静态，动态前景 $\mathcal{F}_t$ 由一组物理粒子 $\{p_j\}$ 构成。每个物理粒子 $p_j$ 作为锚点，绑定一组 $K$ 个高斯原语 $\{g_{j,k}\}$。高斯原语的 3D 位置通过可学习的偏移量限定在粒子半径 $\delta$ 范围内：

$$\mu_{j,k} = p_j + \operatorname{tanh}(\tilde{p}_{j,k}) \cdot \delta$$

其中 $\tilde{p}_{j,k}$ 是可学习的偏移参数，$\operatorname{tanh}$ 函数将其约束在 $[-1,1]$ 区间，确保高斯原语始终位于物理粒子的邻域内。这种约束是 VPP 双向桥梁作用的基础：前向物理模拟驱动高斯原语的粗运动，反向优化则通过更新高斯属性来修正物理状态。

此外，为了建模动态场景中的时序变化，VPP 引入了可学习的**时序不透明度**：

$$o_t(t) = \exp\left( -\frac{1}{2} \times \left( \frac{t - \mu_t}{s_d} \right)^2 \right)$$

该函数由中心时间 $\mu_t$ 和持续时间 $s_d$ 参数化，控制每个高斯原语在时间窗口内的可见性，使表示能够自然地处理物体的出现与消失。

### 3.2 多视角渐进优化与损失函数

在反向优化阶段，PerpetualWonder 采用**渐进多视角优化策略**，以解决直接多视角优化导致的纹理模糊和外观闪烁问题。该策略分为三个阶段：首先使用输入视角的视频进行初步优化；然后引入其他视角但赋予较低权重；最后对所有视角进行联合优化。这种渐进策略确保了多视角渲染的一致性。

优化的总体损失函数由背景损失、前景损失和仿真一致性损失三部分组成：

$$\mathcal{L} = \mathcal{L}_{\mathrm{p}}( \mathrm{Render}(\mathcal{B}_t) \odot (1 - \mathbf{M}), \mathbf{V}_t \odot (1 - \mathbf{M}) ) + \mathcal{L}_{\mathrm{p}}( \mathrm{Render}(\mathcal{G}_t), \mathbf{V}_t \odot M ) + \lambda_{\mathrm{sim}} \mathcal{L}_{\mathrm{sim}}$$

其中 $\mathbf{M}$ 为前景掩码，$\mathbf{V}_t$ 为视频生成模型精炼后的目标视图，$\mathcal{L}_{\mathrm{p}}$ 为像素级损失（如 L1 和感知损失的组合）。关键在于**仿真一致性损失** $\mathcal{L}_{\mathrm{sim}}$，它惩罚高斯原语位置偏离其对应物理粒子的程度：

$$\mathcal{L}_{\mathrm{sim}} = \frac{1}{T \cdot J} \sum_{t=1}^{T} \sum_{j=1}^{J} \left\| p_{j,t} - \frac{1}{K} \sum_{k=1}^{K} \mu_{j,k,t} \right\|_2^2$$

该损失强制每个物理粒子 $p_j$ 的位置与其绑定的 $K$ 个高斯原语的平均位置保持一致。这是 VPP 双向桥梁的数学体现：优化后的高斯位置通过该损失反向更新物理粒子状态，形成闭环修正。

### 3.3 前向物理传递与闭环机制

模拟循环在长度为 $T$ 的时间窗口内运行，包含三个关键阶段：前向物理传递、反向神经优化和闭环闭合。

**前向物理传递**：给定当前场景状态 $\hat{S}_t$ 和用户动作 $\mathcal{A}_t$，通过物理求解器 $\Phi_p$ 生成粗动力学：

$$\hat{S}_{t+1} = \Phi_p(\hat{S}_t, \mathcal{A}_t)$$

物理求解器处理重力、风力等全局力场以及 3D 点力，生成物理粒子在时间窗口内的运动轨迹。由于 VPP 的绑定关系，高斯原语随物理粒子同步运动，产生初始的视觉渲染。

**闭环闭合**：反向优化完成后，利用优化后的高斯位置更新物理粒子状态，并将时间窗口末端的精炼状态 $\boldsymbol{S}_T$ 作为下一轮动作的初始状态 $\boldsymbol{S}_0$。这一闭环设计使得误差不会在长时域交互中累积，是实现多轮连续动作下一致 4D 场景生成的关键机制。

> **注意**：关于 3D 场景初始化模块（利用 GEN3C 合成稠密视图、COLMAP 重建点云、3DGS 优化）的具体实现细节，请参见方法章节的其他部分。

![[assets/figures/papers/paper_list_l2564_https_arxiv_org_abs_2602_04876/figures/009_Figure_6.jpg]]
*Figure 6: Ablation on VPP representation. Top row is with our proposed VPP for the foreground. Bottom row shows using 3D gaussians from the standard Gaussian Splatting [18] optimization*

![[assets/figures/papers/paper_list_l2564_https_arxiv_org_abs_2602_04876/figures/008_Figure_7.jpg]]
*Figure 7: Ablation on progressive multi-view optimization. Top row shows the optimized scene using progressive optimization and the bottom row shows direct optimization results*

## 实验与关键发现

### 主实验结果

PerpetualWonder在定量基准和人类偏好研究上均展现出对先前方法的显著优势。在World-Score指标上，方法在10个场景的测试中取得了相机可控性93.26、3D一致性80.41和成像质量66.98的最佳性能（Table 1）。这三项指标分别衡量了生成视频对指定相机轨迹的遵循程度、跨视角几何外观的稳定性以及整体视觉质量，表明闭环优化框架在多视角一致性生成上的有效性。

在包含350名参与者的2AFC用户研究中，PerpetualWonder在动态真实感的两个关键维度上大幅超越混合生成模拟器**WonderPlay**：物理合理性偏好率达到80.8%，运动保真度偏好率达到86.3%（Table 2）。这一结果直接验证了视觉-物理对齐粒子（VPP）表示在消除物理-视觉解耦带来的动力学误差累积方面的核心作用——当物理粒子与高斯原语建立双向连接后，前向物理驱动与反向视觉优化形成闭环，使得长时域交互中的物理状态持续得到视觉信号的校正。

定性对比（Figure 4）进一步展示了方法在相机运动与场景动力学协同生成上的优势。相比于GEN3C和Open-Sora等仅依赖视频生成模型的方法，PerpetualWonder生成的场景在物体运动轨迹的物理合理性和跨视角外观一致性上均表现出明显提升。在长时域多轮交互场景中（Figure 5），WonderPlay随着动作轮次增加出现物体分裂和纹理退化，而PerpetualWonder通过每轮闭环的状态校正保持了场景表示的稳定性。

![[assets/figures/papers/paper_list_l2564_https_arxiv_org_abs_2602_04876/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparisons between PerpetualWonder (ours) and the baseline methods. The top row shows the input images, actions, camera trajectories, and the texts describing the actions for conditional video generators [34, 40]. For ease of comparison, only one time window is shown. The images from left to right illustrate the resulting scene dynamics and camera motion for each method*

![[assets/figures/papers/paper_list_l2564_https_arxiv_org_abs_2602_04876/figures/007_Figure_5.jpg]]
*Figure 5: Long-horizon actions comparison between PerpetualWonder (top row) and WonderPlay (bottom row). For each method, the view changes across time, illustrating the four-round interaction results on a castle scene. The applied actions are overlaid on the top row*

### 消融实验

消融实验验证了VPP表示和渐进多视角优化两个核心设计选择的必要性。

**VPP表示的消融**（Figure 6）显示，当移除VPP、改用标准3D高斯优化表示前景时，视觉原语在优化过程中会自由漂移，导致动力学特征断裂、物体分裂和严重视觉伪影。这是因为标准3D高斯优化缺乏物理粒子的锚定约束，无法在反向优化中保持视觉表示与物理状态的对应关系。VPP通过将每个高斯原语的位置限定在对应物理粒子的尺寸δ范围内（Equation 1），并施加仿真一致性损失（Equation 4）惩罚位置偏离，确保了双向桥梁的稳定性。

**渐进多视角优化的消融**（Figure 7）对比了直接使用多视角精炼视频进行优化与渐进策略的效果。直接优化导致纹理模糊、外观闪烁和场景表示损坏，而渐进策略——先对输入视角进行优化，再以低权重引入其他视角，最后联合优化——产生了多视角一致的结果。这一差异揭示了多视角视频精炼中不同视角质量不均的关键瓶颈：视频生成模型在输入视角附近的生成质量更高，直接联合优化会引入低质量视角的噪声，而渐进策略通过逐步引入约束平滑了优化景观。

在粒子半径的超参数分析中（Section G），方法在0.25δ至4δ范围内表现鲁棒。但过小的半径（≤0.01δ）会限制高斯原语的空间表达能力，导致视觉细节丢失；过大的半径（≥100δ）则弱化锚定约束，使优化趋于不稳定。这一发现为VPP的粒子尺寸选择提供了实用指导。

### 失败模式与局限性

方法存在两个已知失败模式。第一，当输入图像中未出现物体几何时（如从视野外进入场景的物体），方法无法完整生成该物体的几何结构，出现几何残缺（Figure S3）。这是因为3D场景初始化阶段依赖从输入图像合成的稠密视图，无法恢复未观测到的几何。第二，完整模拟循环的运行时开销较大：初始化约8分钟，前向物理传递不足1分钟，但反向优化需约7分钟，总计约16分钟（Table S2），远未达到实时交互的要求。这一开销主要源于反向优化中多视角视频精炼和场景表示迭代更新的计算需求。

### 物理参数配置

模拟的物理参数及默认值详见Table S1，包括时间窗口长度T、粒子尺寸δ、仿真一致性损失权重λ_sim等关键配置。所有实验均采用这些默认参数，除非在消融实验中单独调整。

![[assets/figures/papers/paper_list_l2564_https_arxiv_org_abs_2602_04876/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative results of the proposed PerpetualWonder. We show the long-horizon scenes with three consecutive actions. and indicate global force (gravity or wind force field), and 3D point force, respectively. The results are all rendered from novel views, demonstrating our method’s ability in long-horizon action-conditioned 4D scene generation*

## 定位与知识库关联

### 1. 与先前工作的关系

PerpetualWonder 的核心推进在于将**视觉生成**与**物理模拟**从“解耦拼接”升级为“双向闭环”。此前的混合生成模拟器（如 **WonderPlay**）虽然也结合了物理求解器与视频生成模型，但其物理粒子与高斯原语之间不存在显式绑定：视觉优化仅作用于渲染结果，无法反向修正物理状态。这导致动力学误差随时间累积，最终在长时域交互中出现物体分裂、外观闪烁等退化。PerpetualWonder 通过引入**视觉-物理对齐粒子（VPP）** 表示，将每个物理粒子锚定一组高斯原语，使前向物理驱动与后向模型优化形成闭环——优化后的高斯位置可平均回写物理粒子，为下一轮动作提供校正后的初始状态。这一“物理-视觉双向桥梁”是该工作相对于 WonderPlay 等解耦方案的决定性差异。

在视频生成基座方面，PerpetualWonder 继承了 **GEN3C** 等相机可控视频生成模型的能力，将其用于两个关键环节：（1）从单张输入图像合成稠密环绕视图以初始化 3D 场景；（2）在模拟循环中对粗渲染视频进行多视角精炼。但与直接使用视频生成模型进行条件生成（如 **Open-Sora** 等力/文本条件视频模型）不同，PerpetualWonder 将视频生成模型定位为“视觉精炼器”，而非端到端动态生成器——物理一致性由求解器保证，视觉质量由生成模型补充，两者通过 VPP 和仿真一致性损失 $\mathcal{L}_{\mathrm{sim}}$ 耦合。

### 2. 适用边界与局限

当前方法存在两个明确的适用边界：

**（1）实时交互不可行。** 完整的模拟循环包含三个阶段：3D 场景初始化（约 8 分钟）、前向物理传递（小于 1 分钟）和反向神经优化（约 7 分钟），总计约 16 分钟（Table S2）。反向优化是主要瓶颈，使得该方法目前无法支持实时或近实时的交互式场景生成。

**（2）未见几何无法补全。** 方法依赖输入图像中可见的物体几何来初始化前景表示。对于在交互过程中从视野外进入场景的物体（如从侧面推入的新物体），系统无法生成其完整的几何结构，仅能产生残缺表示（Figure S3）。这一限制源于初始化阶段对单张图像和合成环绕视图的强依赖，而非 VPP 表示本身的问题。

此外，VPP 表示中的粒子半径存在有效范围：在 $0.25\delta$ 至 $4\delta$ 之间结果鲁棒，但过小（$\leq 0.01\delta$）会导致表示能力不足，过大（$\geq 100\delta$）则引发优化不稳定（Section G, Supplementary）。这表明 VPP 的锚定机制需要在“表示灵活性”与“物理约束强度”之间取得平衡。

### 3. 开放问题

基于上述局限，该方向存在以下开放问题：

- **实时化路径：** 如何在不大幅牺牲生成质量的前提下，压缩反向优化开销？可能的思路包括轻量化视频精炼模型、稀疏视角优化策略，或将部分优化计算迁移到前向阶段。
- **未见几何生成：** 如何赋予系统在交互过程中“补全”新出现物体几何的能力？这可能需要引入生成式先验，在物理粒子层面支持动态增删粒子及其对应的高斯原语。
- **复杂交互泛化：** 当前验证集中在单一刚体物体的力场交互（重力、风力、点力）。对于多物体碰撞、非刚体变形、以及精细材料（如流体、布料）模拟，VPP 表示和闭环优化框架是否仍然足够，尚待检验。

## 原文 PDF

![[paperPDFs/CVPR_2026/PerpetualWonder_Long_horizon_Action_conditioned_4D_Scene_Generation.pdf]]
