---
title: "LaS-Comp: Zero-shot 3D Completion with Latent-Spatial Consistency"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LaS_Comp_Zero_shot_3D_Completion_with_Latent_Spatial_Consistency.pdf
project_link: null
code_link: null
aliases:
- LC
- LaS-Comp
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 显式空间替换（ERS）结合部分感知噪声调度（PNS），通过在几何空间直接注入观测信息并差异化控制观察与缺失区域的噪声幅度，弥合潜在-空间域差距。
primary_logic: 通过两阶段协同设计——显式空间替换保证对部分输入的保真度，隐式对齐阶段（IAS）以单步梯度优化潜在特征消除边界伪影——高效释放预训练3D基础模型的几何先验，实现无需训练、类别无关的零样本补全。
claims:
- 即使部分输入与完整形状共享相同的表面几何，它们在VAE潜在空间中对应区域的编码相似度极低（平均余弦相似度仅0.4593），导致无法直接在潜在空间进行条件补全。
- LaS-Comp在Redwood数据集上比ComPC降低CD 27.2%、EMD 29.0%，比GenPC降低CD 18.4%、EMD 36.1%；在Omni-Comp上平均降低CD 49.6%、EMD 39.4%，达到SOTA。
- "消融实验证实，移除显式替换阶段（ERS）导致性能下降最为严重（Redwood: CD 3.42 vs 1.42），证明空间替换对保真度至关重要。"
- 方法完全无需训练，兼容不同3D基础模型，单个形状补全仅需20秒，比现有零样本方法快3倍以上。
---

# LaS-Comp: Zero-shot 3D Completion with Latent-Spatial Consistency

> [!tip] 核心洞察
> 通过两阶段协同设计——显式空间替换保证对部分输入的保真度，隐式对齐阶段（IAS）以单步梯度优化潜在特征消除边界伪影——高效释放预训练3D基础模型的几何先验，实现无需训练、类别无关的零样本补全。

| 字段 | 内容 |
|------|------|
| 中文题名 | LaS-Comp：基于潜在-空间一致性的零样本三维补全 |
| 英文题名 | LaS-Comp: Zero-shot 3D Completion with Latent-Spatial Consistency |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.18735) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | LaS-Comp |
| Dataset | Redwood, Synthetic, Omni-Comp, ScanNet & KITTI |

> [!tip] 效果简介
> - Redwood (real scans) 上，CD (×10²)↓ / EMD (×10²)↓ 1.42 / 1.84 (Ours TRELLIS) vs ComPC: 1.95 / 2.59, GenPC: 1.74 / 2.88 (27.2% CD↓ over ComPC, 18.4% CD↓ over GenPC)。
> - Synthetic (virtual scans) 上，CD (×10²)↓ / EMD (×10²)↓ 1.11 / 1.41 (Ours TRELLIS) vs ComPC: 1.61 / 2.09 (31.1% CD↓ over ComPC)。
> - Omni-Comp (multi-pattern) 上，CD ↓ / EMD ↓ improvement 49.6% CD, 39.4% EMD over ComPC vs ComPC (49.6% CD↓)。

## 概述

三维形状补全是计算机视觉与图形学中的基础任务，旨在从部分观测中恢复完整几何形状。现有方法大致可分为三类：监督方法（如 **SVDFormer** (Zhu et al., ICCV 2023)、**AdaPoinTr** (Yu et al., TPAMI 2023)）依赖大规模配对数据训练，泛化能力受限；自监督/无监督方法（如 **Shape-Inv** (Zhang et al., CVPR 2021)、**P2C** (Cui et al., ICCV 2023)）无需配对真值，但仍需针对特定类别进行训练；零样本方法（如 **SDS-Comp** (Kasten et al., NeurIPS 2023)、**ComPC** (Huang et al., ICLR 2025)、**GenPC** (Li et al., CVPR 2025)）借助2D扩散先验或3D生成先验，可在未见类别上完成补全，但存在根本性瓶颈。

**核心瓶颈**在于：现代3D基础模型采用潜在-生成式架构（VAE编码器-解码器 + 流匹配生成器），部分输入与完整形状在潜在空间中存在显著的域间隙（latent gap）。实验表明，即使部分输入与完整形状在观察区域共享完全相同的表面几何，它们在VAE潜在空间中对应区域的编码平均余弦相似度仅为0.4593（见补充材料Figure 9）。这意味着直接从潜在空间进行条件补全是不可靠的——这正是现有基于潜在空间操作的方法性能受限的深层原因。另一方面，基于2D渲染先验的方法（如SDS-Comp、ComPC）无法有效处理所有视角均不完整的部分观测场景。

**核心方法**：本文提出 **LaS-Comp**，一种无需训练、类别无关的零样本3D补全框架。其核心洞察是通过两阶段协同设计，高效释放预训练3D基础模型的几何先验：**显式空间替换阶段（Explicit Replacement Stage, ERS）** 在几何空间直接注入观测信息，弥合潜在-空间域差距；**隐式对齐阶段（Implicit Alignment Stage, IAS）** 通过单步梯度优化潜在特征消除边界伪影。框架完全无需训练，可即插即用于任意潜在-生成式3D基础模型（如TRELLIS、Direct3D-S2），单个形状补全仅需约20秒，比现有零样本方法快3倍以上。

**主要结果**：在Redwood真实扫描数据集上，LaS-Comp相比ComPC降低倒角距离（CD）27.2%、降低推土机距离（EMD）29.0%；相比GenPC降低CD 18.4%、EMD 36.1%。在合成数据集上，相比ComPC降低CD 31.1%。在涵盖多种缺失模式的Omni-Comp基准上，平均降低CD 49.6%、EMD 39.4%。在ScanNet和KITTI真实场景扫描上，保真度指标（UCD）平均提升约38%。消融实验证实，移除显式替换阶段（ERS）导致性能下降最为严重（Redwood CD从1.42升至3.42），证明空间替换对保真度至关重要。

## 背景与动机

### 问题背景

三维形状补全（3D shape completion）旨在从部分观测中恢复完整的几何形状，是计算机视觉与图形学中的基础性任务。真实世界采集的三维数据——无论是深度传感器扫描、激光雷达点云还是多视图重建——几乎不可避免地存在遮挡、稀疏采样或语义缺失，因此补全技术对于下游应用（如机器人抓取、自动驾驶场景理解、AR/VR 内容生成）具有关键支撑作用。

近年来，3D 生成基础模型取得了显著进展。以 TRELLIS 和 Direct3D-S2 为代表的潜在-生成式架构（latent-generative architecture）能够在紧凑的潜在空间中学习丰富的几何先验，并通过对潜在特征的迭代去噪生成高质量的三维形状。这类模型天然具备类别无关（category-agnostic）的生成能力，为零样本补全提供了极具吸引力的基础。

### 现有方法缺口

尽管 3D 基础模型潜力巨大，将其直接应用于补全任务却面临根本性障碍。现有方法大致分为两条技术路线，各有难以克服的局限：

**潜在空间补全的域间隙。** 最直观的思路是在潜在空间中对部分输入进行条件生成——将部分形状编码为潜在特征，再引导去噪过程补全缺失区域。然而，实验证据表明，即使部分输入与完整形状在观察区域共享完全相同的表面几何，它们在 VAE 潜在空间中对应区域的编码相似度仍然极低：平均余弦相似度仅为 0.4593（Supp. Figure 9）。这一“潜在域间隙”（latent gap）意味着直接从潜在空间进行条件补全本质上不可靠，生成结果难以忠实保留输入几何。

**2D 先验方法的视角盲区。** 另一条路线借助 2D 扩散模型的强大先验，通过多视图渲染将 2D 生成结果蒸馏为 3D 形状。代表性方法包括 **SDS-Comp**（Kasten et al., NeurIPS 2023）、**ComPC**（Huang et al., ICLR 2025）和 **PCDreamer**（Wei et al., CVPR 2025）。这类方法的致命缺陷在于：它们依赖可见视角的渲染信息来引导补全，当部分观测本身在所有视角下都不完整时（例如物体背面完全缺失），2D 先验便失去了有效的条件信号，补全质量急剧退化。

**监督方法的泛化瓶颈。** 传统的监督式补全方法（如 **SVDFormer** (Zhu et al., ICCV 2023)、**AdaPoinTr** (Yu et al., TPAMI 2023)）需要大规模配对数据训练，且通常局限于特定类别，难以泛化到开放世界的任意形状。无监督方法（如 **Shape-Inv** (Zhang et al., CVPR 2021)）和自监督方法（如 **P2C** (Cui et al., ICCV 2023)）虽降低了对标注的依赖，但仍需在目标数据分布上进行训练，无法实现真正的零样本部署。

### 核心研究动机

上述分析揭示了当前零样本补全的核心瓶颈：**3D 基础模型拥有强大的几何先验，但缺乏将部分观测可靠注入生成过程的机制；2D 方法拥有灵活的扩散先验，但缺乏对全局三维结构的理解。** 这种“潜在-空间”域间隙构成了释放预训练 3D 模型补全能力的关键障碍。

本文的动机由此清晰：**能否设计一种无需训练、即插即用的条件机制，在几何空间而非潜在空间注入部分观测信息，从而弥合域间隙，高效释放 3D 基础模型内在的补全能力？** 这一思路若能实现，将同时获得两类方法的优势——3D 模型的全局几何一致性与几何空间注入的输入保真度——同时规避各自的根本缺陷。

## 核心创新

LaS-Comp 的核心创新在于**首次系统性地诊断并弥合了3D基础模型的潜在-空间域间隙**，并基于此设计了一套**无需训练、即插即用的两阶段补全范式**。与现有方法相比，其关键改变体现在以下四个维度：

### 1. 补全域：从“潜在空间条件生成”到“几何空间显式注入”

**瓶颈诊断**：现有基于3D生成先验的零样本方法（如 **GenPC**（Li et al., CVPR 2025）、**ComPC**（Huang et al., ICLR 2025））试图直接在VAE潜在空间中进行条件补全。然而，LaS-Comp 揭示了一个根本性问题——即使部分输入与完整形状在观察区域共享完全相同的表面几何，它们在潜在空间中的编码相似度极低（平均余弦相似度仅 **0.4593**）。这一“潜在间隙”使得直接在潜在空间进行条件生成从根本上不可靠。

**创新方案**：LaS-Comp 将补全的主战场从潜在空间转移至**几何空间**。其核心操作是**显式空间替换（Explicit Replacement Stage, ERS）**——在每一步去噪迭代中，将解码后的生成形状在观察区域直接替换为部分输入的几何信息（$S_{0|t}' = S_p \odot M + S_{0|t} \odot (1 - M)$），再将替换后的形状重新编码回潜在空间。这一设计保证了补全结果对部分输入的**严格几何保真度**，从根本上规避了潜在空间的不可靠性。

### 2. 去噪调度：从“均匀随机扰动”到“部分感知噪声调度（PNS）”

**基线做法**：传统扩散/流匹配模型在去噪过程中对所有空间区域施加相同的随机噪声扰动，不区分观察区域与缺失区域。

**创新方案**：LaS-Comp 提出**部分感知噪声调度（Partial-aware Noise Schedule, PNS）**，对两类区域施加差异化处理：
- **观察区域**（$M=1$）：使用时间依赖的预测-噪声混合 $\sqrt{1-t} \cdot \hat{\pmb{x}}_{1|t} + \sqrt{t} \cdot \pmb{\epsilon}_1$，随去噪进程逐步衰减噪声幅度，保证与部分输入的一致性；
- **缺失区域**（$M=0$）：直接替换为纯高斯噪声 $\pmb{\epsilon}_2$，最大化生成多样性。

消融实验证实，移除 PNS 会导致明显的条纹状伪影（Redwood CD 从 1.42 升至 1.94），验证了差异化噪声调度对生成质量的关键作用。

### 3. 边界一致性：从“无专门处理”到“隐式对齐阶段（IAS）”

**问题定位**：ERS 在几何空间进行硬性替换后，重新编码的潜在特征在观察区域与缺失区域的边界处会产生**潜在空间的不连续性**，解码后表现为边界空洞、断裂等伪影。

**创新方案**：LaS-Comp 引入**隐式对齐阶段（Implicit Alignment Stage, IAS）**。该阶段在潜在空间计算一个轻量的几何对齐损失——在掩码区域计算预测占用与部分输入的二元交叉熵 $\mathcal{L}_{\mathrm{align}} = \mathrm{BCE}(S_{0|t} \odot M, S_p \odot M)$——并通过**单步梯度更新**优化潜在特征（学习率 $\eta = 1 \times 10^{-5}$）。这一设计以极小的计算代价平滑了边界区域的不连续性。消融实验表明，移除 IAS 会导致边界空洞和不一致（Redwood CD 从 1.42 升至 1.88）。

### 4. 模型依赖：从“特定架构训练”到“零样本即插即用”

**范式转变**：LaS-Comp 完全无需训练，不依赖任何配对数据或特定架构。其两阶段设计（ERS + IAS）作为通用插件，可无缝适配任意潜在-生成式3D基础模型（论文中验证了 **TRELLIS** 和 **Direct3D-S2** 两个不同架构）。单个形状补全仅需约 **20秒**，比现有零样本方法快 **3倍以上**。

### 创新总结

上述四个改变槽位构成了一个**因果协同系统**：ERS 解决“保真度”问题（几何空间显式替换），PNS 解决“多样性”问题（差异化噪声调度），IAS 解决“一致性”问题（潜在空间隐式对齐），三者共同释放了预训练3D基础模型的几何先验，实现了无需训练的类别无关零样本补全。消融实验的定量证据表明，这一协同设计是不可分割的——移除任一模块均导致性能显著退化，其中 ERS 的移除影响最为严重（Redwood CD 从 1.42 升至 3.42），验证了“空间替换”作为核心创新支柱的地位。

## 整体框架

LaS-Comp 是一个**训练无关**（training-free）的两阶段迭代框架，旨在弥合部分观测与完整形状在预训练 3D 基础模型潜在空间中的域间隙。其核心发现是：即使部分输入与真值在几何空间共享相同的表面区域，二者在 VAE 潜在空间中的对应编码相似度极低（平均余弦相似度仅 0.4593），因此直接从潜在空间进行条件补全不可靠（Figure 9）。LaS-Comp 通过**显式空间替换**与**隐式对齐**的协同设计，在不修改模型权重的前提下，将部分输入的几何信息注入生成过程，释放预训练模型的几何先验。

### Pipeline 总览

框架从高斯噪声 $x_T \sim \mathcal{N}(0, I)$ 初始化潜在特征，在流匹配（flow-matching）框架下沿时间轴 $t: 1 \to 0$ 迭代去噪。每个时间步 $t$ 执行两个阶段（Figure 2）：

![[assets/figures/papers/paper_list_l2532_https_arxiv_org_abs_2602_18735/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the LaS-Comp framework. Starting from Gaussian noise, the process iteratively refines a latent feature xt under the guidance of the partial input*

1. **显式替换阶段（Explicit Replacement Stage, ERS）**：将部分输入 $S_p$ 的几何信息显式注入当前潜在状态 $x_t$，生成融合了观测约束的中间潜在 $x_t^*$。
2. **隐式对齐阶段（Implicit Alignment Stage, IAS）**：在 ERS 输出基础上，通过单步梯度优化消除观察区域与生成区域之间的边界伪影，得到对齐后的潜在 $x_{t-dt}$，作为下一时间步的输入。

最终，将 $t=0$ 时的潜在 $x_0$ 解码为完整形状 $S_c = \mathcal{D}(x_0)$，再通过 Marching Cubes 提取网格或采样点云。

### 输入输出与模块关系

- **输入**：部分观测形状 $S_p$（点云或占用网格）及其对应的二值掩码 $M$（标记已知/缺失区域）。
- **预训练模块**（冻结，不参与训练）：编码器 $\mathcal{E}$、解码器 $\mathcal{D}$、流匹配速度场生成器 $\mathcal{G}$。论文基于 **TRELLIS** 和 **Direct3D-S2** 两个 3D 基础模型实现，验证了方法的即插即用兼容性。
- **输出**：完整形状 $S_c$，支持无条件补全与文本引导补全两种模式。

### 关键设计动机

ERS 将生成过程分解为**清洁分支**（保证对部分输入的保真度）与**噪声分支**（为缺失区域提供多样性），并通过**部分感知噪声调度（PNS）** 对观察区域施加时间依赖的衰减扰动、对缺失区域注入纯高斯噪声，从而在保真度与多样性之间取得平衡。IAS 则通过计算掩码区域内的几何对齐损失 $\mathcal{L}_{\mathrm{align}} = \mathrm{BCE}(S_{0|t} \odot M, S_p \odot M)$ 并执行单步梯度更新（学习率 $\eta = 1 \times 10^{-5}$），消除 ERS 在观察/缺失边界处可能引入的不一致性。

消融实验证实了这一两阶段设计的必要性：移除 ERS 导致性能下降最为严重（Redwood 上 CD 从 1.42 升至 3.42），移除 PNS 产生明显的条纹状伪影，移除 IAS 则导致边界空洞和不一致（Table 6, Figure 8）。

### 效率特性

整个流程完全无需训练，单个形状补全仅需约 20 秒，比现有零样本方法（如 **ComPC**, Huang et al., ICLR 2025）快 3 倍以上。框架兼容不同的潜在-生成式 3D 基础模型，无需针对特定架构或类别进行适配。

### 补充图表

![[assets/figures/papers/paper_list_l2532_https_arxiv_org_abs_2602_18735/figures/001_Figure_1.jpg]]
*Figure 1: Our new framework supports category-agnostic shape completion across diverse partial patterns, including (a) random crops, (b) single-view scans, and (c) missing semantic parts. It further supports both unconditional and text-guided completion, offering flexible control for real-world applications, see (d)*

## 核心模块与公式推导

### 问题背景：潜在空间域间隙

LaS-Comp 的核心设计动机源于对 3D 基础模型潜在空间特性的实证观察：即使部分输入 $S_p$ 与完整形状 $S_{gt}$ 在观察区域共享相同的表面几何，它们在 VAE 潜在空间中对应区域的编码相似度极低——平均余弦相似度仅 **0.4593**（见 Supplementary Figure 9, Sec. 6）。这一“潜在间隙”（latent gap）意味着，直接在潜在空间对部分输入进行条件生成是不可靠的，必须寻找弥合该间隙的机制。

![[assets/figures/papers/paper_list_l2532_https_arxiv_org_abs_2602_18735/figures/016_Figure_9.jpg]]
*Figure 9: Illustration of the latent gap between the partial input*

### 框架总览：两阶段迭代精炼

LaS-Comp 从高斯噪声出发，在每个去噪时间步 $t$ 执行两阶段协同设计（见 Figure 2）：

1. **显式替换阶段（Explicit Replacement Stage, ERS）**：在几何空间直接注入部分输入的观测信息，生成保真度强化的潜在状态 $\pmb{x}_t^*$。
2. **隐式对齐阶段（Implicit Alignment Stage, IAS）**：基于几何对齐损失对潜在特征进行单步梯度优化，消除 ERS 引入的边界伪影，得到对齐后的潜在状态 $\pmb{x}_{t-dt}$。

整个过程完全无需训练，可即插即用于任意潜在-生成式 3D 基础模型（如 **TRELLIS** 和 **Direct3D-S2**）。

---

### 显式替换阶段（ERS）

ERS 在每个时间步将生成过程分解为两个并行分支（见 Figure 3）：

![[assets/figures/papers/paper_list_l2532_https_arxiv_org_abs_2602_18735/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the Explicit Replacement Stage (ERS). At each timestep t, ERS decomposes the latent generation into two parallel branches. The clean branch (top) enforces spatial consistency, yielding*

**清洁分支（Clean Branch）**——负责保真度：

1. 利用 3D 基础模型的生成器 $\mathcal{G}$ 估计当前时间步的噪声自由潜在特征：
   $$\hat{\pmb{x}}_{0 \mid t} = \pmb{x}_t - t \cdot \mathcal{G}(\pmb{x}_t, t) \tag{1}$$
   其中 $\mathcal{G}$ 预测流匹配（flow-matching）的速度场，$\pmb{x}_t$ 为当前时间步的潜在状态。

2. 通过解码器 $\mathcal{D}$ 将估计的噪声自由潜在解码为完整形状占用网格：
   $$S_{0|t} = \mathcal{D}(\hat{\pmb{x}}_{0|t}) \tag{2}$$

3. 使用二值掩码 $M$（观察区域为 1，缺失区域为 0）执行**显式空间替换**，将部分输入的已知几何直接注入生成预测：
   $$S_{0|t}' = S_p \odot M + S_{0|t} \odot (1 - M) \tag{3}$$
   随后通过编码器 $\mathcal{E}$ 将替换后的形状重新编码回潜在空间：$\pmb{x}_{0|t}^* = \mathcal{E}(S_{0|t}')$。

**噪声分支（Noisy Branch）**——负责多样性：

采用**部分感知噪声调度（Partial-aware Noise Scheduling, PNS）**，对观察区域与缺失区域施加差异化扰动：
$$\pmb{x}_{1|t}^{*} = M \odot \left( \sqrt{1 - t} \cdot \hat{\pmb{x}}_{1|t} + \sqrt{t} \cdot \pmb{\epsilon}_1 \right) + (1 - M) \odot \pmb{\epsilon}_2 \tag{6}$$

关键设计：
- **观察区域**（$M=1$）：使用时间依赖的预测-噪声混合，系数 $\sqrt{1-t}$ 随去噪进程逐渐衰减扰动，确保观测几何的稳定性。
- **缺失区域**（$M=0$）：替换为纯高斯噪声 $\pmb{\epsilon}_2$，最大化生成多样性。

**分支融合**：将清洁分支输出 $\pmb{x}_{0|t}^*$ 与噪声分支输出 $\pmb{x}_{1|t}^*$ 按流匹配时间插值，合成融合了部分输入几何的当前潜在状态：
$$\pmb{x}_t^* = (1 - t) \cdot \pmb{x}_{0|t}^* + t \cdot \pmb{x}_{1|t}^* \tag{7}$$

---

### 隐式对齐阶段（IAS）

ERS 的空间替换操作虽保证了输入保真度，但可能在观察区域与生成区域的边界引入不一致性。IAS 通过几何对齐损失对潜在特征进行单步梯度优化来解决这一问题。

首先，从 ERS 输出 $\pmb{x}_t^*$ 重新估计噪声自由潜在：
$$\hat{\pmb{x}}_{0|t} = \pmb{x}_t^* - t \cdot \mathcal{G}(\pmb{x}_t^*, t) \tag{8}$$

解码为形状后，在掩码区域计算预测占用与部分输入的二元交叉熵损失：
$$\mathcal{L}_{\text{align}} = \text{BCE}(S_{0|t} \odot M, S_p \odot M) \tag{10}$$

对潜在特征执行**单步梯度更新**（学习率 $\eta = 1 \times 10^{-5}$）：
$$\pmb{x}_{0|t}^{\text{aligned}} = \hat{\pmb{x}}_{0|t} - \eta \cdot \nabla_{\hat{\pmb{x}}_{0|t}} \mathcal{L}_{\text{align}} \tag{11}$$

最后，通过流匹配逆向步骤获得下一时间步的潜在状态：
$$\pmb{x}_{t-dt} = \pmb{x}_{0|t}^{\text{aligned}} + (t - dt) \cdot \mathcal{G}(\pmb{x}_{0|t}^{\text{aligned}}, t) \tag{12}$$

---

### 设计要点总结

| 模块 | 核心机制 | 解决的关键问题 |
|------|---------|---------------|
| 清洁分支 + 空间替换 | 在几何空间直接注入 $S_p$，经编解码器闭环 | 弥合潜在空间域间隙，保证对部分输入的保真度 |
| 噪声分支 + PNS | 观察区域衰减扰动，缺失区域纯噪声 | 在保真度与生成多样性间取得平衡 |
| IAS 单步梯度优化 | 掩码区域 BCE 损失 + 单步梯度下降 | 消除边界伪影，实现观察-生成区域的平滑过渡 |

消融实验（Table 6）证实了三者的必要性：移除 ERS 导致性能下降最为严重（Redwood CD 从 1.42 升至 3.42），移除 PNS 产生条纹状伪影（CD 升至 1.94），移除 IAS 则导致边界空洞和不一致（CD 升至 1.88）。IAS 采用 10 步优化相比单步无显著提升（CD 1.46 vs 1.42），验证了单步设计的效率。

## 实验与分析

### 主实验结果

LaS-Comp在多个基准上一致取得最优零样本补全性能，且完全无需训练。以下从真实扫描、合成数据、真实世界保真度以及多模式鲁棒性四个维度展开。

**真实扫描（Redwood）。** 在Redwood数据集上，基于TRELLIS骨干的LaS-Comp达到平均倒角距离（CD）1.42×10²、搬土距离（EMD）1.84×10²，相比现有零样本方法ComPC（Huang et al., ICLR 2025）分别降低27.2%和29.0%，比GenPC（Li et al., CVPR 2025）分别降低18.4%和36.1%（Table 1）。类别级分析显示，LaS-Comp在椅子、桌子、沙发等常见类别上均保持领先，且对单视角扫描产生的极度稀疏输入（如仅可见椅背）仍能恢复合理几何（Figure 4）。

**合成数据。** 在合成虚拟扫描上，LaS-Comp（TRELLIS）取得CD 1.11×10²、EMD 1.41×10²，比ComPC的CD降低31.1%（Table 2）。值得注意的是，合成数据的缺失模式更为规整，但基于2D扩散先验的方法（如SDS-Comp、PCDreamer）在此设定下仍会产生与输入不一致的结构，而LaS-Comp通过显式空间替换从根本上保证了观察区域的几何保真度。

**真实世界保真度（ScanNet与KITTI）。** 在ScanNet和KITTI真实扫描上，使用单向倒角距离（UCD）和单向豪斯多夫距离（UHD）衡量补全结果对输入点云的保真度。LaS-Comp在ScanNet-Chair上取得UCD 0.8×10⁴、UHD 2.0×10²，在KITTI-Car上取得UCD 1.4×10⁴、UHD 4.5×10²，平均UCD比ComPC降低约38%（Table 3）。Figure 5的定性对比显示，LaS-Comp在极度稀疏的KITTI车辆扫描上能保持车身轮廓的完整性，而ComPC和GenPC则出现明显的结构断裂。

**多模式补全鲁棒性（Omni-Comp）。** 为系统评估方法对不同缺失模式的适应能力，作者构建了Omni-Comp基准，涵盖随机裁剪、单视角扫描、语义部件缺失三种模式。LaS-Comp在Omni-Comp上相比ComPC平均降低CD 49.6%、EMD 39.4%（Table 4），且在所有缺失模式下均保持优势。Figure 6的定性结果表明，LaS-Comp对语义部件缺失（如椅子缺扶手）的补全结果在拓扑上更为合理，而对比方法倾向于生成与输入部件不匹配的几何。

**补全多样性。** 在Redwood与合成数据上，LaS-Comp的最大均值差异（MMD）和总均值差异（TMD）均优于ComPC和GenPC（Table 5），表明其在生成多样化合理补全的同时，不会产生与输入几何矛盾的随机结构。Figure 7展示了同一输入下的多个补全样本，缺失区域的几何在保持全局一致性的前提下呈现自然变化。

### 消融实验

Table 6系统消融了LaS-Comp各核心组件，结果如下：

1. **朴素潜在替换基线（Naive baseline）：** 仅将部分输入的潜在编码直接替换到生成潜在中，Redwood CD达2.15×10²，合成数据CD达2.33×10²，远差于完整方法。这直接验证了论文的核心瓶颈——潜在空间中的域间隙使得简单的潜在替换不可靠。

2. **移除显式替换阶段（w/o ERS）：** 性能下降最为剧烈，Redwood CD飙升至3.42×10²、EMD至4.94×10²，合成数据CD升至3.53×10²。Figure 8的红色框标注显示，无ERS时补全结果在观察区域出现严重的几何偏离和伪影，证明在几何空间进行空间替换对保真度至关重要。

3. **移除部分感知噪声调度（w/o PNS）：** 使用统一噪声调度替代PNS后，Redwood CD升至1.94×10²，合成数据CD升至2.27×10²，且产生明显的条纹状伪影（Figure 8）。这表明对观察区域与缺失区域施加差异化噪声幅度是保证生成质量的关键。

![[assets/figures/papers/paper_list_l2532_https_arxiv_org_abs_2602_18735/figures/014_Figure_8.jpg]]
*Figure 8: Visual comparison of the ablation studies. The red boxes highlight the artifacts and holes*

4. **移除隐式对齐阶段（w/o IAS）：** Redwood CD升至1.88×10²、EMD至2.14×10²，合成数据CD升至1.17×10²。Figure 8显示边界区域出现空洞和不一致，证实IAS通过单步梯度优化有效平滑了观察区域与生成区域的过渡。

5. **IAS优化步数：** 将单步梯度更新扩展为10步（Optimization steps=10），Redwood CD为1.46×10²，与完整方法的1.42×10²相比无显著提升，说明单步优化已足够高效地消除边界伪影。

### 失败模式与局限性

尽管LaS-Comp在多数场景下表现优异，仍存在以下已知局限：

- **极端噪声退化：** 当部分输入包含严重噪声时，细薄结构（如椅腿、桌沿）可能退化或丢失。Figure 10展示了此类失败案例——全局形状虽可恢复，但局部几何质量明显下降。这是因为显式空间替换会将噪声一并注入生成过程，而当前设计缺乏对输入噪声的显式建模。

- **模型先验依赖：** 方法完全依赖预训练3D基础模型（TRELLIS、Direct3D-S2）的表达能力。若模型未充分覆盖某些罕见类别，补全质量会受制于先验知识。作者在开放问题中指出，开发鲁棒的归一化方法以处理任意尺度与姿态的野外输入是未来方向。

- **基准覆盖有限：** Omni-Comp当前仅包含30个对象（Table 7），可能未覆盖所有极端退化场景，结论的泛化性需在更大规模基准上进一步验证。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|---------|
| Table 1 | Redwood上CD/EMD全面超越ComPC、GenPC等零样本方法 |
| Table 2 | 合成数据上CD比ComPC降低31.1% |
| Table 3 | 真实扫描保真度指标UCD/UHD平均优于ComPC约38% |
| Table 4 | Omni-Comp多模式基准上CD/EMD分别降低49.6%/39.4% |
| Table 5 | 补全多样性（MMD/TMD）优于现有零样本方法 |
| Table 6 | ERS对性能贡献最大，移除后CD从1.42恶化至3.42 |
| Figure 4-6 | 定性结果一致显示LaS-Comp在几何合理性与输入保真度上的优势 |
| Figure 8 | 消融可视化：无ERS产生几何偏离，无PNS产生条纹伪影，无IAS产生边界空洞 |

![[assets/figures/papers/paper_list_l2532_https_arxiv_org_abs_2602_18735/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparisons on Redwood [10]. We highlight the best and second-best results*

![[assets/figures/papers/paper_list_l2532_https_arxiv_org_abs_2602_18735/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparisons on the synthetic data [31, 44]. We highlight the best and second-best results*

![[assets/figures/papers/paper_list_l2532_https_arxiv_org_abs_2602_18735/figures/008_Table_3.jpg]]
*Table 3: Completion fidelity on ScanNet [15] and KITTI [21]*

![[assets/figures/papers/paper_list_l2532_https_arxiv_org_abs_2602_18735/figures/009_Table_4.jpg]]
*Table 4: Quantitative comparisons on our proposed Omni-Comp*

![[assets/figures/papers/paper_list_l2532_https_arxiv_org_abs_2602_18735/figures/015_Table_6.jpg]]
*Table 6: Ablation studies. The baseline uses only latent replacement for completion*

![[assets/figures/papers/paper_list_l2532_https_arxiv_org_abs_2602_18735/figures/012_Table_5.jpg]]
*Table 5: Completion diversity evaluation on Redwood [10] and synthetic data [31, 44]*

### 补充图表

![[assets/figures/papers/paper_list_l2532_https_arxiv_org_abs_2602_18735/figures/018_Figure_10.jpg]]
*Figure 10: Visual examples of the completion results under extremely noisy partial inputs. Despite the severe noise that heavily corrupts the observed points, our method can still recover a reasonable global structure and overall object silhouette, but many fine details and thin structures are degraded or missing, revealing the limitation of our model when strong noise overwhelms the underlying geometry*

## 方法谱系与知识库定位

### 问题定位：3D补全中的潜在-空间域间隙

LaS-Comp 解决的核心瓶颈在于：当前主流的3D基础模型（如 TRELLIS、Direct3D-S2）普遍采用**潜在-生成式架构**，即通过 VAE 编码器将几何形状映射到低维潜在空间，再在该空间中进行扩散或流匹配生成。然而，部分观测与完整形状在潜在空间中存在显著的**域间隙（latent gap）**——即使部分输入与真值在观察区域共享完全相同的表面几何，它们在潜在空间对应区域的编码相似度极低（平均余弦相似度仅 0.4593，见 Supp. Figure 9）。这意味着，直接在潜在空间对部分输入进行条件补全本质上是不可靠的。

这一发现将 LaS-Comp 与现有零样本补全方法彻底区分开来。以 **ComPC**（Huang et al., ICLR 2025）和 **GenPC**（Li et al., CVPR 2025）为代表的先前工作，或依赖 2D 扩散先验通过渲染蒸馏进行 3D 补全，或尝试在潜在空间进行条件生成，但均未显式处理上述域间隙问题。2D 先验方法（如 **SDS-Comp** (Kasten et al., NeurIPS 2023)、**PCDreamer** (Wei et al., CVPR 2025)）的另一个根本缺陷在于：当部分输入的所有视角均不完整时（如随机裁剪或语义部件缺失），2D 渲染无法提供有效的跨视角约束，导致补全结果几何不一致。

### 方法谱系：从监督学习到零样本生成的演进

3D 形状补全的方法谱系可沿两个维度展开：**监督范式**与**先验来源**。

**监督学习范式**的代表包括 **SVDFormer**（Zhu et al., ICCV 2023）和 **AdaPoinTr**（Yu et al., TPAMI 2023），它们依赖大规模配对数据（部分-完整形状对）进行端到端训练，在已知类别上表现优异，但泛化到新类别或真实扫描时性能急剧下降。**Shape-Inv**（Zhang et al., CVPR 2021）通过 GAN 反演实现无监督补全，**P2C**（Cui et al., ICCV 2023）采用自监督策略，减少了对配对数据的依赖，但仍需针对特定数据集进行训练。

**零样本生成范式**是近年来的主流趋势，其核心思路是释放预训练生成模型中的几何先验，避免任务特定的训练。这一范式中存在两条技术路线：

- **2D 先验路线**：SDS-Comp、PCDreamer 和 ComPC 均通过 Score Distillation Sampling 将 2D 扩散模型的先验知识蒸馏到 3D 表示中。这类方法的优势在于利用了 2D 基础模型的丰富语义，但受限于 2D-3D 映射的歧义性和视角覆盖的不完整性。
- **3D 先验路线**：GenPC 率先探索了利用 3D 生成先验进行补全的可能性，但仍局限于潜在空间内的操作。LaS-Comp 属于这一路线的深化与突破——它不改变 3D 基础模型的权重，而是通过**在几何空间注入观测约束**的方式，从根本上弥合潜在-空间域间隙。

### 关键设计槽位对比

LaS-Comp 相对于已有方法的核心创新可通过四个关键设计槽位的变更来理解：

| 设计槽位 | 基线方法取值 | LaS-Comp 取值 | 变更逻辑 |
|---------|------------|--------------|---------|
| **补全领域** | 仅在潜在空间进行条件生成，或依赖 2D 渲染的 3D 蒸馏 | 在几何空间进行显式空间替换（ERS），利用清洁/噪声双分支与部分感知噪声调度（PNS）将观测几何注入生成过程 | 绕过潜在空间域间隙，直接在几何空间保证输入保真度 |
| **去噪噪声调度** | 对所有空间区域施加相同的随机扰动 | PNS：对观察区域使用时间依赖的预测-噪声混合（系数 $\sqrt{1-t}$），对缺失区域替换为纯高斯噪声以增强多样性 | 差异化控制观察与缺失区域的随机性，平衡保真度与多样性 |
| **边界一致性处理** | 无专门处理，或依赖后期优化 | 隐式对齐阶段（IAS）：在掩码区域计算几何对齐损失，通过单步梯度更新优化潜在特征以平滑边界 | 消除空间替换引入的边界伪影，实现观察与生成区域的无缝过渡 |
| **模型依赖与训练需求** | 需要特定架构训练或配对数据 | 完全无需训练，可即插即用于任意潜在-生成式 3D 基础模型 | 最大化兼容性与实用性，降低部署门槛 |

### 适用边界与能力定位

**强适用场景**：
- 类别无关的零样本补全：方法不依赖类别标签，可处理训练中未见过的物体类别
- 多样化缺失模式：随机裁剪、单视角扫描、语义部件缺失等模式均适用（Figure 1）
- 文本引导补全：通过将文本条件注入基础模型的生成过程，支持对缺失区域的语义控制（Figure 1d）
- 多模态兼容：已验证与 TRELLIS 和 Direct3D-S2 两种不同架构的 3D 基础模型兼容

**性能边界**：
- 单个形状补全仅需约 20 秒，比现有零样本方法快 3 倍以上
- 在 Redwood 真实扫描数据集上，相比 ComPC 降低 CD 27.2%、EMD 29.0%；相比 GenPC 降低 CD 18.4%、EMD 36.1%
- 在 Omni-Comp 多模式基准上，相比 ComPC 平均降低 CD 49.6%、EMD 39.4%

### 局限性与失效模式

**严重噪声退化**：当部分输入包含极端噪声时，细薄结构或精细细节可能退化或丢失（Figure 10）。尽管全局形状通常可恢复，但局部几何质量会明显下降。这是因为 ERS 的空间替换操作会将噪声也一并注入生成过程，而 IAS 的梯度优化无法完全区分噪声与真实几何。

**先验依赖瓶颈**：方法的表现受制于预训练 3D 基础模型的表达能力。若基础模型在特定类别上训练不充分或覆盖不足，补全质量将直接受限于其先验知识的完整性。这一依赖关系在消融实验中通过切换 TRELLIS 和 Direct3D-S2 两个不同基础模型时的性能差异得到间接验证。

**基准覆盖局限**：当前提出的 Omni-Comp 基准仅包含 30 个对象（来自 Redwood、YCB 和 Synthetic 三个来源），可能尚未覆盖所有极端退化场景（如严重自遮挡、非刚性变形等）。

### 开放问题

1. **野外归一化问题**：当前方法假设输入形状已进行适当的尺度与姿态归一化。在缺乏真实形状标注的野外 3D 补全场景中，如何开发鲁棒的归一化方法以处理任意尺度与姿态的输入，是实现实际部署的关键挑战。

2. **薄壁结构保真度**：能否在潜在空间注入观测几何的同时保留更精确的薄壁结构？当前 ERS 在几何空间进行替换，但解码-编码的循环可能丢失高频细节。一种可能的改进方向是在潜在空间与几何空间之间建立更细粒度的双向映射，以提升极端噪声下的细节恢复能力。

3. **与 2D 先验的融合**：LaS-Comp 完全依赖 3D 先验，而 2D 先验方法在语义理解方面具有优势。如何在保持几何一致性的前提下融合两类先验，是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/LaS_Comp_Zero_shot_3D_Completion_with_Latent_Spatial_Consistency.pdf]]