---
title: "Real-Time Radiance Caching for Volume Path Tracing using 3D Gaussian Splatting"
type: paper
paper_level: A
venue: "IEEE VIS"
year: 2025
pdf_ref: paperPDFs/IEEE_VIS_2025/Real_Time_Radiance_Caching_for_Volume_Path_Tracing_using_3D_Gaussian_Splatting.pdf
project_link: https://dbauer15.github.io/papers/gscache/
aliases:
- RTRCVPTU3GS
tags:
- IEEE_VIS_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过构建多级路径空间3D高斯辐射度缓存，并引入基于路径吞吐量的可调节终止系数C，在偏差与方差之间进行灵活权衡；利用噪声路径样本结合HDR损失和正则化实现稳定在线训练，使缓存持续自适应优化。"
primary_logic: "将路径辐射度按长度分层缓存，利用3D高斯场配合可微光栅化实现快速查询；关键发现是可以从蒙特卡洛渲染器的高噪声单样本路径中在线学习无偏辐射度表示——即使训练目标为单样本噪声，梯度优化仍收敛到期望值，从而在极低SPP下大幅提升图像质量。"
claims:
- "在1 SPP下，GSCache在Carp数据集的PSNR达到16.877，大幅领先NEE（14.657）和NRC（15.524）。"
- "在FullBody数据集上，GSCache冷启动后不到16帧，图像质量即超过无缓存渲染器。"
- "消融实验表明，移除正则化（-REG）导致训练崩溃、质量锐降（SMAPE: 0.089 vs 0.040），证明AdamW对基于噪声数据的在线训练不可或缺。"
- "缓存开销恒定，总运行时间随SPP增加比基线增长更慢；在1 SPP下整体帧时间与NRC相当（约89 ms）。"
---

# Real-Time Radiance Caching for Volume Path Tracing using 3D Gaussian Splatting

> [!tip] 核心洞察
> 将路径辐射度按长度分层缓存，利用3D高斯场配合可微光栅化实现快速查询；关键发现是可以从蒙特卡洛渲染器的高噪声单样本路径中在线学习无偏辐射度表示——即使训练目标为单样本噪声，梯度优化仍收敛到期望值，从而在极低SPP下大幅提升图像质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于3D高斯泼溅的体积路径追踪实时辐射度缓存 |
| 英文题名 | Real-Time Radiance Caching for Volume Path Tracing using 3D Gaussian Splatting |
| 会议/期刊 | IEEE VIS 2025 |
| Links | [paper](https://arxiv.org/abs/2507.19718); [Project](https://dbauer15.github.io/papers/gscache/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | GSCache |
| Dataset | Carp (1 SPP), FullBody (1 SPP), Overall frame time (FullBody) |

> [!tip] 效果简介
> - Carp (1 SPP) 上，PSNR 为 16.877 (GSCache)，对比 14.657 (NEE) / 15.524 (NRC)，变化 +2.22 / +1.353。
> - FullBody (1 SPP) 上，PSNR 为 15.847 (GSCache)，对比 12.454 (NEE) / 14.266 (NRC)，变化 +3.393 / +1.581。
> - Overall frame time (FullBody) 上，Total time (PT + ST/IT + OT) 为 46.64 + 11.42 + 31.49 = 89.55 ms，对比 NRC 47.66 + 13.91 + 26.92 = 88.49 ms，变化 ~1 ms overhead。

## 概述

**问题瓶颈**：体积路径追踪在低样本数（1 SPP）下，蒙特卡洛积分产生大量噪声，严重损害实时渲染质量。传统辐射度缓存方法——无论是基于世界空间探针的启发式方案，还是基于单一 MLP 的神经缓存（如 NRC, Müller et al., ACM Trans. Graph. 2021）——难以同时满足实时性、对体数据的适应性以及动态场景参数快速响应的需求。

**核心思路**：本文提出 **GSCache**，一种基于 3D 高斯泼溅（3D Gaussian Splatting）的多级路径空间辐射度缓存。其关键创新在于：将路径辐射度按长度分层缓存为 3D 高斯集合，利用可微光栅化实现快速查询；并从蒙特卡洛渲染器的高噪声单样本路径中在线学习无偏辐射度表示——即使训练目标为单样本噪声，梯度优化仍收敛到期望值，从而在极低 SPP 下大幅提升图像质量。

**方法定位**：GSCache 属于辐射度缓存方法谱系，但与现有工作有三个根本差异：
- **缓存表示**：用多级路径空间 3D 高斯泼溅替代世界空间探针或单一 MLP；
- **路径终止**：采用基于路径吞吐量亮度的概率终止策略，配合用户参数 $C$ 和级联概率修正以保持无偏；
- **训练范式**：从噪声路径样本在线学习，使用 HDR 归一化损失和 AdamW 优化器，而非依赖干净图像监督。

**主要结果**：在 1 SPP 下，GSCache 在 Carp 数据集上 PSNR 达到 16.877，显著优于 NEE（14.657）和 NRC（15.524）；在 FullBody 数据集上 PSNR 达 15.847（NEE 12.454，NRC 14.266）。冷启动后不到 16 帧，图像质量即超过无缓存渲染器。缓存开销恒定，1 SPP 下总帧时间约 89 ms，与 NRC 相当。消融实验证实，移除正则化会导致训练崩溃（SMAPE 从 0.040 升至 0.089），证明 AdamW 对基于噪声数据的在线训练不可或缺。

## 背景与动机

体积路径追踪是科学可视化与真实感渲染中模拟光传输的核心技术。其基本任务是求解体积辐射传输方程：

$$L ( x , \omega ) = \int _ { 0 } ^ { \infty } T _ { r } ( x ^ { \prime } \to x ) L _ { s } ( x ^ { \prime } , - \omega ) d t$$

该方程沿视线积分所有经过透射率衰减的源项辐射。在实际渲染中，路径追踪器通过蒙特卡洛采样来估计这一积分，但**核心瓶颈**在于：在低样本数（如每像素1个样本，1 SPP）下，蒙特卡洛估计会产生大量噪声，严重损害实时渲染的图像质量。对于医学CT、科学模拟等体积数据集，这种噪声会掩盖关键结构细节，使交互式探索变得困难。

现有方法试图通过辐射度缓存来缓解这一问题——用偏差换取方差降低。传统缓存方案通常将辐射度存储为世界空间中的探针（probes），可在渲染过程中查询。代表性工作如**NRC**（Müller et al., ACM Trans. Graph. 2021）使用单一MLP网络作为神经辐射度缓存，代表了该方向的最新进展。然而，这些方法面临三重缺口：

1. **实时性约束**：缓存构建和查询必须在毫秒级帧预算内完成，传统探针或神经网络推理开销难以满足。
2. **体数据适应性**：体积路径追踪中，辐射度分布在三维空间且与路径长度强相关，世界空间的探针结构难以有效捕捉路径空间的结构。
3. **动态场景响应**：当传递函数、光照或相机参数改变时，缓存需要快速适应，而离线预训练的缓存无法胜任。

本文的**核心动机**在于：能否从蒙特卡洛渲染器的高噪声单样本路径中在线学习一个无偏的辐射度表示？关键洞察是：即使训练目标为单样本噪声值，梯度优化仍能收敛到期望辐射度——这为在极低SPP下实现高质量实时渲染提供了理论基础。基于此，我们提出**GSCache**，一种多级路径空间3D高斯辐射度缓存，通过可微光栅化实现快速查询，并利用噪声路径样本进行在线持续优化，在偏差与方差之间提供灵活的用户可控权衡。

## 核心创新

GSCache 的核心创新在于将体积路径追踪的辐射度缓存从传统世界空间探针或单一神经表示，迁移到**多级路径空间3D高斯泼溅**框架中，并建立了一套完整的在线学习与无偏查询机制，从而在极低样本数（1 SPP）下实现实时高质量渲染。

### 1. 多级路径空间3D高斯缓存表示

传统辐射度缓存方法（如 NRC, Müller et al., ACM Trans. Graph. 2021）将辐射度存储于世界空间探针或单一 MLP 中，难以同时捕捉不同路径长度对应的辐射度分布差异。GSCache 的关键改变在于：**按路径长度分层缓存**。每个缓存级别独立存储特定长度 $n$ 的所有路径的衰减辐射度（attenuated path-space radiance），各级别之间通过对初始点云进行对数子采样构建，类似纹理处理中的 MIP 层级结构（Section 3.1, 3.2）。

这一设计使得缓存能够自然适配路径追踪的递归结构：短路径（如直接光照）和长路径（多次散射）分别由不同级别的高斯场表示，查询时根据当前路径长度直接索引对应级别，避免了单一表示对不同尺度辐射度信息的混淆。

### 2. 基于吞吐量的可调节路径终止策略

路径追踪中何时终止路径并转向缓存查询，是偏差-方差权衡的核心控制点。传统方法多依赖基于空间扩散或方差的启发式，缺乏对辐射度贡献的直接感知。GSCache 引入了**基于路径吞吐量亮度的概率终止机制**（Section 3.3, Algorithm 1）：利用当前路径吞吐量 $T_r$ 的亮度生成终止概率 $p$，并通过用户参数 $C$ 灵活调节终止倾向。

更关键的是，GSCache 设计了**级联缓存采样概率修正**以保持无偏性（Section 3.4）。当路径在前 $n-1$ 步均未终止、第 $n$ 步命中缓存时，缓存的辐射度需除以累积采样概率 $\beta_{n-1}$，即 $\hat{L}_n = \frac{L_n \prod_{k=1}^{n} \sigma_k}{\beta_{n-1}}$。图 4 的消融实验证实，忽略该修正会导致显著的衰减误差；加入修正后，渲染结果与参考图像高度一致。这一机制将偏差控制从启发式猜测转变为精确的概率补偿。

### 3. 从噪声路径样本中在线学习无偏辐射度

这是 GSCache 最深刻的理论创新。常规 3DGS 训练需要干净的像素级真值，而 GSCache 的缓存训练目标直接来自**蒙特卡洛渲染器的高噪声单样本路径**（Section 3.5, 3.6）。论文发现了一个关键性质：即使训练目标为单样本噪声，梯度优化仍收敛到期望值——因为噪声的期望等于无偏辐射度。

基于此，GSCache 维护 $K$ 个中间路径缓冲区（每个缓存级别一个），收集路径追踪过程中产生的噪声样本，使用 HDR 归一化损失函数 $\mathcal{L}_{hdr} = \frac{(\hat{x} - \hat{y})^2}{k(\hat{y} + 0.01)^2}$ 和 AdamW 优化器进行在线训练。消融实验（Fig. 12）提供了决定性证据：移除正则化（-REG）导致训练崩溃，SMAPE 从 0.040 恶化至 0.089，证明 AdamW 对噪声数据在线训练的稳定性不可或缺。这一发现使得缓存能够在渲染过程中持续自适应优化，无需预计算或干净参考图像。

### 4. 创新协同效应

上述三个 changed slots 并非孤立改进，而是形成因果闭环：多级路径空间表示提供了查询的粒度基础；吞吐量终止策略决定了何时查询缓存；噪声学习理论保证了缓存表示能持续逼近无偏辐射度。实验结果表明，在 1 SPP 下 GSCache 的 PSNR 达到 16.877（Carp 数据集），显著领先 NEE（14.657）和 NRC（15.524）；在 FullBody 数据集上冷启动后不到 16 帧，图像质量即超过无缓存渲染器（Fig. 7），验证了该协同设计的有效性。

## 整体框架

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2507_19718/figures/007_Figure_6.jpg]]
*Figure 6: Visual quality of our method compared to the baseline path tracer. We show results for images at 1 SPP and compare our method (GSCache) against a baseline volume path tracer with uniform sampling (Uniform), a version that uses next-event estimation (NEE), and our implementation of NRC [34]*

GSCache 的整体管线由两个紧密耦合的循环构成：**路径追踪渲染循环**与**缓存在线训练循环**。两者共享路径样本缓冲区，在每一帧中交替执行，使缓存能够持续从渲染器的高噪声单样本路径中学习并反馈高质量辐射度估计。

### 核心模块与数据流

1. **缓存初始化（Cache Initialization）**  
   在渲染开始前，通过对体积数据执行一次采样遍历生成初始点云（默认 $N = 300\text{k}$）。该点云按路径长度级别进行对数下采样，为每个缓存级别构建独立的 3D 高斯集合。各向同性尺度由 3 近邻平均距离经异常值裁剪后确定：
   $$s_i = \frac{ (\mu_N + 2 \cdot \sigma_N) \wedge \frac{1}{3}\sum_{j=0}^{2} d_{ij} }{2}$$

2. **路径追踪与终止（Path Tracing & Termination）**  
   渲染器沿路径逐段追踪，在每个顶点处计算当前路径吞吐量的亮度，并据此生成终止概率 $p$。用户通过系数 $C$ 控制偏差-方差权衡：$C$ 越大，路径越早终止并转向缓存查询。若路径在到达光源前被终止，则以缓存辐射度替代零贡献样本；否则使用无偏路径样本。

3. **缓存采样与无偏修正（Cache Sampling & Bias Correction）**  
   当路径在深度 $n$ 处命中缓存时，需对缓存的辐射度进行级联概率修正，以保持估计的无偏性。有效衰减辐射度定义为：
   $$\hat{L}_n = \frac{L_n \prod_{k=1}^{n} \sigma_k}{\beta_{n-1}}$$
   其中 $\beta_{n-1}$ 为前 $n-1$ 次缓存未命中概率的乘积。该修正补偿了因路径提前终止而引入的偏差，是方法保持无偏性的关键机制（Fig. 4 的误差图验证了其必要性）。

4. **缓存训练（Cache Training）**  
   系统维护 $K$ 个路径缓冲区（每缓存级别一个），收集路径追踪过程中产生的噪声辐射度样本。训练循环使用高斯泼溅的可微光栅化，以 **HDR 归一化损失** 和 **AdamW 优化器** 在线优化各缓存级别的高斯参数：
   $$\mathcal{L}_{hdr} = \frac{(\hat{x} - \hat{y})^2}{k(\hat{y} + 0.01)^2}$$
   核心理论洞见在于：即使训练目标为单样本噪声，梯度优化仍收敛到期望值，从而在极低 SPP 下实现稳定学习。

5. **高斯光栅化查询（Gaussian Splatting Rasterization）**  
   各级别 3D 高斯被光栅化为缓存图像，路径追踪器可直接从中查询对应路径长度的衰减辐射度，实现快速、可微的缓存访问。

### 输入输出流

- **输入**：体积密度场、传递函数、相机参数、用户指定的终止系数 $C$。
- **输出**：经缓存增强的渲染图像，在 1 SPP 下即可达到显著优于无缓存路径追踪（Uniform/PT）和次世代估计（NEE）的图像质量。
- **中间状态**：多级路径空间 3D 高斯缓存持续在线更新，路径缓冲区作为渲染循环与训练循环之间的共享数据通道。

整个管线在单 GPU 上运行，缓存开销恒定，总帧时间与 **NRC**（Müller et al., ACM Trans. Graph. 2021）相当（约 89 ms），但图像质量大幅领先。

## 核心模块与公式推导

### 3.1 路径空间辐射度缓存表示

GSCache的核心是将体积路径追踪的辐射度在**路径空间**中按路径长度分层缓存。给定体积辐射传输方程：

$$L ( x , \omega ) = \int _ { 0 } ^ { \infty } T _ { r } ( x ^ { \prime } \to x ) L _ { s } ( x ^ { \prime } , - \omega ) d t$$

其中 $T_r$ 为透射率，$L_s$ 为源项辐射度。路径追踪积分可表征为所有可能长度路径的集合（Fig. 2）。GSCache将长度为 $n$ 的所有路径的总辐射度存储在一个独立的缓存层级中，共维护 $K$ 个层级，每一层由一组3D高斯泼溅（3D Gaussian Splatting）表示。缓存层级尺寸从高层到低层进行对数子采样，类似于纹理处理中的MIP层级构建。

### 3.2 缓存初始化

缓存通过单次体积密度采样生成初始点云。对体积数据进行一次采样遍历，生成 $N=300k$ 个初始点（消融实验表明此规模在质量与开销间取得良好平衡）。每个高斯各向同性尺度初始化为：

$$s _ { i } = \frac { ( \mu _ { N } + 2 * \sigma _ { N } ) \wedge \frac { 1 } { 3 } \sum _ { j = 0 } ^ { 2 } d _ { i j } } { 2 }$$

其中 $d_{ij}$ 为第 $i$ 个高斯的3个最近邻距离，$\mu_N$ 和 $\sigma_N$ 为所有最近邻距离的均值和标准差。该公式将尺度限制在均值加2倍标准差以内，并缩放至50%，防止异常大值导致过平滑。

### 3.3 路径终止启发式

路径终止策略是GSCache实现偏差-方差权衡的关键控制旋钮。引入用户可调参数 $C$，基于当前路径吞吐量 $Tr$ 的亮度生成终止概率 $p$（Algorithm 1）。若路径以非零辐射度贡献终止，使用无偏样本；否则，在终止路径长度处查询缓存辐射度值替代。这一机制使渲染器在路径贡献微弱时提前转向缓存，避免低效的后续散射采样。

### 3.4 级联缓存采样与无偏修正

缓存查询采用级联重要性采样：在每个路径顶点，以概率 $p$ 决定是否终止并查询对应层级的缓存。为保持估计无偏，需对缓存辐射度进行概率修正。当缓存在第 $n$ 层被命中时，有效衰减辐射度为：

$$\hat { L } _ { n } = \frac { L _ { n } \prod _ { k = 1 } ^ { n } \sigma _ { k } } { \beta _ { n - 1 } }$$

其中 $\prod_{k=1}^{n} \sigma_k$ 为常规路径衰减（各顶点反照率乘积），$\beta_{n-1} = \prod_{k=1}^{n-1} p_k$ 为前 $n-1$ 步未命中缓存的累积概率。除以 $\beta_{n-1}$ 补偿了缓存被多次“错过”的概率效应，确保估计的无偏性（Fig. 4 消融验证了忽略此修正将引入显著误差）。

### 3.5 在线训练与HDR损失

GSCache采用实时在线训练范式。维护 $K$ 个中间路径缓冲区，每个对应一个缓存层级，收集路径追踪过程中产生的噪声路径样本。训练使用高斯泼溅可微光栅化进行逆渲染优化，损失函数采用HDR归一化损失：

$$\mathcal { L } _ { h d r } = \frac { \left( \hat { x } - \hat { y } \right) ^ { 2 } } { k ( \hat { y } + 0 . 0 1 ) ^ { 2 } }$$

其中 $\hat{x}$ 为预测值，$\hat{y}$ 为噪声目标值，分母归一化项处理高动态范围辐射度值。**核心理论洞察**在于：即使训练目标为单样本噪声，梯度优化仍收敛到期望值，使得从极低SPP（如1 SPP）的噪声路径中学习无偏辐射度表示成为可能。优化器采用AdamW，消融实验（Fig. 12）表明移除正则化（-REG）将导致训练崩溃，SMAPE从0.040恶化至0.089，验证了AdamW对基于噪声数据的在线训练不可或缺。

## 实验与分析

### 1. 实验设置

实验在六个体积数据集上进行（Table 1），涵盖医学扫描（Carp、Foot）、CT扫描（Bonsai、FullBody）和科学模拟（Nucleon、Meteorite），数据分辨率从 $256^3$ 到 $1024 \times 1024 \times 1024$ 不等，传递函数复杂度各异。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2507_19718/figures/008_Table_1.jpg]]
*Table 1: We use volume datasets from medical scans, CT scans, and scientific simulations to test our method. Data ranges in size and complexity*

所有方法基于相同路径追踪后端（NVIDIA OptiX 7.3），在相同硬件、相机路径和传递函数下评估。为公平对比，NRC的实现额外增加了与GSCache相同的路径终止启发式和训练样本收集逻辑（Table 2中 $PT_{nee**}$ 列）。GSCache默认使用三级缓存，点数分别为300K、150K、75K，缓存初始化点数 $N=300\mathrm{k}$，训练采用AdamW优化器配合HDR损失。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2507_19718/figures/009_Table_2.jpg]]
*Table 2: Frame timings of our method on different datasets captured from a screen-filling camera fly-through of 200 frames. We allowed for a 40-frame warm-up period to initialize the cache and show path tracing time (PT) for all four methods and splatting time (ST) , inference time (IT), and optimization time (OT) for our method and NRC [34]. IT includes a composition pass to back-propagate and compose cached radiance. The notation P $T _ { n e e * }$ denotes NEE with the addition of our path termination heuristic and P $T _ { \mathsf { n e e * * } }$ additionally adds path records and training sample collection for NRC [34]. All values were captured at C = 0 . 5 with N = 3 0 0 ${ \mathrm { k } }$ initial...

### 2. 主结果

**图像质量。** 在1 SPP极端低采样条件下，GSCache在所有数据集上一致且显著地超越基线方法（Fig. 6, 13, 14）：

- **Carp数据集**：GSCache的PSNR达到 **16.877**，相比NEE（14.657）提升 **+2.22 dB**，相比NRC（15.524）提升 **+1.353 dB**（Fig. 13）。
- **FullBody数据集**：GSCache的PSNR达到 **15.847**，相比NEE（12.454）提升 **+3.393 dB**，相比NRC（14.266）提升 **+1.581 dB**（Fig. 14）。

定性观察显示，GSCache在保持细节和边缘清晰度的同时，有效抑制了低SPP下的蒙特卡洛噪声，而NRC和NEE在相同条件下仍残留明显噪声结构。

**冷启动速度。** 在FullBody数据集上，GSCache从冷启动开始，不到16帧图像质量即超过无缓存的路径追踪渲染器（Fig. 7），证明了在线训练策略的快速自适应能力。

**运行时性能。** Table 2给出了各数据集的帧时间分解。在FullBody数据集上，GSCache总帧时间约 **89.55 ms**（路径追踪46.64 ms + 高斯泼溅11.42 ms + 训练31.49 ms），与NRC的88.49 ms（路径追踪47.66 ms + 推理13.91 ms + 训练26.92 ms）基本持平，额外开销仅约1 ms。关键优势在于：缓存开销恒定，总运行时间随SPP增加比基线方法增长更慢（Fig. 10），这意味着在高SPP或复杂场景下GSCache的相对效率优势将进一步扩大。

**内存占用。** Table 3给出缓存内存分解。三级缓存（300K + 150K + 75K高斯点）总内存约 **45.5 MB**，其中球谐系数（每个高斯48个系数）占主要部分。Table 4显示缓存初始化时间因数据集密度而异，平均在 **0.5–2.5 秒** 范围内。

### 3. 消融实验

**缓存初始化点数 $N$ 的影响。** Fig. 11显示，将初始化点数从10K增至300K时，FullBody数据集上PSNR从33.03显著提升至36.58；继续增至3M时增益趋于平滑（37.81）。这表明300K在质量与效率之间取得了良好平衡。

**正则化与优化器的作用。** Fig. 12的消融实验揭示了两个关键设计决策：

- **移除正则化（-REG）**：训练崩溃，SMAPE从0.040急剧恶化至0.089，图像出现严重伪影。这证明在基于噪声路径样本的在线训练中，AdamW的正则化对稳定优化不可或缺。
- **移除高斯初始尺寸限制（-SC）**：细节保留略有改善，但噪声稍有增加，总体影响较小。表明尺寸约束主要起正则化作用，防止过大的高斯核引入偏差。

### 4. 关键发现与讨论

GSCache的核心经验性发现是：**可以从蒙特卡洛渲染器的高噪声单样本路径中在线学习无偏辐射度表示**。即使训练目标本身是单样本噪声，梯度优化仍收敛到期望值，这解释了为何在1 SPP下能获得显著质量提升。该发现与HDR损失的设计密切相关——HDR归一化项 $k(\hat{y} + 0.01)^2$ 有效处理了辐射度值的高动态范围，防止高亮度区域主导梯度。

路径终止系数 $C$ 提供了偏差-方差权衡的用户可控旋钮：较小的 $C$ 使路径更早终止并依赖缓存（低方差、高偏差），较大的 $C$ 则保留更多路径采样（高方差、低偏差）。级联缓存采样概率修正 $\beta_{n-1}$ 是保持无偏性的关键——Fig. 4显示，忽略该修正会导致明显的系统性亮度偏差。

### 5. 局限性与失败模式

*注：原文未明确列出局限性章节，以下基于实验数据和消融结果推断，需人工确认。*

- **缓存初始化依赖体积密度分布**：Table 4显示初始化时间与数据集密度正相关，对于极高分辨率或极稀疏体积，点云采样策略可能需要调整。
- **三级缓存结构固定**：当前设计使用固定的三级缓存和预定义的子采样比率，对于路径长度分布差异极大的场景，自适应级别数可能更优。
- **训练与渲染耦合**：在线训练占用约35%的帧时间（Table 2中OT列），在需要极低延迟的应用中可能成为瓶颈——尽管作者指出缓存训练可与渲染异步执行以缓解此问题。

### 补充图表

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2507_19718/figures/014_Figure.jpg]]
*Figure: smape: 0.070 psnr:37.892*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2507_19718/figures/015_Figure.jpg]]
*Figure: smape: 0.041 psnr:38.693 smape: 0.089 psnr:32.369 smape: 0.041 psnr:39.285 smape:0.054 psnr:37.367*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2507_19718/figures/019_Figure.jpg]]
*Figure: Uniform 1SPP smape:0.418 psnr:12.372 NEE1SPP smape:0.256 psnr:14.657 NRC 1SPP GSCache 1SPP smape:0.220 psnr:15.524 smape: 0.169 psnr:16.877 Reference*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2507_19718/figures/020_Figure.jpg]]
*Figure: Uniform 1SPP*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2507_19718/figures/021_Figure.jpg]]
*Figure: Uniform 1SPP NEE1SPP NRC 1SPP GSCache 1SPP*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2507_19718/figures/022_Figure.jpg]]
*Figure: Uniform 1SPP*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2507_19718/figures/023_Figure.jpg]]
*Figure: Uniform 1SPP NEE1SPP NRC 1SPP*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2507_19718/figures/024_Figure.jpg]]
*Figure: Uniform 1SPP NEE1SPP NRC 1SPP*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2507_19718/figures/001_Figure_1.jpg]]
*Figure 1: Our path-space cache improves image quality at low sample counts at comparable compute cost. We compare against a path tracer (PT) using uniform sampling and a version implementing next-even-estimation (NEE). Cache rendering time is constant, yielding increasing returns as sample counts increase. The method is non-invasive and easy to integrate into existing rendering applications*

## 方法谱系与知识库定位

GSCache 处于**体积路径追踪实时辐射度缓存**这一细分方向，其核心设计决策——用多级路径空间3D高斯泼溅替代传统世界空间探针或单一MLP——在方法谱系中形成了明确的差异化定位。

### 与缓存方法的谱系关系

传统辐射度缓存方法将辐照度/辐射度存储为世界空间探针（如经典辐照度缓存 [13, 23, 44]），查询时通过空间插值获取近似值。这类方法在体积渲染中面临两个根本性困难：一是体数据缺乏明确表面，探针放置策略难以泛化；二是空间插值无法捕捉路径长度带来的辐射度差异。

**NRC**（Müller et al., ACM Trans. Graph. 2021）是当前最先进的神经网络辐射度缓存方法，将缓存建模为单一MLP，以世界空间坐标和方向为输入直接预测辐射度。GSCache 与 NRC 的关键分歧在于表示粒度：NRC 将整个路径空间的辐射度压缩到一个全局函数中，而 GSCache 按路径长度分层，每层独立维护一组3D高斯。这一设计使得 GSCache 能够通过可微光栅化实现恒定时间的缓存查询，而 NRC 需要逐像素评估神经网络。实验表明，在 FullBody 数据集 1 SPP 下，GSCache 的 PSNR 达到 15.847，领先 NRC 的 14.266（+1.581 dB），且总帧时间相当（约 89 ms vs 88 ms，见表2）。

### 与3D高斯泼溅（3DGS）的关系

GSCache 继承了 **3D Gaussian Splatting**（Kerbl et al., ACM Trans. Graph. 2023）的核心机制——可微光栅化和基于梯度的在线优化——但对其训练范式进行了根本性改造。常规 3DGS 训练依赖多视角干净图像作为监督信号，通过迭代优化高斯参数来重建静态场景。GSCache 将这一框架迁移到**在线、噪声、单样本**的路径追踪场景中，其训练目标是来自蒙特卡洛渲染器的无偏但高噪声的单样本路径辐射度。

这一迁移的关键理论支撑是：即使训练目标为单样本噪声，梯度优化仍收敛到期望值。消融实验（Fig.12）证实了训练稳定性的脆弱性——移除正则化（-REG）导致训练崩溃，SMAPE 从 0.040 急剧恶化至 0.089，表明 AdamW 优化器对噪声数据在线训练不可或缺。这一发现揭示了 3DGS 在实时渲染管线中作为动态缓存表示的潜力，也暴露了其训练过程对优化器配置的高度敏感性。

### 与路径追踪方法的谱系关系

GSCache 本质上是一种**偏差-方差权衡机制**，与无缓存路径追踪形成互补而非替代关系。基线方法包括：
- **Uniform Sampling (PT)**：无缓存的均匀采样体积路径追踪，在低 SPP 下噪声严重
- **Next-Event Estimation (NEE)**：带直接光照采样的进阶基线，通过重要性采样降低部分方差

GSCache 在路径追踪器中引入了一个可调节的“终止旋钮”——基于路径吞吐量亮度的概率终止系数 C。这一设计将传统路径追踪的固定终止策略（如俄罗斯轮盘赌）替换为自适应缓存查询：当路径吞吐量低于阈值时，路径终止并转向缓存，利用缓存的低偏差辐射度替代高方差采样。用户参数 C 控制终止激进程度，在偏差与方差之间提供连续权衡。

实验表明，在 1 SPP 的极端低样本条件下，GSCache 在 Carp 数据集上 PSNR 达到 16.877，大幅领先 NEE（14.657）和 NRC（15.524），且缓存开销恒定——总运行时间随 SPP 增加比基线增长更慢（Fig.10, Table 2）。

### 适用边界与局限

**适用场景**：GSCache 针对体积路径追踪的实时/交互式渲染场景设计，特别适用于医学可视化、科学模拟等需要快速预览体数据的应用。其恒定缓存开销特性使其在低 SPP 条件下优势最显著。

**已知局限**：
1. **动态场景适应性**：缓存在线训练需要若干帧收敛（FullBody 数据集冷启动后约 16 帧超过无缓存渲染器，见 Fig.7），在场景参数突变时可能出现短暂质量下降
2. **初始化敏感性**：缓存初始化点数 N 对质量有显著影响（消融实验表明 N 从 10k 增至 300k 时 PSNR 显著提升，但 N=3M 时增益已平滑，见 Fig.11），需要针对不同体数据规模调整
3. **训练稳定性**：对优化器配置（正则化、AdamW）高度敏感，移除正则化会导致训练崩溃（Fig.12）

**开放问题**：论文未深入探讨缓存在不同传递函数和光照条件下的泛化能力，也未评估在高动态场景（如快速旋转或缩放）下的缓存失效与重建代价。此外，多级缓存之间的信息共享机制是否可进一步优化以加速收敛，仍待探索。

## 原文 PDF

![[paperPDFs/IEEE_VIS_2025/Real_Time_Radiance_Caching_for_Volume_Path_Tracing_using_3D_Gaussian_Splatting.pdf]]
