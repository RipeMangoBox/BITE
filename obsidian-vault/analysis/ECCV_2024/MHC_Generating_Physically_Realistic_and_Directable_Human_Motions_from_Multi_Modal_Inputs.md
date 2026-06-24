---
title: MHC Generating Physically Realistic and Directable Human Motions from Multi Modal Inputs
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/MHC_Generating_Physically_Realistic_and_Directable_Human_Motions_from_Multi_Modal_Inputs.pdf
aliases:
- MHCM
- MGPRDHMFMMI
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过在强化学习中随机掩码运动指令的通道和关节，结合增强数据集和多部位风格判别器，迫使控制器学习利用部分信息生成自然运动。
primary_logic: 掩码训练迫使策略隐式学习运动先验和协调能力，从而统一实现从不完整、组合或不同步的指令中生成物理一致的自然运动。
claims:
- MHC在模仿、追赶、组合任务中显著优于ASE基线，MPJPE从123.51降至51.05，成功率从0.6升至0.92。
- 消融实验显示移除风格奖励导致训练完全失败（MPJPE 552.25, 成功率0.0）。
- MHC在不同通道掩码和高达75%关节掩码下保持稳定性能，且优于未掩码训练的ASE。
- MHC与DAC-MDP集成，实现零样本高层任务规划（如目标导航与动作执行）。
---

# MHC Generating Physically Realistic and Directable Human Motions from Multi Modal Inputs

> [!tip] 核心洞察
> 掩码训练迫使策略隐式学习运动先验和协调能力，从而统一实现从不完整、组合或不同步的指令中生成物理一致的自然运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | MHC：从多模态输入生成物理真实且可指导的人体运动 |
| 英文题名 | MHC Generating Physically Realistic and Directable Human Motions from Multi Modal Inputs |
| 会议/期刊 | ECCV 2024 |
| Links | [Project](https://idigitopia.github.io/projects/mhc/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Masked Humanoid Controller (MHC) |
| Dataset | Imitation on Reallusion M_Real |

> [!tip] 效果简介
> - Imitation on Reallusion M_Real 上，MPJPE (mm) 51.05 vs 123.51 (-72.46)；Success Rate 0.92 vs 0.60 (+0.32)。

## 概述

### 1. 问题瓶颈

物理仿真中的人体运动生成面临一个核心矛盾：现有基于物理的类人控制器无法同时具备**追赶（Catch-up）**、**组合（Combine）** 和**补全（Complete）** 三项能力（合称 CCC）。追赶要求控制器从不同步的姿态出发追踪运动指令；组合要求控制器模仿由不同运动片段拼接而成的上下半身指令；补全要求控制器从稀疏、欠指定的关节信息中还原完整运动。传统方法（如 **ASE**，Peng et al., ACM TOG 2022）依赖完全指定的运动指令，难以处理现实世界中多模态输入天然存在的稀疏性、不同步性和局部性。

### 2. 核心方法：掩码类人控制器（MHC）

本文提出 **MHC（Masked Humanoid Controller）**，一种基于强化学习的多目标模仿学习框架。其核心调控变量是**指令掩码（Directive Masking）**：在训练过程中随机掩盖运动指令的部分通道（如根状态、关节旋转、局部/全局位置）和部分关节，迫使策略网络隐式学习运动先验与关节协调能力。与之配套的关键设计包括：

- **增强运动数据集（M⁺）**：通过随机拼接上下半身运动片段并施加平面旋转，制造突兀的动作转换，迫使控制器学习组合能力。
- **多部位风格判别器集成**：为根、左上肢、右上肢、下半身、全身五个部位分别训练判别器，以正则化对抗损失提供风格奖励，确保生成运动的自然性。
- **分级追踪奖励**：按优先级依次激活根高度、根朝向、根速度、关节欧拉角奖励，仅当前置奖励超过阈值（0.9）时才激活后续项，引导策略优先稳定根运动。

MHC 将问题建模为强化学习：每个 episode 随机采样初始姿态（混合数据集姿态与跌倒姿态）和掩码运动指令，策略网络以当前姿态和未来 H 步的掩码指令为输入，输出关节目标位置，经 PD 控制器转换为力矩驱动物理仿真。

### 3. 核心结论

MHC 在 87 种运动技能的数据集上训练后，统一实现了 CCC 三项能力。定量结果表明：

- **模仿任务**：MHC 的 MPJPE（每关节平均位置误差）为 51.05 mm，成功率 0.92，显著优于 ASE 基线（MPJPE 123.51 mm，成功率 0.60）。
- **掩码鲁棒性**：MHC 在不同通道掩码组合以及高达 75% 关节掩码下保持稳定性能，且始终优于接受完全指定指令的 ASE。
- **消融验证**：移除风格奖励导致训练彻底失败（MPJPE 552.25，成功率 0.0）；移除随机姿态初始化削弱追赶能力；移除运动指令增强削弱组合能力。
- **零样本规划集成**：MHC 可与有限状态机（FSM）和 DAC-MDP 规划器无缝集成，实现目标导航与动作执行等高层任务，无需额外训练。

### 4. 方法谱系与知识库定位

MHC 属于**物理仿真驱动的运动生成**方向，继承自基于对抗技能嵌入（ASE）的类人控制框架，但通过指令掩码训练范式实现了关键突破。与依赖完整运动指令的 ASE 不同，MHC 的掩码训练使其天然兼容多模态输入（VR 设备、手柄、视频提取的 3D 关节、文本生成的运动），将不同模态统一为“部分指定的运动指令”这一抽象表示。在规划集成层面，MHC 作为低层运动原语执行器，与数据驱动规划器（DAC-MDP）构成分层架构，实现了从高层任务目标到物理真实运动的端到端生成。

## 背景与动机

### 问题背景：物理仿真中的人体运动生成

生成物理真实且可操控的人体运动是计算机图形学与具身智能的核心挑战之一。在物理仿真环境中，运动生成器（或称控制器）需要在遵循物理定律的前提下，驱动仿人机器人跟踪特定的运动指令（directive），同时保持动作的自然性与风格一致性。这类指令可以来自多种模态：动作捕捉（MoCap）数据、VR手柄、游戏摇杆、视频提取的3D关节位置，乃至文本到动作的生成器输出。

### 现有方法的缺口：CCC能力的三重缺失

现有的物理类人控制器在设计上普遍存在一个结构性瓶颈：它们无法同时具备**追赶（Catch-up）、组合（Combine）和补全（Complete）**这三项关键能力。

- **追赶（Catch-up）**：当仿人机器人的初始姿态与指令不同步时（例如从跌倒状态开始），控制器需要自主调整并追上目标运动。
- **组合（Combine）**：当指令由不同运动片段的上半身与下半身拼接而成时，控制器需要协调地合成出物理一致的整体运动。
- **补全（Complete）**：当指令仅提供稀疏的部分关节信息（如仅头部、手部和脚部位置）时，控制器需要推断并补全缺失的关节运动。

传统的模仿学习方法通常假设指令是完整、同步且单一片段式的，因此在这三类场景下表现脆弱。以主要对比基线**ASE**（Adversarial Skill Embeddings, Peng et al., ACM TOG 2022）为例，其训练过程依赖完全指定的运动指令，缺乏处理不完整或组合式指令的机制。

### 核心动机：用掩码训练统一处理多模态稀疏指令

本文的核心动机在于：**能否通过一种统一的训练范式，使控制器在面对不完整、不同步或组合式的多模态指令时，都能生成物理一致且自然的运动？**

作者的关键洞察是：**掩码训练**可以迫使策略隐式地学习运动先验与关节间协调能力。具体而言，在强化学习训练过程中，随机掩盖运动指令的特定通道（如根位移、关节旋转、局部/全局位置）或特定关节，迫使控制器仅凭部分信息推断完整的运动模式。这一机制与语言模型中的掩码预训练逻辑相通——通过“遮挡”迫使模型学习数据的内在结构。

### 方法定位

MHC并非从头构建全新的控制器架构，而是在现有物理角色控制框架的基础上，通过以下关键改造实现CCC能力：

1. **指令掩码机制**：在训练时对运动指令施加通道级与关节级随机掩码。
2. **增强数据集**：通过拼接上下半身运动片段并施加平面旋转，构建更具挑战性的训练数据。
3. **多部位风格判别器**：使用5个独立判别器（左上肢、右上肢、根关节、下半身、全身）提供细粒度风格奖励，替代单一判别器。
4. **分级跟踪奖励**：将跟踪目标按根高度→根朝向→根速度→关节欧拉角的优先级分层激活，仅当前置奖励达标后才激活后续奖励。

这些设计共同使MHC成为首个同时实现追赶、组合、补全能力的物理运动生成器，并可与有限状态机（FSM）及数据驱动规划器（如DAC-MDP）无缝集成，实现零样本的高层任务规划。

## 核心创新

MHC 的核心创新在于**通过指令掩码训练，将物理类人控制器的能力边界从单一模仿扩展到追赶（Catch-up）、组合（Combine）与补全（Complete）的统一框架**。现有物理控制器（如 ASE，Peng et al., ACM TOG 2022）要求完全指定的运动指令，无法处理稀疏、不同步的多模态输入。MHC 通过在强化学习训练中引入通道级与关节级随机掩码，迫使策略隐式学习运动先验与协调能力，从而在推理时仅凭部分指令即可生成物理一致的自然运动。

### 关键改动槽位（Changed Slots）

**1. 指令掩码（Directive Masking）**

- **Baseline 做法**：完全指定的运动指令，所有通道和关节信息均可见。
- **MHC 做法**：在训练时随机施加两类掩码——通道级掩码（随机掩盖根状态、关节旋转、局部/全局位置等通道）和关节级掩码（随机掩盖 0%–75% 的关节）。推理时，策略可接受任意掩码模式下的不完整指令，实现从 VR、手柄、视频、文本等多模态输入的零样本运动生成。
- **证据**：Figure 6 显示，未使用掩码训练的 MHC 在通道掩码或关节掩码下性能急剧退化，而使用掩码训练的 MHC 在不同掩码模式下保持稳定，且显著优于接收完全指定指令的 ASE 基线。

**2. 初始姿态分布（Initial Pose Distribution）**

- **Baseline 做法**：仅从数据集中采样姿态作为初始状态。
- **MHC 做法**：混合数据集姿态与跌倒姿态（跌倒权重 0.1），并随机施加平面内旋转。这使策略在训练中频繁遭遇“不同步”的初始状态，从而学会从任意姿态追赶目标运动。
- **证据**：消融实验（Table 1, catchup ablation）表明，移除随机姿态初始化会削弱追赶能力。

**3. 目标运动增强（Target Motion Augmentation）**

- **Baseline 做法**：使用单段完整运动序列作为跟踪目标。
- **MHC 做法**：构建增强数据集 $M^+$，通过随机拼接不同运动的上半身与下半身子序列（长度 120–240 帧）并施加随机旋转，制造突兀的动作转换。这迫使策略学习如何将来自不同运动的身体部位指令组合为连贯运动。
- **证据**：消融实验（Table 1, combine ablation）显示，移除运动增强（即仅在原始数据集 $M$ 上训练）会导致组合任务性能下降。

**4. 风格奖励（Style Reward）**

- **Baseline 做法**：无风格奖励或使用单一判别器。
- **MHC 做法**：引入 5 个身体部位（左上肢、右上肢、躯干、下半身、全身）的独立判别器，输入 10 帧运动子序列，使用正则化对抗损失。多部位判别器为策略提供细粒度的自然度反馈，是训练稳定的关键。
- **证据**：消融实验（Table 1, MHC(abl)）表明，移除风格奖励导致模仿任务彻底失败（MPJPE 552.25 mm，成功率 0.0）。

**5. 跟踪奖励优先级（Tracking Reward Priority）**

- **Baseline 做法**：各奖励项均匀加权。
- **MHC 做法**：采用分级奖励机制——根高度奖励 $r_t^h$ → 根朝向奖励 $r_t^o$ → 根速度奖励 $r_t^v$ → 关节欧拉角奖励 $r_t^l$，仅当前置奖励超过阈值 0.9 时才激活后续奖励。这种设计确保策略优先稳定根状态，再精细匹配关节姿态。
- **证据**：该设计体现在公式 Eq. 1–4 的条件激活机制中，是 MHC 在高度不完整指令下仍能维持物理稳定性的重要因素。

### 因果机制总结

掩码训练是 MHC 统一 CCC 能力的**核心因果旋钮**：通过随机剥夺部分运动信息，策略被迫从剩余信息中推断缺失部分，从而隐式学习运动先验与全身协调模式。增强数据集 $M^+$ 和跌倒姿态初始化分别强化了组合与追赶能力，多部位风格判别器则提供了必要的自然度约束。这五个改动槽位相互依赖——移除任一项均会导致特定能力或整体性能的显著退化。

## 整体框架

MHC（Masked Humanoid Controller）的整体框架围绕一个核心矛盾展开：**如何让物理仿真中的人形机器人，从稀疏、不同步、甚至不完整的运动指令中，生成物理真实且风格自然的运动**。传统物理类人控制器（如ASE, Peng et al., ACM TOG 2022）要求完全指定的运动指令，缺乏对不完整信息的鲁棒性，无法同时具备追赶（Catch-up）、组合（Combine）和补全（Complete）这三项关键能力。MHC通过在强化学习训练中引入**指令掩码**这一因果调节旋钮，迫使策略隐式学习运动先验与跨关节协调机制，从而统一解决上述问题。

### Pipeline 总览

MHC的pipeline由五个核心模块串联构成，形成“指令生成—策略推理—物理执行—多部位风格判别—奖励反馈”的闭环：

1. **数据增强模块（M+）**  
   从原始MoCap数据集中，通过随机拼接上下半身的不同运动子序列（长度120–240帧），并施加平面内随机旋转，构造出包含突兀运动转换的增强数据集 $M^+$。这一步骤为后续的组合（Combine）能力提供训练基础。

2. **指令掩码生成**  
   对增强后的目标运动指令 $\hat{q}_{t+1:t+H}$ 施加两类随机掩码：**通道级掩码**（随机掩盖根状态、关节旋转、局部位置或全局位置中的若干通道）和**关节级掩码**（随机掩盖0%至75%的关节）。掩码后的指令 $(\hat{q}, I)$ 作为策略网络的输入，其中 $I$ 为指示各通道/关节是否可见的掩码张量。

3. **策略网络（Controller）**  
   策略网络以当前人形机器人姿态 $q_t$ 和未来 $H$ 步的掩码指令为输入，输出各关节的目标位置（动作）。该网络通过PD控制器将目标位置转换为关节力矩，驱动物理仿真环境中的运动。

4. **多部位风格判别器集成**  
   5个独立判别器分别对左上肢、右上肢、根关节、下半身和全身这五个身体部位进行风格评估。每个判别器输入10帧运动子序列，使用正则化对抗损失，为策略提供细粒度的风格奖励信号，鼓励生成自然运动。

5. **PPO训练循环**  
   整个系统使用PPO算法进行端到端强化学习训练。每个episode随机采样初始姿态（混合数据集姿态与跌倒姿态，跌倒权重0.1，并施加随机旋转）和掩码指令。奖励函数由分级跟踪奖励、多部位风格奖励和能量惩罚项加权构成，驱动策略同时优化运动精度与自然度。

### 输入输出流

- **输入**：人形机器人当前姿态 $q_t$（包含根关节状态、关节旋转、局部位置、全局位置）以及未来 $H$ 步的掩码目标指令 $(\hat{q}_{t+1:t+H}, I_{t+1:t+H})$。
- **输出**：各关节的目标位置，经PD控制器转换为力矩后，驱动仿真环境中的物理运动。
- **奖励信号**：分级跟踪奖励（根高度 $\to$ 根朝向 $\to$ 根速度 $\to$ 关节欧拉角，仅当前置奖励阈值 > 0.9 时激活后续奖励）、多部位风格奖励、能量惩罚项（抑制高频抖动）。

### 关键设计决策

框架中的三个设计决策对最终能力起决定性作用：

- **掩码训练**是因果核心：消融实验表明，未使用指令掩码训练的MHC在通道掩码下性能严重退化（Figure 6左），且随关节掩码比例增加性能急剧下降（Figure 6右）。掩码迫使策略学习从部分信息推断整体运动的能力。
- **增强数据集 $M^+$** 是组合能力的必要条件：移除运动指令增强（不使用 $M^+$）直接导致组合任务性能下降（Table 1, combine ablation）。
- **多部位风格判别器**是训练稳定的基石：移除风格奖励导致模仿任务完全失败，MPJPE从51.05飙升至552.25，成功率从0.92降至0.0（Table 1, MHC(abl)）。

### 与高层规划的集成

MHC的掩码指令接口天然支持与高层规划框架的零样本集成。通过将抽象动作映射为特定的掩码指令模式，MHC可直接作为有限状态机（FSM）或数据驱动规划器（DAC-MDP）的低层执行器，无需针对新任务进行微调或额外的RL训练（Figure 8, Section 6.3）。这种模块化设计使得MHC既能独立完成运动生成任务，又能作为更大智能系统的物理运动执行组件。

### 补充图表

![[assets/figures/papers/paper_list_l1876_MHC_Generating_Physically_Realistic_and_Directable_Human_Motions_from_Mu/figures/003_Figure_3.jpg]]
*Figure 3: Illustrates the architecture and training details of the MHC framework, which consists of a controller and an ensemble of discriminators. Here the controller is trained to follow an augmented set of masked directives derived from the provided MoCap dataset. The controller gets feedback via tracking objective and style rewards generated by the ensemble of discriminators. Together they enable a directable policy to generate physically realistic motions capable of catching up, combining primitives, and completing motions from under-specified directives. (Figure layout adapted from [35])*

![[assets/figures/papers/paper_list_l1876_MHC_Generating_Physically_Realistic_and_Directable_Human_Motions_from_Mu/figures/002_Figure_2.jpg]]
*Figure 2: Shows generated motions that illustrate the CCC capabilities. From left to right: MHC is able to generate motions that (1) adjust and catchup starting from an out-of-sync pose, (2) imitate a target directive that combines upper and lower body sub-segments from different motions, and (3) complete the motion from under-specified directives as indicated by missing target outlines*

## 核心模块与公式推导

### 问题形式化

MHC 将人体运动定义为一个多通道姿态序列 $q_{1:H}$，其中每一帧姿态 $q_i$ 由四个通道组成：$q_i = (q^r, q^\theta, q^l, q^g)$，分别对应根关节状态、3D 关节旋转、局部关节位置和全局关节位置。运动指令以二元掩码 $I_{t+1:t+H}$ 标记未来 $H$ 步中哪些通道/关节被提供，控制器接收当前姿态 $q_t$ 与掩码指令 $(\hat{q}_{t+1:t+H}, I_{t+1:t+H})$，输出关节目标位置，经由 PD 控制器转换为力矩驱动物理仿真。

### 核心模块

**1. 指令掩码机制（Directive Masking）**

掩码训练是 MHC 实现 CCC 能力（追赶、组合、补全）的核心因果杠杆。训练时对运动指令施加两类随机掩码：
- **通道级掩码**：随机掩盖根状态、关节旋转、局部位置或全局位置等通道，模拟不同输入模态（如 VR 仅提供头手位置、视频仅提供部分 3D 关节坐标）。
- **关节级掩码**：随机掩盖 0%–75% 的关节，迫使策略从稀疏观测中推断全身运动。

掩码迫使策略隐式学习运动先验与协调能力，从而在推理时统一处理不完整、组合或不同步的指令。

**2. 增强数据集 M+**

为训练组合能力，从原始动作捕捉数据集中随机拼接不同运动的上半身与下半身子序列（长度 120–240 帧），并施加随机平面内旋转，制造突兀的运动转换。这使控制器学会平滑连接来自不同运动的身体部位。

**3. 多部位风格判别器集成**

采用 5 个独立判别器，分别对应左上肢、右上肢、根关节、下半身和全身，输入为 10 帧运动子序列。使用正则化对抗损失为策略提供风格奖励，鼓励生成自然运动。消融实验表明，移除风格奖励导致训练完全失败（MPJPE 552.25，成功率 0.0）。

**4. 分级跟踪奖励**

跟踪奖励采用级联激活机制，仅当前置奖励超过阈值 0.9 时才激活后续奖励，优先级为：根高度 > 根朝向 > 根速度 > 关节欧拉角。奖励函数定义如下：

$$r_t^{tr} = r_t^h + r_t^o + r_t^v + r_t^l$$

**根高度奖励**：
$$r_t^h = e^{-m_h \cdot 8 || q_t^h - \hat{q}_t^h ||_2}$$

**根朝向奖励**（仅当 $r_t^h > 0.9$ 时激活）：
$$r_t^o = I(r_t^h > 0.9) \cdot e^{-m_o \cdot || d(q_t^o - \hat{q}_t^o) ||_2}$$

**根速度奖励**（仅当 $r_t^o > 0.9$ 时激活）：
$$r_t^v = I(r_t^o > 0.9) \cdot e^{-m_v \cdot || q_t^v - \hat{q}_t^v ||_2}$$

**关节欧拉角奖励**（仅当 $r_t^v > 0.9$ 时激活）：
$$r_t^l = I(r_t^v > 0.9) \cdot \frac{1}{\sum_{j \in J} m_j} \sum_{j \in J} e^{-m_j \cdot 40 || q_t^j - \hat{q}_t^j ||_2}$$

其中 $m_h, m_o, m_v, m_j$ 为二元掩码系数：若对应奖励分量依赖的姿态信息未被当前指令掩码选中，则置 0（不计入损失），否则为 1。

**5. 能量惩罚项**

为消除脚部高频抖动，引入动作平滑与力矩惩罚：
$$c_t = \sum_{j \in J} 0.01 \cdot || a_t^j - a_{t-1}^j ||_1 + 0.0002 \cdot || \tau_t^j ||_1$$

### 训练流程

MHC 训练形式化为强化学习，使用 PPO 算法。每个 episode 随机采样初始人形姿态与目标指令对：初始姿态混合数据集姿态与跌倒姿态（跌倒权重 0.1）并随机施加平面内旋转，以训练跌倒恢复与追赶能力。控制器通过跟踪奖励与风格奖励的联合信号优化策略网络。

### 补充图表

![[assets/figures/papers/paper_list_l1876_MHC_Generating_Physically_Realistic_and_Directable_Human_Motions_from_Mu/figures/004_Figure_4.jpg]]
*Figure 4: Highlights the potential applications of MHC. [Top] The selective masking of the target directive allows MHC to represent various modalities of motion data under a single framework. These multi-modal inputs include MoCap, full or occluded video, joystick, VR controller among others. [Bottom] Similarly selective masking of target directive also allows us to treat the guiding signal itself as abstract actions. This enables straightforward integration with Finite State Machines and Data Driven Planning to allow zero-shot motion generation for higher-level task specifications*

![[assets/figures/papers/paper_list_l1876_MHC_Generating_Physically_Realistic_and_Directable_Human_Motions_from_Mu/figures/005_Figure_5.jpg]]
*Figure 5: Illustrates generated motions corresponding to key CCC capabilities of MHC. The simulation (left) displays key-frames of humanoid following different motion directives (right). From top to bottom the simulated humanoid (A) follows an imitation target, (B) transitions from falling-down position to catch-up to the target directive, (C) imitates motion directive that combines upper-body and lower-body movements from distinct motions (D) completes the motion using only 3D joint positions of the head, hands and feets*

## 实验与分析

### 主结果：CCC 能力统一评估

MHC 在模仿（Imitation）、追赶（Catch-up）和组合（Combine）三项核心任务上全面超越 ASE 基线（Peng et al., ACM TOG 2022），且 MHC 接收的是**不完全（掩码）指令**，而 ASE 接收的是完全指定指令——这构成了对 MHC 更严苛的测试条件。

**Table 1** 的核心数据（Reallusion $M_{Real}$ 数据集）：

- **模仿任务**：MHC 的 MPJPE 从 ASE 的 123.51 mm 降至 **51.05 mm**（降幅 58.7%），成功率从 0.60 提升至 **0.92**。
- **追赶任务**与**组合任务**：MHC 同样显著优于 ASE，表明掩码训练赋予控制器的隐式运动先验使其能在不同步初始姿态或上下半身拼接指令下生成自然运动。

在 ASE rollout 数据集 $M_{ASE}$ 上，MHC 同样保持优势，说明其泛化能力不依赖于特定数据分布。

### 消融实验：各组件的因果作用

Table 1 同时报告了针对性消融结果，每项消融对应一种 CCC 能力的退化：

![[assets/figures/papers/paper_list_l1876_MHC_Generating_Physically_Realistic_and_Directable_Human_Motions_from_Mu/figures/006_Table_1.jpg]]
*Table 1: Results for the ASE baseline, the MHC, and MHC ablations for the imitation, catchup and combine experiments. The ablation differs across expeirments. For imitation we remove the style reward, for catchup we remove random pose initialization, and for combine we remove target motion augmentation (i.e. training on M rather than*

1. **移除风格奖励（Style Reward）**  
   在完全指定指令的模仿任务中，MHC(abl) 的 MPJPE 飙升至 **552.25 mm**，成功率降至 **0.0**。这表明多部位判别器提供的风格奖励是训练稳定性和运动自然度的**必要条件**，缺失时跟踪奖励无法单独引导出合理行为。

2. **移除随机姿态初始化**  
   削弱了追赶（Catch-up）能力。随机初始化迫使策略学习从任意跌倒姿态恢复并追上目标指令，移除后策略对该场景的鲁棒性下降。

3. **移除目标运动增强（不使用 $M^+$）**  
   导致组合（Combine）性能下降。$M^+$ 通过拼接不同运动的上下半身子序列并随机旋转，制造突兀转换，迫使策略学习协调不同来源的身体部位运动。缺少该增强，策略无法处理组合指令。

4. **能量惩罚项的作用**  
   消融分析（Section 4.2）指出，能量代价 $c_t$ 对消除脚部高频抖动至关重要。该惩罚项通过约束动作变化量 $\|a_t^j - a_{t-1}^j\|_1$ 和力矩 $\|\tau_t^j\|_1$ 来抑制仿真中的不自然振荡。

### 掩码鲁棒性分析

**Figure 6** 从两个维度验证了掩码训练的关键作用：

- **通道级掩码（左图）**：经指令掩码训练的 MHC 在不同通道掩码变体下保持稳定的模仿性能；而未使用掩码训练的 MHC 在通道掩码下性能严重退化。
- **关节级掩码（右图）**：MHC 在 0% 至 75% 的关节掩码比例范围内性能稳定，且**始终优于接收完全指定指令的 ASE**；未使用关节级掩码训练的 MHC 则随掩码比例增加性能急剧下降。

> **公平性说明**：ASE 在不同掩码水平下的性能变化源于评估仅在未掩码关节上进行，而 MHC 的优势是在更少信息输入下取得的。

### 方向运动控制与零样本任务规划

**Table 2** 报告了方向运动控制（Heading）和零样本高层任务求解的定量结果。实验考虑两种运动形式（Run 和 Crouch walk），每种具有不同的速度和风格，并设置不同的终点动作（Sword Swing 和 Taunt）。

**Figure 8** 展示了 MHC 与 DAC-MDP 集成后的零样本规划能力：
- FSM A1/A2 实现了“走向目标位置同时执行挥剑动作，到达后倒地恢复”的复杂行为序列。
- DAC-MDP 通过原始/取反奖励函数分别产生“趋向目标”和“避开目标”的行为（B1/B2），通过调整折扣因子控制规划视野（C1 短视挥剑后终止，C2 长视走向目标获取更大长期奖励）。

该集成方案的关键特性是**零样本**——无需针对新高层任务进行微调或额外 RL 训练，仅需将低层指令视为抽象动作嵌入 MDP 框架即可。

### 多模态输入定性结果

**Figure 7** 展示了 MHC 在四类多模态输入下的运动生成关键帧：
- VR 头显与手柄
- 摇杆控制器
- 视频提取的 3D 关节位置
- 文本到运动生成器

这些结果表明，掩码训练使 MHC 能够统一处理来自不同模态的稀疏、含噪、欠指定指令，无需为每种输入模态单独设计控制器。

### 失败模式与局限

论文未报告系统性失败案例，但可从实验设计推断以下边界：
- 移除风格奖励时训练完全崩溃（MPJPE 552.25, 成功率 0.0），说明纯跟踪奖励不足以在物理仿真中产生自然运动。
- 关节掩码超过 75% 时的性能趋势未在 Figure 6 中展示，极端稀疏指令下的行为保真度需进一步验证。
- 学到的生成器在增强数据集 $M^+$ 之外的泛化能力仍是一个开放问题。

![[assets/figures/papers/paper_list_l1876_MHC_Generating_Physically_Realistic_and_Directable_Human_Motions_from_Mu/figures/007_Figure_6.jpg]]
*Figure 6: (Left) Performance across different channel-level masks. We find that the MHC trained with directive masking retains its imitation performance across different variants of channel masks in contrast to the MHC trained without masking. (Right) Performance across different percentages of joint masking (0% to 75%). We see that the MHC shows stable performance as the amount of masking increases compared to the MHC trained without joint-level masking. We also see that the MHC significantly outperforms ASE, even though ASE is provided fully-specified (unmasked) directives. The performance of ASE varies across masking levels because we only evaluate the metric over unmasked joints*

### 补充图表

![[assets/figures/papers/paper_list_l1876_MHC_Generating_Physically_Realistic_and_Directable_Human_Motions_from_Mu/figures/010_Table_2.jpg]]
*Table 2: Quantitative evaluation of directional motion control (Heading) and zero-shot task solution. We consider two forms of locomotion Run and Crouch walk, each characterized by a different speed and style. We consider various finishing motions for the location task: (Sword Swing) and (Taunt)*

![[assets/figures/papers/paper_list_l1876_MHC_Generating_Physically_Realistic_and_Directable_Human_Motions_from_Mu/figures/008_Figure_7.jpg]]
*Figure 7: Illustrates qualitative results using keyframes for motion generation under multi-modal inputs such as (A) VR headset and controllers, (B) joystick controllers, (C) 3D joint positions derived from video and (D) text-to-motion generator. This highlights the versatility of MHC and its applications for motion generation directed by various modalities that may be noisy, under-specified*

![[assets/figures/papers/paper_list_l1876_MHC_Generating_Physically_Realistic_and_Directable_Human_Motions_from_Mu/figures/009_Figure_8.jpg]]
*Figure 8: (A) Key frame visualization of FSMs for Go-To-Location task. FSM A1 (blue) generates a motion of walking towards the goal position while doing right sword slashes and ultimately falling down and recovering on reaching the goal. FSM A2 (green) generates a motion that swings its sword as it crouch-walks towards the goal while facing the other away. and swinging the sword along the way. (B) Visualization of FSM produced by DAC-MDP using original/negated reward functions for Go-To-Location task. FSM B1 (green) uses original reward function and reliably reaches the goal. FSM B2 (blue) uses negated reward function and avoids the goal. (C) Visualization of FSM produced by DAC-MDP for different dis...*

![[assets/figures/papers/paper_list_l1876_MHC_Generating_Physically_Realistic_and_Directable_Human_Motions_from_Mu/figures/001_Figure_1.jpg]]
*Figure 1: Showcases generated human motions from multi-modal inputs: (A) VR device, (B) joystick controller, (C) video, and (D) text. Our proposed method, Masked Humanoid Controller (MHC), can generate physically realistic motions from a wide variety of muli-modal directives*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

MHC 的核心对比基线是 **ASE**（Adversarial Skill Embeddings，Peng et al., ACM TOG 2022）。ASE 代表了物理类人运动控制中“模仿学习+对抗风格奖励”的主流范式，其控制器接收**完全指定的运动指令**（包含完整的根状态、关节旋转、局部和全局位置），并通过单一判别器提供风格信号。

MHC 在以下维度上对 ASE 进行了系统性改造：

| 改造维度 | ASE 基线 | MHC 改进 | 因果机制 |
|----------|----------|----------|----------|
| **指令完整性** | 完全指定（无掩码） | 通道级掩码（随机掩盖根、关节旋转、局部/全局位置等）及关节级掩码（随机掩盖至多75%关节） | 迫使策略隐式学习运动先验，从而在推理时能从稀疏、部分指令中补全运动 |
| **初始姿态分布** | 仅从数据集中采样姿态 | 混合数据集姿态与跌倒姿态（跌倒权重0.1），并随机施加平面内旋转 | 制造“不同步”初始状态，训练控制器从任意姿态追赶（catch-up）目标运动 |
| **目标运动增强** | 单段完整运动序列 | 从增强数据集 M+ 中随机拼接子序列（长度120–240帧），并随机旋转，制造突兀转换 | 暴露策略于上下半身不匹配的组合指令，从而习得组合（combine）能力 |
| **风格奖励** | 无风格奖励或单一判别器 | 5个身体部位（左上、右上、根、下半身、全身）独立判别器，输入10帧运动子序列，使用正则化对抗损失 | 提供更细粒度的自然运动监督；消融实验表明移除风格奖励导致训练彻底失败（MPJPE 552.25，成功率0.0） |
| **跟踪奖励优先级** | 均匀加权奖励 | 分级奖励：根高度 > 根朝向 > 根速度 > 关节欧拉角，仅当前置奖励阈值>0.9时激活后续奖励 | 稳定早期训练，避免策略在未掌握基础平衡时被复杂关节匹配信号干扰 |

**关键公平性说明**：在对比实验中，ASE 接收的是完全指定的指令，而 MHC 接收的是不完全（掩码）指令。即便如此，MHC 在所有任务上均显著优于 ASE（模仿任务 MPJPE：51.05 vs 123.51；成功率：0.92 vs 0.60），这表明掩码训练带来的隐式运动先验学习比完全信息下的模仿学习更为有效。

### 2. 适用边界

MHC 的设计假设和适用边界可从其训练设置和实验覆盖范围中推断：

- **动作库规模**：MHC 在包含 87 种不同技能的 Reallusion 数据集上训练。方法在现有动作库内的泛化能力已得到验证，但学到的生成器在 M+ 增强集之外的泛化能力仍是一个开放问题。
- **物理仿真环境**：MHC 基于标准的人形机器人物理仿真（PD 控制器将关节目标位置转换为力矩），其自然运动风格由多部位判别器在训练数据分布内约束。在显著偏离训练分布的运动风格或极端物理条件下，性能可能退化。
- **多模态输入**：MHC 通过选择性掩码将不同模态（MoCap、视频、VR、手柄、文本生成的运动）统一为同一指令框架。这意味着任何能转换为“部分关节/通道信息”的输入模态理论上都可接入，但输入质量（如视频估计的关节噪声）会影响生成质量。
- **零样本高层规划**：MHC 与有限状态机（FSM）和 DAC-MDP 集成后，可在无额外微调的情况下完成目标导航等高层任务。但这种零样本能力受限于低层控制器能否快速完成高层目标——论文明确指出这仍是一个开放挑战。

### 3. 局限与开放问题

**论文明确指出的开放问题**：

1. **高层目标完成效率**：如何使低层控制器快速完成高层目标仍是一个开放挑战。当前集成方案（FSM/DAC-MDP）依赖于在抽象动作间切换，但每次切换后控制器需要时间“追赶”新指令，可能影响任务完成速度。
2. **泛化能力**：学到的生成器在 M+ 之外的泛化能力如何？当前训练数据增强虽已显著扩展了指令空间，但能否泛化到全新类型的运动组合或完全未见过的动作类别尚未被验证。
3. **控制器与规划器的集成**：如何将低层控制器与数据驱动规划器有效集成以实现零样本泛化？当前 DAC-MDP 集成方案依赖于手工定义的抽象状态和动作空间，扩展到更复杂的任务场景可能需要自动化抽象学习方法。
4. **动作库与交互场景的扩展**：该方法能否扩展到更丰富的动作库和交互场景（如与动态物体或他人的交互）？当前实验限于单人运动控制，物理交互引入了额外的接触约束和力控制挑战。

**从分析中可推断的潜在局限**：

- **能量惩罚的必要性**：消融实验表明能量惩罚项对于消除脚部高频抖动至关重要（confidence 0.9）。这意味着方法对奖励权重的设置较为敏感，在实际部署中可能需要针对不同运动风格调整惩罚系数。
- **掩码比例的鲁棒性边界**：实验显示 MHC 在高达 75% 关节掩码下保持稳定性能，但极端掩码（如仅保留单一关节信息）下的行为未被报告。补全能力的上限受限于训练期间所见的最小信息量。
- **风格判别器的过拟合风险**：多部位判别器在训练数据分布内提供有效的风格监督，但在分布外运动风格上可能产生不可靠的奖励信号，导致生成运动的质量下降或行为异常。

## 原文 PDF

![[paperPDFs/ECCV_2024/MHC_Generating_Physically_Realistic_and_Directable_Human_Motions_from_Multi_Modal_Inputs.pdf]]