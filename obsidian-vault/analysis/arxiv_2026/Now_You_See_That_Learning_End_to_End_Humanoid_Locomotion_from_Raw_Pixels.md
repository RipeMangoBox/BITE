---
title: "Now You See That: Learning End-to-End Humanoid Locomotion from Raw Pixels"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/Now_You_See_That_Learning_End_to_End_Humanoid_Locomotion_from_Raw_Pixels.pdf
project_link: https://octomap.github.io
code_link: https://github.com/Hellod035/Now\_You\_See\_That
aliases:
- EEVBHLO
- NYSTLEEHLFRP
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 高保真深度传感器仿真与全面增强
primary_logic: 通过综合立体深度增强、视觉感知蒸馏和地形特定多评论家强化学习，仿人机器人可以直接从原始深度图像学习鲁棒且通用的运动技能。
claims:
- 本文方法在RDT-Bench上实现平均98.9%成功率，仅5.8%功率衰减率，远超现有最佳方法（Humanoid Parkour 71.0%/30.9%）。
- 移除所有深度增强导致成功率骤降至43.0%，功率衰减率飙升至70.9%，证明感知噪声是核心瓶颈。
- 直接对深度图像进行RL训练而不蒸馏，功率衰减率最高（58.1%），表明两阶段训练对视觉控制至关重要。
- 多评论家和多鉴别器架构优于单一评论家/鉴别器，平均成功率提升17个百分点（从82.0%到98.9%）。
---

# Now You See That: Learning End-to-End Humanoid Locomotion from Raw Pixels

> [!tip] 核心洞察
> 通过综合立体深度增强、视觉感知蒸馏和地形特定多评论家强化学习，仿人机器人可以直接从原始深度图像学习鲁棒且通用的运动技能。

| 字段 | 内容 |
|------|------|
| 中文题名 | 眼见为实：从原始像素学习端到端仿人运动 |
| 英文题名 | Now You See That: Learning End-to-End Humanoid Locomotion from Raw Pixels |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2602.06382) · [Code](https://github.com/Hellod035/Now\_You\_See\_That) · [paper](https://arxiv.org/abs/2511.14625) · [Project](https://octomap.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | End-to-End Vision-Based Humanoid Locomotion (Ours) |
| Dataset | RDT-Bench |

> [!tip] 效果简介
> - RDT-Bench (Average) 上，成功率 (%) 98.9±0.4 vs 71.0 (Humanoid Parkour Learning) (+27.9%)；功率衰减率 (%) 5.8±0.3 vs 30.9 (Humanoid Parkour Learning) (-25.1%)。
> - RDT-Bench (Stairs Up) 上，成功率 (%) 99.2±0.3 vs 74.2±1.1 (Humanoid Parkour Learning) (+25.0%)。
> - RDT-Bench (Gaps) 上，成功率 (%) 99.3±0.2 vs 72.8±1.0 (Humanoid Parkour Learning) (+26.5%)。

## 概要

本文致力于解决仿人机器人在复杂地形上仅凭原始深度图像实现端到端运动控制的难题。现有视觉运动方法面临两大瓶颈：**仿真到现实的深度感知噪声**导致细粒度运动任务（如爬楼梯、跨越间隙）性能急剧下降；以及**跨异构地形的统一策略训练**存在目标冲突，单一评论家难以同时优化楼梯、平台、粗糙地面和间隙等不同运动模式。

针对上述瓶颈，本文提出了一套两阶段训练框架。其核心在于三个关键设计：**高保真深度传感器仿真**——通过综合立体融合、距离相关噪声、柏林噪声、光学畸变等八项增强操作，在训练中充分暴露策略于真实传感器噪声模式；**地形特定多评论家与多鉴别器架构**——为不同地形类别分配专用价值网络和对抗运动先验，解决统一策略的优化冲突；**视觉感知行为蒸馏**——将依赖特权高度扫描的教师策略迁移至仅使用深度图像的学生策略，并通过降噪辅助任务和KL正则化确保特征鲁棒性。

在统一的RDT-Bench基准上，本文方法实现了**平均98.9%的成功率**和仅**5.8%的功率衰减率**，大幅超越现有最佳方法Humanoid Parkour Learning（71.0%成功率，30.9%功率衰减率）。消融实验进一步揭示了各组件的关键贡献：移除所有深度增强导致成功率骤降至43.0%、功率衰减率飙升至70.9%，证实感知噪声是核心瓶颈；而多评论家架构相比单评论家提升成功率17个百分点，蒸馏损失中的降噪与KL正则化相比纯行为克隆提升12.9个百分点。

仿人机器人要实现真正的自主部署，必须具备在复杂非结构化地形中仅凭机载视觉传感器进行鲁棒运动的能力。与四足机器人相比，仿人机器人因更高的质心、更小的支撑多边形和更严格的足部放置约束，对地形感知的精度和鲁棒性提出了更苛刻的要求。然而，当前绝大多数仿人运动学习方法仍然依赖特权高度扫描（height scan）或外部运动捕捉系统，无法在真实世界中仅凭视觉独立运行。

### 现有视觉仿人运动方法的缺口

已有的视觉仿人运动工作虽尝试引入深度相机，但在感知噪声建模、地形泛化能力和细粒度运动精度三个维度上存在显著不足。**Humanoid Parkour Learning**（Zhuang et al., CoRL 2024）作为当前最佳方法，在RDT-Bench上的平均成功率仅为71.0%，功率衰减率高达30.9%（TABLE IV），表明其策略在面对真实深度噪声时性能急剧退化。更广泛地，现有方法存在以下共性缺口（TABLE I）：

1. **深度传感器仿真不充分**：多数工作仅使用简单的域随机化（如高斯噪声、随机掩码），未能复现真实立体相机的系统性缺陷——包括立体匹配失败产生的空洞、距离相关的噪声增长、镜头光学畸变和标定不确定性。这导致仿真中训练的策略在接触真实深度图像时出现严重分布偏移。

2. **跨地形目标冲突**：仿人运动需要在楼梯、间隙、平台、粗糙地形等截然不同的地形上执行精细的足部放置。单一评论家和单一鉴别器架构无法有效处理这些地形间的目标冲突——例如，楼梯要求精确的垂直足部抬起，而间隙要求水平方向的速度优先。这种冲突导致策略在特定地形上妥协，整体性能受限。

3. **视觉策略迁移脆弱**：直接从深度图像进行强化学习训练或采用标准行为克隆，均无法保证部署策略对感知噪声的鲁棒性。直接RL训练因感知与控制的联合优化困难，功率衰减率可达58.1%（TABLE IV）；纯行为克隆则缺乏对编码器表征的噪声不变性约束，成功率仅为86.0%。

### 核心瓶颈与本文动机

上述缺口的本质可归结为一个核心瓶颈：**仿真到现实的深度感知噪声导致细粒度运动任务性能下降，且跨异构地形的统一策略训练存在目标冲突**。具体而言，当深度图像中的噪声模式与训练分布不一致时，策略的足部放置决策出现系统性偏差，在楼梯和间隙等需要厘米级精度的任务上尤为致命。消融实验证实，完全移除深度增强后成功率骤降至43.0%，功率衰减率飙升至70.9%（TABLE IV），直接验证了感知噪声是性能退化的首要因素。

本文的动机在于：**通过综合立体深度增强、视觉感知蒸馏和地形特定多评论家强化学习，使仿人机器人可以直接从原始深度图像学习鲁棒且通用的运动技能**。这一思路的核心假设是，若能高保真地仿真真实深度传感器的噪声特性，并通过专门设计的蒸馏损失将噪声不变性注入视觉编码器，则策略可以在不依赖任何真实世界微调的情况下实现从仿真到现实的零样本迁移。

## 核心方法与创新机理

本文提出了一套端到端从原始深度图像学习仿人机器人运动的完整框架，其核心创新围绕**仿真到现实（Sim-to-Real）深度感知噪声**这一瓶颈展开，通过三个紧密耦合的“变更槽”（changed slots）实现突破。

### 创新一：高保真立体深度增强管道

现有方法（如 **Humanoid Parkour Learning** (Zhuang et al., CoRL 2024)）通常采用标准域随机化（高斯噪声、随机掩码）处理深度图像，难以复现真实立体相机的复杂失效模式。本文提出了一套包含8个操作的**综合深度模拟管道**（Section III-A, TABLE II, Fig. 3），从根本上弥补了这一差距：

1.  **立体深度融合与一致性检查**：模拟双目匹配中的遮挡空洞。通过视差对应公式 $u_r = u - \frac{f_x b}{d_{\mathrm{left}}(u,v) + \epsilon}$ 计算右图对应像素，再经一致性检查 $d_{\mathrm{fused}}(u,v) = \begin{cases} d_{\mathrm{left}}(u,v) & \text{if } |d_{\mathrm{left}} - d_{\mathrm{right}}(u_r,v)| < \tau \cdot d_{\mathrm{left}} \\ 0 & \text{otherwise} \end{cases}$ 将无效像素标记为0，逼真再现纹理缺失和遮挡导致的深度空洞。
2.  **距离相关噪声**：依据深度值添加二次方缩放的高斯噪声 $\widetilde{d}(u,v) = d(u,v) + \mathcal{N}(0, \sigma^2(d)), \sigma(d) = |c_0 + c_1 d + c_2 d^2|$，模拟真实传感器随距离增加而恶化的信噪比。
3.  **结构化柏林噪声**：通过多倍频叠加 $n_{\mathrm{perlin}}(u,v) = \sum_{o=0}^{4} 0.5^o \cdot \mathcal{P}(2^o u, 2^o v)$ 生成空间相关的噪声模式，复现传感器制造工艺引入的固定模式噪声。
4.  **光学畸变与标定不确定性**：采用随机卷积 $\tilde{d} = d * (W + I)$（$W$ 为 $3\times3$ 核，参数采样自 $U(-0.05, 0.05)$）模拟镜头畸变，并结合尺度随机化、像素失效（零值/最大值）和深度裁剪等操作，覆盖标定误差与传感器故障。

**因果作用**：该管道直接作用于“仿真深度图像→真实深度图像”的分布偏移，是后续策略蒸馏成功的前提。消融实验（TABLE IV）表明，完全移除增强导致成功率从98.9%骤降至43.0%，功率衰减率飙升至70.9%，证实感知噪声是核心瓶颈；移除立体融合或柏林噪声等单个组件均导致性能显著恶化（TABLE V）。

### 创新二：地形特定的多评论家与多鉴别器架构

传统强化学习使用单一评论家（critic）和鉴别器（discriminator）处理所有地形，忽略了不同地形类别（楼梯/平台、间隙、粗糙地形）在运动模式和奖励需求上的根本差异，导致训练中的目标冲突。本文提出**地形特定多评论家与多鉴别器**架构（Section III-B, Fig. 4）：

*   **多评论家**：根据地形类别 $k(s_t)$ 动态选择对应的价值网络 $V(s_t) = V_{k(s_t)}(s_t)$，使每个地形类别拥有专用的价值估计，避免跨地形梯度冲突。
*   **多鉴别器**：对抗运动先验（AMP）的鉴别器同样按地形分类 $D(s_t) = D_{k(s_t)}(s_t)$，使风格奖励适应不同地形的运动特征（如楼梯的抬腿模式 vs. 间隙的跳跃模式）。
*   **地形特定奖励函数**：为不同地形设计差异化的速度跟踪奖励——楼梯/平台/粗糙地形采用指数速度跟踪 $r_{\mathrm{vel}}^{\mathrm{exp}} = \exp\left(-\frac{\|\mathbf{v}_{xy}^{\mathrm{cmd}} - \mathbf{v}_{xy}^{\mathrm{robot}}\|^2}{\sigma^2}\right)$ 强调精确跟随；间隙地形采用方向速度跟踪 $r_{\mathrm{vel}}^{\mathrm{dir}} = \frac{\min\left(\mathbf{v}_{xy}^{\mathrm{robot}} \cdot \hat{\mathbf{d}}_{\mathrm{cmd}}, \|\mathbf{v}_{xy}^{\mathrm{cmd}}\|\right)}{\|\mathbf{v}_{xy}^{\mathrm{cmd}}\| + \epsilon}$ 鼓励沿命令方向移动而不惩罚超速。同时引入足部接触高度奖励 $r_{\mathrm{contact}} = \sum_{f} \mathbf{1}_{\mathrm{contact}}^f \cdot \mathrm{std}\left(\mathrm{clip}(h_f^{\mathrm{scan}}, -h_{\mathrm{max}}, h_{\mathrm{max}})\right)$ 惩罚落足点不平整。

**因果作用**：该架构解决了异构地形统一策略训练中的目标冲突。消融实验（TABLE VI）显示，采用单评论家/鉴别器使平均成功率从98.9%降至82.0%，楼梯场景成功率下降14.9个百分点，功率衰减率升高13.5个百分点，证明地形特定架构是实现通用运动技能的关键。

### 创新三：带去噪与KL正则化的视觉感知蒸馏

从特权高度扫描到深度图像的策略迁移面临两个挑战：(1) 深度噪声导致编码器表征不稳定；(2) 标准行为克隆缺乏对表征空间的约束。本文提出**视觉感知行为蒸馏**（Section III-C, Eq. 8-12），在行为克隆基础上引入两个辅助目标：

*   **降噪目标** $\mathcal{L}_{\mathrm{denoise}} = \mathbb{E}_{d, \tilde{d}}\left[\left\|E(d) - E(\tilde{d})\right\|_2^2\right]$：强制干净深度图像与增强深度图像在编码器潜在空间中保持一致，使学生策略对传感器噪声不敏感。
*   **KL正则化** $\mathcal{L}_{\mathrm{kl}} = \mathrm{KL}\big(\mathcal{N}(\pmb{\mu}, \mathrm{diag}(\pmb{\sigma}^2)) \big|\big| \mathcal{N}(\mathbf{0}, \mathbf{I})\big)$：将编码器输出的经验分布（$\mu_j = \frac{1}{N}\sum z_{i,j}, \sigma_j^2 = \frac{1}{N}\sum (z_{i,j} - \mu_j)^2 + \epsilon$）约束到标准正态先验，防止表征空间坍塌并提升泛化能力。
*   **总蒸馏损失** $\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{behavior}} + \lambda_{\mathrm{denoise}}\mathcal{L}_{\mathrm{denoise}} + \lambda_{\mathrm{kl}}\mathcal{L}_{\mathrm{kl}}$ 将三者加权组合。

**因果作用**：该蒸馏策略直接决定了视觉控制的鲁棒性。消融实验（TABLE VII）表明，仅使用行为克隆（BC Only）使平均功率衰减率从5.8%升至17.7%，成功率从98.9%降至86.0%；直接对深度图像进行RL训练而不蒸馏（Direct RL）的功率衰减率最高（58.1%），证明两阶段训练与辅助损失对视觉策略的鲁棒性至关重要。

### 创新协同效应

三个创新的协同关系体现在：**深度增强管道**为蒸馏提供了逼真的噪声分布，使降噪目标能够学习有效的噪声不变表征；**多评论家架构**为教师策略提供了高质量的运动先验，确保蒸馏目标的可靠性；**视觉感知蒸馏**则将这些先验稳健地迁移到仅依赖深度图像的部署策略。三者共同作用，使最终策略在RDT-Bench上实现98.9%平均成功率、5.8%功率衰减率，远超现有最佳方法 **Humanoid Parkour Learning** 的71.0%成功率和30.9%功率衰减率（TABLE IV）。

本文提出一个两阶段训练框架，使仿人机器人能够直接从原始深度图像学习跨异构地形的端到端运动技能。框架的核心设计逻辑围绕一个瓶颈展开：**仿真到现实的深度感知噪声**会严重破坏细粒度运动控制（如精确落足、楼梯踏步），而单一策略在跨地形训练时面临目标冲突。为解决这一问题，框架通过三条因果链路协同工作：（1）高保真深度传感器仿真弥合感知差距；（2）地形特定的多评论家/多鉴别器架构缓解任务冲突；（3）带去噪和KL正则化的视觉感知蒸馏实现鲁棒的策略迁移。

### 两阶段训练流程

框架分为两个阶段，如 **Figure 4** 所示：

![[assets/figures/papers/paper_list_l59_https_arxiv_org_abs_2602_06382/figures/007_Figure_4.jpg]]
*Figure 4: Method Overview. Our framework consists of two stages: (1) Privileged RL Training: A teacher policy is trained with height scan observations using multi-critic and multi-discriminator learning, where terrain-specific reward shaping and dedicated value networks handle diverse terrain categories (stairs/platforms, gaps, rough terrain). (2) Vision-Aware Distillation: The privileged policy is distilled into a deployment policy operating on augmented depth images, combining behavior cloning with denoising objectives for robust sim-to-real transfer*

**第一阶段：特权强化学习（教师策略）**。教师策略使用高精度的**高度扫描**（height scan）作为感知输入，这是一种在仿真中可获取但真实机器人难以直接获得的特权信息。教师策略采用地形特定的多评论家和多鉴别器架构，结合针对不同地形类别（楼梯/平台、间隙、粗糙地形）定制的奖励函数进行训练。具体而言，评论家和鉴别器的选择由当前地形类别 $k(s_t)$ 决定：

$$V(s_t) = V_{k(s_t)}(s_t), \quad D(s_t) = D_{k(s_t)}(s_t)$$

这一设计使每个地形类别拥有专用的价值网络和对抗运动先验鉴别器，避免了单一评论家在跨地形训练中的目标冲突。教师策略的输出是一个通用的运动先验，涵盖步态模式、足部放置策略和身体姿态控制。

**第二阶段：视觉感知行为蒸馏（学生策略）**。学生策略仅使用经过综合增强的深度图像作为输入，通过蒸馏从教师策略迁移运动技能。蒸馏损失由三个组分构成：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{behavior}} + \lambda_{\mathrm{denoise}}\mathcal{L}_{\mathrm{denoise}} + \lambda_{\mathrm{kl}}\mathcal{L}_{\mathrm{kl}}$$

其中，$\mathcal{L}_{\mathrm{behavior}}$ 是标准的行为克隆损失，最小化学生与教师策略的动作差异；$\mathcal{L}_{\mathrm{denoise}}$ 强制干净深度图像和增强深度图像在编码器潜在空间中的表征一致性；$\mathcal{L}_{\mathrm{kl}}$ 则将编码器输出的潜在分布正则化至标准正态先验，防止过拟合于增强噪声的特定模式。消融实验表明，移除降噪和KL正则化后，平均成功率从98.9%降至86.0%，功率衰减率从5.8%升至17.7%，证明这两个辅助目标对鲁棒性至关重要。

### 深度增强管道

深度增强管道是弥合仿真与现实感知差距的核心模块，如 **Figure 3** 所示，从干净的左右深度图像出发，依次施加8个操作：

1. **立体深度融合**：通过视差对应公式 $u_r = u - \frac{f_x b}{d_{\mathrm{left}}(u,v) + \epsilon}$ 计算右侧图像对应像素，然后进行一致性检查，将不一致像素标记为无效（空洞），模拟真实双目匹配中的遮挡和纹理缺失效应。
2. **随机卷积光学畸变**：使用3×3随机核与恒等核相加进行卷积 $\tilde{d} = d * (W + I)$，模拟镜头畸变。
3. **距离相关高斯噪声**：噪声标准差随距离二次方缩放 $\sigma(d) = |c_0 + c_1 d + c_2 d^2|$，模拟真实深度传感器在远距离处精度下降的特性。
4. **多倍频柏林噪声**：$n_{\mathrm{perlin}}(u,v) = \sum_{o=0}^{4} 0.5^o \cdot \mathcal{P}(2^o u, 2^o v)$，生成结构化噪声模式，模拟传感器像素串扰和固定模式噪声。
5. **尺度随机化**、**零像素失效**、**最大像素失效**：模拟传感器标定误差和局部失效。
6. **深度裁剪与空间裁剪**：将深度值限制在有效范围并裁剪至策略输入尺寸。

消融实验（**TABLE V**）表明，移除任一增强组件均导致性能显著下降。特别地，移除立体融合操作使成功率下降约8.5个百分点，功率衰减率升高约11.7个百分点，验证了模拟双目匹配缺陷对策略鲁棒性的关键作用。

### 输入输出流

整个系统的输入输出流可概括为：

- **教师策略输入**：高度扫描（仿真特权信息）、本体感知状态（关节位置/速度、躯干姿态/速度、重力方向）、速度指令、地形类别标签。
- **教师策略输出**：关节位置目标。
- **学生策略输入**：增强后的深度图像（单通道，经空间裁剪）、本体感知状态、速度指令。
- **学生策略输出**：关节位置目标，与教师策略同维。

在真实部署时，仅运行学生策略，深度图像由机器人搭载的立体相机实时获取。框架在RDT-Bench上实现了平均98.9%的成功率和仅5.8%的功率衰减率，远超现有最佳方法**Humanoid Parkour Learning**（Zhuang et al., CoRL 2024）的71.0%成功率和30.9%功率衰减率。

![[assets/figures/papers/paper_list_l59_https_arxiv_org_abs_2602_06382/figures/001_Figure_1.jpg]]
*Figure 1: Overview. Our end-to-end vision-based humanoid locomotion policy enables robust traversal across diverse challenging terrains, including high stones, long staircases (both ascending and descending), debris fields, gaps with varying heights, trolleys, high platforms, grid holes, and platform-slope-gap combinations. All behaviors emerge from a single unified policy trained with raw depth images*

本文方法采用两阶段训练框架：第一阶段在仿真中利用高度扫描（height scan）作为特权观测，训练教师策略；第二阶段通过视觉感知行为蒸馏，将教师策略迁移至仅依赖深度图像的学生策略，实现端到端的像素到动作控制。整个框架由三个核心模块构成：高保真深度传感器仿真、特权强化学习、视觉感知行为蒸馏。

### 高保真深度传感器仿真

该模块通过8个顺序操作，将仿真中干净的双目深度图像转化为接近真实传感器输出的带噪深度图，弥合仿真与现实之间的感知差距。

**立体深度融合** 首先模拟双目匹配中的空洞效应。给定左视图深度 $d_{\mathrm{left}}(u,v)$，右视图对应像素坐标为：

$$u_r = u - \frac{f_x b}{d_{\mathrm{left}}(u,v) + \epsilon}$$

其中 $f_x$ 为焦距，$b$ 为基线长度，$\epsilon$ 防止除零。立体一致性检查将不一致像素标记为无效：

$$d_{\mathrm{fused}}(u,v) = \begin{cases} d_{\mathrm{left}}(u,v) & \text{if } |d_{\mathrm{left}} - d_{\mathrm{right}}(u_r,v)| < \tau \cdot d_{\mathrm{left}} \\ 0 & \text{otherwise} \end{cases}$$

这复现了遮挡和弱纹理区域产生的空洞模式。

**距离相关噪声** 根据像素深度值施加二次方缩放的高斯噪声，模拟远距离测量精度下降：

$$\widetilde{d}(u,v) = d(u,v) + \mathcal{N}(0, \sigma^2(d)), \quad \sigma(d) = |c_0 + c_1 d + c_2 d^2|$$

**多倍频柏林噪声** 生成结构化传感器噪声，模拟真实深度传感器的空间相关噪声模式：

$$n_{\mathrm{perlin}}(u,v) = \sum_{o=0}^{4} 0.5^o \cdot \mathcal{P}(2^o u, 2^o v)$$

**光学畸变** 通过随机卷积模拟镜头畸变：

$$\tilde{d} = d * (W + I)$$

其中 $W \in \mathbb{R}^{3\times3}$ 的元素从 $\mathcal{U}(-0.05, 0.05)$ 采样，$I$ 为单位核，保证畸变以原始图像为中心。

后续操作还包括尺度随机化、零像素失效、最大值像素失效、深度裁剪和空间裁剪，共同构成完整的增强管道。

### 特权强化学习

教师策略利用高度扫描作为特权观测，结合地形特定的多评论家和多鉴别器架构进行训练。根据当前地形类别 $k(s_t) \in \{1, 2, 3\}$ 选择对应的价值网络和鉴别器：

$$V(s_t) = V_{k(s_t)}(s_t), \quad D(s_t) = D_{k(s_t)}(s_t)$$

对抗运动先验（AMP）鉴别器的观测向量以躯干为中心：

$$\Phi_{\mathrm{amp}} = [\mathbf{q}_{\mathrm{rel}}, \dot{\mathbf{q}}_{\mathrm{rel}}, \mathbf{v}_{\mathrm{torso}}^{b}, \omega_{\mathrm{torso}}^{b}, \mathbf{g}^{b}, \mathbf{p}_{\mathrm{body}}^{b}, \mathbf{q}_{\mathrm{body}}^{b}]$$

奖励函数针对不同地形定制。对于楼梯、平台和粗糙地形，采用指数速度跟踪奖励：

$$r_{\mathrm{vel}}^{\mathrm{exp}} = \exp\left(-\frac{\|\mathbf{v}_{xy}^{\mathrm{cmd}} - \mathbf{v}_{xy}^{\mathrm{robot}}\|^2}{\sigma^2}\right)$$

对于间隙地形，采用方向速度跟踪奖励，鼓励沿命令方向移动而不惩罚超速：

$$r_{\mathrm{vel}}^{\mathrm{dir}} = \frac{\min\left(\mathbf{v}_{xy}^{\mathrm{robot}} \cdot \hat{\mathbf{d}}_{\mathrm{cmd}}, \|\mathbf{v}_{xy}^{\mathrm{cmd}}\|\right)}{\|\mathbf{v}_{xy}^{\mathrm{cmd}}\| + \epsilon}$$

足部接触高度奖励惩罚落足点不平整：

$$r_{\mathrm{contact}} = \sum_{f \in \{\mathrm{left, right}\}} \mathbf{1}_{\mathrm{contact}}^f \cdot \mathrm{std}\left(\mathrm{clip}(h_f^{\mathrm{scan}}, -h_{\mathrm{max}}, h_{\mathrm{max}})\right)$$

### 视觉感知行为蒸馏

学生策略仅接收增强后的深度图像，通过复合损失函数从教师策略迁移知识。

**行为克隆损失** 最小化部署策略与特权策略的动作差异：

$$\mathcal{L}_{\mathrm{behavior}} = \mathbb{E}_{s_t}\left[\left\|\mu_{\mathrm{deploy}}(s_t) - \mu_{\mathrm{priv}}(s_t)\right\|_2^2\right]$$

**降噪目标** 强制干净深度图像和增强深度图像的表征一致性：

$$\mathcal{L}_{\mathrm{denoise}} = \mathbb{E}_{d, \tilde{d}}\left[\left\|E(d) - E(\tilde{d})\right\|_2^2\right]$$

**KL正则化** 约束编码器输出的潜在分布接近标准正态先验。首先估计对角高斯分布的参数：

$$\mu_j = \frac{1}{N}\sum_{i=1}^{N} z_{i,j}, \quad \sigma_j^2 = \frac{1}{N}\sum_{i=1}^{N} (z_{i,j} - \mu_j)^2 + \epsilon$$

然后最小化与标准正态先验的KL散度：

$$\mathcal{L}_{\mathrm{kl}} = \mathrm{KL}\big(\mathcal{N}(\pmb{\mu}, \mathrm{diag}(\pmb{\sigma}^2)) \big|\big| \mathcal{N}(\mathbf{0}, \mathbf{I})\big)$$

**总蒸馏损失** 为上述三个损失项的加权和：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{behavior}} + \lambda_{\mathrm{denoise}}\mathcal{L}_{\mathrm{denoise}} + \lambda_{\mathrm{kl}}\mathcal{L}_{\mathrm{kl}}$$

消融实验表明，纯行为克隆（BC Only）的平均功率衰减率从5.8%升至17.7%，验证了降噪和KL正则化对鲁棒性的关键贡献。

![[assets/figures/papers/paper_list_l59_https_arxiv_org_abs_2602_06382/figures/005_Figure_3.jpg]]
*Figure 3: Visualization of the depth augmentation pipeline. Starting from clean left and right depth images, the pipeline sequentially applies: (1) stereo fusion, (2) random convolution, (3) Gaussian noise, (4) Perlin noise, (5) scale randomization, (6) zero pixel failures, (7) max pixel failures, (8) depth clipping and spatial cropping to produce realistic depth observations for sim-to-real transfer*

## 实验与关键发现

### 核心瓶颈与因果机制

本文的核心发现是：**仿真到现实的深度感知噪声是制约细粒度仿人运动任务性能的关键瓶颈**，而跨异构地形的统一策略训练存在严重的目标冲突。这一瓶颈的因果链条如下：真实立体相机受遮挡、纹理缺失、光学畸变和标定误差影响，产生大量空洞和噪声，导致仿真中训练的策略在现实场景中无法准确感知地形几何，进而引发步态错乱、足部打滑和关节过载。为验证这一因果机制，作者设计了消融实验：当完全移除深度增强（No Augmentation）时，平均成功率从98.9%骤降至43.0%，功率衰减率从5.8%飙升至70.9%（TABLE IV）。这直接证明了感知噪声是导致性能崩溃的主导因素，而非动力学差异或控制架构问题。

### 主实验结果

在统一的RDT-Bench基准上，本文方法与现有最佳方法**Humanoid Parkour Learning**（Zhuang et al., CoRL 2024）及多个消融基线进行了系统对比。所有方法均在CycleGAN注入的真实深度噪声下评估，确保对比的公平性。

**TABLE IV** 展示了核心结果。本文方法在四种地形配置上均取得最优表现：
- **平均成功率**：98.9% ± 0.4%，较Humanoid Parkour Learning（71.0%）提升27.9个百分点；
- **平均功率衰减率（PDR）**：5.8% ± 0.3%，远低于Humanoid Parkour Learning的30.9%，表明策略在噪声下保持高效能量利用；
- **楼梯上坡**：成功率99.2% ± 0.3%，对比基线74.2% ± 1.1%；
- **间隙跨越**：成功率99.3% ± 0.2%，对比基线72.8% ± 1.0%。

值得注意的是，下楼梯场景是所有方法中表现最弱的环节，本文方法成功率为98.6% ± 0.4%，但仍显著领先。这一相对劣势源于面向下的视角导致目标落足点被遮挡，以及重力放大效应加剧了控制误差。实际部署结果（TABLE VIII）进一步验证了仿真到现实的迁移能力：上楼梯15次试验全成功（100%），下楼梯13/15成功（86.7%），与仿真趋势一致。

### 消融实验：深度增强组件

**TABLE V** 系统消融了深度增强管道的各组件。完整管道包含立体融合、随机卷积、高斯噪声、柏林噪声、尺度随机化、零像素失效、最大像素失效、深度裁剪和空间裁剪共8个操作。逐一移除各组件的实验表明：

- **移除立体融合**导致成功率下降8.5个百分点，功率衰减率升高11.7个百分点。立体融合模拟了双目匹配失败产生的空洞模式，是弥合仿真与现实深度分布差距的关键操作。
- **移除高斯噪声**和**柏林噪声**均导致显著性能退化，表明距离相关噪声和结构化传感器噪声的联合建模不可或缺。
- **部分增强（Partial Augmentation）** 仅保留部分操作，平均成功率降至78.3%，PDR升至30.2%，远不如完整管道。

这些结果共同说明：逼真的深度感知需要多维度噪声的复合建模，任何单一增强组件的缺失都会在现实噪声下暴露脆弱性。

### 消融实验：多评论家/鉴别器架构

**TABLE VI** 对比了多评论家/多鉴别器架构与单一评论家/鉴别器架构。多评论家架构的核心思想是：为楼梯/平台、间隙、粗糙地形三类地形分别训练专用的价值网络和鉴别器，以缓解跨地形目标冲突。

- **单评论家/鉴别器**的平均成功率仅为82.0%，较完整方法下降16.9个百分点；功率衰减率升至20.8%，恶化15.0个百分点。
- 在楼梯场景上，单评论家架构的成功率下降14.9个百分点，PDR升高13.5个百分点，表明楼梯的精确足部放置与其他地形的速度跟踪之间存在显著冲突，地形特定的价值估计有效解耦了这些冲突。

### 消融实验：蒸馏损失组件

**TABLE VII** 消融了视觉感知蒸馏损失的三个组分：行为克隆（BC）、降噪目标（Denoise）和KL正则化。

- **仅行为克隆（BC Only）**：平均成功率降至86.0%，PDR升至17.7%。这表明单纯模仿教师策略的动作分布不足以应对感知噪声，学生策略在噪声下会产生累积偏差。
- **加入降噪目标**：通过强制干净深度图像和增强深度图像的表征一致性，显著提升了鲁棒性。
- **加入KL正则化**：通过约束编码器输出的潜在分布接近标准正态先验，进一步改善了泛化能力。

三者联合使PDR从17.7%降至5.8%，证明蒸馏损失的每个组分都对噪声鲁棒性有独立且互补的贡献。

### 直接RL训练的失败模式

**TABLE IV** 中Direct RL基线（直接在增强深度图像上进行RL训练，无教师蒸馏）的结果揭示了端到端视觉RL的关键困难：平均成功率仅74.2%，PDR高达58.1%，是所有基线中功率衰减最严重的。这说明即使有了高保真深度增强，直接从高维像素输入学习运动控制仍面临严重的样本效率瓶颈和表征学习困难。两阶段的教师-学生蒸馏框架通过特权高度扫描提供密集的监督信号，有效规避了这一困难。

### 潜在空间可视化

**Figure 6** 的t-SNE可视化展示了深度编码器在六种地形类型上的潜在表征分布。各地形形成清晰分离的聚类，表明即使在真实传感器噪声下，编码器仍能学习到地形特定的判别性表征。这一结构化表征是多评论家架构和地形特定奖励函数能够有效运作的基础。

### 跨平台泛化

**TABLE XVI** 和 **Figure 7** 展示了策略在Unitree G1平台上的零样本迁移能力。尽管训练平台与G1在运动学和深度传感器配置上存在差异，策略仍能成功完成户外楼梯上坡任务。这得益于深度增强管道模拟了通用立体相机的噪声特性，而非特定传感器的特性，使得学到的深度表征具有跨平台泛化性。但需注意，跨平台验证仅限于上楼梯场景，在间隙、平台和下楼梯等更复杂地形上的泛化能力尚未验证。

### 限制与失败模式

1. **下楼梯鲁棒性不足**：下楼梯是唯一在实际部署中出现失败案例的场景（86.7%成功率）。面向下的视角导致目标落足点被遮挡，且重力放大效应使控制误差的后果更严重。当前方法缺乏预测性足部放置机制，完全依赖反应式控制。
2. **增强参数覆盖范围有限**：深度增强管道的噪声参数基于启发式设置，可能未完全涵盖某些极端传感器变体（如强光过曝、镜面反射导致的系统性空洞）。
3. **单仿真器评估**：尽管采用CycleGAN注入真实噪声，所有评估仍在单一仿真器内进行，缺乏在不同物理引擎间的泛化验证。
4. **地形类别扩展性**：多评论家架构需要为每类地形训练专用网络，当地形类别大幅增加时，训练成本将线性增长。

![[assets/figures/papers/paper_list_l59_https_arxiv_org_abs_2602_06382/figures/012_Figure_6.jpg]]
*Figure 6: t-SNE visualization of the depth encoder’s latent space across six terrain types. Each terrain forms a distinct cluster, demonstrating effective terrain-specific representation learning despite realistic sensor noise*

![[assets/figures/papers/paper_list_l59_https_arxiv_org_abs_2602_06382/figures/014_Table.jpg]]
*Table: VII: Ablation study on distillation loss components. Results report mean $\pm$ $\mathrm { s t d }$ over 5 random seeds*

![[assets/figures/papers/paper_list_l59_https_arxiv_org_abs_2602_06382/figures/002_Table.jpg]]
*Table: I: Comparison of perceptive humanoid locomotion methods. Representation indicates the terrain perception approach. Noise Modeling indicates the comprehensiveness of depth sensor simulation. Long-Term Deploy indicates drift-free operation capability. Fine Locomotion indicates support for precise movements like stair climbing. Extreme Parkour indicates support for dynamic maneuvers across challenging obstacles*

## 定位与知识库关联

### 1. 方法谱系与知识库定位

本文工作处于**感知型仿人运动控制**（perceptive humanoid locomotion）这一研究脉络中，其核心问题是如何让仿人机器人在复杂地形上仅凭机载视觉传感器实现鲁棒、通用的端到端运动。该领域此前的方法可沿三个维度加以区分：感知表征形式、传感器噪声建模的完备性，以及策略架构对多地形泛化的支持程度。

#### 1.1 与现有感知型仿人运动方法的关系

在本文之前，最具代表性的视觉仿人运动工作是 **Humanoid Parkour Learning**（Zhuang et al., CoRL 2024），该方法首次展示了仿人机器人仅凭深度图像完成跑酷动作的能力。然而，该方法在深度传感器仿真上仅采用标准域随机化（如高斯噪声和随机掩码），未能系统性地复现立体相机在实际部署中的复杂失效模式。这导致其在RDT-Bench上的平均成功率仅为71.0%，且功率衰减率高达30.9%（TABLE IV），表明策略在应对真实深度噪声时存在显著的鲁棒性缺口。

本文的方法在三个关键维度上实现了对现有工作的系统性推进：

**（1）深度增强的完备性**。现有方法普遍采用简单的噪声注入策略，而本文提出的综合深度增强管道涵盖了立体融合、距离相关噪声、多倍频柏林噪声、随机卷积光学畸变、标定不确定性等8个操作（TABLE II），从物理机理层面模拟了立体深度传感器的真实退化过程。这一设计直接回应了核心瓶颈——仿真到现实深度感知噪声导致细粒度运动任务性能下降。消融实验表明，移除所有深度增强后，成功率从98.9%骤降至43.0%，功率衰减率飙升至70.9%（TABLE IV），定量验证了感知噪声是制约视觉运动策略sim-to-real迁移的首要因素。

**（2）多地形策略架构**。现有工作通常采用单一评论家与鉴别器架构，忽略了不同地形类别（楼梯/平台、间隙、粗糙地形）对运动策略的差异化要求。本文引入地形特定的多评论家和多鉴别器，结合针对性的奖励函数设计（如指数速度跟踪奖励用于楼梯，方向速度跟踪奖励用于间隙），有效缓解了跨异构地形的目标冲突问题。消融结果显示，替换为单一评论家/鉴别器后，平均成功率下降16.9个百分点（从98.9%降至82.0%），楼梯场景成功率下降14.9个百分点（TABLE VI），证实了多地形专用架构对统一策略泛化能力的关键贡献。

**（3）视觉感知蒸馏机制**。与直接对深度图像进行RL训练或采用标准行为克隆不同，本文引入了带去噪和KL正则化的两阶段蒸馏框架。教师策略利用特权高度扫描学习通用运动先验，学生策略通过行为克隆、降噪目标（强制干净与增强深度图像的表征一致性）和KL正则化（约束潜在空间接近标准正态先验）进行迁移。实验表明，直接RL训练导致功率衰减率高达58.1%（TABLE IV），而仅使用行为克隆的功率衰减率为17.7%（TABLE VII），均显著劣于完整蒸馏框架的5.8%。这一结果表明，两阶段训练对视觉控制的鲁棒性至关重要。

#### 1.2 适用边界与局限

尽管本文方法在RDT-Bench上取得了平均98.9%的成功率，但仍存在明确的适用边界：

- **下楼梯场景的鲁棒性不足**。下楼梯任务的成功率为86.7%（TABLE VIII），明显低于上楼梯的99.2%和间隙的99.3%。面向下的视角导致目标落足点被遮挡，加之重力对落地冲击的放大效应，使得该场景成为当前方法的薄弱环节。论文指出，更高分辨率的近距离感知或预测性足部放置策略可能是改进方向，但尚未验证。

- **跨平台泛化的验证范围有限**。尽管在Unitree G1上进行了零样本迁移验证（Figure 7），但测试仅限于上楼梯场景，未在间隙、平台和下楼梯等更复杂地形上进行全面评估（TABLE XVI）。深度增强管道的噪声参数范围基于启发式设置，可能未完全涵盖不同传感器型号的真实噪声特性。

- **地形类别的可扩展性**。多评论家/多鉴别器架构当前针对三类地形（楼梯/平台、间隙、粗糙地形）设计。论文未探讨将该架构扩展到更多地形类别（如动态障碍物）时的训练成本增长和性能退化情况。

- **评估环境的单一性**。尽管采用CycleGAN注入真实深度噪声以增强评估公平性，但所有实验均在单一仿真环境中进行，缺乏在不同仿真器间的泛化验证，也未能完全排除仿真环境特有的偏差。

#### 1.3 开放问题

从本文的工作出发，以下问题值得进一步探索：

1. **下楼梯鲁棒性的提升路径**。是否可以通过更高分辨率的近距离感知、预测性足部放置策略，或引入触觉反馈来弥补视觉遮挡带来的信息缺失？

2. **多地形架构的规模化**。所提多评论家方法能否扩展到更多地形类别（如动态障碍物、斜坡、泥泞地面），而不显著增加训练成本？是否存在自动地形识别与评论家分配的自适应机制？

3. **多模态感知融合**。深度增强策略是否可以与基于事件的相机（event camera）或RGB线索融合，以在极端光照或纹理缺失条件下进一步提升感知精度？

4. **长期部署的漂移问题**。当前方法未显式处理长期部署中传感器漂移和累计误差。是否可以通过在线自监督微调或视觉-惯性融合来缓解这一问题？

5. **跨机器人形态的迁移**。深度增强管道和蒸馏框架是否可推广至四足机器人或其他形态的腿式机器人？跨形态迁移中的感知表征对齐问题尚待研究。

## 原文 PDF

![[paperPDFs/arxiv_2026/Now_You_See_That_Learning_End_to_End_Humanoid_Locomotion_from_Raw_Pixels.pdf]]
