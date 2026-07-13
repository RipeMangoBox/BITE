---
title: "LiteVSR: Lightweight Adaptation of Frozen Diffusion Transformers for Video Super-Resolution"
type: paper
paper_level: A
venue: ICML
year: 2026
pdf_ref: paperPDFs/ICML_2026/LiteVSR_Lightweight_Adaptation_of_Frozen_Diffusion_Transformers_for_Video_Super-Resolution.pdf
project_link: null
code_link: null
aliases:
- LiteVSR
tags:
- ICML_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 基于流匹配的恒定速度预测特性，将 VSR 适配任务简化为在每个 DiT 块提供固定的注入模式，从而允许完全冻结 DiT 骨干；并设计状态感知适配器（State-Aware Adapter），通过双流结构（低质输入的静态结构流和中间去噪状态的动态细化流）结合时间调制交叉注意力，实现从结构对齐到纹理细化的自适应引导。
primary_logic: 流匹配中目标速度场在整个时间步上恒定，因此条件注入不再需要学习时变的变换，适配器仅需学习一个固定的引导信号，使得可以在不破坏预训练生成动力学的前提下，以极少的可训练参数实现 VSR。
claims:
- LiteVSR 使用完全冻结的 DiT 骨干和轻量级 State-Aware Adapter 进行 VSR，仅 11.25% 可训练参数。
- 流匹配学习恒定速度场，使条件任务从时变变换简化为固定注入模式，适配器只需提供固定引导信号。
- LiteVSR 在单个 A100 GPU 上训练约 12 GPU 小时，即能获得有竞争力的恢复质量，远低于现有方法的训练成本。
- REDS4 (synthetic) 上 CLIPIQA↑ = 0.3748
---

# LiteVSR: Lightweight Adaptation of Frozen Diffusion Transformers for Video Super-Resolution

> [!tip] 核心洞察
> 流匹配中目标速度场在整个时间步上恒定，因此条件注入不再需要学习时变的变换，适配器仅需学习一个固定的引导信号，使得可以在不破坏预训练生成动力学的前提下，以极少的可训练参数实现 VSR。

| 字段 | 内容 |
|------|------|
| 中文题名 | LiteVSR：基于冻结扩散变换器的轻量级视频超分辨率自适应 |
| 英文题名 | LiteVSR: Lightweight Adaptation of Frozen Diffusion Transformers for Video Super-Resolution |
| 会议/期刊 | ICML 2026 |
| Links | [paper](https://arxiv.org/abs/2606.09250) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | LiteVSR |
| Dataset | REDS4, UDM10, SPMCS |

> [!tip] 效果简介
> - REDS4 (synthetic) 上，CLIPIQA↑ 0.3748 vs 0.3186 (FlashVSR) (+0.0562)。
> - UDM10 (synthetic) 上，DOVER↑ 0.515 vs 0.4618 (FlashVSR) (+0.0532)。
> - SPMCS (synthetic) 上，MUSIQ↑ 70.42 vs 70.33 (FlashVSR) (+0.09)。

## 概要

视频超分辨率（VSR）旨在从低质量视频中恢复高保真细节。近年来，大规模预训练视频生成模型为VSR带来了显著的纹理生成能力，但其适配成本极高：现有方案要么对扩散变换器（DiT）进行全量微调，需要数十块GPU和数百万训练样本；要么采用ControlNet风格的适配器，在DiT架构下被迫复制整个骨干网络，导致参数量翻倍。这些方法均未能在保持预训练先验的同时实现轻量级高效适配。

LiteVSR的核心洞察在于，流匹配（Flow Matching）学习的是恒定速度场，因此条件注入任务被简化为在每个DiT块提供固定的引导信号，而无需学习时变的变换。基于这一原理，LiteVSR提出了一种极简框架：**完全冻结**DiT骨干网络，仅训练一个轻量级的**状态感知适配器（State-Aware Adapter）**。该适配器采用双流架构——从低质输入提取静态结构线索，从中间去噪状态提取动态细化线索——并通过时间调制交叉注意力实现从结构对齐到纹理细化的自适应引导。

在效率方面，LiteVSR仅需**11.25%的可训练参数**，在单张A100 GPU上训练约**12 GPU小时**即可收敛，训练成本远低于现有方法。在合成和真实世界数据集上的定量评估与用户研究表明，LiteVSR以极低的计算开销取得了有竞争力的恢复质量，在感知质量指标（如CLIPIQA、DOVER）上达到或超越同期方法。

**方法定位**：LiteVSR属于基于预训练视频扩散模型的VSR方法，与**Upscale-A-Video**（Zhou et al., CVPR 2024）、**DiffVSR**（Li et al., 2025）、**FlashVSR**（Zhuang et al., 2025）等处于同一技术脉络，但其独特的冻结骨干+轻量适配器范式显著区别于全量微调或骨干复制方案。



视频超分辨率（VSR）旨在从低质、退化的视频输入中恢复高保真细节。近年来，大规模预训练视频生成模型凭借其强大的先验知识，在生成式 VSR 中展现出卓越的重建能力。然而，如何高效地适配这些大模型到 VSR 任务，已成为制约其实际应用的核心瓶颈。

### 现有适配范式的困境

当前主流的适配方案主要沿两条技术路线展开，但均面临严重的计算效率问题。

**全量微调路线**：以 **DiffVSR**（Li et al., 2025）和 SeedVR 为代表的方法，从低质输入初始化扩散过程并进行全量微调。这类方法虽然能充分利用预训练先验，但训练成本极其高昂——通常需要数十块 GPU 和数百万训练样本，对于大多数研究者和应用场景而言几乎不可承受。

**ControlNet 风格适配路线**：受图像生成领域 ControlNet 的启发，部分方法尝试通过可训练的适配器分支注入条件信号。然而，这一范式在扩散变换器（DiT）架构下暴露出结构性的效率缺陷。如图 2 所示，标准 ControlNet 要求复制整个 DiT 骨干网络作为条件处理分支，导致参数量完全翻倍、内存消耗加倍。根本原因在于，DiT 架构缺乏传统 U-Net 中的编码器-解码器层级结构，无法像在 Stable Diffusion 中那样仅复制编码器部分，而必须整体复制。

上述两条路线的共同困境揭示了一个深层矛盾：**如何在保持预训练生成动力学完整性的前提下，实现轻量级高效适配**——这正是 LiteVSR 试图解决的核心问题。

### 流匹配带来的简化契机

LiteVSR 的关键洞察源于流匹配（Flow Matching）框架的一个独特性质。与扩散模型中学习时变的得分函数不同，流匹配学习的是连接低质分布与目标分布的恒定速度场：

$$\mathcal{L}_{FM} = \mathbb{E}_{t, x_0, x_1} \left[ \| v_\theta(x_t, t, c) - (x_1 - x_0) \|^2 \right]$$

由于目标速度场在整个时间步上保持恒定，条件注入不再需要学习时变的变换——适配器仅需学习一个固定的引导信号，在每个 DiT 块提供相同的注入模式。这一性质从根本上简化了 VSR 适配任务：**条件机制从学习“如何随时间变化”简化为学习“注入什么固定信息”**。

### LiteVSR 的动机定位

基于上述分析，LiteVSR 的动机可以概括为三点：

1. **冻结而非微调**：利用流匹配的恒定速度特性，完全冻结 DiT 骨干网络，避免任何对预训练生成动力学的破坏。
2. **共享而非复制**：通过批量前向传播让噪声状态和条件特征共享同一冻结 DiT 块，从根本上消除 ControlNet 风格的参数复制问题。
3. **状态感知而非静态条件**：设计双流适配器，同时感知低质输入的静态结构线索和中间去噪状态的动态细化需求，实现从结构对齐到纹理细化的自适应引导。

这一设计使得 LiteVSR 能够以仅 11.25% 的可训练参数和单张 A100 GPU 上约 12 小时的训练代价，获得有竞争力的恢复质量（Table 1），将大规模视频生成模型在 VSR 中的适配效率推向了新的边界。



## 核心方法与创新机理

LiteVSR 的核心创新在于利用**流匹配（Flow Matching）的恒定速度场特性**，将视频超分辨率（VSR）的条件适配任务从根本上简化，从而实现了对预训练扩散变换器（DiT）的**完全冻结式轻量级适配**。这一设计打破了现有方案在计算效率与生成质量之间的权衡。

### 1. 流匹配驱动的冻结式适配范式

现有基于大规模预训练视频生成器的 VSR 方法面临严重的计算瓶颈：全量微调方案（如 SeedVR、DiffVSR）需要数十块 GPU 和百万级训练样本；而 ControlNet 风格的适配器在 DiT 架构下，由于缺乏编码器-解码器层级，必须**复制整个骨干网络**来处理条件输入，导致参数量翻倍、内存消耗加倍。

LiteVSR 的关键洞察在于：流匹配学习的是从噪声到干净样本的**恒定速度场** $v_\theta$，该速度场在整个时间步 $t$ 上保持不变。这意味着条件注入不再需要学习时变的复杂变换——适配器仅需为每个 DiT 块提供一个**固定的引导信号**，即可在不破坏预训练生成动力学的前提下实现 VSR。

基于这一洞察，LiteVSR 完全冻结 DiT 骨干，通过**批量处理（batched forward pass）**让噪声状态 $z_t$ 和条件特征共享同一组 DiT 块，仅在各块之间插入轻量级适配器注入引导信号。这与标准 ControlNet 范式形成鲜明对比（Figure 2）：标准方案需复制整个骨干处理条件，而 LiteVSR 以零额外骨干参数实现条件注入。

### 2. State-Aware Adapter：双流结构感知适配器

适配器的设计是 LiteVSR 的另一核心创新。与仅从低质（LQ）输入提取静态条件的现有方案不同，**State-Aware Adapter** 采用双流架构，同时感知：

- **结构流（Structural Stream）**：从 LQ 输入 $z_y$ 提取静态布局和结构线索，提供基础的空间对齐信息。
- **细化流（Refinement Stream）**：从当前去噪状态的干净估计 $\hat{z}_{0,t}$ 提取动态纹理细节，随去噪进程逐步提供高频信息。

两条流通过**时间调制交叉注意力（Time-Modulated Cross-Attention）**进行融合：
$$C_{out} = \mathrm{Attention}(Q_t, [K_{str} \oplus K_{ref}], [V_{str} \oplus V_{ref}])$$

其中可学习的查询 $Q_t$ 受时间步调制，使其能够动态调整对结构流和细化流的关注程度。如 Figure 4 所示，在去噪早期（$t=0.8$），注意力集中于结构流以建立全局布局；随着去噪推进（$t \to 0$），注意力逐渐转向细化流以增强纹理细节。这一机制实现了从**结构对齐到纹理细化**的自适应引导。

### 3. 自适应递归展开策略

训练期间，LiteVSR 采用递归展开（recursive unrolling）来迭代细化干净估计 $\hat{z}_0$：
$$\hat{z}_0^{(k)} = z_t - (1 - t) \cdot v_\theta(z_t, t, \mathcal{A}_\phi(z_y, \hat{z}_0^{(k-1)}, t))$$

为平衡训练效率与细化质量，提出**自适应展开策略（AUS）**，根据时间步动态调整展开步数：
$$M(t) = \left\lfloor 1 + \frac{s \cdot (1 - t)}{1 + (s - 1) \cdot (1 - t)} \cdot (M_{max} - 1) \right\rceil$$

在噪声较大的早期时间步分配较少展开步，而在接近干净样本的后期时间步增加展开步数以精细刻画纹理。消融实验（Table 5）表明，AUS 将 CLIPIQA 从 0.4430 提升至 0.4642。

### 4. 单阶段纯潜在空间训练

与多阶段训练（如 DOVE、FlashVSR 需像素域监督）不同，LiteVSR 采用**单阶段纯潜在空间流匹配训练**，无需任何像素域损失。适配器输出通过**零初始化线性层**注入主分支，确保训练初期不干扰预训练生成动力学，随后逐步学习有效的引导信号。

综上，LiteVSR 通过“冻结骨干 + 流匹配恒定速度场 + 双流状态感知适配器”的组合，实现了仅 **11.25% 可训练参数**、单张 A100 GPU 约 12 小时训练即可获得有竞争力恢复质量的轻量级 VSR 方案（Table 1）。



LiteVSR 的整体架构围绕一个核心设计原则展开：**完全冻结预训练视频生成器的骨干网络，仅通过轻量级适配器注入条件信号**。这一设计根植于流匹配（flow matching）的一个关键性质——目标速度场 $v = x_1 - x_0$ 在整个时间步上保持恒定，使得条件注入不再需要学习时变的变换，适配器只需学习一个固定的引导模式（见 Eq.3—Eq.4）。

### 框架总览

如图 3 所示，LiteVSR 由四个核心模块串联构成：

1. **VAE 编码器/解码器**：将低质视频 $y$ 编码到潜在空间得到 $z_y = \mathcal{E}(y)$，并在推理末端将去噪后的潜在表示解码回像素空间。这一压缩步骤使所有后续计算均在低维潜在空间中进行，显著降低了计算开销。

2. **冻结的扩散变换器骨干（Frozen DiT Backbone）**：基于 Wan2.2-5B 视频生成器，所有 DiT 块参数在训练和推理期间均保持冻结。与 ControlNet 风格适配器（需复制整个骨干网络导致参数量翻倍）不同，LiteVSR 通过**批量前向传播**使噪声状态 $z_t$ 和条件特征共享同一组 DiT 块，从根本上消除了参数重复（见 Figure 2 对比）。

3. **状态感知适配器（State-Aware Adapter）**：这是 LiteVSR 唯一可训练的核心组件，以双流结构接收三类输入——低质潜在表示 $z_y$（静态结构流）、当前干净估计 $\hat{z}_{0,t}$（动态细化流）和时间步 $t$。两流特征通过**时间调制交叉注意力**融合（Eq.5），使适配器能够根据去噪阶段动态平衡结构对齐与纹理细化。

4. **零初始化线性融合层**：在每个 DiT 块处，适配器输出的条件特征通过零初始化线性层投影到主分支。零初始化确保训练初期条件注入为零，不会干扰预训练的生成动力学，随后逐步学习有效的引导信号。

### 数据流与推理过程

一次完整的推理迭代遵循以下数据流：

- **输入**：低质视频 $y$ 经 VAE 编码得到 $z_y$，同时从纯噪声采样初始潜在状态 $z_1 \sim \mathcal{N}(0, I)$。
- **条件生成**：在当前时间步 $t$，适配器 $\mathcal{A}_\phi$ 接收 $z_y$、上一轮估计的干净潜在 $\hat{z}_{0,t}$ 和时间步 $t$，输出条件特征 $c = \mathcal{A}_\phi(z_y, \hat{z}_{0,t}, t)$。
- **速度预测与更新**：冻结的 DiT 骨干以批量方式同时处理噪声状态 $z_t$ 和条件特征 $c$，预测速度场 $v_\theta(z_t, t, c)$，并执行一步去噪更新：$z_{t-\Delta t} = z_t - \Delta t \cdot v_\theta(z_t, t, c)$（Eq.4）。
- **递归细化**：训练期间采用自适应展开策略（Adaptive Unrolling Schedule, AUS），根据时间步动态调整递归步数 $M(t)$（Eq.10），在高噪声阶段（$t \to 1$）使用较少展开步以侧重结构恢复，在低噪声阶段（$t \to 0$）增加展开步以精细纹理。

### 训练范式

LiteVSR 采用**单阶段纯潜在空间流匹配训练**，无需像素域监督或多阶段微调。训练仅使用 REDS 数据集的 266 个片段，在单张 A100 GPU 上约 12 GPU 小时即可收敛，可训练参数仅占扩散骨干的 11.25%（Table 1）。这一高效性源于冻结骨干与轻量适配器的协同设计，使得大规模预训练先验得以完整保留，同时仅需极少数据即可完成领域适配。

需要指出的是，训练数据规模有限（266 个片段），可能影响模型在更广泛退化场景下的泛化能力；当前评估主要依赖合成退化，现实世界退化分布的偏移尚未充分测试。

### 补充图表

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2606_09250/figures/004_Figure_3.jpg]]
*Figure 3: LiteVSR. Left: The overall framework keeps all DiT blocks frozen and injects control signals via zero-initialized linear layers. The State-Aware Adapter processes both the LR latent and the current noisy state to produce conditioning features. Right: The adapter employs dual-stream patch embeddings to extract features from the LR input and the denoising state, which are concatenated as keys and values. A learnable query attends to these features via cross-attention to produce the output. Bottom: Resolution-agnostic query tiling enables inference at arbitrary resolutions by repeating and cropping the learned query prototypes to match the target spatial dimensions*



### 3.1 流匹配与条件注入简化

LiteVSR 的核心洞察源于流匹配（Flow Matching）的动力学特性。标准扩散模型学习时变的噪声/得分函数，条件注入需要学习随 $t$ 变化的变换；而流匹配学习的是恒定速度场 $v(x_t, t, c) = x_1 - x_0$，该目标在整个时间步上保持不变。这一时间一致性将 VSR 适配任务简化为：在每个 DiT 块提供**固定的注入模式**，适配器仅需学习一个固定的引导信号，无需建模时变变换。这为完全冻结 DiT 骨干提供了理论基础。

前向过程将干净潜在 $z_0$ 与噪声 $z_1$ 线性插值：

$$z_t = t z_1 + (1 - t) z_0$$

其中 $t \in [0, 1]$。流匹配损失为：

$$\mathcal{L}_{FM} = \mathbb{E}_{t, z_0, z_1} \left[ \| v_\theta(z_t, t, c) - (z_1 - z_0) \|^2 \right] \tag{3}$$

这里 $v_\theta$ 是冻结的速度预测网络，$c$ 是条件信号。训练时 $z_1$ 从高斯噪声采样，推理时 $z_1 = 0$。

### 3.2 冻结 DiT 骨干与零初始化注入

与 ControlNet 风格适配器（需复制整个 DiT 骨干处理条件，参数量翻倍）不同，LiteVSR 通过**批量前向传播**让 $z_t$ 和条件特征共享同一组冻结的 DiT 块（Figure 2B）。适配器输出通过零初始化线性层注入主分支，避免干扰预训练生成动力学。

单步去噪更新为：

$$z_{t - \Delta t} = z_t - \Delta t \cdot v_\theta(z_t, t, \mathcal{A}_\phi(z_y, \hat{z}_{0,t}, t)) \tag{4}$$

其中 $\mathcal{A}_\phi$ 是 State-Aware Adapter，$z_y$ 是低质潜在，$\hat{z}_{0,t}$ 是当前干净估计。

### 3.3 State-Aware Adapter：双流结构与时间调制交叉注意力

适配器接收三个输入（Figure 3 右）：

- **低质潜在** $z_y = \mathcal{E}(y)$：提供静态结构线索
- **预测干净估计** $\hat{z}_{0,t}$：提供动态细化信号
- **时间步** $t$：调制融合权重

双流处理流程：

1. **结构流**：从 $z_y$ 提取静态布局特征 $K_{str}, V_{str}$
2. **细化流**：从 $\hat{z}_{0,t}$ 提取动态细节特征 $K_{ref}, V_{ref}$
3. **时间调制交叉注意力**融合两流：

$$C_{out} = \text{Attention}(Q_t, [K_{str} \oplus K_{ref}], [V_{str} \oplus V_{ref}]) \tag{5}$$

其中 $Q_t$ 是可学习查询原型，$t$ 调制注意力权重，使早期去噪步侧重结构对齐，后期侧重纹理细化（Figure 4 验证了这一转移）。

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2606_09250/figures/005_Figure_4.jpg]]
*Figure 4: Attention maps illustrating the shift of focus across timesteps*

### 3.4 递归细化与自适应展开策略

训练时采用 $M$ 步递归展开生成精细化条件：

$$\hat{z}_0^{(k)} = z_t - (1 - t) \cdot v_\theta(z_t, t, \mathcal{A}_\phi(z_y, \hat{z}_0^{(k-1)}, t)) \tag{9}$$

初始 $\hat{z}_0^{(0)} = z_y$，最终条件 $c_{ref} = \mathcal{A}_\phi(z_y, \hat{z}_0^{(M(t)-1)}, t)$。

展开步数 $M(t)$ 通过自适应调度函数确定，在 $t \to 0$（高信噪比）时增加步数以获得更精确的干净估计：

$$M(t) = \left\lfloor 1 + \frac{s \cdot (1 - t)}{1 + (s - 1) \cdot (1 - t)} \cdot (M_{max} - 1) \right\rceil \tag{10}$$

其中 $s=5$ 控制曲率，$M_{max}$ 为最大展开步数。消融实验（Table 5）表明该策略将 CLIPIQA 从 0.4430 提升至 0.4642。

### 3.5 训练目标

最终损失为加权流匹配损失，权重 $\lambda(t) = \sigma_t^{-2}$ 优先高信噪比时间步：

$$\mathcal{L} = \mathbb{E}_{t, z_0, z_1} \left[ \lambda(t) \left\| v_\theta(z_t, t, c_{ref}) - (z_1 - z_0) \right\|^2 \right] \tag{11}$$

训练完全在潜在空间进行，无需像素域监督，采用单阶段流程。

### 补充图表

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2606_09250/figures/003_Figure_2.jpg]]
*Figure 2: ControlNet paradigms for DiT. (A) Standard Control-Net duplicates the backbone for condition processing. (B) Our approach shares frozen DiT blocks via batch processing, requiring only a lightweight adapter*



## 实验与关键发现

### 训练效率对比

LiteVSR 的核心设计目标是在保持预训练生成先验的前提下，大幅降低视频超分辨率（VSR）适配的计算开销。Table 1 给出了与代表性方法的训练效率对比。LiteVSR 仅使用 REDS 数据集的 266 个训练片段，在单张 A100 GPU 上训练约 6K 次迭代（约 12 GPU 小时），扩散骨干中可训练参数仅占 11.25%。相比之下，基于 LQ 初始化的全量微调方法（如 **SeedVR** 和 **DiffVSR**）需要数十块 GPU 和数百万训练样本，训练成本高出数个数量级；ControlNet 风格的适配器在 DiT 架构下因缺乏编码器-解码器层级而必须复制整个骨干网络，导致参数量翻倍。LiteVSR 通过冻结 DiT 骨干并以零初始化线性层注入适配器特征，从根本上规避了参数复制问题。

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2606_09250/figures/002_Table_1.jpg]]
*Table 1: Training efficiency comparison. Percentages indicate trainable parameters within the diffusion backbone; additional finetuned VAE components are listed separately*

### 合成与真实场景定量评估

Table 2 报告了在五个基准上的全指标对比。在合成退化场景下，LiteVSR 在感知质量指标上表现突出：

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2606_09250/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison on REDS4, UDM10, SPMCS, YouHQ40 (synthetic), and VideoLQ (real-world). Best results are in bold; second-best are underlined*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2606_09250/figures/011_Table_5.jpg]]
*Table 5: Ablation studies on VideoLQ. We evaluate sampling steps, query window size, injection layer rank, and the adaptive unrolling strategy (AUS). Checkmarks (✓) indicate the default settings used in Table 2*

- **REDS4**：CLIPIQA 达到 0.3748，较第二名 FlashVSR（0.3186）提升 0.0562；DOVER 和 MUSIQ 同样取得最优或次优。
- **UDM10**：DOVER 达到 0.515，较 FlashVSR（0.4618）提升 0.0532，CLIPIQA 和 MUSIQ 也保持领先。
- **SPMCS**：MUSIQ 达到 70.42，与 FlashVSR（70.33）持平。

在真实世界退化场景 **VideoLQ** 上，LiteVSR 在 CLIPIQA、DOVER 和 MUSIQ 三项无参考感知指标上均取得最优，表明其生成结果在纹理自然度和视觉保真度方面优于现有方法。需要注意的是，在 PSNR、LPIPS 等像素级保真度指标上，LiteVSR 通常不占优势——这是生成式 VSR 方法的共性特征：生成模型倾向于产生感知上更真实但像素级偏差较大的结果。

### 用户主观偏好研究

Table 3 的用户研究进一步验证了定量结果。在包含 17 个序列的整体评估中，LiteVSR 在“整体质量”“清晰度”和“自然度”三个维度上均获得最高偏好比例。按输入视频质量分场景的细分显示，LiteVSR 在不同退化程度下均保持一致的偏好优势，说明其生成结果对不同质量的低质输入具有鲁棒性。

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2606_09250/figures/008_Table_3.jpg]]
*Table 3: User study results. The Overall block aggregates across all 17 sequences with three evaluation metrics; the per-scenario block breaks down overall preference by input video quality. Values indicate the percentage of participants preferring each method*

### 消融实验

#### 双流适配器设计

Table 4 在 VideoLQ 上对 State-Aware Adapter 的双流结构进行了消融。完整模型（结构流 + 细化流 + 时间调制）在 CLIPIQA 上达到 0.4642。移除时间调制后，性能显著下降至 0.4292，验证了时间调制交叉注意力在动态平衡结构对齐与纹理细化中的关键作用。单独使用结构流或细化流均导致不同程度的性能退化，表明静态结构线索和动态去噪状态信息的互补性。

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2606_09250/figures/009_Table_4.jpg]]
*Table 4: Ablation on the dual-stream adapter design (evaluated on VideoLQ)*

#### 自适应展开策略与秩选择

Table 5 报告了采样步数、查询窗口大小、注入层秩和自适应展开策略（AUS）的消融结果。AUS 将 CLIPIQA 从 0.4430 提升至 0.4642，证实了根据时间步自适应调整展开深度的重要性——在去噪后期（$t \to 0$）增加展开步数能更准确地估计干净潜在表示，从而提供更精确的细化信号。此外，使用 LoRA-128 将可训练参数从 634M 降至 375M（降低 40.9%），性能保持可比甚至更优，表明适配器设计具有较高的参数效率冗余。

### 注意力机制可视化

Figure 4 展示了不同时间步下结构流和细化流的注意力图。在去噪早期（$t = 0.8$），注意力主要集中于结构流，适配器从低质输入中提取布局和结构信息；随着去噪推进（$t = 0.5, 0.2$），注意力逐渐向细化流转移，模型更多依赖当前干净估计来引导纹理细化。这一动态转移机制是 State-Aware Adapter 能够同时保证结构保真度和纹理自然度的内在原因。

### 失败模式与局限性

Figure 7 揭示了生成式 VSR 方法在文字重建上的共性局限。在严重退化下，所有对比方法（包括 LiteVSR）均无法忠实恢复文字内容，往往生成看似合理但实际错误的字符。这是因为扩散模型的生成先验倾向于产生视觉上连贯的纹理，但缺乏对文字语义的精确约束。该问题指向一个开放方向：如何整合 OCR 引导的约束或文字感知模块，以改进生成式 VSR 在文字区域的保真度。

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2606_09250/figures/014_Figure_7.jpg]]
*Figure 7: Limitation of generative VSR methods on text reconstruction. All methods, including ours, struggle to faithfully restore text content under degradation, often generating plausible but incorrect characters*

### 训练细节与超参数

Table 6 汇总了实现细节和关键超参数。LiteVSR 采用单阶段纯潜在空间流匹配训练，无任何像素域损失。训练目标为加权流匹配损失（Eq. 11），权重函数 $\lambda(t) = \sigma_t^{-2}$ 优先关注高信噪比的时间步。自适应展开调度（Eq. 10）中 $s = 5$，$M_{max}$ 控制最大展开步数。这些设计使得 LiteVSR 能够在不破坏预训练生成动力学的前提下，以极少的训练开销实现有竞争力的 VSR 质量。

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2606_09250/figures/012_Table_6.jpg]]
*Table 6: Implementation details and hyperparameters*

### 补充图表

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2606_09250/figures/010_Figure_6.jpg]]
*Figure 6: Visual comparison on high-density detail regions (greenery and hair)*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2606_09250/figures/001_Figure_1.jpg]]
*Figure 1: Visual comparisons of LiteVSR with SOTA methods (Zoom-in for best view)*



## 定位与知识库关联

### 1. 与现有工作的关系

LiteVSR 处于**生成式视频超分辨率（Generative VSR）**与**大规模扩散模型高效适配**两条技术路线的交汇点上。其最直接的参照系是两类工作：

**（1）基于扩散模型的 VSR 方法。** 近年来，扩散模型在 VSR 领域展现出强大的纹理生成能力，但计算代价极高。**Upscale-A-Video**（Zhou et al., CVPR 2024）在图像扩散模型上插入时间模块实现 VSR；**MGLD-VSR**（Yang et al., 2024）引入运动引导的潜在扩散；**STAR**（Xie et al., 2025）利用文本-视频模型进行时空增强；**DiffVSR**（Li et al., 2025）通过渐进式学习处理复杂退化。这些方法均需对预训练骨干进行大量微调或适配，训练成本居高不下。而 **FlashVSR**（Zhuang et al., 2025）和 **DOVE**（Chen et al., 2025）虽通过一步蒸馏降低推理成本，但训练仍需多阶段像素域监督，未能从根本上解决训练效率问题。

**（2）ControlNet 风格的条件注入范式。** 在扩散变换器（DiT）架构下，标准 ControlNet 需要复制整个骨干网络用于条件处理，导致参数量翻倍和内存消耗加倍（见 Figure 2A）。LiteVSR 的关键突破在于利用了流匹配（Flow Matching）的恒定速度场特性——目标速度场 $v = x_1 - x_0$ 在整个时间步上保持不变，这意味着条件注入不再需要学习时变的变换，适配器仅需学习一个固定的引导信号。基于这一洞察，LiteVSR 完全冻结 DiT 骨干，通过批量前向传播共享冻结块，仅用轻量级适配器注入条件信号（见 Figure 2B），从根本上消除了参数复制问题。

### 2. 核心差异与适用边界

LiteVSR 与现有方法存在三个结构性差异：

- **条件注入架构**：从“复制骨干”转向“共享冻结块 + 零初始化注入”，可训练参数仅占扩散骨干的 11.25%。
- **适配器设计**：State-Aware Adapter 同时接收低质输入的静态结构流和中间去噪状态的动态细化流，通过时间调制交叉注意力实现从结构对齐到纹理细化的自适应引导，而非仅依赖静态条件。
- **训练范式**：单阶段纯潜在空间流匹配训练，无需像素域损失，训练仅需 266 个 REDS 片段和约 12 GPU 小时（单张 A100）。

**适用边界**：LiteVSR 的设计强依赖于流匹配框架的恒定速度场特性，因此其轻量级适配策略无法直接迁移到标准扩散模型（DDPM/DDIM）上。此外，该方法使用冻结的 Wan2.2-5B 视频生成器作为骨干，其生成先验主要来自通用视频数据，对于特定领域（如医学影像、遥感）的退化分布可能需要额外的领域适配。

### 3. 局限与开放问题

**已知局限**：论文明确指出，LiteVSR 与其他生成式 VSR 方法一样，无法忠实重建视频中的文字内容——在严重退化下往往生成看似合理但实际错误的字符（见 Figure 7）。这一局限源于生成式方法本质上是在学习数据分布而非精确恢复信号，对于需要严格保真度的结构化内容（文字、符号、精细几何图案）存在固有缺陷。

**开放问题**：

1. **文字保真度改进**：如何整合 OCR 引导的约束或文字感知模块，在保持生成质量的同时提升文字区域的还原准确性？
2. **数据规模与泛化**：当前训练仅使用 REDS 的 266 个片段，评估主要依赖合成退化，模型在更广泛真实世界退化分布下的泛化能力尚待验证。
3. **骨干替换的灵活性**：该方法对 Wan2.2-5B 的冻结策略是否可平滑迁移到其他 DiT 架构（如 Sora 类模型），仍需实验验证。
4. **推理效率**：虽然训练成本极低，但推理仍需多步采样，能否与蒸馏策略（如 FlashVSR 的一步蒸馏）结合以进一步降低推理延迟，是实用化部署的关键问题。



## 原文 PDF

![[paperPDFs/ICML_2026/LiteVSR_Lightweight_Adaptation_of_Frozen_Diffusion_Transformers_for_Video_Super-Resolution.pdf]]
