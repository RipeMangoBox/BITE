---
title: "MotionMaster: Generalizable Text-Driven Motion Generation and Editing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MotionMaster_Generalizable_Text_Driven_Motion_Generation_and_Editing.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Jiang_MotionMaster_Generalizable_Text-Driven_Motion_Generation_and_Editing_CVPR_2026_paper.html
project_link: https://jnnan.github.io/motionmaster
code_link: null
aliases:
- MotionMaster
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 使用大规模、多级语义标注的运动数据（MotionGB）对预训练的MLLM（Qwen2.5-VL）进行微调，使运动令牌与语言令牌共享嵌入空间，通过联合训练生成和编辑任务，并引入语义平衡采样，从而将MLLM的语义先验注入运动生成。
primary_logic: 微调预训练MLLM是利用其动作语义和长程依赖的的高效途径；结合FSQ化的局部运动特征与全局重建损失，可兼顾紧凑表示与轨迹精度；统一生成和编辑的联合训练，配合语义平衡，使模型获得零样本泛化、复杂动作组合和精细局部控制的能力，而不依赖于记忆训练样本。
claims:
- 微调预训练MLLM在多种文本驱动运动生成和编辑任务上实现了强大的零样本泛化。
- 在multi-action语义一致性上比现有方法提高41.6%。
- 在身体部位组合上准确率提高20.8%。
- OOD单动作生成提高26.8%，且由预训练MLLM带来的语义理解使其能生成训练期间未见过的动作组合（如“投篮后做侧手翻”）。
---

# MotionMaster: Generalizable Text-Driven Motion Generation and Editing

> [!tip] 核心洞察
> 微调预训练MLLM是利用其动作语义和长程依赖的的高效途径；结合FSQ化的局部运动特征与全局重建损失，可兼顾紧凑表示与轨迹精度；统一生成和编辑的联合训练，配合语义平衡，使模型获得零样本泛化、复杂动作组合和精细局部控制的能力，而不依赖于记忆训练样本。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionMaster：可泛化的文本驱动运动生成与编辑 |
| 英文题名 | MotionMaster: Generalizable Text-Driven Motion Generation and Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Jiang_MotionMaster_Generalizable_Text-Driven_Motion_Generation_and_Editing_CVPR_2026_paper.html) · [Project](https://jnnan.github.io/motionmaster) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MotionMaster |
| Dataset | Multi-action temporal composition, Body-part spatial composition, OOD single motion generation |

> [!tip] 效果简介
> - Multi-action temporal composition 上，语义一致性 (semantic consistency) 相对提升41.6% vs Prior SOTA methods (+41.6%)。
> - Body-part spatial composition 上，准确率 (accuracy) 相对提升20.8% vs Prior SOTA methods (+20.8%)。
> - OOD single motion generation 上，性能 (performance) 相对提升26.8% vs Existing SOTA methods (+26.8%)。

## 概述

**问题瓶颈**：现有的文本驱动人体运动生成方法面临三个结构性困境。其一，依赖HumanML3D、KIT-ML等小规模、粗粒度标注的数据集，缺乏对复杂文本指令的语义覆盖与组合泛化能力。其二，运动表示往往在局部关节精度与全局轨迹一致性之间顾此失彼——直接编码全局坐标容易累积漂移，而纯局部表示又丢失长程空间约束。其三，多动作生成与局部编辑通常依赖分离的后组合管道，缺少端到端的统一语义理解。更根本的是，绝大多数方法从零训练模型，未能利用预训练多模态大语言模型（MLLM）中已编码的丰富动作语义和长程推理能力。

**核心方法**：**MotionMaster** 通过三个关键设计突破上述瓶颈。首先，构建了**MotionGB**——一个10,000小时、多级语义标注的运动-语言数据集，通过时间拼接、身体部位组合和精细化参数编辑生成丰富的训练对。其次，提出基于有限标量量化（FSQ）的运动标记器：将每帧的局部特征（偏航角速度 + 相对关节位置）量化为离散令牌，同时以全局坐标下的关节位置损失和速度损失监督重建，兼顾紧凑表示与轨迹精度。最后，将运动令牌与语言令牌嵌入同一个空间，对预训练MLLM（Qwen2.5-VL）进行微调，统一执行文本到运动生成和文本引导的运动编辑，并引入基于语义密度的采样平衡策略，防止模型偏向高频简单动作。

**核心结论**：微调预训练MLLM使MotionMaster获得了显著的零样本泛化能力。在multi-action时序组合任务上，语义一致性相对现有方法提升**41.6%**；在body-part空间组合任务上，准确率提升**20.8%**；在OOD单动作生成上，性能提升**26.8%**。模型能够生成训练期间从未见过的动作组合（如“投篮后做侧手翻”），证明其继承自预训练MLLM的动作语义理解而非记忆训练样本。

**方法定位**：MotionMaster属于**基于MLLM微调的统一运动生成-编辑框架**，区别于基于扩散的MDM（Tevet et al., ICLR 2023）、基于离散令牌自回归的T2M-GPT（Zhang et al., CVPR 2023）和MotionGPT（Jiang et al., NeurIPS 2023）、基于掩码建模的MMM（Pinyoanuntapong et al., CVPR 2024）等从零训练或分离式方案。其核心差异在于：以大规模多级标注数据为燃料，将预训练MLLM的语义先验注入运动生成，并通过统一的运动-语言令牌空间和联合训练策略，实现生成与编辑的互惠增强。

## 背景与动机

### 问题背景：文本驱动的三维人体运动生成

文本驱动的三维人体运动生成旨在根据自然语言描述合成逼真的人体动作序列，在动画制作、虚拟现实、人机交互等领域具有广泛应用。该任务的核心挑战在于建立自然语言语义与人体运动动力学之间的精确映射，同时保证生成运动的物理合理性、时序连贯性以及与文本指令的语义一致性。

### 现有方法的瓶颈

当前文本驱动运动生成方法面临三个关键瓶颈：

**数据瓶颈：语义覆盖与组合泛化不足。** 现有方法普遍依赖HumanML3D、KIT-ML等小规模数据集，这些数据集仅提供粗粒度的单一动作标注，缺乏对复杂文本指令的语义覆盖。模型难以从有限标注中习得动作的组合泛化能力，导致在面对多动作序列描述或身体部位组合指令时性能急剧下降。

**表示瓶颈：局部精度与全局一致性的两难。** 运动表示的选择直接影响生成质量。基于全局关节位置或全局旋转矩阵的直接编码方案虽能保持轨迹一致性，却难以捕捉局部关节的精细运动模式；而纯局部表示则容易因误差累积导致轨迹漂移。现有方法缺乏一种能同时兼顾局部关节精度与全局轨迹一致性的紧凑表示。

**架构瓶颈：管道碎片化与语义理解缺失。** 主流方法要么基于扩散模型（如**MDM**，Tevet et al., ICLR 2023；**MLD**），要么基于离散令牌的自回归生成（如**T2M-GPT**，Zhang et al., CVPR 2023；**MotionGPT**，Jiang et al., NeurIPS 2023），但多动作生成和局部编辑通常依赖后组合或分离的任务分支（如**MMM**，Pinyoanuntapong et al., CVPR 2024），缺乏端到端的统一语义理解框架。最关键的是，这些方法绝大多数从头训练模型，未能利用预训练多模态大语言模型中已编码的丰富动作语义和长程推理能力。

### 核心动机

针对上述瓶颈，MotionMaster的核心动机在于：**通过微调预训练多模态大语言模型，将其已编码的动作语义先验注入运动生成过程，从而以统一框架实现文本到运动生成和文本引导运动编辑的零样本泛化。** 这一思路的关键洞察是：预训练MLLM中蕴含的丰富语义知识和长程依赖建模能力，是突破数据规模限制、实现复杂动作组合和精细局部控制的高效途径。为此，需要构建大规模、多级语义标注的运动数据集，设计兼顾局部精度与全局一致性的运动表示，并通过联合训练和语义平衡策略充分释放MLLM的泛化潜力。

## 核心创新

MotionMaster 的核心创新并非单一技术的突破，而是通过**数据、表示、模型架构与训练策略四个维度的协同重构**，将预训练多模态大语言模型（MLLM）中已编码的丰富动作语义与长程推理能力注入运动生成。其关键 changed slots 如下：

### 1. 数据：从稀疏标注到大规模多级语义覆盖

现有方法（如 MDM、T2M-GPT、MotionGPT）依赖 HumanML3D 或 KIT-ML 等小规模、单一层级标注的数据集，缺乏对复杂文本指令的语义覆盖与组合泛化能力。MotionMaster 构建了 **MotionGB**——一个 10,000 小时的多级语义标注运动-语言数据集（Figure 2）。其构建管道包括：
- 从开源动捕数据库、视频源和专有录制中收集 400 小时原始运动数据；
- 经人工验证清洗后，利用 Gemini 为每条序列生成多层级运动描述；
- 通过**时序拼接**（组合连续动作）、**身体部位拼接**（合并不同身体部位的运动）和**精细化运动调整**（参数化修改以创建编辑对）三种增强策略，将数据集扩展至 10,000 小时。

这一数据层面的根本性变化，为模型学习复杂动作组合和精细局部控制提供了必要的语义密度和多样性。

### 2. 运动表示与量化：从全局编码到局部特征 FSQ + 全局重建监督

传统方法通常对全局关节位置或全局旋转矩阵直接进行整体编码，难以兼顾局部关节精度与全局轨迹一致性。MotionMaster 提出了一种基于 **有限标量量化（FSQ）** 的局部运动标记化方法（Figure 3a）：

- **局部特征提取**：对 SMPL-X 关节序列逐帧提取偏航角变化 $\Delta\theta_t$ 和相对于前一帧局部坐标系的关节位置 $\mathbf{p}_{t+1}'$，构成 85 维局部特征向量 $\mathbf{f}_t = [\Delta\theta_t, \mathrm{flatten}(\mathbf{p}_{t+1}')] \in \mathbb{R}^{85}$。这一设计显式剥离了全局朝向，使量化器专注于局部运动模式。
- **FSQ 离散化**：通过 $\hat{z}_{i,d} = \mathrm{round}(z_{i,d} \cdot L_d) / L_d$ 对每个潜在维度独立量化，无需维护码本，避免了 VQ 中的码本坍塌和索引分配问题。
- **全局重建损失**：在全局坐标系上计算关节位置损失 $\mathcal{L}_{\mathrm{global}}$ 和速度损失 $\mathcal{L}_{\mathrm{vel}}$，直接监督解码重建，防止累积轨迹漂移。

消融实验（Table 3）证实，该标记器在局部关节位置误差（9.14 cm）和全局位置误差（9.53 cm）上均达到最优，显著优于常见的 Global VQ 等方案。

### 3. 模型架构：从从头训练到微调预训练 MLLM

这是 MotionMaster 最根本的架构创新。现有方法（MDM、MLD、MMM 等）大多从头训练 CLIP 文本编码器加扩散或 Transformer 模型，未能利用预训练模型中已有的丰富语义先验。MotionMaster 选择**微调预训练 MLLM（Qwen2.5-VL）**，使运动令牌与语言令牌共享同一个嵌入空间（Figure 3b, c），通过自回归生成实现跨模态融合。

这一设计的核心洞察在于：预训练 MLLM 中已编码大量关于人体动作的语义知识和长程依赖关系，微调是将其注入运动生成的高效途径，而非从零开始学习。实验证明，该策略使模型能够生成训练期间从未见过的动作组合（如“投篮后做侧手翻”），实现了真正的零样本泛化。

### 4. 训练策略：从分离训练到联合训练 + 语义平衡采样

传统方法将运动生成与编辑视为独立任务分别训练，管道碎片化。MotionMaster 采用**生成与编辑任务的联合训练**，并引入**基于语义密度的采样概率调整**：

- **联合训练**：单一模型同时执行文本到运动生成和文本引导的运动编辑，两任务共享语义理解能力。消融实验（Table 2）表明，联合训练始终优于单独训练——生成任务语义得分从 7.40 提升至 9.88，编辑任务同样受益，证实两任务互补且相互增强。
- **语义密度平衡**：基于 T5 文本嵌入计算局部语义密度 $\rho_i$，并以 $p_i \propto \rho_i^{-\alpha}$ 调整采样概率，防止模型偏向高频简单动作而过拟合。这一机制确保模型在语义多样的长尾动作上也保持生成能力。

### 创新协同效应

上述四个 changed slots 形成闭环：MotionGB 提供的大规模多级语义数据为 MLLM 微调提供了基础；FSQ 局部标记化使运动令牌与语言令牌在共享嵌入空间中的对齐更为紧凑高效；联合训练与语义平衡则充分利用了数据和架构的潜力。最终，MotionMaster 在多动作时序组合语义一致性上相对现有 SOTA 提升 **41.6%**，在身体部位空间组合准确率上提升 **20.8%**，在 OOD 单动作生成上提升 **26.8%**，验证了这一协同设计的有效性。

## 整体框架

MotionMaster 构建了一个端到端的统一框架，将文本驱动的运动生成与运动编辑整合在单个自回归模型中。该框架的核心思路是：**通过微调预训练多模态大语言模型（MLLM），将其固有的动作语义先验和长程推理能力注入运动生成任务**，而非从头训练专用模型。

### 框架总览

整个 pipeline 由四个核心模块串联而成，形成“文本/运动输入 → 离散令牌 → 自回归生成/编辑 → 物理重建”的完整链路：

| 模块 | 功能 | 输入 | 输出 |
|------|------|------|------|
| **Motion Tokenizer (FSQ)** | 将连续运动序列编码为离散令牌，并支持解码重建 | SMPL-X 关节序列 | 离散运动令牌 / 重建的 3D 关键点轨迹 |
| **Unified Motion-Language Model** | 基于微调的 Qwen2.5-VL，自回归地生成或编辑运动令牌 | 文本提示（+ 原始运动令牌，编辑时） | 目标运动令牌序列 |
| **Coarse-to-Fine IK Solver** | 将生成的 3D 关键点轨迹转化为物理合理的 SMPL-X 参数 | 3D 关键点轨迹 | SMPL-X 姿态与形状参数 |
| **Semantic Density Balancer** | 在微调过程中按语义密度重平衡采样概率 | 训练样本的 T5 文本嵌入 | 加权采样分布 |

### 推理流程

**文本到运动生成**（Figure 3b）：用户输入自然语言描述（如“投篮后做侧手翻”），MLLM 以文本为条件，自回归地逐帧解码运动令牌序列；Motion Tokenizer 的解码器将令牌序列重建为 3D 关键点轨迹；最后通过 IK Solver 拟合出完整的 SMPL-X 身体运动。

**文本引导的运动编辑**（Figure 3c）：用户提供原始运动序列和编辑指令（如“将右手举过头顶”），原始运动先经 Motion Tokenizer 编码为令牌序列，与编辑文本一同输入 MLLM；MLLM 选择性修改相关令牌，保留未指定的运动部分，再经解码和 IK 求解输出编辑后的运动。

### 设计决策与因果机制

框架设计的三个关键决策直接回应了现有方法的瓶颈：

1. **微调预训练 MLLM 而非从头训练**：现有方法（如 **MDM** (Tevet et al., ICLR 2023)、**T2M-GPT** (Zhang et al., CVPR 2023)、**MotionGPT** (Jiang et al., NeurIPS 2023)）使用 CLIP 等文本编码器从头训练，缺乏对复杂动作语义和长程依赖的理解。MotionMaster 选择 Qwen2.5-VL 作为基座，运动令牌与语言令牌共享同一嵌入空间，使模型天然具备组合泛化能力——证据显示，模型能生成训练期间从未见过的动作组合（如“投篮后做侧手翻”），这正是预训练语义先验的直接体现。

2. **FSQ 局部特征量化 + 全局损失监督**：纯全局坐标编码容易丢失局部关节精度，纯局部编码则累积轨迹漂移。MotionMaster 将每帧编码为 85 维局部特征 $\mathbf{f}_t = [\Delta\theta_t, \mathrm{flatten}(\mathbf{p}_{t+1}')]$（偏航角变化 + 相对关节位置），经 FSQ 量化为离散令牌，同时用全局位置损失 $\mathcal{L}_{\mathrm{global}}$ 和速度损失 $\mathcal{L}_{\mathrm{vel}}$ 监督解码重建。消融实验（Table 3）表明，该方案在局部关节位置误差（9.14 cm）和全局位置误差（9.53 cm）上均达到最优，显著优于 Global VQ 等常见方案。

3. **联合训练 + 语义平衡采样**：生成和编辑任务共享同一模型和训练过程，避免了传统方法中分离管道带来的语义割裂。语义密度平衡器根据 T5 嵌入的局部密度 $\rho_i$ 调整采样概率 $p_i \propto \rho_i^{-\alpha}$，防止模型偏向高频简单动作而过拟合。消融实验（Table 2）证实，联合训练使生成任务语义得分从 7.40 提升至 9.88，编辑任务同样受益，两任务形成互补增强。

### 数据基础

框架的训练数据来自 **MotionGB** 数据集（Figure 2）：从开源动捕数据库、视频源和专有录制中收集 400 小时原始运动数据，经人工校验后使用 Gemini 进行多级语义标注，再通过时间拼接、身体部位组合和精细化参数调整三种增强策略扩展至 10,000 小时。这一大规模、多级标注的数据集为 MLLM 微调提供了丰富的语义覆盖和组合训练对，是零样本泛化能力的物质基础。

![[assets/figures/papers/paper_list_l18_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_MotionMaster_Gen/figures/002_Figure_2.jpg]]
*Figure 2: Overview of MotionGB construction pipeline. (a) 400 hours of raw motion data are collected from open-source motion capture databases, video sources, and proprietary recordings. (b) After manual verification and cleaning, each sequence is annotated with multilevel motion descriptions generated via Gemini [56]. (c) The dataset is expanded to 10,000 hours through three augmentation strategies: temporal concatenation (combining sequential actions), body-part concatenation (merging movements from different body parts), and finegrained motion adjustment (applying parametric modifications to create editing pairs)*

### 补充图表

![[assets/figures/papers/paper_list_l18_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_MotionMaster_Gen/figures/001_Figure.jpg]]
*Figure: (a) End-to-end sequential text-to-motion generation*

## 核心模块与公式推导

### 3.1 局部运动特征提取与坐标变换

运动标记器（Motion Tokenizer）的核心设计目标是将全局人体运动转化为一种**紧凑、局部化且易于量化的特征表示**，同时保留重建全局轨迹的能力。为此，MotionMaster 设计了五步特征提取管线。

**Step 1: 偏航角提取。** 对每一帧 $t$，从 SMPL-X 根关节的旋转矩阵 $\mathbf{r}_t$ 中提取水平偏航角：

$$\theta_t = \mathtt{atan2}(\mathbf{r}_t \cdot [0, 0, 1])$$

**Step 2: 偏航角变化。** 计算相邻帧之间的偏航角差，作为局部方向变化信号：

$$\Delta\theta_t = \theta_{t+1} - \theta_t$$

**Step 3: 前一帧根关节投影。** 将前一帧的根关节投影到地面平面（y-up 坐标系），用于后续的相对坐标变换：

$$\mathbf{p}_t^{\mathrm{root}} = [\mathbf{p}_{t,0,x},\ 0,\ \mathbf{p}_{t,0,z}]$$

**Step 4: 相对坐标变换。** 将第 $t+1$ 帧的所有关节变换到第 $t$ 帧的局部坐标系中，抵消偏航旋转的影响：

$$\mathbf{p}_{t+1}' = R_{-\theta_t}\big(\mathbf{p}_{t+1} - \mathbf{p}_t^{\mathrm{root}}\big)$$

其中偏航旋转矩阵 $R_{-\theta_t}$ 为绕 y 轴旋转 $-\theta_t$ 的 3×3 矩阵：

$$R_{-\theta_t} = \begin{bmatrix} \cos(-\theta_t) & 0 & -\sin(-\theta_t) \\ 0 & 1 & 0 \\ \sin(-\theta_t) & 0 & \cos(-\theta_t) \end{bmatrix}$$

**Step 5: 特征向量拼接。** 将偏航角变化与扁平化的 21 个关节相对坐标拼接，形成第 $t$ 帧的 85 维局部运动特征：

$$\mathbf{f}_t = [\Delta\theta_t,\ \mathrm{flatten}(\mathbf{p}_{t+1}')] \in \mathbb{R}^{85}$$

这一设计的因果机制在于：仅对局部模式（偏航差 + 相对关节位置）进行离散化，避免了直接量化全局坐标带来的大误差和轨迹漂移问题；而全局轨迹的一致性则通过后续的重建损失来保证。

### 3.2 FSQ 量化与重建监督

**编码与量化。** 1D 卷积编码器 $E$ 将长度为 $T$ 的局部特征序列压缩为潜在表示：

$$\mathbf{z} = E(\mathbf{f}) \in \mathbb{R}^{T' \times D}$$

随后，**有限标量量化**（Finite Scalar Quantization, FSQ）对潜在表示的每个维度独立进行离散化：

$$\hat{z}_{i,d} = \mathrm{round}(z_{i,d} \cdot L_d) / L_d$$

其中 $L_d$ 为第 $d$ 维的量化级别数。与传统的 VQ（Vector Quantization）相比，FSQ 无需维护码本和进行码本坍塌修复，训练更稳定，且能产生紧凑的离散运动令牌，直接作为 MLLM 的输入。

**全局重建损失。** 解码器将量化后的潜在表示重建为关节序列。为防止仅依赖局部特征导致的轨迹漂移，在**全局坐标系**上施加两个监督损失。

全局位置损失直接监督每个关节的绝对位置：

$$\mathcal{L}_{\mathrm{global}} = \frac{1}{TJ}\sum_{t=1}^{T}\sum_{j=1}^{J}\|\mathbf{p}_{t,j} - \hat{\mathbf{p}}_{t,j}\|_2^2$$

速度损失监督关节运动的一阶差分一致性：

$$\mathcal{L}_{\mathrm{vel}} = \frac{1}{(T-1)J}\sum_{t=1}^{T-1}\sum_{j=1}^{J}\|\big(\mathbf{p}_{t+1,j} - \mathbf{p}_{t,j}\big) - \big(\hat{\mathbf{p}}_{t+1,j} - \hat{\mathbf{p}}_{t,j}\big)\|_2^2$$

这两个损失的组合构成了运动标记器重建质量的关键保障。消融实验（Table 3）表明，该方案在局部关节位置误差（9.14 cm）和全局位置误差（9.53 cm）上均达到最优，显著优于常见的 Global VQ 等方案。

### 3.3 语义密度平衡采样

MotionGB 数据集中存在严重的语义长尾分布——简单高频动作（如“行走”“站立”）远多于复杂稀有动作。为避免模型过拟合常见模式，MotionMaster 在微调阶段引入了**语义密度平衡器**。

首先，利用 T5 文本编码器为每个运动样本的文本描述生成嵌入 $e_i$，然后计算其局部语义密度：

$$\rho_i = \frac{1}{k}\sum_{j \in \mathcal{N}_k(i)} \exp\left(-\frac{\|e_i - e_j\|^2}{2\sigma^2}\right)$$

其中 $\mathcal{N}_k(i)$ 是嵌入空间中样本 $i$ 的 $k$ 个最近邻。语义密度 $\rho_i$ 越高，表示该样本处于语义密集区域（即常见动作），应降低其采样权重。

采样概率按语义密度的负幂次进行重平衡：

$$p_i \propto \rho_i^{-\alpha}$$

其中 $\alpha$ 控制重平衡强度。这一机制使训练过程更均匀地覆盖语义多样的动作，是模型获得零样本泛化和复杂动作组合能力的关键训练策略。

### 补充图表

![[assets/figures/papers/paper_list_l18_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_MotionMaster_Gen/figures/004_Figure_3.jpg]]
*Figure 3: Overview of MotionMaster. (a) The FSQ-based motion tokenizer encodes joint positions into localized features, quantizes them into discrete tokens, and supervises reconstruction via a loss computed in global coordinates. (b) For text-to-motion generation, the finetuned MLLM autoregressively decodes motion tokens conditioned on a text prompt. (c) For text-guided editing, the original motion is provided as additional context, and the MLLM selectively modifies the relevant tokens while preserving the remainder of the sequence*

## 实验与分析

### 主实验结果

MotionMaster 在运动生成与编辑两大任务上均取得了全面领先。**Table 1** 汇总了与现有 SOTA 方法的定量对比。在生成任务上，MotionMaster 的语义一致性得分达到 9.88，显著超越所有基线方法。具体而言，在多动作时序组合（multi-action temporal composition）任务上，语义一致性相对现有方法提升 **41.6%**；在身体部位空间组合（body-part spatial composition）准确率上提升 **20.8%**；在分布外（OOD）单动作生成任务上提升 **26.8%**。编辑任务同样展现出明显优势，MotionMaster 能够根据文本指令精确修改特定身体部位或运动属性，同时保持其余序列不变。

![[assets/figures/papers/paper_list_l18_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_MotionMaster_Gen/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison of MotionMaster against SOTA baselines and ablation studies. MotionMaster achieves superior performance across most metrics for both motion generation and editing. The relatively lower diversity scores reflect a known trade-off between diversity and semantic fidelity rather than a limitation of the approach*

值得注意的是，MotionMaster 在多样性指标上的得分相对较低。论文明确指出，这反映了语义保真度与多样性之间的已知权衡（trade-off），而非方法本身的缺陷——模型倾向于生成语义更准确的运动，而非追求表面的多样性。

这些提升的核心驱动力来自预训练 MLLM 中编码的丰富动作语义。MotionMaster 能够生成训练期间从未见过的动作组合（如“投篮后做侧手翻”），这直接证明模型并非记忆训练样本，而是真正继承了 MLLM 的语义理解和组合泛化能力。

### 消融实验

#### 联合训练对生成与编辑的互惠效应

**Table 2** 展示了联合训练与任务特定训练的对比。结果表明，联合训练生成与编辑任务始终优于单独训练：生成任务的语义得分从 7.40 提升至 9.88，编辑任务同样显著受益。这验证了两个任务之间存在互补关系——编辑任务提供的局部运动修改信号有助于模型学习更精细的运动控制，而生成任务提供的全局语义理解又反哺编辑的准确性。

#### 运动标记器重建精度

**Table 3** 评估了 FSQ 运动标记器在 MotionGB-test 上的重建精度。该标记器在局部关节位置误差（Local Pos. 9.14 cm）和全局位置误差（Global Pos. 9.53 cm）两项指标上均达到最优，显著优于常见的 Global VQ 等方案。这验证了“局部特征量化 + 全局损失监督”设计的有效性：FSQ 对偏航角速度和相对关节位置等局部模式进行离散化，保证了紧凑的令牌表示；而全局位置损失 $\mathcal{L}_{\mathrm{global}}$ 和速度损失 $\mathcal{L}_{\mathrm{vel}}$ 直接监督全局坐标下的重建，有效防止了自回归解码中的轨迹漂移。

#### 语义平衡采样的作用

语义密度平衡器通过调整采样概率 $p_i \propto \rho_i^{-\alpha}$，降低了高频简单动作（如“行走”“站立”）的采样权重，提升了语义多样动作的曝光率。消融表明，移除语义平衡后，模型在复杂动作组合和 OOD 场景下的性能明显下降，验证了该策略对防止模型偏向常见模式的关键作用。

### 失败模式与局限性

尽管 MotionMaster 在多数指标上表现优异，论文中未提供详细的失败案例分析。根据方法设计可推断以下潜在局限：

1. **自回归误差累积**：尽管全局损失有效抑制了轨迹漂移，但在极长序列（数百帧以上）的自回归生成中，误差仍可能逐步累积，导致末端动作偏离文本描述。这一点的具体影响需要手动验证。
2. **IK 求解器的物理合理性边界**：Coarse-to-Fine IK Solver 依赖 VPoser 潜空间先验，对于极端或罕见的身体姿态（如高难度体操动作），优化可能陷入局部最优，产生不自然的关节旋转。
3. **MLLM 语义理解的盲区**：模型继承了预训练 MLLM 的动作语义，但对于训练数据中完全未覆盖的动作概念（如特定文化舞蹈或专业运动术语），零样本泛化能力可能受限。论文未对此类边界情况进行定量评估。

### 重要图表结论

- **Table 1**：MotionMaster 在生成与编辑双任务上全面超越 SOTA，语义一致性提升 41.6%，身体部位组合准确率提升 20.8%，OOD 单动作生成提升 26.8%。
- **Table 2**：联合训练生成与编辑任务互惠互利，生成语义得分从 7.40 跃升至 9.88，编辑任务同步受益。
- **Table 3**：FSQ 运动标记器在局部（9.14 cm）和全局（9.53 cm）关节位置误差上均达最优，验证了局部量化 + 全局监督设计的有效性。

![[assets/figures/papers/paper_list_l18_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_MotionMaster_Gen/figures/007_Table_2.jpg]]
*Table 2: Mutual benefits of joint training on generation and editing. Joint training consistently outperforms task-specific training on both generation and editing, confirming that the two tasks are complementary and mutually reinforcing*

![[assets/figures/papers/paper_list_l18_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_MotionMaster_Gen/figures/008_Table_3.jpg]]
*Table 3: Motion tokenizer evaluation on MotionGB-test. Our tokenizer achieves the best joint position accuracy across both local and global metrics. Lower values indicate better performance*

## 方法谱系与知识库定位

### 1. 方法谱系：从扩散模型到预训练MLLM的运动生成演进

MotionMaster 处于文本驱动人体运动生成这一快速迭代的领域，其核心突破在于将运动生成从“从头训练专用模型”的范式迁移到“微调预训练多模态大语言模型（MLLM）”的范式。理解这一跃迁需要梳理其与三类主要基线方法的关系。

**扩散模型路线**以 **MDM**（Tevet et al., ICLR 2023）和 **MLD** 为代表，它们将运动生成建模为从噪声中逐步去噪的过程。这类方法在单动作生成上表现良好，但受限于扩散采样的迭代开销，且缺乏对复杂组合语义的内建理解——它们依赖独立的文本编码器（如CLIP），而CLIP本身并未在运动数据上训练，因此语义对齐能力存在天然上限。MotionMaster 通过自回归地解码运动令牌，避免了迭代采样，同时将文本理解完全交由经过运动数据微调的MLLM，从根本上改变了语义获取方式。

**离散令牌路线**以 **T2M-GPT**（Zhang et al., CVPR 2023）和 **MotionGPT**（Jiang et al., NeurIPS 2023）为代表，它们将运动量化为离散令牌并用GPT类架构进行自回归生成。MotionGPT 首次尝试将运动生成纳入语言模型框架，但其核心瓶颈在于：（1）使用的数据集规模小（HumanML3D / KIT-ML），语义标注粒度粗；（2）运动令牌与语言令牌的嵌入空间未经过大规模预训练语义先验的初始化，本质上仍是从头学习跨模态对齐。MotionMaster 继承了“统一运动-语言令牌”的思路，但通过两个关键升级实现了质变：用 10,000 小时的 MotionGB 替代小规模数据集，用 Qwen2.5-VL 的预训练权重替代随机初始化，使运动令牌天然继承了MLLM中已编码的丰富动作语义和长程推理能力。

**统一生成与编辑路线**以 **MMM**（Pinyoanuntapong et al., CVPR 2024）和 **MotionLab** 为代表，它们试图在同一框架内处理生成和编辑。MMM 基于掩码建模，MotionLab 基于整流流，但两者均未利用预训练MLLM的语义先验，且训练数据规模有限。MotionMaster 的联合训练策略（生成与编辑共享同一自回归目标）证明了两个任务可以相互增强——生成任务获得的语义得分从单独训练的7.40提升至9.88，编辑任务同样受益（Table 2），这揭示了“理解运动语义”与“精确操控运动”在表示层面的深层共享性。

### 2. 知识库定位：核心贡献与适用边界

MotionMaster 对知识库的增量贡献可归纳为四个相互依赖的组件，每个组件解决了一个此前方法未能有效处理的瓶颈：

| 贡献组件 | 解决的核心瓶颈 | 证据强度 |
|---------|--------------|---------|
| MotionGB 数据集（10,000小时，多级语义标注） | 小规模粗粒度数据导致组合泛化能力缺失 | 强：OOD单动作生成提升26.8%，多动作组合提升41.6% |
| FSQ局部运动标记器 + 全局重建损失 | 运动表示无法兼顾局部精度与全局轨迹一致性 | 强：局部位置误差9.14 cm，全局位置误差9.53 cm（Table 3） |
| 微调预训练MLLM（Qwen2.5-VL） | 从头训练模型缺乏动作语义先验 | 强：零样本生成训练中未见过的动作组合（如“投篮后做侧手翻”） |
| 语义平衡采样 + 联合生成编辑训练 | 高频简单动作过拟合，生成与编辑管道碎片化 | 强：联合训练语义得分从7.40提升至9.88（Table 2） |

**适用边界**方面，需要注意以下几点：

1. **数据依赖性**：MotionMaster 的泛化能力高度依赖 MotionGB 的覆盖范围。对于 MotionGB 中未充分表示的运动类型（如极端体育动作、非人形运动），性能可能退化。论文未提供跨数据集（如 HumanML3D → KIT-ML）的零样本迁移实验，这一点需要手动验证。

2. **多样性-语义保真度权衡**：Table 1 中 MotionMaster 的多样性指标相对较低，论文将其解释为“已知的多样性-语义保真度权衡”。这意味着模型倾向于生成语义准确但模式相对集中的运动，在需要高多样性的创意场景（如舞蹈生成）中可能不是最优选择。

3. **MLLM 基座的选择**：当前仅验证了 Qwen2.5-VL 作为基座模型。不同 MLLM 的预训练数据分布和架构差异可能影响运动语义的继承质量，这一泛化性尚未被探索。

4. **计算成本**：微调 72B 级别的 MLLM 需要可观的算力资源，这可能限制了该方法在资源受限场景下的直接复现。

### 3. 局限与开放问题

**已知局限**（来自论文本身）：
- 多样性指标相对较低，论文承认这是语义保真度优化的副产品，但未提出缓解方案。
- 对 MotionGB 数据分布之外的运动类型的泛化能力未被系统评估。

**开放问题**（需要未来工作验证）：
- **跨具身泛化**：FSQ 标记器基于 SMPL-X 的 21 个关节设计，能否泛化到不同骨骼拓扑（如动物运动、机器人运动）尚不明确。
- **实时交互场景**：当前框架的自回归生成 + IK 后处理流程是否满足实时交互的延迟要求，论文未讨论。
- **细粒度物理合理性**：虽然全局重建损失防止了轨迹漂移，但足部滑动、地面穿透等物理约束并未显式建模，IK 求解器的物理合理性边界需要更系统的评估。
- **多模态扩展**：MLLM 原生支持图像输入，但论文未探索“图像/视频 + 文本”联合条件生成的可能性，这是预训练 MLLM 路线的天然优势所在。

## 原文 PDF

![[paperPDFs/CVPR_2026/MotionMaster_Generalizable_Text_Driven_Motion_Generation_and_Editing.pdf]]
