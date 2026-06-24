---
title: "Neural State Machine for Character-Scene Interactions"
type: paper
paper_level: A
venue: TOG
year: 2019
pdf_ref: paperPDFs/TOG_2019/Neural_State_Machine_for_Character_Scene_Interactions.pdf
project_link: https://github.com/sebastianstarke/AI4Animation/tree/master/AI4Animation/SIGGRAPH_Asia_2019
aliases:
- NSM
- NSMN
- NSMCSI
tags:
- TOG_2019
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "通过门控网络根据动作标签和运动相位动态生成专家混合系数，实现动作相关权重插值；同时引入双向控制框架（自中心与目标中心推断混合）提高目标到达精度。"
primary_logic: "将动作标签和相位编码为门控网络的输入，用 Kronecker 积增强相位影响，使网络学习每种动作对应的相位轨迹和专家组合，从而在一个模型中分离并平滑过渡多种截然不同的运动；配合双向轨迹预测和体积传感器，实现对几何环境的精确适配。"
claims:
- "NSM 的门控网络根据目标动作和相位动态混合 K 个专家权重，使不同运动模式被分离，避免模糊。"
- "双向控制器预测未来轨迹在自中心和目标坐标系下，并通过距离相关权重混合，显著提高最终姿态精度。"
- "在坐、搬运等任务上，NSM 的位置误差 (PE) 和旋转误差 (RE) 远低于 PFNN、MANN 等基线，且消融实验验证了各模块的必要性。"
- "Kronecker 积调制相较于简单拼接显著提升运动细节并减少脚滑，证明相位与特征交互设计的重要性。"
---

# Neural State Machine for Character-Scene Interactions

> [!tip] 核心洞察
> 将动作标签和相位编码为门控网络的输入，用 Kronecker 积增强相位影响，使网络学习每种动作对应的相位轨迹和专家组合，从而在一个模型中分离并平滑过渡多种截然不同的运动；配合双向轨迹预测和体积传感器，实现对几何环境的精确适配。

| 字段 | 内容 |
|------|------|
| 中文题名 | 用于角色-场景交互的神经状态机 |
| 英文题名 | Neural State Machine for Character-Scene Interactions |
| 会议/期刊 | TOG 2019 |
| Links | [paper](https://doi.org/10.1145/3355089.3356505); [GitHub](https://github.com/sebastianstarke/AI4Animation/tree/master/AI4Animation/SIGGRAPH_Asia_2019) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | Neural State Machine (NSM) |
| Dataset | Sitting task – final pose precision, Carrying task – final pose precision, Responsiveness – idle to walk transition, Responsiveness – idle to run transition |

> [!tip] 效果简介
> - Sitting task – final pose precision 上，Positional Error (PE, cm) / Rotational Error (RE, deg) at hip 为 PE: 2.93, RE: 0.92，对比 PFNN: PE 8.21 / RE 2.78; MANN: PE 3.45 / RE 0.96; LSTM: PE 4.10 / RE 1.12; Auto-LSTM: PE 3.88 / RE 1.05; MLP: PE 4.28 / RE 1.45，变化 PE: -5.28 vs PFNN; RE: -1.86 vs PFNN。
> - Carrying task – final pose precision 上，Positional Error (PE, cm) / Rotational Error (RE, deg) at hand 为 PE: 3.05, RE: 1.02，对比 PFNN: PE 7.62 / RE 2.50; MANN: PE 3.84 / RE 1.15; LSTM: PE 4.15 / RE 1.23; Auto-LSTM: PE 3.92 / RE 1.09; MLP: PE 4.42 / RE 1.68，变化 PE: -4.57 vs PFNN; RE: -1.48 vs PFNN。
> - Responsiveness – idle to walk transition 上，Average response time (s) 为 1.49，对比 Lower than MLP, PFNN, MANN, LSTM, Auto-LSTM (exact values not listed)，变化 Fastest among compared methods。

## 概述

角色与3D场景进行精确、目标驱动的交互是计算机动画中长期存在的难题。此类任务不仅涉及周期性运动（如行走）与非周期性运动（如坐下）的复杂组合，还要求角色的姿态与多样化的物体几何实现高精度对齐。传统的监督学习方法，如基于固定相位函数的**PFNN**（Holden et al., ACM Trans. Graph. 2017）或模式自适应的**MANN**（Zhang et al., ACM Trans. Graph. 2018），难以在一个统一模型中有效分离这些多模态运动，常导致运动模糊、物体穿透或姿态抖动等问题。

针对上述瓶颈，本文提出**神经状态机（Neural State Machine, NSM）**，一个新颖的数据驱动框架。其核心思想是通过门控网络（Gating Network）根据动作标签和运动相位动态生成专家混合系数，使网络能够自主学习每种动作对应的相位轨迹和专家组合，从而在一个模型内分离并平滑过渡多种截然不同的运动模式。配合双向控制框架（同时从角色自身和交互目标两个坐标系预测未来轨迹并混合）和体积传感器，NSM 实现了对复杂3D几何环境的精确适配。

实验结果表明，NSM 在坐下、搬运等精确交互任务上的位置误差和旋转误差显著低于 PFNN、MANN、LSTM 等基线方法，同时响应速度最快，脚滑现象也几乎可忽略。消融实验进一步验证了双向控制器、交互/环境传感器以及 Kronecker 积相位调制等关键设计的必要性。然而，该方法对训练中未见过的、几何差异过大的物体泛化能力仍然有限，且依赖手动相位标注，这构成了其主要局限。

## 背景与动机

角色动画的核心挑战之一是生成自然、精确的目标驱动场景交互——例如角色走到椅子前坐下、搬运物体或开门。这类任务要求运动控制系统同时满足三个相互制约的条件：**周期性运动**（如行走）与**非周期性精细操作**（如伸手抓握）的无缝切换、**亚厘米级**的末端执行器姿态对齐，以及对**多样化 3D 几何体**（不同形状的椅子、桌子等）的自适应。传统动画管线依赖手工设计的状态机和运动匹配，不仅工作量巨大，且难以泛化到未见过的场景配置。

数据驱动方法为这一难题提供了新路径。早期的运动合成工作（如 Motion Matching）或基于相位函数的方法（如 **PFNN**，Holden et al., ACM Trans. Graph. 2017）在 locomotion 任务上取得了显著成功，其核心思路是使用一个外部定义的标量相位变量来索引周期运动的控制参数。然而，当任务从单纯的行走扩展到包含坐下、搬运等高度多模态的交互行为时，这些方法暴露出根本性缺陷：**单一相位曲线无法同时描述多个截然不同的运动模式**。PFNN 的固定相位函数基于足部接触设计，对于坐下这类非周期性动作缺乏明确的相位定义，导致网络被迫将所有运动模式“挤压”到同一个相空间内，产生运动模糊、穿透物体或抖动伪影（Fig. 11）。

**MANN**（Zhang et al., ACM Trans. Graph. 2018）引入了门控网络来混合多个专家权重，但其门控仅依赖运动学特征（如速度），未显式建模动作语义和相位信息，在多任务场景下仍然难以清晰分离不同运动模式。循环神经网络（LSTM）及其变体（如 **Auto-LSTM**，Li et al., 2017）虽然在序列建模上具有优势，但面对精确的空间对齐要求时，其隐式记忆机制不足以补偿几何感知的缺失。简而言之，现有方法的共同瓶颈在于：**缺乏一个统一的框架，能够同时（1）根据高层动作目标动态重组网络行为，（2）精确感知并适配 3D 场景几何，以及（3）在高精度交互任务中保持运动的平滑性和物理合理性。**

本文的动机正是填补这一空白。核心洞见在于：如果将动作标签和运动相位**显式地**编码为网络结构的一部分，让模型自主学习每种动作对应的相位轨迹和专家组合，就有可能在单一模型中分离并平滑过渡多种截然不同的运动。同时，通过在自中心坐标系和目标中心坐标系之间进行**双向轨迹预测**，并引入**体积传感器**来编码场景几何，可以大幅提升目标到达精度和几何适配能力。这一思路催生了 **Neural State Machine (NSM)**——一个能够根据高层目标指令，在复杂 3D 场景中生成精确交互行为的数据驱动框架。

## 核心创新

NSM 的核心创新在于通过**动作感知的门控相位混合**与**双向目标控制**两大机制，系统性地解决了目标驱动的精确场景交互难题。与现有方法相比，NSM 在以下五个关键维度上实现了突破性改进。

### 1. 动作感知的相位-专家联合建模

传统相位驱动方法（如 **PFNN**，Holden et al., ACM Trans. Graph. 2017）依赖固定的外部相位函数，通过单周期曲线插值一组网络权重，难以处理周期性与非周期性运动共存的复杂交互场景。NSM 的关键创新在于将**动作标签与相位信息深度融合**：门控网络（Gating Network）的输入并非简单的相位值，而是 2D 相位向量 $\mathbf{P}_i = \{ \sin(\mathbf{p}_i), \cos(\mathbf{p}_i) \}$ 与动作/目标特征子集 $\mathbf{X}_i'$ 的 **Kronecker 积**（Eq. 5）。这一设计使相位对特征空间的调制作用被显著放大，网络能够自主学习每类动作（如行走、坐下、搬运）对应的独特相位轨迹和专家激活模式。

门控网络根据当前动作标签、目标动作标签、目标距离及角度，动态输出 $K$ 个专家权重的混合系数 $\boldsymbol{\omega}$（Eq. 8），进而通过 $\boldsymbol{\alpha} = \sum_{i=1}^K \omega_i \boldsymbol{\alpha}_i$（Eq. 3）生成运动预测网络（Motion Prediction Network）的参数。这种机制使不同运动模式在专家空间中被有效分离——Fig. 7 的可视化清晰展示了各任务对应截然不同的相位周期轨迹，避免了 **PFNN** 中因跨任务运动混合导致的振动伪影和穿透问题（Fig. 11）。消融实验证实，将 Kronecker 积替换为简单拼接会导致关节角度更新量显著减少、脚滑增加（Fig. 12），验证了该交互设计对运动细节保真度的关键作用。

### 2. 双向轨迹预测与控制框架

传统方法（如 **PFNN**）仅基于自中心坐标系预测未来轨迹，当角色接近目标时缺乏对目标坐标系的直接感知，导致最终姿态对齐精度不足。NSM 引入了**双向控制器**：运动预测网络同时输出自中心坐标系下的未来轨迹 $\widetilde{\mathbf{t}}_i^p$ 和目标中心坐标系下的未来轨迹，并通过距离相关权重 $\lambda = w^{d_i^2}$ 进行混合（Section 4.2, Fig. 4）。当角色远离目标时，自中心预测主导运动方向；当角色接近目标时，目标中心预测的权重增大，使末端关节（如髋部、手部）能精确对齐目标位置和方向。

这一设计直接转化为显著的精度提升。在坐下任务中，NSM 的髋部位置误差（PE）仅为 2.93 cm，旋转误差（RE）为 0.92°，而 **PFNN** 分别为 8.21 cm 和 2.78°（Table 3）。移除双向控制器后，角色无法正确对齐目标物体，位置和旋转误差显著增加（Table 3 lower, Fig. 13 top），证实了该模块对目标到达精度的决定性贡献。

### 3. 体积几何传感器替代低保真表示

**PFNN** 等基线使用高度图或简单地形高度来表示环境几何，无法描述凹形物体或复杂障碍物。NSM 采用两类**体积传感器**（Section 4.3, Fig. 5）：围绕交互对象的 8×8×8 立方体 **Interaction Sensor** 和围绕角色的圆柱采样球 **Environment Sensor**，每个采样单元输出连续占用值 $s \in [0,1]$。这种表示能够捕获凹形几何和精细障碍物结构，使角色在接近椅子时能感知扶手、靠背等细节，在避障时能绕过凹形物体。

消融实验表明，移除 Interaction Sensor 导致角色穿透目标几何并出现不自然姿态（Table 3 lower, Fig. 13 bottom），移除 Environment Sensor 则使角色忽略障碍物、无法保持安全距离（Table 3 lower, Fig. 14），验证了体积表示对几何适配的必要性。

### 4. 面向几何泛化的逐帧数据增强

传统数据增强通常仅对运动进行镜像或小幅扰动，无法扩展模型对多样化 3D 几何的适配能力。NSM 提出**五步数据增强策略**（Section 5.2, Fig. 6）：在保持运动上下文不变的前提下，逐帧随机替换或变换 3D 几何并重新计算交互姿态。这种增强在不增加数据集规模的情况下，极大扩充了训练样本覆盖的几何形状范围，使模型能够泛化到训练集中未出现的椅子（Fig. 9），尽管对差异极大的几何仍存在失败案例（Fig. 15）。

### 5. 统一框架下的多任务运动分离

与 **MANN**（Zhang et al., ACM Trans. Graph. 2018）仅通过门控速度特征混合专家权重不同，NSM 的门控网络同时接收**动作标签、目标信息与相位**，使专家混合不仅依赖运动状态，更取决于高层任务语义。这使 NSM 能够在单一模型中同时处理行走、跑步、坐下、搬运、开门等多种截然不同的任务，并在响应速度上全面优于所有基线——从静止到行走的平均响应时间为 1.49 秒，从静止到跑步仅为 0.81 秒（Table 2），同时脚滑量在所有任务中均为最低（Fig. 10）。

## 整体框架

NSM 是一个自回归的**数据驱动框架**，旨在为虚拟角色生成目标驱动的精确场景交互动作。其核心由一个**运动预测网络** (Motion Prediction Network) 和一个**门控网络** (Gating Network) 构成（图 2）。系统以逐帧循环的方式运行：每一帧，运动预测网络接收来自上一帧的角色状态、目标信息以及场景几何编码，输出当前帧的姿态与轨迹；这些输出随后被反馈回输入端，作为下一帧的控制信号，形成闭环。

### 输入与编码器

在第 $i$ 帧，运动预测网络的输入 $\mathbf{X}_i$ 由四部分组成：

$$\mathbf{X}_i = \{ \mathbf{F}_i, \mathbf{G}_i, \mathbf{I}_i, \mathbf{E}_i \}$$

- **帧输入** $\mathbf{F}_i$：包含上一帧的关节位置 $\mathbf{j}_{i-1}^p$、旋转 $\mathbf{j}_{i-1}^r$、速度 $\mathbf{j}_{i-1}^v$，以及根轨迹的位置 $\mathbf{t}_{i-1}^p$、方向 $\mathbf{t}_{i-1}^d$ 和当前动作标签 $\mathbf{t}_{i-1}^a$。
- **目标输入** $\mathbf{G}_i$：包含目标位置 $\mathbf{g}_{i-1}^p$、方向 $\mathbf{g}_{i-1}^d$ 和目标动作标签 $\mathbf{g}_{i-1}^a$。
- **交互几何输入** $\mathbf{I}_i$：由 $8\times8\times8$ 的体素传感器（Interaction Sensor）编码目标物体的几何占用信息（图 5）。
- **环境几何输入** $\mathbf{E}_i$：由圆柱形采样球阵列（Environment Sensor）编码角色周围的场景障碍物几何信息（图 5）。

这四类输入分别通过对应的编码器 $\mathcal{F}$、$\mathcal{G}$、$\mathcal{I}$、$\mathcal{E}$ 进行特征提取，随后拼接为统一的编码表示 $\mathbf{H}(\mathbf{X}; \boldsymbol{\beta})$：

$$\mathbf{H}(\mathbf{X}; \boldsymbol{\beta}) = \{ \mathcal{F}(\mathbf{F}_i; \boldsymbol{\beta}^\mathcal{F}), \mathcal{G}(\mathbf{G}_i; \boldsymbol{\beta}^\mathcal{G}), \mathcal{I}(\mathbf{I}_i; \boldsymbol{\beta}^\mathcal{I}), \mathcal{E}(\mathbf{E}_i; \boldsymbol{\beta}^\mathcal{E}) \}$$

### 运动预测网络与专家混合

运动预测网络的核心是一个三层全连接网络，但其权重并非固定值，而是由 $K$ 组**专家权重** $\boldsymbol{\alpha}_i$ 通过门控系数 $\omega_i$ 动态混合而成：

$$\boldsymbol{\alpha} = \sum_{i=1}^K \omega_i \boldsymbol{\alpha}_i$$

整个前向计算过程为：

$$\Theta(\mathbf{X}; \boldsymbol{\alpha}, \beta) = \mathbf{W}_2 \mathrm{ELU}(\mathbf{W}_1 \mathrm{ELU}(\mathbf{W}_0 \mathbf{H}(\mathbf{X}; \beta) + \mathbf{b}_0) + \mathbf{b}_1) + \mathbf{b}_2$$

其中激活函数采用指数线性单元：

$$\mathrm{ELU}(x) = \max(x, 0) + \exp(\min(x, 0)) - 1$$

网络输出 $\mathbf{Y}_i$ 包含当前帧的关节姿态、根轨迹、未来轨迹预测（自中心坐标系与目标中心坐标系）、更新后的目标参数、接触标签以及相位增量。

### 门控网络

门控网络负责根据当前动作、目标动作以及运动相位，动态生成 $K$ 个专家的混合系数 $\boldsymbol{\omega}$。其关键设计在于将 2D 相位向量 $\mathbf{P}_i = \{ \sin(\mathbf{p}_i), \cos(\mathbf{p}_i) \}$ 与动作/目标特征子集 $\mathbf{X}_i'$ 进行 **Kronecker 积** 调制，以增强相位对门控决策的影响：

$$\hat{\mathbf{X}}_i = \mathbf{P}_i \otimes \mathbf{X}_i'$$

门控网络同样为三层全连接结构，最终通过 softmax 输出归一化的混合系数：

$$\boldsymbol{\omega} = \Omega(\hat{\mathbf{X}}; \mu) = \sigma(\mathbf{W}_2' \mathrm{ELU}(\Sigma \mathbf{W}_1' \mathrm{ELU}(\Sigma \mathbf{W}_0' \hat{\mathbf{X}} + \mathbf{b}_0') + \mathbf{b}_1') + \mathbf{b}_2')$$

这种设计使网络能够自主学习每种动作对应的相位轨迹和专家激活模式，从而在一个统一模型中分离并平滑过渡多种截然不同的运动（图 7），避免了传统方法中不同任务运动被强制混合导致的模糊和抖动伪影（图 11）。

### 训练与损失

整个系统端到端训练，损失函数为预测输出与真实值的均方误差：

$$\mathrm{Cost}(\mathbf{X}, \mathbf{Y}; \gamma, \beta, \mu) = \| \mathbf{Y} - \Theta(\mathbf{H}(\mathbf{X}; \beta), \Omega(\hat{\mathbf{X}}; \mu); \gamma) \|_2^2$$

训练数据经过几何增强处理（逐帧随机替换/变换 3D 几何并重新计算交互姿态），在保持运动上下文的同时极大扩充了可适配几何的范围，使模型能够泛化到训练中未见过的物体形状（图 9），尽管对于差异过大的几何仍存在失败风险（图 15）。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_doi_org_10_1145_3355089_3356505/figures/001_Figure_1.jpg]]
*Figure 1: A selection of results using our method to generate scene interaction behaviors*

## 核心模块与公式推导

### 整体架构

NSM 由两个核心网络构成：**运动预测网络（Motion Prediction Network）** 和 **门控网络（Gating Network）**。运动预测网络负责根据当前状态生成下一帧的角色姿态与轨迹；门控网络则根据目标动作和运动相位动态决定专家权重的混合系数，从而实时生成运动预测网络的参数。系统以自回归方式运行，将当前帧的输出反馈为下一帧的输入。

### 运动预测网络

运动预测网络由编码器模块和预测模块两部分组成。编码器模块包含四个子编码器，分别处理不同类型的输入：

**帧编码器（Frame Encoder）** 接收上一帧的角色状态：

$$\mathbf{F}_i = \{ \mathbf{j}_{i-1}^p, \mathbf{j}_{i-1}^r, \mathbf{j}_{i-1}^v, \mathbf{t}_{i-1}^p, \mathbf{t}_{i-1}^d, \mathbf{t}_{i-1}^a \}$$

其中 $\mathbf{j}^p, \mathbf{j}^r, \mathbf{j}^v$ 分别表示关节位置、旋转和速度，$\mathbf{t}^p, \mathbf{t}^d, \mathbf{t}^a$ 表示根轨迹的位置、方向和动作标签。

**目标编码器（Goal Encoder）** 接收目标相关信息：

$$\mathbf{G}_i = \{ \mathbf{g}_{i-1}^p, \mathbf{g}_{i-1}^d, \mathbf{g}_{i-1}^a \}$$

其中 $\mathbf{g}^p, \mathbf{g}^d, \mathbf{g}^a$ 分别表示目标位置、方向和目标动作标签。

**交互几何编码器（Interaction Geometry Encoder）** 和 **环境几何编码器（Environment Geometry Encoder）** 分别处理交互对象周围 $8 \times 8 \times 8$ 体积传感器和角色周围圆柱体积传感器的信息（详见 4.3 节）。

四个编码器的输出拼接为统一的编码表示：

$$\mathbf{H}(\mathbf{X}; \boldsymbol{\beta}) = \{ \mathcal{F}(\mathbf{F}_i; \boldsymbol{\beta}^\mathcal{F}), \mathcal{G}(\mathbf{G}_i; \boldsymbol{\beta}^\mathcal{G}), \mathcal{I}(\mathbf{I}_i; \boldsymbol{\beta}^\mathcal{I}), \mathcal{E}(\mathbf{E}_i; \boldsymbol{\beta}^\mathcal{E}) \}$$

预测模块是一个三层全连接网络，其权重由 $K$ 个专家权重通过门控系数动态混合生成：

$$\boldsymbol{\alpha} = \sum_{i=1}^K \omega_i \boldsymbol{\alpha}_i$$

网络的前向计算过程为：

$$\Theta(\mathbf{X}; \boldsymbol{\alpha}, \beta) = \mathbf{W}_2 \mathrm{ELU}(\mathbf{W}_1 \mathrm{ELU}(\mathbf{W}_0 \mathbf{H}(\mathbf{X}; \beta) + \mathbf{b}_0) + \mathbf{b}_1) + \mathbf{b}_2$$

其中激活函数采用指数线性单元：

$$\mathrm{ELU}(x) = \max(x, 0) + \exp(\min(x, 0)) - 1$$

网络的输出 $\mathbf{Y}_i$ 包含当前帧的预测姿态、未来轨迹（自中心与目标中心坐标系）、更新后的目标参数、接触标签及相位增量，共计 13 类变量。

### 门控网络与相位感知

门控网络的核心创新在于对运动相位的处理方式。与 PFNN 使用固定外部相位函数不同，NSM 将标量相位映射为 2D 连续表示：

$$\mathbf{P}_i = \{ \sin(\mathbf{p}_i), \cos(\mathbf{p}_i) \}$$

门控网络的输入是 2D 相位向量与动作/目标特征子集的 **Kronecker 积**，这一设计使相位与特征产生乘法交互，显著增强了相位对专家选择的影响力：

$$\hat{\mathbf{X}}_i = \mathbf{P}_i \otimes \mathbf{X}_i'$$

其中特征子集为：

$$\mathbf{X}_i' = \{ \mathbf{t}_{i-1}^a, \mathbf{g}_{i-1}^a, \delta \cdot \mathbf{g}_{i-1}^a, \boldsymbol{\theta} \cdot \mathbf{g}_{i-1}^a \}$$

包含当前动作、目标动作，以及由距离 $\delta$ 和角度 $\boldsymbol{\theta}$ 加权的目标动作，使门控网络能够根据目标远近自适应调整专家激活模式。

门控网络本身是一个三层全连接网络，输出经 softmax 归一化为 $K$ 个混合系数：

$$\boldsymbol{\omega} = \Omega(\hat{\mathbf{X}}; \mu) = \sigma(\mathbf{W}_2' \mathrm{ELU}(\Sigma \mathbf{W}_1' \mathrm{ELU}(\Sigma \mathbf{W}_0' \hat{\mathbf{X}} + \mathbf{b}_0') + \mathbf{b}_1') + \mathbf{b}_2')$$

实验中将专家数量 $K$ 设为 8 或 10。

### 双向轨迹预测

为提高目标到达精度，NSM 同时预测自中心坐标系和目标中心坐标系下的未来轨迹，并通过距离相关的指数衰减权重 $\lambda = w^{d_i^2}$ 进行混合。当角色远离目标时，自中心预测主导；接近目标时，目标中心预测权重增大，从而精确对齐最终姿态。

### 训练损失

整个系统端到端训练，损失函数为预测输出与真实值的均方误差：

$$\mathrm{Cost}(\mathbf{X}, \mathbf{Y}; \gamma, \beta, \mu) = \| \mathbf{Y} - \Theta(\mathbf{H}(\mathbf{X}; \beta), \Omega(\hat{\mathbf{X}}; \mu); \gamma) \|_2^2$$

### 消融验证的关键结论

消融实验表明（Table 3 下部，Fig. 12-14）：移除双向控制器导致角色无法正确对齐目标物体，位置和旋转误差显著增加；移除交互传感器使角色穿透目标几何并产生不自然姿态；移除环境传感器使角色忽略障碍物；将 Kronecker 积替换为简单拼接会降低运动细节并增加脚滑。这些结果确认了每个模块对系统性能的必要性。

## 实验与分析

### 1. 核心性能对比

NSM 在目标驱动的精确场景交互任务上显著优于现有基线方法，尤其在坐姿和搬运任务中表现出数量级的精度提升。**Table 3** 的上半部分与中部详细报告了坐姿任务（以髋关节为测量点）和搬运任务（以手部关节为测量点）的位置误差（PE，单位 cm）与旋转误差（RE，单位度）。

![[assets/figures/papers/paper_list_l6_https_doi_org_10_1145_3355089_3356505/figures/014_Table_3.jpg]]
*Table 3: Upper and middle parts: The average positional error (PE) and rotational error (RE) produced by different models in the sitting and carrying tasks. Lower part: The error produced by NSM when the corresponding technique is removed. 10 different character positions/rotations are initialized for each task, error is measured at the ending point of the sitting and grasping transitions on the hip and hand joints correspondingly*

在坐姿任务中，NSM 取得了 PE 2.93 cm、RE 0.92° 的成绩。相比之下，**PFNN**（Holden et al., 2017）的 PE 高达 8.21 cm，RE 为 2.78°，NSM 将位置误差降低了约 64%。**MANN**（Zhang et al., 2018）虽然表现优于 PFNN（PE 3.45 cm, RE 0.96°），但仍逊于 NSM。LSTM 及其变体 Auto-LSTM 的误差也明显更高（PE 4.10 cm 与 3.88 cm），验证了 NSM 门控架构在分离多模态运动上的独特优势。

在搬运任务中，NSM 同样保持领先（PE 3.05 cm, RE 1.02°），而 PFNN 的误差为 PE 7.62 cm、RE 2.50°。值得注意的是，MANN 的搬运误差（PE 3.84 cm）相比坐姿任务有所上升，表明其门控机制在处理涉及手部精细交互的任务时，对目标几何的适配能力弱于 NSM 的体积传感器与双向控制框架。

### 2. 响应性与运动质量

**Table 2** 展示了不同模型在动作切换时的平均响应时间。NSM 在从静止到行走的过渡中平均响应时间为 1.49 秒，从静止到跑步的过渡仅需 0.81 秒，在所有对比方法（MLP、PFNN、MANN、LSTM、Auto-LSTM）中均为最快。这表明 NSM 的门控网络能够根据目标动作标签快速切换专家权重组合，而不会像 PFNN 那样受限于固定相位函数的插值延迟。

**Fig. 10** 量化了各模型在不同任务中的脚滑漂移量。在行走和跑步等周期性运动中，NSM 与 PFNN 表现相当；但在坐姿和搬运等交互任务中，NSM 的脚滑量远低于 MANN 和 LSTM，几乎可以忽略不计。这归因于 NSM 的 Kronecker 积相位调制设计（见 **Fig. 12**），使得网络在非周期性交互中依然能保持高精度的足部接触。

### 3. 关键模块消融实验

**Table 3** 的下半部分通过逐一移除 NSM 的核心组件，验证了每个模块的必要性：

- **移除双向控制器**：位置误差和旋转误差显著增加，角色无法正确对齐目标物体。如 **Fig. 13**（上）所示，缺失双向轨迹混合的角色在椅子上出现明显错位，无法完成精确的坐姿对齐。
- **移除交互传感器（Interaction Sensor）**：角色无法感知目标物体的几何形状，导致穿透和不自然姿态。**Fig. 13**（下）中，角色臀部穿透椅子，姿态扭曲，证明 8×8×8 体积传感器对于适配多样化 3D 几何至关重要。
- **移除环境传感器（Environment Sensor）**：角色在接近目标时忽略障碍物，无法保持安全距离。**Fig. 14** 显示，缺失环境传感器的角色在走向椅子时直接穿透了椅背，产生不真实的运动轨迹。

### 4. 相位交互设计的消融

**Fig. 12** 对比了门控网络中使用 Kronecker 积与简单拼接两种相位特征融合方式的效果。实验表明，使用拼接会降低运动细节（关节角度更新量减少）并增加脚滑。Kronecker 积通过增强相位与动作/目标特征之间的二阶交互，使网络能够学习到更精细的相位轨迹与专家激活模式（如 **Fig. 7** 所示），从而在运动平滑度和细节保真度上取得明显优势。

### 5. 泛化能力与失败模式

NSM 对训练中未见过的椅子形状表现出一定的泛化能力（**Fig. 9**），能够成功执行坐姿动作。然而，当目标物体的几何形状与训练集差异过大时，系统会失败。如 **Fig. 15** 所示，对于一把与训练数据差异极大的椅子，角色的手臂无法正确放置在扶手上，臀部悬空。这一局限性源于训练数据中 3D 几何形状的有限覆盖，表明体积传感器的分辨率和训练数据的多样性是制约泛化能力的关键瓶颈。

**公平性说明**：需要指出，上述性能对比存在一定的不对称性。PFNN 最初专为 locomotion 设计，其固定相位函数假设运动具有单一周期性，这与高度多模态的交互数据存在架构上的失配，因此其较差的交互精度部分源于任务与假设的不匹配。此外，NSM 的训练数据经过了逐帧几何增强（**Fig. 6**），极大扩充了可适配几何的范围，而其他基线未使用此增强策略，这可能在一定程度上放大了 NSM 的优势。尽管如此，消融实验的结果依然强有力地证明了各模块的独立贡献。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_doi_org_10_1145_3355089_3356505/figures/006_Table_1.jpg]]
*Table 1: Action distribution of motion capture*

![[assets/figures/papers/paper_list_l6_https_doi_org_10_1145_3355089_3356505/figures/010_Table_2.jpg]]
*Table 2: The average response time in seconds produced by different models. The responsiveness from idle to walking/running is measured by the style transition time to 4 different directions (forward/backward/left/right). The responsiveness from walking/running to sitting is measured by the task accomplishing time from 10 different positions/directions within 3 meters from the chair*

![[assets/figures/papers/paper_list_l6_https_doi_org_10_1145_3355089_3356505/figures/015_Figure_12.jpg]]
*Figure 12: The resulting performance in motion detail and foot sliding when combining features with the phase by either using Kronecker product [K] or concatenation [C] as input to the gating network*

## 方法谱系与知识库定位

NSM 的核心贡献在于将**动作标签感知的门控相位调制**与**双向目标控制框架**相结合，解决了数据驱动角色动画中目标导向精确交互的瓶颈。其在方法谱系中的定位可从以下四个维度理解。

### 1. 与相位驱动方法的继承与突破

NSM 直接继承自 **PFNN**（Holden et al., ACM Trans. Graph. 2017）的相位驱动思想，但在相位处理方式上实现了根本性突破。PFNN 使用固定的外部相位函数（基于足部接触检测），通过单周期曲线插值一组网络控制点权重，其相位是预定义的标量，无法区分不同动作的运动模式。NSM 将相位扩展为 2D 向量 $\mathbf{P}_i = \{ \sin(\mathbf{p}_i), \cos(\mathbf{p}_i) \}$，并通过 Kronecker 积 $\mathbf{P}_i \otimes \mathbf{X}_i'$ 将其与动作标签、目标距离/角度等特征深度融合，使门控网络能够**自主学习每类动作的相位轨迹和专家激活模式**（Fig. 7）。这一设计的因果效应在于：不同动作（行走、跑步、坐下、搬运）在相位圆上形成截然不同的专家激活轨迹，从而在单一模型中实现多模态运动的分离，避免了 PFNN 在交互任务中出现的振动伪影和身体穿透（Fig. 11）。

### 2. 与门控专家混合方法的对比

**MANN**（Zhang et al., ACM Trans. Graph. 2018）同样采用门控网络混合专家权重，但其门控输入仅基于速度等运动特征，缺乏对目标动作和相位的显式建模。NSM 的门控网络输入 $\mathbf{X}_i' = \{ \mathbf{t}_{i-1}^a, \mathbf{g}_{i-1}^a, \delta \cdot \mathbf{g}_{i-1}^a, \boldsymbol{\theta} \cdot \mathbf{g}_{i-1}^a \}$ 显式编码了当前动作、目标动作及其空间关系，使专家混合系数 $\boldsymbol{\omega}$ 同时受运动状态和目标状态的联合约束。实验表明，MANN 在坐下任务中的位置误差（PE 3.45 cm）虽优于 PFNN（PE 8.21 cm），但仍显著高于 NSM（PE 2.93 cm），说明仅靠速度门控无法充分捕捉目标到达所需的精确姿态对齐（Table 3）。

### 3. 双向控制框架的独特贡献

现有方法（包括 PFNN、MANN）的轨迹预测仅基于角色自身坐标系（egocentric），这在目标导向任务中导致累积误差。NSM 引入双向轨迹预测：同时预测自中心坐标系下的未来轨迹（红色曲线）和目标中心坐标系下的未来轨迹（绿色曲线），并通过距离相关权重 $\lambda = w^{d_i^2}$ 进行混合。当角色接近目标时，目标中心预测的权重增大，显著提高了最终姿态的到达精度。消融实验证实，移除双向控制器后，角色无法正确对齐目标物体（Table 3 下部，Fig. 13 上部），这一定量证据表明双向控制是 NSM 精确交互的必要条件。

### 4. 环境几何表示与数据增强的推进

在环境感知方面，PFNN 仅使用地形高度图，无法描述凹形几何或复杂障碍物。NSM 引入两类体积传感器：Interaction Sensor（$8 \times 8 \times 8$ 立方体）编码交互对象的局部几何，Environment Sensor（圆柱采样球）编码角色周围场景信息，两者均输出连续占用值 $s \in [0,1]$，可描述任意形状的碰撞几何（Fig. 5）。消融实验显示，移除 Interaction Sensor 导致角色穿透物体并产生不自然姿态（Fig. 13 下部），移除 Environment Sensor 则使角色忽略障碍物（Fig. 14）。

此外，NSM 提出逐帧随机替换/变换 3D 几何的数据增强策略（Fig. 6），在保持运动上下文的同时极大扩充了可适配几何的范围。这一策略是 NSM 泛化到训练集外椅子形状的关键（Fig. 9），但公平性方面需注意：其他基线未使用此增强，可能放大 NSM 的优势。

### 5. 适用边界与局限

NSM 的适用边界受以下因素制约：

- **几何泛化上限**：训练数据仅包含有限的 3D 几何形状，对于与训练集差异过大的物体（如扶手形状、椅面高度显著不同的椅子），系统会失败——手臂无法放在扶手上，臀部悬空（Fig. 15）。这提示体积传感器的分辨率（$8 \times 8 \times 8$）可能不足以捕获细粒度几何差异。
- **目标切换的平滑性**：目标动作切换时，网络输入可能发生不连续变化，导致突然的运动；通过平滑窗口可缓解，但会增加响应延迟。
- **交互类型有限**：当前仅覆盖坐、搬运和避开障碍物，未涉及更一般的多样物体交互（如开门仅作为定性展示，Fig. 8 第四行）。
- **相位标注依赖**：所有运动都需要相位标注；自动相位标注仅对周期性运动有效，非周期运动仍需手动启发式标注，且无法处理同一动作内的多周期分量（如边走边挥剑）。

### 6. 开放问题

- **几何表示的扩展**：如何采用更高分辨率体积或预训练的 PointNet++ 结合 ShapeNet，提高对广泛 3D 形状的泛化能力？
- **多周期运动的相位建模**：如何处理不同身体部位以不同频率运动的场景（如边走边挥剑）的自动相位检测与分离？
- **数据采集的自动化**：如何联合采集运动与环境信息（如佩戴 RGBD 摄像头的动捕服），以无人工干预地丰富训练数据？
- **物理仿真中的强化学习**：如何定义适合低能量日常生活交互（如从椅子上站起）的强化学习奖励函数，以在物理仿真中复现类似效果？

## 原文 PDF

![[paperPDFs/TOG_2019/Neural_State_Machine_for_Character_Scene_Interactions.pdf]]
