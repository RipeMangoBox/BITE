---
title: CMDM-HP
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CMDM_HP.pdf
project_link: null
code_link: null
aliases:
- CMDMC
- CH
tags:
- CVPR_2026
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在语义对齐的因果潜在空间中，采用因果扩散强制（Causal Diffusion Forcing）与帧级采样调度（FSS），通过独立的帧级噪声注入和因果自注意力实现有序逐帧去噪。
primary_logic: 在运动-语言对齐的因果潜在空间中，利用因果扩散变压器和帧级噪声调度，可以融合扩散模型的高质量生成与自回归模型的因果性，从而实现流式、低延迟的文本到运动生成。
claims:
- CMDM w/ FSS 在 HumanML3D 上取得了最高的 R-Precision (0.588) 和 CLIP-score (0.685)，并显著降低了 MM-Dist (2.620)。
- 消融实验表明，移除运动-语言对齐（C-VAE）导致 R-Top1 降至 0.575，替换为全序列扩散导致过渡 FID 升高至 1.96。
- CMDM 仅包含 114M 参数，使用 FSS 可实现最高 125 fps 的推理速度，较自回归模式加速 5–12 倍。
- HumanML3D 上 R-Precision Top1 = 0.588
---

# CMDM-HP

> [!tip] 核心洞察
> 在运动-语言对齐的因果潜在空间中，利用因果扩散变压器和帧级噪声调度，可以融合扩散模型的高质量生成与自回归模型的因果性，从而实现流式、低延迟的文本到运动生成。

| 字段      | 内容                                                                                                                                                                                                  |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 中文题名    | 面向自回归运动生成的因果运动扩散模型                                                                                                                                                                                  |
| 英文题名    | CMDM-HP                                                                                                                                                                                             |
| 会议/期刊   | CVPR 2026                                                                                                                                                                                          |
| Links | [paper](https://arxiv.org/abs/2602.22594) |
| Topic   | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method  | Causal Motion Diffusion Models (CMDM)                                                                                                                                                               |
| Dataset | HumanML3D                                                                                                                                                                                           |

> [!tip] 效果简介
> - HumanML3D 上，R-Precision Top1 0.588 vs 0.581 (SALAD) (+0.007)；CLIP-score 0.685 vs 0.671 (SALAD) (+0.014)；MM-Dist 2.620 vs 2.649 (SALAD) (-0.029)。

## 概要

### 问题瓶颈

文本驱动的人体运动生成是实现数字人、游戏和具身智能的核心技术，但现有方法面临一个根本性矛盾：**扩散模型**（如 MDM、MLD、SALAD 等）通过对全序列进行双向去噪获得高质量运动，却打破了时间因果关系，无法支持实时流式生成；**自回归模型**（如 MARDM+、T2M-GPT 等）虽能逐帧生成，却因误差累积导致运动质量下降和长序列不稳定。如何在保持扩散模型高质量生成的同时，实现严格的时间因果性和低延迟推理，是领域内尚未解决的瓶颈。

### 核心方法

本文提出 **Causal Motion Diffusion Models (CMDM)**，首次将扩散生成与因果自回归统一在单一框架中。其核心洞察是：在运动-语言对齐的因果潜在空间中，利用因果扩散强制与帧级噪声调度，可以融合扩散模型的高质量生成与自回归模型的因果性，实现流式、低延迟的文本到运动生成。CMDM 由三个关键组件构成：

- **MAC-VAE**：运动-语言对齐的因果变分自编码器，将运动序列编码到语义对齐的因果潜在空间，实现 4 倍时间下采样，并通过边缘余弦相似度和距离矩阵相似度损失与预训练运动-语言模型（Part-TMR）对齐。
- **Causal-DiT**：因果扩散变压器，采用因果自注意力、交叉注意力与文本条件（DistilBERT 词级嵌入），结合 AdaLN 与 ROPE 位置编码，在因果约束下执行帧级去噪。
- **Frame-Wise Sampling Scheduler (FSS)**：帧级采样调度器，通过因果不确定性调度实现高效推理——过去帧保持较低噪声，未来帧逐步去噪，有效缓解曝光偏差。

### 主要结果

在 **HumanML3D** 数据集上，CMDM 取得了最优的文本-运动语义对齐性能：R-Precision Top1 达 0.588，CLIP-score 达 0.685，MM-Dist 降至 2.620，FID 降至 0.068，全面超越 SALAD、StableMoFusion 等扩散基线以及 T2M-GPT、MoMask 等 VQ 基线。在长时域运动生成任务中，CMDM 在子序列质量和过渡平滑性上均显著优于现有方法。模型仅含 114M 参数，使用 FSS 可实现最高 125 fps 的推理速度，较自回归模式加速 5–12 倍。

### 方法定位

CMDM 属于**扩散生成与自回归生成融合**的新范式，通过因果扩散强制（Causal Diffusion Forcing）将扩散模型的迭代去噪能力赋予自回归框架。与现有方法相比，其关键区分在于：扩散范式从全序列双向扩散变为帧级因果扩散，潜在空间从标准 VAE 升级为运动-语言对齐的因果 VAE，推理采样从完整自回归扩散变为帧级不确定性调度。这一设计使 CMDM 兼具扩散模型的高质量与自回归模型的因果性和实时性，为流式运动生成和长序列合成提供了新的技术路径。



### 文本驱动运动生成的核心挑战

文本到运动生成（Text-to-Motion Generation）旨在根据自然语言描述生成逼真、语义对齐的三维人体运动序列。这一任务在动画制作、虚拟现实、人机交互等领域具有广泛应用前景。然而，现有方法面临一个根本性的困境：**高质量生成与时间因果性难以兼得**。

现有主流方法可归为两类范式：
- **扩散模型**（如 MDM、MLD、MotionLCM、StableMoFusion）：在完整运动序列上执行双向扩散去噪，所有帧共享相同的噪声水平。这类方法能够生成高质量运动，但破坏了时间因果关系——在生成当前帧时，模型可以“看到”未来帧的信息，导致无法实现流式、实时的运动生成。
- **自回归模型**（如 T2M-GPT、MoMask、MARDM+）：逐帧或逐片段生成运动序列，天然满足时间因果性。然而，自回归范式存在误差累积问题——早期帧的预测误差会逐步传播到后续帧，导致长序列生成不稳定、运动质量下降。

### 瓶颈分析：因果性与质量的对立

上述困境的核心瓶颈在于：**全序列双向扩散打破了时间因果结构，而纯自回归模型缺乏对不确定性的有效建模**。具体表现为：

1. **扩散方法的因果缺失**：传统扩散模型在训练和推理时，对所有帧施加统一的噪声水平，并使用双向注意力机制。这使得模型无法区分“过去”与“未来”，生成的每一帧都隐式依赖全局上下文，难以支持在线、低延迟的流式推理。

2. **自回归方法的误差累积**：自回归模型在生成当前帧时，仅依赖已生成帧的确定性表示。一旦某帧出现偏差，该偏差会作为条件输入影响后续所有帧的生成，导致运动质量随时间推移而恶化，尤其在长序列生成中表现明显。

3. **语义对齐的不足**：许多方法使用句子级文本嵌入（如 CLIP）作为全局条件，缺乏对细粒度语义（如动作的起止、过渡、节奏）的建模能力，导致生成的运动与文本描述之间存在语义漂移。

### 本文动机：融合扩散质量与自回归因果性

针对上述瓶颈，**Causal Motion Diffusion Models (CMDM)** 提出了一个统一的解决框架。其核心动机在于：**是否可以在保持扩散模型高质量生成能力的同时，引入严格的时间因果约束，从而实现流式、低延迟、语义对齐的运动生成？**

CMDM 的关键思路是在三个层面实现因果性与质量的融合：

- **因果潜在空间**：通过运动-语言对齐的因果变分自编码器（MAC-VAE），将运动序列编码到语义对齐的因果潜在空间中。每一帧的潜在表示仅依赖过去帧，同时通过运动-语言对齐损失确保语义一致性。

- **因果扩散强制**：在因果潜在空间中，为每一帧分配独立的噪声水平（而非统一的全局噪声），并使用因果自注意力机制。这使得模型能够以有序的、逐帧的方式执行扩散去噪，既保留了扩散模型的生成质量，又满足了时间因果性。

- **帧级采样调度**：在推理阶段，设计帧级采样调度器（FSS），利用因果不确定性机制——过去帧保持较低噪声水平以提供稳定条件，未来帧逐渐去噪以减少曝光偏差。这一设计显著降低了自回归生成中的误差累积问题。

通过上述设计，CMDM 仅需 114M 参数即可在 HumanML3D 数据集上取得最优的语义对齐精度（R-Precision Top1 0.588）和文本匹配度（CLIP-score 0.685），同时实现最高 125 fps 的推理速度，较传统自回归模式加速 5–12 倍。这一结果表明，扩散模型的高质量生成与自回归模型的因果性并非不可调和的对立面，而是可以通过精心设计的因果架构实现有机融合。



## 核心方法与创新机理

### 问题瓶颈：扩散质量与因果性的两难困境

文本到运动生成领域长期面临一个结构性矛盾：**全序列双向扩散模型**（如 MDM、MLD）能够生成高质量运动，但其全局去噪机制破坏了时间因果关系，无法支持流式、实时的逐帧生成；而**自回归模型**（如 T2M-GPT、MoMask）虽然满足因果性，却因误差累积导致长序列质量下降和不稳定。现有方法难以同时满足高质量、时间因果性和低延迟推理三大需求。

### 关键洞察：因果潜在空间中的扩散强制

CMDM 的核心洞察在于：**在运动-语言对齐的因果潜在空间中，利用帧级噪声调度与因果注意力机制，可以将扩散模型的高质量生成能力与自回归模型的因果性统一起来**。具体而言，CMDM 通过三个相互协同的模块实现这一目标：

1. **MAC-VAE**：构建语义对齐的因果潜在空间，将运动序列压缩 4 倍时间维度，并强制潜在特征与文本嵌入在语义上对齐；
2. **Causal-DiT**：在因果自注意力的约束下，对每帧独立注入噪声并逐帧去噪，确保当前帧仅依赖过去帧；
3. **帧级采样调度（FSS）**：在推理时利用因果不确定性，使过去帧保持较低噪声、未来帧逐步去噪，有效缓解曝光偏差。

### 相对基线的关键变革（Changed Slots）

| 设计维度 | 基线方法 | CMDM 创新 | 证据锚点 |
|---------|---------|----------|---------|
| **扩散范式** | 全序列双向扩散（所有帧共享同一噪声水平） | 因果扩散强制：每帧独立的噪声水平 $k_t$，配合因果自注意力实现有序去噪 | Section 3.2, Eq. 9-10 |
| **潜在空间** | 标准 VAE 或非因果 VAE | MAC-VAE：运动-语言对齐的因果 VAE，4× 时间下采样，引入边缘余弦相似度与距离矩阵相似度对齐损失 | Section 3.1, Eq. 2-3 |
| **推理采样** | 完整自回归扩散或全序列去噪 | 帧级采样调度（FSS）：利用因果不确定性矩阵 $K_{m,t}$，过去帧噪声低、未来帧噪声高，$L$ 控制不确定度尺度 | Section 3.4, Eq. 13 |
| **文本编码** | 句子级嵌入（如 CLIP） | 词级嵌入（DistilBERT），提供细粒度语义对齐 | Table 11 |

### 因果扩散强制的技术机理

传统扩散模型对全序列施加统一噪声水平，破坏了帧间因果依赖。CMDM 的**因果扩散强制**（Causal Diffusion Forcing）为每帧 $t$ 分配独立的扩散时间步 $k_t$：

$$\tilde{\mathbf{z}}_t^{k_t} = \sqrt{\bar{\alpha}_{k_t}} \mathbf{z}_t^{k_t} + \sqrt{1 - \bar{\alpha}_{k_t}} \boldsymbol{\epsilon}_t^{k_t}$$

训练时，模型在因果掩码下根据过去帧和文本条件预测当前帧噪声：

$$\mathcal{L}_{\mathrm{DF}} = \mathbb{E}_{k_t, \boldsymbol{\epsilon}_t^{k_t}} \Big[ \| \boldsymbol{\epsilon}_t^{k_t} - \boldsymbol{\epsilon}_\theta \big( \tilde{\mathbf{z}}_{\le t}, k_t, \mathbf{c} \big) \|_2^2 \Big]$$

这一设计迫使模型学习有序的去噪过程，为流式生成奠定基础。

### MAC-VAE：语义对齐的因果压缩

MAC-VAE 不仅通过因果卷积和因果 ResNet 块保证编码/解码的时序因果性（$\mathbf{z}_t = E_\phi(\mathbf{x}_{\le t})$），更关键的是引入了**运动-语言对齐损失**：

$$\mathcal{L}_{\mathrm{align}} = \mathcal{L}_{\mathrm{mcos}} + \mathcal{L}_{\mathrm{mdms}}$$

其中 $\mathcal{L}_{\mathrm{mcos}}$ 最小化投影运动特征与基础模型特征之间的余弦相似度差距，$\mathcal{L}_{\mathrm{mdms}}$ 通过匹配成对距离矩阵强制内部结构关系对齐。这一双重约束使潜在空间同时具备因果性和语义一致性，为后续扩散生成提供高质量表征基础。

### 帧级采样调度：缓解曝光偏差

自回归生成的核心痛点是曝光偏差——训练时使用真实帧，推理时使用生成帧，误差逐步累积。FSS 通过**因果不确定性调度矩阵** $K_{m,t}$ 解决此问题：在推理迭代中，过去帧保持较低噪声（甚至完全去噪），未来帧保持较高噪声。这使得模型在生成当前帧时，能够利用部分去噪的前序帧信息，而非完全依赖可能带有误差的生成帧，从而显著降低累积误差。

消融实验证实，FSS 的不确定度参数 $L=5$ 时获得最平滑的过渡效果（过渡 FID 1.64，AUJ 0.38），而采用全序列扩散替代因果扩散强制会导致过渡 FID 升至 1.96，AUJ 升高至 0.72（Table 4）。

### 效率优势

CMDM 仅含 114M 参数，FSS 推理模式可实现最高 **125 fps** 的生成速度，较自回归模式加速 **5–12 倍**（Section 4.3, B.4）。这一效率优势源于因果潜在空间的低维表征（64 维）和 FSS 的并行去噪能力，使 CMDM 成为首个同时满足高质量、因果性和实时性要求的文本到运动生成框架。



CMDM 提出了一种融合扩散模型生成质量与自回归模型因果性的统一范式，其核心矛盾在于：现有方法要么采用全序列双向扩散（破坏时间因果关系，无法实现流式生成），要么采用纯自回归模型（误差累积、生成不稳定）。CMDM 通过三个关键模块的系统协作来解决这一瓶颈。

**Pipeline 概览。** 给定文本描述 $\mathbf{c}$ 和目标运动序列长度 $T$，整体流程分为三个阶段：

1. **语义因果编码（MAC-VAE）**：将原始运动序列 $\mathbf{x}_{1:T}$ 编码到运动-语言对齐的因果潜在空间 $\mathbf{z}_{1:T/4}$，实现 4 倍时间下采样。编码器 $E_\phi$ 和解码器 $D_\psi$ 均采用因果卷积与因果 ResNet 块（左填充），严格保证每个潜在帧 $\mathbf{z}_t$ 仅依赖于过去帧 $\mathbf{x}_{\le t}$（Eq. 1）。潜在维度设为 64。

2. **因果扩散去噪（Causal-DiT）**：在潜在空间中执行帧级扩散去噪。训练时，每帧 $t$ 被注入独立的噪声水平 $k_t$（Eq. 9），模型通过因果自注意力机制仅基于过去帧 $\tilde{\mathbf{z}}_{\le t}$ 和文本条件 $\mathbf{c}$ 预测当前帧的噪声 $\boldsymbol{\epsilon}_t^{k_t}$（Eq. 10）。Causal-DiT 采用 AdaLN 嵌入帧级扩散时间步信息，结合 ROPE 相对位置编码以稳定长时域去噪。

3. **帧级采样推理（FSS）**：推理时，通过因果不确定性调度矩阵 $K_{m,t}$（Eq. 13）控制每帧在不同迭代步的噪声水平——过去帧保持较低噪声（提供稳定上下文），未来帧逐渐去噪。具体而言，每个后续帧从部分去噪的前序帧生成，利用因果不确定性机制减少自回归累积误差，最终将干净潜在序列 $\tilde{\mathbf{z}}_{1:T/4}^0$ 解码为运动序列 $\hat{\mathbf{x}}_{1:T}$。

**模块间的因果闭环。** MAC-VAE 为 Causal-DiT 提供了语义对齐且时间因果的压缩表示，使得扩散过程可以在低维空间高效运行；Causal-DiT 的因果自注意力与帧级噪声注入则确保了去噪过程的有序性；FSS 利用这一因果结构，通过可控的不确定度尺度 $L$ 在生成质量与推理延迟之间取得平衡。三者共同构成了从文本到运动的因果生成闭环，使得 CMDM 既能保持扩散模型的高质量输出，又能实现自回归式的流式推理（最高 125 fps，较自回归模式加速 5–12 倍）。

**与基线方法的关键差异。** 相较于全序列扩散方法（如 MDM、MLD），CMDM 将统一的噪声水平替换为帧级独立噪声，将双向注意力替换为因果自注意力，从根本上保证了时间因果性；相较于纯自回归方法（如 MARDM+），CMDM 通过 FSS 的因果不确定性调度显著缓解了曝光偏差问题，在长时域生成中实现了更平滑的过渡（过渡 FID 降至 1.64，AUJ 降至 0.38）。



CMDM 由三个核心模块构成：**MAC-VAE**（运动-语言对齐的因果变分自编码器）、**Causal-DiT**（因果扩散变压器）和 **FSS**（帧级采样调度器）。三者协同，在因果约束的潜在空间中实现帧级扩散去噪与流式推理。

### 3.1 MAC-VAE：因果编码与语义对齐

MAC-VAE 将长度为 $T$ 的运动序列编码到因果潜在空间，并实现 4 倍时间下采样（$T \rightarrow T/4$）。其核心因果约束为：

$$
\mathbf{z}_t = E_\phi(\mathbf{x}_{\le t}), \quad \hat{\mathbf{x}}_t = D_\psi(\mathbf{z}_{\le t}) \tag{1}
$$

每个潜在帧 $\mathbf{z}_t$ 和重建帧 $\hat{\mathbf{x}}_t$ 仅依赖于过去帧，严格保证时间因果性。编码器与解码器均采用 7 层因果卷积和 2 个因果 ResNet 块，配合左填充实现单向时序依赖。

MAC-VAE 的总损失函数为：

$$
\mathcal{L}_{\mathrm{MAC-VAE}} = \mathcal{L}_{\mathrm{rec}} + \beta D_{\mathrm{KL}}(q_\phi(\mathbf{z}|\mathbf{x})\|p(\mathbf{z})) + \lambda \mathcal{L}_{\mathrm{align}} \tag{2}
$$

其中，$\mathcal{L}_{\mathrm{align}}$ 是本文新引入的运动-语言对齐损失，由两部分构成：

$$
\mathcal{L}_{\mathrm{align}} = \mathcal{L}_{\mathrm{mcos}} + \mathcal{L}_{\mathrm{mdms}} \tag{3}
$$

- **边缘余弦相似度损失** $\mathcal{L}_{\mathrm{mcos}}$：最小化投影运动特征 $\mathbf{z}'_{ij}$ 与基础模型特征 $\mathbf{f}_{ij}$ 之间的余弦相似度差距，带边距 $m_1$：

$$
\mathcal{L}_{\mathrm{mcos}} = \frac{1}{N} \sum_{i,j} \mathrm{ReLU}\left(1 - m_1 - \frac{\mathbf{z}_{ij}' \cdot \mathbf{f}_{ij}}{\|\mathbf{z}_{ij}'\| \|\mathbf{f}_{ij}\|}\right)
$$

- **边缘距离矩阵相似度损失** $\mathcal{L}_{\mathrm{mdms}}$：通过匹配运动潜在表示与文本嵌入的成对距离矩阵，强制内部结构关系对齐，带边距 $m_2$：

$$
\mathcal{L}_{\mathrm{mdms}} = \frac{1}{N^2} \sum_{i,j} \mathrm{ReLU}\left(\left|\frac{\mathbf{z}_i \cdot \mathbf{z}_j}{\|\mathbf{z}_i\| \|\mathbf{z}_j\|} - \frac{\mathbf{f}_i \cdot \mathbf{f}_j}{\|\mathbf{f}_i\| \|\mathbf{f}_j\|}\right| - m_2\right)
$$

$\mathcal{L}_{\mathrm{mcos}}$ 优化局部特征的语义对齐，$\mathcal{L}_{\mathrm{mdms}}$ 则从全局结构层面约束潜在空间与语言空间的分布一致性。对齐监督信号来自预训练的运动-语言模型 Part-TMR，潜在维度设为 64。

### 3.2 Causal-DiT：因果扩散强制

Causal-DiT 在 MAC-VAE 的因果潜在空间中执行帧级扩散去噪。**因果扩散强制**（Causal Diffusion Forcing）的核心机制是：训练时为每一帧分配独立的噪声水平 $k_t$，注入帧级噪声：

$$
\tilde{\mathbf{z}}_t^{k_t} = \sqrt{\bar{\alpha}_{k_t}} \mathbf{z}_t^{k_t} + \sqrt{1 - \bar{\alpha}_{k_t}} \boldsymbol{\epsilon}_t^{k_t}, \quad \boldsymbol{\epsilon}_t^{k_t} \sim \mathcal{N}(0, I) \tag{9}
$$

训练目标是在因果掩码下，根据过去帧的潜在表示和文本条件 $\mathbf{c}$ 预测当前帧的噪声：

$$
\mathcal{L}_{\mathrm{DF}} = \mathbb{E}_{k_t, \boldsymbol{\epsilon}_t^{k_t}} \Big[ \| \boldsymbol{\epsilon}_t^{k_t} - \boldsymbol{\epsilon}_\theta \big( \tilde{\mathbf{z}}_{\le t}, k_t, \mathbf{c} \big) \|_2^2 \Big] \tag{10}
$$

其中 $\boldsymbol{\epsilon}_\theta(\tilde{\mathbf{z}}_{\le t}, k_t, \mathbf{c}) = \mathrm{CausalDiT}(\tilde{\mathbf{z}}_{\le t}, k_t, \mathbf{c})$。Causal-DiT 采用因果自注意力机制，确保每帧只能关注自身及之前的帧，同时通过交叉注意力融合词级文本嵌入（DistilBERT）。时间步信息通过 AdaLN 注入，长序列稳定性由 ROPE 相对位置编码保障。

### 3.3 FSS：帧级采样调度

推理阶段，FSS 利用**因果不确定性**机制实现高效流式生成。核心思想是：过去帧保持较低的噪声水平（接近干净），未来帧噪声较高，逐步去噪。其噪声调度矩阵为：

$$
K_{m,t} = \begin{bmatrix} 
K & K & K \\ 
K-L & K & K \\ 
K-2L & K-L & K \\ 
\vdots & \ddots & K-L \\ 
0 & \ldots & \vdots \\ 
0 & 0 & 0 
\end{bmatrix} \tag{13}
$$

其中 $K$ 为总扩散步数（设为 50），$L$ 为不确定度尺度（设为 2）。矩阵的行对应迭代步 $m$，列对应帧索引 $t$。每帧从部分去噪的前序帧中生成，有效缓解自回归的曝光偏差问题。消融实验表明，$L=5$ 时获得最平滑的过渡效果（过渡 FID 1.64，AUJ 0.38）。

生成过程可形式化为：

$$
\widetilde{\mathbf{z}}_t^{k_t-1} = G_{\theta}(\{\widetilde{\mathbf{z}}_{<t}^0, \widetilde{\mathbf{z}}_t^{k_t}\}, k_t, \mathbf{c}), \quad \hat{\mathbf{x}}_t = D_{\psi}(\widetilde{\mathbf{z}}_{\le t}^0)
$$

即利用前序帧的干净潜在表示 $\widetilde{\mathbf{z}}_{<t}^0$ 和当前帧的噪声潜在表示 $\widetilde{\mathbf{z}}_t^{k_t}$，预测下一帧的干净潜在，再通过解码器重建运动帧。

### 关键设计要点

- **因果性保证**：从 MAC-VAE 的因果编码器/解码器，到 Causal-DiT 的因果自注意力，再到 FSS 的有序去噪，全链路保证时间因果关系。
- **语义对齐**：MAC-VAE 的对齐损失同时约束局部特征（$\mathcal{L}_{\mathrm{mcos}}$）和全局结构（$\mathcal{L}_{\mathrm{mdms}}$），确保潜在空间与语言空间的一致性。
- **推理效率**：FSS 利用因果不确定性调度，使 CMDM 仅含 114M 参数即可实现最高 125 fps 的推理速度，较自回归模式加速 5–12 倍。



## 实验与关键发现

### 核心瓶颈与实验动机

现有文本到运动生成方法面临一个根本性两难：全序列双向扩散模型（如 MDM、MLD）虽然生成质量高，但打破时间因果关系，无法支持实时流式生成；自回归模型（如 T2M-GPT、MoMask）虽保持因果性，却受困于误差累积和训练不稳定。CMDM 的实验设计围绕一个核心假设展开——**在语义对齐的因果潜在空间中，通过帧级噪声调度可以同时获得扩散模型的高质量与自回归模型的因果性**。以下实验从标准文本到运动生成、长时域生成、消融分析和推理效率四个维度验证这一假设。

### 主实验结果

**HumanML3D 基准测试**（Table 1）显示，CMDM w/ FSS 在语义对齐与运动质量两个维度均达到最优。在语义精度指标上，R-Precision Top1 达到 0.588，CLIP-score 达到 0.685，分别超过此前最优的 SALAD（0.581 和 0.671）和 MoMask（0.574 和 0.673）。在运动质量指标上，FID 降至 0.068（SALAD 为 0.076），MM-Dist 降至 2.620（SALAD 为 2.649）。值得注意的是，CMDM 仅使用 114M 参数，远小于多数基线模型（如 MDM 的 250M+），却实现了全面的性能超越。

**SnapMoGen 数据集**（Table 2）进一步验证了方法的泛化能力，CMDM 在所有评估指标上均取得最优结果，表明因果扩散强制范式对不同运动表示和文本描述风格具有鲁棒性。

**关键对比**：与自回归方法 MARDM+ 相比，CMDM w/ FSS 的 FID 降低约 40%，这直接归因于帧级采样调度（FSS）对曝光偏差的抑制——过去帧保持部分噪声状态，为当前帧的去噪提供了更丰富的上下文不确定性信息，而非自回归方法中已确定性解码的“干净”帧。

### 长时域运动生成

长时域生成是检验因果性与时序一致性的关键场景。Table 3 报告了 HumanML3D 和 SnapMoGen 上的子序列质量与过渡平滑性指标。CMDM w/ FSS 在过渡 FID（Transition FID）上达到 1.64，显著优于全序列扩散基线（1.96）和标准自回归采样模式（CMDM w/ AR, 1.82）。过渡平滑性指标 AUJ（Area Under Jerk）为 0.38，表明相邻子序列间的运动加速度变化最小，时序衔接自然。

![[assets/figures/papers/CMDM-HP_Causal_Motion_Diffusion_Models_1abbad72e178/figures/004_Table_2.jpg]]
*Table 2: Results of text-to-motion generation on SnapMoGen. The average is reported over 10 runs with 95% confidence intervals. Table 3. Results of long-horizon motion generation on HumanML3D and SnapMoGen. The motion quality of each subsequence and the smoothness of each transition are evaluated*

定性结果（Figure 3–5）展示了 CMDM 生成的连续长序列——在“走路→转身→坐下”等多段文本描述的场景中，动作过渡无明显跳变或滑步伪影，而全序列扩散方法在段间边界常出现不自然的静止帧或速度突变。

![[assets/figures/papers/CMDM-HP_Causal_Motion_Diffusion_Models_1abbad72e178/figures/013_Figure.jpg]]

![[assets/figures/papers/CMDM-HP_Causal_Motion_Diffusion_Models_1abbad72e178/figures/014_Figure.jpg]]

![[assets/figures/papers/CMDM-HP_Causal_Motion_Diffusion_Models_1abbad72e178/figures/017_Figure.jpg]]

![[assets/figures/papers/CMDM-HP_Causal_Motion_Diffusion_Models_1abbad72e178/figures/018_Figure.jpg]]

![[assets/figures/papers/CMDM-HP_Causal_Motion_Diffusion_Models_1abbad72e178/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative results of long-horizon motion generation. Comparison between our CMDM and previous methods. The generated motion is continuous and seamless; for visualization purposes, we split each long sequence into shorter segments corresponding to their captions. Please refer to the videos in the supplementary materials for the complete motion sequences*

### 消融实验

Table 4 的系统消融揭示了三个关键设计的作用机制：

![[assets/figures/papers/CMDM-HP_Causal_Motion_Diffusion_Models_1abbad72e178/figures/006_Table_4.jpg]]
*Table 4: Ablation studies of CMDM*

**因果潜在空间（MAC-VAE）**：将 MAC-VAE 替换为标准 VAE（无因果约束、无运动-语言对齐）导致 FID 从 0.068 恶化至 0.107，过渡质量显著下降（AUJ 从 0.38 升至 0.52）。这表明因果编码不仅保证了时序一致性，还通过 4 倍时间下采样降低了扩散模型的建模难度。

**运动-语言对齐损失**：移除对齐损失（C-VAE w/o MA）使 R-Top1 从 0.588 降至 0.575，CLIP-score 同步下降。对齐损失通过边缘余弦相似度和距离矩阵相似度两个约束，在潜在空间中建立了运动帧与词级文本嵌入的细粒度对应关系，这是语义精度提升的直接来源。

**因果扩散强制 vs. 全序列扩散**：将因果扩散强制替换为全序列双向扩散（所有帧使用相同噪声水平），过渡 FID 急剧升高至 1.96，AUJ 升至 0.72。这一对比直接证明了**帧级独立噪声注入与因果自注意力**是融合扩散质量与因果性的关键机制——全序列扩散虽然单帧质量高，但缺乏时间因果约束，导致段间过渡不自然。

**FSS 不确定度参数 L**：L=5 时获得最优过渡平滑性（过渡 FID 1.64，AUJ 0.38），相比 L=2（过渡 FID 1.72）和 L=10（过渡 FID 1.68）更优。这一参数控制过去帧保留的噪声水平：L 过小则退化为近似自回归模式，L 过大则噪声过多、语义信息不足。

### 推理效率分析

CMDM 的推理效率优势来自两个层面。在模型层面，114M 的轻量参数使单步推理延迟极低。在采样层面，FSS 利用因果不确定性实现了帧级并行去噪——过去帧保持较低噪声、未来帧逐渐去噪，相比标准自回归逐帧采样（K=50 步/帧）加速 5–12 倍，最高可达 125 fps（Section 4.3, B.4）。这一加速比使得 CMDM 成为首个能够实时流式生成高质量运动的扩散模型。

### 失败模式与局限性

尽管整体性能优异，实验中也观察到以下边界情况：

1. **极长序列的时序漂移**：当生成序列超过 2 分钟（约 3000+ 帧）时，偶有轻微的关节位置漂移，表现为脚部与地面的接触约束逐渐松弛。这源于因果自注意力在极长上下文中的注意力衰减，需要手动验证是否可通过位置编码改进缓解。

2. **抽象文本的语义偏差**：对于高度抽象的描述（如“像风一样自由地舞动”），MAC-VAE 的对齐损失依赖预训练的 Part-TMR 模型，可能产生语义偏差，导致生成的运动与文本意图不完全匹配。

3. **多角色场景缺失**：当前框架仅支持单人运动生成，实验未涉及多人交互或协同运动场景。

### 补充实验要点

Table 5（BABEL 数据集）验证了 CMDM 在长时域动作捕捉数据上的泛化能力。Table 7（MTT 数据集）展示了 CMDM 在组合运动生成任务上的优势——通过因果逐段生成，无需额外组合训练即可实现多段文本描述的顺序合成。Table 8–11 的系统消融进一步确认了潜在维度 64、4 倍下采样、DistilBERT 文本编码器和 (H=8, L=6, D=512) 的 Causal-DiT 配置为最优选择。

![[assets/figures/papers/CMDM-HP_Causal_Motion_Diffusion_Models_1abbad72e178/figures/007_Table_5.jpg]]
*Table 5: Comparison of long-horizon motion generation on BABEL. Subsequence metrics evaluate motion quality and diversity within segments, while transition metrics assess temporal continuity and smoothness between segments. Table 6. Results of text-to-motion generation on HumanML3D without redundant features. The average is reported over 10 runs with 95% confidence intervals. Bold indicates the best result, and underline denotes the second-best result*

![[assets/figures/papers/CMDM-HP_Causal_Motion_Diffusion_Models_1abbad72e178/figures/008_Table_7.jpg]]
*Table 7: Comparison with prior compositional motion generation methods on the Multi-track timeline (MTT) dataset [32]*

### 补充图表

![[assets/figures/papers/CMDM-HP_Causal_Motion_Diffusion_Models_1abbad72e178/figures/009_Table_9.jpg]]
*Table 9: Comparison of motion-language models in MAC-VAE on HumanML3D. MPJPE is measured in millimeters*

![[assets/figures/papers/CMDM-HP_Causal_Motion_Diffusion_Models_1abbad72e178/figures/003_Table_1.jpg]]
*Table 1: Results of text-to-motion generation on HumanML3D. The average is reported over 10 runs with 95% confidence intervals. Methods marked with † were originally implemented with different motion representations and have been re-trained using our codebase to ensure a fair comparison. Bold indicates the best result, while underline denotes the second-best result*

![[assets/figures/papers/CMDM-HP_Causal_Motion_Diffusion_Models_1abbad72e178/figures/010_Table_10.jpg]]
*Table 10: Comparison of model sizes on HumanML3D. The notation (H, L, D) denotes the number of attention heads H, layers L, and hidden dimension D. Table 11. Comparison of text encoders on HumanML3D*



## 定位与知识库关联

### 1. 问题定位：扩散与自回归的范式裂隙

文本到运动生成领域长期存在两条技术路线的张力：

- **全序列扩散模型**（如 **MDM**、**MLD**、**MotionLCM**、**StableMoFusion**）通过双向注意力在完整序列上同时去噪，生成质量高，但破坏了时间因果关系，无法实现流式推理。
- **自回归模型**（如 **T2M-GPT**、**MoMask**、**MARDM+**）逐帧预测，天然支持因果生成，但面临误差累积和曝光偏差问题，长序列稳定性不足。

CMDM 的核心定位是**在因果约束下融合扩散模型的高质量生成与自回归模型的因果性**，从而同时满足三个需求：语义保真度、时间因果性、低延迟推理。

### 2. 与基线方法的关键差异

#### 2.1 扩散范式的根本转变

| 维度 | 全序列扩散基线 | CMDM |
|------|---------------|------|
| 噪声注入 | 所有帧共享同一噪声水平 | 每帧独立的帧级噪声 $k_t$（Eq. 9） |
| 注意力机制 | 双向自注意力 | 因果自注意力（仅依赖过去帧） |
| 去噪方式 | 全序列同步去噪 | 因果扩散强制：有序逐帧去噪（Eq. 10） |
| 推理模式 | 批量生成完整序列 | 流式生成，支持实时输出 |

这一转变使得 CMDM 在推理时可选择两种模式：标准自回归采样（CMDM w/ AR）和帧级采样调度（CMDM w/ FSS）。FSS 通过因果不确定性机制，让后续帧从部分去噪的前序帧生成，显著降低了自回归的累积误差。

#### 2.2 潜在空间的对齐增强

与标准 VAE（如 **MLD** 采用的潜在扩散）不同，CMDM 的 MAC-VAE 引入两个关键改进：
- **因果编码器/解码器**：7 层因果卷积 + 2 个因果 ResNet 块，确保 $\mathbf{z}_t = E_\phi(\mathbf{x}_{\le t})$（Eq. 1），实现严格的时间因果性。
- **运动-语言对齐损失**：$\mathcal{L}_{\text{align}} = \mathcal{L}_{\text{mcos}} + \mathcal{L}_{\text{mdms}}$（Eq. 3），同时优化局部特征余弦相似度和全局结构距离矩阵，将语义信息注入潜在空间。

消融实验（Table 4）表明，移除对齐损失使 R-Top1 从 0.588 降至 0.575；替换为标准 VAE 使 FID 从 0.068 恶化至 0.107。

#### 2.3 文本编码的细粒度化

CMDM 采用 **DistilBERT** 提取词级嵌入，而非基线常用的句子级 CLIP 嵌入。Table 11 的消融显示，词级编码在 R-Precision 和语义对齐上均优于句子级方案，为细粒度运动-语言对齐提供了更丰富的条件信号。

### 3. 适用边界与能力定位

**强适用场景**：
- 流式文本到运动生成（实时交互、游戏引擎驱动）
- 长时域运动合成（多段文本描述拼接为连续运动序列）
- 对推理延迟敏感的应用（FSS 模式下最高 125 fps，较自回归模式加速 5–12 倍）

**约束与局限**：
- **依赖预训练对齐模型**：MAC-VAE 使用 Part-TMR 提供语义监督，对高度抽象或模糊的文本描述可能产生语义偏差。
- **极长序列的时序伪影**：在数分钟以上的序列上偶有轻微抖动，限制了超长视频生成场景。
- **单角色限制**：当前框架仅支持单人运动，尚未扩展到多角色或交互场景。
- **训练资源需求**：尽管推理效率高，训练仍需大量计算资源。

### 4. 开放问题与后续方向

1. **曝光偏差的进一步缓解**：FSS 已显著降低累积误差，但在极长序列（数百帧以上）上仍有改进空间。是否可引入重排序或回看机制？
2. **跨模态泛化**：因果扩散强制的帧级噪声调度和因果自注意力机制是否可推广到语音合成、视频生成等顺序数据任务？
3. **多角色交互扩展**：如何将 CMDM 的因果框架扩展到多人协同运动生成，处理角色间的时空依赖？
4. **基础模型替代**：能否利用大语言模型（LLM）直接提供语义监督，替代微调的对齐模块，进一步简化训练流程并提升泛化能力？

### 5. 知识库贡献总结

CMDM 的核心知识贡献在于**因果扩散强制**这一训练-推理范式：在训练时对每帧施加独立噪声并因果去噪，在推理时通过帧级采样调度利用因果不确定性实现高效流式生成。该范式为顺序数据生成提供了一种新的融合思路——在保持扩散模型高质量的同时获得自回归模型的因果性，而非在两者之间做取舍。



## 原文 PDF

![[paperPDFs/CVPR_2026/CMDM_HP.pdf]]
