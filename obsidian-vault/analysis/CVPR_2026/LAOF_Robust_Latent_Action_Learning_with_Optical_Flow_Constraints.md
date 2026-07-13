---
title: "LAOF: Robust Latent Action Learning with Optical Flow Constraints"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LAOF_Robust_Latent_Action_Learning_with_Optical_Flow_Constraints.pdf
project_link: null
code_link: "https://github.com/XizoB/LAOF"
aliases:
- LLA
- LAOF
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 引入智能体的帧间光流作为伪监督信号，通过一个专用的光流解码器将潜在动作直接映射到像素级运动，从而为潜在动作学习提供与物理动作高度相关的运动先验约束。
primary_logic: 光流天然过滤静态背景、强调运动物体，且现代光流模型（如RAFT）具备强跨场景泛化能力，可生成无需人工标注的高质量运动伪标签。将光流作为额外的重建目标，可以有效地将潜在动作锚定在物理有意义的运动空间中，大幅提升训练的稳定性和表征的鲁棒性。
claims:
- 在无动作监督的极端设置下，LAOF在1%动作比例下匹配或超越有监督的LAOM-Action (PROCGEN实验，Fig.4)
- 光流约束将无监督方法的LIBERO成功率提升4.2%，有监督方法提升11.5%；在PROCGEN上归一化回合回报分别提升16%和22%
- 光流约束在高达10%的动作标签比例下仍能为基线方法提供持续的性能增益 (Fig.4)
- 相比于将光流约束集成到FDM中，直接附加专用光流解码器的架构变体（LAOF）取得了最佳性能 (Table 3)
---

# LAOF: Robust Latent Action Learning with Optical Flow Constraints

> [!tip] 核心洞察
> 光流天然过滤静态背景、强调运动物体，且现代光流模型（如RAFT）具备强跨场景泛化能力，可生成无需人工标注的高质量运动伪标签。将光流作为额外的重建目标，可以有效地将潜在动作锚定在物理有意义的运动空间中，大幅提升训练的稳定性和表征的鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | LAOF: 基于光流约束的鲁棒潜在动作学习 |
| 英文题名 | LAOF: Robust Latent Action Learning with Optical Flow Constraints |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.16407) · [Code](https://github.com/XizoB/LAOF) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | LAOF (and LAOF-Action) |
| Dataset | LIBERO, PROCGEN |

> [!tip] 效果简介
> - LIBERO (SPATIAL) 上，Success Rate (%) 82.5 (LAOF), 88.2 (LAOF-Action) vs 80.4 (LAPO) (+2.1 / +7.8)。
> - LIBERO (Average over 4 task suites) 上，Success Rate (%) improvement +4.2 (LAOF), +11.5 (LAOF-Action) vs LAPO (+4.2 / +11.5)。
> - PROCGEN (BIGFISH) 上，Normalized Return 0.76 (LAOF), 0.80 (LAOF-Action) vs 0.72 (LAPO) (+0.04 / +0.08)。

## 概要

**问题瓶颈**：现有基于视频的潜在动作学习方法（如 **LAPO**，Schmidt & Jiang, ICLR 2024）在预训练时仅依赖下一帧重建损失，缺乏显式的运动约束。这导致潜在动作容易与视觉外观纠缠，无法可靠地捕获物理动作——尤其在存在动态干扰物或动作标签极度稀缺时，模型容易过拟合到虚假相关性，训练不稳定。

**核心洞察与因果机制**：智能体的帧间光流天然过滤静态背景、强调运动物体，且现代光流基础模型（如 **RAFT**）具备强跨场景泛化能力，可生成无需人工标注的高质量运动伪标签。将光流作为额外的重建目标，可以有效地将潜在动作锚定在物理有意义的运动空间中。

**方法定位**：**LAOF** 在 LAPO 的逆动力学模型（IDM）与前向动力学模型（FDM）架构之上，引入一个**专用的光流解码器**，将潜在动作直接映射到像素级运动特征。预训练损失由下一状态重建损失与光流约束损失联合构成（式1），为潜在动作学习提供与物理动作高度相关的运动先验。在有稀疏动作标签的场景下，**LAOF-Action** 进一步引入动作解码器，以标签比例自适应的权重 $\lambda = M/(N+M)$ 平衡动作监督与光流约束（式2）。

**主要结果**：
- 在 **LIBERO** 基准上，无监督的 LAOF 相较 LAPO 平均成功率提升 **+4.2%**，有监督的 LAOF-Action 提升 **+11.5%**（Table 1）。
- 在 **PROCGEN** 基准上，LAOF 与 LAOF-Action 的归一化回合回报分别提升 **+16%** 和 **+22%**（Table 2）。
- 在极端 **1% 动作标签比例**下，无任何动作监督的 LAOF 匹配甚至超越了有监督的 **LAOM-Action**（Nikulin et al., ICML 2025）（Fig. 4）。
- 光流约束在高达 **10% 动作标签比例**下仍为基线方法提供持续增益，且专用光流解码器的架构变体（LAOF）在所有消融变体中取得最佳性能（Table 3）。

**局限与展望**：方法目前基于第三人称固定视角视频，尚未验证在眼在手（eye-in-hand）及第一人称场景下的效果；物体中心光流提取依赖 **LangSAM** 的语义分割与文本提示，对复杂动态场景的泛化性有限。未来方向包括扩展到第一人称视角、自适应损失权重学习，以及探索光流约束在更大规模具身基础模型预训练中的应用。

### 问题背景：从视频中学习可复用的潜在动作

具身智能体要从海量无标签视频数据中学习可复用的技能，核心挑战之一是如何从原始像素观测中提取紧凑且物理有意义的动作表征。潜在动作学习（latent action learning）为此提供了一条有前景的路径：通过逆动力学模型（IDM）从连续帧中推断潜在动作，再以前向动力学模型（FDM）预测下一帧来提供自监督信号。这类方法无需人工标注的动作标签，理论上可以扩展到大规模视频数据。

然而，现有方法面临一个关键瓶颈：**仅依赖下一帧重建损失来训练潜在动作表征，缺乏对物理运动的显式约束**。这导致潜在动作容易与视觉外观（如光照、纹理、背景）纠缠在一起，而非真正捕获智能体的物理动作。尤其在存在动态干扰物或动作标签极度稀缺时，模型容易过拟合到虚假相关性，训练过程不稳定。

### 现有方法的缺口

近期工作 **LAPO**（Schmidt and Jiang, ICLR 2024）通过联合训练IDM和FDM，在无动作标签条件下学习潜在动作，但其预训练目标仅为下一状态重建损失 $\mathcal{L}_{\text{reconstruction}}$。这种纯外观驱动的监督信号无法区分“什么在动”和“为什么动”——模型可能将背景变化或干扰物运动误编码为潜在动作，导致表征的物理可解释性和下游任务迁移能力受限。

**CoMo**（Yang et al., arXiv 2025）尝试通过帧间差分输入来缓解捷径学习问题，但帧间差分本质上只是像素级的亮度变化，缺乏对运动方向、幅度和物体归属的结构化建模能力。实验证据表明，在CoMo基础上加入光流约束的提升幅度（PROCGEN平均归一化回报+0.12）小于直接对LAPO加入光流约束（+0.16），说明帧间差分并不能替代真正的运动先验。

在有监督方向，**LAOM-Action**（Nikulin et al., ICML 2025）引入动作解码器将潜在动作映射到物理动作，但在极端低标签比例（如1%）下，其训练稳定性不足，且对损失权重 $\lambda$ 高度敏感。

### 核心洞察：光流作为运动先验

本文的核心洞察在于：**帧间光流天然过滤静态背景、强调运动物体，且现代光流基础模型（如RAFT）具备强跨场景泛化能力，可生成无需人工标注的高质量运动伪标签**。将光流作为额外的重建目标，可以有效地将潜在动作锚定在物理有意义的运动空间中。

具体而言，光流提供的是像素级的稠密运动场，直接编码了“哪个物体在朝哪个方向以多大速度运动”。这种信号与智能体的物理动作高度相关——典型相关分析（CCA）显示，光流特征与物理动作之间的相关性显著高于帧间差分特征或随机噪声（Table 4）。因此，光流可以作为连接像素观测与物理动作之间的天然桥梁。

### 本文动机与贡献

基于上述洞察，本文提出 **LAOF（Latent Action learning with Optical Flow constraints）**，核心思路是：**引入一个专用的光流解码器，将潜在动作直接映射到像素级光流，从而为潜在动作学习提供与物理动作高度相关的运动先验约束**。该方法在无动作标签（LAOF）和稀疏动作标签（LAOF-Action）两种设置下均适用，通过将光流约束与重建损失联合优化，大幅提升训练的稳定性和表征的鲁棒性。

关键证据表明这一思路的有效性：在极端1%动作标签比例下，无任何动作监督的LAOF能够匹配甚至超越有监督的LAOM-Action（PROCGEN实验，Fig.4）；光流约束在高达10%的动作标签比例下仍能为基线方法提供持续增益。

## 核心方法与创新机理

LAOF 的核心创新在于引入**光流作为潜在动作学习的显式运动先验**，通过一个专用的光流解码器将潜在动作直接映射到像素级运动，从而将潜在动作锚定在物理有意义的运动空间中。这一设计从根本上改变了现有潜在动作学习方法的训练范式。

### 问题瓶颈：潜在动作与视觉外观的纠缠

现有潜在动作学习方法（如 **LAPO**，Schmidt and Jiang, ICLR 2024）在预训练阶段仅依赖下一帧重建损失 $\mathcal{L}_{\text{reconstruction}}$ 来约束潜在动作的学习。这种纯外观驱动的监督信号存在一个关键缺陷：潜在动作容易与场景的视觉外观（如背景纹理、光照变化、静态物体）产生虚假相关性，而非真正捕获智能体的物理动作。当场景中存在动态干扰物或动作标签极度稀缺时，模型容易过拟合到这些虚假相关性，导致训练不稳定、表征泛化性差。

**CoMo**（Yang et al., arXiv 2025）尝试通过帧间差分输入来缓解捷径学习问题，但差分信号本身仍混杂了外观变化与真实运动，无法从根本上解耦动作与外观。

### 因果调节变量：光流作为运动伪监督

LAOF 的关键洞察是：**光流天然过滤静态背景、强调运动物体**，且现代光流基础模型（如 RAFT）具备强跨场景泛化能力，可生成无需人工标注的高质量运动伪标签。将光流作为额外的重建目标，可以为潜在动作学习提供与物理动作高度相关的运动先验约束。

具体而言，LAOF 在 **LAPO** 基础上引入了三个关键的 changed slots：

| 变更模块 | 基线（LAPO） | LAOF 方案 | 作用机制 |
|---------|------------|----------|---------|
| **光流解码器** | 无 | 专用空间 Transformer 解码器，从潜在动作 $z_t$ 直接预测光流特征 | 建立潜在动作到像素级运动的直接映射通道 |
| **预训练损失函数** | 仅 $\mathcal{L}_{\text{reconstruction}}$ | $\mathcal{L}_{\text{pretrain}} = \mathcal{L}_{\text{reconstruction}} + \mathcal{L}_{\text{flow}}$ | 在重建约束之上叠加运动约束，双重监督 |
| **稀疏动作监督下的损失权重** | 仅动作监督或无监督 | $\lambda = M/(N+M)$ 平衡动作监督与光流约束 | 根据标签比例自适应分配监督信号强度 |

其中，$\mathcal{L}_{\text{flow}}$ 约束潜在动作解码出的光流与预训练光流模型（RAFT）生成的伪标签保持一致。对于包含动态干扰物的场景，LAOF 进一步利用 LangSAM 提取物体中心语义掩码，将全局光流过滤为仅包含智能体的运动信号，从而避免干扰物运动的污染。

### 架构设计的关键决策：专用光流解码器

消融实验（Table 3）验证了一个重要的架构选择：**直接附加专用光流解码器（LAOF）优于将光流约束集成到前向动力学模型（FDM）中**。具体变体对比：

- **LAOF-FlowFDM**（将光流预测集成到 FDM 中）：LIBERO 平均提升 +3.3%
- **LAOF-Only(zt)**（仅保留光流解码器，去除 FDM）：平均提升 +3.6%
- **LAOF**（完整架构，FDM + 专用光流解码器）：平均提升 +4.2%

这表明专用光流解码器提供了最强的物理运动监督，而 FDM 提供的结构上下文信息对完整性能仍有补充作用。值得注意的是，即使去除 FDM（LAOF-Only(zt)），仅靠光流约束的性能仍优于将光流集成到 FDM 中的方案，进一步验证了独立运动建模通道的价值。

### 训练稳定性的质变

光流约束带来的另一个关键创新是**训练稳定性的显著提升**。在 $\lambda$ 系数消融实验（Figure 9）中，**LAOF-Action** 在 $\lambda \in [0.001, 0.1]$ 范围内保持高度稳定，方差极小；而 **LAOM-Action**（Nikulin et al., ICML 2025）对 $\lambda$ 敏感且表现剧烈波动。这表明光流约束为潜在动作学习提供了稳定的优化景观，即使在稀疏动作监督下也能避免过拟合到噪声标签。

LAOF 遵循三阶段训练流水线：**预训练（pre-training）→ 蒸馏（distillation）→ 微调（fine-tuning）**，各阶段对应不同的数据集与优化目标。核心创新集中在预训练阶段，通过引入帧间光流作为伪监督信号，为潜在动作学习提供物理运动约束。

### 模块架构与数据流

如图 1 所示，LAOF 的预训练架构由以下模块串联构成：

1. **视觉编码器（DINOv2）**：冻结的 ViT-B/14 将连续观测对 $(o_t, o_{t+1})$ 及对应的 RGB 格式光流 $f_{\text{rgb},t}$ 分别映射到特征空间，得到状态特征 $s_t, s_{t+1}$ 和光流特征 $f_t$。

2. **逆动力学模型（IDM）**：从连续状态特征对 $(s_t, s_{t+1})$ 推断潜在动作 $z_t$。在 LIBERO 上实现为时空 Transformer，在 PROCGEN 上实现为 CNN 编码器。

3. **前向动力学模型（FDM）**：以当前状态 $s_t$ 和潜在动作 $z_t$ 为输入，预测下一状态特征 $\hat{s}_{t+1}$，接受下一状态重建损失 $\mathcal{L}_{\text{reconstruction}}$ 的监督。FDM 实现为空间 Transformer 或 U-Net。

4. **光流解码器（Flow Decoder）**：从潜在动作 $z_t$ 直接解码光流特征 $\hat{f}_t$，与预计算的光流伪标签 $f_t$ 对齐，构成光流约束损失 $\mathcal{L}_{\text{flow}}$。该解码器同样为空间 Transformer，与 FDM 并行但独立。

5. **动作解码器（Action Decoder）**：仅 LAOF-Action 变体使用，为轻量 MLP，将潜在动作映射到物理动作空间，在稀疏动作标签上接受监督。

预训练总损失为：

$$\mathcal{L}_{\text{pretrain}} = \mathcal{L}_{\text{reconstruction}} + \mathcal{L}_{\text{flow}}$$

对于 LAOF-Action，引入系数 $\lambda = M/(N+M)$（$M$ 为有标签样本数，$N$ 为无标签样本数）平衡光流约束与动作监督：

$$\mathcal{L}_{\text{pretrain}} = \mathcal{L}_{\text{reconstruction}} + (1-\lambda) \cdot \mathcal{L}_{\text{flow}} + \lambda \cdot \mathcal{L}_{\text{action}}$$

### 光流伪标签生成

光流伪标签的生成独立于主训练流程，由两个模块协同完成：

- **RAFT**：预训练光流基础模型，提供帧间的全局密集运动估计。
- **LangSAM**：当场景中存在动态干扰物时，利用文本提示生成物体中心语义掩码，将全局光流过滤为仅保留智能体运动区域的物体中心光流（object-centric optical flow）。在静态场景下，智能体的光流可直接从全局光流中提取。

光流幅度通过以下公式归一化，以适应不同尺度的运动：

$$m_{\text{norm}} = \min\left(1.0, \frac{m}{\sigma \cdot \sqrt{H^2 + W^2}}\right)$$

其中 $\sigma$ 为敏感度因子，$H$ 和 $W$ 为图像尺寸。

### 设计动机与因果机制

现有方法（如 **LAPO**，Schmidt and Jiang, ICLR 2024）仅依赖下一帧重建损失训练 IDM 和 FDM，缺乏显式运动约束，导致潜在动作容易与视觉外观纠缠，在动态干扰物或动作标签极度稀缺时训练不稳定。LAOF 的核心洞察在于：光流天然过滤静态背景、强调运动物体，且现代光流模型（如 RAFT）具备强跨场景泛化能力。将光流作为额外的重建目标，通过专用光流解码器将潜在动作直接映射到像素级运动，可有效将潜在动作锚定在物理有意义的运动空间中。

消融实验（Table 3）验证了这一设计：直接附加专用光流解码器的 LAOF 取得了最佳性能，优于将光流约束集成到 FDM 中（LAOF-FlowFDM）或对光流进行自编码（LAOF-AE）的变体。去除 FDM 仅保留光流解码器（LAOF-Only($z_t$)）仍优于 LAOF-FlowFDM，但不及完整 LAOF，表明 FDM 提供的结构上下文对潜在动作学习具有辅助作用。

![[assets/figures/papers/paper_list_l890_https_arxiv_org_abs_2511_16407/figures/001_Figure_1.jpg]]
*Figure 1: Overview of LAOF framework: Consecutive observations*

### 三阶段训练流水线

LAOF的训练过程遵循**预训练→蒸馏→微调**的三阶段流水线，各阶段对应不同的数据配置。核心创新集中在预训练阶段——通过引入光流伪标签为潜在动作学习提供物理运动约束。

### 预训练损失函数

LAOF的预训练目标将传统下一帧重建损失与光流约束损失联合优化：

$$
\mathcal{L}_{\text{pretrain}} = \mathcal{L}_{\text{reconstruction}} + \mathcal{L}_{\text{flow}} \tag{1}
$$

其中 $\mathcal{L}_{\text{reconstruction}}$ 为前向动力学模型（FDM）预测的下一状态与真实下一状态之间的重建损失，$\mathcal{L}_{\text{flow}}$ 为光流解码器输出的光流特征与RAFT生成的伪标签之间的约束损失。

### 稀疏动作监督下的损失权重

当引入少量动作标签时，LAOF-Action通过自适应权重 $\lambda$ 平衡动作监督与光流约束：

$$
\mathcal{L}_{\text{pretrain}} = \mathcal{L}_{\text{reconstruction}} + (1-\lambda) \cdot \mathcal{L}_{\text{flow}} + \lambda \cdot \mathcal{L}_{\text{action}} \tag{2}
$$

$\lambda = M/(N+M)$，其中 $M$ 为有动作标签的样本数，$N$ 为无标签样本数。该设计使 $\lambda$ 直接对应动作标签在整体训练数据中的比例——当标签极度稀疏（如1%动作比例）时，光流约束主导训练；当标签充足时，动作监督自动获得更高权重。

### 光流幅度归一化

为适应不同场景下的运动尺度差异，LAOF对光流幅度进行归一化处理：

$$
m_{\text{norm}} = \min\left(1.0, \frac{m}{\sigma \cdot \sqrt{H^2 + W^2}}\right) \tag{3}
$$

其中 $m$ 为光流向量幅度，$H$ 和 $W$ 为图像尺寸，$\sigma$ 为敏感度因子。该归一化将光流幅度压缩至 $[0, 1]$ 区间，以图像对角线长度作为归一化基准，确保不同分辨率下的运动信号具有可比性。

### 关键模块架构

**逆动力学模型（IDM）**：在LIBERO上实现为时空Transformer，在PROCGEN上实现为CNN编码器，从连续状态对 $(s_t, s_{t+1})$ 推断潜在动作 $z_t$。

**前向动力学模型（FDM）**：实现为空间Transformer或U-Net，基于当前状态 $s_t$ 和潜在动作 $z_t$ 预测下一状态 $\hat{s}_{t+1}$，提供 $\mathcal{L}_{\text{reconstruction}}$ 的结构上下文约束。

**光流解码器**：专用空间Transformer解码器 $d_{\text{flow}}: Z \to \mathcal{F}_{\text{rgb}}$，将潜在动作直接映射到RGB格式的光流特征空间，为潜在动作学习提供与物理运动高度相关的显式监督信号。消融实验（Table 3）表明，这种专用解码器架构优于将光流约束集成到FDM中的方案。

**动作解码器（仅LAOF-Action）**：轻量MLP，将潜在动作映射到物理动作空间，在有标签样本上计算 $\mathcal{L}_{\text{action}}$ 的均方误差。

**光流伪标签生成**：利用预训练RAFT模型生成帧间稠密光流，在存在动态干扰物的场景下，结合LangSAM的语义分割掩码提取物体中心光流，过滤背景运动噪声。

## 实验与关键发现

### 核心瓶颈与因果机制

现有潜在动作学习方法（如 **LAPO**，Schmidt and Jiang, ICLR 2024）在预训练阶段仅依赖下一帧重建损失 $\mathcal{L}_{\text{reconstruction}}$，缺乏对智能体物理运动的显式约束。这导致两个关键失效模式：（1）**外观-动作纠缠**：潜在动作 $z_t$ 容易与视觉外观特征产生虚假相关性，而非捕获真实的物理动作；（2）**训练不稳定**：在动作标签极度稀缺（如1%标注比例）时，模型缺乏足够的监督信号来学习有意义的动作表征，容易过拟合到数据中的虚假模式。

LAOF 的核心因果机制在于引入**光流伪监督信号**作为运动先验，通过一个专用的光流解码器 $d_{\text{flow}}: Z \to \mathcal{F}_{\text{rgb}}$ 将潜在动作直接映射到像素级运动。光流天然过滤静态背景、强调运动物体，且现代光流基础模型（如 **RAFT**，Teed and Deng, ECCV 2020）具备强跨场景泛化能力，可生成无需人工标注的高质量运动伪标签。这一约束将潜在动作锚定在物理有意义的运动空间中，有效解耦了外观信息与运动信息。

### 主实验结果

#### LIBERO 模仿学习基准

在 LIBERO 四个任务套件（SPATIAL、OBJECT、GOAL、LONG）上的连续潜在动作评估中，LAOF 在两个设置下均取得一致提升（Table 1）：

![[assets/figures/papers/paper_list_l890_https_arxiv_org_abs_2511_16407/figures/003_Table_1.jpg]]
*Table 1: Effect of continuous latent actions on downstream imitation learning performance on LIBERO. MSE denotes the mean squared error between the predicted and ground-truth actions, Succ. denotes the average task success rate over 1000 trials, w/ OF denotes that the method uses optical flow constraints, and Avg. Impr. indicates the average improvement over LAPO. LAOM-Action and LAOF-Action are action-supervised methods, evaluated under a 1% action ratio*

| 方法 | SPATIAL Succ.(%) | OBJECT Succ.(%) | GOAL Succ.(%) | LONG Succ.(%) | 平均提升 |
|------|-----------------|-----------------|---------------|---------------|---------|
| LAPO | 80.4 | 94.3 | 86.4 | 56.2 | — |
| LAOF (无监督) | 82.5 | 95.5 | 87.5 | 60.2 | **+4.2%** |
| LAOF-Action (1%标签) | 88.2 | 95.9 | 88.6 | 63.7 | **+11.5%** |

关键发现：
- 无监督 LAOF 在所有任务上均超越 LAPO 基线，平均成功率提升 4.2%。
- 在 1% 动作标签比例下，LAOF-Action 将提升幅度扩大至 11.5%，验证了光流约束与稀疏动作监督的互补性。

#### PROCGEN 强化学习基准

在 PROCGEN 四个任务（BIGFISH、STARPILOT、JUMBLE、FRUITBOT）上的离散潜在动作评估中，LAOF 同样展现出显著增益（Table 2）：

| 方法 | BIGFISH Return | STARPILOT Return | JUMBLE Return | FRUITBOT Return | 平均提升 |
|------|---------------|-----------------|---------------|-----------------|---------|
| LAPO | 0.72 | 0.58 | 0.65 | 0.70 | — |
| LAOF (无监督) | 0.76 | 0.64 | 0.71 | 0.74 | **+0.16** |
| LAOF-Action (1%标签) | 0.80 | 0.67 | 0.74 | 0.76 | **+0.22** |

归一化回合回报平均提升 16%（无监督）和 22%（有监督），表明光流约束在离散动作空间中同样有效。

#### 极端低标签比例下的突破

在 1% 动作标签比例的极端设置下，**无任何动作监督的 LAOF 匹配甚至超越了有监督的 LAOM-Action**（Nikulin et al., ICML 2025）（Figure 4）。这一结果直接证明了光流伪标签可以作为动作标签的有效替代，在标签极度稀缺时提供可靠的物理运动先验。

### 光流约束的增益边界

Figure 4 进一步揭示了光流约束在不同动作标签比例下的增益模式：
- 在 0%~10% 的动作标签范围内，光流约束为基线方法提供持续且稳定的性能增益。
- 随着标签比例增加，增益幅度逐渐收敛，但在 10% 比例下仍保持正向贡献。
- 这一趋势表明光流约束与动作监督之间存在互补而非替代关系：光流提供运动先验，动作标签提供任务特定的语义对齐。

### 训练稳定性分析

Figure 5 对比了不同方法在预训练过程中的稳定性：
- **LAOM-Action** 在 1% 标签比例下表现出明显的训练波动，对超参数 $\lambda$ 敏感。
- **LAOF-Action** 在不同 $\lambda$ 值（0.001~0.1）下保持高度稳定，方差显著低于 LAOM-Action（Figure 9）。
- 无监督 LAOF 的损失曲线平滑收敛，未出现过拟合迹象。

![[assets/figures/papers/paper_list_l890_https_arxiv_org_abs_2511_16407/figures/007_Figure_5.jpg]]
*Figure 5: Comparison of stability and overfitting among different methods, where solid lines represent unsupervised methods and dashed lines represent action-supervised methods. LAOM-Action and LAOF-Action are evaluated at a 1% action ratio*

![[assets/figures/papers/paper_list_l890_https_arxiv_org_abs_2511_16407/figures/014_Figure_9.jpg]]
*Figure 9: Effect of the coefficient ?? on training stability. A shared legend for all four subfigures is shown in subfigure (a)*

这一稳定性优势源于光流约束为潜在动作学习提供了密集的像素级监督信号，有效缓解了稀疏动作标签带来的梯度稀疏性问题。

### 消融实验

#### 架构变体比较（Table 3）

![[assets/figures/papers/paper_list_l890_https_arxiv_org_abs_2511_16407/figures/008_Table_3.jpg]]
*Table 3: Average performance improvement of LAOF variants over LAPO across all LIBERO and PROCGEN tasks*

| 变体 | LIBERO 平均提升 | PROCGEN 平均提升 | 说明 |
|------|---------------|-----------------|------|
| LAOF-FlowFDM | +3.3% | +0.12 | 将光流约束集成到 FDM 中 |
| LAOF-Only($z_t$) | +3.6% | +0.14 | 仅保留光流解码器，去除 FDM |
| LAOF-Only($z_t, s_t$) | +3.0% | +0.10 | 光流解码器同时接收 $z_t$ 和 $s_t$ |
| LAOF-AE | +3.8% | +0.15 | 对光流进行自编码 |
| **LAOF** | **+4.2%** | **+0.16** | 专用光流解码器（完整方法） |

关键结论：
1. **专用光流解码器优于集成方案**：将光流约束集成到 FDM 中（LAOF-FlowFDM）性能次优，表明物理运动预测需要独立的解码路径。
2. **FDM 提供有益的结构上下文**：去除 FDM 后（LAOF-Only($z_t$)）性能下降但仍有竞争力，说明光流约束本身已能学到有效的动作表征，而 FDM 提供的状态预测进一步增强了表征质量。
3. **自编码光流（LAOF-AE）具有竞争力但不及直接预测**：对光流进行自编码的性能接近完整 LAOF，但直接映射潜在动作到光流的方式更直接地建立了动作-运动的因果关联。

#### 光流与帧间差分的对比

将光流约束应用于 **CoMo**（Yang et al., arXiv 2025）——一种使用帧间差分输入以避免捷径学习的方法——其提升幅度（LIBERO +4.0%，PROCGEN +0.12）略低于直接应用于 LAPO 的效果。这表明帧间差分虽然能过滤部分静态背景，但无法替代真实光流提供的稠密运动向量场信息（包括运动方向和幅度）。

### 光流与物理动作的相关性验证

Table 4 通过典型相关分析（CCA）量化了光流表征与物理动作的关联强度：
- 将 DINOv2 提取的光流特征（768维）经 PCA 降维至 50 维后，与物理动作计算 CCA。
- 光流表征与物理动作的相关性显著高于帧间差分特征（$\Delta$DINOv2）和随机噪声。
- 这一结果从统计层面验证了光流作为物理动作代理信号的有效性。

![[assets/figures/papers/paper_list_l890_https_arxiv_org_abs_2511_16407/figures/012_Table_4.jpg]]
*Table 4: Canonical Correlation Analysis between optical flow representations and physical actions across different models. Optical flow features were first extracted using DINOv2 (768-dim) and then reduced to 50 dimensions via Principal Component Analysis (PCA) before computing CCA. Each benchmark reports results over 200K randomly drawn samples. Here, ΔDINOv2 denotes features obtained by differencing consecutive observations extracted using DINOv2. “Noise” denotes Gaussian noise, and “Action” denotes physical actions*

### 光流模型的鲁棒性

Table 5 展示了不同光流模型在 LIBERO-Plus（含光照和背景干扰）及真实世界场景下的表现：
- **RAFT**（LAOF-R）和 **SEA-RAFT**（LAOF-S）在光照变化和背景干扰下均保持稳定的性能增益。
- 帧间差分特征（LAOF-$\Delta$）在干扰条件下性能下降明显，进一步验证了真实光流对域偏移的鲁棒性。

### 失败模式与局限性

1. **视角限制**：当前方法基于第三人称固定视角视频，尚未验证在眼在手（eye-in-hand）腕部相机及第一人称视频上的效果。
2. **物体中心光流的语义依赖**：在存在动态干扰物的场景中，物体中心光流的提取依赖 **LangSAM**（Guerrero, 2023）的语义分割，需要文本提示且对复杂动态场景的泛化性有限。
3. **高标签比例下的边际效益递减**：在极端高动作标签比例（>10%）下，光流约束的增益趋于饱和，其边际效益需进一步评估。
4. **光流伪标签质量依赖**：光流伪标签的质量受预训练光流模型（RAFT）性能影响，在域偏移较大时可能引入噪声伪影。

### 关键图表索引

- **Table 1**：LIBERO 连续潜在动作模仿学习性能对比
- **Table 2**：PROCGEN 离散潜在动作强化学习性能对比
- **Figure 4**：不同动作标签比例下离散潜在动作质量评估
- **Figure 5**：预训练过程中的稳定性与过拟合对比
- **Table 3**：LAOF 架构变体消融实验
- **Table 4**：光流表征与物理动作的典型相关分析
- **Table 5**：不同光流模型的鲁棒性实验
- **Figure 9**：系数 $\lambda$ 对训练稳定性的影响

## 定位与知识库关联

### 1. 与基线方法的关系

LAOF 的核心贡献是在潜在动作学习框架中引入光流约束，其直接对标的方法谱系如下：

**LAPO** (Schmidt and Jiang, ICLR 2024) 是 LAOF 的直接基线。LAPO 联合训练逆动力学模型（IDM）与前向动力学模型（FDM），仅依赖下一帧重建损失 $\mathcal{L}_{\text{reconstruction}}$ 进行预训练。其核心瓶颈在于：缺乏显式运动约束，导致潜在动作容易与视觉外观纠缠，无法可靠捕获物理动作——尤其在存在动态干扰物或动作标签极度稀缺时，模型容易过拟合到虚假相关性，训练不稳定。LAOF 在此框架上新增专用光流解码器，将损失函数扩展为 $\mathcal{L}_{\text{pretrain}} = \mathcal{L}_{\text{reconstruction}} + \mathcal{L}_{\text{flow}}$，从而将潜在动作锚定在物理有意义的运动空间中。

**CoMo** (Yang et al., arXiv 2025) 在 LAPO 基础上使用帧间差分输入以避免捷径学习（shortcut learning），但本质上仍缺乏对运动本身的直接监督。实验表明，光流约束对 CoMo 的提升（LIBERO 平均 +4.0%，PROCGEN 平均 +0.12）不如对 LAPO 直接（+4.2% / +0.16），说明帧间差分并不能替代真实光流运动先验（Table 1, 2）。这从反面验证了光流作为显式运动约束的不可替代性。

**LAOM-Action** (Nikulin et al., ICML 2025) 引入动作解码器将潜在动作映射到物理动作，是一种有监督方法。LAOF-Action 在此基础上将动作监督与光流约束融合，损失函数为 $\mathcal{L}_{\text{pretrain}} = \mathcal{L}_{\text{reconstruction}} + (1-\lambda) \cdot \mathcal{L}_{\text{flow}} + \lambda \cdot \mathcal{L}_{\text{action}}$，其中 $\lambda = M/(N+M)$ 对应动作标签在训练集中的比例。在 1% 动作比例的极端设置下，LAOF（无动作监督）即可匹配甚至超越 LAOM-Action 的性能（PROCGEN 实验，Fig. 4），而 LAOF-Action 则进一步拉开了差距。

### 2. 方法适用边界

**适用场景：**

- **无动作标签或标签极度稀缺**（<1% 动作比例）的模仿学习与强化学习预训练。光流伪标签由预训练光流模型（RAFT）自动生成，无需人工标注。
- **静态背景或可语义分割的动态场景**。对于静态干扰物场景，全局光流可直接使用；对于动态干扰物场景，可借助 LangSAM 提取物体中心光流（Figure 2）。
- **第三人称固定视角视频**，这是当前实验覆盖的设定。

**不适用或需谨慎的场景：**

- **眼在手（eye-in-hand）腕部相机及第一人称视频**：论文明确将此列为未验证的局限，因为第一人称视角下智能体运动与环境运动的解耦更为复杂。
- **域偏移较大的环境**：光流伪标签的质量受预训练光流模型（RAFT）性能影响，在域偏移较大时可能引入噪声（Table 5 展示了不同光流模型对鲁棒性的影响，但极端域偏移仍需进一步评估）。
- **极端高动作标签比例（>10%）**：光流约束的边际效益可能趋于饱和，其增益边界需进一步量化。

### 3. 局限与开放问题

**论文明确指出的局限：**

1. **视角限制**：方法目前基于第三人称固定视角视频，尚未在眼在手相机及第一人称视频上验证。
2. **语义分割依赖**：物体中心光流的提取依赖 LangSAM 的语义分割，对复杂动态场景的泛化性可能有限，且需要文本提示。
3. **光流模型依赖**：光流伪标签的质量受预训练光流模型性能影响，域偏移时可能引入噪声。
4. **边际效益饱和**：在 >10% 动作标签比例下，光流约束的增益可能趋于饱和。

**开放问题：**

1. **如何将 LAOF 扩展到第一人称和眼在手场景**，同时解耦智能体运动与环境运动？这需要处理相机自身运动带来的全局光流偏移。
2. **能否将 $\lambda$ 设置为可学习参数**，以自动适应不同动作标签比例，而非依赖启发式设定 $\lambda = M/(N+M)$？
3. **如何在不依赖文本提示的情况下实现通用的物体中心光流提取**？这关乎方法在开放场景中的部署能力。
4. **光流约束是否可用于更复杂的具身基础模型（如 VLA）预训练**？这涉及将运动先验注入更大规模的世界模型。

### 4. 知识库定位

LAOF 处于**无监督/弱监督表征学习**与**基于模型的强化学习**的交叉地带，其知识贡献可定位于以下坐标：

- **运动先验注入**：区别于利用语言监督（如 VLMs）或动作标签的方法，LAOF 选择光流作为低成本、高信息密度的运动先验。典型相关分析（Table 4）表明光流特征与物理动作高度相关，这为“光流可作为动作的代理监督信号”提供了定量依据。
- **架构设计原则**：消融实验（Table 3）确立了“专用光流解码器优于集成到 FDM 中”的设计原则——LAOF 的专用解码器变体取得最佳性能，而将光流约束集成到 FDM（LAOF-FlowFDM）或对光流进行自编码（LAOF-AE）均不如直接解码。
- **训练稳定性**：LAOF-Action 在不同 $\lambda$ 值（0.001~0.1）下保持训练稳定，而 LAOM-Action 对 $\lambda$ 敏感且表现波动（Figure 9），表明光流约束具有正则化效应，可缓解有限监督下的过拟合。

**需手动验证的定位点**：论文未提供会议/期刊发表信息，若后续正式发表，其知识库定位可能需要根据发表场合（如机器人学习顶会 CoRL / ICRA 或表征学习顶会 ICLR / NeurIPS）进行校准。

## 原文 PDF

![[paperPDFs/CVPR_2026/LAOF_Robust_Latent_Action_Learning_with_Optical_Flow_Constraints.pdf]]
