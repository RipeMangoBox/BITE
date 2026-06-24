---
title: Autonomous Character-Scene Interaction Synthesis from Text Instruction
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2024/LINGO_Autonomous_Character_Scene_Interaction_Synthesis_from_Text_Instruction.pdf
aliases:
- PAHSM
- ACSISFTI
tags:
- SIGGRAPH_ASIA_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过自回归扩散模型、双体素场景表示、帧嵌入的文本调节以及阶段特定的目标编码器，结合自主调度器预测阶段转换，实现了多阶段人-场景交互的自主合成。
primary_logic: 将复杂人-场景交互分解为自回归生成的连续运动片段，引入自主调度器决定阶段转换时机，同时利用双体素场景感知和帧嵌入的文本条件，使模型能从简单文本指令生成路径规划、场景避障和交互动作无缝衔接的连贯运动。
claims:
- 本文方法在交互运动合成中FID显著优于TRUMANS（2.048 vs 2.438），并取得更高精度和召回率
- 在杂乱场景中的运动合成中，本文方法的场景穿透指标（Pene_mean 0.402）远低于TRUMANS（1.011）
- 移除帧嵌入导致FID从2.048升至2.368，且合成动作紊乱重复，证明帧嵌入对时序语义连贯性的重要性
- 替换双体素场景表示为平面可行走图使Pene_mean从0.402升至0.587，证明预测性场景信息对避障的必要性
---

# Autonomous Character-Scene Interaction Synthesis from Text Instruction

> [!tip] 核心洞察
> 将复杂人-场景交互分解为自回归生成的连续运动片段，引入自主调度器决定阶段转换时机，同时利用双体素场景感知和帧嵌入的文本条件，使模型能从简单文本指令生成路径规划、场景避障和交互动作无缝衔接的连贯运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于文本指令的自主角色-场景交互合成 |
| 英文题名 | Autonomous Character-Scene Interaction Synthesis from Text Instruction |
| 会议/期刊 | SIGGRAPH ASIA 2024 |
| Links | [Project](https://lingomotions.com) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Proposed autonomous HSI synthesis method |
| Dataset | Interactive motion synthesis, Locomotion in cluttered scenes, Object reaching |

> [!tip] 效果简介
> - Interactive motion synthesis (LINGO-eval) 上，FID 2.048 ± 0.058 vs 2.438 ± 0.041 (TRUMANS) (-0.390)。
> - Locomotion in cluttered scenes 上，Pene_mean 0.402 ± 0.004 vs 1.011 ± 0.012 (TRUMANS) (-0.609)。
> - Object reaching 上，Error dist. 0.061 ± 0.004 vs 0.156 ± 0.028 (GOAL) (-0.095)。

## 概述

合成真实且多样化的人-场景交互（HSI）运动是计算机图形学与具身智能中的核心挑战。现有方法通常依赖多个分离模型分别处理行走、伸手、物体交互等运动阶段，并要求用户预先指定路径点与阶段转换时机，难以从单一文本指令和目标任务位置直接生成连贯的多阶段交互运动。这一瓶颈源于缺乏统一的生成框架，使得运动连贯性差且实用性受限。

针对上述问题，本文提出一种自主角色-场景交互合成方法，其核心洞察在于：将复杂人-场景交互分解为自回归生成的连续运动片段，引入自主调度器决定阶段转换时机，同时利用双体素场景感知和帧嵌入的文本条件，使模型能从简单文本指令生成路径规划、场景避障和交互动作无缝衔接的连贯运动。该方法通过自回归扩散模型、双体素场景表示、帧嵌入的文本调节以及阶段特定的目标编码器，结合自主调度器预测阶段转换，实现了多阶段人-场景交互的自主合成（Fig. 2）。

在交互运动合成任务上，本文方法的FID显著优于TRUMANS（2.048 vs 2.438）；在杂乱场景中的运动合成中，场景穿透指标Pene_mean远低于TRUMANS（0.402 vs 1.011），验证了双体素场景表示对避障的关键作用。消融实验进一步表明，移除帧嵌入导致FID升至2.368且合成动作紊乱重复，替换双体素为平面可行走图则使Pene_mean升至0.587，证实了各设计选择的有效性。

在方法谱系上，本文工作衔接了基于扩散模型的运动生成（如TRUMANS, Jiang et al., SIGGRAPH 2024）与场景感知交互合成（如GOAL, Taheri et al., CVPR 2022），但通过统一的自回归扩散框架和自主调度机制，首次实现了从文本指令到多阶段人-场景交互的端到端自主合成。当前方法尚未涵盖面部表情和手部精细操作，对未见交互类型的泛化能力也有待进一步验证。

## 背景与动机

### 问题背景

在虚拟现实、游戏开发和电影制作等应用中，合成真实的人-场景交互（Human-Scene Interaction, HSI）运动是一个核心挑战。理想情况下，用户希望仅通过一句自然语言指令（如“走向沙发并坐下”）和目标任务位置，系统便能自主生成角色在三维场景中移动、避障并与物体交互的连贯运动序列。

### 现有方法的局限

当前主流的运动合成方法通常采用**多阶段分离式架构**：将整个交互过程拆解为行走（locomotion）、伸手（reaching）和物体交互（object interaction）等独立阶段，分别由不同的模型处理。这类方法的代表包括 **TRUMANS**（Jiang et al., SIGGRAPH 2024）和 **GOAL**（Taheri et al., CVPR 2022）。这种分离式设计存在两个根本性缺陷：

1. **依赖人工指定路径点和阶段转换**：用户需要显式地为角色规划行走路径，并手动决定何时从行走阶段切换到交互阶段，这在实际应用中极不便利。
2. **运动连贯性差**：由于各阶段由独立模型生成，阶段间的过渡往往生硬不自然，缺乏对场景上下文和任务语义的全局理解。

从场景感知的角度看，现有方法（如TRUMANS）通常将三维场景压缩为扁平的可行走图（flattened walkable map），丢失了关键的立体空间信息，导致角色在杂乱场景中频繁穿透物体。从文本语义理解的角度看，现有方法的文本条件注入缺乏时序维度，无法精确引导不同时间阶段的动作语义。

### 核心瓶颈

现有方法的根本瓶颈在于：**缺乏一个统一的框架，能够从单一的文本指令和目标任务位置出发，自主完成路径规划、场景避障、阶段转换和交互动作的无缝合成**。这要求模型同时具备以下能力：

- 理解文本指令中的时序语义（先走到哪里，再做什么动作）；
- 感知三维场景的几何结构以主动避障；
- 自主决定何时从行走切换为交互，而非依赖人工指定。

### 本文动机

针对上述瓶颈，本文提出了一种**自主角色-场景交互合成方法**，其核心动机是实现从文本指令到多阶段交互运动的“端到端”自主生成。该方法在SIGGRAPH Asia 2024上发表，旨在消除对人工路径点和阶段转换的依赖，使角色能够像人类一样，在理解指令后自主规划行为序列并适应环境。

## 核心创新

本文的核心创新在于将多阶段人-场景交互（HSI）从“分离模型+人工调度”的范式升级为**统一自回归扩散框架+自主阶段调度**，使角色能够直接从单一文本指令和目标位置生成连贯的避障行走、伸手及物体交互动作。以下从三个关键 changed slots 展开分析。

### 1. 统一自回归扩散生成与自主阶段调度

**Baseline 瓶颈**：现有方法（如 **TRUMANS**，Jiang et al., SIGGRAPH 2024）依赖多个分离模型分别处理行走、伸手、物体交互等运动阶段，需要用户预先指定路径点和阶段转换时机。这种人工调度不仅降低了实用性，还导致阶段间运动连贯性差。

**本文方案**：将整个 HSI 过程建模为自回归扩散模型的连续生成问题。具体而言，模型以固定长度 $W$ 的运动片段 $X = \{X_i\}_{i=1}^W$ 为单位，基于已生成的运动序列和场景条件，通过去噪扩散概率模型（DDPM）自回归地合成下一段运动。训练损失为标准噪声预测的均方误差：

$$\mathcal{L} = \mathbb{E}_{\tilde{X}_t \sim q(\tilde{X}_t \mid C), t \sim U(1, T)} \| \epsilon - \epsilon_\theta(\tilde{X}_t, t, C) \|_2^2$$

其中 $C$ 为条件项集合，$\epsilon_\theta$ 为去噪网络。

**关键突破——自主调度器**：框架引入一个自主调度器（Autonomous Scheduler），负责预测阶段转换的时机（如从行走切换至伸手），无需人工指定路径点或阶段边界。这使模型能够自主决定“何时开始交互”，实现了从文本指令到多阶段动作的端到端生成。

### 2. 双体素场景编码器：从平面可行走图到预测性3D感知

**Baseline 瓶颈**：TRUMANS 采用扁平化的2D可行走图作为场景表示，丢失了3D空间信息，导致角色在杂乱场景中避障能力不足。

**本文方案**：提出双体素场景编码器（Dual Voxel Scene Encoder），同时编码**当前帧体素**和**预测性场景体素**。当前体素捕获角色即时周围的3D几何信息，预测性体素则提供未来运动路径上的场景先验，使模型能够提前感知障碍物并规划避障路径。

**证据强度**：消融实验（Table 2）显示，将双体素替换为扁平可行走图后，场景穿透指标 Pene_mean 从 0.402 升至 0.587，证明预测性3D场景信息对避障的必要性。定性对比（Fig. 5(a,b)）也表明，本文方法生成的角色能主动绕开场景物体，而 TRUMANS 因依赖预定义轨迹而频繁穿透场景。

### 3. 帧嵌入文本条件：时序语义对齐

**Baseline 瓶颈**：现有方法通常直接使用 CLIP 文本嵌入作为全局条件，缺乏对运动时序的细粒度语义指导，导致长序列合成中动作语义混乱或重复。

**本文方案**：在 CLIP 文本嵌入基础上引入正弦帧嵌入（sinusoidal frame embedding），将时间步信息注入文本条件，形成**帧嵌入文本编码器**。这使得同一文本指令在不同时间帧可以引导不同的子动作（如“走向椅子”在前期引导行走、后期引导坐下），实现时序语义的精确对齐。

**证据强度**：消融实验（Table 1）表明，移除帧嵌入后交互运动 FID 从 2.048 升至 2.368，且合成动作变得无序并倾向于重复（Fig. 5(c,d)），充分验证了帧嵌入对时序语义连贯性的关键作用。

### 创新点总结

三个 changed slots 形成协同效应：**统一自回归扩散框架**提供了多阶段运动生成的模型基础，**自主调度器**消除了人工阶段切换的依赖，**双体素场景编码**赋予角色3D避障能力，而**帧嵌入文本条件**确保了长序列中语义的时序一致性。这些创新共同实现了从“分离模型+人工调度”到“单一文本指令驱动自主交互合成”的范式跃迁。

## 整体框架

本文提出一种统一的自回归扩散框架，从**单一文本指令**和**目标任务位置**出发，自主合成包含行走、伸手触及、物体交互在内的多阶段人-场景交互运动。该框架的核心设计在于将复杂的交互过程建模为连续运动片段的生成序列，并通过自主调度器决定阶段转换时机，从而避免了对预定义路径点或人工阶段切换的依赖。

### 输入输出流

框架接收三类输入：
- **文本指令**：描述角色需要执行的动作（如“走到沙发前坐下”）；
- **目标位置**：交互任务的空间目标点（如沙发位置）；
- **三维场景**：以体素形式编码的环境几何信息。

输出为连续的角色运动序列，包含全身关节旋转和根节点位移，能够自主完成从行走、避障到物体交互的无缝过渡。

### 模块组成与数据流

框架由五个核心模块构成，其协作流程如 **Fig. 2** 所示：

![[assets/figures/papers/paper_list_l1808_LINGO_Autonomous_Character_Scene_Interaction_Synthesis_from_Text_Instruc/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our method. Our method uses an auto-regressive diffusion model that generates the next motion segment based on existing motions (Section 3.2). The 3D environment is captured through a dual voxel scene encoder (Section 3.3). The text instructions are encoded with the time frame to provide precise and time-specific semantic guidance (Section 3.4). The goal encoder (Section 3.5) embeds the sub-goal locations for different interaction stages, which are automatically determined by our autonomous scheduler (Section 3.6)*

1. **Motion Diffusion Module（运动扩散模块）**  
   采用自回归策略，将运动序列划分为固定长度的片段 $X = \{X_i\}_{i=1}^W$。每个片段通过去噪扩散概率模型（DDPM）生成，以上一片段的最后若干帧作为历史条件，实现时序连贯的逐段合成。训练目标为预测噪声的均方误差损失：
   $$\mathcal{L} = \mathbb{E}_{\tilde{X}_t \sim q(\tilde{X}_t \mid C), t \sim U(1, T)} \| \epsilon - \epsilon_\theta(\tilde{X}_t, t, C) \|_2^2$$

2. **Dual Voxel Scene Encoder（双体素场景编码器）**  
   同时编码当前帧周围的三维场景体素和预测性场景体素（即角色未来可能到达区域的几何信息），为运动生成提供即时的避障感知和前瞻性的路径规划能力。消融实验表明，将双体素替换为扁平可行走图后，场景穿透指标 Pene_mean 从 0.402 升至 0.587（**Table 2**），验证了预测性场景信息对避障的必要性。

3. **Frame-embedded Text Encoder（帧嵌入文本编码器）**  
   将 CLIP 文本嵌入与正弦帧嵌入（sinusoidal frame embedding）相结合，为每一帧提供时间特定的语义引导。移除帧嵌入后，交互运动的 FID 从 2.048 升至 2.368，且合成动作出现紊乱和重复（**Table 1; Fig. 5(c,d)**），证明帧嵌入对维持时序语义连贯性至关重要。

4. **Goal Encoder（目标编码器）**  
   根据当前交互阶段编码子目标位置：行走阶段编码移动方向，物体交互阶段编码交互目标点。对于小物体交互，目标嵌入设为零，因为交互过程中身体位置不受特定目标约束。

5. **Autonomous Scheduler（自主调度器）**  
   预测阶段转换的似然概率，自动决定何时从行走阶段切换至伸手触及阶段、从伸手触及阶段切换至物体交互阶段。该模块使框架无需人工指定阶段边界，实现了真正的自主多阶段控制。

### 关键设计决策

与现有方法相比，本框架在三个关键维度上进行了根本性改进：

| 设计维度 | 基线方法 | 本文方法 | 证据 |
|---------|---------|---------|------|
| 运动生成范式 | 分离系统 + 预定义路径点/人工阶段切换 | 统一自回归扩散模型 + 自主调度器 | Section 3.2, 3.6 |
| 场景表示 | 扁平可行走图（TRUMANS）/ 单体素 | 双体素编码器（当前 + 预测场景体素） | Section 3.3, Table 2 |
| 文本条件化 | CLIP 文本嵌入（无帧嵌入） | CLIP 文本嵌入 + 正弦帧嵌入 | Section 3.4, Table 1, Table 3 |

这些设计共同实现了从文本指令到连贯多阶段交互运动的端到端自主合成，无需任何中间人工干预。

### 补充图表

![[assets/figures/papers/paper_list_l1808_LINGO_Autonomous_Character_Scene_Interaction_Synthesis_from_Text_Instruc/figures/001_Figure_1.jpg]]
*Figure 1: Autonomous HSI synthesis. Our proposed method generates realistic character motion in 3D scenes based on a single textual instruction and goal location, incorporating seamless transitions between locomotion and HOI autonomously*

## 核心模块与公式推导

本节解析本文提出的统一自回归扩散框架中五个核心模块的设计动机、功能定位与关键公式，揭示其如何协同实现从文本指令到多阶段人-场景交互的自主合成。

### 3.1 运动扩散模块（Motion Diffusion Module）

该模块是整个框架的生成核心，采用去噪扩散概率模型（DDPM）以自回归方式合成固定长度的运动片段。给定历史运动序列，模型在当前条件信号引导下生成下一段运动，从而实现长序列的连贯合成。

**训练目标**：网络 $\epsilon_\theta$ 学习预测在任意时间步 $t$ 添加到原始运动数据中的噪声 $\epsilon$，损失函数为标准均方误差：

$$\mathcal{L} = \mathbb{E}_{\tilde{X}_t \sim q(\tilde{X}_t \mid C), t \sim U(1, T)} \| \epsilon - \epsilon_\theta(\tilde{X}_t, t, C) \|_2^2$$

其中 $\tilde{X}_t$ 表示在时间步 $t$ 被噪声扰动的运动片段，$C$ 为条件信号集合（包含场景编码、文本嵌入、目标编码等），$T$ 为扩散总步数。该损失驱动模型在推理阶段从纯噪声逐步去噪，恢复出符合条件约束的运动序列。

**自回归生成**：推理时，模型以固定窗口长度 $W$ 逐段生成运动 $X = \{X_i\}_{i=1}^W$，当前段生成完毕后滑入历史窗口，作为下一段生成的条件输入。这种设计使模型能够处理任意长度的交互序列，同时保持相邻片段间的运动连贯性。

### 3.2 双体素场景编码器（Dual Voxel Scene Encoder）

场景感知是人-场景交互合成的关键挑战。本文提出双体素场景表示，同时编码当前帧的局部场景体素和预测帧的局部场景体素，为模型提供即时的障碍物信息和前瞻性的空间约束。

**设计动机**：TRUMANS（Jiang et al., SIGGRAPH 2024）等基线方法采用扁平可行走图作为场景表示，仅提供二维地面信息，缺乏对三维空间结构的完整感知。消融实验表明，将双体素替换为扁平可行走图后，场景穿透指标 Pene_mean 从 0.402 显著升至 0.587（Table 2），验证了预测性三维场景信息对避障的必要性。

**工作机制**：编码器分别对角色当前位置周围的体素化场景和未来预测位置周围的体素化场景进行卷积编码，提取多尺度空间特征。两部分特征融合后注入扩散模型的条件信号中，使生成的运动既能即时避开障碍物，又能提前规划路径。

### 3.3 帧嵌入文本编码器（Frame-embedded Text Encoder）

文本指令为运动生成提供高层语义指导，但传统 CLIP 文本嵌入缺乏时序维度，无法区分同一指令在不同执行阶段应产生的差异化动作。

**设计动机**：消融实验（Table 1）显示，移除帧嵌入后 FID 从 2.048 升至 2.368，且合成动作变得无序并倾向于重复（Fig. 5c,d）。这证明帧嵌入对时序语义连贯性至关重要。

**实现方式**：将 CLIP 文本嵌入与正弦帧嵌入（sinusoidal frame embedding）相结合。帧嵌入编码当前运动片段在整体序列中的相对位置，使模型能够根据执行进度调整动作语义——例如，“走向沙发并坐下”指令中，早期帧应生成行走动作，后期帧应生成坐下动作。

### 3.4 目标编码器（Goal Encoder）

不同交互阶段具有不同的子目标：行走阶段需要方向指引，物体交互阶段需要目标物体位置，而小物体交互阶段则无需空间目标。

**阶段特定编码**：目标编码器根据当前阶段的类型，将子目标位置（行走方向向量或交互目标坐标）编码为条件信号。对于涉及小物体的交互（如抓取杯子），目标嵌入设为零向量，因为交互过程中身体位置不由目标物体决定。

**穿透修正**：在物体到达阶段，若生成的手部关节与场景物体发生穿透，模型通过计算穿透关节最近表面点的平均法线方向，沿该方向平移手部关节以解决穿透问题。这一后处理步骤有效提升了交互的物理合理性。

### 3.5 自主调度器（Autonomous Scheduler）

传统方法需要用户手动指定阶段转换时机，限制了系统的自主性。自主调度器是本文实现端到端自主合成的关键创新。

**核心功能**：调度器在每个时间步预测当前阶段向下一阶段转换的概率，当概率超过阈值时自动触发阶段切换。这一机制使模型能够根据运动进度和场景上下文自主决定何时从行走阶段过渡到伸手阶段、从伸手阶段过渡到交互阶段，无需人工干预。

**与框架的协同**：调度器的预测结果同时影响目标编码器的阶段选择，形成闭环控制——调度器决定当前阶段，目标编码器提供该阶段对应的子目标信号，运动扩散模块据此生成相应动作，动作进度又反馈给调度器以判断是否切换阶段。这一设计实现了多阶段人-场景交互的全自主合成。

## 实验与分析

### 核心实验结果

本文在三个互补任务上系统评估了所提方法：交互运动合成、杂乱场景中的行走运动、以及物体伸手动作。所有定量对比均在 LINGO 数据集上完成，训练集为 LINGO-train，评估集为 LINGO-eval。为保证公平性，对比时将基线方法 TRUMANS 的动作编码器替换为与本文相同的文本编码器（CLIP+MLP）。

**交互运动合成**（Table 1）是本方法的核心测试场景，要求角色根据文本指令在场景中完成与物体的交互。本文方法在 FID 指标上达到 **2.048 ± 0.058**，显著优于 TRUMANS 的 2.438 ± 0.041（Δ = -0.390），同时取得了更高的精度和召回率。这表明自回归扩散框架生成的交互运动在分布质量和语义准确性上均优于依赖预定义路径点的分离式系统。

**杂乱场景中的行走运动**（Table 2）测试角色在障碍物密集环境中的避障能力。本文方法的场景穿透指标 Pene_mean 仅为 **0.402 ± 0.004**，远低于 TRUMANS 的 1.011 ± 0.012（Δ = -0.609），降幅超过 60%。这一优势源于双体素场景编码器提供的预测性 3D 场景信息，使模型能主动规划避障路径，而非仅依赖扁平可行走图的被动约束。

**物体伸手动作**（Table 3）评估角色走向并伸手接触物体的精度。本文方法的到达误差仅为 **0.061 ± 0.004**，相比 GOAL（Taheri et al., CVPR 2022）的 0.156 ± 0.028 降低了约 61%（Δ = -0.095）。值得注意的是，GOAL 是专门针对物体伸手任务设计的方法，而本文的统一框架在此任务上仍表现出明显优势。

### 消融实验

消融实验揭示了三个关键设计选择的因果作用：

**帧嵌入的时序语义引导**：移除帧嵌入后（Table 1, w/o frame embedding），交互运动合成的 FID 从 2.048 升至 2.368，且合成动作出现紊乱和重复倾向（Fig. 5(c,d)）。这证明帧嵌入通过将时间位置编码注入文本条件，为自回归生成提供了必要的时序语义连贯性——没有这一信号，模型无法区分“走向沙发”和“坐在沙发上”的阶段顺序。

**双体素场景表示的避障能力**：将双体素场景编码替换为扁平可行走图后（Table 2, flattened voxel），Pene_mean 从 0.402 升至 0.587，穿透显著增加。这表明预测性体素信息（包含当前帧和未来帧的场景占用）对主动避障至关重要，而扁平表示仅能提供当前帧的可行走区域约束。

**场景感知对伸手精度的影响**：移除双体素场景编码后（Table 3, w/o dual voxel），物体到达误差从 0.061 升至 0.111。即使伸手动作本身主要依赖目标编码器，场景上下文仍为角色提供了身体定位和路径规划的辅助信息。

### 定性分析

Fig. 3 的定性对比直观展示了本文方法与 TRUMANS 的差异：左侧行走场景中，本文方法生成的角色主动绕开场景障碍物，而 TRUMANS 依赖预定义轨迹导致穿透；右侧“坐在沙发上”的交互中，本文方法展现出自然的场景感知线索（如身体朝向调整和接触前减速），而 TRUMANS 的合成动作缺乏此类细节。

![[assets/figures/papers/paper_list_l1808_LINGO_Autonomous_Character_Scene_Interaction_Synthesis_from_Text_Instruc/figures/003_Figure_3.jpg]]
*Figure 3: Comparison results. We qualitatively compare our method with TRUMANS [Jiang et al. 2024]. The left side shows the locomotion along a trajectory, and the right side shows the interaction of sitting on the sofa. Our method generates characters that actively avoid penetrating the scene and exhibit natural cues of scene awareness. For more qualitative results, we refer readers to the supplementary video*

### 局限性与失败模式

尽管在主要指标上表现优异，本文方法存在以下已知局限：

1. **精细操作缺失**：当前框架未涵盖面部表情和手部精细操作（如手指级抓取），这限制了其在需要高精度手物交互场景中的应用。

2. **物理合理性未完全保证**：生成运动的动力学约束（如接触力、动量守恒）未显式建模，可能导致脚部滑动或穿透等物理不合理现象。Table 2 中的 foot sliding 指标虽有改善但仍存在。

![[assets/figures/papers/paper_list_l1808_LINGO_Autonomous_Character_Scene_Interaction_Synthesis_from_Text_Instruc/figures/006_Table_2.jpg]]
*Table 2: Quantitative results of locomotion, where the character walks from one place to another in cluttered scenes*

3. **泛化性未充分验证**：模型对训练中未出现的交互类型和场景布局的泛化能力尚需进一步测试。当前实验均在 LINGO 数据集的分布内进行评估。

4. **自主调度器的长期任务性能未知**：自主调度器在多步序列任务（如“先走到桌子旁，拿起杯子，然后走到沙发坐下”）中的阶段转换准确性尚未系统评估。

### 数据集统计

LINGO 数据集包含丰富的运动类型分布（Table A1, Fig. 6），涵盖行走、伸手、坐下、抓取等常见人-场景交互动作。运动片段长度分布（Fig. A2）和行走目标位置分布（Fig. A3）显示了数据的多样性和空间覆盖范围。VR 辅助的动作捕捉设置（Fig. 4）保证了运动数据的质量和场景交互的真实性。

![[assets/figures/papers/paper_list_l1808_LINGO_Autonomous_Character_Scene_Interaction_Synthesis_from_Text_Instruc/figures/004_Figure_4.jpg]]
*Figure 4: LINGO dataset. We show some selected frames and the setup of the VR-assisted MoCap*

![[assets/figures/papers/paper_list_l1808_LINGO_Autonomous_Character_Scene_Interaction_Synthesis_from_Text_Instruc/figures/009_Figure_6.jpg]]
*Figure 6: Number of occurrences of each motion type in LINGO dataset*

![[assets/figures/papers/paper_list_l1808_LINGO_Autonomous_Character_Scene_Interaction_Synthesis_from_Text_Instruc/figures/011_Table.jpg]]
*Table: A1. Motion types of LINGO*

![[assets/figures/papers/paper_list_l1808_LINGO_Autonomous_Character_Scene_Interaction_Synthesis_from_Text_Instruc/figures/012_Figure.jpg]]
*Figure: Fig. A2. Motion length distribution of each motion type in LINGO dataset. Fig. A3. Distribution of goal locations for all locomotion clips in the local coordinate system of the first frame. The character is aligned to initially face the y-axis direction. Unit: meter*

### 补充图表

![[assets/figures/papers/paper_list_l1808_LINGO_Autonomous_Character_Scene_Interaction_Synthesis_from_Text_Instruc/figures/005_Table_1.jpg]]
*Table 1: Quantitative results of interactive motion synthesis. The instructions involve performing interaction with an object in the scene*

![[assets/figures/papers/paper_list_l1808_LINGO_Autonomous_Character_Scene_Interaction_Synthesis_from_Text_Instruc/figures/007_Table_3.jpg]]
*Table 3: Quantitative results of object reaching, where the character is instructed to walk toward and reach for an object*

![[assets/figures/papers/paper_list_l1808_LINGO_Autonomous_Character_Scene_Interaction_Synthesis_from_Text_Instruc/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative comparison. We compare (a) our method with (b) TRUMANS [Jiang et al. 2024] on the task of walking to the goal location. It is shown that our method is aware of the surroundings for collision avoidance, while TRUMANS depends on a pre-defined trajectory. We show (c) our method and (d) w/o frame embedder given “grasp an object” instruction. The synthesized motion without a frame embedder is disordered and tends to repeat*

## 方法谱系与知识库定位

### 1. 核心问题定位

现有角色-场景交互（HSI）合成方法在架构上存在根本性割裂：它们依赖多个分离模型分别处理行走、伸手、物体交互等不同运动阶段，并要求用户手动指定路径点和阶段转换时机。以 **TRUMANS**（Jiang et al., SIGGRAPH 2024）为代表的现有方案，其运动合成依赖于预定义轨迹和显式的阶段切换指令，缺乏从单一文本指令和目标任务位置自主生成连贯多阶段人-场景交互的统一框架。这种分离式设计导致运动连贯性差、场景感知能力弱，且实用性严重受限。

### 2. 方法谱系定位

本文方法在以下三个维度上实现了对现有工作的系统性改进：

| 方法维度 | 现有方案 | 本文方案 | 改进本质 |
|---------|---------|---------|---------|
| **运动生成范式** | 分离系统 + 手动路径点/阶段切换（如 TRUMANS） | 统一自回归扩散模型 + 自主调度器 | 从"人工编排"到"自主合成"的范式转变 |
| **场景表示** | 扁平可行走图（TRUMANS）/ 单体素 | 双体素编码器（当前 + 预测性场景体素） | 从"2D投影"到"3D预测性感知"的表示升级 |
| **文本条件化** | CLIP 文本嵌入（无帧信息） | CLIP + 正弦帧嵌入 | 从"静态语义"到"时序语义"的条件增强 |

#### 2.1 与 TRUMANS 的关系

TRUMANS 是本文最直接对比的基线方法。两者均面向人-场景交互运动合成，但核心差异在于控制模式：TRUMANS 需要预定义轨迹和阶段切换指令，而本文通过自主调度器（Autonomous Scheduler）自动预测阶段转换时机，使模型能从单一文本指令生成包含路径规划、场景避障和交互动作的完整运动序列。实验表明，在交互运动合成中本文的 FID 为 2.048，显著优于 TRUMANS 的 2.438（Table 1）；在杂乱场景中的场景穿透指标 Pene_mean 为 0.402，远低于 TRUMANS 的 1.011（Table 2），证明了自主调度与双体素场景感知的联合优势。

#### 2.2 与 GOAL 的关系

**GOAL**（Taheri et al., CVPR 2022）是物体伸手动作合成的代表性方法。本文在物体到达任务上与 GOAL 进行了直接对比，到达误差从 GOAL 的 0.156 降至 0.061（Table 3），表明统一框架在保持伸手动作精度的同时，实现了与行走阶段的自主衔接。

#### 2.3 技术谱系中的位置

从扩散模型在运动生成中的应用谱系来看，本文属于**条件自回归扩散生成**路线。与单阶段扩散运动生成方法不同，本文引入自回归生成策略，将长序列运动分解为固定长度的运动片段逐段生成，并通过帧嵌入维持跨片段的时间语义连贯性。消融实验证实，移除帧嵌入导致 FID 从 2.048 升至 2.368，且合成动作出现紊乱和重复（Table 1; Fig. 5(c,d)），验证了该设计的必要性。

### 3. 适用边界与局限

本文方法存在以下明确局限：

1. **交互粒度受限**：当前框架未涵盖面部表情和手部精细操作（如手指级抓取）的合成，仅处理全身级别的物体交互。这意味着对于需要精细手部姿态的交互场景（如打字、弹琴），方法尚不具备直接适用性。

2. **物理合理性未完全保证**：生成运动的物理约束（如动力学、接触力、摩擦力等）未在框架中显式建模。尽管通过后处理步骤（如穿透解决）缓解了部分问题，但运动的物理真实性（如重心平衡、动量守恒）缺乏严格保证。这一局限在快速转向或复杂地形场景中可能更为突出。

3. **泛化能力待验证**：模型在 LINGO 数据集上训练和评估，对训练中未出现的交互类型和场景布局的泛化能力尚未充分验证。开放词汇指令下的零样本泛化能力仍是未解决的问题。

4. **数据集规模与多样性**：LINGO 数据集虽覆盖多种交互类型，但相比自然语言指令的开放空间，其动作类型和场景多样性的覆盖仍有限，可能限制模型在真实应用中的鲁棒性。

### 4. 开放问题

基于本文的局限和技术路线，以下问题值得后续探索：

1. **精细操作与表情的联合合成**：如何将自回归扩散框架扩展到手部精细操作和面部表情的联合生成，实现从"身体级"到"全身级"交互合成的跨越？

2. **物理模拟与生成模型的融合**：能否将物理模拟器作为后处理或联合优化模块，在保持扩散模型生成多样性的同时，提高运动的物理可行性？这一方向可能涉及可微分物理与去噪扩散过程的深度耦合。

3. **开放词汇泛化**：如何利用大规模语言-运动预训练或元学习策略，提升模型对未见交互类型和开放词汇指令的泛化能力？

4. **长期任务规划**：自主调度器在更复杂的长期多步序列任务（如"走到桌子旁，拿起杯子，走到沙发坐下"）中的性能如何？当前的单步阶段预测能否扩展为层次化任务规划？

5. **多智能体场景扩展**：本文聚焦单角色-场景交互，未来是否可将框架扩展至多角色协同交互场景，处理角色间避障和协作动作的自主合成？

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2024/LINGO_Autonomous_Character_Scene_Interaction_Synthesis_from_Text_Instruction.pdf]]