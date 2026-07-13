---
title: "ResCa: Residual Caching for Diffusion Transformers Acceleration"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ResCa_Residual_Caching_for_Diffusion_Transformers_Acceleration.pdf
project_link: "https://fanghaipeng.github.io/ResCa"
code_link: null
aliases:
- ResCa
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用代理令牌的多阶残差作为方向性修正项，结合隐式ODE更新来模拟完整去噪过程，从而在保持自洽和更新方向的同时减少计算量。
primary_logic: 沿相似去噪轨迹的令牌，其低阶残差具有高度可复用性，可以通过代理令牌的真实去噪获取多阶残差，对驱动令牌进行置信度加权修正，实现高质量的模拟去噪。
claims:
- 基于轨迹的聚类比基于特征的聚类能更准确地找到相似残差，簇内残差L2距离更小。
- 低阶残差（1阶、2阶）比0阶特征具有更高的可复用性，其效果可通过历史残差关系预估。
- 在FLUX上实现5.5× GFLOPs加速同时保持接近无损的生成质量。
- FLUX.1-dev 上 Latency (s) ↓ = 7.17 (ResCa-IT N=6 O=2 K=16)
---

# ResCa: Residual Caching for Diffusion Transformers Acceleration

> [!tip] 核心洞察
> 沿相似去噪轨迹的令牌，其低阶残差具有高度可复用性，可以通过代理令牌的真实去噪获取多阶残差，对驱动令牌进行置信度加权修正，实现高质量的模拟去噪。

| 字段 | 内容 |
|------|------|
| 中文题名 | ResCa: 基于残差缓存的扩散Transformer加速方法 |
| 英文题名 | ResCa: Residual Caching for Diffusion Transformers Acceleration |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Fang_ResCa_Residual_Caching_for_Diffusion_Transformers_Acceleration_CVPR_2026_paper.html) · [Project](https://fanghaipeng.github.io/ResCa) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ResCa |
| Dataset | FLUX.1-dev, HunyuanVideo |

> [!tip] 效果简介
> - FLUX.1-dev 上，Latency (s) ↓ 7.17 (ResCa-IT N=6 O=2 K=16) vs 25.82 (原始50步) (3.60× 加速)；FLOPs (T) ↓ 749.5 (ResCa-IT N=6 O=2 K=16) vs 3719.5 (原始) (4.96× 减少)；Image Reward ↑ 0.9958 (ResCa-IE N=5 K=16) vs 0.9898 (原始) (+0.006)。
> - HunyuanVideo 上，VBench Score (%) ↑ 79.98 (ResCa-IE N=6 K=32) vs 80.20 (原始50步) (-0.22)；FLOPs Speedup 6.19× (ResCa-IT N=7 O=2 K=64) vs 1× (6.19× 加速)。

## 概要

扩散Transformer（Diffusion Transformer, DiT）在高质量图像与视频生成中取得了显著进展，但其巨大的计算开销严重制约了实际部署效率。现有的加速方法主要沿两条路径展开：**缓存方法**（如ToCa, Zou et al., ICLR）在相邻时间步间复用令牌特征，但会导致去噪方向“非更新”（non-updated），即复用特征无法反映当前时间步的真实去噪变化；**合并方法**（如ToMeSD, Bolya & Hoffman, CVPRW 2023）将相似令牌合并以减少计算量，却引入了“非自洽”（non-self）的去噪方向——合并后的令牌轨迹偏离了其原始去噪路径。这两类方法的根本矛盾在于：减少计算的同时，难以同时保持去噪轨迹的**自洽性**（self）与**更新性**（updated）。

**ResCa**（Residual Caching）从“代理去噪”视角重新审视这一问题。其核心洞察是：沿相似去噪轨迹的令牌，其**多阶残差**（multi-order residuals）具有高度可复用性——即令牌在不同时间步间特征变化的高阶差分在相似轨迹间表现出强一致性。基于此，ResCa提出了一种全新的加速范式：仅在每个轨迹簇中选取一个**代理令牌**（proxy token）进行真实去噪，利用其计算得到的多阶残差作为方向性修正项，通过**隐式ODE更新**（implicit ODE update）来模拟簇内其余“驱动令牌”（driven tokens）的去噪过程，从而在显著降低计算量的同时，维持去噪轨迹的自洽与更新。

在技术实现上，ResCa包含两个关键组件：**时序增强轨迹聚类**（Temporal-Enhanced Trajectory Clustering, TETC）与**代理驱动去噪模拟**（Proxy-Driven Denoising Simulation, PDDS）。TETC通过对历史去噪轨迹进行时序加权累积，将具有相似演化模式的令牌归入同一簇，相比传统基于单步特征相似性的聚类，能更准确地定位可复用残差的令牌群。PDDS则对代理令牌执行真实去噪，提取其多阶残差，并以置信度加权的方式将这些残差迁移至驱动令牌，最终通过隐式ODE步进（支持Euler、BDF2、Taylor等格式）完成驱动令牌的模拟更新。

实验结果表明，ResCa在多个主流DiT模型上实现了显著的加速效果。在**FLUX.1-dev**文本到图像生成任务上，ResCa实现了最高**5.5×**的GFLOPs加速（从3719.5T降至749.5T），同时保持接近无损的生成质量——Image Reward指标从0.9898提升至0.9958，CLIP Score仅微降0.224。在**HunyuanVideo**文本到视频生成任务上，ResCa实现了**6.19×**的FLOPs加速，VBench综合得分仅下降0.22%（从80.20%降至79.98%），定性结果中其他方法普遍存在的物体错位、细节缺失等问题在ResCa中得到有效抑制。消融实验进一步验证了轨迹聚类优于特征聚类、高阶残差（1阶、2阶）的可复用性显著高于0阶特征等关键设计选择。

**方法谱系与知识库定位**：ResCa属于扩散模型推理加速中的**令牌减少**（token reduction）路线，但其技术路径与现有方法形成本质差异。与**ToCa**的直接缓存复用不同，ResCa通过残差引导实现了去噪方向的更新；与**ToMeSD**的合并策略不同，ResCa保持了每个令牌的独立轨迹自洽性；与**TaylorSeer**（Liu et al., ICCV 2025）的泰勒外推预测不同，ResCa利用代理令牌的真实去噪信息进行校正，避免了纯预测带来的误差累积；与**ClusCa**（Zheng et al., ACM MM 2025）的缓存与空间相似性线性加权不同，ResCa通过多阶残差的置信度加权实现了更精细的方向性修正。ResCa为扩散模型加速提供了“以计算换精度”之外的新思路——通过挖掘轨迹间的结构相似性，以极小的代理计算代价换取全局的高质量模拟去噪。



扩散Transformer（Diffusion Transformer, DiT）已成为高质量文本到图像和文本到视频生成的主流架构，但其推理计算开销巨大——单张图像生成通常需要数十次模型前向传播，每次前向都需处理全部令牌（token），导致GFLOPs和延迟居高不下。以FLUX.1-dev为例，原始50步去噪的GFLOPs高达3719.5T，延迟达25.82秒（Table 1），严重制约了实际部署。

为降低计算成本，现有方法主要沿两条路径探索：**令牌缓存（token caching）** 和**令牌合并（token merging）**。缓存方法（如**ToCa**, Zou et al., ICLR）直接复用前一时间步的缓存特征，形成“非更新”（non-updated）的去噪方向；合并方法（如**ToMeSD**, Bolya & Hoffman, CVPRW 2023）将相似令牌合并后复用混合特征，形成“非自洽”（non-self）的去噪方向。如Figure 1所示，这两种策略均偏离了原始去噪轨迹，导致生成质量下降。此外，**TaylorSeer**（Liu et al., ICCV 2025）尝试用泰勒外推预测特征，但未解决方向自洽性问题；**ClusCa**（Zheng et al., ACM MM 2025）通过缓存与空间相似性的线性加权混合，仍受限于非自洽与非更新的根本矛盾。

核心瓶颈在于：**如何在减少令牌处理量的同时，保持去噪轨迹的自洽性（self）和更新性（updated）？** 现有方法只能满足其一，无法兼得。

本文的动机源于一个关键观察：**沿相似去噪轨迹的令牌，其多阶残差具有高度可复用性**。Figure 2的预备实验揭示了两层洞察：（1）基于历史去噪轨迹的聚类（trajectory-based clustering）比基于当前特征的聚类（feature-based clustering）能更准确地定位相似残差——轨迹聚类后的簇内一阶残差L2距离显著更小（Figure 2c）；（2）低阶残差（1阶、2阶）比0阶特征本身具有更高的可复用性，且历史残差距离越小，未来残差的复用价值越高（Figure 2d, 2e）。这提示我们：**可以用少量“代理令牌”的真实去噪残差，引导其他“驱动令牌”的模拟去噪**，从而在保持方向自洽和更新的同时大幅减少计算量。

基于此，本文提出**ResCa（Residual Caching）**，核心思路是：在每个轨迹聚类簇内仅对一个代理令牌执行真实去噪，利用其计算得到的多阶残差作为方向性修正项，通过隐式ODE更新驱动令牌，实现高质量的模拟去噪（Figure 1d）。该方法在FLUX上实现了高达5.5×的GFLOPs加速，同时保持接近无损的生成质量（Image Reward 0.9958 vs. 原始0.9898）。



## 核心方法与创新机理

ResCa 的核心创新在于将扩散Transformer加速问题从“特征复用/合并”范式重新定位为“代理去噪引导的隐式ODE模拟”范式。现有方法（如缓存类方法 **ToCa** (Zou et al., ICLR) 直接复用前一时间步特征，合并类方法 **ToMeSD** (Bolya & Hoffman, CVPRW 2023) 合并相似token）在减少计算量的同时，均破坏了去噪轨迹的**自洽性**或**更新方向性**——缓存方法导致去噪方向不更新，合并方法使去噪方向偏离自身轨迹（见 Figure 1）。ResCa 通过以下三个关键机制解决了这一矛盾：

### 1. 特征复用方式：从直接复用转向代理残差引导的模拟去噪

传统方法直接复用缓存特征或合并后的混合特征。ResCa 提出 **Proxy-Driven Denoising Simulation (PDDS)**：在每个簇中仅对**一个代理令牌**执行真实去噪，利用其计算得到的**多阶残差**作为方向性修正项，引导簇内其他“驱动令牌”的模拟去噪。具体而言，驱动令牌的更新结合了自身残差（保持自洽）与代理令牌残差（提供更新方向），通过置信度加权融合：
$$\hat{\mathcal{F}}^{(m)}(d_{t-1}) = (1 - \theta_t^{(m)}) \cdot \mathcal{F}^{(m)}(d_t) + \theta_t^{(m)} \cdot \mathcal{F}^{(m)}(p_{t-1})$$
其中置信度权重 $\theta_t^{(m)}$ 基于代理与驱动令牌第 $m$ 阶残差的余弦相似度计算。这一设计使得驱动令牌的去噪轨迹既保持与自身历史的一致性，又能从代理令牌获取有效的更新信息。

### 2. 聚类策略：从特征聚类转向时序增强轨迹聚类

**ToMeSD** 等方法基于当前时间步的特征相似性进行聚类，但 ResCa 的预备实验（Figure 2）揭示了一个关键发现：**低阶残差（1阶、2阶）比0阶特征本身具有更高的可复用性**，且沿相似去噪轨迹的令牌，其残差相似度更高。基于此，ResCa 设计了 **Temporal-Enhanced Trajectory Clustering (TETC)**，通过时序移动平均累积历史相似度矩阵：
$$\tilde{S}_t = \alpha_S \cdot S_t + (1 - \alpha_S) \cdot \tilde{S}_{t+1}$$
并基于累积相似度进行 K-medoids 聚类。实验验证（Figure 2(c)）表明，轨迹聚类使簇内残差的成对 L2 距离显著低于特征聚类，从而为后续的残差复用提供更准确的令牌分组。

### 3. 更新机制：从无更新/直接替换转向多阶隐式ODE步进

传统缓存方法对未处理令牌无更新或仅做直接特征替换。ResCa 引入**多阶残差校正 + 隐式ODE步进**机制，将估计的多阶残差通过隐式泰勒展开进行特征更新：
$$d_{t-1} = d_t + \sum_{m=1}^{M} \frac{1}{m!} \hat{\mathcal{F}}^{(m)}(d_{t-1})$$
该框架支持三种隐式ODE求解器（隐式Euler、隐式BDF2、隐式Taylor），对应 ResCa-IE、ResCa-IB、ResCa-IT 三个版本。其中 2 阶隐式 Taylor 方法（ResCa-IT）在 FLUX.1-dev 上以 16 个簇、6 个密集时间步的配置，实现了 **4.96× FLOPs 减少**（749.5T vs 3719.5T）和 **3.60× 延迟加速**，同时保持 Image Reward 0.9958 的近乎无损生成质量（Table 1）。

### 创新总结

ResCa 的方法论突破在于：**将扩散Transformer加速的核心矛盾从“计算-质量权衡”重新定义为“自洽性-更新性权衡”**。通过代理令牌的多阶残差引导与隐式ODE模拟，ResCa 首次在 token 减少框架下实现了同时满足自洽和更新的去噪轨迹，为扩散模型加速提供了新的理论视角和实践方案。这一范式在 FLUX 文本到图像生成和 HunyuanVideo 文本到视频生成任务上均验证了其有效性，最高实现 **6.19× FLOPs 加速**（Table 2）。



ResCa 的推理流程以**密集/稀疏时间步交替调度**为核心，将去噪过程划分为两个阶段，并通过**时序增强轨迹聚类（TETC）** 与**代理驱动去噪模拟（PDDS）** 两个关键模块协同完成高质量加速生成。

### 两阶段调度策略

整个去噪过程被划分为**密集计算时间步**与**稀疏计算时间步**。在密集时间步，所有令牌均经过完整的 DiT 前向去噪，并缓存其特征；在稀疏时间步，仅对极少数代理令牌执行真实去噪，其余驱动令牌则通过模拟方式更新。这种调度使得计算量从 O(N) 压缩至 O(K)，其中 K 为簇数量，远小于令牌总数 N。

### 时序增强轨迹聚类（TETC）

在密集时间步完成后，TETC 模块对所有令牌的历史去噪轨迹进行聚类，以发现具有相似残差演化方向的令牌组。其核心流程为：

1. **逐时间步余弦相似度计算**：对每个时间步 t，计算令牌特征矩阵 X_t 的成对余弦相似度矩阵 S_t：
   $$S_t = \frac{X_t X_t^T}{\|X_t\|_2 \|X_t^T\|_2}$$

2. **时序增强累积**：沿时间反向对相似度矩阵进行移动平均，赋予近期时间步更高权重，得到累积相似度矩阵 $\tilde{S}_t$：
   $$\tilde{S}_t = \alpha_S \cdot S_t + (1 - \alpha_S) \cdot \tilde{S}_{t+1}$$

3. **K-medoids 聚类**：基于累积相似度执行 K-medoids 聚类，簇中心强制为实际数据点，目标函数为：
   $$\min_{\{C_1, C_2, \ldots, C_K\}} \sum_{i=1}^N \sum_{k=1}^K \mathbb{I}(X_i \in C_k) \cdot (1 - \tilde{S}_t(X_i, C_k))$$

聚类完成后，从每个簇中随机选取一个令牌作为**代理令牌**，其余为驱动令牌。

### 代理驱动去噪模拟（PDDS）

在稀疏时间步，PDDS 模块以代理令牌的真实去噪结果为锚点，引导驱动令牌的模拟更新。该模块包含三个步骤（参见 Figure 3 橙色部分）：

![[assets/figures/papers/paper_list_l923_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_ResCa_Residual_Ca/figures/003_Figure_3.jpg]]
*Figure 3: Overview. grey: In the dense timestep, all tokens are processed to cache their features, followed by TETC to group tokens. In the sparse timestep, one proxy token from each group is selected for denoising, which then uses PDDS to guide the denoising of other tokens. blue: Temporal-Enhanced Trajectory Clustering (TETC): perform clustering using a similarity metric computed by token trajectories. orange: Proxy-driven Denoising Simulation (PDDS): use the driven token’s residuals as the main direction; the proxy token’s residuals provide directional corrections to estimate the future direction, and subsequently simulate the denoising process using an implicit ODE*

1. **代理令牌真实去噪**：对代理令牌 p 执行完整的 DiT 去噪步，获取其在各层的真实特征变化。

2. **多阶残差估计**：计算代理令牌的多阶残差 $\mathcal{F}^{(m)}(p_t)$，并通过置信度加权结合驱动令牌自身历史残差，估计驱动令牌在下一时间步的残差 $\hat{\mathcal{F}}^{(m)}(d_{t-1})$。置信度由代理与驱动令牌在第 m 阶残差上的余弦相似度决定：
   $$\theta_t^{(m)} = \max\left(0, \cos\left(\mathcal{F}^{(m)}(p_t), \mathcal{F}^{(m)}(d_t)\right)\right)$$
   $$\hat{\mathcal{F}}^{(m)}(d_{t-1}) = (1 - \theta_t^{(m)}) \cdot \mathcal{F}^{(m)}(d_t) + \theta_t^{(m)} \cdot \mathcal{F}^{(m)}(p_{t-1})$$

3. **隐式 ODE 更新**：利用估计的多阶残差，通过隐式数值方法更新驱动令牌特征。ResCa 提供三种变体：
   - **ResCa-IE**：隐式 Euler 方法（1 阶）
   - **ResCa-IB**：隐式 BDF2 方法（1 阶）
   - **ResCa-IT**：隐式 Taylor 方法（可配置阶数 O），其通用更新公式为：
     $$d_{t-1} = d_t + \sum_{m=1}^{M} \frac{1}{m!} \hat{\mathcal{F}}^{(m)}(d_{t-1})$$

### 数据流总结

整个框架的数据流可概括为：密集时间步缓存所有令牌特征 → TETC 基于历史轨迹聚类 → 稀疏时间步选取代理令牌 → 代理令牌真实去噪产生多阶残差 → PDDS 利用残差引导驱动令牌隐式更新。这一设计使得驱动令牌的更新方向既保持了与自身历史轨迹的**自洽性**，又通过代理残差获得了**方向性修正**，从而在显著降低计算量的同时维持生成质量。



ResCa 将扩散Transformer的去噪过程划分为**密集时间步（Dense Timesteps）** 与**稀疏时间步（Sparse Timesteps）** 两个阶段，并围绕“轨迹聚类”与“代理引导模拟”两个核心机制构建加速框架。

### 时序增强轨迹聚类（TETC）

在密集时间步，所有令牌均被完整处理，其各层特征被缓存。随后，TETC 基于令牌在整个历史去噪轨迹上的相似性进行聚类，而非仅依赖当前时间步的特征相似性。这一设计的动机在于：沿相似去噪轨迹的令牌，其残差具有高度可复用性（见 Figure 2）。

![[assets/figures/papers/paper_list_l923_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_ResCa_Residual_Ca/figures/002_Figure_2.jpg]]
*Figure 2: Preliminaries. Upper: Where to find the similar residuals? Illustration of (a) feature- and (b) trajectory-based clusters, where the trajectory-based clusters groups the blue and red trajectories more accurately. (c) Comparison of the two methods showing that trajectorybased clusters have lower pairwise distance of residuals within each cluster. Lower: How to use the similar residuals? (d) Intra-cluster L2 distance of multi-order residuals, indicating that 1st-, 2nd-, and 3rd-order residuals are more reusable than 0th-order ones. (e) Intra-cluster residual relationships across timesteps, showing that smaller historical residual distance implies higher reuse value for future residuals*

具体而言，对每个时间步 $t$，计算令牌间的成对余弦相似度矩阵：

$$S_t = \frac{X_t X_t^T}{\|X_t\|_2 \|X_t^T\|_2} \tag{1}$$

为赋予近期时间步更高权重，对相似度矩阵进行时序移动平均，得到时序增强累积相似度：

$$\tilde{S}_t = \alpha_S \cdot S_t + (1 - \alpha_S) \cdot \tilde{S}_{t+1} \tag{2}$$

其中 $\alpha_S$ 为平滑系数。基于 $\tilde{S}_t$，采用 K-medoids 算法进行聚类，其目标函数为：

$$\min_{\{C_1, C_2, \ldots, C_K\}} \sum_{i=1}^N \sum_{k=1}^K \mathbb{I}(X_i \in C_k) \cdot (1 - \tilde{S}_t(X_i, C_k)) \tag{3}$$

K-medoids 约束每个簇中心必须为实际数据点，这为后续代理令牌的选择提供了便利——从每个簇中随机选取一个令牌作为**代理令牌（Proxy Token）**。

### 代理驱动去噪模拟（PDDS）

在稀疏时间步，仅对代理令牌执行真实去噪，其余**驱动令牌（Driven Tokens）** 的去噪则通过 PDDS 进行模拟。PDDS 包含三个步骤：

**步骤一：代理令牌去噪。** 对第 $k$ 个簇的代理令牌 $p_{k,t+1}^l$，执行反向去噪步：

$$p_{k,t}^l = \mathcal{F}(p_{k,t+1}^l, t+1)$$

**步骤二：多阶残差估计。** 定义代理令牌的 $m$ 阶残差为递归有限差分：

$$\mathcal{F}^{(m)}(p_t) = \mathcal{F}^{(m-1)}(p_t) - \mathcal{F}^{(m-1)}(p_{t+1}), \quad m \ge 1 \tag{6}$$

其中零阶项 $\mathcal{F}^{(0)}(p_t) = p_t$ 即为特征本身。驱动令牌的残差则通过置信度加权结合自身历史残差与代理令牌残差来估计。置信度权重基于代理与驱动令牌在第 $m$ 阶残差上的余弦相似度：

$$\theta_t^{(m)} = \max\left(0, \cos\left(\mathcal{F}^{(m)}(p_t), \mathcal{F}^{(m)}(d_t)\right)\right) \tag{7}$$

驱动令牌在 $t-1$ 时刻的残差估计为：

$$\hat{\mathcal{F}}^{(m)}(d_{t-1}) = (1 - \theta_t^{(m)}) \cdot \mathcal{F}^{(m)}(d_t) + \theta_t^{(m)} \cdot \mathcal{F}^{(m)}(p_{t-1}) \tag{8}$$

**步骤三：隐式ODE更新。** 利用估计的多阶残差，通过隐式泰勒方法更新驱动令牌特征：

$$d_{t-1} = d_t + \sum_{m=1}^{M} \frac{1}{m!} \hat{\mathcal{F}}^{(m)}(d_{t-1}) \tag{9}$$

ResCa 框架提供了三种隐式ODE变体：**ResCa-IE**（隐式Euler，$M=1$）、**ResCa-IB**（隐式BDF2，$M=1$）和 **ResCa-IT**（隐式Taylor，$M \ge 2$）。其中 BDF2 风格的隐式更新公式为：

$$d_{t-1} = \frac{4}{3} d_t - \frac{1}{3} d_{t+1} + \frac{2}{3} \hat{\mathcal{F}}^{(1)}(d_{t-1})$$

### 核心机制总结

ResCa 的关键创新在于用**代理令牌的多阶残差作为方向性修正项**，替代了传统缓存方法中直接复用过期特征或合并方法中破坏自洽性的做法。置信度加权机制确保了对齐度高的代理残差获得更大权重，而对齐度低时则退化为依赖驱动令牌自身的历史残差，从而在加速与质量之间取得平衡。

### 补充图表

![[assets/figures/papers/paper_list_l923_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_ResCa_Residual_Ca/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of denoising trajectories. Solid and dashed line denotes the realized and the target trajectories. (a) Original trajectory. (b) Caching: reuse the previous step*



## 实验与关键发现

### 主实验结果

#### 文本到图像生成（FLUX.1-dev）

ResCa 在 FLUX.1-dev 上进行了系统评估，对比方法包括 ToCa、ToMeSD、TaylorSeer 和 ClusCa。Table 1 给出了以 Image Reward 和 CLIP Score 为指标的量化结果。ResCa 框架包含三个变体：**ResCa-IE**（隐式 Euler）、**ResCa-IB**（隐式 BDF2）和 **ResCa-IT**（隐式 Taylor），其中 IE 和 IB 的阶数固定为 1，IT 支持多阶残差。

![[assets/figures/papers/paper_list_l923_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_ResCa_Residual_Ca/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison in text-to-image generation for FLUX on Image Reward. The best results are highlighted in bold*

在加速效率方面，ResCa-IT（N=6, O=2, K=16）实现了 **3.60× 延迟加速**和 **4.96× FLOPs 减少**（749.5 T vs 原始 3719.5 T），同时 Image Reward 达到 0.9915，CLIP Score 为 19.604。更激进的配置 ResCa-IT（N=8, O=2, K=32）进一步将加速比提升至 **3.95×**，FLOPs 降至 604.6 T（6.15× 减少），Image Reward 仍保持 0.9840。在质量优先配置下，ResCa-IE（N=5, K=16）取得了 **0.9958 的 Image Reward**，甚至略超原始模型的 0.9898，CLIP Score 为 19.537（原始 19.761），仅下降 0.224。

定性对比（Figure 4）显示，ResCa 在 5.51× 加速下仍能生成更精细的纹理细节，如水壶反射、机器人肢体和人类大脑结构，而其他方法在这些区域出现模糊或失真。

![[assets/figures/papers/paper_list_l923_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_ResCa_Residual_Ca/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison in text-to-image generation on FLUX. ResCa show stronger texture details in the kettle reflection, robotic limbs, and human brain, with a 5.51× acceleration*

#### 文本到视频生成（HunyuanVideo）

在 HunyuanVideo 上以 VBench 为指标进行评估（Table 2）。ResCa-IE（N=6, K=32）取得 **79.98% 的 VBench 分数**，与原始 50 步的 80.20% 仅差 0.22 个百分点。ResCa-IT（N=7, O=2, K=64）实现了 **6.19× FLOPs 加速**，VBench 分数为 79.72%，在相同加速比下超越 ClusCa 约 0.18%。定性结果（Figure 5）表明，ResCa 生成的视频语义对齐度高、物体完整性好，而对比方法出现瓶盖错位、水花细节丢失、鼓槌物体缺失等问题。

![[assets/figures/papers/paper_list_l923_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_ResCa_Residual_Ca/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison in text-to-video generation for HunyuanVideo on VBench. Best results are highlighted in bold*

![[assets/figures/papers/paper_list_l923_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_ResCa_Residual_Ca/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison in text-to-video generation on HunyuanVideo. ResCa generates high-quality, semantically aligned videos, while others suffer from issues such as misplaced bottle caps, missing water splash details, and missing drumstick objects*

#### 类别条件图像生成（DiT-XL/2 on ImageNet）

在 DiT-XL/2 上的类别条件生成任务中（Table 3），ResCa-IE 在 N=5 时取得 **2.59 的 FID**，优于 ToCa（2.77）、ToMeSD（3.15）、TaylorSeer（2.82）和 ClusCa（2.67），同时实现约 2.5× 加速。

![[assets/figures/papers/paper_list_l923_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_ResCa_Residual_Ca/figures/009_Table_3.jpg]]
*Table 3: Quantitative comparison in class-to-image generation for DiT-XL/2 on ImageNet. Best results are highlighted in blod*

### 消融实验

#### 簇数量 K 的影响

Figure 6 展示了簇数量 K 对 FID 和加速比的影响。随着 K 从 8 增加到 64，FID 持续降低（质量提升），这是因为更多簇意味着代理令牌能更精确地代表簇内驱动令牌的去噪行为。但加速比随之略微下降，原因在于代理令牌数量增加导致真实去噪的计算开销上升。这一权衡验证了 TETC 聚类在质量-效率平衡中的关键作用。

![[assets/figures/papers/paper_list_l923_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_ResCa_Residual_Ca/figures/008_Figure_6.jpg]]
*Figure 6: Ablation on the number of clusters*

#### 多阶残差的贡献

Table 4 消融了残差阶数对生成质量的影响。仅使用 0 阶（特征本身）时 FID 较高；引入 1 阶残差后 FID 大幅降低；2 阶残差相比 1 阶进一步提升。这直接支持了论文的核心洞察：**低阶残差（1 阶、2 阶）比 0 阶特征具有更高的可复用性**，且高阶残差能提供更精确的去噪方向修正。

#### 聚类策略对比

Figure 7 对比了基于特征的聚类与基于轨迹的聚类（TETC）的生成效果。TETC 在视觉质量和语义一致性上均优于特征聚类，验证了 **沿去噪轨迹的时序增强相似度** 能更准确地找到具有相似残差行为的令牌组。这一结果与 Figure 2(c) 的预备实验一致：轨迹聚类使簇内一阶残差的成对 L2 距离更小。

![[assets/figures/papers/paper_list_l923_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_ResCa_Residual_Ca/figures/010_Figure_7.jpg]]
*Figure 7: Visual comparisons of clustering methods*

### 关键图表结论

- **Table 1**：ResCa 在 FLUX 上以 5.5× GFLOPs 加速实现接近无损的生成质量，Image Reward 在部分配置下甚至超越原始模型。
- **Table 2**：ResCa 在 HunyuanVideo 上以 6.19× 加速保持 VBench 分数仅下降 0.48%，显著优于同类加速方法。
- **Figure 6**：簇数量 K 是质量-效率的核心调节旋钮，K 增大提升质量但降低加速比。
- **Table 4**：多阶残差是 ResCa 性能的关键来源，2 阶残差相比 0 阶带来显著质量增益。
- **Figure 7**：轨迹聚类（TETC）在生成质量上一致优于特征聚类，是方法有效性的基础组件。



## 定位与知识库关联

### 1. 加速范式的演进与ResCa的定位

扩散Transformer（DiT）的推理加速研究，核心矛盾在于**计算开销与生成轨迹保真度之间的权衡**。现有方法可归纳为三条技术路线，ResCa在每条路线上都做出了关键修正：

**（1）缓存范式（Caching）**：以 **ToCa**（Zou et al., ICLR）为代表，在相邻时间步之间直接复用token特征，跳过部分去噪计算。其根本缺陷在于：缓存特征来自前一时间步，导致当前步的“去噪方向”是**非更新的**（non-updated）——即方向向量基于过时的特征计算，与当前步应有的真实方向存在偏差（见Figure 1b）。

**（2）合并范式（Merging）**：以 **ToMeSD**（Bolya & Hoffman, CVPRW 2023）为代表，将相似token合并为少量代表token进行去噪，再将结果广播回原始token。其根本缺陷在于：合并后的token去噪轨迹是**非自洽的**（non-self）——被合并的token并未经历属于自己的去噪过程，而是“借用”了其他token的轨迹（见Figure 1c）。

**（3）动态预测范式（Prediction）**：以 **TaylorSeer**（Liu et al., ICCV 2025）为代表，利用泰勒展开外推未来时间步的特征。这类方法虽然考虑了轨迹的连续性，但纯外推缺乏对去噪方向的结构性约束，在高阶近似时容易累积误差。

**ClusCa**（Zheng et al., ACM MM 2025）尝试将缓存与合并结合，通过空间相似性进行线性加权，但本质上仍属于上述范式的混合，未能从根本上解决“非自洽”与“非更新”的矛盾。

ResCa的突破在于引入**代理去噪视角**（proxy denoising perspective），将问题重新表述为：*如何利用簇内少量token的真实去噪信息，为其余token构造一个既自洽又更新的模拟去噪轨迹？* 这一视角将上述三条路线的优势统一在一个理论框架下——缓存提供基础特征、聚类提供结构先验、多阶残差提供方向性修正。

### 2. 核心技术差异：从“复用特征”到“复用残差方向”

ResCa与所有基线方法最本质的区别，在于**复用对象**的转变：

| 方法 | 复用对象 | 更新机制 | 自洽性 |
|------|----------|----------|--------|
| ToCa | 缓存特征（0阶） | 无更新 | ✓ |
| ToMeSD | 合并后特征（0阶） | 无更新 | ✗ |
| TaylorSeer | 外推特征（多阶泰勒） | 纯预测 | ✓（近似） |
| **ResCa** | **多阶残差（1阶/2阶）** | **隐式ODE步进** | **✓（精确）** |

这一转变的深层依据来自论文的预备实验发现（Figure 2d-e）：沿相似去噪轨迹的token，其**低阶残差（1阶、2阶）在簇内的L2距离显著小于0阶特征本身**。这意味着残差比原始特征具有更高的跨token可复用性——这正是ResCa选择“复用残差”而非“复用特征”的经验基础。

### 3. 方法谱系中的知识贡献

ResCa对扩散模型加速领域的知识贡献可分解为三个层面：

**（1）聚类策略的时序化**：传统方法（如ToMeSD）基于当前时间步的特征相似性进行聚类，忽略了去噪过程的动态演化特性。ResCa提出的**时序增强轨迹聚类（TETC）**通过累积历史相似度矩阵（Eq. 2: $\tilde{S}_t = \alpha_S \cdot S_t + (1 - \alpha_S) \cdot \tilde{S}_{t+1}$），使聚类结果反映整个去噪轨迹的相似性，而非单一快照。Figure 2c的实验证据表明，轨迹聚类使簇内一阶残差的成对L2距离显著低于特征聚类。

**（2）残差引导的模拟去噪**：ResCa的**代理驱动去噪模拟（PDDS）**将代理token的多阶残差作为“方向性修正项”，通过置信度加权机制（Eq. 7: $\theta_t^{(m)} = \max(0, \cos(\mathcal{F}^{(m)}(p_t), \mathcal{F}^{(m)}(d_t)))$）融合驱动token的自身残差与代理残差，再通过隐式ODE方法（Euler/BDF2/Taylor）完成特征更新。这一设计使驱动token的去噪方向既保持了自洽性（基于自身历史），又获得了更新（引入代理信息）。

**（3）密集-稀疏时间步调度**：ResCa将去噪过程划分为密集计算步（所有token完整去噪并缓存特征）和稀疏计算步（仅代理token去噪，其余模拟）。这种调度策略在计算开销与轨迹精度之间建立了可控的权衡——密集步的频率和稀疏步的压缩比可通过参数 $N$（密集步数）和 $K$（簇数）灵活调节。

### 4. 适用边界与局限

基于论文的实验设置和方法设计，ResCa的适用边界可归纳如下：

**已验证的适用场景**：
- 文本到图像生成（FLUX.1-dev，DiT架构）
- 文本到视频生成（HunyuanVideo，3D VAE + DiT架构）
- 类别条件图像生成（DiT-XL/2 on ImageNet）
- 在5-6× FLOPs加速比下保持接近无损的生成质量

**潜在局限与开放问题**：

1. **聚类开销**：TETC涉及历史相似度矩阵的累积与K-medoids聚类，在高分辨率或超长序列场景下，聚类本身的计算开销可能侵蚀加速收益。论文未报告聚类时间占总延迟的比例，这一指标对于评估方法的实际效率边界至关重要。

2. **高压缩比下的质量退化**：Figure 6的消融实验显示，随着簇数 $K$ 减少（即压缩比增大），FID持续上升。这意味着ResCa的加速上限受到簇内残差相似性的约束——当簇过大时，代理token的残差无法充分代表簇内所有token的去噪方向。

3. **密集-稀疏调度的手工设计**：当前 $N$ 和 $K$ 的配置依赖人工设定（如FLUX上 $N=6, K=16$），缺乏自适应的动态调度机制。能否学习一个调度策略，根据输入prompt的复杂度或去噪阶段的特性自动调整密集步频率，是一个值得探索的方向。

4. **对非DiT架构的泛化性**：ResCa的核心假设——沿相似轨迹的token具有可复用的低阶残差——是否在UNet架构或其他生成范式（如自回归模型）中成立，论文未提供证据。这一假设的普适性需要进一步验证。

5. **与蒸馏/量化方法的兼容性**：ResCa属于推理时的token减少方法，与模型蒸馏、权重量化等正交加速技术是否可以叠加使用，叠加后的累积质量损失如何，论文未涉及。



## 原文 PDF

![[paperPDFs/CVPR_2026/ResCa_Residual_Caching_for_Diffusion_Transformers_Acceleration.pdf]]
