---
title: Towards Balanced Multi-Modal Learning in 3D Human Pose Estimation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Towards_Balanced_Multi_Modal_Learning_in_3D_Human_Pose_Estimation.pdf
project_link: null
code_link: "https://github.com/MICLAB-BUPT/AWC"
aliases:
- BMMLSBAAWCA
- TBMML3HPE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过Shapley值与Pearson相关系数在回归场景中量化各模态贡献，并利用Fisher信息矩阵（FIM）加权对强模态施加更强的参数更新约束，在训练早期窗口内动态调节各模态的优化力度。
primary_logic: 将Shapley值贡献评估从分类扩展到回归任务，以Pearson相关系数替代交叉熵作为利润函数，避免均方误差等指标在回归中偏向输出幅度大的模态；同时提出FIM加权的自适应权重约束（AWC）损失，在训练早期窗口内对强模态施加较强正则、对弱模态施加较弱正则，不引入额外可学习参数，实现多模态均衡优化。
claims:
- 采用Pearson相关系数作为利润函数，成功将Shapley值贡献评估应用于回归任务，避免MSE/MAE导致的偏差。
- AWC损失利用FIM对角近似加权参数更新偏差，同时约束更新方向和幅度，且仅在早期学习窗口内生效。
- 在MM-Fi数据集Protocol 1（Concatenation融合）上，所提方法MPJPE达到51.16 mm，比四模态朴素联合训练（53.87 mm）降低2.71 mm，且超越其他平衡方法约5 mm。
- Shapley贡献计算的开销在各融合策略下均低于训练总时间的5.4%，验证了方法的高效性。
---

# Towards Balanced Multi-Modal Learning in 3D Human Pose Estimation

> [!tip] 核心洞察
> 将Shapley值贡献评估从分类扩展到回归任务，以Pearson相关系数替代交叉熵作为利润函数，避免均方误差等指标在回归中偏向输出幅度大的模态；同时提出FIM加权的自适应权重约束（AWC）损失，在训练早期窗口内对强模态施加较强正则、对弱模态施加较弱正则，不引入额外可学习参数，实现多模态均衡优化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向3D人体姿态估计的均衡多模态学习 |
| 英文题名 | Towards Balanced Multi-Modal Learning in 3D Human Pose Estimation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2501.05264) · [Code](https://github.com/MICLAB-BUPT/AWC) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Balanced Multi-Modal Learning with Shapley-based Assessment and Adaptive Weight Constraint (AWC) |
| Dataset | MM-Fi Protocol 1 |

> [!tip] 效果简介
> - MM-Fi Protocol 1 (Concatenation fusion) 上，MPJPE (mm) 51.16 vs 53.87 (Naive 4-modality joint training) (-2.71)。

## 概要

### 问题背景

3D人体姿态估计（3D HPE）在自动驾驶、运动分析、虚拟现实等领域具有重要应用。多模态融合——例如同时利用RGB相机、LiDAR、毫米波雷达（mmWave）和WiFi信号——理论上能够提升估计精度与鲁棒性。然而，端到端训练中普遍存在**模态不平衡**问题：强模态（如RGB、LiDAR）在训练早期迅速占据主导，压制弱模态（如mmWave、WiFi）的优化，导致弱模态预测趋于常数、方差趋近于零，几乎不对最终姿态估计产生有效贡献（见Figure 3）。现有平衡方法多针对分类任务设计，缺乏适用于回归场景的贡献评估与均衡策略。

### 核心方法

本文提出一种面向回归任务的均衡多模态学习框架，核心包含两个模块：

1. **基于Shapley值的贡献评估**：将Shapley值贡献分析从分类扩展到回归，以**Pearson相关系数**替代交叉熵作为利润函数，量化各模态在多模态融合中的边际贡献，避免均方误差（MSE）等指标偏向输出幅度大的模态。
2. **自适应权重约束（AWC）损失**：利用**Fisher信息矩阵（FIM）**对角近似加权参数更新偏差，对强模态施加较强的参数更新约束，对弱模态施加较弱的约束，同时调节更新方向与幅度。该约束仅作用于训练前K个epoch的**学习窗口**内，不引入任何额外可学习参数。

### 主要结果

在MM-Fi数据集Protocol 1（Concatenation融合策略）上，所提方法取得**MPJPE 51.16 mm**，相比四模态朴素联合训练（53.87 mm）降低2.71 mm，且超越OGM-GE、PMR、MMPareto等现有平衡方法约5 mm。Shapley贡献评分的计算开销在各融合策略下均低于训练总时间的5.4%，验证了方法的高效性。

### 方法定位

该方法属于**多模态学习中的动态平衡优化**范畴，与OGM-GE（Peng et al., CVPR 2022）的梯度调制、AGM（Li et al., ICCV 2023）的自适应梯度调节、MMPareto（Wei & Hu, ICML 2024）的帕累托前沿方法等形成对比。区别于引入单模态辅助头或额外可学习参数的方案，本文通过FIM加权的正则化损失实现无参数平衡，且专门针对回归任务设计贡献度量。

### 多模态3D人体姿态估计的兴起与挑战

3D人体姿态估计（3D HPE）是计算机视觉中的核心任务，旨在从传感器数据中恢复人体关节的三维坐标。近年来，随着感知技术的发展，研究者开始整合多种互补模态以提升估计精度和鲁棒性。如图1所示，典型的多模态3D HPE系统同时利用RGB摄像头、LiDAR、毫米波雷达（mmWave）和WiFi信号等异构数据源，期望通过模态间的信息互补克服单一传感器的固有局限——例如RGB对光照敏感、LiDAR在远距离稀疏、mmWave和WiFi虽具备穿透性和隐私保护优势但空间分辨率较低。

然而，简单地联合训练多模态模型并不能保证性能提升。**模态不平衡（modality imbalance）** 已成为多模态学习中的关键瓶颈：在端到端训练的早期阶段，信息丰富、信号质量高的“强模态”（如RGB、LiDAR）会主导优化过程，压制“弱模态”（如mmWave、WiFi）的梯度更新，导致弱模态的编码器无法学习到有效的特征表示。图3直观地揭示了这一现象——在训练过程中，mmWave和WiFi模态的关节坐标预测标准差趋近于零，意味着其输出坍缩为近乎常数的值，实质上退出了对最终姿态估计的贡献。

### 现有平衡方法的局限

针对多模态学习中的不平衡问题，学界已提出多种平衡策略。**OGM-GE**（Peng et al., CVPR 2022）通过动态梯度调制减缓强模态的学习速度；**AGM**（Li et al., ICCV 2023）进一步引入自适应梯度调节机制；**MMPareto**（Wei and Hu, ICML 2024）利用帕累托前沿和单模态辅助梯度寻找多目标最优解；**ReconBoost**（Hua et al., ICML 2024）则从Boosting视角调和模态间的竞争。然而，这些方法存在一个共同的局限性：**它们均面向分类任务设计**，其贡献评估和平衡策略深度依赖交叉熵损失等分类指标。

在3D人体姿态估计这类**回归任务**中，常用的误差指标（如均方误差MSE、平均绝对误差MAE）天然偏向输出幅度大的模态，无法公平反映各模态的真实贡献。例如，一个预测值范围在[0, 2]米内的LiDAR模态，其MSE绝对值可能远大于预测值范围在[-0.1, 0.1]米内的mmWave模态，即便后者的相对预测质量更优。这意味着，直接将分类场景下的平衡方法迁移到回归任务中，不仅贡献评估会失真，后续的梯度调制策略也会失去依据。

### 本文动机与核心思路

基于上述分析，本文的核心动机可归纳为两点：

1. **贡献评估的回归适配**：需要一种对输出尺度不敏感的利润函数，使得Shapley值等博弈论贡献评估框架能够公正地量化各模态在回归任务中的边际效用。
2. **回归场景下的均衡优化**：需要一种不依赖分类损失特性的参数更新约束机制，在训练关键窗口期内对强弱模态施加差异化正则，同时避免引入额外可学习参数增加优化负担。

为此，本文提出了一套面向回归任务的均衡多模态学习框架：以**Pearson相关系数**替代交叉熵作为Shapley值的利润函数，消除输出尺度偏差；并设计基于**Fisher信息矩阵（FIM）加权的自适应权重约束损失（AWC）**，在训练早期窗口内对强模态施加更强的参数偏离惩罚，对弱模态施加更弱的约束，从而在不增加模型参数的前提下实现多模态的均衡优化。

## 核心方法与创新机理

本文的核心创新在于将多模态平衡学习从分类任务系统性地迁移到**3D人体姿态估计这一回归任务**，并围绕该迁移设计了两个紧密耦合的模块：**基于Shapley值的回归贡献评估**和**基于Fisher信息矩阵的自适应权重约束（AWC）**。两者共同解决了端到端训练中强模态（RGB、LiDAR）压制弱模态（mmWave、WiFi）的模态不平衡问题，且整个过程不引入任何额外可学习参数。

### 1. 回归场景下的Shapley贡献量化

现有基于Shapley值的多模态贡献评估方法（如**OGM-GE**，Peng et al., CVPR 2022）依赖交叉熵作为利润函数，天然适用于分类任务。将其直接迁移到回归任务时，若使用均方误差（MSE）或平均绝对误差（MAE）作为利润函数，会因回归输出的幅值差异而产生系统性偏差——输出幅度大的模态天然获得更高的“贡献”评分。

本文的关键洞察是：**用Pearson相关系数替代交叉熵作为Shapley值的利润函数**。具体而言，利润函数定义为所有关节坐标预测值与真值之间Pearson相关系数之和：

$$s ( y , \hat { y } ) = \sum _ { i = 1 } ^ { j \times 3 } \rho ( y _ { i } , \hat { y } _ { i } )$$

其中单个关节坐标的Pearson相关系数为：

$$\rho ( y _ { i } , \hat { y } _ { i } ) = \frac { c o v ( y _ { i } , \hat { y } _ { i } ) } { \sigma _ { y _ { i } } \cdot \sigma _ { \hat { y } _ { i } } }$$

Pearson相关系数天然具有尺度不变性，不受预测值幅值大小的影响，仅度量预测与真值之间的线性相关性强度。这一选择使得Shapley值能够公平地评估不同模态对最终预测的贡献，避免了对输出幅度大的模态的偏袒。

在此基础上，Shapley贡献值的计算遵循标准公式：

$$\phi ^ { m } ( \mathcal { M } ) = \sum _ { S \subseteq \mathcal { M } \backslash \{ m \} } \frac { | S | ! ( | \mathcal { M } | - | S | - 1 ) ! } { | \mathcal { M } | ! } V ( S , m )$$

其中边际利润 $V(S, m)$ 通过将多模态模型输出分解为各模态预测的线性组合来计算：

$$\hat { y } = w ^ { R } f ^ { R } + w ^ { L } f ^ { L } + w ^ { M } f ^ { M } + w ^ { W } f ^ { W } + b$$

该分解使得每个模态子集的预测可被独立评估，从而精确量化单个模态的边际贡献。

### 2. Fisher信息矩阵加权的自适应约束（AWC）

在获得各模态的Shapley贡献评分后，本文通过K-Means聚类将模态分为**强模态集合 $\mathcal{M_S}$** 和**弱模态集合 $\mathcal{M_T}$**，并据此设计差异化正则策略。核心机制是AWC损失：

$$\mathcal { L } _ { \mathrm { A W C } } = \sum _ { m \in \mathcal { M } } \left[ \alpha _ { \mathcal { S } } \cdot \mathbf { 1 } _ { \{ m \in \mathcal { M } _ { \mathcal { S } } \} } + \alpha _ { \mathcal { T } } \cdot \mathbf { 1 } _ { \{ m \in \mathcal { M } _ { \mathcal { T } } \} } \right] \cdot \mathcal { L } _ { W } ^ { m }$$

其中 $\alpha_S > \alpha_T$，对强模态施加更强的参数更新约束，对弱模态施加较弱约束，从而**同时调控参数更新的方向和幅度**。

单个模态的约束项 $\mathcal{L}_W^m$ 基于Fisher信息矩阵（FIM）的对角近似加权参数偏离初始值的程度：

$$\mathcal { L } _ { W } ^ { m } = \sum _ { i } \frac { [ \mathcal { T } _ { D } ] _ { i i } ( \theta _ { t , i } ^ { m } - \theta _ { 0 , i } ^ { m , * } ) ^ { 2 } } { 2 }$$

其中FIM对角近似由初始参数 $\theta_0^*$ 下的梯度平方均值估计：

$$[ \mathcal { T } ] _ { i i } = \frac { 1 } { | \mathcal { D } | } \sum _ { ( x _ { n } , y _ { n } ) \in \mathcal { D } } \left( \frac { \partial \mathcal { L } ( x _ { n } , y _ { n } ; \theta _ { 0 } ^ { * } ) } { \partial \theta _ { i } } \right) ^ { 2 }$$

FIM对角元素反映了各参数对任务损失的重要性——重要参数的偏离会被施加更大的惩罚。这比简单的L2正则更精确地保护了关键知识，同时允许非关键参数灵活适应弱模态。

### 3. 仅作用于早期学习窗口

与现有方法在整个训练过程中施加平衡策略不同，本文的AWC损失**仅在训练的前K个epoch（学习窗口）内生效**。总损失函数在此阶段为：

$$\mathcal { L } _ { \mathrm { t o t a l } } = \mathcal { L } _ { \mathrm { M P J P E } } + \mathcal { L } _ { \mathrm { A W C } }$$

学习窗口结束后，AWC约束被移除，模型仅由MPJPE损失驱动继续优化。这一设计的直觉是：模态不平衡主要发生在训练早期——强模态快速拟合，弱模态的预测坍缩为近常数（如Figure 3所示，mmWave和WiFi的预测标准差趋近于零）。通过在关键窗口内“减速”强模态、“保护”弱模态，即可在后续自由训练中维持平衡。消融实验证实K=20时MPJPE达到最优的51.16 mm。

### 4. 与现有方法的本质差异

| 设计维度 | 现有方法 | 本文方法 |
|---------|---------|---------|
| 贡献评估利润函数 | 交叉熵（分类） | Pearson相关系数（回归） |
| 平衡策略 | 单一梯度调制或辅助单模态头 | FIM加权的AWC损失，同时约束更新方向和幅度 |
| 约束作用阶段 | 整个训练过程 | 仅前K个epoch（学习窗口） |
| 额外可学习参数 | 部分方法引入（如单模态头） | 无 |

与**OGM-GE**（Peng et al., CVPR 2022）仅调制梯度幅度、**PMR**依赖类原型、**MMPareto**（Wei and Hu, ICML 2024）利用帕累托前沿和单模态辅助梯度、**AGM**（Li et al., ICCV 2023）自适应梯度调制、**ReconBoost**（Hua et al., ICML 2024）基于Boosting调和等方法相比，本文的AWC机制通过FIM加权实现了更精细的参数级约束，且不引入额外可学习参数，在MM-Fi数据集上MPJPE超越其他平衡方法约5 mm，验证了设计的有效性。

本文提出一种面向3D人体姿态估计的均衡多模态学习框架，核心目标是在端到端训练中解决强模态（RGB、LiDAR）压制弱模态（mmWave、WiFi）的模态不平衡问题。框架由五个关键模块串联构成，图2给出了整体流程。

**输入层**：系统接收四种异构模态数据——RGB视频帧中提取的2D人体关节点序列 $X_R = \{p_i^{2d}\}_{i=0}^N, p_i^{2d} \in \mathbb{R}^{j \times 2}$、LiDAR点云、mmWave热图以及WiFi CSI信号。四种模态在时间维度对齐后分别送入各自的模态专用编码器。

**Modality-specific Encoders**：每个模态拥有独立的特征提取分支，将异构输入映射到统一的特征空间。编码器架构因模态而异，但输出维度保持一致，为后续融合提供标准化特征表示。

**Shapley Contribution Module**：该模块是框架的“不平衡检测器”。它基于Shapley值理论，通过遍历所有模态子集组合（$2^4-1$种）来计算每个模态的边际贡献。关键创新在于将利润函数从分类任务中的交叉熵替换为Pearson相关系数：$s(y, \hat{y}) = \sum_{i=1}^{j \times 3} \rho(y_i, \hat{y}_i)$，其中 $\rho(y_i, \hat{y}_i) = \frac{cov(y_i, \hat{y}_i)}{\sigma_{y_i} \cdot \sigma_{\hat{y}_i}}$，从而避免MSE/MAE等指标在回归任务中偏向输出幅值大的模态。计算出的Shapley分数随后通过K-Means聚类将模态划分为强模态集合 $\mathcal{M}_{\mathcal{S}}$ 和弱模态集合 $\mathcal{M}_{\mathcal{T}}$，为后续AWC损失提供调制依据。

**Multi-modal Fusion Module**：各模态编码器输出的特征在此汇聚融合。框架支持多种融合策略——简单的拼接（Concatenation）或基于注意力的融合，实验部分对不同策略进行了对比。融合后的联合特征送入最终的姿态回归头。

**Pose Regression Head**：基于融合特征预测人体 $j$ 个关节的3D坐标 $\hat{y} \in \mathbb{R}^{j \times 3}$。训练主损失采用标准MPJPE损失：$\mathcal{L}_{\mathrm{MPJPE}} = \frac{1}{j} \sum_{i=1}^{j} \Vert \hat{y}_i - y_i \Vert_2$。

**AWC Loss Module**：这是框架的“平衡调节器”，仅在训练的前 $K$ 个epoch（学习窗口）内生效。它基于Fisher信息矩阵（FIM）对角近似 $[\mathcal{T}]_{ii} = \frac{1}{|\mathcal{D}|} \sum_{(x_n, y_n) \in \mathcal{D}} (\frac{\partial \mathcal{L}(x_n, y_n; \theta_0^*)}{\partial \theta_i})^2$ 来估计各参数的重要性，然后对每个模态编码器施加权重约束：$\mathcal{L}_W^m = \sum_i \frac{[\mathcal{T}_D]_{ii} (\theta_{t,i}^m - \theta_{0,i}^{m,*})^2}{2}$。总AWC损失 $\mathcal{L}_{\mathrm{AWC}} = \sum_{m \in \mathcal{M}} [\alpha_{\mathcal{S}} \cdot \mathbf{1}_{\{m \in \mathcal{M}_{\mathcal{S}}\}} + \alpha_{\mathcal{T}} \cdot \mathbf{1}_{\{m \in \mathcal{M}_{\mathcal{T}}\}}] \cdot \mathcal{L}_W^m$ 对强模态施加较大系数 $\alpha_{\mathcal{S}}$、对弱模态施加较小系数 $\alpha_{\mathcal{T}}$，从而同时约束参数更新的方向和幅度。

**训练流程**：学习窗口内的总损失为 $\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{MPJPE}} + \mathcal{L}_{\mathrm{AWC}}$；窗口结束后，AWC损失退出，模型仅由MPJPE损失驱动完成剩余训练。整个框架不引入任何额外可学习参数，Shapley贡献评分的计算开销在不同融合策略下均低于训练总时间的5.4%。

### 整体框架

本文提出的均衡多模态学习方法由两大核心模块构成：**基于 Shapley 值的模态贡献评估模块**与**自适应权重约束（AWC）损失模块**。前者负责在回归任务中量化各模态的贡献度并检测不平衡，后者利用 Fisher 信息矩阵（FIM）在训练早期窗口内对强弱模态施加差异化的参数更新约束，从而实现多模态均衡优化。

---

### 模态贡献评估模块

#### 问题设定

给定模态集合 $\mathcal{M} = \{R, L, M, W\}$（分别对应 RGB、LiDAR、mmWave、WiFi），多模态模型的输出可分解为各单模态预测的线性组合：

$$
\hat{y} = w^R f^R + w^L f^L + w^M f^M + w^W f^W + b
$$

其中 $f^m$ 为模态 $m$ 的编码器输出经融合层后的等效单模态预测，$w^m$ 与 $b$ 为融合权重与偏置。该分解使得 Shapley 值计算能够在单模态预测层面进行。

#### Shapley 值贡献计算

对于模态 $m$，其 Shapley 贡献值 $\phi^m(\mathcal{M})$ 定义为该模态加入所有可能子集 $S \subseteq \mathcal{M} \setminus \{m\}$ 时带来的边际利润加权和：

$$
\phi^m(\mathcal{M}) = \sum_{S \subseteq \mathcal{M} \setminus \{m\}} \frac{|S|! (|\mathcal{M}| - |S| - 1)!}{|\mathcal{M}|!} V(S, m)
$$

其中 $V(S, m)$ 为利润函数，衡量子集 $S$ 加入模态 $m$ 后的性能增益。

#### 利润函数：从交叉熵到 Pearson 相关系数

现有 Shapley 贡献评估方法多用于分类任务，利润函数通常采用交叉熵。本文将其扩展到回归任务，**以 Pearson 相关系数替代交叉熵**，避免均方误差（MSE）等指标偏向输出幅度大的模态。

具体而言，利润函数定义为所有关节坐标预测值与真值的 Pearson 相关系数之和：

$$
s(y, \hat{y}) = \sum_{i=1}^{j \times 3} \rho(y_i, \hat{y}_i)
$$

其中单个关节坐标的 Pearson 相关系数为：

$$
\rho(y_i, \hat{y}_i) = \frac{cov(y_i, \hat{y}_i)}{\sigma_{y_i} \cdot \sigma_{\hat{y}_i}}
$$

该利润函数沿 batch 维度计算，度量预测与真值的线性相关性，对输出尺度不敏感，从而在回归场景下给出更公平的模态贡献评估。

#### 模态不平衡检测

获得各模态的 Shapley 贡献分数后，采用 **K-Means 聚类**（K=2）将四个模态划分为强模态集合 $\mathcal{M}_{\mathcal{S}}$ 和弱模态集合 $\mathcal{M}_{\mathcal{T}}$。该划分结果直接用于后续 AWC 损失中差异化正则化系数的分配。

---

### 自适应权重约束（AWC）损失模块

#### 设计动机

端到端训练早期，强模态（如 RGB、LiDAR）的梯度主导优化过程，导致弱模态（如 mmWave、WiFi）的编码器参数迅速偏离初始值，预测坍缩为近常数输出（见 Figure 3）。AWC 损失通过在早期学习窗口内约束参数更新，减缓强模态的学习速度，同时保护弱模态不被压制。

![[assets/figures/papers/paper_list_l1036_https_arxiv_org_abs_2501_05264/figures/003_Figure_3.jpg]]
*Figure 3: (a) Mean and (b) standard deviation of human joint coordinate predictions sampled from MM-Fi [56] during the training process. Modalities like mmWave and WiFi show near-zero standard deviations, indicating their predictions collapse to nearly constant values and contribute little to pose estimation*

#### 总损失形式

AWC 正则损失对各模态编码器施加加权约束：

$$
\mathcal{L}_{\mathrm{AWC}} = \sum_{m \in \mathcal{M}} \left[ \alpha_{\mathcal{S}} \cdot \mathbf{1}_{\{m \in \mathcal{M}_{\mathcal{S}}\}} + \alpha_{\mathcal{T}} \cdot \mathbf{1}_{\{m \in \mathcal{M}_{\mathcal{T}}\}} \right] \cdot \mathcal{L}_{W}^m
$$

其中 $\alpha_{\mathcal{S}}$ 和 $\alpha_{\mathcal{T}}$ 分别为强模态和弱模态的约束强度超参数（$\alpha_{\mathcal{S}} > \alpha_{\mathcal{T}}$），$\mathcal{L}_W^m$ 为单个模态的参数更新约束项。

#### 单模态约束项：FIM 加权

单模态约束项基于 Fisher 信息矩阵的对角近似，对参数更新方向和幅度同时进行正则化：

$$
\mathcal{L}_{W}^m = \sum_i \frac{[\mathcal{T}_D]_{ii} (\theta_{t,i}^m - \theta_{0,i}^{m,*})^2}{2}
$$

其中 $\theta_{t,i}^m$ 为模态 $m$ 编码器第 $i$ 个参数在训练步 $t$ 的值，$\theta_{0,i}^{m,*}$ 为其初始值。**核心机制**：FIM 对角元素 $[\mathcal{T}_D]_{ii}$ 度量参数 $i$ 对任务损失的重要性——重要参数偏离初始值时受到更强的约束惩罚，从而同时约束更新方向（朝向初始值）和幅度（按重要性加权）。

#### FIM 对角近似

FIM 对角元素通过在初始参数 $\theta_0^*$ 下计算任务损失梯度的平方均值来估计：

$$
[\mathcal{T}]_{ii} = \frac{1}{|\mathcal{D}|} \sum_{(x_n, y_n) \in \mathcal{D}} \left( \frac{\partial \mathcal{L}(x_n, y_n; \theta_0^*)}{\partial \theta_i} \right)^2
$$

该近似仅需一次初始梯度计算，不引入额外可学习参数，计算开销低。

#### 学习窗口机制

AWC 损失仅在训练的前 $K$ 个 epoch（学习窗口）内生效。窗口结束后，模型仅使用 MPJPE 损失进行标准训练：

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{MPJPE}} + \mathcal{L}_{\mathrm{AWC}} \quad \text{（前 } K \text{ 个 epoch）}
$$

其中 MPJPE 损失定义为：

$$
\mathcal{L}_{\mathrm{MPJPE}} = \frac{1}{j} \sum_{i=1}^{j} \Vert \hat{y}_i - y_i \Vert_2
$$

学习窗口 $K$ 与正则化系数 $\alpha_{\mathcal{S}}$、$\alpha_{\mathcal{T}}$ 为关键超参数，消融实验表明 $K=20$、$\alpha_{\mathcal{S}}=20k$、$\alpha_{\mathcal{T}}=10k$ 时在 MM-Fi Protocol 1 上取得最优 MPJPE（51.16 mm）。

![[assets/figures/papers/paper_list_l1036_https_arxiv_org_abs_2501_05264/figures/006_Figure_4.jpg]]
*Figure 4: Visualization of contribution scores calculated by our Shapley value-based contribution algorithm using attention-based fusion strategy*

## 实验与关键发现

### 主实验结果

我们在MM-Fi数据集上评估了所提方法，并与多种多模态平衡基线进行对比。**Table 1** 汇总了Protocol 1（Concatenation融合）下的主要结果。朴素四模态联合训练（Naive Joint Training）的MPJPE为53.87 mm，而我们的方法达到 **51.16 mm**，降低了2.71 mm。与其他专门设计的平衡方法相比，优势更为显著：我们的方法在MPJPE上超越 **OGM-GE**（Peng et al., CVPR 2022）、**AGM**（Li et al., ICCV 2023）、**MMPareto**（Wei & Hu, ICML 2024）等方法约5 mm，在PA-MPJPE上领先约2 mm。这表明基于Shapley贡献评估与FIM加权约束的策略在回归任务中比现有以分类为导向的平衡方法更有效。

![[assets/figures/papers/paper_list_l1036_https_arxiv_org_abs_2501_05264/figures/004_Table_1.jpg]]
*Table 1: Comparisons of our proposed method and existing balancing multi-modal learning methods on MM-Fi. - denotes the results are inapplicable. The lower is better; the best results are highlighted in bold*

**Table 3** 进一步揭示了模态不平衡的本质：单模态中，RGB（MPJPE 57.37 mm）和LiDAR（76.58 mm）远优于mmWave（165.98 mm）和WiFi（162.47 mm）。在端到端联合训练中，强模态会压制弱模态的优化，导致弱模态预测坍缩为近乎常数值（**Figure 3**，方差接近零），从而无法贡献有效信息。我们的AWC损失通过在训练早期窗口内对强模态施加更强的参数更新约束，保护了弱模态的学习过程。

定性结果（**Figure 5**）显示，与OGM-GE相比，我们的方法在多个关节位置（红色圆圈标注）上取得了更精确的预测，验证了均衡策略对最终姿态估计质量的改善。

![[assets/figures/papers/paper_list_l1036_https_arxiv_org_abs_2501_05264/figures/008_Figure_5.jpg]]
*Figure 5: Visual comparisons of 3D human pose estimation between OGM-GE and our method on MM-Fi. Red circles indicate joints where our method achieves superior results*

### 消融实验

**学习窗口长度K的敏感性。** **Figure 6** 展示了不同K值对MPJPE的影响。当K=20时，模型取得最优性能（51.16 mm）。窗口过短（K=5）时，弱模态尚未充分学习便停止约束，性能下降；窗口过长（K>30）则会过度限制强模态的优化潜力，同样导致精度损失。这一结果验证了“仅在训练早期窗口内施加约束”设计的合理性。

**AWC损失超参数。** **Table 4** 给出了正则化系数α_S（强模态约束强度）和α_T（弱模态约束强度）的消融结果。最优配置为α_S=20k、α_T=10k，此时MPJPE为51.16 mm，相比无AWC约束的朴素训练降低2.71 mm。当α_S过小或α_T过大时，强模态优化未被有效抑制，性能接近朴素训练水平；反之，若α_S过大，则会过度限制强模态，导致整体精度下降。

**计算开销分析。** **Table 2** 分解了不同融合策略下Shapley贡献评分的计算开销。在所有融合策略（Concatenation、Attention等）下，评分模块的额外开销均低于训练总时间的5.4%，验证了方法的高效性——我们无需引入额外可学习参数即可实现模态贡献评估与均衡优化。

### 失效模式与局限性

尽管方法在MM-Fi上表现优异，但存在以下已知局限：

1. **数据集泛化性未验证。** 所有实验仅基于MM-Fi数据集，该数据集包含特定的传感器布局（RGB、LiDAR、mmWave、WiFi）和室内场景。在其他环境、传感器组合或数据集上的有效性需要手动验证。
2. **模态数量扩展的挑战。** Shapley值计算需要遍历所有模态子集（2^|M|-1种组合），当模态数量超过4时，计算复杂度将显著上升。文中未提供针对大规模模态场景的近似或加速策略。
3. **FIM对角近似的时效性。** AWC损失中的Fisher信息矩阵基于初始参数θ_0*计算（公式8），在训练中后期参数发生较大变化后，该近似可能不再精确反映参数重要性，约束效果可能衰减——这也解释了为何AWC仅在早期窗口内生效。
4. **超参数依赖手动调节。** 学习窗口长度K和正则化系数α_S、α_T需针对具体任务手动调参，缺乏自动化或自适应设置机制，增加了方法在新任务上的部署成本。

![[assets/figures/papers/paper_list_l1036_https_arxiv_org_abs_2501_05264/figures/007_Table_3.jpg]]
*Table 3: Uni-modal and multi-modal performance on Protocol 1*

![[assets/figures/papers/paper_list_l1036_https_arxiv_org_abs_2501_05264/figures/010_Table_4.jpg]]
*Table 4: Ablation study on the sensitivity of AWC loss hyperparameters*

## 定位与知识库关联

### 任务背景与核心瓶颈

3D人体姿态估计（3D HPE）在端到端多模态训练中面临**模态不平衡**问题：强模态（如RGB、LiDAR）凭借高信息密度在训练早期快速收敛，其梯度主导优化过程，压制弱模态（如mmWave、WiFi）的学习，导致弱模态预测坍缩为近乎常数值，无法贡献有效表示。现有平衡方法如**OGM-GE**（Peng et al., CVPR 2022）、**AGM**（Li et al., ICCV 2023）、**MMPareto**（Wei and Hu, ICML 2024）等主要针对分类任务设计，依赖交叉熵作为贡献度量，难以直接适配回归场景——均方误差（MSE）等指标在回归中倾向于输出幅度大的模态，造成贡献评估偏差。

### 方法谱系定位

本文提出的**Balanced Multi-Modal Learning with Shapley-based Assessment and Adaptive Weight Constraint (AWC)** 在以下关键维度上区别于现有工作：

| 维度 | 现有方法 | 本文方法 |
|------|---------|---------|
| **贡献度量** | 交叉熵（分类任务） | Pearson相关系数（回归任务） |
| **平衡策略** | 单一梯度调制/辅助单模态头 | FIM加权的自适应权重约束（AWC） |
| **约束阶段** | 整个训练过程 | 仅前K个epoch（学习窗口） |
| **额外参数** | 部分方法引入单模态头等 | 不引入任何额外可学习参数 |

**与OGM-GE的关系**：OGM-GE通过动态梯度调制缓解模态间优化速度差异，但其调制策略基于分类场景的准确率差异设计，缺乏对回归任务中参数更新方向和幅度的联合约束。本文的AWC损失同时约束更新方向（通过参数偏离初始值的二次惩罚）和幅度（通过FIM对角加权），在机制上更为精细。

**与MMPareto的关系**：MMPareto利用帕累托前沿和单模态辅助梯度寻求多目标平衡，但需要为每个模态维护独立的辅助头，引入额外可学习参数。本文通过Shapley值贡献评分和FIM加权约束，在不增加参数的前提下实现平衡优化。

### 适用边界

1. **模态数量**：当前验证基于四模态（RGB、LiDAR、mmWave、WiFi）场景。Shapley值计算需遍历所有模态组合（$2^{|\mathcal{M}|}-1$种），当模态数量显著增加时，计算复杂度呈指数增长，需结合蒙特卡洛采样等近似方法。
2. **任务类型**：Pearson相关系数作为利润函数适用于输出为连续值的回归任务；对于离散输出或结构化预测任务，需重新设计利润函数。
3. **数据集依赖**：仅在MM-Fi数据集上验证，该数据集在受控室内环境采集，传感器布局固定。在室外、多遮挡或不同传感器配置下的泛化性尚不明确。
4. **训练阶段**：AWC损失仅在早期学习窗口内生效，依赖Shapley评分对模态强弱关系的准确判断。若初始评分受噪声干扰导致强弱划分错误，可能反向加剧不平衡。

### 局限与开放问题

**已知局限**（论文已指出或可从实验中推断）：
- FIM对角近似依赖于初始参数$\theta_0^*$和特定数据集分布，训练中期参数漂移后，FIM估计可能不再精确反映参数重要性。
- 学习窗口长度$K$和正则化系数$\alpha_{\mathcal{S}}$、$\alpha_{\mathcal{T}}$需手动调节，缺乏自动化设置机制（消融实验显示$K=20$、$\alpha_{\mathcal{S}}=20k$、$\alpha_{\mathcal{T}}=10k$为Protocol 1最优配置）。

**开放问题**：
1. **模态扩展性**：能否有效扩展至更多（>4）模态场景（如加入深度摄像头、惯性传感器）？Shapley值组合爆炸问题如何通过采样或近似方法缓解？
2. **利润函数最优性**：Pearson相关系数是否是最优的回归贡献度量？Spearman秩相关系数或距离相关系数等更稳健的指标能否进一步提升评估准确性？
3. **训练策略协同**：AWC损失能否与学习率调度（如余弦退火）、数据增强等策略协同，在更复杂训练范式下保持平衡效果？
4. **跨任务迁移**：在非人体姿态估计的回归任务（如深度估计、温度预测、力估计）中，该方法是否同样有效？需要哪些适配修改？
5. **自适应超参数**：能否设计基于训练动态的自适应机制（如根据Shapley评分变化率自动调整$K$和正则化系数），完全免除超参数调节？

## 原文 PDF

![[paperPDFs/CVPR_2026/Towards_Balanced_Multi_Modal_Learning_in_3D_Human_Pose_Estimation.pdf]]
