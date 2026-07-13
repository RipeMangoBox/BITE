---
title: "MoCapAnything V2: End-to-End Motion Capture for Arbitrary Skeletons"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/MoCapAnything_V2_End_to_End_Motion_Capture_for_Arbitrary_Skeletons.pdf
project_link: https://animotionlab.github.io/MoCapAnythingV2/
code_link: null
aliases:
- MV
- MVEEMCAS
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 在目标资产的静止姿态之外，额外引入一个参考姿态-旋转对作为坐标轴锚点。该参考对与静止姿态共同完整定义了关节的局部坐标系，将多值P→R映射转化为良好约束的条件预测问题，从而使P→R模块变得可学习。
primary_logic: 静止姿态仅提供坐标系原点，而参考姿态-旋转对提供了坐标轴方向。两者结合将病态的P→R映射转化为可学习的条件预测任务，进而解锁了整个V→P→R管线的端到端联合优化——梯度从旋转损失回传至视觉编码器，使中间姿态表示不再是单纯的位置精度优化目标，而是自动重塑为最有利于旋转恢复的表示形式。这一能力是因子化管线（带有不可微IK）无法实现的。
claims:
- 添加参考姿态-旋转对使Zoo-Unseen旋转误差从24.05°骤降至6.54°，证明坐标轴锚定是解决P→R病态性的关键
- 端到端联合训练（含梯度耦合）相比梯度截断变体，Zoo-Unseen角度误差从7.82°进一步降至6.54°，证明V→P与P→R协同优化的收益
- 去除网格中间表示在保持旋转精度的同时实现了约20倍推理加速，且避免了预测网格的误差累积
- 显式关节位置中间表示是必要的结构瓶颈——直接V→R变体在Zoo-Unseen上仅23.73°，而显式姿态中间表示达到6.54°
---

# MoCapAnything V2: End-to-End Motion Capture for Arbitrary Skeletons

> [!tip] 核心洞察
> 静止姿态仅提供坐标系原点，而参考姿态-旋转对提供了坐标轴方向。两者结合将病态的P→R映射转化为可学习的条件预测任务，进而解锁了整个V→P→R管线的端到端联合优化——梯度从旋转损失回传至视觉编码器，使中间姿态表示不再是单纯的位置精度优化目标，而是自动重塑为最有利于旋转恢复的表示形式。这一能力是因子化管线（带有不可微IK）无法实现的。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoCapAnything V2：面向任意骨骼的端到端动作捕捉 |
| 英文题名 | MoCapAnything V2: End-to-End Motion Capture for Arbitrary Skeletons |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2604.28130v1) · [Project](https://animotionlab.github.io/MoCapAnythingV2/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MoCapAnything V2 |
| Dataset | Truebones Zoo-Seen, Truebones Zoo-Rare, Truebones Zoo-Unseen, Objaverse |

> [!tip] 效果简介
> - Truebones Zoo-Seen 上，Ang. Err (°) 10.73 vs 19.67 (VIBE) (-8.94)；MPJPE (cm) 2.34 vs 19.66 (GLoT) (-17.32)。
> - Truebones Zoo-Rare 上，Ang. Err (°) 14.38 vs 24.72 (HRNet) (-10.34)。
> - Truebones Zoo-Unseen 上，Ang. Err (°) 6.54 vs 24.46 (ViTPose) (-17.92)。

## 概要

从单目视频中恢复任意骨骼结构的运动捕捉，面临一个根本性的病态问题：相同的3D关节位置，在不同骨骼的静止姿态和局部坐标轴约定下，可以对应完全不同的关节旋转值。现有方法——包括因子化管线 **MoCapAnything V1**（Gong et al., arXiv 2025）——将问题拆解为“视频→姿态（V→P）”和“姿态→旋转（P→R）”两个阶段，但P→R阶段依赖不可微的解析逆运动学（IK），既无法解决骨骼轴向扭转等欠约束自由度，也切断了梯度回传，使V→P阶段无法针对最终旋转目标进行优化。

**MoCapAnything V2** 的核心洞察在于：静止姿态仅提供了关节坐标系的**原点**，而缺少**坐标轴方向**。为此，方法在目标资产的静止姿态之外，额外引入一个参考姿态-旋转对作为坐标轴锚点。这一简单的扩展将多值的P→R映射转化为良好约束的条件预测问题，使P→R模块变得可学习，进而解锁了整个V→P→R管线的端到端联合优化——梯度从旋转损失回传至视觉编码器，使中间姿态表示自动重塑为最有利于旋转恢复的形式。

在方法定位上，MoCapAnything V2 是首个面向任意骨骼的**完全端到端可学习**动作捕捉框架。它消除了V1中的网格中间表示和解析IK，代之以直接从视频预测3D关节位置的V→P模块和参考条件化的可学习P→R模块，两阶段共享GL-GMHA（全局-局部图引导多头注意力）结构骨干，并联合优化。

实验结果表明，该方法在 Truebones Zoo 和 Objaverse 基准上实现了显著提升：平均旋转角度误差从因子化管线的约17°降至约10°，在未见骨骼（Zoo-Unseen）上进一步降至6.54°；同时，去除网格中间表示带来了约20倍的推理加速。消融实验系统性地验证了参考条件化、端到端联合训练和显式关节位置瓶颈各自的贡献：无参考对时Zoo-Unseen误差骤升至24.05°，梯度截断变体升至7.82°，直接V→R变体仅23.73°，分别证明了坐标轴锚定、梯度耦合和显式中间表示的必要性。



### 问题背景：从单目视频到任意骨骼动作捕捉

从单目视频中恢复三维人体运动是计算机视觉与图形学的长期目标。近年来，基于参数化人体模型（如SMPL）的方法取得了显著进展，但其核心假设——所有目标对象共享相同的骨骼拓扑——严重限制了应用的边界。现实世界中的动作捕捉需求远超人体范畴：从四足动物到鸟类的运动分析、从虚拟角色到机器人遥操作，目标骨骼的拓扑结构、关节数量、肢体比例和静止姿态千差万别。因此，**面向任意骨骼的动作捕捉**——即从单目视频输入直接输出与目标资产骨骼兼容的动画就绪旋转——成为一个具有高度实用价值但极具挑战性的开放问题。

### 现有方法及其结构性缺口

现有方法可大致分为两类，各自存在根本性局限。

**第一类：因子化管线（Factorized Pipeline）。** 代表性工作MoCapAnything V1（Gong et al., arXiv 2025）将问题分解为两个阶段：首先从视频预测4D网格，再从网格中提取3D关节位置（Video-to-Pose），随后通过解析逆运动学（IK）将关节位置转化为关节旋转（Pose-to-Rotation）。这一设计存在两个结构性缺陷：

1. **不可微的IK切断了梯度回传。** 解析IK是纯几何运算，梯度无法从旋转损失回传至姿态预测器。这意味着V→P模块只能以位置精度为优化目标，而无法感知下游旋转恢复的实际需求——即使位置误差很小，IK阶段仍可能产生关节抖动或肢体翻转（见Fig. 4的定性对比）。

2. **网格中间表示引入冗余计算与误差累积。** 网格预测本身是高维重建任务，不仅推理耗时（处理120帧序列需20分钟以上），且预测网格的误差会传导至后续的姿态提取和旋转恢复阶段。表2显示，V1使用预测网格时角度误差为18.9°，而使用真实网格时降至10.2°，说明网格预测质量成为性能瓶颈。

**第二类：端到端方法（End-to-End）。** 传统端到端方法直接从视频回归旋转（V→R），绕过了显式的姿态中间表示。然而，这类方法在跨骨骼泛化场景中表现糟糕——如表5所示，直接V→R变体在Zoo-Unseen上的角度误差高达23.73°。原因在于，旋转空间与视觉外观之间的映射高度依赖骨骼拓扑，缺乏结构化的中间表示使得模型难以将视觉特征有效地映射到任意骨骼的旋转空间。

### 核心瓶颈：从关节位置到旋转的病态映射

上述方法共同指向一个更深层的根本问题：**从关节位置恢复关节旋转本质上是一个病态问题（ill-posed problem）。**

给定一组3D关节位置 $\mathbf{P}$ 和目标骨骼的静止姿态 $\mathbf{o}$，映射 $\mathbf{R} = f(\mathbf{P}, \mathbf{o})$ 是多值函数——相同的关节位置，在不同的局部坐标轴约定下，可以对应完全不同的旋转值。静止姿态仅提供了关节坐标系的原点（即骨骼偏移量），但并未定义坐标轴的方向。以人体肘关节为例：已知手腕相对于肘部的位置，可以确定前臂的指向，但前臂绕自身长轴的旋转（轴向扭转）是完全自由的——这一自由度在位置空间中不可观测，却是旋转空间中必须确定的关键分量。

解析IK通过手工设计的启发式规则（如最小化角速度或参考预定义扭转方向）来填补这些欠约束自由度，但其选择未必与真实运动一致，且无法针对下游任务（如动画质量）进行优化。因子化管线中不可微的IK阶段进一步固化了这一缺陷——即使姿态预测器产出了更精确的位置，IK的启发式选择仍可能导致不合理的旋转。

### 本文动机与核心思路

针对上述瓶颈，本文提出**MoCapAnything V2**，核心动机在于两点：

**动机一：将病态映射转化为可学习问题。** 既然静止姿态仅提供坐标系原点，那么额外引入**参考姿态-旋转对（reference pose–rotation pair）** 作为坐标轴锚点，就可以完整定义关节的局部坐标系。该参考对与静止姿态共同锚定了P→R映射的坐标约定，将原本多值的病态映射转化为良好约束的条件预测问题，从而使P→R模块变得可学习。

**动机二：解锁端到端联合优化。** 一旦P→R模块可学习，整个V→P→R管线就可以端到端联合训练。梯度从旋转损失回传至视觉编码器，使中间姿态表示不再仅仅是位置精度的优化目标，而是自动重塑为最有利于旋转恢复的表示形式——这一能力是任何带有不可微IK的因子化管线无法实现的。

同时，本文直接预测3D关节位置作为中间表示，消除了V1中的网格瓶颈，在保持旋转精度的同时实现约20倍推理加速。通过GL-GMHA（全局-局部图引导多头注意力）作为共享结构骨干，模型天然适应多样化的骨骼拓扑，无需针对不同骨骼重新设计网络架构。



## 核心方法与创新机理

MoCapAnything V2 的核心创新在于将面向任意骨骼的动作捕捉管线从**因子化、不可微的两阶段设计**重构为**端到端可学习的统一架构**，并引入**参考条件化旋转建模**以解决从关节位置恢复旋转这一根本性病态问题。以下从三个 changed slots 展开分析。

### 1. 从因子化管线到端到端可学习架构

**基线瓶颈**：MoCapAnything V1（Gong et al., arXiv 2025）采用因子化设计——Video-to-Pose（V→P）阶段学习预测关节位置，Pose-to-Rotation（P→R）阶段则依赖不可微的解析逆运动学（IK）求解旋转。这一设计的致命缺陷在于：IK 阶段切断了梯度回传，使 V→P 模块无法针对最终旋转目标进行优化。V1 的中间表示是 4D 网格——模型先预测网格，再从网格中提取姿态——这引入了额外的推理开销和误差累积路径。

**核心改变**：V2 将两个阶段均实现为可学习神经模块，并在统一损失函数下进行端到端联合优化。损失函数为：

$$\mathcal{L} = \lambda_{\mathrm{pos}} \mathcal{L}_{\mathrm{pos}} + \lambda_{\mathrm{rot}} \mathcal{L}_{\mathrm{rot}} + \lambda_{\mathrm{rot\_v}} \mathcal{L}_{\mathrm{rot\_v}} + \lambda_{\mathrm{root}} \mathcal{L}_{\mathrm{root}}$$

其中旋转损失 $\mathcal{L}_{\mathrm{rot}}$ 的梯度可回传至 V→P 模块，使中间姿态表示不再单纯追求位置精度，而是**自动重塑为最有利于旋转恢复的表示形式**。这一能力是因子化管线（带不可微 IK）无法实现的。

**因果证据**：Table 3 的消融实验直接验证了这一因果机制的强度——将端到端联合训练替换为梯度截断变体（V→P 与 P→R 独立优化），Zoo-Unseen 旋转误差从 6.54° 显著退化至 7.82°，证实梯度耦合是性能增益的关键来源。

**效率跃升**：V2 同时消除了网格中间表示，直接从视频预测 3D 关节位置。Table 2 显示，这一改变在保持旋转精度优势的同时（Ours 10.6° vs V1 GT Mesh 18.9°），实现了约 20 倍推理加速——处理 120 帧序列从 V1 的 20+ 分钟降至约 1 分钟。

### 2. 参考姿态-旋转对：将病态映射转化为可学习问题

**问题本质**：从关节位置 $\mathbf{P}$ 恢复旋转 $\mathbf{R}$ 本质上是病态的——映射 $\mathbf{R} = f(\mathbf{P}, \mathbf{o})$ 中，相同的关节位置在不同骨骼的静止姿态 $\mathbf{o}$ 和局部坐标轴约定下，可以对应完全不同的旋转值。静止姿态仅提供坐标系原点，但无法确定坐标轴方向，导致骨骼轴向扭转等欠约束自由度无法被唯一确定。

**创新机制**：V2 在静止姿态之外，额外引入一个**参考姿态-旋转对**作为坐标轴锚点。该参考对与静止姿态共同完整定义了关节的局部坐标系——静止姿态提供原点，参考对提供轴方向——从而将多值的 P→R 映射转化为良好约束的条件预测问题。

**决定性证据**：Table 4 的消融实验以极高的置信度验证了这一机制的因果效应。在 Zoo-Unseen 上：
- 无参考对时，旋转误差高达 **24.05°**，模型完全无法泛化至未见骨骼；
- 仅添加参考对（无静止姿态编码），误差骤降至 **7.37°**；
- 结合静止姿态与参考对，误差进一步降至 **6.54°**。

24.05° → 6.54° 的降幅（约 73%）直接证明了坐标轴锚定是解决 P→R 病态性的**必要且充分条件**。需要指出的是，参考对是从目标资产中采样得到的单个姿态-旋转对，而非需要大量标注数据——这一设计的实用价值在于，只需为每个新骨骼提供一帧参考即可实现泛化。

### 3. GL-GMHA：全局-局部交替的图引导注意力

V2 在两个阶段共享的结构骨干中引入了 **GL-GMHA（Global-Local Graph-guided Multi-Head Attention）**。其核心设计是交替使用两种互补的注意力模式：
- **局部层**：沿运动链限制注意力范围，建模关节内依赖；
- **全局层**：允许全连接，建模跨分支协调（如四肢间的运动耦合）。

这一设计天然泛化至多样骨骼拓扑——不同骨骼的关节数量和连接关系各异，但运动链的局部结构具有普适性。Table 6 的消融实验显示，GL-GMHA 的交替设计优于纯全局 GMHA 和纯局部变体；仅使用局部注意力时，Zoo-Rare 上旋转误差从 14.38° 退化至 16.91°，说明跨分支全局建模对复杂骨骼运动（如稀有物种）至关重要。

### 4. 显式关节位置瓶颈的结构必要性

V2 坚持保留显式的关节位置中间表示（而非直接从视频回归旋转），这一设计选择有深层原因。Table 5 的消融实验显示，直接 V→R 变体在 Zoo-Unseen 上仅达到 23.73°，而显式姿态中间表示（Full）达到 6.54°。显式关节位置作为结构瓶颈，迫使模型学习可解释的中间几何表示，这对跨骨骼泛化起到了关键的**正则化作用**——不同骨骼的旋转空间差异巨大，但关节位置空间具有更强的跨骨骼不变性。

**总结**：MoCapAnything V2 的创新链条呈现清晰的因果逻辑——参考条件化解决了 P→R 的病态性（必要条件），端到端联合优化释放了 V→P 与 P→R 的协同潜力（充分条件），而 GL-GMHA 和显式姿态瓶颈则为这一框架提供了跨骨骼泛化的结构基础。三者缺一不可，共同构成了从“因子化不可微”到“端到端可学习”的范式转变。



MoCapAnything V2 将任意骨骼的动作捕捉问题分解为一个端到端可学习的**两阶段管线**：

$$
\mathrm{Video} \xrightarrow{\mathrm{Stage~1}} \mathrm{Pose} \xrightarrow{\mathrm{Stage~2}} \mathrm{Rotation}
$$

**第一阶段（Video-to-Pose, V→P）** 从单目视频直接预测目标骨骼的 3D 关节位置序列；**第二阶段（Pose-to-Rotation, P→R）** 从预测的关节位置恢复关节旋转。两个阶段均为可学习的神经模块，并通过联合损失进行端到端优化——这是任意骨骼动作捕捉领域首次实现 V→P→R 全管线梯度耦合（Abstract; §3.2）。

### 与 V1 的架构对比

MoCapAnything V1（Gong et al., arXiv 2025）采用因子化设计：学习 V→P 模块预测 4D 网格，再通过不可微的解析 IK 从网格提取姿态并求解旋转。该设计存在两个根本性局限（Fig. 2）：
- **网格中间表示**带来高昂的计算开销（处理 120 帧需 20+ 分钟）和误差累积；
- **不可微 IK**切断了梯度回传，使 V→P 模块无法针对最终旋转目标进行优化。

![[assets/figures/papers/paper_list_l56_https_arxiv_org_abs_2604_28130v1/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of MoCapAnything V1 and V2. Unlike V1, which depends on mesh-conditioned video-to-pose estimation and analytical inverse kinematics (IK) for rotation recovery, V2 eliminates mesh conditioning and introduces a fully learnable Pose2Rot module. The entire pipeline is optimized end-to-end, enabling bidirectional coupling between pose and rotation for improved robustness and animation-ready motion synthesis*

V2 做出了两项核心架构变革：
1. **消除网格中间表示**，直接从视频预测 3D 关节位置，推理速度提升约 20 倍（§4.10）；
2. **将 P→R 阶段替换为可学习的神经模块**，使整个管线可端到端联合优化。

### 模块构成与数据流

完整框架如 Fig. 3 所示，包含以下核心模块：

**Video-to-Pose 阶段**（§3.4）：
- **Reference Query Encoder**：以目标资产的参考帧（骨骼结构 + 视觉外观）为输入，编码生成参考关节查询嵌入 $Q^{\mathrm{ref}}$，为姿态预测提供骨骼拓扑条件；
- **Temporal Pose Decoder**：以 $Q^{\mathrm{ref}}$ 和逐帧视频特征为输入，通过时序 Transformer（含 RoPE 位置编码）逐帧预测 3D 关节位置序列 $P$。

**Pose-to-Rotation 阶段**（§3.5）：
- **Rest Pose Encoder**：编码目标骨骼的静止姿态（骨骼偏移）和拓扑结构，生成静止姿态嵌入 $\bar{\mathbf{E}}^{\mathrm{rest}} \in \mathbb{R}^{J \times d}$；
- **Reference Encoder（Anchor Encoder）**：联合嵌入一个参考姿态-旋转对，生成坐标轴锚定特征 $\mathbf{C}^{\mathrm{ref}}$，与静止姿态共同完整定义关节局部坐标系；
- **Pose Encoder**：编码预测的关节位置序列 $P$，结合 GL-GMHA 空间推理和时序注意力；
- **Rotation Decoder**：从姿态特征预测每帧每关节的 6D 旋转参数，内部包含 FiLM 调制、时序自注意力、GL-GMHA 空间注意力、参考交叉注意力和前馈网络。

**共享结构骨干**（§3.3）：
两个阶段均采用 **GL-GMHA（Global-Local Graph-guided Multi-Head Attention）** 作为空间推理骨干。该机制交替使用两种注意力模式：
- **局部层**沿运动链限制注意力范围，建模关节内依赖；
- **全局层**允许全连接，建模跨分支协调。

这种交替设计使模型天然泛化至多样骨骼拓扑，无需针对不同骨骼结构调整架构。

### 端到端训练策略

整个管线通过联合损失进行端到端优化（§3.6）：

$$
\mathcal{L} = \lambda_{\mathrm{pos}} \mathcal{L}_{\mathrm{pos}} + \lambda_{\mathrm{rot}} \mathcal{L}_{\mathrm{rot}} + \lambda_{\mathrm{rot\_v}} \mathcal{L}_{\mathrm{rot\_v}} + \lambda_{\mathrm{root}} \mathcal{L}_{\mathrm{root}}
$$

四项损失分别约束位置误差、旋转角度误差、旋转角速度误差和根关节旋转误差（权重 $\lambda_{\mathrm{pos}}=\lambda_{\mathrm{rot}}=\lambda_{\mathrm{rot\_v}}=1.0$，$\lambda_{\mathrm{root}}=0.1$）。

为解决训练-推理分布差距，V2 采用**混合姿态训练策略**：训练中向 P→R 模块馈送预测姿态（而非真实姿态）的概率随训练轮数线性增加：

$$
p_{\mathrm{pred}}(e) = p_{\mathrm{start}} + (p_{\mathrm{end}} - p_{\mathrm{start}}) \cdot \min\left(1, \frac{e}{E_{\mathrm{warmup}}}\right)
$$

其中 $p_{\mathrm{start}}=0.1$，$p_{\mathrm{end}}=1.0$，$E_{\mathrm{warmup}}=30$。消融实验表明，纯真实姿态训练（GT-only）在 Zoo-Unseen 上角度误差高达 13.28°，而混合策略（$E_w=30$）降至 6.54°，证明弥合分布差距对跨骨骼泛化至关重要（Table 3）。

### 端到端优化的关键收益

端到端联合训练使梯度从旋转损失回传至视觉编码器，中间姿态表示不再仅是位置精度优化目标，而是被自动重塑为最有利于旋转恢复的表示形式。消融实验直接验证了这一收益：相比梯度截断变体，联合训练将 Zoo-Unseen 角度误差从 7.82° 进一步降至 6.54°（Table 3）。这一能力是因子化管线（带有不可微 IK）无法实现的。

### 补充图表

![[assets/figures/papers/paper_list_l56_https_arxiv_org_abs_2604_28130v1/figures/001_Figure_1.jpg]]
*Figure 1: Overview of MoCapAnything V2. Given an input video of a human or an animal, our method infers a topology-agnostic skeleton sequence across diverse skeleton topologies. Conditioned on a reference asset, the model predicts animation-ready rotations via an end-to-end framework, enabling the reference asset to perform the input motion*



### 问题形式化与两阶段分解

MoCapAnything V2 将任意骨骼的动作捕捉形式化为一个两阶段映射问题：

$$\mathrm{Video} \xrightarrow{\mathrm{Stage~1}} \mathrm{Pose} \xrightarrow{\mathrm{Stage~2}} \mathrm{Rotation}$$

其中 Stage 1（Video-to-Pose，V→P）从单目视频预测 3D 关节位置序列 $\mathbf{P} \in \mathbb{R}^{T \times J \times 3}$，Stage 2（Pose-to-Rotation，P→R）从关节位置恢复关节旋转 $\mathbf{R}$。两个阶段均为可学习的神经模块，且进行端到端联合优化——这是首个实现此能力的任意骨骼动作捕捉框架。

### 核心瓶颈：P→R 映射的病态性

从关节位置恢复旋转本质上是一个病态问题。仅依赖关节位置 $\mathbf{P}$ 和静止姿态骨骼偏移 $\mathbf{o}$ 的映射：

$$\mathbf{R} = f(\mathbf{P}, \mathbf{o})$$

是多值函数：相同的关节位置在不同骨骼的局部坐标轴约定下，可以对应完全不同的旋转值。静止姿态仅提供坐标系的**原点**，而坐标轴方向（尤其是骨骼轴向扭转）仍处于欠约束状态。V1 采用的不可微解析 IK 无法解决这一问题，且切断了从旋转损失到视觉编码器的梯度回传路径。

### 关键使能技术：参考条件化 P→R 模块

为解决上述病态性，P→R 模块在静止姿态之外引入一个**参考姿态-旋转对**作为坐标轴锚点。该参考对与静止姿态共同完整定义了关节的局部坐标系——静止姿态提供原点，参考对提供坐标轴方向——将多值映射转化为良好约束的条件预测问题。

P→R 模块由四个子模块组成：

1. **Rest Pose Encoder**：编码目标骨骼的静止姿态（骨骼偏移和拓扑结构），输出静止姿态嵌入 $\bar{\mathbf{E}}^{\mathrm{rest}} \in \mathbb{R}^{J \times d}$。
2. **Reference Encoder (Anchor Encoder)**：联合嵌入参考姿态-旋转对，生成坐标轴锚定特征 $\mathbf{C}^{\mathrm{ref}}$。
3. **Pose Encoder**：编码预测的关节位置序列 $\mathbf{P}$，结合 GL-GMHA 空间推理和时序注意力。
4. **Rotation Decoder**：从姿态特征预测每帧每关节的 6D 旋转参数，包含 FiLM 调制、时序自注意力、GL-GMHA 空间注意力、参考交叉注意力和前馈网络。其中参考交叉注意力将锚定特征 $\mathbf{C}^{\mathrm{ref}}$ 注入解码过程，是实现 P→R 可学习化的核心机制。

### 共享结构骨干：GL-GMHA

两个阶段共享同一个结构骨干——全局-局部图引导多头注意力（Global-Local Graph-guided Multi-Head Attention, GL-GMHA）。其核心设计是交替使用两种互补注意力模式：

- **局部层**：沿运动链限制注意力范围，建模关节内的父子依赖关系。
- **全局层**：允许全连接注意力，建模跨分支（如四肢间）的协调关系。

这种交替设计使模型既能精细捕捉局部运动学约束，又能建模全局协调，且天然泛化至多样骨骼拓扑。

### 训练策略与损失函数

端到端联合训练的总损失函数为：

$$\mathcal{L} = \lambda_{\mathrm{pos}} \mathcal{L}_{\mathrm{pos}} + \lambda_{\mathrm{rot}} \mathcal{L}_{\mathrm{rot}} + \lambda_{\mathrm{rot\_v}} \mathcal{L}_{\mathrm{rot\_v}} + \lambda_{\mathrm{root}} \mathcal{L}_{\mathrm{root}}$$

其中 $\mathcal{L}_{\mathrm{pos}}$ 为关节位置误差，$\mathcal{L}_{\mathrm{rot}}$ 为旋转角度误差，$\mathcal{L}_{\mathrm{rot\_v}}$ 为旋转角速度误差（促进时序平滑），$\mathcal{L}_{\mathrm{root}}$ 为根关节旋转误差。权重设置为 $\lambda_{\mathrm{pos}} = \lambda_{\mathrm{rot}} = \lambda_{\mathrm{rot\_v}} = 1.0$，$\lambda_{\mathrm{root}} = 0.1$。

为弥合训练-推理分布差距，采用**混合姿态训练策略**：训练中向 P→R 模块馈送预测姿态（而非真实姿态）的概率随训练轮数线性增加：

$$p_{\mathrm{pred}}(e) = p_{\mathrm{start}} + (p_{\mathrm{end}} - p_{\mathrm{start}}) \cdot \min\left(1, \frac{e}{E_{\mathrm{warmup}}}\right)$$

其中 $p_{\mathrm{start}} = 0.1$，$p_{\mathrm{end}} = 1.0$，$E_{\mathrm{warmup}} = 30$。该调度使 P→R 模块在训练初期从真实姿态中学习稳定的旋转映射，随后逐步适应预测姿态的噪声分布，最终实现与 V→P 模块的协同优化。

### 补充图表

![[assets/figures/papers/paper_list_l56_https_arxiv_org_abs_2604_28130v1/figures/003_Figure_3.jpg]]
*Figure 3: Framework of MoCapAnything V2. Our method unifies video-to-pose and pose-to-rotation within a single end-to-end trainable architecture. The video-to-pose stage consists of a reference-conditioned pose prompt encoder (A), which encodes skeleton and image cues into joint prompt, and a unified pose decoder (B), which predicts temporally coherent joint positions via cross-attention with video features. The pose-to-rotation stage is formulated as a learnable inverse kinematics module, composed of a rotation prompt encoder (C) that maps predicted poses into rot prompt, an anchor encoder (D) that encodes reference pose–rotation pairs to establish a consistent rotation coordinate space, and a unifi...*



## 实验与关键发现

### 核心实验设计

MoCapAnything V2 在 **Truebones Zoo**（Seen / Rare / Unseen 三个泛化难度）和 **Objaverse（Obj）** 四个评估集上与多个基线进行了系统对比。所有基线方法——**HRNet**（Sun et al., CVPR 2019）、**ViTPose**（Xu et al., NeurIPS 2022）、**VIBE**（Kocabas et al., CVPR 2020）、**GLoT**（Shen et al., CVPR 2023）——均配备了统一的可学习旋转模块并进行了端到端联合训练，确保对比公平。唯一的例外是 **MoCapAnything V1**（Gong et al., arXiv 2025），由于其因子化设计的固有约束，V1 使用传统的不可微解析 IK。

评估指标包含两个维度：**MPJPE（cm）**衡量关节位置精度，**Ang. Err（°）**衡量关节旋转角度误差。所有指标使用逐关节掩码处理不同骨骼的可变关节数量，并进行统一的尺度归一化。

### 主实验结果

Table 1 展示了全面对比结果。MoCapAnything V2 在所有评估集上均以显著优势超越所有基线。

![[assets/figures/papers/paper_list_l56_https_arxiv_org_abs_2604_28130v1/figures/004_Table_1.jpg]]
*Table 1: Main results on Zoo (Seen/Rare/Unseen) and Obj. Position in cm (↓); rotation in degrees (↓). All baselines are trained jointly end-to-end with learnable rotation modules; only V1 uses traditional IK. Best angle error per split in bold*

![[assets/figures/papers/paper_list_l56_https_arxiv_org_abs_2604_28130v1/figures/005_Table_2.jpg]]
*Table 2: V1 vs. Ours under different mesh configurations. “GT Mesh” = ground-truth mesh; “Pred Mesh” = predicted mesh; “Ours” removes mesh entirely. For fair comparison with V1 (which was trained on Zoo only), all models in this table are both trained and evaluated on Zoo only; the Ours numbers therefore differ slightly from those in Table 1, where the model is trained on Zoo+Obj. Best angle error per split in bold*

**Zoo-Seen（可见骨骼）**：在旋转精度上，V2 达到 **10.73°**，相比 VIBE 的 19.67° 降低了 8.94°；在位置精度上，V2 达到 **2.34 cm**，相比 GLoT 的 19.66 cm 降低了 17.32 cm。这一结果表明，端到端可学习管线在熟悉骨骼上已大幅超越传统因子化方法和通用人体姿态估计器。

**Zoo-Rare（稀有骨骼）**：V2 的旋转误差为 **14.38°**，相比 HRNet 的 24.72° 降低了 10.34°，证明方法对训练集中出现频率较低的骨骼拓扑同样具备良好的泛化能力。

**Zoo-Unseen（未见骨骼）**：这是最具挑战性的泛化场景。V2 的旋转误差仅为 **6.54°**，相比 ViTPose 的 24.46° 降低了 17.92°，降幅高达 73.3%。这一结果直接验证了参考条件化策略对跨骨骼泛化的核心价值——即使在训练中从未见过的骨骼拓扑上，参考姿态-旋转对提供的坐标轴锚定仍能有效消解 P→R 映射的病态性。

**Objaverse**：在来自 Objaverse 数据集的多样化资产上，V2 达到 **11.06°**，相比 VIBE 的 28.72° 降低了 17.66°，证明方法对合成资产同样具有强泛化能力。

### 消融实验：管线架构与训练策略

**Table 3** 系统消融了训练策略对性能的影响，揭示了三个关键发现：

**端到端联合训练的必要性**：将 V→P 与 P→R 模块的梯度截断（gradient-detached）后，Zoo-Unseen 旋转误差从 **6.54° 升至 7.82°**。这一 1.28° 的差距直接证明了梯度耦合带来的协同优化收益——当旋转损失可以回传至视觉编码器时，中间姿态表示会自动重塑为最有利于旋转恢复的表示形式，而非单纯追求位置精度。这是因子化管线（带有不可微 IK）无法实现的能力。

**混合姿态训练弥合分布差距**：纯真实姿态训练（GT-only）在 Zoo-Unseen 上失败，旋转误差高达 **13.28°**。原因是 P→R 模块在训练时仅见过完美的真实姿态，而推理时接收的是有噪声的预测姿态，导致严重的分布偏移。采用混合姿态策略（mixed-pose），以 $E_{w}=30$ 的预热调度逐步增加预测姿态的馈送比例，将误差降至 **6.54°**，弥合了训练-推理分布差距。

**Table 2** 进一步消融了网格中间表示的影响。去除网格中间表示后，V2 在 Zoo-Unseen 上的旋转误差为 **10.6°**，优于 V1 使用真实网格（GT Mesh）时的 18.9°，且推理速度提升约 **20 倍**（处理 120 帧序列从 20+ 分钟降至约 1 分钟）。这一结果说明，网格中间表示不仅引入额外计算开销，其预测误差还会累积并损害旋转恢复质量。

### 消融实验：参考条件化的核心作用

**Table 4** 是理解方法核心使能因素的关键消融。当完全去除参考姿态-旋转对（No Ref）时，Zoo-Unseen 旋转误差骤升至 **24.05°**，几乎回到不可学习 P→R 映射的水平。单独添加参考对（Ref only）将误差降至 **7.37°**，结合静止姿态（Ref+Rest）进一步降至 **6.54°**。

这一消融链条清晰揭示了因果机制：静止姿态仅提供坐标系原点（关节偏移），而参考姿态-旋转对提供了坐标轴方向。两者结合将多值 P→R 映射转化为良好约束的条件预测问题，使 P→R 模块变得可学习。24.05° → 7.37° 的跳跃是该方法最决定性的证据之一。

### 消融实验：中间表示与注意力机制

**Table 5** 验证了显式关节位置中间表示的结构必要性。直接 V→R 变体（跳过显式姿态瓶颈）在 Zoo-Unseen 上仅 **23.73°**，而显式姿态中间表示（Full）达到 **6.54°**。这一巨大差距说明，显式关节位置瓶颈为跨骨骼泛化提供了关键的几何归纳偏置——不同骨骼拓扑共享关节位置这一统一的中间语言，使旋转解码器可以在相对稳定的表示空间上工作。

**Table 6** 消融了 GL-GMHA（Global-Local Graph-guided Multi-Head Attention）的设计。纯局部注意力（All-local）在 Zoo-Rare 上退化至 **16.91°**（vs GL-GMHA 的 14.38°），说明仅沿运动链限制注意力会损害跨分支协调能力。GL-GMHA 的交替设计——局部层建模关节内依赖，全局层允许全连接协调——在保持拓扑泛化能力的同时实现了最佳性能。

### 模型深度与交叉注意力深度

**Table 7** 显示 8 层模型深度达到最优（Zoo-Unseen 6.54°），12 层反而导致性能退化，说明更深模型可能出现过拟合或优化困难。

**Table 8** 消融了旋转解码器中参考交叉注意力的深度 $L_{cross}$。$L_{cross}=6$ 达到最优（Zoo-Unseen 6.54°），而无交叉注意力（$L_{cross}=0$）直接失败（**23.49°**），再次验证参考条件化信息必须通过充分的注意力交互注入旋转预测过程。

### 失败模式与局限性

尽管整体性能优异，方法存在三类已知局限：

1. **分布外运动泛化不足**：P→R 解码器依赖从训练分布中学习的运动先验。当输入运动远离训练分布时（例如将四足骨骼强制置入双足“高举双臂”姿态），解码器可能产生不合理的旋转，即使上游姿态预测仍然合理。这本质上是数据覆盖问题而非框架瓶颈——扩展训练数据中（骨骼，运动）组合的多样性是最直接的改进方向。

2. **遮挡与相机运动**：框架假设单前景主体且相机运动最小，未显式处理严重遮挡情况。这些场景在训练数据中代表性不足，引入遮挡感知的数据增强或基于分割条件化的视觉骨干是值得探索的方向。

3. **稀有物种的旋转质量受限**：训练集中各物种覆盖不均匀（Truebones Zoo 包含约 1000 条序列但仅涵盖几十个物种），稀有物种的旋转质量受数据稀缺限制。

### 补充图表

![[assets/figures/papers/paper_list_l56_https_arxiv_org_abs_2604_28130v1/figures/006_Table_3.jpg]]
*Table 3: Ablation of training strategies on Zoo (Seen/Rare/Unseen) and Obj. Position in cm; rotation in degrees (↓). Best angle error per split in bold*

![[assets/figures/papers/paper_list_l56_https_arxiv_org_abs_2604_28130v1/figures/007_Table_4.jpg]]
*Table 4: Ablation of reference conditioning (Ref ) and rest pose (Rest). Position in cm; rotation in degrees (↓). Best angle error per split in bold*

![[assets/figures/papers/paper_list_l56_https_arxiv_org_abs_2604_28130v1/figures/008_Table_5.jpg]]
*Table 5: Ablation of the intermediate pose representation. Position in cm; rotation in degrees (↓). “Direct (V→R)” regresses rotations directly from video without a pose branch; joint positions for this variant are recovered by applying forward kinematics to the predicted rotations. “Latent +*

![[assets/figures/papers/paper_list_l56_https_arxiv_org_abs_2604_28130v1/figures/010_Table_7.jpg]]
*Table 7: Effect of model depth (Video-to-Pose and Pose-to-Rotation jointly scaled). Position in cm; rotation in degrees (↓). Best angle error per split in bold*

![[assets/figures/papers/paper_list_l56_https_arxiv_org_abs_2604_28130v1/figures/011_Table_8.jpg]]
*Table 8: Effect of reference cross-attention depth*



## 定位与知识库关联

### 1. 问题定位：从因子化管线到端到端可学习框架

MoCapAnything V2 试图解决的核心问题是**任意骨骼拓扑的动作捕捉**——给定一段单目视频，输出能够直接驱动任意目标骨骼（人体、动物、虚构角色）的关节旋转序列。该问题的根本困难在于从 3D 关节位置恢复关节旋转是一个**病态映射**：相同的关节位置，在不同骨骼的静止姿态和局部坐标轴约定下，可以对应完全不同的旋转值。这一病态性在跨骨骼泛化场景中被急剧放大——测试时遇到训练中未见过的骨骼拓扑时，传统方法几乎必然失败。

在 V2 之前，该领域的主流范式是**因子化管线**：将问题拆解为 Video-to-Pose（V→P）和 Pose-to-Rotation（P→R）两个阶段，其中 V→P 阶段可学习，而 P→R 阶段依赖不可微的解析逆向运动学（IK）求解器。这一设计存在两个结构性缺陷：

1. **P→R 的不可微性切断了梯度回传**，使 V→P 模块无法针对最终旋转目标进行优化，只能被迫优化中间位置精度——而位置精度与旋转精度并不完全对齐。
2. **解析 IK 无法解决骨骼轴向扭转等欠约束自由度**，导致关节抖动和肢体翻转等伪影（见 Fig. 4 的定性对比）。

MoCapAnything V2 的直接前任 **MoCapAnything V1**（Gong et al., arXiv 2025）正是这一范式的代表：它通过预测 4D 网格作为中间表示来提取姿态，再调用解析 IK 求解旋转。V2 的核心突破在于将 P→R 阶段也变为可学习模块，从而打通了 V→P→R 全链路的梯度流动，实现了端到端联合优化。

### 2. 核心技术贡献的知识库定位

#### 2.1 参考条件化：将病态映射转化为条件预测

V2 最关键的创新是在目标资产的**静止姿态（rest pose）之外，额外引入一个参考姿态-旋转对（reference pose–rotation pair）作为坐标轴锚点**。静止姿态仅提供关节坐标系的**原点**（骨骼偏移量），而参考对提供了**坐标轴方向**。两者结合，将原本多值的 P→R 映射 ${\bf R} = f({\bf P}, {\bf o})$ 转化为良好约束的条件预测问题。

这一设计的消融证据极为有力（Table 4）：当完全移除参考对时，Zoo-Unseen 上的旋转误差从 6.54° 骤升至 24.05°–24.26°；仅使用参考对（无静止姿态编码）为 7.37°；两者结合达到最优的 6.54°。这表明**坐标轴锚定是解决 P→R 病态性的使能因素**，而非锦上添花的辅助信号。

从知识库定位来看，这一设计将“参考条件化”从传统的视觉特征增强（如 DINOv2 特征条件化）提升到了**几何坐标系定义**的层面。它与 SMPL 等参数化人体模型中的 shape-dependent 坐标系定义有概念上的亲缘性，但 V2 将其推广到了任意骨骼拓扑的通用设定。

#### 2.2 端到端联合优化：梯度耦合的结构性收益

V2 的第二个核心贡献是证明了**V→P 与 P→R 协同优化的必要性**。Table 3 的关键消融显示：梯度截断变体（V→P 和 P→R 独立训练，无梯度回传）在 Zoo-Unseen 上角度误差为 7.82°，而端到端联合训练降至 6.54°。这 1.28° 的差距揭示了梯度耦合的结构性收益：当旋转损失可以回传至视觉编码器时，中间姿态表示不再单纯追求位置精度，而是**自动重塑为最有利于旋转恢复的表示形式**。

这一发现对因子化管线（带有不可微 IK）构成了根本性挑战——它表明即使 V→P 的位置精度再高，也无法弥补 P→R 阶段缺乏梯度引导的损失。Table 2 进一步佐证了这一点：V1 即使使用真实网格（GT Mesh）作为中间表示，平均角度误差仍高达 18.9°，而 V2 在完全去除网格中间表示的情况下仅 10.6°，且推理速度提升约 20 倍。

#### 2.3 显式姿态中间表示：跨骨骼泛化的结构瓶颈

Table 5 的消融提供了另一个关键洞察：直接 V→R 变体（跳过显式姿态中间表示）在 Zoo-Unseen 上角度误差高达 23.73°，而显式姿态中间表示（Full）仅 6.54°。这表明**显式的关节位置瓶颈对跨骨骼泛化至关重要**——它迫使模型学习一种骨骼无关的运动表示，而非将旋转预测与特定骨骼拓扑过拟合。

这一发现与计算机视觉中“显式中间表示促进泛化”的经典直觉一致（如关键点热力图之于姿态估计），但在任意骨骼动作捕捉的语境下得到了量化验证。

#### 2.4 GL-GMHA：拓扑感知的注意力机制

V2 引入的**全局-局部交替图引导多头注意力（GL-GMHA）**在 V→P 和 P→R 两个阶段共享，作为结构骨干。其核心设计是交替使用两种注意力模式：局部层沿运动链限制注意力范围（建模关节内依赖），全局层允许全连接（建模跨分支协调）。Table 6 显示，纯局部变体在 Zoo-Rare 上退化至 16.91°（vs GL-GMHA 的 14.38°），验证了全局协调对稀有骨骼的必要性。

这一设计与 **Graphormer**（Ying et al., NeurIPS 2021）等图 Transformer 工作有方法论上的亲缘性，但 V2 的贡献在于将其适配到**跨骨骼泛化**场景，并通过交替设计平衡了局部精度与全局协调。

### 3. 与基线方法的关系

#### 3.1 姿态估计基线

**HRNet**（Sun et al., CVPR 2019）和 **ViTPose**（Xu et al., NeurIPS 2022）代表了从高分辨率表示学习和视觉 Transformer 两个方向解决姿态估计的经典工作。在 Table 1 中，HRNet 在 Zoo-Rare 上角度误差为 24.72°，ViTPose 在 Zoo-Unseen 上为 24.46°，而 V2 分别降至 14.38° 和 6.54°。这些基线在跨骨骼泛化上的失败印证了仅优化位置精度不足以解决旋转恢复问题。

#### 3.2 视频人体运动捕捉基线

**VIBE**（Kocabas et al., CVPR 2020）和 **GLoT**（Shen et al., CVPR 2023）代表了视频人体运动捕捉的主流方法。VIBE 在 Zoo-Seen 上角度误差为 19.67°，在 Obj 上为 28.72°；GLoT 在 Zoo-Seen 上 MPJPE 为 19.66 cm。V2 分别降至 10.73°（-8.94°）和 2.34 cm（-17.32 cm）。这些差距主要源于两个因素：(1) VIBE/GLoT 依赖 SMPL 参数化人体模型，无法泛化至任意骨骼；(2) 它们的旋转恢复策略未针对跨骨骼场景设计。

值得注意的是，Table 1 中所有基线方法均采用统一的可学习旋转模块进行端到端联合训练，确保对比公平——只有 V1 因因子化设计的固有约束而使用传统解析 IK。这意味着 V2 的领先并非来自更强大的旋转模块，而是来自**端到端可学习管线本身的架构优势**。

#### 3.3 与 V1 的详细对比

Table 2 提供了 V1 与 V2 在公平训练配置下的直接对比（仅在 Zoo 数据集上训练和评估，匹配 V1 原始配置）。关键发现：
- V1 + GT Mesh（真实网格）：角度误差 18.9°，位置误差 3.41 cm
- V1 + Pred Mesh（预测网格）：角度误差 23.8°，位置误差 5.26 cm
- V2（无网格）：角度误差 10.6°，位置误差 4.17 cm

V2 在位置精度上略逊于 V1 + GT Mesh（4.17 vs 3.41 cm），但在旋转精度上大幅领先（10.6° vs 18.9°），且推理速度提升约 20 倍。位置精度的微小差距可能源于网格中间表示提供的额外几何约束，但 V2 的旋转优势表明**端到端优化对最终动画质量的收益远超位置精度的微小损失**。

### 4. 适用边界与局限

#### 4.1 训练分布依赖

P→R 解码器依赖从训练分布中学习的运动先验。当测试运动远离训练分布时——例如将四足骨骼强制置入双足“高举双臂”姿态——解码器可能产生不合理的旋转，即使上游姿态预测仍然合理。这一局限的根源在于训练数据中（骨骼, 运动）组合的覆盖度不足，而非建模框架本身的瓶颈。

#### 4.2 遮挡与相机运动

框架假设单前景主体且相机运动最小，未显式处理严重遮挡情况。这些场景在训练数据中代表性不足，导致模型在此类条件下的鲁棒性缺乏保证。引入遮挡感知的数据增强或基于分割条件化的视觉骨干是值得探索的方向。

#### 4.3 物种覆盖不均

Truebones Zoo 数据集包含约 1000 条序列但仅涵盖几十个物种，稀有物种的旋转质量受数据稀缺限制。Table 1 中 Zoo-Rare 的角度误差（14.38°）显著高于 Zoo-Unseen（6.54°），这一反直觉现象可能反映了稀有物种的运动模式与常见物种差异较大，而非骨骼拓扑的未见性本身。

#### 4.4 模型深度的边际收益递减

Table 7 显示 8 层模型深度达到最优（Zoo-Unseen 6.54°），12 层反而导致性能退化。这表明当前数据规模下，更深模型可能过拟合训练分布中的骨骼-运动组合，损害跨骨骼泛化能力。

### 5. 开放问题

1. **位置-旋转精度权衡**：能否通过更强的视觉编码器或辅助几何监督，在不牺牲推理速度的前提下缩小与 V1 + GT Mesh 的位置精度差距（Table 2 中约 0.76 cm）？

2. **分布外运动泛化**：如何系统性地扩展训练数据的（骨骼, 运动）组合多样性，使 P→R 解码器能够覆盖任意运动？合成数据生成（如物理仿真）是否可行？

3. **遮挡鲁棒性**：如何以最小架构改动引入遮挡感知机制？基于分割掩码的条件化或遮挡模拟数据增强的效果如何？

4. **物种覆盖度扩展**：Truebones Zoo 的物种覆盖有限，如何高效采集或生成更多物种的运动数据以提升稀有骨骼的旋转质量？

5. **参考对选择策略**：当前参考姿态-旋转对从同一资产中采样，其对模型性能的敏感性尚未系统研究。参考对的选择策略（如运动范围最大化）是否影响旋转恢复质量？



## 原文 PDF

![[paperPDFs/arxiv_2026/MoCapAnything_V2_End_to_End_Motion_Capture_for_Arbitrary_Skeletons.pdf]]
