---
title: "Unifying Perception and Action: A Hybrid-Modality Pipeline with Implicit Visual Chain-of-Thought for Robotic Action Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Unifying_Perception_and_Action_A_Hybrid_Modality_Pipeline_with_Implicit_Visual_Chain_of_Thought_for_Robotic_Action_Generation.pdf
project_link: "https://vita-cvpr26.github.io/"
code_link: null
aliases:
- VVITA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过构建跨模态共享离散潜在空间，使统一标记同时解码为未来帧和动作，并将未来帧预测作为动作生成的归纳偏置，从而统一前向与逆向动力学。
primary_logic: 隐式视觉思维链：自回归生成的共享标记序列经过双解码器并行输出未来帧预测和机器人动作，将视觉动态内部化为运动规划的引导，无需显式轨迹模拟。
claims:
- VITA 在 CALVIN ABC‑D 上平均完成 4.73 个连续指令，相对于最强基线 DeFI（4.51）提升 4.9%，相对 UP‑VLA 提升 14.5%。
- 在 LIBERO‑Long 上，VITA 成功率达到 96.8%，较 CoT‑VLA 提升 36.2%，显著增强了长时域任务建模能力。
- 消融研究表明，仅保留隐式视觉思维链（Internal CoT）即大幅优于纯文本思维链变体，完整 VITA（Internal + Textual CoT）在 LIBERO 平均成功率 96.7%。
- 真实世界 6 项任务平均成功率达 80.5%，在 OOD 任务上性能下降远小于所有基线，展现出优异的泛化能力。
---

# Unifying Perception and Action: A Hybrid-Modality Pipeline with Implicit Visual Chain-of-Thought for Robotic Action Generation

> [!tip] 核心洞察
> 隐式视觉思维链：自回归生成的共享标记序列经过双解码器并行输出未来帧预测和机器人动作，将视觉动态内部化为运动规划的引导，无需显式轨迹模拟。

| 字段 | 内容 |
|------|------|
| 中文题名 | 统一感知与动作：一种具备隐式视觉思维链的混合模态机器人动作生成方法 |
| 英文题名 | Unifying Perception and Action: A Hybrid-Modality Pipeline with Implicit Visual Chain-of-Thought for Robotic Action Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.19859) · [Project](https://vita-cvpr26.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VITA (Vision-Integrated Trajectory Alignment) |
| Dataset | CALVIN ABC-D, LIBERO, LIBERO-Long, SimplerEnv Google Robot |

> [!tip] 效果简介
> - CALVIN ABC-D 上，平均完成指令数 (Avg. Len) 4.73 vs 4.51 (DeFI) (+4.9%)。
> - LIBERO (全部套件平均) 上，成功率 (%) 96.7 vs 95.5 (UniVLA) (+1.3%)。
> - LIBERO-Long 上，成功率 (%) 96.8 vs 94.0 (UniVLA) (+3.0%)。

## 概述

机器人视觉-语言-动作（VLA）模型在从像素直接生成精确动作时面临一个根本性瓶颈：高维视觉观测与低维动作之间存在巨大的**模态差距**。现有方法要么将视觉预测作为独立代理任务，与动作生成目标相互竞争导致训练不稳定；要么在推理阶段采用“先预测未来帧、再生成动作”的显式思维链，未能将视觉动态真正内化为运动规划的归纳偏置。

针对这一问题，本文提出 **VITA（Vision-Integrated Trajectory Alignment）**，一种统一感知与动作的混合模态框架。其核心洞察是**隐式视觉思维链**：通过构建跨模态共享的离散潜在空间，使统一标记序列同时解码为未来帧预测和机器人动作轨迹，将前向动力学（视觉预测）与逆向动力学（动作生成）统一在同一优化目标下。

VITA 在三个关键维度上实现了突破：

- **表示层面对齐**：视觉编码与动作编码共享同一个矢量量化码本（大小 8192），使两种模态的 token 可以在 VLM 主干中无缝共享，从根本上缩小模态差距。
- **优化目标统一**：自回归生成的跨模态 token 经双解码器（视觉解码器与动作解码器）并行输出，未来帧预测不再是与动作竞争的外部任务，而是作为内部归纳偏置直接参与动作优化。
- **三阶段渐近训练**：预热阶段独立训练视觉/动作自编码器与共享码本，共训阶段联合学习 VLM 主干与双解码器，微调阶段仅更新动作解码器，确保训练稳定收敛。

实验结果表明，VITA 在多个基准上达到最优性能：在 CALVIN ABC‑D 上平均完成 4.73 个连续指令，较最强基线 DeFI（4.51）提升 4.9%；在 LIBERO‑Long 上成功率达 96.8%，较 CoT‑VLA 提升 36.2%；在真实世界 6 项任务中平均成功率达 80.5%，且在分布外（OOD）任务上性能下降远小于所有基线。消融研究进一步证实，仅保留隐式视觉思维链（Internal CoT）即大幅优于纯文本思维链变体，验证了视觉动态内化作为运动规划引导的有效性。

## 背景与动机

### 从感知到行动的鸿沟

机器人操作的核心挑战在于将高维视觉感知转化为精确的低维动作控制。近年来，视觉-语言-动作（VLA）模型通过将大规模预训练的视觉-语言模型（VLM）适配到机器人领域，显著提升了策略的泛化能力。然而，现有 VLA 方法面临两个根本性瓶颈：

**模态差距**：视觉观测（高维像素空间）与动作指令（低维关节空间或末端位姿）之间存在显著的表示鸿沟。直接从像素回归精确动作轨迹，要求模型隐式地学习前向动力学（从当前状态预测未来状态）和逆向动力学（从目标状态反推所需动作），这一过程缺乏明确的归纳偏置，导致学习效率低下且精度受限。

**训练目标冲突**：部分工作尝试引入视觉预测作为辅助任务来缓解上述问题，但视觉重建与动作生成的优化目标往往相互竞争——前者追求像素级保真度，后者追求运动控制精度——造成训练不稳定，尤其在长时域任务中表现退化。

### 现有方法的局限

当前 VLA 模型大致可分为两类范式：

- **端到端动作生成**（如 **OpenVLA**、**Pi0**、**Octo**）：直接将视觉-语言嵌入映射为动作，忽略了未来状态预测所提供的丰富动力学信息，在需要长期规划的复杂任务中表现受限。
- **显式视觉思维链**（如 **CoT-VLA**、**DeFI**）：采用“预测-再行动”的策略，先生成未来帧图像，再基于预测图像规划动作。这种两阶段范式将视觉预测与动作生成解耦，虽能提供一定的动力学引导，但推理成本高昂，且预测误差会向动作规划阶段累积传播。

此外，现有方法通常在独立的特征空间中处理视觉和动作模态，缺乏跨模态的表示对齐机制，限制了从大规模人类视频和机器人操作数据中迁移运动知识的能力。

### 本文动机

针对上述瓶颈，本文提出 **VITA（Vision-Integrated Trajectory Alignment）** 框架，核心动机在于：

1. **统一感知与动作的表示空间**：构建跨模态共享的离散潜在空间，使视觉观测和动作轨迹映射到同一码本中，从表示层面消除模态差距。
2. **隐式视觉思维链**：将未来帧预测作为动作生成的归纳偏置，而非独立的推理阶段。自回归生成的统一 token 序列同时解码为未来帧和动作轨迹，视觉动态内部化为运动规划的隐式引导，避免显式“预测-再行动”的误差累积和计算开销。
3. **渐进式训练策略**：通过预热、共训、微调三阶段训练，逐步建立跨模态对齐，缓解多目标优化的冲突，提升训练稳定性。

通过上述设计，VITA 旨在实现感知与动作的深度融合，使机器人策略能够从大规模异构数据中高效学习可泛化的运动知识，在仿真和真实场景中均展现出优异的长时域任务建模能力和数据效率。

## 核心创新

VITA 的核心创新在于通过**跨模态共享离散潜在空间**将视觉感知与动作生成统一建模，并以**隐式视觉思维链**将未来帧预测内化为动作生成的归纳偏置，从而系统性地解决了当前 VLA 方法面临的两大瓶颈：高维视觉观测与低维动作之间的模态差距，以及视觉预测代理任务与动作生成任务优化目标相互竞争导致的训练不稳定问题。

### 跨模态表示统一：共享码本对齐视觉与动作

现有 VLA 方法（如 **GR-1**、**OpenVLA**、**Pi0**）通常将视觉和动作在独立特征空间中建模，缺乏显式的跨模态对齐机制，导致从像素直接生成精确动作时信息损失严重。VITA 的核心突破在于构建了一个大小为 8192 的共享离散码本（Shared Codebook），使视觉编码和动作编码映射到同一矢量量化空间：

$$
\mathcal{Q}(z) = c_k, \text{ where } k = \arg\min_j \|z - c_j\|_2
$$

具体而言，视觉分支通过冻结的 DINOv2 和 M‑Former 从连续帧中提取运动感知时空嵌入 $z_v = \text{M-Former}([f_t; f_{t+1}])$，动作分支则通过离散余弦变换（DCT）将动作序列压缩至频域后再由 MLP 编码为 $z_a$。两者经同一量化器映射到共享码本后，分别由视觉解码器和动作解码器重建。这一设计使得视觉动态与运动控制指令在表示层面实现根本对齐，为后续统一生成奠定了基础。

### 隐式视觉思维链：从“预测-再行动”到“预测即行动”

传统方法（如 **CoT-VLA**、**TraceVLA**）若引入视觉预测，通常采用显式“预测-再行动”范式——先完整生成未来图像，再据此规划动作，这不仅引入额外推理延迟，且视觉预测与动作生成之间缺乏梯度耦合。VITA 提出的**隐式视觉思维链（Internal CoT）**从根本上改变了这一范式：VLM 主干自回归生成的统一 token 序列同时路由到视觉解码器和动作解码器，未来帧预测作为归纳偏置直接参与动作优化，而无需显式中间输出。

这一机制的本质是将前向动力学（视觉预测）与逆向动力学（动作生成）统一在同一自回归过程中。共训练阶段的联合损失函数体现了这种双重一致性：

$$
\mathcal{L}_{co} = \lambda_v \|\mathbf{I}_{1:T} - \hat{\mathbf{I}}_{1:T}\|_1 + \lambda_a \|\mathbf{a}_{1:H} - \hat{\mathbf{a}}_{1:H}\|_2^2
$$

推理时，视觉解码器可被完全丢弃，仅保留动作解码器，从而在不增加推理开销的前提下获得视觉动力学提供的运动先验。

### 渐进式注意力：感知-计划-执行的信息定向流动

VITA 设计了**渐进式注意力机制**，明确划分 token 的信息流向：

$$
\mathrm{input} \to \mathrm{textual} \to \mathrm{cross-modality}
$$

输入 token（图像、指令、机器人状态）首先通过标准注意力交互；随后生成的文本思维链 token 将指令分解为符号化子任务（如 `[GRASP]`、`[MOVE]`、`[PLACE]` 等），实现任务规划的结构化表示；最后生成的跨模态 token 承载统一的感知-动作信息，供双解码器并行使用。这种设计实现了感知、规划与执行的解耦，使模型在长时域任务中保持清晰的推理链路。

### 三阶段渐近训练：稳定跨模态联合学习

直接端到端联合训练视觉和动作模块容易因优化目标竞争而导致训练不稳定。VITA 采用**三阶段渐近训练策略**：

1. **预热阶段**：视觉自编码器和动作自编码器独立训练，仅通过共享码本建立初步的跨模态对齐，各自最小化重建损失。
2. **共训练阶段**：VLM 主干与双解码器联合学习，同时利用纯视频数据（仅视觉预测）和同步视觉-动作配对数据（双目标联合优化），使模型逐步掌握从统一 token 同时解码未来帧和动作的能力。
3. **微调阶段**：仅更新动作解码器，使模型快速适配特定机器人平台和任务，同时保留已学到的视觉动力学知识。

消融实验（Table 7）证实，跳过预热阶段或仅进行共训练均导致性能显著下降，验证了渐近训练对共享码本收敛和跨模态对齐的关键作用。此外，VITA 展现出突出的数据效率：仅使用 10% 的微调数据即可超越 OpenVLA 在全数据集上的表现（Table 8a），表明共享离散空间带来的表示迁移能力显著降低了对大规模标注机器人数据的依赖。

## 整体框架

VITA（Vision-Integrated Trajectory Alignment）构建了一条**统一感知与动作的混合模态流水线**，其核心设计围绕一个关键洞察展开：将未来帧预测作为动作生成的归纳偏置，而非显式的“先预测再行动”中间产物。整个框架通过**跨模态共享离散潜在空间**将高维视觉观测与低维机器人动作对齐，消除了两者之间的模态鸿沟。

### 流水线总览

VITA 的端到端流程可概括为四个阶段，如 Figure 2 所示：

1. **跨模态对齐（①）**：视觉自编码器与动作自编码器分别将连续帧和动作轨迹编码为嵌入向量，经同一个矢量量化器（共享码本大小为 8192）映射为离散 token，使两种模态在统一潜在空间中对齐。
2. **VLM 主干生成（④）**：以 SigLIP 视觉编码器与 Gemma 语言模型为骨干，接收多模态上下文（当前帧、文本指令、机器人本体状态），通过渐进式注意力机制依次生成文本思维链 token 和跨模态统一 token。
3. **双解码输出（②③）**：统一 token 并行路由至视觉解码器（轻量 ViT）与动作解码器（Transformer + 逆离散余弦变换），同时输出未来帧预测和机器人动作轨迹。
4. **推理精简**：推理时仅保留动作解码器，视觉解码器可丢弃，单步推理延迟仅 60–71 ms，动作级吞吐接近 60 Hz（Table 9）。

### 模块关系与数据流

五个核心模块构成 VITA 的完整架构，其依赖关系如下：

| 模块 | 角色 | 训练阶段 | 推理保留 |
|------|------|----------|----------|
| **Visual Auto-encoder** | 冻结 DINOv2 + M‑Former 提取运动感知时空特征，经共享码本量化后重建未来帧 | 仅预热 | 否 |
| **Action Auto-encoder** | DCT 压缩动作序列至频域 → MLP 编码 → 共享码本量化 → 动作重建 | 仅预热 | 否 |
| **Shared Codebook** | 大小为 8192 的跨模态离散潜在空间，视觉与动作共享同一量化器 | 全阶段 | 是 |
| **VLM Backbone (SigLIP + Gemma)** | 渐进注意力生成文本子任务 token → 跨模态统一 token | 共训 + 微调 | 是 |
| **Visual Decoder / Action Decoder** | 从统一 token 并行解码未来帧（L1 损失）与动作轨迹（MSE 损失） | 共训 | 仅动作解码器 |

输入流：**当前帧 $I_0$ + 文本指令 $x$ + 机器人状态 $s$** → VLM 主干 → 文本思维链 token（符号子任务如 `[GRASP]`, `[MOVE]`, `[PLACE]`）→ 跨模态统一 token → 双解码器并行输出。

输出流：**未来帧序列 $\hat{I}_{1:T}$**（训练时参与损失，推理时丢弃）+ **动作轨迹 $\hat{a}_{1:H}$**（推理时唯一输出）。

### 关键设计：隐式视觉思维链

与显式视觉思维链方法（如 CoT-VLA 先生成图像再生成动作）不同，VITA 的**隐式视觉思维链**将视觉预测内化为动作优化的归纳偏置：自回归生成的统一 token 同时承载视觉动态与运动控制信息，视觉解码器提供的未来帧预测通过联合损失（式 20）反向约束动作生成，使模型隐式地学习前向动力学（视觉→未来状态）与逆向动力学（目标状态→动作）的统一表示。消融实验证实，仅保留隐式视觉思维链（Internal CoT）即可大幅优于纯文本思维链变体，完整 VITA 在 LIBERO 平均成功率达 96.7%（Table 6）。

### 三阶段渐近训练策略

VITA 采用渐近训练以避免多目标优化冲突（Algorithm 1）：

- **预热阶段**：独立训练视觉/动作自编码器与共享码本，仅使用重建损失，建立跨模态对齐基础。
- **共训阶段**：VLM 主干与双解码器联合学习，混合使用仅视频数据（视觉预测损失）和视频-动作配对数据（式 20 的双目标损失）。
- **微调阶段**：冻结视觉解码器，仅更新动作解码器，聚焦于下游任务的动作精度。

消融表明，跳过预热直接共训会导致性能显著下降，验证了共享码本预热的必要性（Table 7）。

### 补充图表

![[assets/figures/papers/paper_list_l2354_https_arxiv_org_abs_2511_19859/figures/001_Figure_1.jpg]]
*Figure 1: We propose VITA, a novel framework that unifies visual perception and action generation. A cross-modal shared codebook is established, where latent variables are decoded into videos or motion trajectories through forward and inverse dynamics processes respectively. This dual consistency at both the representation level and optimization objectives enables VITA to effectively learn motion knowledge from extensive human demonstrations and robot operation videos*

## 核心模块与公式推导

VITA 的核心架构围绕一个关键设计展开：**跨模态共享离散潜在空间**。该空间通过一个大小为 8192 的向量量化码本（Codebook）实现，使视觉感知嵌入与运动控制嵌入映射到同一离散表示域，从而在表示层面统一前向动力学（视觉预测）与逆向动力学（动作生成）。

### 3.1 跨模态向量量化框架

VITA 的表示对齐依赖于一个共享的向量量化器。给定任意连续嵌入 $z \in \mathbb{R}^d$，量化算子将其映射到码本中欧氏距离最近的向量：

$$
\mathcal{Q}(z) = c_k, \quad \text{where } k = \arg\min_j \|z - c_j\|_2
$$

该算子同时服务于视觉自编码器和动作自编码器，是跨模态 token 共享的数学基础。

**视觉运动编码**。视觉分支使用冻结的 DINOv2 提取单帧特征，再通过轻量级 M-Former 从连续帧对中捕获时空运动信息：

$$
z_v = \text{M-Former}([f_t; f_{t+1}]) \in \mathbb{R}^d
$$

其中 $f_t$、$f_{t+1}$ 分别为时刻 $t$ 和 $t+1$ 的 DINOv2 特征图。M-Former 输出的运动感知嵌入 $z_v$ 经共享量化器离散化后，由轻量 ViT 解码器重建未来帧。

**动作 DCT 编码**。动作分支将长度为 $H$ 的动作序列 $\mathbf{a}_{t:t+H}$ 通过离散余弦变换（DCT）压缩至频域，再由 MLP 编码为连续嵌入：

$$
z_a = \text{MLP}(\text{flatten}(\text{DCT}(\mathbf{a}_{t:t+H})))
$$

DCT 压缩的作用是将时域动作轨迹的能量集中到少数低频系数上，抑制高频噪声，使量化后的离散 token 能更紧凑地表征动作的宏观模式。量化后的动作 token 经 Transformer 解码器和逆 DCT 重建连续动作轨迹。

### 3.2 VLM 主干与渐进式注意力

VITA 的 VLM 主干由 SigLIP 视觉编码器和 Gemma 语言模型组成，负责接收多模态输入并自回归生成统一 token 序列。其核心创新在于**渐进式注意力**机制，将 token 序列显式划分为三个信息组，并约束注意力流的方向：

$$
\mathrm{input} \to \mathrm{textual} \to \mathrm{cross\text{-}modality}
$$

具体而言，多模态上下文由文本指令 token、观测图像 token 和机器人本体状态拼接而成：

$$
h_{ctx} = [T_{\text{text}}(\mathbf{x}); T_{\text{image}}(\mathbf{I}_0); \mathbf{s}] \in \mathbb{R}^{N \times d}
$$

其中 $\mathbf{x}$ 为语言指令，$\mathbf{I}_0$ 为当前观测帧，$\mathbf{s}$ 为机器人状态向量。VLM 首先生成文本思维链（Textual CoT），将指令分解为预定义符号子任务（如 `[GRASP]`、`[MOVE]`、`[PLACE]` 等），随后生成跨模态统一 token。这种设计实现了感知-计划-执行的信息解耦：输入 token 提供感知上下文，文本 token 承载符号级任务规划，跨模态 token 直接驱动视觉与动作的双解码。

### 3.3 隐式视觉思维链与双解码器

VITA 的隐式视觉思维链（Internal CoT）体现在：VLM 自回归生成的跨模态 token 序列同时路由到**视觉解码器**（轻量 ViT）和**动作解码器**（Transformer + 逆 DCT），并行输出未来帧预测和机器人动作轨迹。训练阶段的联合损失函数为：

$$
\mathcal{L}_{co} = \lambda_v \|\mathbf{I}_{1:T} - \hat{\mathbf{I}}_{1:T}\|_1 + \lambda_a \|\mathbf{a}_{1:H} - \hat{\mathbf{a}}_{1:H}\|_2^2
$$

其中 $\mathbf{I}_{1:T}$ 为真实未来 $T$ 帧，$\hat{\mathbf{I}}_{1:T}$ 为视觉解码器预测帧（L1 损失）；$\mathbf{a}_{1:H}$ 为真实动作序列，$\hat{\mathbf{a}}_{1:H}$ 为动作解码器输出（MSE 损失）；$\lambda_v$、$\lambda_a$ 为平衡权重。视觉预测作为归纳偏置，将环境动态信息内部化到共享 token 中，引导动作生成——推理时视觉解码器可完全丢弃，仅保留动作解码器以降低延迟。

### 3.4 三阶段渐近训练

VITA 的训练分为三个阶段，逐步建立跨模态对齐：

1. **预热阶段**：独立训练视觉自编码器和动作自编码器，仅通过各自的帧预测损失与动作重建损失优化编码器、解码器和共享码本。此阶段确保两种模态的嵌入均可被同一码本有效量化。
2. **共训阶段**：VLM 主干与双解码器联合学习。混合使用纯视频数据（仅优化视觉预测损失）和同步视觉-动作配对数据（优化联合损失 $\mathcal{L}_{co}$），使 VLM 学会生成同时蕴含视觉动态和运动控制信息的统一 token。
3. **微调阶段**：冻结 VLM 主干和视觉解码器，仅更新动作解码器，在目标机器人数据上适配特定硬件和任务分布。

消融实验证实，跳过预热直接共训会导致性能显著下降，验证了共享码本预热对跨模态表示对齐的必要性（Table 7）。

### 补充图表

![[assets/figures/papers/paper_list_l2354_https_arxiv_org_abs_2511_19859/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the VITA framework. Utilizing the cross-modal alignment in ⃝1 , visual perception and motor control modalities are unified in the shared discrete latent space, where the dual-autoencoder architectures are illustrated in ⃝2 and ⃝3 . Benefiting from the representation alignment, the VLM backbone in ⃝4 generates dynamics-unified tokens via a hybrid attention mechanism. These tokens are decoded into future frames and robot actions, as Internal CoT*

## 实验与分析

### 核心性能：跨基准全面领先

VITA 在五个主流机器人操纵基准上均取得最优或接近最优的结果，涵盖仿真长序列指令跟随、多任务操作、跨具身迁移和真实世界泛化。

**CALVIN ABC‑D 长序列指令跟随。** CALVIN 要求模型在 5 条连续指令下完成多步操纵，以平均完成指令数（Avg. Len）和连续完成 5 条指令的序列成功率（Task Completed in a Row）为核心指标。VITA 取得 Avg. Len 4.73，较先前最强基线 DeFI（4.51）提升 4.9%，较 UP‑VLA 提升 14.5%（Table 1）。连续完成 5 条指令的成功率达 84.5%，表明 VITA 在长时域任务中具备稳定的指令链接能力。

**LIBERO 多任务操作。** LIBERO 包含四个子套件（LIBERO‑Spatial、LIBERO‑Object、LIBERO‑Goal、LIBERO‑Long），覆盖空间推理、物体泛化、目标条件与长时域任务。VITA 在全部套件的平均成功率达 96.7%，超越 UniVLA（95.5%）和所有基线（Table 2）。在最具挑战性的 LIBERO‑Long 上，VITA 成功率 96.8%，较 CoT‑VLA 提升 36.2 个百分点，较 UniVLA 提升 3.0 个百分点，直接验证了隐式视觉思维链对长时域建模的增益。

**SimplerEnv 跨具身迁移。** SimplerEnv 包含 Google Robot 和 WidowX 两个分支，评估模型在不同机器人形态下的泛化能力。在 Google Robot 分支（视觉匹配设置）上，VITA 平均成功率 57.4%，较 DeFI（51.2%）提升 12.1%（Table 3）。在 WidowX 分支上，VITA 取得 71.5% 的平均成功率，优于此前最佳的 UniVLA（Table 4）。这表明共享离散潜在空间学习到的跨模态表示具备跨具身迁移能力。

**真实世界泛化。** 在 UR‑5e 真实机器人平台上评估 6 项任务（4 项 ID 任务 + 2 项 OOD 任务），VITA 平均成功率达 80.5%，显著超越所有基线（Table 5）。尤其在 OOD 任务上，VITA 性能下降幅度远小于各基线方法，展现出优异的分布外泛化能力。

### 消融实验：隐式视觉思维链是核心驱动力

**思维链策略消融。** Table 6 对比了四种思维链变体在四个基准上的表现：（1）无 CoT（仅直接生成动作）；（2）Textual CoT（纯文本子任务分解）；（3）Internal CoT（仅隐式视觉思维链，推理时丢弃视觉解码器）；（4）完整 VITA（Internal + Textual CoT）。关键发现：

- 仅 Internal CoT 在 LIBERO 上即达到 94.1% 平均成功率，大幅超越纯 Textual CoT，证明**未来帧预测作为动作生成的归纳偏置**是性能提升的根本原因，而非文本推理的附加效应。
- 完整 VITA（Internal + Textual CoT）将 LIBERO 平均成功率推至 96.7%，表明文本子任务分解与隐式视觉动力学偏置存在协同效应：文本 CoT 提供高层任务规划，视觉 CoT 提供底层运动动力学引导。

**训练策略消融。** Table 7 验证了三阶段渐近训练的必要性。跳过预热阶段直接进行共训，或仅进行共训而不微调，均导致性能显著下降。共享码本的独立预热是跨模态表示对齐的关键前提——若视觉和动作自编码器未在预热阶段学会将各自模态映射到同一离散空间，后续 VLM 主干难以有效学习统一的跨模态 token 生成。

**数据效率。** Table 8(a) 显示，VITA 仅使用 10% 的微调数据即可超越 OpenVLA 在全数据集上的表现，证明共享离散潜在空间带来的表示复用性显著降低了数据需求。Table 8(b) 进一步表明，VITA 在较少训练步数下即可收敛至高性能，训练效率突出。

### 推理效率：视觉解码器可丢弃，不影响实时性

Table 9 报告了 VITA 在不同未来帧预测数（12/24/48 帧）下的推理延迟。单步推理仅需 60–71 ms，动作级吞吐接近 60 Hz。关键设计在于：**推理时仅使用动作解码器，视觉解码器可完全丢弃**，未来帧预测仅在训练时作为归纳偏置参与损失函数。这保证了 VITA 在部署时不会因额外的视觉生成而增加延迟。

![[assets/figures/papers/paper_list_l2354_https_arxiv_org_abs_2511_19859/figures/013_Table_9.jpg]]
*Table 9: We report the model’s inference latency (ms) under different predicted future frame horizons*

### 失败模式与局限性

尽管 VITA 在多基准上表现优异，分析揭示了以下结构性问题：

1. **视觉思维链与文本思维链的融合不充分。** 当前 VITA 的文本 CoT 使用固定的符号子任务词汇表（如 `[GRASP]`、`[MOVE]`、`[PLACE]`），缺乏开放域语言推理能力。在需要深层语言理解和指令接地的复杂多步任务（如“制作三明治”式组合操作）中，纯符号子任务分解可能不足以捕捉任务语义的全部复杂性。

2. **动作离散化对精细时序动态的捕捉不足。** 动作序列通过离散余弦变换（DCT）压缩至频域后经共享码本量化，这一过程对平稳、周期性运动模式有效，但难以精细保留非平稳、非周期运动特征（如突发停止、多阶段操作切换、反应性在线纠正）。这可能在需要毫秒级时序控制精度的任务中构成瓶颈。

3. **真实世界 OOD 任务仍有提升空间。** 尽管 VITA 在 OOD 任务上的性能下降远小于基线，但绝对成功率仍有改进余地。当前共享码本的跨模态对齐依赖于训练数据的分布覆盖，对极端分布偏移的鲁棒性需要进一步验证。

### 关键图表结论速览

- **Table 1（CALVIN ABC‑D）**：VITA Avg. Len 4.73，连续 5 指令成功率 84.5%，双指标均最优。
- **Table 2（LIBERO）**：VITA 四套件平均 96.7%，LIBERO‑Long 96.8%，较 CoT‑VLA 提升 36.2pp。
- **Table 3–4（SimplerEnv）**：跨具身迁移能力验证，Google Robot 分支 57.4%（+12.1% vs DeFI），WidowX 分支 71.5%。
- **Table 5（真实世界）**：6 项任务平均 80.5%，OOD 泛化优势显著。
- **Table 6（CoT 消融）**：Internal CoT 单独使用即大幅优于 Textual CoT，完整 VITA 达 96.7%。
- **Table 7（训练策略消融）**：三阶段渐近训练各阶段均不可或缺，预热阶段对码本对齐至关重要。
- **Table 9（推理延迟）**：单步 60–71 ms，视觉解码器可丢弃，实时性不受影响。

![[assets/figures/papers/paper_list_l2354_https_arxiv_org_abs_2511_19859/figures/003_Table_1.jpg]]
*Table 1: Results on CALVIN ABC-D. We report The average number of tasks completed after executing 5 consecutive instructions over 1,000 evaluation rollouts*

![[assets/figures/papers/paper_list_l2354_https_arxiv_org_abs_2511_19859/figures/005_Table_2.jpg]]
*Table 2: Performance comparison of VITA and baseline models on the LIBERO simulations*

![[assets/figures/papers/paper_list_l2354_https_arxiv_org_abs_2511_19859/figures/007_Table_3.jpg]]
*Table 3: Performance evaluation of VITA and baselines on the SimplerEnv-GoogleRobot benchmark (visual matching)*

![[assets/figures/papers/paper_list_l2354_https_arxiv_org_abs_2511_19859/figures/006_Table_5.jpg]]
*Table 5: Real-World Evaluation Results. For each model, we report the average success rate over 1,000 rollouts, where the top four are ID tasks, and bottom two are OOD tasks*

![[assets/figures/papers/paper_list_l2354_https_arxiv_org_abs_2511_19859/figures/008_Table_6.jpg]]
*Table 6: Performance comparison of various chain-of-thought strategies in simulated environments*

![[assets/figures/papers/paper_list_l2354_https_arxiv_org_abs_2511_19859/figures/012_Table_7.jpg]]
*Table 7: Performance comparison of various training strategies*

### 补充图表

![[assets/figures/papers/paper_list_l2354_https_arxiv_org_abs_2511_19859/figures/004_Table_4.jpg]]
*Table 4: Performance evaluation of VITA and existing baseline models on the SimplerEnv-WidowX benchmark*

![[assets/figures/papers/paper_list_l2354_https_arxiv_org_abs_2511_19859/figures/010_Table_8.jpg]]
*Table 8: Further experiments in simulated environment to evaluate model data and training efficiency*

![[assets/figures/papers/paper_list_l2354_https_arxiv_org_abs_2511_19859/figures/009_Figure_3.jpg]]
*Figure 3: Visualization of the “contextual reasoning and color matching” in the real world*

## 方法谱系与知识库定位

### 1. 核心瓶颈与VITA的因果杠杆

现有视觉‑语言‑动作（VLA）方法面临两个根本瓶颈，构成了VITA提出的直接动机：

- **模态差距**：高维视觉观测（像素空间）与低维动作指令（关节角度/末端位姿）之间存在巨大的表示鸿沟。从像素直接回归精确动作，要求模型隐式学习前向动力学（视觉→动作）和逆向动力学（动作→视觉后果），而这两个映射在独立特征空间中极难同时优化。
- **目标竞争**：视觉预测代理任务（如未来帧重建）与动作生成任务共享同一主干时，二者的优化目标往往相互竞争，导致训练不稳定、收敛缓慢，甚至出现“跷跷板”效应——一个任务的提升以另一个任务的退化为代价。

VITA的因果杠杆在于**构建跨模态共享离散潜在空间**（shared discrete latent space）。通过矢量量化（Vector Quantization, VQ）码本，视觉嵌入和动作嵌入被映射到同一离散词汇表。这一设计使得统一标记（unified tokens）可以同时解码为未来帧和动作轨迹，从而将未来帧预测作为动作生成的归纳偏置（inductive bias），统一了前向与逆向动力学。核心洞察可概括为**隐式视觉思维链**（Implicit Visual Chain-of-Thought）：自回归生成的共享标记序列经过双解码器并行输出未来帧预测和机器人动作，将视觉动态内部化为运动规划的引导，而无需显式的轨迹模拟或“先预测再行动”的两阶段流水线。

### 2. 在VLA方法谱系中的定位

VITA处于VLA研究的交汇地带——既继承了视频预测增强策略的思想，又超越了显式视觉思维链的范式。以下沿两条技术脉络定位其贡献：

#### 2.1 视频预测增强的VLA

**DeFI** 等方法率先将未来帧预测作为辅助任务引入VLA训练，证明视觉动态建模有助于动作生成。然而，DeFI的视觉预测与动作生成仍共享连续潜在空间，未解决模态对齐问题。VITA通过共享离散码本，将视觉预测从“辅助正则项”提升为“动作生成的归纳偏置”，使两者在表示层面和优化目标上均保持一致。在CALVIN ABC‑D上，VITA平均完成4.73个连续指令，相对于DeFI（4.51）提升4.9%（Table 1），验证了离散共享空间相对于连续共享空间的优势。

**UniVLA** 和 **UP‑VLA** 代表利用大规模无标签/人类视频预训练的另一条路线。UniVLA在LIBERO四套件上平均成功率95.5%，为先前最佳；VITA达到96.7%，并在长时域子集LIBERO‑Long上以96.8%显著超越UniVLA的94.0%（Table 2）。这表明，即使在大规模预训练的强基线面前，隐式视觉思维链仍能提供额外的长时域建模增益。

#### 2.2 显式视觉思维链VLA

**CoT‑VLA** 采用显式视觉思维链——先自回归生成未来图像，再基于生成的图像预测动作。这种“预测‑再行动”范式将视觉推理与动作生成解耦，但引入级联误差，且生成高维图像的计算开销巨大。VITA的隐式视觉思维链在共享潜在空间中完成视觉动态推理，无需生成像素级中间表示，从根本上避免了级联误差。在LIBERO上，VITA成功率较CoT‑VLA提升36.2%（Table 2），消融实验进一步表明：仅保留隐式视觉思维链（Internal CoT）即大幅优于纯文本思维链变体，完整VITA（Internal + Textual CoT）在LIBERO平均成功率达96.7%（Table 6）。

#### 2.3 通用机器人策略基线

在更广泛的VLA基线中，**OpenVLA** 作为开源VLA基线被广泛使用；**Pi0** 和 **Pi0‑FAST** 探索离散动作解码；**GR‑1**、**Octo**、**CogACT** 等代表通用机器人操纵策略的不同设计取向。VITA在SimplerEnv Google Robot分支上平均成功率57.4%，较DeFI（51.2%）提升12.1%（Table 3）；在真实世界6项任务上平均成功率达80.5%，显著超越所有基线（Table 5），且在OOD任务上性能下降远小于各基线，展现出优异的泛化能力。

### 3. 适用边界与局限

尽管VITA在多个基准上取得领先，其设计选择也划定了适用边界：

1. **视觉‑语言推理的深层融合不足**：VITA尚未完全整合视觉思维链（V‑CoT）与文本思维链（T‑CoT）。当前设计中，文本CoT生成符号子任务（如[GRASP]、[MOVE]、[PLACE]），视觉CoT生成未来帧，二者在VLM主干中共享渐进注意力但缺乏显式的协同推理机制。在需要深层语言理解和指令接地的复杂多步任务（如“制作三明治”这类涉及条件判断、计数和语义组合的任务）中，性能可能受限。论文明确指出这一局限，并将其列为开放问题。

2. **动作离散化的时序精度瓶颈**：动作序列通过离散余弦变换（DCT）压缩至频域，再经共享码本量化。这一设计有效降低了动作表示的维度，但DCT天然假设信号的平稳性和周期性，难以精细捕捉非平稳、非周期运动模式——如突发停止、多阶段操作中的模式切换、或基于力反馈的反应性纠正。在需要毫秒级时序控制精度的接触富集任务（如精密装配、柔性物体操纵）中，该瓶颈可能成为性能天花板。

3. **共享码本的容量‑特异性权衡**：码本大小为8192，视觉和动作共享同一量化器。当训练数据涵盖高度异构的机器人平台、相机视角和动作空间时，码本可能面临“表示碰撞”——不同模态或不同平台的嵌入被迫共享码字，导致信息损失。论文未系统评估码本大小对跨平台泛化的影响，这一维度需要进一步验证。

### 4. 开放问题

论文明确提出的开放问题指向VITA范式的两个演进方向：

- **动作标记化的重新设计**：如何构建保留细粒度时间动态的动作离散标记化机制？可能的路径包括：引入层次化VQ（如残差VQ）以增加表示容量；采用学习式基函数替代固定DCT基；或探索直接在时域进行向量量化的方案，以捕捉非平稳运动模式。

- **视觉与文本思维链的协同融合**：如何实现V‑CoT与T‑CoT的充分协同推理？当前设计是“串联式”的（先文本CoT，再跨模态CoT），未来可探索交叉注意力、联合推理或规划‑执行交替的架构，使语言理解直接参与视觉动态推理，反之亦然。

此外，从知识库视角看，VITA的共享离散潜在空间设计在概念上与多模态基础模型中的“统一词汇表”思路（如将视觉、语言、动作均视为token）一脉相承，但其三阶段渐近训练策略（预热→共训→微调）为跨模态码本学习提供了可操作的工程范式。消融实验表明，跳过预热阶段直接共训会导致性能显著下降（Table 7），验证了独立预训练码本对于后续联合学习的必要性——这一发现对相关领域（如视频‑语言预训练、多模态具身智能）具有借鉴意义。

## 原文 PDF

![[paperPDFs/CVPR_2026/Unifying_Perception_and_Action_A_Hybrid_Modality_Pipeline_with_Implicit_Visual_Chain_of_Thought_for_Robotic_Action_Generation.pdf]]
