---
title: Ponimator Unfolding Interactive Pose for Versatile Human-human Interaction Animation
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/Ponimator_Unfolding_Interactive_Pose_for_Versatile_Human_human_Interaction_Animation.pdf
project_link: https://stevenlsw.github.io/ponimator/
code_link: null
aliases:
- PUIPVHHIA
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 以交互姿态作为中间锚点，并将任务解耦为基于空间先验的姿态生成和基于时间先验的运动动画两个阶段。
primary_logic: 交互姿态蕴含着丰富的时空先验，能够作为桥梁连接姿态生成与运动动画，使得模型只需少量条件即可在各种输入（如图像、文本）下生成逼真的双人交互动态。
claims:
- 在 Inter-X 数据集上，本方法在无约束交互生成任务中 FID 达到 22.6，远优于 InterGen 的 56.6。
- 消融实验表明，移除交互姿态锚定导致 Inter-X 上的 FID 从 5.0 上升至 7.1。
- 本方法在 Inter-X 和 Dual-Human 数据集上均显著提升接触率 (Contact Ratio)，证明交互姿态先验能有效保证物理接触。
- Inter-X (unconstrained) 上 FID↓ = 22.6
---

# Ponimator Unfolding Interactive Pose for Versatile Human-human Interaction Animation

> [!tip] 核心洞察
> 交互姿态蕴含着丰富的时空先验，能够作为桥梁连接姿态生成与运动动画，使得模型只需少量条件即可在各种输入（如图像、文本）下生成逼真的双人交互动态。

| 字段 | 内容 |
|------|------|
| 中文题名 | Ponimator: 展开交互姿态以实现多用途人-人交互动画 |
| 英文题名 | Ponimator Unfolding Interactive Pose for Versatile Human-human Interaction Animation |
| 会议/期刊 | ICCV 2025 |
| Links | [Project](https://stevenlsw.github.io/ponimator/) · [paper](https://arxiv.org/abs/2510.14976) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Ponimator |
| Dataset | Inter-X, Dual-Human |

> [!tip] 效果简介
> - Inter-X (unconstrained) 上，FID↓ 22.6 vs 56.6 (InterGen) (-34.0)。
> - Inter-X (pose animation) 上，FID↓ 5.0 vs 7.1 (w/o anchor) (-2.1)。
> - Dual-Human (pose animation) 上，FID↓ 24.2 vs 36.9 (w/o anchor) (-12.7)。

## 概要

**核心问题**：生成逼真的双人交互动态存在一个关键瓶颈——现有方法难以在保证运动自然感的同时维持物理接触，并且无法将高质量动作捕捉数据中的交互先验有效迁移到开放域图像或文本输入中。直接端到端生成往往导致穿透、滑动和接触缺失。

**核心思路**：Ponimator 提出以**交互姿态（interactive pose）**作为中间锚点，将任务解耦为两个阶段：① 基于空间先验的姿态生成器，从单姿态、文本或两者生成交互姿态；② 基于时间先验的姿态动画器，从交互姿态展开前后文运动序列。交互姿态蕴含丰富的时空先验，成为连接生成与动画的桥梁，使模型仅需少量条件即可产出逼真的双人动态。

**方法定位**：Ponimator 属于**解耦式条件扩散模型**，由两个扩散模块串联构成：姿态动画器以交互姿态为条件，通过插补策略（交互帧噪声置零）和残差去噪目标生成运动；姿态生成器通过统一掩码机制灵活融合文本与单姿态条件。与 **InterGen**（Liang et al., CVPR 2024）、**ComMDM**（Liu et al., CVPR 2024）等端到端方法不同，Ponimator 显式利用交互姿态先验，而非直接从文本或噪声映射到完整运动序列。

**主要结果**：在 Inter-X 数据集的无约束交互生成任务中，Ponimator 的 FID 达到 **22.6**，远优于 InterGen 的 56.6（Table 1）。消融实验表明，移除交互姿态锚定使 Inter-X 上 FID 从 5.0 升至 7.1，接触率显著下降（Table 2），验证了交互姿态先验的核心作用。在文本到交互合成（FID 1.82 vs. InterGen 2.87）和单姿态到交互合成（FID 27.8 vs. 无锚基线 40.0）任务上，本方法同样取得显著提升（Table 3, Table 4）。

**局限与展望**：当前方法聚焦短时交互片段，长序列生成时交互姿态先验作用减弱；未显式建模人际穿透，在亲密接触场景中可能出现穿透；缺乏场景上下文意识，可能与环境碰撞；交互姿态估计误差会传播至动画阶段。未来方向包括显式穿透建模、场景上下文整合、文本引入动画阶段以解决语义歧义，以及向多人交互扩展。



### 问题背景

生成逼真的人-人交互动态是计算机视觉与图形学中长期存在的挑战。与单人运动生成不同，双人交互涉及复杂的空间协调与时间同步：两个个体的姿态不仅需要各自自然，还必须在空间上紧密配合、在物理上产生可信的接触。这种双重约束使得交互运动生成远比单人运动困难。

现有的运动生成方法主要沿着两条路径发展。一类是基于文本到运动的扩散模型，如 **MDM**（Tevet et al., ICLR 2023），其在单人运动生成上取得了显著进展，但直接扩展到双人场景时往往无法显式建模人际交互关系。另一类工作则专门针对多人交互设计，例如 **ComMDM**（Liu et al., CVPR 2024）通过通信机制协调多人运动，**RIG**（Sun et al., ECCV 2024）关注反应感知的交互生成，**InterGen**（Liang et al., CVPR 2024）则利用扩散模型从文本直接合成双人运动。然而，这些方法在生成近距离、高接触的双人交互时，仍然难以同时保证运动的真实感和物理接触的准确性。

### 核心瓶颈

现有方法面临一个根本性的瓶颈：**在生成近距离双人交互时，难以同时保证运动真实感和物理接触，且无法有效将高质量动作捕捉数据中的交互先验迁移到开放域图像中**。

具体而言，动作捕捉数据集（如 Inter-X、Dual-Human）包含了大量高质量的近距离交互序列，其中蕴含着丰富的时空先验——两个人在接触瞬间的相对位置、朝向、关节对应关系等信息。然而，现有方法要么将这些先验隐式地编码在端到端模型中（导致泛化能力受限），要么完全依赖文本条件生成（缺乏精确的空间约束），均未能有效利用这些宝贵的先验知识。当输入从文本或单张图像出发时，模型缺乏足够的空间锚点来约束两人的相对关系，导致生成的运动出现穿透、接触不实或动作失真等问题。

### 核心洞察与动机

本文的核心洞察在于：**交互姿态蕴含着丰富的时空先验，能够作为桥梁连接姿态生成与运动动画**。如图 Figure 2 所示，交互姿态（即两人近距离接触时的静态姿态对）与非交互姿态有着本质区别——观察者可以从一个交互姿态中直观地推断出前后文的动态信息（如“推”的动作前后帧），而非交互姿态则缺乏这种时间暗示。这意味着交互姿态天然地编码了交互的“空间快照”，同时暗含了时间演化的约束。

基于这一洞察，Ponimator 提出将任务解耦为两个阶段：先利用**空间先验**生成交互姿态，再利用**时间先验**从交互姿态展开为完整运动序列。这种解耦使得模型只需少量条件（单姿态、文本或两者组合）即可在各种输入下生成逼真的双人交互动态，同时通过交互姿态这一中间锚点，自然保证了物理接触和运动真实感。训练数据则来自动作捕捉交互数据集中检测到的近距离双人姿态及其前后文运动片段，从而将高质量 MoCap 数据中的交互先验有效迁移到开放域应用中。



## 核心方法与创新机理

Ponimator 的核心创新在于**将交互姿态（Interactive Pose）作为连接静态姿态生成与动态运动动画的中间锚点**，从而将复杂的双人交互生成任务解耦为两个可控的子问题。这一设计直接回应了现有方法的瓶颈：在生成近距离双人交互时，难以同时保证运动真实感与物理接触，且无法有效将高质量动作捕捉数据中的交互先验迁移到开放域图像中。

### 关键洞察：交互姿态蕴含时空先验

本方法建立在“交互姿态蕴含着丰富的时空先验”这一洞察之上。具体而言，交互姿态被定义为两个体在近距离接触中的姿态（Figure 2）。与非交互姿态不同，交互姿态使观察者能够直观地推断前后文的运动时序——例如，从“两人握手”的姿态可以自然推演出“伸手—握住—松开”的动态过程。这一先验使得模型能够**以少量条件（单姿态、文本或两者组合）生成逼真的双人交互动态**。

基于此，Ponimator 将交互运动概率分解为两个先验的乘积（Eq. 1）：
$$p(\mathcal{X}, \beta) = p(\mathcal{X}; \mathbf{x}_I, \beta) \cdot p(\mathbf{x}_I, \beta)$$
其中 $p(\mathcal{X}; \mathbf{x}_I, \beta)$ 由姿态动画器（Pose Animator）建模，捕获时间先验；$p(\mathbf{x}_I, \beta)$ 由姿态生成器（Pose Generator）建模，捕获空间先验。二者以交互姿态 $\mathbf{x}_I$ 为桥梁协同工作。

### 相对于 Baseline 的关键设计变更（Changed Slots）

Ponimator 在扩散模型框架内引入了一系列针对交互姿态锚定的设计变更，这些变更是其性能优势的直接来源：

| 设计维度 | Baseline 做法 | Ponimator 做法 | 作用机制 |
|---------|-------------|--------------|---------|
| **去噪目标表示** | 绝对姿态序列 $\{x_i\}$ | 相对于交互姿态的残差 $\{x_i - x_I\}$ | 将生成目标转化为“从交互姿态出发的运动偏移”，降低学习难度，使模型聚焦于动态变化而非静态姿态 |
| **噪声注入策略** | 标准噪声添加 | 交互帧位置噪声置零（Imputation，Eq. 3） | 在扩散过程中保留交互姿态的空间结构信息，确保生成的运动始终以该姿态为锚点展开 |
| **交互时间条件** | 无时间索引 | One-hot 向量 $\mathbf{m}_I$ 编码交互时刻 | 显式告知模型交互姿态在序列中的时间位置，帮助模型建立“交互前—交互中—交互后”的时序结构 |
| **姿态条件编码** | 无显式编码 | 通过 FK 计算关节位置并用 MLP 嵌入注入 AdaIN | 将交互姿态的结构信息深度融入网络各层，而非仅作为输入特征 |
| **统一输入条件** | 单一条件 | 掩码 $\mathbf{m}_a$ 和 $\mathbf{m}_c$ 融合文本与单姿态条件（Eq. 4） | 使同一姿态生成器可灵活处理仅文本、仅单姿态、或两者组合的输入，实现多用途统一 |

### 消融实验验证

消融实验（Table 2）直接验证了上述设计的必要性：
- **移除交互姿态锚定**（w/o anchor）：Inter-X 上 FID 从 5.0 上升至 7.1，Dual-Human 上从 24.2 上升至 36.9，接触率显著下降
- **移除交互时间编码**（-time）或**关节条件编码**（-joints）：均导致性能明显退化
- **使用随机姿态替代交互姿态**（random-pose）：性能同样下降，证明交互姿态的先验信息不可替代
- **将 InterGen 直接适配为交互姿态输入**（InterGen\*）：因缺乏显式交互建模而表现不佳，进一步说明锚定机制的重要性

这些结果一致表明：**交互姿态锚定及其配套的条件编码机制是 Ponimator 性能优势的核心来源**，而非模型容量或训练策略的简单提升。



Ponimator 的核心设计是将双人交互运动生成解耦为两个阶段，以**交互姿态**作为中间桥梁。整体 pipeline 由两个条件扩散模型串联构成：**交互姿态生成器** 和 **交互姿态动画器**，分别利用空间先验和时间先验来完成从条件输入到动态运动的生成。

### 设计动机与概率分解

现有方法在生成近距离双人交互时，难以同时保证运动真实感和物理接触，且无法有效将高质量动作捕捉数据中的交互先验迁移到开放域图像中。Ponimator 的核心洞察在于：**交互姿态蕴含着丰富的时空先验**——观察者仅凭一帧紧密接触的双人姿态，就能直观推断出前后文的时间动态。

基于这一观察，方法将交互运动概率分解为两个先验的乘积：

$$p(\mathcal{X}, \beta) = p(\mathcal{X}; \mathbf{x}_I, \beta) \cdot p(\mathbf{x}_I, \beta)$$

其中 $\mathbf{x}_I$ 为交互姿态，$\beta$ 为两人体型参数。这一分解将任务解耦为：**姿态动画器**捕获给定交互姿态的时间先验 $p(\mathcal{X}; \mathbf{x}_I, \beta)$，**姿态生成器**捕获空间先验 $p(\mathbf{x}_I, \beta)$。

### 模块关系与数据流

整体 pipeline 包含以下模块，数据流向如 Figure 3 所示：

![[assets/figures/papers/paper_list_l1771_Ponimator_Unfolding_Interactive_Pose_for_Versatile_Human_human_Interacti/figures/003_Figure_3.jpg]]
*Figure 3: Frameworkoverview.Ponimatorconsistsofapose generatorandanimator,bridgedbyinteractiveposes.Theeneratortakes asingle pose,text,orbothasinputtoproduce interactive poses,whiletheanimatoruleashesinteractiondynamics fromstatic poses*

1. **交互姿态提取器**：从动作捕捉序列中，通过 SMPL-X 顶点距离阈值检测近距离双人交互姿态，构建训练所需的交互姿态-运动配对数据。

2. **交互姿态动画器**：以交互姿态 $\mathbf{x}_I$ 和两人体型 $\beta$ 为条件，生成前后文运动序列 $\mathcal{X}$。该模块将去噪目标定义为相对于交互姿态的运动残差 $\mathbf{z}_0 = \{\mathbf{x}_i - \mathbf{x}_I\}_{i=1}^N$，并通过插补策略在交互时刻的噪声输入中对应位置置零，保留交互姿态的空间结构。

3. **交互姿态生成器**：从单姿态、文本或两者组合中生成交互姿态 $\mathbf{x}_I$ 和体型 $\beta$。通过掩码 $\mathbf{m}_a$ 和 $\mathbf{m}_c$ 灵活控制文本和单姿态条件的引入，实现统一的姿态生成。

4. **CLIP 文本编码器**：编码文本条件，用于姿态生成阶段。

### 应用流水线

根据输入类型，框架支持三种应用模式：

- **双人图像动画**：使用现成模型从双人图像中估计交互姿态，直接送入动画器生成动态。
- **单人交互生成**：从单人图像估计姿态，经生成器产生交互姿态，再送入动画器。
- **文本到交互合成**：文本经 CLIP 编码后直接由生成器合成交互姿态，再驱动动画器。

这种解耦设计使得模型只需少量条件即可在各种输入下生成逼真的双人交互动态，且交互姿态作为锚点天然保证了物理接触。

### 补充图表

![[assets/figures/papers/paper_list_l1771_Ponimator_Unfolding_Interactive_Pose_for_Versatile_Human_human_Interacti/figures/014_Figure_10.jpg]]
*Figure 10: Diverse interactive motion generation. From a single pose,our framework generates varied interactive poses (magenta box)and motions (lst,2nd rows) and text-driven ones (3rd row)*



### 3.1 交互姿态的定义与概率分解

Ponimator 的核心洞察在于：**交互姿态（Interactive Pose）**——即两个个体在近距离接触下的静态姿态——蕴含着丰富的时空先验。观察者仅凭一帧交互姿态（如握手、拥抱），便能直觉性地推断出前后文的动态过程（Figure 2）。基于此，方法将双人交互运动 $\mathcal{X}$ 的生成概率显式地分解为两个条件概率的乘积：

![[assets/figures/papers/paper_list_l1771_Ponimator_Unfolding_Interactive_Pose_for_Versatile_Human_human_Interacti/figures/002_Figure_2.jpg]]
*Figure 2: Interactive poses refer to two-person poses in proximity and close contact. The top row displays interactive (green) and non-interactive (red) poses within one sequence. Interactive poses allow observers to intuitively infer the temporal context,while non-interactive poses are more ambiguous and difficult to interpret. The bottom row showcases common daily interactive poses*

$$p(\mathcal{X}, \beta) = p(\mathcal{X}; \mathbf{x}_I, \beta) \cdot p(\mathbf{x}_I, \beta)$$

其中：
- $\mathcal{X} = \{\mathbf{x}_i\}_{i=1}^N$ 表示长度为 $N$ 的双人运动序列，$\mathbf{x}_i$ 为第 $i$ 帧的绝对姿态；
- $\beta$ 为两人的体型参数；
- $\mathbf{x}_I$ 为从序列中提取的**交互姿态**，作为连接两个子任务的锚点。

这一分解将问题解耦为两个阶段：
- **$p(\mathcal{X}; \mathbf{x}_I, \beta)$**：由**交互姿态动画器（Interactive Pose Animator）**建模，捕获给定交互姿态和体型下的**时间先验**，负责从静态交互姿态生成前后文运动序列。
- **$p(\mathbf{x}_I, \beta)$**：由**交互姿态生成器（Interactive Pose Generator）**建模，捕获**空间先验**，负责从各种条件（单姿态、文本或两者组合）生成合理的交互姿态。

### 3.2 交互姿态动画器

动画器的目标是学习时间先验 $p(\mathcal{X}; \mathbf{x}_I, \beta)$：给定一帧交互姿态 $\mathbf{x}_I$ 和体型 $\beta$，生成完整的交互运动序列。其设计包含三个关键机制：

**（1）去噪目标重定义。** 不同于标准运动扩散模型直接预测绝对姿态序列，动画器的去噪目标 $\mathbf{z}_0$ 被定义为**相对于交互姿态的运动残差**：

$$\mathbf{z}_0 = \{\mathbf{x}_i - \mathbf{x}_I\}_{i=1}^N$$

这一设计使模型始终以交互姿态为参考锚点，强化了生成运动与交互帧之间的空间一致性。

**（2）插补式噪声注入策略。** 在扩散过程的前向加噪阶段，交互姿态对应帧位置的噪声被显式置零，以保留其空间结构信息：

$$\tilde{\mathbf{z}}_t = (1 - \mathbf{m}_I) \odot \mathbf{z}_t + \mathbf{m}_I \odot \mathbf{0}, \quad \mathbf{c} = (\mathbf{m}_I, \mathbf{x}_I, \beta)$$

其中 $\mathbf{m}_I$ 是一个 one-hot 向量，用于标记交互姿态在序列中的时间位置。条件 $\mathbf{c}$ 同时包含时间索引 $\mathbf{m}_I$、交互姿态 $\mathbf{x}_I$ 和体型 $\beta$。这一策略确保交互帧的原始姿态信息在去噪过程中不被破坏。

**（3）条件编码。** 交互姿态 $\mathbf{x}_I$ 首先通过前向运动学（FK）计算关节位置，随后经 MLP 嵌入后注入扩散模型的 AdaIN 层，为生成过程提供精细的空间引导。

训练采用标准扩散模型的均方误差损失：

$$\mathcal{L}_D = \mathbb{E}_{\mathbf{z}_0, \mathbf{c}, \epsilon \sim \mathcal{N}(0, \mathbf{I}), t} \left[ \| \mathbf{z}_0 - G(\mathbf{z}_t, t, \mathbf{c}) \|_2^2 \right]$$

### 3.3 交互姿态生成器

生成器建模空间先验 $p(\mathbf{x}_I, \beta)$，支持从多种条件生成交互姿态。其核心创新在于**统一条件掩码机制**：

$$\tilde{\mathbf{z}}_t = \big( (1 - \mathbf{m}_a) \odot \mathbf{z}_t^a + \mathbf{m}_a \odot \mathbf{z}_0^a,\ \mathbf{z}_t^b \big), \quad \tilde{\mathbf{c}} = \mathbf{m}_c \odot \mathbf{c}$$

其中：
- $\mathbf{z}_t^a$ 和 $\mathbf{z}_t^b$ 分别表示人物 A 和 B 的噪声姿态；
- $\mathbf{m}_a$ 为姿态条件掩码：当提供 A 的单人姿态作为条件时，$\mathbf{m}_a = 1$，此时 A 的姿态被固定为条件输入 $\mathbf{z}_0^a$；否则 $\mathbf{m}_a = 0$，A 的姿态从噪声中自由生成；
- $\mathbf{m}_c$ 为文本条件掩码：当提供文本条件时，$\mathbf{m}_c = 1$，文本嵌入通过 CLIP 编码后注入模型；否则 $\mathbf{m}_c = 0$。

通过灵活组合 $\mathbf{m}_a$ 和 $\mathbf{m}_c$，单一模型即可覆盖三种条件模式：纯文本（$\mathbf{m}_a = 0, \mathbf{m}_c = 1$）、纯单姿态（$\mathbf{m}_a = 1, \mathbf{m}_c = 0$）、以及文本+单姿态（$\mathbf{m}_a = 1, \mathbf{m}_c = 1$），实现了统一的交互姿态生成。



## 实验与关键发现

### 核心实验设置

Ponimator 的姿态动画器采用 8 层 Transformer（隐空间维度 1024），使用 AdamW 优化器（学习率 1e-4）训练。推理阶段使用 DDIM 采样 50 步，在 A100 上生成 3 秒、10 fps 的运动序列仅需 0.24 秒。交互姿态提取器通过 SMPLX 顶点距离阈值从动作捕捉序列中自动检测近距离双人交互姿态（详见 Sec 3.1 和附录 A）。评估指标涵盖运动质量（FID）、物理接触率（Contact Ratio）等。

### 无约束交互生成（主实验）

在 Inter-X 数据集上的无约束交互生成任务中，Ponimator 取得了 **FID 22.6** 和 **接触率 68.1** 的显著优势（Table 1）。相比端到端文本驱动方法 InterGen（Liang et al., CVPR 2024）的 FID 56.6，FID 降低了 **34.0**（降幅约 60%），接触率提升了 17.2 个百分点。这一结果直接验证了核心因果机制：以交互姿态作为中间锚点，能够将运动真实感和物理接触这两个长期难以兼顾的目标统一到一个框架中。其他基线方法如 MDM*（Tevet et al., ICLR 2023，改编自单人运动扩散模型）、ComMDM（Liu et al., CVPR 2024）和 RIG（Sun et al., ECCV 2024）在 FID 和接触率上均显著劣于 Ponimator，表明缺乏显式交互姿态先验的建模方式难以同时保证运动质量和物理接触。

![[assets/figures/papers/paper_list_l1771_Ponimator_Unfolding_Interactive_Pose_for_Versatile_Human_human_Interacti/figures/008_Table_1.jpg]]
*Table 1: Unconstrained interaction synthesis comparison on Inter-X [65] dataset.-→means the closer to ground truth the better the result.Method in * is adapted from ours for two-person interaction. Our method largely outperforms others in motion quality and contact ratio,naturally ensuring physical contact and motion realism by anchoring on interactive poses*

### 消融实验：交互姿态锚定的决定性作用

消融实验（Table 2）系统验证了交互姿态锚定及其条件编码的必要性：

![[assets/figures/papers/paper_list_l1771_Ponimator_Unfolding_Interactive_Pose_for_Versatile_Human_human_Interacti/figures/009_Table_2.jpg]]
*Table 2: Interactive pose animation comparison on Inter-X [65] and Dual-Human [7] dataset. InterGen* is adapted to take interactive poses input but lacks explicit interaction modeling,limiting its use of pose priors. Interactive pose anchoring,condition encoding, and interactive frames are crucial for the performance*

- **移除交互姿态锚定**（w/o anchor）：在 Inter-X 上 FID 从 5.0 上升至 7.1，Dual-Human 上从 24.2 上升至 36.9，接触率同步下降。这证明交互姿态蕴含的时空先验是运动生成质量的关键来源。
- **移除交互时间编码**（-time）或**关节条件编码**（-joints）：均导致性能明显下降，表明交互时刻的定位和关节空间的条件注入对姿态动画至关重要。
- **用随机姿态替代交互姿态**（random-pose）：同样导致性能退化，进一步证实交互姿态的先验信息不可被随机噪声替代。
- **将 InterGen 直接适配为交互姿态输入**（InterGen*）：表现不佳，因其缺乏显式的交互建模机制，无法有效利用姿态先验。

上述消融结果一致指向同一个结论：交互姿态锚定及其配套的条件编码策略（imputation 策略将交互帧噪声置零、残差去噪目标、时间索引编码、关节位置 FK 嵌入）共同构成了 Ponimator 性能的因果基础。

### 文本到交互与单姿态到交互合成

在文本到交互合成任务中（Table 3），Ponimator 的 FID 为 **1.82**，优于 InterGen 的 2.87，表明统一姿态生成器能够更有效地将文本语义映射为交互姿态空间先验。在单姿态到交互合成任务中（Table 4），Ponimator 的 FID 为 **27.8**，相比无锚定基线（w/o anchor）的 40.0 降低了 12.2，验证了交互姿态作为中间表示在条件稀疏场景下的桥接能力。

![[assets/figures/papers/paper_list_l1771_Ponimator_Unfolding_Interactive_Pose_for_Versatile_Human_human_Interacti/figures/010_Table_3.jpg]]
*Table 3: Text-to-interaction synthesis results on Inter-X [65] dataset. Our unified pipeline outperforms end-to-end w/o interactive pose as anchor method in short-term interaction synthesis*

![[assets/figures/papers/paper_list_l1771_Ponimator_Unfolding_Interactive_Pose_for_Versatile_Human_human_Interacti/figures/011_Table_4.jpg]]
*Table 4: Single pose-to-interaction synthesis results on Inter-X[65] dataset. Compared to without anchor baseline,our method uses interactive poses for more effective interaction modeling*

定性比较进一步支持定量结论：在文本“push”的生成对比中（Figure 8），Ponimator 比 InterGen 和端到端基线展现出更好的接触和更真实的动态；在单姿态到交互合成中（Figure 9），有锚定的模型生成的人-人交互更加自然。

![[assets/figures/papers/paper_list_l1771_Ponimator_Unfolding_Interactive_Pose_for_Versatile_Human_human_Interacti/figures/013_Figure_8.jpg]]
*Figure 8: Text-to-interaction comparison for "push".Anchored on interactive poses,our method achieves better contact and more realistic dynamics than InterGen [31] and the end-to-end baseline*

![[assets/figures/papers/paper_list_l1771_Ponimator_Unfolding_Interactive_Pose_for_Versatile_Human_human_Interacti/figures/012_Figure_9.jpg]]
*Figure 9: Single pose-to-interaction comparison on Inter-X dataset [65]. Compared to the model without interactive pose anchors,our method generates more natural human interactions*

### 跨数据集泛化与多人生成

Figure 7 展示了交互姿态动画器在域内数据集（Inter-X、Dual-Human）和域外数据集（Duolando、Hi4D、Interhuman）上的泛化能力，甚至可以直接应用于随机组合的多人姿态而无需修改或重新训练。这表明学习到的交互姿态先验具有通用性，能够跨越不同数据分布和人数规模。

![[assets/figures/papers/paper_list_l1771_Ponimator_Unfolding_Interactive_Pose_for_Versatile_Human_human_Interacti/figures/007_Figure_7.jpg]]
*Figure 7: Interactive pose animation on in-domain datasets (Inter-X[65],Dual-Human[7])，out-of-domaindataset (Duolando [53],Hi4D [7O]，Interhuman [31])，and random composed multi-person pose. Each row: left—interactive pose, right—animation sequence.Our learned interactive pose prior is universal,generalizing across datasets and enabling multi-person interactions (6th row) without modification or retraining*

### 失败模式与局限性

Figure 12 系统性揭示了方法的四类典型失败模式：

![[assets/figures/papers/paper_list_l1771_Ponimator_Unfolding_Interactive_Pose_for_Versatile_Human_human_Interacti/figures/016_Figure_12.jpg]]
*Figure 12: Methodimitationanalysis.Thefrsttworowssowin-the-wildinteractiveposeanimationresults.Ithefrstsample,evere interpenetrationoccursasourmethoddoesotexplicitlyodelpenetrationbetweentwoindividuals.Intesecond,tegeneratedotion is physicallyimplausibleuetthelackofscenecontextawareessleading tocolisions withteenvironent.Tebottomtworows ilustrate interactionmotiongenerationfromasinglepoeiput.Duetoinaccuracies ininteractivepose generation,ourmethodfailsto produce realistic contact, resulting in unnatural motion*

1. **人际穿透**：在亲密接触场景中，由于方法未显式建模人际穿透约束，可能出现身体部位相互穿透（第 1 行）。
2. **缺乏场景意识**：生成过程仅依赖人体姿态信息，忽略周围环境，可能导致与环境碰撞（第 2 行）。
3. **接触不准确**：当交互姿态估计器或生成器产生不准确姿态时，动画器无法补偿上游误差，导致生成的运动缺乏真实接触（第 3-4 行）。
4. **脚步滑动**：生成的运动可能存在脚步滑动等常见运动合成瑕疵，且未进行后处理。

此外，当前方法主要关注短时交互片段（3 秒），长序列生成时交互姿态先验的作用会逐渐减弱；文本语义歧义（如“举起”与“放下”的时序方向）也无法在姿态动画阶段被区分，因为动画器缺乏文本条件。

### 补充图表

![[assets/figures/papers/paper_list_l1771_Ponimator_Unfolding_Interactive_Pose_for_Versatile_Human_human_Interacti/figures/017_Figure_13.jpg]]
*Figure 13: Longer motion generation bychaining interactive poses.Wereuse the last generated pose as the next input,reseting interactive time to zero,enabling sliding-window synthesis of longer motions (key-frame in magenta box)*



## 定位与知识库关联

### 核心瓶颈与设计动机

人-人交互运动生成面临一个根本性张力：现有方法在生成近距离双人交互时，难以同时保证运动真实感和物理接触，且无法有效将高质量动作捕捉数据中的交互先验迁移到开放域图像中。扩散模型虽在单人运动生成上取得了显著进展，但直接扩展到双人交互时，往往产生漂浮、穿透或接触缺失等不自然现象。Ponimator 的因果调节变量在于：**以交互姿态作为中间锚点，并将任务解耦为基于空间先验的姿态生成和基于时间先验的运动动画两个阶段**。这一设计的核心洞察是：交互姿态蕴含着丰富的时空先验——观察者仅凭一帧近距离接触的双人姿态，就能直观推断前后文的运动动态——因此可以作为桥梁，连接条件输入与动态输出。

### 与现有工作的关系

**扩散运动生成基准。** **MDM** (Tevet et al., ICLR 2023) 是单人运动扩散模型的代表性工作，Ponimator 将其适配为双人交互基线（MDM*），但在无约束交互生成任务中表现有限。**ComMDM** (Liu et al., CVPR 2024) 引入通信机制处理多人运动，**RIG** (Sun et al., ECCV 2024) 关注反应感知的交互生成，两者均未显式利用交互姿态作为结构化先验。

**双人交互生成。** **InterGen** (Liang et al., CVPR 2024) 是端到端的文本到双人运动扩散模型，在 Inter-X 数据集上无约束交互生成的 FID 为 56.6，而 Ponimator 在同一基准上达到 22.6（Table 1），降幅达 60%。这一差距的根源在于：InterGen 缺乏对交互姿态的显式建模，其生成的运动在接触率和真实感上均明显不足。当将 InterGen 修改为以交互姿态作为输入（InterGen*）时，其表现仍然不佳（Table 2），进一步验证了仅靠条件替换无法弥补显式交互建模的缺失。

**条件运动生成谱系中的定位。** Ponimator 的独特贡献在于将交互运动生成问题分解为两个条件扩散模型的级联，这与端到端的条件生成范式形成对比。在文本到交互合成任务中，Ponimator 的 FID 为 1.82，优于 InterGen 的 2.87（Table 3）；在单姿态到交互合成中，FID 为 27.8，显著优于无锚定基线（w/o anchor）的 40.0（Table 4）。这一优势源于交互姿态作为中间表示，有效压缩了条件到运动的映射难度。

### 关键设计决策与消融证据

Ponimator 的方法栈包含五个关键设计槽位，每个均经过消融验证：

1. **去噪目标表示**：将绝对姿态序列 $\{x_i\}$ 改为相对于交互姿态的残差 $\{x_i - x_I\}$，使模型专注于学习运动动态而非绝对位置。消融实验（Table 2）中，移除交互姿态锚定（w/o anchor）使 Inter-X 上的 FID 从 5.0 升至 7.1，Dual-Human 上从 24.2 升至 36.9，接触率同步下降。

2. **扩散噪声注入策略**：在交互帧位置采用插补策略（imputation strategy，Eq. (3)），将噪声输入中对应位置置零，保留交互姿态的空间结构。这一设计确保了去噪过程始终以交互姿态为条件锚点。

3. **交互时间条件**：引入 one-hot 向量 $\mathbf{m}_I$ 表示交互时刻，使模型明确知晓哪一帧是交互姿态。移除该编码（-time）导致性能下降（Table 2）。

4. **姿态条件编码**：通过前向运动学计算关节位置并用 MLP 嵌入注入 AdaIN 层。移除关节条件编码（-joints）同样导致性能退化（Table 2）。

5. **统一输入条件**：在姿态生成器中，使用掩码 $\mathbf{m}_a$ 和 $\mathbf{m}_c$ 融合文本与单姿态条件（Eq. (4)），实现单一模型处理多种条件组合。

此外，使用随机姿态代替交互姿态（random-pose）的实验（Table 2）表明，即使保留相同的网络结构，非交互姿态无法提供有效的时空先验，性能显著下降，证明交互姿态的先验信息不可替代。

### 适用边界与局限性

**短时建模约束。** 当前方法主要关注短时交互片段（约 3 秒），长序列生成时交互姿态先验的作用会逐渐减弱。虽然可通过滑动窗口拼接交互姿态实现更长运动（Figure 13），但文本到交互合成可能只生成部分动作，缺乏完整的长程语义控制。

**人际穿透问题。** 方法未显式建模人际穿透，在亲密接触场景中可能出现穿透现象（Figure 12 第 1 行）。这是当前框架的结构性局限——扩散模型学习的是运动分布，而非物理约束。

**场景上下文缺失。** 生成过程仅依赖人体姿态信息，忽略周围环境，可能导致与环境碰撞或物理不合理的结果（Figure 12 第 2 行）。这限制了方法在开放域场景中的鲁棒性。

**误差传播链。** 当交互姿态估计器（用于两人图像）或生成器（用于单人/文本输入）产生不准确姿态时，动画器无法补偿上游错误，导致生成的运动不真实（Figure 12 第 3-4 行）。这一级联误差问题是两阶段架构的固有风险。

**语义歧义与脚步滑动。** 姿态动画器缺乏文本条件，无法区分"举起"和"放下"等方向性语义。此外，生成的运动可能存在脚步滑动等常见运动合成瑕疵，且未进行后处理。

### 开放问题与后续方向

1. **物理约束的显式建模**：如何在保证运动自然性的前提下，引入穿透检测与惩罚机制，或通过物理模拟后处理修正接触误差？
2. **场景感知扩展**：如何将场景上下文（如图像特征、环境几何）整合到扩散模型中，以避免碰撞并提升物理合理性？这可能需要额外的条件编码分支或跨模态注意力机制。
3. **长程语义控制**：如何将文本条件引入姿态动画阶段，以解决语义歧义并生成更符合文本描述的长程交互？这涉及对现有框架中条件流的重新设计。
4. **上游精度提升**：如何进一步提升交互姿态估计和生成的准确性，以减轻动画阶段的误差传播？这可能涉及更强的姿态先验或迭代优化策略。
5. **多人扩展**：框架是否可以在不重新训练的情况下扩展到三人或多人交互？Figure 7 第 6 行展示了初步的多人组合实验，但系统性验证和性能评估仍是开放问题。



## 原文 PDF

![[paperPDFs/ICCV_2025/Ponimator_Unfolding_Interactive_Pose_for_Versatile_Human_human_Interaction_Animation.pdf]]
