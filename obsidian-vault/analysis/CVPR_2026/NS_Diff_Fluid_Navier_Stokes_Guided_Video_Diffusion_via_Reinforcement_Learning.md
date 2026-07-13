---
title: "NS-Diff: Fluid Navier-Stokes Guided Video Diffusion via Reinforcement Learning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/NS_Diff_Fluid_Navier_Stokes_Guided_Video_Diffusion_via_Reinforcement_Learning.pdf
project_link: null
code_link: null
aliases:
- ND
- NS-Diff
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过强化学习在潜空间中引入物理奖励（刚体加加速度最小化与流体简化Navier-Stokes约束），并配合自适应物理激活调度，直接优化扩散轨迹以提升运动物理可信度。
primary_logic: 将简化的可微分物理约束（最小加加速度、不可压缩性等）作为强化学习的奖励函数，无需额外标注或仿真即可在潜空间内引导扩散生成过程，显著提高视频的物理一致性。
claims:
- 相较于现有方法，NS-Diff 将 Jerk 误差降低 43%，流体散度误差降低 33%，FVD 指标提升 22.7%。
- 在 PhysVideoBench 上，NS-Diff-DiT1B 的 ΔJ 为 0.33，L_div 为 2.9，大幅优于 VideoJam（0.74 / 4.7）和 Wan2.1（0.67 / 3.7）。
- PhysVideoBench 上 ΔJ (Jerk 误差) = 0.33
- PhysVideoBench 上 L_div (流体散度误差) = 2.9
---

# NS-Diff: Fluid Navier-Stokes Guided Video Diffusion via Reinforcement Learning

> [!tip] 核心洞察
> 将简化的可微分物理约束（最小加加速度、不可压缩性等）作为强化学习的奖励函数，无需额外标注或仿真即可在潜空间内引导扩散生成过程，显著提高视频的物理一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | NS-Diff: 基于强化学习的流体纳维-斯托克斯引导视频扩散模型 |
| 英文题名 | NS-Diff: Fluid Navier-Stokes Guided Video Diffusion via Reinforcement Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Deng_NS-Diff_Fluid_Navier-Stokes_Guided_Video_Diffusion_via_Reinforcement_Learning_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | NS-Diff |
| Dataset | PhysVideoBench, WebVid-10M |

> [!tip] 效果简介
> - PhysVideoBench 上，ΔJ (Jerk 误差) 0.33 vs 0.74 (VideoJam) (-55.4%)；L_div (流体散度误差) 2.9 vs 4.7 (VideoJam) (-38.3%)；Appear. (VBench) 73.1 vs 71.6 (VideoJam) (+1.5)。
> - WebVid-10M 上，FVD 275 vs 322 (VideoFactory) (-14.6%)；CLIPSIM 0.34 vs 0.31 (VideoFactory) (+9.7%)。

## 概要

现有视频扩散模型（如 Sora）虽能生成视觉质量极高的视频，但其生成的运动常违反物理规律——刚体出现非刚性变形、流体缺乏连续性，根本原因在于生成过程未引入物理约束。**NS-Diff**（CVPR 2026）针对这一瓶颈，提出了一种基于强化学习的物理引导视频扩散框架。其核心思路是：将简化的可微分物理约束（刚体最小加加速度、流体不可压缩性等）作为强化学习的奖励函数，在潜空间内直接优化扩散轨迹，从而显著提升视频的物理一致性，无需额外标注或外部仿真。

方法层面，NS-Diff 在标准视频扩散模型的基础上引入了三个关键改动：**(1) 物理属性检测**——从带噪潜变量中估计光流并检测刚体/流体区域；**(2) 物理条件潜变量注入（PCLI）**——将速度场、形变梯度与材质嵌入编码为物理潜变量，通过交叉注意力注入去噪网络；**(3) 强化学习优化**——将去噪轨迹形式化为物理约束 MDP，基于 PPO 最大化物理奖励，并配合自适应调度器根据噪声水平动态调节引导强度。

实验结果表明，NS-Diff 在 PhysVideoBench 上将 Jerk 误差（ΔJ）降至 0.33，相比 VideoJam（0.74）降低 55.4%；流体散度误差（L_div）降至 2.9，相比 VideoJam（4.7）降低 38.3%；同时 FVD 指标提升 22.7%，视觉质量（VBench）也略有提升。消融实验进一步证实，RL 优化、物理条件注入、自适应调度器及流体/刚体损失各自对物理一致性有显著贡献。



### 视频生成模型的物理可信度危机

近年来，以扩散模型（Diffusion Models）为核心的视频生成技术取得了令人瞩目的进展。从早期的 **ModelScope**（Luo et al., CVPR 2023）到后来的 **OpenSora2**（Peng et al., ArXiv 2025）和 **Wan2.1**（Wan Team, 2025），生成视频的视觉质量不断提升。然而，一个根本性的瓶颈逐渐暴露：**这些模型生成的视频虽然在像素层面逼真，但其运动模式常常严重违反物理规律**。如 Figure 1 所示，现有方法（包括Sora）会产生物理上不合理的变形——一把塑料椅子在运动中像流体一样扭曲，流沙则缺乏应有的连续性和不可压缩性。

这一问题的根源在于：标准扩散模型的训练目标仅仅是噪声预测的均方误差，完全没有引入任何物理约束。模型学会的是“看起来像”的统计模式，而非“物理上正确”的运动规律。这导致了两类典型的物理失真：
- **刚体非刚性变形**：本应保持形状的刚体对象出现不合理的弯曲、拉伸或断裂。
- **流体不连续性**：液体或颗粒状物质缺乏质量守恒和不可压缩性，出现突然消失、分裂或合并等非物理行为。

### 现有物理感知方法的局限

学术界已开始尝试将物理约束引入视频生成。**PhysGen**（Liu et al., ECCV 2024）通过外部物理仿真器生成运动轨迹，再结合扩散模型进行渲染，但这种方法依赖昂贵的仿真计算，且难以泛化到开放域场景。**VideoJam**（Chefer et al., ICML 2025）在生成过程中引入物理感知信号，但其物理引导机制较为粗糙，对复杂运动的约束效果有限。这些方法本质上都面临一个核心矛盾：**如何在保持扩散模型强大生成能力的同时，有效地注入物理约束，而无需依赖外部仿真器或额外的标注数据**。

### 本文动机与核心思路

NS-Diff 的提出正是为了填补这一缺口。其核心洞见是：**将简化的可微分物理约束转化为强化学习的奖励函数，直接在潜空间内优化扩散模型的去噪轨迹**。具体而言，该方法为刚体运动设计最小加加速度（Jerk）平滑约束，为流体运动设计基于简化Navier-Stokes方程的不可压缩性约束，并通过近端策略优化（PPO）将这些物理奖励融入扩散模型的训练过程。这一设计使得物理引导无需外部仿真器，也无需额外的物理标注，即可显著提升生成视频的物理一致性——实验表明，NS-Diff 将 Jerk 误差降低 43%，流体散度误差降低 33%，FVD 指标提升 22.7%。



## 核心方法与创新机理

NS-Diff 的核心创新在于将视频扩散模型的去噪轨迹重新形式化为**物理约束的马尔可夫决策过程（MDP）**，并通过强化学习在潜空间中直接施加物理引导，而非依赖外部仿真器或物理模拟器进行后处理。这一设计从根源上解决了现有视频扩散模型（如 Sora）生成的运动违反物理规律的问题——刚体发生非刚性变形、流体出现不连续性等。

与现有物理感知方法相比，NS-Diff 在四个关键维度上实现了根本性改变：

### 1. 训练目标：从噪声预测到物理奖励驱动的策略优化

现有方法（OpenSora2、Wan2.1 等）采用标准扩散损失——噪声预测均方误差，仅优化视觉质量而完全忽略物理一致性。**VideoJam**（Chefer et al., ICML 2025）虽引入物理感知，但仍以扩散损失为主。NS-Diff 则将训练目标替换为 **PPO 强化学习损失**，配合物理奖励函数：

$$\mathcal{T}_t = - \lambda_1 \mathcal{L}_{\mathrm{rigid}} - \lambda_2 \mathcal{L}_{\mathrm{fluid}}$$

其中 $\mathcal{L}_{\mathrm{rigid}}$ 惩罚刚体运动的加加速度（Jerk），强制运动平滑性；$\mathcal{L}_{\mathrm{fluid}}$ 采用简化 Navier-Stokes 约束，包含压力代理项 $\lambda_p\|\nabla(\nabla\cdot\mathbf{v}_t^k)\|_2^2$、散度项 $\|\nabla\cdot\mathbf{v}_t^k\|_2^2$、粘性项 $\nu\|\nabla^2\mathbf{v}_t^k\|_2^2$ 和对流项 $\eta\|\mathbf{v}_t^k\cdot\nabla\mathbf{v}_t^k\|_2^2$。PPO 目标函数为：

$$\mathcal{L}_{\mathrm{PPO}} = \mathbb{E}_t \left[ \min(r_t(\theta) A_t, \mathrm{CL}(r_t(\theta), 1-\epsilon, 1+\epsilon) A_t) \right]$$

这一转变的因果机制在于：扩散损失仅约束逐像素重建，而 PPO 通过策略梯度直接优化生成轨迹的物理属性。消融实验证实了该设计的决定性作用——移除 RL 优化、仅使用物理损失（Physics Losses w/o RL）会导致 ΔJ 从 0.33 增至 0.58，L_div 从 2.9 升至 4.7（Table 6），表明 PPO 对时序稳定性至关重要。

### 2. 物理条件注入：从无条件生成到交叉注意力引导的物理潜变量

现有方法仅依赖文本或时间嵌入进行条件生成，缺乏对运动动力学的显式建模。NS-Diff 设计了**物理条件潜变量注入（PCLI）**模块，将检测到的速度场、形变梯度与材质嵌入拼接后，通过 MLP 投影为物理潜变量：

$$\mathbf{p}_t^{(i)} = \mathbf{MLP}_{\mathrm{phys}}(\mathbf{s}_t^{(i)})$$

随后通过交叉注意力注入 DiT 去噪网络的中间特征：

$$\mathrm{Attn}(\mathbf{f}_t, \mathbf{p}_t) = \mathrm{Softmax}\left(\frac{(\mathbf{f}_t W_Q)(\mathbf{p}_t W_K)^\top}{\sqrt{d_p}}\right)(\mathbf{p}_t W_V)$$

移除该模块（w/o Condition Injection）使 ΔJ 恶化至 0.82，L_div 升至 6.9（Table 6），视觉质量同步下降，验证了物理条件注入是连接感知与生成的关键桥梁。

### 3. 运动与材质检测：从无显式检测到噪声鲁棒的刚体/流体区域识别

现有方法不区分运动类型，对所有区域施加统一处理。NS-Diff 引入**噪声鲁棒光流估计**，从带噪潜变量解码出低分辨率 RGB 代理后，使用 ARFlow 计算光流 $\mathbf{D}_t = \mathrm{ARFlow}(\hat{\mathbf{x}}_{t+1}, \hat{\mathbf{x}}_t)$，并通过全局运动补偿 $\mathbf{p}^{\prime} = \mathbf{H}_t \mathbf{p}$ 消除相机运动干扰。随后基于仿射拟合与软材质分类，将场景划分为刚体区域和流体区域，分别施加不同的物理约束。这一检测机制使物理引导具有**区域自适应性**——刚体区域最小化加加速度，流体区域强制不可压缩性。

### 4. 物理引导时机：从固定应用到自适应噪声感知调度

现有方法或未使用物理引导，或在整个去噪过程中固定施加。NS-Diff 提出**自适应物理激活调度器**，根据扩散时间步动态调节物理引导权重：

$$w_t = \left\{ \begin{array}{ll} 0, & \alpha\cdot(e^{(t/T)^2}-1) \le \sigma \\ \alpha\cdot(t/T)^2, & \alpha\cdot(e^{(t/T)^2}-1) > \sigma \end{array} \right.$$

该设计的核心洞察在于：高噪声阶段（早期去噪步）的物理属性检测不可靠（Table 1 显示噪声 0.35 时刚体 IoU 仅 71.3%），强制施加物理约束会引入错误梯度。调度器在高噪声时完全关闭物理引导（$w_t=0$），随去噪推进逐步激活。消融实验表明，移除自适应调度器（w/o Adaptive Scheduler）使 ΔJ 从 0.33 增至 0.67，L_div 从 2.9 升至 4.1，FVD 从 183 升至 207（Table 2 & Table 6），证明了噪声感知调度对物理引导精度的关键作用。

### 与代表性方法的本质差异

- **PhysGen**（Liu et al., ECCV 2024）依赖外部物理仿真器生成运动轨迹，再通过扩散模型渲染图像，属于“仿真-渲染”两阶段范式，计算开销大且难以端到端优化。NS-Diff 直接在扩散潜空间内施加可微分物理约束，无需外部仿真器。
- **VideoJam**（Chefer et al., ICML 2025）虽引入物理感知，但仍以扩散损失为主，物理约束作为辅助正则项。NS-Diff 将物理约束提升为强化学习的奖励函数，通过策略梯度直接优化生成策略，物理一致性提升更为显著（ΔJ 降低 55.4%，L_div 降低 38.3%）。

综上，NS-Diff 的创新本质在于**将物理先验从外部约束转变为核心优化目标**，通过 RL 框架实现物理引导与视觉生成的联合优化，配合噪声感知调度确保引导精度，从而在不牺牲视觉质量的前提下大幅提升运动物理可信度。



NS-Diff 将视频扩散模型的去噪轨迹重新形式化为一个物理约束的马尔可夫决策过程（MDP），在潜空间中直接引入物理引导。整体框架由三个核心模块串联构成，并通过一个自适应调度器协调物理引导的介入时机。

**Pipeline 概览。** 给定一个带噪潜变量序列 $\mathbf{z}_t$，框架首先将其解码为低分辨率 RGB 代理 $\hat{\mathbf{x}}_t$，送入**物理属性检测**模块以估计运动场并识别刚体/流体区域。随后，**物理条件潜变量注入（PCLI）** 模块将运动动力学（速度场、形变梯度）与材质嵌入编码为物理潜变量 $\mathbf{p}_t$，通过交叉注意力注入 DiT 去噪网络的特征 $\mathbf{f}_t$。最后，**强化学习优化**模块基于 PPO 策略梯度，以物理奖励 $\mathcal{T}_t$ 为信号更新 DiT 参数，使生成轨迹逐步逼近物理可行解。整个过程中，**自适应物理激活调度器**根据扩散时间步 $t/T$ 动态调节物理引导权重 $w_t$，在高噪声阶段关闭物理信号以避免错误梯度。

**模块间的数据流。** 物理属性检测模块输出两类信息：逐 patch 的运动速度 $\mathbf{v}_t^{(i)}$ 和形变梯度 $\nabla\mathbf{v}_t^{(i)}$，以及软材质分类分布 $\mathbf{q}_t^{(i)}$。这些信号与可学习的材质嵌入拼接后，经 MLP 投影为物理潜变量 $\mathbf{p}_t^{(i)}$，作为 PCLI 中交叉注意力的 Key 和 Value。PCLI 的输出 $\mathbf{f}_t' = \mathbf{f}_t + w_t \cdot \text{Attn}(\mathbf{f}_t, \mathbf{p}_t)$ 替换原 DiT 特征，参与后续去噪步骤。RL 优化器则从去噪轨迹中采样状态-动作对，计算物理奖励 $R_t = w_t(-\lambda_1\mathcal{L}_{\text{rigid}} - \lambda_2\mathcal{L}_{\text{fluid}})$，并通过 PPO 目标函数更新 DiT 参数。

**物理约束的定位。** 刚体惩罚 $\mathcal{L}_{\text{rigid}}$ 最小化检测到的刚体区域内速度场的加加速度（Jerk），强制运动平滑；流体惩罚 $\mathcal{L}_{\text{fluid}}$ 采用简化 Navier-Stokes 形式，约束流体区域的散度（不可压缩性）、粘性扩散和对流项。两项损失均仅在各自检测区域内计算，避免跨材质物理混淆。自适应调度器 $w_t$ 在扩散早期 $t/T$ 较小时保持为零，仅在噪声衰减到阈值 $\sigma$ 以下后平滑激活，确保物理梯度仅在潜变量结构初步显现时介入。

图 Figure 2 给出了三阶段框架的完整示意图，清晰展示了从噪声潜变量到物理感知去噪特征的信息流动路径。

![[assets/figures/papers/paper_list_l2697_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_NS_Diff_Fluid_Nav/figures/002_Figure_2.jpg]]
*Figure 2: Our framework enhances video diffusion via three stages: (1) Physical Attribute Detection: noise-robust optical flow estimates motion cues and object regions; (2) Physics-Conditioned Generation: motion dynamics are encoded into latent representations and injected into the DiT through adaptive cross-attention; (3) Reinforcement Learning Optimization: policy gradients enforce rigid jerk and fluid divergence constraints. An adaptive scheduler activates physics guidance based on noise levels*



NS-Diff 将视频扩散模型的去噪轨迹重新形式化为一个**物理约束的马尔可夫决策过程（MDP）**，并通过三个核心模块在潜空间中施加物理引导：物理属性检测、物理条件潜变量注入（PCLI）、以及强化学习优化。以下按模块拆解其关键公式与机制。

### 1. 物理属性检测：从带噪潜变量到运动与材质标签

该模块的目标是在扩散过程的中间步骤 $t$，从带噪潜变量 $\mathbf{z}_t$ 中提取可靠的物理属性，为后续的物理条件注入和奖励计算提供依据。

**前向扩散与代理解码**  
视频扩散模型的前向过程对初始潜变量 $\mathbf{z}_0$ 逐步加噪：
$$q(\mathbf{z}_t \vert \mathbf{z}_{t-1}) = \mathcal{N}(\mathbf{z}_t; \sqrt{\alpha_t} \mathbf{z}_{t-1}, (1 - \alpha_t) \mathbf{I}) \tag{eq.1}$$
为了在带噪状态下估计运动信息，模型将 $\mathbf{z}_t$ 解码为低分辨率 RGB 代理 $\hat{\mathbf{x}}_t$，并在其上运行光流估计。

**全局运动补偿**  
首先通过全局单应矩阵 $\mathbf{H}_t$ 消除相机运动，得到纯物体光流：
$$\mathbf{p}^{\prime} = \mathbf{H}_t \mathbf{p}, \quad \mathbf{D}_t(\mathbf{p}) = \mathbf{p}^{\prime} - \mathbf{p} \tag{eq.2}$$
其中 $\mathbf{p} = (x, y, 1)^{\top}$ 为齐次像素坐标。

**噪声鲁棒光流与时序平滑**  
在补偿后的代理帧上使用 ARFlow 估计光流：
$$\mathbf{D}_t = \mathrm{ARFlow}(\hat{\mathbf{x}}_{t+1}, \hat{\mathbf{x}}_t) \tag{eq.3}$$
为抑制单帧估计噪声，采用 $K=2$ 的 5 帧时序平滑：
$$\tilde{\mathbf{D}}_t = \frac{1}{2K+1} \sum_{k=-K}^{K} \mathbf{D}_t^k \tag{eq.4}$$

**刚体/流体区域检测与材质分类**  
基于平滑后的光流场，通过对局部 patch 的仿射拟合残差判定刚体区域 $\mathcal{R}_t^k$ 与流体区域 $\mathcal{F}_t^k$。同时，从 DiT 的 patch 特征 $\mathbf{f}_t^{\mathrm{patch},(i)}$ 通过小型 MLP 预测材质类型分布：
$$\mathbf{q}_t^{(i)} = \mathrm{Softmax}\big(\mathrm{MLP}_{\mathrm{type}}(\mathbf{f}_t^{\mathrm{patch},(i)})\big)$$
该分布用于生成材质嵌入，为后续物理约束提供细粒度的材质先验。

### 2. 物理条件潜变量注入（PCLI）：将物理信号注入 DiT

PCLI 模块将检测到的运动动力学和材质信息编码为物理潜变量，并通过交叉注意力注入 DiT 的中间特征层。

**物理潜变量投影**  
对每个 patch $i$，将速度场、形变梯度与材质嵌入拼接后，经 MLP 投影为物理潜变量：
$$\mathbf{p}_t^{(i)} = \mathbf{MLP}_{\mathrm{phys}}(\mathbf{s}_t^{(i)}) \tag{eq.9}$$
其中 $\mathbf{s}_t^{(i)}$ 为拼接后的物理信号向量。

**交叉注意力注入**  
物理潜变量 $\mathbf{p}_t$ 作为 Key 和 Value，DiT 特征 $\mathbf{f}_t$ 作为 Query，通过交叉注意力进行条件注入：
$$\mathrm{Attn}(\mathbf{f}_t, \mathbf{p}_t) = \mathrm{Softmax}\left(\frac{(\mathbf{f}_t W_Q)(\mathbf{p}_t W_K)^\top}{\sqrt{d_p}}\right)(\mathbf{p}_t W_V) \tag{eq.10}$$
注入后的特征为 $\mathbf{f}_t^{\prime} = \mathbf{f}_t + w_t \cdot \mathrm{Attn}(\mathbf{f}_t, \mathbf{p}_t)$，其中 $w_t$ 为自适应调度器输出的时变权重。

### 3. 强化学习优化：物理奖励驱动的去噪策略

NS-Diff 将去噪过程视为策略 $\pi_\theta$（即 DiT 网络）在 MDP 中的轨迹，通过 PPO 优化以最大化物理奖励。

**物理奖励函数**  
奖励由刚体加加速度最小化损失 $\mathcal{L}_{\mathrm{rigid}}$ 和流体简化 Navier-Stokes 损失 $\mathcal{L}_{\mathrm{fluid}}$ 组合而成：
$$\mathcal{T}_t = - \lambda_1 \mathcal{L}_{\mathrm{rigid}} - \lambda_2 \mathcal{L}_{\mathrm{fluid}} \tag{eq.16}$$
实际奖励信号经调度器加权：$R_t = w_t \cdot \mathcal{T}_t$。

**流体简化 Navier-Stokes 惩罚**  
对流体区域 $\mathcal{F}_t^k$，施加轻量级物理约束，包含压力代理项（梯度惩罚）、散度项（不可压缩性）、粘性项（拉普拉斯平滑）和对流项：
$$\mathcal{L}_{\mathrm{fluid}} = \frac{1}{|\mathcal{F}_t^k|} \sum_{(\boldsymbol{u},\boldsymbol{v})\in\mathcal{F}_t^k} \left( \lambda_p \|\nabla(\nabla\cdot\mathbf{v}_t^k)\|_2^2 + \|\nabla\cdot\mathbf{v}_t^k\|_2^2 + \nu\|\nabla^2\mathbf{v}_t^k\|_2^2 + \eta\|\mathbf{v}_t^k\cdot\nabla\mathbf{v}_t^k\|_2^2 \right) \tag{eq.15}$$
其中 $\mathbf{v}_t^k$ 为局部速度场，$\lambda_p$、$\nu$、$\eta$ 分别为各约束项的权重。

**PPO 策略优化**  
DiT 参数 $\theta$ 通过近端策略优化损失更新：
$$\mathcal{L}_{\mathrm{PPO}} = \mathbb{E}_t \left[ \min(r_t(\theta) A_t, \mathrm{CL}(r_t(\theta), 1-\epsilon, 1+\epsilon) A_t) \right] \tag{eq.18}$$
其中 $r_t(\theta)$ 为新旧策略的概率比，$A_t$ 为优势函数（基于物理奖励的价值估计），$\mathrm{CL}$ 为裁剪函数。

### 4. 自适应物理激活调度器

物理引导在高噪声阶段可能引入错误梯度，因此 NS-Diff 设计了自适应调度器，根据扩散时间步 $t/T$ 动态调节权重 $w_t$：
$$w_t = \left\{ \begin{array}{ll} 0, & \alpha\cdot(e^{(t/T)^2}-1) \le \sigma \\ \alpha\cdot(t/T)^2, & \alpha\cdot(e^{(t/T)^2}-1) > \sigma \end{array} \right. \tag{eq.19}$$
其中 $\alpha$ 为最大引导强度，$\sigma$ 为噪声阈值。在去噪早期（高噪声），$w_t = 0$ 完全关闭物理引导；随着 $t/T$ 增大、噪声降低，$w_t$ 平滑增长至 $\alpha$。该设计确保物理约束仅在潜变量结构足够清晰时才介入。

**调度器消融证据**：Table 2 显示，相比线性调度器，自适应调度器将 $\Delta J$ 从 0.67 降至 0.33，FVD 从 207 降至 183，验证了其在高噪声阶段抑制错误梯度的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l2697_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_NS_Diff_Fluid_Nav/figures/010_Figure_4.jpg]]
*Figure 4: t-SNE visualization of material embeddings*



## 实验与关键发现

### 主要性能对比

NS-Diff 在 **PhysVideoBench** 上的物理一致性与视觉质量均显著超越现有方法。如 Table 3 所示，NS-Diff-DiT1B 的 Jerk 误差 ΔJ 仅为 **0.33**，相较于 VideoJam（0.74）和 Wan2.1（0.67）分别降低 **55.4%** 和 **50.7%**；流体散度误差 L_div 为 **2.9**，远低于 VideoJam 的 4.7（降低 38.3%）。这表明 RL 驱动的物理奖励机制有效约束了刚体的非平滑运动与流体的不可压缩性。

![[assets/figures/papers/paper_list_l2697_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_NS_Diff_Fluid_Nav/figures/004_Table_3.jpg]]
*Table 3: Video Generation Performance on PhysVideoBench*

在视觉质量维度，NS-Diff 同样保持优势：VBench 的 Appearance 得分 **73.1**（VideoJam 71.6），Motion 得分 **92.4**（VideoJam 90.1），说明物理约束并未损害生成质量，反而通过抑制物理伪影提升了帧间一致性。

Figure 3 的定性对比进一步印证了定量结果——NS-Diff 生成的刚体保持结构完整性，流体运动自然，而 ModelScope、PhysGen、Wan2.1 和 OpenSora2 均出现物体异常出现/消失、非自然分裂/合并等物理伪影。

![[assets/figures/papers/paper_list_l2697_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_NS_Diff_Fluid_Nav/figures/007_Figure_3.jpg]]
*Figure 3: Visual comparison of NS-Diff, ModelScope, PhysGen, Wan2.1, and OpenSora2. Our method produces more realistic rigid and fluid motion, reduces unphysical artifacts (object appearance/disappearance, unnatural splitting/merging), and improves frame consistency*

在通用文本到视频基准 **WebVid-10M** 上，NS-Diff 的 FVD 降至 **275**（VideoFactory 322），CLIPSIM 提升至 **0.34**（VideoFactory 0.31），证明物理引导对通用视频生成任务也具有正向迁移效果。

### 组件消融分析

Table 6 的系统消融揭示了各模块的关键贡献：

![[assets/figures/papers/paper_list_l2697_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_NS_Diff_Fluid_Nav/figures/008_Table_6.jpg]]
*Table 6: Component Ablation Study on PhysVideoBench*

- **移除 RL 优化（仅保留物理损失）**：ΔJ 从 0.33 恶化至 0.58，L_div 升至 4.7。这表明直接施加物理损失作为监督信号无法有效约束时序一致性，PPO 的策略梯度机制对维持去噪轨迹的物理稳定性至关重要。
- **移除物理条件注入（w/o Condition Injection）**：ΔJ 飙升至 0.82，L_div 升至 6.9，视觉质量同步下降。物理潜变量通过交叉注意力注入 DiT 是引导生成的核心通路。
- **移除自适应调度器（w/o Adaptive Scheduler）**：ΔJ 增至 0.67，L_div 升至 4.1，FVD 从 183 升至 207（Table 2）。固定或线性调度在高噪声阶段引入错误梯度，反而损害生成质量。
- **移除流体损失（w/o L_fluid）**：L_div 从 2.9 骤升至 10.4，流体区域不可压缩性严重破坏，验证了简化 Navier-Stokes 约束的有效性。
- **移除刚体损失（w/o L_rigid）**：ΔJ 从 0.33 升至 1.33，刚体运动平滑性丧失，最小加加速度约束对刚体运动建模不可或缺。

![[assets/figures/papers/paper_list_l2697_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_NS_Diff_Fluid_Nav/figures/005_Table_2.jpg]]
*Table 2: Impact of Schedulers on Guidance Steps and FVD*

### 噪声鲁棒性与调度器设计

物理属性检测的精度高度依赖噪声水平。Table 1 显示，当噪声标准差为 0.05 时，刚体区域 IoU 达 **98.7%**，但在噪声 0.35 时降至 **71.3%**。这解释了自适应调度器的必要性：高噪声阶段（扩散早期）关闭物理引导，避免错误检测的梯度污染去噪轨迹。

![[assets/figures/papers/paper_list_l2697_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_NS_Diff_Fluid_Nav/figures/003_Table_1.jpg]]
*Table 1: Detection Accuracy under Increasing Noise*

Table 2 对比了不同调度策略：NS-Diff 的自适应调度器在仅使用 **6.2 步**物理引导的情况下，FVD 为 **183**，优于线性调度（10 步，FVD 207）和常数调度（10 步，FVD 195），以更少的引导步数实现了更优的生成质量。

### 超参数与设计选择

Table 7 的超参数敏感性分析表明，噪声阈值 σ 和对流权重 η 存在最优区间。Table 8 的光流骨干消融显示，在解码后的低分辨率 RGB 代理上估计光流优于直接在潜空间操作，ARFlow 的性能优于 RAFT 等替代方案。

![[assets/figures/papers/paper_list_l2697_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_NS_Diff_Fluid_Nav/figures/009_Table_8.jpg]]
*Table 8: Ablation on flow backbone and estimation domain*

![[assets/figures/papers/paper_list_l2697_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_NS_Diff_Fluid_Nav/figures/011_Table_7.jpg]]
*Table 7: Hyperparameter Sensitivity Analysis*

### 公平性说明

所有方法均在统一设置下评估：生成 2048 个片段，16 帧，256×256 分辨率，不使用文本提示或类别标签。物理指标（ΔJ、L_div）基于数据集真实光流或深度对齐的运动代理计算，避免学习型光流估计器的偏差。FVD 采用预训练于 Kinetics-400 的 I3D 模型评估。



## 定位与知识库关联

### 物理感知视频生成中的方法定位

NS-Diff 处于视频扩散模型与物理仿真交叉的前沿，其核心创新在于**将物理约束直接嵌入扩散模型的潜空间强化学习优化过程**，而非依赖外部仿真器或后处理修正。这一设计使其在方法谱系中占据独特位置。

**与现有物理感知方法的对比：**

- **VideoJam** (Chefer et al., ICML 2025) 同样探索物理感知视频生成，但 NS-Diff 在 PhysVideoBench 上实现了显著更优的物理一致性——Jerk 误差（ΔJ）从 0.74 降至 0.33（降幅 55.4%），流体散度误差（L_div）从 4.7 降至 2.9（降幅 38.3%）。这一差距表明，直接优化潜空间扩散轨迹比后处理或弱约束策略更有效。

- **PhysGen** (Liu et al., ECCV 2024) 采用“仿真-扩散渲染”两阶段流水线，需要显式物理模拟作为中间步骤。NS-Diff 避开了这一计算密集型路径，通过可微分的简化物理奖励（最小加加速度、不可压缩性代理）在潜空间内隐式地实现物理引导，无需运行完整仿真器。

- 相较于 **OpenSora2** (Peng et al., ArXiv 2025)、**Wan2.1** (Wan Team, 2025)、**ModelScope** (Luo et al., CVPR 2023) 和 **VideoFactory** (Wang et al., IJCV 2025) 等纯数据驱动的视频扩散模型，NS-Diff 在视觉质量指标上保持竞争力（VBench Appear. 73.1 vs. VideoJam 71.6），同时在物理可信度上实现质的飞跃。这验证了物理引导不必然以牺牲视觉保真度为代价。

### 适用边界与约束条件

NS-Diff 的设计基于以下关键假设和简化，定义了其当前适用边界：

1. **物理模型的简化近似**：刚体约束仅考虑最小加加速度（jerk minimization）平滑，未建模碰撞响应、摩擦、关节约束等交互力学；流体约束采用轻量级 Navier-Stokes 代理（散度惩罚 + 粘性正则 + 对流项），而非完整 CFD 求解。这意味着 NS-Diff 擅长抑制“明显违反直觉”的物理伪影，但无法保证严格物理精度。

2. **噪声鲁棒检测的退化边界**：物理属性检测模块在低噪声水平下表现优异（噪声 0.05 时刚体 IoU 达 98.7%），但在高噪声下显著退化（噪声 0.35 时降至 71.3%）。自适应调度器通过在早期扩散步关闭物理引导来规避此问题，但这限制了物理约束在去噪全程的作用范围。

3. **时序范围的局限**：当前实现支持 16 帧生成，扩展到长视频时，物理一致性的维持与计算开销的平衡尚未验证。PPO 优化在长时序上的信用分配（credit assignment）可能面临挑战。

### 局限与开放问题

**已识别的局限：**

- 物理约束为简化近似，在复杂多物体交互场景（如碰撞连锁反应、非牛顿流体）中的泛化性需要进一步验证。消融实验表明，移除流体损失使 L_div 从 2.9 飙升至 10.4，说明当前流体约束虽有效但仍高度依赖显式损失项，而非模型内化的物理理解。
- 极高噪声下的物理属性检测精度有限（刚体 IoU 仅 71.3%），限制了早期扩散步的物理引导潜力。Table 1 的噪声鲁棒性评估揭示了这一瓶颈。
- 材料嵌入虽展现出自主学习细粒度物理类别的能力（Figure 4 的 t-SNE 可视化），但其泛化到训练分布外材质的能力未经测试。

**开放问题：**

- 如何在更普适的视频生成任务（如大规模开放域文本到视频）中自动识别并施加恰当的物理约束，而非依赖预设的刚体/流体二分，仍是一个开放挑战。
- 当前方法未建模热力学、电磁学等其他物理领域，扩展到多物理场耦合生成的方向值得探索。
- 物理奖励的权重（λ₁、λ₂）和自适应调度器的噪声阈值（σ）需要通过超参数搜索确定（Table 7），如何实现任务自适应的自动调参是一个实用性问题。

### 知识库贡献

NS-Diff 的核心知识贡献在于**证明了强化学习可以有效地将可微分物理约束注入扩散模型的潜空间去噪轨迹**，而无需外部仿真器或额外标注。这一范式为物理感知生成模型开辟了新路径：将物理定律形式化为奖励函数，通过策略梯度直接优化生成过程。其自适应物理激活调度器（eq.19）解决了高噪声下物理梯度不可靠的关键工程挑战，这一设计模式可被后续工作在更广泛的物理领域中复用。



## 原文 PDF

![[paperPDFs/CVPR_2026/NS_Diff_Fluid_Navier_Stokes_Guided_Video_Diffusion_via_Reinforcement_Learning.pdf]]
