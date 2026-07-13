---
title: Landscape-Awareness for Geometric View Diffusion Model
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Landscape_Awareness_for_Geometric_View_Diffusion_Model.pdf
project_link: null
code_link: null
aliases:
- LASGTSO
- LAGVDM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 引入一个学习数据分布得分的分数网络，重塑优化景观的梯度场，将姿态更新引导至高似然区域，从而有效避开局部极小值。
primary_logic: 通过两阶段优化——先利用学习的得分模型进行全局引导，再用Zero123的MSE进行局部精炼——在不依赖大量初始化的情况下显著提高收敛稳定性和样本效率。
claims:
- Zero123 MSE损失景观中存在单一最小值、平台和多个局部极小值，导致iFusion等方法的优化过程陷入局部极小。
- 从不同初始化点出发的优化轨迹中，仅有部分能收敛到真实姿态，其余陷入局部极小。
- "两阶段优化框架在GSO数据集上相比iFusion显著提升成功率（SR@30: 0.836 vs 0.382），并在仅用2个初始化点时达到与iFusion 8个初始化点相当的召回率。"
- GSO (synthetic) 上 Success Rate @30° = 0.836
---

# Landscape-Awareness for Geometric View Diffusion Model

> [!tip] 核心洞察
> 通过两阶段优化——先利用学习的得分模型进行全局引导，再用Zero123的MSE进行局部精炼——在不依赖大量初始化的情况下显著提高收敛稳定性和样本效率。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向几何视角扩散模型的景观感知方法 |
| 英文题名 | Landscape-Awareness for Geometric View Diffusion Model |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.19865) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Landscape-Awareness Score-Guided Two-Stage Optimization |
| Dataset | GSO, CO3Dv2, HOPEv2 |

> [!tip] 效果简介
> - GSO (synthetic) 上，Success Rate @30° 0.836 vs 0.382 (iFusion) (+0.454)；Recall @30° (2 init. poses) 0.901 (R@30, 2 poses, 12.86 s) vs 0.661 (iFusion, 2 poses, 23.30 s) (+0.240 (recall) / -10.44 s (time))。
> - CO3Dv2 (scene-level) 上，Success Rate @30° 0.567 vs 0.237 (iFusion) / 0.050 (ID-Pose) (+0.330 over iFusion)。
> - HOPEv2 (real-world) 上，Success Rate @30° 0.786 vs 0.382 (iFusion) (+0.404)。

## 概要

从单张或少量图像估计物体三维姿态是视觉理解的核心问题。近年来，基于扩散模型先验的姿态反求方法——如**ID-Pose**和**iFusion**——将姿态估计转化为在Zero123扩散噪声空间中最小化均方误差（MSE）的优化问题，取得了显著进展。然而，这一范式的根本瓶颈在于**优化景观的几何性质**：Zero123 MSE损失函数构成的优化曲面普遍存在大量局部极小值和平台区域（Figure 1），导致梯度下降对初始化高度敏感。从不同起点出发的优化轨迹中，仅部分能收敛到真实姿态，其余则陷入局部极小（Figure 2）。因此，现有方法必须依赖4-8个随机初始化点的多起点采样策略来提升成功率，计算效率低且收敛稳定性不足。

本文提出**Landscape-Awareness Score-Guided Two-Stage Optimization**框架，核心洞察在于：与其被动应对恶劣的优化景观，不如主动重塑梯度场。具体而言，通过引入一个显式学习数据分布得分的**分数网络**，将姿态更新方向从MSE损失隐含的梯度替换为指向高似然区域的得分梯度，从而有效避开局部极小值。整个框架分为两阶段：（1）**得分引导阶段**，利用Langevin动力学沿学习到的得分方向进行全局姿态探索；（2）**Zero123精炼阶段**，将第一阶段输出作为初始化，通过冻结的Zero123扩散模型MSE损失进行细粒度局部优化。这一设计将全局引导与局部精化解耦，在不依赖大量初始化的情况下显著提升收敛稳定性和样本效率。

实验结果表明，该方法在多个基准上取得了一致且显著的提升：在合成数据集**GSO**上，成功率（SR@30°）从iFusion的0.382提升至0.836（Table 1）；在真实场景数据集**HOPEv2**上，SR@30°从0.382提升至0.786（Table 2）；在场景级数据集**CO3Dv2**上，SR@30°从0.237提升至0.567（Table 7）。更重要的是，本文方法仅需1-2个初始化点即可达到与iFusion 8个初始化点相当的召回率，同时推理时间从91.92秒大幅缩减至12.86秒（Table 8），展示了卓越的样本效率与计算效率。

**方法定位**：本研究属于扩散模型先验引导的姿态优化范式，与ID-Pose、iFusion构成直接竞争关系。区别于这些仅依赖单一MSE梯度的方法，本文首次从优化景观分析的视角揭示了失败的本质原因，并通过得分建模提供了系统性的解决方案。与基于密集点图的重建方法（如**DUSt3R**）和视觉几何Transformer（如**VGGT**）相比，本文方法利用生成先验而非显式几何约束，在纹理信息丰富的物体上具有互补优势。

**主要局限**：Zero123模型对某些物体的生成能力有限，多视图不一致性可能导致精炼阶段劣化；球坐标相对姿态表示对对称物体存在固有歧义（Figure 9）。未来方向包括探索更强的姿态条件扩散模型（如Zero123-XL）与得分引导框架的深度融合，以及引入显式物体坐标系以缓解对称性歧义。

### 问题背景：从扩散先验反求相机姿态

从二维图像恢复物体的三维几何与相机姿态是计算机视觉的核心问题。近年来，以 **Zero123** 为代表的视角条件扩散模型展示了强大的新视角合成能力——给定一张参考图像和一个目标相机姿态，模型能够生成对应视角下的逼真图像。这一能力催生了一类新的姿态估计范式：将姿态估计转化为逆问题，即寻找一个相机姿态，使得扩散模型在该姿态条件下生成的图像与查询图像尽可能一致。

具体而言，**ID-Pose** 和 **iFusion** 等方法将姿态估计形式化为最小化扩散噪声空间中的均方误差（MSE）。给定参考图像 $I_r$、查询图像 $I_q$ 以及一个冻结的 Zero123 扩散模型，通过梯度下降优化相对姿态 $T_{r \to q}$：

$$\hat { T } _ { r \to q } = \mathop { \mathrm { a r g m i n } } _ { T \in S E ( 3 ) } \mathcal { L } ( I _ { q } , ( I _ { r } , T ) ) + \mathcal { L } ( I _ { r } , ( I _ { q } , T ^ { - 1 } ) )$$

其中 $\mathcal{L}$ 为扩散模型预测噪声与真实噪声之间的 MSE 损失。这一框架无需显式的 3D 标注或特征匹配，仅依赖扩散模型的生成能力即可实现姿态估计。

### 核心瓶颈：MSE 损失景观的几何缺陷

然而，上述基于梯度优化的方法面临一个根本性障碍：**Zero123 的 MSE 损失函数构成的优化景观存在严重的非凸性**。论文通过对 GSO 数据集中多个物体的损失景观进行系统可视化（Figure 1），揭示了三种典型的景观形态：

1. **单一最小值**：景观呈现清晰的全局极小值，梯度下降可顺利收敛。
2. **平台区域**：沿经度方向出现大范围平坦区域，反映球坐标表示的连续对称性，梯度信号微弱甚至消失。
3. **多个局部极小值**：景观中存在两个或更多显著分离的局部极小值，梯度下降极易陷入次优解。

后两种情形在实际物体中普遍存在（见 Figure 10 的更多景观可视化），直接导致 iFusion 等方法的优化过程频繁陷入局部极小值，无法收敛到真实姿态。

这一景观缺陷在优化轨迹层面得到了进一步验证。Figure 2 展示了从四个不同初始化点（经度 0°、90°、180°、270°）出发的优化轨迹：尽管所有轨迹最终生成的图像在视觉上与查询图像相似，但仅有两条轨迹准确恢复了物体的正确外观（前白后蓝、前黄后红），另外两条则收敛到了局部极小值。Figure 11 的更多轨迹示例进一步证实，多起点中多数陷入局部极小是普遍现象，而非个别案例。

### 现有方法的应对与局限

为应对上述非凸景观带来的优化困难，现有方法（如 iFusion）普遍采用**多起点随机初始化**策略——从 4 到 8 个不同的初始姿态出发独立优化，最终选取损失最小的结果。这一策略虽然在一定程度上提高了收敛成功率，但代价高昂：

- **计算效率低**：每个初始化点需要完整执行梯度优化流程，推理时间随初始化数量线性增长。例如，iFusion 使用 8 个初始化点需耗时约 91.92 秒。
- **成功率不稳定**：即使采用多起点策略，成功率（Success Rate @30°）在 GSO 数据集上仅为 0.382，仍有大量样本无法收敛到正确姿态。
- **样本效率差**：在仅使用 2 个初始化点时，iFusion 的召回率（Recall @30°）仅为 0.661，远未达到实用水平。

### 本文动机：重塑优化景观

上述分析揭示了问题的本质：**瓶颈不在于扩散模型的表达能力，而在于 MSE 损失函数所诱导的优化景观本身存在几何缺陷**。局部极小值和平台区域是景观的固有属性，单纯增加初始化点数量只是“暴力搜索”式的权宜之计，无法从根本上解决问题。

本文的核心动机在于：**能否主动重塑优化景观，使梯度下降能够更可靠地收敛到全局最优？** 具体而言，论文提出引入一个显式学习数据分布得分的**分数网络（Score Network）**，利用其提供的梯度场引导姿态更新向高概率区域移动，从而有效避开 MSE 景观中的局部极小值陷阱。在此基础上，再结合 Zero123 的 MSE 损失进行局部精炼，形成两阶段优化框架，在显著减少初始化点需求的同时提升收敛稳定性和成功率。

## 核心方法与创新机理

### 问题诊断：Zero123 MSE 损失景观的结构性缺陷

本文的核心创新始于对现有方法失败根源的系统性诊断。以 **iFusion** 和 **ID-Pose** 为代表的梯度优化方法，将姿态估计形式化为扩散噪声空间中 MSE 损失的最小化问题。然而，这一看似自然的优化目标在几何上存在严重缺陷。

Figure 1 可视化了不同物体的三维 MSE 损失景观，揭示了三种典型地形：(a) 存在单一清晰最小值的理想情况；(b) 沿经度方向出现连续平台，反映球坐标表示的对称性；(c) 包含两个截然不同的局部极小值。在 (b) 和 (c) 两种情形下，基于梯度下降的优化过程极易陷入局部极小或停滞于平台区域，无法收敛到全局最优解。

Figure 2 进一步从优化轨迹角度验证了这一诊断。从四个不同初始经度（0°、90°、180°、270°）出发的轨迹中，仅有两组成功收敛到真实姿态，其余两组陷入局部极小。尽管所有轨迹在时间步 T 生成的图像在视觉上与查询图相似，但只有正确收敛的轨迹能准确再现物体的真实外观（前白后蓝、前黄后红）。这说明 **MSE 损失景观的局部极小值与感知上合理的错误解相对应**，仅凭视觉相似性无法区分收敛质量。

### 核心操作杆：学习得分函数重塑优化景观

针对上述瓶颈，本文的核心创新在于引入一个**显式学习的得分网络（Score Network）**，从根本上改变优化的梯度信息来源。

现有方法（iFusion、ID-Pose）的梯度完全由 Zero123 去噪 MSE 损失对姿态的隐式微分提供，这一梯度场在损失景观的局部极小和平台区域近乎为零或指向错误方向。本文提出的得分网络则直接学习数据分布的条件得分 $\nabla_{\tilde{\mathbf{x}}} \log p(\tilde{\mathbf{x}} \mid \mathbf{y})$，即姿态在高概率区域的方向导数。

Figure 4 的玩具示例直观展示了这一差异：(b) 为 Oracle 得分场，(c) 为本文得分模型预测的得分场，两者高度一致；(d) 为从 Zero123 MSE 损失反传得到的得分场，其向量场在远离真实姿态的区域杂乱无章；(f) 和 (g) 分别展示了 Zero123 MSE 和本文能量模型的概率景观，其中 Zero123 的概率密度呈现双峰分布，而得分建模能够更精确地捕捉数据分布的结构。

得分网络的架构设计（Figure 3a）采用 ResNet-50 编码器提取参考图像和查询图像的视觉特征，将含噪姿态通过正弦位置编码后与图像特征拼接，送入 MLP 预测得分向量。训练使用简化的去噪得分匹配损失（Eq. 3），在低维姿态空间中采用均匀噪声采样和固定噪声尺度 $\sigma=1$，避免了高维数据上复杂的噪声调度。

### 两阶段优化框架：全局引导与局部精炼的协同

本文提出的 **Landscape-Awareness Score-Guided Two-Stage Optimization** 框架将优化过程分解为两个互补阶段，这是方法层面的核心 changed slot。

**第一阶段——得分引导的姿态更新**，采用 Langevin 动力学形式的迭代更新：

$$\tilde{\mathbf{x}}_t = \tilde{\mathbf{x}}_{t-1} + \alpha s_\theta(\tilde{\mathbf{x}}_{t-1}, \mathbf{y}) + G\mathbf{z}_t, \quad \mathbf{z}_t \sim \mathcal{N}(0, \mathbf{I}_3)$$

其中 $\alpha$ 为步长，$G$ 控制高斯噪声的幅度。该更新具有两个关键性质：(1) 期望姿态误差呈指数衰减，$\|\mathbb{E}[\tilde{\mathbf{x}}_t - \mathbf{x}_{\mathrm{gt}}]\| = M(1-\alpha)^t$；(2) 预测方差近似为 $G^2/(2\alpha)$。噪声项 $G\mathbf{z}_t$ 赋予优化过程随机探索能力，使其能够逃离局部极小，而得分项 $s_\theta$ 提供指向高概率区域的确定性引导。

**第二阶段——Zero123 精炼**，将第一阶段输出的姿态作为初始化，利用冻结的 Zero123 扩散模型作为能量函数，通过最小化去噪 MSE 损失进行细粒度优化。这一阶段继承了 Zero123 在局部区域的精确梯度信息，但受益于第一阶段提供的优质初始化，避免了对多起点随机采样的依赖。

### 初始化效率的结构性提升

两阶段设计带来的最显著 changed slot 是**初始化需求的大幅降低**。iFusion 通常需要 4–8 个随机初始化点以覆盖不同的吸引盆，而本文方法仅需 1–2 个初始化点即可达到相当或更优的性能。

Table 8 的对比数据极具说服力：在仅使用 2 个初始化点时，本文方法达到 R@30 = 0.901，推理时间 12.86 秒；iFusion 在 2 个初始化点下仅为 0.661（23.30 秒），即使将初始化点增至 8 个（91.92 秒），其性能提升仍有限。Figure 6 进一步展示了不同初始化点数量下的召回率曲线，本文框架在极少样本下即达到饱和性能，而 iFusion 需要更多样本才能逼近。

### 多视图全局一致性扩展

对于多视图场景，本文进一步引入全局一致性优化模块（Eq. 6）。第一阶段利用得分网络推断所有成对相对姿态 $\mathcal{T} = \{T_{ij}\}_{i \neq j}$，随后通过全局优化获得一致的绝对姿态集 $\overline{\mathcal{T}} = \{\overline{T}_i\}_{i=1}^N$。这一设计将两阶段优化的优势从双视图扩展到多视图联合推理，增强了场景级姿态估计的鲁棒性。

### 与竞争方法的本质差异

相较于直接竞争的 **iFusion** 和 **ID-Pose**，本文方法的本质差异不在于优化目标的形式（均使用 Zero123 的 MSE 损失），而在于**优化过程的引导机制**。iFusion/ID-Pose 完全依赖 MSE 损失的隐式梯度，其优化轨迹受限于损失景观的几何结构；本文方法通过显式学习的得分函数注入数据分布的先验知识，使优化过程具备“景观感知”能力——在远离真实解时由得分引导方向，在接近真实解时由 MSE 梯度精细调整。Table 5 的消融实验直接验证了这一差异：在相同 GSO 10 对象子集上，得分建模的 R@15 达到 0.963，显著优于能量建模的 0.850。

本文提出**Landscape-Awareness Score-Guided Two-Stage Optimization**框架，其核心动机源于对Zero123 MSE损失景观的系统分析：该景观中普遍存在单一最小值、平台区域和多个局部极小值（Figure 1），导致iFusion等基于纯梯度下降的方法极易陷入局部最优，必须依赖多起点随机初始化才能收敛到全局最优。

为重塑这一优化景观，框架将姿态估计分解为两个互补阶段：

**第一阶段：得分引导的全局探索。** 该阶段使用一个显式学习的得分网络（Score Network）来估计姿态数据分布的得分函数，并通过Langevin动力学进行迭代更新：

$$\tilde { \mathbf { x } } _ { t } = \tilde { \mathbf { x } } _ { t - 1 } + \alpha s _ { \theta } ( \tilde { \mathbf { x } } _ { t - 1 } , \mathbf { y } ) + G \mathbf { z } _ { t } , \quad \mathbf { z } _ { t } \sim \mathcal { N } ( 0 , \mathbf { I } _ { 3 } )$$

其中得分网络 $s_\theta$ 以参考图像 $I_r$、查询图像 $I_q$ 和当前含噪姿态 $\tilde{\mathbf{x}}$ 为输入，输出指向高概率区域的梯度方向。高斯噪声项 $G\mathbf{z}_t$ 提供随机探索能力，帮助轨迹跳出局部极小值。理论分析表明，姿态误差的期望呈指数衰减：$\| \mathbb { E } [ \tilde { \mathbf { x } } _ { t } - \mathbf { x } _ { \mathrm { g t } } ] \| = M ( 1 - \alpha ) ^ { t }$（Eq. 5）。

得分网络的结构如Figure 3(a)所示：使用ResNet-50编码器提取图像特征，含噪姿态通过正弦位置编码后与图像特征拼接，经MLP预测得分向量。训练采用简化的去噪得分匹配损失（Eq. 3），在低维姿态空间中以固定噪声尺度 $\sigma=1$ 和均匀噪声采样进行。

**第二阶段：Zero123能量精炼。** 第一阶段将姿态引导至真实值附近后，切换至冻结的Zero123扩散模型作为能量函数，通过最小化去噪MSE损失进行细粒度优化：

$$\hat { T } _ { r \to q } = \mathop { \mathrm { a r g m i n } } _ { T \in S E ( 3 ) } \mathcal { L } ( I _ { q } , ( I _ { r } , T ) ) + \mathcal { L } ( I _ { r } , ( I _ { q } , T ^ { - 1 } ) )$$

该阶段沿用iFusion的梯度优化范式，但受益于第一阶段提供的优质初始化，无需多起点搜索即可稳定收敛。

**多视图扩展。** 对于 $N$ 张图像的多视图场景，第一阶段先推断所有成对相对姿态 $\mathcal{T} = \{T_{ij}\}_{i \neq j}$，再通过全局优化获得一致的绝对姿态 $\overline{\mathcal{T}} = \{\overline{T}_i\}_{i=1}^N$，最终在全局能量约束下联合优化：

$$\hat { \mathcal { T } } = \underset { \{ T _ { 1 } , \ldots , T _ { n } \} \subset S E ( 3 ) } { \arg \operatorname* { m i n } } \sum _ { i = 1 } ^ { N } \sum _ { j \neq i } \mathcal { L } \big ( I ^ { ( j ) } , ( I ^ { ( i ) } , T _ { i } ^ { - 1 } T _ { j } ) \big )$$

这一全局一致性约束进一步增强了多视图推理的鲁棒性（Table 4）。

**关键设计选择。** 与直接使用能量建模（学习能量函数 $E_\theta$ 并通过自动微分获取得分）相比，显式得分建模在相同条件下表现更优（R@15: 0.963 vs 0.850, Table 5），因为得分网络直接学习梯度方向，避免了能量函数二阶导数的数值不稳定性。Figure 4的玩具示例直观展示了得分场与真实Oracle场的高度一致性，以及Zero123 MSE场中存在的多模态问题。

### 问题形式化与基线瓶颈

给定参考图像 $I_r$ 和查询图像 $I_q$，基于扩散先验的姿态反求方法（如 **iFusion**、**ID-Pose**）将相对姿态估计形式化为以下能量最小化问题：

$$\hat { T } _ { r \to q } = \mathop { \mathrm { a r g m i n } } _ { T \in S E ( 3 ) } \mathcal { L } ( I _ { q } , ( I _ { r } , T ) ) + \mathcal { L } ( I _ { r } , ( I _ { q } , T ^ { - 1 } ) )$$

其中 $\mathcal{L}$ 为冻结的 Zero123 扩散模型在姿态条件下去噪的 MSE 损失。该目标的优化景观存在三类典型地形（图 1）：单一全局最小值、沿经度方向的连续平台区域、以及多个局部极小值。后两种地形导致纯梯度下降对初始化高度敏感——从不同经度起始点出发的优化轨迹中，仅部分能收敛到真实姿态，其余陷入局部极小（图 2）。这一瓶颈迫使 iFusion 依赖 4–8 个随机初始化点以保证召回率，计算开销显著。

### 核心洞察：从能量建模到得分建模

本文的核心思路是将优化过程拆分为**全局引导**与**局部精炼**两个阶段。第一阶段不再直接最小化 Zero123 的 MSE 能量，而是显式学习数据分布的得分函数（score function）$s_\theta$，利用其梯度场将姿态引导至高似然区域，从而绕开能量景观中的局部极小。

得分网络采用简化的去噪得分匹配（Denoising Score Matching）目标训练。与标准 NCSN 不同，由于姿态空间维度低，噪声从均匀分布 $U$ 采样且噪声尺度固定为 $\sigma = 1$：

$$L(\theta) = \mathbb{E}_{\mathbf{x},\mathbf{y}}\mathbb{E}_{\tilde{\mathbf{x}}\sim U} \| s_\theta(\tilde{\mathbf{x}}, \mathbf{y}) - \nabla_{\tilde{\mathbf{x}}} \log p_\sigma(\tilde{\mathbf{x}} \mid \mathbf{x}, \mathbf{y}) \|^2$$

其中 $\mathbf{x}$ 为真实相对姿态，$\tilde{\mathbf{x}}$ 为加噪后的含噪姿态，$\mathbf{y}$ 为参考-查询图像对的条件信息。该损失的全局最优解为：

$$s ^ { \star } ( \tilde { \mathbf { x } } , \mathbf { y } ) = \mathbb { E } _ { \mathbf { x } \sim p ( \mathbf { x } \mid \mathbf { y } , \tilde { \mathbf { x } } ) } [ \nabla _ { \tilde { \mathbf { x } } } \log p _ { \sigma } ( \tilde { \mathbf { x } } \mid \mathbf { x } , \mathbf { y } ) ]$$

即条件后验下平滑得分函数的期望。

**得分网络结构**（图 3a）：使用 ResNet-50 编码器分别提取参考图像和查询图像的特征；含噪姿态通过正弦位置编码后与图像特征拼接，送入 MLP 预测得分向量。该得分向量指向真实姿态所在的高概率区域。

### 两阶段优化流程

整体优化框架（图 3c）由两个串行阶段构成：

**第一阶段：得分引导的 Langevin 动力学更新。** 利用学习的得分函数进行迭代姿态更新，显式注入高斯噪声以增强探索能力：

$$\tilde { \mathbf { x } } _ { t } = \tilde { \mathbf { x } } _ { t - 1 } + \alpha s _ { \theta } ( \tilde { \mathbf { x } } _ { t - 1 } , \mathbf { y } ) + G \mathbf { z } _ { t } , \quad \mathbf { z } _ { t } \sim \mathcal { N } ( 0 , \mathbf { I } _ { 3 } )$$

其中 $\alpha$ 为步长，$G$ 控制噪声幅度。该更新具有理论保证：姿态误差的期望呈指数衰减，方差近似为常数：

$$\| \mathbb { E } [ \tilde { \mathbf { x } } _ { t } - \mathbf { x } _ { \mathrm { g t } } ] \| = M ( 1 - \alpha ) ^ { t } , \quad \mathrm { V a r } [ \tilde { \mathbf { x } } _ { t } ] \approx \frac { G ^ { 2 } } { 2 \alpha }$$

这表明第一阶段能将姿态可靠地驱动至真实姿态附近的有界邻域内。

**第二阶段：Zero123 能量精炼。** 将第一阶段输出的姿态作为初始化，切换回冻结的 Zero123 扩散模型，通过最小化去噪 MSE 损失 $\mathcal{L}$ 进行细粒度姿态优化（图 3b）。此时姿态已位于全局最优的吸引域内，纯梯度下降即可稳定收敛。

### 多视图全局一致性扩展

对于 $N$ 张图像的多视图场景，第一阶段先推断所有成对相对姿态 $\mathcal{T} = \{T_{ij}\}_{i \neq j}$，再通过全局优化获得一致的绝对姿态 $\overline{\mathcal{T}} = \{\overline{T}_i\}_{i=1}^N$。第二阶段在此基础上进行联合能量最小化：

$$\hat { \mathcal { T } } = \underset { \{ T _ { 1 } , \ldots , T _ { n } \} \subset S E ( 3 ) } { \arg \operatorname* { m i n } } \sum _ { i = 1 } ^ { N } \sum _ { j \neq i } \mathcal { L } \big ( I ^ { ( j ) } , ( I ^ { ( i ) } , T _ { i } ^ { - 1 } T _ { j } ) \big )$$

该公式对所有视图对的去噪 MSE 损失求和，强制全局几何一致性，增强了多视图场景下的鲁棒性。

### 得分建模与能量建模的对比

图 4 的玩具示例直观展示了两种建模范式的差异：从 Zero123 MSE 损失导出的概率景观呈现双峰结构（图 4f），对应能量景观中的两个局部极小；而得分建模学到的得分场（图 4c）与 Oracle 得分场（图 4b）高度一致，能正确指向全局最优。消融实验（Table 5）定量证实：在相同 GSO 10 对象子集上，得分建模的 R@15 达到 0.963，显著优于能量建模的 0.850。

![[assets/figures/papers/paper_list_l2531_https_arxiv_org_abs_2605_19865/figures/002_Figure_2.jpg]]
*Figure 2: (a) & (b) Reference and query images of the object, captured from different camera poses. (c) Images generated by feeding the poses from optimization trajectory back into Zero123 [28]. Although all timestep-T images appear visually similar to the query, only two accurately reproduce the object’s correct appearance—white and blue in the front, yellow and red in the back—indicating correct pose alignment. (d) 2D MSE landscape with optimization trajectories initialized from four different starting poses at longitudes 0◦, 90◦, 180◦, and 270◦. Two of the trajectories converge to local minima. The bottom-left inset shows the 3D landscape for a clearer comparison*

## 实验与关键发现

### 核心实验设置

本文在三个代表性基准上系统评估了所提出的两阶段优化框架：**GSO**（合成物体数据集，用于物体级姿态估计）、**HOPEv2**（真实世界物体数据集）以及 **CO3Dv2**（大规模场景级数据集）。评价指标采用 Recall@15°/30° 和 Success Rate@30°（SR@30），其中 Success Rate 定义为在所有目标视图中均满足误差阈值 30° 的比例。基线方法包括基于 Zero123 梯度优化的 **iFusion** 和 **ID-Pose**，以及基于密集点图重建的 **DUSt3R** 和视觉几何 Transformer **VGGT**。对于无法输出绝对尺度的基线（DUSt3R、VGGT），通过寻找最优尺度因子来确保与本文归一化坐标表示的公平比较。

### 主要定量结果

**合成数据集上的显著提升。** 在 GSO 数据集上，本文方法在 SR@30 指标上达到 **0.836**，相比 iFusion 的 0.382 提升了 **+0.454**（Table 1），近乎翻倍。在 OO3D 数据集上同样取得最优结果。这一提升的核心机制在于：第一阶段得分引导有效绕过了 Figure 1 所示的局部极小值和平台区域，使得后续第二阶段精炼能够从高似然区域出发，而非像 iFusion 那样从随机初始化点直接进行梯度下降。

**真实场景下的鲁棒性。** 在 HOPEv2 真实世界数据集上，本文方法维持了强性能，SR@30 达到 **0.786**，而 iFusion 仅为 0.382（Table 2）。值得注意的是，即使面对具有强几何对称性的真实物体，由于纹理信息的存在，得分引导仍能有效消歧，使优化轨迹收敛到正确姿态（Figure 5b）。

**场景级姿态估计。** 在 CO3Dv2 的 29 个采样场景上，本文方法在 SR@30 上达到 **0.567**，远超 iFusion 的 0.237 和 ID-Pose 的 0.050（Table 7）。这表明得分引导框架在场景级多视图推理中同样有效，全局一致性优化（Eq. (6)）进一步增强了成对姿态估计的鲁棒性。

### 样本效率与推理时间

本文方法的核心优势之一在于对初始化点数量的低依赖性。如 Table 8 和 Figure 6 所示，当仅使用 **2 个初始化点**时，本文方法在 GSO 上的 R@30 达到 **0.901**，推理时间仅 **12.86 秒**；而 iFusion 在同样 2 个初始化点下 R@30 仅为 0.661，推理时间 23.30 秒。更重要的是，本文方法用 2 个初始化点即达到与 iFusion 用 8 个初始化点相当的召回率（0.901 vs 0.907），但推理时间减少了约 7 倍（12.86 s vs 91.92 s）。这一效率优势源于得分引导将初始化点快速引导至高似然区域，避免了大量随机采样带来的计算浪费。

![[assets/figures/papers/paper_list_l2531_https_arxiv_org_abs_2605_19865/figures/017_Table_8.jpg]]
*Table 8: Comparison of inference time and performance. We report recall (R@30) and inference time for different numbers of initial poses for each method. Our method achieves comparable performance while requiring substantially less inference time*

### 消融实验

**两阶段各自的贡献。** Table 4 的多视图消融实验表明，移除第一阶段得分引导（仅用 Zero123 MSE 优化）会导致性能大幅下降，验证了得分引导对于逃离局部极小值的关键作用。单独使用第一阶段而不进行第二阶段精炼同样性能不足，说明两阶段互补：第一阶段负责全局引导，第二阶段负责局部精炼。

**得分建模 vs 能量建模。** 在 GSO 10 对象子集上，得分建模在 R@15 上达到 **0.963**，显著优于能量建模的 0.850（Table 5）。Figure 4 的玩具示例直观展示了原因：得分建模学习的得分场（c）与 Oracle 得分场（b）高度一致，而能量建模的概率景观（g）虽能捕捉双峰结构，但其导出的得分场（e）精度不如直接学习得分。从因果机制上看，得分建模直接学习梯度方向，避免了能量建模中先建模能量再求导带来的误差放大。

**噪声尺度 γ 的权衡。** Table 9 揭示了第一阶段 Langevin 动力学中噪声尺度 γ 对性能的影响：增大 γ 可提高召回率（探索能力增强），但降低成功率（收敛稳定性下降）。这一权衡与 Eq. (5) 的理论分析一致——γ 通过影响方差项 $G^2/(2\alpha)$ 来控制探索-利用平衡。

**第二阶段先验模型的影响。** Table 10 显示，使用 **Zero123-XL** 作为第二阶段先验在所有指标上均优于原始 Zero123，表明更强的姿态条件扩散模型能进一步提升精炼质量。

### 泛化能力

Table 3 评估了在 GSO 数据集中未参与训练的 10 个新物体上的泛化性能。本文方法在未见物体上仍保持优势，说明得分网络学习的是与物体类别无关的姿态分布结构，而非过拟合于特定物体的外观特征。

### 失败模式与局限性

尽管整体性能显著提升，本文方法仍存在两类主要失败模式：

1. **Zero123 生成能力不足。** 对于某些物体，Zero123 的多视图生成不一致会导致第二阶段精炼劣化。Figure 9 展示了一个典型案例：螺丝刀物体在不同方位角下由 Zero123 生成的图像存在姿态歧义，使得 MSE 损失无法提供可靠的梯度信号。

![[assets/figures/papers/paper_list_l2531_https_arxiv_org_abs_2605_19865/figures/015_Figure_9.jpg]]
*Figure 9: (a) Reference image and (b) query image of the object, captured from different camera poses. (c) Rendered image from the 3D CAD model. (d) Image generated by the Zero123 model. Both vary ϕ from 0◦ to 315◦ in 45◦ increments*

2. **球坐标表示的对称性歧义。** Zero123 使用的球坐标相对姿态表示未显式定义物体坐标系，对于对称物体可能产生多义的目标视图。这一局限性源于表示本身，而非优化框架，需要在未来通过引入显式物体坐标系或改进姿态参数化来解决。

![[assets/figures/papers/paper_list_l2531_https_arxiv_org_abs_2605_19865/figures/006_Table_1.jpg]]
*Table 1: Evaluation results on the synthetic dataset. Results on the GSO and OO3D datasets show that our two-stage optimization framework improves success rate and recall across thresholds. Red indicates our best result, and blue denotes the second best result*

![[assets/figures/papers/paper_list_l2531_https_arxiv_org_abs_2605_19865/figures/010_Table_4.jpg]]
*Table 4: Multi-view joint reasoning. We evaluate our framework for multi-view estimation, reporting recall at thresholds of 15◦ and 30◦. To analyze the contributions of each stage, we include ablation results: without Stage 1 (score-based initialization), without Stage 2 (Zero123 refinement), and using both Stage 1 and Stage 2*

![[assets/figures/papers/paper_list_l2531_https_arxiv_org_abs_2605_19865/figures/011_Table_5.jpg]]
*Table 5: Ablation on different modeling approaches. We compares score-based modeling and energy-based modeling on the GSO dataset with 10 objects*

## 定位与知识库关联

### 1. 问题定位：扩散先验反推姿态的优化瓶颈

本文聚焦于利用预训练2D扩散模型（如Zero123）估计物体相对相机姿态这一新兴范式。该范式的核心思路是将姿态估计转化为逆问题：给定参考图 $I_r$ 和查询图 $I_q$，通过最小化扩散模型的去噪MSE损失来优化姿态参数 $T \in SE(3)$：

$$\hat { T } _ { r \to q } = \mathop { \mathrm { a r g m i n } } _ { T \in S E ( 3 ) } \mathcal { L } ( I _ { q } , ( I _ { r } , T ) ) + \mathcal { L } ( I _ { r } , ( I _ { q } , T ^ { - 1 } ) )$$

**ID-Pose** 和 **iFusion** 是该范式的代表性工作，它们直接对上述MSE损失执行梯度下降。然而，本文通过系统性的损失景观分析（Figure 1, Figure 10）揭示了一个此前未被充分诊断的关键瓶颈：Zero123的MSE损失景观普遍存在**多局部极小值**和**纵向平台区域**（continuous symmetry along longitude），导致梯度下降对初始化高度敏感——从不同初始经度出发的优化轨迹中，多数陷入局部极小，仅少数能收敛到真实姿态（Figure 2, Figure 11）。这一发现构成了本文方法设计的因果起点。

### 2. 方法锚点：得分建模重塑优化景观

针对上述瓶颈，本文的核心操作变量是**改变梯度信息的来源**：将第一阶段优化从隐式的能量梯度（Zero123 MSE对姿态的导数）替换为**显式学习的得分函数** $s_\theta(\tilde{\mathbf{x}}, \mathbf{y})$，其训练目标为去噪得分匹配（DSM）：

$$\mathcal { L } _ { \mathrm { D S M } } ( \theta ) = \frac { 1 } { 2 } \mathbb { E } _ { \tilde { \mathbf { x } } , \mathbf { x } } \left[ \lVert s _ { \theta } ( \tilde { \mathbf { x } } ) - \nabla _ { \tilde { \mathbf { x } } } \log p _ { \sigma } ( \tilde { \mathbf { x } } \mid \mathbf { x } ) \rVert _ { 2 } ^ { 2 } \right]$$

第一阶段使用Langevin动力学进行姿态迭代更新：

$$\tilde { \mathbf { x } } _ { t } = \tilde { \mathbf { x } } _ { t - 1 } + \alpha s _ { \theta } ( \tilde { \mathbf { x } } _ { t - 1 } , \mathbf { y } ) + G \mathbf { z } _ { t } , \quad \mathbf { z } _ { t } \sim \mathcal { N } ( 0 , \mathbf { I } _ { 3 } )$$

第二阶段则回归到Zero123的MSE损失进行局部精炼。这一两阶段设计的关键洞察在于：**得分网络学习的是数据分布的整体梯度场结构**，能够将姿态引导至高似然区域，从而有效避开MSE景观中的局部极小陷阱。玩具实验（Figure 4）直观地展示了得分场与能量场（MSE导出的隐式得分）的本质差异——前者与oracle得分场高度吻合，后者则表现出明显的局部结构缺陷。

### 3. 与相关工作的关系谱系

**直接竞争基线（同范式）**：
- **iFusion**：直接使用Zero123 MSE梯度优化，依赖4-8个随机初始化点来缓解局部极小问题。本文的方法在仅用2个初始化点时即达到iFusion 8个初始化点相当的召回率（R@30: 0.901 vs 0.661），推理时间从91.92秒降至12.86秒（Table 8），直接证明了得分引导对样本效率的根本性改善。
- **ID-Pose**：同为Zero123反求姿态的梯度优化方法，在CO3Dv2场景级测试中成功率仅0.050，显著低于本文的0.567（Table 7），进一步印证了纯MSE优化的脆弱性。

**跨范式对比**：
- **DUSt3R**和**VGGT**：基于密集点图或视觉Transformer的直接回归方法，与本文的优化范式有本质区别。值得注意的是，这些方法无法输出绝对尺度，而本文的球坐标表示天然具有归一化性质。为确保公平比较，本文通过搜索最优尺度因子来对齐坐标系统（Section C.1）。

**得分建模的理论渊源**：
本文的得分网络设计借鉴了**NCSN**（Song & Ermon, NeurIPS 2019）的得分匹配框架，但做了关键的简化适配：由于姿态空间是低维的（球坐标的3个参数），本文采用均匀噪声采样和固定噪声尺度 $\sigma=1$，避开了NCSN中多噪声尺度的复杂性。这一简化是合理的——低维空间的得分估计对噪声尺度的敏感度远低于高维图像空间。

### 4. 适用边界与失效模式

**适用条件**：
- 依赖Zero123的生成质量作为第二阶段精炼的基础。当Zero123对特定物体的视角生成能力不足时，精炼阶段可能劣化。
- 球坐标相对姿态表示天然适合物体中心场景，但不显式定义物体坐标系。

**已知失效模式**：
1. **对称性歧义**：对于螺丝刀等具有旋转对称性的物体，Zero123在不同方位角下生成的图像视觉上高度相似（Figure 9），导致姿态表示存在内在歧义。球坐标表示无法显式编码物体坐标系，加剧了这一问题。
2. **多视图不一致**：Zero123的生成结果在多视图间可能存在不一致性，这会通过第二阶段精炼传播为姿态估计误差。

**探索-收敛权衡**：
消融实验（Table 9）揭示了一个重要的调控维度：增大第二阶段噪声尺度 $\gamma$ 可提高召回率（更多初始化点最终被引导至正确区域），但降低成功率（精炼后的解不够精确）。这反映了得分引导的探索能力与MSE精炼的收敛稳定性之间的内在张力，实际部署时需根据应用场景（高召回 vs 高精度）调整。

### 5. 开放问题与未来方向

1. **更强先验的集成**：Table 10显示使用Zero123-XL作为第二阶段先验可全面提升性能，但当前框架中得分网络与Zero123-XL是独立训练的。如何将更强的姿态条件扩散模型与得分引导框架进行端到端联合优化，是一个值得探索的方向。

2. **姿态参数化的重新思考**：球坐标表示虽然简洁，但对对称物体的歧义问题表明，可能需要引入显式的物体坐标系或等变表示来从根本上减少姿态空间的多义性。这需要权衡表示的完备性与优化的难易程度。

3. **场景级扩展的深化**：CO3Dv2上的结果（Table 7）展示了向场景级应用的初步潜力，但成功率（0.567）仍显著低于物体级（0.836），说明场景中的遮挡、多物体交互等因素对当前框架构成额外挑战。

## 原文 PDF

![[paperPDFs/CVPR_2026/Landscape_Awareness_for_Geometric_View_Diffusion_Model.pdf]]
