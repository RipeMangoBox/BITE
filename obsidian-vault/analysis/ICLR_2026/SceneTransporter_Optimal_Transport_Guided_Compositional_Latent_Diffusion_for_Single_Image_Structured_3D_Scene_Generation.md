---
title: "SceneTransporter: Optimal Transport-Guided Compositional Latent Diffusion for Single-Image Structured 3D Scene Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SceneTransporter_Optimal_Transport_Guided_Compositional_Latent_Diffusion_for_Sin_832fbf2b9f56.pdf
project_link: "https://2019epwl.github.io/SceneTransporter/"
code_link: null
aliases:
- SceneTransporter
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在组合潜扩散模型的去噪循环内部，引入基于最优传输（OT）的全局相关性分配机制：通过求解熵正则化OT问题获得patch到部件的传输计划，并利用该计划门控交叉注意力，强制实施一对一的路由约束；同时以边缘正则化的分配代价引导相似patch聚类，阻止跨边缘信息泄漏。
primary_logic: 将结构化3D场景生成重新定义为全局相关分配问题，并用最优传输显式注入两种结构约束：(1) OT门控交叉注意力执行排他性的patch到部件路由，根本性地防止特征纠缠；(2) 传输的竞争性质结合边缘感知代价，诱导连贯区域自然聚集成物体并保持清晰边界，从而在无监督条件下实现实例级分离。
claims:
- CCA去偏聚类探针显示原始部件令牌聚类失败，而移除共享子空间后聚类成功，证明模型内部分配机制缺乏结构约束。
- 在开放世界场景图像评测中，我们的方法在几何保真度（ULIP↑ 0.1466, ULIP-2↑ 0.3220, Uni3D↑ 0.3021）和部件解耦（IoU_max↓ 0.0101）上均取得最优或次优结果，显著优于PartPacker基线。
- 消融可视化显示OT门控注意力产生清晰的一对一分配图，而标准注意力图分散混乱，导致几何紊乱，直接验证了排他性路由是防止特征纠缠的关键。
- 边缘正则化代价使图像中空间相邻的物体（如沙发与边桌、木柱与栅栏）在生成中得到干净分离，而移除该代价则导致混合部件。
---

# SceneTransporter: Optimal Transport-Guided Compositional Latent Diffusion for Single-Image Structured 3D Scene Generation

> [!tip] 核心洞察
> 将结构化3D场景生成重新定义为全局相关分配问题，并用最优传输显式注入两种结构约束：(1) OT门控交叉注意力执行排他性的patch到部件路由，根本性地防止特征纠缠；(2) 传输的竞争性质结合边缘感知代价，诱导连贯区域自然聚集成物体并保持清晰边界，从而在无监督条件下实现实例级分离。

| 字段 | 内容 |
|------|------|
| 中文题名 | SceneTransporter：基于最优传输引导的组合潜扩散单图像结构化3D场景生成 |
| 英文题名 | SceneTransporter: Optimal Transport-Guided Compositional Latent Diffusion for Single-Image Structured 3D Scene Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=xjCkwPhQWq) · [Project](https://2019epwl.github.io/SceneTransporter/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | SceneTransporter |
| Dataset | Open-world scene images |

> [!tip] 效果简介
> - Open-world scene images (74 collected images) 上，ULIP ↑ 0.1466 vs 0.1417 (PartPacker) (+0.0049)；ULIP-2 ↑ 0.3220 vs 0.3083 (PartPacker) (+0.0137)；Uni3D ↑ 0.3021 vs 0.2887 (PartPacker) (+0.0134)。

## 概述

### 问题背景

从单张图像生成结构化的3D场景是一个核心的视觉计算任务，要求同时恢复场景的几何形状、外观和实例级分解。现有方法主要分为两类：一是“分而治之”策略，先进行2D分割与深度估计，再独立重建每个物体并组装，但这类方法依赖外部模型的精度，易受误差累积影响；二是端到端的部件级3D生成器，如**PartPacker**（Tang et al., 2025），通过组合潜扩散模型直接从图像生成多部件3D场景。然而，当这些方法被直接应用于开放世界复杂场景时，暴露出两种系统性的几何病理：**结构错分**（同一语义实例被分散到多个部件令牌中）和**几何冗余**（多个部件令牌竞争描述同一图像区域，产生重叠或空洞）。

### 核心发现

通过CCA去偏聚类探针分析，我们发现PartPacker的部件令牌无法形成稳定的实例分组——原始令牌聚类结果与真实物体边界严重不一致。然而，当移除共享混淆因子后，聚类立即成功（Figure 2）。这表明模型内部存在隐含的结构信息，但缺乏显式的分配机制将其转化为部件级分离。这一发现揭示了现有组合扩散模型的核心瓶颈：**标准交叉注意力缺乏排他性路由约束，导致特征纠缠和冗余几何**。

### 方法定位

SceneTransporter将结构化3D场景生成重新定义为**最优传输引导的全局相关性分配问题**。在组合潜扩散模型的去噪循环内部，我们引入两个关键的结构约束：

1. **OT计划门控交叉注意力**：通过求解熵正则化最优传输问题，获得图像patch到部件令牌的传输计划，并利用该计划对注意力中的键和值进行门控，强制实施一对一的patch到部件路由，从根本上防止特征纠缠。
2. **边缘正则化分配代价**：利用输入图像的边缘图对传输代价进行空间平滑，惩罚跨边缘的patch分配，促使空间相邻但语义不同的物体（如沙发与边桌）在生成中获得干净分离。

该方法在模型层面属于**组合潜扩散生成器**，在机制层面引入了**最优传输驱动的结构化注意力路由**，与依赖外部分割掩码的MIDI（Huang et al., 2025）和舍弃背景区域的PartCrafter（Lin et al., 2025b）等基线形成根本性区别。

### 主要结果

在74张开放世界场景图像的评测中，SceneTransporter在几何保真度与部件解耦两个维度均取得最优或次优结果：

- **几何保真度**：ULIP达到0.1466，ULIP-2达到0.3220，Uni3D达到0.3021，均优于PartPacker基线（Table 1）。
- **部件解耦**：IoU_max降至0.0101（PartPacker为0.0319），IoU_mean降至0.0926（PartPacker为0.2142），表明部件间重叠大幅减少（Table 1）。

消融实验进一步证实：移除OT门控注意力后，IoU_max急剧恶化至0.2142，验证了排他性路由是抑制特征泄漏和冗余几何的核心机制；边缘正则化代价的移除也使IoU_max升至0.0241，说明边缘感知平滑对精细部件分离的额外贡献（Table 4）。OT传输计划在去噪早期（约t≈540/600步）即稳定，后续仅进行局部细化，保证了物体级部分的连贯性（Figure 7）。

### 局限与展望

当前方法在细小且密集重复的物体场景中（如拥挤的船只、树木）可能将少数弱实例合并到相邻物体中；面对严重分布外（OOD）的真实图像时几何质量下降，需通过风格迁移预处理缓解。未来方向包括：将边缘正则化器替换为端到端可学习模块以减少预处理依赖；扩展至视频或多视图输入以实现时序一致的结构化场景生成；以及在大规模开放世界数据上微调以消除合成到真实的领域差距。

## 背景与动机

### 结构化3D场景生成的任务困境

从单张图像生成具有实例级语义分离的完整3D场景，是计算机视觉与图形学交叉领域的前沿难题。与单物体生成不同，场景生成要求模型同时完成**几何重建**与**结构理解**——不仅需要推断每个物体的三维形状，还必须正确地将场景分解为语义连贯、边界清晰的独立部件。这一双重需求使得现有的“分而治之”范式（先检测分割、再逐物体重建、最后组装）面临根本性瓶颈：流水线各阶段独立优化，误差在阶段间累积且无法反向修正，导致最终场景出现物体错位、尺度失调和几何冲突。

### 组合潜扩散模型的隐式承诺与显式失效

近年来，基于组合潜扩散的端到端生成器（如 **PartPacker**（Tang et al., 2025））尝试打破这一范式：在统一的扩散去噪框架内，同时维护多个部件令牌，隐式地学习将图像特征分配到不同部件。这种设计承诺了更简洁的优化目标和全局一致的场景结构。然而，当这些模型被直接应用于开放世界的复杂场景时，两种系统性的几何病理反复出现（Figure 4）：

1. **结构错分（Structural Mispartition）**：同一语义实例（如一张完整的桌子）被分散分配到多个不同的部件令牌中，导致物体被“肢解”为碎片化的几何块。
2. **几何冗余（Geometric Redundancy）**：多个部件令牌竞争性地描述同一空间区域，产生重叠、重复的几何体，造成场景臃肿且语义混乱。

### 根源诊断：分配机制的结构性缺失

为揭示上述病理的深层原因，本文对PartPacker的组合潜空间进行了系统性的**潜结构探针实验**（Figure 2）。具体而言，对部件令牌的潜编码直接执行聚类，发现聚类结果与真实的实例分组几乎无关——这表明部件令牌本身并未形成稳定的物体级表征。然而，当通过CCA（典型相关分析）去偏探针移除共享的混淆子空间后，聚类成功恢复出清晰的实例分组。这一发现揭示了关键瓶颈：**模型中并非缺乏结构信息，而是其内部的隐式分配机制（标准Softmax交叉注意力）缺乏显式的结构约束，无法将已有的隐含信息转化为正确的部件-区域对应关系**。标准交叉注意力的软分配特性允许每个图像patch同时向多个部件令牌“泄漏”信息，从根本上导致了特征纠缠和冗余几何的产生。

### 本文动机：将结构化生成重新定义为全局相关分配问题

基于上述诊断，本文提出一种范式的转换：**将结构化3D场景生成的核心挑战重新定义为全局相关分配问题**，而非单纯的条件生成问题。核心洞见在于：一个正确的场景结构等价于图像区域到部件令牌的一个全局一致、互不重叠的分配方案——这正是最优传输（Optimal Transport, OT）理论所擅长求解的问题类型。

由此，本文提出 **SceneTransporter**，在组合潜扩散模型的去噪循环内部，引入基于熵最优传输的全局相关性分配机制，显式地注入两种结构约束：（1）通过OT计划门控交叉注意力，强制执行排他性的patch到部件一对一路由，从根本上阻断跨部件的特征泄漏；（2）利用边缘正则化的分配代价，引导空间上相邻的相似patch自然聚集成连贯物体，同时惩罚跨边缘的信息传播，在无监督条件下实现清晰的实例边界分离。

## 核心创新

SceneTransporter 的核心创新在于将结构化 3D 场景生成重新定义为**全局相关性分配问题**，并通过最优传输（Optimal Transport, OT）框架在组合潜扩散模型的去噪循环内部显式注入两种结构约束，从根本上解决了现有部件级生成器中普遍存在的特征纠缠与几何冗余问题。

### 问题诊断：潜空间的结构性缺失

现有端到端部件级 3D 生成器（如 **PartPacker** (Tang et al., 2025)）虽能处理任意数量的部件，但其标准 Softmax 交叉注意力机制缺乏显式的 patch 到部件分配约束。当这些模型被直接应用于大规模开放世界场景时，暴露出两种系统性失效模式（见 Figure 4）：

- **结构错分（Structural Mispartition）**：语义上属于同一物体的图像区域被分散分配到多个不同的部件令牌，导致单个物体被错误地拆分为多个部件。
- **几何冗余（Geometric Redundancy）**：多个部件令牌竞争描述同一图像区域，产生重叠或重复的几何体。

为验证这一诊断，作者设计了 **CCA 去偏聚类探针**（Figure 2）：在 PartPacker 的组合潜空间中对原始部件令牌直接聚类，无法形成稳定的实例分组；然而，当移除由共享上下文引入的混淆因子后，聚类结果成功恢复了清晰的物体边界。这表明模型潜空间中**隐含**了足够的判别信息，但**显式**的分配机制缺乏必要的结构约束——这正是 SceneTransporter 所要填补的缺口。

### 创新一：OT 计划门控交叉注意力——强制一对一路由

SceneTransporter 将 patch 到部件的路由重新定义为一个**熵正则化最优传输问题**。在每个去噪步骤 $t$，求解以下目标获得传输计划 $\mathbf{A}_t$：

$$\mathbf{A}_t = \arg\min_{\mathbf{A} \geq 0} \langle \mathbf{C}_t, \mathbf{A} \rangle + \varepsilon_t \mathcal{H}(\mathbf{A}) \quad \mathrm{s.t.} \quad \mathbf{A} \mathbf{1} = \mu, \mathbf{A}^\top \mathbf{1} = \nu$$

其中 $\mathbf{C}_t$ 为基于 patch 与部件令牌相似度构建的代价矩阵，$\mathcal{H}(\mathbf{A})$ 为熵正则化项，$\mu$ 和 $\nu$ 分别为 patch 侧和部件侧的边际约束。通过 Sinkhorn 迭代高效求解后，传输计划 $\mathbf{A}_t$ 给出了每个 patch 到每个部件的**全局最优软分配**。

该传输计划随后通过门控函数注入交叉注意力：

$$\psi_{\lambda_t, \varepsilon_g}(w) = \varepsilon_g + (1 - \varepsilon_g) w^{\lambda_t}, \quad w \in [0,1]$$

$$\mathbf{K}_h^{(i)}(j,:) = \psi_{\lambda_t, \varepsilon_g}(\omega_i(j)) \mathbf{K}_h(j,:), \quad \mathbf{V}_h^{(i)}(j,:) = \psi_{\lambda_t, \varepsilon_g}(\omega_i(j)) \mathbf{V}_h(j,:)$$

其中 $\omega_i(j)$ 为传输计划中 patch $j$ 对部件 $i$ 的归一化权重。该机制对每个部件的键（Key）和值（Value）进行**逐行缩放**，强制实施排他性的 patch 到部件路由：当 $\lambda_t > 0$ 时，只有被 OT 计划分配给某部件的 patch 才能显著贡献该部件的注意力输出；当 $\lambda_t = 0$ 时，门控函数恒为 1，退化为标准交叉注意力。

**因果机制**：这一对一路由从根本上防止了特征纠缠——每个图像 patch 的视觉信息只能流向其被分配的唯一部件令牌，从而在无监督条件下实现了实例级的特征分离。消融实验（Figure 6）直观验证了这一点：OT 门控注意力产生清晰的一对一分配图，而标准注意力图分散混乱，直接导致几何紊乱。

### 创新二：边缘正则化分配代价——保持物体边界

标准 OT 的分配代价仅基于余弦相似度，忽略了图像中的物体边界信息，可能导致跨边界的特征泄漏。SceneTransporter 引入**边缘正则化的分配代价**：

1. 从输入图像提取边缘图并下采样至 patch 网格 $\mathbf{E}_\downarrow$；
2. 构建 4-邻域图，定义边缘感知耦合权重：

$$w_{j\ell} = \exp\big(-\gamma_{\mathrm{edge}} \max\{\mathbf{E}_\downarrow(j), \mathbf{E}_\downarrow(\ell)\}\big)$$

3. 利用该权重对 patch 间相似度进行单步平滑：

$$\widehat{S}_{i,j} = \frac{S_{i,j} + \lambda_{\mathrm{edge}} \sum_{\ell \in \mathcal{N}(j)} w_{j\ell} S_{i,\ell}}{1 + \lambda_{\mathrm{edge}} \sum_{\ell \in \mathcal{N}(j)} w_{j\ell}}$$

4. 基于平滑后的相似度构建最终 OT 代价：

$$\mathbf{C}_t(i,j) = \frac{1}{2}(1 - \widetilde{S}_{i,j})$$

**因果机制**：在区域内部，相似 patch 的分配代价被平滑拉近，促进连贯区域自然聚集成同一物体；在边缘处，耦合权重指数衰减，阻止相似度信息跨边缘传播，从而保持清晰的部件边界。消融实验（Figure 5）显示，移除边缘正则化后，空间相邻的物体（如沙发与边桌、木柱与栅栏）出现混合部件，验证了边缘感知代价对边界分离的关键作用。

### 创新三：早期路由与后期细化的分阶段策略

SceneTransporter 在 DiT 去噪器的前半部分块（前 12 个注意力块）中启用 OT 门控注意力，后半部分使用标准注意力。消融实验（Table 4 e.1–e.3）表明这一设计获得了最佳权衡：全部块启用 OT 门控使推理时间从 54.99s 增至 65.24s 而指标改善甚微。进一步的可视化分析（Figure 7）揭示了深层原因：OT 传输计划在去噪早期（约 $t \approx 540/600$ 步）即已稳定，后续步骤仅进行局部微调。这意味着**粗粒度语义路由在早期确定并保持不变**，后期标准注意力足以完成几何细节的精细化，无需持续的全局约束。

### 与 baseline 的本质差异

相较于 PartPacker 的标准交叉注意力机制，SceneTransporter 的两个 changed slots 构成了质变：

| 机制槽位 | PartPacker (baseline) | SceneTransporter (ours) | 因果效应 |
|---------|----------------------|------------------------|---------|
| 跨注意力路由 | 标准 Softmax，无显式分配约束 | OT 计划门控，强制一对一 patch 到部件路由 | 防止特征纠缠，消除结构错分与几何冗余 |
| 分配代价函数 | 基于查询-键余弦相似度，无边缘感知 | 边缘正则化平滑相似度，惩罚跨边缘传输 | 保持物体边界，防止相邻实例混合 |

这两种约束的**协同效应**是方法成功的关键：OT 门控提供了全局排他性路由的骨架，边缘正则化代价则在局部层面精炼了分配边界。单独使用任一组分均无法达到完整模型的性能（Table 4 a.1–a.2）。

## 整体框架

SceneTransporter 构建于组合式潜扩散模型之上，将结构化 3D 场景生成重新定义为**最优传输引导的全局相关性分配问题**。其核心流程如下：

### 输入编码与令牌初始化
给定一张 RGB 图像，系统首先通过 **DINOv2 图像编码器**将其编码为 $L$ 个 patch 特征 $\mathbf{I} \in \mathbb{R}^{L \times d}$，作为条件输入。同时，模型维护 $N$ 个部件特定的令牌块 $\{\mathbf{z}_i^{(t)}\}_{i=1}^N$，每个块包含 $K$ 个潜令牌。为区分不同部件，为每个部件的所有令牌添加可学习的部件身份嵌入 $\mathbf{e}_i$，并将所有部件令牌拼接为统一的潜表示 $\mathbf{Z}^{(t)} \in \mathbb{R}^{(NK) \times D}$。

### 组合式潜扩散去噪循环
在去噪步 $t$，组合式 DiT（校正流，24 个注意力块）执行以下操作：
1. **投影**：将潜令牌和图像特征通过线性层投影为查询 $\mathbf{Q}$、键 $\mathbf{K}$、值 $\mathbf{V}$。
2. **OT 引导的相关性分配**：在前半部分 DiT 块中，系统构建图像 patch 与部件令牌之间的熵最优传输问题，求解传输计划 $\mathbf{A}_t$。该计划通过门控函数 $\psi_{\lambda_t, \varepsilon_g}$ 对每个部件的键和值进行逐行缩放，强制实施**一对一的 patch 到部件路由**，从根本上防止特征纠缠。后半部分块使用标准交叉注意力进行局部细化。
3. **边缘正则化**：在计算 OT 代价矩阵时，系统从输入图像提取边缘图并下采样至 patch 网格，利用边缘感知耦合权重对 patch 间相似度进行平滑，惩罚跨边缘的信息泄漏，诱导连贯区域自然聚集成独立物体。

### 解码与场景重建
去噪完成后，清理后的部件潜令牌通过 **3D VAE 解码器**解码为每个部件的独立网格体，最终组合成完整的结构化 3D 场景。

### 管道特点
与现有“分而治之”方法（如先分割后重建）不同，SceneTransporter 实现了**端到端的单图像到结构化场景生成**，无需额外的实例掩码或预分割步骤。OT 传输计划在去噪早期（约 $t \approx 540/600$ 步）即稳定，后续仅进行局部微调，保证了物体级部件的全局连贯性。

### 补充图表

![[assets/figures/papers/paper_list_l62_https_openreview_net_forum_id_xjCkwPhQWq/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the SceneTransporter pipeline. At each denoising step t, our Optimal-Transport–Guided Correlation Assignment framework formulates a global OT problem between image patches and part-level tokens within the compositional latent DiT. We compute a part-patch cost from Q/K similarity, regularized by image edges, and solve for an optimal transport plan using Sinkhorn iteration. The OT plan gates the cross attention to enforce an explicit patch-to-part routing, and the resulting gated attention map updates the latent*

![[assets/figures/papers/paper_list_l62_https_openreview_net_forum_id_xjCkwPhQWq/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between our end-to-end scene generation pipeline in (c) with compositional 3D latent diffusion and existing “divide and conquer” methods*

## 核心模块与公式推导

SceneTransporter 的核心创新在于将去噪循环中的视觉证据路由重新定义为一个**全局最优传输（Optimal Transport, OT）引导的相关性分配问题**。该方法在组合潜扩散模型的交叉注意力机制中显式注入两种结构约束：排他性的一对一路由和边缘感知的分配代价。

### 部件令牌嵌入与投影

在去噪步骤 $t$，模型维护 $N$ 个部件特定的令牌块 $\{\mathbf{z}_i^{(t)}\}_{i=1}^N$，其中每个 $\mathbf{z}_i^{(t)} \in \mathbb{R}^{K \times D}$ 包含 $K$ 个令牌。首先为每个部件的所有令牌添加可学习的部件身份嵌入 $\mathbf{e}_i \in \mathbb{R}^D$：

$$\tilde{\mathbf{z}}_i^{(t)} = \mathbf{z}_i^{(t)} + \mathbf{1}_K \mathbf{e}_i^\top, \quad \mathbf{Z}^{(t)} = \mathrm{concat}_{\mathrm{tokens}}(\tilde{\mathbf{z}}_1^{(t)}, \dots, \tilde{\mathbf{z}}_N^{(t)}) \in \mathbb{R}^{(NK) \times D}$$

随后将拼接后的潜令牌和图像特征 $\mathbf{I}$ 通过线性层投影到查询、键、值空间：

$$\mathbf{Q} = \ell_Q(\mathbf{Z}^{(t)}) \in \mathbb{R}^{(NK) \times d}, \quad \mathbf{K} = \ell_K(\mathbf{I}) \in \mathbb{R}^{L \times d}, \quad \mathbf{V} = \ell_V(\mathbf{I}) \in \mathbb{R}^{L \times d}$$

其中 $L = H_p \times W_p$ 为图像 patch 数量。

### 熵最优传输计划求解

在每个去噪步骤，SceneTransporter 在图像 patch 与部件令牌之间构建并求解一个熵正则化的最优传输问题。该问题的目标是找到一个传输计划 $\mathbf{A}_t \in \mathbb{R}^{N \times L}$，将 $L$ 个图像 patch 的质量分配给 $N$ 个部件令牌：

$$\mathbf{A}_t = \arg\min_{\mathbf{A} \geq 0} \langle \mathbf{C}_t, \mathbf{A} \rangle + \varepsilon_t \mathcal{H}(\mathbf{A}) \quad \mathrm{s.t.} \quad \mathbf{A} \mathbf{1} = \mu, \mathbf{A}^\top \mathbf{1} = \nu$$

其中 $\mathbf{C}_t$ 为传输代价矩阵，$\mathcal{H}(\mathbf{A})$ 为熵正则化项，$\varepsilon_t$ 控制正则化强度，$\mu$ 和 $\nu$ 分别为 patch 和部件的边际分布。该问题通过 Sinkhorn 迭代高效求解，对偶变量和传输计划残差在 3–5 次迭代内下降 3–5 个数量级。

### 传输代价的边缘正则化

传输代价矩阵 $\mathbf{C}_t$ 基于 patch 与部件之间的余弦相似度构建，并引入**边缘感知平滑**以防止跨物体边界的信息泄漏。首先计算原始相似度：

$$S_{i,j} = \cos(\bar{\mathbf{q}}_i^{(t)}, \mathbf{k}_j) \in [-1, 1]$$

其中 $\bar{\mathbf{q}}_i^{(t)}$ 为部件 $i$ 的聚合查询向量。随后构建基于下采样边缘图 $\mathbf{E}_\downarrow$ 的空间耦合权重：

$$w_{j\ell} = \exp\big(-\gamma_{\mathrm{edge}} \max\{\mathbf{E}_\downarrow(j), \mathbf{E}_\downarrow(\ell)\}\big)$$

该权重在边缘附近衰减，阻止跨边缘的相似度平滑。利用该权重对相似度进行单步边缘感知平滑：

$$\widehat{S}_{i,j} = \frac{S_{i,j} + \lambda_{\mathrm{edge}} \sum_{\ell \in \mathcal{N}(j)} w_{j\ell} S_{i,\ell}}{1 + \lambda_{\mathrm{edge}} \sum_{\ell \in \mathcal{N}(j)} w_{j\ell}}$$

其中 $\mathcal{N}(j)$ 表示 patch $j$ 的 4 邻域。最终传输代价定义为：

$$\mathbf{C}_t(i,j) = \frac{1}{2}(1 - \widetilde{S}_{i,j})$$

其中 $\widetilde{S}_{i,j}$ 为经过对比度归一化后的平滑相似度。

### OT 计划门控交叉注意力

获得传输计划 $\mathbf{A}_t$ 后，SceneTransporter 利用它来门控交叉注意力中的键和值，强制实施排他性的 patch 到部件路由。首先定义门控函数，将每个部件的 patch 权重 $\omega_i(j)$ 转换为门控信号：

$$\psi_{\lambda_t, \varepsilon_g}(w) = \varepsilon_g + (1 - \varepsilon_g) w^{\lambda_t}, \quad w \in [0,1], \lambda_t \geq 0, \varepsilon_g \in [0,1)$$

当 $\lambda_t = 0$ 时，门控函数恒为 1，退化为标准交叉注意力。随后对每个部件 $i$ 和多头注意力头 $h$ 的键和值进行逐行缩放：

$$\mathbf{K}_h^{(i)}(j,:) = \psi_{\lambda_t, \varepsilon_g}(\omega_i(j)) \mathbf{K}_h(j,:), \quad \mathbf{V}_h^{(i)}(j,:) = \psi_{\lambda_t, \varepsilon_g}(\omega_i(j)) \mathbf{V}_h(j,:)$$

最终计算门控多头注意力输出：

$$\widehat{\mathbf{Z}}^{(t)}(S_i,:) = \mathrm{Concat}_{h=1}^H [\mathbf{H}_h^{(i)}] \mathbf{W}_O, \quad \mathbf{H}_h^{(i)} = \mathbf{M}_h^{(i)} \mathbf{V}_h^{(i)}$$

其中 $\mathbf{M}_h^{(i)} = \mathrm{softmax}(\mathbf{Q}_h^{(i)} {\mathbf{K}_h^{(i)}}^\top / \sqrt{d})$ 为注意力权重矩阵，$S_i$ 表示部件 $i$ 的令牌索引范围。

### 关键设计选择

**OT 门控的阶段性启用**：SceneTransporter 在 DiT 去噪器的前半部分块（前 12 个注意力块）中启用 OT 门控交叉注意力，后半部分使用标准注意力。消融实验表明，该配置在几何保真度（ULIP 0.1466）和部件解耦（IoU_max 0.0101）之间取得最佳权衡，推理时间仅为 54.99 秒；若全部块启用，时间增至 65.24 秒而指标改善甚微。

**传输计划的早期稳定性**：可视化分析显示，OT 传输计划在去噪步骤约 $t \approx 540/600$ 后即基本稳定，全局划分不再显著变化，仅在局部进行微调。这表明粗粒度的语义路由在去噪早期即已确定，保证了物体级部件的连贯性。

### 补充图表

![[assets/figures/papers/paper_list_l62_https_openreview_net_forum_id_xjCkwPhQWq/figures/002_Figure_2.jpg]]
*Figure 2: Qualitative Results on Vecset-based Latent Probing. Cluster and Cluster with CCA are our probes that perform in the compositional latent space of PartPacker; VAE clusters the latent obtained by encoding the fused geometry produced by PartPacker into the VAE. Colors denote part assignments*

![[assets/figures/papers/paper_list_l62_https_openreview_net_forum_id_xjCkwPhQWq/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative Ablation Studies on the Edge–Regularized Assignment Cost*

![[assets/figures/papers/paper_list_l62_https_openreview_net_forum_id_xjCkwPhQWq/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative Ablation Studies on the OT Plane-gated Cross Attention. Here, A attn. and B attn. denote the dual-volume soft attention probability maps, reshaped to the image patch grid (brighter means higher affinity). Hard affinity visualizes the argmax(A,B) patch assignments overlaid on the input image (blue→A, red→B). A geo. and B geo. are the geometries decoded from dual volumes, respectively, and Uni geo. is their fused scene mesh. Row (a) shows our OT plan–gated cross-attention; row (b) shows the standard cross-attention*

![[assets/figures/papers/paper_list_l62_https_openreview_net_forum_id_xjCkwPhQWq/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative Ablation Studies on the OT Plan Progression over Denoising Steps. Each map visualizes the hard OT plan at a given denoising step: every cell is an image patch assigned to one volume (dark blue = A, light cyan = B). Left→right shows the OT plan’s evolution; later steps mostly stabilize with only local refinements*

## 实验与分析

### 核心瓶颈的实证诊断

现有部件级3D生成器（如PartPacker）在开放世界场景中暴露出两类系统性几何病理：**结构错分**（同一语义实例被分散到多个部件令牌）与**几何冗余**（多个令牌竞争描述同一区域）。为验证其根源在于模型内部缺乏显式结构约束，作者设计了CCA去偏聚类探针：直接对原始部件令牌聚类无法形成稳定实例分组，而移除共享混淆因子后聚类成功（Figure 2），证明模型中隐含信息与显式分配之间存在结构性缺失。这一诊断直接驱动了最优传输引导的全局相关性分配设计。

### 主定量结果

在74张开放世界场景图像构成的评测集上，SceneTransporter与PartPacker、PartCrafter、MIDI等方法进行了公平对比（Table 1）。所有方法均使用官方发布代码与权重，确保硬件与代码层面的一致性。

![[assets/figures/papers/paper_list_l62_https_openreview_net_forum_id_xjCkwPhQWq/figures/004_Table_1.jpg]]
*Table 1: Quantitative Comparison on Structured 3D Scene Generation across Methods. Bold values indicate the best scores, while underlined values indicate the second-best scores among the fair comparison*

**几何保真度**：SceneTransporter在三个几何质量指标上均取得最优或次优成绩——ULIP达到0.1466（PartPacker为0.1417），ULIP-2达到0.3220（PartPacker为0.3083），Uni3D达到0.3021（PartPacker为0.2887）。三项指标分别提升+0.0049、+0.0137和+0.0134，表明OT引导的路由在保持几何质量的同时未引入退化。

**部件解耦**：这是SceneTransporter取得最显著优势的维度。IoU_max从PartPacker的0.0319骤降至0.0101（降幅68.3%），IoU_mean从0.2142降至0.0926（降幅56.8%）。IoU_max直接衡量最严重重叠的部件对，其大幅下降证明一对一patch到部件路由有效抑制了特征纠缠和冗余几何。值得注意的是，PartCrafter虽然报告了最低IoU，但这是因为它主动丢弃了背景/地面区域，牺牲了场景完整性，因此其IoU数值不与其它方法完全可比。

### 用户研究

Table 2展示了三个维度的人类偏好评分（1-4分制）：几何质量（3.09 vs. PartPacker 2.67）、布局连贯性（3.34 vs. PartPacker 2.74）和分割合理性（3.22 vs. PartPacker 2.62）。SceneTransporter在所有维度均获得最高评分，尤其在布局连贯性上的领先幅度最大（+0.60），与边缘正则化代价促进物体间清晰分离的机制一致。

### 消融实验：因果旋钮的逐一验证

Table 4系统拆解了SceneTransporter各组件的贡献，默认配置以星号（∗）标注。

**OT计划门控交叉注意力的核心作用**（Table 4 a.1）：移除OT门控、退化为标准交叉注意力后，ULIP降至0.1417（与PartPacker基线持平），IoU_max飙升至0.2142（恶化近20倍）。Figure 6的注意力图可视化揭示了根本原因：OT门控产生清晰的一对一分配图，每个patch仅路由到单一部件；而标准注意力图分散混乱，多个部件竞争同一图像区域，直接导致几何紊乱。这确证了排他性路由是防止特征纠缠的关键因果机制。

**边缘正则化代价的独立贡献**（Table 4 a.2）：保留OT门控但移除边缘正则化代价后，IoU_max升至0.0241，虽仍远优于无门控的0.2142，但显著差于完整模型的0.0101。Figure 5的定性对比直观展示了差异：边缘正则化使空间相邻物体（如沙发与边桌、木柱与栅栏）得到干净分离，而移除该代价则导致跨边界部件混合。这验证了边缘感知平滑在OT全局分配基础上的额外解耦增益。

**OT门控的时序配置**（Table 4 e.1–e.3）：默认在前半部分DiT块（前12块）启用OT门控，后半部分使用标准注意力，获得最佳权衡——ULIP 0.1466，IoU_max 0.0101，推理时间54.99秒。全部24块启用OT门控虽使IoU_max微降至0.0087，但推理时间增至65.24秒且ULIP略有下降（0.1438），表明后期去噪步骤中过强的结构约束反而限制了细节细化。仅在前6块启用则IoU_max升至0.0166，约束不足。

**OT计划的时间稳定性**（Figure 7）：传输计划在去噪早期（约t≈540/600步）即趋于稳定，后续仅进行局部微调。这表明粗粒度语义路由在早期确定并保持，保证了物体级部件的连贯性，与DiT去噪的动态特性高度契合。

**OT求解器的收敛性**（Figure 9）：对偶变量和传输计划残差在3-5次Sinkhorn迭代内下降3-5个数量级，边际约束违反迅速趋于微小值，证明熵OT求解器在注意力层内的高效收敛，为端到端训练中的稳定梯度反传提供了保证。

### 失败模式与局限性

尽管SceneTransporter在大多数场景中表现优异，分析揭示了以下边界情形：

- **细小密集重复物体**：在拥挤的船只、树木等场景中，OT引导的路由可能将少数弱实例合并到相邻物体中，导致微小物体数量低估。这与OT的边际约束在极端稀疏信号下的退化有关。
- **去噪步长不足**：当去噪步骤过短或令牌数量不足时，偶尔出现表面不平滑或漂浮几何伪影，表明OT约束需要足够的去噪迭代来充分细化。
- **合成到真实的泛化差距**：模型在合成渲染数据上训练，面对严重分布外（OOD）的真实图像时几何质量和部件分组下降。Figure 8显示通过风格迁移预处理（基于GPT-5的图像编辑模型将真实图像风格迁移为类渲染风格）有所缓解，但仍存在明显的领域差距。

### 补充图表

![[assets/figures/papers/paper_list_l62_https_openreview_net_forum_id_xjCkwPhQWq/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative Comparison on Structured 3D Scene Generation across Methods. Different colors indicate different parts in the generated 3D scene*

![[assets/figures/papers/paper_list_l62_https_openreview_net_forum_id_xjCkwPhQWq/figures/013_Table_4.jpg]]
*Table 4: Comparison of metrics for ablation. Bold values indicate the best scores, while underlined values indicate the second-best scores among the fair comparison. Asterisk (∗) indicates the default settings in our method*

![[assets/figures/papers/paper_list_l62_https_openreview_net_forum_id_xjCkwPhQWq/figures/012_Figure_9.jpg]]
*Figure 9: Convergence of the entropic OT solver across OT-gated cross-attention layers. We plot the residuals of the dual variables and transport plan, as well as the marginal-constraint violation, for three representative OT-gated cross-attention layers*

![[assets/figures/papers/paper_list_l62_https_openreview_net_forum_id_xjCkwPhQWq/figures/011_Figure_8.jpg]]
*Figure 8: Qualitative Results on Structured 3D Scene Generation from Real-World Images. We use a GPT-5–based image editing model to transfer the style of real-world images, making them look like images rendered from a graphics engine*

![[assets/figures/papers/paper_list_l62_https_openreview_net_forum_id_xjCkwPhQWq/figures/014_Figure_10.jpg]]
*Figure 10: Effect of adding a residual vanilla cross-attention branch. Left to right: input image, PartPacker baseline, our OT-guided routing, and our OT-guided routing with an additional residual cross-attention branch (Ours residual), which recovers the small crowded instances (e.g., boats) while preserving the improved global layout and part separation*

## 方法谱系与知识库定位

### 1. 任务定位与基线谱系

SceneTransporter 面向**单图像结构化3D场景生成**任务：给定单张RGB图像，直接输出由多个独立网格部件组成的完整3D场景，无需任何实例掩码、深度图或多视图输入。该任务处于组合式3D生成与开放世界场景理解的交汇点。

现有方法可沿两条技术路线追溯：

- **分治式管线**：先进行2D分割/检测，再对每个物体独立重建，最后拼合。代表性工作如 **MIDI**（Huang et al., 2025），其多实例注意力框架需要额外的实例分割掩码作为输入，且在室外复杂场景上性能显著下降——论文实验表明其在开放世界场景上的几何保真度指标 ULIP 仅约 0.13，低于本方法（0.1466）。这类方法的根本瓶颈在于：2D分割误差会直接传导至3D重建，且拼合步骤缺乏全局场景级一致性约束。

- **端到端组合式生成**：直接在潜空间中生成多个部件令牌，通过交叉注意力从图像特征中汲取信息。**PartCrafter**（Lin et al., 2025b）面向部件级物体生成，但生成时舍弃背景区域，牺牲了场景完整性。**PartPacker**（Tang et al., 2025）作为本方法的直接基础模型，使用组合潜扩散和双体积打包策略，支持任意部件数量，是当前端到端路线的最强基线。

SceneTransporter 在 PartPacker 的架构骨架之上，**仅替换交叉注意力中的路由机制和分配代价函数**，将结构化场景生成重新定义为全局最优传输问题，从而在保持端到端训练的前提下，从根本上解决了部件令牌分配缺乏结构约束的核心瓶颈。

### 2. 核心改进槽位

SceneTransporter 对 PartPacker 基线的改动集中在两个精确槽位，而非整体架构重构：

| 槽位 | 基线值 | 改进值 | 证据锚点 | 置信度 |
|------|--------|--------|----------|--------|
| 跨注意力路由机制 | 标准 Softmax 交叉注意力，无显式分配约束 | OT 计划门控交叉注意力：通过熵最优传输计划对键和值进行部件特定缩放，强制实施一对一的 patch 到部件路由 | Section 3.3 (Eq. 4–8) | 0.98 |
| 分配代价函数 | 基于查询和键的余弦相似度，无边缘感知 | 边缘正则化的分配代价：利用下采样边缘图对相似度进行平滑，惩罚跨边缘传输 | Section 3.3 (Eq. 9–12) | 0.98 |

这两个槽位的改动互为补充：OT 门控提供了**排他性**（每个 patch 只能路由到一个部件），边缘正则化代价提供了**空间连贯性**（同一物体的相邻 patch 倾向于路由到同一部件，但在物体边界处阻止信息泄漏）。消融实验（Table 4）证实：单独移除 OT 门控导致 IoU_max 从 0.0101 飙升至 0.2142（恶化 21 倍），而单独移除边缘正则化代价使 IoU_max 升至 0.0241（恶化 2.4 倍），验证了排他性路由是防止特征纠缠的**必要条件**，边缘感知平滑在此基础上的**额外增益**。

### 3. 关键设计决策与适用边界

**OT 求解器集成位置**：SceneTransporter 将熵 OT 求解器嵌入去噪循环的**每个去噪步骤**，而非仅作为一次性预处理。这一设计的关键依据来自 Figure 7 的消融观察：OT 传输计划在去噪早期（约 t≈540/600 步）即稳定，后续仅进行局部细化。这意味着粗粒度语义路由在早期确定并保持，OT 求解器无需在每个步骤从头计算——论文利用 Sinkhorn 迭代的快速收敛性（3-5 次迭代内残差下降 3-5 个数量级，Figure 9）使每步开销可控。

**门控注意力与标准注意力的混合策略**：默认配置仅在前半部分 DiT 块（12/24）中启用 OT 门控，后半部分使用标准交叉注意力。Table 4(e) 的消融显示：全部 24 块启用 OT 门控时推理时间从 54.99s 增至 65.24s，而指标改善甚微（ULIP 仅从 0.1466 升至 0.1472），表明早期块的结构路由已足够，后期块的标准注意力可提供局部细节精化。

**适用边界与已知局限**：

1. **密集微小物体场景**：在拥挤的船只、树木等细小且密集重复的场景中，OT 引导的路由可能将少数弱实例合并到相邻物体中，导致微小物体数量低估。这一局限源于 OT 的边际约束假设了固定的部件数量 N，当实际物体数超过 N 时必然发生合并。

2. **合成到真实的泛化差距**：模型在合成渲染数据上训练，面对严重分布外（OOD）的真实图像时几何质量和部件分组下降。论文采用 GPT-5 风格迁移作为预处理缓解此问题（Figure 8），但本质上仍存在领域差距。

3. **表面平滑度与漂浮伪影**：当去噪步骤过短或令牌数量不足时，偶尔出现表面不平滑或漂浮几何伪影，这是组合潜扩散模型的共有问题，非 OT 路由引入。

### 4. 开放问题与扩展方向

论文明确或隐含地留下了以下开放问题：

- **残差交叉注意力分支的扩展性**：Figure 10 显示添加残差标准交叉注意力分支可进一步改善细节，但在包含数百个微小实例的极密集场景中，该分支的计算开销与纯 OT 路由相比如何？其可扩展性尚未验证。

- **边缘正则化器的可学习化**：当前边缘正则化器依赖固定的边缘检测器（下采样边缘图），是否可以通过端到端学习取代，从而减少对预处理步骤的依赖并自适应不同图像风格？

- **时序/多视图扩展**：该方法能否扩展至视频或多视图输入，实现时序一致的结构化场景生成？OT 框架天然支持多帧间的对应关系建模，但需要重新设计边际约束和代价函数。

- **与其他结构先验的融合**：OT 引导的注意力能否与深度图、法线图等其他形式的结构先验结合，进一步提高场景布局精确度？边缘正则化代价已展示了空间先验注入的有效性，更丰富的几何先验可能带来额外增益。

- **开放世界微调消除领域差距**：能否在更大规模的开放世界场景数据上进行微调，以消除合成到真实的领域差距，而无需依赖风格迁移预处理？这需要构建相应的训练数据集和评估基准。

## 原文 PDF

![[paperPDFs/ICLR_2026/SceneTransporter_Optimal_Transport_Guided_Compositional_Latent_Diffusion_for_Sin_832fbf2b9f56.pdf]]