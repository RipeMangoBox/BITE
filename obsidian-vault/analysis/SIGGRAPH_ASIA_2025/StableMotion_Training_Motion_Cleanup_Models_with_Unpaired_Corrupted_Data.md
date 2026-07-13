---
title: "StableMotion: Training Motion Cleanup Models with Unpaired Corrupted Data"
type: paper
paper_level: A
venue: "SIGGRAPH Asia"
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2025/StableMotion_Training_Motion_Cleanup_Models_with_Unpaired_Corrupted_Data.pdf
code_link: null
project_link: https://yxmu.foo/stablemotion-page/
aliases:
- StableMotion
tags:
- SIGGRAPH_ASIA_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "帧级质量指示变量(QualVar)，通过联合训练生成-判别扩散模型，使模型能根据指定质量生成运动，从而在测试时通过设定高质量指示变量生成干净运动。"
primary_logic: "将运动清理转化为一种质量可控的条件生成问题：通过引入质量指示变量并设计生成-判别联合训练框架，模型既能评估运动质量又能根据质量提示生成运动，从而在无需配对数据的情况下从混合质量数据中学习清理能力。"
claims:
- "引入帧级质量指示变量(QualVar)使模型能从混合质量数据学习清理能力。"
- "在SoccerMocap上将运动pops减少68%，冻结帧减少81%。"
- "在BrokenAMASS基准上，StableMotion训练的模型超越使用干净或配对数据训练的SOTA方法。"
- "移除质量指示变量后模型性能显著下降，证明QualVar是关键设计。"
---

# StableMotion: Training Motion Cleanup Models with Unpaired Corrupted Data

> [!tip] 核心洞察
> 将运动清理转化为一种质量可控的条件生成问题：通过引入质量指示变量并设计生成-判别联合训练框架，模型既能评估运动质量又能根据质量提示生成运动，从而在无需配对数据的情况下从混合质量数据中学习清理能力。

| 字段      | 内容                                                                                                     |
| ------- | ------------------------------------------------------------------------------------------------------ |
| 中文题名    | StableMotion: 使用不配对损坏数据训练运动清理模型                                                                        |
| 英文题名    | StableMotion: Training Motion Cleanup Models with Unpaired Corrupted Data                              |
| 会议/期刊   | SIGGRAPH Asia 2025                                                                                     |
| Links   | [paper](https://arxiv.org/abs/2505.03154) · [Project](https://yxmu.foo/stablemotion-page/)              |
| Topic   | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method  | StableMotion                                                                                           |
| Dataset | SoccerMocap, BrokenAMASS                                                     |

> [!tip] 效果简介
> - SoccerMocap 上，Foot Skating Dist (FS Dist) 为 2.14，对比 6.42 (Input)，变化 -66.7%。
> - SoccerMocap 上，Pops Rate 为 0.13%，对比 0.41% (Input)，变化 -68.3%。
> - SoccerMocap 上，Frozen Rate 为 4.50%，对比 23.68% (Input)，变化 -81.0%。

## 概要
### 问题背景

动作捕捉（mocap）是动画、游戏和影视制作的核心技术，但实际采集的原始数据常因传感器遮挡、信号干扰或算法误差而包含多种运动伪影——如足部滑步、冻结帧、关节抖动和异常穿透。现有数据驱动的运动清理方法普遍依赖**配对的干净-损坏数据**进行监督训练，而在实际生产环境中获取域内配对数据的成本极高：这要求专业人员逐帧手工修复或借助昂贵的物理模拟系统，难以规模化。直接丢弃损坏片段则会破坏时序连续性，导致模型无法学习长时运动动态。

### 核心贡献

**StableMotion**（SIGGRAPH Asia 2025）提出了一种全新的运动清理范式：**仅使用不配对的混合质量原始数据训练运动清理模型**，从而从根本上绕过了对配对标注的依赖。其核心洞察是将运动清理重新定义为一种**质量可控的条件生成问题**——引入帧级质量指示变量（QualVar），并设计生成-判别联合训练框架，使单一模型同时具备两项能力：评估每帧的运动质量，以及根据指定的质量水平生成对应质量的运动。测试时，模型通过“质量提示”（quality prompting）即可自动识别并修复损坏帧。

这一框架的关键因果杠杆在于：QualVar 变量在训练时编码了数据中不同质量水平的分布信息，模型由此学会将“高质量指示”映射到干净的运动生成，从而在无需配对监督的情况下从混合质量数据中习得清理能力。

### 方法定位

StableMotion 在方法谱系中处于**条件扩散生成**与**自监督运动修复**的交叉点。与现有方法的本质区别如下：

| 维度     | 现有方法                        | StableMotion               |
| ------ | --------------------------- | -------------------------- |
| 训练数据要求 | 需要配对的干净-损坏数据（如 XClean、RoHM） | 仅需混合质量的原始数据，无需配对           |
| 质量控制机制 | 无显式质量控制，或仅基于输入特征            | 帧级质量指示变量 QualVar，可显式控制生成质量 |
| 模型范式   | 单独的运动生成或分类模型                | 统一的生成-判别联合扩散模型             |
| 测试时策略  | 固定步数扩散修复                    | 基于软质量估计的自适应修复 + 质量感知集成     |

在技术路线上，StableMotion 与基于物理模拟的方法（如 **PHC**，Luo et al., 2023）形成互补：物理方法擅长修正物理不可行伪影但可能引入新的抖动，而 StableMotion 可进一步清理这些残留伪影。与条件运动扩散修复方法（如 CondMDI-B）相比，StableMotion 的质量条件变量设计使其能在推理时灵活控制修复强度。

### 主要结果

在真实工业场景的 **SoccerMocap** 数据集上，StableMotion 实现了显著的伪影清理效果：

- **运动突变（Pops）减少 68%**：Pops Rate 从 0.41% 降至 0.13%
- **冻结帧（Frozen frames）减少 81%**：Frozen Rate 从 23.68% 降至 4.50%
- **足部滑步（Foot Skating）减少 67%**：FS Dist 从 6.42 降至 2.14

在合成基准 **BrokenAMASS** 上，StableMotion 训练的模型**超越了使用干净数据或配对数据训练的最先进方法**：相比 RoHM，足滑距离（FS Dist）降低 16.5%（3.70 vs 4.43），加速度误差（Accel）降低 40%（0.60 vs 1.00）。

消融实验证实了 QualVar 的关键作用：移除质量指示变量后，足滑率（FS Rate）从 3.60% 显著上升至 6.37%。自适应清理技术将内容保留指标 GMPJPE 从 3.59 cm 改善至 2.21 cm，质量感知集成进一步将 FS Dist 从 3.44 降至 3.31。模型在视觉动捕数据（IDEA400）和物理模拟角色（PHC-Tracking）等域外数据上也展现了良好的泛化能力。

### 局限与展望

当前方法仍需人工标注或启发式算法提供初始质量指示变量，尤其对细微伪影的检测尚未完全自动化。软阈值设定（如 $\tau=0.5$）和软修复调度是启发式设计，可能对不同类型的动作或伪影并非最优。扩散模型采样的固有随机性有时仍会导致次优结果，尽管集成策略有所缓解。未来方向包括：开发自动化的质量标注技术以减少人工依赖，探索测试时分类器引导以改善内容保留与保真度的权衡，以及将该框架扩展到面部动作或交互数据等其他运动类型的清理任务。

### 问题背景：运动数据中的真实伪影

动作捕捉（mocap）数据是动画制作、游戏开发和运动分析的核心资产。然而，在真实生产环境中采集的原始动作数据普遍存在各种伪影（artifacts），包括：

- **足部滑动（foot skating）**：脚与地面的接触关系被破坏，产生不真实的滑动。
- **运动突变（motion pops）**：帧间过渡出现抖动或不连续跳变。
- **冻结帧（frozen frames）**：部分关节或全身在若干帧内保持静止，破坏运动流畅性。
- **身体自穿透（self-penetration）**：肢体相互穿插，违反物理约束。
- **不自然关节旋转**：因传感器遮挡或算法估计错误导致的异常姿态。

以文中使用的 **SoccerMocap** 数据集为例，该数据集包含约 245 小时、50 fps 的运动数据，其中人工标注的伪影帧约占 1%，而启发式算法标记的损坏帧高达 39%（Section 8）。这些伪影的存在严重影响了数据在下游任务中的可用性。

### 现有方法的瓶颈：对配对数据的刚性依赖

当前主流的运动清理方法可分为三类，均存在显著局限：

1. **基于配对数据的有监督方法**：如 **XClean**、**RoHM** 等，需要成对的“损坏-干净”运动数据进行监督训练。然而在实际生产中，获取域内配对数据成本极高——需要专业动画师逐帧修复，一个包含冻结帧和运动突变的片段可能需要数小时的人工修复（Figure 6）。

2. **条件扩散修复方法**：如 **CondMDI-B**，虽然利用了扩散模型的生成能力，但仍依赖配对数据来学习从损坏到干净的映射。

3. **物理模拟方法**：如 **PHC**（Luo et al., 2023），通过物理约束来修复运动，但可能引入新的伪影，如足部抖动（Figure 14）。

**核心瓶颈**在于：直接丢弃损坏片段会破坏时序连续性，导致模型无法学习长时运动动态；而保留损坏数据又缺乏有效的利用机制。这种“数据困境”使得现有方法在真实生产场景中难以规模化应用。

### 本文动机：从混合质量数据中学习清理能力

**StableMotion** 的核心动机是打破对配对数据的刚性依赖。作者观察到，原始动作数据虽然包含伪影，但整体上仍包含大量有效运动信息——关键在于如何让模型从这种“混合质量”的数据中自主学习区分和生成高质量运动。

受强化学习中状态奖励（state-level reward）的启发，StableMotion 将运动清理重新定义为一种**质量可控的条件生成问题**：通过引入帧级质量指示变量（QualVar），模型被联合训练以同时评估运动质量和根据指定质量生成运动。这一设计使模型能够：

- 在训练阶段，直接从混合质量的原始数据中学习，无需配对标签。
- 在测试阶段，通过设定高质量指示变量，引导模型生成干净运动。

这种方法论转变使得运动清理模型可以在真实生产数据上端到端训练，从根本上降低了数据准备成本，同时保持了与有监督方法相当甚至更优的清理效果。

## 核心方法与创新机理
StableMotion的核心创新在于将运动清理重新定义为一种**质量可控的条件生成问题**，从而彻底绕过了传统方法对配对干净-损坏数据的依赖。其关键洞察在于：通过引入帧级质量指示变量（QualVar）并设计生成-判别联合训练框架，模型既能评估运动质量，又能根据指定的质量水平生成运动——这使得模型可以直接从混合质量的原始数据中学习清理能力，而无需任何配对监督。

### 关键创新组件

**1. 质量指示变量（QualVar）**
StableMotion引入帧级质量指示变量 $h$，用以表征每帧运动的数据质量分布（Section 5.1）。这一设计类似于强化学习中的状态级奖励信号，使模型能够显式地感知并区分不同质量水平的运动帧。在训练时，$h$ 与运动特征 $m$ 组合为联合表示 $\mathbf{x}_t = (\mathbf{m}, \mathbf{h})_t$ 输入扩散模型；在测试时，通过设定高质量指示变量进行“质量提示（quality prompting）”，引导模型生成干净的运动帧。

**2. 生成-判别联合扩散模型**
StableMotion采用统一的扩散框架，联合执行两个任务（Section 5.2）：
- **判别任务** $D(h|m)$：评估每帧运动质量，预测质量指示变量；
- **生成任务** $G(m|h)$：根据指定的质量指示变量生成对应质量水平的运动。

这种双功能设计使单一模型同时具备“识别损坏帧”和“生成干净帧”的能力，无需额外的分类器或修复网络。

**3. 测试时自适应技术**
为进一步提升内容保留和结果一致性，StableMotion提出两项测试时技术：
- **自适应清理（Adaptive Cleanup）**：通过蒙特卡洛采样估计软质量标签 $\bar{h}^i$，并根据软修复调度函数决定每帧的扩散起始步数，使得轻微伪影的帧从较晚的扩散步开始修复，从而保留更多原始信息（Section 6.1）。
- **质量感知集成（Quality-Aware Ensemble）**：利用扩散模型的采样多样性和生成-判别模型的自评估能力，生成多个候选运动并通过预测的质量分数选择最优结果，提升输出的鲁棒性和一致性（Section 6.2）。

### 与基线方法的范式差异

| 维度 | 现有方法 | StableMotion |
|------|---------|-------------|
| 训练数据要求 | 需要配对的干净-损坏数据（如XClean、RoHM） | 仅需混合质量的原始数据，无需配对 |
| 质量控制机制 | 无显式质量控制或仅基于输入特征 | 帧级质量指示变量（QualVar）进行条件控制 |
| 模型范式 | 单独的运动生成或分类模型 | 统一的生成-判别联合扩散模型 |
| 测试时策略 | 固定步数扩散修复 | 基于软质量估计的自适应修复+质量感知集成 |

这一范式转换的核心价值在于：**将数据需求从“昂贵配对”降级为“廉价标注”**——质量指示变量可通过人工标注或启发式算法获取，而无需构建成对的干净-损坏运动数据。消融实验表明，移除QualVar后模型性能显著下降（足滑率从3.60%升至6.37%，Table 6），验证了该设计的关键性。

StableMotion 的核心思路是将运动清理重新定义为一种**质量可控的条件生成问题**。传统方法依赖配对的干净-损坏数据训练有监督模型，而 StableMotion 通过引入帧级质量指示变量（QualVar），使模型能够直接从混合质量的原始运动捕捉数据中学习清理能力，无需任何配对数据。

### 框架总览

整个框架围绕一个统一的**生成-判别扩散模型**构建。如 Figure 2 所示，该模型在训练时联合学习两项任务：

1. **质量判别**：预测每帧运动的质量指示变量 $h$，评估运动质量。
2. **运动生成**：根据指定的质量指示变量生成对应质量水平的运动帧。

训练时，模型直接在混合质量的原始数据上学习，输入为运动 $m$ 与质量指示变量 $h$ 的联合表示 $\mathbf{x}_t = (\mathbf{m}, \mathbf{h})_t$。通过扩散过程逐步加噪与去噪，模型学会在给定不同 $h$ 的条件下生成不同质量的运动。这种联合训练使模型内在地理解“什么是高质量运动”以及“如何生成高质量运动”，从而在测试时，只需将质量指示变量设定为“高质量”，模型即可将损坏的运动修复为干净运动。

### 核心模块与数据流

StableMotion 框架包含以下关键模块，形成完整的训练-推理流水线：

**1. 质量指示变量预测模块**
该模块评估每帧运动的质量，输出对应的 QualVar $h$。质量标签可通过人工标注或启发式算法获取，训练时模型学习从运动特征中推断质量水平。在推理阶段，该模块负责识别哪些帧存在伪影、伪影的严重程度如何，为后续的自适应清理提供依据。

**2. 质量条件运动生成模块**
该模块是框架的核心生成器，根据指定的质量指示变量 $h$ 生成运动帧。训练时，模型学习 $G(\mathbf{m}|\mathbf{h})$ 的映射关系，即给定任意质量水平 $h$，生成对应质量的运动。测试时，通过将 $h$ 设定为高质量值，模型即可将损坏帧修复为干净运动。

**3. 扩散 Transformer (DiT) 主干网络**
上述两个模块共享同一个扩散 Transformer 骨干网络。该网络采用旋转位置嵌入（RoPE）替代绝对位置嵌入，以更好地捕捉运动的时序结构。在去噪过程中，网络同时预测运动 $\mathbf{m}$ 和质量指示变量 $\mathbf{h}$，实现生成与判别的统一。

**4. 自适应清理模块（测试时）**
如 Figure 3 所示，该模块通过蒙特卡洛采样估计每帧的软质量标签 $\bar{\mathbf{h}}^i$，并根据软修复调度函数确定每帧的修复起始步数：

$$
\mathbf{t}_{\mathrm{soft}}^{i} = \begin{cases} 
T \sin \frac{\pi}{2} \min(1, 2\bar{\mathbf{h}}^{i} - 1 + \tau), & \text{if } \bar{\mathbf{h}}^{i} \geq \tau \\
0, & \text{otherwise}
\end{cases}
$$

其中 $\tau = 0.5$ 为阈值。质量较高的帧（伪影轻微）从较晚的扩散步开始修复，保留更多原始信息；质量较低的帧（伪影严重）从较早的扩散步开始修复，更彻底地去除损坏。这种自适应策略在内容保留与伪影去除之间实现了更好的平衡。

**5. 质量感知集成模块（测试时）**
如 Figure 5 所示，该模块利用扩散模型的随机性生成多个候选清理结果（默认 5 个），然后通过模型自身的质量判别能力评估每个候选，选择质量最高的结果作为最终输出。由于扩散模型支持批量推理，该集成策略不会显著增加推理耗时，同时有效提升了清理结果的一致性和鲁棒性。

### 训练与推理流程

**训练阶段**：模型在混合质量的原始运动数据上训练，学习联合分布 $p(\mathbf{m}, \mathbf{h})$。训练目标与 DDPM 的简单目标一致，只是将预测对象从纯运动 $\mathbf{x}_0$ 扩展为联合表示 $(\mathbf{m}, \mathbf{h})_0$。模型无需知道哪些帧是“干净”的，只需学习质量指示变量与运动质量之间的对应关系。

**推理阶段**：给定一段损坏的运动序列，模型首先通过质量指示变量预测模块识别损坏帧及其严重程度，然后通过自适应清理模块为每帧确定修复步数，最后由质量条件运动生成模块在高质量指示变量的引导下生成修复后的运动。质量感知集成进一步从多个候选结果中择优输出。

这种生成-判别统一的设计使得 StableMotion 能够在不依赖配对数据的情况下，从混合质量数据中自动学习运动清理能力，实现了训练数据需求与清理性能之间的根本性突破。

### 3.1 问题形式化与扩散基础

StableMotion 将运动清理建模为质量可控的条件生成问题。给定一段包含混合质量帧的运动序列，模型需要同时识别损坏帧并生成高质量的替代帧。其核心数学基础建立在去噪扩散概率模型（DDPM）之上。

前向扩散过程逐步向数据样本添加高斯噪声，总步数为 $T$：

$$q ( \mathbf { x } _ { t } | \mathbf { x } _ { t - 1 } ) = N ( \mathbf { x } _ { t } ; \sqrt { \alpha _ { t } } \mathbf { x } _ { t - 1 } , \beta _ { t } \mathbf { I } )$$

其中 $\mathbf{x}_0$ 为原始数据，$\mathbf{x}_t$ 为第 $t$ 步的噪声版本，$\alpha_t$ 和 $\beta_t$ 为噪声调度参数。训练目标是让去噪模型 $g$ 从任意噪声步的 $\mathbf{x}_t$ 预测完全去噪的样本 $\mathbf{x}_0$：

$$\mathcal { L } _ { \mathrm { s i m p l e } } = \mathbb { E } _ { \mathbf { x } _ { 0 } \sim \mathcal { M } , t \sim \mathcal { U } \left[ 1 , T \right] , \mathbf { x } _ { t } \sim q \left( \mathbf { x } _ { t } | \mathbf { x } _ { 0 } \right) } \left[ \left| \left| \mathbf { x } _ { 0 } - g ( \mathbf { x } _ { t } ) \right| \right| ^ { 2 } \right]$$

---

### 3.2 核心模块一：质量指示变量（QualVar）

**瓶颈定位**：现有方法依赖配对的干净-损坏数据训练，而实际生产中获取域内配对数据成本高昂。直接丢弃损坏片段会破坏时序连续性，导致模型无法学习长时运动动态。

**核心设计**：引入帧级质量指示变量 $\mathbf{h}$，作为每帧运动质量的量化表征。该变量类似于强化学习中的状态级奖励信号，使模型能够区分不同质量水平的运动数据。训练时，模型在联合特征空间上操作：

$$\mathbf{x}_t = (\mathbf{m}, \mathbf{h})_t$$

其中 $\mathbf{m}$ 为运动特征，$\mathbf{h}$ 为对应的质量指示变量，$t$ 为扩散步数。这一设计使模型能够从混合质量的原始数据中直接学习，无需配对监督——模型通过联合训练同时学会评估运动质量（判别能力）和根据指定质量生成运动（生成能力）。

**因果机制**：在测试时，用户通过设定高质量指示变量（即“质量提示”）驱动模型生成干净运动，从而将运动清理转化为质量条件生成任务。消融实验（Table 6）证实，移除 QualVar 后足滑率从 3.60% 上升至 6.37%，验证了该变量是模型学习高质量运动生成能力的关键因果旋钮。

---

### 3.3 核心模块二：生成-判别联合扩散模型

StableMotion 的模型范式是一个统一的生成-判别联合扩散模型，包含两个协同训练的子功能：

1. **质量评估模块** $D(\mathbf{h}|\mathbf{m})$：给定运动 $\mathbf{m}$，预测其帧级质量指示变量 $\mathbf{h}$，实现对任意运动帧的自动质量评估。
2. **质量条件运动生成模块** $G(\mathbf{m}|\mathbf{h})$：给定目标质量指示变量 $\mathbf{h}$，生成对应质量水平的运动 $\mathbf{m}$。

这两个模块共享同一个扩散 Transformer（DiT）主干网络，在去噪过程中同时预测 $\mathbf{m}$ 和 $\mathbf{h}$。训练时，模型在混合质量数据上学习联合分布 $p(\mathbf{m}, \mathbf{h})$，从而隐式地捕获了“何种运动特征对应何种质量水平”的映射关系。测试时，通过将 $\mathbf{h}$ 设定为高质量标签，模型反向推理出对应的干净运动。

---

### 3.4 核心模块三：自适应清理（Adaptive Cleanup）

**瓶颈定位**：标准扩散修复对所有帧采用相同的去噪步数，导致轻微损坏帧的内容被过度修改，内容保真度下降。

**核心设计**：通过蒙特卡洛采样估计每帧的软质量标签 $\bar{\mathbf{h}}^i$（对预测的 $\hat{\mathbf{h}}^i$ 多次采样取期望），然后根据软修复调度函数决定每帧的初始扩散步数：

$$\mathbf { t } _ { \mathrm { s o f t } } ^ { i } = \left\{ \begin{array} { l l } { T \sin \frac { \pi } { 2 } \operatorname* { m i n } \big ( 1 , 2 \bar { \mathbf { h } } ^ { i } - 1 + \tau \big ) , } & { \mathrm { i f } \bar { \mathbf { h } } ^ { i } \geq \tau } \\ { 0 , } & { \mathrm { o t h e r w i s e } } \end{array} \right.$$

其中 $\tau=0.5$ 为质量阈值，$T$ 为总扩散步数。该调度函数的直觉是：$\bar{\mathbf{h}}^i$ 越高的帧（质量越好），从越晚的扩散步开始修复，保留更多原始信息；$\bar{\mathbf{h}}^i$ 越低的帧（损坏越严重），从越早的步开始修复，给予模型更大的修改自由度。

**证据强度**：Table 7 显示，加入 Adaptive Cleanup 后，全局平均关节位置误差（GMPJPE）从 3.59 cm 降至 2.21 cm，证明该模块显著改善了内容保留能力。

---

### 3.5 核心模块四：质量感知集成（Quality-Aware Ensemble）

**瓶颈定位**：扩散模型的采样随机性可能导致单次推理结果不稳定，尤其在损坏严重的帧上可能产生次优修复。

**核心设计**：利用扩散模型的随机性生成多个候选运动（文中使用 5 个候选），然后利用模型自身的质量评估功能对每个候选进行自评分，选择质量得分最高的结果作为最终输出。该技术无需额外模型，直接复用生成-判别模型的判别能力，且由于批量推理的特性，墙钟时间增加不显著。

**证据强度**：Table 7 显示，加入 Quality-Aware Ensemble 后，足滑距离（FS Dist）从 3.44 进一步降至 3.31，提升了修复结果的鲁棒性和一致性。

---

### 1. 标签是二值标签吗？

**在训练阶段，它是二值标签（Binary Labels）** 。
- **$h^i = 1$**：代表该帧是**损坏的帧**（Corrupted Frame），包含动作瑕疵 。
- **$h^i = 0$**：代表该帧是**干净的帧**（Clean Frame） 。

但在**测试/推理阶段**，为了更细腻地评估动作损坏的严重程度，论文引入了一种“软质量标签”（Soft Quality Label, $\tilde{h}^i$） 。它是通过对同一个模型进行多次蒙特卡洛采样（Monte Carlo Estimation）并计算期望值得到的连续数值 ，数值越接近 1.0 代表损坏越严重，越接近 0.5 甚至更低则代表瑕疵很轻微 。

### 2. 标签 $h$ 是如何获取的？

根据论文在不同实验数据集中的描述，这些标签主要通过以下三种方式（**人工标注、启发式算法、或两者结合**）来获取：

#### 方法一：人工标注与启发式算法结合（以 SoccerMocap 数据集为例）

在大型真实世界生产环境数据集上，标签是由动画师与算法共同合作完成的 ：

- **人工标注（HAA - Human-Annotated Artifacts）**：由专业美术/动画师手动标记出大约 1% 的损坏帧 。这部分标注主要集中在自动算法很难检测到的复杂动作瑕疵上，例如**身体穿模（Self-penetration）**和**不自然的关节姿态错误** 。
    
- **启发式算法自动检测**：为了扩大标注覆盖面，引入了自动检测算法，专门用来识别**滑步（Foot-skating）、翻转（Flipping）、动作突变（Motion pops）**和**冻结帧（Frozen frames）** 。这种算法被设计为具有高召回率（High Recall），以确保尽可能漏掉极少的瑕疵帧，最终自动标记了约 39% 的损坏帧 。

#### 方法二：纯启发式算法自动生成（以 PopDanceSet 数据集为例）

- 对于从网络视频中通过姿态估计技术提取的在野（In-the-wild）数据集，训练 StableMotion 所需的动作质量标签**完全是通过自动化启发式算法（Automatic Heuristics）计算生成的**，无需人工干预 。

#### 方法三：通过代码人工合成标记（以 BrokenAMASS 基准测试为例）

- 为了在受控环境中进行定量评估，研究人员通过预设的逻辑代码（如论文附录中的 Python 损坏函数）主动对干净的数据集进行污染（加入高斯噪声、超平滑、速度缩放等） ，在代码运行的同时，**系统会自动将受到污染的区间在 Mask（掩码）中标记为 1**，从而直接获得精确的地面真值（Ground Truth）二值标签 。

----

## 实验与关键发现
### 核心定量结果

StableMotion 在三个基准上均展现出显著的清理能力，且无需任何配对干净数据训练。

**SoccerMocap（真实足球运动捕捉数据）**：该数据集包含冻结帧、运动突变(pops)、足部滑动等真实世界伪影。如 Table 1 所示，StableMotion 将足滑距离(FS Dist)从输入的 6.42 降至 2.14（降低 66.7%），运动突变率(Pops Rate)从 0.41% 降至 0.13%（降低 68.3%），冻结帧率(Frozen Rate)从 23.68% 降至 4.50%（降低 81.0%）。这些伪影类型是实际生产中动画师需要数小时手动修复的问题，而 StableMotion 可在数秒内完成平滑纠正（Figure 6, Figure 7）。

**BrokenAMASS（合成破损运动数据集）**：该基准通过向 AMASS 干净运动注入多种合成伪影构建，用于对比各方法的清理与内容保留能力。如 Table 2 所示，StableMotion (Base) 在足滑距离(FS Dist=3.70)和加速度误差(Accel=0.60)两项核心指标上均优于所有基线方法，包括使用干净数据训练的 **RoHM**（FS Dist=4.43, Accel=1.00）和使用配对数据训练的 **XClean**（FS Dist=3.80, Accel=0.66）。值得注意的是，StableMotion 在全局运动精度(GMPJPE=3.59 cm)上也表现优异，说明其在去除伪影的同时有效保留了原始运动内容。Figure 8 和 Figure 9 展示了动态运动行为的清理效果，模型能生成自然的足部和身体运动，同时保持全局轨迹。

**PopDanceSet（抖动舞蹈运动数据）**：如 Table 3 所示，StableMotion 在高度抖动的舞蹈运动上也表现出色，进一步验证了方法对不同伪影类型的鲁棒性（Figure 11）。

### 消融实验

#### 关键设计组件消融

Table 6 揭示了两个核心设计的作用：

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2505_03154/figures/019_Table_6.jpg]]
*Table 6: Ablation experiments on quality indicator variables (QualVar) and rotary positional embeddings (RoPE). Methods marked with “*” use the ground truth quality labels to determine which frames need cleanup*

- **质量指示变量(QualVar)**：移除 QualVar 后，在使用真实质量标签指定清理帧的设置下（标记 *），足滑率(FS Rate)从 3.60% 上升至 6.37%，足滑距离(FS Dist)从 2.39 恶化至 2.55。这表明 QualVar 是模型学习从混合质量数据中生成高质量运动的关键因果机制——没有它，模型无法区分不同质量水平的运动，也就无法在测试时通过“质量提示”生成干净运动。

- **旋转位置嵌入(RoPE)**：将绝对位置嵌入替换为 RoPE 对伪影清理有显著改善，尤其是足滑指标。Table 6 中 w/o RoPE 配置的 FS Dist 和 FS Rate 均劣于 Base 配置，说明 RoPE 有助于模型更好地建模运动序列的时序结构。

#### 推理技术消融

Table 7 展示了测试时技术的增量贡献：

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2505_03154/figures/017_Table_7.jpg]]
*Table 7: Ablation experiments on Adaptive Cleanup and Quality-Aware Ensemble*

- **自适应清理(Adaptive Cleanup)**：在 Base 推理基础上加入自适应清理后，全局运动精度 GMPJPE 从 3.59 cm 大幅改善至 2.21 cm，表明基于软质量估计的自适应修复策略能更好地保留原始运动内容，尤其对细微伪影的处理更为精准（Figure 10）。

- **质量感知集成(Quality-Aware Ensemble)**：进一步将足滑距离 FS Dist 从 3.44 降至 3.31，通过自评估从 5 个候选生成结果中选择最优运动，提升了输出的一致性和鲁棒性。

#### 训练数据鲁棒性消融

- **质量标签数据量**（Table 4）：即使仅使用 10% 的带质量标签数据训练，模型仍能保持相当的清理能力，说明框架对标注成本具有较好的鲁棒性。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2505_03154/figures/016_Table_4.jpg]]
*Table 4: Performance of StableMotion model when trained with different sized subsets of BrokenAMASS with quality labels. All results are reported from StableMotion (Base) inference setting without the proposed special test-time techniques*

- **训练数据破损率**（Table 5）：在不同破损率（25%-100%）下，StableMotion 均能有效学习高质量运动生成能力。即使在 100% 破损率的极端情况下，模型仍能生成优于输入的干净运动，这归功于 QualVar 提供的质量条件控制机制——模型学会了根据指定的高质量指示变量生成相应质量水平的运动。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2505_03154/figures/018_Table_5.jpg]]
*Table 5: Effect of training data corruption rate on StableMotion framework. “*” marks that results are obtained using the ground truth quality labels to specify the segments for cleanup. This setting focuses on the model’s high-quality motion generation ability learned from the corrupted data, excluding the effect of the quality indicator variable prediction pefromance*

### 域外泛化

Table 8 和 Table 9 展示了模型在未见域数据上的泛化能力：

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2505_03154/figures/020_Table_8.jpg]]
*Table 8: Out-of-domain motion cleanup results on the vision-based motion capture dataset (IDEA400 [Lin et al. 2024]) and physics-based simulated character motion (PHC-Tracking [Luo et al. 2023])*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2505_03154/figures/023_Table_9.jpg]]
*Table 9: Out-of-domain motion cleanup results on Motion-X Music [Lin et al. 2024], a motion dataset constructed by human pose estimation from online videos. PHC [Luo et al. 2023], a SOTA physics-based motion tracking model, is applied to cleanup motion through zero-shot imitation in physicsconstrained environments*

- **IDEA400**（基于视觉的运动捕捉数据）：模型能自动解决足部冻结问题，修复自然的下半身运动，同时保持僵尸式手臂运动风格（Figure 13）。
- **PHC-Tracking**（物理模拟角色运动）：基于物理的运动跟踪器如 **PHC**（Luo et al., 2023）虽能修复部分物理不合理伪影，但也可能引入新的抖动等问题。StableMotion 能有效缓解这些来自物理模拟角色的伪影（Figure 14）。
- **Motion-X Music**（在线视频人体姿态估计数据）：进一步验证了方法对真实世界噪声的清理能力。

### 失败模式与局限

1. **质量标注依赖**：QualVar 需要人工标注或启发式算法提供，尤其对细微伪影的检测仍需人工参与，限制了完全自动化的部署。
2. **域外性能衰减**：尽管展示了域外泛化能力，模型在显著不同于训练分布的领域仍可能出现性能下降，需要手动验证具体衰减程度。
3. **启发式阈值敏感性**：自适应清理中的软阈值 τ=0.5 和软修复调度是启发式设计，对不同类型的动作或伪影可能不是最优的。
4. **扩散采样随机性**：扩散模型固有的随机性有时仍会导致次优结果，尽管质量感知集成在一定程度上缓解了这一问题。
5. **评估公平性**：使用的伪影检测算法为专有系统，可能对某些伪影类型不敏感；且所有基线方法使用同一模型预测的破损帧标签，可能导致其他方法在检测阶段处于不利地位。

## 定位与知识库关联
### 1. 与现有工作的关系

StableMotion 的核心贡献在于将运动清理问题从“有监督修复”范式重构为“质量条件生成”范式，其方法定位可从三个维度理解。

**相对于有监督运动清理方法**：现有方法如 **XClean**、**RoHM** 和 **ConvAE-B** 均依赖配对的干净-损坏数据进行训练。在实际生产中，获取域内配对数据成本高昂，且直接丢弃损坏片段会破坏时序连续性，使模型无法学习长时运动动态。StableMotion 通过引入帧级质量指示变量（QualVar），使模型能直接从混合质量的原始数据中学习清理能力，彻底消除了对配对数据的依赖。在 BrokenAMASS 基准上，StableMotion 训练的模型在足滑距离（FS Dist）上达到 3.70，优于使用干净或配对数据训练的 **RoHM**（4.43），加速度误差（Accel）从 1.00 降至 0.60（Table 2）。

**相对于条件扩散修复方法**：**CondMDI-B** 等条件扩散方法通常基于输入特征进行修复，缺乏对运动质量的显式建模。StableMotion 的生成-判别联合扩散模型将质量评估与运动生成统一在同一框架中——模型同时预测质量指示变量 $h$ 并生成运动 $m$，训练时使用联合特征 $\mathbf{x}_t = (\mathbf{m}, \mathbf{h})_t$。这种设计使模型既能评估运动质量，又能根据指定的质量提示生成运动，在测试时通过设定高质量指示变量即可生成干净运动。

**相对于物理模拟方法**：**PHC**（Luo et al., 2023）通过物理约束进行运动跟踪与清理，虽能修复部分物理不可信的伪影，但可能引入新的伪影（如抖动脚步）。StableMotion 在 PHC-Tracking 输出上的域外实验表明，该方法也能有效缓解物理模拟角色产生的伪影（Table 8），展示了与物理方法的互补性。

### 2. 适用边界与局限

尽管 StableMotion 在多个基准上表现优异，其适用性仍受以下因素制约：

**质量标注依赖**：框架需要人工标注或启发式算法提供质量指示变量。对于细微伪影（如轻微关节旋转异常），现有专有检测算法可能不敏感，这影响了评估公平性，也限制了完全自动化部署的可能性。Table 4 的消融实验表明，使用不同规模的质量标签子集训练时，模型性能随标签数据量增加而提升，进一步证实了质量标签的重要性。

**域外泛化的不确定性**：虽然模型在 IDEA400（基于视觉的动作捕捉数据）和 Motion-X Music（在线视频姿态估计数据）上展示了域外泛化能力（Table 8、Table 9），但在显著不同于训练分布的动作领域（如灵巧操作动画）仍可能出现性能下降。这种泛化能力的边界尚未被系统性地刻画。

**启发式设计的局限性**：自适应清理中的软阈值设定（$\tau = 0.5$）和软修复调度函数是启发式设计，其通用性未经验证。软修复调度公式为：
$$\mathbf{t}_{\mathrm{soft}}^{i} = \begin{cases} T \sin \frac{\pi}{2} \min(1, 2\bar{\mathbf{h}}^{i} - 1 + \tau), & \text{if } \bar{\mathbf{h}}^{i} \geq \tau \\ 0, & \text{otherwise} \end{cases}$$
该调度对不同类型伪影（如足滑 vs. 冻结帧）的适应性可能不同，当前设计未提供自适应调整机制。

**扩散采样的固有随机性**：尽管质量感知集成（使用 5 个候选运动进行自评估选择）在一定程度上缓解了随机性，扩散模型的采样过程仍可能导致次优结果，尤其在需要极高时序一致性的长序列场景中。

### 3. 开放问题

基于上述局限，以下问题值得进一步探索：

1. **自动化质量标注**：能否开发自监督或半监督的质量标注技术，以减少对手工标注或特定启发式算法的依赖？例如，利用运动学约束（如足部接触一致性、关节角度范围）作为弱监督信号。

2. **测试时引导的保真度权衡**：能否通过测试时分类器引导（classifier guidance）进一步改善内容保留与伪影清理之间的权衡？当前的自适应清理通过软修复调度实现这一平衡，但引导机制可能提供更精细的控制。

3. **长时一致性增强**：在需要极长时序一致性的应用（如灵巧操作动画、多人交互场景）中，如何增强模型的长期一致性？当前框架以帧级质量变量为核心，缺乏显式的长时依赖建模。

4. **跨模态扩展**：该生成-判别联合框架能否扩展到其他非运动数据的清理任务，如面部动作捕捉数据的抖动修复或手物交互数据的物理合理性校正？核心挑战在于如何定义适用于不同模态的质量指示变量。

## 原文 PDF
![[paperPDFs/SIGGRAPH_ASIA_2025/StableMotion_Training_Motion_Cleanup_Models_with_Unpaired_Corrupted_Data.pdf]]
