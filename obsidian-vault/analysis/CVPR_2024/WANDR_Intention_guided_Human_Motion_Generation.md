---
title: "WANDR: Intention-guided Human Motion Generation"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/WANDR_Intention_guided_Human_Motion_Generation.pdf
aliases:
- WWDANDBGR
- WANDR
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 引入意图特征（intention features），通过后见经验重放（Hindsight Experience Replay）在训练时为无标签数据生成伪目标，统一了不同数据集的训练目标，使模型能够学习从导航到伸手的整体运动策略。
primary_logic: 将人体运动建模为自回归条件变分自编码器（c-VAE），以当前姿态、动态以及手腕/朝向/骨盆三维意图特征为条件逐帧生成姿态增量，从而在闭环反馈中动态引导角色到达任意3D目标位置，无需预定义路径或子目标。
claims:
- WANDR（AMASS+CIRCLE联合训练）在测试集上达到32%的成功率，16%的脚部滑动率，24.8 cm平均距目标距离，远优于仅使用CIRCLE（0% SR，205.4 cm）或仅AMASS（16% SR，48.0 cm）以及GOAL基线（0% SR，149.2 cm）。
- 意图特征消融实验：完整的意图向量获得32%成功率，移除任何成分（手腕、朝向、骨盆）均导致显著性能下降；仅使用VAE+优化的基线成功率仅3%、距离217 cm，证明意图机制的必要性。
- WANDR生成的运动能够跨越不同距离、角度和高度达到目标，成功率分布稳定，展示了对未见过目标位置的泛化能力。
- 3D Goal Reaching Test 上 Success Rate (SR) ↑ = 32%
---

# WANDR: Intention-guided Human Motion Generation

> [!tip] 核心洞察
> 将人体运动建模为自回归条件变分自编码器（c-VAE），以当前姿态、动态以及手腕/朝向/骨盆三维意图特征为条件逐帧生成姿态增量，从而在闭环反馈中动态引导角色到达任意3D目标位置，无需预定义路径或子目标。

| 字段 | 内容 |
|------|------|
| 中文题名 | WANDR：意图引导的人体运动生成 |
| 英文题名 | WANDR: Intention-guided Human Motion Generation |
| 会议/期刊 | CVPR 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | WANDR (Wrist-driven Autonomous Navigation for Data-based goal Reaching) |
| Dataset | 3D Goal Reaching Test |

> [!tip] 效果简介
> - 3D Goal Reaching Test 上，Success Rate (SR) ↑ 32% vs 0% (GOAL) (+32%)；Distance to Goal (DTG) ↓ (cm) 24.8 vs 48.0 (AMASS only) (-23.2)；Foot Skating (FS) ↓ 16% vs 56% (CIRCLE only) (-40%)。

## 概述

**核心问题**：现有数据驱动的人体运动生成方法面临一个结构性瓶颈——大规模无目标标签的运动捕捉数据（如AMASS）与目标导向的小型数据集（如CIRCLE）无法被联合利用。单独使用AMASS训练能保证运动自然度，但缺乏目标达成能力；单独使用CIRCLE训练则因数据量有限导致运动质量严重退化。这一矛盾使得现有方法难以在维持自然运动的同时泛化到任意未见过目标。

**核心方法**：WANDR（Wrist-driven Autonomous Navigation for Data-based goal Reaching）是一个意图引导的条件变分自编码器（c-VAE），将人体运动建模为自回归的逐帧生成过程。其关键创新在于引入**意图特征**——由手腕意图、朝向意图和骨盆意图三部分组成的条件向量——实时编码当前姿态与目标之间的空间关系。通过**后见经验重放**，WANDR在训练时为无标签数据利用未来手腕位置构建伪目标，从而统一了AMASS和CIRCLE的训练目标，使模型能够从导航到伸手学习整体的运动策略。

**核心结论**：WANDR在3D目标到达测试中达到**32%的成功率**，平均距目标距离仅**24.8 cm**，脚部滑动率低至**16%**，显著优于所有基线方法（GOAL成功率为0%，仅AMASS训练为16%，VAE+优化基线仅3%）。消融实验证实意图向量的每个成分均不可或缺，移除任一成分均导致性能显著下降。模型展示了对不同距离、角度和高度的未见过目标的稳定泛化能力。

## 背景与动机

### 问题背景：目标导向人体运动生成的现实需求

在虚拟角色动画、人机交互和具身智能领域，生成能够自然到达指定3D目标位置的人体运动是一个核心挑战。理想情况下，角色应从任意初始姿态出发，无需预定义路径或中间子目标，即可在保持运动自然度的同时，精确到达任意给定的3D目标点。这一能力对于构建可交互的虚拟人、机器人遥操作以及游戏角色控制等应用至关重要。

### 现有方法的根本瓶颈：数据异构性导致的泛化困境

当前数据驱动的人体运动生成方法面临一个结构性困境：可用的大规模运动捕捉数据集与目标导向数据集之间存在根本性的数据异构。

一方面，大规模无目标标签的运动捕捉数据（如**AMASS**，包含约17,000条序列）提供了丰富多样的自然人体运动，涵盖行走、跑步、舞蹈等日常行为，但其缺乏明确的目标标注，无法直接用于训练目标到达任务。另一方面，专门的目标导向数据集（如**CIRCLE**，约7,200条序列）提供了抓取和伸手等精细的目标交互行为，但规模有限且运动类型单一，难以泛化到未见过的新目标位置。

现有方法无法联合利用这两类互补的数据资源：
- 仅在CIRCLE上训练的模型会产生极不自然的运动（脚部滑动率高达56%），因为该数据集缺乏多样化的全身运动模式；
- 仅在AMASS上训练的模型虽然运动质量较高，但缺乏目标到达的精细技能，成功率仅16%，平均距目标距离达48.0 cm；
- 现有目标导向方法如**GOAL**（Taheri et al., CVPR 2022）无法有效泛化，在测试集上成功率为0%，平均距目标距离高达149.2 cm。

**核心瓶颈在于**：缺乏一种统一的训练机制，能够将无目标标签的大规模运动数据与目标导向的小规模数据有效融合，使模型既能保持运动的自然度，又能学习到精确到达任意目标的能力。

### WANDR的动机与核心洞察

WANDR的提出正是为了解决上述数据异构与泛化困境。其核心洞察是：**通过引入意图特征（intention features）作为条件信号，并采用后见经验重放（Hindsight Experience Replay）策略为无标签数据生成伪目标，可以统一异构数据集的训练目标**。

具体而言，WANDR将人体运动建模为自回归条件变分自编码器（c-VAE），以当前姿态、动态状态以及手腕、朝向、骨盆三维意图特征为条件，逐帧生成姿态增量。意图特征实时编码了从当前状态到达目标所需的空间与时间信息，使模型能够在闭环反馈中动态引导角色到达任意3D目标位置。在训练阶段，对于AMASS中无目标标签的序列，WANDR通过选取未来帧的手腕位置作为伪目标，构建对应的意图特征，从而将无监督的运动数据转化为有监督的目标到达学习信号。

这一设计使得WANDR能够同时从AMASS的丰富运动模式和CIRCLE的精确目标交互中学习，在保持运动自然度的同时，获得对未见过目标位置的泛化能力——在测试集上达到32%的成功率，脚部滑动率降至16%，平均距目标距离缩短至24.8 cm，显著优于所有基线方法。

## 核心创新

WANDR 的核心创新在于引入**意图特征（Intention Features）**作为条件信号，将目标导向的人体运动生成重新表述为一个统一的、数据驱动的自回归条件变分自编码器（c-VAE）框架。该方法通过三个关键设计突破现有数据驱动方法的瓶颈：

### 1. 意图特征：从“状态-动作”到“状态-意图-动作”的条件扩展

传统数据驱动方法（如 **GOAL**，Taheri et al., CVPR 2022）仅以当前姿态状态为条件生成下一帧动作，缺乏对目标位置的显式建模能力。WANDR 将条件输入从单一的状态表示 $p_i^{dyn}$ 扩展为状态与意图特征的拼接，使模型能够在闭环反馈中动态感知目标位置并调整运动策略。

意图特征由三个互补成分组成，分别从不同空间维度引导角色向目标靠近：

- **手腕意图 $I_i^w$**：编码手腕从当前位置 $W_i$ 到达目标 $G$ 所需的平均速度，公式为 $I_i^w = \frac{G - W_i}{t_G - i}$，为手部运动提供直接的时空引导信号。
- **朝向意图 $I_i^r$**：编码身体朝向与目标方向的差异。训练时使用未来帧的真实身体朝向 $H_{t_G}^{xy}$，推理时使用骨盆到目标的水平方向 $(G - P_i)^{xy}$ 作为替代，使模型学会在无真实朝向标签时自主调整身体面向。
- **骨盆意图 $I_i^p$**：通过指数饱和函数 $I_i^p = 2 \times (1 - e^{||G^{xy} - P_i^{xy}||_2}) \times \frac{G^{xy} - P_i^{xy}}{||G^{xy} - P_i^{xy}||_2}$ 将骨盆到目标的归一化方向向量压缩至最大范数为 2，避免远距离目标导致的条件信号爆炸，同时保留方向信息。

消融实验（Table 2）验证了三个成分的不可或缺性：完整的意图向量达到 32% 成功率，移除任一成分均导致性能显著下降。仅使用无条件 VAE 加优化的基线仅获得 3% 的成功率和 217 cm 的平均距目标距离，证明意图引导机制无法被简单的后优化替代。

### 2. 后见经验重放：统一无标签与有标签数据的训练策略

现有数据集的根本矛盾在于：大规模运动捕捉数据（如 AMASS）提供丰富的自然运动，但缺乏目标标注；目标导向数据集（如 CIRCLE）提供精确的目标-动作配对，但规模有限且运动多样性不足。WANDR 通过**后见经验重放（Hindsight Experience Replay）**策略统一了两类数据的训练目标：

- 对于无目标标签的 AMASS 数据，随机选取未来帧的右手腕位置作为伪目标 $G$，并以该帧作为 $t_G$ 计算意图特征。这使得模型能够从任意自然运动序列中学习“如果目标是某处，当前动作应如何调整”的因果关联。
- 对于有目标标签的 CIRCLE 数据，直接使用标注目标计算意图特征。

这一策略的因果机制在于：意图特征将“目标位置”从运动生成的外部约束转化为可学习的条件变量，使得模型在训练时始终以“目标导向”的方式理解运动，无论原始数据是否包含目标信息。实验结果（Table 1）验证了联合训练的关键作用：仅使用 CIRCLE 训练成功率为 0%、脚部滑动率高达 56%；仅使用 AMASS 训练成功率仅 16%、距目标距离 48.0 cm；联合训练达到 32% 成功率、16% 脚部滑动率和 24.8 cm 距目标距离，实现了运动自然度与目标达成能力的平衡。

### 3. 姿态增量表示：去除全局方向的归纳偏置

WANDR 将运动表示从绝对姿态改为去除全局 z 方向的姿态增量 $d_i = (d_i^{t_{-z}}, d_i^{r_{-z}}, d_i^{\theta})$，其中 $d_i^{t_{-z}}$ 和 $d_i^{r_{-z}}$ 分别表示移除全局 z 方向后的平移和旋转增量，$d_i^{\theta}$ 为身体姿态参数增量。这一设计提供了重要的归纳偏置：模型无需学习全局坐标与局部姿态之间的复杂映射，而是专注于相邻帧之间的相对变化，降低了学习难度并提升了生成运动的平滑性。

## 整体框架

WANDR 的整体框架围绕一个核心机制展开：**以意图特征为条件的自回归条件变分自编码器（c-VAE）**。该框架将人体运动生成建模为逐帧的姿态增量预测过程，在闭环反馈中动态引导角色到达任意 3D 目标位置，无需预定义路径或子目标。

### 核心设计理念

框架的根本创新在于解决了数据驱动方法中的一个关键瓶颈：大规模无目标标签的运动捕捉数据（如 AMASS）与目标导向的小型数据集（如 CIRCLE）无法被联合利用。WANDR 通过**后见经验重放（Hindsight Experience Replay）**统一了这两类数据的训练目标：对于无标签数据，随机选取未来某一帧的手腕位置作为伪目标；对于有标签数据，直接使用给定的目标位置。这一策略使得模型能够从两类数据中同时学习导航与精细操作的整体运动策略。

### Pipeline 模块与数据流

WANDR 的完整 pipeline 由五个核心模块串联构成，数据流在训练与推理阶段存在结构性差异（见 Figure 2）：

![[assets/figures/papers/paper_list_l1854_WANDR_Intention_guided_Human_Motion_Generation/figures/002_Figure_2.jpg]]
*Figure 2: WANDR architecture. During training, our model conditions on the intention vectors*

**1. 意图特征计算（Intention Feature Computation）**

该模块从当前姿态与目标位置实时计算三个互补的意图特征，为运动生成提供空间与时间引导信号（Section 3.2）：

- **手腕意图** $I_{i}^{w} = \frac{G - W_{i}}{t_{G} - i}$：手腕从当前位置 $W_i$ 到达目标 $G$ 所需的平均速度，编码了末端执行器的运动趋势。
- **朝向意图** $I_{i}^{r}$：训练时使用未来帧的真实身体朝向与当前朝向之差 $H_{t_{G}}^{xy} - H_{i}^{xy}$；推理时使用骨盆到目标的水平方向与当前朝向之差 $(G - P_{i})^{xy} - H_{i}^{xy}$，引导角色面向目标。
- **骨盆意图** $I_{i}^{p} = 2 \times (1 - e^{||G^{xy} - P_{i}^{xy}||_{2}}) \times \frac{G^{xy} - P_{i}^{xy}}{||G^{xy} - P_{i}^{xy}||_{2}}$：指数饱和的归一化方向向量，最大范数为 2，编码了身体整体向目标移动的方向信息。

消融实验（Table 2）的强证据表明，**三个意图成分缺一不可**：完整的意图向量获得 32% 成功率，移除任一成分均导致性能显著下降。

**2. 状态编码器（State Encoder）**

该模块将当前帧的 SMPL-X 局部姿态参数 $p_i$ 与上一帧的姿态增量 $d_{i-1}$ 融合，形成动态状态表示 $p_i^{dyn}$。这种设计使模型同时感知当前姿态和运动趋势，为后续的条件生成提供丰富的上下文。

**3. c-VAE 编码器（仅训练阶段）**

在训练阶段，c-VAE 编码器将真实的姿态增量 $d_i$ 映射到潜在空间中的分布参数（均值与方差），通过 KL 散度约束使潜在空间结构化。推理阶段该模块被完全移除，模型直接从先验分布采样噪声。

**4. c-VAE 解码器**

解码器以三个条件信号的拼接作为输入：动态状态 $p_i^{dyn}$、意图特征 $I_i = (I_i^w, I_i^r, I_i^p)$，以及从潜在空间采样的噪声向量。解码器输出下一帧的姿态增量预测 $\hat{d}_i$。姿态增量采用去除全局 z 方向的表示 $d_i = (d_i^{t_{-z}}, d_i^{r_{-z}}, d_i^{\theta})$，这一重要的归纳偏置使模型专注于局部运动模式，而非绝对空间位置（Section 3.3）。

**5. 姿态积分（Pose Integration）**

将解码器预测的姿态增量 $\hat{d}_i$ 叠加至前一帧姿态 $\hat{p}_{i-1}$，获得当前帧的完整姿态 $\hat{p}_i$。该模块在推理阶段形成闭环：新姿态被反馈至意图特征计算和状态编码器，驱动下一帧的生成。

### 训练与推理的差异

框架在训练与推理阶段存在关键的结构性差异（Figure 3）：

- **训练阶段**：对于 AMASS 等无目标标签数据，伪目标 $G$ 取未来随机帧的右手腕位置；对于 CIRCLE 等有标签数据，使用真实目标位置。c-VAE 编码器参与训练，通过重构损失 $\mathcal{L}_{rec}$、KL 散度损失 $\alpha\mathcal{L}_{KL}$ 和关节位置损失 $\mathcal{L}_J$ 的加权和进行优化（Section 3.4）。
- **推理阶段**：目标位置由外部指定，c-VAE 编码器被移除，直接从标准高斯分布采样噪声。朝向意图的计算方式切换为骨盆-目标方向，以适应无真实未来朝向的场景。

### 证据强度评估

框架设计的有效性由多维度实验支撑：联合训练（AMASS+CIRCLE）在测试集上达到 32% 成功率、16% 脚部滑动率、24.8 cm 平均距目标距离，显著优于仅使用单一数据集的变体（Table 1，置信度 0.98）。意图特征的消融实验进一步证实了每个成分的必要性（Table 2，置信度 0.98）。然而，框架仍存在自回归误差累积、极端目标泛化不足等局限，需在后续研究中改进。

### 补充图表

![[assets/figures/papers/paper_list_l1854_WANDR_Intention_guided_Human_Motion_Generation/figures/001_Figure_1.jpg]]
*Figure 1: WANDR starts from an arbitrary body pose and generates precise and realistic human motions that reach a specified 3D goal (depicted as a red sphere). Employing a purely data-driven approach, WANDR is a conditional Variational Autoencoder guided by intention features (depicted arrows) that steer the human’s orientation (yellow), position (cyan) and wrist (pink) towards the goal. WANDR is able to reach a wide range of goals even if they deviate significantly from the training data*

## 核心模块与公式推导

WANDR 将人体运动建模为一个自回归条件变分自编码器（c-VAE），以逐帧方式生成姿态增量。其核心设计围绕意图特征（intention features）的计算与条件注入展开，使模型能够在闭环反馈中动态引导角色到达任意3D目标位置。

### 意图特征计算（Intention Feature Computation）

意图特征是连接当前姿态与目标位置的关键桥梁，由三个互补的成分构成，分别从手腕、朝向和骨盆三个层面编码到达目标所需的空间与时间信息。

**手腕意图（Wrist Intention）** 编码手腕从当前位置到达目标所需的平均速度：

$$I_{i}^{w} = \frac{G - W_{i}}{t_{G} - i}$$

其中 $G$ 为目标位置，$W_i$ 为第 $i$ 帧的手腕位置，$t_G$ 为目标时间步。该特征为模型提供了到达目标所需的运动速率与方向信息，其分母随时间递减，使得越接近目标时刻，速度信号的引导作用越强。

**朝向意图（Orientation Intention）** 引导角色身体朝向与目标方向对齐，训练与推理阶段采用不同的计算方式：

$$I_{i}^{r} = \begin{cases} H_{t_{G}}^{xy} - H_{i}^{xy} & \text{during training} \\ (G - P_{i})^{xy} - H_{i}^{xy} & \text{during inference} \end{cases}$$

训练时，$H_{t_G}^{xy}$ 是目标时刻身体在水平面上的朝向向量，$H_i^{xy}$ 是当前朝向向量，两者之差引导角色旋转至目标姿态。推理时，由于没有目标时刻的姿态信息，改用骨盆到目标的水平方向 $(G - P_i)^{xy}$ 作为期望朝向，使角色面向目标点。这种训练-推理的非对称设计是后见经验重放策略的自然延伸。

**骨盆意图（Pelvis Intention）** 提供骨盆到目标的归一化方向，并引入指数饱和机制：

$$I_{i}^{p} = 2 \times (1 - e^{||G^{xy} - P_{i}^{xy}||_{2}}) \times \frac{G^{xy} - P_{i}^{xy}}{||G^{xy} - P_{i}^{xy}||_{2}}$$

其中 $P_i^{xy}$ 为骨盆在水平面上的位置。该特征本质是一个缩放的单位方向向量：当骨盆距离目标较远时，指数项 $(1 - e^{-d})$ 趋近于1，向量模长接近2；当骨盆接近目标时，模长衰减至接近0。这种设计使模型在远距离时有强方向引导，在近距离时避免过冲。

### 姿态增量表示（Pose Delta Representation）

WANDR 不直接预测绝对姿态，而是生成相邻帧间的姿态增量 $d_i$，以获得重要的归纳偏置——相邻帧的姿态变化通常较小且分布更集中：

$$d_i = (d_i^{t_{-z}}, d_i^{r_{-z}}, d_i^{\theta})$$

其中 $d_i^{t_{-z}}$ 是去除全局 $z$ 方向后的平移增量，$d_i^{r_{-z}}$ 是去除全局 $z$ 旋转后的朝向增量，$d_i^{\theta}$ 是 SMPL-X 身体姿态参数的增量。移除全局 $z$ 分量使模型专注于与目标到达相关的水平面运动和身体姿态变化，而不被绝对高度或全局旋转所干扰。

### 条件注入与自回归生成

在每一帧 $i$，模型将当前动态状态 $p_i^{dyn}$（包含当前姿态参数及上一帧的姿态增量 $d_{i-1}$）与意图特征 $I_i = (I_i^w, I_i^r, I_i^p)$ 拼接作为条件，输入 c-VAE 解码器。解码器同时接受从标准高斯分布采样的噪声 $z \sim \mathcal{N}(0, I)$，生成当前帧的姿态增量 $\hat{d}_i$。新姿态 $\hat{p}_i$ 通过将 $\hat{d}_i$ 叠加至前一帧姿态 $\hat{p}_{i-1}$ 获得，形成闭环自回归生成过程。

### 训练损失

训练时，c-VAE 编码器将真实姿态增量 $d_i$ 编码至潜在空间，解码器以条件信号和潜在变量为输入重构增量。整体损失函数为：

$$\mathcal{L} = \mathcal{L}_{rec} + \alpha \mathcal{L}_{KL} + \mathcal{L}_J$$

其中 $\mathcal{L}_{rec}$ 为姿态增量重构损失，$\mathcal{L}_{KL}$ 为潜在分布与先验分布间的 KL 散度，$\mathcal{L}_J$ 为关节位置损失（将预测姿态通过前向运动学计算关节位置后与真实关节位置比较），$\alpha$ 为 KL 项权重。关节位置损失的引入有助于约束生成运动的全局合理性，缓解仅优化局部增量可能导致的误差累积。

### 后见经验重放（Hindsight Experience Replay）

对于无目标标签的数据（如 AMASS），WANDR 在训练时随机选取未来某一帧 $t_G$，将该帧的右手腕关节位置作为伪目标 $G$（见 Figure 3）。这使得模型能够从大规模无标签运动捕捉数据中学习到达任意位置的策略，统一了有标签（CIRCLE）与无标签（AMASS）数据集的训练目标，是 WANDR 能够泛化到未见目标位置的核心训练机制。

![[assets/figures/papers/paper_list_l1854_WANDR_Intention_guided_Human_Motion_Generation/figures/003_Figure_3.jpg]]
*Figure 3: In training, if goals are not specified, they are determined by the future wrist location at a randomly selected future timestep, compensating for the lack of paired ground-truth data in AMASS and direct human motion through intention vectors. During inference, target locations are used as goals with intention vectors calculated based on these specific locations*

## 实验与分析

### 实验设置

WANDR 的训练数据来自 AMASS 和 CIRCLE 两个数据集的联合。AMASS 提供约 17k 个无目标标签的大规模运动捕捉序列，CIRCLE 提供约 7.2k 个目标导向的抓取运动序列，经筛选后共约 20k 个序列用于训练。数据集按 80%/10%/10% 划分为训练集、验证集和测试集。

评测指标包括三项核心指标：**成功率（Success Rate, SR ↑）**——角色手腕到达目标 15 cm 半径内即视为成功；**距目标距离（Distance to Goal, DTG ↓）**——角色手腕与目标之间的最终欧氏距离；**脚部滑动率（Foot Skating, FS ↓）**——脚部速度超过阈值的帧占比，用于衡量运动自然度。

### 主实验结果

Table 1 展示了 WANDR 在不同训练数据配置下与基线方法 **GOAL**（Taheri et al., CVPR 2022）的对比。核心发现如下：

![[assets/figures/papers/paper_list_l1854_WANDR_Intention_guided_Human_Motion_Generation/figures/005_Table_1.jpg]]
*Table 1: We evaluate WANDR trained on different datasets and compare with GOAL [32]. Training solely on CIRCLE results in unrealistic motions, whereas AMASS excels in motion quality but struggles with finer goal-reaching skills. WANDR, leveraging both of what these datasets offer, demonstrates realistic motions as well as better ability to reach goals compared to baselines and existing methods*

- **WANDR（AMASS+CIRCLE 联合训练）** 在测试集上达到 **32% 的成功率**，**24.8 cm 平均距目标距离**，**16% 脚部滑动率**，三项指标均显著优于所有对比配置。
- **仅使用 CIRCLE 训练**：成功率 **0%**，距目标 **205.4 cm**，脚部滑动高达 **56%**。CIRCLE 数据量小且场景单一，导致模型无法泛化到测试集中的未见过目标，同时生成的运动极不自然。
- **仅使用 AMASS 训练**：成功率 **16%**，距目标 **48.0 cm**，脚部滑动 **17%**。AMASS 提供了丰富的运动多样性，但因缺乏目标导向标签，模型难以学习精确的到达行为。
- **GOAL 基线**：成功率 **0%**，距目标 **149.2 cm**，脚部滑动 **40%**。该数据驱动抓取方法在泛化到任意 3D 目标时完全失效。

这些结果揭示了 WANDR 的核心因果机制：AMASS 提供运动自然度的先验，CIRCLE 提供目标到达技能的监督信号，后见经验重放（Hindsight Experience Replay）机制将两者统一为同一训练范式，使模型在保持运动质量的同时获得泛化到未见过目标的能力。

### 消融实验

Table 2 报告了对意图特征各成分的消融结果，以及一个无条件 VAE+优化的基线对比：

![[assets/figures/papers/paper_list_l1854_WANDR_Intention_guided_Human_Motion_Generation/figures/007_Table_2.jpg]]
*Table 2: Ablation Study. We evaluate the impact of each component of the intention vector. We also compare with an optimization baseline that does not use any condition signals. The results highlight the effectiveness of all of the components of intention as well as the fact that the complexity of the task makes “brute-forcing” with optimization unsuccessful*

- **完整意图向量**：成功率 32%，距目标 24.8 cm，脚部滑动 16%。
- **移除手腕意图（w/o wrist）**：成功率降至 **7%**，距目标恶化至 **72.7 cm**。手腕意图直接编码了末端执行器到达目标所需的速度信息，是目标到达的核心驱动信号。
- **移除朝向意图（w/o orientation）**：成功率降至 **18%**，距目标 **39.6 cm**。朝向意图引导角色面向目标方向，缺失时角色难以调整身体朝向以配合手腕到达。
- **移除骨盆意图（w/o pelvis）**：成功率降至 **20%**，距目标 **37.5 cm**。骨盆意图提供全局位移方向，缺失时角色缺乏向目标靠近的驱动力。
- **VAE+优化基线**：成功率仅 **3%**，距目标 **217 cm**。该基线使用无条件 VAE 生成运动后通过优化逼近目标，结果极差，表明“蛮力”优化无法替代意图引导——目标到达任务的复杂度和高维动作空间的搜索难度远超简单优化的能力范围。

消融实验的结论是确定的：意图向量的三个成分（手腕、朝向、骨盆）**均不可或缺**，它们各自提供互补的空间与时间引导信息，共同构成完整的到达策略。

### 泛化能力分析

Figure 5 展示了 WANDR 在不同目标高度、角度和距离下的成功率分布。结果表明，模型在训练分布覆盖的区域内表现稳定，能够跨越不同距离和角度到达目标。然而，在目标位置位于**极低（接近地面）或极高（远超头顶）** 的区域时，成功率明显下降——这与训练数据中此类极端姿态的稀缺直接相关，属于数据驱动的固有局限。

![[assets/figures/papers/paper_list_l1854_WANDR_Intention_guided_Human_Motion_Generation/figures/006_Figure_5.jpg]]
*Figure 5: We show the success rates of reaching goals at various heights, angles, and distances from the initial human pose. It highlights how goal position affects the model in accurately navigating and achieving the goals*

### 失败模式与局限

除上述极端目标位置的泛化衰减外，WANDR 还存在以下失败模式：

1. **误差累积**：自回归生成过程中，每帧的预测误差会逐步累积，导致角色可能陷入无法恢复的姿态，尤其在长序列生成时更为明显。
2. **目标类型受限**：当前模型仅考虑空中的 3D 目标点，未涉及实际抓取手势或物体交互，生成的运动是“指向目标”而非“操作目标”。
3. **缺乏环境上下文**：模型未考虑场景几何信息，无法进行避障或路径规划，这在真实应用场景中可能造成穿透或碰撞。

### 关键图表结论

- **Figure 2**（网络架构图）：展示了 WANDR 的训练与推理流程——训练时通过未来手腕位置构建伪目标，推理时使用指定目标位置计算意图向量，c-VAE 以意图、状态和噪声为条件自回归生成姿态增量。
- **Figure 4**（定性结果）：展示了从不同初始姿态出发到达各类目标的多样化运动，包括非面向目标的初始朝向、伸手够高处目标、弯腰触地目标等场景，验证了模型对未见过目标位置的适应能力。
- **Table 1 & Table 2**：联合训练与意图机制的定量证据，构成了本文的核心实验支撑。

![[assets/figures/papers/paper_list_l1854_WANDR_Intention_guided_Human_Motion_Generation/figures/004_Figure_4.jpg]]
*Figure 4: Diverse motion generated with WANDR: Displaying a range of motions generated by WANDR from various initial poses towards arbitrary goals. Examples include navigating towards goals from initial orientations not facing the goal*

## 方法谱系与知识库定位

### 任务背景与瓶颈定位

数据驱动的人体运动生成长期面临一个结构性矛盾：大规模运动捕捉数据集（如AMASS）提供了丰富的自然运动先验，但缺乏明确的目标标签；而目标导向的小型数据集（如CIRCLE）虽包含抓取与伸手动作，却因规模有限导致生成的运动自然度不足。现有方法无法在单一框架内联合利用这两类数据，导致在保证运动质量的同时难以泛化到任意未见过目标位置。WANDR的核心贡献在于识别并突破了这一瓶颈——通过引入意图特征（intention features）与后见经验重放（Hindsight Experience Replay），将无标签数据转化为可监督信号，从而统一了异质数据集的训练目标。

### 与基线方法的关系

**GOAL**（Taheri et al., CVPR 2022）是数据驱动的抓取运动生成方法，但其设计依赖于明确的目标标签数据，无法利用AMASS等大规模无标签运动捕捉数据。在WANDR的测试基准上，GOAL的成功率（Success Rate）为0%，平均距目标距离（DTG）达149.2 cm，表明其完全无法泛化到训练分布外的目标位置（Table 1）。

**VAE+优化基线**（无条件VAE后接优化）代表了一类朴素的替代方案：先训练无条件的运动生成模型，再通过优化方式引导角色到达目标。该基线仅获得3%的成功率和217 cm的距目标距离（Table 2），证明“暴力优化”无法替代意图引导机制。这一结果从反面验证了意图特征在闭环反馈中的因果必要性——优化方法缺乏对目标空间关系的结构化编码，难以在复杂姿态空间中有效搜索。

**仅使用CIRCLE或AMASS单独训练**的变体进一步揭示了数据瓶颈：CIRCLE单独训练成功率0%，且脚部滑动率高达56%，运动极不自然；AMASS单独训练虽运动质量较好（脚部滑动率16%），但成功率仅16%，距目标距离48 cm（Table 1）。WANDR通过联合训练将成功率提升至32%，距目标距离降至24.8 cm，同时保持16%的低脚部滑动率，实现了运动自然度与目标达成能力的折中。

### 方法谱系中的位置

WANDR在方法谱系中处于**条件运动生成**与**目标导向控制**的交汇点。其技术路线可定位如下：

- **条件变分自编码器（c-VAE）** 构成生成主干，以自回归方式逐帧预测姿态增量 $d_i = (d_i^{t_{-z}}, d_i^{r_{-z}}, d_i^{\theta})$，而非绝对姿态。这一设计引入的归纳偏置使模型专注于帧间变化，降低了学习难度（Section 3.3）。

- **意图特征**是WANDR区别于一般条件生成模型的关键创新。手腕意图 $I_i^w$、朝向意图 $I_i^r$ 和骨盆意图 $I_i^p$ 共同构成一个紧凑的引导信号，编码了从当前姿态到目标的空间关系与时间紧迫性。消融实验表明，移除任一成分均导致成功率显著下降（Table 2），证实了三者的互补性。

- **后见经验重放**借鉴了强化学习中的技术思想，在训练时为AMASS数据随机选取未来帧的手腕位置作为伪目标，使无标签数据也能参与条件生成训练。这一策略是WANDR能够联合利用异质数据集的核心机制。

与基于强化学习或运动规划的方法不同，WANDR完全依赖数据驱动，无需预定义路径、子目标或显式物理约束，而是通过意图特征在闭环反馈中动态引导角色。

### 适用边界

WANDR的有效性受以下边界条件约束：

1. **目标空间分布**：模型在到达极低或极高目标时表现较差，这些区域缺乏足够的训练数据覆盖。Figure 5的成功率分布分析显示，目标高度、角度和距离对成功率有显著影响，分布外目标的性能下降明显。

2. **误差累积**：自回归生成框架中，每帧的预测误差会逐步累积，可能导致角色陷入无法恢复的姿态。这是自回归方法的固有局限。

3. **任务范围**：当前方法仅考虑空中的3D目标点到达，未涉及实际抓取手势生成或物体交互。WANDR生成的是“到达目标”的运动，而非“操作目标”的全流程动作。

4. **环境上下文缺失**：模型未使用场景几何或障碍物信息，因此不具备避障能力，仅适用于无障碍空间中的目标导向运动。

### 局限与开放问题

WANDR揭示了意图引导运动生成的可行性，但留下了若干待解决的问题：

1. **分布外泛化**：如何使意图机制对极端分布外的目标位置保持高泛化能力？当前的指数饱和骨盆意图 $I_i^p = 2 \times (1 - e^{||G^{xy} - P_i^{xy}||_2}) \times \frac{G^{xy} - P_i^{xy}}{||G^{xy} - P_i^{xy}||_2}$ 在远距离时趋于饱和，可能限制长程引导的有效性。

2. **误差累积缓解**：是否可以通过改进训练策略（如scheduled sampling）或引入闭环校正机制来减少自回归生成中的误差累积？

3. **从到达走向交互**：如何将意图引导框架扩展至真实抓取手势生成和物体交互，实现全流程的目标导向动作？这需要融合手部姿态精细建模与接触约束。

4. **环境感知整合**：引入场景几何信息是否可以进一步提升导航能力，使角色在复杂环境中自主避障并到达目标？这需要将意图特征与场景表征进行联合编码。

5. **意图机制的通用性**：当前意图特征专为手腕到达设计，该框架是否可以泛化至其他末端执行器（如脚部、头部）或其他任务类型（如踢球、头顶物体），仍有待验证。

## 原文 PDF

![[paperPDFs/CVPR_2024/WANDR_Intention_guided_Human_Motion_Generation.pdf]]