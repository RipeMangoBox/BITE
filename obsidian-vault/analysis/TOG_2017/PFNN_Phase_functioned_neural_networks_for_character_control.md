---
title: "Phase-functioned neural networks for character control"
type: paper
paper_level: A
venue: TOG
year: 2017
pdf_ref: paperPDFs/TOG_2017/Phase_functioned_neural_networks_for_character_control.pdf
project_link: https://github.com/sebastianstarke/AI4Animation/tree/master/AI4Animation/SIGGRAPH_2017
aliases:
- PFNN
- PFNNP
- PFNNCC
tags:
- TOG_2017
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "相位（phase）——将网络权重设计为相位的函数，使权值随相位周期性平滑演化，从而避免不同相位数据的混合，消除漂移并大幅度提升相位对输出的影响。"
primary_logic: "采用周期性相位函数（如三次Catmull-Rom样条）动态生成回归网络的权重，而非将相位作为普通输入。这一设计使相位能够全局、强有力地控制输出，同时保持网络结构简单，在复杂地形交互中实现高质量实时角色控制。"
claims:
- "标准神经网络不提供相位输入时，由于混合不同相位的姿态导致角色漂浮，运动质量差。"
- "将相位作为额外输入的标准神经网络，由于dropout等原因相位影响力被忽略，动作僵硬不自然。"
- "PFNN只混合相同相位的样本，从根本上避免了不同相位混合导致的运动退化。"
- "在PFNN中，相位改变所有网络权重，输出相对于相位的变化幅度约是标准NN的50倍，保证了相位的强约束。"
---

# Phase-functioned neural networks for character control

> [!tip] 核心洞察
> 采用周期性相位函数（如三次Catmull-Rom样条）动态生成回归网络的权重，而非将相位作为普通输入。这一设计使相位能够全局、强有力地控制输出，同时保持网络结构简单，在复杂地形交互中实现高质量实时角色控制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于相位函数神经网络的角色控制 |
| 英文题名 | Phase-functioned neural networks for character control |
| 会议/期刊 | TOG 2017 |
| Links | [paper](https://doi.org/10.1145/3072959.3073663); [GitHub](https://github.com/sebastianstarke/AI4Animation/tree/master/AI4Animation/SIGGRAPH_2017) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | Phase-Functioned Neural Network (PFNN) |
| Dataset | Locomotion Dataset (1h mocap + terrain fitting), Character Responsiveness (trajectory following) |

> [!tip] 效果简介
> - Locomotion Dataset (1h mocap + terrain fitting) 上，Runtime / Memory 为 0.0008s (PFNN constant), 125MB，对比 0.0004s (NN w/o phase, 9MB) ; 0.0007s (ERD, 9MB) ; ∼0.1s (GP, >1GB)，变化 PFNN constant 比标准 NN 慢约2倍但质量显著更高；比 GP 快两个数量级。内存消耗约125MB，在可接受范围。。
> - Character Responsiveness (trajectory following) 上，Average Trajectory Error (cm) 为 5.82 cm (Circle, τ_v=5.0, τ_d=10.0)，对比 17.29 cm (Wave, τ_v=0.5, τ_d=2.0)，变化 通过调节未来轨迹混合偏置，响应性显著提升，平均误差降低约3倍，代价极小的动画质量损失。。

## 概述

在实时角色动画中，如何根据用户输入和环境几何自动生成自然、富有表现力的运动，是一个长期存在的挑战。传统自回归模型（如基于LSTM的**ERD**（Fragkiadaki et al., ICCV 2015）和**条件受限玻尔兹曼机**（Taylor and Hinton, ICML 2009））在长时间运动生成中因误差累积导致动作逐渐漂移甚至崩溃；而卷积模型（如**Holden et al., ACM Trans. Graph. 2016**）需要完整控制信号作为输入，不适用于在线实时应用。一个直观的改进方向是将运动周期的时间信息——**相位**（phase）——作为额外输入提供给神经网络，但实验表明，由于dropout等因素，相位的影响力容易被网络稀释，导致动作僵硬、不自然。

本文的核心洞察在于：**将网络权重本身设计为相位的函数，而非将相位作为普通输入。** 具体而言，Phase-Functioned Neural Network（PFNN）采用周期性相位函数（三次Catmull-Rom样条）在每一帧动态生成回归网络的全部权重与偏置，使相位成为全局控制变量。这一设计从根本上避免了不同相位姿态的混合，消除了动作漂浮现象，并使输出相对于相位的变化幅度达到标准神经网络的约50倍，确保了相位对运动生成的强约束。

在方法定位上，PFNN处于数据驱动角色控制与周期性归纳偏置的交汇点。它既不同于依赖手工规则的运动匹配（如**Motion Matching**（Clavet, GDC 2016）），也不同于计算和内存开销随数据规模平方/立方增长的高斯过程自回归器（**Wang et al., IEEE PAMI 2008**）。PFNN以端到端方式在大规模运动捕捉数据集（约1小时数据，经地形拟合扩充至约400万帧）上训练，推理时仅需约0.8毫秒，内存占用约125 MB，在实时性与运动质量之间取得了实用平衡。

实验结果表明，PFNN在崎岖地形穿越、跳跃、蹲伏等复杂场景中能够自动生成适当且富有表现力的运动，并通过调节未来轨迹混合偏置实现响应性与平滑性的灵活权衡——在圆形路径跟随任务中，平均轨迹误差可降至5.82 cm。消融实验进一步证实，移除相位或将其降级为普通输入均会导致运动质量显著退化，验证了相位函数化设计的决定性作用。

## 背景与动机

实时角色动画是游戏与交互式虚拟环境的核心技术挑战。高质量的角色运动要求系统能同时响应三方面的约束：用户的实时操控指令、角色自身的物理状态、以及复杂的三维场景几何。传统方法在这三个维度的交汇点上始终存在难以调和的矛盾。

数据驱动的运动合成方法长期依赖两类范式。一类是基于运动匹配的启发式拼接方法，如 **Motion Matching**（Clavet, GDC 2016），其参数化思路与本工作相似，但本质上不具备学习泛化能力，无法在未见过的地形配置上自动生成合理运动。另一类是基于自回归模型的生成方法，包括 **cRBM**（Taylor and Hinton, ICML 2009）、**GP Autoregressor**（Wang et al., IEEE PAMI 2008）以及基于 LSTM 的 **ERD**（Fragkiadaki et al., ICCV 2015）。这些自回归模型面临一个共同的瓶颈：**在长时间运动生成中，误差逐步累积导致动作逐渐消失或爆炸**，产生严重的运动漂移。此外，基于高斯过程的自回归器其内存与计算量随数据量平方或立方增长，无法扩展到大规模运动数据集。

卷积模型如 **CNN**（Holden et al., ACM Trans. Graph. 2016）虽然避免了自回归的误差累积问题，但其要求完整的控制信号作为输入，无法满足在线实时生成的场景需求——在交互式应用中，未来的控制信号并不可知。

一个关键但长期被低估的因素是**运动相位**（phase）——即角色在周期性运动（如行走、跑步）中所处的时间位置。不同相位的姿态在运动学上差异巨大：支撑相与摆动相的关节配置、重心高度、足部接触状态截然不同。如果模型不加区分地混合来自不同相位的训练样本，会导致姿态平均化，使角色出现“漂浮”或“滑步”等不自然现象。然而，将相位作为普通输入变量直接送入标准神经网络同样效果不佳：由于 dropout 等正则化机制的存在，网络可能忽略相位信息而依赖其他变量推断姿态，导致动作僵硬不自然。

上述困境揭示了一个更深层的设计缺陷：**相位的影响力在标准神经网络架构中被结构性稀释**。当相位仅作为输入向量中的一个维度时，它只能通过第一层权重间接影响网络行为，其控制力受限于该层权重的范数。在复杂地形交互中，这种弱约束不足以确保网络在正确的相位区间生成正确的姿态。

本文的核心动机正是突破这一结构局限：**能否让相位成为网络的全局控制变量，使其能够强有力地、周期性地调节整个网络的权重**，从而从根本上避免不同相位数据的混合，消除运动漂移，同时保持模型结构的简洁与实时推理的高效？这一思路引出了 Phase-Functioned Neural Network（PFNN）的核心设计——将网络权重定义为相位的函数，而非将相位作为输入。

## 核心创新

### 问题瓶颈：相位混合导致的运动退化

在基于学习的角色控制中，运动数据天然具有周期性结构——行走、跑步、跳跃等动作均包含明确的相位信息（如脚掌触地、离地）。然而，传统方法在利用此类数据时面临一个根本性瓶颈：**不同相位的运动姿态被模型混合，导致生成的动作出现漂浮、僵硬甚至逐渐退化**。

具体而言，标准神经网络若不提供相位输入，会将不同相位的姿态进行平均化处理，使角色呈现“漂浮”状态（Fig. 10a），运动质量严重下降。即便将相位作为额外输入变量显式提供给网络，由于训练中 dropout 等正则化机制的作用，相位的影响力容易被稀释甚至忽略，网络转而依赖其他变量推断姿态，导致动作僵硬不自然（Fig. 11, Section 7）。自回归模型（如基于 LSTM 的编码器-循环-解码器网络 **ERD** (Fragkiadaki et al., ICCV 2015) 和条件受限玻尔兹曼机 **cRBM** (Taylor and Hinton, ICML 2009)）即使额外接收相位输入，仍因误差累积而无法有效学习隐藏的相位变量，动作随时间逐步漂移（Fig. 10c,d）。离线卷积模型 **CNN** (Holden et al., ACM Trans. Graph. 2016) 虽能避免自回归漂移，但需要完整控制信号作为输入，不适用于在线实时生成。基于高斯过程的自回归器 **GP** (Wang et al., IEEE PAMI 2008) 则面临内存和计算量随数据量平方/立方增长的扩展性问题。

### 因果杠杆：相位作为网络权重的全局控制变量

PFNN 的核心创新在于**改变了相位在模型中的作用方式**——从“作为输入向量的一个分量”转变为“直接参数化整个网络的权重矩阵和偏置”。这一设计使相位成为全局控制变量，从根本上避免了不同相位数据的混合。

具体而言，PFNN 由两部分组成（Fig. 2）：
- **回归网络 Φ**：一个三层全连接网络，负责从控制输入映射到角色姿态输出，使用 ELU 激活函数；
- **相位函数 Θ**：一个周期性函数，根据当前相位值 $p$ 动态生成回归网络的所有权重和偏置。

在每一帧，系统首先根据当前相位通过相位函数计算网络权重，然后将用户控制、上一帧角色状态和环境几何输入回归网络，生成当前帧姿态。由于网络权重随相位周期性平滑演化，**只有相同相位的样本才会被混合**，从而消除了不同相位数据混合带来的运动退化。

### 关键设计：Catmull-Rom 样条相位函数

相位函数的具体实现采用**三次 Catmull-Rom 样条**，仅使用四个控制点即可表达角色控制所需的回归能力。对于相位 $p \in [0, 2\pi)$，样条通过四个控制点 $\alpha_{k_0}, \alpha_{k_1}, \alpha_{k_2}, \alpha_{k_3}$ 插值生成网络参数：

$$\Theta(p; \beta) = \alpha_{k_1} + w\left(\frac{1}{2}\alpha_{k_2} - \frac{1}{2}\alpha_{k_0}\right) + w^2(\alpha_{k_0} - \frac{5}{2}\alpha_{k_1} + 2\alpha_{k_2} - \frac{1}{2}\alpha_{k_3}) + w^3(\frac{3}{2}\alpha_{k_1} - \frac{3}{2}\alpha_{k_2} + \frac{1}{2}\alpha_{k_3} - \frac{1}{2}\alpha_{k_0})$$

其中 $w$ 为相位在控制点间的插值权重，$\beta$ 为所有控制点的集合（即相位函数的可学习参数）。整个网络端到端训练，优化目标为均方误差损失与 L2 正则化之和：

$$\operatorname{Cost}(\mathbf{X}, \mathbf{Y}, \mathbf{P}; {\boldsymbol{\beta}}) = \| \mathbf{Y} - \Phi(\mathbf{X}; \Theta(\mathbf{P}; {\boldsymbol{\beta}})) \| + \gamma \ | {\boldsymbol{\beta}} |$$

正则化仅施加于相位函数参数 $\beta$（$\gamma=0.01$），防止过拟合。

### 效果验证：相位影响力的数量级差异

实验定量证实了 PFNN 中相位对输出的控制力远超基线。通过测量输出相对于相位的变化幅度，**PFNN 中该值约为标准 NN（相位作为输入）的 50 倍**（$\sim 0.05$ vs $\sim 0.001$），说明相位函数化设计使相位能够全局、强有力地约束网络行为（Section 7）。这一机制使 PFNN 在崎岖地形穿越、跳跃、蹲伏等复杂交互场景中自动生成适当且富有表现力的运动（Fig. 1, Fig. 9），同时网络结构保持简洁——仅三层全连接，隐藏层 512 单元。

### 与 Motion Matching 的关系

值得注意的是，同期提出的启发式动画拼接方法 **Motion Matching** (Clavet, GDC 2016) 采用了与 PFNN 相似的参数化方式（轨迹、步态、地形高度等），但其本质是通过在大规模动画数据库中搜索最匹配片段来合成运动，不具备学习泛化能力。PFNN 可视为 Motion Matching 的**可学习、可微分版本**——通过相位函数网络隐式地学习从控制参数到姿态的映射，避免了运行时昂贵的搜索开销。

## 整体框架

![[assets/figures/papers/paper_list_l47_https_doi_org_10_1145_3072959_3073663/figures/001_Figure_1.jpg]]
*Figure 1: A selection of results using our method of character control to traverse rough terrain: the character automatically produces appropriate and expressive locomotion according to the real-time user control and the geometry of the environment*

PFNN 系统由三个核心阶段构成：数据预处理、模型训练和实时推理（Fig. 3）。整个 pipeline 的设计围绕一个关键洞察展开——**将相位（phase）从普通输入提升为网络权重的全局控制变量**，从而消除传统方法中不同相位数据混合导致的运动退化。

### 数据预处理阶段

该阶段完成从原始动捕数据到结构化训练样本的转换，包含三个关键步骤：

**动捕数据处理与特征提取。** 系统首先对约1小时的运动捕捉数据进行清洗，半自动标注相位信息——通过计算脚后跟和脚趾关节的速度幅值，检测其低于阈值的时间点来自动标记足部接触时刻，进而确定运动周期相位。同时提取步态（gait）标签作为二值向量输入，以消除不同步态间的歧义。角色根变换（root transformation）通过将髋关节中心投影到地面来获取。

**地形拟合。** 这是数据准备中最具创新性的环节。系统将动捕数据与外部高度图数据库进行对齐，采用两阶段策略：首先对每个运动周期在高度图数据库中暴力搜索10个最佳匹配的地形块；然后通过径向基函数（RBF）网格变形进行精细调整。拟合误差由三项组成：

$$E_{fit} = E_{down} + E_{up} + E_{over}$$

其中 $E_{down}$ 确保足部接触地面时地形高度与足部匹配，$E_{up}$ 防止非接触时足部与地形穿插，$E_{over}$ 处理跳跃高度约束。这一过程生成约400万帧环境-运动配对数据，处理耗时约3小时（Intel i7-6700 CPU 单线程）。消融实验证实，相比简单的RBF网格编辑方法（会导致系统过拟合到人工地形风格，在未见地形上产生异常动作），这种数据库匹配的地形拟合方法能产生更自然的运动（Fig. 13）。

**输入输出参数化。** 每帧的输入向量 $\mathbf{x}_i$ 包含：用户控制参数（以当前帧为中心的局部窗口内每10帧采样的轨迹位置 $\mathbf{t}_i^p$、方向 $\mathbf{t}_i^d$、地形高度 $\mathbf{t}_i^h$ 和步态标签 $\mathbf{t}_i^g$），以及上一帧的角色状态（相对于根变换的关节位置 $\mathbf{j}_{i-1}^p$ 和速度 $\mathbf{j}_{i-1}^v$）。输出向量 $\mathbf{y}_i$ 则包含：下一帧的预测轨迹、当前帧的关节位置/速度/角度、根变换速度、相位变化量 $\dot{p}_i$ 和足部接触标签 $\mathbf{c}_i$。Fig. 5 可视化了这一参数化方案。

### 模型训练阶段

PFNN 的核心创新在于**网络权重不是静态存储的，而是由相位函数 $\Theta$ 根据当前相位 $p$ 动态生成**（Fig. 2）。回归网络 $\Phi$ 是一个三层全连接结构，每层512个单元，使用ELU激活函数：

$$\Phi ( \mathbf { x } ; \pmb { \alpha } ) = \mathbf { W } _ { 2 } \mathrm { E L U } ( \mathbf { W } _ { 1 } \mathrm { E L U } ( \mathbf { W } _ { 0 } \mathbf { x } + \mathbf { b } _ { 0 } ) + \mathbf { b } _ { 1 } ) + \mathbf { b } _ { 2 }$$

其中所有权重矩阵 $\mathbf{W}_k$ 和偏置 $\mathbf{b}_k$ 均由参数 $\pmb{\alpha}$ 决定，而 $\pmb{\alpha}$ 本身由相位函数 $\Theta(p; \beta)$ 输出。相位函数选用三次 Catmull-Rom 样条，仅需四个控制点即可表达周期性回归需求：

$$\Theta ( p ; \beta ) = \alpha _ { k _ { 1 } } + w \left( \frac { 1 } { 2 } \alpha _ { k _ { 2 } } - \frac { 1 } { 2 } \alpha _ { k _ { 0 } } \right) + w ^ { 2 } ( \alpha _ { k _ { 0 } } - \frac { 5 } { 2 } \alpha _ { k _ { 1 } } + 2 \alpha _ { k _ { 2 } } - \frac { 1 } { 2 } \alpha _ { k _ { 3 } } ) + w ^ { 3 } ( \frac { 3 } { 2 } \alpha _ { k _ { 1 } } - \frac { 3 } { 2 } \alpha _ { k _ { 2 } } + \frac { 1 } { 2 } \alpha _ { k _ { 3 } } - \frac { 1 } { 2 } \alpha _ { k _ { 0 } } )$$

训练使用 Adam 优化器，结合 dropout（保留概率 0.7）和仅作用于相位函数参数 $\beta$ 的 L2 正则化（系数 $\gamma = 0.01$），损失函数为：

$$\operatorname { C o s t } ( \mathbf { X } , \mathbf { Y } , \mathbf { P } ; { \boldsymbol { \beta } } ) = \| \mathbf { Y } - \Phi ( \mathbf { X } ; \Theta ( \mathbf { P } ; { \boldsymbol { \beta } } ) ) \| + \gamma \ | { \boldsymbol { \beta } } |$$

完整训练在 NVIDIA GeForce GTX 660 GPU 上耗时约30小时。

### 实时推理阶段

运行时，系统根据当前相位值通过预计算或实时样条计算网络权重，支持多种速度/内存折中方案（Table 1）。输入的用户控制轨迹并非直接使用，而是通过混合函数将游戏手柄输入的期望轨迹与上一帧 PFNN 预测的轨迹进行融合：

$$TrajectoryBlend(a_0, a_1, t, \tau) = (1 - t^\tau) a_0 + t^\tau a_1$$

其中 $\tau$ 控制的非线性偏置可调节响应速度——增大 $\tau$ 使角色更紧密地跟随用户输入，但可能牺牲动画质量。回归网络前向传播后，对输出施加逆运动学（IK）后处理，生成最终的角色姿态。

### 设计动机：相位作为因果调控旋钮

理解这一 pipeline 设计的关键在于其解决的**根本瓶颈**：传统自回归模型（如 LSTM/RNN）在长时间运动生成中因误差累积导致动作逐渐消失或爆炸，而卷积模型（如 **Holden et al., ACM Trans. Graph. 2016** 的 CNN）需要完整控制信号作为输入，不适用于在线实时生成。更微妙的是，即使将相位作为额外输入的标准神经网络，由于 dropout 等机制，相位的影响力容易被稀释，导致动作僵硬不自然（Fig. 10b, Fig. 11）。

PFNN 通过让相位直接参数化整个网络的权重矩阵，实现了**约50倍于标准NN的相位影响力**（输出相对于相位的变化幅度从约0.001提升至约0.05），从根本上避免了不同相位数据的混合，消除了漂移问题。这一设计使得系统在复杂地形交互中能够自动生成适当且富有表现力的运动（Fig. 1, Fig. 9），同时保持极低的推理延迟（PFNN constant 模式约 0.0008s/帧）。

## 核心模块与公式推导

### 相位函数神经网络（PFNN）总体结构

PFNN 的核心设计是将一个标准回归网络的权重，由静态参数变为相位的函数。系统包含两个逻辑组件：**相位函数**（Phase Function）和**回归网络**（Regression Network）。每帧运行时，先由相位函数根据当前相位值 $p$ 生成网络的全部权重与偏置，再由回归网络以前一帧姿态、用户控制、环境几何为输入，输出当前帧的姿态及辅助变量（Fig. 2）。

回归网络采用三层全连接结构，使用 ELU 激活函数：

$$\Phi ( \mathbf { x } ; \pmb { \alpha } ) = \mathbf { W } _ { 2 } \mathrm { E L U } ( \mathbf { W } _ { 1 } \mathrm { E L U } ( \mathbf { W } _ { 0 } \mathbf { x } + \mathbf { b } _ { 0 } ) + \mathbf { b } _ { 1 } ) + \mathbf { b } _ { 2 }$$

其中 $\mathbf{x} \in \mathbb{R}^n$ 为输入向量，$\pmb{\alpha}$ 为网络所有可训练参数的集合（包括所有权重矩阵 $\mathbf{W}_0, \mathbf{W}_1, \mathbf{W}_2$ 和偏置 $\mathbf{b}_0, \mathbf{b}_1, \mathbf{b}_2$），每层隐藏单元数设为 512。

ELU 激活函数定义为：

$$\operatorname { E L U } ( x ) = \operatorname* { m a x } ( x , 0 ) + \exp ( \operatorname* { m i n } ( x , 0 ) ) - 1$$

该函数在负半轴平滑且有非零导数，有助于加速训练并提升模型性能。

### 相位函数：Catmull-Rom 样条

相位函数 $\Theta(p; \beta)$ 是 PFNN 区别于标准神经网络的关键模块。它以标量相位 $p$ 为输入，输出回归网络所需的全部参数 $\pmb{\alpha}$。文中选用**三次 Catmull-Rom 样条**作为相位函数，使用四个控制点实现周期性插值：

$$\Theta ( p ; \beta ) = \alpha _ { k _ { 1 } } + w \left( \frac { 1 } { 2 } \alpha _ { k _ { 2 } } - \frac { 1 } { 2 } \alpha _ { k _ { 0 } } \right) + w ^ { 2 } ( \alpha _ { k _ { 0 } } - \frac { 5 } { 2 } \alpha _ { k _ { 1 } } + 2 \alpha _ { k _ { 2 } } - \frac { 1 } { 2 } \alpha _ { k _ { 3 } } ) + w ^ { 3 } ( \frac { 3 } { 2 } \alpha _ { k _ { 1 } } - \frac { 3 } { 2 } \alpha _ { k _ { 2 } } + \frac { 1 } { 2 } \alpha _ { k _ { 3 } } - \frac { 1 } { 2 } \alpha _ { k _ { 0 } } )$$

其中 $\beta = \{\alpha_0, \alpha_1, ..., \alpha_{K-1}\}$ 为 $K$ 个控制点（实验中取 $K=4$），$k_n = ( \lfloor p K \rfloor + n - 1 ) \bmod K$ 为循环索引，$w = pK - \lfloor pK \rfloor$ 为插值权重。仅四个控制点即足以表达本系统所需的回归能力。

**因果机制**：相位通过全局控制所有网络权重，而非作为普通输入变量。消融实验证实，在 PFNN 中输出相对于相位的变化幅度约是标准 NN（相位作为输入）的 50 倍（~0.05），从根本上避免了不同相位姿态的混合，消除了角色漂浮与动作僵硬问题（Section 7, Fig. 10, Fig. 11）。

### 输入/输出参数化

**输入向量** $\mathbf{x}_i$ 包含三类信息：

$$\mathbf{x}_i = \{ \mathbf{t}_i^p, \mathbf{t}_i^d, \mathbf{t}_i^h, \mathbf{t}_i^g, \mathbf{j}_{i-1}^p, \mathbf{j}_{i-1}^v \} \in \mathbb{R}^n$$

- $\mathbf{t}_i^p, \mathbf{t}_i^d, \mathbf{t}_i^h$：以当前帧为中心的局部窗口内，每 10 帧采样的未来轨迹位置、方向及地形高度（Fig. 5 黑色部分）。
- $\mathbf{t}_i^g$：步态标签（二值向量），用于消除不同步态间的歧义。
- $\mathbf{j}_{i-1}^p, \mathbf{j}_{i-1}^v$：前一帧各关节相对于角色根节点的位置与速度（Fig. 5 粉色部分）。

**输出向量** $\mathbf{y}_i$ 包含当前帧状态与辅助预测：

$$\mathbf{y}_i = \{ \mathbf{t}_{i+1}^p, \mathbf{t}_{i+1}^d, \mathbf{j}_i^p, \mathbf{j}_i^v, \mathbf{j}_i^a, \mathbf{r}_i^x, \mathbf{r}_i^z, \mathbf{r}_i^a, \dot{p}_i, \mathbf{c}_i \} \in \mathbb{R}^m$$

- $\mathbf{t}_{i+1}^p, \mathbf{t}_{i+1}^d$：下一帧的预测轨迹位置与方向，用于运行时轨迹混合。
- $\mathbf{j}_i^p, \mathbf{j}_i^v, \mathbf{j}_i^a$：当前帧的关节位置、速度与旋转角度。
- $\mathbf{r}_i^x, \mathbf{r}_i^z, \mathbf{r}_i^a$：根节点的水平位移与绕垂直轴旋转速度。
- $\dot{p}_i$：相位变化量，驱动运动周期推进。
- $\mathbf{c}_i$：足部接触标签。

### 训练损失函数

网络以端到端方式训练，损失函数为均方误差与 L2 正则化之和：

$$\operatorname { C o s t } ( \mathbf { X } , \mathbf { Y } , \mathbf { P } ; { \boldsymbol { \beta } } ) = \| \mathbf { Y } - \Phi ( \mathbf { X } ; \Theta ( \mathbf { P } ; { \boldsymbol { \beta } } ) ) \| + \gamma \ | { \boldsymbol { \beta } } |$$

其中 $\mathbf{X}, \mathbf{Y}, \mathbf{P}$ 分别为输入、输出和相位值的批量矩阵，$\gamma = 0.01$ 为正则化系数。**正则化仅施加于相位函数参数 $\beta$**，而非回归网络权重，因为后者由样条动态生成，直接对其正则化缺乏物理意义。训练使用 Adam 优化器，dropout 保留概率 0.7，完整训练约需 30 小时（NVIDIA GTX 660 GPU），最终数据集约 400 万帧。

### 运行时轨迹混合

为平衡用户响应性与运动平滑性，运行时对轨迹输入进行非线性混合：

$$TrajectoryBlend(a_0, a_1, t, \tau) = (1 - t^\tau) a_0 + t^\tau a_1$$

其中 $a_0$ 为游戏手柄控制的期望轨迹，$a_1$ 为上一帧 PFNN 预测的轨迹，$t \in [0,1]$ 为轨迹窗口内的归一化时间，$\tau$ 为偏置参数。当 $\tau$ 较小时混合偏向 $a_0$（响应更快），较大时偏向 $a_1$（更平滑）。实验表明，调节 $\tau_v=5.0, \tau_d=10.0$ 可将平均轨迹误差从 17.29 cm 降至 5.82 cm，代价极小的动画质量损失（Table 2, Fig. 14）。

## 实验与分析

### 核心瓶颈验证：相位缺失与相位稀释的代价

PFNN 的设计根植于一个明确的实验观察：传统神经网络在处理周期性运动控制时存在系统性缺陷。作者通过一系列消融实验清晰揭示了这一瓶颈的因果链条。

**无相位输入的基线网络**（NN without phase）直接将不同相位的姿态数据混合学习。由于网络权重是静态的，训练过程被迫将步态周期中姿态迥异的样本（如左脚着地与右脚抬起）映射到同一组参数空间，导致输出退化为平均姿态。定性结果中角色呈现出明显的“漂浮”现象——脚部缺乏明确的接触与离地时序，整体运动失去重量感（Fig. 10a）。这一现象直接证实了相位信息是消除不同周期阶段样本混合的关键变量。

**将相位作为额外输入的神经网络**（NN with phase as input）试图以温和的方式引入相位信息，但效果远不如预期。由于训练中采用了 dropout（保留概率 0.7），网络存在忽略特定输入通道的倾向，相位变量的影响力在深层传播中被严重稀释。定量分析显示，在该配置下，输出相对于相位的变化幅度仅为约 0.001；相比之下，PFNN 中相位通过权重函数全局控制所有参数，该变化幅度约为 0.05——**相差约 50 倍**（Section 7）。定性结果表现为动作僵硬、不自然，角色在转向和变速时缺乏流畅的过渡（Fig. 10b, Fig. 11）。这一对比直接证明了“权重函数化”比“输入附加”是更有效的相位利用方式。

**自回归模型的误差累积**进一步排除了替代架构的可行性。Encoder-Recurrent-Decoder (ERD) 网络即使额外提供相位输入，仍因逐帧自回归的误差累积而无法学习到稳定的隐藏相位变量（Fig. 10c,d）。条件受限玻尔兹曼机（cRBM）和高斯过程自回归器（GP Autoregressor）同样受困于此，且 GP 方法的内存和计算量随数据量平方/立方增长，难以扩展到大规模数据集。

### 性能对比：速度、内存与质量的权衡

Table 1 汇总了 PFNN 与各基线方法在相同硬件环境（NVIDIA GTX 660 GPU）下的运行时性能。PFNN 提供了三种运行时配置以适配不同部署需求：


![[assets/figures/papers/paper_list_l47_https_doi_org_10_1145_3072959_3073663/figures/011_Table_1.jpg]]
*Table 1: Numerical comparison between our method and other methods described in Fig. 10*

- **PFNN constant**：预计算所有权重并存储，推理时仅执行矩阵乘法，耗时约 0.0008s/帧，内存占用约 125MB。相比标准 NN（0.0004s, 9MB）慢约 2 倍，但运动质量有质的飞跃；相比 GP 方法（约 0.1s, >1GB）快两个数量级，内存仅为八分之一。
- **PFNN linear** 与 **PFNN cubic**：在存储与实时计算之间提供折中，适用于内存受限的平台。

值得注意的是，标准 NN 虽然速度最快、内存最小，但其输出的运动质量不可接受，因此该性能优势在实际应用中无意义。PFNN 在实时性（远低于 30fps 的 33ms 预算）和内存开销（125MB 在现代硬件上完全可接受）之间取得了实用化的平衡。

### 响应性与轨迹跟随能力

角色控制的响应性是交互式应用的核心指标。PFNN 通过轨迹混合函数 `TrajectoryBlend` 调节用户输入与网络预测之间的权重：

$$\text{TrajectoryBlend}(a_0, a_1, t, \tau) = (1 - t^\tau) a_0 + t^\tau a_1$$

其中偏置参数 $\tau$ 控制未来轨迹向用户期望收敛的速度。Table 2 和 Fig. 14 给出了系统的定量响应性评估：在圆形路径场景中，当 $\tau_v=5.0, \tau_d=10.0$ 时，平均轨迹误差仅为 5.82 cm；而在波浪路径场景中采用更保守的偏置（$\tau_v=0.5, \tau_d=2.0$）时，误差为 17.29 cm。通过调节偏置参数，响应性可提升约 3 倍，代价是动画质量的轻微下降。这一可控的权衡机制使系统能根据应用场景灵活配置。


![[assets/figures/papers/paper_list_l47_https_doi_org_10_1145_3072959_3073663/figures/015_Table_2.jpg]]
*Table 2: Numerical evaluation of character responsiveness and following ability. For each scene in $\mathsf { F i g . }$ 14 we measure the average error between the desired path and that taken by the character with different biases supplied to the future trajectory blending function Eq. (9). Here $\tau _ { v }$ represents the blending bias for the future trajectory velocity, and $\tau _ { d }$ τrepresents the blendτing bias for the future trajectory facing direction (see Section 6 for a more detailed explanation)

### 地形拟合方法的消融

数据准备阶段的地形拟合策略对最终运动自然度有显著影响。作者对比了两种方法：简单的 RBF 网格编辑（直接根据足部接触点变形平面）与本文提出的数据库匹配方法（从外部高度图数据库中搜索最佳匹配地形片并拟合）。Fig. 13 的对比显示，简单网格编辑产生的人工地形风格导致网络过拟合到该特定模式，在训练时未见过的真实地形上产生异常动作；而数据库匹配方法使训练地形与运行时地形统计特性一致，从而产生更自然的泛化运动。这一消融表明，训练数据的分布匹配对于学习型角色控制系统的泛化能力至关重要。

### 失败模式与局限性

Fig. 15 展示了系统的主要失败模式：当用户提供的输入轨迹在环境中不可实现时（如地形过于陡峭），网络被迫外推到训练分布之外的区域，产生不理想的动画。这是数据驱动方法的固有局限——模型无法保证在分布外输入的合理性。

此外，系统对地形高度的感知仅限于沿轨迹的粗粒度采样点，对尖锐小障碍等高频几何细节不敏感，实际部署中需要额外的局部避障层。精确的手部接触交互（如攀爬中的抓取动作）在当前框架下无法生成，因为输入参数化中未包含手部接触的显式建模。训练时间约 30 小时（NVIDIA GTX 660），对于需要快速迭代的制作流程而言偏长，增量训练能力是重要的工程需求。

### 实验公平性说明

所有对比实验均在相同条件下进行：统一使用约 1 小时动捕数据经地形拟合后生成的约 400 万帧训练集，相同的训练/验证划分，相同的优化器（Adam）、dropout 配置（保留概率 0.7）、L2 正则化系数（$\gamma=0.01$），以及相同的网络深度（3 层）和隐藏单元数（512）。运行时性能测量在同一 NVIDIA GTX 660 GPU 上完成，确保架构层面和硬件层面的公平比较。

### 补充图表

![[assets/figures/papers/paper_list_l47_https_doi_org_10_1145_3072959_3073663/figures/009_Figure_9.jpg]]
*Figure 9: Result of the character where the future trajectory has been collided with walls, pits and other objects in the environment. By colliding the future trajectory with non-traversable objects the character will slow down or avoid such obstacles. When walking along the beam, since the measured heights on either side of the character are significantly lower than in the center, a balancing motion is naturally produced*


## 方法谱系与知识库定位

### 核心问题与因果机制

角色控制领域长期面临一个核心瓶颈：传统自回归模型（如LSTM/RNN）在长时间运动生成中因误差累积导致动作逐渐消失或爆炸，而离线卷积模型（如 **Holden et al., ACM Trans. Graph. 2016** 的CNN方案）需要完整控制信号作为输入，无法满足在线实时生成需求。将相位作为额外输入的标准神经网络，其相位影响力容易被dropout等机制稀释，导致动作僵硬或漂浮。

PFNN的因果调节变量是**相位（phase）**——将网络权重设计为相位的函数，使权值随相位周期性平滑演化。这一设计的决定性优势在于：系统只混合相同相位的样本，从根本上避免了不同相位姿态平均化导致的运动退化。定量证据表明，在PFNN中相位改变所有网络权重，输出相对于相位的变化幅度约是标准NN的50倍（∼0.05），保证了相位对输出的强约束。

### 在方法谱系中的位置

PFNN处于**数据驱动运动合成**与**实时角色控制**的交汇点，其前后方法谱系如下：

**自回归模型路线**（存在漂移问题）：
- **cRBM**（Taylor and Hinton, ICML 2009）：条件受限玻尔兹曼机，自回归生成，受漂移影响。
- **ERD**（Fragkiadaki et al., ICCV 2015）：基于LSTM的编码器-循环-解码器网络，即使额外提供相位输入，仍因自回归误差累积无法学习到隐藏的相位变量。
- **GP Autoregressor**（Wang et al., IEEE PAMI 2008）：基于高斯过程的自回归器，内存和计算量随数据量平方/立方增长，难以扩展到大数据（>1GB内存，∼0.1s/帧）。

**非学习路线**：
- **Motion Matching**（Clavet, GDC 2016）：启发式动画拼接方法，参数化方式与PFNN相似，但不具备学习泛化能力。PFNN可视为对该思想的神经网络泛化。

**PFNN的独特定位**：通过相位函数（三次Catmull-Rom样条）动态生成回归网络权重，而非将相位作为普通输入。这一设计使网络结构保持简单（三层全连接，512隐藏单元），同时相位能全局、强有力地控制输出。在性能上，PFNN constant模式（0.0008s/帧，125MB）比GP快两个数量级，比标准NN慢约2倍但质量显著更高。

### 适用边界与局限

1. **地形感知粒度粗**：系统只能粗粒度采样地形高度，对尖锐小障碍等高频细节不敏感，实际使用中需要额外的避障层。
2. **手部交互缺失**：难以处理精确手部接触的复杂交互（如爬墙），当前无法生成手部抓取等动作。
3. **训练效率低**：完整训练需约30小时（NVIDIA GTX 660 GPU），增量学习或加速训练是重要需求。
4. **外推失败**：当用户提供的输入轨迹在环境中无法实现时（如过于陡峭），系统会外推产生不理想的动画（Fig. 15）。
5. **可编辑性不足**：模型输出对艺术家来说较难预测和编辑，缺少专门的操控工具。

### 开放问题

- 如何显著加速PFNN的训练过程或实现增量训练，以支持快速添加新数据？
- 如何扩展框架以支持精确的手部接触与物体交互（如攀爬）？
- 能否提供可控性和可编辑性工具，让动画师可以干预或修正PFNN的行为？
- 将该框架应用于物理仿真，结合相位索引的反馈控制器是否能实现更稳定的崎岖地形行走？
- 相位函数网络思想能否推广到其他周期性模态数据（如心跳fMRI、周期视频），以提升学习效率？

## 原文 PDF

![[paperPDFs/TOG_2017/Phase_functioned_neural_networks_for_character_control.pdf]]
