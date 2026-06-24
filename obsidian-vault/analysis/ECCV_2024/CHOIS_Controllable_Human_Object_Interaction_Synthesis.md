---
title: "CHOIS: Controllable Human-Object Interaction Synthesis"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/CHOIS_Controllable_Human_Object_Interaction_Synthesis.pdf
aliases:
- CHOIS
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 物体几何损失（Object Geometry Loss）和基于重构引导的接触约束项（手-物、脚-地、物体-地面）
primary_logic: 将稀疏物体路标点与语言描述共同作为扩散模型的生成条件，在训练时引入物体几何损失增强路标点匹配，在采样时施加解析接触引导函数来强制执行物理接触约束，能够大幅提升人机交互动作的同步性、真实感和条件遵循度。
claims:
- 引入物体几何损失显著提升了路标点条件匹配指标。
- 在推理时添加引导项能够获得更优的接触精度、更少的手-物穿透以及更少的脚浮空现象。
- CHOIS在FullBodyManipulation数据集上的脚滑动和FID指标均优于基线方法。
- FullBodyManipulation 上 Foot Sliding (FS) ↓ = 0.35
---

# CHOIS: Controllable Human-Object Interaction Synthesis

> [!tip] 核心洞察
> 将稀疏物体路标点与语言描述共同作为扩散模型的生成条件，在训练时引入物体几何损失增强路标点匹配，在采样时施加解析接触引导函数来强制执行物理接触约束，能够大幅提升人机交互动作的同步性、真实感和条件遵循度。

| 字段 | 内容 |
|------|------|
| 中文题名 | CHOIS：可控人机交互合成 |
| 英文题名 | CHOIS: Controllable Human-Object Interaction Synthesis |
| 会议/期刊 | ECCV 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | CHOIS |
| Dataset | FullBodyManipulation, 3D-FUTURE |

> [!tip] 效果简介
> - FullBodyManipulation 上，Foot Sliding (FS) ↓ 0.35 vs N/A (低于基线)；FID ↓ 0.69 vs N/A (低于基线)。
> - 3D-FUTURE 上，Foot Sliding (FS) ↓ 0.38 vs N/A (低于基线)；FID ↓ 1.60 vs N/A (低于基线)。

## 概述

合成逼真的人-物交互（Human-Object Interaction, HOI）运动是计算机视觉和图形学的核心挑战。其根本瓶颈在于：**普通条件扩散模型无法保证生成的物体运动与用户给定的稀疏路标点精确对齐，同时也难以维持手-物接触和脚-地接触的物理真实性**——这直接导致生成的运动出现物体漂移、手部穿透或脚部浮空等违背物理常识的瑕疵。

针对这一瓶颈，CHOIS 提出了一个统一的框架，其核心操控变量体现在三个层面：**物体几何损失（Object Geometry Loss）** 在训练阶段强制模型准确预测物体顶点位移，从而大幅提升路标点匹配精度；**基于重构引导的解析接触约束项**（包括手-物接触引导、脚-地接触引导和物体-地面穿透引导）在采样阶段通过梯度扰动强制执行物理接触条件；**CLIP 编码的语言描述嵌入** 则作为风格和意图的条件信号，指导交互的整体语义。

该方法的深层洞见在于：**将稀疏物体路标点与语言描述共同作为扩散模型的生成条件，在训练时引入物体几何损失增强路标点匹配，在采样时施加解析接触引导函数来强制执行物理接触约束，能够大幅提升人机交互动作的同步性、真实感和条件遵循度。**

在实验验证方面，CHOIS 在 FullBodyManipulation 和 3D-FUTURE 两个数据集上均取得了优于基线方法的结果。具体而言，在 FullBodyManipulation 数据集上，CHOIS 的脚滑动指标（Foot Sliding, FS）达到 **0.35**，FID 达到 **0.69**；在 3D-FUTURE 数据集上，FS 为 **0.38**，FID 为 **1.60**，均低于对比方法。消融实验进一步证实了各组件的因果作用：移除手-物接触引导后，接触百分比（C%）从 0.67 骤降至 0.49；移除脚-地接触引导后，脚平均高度从 4.20 cm 升至 6.65 cm，浮空现象显著加重；移除物体几何损失则导致路标点条件匹配误差大幅增加。此外，人类感知研究也表明，CHOIS 生成的交互运动在自然度和条件遵循度上获得了更高的偏好比例。

在方法谱系上，CHOIS 定位在**条件扩散生成与物理约束引导的交汇点**。相较于仅依赖完整物体运动序列生成人体运动的 **OMG**（Li et al., ACM Trans. Graph. 2023）和利用物理信息扩散模型但缺乏语言条件的 **InterDiff**（Xu et al., ICCV 2023），CHOIS 首次将稀疏路标点、语言描述与解析接触引导统一到一个扩散框架中，实现了从高层规划到底层物理约束的端到端可控合成。

## 背景与动机

人-物交互（Human-Object Interaction, HOI）合成是计算机视觉与图形学中的一个核心挑战，其目标是生成与物体运动同步、物理上合理且语义一致的全身体运动。这一任务在具身智能、动画制作和虚拟现实等领域具有广泛的应用前景。

当前的主流方法大致分为两类。一类以 **OMG**（Li et al., ACM Trans. Graph. 2023）为代表，利用完整的物体运动序列作为条件来生成人体运动，但该方法既缺乏对语言意图的建模，也无法接受稀疏的路标点约束。另一类如 **InterDiff**（Xu et al., ICCV 2023），在扩散模型中引入物理信息来生成人-物交互，但同样不包含语言描述条件，难以将高层语义意图转化为具体的交互行为。

这两类方法的共同瓶颈在于：**普通条件扩散模型无法保证生成物体运动与给定稀疏路标点对齐，也难以维持手-物接触和脚-地接触的真实性**。具体而言，当仅提供稀疏的物体路标点（如每30帧一个2D位置）和终点3D位置时，模型容易在未标注的时间段内产生物体漂移；同时，生成的交互序列常出现手部穿透物体、脚部浮空或物体陷入地面等物理不合理现象。

上述缺口直接驱动了 **CHOIS** 的提出。其核心动机是：将稀疏物体路标点与语言描述共同作为扩散模型的生成条件，在训练时引入物体几何损失增强路标点匹配，在采样时施加解析接触引导函数来强制执行物理接触约束，从而大幅提升人机交互动作的同步性、真实感和条件遵循度。这一思路使得系统既能接受来自高层规划模块的路标点输入，又能保持生成运动的物理合理性，为长期、场景感知的人机交互合成奠定了基础。

## 核心创新

CHOIS的核心贡献在于将**稀疏物体路标点**与**语言描述**共同作为条件引入条件扩散模型，并通过训练阶段的**物体几何损失**与采样阶段的**解析接触引导**，系统性地解决了普通条件扩散模型在人机交互合成中的两个关键瓶颈：生成物体运动与给定稀疏路标点对齐困难，以及手-物接触和脚-地接触的真实性难以维持。

### 1. 稀疏物体路标点条件

与仅依赖完整物体运动序列（如**OMG**，Li et al., ACM Trans. Graph. 2023）或初始状态的方法不同，CHOIS将稀疏的物体2D路标点（每30帧采样）和终点3D位置作为显式生成条件。这一设计使得模型能够从高层规划模块输出的稀疏路标点出发，生成同步的物体运动与人体运动，从而为长期、场景感知的交互合成提供了接口。

### 2. 物体几何损失

在训练阶段，CHOIS在标准扩散损失之外引入了物体几何损失 $\mathcal{L}_{obj}$（Eq.5）：

$$\mathcal{L}_{obj} = \sum_{t=1}^T \| \hat{R}_t K_{rest} + \hat{d}_t - K_t \|_1$$

该损失直接监督物体顶点位移的预测精度，强制模型准确预测物体位姿变换。消融实验证实，引入物体几何损失后，路标点条件匹配指标（$T_s$、$T_e$、$T_{xy}$）显著提升，表明该损失是改善路标点对齐的关键因果旋钮。

### 3. 解析接触引导

在采样阶段，CHOIS在最后10个去噪步骤中施加重构引导（Eq.6），通过三类解析代价函数的梯度扰动生成结果：

- **手-物接触引导**（Eq.7）：对预测为接触的帧，惩罚手部关键点与最近物体顶点的距离；
- **脚-地接触引导**（Eq.8）：约束最低脚趾垂直高度逼近阈值 $h=0.02\text{m}$；
- **物体-地面穿透引导**（Eq.9）：惩罚物体顶点 $z$ 轴负值，防止穿透地面。

消融实验表明：移除手-物接触引导后，接触百分比从0.67降至0.49；移除脚-地接触引导后，脚平均高度从4.20 cm升至6.65 cm，浮空显著加重。

### 4. 与基线方法的差异总结

| 创新维度 | 基线方法 | CHOIS |
|---------|---------|-------|
| 物体运动条件 | **OMG**：完整物体运动序列；**InterDiff**（Xu et al., ICCV 2023）：无语言条件 | 稀疏物体2D路标点 + 终点3D位置 |
| 语言条件 | 多数基线不使用语言或仅使用动作类别 | CLIP编码的语言描述嵌入，指导风格和意图 |
| 训练监督 | 无额外监督 | 物体几何损失 $\mathcal{L}_{obj}$，增强路标点匹配 |
| 推理约束 | 无接触约束 | 手-物、脚-地、物体-地面三类解析引导函数 |

这种“稀疏条件 + 几何损失 + 解析引导”的三层设计，使得CHOIS在FullBodyManipulation数据集上取得了更低的脚滑动（FS=0.35）和FID（0.69），并在3D-FUTURE数据集上展现出对新物体的泛化能力（FS=0.38，FID=1.60）。

## 整体框架

CHOIS 的整体 pipeline 围绕一个**条件扩散模型**构建，其核心设计目标是在给定稀疏物体路标点与语言描述的条件下，**同步生成**物体运动与人体运动。与仅从完整物体轨迹生成人体运动的 OMG（Li et al., ACM Trans. Graph. 2023）或缺乏语言条件的 InterDiff（Xu et al., ICCV 2023）不同，CHOIS 通过三个关键模块的协同，实现了从高层规划信号到物理合理交互的端到端合成。

**输入流**始于三类异构条件：初始的人体与物体状态、描述交互风格与意图的语言指令（经 CLIP 编码为嵌入向量）、以及稀疏的物体 2D 路标点（每 30 帧采样一次）与终点 3D 位置。这些条件信号分别进入编码与条件注入阶段。

**模块关系**可概括为“编码—生成—约束”三阶段串联：

1. **BPS 物体几何编码器**：将物体几何转换为 Basis Point Set（BPS）表示，并通过 MLP 投影为低维逐帧特征向量。该特征向量与掩码后的姿态状态拼接，构成去噪网络的完整条件信号（Figure 2）。

![[assets/figures/papers/paper_list_l1758_CHOIS_Controllable_Human_Object_Interaction_Synthesis/figures/002_Figure_2.jpg]]
*Figure 2: Method Overview. Given an object geometry, we use the BPS representation to encode the geometry and an*

2. **条件扩散去噪 Transformer**：以 Transformer 作为去噪网络，输入为含噪运动序列、噪声水平嵌入、语言嵌入及上述条件信号，输出为预测的干净运动数据 $\hat{\tau}_0$。训练时最小化 L1 损失 $\mathcal{L} = \mathbb{E}_{\tau_0, n} \| \hat{\tau}_\theta(x_n, n, c) - \tau_0 \|_1$，并额外引入**物体几何损失** $\mathcal{L}_{obj} = \sum_{t=1}^T \| \hat{R}_t K_{rest} + \hat{d}_t - K_t \|_1$，强制模型准确预测物体顶点位移，从而增强生成物体运动与输入路标点的对齐。

3. **解析引导采样**：在推理阶段的最后 10 个去噪步骤中，通过**重构引导** $\tilde{\tau}_0 = \hat{\tau}_0 - \alpha \Sigma_n \nabla_{\tau_n} F(\hat{\tau}_0)$ 施加物理接触约束。引导函数 $F$ 由三项解析代价函数加权组合而成——手-物接触引导 $F_{contact}$（惩罚预测接触帧中手部与最近物体顶点的距离）、脚-地接触引导 $F_{feet}$（约束最低脚趾高度逼近地面阈值）、以及物体-地面穿透引导 $F_{obj}$（惩罚物体顶点的负 z 值）。

**输出流**为同步的物体运动序列与人体运动序列，其中人体运动以全局关节位置和 6D 连续旋转表示。该 pipeline 进一步与**长期路径规划模块**串联，可将稀疏路标点生成与交互合成衔接，实现场景感知的长期人机交互生成（Figure 5）。

**关键因果机制**：物体几何损失在训练阶段解决了扩散模型对稀疏路标点条件匹配不足的瓶颈；解析引导函数在采样阶段强制执行手-物接触、脚-地接触与物体-地面非穿透约束，弥补了无条件生成在物理真实性上的缺陷。消融实验证实，移除物体几何损失会导致路标点匹配误差（$T_s, T_e, T_{xy}$）显著增加；移除手-物接触引导使接触百分比从 0.67 降至 0.49；移除脚-地接触引导使脚平均高度从 4.20 cm 升至 6.65 cm。物体-地面穿透引导主要贡献于定性改善，其定量消融指标未在文中列出，该点需人工验证。

### 补充图表

![[assets/figures/papers/paper_list_l1758_CHOIS_Controllable_Human_Object_Interaction_Synthesis/figures/001_Figure_1.jpg]]
*Figure 1: Given an initial object and human state, a language description, and sparse object waypoints in a 3D scene, CHOIS generates synchronized object motion and human motion at the same time*

## 核心模块与公式推导

### 3.1 数据表示与条件编码

**人体运动表示**：每帧人体姿态 $X_t$ 由全局关节位置与6D连续旋转表示构成（**Figure 2**）。动作序列 $\tau$ 同时包含人体运动与物体运动，作为扩散模型的生成目标。

**物体几何编码**：给定物体几何形状，CHOIS采用基点点集（Basis Point Set, BPS）表示进行编码，并通过一个MLP将高维特征投影为低维向量。该特征向量与掩码后的姿态状态拼接，共同构成去噪网络的条件信号（**Figure 2**）。

**条件信号构成**：模型接收三类条件输入——
- **语言描述**：经CLIP编码的文本嵌入，指导交互风格与意图；
- **稀疏物体路标点**：每30帧采样的2D路标点及终点3D位置，锚定物体运动轨迹；
- **初始状态**：人体与物体的初始姿态。

### 3.2 条件扩散模型

CHOIS以条件扩散模型为核心框架，同时生成物体运动与人体运动。

**前向扩散过程**：逐步向干净数据 $\tau_0$ 添加高斯噪声，单步转移为：

$$q(\tau_n \mid \tau_{n-1}) := \mathcal{N}(\tau_n; \sqrt{1-\beta_n}\tau_{n-1}, \beta_n I) \quad \text{(Eq. 1)}$$

完整前向过程的联合分布为：

$$q(\tau_{1:N} \mid \tau_0) := \prod_{n=1}^N q(\tau_n \mid \tau_{n-1}) \quad \text{(Eq. 2)}$$

**反向去噪过程**：学习参数化高斯转移，从纯噪声逐步恢复干净数据：

$$p_\theta(\tau_{n-1} \mid \tau_n, c) := \mathcal{N}(\tau_{n-1}; \mu_\theta(\tau_n, n, c), \Sigma_n) \quad \text{(Eq. 3)}$$

其中 $c$ 为条件信号（语言嵌入、物体几何特征、路标点信息），$\mu_\theta$ 由Transformer去噪网络参数化。

**训练损失**：模型直接预测干净数据 $\hat{\tau}_\theta$，采用L1损失：

$$\mathcal{L} = \mathbb{E}_{\tau_0, n} \| \hat{\tau}_\theta(x_n, n, c) - \tau_0 \|_1 \quad \text{(Eq. 4)}$$

### 3.3 物体几何损失

为解决标准扩散训练无法保证生成物体运动与稀疏路标点对齐的问题，CHOIS引入物体几何损失作为额外监督。该损失在物体顶点级别施加约束，强制模型准确预测物体位姿变换后的顶点位置：

$$\mathcal{L}_{obj} = \sum_{t=1}^T \| \hat{R}_t K_{rest} + \hat{d}_t - K_t \|_1 \quad \text{(Eq. 5)}$$

其中 $\hat{R}_t$、$\hat{d}_t$ 为预测的旋转矩阵与平移向量，$K_{rest}$ 为物体静止姿态下的顶点坐标，$K_t$ 为真实顶点位置。该损失直接惩罚顶点级L1误差，是提升路标点条件匹配指标的关键因果杠杆（消融实验证实移除该损失后 $T_s$、$T_e$、$T_{xy}$ 等匹配误差显著增加）。

### 3.4 采样时的解析引导

在推理阶段，CHOIS对最后10个去噪步骤施加基于重构引导的解析约束，以强制执行物理接触条件。核心机制为利用代价函数 $F$ 的梯度扰动预测的干净数据：

$$\tilde{\tau}_0 = \hat{\tau}_0 - \alpha \Sigma_n \nabla_{\tau_n} F(\hat{\tau}_0) \quad \text{(Eq. 6)}$$

其中 $\Sigma_n$ 为噪声协方差，$\alpha$ 为引导强度。代价函数 $F$ 由三项解析约束加权组成：

**手-物接触引导**：对预测为接触的帧，惩罚手部关节与最近物体顶点的距离：

$$F_{contact} = \|M_l \odot |J_l - V_l|\|_1 + \|M_r \odot |J_r - V_r|\|_1 \quad \text{(Eq. 7)}$$

其中 $M_l$、$M_r$ 为左右手接触掩码，$J$ 为手部关节位置，$V$ 为最近物体顶点。

**脚-地接触引导**：约束最低脚趾的垂直高度逼近地面阈值 $h = 0.02\text{m}$：

$$F_{feet} = \|\min(J_l^z, J_r^z) - h\|_2 \quad \text{(Eq. 8)}$$

**物体-地面穿透引导**：惩罚物体顶点出现在地面以下（z轴负值）：

$$F_{obj} = \|\min(V^z, 0)\|_1 \quad \text{(Eq. 9)}$$

消融实验表明，移除手-物接触引导后接触百分比从0.67降至0.49；移除脚-地接触引导后脚平均高度从4.20 cm升至6.65 cm，浮空显著加重。物体-地面穿透引导主要改善定性效果，相关定量消融指标未在论文中列出。

## 实验与分析

### 核心实验设置与评估基准

CHOIS 在两个数据集上进行了系统评估：**FullBodyManipulation**（Li et al., ACM Trans. Graph. 2023）和 **3D-FUTURE**（Fu et al., CVPR 2021）。前者包含全身人体与物体的交互动作序列，后者用于验证方法对未见物体的泛化能力。评估指标涵盖运动质量（FID ↓）、物理合理性（Foot Sliding ↓）、接触精度（Contact Percentage C% ↑）以及条件匹配误差（起始位置误差 T_s、终点位置误差 T_e、路标点轨迹误差 T_xy）。

### 主要定量结果

在 FullBodyManipulation 数据集上，CHOIS 取得了 **Foot Sliding 0.35** 和 **FID 0.69** 的成绩（Table 1），显著优于基线方法。在 3D-FUTURE 数据集上，CHOIS 同样表现出色，**Foot Sliding 为 0.38，FID 为 1.60**（Table 2），验证了该方法对新颖物体几何的泛化能力。值得注意的是，由于原论文未提供基线方法的具体数值，上述比较基于论文中的定性描述和趋势判断，建议查阅原表获取完整对比数据。

![[assets/figures/papers/paper_list_l1758_CHOIS_Controllable_Human_Object_Interaction_Synthesis/figures/003_Table_1.jpg]]
*Table 1: Interation synthesis on the FullBodyManipulation dataset [28]*

![[assets/figures/papers/paper_list_l1758_CHOIS_Controllable_Human_Object_Interaction_Synthesis/figures/004_Table_2.jpg]]
*Table 2: Interaction synthesis on the 3D-FUTURE dataset [12]*

### 消融实验：引导项的因果作用

消融实验揭示了各引导项对生成质量的因果贡献（Table 3）：

![[assets/figures/papers/paper_list_l1758_CHOIS_Controllable_Human_Object_Interaction_Synthesis/figures/007_Table_3.jpg]]
*Table 3: Ablation study on the FullBodyManipulation dataset [28]. We measure the effect of different guidance terms in the human and object motion generation*

- **手-物接触引导**：移除后，接触百分比（C%）从 0.67 降至 0.49，表明该引导项是维持手部与物体稳定接触的关键因素。
- **脚-地接触引导**：移除后，脚部平均高度（H_feet）从 4.20 cm 升至 6.65 cm，浮空现象显著加重，证实了该引导项对脚部物理合理性的约束作用。
- **物体几何损失**：移除后，路标点条件匹配误差（T_s, T_e, T_xy）显著增加，说明该损失项是生成物体运动与输入路标点对齐的核心机制。

物体-地面穿透引导主要提供定性改善，其定量消融指标未在论文中列出，该点需手动验证。

### 长期交互合成能力

CHOIS 通过与路径规划模块的集成，支持长期、场景感知的人机交互生成。在长期交互合成实验中（Table 4），该方法在 FullBodyManipulation 和 3D-FUTURE 数据集上均保持了良好的运动质量和物理合理性。图 5 展示了给定语言描述、3D 场景语义标签以及初始状态后，系统合成长期人机交互序列的能力。

![[assets/figures/papers/paper_list_l1758_CHOIS_Controllable_Human_Object_Interaction_Synthesis/figures/009_Table_4.jpg]]
*Table 4: Long-term interaction synthesis results on the FullBodyManipulation [28] and 3D-FUTURE datasets [12]. ∗ represents the results on the 3D-FUTURE dataset*

### 条件解耦与控制能力

图 6 展示了 CHOIS 对语言和路标点条件的解耦控制能力：在相同文本描述下使用不同路标点，可生成不同空间轨迹的交互动作；在相同路标点下使用不同文本描述，可改变交互风格和意图。这一特性验证了语言嵌入与空间路标点作为独立条件通道的有效性。

### 人类感知评估

通过人类感知研究（Figure 4），受试者在运动偏好上显著倾向于 CHOIS 的生成结果，进一步验证了该方法在视觉真实感和交互自然性上的优势。具体的文本输入内容和评估协议细节在论文中有详细说明，此处不再赘述。

![[assets/figures/papers/paper_list_l1758_CHOIS_Controllable_Human_Object_Interaction_Synthesis/figures/006_Figure_4.jpg]]
*Figure 4: Results of human perceptual studies. The numbers shown in the chart represent the percentage (%) over motion preferences*

### 失败模式与局限性

尽管 CHOIS 在定量指标和定性评估上表现优异，论文未系统报告失败案例。从方法设计推断，潜在失败模式可能包括：极端稀疏路标点下物体运动预测不准确、复杂接触场景中引导项权重难以平衡、以及长序列生成中的误差累积问题。这些推断需在实际应用中进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l1758_CHOIS_Controllable_Human_Object_Interaction_Synthesis/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative results of the FullBodyManipulation dataset [28]*

![[assets/figures/papers/paper_list_l1758_CHOIS_Controllable_Human_Object_Interaction_Synthesis/figures/008_Figure_5.jpg]]
*Figure 5: Long-term interaction synthesis. Given language descriptions, a 3D scene with semantic labels, and initial human and object states, we synthesize long-term human-object interactions. The initial state is shown in green*

![[assets/figures/papers/paper_list_l1758_CHOIS_Controllable_Human_Object_Interaction_Synthesis/figures/010_Figure_6.jpg]]
*Figure 6: Results of interaction synthesis using the same text but different waypoints (a) and using the same waypoints but different text (b). The initial state is in green*

## 方法谱系与知识库定位

### 与基线方法的关系

CHOIS 处于条件扩散模型用于人-物交互生成这一技术脉络中，但其条件设计、训练监督和推理约束机制与现有工作形成显著差异。

**与 OMG 的关系。** **OMG**（Li et al., ACM Trans. Graph. 2023）以完整物体运动序列为条件生成人体运动，是一种“物体运动引导”的范式。该工作的核心假设是物体运动已知，模型只需补全人体响应。CHOIS 从根本上改变了这一设定：它同时生成物体运动和人体运动，且仅需稀疏的物体 2D 路标点（每 30 帧）和终点 3D 位置作为条件，而非完整的物体轨迹。这一差异使得 CHOIS 的输入条件更接近高层规划的输出，为与路径规划模块的集成提供了接口（见 Figure 5 的长期交互合成）。

**与 InterDiff 的关系。** **InterDiff**（Xu et al., ICCV 2023）利用物理信息扩散模型生成人-物交互，但不使用语言描述作为条件。CHOIS 在此基础上引入了 CLIP 编码的语言嵌入，使得生成结果不仅受几何条件约束，还受语义意图引导。Figure 6 的对比实验表明，相同路标点搭配不同语言描述可产生风格迥异的交互动作，验证了语言条件的独立调控能力。

**技术差异的关键维度。** 从条件扩散模型的视角看，CHOIS 与上述基线在三个关键维度上存在差异：(1) 条件信号的构成——OMG 使用完整物体运动，InterDiff 不使用语言，CHOIS 则组合了稀疏路标点、语言描述和初始状态；(2) 训练阶段的额外监督——OMG 和 InterDiff 均未引入针对物体几何的显式损失，CHOIS 通过物体几何损失 $\mathcal{L}_{obj}$（Eq. 5）强制模型准确预测物体顶点位移；(3) 推理阶段的约束引导——OMG 和 InterDiff 在采样过程中无额外接触约束，CHOIS 在最后 10 个去噪步骤中施加手-物接触引导（Eq. 7）、脚-地接触引导（Eq. 8）和物体-地面穿透引导（Eq. 9），通过重构引导框架（Eq. 6）将解析约束梯度注入生成过程。

### 适用边界与局限

**适用场景。** CHOIS 的设计使其特别适用于以下场景：(1) 给定高层规划（如“将杯子从桌子移到水槽”）和稀疏路标点，需要生成同步的人-物交互动作序列；(2) 需要语言描述来区分同一路标点序列下的不同交互风格（如“小心地”vs“快速地”移动物体）；(3) 需要将交互合成模块与路径规划模块串联，实现长期、场景感知的人机交互生成（见 Table 4 的长期交互结果）。在 FullBodyManipulation 和 3D-FUTURE 两个数据集上，CHOIS 在脚滑动（FS）和 FID 指标上均优于基线方法（Table 1, Table 2）。

**已知局限。** 论文原文中未明确列出方法局限，但基于方法设计和实验设置可以推断以下边界：(1) 物体几何损失的引入要求训练数据包含物体顶点级别的真值标注，这限制了该方法在仅有粗略物体表示的数据集上的直接应用；(2) 接触引导项中的超参数（如 Eq. 7 中的接触掩码阈值、Eq. 8 中的脚高度阈值 $h=0.02\mathrm{m}$）需要针对不同场景进行调优，泛化到显著不同的交互类型时可能需要重新校准；(3) 物体-地面穿透引导（Eq. 9）主要面向定性改善，论文未提供其独立的定量消融结果，其对物理一致性指标的具体贡献尚不明确。

### 开放问题

以下问题在论文中未得到充分回答，值得后续工作关注：

1. **物体几何损失的机制解释。** 物体几何损失相对于标准扩散训练究竟如何改善路标点对齐？消融实验（Table 3）显示移除该损失后路标点条件匹配误差（$T_s$, $T_e$, $T_{xy}$）显著增加，但其作用机制——是通过约束物体位姿预测精度间接改善路标点匹配，还是通过正则化扩散模型的生成空间——需要进一步分析。

2. **接触约束的量化评估体系。** 当前评估中，接触百分比（C%）和脚平均高度（$H_{feet}$）分别衡量手-物接触和脚-地接触，但缺乏统一的物理一致性综合指标。物体-地面穿透引导的效果仅通过定性结果展示，其对定量指标（如穿透深度分布、物理模拟兼容性）的影响需要系统评估。

3. **跨数据集泛化能力。** CHOIS 在 FullBodyManipulation 和 3D-FUTURE 上展示了泛化能力，但这两个数据集均以桌面级物体操作为主。该方法能否在更大规模的动态物体交互数据（如包含铰接物体、可变形物体的场景）上保持性能，仍有待验证。

4. **人类感知研究的文本输入覆盖度。** Figure 4 的人类感知研究表明 CHOIS 在用户偏好上优于基线，但论文未披露感知研究中使用的具体文本输入集合。文本描述的多样性和难度分布是否覆盖了方法的能力边界，需要更多信息来判断结论的稳健性。

5. **引导强度的自适应调节。** 当前设计在最后 10 个去噪步骤中施加固定权重的引导项（$\lambda_2$, $\lambda_3$）。是否可以根据噪声水平或预测置信度自适应调节引导强度，以在早期步骤避免过度约束、在后期步骤强化接触精度，是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/ECCV_2024/CHOIS_Controllable_Human_Object_Interaction_Synthesis.pdf]]