---
title: "Beyond Fixed Formulas: Data-Driven Linear Predictor for Efficient Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Beyond_Fixed_Formulas_Data_Driven_Linear_Predictor_for_Efficient_Diffusion_Models.pdf
project_link: null
code_link: "https://github.com/Aredstone/L2P-Cache"
aliases:
- L2PLLP
- BFFDDLPEDM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 线性组合系数的可学习性——将固定公式系数替换为数据驱动的可学习权重W，使预测器能针对不同模型与去噪步长自适应学习最优线性组合。
primary_logic: 扩散Transformer在大部分去噪步骤中，当前层特征可以被历史特征以超过0.95的投影保真度线性表示；因此一个极简的可学习线性预测器即可逼近最优预测，无需复杂非线性建模。
claims:
- 现有预测型缓存方法的数学本质即对历史特征的固定系数线性组合。
- 对于大多数去噪步骤，当前特征可被历史特征以投影保真度超过0.95线性重建。
- L2P仅用50张图像训练约20秒，在极端加速比下显著超越所有基线方法。
- FLUX.1-dev 上 PSNR = 31.459 (Ours N=5)
---

# Beyond Fixed Formulas: Data-Driven Linear Predictor for Efficient Diffusion Models

> [!tip] 核心洞察
> 扩散Transformer在大部分去噪步骤中，当前层特征可以被历史特征以超过0.95的投影保真度线性表示；因此一个极简的可学习线性预测器即可逼近最优预测，无需复杂非线性建模。

| 字段 | 内容 |
|------|------|
| 中文题名 | 超越固定公式：面向高效扩散模型的数据驱动线性预测器 |
| 英文题名 | Beyond Fixed Formulas: Data-Driven Linear Predictor for Efficient Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.26365) · [Code](https://github.com/Aredstone/L2P-Cache) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | L^2 P (Learnable Linear Predictor) |
| Dataset | FLUX.1-dev, Qwen Image, HunyuanVideo |

> [!tip] 效果简介
> - FLUX.1-dev 上，PSNR 31.459 (Ours N=5) vs 29.328 (TaylorSeer O=2, N=5) (+2.131)。
> - Qwen Image 上，PSNR 30.62 (Ours N=7) vs 28.58 (TaylorSeer N=6) (+2.04)。
> - HunyuanVideo 上，PSNR 21.10 (Ours N=7) vs 18.25 (TeaCache l=0.4) (+2.85)。

## 概要

扩散Transformer（DiT）已成为高保真图像与视频生成的主流架构，但其多步迭代去噪特性导致极高的计算成本。现有的加速方法中，**预测型特征缓存**（如TaylorSeer、FoCa）通过跳过部分DiT前向计算来降低开销，然而这些方法的本质均可统一为一种**固定系数的线性组合**——系数由泰勒展开或BDF2等数值公式先验决定，缺乏对具体模型和去噪步长的适应性，在高加速比下质量退化严重。

本文的核心发现是：在扩散去噪轨迹的大部分步骤中，当前层的特征可以被历史特征以**超过0.95的投影保真度**线性重建（Figure 1）。这意味着特征演化高度近似于在一个低维线性子空间中行进，一个极简的可学习线性预测器即可逼近最优预测，无需复杂的非线性建模。

基于此洞察，本文提出 **L²P（Learnable Linear Predictor）**，将固定公式系数替换为**数据驱动的可学习权重矩阵 W**。该方法仅需约50张图像、在单块GPU上训练约20秒，即可学习到针对特定模型和步长间隔的最优线性组合。推理时，L²P利用缓存的最后一层历史特征直接预测被跳过步骤的特征，从而绕过昂贵的DiT前向传播。

在FLUX.1-dev上，L²P实现了**4.55倍FLOPs降低和4.15倍延迟加速**，PSNR达到31.459，较TaylorSeer（29.328）提升+2.131 dB；在Qwen Image上加速比可达7.18倍，PSNR提升+2.04 dB；在HunyuanVideo视频生成上PSNR提升+2.85 dB。消融实验进一步表明，该方法具有极高的数据效率（仅5个样本即可超越基线）和语义无关性（使用无意义图像训练仍保持高性能），证明其学习到的是**特征演化的内在动态模式**而非数据语义。

扩散Transformer（DiT）已成为文本到图像与视频生成的主流架构，但其推理速度受限于多步去噪过程中大量Transformer模块的重复计算。为缓解这一瓶颈，**特征缓存（Feature Caching）** 方法被提出，其核心思路是：在部分去噪步骤跳过昂贵的DiT前向计算，转而利用已缓存的历史特征来近似当前步骤的特征表示。

现有特征缓存方法可分为两类范式：

- **重用型缓存（Reuse-based Caching）**：以固定间隔 $N$ 选取锚点步 $t$，计算并缓存该步所有层的特征 $\mathcal{C}(x_t^l)$；在随后的 $N-1$ 个跳过步中，直接将锚点特征赋值给当前步，即 $\hat{\mathcal{F}}(x_{t+k}^l) := \mathcal{C}(x_t^l)$。此类方法实现简单，但完全忽略了特征在去噪过程中的时序演化，在较大加速比下保真度急剧下降。
- **预测型缓存（Forecasting-based Caching）**：不直接复用锚点特征，而是利用缓存的历史时序统计量来预测跳过步的特征。代表性工作包括 **TaylorSeer**（Liu et al., ICCV 2025）和 **FoCa**（Zheng et al., AAAI 2026），它们分别基于截断泰勒展开和BDF2预测-校正机制来估计未来特征。

### 现有方法的统一形式与本质局限

本文揭示了一个关键洞察：**现有预测型缓存方法在数学上均可统一为历史特征的固定系数线性组合形式**。具体而言，TaylorSeer利用锚点特征及其高阶有限差分进行预测，而有限差分本身可展开为历史特征的线性组合：

$$\Delta^i \mathcal{F}(x_t^l) = \sum_{j=0}^{i} (-1)^j \binom{i}{j} \mathcal{F}(x_{t-jN}^l)$$

将有限差分代入泰勒展开后，整个预测过程等价于：

$$\hat{\mathcal{F}}(x_{t+k}^l) = \sum_{j=0}^{m} \alpha_j \cdot \mathcal{F}(x_{t-jN}^l)$$

其中系数 $\alpha_j$ 完全由展开阶数 $m$ 和步长 $N$ 等先验公式决定，与具体模型和数据无关。FoCa的BDF2预测器同样可归约为该形式。这种**固定公式先验**的根本缺陷在于：系数无法针对不同DiT架构、不同去噪阶段、不同步长间隔进行自适应调整，导致在高加速比下预测误差累积，生成质量严重退化。

### 线性表示上界：动机的实证基础

为探索预测型缓存的性能上限，本文对DiT特征轨迹进行了深入分析。核心问题是：**当前步特征能否被历史特征线性表示？** 作者将当前步特征 $\mathcal{F}(x_t)$ 正交投影到历史特征张成的子空间 $V_t = \text{span}(\mathcal{F}(x_0), \dots, \mathcal{F}(x_{t-1}))$ 上，得到最优线性近似 $\mathcal{F}^*(x_t)$，并计算投影保真度：

$$\text{Projection Fidelity} = 1 - \frac{\|\mathcal{F}(x_t) - \mathcal{F}^*(x_t)\|_2}{\|\mathcal{F}(x_t)\|_2}$$

如 Figure 1 所示，在50步扩散轨迹中，**大多数内部去噪步骤的投影保真度超过0.95**，即相对残差小于5%。这一发现表明：DiT特征在去噪过程中具有极强的线性可预测性，历史特征的线性组合已足以逼近最优预测，无需复杂的非线性建模。

### 本文动机

基于上述分析，本文提出核心主张：**将预测系数的选择从“固定公式先验”转变为“数据驱动学习”**。具体而言，设计一个可学习的线性预测器 **L²P（Learnable Linear Predictor）**，用参数化的权重矩阵 $W$ 替代手工设计的固定系数 $\alpha_j$，通过最小化预测特征与真实特征之间的MSE损失来端到端学习最优线性组合。该方法仅需约50张图像和20秒训练时间，即可在多个DiT模型上实现显著的加速与质量提升。

## 核心方法与创新机理

### 问题瓶颈：固定公式的线性组合天花板

现有预测型特征缓存方法——典型代表为 **TaylorSeer**（Liu et al., ICCV 2025）和 **FoCa**（Zheng et al., AAAI 2026）——虽然在中等加速比下表现良好，但其数学本质存在一个根本性约束：**它们对历史特征的预测均可统一为固定系数的线性组合**。

具体而言，TaylorSeer 基于截断泰勒展开，利用锚点特征及其时间有限差分进行预测；FoCa 则采用 BDF2 预测-校正机制。然而，无论泰勒展开的阶数取多少，其预测过程在数学上等价于对有限个历史特征施加一组由展开阶数和步长唯一确定的固定标量系数 $\alpha_j$：

$$\hat{\mathcal{F}}(x_{t+k}^{l}) = \sum_{j=0}^{m} \alpha_j \cdot \mathcal{F}(x_{t-jN}^{l})$$

这组系数 $\alpha_j$ 完全由公式先验决定，与具体模型架构、去噪时间步、数据分布均无关。在高加速比（大步长间隔）场景下，这种缺乏适应性的固定组合导致预测误差急剧累积，造成严重的生成质量退化——这正是现有方法的**真实瓶颈**所在。

### 核心洞察：线性表示的高保真上界

本文的关键发现是：扩散 Transformer（DiT）在去噪过程中，**当前时间步的特征可以被历史特征以极高的保真度线性表示**。作者沿 50 步扩散轨迹，将每一步的当前特征正交投影到由所有历史特征张成的子空间上，并计算投影保真度（定义为 $1 - \frac{\|\mathcal{F}(x_t) - \mathcal{F}^*(x_t)\|_2}{\|\mathcal{F}(x_t)\|_2}$）：

$$\mathcal{F}^*(\boldsymbol{x}_t) = \mathrm{Proj}_{V_t}(\mathcal{F}(\boldsymbol{x}_t)), \quad V_t = \mathrm{span}(\mathcal{F}(\boldsymbol{x}_0), \dots, \mathcal{F}(\boldsymbol{x}_{t-1}))$$

结果如图 1 所示：**绝大多数内部去噪步骤的投影保真度超过 0.95**，即相对残差不足 5%。这一发现揭示了一个重要事实：特征演化轨迹本身具有强线性结构，理论上一个最优的线性预测器即可逼近极低的预测误差，无需引入复杂的非线性建模。

### 关键改变：从固定系数到可学习权重

基于上述洞察，L²P 的核心创新在于**将预测器的因果调节旋钮从“公式先验”切换为“数据驱动”**——具体体现为两个 changed slots：

**Slot 1：预测系数——从固定标量 $\alpha_j$ 到可学习权重矩阵 $W_{t,j}$**

L²P 彻底摒弃了由泰勒展开或 BDF2 等数值公式导出的固定系数，代之以通过数据学习得到的逐时间步权重矩阵 $W \in \mathbb{R}^{49 \times 49}$。预测公式变为：

$$\hat{\mathcal{F}}(x_t) = \sum_{j=0}^{t-1} W_{t,j} \cdot \mathcal{F}(x_j)$$

矩阵的第 $t$ 行包含预测第 $t$ 步特征所需的所有历史特征线性组合权重。训练时，权重初始化为朴素特征缓存的等价形式（$W_{t,t-1}=1$，其余为 0），随后通过最小化预测特征与真实特征的 MSE 损失进行优化。这一设计使预测器能够**针对不同模型架构与去噪步长自适应学习最优线性组合**，从根本上突破了固定公式的表达能力上限。

**Slot 2：预测特征层级——从多层到仅最后一层**

与 TaylorSeer 等利用各层特征进行预测的方法不同，L²P **仅使用 DiT 的最后一层特征进行线性预测**。这一简化大幅降低了缓存内存开销和预测计算量，同时实验表明最后一层特征已包含足够的信息用于高保真线性重建。

### 创新性验证：线性设计的充分性

一个自然的问题是：是否需要更强的非线性建模？作者在补充实验中系统尝试了空间变化系数、二次项、注意力机制等非线性增强方案，**均未带来显著的性能提升**。这一消融结果反向验证了核心洞察的正确性：在 DiT 特征轨迹的强线性结构下，一个极简的可学习线性预测器已足以逼近最优预测，复杂非线性设计是冗余的。

### 方法谱系与知识库定位

L²P 属于**预测型特征缓存**范式，与以下基线方法构成直接对比关系：

| 方法 | 范式 | 预测机制 | 系数来源 |
|------|------|----------|----------|
| **TaylorSeer** (Liu et al., ICCV 2025) | 预测型 | 截断泰勒展开 | 固定公式 |
| **FoCa** (Zheng et al., AAAI 2026) | 预测型 | BDF2 + Heun 校正 | 固定公式 |
| **TeaCache** | 重用/自适应型 | 自适应阈值重用 | — |
| **FORA** | 重用型 | 特征重用 | — |
| **ToCa** | 令牌感知型 | 令牌级缓存 | — |
| **DuCa** | 双特征型 | 双特征缓存 | — |
| **L²P (Ours)** | **预测型** | **可学习线性组合** | **数据驱动** |

L²P 的核心贡献在于揭示了预测型缓存方法中“固定系数”这一被忽视的设计瓶颈，并通过极简的可学习线性预测器实现了对最优预测的有效逼近，在 DiT 特征缓存加速领域建立了新的方法论基线。

L²P 的整体框架由两个对称的阶段构成：**离线训练**与**在线推理**，二者共享同一个轻量级可学习线性预测器，如图2所示。

### 训练阶段：轨迹采集与权重回归

训练阶段并不修改扩散模型的参数，而是对预测器权重矩阵 $W$ 进行极小规模的监督学习。流程如下：

1. **轨迹数据采集**：使用约50张图像运行完整的扩散去噪轨迹（50步），在每个时间步 $t$ 记录DiT最后一层的输出特征 $\mathcal{F}(x_t)$，形成“历史特征→当前特征”的训练对。这一设计源于关键发现：仅使用最后一层特征即可实现高保真预测，无需存储或处理中间层特征，从而大幅降低内存与计算开销。

2. **预测器结构**：可学习线性预测器的参数为矩阵 $W \in \mathbb{R}^{49 \times 49}$，其中第 $t$ 行 $W_{t,:}$ 包含了预测第 $t$ 步特征所需的所有历史特征线性组合权重。预测公式为：
   $$\hat{\mathcal{F}}(x_t) = \sum_{j=0}^{t-1} W_{t,j} \cdot \mathcal{F}(x_j)$$
   其中 $\hat{\mathcal{F}}(x_t)$ 为预测特征，$\mathcal{F}(x_j)$ 为缓存的历史特征。

3. **训练目标与初始化**：以均方误差（MSE）损失最小化预测特征与真实特征的差异为目标。权重矩阵采用特殊初始化策略：除 $W_{t,t-1}$ 初始化为1外，其余系数均初始化为0。这一初始化等价于朴素的“特征重用”缓存策略，为优化提供了一个合理的起点。训练在单块GPU上约20秒即可收敛。

### 推理阶段：跳过计算与特征预测

推理阶段利用训练好的权重矩阵 $W$，在保持生成质量的同时大幅减少DiT前向计算次数：

1. **周期性调度**：以步长间隔 $N$ 定义锚点步与跳过步。在锚点步执行完整的DiT前向计算，并将最后一层特征存入缓存。

2. **特征预测**：对于跳过步，不执行DiT计算，而是调用预测器，用缓存中的历史特征与对应的权重行 $W_{t,:}$ 进行加权求和，直接输出预测特征 $\hat{\mathcal{F}}(x_t)$。该预测特征替代真实DiT输出进入后续去噪流程。

3. **计算节省**：由于跳过步完全绕过了昂贵的DiT前向传播，FLOPs和延迟均获得与跳过比例成正比的降低。例如在 $N=5$ 的设置下，仅约1/5的时间步需要完整计算。

### 模块关系与数据流

整个框架的核心数据流可概括为：**完整轨迹 → 特征缓存 → 线性回归 → 权重矩阵 → 跳跃推理**。训练阶段产生的权重矩阵 $W$ 是连接两个阶段的唯一桥梁，其极小的参数量（49×49）确保了训练和推理的额外开销几乎可忽略。预测器本身不依赖任何特定数据语义（消融实验证实，即使使用无语义内容图像训练，性能依然远超固定公式基线），学习到的是去噪轨迹中特征演化的内在时序模式。

![[assets/figures/papers/paper_list_l839_https_arxiv_org_abs_2604_26365/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed*

### 3.1 现有预测型缓存方法的统一线性形式

L²P 首先揭示了一个关键观察：现有的预测型特征缓存方法——无论其表面形式是泰勒展开还是预测-校正——在数学本质上均可统一为历史特征的固定系数线性组合。

具体而言，**TaylorSeer**（Liu et al., ICCV 2025）通过截断泰勒展开预测特征：

$$\mathcal{F}_{\mathrm{pred},m}(x_{t-k}^{l}) = \mathcal{F}(x_{t}^{l}) + \sum_{i=1}^{m} \frac{\Delta^{i} \mathcal{F}(x_{t}^{l})}{i! \mathcal{N}^{i}} (-k)^{i}$$

其中 $m$ 阶有限差分 $\Delta^{i} \mathcal{F}(x_{t}^{l})$ 可展开为历史特征的线性组合：

$$\Delta^{i} \mathcal{F}(x_{t}^{l}) = \sum_{j=0}^{i} (-1)^{j} \binom{i}{j} \mathcal{F}(x_{t-jN}^{l})$$

将上述两式合并，TaylorSeer 的预测本质上等价于：

$$\hat{\mathcal{F}}(x_{t+k}^{l}) = \sum_{j=0}^{m} \alpha_j \cdot \mathcal{F}(x_{t-jN}^{l})$$

其中系数 $\alpha_j$ 完全由展开阶数 $m$ 和步长间隔 $N$ 决定，是固定不变的手工设计值。

类似地，**FoCa**（Zheng et al., AAAI 2026）虽采用 BDF2 预测-校正机制，其核心预测步骤同样可归约为对有限历史特征的固定系数加权求和。这一统一视角揭示出此类方法的根本瓶颈：**系数由先验公式锁定，无法适应不同模型架构与去噪阶段的特征演化动态**。

### 3.2 线性表示上界的实证验证

为论证可学习线性预测的可行性，L²P 对扩散 Transformer 的特征轨迹进行了线性表示能力分析。对于时间步 $t$ 的当前特征 $\mathcal{F}(x_t)$，其最优线性近似为在历史特征张成子空间 $V_t = \mathrm{span}(\mathcal{F}(x_0), \dots, \mathcal{F}(x_{t-1}))$ 上的正交投影：

$$\mathcal{F}^*(x_t) = \mathrm{Proj}_{V_t}(\mathcal{F}(x_t))$$

投影质量通过相对残差衡量：

$$\mathrm{Relative\ Residual} = \frac{\|\mathcal{F}(x_t) - \mathcal{F}^*(x_t)\|_2}{\|\mathcal{F}(x_t)\|_2}$$

在 50 步扩散轨迹上的实验（Figure 1）显示，绝大多数内部去噪步骤的投影保真度（$1 - \mathrm{Relative\ Residual}$）超过 **0.95**，表明当前特征可被历史特征以极高精度线性重建。这一发现构成了 L²P 极简线性设计的理论依据：既然线性表示的上界已经足够高，则无需引入复杂的非线性建模。

### 3.3 L²P 可学习线性预测器

基于上述分析，L²P 的核心创新在于将固定公式系数替换为数据驱动的可学习权重矩阵 $W$。预测公式为：

$$\hat{\mathcal{F}}(x_t) = \sum_{j=0}^{t-1} W_{t,j} \cdot \mathcal{F}(x_j)$$

其中：
- $\hat{\mathcal{F}}(x_t)$ 为时间步 $t$ 的预测特征；
- $\mathcal{F}(x_j)$ 为历史时间步 $j$ 的缓存特征（仅使用最后一层特征，以减少内存开销）；
- $W_{t,j}$ 为针对时间步 $t$ 和历史步 $j$ 的可学习标量权重。

完整权重矩阵 $W \in \mathbb{R}^{49 \times 49}$（对应 50 步扩散轨迹），第 $t$ 行包含预测第 $t$ 步所需的所有历史步权重。训练时，使用约 50 张图像运行完整扩散轨迹并记录各步的最后一层特征，构建训练对（历史特征 → 当前特征），通过最小化 MSE 损失优化 $W$：

$$W^* = \arg\min_W \mathbb{E}\left[ \|\hat{\mathcal{F}}(x_t) - \mathcal{F}(x_t)\|_2^2 \right]$$

权重矩阵初始化为朴素特征缓存策略：除 $W_{t, t-1} = 1$ 外，其余系数均为 0。这一初始化在数学上等价于直接重用上一步特征，使训练从合理起点出发，在单块 GPU 上约 20 秒即可收敛。

推理时，对于被跳过的时间步 $t$，直接利用已缓存的历史特征和训练好的权重 $W_{t,j}$ 计算预测特征，从而绕过昂贵的 DiT 前向计算。

![[assets/figures/papers/paper_list_l839_https_arxiv_org_abs_2604_26365/figures/004_Figure_3.jpg]]
*Figure 3: MSE Loss Comparison Across Intervals. Logarithmic comparison of MSE loss between our method, TaylorSeer, and FoCa for predictions at different step intervals*

## 实验与关键发现

### 主要结果：文本到图像生成

L²P 在主流扩散Transformer模型上进行了系统的定量评估，涵盖延迟加速比、FLOPs缩减以及多项感知质量指标（PSNR、SSIM、LPIPS）。所有对比基线均使用官方实现，在相同的50步推理基准下评估，确保公平性。

**FLUX.1-dev 上的性能。** 如 Table 1 所示，在 N=5 的设置下，L²P 实现了 **4.55× FLOPs 缩减**和 **4.15× 延迟加速比**，同时保持 **PSNR 31.459**。相比之下，最强的预测型基线方法 **TaylorSeer**（Liu et al., ICCV 2025）在相同 N=5 设置下仅达到 PSNR 29.328，L²P 领先 **+2.131 dB**。在更激进的 N=9 设置下，L²P 的 PSNR 为 30.031，而 TaylorSeer 仅为 28.381，优势进一步扩大。这表明可学习系数在高加速比场景下的鲁棒性远超固定公式方法。

**Qwen Image 上的性能。** Table 2 展示了在 Qwen Image 上的结果。在 N=7（5.56× FLOPs 缩减）设置下，L²P 取得 **PSNR 30.627**，显著优于 FoCa（29.193）和 TaylorSeer（28.671）。当加速比推至 N=10（7.14× FLOPs 缩减）时，L²P 仍保持 PSNR 30.031，而所有基线方法均低于 29.1。在 Qwen-Image-Lightning 上，L²P 进一步实现了高达 **7.18× 加速比**，同时保持高视觉保真度。

**视频生成扩展。** L²P 的线性预测框架同样适用于视频扩散模型。在 HunyuanVideo 上（Table 5），N=7 设置下 L²P 取得 **PSNR 21.10**，远超 TeaCache（18.25，l=0.4），提升 **+2.85 dB**。定性结果（Figure 8）显示，L²P 在高加速比下仍能构建连续的动态过程，主体准确性优异。

### 预测精度分析

Figure 3 从预测精度的角度揭示了 L²P 优势的根源。在不同步长间隔（N=1, 5, 10）下，L²P 的 MSE 损失始终显著低于 TaylorSeer 和 FoCa，且差距随间隔增大而急剧扩大。这验证了核心论断：固定公式系数在近距离预测时勉强可用，但在远距离（高加速比）场景下，数据驱动的可学习权重能够自适应地捕捉特征演化模式，从而维持高预测精度。

### 消融实验

**数据效率。** Figure 6 展示了训练样本数量对性能的影响。仅使用 **5 个训练样本**，L²P 即可达到 PSNR 29.412，已超过 TaylorSeer（N=9）的 28.381。当训练样本增至 50 时，PSNR 达到峰值 30.031，此后趋于饱和。这一极低的数据需求源于 L²P 仅需学习 49×49 的参数矩阵，训练在单块 A100 GPU 上约 **20 秒**即可收敛。

**语义无关性。** Table 3 揭示了 L²P 学习到的究竟是什么。当使用无语义内容（gibberish）的图像训练时，L²P 仍取得 PSNR **30.430**，远超 TaylorSeer 的 28.671。使用随机噪声或反事实（错误文本对应图像）训练时，性能同样保持稳定。这强有力地证明：L²P 学习的是**特征演化的时间动力学模式**，而非训练数据的语义内容。这一特性赋予了方法极强的泛化能力。

**线性设计的充分性。** 论文在补充材料中探索了多种非线性增强方案，包括空间变化系数、二次项和注意力机制。实验结果表明，这些增强均未带来显著的性能提升，验证了当前极简线性设计的充分性。这与 Figure 1 的发现一致：对于大多数去噪步骤，当前特征可被历史特征以超过 0.95 的投影保真度线性重建，因此线性预测器已逼近理论上界。

**内存开销。** Table 4 对比了各方法的 GPU 内存占用。L²P 由于仅缓存最后一层特征（而非全部层），内存开销显著低于需要维护多层特征或高阶差分统计量的基线方法，在保持高性能的同时实现了更优的内存效率。

### 定性分析

Figure 4 展示了不同方法在相同 prompt 下的生成结果对比。在多个加速比设置下，L²P 生成的图像在细节保真度、纹理一致性和语义对齐方面均优于 TeaCache、ToCa、DuCa、TaylorSeer 和 FoCa。尤其在极端加速比下，固定公式方法出现明显的纹理崩坏和语义漂移，而 L²P 仍能保持稳定的视觉质量。

![[assets/figures/papers/paper_list_l839_https_arxiv_org_abs_2604_26365/figures/005_Figure_4.jpg]]
*Figure 4: Image Generation Comparison Across Methods. Comparison of image generation results for different methods (TeaCache, ToCa, DuCa, TaylorSeer, FoCa, and Ours) based on a set of prompts. The results show the generated images for each method along with the scaling factors, highlighting how each model interprets the given prompts*

### 局限性与失效模式

尽管 L²P 在特征缓存加速范式中表现优异，其局限性同样值得注意：

1. **无法减少采样总步数。** L²P 属于特征缓存加速范式，仍依赖原始 DiT 计算某些关键时间步，无法像蒸馏方法（如一致性模型）那样从根本上减少去噪步数。
2. **中间层特征依赖。** L²P 的线性预测仅作用在最后一层特征。若下游任务或特定应用场景依赖中间层特征，该方法可能不直接适用。不过，论文指出这一设计选择是基于实验验证——仅使用最后一层特征即可实现高质量预测，同时最大化内存和计算效率。
3. **新模型的适配成本。** 虽然训练仅需 50 张图像和约 20 秒，但对每个新模型仍需额外收集离线轨迹数据。该过程可自动化，但仍构成一定的工程开销。

![[assets/figures/papers/paper_list_l839_https_arxiv_org_abs_2604_26365/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison in text-to-image generation for FLUX*

![[assets/figures/papers/paper_list_l839_https_arxiv_org_abs_2604_26365/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison in text-to-image generation for Qwen Image*

![[assets/figures/papers/paper_list_l839_https_arxiv_org_abs_2604_26365/figures/009_Figure_6.jpg]]
*Figure 6: Ablation Study on Data Efficiency. Analysis of our method’s performance with varying training set sizes (5, 10, 25, 50, 100) at*

## 定位与知识库关联

### 预测型缓存方法的统一线性形式

在扩散Transformer加速的缓存方法谱系中，现有工作可大致分为**重用型**与**预测型**两类。重用型方法（如 **TeaCache**、**FORA**、**ToCa**、**DuCa**）在锚点步计算并存储特征，后续被跳过的步直接复用该缓存特征，其核心在于设计何时刷新缓存的调度策略。预测型方法则试图通过历史特征的组合来推断被跳过步的特征，代表工作包括 **TaylorSeer**（Liu et al., ICCV 2025）和 **FoCa**（Zheng et al., AAAI 2026）。

本文的关键洞察在于揭示：这些预测型方法的数学本质是**历史特征的固定系数线性组合**。TaylorSeer通过截断泰勒展开预测特征，其有限差分展开等价于对历史特征施加一组仅由展开阶数和步长决定的固定标量系数；FoCa的BDF2预测-校正机制同样可归约为历史特征的固定线性加权。这一统一视角意味着，现有预测型方法的性能瓶颈不在于线性形式的表达能力不足，而在于**系数由数学公式先验决定，缺乏对具体模型和去噪步长的自适应性**。

### 线性表示上界的实证发现

为验证线性预测的潜力上限，本文对扩散Transformer的特征轨迹进行了投影保真度分析。如Figure 1所示，在50步扩散轨迹中，将当前时间步特征投影到历史特征张成的线性子空间上，其投影保真度（定义为1减去相对投影残差）在大多数内部去噪步中超过0.95。这一发现表明：**扩散Transformer在大部分去噪步骤中，当前层特征可以被历史特征以极高的精度线性表示**，线性预测的理论上界远高于现有固定系数方法所能达到的水平。这为用数据驱动方式学习最优线性组合系数提供了坚实的实证动机。

### 方法定位与核心差异

**L²P（Learnable Linear Predictor）** 在缓存方法谱系中的定位是**预测型缓存方法的可学习化升级**。与TaylorSeer和FoCa相比，L²P保持了相同的线性组合形式，但将固定公式系数替换为通过MSE损失在缓存轨迹上学习得到的逐时间步权重矩阵 $W_{t,j}$。这一设计选择具有三个关键特征：

1. **极简性**：L²P仅使用最后一层特征进行预测，参数矩阵大小仅为 $49 \times 49$，训练在单块GPU上约20秒即可收敛。
2. **数据效率**：仅需约50张图像即可达到性能饱和，甚至5个训练样本就能使PSNR超过TaylorSeer在更大加速比下的表现（Figure 6）。
3. **语义无关性**：使用无语义内容（gibberish）图像训练时，L²P仍取得PSNR 30.430，远超TaylorSeer的28.671（Table 3），证明学习到的是**特征演化模式**而非数据语义。

### 适用边界与局限

L²P的适用边界由以下因素界定：

- **范式约束**：方法属于特征缓存加速范式，无法减少扩散采样的总步数，仍依赖原始DiT计算某些关键时间步。这与基于蒸馏的少步生成方法（如一致性模型）处于不同的加速维度。
- **特征层级限制**：线性预测仅作用在最后一层特征。若下游任务或特定模型架构强依赖中间层特征，当前设计可能不直接适用。
- **离线训练需求**：虽然训练开销极低，但对每个新模型仍需额外的轨迹数据收集步骤，无法实现零样本迁移。
- **非线性增强的边际收益**：论文在补充材料中尝试了空间变化系数、二次项、注意力等非线性增强，均未带来显著性能提升，验证了当前线性设计的充分性，但也表明该方法在表达能力上已接近当前假设下的上限。

### 开放问题

以下问题尚待进一步探索：

1. **跨架构迁移性**：学习到的线性权重 $W$ 能否在不同DiT结构间直接迁移或微调？这决定了方法在多模型部署场景中的实用性。
2. **高分辨率/长序列扩展**：在更高分辨率图像或更长视频序列上，线性表示假设是否依然保持高保真度？HunyuanVideo上的初步结果（Table 5）显示L²P在视频生成中同样有效，但更极端的序列长度仍有待验证。
3. **与少步生成方法的叠加**：L²P能否与基于蒸馏的少步生成方法（如一致性模型、LCM）结合，实现特征缓存与采样步数减少的叠加加速？
4. **细粒度权重设计**：是否可以将可学习系数从全局共享推广到token级别或层级别的细粒度权重，以进一步提升预测精度？

## 原文 PDF

![[paperPDFs/CVPR_2026/Beyond_Fixed_Formulas_Data_Driven_Linear_Predictor_for_Efficient_Diffusion_Models.pdf]]
