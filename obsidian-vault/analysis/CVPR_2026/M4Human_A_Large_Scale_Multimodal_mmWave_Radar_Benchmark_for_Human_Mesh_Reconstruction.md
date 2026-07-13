---
title: "M4Human: A Large-Scale Multimodal mmWave Radar Benchmark for Human Mesh Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/M4Human_A_Large_Scale_Multimodal_mmWave_Radar_Benchmark_for_Human_Mesh_Reconstruction.pdf
project_link: "https://fanjunqiao.github.io/M4Human-site/"
code_link: "https://github.com/facebookresearch/detectron2"
aliases:
- RM
- M4Human
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 构建大规模、多模态、包含高精度动捕标注和原始RT与点云(RPC)的M4Human基准，为训练和评估雷达基HMR提供关键基础。
primary_logic: 高分辨率毫米波雷达的原始张量(RT)保留比处理后的点云(RPC)更丰富的空间上下文，结合大规模多样化的标注数据，可以训练出具有竞争力的雷达基HMR模型，缩小与视觉系统的性能差距，并在跨主体和跨动作场景中展现更好的泛化能力。
claims:
- M4Human包含661K帧，是此前最大数据集的9倍，支持50种多样动作和原始RT模态，提供高质量动捕网格标注。
- RT-Mesh在随机分割(S1)上实现90.9 mm MVE，在跨主体(S2)和跨动作(S3)上显著优于RPC基线（135.1 vs 140.8, 143.1 vs 147.8），表明RT模态更好的泛化性。
- 扩大训练数据规模一致提升跨主体和跨动作泛化：RT-Mesh在S2上MVE从25%数据的161.0降至100%数据的135.1，在S3上从174.9降至143.1。
- M4Human (S2 ALL) 上 MVE (mm) = RT-Mesh 135.1
---

# M4Human: A Large-Scale Multimodal mmWave Radar Benchmark for Human Mesh Reconstruction

> [!tip] 核心洞察
> 高分辨率毫米波雷达的原始张量(RT)保留比处理后的点云(RPC)更丰富的空间上下文，结合大规模多样化的标注数据，可以训练出具有竞争力的雷达基HMR模型，缩小与视觉系统的性能差距，并在跨主体和跨动作场景中展现更好的泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | M4Human：面向人体网格重建的大规模多模态毫米波雷达基准 |
| 英文题名 | M4Human: A Large-Scale Multimodal mmWave Radar Benchmark for Human Mesh Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.12378) · [Project](https://fanjunqiao.github.io/M4Human-site/) · [Code](https://github.com/facebookresearch/detectron2) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | RT-Mesh |
| Dataset | M4Human |

> [!tip] 效果简介
> - M4Human (S2 ALL) 上，MVE (mm) RT-Mesh 135.1 vs P4Transformer (RPC) 140.8 (-5.7)。
> - M4Human (S1 ALL) 上，MVE (mm) RT+RPC Fusion 84.3 vs P4Transformer (RPC) 90.4 (-6.1)。

## 概要

毫米波雷达因其隐私保护、光照不敏感等优势，被视为室内人体感知的关键传感器。然而，现有雷达人体网格重建（Human Mesh Reconstruction, HMR）研究长期受困于一个根本瓶颈：**数据集规模小、动作单一，且缺乏高质量的网格标注与原始雷达张量（Raw Tensor, RT）模态**。这严重限制了高保真雷达HMR方法的发展与评估。

针对这一瓶颈，本文提出了**M4Human**——一个大规模、多模态的毫米波雷达人体网格重建基准。其核心洞察在于：高分辨率毫米波雷达的原始张量保留了比处理后点云（Radar Point Cloud, RPC）更丰富的空间上下文信息，结合大规模多样化的标注数据，可以训练出具有竞争力的雷达基HMR模型，缩小与视觉系统的性能差距。

M4Human包含**661K帧**同步多模态数据（999个序列，约15.3小时），规模为此前最大数据集的**9倍**，覆盖**50种**从康复、健身到运动的多样化自由空间动作，并提供高精度光学动捕网格标注。该基准同时提供原始RT与RPC两种雷达模态，为系统研究不同雷达表示对HMR的影响提供了基础。

为建立性能参考，本文提出了**RT-Mesh**基线模型。该模型将RT张量重塑为2D鸟瞰图进行人体定位，再通过3D特征提取器与HMR头回归SMPL-X参数。实验揭示了几个关键发现：

1. **RT模态的泛化优势**：在跨主体（S2）和跨动作（S3）设置下，RT-Mesh的MVE（135.1 mm, 143.1 mm）显著优于RPC基线（140.8 mm, 147.8 mm），表明RT保留的丰富空间信息带来更好的泛化能力。

2. **数据规模的因果效应**：扩大训练数据一致提升跨主体和跨动作泛化性能——RT-Mesh在S2上MVE从25%数据的161.0 mm降至100%数据的135.1 mm。

3. **多模态融合的增益**：简单拼接RT与RPC特征即可在所有评估分割上优于任一单模态，在随机分割（S1）上MVE降至84.3 mm，进一步缩小与深度模态的差距。

在方法谱系中，RT-Mesh定位为基于原始RT张量的HMR基线，与基于RPC的**mmMesh**（LSTM架构）、**P4Transformer**（点云Transformer）以及从姿态估计改编的**RT-Pose**、**RETR**等方法形成系统对比。所有方法共享统一的HMR预测头与网格损失，确保公平比较。

尽管M4Human显著推进了雷达HMR的研究基础，但当前方法仍存在明显局限：对复杂动力学动作（如侧弓步、拳击）的重建误差较大；传感器最优感知范围限于2.0–4.0米；跨主体和跨动作的泛化性能仍显著低于随机分割。这些差距指明了未来的研究方向——引入更强的运动先验、更先进的时序建模与多模态融合机制。



### 毫米波雷达人体感知的兴起

人体网格重建（Human Mesh Reconstruction, HMR）是计算机视觉与无线感知领域的核心挑战，其目标是从传感器数据中恢复精细的三维人体表面模型。传统方案高度依赖RGB摄像头，但在遮挡、光照变化和隐私敏感场景中面临根本性局限。毫米波雷达作为一种隐私保护、抗光照干扰且能穿透部分遮挡的感知模态，近年来在人体姿态估计（HPE）和动作识别中展现出独特优势。

然而，雷达基人体网格重建的发展远落后于视觉方案。其根本瓶颈并非算法设计，而是**高质量标注数据的严重匮乏**。

### 现有雷达数据集的三大缺口

截至本文工作，公开可用的雷达人体感知数据集普遍存在以下结构性缺陷：

**1. 规模与多样性不足。**
现有数据集通常仅包含数十个序列、数万帧数据，动作类型局限于原地挥手、行走等简单日常动作。以当时最大的雷达HMR数据集mmBody为例，其有效雷达点云（RPC）比率低，且缺乏自由空间中的复杂运动轨迹。这种数据贫乏直接制约了深度学习模型的训练效果和泛化边界。

**2. 标注粒度粗糙。**
大多数数据集仅提供稀疏骨架关节点标注，缺乏高保真的三维网格真值。稀疏骨架无法完整刻画人体表面形变，难以支撑网格重建任务。部分数据集虽提供网格标注，但多通过拟合视觉系统结果间接获得，精度受限。

**3. 模态信息不完整。**
商用毫米波雷达通常输出两种互补表示：原始雷达张量（Raw Tensor, RT）和经CFAR滤波后的雷达点云（Radar Point Cloud, RPC）。RT保留了完整的3D空间强度分布，蕴含丰富的上下文信息；RPC则仅保留超过自适应阈值的显著反射点，信息损失严重。然而，几乎所有现有数据集仅公开RPC，剥夺了研究者利用原始RT进行高保真重建的可能性。

### 核心动机：从数据侧破局

上述缺口揭示了一个清晰的因果链条：**缺乏大规模、多模态且带有高精度网格标注的雷达数据集 → 雷达HMR模型训练不充分、评估不可靠 → 雷达基方案与视觉系统的性能鸿沟持续存在。**

M4Human的构建动机正是从数据侧切断这一链条。通过设计多模态同步采集平台，融合高精度光学动捕系统（marker-based MoCap）与毫米波雷达，本文构建了一个包含66.1万帧、999个序列、超过15小时同步数据的基准。该数据集覆盖康复、健身、运动等50种多样化自由空间动作，同时提供原始RT与RPC两种雷达模态，以及由动捕系统导出的高质量SMPL-X网格真值。这一数据基础为训练和公平评估雷达HMR模型提供了此前不存在的关键条件，也为探索RT模态的独特价值打开了可能性。



## 核心方法与创新机理

M4Human 的核心创新体现在两个紧密耦合的层面：**基准本身的设计突破**与**基于该基准揭示的模态-规模-泛化因果链条**。

### 1. 基准设计的结构性创新

M4Human 并非简单扩大现有数据集，而是针对雷达人体网格重建（HMR）的瓶颈进行了三项结构性改造：

**（1）模态完备性：首次同时提供原始雷达张量（RT）与点云（RPC）**
此前雷达人体感知数据集仅提供处理后的稀疏点云（RPC），丢失了原始信号中的空间上下文。M4Human 同时保留两种模态：
- **RT**：通过 FFT 处理时域信号后映射到笛卡尔坐标系（X-Y-Z）的 3D 强度体积，保留完整空间信息。
- **RPC**：从 RT 经 CFAR 自适应阈值滤波得到，仅保留显著反射点。
这一设计使得**系统性地比较两种模态对 HMR 的贡献**成为可能——这是此前工作无法完成的实验。

**（2）标注质量：高精度动捕驱动的网格真值**
M4Human 采用基于标记的光学动捕系统（marker-based MoCap）获取 SMPL-X 参数真值，而非依赖稀疏骨架或视觉估计。这为训练和评估高保真网格重建提供了可靠的监督信号。对比此前数据集（如 mmBody）仅提供稀疏骨架标注，M4Human 的标注粒度从“关节级”跃升至“顶点级”。

**（3）规模与多样性：661K 帧 × 50 种动作的泛化压力测试**
M4Human 包含 999 个序列、约 661K 帧同步多模态数据（约 15.3 小时），是此前最大雷达人体数据集的 **9 倍**。动作覆盖康复、健身、运动等自由空间动态，远超现有数据集的原地简单动作。这一设计直接支撑了跨主体（S2）和跨动作（S3）泛化评估协议，将雷达 HMR 从“见过的主体/动作”推向“未见过的主体/动作”。

### 2. RT-Mesh 的架构创新：从 3D 张量到高效两阶段 HMR

RT-Mesh 是首个专门为原始 RT 模态设计的 HMR 基线，其架构创新在于**将高维雷达张量的计算瓶颈转化为两阶段级联策略**：

| 阶段 | 操作 | 创新点 |
|------|------|--------|
| **BEV 2D 定位** | 将 4D RT 张量 $X_{\mathrm{RT}} \in \mathbb{R}^{T \times X \times Y \times Z}$ 沿 Z 轴和 T 轴堆叠为 2D 鸟瞰图，用 2D 卷积 + 自注意力定位人体中心 | 将 3D 空间定位降维为 2D 问题，大幅降低搜索空间 |
| **3D RoI 裁剪 + 回归** | 基于预测中心裁剪固定大小 3D 区域，用 3D 卷积 + Transformer 提取特征，回归 SMPL-X 参数 $(\alpha, \beta, \tau, \theta)$ | 仅在局部区域进行高开销的 3D 计算，实现 2.74 ms 延迟和 2.6 GFLOPs |

这一设计与基于 RPC 的方法（如 P4Transformer、mmMesh）形成互补：RPC 方法依赖点云稀疏性，而 RT-Mesh 利用 RT 的密集空间上下文，在跨主体和跨动作场景中展现出更好的泛化能力。

### 3. 揭示的因果链条：模态 × 规模 → 泛化

M4Human 的核心洞察并非单个模型或数据集，而是通过系统性实验揭示的因果机制：

**（1）RT 模态保留更丰富的空间上下文 → 更好的泛化**
在跨主体（S2）和跨动作（S3）设置下，RT-Mesh 的 MVE 显著低于 RPC 基线（S2: 135.1 vs 140.8 mm；S3: 143.1 vs 147.8 mm）。这表明 RT 中未被 CFAR 过滤的弱反射区域携带了对泛化至关重要的上下文信息。

**（2）数据规模是泛化的关键杠杆**
消融实验（Figure 5）显示，将训练数据从 25% 扩大到 100%，RT-Mesh 在 S2 上 MVE 从 161.0 降至 135.1 mm，在 S3 上从 174.9 降至 143.1 mm——**规模收益在跨场景设置下尤为显著**，且未见饱和趋势。

**（3）多模态融合进一步缩小与视觉系统的差距**
将 RT 与 RPC 特征沿通道拼接融合后，在随机分割（S1）上 MVE 降至 84.3 mm，优于单独使用任一雷达模态（RT: 90.9 mm, RPC: 90.4 mm），且在所有三个评估分割上一致提升。这验证了两种雷达模态的信息互补性。

### 4. 与 baseline 的差异定位

相较于现有雷达 HMR 基线：
- **mmMesh** 依赖 LSTM 处理 RPC，受限于点云稀疏性和序列建模能力；
- **P4Transformer** 虽引入 Transformer，但仍以 RPC 为输入，丢失空间上下文；
- **RT-Pose / RETR** 虽使用 RT 模态，但面向姿态估计（HPE）设计，非 HMR。

RT-Mesh 的 changed slot 在于：**首次将 RT 模态的密集空间信息与高效两阶段 HMR 架构结合**，在保持低延迟的同时，系统性地揭示了 RT 模态在泛化场景下的优势——这一发现本身是 M4Human 基准设计的直接产物。



M4Human 基准的工作流围绕“多模态感知采集—高精度标注生成—基准模型训练与评估”三条主线展开，其核心目标是构建一个大规模、多模态的毫米波雷达人体网格重建（HMR）数据集，并提供可复现的评估协议与基线模型。

### 1. 感知与标注流水线

系统的感知硬件由三部分组成：高分辨率毫米波雷达、RGB-D 相机和基于标记点的高精度光学运动捕捉（MoCap）系统（Vicon）。三者在空间和时间上均经过严格标定与同步，以确保多模态数据与人体网格真值之间的精确对齐（Figure 3）。

![[assets/figures/papers/paper_list_l974_https_arxiv_org_abs_2512_12378/figures/004_Figure_3.jpg]]
*Figure 3: Overview of the system setup. M4Human designs a multimodal sensing platform with high-precision marker-based MoCap system. Appropriate calibration and synchronization workflow are designed for accurate alignment between modalities and annotations*

- **雷达模态生成**：毫米波雷达首先通过 FFT 处理时域信号，沿距离、方位角和俯仰角三个维度生成三维强度体，再映射到笛卡尔坐标系（X-Y-Z），得到原始雷达张量（RT）。随后，RT 通过 CFAR 自适应阈值检测，仅保留显著反射点，形成雷达点云（RPC）。因此，M4Human 同时提供 RT 和 RPC 两种互补的雷达模态。
- **视觉模态对齐**：RGB-D 相机提供彩色图像与深度图，用于辅助可视化和多模态融合实验。
- **真值标注**：Vicon 系统采集 42 个标记点的三维轨迹，通过逆运动学求解得到 SMPL-X 参数（姿态、体型、全局平移等），作为高精度网格真值。相机与 Vicon 之间的外参通过 PnP 算法估计，变换关系为 $\mathbf{P}^C = \mathbf{R}_{CV} \mathbf{P}^V + \mathbf{t}_{CV}$。

最终，数据集包含 999 个有效序列、约 661K 帧同步多模态数据、超过 15 小时的运动捕捉，覆盖 50 种多样化动作（康复、健身、运动等），远超此前最大的雷达人体感知数据集。

### 2. 基准模型 RT-Mesh 的流水线

论文提出了一个简单高效的 RT 基线模型 **RT-Mesh**，专为原始雷达张量设计，其整体架构遵循“定位—裁剪—回归”的两阶段流程（Figure 4）。

![[assets/figures/papers/paper_list_l974_https_arxiv_org_abs_2512_12378/figures/005_Figure_4.jpg]]
*Figure 4: Overview of the proposed RT-Mesh baseline. Given a 3D radar tensor (RT), RT-Mesh first reshapes it into a 2D BEV representation. A lightweight 2D BEV Transformer, combining 2D convolution and self-attention, performs efficient 2D human localization (ˆx, yˆ) under the supervision of*

| 模块 | 功能 | 关键设计 |
|------|------|----------|
| **BEV 2D 定位** | 从 4D 雷达张量中定位人体中心 | 将 RT 沿 Z 和 T 轴堆叠为 2D 鸟瞰图（BEV），使用 2D 卷积与自注意力预测人体中心 $(\hat{x}, \hat{y})$ |
| **3D RoI 裁剪** | 降低后续计算量 | 基于预测的 2D 中心，裁剪固定大小的 3D 感兴趣区域 |
| **3D 特征提取器** | 提取局部 3D 特征 | 使用 3D 卷积与 Transformer 处理裁剪后的 RT 张量 |
| **HMR 预测头** | 回归 SMPL-X 参数 | 输出根旋转 $\alpha$、体型 $\beta$、全局平移 $\tau$、身体姿态 $\theta$ 和性别 |

**输入**：堆叠 $T=4$ 帧的 4D 雷达张量 $X_{\mathrm{RT}} \in \mathbb{R}^{T \times X \times Y \times Z}$，空间分辨率为 $X=121, Y=111, Z=31$。  
**输出**：SMPL-X 参数 $(\alpha, \beta, \tau, \theta)$，可进一步通过 SMPL-X 模型解码为 3D 人体网格。  
**训练损失**：联合优化 2D BEV 定位损失和 3D 网格回归损失 $\mathcal{L} = \lambda_{2D}\mathcal{L}_{2D} + \lambda_{\mathrm{mesh}}\mathcal{L}_{\mathrm{mesh}}$，其中网格损失 $\mathcal{L}_{\mathrm{mesh}}$ 包含姿态旋转、根旋转、体型、平移和性别分类的加权项。

### 3. 多模态融合流水线

为探索雷达模态间的互补性，论文进一步设计了简单的多模态融合方案：将 RT 和 RPC 的编码器特征沿通道维度拼接 $f_{\mathrm{fuse}} = [\boldsymbol{f}^{(m_1)} \boldsymbol{f}^{(m_2)}] \in \mathbb{R}^{2 d_m}$，再送入统一的 HMR 预测头。实验表明，这种简单融合在所有三个评估分割上均优于单独使用任一雷达模态，进一步缩小了与深度模态的性能差距。

### 4. 关键设计决策与瓶颈

RT-Mesh 的核心设计动机在于：原始 RT 保留了比处理后的 RPC 更丰富的空间上下文信息。这一假设在跨主体（S2）和跨动作（S3）泛化实验中得到了验证——RT-Mesh 的 MVE 分别为 135.1 mm 和 143.1 mm，显著优于 RPC 基线的 140.8 mm 和 147.8 mm。然而，当前流水线仍存在明显瓶颈：雷达缺乏视觉外观线索导致体型预测不稳定，对复杂动力学动作（如侧弓步、拳击）的重建误差较大，且最佳感知距离局限于 2.0–4.0 米。

### 补充图表

![[assets/figures/papers/paper_list_l974_https_arxiv_org_abs_2512_12378/figures/012_Figure_8.jpg]]
*Figure 8: (a) A conventional file-system dataloader repeatedly performs file-name lookup and disk I/O on large .mat files (e.g., RT), which quickly becomes a bottleneck at scale. (b) Our LMDB-based system converts all data into a single contiguous byte stream stored in a memory-mapped database, indexed by the key*



### RT-Mesh 两阶段基线架构

RT-Mesh 采用两阶段结构（Figure 4），专为原始雷达张量（RT）模态设计。第一阶段在压缩的 2D 鸟瞰图（BEV）上高效定位人体前景区域，第二阶段在局部 3D RT 裁剪体上回归最终的 SMPL-X 参数。该设计兼顾了计算效率与重建精度，单样本延迟仅 2.74 ms，计算量 2.6 GFLOPs。

#### 阶段一：BEV 2D 定位

给定堆叠 $T=4$ 帧的 4D 雷达张量：

$$X_{\mathrm{RT}} \in \mathbb{R}^{T \times X \times Y \times Z}$$

其中空间分辨率 $X=121$, $Y=111$, $Z=31$。将 $X_{\mathrm{RT}}$ 沿 Z 轴（高度）和 T 轴（时间）堆叠，重塑为 2D BEV 表示。随后，一个轻量级 2D BEV Transformer——结合 2D 卷积与自注意力——在 BEV 图上预测人体中心坐标 $(\hat{x}, \hat{y})$，完成杂波环境下的前景定位。

#### 阶段二：3D RoI 裁剪与特征提取

基于预测的 2D 中心，从原始 4D 张量中裁剪固定大小的 3D 感兴趣区域（RoI），大幅降低后续计算量。裁剪后的局部 3D 张量送入 3D 特征提取器，该模块使用 3D 卷积与 Transformer 提取局部时空特征。

#### 阶段三：HMR 预测头

提取的 3D 特征最终送入统一的 HMR 预测头，回归 SMPL-X 参数：

$$(\alpha, \beta, \tau, \theta)$$

其中 $\alpha$ 为根旋转（轴角表示），$\beta$ 为体型参数，$\tau$ 为全局平移，$\theta$ 为身体姿态参数。头部同时输出性别预测 $g$。

### 训练损失函数

总训练损失联合优化 2D 定位与 3D 网格回归：

$$\mathcal{L} = \lambda_{2D}\mathcal{L}_{2D} + \lambda_{\mathrm{mesh}}\mathcal{L}_{\mathrm{mesh}}$$

其中网格回归损失 $\mathcal{L}_{\mathrm{mesh}}$ 对 SMPL-X 各参数分量施加监督：

$$\mathcal{L}_{\mathrm{mesh}} = \lambda_{\theta}\mathcal{L}_{\mathrm{rot}}(\hat{\theta},\theta) + \lambda_{\alpha}\mathcal{L}_{\mathrm{rot}}(\hat{\alpha},\alpha) + \lambda_{\beta}\|\hat{\beta}-\beta\|_2^2 + \lambda_{\tau}\|\hat{\tau}-\tau\|_1 + \lambda_{g}\mathrm{BCE}(\hat{g},g)$$

各分量含义：
- $\mathcal{L}_{\mathrm{rot}}$：姿态/根旋转的旋转损失
- $\|\hat{\beta}-\beta\|_2^2$：体型的 $L_2$ 范数损失
- $\|\hat{\tau}-\tau\|_1$：全局平移的 $L_1$ 范数损失
- $\mathrm{BCE}(\hat{g},g)$：性别的二值交叉熵损失

### 多模态特征融合

对于 RT 与 RPC 等多模态融合实验，采用通道拼接策略。两个模态的编码器特征 $f^{(m_1)}$ 和 $f^{(m_2)}$ 沿通道维度拼接：

$$f_{\mathrm{fuse}} = [\boldsymbol{f}^{(m_1)} \boldsymbol{f}^{(m_2)}] \in \mathbb{R}^{2 d_m}$$

拼接后特征维度翻倍，直接送入共享的 HMR 预测头进行参数回归。该简单融合策略在实验中已展现出对单模态的显著提升（Table 3），但更复杂的注意力融合或跨模态 Transformer 机制是否带来额外增益，仍是开放问题。

### 雷达模态预处理

M4Human 提供两种互补的雷达模态，均源自同一硬件采集的时域信号：

- **RT（原始雷达张量）**：对时域信号沿距离、方位角、俯仰角三个维度进行 FFT 处理，得到 3D 强度体积，再映射到笛卡尔坐标系 $(X, Y, Z)$。RT 保留了完整的空间上下文信息。
- **RPC（雷达点云）**：从 RT 通过 CFAR（恒虚警率）算法导出，仅保留超过自适应阈值的显著反射点。RPC 稀疏但噪声更低，适合点云基方法。

两种模态的互补性为多模态融合提供了基础：RT 的密集空间信息有助于泛化，RPC 的稀疏结构则利于高效处理。



## 实验与关键发现

### 评估协议与基准设定

M4Human 基准定义了三种数据划分（S1 随机分割、S2 跨主体、S3 跨动作）和四种动作协议（P1 原地动作、P2 坐姿原地、P3 非原地动态、ALL 全部），以全面评估雷达人体网格重建（HMR）的性能。主要指标为平均顶点误差（MVE，mm），辅以 Procrustes 对齐后的 PA-MVE、MPJPE 和 PA-MPJPE。

### 雷达 HMR 主结果

**Table 2** 汇总了基于雷达点云（RPC）和原始张量（RT）模态的 SOTA 方法在 M4Human 上的表现。核心发现如下：

- **RT-Mesh 在随机分割（S1）下达到 90.9 mm MVE**，在 S2 和 S3 上分别为 135.1 mm 和 143.1 mm，在所有 RT 方法中取得最优或竞争性结果。
- **RT 模态在泛化性上显著优于 RPC**：在 S2 上 RT-Mesh（135.1）对比 P4Transformer-RPC（140.8）降低 5.7 mm；在 S3 上 RT-Mesh（143.1）对比 P4Transformer-RPC（147.8）降低 4.7 mm。这验证了核心洞察：原始张量保留的更丰富空间上下文带来更好的跨主体和跨动作泛化能力。
- **非原地动态动作（P3）仍是主要难点**：RT-Mesh 在 S1/P3 上 MVE 为 121.7 mm，显著高于原地动作的 72.4 mm（S1/P1），表明复杂动力学动作对雷达 HMR 构成严峻挑战。
- **计算效率**：RT-Mesh 仅需 2.74 ms 延迟和 2.6 GFLOPs，远低于基于点云的 Transformer 方法（如 P4Transformer 的 113 GFLOPs），适合实时应用。

### 数据规模消融实验

**Figure 5** 揭示了训练数据规模对泛化能力的关键影响：

- 将训练数据从 25% 逐步增加到 100%，RT-Mesh 在 S2 上的 MVE 从 161.0 mm 持续下降至 135.1 mm（降幅 25.9 mm），在 S3 上从 174.9 mm 降至 143.1 mm（降幅 31.8 mm）。
- 这一单调改善趋势表明，**大规模多样化数据是提升雷达 HMR 跨主体和跨动作泛化的关键杠杆**，M4Human 的 661K 帧规模为此提供了必要基础。

### 多模态融合实验

**Table 3** 对比了单模态与多模态融合的性能：

- **RT+RPC 融合在全部三个划分上均优于任一单雷达模态**：S1 上 MVE 为 84.3 mm，比单独 RPC（90.4 mm）和单独 RT（90.9 mm）分别降低 6.1 mm 和 6.6 mm。
- 融合采用简单通道拼接策略（$f_{\text{fuse}} = [\boldsymbol{f}^{(m_1)} \boldsymbol{f}^{(m_2)}] \in \mathbb{R}^{2 d_m}$），已能带来一致增益，暗示更先进的融合机制（如注意力融合、门控）可能存在更大提升空间。
- **深度模态（Depth）仍保持绝对领先**：深度单模态在 S1 上 MVE 为 73.5 mm，RT+RPC 融合（84.3 mm）仍有 10.8 mm 差距，但融合使差距从单独 RT 的 17.4 mm 缩小至 10.8 mm。

### 下游动作识别基准

**Table 4** 展示了基于雷达预测骨架的下游动作识别（50 类）结果：

- 使用 GT 骨架时，AGCN 在 S1 上达到 97.8% Top-1 准确率，验证了标注质量和动作集的合理性。
- 使用 RT 预测骨架时，S1 上 Top-1 准确率为 83.0%（AGCN），S2 跨主体下降至 64.1%，反映出 HMR 误差向高层语义任务的传播效应。

### 失败模式与局限性分析

1. **复杂动力学动作**：侧弓步、拳击等非原地动作的 MVE 显著偏高（P3 协议下 121.7 mm vs. P1 的 72.4 mm），雷达信号对快速肢体运动的时空分辨率不足以精确捕捉末端关节。
2. **体型预测不稳定**：雷达缺乏视觉外观线索，导致身体形状参数 $\beta$ 的回归方差较大，预测网格在体型维度上与真值存在系统性偏差。
3. **感知距离敏感**：最佳重建精度集中在 2.0–4.0 m 范围，近距离（<2 m）因多径反射干扰、远距离（>4 m）因信号衰减导致性能下降明显，限制了实际部署灵活性。
4. **跨主体泛化瓶颈**：尽管 RT 模态优于 RPC，S2 上 135.1 mm 的 MVE 仍远高于 S1 的 90.9 mm，说明模型对未见主体的体型和运动模式泛化能力有待加强，需要更强的运动先验或数据增强策略。

### 关键图表结论

- **Table 1**：M4Human 以 661K 帧、50 种动作、双雷达模态（RT+RPC）和高精度动捕网格标注，在规模、多样性和标注粒度上全面超越此前最大的 mmBody 数据集。
- **Table 6**（完整结果）：所有方法在 S1→S2→S3 上性能递减，RT 方法在泛化性上一致优于 RPC 方法，但整体仍显著弱于深度模态，指明了未来改进方向。
- **Figure 10**：可视化对比显示，RT+RPC 融合预测的网格与真值重叠度明显高于单模态，尤其在四肢末端和躯干旋转等细节上改善显著。

![[assets/figures/papers/paper_list_l974_https_arxiv_org_abs_2512_12378/figures/002_Table_1.jpg]]
*Table 1: Comparison of M4Human with prior datasets († denotes non-public data). Overall, M4Human is the largest RF-based dataset with multi-granularity motion annotations. Modalities: It provides both raw radar tensors (RT) and filtered radar point clouds (RPC) for high-fidelity HMR. Annotations: Human body annotations are obtained with a high-precision marker-based MoCap system (* denotes pseudo-GTs from RGB(D)). Diversity: It extends beyond simple in-place activities to complex, non-in-place rehabilitation and sports*

![[assets/figures/papers/paper_list_l974_https_arxiv_org_abs_2512_12378/figures/014_Table_6.jpg]]
*Table 6: Radar-based HMR results on M4Human using state-of-the-art indoor human sensing HMR/HPE models. All methods are evaluated on the S1, S2, and S3 splits under four protocols: P1 In-Place (IP), P2 Sit-In-Place (SIP), P3 Non-In-Place (NIP), and ALL (all actions)*

![[assets/figures/papers/paper_list_l974_https_arxiv_org_abs_2512_12378/figures/016_Figure_10.jpg]]
*Figure 10: Visualization of single-modality predictions and multi-modal fusion. Predicted meshes are shown in orange and ground truth in blue; higher overlap indicates higher accuracy. The performance gap between line-of-sight (LoS) RGB-D and radio-frequency (RF) modalities is smaller than expected, thanks to the high-resolution radar in M4Human, making radar-based HMR feasible. Notably, RGB-only HMR struggles with accurate depth estimation, leading to larger reconstruction errors*

### 补充图表

![[assets/figures/papers/paper_list_l974_https_arxiv_org_abs_2512_12378/figures/006_Table_2.jpg]]
*Table 2: Performance of SOTA radar-based HMR using RPC and RT modalities. The mean vertex error (MVE) (mm) is recorded for all protocols and splits, lower the better. We also include the single-sample Latency (Lat.) and GFLOPs for comparing model efficiency*

![[assets/figures/papers/paper_list_l974_https_arxiv_org_abs_2512_12378/figures/008_Table_3.jpg]]
*Table 3: Performance of different single modalities and multi-modality fusion under protocol ALL and 3 different splits. All four metrics are reported to reflect the advantages of different modalities, lower the better*

![[assets/figures/papers/paper_list_l974_https_arxiv_org_abs_2512_12378/figures/007_Figure_5.jpg]]
*Figure 5: Impact of the training dataset size on radar-based HMR. Larger dataset consistently improves performance on S2 (crosssubject) and S3 (cross-action) across all evaluation metrics*

![[assets/figures/papers/paper_list_l974_https_arxiv_org_abs_2512_12378/figures/010_Table_4.jpg]]
*Table 4: Benchmark on downstream skeleton-based human action recognition (HAR) out of 50 actions. We show the Top-1 and Top-5 accuracy (%) using GT skeletons on S1, radar tensor (RT) predicted skeletons on S1 and S2*

![[assets/figures/papers/paper_list_l974_https_arxiv_org_abs_2512_12378/figures/009_Figure_6.jpg]]
*Figure 6: Visualization of (left) RT-based HMR under challenging (P3) non-in-place actions, and (right) comparison between RPC and RT predicted meshes. The proposed RT-Mesh can simultaneously track and reconstruct 3D human meshes during complex sports motions. In contrast, RPC-based prediction may fail when points are missing for certain body parts*

![[assets/figures/papers/paper_list_l974_https_arxiv_org_abs_2512_12378/figures/019_Figure_13.jpg]]
*Figure 13: Mean Vertex Error (MVE) across different action types. Dynamic non-in-place actions exhibit higher MVE, highlighting their increased difficulty and suggesting the need for more advanced motion modeling and stronger prior knowledge*



## 定位与知识库关联

### 1. 在雷达人体感知谱系中的位置

M4Human 及其基线 RT-Mesh 处于 **毫米波雷达人体感知从稀疏骨架估计向高保真网格重建跃迁** 的关键节点。此前雷达人体感知数据集（如 mmBody）主要面向粗粒度人体姿态估计（HPE），仅提供稀疏骨架标注，且动作以原地日常活动为主。M4Human 首次将雷达模态与 SMPL-X 参数化网格标注规模化对齐，填补了“雷达→密集三维表面”的数据空白。

在方法层面，RT-Mesh 的设计思路与视觉 HMR 中的两阶段范式（检测→回归）一脉相承，但针对雷达张量的四维结构（T×X×Y×Z）做了专门适配：
- **BEV 2D 定位** 将 4D 张量沿 Z 轴和 T 轴折叠为 2D 鸟瞰图，利用 2D 卷积与自注意力定位人体中心——这一策略借鉴了自动驾驶中 BEV 感知的思想，但目标从多目标检测变为单人体中心定位。
- **3D RoI 裁剪 + 3D 特征提取** 则类似点云目标检测中的两阶段 RoI 池化思路，在降低计算量的同时保留局部空间上下文。
- **HMR 预测头** 直接回归 SMPL-X 参数 $(\alpha, \beta, \tau, \theta)$，与视觉 HMR 的主流参数化回归方法一致。

### 2. 与同期基线的对比关系

论文在 M4Human 基准上系统比较了四类方法，构成雷达 HMR 的方法谱系：

| 方法 | 输入模态 | 核心架构 | 在谱系中的角色 |
|------|----------|----------|----------------|
| **mmMesh** | RPC | LSTM 时序建模 | RPC 基 HMR 的早期代表，验证点云序列到网格的可行性 |
| **P4Transformer** | RPC / Depth | Transformer 点云编码 | 点云 HMR 的 SOTA，作为 RPC 模态的强基线 |
| **RT-Pose** | RT | 3D CNN | 从 RT 姿态估计改编为 HMR，验证 3D 卷积在 RT 上的有效性 |
| **RETR** | RT | 多视图 Transformer | 从 RT 姿态估计改编，验证多视图注意力在 RT 上的潜力 |
| **RT-Mesh** (本文) | RT | 两阶段 BEV + 3D CNN/Transformer | 首个专为 RT 模态设计的 HMR 基线，兼顾效率与精度 |

RT-Mesh 的核心区分点在于 **显式的两阶段设计**：先 2D 定位再 3D 回归，使其在效率上显著优于直接处理全量 3D 张量的方法（2.74 ms 延迟，2.6 GFLOPs）。这一设计选择反映了对雷达数据特性的洞察——RT 张量虽包含丰富空间信息，但大部分体素为背景，两阶段裁剪可大幅压缩无效计算。

### 3. 适用边界

**场景边界**：
- **动作类型**：对原地动作（In-Place）重建精度最高（RT-Mesh 在 S1 上达 72.4 mm MVE），对非原地动态动作（如侧弓步、拳击）误差显著增大，表明当前方法对复杂动力学的建模能力有限。
- **感知距离**：最佳重建精度在 2.0–4.0 米范围内，近距离（<2m）因雷达近场效应和远距离（>4m）因信号衰减均导致性能下降，限制了实际部署的灵活空间。
- **主体泛化**：跨主体（S2）性能（135.1 mm MVE）显著弱于随机分割（S1，90.9 mm），说明模型对未见主体的体型和运动模式泛化不足。

**模态边界**：
- RT 模态保留更丰富的空间上下文，在跨主体和跨动作设置下泛化性优于 RPC（S2: 135.1 vs 140.8；S3: 143.1 vs 147.8），但其缺乏视觉外观线索，导致身体形状参数 $\beta$ 的预测不稳定。
- 融合 RT+RPC 可进一步缩小与深度模态的差距（S1 ALL: 84.3 vs 深度 90.4），但简单拼接融合的增益有限，更先进的跨模态融合机制仍是开放问题。

### 4. 局限性与开放问题

**已确认的局限**：
1. **形状估计不稳定**：雷达数据缺乏 RGB/深度等视觉外观信息，SMPL-X 的体型参数 $\beta$ 难以从纯几何反射中可靠推断。
2. **复杂动作误差大**：非原地动态动作（P3 协议）的 MVE 偏高，需要更强的运动先验来约束时序姿态序列。
3. **感知距离受限**：有效范围集中在 2–4 米，近场和远场性能下降明显，限制了实际应用场景的灵活性。
4. **跨域泛化不足**：跨主体和跨动作设置下性能显著低于随机分割，模型对训练分布外的运动模式适应能力有限。

**开放问题**：
- **运动先验引入**：能否引入预训练的人体运动生成模型（如 VAE 或扩散模型）作为运动先验，约束复杂动作下的时序姿态一致性？
- **多模态融合深化**：注意力融合、门控机制或跨模态 Transformer 相较于简单拼接能带来多少额外增益？特别是在形状估计和远距离场景下。
- **时序建模扩展**：当前 RT-Mesh 仅堆叠 4 帧历史，更长的时序窗口或显式运动轨迹建模能否提升复杂动作的重建精度和时间一致性？
- **感知范围扩展**：是否可通过超分辨率处理或多尺度特征提取来扩展雷达的有效感知距离，使其覆盖更广的室内空间？



## 原文 PDF

![[paperPDFs/CVPR_2026/M4Human_A_Large_Scale_Multimodal_mmWave_Radar_Benchmark_for_Human_Mesh_Reconstruction.pdf]]
