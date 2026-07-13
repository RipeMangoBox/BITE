---
title: "UniHand: A Unified Model for Diverse Controlled 4D Hand Motion Modeling"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/UniHand_A_Unified_Model_for_Diverse_Controlled_4D_Hand_Motion_Modeling_fb445fed84c1.pdf
project_link: null
code_link: null
aliases:
- UniHand
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将估计与生成统一为条件运动合成任务，通过联合变分自编码器（Joint VAE）将2D/3D骨架、MANO参数等结构化条件映射至共享隐空间，并设计手部感知机（Hand Perceptron）从全帧视觉标记中直接关注手部特征，使扩散模型灵活融合多模态条件。
primary_logic: 联合VAE学习跨模态对齐的共享隐空间，手部感知机从完整图像密集标记中提取手部相关特征，避免检测裁剪流水线；在此隐空间上进行扩散，模型可同时利用结构化信号与视觉细节，实现鲁棒、统一的手部运动重建与生成。
claims:
- 在DexYCB整个测试集上，UniHand的PA-MPJPE为4.08mm，优于之前最好的视频方法HaWoR（4.76mm）14.3%；在最高遮挡（75-100%）下PA-MPJPE仅为4.26mm，展现出对严重遮挡的鲁棒性。
- 消融实验去掉了手部感知机后，PA-MPJPE从4.08升至7.81（性能下降91%），证明该模块在利用全帧视觉信息中的关键作用。
- DexYCB (All) 上 PA-MPJPE (mm) = 4.08
- DexYCB (Occlusion 75-100%) 上 PA-MPJPE (mm) = 4.26
---

# UniHand: A Unified Model for Diverse Controlled 4D Hand Motion Modeling

> [!tip] 核心洞察
> 联合VAE学习跨模态对齐的共享隐空间，手部感知机从完整图像密集标记中提取手部相关特征，避免检测裁剪流水线；在此隐空间上进行扩散，模型可同时利用结构化信号与视觉细节，实现鲁棒、统一的手部运动重建与生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniHand：面向多样化受控4D手部运动建模的统一模型 |
| 英文题名 | UniHand: A Unified Model for Diverse Controlled 4D Hand Motion Modeling |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=upUl6hMYwy) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | UniHand |
| Dataset | DexYCB, HO3D, HOT3D |

> [!tip] 效果简介
> - DexYCB (All) 上，PA-MPJPE (mm) 4.08 vs HaWoR 4.76 (↓0.68 (14.3%))。
> - DexYCB (Occlusion 75-100%) 上，PA-MPJPE (mm) 4.26 vs HaWoR 5.07 (↓0.81 (16.0%))。
> - HO3D 上，PA-MPJPE (mm) 6.7 vs WiLoR 7.5 (↓0.8 (10.7%))。

## 概要

**问题瓶颈**：4D手部运动建模长期被割裂为“从视觉输入估计手部姿态”和“从条件信号生成手部运动”两个独立任务。这种分离导致异构条件信号（RGB视频帧、2D/3D骨架、MANO参数等）缺乏统一的表示空间，运动先验难以跨任务迁移。尤其在严重遮挡或时间维度不完整的输入下，传统方法性能急剧退化——例如最高遮挡区间（75–100%）下，此前最优视频方法HaWoR的PA-MPJPE仍达5.07 mm，暴露了单任务框架对时序上下文和全局视觉线索利用不足的根本缺陷。

**核心方法**：UniHand首次将手部运动估计与生成统一为条件运动合成任务，构建了一个由联合变分自编码器（Joint VAE）和潜在扩散模型（Latent Diffusion Model）组成的统一框架。其关键创新在于：

- **共享隐空间对齐**：Joint VAE将MANO参数、2D/3D骨架等结构化条件与运动序列映射至同一隐空间，通过重建损失、KL散度与隐空间对齐损失的联合优化，实现跨模态表示的对齐，使扩散模型能够灵活融合任意组合的异构条件。
- **手部感知机（Hand Perceptron）**：摒弃传统“检测-裁剪”流水线，直接对冻结视觉骨干（DINO-v2）提取的全帧密集token进行注意力聚合，提取每帧单一手部特征token，保留环境与交互物体上下文信息。
- **规范相机坐标系**：以首帧定义规范相机空间，解耦相机运动与手部运动，无需显式外参即可同时适用于静态与动态相机场景。

**主要结果**：在DexYCB全测试集上，UniHand取得PA-MPJPE 4.08 mm，较此前最优视频方法HaWoR（4.76 mm）降低14.3%；在最高遮挡区间（75–100%）下PA-MPJPE仅4.26 mm，较HaWoR降低16.0%。消融实验证实，移除手部感知机后PA-MPJPE从4.08退化至7.81（性能下降91%），验证了该模块在利用全帧视觉信息中的关键作用。在HO3D跨域泛化测试与世界坐标系HOT3D评估中，UniHand同样以一致优势超越现有方法，证明了统一框架的鲁棒性与通用性。

### 任务定义与核心挑战

4D手部运动建模旨在从视觉输入中恢复手部在三维空间中的姿态序列与轨迹。该任务面临三个核心挑战：

1. **异构条件信号的融合困境**：手部运动可由多种异构信号驱动——RGB图像、2D/3D骨架、MANO参数等。传统方法通常将估计与生成视为两个独立任务，导致不同模态的条件信号缺乏共享表示空间，运动先验难以跨任务迁移。
2. **严重遮挡下的性能退化**：当手部被物体或自身遮挡时，基于区域裁剪的检测流水线会丢失关键视觉信息，重建精度急剧下降。
3. **动态相机下的运动不连续**：在相机运动场景中，基于相机坐标系的建模会导致手部运动与相机运动耦合，需额外SLAM估计外参才能恢复世界坐标系下的连续轨迹。

### 现有方法缺口

当前主流方法可归为三类，但均存在明显局限：

**图像级方法**（如 **HaMeR**，Pavlakos et al., 2024；**MeshGraphormer**，Lin et al., 2021）逐帧独立估计手部姿态，缺乏时序一致性建模，在遮挡或模糊帧上容易产生抖动和错误。**WiLoR**（Potamias et al., 2025）虽支持多手估计与优化，但仍未利用视频帧间的运动先验。

**视频级方法**（如 **Deformer**，Fu et al., 2023；**HaWoR**，Zhang et al., 2025；**Dyn-HaMR**，Yu et al., 2025）引入时序Transformer或解耦策略来提升连续性，但普遍依赖手部检测裁剪区域作为输入，丢弃了环境上下文和交互物体信息。在严重遮挡（75-100%遮挡率）下，**HaWoR**的PA-MPJPE为5.07mm，仍存在显著误差。

**生成式方法**虽能合成多样化的运动序列，但通常仅支持单一条件模态（如纯骨架驱动），缺乏与视觉观测的有效融合，难以应用于真实场景的运动重建。

### 核心瓶颈

传统流水线的根本瓶颈在于**估计与生成的割裂**：估计任务依赖视觉特征提取但缺乏运动先验约束，生成任务拥有丰富的运动先验却难以与视觉观测对齐。这种割裂导致：
- 异构条件信号无法在统一空间中有效融合
- 运动先验知识无法跨任务迁移
- 遮挡或时间不完整输入下性能大幅退化

### 本文动机

针对上述缺口，UniHand提出将4D手部运动估计与生成统一为**条件运动合成**任务，其核心设计动机包括：

1. **统一框架**：通过扩散模型在共享隐空间上同时支持估计与生成，使运动先验可在两类任务间自由迁移。
2. **全帧视觉利用**：摒弃检测裁剪流水线，通过手部感知机从全帧密集视觉标记中直接关注手部特征，保留环境与物体上下文。
3. **规范坐标系建模**：以首帧定义规范相机空间，解耦相机运动与手部运动，无需显式外参即可实现静态与动态相机下的连续运动建模。

该设计使得模型在DexYCB全测试集上达到PA-MPJPE 4.08mm，较此前最优视频方法HaWoR（4.76mm）提升14.3%；在最高遮挡场景下PA-MPJPE仅为4.26mm，展现出对严重遮挡的强鲁棒性（Table 1）。

## 核心方法与创新机理

UniHand 的核心创新在于将 4D 手部运动估计与生成统一为**条件运动合成**这一单一范式，并围绕该范式重新设计了三个关键环节：多模态条件对齐、视觉特征提取和坐标空间建模。

### 1. 统一范式：从任务分离到条件运动合成

传统方法将手部运动估计（从视觉输入恢复运动）与运动生成（从结构化条件合成运动）视为两个独立任务，导致异构条件信号（视觉、骨架、MANO 参数等）无法有效融合，运动先验知识难以跨任务迁移。UniHand 首次将二者统一为条件运动生成框架：给定任意组合的条件信号 $C$（视频帧、2D/3D 骨架关键点、可选的 MANO 姿态参数），模型均输出一致的手部运动序列 $\boldsymbol{x} = \{x^i\}_{i=1}^N$。这一统一范式使得模型能够灵活处理从纯生成（仅给定稀疏骨架）到密集估计（给定全帧视频）的各类下游任务，无需针对不同任务设计独立流水线。

### 2. 多模态条件融合：联合 VAE 构建共享隐空间

**Changed Slot：多条件信号融合**

| 维度 | Baseline 做法 | UniHand 做法 |
|------|--------------|-------------|
| 编码方式 | 各条件独立编码，通常仅支持单一模态或简单拼接 | 联合 VAE 将 MANO 参数、2D/3D 骨架等结构化条件编码至**共享隐空间** |
| 融合能力 | 缺乏跨模态对齐机制 | 通过隐空间对齐损失 $\mathcal{L}_{\mathrm{latent}}$ 显式拉近不同模态编码 |
| 条件组合 | 固定条件类型 | 支持任意组合的异构条件，推理时可灵活增删 |

联合 VAE 包含多个模态专属编码器和一个共享的自回归解码器。运动序列被编码为一组隐 token $z = \{z^i\}_{i=1}^N$ 和一个全局 token $g \sim \mathcal{N}(\mu_g, \sigma_g)$，条件信号则通过对应编码器映射至同一隐空间。训练损失为：

$$\mathcal{L}_{\mathrm{JointVAE}} = \mathcal{L}_{\mathrm{rec}} + \omega_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}} + \omega_{\mathrm{latent}} \mathcal{L}_{\mathrm{latent}} + \omega_{\mathrm{aux}} \mathcal{L}_{\mathrm{aux}}$$

其中 $\mathcal{L}_{\mathrm{latent}}$ 是跨模态隐空间对齐损失，确保不同条件编码在隐空间中具有一致的几何结构。消融实验证实，移除条件编码器后 PA-MPJPE 从 4.08 升至 5.21（DexYCB-All），验证了共享隐空间对齐的必要性。

### 3. 视觉特征提取：手部感知机替代检测裁剪流水线

**Changed Slot：视觉输入处理**

| 维度 | Baseline 做法 | UniHand 做法 |
|------|--------------|-------------|
| 输入处理 | 基于手部检测的区域裁剪与对齐，丢弃环境上下文 | 冻结视觉骨干（DINO-v2）提取**全帧密集标记** |
| 特征筛选 | 裁剪后直接编码 | 手部感知机通过可学习手部 token 对密集标记做注意力，筛选手部相关 token |
| 上下文保留 | 丢弃物体与环境信息 | 保留环境与交互物体上下文 |

手部感知机的核心机制是：引入一组可学习的手部 token $H = \{H_i\}_{i=1}^N$ 和一个初始化姿态 token $a^1$ 作为 Query，对冻结视觉骨干输出的全帧密集标记 $v$ 执行缩放点积注意力：

$$\operatorname{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \operatorname{Softmax}(\mathbf{Q}\mathbf{K}^T / \sqrt{d_k}) \mathbf{V}$$

其中 Query 和 Key 分别施加 1D 和 3D 旋转位置编码（RoPE），以注入时序与空间位置信息：

$$\mathbf{Q} = \mathrm{RoPE}(\mathrm{LayerNorm}(W_{\mathbf{Q}}(a^1, H), P_{\mathrm{1D}}))$$
$$\mathbf{K} = \mathrm{RoPE}(\mathrm{LayerNorm}(W_{\mathbf{K}}(v), P_{\mathrm{3D}}))$$
$$\mathbf{V} = \operatorname{LayerNorm}(W_{\mathbf{V}}(v))$$

该模块每帧输出一个单一手部特征 token $h^i$，随后被注入扩散去噪网络的注意力层。消融实验表明，移除手部感知机后 PA-MPJPE 从 4.08 急剧退化至 7.81（性能下降约 91%），证明该模块是利用全帧视觉信息的关键瓶颈。

### 4. 坐标空间建模：规范坐标系解耦相机与手部运动

**Changed Slot：坐标空间建模**

| 维度 | Baseline 做法 | UniHand 做法 |
|------|--------------|-------------|
| 静态相机 | 相机坐标系，坐标连续 | 以首帧定义的**规范相机空间**，与相机坐标系等价 |
| 动态相机 | 相机坐标系下运动不连续，或需外部 SLAM 估计世界轨迹 | 规范相机空间自动解耦相机运动与手部运动，无需显式外参 |
| 轨迹恢复 | 依赖外部轨迹估计 | 直接生成规范空间运动，可后处理映射至世界坐标系 |

UniHand 在规范相机空间中生成运动，该空间由视频首帧的相机位姿定义。这使得模型在静态和动态相机场景下均能保持运动连续性，无需依赖外部相机标定或 SLAM 系统。如图 2 所示，在动态相机拍摄的魔方操作场景中，UniHand 在规范空间下生成平滑的手部轨迹，而传统方法因相机运动导致坐标跳变。但需注意，规范坐标系虽无需外参，其在世界坐标系下的轨迹重建精度（G-MPJPE 63.97）相比使用显式相机轨迹的方法（如 Dyn-HaMR 的 59.04）仍有差距。

### 5. 扩散模型设计：预测干净隐变量而非噪声

在共享隐空间上，UniHand 训练一个条件去噪扩散模型。与标准 DDPM 预测噪声不同，UniHand 的去噪器 $G_\theta$ 直接预测干净隐变量 $\hat{z}_0 = G_\theta(z_t, t, C)$，反向过程均值由预测的干净隐变量和当前噪声隐变量共同计算：

$$\mu_t = \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1-\bar{\alpha}_t}\hat{z}_0 + \frac{\sqrt{\alpha_t}(1-\bar{\alpha}_{t-1})}{1-\bar{\alpha}_t}z_t$$

这一设计选择有利于保持时序一致性，因为直接预测干净隐变量比预测噪声更容易约束帧间连续性。消融实验显示，引入 3D RoPE 后 PA-MPJPE 从 4.65 降至 4.08，证明时空位置编码对扩散模型中的时序建模至关重要。

### 创新总结

UniHand 的四项 changed slot 形成了一条完整的因果链：**联合 VAE** 解决了异构条件的对齐与融合问题，**手部感知机**突破了传统检测裁剪流水线的信息瓶颈，**规范坐标系**消除了动态相机下的运动不连续性，**预测干净隐变量的扩散设计**则强化了时序一致性。这些创新相互依赖——没有联合 VAE 的共享隐空间，手部感知机的视觉 token 与结构化条件无法有效融合；没有规范坐标系，动态相机下的运动先验无法在隐空间中一致表达。消融实验中多模态条件的互补效果（$c_{\text{vision}} + c_{\text{3D}}$ 将 PA-MPJPE 进一步降至 3.48）进一步验证了这一协同设计。

UniHand 将 4D 手部运动估计与生成统一为**条件运动合成**任务，核心由两大模块串联构成：**联合变分自编码器（Joint VAE）** 与 **潜在扩散模型（Latent Diffusion Model）**，如 Figure 1 所示。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_upUl6hMYwy/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the UniHand framework. (I) The Joint VAE aligns motion and condition encoders within a shared latent space. An autoregressive decoder iteratively reconstructs motion to preserve temporal consistency. (II) The latent diffusion model is trained on this latent space, where multimodal conditions are fused, and hand-relevant vision tokens are integrated into the denoiser*

### 输入与输出流

给定一段长度为 $N$ 的手部运动序列 $\boldsymbol{x} = \{x^i\}_{i=1}^N$ 及异构条件集合 $C$（可包含视频帧、2D/3D 骨架关键点、MANO 参数等），UniHand 的目标是学习条件分布 $p(\boldsymbol{x} | C)$。整个流水线分两阶段运作：

1. **Joint VAE 阶段**：将运动序列与多模态条件信号压缩至共享隐空间。运动编码器将 $\boldsymbol{x}$ 映射为一组潜在运动 token $z = \{z^i\}_{i=1}^N$ 及全局 token $g \sim \mathcal{N}(\mu_g, \sigma_g)$；条件编码器则将 $C$ 中的结构化信号（骨架、MANO 参数等）编码为对齐的隐表示。自回归解码器以锚点 token、运动隐 token 和全局 token 为条件，逐段重建运动序列，保证时序一致性。

2. **潜在扩散模型阶段**：在 Joint VAE 建立的隐空间上执行条件去噪扩散。去噪网络 $G_\theta$ 并非预测噪声，而是直接预测干净隐变量 $\hat{z}_0 = G_\theta(z_t, t, C)$，以增强时序连贯性。视觉条件通过**手部感知机（Hand Perceptron）** 注入：冻结的 DINO-v2 视觉骨干从全帧图像中提取密集视觉 token，手部感知机以可学习手部 token 和初始化手部姿态 token 为查询，利用 3D 旋转位置编码（3D RoPE）对视觉 token 进行注意力聚合，每帧输出单一手部特征 token $h^i$，并在每个去噪步中通过注意力层融入去噪网络。

### 关键设计决策

- **规范相机空间**：所有运动在首帧定义的规范坐标系中生成，解耦相机运动与手部运动，使模型同时适用于静态与动态相机，无需显式外参。
- **预测干净隐变量而非噪声**：相比标准扩散的噪声预测，直接预测 $\hat{z}_0$ 有助于维持运动序列的时序一致性。
- **全帧视觉处理**：摒弃传统检测-裁剪流水线，通过手部感知机从完整帧中直接关注手部相关 token，保留环境与交互物体上下文，这是模型在严重遮挡下保持鲁棒的核心机制（消融实验证实移除该模块后 PA-MPJPE 从 4.08 mm 退化至 7.81 mm）。

### 模块关系总结

Joint VAE 负责将异构条件与运动序列对齐至共享隐空间，提供紧凑、解耦的表示；潜在扩散模型在此空间上进行灵活的条件融合与高质量运动合成。手部感知机作为视觉条件与扩散模型之间的桥梁，使模型能同时利用结构化信号（骨架、MANO）与稠密视觉细节，实现统一的估计与生成。

### 3.1 统一条件运动生成框架

UniHand将手部运动估计与生成统一建模为条件运动合成问题。给定长度为 $N$ 的手部运动序列 $\boldsymbol{x} = \{ x^i \}_{i=1}^N$ 和条件信号集合 $C$（可包含视频帧、2D/3D骨架关键点及可选的手部姿态参数），框架由两个核心组件构成：**联合变分自编码器（Joint VAE）** 和 **潜在扩散模型（Latent Diffusion Model）**。

Joint VAE负责将运动序列与异构条件信号映射至共享隐空间，形成统一的潜在表示；扩散模型则在该隐空间上执行条件去噪，融合多模态条件并合成运动。整体架构如 Figure 1 所示。

### 3.2 联合变分自编码器（Joint VAE）

Joint VAE包含多个模态专用编码器和一个共享的自回归解码器。其核心功能是将运动序列和结构化条件（2D/3D骨架、MANO参数等）编码为共享的潜在token表示。

运动编码器将每帧手部姿态映射为潜在运动token $z = \{ z^i \}_{i=1}^N$，同时预测全局运动token的分布参数，从中采样得到全局token $g \sim \mathcal{N}(\mu_g, \sigma_g)$。条件编码器则将各类结构化条件信号对齐至同一隐空间，实现跨模态的语义一致。

训练总损失由四项加权求和构成：

$$\mathcal{L}_{\mathrm{JointVAE}} = \mathcal{L}_{\mathrm{rec}} + \omega_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}} + \omega_{\mathrm{latent}} \mathcal{L}_{\mathrm{latent}} + \omega_{\mathrm{aux}} \mathcal{L}_{\mathrm{aux}}$$

其中 $\mathcal{L}_{\mathrm{rec}}$ 为运动重建损失，$\mathcal{L}_{\mathrm{KL}}$ 为KL散度正则项，$\mathcal{L}_{\mathrm{latent}}$ 为隐空间对齐损失（确保不同模态条件映射至一致表示），$\mathcal{L}_{\mathrm{aux}}$ 为辅助损失（如关节点位置监督）。自回归解码器基于锚点token、运动隐token和全局token逐步重建完整运动片段，保证时序一致性。

### 3.3 潜在扩散模型

扩散模型在Joint VAE建立的共享隐空间上执行条件去噪。与传统噪声预测不同，UniHand的去噪网络 $G_\theta$ 直接预测干净隐变量 $\hat{z}_0 = G_\theta(z_t, t, C)$，以获得更好的时序连贯性。

反向过程的均值由预测的干净隐变量和当前噪声隐变量共同计算：

$$\mu_t = \frac{\sqrt{\bar{\alpha}_{t-1}} \beta_t}{1 - \bar{\alpha}_t} \hat{z}_0 + \frac{\sqrt{\alpha_t} (1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t} z_t$$

其中 $\bar{\alpha}_t$ 为累积噪声调度参数，$\beta_t$ 为单步噪声方差，$z_t$ 为第 $t$ 步的噪声隐变量。该公式定义了从 $z_t$ 向 $z_{t-1}$ 过渡的均值，是去噪采样的核心计算。

### 3.4 手部感知机（Hand Perceptron）

手部感知机是视觉信息利用的关键模块。传统方法依赖手部检测与裁剪，丢弃环境上下文且坐标不连续。UniHand采用冻结的预训练视觉骨干（DINO-v2）提取全帧密集视觉token $v$，由手部感知机通过注意力机制从中筛选手部相关特征。

模块使用一组可学习手部token $H = \{H_i\}_1^N$ 和初始化手部姿态token $a^1$ 作为查询（Query），对视觉token计算注意力。查询、键、值的计算方式为：

$$\mathbf{Q} = \mathrm{RoPE}(\mathrm{LayerNorm}(W_{\mathbf{Q}}(a^1, H), P_{\mathrm{1D}}))$$

$$\mathbf{K} = \mathrm{RoPE}(\mathrm{LayerNorm}(W_{\mathbf{K}}(v), P_{\mathrm{3D}}))$$

$$\mathbf{V} = \mathrm{LayerNorm}(W_{\mathbf{v}}(v))$$

注意力机制采用标准缩放点积形式：

$$\mathrm{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \mathrm{Softmax}(\mathbf{Q}\mathbf{K}^T / \sqrt{d_k}) \mathbf{V}$$

其中查询使用1D位置编码 $P_{\mathrm{1D}}$（沿时间轴），键使用3D位置编码 $P_{\mathrm{3D}}$（融入空间位置信息），值直接使用视觉token的线性投影。每帧输出单一手部特征token $h^i$，随后通过注意力层融入去噪网络的每一步去噪过程，使扩散模型能够同时利用结构化条件与视觉细节。

### 3.5 遮挡程度计算

为评估模型在不同遮挡条件下的鲁棒性，DexYCB数据集的遮挡比例通过掩膜比较计算：

$$r_{\mathrm{occ}} = \frac{|M_{\mathrm{hand}}| - |M_{\mathrm{hand}} \cap M_{\mathrm{vis}}|}{|M_{\mathrm{hand}}|}$$

其中 $M_{\mathrm{hand}}$ 为完整手部掩膜，$M_{\mathrm{vis}}$ 为可见区域掩膜，分子表示被遮挡的手部像素数，分母为手部总像素数。该指标将测试样本划分为不同遮挡级别（25-50%、50-75%、75-100%），用于细粒度性能分析（见 Table 1）。

## 实验与关键发现

### 主实验结果

UniHand在三个主流基准数据集上均取得最优性能，涵盖相机坐标系与世界坐标系、静态与动态相机、不同遮挡程度等多种评估条件。

**DexYCB数据集（Table 1）** 是该领域最广泛使用的评估基准。UniHand在整个测试集上取得PA-MPJPE **4.08 mm**，相比此前最好的视频方法**HaWoR**（Zhang et al., 2025）的4.76 mm降低14.3%，同时优于所有图像方法和视频方法。在不同遮挡程度下，UniHand均保持领先：轻遮挡（25-50%）下PA-MPJPE为4.22 mm，中遮挡（50-75%）下为4.25 mm，重遮挡（75-100%）下仅为**4.26 mm**，而HaWoR在重遮挡下为5.07 mm，UniHand的优势扩大至16.0%。AUC指标同样全面领先，整体AUC达到0.918。这组结果直接验证了UniHand将估计与生成统一为条件运动合成的核心设计——即使手部大面积不可见，模型仍能通过隐空间中的运动先验和视觉上下文线索恢复合理姿态。

**HO3D数据集（Table 2）** 用于评估跨域泛化能力。UniHand在相机坐标系下取得PA-MPJPE **6.7 mm**，优于**WiLoR**（Potamias et al., 2025）的7.5 mm（降幅10.7%），AUC达到0.866。值得注意的是，UniHand仅在DexYCB上训练，未使用HO3D数据进行微调，表明联合VAE学习到的共享隐空间表示具有良好的域迁移能力。

**HOT3D数据集（Table 3）** 包含动态相机场景，是世界坐标系评估的标准基准。UniHand在世界空间PA-MPJPE上取得**4.76 mm**，优于HaWoR的5.47 mm（降幅13.0%）。在加速度误差（AccEr）指标上，UniHand为**4.93 m/s²**，优于**Dyn-HaMR**（Yu et al., 2025）的5.16 m/s²（降幅4.5%），表明规范坐标系设计有效解耦了相机运动与手部运动，在不依赖显式外参的情况下仍能生成时间连续的运动序列。

### 消融实验分析

Table 4系统验证了各核心组件的贡献，所有消融均在DexYCB-All上进行。

**手部感知机（Hand Perceptron）是关键模块。** 移除该模块后，PA-MPJPE从4.08 mm急剧退化至**7.81 mm**（性能下降91%），证明从全帧密集视觉标记中通过注意力机制筛选手部相关token的设计不可替代。若仅使用简单的区域裁剪而不保留环境上下文，模型在遮挡场景下将丧失关键的空间参照信息。

**条件编码器（Condition Encoder）** 的移除导致PA-MPJPE升至5.21 mm，验证了联合VAE将异构条件信号对齐至共享隐空间的必要性。没有这一对齐机制，扩散模型无法有效融合多模态条件。

**预训练视觉骨干** 的影响显著：使用未预训练的视觉骨干时PA-MPJPE升至6.52 mm，表明DINO-v2提供的强语义特征对后续手部感知机的注意力筛选至关重要。

**3D RoPE位置编码** 的移除使PA-MPJPE升至4.65 mm，证明3D旋转位置编码有助于扩散模型中的时空建模，使去噪网络能感知各帧token在空间中的相对位置关系。

**多模态条件互补** 的实验尤为关键：当同时使用视觉帧和3D骨架作为条件（c_vision + c_3D）时，PA-MPJPE进一步降至**3.48 mm**，优于单一条件配置。这证实了联合VAE的设计初衷——结构化信号（骨架）提供精确的姿态约束，视觉信号提供环境上下文和遮挡补偿，两者在共享隐空间中互补融合。

### 定性分析

**Figure 5** 对比了UniHand与**HaMeR**（Pavlakos et al., 2024）的时序连续性。HaMeR作为逐帧图像方法，在快速运动或遮挡帧间产生明显的姿态跳变；UniHand通过扩散模型在隐空间中进行时序建模，生成的运动序列更加平滑连续。

**Figure 6** 展示了严重自遮挡场景下的左右手分类鲁棒性。当手部大面积自遮挡时，HaMeR错误地将右手分类为左手，导致重建质量严重下降；UniHand利用手部感知机从全帧视觉token中提取的空间上下文信息，能够正确区分左右手并保持稳定的姿态重建。

**Figure 7** 展示了手部完全不可见帧的处理能力。当视频帧中手部暂时离开画面或被完全遮挡时，HaMeR无法估计有效姿态；UniHand通过隐空间中的运动先验和时序建模，能够维持合理的重建结果，不会因单帧缺失而崩溃。

### 局限性与失败模式

尽管UniHand在主要指标上表现优异，分析中仍存在若干值得关注的局限：

1. **世界坐标系下的轨迹精度**：在HOT3D数据集上，UniHand的G-MPJPE（全局对齐后）为63.97 mm，逊于Dyn-HaMR的59.04 mm。规范坐标系虽避免了显式外参依赖，但在世界空间下的绝对轨迹重建仍存在累积漂移，这是不依赖SLAM方法的固有瓶颈。

2. **双手场景效率**：当前模型假设单只手输入，双手场景需分别推理两次，缺乏手-手交互建模，且推理时间翻倍。

3. **域外泛化**：训练数据主要来自第一人称抓取场景（DexYCB、HOT3D），对第三人称视角、自由手势或极端光照条件的泛化性尚未验证。

4. **上游依赖**：推理过程依赖预训练的2D关键点检测器（HaMeR ViT骨干）提供条件信号，该模块的检测误差会直接传播至UniHand的运动生成结果。

### 补充图表

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_upUl6hMYwy/figures/002_Table_1.jpg]]
*Table 1: Quantitative comparison of SoTA hand pose and motion modeling methods on the DexYCB test set in the camera coordinate space. Results are reported in terms of MPJPE (mm) and AUC, with statistics across different occlusion levels*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_upUl6hMYwy/figures/003_Table_2.jpg]]
*Table 2: Quantitative comparison of baseline hand pose estimation methods on the HO3D dataset in the camera coordinate space. Results are reported in terms of MPJPE (mm), AUC scores, and F-scores*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_upUl6hMYwy/figures/005_Table_4.jpg]]
*Table 4: Ablation studies on the core components, design choices, and different condition configurations during inference, evaluated on the DexYCB and HOT3D datasets. Results are reported in terms of MPJPE (mm) under different alignment strategies and AUC scores*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_upUl6hMYwy/figures/004_Figure_2.jpg]]
*Figure 2: Visualization of generated hand poses and trajectories. The first example shows a static camera scenario where the subject picks up a red bowl, with significant hand occlusion. The second example is recorded with a dynamic camera, where the subject picks up and manipulates a magic cube, involving large hand movements. UniHand produces more accurate hand motion by modeling motions in a canonical coordinate space, even without relying on explicit camera extrinsics*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_upUl6hMYwy/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative comparison between HaMeR and our UniHand. Our method generates more continuous and accurate hand pose sequences compared to HaMeR*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_upUl6hMYwy/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative comparison between HaMeR and our UniHand. In cases of severe hand selfocclusion, HaMeR misclassifies the right hand as the left hand, resulting in poor reconstruction quality, whereas UniHand generates reliable and consistent hand motions*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_upUl6hMYwy/figures/010_Figure_7.jpg]]
*Figure 7: Qualitative comparison between HaMeR and our UniHand. HaMeR fails to estimate valid poses in video frames where the hand is absent, whereas UniHand maintains stable reconstructions by exploiting vision perception and temporal modeling*

## 定位与知识库关联

### 任务定位：从分离式建模到统一条件运动合成

UniHand 将 4D 手部运动估计与生成统一为**条件运动合成**这一单一范式，打破了此前该领域“估计归估计、生成归生成”的分离格局。传统方法将手部姿态估计视为逐帧回归问题，将运动生成视为无条件或弱条件先验学习问题，两者共享的运动先验与跨模态对齐能力几乎为零。UniHand 的核心贡献在于：通过联合 VAE 构建跨模态共享隐空间，并在其上训练条件扩散模型，使得**估计任务本质上成为“以视觉观测为条件的运动生成”**，而生成任务则是“以稀疏骨架或参数为条件的运动合成”——二者在模型层面完全统一。

这一统一范式直接回应了领域内的一个长期瓶颈：异构条件信号（RGB 视频帧、2D/3D 骨架、MANO 参数）缺乏有效的融合机制，导致运动先验难以跨任务迁移，尤其在遮挡或时序不完整输入下性能急剧退化。

### 与基线方法的关系：关键设计差异与性能跨越

UniHand 在 DexYCB、HO3D、HOT3D 三个主流基准上均取得最优结果，但其与各基线的关系不仅是数值超越，更体现了架构选择带来的质变。

**图像级方法对比。** **HaMeR**（Pavlakos et al., 2024）和 **WiLoR**（Potamias et al., 2025）代表基于 ViT 的图像手部姿态估计路线，依赖手部检测与区域裁剪，丢弃环境上下文，且逐帧独立推理缺乏时序一致性。UniHand 冻结 DINO-v2 骨干从**全帧密集标记**中提取特征，由手部感知机（Hand Perceptron）以注意力机制筛选与手部相关的 token，保留了物体交互与环境线索。在 DexYCB 全测试集上，UniHand 的 PA-MPJPE 为 4.08 mm，显著优于 HaMeR 的 6.43 mm（↓36.5%）和 WiLoR 的 5.69 mm（↓28.3%）。在最高遮挡档位（75-100%），UniHand 仅 4.26 mm，而 WiLoR 为 5.92 mm，**MeshGraphormer**（Lin et al., 2021）为 7.38 mm，**HandOccNet**（Park et al., 2022）为 8.52 mm——差距在遮挡加剧时反而拉大，表明全帧视觉感知与隐空间时序建模对遮挡鲁棒性的关键作用。

**视频级方法对比。** **Deformer**（Fu et al., 2023）通过时序 Transformer 建模视频手部姿态，但仍在相机坐标系下操作，动态相机场景下运动连续性差。**HaWoR**（Zhang et al., 2025）解耦相机与手部运动，是此前 DexYCB 上的最优视频方法（PA-MPJPE 4.76 mm），但其视觉处理仍依赖手部检测裁剪。UniHand 以规范坐标系（首帧定义的 canonical camera space）统一静态与动态相机场景，无需显式外参估计，在 DexYCB 上以 4.08 mm 超越 HaWoR 14.3%。在 HOT3D 世界坐标系评估中，**Dyn-HaMR**（Yu et al., 2025）利用多阶段动态相机处理取得 G-MPJPE 59.04 mm 和 AccEr 5.16 m/s²，UniHand 的 G-MPJPE 为 63.97 mm（略逊于 Dyn-HaMR），但 AccEr 以 4.93 m/s² 更优——这揭示了一个值得关注的权衡：规范坐标系虽免除了对外部 SLAM 或标定的依赖，但在世界坐标系下的绝对轨迹精度仍不及显式利用相机轨迹的方法。

### 核心设计选择的知识库贡献

**联合 VAE 与共享隐空间。** 此前多模态条件融合的主流做法是简单拼接或独立编码后送入生成器，缺乏跨模态对齐的显式监督。UniHand 的联合 VAE 将 MANO 参数、2D/3D 骨架等结构化条件与运动序列映射至同一隐空间，并通过隐空间对齐损失（$\mathcal{L}_{\mathrm{latent}}$）显式约束模态间一致性。这一设计使得模型在推理时可**灵活组合异构条件**——消融实验显示，同时使用视觉帧和 3D 骨架作为条件（c_vision + c_3D）可将 PA-MPJPE 进一步降至 3.48 mm，验证了多模态互补的实际收益。

**手部感知机与全帧视觉处理。** 传统手部检测-裁剪流水线在遮挡、截断或手部不可见时失效，且丢弃了物体与场景上下文。手部感知机通过可学习的手部 token 对 DINO-v2 全帧密集标记执行交叉注意力，每帧输出单一手部特征 token，随后注入扩散去噪网络。消融实验表明，移除该模块后 PA-MPJPE 从 4.08 退化至 7.81（性能下降 91%），是单一组件中影响最大的设计选择。这为“密集视觉特征中注意力筛选优于显式检测裁剪”提供了强证据。

**规范坐标系建模。** 在动态相机场景中，相机坐标系下的手部运动包含相机自身运动，导致时序不连续。UniHand 以首帧定义规范坐标系，将手部运动与相机运动解耦，无需外参估计。这一设计在 HOT3D 的 PA-MPJPE 上取得 4.76 mm（vs HaWoR 5.47 mm），但 G-MPJPE 的劣势表明，规范坐标系的累积漂移问题在长序列世界坐标系评估中仍待解决。

### 适用边界与已知局限

1. **单手假设。** 当前模型仅支持单只手推理，双手场景需分别处理，缺乏手-手交互建模能力，效率受限。
2. **训练数据分布。** 训练数据主要来自第一人称抓取场景（DexYCB、HOT3D），对第三人称视角、自由手势、极端视角变化的泛化性未经验证。
3. **外部依赖链。** 推理依赖预训练的 2D 关键点检测器（HaMeR ViT 骨干）提供条件信号，该模块的误差会传播至最终运动生成，形成误差累积链。
4. **世界坐标系精度。** 规范坐标系虽无需外参，但在世界坐标系下的轨迹重建精度（G-MPJPE 63.97 mm）相比利用显式相机轨迹的 Dyn-HaMR（59.04 mm）仍有差距，累积漂移是核心瓶颈。
5. **端到端能力缺失。** 模型未实现从原始视频到世界坐标系运动轨迹的完全端到端推理，仍依赖分离的视觉骨干和关键点检测器。

### 开放问题与后续方向

1. **多手交互统一建模。** 如何扩展共享隐空间以支持多手、手-物体、手-手关系的联合推理，是走向实用化手部运动理解的关键一步。
2. **端到端相机-手部联合恢复。** 能否在不依赖外部 SLAM 或关键点检测器的情况下，从原始视频端到端地同时恢复相机轨迹与手部运动，消除外部依赖的误差传播。
3. **规范坐标系与相机运动的融合。** 如何将规范坐标系下的运动与估计的相机运动融合，以降低世界坐标系下的累积漂移，弥合与显式 SLAM 方法的精度差距。
4. **向全身姿态与交互扩展。** 该统一框架的隐空间对齐与扩散生成思路能否扩展到全身姿态估计或人手-物体交互的联合建模，是值得探索的方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/UniHand_A_Unified_Model_for_Diverse_Controlled_4D_Hand_Motion_Modeling_fb445fed84c1.pdf]]
