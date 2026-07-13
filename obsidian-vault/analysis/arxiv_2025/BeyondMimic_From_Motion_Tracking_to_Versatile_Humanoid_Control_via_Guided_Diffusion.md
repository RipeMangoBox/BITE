---
title: "BeyondMimic: From Motion Tracking to Versatile Humanoid Control via Guided Diffusion"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/BeyondMimic_From_Motion_Tracking_to_Versatile_Humanoid_Control_via_Guided_Diffusion.pdf
project_link: null
code_link: https://github.com/mujocolab/mjlab
aliases:
- BeyondMimic
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 紧凑且原则性的强化学习公式（基于锚点的相对跟踪、仅三项正则化的统一奖励、精确的驱动器电枢建模）实现可扩展的多样化运动跟踪；潜状态‑动作扩散模型利用其天然梯度场，通过分类器引导在测试时针对任意可微目标进行在线优化，从而零样本解决多种下游任务。
primary_logic: 扩散模型不仅能够捕捉复杂的多模态运动分布，其学习到的得分函数天然支持通过梯度进行测试时条件化（分类器引导），使得单一模型无需为每个任务重新训练或枚举目标组合，即可灵活组合已学技能并适应新目标。
claims:
- 使用统一的奖励公式和共享超参数成功学习约2.5小时多样化人类运动，30个运动片段（共15分钟）零样本部署到真实机器人。
- 在77人用户研究中，BeyondMimic动作的自然性显著优于Unitree原生控制器，总体偏好70.8%对比29.2%，p<.001。
- 消融实验表明，无观测历史、Rot6D连续旋转表示、精确电枢惯量和低部署延迟是实现成功sim-to-real的关键设计。
- 潜空间扩散模型在仿真中完成侧手翻的成功率达到95%，而无潜空间编码的基线仅5%。
---

# BeyondMimic: From Motion Tracking to Versatile Humanoid Control via Guided Diffusion

> [!tip] 核心洞察
> 扩散模型不仅能够捕捉复杂的多模态运动分布，其学习到的得分函数天然支持通过梯度进行测试时条件化（分类器引导），使得单一模型无需为每个任务重新训练或枚举目标组合，即可灵活组合已学技能并适应新目标。

| 字段 | 内容 |
|------|------|
| 中文题名 | BeyondMimic：从运动跟踪到通过引导扩散实现通用人形机器人控制 |
| 英文题名 | BeyondMimic: From Motion Tracking to Versatile Humanoid Control via Guided Diffusion |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2508.08241) · [paper](https://arxiv.org/abs/2503.11801) · [Code](https://github.com/mujocolab/mjlab) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | BeyondMimic |
| Dataset |  |

> [!tip] 效果简介
> - 用户偏好调查 (N=77) 上，选择“更像人/更自然”的比例 70.8% (总体) vs 29.2% (Unitree原生控制器, 总体) (+41.6% (总体); 步行+14.0%; 跑步+69.4%)。
> - 仿真速度跟踪 上，平均速度跟踪误差 步行12.14%, 跑步13.65% vs 未明确提供基线 (N/A)。
> - 仿真侧手翻成功率 上，成功率 95% (有潜空间) vs 5% (无潜空间编码) (+90%)。

## 概要

人形机器人控制面临一个根本性瓶颈：现有方法要么产生不自然的动作、需要针对每个具体运动进行大量调参，要么缺乏组合多种技能以解决未见任务的通用性，难以在保持人类级敏捷性和自然性的同时实现可扩展的任务适应。**BeyondMimic** 通过两个核心机制突破这一困境：

1. **可扩展的运动跟踪**：一个紧凑且原则性的强化学习公式——基于锚点的相对跟踪、仅三项正则化的统一奖励、精确的驱动器电枢建模——使得单一策略和共享超参数即可掌握约2.5小时的多样化人类运动，包括空翻、旋踢、冲刺等高动态技能，并零样本部署到真实机器人。

2. **通过引导扩散实现通用控制**：一个潜状态‑动作扩散模型利用其天然梯度场，通过分类器引导在测试时针对任意可微目标进行在线优化，从而零样本解决航点导航、摇杆遥控、障碍物回避和动作补全等多种下游任务，无需重新训练。

核心洞察在于：扩散模型不仅能够捕捉复杂的多模态运动分布，其学习到的得分函数天然支持通过梯度进行测试时条件化，使得单一模型可以灵活组合已学技能并适应新目标。

**主要结果**：
- 在77人用户研究中，BeyondMimic动作的自然性显著优于Unitree原生控制器，总体偏好70.8%对比29.2%（p<.001）。
- 潜空间扩散模型在仿真中完成侧手翻的成功率达95%，而无潜空间编码的基线仅5%。
- 消融实验证实，Rot6D连续旋转表示、无观测历史、精确电枢惯量和低部署延迟是实现成功sim-to-real的关键设计。

**方法定位**：与需要逐运动调参的**DeepMimic**（Peng et al., ACM Trans. Graph. 2018）、策略不可跨任务复用的**Adversarial Motion Priors**（Peng et al., ACM Trans. Graph. 2021）、依赖显式目标条件训练的VAE类方法、以及解耦训练导致敏捷性下降的分层控制架构相比，BeyondMimic通过统一的跟踪公式与扩散引导实现了可扩展的多样化运动学习和零样本任务适应。

使双足人形机器人在现实世界中展现出人类般的敏捷性与自然性，一直是机器人学领域的核心挑战。人类运动具有高度的多样性、动态性和协调性——从平稳行走、快速奔跑到空翻、旋踢等高难度技巧动作——而机器人系统要在保持平衡与物理一致性的同时复现这些行为，面临着建模、学习与部署等多重瓶颈。

### 现有方法的局限

当前主流方法可归纳为以下几类，但各自存在根本性瓶颈：

**基于强化学习的运动跟踪方法**，以 **DeepMimic**（Peng et al., ACM Trans. Graph. 2018）为代表，通过逐帧跟踪参考运动来学习控制策略。这类方法虽然能复现特定运动，但通常需要针对每个具体运动片段进行大量奖励调参，难以扩展到多样化运动集合。运动风格控制方面，**Adversarial Motion Priors (AMP)**（Peng et al., ACM Trans. Graph. 2021）利用对抗学习使策略隐式匹配参考运动分布，但学到的策略往往不可跨任务复用，每个新任务都需要从零训练。

**基于变分自编码器的多任务生成方法**（如 LocoVAE、MoGlow）试图通过潜变量建模运动多样性，但依赖显式目标条件训练，对训练中未见的隐性目标（如“避开障碍物同时保持自然步态”）泛化能力差。**分层控制架构**将运动跟踪器与高层规划器解耦训练，但这种解耦常导致规划器与控制器之间的失配，损害运动的敏捷性和自然性。

这些方法的共同困境在于：要么产生不自然的动作模式，要么缺乏组合多种技能以解决未见任务的通用性，难以在保持人类级敏捷性和自然性的同时实现可扩展的任务适应。

### 核心动机

BeyondMimic 的出发点是打破上述困境，实现两个关键目标：

1. **可扩展的运动学习**：通过紧凑且原则性的强化学习公式，使单一策略能够掌握从静态姿态到高动态技巧的广泛运动谱系，无需针对每个运动进行单独调参。
2. **通用任务适应**：使学到的多种运动技能能够灵活组合，在测试时零样本适应航点导航、摇杆遥控、障碍物回避等未见下游任务，无需重新训练或枚举目标组合。

实现这一愿景的技术直觉在于：扩散模型不仅能够捕捉复杂的多模态运动分布，其学习到的得分函数天然支持通过梯度进行测试时条件化（分类器引导），使得单一模型即可灵活组合已学技能并适应新目标。这一洞察将运动学习与任务适应统一在一个连贯的框架内，为通用人形机器人控制提供了新的路径。

## 核心方法与创新机理

BeyondMimic 的核心创新在于将**可扩展的运动跟踪强化学习**与**基于引导扩散的通用控制**深度耦合，形成一条从多样运动学习到零样本任务适应的完整技术链路。其关键突破可归结为以下五个“changed slots”，每个 slot 均通过消融实验或用户研究获得了有力验证。

### 1. 统一的奖励公式：从繁琐调参到三项正则化

传统运动跟踪方法（如 **DeepMimic** (Peng et al., ACM Trans. Graph. 2018)）需要为每个运动片段单独设计接触力、滑移、跌倒等惩罚项，泛化性严重受限。BeyondMimic 将奖励函数蒸馏为仅三项正则化项——**动作平滑惩罚**、**关节位置限制惩罚**和**非必要自接触惩罚**——外加一个统一的、基于高斯形状的指数任务奖励：

$$
r = r_{\mathrm{task}} - \lambda_l r_{\mathrm{limit}} - \lambda_s r_{\mathrm{smooth}} - \lambda_c r_{\mathrm{contact}}
$$

其中 $r_{\mathrm{task}} = \sum_{s\in\{\mathbf{p},R,\mathbf{v},\omega\}} r(\bar{e}_s,\sigma_s)$，对位置、朝向、线速度和角速度的跟踪误差分别计算高斯奖励后求和。这一公式使策略能够在**完全相同的 MDP 和超参数**下学习约 2.5 小时的多样化人类运动，无需任何针对特定运动的调参（证据锚点：part_006, Table S1）。

### 2. 锚点相对跟踪：允许全局漂移的运动表示

与绝对坐标跟踪不同，BeyondMimic 引入**锚点相对跟踪**机制：以当前机器人姿态的锚点身体为参考系，表达目标姿态的相对位置和朝向。这一设计使策略允许全局位置的合理漂移与恢复，大幅提升了 sim-to-real 转移的鲁棒性。消融实验表明，该设计是实现零样本真实部署的关键要素之一（证据锚点：part_006, part_007, Fig. 7A）。

### 3. 连续旋转表示与精确电枢建模：Sim-to-Real 的关键工程突破

消融实验（Fig. 8A）揭示了四个对 sim-to-real 转移至关重要的设计选择：

- **Rot6D 连续旋转表示**：相比四元数或轴角，Rot6D 在真实机器人上获得了显著更好的跟踪性能。
- **无观测历史**：策略仅使用当前观测，包含历史信息反而降低性能——这与直觉相悖，但对真实部署的延迟敏感性至关重要。
- **精确电枢反射惯量**：使用制造商提供的精确值，不准确或设为零的电枢惯量会导致加速度过大和自碰撞，严重降低跟踪精度。
- **极低部署延迟**：通过 C++ 实时框架优化，单次策略推理 < 1ms。消融显示，2ms 延迟即增加速度误差，5ms 导致一次失败，10ms 在三试中失败两次。

这些工程细节的累积效应是：30 个运动片段（共 15 分钟）从仿真零样本部署到真实 Unitree G1 机器人，无需硬件微调。

### 4. 潜状态‑动作扩散模型：从单任务策略到通用控制

与 **AMP** (Peng et al., ACM Trans. Graph. 2021) 需要从零训练每个任务、VAE 类方法依赖显式目标条件训练不同，BeyondMimic 在第二阶段训练一个**统一的潜状态‑动作扩散模型**。该模型的关键特性在于：扩散模型天然学习到的得分函数 $\nabla_{\tau} \log p(\tau)$ 支持通过贝叶斯规则进行测试时条件化：

$$
\nabla_{\tau} \log p(\tau \mid \tau^*) = \nabla_{\tau} \log p(\tau) + \nabla_{\tau} \log p(\tau^* \mid \tau)
$$

其中条件梯度 $\nabla_{\tau} \log p(\tau^* \mid \tau)$ 用可微任务成本函数 $G(\tau)$ 近似：$\nabla_{\tau} \log p(\tau^* \mid \tau) = -\nabla_{\tau} G(\tau)$。这一**分类器引导**机制使得单一模型在推理时即可针对任意可微目标进行在线优化，无需重新训练或枚举目标组合（证据锚点：part_009, part_017）。

### 5. 零样本任务组合：从运动跟踪到通用人形控制

基于上述引导机制，BeyondMimic 在零样本条件下实现了多种未见任务的灵活组合：

- **航点导航**：通过混合成本函数引导扩散轨迹走向目标航点。
- **摇杆遥控**：以速度命令平方差为成本，实现实时速度控制。
- **障碍物回避**：利用 SDF 障碍函数进行场景感知导航。
- **动作补全**：注入稀疏未来关键帧，引导策略生成平滑的过渡动作（如从行走到侧手翻）。
- **任务组合**：将多个简单任务成本直接求和，实现避障导航等复合行为。

消融实验进一步表明，潜空间编码对复杂运动至关重要：侧手翻的成功率从无潜空间编码的 5% 跃升至 95%（证据锚点：part_010）。

### 创新总结

BeyondMimic 的核心创新不在于提出全新的算法组件，而在于**系统性地识别并解决了从多样化运动学习到通用控制的关键瓶颈**：通过锚点相对跟踪和统一奖励实现可扩展的运动学习，通过精确电枢建模和极低延迟实现可靠的 sim-to-real 转移，通过潜扩散引导实现零样本任务适应。这些 changed slots 共同构成了一个从数据到部署的完整解决方案，在 77 人用户研究中以 70.8% 对 29.2% 的显著优势超越 Unitree 原生控制器（p < .001, Cohen's h = 0.859），验证了其产生类人自然运动的能力（证据锚点：part_003）。

BeyondMimic 采用两阶段流水线架构，将多样化人类运动的学习与面向未见任务的通用控制解耦为两个模块，二者通过紧凑的潜空间衔接。

**阶段一：可扩展运动跟踪 (Scalable Motion Tracking).** 该阶段将运动跟踪建模为马尔可夫决策过程（MDP），使用强化学习训练一个统一的跟踪策略。核心设计在于“锚点相对跟踪”（anchor-relative tracking）：以机器人骨盆为锚点，将所有身体部位的目标位姿表达在锚点中心坐标系中，使策略能够容忍全局漂移并在偏离后自然恢复，这是实现零样本 sim‑to‑real 迁移的关键（Figure 7A）。任务奖励采用高斯形状的指数跟踪误差之和，仅叠加三项正则化惩罚（关节限位、动作平滑、非必要自接触），整个奖励公式对所有运动共享同一组超参数，无需针对特定运动调参。策略网络是一个 MLP，以 50 Hz 运行，输入当前观测（运动相位、锚点误差、IMU 速度、相对关节位置/速度、上一步动作），输出关节位置设定点，由底层 PD 控制器执行。

**阶段二：潜状态‑动作扩散模型 (Latent State‑Action Diffusion Model).** 为赋予单一模型组合多种技能并适应新目标的能力，论文首先使用 VAE 将状态‑动作轨迹压缩到紧凑潜空间（维数 32），再在该潜空间中训练一个去噪扩散概率模型（DDPM）。扩散模型以 Transformer 为骨干，预测未来 16 步（0.64 s）的潜轨迹，通过 20 步迭代去噪恢复干净轨迹。其核心洞察在于：扩散模型学习到的得分函数天然支持分类器引导（classifier guidance）——在推理时，通过贝叶斯规则将无条件得分场转换为条件得分场，条件梯度由可微任务成本函数近似。这使得同一模型无需重新训练或枚举目标组合，即可在测试时针对任意可微目标进行在线优化，零样本解决航点导航、摇杆遥控、障碍物回避、动作补全等多种下游任务。

**实时部署.** 整个框架以 C++ 实现：状态估计以 500 Hz 运行，策略推理在 CPU 上单次 < 1 ms，扩散推理异步执行于移动 GPU（约 20 ms）。梯度通过 CppAD 自动求导，模型经 TensorRT 加速，确保精确的时序同步。

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2508_08241/figures/007_Figure_7.jpg]]
*Figure 7: Overview of the framework. (A) Scalable learning of diverse human motions via motion tracking. (i) The target motion is re-anchored to the current pose to allow drift and recovery, which is critical for successful sim-to-real transfer. (ii) Diverse motions are tracked with RL using a single recipe and shared hyperparameters, showing scalability across a broad spectrum of skills. (B) Versatile control via latent state-action diffusion model. (i) Stage 1: A VAE is trained via DAgger to compress the diverse motion tracking policies into a smooth, structured latent space. (ii) Stage 2: A state-latent diffusion model is trained on VAE trajectory rollouts. During inference, the current action is...*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2508_08241/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed versatile humanoid control framework. (A) Scalable and robust learning from human motions with agile, human-like behaviors via motion tracking. (B) Versatile control over unseen downstream tasks with diverse learned motor skills via guided diffusion*

BeyondMimic 采用两阶段流水线：第一阶段通过紧凑的强化学习公式实现可扩展的运动跟踪，第二阶段构建统一的潜状态‑动作扩散模型，通过分类器引导在测试时实现零样本任务适应。

### 运动跟踪策略

运动跟踪被形式化为马尔可夫决策过程（MDP），使用 PPO 求解。核心设计原则是**锚点相对跟踪**：定义一个锚点身体 $b_{\mathrm{anchor}}$（通常为骨盆），将所有期望姿态表达在锚点中心坐标系中。这一设计允许策略在发生全局漂移时自行恢复，是成功 sim-to-real 的关键。

**观测向量**定义为：

$$
\mathbf{o} = [\psi, \mathbf{e}_{\mathrm{anchor}}, \mathcal{V}_{\mathrm{imu}}, \theta - \theta^0, \dot{\theta}, \mathbf{a}_{\mathrm{last}}]
$$

其中 $\psi$ 为运动相位，$\mathbf{e}_{\mathrm{anchor}}$ 为锚点跟踪误差，$\mathcal{V}_{\mathrm{imu}}$ 为 IMU 线速度和角速度，$\theta - \theta^0$ 为相对默认关节位置，$\dot{\theta}$ 为关节速度，$\mathbf{a}_{\mathrm{last}}$ 为上一步动作。策略网络（MLP）以 50Hz 输出动作 $\mathbf{a}$，关节位置设定点由下式给出：

$$
\boldsymbol{\theta}^{\mathrm{sp}} = \boldsymbol{\theta}^0 + \boldsymbol{\alpha} \odot \mathbf{a}
$$

其中 $\boldsymbol{\alpha}$ 为动作缩放因子。

**统一奖励函数**仅包含四项，对所有运动使用相同超参数：

$$
r = r_{\mathrm{task}} - \lambda_l r_{\mathrm{limit}} - \lambda_s r_{\mathrm{smooth}} - \lambda_c r_{\mathrm{contact}}
$$

任务奖励为各跟踪部分的高斯形状指数奖励之和：

$$
r_{\mathrm{task}} = \sum_{s\in\{\mathbf{p},R,\mathbf{v},\omega\}} r(\bar{e}_s,\sigma_s)
$$

其中 $s$ 分别对应位置、朝向、线速度和角速度的跟踪误差。三项正则化分别为关节位置限制惩罚 $r_{\mathrm{limit}}$、动作平滑惩罚 $r_{\mathrm{smooth}}$ 和非必要自接触惩罚 $r_{\mathrm{contact}}$。

### VAE 潜空间编码

为将高维状态‑动作轨迹压缩到紧凑潜空间以高效训练扩散模型，使用变分自编码器（VAE）进行编码。VAE 使用 DAgger 训练，编码器仅接收参考运动组件（相位 $\psi$ 和锚点误差 $\mathbf{e}_{\mathrm{anchor}}$），解码器结合本体感觉重建动作。潜空间维数为 32。

VAE 训练损失为：

$$
\mathcal{L}_{\mathrm{VAE}} = \mathbb{E}[\|\hat{\mathbf{a}} - \mathbf{a}\|^2] + \beta D_{\mathrm{KL}}(q_{\mathcal{E}}(\mathbf{z}\mid\psi,\mathbf{e}_{\mathrm{anchor}})\|\mathcal{N}(\mathbf{0},\mathbf{I}))
$$

包含动作重建均方误差和 KL 正则项，$\beta$ 控制潜空间的正则化强度。

### 潜状态‑动作扩散模型

扩散模型在 VAE 的潜空间中执行去噪扩散概率模型（DDPM），预测未来 16 步（0.64 秒）的潜轨迹 $\tau$。使用 Transformer 骨干（6 层，8 头），20 步去噪。

扩散模型的自监督训练损失为预测干净潜轨迹的均方误差：

$$
\mathcal{L}_{\mathrm{Diffusion}} = \mathbb{E}\big[\| z_{\phi}(\tau^{\mathbf{k}}, \mathbf{k}) - \tau \|^2 \big]
$$

其中 $z_{\phi}$ 为去噪网络，$\tau^{\mathbf{k}}$ 为第 $\mathbf{k}$ 步加噪后的潜轨迹。

推理时，迭代去噪步骤为：

$$
\tau^{\mathbf{k}-1} = \alpha_{\mathbf{k}} (\tau^{\mathbf{k}} - \gamma_{\mathbf{k}} (\tau^{\mathbf{k}} - z_{\phi}(\tau^{\mathbf{k}}, \mathbf{k}))) + \sigma_{\mathbf{k}} N(0, \mathbf{I})
$$

从纯噪声 $\tau^{\mathbf{K}} \sim \mathcal{N}(0, \mathbf{I})$ 开始，逐步恢复干净轨迹 $\tau^0$，再经 VAE 解码器重建动作序列。

### 分类器引导

扩散模型的核心优势在于其学习到的得分函数 $\nabla_{\tau} \log p(\tau)$ 天然支持测试时条件化。通过贝叶斯规则：

$$
\nabla_{\tau} \log p(\tau \mid \tau^*) = \nabla_{\tau} \log p(\tau) + \nabla_{\tau} \log p(\tau^* \mid \tau)
$$

将无条件得分场转化为条件得分场。似然梯度用可微任务成本函数 $G(\tau)$ 近似：

$$
\nabla_{\tau} \log p(\tau^* \mid \tau) = -\nabla_{\tau} G(\tau)
$$

在去噪的每一步，将 $-\nabla_{\tau} G(\tau)$ 加到无条件得分上，即可引导生成轨迹向满足任务目标的方向优化。不同任务的成本函数可灵活组合，实现零样本任务泛化。

### 实时部署框架

C++ 实现，全状态估计以 500Hz 运行，策略推理单次 <1ms（CPU），扩散推理异步进行约 20ms（移动 GPU）。使用 TensorRT 加速扩散模型，梯度通过 CppAD 自动求导计算。精确的驱动器电枢惯量建模和极低的部署延迟（<1ms）是成功 sim-to-real 的关键工程保障。

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2508_08241/figures/008_Figure_8.jpg]]
*Figure 8: Ablation studies. (A) Motion tracking error comparison ablating orientation representation, history length, armature, and delay, showing that continuous orientations, no observation history, correct armature settings, and minimal deployment delay are critical for sim-to-real transfer in our setup. (B) Training performance ablating adaptive sampling (AS). (i) Iterations required to solve the motion; without AS, difficult segments remain unsolved even after 30k iterations. (ii) Visualization for Motion 1, highlighting two challenging cartwheel segments that cause the baseline to fail. (iii) Evolution of the sampling distribution, showing that AS concentrates sampling on difficult segments ear...*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2508_08241/figures/005_Figure_5.jpg]]
*Figure 5: Command-conditioned locomotion via guided diffusion. (A) Visualization of diffusion process under joystick control. Starting from Gaussian noise, the distribution progressively converges to optimize for a right-turn command. (B) Waypoint navigation. From multiple start points, the robot reaches the goal using forward or backward walking. (C) Joystick teleoperation. The robot tracks the joystick velocity command. Even under an impulsive disturbance, it recovers quickly and continues following the backward command. (D) t-SNE visualization of the latent space, illustrating the transition from walking to running. (E) Real-world transition from walking to running conditioned on velocity command*

## 实验与关键发现

### 主结果：可扩展运动学习与零样本部署

BeyondMimic在统一奖励公式和共享超参数下，成功学习约2.5小时多样化人类运动，并将其中30个代表性片段（共15分钟）零样本部署到真实Unitree G1机器人，涵盖静态平衡、动态步态和高动态特技动作（图2）。在户外环境中，机器人完成空翻、旋踢等高敏捷性动作：空中阶段峰值加速度达31 m/s²，骨盆角速度最高达20 rad/s（均值7.01 rad/s）（图3）。

在行走与跑步的自然性评估中，77人用户研究显示BeyondMimic总体偏好率为70.8%，显著优于Unitree原生控制器的29.2%（p<.001, Cohen's h=0.859）。分项来看，行走偏好为57.0%对43.0%（p<.001, h=0.281），跑步偏好为84.7%对15.3%（p<.001, h=1.532）。仿真速度跟踪误差为步行12.14%、跑步13.65%。

潜空间扩散模型在仿真侧手翻任务中达到95%成功率，而无潜空间编码的基线仅5%（+90%），验证了潜空间压缩对高动态运动生成的关键作用。

### 通用控制：零样本任务适应

通过分类器引导，单一扩散模型在测试时实现了多种未见任务的零样本解决，无需重新训练：
- **命令条件运动**：摇杆遥控实现连续速度跟踪，并展示从步行到跑步的平滑步态过渡（图5D-E）。
- **运动补全**：以0.2秒间隔注入侧手翻关键帧，策略自动生成平滑中间动作，实现从摇杆步行到侧手翻的无缝过渡（图6A）。
- **任务组合**：将航点导航成本与SDF避障成本简单求和，同时实现目标导航与障碍物回避（图6B）。成本函数可微且任务特定，推理时灵活组合而无需枚举所有可能。

### 消融实验：关键设计选择

消融实验（图8A）揭示了实现成功sim-to-real转移的四个核心设计：

1. **朝向表示**：Rot6D连续旋转表示的sim-to-real性能显著优于四元数或轴角。
2. **观测历史**：策略观测中不包含历史信息比包含历史有更好的sim-to-real性能，与直觉相反。
3. **电枢惯量**：使用制造商提供的精确反射惯量（Table S3-S4）显著优于不准确或零电枢配置；零电枢导致加速度过大和自碰撞。
4. **部署延迟**：延迟对性能影响极大——2ms即增加速度误差，5ms导致一次失败，10ms在三试中失败两次。通过C++实时框架将单次推理优化至<1ms，确保精确同步。

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2508_08241/figures/013_Table_S.3.jpg]]
*Table S.3: Actuator reflected inertia. Total*

此外，自适应采样（AS）消融（图8B）表明：无AS时4个困难运动中有3个在30k轮次后仍失败；启用AS后不仅解决所有运动，还将简单运动所需迭代轮次从4k降至2k。PD增益消融（图S2）显示固有频率10Hz实现最佳全局跟踪性能；更高频率（如25Hz）引起高频振荡和硬件冲击。

### 失败模式与局限性

1. **状态估计噪声传播**：潜扩散模型依赖本体感觉状态估计，估计噪声会传播到生成轨迹中，影响动作质量。
2. **预测时域受限**：当前预测窗口仅0.64秒，无法处理需要远距离推理的长期规划任务。
3. **历史依赖与引导冲突**：模型依赖历史信息以稳定预测，但在引导激活时可能导致陷入重复运动模式；加大引导权重可缓解，但在模式切换或高方差状态下会破坏稳定性，导致运动起始和结束时踉跄。
4. **细粒度目标局限**：引导优化对粗粒度目标有效，但对细粒度目标效果有限，且仍需对引导权重进行轻量手动调节。
5. **硬件约束**：机器人缺乏脚趾关节，限制了行走时的蹬地推进，导致地面反力峰值更尖锐，与人类的柔顺性仍有差距。

### 公平性说明

所有运动跟踪策略使用完全相同的MDP公式、奖励函数和超参数，无任何针对特定运动的调参。sim-to-real转移为零样本，策略直接在仿真中训练后部署到真实机器人，未进行硬件特定的微调。用户研究采用双尾二项检验和Bonferroni校正，比较对象是同一机器人平台上的Unitree原生控制器，并报告了效应量。消融实验在统一仿真设置下进行，仅改变所研究的设计因素，其余保持一致。

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2508_08241/figures/002_Figure_2.jpg]]
*Figure 2: Diverse motion tracking policies deployed on a real humanoid robot. We demonstrate accurate and robust tracking across a wide spectrum of motions, ranging from static to highly dynamic and from athletic feats to stylized motions, showing the scalability of our framework. In total, 30 distinct motion clips are deployed on hardware; with a subset shown here due to space. See Movie S2 for the full repertoire*

## 定位与知识库关联

### 与基线工作的关系

**BeyondMimic** 处于人形机器人运动学习与控制的两阶段范式交汇处，其设计直接回应了现有方法的几个关键瓶颈。

**与 DeepMimic 的关系**（Peng et al., ACM Trans. Graph. 2018）。DeepMimic 开创了基于强化学习的运动跟踪框架，但需要为每个具体运动片段单独调整奖励权重和训练策略，泛化性有限。BeyondMimic 继承了运动跟踪的基本 MDP 框架，但通过三项关键设计实现了可扩展性突破：基于锚点的相对跟踪公式、统一的高斯形状任务奖励、以及仅三项正则化项（关节限制、动作平滑、非必要自接触惩罚）。这使得约 2.5 小时的多样化人类运动数据可用完全相同的超参数和奖励结构一次性训练完成，无需任何针对特定运动的调参。

**与 Adversarial Motion Priors (AMP) 的关系**（Peng et al., ACM Trans. Graph. 2021）。AMP 通过对抗学习从参考数据中提取风格先验，但训练后的策略通常不可跨任务复用，每个新任务需从零训练。BeyondMimic 采用不同的路径：第一阶段通过运动跟踪学习可复用的运动技能库，第二阶段通过潜扩散模型在测试时组合这些技能。这种分离使得运动技能的学习与下游任务的适应解耦，避免了 AMP 中策略重训的高昂成本。

**与 VAE 基策略的关系**（如 LocoVAE、MoGlow）。这类方法依赖显式目标条件训练，策略的泛化能力受限于训练时所见的目标组合。BeyondMimic 的潜状态‑动作扩散模型利用其天然得分函数的梯度场，通过分类器引导在测试时针对任意可微目标进行在线优化，无需枚举所有可能的目标组合。这使得单一模型可以零样本解决航点导航、摇杆遥控、障碍物回避等多种未见任务。

**与分层控制方法的关系**。传统的“运动跟踪器+规划器”分层架构因解耦训练常导致规划器与控制器失配，损害敏捷性和自然性。BeyondMimic 的扩散模型直接预测未来 16 步（0.64 秒）的状态‑动作轨迹，在统一的潜空间中同时优化运动质量和任务目标，避免了分层架构中的信息断裂。

**与 Unitree 原生控制器的关系**。在 77 人用户研究中，BeyondMimic 的动作自然性显著优于同一机器人平台（Unitree G1）上的原生控制器，总体偏好 70.8% 对比 29.2%（p < .001，Cohen's h = 0.859），在跑步场景中优势尤为突出（84.7% vs 15.3%，h = 1.532）。这一对比直接验证了运动跟踪范式在产生类人自然性方面的优势。

### 关键设计选择与消融证据

消融实验揭示了几个对 sim-to-real 转移至关重要的设计选择，这些选择构成了 BeyondMimic 方法的知识贡献：

- **Rot6D 连续旋转表示**：相比四元数或轴角表示，Rot6D 在真实机器人上实现了显著更好的跟踪性能。这一发现与计算机视觉领域的经验一致——连续表示避免了角度空间的非连续性问题。
- **无观测历史**：策略观测中仅使用当前帧信息，不包含历史栈。消融显示加入历史反而降低 sim-to-real 性能，可能因为历史信息在仿真与真实之间的分布偏移放大了域间隙。
- **精确电枢惯量建模**：使用制造商提供的精确反射惯量值对跟踪精度有显著影响。不准确或设为零的电枢值导致仿真中加速度过大和自碰撞，直接破坏 sim-to-real 转移。
- **部署延迟最小化**：通过 C++ 实时框架将单次策略推理优化至 1 毫秒以内。消融显示 2 毫秒延迟即增加速度误差，5 毫秒导致一次失败，10 毫秒在三试中失败两次。这一发现对实际部署具有重要工程指导意义。
- **自适应采样**：在训练过程中根据运动难度动态调整采样权重。消融显示，无自适应采样时 4 个困难运动中有 3 个在 30k 轮次后仍失败；启用后不仅解决所有运动，还将简单运动所需迭代轮次从 4k 降至 2k。

### 适用边界

BeyondMimic 的适用边界由以下几个维度界定：

1. **运动类型**：方法在静态平衡、动态行走/跑步、高敏捷性空翻/旋踢、风格化舞蹈等多样化运动上验证有效。但所有运动均属于全身运动跟踪范畴，未涉及精细物体操控或需要语义推理的社交交互任务。

2. **预测时域**：扩散模型预测窗口仅 0.64 秒（16 步），适合短时域的运动规划与在线修正，但无法处理需要远距离推理的长期规划任务（如提前避障需要数秒的前瞻）。

3. **目标粒度**：引导优化对粗粒度目标（速度命令、航点导航、障碍物回避）效果良好，但对细粒度目标（如精确的脚部着地位置）效果有限，且仍需对引导权重进行轻量手动调节。

4. **硬件平台**：所有实验在 Unitree G1 人形机器人上进行。方法的核心设计（锚点跟踪、统一奖励、扩散引导）原则上可迁移到其他具身平台，但电枢惯量建模和 PD 增益选择需根据具体硬件重新校准。

5. **状态估计依赖**：潜扩散模型依赖于本体感觉状态估计（IMU 速度、关节位置/速度），估计噪声会传播到生成轨迹中，影响引导质量。

### 局限与开放问题

**已识别的局限**：

- **历史依赖与瞬态响应**：模型依赖历史信息以稳定预测，但在引导激活时可能导致陷入重复运动模式。加大引导权重可缓解，但在模式切换或高方差状态下会破坏稳定性，导致运动起始和结束时踉跄。
- **细粒度控制不足**：引导优化对粗粒度目标有效，但对细粒度目标效果有限，仍需手动调节引导权重。
- **硬件限制**：Unitree G1 缺乏脚趾关节，限制了行走时的蹬地推进，导致地面反力峰值更尖锐，与人类的柔顺性仍有差距。
- **异步推理延迟**：扩散模型推理约需 20 毫秒（在移动 GPU 上），与 50Hz 策略控制回路异步运行，对控制稳定性的影响需进一步量化。

**开放问题**：

1. **减少历史依赖**：如何减少或移除对历史的依赖，以提升在引导扩散下的瞬态响应和模式切换鲁棒性？可能的路径包括改进潜空间表示或引入显式的模式切换机制。

2. **细粒度可组合控制**：能否借鉴视觉领域的监督微调或适配器方法，实现细粒度、可组合的轨迹控制而无需大量重新训练或手动调权？RLHF 或偏好优化可能是一条有前景的路径。

3. **异步推理的优化**：扩散模型的异步推理对控制回路稳定性和延迟的影响如何进一步量化与优化？模型蒸馏或更高效的采样策略可能缩短推理时间。

4. **任务类别泛化**：该方法能否泛化到完全新颖的任务类别，如物体操控或需要语义推理的社交交互？这可能需要将扩散模型的条件空间从运动学目标扩展到语义目标。

5. **状态估计质量**：通过传感器融合或学习的估计器提升状态估计质量，能否进一步改善动作质量和引导性能？特别是在高动态运动中，本体感觉估计的噪声可能成为瓶颈。

### 知识库定位

BeyondMimic 在以下知识节点上做出了可验证的贡献：

- **可扩展运动跟踪的奖励设计原则**：证明了仅需三项正则化项即可实现多样化运动的统一学习，为后续工作提供了简洁的基线公式。
- **扩散模型用于测试时运动合成与任务适应**：首次将潜状态‑动作扩散模型的分类器引导用于人形机器人的零样本任务适应，展示了得分函数天然支持条件化的优势。
- **sim-to-real 转移的关键工程因素**：通过系统消融明确了旋转表示、观测历史、电枢惯量、部署延迟对真实机器人部署的影响权重，为后续工作提供了实用的工程指南。

## 原文 PDF

![[paperPDFs/arxiv_2025/BeyondMimic_From_Motion_Tracking_to_Versatile_Humanoid_Control_via_Guided_Diffusion.pdf]]
