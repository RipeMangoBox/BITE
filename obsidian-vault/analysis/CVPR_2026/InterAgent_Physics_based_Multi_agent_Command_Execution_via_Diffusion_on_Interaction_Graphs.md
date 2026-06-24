---
title: "InterAgent: Physics-based Multi-agent Command Execution via Diffusion on Interaction Graphs"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/InterAgent_Physics_based_Multi_agent_Command_Execution_via_Diffusion_on_Interaction_Graphs.pdf
project_link: "https://binlee26.github.io/InterAgent-Page"
code_link: null
aliases:
- InterAgent
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入交互图外部感知表示、多流DiT解耦异质模态、边缘稀疏注意力选择关键空间依赖，形成端到端的自回归扩散框架。
primary_logic: 将本体感知、外部感知和动作分解为独立流并在交互图上施加稀疏注意力，使扩散Transformer能够高效捕捉多智能体间关键空间关系，生成物理合理且语义一致的交互行为。
claims:
- InterAgent 是首个端到端的文本驱动物理多智能体控制框架，在InterHuman测试集上达到SOTA性能。
- 交互图外部感知与稀疏边缘注意力显著提升交互建模鲁棒性。
- 在InterHuman数据集上，InterAgent 的 R-precision Top-3 (0.615) 和 FID (0.582) 皆大幅优于最强基线InterGen++ (0.542, 0.943)。
- InterHuman 测试集 上 R-precision Top-1 ↑ = 0.375±0.006
---

# InterAgent: Physics-based Multi-agent Command Execution via Diffusion on Interaction Graphs

> [!tip] 核心洞察
> 将本体感知、外部感知和动作分解为独立流并在交互图上施加稀疏注意力，使扩散Transformer能够高效捕捉多智能体间关键空间关系，生成物理合理且语义一致的交互行为。

| 字段 | 内容 |
|------|------|
| 中文题名 | InterAgent：基于交互图扩散的物理多智能体命令执行 |
| 英文题名 | InterAgent: Physics-based Multi-agent Command Execution via Diffusion on Interaction Graphs |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.07410) · [Project](https://binlee26.github.io/InterAgent-Page) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | InterAgent |
| Dataset | InterHuman 测试集 |

> [!tip] 效果简介
> - InterHuman 测试集 上，R-precision Top-1 ↑ 0.375±0.006 vs 0.287±0.007 (InterGen++) (+0.088)；R-precision Top-3 ↑ 0.615±0.007 vs 0.542±0.006 (InterGen++) (+0.073)；FID ↓ 0.582±0.018 vs 0.943±0.012 (InterGen++) (-0.361)。

## 概述

现有物理驱动的人形控制方法局限于单智能体，难以建模多智能体交互所需的精细关节间依赖与异质模态（本体感知、外部感知、动作）的协同，导致生成行为物理不一致或交互细节缺失。针对这一瓶颈，InterAgent 提出首个端到端的文本驱动物理多智能体控制框架，其核心思路是将本体感知、外部感知和动作分解为独立流，并在交互图上施加稀疏注意力，使扩散 Transformer 能够高效捕捉多智能体间关键空间关系，生成物理合理且语义一致的交互行为。

在方法定位上，InterAgent 引入交互图外部感知表示、多流 DiT 解耦异质模态、以及基于 Gumbel-Softmax 的边缘稀疏注意力机制，形成端到端的自回归扩散框架。与物理化文本到交互基线（如 InterGen++、InterMask++）和端到端物理控制基线（如 PDP、CLoSD）相比，InterAgent 在 InterHuman 测试集上取得 SOTA 性能：R-precision Top-3 达到 0.615，FID 降至 0.582，显著优于最强基线 InterGen++（0.542 和 0.943）。消融实验进一步验证了交互图外部感知、三流解耦架构和边缘稀疏注意力各自对交互建模鲁棒性的关键贡献。

## 背景与动机

### 问题背景：从单智能体控制到多智能体交互

物理仿真中的人形角色控制（physics-based humanoid control）近年来取得了显著进展，使得虚拟角色能够在物理约束下生成逼真的运动。然而，现有工作几乎全部聚焦于**单智能体**场景：给定文本指令或高层目标，控制单个人形角色在物理仿真器中执行相应的动作。当场景扩展到**多智能体交互**时——例如两人握手、击掌、推搡或协作搬运——问题难度呈指数级增长。

多智能体交互的核心挑战在于，每个智能体的行为不仅取决于自身的本体感知（proprioception）和文本指令，还高度依赖于对其他智能体的**外部感知**（exteroception）。两个智能体之间的空间关系、时序协调和物理接触需要被精确建模，否则生成的交互行为会出现穿透、滑步、语义错位等物理不一致现象。

### 现有方法的缺口

当前处理多智能体交互的方法可大致分为两类，各有明显局限：

**1. 运动学生成 + 跟踪策略的级联方案**

以 **InterGen++** 和 **InterMask++** 为代表的方法采用两阶段流程：首先使用运动学扩散模型生成多智能体的运动序列，再通过训练好的跟踪策略（tracking policy）将其“物理化”——即驱动物理仿真器中的人形角色去跟踪生成的运动。这种级联方案存在两个根本性问题：

- **误差累积**：运动学模型生成的参考运动未必物理可行，跟踪策略在跟踪时会产生额外偏差，两级误差叠加导致最终行为偏离预期。
- **模态割裂**：运动学生成阶段缺乏对物理约束的感知，无法保证生成的交互（如接触力、动量交换）在物理仿真中可复现。

**2. 端到端物理控制基线**

**PDP**（Physics-based Diffusion Policy）和 **CLoSD**（Closing the Loop between Simulation and Diffusion）等方法实现了端到端的物理控制，直接从状态观测预测动作，避免了级联误差。但它们的架构设计针对单智能体，在扩展到多智能体时面临关键瓶颈：

- **外部感知表示粗糙**：通常使用简单的相对状态向量（如两智能体根节点的相对位置和朝向），无法捕捉**关节级别**的细粒度空间交互。当交互涉及特定身体部位（如手部接触、脚部绊摔）时，粗粒度的外部感知会导致交互细节丢失或物理穿透。
- **模态混合建模**：采用单流扩散Transformer（single-stream DiT）将本体感知、外部感知和动作序列合并为单一输入流。这种混合处理方式使模型难以解耦不同模态的特征，导致训练效率低下，生成行为在物理合理性与语义一致性之间难以平衡。

### 核心瓶颈

综上，现有物理驱动的人形控制方法存在一个核心瓶颈：

> **难以建模多智能体交互所需的精细关节间依赖与异质模态（本体感知、外部感知、动作）的协同，导致生成行为物理不一致或交互细节缺失。**

具体而言，瓶颈体现在三个层面：
- **表示层面**：缺乏能够显式编码智能体间所有关节对空间关系的结构化外部感知表示。
- **架构层面**：单流模型无法解耦异质模态，阻碍了各模态的专门化处理和跨模态协调。
- **注意力层面**：密集注意力在交互图上产生大量冗余连接，淹没了真正关键的关节间依赖信号。

### 本文动机

针对上述瓶颈，本文提出 **InterAgent**——首个端到端的文本驱动物理多智能体控制框架。核心动机是通过三个协同创新来系统性解决多智能体交互建模的挑战：

1. **交互图外部感知**：将智能体间所有关节对的有向空间关系显式编码为交互图（Interaction Graph），提供结构化、关节级别的外部感知表示。
2. **多流扩散Transformer**：将本体感知、外部感知和动作分解为独立流，通过流间融合注意力和上下文感知条件注意力实现解耦但协调的建模。
3. **边缘稀疏注意力**：在交互图上施加基于Gumbel-Softmax的稀疏注意力，动态抑制冗余连接，聚焦对交互动力学贡献最大的关键关节对。

通过这些设计，InterAgent 旨在实现一个端到端框架，能够从纯文本指令生成物理合理、语义一致的多智能体交互行为，并在公开基准上达到最优性能。

## 核心创新

InterAgent 的核心创新在于首次将**端到端的物理仿真多智能体控制**与**文本条件生成**统一在一个框架下，其关键突破并非单一技术点，而是通过三个紧密耦合的“changed slot”系统性地解决了现有多智能体交互建模中的瓶颈。

### 瓶颈与因果路径

现有物理驱动的人形控制方法（如 PDP、CLoSD）局限于单智能体场景，而将文本到动作的生成方法（如 InterGen++、InterMask++）物理化时，面临一个根本性瓶颈：**缺乏对多智能体间精细关节级空间依赖的显式建模，且将本体感知、外部感知和动作等异质模态粗暴合并处理**，导致生成的交互行为物理不一致或交互细节缺失。InterAgent 的因果路径是：将外部感知重构为结构化的交互图 → 以多流架构解耦异质模态 → 在交互图上施加稀疏注意力聚焦关键依赖，从而在物理仿真循环中自回归地生成物理合理且语义一致的交互行为。

### Changed Slot 1：从相对状态到交互图外部感知

基线方法通常使用简单的相对状态（Relative State, RS）来表示智能体间的空间关系，或根本未显式建模外部感知。InterAgent 提出了**交互图（Interaction Graph, IG）**作为外部感知表示。在全连接交互图（FIG）中，两个智能体的所有关节对之间建立有向边，每条边编码两关节间的相对位置向量：

$$\pmb{x}_e = (\pmb{e}_{1,1}, \pmb{e}_{1,2}, ..., \pmb{e}_{J,J}) \in \mathbb{R}^{(J \times J) \times 3}$$

这一表示将“一个智能体对另一个智能体的感知”从粗粒度的根节点相对关系提升到**关节级的全对全空间交互编码**，为后续的稀疏注意力提供了结构化基础。消融实验（Table 2）表明，即使使用相同的三流 DiT 架构，FIG 在 R-precision Top-3（0.612）和 FID（0.634）上已显著优于 RS（0.588, 0.676），验证了结构化外部感知表示本身的关键作用。

### Changed Slot 2：从单流 DiT 到三流解耦架构

基线方法（如 PDP）使用单流 DiT 将状态与动作合并处理，忽视了本体感知（自身关节状态）、外部感知（交互图边向量）和动作（PD 目标）之间的模态异质性。InterAgent 设计了**多流 DiT 块（Multi-stream DiT block）**，将三种模态分别送入独立的 Transformer 流处理，并通过两个关键注意力机制实现解耦但协调的建模：

- **流间融合注意力（Inter-stream fusion attention）**：在三个独立流之间交换信息，使各模态能够感知其他模态的上下文。
- **上下文感知条件注意力（Context-aware conditioning attention）**：整合时序历史缓存和文本 CLIP 嵌入，为每个流提供全局条件信号。

这一设计的因果逻辑是：**解耦让各模态专注于自身表征学习，而融合注意力确保跨模态协同不丢失**。消融实验（Table 2）提供了强有力的因果证据：在 FIG 外部感知下，单流 DiT 的 R-precision Top-3 仅 0.523，FID 高达 0.828；双流降至 0.608 和 0.662；三流进一步优化至 0.612 和 0.634。模态解耦程度与性能呈单调正相关，明确验证了解耦建模的必要性。

### Changed Slot 3：从密集注意力到边缘稀疏注意力

全连接交互图虽然结构完备，但包含大量冗余连接（如远距离无关关节对），密集注意力会引入噪声并浪费计算。InterAgent 在交互图外部感知流中引入了**基于 Gumbel-Softmax 的边缘稀疏注意力机制**：

$$\pmb{A} = \mathrm{Gumbel-Softmax}\left(\frac{\pmb{Q}\pmb{K}^T}{\sqrt{d_f}}\right)$$

$$M_{ij} = \begin{cases} 1, & j \in \arg\mathrm{TopK}_k(A_i) \\ 0, & \mathrm{otherwise} \end{cases}$$

$$\pmb{f}' = (M \circ A)V$$

通过 Top-K 掩码仅保留每行注意力得分最高的 k 条边，强制模型聚焦于真正关键的关节间空间依赖。消融实验（Table 3）显示，边缘级稀疏配合 1/2 稀疏比取得最佳性能（R-precision Top-3: 0.615, FID: 0.582），优于非稀疏注意力（0.612, 0.634）和关节级稀疏。这表明**在正确的结构化表示（交互图）上施加正确的稀疏粒度（边缘级）**，是性能从“好”到“最优”的关键跃迁。

### 架构层面的系统性创新

除上述三个核心 changed slot 外，InterAgent 的框架设计本身构成了一项架构创新：**两个合作、权值共享的 Inter-DiT 网络**在自回归扩散范式下运行，以分类器自由引导（引导尺度 3.5，10% 丢弃率）提升文本一致性。这种对称权值共享设计天然保证了交互双方的行为协调性，避免了非对称架构可能引入的偏差。

### 创新边界与局限

需要指出，InterAgent 的创新聚焦于**固定双智能体**场景下的物理交互生成。其对高度动态行为（如跳跃）表现不佳（Figure 9），因为自回归扩散模型倾向平滑过渡，难以处理爆发性瞬间动力学。此外，交互图的边数量随智能体数量呈二次增长，当前框架无法直接扩展至可变数量智能体——这属于**未解决的扩展性问题**，而非方法内部的缺陷。

## 整体框架

InterAgent 的端到端物理多智能体控制框架围绕一个核心设计展开：**将文本条件直接映射为物理仿真器中两个合作人形角色的交互行为**，无需中间运动生成与跟踪策略的分阶段衔接。框架由三个紧密耦合的模块构成闭环（Figure 2）。

![[assets/figures/papers/paper_list_l2522_https_arxiv_org_abs_2512_07410/figures/002_Figure_2.jpg]]
*Figure 2: InterAgent overview. A physics-based framework for text-driven multi-agent interactive behavior generation, built upon Inter-DiT — two cooperative, weight-sharing networks under an autoregressive diffusion paradigm*

### 输入流与状态表示

系统接收两类输入：(1) 自然语言文本命令，经由 CLIP 编码为条件向量 $\mathbf{c}$；(2) 两个智能体的历史行为状态 $\pmb{S}$，作为自回归上下文。每个智能体的本体感知状态定义为：

$$\pmb{x}_s = (R_h, p, r, \pmb{v}, \pmb{w})$$

其中 $R_h$ 为根关节高度，$p$ 和 $r$（6D 连续表示）分别为所有关节的位置与旋转，$\pmb{v}$ 和 $\pmb{w}$ 为线速度与角速度（Eq. 1）。外部感知则通过**交互图**（Interaction Graph, IG）显式建模：对两个智能体的 $J$ 个关节，构造所有关节对之间的有向边向量 $\pmb{e}_{i,j} \in \mathbb{R}^3$，编码相对空间关系：

$$\pmb{x}_e = (\pmb{e}_{1,1}, \pmb{e}_{1,2}, ..., \pmb{e}_{J,J}) \in \mathbb{R}^{(J \times J) \times 3}$$

这一表示将隐式的多智能体空间依赖转化为结构化的图信号，为后续稀疏注意力提供了可操作的几何先验（Eq. 2）。

### 核心生成器：Inter-DiT

框架的生成核心是 **Interaction Diffusion Transformer（Inter-DiT）**——两个权值共享的合作网络，在自回归扩散范式下工作。给定历史状态 $\pmb{S}$（缓存长度 $h=364$ 帧）和文本条件 $\mathbf{c}$，Inter-DiT 从噪声序列出发，预测未来 $m=4$ 帧的行为 $\hat{\mathbf{X}}^{(0)}$，经训练损失优化：

$$\mathcal{L} = \mathbb{E}_{t, \mathbf{X}} \left[ || \mathbf{X} - \Phi(\mathbf{X}^{(t)}, t, \mathbf{c}, \pmb{S}) || \right]$$

其中 $\Phi$ 为去噪网络，$\mathbf{X}^{(t)}$ 为扩散时间步 $t$ 的噪声版本（Eq. 3）。推理时，模型以自回归方式滚动预测，每次将新生成的帧附加到历史缓存，实现持续交互生成。分类器自由引导（10% 丢弃率，引导尺度 3.5）进一步增强文本一致性。

Inter-DiT 的关键创新在于其**多流 DiT 块**设计（Figure 3）：将本体感知、外部感知（交互图）和动作三种异质模态分配到三个独立流中处理，每个流保持各自的特征空间。流间通过两类注意力实现解耦但协调的建模——**流间融合注意力**（inter-stream fusion attention）在模态间交换信息，**上下文感知条件注意力**（context-aware conditioning attention）整合时序历史与跨智能体上下文。这种设计避免了单流架构中模态混杂导致的物理不一致问题。

### 稀疏交互图与边缘注意力

全连接交互图（FIG）包含 $J \times J$ 条边，存在大量冗余连接。InterAgent 引入**基于 Gumbel-Softmax 的边缘稀疏注意力**以聚焦关键空间依赖：

$$\pmb{A} = \mathrm{Gumbel\text{-}Softmax}\left( \frac{\pmb{Q}\pmb{K}^T}{\sqrt{d_f}} \right)$$

$$M_{ij} = \begin{cases} 1, & j \in \arg\mathrm{TopK}_k(A_i) \\ 0, & \mathrm{otherwise} \end{cases}$$

$$\pmb{f}' = (M \circ A) V$$

查询 $\pmb{Q}$ 与交互图边特征的键 $\pmb{K}$ 计算注意力得分矩阵 $\pmb{A}$，Top-K 掩码 $M$ 仅保留每行得分最高的 $k$ 条边，最终通过哈达玛积得到稀疏注意力输出 $\pmb{f}'$（Eq. 4-6）。消融实验证实，边缘级稀疏配合 1/2 稀疏比取得最佳性能（R-precision Top-3: 0.615, FID: 0.582），优于关节级稀疏和非稀疏变体（Table 3）。

### 物理执行与闭环

Inter-DiT 预测的未来状态-动作序列通过物理仿真器执行：预测的下一帧参考状态 $\mathbf{s}_{t+1}^{ref}$ 输入跟踪策略 $\pmb{\pi}(\pmb{s}_t, \pmb{s}_{t+1}^{ref})$，输出关节力矩驱动仿真，产生实际状态 $\mathbf{s}_{t+1}$。这一闭环确保生成行为遵守物理定律，物理正确性指标（Floating, Skating, Jerk）接近真值水平（Table 4）。

### 反应式控制能力

框架进一步支持反应式控制：推理时通过修复机制（inpainting）固定一个智能体的运动轨迹，让另一个智能体生成文本条件的反应行为，无需额外训练（Figure 7）。这展示了 InterAgent 对交互上下文的灵活适应能力。

## 核心模块与公式推导

InterAgent 的核心架构围绕三个关键设计展开：**三流解耦的扩散Transformer (Inter-DiT)**、**交互图外部感知表示**以及**稀疏边缘注意力机制**。以下逐一剖析各模块的结构与作用。

### 1. 状态表示与交互图外部感知

框架首先将每个人形智能体的状态定义为一个高维向量：

$$
\pmb{x}_s = (R_h, p, r, \pmb{v}, \pmb{w})
$$

其中 $R_h$ 为根关节高度，$p$ 和 $r$ 分别为关节位置与6D旋转表示，$\pmb{v}$ 和 $\pmb{w}$ 为线速度与角速度。这一表示涵盖了本体感知所需的全部运动学信息。

为显式建模多智能体间的空间依赖，InterAgent 提出**交互图 (Interaction Graph, IG)** 作为外部感知表示。对于两个各含 $J$ 个关节的人形体，全连接交互图 (Fully-connected IG, FIG) 定义为所有关节对之间的有向边向量集合：

$$
\pmb{x}_e = (\pmb{e}_{1,1}, \pmb{e}_{1,2}, ..., \pmb{e}_{J,J}) \in \mathbb{R}^{(J \times J) \times 3}
$$

每条边 $\pmb{e}_{i,j}$ 编码了智能体A的第 $i$ 个关节到智能体B的第 $j$ 个关节的相对位置向量，从而将交互建模为一张结构化的有向图。相比传统方法中仅使用相对状态 (Relative State, RS) 的隐式建模，IG 提供了更显式、更细粒度的空间交互表征。

### 2. 三流解耦的扩散Transformer (Inter-DiT)

Inter-DiT 由两个**权值共享**的协作网络组成，在自回归扩散范式下运行。其核心创新在于**多流 DiT 块 (Multi-stream DiT Block)** 的设计——将本体感知 (proprioception)、外部感知 (exteroception) 和动作 (action) 作为三个独立流处理，每个模态在各自的流中经过线性投影与注意力计算，再通过两种关键注意力机制实现解耦但协调的建模：

- **流间融合注意力 (Inter-stream Fusion Attention)**：在三个流之间交换信息，使本体感知、外部感知和动作能够协调一致；
- **上下文感知条件注意力 (Context-aware Conditioning Attention)**：整合时序历史与跨智能体上下文，将文本条件 $\pmb{c}$ 和历史状态 $\pmb{S}$ 注入各流。

训练目标为标准扩散损失，模型 $\Phi$ 从噪声序列 $\mathbf{X}^{(t)}$ 中预测干净的行为序列 $\mathbf{X}$：

$$
\mathcal{L} = \mathbb{E}_{t, \mathbf{X}} \left[ || \mathbf{X} - \Phi(\mathbf{X}^{(t)}, t, \mathbf{c}, \pmb{S}) || \right]
$$

推理时采用分类器自由引导 (classifier-free guidance)，以10%的CLIP嵌入丢弃率和3.5的引导尺度增强文本一致性。

### 3. 稀疏边缘注意力机制

全连接交互图虽然完备，但包含大量冗余连接，增加了计算负担并可能引入噪声。InterAgent 引入基于 **Gumbel-Softmax** 的稀疏边缘注意力来动态筛选关键交互依赖。

首先，对交互图的边特征计算注意力得分矩阵：

$$
\pmb{A} = \mathrm{Gumbel-Softmax}\left( \frac{\pmb{Q}\pmb{K}^T}{\sqrt{d_f}} \right)
$$

其中 $\pmb{Q}$ 为查询，$\pmb{K}$ 为交互图边的键，$d_f$ 为特征维度。Gumbel-Softmax 在保持可微性的同时使注意力分布趋于离散，便于后续稀疏化。

随后，通过 Top-K 掩码仅保留每行注意力得分最高的 $k$ 条边：

$$
M_{ij} = \begin{cases}
1, & j \in \arg\mathrm{TopK}_k(A_i) \\
0, & \mathrm{otherwise}
\end{cases}
$$

最终的稀疏注意力输出为掩码与注意力权重的哈达玛积对值 $\pmb{V}$ 的加权求和：

$$
\pmb{f}' = (M \circ A) V
$$

这一机制使得模型能够**在边缘级别**（而非粗糙的关节级别）自适应地聚焦于对交互动力学贡献最大的空间关系，从而在保持建模能力的同时显著提升效率。消融实验表明，边缘级稀疏配合1/2稀疏比取得了最优的 R-precision Top-3 (0.615) 和 FID (0.582)，优于非稀疏与关节级稀疏方案（Table 3）。

### 4. 自回归推理与物理仿真闭环

推理时，Inter-DiT 以历史缓存（$h=364$ 帧）作为上下文，从噪声序列出发预测未来 $m=4$ 帧的行为状态，随后通过一个预训练的跟踪策略将预测状态转化为关节力矩驱动物理仿真器。这一过程自回归地重复，形成端到端的文本到物理交互生成闭环。

---

**关键公式速查**：
| 公式 | 含义 | 编号 |
|------|------|------|
| $\pmb{x}_s = (R_h, p, r, \pmb{v}, \pmb{w})$ | 人形体状态表示 | Eq. (1) |
| $\pmb{x}_e \in \mathbb{R}^{(J \times J) \times 3}$ | 全连接交互图外部感知 | Eq. (2) |
| $\mathcal{L} = \mathbb{E}[||\mathbf{X} - \Phi(\mathbf{X}^{(t)}, t, \mathbf{c}, \pmb{S})||]$ | 扩散训练损失 | Eq. (3) |
| $\pmb{A} = \mathrm{Gumbel-Softmax}(\pmb{Q}\pmb{K}^T / \sqrt{d_f})$ | 稀疏注意力得分矩阵 | Eq. (4) |
| $M_{ij} = 1$ if $j \in \arg\mathrm{TopK}_k(A_i)$ else $0$ | Top-K 稀疏掩码 | Eq. (5) |
| $\pmb{f}' = (M \circ A)V$ | 稀疏注意力输出 | Eq. (6) |

### 补充图表

![[assets/figures/papers/paper_list_l2522_https_arxiv_org_abs_2512_07410/figures/003_Figure_3.jpg]]
*Figure 3: Multi-stream DiT block design. Each modality—proprioception, exteroception, and action—is processed in an independent stream. Inter-stream fusion attention exchanges information across modalities, while context-aware conditioning attention integrates temporal and inter-agent context, enabling decoupled yet coordinated modeling*

![[assets/figures/papers/paper_list_l2522_https_arxiv_org_abs_2512_07410/figures/004_Figure_4.jpg]]
*Figure 4: Sparse Interaction Graph. Each joint of one character connects to all joints of the other via directed edges (dark green), where each edge vector encodes the spatial interaction between the corresponding joints. The thickness of each edge encodes the magnitude of its contribution to the interactive dynamics. Light purple arrows on the ground indicate temporal progression*

## 实验与分析

### 主要结果：文本驱动的物理多智能体控制

InterAgent 在 InterHuman 测试集上对所有基线方法实现了全面超越，验证了端到端物理多智能体框架的有效性。表 1 汇总了核心指标的定量对比。

在文本-行为对齐的核心指标上，InterAgent 的 **R-precision Top-3 达到 0.615**，较最强的物理化基线 InterGen++（0.542）提升 **+0.073**；Top-1 同样从 0.287 提升至 0.375（+0.088）。这表明模型生成的交互行为与文本描述的语义一致性显著增强。

在生成质量方面，InterAgent 的 **FID 降至 0.582**，远优于 InterGen++ 的 0.943（降幅 0.361），MMDist 也从 3.751 降至 3.585。这一差距反映了交互图外部感知与多流解耦建模在捕捉多智能体交互细节上的关键作用——基线方法（如 InterGen++ 和 InterMask++）依赖“先运动生成、后物理跟踪”的两阶段管线，物理化过程中的误差累积导致行为失真，而 InterAgent 的端到端自回归扩散范式直接避免了这一瓶颈。

值得注意的是，在 **Diversity 和 MModality** 指标上，InterAgent（2.018, 1.903）略低于 InterGen++（2.044, 2.482），但仍优于其他基线。这一现象可归因于物理仿真器对生成行为的隐式正则化——物理约束天然限制了运动多样性，但换来了更真实的交互动力学。

物理正确性评估（表 4）进一步证实，InterAgent 在 Floating、Skating 和 Jerk 指标上均接近真值（Ground Truth），未因追求语义对齐而牺牲物理合理性。这得益于自回归扩散策略直接输出可执行的动作序列，而非中间运动表示。

### 消融实验：解耦建模与交互图外部感知

消融实验围绕两个核心设计展开：多流架构的流数选择与外部感知表示的形式。

**三流解耦的必要性。** 表 2 显示，在统一使用全连接交互图（FIG）的条件下，三流架构（Top-3: 0.612, FID: 0.634）显著优于单流（0.523, 0.828）和双流（0.608, 0.662）。单流架构将本体感知、外部感知和动作合并处理，导致异质模态间的信息混杂，难以捕捉精细的交互依赖；双流虽有所改善，但仍无法充分解耦动作与感知信号。三流设计通过 inter-stream fusion attention 实现模态间协调，同时保持各自独立的特征空间，是性能提升的结构性原因。

**交互图外部感知的优势。** 在最优三流配置下，稀疏交互图（SIG）取得了最佳性能（Top-3: 0.615, FID: 0.582），优于全连接交互图 FIG（0.612, 0.634）和传统相对状态表示 RS（0.588, 0.676）。RS 仅编码智能体间的整体相对位置，丢失了关节级的细粒度空间关系；FIG 虽捕获了所有关节对交互，但引入了大量冗余连接。SIG 通过 Gumbel-Softmax 驱动的边缘稀疏注意力，在保留关键空间依赖的同时抑制噪声，使模型聚焦于真正影响交互动态的关节对（如手-手、手-躯干），从而提升生成质量。

**稀疏机制与稀疏比。** 表 3 进一步分析了注意力类型与稀疏比的影响。边缘级稀疏注意力（edge-based）在 1/2 稀疏比下达到最优（Top-3: 0.615, FID: 0.582），优于关节级稀疏（joint-based）和非稀疏注意力。关节级稀疏以整条肢体为单位进行稀疏化，粒度粗糙，可能丢失跨关节的微妙交互；边缘级稀疏则直接在关节对层面筛选，更精准地建模空间依赖。稀疏比过高（如 1/4）会导致信息丢失，过低则退化为近似密集注意力，1/2 在两者间取得平衡。

定性消融（图 6）佐证了上述结论：单流架构生成的交互行为僵硬、缺乏协调性；RS 表示下智能体间空间关系模糊；而 SIG 配合三流架构产生的交互自然连贯，与文本描述高度一致。

### 失败模式与局限性

尽管 InterAgent 在整体性能上表现优异，但存在明确的失败边界。**高度动态行为（如跳跃）是主要失败场景**（图 9）。模型的自回归扩散范式倾向于生成平滑的运动轨迹，难以处理需要爆发性加速度的瞬间动力学——跳跃动作涉及短时间内的大幅关节力矩变化，与模型学到的时序平滑先验冲突。这一局限指向未来工作的方向：引入动态物理约束模块或混合运动基元，以增强对瞬态行为的建模能力。

此外，当前框架固定处理两个智能体，扩展至更多智能体时，交互图的全连接边数呈平方增长，计算开销显著上升。这限制了框架在群体交互场景中的直接应用。

### 反应式控制：推理时的泛化能力

InterAgent 展示了无需重新训练的反应式控制能力（图 7）。通过在推理时引入 inpainting 机制，固定一个智能体的运动轨迹，模型可自回归生成另一智能体的文本条件反应行为。这一能力源于多流架构中外部感知流的独立建模——模型在训练时已学会根据交互图推断空间关系，因此推理时仅需替换部分状态序列即可泛化至新的交互模式，体现了框架的灵活性。

### 补充图表

![[assets/figures/papers/paper_list_l2522_https_arxiv_org_abs_2512_07410/figures/005_Table_1.jpg]]
*Table 1: Comparison of text-driven physics-based multi-agent control on the InterHuman [32] test set, where ± indicates 95% confidence interval and →*

![[assets/figures/papers/paper_list_l2522_https_arxiv_org_abs_2512_07410/figures/006_Table_2.jpg]]
*Table 2: Quantitative evaluation of the stream number of multistream blocks and different exteroception representations*

![[assets/figures/papers/paper_list_l2522_https_arxiv_org_abs_2512_07410/figures/009_Figure_6.jpg]]
*Figure 6: Ablation study. We qualitatively evaluate how varying the number of streams in the multi-stream blocks and using different exteroception representations affect the quality and coherence of the generated multi-agent interactions*

![[assets/figures/papers/paper_list_l2522_https_arxiv_org_abs_2512_07410/figures/010_Table_3.jpg]]
*Table 3: Quantitative analysis of the IG attention and the effect of different sparsity ratios*

![[assets/figures/papers/paper_list_l2522_https_arxiv_org_abs_2512_07410/figures/011_Table_4.jpg]]
*Table 4: Quantitative evaluation of physical correctness. Bold and underline indicate the best and the second best result*

![[assets/figures/papers/paper_list_l2522_https_arxiv_org_abs_2512_07410/figures/001_Figure_1.jpg]]
*Figure 1: InterAgent produces physically plausible multi-agent interactions across diverse scenarios from only text prompts*

![[assets/figures/papers/paper_list_l2522_https_arxiv_org_abs_2512_07410/figures/008_Figure.jpg]]
*Figure: RS + 3 stream DiT FIG + 1 stream DiT FIG + 2 stream DiT FIG + 3 stream DiT SIG + 3 stream DiT “One charges forward while the other raises both hands in defense.”*

![[assets/figures/papers/paper_list_l2522_https_arxiv_org_abs_2512_07410/figures/012_Figure.jpg]]

![[assets/figures/papers/paper_list_l2522_https_arxiv_org_abs_2512_07410/figures/013_Figure.jpg]]

## 方法谱系与知识库定位

### 1. 与基线方法的关系

InterAgent 处于**物理仿真驱动的文本到多智能体交互生成**这一新兴交叉点，其直接对手可分为两类：物理化运动基线与端到端物理控制基线。

**物理化文本到交互基线。** 最具竞争力的方法是 **InterGen++** 和 **InterMask++**，它们本身并非端到端物理控制方法，而是将 InterGen/InterMask 生成的 kinematic 运动序列通过一个独立的跟踪策略（tracking policy）转化为物理仿真中的关节力矩。这种级联架构存在两个固有弱点：(1) 运动生成阶段不考虑物理约束，导致跟踪策略需要纠正的运动偏差较大，容易产生漂浮、滑步等伪影；(2) 跟踪策略的训练目标与文本条件解耦，无法保证物理化后的行为仍与文本语义一致。InterAgent 以端到端自回归扩散框架直接预测状态-动作序列，消除了运动生成与物理仿真之间的信息断层，在 R-precision Top-3 上以 0.615 对 0.542 显著超越 InterGen++，FID 从 0.943 降至 0.582（Table 1），降幅达 38%。

**端到端物理控制基线。** **PDP** (Physics-based Diffusion Policy) 和 **CLoSD** (Closing the Loop between Simulation and Diffusion) 代表了单智能体物理扩散策略的当前水平。它们虽然也采用端到端范式，但核心架构为单流 DiT，将本体感知、外部感知和动作合并为单一 token 序列处理。这种设计在多智能体场景下暴露了两个瓶颈：(1) 异质模态的统计特性差异被强行混合，扩散模型难以学习到各自的条件分布；(2) 缺乏对智能体间空间依赖的显式建模，外部感知仅以简单的相对状态（RS）表示，信息密度低。InterAgent 的三流解耦架构直接回应了这些缺陷，消融实验（Table 2）显示单流变体的 R-precision Top-3 仅为 0.523，FID 高达 0.828，与三流 SIG 变体（0.615 / 0.582）的差距印证了解耦建模的因果作用。

### 2. 关键技术谱系

InterAgent 的方法设计可追溯至三条技术脉络的融合：

**扩散策略（Diffusion Policy）。** 自 Chi et al. (RSS 2023) 将扩散模型引入机器人动作生成以来，扩散策略已成为物理控制的主流范式。InterAgent 继承了自回归扩散框架，但将其从单智能体操控扩展到多智能体交互，核心改造在于用交互图外部感知替代简单的物体位姿观测，并将条件生成空间从单智能体动作序列扩展为双智能体的联合状态-动作序列。

**多流 Transformer。** 多流架构在多媒体理解（如 VideoBERT 的双流、MMT 的多流）中已有验证，其核心思想是对不同模态保持独立编码路径，仅在关键层进行跨模态融合。InterAgent 将这一思想迁移到物理控制领域，三条流分别对应本体感知（关节状态）、外部感知（交互图边向量）和动作（关节力矩/目标位姿），并通过 inter-stream fusion attention 实现流间信息交换（Figure 3）。这一设计使得每个模态的 token 分布保持稳定，扩散过程仅需学习各流内部的去噪映射，训练稳定性显著提升。

**图神经网络与稀疏注意力。** 交互图（IG）的构建借鉴了图网络在人体姿态建模中的应用（如 ST-GCN），将两个智能体的所有关节对建模为有向完全图，每条边编码相对位置向量（Eq. 2）。然而，完全图的边数随关节数平方增长（$J \times J$ 条边），大量冗余连接会淹没关键交互信号。InterAgent 引入的 Gumbel-Softmax + Top-K 稀疏注意力（Eq. 4-6）与 Graph Transformer 中的稀疏图池化思路一致，但创新在于稀疏化发生在**边级**而非节点级——这意味着模型可以动态选择“哪些关节对之间的空间关系对当前交互最重要”，而非简单地丢弃某些关节。Table 3 的消融证实，边级稀疏（1/2 稀疏比）优于关节级稀疏和非稀疏注意力，R-precision Top-3 从 0.588（非稀疏）提升至 0.615。

### 3. 适用边界与局限

**固定智能体数量。** InterAgent 的训练和推理均假设恰好两个智能体。扩展至 $N$ 个智能体时，交互图的边数将增长为 $\mathcal{O}(N^2 J^2)$，稀疏注意力虽然能部分缓解计算压力，但网络架构本身（两个权值共享的 Inter-DiT）需要重新设计以支持可变数量的智能体流。这是一个架构层面的限制，而非简单的数据扩展问题。

**高度动态行为的失效。** 论文明确承认模型在跳跃等爆发性动作上表现不佳（Figure 9）。根本原因在于扩散模型的去噪过程天然倾向平滑轨迹，而跳跃需要在极短时间窗口内产生大幅度的关节加速度和地面反作用力。当前的 L2 扩散损失（Eq. 3）对高频动力学成分的惩罚权重不足，导致模型倾向于“保守”地生成类站立或缓慢移动的行为。可能的改进方向包括在损失中引入加速度惩罚项，或采用 flow matching 等替代生成范式。

**Sim-to-Real 鸿沟。** 当前所有实验均在 Isaac Gym 仿真环境中完成，使用简化的人形模型（13 个关节，21 个自由度）。部署到真实人形机器人面临三重挑战：(1) 仿真中的理想关节力矩控制与真实电机的非线性响应之间存在分布偏移；(2) 自回归推理（预测视野 $m=4$，历史缓存 $h=364$）的实时性要求在边缘设备上难以满足；(3) 交互图外部感知依赖精确的对方关节位置估计，这在真实多智能体场景中需要鲁棒的多视角姿态估计系统。

### 4. 开放问题与后续工作方向

1. **可变数量智能体的可扩展架构。** 如何设计一个支持 2 到 $N$ 个智能体的统一框架，使交互图表示和注意力机制能够随智能体数量线性扩展而非平方增长？可能的思路包括引入智能体级别的层次化图池化，或采用基于集合的注意力（如 Perceiver）替代全对全的边建模。

2. **高层规划与低层控制的整合。** InterAgent 目前直接根据文本指令生成短时行为（预测视野仅 4 帧，约 0.13 秒）。对于需要多轮协作的复杂交互（如“A 将球传给 B，B 接球后投篮”），需要引入高层任务规划模块（如 LLM-based planner）将长时文本分解为子任务序列，再由 InterAgent 逐段执行。这涉及离散符号规划与连续物理控制的对齐问题。

3. **动态行为的物理约束注入。** 解决跳跃等动态行为失效的一个可能路径是在扩散采样过程中加入物理约束引导（如足部离地高度、质心加速度阈值），类似于 classifier-guided diffusion 但约束来自物理规则而非分类器。这需要设计可微的物理约束函数，并平衡约束强度与生成多样性。

4. **真实世界部署的域适应。** 从仿真到真实的迁移可通过域随机化（在训练中引入传感器噪声、质量扰动、地面摩擦变化）和在线自适应（利用真实机器人数据微调跟踪策略或扩散模型）两步走。但多智能体场景下的在线数据采集成本极高，可能需要探索基于离线 RL 或模仿学习的 sim-to-real 策略。

## 原文 PDF

![[paperPDFs/CVPR_2026/InterAgent_Physics_based_Multi_agent_Command_Execution_via_Diffusion_on_Interaction_Graphs.pdf]]
