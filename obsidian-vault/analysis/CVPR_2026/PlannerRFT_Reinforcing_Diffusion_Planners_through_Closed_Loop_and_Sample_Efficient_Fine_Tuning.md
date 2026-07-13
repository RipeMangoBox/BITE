---
title: "PlannerRFT: Reinforcing Diffusion Planners through Closed-Loop and Sample-Efficient Fine-Tuning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PlannerRFT_Reinforcing_Diffusion_Planners_through_Closed_Loop_and_Sample_Efficient_Fine_Tuning.pdf
project_link: "https://opendrivelab.com/PlannerRFT"
code_link: null
aliases:
- PlannerRFT
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过Policy-Guided Denoising引入可学习的探索策略（Exploration Policy），该策略根据驾驶上下文动态调整横向/纵向引导尺度（η_lat, η_lon），生成多模态且场景自适应的候选轨迹组，从而为GRPO提供高效且稳定的探索信号。
primary_logic: 将分类器引导去噪与可学习的探索策略相结合，使扩散规划器在闭环强化微调中能够自适应探索行为空间，既保持与参考轨迹的一致性，又提供足够的多样性，从而有效利用奖励信号提升闭环安全性和效率。
claims:
- PlannerRFT with policy-guided denoising outperforms uniform, fixed, and unguided exploration in closed-loop performance (Tab. 2).
- Policy-guided denoising improves trajectory diversity D from 5.65 (w/o guidance) to 25.34, with mean reward r¯ increasing from 69.06 to 73.88 (Tab. 2).
- Survival reward formulation with a 4 s horizon gives best performance, outperforming terminal reward (Tab. 4).
- PlannerRFT achieves +2.99 on Test14-hard R and +1.66 on Val14 R over pretrained Diffusion Planner (Tab. 1).
---

# PlannerRFT: Reinforcing Diffusion Planners through Closed-Loop and Sample-Efficient Fine-Tuning

> [!tip] 核心洞察
> 将分类器引导去噪与可学习的探索策略相结合，使扩散规划器在闭环强化微调中能够自适应探索行为空间，既保持与参考轨迹的一致性，又提供足够的多样性，从而有效利用奖励信号提升闭环安全性和效率。

| 字段 | 内容 |
|------|------|
| 中文题名 | PlannerRFT：通过闭环与样本高效微调增强扩散规划器 |
| 英文题名 | PlannerRFT: Reinforcing Diffusion Planners through Closed-Loop and Sample-Efficient Fine-Tuning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.12901) · [Project](https://opendrivelab.com/PlannerRFT) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | PlannerRFT |
| Dataset | Val14, Test14-hard, Test14-random |

> [!tip] 效果简介
> - Val14 (Reactive) 上，nuPlan score 84.46 vs 82.80 (Diffusion Planner) (+1.66)。
> - Test14-hard (Reactive) 上，nuPlan score 72.21 vs 69.22 (Diffusion Planner) (+2.99)。
> - Test14-random (Reactive) 上，nuPlan score 85.80 vs 82.63 (Diffusion Planner DDIM) (+3.17)。

## 概要

自动驾驶规划器从行为克隆（IL）预训练中获得初始能力，但在安全关键场景中仍表现出明显的性能瓶颈。扩散规划器虽然能生成多样化的候选轨迹，但在强化微调（RL fine-tuning）过程中普遍存在**模式崩溃**和**场景不自适应**两大问题：传统去噪过程倾向于生成高度相似的轨迹，导致探索效率低下；而基于锚点的方法虽然增加了多样性，却忽略了驾驶上下文，产生大量与场景无关的噪声候选。这直接限制了闭环性能的提升空间。

PlannerRFT 针对上述瓶颈提出了一个**闭环强化微调框架**，其核心创新在于将可学习的探索策略（Exploration Policy）与分类器引导去噪（classifier-guided denoising）相结合。通过引入横向和纵向的能量函数引导，扩散去噪过程能够在保持与参考轨迹一致性的同时，根据驾驶上下文自适应地调节引导尺度，生成**多模态且场景自适应**的候选轨迹组。这一机制为后续的群相对策略优化（GRPO）提供了高效且稳定的探索信号。

在 nuPlan 闭环规划基准上，PlannerRFT 相较于预训练的 Diffusion Planner 在反应式（Reactive）场景中取得显著提升：Val14 上 nuPlan score 从 82.80 提升至 84.46（+1.66），Test14-hard 上从 69.22 提升至 72.21（+2.99），达到该基准上的领先水平。消融实验证实，策略引导去噪将轨迹多样性从 5.65 提升至 25.34，同时平均奖励从 69.06 提升至 73.88，在探索广度与优化质量之间取得了最佳平衡。定性结果表明，PlannerRFT 能够在行人避让、紧急制动、S 弯换道等安全关键场景中成功避免 IL 预训练模型发生的碰撞。

方法层面，PlannerRFT 属于**扩散规划器的强化微调范式**，与现有基于规则的 PDM-Closed、基于学习的 PlanTF/PLUTO 等方法形成互补。其技术路线融合了分类器引导扩散、策略梯度优化和 GPU 并行仿真三个技术分支，为生成式规划器的闭环自进化提供了新的技术路径。



自动驾驶中的运动规划任务要求系统在高维、多模态的行为空间中做出安全且高效的决策。近年来，扩散模型因其强大的多模态生成能力而被引入规划领域，形成了以 **Diffusion Planner** 为代表的一类生成式规划器。这类方法通过去噪过程从高斯噪声中逐步恢复出符合场景约束的轨迹，在模仿学习（IL）范式下展现出了有竞争力的开环性能。

然而，当扩散规划器被部署到闭环交互环境中时，一个根本性的瓶颈逐渐暴露：**模式崩溃（modality collapse）与场景不自适应**。如图 1(a) 所示，原生扩散规划器在去噪采样时倾向于生成高度集中的轨迹簇，缺乏足够的行为多样性。这使得在强化微调（Reinforcement Fine-Tuning, RFT）过程中，候选轨迹组无法有效覆盖行为空间，导致探索效率低下、优化信号不稳定。另一方面，以 **DiffusionDrive** 为代表的锚点（anchor）方法虽然通过固定锚点噪声引入了多样性，但其探索方向是场景无关的（scenario-agnostic），容易产生与驾驶上下文脱节的噪声交互（图 1(b)），同样难以稳定地利用奖励信号进行策略改进。

上述困境揭示了一个因果性的调控节点：**去噪过程中的探索机制**。若能在保持与参考轨迹一致性的前提下，根据驾驶场景自适应地调节探索的方向和幅度，便可同时获得多模态候选与场景相关性，从而为闭环强化学习提供高效且稳定的探索信号。这正是 PlannerRFT 的核心动机——将分类器引导去噪（classifier-guided denoising）与可学习的探索策略相结合，使扩散规划器在 RFT 中能够自适应地探索行为空间。

此外，闭环 RFT 的规模化部署还面临仿真效率的工程挑战。原生 nuPlan 仿真器的串行架构难以支撑大规模 on-policy rollout 的吞吐需求，这进一步制约了扩散规划器在闭环优化中的样本效率。PlannerRFT 通过引入 GPU 并行的 **nuMax** 仿真器，将仿真速度提升约 10 倍，为闭环 RFT 提供了基础设施支撑。

综上，本文的动机源于一个清晰的因果链条：扩散规划器在闭环 RFT 中因模式崩溃和场景不自适应而无法有效利用奖励信号 → 去噪过程中的探索机制是调控这一瓶颈的关键环节 → 通过可学习的策略引导去噪，有望在保持稳定性的同时注入场景自适应的多模态性，从而显著提升闭环安全性与效率。



## 核心方法与创新机理

PlannerRFT 的核心创新在于将**闭环强化微调**引入扩散规划器，并通过**策略引导去噪**（Policy-Guided Denoising）解决扩散模型在 RL 采样中普遍存在的模式崩溃与场景不自适应问题。相较于预训练的 Diffusion Planner，该方法在四个关键维度上进行了系统性改造：

### 1. 从开环模仿到闭环强化的范式跃迁

扩散规划器传统上依赖行为克隆进行开环训练，无法利用闭环交互中的安全反馈信号。PlannerRFT 首次将群相对策略优化（GRPO）引入扩散 Transformer 的微调，使规划器能在闭环仿真中通过“生成-评估”范式持续改进。这一转变的本质瓶颈在于：标准扩散去噪过程从纯噪声出发，生成的候选轨迹多样性极低（模式崩溃），且与当前驾驶上下文无关，导致 RL 探索效率低下、优化信号不稳定。

### 2. 策略引导去噪：可学习的多模态探索机制

PlannerRFT 的核心技术贡献是**策略引导去噪**，它由三个紧密耦合的组件构成：

- **能量引导去噪**：在 DDIM 去噪的每一步注入横向与纵向能量函数（Eq. 2-3），以分类器引导的方式将轨迹推向参考轨迹附近的偏移位置。这使扩散过程不再是“从噪声到单一解”的确定性映射，而是“从噪声到以参考轨迹为锚点的多模态分布”。

- **可学习探索策略**：引导尺度 $\eta_{\text{lat}}, \eta_{\text{lon}}$ 并非固定值，而是由一个探索策略 $\pi_\phi$ 根据驾驶状态和参考轨迹自适应采样（Eq. 4）。该策略输出 Beta 分布参数，通过 PPO 与 GAE 优化长期闭环回报，使探索行为随场景动态调整——在简单场景保持保守，在安全关键场景增加多样性。

- **参考轨迹锚定**：冻结的 IL 预训练模型提供参考轨迹 $\mathbf{x}^{\text{ref}}$，确保引导去噪始终围绕合理的行为空间展开，避免无引导探索中的随机漂移。

这种设计的因果机制清晰：**探索策略决定“探索多少”，能量引导决定“朝哪个方向探索”，参考轨迹保证“不偏离可行域”**。三者协同使扩散规划器在闭环微调中既能保持与专家轨迹的一致性，又能自适应地探索行为空间的边界，从而有效利用稀疏的碰撞/安全奖励信号。

### 3. 生存奖励：解决稀疏奖励下的信号坍塌

在安全关键场景中，轨迹级终端奖励常因早期碰撞而直接归零，导致 GRPO 无法区分不同候选轨迹的相对优劣。PlannerRFT 引入**生存奖励**（Eq. 6）：仅累积非终止时间步的奖励，并沿时间轴向后截断。这一设计鼓励规划器尽可能推迟失败时刻，即使在最终碰撞的场景中，能“多存活几秒”的轨迹也能获得更高的奖励信号，从而为 GRPO 提供更细粒度的优化梯度。

### 4. 高效闭环仿真基础设施

为支撑大规模 RL 训练，PlannerRFT 构建了 nuMax——基于 JAX 的 GPU 并行仿真器，将 nuPlan 的闭环 rollout 速度提升约 10 倍。nuMax 通过场景预缓存、LQR 跟踪器校准和分布式 RL 通信管道，使策略引导去噪所需的多次采样-评估循环在计算上可行。这一工程创新是方法得以验证的关键使能因素，但本身不构成算法贡献。

### 与 baseline 的差异总结

| 改造维度 | 预训练 Diffusion Planner | PlannerRFT |
|---------|------------------------|-----------|
| 去噪过程 | ODE-based DPMsolver（10 步） | 5-step DDIM + 策略引导能量去噪 |
| 探索机制 | 无显式探索（模式崩溃） | 可学习探索策略（Beta 分布 + PPO） |
| 奖励设计 | 终端奖励（PDMS） | 生存奖励（累积非终止段） |
| 优化算法 | 仅 IL | GRPO（DiT）+ PPO（探索策略） |
| 仿真器 | 原生 nuPlan | nuMax GPU 并行（~10× 加速） |

这些 changed slots 并非独立改进，而是围绕“闭环高效探索”这一核心目标形成的耦合系统：策略引导去噪提供多模态候选轨迹，生存奖励提供细粒度优化信号，GRPO+PPO 双支优化分别调整轨迹分布和探索行为，nuMax 提供计算可行性保障。消融实验（Table 2）表明，移除策略引导（无引导/均匀/固定探索）会导致轨迹多样性-性能的失衡，验证了各组件间的强耦合关系。



PlannerRFT 围绕 **闭环强化微调** 这一核心目标，将扩散规划器从纯模仿学习范式提升为可在线自我优化的策略。整个 pipeline 由三个关键阶段串联而成：**引导去噪采样**、**闭环仿真评估**与**双分支策略优化**，它们构成一个完整的生成–评估–优化循环（Figure 2）。

![[assets/figures/papers/paper_list_l912_https_arxiv_org_abs_2601_12901/figures/002_Figure_2.jpg]]
*Figure 2: Overview of PlannerRFT. We enhance multi-modality during RL sampling through Guided Denoising, with guidance scales modulated by the Exploration Policy to generate scenario-adaptive trajectories (Sec. 4.2). The planner gathers on-policy interaction data through Closed-Loop Rollout in simulation (Sec. 4.3). A dual-branch optimization framework performs Trajectory Optimization and Exploration Optimization to steer the denoising process (Sec. 4.4)*

### 模块组成与数据流

1. **参考规划器（Reference Planner）**  
   一个冻结的 IL 预训练扩散规划器（基于 **Diffusion Planner**），负责为每个驾驶场景生成一条参考轨迹 $\mathbf{x}^{\mathrm{ref}}$。该轨迹作为后续探索的“锚点”，在保证基本安全性的前提下约束偏移范围。

2. **探索策略（Exploration Policy）**  
   一个可学习的策略网络 $\pi_{\phi}$，输入驾驶上下文 $\mathbf{s}$ 和参考轨迹 $\mathbf{x}^{\mathrm{ref}}$，输出一对引导尺度 $(\eta_{\mathrm{lat.}}, \eta_{\mathrm{lon.}})$，分别控制横向偏移与纵向速度调节的幅度。该策略通过 Beta 分布建模，使采样既具随机性又保持场景自适应性。

3. **引导去噪（Guided Denoising）**  
   在扩散 Transformer（DiT）的 5 步 DDIM 去噪过程中，注入基于能量函数的分类器引导。具体而言，横向能量 $\Psi_{\mathrm{lat.}}$ 与纵向能量 $\Psi_{\mathrm{lon.}}$ 通过梯度 $\nabla_{\mathbf{x}} \log p(\eta \mid \mathbf{x})$ 将轨迹拉向满足 $\eta$ 所指定的偏移目标，从而在保持与参考轨迹一致性的同时，生成多模态、场景自适应的候选轨迹组。

4. **闭环仿真器（nuMax）**  
   基于 JAX 的 GPU 并行仿真器，支持高速 rollout。nuMax 从预处理场景缓存中加载 nuPlan 场景，通过 LQR 跟踪器执行规划轨迹，并计算闭环奖励。其仿真速度可达原生 nuPlan 的 **10 倍**，为大规模 RL 训练提供算力基础。

5. **双分支优化器**  
   - **GRPO 轨迹优化**：利用候选轨迹组在仿真中获得的相对奖励，更新 DiT 参数 $\theta$，使模型倾向于生成高奖励轨迹。奖励函数采用 **生存奖励（survival reward）** 设计，仅累积非终止步的奖励，避免困难场景中的零奖励坍塌。  
   - **PPO 探索优化**：基于长期闭环回报，通过 GAE 更新探索策略 $\pi_{\phi}$，使其学会在不同场景下自适应地调节引导尺度，最大化探索效率。

### 训练流程

每次迭代中，探索策略为一批场景采样 $\eta$，经引导去噪生成候选轨迹组；nuMax 并行执行闭环仿真并返回奖励；GRPO 与 PPO 分别利用这些奖励信号更新轨迹生成器和探索策略。这一闭环设计使 PlannerRFT 能够持续从交互数据中学习，逐步提升在反应式交通中的安全性与通行效率。

> **注意**：nuMax 当前使用 log-replay 而非 IDM 反应式交通模型，这可能降低交互仿真的真实度；在高度反应式场景中部署时需考虑该差异。

### 补充图表

![[assets/figures/papers/paper_list_l912_https_arxiv_org_abs_2601_12901/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of nuMax. (a) Scenario cache: nuPlan scenarios are preprocessed and cached for fast loading during largescale RL rollouts; (b) LQR tracker and scorer: vehicle kinematics and reward computation are calibrated to match nuPlan; and (c) Distributed RL training pipeline: enables communication between PyTorch DistributedDataParallel (DDP) workers and the JAX-based simulator*



PlannerRFT 的核心技术架构围绕**策略引导去噪（Policy-Guided Denoising）** 展开，由以下关键模块协同构成。

### 1. 扩散Transformer去噪器（DiT Denoiser）

预训练的扩散规划器以噪声轨迹样本 $\mathbf{x}^k$、场景嵌入 $F_{\mathrm{scene}}$、导航嵌入 $F_{\mathrm{navi}}$ 和扩散时间步 $t$ 为条件，预测干净轨迹：

$$
\hat{\mathbf{x}}_0^k = \mathrm{DiT}_\theta\left(\mathrm{MLP}(\mathbf{x}^k); F_{\mathrm{scene}}; F_{\mathrm{navi}}; t\right) \tag{1}
$$

该模块是轨迹生成的基础骨架，在强化微调阶段保持冻结的参考规划器（Reference Planner）同样基于此架构，用于提供参考轨迹以稳定探索。

### 2. 策略引导去噪（Policy-Guided Denoising）

为解决扩散规划器在强化微调中的**模式崩溃（modality collapse）** 和**场景不自适应**问题，PlannerRFT 引入基于能量的分类器引导，将残差偏移注入去噪过程。引导能量分解为横向与纵向两个分量。

**横向引导能量**控制轨迹相对于参考线的侧向偏移：

$$
\Psi_{\mathrm{lat.}} = \frac{1}{T} \sum_{\tau=1}^{T} \left( \mathbf{n}_{\tau}^{\perp} \left( \mathbf{x}_{\tau} - \mathbf{x}_{\tau}^{\mathrm{ref}} \right) - \lambda_{\mathrm{lat.}} \eta_{\mathrm{lat.}} \right)^{2} \tag{2}
$$

其中 $\mathbf{n}_{\tau}^{\perp}$ 为参考轨迹点的横向法向量，$\mathbf{x}_{\tau}^{\mathrm{ref}}$ 为参考轨迹点，$\lambda_{\mathrm{lat.}}$ 为最大引导偏移量，$\eta_{\mathrm{lat.}}$ 为探索策略输出的横向引导尺度。

**纵向引导能量**调节规划速度与参考速度的偏差：

$$
\Psi_{\mathrm{lon.}} = \frac{1}{T} \sum_{\tau=1}^{T} \left( \mathbf{n}_{\tau}^{\parallel} ( \mathbf{v}_{\tau} - \lambda_{\mathrm{lon.}} \eta_{\mathrm{lon.}} \mathbf{v}_{\tau}^{\mathrm{ref}} ) \right)^{2} \tag{3}
$$

其中 $\mathbf{n}_{\tau}^{\parallel}$ 为参考轨迹点的纵向切向量，$\mathbf{v}_{\tau}^{\mathrm{ref}}$ 为参考速度，$\lambda_{\mathrm{lon.}}$ 和 $\eta_{\mathrm{lon.}}$ 分别为纵向最大偏移和引导尺度。

### 3. 探索策略（Exploration Policy）

探索策略 $\pi_{\phi}$ 根据驾驶上下文动态调节引导尺度 $\eta = (\eta_{\mathrm{lat.}}, \eta_{\mathrm{lon.}})$：

$$
\eta \sim \pi_{\phi}( \cdot \mid \mathbf{s}, \mathbf{x}^{\mathrm{ref}} ) \tag{4}
$$

其中 $\mathbf{s}$ 为当前驾驶状态，$\mathbf{x}^{\mathrm{ref}}$ 为参考轨迹。探索策略输出 Beta 分布的参数，使引导尺度在 $(0,1)$ 范围内自适应变化——在安全区域增大探索，在危险区域缩小探索以保持与参考轨迹的一致性。

### 4. 分类器引导的去噪梯度

在每一去噪步中，引导信号通过能量函数的负梯度注入：

$$
\nabla_{\mathbf{x}} \log p(\eta | \mathbf{x}) \approx -\nabla_{\mathbf{x}} \left[ \Psi_{\mathrm{lat.}}(\mathbf{x}; \eta_{\mathrm{lat.}}) + \Psi_{\mathrm{lon.}}(\mathbf{x}; \eta_{\mathrm{lon.}}) \right] \tag{5}
$$

该梯度引导去噪过程向满足横向/纵向偏移约束的方向演化，使生成的候选轨迹既保持多模态性，又与场景上下文自适应匹配。

### 5. 生存奖励（Survival Reward）

为解决困难场景中因早期碰撞导致的零奖励崩溃问题，PlannerRFT 采用生存奖励公式：

$$
R_{\mathrm{surv}} = \frac{1}{T_{r}} \sum_{\tau=1}^{T_{r}} R_{\tau}^{\mathrm{term}} \prod_{j=1}^{\tau} \mathbb{I}[R_{j}^{\mathrm{term}} \neq 0] \tag{6}
$$

该公式仅累积非终止步的轨迹级奖励——一旦发生终止事件（如碰撞），后续时间步的奖励不再计入。消融实验表明，4 秒奖励时域配置下生存奖励表现最优（Table 4），其核心机制在于鼓励规划器推迟失败时刻，从而为 GRPO 提供更稳定的优化信号。

### 6. 双分支优化框架

- **轨迹优化**：采用 GRPO（Group Relative Policy Optimization）微调 DiT 的轨迹分布，组大小 8 在性能与计算成本间取得最优平衡（Table A5）。
- **探索优化**：采用 PPO 结合 GAE 优化探索策略的长期回报，使 $\eta$ 的采样分布随训练逐步收敛至高效探索区域。

### 补充图表

![[assets/figures/papers/paper_list_l912_https_arxiv_org_abs_2601_12901/figures/007_Figure_5.jpg]]
*Figure 5: Visualization of Different Exploration Policies. (a) Without guidance: denoising from random noise. (b) Uniform exploration policy*



## 实验与关键发现

### 核心实验设置

PlannerRFT 以 **Diffusion Planner**作为 IL 预训练基座，在 nuPlan 数据集 100 万片段上完成模仿学习。为适配强化微调的采样效率需求，作者将原 ODE-based DPMsolver（10 步）替换为 **5 步 DDIM 采样器**，并在自研的 **nuMax GPU 并行仿真器**（宣称 10× 加速）中执行闭环 rollout。微调阶段采用双支路优化：DiT 轨迹分布通过 **GRPO** 更新，探索策略通过 **PPO + GAE** 更新。训练数据选择碰撞或低分场景（Lt90），而非全部数据或仅失败场景——后者在消融中被证实会导致常规场景严重退化（Table 3）。

![[assets/figures/papers/paper_list_l912_https_arxiv_org_abs_2601_12901/figures/008_Table_3.jpg]]
*Table 3: Ablations of fine-tuning data distribution*

### 主要结果

**Table 1** 汇总了 PlannerRFT 在 nuPlan 四个闭环基准上的表现。在反应式交通设定下，PlannerRFT 相较预训练 Diffusion Planner 取得显著提升：Val14 Reactive 上 **+1.66**（84.46 vs. 82.80），Test14-hard Reactive 上 **+2.99**（72.21 vs. 69.22）。在非反应式设定下提升幅度收窄：Val14 Non-reactive 仅 **+0.09**，Test14-hard Non-reactive 为 **+1.17**——作者将这一差异归因于非反应式环境的分布偏差。在 Test14-random Reactive 上，PlannerRFT 达到 **85.80**，较 Diffusion Planner DDIM 提升 **+3.17**（Table A3）。

横向对比中，PlannerRFT 在四个基准中的三个取得最优，超越 **PDM-Closed**（rule-based）、**GameFormer**、**PlanTF**、**PLUTO** 等学习型方法以及 **Flow Planner** 等生成式规划器。

### 探索策略消融

探索策略是 PlannerRFT 的核心设计。**Table 2** 系统对比了四种探索范式：

![[assets/figures/papers/paper_list_l912_https_arxiv_org_abs_2601_12901/figures/006_Table_2.jpg]]
*Table 2: Ablation on Exploration Policy. IL Pretrain*

| 探索策略 | 多样性 D ↑ | 平均奖励 r̄ ↑ | R-score ↑ |
|----------|-----------|-------------|----------|
| 无引导（随机噪声去噪） | 5.65 | 69.06 | 68.18 |
| 均匀探索 | **39.78** | 65.82 | 65.82 |
| 固定 Beta 探索 | 25.34 | 73.88 | 72.21 |
| **策略引导探索（PlannerRFT）** | 25.34 | **73.88** | **72.21** |

关键发现：
- **无引导**去噪导致严重的模式崩溃，轨迹多样性仅 5.65，探索效率极低。
- **均匀探索**虽获得最高多样性（39.78），但大量候选轨迹与场景无关，平均奖励和 R-score 反而最差——这印证了“多样性≠有效探索”的核心洞察。
- **策略引导探索**在多样性与场景自适应性之间取得最优平衡：多样性从 5.65 跃升至 25.34，平均奖励从 69.06 提升至 73.88。

**Figure 6** 从训练动态角度进一步验证：策略引导探索在所有安全指标（Score、NC、DAC、TTC）上均保持最高且最稳定的收敛曲线，固定探索次之，均匀探索和无引导探索则波动剧烈且终值显著偏低。

### 奖励设计与预测时长消融

**Table 4** 消融了 GRPO 奖励类型与预测时长。核心结论：
- **Survival reward**（式 6）在所有设定下均优于 terminal reward，验证了“仅累积非终止步奖励”对延迟失败时刻的有效激励。
- 预测时长 **4 s** 达到最优 R-score，短于或长于此窗口均导致性能下降——过短缺乏前瞻性，过长则引入噪声和不确定性。

### 引导分量与偏移范围消融

**Table A4** 拆分了横向引导与纵向引导的贡献：单独使用横向或纵向引导均可带来增益，但**二者联合**取得最佳 R-score 72.21，表明横纵向引导具有互补效应。

**Table 5** 消融了最大引导偏移 λ 的取值。λ 过小限制探索空间，过大则使候选轨迹偏离参考线过远、引入不安全行为。实验在 Test14-hard Reactive 上确定了最优 λ 配置。

### 微调数据分布消融

**Table 3** 表明数据分布选择对微调效果至关重要：
- 仅使用**碰撞场景（Fail）**训练会导致模型在常规场景上严重退化，说明灾难性遗忘风险显著。
- 使用**碰撞+低分场景（Lt90）**取得最佳性能，在安全关键场景与常规场景之间保持了良好平衡。
- 使用**全部数据（All）**虽未退化，但效率低于 Lt90，说明针对性采样更为高效。

### GRPO 组规模消融

**Table A5** 在 Test14-random 上消融 GRPO group size。组规模 8 在性能与计算开销之间达到最优平衡：更小的组（4）探索不足，更大的组（16）边际收益递减且显著增加仿真成本。

### 定性分析

**Figure 4** 展示了预训练规划器与 RFT 规划器在 OOD 场景中的轨迹对比：预训练模型在分布外场景下产生不安全轨迹，而 RFT 模型通过强化微调学会了更安全的决策。**Figure 5** 可视化不同探索策略生成的轨迹组：策略引导探索产生的候选轨迹既保持多模态，又与驾驶上下文高度相关；均匀探索则产生大量无意义偏移。

安全关键场景的定性结果进一步支撑定量结论：
- **行人避让**（Figure A4）：预训练规划器在 7.5 s 与行人碰撞，PlannerRFT 等待行人通过后安全右转。
- **紧急制动**（Figure A5）：预训练规划器未能及时刹车与前车碰撞，PlannerRFT 在 1 s 检测到静止前车并制动。
- **S 弯换道**（Figure A6）与**锥桶穿行**（Figure A7）：PlannerRFT 在复杂几何约束下实现精细轨迹调整，成功规避障碍物。

![[assets/figures/papers/paper_list_l912_https_arxiv_org_abs_2601_12901/figures/019_Figure.jpg]]
*Figure: A4. Intersection Pedestrian Avoidance. The ego vehicle intends to make a right turn at an intersection while pedestrians are crossing. (a) The IL Pretrained planner collision with a pedestrian at t _ ${ \mathrm { s i m } } = 7$ . 5 ~ s . (b) PlannerRFT waits for all pedestrians to finish crossing and then proceeds with the right turn. In each frame shot, the simulation position and planning trajectory are marked as orange, the ground-truth position and ground-truth trajectory recorded in the driving log are marked as gray and blue, respectively. Surrounding vehicles are marked as black rectangles with white arrows indicating heading. The pedestrians are marked as purple, and the static object...*

### 失败模式与局限性

1. **非反应式环境增益有限**：Val14 Non-reactive 仅提升 0.09，表明 PlannerRFT 的探索机制高度依赖反应式交互信号，在静态交通中优势无法充分发挥。
2. **仿真交互保真度受限**：nuMax 沿用 log-replay 而非 IDM 反应式交通，周围车辆行为缺乏对自车动作的反馈，可能高估某些交互场景下的安全性。
3. **灾难性遗忘风险**：仅用碰撞场景微调会导致常规场景严重退化（Table 3），需精心设计数据分布。
4. **视觉规划器泛化未验证**：当前工作聚焦于特权场景信息的轨迹级规划器，在相机输入的视觉运动规划器上的适用性仍是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l912_https_arxiv_org_abs_2601_12901/figures/005_Table_1.jpg]]
*Table 1: Closed-loop Planning Results on nuPlan Dataset. The highest and the second-best results of each benchmark are denoted by bold and underline*

![[assets/figures/papers/paper_list_l912_https_arxiv_org_abs_2601_12901/figures/009_Table_4.jpg]]
*Table 4: Ablations of the GRPO reward type and reward horizon*

![[assets/figures/papers/paper_list_l912_https_arxiv_org_abs_2601_12901/figures/010_Table_5.jpg]]
*Table 5: Ablations of the maximum guidance offset λ on the Test14-hard Reactive benchmark*

![[assets/figures/papers/paper_list_l912_https_arxiv_org_abs_2601_12901/figures/011_Figure_6.jpg]]
*Figure 6: Closed-loop performance of safety metrics during training under different exploration policy. Score denotes the nuPlan aggregate score, NC refers to No at-fault Collisions, DAC represents Drivable Area Compliance, and TTC indicates Time-to-Collision. Our adaptive exploration policy achieves consistently higher performance and stability across all metrics compared to fixed, uniform, and unguided exploration baselines*

![[assets/figures/papers/paper_list_l912_https_arxiv_org_abs_2601_12901/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative Comparison of Pretrained Planner and RFT Planner. In each frame shot, the simulation position and planning trajectory are marked as orange, the ground-truth position and ground-truth trajectory recorded in the driving log are marked as gray and blue, respectively*

![[assets/figures/papers/paper_list_l912_https_arxiv_org_abs_2601_12901/figures/016_Table.jpg]]
*Table: A3. Closed-loop Planning Results on nuPlan Val14, Test14-hard, and Test14 benchmarks. “Diffusion PlannerDPM” employs the official 10-step DPM-solver. “Diffusion PlannerDDIM” employs a 5-step DDIM sampler, identical to that used in PlannerRFT. Table A4. Ablation on Guidance Type. Results are reported on the Test14-random reactive benchmark*



## 定位与知识库关联

### 1. 在扩散规划器谱系中的位置

PlannerRFT 直接建立在 **Diffusion Planner**（Zheng et al., 2025）之上，后者是一种基于扩散 Transformer（DiT）的生成式轨迹规划器，采用 ODE-based DPMsolver（10 步）进行去噪采样。PlannerRFT 保留了 Diffusion Planner 的场景编码器与 DiT 轨迹生成器架构，但对其采样与优化范式进行了根本性改造：

- **去噪过程替换**：将 DPMsolver 替换为 5 步 DDIM 采样器，并在去噪过程中注入基于能量函数的分类器引导，形成 policy-guided denoising（Sec. 4.2, Eq. 2–5）。这一改动使原本“从随机噪声出发”的单模态采样转变为“以参考轨迹为锚点、横向/纵向可偏移”的多模态采样。
- **从 IL 到 RL 的范式升级**：Diffusion Planner 仅通过模仿学习（IL）预训练，缺乏闭环交互优化能力。PlannerRFT 引入 GRPO（Group Relative Policy Optimization）对 DiT 进行强化微调，同时用 PPO 优化一个独立的探索策略（Exploration Policy），形成双支路优化框架（Sec. 4.4）。

与另一类扩散规划范式——**anchor-based 方法**（如 **DiffusionDrive**, Zhou et al., 2025）——相比，PlannerRFT 的策略引导去噪具有本质区别。Anchor-based 方法在去噪时注入场景无关的锚点噪声（anchor noises），导致候选轨迹缺乏场景自适应性，产生“噪声交互”（Figure 1b）。PlannerRFT 的探索策略则根据驾驶上下文动态调节横向/纵向引导尺度 $(\eta_{\text{lat}}, \eta_{\text{lon}})$，使采样既保持与参考轨迹的一致性，又提供足够的场景自适应多样性（Figure 1c）。

### 2. 与主流闭环规划方法的关系

在 nuPlan 闭环规划基准上，PlannerRFT 与以下代表性方法形成对比：

| 方法 | 类型 | 核心机制 | 局限性（PlannerRFT 视角） |
|------|------|----------|--------------------------|
| **IDM** | 规则式 | 智能驾驶员模型 | 缺乏场景理解，泛化能力弱 |
| **PDM-Closed** | 规则式 | 基于提议的决策-运动规划 | 依赖手工设计的轨迹提议 |
| **PDM-Open** | 学习式 | 开环模仿学习 | 无闭环反馈，分布偏移敏感 |
| **GameFormer** | 学习式 | 博弈论交互建模 | 未针对闭环 RL 微调 |
| **PlanTF** | 学习式 | Transformer 规划 | 开环训练，闭环表现受限 |
| **PLUTO** | 学习式 | 端到端规划 | 未引入强化微调机制 |
| **Diffusion Planner** | 生成式 | DiT + DPMsolver 去噪 | 模式崩溃，闭环探索效率低 |
| **Flow Planner** | 生成式 | 流匹配规划 | 未探索 RL 微调路径 |

PlannerRFT 的核心区分点在于：它是首个将**闭环强化微调**与**策略引导去噪**相结合的扩散规划框架。在 Test14-hard Reactive 基准上，PlannerRFT 达到 72.21 R-score，较 Diffusion Planner 提升 +2.99，较 IL Pretrain DDIM 提升 +4.03（Table 1, Table 2），验证了 RL 微调与自适应探索的叠加收益。

### 3. 适用边界与关键局限

**适用前提**：
- PlannerRFT 当前聚焦于**基于特权场景信息（privileged scene information）的轨迹级规划器**，即场景编码器直接访问 nuPlan 的真值感知数据，而非从原始传感器（相机/LiDAR）中提取特征。
- 强化微调依赖于**闭环仿真器**进行 on-policy rollout；本文使用自研的 nuMax GPU 并行仿真器（10× 加速），该仿真器校准了 LQR 跟踪器和 nuPlan 评分器，但周围交通仍为 log-replay 而非反应式 IDM 模型。

**已识别的局限**：
1. **视觉-运动端到端泛化未验证**：PlannerRFT 在视觉规划器（visuomotor planner）上的适用性尚未探索。作者将此列为未来工作方向。
2. **仿真交互保真度受限**：nuMax 继承 XLA 静态形状约束，更换输入表示需额外后处理；同时，log-replay 交通无法模拟反应式交互（如周围车辆对自车行为的动态响应），可能降低 RL 训练中交互信号的真实度。
3. **非反应式环境提升微弱**：在 Val14 Non-reactive 基准上，PlannerRFT 仅较 Diffusion Planner 提升 +0.09（Table 1），说明在分布内、无交互场景中，RL 微调的边际收益有限，存在训练-测试分布偏差。
4. **训练数据分布敏感**：仅使用碰撞场景（Fail）进行微调会导致模型在常规场景上严重退化（Table 3），表明微调数据构成需要精心设计（本文采用 Lt90，即碰撞+低分场景）。

### 4. 开放问题

1. **跨模态泛化**：PlannerRFT 的策略引导去噪机制能否泛化至基于相机输入的视觉运动规划器？这需要解决视觉编码器与 RL 训练的联合优化问题。
2. **反应式交通仿真**：如何在 nuMax 中高效集成反应式 IDM 交通模型，以提升交互保真度而不显著牺牲仿真吞吐量？
3. **自适应超参数**：引导偏移 $\lambda_{\text{lat}}, \lambda_{\text{lon}}$（Table 5 消融显示最优值分别为 2.0 和 1.5）和微调数据构成目前依赖人工调参。是否可以通过元学习或自动调参方法实现场景自适应调节？
4. **探索策略的进一步优化**：当前探索策略输出 Beta 分布参数，是否可以通过更丰富的动作空间（如时变引导尺度、多模态混合分布）进一步提升探索效率？
5. **与其他 RL 算法的兼容性**：PlannerRFT 采用 GRPO + PPO 双支路优化，是否可以从 PPO 切换到其他策略梯度方法（如 SAC、TD3）以获得更好的样本效率或稳定性？



## 原文 PDF

![[paperPDFs/CVPR_2026/PlannerRFT_Reinforcing_Diffusion_Planners_through_Closed_Loop_and_Sample_Efficient_Fine_Tuning.pdf]]
