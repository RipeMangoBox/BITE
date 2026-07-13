---
title: "From Cluster to Desktop: A Cache-Accelerated INR framework for Interactive Visualization of Tera-Scale Data"
type: paper
paper_level: A
venue: EGPGV
year: 2025
pdf_ref: paperPDFs/EGPGV_2025/From_Cluster_to_Desktop_A_Cache_Accelerated_INR_framework_for_Interactive_Visualization_of_Tera_Scale_Data.pdf
code_link: null
project_link: https://wilsoncernwq.github.io/publications/egpgv2025-cinr
aliases:
- CAIRF
- FCDCAIFIVTSD
tags:
- EGPGV_2025
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "为INR渲染引入多分辨率GPU缓存，存储先前生成的体素砖块并复用，从而大幅减少每帧需要进行的网络推理次数。"
primary_logic: "将多层级多分辨率页面表（MRPD）缓存与先进先出优先级调度相结合，并利用LoD预加载与随机过渡，可在不显著损失重构质量的前提下将INR渲染性能平均提升5倍，使太字节数据在桌面端可实现交互可视化。"
claims:
- "提出的缓存管线在光线行进模式下平均获得约5倍加速，路径追踪约2倍加速。"
- "优先级排序使缓存更早覆盖高重要性区域，降低缓存未命中率并减少帧率波动。"
- "预加载高LOD砖块显著提升初始帧率并加速FPS稳定。"
- "在DNS数据集（0.96TB）上实现6444:1压缩比并达到近6.5倍光线行进加速与2倍路径追踪加速。"
---

# From Cluster to Desktop: A Cache-Accelerated INR framework for Interactive Visualization of Tera-Scale Data

> [!tip] 核心洞察
> 将多层级多分辨率页面表（MRPD）缓存与先进先出优先级调度相结合，并利用LoD预加载与随机过渡，可在不显著损失重构质量的前提下将INR渲染性能平均提升5倍，使太字节数据在桌面端可实现交互可视化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 从集群到桌面：一种面向太尺度数据交互可视化的缓存加速隐式神经表示框架 |
| 英文题名 | From Cluster to Desktop: A Cache-Accelerated INR framework for Interactive Visualization of Tera-Scale Data |
| 会议/期刊 | EGPGV 2025 |
| Links | [paper](https://arxiv.org/abs/2504.18001) · [Project](https://wilsoncernwq.github.io/publications/egpgv2025-cinr) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | Cache-Accelerated INR Rendering Framework |
| Dataset | Magnetic (recentered 2560×1280×1280), DNS (5120×3072×15360, 0.96TB), DNS (5120×3072×15360) |

> [!tip] 效果简介
> - Magnetic (recentered 2560×1280×1280) 上，Ray Marching FPS 为 174.8，对比 36.3，变化 4.8×。
> - Magnetic (recentered 2560×1280×1280) 上，Path Tracing FPS 为 9.4，对比 5.5，变化 1.7×。
> - DNS (5120×3072×15360, 0.96TB) 上，Ray Marching FPS 为 ~11 (from Figure 8 top, approximate)，对比 ~1.7，变化 ~6.5×。

## 概要

**核心问题**：隐式神经表示（INR）虽然能将太字节（TB）级科学数据压缩数千倍，但在消费级GPU上进行交互式体渲染时，每帧需对数十万条光线追踪样本逐一调用网络推理，导致帧率远低于直接内存读取，难以实现流畅交互。这一瓶颈源于INR解码器的计算开销远大于缓存命中时的内存访问成本。

**核心思路**：将大规模科学可视化中成熟的多分辨率GPU缓存策略引入INR渲染管线。具体而言，在Wavefront光线行进/路径追踪框架的采样器与INR之间插入一个**多级多分辨率页表（MRPD）缓存层**，并辅以**显著性优先级调度**与**细节层次（LoD）预加载**机制。光线采样时优先查询缓存中的体素砖块；未命中时依次回退到更高LoD砖块，最终才触发INR推理。这使得绝大多数采样点绕过了昂贵的网络前向计算。

**方法定位**：该方法处于**INR压缩表示**与**体渲染缓存管理**的交叉点。其INR骨干沿用Instant NGP风格的多分辨率哈希网格编码器加小型MLP（**Wu et al., IEEE TVCG 2024**），渲染器采用Wavefront架构以提升GPU占用率。创新集中于**缓存架构与调度策略**：将Hadwiger et al. (2012) 提出、Sarton et al. (2020) 优化的MRPD缓存适配到INR渲染上下文，并加入优先级排序与随机LoD过渡。

**关键结果**：
- 在多个数据集上，缓存管线在光线行进模式下平均获得**约5倍加速**，路径追踪约**2倍加速**。
- 在0.96 TB的DNS湍流数据集上，INR模型实现**6444:1压缩比**，光线行进加速近**6.5倍**，路径追踪加速**2倍**，峰值显存占用仅11.3 GB。
- 优先级排序使缓存更早覆盖视觉显著性区域，降低未命中率并减少帧率抖动；LoD预加载显著提升初始帧率并加速FPS稳定。
- 即使采用激进的LoD缩放，重构质量仍可保持PSNR约41 dB、MSSIM 0.996，提供了性能与质量之间的弹性权衡空间。

**局限与开放问题**：当前缓存以全精度浮点存储，未探索半精度/混合精度；LoD选择仅依赖相机距离，对细小结构或平坦表面可能产生质量退化；尚未验证时变数据的时间缓存一致性；在集成GPU或移动设备上的效能有待评估。



### 体积数据可视化的规模瓶颈

科学计算与工程仿真产生的体积数据正以前所未有的速度增长，单数据集规模已突破太字节（TB）量级。传统直接体渲染方法需要将完整数据加载至GPU显存，而消费级硬件的显存容量（通常为8–24 GB）远不足以容纳此类数据。即使采用带外核（out-of-core）策略按需加载数据块，存储I/O带宽与渲染计算之间的鸿沟依然使得交互式可视化难以实现。

### 隐式神经表示（INR）带来的机遇与挑战

近年来，隐式神经表示（Implicit Neural Representation, INR）为体积数据压缩提供了一条极具吸引力的路径。其核心思想是将体积标量场建模为一个连续函数 $\Phi: \mathbb{R}^3 \to \mathbb{R}$，对于任意空间坐标 $(x,y,z)$ 返回离散标量值 $\mathbf{v}$。该方法通过小型神经网络（通常结合多分辨率哈希网格编码器）将原始体积数据压缩数个数量级，使TB级数据可在显存中以数十至数百兆字节的模型形式驻留。例如，**Instant NGP** 风格的哈希网格编码器（Müller et al., SIGGRAPH 2022）已被 Wu et al.（IEEE TVCG 2024）适配至科学可视化领域，展示了极高的压缩潜力。

然而，这一压缩能力是以运行时计算为代价的：**每帧渲染期间，数十万条光线追踪样本中的每个采样点都需要调用INR进行前向推理**，以重建该位置的标量值。在光线行进（ray marching）和路径追踪（path tracing）等渲染模式下，这意味着每帧需要执行数十万乃至数百万次神经网络推理。这一计算开销远超直接从GPU内存读取预存体素值的开销，成为限制消费级硬件上交互帧率的核心瓶颈。本文识别出的根本矛盾在于：**INR将存储压力转化为计算压力，而后者在渲染管线的逐帧推理循环中被急剧放大**。

### 现有方法的缺口

Wu et al.（IEEE TVCG 2024）的管线虽然通过宏单元（macro-cell）加速结构跳过了透明区域，减少了不必要的采样，但其采样器在每次需要体素值时仍直接调用INR进行推理。这种“无缓存”策略意味着：

1. **重复计算浪费**：相邻帧之间、同一帧内相邻像素之间，大量采样点落在相同或邻近的空间区域，其INR推理结果完全可复用，但现有方法每次均从头计算。
2. **帧率受限于推理速度**：即使MLP规模较小（如40.6 MB模型），在消费级GPU上每秒可执行的推理次数仍远低于交互式渲染所需的吞吐量，导致帧率长期处于不可交互的低水平（例如，光线行进模式下仅约36 FPS，路径追踪下约5.5 FPS，见Table 1的Magnetic数据集基线）。
3. **缺乏多分辨率感知**：单分辨率采样策略无法根据相机距离或视觉显著性动态调整细节层次（Level-of-Detail, LoD），导致远端区域的计算开销与近端区域无异，进一步浪费了有限的推理预算。

### 本文动机与核心思路

上述分析揭示了关键的可控因果旋钮：**若能在INR渲染管线中引入一个GPU缓存层，存储先前推理生成的体素砖块（voxel bricks）并加以复用，则可大幅削减每帧所需的网络推理次数**，从而将渲染性能从推理速度的束缚中解放出来。

本文的核心洞察在于：将**多层级多分辨率页面表（Multi-Level Multi-Resolution Page Table, MRPD）缓存**（Hadwiger et al., 2012; Sarton et al., 2020）与**显著性优先级调度**相结合，并辅以**LoD预加载**与**随机过渡**机制，可在不显著损失重构质量的前提下，将INR渲染性能平均提升约5倍（光线行进）和约2倍（路径追踪），使太字节数据在桌面级GPU上实现交互可视化成为可能。



## 核心方法与创新机理

本工作针对隐式神经表示（INR）在体渲染中每帧需为数十万光线追踪样本重复推理全部数据值、导致消费级GPU上交互帧率严重受限的瓶颈，提出了**缓存加速的INR渲染框架**。其核心创新可归结为三个相互协同的**changed slots**，它们共同将渲染性能平均提升约5倍，同时保持与无缓存基线可比的重构质量。

### 1. 多分辨率GPU缓存优先采样（Voxel Sampling Strategy）

基线方法（**Instant NGP / Direct INR rendering**, Wu et al., IEEE TVCG 2024）在每次体素采样时直接调用INR网络进行推理。本工作将这一采样策略替换为**多分辨率GPU缓存优先查询**：渲染器首先向缓存请求体素值；若缓存命中则直接返回，若未命中则回退到更高LOD级别的已缓存砖块，仅在所有缓存层级均缺失时才执行INR推理。这一机制将昂贵的网络推理次数从“每采样一次”压缩为“每缺失砖块一次”，是性能提升的根本来源。

### 2. 基于显著性的优先级缓存调度（Cache Management）

缓存管理层面，本工作在**多级多分辨率页表（MRPD）** 缓存架构（Hadwiger et al., 2012; Sarton et al., 2020）之上引入了**显著性优先级排序**。具体而言，每个待加载砖块维护一个基于首次请求时间戳的初始值，并在每次被后续采样步再次请求时递增计数；请求处理器按此计数值降序调度砖块加载，使视觉显著性高、被反复访问的区域优先驻留缓存。消融实验表明（Figure 3），相比简单的时间戳排序，优先级排序使缓存未命中率下降更快，缓存内容更贴合数据中视觉重要的区域，并显著降低了帧率抖动。

### 3. 细节层次预加载与随机过渡（Level-of-Detail Handling）

为缓解缓存冷启动和视点突变导致的性能骤降，本工作设计了**基于相机距离的LoD选择**，并辅以两项关键策略：
- **随机LoD过渡**：在相邻LoD级别之间引入概率性切换，消除因离散级别切换产生的可见边界伪影；
- **高LoD砖块预加载**：利用缓存自身的回退机制，在空闲时主动预加载高LoD砖块，使初始帧率和交互稳定性大幅提升（Figure 5，预加载启用后初始FPS显著高于无预加载配置，且更快达到稳态）。

这三项创新构成了一条完整的因果链：**多分辨率缓存查询**减少了对INR推理的依赖，**优先级调度**确保有限缓存容量被高效利用于视觉关键区域，而**LoD预加载与随机过渡**则平滑了性能的时间波动并提升了交互响应质量。在0.96TB的DNS数据集上，该框架实现了6444:1的压缩比，光线行进模式加速近6.5倍，路径追踪模式加速约2倍，验证了从集群端压缩到桌面端交互可视化的可行性。



![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2504_18001/figures/002_Figure_2.jpg]]
*Figure 2: An overview of the model architecture and hash-grid encoder. A vector of size n is constructed from each resolution grid via interpolation of nearby grid points. The resulting feature vector thus encodes a multi-resolution representation of the input, allowing for a smaller MLP*

本文提出一套面向太字节（TB）级科学数据的**缓存加速隐式神经表示（INR）渲染框架**，其核心目标是在消费级桌面GPU上实现交互式体绘制。框架将INR的极致压缩能力与基于GPU的多分辨率体素缓存相结合，通过复用先前推理出的砖块（brick）数据，大幅减少每帧渲染所需的神经网络前向推理次数。

### 系统流水线概览

整个流水线（见 Figure 1）包含两条主线：**离线预处理**与**在线渲染**。

**离线阶段**首先对原始体积数据进行两项预处理：
1. **宏单元加速结构生成**：构建轻量级的宏单元网格（macro-cell grid），用于在光线行进过程中快速跳过透明或空区域，减少无效采样。宏单元网格尺寸为 $\lceil \frac{V_x}{N} \rceil \times \lceil \frac{V_y}{N} \rceil \times \lceil \frac{V_z}{N} \rceil$，其中 $V$ 为体积各维度尺寸，$N$ 为宏单元边长。
2. **INR模型压缩**：将体积数据压缩为小型神经网络模型。模型主体采用**哈希网格编码器**（hash-grid encoder），通过 $m$ 个不同分辨率的三维网格对输入坐标 $(x,y,z)$ 进行多分辨率特征编码，每个网格点通过固定大小的哈希表存储 $n$ 个可训练参数。各分辨率网格经插值后拼接为多分辨率特征向量，馈入一个小型MLP，最终输出标量值 $\Phi: \mathbb{R}^3 \to \mathbb{R}$。模型大小固定为40.6MB（DNS数据集因复杂度更高采用150MB的更大网络）。

**在线渲染阶段**，光线行进与路径追踪均采用**Wavefront架构**，将渲染器分解为三个独立GPU内核：射线生成、坐标计算与着色，以提升GPU利用率。渲染的核心交互发生在**采样器接口**与**MRPD缓存系统**之间：

1. **采样器接口**：渲染器通过采样器请求体素值。采样器优先查询GPU缓存，若命中则直接返回；若未命中，则回退到更高LOD（Level-of-Detail）的砖块，或最终标记为“真实缺失”（true miss）。
2. **MRPD缓存管理器**：管理多层级多分辨率页表层次结构，维护虚拟地址到物理砖块的映射，处理体素请求并生成砖块加载请求。
3. **请求处理器**：异步运行，接收缺失砖块ID的小批量请求，调度GPU上的砖块生成任务。每个砖块请求包含坐标信息，请求处理器据此生成对应坐标并通过INR推理出完整砖块数据。
4. **缓存更新与回写**：新生成的砖块写入GPU数据缓存，页表层次结构与LRU链表同步更新。每个采样步骤结束时，所有缓存未命中的体素通过单次INR前向推理批量完成。

### 核心设计决策

框架的三个关键设计直接决定了性能与质量的权衡：

- **多分辨率缓存与LoD选择**：砖块尺寸固定为 $40^3$ 个体素，缓存容量为 $30^3$ 个砖块。LoD级别基于相机距离动态选择，步长为 $2^{LoD}$。为实现无缝过渡，采用**随机LoD切换**，避免可见的边界伪影。
- **显著性优先级调度**：在传统时间戳排序基础上，引入基于砖块利用率（utilization）的优先级排序。每次砖块被访问时其优先级递增，使缓存更早覆盖视觉显著性高的区域，降低缓存未命中率并减少帧率抖动（见 Figure 3）。
- **高LoD预加载**：利用缓存自身的回退机制，在加载阶段预先填充高LoD砖块，显著提升初始帧率并加速FPS稳定（见 Figure 5）。

### 输入输出流

| 阶段 | 输入 | 输出 |
|------|------|------|
| 离线预处理 | 原始体积数据（最高0.96TB） | 宏单元加速结构 + INR模型文件（40.6–150MB） |
| 在线渲染 | 相机参数、传输函数 | 渲染图像帧 |
| 缓存查询 | 体素坐标 | 缓存命中：体素值；未命中：缺失砖块请求 |
| INR推理 | 砖块坐标（含LoD信息） | $40^3$ 体素砖块数据 |

该框架将INR的压缩优势（DNS数据集上达到6444:1压缩比）与缓存复用机制有机结合，在光线行进模式下平均获得约5倍加速，路径追踪约2倍加速，使太字节级数据在桌面端实现交互可视化成为可能。



### 标量场映射与体素采样

本框架的操作对象是由离散体素构成的标量体积场。其数学基础为从三维空间坐标到标量值的映射：

$$\Phi: \mathbb{R}^3 \to \mathbb{R}$$

对于体积场中的任意体素，采样过程可表达为：

$$(x,y,z) \mapsto \Phi(x,y,z) = \mathbf{v}$$

其中 $\mathbf{v}$ 为离散标量值。该映射通过哈希网格编码器与小型MLP构成的隐式神经表示（INR）来近似，训练域为归一化空间 $[0,1)^3$，真值数据范围为 $[0,1]$。

### 哈希网格编码器

INR模型的核心是哈希网格编码器（Figure 2），其设计思想是将绝大部分模型参数分配给 $m$ 个不同分辨率的三维网格。每个分辨率级别的网格点存储于固定大小的哈希表中，每个表项关联 $n$ 个可训练参数。对于给定输入坐标，通过对邻近网格点进行插值，从各分辨率网格中分别提取长度为 $n$ 的特征向量，拼接后形成多分辨率特征表示。这种多分辨率编码使得后续的MLP可以保持较小的规模，从而在压缩率与推理速度之间取得平衡。

### 多分辨率缓存架构

缓存系统的核心是**多级多分辨率页表（MRPD）**层次结构。系统包含两个关键组件：

- **缓存管理器（Cache Manager, CM）**：管理MRPD层次结构与体素请求，维护虚拟地址到物理缓存砖块的映射关系。
- **请求处理器（Request Handler, RH）**：异步运行，接收缺失砖块ID，根据请求中的坐标信息生成对应砖块并调用INR进行推理，将结果写入GPU缓存后更新页表和LRU状态。

### 细节层次（LoD）与砖块采样

砖块内采样点的步长由LoD级别决定：

$$\text{步长} = 2^{LoD}$$

即LoD每增加一级，采样密度减半，砖块覆盖的空间范围加倍。砖块请求在空间上的偏移量设计考虑了相邻砖块间的单个体素重叠，以保证边界处的连续性。沿y轴的偏移量为：

$$40 \times 2^{LoD} - 1$$

沿z轴的偏移量为：

$$40 \times 2^{LoD} \times 2 - 1$$

其中40为立方体砖块的边长（体素数），$-1$用于在相邻砖块间保留单个体素的重叠区域，乘2对应第三坐标轴的索引计算。

### 宏单元加速结构

为跳过体积中的透明区域，系统生成轻量级的宏单元加速结构。对于体积尺寸为 $V_x \times V_y \times V_z$ 的数据，以 $N$ 为宏单元边长时，各维度上的宏单元数量为：

$$\lceil \frac{V_x}{N} \rceil \times \lceil \frac{V_y}{N} \rceil \times \lceil \frac{V_z}{N} \rceil$$

例如，将Miranda数据集向上缩放至 $4096^3$ 并以 $N=16$ 为宏单元边长时，宏单元总数可达1680万个。

### GPU缓存容量与缓冲区

GPU缓存的理论最大容量由砖块尺寸和缓存网格维度共同决定。以立方体砖块边长40体素、缓存网格尺寸 $30 \times 30 \times 30$ 砖块计算，缓存可容纳的最大体素数为：

$$30^3 \times 40^3 = 1.728 \times 10^9$$

砖块加载缓冲区所需的GPU显存大小为：

$$40^4 \times 4 = 10.24 \text{ MB}$$

其中 $40^4$ 为单个砖块的总采样点数（含重叠区域），乘4表示每个体素以全精度浮点数存储。

### 优先级排序机制

在请求处理器调度砖块加载时，系统引入基于显著性的优先级排序。初始时记录缺失砖块被首次识别的时间戳，随后每次该砖块被请求时将其优先级值递增1。这一机制使得高频访问的视觉显著性区域能更早被加载到缓存中，从而加速缓存未命中率的下降并减少帧率抖动。

### 缓存未命中处理

当采样器在缓存中未找到所需砖块时，系统采用两级回退策略：首先尝试从更高LoD级别（即更低分辨率）的已缓存砖块中获取近似值；若仍不可得，则将该请求标记为真实未命中。每个采样步骤结束后，系统将所有真实未命中的体素坐标批量送入INR进行一次推理，而非逐体素调用网络，从而摊销推理开销。此外，系统利用缓存的回退机制，在渲染初期预加载高LoD砖块，使得初始帧即可获得可用的近似数据，大幅提升加载阶段的交互体验。



## 实验与关键发现

### 主结果：缓存加速渲染性能

与无缓存的 Instant NGP 基准（Wu et al., IEEE TVCG 2024）相比，本文提出的缓存加速管线在多个科学可视化数据集上均取得显著帧率提升。所有实验使用相同的 INR 模型架构（DNS 数据集除外，其使用 150 MB 的更大网络）和相同的 Wavefront 渲染内核，仅改变是否启用缓存及其策略；渲染分辨率、砖块大小（40³ 体素）和缓存容量（30³ 砖块）在所有对比中保持一致。

**Table 1** 汇总了光线行进（Ray Marching, RM）与路径追踪（Path Tracing, PT）两种模式下的帧率对比。在 Magnetic（2560×1280×1280）数据集上，缓存管线在 RM 模式下达到 174.8 FPS，相比基准的 36.3 FPS 获得 **4.8× 加速**；PT 模式下从 5.5 FPS 提升至 9.4 FPS，获得 **1.7× 加速**。在更大的 DNS 数据集（5120×3072×15360，原始体积 0.96 TB）上，**Figure 8 (Top)** 显示 RM 模式从约 1.7 FPS 提升至约 11 FPS，加速比约 **6.5×**；PT 模式从约 0.6 FPS 提升至约 1.2 FPS，加速比约 **2×**。DNS 数据集的压缩比达到 6444:1，峰值显存占用为 11.3 GB。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2504_18001/figures/009_Figure_8.jpg]]
*Figure 8: Both a performance and quality comparison of the rendered DNS data. (Top) plots the rendering FPS of DNS in both network-only and cache-enabled pipelines using our ray marching algorithm. The bottom half of the figure shows our rendered results and quality metrics for both the ray marching (Left) and path tracing (Right) pipelines. These metrics are calculated identically to our previous results*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2504_18001/figures/006_Table_1.jpg]]
*Table 1: Comparison of our cached pipeline’s rendering performance to an un-cached method utilizing the same ray marching (RM) and path tracing (PT) algorithms. Our INR model architecture is fixed at 40.6MB for all datasets apart from DNS in which we use a larger network to represent the data more accurately at 150MB. For all experiments, we use the same cubic brick size of 40 voxels and a cache size of 30 × 30 × 30 bricks. All experiments result in a similar VRAM utilization with a maximum of 11.3GB for DNS*

总体而言，缓存管线在光线行进模式下平均获得约 **5 倍加速**，路径追踪模式下约 **2 倍加速**，同时保持与无缓存基线可比的重构质量（见下文质量分析）。

### 消融实验

#### 优先级排序的贡献

**Figure 3 (Top)** 对比了启用与禁用显著性优先级排序时的性能差异。启用优先级排序后，缓存未命中率下降更快，帧率波动显著减小。**Figure 3 (Bottom)** 的时间线显示，优先级排序使缓存内容更早覆盖视觉显著性高的区域，从而在相同帧数下呈现更贴合场景上下文的缓存分布。这说明基于利用率的优先级调度是降低缓存冷启动开销和性能抖动的关键设计。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2504_18001/figures/003_Figure_3.jpg]]
*Figure 3: (Top) Performance comparison with our priority ranking enabled/disabled. (Bottom) Shows a timeline of the cache content after rendering without LoD pre-loading and fallback network calls on cache misses at 250, 500, 1000, and 2000 frames respectively. We see that ranking enables a more context aware representation of the data in the cache*

#### LoD 预加载的贡献

**Figure 5** 展示了三种配置下的逐帧 FPS 曲线：缓存禁用（直接 INR 推理）、缓存启用但无预加载、缓存启用且预加载高 LoD 砖块。预加载配置在初始帧阶段 FPS 明显更高，且达到稳定帧率所需时间更短。这一结果验证了利用缓存自身的回退机制预加载高 LoD 砖块，可有效减少真实缓存未命中的发生频率，加速交互响应的收敛。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2504_18001/figures/005_Figure_5.jpg]]
*Figure 5: FPS measured each frame over the course of our testing for section 5.3. (Top) Results with our cache disabled and sampling directly from the INR. (Middle) Results after enabling our cache without pre-loading higher LoDs. (Bottom) Results with pre-loading enabled. We see that pre-loading greatly improves performance during the initial frames and allows the FPS to stabilize quicker on the more challenging datasets*

#### LoD 激进程度对质量的影响

**Figure 6** 给出了 Fialka 和 Miranda 两个数据集在不同 LoD 缩放级别下的性能与质量对比。对于 Miranda 这类以低频成分为主的数据集，即使将 LoD 激进程度加倍（FPS > 100），重构 PSNR 仍可达 41 dB，MSSIM 达 0.996。而 Fialka 等包含更多高频细节的数据集，在同样激进的 LoD 下质量退化更明显。这表明模型可提供质量与性能之间的弹性权衡，但具体收益取决于数据本身的频谱特性。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2504_18001/figures/007_Figure_6.jpg]]
*Figure 6: A performance and quality comparison between a sensitive and resilient dataset to changes in LoD scaling. (Top) A Graph showing the measured FPS for the two datasets at different LoD scales. (Left) Quality measurements of the Fialka dataset at increasingly aggressive LoD scaling. (Right) Similar measurements for the Miranda dataset which is more resilient to LoD scaling. We see that datasets with more low frequency data are more forgiving at increased LoD and offer higher performance gains at increasing scales*

### 质量保持分析

**Figure 4** 以 Wu et al. 的单分辨率 INR 管线渲染图像为真值，对比了缓存管线的输出质量。FLIP 差异图显示像素级误差较小，定量指标（PSNR、MSSIM、LPIPS）均表明缓存管线在实现 5× 加速的同时，重构质量与基线保持可比水平。**Figure 8** 底部进一步给出了 DNS 数据在 RM 和 PT 两种模式下的渲染结果与质量指标，计算方法与前述实验一致。

### 失败模式与局限性

**Figure 7** 揭示了高 LoD 下两类典型伪影：(1) 平坦表面（Scrambler 数据集）在远处视角出现块状不连续性；(2) 精细结构（Flower 数据集）在激进 LoD 下细节丢失严重。这些失败案例表明，仅依赖相机距离的 LoD 选择策略对包含薄平面或细小结构的数据集存在质量退化风险，需要更智能的上下文感知启发式方法。

此外，当前缓存存储全精度浮点数，未探索半精度或混合精度以降低显存压力；方法尚未在动态或时变数据集上验证，缺乏时间维度上的缓存一致性支持。这些构成了当前框架的主要局限。



## 定位与知识库关联

### 与基线方法的关系

本工作的直接基线是 **Wu et al.** 提出的单分辨率哈希网格 INR 渲染框架（IEEE TVCG 2024 [WBDM24]）。该基线将体积数据压缩为小型神经网络模型，在光线行进或路径追踪过程中，每条射线上的每个采样点均需直接调用 INR 进行推理以获取标量值。论文在其基础上进行了三个关键维度的扩展：

1. **采样策略替换**：将基线中“每次采样直接调用 INR”替换为“多分辨率 GPU 缓存优先查询”。当缓存命中时直接返回已存储的体素值；未命中时回退到更高 LoD 级别的砖块，仅在最终仍缺失时才触发 INR 推理。这一改动将渲染过程中每帧数十万次的网络前向传播大幅削减为少量缓存未命中时的按需推理。

2. **缓存管理体系引入**：基线无任何缓存机制。论文引入了基于 **MRPD**（Multi-Level Multi-Resolution Page Table）的多级多分辨率页表缓存架构。MRPD 最初由 Hadwiger et al. 提出（[HBJP12]），后经 Sarton et al. 优化（[SCRL20]），本工作在其基础上进一步加入了基于显著性的优先级排序方案，使缓存内容更贴合视觉关注区域。

3. **细节层次处理增强**：基线仅支持单分辨率采样，本工作实现了基于相机距离的 LoD 选择，并辅以随机过渡和预加载机制，在避免可见边界伪影的同时提升初始帧率。

值得注意的是，论文的渲染管线（Wavefront 架构的光线行进与路径追踪）和 INR 模型架构（哈希网格编码器 + MLP）均直接继承自 Wu et al. 的工作，仅在采样器接口处嵌入缓存层。因此，该方法的性能增益完全归因于缓存机制本身，而非模型或渲染算法的改进。

### 适用边界

**数据规模**：方法在 0.96TB 的 DNS 数据集上验证了可行性，实现了 6444:1 的压缩比和近 6.5 倍的光线行进加速。理论上，只要 INR 模型能够成功压缩目标数据，缓存框架即可适用。但论文未验证超过 1TB 的数据集。

**数据特征**：方法对低频占主导的体积数据（如 Miranda）表现出更好的 LoD 弹性——即使将 LoD 激进程度加倍，PSNR 仍可达 41dB，MSSIM 达 0.996。但对于包含大量平坦表面（如 Scrambler）或精细结构（如 Flower）的数据集，高 LoD 下会出现可见伪影，需要更保守的 LoD 缩放策略。

**硬件约束**：所有实验在消费级 GPU 上进行，峰值 VRAM 占用为 11.3GB（DNS 数据集）。缓存容量固定为 $30^3$ 个砖块（可容纳 $1.728 \times 10^9$ 个体素）。对于显存更受限的集成 GPU 或移动设备，方法的效能尚未验证。

**渲染模式**：方法同时支持光线行进和路径追踪两种模式，但在路径追踪下的加速比（约 2 倍）显著低于光线行进（约 5 倍），这是因为路径追踪的采样点分布更分散，缓存命中率天然较低。

### 局限与开放问题

**当前局限**：

1. **缓存精度未优化**：当前缓存以全精度浮点数存储体素值，未探索半精度或混合精度存储，限制了在同等显存预算下可容纳的砖块数量。
2. **LoD 选择策略粗糙**：LoD 仅依赖相机距离这一单一启发式，对包含细小结构或平坦表面的数据可能在远处产生可见质量退化。
3. **INR 推理瓶颈未根除**：缓存未命中时的回退推理仍依赖 MLP 有限的前向速度，未探索更低开销的表示形式（如 3D 高斯表示）。
4. **时变数据未覆盖**：方法仅在静态数据集上验证，缺乏对时间维度缓存复用与一致性的支持。

**开放问题**：

- 如何自动识别体积中高频、小尺度区域以及薄平面，并自适应调整 LoD 以兼顾质量与性能？
- 能否将管线扩展到太字节级时变数据集，实现时间维度上的缓存复用与一致性？
- 半精度或混合精度编码在缓存中引入后，对重构质量的影响如何定量控制？
- 可否利用宏单元的值域统计信息或表面检测来动态选择更优的 LoD 级别？
- 将 3D 高斯泼溅表示与体缓存结合，是否可在类似内存预算下进一步提升交互帧率？
- 在资源更加受限的集成 GPU 或移动设备上，该缓存框架的效能如何？



## 原文 PDF

![[paperPDFs/EGPGV_2025/From_Cluster_to_Desktop_A_Cache_Accelerated_INR_framework_for_Interactive_Visualization_of_Tera_Scale_Data.pdf]]
