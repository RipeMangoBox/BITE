---
title: "PRISM: Streaming Human Motion Generation with Per-Joint Latent Decomposition"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition.pdf
project_link: null
code_link: https://github.com/ZeyuLing/PRISM
aliases:
- PRISM
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将每关节作为独立标记（token），形成结构化的2D潜在网格（时间×关节），并使用因果VAE和前向动力学监督，从而显式保持运动学结构，并允许每标记噪声注入。
primary_logic: 通过设计每关节因子分解的潜在空间和每标记时间步嵌入，一个流匹配Transformer可以统一文本到动作、姿态条件生成和自回归流式生成，无需任务特定修改，且自激励训练有效抑制长序列漂移。
claims:
- 每关节因子分解的潜在空间将重建MPJPE降低18倍（1.82 vs 33.82 mm），rFID降低20倍，并显著提升生成FID。
- 每标记时间步嵌入（噪声自由条件注入）使模型在没有架构改变的情况下统一文本到动作与姿态条件生成，并直接支持自回归流式生成。
- 自激励训练弥合了训练与推理的差距，使得在10段以上的长序列生成中保持稳定，远超训练时的片段长度。
- 因果时间卷积对于无缝的自回归拼接至关重要，同时不影响单段质量。
---

# PRISM: Streaming Human Motion Generation with Per-Joint Latent Decomposition

> [!tip] 核心洞察
> 通过设计每关节因子分解的潜在空间和每标记时间步嵌入，一个流匹配Transformer可以统一文本到动作、姿态条件生成和自回归流式生成，无需任务特定修改，且自激励训练有效抑制长序列漂移。

| 字段 | 内容 |
|------|------|
| 中文题名 | PRISM: 基于逐关节潜在分解的流式人体运动生成 |
| 英文题名 | PRISM: Streaming Human Motion Generation with Per-Joint Latent Decomposition |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.08590) · [Code](https://github.com/ZeyuLing/PRISM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | PRISM |
| Dataset | HumanML3D, MotionHub, BABEL Seq., Narrative Composition |

> [!tip] 效果简介
> - HumanML3D (T2M) 上，FID↓ 0.027 vs 0.060 (previous best) (-55%)。
> - MotionHub (T2M) 上，FID↓ 0.055 vs 0.106 (Go-To-Zero) (-48%)。
> - BABEL Seq. 上，Subseq. R@3↑ 0.587 vs 0.469 (MotionStreamer) (+0.118)。

## 概要

人体运动生成的核心瓶颈在于**潜在空间设计**：现有方法（如**MotionStreamer**，Xiao et al., ICCV 2025；**MLD**，Chen et al., ICLR 2024）将每帧运动信息压缩为单一向量，轨迹与各关节旋转深度缠绕，迫使下游生成器隐式解耦异构信号，浪费模型容量并限制生成质量。

PRISM 提出**逐关节因子分解**的潜在空间，将每关节作为独立标记（token），形成结构化的 2D 潜在网格（时间 × 关节），配合**因果 VAE** 与**前向动力学监督**，显式保持运动学结构。在此基础上，**每标记时间步嵌入**使单个流匹配 Transformer 无需架构修改即可统一文本到动作、姿态条件生成和自回归流式生成；**自激励训练**则有效弥合训练-推理差距，抑制长序列漂移。

关键实证结果：
- 潜在空间重构误差（MPJPE）降低 **18 倍**（1.82 vs 33.82 mm），重构 FID 降低 **20 倍**（Table 4）；
- 文本到动作生成 FID 在 HumanML3D 上达到 **0.027**，较此前最优降低 55%；在 MotionHub 上达到 **0.055**，降低 48%（Table 1）；
- 自回归流式生成在 BABEL 序列任务上子序列 R@3 达到 **0.587**（+0.118），且转换平滑度（Area Under Jerk）较 MotionStreamer 降低 **51%**（Table 3）；
- 叙事动作组合用户研究中，整体偏好（Good%）达 **76.4%**，远超 MotionStreamer 的 8.8%（Table 8）。

PRISM 的局限性包括仅支持 SMPL-22 身体运动（不含手部和表情）、超长序列（>5 分钟）仍可能累积轨迹漂移，以及生成速度约 20 fps 尚不足以支持实时交互。



### 问题背景：从单段生成到流式人体运动合成

人体运动生成是计算机视觉与图形学中的核心任务，旨在根据文本描述、姿态条件或序列动作标签合成自然、物理合理的人体运动序列。近年来，扩散模型和流匹配模型在该领域取得了显著进展，涌现出一批代表性工作：**MLD**（Chen et al., ICLR 2024）将潜在扩散模型引入运动生成，**MoMask**（Guo et al., CVPR 2024）采用掩码Transformer进行离散标记生成，**FlowMDM**（Dai et al., ECCV 2024）结合流匹配与混合位置编码，**ViMoGen**（Shi et al., arXiv 2025）则探索了大规模流匹配模型的潜力。

然而，现有方法大多聚焦于**单段运动生成**——模型接收一个文本提示或动作标签，输出一段固定时长的运动序列。这一范式在流式场景下面临根本性局限：实际应用（如交互式角色动画、叙事驱动的人体动作合成）要求模型能够持续生成连贯的运动流，支持文本到动作、姿态条件生成、序列合成和长时叙述组合等多种模式，且生成质量不应随时间退化。

### 现有方法的瓶颈：潜在空间的异构信号缠绕

当前运动生成模型普遍采用一种**每帧单一向量**的潜在空间设计：将每一帧的人体运动信息（包括根轨迹位移、全局朝向和所有关节的旋转参数）压缩为一个潜在向量。这种设计的核心问题在于**异构信号的强制缠绕**——轨迹信息描述的是全局空间位移，而关节旋转描述的是局部姿态变化，它们在物理语义和统计特性上截然不同，却被强行编码为同一向量。下游生成器（如扩散Transformer或DiT）需要隐式地解耦这些信号，这不仅浪费了模型容量，还直接限制了生成质量。

具体而言，这种缠绕带来三个层面的问题：

1. **运动学结构丢失**：人体骨骼具有明确的树状运动学链，父关节的旋转会通过前向动力学（FK）传播到子关节。每帧单一向量无法显式保持这种结构化约束，导致重建和生成中出现关节错位和物理伪影。
2. **条件注入困难**：在流式场景中，模型需要根据已生成的帧（干净信号）预测后续帧（含噪信号）。单一时间步标量无法区分干净条件标记与待去噪标记，迫使现有方法依赖专用的修复网络或额外的条件编码器。
3. **自回归漂移**：流式生成本质上是一个自回归过程——模型使用自身的历史输出作为条件来生成未来帧。训练时常用的教师强制（teacher forcing）策略使用真实值作为条件，导致训练-推理分布不匹配，在长序列生成中迅速累积误差。

### PRISM的动机：结构化潜在空间与统一生成范式

针对上述瓶颈，PRISM提出了一套系统性的解决方案，其核心动机可以概括为三个递进的因果逻辑：

**因果逻辑1：显式因子分解 → 降低解耦负担。** 将每关节作为独立标记，形成时间×关节的2D结构化潜在网格，使潜在空间本身保持运动学结构。下游生成器无需隐式解耦异构信号，模型容量可完全用于学习运动分布。

**因果逻辑2：每标记时间步嵌入 → 统一生成模式。** 为每个潜在标记分配独立的时间步嵌入，干净条件标记使用$t=0$注入，待生成标记使用对应噪声时间步。这一设计使得同一个流匹配Transformer在不改变架构的情况下，原生支持文本到动作、姿态条件生成和自回归流式生成。

**因果逻辑3：自激励训练 → 抑制长序列漂移。** 在训练中模拟自回归推理管道，使用模型自身输出而非真实值作为历史条件，从根本上弥合训练-推理差距，使模型在远超训练片段长度的序列上保持稳定。

这一设计哲学使得PRISM成为一个**单一模型、多种模式**的统一框架，无需任务特定的架构修改或后处理，即可在文本到动作、姿态条件生成、序列动作合成和叙事运动组合等任务上达到最优性能。



## 核心方法与创新机理

PRISM的核心创新在于对动作生成潜在空间的根本性重构，以及一套与之配套的、无需架构修改即可统一多种生成模式的注入机制。其设计围绕一个核心洞察展开：**现有方法将每帧动作信息压缩为单一向量，迫使下游生成器隐式解耦异构的轨迹与关节旋转信号，浪费模型容量并限制生成质量**。PRISM通过四个关键的“changed slots”，系统性地解决了这一问题。

### 1. 逐关节因子分解的潜在空间（Joint-Factorized Latent Space）

PRISM将动作序列构建为一个结构化的2D潜在网格，维度为时间 × 关节数，每个关节占据一个独立的标记（token）。这与主流方法（如**MotionStreamer** (Xiao et al., ICCV 2025)、**MLD** (Chen et al., ICLR 2024)）将每帧动作信息压缩为单一向量的做法形成根本性差异。

**因果机制**：通过将根位移、朝向和每关节旋转显式地组织为独立的标记，PRISM的VAE编码器无需再隐式地解耦这些异构信号。编码器使用严格的因果时序卷积处理每个关节的时间序列，再通过空间关节注意力层进行跨关节交互。这种设计显式地保持了运动学结构，使得潜在空间本身就对下游生成任务更加友好。

**证据强度**：该设计的有效性在重建和生成两个层面均得到强有力验证（Table 4, Table 6）。在HumanML3D上，逐关节因子分解的VAE将重建MPJPE从MotionStreamer的33.82 mm降至1.82 mm，**降低18倍**；重建FID（rFID）从0.020降至0.001，**降低20倍**。消融实验进一步表明，2D关节潜在空间相比1D整体潜在空间，将MPJPE降低14倍（1.99 vs 28.47 mm），并将下游生成FID从0.137大幅降至0.055（Table 6）。这表明，**潜在空间的结构化设计是生成质量跃升的首要瓶颈因素**。

### 2. 因果时序卷积（Causal Temporal Convolutions）

与大多数动作VAE采用的双向（非因果）卷积不同，PRISM在编码器和解码器中均采用严格的因果时序卷积。这一设计是支撑PRISM流式生成能力的关键。

**因果机制**：因果卷积确保在任意时间步，模型只能看到当前及过去的帧信息，而无法窥视未来。这使得VAE天然支持自回归式的序列生成，因为在对当前片段进行编码或解码时，不会引入来自未来片段的“信息泄露”，从而保证了多片段拼接时的逻辑一致性和平滑性。

**证据强度**：消融实验（Table 5）证实了因果设计的必要性。在BABEL序列生成任务中，因果VAE的序列FID达到0.100，优于非因果VAE的0.136；子序列R@3也更高（0.587 vs 0.543）。更重要的是，因果VAE在保持单段文本到动作生成质量（MotionHub FID 0.055 vs 0.054）的同时，显著提升了多片段拼接的平滑度。**这证明因果性是为实现无缝自回归拼接而付出的几乎无代价的架构选择**。

### 3. 无噪声条件注入（Noise-Free Condition Injection）

PRISM提出了一种极简但强大的条件注入机制：**为潜在网格中的每个标记分配独立的时间步嵌入**。在训练和推理时，条件帧（如姿态条件生成中的前k帧，或自回归生成中的上一片段）被编码后，其对应标记的时间步被设为 $t=0$（无噪声），而待生成的其余标记则接收 $t>0$ 的噪声时间步。

**因果机制**：这一机制使得PRISM的流匹配DiT生成器无需任何专门的修复网络（inpainting network）或混合编码，就能原生地理解“哪些部分是给定的干净条件，哪些部分是需要去噪生成的目标”。它将文本到动作、姿态条件生成和自回归流式生成统一在了同一个去噪框架下。

**证据强度**：论文明确指出，PRISM“无需专用的修复网络或混合编码”即可处理姿态条件生成（Sec 4.3），这与先前方法（如**FlowMDM** (Dai et al., ECCV 2024)）形成对比。Table 2的姿态条件生成结果验证了该机制的有效性，PRISM在所有指标上均取得最佳性能。

### 4. 自激励训练（Self-Forcing Training）

为了弥合自回归生成中训练与推理的差距，PRISM采用了自激励训练策略。传统的“教师强制”（teacher forcing）方法在训练时使用真实历史帧作为条件，而推理时则使用模型自身生成的、可能包含误差的预测帧，这种不匹配会导致长序列生成中的误差累积和漂移。

**因果机制**：自激励训练在训练过程中，以一定概率将条件帧替换为模型自身的输出，迫使生成器学会在带有噪声的条件下进行去噪预测。这使得模型在推理时面对自身生成的历史帧时，具备更强的鲁棒性和漂移抑制能力。

**证据强度**：消融实验（Table 7）表明，自激励训练在BABEL序列生成上取得了最佳的子序列FID（0.100）和最低的转换急动度（Area Under Jerk 0.44），显著优于教师强制和无激励方案。这证明**自激励是抑制长序列漂移、实现远超训练片段长度的流式生成的关键训练策略**。



PRISM 的整体管道由两个紧耦合的模块构成：**因果逐关节因子化动作 VAE（Causal Joint-Factorized Motion VAE）** 和 **潜在流匹配 DiT 生成器（Flow-Matching DiT Generator）**，两者通过一个结构化的 2D 潜在网格进行桥接。

### 输入表示：逐关节结构化的 2D 网格

管道的输入端将每帧 SMPL 运动参数组织为一个结构化的 2D 标记网格 $X \in \mathbb{R}^{T \times K \times 6}$，其中 $T$ 为时间帧数，$K$ 为标记数（根位移+朝向+各关节旋转）。每个身体关节占据一个独立的标记，显式保持运动学结构：

$$X = \big[ \underbrace{[\mathbf{p}_i; \Delta\mathbf{p}_i]}_{\mathrm{root}}, \underbrace{\boldsymbol{\theta}_i^0}_{\mathrm{orient.}}, \underbrace{\boldsymbol{\theta}_i^1, \ldots, \boldsymbol{\theta}_i^J}_{\mathrm{joint~rotations}} \big]_{i=1}^T \in \mathbb{R}^{T \times K \times 6}$$

### 模块一：因果逐关节因子化 VAE

该模块将上述输入网格压缩为低维潜在表示，形成同样保持时间×关节结构的 2D 潜在网格。其关键设计包括：

- **严格因果时序卷积**：编码器和解码器均使用因果卷积，确保每个时间步的特征仅依赖于过去帧，这是后续无缝自回归拼接的基础。
- **空间关节注意力**：在时间卷积之后应用跨关节的注意力机制，捕获身体各部位间的空间依赖。
- **前向动力学监督**：训练损失中引入前向动力学（FK）关节点损失 $\mathcal{L}_{\mathrm{joints}}$ 和累计轨迹损失 $\mathcal{L}_{\mathrm{traj}}$，显式监督重建的运动学一致性。轨迹损失对逐帧预测位移进行累积求和后与真实轨迹对比，有效抑制长序列中的轨迹漂移。

VAE 的总训练损失为参数 L1 损失、FK 关节点损失、轨迹损失和 KL 正则化的加权组合：

$$\mathcal{L}_{\mathrm{VAE}} = \lambda_{\mathrm{param}} \mathcal{L}_{\mathrm{param}} + \lambda_{\mathrm{joints}} \mathcal{L}_{\mathrm{joints}} + \lambda_{\mathrm{traj}} \mathcal{L}_{\mathrm{traj}} + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}}$$

### 模块二：流匹配 DiT 生成器

生成器在 VAE 的潜在空间上进行流匹配去噪。其核心创新是 **无噪声条件注入（Noise-Free Condition Injection）** 机制：为潜在网格中的每个标记分配独立的时间步嵌入。条件帧（如姿态条件生成中的前 $F$ 帧）被编码后以时间步 $t=0$（无噪声）注入，其余标记则接受标准去噪过程。这一设计使得同一模型无需任何架构修改即可统一处理：

- **文本到动作生成**：所有标记从噪声开始去噪。
- **姿态条件生成**：前若干帧作为干净条件标记注入，其余帧从噪声生成。
- **自回归流式生成**：已生成片段作为干净条件，逐段生成后续运动，实现远超训练片段长度的流式输出。

### 训练策略：自激励训练

为弥合训练与推理之间的分布偏移，PRISM 采用 **自激励训练（Self-Forcing）** 策略：在训练中模拟自回归推理管道，使用模型自身的输出作为后续片段的条件，而非依赖真实值（教师强制）。这有效抑制了长序列生成中的累积误差，使得模型在 10 段以上的流式生成中保持稳定。

### 辅助模块：动作感知文本重写器

针对叙事动作合成场景，PRISM 引入一个 **动作感知文本重写器（Motion-Aware Text Rewriter）**，将自由形式的叙事文本分解为原子动作提示序列，为生成器提供结构化的文本条件。

### 数据流总结

1. SMPL 运动参数 → 结构化 2D 输入网格 → 因果 VAE 编码 → 2D 潜在网格
2. 2D 潜在网格 + 每标记时间步嵌入 → 流匹配 DiT 去噪 → 去噪潜在网格
3. 去噪潜在网格 → 因果 VAE 解码 → SMPL 参数 → 前向动力学 → 3D 关节点位置

整个管道在 SMPL 参数空间生成，通过前向动力学转换为关节点位置用于评估，这与基线方法直接生成 HumanML3D 原生关节表示形成跨表示设定。

### 补充图表

![[assets/figures/papers/paper_list_l86_https_arxiv_org_abs_2603_08590/figures/002_Figure_2.jpg]]
*Figure 2: Overview of PRISM. (a) A causal joint-factorized VAE compresses per-joint SMPL tokens into a structured 2D latent grid. (b) A flow-matching DiT denoises the grid with per-token timestep embeddings, unifying T2M, pose-conditioned generation, and autoregressive streaming via noise-free condition injection. Self-forcing suppresses drift over long rollouts*



PRISM由两个紧密耦合的核心组件构成（图2）：**因果关节因子化运动VAE**（Causal Joint-Factorized Motion VAE）和**流匹配DiT生成器**（Flow-Matching DiT Generator）。两者通过结构化的2D潜在网格和每标记时间步嵌入实现无缝衔接，无需任务特定的架构修改即可统一文本到动作、姿态条件生成和自回归流式生成。

### 3.1 因果关节因子化运动VAE

#### 动机与瓶颈

现有潜在空间设计（如MotionStreamer的TAE）将每帧运动信息压缩为单一向量，缠绕了根轨迹和每关节旋转，迫使下游生成器隐式解耦这些异构信号，浪费模型容量并限制生成质量。PRISM的核心洞察是：**将每关节作为独立标记，形成时间×关节的2D结构化潜在网格**，从而显式保持运动学结构。

#### 输入表示

VAE的输入被组织为一个2D标记网格，每帧包含根位移、朝向和所有关节旋转：

$$X = \big[ \underbrace{[\mathbf{p}_i; \Delta\mathbf{p}_i]}_{\mathrm{root}}, \underbrace{\boldsymbol{\theta}_i^0}_{\mathrm{orient.}}, \underbrace{\boldsymbol{\theta}_i^1, \ldots, \boldsymbol{\theta}_i^J}_{\mathrm{joint~rotations}} \big]_{i=1}^T \in \mathbb{R}^{T \times K \times 6}$$

其中 $\mathbf{p}_i$ 为根位置，$\Delta\mathbf{p}_i$ 为帧间位移，$\boldsymbol{\theta}_i^0$ 为根朝向，$\boldsymbol{\theta}_i^j$ 为第 $j$ 个关节的旋转（6D连续表示），$T$ 为帧数，$K=J+2$ 为每帧标记数。

#### 编码器-解码器架构

编码器采用**严格因果时序卷积**处理每个关节的时间序列，确保当前帧编码仅依赖过去帧，这对自回归流式生成至关重要。空间维度上使用**关节注意力层**（joint-attention）建模同一帧内不同关节间的交互。解码器对称地使用因果卷积和关节注意力重建SMPL参数。

#### 前向动力学监督

为抑制重建误差在长序列中的累积，VAE训练损失显式包含前向动力学（FK）监督：

$$\mathcal{L}_{\mathrm{VAE}} = \lambda_{\mathrm{param}} \mathcal{L}_{\mathrm{param}} + \lambda_{\mathrm{joints}} \mathcal{L}_{\mathrm{joints}} + \lambda_{\mathrm{traj}} \mathcal{L}_{\mathrm{traj}} + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}}$$

各损失项含义：
- $\mathcal{L}_{\mathrm{param}}$：SMPL参数的L1重建损失
- $\mathcal{L}_{\mathrm{joints}}$：通过FK将预测的旋转参数转换为3D关节点位置后的关节位置损失
- $\mathcal{L}_{\mathrm{traj}}$：对预测的帧间位移 $\Delta\hat{\mathbf{p}}_i$ 进行累积求和得到的**全局轨迹**进行监督，而非仅监督逐帧位移，从而抑制轨迹漂移
- $\mathcal{L}_{\mathrm{KL}}$：潜在空间的KL散度正则化

这种设计使VAE的重建MPJPE相比MotionStreamer的单向量TAE降低18倍（1.82 vs 33.82 mm），rFID降低20倍（0.001 vs 0.020），为下游生成器提供了高质量的潜在空间（Table 4）。

### 3.2 流匹配DiT生成器与噪声自由条件注入

#### 每标记时间步嵌入：统一生成模式的关键

传统扩散/流匹配模型使用单一标量时间步 $t$ 控制整个序列的噪声水平。PRISM的核心创新是**为每个潜在标记分配独立的时间步嵌入**：

- **文本到动作生成**：所有标记接收相同的时间步 $t>0$，进行标准去噪
- **姿态条件生成**：将 $F$ 帧条件姿态通过VAE编码后，注入为 $t=0$ 的干净标记（无噪声），其余标记接收 $t>0$ 进行去噪
- **自回归流式生成**：已生成的片段作为干净条件标记（$t=0$），新片段从纯噪声开始去噪

这一机制使得PRISM无需专用修复网络或混合编码即可原生支持多种生成模式，是统一架构的关键。

#### 自激励训练：弥合训练-推理鸿沟

自回归生成中，推理时使用模型自身输出作为条件，而标准训练使用真实值（教师强制），这种不一致导致长序列中的误差累积。PRISM采用**自激励训练**（Self-Forcing）：训练时随机使用模型自身的去噪输出作为条件标记，模拟推理管道。消融实验（Table 7）表明，自激励训练在BABEL序列生成上取得了最佳的子序列FID（0.100）和最低的转换急动度（Area Under Jerk 0.44），有效抑制了10段以上的长序列漂移。

#### 叙事动作组合

对于长时域叙事文本，PRISM引入**Motion-Aware Text Rewriter**将自由形式叙述分解为原子动作提示序列，然后通过自回归管道逐段生成，实现超训练片段长度的连贯动作合成。



## 实验与关键发现

### 核心实验设置

PRISM在三个主流基准上接受评估：**HumanML3D**（文本到动作）、**MotionHub**（更大规模的文本到动作）和**BABEL**（序列动作生成）。一个关键且对PRISM不利的设定是：所有基线方法操作在HumanML3D原生关节表示上，而PRISM生成SMPL参数并通过前向动力学转换为关节位置——这种跨表示设定会在某些指标上产生评估开销，使得PRISM的优势实际上被低估。所有指标均使用论文自行训练的TMR特征计算，以保证可比性。

### 文本到动作生成：全面领先

Table 1汇总了HumanML3D和MotionHub上的文本到动作结果。PRISM在核心质量指标FID上实现显著突破：

- **HumanML3D**：FID达到**0.027**，相比此前最佳结果（0.060）降低**55%**；R-Precision Top-3达到0.893，与真实运动的0.906仅差1.4%，表明语义对齐已接近数据上限。
- **MotionHub**：FID达到**0.055**，相比此前最佳方法**Go-To-Zero**（Hong et al., arXiv 2025）的0.106降低**48%**，且FID和R-Precision均优于包括**ViMoGen**（Shi et al., arXiv 2025）在内的大规模流匹配模型。

定性对比（Fig. 3）显示，PRISM生成的运动具有明显更少的抖动和足部滑动，物理合理性优于基线。

![[assets/figures/papers/paper_list_l86_https_arxiv_org_abs_2603_08590/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison on text-to-motion. PRISM produces smoother, physically plausible motions with less jitter and foot sliding than baselines*

### 姿态条件生成：零架构修改的泛化

Table 2展示了姿态条件生成结果——模型接收前k帧作为条件，配合文本提示生成剩余运动。PRISM通过噪声自由条件注入原生支持该任务，无需专用修复网络或混合编码。在HumanML3D上，PRISM在多个条件帧数设置下均取得最优FID；在MotionHub上同样保持领先。值得注意的是，这种能力完全来自每标记时间步嵌入的设计，没有引入任何额外的架构组件。

### 序列动作生成：无缝自回归拼接

Table 3报告了BABEL数据集上的序列生成结果。评估分为两个维度：**子序列质量**（Subseq.）评估每段运动的独立质量，**转换平滑度**（Trans.）评估段边界±15帧范围内的连贯性。

PRISM在子序列R@3上达到**0.587**，显著优于**MotionStreamer**（Xiao et al., ICCV 2025）的0.469；更重要的是，转换区域的急动度面积（Area Under Jerk）仅为0.44，而MotionStreamer高出51%。这说明因果VAE和自激励训练共同保证了段间过渡的物理平滑性，避免了自回归生成中常见的突变和漂移。

### 动作标记器重建质量：潜在空间设计的决定性作用

Table 4将PRISM的因果关节因子化VAE与现有标记器进行公平对比——所有标记器均搭配相同的200M DiT生成器，以隔离潜在空间质量的影响。

核心发现：
- 相比**MotionStreamer**的TAE，PRISM VAE将MPJPE从33.82 mm降至**1.82 mm**（**18倍**提升），rFID从0.020降至**0.001**（**20倍**提升）。
- 在MotionHub上，MPJPE从16.02 mm降至**3.04 mm**（**5倍**提升），PA-MPJPE从28.54 mm降至**3.10 mm**（**9倍**提升）。

这些结果表明，每关节因子分解的潜在空间从根本上解决了单向量压缩带来的信息缠绕问题，为下游生成器提供了更高质量的压缩表示。

### 消融实验：因果性、潜在空间维度与训练策略

**因果 vs 非因果VAE**（Table 5）：因果VAE在BABEL序列FID上达到0.100，优于非因果VAE的0.136；子序列R@3更高（0.587 vs 0.543）；同时单段T2M质量保持竞争性（MotionHub FID 0.055 vs 0.060）。这证明因果时序卷积对自回归拼接至关重要，且不损害单段生成能力。

**2D vs 1D潜在空间**（Table 6）：2D关节潜在空间相比1D整体潜在空间将重建MPJPE降低**14倍**（1.99 vs 28.47 mm），生成FID从0.137降至0.055。这直接验证了结构化2D网格的核心价值。

**自回归训练策略**（Table 7）：自激励训练（Self-Forcing）在BABEL上取得了最佳的子序列FID（0.100）和最低的转换急动度（Area Jk. 0.44），优于教师强制（Teacher Forcing）和无激励方案。这证实自激励训练有效弥合了训练-推理差距，抑制了长序列累积误差。

### 叙事动作组合：用户研究验证

Table 8展示了叙事动作组合的用户研究（GSB偏好）。20名评估者对50个叙事提示进行评判（每维度1000次判断）。PRISM在整体偏好上获得**76.4%**的“更好”评价，而MotionStreamer仅获8.8%。在动作完成度、转换平滑度和整体连贯性三个维度上，PRISM均大幅领先。两种方法使用相同的文本分解管道，确保比较的公平性。

### MBench多维评估

Table 9报告了MBench的9维度评估结果，涵盖VLM-based（泛化性、条件一致性）、物理-based（抖动、动力学、足部伪影、地面穿透、身体穿透）和分布-based（姿态质量）三大支柱。PRISM在多个物理合理性指标上表现突出，进一步支持了定性观察。

### 失败模式与局限性

尽管PRISM在各项指标上表现优异，仍存在以下局限：

1. **表示范围受限**：当前模型仅支持SMPL-22身体运动，未包含手部和面部表情。扩展到SMPL-X是自然的下一步，但会增加潜在空间的复杂度。

2. **超长序列漂移**：自激励策略虽有效抑制漂移，但在超过5分钟的极长序列中仍可能累积细微轨迹误差。这可能需要在推理时引入全局轨迹规划或闭环校正机制。

3. **推理速度不足**：生成速度约20 fps（SMPL空间），对于实时交互场景（如游戏、VR）尚不足够。需通过知识蒸馏和架构优化提升吞吐量。

4. **评估体系局限**：VLM-based评估指标仍在开发中，当前可能无法完全反映感知质量。建立更鲁棒、更全面的评估体系仍是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l86_https_arxiv_org_abs_2603_08590/figures/003_Table_1.jpg]]
*Table 1: Text-to-motion on HumanML3D and MotionHub. All metrics are computed using our trained TMR features. “∗” denotes models retrained on the corresponding dataset. Bold: best; underline: second best*

![[assets/figures/papers/paper_list_l86_https_arxiv_org_abs_2603_08590/figures/005_Table_2.jpg]]
*Table 2: Pose-conditioned generation on HumanML3D and MotionHub. The model receives the first k frames as a noise-free condition together with a text prompt, and generates the remaining motion. All metrics are computed using our trained TMR features. Bold: best; underline: second best*

![[assets/figures/papers/paper_list_l86_https_arxiv_org_abs_2603_08590/figures/006_Table_3.jpg]]
*Table 3: Sequential action generation on BABEL [26]. “Subseq.” evaluates per-segment motion quality; “Trans.” evaluates the smoothness at segment boundaries (±15 frames)*

![[assets/figures/papers/paper_list_l86_https_arxiv_org_abs_2603_08590/figures/007_Table_4.jpg]]
*Table 4: Motion tokenizer comparison on HumanML3D and MotionHub. Reconstruction quality measured by rFID, MPJPE, PA-MPJPE, and MPJRE. All tokenizers are paired with the same 200M DiT for a fair comparison of latent space quality. Bold: best; underline: second best*

![[assets/figures/papers/paper_list_l86_https_arxiv_org_abs_2603_08590/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative comparison on long-horizon narrative composition. PRISM follows all sub-actions with smooth transitions, while MotionStreamer misses several actions and exhibits drift*

![[assets/figures/papers/paper_list_l86_https_arxiv_org_abs_2603_08590/figures/009_Table_5.jpg]]
*Table 5: Causal vs. non-causal Motion VAE. Downstream generation quality on T2M (MotionHub), TP2M (HumanML3D, 1-frame), and BABEL sequential. Both variants share the same 1.4B DiT*

![[assets/figures/papers/paper_list_l86_https_arxiv_org_abs_2603_08590/figures/010_Table_7.jpg]]
*Table 7: Autoregressive training strategy comparison on BABEL [26]. All variants share the same 1.4B DiT with noise-free condition injection*

![[assets/figures/papers/paper_list_l86_https_arxiv_org_abs_2603_08590/figures/011_Table_6.jpg]]
*Table 6: 2D vs. 1D latent space. Recon. and T2M gen. on MotionHub*

![[assets/figures/papers/paper_list_l86_https_arxiv_org_abs_2603_08590/figures/012_Table_8.jpg]]
*Table 8: User study on narrative motion composition (GSB preference). Percentage of trials where PRISM is judged Good / Same / Bad vs. MotionStreamer, by 20 evaluators on 50 narrative prompts (1,000 judgments per dimension). Both methods use the same decomposition pipeline*

![[assets/figures/papers/paper_list_l86_https_arxiv_org_abs_2603_08590/figures/013_Table_9.jpg]]
*Table 9: Results on MBench [16]. MBench evaluates 9 dimensions across three pillars: VLM-based (generalizability, condition consistency), physics-based (jitter, dynamics, foot artifacts, ground penetration, body penetration), and distribution-based (pose quality). ↑ = higher is better; ↓ = lower is better. Scores are from the official MBench leaderboard except those marked with † (evaluated by us)*



## 定位与知识库关联

### 1. 核心瓶颈与因果调控变量

PRISM 的核心洞察源于对现有流式运动生成方法瓶颈的精准诊断：**潜在空间设计的结构性缺陷**。现有方法（如 **MotionStreamer** (Xiao et al., ICCV 2025)）将每帧运动信息压缩为单一向量，将根轨迹、朝向和每关节旋转等异构信号强制缠绕在同一表示中。这迫使下游生成器隐式地解耦这些信号，显著浪费模型容量，并限制了生成质量与可控性。

PRISM 提出的因果调控变量是**将每关节作为独立标记（token），形成结构化的2D潜在网格（时间×关节）**。这一设计配合因果VAE和前向动力学监督，显式保持了运动学结构，并允许对每个标记独立注入噪声或条件。基于此，一个流匹配Transformer可以**无需任务特定修改**地统一文本到动作、姿态条件生成和自回归流式生成。

### 2. 与基线工作的差异化定位

PRISM 通过四个关键设计槽位的改变，在运动生成的潜在空间设计、时序建模、条件注入和训练策略四个维度上与现有工作形成系统性差异：

| 设计槽位 | 基线方法典型取值 | PRISM 取值 | 关键影响 |
|:---|:---|:---|:---|
| **潜在标记化粒度** | 每帧单一向量（MotionStreamer, MLD） | 每关节独立标记（T×J 2D网格） | 重建MPJPE降低18×，rFID降低20× |
| **时序编码因果性** | 双向（非因果）卷积 | 严格因果时序卷积 | 无缝自回归拼接，同时保持单段质量 |
| **条件注入机制** | 单一标量时间步或专用修复网络 | 每标记时间步嵌入（t=0表示干净条件） | 无需架构修改即可统一多种生成模式 |
| **自回归训练策略** | 教师强制（使用真实值作为条件） | 自激励训练（使用模型自身输出） | 长序列生成中显著抑制漂移 |

**与具体基线的对比：**

- **MotionStreamer** (Xiao et al., ICCV 2025)：同为流式自回归扩散生成方法，但使用每帧单一潜在向量和非因果编码器。PRISM 在 BABEL 序列生成中，子序列 R@3 从 0.469 提升至 0.587，转换急动度（Area Under Jerk）降低 51%（Table 3）。在叙事动作组合的用户研究中，PRISM 获得 76.4% 的整体偏好，而 MotionStreamer 仅 8.8%（Table 8）。

- **MLD** (Chen et al., ICLR 2024)：潜在扩散模型，使用整体帧级潜在表示。PRISM 的每关节因子分解在重建精度上形成数量级优势。

- **MoMask** (Guo et al., CVPR 2024)：掩码Transformer生成方法。PRISM 在 HumanML3D 上 FID 为 0.027，显著优于 MoMask 的 0.060（Table 1）。

- **Go-To-Zero** (Hong et al., arXiv 2025)：自回归VQ生成方法。PRISM 在 MotionHub 上 FID 为 0.055，相比 Go-To-Zero 的 0.106 提升 48%（Table 1）。

- **FlowMDM** (Dai et al., ECCV 2024)：流匹配与混合位置编码方法。PRISM 在扩散框架上共享流匹配思想，但通过结构化潜在空间和每标记时间步嵌入实现了更灵活的条件注入。

- **ViMoGen** (Shi et al., arXiv 2025)：大规模流匹配模型。PRISM 在模型规模上可能较小，但通过潜在空间的结构化设计实现了更高效的表示。

### 3. 适用边界与局限

**当前适用边界：**
- 支持 SMPL-22 身体运动（不含手部和面部表情），扩展到 SMPL-X 是自然下一步。
- 生成速度约 20 fps（SMPL 空间），对于实时交互场景尚不足，需通过蒸馏和架构优化提升。
- 自激励策略虽有效抑制漂移，但非常长序列（>5分钟）仍可能累积细微轨迹误差，可能需要全局轨迹规划。

**评估公平性说明：**
所有基线方法操作在 HumanML3D 原生关节表示上，而 PRISM 生成 SMPL 参数并通过前向动力学转换为关节位置。这种跨表示设定可能在某些指标上产生评估开销，对 PRISM 不利——即便如此，PRISM 仍取得了最优结果。在叙事动作组合的用户研究中，PRISM 和 MotionStreamer 使用相同的文本分解管道，确保生成质量的公平比较。

### 4. 开放问题

1. **完整人体建模**：如何扩展模型以处理完整的 SMPL-X（含手部和面部表情），同时保持结构化潜在空间的计算效率？

2. **超长序列稳定性**：如何在数分钟级别的超长序列中进一步抑制轨迹漂移？是否需要引入全局轨迹规划或分层时间建模？

3. **实时交互生成**：能否通过知识蒸馏和架构优化（如减少 DiT 推理步数、使用更轻量的解码器）实现实时交互式的生成？

4. **评估体系鲁棒性**：VLM-based 评估指标仍在开发中，当前可能无法完全反映感知质量。如何建立更鲁棒、多维度的评估体系来捕捉运动生成的物理合理性、语义一致性和时序连贯性？

5. **多模态条件扩展**：每标记时间步嵌入的框架天然支持多模态条件注入（如音乐、语音、场景上下文），如何有效利用这一灵活性进行跨模态运动生成？



## 原文 PDF

![[paperPDFs/arxiv_2026/PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition.pdf]]
