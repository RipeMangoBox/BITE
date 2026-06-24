---
title: "PARC: Physics-based Augmentation with Reinforcement Learning for Character Controllers"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/PARC_Physics_based_Augmentation_with_Reinforcement_Learning_for_Character_Controllers.pdf
project_link: https://michaelx.io/parc/index.html
aliases:
- PARC
tags:
- SIGGRAPH_2025
- topic/motion_animation
- topic/motion_animation/character_control_physics
core_operator: "在每次迭代中，利用强化学习训练的物理跟踪控制器模仿生成的运动，并将仿真中记录的物理合理运动反馈到数据集中，切断误差累积。"
primary_logic: "通过生成器和跟踪器在自我增强循环中的协同进化，物理仿真成为数据质量的过滤器，使得模型能力能够持续提升，实现了从小数据集出发逐步掌握复杂地形穿越技能。"
claims:
- "PARC迭代训练生成器和跟踪器，相互增强数据。"
- "跟踪器纠正物理伪影后再加入数据集。"
- "无物理校正的自增强导致运动质量大幅下降（高抖动帧比例达18.68%）。"
- "经过4轮迭代，运动生成器的FWD、TPL、TCL、%HJF等指标持续优化。"
---

# PARC: Physics-based Augmentation with Reinforcement Learning for Character Controllers

> [!tip] 核心洞察
> 通过生成器和跟踪器在自我增强循环中的协同进化，物理仿真成为数据质量的过滤器，使得模型能力能够持续提升，实现了从小数据集出发逐步掌握复杂地形穿越技能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | PARC：基于物理增强的强化学习角色控制器 |
| 英文题名 | PARC: Physics-based Augmentation with Reinforcement Learning for Character Controllers |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](https://arxiv.org/abs/2505.04002); [Project](https://michaelx.io/parc/index.html) |
| Topic | #topic/motion_animation #topic/motion_animation/character_control_physics |
| Method | PARC |
| Dataset | 100 procedurally generated test terrains |

> [!tip] 效果简介
> - 100 procedurally generated test terrains 上，%HJF (percentage of high jerk frames) 为 2.73 (PARC Iteration 4)，对比 18.68 (self-consuming without physics correction)，变化 -85.4%。
> - 100 procedurally generated test terrains 上，Tracker Success Rate 为 68% (Iteration 4)。

## 概述

高质量地形穿越动作捕捉数据稀缺，是小数据集训练运动生成器的根本瓶颈。当训练数据有限时，生成的运动在复杂地形上容易产生物理伪影（如滑步、穿透、抖动）；若直接采用自增强（self-augmentation）循环——即用模型自身生成的运动扩充数据集——则误差会在迭代中累积放大，导致模型退化甚至崩溃。PARC 的核心洞察在于：**物理仿真可以充当数据质量的过滤器**。通过让一个基于强化学习的物理跟踪控制器在仿真中模仿生成的运动，并将仿真中记录的物理合理运动反馈到数据集中，PARC 切断了自增强循环中的误差累积路径，使生成器与跟踪器在协同进化中持续提升能力。

该方法的关键因果机制是**迭代联合训练**：每一轮迭代中，运动生成器（地形条件扩散模型）生成运动序列，运动跟踪器（RL 物理控制器）在仿真中追踪这些运动并记录物理校正后的结果，校正后的运动被加入数据集用于下一轮训练。与使用固定预训练跟踪器进行一次性校正的方法（如 Gillman et al., 2024）不同，PARC 的跟踪器随迭代持续进化，能够适应并纠正生成器产生的新型运动中的物理错误。

实验证据表明，这一设计是决定性的：去除物理校正的自增强循环导致运动质量急剧恶化，高抖动帧比例（%HJF）从 2.73 飙升至 18.68；而经过 4 轮 PARC 迭代，运动生成器在最终路径点距离（FWD）、地形穿透损失（TPL）、地形接触损失（TCL）和 %HJF 等指标上均持续优化，跟踪器的运动完成成功率也提升至 68%。

PARC 的方法定位介于运动生成与物理角色控制之间：它不依赖大规模动捕数据集，也不假设生成的运动天然物理合理，而是通过生成-跟踪-校正的闭环，从小数据集出发逐步掌握复杂地形穿越技能（如跳跃、攀爬、落地等）。其局限性包括生成器推理速度尚不足以支持实时闭环规划，以及训练计算开销较大（单张 A6000 GPU 上约一个月）。

## 背景与动机

### 问题背景：复杂地形穿越的物理角色动画

让虚拟角色在复杂三维地形上做出敏捷、物理真实的穿越动作——例如跳跃、攀爬、翻越——是计算机动画、游戏和机器人领域的长期难题。传统方法依赖大量高质量的动作捕捉数据来训练运动生成模型。然而，**获取覆盖多样化地形和技能组合的高质量动捕数据极其困难且成本高昂**。现实中的动捕数据集往往规模小、地形简单、技能单一，难以泛化到复杂场景。

PARC 的出发点正是这一核心瓶颈：**高质量地形穿越动作捕捉数据稀缺，小数据集训练的运动生成器在复杂地形上产生物理伪影**。当生成器面对训练分布之外的地形时，容易出现脚部滑动、身体穿透地形、关节抖动等物理不合理现象。

### 现有方法的缺口：自增强的陷阱

一种直观的缓解思路是**自增强**——让生成器在未见过的地形上生成运动，再将这些生成的运动加入数据集重新训练，从而逐步扩展数据覆盖范围。然而，这一策略存在严重缺陷：**生成器产生的运动往往包含物理伪影，将这些有缺陷的运动直接反馈到训练集中，会导致误差累积，模型逐渐退化**。

PARC 论文明确指出，若不进行物理校正，自增强循环会使运动质量急剧恶化。实验数据显示，无物理校正的自增强方法生成的运动中，高抖动帧比例（%HJF）高达 **18.68%**，而 PARC 的迭代校正方法可将该指标降至 **2.73%**（Table 1, Fig 9）。

此前有工作尝试用**固定的预训练物理跟踪器**对生成运动进行一次性校正（如 Gillman et al., 2024 的自消耗扩散模型方法），但固定跟踪器的能力受限于初始数据集，无法随生成器能力的提升而同步进化，因而校正效果有限。

### 核心动机：生成器与跟踪器的协同进化

PARC 的核心洞察在于：**物理仿真可以成为数据质量的过滤器**。与其让生成器独自在自增强循环中退化，不如引入一个基于强化学习的物理跟踪控制器，在每次迭代中模仿生成的运动，并将仿真中记录的物理合理运动反馈到数据集中。这一设计切断了误差累积链条——跟踪器在物理仿真中强制执行接触约束和动力学方程，天然地纠正了运动学伪影。

更重要的是，PARC 让生成器和跟踪器在迭代循环中**协同进化**：随着数据集不断扩展，生成器能产生更多样的运动，这些运动反过来训练出更强大的跟踪器，而更强大的跟踪器又能校正更复杂的运动，形成正向飞轮效应。这使得模型能够从仅 **14 分钟** 的初始动捕数据出发，逐步掌握跨越沟壑、攀爬高墙、组合跳跃与抓取等复杂地形穿越技能，最终生成长达数十秒的物理合理运动序列（Fig 4, Fig 7）。

## 核心创新

PARC 的核心创新在于构建了一个**生成器与跟踪器协同进化的自增强闭环**，从根本上解决了小规模动捕数据集在复杂地形穿越任务中面临的物理伪影与误差累积问题。

### 问题瓶颈：自增强的退化陷阱

高质量地形穿越动作捕捉数据获取成本极高，直接导致初始训练集规模受限（PARC 仅使用约 14 分钟的动捕数据）。在小数据集上训练的运动生成器在复杂地形上产生大量物理伪影，如足部滑动、地形穿透和关节抖动。更关键的是，若将这些生成的运动直接反馈到数据集中进行自增强训练，模型会不断放大自身误差，形成**模型退化的恶性循环**。实验表明，无物理校正的自增强方案导致高抖动帧比例（%HJF）飙升至 18.68%，运动质量急剧恶化。

### 关键调控变量：物理仿真作为质量过滤器

PARC 的核心调控变量在于**自增强循环中的物理校正方式**。与两类 baseline 方案形成鲜明对比：

| 方案 | 物理校正方式 | 效果 |
|------|-------------|------|
| 无校正自增强 | 生成动作直接加入数据集 | 误差累积，模型崩溃（%HJF=18.68） |
| 固定跟踪器校正（Gillman et al., 2024） | 使用预训练跟踪器一次性校正 | 跟踪器能力固定，无法适应生成器进化 |
| **PARC** | 每轮迭代联合训练生成器与跟踪器，跟踪器在仿真中模仿并记录物理合理运动后反馈到数据集 | 跟踪器能力同步提升，持续提供高质量校正 |

PARC 在每轮迭代中，利用强化学习训练的物理跟踪控制器在仿真环境中模仿生成的运动，并将仿真中记录的**物理校正后运动**（而非原始生成运动）加入数据集。物理仿真在此充当了严格的质量过滤器——任何违反物理定律的伪影在跟踪过程中被自然纠正，只有物理合理的运动才能通过仿真验证并进入数据集。这一机制切断了误差累积链条，使自增强循环从"退化螺旋"转变为"进化飞轮"。

### 核心洞察：协同进化实现能力跃迁

PARC 的根本洞察在于：**生成器与跟踪器的能力上限相互制约，单独提升任一方都会遭遇瓶颈，唯有让二者在迭代中协同进化，才能实现整体能力的持续跃迁**。

具体而言，生成器为跟踪器提供日益多样化的训练数据，推动跟踪器掌握更复杂的物理技能；而能力提升后的跟踪器能够成功追踪更具挑战性的运动，从而为生成器提供更高质量的训练样本。经过 4 轮迭代，运动生成器在最终航点距离（FWD）、地形穿透损失（TPL）、地形接触损失（TCL）和 %HJF 等指标上持续优化，%HJF 从无校正方案的 18.68% 降至 2.73%，降幅达 85.4%，同时跟踪器成功率提升至 68%。这一结果表明，PARC 成功实现了从小数据集出发逐步掌握复杂地形穿越技能的突破。

## 整体框架

PARC 的核心思想是将运动生成与物理仿真嵌入一个**自我增强循环**（self-augmentation loop）中，使生成器与跟踪器协同进化。框架的输入是一个小规模的地形穿越运动捕捉数据集，输出是能够生成物理合理、长时域复杂地形穿越运动的生成器和控制器。

### 迭代增强循环

PARC 的迭代流程（图 2）由四个阶段构成一个闭环：

1. **地形生成与路径规划**：程序化生成训练地形（如 Random Boxes 方法，图 11），并在其上规划导航路径，确定角色需要穿越的起点、终点及途经点。
2. **运动生成**：地形条件扩散模型根据局部高度图和目标方向，沿规划路径生成运动序列。
3. **物理跟踪与校正**：强化学习训练的物理跟踪控制器在仿真中模仿生成的运动，记录物理合理的运动数据。这一步是**切断误差累积的关键**——跟踪器在仿真中自然纠正了生成运动的物理伪影（如滑步、穿透、抖动）。
4. **数据集扩充**：将物理校正后的运动片段加入数据集，用于下一轮训练。

此循环的核心因果机制在于：**物理仿真充当了数据质量的过滤器**。若直接将生成的运动加入数据集（无物理校正的自增强），模型会因误差累积而退化——实验表明，这种情况下高抖动帧比例（%HJF）高达 18.68%，而经过物理校正后降至 2.73%（表 1，图 9）。

### 模块关系与数据流

PARC 包含以下核心模块，其间的数据流关系如下：

| 模块 | 角色 | 输入 | 输出 |
|------|------|------|------|
| **运动生成器**（地形条件扩散模型） | 根据地形与方向生成运动序列 | 局部高度图 `h`、目标方向 `d`、起始帧 `x₀¹` 和 `x₀²` | 运动序列 `x̂₀` |
| **运动跟踪器**（RL 跟踪控制器） | 在物理仿真中追踪参考运动 | 参考运动序列、角色物理状态 | 物理仿真轨迹、物理校正运动 |
| **运动学运动校正** | 启发式选择与优化，减少生成运动的伪影 | 扩散模型生成的原始运动 | 筛选并校正后的运动序列 |
| **地形生成与路径规划** | 生成训练地形并规划路径 | 地形参数 | 高度图、导航路径 |
| **迭代增强循环** | 协调上述模块的循环流程 | 初始数据集 | 扩充后的数据集、训练好的模型 |

生成器的架构采用 Transformer Encoder（图 3），类似于 MDM（Tevet et al., 2023）。高度图 `h` 先经 CNN 处理为 64×16×16 的特征图，再展开为 64 个 64×2×2 的非重叠图像块，嵌入后与运动帧 token 一同输入 Transformer。训练时使用混合损失函数：

$$\mathcal{L}(G) = \mathcal{L}_{\mathrm{rec}}(G) + \mathcal{L}_{\mathrm{velocity}}(G) + \mathcal{L}_{\mathrm{joint}}(G) + \mathcal{L}_{\mathrm{pen}}(G)$$

其中 $\mathcal{L}_{\mathrm{rec}}$ 为扩散重建损失（Eq 1），$\mathcal{L}_{\mathrm{pen}}$ 为地形穿透损失（Eq 7），惩罚角色身体点穿透地形的程度。

跟踪器的策略网络为三层全连接网络（2048→1024→512），训练目标为最大化期望折扣回报 $J(\pi)$（Eq 2）。跟踪奖励（Eq 22）综合考虑了姿态、根位置、根速度、关节速度、关键点位置和接触标签的匹配程度。

### 与基线方法的差异

PARC 与现有方法的关键差异在于自增强循环中的物理校正方式：

- **无校正的自增强**：生成动作直接加入数据集，误差累积导致模型崩溃。
- **固定跟踪器校正**（如 Gillman et al., 2024）：使用预训练的固定跟踪器进行一次性物理校正，但跟踪器能力不随数据集增长而提升，限制了校正质量。
- **PARC 的迭代校正**：每轮迭代联合训练生成器和跟踪器，跟踪器在仿真中模仿并记录动作，将物理校正后的动作加入数据集。跟踪器能力随数据集扩展而同步提升，形成正向反馈。

### 生成流程

完整的运动学运动生成流程（图 19）展示了从地形到最终运动序列的端到端管线：地形生成模块产生高度图 → 路径规划模块计算导航路径 → 训练好的扩散模型沿路径生成运动序列 → 运动学校正模块筛选并优化输出。跟踪控制器的训练流程（图 20）则展示了如何利用 RL 在物理仿真中训练跟踪策略，并记录物理合理的运动数据。

### 补充图表

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2505_04002/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the PARC framework. PARC iteratively trains a motion generator and motion tracker with self-generated motion data. The motion generator produces kinematic motion sequences to train the motion tracker, while the motion tracker corrects physics-related artifacts in a simulator, enabling the motion generator to continue training on new physics-based motions*

## 核心模块与公式推导

### 运动生成器：地形条件扩散模型

PARC的运动生成器是一个以局部地形高度图 $\mathbf{h}$ 和目标方向 $\mathbf{d}$ 为条件的扩散模型。该模型采用与MDM（Tevet et al., 2023）类似的Transformer编码器架构：地形高度图首先经CNN处理为 $64 \times 16 \times 16$ 的特征图，再展开为64个不重叠的图像块，经嵌入后与噪声运动帧的嵌入一同输入Transformer编码器（Figure 3）。

扩散模型的核心训练目标是预测去噪后的干净运动样本 $\hat{\mathbf{x}}_0$，其重建损失为：

$$\mathcal{L}_{\mathrm{rec}}(G):=\mathbb{E}_{\mathbf{x}_0,C\sim D}\mathbb{E}_{k\sim p(k)}\mathbb{E}_{\mathbf{x}_k\sim q(\mathbf{x}_k\mid\mathbf{x}_0)}\left[\mid\mid\mathbf{x}_0-G(\mathbf{x}_k,k,C)\mid\mid^2\right]$$

其中 $\mathbf{x}_0$ 为原始干净运动序列，$C$ 为条件上下文，$k$ 为扩散时间步，$\mathbf{x}_k$ 为加噪后的运动序列。生成器的完整训练损失还包含速度一致性损失 $\mathcal{L}_{\mathrm{velocity}}$、关节一致性损失 $\mathcal{L}_{\mathrm{joint}}$ 和地形穿透损失 $\mathcal{L}_{\mathrm{pen}}$：

$$\mathcal{L}(G) = \mathcal{L}_{\mathrm{rec}}(G) + \mathcal{L}_{\mathrm{velocity}}(G) + \mathcal{L}_{\mathrm{joint}}(G) + \mathcal{L}_{\mathrm{pen}}(G)$$

其中地形穿透损失专门用于惩罚角色身体点穿透地形的程度：

$$\mathcal{L}_{\mathrm{pen}} = \sum_{i=1}^{N_{\mathrm{points}}} -\min(\mathrm{sdTerrain}(\mathbf{p}_i), 0)$$

$\mathrm{sdTerrain}(\mathbf{p}_i)$ 为点 $\mathbf{p}_i$ 到地形表面的有符号距离，$N_{\mathrm{points}}$ 为采样的身体点数。该损失仅在点穿透地形时（负距离）产生惩罚。

### 混合去噪策略

为在生成运动的**地形遵守性**与**时间平滑性**之间取得平衡，PARC采用混合去噪策略。在推理时，将无条件去噪输出与条件去噪输出进行线性混合：

$$G_{\mathrm{blend}}(k,\mathbf{x}_k,C=(\mathbf{h},\mathbf{d},\mathbf{x}_0^1,\mathbf{x}_0^2)) = s G(k,\mathbf{x}_k,C=(\mathbf{h},\mathbf{d})) + (1-s) G(k,\mathbf{x}_k,C=(\mathbf{h},\mathbf{d},\mathbf{x}_0^1,\mathbf{x}_0^2))$$

其中 $s$ 为混合系数，$\mathbf{x}_0^1$ 和 $\mathbf{x}_0^2$ 为运动序列的前两帧，用于约束生成序列的初始状态。消融实验表明 $s=0.65$ 时取得最优平衡（Table 3）。

### 运动跟踪器：强化学习物理控制器

运动跟踪器以强化学习训练，目标是在物理仿真中精确追踪参考运动。其优化目标为最大化期望折扣回报：

$$J(\pi)=\mathbb{E}_{p(\tau\mid\pi)}\left[\sum_{t=0}^{T-1}\gamma^t r_t\right]$$

策略网络结构为三层全连接网络（2048→1024→512单元）。跟踪奖励函数设计为加权组合，最小化仿真角色与参考运动在以下维度的差异：

$$r_t = 0.5 r_t^{\mathrm{pose}} + 0.1 r_t^{\mathrm{pose\ velocity}} + 0.15 r_t^{\mathrm{root}} + 0.1 r_t^{\mathrm{root\ velocity}} + 0.15 r_t^{\mathrm{key}} + r_t^{\mathrm{contact}}$$

各分量分别对应姿态、姿态速度、根位置、根速度、关键身体点位置和接触标签的跟踪误差。该框架继承了**DeepMimic**（Peng et al., SIGGRAPH 2018）的模仿奖励设计范式。

### 迭代自增强循环

PARC的核心机制在于生成器与跟踪器的协同进化：每轮迭代中，运动生成器产生运动序列，跟踪器在物理仿真中模仿这些运动并记录物理校正后的版本，校正后的运动被加入数据集用于下一轮训练。这一循环切断了单纯自增强（self-consuming）中误差累积导致模型退化的因果链——消融实验表明，去除物理校正后，高抖动帧比例（%HJF）从2.73飙升至18.68，模型实质上发生崩溃（Table 1, Figure 9）。

## 实验与分析

PARC 的核心实验围绕一个核心主张展开：**生成器与跟踪器的协同迭代训练能够持续提升运动质量，而缺少物理校正的自增强循环会导致模型退化。** 实验在 100 个程序化生成的测试地形上进行，评估指标覆盖运动学质量与物理合理性两个维度。

### 主实验结果

**迭代训练带来持续的性能增益。** Table 1 和 Figure 9 展示了运动生成器在四轮迭代中的定量指标变化。关键指标 %HJF（高抖动帧比例）从初始模型的 3.22 持续下降至第 4 轮的 2.73，表明运动的时间平滑性随迭代逐步改善。同时，FWD（终点距离）和 TCL（地形接触损失）等指标也呈现一致的优化趋势，验证了生成器在每一轮迭代中确实从物理校正后的增强数据中获益。

**物理校正机制是防止模型崩溃的关键。** 消融实验直接将 PARC 与无物理校正的自增强基线对比。当生成的运动不经跟踪器校正直接回灌数据集时，模型迅速退化：%HJF 飙升至 18.68（Table 1，Figure 9），TPL 和 TCL 同步恶化。这一结果直接支撑了论文的核心瓶颈判断——自增强循环中的误差累积会导致灾难性遗忘，而物理仿真作为数据质量过滤器是切断这一反馈回路的核心机制。

**跟踪器能力随生成器同步提升。** Table 2 报告了运动跟踪器在不同迭代轮次的表现。跟踪成功率从初始轮次的较低水平提升至第 4 轮的 68%，关节跟踪误差也呈下降趋势。这表明生成器产出的运动越合理，跟踪器越容易在物理仿真中成功模仿，进而产生更高质量的训练数据反馈给生成器，形成正向飞轮。

### 消融实验

**混合系数 λ 在地形遵守与时间平滑性之间取得平衡。** Table 3 展示了第 4 轮生成器在不同混合系数下的性能。λ=0.65 时达到最优平衡，FWD=0.596，%HJF=2.730。过高的 λ 值过度强调地形条件，导致运动抖动加剧；过低的 λ 值则削弱地形遵守能力，角色可能偏离目标路径或穿透地形。这一消融验证了公式 5 中混合去噪更新策略的必要性。

**优先状态初始化提升了困难运动的采样效率。** 在跟踪器训练中，采用优先状态初始化（prioritized state initialization）策略显著改善了对高难度运动片段的覆盖。该策略根据跟踪误差分布有偏向地采样初始状态，使训练集中于跟踪器表现较差的运动阶段，从而加速收敛并提升整体成功率。

### 定性分析

Figure 4 展示了最终模型生成的长程物理角色动画，角色在复杂地形上连续执行跑酷动作，运动流畅且与地形交互合理。Figure 8 对比了不同迭代轮次在同一测试地形上的生成结果，直观展示了运动质量从初始轮次到第 4 轮的逐步改善。Figure 7 进一步展示了框架涌现的新行为——这些行为在原始动捕数据集中并不存在，是生成器与跟踪器协同进化过程中自发习得的。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2505_04002/figures/009_Figure_8.jpg]]
*Figure 8: Motions generated on a test terrain for different iterations of PARC. Each motion was generated using a batch of 32 for up to 15 seconds of motion time and then automatically selected based on a heuristic incorporating terrain penetration, contact loss, and incompletion penalty. (Left) The iteration 1 motion generator is only trained on the initial dataset, and struggles to navigate across complex terrain. The character was only able to get off the cliff within 15 seconds. (Middle) The motion produced by a motion generator trained on uncorrected generated data from the iteration 1 motion generator. It exhibits physically implausible artifacts such as changing directions while flying through...*

### 失败模式与局限性

尽管 PARC 在迭代训练中持续改进，论文明确指出以下局限：

- **实时性不足**：运动生成器当前推理速度无法支持实时闭环规划，限制了在视频游戏和机器人领域的直接部署。
- **场景泛化受限**：框架依赖程序化生成或手动设计的地形，扩展到照片级真实的复杂三维场景仍需进一步研究。
- **运动自然度仍有差距**：生成的行为偶尔存在不自然之处，缺乏人类运动的精细度。
- **计算成本高昂**：完整训练流程在单张 A6000 GPU 上约需一个月，迭代成本较高，限制了更大规模实验的可行性。

这些失败模式为后续研究指明了方向：加速生成器推理、拓展场景复杂度、引入更精细的运动风格约束，以及降低对初始动捕数据的依赖。

### 补充图表

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2505_04002/figures/012_Figure_9.jpg]]
*Figure 9: Plots showing the measured quantitative results of generated motions from the kinematic motion generator across different PARC iterations, including an iteration with no physics-based motion correction (labeled "NC"). Each metric reports the mean calculated over 3200 motions that were generated across 100 different test terrains for each motion generator. Without physics-based correction, the models generate motions that are much less physically realistic*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2505_04002/figures/008_Table_1.jpg]]
*Table 1: Quantitative results of our motion generators across PARC iterations with the best values bolded. These metrics measure various aspects of motion quality, and include FWD (final waypoint distance), TPL (terrain penetration loss), TCL (terrain contact loss), and %HJF (percentage of high jerk frames). The motion generators from each iteration are used to generate 32 motions for each of the 100 test terrains. The average value across all 3200 generated test motions is reported for each metric*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2505_04002/figures/010_Table_2.jpg]]
*Table 2: Quantitative results of our motion tracker for different PARC iterations. The success rate is the tracker’s average rate of motion completion over 100 generated test motions. The joint tracking error is computed using an average of 2048 episodes for each of the 100 generated test motions at random initial timesteps*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2505_04002/figures/011_Table_3.jpg]]
*Table 3: Quantitative results of our 4th iteration motion generator using different blending coefficients ??. These metrics measure various aspects of motion quality, and include FWD (final waypoint distance), TPL (terrain penetration loss), TCL (terrain contact loss), and %HJF (percentage of high jerk frames). The motions with the best quality have a balance between terrain compliance (low FWD, TPL, TCL) and temporal continuity (low %HJF). We used ?? = 0.65 for automatically augmenting the dataset through PARC, and ?? = 0.5 for generating long horizon motions on complex terrain using the final motion generator*

## 方法谱系与知识库定位

### 核心问题与瓶颈

PARC 直面的核心瓶颈在于：**高质量地形穿越动作捕捉数据极度稀缺**。现有动捕数据集通常仅包含简单地形上的单一技能演示（如跳跃、上楼梯、攀墙），缺乏在复杂地形上组合多种技能的长序列运动。当运动生成器仅基于此类小数据集训练时，在复杂地形上生成的运动会表现出严重的物理伪影，如脚部滑动、地形穿透、关节抖动等。更关键的是，若采用朴素的自增强（self-augmentation）循环——即将生成器产生的运动直接反馈到训练集中——误差会随迭代逐步放大，最终导致模型退化。PARC 的消融实验直接验证了这一点：去除物理校正的自增强方案使高抖动帧比例（%HJF）飙升至 18.68%，而 PARC 迭代 4 次后仅为 2.73%（Table 1, Fig 9）。

### 方法谱系与关键差异

PARC 建立在两条成熟技术路线之上，并通过独特的协同训练机制实现突破：

**运动生成器**采用基于扩散模型（diffusion model）的运动生成范式，具体实现为类似 **MDM**（Tevet et al., 2023）的 Transformer Encoder 架构，以地形高度图和目标方向为条件生成运动序列。训练目标在标准扩散重建损失基础上，额外引入速度一致性损失、关节一致性损失和地形穿透损失 $\mathcal{L}_{\mathrm{pen}}$（Eq 7），以在运动学层面抑制物理伪影。

**运动跟踪器**继承自 **DeepMimic**（Peng et al., SIGGRAPH 2018）的模仿学习框架，通过强化学习训练物理仿真角色跟踪参考运动。其跟踪奖励函数（Eq 22）综合了姿态、速度、根节点位置、关键点位置和接触标签的多项差异。

PARC 与现有工作的关键差异在于**自增强循环中的物理校正方式**：

| 方法 | 物理校正策略 | 局限性 |
|------|-------------|--------|
| 朴素自增强 | 无校正，生成运动直接加入数据集 | 误差累积，模型崩溃（%HJF 18.68） |
| Self-consuming diffusion model（Gillman et al., 2024） | 使用固定预训练跟踪器进行一次性校正 | 跟踪器能力固定，无法适应生成器能力提升后产生的新运动分布 |
| **PARC** | 每轮迭代联合训练生成器和跟踪器，由跟踪器在仿真中模仿并记录动作，将物理校正后的动作加入数据集 | 生成器与跟踪器协同进化，持续提升数据质量和模型能力 |

PARC 的核心洞察在于：**物理仿真成为数据质量的过滤器**。跟踪器不仅是校正工具，更是数据质量的“守门人”——只有物理上可跟踪的运动才能通过仿真验证并进入数据集，从而切断了误差累积的恶性循环。

### 适用边界与局限

PARC 在以下边界内展现出显著的迭代提升能力，但其局限性同样明确：

**适用条件：**
- 需要初始小规模动捕数据集作为种子（论文使用约 14 分钟的动捕数据，经空间增强扩展为 50 倍变体）
- 依赖程序化生成或手动设计的地形进行训练和测试
- 角色模型固定（论文使用统一的人形骨骼结构）

**已知局限（论文明确指出的）：**
1. **实时性不足**：运动生成器目前推理速度无法支持实时闭环规划，限制了在视频游戏和机器人领域的直接部署。
2. **场景泛化受限**：当前框架依赖程序化地形（如 Random Boxes 方法，Fig 11），扩展到照片级真实的复杂三维场景（如城市环境）仍待研究。
3. **运动自然度**：生成的行为偶尔仍存在不自然之处，缺乏人类运动的精细度和风格多样性。
4. **计算成本高昂**：完整训练流程在单张 A6000 GPU 上约需一个月，迭代训练的计算开销较大。

### 开放问题

PARC 为物理合理运动生成开辟了新路径，同时引出了若干待解决的研究问题：

1. **实时推理**：如何加速运动生成器的推理速度，使其满足游戏和机器人领域的实时控制需求？
2. **场景扩展**：如何将框架应用于具有丰富几何细节的真实场景，例如照片级扫描的城市环境或自然地形？
3. **运动质量提升**：能否引入更高级的运动先验、风格约束或对抗性奖励，以进一步提高生成运动的自然度和表现力？
4. **减少数据依赖**：是否可能减少对初始动捕数据的依赖，甚至通过纯强化学习从零开始发现运动技能，仅在后期引入少量演示进行精调？
5. **多角色与交互**：当前框架仅处理单个角色，扩展到多角色交互场景（如协作、对抗）需要解决运动协调和物理交互的耦合问题。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/PARC_Physics_based_Augmentation_with_Reinforcement_Learning_for_Character_Controllers.pdf]]
