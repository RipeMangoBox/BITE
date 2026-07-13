---
title: Breaking the Scalability Limit of Multi-Projector Calibration with Embedded Cameras
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Breaking_the_Scalability_Limit_of_Multi_Projector_Calibration_with_Embedded_Cameras.pdf
project_link: "https://www.xr.sys.es.osaka-u.ac.jp/"
code_link: null
aliases:
- MPCECP
- BSLMPCEC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将相机嵌入标定板表面，使光学中心与标定平面共面，直接按入射方向捕获投影光，实现多投影仪图案的方向性分离。
primary_logic: 通过反向配置（相机朝向投影仪并作为标定目标），利用嵌入式相机直接捕获方向编码光，从单次采集即可同时解码多个投影仪的图案，打破串行标定的可扩展性限制。
claims:
- 嵌入式相机利用入射角度分离同时投影的结构光图案（类似光场相机原理），从而建立相机光心坐标与投影仪像素的对应关系。
- 在3台投影仪上，经过光学中心偏移补偿后，本文方法的重投影误差低于1像素（0.89–0.91），与使用4个角点的传统方法相当，证明其标定精度足以实用。
- 同时投影将所需投影图案数从传统方法的1,100幅降至54幅，减少95%，大幅提升标定效率。
- 在约70 klux的户外阳光下，本文方法仍能成功分离并解码两投影仪的结构光图案，而传统方法完全失效，验证了其对强环境光的鲁棒性。
---

# Breaking the Scalability Limit of Multi-Projector Calibration with Embedded Cameras

> [!tip] 核心洞察
> 通过反向配置（相机朝向投影仪并作为标定目标），利用嵌入式相机直接捕获方向编码光，从单次采集即可同时解码多个投影仪的图案，打破串行标定的可扩展性限制。

| 字段 | 内容 |
|------|------|
| 中文题名 | 嵌入摄像头的多投影仪可扩展标定方法 |
| 英文题名 | Breaking the Scalability Limit of Multi-Projector Calibration with Embedded Cameras |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.24024) · [Project](https://www.xr.sys.es.osaka-u.ac.jp/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Multi-Projector Calibration with Embedded Cameras (proposed) |
| Dataset | 3-projector system, 25-projector array, Outdoor ambient light (~70 klux sunlight), 2 projectors |

> [!tip] 效果简介
> - 3-projector system (Optoma ML1050ST+, BenQ TK685, BenQ TK850) 上，RMS reprojection error (pixels) @ 4 reference points 0.89–0.91 (with compensation) vs 0.65–0.76 (conventional with 4 corners) (~ +0.2 px (slightly less accurate but <1 pixel, considered acceptable))。
> - 25-projector array (simulated with 5 × 5 shifted positions) 上，number of required patterns per board pose 54 (simultaneous projection from all projectors) vs 1,100 (sequential projection, conventional method) (95% reduction)。
> - Outdoor ambient light (~70 klux sunlight), 2 projectors 上，successful pattern separation and geometric alignment successful (accurate checkerboard alignment) vs fail (projected patterns overwhelmed by ambient light) (proposed robust to 70 klux, conventional completely fails)。

## 概要

多投影仪系统在沉浸式显示、空间增强现实和大屏拼接等应用中日益普及，但其规模化部署始终受制于一个根本瓶颈：**标定时间随投影仪数量线性增长**。传统方法依赖外部相机捕获漫反射的结构光图案，由于漫反射丧失了入射方向信息，不同投影仪同时投射的图案在相机像面上完全重叠、无法分辨。因此必须串行投影——一台接一台地标定——导致所需投影图案数按 $M \times (\lceil \log_2 W \rceil + \lceil \log_2 H \rceil + L)$ 线性增长，其中 $M$ 为投影仪数量。当系统规模达到数十台时，标定过程变得极其耗时，严重制约了多投影系统的可扩展性。

本文提出了一种**反向配置**方案，从根本上打破了这一可扩展性限制。核心思路是将微型摄像头嵌入标定板表面，使相机光学中心与标定平面共面，从而**直接按入射方向捕获投影光**。这一方向编码特性类似于光场相机的原理：来自不同位置的投影仪光线，因入射角不同而落在嵌入式相机的不同像素上，实现了多投影仪图案在空间上的自然分离。由此，所有投影仪可同时投影结构光图案，从单次采集即可并行解码每台投影仪的像素对应关系。

在方法定位上，本文工作属于**基于结构光的投影仪标定**路线，但将标定目标的角色从“被观测的被动参考物”转变为“主动观测的多目传感阵列”。与传统的 Zhang 方法（Zhang, IEEE TPAMI 2000）相比，本文在三个关键环节做出了改变：（1）图案分离机制从时间串行转为方向空间分离；（2）标定参考点从印刷棋盘角点转为嵌入式相机的光学中心；（3）所需投影图案数从 $O(M)$ 降至 $O(\log M)$。

实验结果表明，该方法在3台真实投影仪上实现了低于1像素的重投影误差（0.89–0.91像素），与使用4个棋盘角点的传统方法精度相当。在25台投影仪的模拟阵列中，同时投影将所需图案数从传统方法的1,100幅降至54幅，**减少95%**。此外，在约70 klux的户外阳光直射条件下，本文方法仍能成功分离并解码结构光图案，而传统方法因环境光淹没投影图案完全失效，验证了其对强环境光的鲁棒性。

本方法的主要局限在于：要求所有投影仪共享公共投影区域，对于不重叠的大范围部署需分组标定；目前仅支持平面标定靶；精度略低于使用大量棋盘角点的传统方法（约+0.2像素），但可通过增加嵌入式相机数量进一步提升。



### 多投影仪系统的标定瓶颈

大规模多投影仪系统（如沉浸式显示墙、投影映射、光雕投影）需要精确的几何标定，以确保多台投影仪输出的图像在空间上无缝对齐。标定的核心任务是建立每台投影仪像素坐标与三维空间中对应点之间的映射关系，即估计投影仪的内参（焦距、光心）和外参（位置与朝向）。

传统标定方法普遍采用**外部相机**作为观测中介：将印有已知棋盘格图案的平板置于投影区域，每台投影仪依次投射结构光图案（如 Gray-code 或相移条纹）到该平板上，外部相机通过捕获漫反射光来解码投影仪像素与棋盘角点之间的对应关系，进而利用 **Zhang 的平面标定法**（Zhang, IEEE TPAMI 2000）求解投影仪参数。这一串行流程存在一个根本性的可扩展性瓶颈：

> **当多台投影仪同时投影时，外部相机捕获的是所有投影仪图案在漫反射表面上的叠加混合信号，丧失了入射方向信息，无法区分各投影仪的图案。因此，必须采用时分复用的串行投影策略，导致标定时间随投影仪数量线性增长。**

具体而言，对于 M 台分辨率为 W×H 的投影仪，若每台使用 Gray-code 和 L 幅线移图案，传统方法所需的投影图案总数为：

$$M \times ( \lceil \log_2 W \rceil + \lceil \log_2 H \rceil + L )$$

该数量随 M 线性增长。当 M 达到数十甚至上百台时，标定过程变得极其耗时，成为大规模投影系统部署的关键障碍。此外，外部相机对环境光敏感，在户外强光条件下，投影图案极易被环境光淹没，进一步限制了方法的适用场景。

### 核心洞察：从“看向投影面”到“看向投影仪”

本文的根本洞察在于**反转观测方向**：将相机嵌入标定板的表面，使其光学中心与标定平面共面，相机直接朝向投影仪而非投影面。这一反向配置带来了决定性的能力跃迁——嵌入式相机以**方向编码**的方式直接捕获入射投影光：来自不同空间位置的投影仪，其光线以不同角度到达相机，在相机像面上落在不同像素上。这种方向性编码特性类似光场相机的原理，使得从**单次同时投影**中即可按入射角度分离并解码多台投影仪的结构光图案，从而彻底打破了串行标定的可扩展性限制。

通过这一机制，本文方法将所需投影图案数降至：

$$\lceil \log_2 M \rceil + \lceil \log_2 W \rceil + \lceil \log_2 H \rceil + L$$

其中与投影仪数量相关的项仅为 ⌈log₂ M⌉（一个微小的常数增量），使得标定时间几乎与投影仪数量解耦。

### 本文动机与目标

基于上述洞察，本文旨在建立一套**可扩展的多投影仪同时标定框架**，其核心目标包括：

1. **打破串行标定瓶颈**：通过嵌入式相机的方向分离能力，实现所有投影仪的同时标定，将投影图案数量从线性增长压缩为近乎常数。
2. **保证标定精度**：在显著提升效率的同时，维持与传统方法可比的重投影精度（亚像素级）。
3. **增强环境光鲁棒性**：利用嵌入式相机直接接收投影光（而非依赖漫反射），在强环境光（如户外阳光）下仍能可靠工作。
4. **补偿系统误差**：通过离线标定的单应变换，补偿嵌入式相机光学中心与标定板平面之间的微小偏移，确保高精度几何对齐。



## 核心方法与创新机理

本文的核心创新在于**将相机从“观察者”变为“标定目标”**，从根本上改变了多投影仪标定中图案分离的物理机制，从而突破了串行标定的可扩展性瓶颈。

### 瓶颈诊断：外部相机丢失方向信息

传统多投影仪标定方法（如 **Zhang** (IEEE TPAMI 2000) 的平面标定法）依赖一台外部相机，通过漫反射捕捉投影到标定板上的结构光图案。这一采集方式存在一个根本性缺陷：**漫反射过程抹去了投影光的入射方向信息**。当多台投影仪同时向同一区域投影时，外部相机像面上的每个像素接收的是来自所有投影仪的光线叠加，无法区分各图案的来源（见 Figure 1(a)）。因此，传统方法被迫采用**串行投影**——每次只让一台投影仪工作，用时间换空间。这导致所需投影图案数量随投影仪数量 $M$ 线性增长：

$$M \times ( \lceil \log_2 W \rceil + \lceil \log_2 H \rceil + L )$$

其中 $W \times H$ 为投影仪分辨率，$L$ 为线移图案数。当 $M$ 增大到数十台时，标定时间变得不可接受，成为大规模投影系统的可扩展性瓶颈。

### 核心机制：方向编码实现图案空间分离

本文方法的核心洞察是**反向配置**：将微型相机嵌入标定板表面，使其光学中心与标定平面共面，相机朝向投影仪并直接捕获入射光（见 Figure 1(b)）。这一配置带来了关键的物理性质变化：

- **方向编码**：由于嵌入式相机直接接收投影光，不同位置的投影仪发出的光线以不同角度入射，落在相机像面的**不同像素**上。这一性质类似于光场相机的方向编码原理——每个像素不仅记录亮度，还隐含了入射方向信息。
- **单次采集即分离**：所有投影仪可同时投影各自的 Gray-code 图案、线移图案和投影仪 ID 编码序列。嵌入式相机以高时间分辨率捕获这些序列后，对每个像素独立解码：先通过阈值检测判定该像素是否接收到投影光，再解码投影仪 ID 以确定光源，最后解码 Gray-code 和线移图案以获得对应的投影仪像素坐标 $p_m(n)$。

这一机制将图案分离从“时间域”移到了“空间域”，使得**同时投影、单次采集**成为可能。所需投影图案数从线性项 $M$ 降至对数项 $\lceil \log_2 M \rceil$：

$$\lceil \log_2 M \rceil + \lceil \log_2 W \rceil + \lceil \log_2 H \rceil + L$$

在 25 台投影仪的实验中，这一改变将每姿态所需图案从 1,100 幅降至 54 幅，**减少 95%**。

### 配套创新：光学中心偏移补偿

嵌入式相机带来了一个新问题：相机的光学中心不可能完全精确地落在标定板平面上，导致光线在板平面的实际交点 $x_n(m)$ 偏离相机的标称位置 $x_n$（见 Figure 3）。这引入了系统性的几何误差。

本文通过**离线单应标定**解决此问题：对每台嵌入式相机 $n$，估计一个单应矩阵 $\mathcal{M}_n$，将相机像素坐标 $c_n(m)$ 映射为板平面上的实际交点：

$$\pmb{x}_n(m) = \mathcal{M}_n(\pmb{c}_n(m))$$

该映射随后作为 Zhang 标定方法的输入，替代标称位置。消融实验表明，**移除该补偿后重投影误差从约 0.9 像素升至 2.2–2.5 像素**（Table 1），且 25 台投影仪的对齐结果出现明显模糊（Figure 10），验证了补偿步骤对高精度标定的必要性。

### 创新带来的附加优势

方向编码机制还带来了一个意外收益：**对环境光的天然鲁棒性**。外部相机采集漫反射光，环境光直接叠加在投影图案上，强光下信噪比急剧下降。而嵌入式相机直接捕获来自投影仪的定向光，环境光（漫射光）仅作为均匀偏置，可通过阈值检测有效滤除。实验表明，在约 **70 klux** 的户外阳光下，本文方法仍能成功分离并解码两投影仪的结构光图案，而传统方法完全失效（Figure 12）。

### 方法谱系与知识库定位

本工作处于**多投影仪标定**与**计算成像**的交叉点：

- **上游基础**：继承 Zhang 的平面标定框架（Zhang, IEEE TPAMI 2000）作为参数估计后端，利用其成熟的闭式解和优化方法。
- **方向编码原理**：借鉴光场相机（如 Ng et al., 2005）的微透镜阵列方向采样思想，但将其反转——不是用微透镜阵列对场景光进行方向采样，而是用嵌入式相机阵列对投影光进行方向分离。
- **结构光编码**：采用经典的 Gray-code 加线移图案方案，额外增加投影仪 ID 的二进制时间编码，实现对多投影仪源的区分。
- **差异化定位**：与基于外部相机阵列或全光相机的方法不同，本文不增加外部观测设备，而是将相机微型化并嵌入标定目标本身，实现了“标定目标即传感器”的范式转换。



本文提出的多投影仪标定方法通过**反向配置**彻底重构了传统标定流程：将相机从“外部观察者”转变为“嵌入式方向传感器”，从而将标定效率从与投影仪数量线性相关压缩为近乎常数。

### 核心流程

整个标定流程由**离线准备**和**在线标定**两个阶段构成，二者通过预标定的单应映射衔接。

**在线标定阶段**（核心创新）包含以下步骤：

1. **同时投影编码图案**：所有 $M$ 台投影仪同时向标定板投射结构光序列。序列包含三部分——Gray-code 图案用于粗定位、线移图案用于亚像素精定位、以及用于编码投影仪 ID 的二进制黑白时间序列。图案总数由传统方法的 $M \times (\lceil \log_2 W \rceil + \lceil \log_2 H \rceil + L)$ 降至 $\lceil \log_2 M \rceil + \lceil \log_2 W \rceil + \lceil \log_2 H \rceil + L$，其中 $W \times H$ 为投影仪分辨率，$L$ 为线移图案数。

2. **嵌入式相机方向捕获**：标定板表面嵌入的 $N$ 台相机以高时间分辨率同步采集入射光序列。由于相机光学中心与标定板平面共面，来自不同空间位置的投影仪光线会按入射角度投射到相机像面的不同像素上，实现**空间-方向解复用**——这一机制类似于光场相机的方向编码原理（Section 3.1）。

3. **逐像素解码**：对每台嵌入式相机的每个像素，先通过亮度阈值判断是否接收到投影光；若接收到，则解码二进制时间序列获取投影仪 ID $m$，再结合 Gray-code 和线移图案解码出该投影仪中对应的像素坐标 $\mathbf{p}_m(n)$。由此建立“相机光学中心 $\mathbf{x}_n$ ↔ 投影仪像素 $\mathbf{p}_m(n)$”的对应关系。

4. **光学中心偏移补偿**：由于嵌入式相机的光学中心实际上并不严格位于标定板平面，光线与板平面的交点 $\mathbf{x}_n(m)$ 会随投影仪位置变化。本方法通过离线阶段预标定的单应矩阵 $\mathcal{M}_n$ 对每个像素进行映射：
   $$\mathbf{x}_n(m) = \mathcal{M}_n(\mathbf{c}_n(m))$$
   其中 $\mathbf{c}_n(m)$ 是相机 $n$ 中接收到投影仪 $m$ 光线的像素坐标。该映射将原始像素坐标校正为板平面上的真实交点坐标。

5. **Zhang 方法联合标定**：在不同标定板姿态下重复上述采集，获得多组 $(\mathbf{x}_n(m), \mathbf{p}_m(n))$ 对应关系，输入 Zhang 的相机标定框架（Zhang, IEEE TPAMI 2000），同时估计所有投影仪的内参和外参。

**离线准备阶段**负责标定补偿所需的基础设施：

- 使用外部相机和印刷棋盘格，通过投影已知点 $\mathbf{X}_k$ 并观测其在嵌入式相机像面上的位置，估计每个嵌入式相机像素到标定板平面交点的单应矩阵 $\mathcal{M}_n$（Figure 4）。该过程采用 RANSAC 结合最小二乘拟合，且由于相机全像面被映射到标定板上约 $25\text{ mm}^2$ 的小区域内，镜头畸变在该局部范围内可忽略。

### 输入输出与模块关系

| 阶段 | 输入 | 处理 | 输出 |
|------|------|------|------|
| 离线 | 外部相机 + 棋盘格 + 已知投影点 | 单应矩阵估计（RANSAC + 最小二乘） | 每台嵌入式相机的 $\mathcal{M}_n$ |
| 在线 | 所有投影仪同时投射编码图案 | 方向捕获 → 逐像素解码 → 偏移补偿 | $(\mathbf{x}_n(m), \mathbf{p}_m(n))$ 对应 |
| 在线 | 多姿态下的 $(\mathbf{x}_n(m), \mathbf{p}_m(n))$ | Zhang 方法联合优化 | 所有投影仪的内参 $\mathbf{K}_m$ 和外参 $[\mathbf{R}_m \mid \mathbf{t}_m]$ |

### 与传统方法的根本差异

传统方法（Zhang 式串行标定）的瓶颈在于：外部相机通过漫反射捕获图案时，所有投影仪的光线在像面上**不可区分地叠加**，必须依赖时间分离（串行投影）。本方法通过将相机嵌入标定板表面，使光学中心与标定平面共面，相机直接按入射方向捕获投影光，从而在**单次采集中实现多投影仪图案的方向性分离**。这一“反向配置”是打破可扩展性瓶颈的因果开关——标定时间不再随投影仪数量线性增长，而是仅增加一个 $\lceil \log_2 M \rceil$ 的微小常数项。

### 补充图表

![[assets/figures/papers/paper_list_l2114_https_arxiv_org_abs_2604_24024/figures/001_Figure_1.jpg]]
*Figure 1: Imaging principle of simultaneously projected structured light patterns from multiple projectors: (a) Overlapping patterns captured by an external camera are difficult to separate, whereas (b) the embedded cameras directly receive the projection light, enabling separation of individual patterns*



### 方向性编码与图案分离

本文方法的核心机制在于将相机嵌入标定板表面，使光学中心与标定平面共面，从而直接按入射方向捕获投影光。这一反向配置（相机朝向投影仪并作为标定目标）使得来自不同位置的投影仪光线落在相机像面的不同像素上，实现了多投影仪图案的方向性分离。如 **Figure 1** 所示，外部相机通过漫反射捕获重叠图案时丧失入射方向信息，无法区分不同投影仪的图案；而嵌入式相机直接接收投影光，可按入射方向分离各投影仪的图案。

方向性编码的原理类似于光场相机：嵌入式相机不仅记录光强，还保留了光线的入射方向信息。通过在每个相机像素上检测是否接收到投影光，并解码投影仪ID，即可建立相机光学中心坐标与投影仪像素坐标之间的对应关系。这一机制使得所有投影仪可**同时投影**结构光图案，从根本上打破了传统方法必须串行投影的可扩展性限制。

### 光学中心偏移补偿

当嵌入式相机的光学中心未精确位于标定板表面时，投影仪 $m$ 到相机 $n$ 的光线与标定板平面的交点 $\pmb{x}_n(m)$ 会因投影仪位置不同而偏移（**Figure 3**）。若直接使用相机光学中心的板坐标 $\pmb{x}_n$ 作为标定输入，将引入系统误差。

![[assets/figures/papers/paper_list_l2114_https_arxiv_org_abs_2604_24024/figures/003_Figure_3.jpg]]
*Figure 3: The light ray from projector m observed by camera n intersects the plane of the calibration board at xn(m) and the camera image plane at pixel*

为此，本文通过离线过程估计每个相机像素到标定板平面交点的单应变换 $\mathcal{M}_n$：

$$\pmb{x}_n(m) = \mathcal{M}_n(\pmb{c}_n(m))$$

其中 $\pmb{c}_n(m)$ 为相机 $n$ 中接收到投影仪 $m$ 光线的像素坐标。该单应矩阵通过最小二乘法结合 RANSAC 进行估计，并在在线标定中将映射后的交点坐标 $\pmb{x}_n(m)$ 替代 $\pmb{x}_n$ 作为 Zhang 标定方法的输入。消融实验表明，移除该补偿后重投影误差从约0.9像素显著升高至2.2–2.5像素，验证了补偿步骤对高精度标定的必要性。

### 投影图案数量的可扩展性分析

传统串行标定方法中，对于 $M$ 台分辨率为 $W \times H$ 的投影仪，采用 $L$ 幅线移图案时所需的投影图案总数为：

$$M \times \left( \lceil \log_2 W \rceil + \lceil \log_2 H \rceil + L \right)$$

该数量随投影仪数量 $M$ 线性增长，成为大规模系统的可扩展性瓶颈。

本文方法通过同时投影和方向性分离，将所需图案数降低为：

$$\lceil \log_2 M \rceil + \lceil \log_2 W \rceil + \lceil \log_2 H \rceil + L$$

其中新增项 $\lceil \log_2 M \rceil$ 用于编码投影仪ID（通过投影均匀白/黑图像的二进制时间序列），其值远小于与分辨率相关的项。例如在25台投影仪实验中，传统方法需1,100幅图案，而本文方法仅需54幅，减少95%。该公式揭示了方法的核心优势：**标定时间几乎与投影仪数量无关**，仅随投影仪数量的对数增长。

### 补充图表

![[assets/figures/papers/paper_list_l2114_https_arxiv_org_abs_2604_24024/figures/002_Figure_2.jpg]]
*Figure 2: Geometric relationship of light rays in the proposed method for the case of two projectors*

![[assets/figures/papers/paper_list_l2114_https_arxiv_org_abs_2604_24024/figures/004_Figure_4.jpg]]
*Figure 4: Measurement method of the intersection point*



## 实验与关键发现

### 核心实验结果

本文方法在3台真实投影仪（Optoma ML1050ST+、BenQ TK685、BenQ TK850）上进行了定量评估，以RMS重投影误差作为精度指标。在启用光学中心偏移补偿后，三台投影仪的重投影误差分别为0.91、0.91和0.89像素（Table 1），均低于1像素的实用阈值。作为对照，使用4个棋盘角点的传统串行标定方法（Zhang, IEEE TPAMI 2000）的误差范围为0.65–0.76像素。本文方法的重投影误差比传统方法高出约0.2像素，这一差距主要源于参考点数量的限制——4台嵌入式相机提供的约束数量与4个棋盘角点相当，但远少于传统方法可利用的108个角点。在参考点数量可比的前提下，本文方法以微小的精度损失换取了标定效率的指数级提升。

![[assets/figures/papers/paper_list_l2114_https_arxiv_org_abs_2604_24024/figures/012_Table_1.jpg]]
*Table 1: RMS reprojection errors (pixels) for each projector*

在25台投影仪的模拟实验中（通过5×5位置偏移模拟大规模阵列），本文方法展示了其核心优势：同时投影所有投影仪的结构光图案仅需54幅图案即可完成标定，而传统串行方法需要1,100幅，图案数量减少了95%。这一结果直接验证了方法的核心主张——标定时间从随投影仪数量线性增长转变为近乎常数。

### 消融实验

**光学中心偏移补偿的必要性**是最关键的消融发现。移除补偿步骤后，3台投影仪的重投影误差骤升至2.18、2.47和2.44像素（Table 1, Proposed w/o compensation列），约为启用补偿时的2.5倍。在25台投影仪实验中，无补偿条件下的对齐结果出现明显模糊（Figure 10），表明光学中心与标定板平面的微小偏移在大规模系统中会产生累积性几何误差。该消融实验确认：尽管嵌入式相机的光学中心偏移量很小，但通过离线单应变换$\mathcal{M}_n$进行逐像素补偿是高精度标定的必要条件。

### 环境光鲁棒性验证

在约70 klux的户外直射阳光下，本文方法对两台投影仪成功完成了结构光图案的分离与解码，并实现了准确的棋盘格几何对齐（Figure 12）。同等条件下，传统外部相机方法完全失效——环境光淹没了投影图案，无法进行任何有意义的解码。这一鲁棒性来源于嵌入式相机的方向性捕获机制：相机像面上每个像素仅接收来自特定入射方向的光线，自然滤除了大部分漫反射环境光。需要指出的是，该实验仅在2台投影仪配置下进行，更大规模户外配置下的鲁棒性尚待验证。

![[assets/figures/papers/paper_list_l2114_https_arxiv_org_abs_2604_24024/figures/011_Figure_12.jpg]]
*Figure 12: Experiment evaluating robustness to ambient light with two projectors outdoors. (Left) Experimental setup placed outdoors under direct sunlight (≈70 klux). (Right) Alignment result of a half-scale checkerboard pattern using the homography transformation estimated with the proposed method*

### 角度分离能力

嵌入式相机的可观测入射角范围约为x轴方向±32°、y轴方向±40°（Figure 6，亮度半角）。两台投影仪的最小可区分角度间隔为0.88°（Figure 7），这一数值决定了系统可支持的最大投影仪密度。在实际部署中，只要任意两台投影仪相对于标定板的张角大于该阈值，即可实现可靠的图案分离。

![[assets/figures/papers/paper_list_l2114_https_arxiv_org_abs_2604_24024/figures/005_Figure_6.jpg]]
*Figure 6: Relationship between incident angle and observed brightness by the embedded camera*

![[assets/figures/papers/paper_list_l2114_https_arxiv_org_abs_2604_24024/figures/008_Figure_7.jpg]]
*Figure 7: Experiment to determine the minimum separation distance between two projectors*

### 公平性讨论

本文与传统方法的比较在参考点数量可比（4点vs 4点）的条件下进行，具有合理的公平性。传统方法在使用108个棋盘角点时能获得0.34–0.39像素的更优精度，但本文方法同样可以通过增加嵌入式相机数量来缩小这一差距。此外，本文方法的精度损失（约+0.2像素）在实际投影应用中通常不可感知，而95%的图案数量减少和户外环境光鲁棒性带来的实际收益远超这一微小代价。

### 补充图表

![[assets/figures/papers/paper_list_l2114_https_arxiv_org_abs_2604_24024/figures/006_Figure_5.jpg]]
*Figure 5: Prototype calibration board*

![[assets/figures/papers/paper_list_l2114_https_arxiv_org_abs_2604_24024/figures/007_Figure_8.jpg]]
*Figure 8: Alignment results of red and green checkerboard patterns projected from two projectors. (Top) Overall view; (Bottom) Magnified view*

![[assets/figures/papers/paper_list_l2114_https_arxiv_org_abs_2604_24024/figures/009_Figure_9.jpg]]
*Figure 9: MTF comparison for the two-projector alignment*

![[assets/figures/papers/paper_list_l2114_https_arxiv_org_abs_2604_24024/figures/010_Figure_10.jpg]]
*Figure 10: Experiment with 25 projectors. (a) The calibration board under simultaneous Gray-code projection. (b) Corresponding image captured by one of the embedded cameras with decoded coordinates overlaid. (c) Result of the alignment projection*



## 定位与知识库关联

### 1. 方法谱系：从串行标定到并行方向分离

本文方法的核心贡献在于将多投影仪标定从**时间域串行分离**范式迁移至**空间域方向分离**范式，其技术谱系可追溯至以下关键节点：

- **传统串行标定基线**：基于平面靶标的投影仪标定方法以 **Zhang** (IEEE TPAMI 2000) 为基石，通过外部相机依次采集各投影仪投射的结构光图案，利用时间分离避免图案重叠。该方法将投影仪建模为逆向相机，通过棋盘角点建立 2D–3D 对应关系。其根本局限在于：外部相机通过漫反射捕获图案时丧失了入射方向信息，因此无法区分同时投影的多投影仪图案，必须串行操作，导致标定时间随投影仪数量线性增长。

- **光场相机原理的逆向应用**：本文方法的核心洞察——利用嵌入式相机按入射方向分离投影图案——与光场相机通过微透镜阵列记录光线方向信息的原理同源（文中明确类比了光场相机 ）。不同的是，本文并非记录场景光场，而是利用方向编码**主动分离已知编码的结构光**，实现了从“捕获场景光场”到“解码投影方向”的范式反转。

- **与并行标定方法的差异**：现有并行标定方法多依赖颜色编码、频率复用或几何约束来分离重叠图案，但这些方法在投影仪数量增加时面临编码容量不足或串扰加剧的问题。本文通过**物理层面的方向分离**（嵌入式相机直接接收入射光），从根本上规避了编码层面的串扰，使分离能力仅受限于相机的角度分辨率和投影仪的空间分布。

### 2. 核心机制对比：从时间分离到方向分离

| 维度 | 传统串行方法 (Zhang) | 本文方法 (Proposed) |
|------|---------------------|-------------------|
| **分离机制** | 时间分离（串行投影） | 空间方向分离（同时投影） |
| **信息载体** | 漫反射光（丧失方向信息） | 直接入射光（保留方向信息） |
| **标定参考点** | 印刷棋盘角点 | 嵌入式相机光学中心 |
| **图案数量** | $M \times (\lceil \log_2 W \rceil + \lceil \log_2 H \rceil + L)$ | $\lceil \log_2 M \rceil + \lceil \log_2 W \rceil + \lceil \log_2 H \rceil + L$ |
| **可扩展性** | 线性增长 | 近乎常数 |
| **环境光鲁棒性** | 弱（漫反射易被环境光淹没） | 强（直接接收投影光） |

### 3. 适用边界与局限

#### 3.1 必要条件

- **投影区域共享**：所有投影仪必须存在公共投影区域，标定板需放置于该区域内。对于无重叠的大范围多投影系统（如建筑投影），需分组放置标定板，此时标定时间恢复为线性增长。
- **角度分离约束**：投影仪之间的角间距必须大于嵌入式相机的最小可区分角度（实测约 $0.88^\circ$），否则方向分离会失效。
- **平面靶标限制**：目前仅支持平面或多平面组合的标定靶，无法直接处理曲面靶标。

#### 3.2 精度–效率权衡

- 在参考点数量可比（4 台嵌入式相机 vs 4 个棋盘角点）的条件下，本文方法的重投影误差约为 0.89–0.91 像素，略高于传统方法的 0.65–0.76 像素（约 +0.2 px），但仍在 1 像素以内，满足实用精度要求。
- 传统方法使用 108 个棋盘角点时可达 0.34–0.39 像素的重投影误差，本文方法可通过增加嵌入式相机数量来逼近该精度，但需额外硬件成本。

#### 3.3 环境光鲁棒性的验证边界

- 在约 70 klux 的户外阳光下，本文方法在 2 台投影仪配置下成功完成标定，传统方法完全失效。
- **尚未验证**：更大规模配置（如 25 台）在强环境光下的表现，以及极端光照条件（如 >100 klux）下的鲁棒性。

### 4. 开放问题与未来方向

1. **方向信息作为额外约束**：嵌入式相机捕获的方向信息目前仅用于图案分离，能否将其作为几何约束融入标定优化，以减少所需的标定板姿态数量？

2. **单次拍摄结构光结合**：当前每台投影仪仍需投射 Gray-code 序列，若能结合 De Bruijn 序列等单次拍摄方法，可进一步将图案数量降至接近常数，实现真正意义上的“单帧标定”。

3. **精度提升的定量规律**：增加嵌入式相机数量对标定精度的提升遵循何种规律？需要多少台相机才能达到 108 角点的传统方法精度？这一规律对硬件设计具有指导意义。

4. **大规模真实系统验证**：在超过 25 台真实投影仪的系统中，方向分离能力是否会出现退化？环境光鲁棒性在大规模配置下是否仍然保持？

5. **投影仪物理属性提取**：嵌入式相机捕获的方向编码光中是否蕴含投影仪的镜头像差、光圈形状、对焦距离等物理属性信息？这些信息能否用于投影仪的自诊断或自适应校正？

6. **镜头畸变校正的必要性**：文中认为相机镜头畸变在标定板小区域内可忽略，但作为预处理步骤加入无畸变校正是否会进一步降低重投影误差？其定量效果尚待验证。

7. **离线标定的简化**：当前离线单应标定需要外部相机和印刷棋盘格，增加了系统搭建复杂度。能否利用投影仪自身投射已知图案，结合嵌入式相机实现自标定，从而消除对外部设备的依赖？

### 5. 知识库定位

本文属于**多投影仪几何标定**领域，位于以下研究方向的交叉点：

- **投影仪–相机系统标定**：继承 Zhang (2000) 的平面靶标标定框架，但将参考点从被动棋盘角点替换为主动嵌入式相机。
- **结构光编码与解码**：使用 Gray-code 和线移图案进行投影仪像素坐标编码，同时创新性地引入投影仪 ID 的二进制时间序列编码。
- **光场成像**：借鉴光场相机的方向编码原理，但将其逆向用于主动投影的方向分离。
- **多设备协同标定**：将标定从单投影仪串行扩展至多投影仪并行，解决了大规模投影系统的可扩展性瓶颈。

该方法在概念上与**分布式孔径成像**和**多视角几何标定**存在潜在关联，但其核心创新——通过嵌入式相机实现方向性图案分离——在当前文献中尚无直接对应工作，属于原创性贡献。



## 原文 PDF

![[paperPDFs/CVPR_2026/Breaking_the_Scalability_Limit_of_Multi_Projector_Calibration_with_Embedded_Cameras.pdf]]
