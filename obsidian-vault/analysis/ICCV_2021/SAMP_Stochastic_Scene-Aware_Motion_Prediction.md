---
title: "SAMP: Stochastic Scene-Aware Motion Prediction"
type: paper
paper_level: A
venue: ICCV
year: 2021
pdf_ref: "paperPDFs/ICCV_2021/SAMP:_Stochastic_Scene-Aware_Motion_Prediction.pdf"
project_link: https://samp.is.tue.mpg.de
code_link: null
aliases:
- SAMP
tags:
- ICCV_2021
- topic/vision_multimodal_applications
core_operator: 通过MotionNet每帧采样的随机潜在向量 Z 控制动作风格的多样性，通过GoalNet采样的潜在向量 Z_goal 控制目标接触点/方向的多样性，并通过路径规划模块的航路点引导无碰撞导航。
primary_logic: 将条件变分自编码器（cVAE）应用于目标条件运动生成，随机采样潜在代码以产生多样化的动作序列；同时，使用另一个cVAE从物体几何中预测可行交互目标，结合显式A*路径规划，实现了杂乱场景中具有碰撞避免和多样风格的交互运动合成。
claims:
- SAMP 在坐下动作上执行时间优于 MLP/MoE，在躺下动作上成功执行而基线失败
- SAMP 的位置精度优于基线，躺下动作 PE=5.76 cm
- "SAMP 较 NSM 显著降低穿透率（坐下: 3.8% vs 8.11%）并产生非零多样性"
- GoalNet 生成的目标多样性与真实数据相当，同时具有高重建精度（位置误差 6.04 cm）
---

# SAMP: Stochastic Scene-Aware Motion Prediction

> [!tip] 核心洞察
> 将条件变分自编码器（cVAE）应用于目标条件运动生成，随机采样潜在代码以产生多样化的动作序列；同时，使用另一个cVAE从物体几何中预测可行交互目标，结合显式A*路径规划，实现了杂乱场景中具有碰撞避免和多样风格的交互运动合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | SAMP：随机场景感知运动预测 |
| 英文题名 | SAMP: Stochastic Scene-Aware Motion Prediction |
| 会议/期刊 | ICCV 2021 |
| Links | [paper](https://arxiv.org/abs/2108.08284) · [Project](https://samp.is.tue.mpg.de) |
| Topic | #topic/vision_multimodal_applications |
| Method | SAMP |
| Dataset | Sit action, Lie down action, Sit/Carry tasks, Overall actions |

> [!tip] 效果简介
> - Sit action 上，Execution Time (s) 12.53 vs MLP 13.06, MoE 12.99, GT 11.7 (SAMP更快且完成，MLP/MoE有时失败)；PE (cm) / RE (deg) 6.09 / 3.55 vs MLP 9.27/3.99, MoE 7.99/5.73 (位置误差降低约2-3 cm)。
> - Lie down action 上，Execution Time (s) 17.06 vs MLP ∞, MoE ∞, GT 15.49 (SAMP是唯一能完成任务的模型)；PE (cm) / RE (deg) 5.76 / 6.45 vs MLP ∞, MoE ∞ (SAMP成功完成并达到合理精度)。
> - Sit/Carry tasks 上，Penetration (%) 3.8 / 3.62 vs NSM 8.11 / 10.22 (穿透率降低超过50%)。

## 概述

**问题瓶颈**：现有的人‑场景交互运动合成方法难以在杂乱三维场景中生成多样化的目标驱动运动。确定性前馈网络（MLP/MoE）无法适应不同物体几何形状且缺乏风格变化；**NSM**（Starke et al., ACM Trans. Graph. 2019）虽能处理场景约束，但输出是确定性的（多样性为零），且缺乏显式路径规划，导致穿透率高（坐下 8.11%，搬运 10.22%）。躺下等复杂动作更是使基线方法完全失败。

**核心思路**：SAMP 将条件变分自编码器（cVAE）引入目标条件运动生成，通过两个随机潜在变量控制多样性——MotionNet 每帧采样的 $Z$ 控制动作风格，GoalNet 采样的 $Z_{goal}$ 控制目标接触点与朝向的多样性。同时，显式 A* 路径规划模块基于导航网格预计算无障碍路径，提供中间航路点引导角色无碰撞导航。

**方法定位**：SAMP 由三个模块串联构成流水线（Figure 2）。GoalNet 根据物体体素几何采样多样化的交互目标位置与方向；路径规划模块计算从起点到目标的无障碍路径；MotionNet 以自回归 cVAE 形式，逐帧条件生成角色姿态。该方法在方法谱系上位于“随机场景感知运动合成”节点，区别于确定性运动预测（MLP/MoE）和无随机性的场景交互方法（NSM）。

**主要结果**：
- **任务完成能力**：SAMP 是唯一能完成躺下动作的模型（执行时间 17.06s，MLP/MoE 均失败），坐下动作执行时间（12.53s）优于 MLP（13.06s）和 MoE（12.99s），接近真实数据（11.7s）（Table 2）。
- **精度**：坐下位置误差 6.09 cm，较 MLP（9.27 cm）和 MoE（7.99 cm）降低 2–3 cm；躺下位置误差 5.76 cm（Table 3）。
- **碰撞避免**：穿透率较 NSM 降低超过 50%（坐下 3.8% vs 8.11%，搬运 3.62% vs 10.22%）（Table 5）。
- **多样性**：SAMP 的动作多样性与真实数据相当（Table 1），而 NSM 的多样性为 0.0（Table 5）。GoalNet 生成的目标多样性同样与真实数据匹配，位置误差仅 6.04 cm。

**证据强度**：上述结论由多组定量实验和消融实验支撑（Table 2/3/5, Section 5.2, Appendix G），置信度 0.95–0.98。需要手动验证的是：模型对与训练数据几何形状显著不同的物体泛化能力有限（Appendix I, Figure S.7），且路径规划依赖预计算导航网格，不适用于动态场景。

## 背景与动机

### 问题背景

在计算机图形学与具身人工智能领域，合成虚拟角色在三维场景中的自然运动是一个长期挑战。这一问题的核心难点在于：角色不仅需要生成物理上合理的动作序列，还必须理解场景中物体的几何结构与语义功能，从而执行有意义的交互行为——例如绕过障碍物走向椅子并坐下、或接近桌子并拿起物体。这类**场景感知的人‑物交互运动合成**在虚拟现实、游戏开发、电影制作以及机器人仿真中具有广泛的应用需求。

### 现有方法的缺口

当前的运动合成方法在应对上述挑战时存在三个根本性瓶颈：

**1. 确定性生成导致风格单一。** 传统的运动预测模型，如前馈网络（MLP）或专家混合模型（MoE），通常将运动生成建模为确定性映射：给定历史状态和场景信息，输出唯一的下一帧姿态。这种设计无法捕捉人类行为的固有随机性——面对同一把椅子，不同的人可能以不同的速度、轨迹和身体姿态坐下。虽然某些方法引入了随机性，但它们在杂乱场景中的表现仍然受限。

**2. 缺乏显式的目标推理与路径规划。** 现有的人‑场景交互方法（如 **NSM**, Starke et al., ACM Trans. Graph. 2019）通常将物体中心作为默认交互目标，并依赖体积传感器进行局部避障。这种做法忽略了两个关键事实：(a) 物体的可行交互位置是多样且受几何约束的——椅子的坐面、扶手、靠背提供了不同的接触可能；(b) 从起点到交互目标的全局导航需要显式的无碰撞路径，仅靠局部感知难以在复杂障碍物布局中保证到达。

**3. 无法同时实现多样性与物理合理性。** 确定性方法（如 NSM）虽然能生成相对稳定的交互，但其输出多样性为零——给定相同输入，永远产生相同结果。另一方面，引入随机性的早期尝试往往导致穿透、漂浮或不完整动作等物理不合理现象。**如何在杂乱场景中同时实现目标驱动的导航、多样化的交互风格以及低碰撞率，是现有方法未能解决的瓶颈。**

### 本文动机

SAMP 的核心动机正是弥合上述缺口。本文提出将**条件变分自编码器（cVAE）**引入目标条件运动生成框架：通过每帧采样的随机潜在向量控制动作风格的多样性，通过另一个 cVAE 从物体几何中预测多样化的可行交互目标，再结合显式的 A* 路径规划模块提供全局无碰撞导航。这一设计使得 SAMP 能够在复杂室内场景中生成**多样化、目标驱动且物理合理**的人‑场景交互运动——在坐下、躺下等任务上，SAMP 是唯一能成功完成的模型，同时将穿透率降低超过 50%，并产生了与真实数据相当的多样性水平。

## 核心创新

SAMP 的核心创新在于将**人‑场景交互运动生成**从一个确定性轨迹回归问题，重构为**目标条件随机生成 + 显式路径规划**的联合框架。这直接回应了现有方法的根本瓶颈：确定性模型（如 MLP/MoE）无法产生多样化的动作风格，而已有人‑场景交互方法（如 **NSM**，Starke et al., ACM Trans. Graph. 2019）虽能处理场景约束，却缺乏随机性，输出单一，且在杂乱场景中缺乏有效的导航机制，导致高碰撞率。

SAMP 通过三个**changed slots**系统性地突破了上述限制：

| 组件 | 基线做法 | SAMP 做法 | 因果机制 |
|------|----------|-----------|----------|
| **运动生成模型** | 确定性前馈网络（MLP/MoE）或无随机性的 NSM | MotionNet：基于 cVAE 的自回归生成器，每帧从标准正态分布采样潜在代码 $Z$ | 潜在变量 $Z$ 编码了动作风格的多模态分布，使同一目标条件下可生成不同执行方式（如不同坐姿、步态） |
| **交互目标预测** | 使用物体中心作为目标（NSM）或无此组件 | GoalNet：条件变分自编码器，根据物体体素几何采样多样化的接触位置 $\hat{\pmb{g}}^p$ 和朝向 $\hat{\pmb{g}}^d$ | 从物体几何中学习可行交互区域的分布，而非硬编码单一目标点，使角色能适应不同物体形状并选择合理接触位置 |
| **场景导航策略** | 无显式路径规划（MLP/MoE）或仅依赖体积传感器（NSM） | 显式 A* 路径规划模块，基于导航网格预计算无障碍路径，提供中间航路点 | 将全局导航与局部运动生成解耦，航路点作为 MotionNet 的条件输入，引导角色在杂乱场景中无碰撞到达目标 |

这三个 slot 的协同作用形成了 SAMP 的核心因果链：**GoalNet** 提供多样化的可行交互目标 → **路径规划模块** 生成从起点到目标的无障碍全局路径 → **MotionNet** 在随机潜在代码的驱动下，沿航路点生成风格多样的局部运动序列。这一设计使得 SAMP 在躺下动作上成为唯一能完成任务的模型（MLP/MoE 均失败），并将坐下动作的穿透率从 NSM 的 8.11% 降至 3.8%，同时产生了非零的动作多样性，而 NSM 的多样性为 0.0（Table 5）。

**关键设计细节**：MotionNet 的 Interaction Encoder 专门编码物体几何与角色状态的交互特征，其重要性在消融实验中得到证实——移除该编码器后，目标位置误差从 6.09 cm 飙升至 14.82 cm（Appendix G），说明该模块是精确目标到达的关键。调度采样策略（Scheduled Sampling）则保障了长序列生成的稳定性，不使用该策略会导致角色频繁无法到达目标（Appendix D, Figure S.6）。

## 整体框架

SAMP 是一个**随机场景感知运动预测**系统，输入为 3D 杂乱场景和指定的交互动作，输出为角色从起始位置导航到目标物体并完成交互的多样化运动序列。系统由三个核心模块串联构成：**GoalNet** 负责预测可交互的目标位置与方向，**路径规划模块** 负责生成无障碍的导航路径，**MotionNet** 负责逐帧生成角色姿态。

### 模块关系与数据流

如图 2 所示，三个模块的协作流程为：

1. **GoalNet** 接收目标物体的体素表示 $I$，采样潜在变量 $\mathbf{Z}_{goal}$，输出多个可行的目标位置 $\hat{\mathbf{g}}^p$ 和方向 $\hat{\mathbf{g}}^d$（绿色球体和蓝色箭头）。
2. **路径规划模块** 基于预计算的导航网格（NavMesh），使用 A* 算法计算从角色起始位置到选定目标的障碍物回避路径，并提供中间航路点。
3. **MotionNet** 以自回归方式运行：每帧接收前一帧的角色状态 $\mathbf{X}_{i-1}$、物体几何编码、目标信息及路径航路点，从标准正态分布采样随机潜在向量 $\mathbf{Z}$，预测下一帧状态 $\hat{\mathbf{X}}_i$，直至动作执行完成。

这种设计将“去哪做”和“怎么做”解耦：GoalNet 处理目标可行性，路径规划处理空间导航，MotionNet 处理动作生成与风格多样性。

### 状态表示

MotionNet 在每帧 $i$ 操作一个高维状态向量 $\mathbf{X}_i$，其完整定义如公式 (1) 所示：

$$\mathbf{X}_i = \{ j_i^p, j_i^r, j_i^v, \tilde{j}_i^p, t_i^p, t_i^d, \tilde{t}_i^p, \tilde{t}_i^d, t_i^a, g_i^p, g_i^d, g_i^a, c_i \}$$

其中包含关节位置/旋转/速度、未来关节位置、根轨迹、目标位置/方向/动作标签和接触标签。这一设计将运动历史、目标条件和场景交互信息统一编码，为 MotionNet 的逐帧预测提供完整的上下文。

### 训练策略

为保证长序列生成的稳定性，SAMP 采用**调度采样**（Scheduled Sampling）训练，使用真实前一帧输入的概率 $P$ 随训练轮数从 1 线性衰减到 0：

$$P = \begin{cases} 1 & \text{epoch} \leq C_1, \\ 1 - \frac{\text{epoch} - C_1}{C_2 - C_1} & C_1 < \text{epoch} \leq C_2, \\ 0 & \text{epoch} > C_2. \end{cases}$$

消融实验证实，移除调度采样会导致角色频繁无法到达目标或行为不稳定（Appendix D, Figure S.6）。

### 网络架构概览

三个模块均采用三层全连接网络加 ELU 激活（Table S.3），具体架构为：

- **MotionNet**（Figure 3）：编码器包含 State Encoder 和 Interaction Encoder 两个子编码器，分别处理角色状态和物体几何；解码器采用混合专家（MoE）结构，由 Prediction Network 生成 $K$ 个专家权重，Gating Network 输出混合系数 $\omega_i$，最终预测权重为 $\pmb{\alpha} = \sum_{i=1}^{K} \omega_i \pmb{\alpha}_i$。
- **GoalNet**（Figure 4）：标准 cVAE 结构，以物体体素为条件，编码器输出潜在分布，解码器从采样 $\mathbf{Z}_{goal}$ 重建目标位置和方向。
- **路径规划模块**：非学习组件，基于 NavMesh 的 A* 搜索，输出离散航路点序列。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2108_08284/figures/002_Figure_2.jpg]]
*Figure 2: Our system consists of three main components. GoalNet predicts oriented goal locations (green sphere and blue arrow on the chair) given an interaction object. The Path Planning Module predicts an obstacle-free path from the starting position to the goal. MotionNet sequentially predicts the next character state until the desired action is executed*

## 核心模块与公式推导

SAMP 由三个功能互补的模块构成：**MotionNet** 负责逐帧姿态自回归生成，**GoalNet** 负责从物体几何中采样多样化的交互目标，**Path Planning Module** 负责在杂乱场景中计算无碰撞导航路径。三个模块的协同关系如 Figure 2 所示：GoalNet 首先为给定交互物体预测带方向的目标位置，路径规划模块据此计算从起点到目标的避障路径，MotionNet 则在目标引导下逐帧生成角色运动序列。

### MotionNet：条件变分自编码器

MotionNet 是一个自回归条件变分自编码器（cVAE），其核心设计是将运动生成建模为条件概率分布的学习问题。在每一帧，网络从前一帧状态和当前场景条件中采样随机潜在向量，从而产生多样化的动作输出。

**状态表示**：第 $i$ 帧的角色状态 $X_i$ 定义为包含关节运动学、根轨迹、目标和接触信息的综合特征向量：

$$X _ { i } = \left\{ j _ { i } ^ { p } , j _ { i } ^ { r } , j _ { i } ^ { v } , \tilde { j } _ { i } ^ { p } , t _ { i } ^ { p } , t _ { i } ^ { d } , \tilde { t } _ { i } ^ { p } , \tilde { t } _ { i } ^ { d } , t _ { i } ^ { a } , g _ { i } ^ { p } , g _ { i } ^ { d } , g _ { i } ^ { a } , c _ { i } \right\}$$

其中 $j^p, j^r, j^v$ 分别为关节位置、旋转和速度，$\tilde{j}^p$ 为未来关节位置，$t^p, t^d$ 为根轨迹位置和方向，$g^p, g^d, g^a$ 为目标位置、方向和动作标签，$c$ 为接触标签。

**编码器结构**：如 Figure 3 所示，编码器由两个子编码器组成——**State Encoder** 编码角色当前状态，**Interaction Encoder** 编码交互物体的体素几何信息。Interaction Encoder 的存在对目标到达精度至关重要：消融实验表明，移除该模块会导致目标位置误差从 6.09 cm 急剧升至 14.82 cm（Appendix G）。

**解码器与专家混合**：解码器采用专家混合（Mixture of Experts）架构，包含 Prediction Network 和 Gating Network。Gating Network 输出 $K$ 个专家的混合权重 $\omega_i$，最终预测由各专家输出加权融合：

$$\pmb { \alpha } = \sum _ { i = 1 } ^ { K } \omega _ { i } \pmb { \alpha } _ { i }$$

**训练损失**：MotionNet 的损失函数由状态重建误差和 KL 散度正则项组成：

$$\mathcal { L } _ { \mathrm { m o t i o n } } = | | \hat { \mathbf { X } } _ { i } - \mathbf { X } _ { i } | | _ { 2 } ^ { 2 } + \beta _ { 1 } K L ( Q ( Z | \mathbf { X } _ { i } , \mathbf { X } _ { i - 1 } , \pmb { I } ) | | p ( Z ) )$$

其中 $Z$ 为从标准正态分布采样的潜在向量，$Q$ 为编码器输出的后验分布，$\pmb{I}$ 为物体几何表示。KL 散度项约束潜在空间接近先验分布，$\beta_1$ 控制正则化强度。

### GoalNet：目标条件变分自编码器

GoalNet 解决的是“在物体上何处执行交互”的问题。与基线方法（如 NSM）简单使用物体中心作为目标不同，GoalNet 学习从物体体素几何到可行接触位置和方向的映射，并能采样生成多样化的目标。

**架构**：如 Figure 4 所示，GoalNet 同样基于 cVAE 框架，以物体体素表示 $\pmb{I}$ 为条件，从潜在空间采样 $\pmb{Z}_{goal}$，解码生成目标位置 $\hat{\pmb{g}}^p$ 和方向 $\hat{\pmb{g}}^d$。

**训练损失**：

$$\mathcal { L } _ { \mathrm { g o a l } } = | | \hat { \pmb { g } } ^ { p } - \pmb { g } ^ { p } | | _ { 2 } ^ { 2 } + | | \hat { \pmb { g } } ^ { d } - \pmb { g } ^ { d } | | _ { 2 } ^ { 2 } + \beta _ { 2 } K L ( Q ( \pmb { Z } _ { g o a l } | \pmb { g } ^ { p } , \pmb { g } ^ { d } , \pmb { I } ) | | p ( \pmb { Z } _ { g o a l } ) )$$

损失包含位置重建误差、方向重建误差和 KL 散度三项。在 150 个未见目标上的评估显示，GoalNet 的位置重建误差仅为 6.04 cm，方向误差为 2.29°，同时生成的目标多样性与真实数据相当。

### Path Planning Module：显式路径规划

路径规划模块采用经典的 A* 算法在预计算导航网格上搜索从角色当前位置到目标位置的无障碍路径，并生成中间航路点序列。该模块是 SAMP 在杂乱场景中实现低碰撞率的关键——定量评估表明，移除路径规划模块后穿透帧比例从 3.8% 上升至 11.2%。

### 调度采样策略

为保证长序列生成的稳定性，训练过程中采用调度采样（Scheduled Sampling），逐步从使用真实前一帧输入过渡到使用模型自身预测作为输入。设 $P$ 为使用真实输入的概率：

$$P = \begin{cases} 1 & e p o c h \leq C _ { 1 } , \\ 1 - \frac { e p o c h - C _ { 1 } } { C _ { 2 } - C _ { 1 } } & C 1 < e p o c h \leq C _ { 2 } , \\ 0 & e p o c h > C 2 . \end{cases}$$

其中 $C_1$ 和 $C_2$ 为预设的训练轮次阈值。消融实验（Appendix D, Figure S.6）表明，不使用调度采样会导致角色频繁无法到达目标或行为不稳定，验证了该策略对自回归模型长时稳定性的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2108_08284/figures/003_Figure_3.jpg]]
*Figure 3: MotionNet consists of an encoder and a decoder. The encoder consists of two sub-encoders: State Encoder and Interaction Encoder. The decoder consists of a Prediction Network to predict the next character state and a gating network that predicts the blending weights of the Prediction Network. See Sec. 3.1*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2108_08284/figures/004_Figure_4.jpg]]
*Figure 4: GoalNet generates multiple valid goal positions*

## 实验与分析

### 核心性能：执行成功率与位置精度

SAMP 在杂乱场景中的目标驱动交互任务上展现出相对于确定性基线的显著优势，尤其在需要复杂导航和精确接触的动作上。Table 2 和 Table 3 分别报告了执行时间和终点精度。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2108_08284/figures/007_Table_2.jpg]]
*Table 2: Average execution Time in seconds. ∞ means the method failed to reach the goal within 3 minutes*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2108_08284/figures/013_Table_3.jpg]]
*Table 3: Average precision in terms of positional and rotational errors (PE and RE). ∞ means the method failed to reach the goal within 3 minutes*

对于“坐下”动作，SAMP 的平均执行时间为 12.53 秒，快于 MLP（13.06 秒）和 MoE（12.99 秒）基线，且更接近真实数据（GT）的 11.7 秒。关键在于，MLP 和 MoE 有时无法在 3 分钟时限内到达目标，而 SAMP 始终能完成。对于更具挑战性的“躺下”动作，这一差距变为质变：MLP 和 MoE 完全失败（执行时间 ∞），而 SAMP 以 17.06 秒成功执行，仅略慢于 GT 的 15.49 秒。这表明，确定性前馈网络在面对杂乱场景中的远距离、非平凡导航时，缺乏鲁棒的闭环控制能力。

位置精度指标进一步验证了 SAMP 的交互质量。在“坐下”任务中，SAMP 的终点位置误差（PE）为 6.09 cm，优于 MLP 的 9.27 cm 和 MoE 的 7.99 cm。在“躺下”任务中，SAMP 的 PE 达到 5.76 cm。考虑到基线在此任务上完全失败，这一精度证明了 GoalNet 生成的目标引导和 MotionNet 的闭环执行能力共同确保了角色能够精确抵达有效交互位置。

### 多样性生成：随机潜在变量的作用

SAMP 的核心设计目标之一是生成同一动作的多样化风格，这是确定性方法（如 NSM）无法实现的。Table 1 使用平均成对距离（APD）量化了生成运动的多样性。SAMP 在行走、跑步、坐下、躺下四个动作上的 APD 分别为 5.63、5.75、5.05、6.69，与 GT 的 5.95、7.74、5.18、7.52 处于同一水平。这说明 MotionNet 每帧采样的随机潜在向量 $Z$ 成功捕获了真实数据中的动作风格分布，而非简单地回归平均姿态。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2108_08284/figures/005_Table_1.jpg]]
*Table 1: Diversity metric. Higher values indicate more diversity*

与 NSM 的直接对比（Table 5）更凸显了随机生成的价值。在“坐下”和“搬运”任务上，NSM 的多样性指标为 0.0（因其输出完全确定），而 SAMP 分别达到 0.44 和 0.26。同时，SAMP 的物理合理性显著更优：在“坐下”任务中，穿透帧占比仅 3.8%，而 NSM 高达 8.11%；在“搬运”任务中，SAMP 为 3.62%，NSM 为 10.22%。这证明 SAMP 的随机性并非以牺牲物理合理性为代价，相反，其显式路径规划和目标采样机制共同降低了碰撞风险。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2108_08284/figures/011_Table_5.jpg]]
*Table 5: SAMP vs. NSM*

### 目标预测精度与消融分析

GoalNet 作为独立模块，其重建精度直接决定下游运动的有效性。在 150 个未见过的测试目标上，GoalNet 的平均位置重建误差为 6.04 cm，方向误差为 2.29°，表明 cVAE 能够从物体体素表示中准确编码交互先验。

消融实验揭示了各组件的因果贡献：

- **移除 GoalNet（改用物体中心）**：如 Figure 6 所示，角色无法找到有效坐下位置，导致动作失败。这验证了物体中心并非合理的交互目标代理——椅子中心可能被扶手或靠背占据，而 GoalNet 学会了从几何中推断可行表面。
- **移除路径规划模块**：穿透帧比例从 3.8% 急剧上升至 11.2%（Section 5.2）。没有显式 A* 航路点引导，MotionNet 仅依赖局部传感器信息，在杂乱场景中频繁将角色驱入障碍物。
- **移除 Interaction Encoder**：目标到达精度严重退化，位置误差从 6.09 cm 飙升至 14.82 cm（Appendix G）。Interaction Encoder 负责将物体几何编码为条件信号，其缺失使 MotionNet 丧失了对场景上下文的感知能力，无法精确调整末端姿态。
- **移除调度采样**：如 Figure S.6 所示，角色在长序列生成中逐渐偏离目标，最终无法到达。调度采样通过逐步从真实输入切换至自生成输入，弥合了训练-推理分布偏移，是维持闭环稳定性的关键训练策略。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2108_08284/figures/008_Figure_6.jpg]]
*Figure 6: Without GoalNet (left), SAMP fails to sit on a valid place. SAMP with GoalNet is shown on the right*

### 运动分布质量

Table 4 报告了 Fréchet 距离，用于评估生成运动与真实运动在特征空间中的分布相似度。SAMP 在行走、跑步、坐下、躺下四个动作上的 Fréchet 距离分别为 0.95、1.12、0.89、1.05，表明生成分布与真实分布高度重叠。这一结果与 APD 多样性指标相互印证：SAMP 不仅生成了多样化的样本，且这些样本的聚合统计特性与真实数据一致，未出现模式坍塌或分布外样本泛滥。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2108_08284/figures/014_Table_4.jpg]]
*Table 4: Frechet distance. `*

### 已知失败模式

尽管 SAMP 在多数指标上表现优异，论文明确指出了若干局限性：

1. **轻微穿透**：即使配备路径规划模块，角色与物体之间仍存在约 3.8% 帧的穿透（Table 5）。这源于 MotionNet 的姿态预测未显式建模碰撞约束，A* 路径仅保证根关节的无障碍轨迹，而四肢可能与场景几何相交。
2. **几何泛化不足**：当测试物体与训练数据中的几何形状显著不同时，GoalNet 和 MotionNet 的性能均下降（Appendix I, Figure S.7）。体素编码的表示能力有限，且训练数据覆盖的物体类别和形状变体不足。
3. **静态场景假设**：路径规划依赖预计算的导航网格，无法适应动态障碍物或场景在线变化。
4. **数据标注依赖**：GoalNet 训练需要人工标注的接触目标和风格标签，限制了向新物体类别的快速扩展。

这些失败模式指向了未来的改进方向，包括引入物理仿真作为后处理精修步骤、设计更强大的几何编码器（如点云或隐式场），以及探索无监督目标发现方法。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2108_08284/figures/012_Figure_9.jpg]]
*Figure 9: Our Path Planning Module helps SAMP to successfully navigate cluttered scenes (left). NSM [47] fails in such scenes (right)*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2108_08284/figures/006_Figure_5.jpg]]
*Figure 5: SAMP generates plausible and diverse action styles and adapts to different object geometries*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2108_08284/figures/009_Figure_7.jpg]]
*Figure 7: GoalNet generates diverse valid goals on different objects. Spheres indicate goal positions, and blue arrows indicate goal directions*

## 方法谱系与知识库定位

### 问题定位与核心瓶颈

SAMP 切入的是**杂乱场景下目标驱动的人‑场景交互运动生成**问题。该领域存在一个长期未解的矛盾：现有方法要么是确定性的前馈网络，无法适应不同物体几何形状并产生多样化动作风格；要么缺乏显式路径规划，导致角色在复杂环境中频繁穿透物体；要么无法在同一动作类别下生成多种合理的执行方式（如不同的坐姿）。SAMP 将这一瓶颈分解为三个子问题——**目标多样性缺失**、**导航无碰撞能力不足**、**运动风格单一**——并通过随机生成框架逐一回应。

### 方法谱系与关键对比

**相对于确定性运动预测基线（MLP / MoE）**：SAMP 最直接的前身是使用前馈网络直接回归下一帧姿态的方法，如简单的 MLP 和 MoE（类似 Zhang et al. 2018 的混合专家架构）。这些基线在简单场景下可以工作，但在躺下动作中完全失败（Table 2 中执行时间为 ∞），因为它们缺乏目标采样和路径规划能力，一旦初始预测偏离就无法恢复。SAMP 的核心改造在于将运动生成从确定性映射转变为 **cVAE 随机采样**：每帧从标准正态分布采样潜在代码 $Z$，使模型能够为同一目标生成不同的到达路径和动作风格。

**相对于 NSM（Neural State Machine）**：NSM（Starke et al., ACM Trans. Graph. 2019）是该领域最具代表性的场景感知交互方法，但它存在两个结构性问题。其一，NSM 使用物体中心作为交互目标，这在几何形状复杂的物体上会导致无效接触（如角色坐到椅子扶手而非座面）。SAMP 用 **GoalNet（目标 cVAE）** 替代了这一硬编码策略：GoalNet 从物体体素表示中采样多样化的接触位置和朝向，重建位置误差仅 6.04 cm，方向误差 2.29°。其二，NSM 依赖体积传感器进行局部避障，缺乏全局路径规划，在杂乱场景中穿透率达 8.11%（坐动作）。SAMP 引入基于导航网格的显式 A* 路径规划模块，将穿透率降至 3.8%（Table 5），降幅超过 50%。此外，NSM 输出是确定性的，多样性指标为 0.0，而 SAMP 的 APD 多样性与真实数据相当（Table 1）。

**在 cVAE 运动生成谱系中的位置**：SAMP 的 MotionNet 继承了条件变分自编码器在运动预测中的应用范式，但将其扩展到**目标条件、场景感知的交互动作**。与通用的人体运动预测 cVAE 不同，MotionNet 的编码器包含两个子编码器——状态编码器和交互编码器——后者专门处理物体几何信息。消融实验（Appendix G）表明，移除交互编码器会导致目标位置误差从 6.09 cm 骤升至 14.82 cm，证明场景几何编码对精确交互是不可或缺的。

### 适用边界与局限

SAMP 的能力边界受以下因素制约：

1.  **物体几何泛化**：模型对与训练数据中几何形状显著不同的物体泛化能力有限（Appendix I, Figure S.7）。GoalNet 的体素编码虽能捕捉局部几何特征，但面对全新物体类别时，采样到的目标位置可能不合理。这是一个需要手动验证的局限点。

2.  **碰撞消除的不完全性**：即使有路径规划模块，SAMP 仍存在约 3.8% 的穿透帧（Table 5）。路径规划提供的是导航网格级别的无碰撞路径，但角色肢体与物体的精细交互仍可能出现轻微穿透。

3.  **静态场景假设**：路径规划依赖预计算的导航网格，不适用于动态变化的场景（如移动障碍物或其他角色）。

4.  **数据依赖性**：训练需要手动标注的目标位置和方向数据（Figure S.3），对于新的物体类别需要重新标注，限制了模型向新交互类型的快速迁移。

5.  **单角色与固定身形**：模型基于单一演员的 MoCap 数据训练，可能无法捕捉不同身材比例和运动风格的变化。

### 开放问题

从 SAMP 的局限出发，可以识别出以下值得探索的方向：

- **更好的物体几何编码**：如何设计对拓扑和尺度变化更鲁棒的几何表示（如图神经网络或隐式场），以提升 GoalNet 对未见物体的泛化能力？
- **完全消除碰撞**：能否将物理仿真或接触约束整合进生成循环，在复杂交互中实现零穿透？
- **多角色与动态场景**：如何将 SAMP 的路径规划和目标采样框架扩展到多人交互场景，或适应动态移动的物体？
- **跨身形泛化**：能否通过骨骼重定向或条件编码，使模型适应不同身高、体型的角色？
- **无监督交互风格发现**：当前依赖手动风格标注，能否以无监督方式自动从数据中发现不同的交互风格（如不同的坐姿模式）？
- **端到端路径学习**：路径规划模块目前是独立于神经网络的外部模块，能否与 MotionNet 联合学习，以提供更平滑且自适应的导航行为？

## 原文 PDF

![[paperPDFs/ICCV_2021/SAMP:_Stochastic_Scene-Aware_Motion_Prediction.pdf]]