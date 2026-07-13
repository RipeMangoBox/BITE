---
title: "Geometry-as-context: Modulating Explicit 3D in Scene-consistent Video Generation to Geometry Context"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Geometry_as_context_Modulating_Explicit_3D_in_Scene_consistent_Video_Generation_to_Geometry_Context.pdf
project_link: null
code_link: null
aliases:
- GACG
- Geometry-as-context
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将非可微分重建与绘制算子替换为可微分的自回归生成模型，并将显式几何信息作为上下文输入，实现端到端优化以减轻累积误差。
primary_logic: 利用视频生成模型的强先验，将几何估计与视图合成统一在单一模型中，通过交错文本-图像-几何序列和Camera Gated Attention机制，让模型学会利用相机姿态区分不同任务，同时采用几何Dropout策略平衡效率与性能。
claims:
- 使用单个模型代替独立的几何预测、图像变形和完成步骤，实现端到端训练，减少累积误差。
- Camera Gated Attention 显著降低旋转和平移误差，提升视觉质量。
- "几何上下文变体（Variant #1）在所有指标上优于无几何或仅变形图像的变体，说明显式3D信息对长序列3D一致性至关重要。"
- 几何Dropout 在不显著降低性能的前提下，将训练和推理时间减半。
---

# Geometry-as-context: Modulating Explicit 3D in Scene-consistent Video Generation to Geometry Context

> [!tip] 核心洞察
> 利用视频生成模型的强先验，将几何估计与视图合成统一在单一模型中，通过交错文本-图像-几何序列和Camera Gated Attention机制，让模型学会利用相机姿态区分不同任务，同时采用几何Dropout策略平衡效率与性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | 几何即上下文：面向几何上下文的场景一致性视频生成中的显式3D调制 |
| 英文题名 | Geometry-as-context: Modulating Explicit 3D in Scene-consistent Video Generation to Geometry Context |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.21929) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Geometry-as-Context (GaC) |
| Dataset | RealEstate10K, Tanks-and-Temples |

> [!tip] 效果简介
> - RealEstate10K 上，PSNR 19.01 vs 18.57 (w/o CGA) (+0.44)；FID 55.76 vs 68.42 (w/o CGA) (-12.66)。
> - 训练效率 上，Training Time per step (s/step) 11 vs 24 (w/o dropout) (-54%)。
> - 推理效率 上，Inference Time per image (s/img) 2.2 vs 4.6 (w/o dropout) (-52%)。

## 概要

### 问题背景与瓶颈

从单张图像生成场景一致的长序列视频是视觉内容生成的核心挑战。现有方法主要分为两类：基于视频的生成式方法直接利用视频扩散模型产生新视角，但缺乏显式3D约束，难以维持长距离相机运动下的几何一致性；基于重建的方法则通过迭代式几何估计、3D重建、新视角渲染和图像修复来保证一致性，但其流水线中的几何估计器、反投影与渲染算子均为不可微分操作，导致各步骤间的累积误差无法通过端到端训练进行修正。这一结构性瓶颈限制了场景视频生成在长序列和往复轨迹下的3D一致性表现。

### 核心方法

本文提出 **Geometry-as-Context (GaC)** 框架，将显式几何信息作为上下文引入场景视频生成。其核心思想是将传统的非可微分重建流水线替换为单一的自回归相机可控视频生成模型，使几何预测、图像变形和修复三个子任务统一在同一个扩散变换器（DiT）中完成，从而实现端到端优化以减轻累积误差。具体而言，GaC 构建了文本引导的交错序列建模，通过插入任务提示令牌（`<Geometry>` 或 `<Image>`）告知模型下一步生成几何信息还是RGB图像；同时设计了 **Camera Gated Attention (CGA)** 机制，利用Plücker射线增强自注意力查询并生成门控矩阵，使模型能够根据相机姿态区分几何估计与视图合成两种不同任务。此外，**几何Dropout** 策略在训练时随机丢弃几何上下文，既让模型学会从几何信息中提取3D一致性约束，又允许推理时仅输出RGB图像，显著提升效率。

### 方法谱系与知识库定位

GaC 属于基于重建的场景视频生成方法，与 **ViewCrafter**（Yu et al., TPAMI 2025）、**GEN3C**（Ren et al., CVPR 2025）和 **Voyager**（Huang et al., TOG 2025）等工作共享利用显式3D表示保持一致性的设计理念。区别于这些方法依赖独立的几何估计器和非可微分重建算子，GaC 首次将几何估计与视图合成统一在单个生成模型中，并通过CGA和几何Dropout实现端到端训练。与纯视频生成方法如 **VMem**（Li et al., ICCV 2025）和 **Stable Virtual Camera**（Zhou et al., arXiv 2025）相比，GaC 引入了显式深度图作为几何上下文，增强了长序列3D记忆能力。

### 主要结果概要

在 RealEstate10K 和 Tanks-and-Temples 等基准上，GaC 在单视图场景视频生成任务中取得了具有竞争力的定量结果（如 Tanks-and-Temples 上 PSNR 15.77）。消融实验表明，使用几何作为上下文（Variant #1）在所有指标上显著优于不使用上下文或仅使用变形图像的变体，验证了显式3D信息对场景一致性的关键作用。Camera Gated Attention 不仅提升了图像质量（FID 从 68.42 降至 55.76），还显著降低了相机姿态误差。几何Dropout 策略在几乎不损失生成质量的前提下，将训练迭代时间和推理时间分别降低约一半。定性结果展示了 GaC 在室外、室内、开放场景以及前后往复相机轨迹下的长期3D一致性，尤其在循环运动中能够忠实恢复先前消失的物体。

### 局限与开放问题

当前方法对人体和复杂主体的生成效果仍然有限，部分室外场景在大幅视点外推时可能出现边界纹理变暗的伪影。在前后往复长距离轨迹上，所有方法的性能均有明显下降，GaC 虽表现最优但仍存在3D一致性退化。该方法依赖预先计算的相机轨迹，尚未支持实时交互场景生成。未来方向包括扩展几何上下文的表示能力（如引入语义信息或3DGS）、利用更长序列和更大模型增强长距离3D记忆，以及探索与实时SLAM系统的结合以实现交互式探索。

### 场景一致性视频生成的核心挑战

从单张图像或文本描述生成具有3D一致性的长序列视频，是计算机视觉与生成模型交叉领域的前沿问题。其核心难点在于：模型不仅需要合成逼真的单帧图像，还必须确保跨视点的几何连贯性——即场景中的物体在相机运动过程中保持形状、纹理和空间位置的一致性，不发生扭曲、漂移或突然消失。这一需求在自动驾驶仿真、虚拟现实漫游、影视特效预览等应用中尤为关键。

### 现有方法的三条技术路线及其瓶颈

当前解决该问题的方法可大致归为三类：

**基于视频的方法**以**VMem**（Li et al., ICCV 2025）为代表，将场景生成建模为视频帧的时序预测问题。这类方法依赖视频扩散模型的强时序先验来维持帧间连贯性，但缺乏对底层3D结构的显式建模，在长距离相机运动或大角度旋转时容易出现几何漂移和细节丢失。

**基于重建的方法**是目前的主流范式，包括**ViewCrafter**（Yu et al., TPAMI 2025）、**GEN3C**（Ren et al., CVPR 2025）和**Voyager**（Huang et al., TOG 2025）等。它们采用“几何估计—3D重建—新视角渲染—图像修复”的迭代流水线：先从当前帧估计深度或点云等几何信息，反投影为3D表示，再根据目标相机姿态渲染新视角图像，最后由生成模型修复渲染图中的空洞和伪影。这一流程可形式化为四个步骤：

$$G_i = \epsilon(I_i)$$
$$3D = \mathrm{Unproject}(I_i, G_i)$$
$$I_{i+1}' = \mathrm{Render}(3D, P_{i+1})$$
$$I_{i+1} = \varrho(I_{i+1}', P_{i+1})$$

尽管显式3D表示提供了几何约束，该流程存在一个**根本性瓶颈**：几何估计器 ε、反投影 Unproject 和渲染算子 Render 均为非可微分操作，导致整个流水线无法端到端训练。几何估计的误差会通过不可微的3D重建步骤传递到渲染图像，再由修复网络放大，形成**累积误差**。随着生成序列增长，这种误差不断叠加，最终导致3D一致性崩溃。

**生成式新视角合成方法**如**Stable Virtual Camera**（Zhou et al., arXiv 2025）尝试绕开显式重建，直接利用扩散模型从输入视图和相机姿态生成新视角。这类方法虽然避免了非可微分算子，但因缺乏显式3D记忆，在长序列生成中难以维持全局几何一致性。

### 本文的动机与核心思路

上述分析揭示了一个关键洞察：**基于重建方法的累积误差根源于流水线中不可微算子与非端到端训练之间的耦合**。若能将这些算子替换为可微分的生成过程，同时保留显式几何信息的约束作用，就有望在维持3D一致性的同时实现端到端优化。

本文提出**Geometry-as-Context (GaC)** 框架，核心思想是：将非可微分的重建与渲染算子替换为**单个自回归相机控制视频生成模型**，并将显式几何信息（如深度图）作为上下文输入该模型。模型以交错序列形式接收RGB图像、几何图和文本提示，统一完成几何预测、图像变形和图像修复三个子任务：

$$\{G_i, I_{i+1}', I_{i+1}\} = \varrho(\{I_i, G_i, I_{i+1}'\}, P_{i+1})$$

这一设计将原本割裂的流水线转化为可端到端训练的生成框架，利用视频扩散模型的强先验来抑制累积误差。同时，为增强模型对相机姿态的利用能力，GaC引入了**Camera Gated Attention (CGA)** 机制，使模型能根据相机运动区分几何估计与视图合成两种不同任务。此外，**几何Dropout**策略在训练时随机丢弃几何上下文，使模型既学会利用3D信息维持一致性，又能在推理时跳过几何输出以提升效率。

简言之，GaC 的动机在于：**用可微分的生成模型替代不可微的重建算子，将显式几何从“中间产物”升级为“调制上下文”，从而在保留3D先验的同时打通端到端训练的路径。**

## 核心方法与创新机理

GaC 的核心创新在于将传统基于重建的场景视频生成流水线中**不可微分的几何重建与绘制算子替换为单一的可微分自回归生成模型**，从而实现了端到端优化，从根本上缓解了累积误差问题。这一创新通过三个关键的 **changed slots** 体现：

### 1. 几何估计与视图合成的统一建模

传统方法（如 **ViewCrafter** (Yu et al., TPAMI 2025) 和 **GEN3C** (Ren et al., CVPR 2025)）将场景视频生成分解为独立的几何估计、非可微分重建、渲染和图像修复等子任务，各模块间无法端到端训练，导致几何估计误差在流水线中逐级放大。GaC 提出将所有子任务内部化到单个相机可控的生成模型 $\varrho$ 中：

$$\{G_i, I_{i+1}', I_{i+1}\} = \varrho(\{I_i, G_i, I_{i+1}'\}, P_{i+1})$$

该模型以自回归方式处理交错的 RGB-几何序列，将几何预测、图像变形和修复统一为生成过程，使整个流水线可微分且可端到端优化（Section 4.1, Eq.9）。消融实验证明显式几何上下文（Variant #1）在所有指标上均优于仅使用变形图像（Variant #2）或不使用任何上下文（Variant #3）的变体（Table 3），说明显式 3D 信息对长序列 3D 一致性至关重要。

### 2. Camera Gated Attention 机制

传统相机条件方法通常采用简单的 Plücker 射线编码加法或拼接，无法有效区分相机姿态在不同子任务（几何估计 vs. 视图合成）中的差异化作用。GaC 提出了 **Camera Gated Attention (CGA)**，通过调制自注意力机制实现相机姿态的精细控制：

$$\{Q, K, V\} = \mathrm{Linear}_1(F_i)$$
$$\{Q_{res}, Gate\} = \mathrm{Linear}_2(Q + r_i)$$
$$O = \mathrm{Linear}_3(O * \sigma(Gate))$$

CGA 将 Plücker 射线特征与查询向量相加后投影，生成残差查询和门控矩阵，对自注意力输出进行调制（Section 4.2, Eqs.13-16）。消融实验表明，CGA 不仅显著提升图像质量（PSNR +0.44, FID −12.66），还大幅降低了相机姿态误差（旋转误差 R_err 和位移误差 T_err 均有明显下降），验证了门控机制对相机控制的增强作用（Table 5）。

### 3. 几何 Dropout 训练策略

为平衡 3D 一致性与计算效率，GaC 提出了**几何 Dropout** 策略：训练时随机丢弃几何上下文，使模型既能从几何建模中学习场景一致性，又能在推理时仅生成 RGB 图像，避免不必要的几何输出。该策略将训练迭代时间从 24 s/step 降至 11 s/step（−54%），推理时间从 4.6 s/img 降至 2.2 s/img（−52%），且性能几乎无下降（Table 6）。

Geometry-as-Context (GaC) 的核心动机在于消除传统基于重建的场景视频生成流水线中，由非可微分算子（反投影、渲染）与独立修复网络所导致的累积误差。原始流水线（Algorithm 1）采用串行结构：首先从当前图像 $I_i$ 估计几何信息 $G_i = \epsilon(I_i)$，随后通过反投影得到三维表示 $3D = \mathrm{Unproject}(I_i, G_i)$，再根据目标相机姿态 $P_{i+1}$ 渲染出新视角图像 $I_{i+1}' = \mathrm{Render}(3D, P_{i+1})$，最后交由生成模型 $\varrho$ 进行修复得到最终图像 $I_{i+1} = \varrho(I_{i+1}', P_{i+1})$。这一流程中，几何估计器 $\epsilon$ 与渲染算子均为黑盒模块，无法与生成模型联合优化，导致几何误差在迭代中逐帧放大。

GaC 的关键设计是将上述非可微分的几何估计、反投影与渲染操作全部内化至单一的自回归扩散变换器（DiT）主干中，将问题重新定义为统一的生成任务。具体而言，模型以交错序列作为输入，将当前图像 $I_i$ 与对应的几何上下文 $G_i$（如深度图）拼接后，连同目标相机姿态 $P_{i+1}$ 一并送入生成模型 $\varrho$，同时输出下一视点的几何信息 $G_{i+1}$ 和 RGB 图像 $I_{i+1}$。这一过程可形式化为：

$$\{G_{i+1}, I_{i+1}\} = \varrho(\{I_i, G_i\}, P_{i+1})$$

与原始流水线相比，GaC 不再需要显式的反投影与渲染步骤，而是让模型自主学习从几何上下文到新视角图像的映射关系。这种端到端可微的设计使得梯度能够贯穿整个序列生成过程，有效抑制了累积误差的传播。

在架构层面，GaC 引入了 **Camera Gated Attention (CGA)** 模块，以增强模型对相机姿态的利用效率。CGA 的核心思想是让相机信息（以 Plücker 射线编码形式）直接参与自注意力机制中的查询调制与输出门控。给定潜在特征 $F_i$，首先通过线性投影得到查询、键、值：

$$\{Q, K, V\} = \mathrm{Linear}_1(F_i)$$

随后将查询 $Q$ 与 Plücker 射线特征 $r_i$ 相加，再经线性投影生成残差查询 $Q_{res}$ 与门控矩阵 $Gate$：

$$\{Q_{res}, Gate\} = \mathrm{Linear}_2(Q + r_i)$$

最终的注意力输出由门控信号调节：

$$O = \mathrm{Linear}_3(O * \sigma(Gate))$$

这一设计使模型能够根据相机姿态动态调整注意力分布，从而区分几何预测与视图合成两个子任务对相机信息的不同需求。

训练策略方面，GaC 采用**文本引导的交错序列建模**，通过插入特殊提示词（`<Geometry>` 与 `<Image>`）告知模型当前应生成几何信息还是 RGB 图像，实现多任务的无缝切换。同时，为平衡计算效率与三维一致性，GaC 引入**几何 Dropout** 策略：在训练过程中随机丢弃几何上下文，迫使模型在缺乏显式三维信息时仍能保持场景一致性，同时在推理阶段可直接跳过几何输出以加速生成。消融实验表明，该策略在几乎不损失生成质量的前提下，将训练迭代时间与推理时间分别降低约 54% 和 52%（Table 6）。

综上，GaC 的整体框架通过将显式几何信息作为上下文、以 CGA 实现相机感知的注意力调制、并辅以几何 Dropout 的效率优化，构建了一个端到端可训练的场景一致性视频生成流水线。

### 问题形式化：从多阶段重建到统一生成

本文以**基于重建的场景视频生成**流水线为出发点，形式化其固有的累积误差问题。给定输入图像 $I_i$ 和目标相机姿态 $P_{i+1}$，传统流水线由三个独立且非可微的阶段构成：

**几何估计**：使用几何估计器 $\epsilon$ 从当前视图预测几何信息（如深度图）：

$$G_i = \epsilon(I_i)$$

**反投影与渲染**：将图像与几何信息反投影为3D表示，再从目标姿态渲染出新视角图像：

$$3D = \mathrm{Unproject}(I_i, G_i)$$

$$I_{i+1}' = \mathrm{Render}(3D, P_{i+1})$$

**图像修复**：生成模型 $\varrho$ 对渲染结果进行修复，填补孔洞并增强真实感：

$$I_{i+1} = \varrho(I_{i+1}', P_{i+1})$$

这一流水线的根本瓶颈在于：几何估计误差通过非可微的 Unproject 和 Render 算子传播，修复阶段无法反向修正几何预测，导致长序列生成中累积误差持续放大（见 Figure 2(a)）。

### 核心思路：将几何内化为可微上下文

GaC 的核心设计是将上述三个非可微算子**统一到单个自回归生成模型**中，使几何预测、图像变形和修复成为端到端可优化的子任务。其关键形式化表达为：

$$\{G_i, I_{i+1}', I_{i+1}\} = \varrho(\{I_i, G_i, I_{i+1}'\}, P_{i+1})$$

该公式表明：单个相机受控的生成模型 $\varrho$ 同时输出几何 $G_i$、变形图像 $I_{i+1}'$ 和修复图像 $I_{i+1}$，将所有子任务纳入统一的可微分框架，从根本上消除阶段间的误差隔离。

### 几何上下文变体设计

为实现上述统一，论文探索了三种几何上下文变体，对应不同的信息传递策略：

**变体 #1：几何作为上下文（最终方案）**。模型先预测当前视图的几何 $G_i$，再基于该几何生成下一视点的 RGB 图像 $I_{i+1}$：

$$\{G_i, I_{i+1}\} = \varrho(\{I_i, G_i\}, P_{i+1})$$

此变体将显式3D几何作为中间上下文，使模型在生成新视图时具备显式的3D一致性约束，是消融实验中性能最优的方案（Table 3）。

**变体 #2：变形图像作为上下文**。模型先通过内部隐式变形生成 $I_{i+1}'$，再对其进行修复：

$$\{I_{i+1}', I_{i+1}\} = \varrho(\{I_i, I_{i+1}'\}, P_{i+1})$$

该变体缺乏显式几何约束，3D一致性弱于变体 #1。

**变体 #3：无上下文**。模型直接从当前图像和目标姿态预测下一帧，退化为纯视频生成框架：

$$\{I_{i+1}\} = \varrho(I_i, P_{i+1})$$

该变体完全省略了3D重建组件，长序列一致性最差。

### Camera Gated Attention：相机姿态的条件化注入

为实现相机姿态对生成过程的有效调控，GaC 提出了 **Camera Gated Attention (CGA)** 模块，其核心在于利用 Plücker 射线编码调制自注意力机制，使模型能够区分相机在几何预测和视图合成中的不同作用。

给定潜在特征 $F_i$，CGA 的计算流程如下：

**步骤一：标准投影**。对输入特征进行线性投影得到自注意力的查询、键和值：

$$\{Q, K, V\} = \mathrm{Linear}_1(F_i)$$

**步骤二：相机条件化查询与门控生成**。将查询 $Q$ 与 Plücker 射线特征 $r_i$ 相加后，通过第二个线性层同时生成残差查询 $Q_{res}$ 和门控矩阵 $Gate$：

$$\{Q_{res}, Gate\} = \mathrm{Linear}_2(Q + r_i)$$

**步骤三：门控注意力输出**。注意力输出 $O$ 经门控矩阵调节后，通过第三个线性层得到最终输出：

$$O = \mathrm{Linear}_3(O * \sigma(Gate))$$

其中 $\sigma$ 为 sigmoid 激活函数，$*$ 表示逐元素乘法。该设计的关键在于：门控矩阵使模型能够根据相机姿态动态调节注意力输出的强度，从而在几何估计任务和视图合成任务之间灵活切换注意力模式。消融实验（Table 5）证实，CGA 不仅显著提升 PSNR（+0.44）和 FID（-12.66），还大幅降低了相机姿态误差 $R_{err}$ 和 $T_{err}$。

### 文本引导的交错序列建模与几何 Dropout

为支持多任务切换，GaC 采用**文本引导的交错序列格式**：在输入序列中插入特殊文本提示 `<Geometry>` 或 `<Image>`，告知模型下一输出为几何图还是 RGB 图像。模型以自回归方式处理交错 RGB-几何-文本序列，由单个 DiT 主干统一完成所有子任务（见 Figure 3）。

![[assets/figures/papers/paper_list_l2506_https_arxiv_org_abs_2602_21929/figures/003_Figure_3.jpg]]
*Figure 3: Detailed architecture of geometry-as-context*

训练阶段引入**几何 Dropout 策略**：随机丢弃输入序列中的几何上下文，使模型学会在缺乏显式几何的情况下仍能保持场景一致性，同时大幅缩短序列长度。Table 6 显示，该策略将训练迭代时间从 24 s/step 降至 11 s/step（-54%），推理时间从 4.6 s/img 降至 2.2 s/img（-52%），而生成质量几乎无退化。推理时可通过省略 `<Geometry>` 提示跳过几何输出，仅生成 RGB 图像，进一步提升效率。

## 实验与关键发现

### 主要结果：单视图场景视频生成

GaC 在 RealEstate10K 和 Tanks-and-Temples 两个基准上进行了单视图场景视频生成评测，与基于视频的检索方法 **VMem** (Li et al., ICCV 2025)、基于重建的方法 **ViewCrafter** (Yu et al., TPAMI 2025)、**GEN3C** (Ren et al., CVPR 2025)、**Voyager** (Huang et al., TOG 2025) 以及生成式新视角合成方法 **Stable Virtual Camera** (Zhou et al., arXiv 2025) 进行了全面对比。

在 RealEstate10K 给定相机轨迹的设置下（Table 1），GaC 取得了 **PSNR 19.01**、**FID 55.76** 的领先结果。相比基于视频的方法，GaC 在相机控制精度上展现出明显优势——旋转误差 $R_{err}$ 和位移误差 $T_{err}$ 均显著低于视频类基线，这归因于显式几何上下文对相机姿态的精确约束。定性结果（Figure 4）表明，GaC 生成的第20帧新视角图像在场景结构保持和纹理一致性上优于对比方法，尤其在远距离视点变化下仍能维持合理的3D几何。

![[assets/figures/papers/paper_list_l2506_https_arxiv_org_abs_2602_21929/figures/004_Table_1.jpg]]
*Table 1: Quantitative results of scene video generation from single view with given camera trajectory*

![[assets/figures/papers/paper_list_l2506_https_arxiv_org_abs_2602_21929/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative results of scene video generation from single view. Compared to the baselines, our model generates more consistent novel views. These images are the 20-th frame of the generated video clip except the input one. For a clearer visualization, please zoom in*

在更具挑战性的前后往复相机轨迹设置下（Table 2），所有方法的性能均有明显下降，但 GaC 依然保持最优。这一场景要求模型在离开并返回同一区域时恢复先前可见的物体——例如 Figure 1 最后一行中，计算机在第32帧消失后，GaC 仍能在后续帧中忠实还原该物体，展现出对长期3D记忆的有效保持。

![[assets/figures/papers/paper_list_l2506_https_arxiv_org_abs_2602_21929/figures/001_Figure_1.jpg]]
*Figure 1: Teaser demonstration. We introduce Geometry-as-Context (GaC), a framework that leverages explicit 3D information into reconstruction-based scene video generation. GaC mitigates cumulative errors from non-differentiable reconstruction and non-end-to-end training pipelines. Furthermore, GaC enhances the 3D consistency and long-term 3D memory of generative video models. We showcase GaC under four settings:on outdoor, indoor, in-the-wild, and forth-and-back camera trajectory. GaC maintains consistency under cyclic motion: even when an object (e.g., a computer) disappears in the 32-nd frame of the last row, it is faithfully restored in later frames*

![[assets/figures/papers/paper_list_l2506_https_arxiv_org_abs_2602_21929/figures/006_Table_2.jpg]]
*Table 2: Quantitative results of scene video generation from single view with forth-and-back camera trajectory*

### 消融实验

#### 几何上下文变体分析

Table 3 对比了三种几何上下文变体：
- **Variant #1（几何作为上下文）**：模型先预测几何 $G_i$，再生成下一视点 RGB 图像 $I_{i+1}$；
- **Variant #2（变形图像作为上下文）**：使用渲染的变形图像 $I_{i+1}'$ 作为上下文；
- **Variant #3（无上下文）**：退化为纯视频生成框架，仅从 $I_i$ 和 $P_{i+1}$ 直接预测 $I_{i+1}$。

![[assets/figures/papers/paper_list_l2506_https_arxiv_org_abs_2602_21929/figures/009_Table_3.jpg]]
*Table 3: Ablation on different variants of geometry-as-context*

结果表明，Variant #1 在 PSNR、SSIM、LPIPS、FID 四项指标上均优于其他变体。这证明显式3D几何信息（而非变形RGB图像或空上下文）是维持长序列3D一致性的关键因素。Variant #3 由于完全省略了3D重建组件，场景一致性退化最为严重。

#### 几何表示选择

Table 4 消融了深度图与点图两种几何表示。深度图在 LPIPS 感知质量指标上略优于点图，且作为单通道表示具有更低的内存和计算开销，因此被选为默认几何上下文格式。

#### Camera Gated Attention 的有效性

Table 5 验证了 CGA 模块的贡献。移除 CGA（即使用简单的 Plücker 射线编码相加）后，PSNR 从 19.01 降至 18.57，FID 从 55.76 恶化至 68.42。更重要的是，CGA 显著降低了相机姿态误差——旋转误差 $R_{err}$ 和位移误差 $T_{err}$ 均有大幅下降。这说明 CGA 通过门控机制有效区分了相机姿态在几何预测和视图合成两个子任务中的不同作用，使模型学会根据任务需求选择性利用相机信息。

#### 几何 Dropout 的效率-性能权衡

Table 6 展示了几何 Dropout 策略的效果。训练时随机丢弃几何上下文，使每次迭代时间从 24 s/step 降至 **11 s/step**（减少 54%），推理时单张图像生成时间从 4.6 s/img 降至 **2.2 s/img**（减少 52%）。与此同时，生成质量指标（PSNR、FID 等）仅有可忽略的下降。这表明模型在训练过程中已从几何上下文中学会了3D一致性先验，推理时即使不显式输出几何信息，仍能维持场景结构。

### 失败模式与局限性

Figure 9 展示了典型失败案例。模型在以下场景中表现受限：

1. **人体与复杂主体**：对人体、动物等非刚性主体的生成质量明显不足，可能源于训练数据中此类场景的几何与纹理多样性有限，导致模型难以建立准确的几何-外观映射。
2. **大幅视点外推**：在部分室外场景中，当新视角偏离输入视角过大时，边界区域纹理可能出现略微变暗的伪影，这与几何估计在远距离投影时的精度衰减有关。
3. **长距离往复轨迹的退化**：尽管 GaC 在 Table 2 中表现最优，但所有方法在前后往复长距离轨迹上的绝对指标仍较低，3D一致性退化问题尚未完全解决。这指向当前自回归序列建模在超长上下文记忆上的根本瓶颈。
4. **依赖预定义相机轨迹**：该方法需要预先计算的相机轨迹作为输入，尚不支持实时交互式场景探索。

### 公平性说明

所有基线方法均使用官方代码或开源实现进行评估，采用相同的数据集划分和评估协议。相机轨迹由数据集提供或按标准流程生成，确保对比的公平性。训练资源（8×H100）与部分基线相似或更高，已在文中明确报告。

## 定位与知识库关联

### 问题域定位：场景一致性视频生成的三条技术路线

GaC 面向的核心任务是**给定单张图像与相机轨迹，生成长序列场景视频**，其核心挑战在于维持跨视点的三维一致性。当前解决该问题的方法可归纳为三条主要技术路线：

1. **基于视频的生成方法（Video-based）**：直接利用视频扩散模型的强先验，将相机姿态作为条件注入生成过程。代表工作如 **VMem**（Li et al., ICCV 2025），这类方法无需显式三维表示，但缺乏对场景几何结构的显式约束，在长序列和往复轨迹上容易出现三维一致性问题，相机控制精度也相对有限。

2. **基于重建的生成方法（Reconstruction-based）**：通过迭代式几何估计、三维重建、新视角渲染和图像修复来生成新视图。代表工作包括 **ViewCrafter**（Yu et al., TPAMI 2025）、**GEN3C**（Ren et al., CVPR 2025）和 **Voyager**（Huang et al., TOG 2025）。这类方法引入显式三维表示（点云或深度图）来约束生成结果，但流水线中各模块独立运行且不可微分——几何估计器、反投影操作、渲染算子均为非可微分的黑箱——导致累积误差无法通过端到端优化消除。

3. **生成式新视角合成（Generative NVS）**：如 **Stable Virtual Camera**（Zhou et al., arXiv 2025），直接生成新视角图像而不依赖显式重建，但通常缺乏对场景全局三维结构的长期记忆。

GaC 的定位是**对重建路线的根本性改造**：保留显式几何约束带来的三维一致性优势，同时将非可微分的重建与绘制算子替换为可端到端训练的自回归生成模型，从而弥合两条路线之间的鸿沟。

### 核心因果机制：从累积误差到端到端优化

原始重建流水线可形式化为四个独立步骤：

- 几何估计：$G_i = \epsilon(I_i)$
- 反投影：$3D = \mathrm{Unproject}(I_i, G_i)$
- 渲染：$I_{i+1}' = \mathrm{Render}(3D, P_{i+1})$
- 修复：$I_{i+1} = \varrho(I_{i+1}', P_{i+1})$

其中 $\mathrm{Unproject}$ 和 $\mathrm{Render}$ 为非可微分算子，$\epsilon$ 和 $\varrho$ 为独立训练的子网络。这一架构的根本瓶颈在于：**几何估计的误差会通过不可微分的重建与渲染步骤传播并放大，后续的修复网络无法追溯修正上游误差**。在长序列生成中，这种累积误差导致远景视图出现几何失真和纹理漂移。

GaC 的核心洞察是将上述四个步骤统一为单个自回归生成模型：

$$\{G_i, I_{i+1}', I_{i+1}\} = \varrho(\{I_i, G_i, I_{i+1}'\}, P_{i+1})$$

这一统一化设计的关键因果效应是：**模型可以在生成新视图时，同时访问当前视图的几何信息作为上下文，并利用扩散模型的强先验隐式完成变形与修复**。端到端训练使得几何预测和视图合成的误差信号可以反向传播，从而减轻累积误差——这是 GaC 相较于所有重建类基线的结构性优势。

### 关键设计决策与消融证据

GaC 的三个关键设计决策均通过消融实验验证了其因果必要性：

**1. 几何上下文的必要性（Variant #1 vs #2 vs #3）**

Table 3 的消融实验对比了三种变体：
- Variant #1（几何作为上下文）：$\{G_i, I_{i+1}\} = \varrho(\{I_i, G_i\}, P_{i+1})$
- Variant #2（变形图像作为上下文）：模型输入为变形后的渲染图像而非几何信息
- Variant #3（无上下文）：$\{I_{i+1}\} = \varrho(I_i, P_{i+1})$，退化为纯视频生成

Variant #1 在所有指标（PSNR/SSIM/LPIPS/FID）上均显著优于其他变体，证明显式三维几何信息——而非简单的图像变形——是维持场景一致性的关键信号。Variant #3 由于完全丧失了三维约束，性能退化最为严重，这从反面验证了重建路线的核心价值。

**2. Camera Gated Attention 的任务解耦机制**

CGA 模块的设计动机源于一个微妙但关键的问题：**相机姿态在几何估计和视图合成两个子任务中扮演不同角色**——前者需要从当前视图推断场景结构（相机姿态间接相关），后者需要根据目标姿态生成对应视角的图像（相机姿态直接相关）。简单的 Plücker 射线编码相加无法区分这两种使用模式。

CGA 通过以下机制实现任务解耦：
- 将 Plücker 射线特征与自注意力查询相加后投影，生成残差查询 $Q_{res}$ 和门控矩阵 $Gate$
- 门控矩阵调制自注意力输出：$O = \mathrm{Linear}_3(O * \sigma(Gate))$

Table 5 的消融结果提供了强证据：CGA 不仅提升了图像质量（PSNR +0.44, FID -12.66），还显著降低了相机姿态误差（旋转误差 $R_{err}$ 和位移误差 $T_{err}$ 均有明显改善）。这表明 CGA 确实帮助模型学会了根据任务需求有选择地利用相机信息。

**3. 几何 Dropout 的效率-性能权衡**

几何上下文虽然必要，但输出几何信息会加倍序列长度。GaC 采用的几何 Dropout 策略——训练时随机丢弃几何上下文——在几乎不损失性能的前提下，将训练迭代时间从 24 s/step 降至 11 s/step（-54%），推理时间从 4.6 s/img 降至 2.2 s/img（-52%）（Table 6）。这一策略的巧妙之处在于：模型在训练阶段学会了利用几何信息进行三维推理，但在推理阶段可以通过 `<Image>` 提示跳过几何输出，仅生成 RGB 图像，从而兼顾了三维一致性和推理效率。

### 适用边界与局限

**1. 复杂主体的生成退化**

Figure 9 的失败案例暴露了模型对人体、动物等复杂主体的生成能力不足。这可能是训练数据（RealEstate10K 等场景数据集）中此类主体的几何和纹理多样性有限所致。与通用视频生成模型相比，GaC 的几何上下文机制在非刚体场景中尚未展现出明确的优势。

**2. 大视点外推的边界伪影**

在室外场景的大幅视点外推中，新视角图像的边界区域可能出现纹理略微变暗的伪影。这源于渲染过程中的遮挡区域缺乏足够的上下文信息，模型需要"幻觉"出不可见的内容，而几何上下文在此类区域的约束力有限。

**3. 往复长距离轨迹的一致性退化**

Table 2 显示，在前后往复（forth-and-back）相机轨迹上，所有方法（包括 GaC）的性能均有明显下降。虽然 GaC 仍保持最优，但这一场景暴露了当前方法的共同瓶颈：**长距离循环一致性要求模型维持全局三维记忆，而自回归生成框架中的误差累积仍然存在**。当相机回到先前访问过的位置时，生成的视图可能与历史视图不一致（如 Figure 1 最后一行的电脑屏幕在中间帧消失后又恢复，虽优于基线但仍非完美）。

**4. 对预计算相机轨迹的依赖**

GaC 需要预先给定相机轨迹，不支持实时交互式场景探索。这与基于 SLAM 的实时三维重建方法（如 3D Gaussian Splatting 相关方法）形成互补而非竞争关系。

### 开放问题与后续方向

1. **几何表示的语义扩展**：当前几何上下文为纯几何信息（深度图或点图），Table 4 显示深度图在 LPIPS 上略优于点图。未来可探索融合语义信息的几何表示（如 feature-embedded 3D Gaussians），以提升对复杂场景的建模能力。

2. **长距离三维记忆机制**：往复轨迹的性能退化表明，简单的自回归上下文窗口不足以维持全局一致性。需要设计更高效的上下文记忆策略，如可学习的场景表征缓存或检索增强生成。

3. **动态场景扩展**：当前方法假设场景为静态刚体。在非刚体或动态场景中，几何上下文的定义和有效性需要重新审视——可能需要引入运动场或时空几何表示。

4. **与实时系统的融合**：将 GaC 的端到端可微分生成能力与实时 SLAM 或 3DGS 系统结合，可能实现交互式场景探索中的高质量新视角生成。

5. **训练序列长度的规模化**：当前训练序列长度有限，更长的序列和更大的模型是否能进一步增强三维记忆能力，是一个值得探索的规模化问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/Geometry_as_context_Modulating_Explicit_3D_in_Scene_consistent_Video_Generation_to_Geometry_Context.pdf]]
