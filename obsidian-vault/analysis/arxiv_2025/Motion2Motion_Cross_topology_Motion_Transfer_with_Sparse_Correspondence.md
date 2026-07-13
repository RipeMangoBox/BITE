---
title: "Motion2Motion: Cross-topology Motion Transfer with Sparse Correspondence"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Motion2Motion_Cross_topology_Motion_Transfer_with_Sparse_Correspondence.pdf
project_link: null
code_link: null
aliases:
- Motion2Motion
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
core_operator: 关键调控因素是稀疏骨骼对应关系的数量与质量、运动补丁匹配的权重α以及迭代次数L，这些参数共同决定了迁移运动的保真度与多样性。
primary_logic: 通过观察少量目标骨骼的运动示例，未绑定关节的运动模式可以由绑定关节的运动补丁推断得出，从而以匹配-混合的方式实现跨拓扑迁移，无需密集对应或大规模训练。
claims:
- 在相似骨骼和跨物种设置中，Motion2Motion 的 FID 指标显著优于现有基线（WalkTheDog, Pose-to-Motion）。
- 仅用 6 个后肢骨骼绑定，即可将火烈鸟的行走动作迁移到猴子骨架，未绑定的前肢和尾部动作也能合理推断。
- 用户研究显示，Motion2Motion 在运动质量和对齐度上均显著领先于基线，质量评分达 4.36（满分5）。
- 该方法无需 GPU 和模型训练，在 CPU 上实现实时推理（FPS 752–778），同时保持高水平的运动质量。
---

# Motion2Motion: Cross-topology Motion Transfer with Sparse Correspondence

> [!tip] 核心洞察
> 通过观察少量目标骨骼的运动示例，未绑定关节的运动模式可以由绑定关节的运动补丁推断得出，从而以匹配-混合的方式实现跨拓扑迁移，无需密集对应或大规模训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | Motion2Motion：基于稀疏对应的跨拓扑运动迁移 |
| 英文题名 | Motion2Motion: Cross-topology Motion Transfer with Sparse Correspondence |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2506.03901) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation |
| Method | Motion2Motion |
| Dataset | Similar Skeleton Transfer, Cross-species Skeleton Transfer, User Study |

> [!tip] 效果简介
> - Similar Skeleton Transfer 上，FID 0.033 vs 0.389 (Pose-to-Motion) (-0.356)。
> - Cross-species Skeleton Transfer 上，FID 0.492 vs 1.68 (Pose-to-Motion) (-1.188)。
> - User Study (5-point Likert) 上，Motion Quality 4.36 ± 0.18 vs 3.55 ± 0.22 (WalkTheDog) (+0.81)。

## 概要

**问题瓶颈**：跨拓扑运动迁移的核心困难在于源骨骼与目标骨骼之间的拓扑不一致性——关节数量、层级结构、语义对应均不相同，无法建立直接的一对一骨骼映射。同时，缺乏跨拓扑的大规模配对运动数据，使得数据驱动的监督学习方法难以泛化到未见过的骨架组合。

**核心洞见**：Motion2Motion 提出了一种免训练的跨拓扑运动迁移框架。其关键观察在于：通过少量目标骨骼的运动示例，未绑定关节的运动模式可以由已绑定关节的运动补丁推断得出。方法将运动迁移建模为**基于稀疏骨骼对应的条件运动补丁匹配问题**——用户仅需指定少量关键点对应关系作为空间条件，系统通过匹配-混合机制自动完成剩余关节的运动推断。

**方法定位**：与依赖神经网络预训练的 **WalkTheDog**（Li et al., SIGGRAPH 2024）和 **Pose-to-Motion**（Zhao et al., SCA 2024）不同，Motion2Motion 无需 GPU 和模型训练，仅需目标骨架的 1～3 个运动示例即可在 CPU 上实现实时推理（FPS 752–778）。方法可处理从同物种到极端跨物种（如无肢蟒蛇到两足猛禽）的拓扑差异。

**主要结果**：在相似骨架和跨物种两种设置下，Motion2Motion 的 FID 指标均显著优于基线（相似骨架：0.033 vs. 0.389；跨物种：0.492 vs. 1.68）。用户研究进一步表明，该方法在运动质量（4.36/5.0）和对齐度上均显著领先。消融实验验证了稀疏绑定的有效性——仅 6.1% 的绑定率即可在运动保真度与解剖合理性之间取得最佳平衡。

### 问题背景：跨拓扑运动迁移的核心挑战

在计算机动画与角色控制领域，运动迁移（Motion Transfer）旨在将源角色的动作序列重定向到目标角色上，使后者在保持自身骨骼结构的前提下复现源动作的运动语义与风格。这一任务在电影制作、游戏开发、虚拟人驱动等场景中具有广泛的应用需求。

然而，当源角色与目标角色的骨骼拓扑存在显著差异时——例如将蟒蛇的蜿蜒爬行动作迁移到双足猛禽，或将火烈鸟的双足行走迁移到四足猴——传统运动迁移方法面临根本性瓶颈。这一瓶颈的实质在于**拓扑不一致性**：源骨骼与目标骨骼之间无法建立直接的一对一骨骼对应关系，导致依赖密集对应或全连接映射的方法失效。与此同时，**跨拓扑的大规模配对运动数据极为稀缺**，限制了数据驱动方法的泛化能力。这两个因素共同构成了跨拓扑运动迁移的核心挑战。

### 现有方法缺口：数据依赖与拓扑刚性

当前主流的运动迁移方法大致可分为两类：

- **基于优化的方法**（如 **WalkTheDog**, Li et al., SIGGRAPH 2024）利用相位流形等中间表示实现跨形态运动对齐，但通常需要针对特定骨架对进行精细调优，且在拓扑差异极大时对齐质量下降。
- **基于学习的方法**（如 **Pose-to-Motion**, Zhao et al., SCA 2024）依赖大规模运动数据预训练神经网络或扩散模型，将运动重定向建模为条件生成问题。这类方法在训练分布内表现良好，但面对未见过的骨架拓扑时泛化能力有限，且推理过程通常需要 GPU 支持。

两类方法的共同缺陷在于：**对密集骨骼对应或大规模配对训练数据的依赖**，以及**对极端拓扑变化的适应性不足**。此外，现有方法在处理跨物种迁移时，往往需要针对每对源-目标骨架重新训练或调整模型，缺乏即插即用的灵活性。

### 本文动机：从稀疏对应到免训练迁移

本文的核心观察是：**通过观察少量目标骨骼的运动示例，未绑定关节的运动模式可以由绑定关节的运动补丁推断得出**。换言之，用户只需指定源骨骼与目标骨骼之间极少量的关键点对应关系（如 6 个后肢骨骼绑定），即可为跨拓扑迁移提供足够的空间约束条件。基于这一洞察，本文提出 **Motion2Motion** 方法，将跨拓扑运动迁移建模为**基于运动补丁的条件匹配与混合问题**（conditional patch-based motion matching and blending），从根本上规避了对密集对应和大规模训练的依赖。

与现有方法相比，Motion2Motion 的设计动机体现在三个层面：

1. **稀疏对应替代密集映射**：仅需用户指定或自动匹配的少量骨骼对应关系（绑定率约 6.1%），即可驱动迁移过程，大幅降低人工标注成本。
2. **匹配-混合替代生成模型**：通过从目标骨骼的运动补丁数据库中检索最相似补丁并进行混合，实现运动合成，无需任何模型训练。
3. **CPU 实时推理替代 GPU 依赖**：方法在纯 CPU 上运行，推理速度达 752–778 FPS，满足实时动画制作需求。

这一设计使得 Motion2Motion 能够处理从同物种（蟒蛇→眼镜王蛇）到跨物种（蟒蛇→霸王龙、火烈鸟→猴）的极端拓扑变化，在运动质量、时间一致性和多样性上均显著优于现有基线。

## 核心方法与创新机理

Motion2Motion 的核心创新在于将跨拓扑运动迁移重新定义为**基于运动补丁的条件匹配问题**，而非传统的神经网络回归或优化问题。这一范式转换带来了五个关键维度的突破：

### 1. 稀疏骨骼对应替代密集映射

传统方法（如 **WalkTheDog** (Li et al., SIGGRAPH 2024) 和 **Pose-to-Motion** (Zhao et al., SCA 2024)）依赖密集骨骼对应、全连接映射或隐式学习的对应关系，要求源骨架与目标骨架具有相似拓扑结构。Motion2Motion 仅需用户指定极少量的骨骼关键点对应（如 Fig. 7 中仅绑定 6 个后肢骨骼），通过对应矩阵 $\mathbf{C}$ 将匹配骨骼通道对齐，未绑定关节的运动则由匹配-混合机制自动推断。这一设计使得方法可跨越极端拓扑差异（如无肢蟒蛇到两足猛禽，Fig. 8），突破了传统重定向方法对拓扑一致性的硬性约束。

### 2. 匹配-混合机制替代神经网络生成

现有方法普遍采用扩散模型、神经网络或优化方法生成目标运动，需要大规模配对数据预训练。Motion2Motion 采用免训练的**运动补丁匹配与混合**策略：将源运动分割为重叠补丁后，通过掩码运动匹配损失（Eq. 3）在目标运动补丁数据库中检索最相似补丁，再对所有匹配补丁进行平均混合以重建目标运动。该机制本质上扮演了**频率插值器**的角色，通过灵活组合目标域的运动片段实现迁移，避免了生成模型的模式坍塌和训练开销。

### 3. 免训练与纯 CPU 实时推理

与基线方法依赖 GPU 和深度模型训练不同，Motion2Motion 完全免训练，仅需目标骨架的 1–3 个运动示例作为匹配数据库。在 MacBook M1 CPU 上即可实现 752–778 FPS 的实时推理速度（Table 1），与 WalkTheDog 在 NVIDIA RTX-3090 GPU 上的 FPS 相当，且远快于 Pose-to-Motion。这一特性大幅降低了运动迁移的计算门槛和部署成本。

### 4. 加权掩码损失平衡绑定与未绑定区域

匹配损失函数引入权重 $\alpha$ 和掩码向量 $\mathbf{m}$，对绑定区域和未绑定区域分别加权：

$$
\alpha \mathcal{L}(\mathbf{m} \odot \mathbf{P}, \mathbf{m} \odot \mathbf{P}^{(\widehat{t})}) + (1-\alpha) \mathcal{L}((1-\mathbf{m}) \odot \mathbf{P}, (1-\mathbf{m}) \odot \mathbf{P}^{(\widehat{t})})
$$

默认 $\alpha=0.85$（Table 5 消融验证）使匹配过程既优先保持绑定关节的运动保真度，又允许未绑定区域在目标运动空间中自由检索最合理的运动模式，从而在运动保真度和解剖合理性之间取得平衡。

### 5. 迭代优化与噪声驱动的多样性控制

通过 $L=3$ 次迭代匹配与混合（Algorithm 1），逐步增强迁移运动的时间一致性。同时，在运动投影阶段对未映射维度添加噪声 $\mathbf{N}$（Eq. 2），为同一源运动生成多样化的目标运动结果（Fig. 8）。消融实验（Table 5）表明，$L=3$、补丁大小 $P_S=11$、$\alpha=0.85$ 在 FID、频率对齐、接触一致性和多样性之间达到最优平衡。

### 创新总结

| 维度 | 基线方法 | Motion2Motion |
|------|---------|---------------|
| 对应关系 | 密集/隐式学习 | 稀疏骨骼对应（用户指定） |
| 合成机制 | 神经网络/扩散模型/优化 | 运动补丁匹配与混合 |
| 训练需求 | 大规模数据预训练 | 免训练，仅需 1–3 个目标示例 |
| 推理平台 | GPU 依赖 | 纯 CPU 实时（>750 FPS） |
| 拓扑适应性 | 限于相似拓扑 | 跨极端拓扑（无肢↔两足） |

这些创新共同构成了一个**轻量、灵活且无需训练**的跨拓扑运动迁移框架，其核心洞见在于：未绑定关节的运动模式可由绑定关节的运动补丁通过匹配-混合推断得出，无需建立密集对应或依赖大规模配对数据。

Motion2Motion 将跨拓扑运动迁移建模为一个**基于运动补丁的条件匹配与混合问题**，其核心思想是：通过用户指定的少量骨骼对应关系作为空间条件，引导源运动在目标骨骼上的重构，而无需密集对应或大规模预训练。

### 流水线总览

整个框架由七个顺序模块构成，形成一条从源运动到目标运动的端到端处理链路（图2）：

1. **静息姿态预对齐**：将源骨架与目标骨架的静止姿态统一到同一坐标系，消除全局姿态差异。
2. **运动补丁化**：沿时间轴对源运动序列进行无填充的滑窗切分，生成重叠的固定长度运动补丁。补丁数量由公式 $P = \frac{F_s - \text{patch size} + 1}{\text{step size}}$ 确定。
3. **稀疏对应定义**：用户指定源骨架与目标骨架之间的关键点匹配对集合 $\mathcal{M}$，据此构建对应矩阵 $\mathbf{C}$ 和掩码向量 $\mathbf{m}$。$\mathbf{C}$ 在对应骨骼通道上为单位矩阵块，其余为零矩阵。
4. **运动投影**：利用对应矩阵将源运动补丁投影到目标骨架空间，对未映射维度注入噪声以提供多样性种子：$\mathbf{P}^{s\to t} = \mathbf{S}\mathbf{C}^{\top} + (\mathbf{1} - \mathbf{m}) \odot \mathbf{N}$。
5. **掩码运动匹配**：以投影后的补丁为查询，在预构建的目标运动补丁数据库中检索最相似补丁。匹配损失为映射部分与未映射部分的加权 MSE：$\alpha\mathcal{L}(\mathbf{m}\odot\mathbf{P}, \mathbf{m}\odot\mathbf{P}^{(\widehat{t})}) + (1-\alpha)\mathcal{L}((1-\mathbf{m})\odot\mathbf{P}, (1-\mathbf{m})\odot\mathbf{P}^{(\widehat{t})})$。
6. **运动混合**：对所有匹配到的目标补丁进行平均混合，重建完整的目标运动序列。
7. **迭代优化**：重复匹配与混合 $L$ 次（默认 $L=3$），以增强时间一致性。

### 输入输出规范

- **输入**：源运动序列 $\mathbf{S} \in \mathbb{R}^{F_s \times D_s}$，目标骨架的 1～3 个运动示例，以及用户指定的稀疏骨骼对应关系 $\mathcal{M}$。
- **输出**：重定向后的目标运动序列 $\widehat{\mathbf{T}} \in \mathbb{R}^{F_s \times D_t}$，其帧数与源运动一致，维度与目标骨架匹配。

### 关键设计决策

流水线的核心调控参数包括：**绑定率**（$2|\mathcal{M}|/(J_S+J_T) \times 100\%$）、**混合权重 $\alpha$**（默认 0.85）和**迭代次数 $L$**。消融实验表明，绑定率在约 6.1% 时达到运动保真度与解剖合理性的最佳平衡；$\alpha=0.85$ 在映射保真与未映射多样性之间取得最优折衷；$L=3$ 可有效改善时间一致性，继续增加则收益递减。

与现有方法的关键区别在于：整个流水线**无需 GPU 和模型训练**，仅依赖目标骨架的少量运动示例即可在 CPU 上实现实时推理（FPS 752–778），同时保持跨极端拓扑（如无肢到两足、不同物种）的迁移能力。


Motion2Motion 将跨拓扑运动迁移形式化为一个**条件化的运动补丁匹配与混合**问题，其核心流程由七个模块串联构成，整体框架如 Fig. 2 所示。

### 3.1 静息姿态预对齐

在迁移开始前，首先对源骨架和目标骨架的静息姿态（T-pose 或 A-pose）进行全局旋转与位移对齐，将二者统一到同一坐标系下。该步骤消除了骨骼朝向和位置差异带来的系统性偏差，为后续的稀疏对应和运动投影提供一致的参考空间（见 Section 3.1）。

### 3.2 运动补丁化（Motion Patching）

将源运动序列 $\mathbf{S} \in \mathbb{R}^{F_s \times D_s}$ 沿时间轴通过滑窗切分为重叠的固定长度补丁。补丁数量由下式确定：

$$P = \frac{F_s - \text{patch size} + 1}{\text{step size}}$$

其中 $F_s$ 为源序列总帧数，patch size 为补丁长度，step size 为滑窗步长。每个补丁携带一段局部运动模式，作为后续匹配与迁移的基本单元。目标骨架的运动示例也以相同方式构建补丁数据库 $\mathcal{P}^{(t)}$（见 Section 3.2）。

### 3.3 稀疏对应定义（Sparse Correspondence Definition）

设 $\mathcal{M} = \{(t, s) \mid t \in \mathcal{T}_T, s \in \mathcal{T}_S\}$ 为用户指定或自动匹配的稀疏关键点对应集合，其中 $\mathcal{T}_T$ 和 $\mathcal{T}_S$ 分别为目标和源骨架的骨骼索引集。基于此定义对应矩阵 $\mathbf{C}$ 和掩码向量 $\mathbf{m}$。

对应矩阵 $\mathbf{C}$ 的结构为块对角形式，仅在对齐的骨骼通道上放置单位矩阵：

$$\mathbf{C}\Big[\mathcal{I}_1(t):\mathcal{I}_2(t),\ \mathcal{I}_1(s):\mathcal{I}_2(s)\Big] = \begin{cases} \mathbf{I}, & \mathrm{if}\ (t,s)\in\mathcal{M},\\ \mathbf{O}, & \mathrm{otherwise} \end{cases}$$

其中 $\mathcal{I}_1(\cdot)$ 和 $\mathcal{I}_2(\cdot)$ 分别表示某骨骼在运动特征向量中的起始和结束通道索引。掩码向量 $\mathbf{m}$ 则标记哪些运动维度被对应关系覆盖（值为 1），哪些未被覆盖（值为 0）（见 Section 3.3, Eq. 1）。

### 3.4 运动投影（Motion Projection）

对于每个源运动补丁 $\mathbf{P}^{(s)}$，利用对应矩阵将其投影到目标骨架空间，并对未映射的维度注入高斯噪声以提供多样性种子：

$$\mathbf{P}^{s\to t} = \mathbf{S}\mathbf{C}^{\top} + (\mathbf{1} - \mathbf{m}) \odot \mathbf{N}$$

其中 $\mathbf{S}$ 为源补丁特征，$\mathbf{N} \sim \mathcal{N}(0, \sigma^2)$ 为噪声项，$\odot$ 表示逐元素乘法。投影后的补丁作为检索查询，在目标补丁数据库中寻找最佳匹配（见 Section 3.4, Eq. 2）。

### 3.5 掩码运动匹配（Masked Motion Matching）

匹配过程使用加权 MSE 损失，同时考虑映射部分和未映射部分：

$$\mathbf{P}^{\mathrm{match}} \gets \underset{\mathbf{P}\in\mathcal{P}^{(t)}}{\mathrm{arg\,min}}\ \alpha\mathcal{L}(\mathbf{m}\odot\mathbf{P},\mathbf{m}\odot\mathbf{P}^{(\widehat{t})}) + (1-\alpha)\mathcal{L}((1-\mathbf{m})\odot\mathbf{P},(1-\mathbf{m})\odot\mathbf{P}^{(\widehat{t})})$$

其中 $\mathcal{L}(\cdot,\cdot)$ 为均方误差（MSE），$\alpha \in [0,1]$ 为平衡映射与未映射部分重要性的权重。默认设置 $\alpha = 0.85$，使得匹配过程既忠实于绑定骨骼的运动语义，又允许未绑定部分通过数据库检索自然推断（见 Section 3.4, Eq. 3）。

### 3.6 运动混合（Motion Blending）

对所有匹配到的目标补丁进行平均混合，重建完整的目标运动序列。由于补丁是重叠切分的，混合过程天然具有平滑效果，有效抑制了补丁边界的不连续性（见 Section 3.4, Fig. 2-E, F）。

### 3.7 迭代优化（Iterative Refinement）

上述匹配与混合过程重复执行 $L$ 次，每次迭代以上一轮的输出作为新的查询，逐步增强时间一致性和运动质量。消融实验表明 $L=3$ 时收益趋于饱和，继续增加迭代次数改善有限（见 Table 5）。

### 关键调控参数总结

| 参数 | 含义 | 默认值 | 作用 |
|------|------|--------|------|
| $L$ | 匹配-混合迭代次数 | 3 | 控制时间一致性，过小则抖动，过大则收益递减 |
| $P_S$ | 运动补丁大小 | 11 | 决定局部运动模式的粒度 |
| $\alpha$ | 映射/未映射损失权重 | 0.85 | 平衡绑定保真度与未绑定推断自由度 |
| $\sigma$ | 投影噪声标准差 | — | 控制迁移结果的多样性 |
| 绑定率 | $\frac{2|\mathcal{M}|}{J_S + J_T} \times 100\%$ | 约 6.1% | 在保真度与解剖合理性间取得平衡 |

其中绑定率定义为匹配对应数量相对于源和目标骨骼关节总数的百分比。消融实验表明，绑定率在 6.1% 左右时运动保真度和解剖合理性达到最佳平衡——过小则缺乏一致性约束，过大则引入不匹配骨骼的干扰（见 Fig. 13）。

## 实验与关键发现

### 主要定量结果

Motion2Motion 在相似骨骼迁移与跨物种迁移两个核心场景下均取得了最优性能，且无需 GPU 训练即可实现实时推理。**Table 1** 汇总了与 **WalkTheDog**（Li et al., SIGGRAPH 2024）和 **Pose-to-Motion**（Zhao et al., SCA 2024）的全面对比。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2506_03901/figures/003_Table_1.jpg]]
*Table 1: Main evaluation results for motion transfer. Our method (Motion2Motion), in both similar skeleton and cross-species settings, achieves the best performance on synthesis quality, temporal coherence, and diversity. Different from baselines, our method runs without GPUs and deep model training*

在相似骨骼设置下，Motion2Motion 的 FID 达到 **0.033**，远优于 Pose-to-Motion 的 0.389（Δ = -0.356）；频率对齐度达 96.2%，接触一致性达 93.5%，运动多样性为 3.20，均显著领先。在跨物种设置下，该方法依然保持明显优势：FID 为 **0.492**，而 Pose-to-Motion 为 1.68（Δ = -1.188）；频率对齐度和接触一致性分别为 90.3% 和 79.7%，多样性为 1.90。

推理效率方面，Motion2Motion 在 MacBook M1 CPU 上达到 **752–778 FPS**，与 WalkTheDog 在 NVIDIA RTX-3090 GPU 上的速度可比，且远快于 Pose-to-Motion。需要注意的是，这一对比存在平台不公平性——本方法在 CPU 上运行，而基线均依赖 GPU——即便如此，其实时性依然突出。

### 定性对比

**Figure 3** 展示了从龙骨架到蝙蝠骨架的重定向逐帧对比。Motion2Motion 的结果更忠实地保留了源运动的风格、时间连贯性和运动频率，而 WalkTheDog 和 Pose-to-Motion 在部分帧中出现明显的姿态失真或频率不匹配。**Figure 4** 进一步揭示了匹配机制的工作原理：源运动（熊）的特定帧在目标运动数据库（狗）中找到了语义和时间上均对齐的补丁，验证了掩码运动匹配在跨拓扑场景下的有效性。

### 用户研究

**Table 3** 报告了 5 分 Likert 量表下的用户主观评分。在运动质量维度上，Motion2Motion 获得 **4.36 ± 0.18**，显著高于 WalkTheDog 的 3.55 ± 0.22 和 Pose-to-Motion 的 2.95 ± 0.10；在对齐度维度上同样大幅领先。这表明该方法不仅客观指标占优，在人类感知层面也具有明确优势。

### 测试时缩放特性

**Table 2** 展示了目标运动样本数量对迁移质量的影响。将目标样本数从 1 个增加到 3 个，FID 从 0.263 单调下降至 0.230，频率对齐和接触一致性也同步改善。这表明 Motion2Motion 具备“测试时缩放”（test-time scaling）特性：在不改变方法流程的前提下，仅增加目标示例即可持续提升迁移质量。

### 消融实验

#### 超参数敏感性

**Table 5** 对三个关键超参数进行了消融：迭代次数 $L$、补丁大小 $P_S$ 和混合权重 $\alpha$。默认设置 $L=3$、$P_S=11$、$\alpha=0.85$ 在 FID、频率对齐、接触一致性和多样性之间取得了最佳平衡。具体而言：

- **迭代次数** $L$：从 1 增至 3 可改善时间一致性，继续增加则收益递减。
- **补丁大小** $P_S$：过小导致上下文不足，过大则降低匹配精度。
- **混合权重** $\alpha$：控制映射部分与未映射部分在匹配损失中的相对重要性，0.85 的偏置使绑定骨骼的约束更强，同时保留未绑定部分的合理自由度。

#### 绑定机制与迁移策略

**Table 6** 对比了手动绑定与自动骨骼绑定，以及直接复制绑定运动特征（跳过匹配-混合）的策略。结果表明：

- 在相似骨骼场景下，自动绑定效果接近手动绑定，但跨物种时质量下降明显，说明复杂拓扑下人工先验仍具价值。
- 直接复制绑定关节的运动特征在相似骨架上质量略有提升，但在跨物种场景下效果更差。这验证了匹配-混合机制对于跨拓扑泛化的必要性——单纯复制无法推断未绑定关节的合理运动。

#### 绑定率的影响

**Figure 13** 探索了绑定率（定义为 $\frac{2|\mathcal{M}|}{J_S + J_T} \times 100\%$）对迁移质量的影响。在约 **6.1%** 的绑定率下，运动保真度和解剖合理性达到最佳平衡。绑定率过低会导致运动缺乏一致性，过高则可能引入源-目标骨骼间的不匹配约束，反而损害质量。**Figure 7** 给出了一个极端案例：仅绑定火烈鸟的 6 个后肢骨骼（绑定率约 6.1%），即可将其行走动作迁移至猴子骨架，未绑定的前肢和尾部运动被合理推断，验证了稀疏对应的有效性。

### 多样化迁移能力

**Figure 8** 展示了从无肢骨架（蟒蛇）到两足骨架（猛禽）的跨拓扑迁移，不同颜色的结果代表同一源运动在多次运行中产生的多样化输出。这种多样性由运动投影阶段的噪声项控制，使方法能够生成语义一致但细节各异的目标运动，满足动画制作中对可控多样性的需求。

### 失败模式与局限性

尽管整体性能优异，该方法仍存在以下已知局限：

1. **语义鸿沟**：当源动作与目标动作的语义差异较大时（如功夫动作迁移到舞蹈骨架），自动绑定和匹配质量可能下降，因为目标运动数据库中缺乏语义匹配的补丁。
2. **目标示例依赖**：需要 1–3 个目标骨架的运动示例，在极端稀缺的场景下可能增加数据准备成本。
3. **绑定率确定**：最优绑定率目前依赖手动调整或启发式自动算法，尚未实现全自动最优策略。
4. **极端拓扑**：论文主要在脊椎动物骨架间进行验证，对于更极端的拓扑结构（如昆虫骨架）的有效性仍需进一步检验。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2506_03901/figures/007_Figure_6.jpg]]
*Figure 6: Phase visualization of the motion. (A) and (B) present the phases of RightToe and LeftToe. The bar figure is the phase variation curve, and the clock figure is the phase visualization at the 1-st and 10-th frames. The blue and orange colors denoted retargeted and source motion, respectively. Note that there is a consistent phase bias between the source and target*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2506_03901/figures/019_Figure_13.jpg]]
*Figure 13: (b) (B) Cross-species skeleton motion transfer. Fig. 13. Comparison of different binding rates*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2506_03901/figures/009_Table_2.jpg]]
*Table 2: “Test time scaling” property. The comparison with different number of target samples*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2506_03901/figures/017_Table_6.jpg]]
*Table 6: Ablation study of binding mechanism and transfer strategies. We compare automatic and manual bone binding, as well as direct copying bound motion features from the source after executing Algorithm 1*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2506_03901/figures/004_Figure_3.jpg]]
*Figure 3: Quantitative comparison with baselines. Each animation sequence is listed as frames from left to right. (Highlighted gray frames as comparison for baselines.) (A) Input source motion of a dragon character. (B–D) Retargeted sequences on the bat skeleton produced by (B) our method, (C) Li et al. [2024], and (D) Zhao et al. [2024]. Compared to baselines, our approach more faithfully preserves the original motion style, coherence, and frequency*

## 定位与知识库关联

### 1. 与现有基线的对比定位

Motion2Motion 在运动迁移的方法谱系中占据一个独特位置：它处于传统运动重定向（motion retargeting）与数据驱动的跨域运动生成之间的交叉地带，但通过**免训练的匹配-混合范式**绕开了两者的核心瓶颈。

**相对于 WalkTheDog（Li et al., SIGGRAPH 2024）**：WalkTheDog 构建了基于相位流形的跨形态运动对齐框架，其核心思路是通过相位变量将不同形态的运动映射到统一流形空间，再实现对齐。该方法本质上仍依赖密集的骨骼对应或隐式学习到的形态映射。Motion2Motion 与之的关键分岔点在于：WalkTheDog 需要建立全局运动流形，而 Motion2Motion 仅需**稀疏骨骼对应**作为空间条件，通过局部运动补丁的匹配与混合完成迁移。这一差异使得 Motion2Motion 在拓扑差异极大的场景（如无肢到两足）中表现出更强的适应性——WalkTheDog 的流形假设在极端拓扑变化下可能失效，而 Motion2Motion 的补丁级匹配天然具备局部灵活性。

**相对于 Pose-to-Motion（Zhao et al., SCA 2024）**：Pose-to-Motion 采用基于姿态先验的跨域运动重定向策略，通常需要大量运动数据进行预训练，且推理依赖 GPU。Motion2Motion 与之形成鲜明对比：**完全免训练**，仅需目标骨骼的 1～3 个运动示例即可工作，在纯 CPU 上实现实时推理（FPS 752–778，Table 1）。这一差异源于方法论的根本不同——Pose-to-Motion 依赖神经网络学习运动分布，而 Motion2Motion 将问题重新定义为条件运动补丁匹配，将“生成”替换为“检索与重组”。

**相对于更广泛的运动迁移文献**：传统运动重定向方法（如基于 IK 的骨骼映射）要求源与目标骨架之间存在明确的关节级对应，无法处理跨拓扑场景。近年来基于扩散模型或 Transformer 的运动生成方法虽然可以跨域生成，但通常需要大规模训练数据且推理速度慢。Motion2Motion 的**核心创新**在于揭示了：通过观察少量目标骨骼的运动示例，未绑定关节的运动模式可以由绑定关节的运动补丁推断得出——这一洞察使得匹配-混合机制成为跨拓扑迁移的高效替代方案。

### 2. 适用边界与条件约束

Motion2Motion 的有效性建立在以下几个前提条件之上，这些条件同时定义了其适用的边界：

- **目标运动示例的可用性**：方法需要至少 1 个（理想情况下 3 个）目标骨骼的运动序列作为匹配数据库。当目标样本从 1 个增加到 3 个时，FID 单调降低（Table 2），说明示例的丰富度直接影响迁移质量。在动画制作流程中，这意味着需要为目标角色预先采集或手工制作少量运动数据，增加了前期准备成本。

- **源与目标运动语义的相容性**：匹配-混合机制假设源运动的局部模式可以在目标运动数据库中找到有意义的对应。当源动作与目标动作语义差异过大时（例如将功夫动作迁移到舞蹈骨架），自动绑定和匹配质量可能下降。这是因为目标数据库中缺乏与源运动语义相似的补丁，导致匹配结果在语义上不协调。

- **骨骼绑定率的最优区间**：消融实验表明，绑定率在约 6.1% 左右时，运动保真度和解剖合理性达到最佳平衡（Fig. 13）。绑定率过小则缺乏一致性约束，过大则引入不匹配的骨骼约束。当前绑定率的确定依赖手动调整或自动算法，尚未实现全自动最优绑定策略。

- **拓扑差异的极限**：虽然 Motion2Motion 已展示了从无肢（蟒蛇）到两足（猛禽）、从两足（火烈鸟）到四足（猴子）的跨物种迁移，但对于更极端的拓扑结构（如昆虫骨架、多足生物），其有效性尚未验证。这构成了方法的已知未知边界。

### 3. 局限性与失效模式

基于已验证的分析，Motion2Motion 存在以下明确的局限性：

1. **对目标运动示例的依赖**：尽管仅需少量示例，但在实际动画制作中，为目标角色采集运动数据可能增加工作流成本。这一依赖限制了方法在“零样本”场景下的应用——即完全没有任何目标骨骼运动数据时，方法无法工作。

2. **语义鸿沟问题**：当源运动与目标运动的语义类别差异显著时，匹配机制可能产生不合理的迁移结果。这是因为匹配损失（Eq. 3）仅基于运动学特征的 MSE，缺乏对高层语义的理解。例如，将“跳跃”动作迁移到“游泳”骨骼时，目标数据库中可能不存在语义匹配的补丁。

3. **绑定策略的次优性**：当前方法依赖用户手动指定骨骼对应或自动绑定算法。自动绑定在类似骨架上效果接近手动绑定，但在跨物种场景下质量下降明显（Table 6）。这暗示自动绑定算法在拓扑差异大时可能产生不合理的对应关系，进而损害迁移质量。

4. **直接复制的失效**：消融实验显示，直接复制绑定关节的运动特征（跳过匹配-混合步骤）在类似骨架上质量略有提升，但在跨物种上效果更差（Table 6）。这反证了匹配-混合机制对于跨拓扑泛化是不可或缺的——简单的特征复制无法处理拓扑差异带来的分布偏移。

5. **推理平台的不公平比较**：Motion2Motion 在 MacBook M1 CPU 上运行，而基线 WalkTheDog 和 Pose-to-Motion 在 NVIDIA RTX-3090 GPU 上运行。虽然 Motion2Motion 在 FPS 上仍与 WalkTheDog 可比且远快于 Pose-to-Motion，但这种硬件差异使得绝对速度对比存在不公平性。

### 4. 开放问题与未来方向

基于方法的当前状态和已验证的局限性，以下几个开放问题值得进一步探索：

- **最优绑定率的理论刻画**：当前绑定率通过经验消融确定（Fig. 13），但缺乏理论指导。是否存在一个基于源与目标骨骼拓扑差异的绑定率下界？能否从信息论角度解释“6.1%”这一经验最优值的来源？

- **零样本跨拓扑迁移**：能否完全消除对目标运动示例的依赖？可能的路径包括：利用大规模运动数据的预训练先验来初始化目标运动补丁数据库，或通过物理模拟生成虚拟目标运动作为匹配候选项。

- **语义感知的匹配机制**：当前匹配损失（Eq. 3）仅基于运动学 MSE，无法区分语义不同的运动模式。引入对比学习或语义嵌入来指导匹配过程，可能改善语义差异大时的迁移质量。

- **扩展到物理动画**：该匹配-混合框架能否应用于基于物理的角色动画，包括布料和毛发动力学？这需要将运动补丁的概念从骨骼运动扩展到变形场，并处理物理约束的满足问题。

- **极端拓扑的泛化验证**：在昆虫骨架、多足生物、软体动物等更极端的拓扑结构上系统评估方法的有效性，以确定其泛化边界。这同时需要扩展骨骼对应定义，以处理非标准关节类型（如球形关节、弹性连接）。

## 原文 PDF

![[paperPDFs/arxiv_2025/Motion2Motion_Cross_topology_Motion_Transfer_with_Sparse_Correspondence.pdf]]
