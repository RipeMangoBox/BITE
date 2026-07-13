---
title: "Abstracting Robot Manipulation Skills via Mixture-of-Experts Diffusion Policies"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Abstracting_Robot_Manipulation_Skills_via_Mixture_of_Experts_Diffusion_Policies.pdf
project_link: null
code_link: null
aliases:
- SSMEP
- ARMSMEDP
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "引入状态自适应的正交技能基和粘性路由，将动作分解为少量、可复用的技能分量，并基于变分目标联合训练基、门控和系数扩散模型，实现推理时的自适应专家激活。"
primary_logic: "通过将动作空间局部白化投影到正交技能基底，并用慢变门控控制技能组合，SMP学习到可解耦、可迁移的动作基元，在不同任务间复用技能，从而以较低的活跃参数量和推理延迟取得高成功率。"
claims:
- "SMP explicitly abstracts reusable manipulation skills via a state-dependent orthonormal action basis with sticky routing."
- "Adaptive expert activation dynamically selects a compact subset of experts at inference time, reducing computational cost."
- "Multi-task learning success rate on RoboTwin-2 is 0.54 (SMP) vs 0.41 (Sparse DP), and on RLBench-2 is 0.18 vs 0.14."
- "Ablation: removing sticky gate drops RoboTwin-2 success from 0.54 to 0.44, and using fixed skill basis drops to 0.40."
---

# Abstracting Robot Manipulation Skills via Mixture-of-Experts Diffusion Policies

> [!tip] 核心洞察
> 通过将动作空间局部白化投影到正交技能基底，并用慢变门控控制技能组合，SMP学习到可解耦、可迁移的动作基元，在不同任务间复用技能，从而以较低的活跃参数量和推理延迟取得高成功率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于混合专家扩散策略的机器人操作技能抽象 |
| 英文题名 | Abstracting Robot Manipulation Skills via Mixture-of-Experts Diffusion Policies |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=VSWjHIveqZ) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | SMP (Skill Mixture-of-Experts Policy) |
| Dataset | RoboTwin-2 (multi-task learning), RLBench-2 (multi-task learning), RoboTwin-2 (inference efficiency), Few-shot transfer learning |

> [!tip] 效果简介
> - RoboTwin-2 (multi-task learning) 上，平均成功率 为 0.54，对比 0.41 (Sparse DP)，变化 +0.13。
> - RLBench-2 (multi-task learning) 上，平均成功率 为 0.18，对比 0.14 (Disc. Policy / Sparse DP)，变化 +0.04。
> - RoboTwin-2 (inference efficiency) 上，推理时间 (ms) 为 107.3 (80.2M active params)，对比 94.8 (ACT, 83.9M), 120 (DP, 252.5M), 134.4 (Sparse DP, 260.1M)，变化 比Sparse DP快27 ms，比DP快13 ms。

## 概要

将扩散策略扩展到多任务场景时，模型规模和推理成本急剧上升，传统的混合专家（MoE）方法未能显式解耦可复用的操作技能，导致技能纠缠且跨任务迁移能力不足。针对这一瓶颈，本文提出 **SMP（Skill Mixture-of-Experts Policy）**——一种基于混合专家扩散的技能抽象策略。其核心创新在于引入**状态自适应的正交技能基**和**粘性路由**，将动作显式分解为少量可复用的技能分量，并通过变分推断联合优化基、门控和系数扩散模型，实现推理时的自适应专家激活。

SMP 将动作建模为 $a_t = B(g_t \odot z_t)$，其中 $B$ 是通过可微薄 QR 分解构造的状态依赖正交基，$g_t$ 由具有粘性的 Dirichlet‑Markov 门控过程产生，$z_t$ 为扩散系数。这一设计使得动作空间被投影到可解耦的技能基底上，而门控的时间粘性和全局使用正则化进一步促使技能呈分段常数、相位一致的激活模式，从而在不同任务间复用技能基元，并以较低的活跃参数量获得高效的动作生成。

实验上，SMP 在双臂多任务学习基准 **RoboTwin‑2** 和 **RLBench‑2** 上分别取得 **0.54** 和 **0.18** 的平均成功率，远超 Sparse DP（0.41 / 0.14）等强基线；同时其推理延迟仅为 **107.3 ms**，活跃参数量仅 **80.2M**，比同等参数规模的扩散策略快 13 ms 且成功率更高。在少样本迁移和技能组合任务中，SMP 同样以 **0.38** 和 **0.30** 的平均成功率领先基线，表明其习得的技能基元具有良好的可迁移性和组合性。多项消融实验进一步证实：去除粘性门控或使用固定技能基会使成功率分别下降至 0.44 和 0.40，而采用 PCA 全局基甚至跌至 0.32，从而验证了状态自适应正交基与粘性路由的必要性。

当前方法主要针对双臂操作任务评估，尚未在单臂或移动操作等更广泛的设置中测试；真实机器人实验规模也较小，总参数量（258.9M）对内存仍有较高需求。尽管如此，SMP 为扩散策略的高效多任务扩展提供了一种技能解耦与稀疏激活的统一框架，其显式的技能抽象机制对后续的跨任务泛化和与大规模视觉‑语言‑动作预训练的结合具有参考价值。

将扩散策略（Diffusion Policy）用于机器人操作已经在单任务设定中展现出强大的表现力，但将其扩展到多任务学习时，模型容量与推理成本之间的矛盾迅速激化。若简单地放大扩散模型的参数量以覆盖多个任务，每一步去噪推理需要在全部参数上完成完整的前向传播，导致墙上推理时间大幅增加，难以满足实时控制的要求。目前主要存在两条应对路线：一是沿用大参数量但采用稀疏门控的混合专家（Mixture‑of‑Experts, MoE）架构，让每步只激活部分专家以压缩计算；二是基于向量量化（VQ‑VAE）学习离散技能码本。然而，这些方法大多**没有对技能进行显式的结构化解耦**：专家的输出空间未经约束，不同技能的行为模式容易纠缠在一起，导致学习到的成分难以在不同任务间复用，迁移能力有限。以典型的 MoE 基线 Sparse DP 为例，尽管其总参数量高达 260 M，在多任务学习场景下平均成功率仍明显不足，且活跃参数量并未得到有效控制，推理延迟也较高。

上述瓶颈的核心在于：面对多任务操作，模型既需要大容量来容纳多样化的行为，又必须能够将行为分解为少量、稳定、可复用的“技能原子”。现有的门控策略（如前馈路由）缺乏时间结构先验，容易产生高频的专家切换，破坏技能的一致性；而直接在该未约束空间上训练专家会导致技能相互干扰，无法获得干净解耦的动作基元。

针对这一缺口，本文提出 **Skill Mixture‑of‑Experts Policy (SMP)**。SMP 的核心动机是：**将动作空间投影到一个状态自适应的正交技能基底上，并用具有时间粘性的门控控制技能的组合**，从而显式地抽象出可复用的操作技能。具体而言，SMP 维护一个状态依赖的正交矩阵 $B(s)$（满足 $B^\top B = I_K$），并将其列向量视为一组可解释的“技能方向”。动作通过 $a_t = B(s)\,(g_t \odot z_t)$ 解码，其中 $g_t$ 为路由器给出的技能权重，$z_t$ 为扩散模型在系数空间中去噪得到的技能系数。这种设计将多个专家的输出白化到一个共享的、解耦的系数空间，迫使不同专家对应于相互正交的行为模式，从而**抑制技能纠缠**。同时，SMP 引入一阶 Dirichlet–Markov 先验来描述 $g_t$ 的演化，使门控具有粘性（stickiness），倾向于保持分段常数并跨时间步维持相移一致，这进一步将行为组织为具备明确语义的“技能段落”，并促进跨任务的技能复用。

除了显式的技能抽象，SMP 还设计了**自适应专家激活策略**：推理时不再固定激活所有专家，而是根据平滑后的门控质量 $m_i = \bar{g}_{t,i}^2$ 动态选择一个紧凑的专家子集。这使得在保持动作采样精度的前提下，活跃参数量和单步推理延迟大幅降低。整体动机可以概括为：通过状态自适应的正交技能基、粘性路由以及基于变分下界（ELBO）的端到端训练，SMP 旨在以较低的活跃计算代价，学习到可解耦、可迁移的动作基元，从而在多任务操作中取得高成功率，同时保持高效的推理性能。

## 核心方法与创新机理

SMP 的核心瓶颈，在于将扩散策略扩展到多任务场景时，模型容量与推理开销急剧膨胀，而传统的 MoE 路由（如前馈门控）并未显式解耦可复用技能，导致技能纠缠、可迁移性差。论文通过引入**状态自适应正交技能基**与**粘性路由**两个因果性的设计把手，将动作空间局部白化投影到一组正交的基向量上，并用慢变门控控制技能组合，从而学习到可解耦、可迁移的动作基元，在不同任务间复用技能。

围绕这一洞察，SMP 在以下四个维度上对基线方法进行了系统性改造（changed slots），并有明确的消融证据支撑。

### 1. 技能基构造：从全局专家输出到状态自适应正交基
基线方法（DP、Sparse DP 等）的专家输出在全局无约束空间中混合，缺乏结构化的技能分离。SMP 引入 **Skill‑Basis Network**，通过可微分的 thin‑QR 分解与符号稳定化（sign stabilization），将未约束矩阵投影到 Stiefel 流形，得到状态依赖的正交基 $\mathbf{B}(\mathbf{s}),\ \mathbf{B}^\top\mathbf{B}=\mathbf{I}_K$。这一构造使不同技能分量在几何上正交，强制解耦。消融显示：若替换为**固定技能基**，RoboTwin‑2 成功率从 0.54 降至 0.40；若替换为**全局 PCA 基**，进一步骤降至 0.32，充分说明状态自适应正交基是性能的关键。

### 2. 门控机制：从无时间结构的简单路由到粘性 Dirichlet‑Markov 门控
传统 MoE 门控多为每步独立的前馈路由器，技能激活频繁切换、缺乏相位一致性。SMP 改用**粘性 Dirichlet‑Markov 动态**：门控向量服从 Dirichlet 分布，并通过一阶马尔可夫过程引入时间粘性 $\kappa$ 和全局使用先验 $\vartheta$，同时利用变分后验进行 KL 正则化。这一设计使门控权重呈现分段常数、相位一致的模式，仅少数专家被稀疏激活，且跨任务复用同一组基元（详见 Figure 3 的门控迹线）。**去除粘性门控**直接导致成功率从 0.54 降至 0.44，证实了时间一致性和全局使用约束的必要性。

### 3. 训练目标：从单纯的动作重建 ELBO 到联合生成目标
SMP 的训练目标不再只是动作空间的扩散 ELBO，而是扩展为一个变分 ELBO，同时优化**白化系数空间的重构误差**、**门控与全局使用的 KL 正则**（$\mathcal{L}_{gate}$）和**系数扩散损失**（$\mathcal{L}_{coeff}$）。尤为关键的是，论文采用**双目标系数构造**：stop‑gradient 版本用于系数扩散损失以稳定训练，梯度携流版本用于重构损失以更新基 $\mathbf{B}$ 和门控。此外，训练时还引入一个**状态‑仅路由器对齐损失** $\mathcal{L}_{align}$，将动作条件后验与状态先验对齐，提升测试时的路由一致性。这些设计共同促使基的更新与技能系数的生成在训练中相互促进而非冲突。

### 4. 推理激活：从全专家激活到自适应专家选择
MoE 若不控制，推理时仍需计算所有专家，计算量与参数量依旧庞大。SMP 提出**自适应专家激活策略**：以门控后验均值的二次质量度量 $m_i = \bar{g}_{t,i}^2$ 为依据，通过设定覆盖率阈值 $\tau_m$ 动态选择活跃专家子集。这使 SMP 在 258.9M 总参数中仅需 **80.2M 活跃参数**，推理时间 107.3 ms，比 Sparse DP 快 27 ms，比等容量的 DP 快 13 ms，且去除自适应选择（固定 top‑k=4）时成功率仅微降（0.54→0.53），改用线性质量度量则降至 0.52，说明二次质量与动态阈值的结合是效率与精度的调节杠杆。

综上，SMP 的创新并非模块的简单堆叠，而是通过**正交化基 + 粘性路由**的因果组合，根本上改变了技能表达与组合的方式：基负责解耦技能子空间，门控负责稀疏且平稳地激活它们，系数扩散则在低维白化空间中进行。这套机制在双臂多任务学习（RoboTwin‑2 0.54 vs. 0.41 Sparse DP）、小样本迁移（0.38 vs. 0.31 Disc. Policy）和技能组合（0.30 vs. 0.25 Sparse DP）等设定中均取得一致且显著的优势，消融结果亦强有力地验证了各改变槽位的独立贡献。

![[assets/figures/papers/iclr26_0005_VSWjHIveqZ_Abstracting_Robot_Manipulation_Skills_via_Mixtur/figures/002_Figure_2.jpg]]
*Figure 2: Skill Mixture-of-Experts Policy (SMP) Training Framework. Left (a): During training, raw observations are encoded into state features, which generate an unconstrained matrix W(s). A QR retraction produces a state-adaptive orthogonal basis B(s). Actions are reconstructed via B(s)(g ⊙ z), where g are sticky-gated weights and z are diffusion-based coefficients. The model is trained with reconstruction, diffusion, gate regularization, and alignment losses. Right (b): Illustration of the state-adaptive basis across timesteps: as the robot moves, the basis vectors adjust with the state, while sticky gates preserve consistent expert roles (e.g., translation and rotation).*

![[assets/figures/papers/iclr26_0005_VSWjHIveqZ_Abstracting_Robot_Manipulation_Skills_via_Mixtur/figures/017_Figure_7.jpg]]
*Figure 7: Inference pipeline of SMP. The observation encoder first maps the input observation to a shared feature, which is then fed to the state-dependent skill-basis network and to the MoE module (gate and selected diffusion experts). The basis and experts are evaluated in parallel, with the gate adding only a small overhead. The annotated values indicate the measured per-step runtimes of each component on an NVIDIA A6000 GPU, which sum to an overall inference time of approximately 107 ms per control step.*

SMP 的推理与训练过程均遵循一个统一的“编码-分解-合成”管线。如图 7 所示，视觉编码器首先将多视角 RGB‑D 观测映射为共享的状态特征 $s$；随后该特征同时馈入两条并行分支：**技能基网络** 生成状态自适应的正交技能基 $B(s) \in \mathbb{R}^{d \times K}$ （$B^\top B = I_K$），而 **门控（路由器）** 则输出 $K$ 维的粘性门控权重 $g_t$（服从 Dirichlet 分布）。扩散专家组成 MoE 模块，在动作系数空间 $\mathbb{R}^K$ 内对技能系数 $z_t$ 进行去噪；每个专家为一个条件扩散去噪器，其参数按门控动态激活。

动作的生成过程遵循
$$
a_t = B(s) \, (g_t \odot z_t),
$$
即动作是 $K$ 个技能基向量的门控线性组合。训练时（图 2a），原始动作 $a_t$ 通过反投影得到两个系数目标：一个携带 stop‑gradient 的目标 $\hat{z}_{0,t}^{\mathrm{sg}}$ 用于系数扩散损失 $L_{\mathrm{coeff}}$，另一个携带梯度的目标 $\hat{z}_{0,t}^{\mathrm{rec}}$ 用于动作重构损失 $L_{\mathrm{recon}}$。整体训练目标为变分下界（Equation 6），分解为重构项、门控正则项（含全局使用先验的 KL 散度）和系数扩散正则项，外加一个状态‑路由器对齐损失 $L_{\mathrm{align}}$，以提升测试时门控的一致性。

门控的时序动态由粘性 Dirichlet‑Markov 先验（Equation 3）建模，具体为
$$
\vartheta \sim \mathrm{Dir}(\alpha \mathbf{1}),\; g_1 \sim \mathrm{Dir}(\alpha_0 \vartheta),\; g_t \sim \mathrm{Dir}(\kappa g_{t-1} + \alpha_0 \vartheta),\; t \ge 2,
$$
其中 $\vartheta$ 为全局使用分布，$\kappa$ 控制时间粘性，$\alpha_0$ 锚定强度。这一设计促使门控权重在时间上呈现分段常数、相位一致的稀疏激活，从而将复杂操作分解为少量可复用“技能”的组合（参见 Figure 3 的门控迹线）。

推理阶段，SMP 利用**自适应专家激活**策略（Section 4.2，Equation 41）。对每一步 $t$，路由器先输出均值 $\bar{g}_t$，然后按 $m_i = \bar{g}_{t,i}^2$ 计算每个专家的质量分数，并贪心地选择子集 $S$ 直至累积质量超过阈值 $\tau_m$（默认 $0.95$）。仅在 $S$ 内的扩散专家被执行推理，未激活专家被旁路。通过该机制，SMP 能以 $80.2$ M 活跃参数（总参数量 $258.9$ M）在约 $107$ ms 内完成一步推理（Figure 7，Table 6），在可比成功率下显著低于稠密 MoE 基线的推理成本。

整体而言，SMP 的核心创新在于**正交技能基 + 粘性路由于系数空间联合生成**的设计：技能基网络通过可微薄‑QR 分解（Equation 2）将未约束矩阵 $W(s)$ 投影到 Stiefel 流形上，使基向量随状态自适应旋转但保持正交，从而为动作提供结构化、可解耦的表征；粘性门控确保相位一致、专家复用；自适应激活则动态裁剪计算图。这一管线在双臂多任务学习、小样本迁移和技能组合等场景中均表现出明显的性能‑效率优势，其消融实验也证实各个组件的不可或缺性。

SMP 将扩散策略下的多任务操作技能抽象分解为三个关键设计：状态自适应的正交技能基、粘性门控（sticky routing）下的系数解码，以及在系数空间中进行的扩散建模。下面围绕四个核心模块的职责以及驱动这些模块的关键公式展开。

### 核心模块及其作用

- **视觉编码器（Vision Encoder）**：将原始观测（图像、点云）映射为共享状态特征 $s_t$，供后续所有模块消费。该模块约 11.2M 参数，单步推理耗时约 23 ms。

- **技能基网络（Skill‑Basis Network）**：从状态特征 $s_t$ 生成未约束矩阵 $W(s)$，随后通过可微薄 QR 分解与符号稳定化将其投影到 Stiefel 流形，得到正交技能基 $B(s)\in\mathbb{R}^{d\times K}$，满足 $B(s)^\top B(s)=I_K$。这是动作空间局部“白化”的核心——动作被表示在一组数量远小于动作维度的正交方向上的组合，使得技能在几何上可解释、可解耦。该模块约 12.5M 参数，单步推理约 24 ms。

- **门控路由器（Gate/Router）**：输出粘性 Dirichlet 门控向量 $g_t\in\Delta^{K-1}$（概率单纯形）。门控不仅依赖当前状态，还通过一阶 Dirichlet–Markov 动力学引入强时间粘性（stickiness $\kappa$）和全局使用先验（$\vartheta$），促使技能激活呈现分段常值的阶段式结构，且在任务间复用相同的专家。训练时使用变分后验 $q(g_t\mid s_t,a_t)$，推理时切换为状态路由器 $p_\phi(g_t\mid s_t)$，并辅以对齐损失 $\mathcal{L}_{\mathrm{align}}$ 保证一致性。该模块约 3.6M 参数，单步推理约 10 ms。

- **扩散专家（Diffusion Experts）**：每个专家是一个在系数空间中的扩散去噪器，负责学习技能系数 $z_t$ 的去噪过程。系数 $z_t$ 与门控 $g_t$ 逐元素乘积后再经基 $B(s)$ 解码为动作，即 $a_t = B(s)(g_t\odot z_t)$。扩散损失直接施加于去噪后的 $z_t$，而非原始动作空间。单个专家约 28.9M 参数，推理时每步只激活少量专家（自适应激活策略），总体活跃参数控制在约 80M，单步总推理时间约 107 ms。

### 关键公式及其变量含义

1. **动作解码与正交基约束**  
   $$a_t = B(s_t)\big(g_t \odot z_t\big),\qquad B(s_t)^\top B(s_t)=I_K$$  
   $a_t$ 为执行器动作向量，$K$ 为技能数，$g_t$ 是稀疏门控权重，$z_t$ 是扩散模型生成的连续系数。正交基保证不同技能方向之间独立，组合方式仅由 $g_t$ 和 $z_t$ 控制，而 $B(s_t)$ 随状态变化使技能空间适应任务几何。

2. **可微 QR 构造状态自适应正交基**  
   $$W(s)=\tilde{B}U,\quad D=\mathrm{diag}\big(\mathrm{sign}(\mathrm{diag}(U))\big),\quad B(s)=\tilde{B}D,\quad \tilde{B}^\top\tilde{B}=I_K,\;U\text{为上三角}$$  
   从神经网络输出的未约束矩阵 $W(s)$ 出发，通过 thin‑QR 得到 $\tilde{B}$ 和上三角 $U$，再对 $U$ 的对角元取符号构造对角矩阵 $D$，令 $B(s)=\tilde{B}D$ 以保证状态变化时基的符号连续性，避免跳跃。该操作嵌在计算图中，梯度通过重参数化回传。

3. **粘性 Dirichlet 门控先验**  
   $$\vartheta\sim\mathrm{Dir}(\alpha\mathbf{1}),\quad g_1\sim\mathrm{Dir}(\alpha_0\vartheta),\quad g_t\sim\mathrm{Dir}\big(\kappa g_{t-1}+\alpha_0\vartheta\big),\;t\ge2$$  
   $\vartheta$ 是全局技能使用先验，$\alpha$ 控制其稀疏性；$\alpha_0$ 为锚定强度，将每步门控拉向全局使用；$\kappa$ 是粘性参数，使当前门控贴近上一步 $g_{t-1}$，从而形成长程稳定的技能分配，避免频繁切换。

4. **变分 ELBO 与训练损失分解**  
   $$\log p_\theta(a_{1:T}\mid s_{1:T})\ge\mathbb{E}_q\big[\log p(a_{1:T}\mid g_{1:T},z_{1:T},s_{1:T},B)\big]\\
   -D_{\mathrm{KL}}\big(q(\vartheta,g_{1:T})\big\Vert p(\vartheta,g_{1:T})\big)\\
   -D_{\mathrm{KL}}\big(q(z_{1:T})\big\Vert p(z_{1:T})\big)$$  
   第一项为动作重构项，第二项为正则化门控分布的 KL 散度（鼓励稀疏、粘性使用），第三项为正则化系数扩散先验的 KL 散度。训练时三部分共同优化基网络、门控网络和扩散去噪器。

5. **双目标系数构造——稳定正交基学习**  
   $$\hat{z}_{0,t}^{\mathrm{sg}} = \frac{\overline{B}(s_t)^\top a_t}{\mathbb{E}_q[g_t]+\epsilon},\qquad
     \hat{z}_{0,t}^{\mathrm{rec}} = \frac{B(s_t)^\top a_t}{\mathbb{E}_q[g_t]+\epsilon}$$  
   $\overline{B}$ 表示阻止梯度传播（stop‑gradient）的基，$\hat{z}_{0,t}^{\mathrm{sg}}$ 仅用于计算系数扩散损失（不更新 $B$），而 $\hat{z}_{0,t}^{\mathrm{rec}}$ 允许梯度流入 $B$，用于动作重构损失 $\mathcal{L}_{\mathrm{recon}}$ 更新基和门控。这种双通道设计防止扩散损失干扰基的几何约束。

6. **自适应专家激活——按需选择计算子集**  
   $$m_i = \bar{g}_{t,i}^{\,2}$$  
   推理时，路由器给出均值门控 $\bar{g}_t$，每个专家的“激活质量”定义为门控方差的二次函数 $m_i$。对质量分数从高到低累加，直至达到覆盖阈值 $\tau_m$（默认 0.95），选出的专家子集参与去噪解码，其余跳过。该策略使 SMP 以约 31% 的总参数参与计算，成功率损失极小，推理加速显著。

上述模块与公式构成 SMP 从状态观测到稀疏技能动作的完整流水线：状态特征经基网络生成正交基底，经粘性门控得到稀疏组合权重，经扩散专家在系数空间采样去噪，最终解码为机器人动作。核心假设是演示动作落在一个低维、状态依赖且正交的技能子空间内，并通过门控的稀疏性与粘性实现技能的重用与阶段连贯。

## 实验与关键发现

SMP 的核心实验围绕多任务双臂操作展开，目标在于验证两个命题：
1）**状态自适应的正交技能基与粘性门控能否将扩散策略的动作空间分解为可复用的技能分量**，从而突破传统 MoE 中技能纠缠和模型规模膨胀的瓶颈；
2）**自适应专家激活机制能否在保持成功率的同时大幅降低推理成本**。
证据强度整体较高——实验在 RoboTwin-2 和 RLBench-2 两个标准多任务基准上与 7 种强方法严谨对比，消融实验保留除被消去组件外的全部设计，且通过缩放基线实验排除了容量不足的替代解释。

### 多任务学习主结果
**(Table 1)** RoboTwin-2 六任务平均成功率：SMP 达到 0.54，较最强基线 Sparse DP（0.41）提升 13 个百分点；RLBench-2 四任务平均成功率：SMP 为 0.18，而最优基线仅 0.14。SMP 在大多数单任务上也优于或持平基线。这些结果说明**正交基与粘性门控的组合并非仅仅增加模型容量，而是根本性地改变了技能组合方式**——动作被表示为少量正交基向量的门控线性组合，每个基向量对应可解释的移动基元（如平移、旋转、抓取），粘性路由使同一语义阶段内专家激活保持稳定，避免了传统 MoE 的频繁切换和技能纠缠。

**定性可视化**进一步支撑这一结论：**(Figure 3)** 的门控轨迹显示，SMP 在不同任务间复用同一组专家——例如左臂和右臂的原语共享底层技能基，且门控值在拾取、移动、放置等阶段内呈现长片段、低切换的“相位一致”模式。这种结构化复用是性能提升的关键因果机制。

![[assets/figures/papers/iclr26_0005_VSWjHIveqZ_Abstracting_Robot_Manipulation_Skills_via_Mixtur/figures/003_Figure_3.jpg]]
*Figure 3: Multi-task learning in RoboTwin-2 and RLBench-2. SMP partitions bimanual control into an orthonormal skill basis and routes with sticky gates. Across tasks, the same experts are reused for left- and right-arm primitives and for pick–move–place phases, with few switches and long segments. Gate traces reveal sparse, phase-consistent activation, and cross-task skill reuse, indicating that actions are composed from a small, task-relevant subset of experts.*

### 推理效率
**(Table 2)** 尽管 SMP 总参数量达 258.9M，但**活跃参数仅 80.2M**，推理时间 107.3 ms，比 Sparse DP 快 27 ms，比 DP 快 13 ms，与轻量级的 ACT 接近。效率增益来自两步：1）**正交基投影**将高维动作空间压缩到低维系数空间，使每位专家只需对低维系数去噪，大幅减小单次扩散计算量；2）**自适应专家激活**利用二次质量函数 $m_i = \bar{g}_{t,i}^2$ 动态选择贡献最大的专家子集，步均活跃专家数远低于固定 full-set 或 top‑k 方案。这使 SMP 在保持成功率的同时实现了稀疏计算，缓解了扩散策略在多任务场景下的推理延迟瓶颈。

### 消融分析
**(Table 7)** 逐一拆除 SMP 核心组件，揭示各设计的作用强度：

- **去除粘性门控（W/o sticky gate）**：RoboTwin-2 成功率从 0.54 骤降至 0.44（降幅 0.10）。这一跌幅最大，表明**时间一致性是先决条件**——若门控在每个时间步独立变化，基向量的语义持续性和技能复用将严重退化。
- **固定技能基（Fixed skill basis）**：成功率降至 0.40；**替换为 PCA 全局基**更降至 0.32。两者均显著削弱性能，证实**状态自适应的正交基是解耦技能的核心使能器**——固定基无法适应不同位姿下的动作方向变化，PCA 基则完全丧失状态相关性，导致系数空间无法有效建模差异化行为。
- **自适应专家激活**：移除自适应机制、改用固定 top‑k=4 时，成功率仅微降至 0.53；将质量函数改为线性（Linear mass adapt.）则降至 0.52。尽管影响相对较小，但二次质量函数在极低活跃专家数下保精度的作用仍然显著，且通过覆盖率阈值 $\tau_m$ 可平滑调控成功–延迟曲线（**Figure 9**）。
- **缩放基线实验（Table 8）**：将 DP、DP3、ACT 扩至约 300M 参数后，RoboTwin-2 成功率最高仅 0.42，仍远低于 SMP，且推理时间进一步增加。这排除了“SMP 胜出仅因更大容量”的猜测，再次确认**技能抽象而非参数规模**是性能提升的主因。

下位基准 RLBench-2 和技能组合实验（Table 4）的趋势一致：SMP 在少样本迁移和技能组合任务上同样保持优势（平均成功率 0.38 vs. 0.31 和 0.30 vs. 0.25），证明学到的技能基元具备**跨任务迁移与重组能力**。

### 局限性与失败模式
当前证据存在以下边界：
- **任务范围窄**：全部实验均为双臂桌面操作，未在单臂、移动操作或复杂接触密集任务上验证，因此“可复用技能”的泛化性仍属局部推论。
- **真实世界规模小**：实机实验仅涵盖 4 个任务、每任务 10 次重复（**Figure 5**），缺乏大规模部署和长期鲁棒性测试；传感噪声、视觉域漂移下的稀疏激活鲁棒性也未系统研究。
- **内存开销仍高**：虽然活跃参数量低，但总参数量仍达 258.9M，对边缘设备部署形成限制。
- **粘性路由的调参敏感**：Dirichlet–Markov 先验的性能对 $\kappa$、$\alpha$、$\alpha_0$ 较敏感（**Figure 8**），且当前未给出自动调参方案，可能增加在新环境中的部署成本。
- **失败任务模式未量化**：论文未报告如何失败（如阶段误判、专家冲突），难以分析哪些技能更难解耦或复用。

上述局限提示，若要进一步推广 SMP，需在更宽域的基准上检验技能基的鲁棒性，并量化稠密接触与动态约束任务下的失效模式。

![[assets/figures/papers/iclr26_0005_VSWjHIveqZ_Abstracting_Robot_Manipulation_Skills_via_Mixtur/figures/004_Table_1.jpg]]
*Table 1: Success Rates in Bimanual Multi-Task Learning Tasks ↑*

![[assets/figures/papers/iclr26_0005_VSWjHIveqZ_Abstracting_Robot_Manipulation_Skills_via_Mixtur/figures/005_Table_2.jpg]]

![[assets/figures/papers/iclr26_0005_VSWjHIveqZ_Abstracting_Robot_Manipulation_Skills_via_Mixtur/figures/018_Table_7.jpg]]
*Table 7: Success Rates of Ablation Studies ↑*

## 定位与知识库关联

SMP 处于扩散策略（DP）与混合专家（MoE）的交汇点，但通过显式的技能基分解与结构化门控，与已有工作形成根本性差异。基线扩散策略（DP、DP3）以全局、无约束的方式生成动作，在多任务场景下需要大幅扩展参数量来容纳行为多样性，但仍因技能纠缠而难以高效复用（Table 8: 缩放到~300M 后成功率最高仅 0.42）。Discrete Policy 引入离散码本抽象技能，但其离散化限制了连续动作空间中精妙原语的学习，且未见稀疏激活带来的推理加速。Sparse DP（SDP）虽采用 MoE 架构并在实验中达到 0.41 的平均成功率（RoboTwin-2），但其路由器没有时间结构和空间正交约束，导致专家激活在时间维频繁切换、技能难以解耦和迁移。SMP 对上述格局的改变体现在四个关键设计槽位：

1. **技能基构造（Skill Basis Construction）**：SMP 不直接输出动作，而是生成状态自适应的正交技能基 $B(s)$（经可微薄 QR 分解与符号稳定化投影到 Stiefel 流形，$B^\top B = I_K$）。该基将动作空间局部白化投影到低维流形，使得系数 $z_t$ 在各任务中对应可复用的动作分量，是技能解耦的几何支柱。消融实验表明，将正交基替换为固定基或 PCA 基会导致成功率大幅下降（0.40、0.32 vs 0.54），验证了状态自适应正交结构的关键性。

2. **门控机制（Gating Mechanism）**：SMP 引入粘性 Dirichlet–Markov 门控（$\vartheta, g_t$），并通过全局使用先验和 KL 正则化鼓励分段常数、相位一致的专家激活。这显著区别于 SDP 的前馈路由器和 Discrete Policy 的离散隐变量，使得同一技能在长时间窗口内保持激活，减少路由抖动，同时促进跨任务的技能复用（Figure 3 中可见左右手原语与拾‑放‑移阶段被同一组专家覆盖）。去除粘性门控后，RoboTwin-2 成功率从 0.54 下降到 0.44，直接证实时间粘性对性能的贡献。

3. **训练目标（Training Objective）**：SMP 采用变分 ELBO，联合优化重构（系数空间与动作空间双重目标，带 stop‑gradient 以稳定基的更新）、门控正则与系数扩散损失，并辅以状态路由器对齐损失 $\mathcal{L}_{\mathrm{align}}$。这一多目标配方允许技能基学习、门控动态学习和系数扩散训练彼此协调，而基线方法仅使用标准的扩散 ELBO 或 VQ‑VAE 重构目标。

4. **推理时的自适应专家激活（Adaptive Expert Activation）**：SMP 根据路由均值 $\bar{g}_{t,i}$ 的二次质量度量 $m_i=\bar{g}_{t,i}^2$ 灵活选择激活专家子集，而非固定 top‑k 或激活所有专家。这使得 SMP 在活跃参数量仅约 80.2M 的条件下实现 107.3 ms 推理延迟（Table 2），比 Sparse DP 快约 27 ms，同时保持 0.54 的高成功率。该机制在二次质量和自适应选择两方面的贡献已由消融确认（仅轻微下降至 0.53/0.52）。

在技能抽象方法谱系中，SMP 可视为连续型结构化技能分解与稀疏 MoE 的结合，其核心创新在于通过正交几何和粘性路由将技能抽象从“隐式特征学习”提升到“显式可复用原语层面”，为多任务操作提供了更紧凑且可迁移的技能表达。

**适用边界与局限**

- **任务覆盖范围**：当前评估完全集中在双臂操作任务（RoboTwin‑2、RLBench‑2 及一组 4 项真机任务），尚未在单臂或移动操作等不同构型上验证。方法对非操作型任务的泛化性未知。
- **真实世界部署**：真机实验仅覆盖 4 项任务且每项 10 次试验，缺乏大规模、长周期运行和故障模式的系统记录，也不足以评估在传感器噪声、光照变化和物件多样性下的鲁棒性。
- **鲁棒性检验**：虽然 SMP 在标准传感配置下表现良好，但未曾系统测试粘性路由和自适应激活在视觉域漂移、瞬时传感噪声下的行为；理论上，如果路由器置信度因域漂移而崩塌，自适应激活机制（依赖质量度量）可能错误修剪关键专家。
- **资源需求**：SMP 总参数量仍高达 258.9M（主要由 8 个扩散专家贡献），虽有活跃参数量低和推理快的优势，但对显存仍有较高需求，可能限制在资源受限的嵌入式平台上的直接部署。
- **训练复杂度**：引入薄 QR 分解、Dirichlet 门控动态和双重系数目标，增加了训练复杂度，并引入了额外的超参数（粘性系数 κ、全局使用先验 α、锚定强度 α0 等），需通过超参扫描（Figure 8）进行调节。

**开放问题**

- **规模拓展与泛化**：SMP 能否在更大模型和更多样化任务（例如跨构型单臂、移动操作，或与导航耦合的长期任务）中保持技能解耦与推理效率优势，仍是待探索的方向。
- **实时约束下的成功–延迟权衡**：当前延迟（107 ms）已满足典型操作控制需求，但更极端的实时场景（<50 ms）下，如何进一步压缩活跃专家数量并保持成功率，需定量刻画自适应激活策略的帕累托前沿。
- **鲁棒性与不确定性**：在传感噪声、视觉域偏移或动态环境变化下，正交技能基的降维投影和稀疏激活是否仍能可靠捕捉动作分布的主体模式，以及门控路由器是否需要额外的校准或不确定性估计，尚未有实验验证。
- **与大规模预训练模型的融合**：SMP 的技能抽象机制是否能与视觉‑语言‑动作（VLA）预训练模型结合，将正交基作为低维动作瓶颈接入大规模异构数据训练，从而提升跨任务的零样本和小样本迁移能力，还未有研究涉及。
- **理论理解**：正交基与粘性门控的结合为何能带来如此显著的技能解耦和路由稳定性，其背后的理论保证（如流形约束下的泛化界、门控动态的混合时间）仍待深入分析。

总之，SMP 在技能解耦、路由稳定性和推理效率上相对于现有扩散 MoE 基线取得了明确进展，但其在任务拓展性、鲁棒性和与大规模预训练范式对接等方面尚需大量后续研究。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Abstracting_Robot_Manipulation_Skills_via_Mixture_of_Experts_Diffusion_Policies.pdf

![[paperPDFs/ICLR_2026/Abstracting_Robot_Manipulation_Skills_via_Mixture_of_Experts_Diffusion_Policies.pdf]]
