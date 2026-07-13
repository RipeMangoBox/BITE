---
title: "EnvPoser: Environment-aware Realistic Human Motion Estimation from Sparse Observations with Uncertainty Modeling"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Environment_aware_Realistic_Human_Motion_Estimation_from_Sparse_Observations_with_Uncertainty_Modeling_Xia_et_al.pdf
project_link: https://xspc.github.io/EnvPoser/
code_link: null
aliases:
- EnvPoser
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 显式建模多假设运动分布的关节不确定性估计（heteroscedastic uncertainty regression + 重参数化采样）与利用环境语义/几何约束（环境点云交叉注意力 + COAP碰撞损失 + 接触概率学习）相结合，由不确定性表征多种可能，再由环境信息“筛选”出最合理的结果。
primary_logic: 关节不确定性估计可以显式捕获稀疏观测下运动估计的多假设本质；引入预扫描环境点云的语义和几何约束，能够有效减少不确定性，引导多假设估计收敛到与稀疏输入和环境上下文一致的最可信全身运动。
claims:
- 关节不确定性估计显式建模了稀疏观测导致的多假设运动分布，并与环境语义和几何约束结合，显著降低了下肢估计误差和离群值。
- 在EgoBody和GIMO数据集上，EnvPoser相比非不确定性变体（w/o UNC）将MPJRE/MPJPE误差分别降低8.11%/5.68%（EgoBody），并在GIMO上取得最低的下肢MPJPE最大值和最少的离群值。
- 环境感知精炼（语义注意力+几何碰撞）对于坐姿等复杂人-环境交互场景，能生成贴合不同物体形状的真实姿态，显著优于仅依赖稀疏信号的SOTA方法。
- EgoBody 上 MPJRE (°) = 6.00
---

# EnvPoser: Environment-aware Realistic Human Motion Estimation from Sparse Observations with Uncertainty Modeling

> [!tip] 核心洞察
> 关节不确定性估计可以显式捕获稀疏观测下运动估计的多假设本质；引入预扫描环境点云的语义和几何约束，能够有效减少不确定性，引导多假设估计收敛到与稀疏输入和环境上下文一致的最可信全身运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | EnvPoser：环境感知的基于稀疏观测与不确定性建模的真实人体运动估计 |
| 英文题名 | EnvPoser: Environment-aware Realistic Human Motion Estimation from Sparse Observations with Uncertainty Modeling |
| 会议/期刊 | CVPR 2025 |
| Links | [Project](https://xspc.github.io/EnvPoser/) · [paper](https://arxiv.org/abs/2510.12573) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | EnvPoser |
| Dataset | EgoBody, GIMO |

> [!tip] 效果简介
> - EgoBody 上，MPJRE (°) 6.00 vs 6.42 (AvatarJLM) (-0.42 (6.5% relative))；MPJPE (mm) 74.7 vs 91.7 (AvatarJLM) (-17.0 (18.5% relative))；MPJVE (mm/s) / Jitter 174.0 / 6.6 vs 177.4 / 7.2 (AvatarJLM) (-3.4 (-1.9%) / -0.6 (-8.3%))。
> - GIMO 上，MPJRE (°) 4.38 vs 4.65 (S2Fusion) (-0.27 (5.8% relative))；MPJPE (mm) 57.6 vs 57.8 (S2Fusion) (-0.2 (0.35% relative))；Jitter 8.9 vs 10.1 (S2Fusion) / 10.7 (AvatarJLM) (-1.2 (-11.9%) / -1.8 (-16.8%))。

## 概要

EnvPoser 面向一个严重欠定问题：从 VR 头显和手柄仅有的头/手三点稀疏跟踪信号恢复全身运动。同一组稀疏输入存在多种合理的全身姿态假设，尤其下肢关节缺乏直接观测，导致高度不确定性和一对多映射歧义。EnvPoser 的核心洞察是：**显式建模关节不确定性可以捕获这种多假设本质，而引入预扫描环境点云的语义与几何约束，则能有效“筛选”并引导多假设估计收敛到与环境上下文一致的最可信全身运动**。

方法上，EnvPoser 采用两阶段框架：第一阶段在 AMASS 数据集上训练不确定性感知的初始运动估计模块，通过异方差回归预测关节不确定性并采样生成多假设运动表示；第二阶段在交互数据集上联合训练环境感知精炼模块，利用运动-环境交叉注意力融合语义约束，结合 COAP 碰撞损失和接触概率学习施加几何约束，最终回归精确的全身运动。

在 EgoBody 和 GIMO 两个基准数据集上，EnvPoser 相比 SOTA 方法 **AvatarJLM** 和 **S2Fusion** 取得一致提升：EgoBody 上 MPJPE 降低 18.5%（74.7 vs 91.7 mm），GIMO 上 MPJRE 降低 5.8%（4.38° vs 4.65°）。消融实验证实，移除不确定性估计使 EgoBody 误差上升 8.11%/5.68%（MPJRE/MPJPE），而去除接触概率估计则使两个数据集的 MPJPE 分别上升 3.7% 和 3.0%，验证了各模块的关键作用。定性结果显示，EnvPoser 在坐姿等复杂人-环境交互场景中能生成贴合不同物体形状的真实姿态，并在下肢估计上取得最低的最大误差和最少的离群值。

**局限与待解决问题**：当前方法假设静态环境，未考虑动态多用户或移动物体交互；依赖预扫描点云质量，未利用原始视觉语义线索；泛化到全新环境布局的能力尚未充分验证。



从稀疏穿戴式传感器（如VR头显和手柄）仅有的头部和双手三点跟踪信号恢复全身运动，是虚拟现实、人机交互和具身智能领域的核心挑战。这一问题本质上是**严重欠定的**：同一组稀疏的三点输入，在真实物理世界中可以对应多种合理的全身姿态假设——例如，当用户端坐时，腿部可以交叉、前伸或自然下垂，而头手信号几乎完全相同。这种**一对多映射歧义**在下肢关节表现得尤为突出，因为下肢完全缺乏直接观测信号，仅能依赖运动先验进行推断，导致估计结果中误差和离群值显著偏高。

现有方法主要沿两条技术路径展开。一类方法完全忽略环境上下文，仅从稀疏信号和人体运动先验出发进行回归或生成。**AvatarPoser** 采用纯数据驱动的姿态估计，直接输出单一平均姿态，缺乏对多假设本质的显式建模。**AGRoL** 和 **AvatarJLM** 分别引入扩散模型和两阶段联合层面建模，提升了运动自然度，但依然无法区分不同环境下的合理姿态差异。另一类方法开始尝试融入环境信息，如 **S2Fusion** 利用场景几何约束侧重下肢交互，但其环境利用方式较为简单（仅足-地接触），未充分挖掘环境语义信息对全身运动的引导潜力。

更深层的瓶颈在于：现有方法普遍**缺乏对稀疏观测下多假设运动分布的显式表征能力**。当模型只能输出单一确定性姿态时，它被迫在多个合理假设之间“平均化”，导致估计结果模糊、与环境脱节，甚至出现穿透物体等物理不合理现象。这一问题在复杂人-环境交互场景（如坐姿、倚靠、上下楼梯）中尤为严重，因为此时环境对运动的约束强度急剧上升，而稀疏信号本身无法提供足够的下肢信息。

EnvPoser 的核心洞察是：**关节不确定性估计可以显式捕获稀疏观测下运动估计的多假设本质；引入预扫描环境点云的语义和几何约束，能够有效减少不确定性，引导多假设估计收敛到与稀疏输入和环境上下文一致的最可信全身运动**。这一思路将问题从“从稀疏信号猜测唯一姿态”转变为“先保留多种可能，再利用环境信息筛选最优解”，为突破现有方法的性能上限提供了新的因果路径。



## 核心方法与创新机理

### 问题瓶颈：稀疏观测下的多假设运动歧义

从VR头显和手柄仅有的头/手三点稀疏跟踪信号恢复全身运动是一个严重欠定问题。同一组稀疏输入存在多种合理的全身姿态假设，导致高度不确定性和一对多映射歧义，尤其下肢关节缺乏直接观测，误差和离群值显著。现有方法（如**AvatarPoser**、**AGRoL**、**AvatarJLM**）直接输出单一平均姿态，无法显式表征这种多假设本质。

### 关键洞察：不确定性显式建模 + 环境约束引导收敛

EnvPoser的核心洞察在于：**关节不确定性估计可以显式捕获稀疏观测下运动估计的多假设本质；引入预扫描环境点云的语义和几何约束，能够有效减少不确定性，引导多假设估计收敛到与稀疏输入和环境上下文一致的最可信全身运动。**

这一洞察通过以下四个关键changed slot实现：

#### 1. 异方差关节不确定性估计（核心创新）

**Baseline:** 无显式不确定性估计，直接输出单一平均姿态。

**EnvPoser:** 构建异方差神经网络，从Transformer提取的运动特征$Z_H$同时预测平均运动$\widetilde{\pmb{\theta}}$和关节不确定性$\pmb{\delta}$，并通过重参数化采样$\bar{\pmb{\theta}} = \widetilde{\pmb{\theta}} + \pmb{\delta} \cdot \pmb{\varepsilon}$生成多假设运动表示。训练时以不确定性损失$L_\delta = \lVert \frac{\widetilde{\pmb{\theta}} - \pmb{\theta}}{\pmb{\delta}} \rVert_2 + \log(\lVert \pmb{\delta} \rVert_2)$引导网络准确预测各关节的不确定性程度。

**因果机制:** 不确定性$\pmb{\delta}$显式编码了稀疏观测下各关节估计的置信度——下肢等缺乏直接观测的关节自然获得更高不确定性，而受跟踪信号约束的头/手关节不确定性较低。重参数化采样则在训练中模拟了多假设分布，使后续环境精炼模块能够从多种可能中筛选最优解。

**证据强度:** 消融实验（Table 3）显示，移除不确定性估计模块（EnvPoser w/o UNC）使EgoBody上MPJRE和MPJPE误差分别上升8.11%和5.68%，验证了不确定性建模对处理多假设运动的关键作用（置信度0.98）。

#### 2. 环境语义交叉注意力约束

**Baseline:** 不使用环境信息（AvatarPoser/AGRoL/AvatarJLM）或仅简单足-地接触（S2Fusion）。

**EnvPoser:** 以人体为中心裁剪1m半径内环境点云，采样$N_S=1000$点，使用PointNet++编码得到环境嵌入$Z_{env}$。运动信息嵌入$Z_M$与环境嵌入进行交叉注意力（融合空间显著性权重$\pmb{s}_{spatial}$感知距离），输出运动-环境联合表示$\pmb{Z}_{ME}$，再与$Z_M$拼接经MLP得到精炼表示$Z_{RM}$。

**因果机制:** 交叉注意力使运动特征主动“查询”环境中的相关几何/语义信息——例如坐姿时，臀部区域的特征会关注椅子表面的点云，从而将环境上下文注入运动表示。空间显著性则让模型感知人体与周围物体的距离关系，优先关注近邻交互区域。

**证据强度:** Table 2消融显示，同时结合语义和几何约束取得最优性能；仅使用语义或几何约束均导致性能下降，验证了两种环境信息的互补性（置信度0.98）。

#### 3. 接触概率学习

**Baseline:** 无接触预测，直接回归姿态。

**EnvPoser:** 从精炼表示$Z_{RM}$和扩展稀疏观测$X_{new}$预测22个关节的接触概率$\hat{C}$（BCE损失训练），拼接$Z_{RM}$和$\hat{C}$后通过两层线性层回归最终运动$\hat{\pmb{\theta}}_{RM}$。

**因果机制:** 接触概率为运动回归提供了显式的交互先验——模型不仅知道“身体在哪里”，还知道“哪些关节应该接触环境”。这在下肢接触地面、臀部接触座椅等场景中显著减少了穿透和悬空伪影。

**证据强度:** 去除接触概率估计（EnvPoser w/o Contact）导致EgoBody MPJPE上升3.7%（77.6 vs 74.7），GIMO MPJPE上升3.0%（59.4 vs 57.6），表明接触预测对精准姿态回归至关重要（置信度0.98）。

#### 4. COAP高效碰撞损失

**Baseline:** 无碰撞检测或使用计算代价高的SDF。

**EnvPoser:** 采用COAP模型高效计算人体与周围环境点的碰撞，联合足-地接触/高度/穿透损失约束几何合理性。COAP碰撞损失$L_{coap} = \frac{1}{N_S} \sum_{i=1}^{N_S} \sigma(f_{\Theta}(V_{S_i} | \mathcal{G})) \mathbb{I}_{f_{\Theta}(V_{S_i} | \mathcal{G}) > 0}$直接惩罚人体网格与环境点云的穿透。

**因果机制:** COAP提供了可微、高效的碰撞检测，使几何约束能直接参与梯度优化。与语义约束配合，语义注意力引导运动“靠近”合理交互区域，几何碰撞损失则防止“过度穿透”，两者共同确保姿态的物理合理性。

### 创新协同效应

四个changed slot形成闭环：不确定性估计生成多假设运动分布（探索空间），环境语义交叉注意力注入场景上下文（引导方向），接触概率提供显式交互先验（约束目标），COAP碰撞损失确保几何可行性（边界条件）。这一协同机制使EnvPoser在复杂人-环境交互场景（如不同形状物体的坐姿）中，能生成贴合环境且物理合理的全身运动，显著优于仅依赖稀疏信号的SOTA方法（Fig. 3定性对比，置信度0.95）。



EnvPoser 采用**两阶段流水线**（Figure 2），从 VR 头显和手柄仅有的三点稀疏跟踪信号恢复全身运动，并利用预扫描环境点云进行精炼。

![[assets/figures/papers/paper_list_l1734_Environment_aware_Realistic_Human_Motion_Estimation_from_Sparse_Observat/figures/002_Figure_2.jpg]]
*Figure 2: Overview of EnvPoser: A Two-Stage Motion Estimation Model. Stage I involves training the uncertainty-aware initial estimation K V0 00 0 0module on the AMASS dataset to produce initial motion estimates with uncertainty quantification. Stage II refines these estimates by training on motion-environment datasets, incorporating semantic and geometric environmental constraints*

### 输入与输出

- **输入**：时间窗口长度为 40 的稀疏跟踪信号 $\pmb{X} = \{\pmb{x}_t\}_{t=1}^{T} \in \mathcal{R}^{T \times N_c}$（$N_c=36$，包含头/手位置、旋转和线速度），以及以人体为中心 1 米半径内均匀采样的 $N_S=1000$ 个环境点云 $\pmb{V}_S$。
- **输出**：全身运动序列 $\hat{\pmb{\theta}}_{RM} \in \mathcal{R}^{T \times 132}$（SMPL 模型前 22 个关节的 6D 旋转表示）。

### 阶段一：不确定性感知的初始运动估计（Stage I）

该阶段在 AMASS 大规模运动捕捉数据集上预训练，仅依赖稀疏跟踪信号与历史运动信息，不引入环境约束：

1. **稀疏输入与历史运动嵌入**：将窗口内稀疏观测和历史运动通过线性层嵌入并拼接，得到浅层运动表示 $\pmb{Z}_S$。
2. **Transformer 运动特征提取**：利用含时间位置编码的 Transformer 编码器从 $\pmb{Z}_S$ 提取高维运动特征 $\pmb{Z}_H$。
3. **人体运动与关节不确定性回归**：分别通过姿态回归头和不确定性回归头从 $\pmb{Z}_H$ 预测平均运动 $\widetilde{\pmb{\theta}}$ 和关节不确定性 $\pmb{\delta}$，并通过重参数化采样 $\bar{\pmb{\theta}} = \widetilde{\pmb{\theta}} + \pmb{\delta} \cdot \pmb{\varepsilon}$（$\pmb{\varepsilon} \sim \mathcal{N}(0,1)$）生成**多假设运动表示**，显式建模稀疏观测导致的一对多映射歧义。

阶段一的训练损失为：
$$L_{S\text{-}I} = \lambda_M \lVert \widetilde{\pmb{\theta}} - \pmb{\theta} \rVert_2 + \lambda_\delta \left( \lVert \frac{\widetilde{\pmb{\theta}} - \pmb{\theta}}{\pmb{\delta}} \rVert_2 + \log(\lVert \pmb{\delta} \rVert_2) \right)$$

### 阶段二：环境感知的运动精炼（Stage II）

该阶段在 EgoBody、GIMO 等交互数据集上联合训练，将阶段一的多假设估计与预扫描环境点云融合：

4. **环境点云嵌入**：使用 PointNet++ 编码裁剪后的环境点云，得到环境嵌入 $\pmb{Z}_{env} = F_{env}(\pmb{V}_S)$。
5. **环境语义感知动作精炼**：运动信息嵌入 $\pmb{Z}_M$ 与环境嵌入 $\pmb{Z}_{env}$ 进行交叉注意力（融合空间显著性 $\pmb{s}_{spatial}$ 感知距离），生成运动-环境联合表示 $\pmb{Z}_{ME}$，再与 $\pmb{Z}_M$ 拼接经 MLP 得到精炼表示 $\pmb{Z}_{RM}$。
6. **接触概率估计**：从 $\pmb{Z}_{RM}$ 和扩展稀疏观测预测 22 个关节的接触概率 $\hat{\pmb{C}}$（BCE 损失训练）。
7. **动作解码器**：拼接 $\pmb{Z}_{RM}$ 和 $\hat{\pmb{C}}$，通过两层线性层 + ReLU 回归最终运动 $\hat{\pmb{\theta}}_{RM}$。
8. **场景几何约束**：基于 COAP 模型计算高效碰撞损失 $L_{coap}$，配合足-地接触/高度/穿透损失联合约束几何合理性。

阶段二的总损失在 $L_{S\text{-}I}$ 基础上增加最终运动损失、关节点损失、手部对齐损失及上述环境约束项。

### 核心设计逻辑

整个框架的核心在于**不确定性显式建模与环境语义/几何约束的协同**：阶段一通过异方差不确定性回归捕获稀疏观测下的多假设运动分布；阶段二利用环境点云的交叉注意力和 COAP 碰撞损失，从多种可能中“筛选”出与物理场景一致的最可信全身运动。消融实验表明，移除不确定性模块（EnvPoser w/o UNC）使 EgoBody 上 MPJRE 和 MPJPE 分别上升 8.11% 和 5.68%；仅使用语义或几何约束均导致性能下降，验证了两阶段设计的互补性。

### 补充图表

![[assets/figures/papers/paper_list_l1734_Environment_aware_Realistic_Human_Motion_Estimation_from_Sparse_Observat/figures/001_Figure_1.jpg]]
*Figure 1: EnvPoser can estimate the full-body motion using three tracking signals (HMD and hand controllers) and a pre-scanned environment mesh*



EnvPoser 采用两阶段框架解决稀疏观测下的全身运动估计问题。第一阶段在 AMASS 数据集上训练不确定性感知的初始运动估计模块，第二阶段在运动-环境交互数据集上联合训练环境感知的运动精炼模块。以下按管线顺序阐述关键模块及其核心公式。

### 3.1 问题形式化

给定稀疏跟踪信号序列 $\pmb{X} = \{ \pmb{x}_t \}_{t=1}^{T} \in \mathcal{R}^{T \times N_c}$（$N_c=36$，包含头显与手柄的位置、旋转和线速度）和预扫描的 3D 环境点云 $\pmb{S}$，目标是估计全身运动序列 $\theta = \{ \theta_t \}_{t=1}^{T} \in \mathcal{R}^{T \times 132}$，即 SMPL 模型前 22 个关节的 6D 旋转表示。

### 3.2 第一阶段：不确定性感知的初始运动估计

**稀疏输入与历史运动嵌入。** 将窗口长度为 40 的稀疏观测与历史运动通过线性层嵌入并拼接，得到浅层运动表示 $\pmb{Z}_S$。随后经含时间位置编码的 Transformer 编码器提取高维运动特征 $\pmb{Z}_H$。

**人体运动与关节不确定性回归。** 从 $\pmb{Z}_H$ 分别通过姿态回归头和不确定性回归头预测平均运动 $\widetilde{\pmb{\theta}}$ 和关节不确定性 $\pmb{\delta}$。采用异方差不确定性回归，通过重参数化采样生成多假设运动表示 $\bar{\pmb{\theta}} = \widetilde{\pmb{\theta}} + \pmb{\delta} \cdot \pmb{\varepsilon}$，其中 $\pmb{\varepsilon} \sim \mathcal{N}(0, 1)$。这一设计显式建模了稀疏观测导致的一对多映射歧义——同一组头/手信号可对应多种合理的全身姿态，尤其下肢关节缺乏直接观测。

**第一阶段损失函数。** 平均运动损失与不确定性估计损失分别为：

$$L_M = \lVert \widetilde{\pmb{\theta}} - \pmb{\theta} \rVert_2 \quad (1)$$

$$L_\delta = \lVert \frac{\widetilde{\pmb{\theta}} - \pmb{\theta}}{\pmb{\delta}} \rVert_2 + \log(\lVert \pmb{\delta} \rVert_2) \quad (2)$$

其中 $L_\delta$ 引导网络准确预测关节不确定性：第一项惩罚标准化残差，第二项防止不确定性无限膨胀。第一阶段总损失为两者的加权组合：

$$L_{S\text{-}I} = \lambda_M L_M + \lambda_\delta L_\delta \quad (3)$$

### 3.3 第二阶段：环境感知的运动精炼

**环境点云嵌入。** 以人体为中心裁剪 1m 半径内的环境点云，均匀采样 $N_S=1000$ 个点，使用 PointNet++ 编码得到环境嵌入：

$$\pmb{Z}_{env} = F_{env}(\pmb{V}_S) \quad (4)$$

**环境语义感知精炼。** 将运动信息嵌入 $\pmb{Z}_M$ 作为查询，环境嵌入 $\pmb{Z}_{env}$ 作为键和值，通过交叉注意力融合，并加入空间显著性 $\pmb{s}_{spatial}$ 感知人体-环境距离：

$$\pmb{Z}_{ME} = (Attn(\pmb{Q}, \pmb{K}) + \pmb{s}_{spatial}) \cdot \pmb{V} \quad (5)$$

随后 $\pmb{Z}_{ME}$ 与 $\pmb{Z}_M$ 拼接经 MLP 得到环境精炼的运动表示 $\pmb{Z}_{RM}$。

**接触概率估计。** 从 $\pmb{Z}_{RM}$ 和扩展稀疏观测 $\pmb{X}_{new}$ 预测 22 个关节的接触概率 $\hat{\pmb{C}}$，以二分类交叉熵训练：

$$L_{contact} = BCELoss(\hat{\pmb{C}}, \pmb{C}) \quad (6)$$

**最终运动回归。** 拼接 $\pmb{Z}_{RM}$ 与 $\hat{\pmb{C}}$，通过两层线性层 + ReLU 解码出最终运动：

$$\hat{\pmb{\theta}}_{RM} = F_{out}(concat(\pmb{Z}_{RM}, \hat{\pmb{C}})) \quad (7)$$

**场景几何约束。** 引入基于 COAP 模型的高效碰撞损失，惩罚人体与环境点的穿透：

$$L_{coap} = \frac{1}{N_S} \sum_{i=1}^{N_S} \sigma(f_{\Theta}(\pmb{V}_{S_i} | \mathcal{G})) \mathbb{I}_{f_{\Theta}(\pmb{V}_{S_i} | \mathcal{G}) > 0} \quad (9)$$

同时施加足部接触损失 $L_{fc}$、足部高度损失 $L_{gfh}$ 和地面穿透损失 $L_{gp}$，联合约束足-地交互的几何合理性（式 10）。

**第二阶段总损失。** 联合第一阶段损失、最终运动损失、关节点损失、手部对齐损失及上述所有环境约束项：

$$L_{S\text{-}II} = L_{S\text{-}I} + L_{M'} + \lambda_1 L_{posi} + \lambda_2 L_{hAL} + \lambda_3 L_{fc} + \lambda_4 L_{contact} + \lambda_5 L_{gfh} + \lambda_6 L_{gp} + \lambda_7 L_{coap} \quad (12)$$

### 设计逻辑链

整个管线的核心因果机制为：**不确定性估计显式捕获多假设运动分布 → 环境语义注意力筛选与场景上下文一致的假设 → 接触概率预测与几何碰撞约束进一步消除物理不可行的解**。移除不确定性模块（w/o UNC）导致 EgoBody 上 MPJRE/MPJPE 分别上升 8.11%/5.68%（Table 3）；去除接触概率估计（w/o Contact）使 MPJPE 上升 3.0%–3.7%（Supp. Table 2）；仅使用语义或几何约束均导致性能下降（Table 2），验证了两种环境信息的互补性。



## 实验与关键发现

### 主实验结果

EnvPoser 在 EgoBody 和 GIMO 两个主流交互数据集上与多个 SOTA 方法进行了全面对比，包括 **AvatarPoser**（仅使用三点输入的稀疏跟踪方法）、**AGRoL**（基于扩散模型）、**AvatarJLM**（两阶段联合层面建模）以及 **S2Fusion**（利用环境信息的稀疏运动生成）。所有对比方法均在相同数据集上重新训练至收敛以保证公平性（S2Fusion 因未完全开源，标记为 S2Fusion*，基于论文描述与部分开源代码复现）。

**Table 1** 展示了定量对比结果。在 EgoBody 数据集上，EnvPoser 取得了 6.00° 的 MPJRE 和 74.7 mm 的 MPJPE，相比最强基线 AvatarJLM 分别降低 6.5%（0.42°）和 18.5%（17.0 mm），提升幅度显著。在运动平滑性方面，EnvPoser 的 MPJVE 为 174.0 mm/s，Jitter 指标仅 6.6，均优于所有对比方法。在 GIMO 数据集上，EnvPoser 以 4.38° MPJRE 和 57.6 mm MPJPE 同样取得最优，Jitter 指标 8.9 相比 S2Fusion 的 10.1 和 AvatarJLM 的 10.7 分别降低 11.9% 和 16.8%。

值得注意的是，GIMO 上的 MPJPE 提升幅度（0.35%）远小于 EgoBody（18.5%）。这一差异源于 GIMO 数据集本身包含较丰富的下肢运动观测信息，使得仅依赖稀疏信号的基线方法也能取得较低误差，环境约束的边际增益相对有限。然而在下肢离群值控制方面，**Supp. Figure 2** 的下肢 MPJPE 箱线图显示 EnvPoser 在 GIMO 上取得最低的下肢 MPJPE 最大值和最少的离群值，验证了不确定性建模与环境约束在抑制极端错误预测方面的关键作用。

![[assets/figures/papers/paper_list_l1734_Environment_aware_Realistic_Human_Motion_Estimation_from_Sparse_Observat/figures/011_Figure_2.jpg]]
*Figure 2: Qualitative results of lower-body MPJPE box plot for ablation study on GIMO dataset*

**Figure 3** 和 **Supp. Figure 3** 的可视化对比进一步揭示了 EnvPoser 在复杂人-环境交互场景中的优势。在坐姿等需要精确贴合不同物体形状的场景中，基线方法常出现下肢穿透、悬空或姿态不自然的问题，而 EnvPoser 能够生成与椅子、沙发等物体表面高度一致的真实姿态。**Figure 4** 的交互细节对比同样表明，EnvPoser 在足部接触、手部交互等细粒度动作上更贴近真实人体运动。

### 消融实验

消融实验围绕三个核心模块展开：不确定性估计、环境精炼策略、以及接触概率估计。

**不确定性估计的有效性。** **Table 3** 显示，移除不确定性估计模块（EnvPoser w/o UNC）后，EgoBody 上的 MPJRE 和 MPJPE 分别上升 8.11% 和 5.68%。这一退化证实了关节不确定性建模对处理稀疏观测下多假设运动歧义的关键作用——当网络被迫输出单一平均姿态时，无法有效覆盖多种合理的全身运动假设，尤其在下肢缺乏直接观测的情况下，误差显著累积。

**环境语义与几何约束的互补性。** **Table 2** 对环境精炼模块进行了系统性消融。同时结合语义约束（交叉注意力机制）和几何约束（COAP 碰撞损失及足-地约束组）的完整 EnvPoser 取得最优性能；仅使用语义约束或仅使用几何约束均导致性能下降。这表明两类环境信息具有互补性：语义注意力引导运动估计关注与任务相关的环境区域，而几何碰撞损失确保生成姿态在物理上不与场景穿透。

**接触概率估计的贡献。** **Supp. Table 2** 显示，去除接触概率估计（EnvPoser w/o Contact）使 EgoBody MPJPE 从 74.7 mm 升至 77.6 mm（+3.7%），GIMO MPJPE 从 57.6 mm 升至 59.4 mm（+3.0%）。接触概率作为显式中间表示，为最终运动回归提供了关键的人-环境交互先验，缺失该模块后模型难以精确推断哪些关节应与环境接触，导致姿态回归精度下降。

**环境点云采样策略。** **Supp. Table 1** 和 **Supp. Figure 1** 探索了不同采样策略的影响。以人体为中心、半径 1m 的圆形采样 1000 个点云在准确性与计算效率间达到最优均衡：500 点因稀疏性导致性能下降，2000 点未带来一致提升；方形采样策略略逊于圆形采样，可能因为圆形区域更贴合人体周围的有效交互范围。

### 失败模式与局限性

尽管 EnvPoser 在定量和定性实验中均表现优异，但存在以下已知失败模式：

1. **静态环境假设失效。** 当前方法假设预扫描环境在运动序列期间保持固定不变。当场景中存在其他移动用户或动态物体时，环境点云与实际场景不再匹配，语义注意力和几何碰撞约束可能引导运动估计向错误方向收敛。这一限制在拥挤的多人交互场景中尤为突出。

2. **低质量网格引入噪声约束。** 实时应用中预扫描环境网格的质量参差不齐。当网格存在缺失、噪声或重建伪影时，基于该网格采样的环境点云和 COAP 碰撞损失可能引入不准确的几何约束，反而降低估计质量。论文未提供对噪声网格输入的鲁棒性定量分析，该点需要进一步验证。

3. **对全新环境布局的泛化未充分验证。** 模型训练依赖 AMASS 合成数据预训练及 EgoBody/GIMO 交互数据集微调。虽然两个数据集覆盖了多样的室内场景，但模型在完全未见过的环境布局（如室外场景、非标准家具形状）中的泛化能力尚未系统评估。

4. **仅依赖点云，未利用视觉线索。** 环境信息仅来自预扫描 3D 点云，未利用原始图像或视频流中的丰富语义线索（如物体类别、材质、功能区域）。在复杂遮挡场景下，纯几何点云可能无法提供足够的上下文来区分外观相似但功能不同的物体表面。

### 补充图表

![[assets/figures/papers/paper_list_l1734_Environment_aware_Realistic_Human_Motion_Estimation_from_Sparse_Observat/figures/005_Table_1.jpg]]
*Table 1: The performance comparison with SOTAs*

![[assets/figures/papers/paper_list_l1734_Environment_aware_Realistic_Human_Motion_Estimation_from_Sparse_Observat/figures/006_Table_2.jpg]]
*Table 2: The ablation study on environment refinement module*

![[assets/figures/papers/paper_list_l1734_Environment_aware_Realistic_Human_Motion_Estimation_from_Sparse_Observat/figures/007_Table_3.jpg]]
*Table 3: The effectiveness of the uncertainty estimation*

![[assets/figures/papers/paper_list_l1734_Environment_aware_Realistic_Human_Motion_Estimation_from_Sparse_Observat/figures/010_Table_2.jpg]]
*Table 2: The effectiveness of contact estimation module*

![[assets/figures/papers/paper_list_l1734_Environment_aware_Realistic_Human_Motion_Estimation_from_Sparse_Observat/figures/004_Figure_3.jpg]]
*Figure 3: Visualization of motion estimation on three test sequences from EgoBody Dataset [51]*

![[assets/figures/papers/paper_list_l1734_Environment_aware_Realistic_Human_Motion_Estimation_from_Sparse_Observat/figures/003_Figure_4.jpg]]
*Figure 4: Qualitative Comparison of Interaction Details*

![[assets/figures/papers/paper_list_l1734_Environment_aware_Realistic_Human_Motion_Estimation_from_Sparse_Observat/figures/009_Figure_1.jpg]]
*Figure 1: Environmental point cloud with different sampling strategies*

![[assets/figures/papers/paper_list_l1734_Environment_aware_Realistic_Human_Motion_Estimation_from_Sparse_Observat/figures/012_Figure_3.jpg]]
*Figure 3: Visualization of various sitting motions from EgoBody and GIMO Datasets*

![[assets/figures/papers/paper_list_l1734_Environment_aware_Realistic_Human_Motion_Estimation_from_Sparse_Observat/figures/013_Figure_4.jpg]]
*Figure 4: Visualization of full-body estimation on three test sequences from GIMO Datasets*



## 定位与知识库关联

EnvPoser 处于**稀疏跟踪信号驱动的人体运动估计**这一研究脉络中，其核心贡献在于将**异方差不确定性回归**与**环境语义/几何约束**相结合，形成“多假设生成-环境筛选”的两阶段范式。以下从基线关系、适用边界、局限性与开放问题四个维度进行定位。

### 与基线方法的关系

**仅依赖稀疏信号的 SOTA 方法。** AvatarPoser、AGRoL 与 AvatarJLM 均仅以 VR 头显与手柄的 6D 姿态及速度信号（$N_c=36$）为输入，不引入环境上下文。这些方法在严重欠定的下肢估计上普遍输出“平均姿态”，无法显式表征一对多映射带来的多假设分布。EnvPoser 在 Stage I 即通过异方差网络输出关节级不确定性 $\pmb{\delta}$，并经由重参数化采样 $\bar{\pmb{\theta}} = \widetilde{\pmb{\theta}} + \pmb{\delta} \cdot \pmb{\varepsilon}$ 生成多假设运动表示，从而在原理层面突破了确定性回归的瓶颈。定量上，EnvPoser 在 EgoBody 上相较 AvatarJLM 将 MPJPE 从 91.7 mm 降至 74.7 mm（相对下降 18.5%），在 GIMO 上将 Jitter 从 10.7 降至 8.9（相对下降 16.8%），且下肢离群值显著减少（见 Supp. Fig. 2 箱线图）。

**利用环境信息的方法。** S2Fusion 是当前唯一同时使用稀疏信号与环境几何的对比方法，但其环境利用侧重于足-地接触与下肢交互，缺乏对全身语义约束的建模。EnvPoser 的环境感知精炼模块通过三项设计实现更充分的环境融合：（1）运动-环境交叉注意力（含空间显著性 $\mathbf{s}_{spatial}$）将环境点云嵌入 $\mathbf{Z}_{env}$ 与运动表示交互，得到语义精炼表示 $\mathbf{Z}_{RM}$；（2）接触概率估计以 BCE 损失训练二分类头预测 22 个关节的接触概率 $\hat{\mathbf{C}}$，并拼接入最终回归；（3）基于 COAP 的高效碰撞损失 $L_{coap}$ 替代传统 SDF 查询，在保持几何约束的同时降低计算代价。消融实验表明，同时使用语义与几何约束取得最优性能，仅保留其一均导致 EgoBody 上 MPJPE 上升（Table 2），而去除接触估计使 EgoBody MPJPE 上升 3.7%（Supp. Table 2）。在 GIMO 上，EnvPoser 的 MPJPE（57.6 mm）与 S2Fusion（57.8 mm）基本持平，但 Jitter 显著更低（8.9 vs 10.1），且坐姿等复杂交互场景的定性结果明显更贴合不同形状的物体表面（Fig. 3, Supp. Fig. 3）。

**不确定性建模的消融证据。** 移除不确定性估计模块（EnvPoser w/o UNC）使 EgoBody 上 MPJRE 和 MPJPE 分别上升 8.11% 与 5.68%（Table 3），直接验证了显式不确定性表征对稀疏观测下多假设运动建模的关键作用。该模块的因果机制在于：不确定性估计捕获了初始运动预测的歧义范围，为后续环境精炼提供了“可调整空间”，使环境约束能够有针对性地修正高不确定度关节（通常为下肢），而非均匀地拉扯所有关节。

### 适用边界与依赖条件

EnvPoser 的有效运行依赖以下前提，超出这些条件时性能可能退化：

1. **静态环境假设。** 当前框架假设预扫描环境网格在运动序列期间保持不变，未建模多用户交互或动态物体移动。在拥挤或动态场景中，环境点云与实际几何不匹配将直接污染交叉注意力与碰撞损失，导致错误的环境引导。
2. **预扫描网格质量。** 环境约束的准确性依赖于输入点云的质量。低质量网格（如实时重建产生的噪声、孔洞）会引入虚假的语义关联与碰撞惩罚。文中未定量分析网格质量下降对性能的敏感性。
3. **点云采样策略。** 环境点云以人体为中心裁剪 1m 半径并圆形采样 1000 点。消融显示 500 点因稀疏性导致性能下降，2000 点无一致提升，方形采样略逊于圆形（Supp. Table 1）。这意味着点云密度与采样形状是需针对场景调整的超参数。
4. **训练数据分布。** Stage I 在 AMASS 上预训练，Stage II 在 EgoBody/GIMO 上微调。模型对全新环境布局（如未曾见过的家具形状、房间结构）的泛化能力未经验证，可能需要在目标场景中在线适应。
5. **仅使用点云模态。** 环境信息仅来自预扫描 3D 点云，未利用原始 RGB 图像或视频流中的纹理、光照等语义线索，在遮挡严重或细粒度交互（如手指与物体接触）场景下可能信息不足。

### 局限性与开放问题

**已明确的局限。** 除上述适用边界外，文中直接指出的局限包括：（1）静态环境假设限制动态场景应用；（2）网格质量依赖影响实时部署鲁棒性；（3）未利用原始视觉数据中的丰富语义。此外，尽管 COAP 碰撞损失比 SDF 更高效，其本身仍是对人体-环境穿透的近似建模，在复杂接触（如身体倚靠软质沙发）时可能与真实物理存在偏差。

**待探索的开放问题。**
- *动态多用户场景。* 如何将其他用户的运动作为“动态环境”融入交叉注意力机制，实现多人交互下的协同姿态估计？
- *端到端视觉-运动联合。* 能否直接从自我中心摄像头图像实时推断环境语义与接触点，减少对预扫描点云的依赖，形成“视觉-环境-运动”闭环？
- *网格质量鲁棒性。* 如何设计对噪声点云鲁棒的几何约束（如基于概率占用的碰撞损失），以适应实时重建的低质量网格？
- *新环境泛化。* 模型在未见环境布局中的迁移能力如何？是否需要测试时在线适应（如通过少量无标注交互数据微调）？
- *联合优化。* 当前不确定性估计与环境精炼是两阶段训练，能否将二者联合优化，使不确定性预测直接感知环境约束，形成端到端的“不确定性-环境”协同闭环？



## 原文 PDF

![[paperPDFs/CVPR_2025/Environment_aware_Realistic_Human_Motion_Estimation_from_Sparse_Observations_with_Uncertainty_Modeling_Xia_et_al.pdf]]
