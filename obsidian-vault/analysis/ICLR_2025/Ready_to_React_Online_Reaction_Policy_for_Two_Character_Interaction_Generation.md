---
title: "READY-TO-REACT: ONLINE REACTION POLICY FOR TWO-CHARACTER INTERACTION GENERATION"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/Ready_to_React_Online_Reaction_Policy_for_Two_Character_Interaction_Generation.pdf
aliases:
- RR
- READY-TO-REACT
tags:
- ICLR_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在自回归框架中嵌入扩散模型（diffusion head）替代GPT，预测连续运动隐变量而非离散token，从而减少累积误差并支持在线流式生成。
primary_logic: 通过预测运动隐变量（VQ-VAE latent）并结合专为在线场景设计的运动解码器，实现角色间实时独立反应，可生成长时间连贯且多样的交互动作。
claims:
- Ready-to-React成功生成超过1800帧（约1分钟）的连续拳击动作，而GPT基线在约200帧后即出现方向错误、出界或冻结。
- 在反应动作生成和双角色交互生成两个场景下，本方法在FID（per-frame, per-transition, per-clip）和物理合理性指标（Jitter, Foot Sliding）上均显著优于五个基线方法。
- 消融实验证实，用扩散模型替换GPT后，双角色Per-clip FID从61.117降低至25.283；移除在线解码器或根信息输入会显著损害运动连续性和方向正确性。
- 在稀疏信号控制实验中，本方法的位置误差（2.72 vs 14.52）和旋转误差（4.39 vs 22.40）远低于CAMDM，证明其可控性和实时性。
---

# READY-TO-REACT: ONLINE REACTION POLICY FOR TWO-CHARACTER INTERACTION GENERATION

> [!tip] 核心洞察
> 通过预测运动隐变量（VQ-VAE latent）并结合专为在线场景设计的运动解码器，实现角色间实时独立反应，可生成长时间连贯且多样的交互动作。

| 字段 | 内容 |
|------|------|
| 中文题名 | Ready-to-React：双角色交互生成的在线反应策略 |
| 英文题名 | READY-TO-REACT: ONLINE REACTION POLICY FOR TWO-CHARACTER INTERACTION GENERATION |
| 会议/期刊 | ICLR 2025 |
| Links | [Project](https://zju3dv.github.io/ready\_to\_react/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Ready-to-React |
| Dataset | DuoBox |

> [!tip] 效果简介
> - DuoBox (sparse signal reactive) 上，FID Per-frame 0.249 vs 0.697 (CAMDM) (improved by 0.448)；Position Error 2.72 vs 14.52 (CAMDM) (reduced by 11.8)；Rotation Error 4.39 vs 22.40 (CAMDM) (reduced by 18.01)。
> - DuoBox (two-character generation) 上，FID Per-clip 25.283 vs best baseline (T2MGPT) substantially higher (significantly lower than all baselines)。
> - DuoBox (long-term generation, 1800 frames) 上，generation stability (max frames without collapse) >1800 frames vs ~200 frames (GPT-based) (at least 8x longer)。

## 概述

**待解决问题**：双角色交互动作生成是计算机动画的核心挑战之一。现有方法（如基于GPT的自回归模型）存在两个根本缺陷：一是无法模拟真实场景中角色独立、在线的反应过程——它们通常需要离线访问完整序列或未来信息；二是自回归预测离散运动token会产生严重的**错误累积**，导致长期生成质量急剧劣化（约200帧后即出现方向错误、出界或冻结）。

**核心方法**：Ready-to-React 提出了一种**在线反应策略**，将扩散模型（DDPM）嵌入自回归框架中作为“扩散头”（diffusion head），替代传统GPT的离散token预测。其关键洞察在于：预测连续的**运动隐变量**（VQ-VAE latent）而非离散token，从根本上减少累积误差；同时设计专为在线场景打造的**运动解码器**，利用过去帧和两个连续隐变量实时解码未来运动，使两个角色能够独立、流式地生成交互动作，理论上无长度限制。

**方法定位**：该方法属于自回归运动生成与扩散模型的交叉地带。相比于 **T2MGPT**（Zhang et al., CVPR 2023）的GPT+离散token方案、**CAMDM**（Chen et al., SIGGRAPH 2024）的自回归扩散控制方案，以及 **Duolando**（Siyao et al., ICLR 2024）的基于GPT的跟随者生成方案，Ready-to-React 在生成范式上做出了“预测连续隐变量+在线解码”的差异化设计，使其在长期稳定性和在线实时性上形成独特优势。

**主要结果**：
- **长期生成稳定性**：成功生成超过1800帧（约1分钟）的连续拳击动作，而GPT基线在约200帧后即崩溃（Figure 1）。
- **双角色生成质量**：在DuoBox数据集上，双角色Per-clip FID达到25.283，显著优于所有五个基线方法（Table 1）。
- **反应动作质量**：在反应动作生成场景下，Per-frame FID、Per-transition FID及物理合理性指标（Jitter、Foot Sliding）均全面领先（Table 1）。
- **稀疏信号可控性**：位置误差（2.72 vs 14.52）和旋转误差（4.39 vs 22.40）远低于CAMDM，证明其出色的实时可控性（Table 4）。
- **消融验证**：用扩散模型替换GPT后，双角色Per-clip FID从61.117降至25.283；移除在线解码器或根信息输入会显著损害运动连续性和方向正确性（Table 3）。

**局限与展望**：当前方法仅针对两人交互设计，训练数据限于拳击动作，尚未整合场景/物体交互。未来工作将探索多人交互扩展、跨动作类型泛化，以及全身密集控制等方向。

## 背景与动机

双角色交互动作生成是计算机动画与具身智能领域的核心挑战之一，其目标是根据对手的行为实时生成自然、连贯且物理合理的反应动作。这一任务在游戏、虚拟现实、机器人仿真等场景中具有广泛的应用前景。然而，现有方法在模拟真实在线交互过程时面临两个根本性瓶颈。

**现有方法的根本缺陷：离线生成与错误累积。** 当前主流的双角色交互生成方法通常将两个角色的运动视为一个整体序列进行离线建模，无法模拟真实场景中角色独立、实时地观察对手并做出反应的过程。具体而言，基于GPT的自回归模型（如**T2MGPT**（Zhang et al., CVPR 2023））通过预测离散运动token的概率分布来生成动作，但这类方法存在严重的错误累积问题——每步预测的微小偏差会在自回归过程中被逐步放大，导致长期生成质量急剧劣化。如Figure 1所示，GPT基线在生成约200帧后即出现方向错误、出界或冻结等灾难性失效，而真实交互场景往往需要持续数分钟的运动序列。

**在线反应策略的建模空白。** 从问题定义来看，双角色交互的本质是一个在线反应过程：每个角色需要根据自身及对手的历史运动，独立决定下一时刻的动作。这一过程可形式化为反应策略 $\mathcal{P}$：$\mathbf{A}_f = \mathcal{P}(\mathbf{O}_{i \in [f-W,f)}, \mathbf{A}_{i \in [f-W,f)})$，其中 $\mathbf{A}_f$ 为当前角色在帧 $f$ 的动作，$\mathbf{O}$ 和 $\mathbf{A}$ 分别为对手和自身在过去 $W$ 帧内的运动历史。然而，现有方法（如**InterFormer**（Chopin et al., IEEE TMM 2023）基于transformer建模反应生成，**Duolando**（Siyao et al., ICLR 2024）结合GPT与强化学习生成跟随动作）均未能在自回归框架中有效解决错误累积问题，也无法支持真正的在线流式生成。

**本文动机：在自回归框架中嵌入扩散模型。** 扩散模型在连续信号生成中展现出优于离散token预测的稳定性和多样性。本文的核心洞察是：将扩散模型（Denoising Diffusion Probabilistic Model, DDPM）作为“扩散头”嵌入自回归框架，替代GPT预测连续运动隐变量（而非离散token），可以从根本上减少累积误差。同时，配合专为在线场景设计的运动解码器，实现角色间的实时独立反应，从而支持长时间、连贯且多样的双角色交互动作生成。

## 核心创新

### 问题根源：自回归离散预测的累积错误

现有双角色交互生成方法普遍将角色运动视为离散 token 序列，采用 GPT 类自回归模型逐 token 预测。这一范式存在根本性缺陷：**离散 token 的预测误差会在自回归循环中逐步放大**，导致长期生成质量急剧劣化。如 Figure 1 所示，GPT 基线在生成约 200 帧后即出现方向错误、出界或冻结，而 Ready-to-React 可稳定生成超过 1800 帧（约 1 分钟）的连续拳击动作。

这一瓶颈的因果机制在于：GPT 预测的是离散 token 的概率分布，采样过程中的微小偏差无法被后续步骤纠正，误差单向累积；同时，VQ-VAE 解码器需要完整隐变量序列才能还原运动，无法支持在线流式生成，进一步限制了实时交互场景的应用。

### 核心操控变量：扩散模型替代 GPT 预测连续运动隐变量

Ready-to-React 的关键创新在于**将扩散模型（Denoising Diffusion Probabilistic Model, DDPM）嵌入自回归框架，直接预测连续运动隐变量而非离散 token**。具体而言，方法使用预训练的 VQ-VAE 编码器将原始运动压缩为连续隐变量序列（下采样率 $d=4$），然后以单层 MLP 作为生成模型 $\mathcal{G}$，在扩散过程中从噪声中恢复下一个运动隐变量：

$$\mathcal{L}_{\mathrm{diffusion}} = \mathbb{E}_{t \in [1,T], \mathbf{x}_0 \sim q(\mathbf{x}_0)} \left[ \| \mathbf{x}_0 - \mathcal{G}(\mathbf{x}_t, t, \mathbf{c}) \|_2 \right]$$

这一设计改变了三个关键环节（changed slots）：

| 设计维度 | 基线方案（GPT-based） | Ready-to-React 方案 |
|---------|---------------------|-------------------|
| **生成目标** | 离散 motion token 概率分布 | 连续运动隐变量（VQ-VAE latent） |
| **生成模型** | GPT（自回归 token 预测） | DDPM + 单层 MLP |
| **运动解码方式** | VQ-VAE 解码器（需完整隐变量序列） | 在线运动解码器（仅需过去帧和两个连续隐变量） |

消融实验（Table 3）直接验证了这些改变的因果效应：将扩散模型替换为 GPT 后，双角色 Per-clip FID 从 25.283 升至 61.117；移除 VQ-VAE 运动编码器（直接预测原始姿态）导致 Per-clip FID 飙升至 126.991。

### 洞察：连续隐变量预测 + 在线解码实现实时独立反应

上述技术选择背后是一个更深层的洞察：**连续隐变量空间中的预测误差具有可恢复性**——扩散模型的去噪过程天然具备误差校正能力，每一步预测都在连续空间中逼近真实分布，避免了离散采样不可逆的偏差累积。同时，**专为在线场景设计的运动解码器**利用过去 $d$ 帧运动和两个连续隐变量即可实时输出未来 $d$ 帧，使两个角色能够真正独立、并行地运行同一反应策略，实现流式生成。

这一洞察的直接证据来自稀疏信号控制实验（Table 4）：Ready-to-React 的位置误差（2.72 vs 14.52）和旋转误差（4.39 vs 22.40）远低于自回归扩散基线 **CAMDM**（Chen et al., SIGGRAPH 2024），证明连续隐变量预测在可控性和实时性上的双重优势。

### 方法谱系与知识库定位

Ready-to-React 处于**在线交互运动生成**的交叉点，其设计融合并突破了以下技术路线：

- **自回归运动生成**：**T2MGPT**（Zhang et al., CVPR 2023）和 **Duolando**（Siyao et al., ICLR 2024）采用 GPT 预测离散运动 token，受限于累积误差；Ready-to-React 保留自回归框架但将预测目标改为连续隐变量，从根本上缓解了误差累积。
- **扩散运动生成**：**CAMDM**（Chen et al., SIGGRAPH 2024）使用自回归扩散进行角色控制，但直接预测原始姿态且未针对在线双人场景优化；Ready-to-React 在隐变量空间扩散并引入历史编码器和在线解码器。
- **交互运动合成**：**InterFormer**（Chopin et al., IEEE TMM 2023）基于 Transformer 生成反应动作，但缺乏长期稳定性和在线能力；Ready-to-React 通过反应策略公式 $\mathbf{A}_f = \mathcal{P}(\mathbf{O}_{i \in [f-W,f)}, \mathbf{A}_{i \in [f-W,f)})$ 实现了角色间的独立实时反应。
- **概率运动先验**：**MoGlow**（Henter et al., TOG 2020）使用归一化流建模运动分布，作为本方法的 FID 评估编码器，确保度量一致性。

## 整体框架

Ready-to-React 的核心设计是将双角色交互生成建模为一个**在线反应策略**（online reaction policy），其形式化定义为：

$$\mathbf{A}_f = \mathcal{P}(\mathbf{O}_{i \in [f-W,f)}, \mathbf{A}_{i \in [f-W,f)})$$

该公式表明，对于未来第 $f$ 帧的智能体动作 $\mathbf{A}_f$，反应策略 $\mathcal{P}$ 仅依赖过去 $W$ 帧的对手动作 $\mathbf{O}$ 和智能体自身动作 $\mathbf{A}$ 来做出决策（Equation 1, Section 3.1）。这一范式从根本上区别于现有方法：它不要求同时生成两个角色的动作，而是让每个角色在流式推理中独立、实时地对对方行为做出反应。

### Pipeline 架构

如 Figure 2 所示，整个系统由四个核心模块串联构成：

![[assets/figures/papers/paper_list_l1783_Ready_to_React_Online_Reaction_Policy_for_Two_Character_Interaction_Gene/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline overview. Given a boxing scene at the leftmost figure, where the blue agent is thinking about its next move. The reaction policy (Section 3.2) follows these steps: first, based on the observations, the history encoder encodes the current state and observations; then, the next latent predictor predicts the upcoming motion latent; and finally, an online motion decoder decodes this motion latent into the actual next pose. The same reaction policy can be applied to the pink agent. Through a streaming process for both agents, our reaction policy enables the continuous generation of two-character motion sequences without length limit (Section 3.3)*

1. **VQ-VAE 运动编码器（预训练后固定）**：将原始运动数据压缩为离散隐变量序列。给定智能体运动 $\mathbf{A} = \{\mathbf{A}_i\}$，编码器以 $d=4$ 的下采样率将其映射到隐空间 $\mathbf{Z} = \{\mathbf{Z}_i\}$，再通过码本量化得到离散表示 $\hat{\mathbf{Z}}_i$（Equation 4, Section 3.2）。该模块在 Stage 1 完成预训练后冻结，为后续模块提供紧凑的运动表征。

2. **历史编码器（History Encoder）**：负责编码角色自身及对手的过去运动状态。自身运动经 VQ-VAE 编码器压缩为隐变量序列；对手运动则通过单层 MLP 编码至相同特征维度。两者共同构成条件信息，输入下一模块。

3. **下一隐变量预测器（Next Latent Predictor）**：这是框架的**核心生成引擎**。它首先利用基于 Transformer 的条件编码器融合历史信息，生成条件特征向量 $\mathbf{c}$；随后，一个去噪扩散概率模型（DDPM）以 $\mathbf{c}$ 为条件，预测下一个运动隐变量 $\mathbf{x}_0$。扩散模型以自回归方式运行——每步生成一个隐变量，其输出又作为下一步的历史输入。这一“自回归 + 扩散头”的设计是本方法区别于 GPT 基线的关键：**预测连续运动隐变量而非离散 token 概率**，从根本上抑制了自回归过程中的错误累积。

4. **在线运动解码器（Online Motion Decoder）**：接收过去 $d$ 帧的智能体动作 $\mathbf{A}_{i \in [f-d,f)}$、根信息 $\mathbf{R}_{i \in [f-d,f)}$，以及当前和前一时刻的运动隐变量，通过 Transformer 实时解码出未来 $d$ 帧的动作和根信息。根信息 $\mathbf{R}_i$ 包含角色相对于对手的水平轨迹偏移 $\mathbf{r}_{\mathrm{off}}^{\mathcal{O}}$、方向 $\mathbf{r}_{\mathrm{dir}}^{\mathcal{O}}$，以及距拳击台中心的距离 $\mathbf{r}_{\mathrm{dis}}$（Section 3.2）。该模块专为在线场景设计，无需等待完整隐变量序列即可逐段输出运动帧。

### 流式生成机制

在双角色交互生成中，**同一套反应策略可分别应用于蓝色和粉色智能体**（Figure 2）。流式推理过程如下：给定初始 4 帧，每个角色独立运行反应策略，预测自身下一帧动作；双方的动作输出又互为对方的“对手观察”，输入下一轮的历史编码器。这一交替预测的流式过程使得系统能够生成**无长度限制**的连续双角色运动序列（Section 3.3）。

### 训练流程

训练分为两个阶段（Section 3.4）：
- **Stage 1**：预训练 VQ-VAE 运动编码器，使用重建损失与承诺损失（commitment loss），$\alpha=0.1$，训练 40k 迭代。
- **Stage 2**：联合训练历史编码器、下一隐变量预测器和在线运动解码器。总体损失函数为：

$$\mathcal{L} = \mathcal{L}_{\mathrm{diffusion}} + \beta \| \mathbf{A} - \tilde{\mathbf{A}} \|_2^2 + \gamma \| \mathbf{R} - \tilde{\mathbf{R}} \|_2^2$$

其中 $\beta=\gamma=1.0$，$\mathcal{L}_{\mathrm{diffusion}}$ 定义为：

$$\mathcal{L}_{\mathrm{diffusion}} = \mathbb{E}_{t \in [1,T], \mathbf{x}_0 \sim q(\mathbf{x}_0)} \left[ \| \mathbf{x}_0 - \mathcal{G}(\mathbf{x}_t, t, \mathbf{c}) \|_2 \right]$$

即预测去噪后隐变量与真实隐变量之间的期望 L2 距离。扩散过程设置 $T=1000$ 时间步，推理时使用 DDIM 采样 50 步。所有模型使用 AdamW 优化器（学习率 0.0001）在单张 Nvidia RTX 4090 GPU 上训练。

## 核心模块与公式推导

### 问题形式化

Ready-to-React 将双角色交互生成建模为一个在线反应策略问题。给定时间窗口 $W$ 内的历史观测，反应策略 $\mathcal{P}$ 为每个智能体预测未来帧的动作。策略的形式化定义为：

$$\mathbf{A}_f = \mathcal{P}(\mathbf{O}_{i \in [f-W,f)}, \mathbf{A}_{i \in [f-W,f)})$$

其中 $\mathbf{A}_f$ 表示智能体在未来帧 $f$ 的动作，$\mathbf{O}$ 为对手动作，$\mathbf{A}$ 为智能体自身动作。该公式确立了在线反应的核心机制：每个角色仅基于自身和对手的过去信息独立决策，无需访问对手的未来状态。

每帧动作 $\mathbf{A}_i$ 包含完整的运动表示：水平轨迹偏移 $\mathbf{r}_{\mathrm{off}}^A \in \mathbb{R}^2$、朝向方向 $\mathbf{r}_{\mathrm{dir}}^A \in \mathbb{R}^2$、关节位置 $\boldsymbol{\Theta}_{\mathrm{pos}}^A \in \mathbb{R}^{J \times 3}$、6D旋转表示 $\boldsymbol{\Theta}_{\mathrm{rot}}^A$ 以及对应的速度量。

### 流水线核心模块

如图 Figure 2 所示，反应策略由四个核心模块串联构成，形成“编码-预测-解码”的在线推理流水线。

**VQ-VAE运动编码器（预训练后固定）** 将原始运动序列压缩为离散隐变量序列。给定智能体运动序列 $\mathbf{A} = \{\mathbf{A}_i \mid i \in [0, f), i \in \mathbb{Z}\}$，编码器以采样率 $d=4$ 将其映射为隐变量 $\mathbf{Z} = \{\mathbf{Z}_i \mid i \in [0, \lfloor f/d \rfloor), i \in \mathbb{Z}\}$。量化过程通过查找码本 $\mathcal{C}$ 中最接近的元素完成：

$$\hat{\mathbf{Z}}_i = \underset{\mathcal{C}_k \in \mathcal{C}}{\arg\min} \left\| \mathbf{Z}_i - \mathcal{C}_k \right\|_2$$

码本大小为512，特征维度为512。该模块在Stage 1预训练完成后固定，不再参与后续梯度更新。

**历史编码器** 负责融合双角色历史信息。自身运动经VQ-VAE编码器压缩为隐变量序列，对手运动则通过单层MLP编码至相同特征维度。这一设计的关键在于将不对称的信息源（自身精细运动 vs. 对手观测）统一到共享的表示空间，为后续预测提供完整的上下文。

**下一隐变量预测器** 是方法的核心创新点。该模块采用transformer-based条件编码器融合历史信息，生成条件特征向量 $\mathbf{c}$，随后由扩散模型（DDPM）以自回归方式预测下一个运动隐变量。与现有GPT-based方法预测离散token概率不同，本方法直接预测连续的VQ-VAE隐变量，从根本上改变了误差传播机制——连续隐空间的微小偏差不会像离散token错误那样导致灾难性的级联失效。

**在线运动解码器** 专为流式场景设计。输入包括过去 $d$ 帧的智能体动作 $\mathbf{A}_{i \in [f-d,f)}$、根信息 $\mathbf{R}_{i \in [f-d,f)}$、以及当前和前一时刻的运动隐变量。根信息 $\mathbf{R}_i$ 的定义为：

$$\mathbf{R}_i = \{ \mathbf{r}_{\mathrm{off}}^{\mathcal{O}} \in \mathbb{R}^{2}, \mathbf{r}_{\mathrm{dir}}^{\mathcal{O}} \in \mathbb{R}^{2}, \mathbf{r}_{\mathrm{dis}} \in \mathbb{R}^{1} \}$$

其中 $\mathbf{r}_{\mathrm{off}}^{\mathcal{O}}$ 和 $\mathbf{r}_{\mathrm{dir}}^{\mathcal{O}}$ 为相对于对手根坐标系的水平轨迹位置和朝向，$\mathbf{r}_{\mathrm{dis}}$ 为到拳击台中心的距离。解码器使用transformer架构，输出未来 $d$ 帧的运动和根信息。与标准VQ-VAE解码器需要完整隐变量序列不同，该模块仅依赖两个连续隐变量即可实时解码，是实现真正在线生成的关键。

### 训练损失函数

Stage 2联合训练的总体损失由三项组成：

$$\mathcal{L} = \mathcal{L}_{\mathrm{diffusion}} + \beta \| \mathbf{A} - \tilde{\mathbf{A}} \|_2^2 + \gamma \| \mathbf{R} - \tilde{\mathbf{R}} \|_2^2$$

其中 $\beta = \gamma = 1.0$。第一项为扩散模型的重构损失，定义在连续隐变量空间：

$$\mathcal{L}_{\mathrm{diffusion}} = \mathbb{E}_{t \in [1,T], \mathbf{x}_0 \sim q(\mathbf{x}_0)} \left[ \| \mathbf{x}_0 - \mathcal{G}(\mathbf{x}_t, t, \mathbf{c}) \|_2 \right]$$

该损失衡量去噪后的预测隐变量 $\mathcal{G}(\mathbf{x}_t, t, \mathbf{c})$ 与真实隐变量 $\mathbf{x}_0$ 的L2距离期望。扩散时间步 $T=1000$，推理时使用DDIM采样50步。后两项分别为动作重建损失和根信息重建损失，确保解码器输出的运动序列与根轨迹的准确性。

VQ-VAE预训练阶段使用重构损失与承诺损失（commitment loss）的组合：

$$\mathcal{L}_{\mathrm{vqvae}} = \mathcal{L}_{\mathrm{rec}} + \alpha \| \mathrm{sg}[\hat{\mathbf{Z}}] - \mathbf{Z} \|_2^2$$

其中 $\alpha = 0.1$，$\mathrm{sg}[\cdot]$ 为停止梯度算子。所有模型使用AdamW优化器训练，学习率0.0001，在单张Nvidia RTX 4090 GPU上完成。

## 实验与分析

### 4.1 实验设置与评估协议

所有实验基于 **DuoBox** 拳击数据集进行，按80%训练/20%测试划分。评估指标包括三类 **FID**（per-frame、per-transition、per-clip），通过预训练的 **MoGlow**（Henter et al., TOG 2020）编码器计算特征分布距离，确保度量一致性。物理合理性由 **Jitter**（加速度抖动）和 **Foot Sliding**（足部滑动）量化。对比方法在相同初始条件（4帧起始姿势）和硬件环境下进行评估，推理时间纳入实时性考量。

### 4.2 主实验结果

#### 4.2.1 反应动作生成

在给定对手真实运动序列的条件下，**Ready-to-React** 在所有指标上均显著优于五个基线方法（Table 1 左侧）。具体而言，本方法在 per-clip FID 上达到 **36.755**，远低于基于GPT的 **T2MGPT**（Zhang et al., CVPR 2023）和基于归一化流的 **MoGlow**。在物理合理性方面，足部滑动（FS）仅为31.3%，表明生成的反应动作具有更好的地面接触一致性。

![[assets/figures/papers/paper_list_l1783_Ready_to_React_Online_Reaction_Policy_for_Two_Character_Interaction_Gene/figures/003_Table_1.jpg]]
*Table 1: Comparison with baselines. We compare our method with five baselines (Section 4.2) in the two scenarios: reactive motion generation and two-character motion generation. Among them, bold indicates the best results. ↓ means lower is better. → means closer to the real data is better*

定性对比（Figure 5）揭示了基线的典型失败模式：
- **InterFormer**（Chopin et al., IEEE TMM 2023）生成的反应动作过于靠近对手，导致穿透。
- **CAMDM**（Chen et al., SIGGRAPH 2024）在长期生成中趋于卡顿。
- **Duolando**（Siyao et al., ICLR 2024）在一段时间后出现方向错误。

![[assets/figures/papers/paper_list_l1783_Ready_to_React_Online_Reaction_Policy_for_Two_Character_Interaction_Gene/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative results of generating reactive motions. Given the same ground truth opponent motion, InterFormer can produce reactive motion that is too close to the opponent, leading to penetration. CAMDM tends to get stuck, while Duolando may result in human motion with incorrect orientation after a certain period*

#### 4.2.2 双角色交互生成

在同时生成两个角色动作的场景下，本方法的优势更为突出（Table 1 右侧）。per-clip FID 低至 **25.283**，而最佳基线 **T2MGPT** 的对应指标显著更高。Jitter 仅 **16.844**，足部滑动 **0.97**，均优于所有对比方法。Figure 3 的面朝方向可视化进一步证实：本方法生成的双方朝向角度（蓝色曲线）紧密跟随真实数据（绿色曲线），而基线方法（红色曲线）在长时间生成中逐渐偏离，出现背对或方向混乱。

![[assets/figures/papers/paper_list_l1783_Ready_to_React_Online_Reaction_Policy_for_Two_Character_Interaction_Gene/figures/005_Figure_3.jpg]]
*Figure 3: Visualization of the face direction relative to time. We compare our method with baselines in two scenarios described in Section 4.2. The x-axis represents the frame number f, while the y-axis shows the angle between the facing directions of the two characters (in degrees). An angle of 0◦ indicates that the two agents are facing each other, whereas ±180◦ means they are facing away from each other. The green lines represent the ground truth, the blue lines represent our method, and the red lines represent the baselines*

#### 4.2.3 长期生成稳定性

Table 2 报告了1800帧（约1分钟）的长期生成结果。**Ready-to-React** 成功保持了运动连贯性和交互合理性，而基于GPT的方法在约200帧后即出现方向错误、出界或冻结（Figure 1）。这一对比直接验证了核心瓶颈——**自回归离散token预测存在严重的错误累积**，而本方法通过预测连续运动隐变量有效抑制了该问题。

![[assets/figures/papers/paper_list_l1783_Ready_to_React_Online_Reaction_Policy_for_Two_Character_Interaction_Gene/figures/001_Figure_1.jpg]]
*Figure 1: Demonstration of Ready-to-React, an online reaction policy for two-character interaction generation on the challenging task of boxing. Ready-to-React predicts the next pose of an agent by considering its own and the counterpart’s historical motions. Our method can successfully generate 1800 frames of motion, whereas the GPT-based approach struggles after about 200 frames, displaying issues such as incorrect orientation, leaving the ring boundary, or freezing in place due to the accumulation of errors over time*

![[assets/figures/papers/paper_list_l1783_Ready_to_React_Online_Reaction_Policy_for_Two_Character_Interaction_Gene/figures/004_Table_2.jpg]]
*Table 2: Quantitative results of long-term two-character motion generation. We compare our method with four baselines (Section 4.2). The generated motion lengths are set to 1800 frames*

### 4.3 消融实验

Table 3 系统验证了五个关键设计选择，所有消融变体均导致性能显著下降：

![[assets/figures/papers/paper_list_l1783_Ready_to_React_Online_Reaction_Policy_for_Two_Character_Interaction_Gene/figures/006_Table_3.jpg]]
*Table 3: Ablation study. We compare our method with five variants to validate our main design choices (please refer to Section 4.3 for details). Among them, bold indicates the best results. ↓ means lower is better. → means closer to the real data is better*

1. **移除VQ-VAE运动编码器（w/o motion encoder）**：直接预测原始姿态序列，双角色 per-clip FID 从25.283飙升至 **126.991**。这表明在压缩的隐空间中进行生成对于运动质量至关重要。
2. **用GPT替换扩散模型（use GPT）**：per-clip FID 升至 **61.117**，且运动稳定性明显劣化。这直接证明了扩散头（diffusion head）替代GPT是减少累积误差的核心因果机制。
3. **移除在线解码器（w/o online decoder）**：使用原始VQ-VAE解码器（需完整隐变量序列）导致运动不连续，FID显著升高。这证实了专为在线场景设计的解码器对于流式生成的必要性。
4. **移除解码器中的根信息R（w/o R in decoder）**：模型频繁预测错误的面朝方向，验证了根信息（对手相对位置、方向、距离）对于交互空间感知的关键作用。
5. **禁用角色交换增强（w/o augmentation）**：性能略有下降，表明该数据增强策略对模型鲁棒性有一定贡献。

### 4.4 稀疏信号控制实验

Table 4 展示了在稀疏控制信号（DuoBox reactive setting）下的对比结果。**Ready-to-React** 的位置误差仅 **2.72**（CAMDM为14.52），旋转误差仅 **4.39**（CAMDM为22.40），per-frame FID 为 **0.249**（CAMDM为0.697）。Figure 4 的定性结果显示，本方法能准确响应稀疏目标点（红色标记），而CAMDM在相同条件下出现响应迟滞和精度不足（红色圆圈标注区域）。这证明本方法在保持实时性的同时，具备更强的可控性。

![[assets/figures/papers/paper_list_l1783_Ready_to_React_Online_Reaction_Policy_for_Two_Character_Interaction_Gene/figures/007_Table_4.jpg]]
*Table 4: Quantitative results of generating reactive motion from sparse signals. We compare our method with CAMDM. Among them, bold indicates the best results. ↓ means lower is better. → means closer to the real data is better. Our method outperforms the baseline in terms of all metrics*

![[assets/figures/papers/paper_list_l1783_Ready_to_React_Online_Reaction_Policy_for_Two_Character_Interaction_Gene/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative results of generating reactive motions from sparse signals. We compare our method with CAMDM. Our approach successfully generates realistic motion while effectively adhering to the sparse signals (annotated by red dots in the figures). In contrast, CAMDM struggles to achieve the same level of responsiveness and accuracy, as shown in the red circles*

### 4.5 失败模式与局限性

尽管整体性能优异，本方法存在以下已知局限：
- **场景限制**：当前设计仅针对两人交互，无法直接处理多人或群组场景。
- **环境交互缺失**：模型未考虑与场景物体的交互，限制了在复杂三维环境中的应用。
- **动作类型泛化**：训练数据仅包含拳击动作，向其他交互类型的迁移需要额外数据收集与训练。

### 补充图表

![[assets/figures/papers/paper_list_l1783_Ready_to_React_Online_Reaction_Policy_for_Two_Character_Interaction_Gene/figures/010_Figure_6.jpg]]
*Figure 6: Qualitative results of generating two-character motions. Given the same initial four frames for both characters, InterFormer tends to produce human motion with incorrect orientation. CAMDM often results in the characters getting stuck, while T2MGPT can cause the two characters to drift apart due to accumulated errors*

## 方法谱系与知识库定位

### 问题瓶颈与核心差异

现有双角色交互生成方法普遍面临两个关键瓶颈：其一，无法模拟真实的**在线独立反应过程**——多数方法假设角色能同时获取双方完整的未来运动序列，这与现实交互中每个角色仅能基于历史观察独立决策的设定相悖；其二，基于GPT的自回归模型存在严重的**错误累积问题**，导致长期生成质量急剧劣化——如Figure 1所示，GPT基线在约200帧后即出现方向错误、出界或冻结，而Ready-to-React可稳定生成超过1800帧（约1分钟）的连续拳击动作。

Ready-to-React的核心差异在于**在自回归框架中嵌入扩散模型（diffusion head）替代GPT**，将生成目标从离散token概率分布转变为连续运动隐变量（VQ-VAE latent）的预测。这一设计选择直接针对错误累积的因果机制：离散token预测的误差会逐帧放大，而扩散模型在连续隐空间中的去噪过程天然具有更强的误差容忍度和恢复能力。消融实验（Table 3）定量验证了这一机制——将扩散模型替换为GPT后，双角色Per-clip FID从25.283恶化至61.117。

### 与基线方法的关系定位

**CAMDM** (Chen et al., SIGGRAPH 2024) 是自回归扩散基线，同样使用扩散模型进行角色控制，但其设计目标为单角色运动控制，缺乏对双角色交互历史的信息编码。在稀疏信号控制实验中（Table 4），Ready-to-React的位置误差（2.72 vs 14.52）和旋转误差（4.39 vs 22.40）远低于CAMDM，证明其历史编码和在线解码设计对交互场景的实时可控性具有决定性作用。定性结果（Figure 4）进一步显示，CAMDM在稀疏信号下难以精确响应控制点，而Ready-to-React能有效遵循信号并生成真实感运动。

**Duolando** (Siyao et al., ICLR 2024) 采用GPT-based的跟随者运动生成，结合强化学习进行训练。其局限在于GPT的自回归token预测本质导致长期生成中的误差累积，且强化学习的奖励设计难以覆盖所有交互场景的物理合理性。Figure 5显示Duolando在一段时间后会出现角色朝向错误。

**InterFormer** (Chopin et al., IEEE TMM 2023) 是基于transformer的交互反应生成方法，但其设计假设可访问双方完整序列，不支持在线流式生成。Figure 5和Figure 6的定性结果显示，InterFormer生成的交互动作可能出现穿透（角色过于接近对手）或方向错误。

**T2MGPT** (Zhang et al., CVPR 2023) 是典型的GPT-based离散token运动生成方法，其错误累积问题在双角色场景下尤为突出——Table 1中T2MGPT的各项FID指标均显著劣于Ready-to-React，Figure 6显示其生成的两个角色会因累积误差逐渐漂移分开。

**MoGlow** (Henter et al., TOG 2020) 基于归一化流的概率运动合成，在本工作中主要作为FID计算的预训练编码器，确保度量一致性。

### 关键设计选择的消融证据

Table 3的消融实验揭示了以下因果链条：

1. **VQ-VAE运动编码器**是信息压缩的关键瓶颈：移除编码器直接预测原始姿态序列时，双角色Per-clip FID从25.283飙升至126.991。这表明隐空间表征不仅降低了预测维度，更重要的是通过码本学习提取了运动的结构化先验。

2. **在线运动解码器**决定了流式生成的连续性：使用原始VQ-VAE解码器（需要完整隐变量序列）替代在线解码器后，运动出现明显不连续。在线解码器的设计——仅依赖过去d帧运动和两个连续隐变量——是实现真正在线反应的技术基础。

3. **根信息R的输入**直接影响方向正确性：移除解码器中的根信息输入后，模型频繁预测错误朝向。根信息包含相对对手坐标系的水平轨迹位置、方向及距拳台中心的距离，为角色提供了空间感知能力。

4. **角色交换数据增强**对性能有正向贡献，但影响程度相对较小。

### 适用边界与局限

1. **交互规模限制**：当前方法仅针对两人交互设计，无法直接处理多人或群组交互场景。反应策略的公式 $\mathbf{A}_f = \mathcal{P}(\mathbf{O}_{i \in [f-W,f)}, \mathbf{A}_{i \in [f-W,f)})$ 假设单一对手，扩展到多人需要重新设计历史编码和条件融合机制。

2. **场景交互缺失**：模型未考虑与场景或物体的交互，限制了其在更复杂的真实世界任务（如带障碍物的格斗、道具使用等）中的应用。根信息中的 $\mathbf{r}_{\mathrm{dis}}$ 仅编码到拳台中心的距离，缺乏对三维场景几何的感知。

3. **动作类型泛化不足**：训练数据仅包含拳击动作，泛化到其他类型的交互动作（如舞蹈、球类运动）可能需要额外的数据收集和训练。不同交互类型的运动模式、节奏和空间关系差异显著。

4. **推理效率的潜在权衡**：扩散模型的去噪过程（DDIM 50步采样）相比GPT的单步token采样增加了推理计算量，在需要极低延迟的应用场景中可能构成限制。

### 开放问题

1. **多角色扩展**：如何将反应策略从两人场景扩展到多人物交互，同时保持计算效率和各角色间的一致性？可能的路径包括图神经网络建模角色间关系，或引入注意力机制动态选择相关对手。

2. **场景-角色联合感知**：如何整合环境与物体交互，使角色能够感知并响应周围的三维场景？这需要将场景几何信息融入历史编码器，并在解码器中加入场景约束。

3. **跨动作泛化**：反应策略如何对不同种类的交互动作进行泛化，而无需为每种动作重新收集数据和训练？可能的方案包括元学习、条件生成或大规模多动作预训练。

4. **控制粒度提升**：能否将稀疏控制信号（如关键点位置）扩展到全身密集控制，以支持更沉浸式的VR交互体验？这需要在隐空间中建立更精细的控制映射机制。

## 原文 PDF

![[paperPDFs/ICLR_2025/Ready_to_React_Online_Reaction_Policy_for_Two_Character_Interaction_Generation.pdf]]
