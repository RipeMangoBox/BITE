---
title: Training-free, Perceptually Consistent Low-Resolution Previews with High-Resolution Image for Efficient Workflows of Diffusion Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Training_free_Perceptually_Consistent_Low_Resolution_Previews_with_High_Resolution_Image_for_Efficient_Workflows_of_Diffusion_Models.pdf
project_link: null
code_link: "https://huggingface.co/black-forest-labs/FLUX.1-dev"
aliases:
- PGCZG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 交换子零条件（commutator-zero condition）——通过控制降采样操作与流匹配模型之间的交换子范数，实现低分辨率（LR）预览与对应高分辨率（HR）图像的感知一致性。
primary_logic: 利用流匹配模型早期采样已捕获全局结构的特性，在特定时间步进行降采样，并通过最小化交换子范数选择最优二值降采样矩阵，再以固定点式交换子零引导修正累积误差，可在免训练的条件下生成感知上与HR原图高度一致的LR预览，从而大幅加速扩散模型的工作流。
claims:
- 在FLUX.1-dev上，所提方法的DreamSim感知相似度达6.83，比简单降采样基线（9.20）低2.37，PSNR达21.182 dB，比基线高2.961 dB，同时计算量比原HR生成减少33%。
- 结合时序加速方法TaylorSeer后，总加速比达到3.05倍，且DreamSim（7.79）和PSNR（19.953 dB）均优于单独使用TaylorSeer（9.17, 18.667 dB），证明了方法正交叠加的优越性。
- 消融实验证实，交换子零引导使PSNR从19.115 dB提升至20.962 dB，DreamSim从8.56降至7.05，说明引导模块对感知一致性有决定性贡献。
- FLUX.1-dev 上 DreamSim (感知相似度,↓) = 6.83
---

# Training-free, Perceptually Consistent Low-Resolution Previews with High-Resolution Image for Efficient Workflows of Diffusion Models

> [!tip] 核心洞察
> 利用流匹配模型早期采样已捕获全局结构的特性，在特定时间步进行降采样，并通过最小化交换子范数选择最优二值降采样矩阵，再以固定点式交换子零引导修正累积误差，可在免训练的条件下生成感知上与HR原图高度一致的LR预览，从而大幅加速扩散模型的工作流。

| 字段 | 内容 |
|------|------|
| 中文题名 | 无需训练的感知一致低分辨率预览：面向扩散模型的高效工作流 |
| 英文题名 | Training-free, Perceptually Consistent Low-Resolution Previews with High-Resolution Image for Efficient Workflows of Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.09227) · [HuggingFace](https://huggingface.co/black-forest-labs/FLUX.1-dev) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Preview Generation with Commutator-Zero Guidance (交换子零引导的预览生成) |
| Dataset | FLUX.1-dev, SD3.5-L, FLUX.1-dev + TaylorSeer |

> [!tip] 效果简介
> - FLUX.1-dev 上，DreamSim (感知相似度,↓) 6.83 vs 9.20 (Naive Down.) (-2.37)；PSNR (dB↑) 21.182 vs 18.221 (Naive Down.) (+2.961)；FSIM (↑) 0.7953 vs 0.7375 (Naive Down.) (+0.0578)。
> - SD3.5-L 上，DreamSim (↓) 13.47 vs 14.81 (Naive Down.) (-1.34)；PSNR (dB↑) 14.457 vs 13.858 (Naive Down.) (+0.599)。
> - FLUX.1-dev + TaylorSeer 上，Speedup (加速比↑) 3.05x vs 1.00x (HR参考) (+2.05x)。

## 概述

扩散模型的实际工作流中，用户通常需要针对多个提示词和随机种子反复生成高分辨率（HR）图像，以筛选出理想结果。这种“生成-筛选”循环中，每一轮全分辨率采样都消耗大量计算资源，成为制约效率的核心瓶颈。本文的核心观察是：**流匹配模型在采样早期即已捕获图像的全局结构**，因此可以在特定时间步对中间表示进行降采样，随后在低分辨率（LR）空间完成剩余采样，从而大幅降低计算量。然而，朴素的降采样会破坏LR与HR之间的感知一致性，导致预览结果在构图、物体尺寸乃至色彩上发生偏移。

为解决这一问题，作者提出了**交换子零条件（commutator-zero condition）**：若降采样算子 $\mathbf{D}$ 与速度场 $v_\theta$ 可交换，即

$$[\mathbf{D}, v_\theta](x_t, t) \triangleq \mathbf{D} v_\theta(x_t, t) - v_\theta(\mathbf{D}x_t, t) = 0,$$

则降采样轨迹与原始HR轨迹在感知上保持一致。实验表明，主流流匹配模型（FLUX.1-dev、SD3.5-L）并不天然满足该条件（Table 1中交换子L2范数分别达111.03和105.90），因此需要显式干预。

基于此，论文提出了一种**免训练的预览生成方法**，包含两个关键模块：

1. **最优降采样矩阵选择**：在降采样时刻 $t_D$，从一组互斥的二值降采样矩阵候选中，选择使交换子范数最小的矩阵 $\mathbf{D}^*$，以最小化降采样操作对轨迹的扰动。
2. **交换子零引导修正**：降采样后的 $m$ 个时间步内，利用存储的HR速度场 $\mathbf{D}^* v_\theta(x_{t_D}, t_D)$ 进行固定点迭代修正，强制LR轨迹向HR轨迹对齐，抑制累积误差。

该方法无需额外训练或模型微调，可直接应用于现成的流匹配模型。

**核心实验结果**：在FLUX.1-dev上，所提方法相比朴素降采样基线，DreamSim感知距离从9.20降至6.83，PSNR从18.221 dB提升至21.182 dB，同时计算量减少33%（1.53×加速）。与正交的时序加速方法TaylorSeer结合后，总加速比达到3.05×，且感知一致性指标（DreamSim 7.79, PSNR 19.953 dB）显著优于单独使用TaylorSeer（9.17, 18.667 dB），表明方法具有良好的可叠加性。消融实验进一步证实，交换子零引导模块对PSNR有约1.85 dB的决定性贡献，最优降采样矩阵选择策略亦明显优于最近邻或随机降采样。

## 背景与动机

### 扩散模型工作流的效率瓶颈

扩散模型与流匹配模型已成为文本到图像生成的主流范式，其生成质量在近年来取得了显著提升。然而，在实际应用场景中，用户通常需要针对多个提示词（prompt）和随机种子反复生成大量候选图像，从中筛选出理想结果。这一“试错式”工作流的效率瓶颈在于：**每一次候选生成都需执行完整的高分辨率（HR）去噪过程**，导致计算成本极高，严重拖慢创作迭代速度。以 FLUX.1-dev 为例，生成一张 1024×1024 分辨率的图像需要 30 次函数评估（NFE），多次重复生成时计算开销呈线性累积。

### 现有加速方案的局限性

针对上述瓶颈，已有研究从多个维度探索加速策略，但均存在与生俱来的缺陷：

- **减少函数评估次数（Reduced-NFE）**：通过降低 NFE 来加速生成，但会牺牲图像质量和细节保真度，无法保证预览与最终 HR 结果之间的感知一致性。
- **直接生成低分辨率图像（Low-res. generation）**：以较低分辨率（如 512×512）独立生成预览，但由于去噪轨迹与 HR 生成完全解耦，构图、物体比例和色彩基调可能发生显著偏移，导致预览失去筛选参考价值。
- **超分辨率后处理（SR-upsampling）**：先生成 LR 图像再通过超分辨率模型放大至 HR，但如 Figure 2 所示，这一路径会丢失 HR 直接生成中保留的细微细节（如纹理、边缘锐度），无法忠实反映 HR 输出的真实质量。
- **简单降采样（Naive Downsampling）**：在 HR 采样的某一中间时间步直接进行最近邻降采样后继续生成，虽能部分保留全局结构，但因降采样操作与速度场之间的不可交换性，会引入累积误差，导致感知相似度显著下降（DreamSim 达 9.20，见表 Table 2）。

上述方法的共同缺陷在于：**未能建立 LR 预览与 HR 原图之间的感知一致性保证**，使得预览无法准确反映最终 HR 图像的内容和风格，削弱了筛选环节的可靠性。

### 核心动机：感知一致的预览生成

本文的核心动机源于一个关键观察：流匹配模型的早期采样阶段已捕获图像的全局结构（如构图、物体布局和色彩分布），而后续步骤主要填充高频细节。这意味着，**若能在适当的中间时间步对 HR 轨迹进行降采样，并确保降采样后的 LR 轨迹与原始 HR 轨迹在感知层面保持一致，就可以用更低的计算成本生成具有参考价值的预览图像**。

然而，实现这一目标面临根本性挑战：降采样操作 $\mathbf{D}$ 与流匹配模型的速度场 $v_\theta$ 通常不可交换，即：

$$[\mathbf{D}, v_\theta](x_t, t) \triangleq \mathbf{D} v_\theta(x_t, t) - v_\theta(\mathbf{D}x_t, t) \neq 0$$

Table 1 的实验证据表明，在 FLUX.1-dev 和 SD3.5-L 上，该交换子的空间平均 L2 范数显著不为零，这意味着直接降采样必然导致轨迹偏离，破坏 LR-HR 感知一致性。

### 本文的解决思路

针对上述问题，本文提出**交换子零条件（commutator-zero condition）**作为 LR-HR 感知一致性的充分条件，并以此为基础设计了一套免训练的预览生成方案。该方案包含两个核心机制：

1. **最优降采样矩阵选择**：在降采样时间步 $t_D$，从一组互斥的二值降采样矩阵候选中，选择使交换子范数最小的矩阵 $\mathbf{D}^*$，从源头最小化轨迹偏离。
2. **交换子零引导修正**：在降采样后的若干时间步内，利用重用的 HR 速度场进行固定点迭代修正，强制 LR 轨迹向 HR 轨迹对齐，抑制累积误差。

通过上述设计，本文方法可在免训练条件下生成与 HR 原图感知高度一致的 LR 预览，从而支持用户以低成本快速筛选候选图像，待确定理想种子后再执行完整的 HR 生成。这一工作流在保持筛选可靠性的同时，显著降低了整体计算开销，为扩散模型的实用化部署提供了高效解决方案。

## 核心创新

本工作提出**交换子零引导的预览生成**（Preview Generation with Commutator-Zero Guidance），在免训练条件下实现低分辨率预览与高分辨率原图之间的感知一致性，从而加速扩散模型的实际工作流。其核心创新围绕一个关键因果机制——**交换子零条件**（commutator-zero condition）——展开，并通过三个紧密耦合的**changed slots**予以实现。

### 创新动机：交换子零条件作为一致性判据

扩散模型用户通常需要反复生成不同提示词和种子的高分辨率（HR）图像以筛选理想结果，这一过程计算成本高昂。直接生成低分辨率（LR）图像虽可加速，但会破坏构图、色彩等全局感知属性；而先降采样再超分辨率（LR→SR）的路线已被证实会丢失细微细节（Figure 2）。本工作识别出，问题的本质在于降采样操作 $\mathbf{D}$ 与流匹配模型的速度场 $v_\theta$ 之间的**不可交换性**：当交换子 $[\mathbf{D}, v_\theta](x_t, t) \triangleq \mathbf{D} v_\theta(x_t, t) - v_\theta(\mathbf{D} x_t, t)$ 非零时，LR轨迹将偏离HR轨迹，导致感知不一致。实验测量表明，主流流匹配模型（FLUX.1-dev、SD3.5-L）的交换子平均L2范数分别高达111.03和105.90（Table 1），证实该条件在自然状态下严重不成立。因此，**强制逼近交换子零条件**成为实现LR-HR感知一致性的理论杠杆。

### Changed Slot 1：基于交换子最小化的降采样矩阵选择

**Baseline**：简单降采样方法（如最近邻降采样）在时间步 $t_D$ 直接对HR潜在表示进行空间下采样，未考虑与速度场的交互，导致交换子范数不可控。

**Proposed**：构造 $s^2$ 个互斥的二值降采样矩阵候选 $\mathcal{D}_{\mathrm{down}} = \{\mathbf{D}_1, \dots, \mathbf{D}_{s^2}\}$（每个 $s \times s$ 块内独立选择 $s^2$ 个可能位置之一，见Eq. 6-7），并在降采样时刻 $t_D$ 计算每个候选矩阵与当前速度场的交换子范数，选择使该范数**最小化**的最优矩阵：
$$\mathbf{D}^* = \arg\min_{i=1,\dots,s^2} \| [\mathbf{D}_i, v_\theta](x_{t_D}, t_D) \| \quad \text{(Eq. 8)}$$
随后以 $\mathbf{D}^*$ 执行降采样：$x_{t_D}^\downarrow \triangleq \mathbf{D}^* x_{t_D}$（Eq. 9）。消融实验（Table 4）证实，该策略的PSNR达20.962 dB，显著优于最近邻降采样（18.069 dB）和随机选择（20.851 dB），甚至优于最大化交换子的反向策略（20.408 dB），验证了“最小化交换子→更好一致性”的因果链条。

### Changed Slot 2：速度场重用与固定点式交换子零引导

**Baseline**：降采样后直接以LR分辨率继续标准采样，无任何修正机制，累积误差导致轨迹持续偏离HR参考。

**Proposed**：在降采样后的 $m$ 个时间步内，施加**交换子零引导**修正。其核心思想是利用已存储的HR速度场 $\mathbf{D}^* v_\theta(x_{t_D}, t_D)$ 作为近似目标，通过固定点迭代将LR轨迹拉回与HR轨迹对齐的方向：
$$x_t^{\downarrow, k+1} = x_t^{\downarrow, k} + \alpha \cdot \big( \mathbf{D}^* v_\theta(x_{t_D}, t_D) - v_\theta(x_t^{\downarrow, k}, t) \big) \quad \text{(Eq. 12)}$$
这一设计的关键在于**速度场重用**：基于整流流在局部时间邻域内速度场近似恒定的假设（Figure 7证实余弦相似度>0.95），无需在每一步重新计算HR速度场，从而以极低开销实现有效引导。消融实验（Table 5）表明，启用交换子零引导后，PSNR从19.115 dB跃升至20.962 dB，DreamSim从8.56降至7.05，证明该模块对感知一致性具有决定性贡献。

### Changed Slot 3：HR早期采样与LR后续采样的分阶段策略

**Baseline**：全程以单一分辨率（HR或LR）完成全部去噪步，无法兼顾全局结构捕获与计算效率。

**Proposed**：将采样过程分为两个阶段——在 $t_D$ 之前以HR分辨率进行标准流匹配采样，充分捕获全局构图和语义结构；在 $t_D$ 时刻执行最优降采样并启动交换子零引导修正，此后以LR分辨率完成剩余去噪步。这一设计利用了流匹配模型早期采样已确定全局结构的特性，使得LR预览在保持HR感知属性的同时，计算量减少约33%（FLUX.1-dev上加速比1.53×）。当与正交的时序加速方法**TaylorSeer**（Liu et al., arXiv 2025）结合时，总加速比可达3.05×，且DreamSim（7.79）和PSNR（19.953 dB）均优于单独使用TaylorSeer（9.17, 18.667 dB），验证了方法在空间轴与时序轴上的正交叠加优势（Table 3）。

### 方法定位与谱系

本方法属于**免训练、采样阶段干预**的扩散模型加速范式，与以下路线形成互补或对比：

| 路线 | 代表工作 | 干预维度 | 与本文关系 |
|------|----------|----------|------------|
| 减少函数评估次数 | Reduced-NFE (FLUX.1-dev (20)) | 时序轴 | 正交可叠加 |
| 直接低分辨率生成 | Low-res. generation | 空间分辨率 | 本文的对比基线 |
| 时序缓存加速 | **TaylorSeer** (Liu et al., arXiv 2025) | 时序轴 | 已验证正交叠加（3.05×加速） |
| 超分辨率后处理 | LR→SR pipeline | 后处理 | 本文证明其丢失细节（Figure 2） |

本方法的核心区分在于：通过**交换子零条件**这一理论工具，首次在流匹配框架下建立了降采样操作与感知一致性之间的可优化桥梁，并以**降采样矩阵选择+固定点引导**的免训练方案实现，无需任何模型微调或额外训练数据。

## 整体框架

本文提出的**交换子零引导预览生成**方法，通过在高分辨率（HR）采样过程中引入一次降采样操作及后续的交换子零引导修正，在免训练条件下生成与HR图像感知一致的低分辨率（LR）预览。整体pipeline如Algorithm 1及Figure 3所示，包含五个核心模块。

### 1. 高分辨率早期采样

在时间步 $t_D$ 之前，模型以目标HR分辨率（如1024×1024）执行标准的流匹配采样。此阶段的核心目的是**捕获图像的全局结构**——流匹配模型的早期采样步已基本确定图像的整体布局、物体位置和色彩基调。形式上，该过程遵循流ODE：

$$d x _ { t } = v _ { \theta } ( x _ { t } , t ) d t$$

在 $t \in [0, t_D]$ 区间内，每一步均计算并应用完整的速度场 $v_\theta(x_t, t)$，为后续降采样操作提供高质量的HR潜在表示 $x_{t_D}$。

### 2. 降采样矩阵选择

在时间步 $t_D$，系统面临一个关键决策：如何将HR潜在表示降采样到LR分辨率，同时最小化降采样操作与速度场之间的“冲突”。这一冲突由**交换子**（commutator）度量：

$$[ \mathbf { D } , v _ { \theta } ] ( x _ { t } , t ) \triangleq \mathbf { D } v _ { \theta } ( x _ { t } , t ) - v _ { \theta } ( \mathbf { D } x _ { t } , t )$$

交换子刻画了“先降采样再求速度”与“先求速度再降采样”之间的差异。理想情况是交换子为零，但Table 1的实证结果表明，FLUX.1-dev和SD3.5-L的交换子范数分别高达111.03和105.90，远非零值。

为逼近交换子零条件，本文构造了 $s^2$ 个互斥的候选二值降采样矩阵 $\mathcal{D}_{\mathrm{down}} = \{\mathbf{D}_1, \dots, \mathbf{D}_{s^2}\}$，每个矩阵将HR空间划分为 $h/s \times w/s$ 个块，每块仅保留一个像素。然后选择使交换子 $L_2$ 范数最小的矩阵：

$$\mathbf { D } ^ { * } = \arg \operatorname* { m i n } _ { i = 1 , \dots , s ^ { 2 } } \| [ \mathbf { D } _ { i } , v _ { \theta } ] ( x _ { t } , t ) \|$$

该选择策略是**免训练**的，仅需在 $t_D$ 时刻计算一次交换子范数，计算开销极低。

### 3. 降采样操作

使用选定的最优矩阵 $\mathbf{D}^*$，将HR潜在表示降采样到LR分辨率：

$$x _ { t } ^ { \downarrow } \triangleq \mathbf { D } ^ { * } x _ { t }$$

此操作将空间尺寸从 $H \times W$ 降至 $H/s \times W/s$（如从1024×1024降至512×512），后续去噪步的计算量随之大幅降低。同时，系统**存储** $\mathbf{D}^* v_\theta(x_{t_D}, t_D)$，供后续修正模块重用，避免重复计算HR速度场。

### 4. 交换子零引导修正

降采样后的轨迹 $x_t^\downarrow$ 与理想HR轨迹的降采样版本之间存在累积误差。为纠正这一偏差，在降采样后的 $m$ 个时间步内，应用固定点迭代式交换子零引导：

$$x _ { t } ^ { \downarrow , k + 1 } = x _ { t } ^ { \downarrow , k } + \alpha \cdot ( \mathbf { D } ^ { * } v _ { \theta } ( x _ { t _ { D } } , t _ { D } ) - v _ { \theta } ( x _ { t } ^ { \downarrow , k } , t ) )$$

该公式的核心洞察在于：**整流流的速度场在局部时间邻域近似恒定**（Figure 7验证余弦相似度>0.95），因此可以用 $t_D$ 时刻存储的HR速度场 $\mathbf{D}^* v_\theta(x_{t_D}, t_D)$ 近似当前时刻的HR速度场，避免重复计算。修正项 $\mathbf{D}^* v_\theta(x_{t_D}, t_D) - v_\theta(x_t^{\downarrow,k}, t)$ 度量了LR轨迹与HR轨迹的偏差，通过步长 $\alpha$ 逐步拉近两者。

### 5. 低分辨率续采样

经过 $m$ 步交换子零引导修正后，系统继续以LR分辨率执行剩余的 $N - t_D - m$ 步去噪采样，直至生成最终的LR预览图像 $x_1^\downarrow$。由于LR空间的计算量远低于HR空间，整体加速比可达1.53倍（Table 2）。

### 模块间的数据流

整个pipeline的数据流可概括为：
1. **HR采样** → $x_{t_D}$（HR潜在表示）
2. **矩阵选择** → $\mathbf{D}^*$（最优降采样矩阵），同时存储 $\mathbf{D}^* v_\theta(x_{t_D}, t_D)$
3. **降采样** → $x_{t_D}^\downarrow$（LR潜在表示）
4. **引导修正**（$m$步）→ 逐步对齐的LR轨迹
5. **LR续采样** → $x_1^\downarrow$（最终LR预览）

消融实验（Table 5）证实，交换子零引导模块对感知一致性有决定性贡献：启用后PSNR从19.115 dB提升至20.962 dB，DreamSim从8.56降至7.05。降采样矩阵选择策略同样关键（Table 4），arg min策略的PSNR（20.962 dB）显著优于最近邻降采样（18.069 dB）和随机选择（20.851 dB）。

### 补充图表

![[assets/figures/papers/paper_list_l945_https_arxiv_org_abs_2604_09227/figures/004_Figure_3.jpg]]
*Figure 3: Overall framework. (Left, Top) Overview of our proposed framework. Sampling is first performed in the high-resolution (HR) space up to timestep*

## 核心模块与公式推导

### 问题形式化：预览生成与交换子零条件

设高分辨率（HR）采样过程遵循流匹配常微分方程：

$$d x _ { t } = v _ { \theta } ( x _ { t } , t ) d t$$

其中 $v_\theta$ 为学习到的速度场，$x_t$ 为时刻 $t$ 的潜在表示。预览生成的目标是在某个时间步 $t_D$ 对 $x_t$ 施加降采样操作 $\mathbf{D}$，随后在低分辨率（LR）空间继续采样，使得最终生成的 LR 图像 $x_1^\downarrow$ 与 HR 图像 $x_1$ 经降采样后的结果一致，即满足合规性条件：

$$x _ { 1 } ^ { \downarrow } = \mathbf{D} x _ { 1 }$$

该条件成立的充分条件是降采样操作与速度场可交换，即交换子为零：

$$[ \mathbf { D } , v _ { \theta } ] ( x _ { t } , t ) \triangleq \mathbf { D } v _ { \theta } ( x _ { t } , t ) - v _ { \theta } ( \mathbf { D } x _ { t } , t ) = 0$$

然而，**Table 1** 的实验证据表明，在 FLUX.1-dev 和 SD3.5-L 等主流流匹配模型中，交换子的平均 L2 范数分别高达 111.03（±29.63）和 105.90（±22.38），说明交换子零条件在现实中并不成立。这正是 LR 预览与 HR 原图产生感知偏差的根本原因。

![[assets/figures/papers/paper_list_l945_https_arxiv_org_abs_2604_09227/figures/003_Table_1.jpg]]
*Table 1: Mean L2-norm of the commutator across models. We report the spatial-wise averaged L2-norm of the commutator over 100 samples for FLUX.1-dev and Stable Diffusion 3.5-Large (SD3.5-L). All models generate images or videos with 30 function evaluations (NFE). These results illustrate that flow matching models do not satisfy the commutator condition*

### 核心模块一：基于交换子最小化的降采样矩阵选择

为逼近交换子零条件，方法首先构造一组互斥的二值降采样矩阵候选集。对于 $s$ 倍降采样，将 HR 潜在空间划分为 $\frac{h}{s} \times \frac{w}{s}$ 个 $s \times s$ 的块，每个块内仅保留一个像素，共产生 $s^2$ 个互斥的候选矩阵：

$$\mathcal { D } _ { \mathrm { d o w n } } \triangleq \{ \mathbf { D } _ { 1 } , \dots , \mathbf { D } _ { s ^ { 2 } } \} , \quad \mathbf { D } _ { i } \odot \mathbf { D } _ { j } = \mathbf { 0 }$$

其中每个 $\mathbf{D}_k$ 由各块的局部选择矩阵直和并经过置换 $\Pi$ 得到：

$$\mathbf { D } _ { k } \triangleq \left( \bigoplus _ { i = 1 } ^ { h / s } \bigoplus _ { j = 1 } ^ { w / s } \mathbf { D } _ { s \times s , k } ^ { ( i , j ) } \right) \Pi$$

在降采样时间步 $t_D$，计算每个候选矩阵与当前速度场的交换子范数，选择使交换子最小的矩阵作为最优降采样矩阵：

$$\mathbf { D } ^ { * } = \arg \operatorname* { m i n } _ { i = 1 , \dots , s ^ { 2 } } \| [ \mathbf { D } _ { i } , v _ { \theta } ] ( x _ { t } , t ) \|$$

随后通过 $\mathbf{D}^*$ 获得降采样潜在表示：

$$x _ { t } ^ { \downarrow } \triangleq \mathbf { D } ^ { * } x _ { t }$$

消融实验（**Table 4**）证实，该选择策略的 PSNR 达 20.962 dB，显著优于最近邻降采样（18.069 dB）和随机降采样（20.851 dB），验证了最小化交换子对感知一致性的关键作用。

### 核心模块二：交换子零引导的固定点迭代修正

降采样后的 LR 轨迹与理想轨迹之间仍存在累积误差。交换子零引导在下采样后的 $m$ 个时间步内，通过固定点迭代强制轨迹对齐。理想修正公式为：

$$\boldsymbol { x } _ { t } ^ { \downarrow , k + 1 } = \boldsymbol { x } _ { t } ^ { \downarrow , k } + \alpha \cdot ( \mathbf { D } ^ { * } v _ { \theta } ( \boldsymbol { x } _ { t } , t ) - v _ { \theta } ( \boldsymbol { x } _ { t } ^ { \downarrow , k } , t ) )$$

其中 $\alpha$ 为修正步长。然而该公式需要当前时刻的 HR 速度场 $v_\theta(x_t, t)$，若重新计算将抵消加速收益。方法利用整流流速度场在局部时间邻域近似恒定的特性：

$$v _ { \theta } ( x _ { t _ { 0 } } , t ) \approx v _ { \theta } ( x _ { t _ { 0 } + \Delta t } , t + \Delta t )$$

**Figure 7** 的余弦相似度分析显示该假设在实践中高度成立（相似度 > 0.95）。基于此，直接复用 $t_D$ 时刻已存储的 HR 速度场 $\mathbf{D}^* v_\theta(x_{t_D}, t_D)$，得到高效修正公式：

$$x _ { t } ^ { \downarrow , k + 1 } = x _ { t } ^ { \downarrow , k } + \alpha \cdot ( \mathbf { D } ^ { * } v _ { \theta } ( x _ { t _ { D } } , t _ { D } ) - v _ { \theta } ( x _ { t } ^ { \downarrow , k } , t ) )$$

消融实验（**Table 5**）表明，启用交换子零引导后 PSNR 从 19.115 dB 提升至 20.962 dB，DreamSim 从 8.56 降至 7.05，验证了该模块对 LR-HR 一致性的决定性贡献。超参数消融（**Table 6**）进一步显示，在 $m=5$、$\alpha=0.04$ 时兼顾性能与效率。

### 整体流程

完整算法（**Algorithm 1**）包含五个阶段：
1. **HR 早期采样**：在 $t_D$ 之前以 HR 分辨率进行标准流匹配采样，捕获全局结构；
2. **降采样矩阵选择**：计算并选择使交换子范数最小的 $\mathbf{D}^*$；
3. **降采样**：使用 $\mathbf{D}^*$ 将 HR 潜在表示压缩至 LR 分辨率；
4. **交换子零引导修正**：在后续 $m$ 步内利用重用的 HR 速度场进行固定点迭代修正；
5. **LR 续采样**：以 LR 分辨率完成剩余去噪步，输出最终 LR 预览。

### 补充图表

![[assets/figures/papers/paper_list_l945_https_arxiv_org_abs_2604_09227/figures/009_Figure_6.jpg]]
*Figure 6: Changes in average commutator norm. We measure the change in commutator norm at timesteps*

![[assets/figures/papers/paper_list_l945_https_arxiv_org_abs_2604_09227/figures/011_Figure_7.jpg]]
*Figure 7: Cosine similarity analysis on velocity consistency of flow-matching models. We report the mean and standard deviation of cosine similarity between*

![[assets/figures/papers/paper_list_l945_https_arxiv_org_abs_2604_09227/figures/008_Figure_5.jpg]]
*Figure 5: Generalization of commutator-zero guidance. We show that commutator-zero guidance can be expanded to other operations. For warping, a large kernel (128 × 128) with correlation correction produces distortion, while our method effectively handles artifacts. For translation, na¨ıve cause noticeable difference and unintended objects, whereas ours preserves image content*

## 实验与分析

### 主要定量结果

**Table 2** 在 FLUX.1-dev 和 SD3.5-L 上对本文方法与三类替代方案进行了系统比较：(i) 减少函数评估次数的 Reduced-NFE；(ii) 直接生成低分辨率图像的 Low-res. generation；(iii) 在时间步 $t_D$ 使用最近邻降采样后继续生成的 Naive Downsampling。所有方法均使用 NFE = 30，评估分辨率为 512×512，HR 参考图像为 1024×1024。

在 FLUX.1-dev 上，本文方法取得了全面的最优性能：
- **感知相似度**：DreamSim 降至 6.83，比 Naive Downsampling 的 9.20 降低 2.37，表明 LR 预览与 HR 原图在感知层面高度一致。
- **底层相似度**：PSNR 达 21.182 dB，较 Naive Downsampling 的 18.221 dB 提升 2.961 dB；FSIM 从 0.7375 提升至 0.7953。
- **图像质量**：PIQE 为 28.55，优于其他替代方案。
- **计算效率**：加速比达 1.53×，计算量减少约 33%。

在 SD3.5-L 上，方法同样展现出跨模型的泛化能力：DreamSim 从 14.81 降至 13.47，PSNR 从 13.858 dB 提升至 14.457 dB。

值得注意的是，Reduced-NFE 和 Low-res. generation 虽然计算效率更高，但感知相似度和 PSNR 均显著劣于本文方法，说明单纯的降分辨率或减少步数无法保证 LR-HR 的感知一致性。

### 与时序加速方法的正交叠加

**Table 3** 展示了本文方法与 **TaylorSeer**（Liu et al., arXiv 2025）结合后的性能。TaylorSeer 是一种沿时序轴缓存加速的正交方法。两者叠加后：
- 总加速比达到 3.05×，远超单独使用 TaylorSeer 的加速效果。
- DreamSim 为 7.79，优于 TaylorSeer 单独使用的 9.17。
- PSNR 为 19.953 dB，较 TaylorSeer 单独的 18.667 dB 提升 1.286 dB。

这一结果证明本文方法可与现有时序加速技术正交叠加，在进一步提升效率的同时保持甚至改善感知一致性。

### 消融实验

**降采样矩阵选择策略**（Table 4）：比较了三种策略——最近邻降采样、随机采样、以及本文的交换子最小化（arg min）选择。最近邻降采样 PSNR 仅 18.069 dB，性能最差；随机采样提升至 20.851 dB；本文的交换子最小化策略达到 20.962 dB，验证了最小化交换子范数对轨迹对齐的关键作用。作为对照，使用 arg max 选择最大交换子矩阵的策略 PSNR 降至 20.408 dB，进一步证实了交换子最小化的必要性。

**交换子零引导的有效性**（Table 5）：移除交换子零引导后，PSNR 从 20.962 dB 骤降至 19.115 dB，DreamSim 从 7.05 恶化至 8.56。该模块是维持 LR-HR 感知一致性的决定性组件，其代价是计算量略微增加（加速比从 1.57× 降至 1.53×），但换取的感知收益远超成本。

**超参数敏感性**（Table 6）：修正步数 $m$ 和步长 $\alpha$ 存在明显的精度-效率权衡。增大 $m$ 可提升 PSNR，但计算开销随之增加。每组 $m$ 均存在最优 $\alpha$：在 $m=5$、$\alpha=0.04$（FLUX）或 $\alpha=0.01$（SD3.5）时取得最佳综合性能。

### 定性分析

**Figure 4** 的定性比较直观展示了方法优势。Naive Downsampling 常导致构图偏移、物体尺寸变化甚至色调漂移；Reduced-NFE 和 Low-res. generation 则丢失了 HR 原图中的结构细节。本文方法生成的 LR 预览在构图、色彩和物体关系上与 HR 参考高度一致，同时计算量显著降低。

**Figure 5** 展示了交换子零引导向平移和变形操作的推广能力。对于大核变形操作，直接应用会产生明显失真，而引入交换子零引导后伪影被有效消除，说明该框架不仅限于降采样，对更广泛的空间变换同样适用。

### 关键支撑证据

**Table 1** 提供了交换子条件不成立的实证依据：在 FLUX.1-dev 上，交换子的空间平均 L2 范数高达 111.03（±29.63），SD3.5-L 上为 105.90（±22.38）。这直接证明了流匹配模型本身不满足交换子零条件，因此需要本文提出的降采样矩阵选择和交换子零引导来强制逼近该条件。

**Figure 6** 显示交换子零引导有效降低了后续时间步的交换子范数，**Figure 7** 通过余弦相似度分析验证了整流流速度场在局部时间邻域的恒定性假设（相似度 > 0.95），为速度场重用策略提供了理论支撑。

### 失败模式与局限

尽管方法在主流流匹配模型上表现优异，仍存在若干已知局限：
1. **近似条件非严格保证**：交换子零条件和轨迹合规性依赖经验近似，并非所有架构或采样调度下都严格成立。
2. **降采样算子表达能力受限**：互斥的块状二值矩阵对空间结构敏感，可能在某些复杂纹理场景下产生次优结果。
3. **速度场重用假设**：整流流的局部线性假设在强非线性模型或极端场景下可能失效，导致修正精度下降。
4. **精度-效率权衡**：交换子零引导引入额外计算，增加 $m$ 虽提升质量但降低加速比，需根据应用场景权衡。

以上局限均来自论文自述的限制分析，部分边界条件（如对非流匹配扩散模型的适用性）仍需后续工作验证。

### 补充图表

![[assets/figures/papers/paper_list_l945_https_arxiv_org_abs_2604_09227/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison on FLUX.1-dev and SD3.5-L. Using the FLUX.1-dev and Stable Diffusion 3.5-Large (SD3.5-L) models with NFE = 30, we generate HR (1024 × 1024) reference images. We compare three variants: (i) reduced-NFE generation, (ii) LR (512 × 512) generation with the same NFE, and (iii) a na¨ıve baseline applying nearest downsampling at timestep*

![[assets/figures/papers/paper_list_l945_https_arxiv_org_abs_2604_09227/figures/006_Table_3.jpg]]
*Table 3: Quantitative comparison on FLUX.1-dev with temporal-axis acceleration. We compare our approach combined with orthogonal temporal-axis acceleration. Our method achieves superior performance across all metrics, including image quality, perceptual similarity, and low-level similarity*

![[assets/figures/papers/paper_list_l945_https_arxiv_org_abs_2604_09227/figures/010_Table_4.jpg]]
*Table 4: Ablation study on D selection. We compare three strategies for selecting D: (i) nearest-neighbor downsampling, (ii) random sampling, and (iii) D∗ obtained via the arg max(·) operation in Eq. 8. The results show that our approach, which minimizes the commutator value, achieves the best performance*

![[assets/figures/papers/paper_list_l945_https_arxiv_org_abs_2604_09227/figures/012_Table_5.jpg]]
*Table 5: Ablation study on commutator-zero guidance. Comparing results with and without commutator-zero guidance (CG) shows that while computational efficiency slightly decreases with correction, both perceptual similarity and PSNR increase, highlighting the effectiveness of our proposed method*

![[assets/figures/papers/paper_list_l945_https_arxiv_org_abs_2604_09227/figures/013_Table_6.jpg]]
*Table 6: Ablation study on hyperparameter m and α. We investigate how varying m and α affects performance. Increasing m improves PSNR but also raises computational demand, showing a clear trade-off. Each m exhibits an optimal step size α*

![[assets/figures/papers/paper_list_l945_https_arxiv_org_abs_2604_09227/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative comparison of our proposed method. While other simple alternatives often result in changes to composition, object size, or even color tone, our proposed approach synthesizes low-resolution images faster while preserving the composition and color fidelity of the original image. The prompts used for image generation are provided in the supplementary materials*

![[assets/figures/papers/paper_list_l945_https_arxiv_org_abs_2604_09227/figures/002_Figure_2.jpg]]
*Figure 2: Comparison between SR-upsampled and directly generated HR images. Using FLUX.1-dev, we (a) generated a low-resolution (LR, 256 × 256) image followed by 4× superresolution (SR) to obtain a high-resolution (HR*

## 方法谱系与知识库定位

### 问题定位：扩散模型工作流的效率瓶颈

当前扩散模型（包括流匹配模型）在图像生成中展现出卓越的视觉质量，但其实际应用面临显著的效率问题。用户通常需要针对不同提示词和随机种子反复生成高分辨率（HR）图像以筛选理想结果，这一“试错-筛选”工作流中，每一次HR生成都需完整执行昂贵的去噪过程，计算成本极高。本文的核心洞察是：**在筛选阶段，用户并不需要最终的高保真度图像，而只需要一张能准确反映HR图像构图、色彩和语义结构的低分辨率（LR）预览**。若能以更低的计算代价生成感知上与HR一致的LR预览，即可大幅加速整个工作流。

### 方法谱系：从超分辨率到免训练预览生成

现有解决这一效率问题的思路可归纳为三条路径：

1. **减少函数评估次数（Reduced-NFE）**：直接降低去噪步数，以精度换速度。如表2所示，FLUX.1-dev (20)虽然获得了1.53×加速，但DreamSim感知相似度仅为8.33，PSNR降至18.181 dB，表明简单减少NFE会显著损害图像质量。

2. **超分辨率级联（LR→SR）**：先生成LR图像，再通过超分辨率模型上采样。然而，如Figure 2所示，这一管线会丢失细微细节（如纹理和边缘），因为LR生成阶段未能捕获HR空间中的完整信息，且SR模型难以恢复这些丢失的高频成分。

3. **时序轴加速方法**：如**TaylorSeer**（Liu et al., arXiv 2025），通过缓存和重用中间特征来减少计算量。该方法与本文工作正交，可叠加使用。

本文方法属于第四条路径：**免训练的HR→LR预览生成**。与上述方法不同，本文不试图加速HR生成本身，而是通过在HR采样的早期阶段（时间步 $t_D$）进行降采样，并施加交换子零引导修正，直接生成与HR感知一致的LR预览。这一思路的关键优势在于：（1）无需额外训练；（2）保留了HR早期采样捕获的全局结构；（3）可与现有加速方法正交叠加。

### 核心机制：交换子零条件与轨迹对齐

方法的核心理论支柱是**交换子零条件**（commutator-zero condition）。对于降采样矩阵 $\mathbf{D}$ 和速度场 $v_\theta$，定义交换子：

$$[\mathbf{D}, v_\theta](x_t, t) \triangleq \mathbf{D} v_\theta(x_t, t) - v_\theta(\mathbf{D} x_t, t)$$

若该交换子恒为零，则降采样操作与速度场可交换，意味着LR轨迹 $x_t^\downarrow = \mathbf{D} x_t$ 严格遵循HR轨迹的降采样版本，从而保证LR-HR感知一致性。然而，**Table 1** 显示，FLUX.1-dev和SD3.5-L上的交换子L2范数分别高达111.03和105.90，证明这一条件在实际模型中并不成立。

本文通过两个互补机制逼近交换子零条件：
- **降采样矩阵选择**（Sec 3.3）：在 $s^2$ 个互斥的二值降采样矩阵候选中，选择使交换子范数最小的 $\mathbf{D}^*$，从源头最小化轨迹偏离。
- **交换子零引导**（Sec 3.4）：在下采样后的 $m$ 个时间步内，利用存储的HR速度场 $\mathbf{D}^* v_\theta(x_{t_D}, t_D)$ 进行固定点迭代修正，强制LR轨迹向HR轨迹对齐。

### 与基线方法的实证对比

在FLUX.1-dev上（Table 2），本文方法在多个维度上显著优于基线：

| 方法 | 加速比 | DreamSim↓ | PSNR↑ (dB) | FSIM↑ |
|------|--------|-----------|------------|-------|
| HR参考 | 1.00× | — | — | — |
| Reduced-NFE (20步) | 1.53× | 8.33 | 18.181 | 0.7403 |
| 直接LR生成 (512²) | 1.53× | 8.33 | 18.181 | 0.7403 |
| Naive Downsampling | 1.53× | 9.20 | 18.221 | 0.7375 |
| **本文方法** | **1.53×** | **6.83** | **21.182** | **0.7953** |

关键发现：
- 在相同加速比（1.53×）下，本文方法的DreamSim（6.83）比Naive Downsampling（9.20）低2.37，PSNR高2.961 dB，证明交换子零引导对感知一致性有决定性贡献。
- 直接LR生成与Reduced-NFE在感知质量上无显著优势，说明单纯降低分辨率或步数无法保持HR的结构信息。

### 正交叠加能力

本文方法可与时序轴加速方法无缝集成。结合**TaylorSeer**后（Table 3），总加速比达到**3.05×**，且DreamSim（7.79）和PSNR（19.953 dB）均优于单独使用TaylorSeer（9.17, 18.667 dB）。这表明交换子零引导修正的LR轨迹与TaylorSeer的缓存机制互不冲突，叠加后仍能保持感知一致性优势。

### 消融实验的关键证据

1. **降采样矩阵选择策略**（Table 4）：arg min策略（PSNR 20.962 dB）显著优于最近邻降采样（18.069 dB）和随机选择（20.851 dB），甚至优于arg max策略（20.408 dB），验证了最小化交换子范数的有效性。

2. **交换子零引导的必要性**（Table 5）：移除引导后，PSNR从20.962 dB骤降至19.115 dB，DreamSim从7.05升至8.56，证明该模块是方法的核心贡献。

3. **超参数敏感性**（Table 6）：修正步数 $m=5$、步长 $\alpha=0.04$ 时达到最佳性能-效率平衡。

### 适用边界与局限

1. **模型依赖性**：方法假设流匹配模型的速度场在局部时间邻域近似恒定（$v_\theta(x_{t_0}, t) \approx v_\theta(x_{t_0+\Delta t}, t+\Delta t)$）。Figure 7显示FLUX.1-dev上余弦相似度>0.95，但这一性质并非所有架构或采样调度下严格保证。对于表现出强非线性行为的模型，速度场重用可能引入额外误差。

2. **降采样算子的表达能力**：当前方法将降采样限制为互斥的块状二值矩阵，虽保证了计算效率，但可能对空间结构敏感。更灵活的降采样算子（如自适应、非二值）可能进一步提升表现，但需权衡计算开销。

3. **修正步数的精度-效率权衡**：交换子零引导在 $m$ 个时间步内引入额外计算。虽然 $m=5$ 时已取得良好平衡，但在极端效率需求下可能需要进一步压缩。

4. **对非流式框架的适用性**：方法的核心推导基于流匹配ODE，其向DDPM等扩散框架的推广需要重新审视交换子零条件的定义和引导机制。

### 开放问题

1. **理论保证**：交换子零条件能否在特定模型类或正则化条件下得到更严格的理论证明？当前方法依赖经验近似，缺乏收敛性保证。

2. **算子泛化**：Figure 5展示了交换子零引导向平移和变形操作的推广潜力，但其对更复杂空间变换（如旋转、透视变换）的适用性及理论边界尚待探索。

3. **自适应机制**：降采样时间步 $t_D$、修正步数 $m$ 和步长 $\alpha$ 目前为固定超参数。能否设计自适应策略，根据输入提示的复杂度或模型状态动态调整？

4. **视频生成扩展**：在视频扩散模型中，时空降采样与交换子零条件的交互更为复杂，方法的效率和一致性表现有待验证。

5. **与其他加速范式的深度集成**：除TaylorSeer外，方法能否与蒸馏、量化、架构剪枝等加速技术协同，形成更全面的效率优化方案？

## 原文 PDF

![[paperPDFs/CVPR_2026/Training_free_Perceptually_Consistent_Low_Resolution_Previews_with_High_Resolution_Image_for_Efficient_Workflows_of_Diffusion_Models.pdf]]