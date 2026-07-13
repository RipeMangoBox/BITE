---
title: "Mode-adaptive neural networks for quadruped motion control"
type: paper
paper_level: A
venue: TOG
year: 2018
pdf_ref: paperPDFs/TOG_2018/Mode_adaptive_neural_networks_for_quadruped_motion_control.pdf
code_link: https://github.com/sebastianstarke/AI4Animation/tree/master/AI4Animation/SIGGRAPH_2018
project_link: https://github.com/sebastianstarke/AI4Animation/tree/master/AI4Animation/SIGGRAPH_2018
aliases:
- MANN
- MANNM
- MANNQMC
tags:
- TOG_2018
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "门控网络（gating network）根据足端速度、当前动作标签和期望速度，动态计算一组专家权重（expert weights）的混合系数，使运动预测网络（motion prediction network）的权重在不同运动模式下自适应组合，从而在无人工相位/步态标签的条件下学习多模态运动。"
primary_logic: "将混合专家（MoE）的思想应用于特征级权重混合而非输出层混合，允许网络在无监督学习中自动为不同的运动时序、步态和非周期动作专门化控制点（expert），从根本上避免跨相位的错误插值，无需任何手动标签即可从非结构化数据中合成高质量、可交互的四足动画。"
claims:
- "MANN 在无需步态/相位标签的条件下，合成的步态（walk, pace, trot, canter）在不同期望速度下自然涌现，且速度分布与现有物理控制模型一致（Fig. 5）。"
- "与 vanilla NN 和 PFNN 相比，MANN 显著降低了足部滑动（Table 2）并增大了关节角更新幅度（Table 3），表明运动更具动态且更贴近真实数据。"
- "路径跟随实验中，MANN 在所有轨迹形状上的位置和角度偏差均低于 vanilla NN 和 PFNN（Table 4）。"
- "消融研究证实不同专家权重各自专门化于特定运动模式（如跳跃、转向、特定步态），选择性屏蔽会导致相应运动丧失（Table 5），且激活曲线展示清晰的周期/专门化模式（Fig. 9）。"
---

# Mode-adaptive neural networks for quadruped motion control

> [!tip] 核心洞察
> 将混合专家（MoE）的思想应用于特征级权重混合而非输出层混合，允许网络在无监督学习中自动为不同的运动时序、步态和非周期动作专门化控制点（expert），从根本上避免跨相位的错误插值，无需任何手动标签即可从非结构化数据中合成高质量、可交互的四足动画。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 用于四足动物运动控制的模式自适应神经网络 |
| 英文题名 | Mode-adaptive neural networks for quadruped motion control |
| 会议/期刊 | TOG 2018 |
| Links | [paper](https://doi.org/10.1145/3197517.3201366) · [GitHub](https://github.com/sebastianstarke/AI4Animation/tree/master/AI4Animation/SIGGRAPH_2018) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | Mode-Adaptive Neural Networks (MANN) |
| Dataset | Quadruped locomotion (walk, pace, trot, canter), Trajectory following (circle, square, star, custom paths) |

> [!tip] 效果简介
> - Quadruped locomotion (walk, pace, trot, canter) 上，Average foot skating (cm/frame) 为 MANN4: 0.23 (all legs), 0.10 (back legs); MANN8: 0.22 (all legs), 0.09 (back legs)，对比 PFNN and Vanilla NN: higher values (see Table 2)，变化 MANN 显著减少足部滑动，更接近真实数据水平。
> - Quadruped locomotion (walk, pace, trot, canter) 上，Average angular update per joint (°/frame) 为 MANN4: 3.43 (all legs), 2.82 (back legs); MANN8: 3.69 (all legs), 3.05 (back legs)，对比 PFNN and Vanilla NN: lower values (see Table 3)，变化 MANN 产生更大的关节角变化，避免运动僵硬。
> - Trajectory following (circle, square, star, custom paths) 上，Position deviation (cm) / Angle deviation (°) 为 MANN: circle 2.98/3.21, square 4.65/7.21, star 6.61/8.76, custom 5.31/6.75，对比 Vanilla NN and PFNN: higher deviations (see Table 4)，变化 MANN 在所有路径形状上获得最低的位置和角度偏差。

## 概要

四足动物的运动控制是计算机动画中的经典难题，其核心瓶颈在于运动模式的高度多模态性——行走（walk）、踱步（pace）、小跑（trot）、慢跑（canter）等步态拥有截然不同的脚着地时序，且步态间的转换涉及复杂的相位协调。传统方法如 **Phase-Functioned Neural Networks (PFNN)**（Holden et al., SIGGRAPH 2017）依赖显式的手工标注相位参数，在单一全局相位下对不同步态进行插值，当步态转换时极易因相位失配产生混合伪影。此外，非结构化的四足动作捕捉数据缺乏天然的结构化标签，手工标注步态和相位既耗时又容易引入错误。

针对上述问题，本文提出了 **Mode-Adaptive Neural Networks (MANN)**，其核心洞察在于将混合专家（Mixture of Experts, MoE）的思想从传统的输出层混合迁移到**特征级权重混合**：由一个门控网络（gating network）根据足端速度、动作标签和期望速度，动态计算多组专家权重（expert weights）的混合系数，使运动预测网络（motion prediction network）的权重在不同运动模式下自适应组合。这一设计使得网络能够在无监督学习中自动为不同的运动时序、步态和非周期动作专门化各自的专家控制点，从根本上避免了跨相位的错误插值，**无需任何步态或相位标注**即可从非结构化数据中端到端地学习高质量的四足运动合成。

实验结果表明，MANN 在多个维度上显著优于 vanilla NN 和 PFNN：足部滑动量大幅降低（Table 2），关节角更新幅度更接近真实数据（Table 3），路径跟随任务中的位置和角度偏差在所有轨迹形状上均为最低（Table 4）。消融研究进一步证实，不同的专家权重确实分化出对跳跃、转向、特定步态等运动模式的专门控制能力（Table 5, Fig. 9），且系统可在 CPU 上以约 2 ms/帧的速率实时运行，支持游戏手柄交互控制。

在方法谱系上，MANN 属于数据驱动的运动合成方法，与物理仿真（如轨迹优化、力矩控制）和运动匹配（Motion Matching）等思路并行，但其“特征级专家混合”的架构设计为处理高度多模态的运动数据提供了一条独特的技术路径，有望推广至其他多模态学习任务。

四足动物运动控制是计算机动画领域的核心难题之一。与人类角色不同，四足动物展现出高度多模态的运动特性——行走、踱步、小跑、慢跑等步态的脚着地模式各异（Fig. 2），且步态之间的转换涉及复杂的时序协调。这种多模态性对数据驱动的角色动画方法构成了根本性挑战。

### 现有方法的瓶颈

传统数据驱动方法在处理四足运动时面临两个相互交织的困境。

**相位依赖与插值伪影。** 以 **PFNN**（Holden et al., ACM Trans. Graph. 2017）为代表的方法依赖显式的相位函数，根据手工标注的相位变量在相同相位的运动间进行插值。然而，不同步态的相位结构天然不同——例如，行走（walk）与小跑（trot）的脚着地时序无法对齐——当网络被迫在步态转换时进行跨相位插值，就会产生混合伪影，导致足部滑动、姿态僵硬等问题。本质上，单一全局相位参数无法表征四足运动的多模态时序结构。

**标注成本与可扩展性。** PFNN 需要为所有运动片段手工或半自动标注步态类别和相位增量。对于非结构化的四足动作捕捉数据，这一过程极为费时且易出错。实际采集的四足运动数据往往包含大量未标注的过渡动作、非周期行为和稀有步态，手工标注不仅成本高昂，更难以保证一致性。这限制了数据驱动方法在大规模、多样化四足运动数据上的应用。

### 核心动机

本文的核心动机源于一个关键观察：**混合专家（Mixture of Experts, MoE）** 的思想为解决上述困境提供了新路径。传统 MoE 在输出层进行专家混合，而本文将其推广至**特征级权重混合**——让网络的不同专家权重自动专门化于不同的运动时序、步态和非周期动作，由门控网络根据当前运动状态动态计算混合系数。这一设计从根本上避免了跨相位的错误插值，因为网络不再依赖单一的全局相位，而是在权重空间中自适应地组合多个专门化的运动模式。

更重要的是，这种架构允许系统在**无任何步态标签或相位标签**的条件下，从非结构化动作捕捉数据中端到端地学习多模态运动。门控网络以足端速度、动作标签和期望速度为条件，自动发现不同运动模式之间的边界和转换逻辑，使步态在期望速度变化时自然涌现，而无需人工定义的先验规则。

简言之，本文的目标是构建一个无需手工相位标注、能够从非结构化数据中自动学习多模态四足运动的神经网络架构，从根本上解决现有方法在步态转换时的伪影问题，并显著降低数据预处理的门槛。

## 核心方法与创新机理

MANN 的核心创新在于将**混合专家（Mixture of Experts）思想从输出层混合提升到特征级权重混合**，从而在完全无监督的条件下解决四足运动控制中的高度多模态问题。

### 问题瓶颈

四足动物运动具有天然的强多模态性——行走、踱步、小跑、慢跑等步态的脚着地模式各异（见 Fig. 2），且步态间的转换涉及复杂的时序调整。此前的方法，如 **PFNN**（Holden et al., ACM Trans. Graph. 2017），依赖单一全局相位参数在相同相位的运动间进行插值。然而，当跨越不同步态时，相位难以对齐，导致混合伪影。更关键的是，PFNN 需要为所有运动片段手工标注步态类别和相位增量，这对非结构化的四足动作捕捉数据而言极为费时且易出错。Vanilla NN 则完全缺乏处理多模态的机制，只能回归到模糊的平均姿态。

### 关键机制：特征级专家混合

MANN 的解决方案是引入一个**门控网络（Gating Network, Ω）**，根据当前足端速度、动作标签和期望速度，动态计算一组专家权重的混合系数 ω。运动预测网络（Motion Prediction Network, Θ）的权重 α 并非固定参数，而是由 K 组可学习的专家权重 {α₁, ..., α_K} 通过 ω 线性混合得到：

$$\alpha = \sum_{i=1}^{K} \omega_i \alpha_i$$

这一设计的本质区别在于：传统 MoE 在输出层混合多个专家的预测结果，而 MANN 在**特征提取层**混合专家权重，使网络本身的结构随运动模式动态变化。这允许不同专家权重在训练中自动专门化于特定的运动时序、步态和非周期动作——无需任何人工标签引导。

### 与 Baseline 的核心差异

| 创新维度 | PFNN（Holden et al. 2017） | MANN（本文） |
|---------|---------------------------|-------------|
| 运动插值机制 | 显式相位函数，按手工标注的相位变量插值 | 门控网络动态混合专家权重，以足端速度和期望速度为条件 |
| 数据预处理 | 需手工标注步态类别和相位增量 | 无需任何步态/相位标签，端到端训练 |
| 网络输入 | 包含相位增量和脚步接触信息 | 门控网络输入精简为足端速度、动作向量和期望速度（x̂ ∈ ℝ¹⁹）；运动预测网络额外输入上一帧关节旋转以增强运动锐度 |

### 证据支撑

消融实验（Table 5）提供了最直接的因果证据：选择性屏蔽特定专家权重会导致相应运动能力丧失——α₁ 禁用则跳跃失败，α₂ 禁用则左转失败，α₅ 禁用则慢跑和小跑失败。这证实了专家权重在无监督训练中自发分化出了对不同运动模式的专门控制能力。Fig. 9 的激活曲线进一步展示：低速步行时多个权重呈周期性交替，高速运动和跳跃时特定权重持续高激活，验证了专家对时序和模式的自适应专门化。

![[assets/figures/papers/paper_list_l41_https_doi_org_10_1145_3197517_3201366/figures/001_Figure_1.jpg]]
*Figure 1: A selection of results using our method for quadruped animation. We show some different modes for sitting, turning trot, pace, canter, jumping and standing from left to right. The locomotion gaits are not labeled individually, but naturally produced by the movement velocity control*

MANN 由两个核心模块构成：**运动预测网络（Motion Prediction Network, Θ）** 和 **门控网络（Gating Network, Ω）**（Fig. 3），二者通过端到端联合训练，无需任何步态标签或相位标注即可从非结构化动作捕捉数据中学习多模态运动。

**运动预测网络**是一个三层全连接网络（Equation 1），其权重并非固定参数，而是由 $K$ 组可学习的**专家权重（expert weights）** $\{\alpha_1, \dots, \alpha_K\}$ 经门控网络输出的混合系数 $\omega$ 线性组合得到（$\alpha = \sum_i \omega_i \alpha_i$）。该网络以前一帧的角色状态 $\mathbf{x}$ 为输入（包含轨迹位置、方向、速度、期望速度、动作标签以及上一帧的关节旋转），预测当前帧的姿态、关节及轨迹更新 $\mathbf{y}$。将上一帧的关节旋转纳入输入，是为了产生更锐利、更具动态感的运动。

**门控网络**同样为三层全连接结构（Equation 3），其输入是精简的特征向量 $\hat{\mathbf{x}} \in \mathbb{R}^{19}$，仅包含足端速度、动作标签和期望速度。门控网络输出 $K$ 个混合系数，经 softmax 归一化后，动态决定运动预测网络中各专家权重的参与比例。这种设计使网络能够根据当前的运动状态（足端速度）和控制意图（期望速度、动作标签）自适应地组合专家权重，从而在不同步态（walk, pace, trot, canter）和非周期动作（跳跃、转向）之间平滑切换，从根本上避免了传统方法（如 PFNN）因依赖单一全局相位而导致的跨步态混合伪影。

整个 pipeline 的输入-输出流如下：给定前一帧的状态 $\mathbf{x}$ 和精简输入 $\hat{\mathbf{x}}$，门控网络计算混合系数 $\omega$，运动预测网络据此组合专家权重并预测当前帧输出 $\mathbf{y}$。训练时，系统将输入 $\mathbf{X}$ 和真值输出 $\mathbf{Y}$ 按帧堆叠成矩阵，通过均方误差损失（Equation 4）联合优化运动预测网络的专家权重参数 $\beta$ 和门控网络参数 $\mu$，实现端到端学习。训练后的模型在 Intel Core i-7 CPU 上仅需约 2 ms/帧即可实时运行，内存占用约 22 MB（8 个专家权重），支持游戏手柄交互控制。

后处理阶段，系统采用 CCD 全身逆运动学（Full-body Inverse Kinematics）根据地形高度调整足端和脊柱关节，使合成运动能够适应轻微起伏的地面，同时保持脚部接触的物理合理性（Fig. 7）。

### 整体架构

MANN 由两个核心子网络构成：**运动预测网络（Motion Prediction Network, Θ）** 和 **门控网络（Gating Network, Ω）**，如图 Fig. 3 所示。门控网络根据当前运动上下文动态计算一组混合系数，用以组合多组“专家权重”（expert weights），从而实时调制运动预测网络的参数。这种设计将混合专家（MoE）的思想应用于特征级权重混合，而非传统的输出层混合。

### 运动预测网络 Θ

运动预测网络是一个三层全连接网络，以前一帧的角色状态 $\mathbf{x}$ 为输入，预测当前帧的姿态、关节及轨迹更新 $\mathbf{y}$：

$$
\Theta ( \mathbf { x } ; \pmb { \alpha } ) = \mathbf { W } _ { 2 } \mathrm { E L U } ( \mathbf { W } _ { 1 } \mathrm { E L U } ( \mathbf { W } _ { 0 } \mathbf { x } + \mathbf { b } _ { 0 } ) + \mathbf { b } _ { 1 } ) + \mathbf { b } _ { 2 }
$$

其中，$\pmb{\alpha} = \{\mathbf{W}_0, \mathbf{W}_1, \mathbf{W}_2, \mathbf{b}_0, \mathbf{b}_1, \mathbf{b}_2\}$ 表示该网络的全部可学习参数。关键之处在于，$\pmb{\alpha}$ 并非固定值，而是由 $K$ 组独立的专家权重 $\{\pmb{\alpha}_1, \dots, \pmb{\alpha}_K\}$ 通过门控网络输出的混合系数 $\omega_i$ 线性组合得到：

$$
\pmb{\alpha} = \sum_{i=1}^{K} \omega_i \, \pmb{\alpha}_i
$$

隐藏层激活函数采用指数线性单元（ELU）：

$$
\operatorname { E L U } ( x ) = \operatorname* { m a x } ( x , 0 ) + \exp ( \operatorname* { m i n } ( x , 0 ) ) - 1
$$

输入向量 $\mathbf{x} \in \mathbb{R}^n$ 包含轨迹位置/方向/速度、期望速度、动作标签，以及上一帧的关节旋转/位置/速度。特别地，运动预测网络额外接收上一帧的关节旋转作为输入，以产生更锐利的运动（Section 6.2 末句）。输出向量 $\mathbf{y} \in \mathbb{R}^m$ 预测下一帧的轨迹状态、当前帧的关节状态及根节点速度。

### 门控网络 Ω

门控网络同样为三层全连接结构，但其输入 $\hat{\mathbf{x}} \in \mathbb{R}^{19}$ 是精简后的特征向量，仅包含足端速度、当前动作标签和期望速度：

$$
\boldsymbol { \Omega } ( \hat { \mathbf { x } } ; \mu ) = \sigma ( \mathbf { W } _ { 2 } ^ { \prime } \operatorname { E L U } ( \mathbf { W } _ { 1 } ^ { \prime } \operatorname { E L U } ( \mathbf { W } _ { 0 } ^ { \prime } \hat { \mathbf { x } } + \mathbf { b } _ { 0 } ^ { \prime } ) + \mathbf { b } _ { 1 } ^ { \prime } ) + \mathbf { b } _ { 2 } ^ { \prime } )
$$

其中 $\sigma(\cdot)$ 为 softmax 归一化函数，输出 $K$ 维混合系数向量 $\pmb{\omega} = (\omega_1, \dots, \omega_K)$，满足 $\sum_i \omega_i = 1$。参数 $\mu$ 表示门控网络自身的所有权重和偏置。

### 端到端训练

整个网络以端到端方式联合优化运动预测网络的专家权重 $\pmb{\beta} = \{\pmb{\alpha}_1, \dots, \pmb{\alpha}_K\}$ 和门控网络参数 $\mu$，损失函数为均方误差：

$$
\operatorname { C o s t } ( \mathbf { X } , \mathbf { Y } ; \pmb { \beta } , \mu ) = \| \mathbf { Y } - \Theta ( \mathbf { X } , \pmb { \Omega } ( \hat { \mathbf { X } } ; \mu ) ; \pmb { \beta } ) \| _ { 2 } ^ { 2 }
$$

其中 $\mathbf{X}$ 和 $\mathbf{Y}$ 分别为所有帧的输入和输出堆叠矩阵。训练采用 AdamWR 优化器，在 GTX 970 GPU 上 4 专家约需 20 小时，8 专家约需 30 小时（Section 7）。

### 后处理模块

合成运动后，系统通过 CCD 全身逆运动学（Cyclic Coordinate Descent）对足端和脊柱关节进行后处理，根据地形高度偏移调整关节位置，使角色能够适应轻微起伏的地面（Section 8, Fig. 7）。此外，轨迹控制中引入插值公式 $T = \tau T^{*} + (1 - \tau) T^{+}$，将用户期望轨迹 $T^*$ 与网络预测修正轨迹 $T^+$ 按系数 $\tau$ 混合，以平衡控制响应速度与运动自然度（Section 8: Responsiveness）。

## 实验与关键发现

### 核心实验设计

MANN 的实验验证围绕三个核心维度展开：**运动质量**（足部滑动与关节动态性）、**路径跟随精度**（位置与角度偏差）以及**专家权重的可解释性**（消融与激活模式）。所有实验均以同一套非结构化四足动作捕捉数据为基础（约 60 分钟含镜像，类别分布见 Table 1），对比基线包括 **Vanilla NN**（三层全连接网络，无任何相位或专家机制）和 **PFNN**（Holden et al., ACM Trans. Graph. 2017，需手工标注相位参数）。

![[assets/figures/papers/paper_list_l41_https_doi_org_10_1145_3197517_3201366/figures/005_Table_1.jpg]]
*Table 1: The breakdown of our dog motion dataset for training. This dataset includes the original and mirrored unstructured dog motion capture*

训练配置方面，MANN 采用 AdamWR 优化器，在 GTX 970 GPU 上训练 4 专家约 20 小时、8 专家约 30 小时。由于 trot 和 canter 步态在数据集中极为稀缺，这两类动作被复制 11 次以提升鲁棒性——这一数据增强策略是实验公平性的一个潜在干扰因素，需在解读结果时注意。

### 运动质量：足部滑动与关节动态性

足部滑动是衡量合成运动真实感的关键指标。MANN 采用公式 $s = v ( 2 - 2 ^ { \frac { h } { H } } )$ 估算每帧足部滑动量，其中 $v$ 为足端水平速度，$h$ 为足端高度，$H = 2.5\text{ cm}$ 为高度阈值。

**Table 2** 报告了不同模型在步行（walk）模式下的平均足部滑动。MANN 在所有腿部（all legs）和后腿（back legs）两个维度上均显著优于两个基线。以 MANN4 为例，所有腿部滑动为 0.23 cm/帧，后腿仅为 0.10 cm/帧；MANN8 表现类似（0.22 / 0.09 cm/帧）。相比之下，Vanilla NN 和 PFNN 的滑动量明显更高，表明缺乏自适应模式混合的模型更容易在脚部接触阶段产生漂移伪影。

![[assets/figures/papers/paper_list_l41_https_doi_org_10_1145_3197517_3201366/figures/010_Table_2.jpg]]
*Table 2: The average foot skating for all legs and the back legs in the ground truth data, and when using the vanilla NN, PFNN and MANN models with 4 or 8 expert weights respectively*

**Table 3** 从关节角更新幅度（°/帧）的角度评估运动动态性。真实运动数据中，所有腿部关节的平均角更新为 3.71°/帧，后腿为 3.05°/帧。MANN8 在所有腿部上达到 3.69°/帧，最接近真值；MANN4 为 3.43°/帧。PFNN 和 Vanilla NN 的值则明显偏低。更大的关节角更新意味着运动更少出现“平均姿态”式的僵硬停滞，这是 MANN 通过专家权重动态混合避免跨模式错误插值的直接结果。

![[assets/figures/papers/paper_list_l41_https_doi_org_10_1145_3197517_3201366/figures/012_Table_3.jpg]]
*Table 3: The average angular update per joint along all legs and the back legs in the ground truth data, and when using the vanilla NN, PFNN and MANN models with 4 or 8 expert weights respectively*

**Figure 6** 的训练损失曲线进一步揭示了架构差异：MANN（4 和 8 专家）的收敛损失始终低于 PFNN 和 Vanilla NN，且 AdamWR 的 warm restart（第 11、31、71 轮）未对 MANN 的收敛稳定性造成显著影响，表明门控网络与运动预测网络的联合优化是稳定且有效的。

### 路径跟随精度

路径跟随实验测试了角色在四种轨迹形状（圆形、方形、星形、自定义路径）上的控制精度，指标为位置偏差（cm）和角度偏差（°）。**Table 4** 的结果显示，MANN 在所有路径形状上的两项指标均优于 Vanilla NN 和 PFNN。典型数值：圆形路径上 MANN 的位置偏差仅 2.98 cm、角度偏差 3.21°；星形路径（最复杂）上分别为 6.61 cm 和 8.76°。PFNN 在复杂路径上的偏差显著增大，这与其依赖单一相位参数进行运动插值的机制有关——当路径曲率突变时，相位对齐被破坏，导致运动预测失准。

![[assets/figures/papers/paper_list_l41_https_doi_org_10_1145_3197517_3201366/figures/011_Table_4.jpg]]
*Table 4: Average values for position and angle deviation while aiming to smoothly follow predefined trajectories of different curves, when using vanilla NN, PFNN and MANN models*

轨迹修正采用公式 $T = \tau T^{*} + (1 - \tau) T^{+}$ 将用户期望轨迹 $T^{*}$ 与网络预测修正轨迹 $T^{+}$ 混合，$\tau = 0.5$ 时在控制响应度与运动自然度之间取得平衡。**Figure 8** 定性展示了角色沿自定义路径的跟随效果，即使在急转弯处仍能保持流畅步态。

### 消融研究：专家权重的功能专门化

消融实验通过选择性屏蔽门控网络的混合系数 $\omega_i$（即将对应专家权重 $\alpha_i$ 的贡献置零）来揭示各专家的功能分化。**Table 5** 汇总了关键发现：

![[assets/figures/papers/paper_list_l41_https_doi_org_10_1145_3197517_3201366/figures/013_Table_5.jpg]]
*Table 5: Resulting motion artifacts and disablings when selectively deactivating a weight i by ignoring the corresponding blending coefficient of the αgating network. Some weights have learned features which are specifically responsible for certain motions*

- **$\alpha_1$ 屏蔽** → 跳跃动作完全失败，角色无法离地；
- **$\alpha_2$ 屏蔽** → 左转失败，角色仅能直线移动或右转；
- **$\alpha_4$ 屏蔽** → 右转失败，对称于 $\alpha_2$ 的功能；
- **$\alpha_5$ 屏蔽** → 慢跑（canter）和小跑（trot）失败，步行和踱步不受影响。

这一结果直接证实了 MANN 的核心机制：不同专家权重在无监督训练中自动专门化于特定的运动时序和模式，且这种专门化是可解释、可干预的。

**Figure 9** 的专家激活曲线提供了更细粒度的证据。在低速步行/踱步时，多个权重呈周期性交替激活，反映步态循环中的时序分工；在高速运动和跳跃时，特定权重持续高激活，表明这些专家专门负责快速动态动作的生成。这种“周期性 vs. 持续性”的激活模式是 MANN 区别于 PFNN 固定相位函数的关键优势——网络自行发现了运动的时序结构，而非依赖人工标注。

### 失败模式与局限性

尽管 MANN 在核心指标上表现优异，但其局限性同样值得关注：

1. **地形泛化能力受限**：训练数据仅在平坦地面采集，因此 MANN 无法合成涉及显著高度变化的动作（如跳上高台、从高处跃下）。虽然 CCD 全身逆运动学后处理可适应轻微起伏地形（**Figure 7**），但这仅是运动学层面的脚部位置修正，不涉及物理推离或着陆冲击的动态模拟。

2. **稀缺动作的鲁棒性依赖数据增强**：trot 和 canter 需复制 11 次才能在运行时稳定出现，说明 MANN 对数据分布仍有一定敏感性。在纯原始数据分布下，这些步态的表现可能下降。

3. **训练成本较高**：4 专家需约 20 小时、8 专家需约 30 小时（GTX 970），对于更大规模数据集或更多专家数量的扩展存在计算瓶颈。

4. **基线比较的公平性**：PFNN 需要额外的相位标注信息，但实验中未详细说明 PFNN 的调优是否充分匹配其设计需求，这可能在一定程度上影响对比结论的强度。

### 小结

MANN 在无任何步态/相位标签的条件下，通过特征级专家混合机制实现了对四足多模态运动的端到端学习。定量实验一致表明其在足部滑动抑制、关节动态性保持和路径跟随精度上均优于 Vanilla NN 和 PFNN；消融研究则从机制层面验证了专家权重的功能专门化。主要局限在于地形泛化能力和对稀缺数据的敏感性，这为后续结合物理模拟或域迁移方法留下了明确的研究空间。

## 定位与知识库关联

### 核心瓶颈与设计动机

四足动物运动控制的核心难点在于其高度多模态性——行走（walk）、踱步（pace）、小跑（trot）、慢跑（canter）等步态的脚着地模式（Fig. 2）截然不同，且步态间的转换需要精确的时序协调。传统方法在此问题上存在两个关键瓶颈：

1. **相位依赖与插值伪影**：以 **Phase-Functioned Neural Networks (PFNN)**（Holden et al., ACM Trans. Graph. 2017）为代表的基于相位函数的方法，依赖手工标注的全局相位参数来驱动运动合成。当角色在不同步态间切换时，由于各步态的相位周期和着地模式不同步，基于相位的插值容易产生混合伪影，导致运动失真。
2. **标注成本高昂**：四足动物的非结构化动作捕捉数据难以手工标注准确的步态类别和相位增量。PFNN 需要为所有运动片段标注步态标签和相位信息，这对四足动物数据而言极为费时且易出错。

MANN 的核心洞察在于：将**混合专家（Mixture of Experts, MoE）**的思想应用于特征级权重混合，而非传统的输出层混合。这一设计允许网络在无监督学习中自动为不同的运动时序、步态和非周期动作专门化控制点（expert weights），从根本上避免了跨相位的错误插值。

### 与基线方法的关键差异

与 PFNN 和 vanilla NN 相比，MANN 在三个关键维度上做出了实质性改变：

**运动插值机制**：PFNN 使用显式的相位函数，根据手工标注的相位变量在相同相位的运动间插值。MANN 则用门控网络（gating network）动态混合多组专家权重，以足端速度、动作标签和期望速度为条件，自动学习不同运动的时序和模式，无需任何相位对齐（Section 6.2, Section 10）。这一差异的本质在于：PFNN 依赖外部给定的结构化先验（相位），而 MANN 让网络从数据中自行发现运动的结构化表征。

**数据预处理需求**：PFNN 需要手动或半自动地标注所有运动片段的步态类别和相位增量。MANN 无需任何步态标签或相位标签，可直接从非结构化动作捕捉数据中端到端训练（Section 1, Section 3）。这使得 MANN 在数据获取和预处理成本上具有显著优势。

**网络输入设计**：PFNN 在输入中包含相位增量和脚步接触信息，仅将关节旋转用于输出。MANN 的门控网络接收足端速度、动作向量和期望速度（$\hat{\mathbf{x}} \in \mathbb{R}^{19}$）；运动预测网络额外输入上一帧的关节旋转，以产生更尖锐的运动响应（Section 5, Section 6.2）。

### 方法定位与适用边界

MANN 在方法谱系中处于**数据驱动运动合成**与**混合专家架构**的交汇点。其技术定位可概括为：

- **上游**：继承 PFNN 的实时角色控制框架和端到端运动预测范式，但解除了对相位先验的依赖。
- **核心创新**：将 MoE 的专家混合从输出层下沉到特征层，使网络权重本身成为可动态组合的模块，而非仅在预测结果上加权平均。
- **下游**：为后续研究开辟了无需手工标注的多模态运动合成路径，其“特征级专家混合”架构对其他高度多模态的序列建模任务具有潜在的普适性。

**适用边界**：
- 数据集仅在平坦地形上采集，因此系统无法合成跳跃至高处或从高处跳下等涉及显著高度变化的动作。
- 所采用的 CCD 全身逆运动学后处理可以适应轻微起伏地形，但无法生成涉及物理推离/着陆冲击的动态跳跃动作。
- 动作数据总量（约 60 分钟，含镜像）仍然较小，在稀疏数据区域（如跳跃仅占 0.68%，Table 1）的泛化能力可能不足。
- 部分稀有步态（trot, canter）需人工复制 11 次以增加鲁棒性，这可能引入分布偏移，在纯原始数据下的表现有待检验。

### 局限与开放问题

**已知局限**：
1. 训练时间较长——4 个专家约 20 小时，8 个专家约 30 小时（GTX 970 GPU），限制了快速迭代实验的效率。
2. 对比基线时，PFNN 需要额外的相位信息，但论文未详细说明 PFNN 的调优是否充分，比较的公平性存在一定不确定性。
3. 系统无法处理动态障碍物或显著不平地形上的物理交互，仅限于运动学层面的运动合成。

**开放问题**：
1. **域迁移能力**：MANN 能否应用于不同尺寸和形态的四足动物运动重定向，实现跨骨骼结构的运动迁移？
2. **生成质量提升**：能否结合对抗性损失（adversarial loss）来进一步减少运动模糊和避免平均姿态问题，提升合成运动的锐度和真实感？
3. **物理交互扩展**：能否利用强化学习（RL）自动生成控制信号，使 MANN 驱动的 NPC 在复杂动态环境中实现物理级交互控制？
4. **架构普适性**：MANN 的“特征级专家混合”架构是否对其他高度多模态的机器学习任务（如多风格语音合成、多模态轨迹预测）也具有普适性？

## 原文 PDF

![[paperPDFs/TOG_2018/Mode_adaptive_neural_networks_for_quadruped_motion_control.pdf]]
