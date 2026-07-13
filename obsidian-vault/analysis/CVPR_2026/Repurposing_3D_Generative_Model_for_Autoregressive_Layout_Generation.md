---
title: Repurposing 3D Generative Model for Autoregressive Layout Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Repurposing_3D_Generative_Model_for_Autoregressive_Layout_Generation.pdf
project_link: "https://fenghora.github.io/LaviGen-Page/"
code_link: "https://github.com/fenghora/LaviGen"
aliases:
- R3GMALG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 利用预训练3D生成模型的几何先验，在原生3D体素空间执行自回归扩散过程，通过身份感知嵌入区分场景与物体，并以自推演双重引导蒸馏消除曝光偏差，从而准确建模空间配置。
primary_logic: 将3D生成模型重新用于自回归布局生成：直接继承其内部的空间关系先验，在连续的3D空间中逐次放置物体，确保物理一致性和语义连贯性，同时天然支持编辑与补全。
claims:
- 逐步引入身份感知嵌入、整体引导和步骤引导后，物理合理性（Collision-Free）从75.6提升至97.3，边界内率（In-Boundary）从64.8提升至98.6。
- 定性结果表明，完整模型有效消除了基线中常见的物体碰撞和悬空伪影。
- 用户研究表明，LaviGen在物理合理性和整体质量上显著优于LayoutGPT和LayoutVLM。
- LayoutVLM Benchmark 上 Collision-Free (CF) = 97.3
---

# Repurposing 3D Generative Model for Autoregressive Layout Generation

> [!tip] 核心洞察
> 将3D生成模型重新用于自回归布局生成：直接继承其内部的空间关系先验，在连续的3D空间中逐次放置物体，确保物理一致性和语义连贯性，同时天然支持编辑与补全。

| 字段 | 内容 |
|------|------|
| 中文题名 | 将3D生成模型重新用于自回归布局生成 |
| 英文题名 | Repurposing 3D Generative Model for Autoregressive Layout Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.16299) · [Project](https://fenghora.github.io/LaviGen-Page/) · [Code](https://github.com/fenghora/LaviGen) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | LaviGen |
| Dataset | LayoutVLM Benchmark |

> [!tip] 效果简介
> - LayoutVLM Benchmark 上，Collision-Free (CF) 97.3 vs 83.8 (LayoutGPT) / 81.8 (LayoutVLM) (+15.5 (vs LayoutGPT))；In-Boundary (IB) 98.6 vs 94.9 (LayoutVLM) (+3.7)；Physically-Grounded Semantic Alignment (PSA) 78.8 vs 58.8 (LayoutVLM) (+20.0)。
> - 用户研究 上，物理合理性偏好率 52.1% vs 31.9% (LayoutVLM) (+20.2%)。

## 概要

3D 布局生成是构建沉浸式虚拟环境的核心任务，要求同时满足物理合理性（无碰撞、不悬空、在边界内）与语义连贯性（物体间的空间关系符合常识）。现有方法将布局表示为 JSON 序列化的边界框，依赖大语言模型（LLM）进行文本生成，或将布局投影到 2D 图像空间进行视觉优化。这些范式在原生 3D 空间中无法精确建模物体间的几何关系与物理约束，导致碰撞、穿透和悬空等伪影严重，成为领域的关键瓶颈。

**LaviGen** 提出了一条根本不同的技术路线：**将 3D 生成模型重新用于自回归布局生成**。其核心洞察在于，预训练的 3D 生成模型（如 TRELLIS）内部已蕴含丰富的空间关系先验——直接继承这一先验，在连续的 3D 体素空间中逐次放置物体，可以从机理上保证物理一致性和语义连贯性，同时天然支持编辑与补全。

具体而言，LaviGen 将布局生成形式化为自回归 3D 扩散过程：以 LLM 编码的布局指令为条件，逐步将物体加入场景，每一步均由自适应 3D 扩散模型在原生体素潜空间中预测更新后的场景状态。为区分场景、物体和噪声潜码的来源并保持空间对齐，模型引入了**身份感知的 RoPE 位置嵌入**；为消除自回归生成中固有的曝光偏差（训练依赖真值上下文，推理依赖自生成上下文），模型采用**自推演双重引导蒸馏**——由场景级整体教师和逐级步骤教师联合提供监督，使推理时的自推演分布与训练分布对齐。

在 LayoutVLM Benchmark 上的定量结果表明，LaviGen 的**无碰撞率（Collision-Free）达到 97.3%**，较 LayoutGPT 提升 15.5 个百分点，较 LayoutVLM 提升 15.5 个百分点；**边界内率（In-Boundary）达到 98.6%**；**物理接地的语义对齐（PSA）达到 78.8%**，较 LayoutVLM 提升 20.0 个百分点。同时，**平均推理时间仅 24.3 秒**，相比 LayoutVLM 的 75.5 秒缩短约 68%。用户研究进一步确认，LaviGen 在物理合理性上获得了 52.1% 的偏好率，显著领先于 LayoutVLM（31.9%）和 LayoutGPT（16.0%）。

消融实验揭示了各组件的递进贡献：基础 3D 生成模型直接用于布局生成时，无碰撞率仅 75.6%；加入身份感知嵌入后提升至 89.1%，但曝光偏差仍导致物体间碰撞；仅使用整体引导蒸馏虽可大幅加速推理，却使物体拟合精度下降；完整模型结合步骤引导后，物理合理性和语义连贯性达到最优（无碰撞率 97.3%，边界内率 98.6%），同时保持快速推理。定性消融图（Figure 7）直观展示了从杂乱碰撞到物理合理的渐进改善过程。

在方法谱系中，LaviGen 与现有工作的关键差异体现在四个维度：

| 维度 | 现有方法 | LaviGen |
|------|---------|---------|
| 布局表示 | JSON 序列化边界框 / 2D 渲染图像 | 3D 体素占用潜变量（结构化潜编码） |
| 生成范式 | LLM 文本生成 / 基于 2D 视觉的优化 | 自回归 3D 扩散模型（Flow Matching）原生空间建模 |
| 训练策略 | Teacher Forcing（依赖真值上下文） | Self-Rollout + 双重引导蒸馏 |
| 位置编码 | 无身份区分 | 身份感知 RoPE（区分场景/物体潜码） |

LaviGen 的局限在于：语义一致性（PSA 78.8%）仍逊于物理合理性，复杂空间关系时语义对齐不足；当前体素分辨率有限，更高分辨率会显著增加计算成本；物体的细粒度几何拟合依赖 ICP 后处理，可能引入额外误差。开放问题包括：如何在可控开销下提高体素分辨率、如何增强文本条件机制以改善语义对齐、能否扩展到开放世界的零样本布局生成，以及自推演蒸馏的动力学能否进一步压缩推理步数至实时交互水平。

### 3D布局生成的核心瓶颈

3D布局生成的任务是给定一组3D物体和自然语言指令，在连续三维空间中推理出每个物体的位置、朝向和尺度，使得最终场景既满足物理约束（无碰撞、不悬空、不穿模），又符合语义期望（物体间的功能关系与空间逻辑合理）。这一能力是室内设计自动化、具身智能仿真和交互式3D内容创作的关键基础。

然而，现有方法在解决该问题时面临一个根本性困境：**它们不在原生3D空间中建模几何关系**。主流路线可分为两类：

- **语言序列化路线**（如 **LayoutGPT**、**Holodeck**、**I-Design**）：将3D布局表示为JSON格式的边界框序列，交由大语言模型以文本生成方式逐物体预测坐标。这类方法完全丧失了3D空间的结构化归纳偏置，无法显式建模物体间的碰撞、支撑和遮挡等物理约束，导致生成的布局中物体碰撞和悬空伪影严重。
- **2D视觉优化路线**（如 **LayoutVLM**）：将3D场景渲染为2D图像，借助视觉语言模型进行可微分优化。该方法依赖2D投影的间接监督，丢失了深度维度的精确几何信息，且优化过程计算开销巨大（LayoutVLM平均推理时间达75.5秒），难以扩展到复杂场景。

这两类方法的共同缺陷在于**缺乏对3D空间几何先验的直接利用**——它们将布局生成视为语言序列或2D图像问题，而非本质上的3D空间配置问题。

### 预训练3D生成模型的未利用潜力

与此同时，3D生成领域取得了显著进展。以 **TRELLIS** 为代表的3D生成模型在海量3D资产上预训练，其内部潜空间已经编码了丰富的空间关系先验：物体部件间的对称性、相邻表面的接触模式、典型场景中物体的共现布局等。这些先验天然适用于布局生成任务——因为布局本质上就是对多物体空间配置的生成。

但直接将3D生成模型用于布局生成面临两个技术障碍：
1. **身份混淆**：标准3D生成模型处理的是单一物体的内部结构，而布局生成需要同时处理场景上下文和待放置物体，模型必须区分“已存在的场景”和“即将加入的物体”两种不同语义的身份。
2. **曝光偏差**：自回归生成过程中，若训练时依赖真值上下文（Teacher Forcing），而推理时只能使用模型自身生成的历史状态，训练-推理不一致会导致误差累积，使生成质量随序列增长而急剧恶化。

### 本文动机

基于以上分析，本文的核心动机是：**将预训练3D生成模型重新用于自回归布局生成**，使其直接在原生3D体素空间中逐次放置物体，从根本上解决物理约束建模不足的问题。具体而言，本文提出 **LaviGen** 框架，通过三个关键设计填补上述缺口：

1. **身份感知嵌入**：为场景潜码和物体潜码分配不同的身份标志，使扩散模型在去噪过程中明确区分二者的空间角色。
2. **自回归扩散范式**：将布局生成形式化为条件流匹配过程，每步以当前场景状态和待放置物体为条件，预测更新后的场景占用。
3. **自推演双重引导蒸馏**：训练阶段执行自回归推演，由场景级整体教师和逐级步骤教师联合提供监督信号，消除曝光偏差。

通过这一框架，LaviGen 旨在实现物理合理、语义连贯且推理高效的3D布局生成，同时天然支持布局编辑、补全和长序列扩展等下游任务。

## 核心方法与创新机理

LaviGen的核心创新在于**将3D生成模型重新用于自回归布局生成**，直接在原生3D体素空间建模物体间的几何关系与物理约束，从根本上区别于现有方法将布局视为文本序列或依赖2D图像监督的范式。这一创新通过四个关键的“changed slots”实现：

### 1. 布局表示：从JSON序列化到3D体素占用潜变量

现有方法（如**LayoutGPT**、**LayoutVLM**）将布局表示为JSON格式的边界框序列或2D渲染图像，丢失了物体在3D空间中的精确几何信息。LaviGen采用**结构化3D潜表示** $\mathcal{Z} = \{ z_p \mid p \in \mathcal{P} \}$，将每个3D资产编码为一组体素索引的局部潜码，在TRELLIS的结构级生成阶段预测稀疏体素占用，直接建模物体的空间组织关系（Sec. 3.1–3.2）。这一表示使得模型能够感知物体间的碰撞、穿透和悬空等物理约束，而这是文本或2D表示无法捕捉的。

### 2. 生成范式：从LLM文本生成到自回归3D扩散模型

现有方法依赖LLM的文本生成能力（如LayoutGPT的JSON输出）或基于2D视觉的可微分优化（如LayoutVLM），无法在原生3D空间进行空间推理。LaviGen将布局生成形式化为**自回归过程**：以LLM编码的布局指令为条件 $c$，接收当前场景状态 $S_i$ 和目标物体 $O_i$，通过自适应3D扩散模型生成更新后的场景状态 $S_{i+1}$（Sec. 3.2–3.3）。该扩散模型基于流匹配（Flow Matching）框架，训练目标为：

$$\mathcal{L} = \mathbb{E}_{t, x_0, s, o, c, \epsilon} \left\| v_{\theta}(x, s, o, c, t) - (\epsilon - x_0) \right\|_2^2$$

模型直接继承预训练3D生成模型的几何先验，在连续的3D空间中逐次放置物体，天然支持编辑与补全。

### 3. 训练策略：从Teacher Forcing到自推演双重引导蒸馏

传统自回归模型训练采用**Teacher Forcing**（$S_i^{\theta} = G_{\theta}(S_{i-1}, O_i, c)$），依赖真值历史状态，导致训练-推理不一致的曝光偏差（exposure bias）。LaviGen提出**Self-Rollout + 双重引导蒸馏**的后训练策略（Sec. 3.4），在训练时使用自生成的历史状态 $S_i^{\theta} = G_{\theta}(S_{i-1}^{\theta}, O_i, c)$ 进行推演，并由两个教师模型提供联合监督：

- **场景级整体教师**：提供全局空间配置的校正信号
- **逐级步骤教师**：提供物体级别的精确拟合指导

学生模型通过分数蒸馏梯度更新：

$$\nabla_{\theta} \mathcal{L}_{dual} \approx \mathbb{E}_{x_t, t} [ (s_{\mathcal{T}}(x_t, t) - s_{\psi}(x_t, t)) \nabla_{\theta} x_0 ]$$

这一策略消除了曝光偏差，同时保持了快速推理（平均24.3秒，较LayoutVLM的75.5秒减少67.8%）。

### 4. 位置编码：从无身份区分到身份感知RoPE

LaviGen引入**身份感知旋转位置编码**（Identity-Aware RoPE），通过身份标志 $f$ 区分不同来源的潜码（$f=0$ 为场景/噪声，$f=1$ 为物体）：

$$\Phi(f, h, w, l) = [ \phi_f(f); \phi_h(h); \phi_w(w); \phi_l(l) ]$$

该设计使模型在保持空间对齐的同时精确区分场景与物体的语义，实现语义解耦与几何一致性推理（Sec. 3.3）。

### 消融验证

Table 1的消融实验（Figure 7定性展示）逐步验证了各组件的贡献：
- 基础3D生成模型：碰撞严重（CF仅75.6）
- +身份感知嵌入：分布更合理但仍存碰撞（CF 89.1）
- +整体引导蒸馏：推理加速但物体拟合精度下降（CF 79.5）
- +步骤引导（完整模型）：物理合理性最优（CF 97.3，IB 98.6），且保持快速推理

这证明LaviGen的核心创新并非单一技术点的改进，而是**表示-范式-训练-编码**四个维度的协同重构，使3D布局生成首次在原生3D空间中实现物理一致性与语义连贯性的统一。

LaviGen 将 3D 布局生成重新定义为一个**自回归过程**：给定 LLM 编码的布局指令 $c$，模型以当前场景状态 $S_i$ 和待放置物体 $O_i$ 为条件，生成更新后的场景状态 $S_{i+1}$。这一过程在原生 3D 体素空间中逐次进行，直接继承预训练 3D 生成模型的几何先验，从根本上区别于将布局视为文本序列或依赖 2D 视觉优化的现有方法（Figure 2）。

![[assets/figures/papers/paper_list_l2580_https_arxiv_org_abs_2604_16299/figures/002_Figure_2.jpg]]
*Figure 2: Our layout generation pipeline versus existing methods that treat layouts as language or rely on vision-based optimization*

整体流水线如 Figure 3 所示，由以下核心模块串联构成：

![[assets/figures/papers/paper_list_l2580_https_arxiv_org_abs_2604_16299/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the LaviGen framework for autoregressive 3D layout generation. (a) LaviGen formulates layout generation as an autoregressive process. Specifically, conditioned on LLM-encoded instructions, it takes the current scene state Si and object Oi to generate the updated state*

**文本编码器**。布局指令（如“在房间左侧放置一张床，右侧放置一张书桌”）通过 **Qwen2.5-VL-7B-Instruct** 编码为条件向量 $c$，为后续扩散过程提供语义引导。

**结构与物体编码**。当前场景状态 $S_i$ 和目标物体 $O_i$ 分别被编码为结构化潜变量 $s$ 和 $o$。LaviGen 仅保留预训练 3D 生成模型（TRELLIS）的**结构级生成阶段**，预测稀疏体素占用以建模物体的空间组织，而非生成完整的高分辨率几何细节。

**身份感知位置嵌入**。为区分来自场景、物体和噪声的不同潜码流，模型引入身份感知的 RoPE 编码：
$$
\Phi(f, h, w, l) = [ \phi_f(f); \phi_h(h); \phi_w(w); \phi_l(l) ]
$$
其中 $f=0$ 标识场景/噪声潜码，$f=1$ 标识物体潜码。这一设计使模型在区分不同语义来源的同时保持空间对齐，实现精确的语义解耦和几何一致推理。

**自适应 3D 扩散模型**（Figure 4）。编码后的场景状态 $s$、物体 $o$ 与噪声潜变量 $x$ 沿空间维度拼接，连同身份感知嵌入一并送入多模态 DiT（Diffusion Transformer），进行噪声预测。训练目标为标准流匹配损失的条件扩展：
$$
\mathcal{L} = \mathbb{E}_{t, x_0, s, o, c, \epsilon} \left\| v_{\theta}(x, s, o, c, t) - (\epsilon - x_0) \right\|_2^2
$$
去噪输出经解码得到更新后的场景状态 $S_{i+1}$。

**自推演双重引导蒸馏**。标准 Teacher Forcing 训练（$S_i^{\theta} = G_{\theta}(S_{i-1}, O_i, c)$）依赖真值历史状态，导致训练-推理不一致的**曝光偏差**。LaviGen 在训练阶段执行自推演（$S_i^{\theta} = G_{\theta}(S_{i-1}^{\theta}, O_i, c)$），以自生成的历史状态替代真值上下文，并由场景级整体教师和逐级步骤教师提供联合监督，通过梯度更新对齐学生模型：
$$
\nabla_{\theta} \mathcal{L}_{dual} \approx \mathbb{E}_{x_t, t} [ (s_{\mathcal{T}}(x_t, t) - s_{\psi}(x_t, t)) \nabla_{\theta} x_0 ]
$$
整体教师和步骤教师分别在场景级和物体级提供互补的校正信号，共同消除曝光偏差。

**体素解码与 ICP 注册**。扩散生成的更新场景状态 $S_{i+1}$ 经体素解码器重建为高分辨率体素占用，随后通过迭代最近点（ICP）算法拟合各物体的空间参数（位置、朝向、尺度），得到最终的 3D 布局。

整个框架天然支持**布局编辑**：物体插入和删除均可通过修改自回归序列中的物体列表实现，模型在原生 3D 空间中执行上下文感知的空间一致性修改（Figure 6），无需额外训练或架构调整。

LaviGen 的核心设计在于将预训练 3D 生成模型改造为自回归布局扩散器，使其在原生 3D 体素空间中逐次放置物体。以下按流水线顺序拆解关键模块及其数学形式。

### 结构化 3D 潜表示

LaviGen 继承 TRELLIS 的结构级生成阶段，仅保留稀疏体素占用预测能力。每个 3D 资产被表示为一组由体素索引的局部潜码：

$$\mathcal{Z} = \{ z_p \mid p \in \mathcal{P} \}$$

其中 $\mathcal{P}$ 为体素网格中的有效位置集合，$z_p$ 为位置 $p$ 处的潜向量。这一表示将物体的空间占用编码为连续的潜变量，使扩散模型能够直接操作 3D 几何信息，而非文本序列或 2D 投影。

基础扩散模型采用流匹配（Flow Matching）范式，其标准损失函数为：

$$\mathcal{L} = \mathbb{E}_{t, x_0, \epsilon} \left\| v_{\theta}(x, t) - (\epsilon - x_0) \right\|_2^2$$

其中 $x_0$ 为目标潜码，$\epsilon$ 为噪声样本，$v_{\theta}$ 为学习的时间依赖向量场。该损失驱动模型学习从噪声到目标分布的确定性传输路径。

### 自适应 3D 扩散模型

LaviGen 将上述无条件生成模型改造为条件自回归布局扩散器（见 Figure 4）。给定布局指令，文本编码器（Qwen2.5-VL-7B-Instruct）将其编码为条件向量 $c$；当前场景状态 $S_i$ 和目标物体 $O_i$ 分别编码为潜变量 $s$ 和 $o$，与噪声潜码 $x$ 拼接后送入多模态扩散 Transformer。训练目标扩展为：

![[assets/figures/papers/paper_list_l2580_https_arxiv_org_abs_2604_16299/figures/004_Figure_4.jpg]]
*Figure 4: The overview of the adapted 3D diffusion model. The encoded scene state and object are concatenated with the noisy latent and, together with the identity-aware embedding, fed into the multimodal diffusion transformer for noise prediction. The denoised output is then decoded to produce the updated scene state*

$$\mathcal{L} = \mathbb{E}_{t, x_0, s, o, c, \epsilon} \left\| v_{\theta}(x, s, o, c, t) - (\epsilon - x_0) \right\|_2^2$$

该公式的核心变量含义：
- $x$：带噪声的潜码，是扩散过程的当前状态；
- $s$：当前场景的编码潜变量，携带已放置物体的空间信息；
- $o$：待放置目标物体的编码潜变量；
- $c$：文本指令的条件向量；
- $t$：扩散时间步；
- $\epsilon - x_0$：流匹配的目标向量场方向，从噪声指向干净数据。

### 身份感知位置嵌入

为区分场景潜码、物体潜码和噪声潜码的不同语义来源，同时保持它们在 3D 空间中的对齐关系，LaviGen 引入身份感知的旋转位置编码（RoPE）。其频率计算为：

$$\Phi(f, h, w, l) = [ \phi_f(f); \phi_h(h); \phi_w(w); \phi_l(l) ]$$

其中 $(h, w, l)$ 为体素的 3D 空间坐标，$f$ 为身份标志——$f=0$ 表示场景或噪声潜码，$f=1$ 表示物体潜码。通过将身份信息嵌入位置编码，模型能够在拼接后的潜码序列中精确区分各来源，实现语义解耦和几何一致性推理。

### 自推演与双重引导蒸馏

标准自回归训练采用 Teacher Forcing，即以真值历史状态 $S_{i-1}$ 为条件生成当前状态：

$$S_i^{\theta} = G_{\theta}(S_{i-1}, O_i, c)$$

这导致训练-推理不一致：推理时模型只能依赖自生成的历史 $S_{i-1}^{\theta}$，误差逐步累积形成曝光偏差。

LaviGen 通过自推演（Self-Rollout）打破这一偏差，训练时以模型自身生成的前序状态为条件：

$$S_i^{\theta} = G_{\theta}(S_{i-1}^{\theta}, O_i, c)$$

在此基础上，双重引导蒸馏进一步提供监督信号。整体教师（Holistic Teacher）以完整场景为条件提供全局布局指导，步骤教师（Step-wise Teacher）针对每一步的物体放置提供精细化校正。学生模型通过分数蒸馏更新参数，梯度近似为：

$$\nabla_{\theta} \mathcal{L}_{dual} \approx \mathbb{E}_{x_t, t} \left[ (s_{\mathcal{T}}(x_t, t) - s_{\psi}(x_t, t)) \nabla_{\theta} x_0 \right]$$

其中 $s_{\mathcal{T}}$ 为教师模型的分数函数（整体与步骤教师的联合信号），$s_{\psi}$ 为学生模型的分数函数，二者之差构成校正方向，驱动学生模型在自推演条件下仍能生成物理合理且语义连贯的布局。

## 实验与关键发现

### 主定量对比

LaviGen在LayoutVLM基准上全面超越现有方法。Table 1上半部分报告了四项核心指标的对比结果。在物理合理性方面，LaviGen的无碰撞率（Collision-Free, CF）达到**97.3**，相较LayoutGPT（83.8）和LayoutVLM（81.8）分别提升**+15.5**和**+15.5**个百分点；边界内率（In-Boundary, IB）达到**98.6**，优于LayoutVLM的94.9（+3.7）。这两项指标的大幅领先直接验证了原生3D空间建模对几何约束处理的根本优势——基于文本序列或2D视觉优化的方法无法精确建模物体间的空间关系，导致碰撞和越界问题频发。

在物理锚定的语义对齐（PSA）上，LaviGen取得**78.8**，较LayoutVLM的58.8提升**+20.0**，表明其生成的布局不仅物理合理，且物体间的空间配置与文本指令的语义意图更为一致。推理效率方面，LaviGen平均推理时间仅**24.3秒**，相比LayoutVLM的75.5秒降低**67.8%**。这一速度优势源于自回归扩散过程无需外部优化循环，而LayoutVLM依赖可微分优化迭代，计算开销显著更高。

> **Table 1** 上部为与LayoutGPT、Holodeck、I-Design、LayoutVLM等基线的定量对比，下部为逐组件消融结果。

![[assets/figures/papers/paper_list_l2580_https_arxiv_org_abs_2604_16299/figures/007_Table_1.jpg]]
*Table 1: Main quantitative comparison and ablation study. The top section compares LaviGen against state-of-the-art baselines. The bottom section ablates the key components of our model, validating their progressive contributions to the final performance*

### 用户研究

Table 2报告了用户偏好研究。在物理合理性维度上，**52.1%**的参与者偏好LaviGen的生成结果，显著高于LayoutVLM的31.9%（+20.2%）；在整体质量上，LaviGen同样以**49.6%**领先LayoutVLM的33.6%（+16.0%）。这表明人类评估者对原生3D空间建模带来的物理一致性改善高度敏感，与自动指标的结论相互印证。

> **Table 2** 为用户研究结果，展示物理合理性与整体质量两个维度的偏好率。

### 消融实验

Table 1下半部分的消融实验揭示了各组件的因果贡献，验证了“瓶颈→组件→效果”的完整链条：

**基础模型（Base Model）**：仅使用预训练3D生成模型进行自回归生成，不添加任何适配组件。其CF仅为**75.6**，IB仅为**64.8**，生成布局杂乱、碰撞严重。这暴露了核心瓶颈：通用3D生成模型虽具备空间先验，但缺乏对多物体场景中身份区分和序列依赖的建模能力，直接应用无法解决布局问题。

**+身份感知嵌入（+ id-aware emb.）**：引入区分场景/物体的RoPE位置编码后，CF提升至**89.1**（+13.5），IB提升至**97.0**（+32.2）。该组件使模型能够分辨不同来源的潜码，布局一致性显著改善。然而，此时仍采用Teacher Forcing训练，模型在推理时依赖真值历史上下文，一旦暴露于自生成状态，曝光偏差导致物体间碰撞依然存在。

**+整体引导蒸馏（+ L_holistic.）**：仅使用场景级整体教师进行蒸馏，推理速度大幅提升，但CF反而下降至**79.5**，PSA降至**65.8**。Figure 7的定性消融图显示，该配置下物体拟合精度下降，尤其是小物体的旋转预测出现严重反转错误。这表明整体引导虽能加速推理，但缺乏逐步骤的细粒度校正信号，无法保证单物体级的拟合质量。

**完整模型（+ L_step.，即LaviGen）**：同时引入步骤引导蒸馏后，CF跃升至**97.3**（+17.8 vs. 仅整体引导），IB达到**98.6**，PSA达到**78.8**。Figure 7的定性结果清晰展示了从基础模型到完整模型的渐进式改善：基础模型布局混乱、碰撞严重；添加身份嵌入后分布更合理但仍有碰撞；仅整体引导时物体拟合不准；完整模型则生成物理合理且语义连贯的布局。这证实了双重引导蒸馏中整体教师与步骤教师的互补性——前者提供场景级空间约束，后者确保逐物体放置精度。

### 定性结果与泛化性

Figure 5展示了文本到3D布局生成的定性对比。在“gaming room”场景中，LayoutGPT和LayoutVLM均出现物体碰撞，而LaviGen有效避免了此类伪影；在“children‘s room”和“deli”场景中，基线方法产生悬空物体，LaviGen则保持所有物体正确着地。Figure 6展示了布局编辑能力：LaviGen支持物体插入和删除，且编辑结果与周围上下文空间一致、语义连贯——这是此前方法难以实现的，因为它们无法在原生3D空间中进行直接操作。

Figure 8验证了长序列生成能力，LaviGen可处理超过20个物体的场景，保持物理合理性不退化。Figure 9进一步验证了框架的骨干无关性：在不依赖特定3D生成模型的情况下，LaviGen仍保持高质量生成，表明其核心设计（自回归扩散+身份感知嵌入+双重引导蒸馏）具有通用性。Figure 10展示了多样性生成：同一指令可产生多种合理布局，体现了扩散模型的随机性优势。

### 失败模式与局限性

尽管物理合理性指标表现优异，LaviGen的语义一致性（PSA 78.8）仍显著低于物理指标（CF 97.3, IB 98.6），表明在复杂空间关系（如“椅子朝向桌子”）的语义对齐上仍有不足。这一差距的根源可能在于文本条件机制的容量限制和训练数据中语义标注的稀疏性。此外，当前体素分辨率有限，更高分辨率的网格会显著增加计算成本；物体的细粒度几何拟合依赖ICP后处理，可能引入额外误差。这些局限性指向了未来工作方向：在不显著增加计算开销的前提下提高体素分辨率、改进文本条件机制以增强语义一致性。

![[assets/figures/papers/paper_list_l2580_https_arxiv_org_abs_2604_16299/figures/008_Figure_7.jpg]]
*Figure 7: Qualitative ablation study for LaviGen. We show the progressive improvement from the base model (left) to the full model (right). The baseline produces cluttered layouts with severe collisions, while adding the identity-aware embedding yields a more plausible distribution but still suffers collisions from exposure bias. Distillation with holistic guidance yields inaccurate object fitting and severe inversion errors for small objects. In contrast, the full model generates physically plausible and semantically coherent layouts*

![[assets/figures/papers/paper_list_l2580_https_arxiv_org_abs_2604_16299/figures/010_Figure_8.jpg]]
*Figure 8: Qualitative results for long-sequence generation with more than 20 objects*

## 定位与知识库关联

### 方法谱系：从语言先验到几何先验的范式迁移

3D 场景布局生成长期存在两条技术路线。第一条路线将布局视为**结构化语言**，依赖大语言模型（LLM）的常识推理能力，以 JSON 格式输出物体的边界框参数。代表性工作包括 **LayoutGPT**（以 GPT 系列为骨干，通过 in-context learning 生成空间配置）、**Holodeck**（语言引导的 3D 环境生成）和 **I-Design**（基于 LLM 的迭代优化室内设计）。这些方法的核心瓶颈在于：LLM 缺乏原生 3D 空间的几何感知能力，无法精确建模物体间的碰撞、穿透和悬空等物理约束，生成的布局在物理合理性上存在系统性缺陷。

第二条路线将布局生成转化为**基于视觉的优化问题**，代表工作为 **LayoutVLM**（通过视觉语言模型进行可微分优化，将 2D 渲染图像作为监督信号）。该方法虽然引入了视觉反馈，但本质上仍依赖 2D 投影间接推理 3D 关系，存在维度信息损失，且优化过程计算开销大（平均推理时间约 75.5 秒）。

**LaviGen** 实现了根本性的范式迁移：将预训练的 3D 生成模型（TRELLIS 结构级生成阶段）重新用于自回归布局生成，直接继承其内部的 3D 空间关系先验。这一设计使得模型不再需要从语言或 2D 图像中“猜测”空间关系，而是在连续的 3D 体素空间中逐次放置物体，天然具备物理约束感知能力。从方法谱系看，LaviGen 属于**原生 3D 生成式布局**这一新兴类别，其核心创新在于将 3D 资产生成模型的空间先验迁移至多物体场景组合任务。

### 关键技术差异：四个维度的对比

| 维度 | 基线方法 | LaviGen |
|------|---------|---------|
| **布局表示** | JSON 序列化边界框（LayoutGPT）或 2D 渲染图像（LayoutVLM） | 3D 体素占用潜变量（结构化潜编码） |
| **生成范式** | LLM 文本生成或基于 2D 视觉的优化 | 自回归 3D 扩散模型（Flow Matching）原生空间建模 |
| **训练策略** | Teacher Forcing（依赖真值上下文） | Self-Rollout + 双重引导蒸馏（整体引导与步骤引导） |
| **位置编码** | 无身份区分 | 身份感知 RoPE（区分场景/物体潜码） |

**布局表示**的差异是最根本的。JSON 边界框将 3D 空间关系压缩为 9 个自由度（位置、尺寸、旋转）的数值向量，丢失了物体形状和空间占用的细粒度信息。LaviGen 采用体素级潜编码 $\mathcal{Z} = \{ z_p \mid p \in \mathcal{P} \}$，保留了完整的空间占用信息，使模型能够直接感知物体间的几何交互。

**生成范式**的差异决定了物理合理性的上限。LLM 通过文本 token 的统计相关性预测坐标值，缺乏对欧几里得空间的归纳偏置；LayoutVLM 的 2D 优化路径则受限于视角选择和维度投影损失。LaviGen 的自回归 3D 扩散过程直接在体素空间执行流匹配：
$$\mathcal{L} = \mathbb{E}_{t, x_0, s, o, c, \epsilon} \left\| v_{\theta}(x, s, o, c, t) - (\epsilon - x_0) \right\|_2^2$$
该损失函数在连续 3D 坐标上优化时间依赖向量场，天然编码了空间平滑性和物理约束。

**训练策略**的差异揭示了自回归生成中的核心挑战——曝光偏差（exposure bias）。Teacher Forcing 在训练时使用真值历史状态 $S_i^\theta = G_\theta(S_{i-1}, O_i, c)$，但推理时模型只能依赖自生成状态 $S_i^\theta = G_\theta(S_{i-1}^\theta, O_i, c)$，导致误差累积。LaviGen 的 Self-Rollout 机制在训练阶段即使用自生成上下文，配合双重引导蒸馏（整体教师提供场景级监督，步骤教师提供物体级监督），通过梯度 $\nabla_{\theta} \mathcal{L}_{dual} \approx \mathbb{E}_{x_t, t} [ (s_{\mathcal{T}}(x_t, t) - s_{\psi}(x_t, t)) \nabla_{\theta} x_0 ]$ 消除训练-推理分布偏移。

### 适用边界与局限性

**适用场景**：
- 文本到 3D 布局生成（给定自然语言指令和物体库，自动配置空间布局）
- 布局编辑与补全（支持物体插入、删除，上下文感知的空间一致性修改）
- 长序列生成（已验证可处理超过 20 个物体的场景，见 Figure 8）
- 跨 3D 生成骨干泛化（框架不依赖特定生成模型，见 Figure 9）

**已知局限**：
1. **语义一致性弱于物理合理性**：尽管物理指标（Collision-Free 97.3, In-Boundary 98.6）表现优异，语义对齐评分（PSA 78.8）仍有提升空间，尤其在复杂空间关系（如“钢琴放在角落，面向餐桌”）时语义理解不足。
2. **体素分辨率约束**：当前体素分辨率有限，更高分辨率的网格会显著增加计算成本。物体的细粒度几何拟合依赖 ICP 后处理，可能引入额外误差。
3. **物体库依赖**：当前框架假设物体库预定义，无法处理开放世界中未预定义物体类别的场景。

### 开放问题

1. **效率-精度权衡**：如何在不显著增加计算开销的前提下提高体素分辨率，以处理更精细的物体交互（如抽屉开合、物体堆叠）？
2. **语义对齐增强**：如何改进文本条件机制（当前使用 Qwen2.5-VL-7B-Instruct）和标注数据质量，以进一步增强语义一致性，缩小物理合理性与语义连贯性之间的差距？
3. **零样本扩展**：能否将自回归 3D 扩散框架扩展到开放世界场景，支持未预定义物体类别的零样本布局生成？
4. **实时交互**：自推演蒸馏的动力学能否进一步压缩推理步数（当前平均 24.3 秒），达到实时交互水平，以支持 VR/AR 场景中的即时布局编辑？

---

> **验证提示**：本文中 LayoutGPT、Holodeck、I-Design、LayoutVLM 的具体发表信息（作者、会议、年份）在提供的分析材料中未明确标注，建议查阅原文或引用数据库补充完整引用信息。

## 原文 PDF

![[paperPDFs/CVPR_2026/Repurposing_3D_Generative_Model_for_Autoregressive_Layout_Generation.pdf]]
