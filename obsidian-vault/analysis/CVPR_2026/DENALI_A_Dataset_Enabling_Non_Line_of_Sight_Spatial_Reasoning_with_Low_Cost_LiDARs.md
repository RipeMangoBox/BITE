---
title: "DENALI: A Dataset Enabling Non-Line-of-Sight Spatial Reasoning with Low-Cost LiDARs"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DENALI_A_Dataset_Enabling_Non_Line_of_Sight_Spatial_Reasoning_with_Low_Cost_LiDARs.pdf
project_link: null
code_link: null
aliases:
- DDDDNPB
- DENALI
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 三反弹光子信号的可测量性（由回射物体保障）及数据集多样性（物体形状、尺寸、位置、光照、LiDAR分辨率）是决定数据驱动NLOS感知性能的关键控制因素。
primary_logic: 虽然低价消费级LiDAR硬件限制严重，但其全直方图已包含多反弹光子；利用大规模真实世界采集的直方图直接训练数据驱动模型，可实现鲁棒的NLOS定位、形状分类与尺寸估计，且性能受物体尺寸、位置、光照和传感器分辨率的显著调制。
claims:
- 消费级LiDAR的全直方图包含三反弹光信号，可用于非视距感知。
- DENALI是首个大规模、使用低成本LiDAR的全直方图NLOS数据集，覆盖60种物体、100个位置、两种光照和两种空间分辨率。
- 数据驱动方法可在低成本LiDAR上实现准确NLOS感知，最佳模型定位RMSE达0.046 m，尺寸预测准确率达95%。
- 数值模拟保真度影响sim-to-real迁移，真实数据在低保真度模拟时增益最大。
---

# DENALI: A Dataset Enabling Non-Line-of-Sight Spatial Reasoning with Low-Cost LiDARs

> [!tip] 核心洞察
> 虽然低价消费级LiDAR硬件限制严重，但其全直方图已包含多反弹光子；利用大规模真实世界采集的直方图直接训练数据驱动模型，可实现鲁棒的NLOS定位、形状分类与尺寸估计，且性能受物体尺寸、位置、光照和传感器分辨率的显著调制。

| 字段 | 内容 |
|------|------|
| 中文题名 | DENALI：使用低成本激光雷达实现非视距空间推理的数据集 |
| 英文题名 | DENALI: A Dataset Enabling Non-Line-of-Sight Spatial Reasoning with Low-Cost LiDARs |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.16201) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | DENALI Dataset and Data-Driven NLOS Perception Benchmark |
| Dataset | NLOS Localization, NLOS Object Classification, NLOS Size Prediction |

> [!tip] 效果简介
> - NLOS Localization 上，RMSE (m) 0.0456 (1D CNN) vs Baseline MLP (see Table 2) (see Table 2)。
> - NLOS Object Classification 上，Macro-F1 0.3832 (1D CNN) vs Baseline MLP (see Table 2) (see Table 2)。
> - NLOS Size Prediction 上，Accuracy 0.9468 (1D CNN) vs Baseline MLP (see Table 2) (see Table 2)。

## 概要

非视距（NLOS）感知旨在恢复被遮挡物体的三维信息，传统方法依赖实验室级扫描式SPAD LiDAR和基于物理模型的反演重建。然而，消费级dToF LiDAR（如ams TMF8828，仅3×3或8×8像素、128个时间bin）的粗糙时空分辨率、串扰与噪声，使得这类物理反演方法难以迁移。本文提出**DENALI**，首个大规模、使用低成本LiDAR的全直方图NLOS数据集，包含72,000个真实采集的时空直方图，覆盖60种物体形状、100个位置、两种光照条件和两种空间分辨率。

核心洞察在于：消费级LiDAR的全直方图中已包含三反弹光子信号，可直接用于数据驱动的NLOS推理，无需物理反演。实验表明，基于1D CNN的模型在定位任务上RMSE达0.0456 m，尺寸预测准确率达94.68%，验证了数据驱动范式在低成本硬件上的可行性。此外，数字孪生仿真实验揭示了仿真保真度对sim-to-real迁移的收益递减规律，以及探测器时间抖动对不同NLOS任务的差异化影响。

在方法谱系上，DENALI将NLOS感知从“实验室级硬件+物理反演”推向了“消费级传感器+数据驱动回归/分类”的新范式，为低功耗、可部署的NLOS空间推理系统提供了基准平台。



非视距（Non-Line-of-Sight, NLOS）感知旨在恢复被遮挡的隐藏物体的几何、位置或类别信息。传统NLOS成像依赖实验室级扫描式单光子雪崩二极管（SPAD）激光雷达，通过测量中继墙面上的时间分辨直方图，利用物理反演算法重建隐藏场景。这类系统具有极高的时间分辨率（通常数皮秒）和空间采样密度，能够捕获精细的光子飞行时间信息，从而支撑基于瞬态光传输模型的重建——例如共焦瞬态响应：

$$\tau ( \mathbf { x } ^ { \prime } , t ) = \iiint _ { \Omega } \rho ( \mathbf { x } ) { \frac { \delta ( 2 \| \mathbf { x } ^ { \prime } - \mathbf { x } \| - c t ) } { \| \mathbf { x } ^ { \prime } - \mathbf { x } \| ^ { 4 } } } d \mathbf { x }$$

该公式描述了中继墙面点 $\mathbf{x}'$ 处接收到的、来自隐藏体积 $\Omega$ 的瞬态直方图，其中 $\rho(\mathbf{x})$ 为物体反照率，$c$ 为光速。这一物理模型是传统NLOS重建的理论基石。

然而，**核心瓶颈在于硬件鸿沟**：消费级直接飞行时间（dToF）闪光激光雷达——如ams TMF8828（940 nm，3×3或8×8像素，仅128个时间bin）——的时空分辨率极为粗糙，且受串扰、环境噪声和探测器时间抖动（timing jitter）的严重影响。这使得基于精确物理反演的NLOS重建方法难以直接迁移到低成本传感器。现有NLOS研究几乎完全依赖昂贵的实验室硬件，缺乏在大规模、真实世界消费级传感器数据上验证数据驱动NLOS感知可行性的工作。

本文的**核心洞察**在于：尽管消费级LiDAR硬件限制严重，但其全直方图（full histogram）中已包含多反弹光子信号。如Figure 2所示，传统dToF LiDAR仅报告单次反弹（single-bounce）的深度值，但传感器实际捕获的直方图中，较晚到达的三反弹光子（three-bounce photons）编码了隐藏物体的空间信息。闪光LiDAR像素 $p$ 因其瞬时视场（iFoV）较宽，测得的直方图可建模为中继墙面区域 $\mathcal{A}_p$ 内共焦响应的加权和：

$$\tau _ { p } ( t ) = \int _ { \mathcal { A } _ { p } } w _ { p } ( \mathbf { x } ^ { \prime } ) \tau ( \mathbf { x } ^ { \prime } , t ) d \mathbf { x } ^ { \prime }$$

其中 $w_p(\mathbf{x}')$ 为像素的空间灵敏度权重。这一公式揭示了消费级传感器直方图与隐藏场景之间的可学习映射关系，为数据驱动方法提供了理论基础。

基于此，本文提出了一条互补路径：**不依赖物理反演，而是利用大规模真实世界采集的全直方图直接训练神经网络，实现鲁棒的NLOS定位、形状分类与尺寸估计**。为此，作者构建了DENALI——首个使用低成本LiDAR的大规模NLOS全直方图数据集，覆盖60种物体形状、100个位置、两种光照条件和两种传感器分辨率，共计72,000个场景。该数据集旨在系统性地探究数据驱动NLOS感知的关键控制因素：物体尺寸、位置、光照和传感器分辨率对感知性能的调制效应，以及仿真保真度对sim-to-real迁移的影响。



## 核心方法与创新机理

DENALI的核心创新不在于提出新的网络架构，而在于系统性地改变了NLOS感知的两个基础假设——**传感器硬件**与**感知范式**——从而将NLOS空间推理从实验室级设备推向消费级传感器。

### 从实验室SPAD到消费级dToF：硬件的根本性降级

传统NLOS感知依赖实验室级扫描式SPAD LiDAR，其高时间分辨率（通常为皮秒级）和密集空间采样为基于物理反演的重建方法提供了必要的数据质量。DENALI将传感器替换为消费级闪光dToF LiDAR **ams TMF8828**（940 nm），其硬件规格存在数量级差异：仅提供3×3或8×8的粗糙空间采样，时间bin宽度远大于实验室设备，且伴随显著的串扰与噪声。这一硬件降级使得传统反演方法几乎无法迁移——**真实瓶颈**在于消费级传感器的粗糙时空分辨率与多路径干扰，而非算法本身的局限。

### 从物理反演到数据驱动：感知范式的切换

与硬件的降级相匹配，DENALI在感知范式上做出了根本性切换：放弃基于物理模型（如光传输反演）的重建路径，转而采用**数据驱动的直接推理**。其核心洞察在于：尽管消费级LiDAR硬件受限，但其全直方图（full histogram）中确实包含多反弹光子信号（Figure 2中的蓝色路径），这些三反弹光信号编码了隐藏物体的几何信息。与其试图从噪声中反演场景三维结构，不如直接利用大规模真实采集的直方图训练神经网络，完成定位、形状分类和尺寸估计等具体下游任务。

这一范式切换的关键使能因素是**回射物体**（retroreflective objects）的使用：通过在隐藏物体表面粘贴回射带，显著增强了三反弹光子的可测量性，使得即使在消费级传感器的低信噪比条件下，多反弹信号仍能从背景中有效提取（通过背景减除）。

### 数据集作为核心贡献：规模、多样性与数字孪生

DENALI本身是首个大规模、使用低成本LiDAR的全直方图NLOS数据集，覆盖**60种物体形状、100个位置、两种光照条件和两种空间分辨率**，总计72,000个场景。这种多样性使得数据驱动方法能够学习到物体尺寸、位置、光照和传感器分辨率对三反弹信号的复杂调制效应。此外，每个真实采集场景都配有通过AprilTag标定和Mitsuba 3渲染生成的**数字孪生**（digital twin），为后续的sim-to-real迁移研究提供了可控的实验平台。

### 与已有工作的差异定位

已有NLOS数据集（如基于SPAD的合成或受控采集）通常假设高保真传感器和已知的光传输模型，服务于物理反演算法。DENALI则明确面向**低资源传感器**和**数据驱动方法**，其changed slots清晰界定了这一差异：传感器从实验室级扫描SPAD变为消费级闪光dToF，感知范式从模型反演变为端到端学习。这一双重切换使得DENALI成为连接消费级硬件与NLOS感知能力的桥梁数据集，而非对现有高保真NLOS方法的增量改进。



DENALI 的整体框架围绕“真实采集—数字孪生—数据驱动下游推理”三条主线展开，旨在用低成本消费级 dToF LiDAR 的全直方图直接训练神经网络，实现非视距（NLOS）定位、形状分类与尺寸预测。

### 核心瓶颈与因果机制

传统 NLOS 感知依赖实验室级扫描式 SPAD LiDAR 的高时空分辨率，通过物理反演（如共焦瞬态响应模型）重建隐藏物体。然而，消费级闪光 dToF LiDAR（如 ams TMF8828）仅提供 3×3 或 8×8 像素、128 时间 bin 的粗糙直方图，伴随严重的串扰与噪声，使得物理反演方法难以迁移。DENALI 的核心洞察在于：**即使硬件受限，全直方图中已包含三反弹光子信号**（Figure 2），该信号编码了隐藏物体的几何与位置信息。通过构建大规模真实采集数据集并直接训练数据驱动模型，可绕过物理反演，实现鲁棒的 NLOS 感知。

![[assets/figures/papers/paper_list_l817_https_arxiv_org_abs_2604_16201/figures/002_Figure_2.jpg]]
*Figure 2: Non-line-of-sight signal in mobile LiDARs. Conventional direct time-of-flight (dToF) LiDARs report depth measurements corresponding to primary single-bounce reflections (shown in red). However, dToF LiDARs can also capture later-arriving multi-bounce photons (shown in blue); this three-bounce light signal can encode information about hidden scene objects which may be used for non-line-of-sight inference*

性能的关键控制因素包括：回射物体保障的三反弹信号可测量性、物体尺寸与位置、光照条件以及 LiDAR 空间分辨率。这些因素在 DENALI 中被系统性地变化，以评估其对下游任务性能的调制效应。

### Pipeline 模块与数据流

**模块一：真实采集与背景减除。** 采集系统（Figure 3）由消费级闪光 dToF LiDAR（ams TMF8828，940 nm）与 Intel RealSense RGB-D 相机共轴对准平面中继墙构成，隐藏物体安装在电动龙门架上，位于传感器直视线之外。对每个场景，分别采集带隐藏物体和无隐藏物体的全直方图，相减后得到三反弹信号（Table 1 报告了信号的统计特征）。数据集覆盖 60 种物体形状（10 字母、10 数字、10 形状，各含 4 英寸与 8 英寸两种尺寸）、100 个龙门架位置、两种光照条件（开灯/关灯）和两种 LiDAR 分辨率（3×3 与 8×8），总计 72,000 幅时空直方图。

**模块二：数字孪生生成。** 利用 AprilTag 标定获取传感器、中继墙与隐藏物体的 6-DoF 位姿，结合已知的刚体变换，在 Mitsuba 3 渲染器中为每一幅真实场景重建数字孪生。数字孪生用于分析仿真-真实域差异，并通过逐步增加仿真保真度（缩放、脉冲宽度、噪声）量化 sim-to-real 迁移效果。

**模块三：下游任务训练与评估。** 将背景减除后的直方图输入四种基线模型——无时空归纳偏置的 Baseline MLP、仅利用时间维度的 1D CNN、同时利用时空结构的 3D CNN、以及以时间 bin 为 token 的 Transformer——完成三项 NLOS 任务：定位回归（RMSE/MAE）、物体分类（Top-1/Top-5/Macro-F1）和尺寸预测（Precision/Recall/Accuracy）。模型输出直接预测隐藏物体的 3D 位置、形状类别或尺寸标签，无需中间重建步骤。

### 关键公式

框架的物理基础由两个公式描述。共焦瞬态响应（Eq. 1）给出了中继墙面点 $\mathbf{x}'$ 处接收到的理想直方图：

$$
\tau ( \mathbf { x } ^ { \prime } , t ) = \iiint _ { \Omega } \rho ( \mathbf { x } ) { \frac { \delta ( 2 \| \mathbf { x } ^ { \prime } - \mathbf { x } \| - c t ) } { \| \mathbf { x } ^ { \prime } - \mathbf { x } \| ^ { 4 } } } d \mathbf { x }
$$

其中 $\Omega$ 为隐藏体积，$\rho(\mathbf{x})$ 为物体反照率。由于闪光 LiDAR 像素的瞬时视场较宽，像素 $p$ 实际测得的直方图为中继墙面区域 $\mathcal{A}_p$ 内共焦响应按空间灵敏度 $w_p$ 的加权和（Eq. 2）：

$$
\tau _ { p } ( t ) = \int _ { \mathcal { A } _ { p } } w _ { p } ( \mathbf { x } ^ { \prime } ) \tau ( \mathbf { x } ^ { \prime } , t ) d \mathbf { x } ^ { \prime }
$$

这两个公式共同说明：即使空间分辨率极低，像素直方图仍以积分形式保留了隐藏物体的时空信息，为数据驱动方法提供了信息论基础。

### 补充图表

![[assets/figures/papers/paper_list_l817_https_arxiv_org_abs_2604_16201/figures/003_Figure_3.jpg]]
*Figure 3: Capture setup. Our capture system is designed to record a large-scale dataset of non-line-of-sight, three-bounce light signals from a mobile flash LiDAR. The setup includes a low-cost single-photon LiDAR co-located with an Intel RealSense RGB-D camera, both directed toward a flat relay wall. A hidden object is mounted on a motorized gantry positioned outside their direct line of sight to ensure only indirect three-bounce returns are measured. An additional overhead RealSense tracking camera observes the entire scene, providing accurate localization of the LiDAR, relay wall, and hidden object during data collection*



### 3.1 NLOS信号形成模型

消费级dToF LiDAR的NLOS感知建立在三反弹光路模型之上。传感器向中继墙面发射激光脉冲，光子经墙面反射至隐藏物体，再由物体返回墙面，最终被传感器接收。这一过程可用共焦瞬态响应描述：

$$
\tau ( \mathbf { x } ^ { \prime } , t ) = \iiint _ { \Omega } \rho ( \mathbf { x } ) { \frac { \delta ( 2 \| \mathbf { x } ^ { \prime } - \mathbf { x } \| - c t ) } { \| \mathbf { x } ^ { \prime } - \mathbf { x } \| ^ { 4 } } } d \mathbf { x }
$$

其中，$\mathbf{x}'$为中继墙面上的测量点，$\Omega$为隐藏物体所在体积，$\rho(\mathbf{x})$为物体表面反照率，$c$为光速。该公式编码了隐藏物体的几何与反射特性：距离项$\|\mathbf{x}' - \mathbf{x}\|$决定了光子飞行时间，分母的四次方衰减反映了往返路径损耗。

然而，消费级闪光LiDAR的每个像素具有较宽的瞬时视场（iFoV），实际测量值是墙面区域内共焦响应的加权积分：

$$
\tau _ { p } ( t ) = \int _ { \mathcal { A } _ { p } } w _ { p } ( \mathbf { x } ^ { \prime } ) \tau ( \mathbf { x } ^ { \prime } , t ) d \mathbf { x } ^ { \prime }
$$

其中，$\mathcal{A}_p$为像素$p$对应的中继墙面区域，$w_p(\mathbf{x}')$为空间灵敏度权重。这一宽视场积分是消费级传感器与实验室扫描式SPAD的根本差异：前者牺牲了空间分辨能力，但保留了全直方图中的多反弹光子信息。

### 3.2 关键硬件约束与信号可测性

本文使用的**ams TMF8828**传感器（940 nm消费级闪光dToF）具有两个关键限制：（1）空间分辨率仅为3×3或8×8像素；（2）时间分辨率仅128个时间bin。这导致传统基于物理反演的NLOS重建方法（依赖高时空分辨率的瞬态测量）难以直接迁移。

为使三反弹信号在如此粗糙的硬件上可测，系统设计引入了两个控制因素：
- **回射物体**：隐藏物体表面贴有回射带，优先将光线沿入射方向返回，显著增强三反弹光子产额。
- **背景减除**：对每个场景采集带物体/无物体两组直方图，相减提取纯净的三反弹信号，抑制单反弹和散射本底。

### 3.3 数字孪生生成管线

为支持仿真-真实迁移研究，本文为每幅采集场景构建数字孪生。流程如下：
1. 利用**AprilTag**标定传感器、中继墙面和隐藏物体的6-DoF位姿；
2. 将标定位姿与已知刚体变换输入**Mitsuba 3**渲染器，生成对应仿真直方图；
3. 仿真管线可灵活注入缩放因子、脉冲宽度、噪声模型等参数，用于分析不同保真度对下游任务的影响。

### 3.4 下游任务模型架构

本文评估了四种利用直方图时空结构的不同模型，作为数据驱动NLOS感知的基准：

| 模型 | 结构特点 | 归纳偏置 |
|------|----------|----------|
| Baseline MLP | 将3×3×128直方图展平后通过全连接网络 | 无时空归纳偏置 |
| 1D CNN (Time-Only) | 仅沿时间维度一维卷积 | 时序局部性 |
| 3D CNN (Spatiotemporal) | 同时在空间和时间维度三维卷积 | 时空局部性 |
| Transformer (Time-Token) | 以时间bin为token的自注意力编码器 | 长程时序依赖 |

所有模型共享相同的输入（背景减除后的像素直方图）和输出头（回归头用于定位，分类头用于形状/尺寸预测），差异仅在于对时空结构的利用方式。



## 实验与关键发现

### 基准任务与模型架构

为系统评估低成本LiDAR在NLOS空间推理中的能力，DENALI定义了三个下游任务：**定位回归**（预测隐藏物体的2D平面坐标）、**形状分类**（30类物体识别）和**尺寸预测**（4英寸 vs. 8英寸二分类）。所有任务均以背景减除后的全直方图作为输入。

基线模型覆盖四种不同的时空归纳偏置设计：
- **Baseline MLP**：将 `3×3×128` 或 `8×8×128` 直方图展平后送入全连接网络，无任何空间或时序结构先验。
- **1D CNN（Time-Only）**：仅沿时间维度进行一维卷积，捕捉时序特征但忽略像素间空间关系。
- **3D CNN（Spatiotemporal）**：同时利用空间和时间维度的三维卷积，具备完整的时空归纳偏置。
- **Transformer（Time-Token Encoder）**：将每个时间bin作为token输入自注意力模块，建模长程时序依赖。

### 主实验结果

Table 2汇总了各模型在全部任务上的性能。核心发现如下：

**定位任务**：1D CNN取得最优RMSE **0.0456 m**，显著优于Baseline MLP。值得注意的是，3D CNN并未因引入空间结构而获得额外增益，暗示在 `3×3` 的低空间分辨率下，时序信息已足以编码位置线索。Figure 6进一步揭示了误差的空间分布：大尺寸（8英寸）物体靠近中继墙面时精度更高，但不同光照条件导致截然不同的误差模式——这表明模型难以解耦物体属性、几何位置与光照三者的耦合效应。

**形状分类任务**：1D CNN的Macro-F1达到 **0.3832**（Top-1准确率约38%），远高于随机水平（~3.3%），但绝对性能仍有较大提升空间。Figure 7显示，8英寸物体的分类准确率显著高于4英寸物体，验证了三反弹信号强度对感知能力的决定性影响——更大物体产生更强的回波信号。

**尺寸预测任务**：1D CNN取得 **94.68%** 的准确率，表明即使在低分辨率传感器下，尺寸这一粗粒度属性仍可被可靠提取。

### 消融分析：仿真保真度与Sim-to-Real迁移

DENALI为每个采集场景构建了Mitsuba 3数字孪生，使得系统研究仿真-真实域差异成为可能。Figure 9展示了逐步提升模拟保真度（依次加入：强度缩放、脉冲宽度建模、噪声注入）对定位RMSE的影响：

- **Sim-only**条件下，低保真度模拟的RMSE较高；随着保真度提升，性能单调改善但呈现**收益递减**——从脉冲宽度到噪声注入的增益远小于从纯几何到强度缩放的跃升。
- 当在仿真数据中混入少量真实训练样本时，**低保真度模拟获得最大增益**，高保真度模拟的增益则相对有限。这一发现具有实践指导意义：在真实采集成本高昂的场景下，优先提升模拟保真度可减少对真实数据的依赖，但完全替代仍不可行。

Table 3分析了探测器时间抖动（Gaussian FWHM）对下游任务的影响，揭示了任务间的差异化敏感度：
- **定位和尺寸预测**在抖动增至约600 ps FWHM时性能开始明显下降。
- **物体分类**对中等抖动（~100 ps）反而表现出轻微提升，可能源于适度时序模糊有助于抑制高频噪声、增强形状相关的中频特征。这一反直觉现象需要进一步验证。

### 失败模式与局限性

1. **小尺寸物体感知困难**：4英寸物体的分类和定位精度显著低于8英寸物体，根源在于三反弹光子数随物体表面积减小而急剧下降，信噪比恶化。
2. **光照-几何耦合**：Figure 6中不同光照下误差模式的显著差异表明，当前数据驱动模型未能有效解耦光照变化与物体位置/形状的编码，泛化到新光照条件时性能可能退化。
3. **空间分辨率瓶颈**：3D CNN未优于1D CNN的事实暗示，`3×3` 像素阵列提供的空间信息极为有限，可能不足以支撑有意义的空间特征学习。
4. **受控场景假设**：所有实验均依赖回射带增强信号、固定传感器-墙面几何关系及静态场景，向无约束真实环境的推广仍是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l817_https_arxiv_org_abs_2604_16201/figures/005_Table_1.jpg]]
*Table 1: Statistical analysis of three-bounce signal. For each capture, we subtract the corresponding no-object background to isolate the three-bounce return. We report mean ± SEM for pixels [1,1] (3 × 3) and [2,1] (8 × 8)*

![[assets/figures/papers/paper_list_l817_https_arxiv_org_abs_2604_16201/figures/008_Figure_6.jpg]]
*Figure 6: Spatial mapping of NLOS localization accuracy. We plot RMSE (m) over true gantry positions for a single trained model (1D CNN) broken down by size/lighting. Accuracy generally improves for larger (8in.) objects nearer to relay wall. However, different lighting induces distinct spatial error patterns, suggesting poor separation of object, geometry, and lighting*

![[assets/figures/papers/paper_list_l817_https_arxiv_org_abs_2604_16201/figures/009_Table_2.jpg]]
*Table 2: Benchmarking NLOS perception tasks using low-cost LiDARs with DENALI. We report performance for (a) location regression (RMSE / MAE), (b) object classification (Top-1 / Top-5 / Macro-F1), and (c) size prediction (Precision / Recall / Accuracy). Results are reported overall and by scene factors; CNN-based models perform best but remain dependent on object size, position, and shape*

![[assets/figures/papers/paper_list_l817_https_arxiv_org_abs_2604_16201/figures/010_Figure_7.jpg]]
*Figure 7: NLOS classification accuracy across object types. We train a 1D CNN independently for each object size and evaluate classification performance across shapes; larger 8-inch objects yield consistently higher accuracy*

![[assets/figures/papers/paper_list_l817_https_arxiv_org_abs_2604_16201/figures/013_Table_3.jpg]]
*Table 3: Effect of detector timing jitter (Gaussian FWHM in ps) on downstream NLOS perception tasks, applied to 3 × 3 centerpixel histograms during training and evaluation*



## 定位与知识库关联

### 从物理反演到数据驱动：NLOS感知的范式转折

传统非视距（NLOS）感知的核心范式建立在**基于物理模型的反演重建**之上。其理论基础可追溯到共焦瞬态响应方程：

$$\tau ( \mathbf { x } ^ { \prime } , t ) = \iiint _ { \Omega } \rho ( \mathbf { x } ) { \frac { \delta ( 2 \| \mathbf { x } ^ { \prime } - \mathbf { x } \| - c t ) } { \| \mathbf { x } ^ { \prime } - \mathbf { x } \| ^ { 4 } } } d \mathbf { x }$$

该方程编码了中继墙面点 $\mathbf{x}'$ 处接收到的光子飞行时间直方图与隐藏体积 $\Omega$ 内物体形状、反照率之间的确定性关系。然而，这一范式的有效运作高度依赖**实验室级扫描式SPAD LiDAR**——其高时间分辨率（皮秒级）和高空间分辨率（逐点扫描）是反演算法收敛的前提。

DENALI的工作标志着一次关键的范式转折：**将NLOS感知从物理反演问题重新定义为数据驱动的直方图-属性映射问题**。这一转折的因果扳机在于消费级闪光dToF LiDAR（ams TMF8828）的硬件特性——仅3×3或8×8像素、128个时间bin的粗糙时空分辨率——使得传统反演方法在数学上不可行。但核心洞察在于，**即便硬件严重受限，全直方图中仍包含可测量的三反弹光子信号**（Figure 2），且其统计特征（强度、质心、扩展、偏度）随物体属性呈现系统性变化（Table 1）。

### 模型架构谱系：时空归纳偏置的消融研究

DENALI构建的基线模型谱系构成了对**时空归纳偏置在低分辨率NLOS感知中作用**的系统消融。四种架构形成从无偏置到强偏置的连续谱：

1. **Baseline MLP**：将3×3×128直方图完全展平输入全连接网络，无任何空间或时间归纳偏置。该模型作为性能下界，检验纯粹从统计相关性中学习的可能性。

2. **1D CNN (Time-Only)**：仅沿时间维度施加卷积，捕捉单像素内的时间结构，但忽略空间布局。该架构在定位任务上取得最优RMSE 0.0456 m，暗示**时间结构携带的NLOS信息远多于空间结构**。

3. **3D CNN (Spatiotemporal)**：同时利用空间和时间维度的三维卷积，理论上应捕捉跨像素的时空关联，但在低分辨率（3×3）下空间信息极为有限，实际增益微弱。

4. **Transformer (Time-Token Encoder)**：以时间bin为token的自注意力模型，旨在捕捉长程时序依赖。在128-bin的短序列上，自注意力的长程建模优势未能充分体现。

这一谱系揭示了一个反直觉的发现：在消费级LiDAR的极端低分辨率条件下，**简单的时间卷积已足够提取三反弹信号的关键特征**，更复杂的时空或注意力机制带来的边际收益有限。这与此前基于实验室级数据的工作形成鲜明对比——后者通常依赖复杂的3D反演网络或物理先验嵌入。

### 数据集设计的因果逻辑：回射物体作为可控变量

DENALI数据集设计的核心因果逻辑在于**通过回射物体（retroreflective objects）将三反弹信号提升至消费级传感器可测量的水平**。这一设计选择既是使能条件，也是适用边界：

- **使能逻辑**：回射带优先沿入射方向返回光子，使得即使在3×3像素、128-bin的粗糙分辨率下，三反弹信号仍具有统计可区分性（Table 1中总强度560.36±6.08 counts for 4in. objects under lights-on）。
- **边界约束**：该设计同时限定了当前结论的适用范围——所有60种物体（10字母+10数字+10形状，4英寸和8英寸两种尺寸）均贴有回射带，**未验证对普通朗伯材质或镜面材质的适用性**。

这一设计决策将“物体材质”从变量转化为常数，使得研究聚焦于**物体形状、尺寸、位置、光照和传感器分辨率**对NLOS感知性能的调制效应。这是受控实验的合理取舍，但也意味着向无约束真实场景推广时，**材质多样性将成为首要挑战**。

### 仿真-真实域迁移的知识贡献

DENALI通过为每幅采集场景构建Mitsuba 3数字孪生（利用AprilTag标定的6-DoF位姿），首次系统量化了**仿真保真度对NLOS sim-to-real迁移的边际效应**。Figure 9的消融曲线揭示了两个关键规律：

1. **收益递减律**：依次添加缩放校准、脉冲宽度建模、噪声建模可逐步降低sim-only RMSE，但增益递减。这表明存在一个“足够好”的仿真保真度阈值，超过后继续提升保真度的性价比急剧下降。

2. **真实数据的杠杆效应**：在低保真度仿真下，添加少量真实训练样本带来最大性能增益；随着仿真保真度提升，真实数据的边际贡献降低。这一发现为**有限真实数据预算下的最优数据混合策略**提供了实证指导。

此外，Table 3对探测器时间抖动的消融揭示了**不同NLOS任务对硬件噪声的差异化敏感度**：定位和尺寸预测在~600 ps FWHM时性能开始下降，而物体分类在中等抖动（~100 ps）下反而略有提升——这一非单调现象暗示适度的时序模糊可能有助于提取形状的全局特征。

### 适用边界与局限

当前工作的适用边界由以下约束共同定义：

1. **硬件单一性**：所有实验仅基于ams TMF8828单一型号，该传感器的时间bin宽度、像素数和噪声特性构成了当前结论的硬件前提。不同厂商的消费级dToF传感器（如STMicroelectronics VL53L系列）可能呈现不同的信号特征。

2. **场景静态性**：采集假设场景完全静态，未涵盖移动物体或动态遮挡。现实应用中，行人、车辆等动态元素将引入时变的三反弹信号，需要时序建模或在线适应机制。

3. **背景减除依赖**：三反弹信号的提取依赖固定场景的背景减除（带物体/无物体直方图相减），这在非受控环境中难以实现——无物体的“纯净背景”通常不可得。

4. **中继墙面已知性**：当前设置假设中继墙面为固定平面且位置已知，未探索墙面几何未知或非平面（如曲面、粗糙表面）的情况。

### 开放问题与未来方向

DENALI在NLOS感知知识库中的定位指向以下开放问题：

1. **材质泛化**：如何将数据驱动的NLOS感知推广至无回射带的普通材质？可能的路径包括物理增强的数据增广（在仿真中建模不同BRDF）、域自适应方法，或设计对材质不敏感的直方图特征。

2. **传感器-任务协同设计**：当前工作揭示了不同任务对时间抖动的差异化敏感度，但未系统探索最优传感器配置。针对定位、分类或尺寸预测任务，**最优的像素数、时间bin宽度和激光功率组合**是什么？这属于传感器-算法协同设计的范畴。

3. **可解耦表征学习**：Figure 6显示不同光照条件下定位误差的空间分布呈现不同模式，暗示物体几何、位置和光照在直方图特征中存在纠缠。开发可解耦这些因素的模型（如变分自编码器或因果表征学习）是提升泛化能力的关键。

4. **动态场景扩展**：将静态NLOS感知扩展至动态场景需要解决两个子问题：运动物体的三反弹信号跟踪，以及多物体场景中的信号分离。单像素直方图的时序演化可能携带运动信息，但当前128-bin的时间分辨率限制了速度测量精度。

5. **无背景减除的端到端感知**：摆脱背景减除依赖需要模型直接从原始直方图（包含单反弹、环境光和暗计数）中提取三反弹信号。这本质上是一个盲源分离问题，可能需要自监督预训练或物理引导的注意力机制。

**需要手动验证的点**：上述分析中关于“此前基于实验室级数据的工作通常依赖复杂3D反演网络”的对比陈述，基于对NLOS重建文献的一般性了解，而非本文明确引用的具体基线。如需精确的文献对比，建议核实近期NLOS重建综述（如Faccio et al., Nature Reviews Physics 2020）中列举的代表性方法。



## 原文 PDF

![[paperPDFs/CVPR_2026/DENALI_A_Dataset_Enabling_Non_Line_of_Sight_Spatial_Reasoning_with_Low_Cost_LiDARs.pdf]]
