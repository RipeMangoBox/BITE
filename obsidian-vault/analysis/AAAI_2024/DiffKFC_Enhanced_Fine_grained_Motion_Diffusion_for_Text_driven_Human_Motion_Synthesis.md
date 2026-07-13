---
title: DiffKFC Enhanced Fine grained Motion Diffusion for Text driven Human Motion Synthesis
type: paper
paper_level: A
venue: AAAI
year: 2024
pdf_ref: paperPDFs/AAAI_2024/DiffKFC_Enhanced_Fine_grained_Motion_Diffusion_for_Text_driven_Human_Motion_Synthesis.pdf
project_link: null
code_link: null
aliases:
- DEFGMDTDHMS
tags:
- AAAI_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在训练阶段就将稀疏关键帧作为条件输入，并通过膨胀掩码注意力（DMA）模块逐步融合关键帧信息，使扩散模型能够学习多模态的细粒度协同，从而实现精确的运动控制。
primary_logic: 通过主动学习文本、关键帧和扩散目标帧之间的多模态关联，配合 DMA 的局部-全局注意力膨胀策略以及基于 DCT 的平滑先验，可以在仅 2% 关键帧的条件下生成高保真且符合动画师意图的运动，并附带纠正语义误解与容忍拼写错误的能力。
claims:
- 仅用 2% 的关键帧，在 HumanML3D 上的 FID 比现有最佳文本驱动运动扩散模型提升 41.6%。
- 膨胀掩码注意力模块通过仅允许有效 token 参与局部到全局的注意力，解决了稀疏关键帧信息被大量 token 淹没的问题。
- 基于 DCT 的平滑先验在推理时通过梯度修正均值，引导关键帧附近生成无缝过渡。
- 消融实验表明，将 DMA 替换为普通 Transformer 编码器会导致 FID 从 0.111 升至 0.477，验证了 DMA 的必要性。
---

# DiffKFC Enhanced Fine grained Motion Diffusion for Text driven Human Motion Synthesis

> [!tip] 核心洞察
> 通过主动学习文本、关键帧和扩散目标帧之间的多模态关联，配合 DMA 的局部-全局注意力膨胀策略以及基于 DCT 的平滑先验，可以在仅 2% 关键帧的条件下生成高保真且符合动画师意图的运动，并附带纠正语义误解与容忍拼写错误的能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | DiffKFC：面向文本驱动人体运动合成的增强细粒度运动扩散模型 |
| 英文题名 | DiffKFC Enhanced Fine grained Motion Diffusion for Text driven Human Motion Synthesis |
| 会议/期刊 | AAAI 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DiffKFC |
| Dataset | HumanML3D, KIT |

> [!tip] 效果简介
> - HumanML3D 上，FID 0.111 vs 0.434 (PhysDiff) (0.434→0.111 (-74.4%))；ADE 0.205 vs 0.736 (MDM‑fus) (0.736→0.205 (-0.531, -72.1%))。
> - KIT 上，FID 0.164 vs 0.404 (MLD) (0.404→0.164 (-59.4%))。

## 概要

**问题瓶颈**：现有文本驱动的人体运动扩散模型（如 **MDM** (Tevet et al., ICLR 2023)、**PhysDiff** (Yuan et al., ICCV 2023)、**MLD** (Chen et al., CVPR 2023)）仅提供语义层面的粗略控制，无法约束身体关节的详细姿势。当动画师试图在推理时直接注入稀疏关键帧以细化控制时，这些关键帧会被扩散模型视为噪声，导致生成的运动出现严重不连续或违背原始语义（图1中、底部对比）。

**核心方法**：本文提出 **DiffKFC**，一种面向文本驱动运动合成的条件扩散模型，通过 **关键帧协同** （KeyFrames Collaborated）实现文本与稀疏关键帧的双重细粒度控制。其核心设计包括：（1）在训练阶段即将干净的未加噪关键帧作为条件输入，使模型主动学习文本、关键帧与扩散目标帧之间的多模态协同；（2）定制 **膨胀掩码注意力**（Dilated Mask Attention, DMA）模块，通过逐步扩张有效 token 的局部到全局注意力，解决稀疏关键帧信息被大量 token 淹没的问题；（3）引入基于 **离散余弦变换**（DCT）的过渡平滑先验，在推理时通过分类器引导修正均值，确保关键帧附近生成无缝过渡。

**主要结果**：在 HumanML3D 和 KIT 数据集上，DiffKFC 仅需 **2% 的关键帧**即可实现显著性能提升——相比最优纯文本驱动方法，HumanML3D 上的 FID 从 0.434（PhysDiff）降至 0.111（**降低 74.4%**），KIT 上的 FID 从 0.404（MLD）降至 0.164（**降低 59.4%**）。此外，DiffKFC 展现出纠正语义误解与容忍文本拼写错误的能力（图5、图6），在保持语义保真度的同时精确满足动画师对姿势细节的期望。

**方法定位**：DiffKFC 属于 **条件运动扩散模型** 范畴，与 MDM、PhysDiff、MLD 等纯文本驱动方法形成互补。其关键区别在于将稀疏关键帧从推理时的后处理提升为训练时的原生条件，并通过 DMA 和 DCT 平滑先验克服稀疏控制信号带来的信息淹没与过渡不连续问题。该方法在方法谱系上可视为文本-运动扩散模型向 **多模态细粒度可控生成** 的延伸。

### 文本驱动运动合成的现状与瓶颈

文本驱动的人体运动合成旨在根据自然语言描述生成逼真的三维人体动作序列，在动画制作、游戏开发和虚拟现实等领域具有广泛应用。近年来，扩散模型在该领域取得了显著进展，代表性工作包括 **MDM**（Tevet et al., ICLR 2023）、**MLD**（Chen et al., CVPR 2023）、**MoFusion**（Dabral et al., CVPR 2023）和 **PhysDiff**（Yuan et al., ICCV 2023）等。这些方法将运动生成建模为从高斯噪声中逐步去噪的过程，能够产生多样化的运动序列。

然而，现有方法存在一个根本性瓶颈：**它们仅提供语义层面的粗略控制，无法约束身体关节的详细姿势**。具体而言，纯文本驱动的扩散模型对文本描述中的细微语义差异不够敏感，容易遗漏关键动作信息，甚至产生语义错误的运动。例如，当文本描述包含“短暂站立”这一短词时，模型可能完全忽略该词，生成连续游泳的动作（见 Figure 1 顶部示例）。

### 推理时关键帧注入的失败

动画师在实际工作中通常通过设定稀疏关键帧来精确控制运动的关键姿态。一个直观的思路是：在推理阶段将关键帧条件直接注入扩散模型。论文考察了两种典型的推理编辑策略：

- **MDM-inp（in-painting）**：在去噪过程中直接替换关键帧位置的值，导致运动不连续——生成的运动中会出现单帧突变的典型不真实现象。
- **MDM-grad（gradient guidance）**：通过梯度引导使生成结果靠近关键帧，但关键帧位置的实际姿态与给定关键帧存在明显偏差，无法达到期望的视觉效果。

这两种方法的共同失败根源在于：**稀疏关键帧在推理时被直接注入，会被扩散模型视为噪声，导致运动不连续或违背语义**。扩散模型在训练阶段从未见过稀疏关键帧与加噪目标帧的协同关系，因此无法在推理时正确处理这种条件信号。

### 核心动机：从被动注入到主动协同学习

上述分析揭示了一个关键因果机制：**问题的本质不在于关键帧信息本身，而在于模型是否在训练阶段就学会了文本、关键帧与目标运动之间的多模态协同关系**。

基于此洞察，DiffKFC 提出了一种范式的转变——从“推理时被动注入关键帧”转向“训练时主动学习双重控制”。具体而言：

- **训练阶段就将稀疏关键帧作为条件输入**，使扩散模型学会文本语义与细粒度姿态约束的联合表征；
- **设计专门的注意力机制处理关键帧稀疏性**，避免少量关键帧信息被大量目标帧 token 淹没；
- **引入过渡平滑先验**，确保关键帧附近生成无缝过渡，而非简单替换。

这种协同学习范式使得模型仅需 **2% 的关键帧**即可实现精确的运动控制，同时保留了文本驱动的语义灵活性，甚至具备纠正语义误解和容忍拼写错误的能力（见 Figure 5 和 Figure 6）。

## 核心方法与创新机理

DiffKFC 的核心创新在于将稀疏关键帧从“推理时外挂”升级为“训练时原生条件”，并围绕这一范式设计了三个紧密协同的机制，从而实现对文本驱动运动合成的细粒度控制。

**1. 训练阶段的关键帧条件化**

现有方法（如 **MDM**（Tevet et al., ICLR 2023）的 in-painting 或 gradient guidance 变体）仅在推理时尝试注入关键帧约束，但扩散模型会将这种直接注入视为噪声，导致运动不连续或语义违背。DiffKFC 的根本性改变在于：从训练初期就将**干净的、未加噪的静态关键帧** $\mathcal{X}_0^{kf}$ 作为条件输入，与加噪目标帧 $\mathcal{X}_t^{ta}$ 和文本条件 $\mathcal{C}$ 一起送入模型，主动学习文本语义、关键帧空间约束与目标运动之间的多模态协同。这一设计使得模型能够理解关键帧的“锚点”语义，而非将其视为需要去噪的异常信号。

**2. 膨胀掩码注意力（DMA）模块**

稀疏关键帧（仅占全序列的 2%–5%）在标准 Transformer 编码器中极易被大量目标帧 token 淹没。DiffKFC 提出的 DMA 模块通过**逐步扩张的掩码注意力协议**解决了这一瓶颈：在每一层 DMA 中，仅允许有效 token（关键帧位置及其已膨胀的邻居）参与注意力计算，无效 token 被显式屏蔽（注意力掩码 $M'_{ij} = -\infty$）。随着编码器层数加深，有效 token 的邻域按预设步长 $\{2, 2, 4, 4, 6, 6, 8, N\}$ 逐步膨胀，最终实现从局部到全局的信息融合。DMA 模块还移除了层归一化以降低无效 token 的影响权重，并用特征拼接替代残差连接，进一步强化有效信息的传递。消融实验提供了强证据：将 DMA 替换为普通 Transformer 编码器后，HumanML3D 上的 FID 从 **0.111 飙升至 0.477**；若采用统一编码器直接拼接关键帧与目标帧，FID 也恶化至 0.293，证实了区分干净关键帧与加噪目标的必要性。

**3. 基于 DCT 的过渡平滑先验**

关键帧与生成帧之间的过渡不连续是细粒度控制的常见副作用。DiffKFC 引入了一个基于离散余弦变换（DCT）的平滑先验：在推理阶段，利用 DCT 基对关键帧邻域的低频分量进行近似，定义过渡损失 $\mathcal{L}_{tr}$，并通过分类器引导的方式将损失梯度反向传播到逆向扩散过程的均值估计中，即 $\hat{\mu}_{\theta} = \mu_{\theta} + r \cdot \Sigma_{\theta} \nabla_{\mathcal{X}_t^{ta}} \mathcal{L}_{tr}$。这一设计无需额外训练，仅以极小的推理开销换取了关键帧附近的无缝过渡。消融实验表明，移除该先验后，关键帧过渡平滑度指标 K‑TranS 明显变差。

**三者协同的因果链条**：训练时原生关键帧条件化 → 模型理解关键帧的锚点语义；DMA 模块 → 防止稀疏信息被淹没，高效提取关键帧特征；DCT 平滑先验 → 保证生成帧向关键帧的无缝过渡。三者缺一不可，共同支撑了 DiffKFC 在仅 2% 关键帧条件下 FID 超越纯文本 SOTA 模型 41.6% 的核心性能，以及纠正语义误解、容忍拼写错误等涌现能力。

**DiffKFC** 是一个以文本描述与稀疏关键帧为双重条件的运动扩散模型，其核心设计目标是让扩散模型在训练阶段就主动学习文本、关键帧与目标运动之间的多模态协同，而非仅在推理时被动注入关键帧约束。整体架构由四个主要模块串联构成：**CLIP 文本编码器**、**扩散步嵌入**、**关键帧编码器（DMA 堆栈）** 与 **Transformer 解码器**，并在推理阶段引入基于 DCT 的平滑先验以保证关键帧附近的过渡质量。

### 输入与条件表示

给定一段长度为 $N$ 的目标运动序列 $\boldsymbol{\mathcal{X}} = \{ \mathbf{x}_1, \mathbf{x}_2, \cdots, \mathbf{x}_N \}$，模型将其按帧分割为两个互斥的部分：

- **关键帧** $\mathcal{X}_0^{kf} = \mathcal{X} \odot \mathbf{M}$：从原始序列中按二元掩码 $\mathbf{M}$ 采样的稀疏帧（默认比例为 5%，至少 1 帧），以干净、未加噪的形式直接送入关键帧编码器。
- **目标帧** $\mathcal{X}_t^{ta}$：完整序列在扩散时间步 $t$ 加噪后的版本，送入 Transformer 解码器。

文本描述 $\mathcal{C}$ 由预训练的 **CLIP 文本编码器** 投影为 token $\mathbf{y}_c$，扩散时间步 $t$ 则经嵌入层投影为 token $\mathbf{y}_t$。这两类 token 分别与关键帧编码器和解码器的输入 token 融合，使模型能够感知语义与噪声级别。

### 前向与逆向扩散

模型遵循标准去噪扩散概率模型（DDPM）框架。前向过程以固定方差调度 $\beta_t$ 逐步向目标帧注入高斯噪声：

$$q(\boldsymbol{\chi}_{t}^{ta} | \mathcal{X}_{t-1}^{ta}) = \mathcal{N}(\mathcal{X}_{t}^{ta}; \sqrt{1 - \beta_{t}} \mathcal{X}_{t-1}^{ta}, \beta_{t} \mathbf{I})$$

逆向过程则以干净关键帧和文本为条件，学习从纯噪声中逐步恢复目标帧：

$$p_{\theta}(\mathcal{X}_{t-1}^{ta} \vert \mathcal{X}_{t}^{ta}, \mathcal{X}_{0}^{kf}, \mathcal{C}) = \mathcal{N}(\mathcal{X}_{t-1}^{ta}; \mu_{\theta}(\mathcal{X}_{t}^{ta}, \mathcal{X}_{0}^{kf}, \mathcal{C}, t), \sigma_{t}^{2} \mathbf{I})$$

DiffKFC 采用 **X₀ 预测** 参数化，即网络 $\mathcal{X}_{\theta}$ 直接预测原始干净运动，而非预测噪声。训练损失在目标帧区域计算，通过掩码 $\mathbf{1} - \mathbf{M}$ 排除关键帧位置：

$$\mathcal{L}_{\text{simple}} = \mathbb{E}_{\chi_{0}^{ta}, t}\left[\| (\mathcal{X}_{0}^{ta} - \mathcal{X}_{\theta}(\mathcal{X}_{t}^{ta}, \mathcal{X}_{0}^{kf}, \mathcal{C}, t)) \odot (\mathbf{1} - \mathbf{M}) \|_{2}^{2}\right]$$

此外，模型还引入辅助运动学损失 $\mathcal{L}_{phy}$（包括关节位置、足部接触和速度约束），以提升生成运动的物理合理性。

### 关键帧编码器：DMA 堆栈

关键帧编码器是 DiffKFC 区别于普通条件扩散模型的核心组件。它由 8 层 **膨胀掩码注意力（Dilated Mask Attention, DMA）** 模块堆叠而成，膨胀步长依次为 $\{2, 2, 4, 4, 6, 6, 8, N\}$。DMA 的核心机制是：在每一层注意力中，仅允许被标记为“有效”的 token 参与注意力计算，而无效 token 被屏蔽（注意力掩码 $\mathbf{M}'_{ij} = -\infty$）。随着层数加深，有效 token 的邻域逐步膨胀，最终使全序列（除填充 token 外）均变为有效，实现从局部到全局的信息融合。

DMA 模块在结构上移除了层归一化以削弱无效 token 的影响，并用特征拼接替代残差连接：

$$\mathbf{Z}_k' = \mathsf{FC}([\mathsf{DMA}(\mathbf{Z}_{k-1}) \| \mathbf{Z}_{k-1}]), \quad \mathbf{Z}_k = \mathsf{MLP}(\mathbf{Z}_k')$$

这一设计确保了稀疏关键帧的精细信息不会被大量目标帧 token 淹没。

### Transformer 解码器与条件融合

解码器由 8 层标准 Transformer 层（自注意力 + 交叉注意力 + 前馈网络）构成，隐空间维度 512，8 个注意力头，前馈维度 1024。解码器输入为加噪目标帧 token，先通过自注意力建模帧间全局依赖，再通过交叉注意力从关键帧编码器的输出中提取精细控制信息，最终输出预测的干净运动 $\mathcal{X}_{\theta}$。

### 推理时的平滑先验

为缓解关键帧附近的运动不连续问题，DiffKFC 在推理阶段引入基于 **离散余弦变换（DCT）** 的过渡平滑先验。对于每个关键帧，取其前后各 $l$ 帧构成局部窗口，通过保留前 $m$ 个 DCT 基进行低通近似，定义过渡损失 $\mathcal{L}_{tr}$。该损失通过分类器引导的方式修正逆向扩散的均值：

$$\hat{\mu}_{\boldsymbol{\theta}}(\mathcal{X}_t^{ta}|\mathcal{X}_0^{kf}) = \mu_{\boldsymbol{\theta}}(\mathcal{X}_t^{ta}|\mathcal{X}_0^{kf}) + \boldsymbol{r} \cdot \Sigma_{\boldsymbol{\theta}}(\mathcal{X}_t^{ta}|\mathcal{X}_0^{kf}) \nabla_{\mathcal{X}_t^{ta}} \mathcal{L}_{tr}$$

其中 $\boldsymbol{r}$ 为引导强度。这一机制在无需重新训练的情况下，显著改善了关键帧过渡的平滑性。

### 训练策略

模型采用无分类器引导（classifier-free guidance）训练，通过在训练时随机丢弃文本和关键帧条件，使模型在推理时能够灵活调节细粒度控制的相对权重。扩散总步数 $T=1000$，使用余弦 $\beta$ 调度。

### 补充图表

![[assets/figures/papers/paper_list_l1816_DiffKFC_Enhanced_Fine_grained_Motion_Diffusion_for_Text_driven_Human_Mot/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed DiffKFC method. The encoder of DiffKFC is fed with clean keyframes*

### 3.1 条件扩散框架

DiffKFC 将人体运动合成建模为一个以稀疏关键帧和文本描述为联合条件的扩散生成过程。给定一段包含 $N$ 帧的目标运动序列 $\boldsymbol{\mathcal{X}} = \{ \mathbf{x}_1, \mathbf{x}_2, \cdots, \mathbf{x}_N \}$，通过二值掩码 $\mathbf{M}$ 提取稀疏关键帧 $\dot{\mathcal{X}}^{kf} = \mathcal{X} \odot \mathbf{M}$，剩余部分为目标帧 $\mathcal{X}^{ta}$。

**前向扩散过程**对目标帧施加固定方差调度 $\beta_t$ 的马尔可夫高斯噪声：

$$q(\boldsymbol{\chi}_{t}^{ta} | \mathcal{X}_{t-1}^{ta}) = \mathcal{N}(\mathcal{X}_{t}^{ta}; \sqrt{1 - \beta_{t}} \mathcal{X}_{t-1}^{ta}, \beta_{t} \mathbf{I}) \tag{1}$$

**逆向过程**以干净的静态关键帧 $\mathcal{X}_{0}^{kf}$ 和文本描述 $\mathcal{C}$ 为条件，逐步去噪重建目标运动：

$$p_{\theta}(\mathcal{X}_{t-1}^{ta} \vert \mathcal{X}_{t}^{ta}, \mathcal{X}_{0}^{kf}, \mathcal{C}) = \mathcal{N}(\mathcal{X}_{t-1}^{ta}; \mu_{\theta}(\mathcal{X}_{t}^{ta}, \mathcal{X}_{0}^{kf}, \mathcal{C}, t), \sigma_{t}^{2} \mathbf{I}) \tag{2}$$

模型采用 $\mathcal{X}_0$ 预测范式，训练损失使用掩码排除关键帧位置，仅对目标帧区域计算均方误差：

$$\mathcal{L}_{\text{simple}} = \mathbb{E}_{\chi_{0}^{ta}, t}\left[\| (\mathcal{X}_{0}^{ta} - \mathcal{X}_{\theta}(\mathcal{X}_{t}^{ta}, \mathcal{X}_{0}^{kf}, \mathcal{C}, t)) \odot (\mathbf{1} - \mathbf{M}) \|_{2}^{2}\right] \tag{3}$$

其中 $\mathcal{X}_{\theta}$ 为模型预测的干净运动，$\odot$ 表示逐元素乘法。

### 3.2 膨胀掩码注意力（DMA）

DMA 模块是 DiffKFC 处理稀疏关键帧的核心机制。其关键洞察在于：稀疏关键帧的信息量远小于密集目标帧，若直接让所有 token 参与全局自注意力，关键帧的有效信号会被大量噪声 token 淹没。DMA 通过**掩码注意力协议**和**逐步膨胀策略**解决这一问题。

**掩码注意力协议**：定义注意力掩码 $\mathbf{M}'$，其中 $\mathbf{M}'_{ij}=0$ 表示 token $j$ 对 token $i$ 有效（可参与注意力计算），$\mathbf{M}'_{ij}=-\infty$ 表示无效（被屏蔽）。注意力计算变为：

$$\operatorname{Att}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \operatorname{Softmax}\left(\frac{\mathbf{Q}\mathbf{K}^T + \mathbf{M}'}{\sqrt{d}}\right)\mathbf{V} \tag{7}$$

在有效 token 及其相邻无效 token 的范围内，注意力输出仅为有效 token 的加权和，无效 token 被完全忽略。

**逐步膨胀过程**：初始状态下，仅关键帧位置对应的 token 被标记为有效。每个 DMA 层按预设的膨胀步长（dilated step size）将有效 token 的邻域逐步激活为有效。编码器共 8 层，膨胀步长依次设为 $\{2, 2, 4, 4, 6, 6, 8, N\}$。经过逐层膨胀，最终除填充 token 外的全部序列 token 均变为有效，实现了从局部到全局的渐进式信息融合。

**DMA 块结构**：与传统 Transformer 层不同，DMA 块移除了层归一化以降低无效 token 的重要性，并用特征拼接替代残差连接。第 $k$ 个 DMA 块的输出为：

$$\mathbf{Z}_k' = \mathsf{FC}([\mathsf{DMA}(\mathbf{Z}_{k-1}) \| \mathbf{Z}_{k-1}]), \quad \mathbf{Z}_k = \mathsf{MLP}(\mathbf{Z}_k') \tag{8}$$

其中 $[\cdot \| \cdot]$ 表示通道维度的特征拼接，$\mathsf{FC}$ 为全连接层，$\mathsf{MLP}$ 为多层感知机。

### 3.3 基于 DCT 的过渡平滑先验

稀疏关键帧之间的过渡区域容易产生运动不连续。DiffKFC 利用离散余弦变换（DCT）定义时序平滑先验，在推理阶段通过分类器引导修正逆向扩散的均值。

**过渡损失**：对每个关键帧位置 $i$，取其前后各 $l$ 帧构成局部窗口 $\mathbf{G}_i$，通过保留前 $m$ 个 DCT 基底的近似重构 $\hat{\mathbf{G}}_i = \mathbf{G}_i \mathbf{D} \mathbf{D}^T$ 来度量平滑性。损失函数为：

$$\mathcal{L}_{tr} = \frac{1}{(2l+1) \cdot K} \sum_{i=1}^{K} \| \hat{\mathbf{G}}_{i} - \mathbf{G}_{i} \|_{2}^{2} \tag{4}$$

其中 $K$ 为关键帧数量，$\mathbf{D}$ 编码前 $m$ 个 DCT 基底。

**分类器引导**：在逆向扩散的每一步，利用过渡损失 $\mathcal{L}_{tr}$ 对 $\mathcal{X}_t^{ta}$ 的梯度修正均值 $\mu_{\theta}$：

$$\hat{\mu}_{\boldsymbol{\theta}}(\mathcal{X}_t^{ta}|\mathcal{X}_0^{kf}) = \mu_{\boldsymbol{\theta}}(\mathcal{X}_t^{ta}|\mathcal{X}_0^{kf}) + \boldsymbol{r} \cdot \Sigma_{\boldsymbol{\theta}}(\mathcal{X}_t^{ta}|\mathcal{X}_0^{kf}) \nabla_{\mathcal{X}_t^{ta}} \mathcal{L}_{tr}$$

其中 $\boldsymbol{r}$ 为引导强度，$\Sigma_{\boldsymbol{\theta}}$ 为逆向过程的方差。该机制引导生成的运动在关键帧附近形成无缝过渡，且无需额外训练。

### 3.4 整体架构与训练

DiffKFC 的整体架构（图 2）包含三个主要组件：

- **CLIP 文本编码器**：将文本描述 $\mathcal{C}$ 编码为文本 token $\mathbf{y}_c$。
- **扩散步嵌入**：将时间步 $t$ 投影为 token $\mathbf{y}_t$。
- **关键帧编码器（DMA 堆栈）**：接受干净的静态关键帧 $\mathcal{X}_0^{kf}$，通过 8 层 DMA 模块逐步融合稀疏信息，输出富含关键帧特征的 token。
- **Transformer 解码器**：由自注意力层（SA）、交叉注意力层（CA）和前馈网络（FFN）组成，共 8 层，8 个注意力头，隐空间维度 512，FFN 尺寸 1024。解码器对扩散目标帧 token 进行自注意力建模全局相关性，再通过交叉注意力融合关键帧编码器的输出，最终预测干净运动 $\mathcal{X}_{\theta}$。

训练采用无分类器引导（classifier-free guidance），使动画师在推理时可灵活调节细粒度控制的相对重要性。扩散总步数 $T=1000$，使用余弦 $\beta$ 调度。除 $\mathcal{L}_{\text{simple}}$ 外，还引入辅助运动学损失 $\mathcal{L}_{phy}$，包括关节位置、足部接触和速度约束，以提升物理合理性。

### 补充图表

![[assets/figures/papers/paper_list_l1816_DiffKFC_Enhanced_Fine_grained_Motion_Diffusion_for_Text_driven_Human_Mot/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of dilation strategy. Left: Mask attention protocol. In the range of valid tokens and their invalid neighbors, the output of attention is computed as the weighted sum of valid tokens while invalid tokens are ignored. Right: Dilation process. The invalid neighbors are automatically updated to be valid through each attention. Finally, the whole sequence becomes fully valid except padding tokens (no benefit to interact with diffused tokens)*

## 实验与关键发现

### 主实验结果

DiffKFC 在两个主流文本驱动运动合成基准上进行了评估，所有指标均运行 20 次并报告 95% 置信区间，确保统计稳定性。

**与纯文本驱动方法的对比**（Table 1）：在 HumanML3D 数据集上，DiffKFC 以 5% 的关键帧率取得了 **0.111** 的 FID，相比此前最优的纯文本驱动方法 **PhysDiff**（Yuan et al., ICCV 2023）的 0.434，实现了 **74.4% 的降幅**；在 KIT 数据集上，DiffKFC 的 FID 为 **0.164**，相比 **MLD**（Chen et al., CVPR 2023）的 0.404 降低了 **59.4%**。这一结果验证了细粒度关键帧条件对运动生成质量的显著提升。

**与推理时关键帧编辑方法的对比**（Table 2）：将 DiffKFC 与 MDM 的三种推理时关键帧使用策略——in-painting（MDM‑inp）、gradient guidance（MDM‑grad）和 fusion（MDM‑fus）——进行对比。在 HumanML3D 上，DiffKFC 的 ADE（Average Displacement Error）为 **0.205**，而 MDM‑fus 为 0.736，降幅达 **72.1%**。推理时编辑方法普遍面临关键帧位置运动不连续或关键帧约束失效的问题（见 Figure 4），而 DiffKFC 通过在训练阶段就学习关键帧与文本的协同，从根本上避免了这一缺陷。

### 消融实验

**网络架构消融**（Table 3）揭示了 DMA 模块的关键作用：

- **将 DMA 替换为普通 Transformer 编码器**（Vanilla Enc.）：FID 从 0.111 骤升至 **0.477**，Diversity 也从 8.756 降至 7.639。这表明普通自注意力无法有效提取稀疏关键帧信息，大量无效 token 淹没了关键帧特征。
- **采用统一编码器**（Unified Enc.）直接拼接关键帧与目标帧：FID 恶化至 **0.293**。原因在于统一编码无法区分干净关键帧与加噪目标帧，导致关键帧中的有用信息被噪声污染。

**关键帧率消融**（Table 4）展示了极稀疏关键帧的巨大作用：

- 关键帧率为 **0%**（纯文本驱动）时，FID 高达 **0.597**，验证了缺乏细粒度控制时模型性能显著下降。
- 仅引入 **2%** 的关键帧，FID 即降至 **0.253**，相比纯文本驱动提升 **57.6%**，证实了 DiffKFC 对极稀疏关键帧的高效利用能力。
- 关键帧率从 2% 增至 5% 和 10% 时，FID 进一步从 0.253 降至 0.111 和 0.071，呈单调改善趋势。

**过渡平滑先验消融**：移除过渡引导（w/o TG）后，关键帧过渡平滑度指标 **K‑TranS** 明显恶化，证实了基于 DCT 的平滑先验在保证关键帧间无缝过渡方面的必要性。

### 定性分析

**语义歧义消除**（Figure 4）：面对 "bending then walking" 与 "bending while walking" 的歧义描述，MDM 生成了符合前一种语义的运动，但明显不符合动画师意图（反映在 GT 关键帧中）。DiffKFC 不仅消除了歧义（识别出后一种语义），还生成了连贯且关键帧对齐的运动。相比之下，MDM‑inp 在行走运动中穿插单帧突然屈膝，产生典型的不真实现象；MDM‑grad 在关键帧位置生成的姿态与真实关键帧不同，表明其未能实现期望的视觉效果。

**语义错误纠正**（Figure 5）：当 MDM 因文本理解偏差生成完全错误的跳跃动作时，DiffKFC 通过关键帧引导纠正了这一误解，生成了符合预期的运动。

**拼写错误容忍**（Figure 6）：当文本描述中 "waves" 被误拼为 "walks" 或 "wavs" 时，MDM 无法提取正确信息并产生不同类型的失败，而 DiffKFC 能够容忍这两种拼写错误，仍生成正确的挥手动作。这归因于关键帧提供的细粒度视觉线索对文本噪声的补偿作用。

### 失败模式与局限性

DiffKFC 的主要局限在于推理速度略低于 SOTA 模型，原因包括额外的关键帧编码开销以及约 1000 步的逆向扩散过程。此外，尽管模型对拼写错误具有容忍性，但当文本描述与关键帧传达的语义产生根本性冲突时，模型的行为尚需进一步验证——当前分析仅展示了关键帧纠正文本误解的成功案例，但极端冲突场景下的生成质量与行为边界尚未被系统评估。

### 补充图表

![[assets/figures/papers/paper_list_l1816_DiffKFC_Enhanced_Fine_grained_Motion_Diffusion_for_Text_driven_Human_Mot/figures/004_Table_1.jpg]]
*Table 1: Results of baselines and DiffKFC (with keyframe rate 5%) on HumanML3D and KIT datasets. → means results are better when closer to that of real motion. We evaluate with 20 times of running for each metric, under 95% confidence interval. Bold indicates best results; “-” means unavailable results*

![[assets/figures/papers/paper_list_l1816_DiffKFC_Enhanced_Fine_grained_Motion_Diffusion_for_Text_driven_Human_Mot/figures/007_Table_3.jpg]]
*Table 3: Ablation studies of network architecture designs. ‘Enc.’ is the abbreviation of the keyframe encoder*

![[assets/figures/papers/paper_list_l1816_DiffKFC_Enhanced_Fine_grained_Motion_Diffusion_for_Text_driven_Human_Mot/figures/008_Table_4.jpg]]
*Table 4: Comparison of DiffKFC with different keyframe rates on HumanML3D dataset*

![[assets/figures/papers/paper_list_l1816_DiffKFC_Enhanced_Fine_grained_Motion_Diffusion_for_Text_driven_Human_Mot/figures/001_Figure_1.jpg]]
*Figure 1: Top: Current text-driven motion diffusion models, such as MDM (Tevet et al. 2023), may miss the short standing word and generate a total swimming motion. Middle: Directly imposing keyframe (golden) conditions at inference fails to solve this problem, and results in heavy discontinuities. Bottom: Our collaborative dual-level control paradigm produces the realistic motion towards animator expectations*

![[assets/figures/papers/paper_list_l1816_DiffKFC_Enhanced_Fine_grained_Motion_Diffusion_for_Text_driven_Human_Mot/figures/005_Figure_4.jpg]]
*Figure 4: The description is ambiguous on whether “bending then walking” or “bending while walking”. MDM generates motions that compliant to the former semantics, but obviously do not meet animator needs (reflected in GT keyframes). Our DiffKFC not only removes this ambiguity (identifying the latter semantics), but also generates coherent and keyframe-aligned motions. Visualization of naive inference-editing approaches are also given. MDM-inp yields a continuous walking motion interspersed with single-frame of sudden knee bending, which is a typical unrealistic phenomenon; while for MDM-grad, the generated pose at keyframe positions are different from real keyframes, indicating its failure towards de...*

![[assets/figures/papers/paper_list_l1816_DiffKFC_Enhanced_Fine_grained_Motion_Diffusion_for_Text_driven_Human_Mot/figures/009_Figure_5.jpg]]
*Figure 5: The motion generated by MDM is semantically incorrect (a total jump action), but our DiffKFC corrects this misunderstanding and generates the desired motion*

## 定位与知识库关联

### 1. 与纯文本驱动运动扩散模型的关系

DiffKFC 建立在文本驱动运动扩散模型的范式之上，但其核心不同在于引入了**稀疏关键帧作为第二控制模态**，从而突破了纯文本模型仅能提供语义级粗略控制的瓶颈。具体而言，本工作与以下基线形成对比与继承关系：

- **MDM** (Tevet et al., ICLR 2023)：作为文本驱动运动扩散的基础框架，MDM 仅依赖 CLIP 文本嵌入作为条件。DiffKFC 继承了其基于 Transformer 的扩散架构和 X₀ 预测范式，但关键差异在于：MDM 在推理时若强行注入关键帧（如 in-painting 或 gradient guidance），会将关键帧视为噪声扰动，导致运动不连续或语义违背（见 Figure 1 中间行）。DiffKFC 通过在**训练阶段**就将干净关键帧作为条件输入，从根本上解决了这一问题。

- **PhysDiff** (Yuan et al., ICCV 2023)：通过物理约束提升运动合理性，但本质上仍是纯文本驱动。在 HumanML3D 上 PhysDiff 的 FID 为 0.434，而 DiffKFC 在仅 5% 关键帧条件下达到 0.111，相对提升 74.4%（Table 1），表明细粒度空间控制比纯物理先验对生成质量的提升更为显著。

- **MLD** (Chen et al., CVPR 2023)：采用潜在扩散策略加速推理，在 KIT 上 FID 为 0.404。DiffKFC 在相同数据集上达到 0.164，相对提升 59.4%（Table 1）。

- **MoFusion** (Dabral et al., CVPR 2023)：基于扩散的运动合成框架，在 HumanML3D 上 FID 为 0.281，DiffKFC 同样显著超越。

**关键区分点**：上述所有基线均为纯文本驱动，而 DiffKFC 开创性地将关键帧控制从“推理时后处理”提升为“训练时主动学习”的**双重控制范式**，使模型能够学习文本语义与关键帧空间约束之间的多模态协同。

### 2. 与推理时关键帧编辑方法的对比

在 DiffKFC 之前，将关键帧施加于扩散模型的主流策略均为推理时操作，DiffKFC 通过 Table 2 的消融实验系统性地揭示了这些方法的根本缺陷：

- **MDM-inp (in-painting)**：在反向扩散的每一步用关键帧替换对应位置的预测值。问题在于关键帧与加噪目标帧之间存在分布失配，导致关键帧周围出现突然的姿态跳变（Figure 4 中 MDM-inp 出现“单帧膝盖弯曲”的典型不真实现象）。其 ADE 为 0.736。

- **MDM-grad (gradient guidance)**：通过梯度引导使生成结果逼近关键帧。但梯度信号在稀疏关键帧条件下过于微弱，无法使生成姿态精确对齐关键帧（Figure 4 中 MDM-grad 的关键帧位置姿态与真实关键帧不同）。其 ADE 为 0.605。

- **MDM-fus (fusion)**：将关键帧与目标帧拼接后输入统一模型。由于无法区分干净关键帧与加噪目标，FID 恶化至 0.293（Table 3 中 Unified Enc. 变体也证实了这一点）。

DiffKFC 的 ADE 为 0.205，相比 MDM-inp 降低 72.1%，这得益于两个关键设计：(1) **训练阶段的条件注入**使模型学会区分关键帧与目标帧的分布；(2) **DMA 模块**通过膨胀掩码注意力机制，使稀疏关键帧信息逐步扩散到整个序列，而非粗暴替换。

### 3. 膨胀掩码注意力（DMA）的独特定位

DMA 是 DiffKFC 的核心架构创新，其设计动机在于解决稀疏关键帧信息被大量目标帧 token 淹没的问题。与常规注意力机制的对比：

- **普通 Transformer 编码器**：将 DMA-stack 替换为普通 Transformer 编码器后，FID 从 0.111 升至 0.477（Table 3），验证了标准自注意力无法有效提取稀疏关键帧特征。

- **统一编码器（Unified Enc.）**：将关键帧与目标帧拼接后统一编码，FID 升至 0.293，原因在于加噪目标帧的噪声会污染干净关键帧的有用信息。

DMA 的核心机制——**逐步膨胀有效 token 范围**（Figure 3）——在注意力计算中使用掩码 M' 屏蔽无效 token（$M'_{ij} = -\infty$），仅允许有效 token 参与局部到全局的注意力。膨胀步长从 {2, 2, 4, 4, 6, 6, 8, N} 逐步增大，最终使全序列有效（除 padding token）。这种设计使关键帧信息能够以可控的节奏逐步传播到整个序列，避免了信息淹没和噪声污染。

### 4. 基于 DCT 的过渡平滑先验

DiffKFC 的过渡平滑先验利用离散余弦变换（DCT）定义关键帧过渡损失 $\mathcal{L}_{tr}$，并在推理时通过分类器引导调整逆向扩散的均值：

$$\hat{\mu}_{\theta}(\mathcal{X}_t^{ta}|\mathcal{X}_0^{kf}) = \mu_{\theta}(\mathcal{X}_t^{ta}|\mathcal{X}_0^{kf}) + r \cdot \Sigma_{\theta}(\mathcal{X}_t^{ta}|\mathcal{X}_0^{kf}) \nabla_{\mathcal{X}_t^{ta}} \mathcal{L}_{tr}$$

这一设计与扩散模型中常见的分类器引导方法（如 Dhariwal & Nichol, 2021）同源，但将其应用于**时间序列平滑性约束**是一个新颖的迁移。移除该先验后，关键帧过渡平滑度指标 K-TranS 明显变差（Table 3 消融），证实了其在保证关键帧之间无缝过渡方面的必要性。

### 5. 适用边界与局限

**适用边界**：
- DiffKFC 适用于需要精细空间控制的文本驱动运动合成场景，尤其适合动画师在给定稀疏关键帧约束下生成连贯运动的工作流。
- 关键帧比例极低（2% 即可显著提升质量），适合人机交互中的轻量级控制。
- 具备语义纠正能力（Figure 5）和拼写错误容忍能力（Figure 6），鲁棒性优于纯文本模型。

**已知局限**：
- **推理速度**：由于额外的关键帧编码和约 1,000 步逆向扩散过程，推理速度略低于 SOTA 模型（原文明确指出的 limitation）。这是方法在实用部署中的主要瓶颈。

**开放问题**：
- 论文指出未来可借助扩散模型的加速技术（采样步骤缩减、蒸馏等）提升推理速度，但如何在加速的同时保持关键帧对齐精度和过渡平滑性，仍是一个待验证的开放问题。
- 当前关键帧比例固定为 5%（训练设置），模型对动态变化的关键帧密度的泛化能力未充分探索。
- DMA 的膨胀步长设计目前依赖人工设定，是否存在自适应膨胀策略以进一步优化信息传播效率，值得进一步研究。

## 原文 PDF

![[paperPDFs/AAAI_2024/DiffKFC_Enhanced_Fine_grained_Motion_Diffusion_for_Text_driven_Human_Motion_Synthesis.pdf]]
