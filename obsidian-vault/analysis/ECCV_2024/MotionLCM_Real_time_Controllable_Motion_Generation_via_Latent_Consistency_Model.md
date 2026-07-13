---
title: "MotionLCM: Real-time Controllable Motion Generation via Latent Consistency Model"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/MotionLCM_Real_time_Controllable_Motion_Generation_via_Latent_Consistency_Model.pdf
project_link: https://dai-wenxun.github.io/MotionLCM-page
code_link: null
aliases:
- MotionLCM
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过潜在一致性蒸馏（Latent Consistency Distillation）将MLD转化为一致性模型，实现1~4步快速推理；并引入运动ControlNet在潜在空间中处理控制信号，同时利用冻结VAE解码器恢复运动空间以施加显式控制损失（L_control），从而实现高效且精确的实时可控运动生成。
primary_logic: 首次将一致性模型从图像域推广到运动生成，证明了潜在一致性蒸馏可以在大幅减少采样步骤的同时保持生成质量；并且通过在潜在控制网络之外增加运动空间的显式监督，解决了潜在空间控制信号语义缺失的关键问题，实现了速度与可控性的统一。
claims:
- MotionLCM用1步推理即可达到与MLD（50步DDIM）相当或更优的文本-运动生成质量，同时推理速度提升一个数量级（AITS 0.030 vs 0.225）
- 在运动控制任务上，MotionLCM（1步）比OmniControl快1929倍，且平均控制误差降低32.7%（Avg.err. 0.1127 vs 0.1673）
- 消融实验表明，在潜在空间控制之外加入运动空间显式控制损失（L_control）可显著降低定位误差（Loc.err. 从0.0344降至0.0147）
- HumanML3D T2M 上 AITS (s)↓ = 0.030 (1-step)
---

# MotionLCM: Real-time Controllable Motion Generation via Latent Consistency Model

> [!tip] 核心洞察
> 首次将一致性模型从图像域推广到运动生成，证明了潜在一致性蒸馏可以在大幅减少采样步骤的同时保持生成质量；并且通过在潜在控制网络之外增加运动空间的显式监督，解决了潜在空间控制信号语义缺失的关键问题，实现了速度与可控性的统一。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionLCM：基于潜在一致性模型的实时可控运动生成 |
| 英文题名 | MotionLCM: Real-time Controllable Motion Generation via Latent Consistency Model |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2404.19759) · [Project](https://dai-wenxun.github.io/MotionLCM-page) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MotionLCM |
| Dataset | HumanML3D T2M, HumanML3D Control |

> [!tip] 效果简介
> - HumanML3D T2M 上，AITS (s)↓ 0.030 (1-step) vs 0.225 (MLD* 50-step) (7.5x faster)；FID↓ 0.467 (1-step) vs 0.450 (MLD*) (+0.017)；R-Precision Top-1↑ 0.502 (1-step) vs 0.504 (MLD*) (-0.002)。
> - HumanML3D Control 上，Avg. err.↓ 0.1127 (1-step, LC&MC) vs 0.1673 (OmniControl) (-0.0546)；Inference speed ~30ms (1-step) vs ~81s (OmniControl) (~2700x faster (原文1929×相比MLD))。

## 概要

**问题瓶颈**：现有文本到运动扩散模型（如 **MDM** (Tevet et al., ICLR 2022)、**MLD**）推理速度缓慢，单序列生成需0.2~24秒，难以满足实时交互需求。同时，在潜在扩散模型的压缩空间中实现时空可控运动生成存在根本性困难——潜在特征缺乏显式运动语义，直接注入控制信号会导致语义错位。

**核心方法**：MotionLCM 通过**潜在一致性蒸馏**（Latent Consistency Distillation）将预训练的潜在运动扩散模型 MLD 转化为一致性模型，实现1~4步快速推理。在此基础上，引入**运动 ControlNet** 在潜在空间处理控制信号，并利用冻结的 VAE 解码器将潜在向量恢复至运动空间，施加显式控制损失 $\mathcal{L}_{\mathrm{control}}$，从而弥补潜在空间语义缺失的关键缺陷。

**核心洞察**：首次将一致性模型从图像域推广至运动生成，证明潜在一致性蒸馏可在大幅减少采样步数的同时保持生成质量；通过在潜在控制网络之外增加运动空间的显式监督，解决了速度与可控性的统一问题。

**主要结果**：
- **文本到运动生成**：MotionLCM 以1步推理（约30ms）达到与 MLD（50步 DDIM）相当或更优的生成质量，推理速度提升约7.5倍（AITS 0.030 vs 0.225），FID 为 0.467（Table 1）。
- **可控运动生成**：在 HumanML3D 控制任务上，MotionLCM（1步）的控制误差较 **OmniControl** (Xie et al., ICLR 2024) 降低32.7%（Avg. err. 0.1127 vs 0.1673），推理速度提升约1929倍（Table 2）。
- **消融验证**：运动空间显式控制损失使定位误差从0.0344降至0.0147（Table 4）；动态训练 CFG 范围 [5, 15] 和 Huber 损失对蒸馏质量至关重要（Table 3）。

**方法定位**：MotionLCM 属于**潜在空间一致性运动生成**范式，在方法谱系上位于扩散加速蒸馏与可控生成的交叉点。其两阶段训练流程——先进行 CFG 增强的潜在一致性蒸馏，再冻结基础模型训练运动 ControlNet——为实时可控运动生成提供了可复用的技术路线。



### 问题背景

文本驱动的三维人体运动生成旨在根据自然语言描述合成逼真的人体动作序列，在游戏、影视、虚拟人等领域具有广泛应用前景。近年来，扩散模型（Diffusion Models）在该任务上取得了显著进展，代表性工作包括 **MDM**（Tevet et al., ICLR 2022）、**MotionDiffuse**（Zhang et al., arXiv 2022）以及 **MLD**（Chen et al., 2023）。其中，MLD 通过在潜在空间中进行扩散去噪，将推理时间从 MDM 的约 24 秒压缩至约 0.2 秒，大幅提升了效率。

然而，现有方法的推理速度仍难以满足实时应用需求。如图 2 所示，基于扩散的运动生成模型普遍存在“速度-质量”权衡困境：MDM 生成质量尚可但推理极慢（约 24 秒/序列），MLD 虽有所加速（约 0.225 秒/序列），但距离实时交互（< 50 ms）仍有数量级差距。这一瓶颈的根本原因在于，扩散模型依赖迭代去噪过程，通常需要数十步甚至上百步采样才能收敛到高质量样本。

### 可控运动生成的挑战

除生成速度外，可控性是可部署运动生成系统的另一核心需求。实际应用中，用户往往需要指定特定关节的轨迹（如手部到达某个位置）或初始姿态序列，以实现自回归式的实时运动合成。然而，在潜在扩散模型中实现时空可控运动生成面临独特挑战：

- **潜在空间缺乏显式运动语义**：MLD 等模型通过 VAE 将原始运动序列压缩到低维潜在空间，该压缩过程缺乏显式时序建模，导致潜在特征与关节位置、速度等物理量之间没有直接对应关系，难以直接施加控制信号。
- **现有控制方法速度慢**：以 **OmniControl**（Xie et al., ICLR 2024）为代表的方法在运动空间进行操控，虽能实现较精确的控制，但其推理依赖迭代优化或扩散采样，耗时约 81 秒/序列，无法满足实时需求。

### 一致性模型的机遇

一致性模型（Consistency Models）是近期提出的一类新型生成模型，其核心思想是学习一个直接映射，将 PF-ODE 轨迹上的任意点一步投影到其解（即干净样本），从而在保持生成质量的同时实现单步或少数步采样。该范式已在图像生成领域展现出巨大潜力，但在运动生成领域尚未被探索。

将一致性模型从图像域推广到运动域面临两个关键问题：

1. **蒸馏效率与质量平衡**：如何在潜在空间中有效蒸馏预训练的运动扩散模型，使单步采样即可达到与多步扩散相当的质量？
2. **潜在空间控制语义缺失**：如何在一致性模型的潜在空间中注入时空控制信号，同时弥补潜在特征缺乏显式运动语义的固有缺陷？

### 本文动机

针对上述问题，本文提出 **MotionLCM**（Motion Latent Consistency Model），核心动机包括：

1. **实现实时运动生成**：通过潜在一致性蒸馏（Latent Consistency Distillation），将 MLD 转化为一致性模型，实现 1-4 步快速推理（单步约 30 ms），推理速度相比 MLD 提升约 7.5 倍，相比 MDM 提升约 800 倍。
2. **实现高效可控生成**：引入运动 ControlNet 在潜在空间中处理控制信号，同时利用冻结的 VAE 解码器将潜在向量恢复至运动空间，施加显式控制损失（$\mathcal{L}_{\mathrm{control}}$），从而在保持推理效率的同时实现精确的时空可控运动生成。

本文首次将一致性模型从图像域推广到运动生成领域，并通过潜在空间控制与运动空间显式监督的双重机制，解决了速度与可控性难以兼得的关键问题。



## 核心方法与创新机理

MotionLCM 的核心创新在于将一致性模型从图像域首次推广到运动生成，并通过**潜在-运动空间双级联控制机制**解决了实时可控运动生成中的速度-精度矛盾。其关键创新点可归纳为以下三个层面：

### 1. 从扩散去噪到一致性映射：推理范式的根本转变

传统文本到运动扩散模型（如 **MDM** (Tevet et al., ICLR 2022)、**MLD**）遵循迭代去噪范式，需要 50~1000 步采样才能生成高质量序列，推理时间从约 0.2 秒（MLD）到约 24 秒（MDM）不等，难以满足实时应用需求。

MotionLCM 通过**潜在一致性蒸馏（Latent Consistency Distillation, LCD）**将 MLD 转化为一致性模型。其核心思想是学习一个一致性函数 $f_{\Theta}$，满足自一致性属性：

$$\pmb{f}(\mathbf{x}_t, t) = \pmb{f}(\mathbf{x}_{t'}, t'), \forall t, t' \in [\epsilon, T]$$

该函数将 PF-ODE 轨迹上的任意点直接映射到其解 $\mathbf{z}_0$，从而支持 1~4 步直接采样。蒸馏过程采用三网络架构（Fig. 4(a)）：
- **冻结的教师网络**（MLD 扩散模型）：提供教师预测 $\hat{\mathbf{z}}_0^*$
- **可训练的在线网络** $f_{\Theta}$：学习一致性映射
- **EMA 更新的目标网络** $f_{\Theta^-}$：提供一致性损失中的目标

核心损失函数为潜在一致性蒸馏损失：

$$\mathcal{L}_{\mathrm{LCD}}(\boldsymbol{\Theta}, \boldsymbol{\Theta}^-) = \mathbb{E}\left[ d\left( f_{\boldsymbol{\Theta}}(\mathbf{z}_{n+k}, t_{n+k}, w, \mathbf{c}), \boldsymbol{f}_{\boldsymbol{\Theta}^-}(\hat{\mathbf{z}}_n, t_n, w, \mathbf{c}) \right) \right]$$

其中 $\hat{\mathbf{z}}_n$ 通过融入无分类器引导（CFG）的 k 步 ODE 求解获得：

$$\hat{\mathbf{z}}_n \gets \mathbf{z}_{n+k} + (1 + w) \Phi(\mathbf{z}_{n+k}, t_{n+k}, t_n, \mathbf{c}) - w \Phi(\mathbf{z}_{n+k}, t_{n+k}, t_n, \emptyset)$$

这一蒸馏范式带来了**推理步数的根本性缩减**：从 MLD 的 50 步 DDIM 降至 1 步，推理速度提升约 7.5 倍（AITS 0.030 vs 0.225，Table 1），同时生成质量几乎无损（FID 0.467 vs 0.450）。

### 2. 潜在空间控制网络：速度与可控性的首次统一

在实现实时生成后，MotionLCM 进一步解决了在潜在空间中实现时空可控运动生成的挑战。核心难点在于：潜在特征缺乏显式运动语义，原生潜在扩散模型难以直接施加控制信号。

MotionLCM 引入**运动 ControlNet**（Fig. 4(b)），包含两个可训练模块：
- **轨迹编码器** $\Theta^b$（Transformer）：编码控制关节轨迹，输出全局特征 token
- **运动 ControlNet** $\Theta^a$：零初始化的控制网络，接收轨迹编码和噪声潜在向量，输出控制增强的潜在预测

训练时冻结 MotionLCM 主干，联合优化重建损失和控制损失：

$$\mathcal{L}_{\mathrm{recon}}(\Theta^a, \Theta^b) = \mathbb{E}\left[d\left(f_{\Theta^s}\left(\mathbf{z}_n, t_n, w, \mathbf{c}^*\right), \mathbf{z}_0\right)\right]$$

$$\Theta^a, \Theta^b = \underset{\Theta^a, \Theta^b}{\arg\min}(\mathcal{L}_{\mathrm{recon}} + \lambda \mathcal{L}_{\mathrm{control}})$$

这一设计使得 MotionLCM 在运动控制任务上比 **OmniControl** (Xie et al., ICLR 2024) 快约 1929 倍，且平均控制误差降低 32.7%（Avg.err. 0.1127 vs 0.1673，Table 2）。

### 3. 运动空间显式监督：弥补潜在空间语义缺失

MotionLCM 最具洞察力的设计在于**双重控制监督机制**。除在潜在空间通过 ControlNet 处理控制信号外，还利用冻结的 VAE 解码器 $\mathcal{D}$ 将潜在向量解码回运动空间，施加显式控制损失：

$$\mathcal{L}_{\mathrm{control}}(\Theta^a, \Theta^b) = \mathbb{E}\left[\frac{\sum_i \sum_j m_{ij} ||R(\hat{\mathbf{x}}_0)_{ij} - R(\mathbf{x}_0)_{ij}||_2^2}{\sum_i \sum_j m_{ij}}\right]$$

其中 $m_{ij}$ 为二进制关节掩码，$R(\cdot)$ 提取全局关节位置。这一设计的关键价值在于：**潜在空间的隐式控制无法保证解码后运动序列精确满足时空约束**，而运动空间的显式监督直接优化了最终输出层面的控制精度。

消融实验（Table 4）证实了这一设计的必要性：仅使用潜在空间控制时定位误差为 0.0344，加入运动空间控制损失后降至 0.0147，降幅达 57.3%。控制损失权重 $\lambda = 1.0$ 在控制精度与生成质量间取得最佳平衡。

### 创新总结

| 创新维度 | 基线方法 | MotionLCM | 关键证据 |
|---------|---------|-----------|---------|
| 推理范式 | MLD 需 50 步 DDIM | 1 步一致性采样（~30ms） | Table 1: AITS 0.030 vs 0.225 |
| 控制架构 | OmniControl 运动空间操控（~81s） | 潜在 ControlNet + 运动空间监督（~30ms） | Table 2: 速度快 1929×，误差降 32.7% |
| 监督机制 | 单一空间控制 | 潜在-运动双空间联合监督 | Table 4: Loc.err. 0.0344 → 0.0147 |

**需注意的局限性**：该方法依赖 MLD 的 VAE 压缩，该压缩缺乏显式时序建模，可能限制运动细节的保留；训练流程为两阶段（先蒸馏再训练 ControlNet），增加了训练复杂度；控制损失权重 $\lambda$ 需手动调节。



MotionLCM 的整体架构分为两个阶段：**运动潜在一致性蒸馏（Motion Latent Consistency Distillation）** 和 **潜在空间运动控制（Motion Control in Latent Space）**，如图 4 所示。两个阶段共享相同的 VAE 压缩骨干，但训练目标与模块构成各有侧重。

### 第一阶段：运动潜在一致性蒸馏

该阶段的目标是将预训练的潜在扩散运动模型 MLD 蒸馏为一致性模型，使生成过程从数十步去噪缩减至 1–4 步直接采样。

**数据流**：原始运动序列 $\mathbf{x}_0^{1:N}$ 首先经过冻结的 VAE 编码器 $E$ 压缩到潜在空间，得到潜在向量 $\mathbf{z}_0$。随后执行前向扩散加噪，得到 $n+k$ 步噪声潜在 $\mathbf{z}_{n+k}$。该噪声潜在同时送入三个网络：

- **冻结的教师网络**（即预训练的 MLD 扩散模型）：预测干净潜在 $\hat{\mathbf{z}}_0^*$，并经由 $k$ 步 ODE 求解器 $\Phi$ 估计出更干净的 $\hat{\mathbf{z}}_n$（见 Eq. (6)）。
- **可训练的在线网络** $f_\Theta$：直接从 $\mathbf{z}_{n+k}$ 预测干净潜在 $\hat{\mathbf{z}}_0$。
- **EMA 更新的目标网络** $f_{\Theta^-}$：以 $\hat{\mathbf{z}}_n$ 为输入，预测干净潜在。

核心训练机制是**自一致性约束**：通过潜在一致性蒸馏损失 $\mathcal{L}_{\mathrm{LCD}}$（Eq. (7)）强制在线网络与目标网络的输出保持一致。这等价于学习一个从 ODE 轨迹上任意点直接映射到解 $\mathbf{z}_0$ 的一致性函数 $f_\Theta$（参见 Fig. 3 的示意图）。蒸馏过程中，教师网络和目标网络均冻结，仅更新在线网络；目标网络的参数通过指数移动平均（EMA）从在线网络同步。

**关键设计选择**：蒸馏时采用 CFG 集成的方式（Eq. (6)），在训练过程中动态采样引导强度 $w \sim [w_{\min}, w_{\max}]$，使模型在推理时能灵活适应不同的 CFG 尺度。消融实验（Table 3）表明，动态 CFG 范围 $[5, 15]$ 优于固定 CFG $=7.5$（FID 从 0.568 降至 0.467），且 Huber 损失相比 L2 损失显著提升生成质量（FID 0.467 vs 0.622）。

### 第二阶段：潜在空间运动控制

在第一阶段获得高速生成的 MotionLCM 后，第二阶段引入运动 ControlNet 以实现可控运动生成。核心挑战在于：潜在空间的特征缺乏显式运动语义，难以直接施加空间-时序控制信号。MotionLCM 的解决方案是**双空间监督**——在潜在空间进行控制条件注入，同时在运动空间施加显式控制损失。

**新增模块**（Fig. 4(b)）：

- **轨迹编码器 $\Theta^b$**（Transformer 架构）：编码控制关节的初始轨迹（前 $\tau$ 帧的关节位置），输出全局特征 token。
- **运动 ControlNet $\Theta^a$**：以 MotionLCM 的权重初始化（零卷积层除外），接收轨迹编码和噪声潜在 $\mathbf{z}_n$，输出控制增强的潜在预测。

**训练流程**：冻结第一阶段训练好的 MotionLCM，仅训练 $\Theta^a$ 和 $\Theta^b$。总损失由两部分组成（Eq. (10)）：

$$\Theta^a, \Theta^b = \underset{\Theta^a, \Theta^b}{\arg\min}(\mathcal{L}_{\mathrm{recon}} + \lambda \mathcal{L}_{\mathrm{control}})$$

- **$\mathcal{L}_{\mathrm{recon}}$**（Eq. (8)）：潜在空间的重建损失，确保加入 ControlNet 后仍能恢复原始运动。
- **$\mathcal{L}_{\mathrm{control}}$**（Eq. (9)）：运动空间的显式控制损失。将 ControlNet 预测的潜在向量通过冻结的 VAE 解码器 $D$ 解码回运动空间，计算受控关节的全局位置与真实值之间的加权 MSE。权重 $m_{ij}$ 为二进制关节掩码，仅监督被控制关节的位置。

**双空间监督的必要性**：消融实验（Table 4）显示，仅在潜在空间施加控制（LC）时定位误差为 0.0344；加入运动空间显式控制损失（LC & MC）后，定位误差降至 0.0147，降幅达 57.3%。这验证了潜在控制信号语义缺失是核心瓶颈，而运动空间显式监督是解决该瓶颈的关键。

### 推理阶段

推理时，MotionLCM 支持 1–4 步直接采样。对于文本到运动生成，从随机噪声出发，经 1 步即可生成高质量运动（约 30 ms/序列）。对于可控运动生成，将控制轨迹编码后注入 ControlNet，同样在 1–4 步内完成。自回归生成范式（Fig. 1）中，前一段运动的最后 $\tau$ 帧作为时序控制信号，驱动下一段运动的生成，实现实时交互式运动合成。

![[assets/figures/papers/MotionLCM_Real-time_Controllable_Motion_Generation_via_Latent_Consistency_Model_aa7685020fdd/figures/001_Figure_1.jpg]]
*Figure 1: We propose MotionLCM, a real-time controllable motion latent consistency model. Our model uses the last few frames of the previous motion as temporal control signals to autoregressively generate the next motion in real-time under different text prompts. Green blocks denote the junctions. The numbers in red are the inference time*

### 补充图表

![[assets/figures/papers/MotionLCM_Real-time_Controllable_Motion_Generation_via_Latent_Consistency_Model_aa7685020fdd/figures/004_Figure_4.jpg]]
*Figure 4: The overview of MotionLCM. (a) Motion Latent Consistency Distillation (Sec. 3.2). Given a raw motion sequence*



### 运动潜在一致性蒸馏（Motion Latent Consistency Distillation）

MotionLCM 的核心是将一致性模型（Consistency Model）从图像域迁移到运动生成的潜在空间。该方法以预训练的 **MLD**（运动潜在扩散模型）为基础模型，通过潜在一致性蒸馏将其转化为支持少步采样的生成器。

蒸馏架构包含三个网络（Fig. 4(a)）：
- **冻结的教师网络**：原始 MLD 扩散模型，提供教师预测 $\hat{\mathbf{z}}_0^*$。
- **可训练的在线网络** $f_{\Theta}$：初始化为教师网络权重，接收带噪潜在向量 $\mathbf{z}_{n+k}$ 并预测干净潜在向量 $\hat{\mathbf{z}}_0$。
- **EMA 更新的目标网络** $f_{\Theta^-}$：接收经过 $k$ 步 ODE 求解器预估的更干净潜在向量 $\hat{\mathbf{z}}_n$，预测干净潜在向量。

蒸馏的核心思想源自一致性模型的自一致性属性（Eq. (1)）：

$$ \pmb{f}(\mathbf{x}_t, t) = \pmb{f}(\mathbf{x}_{t'}, t'), \quad \forall t, t' \in [\epsilon, T] $$

即同一 PF-ODE 轨迹上的任意点都应映射到同一解。为满足边界条件 $f_{\Theta}(\mathbf{x}, \epsilon) = \mathbf{x}$，采用跳跃连接参数化（Eq. (2)）：

$$ f_{\Theta}(\mathbf{x}, t) = c_{\mathrm{skip}}(t) \mathbf{x} + c_{\mathrm{out}}(t) F_{\Theta}(\mathbf{x}, t) $$

其中 $c_{\mathrm{skip}}(t)$ 和 $c_{\mathrm{out}}(t)$ 为时间相关的可微系数，$c_{\mathrm{skip}}(\epsilon) = 1$，$c_{\mathrm{out}}(\epsilon) = 0$。

蒸馏过程中，首先利用 ODE 求解器 $\Phi$ 从 $\mathbf{z}_{n+k}$ 进行 $k$ 步预估，得到更接近原点的 $\hat{\mathbf{z}}_n$。为融入无分类器引导（CFG），采用 CFG 增强的 $k$ 步 ODE 求解（Eq. (6)）：

$$ \hat{\mathbf{z}}_n \gets \mathbf{z}_{n+k} + (1 + w) \Phi(\mathbf{z}_{n+k}, t_{n+k}, t_n, \mathbf{c}) - w \Phi(\mathbf{z}_{n+k}, t_{n+k}, t_n, \emptyset) $$

其中 $w$ 为引导尺度，$\mathbf{c}$ 为文本条件，$\emptyset$ 为空条件。

潜在一致性蒸馏损失 $\mathcal{L}_{\mathrm{LCD}}$ 最小化在线网络与目标网络输出之间的差异（Eq. (7)）：

$$ \mathcal{L}_{\mathrm{LCD}}(\boldsymbol{\Theta}, \boldsymbol{\Theta}^-) = \mathbb{E}\left[ d\left( f_{\boldsymbol{\Theta}}(\mathbf{z}_{n+k}, t_{n+k}, w, \mathbf{c}), \boldsymbol{f}_{\boldsymbol{\Theta}^-}(\hat{\mathbf{z}}_n, t_n, w, \mathbf{c}) \right) \right] $$

其中 $d(\cdot, \cdot)$ 为距离度量函数，MotionLCM 选用 **Huber 损失**（消融实验证实其优于 L2 损失，FID 从 0.622 降至 0.467）。

### 潜在空间运动控制（Motion Control in Latent Space）

为实现可控运动生成，MotionLCM 在潜在空间中引入运动 ControlNet（Fig. 4(b)），包含两个可训练模块：

- **轨迹编码器** $\Theta^b$（Transformer 架构）：编码控制关节的时空轨迹，输出全局特征 token。
- **运动 ControlNet** $\Theta^a$：以零初始化方式嵌入 MotionLCM，接收轨迹编码和噪声潜在向量，输出控制增强的潜在预测。

训练时冻结 MotionLCM 主干，联合优化 $\Theta^a$ 和 $\Theta^b$。潜在空间重建损失 $\mathcal{L}_{\mathrm{recon}}$ 确保控制后的潜在预测能还原为干净潜在向量（Eq. (8)）：

$$ \mathcal{L}_{\mathrm{recon}}(\Theta^a, \Theta^b) = \mathbb{E}\left[d\left(f_{\Theta^s}\left(\mathbf{z}_n, t_n, w, \mathbf{c}^*\right), \mathbf{z}_0\right)\right] $$

其中 $\mathbf{c}^*$ 为融合了控制信号的增强条件。

**关键创新**：潜在空间的 ControlNet 缺乏显式运动语义，仅靠潜在空间监督难以精确控制关节位置。MotionLCM 将控制后的潜在向量通过**冻结的 VAE 解码器** $D$ 解码回运动空间，施加显式控制损失 $\mathcal{L}_{\mathrm{control}}$（Eq. (9)）：

$$ \mathcal{L}_{\mathrm{control}}(\Theta^a, \Theta^b) = \mathbb{E}\left[\frac{\sum_i \sum_j m_{ij} \|R(\hat{\mathbf{x}}_0)_{ij} - R(\mathbf{x}_0)_{ij}\|_2^2}{\sum_i \sum_j m_{ij}}\right] $$

其中 $R(\cdot)$ 提取全局关节位置，$m_{ij}$ 为二进制关节掩码（被控制关节为 1，其余为 0），$\hat{\mathbf{x}}_0$ 为解码后的生成运动，$\mathbf{x}_0$ 为真实运动。该损失仅在受控关节上计算位置误差，避免对非受控关节施加不当约束。

总训练目标为（Eq. (10)）：

$$ \Theta^a, \Theta^b = \underset{\Theta^a, \Theta^b}{\arg\min}(\mathcal{L}_{\mathrm{recon}} + \lambda \mathcal{L}_{\mathrm{control}}) $$

其中 $\lambda$ 为控制损失权重，平衡生成质量与控制精度。消融实验表明 $\lambda = 1.0$ 取得最佳平衡：增大 $\lambda$ 可降低控制误差但损害生成质量（Table 4）。运动空间显式监督的引入使定位误差从 0.0344 降至 0.0147（Table 4），验证了该设计的必要性。

### 推理流程

蒸馏完成后，MotionLCM 支持 1-4 步直接采样：从噪声 $\mathbf{z}_T$ 出发，经单步一致性映射即可得到干净潜在向量，再通过 VAE 解码器恢复运动序列。1 步推理仅需约 30ms（NVIDIA Tesla V100，batch_size=1），相比 MLD 的 50 步 DDIM 推理（约 225ms）提速约 7.5 倍。

### 补充图表

![[assets/figures/papers/MotionLCM_Real-time_Controllable_Motion_Generation_via_Latent_Consistency_Model_aa7685020fdd/figures/003_Figure_3.jpg]]
*Figure 3: The training objective of consistency distillation is to learn a consistency function*



## 实验与关键发现

### 主实验结果

#### 文本到运动生成质量与速度

Table 1 报告了 HumanML3D 数据集上的文本到运动生成对比。MotionLCM 以**单步推理**（约30 ms）即达到与 MLD（50步 DDIM）相当甚至更优的生成质量：FID 为 0.467（MLD* 为 0.450），R-Precision Top-1 为 0.502（MLD* 为 0.504），差距均在置信区间内可忽略。而推理速度提升一个数量级——AITS 从 0.225 s 降至 0.030 s（**7.5 倍加速**）。当采用 2 步推理时，MotionLCM 的 FID 进一步降至 0.368，R-Precision Top-1 达到 0.505，超越所有对比方法。

![[assets/figures/papers/MotionLCM_Real-time_Controllable_Motion_Generation_via_Latent_Consistency_Model_aa7685020fdd/figures/005_Table_1.jpg]]
*Table 1: Comparison of text-conditional motion synthesis on HumanML3D [17] dataset. We compute suggested metrics following [17]. We repeat the evaluation 20 times for each metric and report the average with a 95% confidence interval. “ →” indicates that the closer to the real data, the better. Bold and underline indicate the best and the second best result. “∗” denotes the reproduced version of MLD [9]. The MotionLCM in one-step inference (30ms) surpasses all state-of-the-art models*

与扩散基线相比，**MDM**（Tevet et al., ICLR 2022）需约 24 s，**MotionDiffuse**（Zhang et al., arXiv 2022）需约 15 s，而 MotionLCM 以 30 ms 实现实时生成，从 Fig. 2 的 AITS-FID 散点图可见其显著逼近原点（理想点），同时脱离扩散模型所在的蓝色虚线框区域。

![[assets/figures/papers/MotionLCM_Real-time_Controllable_Motion_Generation_via_Latent_Consistency_Model_aa7685020fdd/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of the inference time costs on HumanML3D [17]. We compare the AITS and FID metrics with five SOTA methods. The closer the model is to the origin the better. Diffusion-based models are indicated by the blue dashed box. Our MotionLCM achieves real-time inference speed while ensuring high-quality motion generation*

#### 可控运动生成精度与效率

Table 2 展示了运动控制任务的结果。MotionLCM 在单步推理下，平均控制误差（Avg. err.）为 0.1127，相比 **OmniControl**（Xie et al., ICLR 2024）的 0.1673 **降低 32.7%**。同时，推理速度从 OmniControl 的约 81 s 降至约 30 ms（约 2700 倍加速）。在生成质量方面，MotionLCM 的 FID 为 0.455，优于 OmniControl 的 0.754，R-Precision Top-1 为 0.504 对比 0.479。

![[assets/figures/papers/MotionLCM_Real-time_Controllable_Motion_Generation_via_Latent_Consistency_Model_aa7685020fdd/figures/007_Table_2.jpg]]
*Table 2: Comparison of motion control on HumanML3D [17] dataset. Bold indicates the best result. Our MotionLCM outperforms OmniControl [73] and MLD [9] regarding generation quality, control performance, and inference speed*

值得注意的是，Table 2 中标记为“LC&MC”的 MotionLCM 变体同时使用了潜在空间控制（Latent Control）和运动空间显式控制损失（Motion Control），而仅使用潜在空间控制的变体（LC）在定位误差上表现较差，这直接验证了运动空间显式监督的必要性。

### 消融实验

#### 一致性蒸馏关键超参数

Table 3 系统消融了 MotionLCM 蒸馏阶段的四个关键设计：

![[assets/figures/papers/MotionLCM_Real-time_Controllable_Motion_Generation_via_Latent_Consistency_Model_aa7685020fdd/figures/008_Table_3.jpg]]
*Table 3: Ablation study on different training guidance scale ranges*

- **CFG 范围**：动态训练 CFG 范围 [5, 15] 优于固定 CFG=7.5，FID 从 0.568 降至 0.467。这表明在蒸馏过程中暴露于多样化的引导强度有助于模型泛化。
- **损失函数**：Huber 损失相比 L2 损失显著提升生成质量（FID 0.467 vs 0.622），说明对离群值更鲁棒的损失函数有利于一致性蒸馏的收敛。
- **EMA 率**：μ=0.999 取得最优平衡，过高或过低均导致 FID 上升。
- **跳步间隔 k**：k=20 在速度与质量间取得最优折中。

#### 控制损失权重 λ 的影响

Table 4 展示了控制损失权重 λ 的消融。随着 λ 从 0 增大，控制误差（Loc. err.）单调下降——从无显式控制损失时的 0.0344 降至 λ=1.0 时的 0.0147（降幅 57.3%），但过大的 λ（如 2.0）会导致 FID 从 0.455 劣化至 0.539，表明控制精度与生成质量间存在根本性权衡。λ=1.0 被选为默认设置，在此点 Loc. err. 为 0.0147，FID 为 0.455。

![[assets/figures/papers/MotionLCM_Real-time_Controllable_Motion_Generation_via_Latent_Consistency_Model_aa7685020fdd/figures/010_Table_4.jpg]]
*Table 4: Ablation study on different control loss weights λ. We present the results of (1, 2, 4)-step inference. We add the MotionLCM without ControlNet for comparison*

#### 控制比例 τ 与关节数 K

Table 5 消融了控制信号的两个结构参数：

![[assets/figures/papers/MotionLCM_Real-time_Controllable_Motion_Generation_via_Latent_Consistency_Model_aa7685020fdd/figures/011_Table_5.jpg]]
*Table 5: Ablation study on different control ratios τ and number of control joints K. We report the results of (1, 2, 4)-step inference. “ ∗” is the default training setting*

- **控制比例 τ**：固定 τ=0.25 优于动态比例（Traj. err. 0.1988 vs 0.2821），说明稳定的控制信号比例有助于训练收敛。
- **控制关节数 K**：将 K 从默认的 6 增至 22（全身关节），定位误差进一步从 0.0147 降至 0.0083（降幅 43.5%），表明更多关节的显式监督可有效提升控制精度，但需注意这可能增加计算开销。

#### 测试时 CFG 探索

Fig. 7 展示了测试时不同 CFG 尺度对生成质量的影响。与训练时固定 CFG 不同，测试时 CFG 在 7.5 附近取得 FID 最优，过高或过低均导致质量下降，这与扩散模型的标准行为一致。

![[assets/figures/papers/MotionLCM_Real-time_Controllable_Motion_Generation_via_Latent_Consistency_Model_aa7685020fdd/figures/013_Figure_7.jpg]]
*Figure 7: Comparison of testing CFGs*

### 失败模式与局限性

1. **VAE 压缩瓶颈**：MotionLCM 依赖 MLD 的 VAE 进行运动压缩，该编码器缺乏显式时序建模，可能在高频细节（如快速肢体运动、细微手势）的保留上存在信息损失。Table 4 中即使 λ=0 时 Loc. err. 已达 0.0344，说明潜在空间本身对空间位置的编码并非无损。

2. **控制-质量权衡刚性**：如 Table 4 所示，λ 的调节需要在控制精度与生成质量间手动折中，缺乏自适应机制。λ=2.0 时 FID 劣化幅度（+18.5%）远超控制精度的边际收益。

3. **数据集泛化未验证**：所有实验仅基于 HumanML3D 数据集，对 KIT、AMASS 等其他运动基准的泛化性尚待考察。

4. **两阶段训练复杂度**：先蒸馏后训练 ControlNet 的流程增加了训练时间和工程复杂度，且 ControlNet 训练时 MotionLCM 被冻结，限制了端到端联合优化的可能性。

### 重要图表结论汇总

- **Fig. 2**：MotionLCM 在 AITS-FID 平面上显著脱离扩散模型簇，逼近原点，证明实时性与高质量可兼得。
- **Table 1**：单步推理即超越 MLD 50 步质量，2 步推理全面领先所有对比方法。
- **Table 2**：在控制任务上同时实现精度提升（32.7%）和速度飞跃（2700 倍），验证了潜在空间控制与运动空间监督的协同有效性。
- **Table 4**：运动空间显式控制损失是降低定位误差的关键（降幅 57.3%），但需谨慎调节 λ 以平衡质量。

### 补充图表

![[assets/figures/papers/MotionLCM_Real-time_Controllable_Motion_Generation_via_Latent_Consistency_Model_aa7685020fdd/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison of the state-of-the-art methods in the text-to-motion task. With only one-step inference, MotionLCM achieves the fastest motion generation while producing high-quality movements that closely match the textual descriptions*

![[assets/figures/papers/MotionLCM_Real-time_Controllable_Motion_Generation_via_Latent_Consistency_Model_aa7685020fdd/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative comparison of the state-of-the-art methods in the motion control task. We provide the visualized motion results and real references from five prompts. Compared to OmniControl [73], MotionLCM with ControlNet not only generates the initial poses that accurately follow the given multi-joint trajectories (i.e., the green poses in real references) but also produces motions that closely align with the texts*



## 定位与知识库关联

### 1. 方法类型与谱系定位

MotionLCM 属于**潜在空间一致性运动生成模型**，其技术路线融合了三条关键谱系：

- **运动潜在扩散模型（Motion Latent Diffusion）**：直接继承自 **MLD**（Chen et al.），MotionLCM 将 MLD 作为蒸馏的教师模型，复用其预训练的 VAE 编码器-解码器架构和潜在空间。MLD 本身是潜在扩散模型（Latent Diffusion Model, LDM）在人体运动生成领域的适配，将运动序列压缩到低维潜在空间后进行扩散去噪。MotionLCM 的核心创新在于将这一扩散范式转化为一致性模型范式，而非重新设计潜在空间。

- **一致性模型（Consistency Models）**：MotionLCM 首次将一致性模型从图像域推广到运动生成域。其蒸馏框架直接遵循一致性蒸馏（Consistency Distillation）的理论基础——通过强制在线网络与 EMA 目标网络在 PF-ODE 轨迹上的输出一致性，学习从任意噪声点到干净潜在的单步映射。这一谱系的关键约束是**自一致性属性**（Eq. 1），即 $f(\mathbf{x}_t, t) = f(\mathbf{x}_{t'}, t'), \forall t, t' \in [\epsilon, T]$，确保了少步采样的理论可行性。

- **可控生成（Controllable Generation）**：MotionLCM 引入的运动 ControlNet 借鉴了图像域 ControlNet 的零初始化与冻结主干策略，但针对运动控制的特殊性做了关键适配：（1）使用 Transformer 轨迹编码器处理空间-时间控制信号；（2）在潜在空间控制之外，额外通过冻结的 VAE 解码器恢复运动空间，施加显式的全局关节位置控制损失 $L_{\text{control}}$。这一设计解决了潜在特征缺乏显式运动语义的根本瓶颈。

### 2. 与关键基线的关系

#### 2.1 与 MLD 的关系：继承与超越

MotionLCM 与 MLD 构成**蒸馏-学生**关系，而非简单的改进替代：

| 维度 | MLD | MotionLCM |
|------|-----|-----------|
| 推理范式 | 扩散去噪（50步 DDIM） | 一致性采样（1-4步直接映射） |
| 推理速度 | ~0.225s/序列 | ~0.030s/序列（1步） |
| 生成质量（FID↓） | 0.450 | 0.467（1步），0.368（2步） |
| 可控性 | 未原生支持 | 通过 ControlNet 实现 |

**核心继承**：VAE 架构、潜在空间、文本条件机制均直接复用 MLD，确保了对比的公平性。**核心超越**：通过潜在一致性蒸馏将推理步数从 50 步压缩至 1 步，速度提升约 7.5 倍，同时保持生成质量在 FID 上仅微弱下降（+0.017），在 R-Precision 上几乎持平（-0.002）。

#### 2.2 与 OmniControl 的关系：速度与精度的双重超越

OmniControl（Xie et al., ICLR 2024）是运动控制任务的主要对比基线，代表在运动空间进行操控的扩散方法。MotionLCM 对其实现了**数量级级别的速度超越**和**显著的控制精度提升**：

- **速度**：MotionLCM（1步）约 30ms，OmniControl 约 81s，速度提升约 2700 倍（原文报告 1929× 相比 MLD 的潜在控制）。这一差距源于 OmniControl 需要在扩散采样过程中反复进行运动空间操控和重新编码，而 MotionLCM 仅需单步潜在空间推理加一次解码。
- **控制精度**：平均控制误差从 0.1673 降至 0.1127，降低 32.7%。这得益于 MotionLCM 在潜在空间（LC）和运动空间（MC）的双重监督机制——消融实验表明，单独使用潜在空间控制时定位误差为 0.0344，加入运动空间显式控制损失后降至 0.0147（Table 4）。

#### 2.3 与其他扩散运动模型的关系

- **MDM**（Tevet et al., ICLR 2022）：作为运动扩散模型的代表性工作，MDM 在运动空间直接进行扩散，推理需约 24 秒。MotionLCM 在速度上超越其约 800 倍，且生成质量（FID 0.467 vs MDM 的 0.544）更优。这表明潜在空间压缩与一致性蒸馏的组合在效率和质量上均优于运动空间扩散。

- **MotionDiffuse**（Zhang et al., arXiv 2022）：在 HumanML3D 基准上，MotionLCM 的 1 步推理在 FID 和 R-Precision 上均优于 MotionDiffuse，同时速度优势显著。

### 3. 适用边界与条件约束

MotionLCM 的适用性受以下条件约束：

1. **数据集依赖性**：仅在 HumanML3D 数据集上验证，该数据集以文本-运动对为主，运动序列长度相对固定。对 KIT、AMASS 等其他运动数据集的泛化性尚未考察，属于待验证的开放问题。

2. **VAE 压缩瓶颈**：MotionLCM 继承 MLD 的 VAE，该压缩缺乏显式时序建模，可能限制高频运动细节的保留。在控制任务中，这体现为控制精度与生成质量之间的权衡——增加控制损失权重 $\lambda$ 可降低控制误差，但会损害 FID 和 R-Precision（Table 4）。

3. **控制任务的范围**：当前控制任务定义为给定初始 $\tau$ 帧的关节位置轨迹和文本描述，生成后续运动。控制比例 $\tau$ 和关节数 $K$ 需要预设（消融实验表明 $\tau=0.25$、$K=6$ 为默认最优设置），对更复杂的时空约束（如速度、加速度、中间帧约束）的扩展性未经验证。

4. **两阶段训练成本**：先进行潜在一致性蒸馏（LCD），再冻结 MotionLCM 训练 ControlNet，增加了训练流程的复杂度和总时间成本。这与端到端训练方法相比存在工程上的劣势。

### 4. 局限性与失败模式

根据论文报告的消融实验和设计选择，可识别以下局限：

1. **控制-质量权衡**：$\lambda$ 需要手动调节以平衡控制精度与生成质量。当 $\lambda$ 过大时，生成质量显著下降；过小时控制精度不足。目前缺乏自适应调整机制。

2. **CFG 敏感性**：训练时的 CFG 范围 $[w_{\min}, w_{\max}]$ 对最终性能有显著影响。固定 CFG=7.5 训练导致 FID 为 0.568，而动态范围 $[5, 15]$ 降至 0.467（Table 3）。测试时 CFG 的选择同样敏感（Fig. 7），需要额外调参。

3. **跳跃步间隔 $k$ 的经验性**：蒸馏过程中的 $k$ 值（默认 20）通过消融确定，其与最终生成质量的关系缺乏理论指导，可能在不同数据集或模型规模下需要重新搜索。

4. **损失函数选择的影响**：Huber 损失相比 L2 损失显著提升生成质量（FID 0.467 vs 0.622），表明一致性蒸馏对距离度量的选择敏感。这一现象的深层原因（Huber 损失对异常值的鲁棒性 vs 潜在空间中误差分布的特性）未充分分析。

### 5. 开放问题

1. **可解释的运动压缩架构**：当前 VAE 压缩缺乏运动学先验（如关节层级关系、运动学链），设计注入骨骼拓扑信息的压缩架构可能进一步提升控制精度和运动合理性。

2. **跨数据集泛化性**：在 KIT、AMASS 等不同规模、不同运动类型的数据集上的性能表现如何？特别是 KIT 的数据量较小，一致性蒸馏在小数据下的稳定性需要验证。

3. **高阶约束控制**：能否将方法扩展到速度、加速度、甚至物理约束（如足部滑动消除）的控制任务？这需要在运动空间施加更复杂的可微损失函数。

4. **$\lambda$ 的自适应调节**：控制损失权重能否通过元学习或基于运动复杂度的自适应机制自动调整，以减少人工调参负担？

5. **单阶段训练的可能性**：是否可以将一致性蒸馏与 ControlNet 训练合并为单阶段流程，降低训练复杂度？这需要解决蒸馏目标与控制目标之间的潜在冲突。

6. **更长时序的自回归一致性**：当前自回归生成范式中，使用前一段运动的最后 $\tau$ 帧作为控制信号，误差累积对长序列生成的影响如何？一致性模型的单步特性是否会放大或抑制这一误差传播？



## 原文 PDF

![[paperPDFs/ECCV_2024/MotionLCM_Real_time_Controllable_Motion_Generation_via_Latent_Consistency_Model.pdf]]
