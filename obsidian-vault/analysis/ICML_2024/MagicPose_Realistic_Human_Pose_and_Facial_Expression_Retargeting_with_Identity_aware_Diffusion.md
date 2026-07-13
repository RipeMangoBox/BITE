---
title: "MagicPose: Realistic Human Pose and Facial Expression Retargeting with Identity-aware Diffusion"
type: paper
paper_level: A
venue: ICML
year: 2024
pdf_ref: paperPDFs/ICML_2024/MagicPose_Realistic_Human_Pose_and_Facial_Expression_Retargeting_with_Identity_aware_Diffusion.pdf
project_link: null
code_link: https://github.com/Boese0601/MagicDance
aliases:
- MagicPose
tags:
- ICML_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "引入可训练的外观控制模型（Appearance Control Model）作为SD-UNet的副本，通过Multi-Source自注意力模块拼接参考图像的键值对，配合两阶段训练策略（先外观控制预训练冻结骨干，后联合微调解耦姿态控制），实现稳定的外观保持与姿态控制分离。"
primary_logic: "扩散UNet的自注意力层可作为外观变形模块：将参考图像的特征以键值对形式注入生成过程即可实现外观的跨姿态传递。在此基础上，用一个专门训练的外观控制副本取代零样本注意力连接，可在不依赖文本提示的情况下提供鲁棒的外观引导，并允许姿态控制网络独立学习而不干扰外观。"
claims:
- "外观控制预训练（Appearance Control Pretraining）使Face-Cos从0.038提升至0.426（+944.73%），SSIM从0.291提升至0.752（+149.82%）。"
- "加入外观解耦的姿态控制（Appearance-disentangled Pose Control）后，Face-Cos进一步从0.397提升至0.426（+7.30%），SSIM从0.727提升至0.752（+3.43%）。"
- "在TikTok数据集上，MagicPose取得FID 25.50、Face-Cos 0.426，Face-Cos相较DisCo提升0.260（+156%），全面超越现有方法。"
- "零样本域外泛化测试（包括全身数据集Everybody Dance Now和风格迥异的参考图像）中，MagicPose无需微调仍保持身份与姿态一致性。"
---

# MagicPose: Realistic Human Pose and Facial Expression Retargeting with Identity-aware Diffusion

> [!tip] 核心洞察
> 扩散UNet的自注意力层可作为外观变形模块：将参考图像的特征以键值对形式注入生成过程即可实现外观的跨姿态传递。在此基础上，用一个专门训练的外观控制副本取代零样本注意力连接，可在不依赖文本提示的情况下提供鲁棒的外观引导，并允许姿态控制网络独立学习而不干扰外观。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MagicPose: 基于身份感知扩散的真实感人像姿态与表情重定向 |
| 英文题名 | MagicPose: Realistic Human Pose and Facial Expression Retargeting with Identity-aware Diffusion |
| 会议/期刊 | ICML 2024 |
| Links | [paper](https://arxiv.org/abs/2311.12052) · [GitHub](https://github.com/Boese0601/MagicDance) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | MagicPose |
| Dataset | TikTok |

> [!tip] 效果简介
> - TikTok 上，FID 为 25.50，对比 50.68 (DisCo)，变化 -25.18。
> - TikTok 上，SSIM 为 0.752，对比 0.648 (DisCo)，变化 +0.104。
> - TikTok 上，PSNR 为 29.53，对比 28.81 (DisCo)，变化 +0.72。

## 概要

**核心问题**：现有扩散模型在人体姿态与表情重定向中面临一个根本性瓶颈——外观保持与姿态控制高度耦合。常规方案（如直接使用ControlNet或零样本自注意力连接）无法稳定地将参考图像的外观信息传递到生成结果中，导致身份丢失，或需要针对新域进行微调才能维持外观一致性。

**核心方法**：MagicPose通过引入一个**可训练的外观控制模型（Appearance Control Model）**，作为Stable Diffusion UNet的副本，配合**多源自注意力模块（Multi-Source Self-Attention Module）**将参考图像的键值对注入生成过程，实现外观的跨姿态传递。在此基础上，采用**两阶段训练策略**——先进行外观控制预训练并冻结骨干网络，再进行外观-姿态解耦的联合微调——从根本上分离了外观保持与姿态控制两个任务。

**方法定位**：MagicPose属于基于扩散模型的2D人体姿态与表情重定向方法，可作为Stable Diffusion的即插即用扩展，无需修改预训练权重。在方法谱系中，它区别于直接使用目标图像的GAN方法（如FOMM、MRAA、TPS）和依赖CLIP提取外观的扩散方法（如DisCo），通过专用的外观控制副本实现了更鲁棒的身份保持。

**主要结果**：
- 在TikTok数据集上，MagicPose取得FID 25.50、Face-Cos 0.426，Face-Cos相较DisCo提升0.260（+156%），全面超越现有方法（Table 1）。
- 消融实验证实，外观控制预训练是身份保持的关键：移除后Face-Cos从0.426骤降至0.038（-944.73%），SSIM从0.752降至0.291（-149.82%）（Table 3）。
- 零样本域外泛化测试中，MagicPose无需微调即可在全身数据集Everybody Dance Now及风格迥异的参考图像上保持身份与姿态一致性（Table 4, Figure 6-8）。
- 100人用户研究中，73%的票数选择MagicPose为身份保持最优方法（p-value = 1.11e-12）（Table 2, Table 5）。

### 问题背景：姿态重定向中的身份保持困境

2D人体姿态与表情重定向（retargeting）旨在将参考图像中的人物外观迁移到目标姿态序列上，同时保持面部表情、肤色、着装等身份特征的连贯性。这一任务在虚拟主播、影视制作、游戏角色动画等场景中具有明确的应用需求，其核心挑战在于：**如何在精确跟随目标姿态的同时，不丢失参考人物的身份外观信息**。

早期方法主要基于生成对抗网络（GAN）或薄板样条（TPS）变形，如 **FOMM**、**MRAA** 和 **TPS**，它们直接使用目标图像作为输入，包含的姿态信息比OpenPose骨架更丰富，但在复杂姿态变化下仍会出现面部表情不一致和人体外观失真。近年来，扩散模型（diffusion models）在图像生成领域展现出强大的能力，催生了 **DreamPose**（时尚视频生成）和 **DisCo**（舞蹈生成）等工作，尝试将扩散模型引入姿态重定向。然而，这些方法在身份保持方面存在根本性瓶颈。

### 核心瓶颈：外观控制与姿态控制的高度耦合

现有扩散模型在姿态重定向中面临一个关键矛盾：**外观控制与姿态控制高度耦合**。具体表现为两类典型失败模式：

1. **零样本自注意力连接的不稳定性**：直接将参考图像的自注意力键值对注入生成过程（如DisCo的CLIP外观提取方案），可以在一定程度上传递外观信息，但缺乏专门训练的引导机制，导致身份外观在不同姿态下发生漂移或丢失。

2. **直接联合训练的相互干扰**：若将外观控制模块与姿态ControlNet直接联合训练，姿态控制网络会“学会依赖”外观信息，造成身份混淆——即生成结果中的人物外观会随着目标姿态的变化而发生不应有的改变。

这两种失败模式的根本原因在于：扩散UNet的自注意力层虽然天然具备外观变形的潜力（将参考图像特征以键值对形式注入即可实现跨姿态传递），但**未经专门训练的外观引导缺乏鲁棒性，而未经解耦的训练策略又使姿态控制干扰了外观保持**。

### 现有方法的缺口

从方法谱系来看，现有工作存在以下缺口：

- **基于GAN的方法**（FOMM、MRAA、TPS）：直接依赖目标图像输入，在域内表现尚可，但泛化能力有限，且对大幅度姿态变化的鲁棒性不足。
- **基于扩散的零样本方法**（DisCo）：利用CLIP提取外观信息并控制姿态，但外观保持能力弱——在TikTok数据集上，DisCo的Face-Cos仅为0.166，与MagicPose的0.426相差0.260（+156%），表明其身份保持能力严重不足。此外，DisCo在预训练阶段使用了额外的公开数据集（如LAION），而MagicPose仅使用TikTok的335个视频序列，在更少数据下获得了更优性能。
- **通用ControlNet方案**：vanilla ControlNet尝试直接控制外观，但无法稳定维持身份外观，且依赖文本提示进行外观描述，缺乏对参考图像的精确外观引导。

### 本文动机

基于上述分析，本文的核心动机可归纳为三点：

1. **构建可训练的外观控制机制**：用专门训练的Appearance Control Model取代零样本自注意力连接，使其在不依赖文本提示的情况下提供鲁棒的外观引导，从根本上解决身份丢失问题。

2. **实现外观与姿态的解耦**：通过两阶段训练策略（先外观控制预训练冻结骨干，后联合微调解耦姿态控制），使姿态控制网络独立学习而不干扰外观保持，消除直接联合训练带来的身份混淆。

3. **保持即插即用的泛化能力**：在不修改Stable Diffusion预训练权重的条件下，将所提模块作为插件集成，支持零样本域外泛化——包括全身数据集（Everybody Dance Now）和风格迥异的参考图像（2D卡通、T2I生成图像等），无需针对新域微调。

## 核心方法与创新机理

MagicPose的核心创新在于**将扩散UNet的自注意力层重新定位为外观变形模块**，并通过专门设计的可训练组件和两阶段训练策略，系统性地解决了现有扩散模型在人体姿态重定向中**外观控制与姿态控制高度耦合**的根本瓶颈。

### 瓶颈诊断：为何现有方法无法稳定保持身份？

在扩散模型中进行姿态重定向时，核心矛盾在于：生成过程需要同时满足来自参考图像的外观约束和来自目标姿态的条件约束，但这两类信号在标准扩散UNet中缺乏有效的分离机制。初步实验（Figure 3）揭示了两种常见思路的失败模式：

- **Vanilla ControlNet**直接接收参考图像作为条件输入，试图同时完成外观传递和姿态控制，但结果完全无法维持参考身份的外观特征，生成图像的身份信息严重丢失。
- **零样本自注意力连接**（zero-shot connected self-attention）将参考图像的特征以键值对形式直接注入SD-UNet的自注意力层，虽能产生外观相似性，但生成结果极不稳定，缺乏可控性。

这两种失败指向同一个根本原因：**外观控制需要层次化、可学习的特征传递机制，而非简单的条件注入或零样本注意力拼接**。

### 核心洞察：自注意力层即外观变形模块

MagicPose的核心洞察在于：扩散UNet中的自注意力层天然具备跨图像外观传递的能力。其内在机制是——将参考图像的特征以键（Key）和值（Value）的形式注入生成过程，查询（Query）来自目标生成图像，注意力权重自动建立跨图像的外观对应关系。这一洞察将复杂的身份保持问题转化为**可训练的外观键值对提取与注入问题**。

基于此洞察，MagicPose设计了两个关键的changed slots，分别对应外观控制机制和训练策略的改进。

### Changed Slot 1：从零样本注意力连接到可训练外观控制模型

**Baseline做法**：零样本自注意力连接直接将参考图像和生成图像的自注意力键值对拼接，无需训练即可产生外观相似性，但生成不稳定且无法精细控制身份特征。

**MagicPose方案**：引入**Appearance Control Model**——一个SD-UNet的完整可训练副本，通过**Multi-Source Self-Attention Module**与冻结的SD-UNet进行层次化的键值对拼接。具体而言，外观控制模型接收参考图像 $I_R$，在各Transformer Block中提取键值对 $(K_2, V_2)$，与SD-UNet自身的键值对 $(K_1, V_1)$ 拼接后计算联合注意力：

$$Our\_Attn = softmax\left(\frac{Q_1 \cdot (K_1 \oplus K_2)^T}{\sqrt{d}}\right) \cdot (V_1 \oplus V_2)$$

这一设计的优势在于：
- **层次化引导**：外观信息在UNet的每个尺度上注入，从全局结构到局部纹理逐层传递，而非仅在某一层进行粗糙拼接。
- **不依赖文本提示**：外观控制模型独立提供身份引导，无需文本描述的辅助，避免了文本条件对外观信号的干扰。
- **可训练性**：通过专门的外观控制预训练，模型学习到稳定的外观提取与传递能力，解决了零样本方法的不稳定性。

**证据强度**：消融实验（Table 3）显示，移除外观控制预训练（App-Pretrain）后，Face-Cos从0.426骤降至0.038（降幅944.73%），SSIM从0.752降至0.291（降幅149.82%），证明该模块是身份保持的**必要条件**。

### Changed Slot 2：从联合训练到外观-姿态解耦的两阶段训练

**Baseline做法**：直接联合训练外观控制模块与姿态ControlNet，导致姿态控制网络在学习过程中依赖外观信息，造成身份混淆——模型无法区分“外观来自参考图像”和“外观来自姿态条件”，生成结果的身份一致性受损。

**MagicPose方案**：提出**两阶段训练策略**实现外观与姿态的解耦：

- **第一阶段：外观控制预训练（Appearance Control Pretraining）**。仅训练外观控制模型 $A_{\theta}$ 及其Multi-Source Attention Module，SD-UNet完全冻结。训练目标为：

  $$\mathcal{L} = \mathbb{E}_{\mathcal{E}(I), A_{\theta}(I_R), \epsilon \sim \mathcal{N}(0,1), t} \left[ \| \epsilon - \epsilon_{\theta}(z_t, t, A_{\theta}(I_R)) \|_2^2 \right]$$

  此阶段确保外观控制模型学会从参考图像中提取并传递身份特征，而不受姿态条件的干扰。

- **第二阶段：外观解耦的姿态控制（Appearance-disentangled Pose Control）**。在第一阶段预训练权重的基础上，联合微调外观控制模型 $A_{\theta}$ 和Pose ControlNet $P_{\theta}$：

  $$\mathcal{L} = \mathbb{E}_{\mathcal{E}(I), A_{\theta}(I_R), P_{\theta}(I_C), \epsilon \sim \mathcal{N}(0,1), t} \left[ \| \epsilon - \epsilon_{\theta}(z_t, t, A_{\theta}(I_R), P_{\theta}(I_C)) \|_2^2 \right]$$

  由于外观控制模型已经具备稳定的身份传递能力，Pose ControlNet可以在不干扰外观的前提下独立学习姿态到图像的映射。

**证据强度**：消融实验（Table 3）显示，移除外观解耦的姿态控制（Disentangle）后，Face-Cos从0.426降至0.397（降幅7.30%），SSIM从0.752降至0.727（降幅3.43%），验证了解耦训练对避免外观干扰的贡献。虽然降幅小于外观控制预训练，但考虑到该阶段是在已具备强身份保持能力基础上的进一步优化，其效果仍然显著。

### 辅助创新：数据增强与图像引导

除上述两个核心changed slots外，MagicPose还引入了两项辅助设计：

- **随机掩码数据增强**：在训练中随机掩码面部关键点和手部姿态，迫使模型学习从部分姿态信息中推断完整外观，增强了对OpenPose检测不完整情况的鲁棒性。消融实验显示该增强带来Face-Cos +2.20%、SSIM +0.13%的提升（Table 3）。
- **图像级无分类器引导（Image-CFG）**：将无分类器引导的概念从文本域拓展到图像域，在推理时通过调节外观控制信号的强度来平衡身份保持与生成多样性。移除Image-CFG后Face-Cos下降56.62%（Table 3），证明其对生成质量的重要作用。

### 创新总结

MagicPose的创新本质在于**将身份保持从扩散模型的隐式期望提升为显式的可训练目标**。通过将自注意力层重新定位为外观变形模块，并配合外观控制模型的预训练与姿态解耦策略，MagicPose在不修改SD-UNet预训练权重的前提下，以插件形式实现了鲁棒的身份感知姿态重定向。这一设计范式使得模型在仅使用TikTok数据集335个视频训练的情况下，取得了Face-Cos 0.426的领先性能（相较DisCo提升156%），并展现出对全身数据集和多样化图像风格的零样本泛化能力（Table 4, Figure 6-8）。

![[assets/figures/papers/paper_list_l6_MagicPose_Realistic_Human_Pose_and_Facial_Expression_Retargeting_with_Id/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed MagicPose pipeline for controllable human poses and facial expressions retargeting with motions & facial expressions transfer. The Appearance Control Model is a copy of the entire Stable-Diffusion UNet, initialized with the same weight. The Stable-Diffusion UNet is frozen throughout the training. During a) Appearance Control Pretraining, we train the appearance control model and its Multi-Source Self-Attention Module. During b) Appearance-disentangled Pose Control, we jointly fine-tune the Appearance Control Model, initialized with weights from a), and the Pose ControlNet. After these steps, an optional motion module can be integrated into the pipeline and fine-tune...*

MagicPose 将“给定参考人物图像，将其重定向至目标姿态与表情”这一任务分解为两个正交子问题：**外观保持与迁移**，以及**姿态与表情控制**。这种分解使得两个目标可以分别由独立模块负责，并通过两阶段训练策略实现解耦，避免了常规端到端联合训练中外观控制与姿态控制高度耦合导致的身份混淆。

### 全局 Pipeline

MagicPose 以 Stable Diffusion (SD) 作为冻结的骨干生成网络，在其上外挂两个核心可训练模块，构成一个即插即用的扩展架构：

1. **Appearance Control Model（外观控制模型）**：SD-UNet 的完整可训练副本，接收参考图像 $I_R$，逐层提取外观信息的键值对（Key-Value pairs），为生成过程提供层次化的身份与外观引导。该模型不依赖文本提示，仅通过自注意力机制传递外观。

2. **Pose ControlNet（姿态控制网络）**：基于 ControlNet 架构，接收由 OpenPose 提取的目标姿态骨架和面部关键点作为条件输入 $I_C$，控制生成图像的人体姿态与面部表情。

3. **Multi-Source Self-Attention Module（多源自注意力模块）**：将 Appearance Control Model 各层提取的键值对 $(K_2, V_2)$ 与 SD-UNet 对应层的键值对 $(K_1, V_1)$ 进行拼接，形成新的键值对用于自注意力计算。其核心操作为：

$$Our\_Attn = softmax\left(\frac{Q_1 \cdot (K_1 \oplus K_2)^T}{\sqrt{d}}\right) \cdot (V_1 \oplus V_2)$$

这一设计使得生成过程能够同时关注当前去噪特征和参考图像的外观信息，实现跨姿态的外观传递。

4. **Optional Motion Module（可选运动模块）**：基于 AnimateDiff 微调的时序模块，用于改善连续帧输出的平滑性和一致性，在需要视频生成时集成到 Pipeline 中。

### 输入输出流

- **输入**：一张参考人物图像 $I_R$（提供身份与外观），以及目标姿态条件 $I_C$（OpenPose 骨架 + 面部关键点）。
- **处理流程**：
  - 参考图像 $I_R$ 送入 Appearance Control Model，逐层提取外观键值对；
  - 目标姿态条件 $I_C$ 送入 Pose ControlNet，生成姿态控制信号；
  - SD-UNet 在去噪过程中，通过 Multi-Source Self-Attention Module 融合外观键值对，同时接收 Pose ControlNet 的姿态条件，逐步生成目标潜变量；
  - 潜变量经 VAE Decoder 解码为最终输出图像。
- **输出**：与参考图像保持身份一致、且姿态/表情与目标条件对齐的生成图像。

### 两阶段训练策略

MagicPose 的核心创新在于其训练策略，通过分阶段训练实现外观与姿态的解耦：

- **第一阶段：Appearance Control Pretraining（外观控制预训练）**。仅训练 Appearance Control Model 及其 Multi-Source Self-Attention Module，SD-UNet 完全冻结。训练目标为：

$$\mathcal{L} = \mathbb{E}_{\mathcal{E}(I), A_{\theta}(I_R), \epsilon \sim \mathcal{N}(0,1), t} \left[ \| \epsilon - \epsilon_{\theta}(z_t, t, A_{\theta}(I_R)) \|_2^2 \right]$$

此阶段使外观控制模型学会从参考图像中提取并传递身份相关信息，而不受姿态条件的干扰。

- **第二阶段：Appearance-disentangled Pose Control（外观分离的姿态控制）**。在第一阶段预训练权重的基础上，联合微调 Appearance Control Model 和 Pose ControlNet：

$$\mathcal{L} = \mathbb{E}_{\mathcal{E}(I), A_{\theta}(I_R), P_{\theta}(I_C), \epsilon \sim \mathcal{N}(0,1), t} \left[ \| \epsilon - \epsilon_{\theta}(z_t, t, A_{\theta}(I_R), P_{\theta}(I_C)) \|_2^2 \right]$$

由于外观控制模型已经过预训练，Pose ControlNet 可以在不干扰外观表征的前提下独立学习姿态控制，从而实现外观与姿态的有效解耦。消融实验（Table 3）定量验证了这一策略的有效性：移除外观控制预训练后，Face-Cos 从 0.426 骤降至 0.038（-944.73%），SSIM 从 0.752 降至 0.291（-149.82%）；移除外观解耦的姿态控制后，Face-Cos 下降 7.30% 至 0.397，SSIM 下降 3.43% 至 0.727。

整个框架的模块关系与数据流可参照 **Figure 2** 的 Pipeline 总览图。

### 问题分解与整体架构

MagicPose将人物姿态重定向任务分解为两个子问题：**外观传递**（保持参考图像的身份、肤色、衣着等视觉特征）与**姿态/表情控制**（根据目标姿态骨架和面部关键点生成对应动作）。整体架构包含三个核心模块：冻结的Stable Diffusion UNet（SD-UNet）作为生成骨干、可训练的**Appearance Control Model**负责外观引导、以及**Pose ControlNet**负责姿态条件控制（Figure 2）。

扩散模型的标准训练目标基于潜空间去噪，MagicPose沿用这一范式。SD-UNet的训练损失定义为：

$$\mathcal { L } = \mathbb { E } _ { \mathcal { E } ( I ) , c _ { \mathrm { t e x t } } , \epsilon \sim \mathcal { N } ( 0 , 1 ) , t } \left[ \Vert \epsilon - \epsilon _ { \theta } ( z _ { t } , t , c _ { \mathrm { t e x t } } ) \Vert _ { 2 } ^ { 2 } \right]$$

其中 $\mathcal{E}(I)$ 为图像 $I$ 的VAE编码，$c_{\mathrm{text}}$ 为文本条件，$\epsilon$ 为采样的高斯噪声，$z_t$ 为第 $t$ 步的噪声潜变量，$\epsilon_{\theta}$ 为UNet预测的噪声。MagicPose在此基础上，将文本条件替换为外观控制信号与姿态控制信号的组合，实现身份感知的生成。

### Appearance Control Model与多源自注意力

外观控制的核心机制基于一个关键洞察：**扩散UNet的自注意力层天然具备外观变形能力**——将参考图像的特征以键值对形式注入生成过程，即可实现外观的跨姿态传递。零样本情况下直接拼接自注意力层的键值对虽能产生外观相似性，但生成不稳定（Figure 3）。MagicPose通过设计可训练的Appearance Control Model来解决这一问题。

Appearance Control Model是SD-UNet的完整副本，初始权重相同，但在训练中可更新。它接收参考图像 $I_R$ 并提取层次化的外观特征，通过**Multi-Source Self-Attention Module**将键值对注入SD-UNet的对应Transformer Block。

标准自注意力的计算为：

$$Self\_Attn = softmax(\frac{Q \cdot K^T}{\sqrt{d}}) \cdot V$$

其中 $Q$、$K$、$V$ 分别为查询、键、值矩阵，$d$ 为缩放因子。MagicPose将其改造为多源自注意力：

$$Our\_Attn = softmax(\frac{Q_1 \cdot (K_1 \oplus K_2)^T}{\sqrt{d}}) \cdot (V_1 \oplus V_2)$$

此处 $Q_1$ 来自SD-UNet的查询，$K_1$、$V_1$ 来自SD-UNet自身的键值对，$K_2$、$V_2$ 来自Appearance Control Model对应层的键值对，$\oplus$ 表示拼接操作。通过这种方式，生成过程同时关注自身特征和参考图像的外观信息，实现层次化的外观引导，且不依赖文本提示。

### 两阶段训练策略

外观与姿态的高度耦合是导致身份丢失的根本原因。MagicPose通过两阶段训练实现解耦：

**第一阶段：外观控制预训练（Appearance Control Pretraining）**。此阶段仅训练Appearance Control Model及其多源自注意力模块，SD-UNet完全冻结。训练目标为：

$$\mathcal{L} = \mathbb{E}_{\mathcal{E}(I), A_{\theta}(I_R), \epsilon \sim \mathcal{N}(0,1), t} \left[ \| \epsilon - \epsilon_{\theta}(z_t, t, A_{\theta}(I_R)) \|_2^2 \right]$$

其中 $A_{\theta}(I_R)$ 表示Appearance Control Model从参考图像提取的外观控制信号。SD-UNet $\epsilon_{\theta}$ 的参数在此阶段冻结，仅优化 $A_{\theta}$。这迫使外观控制模型学会提供鲁棒的外观引导，而不干扰预训练的生成先验。

**第二阶段：外观解耦的姿态控制（Appearance-disentangled Pose Control）**。在第一阶段预训练权重的基础上，联合微调Appearance Control Model与Pose ControlNet。Pose ControlNet接收姿态条件 $I_C$（包含OpenPose骨架和面部关键点），训练目标扩展为：

$$\mathcal{L} = \mathbb{E}_{\mathcal{E}(I), A_{\theta}(I_R), P_{\theta}(I_C), \epsilon \sim \mathcal{N}(0,1), t} \left[ \| \epsilon - \epsilon_{\theta}(z_t, t, A_{\theta}(I_R), P_{\theta}(I_C)) \|_2^2 \right]$$

其中 $P_{\theta}(I_C)$ 为Pose ControlNet从姿态条件提取的控制信号。关键设计在于：由于第一阶段已建立稳定的外观控制通路，第二阶段Pose ControlNet可以在不干扰外观传递的前提下独立学习姿态映射，从根本上避免了外观与姿态的耦合。

消融实验（Table 3）验证了该策略的有效性：移除外观控制预训练后，Face-Cos从0.426骤降至0.038（-944.73%），SSIM从0.752降至0.291（-149.82%）；移除外观解耦的姿态控制后，Face-Cos下降7.30%至0.397，SSIM下降3.43%至0.727。这证实了两阶段训练对身份保持和生成质量的决定性作用。

## 实验与关键发现

### 核心瓶颈与因果机制

MagicPose旨在解决扩散模型在人体姿态重定向中的根本矛盾：**外观保持与姿态控制的耦合问题**。常规方法（如直接使用ControlNet或零样本自注意力连接）无法稳定传递参考图像的外观信息，导致身份丢失或需要针对新域微调。MagicPose的因果调节变量在于引入一个**可训练的外观控制模型**（Appearance Control Model），作为SD-UNet的副本，通过Multi-Source自注意力模块拼接参考图像的键值对，配合**两阶段训练策略**（先外观控制预训练冻结骨干，后联合微调解耦姿态控制），实现外观保持与姿态控制的分离。

### 主实验结果

在TikTok数据集上，MagicPose在所有评估指标上均超越现有方法，尤其在身份保持方面取得突破性进展。

**Table 1** 展示了MagicPose与近期SOTA方法DreamPose、DisCo的定量对比。MagicPose取得FID 25.50（DisCo为50.68，降低49.7%）、SSIM 0.752（DisCo为0.648）、PSNR 29.53、LPIPS 0.292、L1误差0.81E-04。最关键的**Face-Cos**指标达到0.426，相较DisCo的0.166提升**+0.260（+156%）**，证明MagicPose在保持面部身份信息方面具有显著优势。

![[assets/figures/papers/paper_list_l6_MagicPose_Realistic_Human_Pose_and_Facial_Expression_Retargeting_with_Id/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparisons of MagicPose with the recent SOTA methods DreamPose (Karras et al., 2023) and Disco (Wang et al., 2023). ↓ indicates that the lower the better, and vice versa. Methods with ∗ directly use the target image as the input, including more information compared to the OpenPose (Cao et al., 2019; Simon et al., 2017; Cao et al., 2017; Wei et al., 2016). † represents that Disco (Wang et al., 2023) is pre-trained on other datasets (Fu et al., 2022; Ge et al., 2019; Schuhmann et al., 2021; Lin et al., 2014) more than our proposed MagicPose, which uses only 335 video sequences in the TikTok (Jafarian & Park, 2021) dataset for pretraning and fine-tuning. Face-Cos represents the c...*

值得注意的是，基线方法FOMM、MRAA、TPS在实验中使用了目标图像作为输入（标记*），包含比OpenPose更多的外观信息，而MagicPose仅依赖姿态骨架和面部关键点，仍取得全面领先。此外，DisCo在预训练阶段使用了额外的公开数据集（如LAION），而MagicPose仅使用TikTok的335个视频进行预训练和微调，在更少数据下获得更优性能。

**定性对比**（Figure 4）显示，TPS、MRAA、DisCo等方法在面部表情一致性和人体姿态身份保持方面存在明显不足，而MagicPose能够准确保持参考图像的身份外观，同时精确跟随目标姿态。

### 用户研究

**Table 2** 和 **Table 5** 展示了100名参与者的用户研究结果。参与者对测试集中8个视频对象进行投票，MagicPose获得了**73%的票数**，被选为身份保持最优的方法，统计显著性p-value = 1.11e-12。在所有8个测试对象上，MagicPose均保持最佳的身份信息保持能力。

### 消融实验

**Table 3** 和 **Figure 5** 系统验证了各模块的贡献：

![[assets/figures/papers/paper_list_l6_MagicPose_Realistic_Human_Pose_and_Facial_Expression_Retargeting_with_Id/figures/009_Table_3.jpg]]
*Table 3: Ablation Analysis of MagicPose with different training and inference settings. App-Pretrain stands for Appearance Control Pretraining through Multi-Source Attention Module and Disentangle denotes Appearance-disentangled Pose Control. Image-CFG denotes classifier free guidance. Data Aug indicates the model is trained with data augmentation of random masking of facial landmarks and hand poses*

1. **外观控制预训练（Appearance Control Pretraining）**：移除该模块后，Face-Cos从0.426骤降至0.038（**-944.73%**），SSIM从0.752降至0.291（**-149.82%**）。这是最关键的消融发现，证明外观控制预训练对身份保持具有决定性作用。该阶段通过Multi-Source Attention Module将参考图像特征以键值对形式注入生成过程，使扩散UNet的自注意力层作为外观变形模块发挥作用。

2. **外观解耦的姿态控制（Appearance-disentangled Pose Control）**：移除解耦策略后，Face-Cos下降7.30%至0.397，SSIM下降3.43%至0.727。这表明直接联合训练外观控制模块与姿态ControlNet会导致姿态控制依赖于外观信息，造成身份混淆。两阶段训练策略有效分离了两个子任务。

3. **无分类器图像引导（Image-CFG）**：移除后Face-Cos下降56.62%至0.272，SSIM下降14.11%至0.659，验证了图像引导对提升生成质量的重要作用。

4. **数据增强（Data Aug）**：加入随机掩码面部标志和手部姿态的数据增强带来Face-Cos +2.20%（0.417→0.426）、SSIM +0.13%的提升，增强了模型对不完整姿态检测的鲁棒性。

### 泛化能力

MagicPose展现出优异的零样本域外泛化能力。**Table 4** 显示，在全身数据集Everybody Dance Now上，直接评估（MagicPose†）取得平均FID 28.64、PSNR 29.63；进一步微调后（MagicPose‡）性能持续提升。

![[assets/figures/papers/paper_list_l6_MagicPose_Realistic_Human_Pose_and_Facial_Expression_Retargeting_with_Id/figures/010_Table_4.jpg]]
*Table 4: Quantitative evaluation of generalization ability of MagicPose. MagicPose† denotes the pipeline is directly evaluated on test set of Everybody Dance Now (Chan et al., 2019b) after being trained on TikTok (Jafarian & Park, 2021), and MagicPose‡ represents the pipeline is further fine-tuned on Everybody Dance Now (Chan et al., 2019b) train set and evaluated on test set*

**Figure 6-8** 的定性结果表明，MagicPose无需任何微调即可对风格迥异的参考图像（包括不同种族、年龄的真实人物，以及卡通、动画角色）实现身份一致性与姿态一致性的重定向。Figure 9进一步展示了模型对训练集（TikTok）中未见的图像风格的泛化能力。

![[assets/figures/papers/paper_list_l6_MagicPose_Realistic_Human_Pose_and_Facial_Expression_Retargeting_with_Id/figures/007_Figure_6.jpg]]
*Figure 6: Comparison of zero-shot pose and facial expression retargeting on out-of-domain image. Figure 7. Visualization of zero-shot pose and facial expression retargeting on in-the-wild real-human with different ethnicity and age from training data (Tiktok)*

### 失败模式与局限性

1. **姿态检测依赖**：MagicPose依赖OpenPose进行姿态估计，当人体快速运动、遮挡或部分可见时，姿态骨骼和面部关键点检测可能不完整，导致生成图像出现伪影。

2. **时序一致性**：尽管集成了可选的AnimateDiff运动模块，复杂舞蹈动作的连续帧生成中时序一致性仍未完全解决，需要特定的DDIM采样策略辅助。

3. **场景限制**：当前模型主要针对单人场景设计，未验证对多人交互或复杂背景下的身份保持能力，且训练数据偏向年轻女性，其他人群的泛化性能未经充分评估。

### 关键公式

MagicPose的核心创新体现在Multi-Source Self-Attention的键值对拼接机制：

$$Our\_Attn = softmax(\frac{Q_1 \cdot (K_1 \oplus K_2)^T}{\sqrt{d}}) \cdot (V_1 \oplus V_2)$$

其中$K_1, V_1$来自SD-UNet，$K_2, V_2$来自Appearance Control Model，通过拼接实现外观信息的层次化注入。两阶段训练分别优化：

$$\mathcal{L}_{pretrain} = \mathbb{E}_{\mathcal{E}(I), A_{\theta}(I_R), \epsilon \sim \mathcal{N}(0,1), t} \left[ \| \epsilon - \epsilon_{\theta}(z_t, t, A_{\theta}(I_R)) \|_2^2 \right]$$

$$\mathcal{L}_{joint} = \mathbb{E}_{\mathcal{E}(I), A_{\theta}(I_R), P_{\theta}(I_C), \epsilon \sim \mathcal{N}(0,1), t} \left[ \| \epsilon - \epsilon_{\theta}(z_t, t, A_{\theta}(I_R), P_{\theta}(I_C)) \|_2^2 \right]$$

第一阶段仅优化外观控制模型$A_{\theta}$，SD-UNet冻结；第二阶段联合优化外观控制器$A_{\theta}$和姿态控制网络$P_{\theta}$，实现外观与姿态的解耦。

![[assets/figures/papers/paper_list_l6_MagicPose_Realistic_Human_Pose_and_Facial_Expression_Retargeting_with_Id/figures/016_Figure_12.jpg]]
*Figure 12: Visualization of Human Motion and Facial Expression Transfer on TikTok (Jafarian & Park, 2021)*

## 定位与知识库关联

### 核心瓶颈与设计动机

MagicPose 旨在解决扩散模型在人体姿态重定向任务中的一个根本性瓶颈：**外观保持与姿态控制的高度耦合**。现有方法的困境在于，当模型试图通过姿态条件（如 OpenPose 骨架）控制生成结果时，参考图像的身份外观信息极易在扩散去噪过程中被稀释或扭曲。具体表现为两类失败模式：

1. **零样本自注意力连接的不稳定性**：直接在前馈过程中将参考图像的自注意力键值对注入生成 UNet（类似视频编辑中的跨帧注意力机制）虽然能带来弱的外观相似性，但生成结果不可控，容易出现伪影和身份漂移（见 Figure 3 的定性对比）。
2. **直接微调 ControlNet 的身份混淆**：如果在一个阶段中同时训练外观控制模块和姿态 ControlNet，姿态控制网络会学会依赖外观信息来辅助生成，导致在推理时参考图像的外观与目标姿态之间产生非预期的纠缠——即“身份混淆”。

MagicPose 的核心洞察在于：**扩散 UNet 的自注意力层本质上是一个可学习的外观变形模块**。将参考图像的特征以键值对形式注入生成过程，即可实现外观的跨姿态传递。基于这一洞察，方法设计的因果旋钮是：用一个专门训练的、作为 SD-UNet 副本的**外观控制模型（Appearance Control Model）**取代零样本注意力连接，并配合**两阶段训练策略**实现外观与姿态的解耦。

### 与现有方法的关系与定位

#### 基于 GAN 的肖像动画方法

**FOMM**、**MRAA** 和 **TPS** 代表了基于运动估计和图像变形的传统路线。这些方法直接使用目标图像作为输入（在 Table 1 中以 ∗ 标记），包含比 OpenPose 骨架更丰富的纹理和形状先验。然而，它们在人脸表情一致性和大幅姿态变化下的身份保持方面表现不足（见 Figure 4），且泛化到域外图像风格的能力有限。MagicPose 仅依赖姿态骨架和面部关键点作为条件，在输入信息更少的情况下取得了全面领先的定量指标，验证了扩散先验在重定向任务中的优势。

#### 基于扩散的重定向方法

- **DreamPose** 将扩散模型应用于时尚视频生成，但其外观控制机制相对简单，在身份保持指标（Face-Cos）上明显落后于 MagicPose。
- **DisCo** 是最具竞争力的基线，使用 CLIP 图像编码器提取参考图像的外观嵌入，并通过交叉注意力注入生成过程。然而，CLIP 嵌入是对图像的全局语义压缩，丢失了细粒度的纹理和身份信息。DisCo 在 TikTok 数据集上的 Face-Cos 仅为 0.166，而 MagicPose 达到 0.426（+156%），这一差距直接反映了**层次化自注意力注入**相较于**全局语义嵌入**在外观保持上的结构性优势。此外，DisCo 在预训练阶段使用了额外的公开数据集（如 LAION），而 MagicPose 仅使用 TikTok 的 335 个视频序列完成全部训练，在更少数据下获得更优性能，说明其训练策略具有更高的数据效率。

#### 与通用可控生成框架的关系

MagicPose 的外观控制模型在架构上是 SD-UNet 的可训练副本，通过 Multi-Source Self-Attention 模块实现层级化的键值对注入。这一设计使其天然成为 Stable Diffusion 的**即插即用插件**——无需修改预训练权重即可集成。相较于 ControlNet 仅提供空间条件控制（如边缘图、深度图），MagicPose 的外观控制分支专门解决“谁”的问题，而 Pose ControlNet 负责“怎么动”的问题，两者在功能上互补且可独立训练。

### 关键设计的消融证据

两阶段训练策略的有效性在 Table 3 的消融实验中得到了量化验证：

1. **外观控制预训练（Appearance Control Pretraining）** 是最关键的设计。移除该阶段后，Face-Cos 从 0.426 骤降至 0.038（降幅 944.73%），SSIM 从 0.752 降至 0.291（降幅 149.82%）。这表明，如果没有专门的外观控制预训练，模型几乎完全丧失了身份保持能力，退化为普通的姿态条件生成。
2. **外观解耦的姿态控制（Appearance-disentangled Pose Control）** 在预训练基础上进一步提升了身份保持：Face-Cos 从 0.397 提升至 0.426（+7.30%），SSIM 从 0.727 提升至 0.752（+3.43%）。这一提升虽不如第一阶段显著，但验证了联合微调时若不刻意解耦，姿态控制网络确实会干扰外观信息的传递。
3. **Classifier-free 图像引导（Image-CFG）** 对生成质量有重要贡献：移除后 Face-Cos 下降 56.62% 至 0.272，SSIM 下降 14.11% 至 0.659。
4. **数据增强（随机掩码面部标志和手部姿态）** 带来边际但稳健的提升（Face-Cos +2.20%，SSIM +0.13%），增强了模型对不完整姿态检测的鲁棒性。

### 适用边界与局限性

尽管 MagicPose 在域内和零样本泛化实验中表现突出，其适用边界受以下因素制约：

1. **姿态检测器依赖**：当前流程依赖 OpenPose 提取姿态骨架和面部关键点。在人体快速运动、严重遮挡或部分可见的场景下，姿态检测可能不完整或错误，导致生成图像出现伪影。这是整个管线的前置瓶颈，而非扩散模型本身的问题——替换为更鲁棒的姿态检测器（如 DensePose 或自监督关键点提取）有望缓解。
2. **单人场景假设**：模型设计和训练均针对单人场景，未验证多人交互下的独立身份控制能力。在多人场景中，Multi-Source Attention 如何区分不同个体的外观特征并避免身份混淆，是一个尚未探索的问题。
3. **训练数据偏差**：TikTok 数据集以年轻女性舞蹈视频为主，其他人群（不同年龄、性别、体型）的泛化性能虽在 Figure 7 的定性结果中有所展示，但缺乏大规模定量评估。
4. **时序一致性**：尽管集成了可选的 AnimateDiff 运动模块，复杂舞蹈动作的连续帧生成仍需特定的 DDIM 采样策略辅助，时序闪烁问题未完全解决。
5. **推理成本**：作为扩散模型，单帧推理的计算开销限制了实时应用场景的部署。

### 开放问题与未来方向

基于 MagicPose 的设计范式和当前局限，以下方向值得进一步探索：

- **姿态检测器的升级**：用更鲁棒或更密集的姿态表征（如 DensePose、自监督关键点）替代 OpenPose，能否在极端姿态和遮挡下维持甚至提升生成质量？
- **外观控制机制的跨任务迁移**：Multi-Source Attention Module 的层级化键值对注入机制本质上是一种通用的外观保持范式。它能否拓展到其他几何控制任务，如新视角合成（以相机姿态为条件）、自然场景形状编辑（以深度图或分割图为条件）或动物运动重定向？
- **多人场景的身份解耦**：如何在多人场景中为不同角色分配独立的外观控制分支，并维持交互一致性（如遮挡关系、接触区域），是一个具有挑战性但应用价值显著的问题。
- **轻量化与实时推理**：能否通过知识蒸馏、步数压缩或一致性模型蒸馏等手段，将 MagicPose 的推理成本降低到实时应用可接受的水平？

## 原文 PDF

![[paperPDFs/ICML_2024/MagicPose_Realistic_Human_Pose_and_Facial_Expression_Retargeting_with_Identity_aware_Diffusion.pdf]]
