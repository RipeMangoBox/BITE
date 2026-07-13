---
title: TRAM Global Trajectory and Motion of 3D Humans from in the wild Videos
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/TRAM_Global_Trajectory_and_Motion_of_3D_Humans_from_in_the_wild_Videos.pdf
project_link: https://yufu-wang.github.io/tram4d/
code_link: null
aliases:
- TGTM3HFWV
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 采用两阶段策略：利用掩码DROID-SLAM结合背景深度对齐获得度量尺度的鲁棒相机轨迹，再通过冻结ViT-H并添加两个时间Transformer的VIMO模型在相机坐标系下回归人体运动。
primary_logic: 场景背景提供了可靠且泛化的尺度信息，优于基于人体运动的先验；通过大规模预训练图像模型上微调时间模块，可高效地实现视频级高精度人体重建。
claims:
- TRAM在EMDB上将全局根轨迹误差（RTE）相对于WHAM降低了60%
- 双掩码策略（输入图像和DBA置信度）使DROID-SLAM在动态人体存在时保持鲁棒
- 通过鲁棒最小二乘和取中位数从ZoeDepth深度预测中估计尺度，可得到度量级相机轨迹
- VIMO的两个时间Transformer分别从图像域和运动域传播时间信息，提升准确性和平滑性
---

# TRAM Global Trajectory and Motion of 3D Humans from in the wild Videos

> [!tip] 核心洞察
> 场景背景提供了可靠且泛化的尺度信息，优于基于人体运动的先验；通过大规模预训练图像模型上微调时间模块，可高效地实现视频级高精度人体重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | TRAM：从野外视频中重建3D人体的全局轨迹与运动 |
| 英文题名 | TRAM Global Trajectory and Motion of 3D Humans from in the wild Videos |
| 会议/期刊 | ECCV 2024 |
| Links | [Project](https://yufu-wang.github.io/tram4d/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | TRAM |
| Dataset | EMDB |

> [!tip] 效果简介
> - EMDB 上，ATE (m) (相机轨迹误差，已知尺度) 0.32 (Masked DROID平均) vs DROID-SLAM (无掩码，常发散) / ORB-SLAM2 (显著提升，避免发散)；RTE (%) (根轨迹误差) 1.4 vs 3.5 (WHAM) (-2.1 (-60%))。

## 概要

### 问题与瓶颈

从动态移动相机拍摄的野外视频中准确恢复3D人体的**全局轨迹**与**局部身体运动**，是计算机视觉中的一个核心难题。其根本瓶颈在于：一方面，单目视频天然缺乏度量尺度信息，现有方法要么依赖泛化能力有限的人体运动先验来推断尺度，要么直接回归视频级人体运动，但受限于训练成本与数据规模；另一方面，动态人体本身会严重干扰SLAM系统的特征匹配与光束平差，导致相机轨迹估计发散。

### 核心思路

TRAM采用**两阶段解耦策略**，将这一复杂问题分解为可独立优化的子任务：

1. **场景驱动**的度量相机轨迹恢复：利用场景背景的静态几何信息，通过掩码增强的DROID-SLAM获得鲁棒的相对相机轨迹，再将其与度量深度预测对齐，从而获取**可靠且泛化性强的尺度信息**——这优于依赖人体运动模型推断尺度的方案。
2. **视频级人体运动回归**：在冻结的大规模预训练图像模型（ViT-H）之上，添加两个轻量级时间Transformer，分别从图像域和运动域传播时序信息，高效实现相机坐标系下的高精度人体姿态与相对位姿回归。

最终，世界坐标系下的全局人体轨迹由度量相机轨迹与相机坐标系下的相对人体位置组合而成：$\{ \mathbf { H } _ { t } \} _ { t = 0 } ^ { T } = \{ \mathbf { G } _ { t } \circ \mathbf { T } _ { t } \} _ { t = 0 } ^ { T }$。

### 方法定位

TRAM处于**SLAM辅助的全局人体运动重建**这一技术路线。与依赖人体运动先验的方法（如**WHAM**，Shin et al., arXiv 2023）不同，TRAM从场景背景中获取尺度；与纯回归方法（如**GLAMR**，Yuan et al., CVPR 2022）不同，TRAM通过SLAM显式建模相机运动，减少长序列漂移。在人体重建层面，TRAM的VIMO模块建立在单帧基线**HMR2.0**（Goel et al., ICCV 2023）之上，通过添加时间Transformer实现视频级精度提升，而非从头训练昂贵的视频模型。

### 主要结果

在EMDB基准上，TRAM取得了显著优势：

- **全局轨迹**：根轨迹误差（RTE）为**1.4%**，相较于WHAM的3.5%降低了**60%**（Table 3）。
- **相机轨迹**：掩码DROID-SLAM结合尺度估计后，在EMDB上平均ATE-S达到**0.32m**，而原始DROID-SLAM在动态人体场景中常发散（Table 1, Table 2）。
- **网格重建**：VIMO在3DPW和EMDB上均达到最优网格精度（Table 4），消融实验证实两个时间Transformer分别贡献于重建精度和运动平滑性（Table 5）。

> **注意**：WHAM在对比中使用的是采用真实陀螺仪数据的版本（Fig. 6注释），实际泛化场景下TRAM的优势可能更大。

从普通摄像机拍摄的野外视频中恢复三维人体运动，是计算机视觉与图形学中长期存在的核心挑战。该问题的完整解包含两个耦合部分：**世界坐标系下的全局人体轨迹**（人在场景中“走到了哪里”）和**相机坐标系下的局部身体姿态**（人“如何动作”）。然而，由于拍摄过程中相机本身也在运动，图像中观察到的运动是人体运动与相机运动叠加后的混合信号，使得准确解耦并重建这两部分变得异常困难。

### 现有方法的瓶颈

当前方法在这一问题上存在明显的结构性缺口，具体表现为三个层次：

**1. 尺度缺失与先验依赖。** 基于单帧图像的人体重建方法（如 **HMR2.0**，Goel et al., ICCV 2023）只能在相机坐标系下输出无尺度的身体姿态，无法提供人在世界中的真实位移。一些方法尝试通过回归全局轨迹来弥补这一缺陷——例如 **WHAM**（Shin et al., arXiv 2023）利用人体运动学先验和惯性传感器数据推断世界坐标系下的运动——但这些先验的泛化能力有限，在复杂地形或长距离运动中容易出现尺度漂移。**GLAMR**（Yuan et al., CVPR 2022）虽能基于人体位移估计全局轨迹，但同样缺乏可靠的度量尺度信息。

**2. 动态场景下的SLAM脆弱性。** 视觉SLAM系统（如 **DROID-SLAM**，Teed & Deng, NeurIPS 2021；**ORB-SLAM2**，Mur-Artal & Tardós, IEEE TRO 2017）能够恢复相机运动，但其设计假设场景是静态的。当画面中存在大范围移动的人体时，动态区域的光流会严重干扰捆集调整（Bundle Adjustment）的优化过程，导致相机轨迹发散或完全失败。在野外人体运动视频中，这一假设几乎从不成立。

**3. 视频级人体回归的训练成本。** 从视频序列中直接回归人体运动需要时序建模能力，但端到端地训练一个大规模视频人体重建模型面临双重困难：一方面，带精确标注的野外视频人体运动数据极为稀缺；另一方面，从头训练视频级Transformer的计算成本高昂，限制了模型规模和泛化性能。

### 核心动机

上述瓶颈指向一个关键洞察：**场景背景提供了可靠且泛化的尺度信息，优于基于人体运动学的先验**。静态场景元素（地面、建筑、植被等）在视频中天然携带度量尺度的线索，且不受人体动作复杂性的影响。如果能够从动态视频中鲁棒地恢复出度量尺度的相机轨迹，就能为人体运动重建提供一个稳定的世界参考系。

基于这一洞察，TRAM采用**两阶段解耦策略**：先利用场景恢复相机运动，再在相机坐标系下回归人体运动，最后将二者组合得到全局结果。这一设计将困难的联合估计问题分解为两个相对成熟的子问题——鲁棒的视觉SLAM和视频人体姿态回归——并通过冻结大规模预训练模型（ViT-H）并仅微调轻量时序模块的方式，高效地赋予单帧模型视频理解能力。

## 核心方法与创新机理

TRAM 的核心创新在于将“从动态相机拍摄的野外视频中恢复全局人体运动”这一难题分解为两个可独立解决、且相互增强的子问题，并通过三个关键“changed slots”实现了对基线方法的系统性改进。

**1. 双掩码鲁棒SLAM（动态物体处理）**

传统视觉SLAM（如 **DROID-SLAM** (Teed & Deng, NeurIPS 2021)）在存在动态人体时极易发散，因为人体运动破坏了静态场景假设。TRAM 提出了一种双掩码策略（Section 3.2, Fig. 2），从两个层面消除动态人体的干扰：
- **输入掩码**：对输入图像中的人体区域进行掩码，使其不参与光流计算。
- **DBA置信度掩码**：在密集光束法平差（Dense Bundle Adjustment, DBA）阶段，将人体区域的流置信度置零，阻止其影响相机位姿和深度的优化。

这一策略的因果机制在于：场景背景提供了可靠且泛化的尺度信息，其几何约束远优于基于人体运动的先验。实验表明，仅掩码输入或仅掩码DBA均不如双掩码有效（Section 4.1, Table 1）。在EMDB数据集上，双掩码使 **Masked DROID-SLAM** 平均ATE降至0.32m（已知尺度），而原始DROID-SLAM常发散（Table 1, Fig. 4）。

**2. 基于场景深度的度量尺度估计（运动尺度获取）**

SLAM恢复的相机轨迹缺乏度量尺度。现有方法（如 **WHAM** (Shin et al., arXiv 2023)）依赖人体运动模型推断尺度，但人体运动先验的泛化能力有限。TRAM 转而利用场景背景的深度信息：将SLAM输出的相对深度与 **ZoeDepth** 预测的度量深度对齐，通过鲁棒最小二乘和取中位数估计全局尺度因子（Section 3.3, Table 2）。

关键设计在于：对整段视频的尺度估计取中位数，而非逐帧计算。这有效规避了单帧深度预测的噪声，因为“使用整段序列的中位数能够很好地逼近真实尺度”（Section 4.1）。Table 2显示，该方法使ATE-S达到0.66m，而直接将ZoeDepth深度输入DROID-SLAM会导致较大误差。

**3. 冻结ViT-H + 双时间Transformer的视频人体回归（VIMO）**

视频级人体运动回归模型受限于训练成本与数据量。TRAM 提出 **VIMO**（Section 3.4, Fig. 3）：在 **HMR2.0** (Goel et al., ICCV 2023) 的冻结ViT-H主干上，添加两个时间Transformer，分别从图像域和运动域传播时间信息：
- **图像域时间Transformer**：对同一空间位置的patch tokens跨时间建模，增强视觉特征的时间一致性。
- **运动域时间Transformer**：对SMPL姿态参数跨时间建模，提升运动平滑性。

这一设计的核心洞察是：大规模预训练图像模型已具备强大的单帧重建能力，仅需轻量级时间模块即可高效实现视频级高精度重建。消融实验（Table 5）证实：移除图像域时间Transformer会导致3DPW上PA-MPJPE从35.6升至36.3；移除运动域时间Transformer则使加速度指标升高，降低运动平滑性。

**4. 两阶段解耦的组合优势**

上述三个创新模块通过“世界坐标系人体轨迹组合”公式（$\\{ \\mathbf { H } _ { t } \\} _ { t = 0 } ^ { T } = \\{ \\mathbf { G } _ { t } \\circ \\mathbf { T } _ { t } \\} _ { t = 0 } ^ { T }$）协同工作：度量尺度相机轨迹 $\mathbf{G}_t$ 提供全局参考系，VIMO在相机坐标系下回归相对人体位姿 $\mathbf{T}_t$，二者组合得到世界轨迹。这种解耦设计使得TRAM在EMDB上将全局根轨迹误差（RTE）相对于WHAM降低了60%（Table 3），同时保持了网格重建的最优精度（Table 4）。

TRAM 将“从野外视频中恢复全局人体运动”这个复杂问题分解为两个可独立优化的子任务：**度量级相机轨迹恢复**与**相机坐标系下的人体运动回归**。这一分解的核心洞察在于：场景背景提供了可靠且泛化的尺度信息，其稳定性远优于基于人体运动学的先验假设；同时，将相机轨迹与人体运动解耦，使得各模块可以分别利用最合适的预训练模型，避免端到端联合训练带来的数据与计算开销。

### 流水线概览

整个流水线由四个模块串联构成，如图 Fig. 2 所示：

![[assets/figures/papers/paper_list_l1643_TRAM_Global_Trajectory_and_Motion_of_3D_Humans_from_in_the_wild_Videos/figures/002_Figure_2.jpg]]
*Figure 2: Overview of TRAM. Top-left: given a video, we first recover the relative camera motion and scene depth with DROID-SLAM, which we robustify with dual masking (Sec. 3.2). Top-right: we align the recovered depth to metric depth prediction with an optimization procedure to estimate metric scaling (Sec. 3.3). Bottom: We introduce VIMO to reconstruct the 3D human in the camera coordinate (Sec. 3.4), and use the metric-scale camera to convert the human trajectory and body motion to the global coordinate*

1. **Masked DROID-SLAM**：接收野外视频帧序列，通过双掩码策略鲁棒地恢复尺度不确定的相机相对轨迹 $\{\mathbf{G}_t\}_{t=0}^T$ 和场景深度 $\mathbf{d}$。
2. **Scale Estimation Module**：将 SLAM 输出的无尺度深度与 ZoeDepth 预测的度量深度对齐，通过鲁棒最小二乘和中位数滤波估计全局尺度因子 $s$，从而将相机轨迹转换为度量级。
3. **VIMO**：在冻结的 ViT-H 特征提取器之上添加两个时间 Transformer，在相机坐标系下回归 SMPL 参数序列 $\{\Theta_t\}_{t=0}^T$ 和人体相对于相机的位置 $\{\mathbf{T}_t\}_{t=0}^T$。
4. **World-frame Composition**：将度量相机轨迹与相对人体位置组合，得到世界坐标系下的全局人体轨迹 $\{\mathbf{H}_t\}_{t=0}^T = \{\mathbf{G}_t \circ \mathbf{T}_t\}_{t=0}^T$。

### 模块间的输入输出关系

流水线的信息流是单向、级联的，各模块之间不存在迭代优化或反馈回路：

- **Masked DROID-SLAM → Scale Estimation**：SLAM 输出的稠密深度图 $\mathbf{d}_i$ 和相机位姿 $\mathbf{G}_t$ 传入尺度估计模块。尺度估计仅使用深度信息，不修改相机位姿本身。
- **Scale Estimation → World-frame Composition**：估计的全局尺度因子 $s$ 用于缩放相机轨迹，得到度量级 $\mathbf{G}_t^{\text{metric}}$。
- **VIMO → World-frame Composition**：VIMO 输出的人体相对平移 $\mathbf{T}_t$ 与缩放后的相机位姿组合，生成世界轨迹。VIMO 本身不依赖尺度估计的结果，二者完全解耦。
- **输入视频 → Masked DROID-SLAM / VIMO**：两个分支共享同一视频输入，但处理方式独立——SLAM 分支使用掩码后的图像，VIMO 分支使用原始图像。

### 关键设计决策

**为什么是两阶段而非端到端？** 端到端联合优化相机与人体运动需要大规模视频级标注数据，且动态人体会严重干扰 SLAM 的捆集调整（BA）。TRAM 通过掩码策略在 SLAM 阶段显式剔除人体区域，使相机轨迹恢复不受人体运动影响；同时，VIMO 在相机坐标系下回归人体运动，避免了世界坐标系下长序列漂移的累积效应。实验表明，这种解耦策略在 EMDB 上将全局根轨迹误差（RTE）相对于端到端方法 **WHAM**（Shin et al., arXiv 2023）降低了 60%（Table 3）。

**为什么在冻结的 ViT-H 上添加时间 Transformer？** HMR2.0 的大规模预训练 ViT-H 已经具备强大的单帧人体理解能力。冻结该骨干网络，仅训练两个轻量时间 Transformer，可以在有限视频训练数据（3DPW、Human3.6M、BEDLAM）下高效地引入时序一致性，同时避免灾难性遗忘。消融实验（Table 5）证实，移除任一 Transformer 都会导致精度或平滑性下降。

![[assets/figures/papers/paper_list_l1643_TRAM_Global_Trajectory_and_Motion_of_3D_Humans_from_in_the_wild_Videos/figures/001_Figure_1.jpg]]
*Figure 1: Overview. Given an in-the-wild video, TRAM reconstructs the complete 3D human motion: global trajectory and local body motion, in diverse and longrange scenarios*

### 3.1 运动分解与全局轨迹组合

TRAM将人体运动分解为世界坐标系下的SE(3)根轨迹与相机坐标系下的运动学姿态序列。给定视频帧$t \in \{0, \ldots, T\}$，人体全局运动表示为：

$$\{ \mathbf { H } _ { t } \} _ { t = 0 } ^ { T } = \{ \mathbf { G } _ { t } \circ \mathbf { T } _ { t } \} _ { t = 0 } ^ { T }$$

其中$\mathbf{G}_t$为度量尺度下的相机到世界变换，$\mathbf{T}_t$为人体根节点在相机坐标系下的相对位姿。该分解的核心优势在于：场景背景提供可靠且泛化的尺度信息，而人体运动在相机坐标系下回归可避免全局漂移累积。

人体运动学姿态由SMPL参数化模型表达：

$$\mathcal { M } ( \theta , \beta , r , \pi ) \in \mathbb { R } ^ { 6 8 9 0 \times 3 }$$

其中$\theta$为姿态参数，$\beta$为形状参数，$r$为根朝向，$\pi$为根平移，输出6890个顶点的网格。

### 3.2 Masked DROID-SLAM：鲁棒相机轨迹恢复

**瓶颈**：原始**DROID-SLAM**（Teed & Deng, NeurIPS 2021）在动态人体场景中易发散，因为光流估计和稠密BA（Dense Bundle Adjustment）将人体运动误判为场景结构变化。

**因果调控**：双掩码策略——同时对输入图像和DBA置信度进行掩码，将动态人体区域置零。

DROID-SLAM优化以下重投影误差目标：

$$E ( G , d ) = \sum _ { ( i , j ) } \parallel p _ { i j } - \varPi ( G _ { i j } \circ \varPi ^ { - 1 } ( p _ { i } , d _ { i } ) ) \parallel _ { \sum _ { i j } } ^ { 2 },\quad \sum _ { i j } = \mathrm { d i a g }( w _ { i j } )$$

其中$p_{ij}$为帧间光流对应点，$G_{ij}$为相对位姿，$d_i$为逆深度，$w_{ij}$为DBA输出的置信度权重。双掩码操作：

$$\hat{\mathbf{I}}_i = \mathrm{mask}(\mathbf{I}_i),\quad \hat{\mathbf{w}}_{ij} = \mathrm{mask}(\mathbf{w}_{ij})$$

将人体分割掩码区域在输入图像和置信度图上均置零，迫使SLAM仅依赖静态背景区域进行优化。消融实验（Table 1）证实：仅掩码输入或仅掩码DBA均不如双掩码有效，双掩码使DROID-SLAM在EMDB长序列上避免发散。

### 3.3 尺度估计模块：从无尺度到度量尺度

**瓶颈**：DROID-SLAM输出为尺度不确定的相机轨迹和场景深度，缺乏度量信息。

**因果调控**：将SLAM深度与**ZoeDepth**预测的度量深度对齐，通过鲁棒最小二乘和取中位数求解全局尺度因子。

尺度对齐能量函数为：

$$E ( \alpha ) = \sum _ { ( h , w ) } \rho ( \alpha * \mathbf { d } _ { i } - \mathbf { D } _ { i } )$$

其中$\mathbf{d}_i$为SLAM输出的逆深度转换后的深度图，$\mathbf{D}_i$为ZoeDepth预测的度量深度，$\rho$为German-McClure鲁棒损失，$\alpha$为待求解的全局尺度因子。对整段视频所有帧求解$\alpha$后取中位数作为最终尺度估计，避免逐帧估计受噪声深度预测干扰。消融实验（Section 3.3, 4.1）表明：将中位数替换为逐帧计算会降低准确性。

### 3.4 VIMO：视频级人体运动回归

**瓶颈**：单帧**HMR2.0**（Goel et al., ICCV 2023）缺乏时间建模，无法利用视频帧间信息提升精度和平滑性。

**因果调控**：冻结预训练ViT-H骨干网络，在其上添加两个时间Transformer——分别从图像域和运动域传播时间信息。

VIMO在HMR2.0的ViT-H编码器基础上插入：
1. **图像域时间Transformer**：对同一空间位置的patch token沿时间轴做自注意力，融合跨帧外观信息；
2. **运动域时间Transformer**：对SMPL姿态参数沿时间轴做自注意力，显式建模运动平滑性。

训练损失为组合损失：

$$\mathcal { L } = \lambda _ { 2 D } \mathcal { L } _ { 2 D } + \lambda _ { 3 D } \mathcal { L } _ { 3 D } + \lambda _ { S M P L } \mathcal { L } _ { S M P L } + \lambda _ { V } \mathcal { L } _ { V }$$

其中3D关节损失为Frobenius范数：

$$\mathcal { L } _ { 3 D } = | | \hat { \mathcal { I } } _ { 3 D } - \mathcal { I } _ { 3 D } | | _ { F } ^ { 2 }$$

消融实验（Table 5）证实：移除图像域时间Transformer导致3DPW上PA-MPJPE从35.6升至36.3；移除运动域时间Transformer导致加速度指标升高，运动平滑性下降。

## 实验与关键发现

### 核心实验设计

TRAM 的实验验证分为两个独立环节：相机轨迹估计与人体运动重建。相机部分在 EMDB 数据集上评估绝对轨迹误差（ATE）和尺度估计后的轨迹误差（ATE-S）；人体部分在 EMDB 和 3DPW 上评估全局根轨迹误差（RTE）、关节位置误差（MPJPE、PA-MPJPE）、顶点误差（PVE）以及运动平滑性指标（加速度 Accel）。这种解耦评估策略直接对应 TRAM 的两阶段设计——先获得度量级相机轨迹，再在相机坐标系下回归人体运动。

训练数据方面，VIMO 使用与基线 **HMR2.0**（Goel et al., ICCV 2023）微调阶段相同的数据集（3DPW、Human3.6M、BEDLAM），保证了比较的公平性。评估时，EMDB 被划分为两个子集：子集 1 用于姿态/形状评估，子集 2 用于全局轨迹评估。

### 相机轨迹估计：双掩码策略的鲁棒性验证

Table 1 展示了在已知真实尺度条件下各方法的 ATE 表现。原始 **DROID-SLAM**（Teed & Deng, NeurIPS 2021）在存在动态人体的场景中频繁发散，而 **ORB-SLAM2**（Mur-Artal & Tardós, IEEE TRO 2017）在 25 个序列中有 9 个完全失败。TRAM 的双掩码策略（同时掩码输入图像和 DBA 置信度中的动态区域）使 DROID-SLAM 在所有序列长度分组（短 <20m、中 <60m、长 >60m）上均保持稳定，平均 ATE 达到 0.32m。消融实验（Section 4.1）进一步表明，仅掩码输入或仅掩码 DBA 均不如双掩码有效——单一掩码无法同时阻断动态人体对光流估计和稠密 BA 优化的干扰。

![[assets/figures/papers/paper_list_l1643_TRAM_Global_Trajectory_and_Motion_of_3D_Humans_from_in_the_wild_Videos/figures/004_Table_1.jpg]]
*Table 1: Evaluation of camera estimation with ground truth scale (ATE). Results are grouped according to sequence length: short(\<20m), medium(\<60m) and long(>60m). Parenthesis denote the number of sequences. ORB-SLAM2 fails in 9/25 sequences so its results are calculated with the other 16 sequences. ATE is in m*

Figure 4 的定性结果直观展示了这一机制：默认 DROID-SLAM 在人体运动剧烈时轨迹严重偏离真值，而双掩码版本始终紧贴真实轨迹。这验证了核心洞察：场景背景提供了比人体运动先验更可靠的几何约束。

### 尺度估计：从相对轨迹到度量轨迹

Table 2 评估了尺度估计后的轨迹误差（ATE-S）。直接将 **ZoeDepth** 的度量深度预测作为 DROID 输入会导致较大误差（ATE-S 平均 1.52m），因为单帧深度预测在动态场景中噪声显著。TRAM 采用鲁棒最小二乘对齐 SLAM 深度与 ZoeDepth 深度，并对整段视频取中位数估计全局尺度，将 ATE-S 降至 0.66m。

![[assets/figures/papers/paper_list_l1643_TRAM_Global_Trajectory_and_Motion_of_3D_Humans_from_in_the_wild_Videos/figures/005_Table_2.jpg]]
*Table 2: Evaluation of camera estimation with estimated scale (ATE-S). Naively using ZoeDepth predictions as depth input for DROID results in large error. The proposed method produces good scale estimation. ATE-S is in m*

消融实验（Section 3.3, 4.1）揭示了一个关键设计选择：将中位数替换为逐帧计算尺度会降低准确性。这是因为单帧深度预测的不确定性在时间维度上被中位数操作有效抑制——个别帧的离群深度值不会主导最终的尺度估计。这一机制在长序列中尤为重要，因为深度预测的累积误差可能随序列长度放大。

### 人体全局轨迹：60% 的 RTE 降低

Table 3 展示了人体全局轨迹的核心结果。TRAM 在 EMDB 上实现 RTE 1.4%，相比 **WHAM**（Shin et al., arXiv 2023）的 3.5% 降低了 60%。这一差距在长距离、复杂地形场景中尤为显著（Fig. 5 定性对比）。值得注意的是，WHAM 在比较中使用的是采用真实陀螺仪数据的版本（Fig. 6 注释），这意味着 TRAM 在输入信息更少的条件下取得了大幅领先。

误差来源分析表明，WHAM 的 RTE 误差主要来自两个方面：一是其人体运动先验在野外场景中泛化能力有限，导致尺度估计偏差；二是其相机运动推断缺乏显式的几何约束。TRAM 通过将相机轨迹估计外包给鲁棒的 SLAM 系统，并将尺度估计建立在场景背景深度对齐之上，从根源上规避了这两个问题。

### 网格重建精度与运动平滑性

Table 4 汇总了 3DPW 和 EMDB 上的网格重建精度。VIMO 在所有指标上均达到最优：3DPW 上 PA-MPJPE 35.6mm、MPJPE 59.3mm、PVE 69.6mm，加速度指标 Accel 4.9 m/s²。相比微调后的 HMR2.0 基线，VIMO 的提升来自两个时间 Transformer 的协同作用。

![[assets/figures/papers/paper_list_l1643_TRAM_Global_Trajectory_and_Motion_of_3D_Humans_from_in_the_wild_Videos/figures/009_Table_4.jpg]]
*Table 4: Comparison of mesh reconstruction on the 3DPW and EMDB datasets. HMR2.0(ft) is our baseline by finetuning HMR2.0b on the same training data as VIMO. Parenthesis denotes the number of body joints used to compute errors for the dataset. Bold numbers denote the best performance. Accel is in*

Table 5 的消融实验量化了每个时间模块的贡献：
- **移除图像域时间 Transformer**：PA-MPJPE 从 35.6 升至 36.3mm，表明图像特征的时间传播对单帧重建精度有直接增益。
- **移除运动域时间 Transformer**：加速度指标显著升高（运动平滑性下降），但单帧精度影响较小。这说明运动域 Transformer 的主要作用是抑制帧间抖动，而非提升单帧精度。

![[assets/figures/papers/paper_list_l1643_TRAM_Global_Trajectory_and_Motion_of_3D_Humans_from_in_the_wild_Videos/figures/011_Table_5.jpg]]
*Table 5: Ablation on VIMO. Removing either temporal transformer decrease reconstruction accuracy or motion smoothness. The proposed VIMO recovers accurate and smooth motion*

两个模块的分工明确：图像域 Transformer 从 ViT-H 的 patch token 序列中提取跨帧外观信息，改善遮挡和模糊帧的重建质量；运动域 Transformer 在 SMPL 姿态空间建模时序一致性，消除高频抖动。这种解耦设计使得 VIMO 在精度和平滑性上同时达到最优。

### 失败模式与局限性

尽管 TRAM 在定量指标上表现优异，论文明确指出了若干失败模式：

1. **焦距依赖**：整个流程要求已知相机焦距。在焦距未知的野外视频中，SLAM 初始化和尺度估计均会退化。这是限制 TRAM 实际部署范围的主要瓶颈。
2. **极端焦距下的深度预测**：ZoeDepth 在极端焦距（如超广角或长焦）下准确性下降，导致尺度估计偏差。这一问题在 Table 2 的长序列分组中已有体现（ATE-S 0.82m，高于短序列的 0.52m）。
3. **相机与人体未联合优化**：两阶段设计虽然高效，但相机轨迹和人体运动独立估计，可能导致脚滑移和场景穿透等物理不一致现象。论文未对此进行定量评估。
4. **遮挡与多人场景**：实验主要在单人、无严重遮挡的场景下进行，复杂交互场景的性能未经验证。
5. **离线处理**：整体流程非实时，限制了在交互式应用中的使用。

### 方法谱系与知识库定位

TRAM 在方法谱系中占据了一个独特位置：它桥接了基于 SLAM 的相机运动估计和基于学习的人体运动重建。与 **GLAMR**（Yuan et al., CVPR 2022）等纯人体位移方法相比，TRAM 用场景几何替代人体运动先验来获取尺度，避免了先验泛化性不足的问题；与 WHAM 等端到端回归方法相比，TRAM 将相机估计显式化，降低了对大规模视频训练数据的依赖。

VIMO 的设计理念——在冻结的大规模预训练图像模型（ViT-H）上添加轻量时间模块——代表了一种高效的视频模型构建范式。这与近年来的“图像预训练 + 时序微调”趋势一致，但 TRAM 通过双时间 Transformer 的解耦设计，在精度和平滑性之间取得了更好的平衡。

## 定位与知识库关联

### 全局人体运动重建的路线图

从动态相机拍摄的野外视频中重建全局人体运动，核心挑战在于同时解决“相机在哪儿”和“人在相机前如何运动”这两个耦合问题。现有方法大致沿两条路线展开：

**路线一：基于人体运动先验的回归方法。** 这类方法直接端到端地从视频像素回归人体在全局坐标系下的轨迹。代表工作包括 **GLAMR** (Yuan et al., CVPR 2022) 和 **WHAM** (Shin et al., arXiv 2023)。GLAMR 依赖人体位移推断相机运动，但缺乏绝对尺度信息，在长序列上容易累积漂移。WHAM 在 GLAMR 基础上引入惯性传感器（陀螺仪）信号辅助相机姿态估计，但其核心局限在于：人体运动先验的泛化能力受限于训练数据的多样性——当遇到训练集中未见的动作类型或地形变化时，尺度估计和轨迹预测的可靠性显著下降。

**路线二：基于SLAM的相机轨迹估计与人体重建分离的方法。** 这类方法先利用场景背景信息恢复相机运动，再在相机坐标系下重建人体。传统SLAM系统如 **ORB-SLAM2** (Mur-Artal & Tardós, IEEE TRO 2017) 依赖稀疏特征点，在动态人体场景中特征匹配容易失效（EMDB上25条序列中9条完全失败）。**DROID-SLAM** (Teed & Deng, NeurIPS 2021) 基于稠密光流和可微BA，鲁棒性更强，但原始版本未对动态物体做特殊处理，当人体占据画面较大区域时，光流估计和BA优化均被干扰，导致轨迹发散。

TRAM 的定位处于两条路线的交汇处：它继承了路线二的“场景背景提供尺度”这一核心洞察，但通过双掩码策略将 DROID-SLAM 改造为对动态人体鲁棒的相机估计器；同时借鉴了路线一的视频级人体重建思想，但将人体运动回归限制在相机坐标系下，避免了从人体运动反推全局尺度的不稳定环节。

### 关键设计决策的对比分析

**动态物体处理：掩码 vs. 隐式鲁棒性。** 原始 DROID-SLAM 假设场景是静态的，动态人体会导致光流估计错误和BA优化发散。TRAM 采用显式双掩码策略：对输入图像进行人体区域掩码，阻止错误光流进入优化；同时对DBA置信度图进行掩码，防止错误梯度反向传播（Table 1, Fig. 4）。消融实验表明，仅掩码输入或仅掩码DBA均不如双掩码有效。这一设计的因果机制在于：输入掩码阻断特征层面的污染，DBA掩码阻断优化层面的污染——两者作用于SLAM流水线的不同阶段，形成互补。

**尺度获取：场景深度对齐 vs. 人体运动推断。** WHAM 等方法的尺度信息来源于人体运动模型（如步长、身高先验），这类先验在非行走动作（如滑板、骑马）中失效。TRAM 转而利用场景深度：将 DROID-SLAM 输出的无尺度深度与 **ZoeDepth** 预测的度量深度对齐，通过鲁棒最小二乘求解全局尺度因子（Eq. 2, Section 3.3）。取中位数而非逐帧计算尺度的设计，有效抑制了单帧深度预测噪声的影响（Table 2）。这一策略的泛化性源于：场景几何（地面、墙壁）的尺度规律远比人体运动模式稳定。

**视频人体重建：冻结预训练 + 时间模块 vs. 全量微调。** **HMR2.0** (Goel et al., ICCV 2023) 作为单帧基线，在视频上逐帧处理无法利用时间信息，导致运动不平滑。TRAM 的 VIMO 在冻结的 ViT-H 骨干上添加两个时间Transformer（Fig. 3）：图像域Transformer沿时间轴传播patch token信息，提升单帧重建精度（3DPW上PA-MPJPE从36.3升至35.6，Table 5）；运动域Transformer沿时间轴传播SMPL姿态信息，提升运动平滑性（加速度指标降低，Table 5）。冻结骨干的设计降低了训练成本，使视频级建模在大规模预训练模型上变得可行。

### 适用边界与失效模式

TRAM 的有效性依赖于以下前提条件，当这些条件不满足时性能会退化：

1. **已知相机焦距。** 尺度估计阶段需要焦距参数将深度图转换为3D坐标。对于焦距未知的野外视频（如手机拍摄的变焦视频），该方法无法直接应用。这是一个硬性约束，而非精度问题。

2. **深度预测模型的泛化范围。** ZoeDepth 在极端焦距（如超广角或长焦）下预测精度下降，导致尺度估计误差增大。这限制了 TRAM 在特殊拍摄条件下的适用性。

3. **场景背景可见性。** 双掩码策略假设人体区域可以被可靠检测并掩码，且剩余背景区域足以支撑SLAM的位姿估计。在人体占据画面绝大部分（如特写镜头）或背景纹理缺失的场景中，SLAM可能退化。

4. **相机与人体运动的独立性。** TRAM 将相机轨迹和人体运动分开估计，未进行联合优化。这可能导致人体与世界坐标系的物理不一致，表现为脚滑移和场景穿透。当相机运动剧烈且人体同时快速移动时，这种解耦误差会被放大。

5. **离线处理假设。** 整个流水线（SLAM + 尺度估计 + VIMO）为离线批处理设计，不适用于实时应用场景。

### 开放问题与未来方向

1. **焦距自估计。** 如何在BA过程中自动估计焦距，使TRAM摆脱对已知内参的依赖，是拓展其适用范围的关键。可能的思路包括利用消失点检测或深度学习的单图内参估计。

2. **深度预测鲁棒性。** 针对极端焦距的深度预测模型改进，或设计焦距自适应的尺度估计策略，可提升边缘场景下的可靠性。

3. **相机-人体联合优化。** 将相机轨迹和人体运动纳入统一的BA框架，结合物理先验（如接触约束、地面穿透惩罚），有望减少滑步和穿透伪影。这需要解决两个异构优化问题的耦合挑战。

4. **时间窗口扩展与效率。** VIMO 当前的时间窗口受限于Transformer的二次复杂度。如何扩展到更长序列（如数分钟的视频）同时保持或接近实时性能，是走向实际部署的必经之路。

5. **遮挡与多人场景。** TRAM 目前主要在单人、少遮挡场景下验证。多人交互场景中的相互遮挡、身份切换等问题，需要更复杂的跟踪和重建策略。

6. **尺度估计的远距离可靠性。** 当人体距离相机较远时，深度预测的绝对误差增大，尺度估计的可靠性需要进一步验证和理论分析。

## 原文 PDF

![[paperPDFs/ECCV_2024/TRAM_Global_Trajectory_and_Motion_of_3D_Humans_from_in_the_wild_Videos.pdf]]
