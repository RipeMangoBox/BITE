---
title: "Sparkle: A Robust and Versatile Representation for Point Cloud-based Human Motion Capture"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Sparkle_A_Robust_and_Versatile_Representation_for_Point_Cloud_based_Human_Motion_Capture.pdf
project_link: null
code_link: null
openreview_forum_id: 0blfYtdJES
aliases:
- Sparkle
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过将人体表征显式分解为内部运动学（骨骼关节）和外部几何（表面锚点），并借助语义分割驱动的点对齐优化、线性初始化的几何先验以及 swing-twist 解析分解，实现了结构先验与几何细节的协同利用。"
primary_logic: "Sparkle 表征将人体状态解耦为互补的运动学空间和几何空间，注入强物理归纳偏置，使模型能够在高噪声、遮挡和多传感器条件下同时保持结构一致性和表面保真度，并通过几何驱动的参数初始化大幅降低学习复杂度。"
claims:
- "在噪声和遮挡严重的 FreeMotion-OBJ 和 NoiseMotion 数据集上，SparkleMotion 的局部关节/顶点误差较最强基线 LiveHPS++ 降低约 28-44%，验证了 Sparkle 表征对噪声的鲁棒性。"
- "在近距离交互场景 Interhuman 中，角度误差从 18.47° 降至 6.75°，下降 63.5%，证明表面锚点有效解决了旋转歧义。"
- "即使在 70% 点云遮挡下，全局关节/顶点误差仍保持在 118.7/128.3 mm，表明两阶段设计（几何初始化+学习精炼）的强鲁棒性。"
- "仅使用 50% 目标域训练数据即可达到与全量监督基线（LiveHPS++）相当的性能（MPJPE 61.5 vs 61.9），验证了 Sparkle 表征的数据高效性和跨域泛化能力。"
---

# Sparkle: A Robust and Versatile Representation for Point Cloud-based Human Motion Capture

> [!tip] 核心洞察
> Sparkle 表征将人体状态解耦为互补的运动学空间和几何空间，注入强物理归纳偏置，使模型能够在高噪声、遮挡和多传感器条件下同时保持结构一致性和表面保真度，并通过几何驱动的参数初始化大幅降低学习复杂度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Sparkle：一种用于点云人体运动捕捉的鲁棒多功能表征 |
| 英文题名 | Sparkle: A Robust and Versatile Representation for Point Cloud-based Human Motion Capture |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=0blfYtdJES) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SparkleMotion |
| Dataset | Interhuman (close interaction), GTA-Human-Point (cross-sensor), HuMMan-Point (cross-sensor), FreeMotion-MV (multi-view) |

> [!tip] 效果简介
> - Interhuman (close interaction) 上，Ang Err (degree) ↓ 为 6.75，对比 18.47 (LiveHPS++)，变化 -63.5%。
> - GTA-Human-Point (cross-sensor) 上，J/V Err(L) (mm) ↓ 为 69.1/82.2，对比 77.5/90.4 (LiveHPS++)，变化 -10.8%/-9.1%。
> - HuMMan-Point (cross-sensor) 上，Ang Err (degree) ↓ 为 12.60，对比 21.47 (LiveHPS++)，变化 -41.3%。

## 概要

### 问题瓶颈

现有的点云人体动作捕捉方法在表征学习上存在一个根本性的权衡：基于原始点云的方法能够保留丰富的几何细节，但对传感器噪声和遮挡极为敏感；基于骨架的方法通过引入强结构先验提升了鲁棒性，却丢失了表面几何信息，导致在肢体旋转估计中出现严重的旋转模糊和姿态歧义。这一瓶颈在近距离交互、严重遮挡和跨传感器场景中尤为突出。

### 核心思路

**Sparkle** 表征将人体状态显式解耦为互补的两个空间——内部运动学空间（骨骼关节）和外部几何空间（表面锚点），并注入强物理归纳偏置，使模型能够在高噪声、遮挡和多传感器条件下同时保持结构一致性和表面保真度。其关键机制包括：

- **语义分割驱动的点对齐残差优化**：通过隐式语义分割将点云分配到各身体部位，对每个关节利用局部点云预测残差偏移，实现精确的骨骼关节估计。
- **骨架引导的线性初始化**：利用从真值数据预计算的最小二乘线性映射，从关节位置解析地初始化表面锚点，注入解剖结构先验。
- **Swing-Twist 解析分解**：将轴角姿态分解为摆动和扭转分量，仅利用骨向量完成摆动对齐，再借助锚点对齐解析计算绕骨轴的扭转，实现无需学习参数的几何驱动姿态初始化。

### 方法定位

**SparkleMotion** 由三个核心模块构成：

| 模块 | 功能 |
|------|------|
| **Point-aligned Skeleton Tracker (PST)** | 从输入点云估计初始关节位置与全局平移，通过点对齐残差优化获得精确骨骼关节 |
| **Skeleton-guided Anchor Estimator (SAE)** | 基于优化后的关节线性初始化表面锚点，再通过交叉注意力融合关节特征与点云几何进行非线性精炼 |
| **Sparkle-based SMPL Solver (SSS)** | 以 swing-twist 解析分解进行几何驱动姿态初始化，利用轻量交叉注意力网络精细修正，输出最终 SMPL 参数 |

在方法谱系中，SparkleMotion 区别于 **LiDARCap**（Li et al., 2022）、**LiveHPS/LiveHPS++**（Ren et al., 2024a/2024b）等直接从点云回归关节的基线，也不同于 **VoteHMR**（Liu et al., 2021）、**PointHPS**（Cai et al., 2023）等纯点云方法，其核心创新在于将人体表征显式分解为运动学与几何两个互补空间，并通过几何驱动的初始化大幅降低学习复杂度。

### 主要结果

SparkleMotion 在 11 个多样化基准数据集上进行了全面验证，涵盖 LiDAR、深度相机和多视图传感器，关键结论如下：

- **噪声与遮挡鲁棒性**：在 FreeMotion-OBJ 和 NoiseMotion 两个高噪声数据集上，局部关节/顶点误差较最强基线 LiveHPS++ 降低约 28–44%（Table 1）。即使在 70% 点云遮挡下，全局关节/顶点误差仍保持在 118.7/128.3 mm（Table 8）。
- **旋转歧义消除**：在近距离交互场景 Interhuman 中，角度误差从 18.47° 降至 6.75°，下降 63.5%，证明表面锚点有效解决了旋转模糊问题（Table 2）。
- **跨传感器泛化**：在 GTA-Human-Point 和 HuMMan-Point 跨传感器数据集上，角度误差分别降低 10.8% 和 41.3%（Table 3）。
- **数据高效性**：仅使用 50% 目标域训练数据即可达到与全量监督基线相当的性能（MPJPE 61.5 vs 61.9），验证了 Sparkle 表征的强泛化能力（Table 11）。

> **注意**：本文未提供论文发表的会议/期刊和年份信息，上述元数据需手动核实。



### 点云人体动作捕捉的根本挑战

从点云中恢复精确的人体运动是计算机视觉与图形学中的基础问题，在体育分析、虚拟现实、人机交互等领域有广泛应用。然而，该任务面临一个根本性的表征学习困境：**如何同时保留几何细节与结构一致性**。

现有方法在这一问题上存在明确的分野与权衡：

- **基于原始点的方法**（如 VoteHMR、PointHPS）直接从点云回归人体参数。这类方法保留了丰富的表面几何信息，但由于缺乏显式的结构先验，对噪声、遮挡和点云稀疏性极为敏感。当输入点云质量下降时，预测结果容易出现肢体错位、关节断裂等结构性问题。

- **基于骨架的方法**（如 LiDARCap、LiveHPS、LiveHPS++）先估计骨骼关节位置，再通过逆向运动学或参数模型恢复姿态。骨架作为强结构先验，提供了运动学一致性保障，但这一过程丢弃了表面几何细节，导致**旋转模糊**和**姿态歧义**——同一组关节位置可以对应多种不同的表面变形，尤其在肢体绕骨轴旋转时，骨骼本身无法提供约束。

这一权衡构成了点云人体动作捕捉领域的核心瓶颈：结构先验与几何细节似乎难以兼得。

### 现有方法的局限性

以当前最强的 LiDAR 基线 LiveHPS++ 为例，其在一般场景下表现良好，但在以下关键场景中暴露出明显不足：

- **噪声与遮挡场景**：在 FreeMotion-OBJ 和 NoiseMotion 等含严重噪声的数据集上，LiveHPS++ 的局部关节误差高达 70.7 mm 和 60.2 mm，顶点误差更是达到 88.4 mm 和 72.0 mm，表明其对点云质量退化缺乏鲁棒性。

- **近距离交互场景**：在 Interhuman 等双人紧密交互数据集中，LiveHPS++ 的角度误差高达 18.47°，说明仅依赖骨骼关节无法有效分辨肢体绕骨轴的旋转，导致严重的旋转歧义。

- **跨传感器泛化**：从 LiDAR 迁移到深度相机点云时，LiveHPS++ 在 HuMMan-Point 上的角度误差仍达 21.47°，反映出其表征对传感器特性变化的适应性不足。

这些局限性根源于一个共同问题：**现有表征未能显式建模人体的双重本质——内部运动学结构（骨骼）与外部几何形态（表面）**。

### 本文动机与核心思路

针对上述瓶颈，本文提出了一种统一的中间表征 **Sparkle**，其核心思想是：**将人体状态显式分解为互补的运动学空间与几何空间，并注入强物理归纳偏置**。

具体而言，Sparkle 表征由两部分构成：

- **内部运动学表征**：一组精确估计的骨骼关节，提供结构骨架与运动学先验。
- **外部几何表征**：一组从 SMPL 网格顶点中通过 PCA 选取的表面锚点，编码表面形状信息。

这一解耦设计的动机在于：骨骼关节负责维持全局结构一致性，表面锚点负责消除旋转歧义并保留局部几何细节。两者协同作用，使模型能够在高噪声、遮挡和多传感器条件下同时保持结构完整性与表面保真度。

基于 Sparkle 表征，本文进一步提出了 **SparkleMotion**——一个三阶段的实时动作捕捉框架，通过几何驱动的解析初始化与学习式精炼相结合，在效率与精度之间取得平衡。该方法在 11 个多样化基准数据集上展现出对现有方法的显著优势，尤其在噪声鲁棒性、交互场景精度和跨域泛化能力方面实现了突破性提升。



## 核心方法与创新机理

SparkleMotion 的核心创新在于提出了一种名为 **Sparkle** 的统一中间表征，将人体运动捕捉中长期对立的两类信息——内部运动学（骨骼关节）与外部几何（表面锚点）——显式解耦并协同利用。这一设计从根本上改变了现有方法的表征学习范式，具体体现在以下四个关键改变槽位（changed slots）上。

### 从直接回归到语义分割驱动的点对齐残差优化

现有 LiDAR/点云动作捕捉方法（如 **LiDARCap** (Li et al., 2022)、**LiveHPS** (Ren et al., 2024b)）通常直接从点云回归骨骼关节位置，缺乏对局部几何结构的显式利用。SparkleMotion 的 **Point-aligned Skeleton Tracker (PST)** 改变了这一范式：它首先通过 PointNet 骨干网络与双向 GRU 预测初始关节位置和全局平移，同时对点云进行隐式语义分割，将每个点分配到 24 个身体部位。在此基础上，PST 对每个关节利用其所属局部点云，通过共享的 PointNet 预测残差偏移量，并通过迭代的点-关节对齐优化获得精确的骨骼关节。

这一改变的因果机制在于：语义分割迫使网络学习每个点的身体部位归属，从而为后续的局部几何推理提供了强归纳偏置；而残差学习而非直接回归的策略，使网络只需建模初始估计与真值之间的微小差异，大幅降低了优化难度。消融实验证实了这一点：去除偏移量学习（w/o offset）或去除优化过程（w/o op）均导致全局关节/顶点误差显著上升（Table 5, PST ablations on FreeMotion），验证了点对齐残差优化的关键作用。

### 从无表面几何到骨架引导的锚点表征

现有方法或仅依赖骨骼关节（如 LiveHPS++），或直接使用原生点云（如 **PointHPS** (Cai et al., 2023)），缺乏对表面几何的显式结构化表征。SparkleMotion 引入 **Skeleton-guided Anchor Estimator (SAE)**，在 SMPL 网格顶点上通过 PCA 选取 32 个表面锚点，作为外部几何的结构化代理。

SAE 的核心创新在于其“线性初始化 + 交叉注意力精炼”的两阶段设计。首先，利用从真值数据通过最小二乘法预计算的线性映射矩阵 $\mathbf{M}_{\mathrm{J2A}} = (\mathbf{A}_{\mathrm{gt}}^{\top} \mathbf{A}_{\mathrm{gt}})^{-1} \mathbf{A}_{\mathrm{gt}}^{\top} \mathbf{J}_{\mathrm{gt}}$，从优化后的关节位置直接初始化表面锚点。这一解剖学先验驱动的线性初始化提供了稳定且物理合理的初值。随后，SAE 通过交叉注意力机制，以 PST 输出的关节特征作为查询（Query），以点云几何特征作为键（Key）和值（Value），学习非线性修正以得到精确锚点。消融实验表明，跳过线性初始化（w/o initialize）会导致锚点预测不稳定（Table 5, SAE ablations），而交叉注意力精炼显著优于直接 MLP 精炼（Table 10），证明结构化先验与几何证据的有效融合是锚点估计成功的关键。

### 从学习式初始化到几何驱动的解析姿态求解

现有方法通常直接回归 SMPL 姿态参数或使用学习式的初始化网络，缺乏对运动学约束的显式利用。SparkleMotion 的 **Sparkle-based SMPL Solver (SSS)** 采用 **swing-twist 解析分解**进行纯几何驱动的姿态初始化，无需任何学习参数。

具体而言，对于 SMPL 骨架中的每根骨骼，SSS 将轴角旋转分解为摆动（swing）和扭转（twist）两个分量：摆动旋转通过骨向量对齐解析计算，仅利用骨骼关节信息（$\vec{n}_{\mathrm{sw}} = \frac{\vec{\mathbf{J}}_{\mathrm{tem}} \times \vec{\mathbf{J}}'_{op}}{\lVert \vec{\mathbf{J}}_{\mathrm{tem}} \times \vec{\mathbf{J}}'_{op} \rVert}$）；扭转旋转则绕骨轴对齐模板锚点与预测锚点，利用表面信息（$\alpha_{\mathrm{tw}} = \arctan 2(\lVert \mathbf{A}_{\mathrm{tem}} \times \mathbf{A}'_{op} \rVert, \mathbf{A}_{\mathrm{tem}} \cdot \mathbf{A}'_{op})$）。这一分解巧妙地利用了 Sparkle 表征中运动学空间与几何空间的互补性：骨骼提供方向约束，锚点提供绕轴旋转约束，二者共同消解了仅依赖骨骼时的旋转歧义。

消融实验证实了这一设计的决定性作用：移除几何初始化（w/o init）导致网络收敛至次优姿态（Table 5, SSS ablations），验证了解析 swing-twist 分解提供有效初值对于后续学习精炼的不可或缺性。

### 从单阶段回归到“几何初始化 + 学习精炼”的两阶段范式

上述三个模块共同构成了 SparkleMotion 的核心方法论创新：将人体运动参数回归从传统的端到端黑箱映射，转变为“几何初始化 + 学习精炼”的两阶段范式。几何初始化阶段注入强物理归纳偏置（线性映射、swing-twist 分解），提供物理一致但可能存在系统偏差的初值；学习精炼阶段（交叉注意力网络）则专注于建模非线性修正，弥合解析解与真实人体形变之间的差距。这一范式在 70% 点云遮挡下仍将全局关节/顶点误差保持在 118.7/128.3 mm（Table 8），并在仅使用 50% 目标域训练数据时达到与全量监督基线相当的性能（MPJPE 61.5 vs 61.9, Table 11），充分展现了其鲁棒性与数据高效性。



![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_0blfYtdJES/figures/002_Figure_2.jpg]]
*Figure 2: The pipeline of SparkleMotion. It can take point clouds of diverse patterns as input in different challenge scenarios, as shown on the left. SparkleMotion consists of three primary modules, the Point-aligned Skeleton Tracker, and Skeleton-guided Anchor Estimator construct the Sparkle Representation, and the Sparkle-based SMPL Solver for motion reconstruction*

SparkleMotion 的整体流水线遵循**两阶段结构化表征 → 参数化运动求解**的设计范式，由三个核心模块串联构成：**Point-aligned Skeleton Tracker (PST)**、**Skeleton-guided Anchor Estimator (SAE)** 和 **Sparkle-based SMPL Solver (SSS)**。其核心思想是将人体状态显式解耦为内部运动学空间（骨骼关节）与外部几何空间（表面锚点），并通过几何驱动的初始化与学习式精炼的协同，实现从原始点云到 SMPL 参数的高效映射。

### 流水线结构

如图 Figure 2 所示，系统以任意分布模式的点云 $\mathcal{P}$ 作为输入，依次经过以下阶段：

1. **PST 模块**：从原始点云中预测初始骨骼关节位置 $\mathbf{J}_{\text{init}}$ 和全局平移 $\mathbf{T}_{\text{init}}$，同时进行隐式语义分割，将点云划分为 24 个身体部位。随后，对每个关节利用其所属局部点云，通过共享的 PointNet 预测残差偏移量，经迭代优化得到精确的骨骼关节 $\mathbf{J}_{\text{op}}$ 和优化后的全局平移 $\mathbf{T}_{\text{op}}$。

2. **SAE 模块**：以上一阶段优化后的关节 $\mathbf{J}_{\text{op}}$ 为条件，通过预计算的线性映射矩阵 $\mathbf{M}_{\text{J2A}}$ 初始化 32 个表面锚点 $\mathbf{A}_{\text{init}}$，再利用交叉注意力机制融合关节特征与点云几何特征，学习非线性修正，输出精确锚点 $\mathbf{A}_{\text{op}}$。PST 和 SAE 的输出拼接构成 **Sparkle 表征** $\bar{\mathcal{S}} = [\mathbf{J}_{\text{op}}', \bar{\mathbf{A}}_{\text{op}}']$。

3. **SSS 模块**：接收 Sparkle 表征，首先通过 swing-twist 解析分解进行几何驱动的姿态初始化——利用骨向量对齐计算摆动旋转，利用锚点对齐计算绕骨轴的扭转旋转，得到物理一致的初始姿态 $\pmb{\theta}_{\text{init}}$；随后通过轻量级交叉注意力网络学习非线性修正，输出最终 SMPL 姿态参数 $\hat{\pmb{\theta}}_{\text{op}}$ 和形状参数 $\hat{\beta}$。

### 设计逻辑

该流水线的关键设计在于**每一阶段都注入了强物理归纳偏置**：PST 通过点-关节对齐优化利用局部几何证据精炼关节位置；SAE 的线性初始化基于解剖学先验（关节到表面锚点的最小二乘映射），使锚点预测具有结构稳定性；SSS 的几何初始化则利用骨骼方向与表面锚点的双重约束解析求解旋转，为后续学习式精炼提供优质初值。这种“几何初始化 + 学习修正”的两阶段策略在多个模块中复现，是 SparkleMotion 在高噪声、遮挡和跨传感器条件下保持鲁棒性的核心机制。

### 多视图扩展

Sparkle 表征的结构化特性使其具备天然的可扩展性。如图 Figure 6 所示，在多视图场景下，系统可接收来自任意视角的点云，分别提取 Sparkle 表征后进行融合与联合优化，无需重新设计网络架构，展示了表征本身的强大可迁移性。



### 问题定义与表征设计

SparkleMotion 的核心思想是将人体运动捕捉问题转化为一个结构化表征的学习与优化过程。给定一帧无序点云 $\mathcal{P} \in \mathbb{R}^{N \times 3}$，目标是恢复 SMPL 模型参数 $(\boldsymbol{\theta}, \boldsymbol{\beta})$，其中 $\boldsymbol{\theta}$ 为姿态参数，$\boldsymbol{\beta}$ 为形状参数。传统方法直接从点云回归参数或骨骼关节，在噪声、遮挡和旋转歧义场景下表现脆弱。

Sparkle 表征将人体状态显式解耦为两个互补空间：

$$\mathbf{\bar{S}} = [\mathbf{J}_{op}', \mathbf{\bar{A}}_{op}']$$

其中 $\mathbf{J}_{op}' \in \mathbb{R}^{24 \times 3}$ 为优化后的 24 个骨骼关节，$\mathbf{\bar{A}}_{op}' \in \mathbb{R}^{32 \times 3}$ 为优化后的 32 个表面锚点。这一设计的关键洞察在于：骨骼关节提供强运动学结构先验，表面锚点保留外部几何细节，二者协同作用，使模型能同时保持结构一致性和表面保真度。

---

### 模块一：Point-aligned Skeleton Tracker (PST)

PST 负责从点云中估计精确的骨骼关节位置，其核心创新在于**语义分割驱动的点对齐残差优化**。

**流程**：首先，PointNet 骨干网络结合双向 GRU 预测初始关节位置 $\mathbf{J}_{\mathrm{init}}$ 和全局平移 $\mathbf{T}_{\mathrm{init}}$。同时，网络执行隐式语义分割，将点云分解为 24 个体部区域，输出逐点标签 $\mathbf{L}_j \in \{0, 1, \dots, 24\}$。随后，对每个关节，利用其对应体部区域的局部点云，通过共享 PointNet 预测残差偏移量，迭代修正关节位置，得到优化关节 $\mathbf{J}_{op}$。

**损失函数**：

$$\mathcal{L}_{\mathrm{PST}} = \lambda_1 \mathcal{L}_{\mathrm{MSE}}(\mathbf{J}_{\mathrm{op}}, \mathbf{J}_{\mathrm{gt}}) + \lambda_2 \mathcal{L}_{\mathrm{CE}}(\mathbf{L}_j, \mathbf{L}_{j_{\mathrm{gt}}}) + \lambda_3 \mathcal{L}_{\mathrm{MSE}}(\mathbf{T}_{\mathrm{op}}, \mathbf{T}_{\mathrm{gt}})$$

其中 $\mathcal{L}_{\mathrm{MSE}}$ 为均方误差，$\mathcal{L}_{\mathrm{CE}}$ 为交叉熵损失。三项分别约束关节位置精度、点云语义分割准确性和全局平移估计。消融实验（Table 5, Table 9）证实，移除残差学习（w/o offset）或迭代优化（w/o op）均导致全局误差大幅上升，验证了点-关节对齐机制的关键作用。

---

### 模块二：Skeleton-guided Anchor Estimator (SAE)

SAE 引入 32 个表面锚点作为外部几何表征，其设计瓶颈在于如何将稀疏的骨骼关节信息有效映射到表面空间。SAE 采用**线性初始化 + 交叉注意力精炼**的两阶段策略。

**线性初始化**：利用预计算的关节-锚点映射矩阵，从优化关节直接估计初始锚点。该映射通过最小二乘法从真值数据预先计算：

$$\mathbf{M}_{\mathrm{J2A}} = (\mathbf{A}_{\mathrm{gt}}^{\top} \mathbf{A}_{\mathrm{gt}})^{-1} \mathbf{A}_{\mathrm{gt}}^{\top} \mathbf{J}_{\mathrm{gt}}$$

这一几何先验基于人体解剖结构的一致性，为锚点预测提供了强约束的初始值。

**交叉注意力精炼**：将 PST 输出的关节特征 $\mathbf{F}_{\mathrm{joint}}$ 作为 Query，锚点特征 $\mathbf{F}_{\mathrm{anchor}}$ 作为 Key 和 Value，通过交叉注意力机制融合结构先验与点云几何证据，学习非线性修正，得到优化锚点 $\mathbf{A}_{op}$。

**损失函数**：

$$\mathcal{L}_{\mathrm{SAE}} = \lambda_4 \mathcal{L}_{\mathrm{MSE}}(\mathbf{A}_{\mathrm{op}}, \mathbf{A}_{\mathrm{gt}}) + \lambda_5 \mathcal{L}_{\mathrm{CE}}(\mathbf{L}_a, \mathbf{L}_{a_{\mathrm{gt}}})$$

联合约束锚点位置精度和锚点级语义分割。消融实验（Table 5, Table 10）表明，省略线性初始化（w/o initialize）会导致锚点预测不稳定，而交叉注意力精炼显著优于直接 MLP 精炼，验证了结构化初始化和注意力融合的有效性。

---

### 模块三：Sparkle-based SMPL Solver (SSS)

SSS 将 Sparkle 表征转化为 SMPL 参数，其核心创新在于**swing-twist 解析分解的几何驱动初始化**，大幅降低了学习复杂度。

**几何驱动初始化**：对 SMPL 骨架中的每根骨骼 $b$，将轴角旋转 $\mathbf{R}$ 分解为摆动（swing）和扭转（twist）两个分量 $\mathbf{R} = \mathbf{R}^{sw} \mathbf{R}^{tw}$。

摆动旋转将模板骨方向对齐到预测的骨方向，仅依赖骨骼信息：

$$\vec{n}_{\mathrm{sw}} = \frac{\vec{\mathbf{J}}_{\mathrm{tem}} \times \vec{\mathbf{J}}'_{op}}{\lVert \vec{\mathbf{J}}_{\mathrm{tem}} \times \vec{\mathbf{J}}'_{op} \rVert},\quad \alpha_{\mathrm{sw}} = \arccos\left(\frac{\vec{\mathbf{J}}_{\mathrm{tem}} \cdot \vec{\mathbf{J}}'_{op}}{\lVert\vec{\mathbf{J}}_{\mathrm{tem}}\rVert\lVert\vec{\mathbf{J}}'_{op}\rVert}\right)$$

扭转旋转绕骨轴对齐模板锚点与预测锚点，利用表面信息解决旋转歧义：

$$\alpha_{\mathrm{tw}} = \arctan 2\left(\lVert \mathbf{A}_{\mathrm{tem}} \times \mathbf{A}'_{op} \rVert, \mathbf{A}_{\mathrm{tem}} \cdot \mathbf{A}'_{op}\right)$$

**Sparkle 引导的参数精炼**：几何初始化提供物理一致的初值，但解析解存在误差。SSS 采用轻量级交叉注意力网络，以 Sparkle 表征为条件，学习姿态和形状参数的非线性修正：

$$\mathcal{L}_{\mathrm{SSS}} = \lambda_6 \mathcal{L}_{\mathrm{MSE}}(\hat{\boldsymbol{\theta}}_{\mathrm{op}}, \boldsymbol{\theta}_{\mathrm{gt}}) + \lambda_7 \mathcal{L}_{\mathrm{MSE}}(\hat{\boldsymbol{\beta}}, \boldsymbol{\beta}_{\mathrm{gt}})$$

消融实验（Table 5）证实，移除几何初始化（w/o init）使网络收敛至次优姿态，而跳过精炼（w/o op）则使解析解误差无法修正，验证了两阶段设计的必要性。

---

### 锚点选择与设计权衡

表面锚点的数量和选取策略直接影响表征能力与计算效率的平衡。实验（Table 6）对比了三种策略：PCA 选取（从 SMPL 网格顶点中通过主成分分析选出最具表达力的锚点）、随机选取和手动选取。结果表明，**PCA-32 方案**在表征能力与计算效率之间达到最优平衡——锚点过少（如 16 个）丢失几何细节，过多（如 50 个）增加冗余计算而收益递减。



## 实验与关键发现

### 核心性能验证：噪声与遮挡场景下的鲁棒性

SparkleMotion 在四个一般场景数据集上进行了系统评估（Table 1），覆盖 LiDAR 和深度相机采集的噪声与遮挡条件。在噪声严重的 **FreeMotion-OBJ** 数据集上，SparkleMotion 的局部关节误差（J Err(L)）和局部顶点误差（V Err(L)）分别为 50.8 mm 和 62.7 mm，较最强基线 **LiveHPS++**（Ren et al., 2024a）的 70.7 mm 和 88.4 mm 分别降低约 28.1% 和 29.1%。在 **NoiseMotion** 数据集上，这一优势更为显著：局部关节/顶点误差从 LiveHPS++ 的 60.2/72.0 mm 降至 27.8/36.3 mm，降幅达 53.8%/49.6%。这直接验证了 Sparkle 表征的核心因果机制——通过显式解耦运动学结构（骨骼关节）与表面几何（锚点），模型在高噪声条件下能同时保持结构一致性和表面保真度，而纯骨架方法（LiveHPS++）因缺乏表面约束导致误差放大。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_0blfYtdJES/figures/004_Table_1.jpg]]
*Table 1: Evaluation Metrics We adopt widely used metrics in motion capture to ensure a comprehensive assessment of human motion accuracy, including local and global joint/vertex errors(J/V Err(L/G))(mm ↓) and angle errors(Ang Err)(degree ↓). Table 1: Evaluations on general scenarios with noisy and occlusion in 4 datasets. Notice our substantial improvement on noisy datasets, FreeMotion-OBJ and NoiseMotion*

在全局误差指标上，SparkleMotion 同样保持领先：FreeMotion 数据集上全局关节/顶点误差为 105.1/113.9 mm，优于 LiveHPS++ 的 115.2/122.5 mm。值得注意的是，即使在相对干净的 **Sloper4D** 数据集上，SparkleMotion 仍以 70.9/77.1 mm（全局关节/顶点误差）优于 LiveHPS++ 的 76.8/82.9 mm，表明该表征在不同噪声水平下具有一致增益。

### 近距离交互场景：旋转歧义的突破性解决

交互场景中人体肢体重叠导致的旋转歧义是点云动作捕捉的核心难题。在 **Interhuman** 数据集上（Table 2），SparkleMotion 将角度误差从 LiveHPS++ 的 18.47° 降至 6.75°，降幅达 63.5%。这一突破性改进源于表面锚点的引入——当骨骼关节因肢体重叠而无法提供可靠方向信息时，32 个 PCA 选取的表面锚点通过 swing-twist 解析分解（公式 4-5）提供了绕骨轴的扭转约束，从根本上消除了旋转歧义。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_0blfYtdJES/figures/005_Table_2.jpg]]
*Table 2: Evaluation on close-interaction datasets*

在 **Chi3D** 和 **Hi4D** 数据集上，SparkleMotion 分别取得 10.52° 和 11.39° 的角度误差，均大幅优于 LiveHPS++（分别为 13.37° 和 15.98°）。局部关节误差在三个交互数据集上均保持在 30.4-36.1 mm 的窄区间内，证明该方法对不同交互模式的泛化能力。

### 跨传感器与多视图泛化

SparkleMotion 在跨传感器泛化实验中展现出强迁移能力（Table 3）。在 **GTA-Human-Point**（合成 LiDAR）和 **HuMMan-Point**（深度相机）数据集上，角度误差分别为 11.52° 和 12.60°，较 LiveHPS++ 的 13.17° 和 21.47° 分别降低 12.5% 和 41.3%。HuMMan-Point 上角度误差的大幅下降（41.3%）表明，Sparkle 表征的几何初始化策略（基于 swing-twist 分解的解析计算，无需学习参数）对传感器特性差异具有天然鲁棒性——该初始化仅依赖骨向量和锚点对齐的几何约束，不依赖特定传感器的统计分布。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_0blfYtdJES/figures/006_Table_3.jpg]]
*Table 3: Evaluation on cross-sensor generalization*

在多视图场景下（Table 4），SparkleMotion 在 **FreeMotion-MV** 上取得 9.61° 的角度误差，优于多视图专用方法 **FreeCap**（Xue et al., 2025）的 12.24°，降幅 21.5%。这验证了 Sparkle 表征的可扩展性：多视图点云融合后，结构化表征（关节+锚点）能更有效地整合多视角几何证据。

### 消融实验：各模块的因果贡献

**PST 模块消融**（Table 5）揭示了残差学习与迭代优化的关键作用。去除偏移量学习（w/o offset）导致全局关节误差在 FreeMotion 上从 105.1 mm 升至 119.8 mm（+14.0%），证明直接从点云回归绝对关节位置难以处理点云稀疏性和噪声。进一步去除优化过程（w/o op）使误差升至 125.3 mm，验证了迭代式点-关节对齐对全局定位精度的贡献。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_0blfYtdJES/figures/008_Table_5.jpg]]
*Table 5: Ablation studies for our network modules across multiple datasets*

**SAE 模块消融**确认了线性初始化的必要性。跳过线性初始化（w/o initialize）使锚点预测不稳定，在 FreeMotion 上全局顶点误差从 113.9 mm 升至 123.5 mm（+8.4%）。该初始化矩阵 $\mathbf{M}_{\mathrm{J2A}}$ 通过最小二乘法从真值数据预计算（公式 2），注入了关节-锚点间的解剖先验，大幅降低了学习复杂度。去除交叉注意力精炼（w/o op）后，误差进一步升至 127.2 mm，证明几何感知的特征融合对修正线性近似误差不可或缺。

**SSS 模块消融**验证了两阶段设计的核心价值。移除几何初始化（w/o init）使网络收敛至次优姿态，全局关节误差从 105.1 mm 升至 116.7 mm（+11.0%）。跳过精炼网络（w/o op）后误差升至 112.3 mm，表明解析 swing-twist 分解虽能提供物理一致的初值，但仍需学习式修正来处理软组织变形和锚点预测噪声。

### 锚点选择策略与数量

Table 6 的消融对比了三种锚点选择策略。**PCA-32**（从 SMPL 网格顶点通过主成分分析选取 32 个锚点）在 FreeMotion 上取得 105.1/113.9 mm 的全局关节/顶点误差，优于随机选取（Random-32: 108.2/117.5 mm）和手动选取（Manual-41: 106.8/115.4 mm）。PCA 选取策略在表征能力与计算效率间达到最优平衡——32 个锚点足以覆盖主要表面变形模式，同时保持轻量级计算开销。增加锚点数量至 50 个（Manual-50）在 HuMMan-Point 上仅带来边际增益（全局关节误差 96.4 vs 97.6 mm），验证了 32 个锚点的充分性。

### 精炼策略的详细对比

Table 9 对比了 PST 模块的四种精炼策略。残差偏移预测（Residual Offset）在 FreeMotion 上取得 105.1/113.9 mm 的全局关节/顶点误差，显著优于直接预测（Direct: 119.8/128.3 mm）、迭代精炼（Iterative: 112.4/121.5 mm）和注意力机制（Attention: 108.7/117.8 mm）。残差学习的优势在于：网络只需预测初始关节位置的小幅修正量，降低了优化难度，同时保持了与点云几何的局部对齐。

Table 10 对比了 SAE 模块的初始化和精炼策略。线性初始化+交叉注意力精炼的组合取得最优性能（全局顶点误差 113.9 mm），优于线性初始化+MLP 精炼（118.2 mm）和无初始化+交叉注意力（123.5 mm）。交叉注意力机制的有效性源于其能动态加权不同关节特征对锚点预测的贡献，而 MLP 的静态映射无法适应不同姿态下的几何变化。

### 鲁棒性极限测试

**遮挡鲁棒性**（Table 8）：在模拟点云移除实验中，即使 70% 点云被遮挡，SparkleMotion 的全局关节/顶点误差仍保持在 118.7/128.3 mm，角度误差为 18.43°。这一鲁棒性源于两阶段设计：几何初始化利用可见骨骼和锚点提供物理一致的初值，精炼网络在此基础上进行局部修正，而非从零开始推理全身姿态。当遮挡率达 90% 时，误差急剧上升（全局关节/顶点误差 178.2/186.5 mm），表明极端遮挡下可见几何信息不足仍是方法瓶颈。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_0blfYtdJES/figures/014_Table_8.jpg]]
*Table 8: Performance analysis under different occlusion ratios. Metrics are reported on a held-out test set with simulated occlusion*

**距离鲁棒性**（Table 7）：在 FreeMotion 数据集的不同捕捉距离下，性能随距离增加而退化。5-10m 距离内全局关节误差为 89.3 mm，10-20m 升至 105.1 mm（+17.7%），20-30m 升至 138.7 mm（+55.3%）。远距离下点云稀疏化导致语义分割精度下降，进而影响 PST 模块的关节定位和 SAE 模块的锚点初始化，这是当前方法的已知局限。

### 数据效率与跨域泛化

Table 11 展示了 Sparkle 表征的数据高效性。仅使用 50% 目标域训练数据（FreeMotion-OBJ）时，SparkleMotion 的 MPJPE 为 61.5 mm，已接近全量监督基线 LiveHPS++ 的 61.9 mm（使用 100% 数据）。使用 100% 数据时，SparkleMotion 的 MPJPE 进一步降至 55.2 mm。这一数据效率优势源于几何初始化提供的强归纳偏置——解析 swing-twist 分解无需从数据中学习基本运动学约束，使网络能专注于学习数据特定的非线性修正。

在跨数据集迁移实验中，从 FreeMotion 预训练后微调至 FreeMotion-OBJ，SparkleMotion 的 MPJPE 为 58.3 mm，优于从头训练的 LiveHPS++（68.9 mm），验证了 Sparkle 表征的跨域泛化能力。



## 定位与知识库关联

### 1. 与基线方法的关系

SparkleMotion 的核心贡献在于提出了一种新的中间表征 **Sparkle**，将人体状态显式解耦为内部运动学（骨骼关节）与外部几何（表面锚点）两个互补空间。这一设计直接回应了现有方法在表征学习上的根本权衡。

**基于原始点云的方法**，如 **VoteHMR** (Liu et al., 2021) 和 **PointHPS** (Cai et al., 2023)，直接从点云回归人体参数，保留了丰富的几何细节，但缺乏结构先验，导致对噪声、遮挡和深度歧义高度敏感。这在 Table 1 的 NoiseMotion 数据集上表现尤为明显：PointHPS 的全局顶点误差高达 88.4 mm，而 SparkleMotion 仅为 45.8 mm（降低约 48%）。

**基于骨架先验的方法**，如 **LiDARCap** (Li et al., 2022)、**LiveHPS** (Ren et al., 2024b) 及其增强版 **LiveHPS++** (Ren et al., 2024a)，通过直接回归骨骼关节位置来注入运动学约束。这类方法在常规场景下表现稳健，但在需要表面细节的场景中暴露了根本缺陷：仅依赖骨骼信息无法唯一确定绕骨轴的旋转（扭转歧义），这在近距离人体交互场景中尤为致命。Table 2 的数据提供了直接证据：在 Interhuman 数据集上，LiveHPS++ 的角度误差高达 18.47°，而 SparkleMotion 通过表面锚点提供的额外几何约束，将角度误差降至 6.75°，降幅达 63.5%。

**多视图方法**，如 **FreeCap** (Xue et al., 2025)，利用多视角融合来缓解遮挡问题，但本质上仍受限于表征能力。SparkleMotion 的多视图扩展（Figure 6）在 FreeMotion-MV 上以 9.61° 的角度误差优于 FreeCap 的 12.24°，表明 Sparkle 表征本身带来的增益独立于传感器配置。

### 2. 技术演进路径

从方法设计的因果链条看，SparkleMotion 沿着以下路径推进了该领域：

1.  **表征解耦**：将人体状态从单一表征（纯点云或纯骨架）推进到运动学-几何双空间联合表征。这是对现有方法“结构先验与几何细节不可兼得”困境的直接破解。

2.  **几何驱动初始化**：SSS 模块中的 swing-twist 解析分解（Equation 4-5）将强物理归纳偏置注入参数估计过程。这与现有方法依赖纯学习式初始化的范式形成对比——Table 5 的消融实验显示，移除几何初始化（w/o init）会使网络收敛至次优姿态，验证了解析先验对降低学习复杂度的关键作用。

3.  **语义分割引导的点对齐**：PST 模块的隐式语义分割与残差偏移学习（Section 3.1.1）将“从点云回归关节”的粗糙范式细化为“先分割、后对齐、再修正”的级联优化过程。Table 9 的详细消融表明，残差偏移策略优于直接预测、迭代优化和注意力机制等替代方案。

4.  **线性初始化 + 非线性精炼**：SAE 模块采用预计算的线性映射 $M_{J2A}$ 初始化表面锚点，再通过交叉注意力学习非线性修正。这种“解剖先验引导初始化、数据驱动精炼”的两阶段设计在 Table 10 中得到验证：跳过线性初始化导致锚点预测不稳定，而将交叉注意力替换为 MLP 精炼则降低了融合效果。

### 3. 适用边界与约束条件

尽管 SparkleMotion 在 11 个基准数据集上展现了优异的泛化能力，其适用边界可从以下维度界定：

**传感器模态**：该方法以点云为输入，覆盖 LiDAR 和深度相机两种主流传感器。Table 3 的跨传感器泛化实验（GTA-Human-Point 和 HuMMan-Point）表明，在源域训练的模型可直接泛化至目标传感器域，且仅需 50% 目标域数据微调即可达到与全量监督基线相当的性能（Table 11：MPJPE 61.5 vs LiveHPS++ 68.9）。但该方法不适用于纯 RGB 输入场景，需依赖深度信息。

**遮挡容忍度**：Table 8 的模拟遮挡实验给出了量化边界。在 50% 点云遮挡下，全局关节/顶点误差保持在 87.3/96.2 mm 的可用水平；当遮挡率升至 70% 时，误差增至 118.7/128.3 mm，性能退化明显但未崩溃；90% 遮挡下误差急剧恶化至 208.7/218.7 mm，表明该方法在极端遮挡下仍需要更鲁棒的补全机制。

**捕捉距离**：Table 7 显示，在 5-10m 距离下角度误差为 9.64°，10-20m 时升至 11.55°，20-30m 时进一步升至 13.37°。点云稀疏化随距离增加是性能退化的主因，远距离场景可能需要多帧时序融合来补偿空间信息的损失。

**多人场景**：该方法集成了 ByteTrack 用于多人跟踪（Table 12），在 FIFA 数据集上展现了实时多人动作捕捉能力。但近距离交互下的多人身份切换和严重交叉遮挡仍然是潜在挑战点。

**锚点数量与选择**：Table 6 的消融表明，PCA 选取 32 个锚点在表征能力与计算效率之间达到最优平衡。手动选取 41 个锚点虽在部分指标上略优，但缺乏可扩展性；随机选取则显著降低性能。锚点策略依赖于 SMPL 模型的顶点分布先验，迁移到其他人体模型时需重新校准。

### 4. 局限与开放问题

基于论文提供的实验证据和分析，可识别以下局限与开放方向：

**物理合理性约束的缺失**：Sparkle 表征虽注入了运动学先验（骨骼长度、关节连接关系），但未显式建模物理约束（如非穿透、力矩平衡、地面接触）。在严重遮挡或极端姿态下，恢复的网格可能出现物理上不合理的变形。引入物理仿真层作为后处理或端到端可微约束是一个值得探索的方向。

**时序一致性的利用不足**：当前方法的 PST 模块使用了双向 GRU 捕捉时序信息，但 SAE 和 SSS 模块主要逐帧处理。在点云瞬时缺失或严重噪声场景下，显式的时序平滑或运动先验（如恒定速度/加速度模型）可进一步提升鲁棒性。

**锚点语义的深层利用**：32 个表面锚点当前主要用于提供扭转约束和初始化。这些锚点是否可承载更丰富的语义信息（如服装形变、肌肉收缩、接触检测）仍是一个开放问题。

**极端姿态的泛化边界**：实验覆盖了足球、篮球等运动场景，但未系统评估在杂技、瑜伽等极端关节活动度下的表现。swing-twist 分解在欧拉角奇异点附近的数值稳定性需要进一步验证。

**计算效率的量化缺失**：论文声称“实时”性能，但未提供具体的推理延迟数据或与基线的效率对比。在资源受限的边缘设备上部署时，PST 的迭代优化和 SAE 的交叉注意力机制的计算开销需要量化评估。

**跨人体模型的迁移**：Sparkle 表征的构建依赖 SMPL 模型的运动学树和顶点分布。迁移到其他参数化人体模型（如 SMPL-X、GHUM）时，关节数量、锚点选取和线性映射矩阵均需重新设计，其迁移成本和性能保持率尚未被研究。



## 原文 PDF

![[paperPDFs/ICLR_2026/Sparkle_A_Robust_and_Versatile_Representation_for_Point_Cloud_based_Human_Motion_Capture.pdf]]
