---
title: Accelerating Diffusion via Hybrid Data-Pipeline Parallelism Based on Conditional Guidance Scheduling
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Accelerating_Diffusion_via_Hybrid_Data_Pipeline_Parallelism_Based_on_Conditional_Guidance_Scheduling.pdf
project_link: null
code_link: "https://github.com/kaist-dmlab/Hybridiff"
aliases:
- HDPPH
- ADHDPPBCGS
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 分类器无关引导（CFG）中条件与无条件去噪分支之间的差异，即“去噪差异（denoising discrepancy）”，它既天然提供了一种新的数据分区方式（按条件 vs 无条件路径），又能指示何时切换串行/并行执行以达到最高效加速。
primary_logic: 利用CFG中条件与无条件去噪路径作为两个独立的数据并行流，结合去噪差异动态判断激活流水线并行的最佳区间，形成“条件分区 + 自适应并行切换”的混合并行框架，成功突破传统数据/流水线并行的加速上限且几乎不损失生成质量。
claims:
- 在SDXL上，2 GPU设置下混合方法取得2.31×加速，延迟从单GPU的16.49s降至7.12s，同时FID（w/ G.T.）为23.831（原始模型23.977），LPIPS几乎不变；大幅领先DistriFusion（1.22×）和AsyncDiff（1.31×）。
- 去噪差异rel-MAE_t在去噪过程中呈U形曲线，中间区域接近零且稳定，作为自适应并行切换的定量依据。该现象在MS-COCO 2014 5000个提示上验证。
- 通信量从AsyncDiff的9.830 GB降至0.516 GB（降低19.6倍），归功于仅在差异稳定期进行条件交换的三阶段调度。
- SDXL (MS-COCO 2014, 2 GPUs) 上 Latency (s) = 7.12
---

# Accelerating Diffusion via Hybrid Data-Pipeline Parallelism Based on Conditional Guidance Scheduling

> [!tip] 核心洞察
> 利用CFG中条件与无条件去噪路径作为两个独立的数据并行流，结合去噪差异动态判断激活流水线并行的最佳区间，形成“条件分区 + 自适应并行切换”的混合并行框架，成功突破传统数据/流水线并行的加速上限且几乎不损失生成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于条件引导调度的混合数据-流水线并行加速扩散模型 |
| 英文题名 | Accelerating Diffusion via Hybrid Data-Pipeline Parallelism Based on Conditional Guidance Scheduling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.21760) · [Code](https://github.com/kaist-dmlab/Hybridiff) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Hybrid Data-Pipeline Parallelism (Hybridiff) |
| Dataset | SDXL, SD3 |

> [!tip] 效果简介
> - SDXL (MS-COCO 2014, 2 GPUs) 上，Latency (s) 7.12 vs 16.49 (Original single-GPU) (2.31× speed-up)；FID (w/ G.T.) 23.831 vs 23.977 (Original) (-0.146)；LPIPS (w/ G.T.) 0.796 vs 0.797 (Original) (-0.001)。
> - SD3 (MS-COCO 2014, 2 GPUs) 上，Latency (s) 9.33 vs 19.36 (Original single-GPU) (2.07× speed-up)；FID (w/ G.T.) 33.322 vs 33.433 (Original) (-0.111)；LPIPS (w/ G.T.) 0.780 vs 0.810 (Original) (-0.030)。
> - SDXL (消融实验, 2 GPUs) 上，Speed-Up 2.31× (全混合) vs 1.78× (仅条件分区) (+0.53×)。

## 概要

扩散模型在高质量图像生成领域取得了显著成功，但推理速度慢始终是部署瓶颈。现有分布式推理加速方案主要分为两类：基于图像补丁的数据并行（如DistriFusion）和基于异步流水线的模型并行（如AsyncDiff）。前者因全聚合（all-gather）操作和补丁边界伪影导致加速有限且质量下降；后者则承受高昂的异步通信开销和误差累积，加速比难以随GPU数量线性扩展。两者均无法在不牺牲生成质量的前提下实现与GPU数量成比例的加速。

本文提出**Hybridiff**——一种融合数据并行与流水线并行的混合并行框架，其核心思想来自对分类器无关引导（Classifier-Free Guidance, CFG）机制的重新审视。CFG在每一步去噪中同时运行条件分支和无条件分支，这一天然的双路径结构恰好构成一种新的数据分区方式：将条件路径和无条件路径分别分配给不同GPU，形成**条件分区（condition-based partitioning）**。进一步，作者发现条件与无条件去噪输出之间的差异——称为**去噪差异（denoising discrepancy）**——在去噪过程中呈现稳定的U形曲线：早期和晚期差异较大，中间阶段趋近于零。这一现象为自适应并行切换提供了定量依据：在差异较大的阶段保持串行以确保条件引导的一致性，仅在差异稳定阶段激活流水线并行以最大化加速。

基于上述洞察，Hybridiff将去噪过程划分为三个阶段：**Warm-Up阶段**（差异大，串行执行）、**Parallelism阶段**（差异近零，条件交换流水线并行）和**Fully-Connecting阶段**（差异再次增大，恢复串行）。切换时机由去噪差异的滑动窗口斜率动态判定，无需人工预设。

在双NVIDIA RTX 3090 GPU配置下，Hybridiff在SDXL上取得**2.31×加速**（延迟从16.49s降至7.12s），在SD3上取得**2.07×加速**，同时FID和LPIPS与单GPU原始模型几乎一致（SDXL FID: 23.831 vs 23.977）。通信量从AsyncDiff的9.830 GB降至**0.516 GB（降低约19倍）**。在速度-质量帕雷托前沿上，Hybridiff全面优于DistriFusion（1.22×）和AsyncDiff（1.31×）等基线方法。

**方法定位**：Hybridiff属于扩散模型推理加速中的分布式并行方法，其条件分区策略为数据并行提供了新视角，自适应切换机制则突破了传统静态调度的加速上限。该方法不修改模型权重，可与现有加速技术（如步数缩减、模型蒸馏）正交叠加。当前实现针对双GPU场景优化，向更多GPU扩展的批量级和层级流水线方案已在附录中给出初步设计，但单图像超过2的并行度仍待进一步验证。

扩散模型已成为图像生成的主流范式，但其推理过程需要迭代执行数十步去噪，每一步都涉及大规模神经网络的前向传播，导致生成延迟居高不下。以 Stable Diffusion XL（SDXL）为例，在单张 NVIDIA RTX 3090 GPU 上生成一张 1024×1024 图像需耗时约 16.5 秒，难以满足交互式应用对实时性的需求。分布式并行推理是缓解这一瓶颈的直接思路，然而现有方法在加速比、生成质量与通用性之间面临显著的权衡困境。

### 现有并行方法的瓶颈

当前扩散推理的并行策略主要分为两类：基于补丁的数据并行与基于异步的流水线并行，二者各有结构性缺陷。

**基于补丁的数据并行**以 **DistriFusion** 为代表。其核心思路是将输入图像切割为多个空间补丁（patch），各 GPU 独立处理一块，再通过全聚合（all-gather）操作同步中间特征。这一策略面临双重瓶颈：一是全聚合操作随 GPU 数量增加而急剧放大通信开销，形成加速瓶颈；二是补丁边界的特征不一致会引入视觉伪影，损害生成质量。在双 GPU 设置下，DistriFusion 的加速比仅为 1.22×，远未达到线性加速的期望。

**基于异步流水线的模型并行**以 **AsyncDiff** 和 **ParaStep** 为代表。这类方法将模型层或去噪步跨 GPU 流水线化，允许各 GPU 异步执行以减少同步等待。然而，异步执行带来的近似误差会在流水线中累积，导致生成质量下降；同时，跨 GPU 的中间激活传输产生巨额通信开销——AsyncDiff 在双 GPU 下的总通信量高达 9.830 GB。其加速比仅为 1.31×，通信代价严重侵蚀了并行收益。

此外，**XDiT-Ring** 等基于环形注意力的 Transformer 并行方案主要针对 DiT 架构设计，对 UNet 类扩散模型的通用性受限。综合来看，现有方法在双 GPU 场景下的加速比均未超过 1.31×，且普遍伴随生成质量退化，无法实现与 GPU 数量成比例的加速。

### 核心动机：从“空间分区”到“条件分区”

上述方法的共同缺陷在于：它们均沿袭了传统视觉模型的**空间分区**思维——将图像或特征图在空间维度上切分。然而，扩散模型独有的**分类器无关引导（Classifier-Free Guidance, CFG）**机制提供了一个被忽视的天然并行维度。

CFG 在每一步去噪中需同时计算两个噪声估计：**条件去噪路径** $\epsilon_\theta(\mathbf{x}_t, c, t)$（接收文本提示）与**无条件去噪路径** $\epsilon_\theta(\mathbf{x}_t, t)$（无提示），最终通过线性组合 $\epsilon_\theta(\mathbf{x}_t, t) + w(\epsilon_\theta(\mathbf{x}_t, c, t) - \epsilon_\theta(\mathbf{x}_t, t))$ 得到引导噪声。这两条路径在计算上完全独立，天然构成两个数据并行流，无需任何空间切分即可分配到不同 GPU 上执行。这一观察将并行分区的视角从“空间”转向“条件”，从根本上规避了补丁边界伪影和全聚合通信的问题。

更进一步，条件与无条件路径之间的**去噪差异（denoising discrepancy）**并非恒定。经验观察表明，在去噪过程的早期和晚期，两条路径的噪声估计差异较大；而在中间阶段，两者趋于一致。这一现象暗示：并非所有去噪步都需要进行条件交换——当差异足够小时，两条路径可以安全地并行执行而不损失引导质量；当差异重新扩大时，则需恢复串行以保证保真度。这一洞察为**自适应并行切换**提供了定量依据，使得混合并行框架能够在保证生成质量的前提下，最大化并行效率。

基于以上动机，本文提出 **Hybridiff**——一种结合条件分区数据并行与自适应流水线切换的混合并行框架，旨在突破现有分布式扩散推理的加速上限，同时几乎不牺牲生成质量。

## 核心方法与创新机理

### 从图像分块到条件分区：数据并行策略的根本转变

现有分布式扩散推理的并行方法均围绕**将输入图像切分为空间补丁**这一核心策略展开。**DistriFusion** 在去噪过程中将图像划分为多个补丁，各GPU独立处理局部区域，再通过全聚合（all-gather）操作同步全局上下文；**AsyncDiff** 则将模型按层切分，以异步流水线方式处理完整图像。这两种范式各自面临不可逾越的瓶颈：补丁数据并行在补丁边界引入生成伪影，且全聚合通信随GPU数量增长成为加速瓶颈；异步流水线并行则因跨步估计误差累积导致质量退化，且异步通信开销高达9.830 GB（Table 1）。

本文的核心突破在于**彻底抛弃了基于空间补丁的分区逻辑**，转而利用分类器无关引导（CFG）机制中天然存在的双路径结构——条件去噪分支 $\epsilon_\theta(\mathbf{x}_t, c, t)$ 和无条件去噪分支 $\epsilon_\theta(\mathbf{x}_t, t)$——作为两个独立的数据并行流。这一“条件分区”（condition-based partitioning）策略将两个分支分别部署到不同GPU上，从根本上消除了补丁边界的伪影问题，同时将通信内容从空间特征聚合转变为条件信息的点对点交换。

### 去噪差异：从静态调度到自适应并行切换

传统流水线并行方法（如AsyncDiff）采用**固定的并行区间**，在预热阶段结束后机械地启动并行执行，无法感知去噪过程中条件与无条件分支之间差异的动态变化。本文的核心洞察在于发现了两分支噪声估计之间的**去噪差异（denoising discrepancy）**呈现稳定的U形曲线：

$$\mathrm{rel-MAE}_t(\epsilon_c, \epsilon_u) = \frac{\mathbb{E}_{\mathbf{x}, \epsilon}[\| \epsilon_\theta(\mathbf{x}_t, c, t) - \epsilon_\theta(\mathbf{x}_t, t) \|_1]}{\mathbb{E}_{\mathbf{x}, \epsilon}[\| \epsilon_\theta(\mathbf{x}_t, t) \|_1]}$$

该指标在去噪初期（$t$ 接近 $T$）和末期（$t$ 接近 0）数值较大，而在中间区域收敛至接近零（Figure 4）。这一现象在MS-COCO 2014验证集的5000个提示上得到验证，为自适应调度提供了定量依据。

基于此，本文设计了**自适应并行切换**机制，通过滑动窗口计算去噪差异的平均斜率 $G_t = \frac{M_t - M_{t-L}}{L}$，动态确定进入并行阶段的时刻 $\tau_1$（即斜率低于阈值 $g_{\text{slope}}$ 且受安全上限 $\tau_{\text{cap}}$ 约束的最早时间步），并设置 $\tau_2 = \tau_1 + k$ 作为并行阶段的终止点。这种数据驱动的切换策略确保了并行执行仅在条件与无条件分支高度一致的区间内进行，从而在加速的同时保持生成质量。

### 通信模式的质变：从全量同步到选择性交换

混合并行框架将去噪过程划分为三个阶段（Figure 3）：**预热阶段**（$[T, \tau_1]$）两分支独立运行，仅进行必要的序数通信；**并行阶段**（$(\tau_1, \tau_2)$）进行条件信息交换以维持引导一致性；**全连接阶段**（$[\tau_2, 0]$）恢复串行执行以保留条件控制的精细度。这一设计使通信量从AsyncDiff的9.830 GB骤降至0.516 GB，**降低19.6倍**（Table 1），从根本上解决了通信开销对加速比的侵蚀。

### 消融验证：条件分区与自适应切换的协同效应

消融实验（Table 2）清晰揭示了两个创新组件的协同关系：单独使用全条件分区（即整个去噪过程始终并行）仅能实现1.78×加速，而加入自适应并行切换后加速比提升至2.31×。这表明自适应调度不仅避免了并行阶段外的无效通信，更重要的是防止了差异较大区间的质量损失——这正是单纯条件分区无法解决的问题。

并行区间长度 $k$ 提供了直观的速度-质量权衡旋钮（Table 4, Figure 6）：当 $k$ 从5增至30时，加速比从2.31×上升至2.78×，但FID从4.100恶化至9.191。这一可控的帕雷托前沿使方法在不同应用场景下具有灵活的部署能力。

Hybridiff 提出了一种面向扩散模型推理的**混合数据-流水线并行框架**，其核心思想是将分类器无关引导（CFG）中的条件与无条件去噪路径重新解释为两种天然的数据并行流，并利用两者之间的**去噪差异（denoising discrepancy）**动态决定何时激活流水线并行，从而在几乎不损失生成质量的前提下突破传统分布式并行方法的加速上限。

### 设计动机与瓶颈突破

现有分布式扩散推理方法主要分为两条技术路线：

- **基于图像补丁的数据并行**（如 DistriFusion）：将输入图像切割成多个空间块分配到不同 GPU，但每次去噪步后需要全聚合（all-gather）操作来同步补丁边界信息，不仅引入高通信开销，还容易在补丁边界产生视觉伪影，加速比难以随 GPU 数量线性增长。
- **基于异步流水线的模型并行**（如 AsyncDiff）：将去噪过程的不同时间步流水线化分配到多 GPU，但异步通信模式导致噪声估计误差累积，且通信量随流水线深度急剧增加。

Hybridiff 的关键洞察在于：CFG 在每个时间步需要同时计算条件噪声估计 $\epsilon_\theta(\mathbf{x}_t, c, t)$ 和无条件噪声估计 $\epsilon_\theta(\mathbf{x}_t, t)$，这两条计算路径天然构成两个独立的数据流——这与传统的空间补丁分区完全不同。通过监控两条路径输出之间的差异（即去噪差异），可以精确判断何时两者的噪声估计足够接近、可以安全地并行执行而不影响最终生成质量。

### 三阶段并行调度

框架将整个去噪过程（从时间步 $T$ 到 $0$）划分为三个阶段，由两个关键切换点 $\tau_1$ 和 $\tau_2$ 分隔：

1. **热身阶段（Warm-Up Stage）** $[T, \tau_1]$：条件分支与无条件分支各自独立执行完整的去噪计算，仅在两者之间保持必要的序贯通信。此阶段去噪差异较大，强制并行会导致条件引导信息丢失。

2. **并行阶段（Parallelism Stage）** $(\tau_1, \tau_2]$：当去噪差异降至接近零的稳定区域时，两条分支的噪声估计高度一致，此时激活流水线并行——GPU 0 处理条件分支，GPU 1 处理无条件分支，仅在两者之间交换条件信息。由于差异极小，这种近似并行几乎不引入质量损失。

3. **全连接阶段（Fully-Connecting Stage）** $[\tau_2, 0]$：去噪差异重新增大，框架切换回全通信模式，确保最终生成图像的条件一致性。

### 自适应切换机制

$\tau_1$ 的确定是框架的核心。Hybridiff 通过实时计算去噪差异的滑动窗口斜率 $G_t$ 来自动判定进入并行阶段的时机：

$$G_t = \frac{M_t - M_{t-L}}{L}$$

其中 $M_t = \mathrm{rel\text{-}MAE}_t(\epsilon_c, \epsilon_u)$ 为当前步的去噪差异，$L$ 为滑动窗口长度。当 $G_t$ 低于预设阈值 $g_{\text{slope}}$ 且当前时间步不超过安全上限 $\tau_{\text{cap}}$ 时，即确定 $\tau_1$。$\tau_{\text{cap}}$ 基于去噪差异曲线的全局最小值离线设定，防止在异常提示下过早进入并行阶段。

$\tau_2$ 由 $\tau_1$ 后延固定步数 $k$ 确定：$\tau_2 = \tau_1 + k$，其中 $k$ 是控制速度-质量权衡的超参数。较小的 $k$ 保持更高保真度，较大的 $k$ 获得更强加速。

### 关键公式：去噪差异

去噪差异的定量定义如下：

$$\mathrm{rel\text{-}MAE}_t(\epsilon_c, \epsilon_u) = \frac{\mathbb{E}_{\mathbf{x}, \epsilon}[\| \epsilon_\theta(\mathbf{x}_t, c, t) - \epsilon_\theta(\mathbf{x}_t, t) \|_1]}{\mathbb{E}_{\mathbf{x}, \epsilon}[\| \epsilon_\theta(\mathbf{x}_t, t) \|_1]}$$

该指标在 MS-COCO 2014 验证集的 5000 个提示上呈现出稳定的 U 形曲线（Figure 4），在去噪中间阶段接近零，在首尾两端较大。这一经验规律为三阶段划分提供了直接依据。

从分数函数的角度，该差异可进一步解释为：

$$\mathrm{rel\text{-}MAE}_t(\epsilon_c, \epsilon_u) \approx \frac{\| \nabla_{\mathbf{x}_t} \log p(c|\mathbf{x}_t) \|_1}{\| s_u(\mathbf{x}_t, t) \|_1}$$

即条件梯度与无条件分数范数之比，揭示了去噪过程中条件信息强度的动态变化规律。

### 多 GPU 扩展

框架原生支持两种多 GPU 扩展策略（Figure 9）：
- **批量级扩展**：$N$ 个 GPU 两两配对，每对生成一张图像，共生成 $N/2$ 张图像。
- **层级流水线扩展**：在单张图像生成中将 UNet 的层切分到多个 GPU，与条件分区结合形成更细粒度的并行。

![[assets/figures/papers/paper_list_l834_https_arxiv_org_abs_2602_21760/figures/012_Figure_9.jpg]]
*Figure 9: Extensibility to many GPU configurations structures. This figure illustrates two strategies for scaling the proposed hybrid parallelism framework to larger GPU configurations. These structures demonstrate how the proposed framework naturally generalizes from the 2 GPUs setting to both batch-level and layer-wise many GPU configurations*

但需要注意的是，当前框架对单张图像超过 2 的并行度仍属开放问题，扩展方案存在质量或效率下降的风险。

![[assets/figures/papers/paper_list_l834_https_arxiv_org_abs_2602_21760/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the proposed diffusion inference hybrid parallel framework. Our method adaptively switches parallelism modes at τ1 and τ2, optimizing the trade-off between computational efficiency and consistency of conditional guidance, and demonstrates superior inference acceleration performance while preserving high generation quality*

![[assets/figures/papers/paper_list_l834_https_arxiv_org_abs_2602_21760/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of parallel strategies for diffusion inference. (a) Patch-based data parallel frameworks suffer from bottlenecks caused by all-gather operations and artifacts at patch boundaries, leading to limited acceleration and quality degradation. (b) Pipeline parallel frameworks incur excessive asynchronous communication overhead and accumulate estimate errors. (c) Our hybrid parallelism, which incorporates condition-based data parallelism, adaptively combines both paradigms to achieve high fidelity and fast generation*

### 3.1 整体框架与三阶段划分

Hybridiff 的核心思想是将分类器无关引导（CFG）中天然存在的**条件去噪路径**与**无条件去噪路径**视为两个独立的数据并行流，并根据两条路径在去噪过程中的差异动态切换并行策略。整个去噪过程被划分为三个阶段：

- **Warm-Up 阶段**（$[T, \tau_1]$）：两条路径独立执行，仅进行最小限度的序数通信（ordinal communication），不交换条件信息。
- **Parallelism 阶段**（$(\tau_1, \tau_2]$）：激活流水线并行，条件分支与无条件分支之间进行条件交换（conditional exchange），实现并行加速。
- **Fully-Connecting 阶段**（$[\tau_2, 0]$）：恢复全连接模式，两条路径重新同步以确保生成质量。

框架的核心模块包括：**条件/无条件去噪分支**、**去噪差异计算器**、**自适应切换调度器**、以及**三阶段处理器**。Figure 3 展示了整体流程。

### 3.2 去噪差异（Denoising Discrepancy）

去噪差异是驱动自适应切换的核心指标，用于量化每一步 $t$ 下条件噪声估计 $\epsilon_c$ 与无条件噪声估计 $\epsilon_u$ 之间的差异。其定义为相对平均绝对误差：

$$
\mathrm{rel\text{-}MAE}_t(\epsilon_c, \epsilon_u) = \frac{\mathbb{E}_{\mathbf{x}, \epsilon}\big[\| \epsilon_\theta(\mathbf{x}_t, c, t) - \epsilon_\theta(\mathbf{x}_t, t) \|_1\big]}{\mathbb{E}_{\mathbf{x}, \epsilon}\big[\| \epsilon_\theta(\mathbf{x}_t, t) \|_1\big]}
$$

其中 $\epsilon_\theta(\mathbf{x}_t, c, t)$ 为以文本提示 $c$ 为条件的噪声预测，$\epsilon_\theta(\mathbf{x}_t, t)$ 为无条件噪声预测。分母使用无条件预测的 $\ell_1$ 范数进行归一化，使得该指标在不同时间步之间可比。

**经验观察**：在 MS-COCO 2014 验证集的 5000 个提示上，$\mathrm{rel\text{-}MAE}_t$ 呈现清晰的 **U 形曲线**（见 Figure 4）。在去噪早期（$t$ 接近 $T$）和末期（$t$ 接近 0），差异较大；在中间区域差异收敛至接近零且保持稳定。这一现象为三阶段划分提供了定量依据——Parallelism 阶段恰对应差异稳定区间，此时两条路径的噪声估计高度一致，条件交换引入的误差最小。

### 3.3 自适应切换调度

切换时间点 $\tau_1$ 和 $\tau_2$ 的确定是混合并行的关键。$\tau_1$ 通过实时监测去噪差异的斜率动态确定：

$$
G_t = \frac{M_t - M_{t-L}}{L}
$$

其中 $M_t = \mathrm{rel\text{-}MAE}_t$，$L$ 为滑动窗口长度。$G_t$ 表示最近 $L$ 步去噪差异的平均斜率。当 $G_t$ 低于预设阈值 $g_{\text{slope}}$ 时，表明差异趋于稳定，此时进入 Parallelism 阶段：

$$
\tau_1 = \min\{t \mid 0 \leq G_t < g_{\text{slope}}, \; t \leq \tau_{\text{cap}}\}
$$

为防止误触发，引入**安全上限** $\tau_{\text{cap}}$，其值基于去噪差异曲线的全局最小值位置离线确定（见 Figure 8）。$\tau_1$ 被约束不超过 $\tau_{\text{cap}}$，确保并行阶段不会在差异尚未充分收敛时启动。

![[assets/figures/papers/paper_list_l834_https_arxiv_org_abs_2602_21760/figures/010_Figure_8.jpg]]
*Figure 8: Empirical visualization of denoising discrepancy curve*

$\tau_2$ 由 $\tau_1$ 后延固定步数 $k$ 确定：

$$
\tau_2 = \tau_1 + k, \quad k \in \mathbb{N}, \; 1 \leq k < T - \tau_1
$$

$k$ 是控制**速度-质量权衡**的超参数：较小的 $k$ 保持更高保真度，较大的 $k$ 获得更高加速比。消融实验（Table 4）显示，$k$ 从 5 增至 30 时，加速比从 2.31× 升至 2.78×，但 FID 从 4.100 恶化至 9.191。

### 3.4 去噪差异的分数解释

从分数函数（score function）角度，去噪差异具有更深层的理论含义。利用噪声预测与分数函数的关系 $s_\theta(\mathbf{x}_t, t) \approx -\epsilon_\theta(\mathbf{x}_t, t)/\sigma_t$，以及条件分数的贝叶斯分解 $s_c(\mathbf{x}_t, t) = s_u(\mathbf{x}_t, t) + \nabla_{\mathbf{x}_t} \log p(c|\mathbf{x}_t)$，可得：

$$
\mathrm{rel\text{-}MAE}_t(\epsilon_c, \epsilon_u) \approx \frac{\| \nabla_{\mathbf{x}_t} \log p(c|\mathbf{x}_t) \|_1}{\| s_u(\mathbf{x}_t, t) \|_1}
$$

该式揭示：去噪差异本质上是**条件信息强度**（条件梯度 $\nabla_{\mathbf{x}_t} \log p(c|\mathbf{x}_t)$）与**无条件数据先验**（无条件分数 $s_u$）的比值。在去噪初期，无条件先验主导，条件梯度相对显著，差异较大；在中期，两者趋于平衡，差异收敛；在末期，条件梯度再次增强以细化细节，差异回升。这一理论解释支撑了三阶段设计的合理性。

## 实验与关键发现

### 主实验结果与核心性能

在双GPU（2× NVIDIA RTX 3090）设置下，Hybridiff在Stable Diffusion XL（SDXL）和Stable Diffusion 3（SD3）上均实现了超过2倍的加速，同时保持与原始单GPU模型几乎一致的生成质量。**Table 1** 汇总了与DistriFusion、AsyncDiff、ParaStep、XDiT-Ring等基线的定量对比。

![[assets/figures/papers/paper_list_l834_https_arxiv_org_abs_2602_21760/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of parallelism methods on the Stable Diffusion XL and Stable Diffusion 3 models. We compare our method with existing distributed inference techniques under 1- and 2-GPU. We report both the baseline latency and the corresponding acceleration ratio (Speed-Up), Communication efficiency (Comm.), and quantitative metrics assessing generation fidelity. Here, w/ G.T. denotes comparison with the ground-truth image, and w/ Orig. indicates comparison with the original (single-GPU) model output*

**SDXL（1024×1024，DDIM 50步）：** 单GPU原始延迟为16.49秒，Hybridiff降至7.12秒，加速比达2.31×。作为对比，基于补丁数据并行的DistriFusion仅实现1.22×加速，基于异步流水线的AsyncDiff为1.31×。在质量维度，Hybridiff的FID（w/ G.T.）为23.831，与原始模型（23.977）基本持平，LPIPS（w/ G.T.）为0.796（原始0.797），PSNR（w/ Orig.）为30.263，均未出现明显劣化。通信量方面，Hybridiff仅需0.516 GB，相比AsyncDiff的9.830 GB降低了19.0倍。

**SD3（1024×1024，DDIM 50步）：** 单GPU延迟19.36秒，Hybridiff降至9.33秒，加速比2.07×。FID（w/ G.T.）为33.322（原始33.433），LPIPS（w/ G.T.）为0.780（原始0.810），质量保持甚至略有改善。

**Figure 5** 的定性对比进一步印证：Hybridiff生成的图像在视觉上与原始输出最为接近，而DistriFusion和AsyncDiff在细节和纹理一致性上存在可见偏差。

### 消融实验

**Table 2** 对混合并行的两个核心组件进行了拆解分析。在SDXL上，仅使用条件分区（condition-based partitioning）策略（即全程将条件与无条件分支分配到不同GPU，但不进行自适应切换）可实现1.78×加速。在此基础上引入自适应并行切换（adaptive parallelism switching）后，加速比提升至2.31×，增幅0.53×。这表明自适应调度通过仅在去噪差异稳定的中间阶段激活并行，有效减少了冗余通信和误差累积，是突破加速瓶颈的关键。

### 并行区间 k 的速度-质量权衡

并行区间 k 是控制质量-速度权衡的核心超参数。**Table 4** 和 **Figure 6** 展示了 k 从5增至30时的系统表现：加速比从2.31×单调上升至2.78×，但FID（w/ G.T.）从4.100恶化至9.191。较小的 k 值（如5–10）保持高保真度，较大的 k 值则通过延长并行阶段换取更高加速，但条件引导的一致性逐渐减弱，导致细节模糊（见 **Figure 11**）。该帕雷托前沿在所有对比方法中占据主导位置，表明Hybridiff在给定质量约束下可提供最优加速。

![[assets/figures/papers/paper_list_l834_https_arxiv_org_abs_2602_21760/figures/008_Figure_6.jpg]]
*Figure 6: Visualization of speed–quality trade-off across different parallelism intervals k. Smaller k values preserve higher fidelity, whereas larger k achieve greater acceleration. Our method consistently dominates prior works across the trade-off frontier. All experiments were conducted on 2 GPUs*

### 多维度综合评估

**Table 3** 将加速比、图像质量、通用性、高分辨率合成能力、通信成本五项指标归一化为5分制。Hybridiff在全部五个维度上均取得最高分，体现出均衡的加速-质量权衡。特别是高分辨率场景（**Figure 7**，NVIDIA H200，分辨率2048×2048和2560×2560）下，Hybridiff仍保持显著加速优势，而部分基线方法因通信开销或伪影问题在高分辨率下性能下降。

### 失败模式与局限性

1. **并行度受限：** 当前框架仅针对双GPU优化，单张图像的并行度超过2时存在质量或效率下降（见原文第4.5节及附录F的扩展方案分析）。
2. **k 需人工设定：** 并行区间 k 无自动化调整机制，需用户根据质量-速度需求手动选择；安全上限 τ_cap 依赖离线计算的去噪差异全局最小值，面对全新数据分布时可能需要重新校准。
3. **调度器依赖未验证：** 所有实验均基于DDIM 50步调度器，未展示在更少步数（如10–20步）或其他调度器（如DPM-Solver）下的加速保持能力。
4. **与其他加速技术未集成：** 未探讨与模型蒸馏、步数缩减等技术的协同，可能限制了整体加速潜力的上限。

## 定位与知识库关联

### 与现有并行策略的关系

扩散模型推理加速的分布式并行研究主要沿两条技术路线展开：**基于图像补丁的数据并行**与**基于异步流水线的模型并行**。本文提出的 Hybridiff 并非简单组合这两种范式，而是通过重新定义数据分区粒度和引入自适应切换机制，从根本上突破了二者的加速瓶颈。

**补丁数据并行（Patch-based Data Parallelism）**以 **DistriFusion** 为代表，将输入图像切割为空间补丁并分配到多 GPU 上并行去噪，每个步骤通过 All-Gather 操作聚合全局上下文。该策略面临两个硬性瓶颈：（1）All-Gather 通信开销随分辨率平方增长，严重侵蚀加速收益；（2）补丁边界处的感受野不完整导致结构性伪影，在 1024×1024 分辨率下尤为明显。实验数据显示 DistriFusion 在双 GPU 设置下仅实现 1.22× 加速，且 FID 从原始模型的 23.977 恶化至 25.001（Table 1），验证了补丁分区策略在质量-速度权衡上的失效。

**异步流水线并行（Asynchronous Pipeline Parallelism）**以 **AsyncDiff** 为代表，将去噪步骤沿时间轴切分为流水线阶段，通过异步执行相邻时间步实现并行。其核心缺陷在于：（1）异步通信引入的估计误差沿时间步累积，导致生成质量退化；（2）全时间步的异步通信量高达 9.830 GB（Table 1），成为加速比不可持续的主要原因。AsyncDiff 在双 GPU 下仅取得 1.31× 加速，远低于理想线性加速。

**Hybridiff 的关键突破**在于识别出分类器无关引导（CFG）中条件与无条件去噪分支之间的天然数据并行性——这是此前所有方法均未利用的结构属性。与补丁分区不同，条件分区不切割空间结构，因此从根本上避免了边界伪影问题；与全异步流水线不同，自适应切换仅在去噪差异接近零的区间激活并行通信，将通信量压缩至 0.516 GB（降低 19.0 倍）。这一设计使得 Hybridiff 在双 GPU 下实现 2.31× 加速（SDXL）和 2.07× 加速（SD3），同时保持与原始模型几乎无差异的 FID 和 LPIPS（Table 1）。

此外，**ParaStep** 通过相邻步骤的噪声估计重用实现加速，但其加速比受限于时间步间的相关性衰减，且不涉及多 GPU 并行。**XDiT-Ring** 针对 Transformer 架构的环形注意力并行，属于模型内部并行范畴，与 Hybridiff 的条件分区策略正交，二者可在更大 GPU 规模下组合使用。

### 适用边界与局限性

**当前适用边界**：
- **GPU 规模**：框架针对双 GPU 场景优化，单图像生成不支持超过 2 的并行度。论文第 4.5 节和附录 F 讨论了扩展到多 GPU 的两种方案（批量级扩展和层级流水线扩展），但实验表明这些扩展方案存在质量或效率下降，需手动验证。
- **模型架构**：已验证于 SDXL 和 SD3 两个代表性扩散模型，二者均采用 CFG 机制。对于不使用 CFG 的扩散模型（如直接预测分数的模型），条件分区策略不可直接迁移。
- **调度器**：所有实验均使用 DDIM 50 步调度器。去噪差异的 U 形曲线在更少步数（如 10–20 步）或其他调度器（如 DPM-Solver）下是否保持稳定并可用于指导切换，尚未验证。
- **任务类型**：当前仅验证于文本到图像生成任务。视频扩散模型或音频生成中条件/无条件分支的语义差异模式可能不同，需重新评估去噪差异指标的适用性。

**已知局限性**：
1. **并行区间 k 需人工预设**：k 控制质量-速度权衡（Table 4: k=5 时加速 2.31×, FID 4.100; k=30 时加速 2.78×, FID 恶化至 9.191），但无自动化选择机制。实际部署中需根据应用场景手动调整，缺乏自适应性。
2. **τ_cap 依赖离线标定**：安全上限 τ_cap 基于去噪差异全局最小值设置，依赖对目标数据分布的经验统计。面对全新数据分布时可能需要重新校准，限制了零样本部署能力。
3. **未与正交加速技术集成**：当前框架未探讨与模型蒸馏、步数缩减、量化等技术的组合效果。这些技术与条件分区策略在原理上正交，联合使用可能进一步提升加速上限，但交互效应未知。

### 开放问题

1. **自适应 k 机制**：能否设计基于实时质量指标的动态 k 调整策略？例如，利用去噪差异的局部统计特性或中间生成结果的感知质量反馈，自动决策并行区间的长度，从而避免人工预设的局限性。

2. **单图像多 GPU 扩展**：通过更细粒度的流水线切分（如将单个去噪步骤的 Transformer 层分配到不同 GPU）与条件分区的组合，能否让单张图像生成高效利用 4/8 块以上 GPU？这需要解决流水线气泡率和条件交换通信量随 GPU 数量增长的问题。

3. **跨调度器泛化性**：去噪差异的 U 形特征是否在非 DDIM 调度器（如 DPM-Solver、Euler 采样器）或更少步数下依然成立？若曲线形态发生变化，现有的斜率阈值 g_slope 和滑动窗口 L 是否需重新设计？

4. **跨模态迁移**：将该并行策略应用于视频扩散模型（如 Sora 类架构）或音频生成时，条件/无条件分支的语义差异模式是否仍呈现 U 形？视频模型中的时序一致性约束是否对并行切换时机提出额外要求？

5. **与推理优化技术的协同**：条件分区策略与模型量化、剪枝、知识蒸馏等推理优化技术的组合效应如何？是否存在加速收益的叠加或饱和效应？

## 原文 PDF

![[paperPDFs/CVPR_2026/Accelerating_Diffusion_via_Hybrid_Data_Pipeline_Parallelism_Based_on_Conditional_Guidance_Scheduling.pdf]]
