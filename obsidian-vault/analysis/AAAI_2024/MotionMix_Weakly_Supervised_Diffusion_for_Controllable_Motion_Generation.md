---
title: "MotionMix: Weakly-Supervised Diffusion for Controllable Motion Generation"
type: paper
paper_level: A
venue: AAAI
year: 2024
pdf_ref: paperPDFs/AAAI_2024/MotionMix_Weakly_Supervised_Diffusion_for_Controllable_Motion_Generation.pdf
project_link: https://nhathoang2002.github.io/MotionMix-page/
code_link: null
aliases:
- MotionMix
tags:
- AAAI_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过将扩散模型的去噪步骤分配为两个阶段：在初始T-T*步使用含噪标注数据学习条件控制，在最后T*步使用干净未标注数据进行无条件精炼。
primary_logic: 扩散模型的分步去噪特性天然允许在不同时间步使用不同质量的数据：噪声数据在早期提供粗略的条件控制，干净数据在后期提升细节质量，两者互不干扰，从而在弱监督下实现可控生成。
claims:
- "The diffusion model trains clean unannotated motions only on steps [1,T*] and noisy annotated motions on steps [T*+1,T]."
- During sampling, when reaching denoising pivot T*, the condition is replaced by c=∅.
- MDM (MotionMix) reduces FID by 30.0% on HumanML3D compared to MDM.
- EDGE (MotionMix) improves PFC by 43.1% and Distk by 95.0% on music-to-dance.
---

# MotionMix: Weakly-Supervised Diffusion for Controllable Motion Generation

> [!tip] 核心洞察
> 扩散模型的分步去噪特性天然允许在不同时间步使用不同质量的数据：噪声数据在早期提供粗略的条件控制，干净数据在后期提升细节质量，两者互不干扰，从而在弱监督下实现可控生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionMix：用于可控运动生成的弱监督扩散模型 |
| 英文题名 | MotionMix: Weakly-Supervised Diffusion for Controllable Motion Generation |
| 会议/期刊 | AAAI 2024 |
| Links | [Project](https://nhathoang2002.github.io/MotionMix-page/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MotionMix |
| Dataset | HumanML3D, KIT-ML, AIST++ |

> [!tip] 效果简介
> - HumanML3D (text-to-motion) 上，FID↓ 0.381±.042 (MDM + MotionMix) vs 0.544±.440 (MDM) (↑30.0%)。
> - KIT-ML (text-to-motion) 上，FID↓ 0.322±.020 (MDM + MotionMix) vs 0.497±.021 (MDM) (↑35.2%)。
> - AIST++ (music-to-dance) 上，Beat Align.↑ 0.256±.013 (EDGE + MotionMix) vs 0.224±.025 (EDGE retrained) (↑13.3%)。

## 概要

**核心问题**：获取大规模高质量标注运动数据成本高昂，而现实世界中大量未标注或含噪声的运动数据未被有效利用，这构成了可控运动生成任务的关键瓶颈。

**核心方法**：MotionMix 提出一种弱监督扩散模型，将扩散去噪过程划分为两个阶段——在初始 $T-T^*$ 步使用含噪标注数据学习条件控制以获取粗略运动近似，在最后 $T^*$ 步使用干净未标注数据进行无条件精炼以提升细节质量。这一设计利用了扩散模型分步去噪的天然特性：噪声数据在早期提供粗略的条件控制，干净数据在后期提升细节质量，两者互不干扰。

**方法定位**：MotionMix 是一种即插即用的训练范式，可适配多种扩散骨干模型（MDM、MotionDiffuse、EDGE），在文本到运动、动作到运动、音乐到舞蹈三类任务上均验证了有效性。

**主要结果**：
- 在 HumanML3D 文本到运动任务上，MDM（MotionMix）相比全监督 MDM 将 FID 降低 30.0%（0.381 vs. 0.544）。
- 在 KIT-ML 上，FID 进一步降低 35.2%（0.322 vs. 0.497）。
- 在 AIST++ 音乐到舞蹈任务上，EDGE（MotionMix）将物理足部接触指标（PFC）提升 43.1%，运动多样性（Distk）相对提升 95.0%。
- 消融实验表明，50%-70% 的含噪数据比例以及适中的噪声范围 $[T_1, T_2]$ 能稳定带来性能增益，验证了方法对弱监督数据分布的良好适应性。

**局限与展望**：方法在小规模数据集上可能性能下降，超参数 $T^*$ 和噪声范围需手动调节，且仅在高斯扩散噪声假设下验证有效。未来方向包括自适应枢轴选择、跨模态扩展及半监督场景下的进一步探索。

### 问题背景

人类运动生成（human motion generation）旨在根据文本、动作标签或音乐等控制信号合成自然、多样的人体动作序列，在动画制作、虚拟现实、游戏开发和人机交互等领域具有广泛应用。近年来，扩散模型（diffusion models）凭借其稳定的训练过程和高质量的生成能力，已成为该领域的主流范式。以 **MDM**（Tevet et al., 2022）、**MotionDiffuse**（Zhang et al., 2022）和 **EDGE**（Tseng et al., 2022）为代表的扩散方法，在文本到运动（text-to-motion）、动作到运动（action-to-motion）和音乐到舞蹈（music-to-dance）等任务上取得了显著进展。

然而，这些方法的成功高度依赖于一个关键前提：训练数据必须同时具备高质量的运动序列和精确的对应标注（如文本描述、动作类别或音乐节拍对齐）。这一前提在实际应用中构成了根本性瓶颈。

### 核心瓶颈：标注数据的稀缺与噪声

获取大规模高质量标注运动数据成本极为高昂。专业运动捕捉设备昂贵、场地受限，而人工标注运动序列的文本描述或动作类别又耗时费力。现实世界中虽然存在大量运动数据，但它们往往以两种“不完美”形式存在：

1. **含噪标注数据（noisy annotated motions）**：运动序列本身质量尚可，但其文本或类别标注存在错误、模糊或不匹配。例如，一段“行走”的运动被错误标注为“跑步”，或音乐舞蹈数据的节拍对齐存在偏差。
2. **无标注干净数据（clean unannotated motions）**：运动序列质量很高，但完全缺乏对应的控制标注，无法直接用于条件生成训练。

现有方法要么完全依赖干净标注数据（导致数据利用率极低），要么在含噪数据上直接训练（导致条件控制能力下降），始终无法有效利用这两种广泛存在的数据资源。这一矛盾构成了领域内的核心瓶颈：**如何在弱监督条件下，同时利用含噪标注数据和无标注干净数据，训练出可控运动生成模型？**

### 现有方法的缺口

传统全监督方法（如 MDM、MotionDiffuse、EDGE）要求所有训练样本均为干净且标注的数据，在整个扩散去噪时间步 $[1, T]$ 上统一训练。当面临数据质量下降时，这些方法缺乏应对机制：

- 若将含噪标注数据直接混入训练，噪声标注会误导条件控制的学习，导致生成动作与给定条件不匹配。
- 若仅使用干净未标注数据，模型将退化为无条件生成器，完全丧失可控性。
- 若丢弃不完美数据，则浪费了大量可用的运动信息，限制了模型对运动分布的学习广度。

部分工作尝试通过数据清洗或半监督学习缓解此问题，但这些方法通常需要额外的标注校正步骤或复杂的多阶段训练流程，未能从根本上解决扩散模型在弱监督数据下的训练难题。

### 本文动机与核心洞察

本文提出的 **MotionMix** 方法，源于对扩散模型去噪过程本质的重新审视。扩散模型的去噪过程是逐步的：在初始的高噪声时间步，模型主要恢复运动的粗略结构；在后续的低噪声时间步，模型逐步精炼细节。这一分步特性暗示了一个关键可能性：**不同质量的数据可以在不同的去噪阶段发挥作用，彼此互不干扰**。

具体而言，含噪标注数据虽然标注不精确，但足以在早期去噪阶段提供粗略的条件控制信号，让模型学会“大致朝哪个方向生成”；而干净未标注数据虽然缺乏条件信息，但其高质量的运动细节可以在后期去噪阶段精炼生成结果，提升运动的自然度和真实性。两者通过扩散时间步的自然划分，可以实现有机协同。

基于这一洞察，MotionMix 将扩散模型的去噪训练分配为两个阶段：在初始 $T - T^*$ 步使用含噪标注数据学习条件控制，在最后 $T^*$ 步使用干净未标注数据进行无条件精炼。这一设计无需额外标注校正，不引入复杂训练流程，仅通过时间步的分配策略，便实现了弱监督下的可控运动生成，为充分利用现实世界中大量不完美运动数据开辟了新路径。

## 核心方法与创新机理

MotionMix 的核心创新在于**将扩散模型的去噪过程按时间步拆分为两个阶段，从而在弱监督条件下实现可控运动生成**。其关键洞察是：扩散模型的分步去噪特性天然允许在不同时间步使用不同质量的数据——含噪数据在早期提供粗略的条件控制，干净数据在后期提升细节质量，两者互不干扰。

### 关键改进槽位

#### 1. 训练数据分配与去噪步范围

**基线做法**：所有训练样本均为干净且标注的数据，在整个时间步 $[1, T]$ 上统一训练。

**MotionMix 做法**：将训练数据分为两个子集，并分配不同的去噪时间步范围：
- **含噪标注样本**：仅在 $[T^*+1, T]$ 步训练，携带条件 $c$（如文本、音乐特征）。噪声通过前向扩散过程施加，噪声步从 $[T_1, T_2]$ 中随机采样。
- **干净未标注样本**：仅在 $[1, T^*]$ 步训练，条件输入替换为 $c = \emptyset$。

其中 $T^*$ 为“去噪枢轴”（denoising pivot），是划分两阶段的关键超参数。这一设计的核心机制在于：含噪数据在扩散初期（高噪声阶段）提供足够的条件信号以建立粗略的运动结构，而干净数据在扩散后期（低噪声阶段）负责精细化的无条件精炼，两者在时间步上互不重叠，避免了噪声与干净信号之间的冲突。

#### 2. 推理阶段的条件输入切换

**基线做法**：整个去噪过程中使用原始条件 $c$（或结合无分类器引导的空条件）。

**MotionMix 做法**：在采样过程中，当去噪步达到枢轴 $T^*$ 时，将条件输入替换为 $c = \emptyset$，实现从条件引导到无条件精炼的切换。结合无分类器引导的采样公式为：

$$\hat{\mathbf{s}}(\mathbf{x}_t, t, c) = w \cdot f_{\theta}(\mathbf{x}_t, t, c) + (1 - w) \cdot f_{\theta}(\mathbf{x}_t, t, \emptyset)$$

在 $t > T^*$ 阶段使用条件 $c$ 进行引导，在 $t \leq T^*$ 阶段则令 $c = \emptyset$，仅依赖无条件模型完成最终的精炼。

### 方法优势

这一两阶段设计带来了三个层面的优势：

1. **数据效率**：无需大规模高质量标注数据，仅需一半含噪标注数据和一半干净未标注数据即可达到与全监督基线竞争甚至更优的性能。例如，MDM (MotionMix) 在 HumanML3D 上 FID 降低 30.0%（从 0.544 降至 0.381），EDGE (MotionMix) 在 AIST++ 音乐到舞蹈任务上 PFC 提升 43.1%、Distk 提升 95.0%。

2. **骨干无关性**：MotionMix 是一种训练范式而非特定模型架构，可无缝应用于不同的扩散模型骨干，包括 **MDM** (Tevet et al., 2022)、**MotionDiffuse** (Zhang et al., 2022) 和 **EDGE** (Tseng et al., 2022)，均取得一致性的提升。

3. **鲁棒性**：消融实验表明，较高的含噪比例（50–70%）持续优于较低比例，说明更广泛的条件信号访问有利于生成质量；方法对不同噪声水平也表现出合理的稳定性。

### 局限性

- 去噪枢轴 $T^*$ 和噪声范围 $[T_1, T_2]$ 需手动调节，缺乏自动化选择策略。
- 仅对高斯扩散噪声有效，对更复杂的现实噪声类型未验证。
- 在小型数据集（如 HumanAct12）上性能可能下降，方法更适用于大规模数据场景。
- 两阶段采样引入了额外的推理步骤切换，可能略微影响推理效率。

MotionMix 通过重新分配扩散模型的去噪目标，将弱监督信号注入标准扩散范式，形成“条件粗糙生成→无条件精炼”的两阶段流水线。整体框架由数据拆分与加噪、两阶段训练、两阶段采样三个核心模块串联而成，骨干扩散模型可替换。

### 核心机制：去噪步分配

扩散模型的去噪过程天然具有从粗到细的特性：高噪声步（$t$ 接近 $T$）负责恢复全局结构，低噪声步（$t$ 接近 $1$）负责细化局部细节。MotionMix 利用这一特性，将去噪步范围 $[1, T]$ 以去噪枢轴 $T^*$ 为界切分为两段：

- **条件粗糙生成阶段**（$t \in [T^*+1, T]$）：模型在含噪标注数据上训练，输入条件 $c$（如文本描述、音乐特征），学习从强噪声中恢复与条件语义对齐的粗略运动骨架。
- **无条件精炼阶段**（$t \in [1, T^*]$）：模型在干净未标注数据上训练，条件输入置为 $\emptyset$，专注于提升运动的物理合理性和细节质量。

两阶段共享同一模型参数，仅在训练时根据样本类型分配不同的时间步范围，推理时则按序切换条件输入。这一设计使得含噪标注数据提供语义控制信号，干净未标注数据提供运动先验，两者互不干扰。

### 数据拆分与加噪

给定一个原始标注数据集，MotionMix 将其随机划分为两个子集：

1. **含噪标注子集**：保留原始条件标注 $c$，对运动序列施加扩散前向过程（Equation 1）的噪声，噪声步从范围 $[T_1, T_2]$ 中随机采样。该子集模拟现实世界中含噪声的标注数据。
2. **干净未标注子集**：保持运动序列的原始质量，但丢弃条件标注（训练时以 $c = \emptyset$ 替代）。该子集模拟大规模无标注运动数据。

两个子集的比例、噪声注入范围 $[T_1, T_2]$ 和去噪枢轴 $T^*$ 是方法的关键超参数，消融实验（Table 4–6）表明这些参数在合理范围内具有较好的鲁棒性。

### 训练流程

训练时，每个 batch 混合含噪样本和干净样本，分别采样不同的去噪步：

- 对于含噪样本：$t \sim \text{Uniform}[T^*+1, T]$，条件输入为 $c$。
- 对于干净样本：$t \sim \text{Uniform}[1, T^*]$，条件输入为 $\emptyset$。

模型通过统一的简单扩散损失 $\mathcal{L}_{\text{simple}}$（Equation 2）优化，无需额外的损失项或对抗训练。

### 推理流程

推理时采用两阶段采样策略：

1. **条件引导阶段**（$t = T \to T^*$）：使用无分类器引导（Equation 3），以权重 $w$ 融合条件输出和无条件输出，确保生成的运动与条件语义对齐。
2. **无条件精炼阶段**（$t = T^* \to 1$）：到达枢轴 $T^*$ 后，将条件输入替换为 $c = \emptyset$，模型仅依赖运动先验完成剩余去噪，细化运动细节。

### 骨干模型兼容性

MotionMix 的方法设计独立于具体扩散架构，论文在三个代表性骨干上验证了兼容性：

- **MDM**（Tevet et al., 2022）：用于文本到运动（text-to-motion）和动作到运动（action-to-motion）任务。
- **MotionDiffuse**（Zhang et al., 2022）：用于文本到运动任务。
- **EDGE**（Tseng et al., 2022）：用于音乐到舞蹈（music-to-dance）任务，使用预训练 Jukebox 模型提取音频特征作为条件。

三个骨干均通过相同的两阶段训练/采样策略适配 MotionMix，无需修改网络结构，仅需调整数据加载和时间步采样逻辑。

### 输入输出规范

- **输入**：
  - 含噪标注数据：运动序列 $\mathbf{x}$（施加 $[T_1, T_2]$ 步噪声）、条件 $c$（文本嵌入/动作类别/音乐特征）
  - 干净未标注数据：运动序列 $\mathbf{x}$（原始质量）、条件 $c = \emptyset$
- **输出**：与条件 $c$ 语义对齐且物理合理的运动序列 $\hat{\mathbf{x}}$
- **运动表示**：根据任务不同采用差异化表示，如 HumanML3D 使用 263 维姿态向量，AIST++ 使用 151 维拼接表示（接触标签 + 根位移 + 姿态）

### 3.1 扩散模型基础

MotionMix 建立在标准扩散模型框架之上。给定一个干净的运动序列 $\mathbf{x}_0$，前向扩散过程逐步向其注入高斯噪声，得到一系列噪声版本 $\mathbf{x}_1, \mathbf{x}_2, \ldots, \mathbf{x}_T$。该过程的后验分布定义为：

$$q(\mathbf{x}_t | \mathbf{x}_0) = \mathcal{N}(\mathbf{x}_t; \sqrt{\bar{\alpha}_t} \mathbf{x}_0, (1 - \bar{\alpha}_t) \mathbf{I})$$

其中 $\bar{\alpha}_t$ 是噪声调度参数，控制第 $t$ 步的噪声强度。反向去噪过程由一个参数为 $\theta$ 的神经网络 $f_\theta$ 建模，其训练目标是最小化简单损失函数：

$$\mathcal{L}_{\mathrm{simple}} = \mathbb{E}_{t \sim [1, T], \mathbf{s}_t} \big[ \| \mathbf{s}_t - f_{\theta}(\mathbf{x}_t, t, c) \|^2 \big]$$

这里 $\mathbf{s}_t$ 是注入的噪声，$c$ 是条件信号（如文本描述、动作类别或音乐特征）。该公式是 MotionMix 训练框架的数学基础，但其核心创新在于对训练过程中时间步 $t$ 和条件 $c$ 的差异化分配。

### 3.2 两阶段训练机制

MotionMix 的核心模块是**去噪时间步分配器**。它引入一个关键超参数——去噪枢轴 $T^*$，将扩散模型的 $T$ 个去噪步划分为两个互不重叠的区间：

- **条件近似阶段**（$t \in [T^*+1, T]$）：模型使用**含噪标注数据**训练。这些样本保留了原始条件标注 $c$，但运动序列本身被注入了噪声（通过前向扩散过程添加随机步噪声）。模型在此阶段学习从高噪声状态中恢复出满足条件约束的粗略运动结构。

- **无条件精炼阶段**（$t \in [1, T^*]$）：模型使用**干净未标注数据**训练。这些样本的运动序列保持原始质量，但条件输入被替换为空条件 $c = \emptyset$。模型在此阶段学习从低噪声状态中精炼运动细节，提升生成质量。

两阶段训练的损失函数保持统一形式，区别仅在于训练样本的采样范围与条件输入：

- 对含噪标注样本：$t \sim [T^*+1, T]$，$c$ 为原始条件
- 对干净未标注样本：$t \sim [1, T^*]$，$c = \emptyset$

### 3.3 两阶段采样机制

在推理阶段，MotionMix 采用**条件切换采样器**。采样过程从纯噪声 $\mathbf{x}_T \sim \mathcal{N}(0, \mathbf{I})$ 开始，逐步去噪至 $\mathbf{x}_0$。关键机制在于到达枢轴 $T^*$ 时的条件切换：

- 当 $t > T^*$ 时，使用无分类器引导（classifier-free guidance）进行条件采样：

$$\hat{\mathbf{s}}(\mathbf{x}_t, t, c) = w \cdot f_{\theta}(\mathbf{x}_t, t, c) + (1 - w) \cdot f_{\theta}(\mathbf{x}_t, t, \emptyset)$$

其中 $w$ 是引导强度权重，控制条件控制的力度。

- 当 $t \leq T^*$ 时，条件输入被强制替换为 $c = \emptyset$，即完全退化为无条件精炼。此时采样公式简化为 $\hat{\mathbf{s}} = f_{\theta}(\mathbf{x}_t, t, \emptyset)$。

这一设计保证了推理过程与训练过程的一致性：模型在训练时从未见过 $t \in [1, T^*]$ 区间的条件信号，因此在推理时也不应在此区间使用条件引导。

### 3.4 数据拆分与噪声注入模块

为构建弱监督训练环境，MotionMix 将原始数据集随机划分为两个子集：

- **含噪标注子集**：保留条件标注 $c$，但运动序列 $\mathbf{x}_0$ 通过前向扩散过程（公式 $q(\mathbf{x}_t | \mathbf{x}_0)$）被注入随机步噪声。噪声注入的步数从区间 $[T_1, T_2]$ 中随机采样，该区间是可调节的超参数。

- **干净未标注子集**：运动序列保持原始质量，但条件标注被丢弃（训练时使用 $c = \emptyset$）。

这一模块的关键洞察在于：扩散模型天然容忍不同质量的数据在不同时间步上训练，因为高噪声步关注全局结构，低噪声步关注局部细节。两者互不干扰，使得弱监督训练成为可能。

### 3.5 运动表征

MotionMix 本身是模型无关的框架，可适配不同的扩散模型骨干。不同任务采用不同的运动表征：

- **文本到动作**：运动序列表示为 $\mathbf{x} \in \mathbb{R}^{N \times D}$，其中 $N$ 是帧数，$D$ 是每帧的姿态向量维度（HumanML3D 为 263，KIT-ML 为 251）。该表征拼接了根关节速度、根关节高度、局部关节位置、速度、旋转以及足部接触标签。

- **动作到动作**：运动序列表示为 $\mathbf{x} = \mathrm{Concat}([\mathbf{p}, \mathbf{r}]) \in \mathbb{R}^{N \times 25 \times 6}$，其中 $\mathbf{p}$ 是 24 关节 SMPL 姿态参数，$\mathbf{r}$ 是根关节平移。

- **音乐到舞蹈**：运动序列表示为 $\mathbf{x} = \mathrm{Concat}([\mathbf{b}, \mathbf{r}, \mathbf{p}]) \in \mathbb{R}^{N \times 151}$，其中 $\mathbf{b}$ 是二值足部接触标签（从 $\mathbf{p}$ 和 $\mathbf{r}$ 计算得出，因此不直接对其注入噪声），$\mathbf{r}$ 是根关节平移，$\mathbf{p}$ 是姿态参数。噪声同时注入 $\mathbf{p}$ 和 $\mathbf{r}$，使用从 $[20, 80]$ 采样的相同噪声步。

## 实验与关键发现

### 核心实验设置

MotionMix 在三个主流运动生成任务上验证其弱监督框架的有效性：文本到运动（Text-to-Motion）、动作到运动（Action-to-Motion）和音乐到舞蹈（Music-to-Dance）。实验的核心设置如下：

- **数据拆分策略**：将原始训练集随机分为两个等量子集。一个子集保留标注条件，但通过前向扩散过程（Equation 1）向运动序列注入噪声，噪声步从范围 $[T_1, T_2]$ 随机采样；另一个子集保留干净的运动数据，但将条件输入替换为空条件 $c = \emptyset$。
- **骨干模型**：MotionMix 作为即插即用的训练框架，分别集成到三个主流扩散模型骨干中——**MDM**（Tevet et al., 2022）、**MotionDiffuse**（Zhang et al., 2022）和 **EDGE**（Tseng et al., 2022）。
- **运动表示**：文本到运动任务采用冗余运动表示，拼接根速度、根高度、局部关节位置、速度、旋转和足部接触标签，HumanML3D 上维度为 $D=263$，KIT-ML 上为 $D=251$。音乐到舞蹈任务使用 $\mathbf{x} = \mathrm{Concat}([\mathbf{b}, \mathbf{r}, \mathbf{p}]) \in \mathbb{R}^{N \times 151}$，其中 $\mathbf{b}$ 为足部接触标签，$\mathbf{r}$ 为根位移，$\mathbf{p}$ 为姿态。
- **评估指标**：采用 FID（Fréchet Inception Distance）、R Precision、Multimodal Distance、Diversity、Multimodality（文本到运动）；Accuracy、FID、Diversity、Multimodality（动作到运动）；FID、Beat Alignment、PFC（Physical Foot Contact）、Dist$_k$（音乐到舞蹈）。所有评估运行 20 次（Multimodality 运行 5 次），报告 95% 置信区间。

---

### 文本到运动主结果

**表 1** 展示了在 HumanML3D 和 KIT-ML 测试集上的定量对比。MotionMix 在仅使用一半含噪标注数据和一半干净未标注数据的弱监督条件下，显著超越或匹敌使用全部干净标注数据训练的全监督基线。

**关键发现**：
- **MDM (MotionMix)** 在 HumanML3D 上取得 FID = $0.381 \pm 0.042$，相比 MDM 基线的 $0.544 \pm 0.440$ 降低 **30.0%**；在 KIT-ML 上 FID 从 $0.497 \pm 0.021$ 降至 $0.322 \pm 0.020$，提升 **35.2%**。这表明含噪标注数据的条件信号在早期去噪步提供了有效的粗粒度控制，而干净未标注数据在后期精炼阶段提升了运动细节质量。
- **MotionDiffuse (MotionMix)** 同样在两项基准上取得有竞争力的结果，验证了 MotionMix 对多种扩散骨干的泛化性。
- 值得注意，基线模型（MDM、MotionDiffuse、**MLD** (Chen et al., 2022)、**Guo et al.** (CVPR 2022) 等）均使用全部高质量标注数据训练，而 MotionMix 仅在弱监督数据下即实现更优或可比性能，这直接验证了核心洞察：扩散模型的分步去噪特性天然允许不同质量数据在不同时间步发挥互补作用。

---

### 动作到运动主结果

**表 2** 展示了在 HumanAct12 和 UESTC 数据集上的结果。MotionMix 在 UESTC 上表现优异，但在 HumanAct12 上出现性能下降，这是论文明确指出的**失败模式**。

**关键发现**：
- 在较大规模的 UESTC 数据集上，MDM (MotionMix) 以更少的高质量标注数据取得有竞争力的性能。
- 在小型数据集 HumanAct12 上，MotionMix 性能劣于全监督基线。论文将此归因于方法更适用于大规模数据场景——小数据集上干净未标注样本数量有限，无条件精炼阶段的训练信号不足，导致细节生成质量下降。这一局限性在**表 2** 中明确体现，需要在应用时根据数据规模审慎评估。

---

### 音乐到舞蹈主结果

**表 3** 展示了在 AIST++ 测试集上的结果，这是 MotionMix 优势最为显著的实验场景。

**关键发现**：
- **EDGE (MotionMix)** 在所有指标上显著优于重新训练的 EDGE 基线。其中 **PFC 提升 43.1%**，**Dist$_k$ 提升 95.0%**，Beat Alignment 从 $0.224 \pm 0.025$ 提升至 $0.256 \pm 0.013$（↑13.3%）。
- PFC（Physical Foot Contact）的大幅提升表明，干净未标注数据在后期精炼阶段有效消除了含噪标注数据可能引入的物理伪影（如滑步），使生成舞蹈的足部接触更加物理真实。
- Dist$_k$ 的 95% 相对提升说明无条件精炼阶段增强了生成动作的多样性，避免了条件过拟合导致的模式坍塌。
- 该实验的噪声注入范围为 $[20, 80]$，噪声同时施加于姿态 $\mathbf{p}$ 和根位移 $\mathbf{r}$，而足部接触标签 $\mathbf{b}$ 由前两者计算得出，故不直接注入噪声。

---

### 定性分析

**图 3** 展示了基线 MDM 和 MotionDiffuse 与 MotionMix 变体的定性对比。在给定文本提示（如 "a person walks forward then turns around"）下，MotionMix 生成的运动序列在时序连贯性和语义对齐度上均优于仅使用高质量标注数据训练的基线。这进一步佐证了定量结果：弱监督框架不仅未因数据质量下降而受损，反而通过两阶段去噪获得了更鲁棒的条件控制与更自然的运动细节。

---

### 消融实验

所有消融实验均在 HumanML3D 测试集上以 MDM 为骨干进行，系统分析了三个关键超参数的影响。

#### 去噪枢轴 $T^*$ 的影响

**表 4** 评估了四个 $T^*$ 取值（$T^* = 40, 50, 60, 70$）。**$T^* = 60$ 在所有指标上取得最优**：R Precision = 0.632，FID = 0.381，Multimodal Distance = 5.325。

**因果解释**：$T^*$ 决定了条件控制与无条件精炼的边界。过小的 $T^*$（如 40）意味着条件控制步过少，模型无法从含噪标注数据中充分学习条件映射，导致语义对齐下降；过大的 $T^*$（如 70）则压缩了无条件精炼空间，干净未标注数据的细节优化作用减弱，FID 回升。$T^* = 60$ 在 HumanML3D 上实现了两者的最优平衡。

#### 含噪与干净数据比例的影响

**表 5** 评估了含噪数据比例从 30% 到 70% 的五种配置。**50% 含噪比例取得最佳 R Precision 和 Multimodal Dist；70% 含噪比例取得最佳 FID = 0.359**。

**因果解释**：较高的含噪比例（50–70%）一致优于较低比例（30%），表明更广泛的条件信号访问有利于模型学习鲁棒的条件映射。但 70% 含噪比例下 R Precision 略有下降，说明过度压缩干净数据会削弱精炼阶段的细节优化能力。50% 比例在语义对齐和生成质量间取得最佳折中。

#### 噪声范围 $[T_1, T_2]$ 的影响

**表 6** 分为上下两个模块消融。上模块固定范围跨度，比较 $[20,40]$、$[20,60]$、$[20,80]$；下模块固定 $T_2$ 或 $T_1$，评估不同噪声水平的影响。

**关键发现**：
- **$[20,60]$ 整体表现最优**，优于更窄的 $[20,40]$ 和更宽的 $[20,80]$。这表明适中的噪声范围既能提供足够的条件扰动以模拟真实含噪数据，又不会因过度噪声破坏条件信号的可辨识性。
- 论文明确指出：“neither smaller value of $T_1$, $T_2$ nor small $T_2 - T_1$ relates to better final performance”，即更小的噪声值或更窄的噪声范围并不自动带来更好性能，需要根据数据集特性手动调节。
- 下模块显示 MotionMix 对噪声水平的变化具有**合理稳定性**，但并非完全鲁棒——这构成了方法的另一个局限性。

---

### 失败模式与局限性

1. **小数据集性能下降**：在 HumanAct12 等小型数据集上，MotionMix 性能劣于全监督基线。原因在于干净未标注样本数量不足，无条件精炼阶段的训练信号有限，导致运动细节生成质量下降。
2. **超参数敏感性与手动调节负担**：去噪枢轴 $T^*$ 和噪声范围 $[T_1, T_2]$ 对性能有显著影响，且最优取值依赖于数据集特性。当前缺乏自动化或自适应的选择策略，需要针对每个新数据集进行手动搜索。
3. **噪声模型假设限制**：方法基于高斯扩散噪声（Equation 1）近似真实含噪数据。对于更复杂的现实噪声类型（如传感器噪声、遮挡导致的缺失数据），两阶段训练的有效性尚未验证。
4. **推理效率的轻微损失**：两阶段采样在达到 $T^*$ 时需要切换条件输入为 $c = \emptyset$，引入额外的推理步骤切换，可能略微影响推理效率，尽管论文未量化这一开销。

---

### 真实场景验证

**表 7**（附录）展示了更贴近真实应用场景的实验：将 AIST++ 作为含噪标注数据源，AMASS 作为干净未标注数据源，混合训练 EDGE (MotionMix)。结果表明，即使两个数据集来自不同分布，MotionMix 仍能有效利用未标注数据提升生成质量，验证了框架在真实弱监督场景下的实用价值。

![[assets/figures/papers/paper_list_l1818_MotionMix_Weakly_Supervised_Diffusion_for_Controllable_Motion_Generation/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative performance of baseline MDM and MotionDiffuse models, trained exclusively on high-quality annotated data, with our MotionMix approach, which learns from imperfect data sources. Their visualized motion results are presented alongside real references for three distinct text prompts. Please refer to supplementary files for more animations*

![[assets/figures/papers/paper_list_l1818_MotionMix_Weakly_Supervised_Diffusion_for_Controllable_Motion_Generation/figures/004_Table_1.jpg]]
*Table 1: Quantitative results of text-to-motion on the test set of HumanML3D and KIT-ML. Note all baselines are trained with gold data. We run all the evaluation 20 times (except Multimodality runs 5 times) and ± indicates the 95% confidence interval. ↑ means higher is better, ↓ means lower is better, → means closer to the real distribution is better. The*

![[assets/figures/papers/paper_list_l1818_MotionMix_Weakly_Supervised_Diffusion_for_Controllable_Motion_Generation/figures/005_Table_2.jpg]]
*Table 2: Quantitative results of action-to-motion on the HumanAct12 dataset and UESTC test set. We run the evaluation 20 times, and the metric details are similar to Table 1*

![[assets/figures/papers/paper_list_l1818_MotionMix_Weakly_Supervised_Diffusion_for_Controllable_Motion_Generation/figures/006_Table_3.jpg]]
*Table 3: Quantitative results of music-to-dance on the AIST++ test set. We run the evaluation 20 times, and the metric details are similar to Table 1. † denotes the EDGE model that is re-trained by us.1*

![[assets/figures/papers/paper_list_l1818_MotionMix_Weakly_Supervised_Diffusion_for_Controllable_Motion_Generation/figures/007_Table_4.jpg]]
*Table 4: We evaluate MDM (MotionMix) on the HumanML3D test set using different values of the denoising pivot*

![[assets/figures/papers/paper_list_l1818_MotionMix_Weakly_Supervised_Diffusion_for_Controllable_Motion_Generation/figures/010_Table_7.jpg]]
*Table 7: Quantitative results of music-to-dance on the AIST++ test set. We run the evaluation 20 times. The best and the second best result are bold and underlined respectively. † denotes the EDGE model that is re-trained by us*

## 定位与知识库关联

### 在扩散生成谱系中的位置

MotionMix 并非提出新的扩散架构，而是提出一种**训练策略层面的弱监督范式**，可叠加于现有扩散骨干之上。论文在三种主流骨干上验证了该策略：**MDM**（Tevet et al., 2022）、**MotionDiffuse**（Zhang et al., 2022）和 **EDGE**（Tseng et al., 2022）。这些骨干在标准全监督设定下均要求全部训练样本同时具备干净的运动序列和精确的条件标注（文本、动作类别或音乐特征）。MotionMix 的核心改动在于**训练数据分配与去噪步范围**的重新划分：含噪标注样本仅在 $[T^*+1, T]$ 步训练并携带条件 $c$，干净未标注样本仅在 $[1, T^*]$ 步训练且条件置为 $\emptyset$。推理阶段则对应地采用两阶段采样——在达到去噪枢轴 $T^*$ 后切换条件输入为 $\emptyset$ 进行无条件精炼。

这一设计根植于扩散模型的分步去噪特性：早期高噪声步主要恢复全局粗结构，后期低噪声步负责细节精炼。MotionMix 利用该特性，让含噪标注数据在早期提供粗粒度的条件控制信号，而让干净未标注数据在后期提升生成质量，两者在时间步上解耦，互不干扰。

### 与相关弱监督/半监督方法的对比

在运动生成领域，已有工作探索了不同形式的标注稀缺问题。**Language2Pose**（Ahuja et al., 2019）和 **Text2Gestures**（Bhattacharya et al., 2021）采用自编码器或检索式方法处理文本到姿态映射，但生成多样性和质量受限。**Guo et al.**（CVPR 2022）和 **MLD**（Chen et al., 2022）虽改进了生成质量，仍依赖全量干净标注数据训练扩散模型。MotionMix 的独特之处在于**同时利用含噪标注和干净未标注两类不完美数据**，且无需任何高质量标注样本即可达到与全监督基线竞争的性能——在 HumanML3D 上，MDM + MotionMix 的 FID 为 0.381，优于全监督 MDM 的 0.544（↓30.0%），而训练仅使用一半含噪标注数据和一半干净未标注数据。

### 适用边界与局限

**适用场景**：方法在数据规模较大的基准上表现突出。在 HumanML3D 和 KIT-ML（文本到动作）以及 AIST++（音乐到舞蹈）上均取得显著提升。消融实验表明，较高的含噪比例（50%–70%）持续优于较低比例，说明该方法能从更广泛的条件访问中获益。

**已知局限**：
1. **小数据集退化**：在 HumanAct12 等小型数据集上性能可能下降，方法更适用于大规模数据场景。
2. **超参数敏感**：噪声范围 $[T_1, T_2]$ 和去噪枢轴 $T^*$ 需手动调节。消融显示 $T^*=60$ 在 R Precision 和 FID 上综合最优，$[20, 60]$ 的噪声范围整体最佳，但这些取值可能因数据集和骨干而异，缺乏自动化选择策略。
3. **噪声模型假设**：方法依赖高斯扩散噪声近似真实世界噪声。论文通过前向扩散过程（公式 1）向干净样本注入噪声来模拟含噪数据，对更复杂的非高斯现实噪声类型未经验证。
4. **推理效率**：两阶段采样在 $T^*$ 处需切换条件输入，引入额外的推理步骤切换，可能略微影响推理效率，但论文未对此进行定量分析。

### 开放问题

1. **自适应枢轴选择**：能否根据数据集特性自动或自适应地选择 $T^*$？当前依赖网格搜索，限制了方法在新场景下的即插即用能力。
2. **跨模态扩展**：两阶段训练策略是否可推广到图像、音频等其他生成任务？扩散模型的分步特性具有通用性，但不同模态的噪声-语义对应关系可能不同。
3. **非高斯噪声鲁棒性**：在更复杂的现实噪声模型下，当前基于高斯扩散噪声的近似策略是否仍然有效？这直接关系到方法在实际部署中的适用性。
4. **少量高质量数据的利用**：当前设定假设零高质量标注样本。若存在少量高质量标注数据，能否通过半监督或主动学习策略进一步利用这些样本提升性能？论文在附录中尝试了结合 AIST++ 和 AMASS 的真实场景实验（Table 7），但未系统探索高质量样本的增量价值。

## 原文 PDF

![[paperPDFs/AAAI_2024/MotionMix_Weakly_Supervised_Diffusion_for_Controllable_Motion_Generation.pdf]]
