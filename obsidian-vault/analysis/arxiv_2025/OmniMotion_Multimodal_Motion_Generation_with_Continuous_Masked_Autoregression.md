---
title: "OmniMotion: Multimodal Motion Generation with Continuous Masked Autoregression"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: "paperPDFs/arxiv_2025/OmniMotion:_Multimodal_Motion_Generation_with_Continuous_Masked_Autoregression.pdf"
project_link: null
code_link: null
aliases:
- OmniMotion
tags:
- arxiv_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用保持时间顺序的因果注意力（causal attention）进行掩码自回归预测，使模型遵循运动序列的时序结构；引入门控线性注意（gated linear attention）自适应地强化关键动作帧并抑制冗余运动；RMSNorm 稳定异质多模态输入分布，缓解异常运动引起的梯度不稳定；DiT 扩散 transformer 将掩码自回归输出的丰富条件特征扩散...
primary_logic: 在连续运动空间中结合掩码自回归建模与 DiT 扩散条件合成，避免了离散量化损失，保留了时序建模能力，并通过因果注意力、门控机制和 RMSNorm 提升运动生成质量；多模态信号通过 AdaLN 与交叉注意力统一注入，实现一个框架内的高质量文本、语音、音乐驱动全身体运动生成。
claims:
- "在 HumanML3D 文本生成运动任务中，OmniMotion 在 Top-1 R-Precision 和 FID 上均大幅超越 MotionCraft 等最强基线（Top-1: 0.704 vs 0.590; FID: 4.838 vs 8.477）。"
- 消融实验证明，用因果注意力替代双向注意力并引入门控机制、RMSNorm 和 DiT，均能在文本到运动及多模态任务上带来一致且显著的性能提升。
- 在语音驱动手势（BEAT2）和音乐驱动舞蹈（FineDance）基准上，OmniMotion 超越了现有的多模态框架，验证了跨模态泛化能力。
- HumanML3D subset of Motion-X (Text-to-motion) 上 R-Precision Top-1 ↑ = 0.704 ± 0.003
---

# OmniMotion: Multimodal Motion Generation with Continuous Masked Autoregression

> [!tip] 核心洞察
> 在连续运动空间中结合掩码自回归建模与 DiT 扩散条件合成，避免了离散量化损失，保留了时序建模能力，并通过因果注意力、门控机制和 RMSNorm 提升运动生成质量；多模态信号通过 AdaLN 与交叉注意力统一注入，实现一个框架内的高质量文本、语音、音乐驱动全身体运动生成。

| 字段      | 内容                                                                                                                                         |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| 中文题名    | OmniMotion：连续掩码自回归的多模态人体动作生成                                                                                                               |
| 英文题名    | OmniMotion: Multimodal Motion Generation with Continuous Masked Autoregression                                                             |
| 会议/期刊   | arXiv 2025                                                                                                                                 |
| Links   | [paper](https://arxiv.org/abs/2510.14954)                                                                                                  |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method  | OmniMotion                                                                                                                                 |
| Dataset | HumanML3D subset of Motion-X, BEAT2, FineDance                                                                                             |

> [!tip] 效果简介
> - HumanML3D subset of Motion-X (Text-to-motion) 上，R-Precision Top-1 ↑ 0.704 ± 0.003 vs MotionCraft: 0.590 ± 0.003 (+0.114)；FID ↓ 4.838 ± 0.100 vs MotionCraft: 8.477 ± 0.102 (-3.639)。
> - BEAT2 (Speech-to-gesture) 上，FID_H ↓ 17.651 vs MotionCraft: 18.486 (-0.835)；Beat Align Score ↑ 8.377 vs MotionCraft: 8.098 (+0.279)。
> - FineDance (Music-to-dance) 上，FID_H ↓ 3.632 vs MotionCraft: 3.858 (-0.226)。

## 概要

人体动作生成领域长期存在两条技术路径的对立：基于离散量化的方法（如 VQ-VAE 结合自回归模型）不可避免地引入量化误差，损害运动精度；基于连续回归的方法虽避免了量化损失，却缺乏自回归或掩码建模的时序建模能力，生成质量受限。更关键的是，现有方法大多针对单一模态（文本、语音或音乐）设计，难以在一个统一框架内实现高质量的全身体运动生成。

OmniMotion 针对上述瓶颈提出了一种**连续掩码自回归**范式。其核心思想是：在连续运动空间中，通过保持时序因果性的掩码自回归 Transformer 进行运动建模，并以该 Transformer 输出的丰富条件特征驱动 DiT（Diffusion Transformer）扩散生成目标运动标记。这一设计同时规避了离散量化的精度损失，并保留了强大的时序建模能力。框架中引入的门控线性注意力与 RMSNorm 进一步增强了模型对关键动作帧的捕捉和训练稳定性，多模态信号则通过 AdaLN 与交叉注意力统一注入。

实验结果表明，OmniMotion 在文本、语音、音乐三个模态上均取得领先性能。在 HumanML3D 文本生成运动任务中，Top-1 R-Precision 达到 0.704，FID 降至 4.838，显著优于 MotionCraft 等最强基线；在 BEAT2 语音手势生成和 FineDance 音乐舞蹈生成基准上同样全面超越现有方法，验证了其跨模态泛化能力。消融实验进一步确认了因果注意力、门控机制、RMSNorm 和 DiT 扩散模块各自对性能的贡献。

人体动作生成是计算机视觉与图形学中的核心问题，其目标是根据文本、语音或音乐等控制信号生成自然、多样且语义对齐的全身体运动序列。近年来，该领域的研究主要沿着两条技术路径展开：**离散量化路径**与**连续回归路径**，但二者均存在难以调和的结构性缺陷。

离散量化方法以 VQ-VAE 为核心，将连续运动映射为离散码本索引，再通过自回归或掩码建模生成运动序列。代表性工作如 **T2M-GPT**（Zhang et al., 2023a）和 **Talkshow**（Yi et al., 2023）分别将这一范式应用于文本生成运动和语音生成手势。然而，离散量化过程引入了**不可恢复的量化误差**，在运动精度要求较高的场景（如手指动作、面部表情）中尤为突出，直接限制了生成质量的上限。

连续回归方法则直接在连续运动空间中进行建模，避免了量化损失。扩散模型是该路径的主流选择，**MDM**（Tevet et al., 2023）和 **MotionDiffuse**（Zhang et al., 2024b）在文本生成运动上取得了显著进展，**Edge**（Tseng et al., 2023）和 **FineDance**（Li et al., 2023a）则将扩散模型应用于音乐驱动舞蹈生成。但这些方法普遍缺乏自回归或掩码建模能力，难以在生成过程中充分利用运动序列的时序依赖关系，导致生成动作的自然度和连贯性偏低。

更为关键的瓶颈在于**多模态统一生成**。现有方法多为单一任务设计，文本、语音、音乐驱动的运动生成各自为政，难以在一个框架内实现高质量的全身体运动生成。**MotionCraft**（Bian et al., 2025）和 **MCM**（Ling et al., 2023）尝试通过扩散模型结合 ControlNet 实现多模态统一，但其条件注入机制较为粗粒度，跨模态泛化能力有限，在语音手势和音乐舞蹈等任务上的表现仍有较大提升空间。

上述困境的根本原因可归结为两点：其一，**离散量化与连续建模之间的取舍**——现有方法要么牺牲运动精度换取建模能力，要么反之；其二，**时序建模与多模态注入的耦合不足**——缺乏一种既能保持运动序列时间因果性，又能自适应地融合异质模态信号的统一架构。

针对这些缺口，OmniMotion 提出了一条新的技术路径：在连续运动空间中引入**掩码自回归建模**，通过因果注意力保持运动序列的时序结构，同时以 DiT 扩散 Transformer 替代简单的预测头，将掩码自回归的丰富条件特征扩散到目标标记。多模态信号则通过 AdaLN 与交叉注意力层统一注入，使得文本、语音、音乐驱动的高质量全身体运动生成得以在一个框架内实现。

## 核心方法与创新机理

OmniMotion 的核心创新在于将**连续掩码自回归建模**与**DiT 扩散条件合成**相结合，构建了一个统一的多模态全身体运动生成框架。这一设计直接回应了现有方法的两大瓶颈：离散量化的不可逆精度损失，以及连续回归方法时序建模能力的缺失。

### 从离散量化到连续自编码

现有主流方法（如 **T2M-GPT**，Zhang et al., 2023a）依赖 VQ-VAE 将运动序列离散化为有限码本中的标记，再通过自回归或掩码建模生成。这一路径不可避免地引入量化误差，限制了运动细节的保真度。OmniMotion 用**连续自编码器**替代 VQ-VAE，通过 1D 卷积与残差块将原始运动序列压缩为连续潜码（长度降至 1/4），以 L1 重建损失 $\mathcal{L}_{\mathrm{AE}} = \sum_t \| \hat{\mathbf{M}}_t - \mathbf{M}_t \|_1$ 进行训练。这一改变从源头消除了量化损失，使后续的掩码建模得以在连续空间中展开。

### 因果注意力与门控线性机制

视觉领域的掩码自回归（MAR）通常采用随机重排与双向注意力，但这破坏了人体运动天然的时序结构。OmniMotion 将注意力改为**保持时间顺序的因果注意力**，使模型在预测被掩码的运动标记时，只能看到过去的帧信息，遵循运动的因果生成逻辑。

在此基础上，模型引入**门控线性注意力**机制。标准注意力的输出被一个由 sigmoid 门控信号 $g = \mathrm{sigmoid}(g_o(x))$ 调制的因子缩放：$o = g \times \mathrm{Softmax}(\frac{Q K^T}{d_k}) V$。这一设计使模型能够自适应地强化关键动作帧的注意力权重，同时抑制冗余或异常运动帧的影响。配合 **RMSNorm** 对异质多模态输入分布进行稳定化，有效缓解了异常运动引起的梯度不稳定问题。

### DiT 扩散条件合成

掩码自回归 Transformer 的输出并非直接用于预测运动标记，而是作为**条件特征**注入 DiT（Diffusion Transformer）扩散模块。具体而言，掩码 Transformer 的输出特征 $\mathbf{z}^i$ 与扩散时间嵌入相加，形成条件信号：$\tilde{\mathbf{x}}_{t-1}^i \sim p(\tilde{\mathbf{x}}_{t-1}^i | \tilde{\mathbf{x}}_t^i, t + \mathbf{z}^i)$。DiT 在扩散过程中逐步去噪，生成目标运动标记。相比直接使用 MLP 预测头，DiT 提供了更强的生成能力与多模态泛化性。消融实验（Table 4）表明，将 MLP 头替换为 DiT 后，多模态生成的 FID 进一步降低。

### 统一的多模态注入

OmniMotion 通过 **AdaLN 与交叉注意力层**统一注入文本、语音、音乐三种模态信号。文本条件通过 AdaLN 调制掩码 Transformer 的归一化参数；语音与音乐信号则额外通过交叉注意力层与运动序列进行细粒度交互建模。在多模态微调阶段，模型冻结 DiT 参数，仅微调掩码 Transformer，在保持文本生成能力的同时高效适配新模态。这一设计使单一框架在文本驱动运动（HumanML3D）、语音驱动手势（BEAT2）和音乐驱动舞蹈（FineDance）三个基准上均超越了现有专用方法。

### 创新点总结

| 设计维度 | 现有方法 | OmniMotion 创新 |
|---------|---------|----------------|
| 运动编码 | 离散 VQ-VAE 量化 | 连续自编码器，无量化损失 |
| 注意力方式 | 双向注意力 / 纯自回归 | 因果注意力，保持时序结构 |
| 特征调制 | 标准注意力 + LayerNorm | 门控线性注意力 + RMSNorm |
| 生成头 | MLP 预测 / 简单扩散 | DiT 扩散条件合成 |
| 多模态注入 | 仅 AdaLN（文本） | AdaLN + 交叉注意力，统一三模态 |

这些创新点的协同效应在消融实验中得到验证：因果注意力替代双向注意力、引入门控机制、使用 RMSNorm、采用 DiT 扩散头，每一步替换均在文本到运动及多模态任务上带来一致且显著的性能提升（Table 4）。

OmniMotion 是一个面向多模态全身体运动生成的统一框架，其核心设计思想是：在连续运动空间中结合掩码自回归建模与 DiT 扩散条件合成，避免离散量化带来的精度损失，同时保留时序建模能力。框架整体分为三个主要阶段：

**阶段一：连续自编码器编码。** 原始运动序列首先通过一个连续自编码器（1D 卷积 + 残差块，下采样 4 倍）压缩为连续潜码，得到“连续运动标记”（continuous motion tokens）。与 VQ-VAE 的离散量化路径不同，连续编码避免了不可恢复的量化误差，为后续高精度运动生成奠定基础（Sec 3.2）。

**阶段二：掩码自回归 Transformer 的条件预测。** 连续运动标记按余弦调度被随机掩码，送入一个保持时间顺序的因果注意力 Transformer 中进行自回归预测。Transformer 内部引入门控线性注意力（gated linear attention）自适应强化关键动作帧、抑制冗余运动，同时使用 RMSNorm 稳定异质输入分布。条件信号（文本、语音、音乐）通过 AdaLN 注入。该阶段输出富含上下文的条件特征 $\mathbf{z}^i$，作为下一阶段扩散过程的条件（Sec 3.3）。

**阶段三：DiT 扩散合成目标标记。** 以掩码 Transformer 的输出特征 $\mathbf{z}^i$ 为条件，DiT（Diffusion Transformer）对目标运动标记执行扩散去噪过程。条件注入方式为 $\tilde{\mathbf{x}}_{t-1}^i \sim p(\tilde{\mathbf{x}}_{t-1}^i \mid \tilde{\mathbf{x}}_t^i, t + \mathbf{z}^i)$，即将时间嵌入与条件特征相加后引导扩散方向（Sec 3.4）。

**多模态扩展。** 在文本到运动模型 $M_{t2m}$ 训练完成后，框架通过冻结 DiT、仅微调掩码 Transformer 的方式扩展至语音和音乐模态。多模态信号（语音/音乐特征）通过 AdaLN 与新增的交叉注意力层显式注入，实现细粒度的跨模态交互（Sec 3.5）。

**推理流程。** 推理时，掩码 Transformer 首先生成条件特征，DiT 模块通过 DDIM 采样逐步去噪生成目标运动标记，最终由自编码器解码器重建为全身体运动序列。分类器自由引导（CFG）在最终线性层调节条件与无条件 Logits，进一步提升生成质量。

整个框架以文本作为共享条件锚点，通过统一的 SMPL-X 表示覆盖文本驱动运动、语音驱动手势和音乐驱动舞蹈三类任务，实现了单一框架内的多模态泛化。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2510_14954/figures/001_Figure_1.jpg]]
*Figure 1: We construct an omni motion framework with a continuous masked autoregressive motion transformer for multimodal whole-body motion modeling, including text-based, music-based, and speech-based motion generation*

OmniMotion 的生成流水线由四个关键模块串联构成：连续自编码器、掩码自回归 Transformer、DiT 扩散块和多模态交叉注意力层。各模块的设计目标与核心公式如下。

### 连续自编码器

传统方法采用 VQ‑VAE 将运动序列离散量化为有限码本索引，但量化操作引入的不可恢复误差会直接损害运动精度。OmniMotion 改用**连续自编码器**：由 1D 卷积与残差块组成，将原始运动序列压缩为连续潜码，长度降至 1/4，完全规避量化损失。训练目标为 L1 重建损失：

$$\mathcal{L}_{\mathrm{AE}} = \sum_t \| \hat{\mathbf{M}}_t - \mathbf{M}_t \|_1 \quad \text{(Eq 1)}$$

其中 $\mathbf{M}_t$ 为原始运动帧，$\hat{\mathbf{M}}_t$ 为重建运动帧。该模块为后续掩码建模提供高保真的连续运动标记。

### 掩码自回归 Transformer

在连续潜码空间上，OmniMotion 构建了**保持时间顺序的因果注意力**（causal attention）进行掩码自回归预测。与视觉 MAR 中常用的随机重排加双向注意力不同，因果注意力强制模型遵循运动序列的时序结构，使预测更符合人体运动的物理连续性。

训练时采用余弦遮罩率调度：

$$\gamma(\tau) = \cos\left(\frac{\pi \tau}{2}\right) \quad \text{(Eq 2)}$$

其中 $\tau \sim \mathcal{U}[0,1]$，控制每次迭代中被掩码的运动标记比例。

为增强模型对关键动作帧的感知并抑制冗余运动，Transformer 中引入了**门控线性注意力**机制：

$$o = g \times \mathrm{Softmax}\left(\frac{Q K^T}{d_k}\right) V, \quad g = \mathrm{sigmoid}(g_o(x)) \quad \text{(Eq 3)}$$

sigmoid 门控信号 $g$ 自适应地缩放标准注意力输出，实现对特征的选择性强化或抑制。同时，使用 **RMSNorm** 替代 LayerNorm 来稳定异质多模态输入分布，缓解异常运动引起的梯度不稳定。

### DiT 扩散块

掩码自回归 Transformer 的输出并非直接解码为运动标记，而是作为**条件特征**注入后续的扩散 Transformer（DiT）。具体而言，将 Transformer 的输出特征 $\mathbf{z}^i$ 与扩散时间嵌入相加，作为 DiT 去噪过程的条件：

$$\tilde{\mathbf{x}}_{t-1}^i \sim p(\tilde{\mathbf{x}}_{t-1}^i \mid \tilde{\mathbf{x}}_t^i, t + \mathbf{z}^i) \quad \text{(Eq 4)}$$

DiT 的训练目标为标准噪声预测损失：

$$\mathcal{L} = \mathbb{E}_{\epsilon, t} \| \epsilon - \epsilon_\theta(\tilde{\mathbf{x}}_t^i \mid t + \mathbf{z}^i) \| \quad \text{(Eq 5)}$$

推理时采用 DDIM 采样：

$$\mathbf{x}_{t-1}^i = \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{x}_t^i - \frac{\sqrt{1-\alpha_t}}{\sqrt{1-\bar{\alpha}_t}} \epsilon_\theta(\mathbf{x}_t^i \mid t + \mathbf{z}^i) \right) + \sigma_t \epsilon_t \quad \text{(Eq 6)}$$

同时应用分类器自由引导（CFG）：

$$l_f = (1 + \alpha) \cdot l_c - \alpha \cdot l_{uc} \quad \text{(Eq 7)}$$

其中 $l_c$ 和 $l_{uc}$ 分别为条件与无条件的最终线性层 Logits。

### 多模态交叉注意力

文本、语音、音乐等多模态信号通过 **AdaLN** 与**交叉注意力层**统一注入掩码 Transformer。交叉注意力层显式建模语音/音乐与运动序列的细粒度交互。多模态微调时，冻结 DiT 参数，仅更新掩码 Transformer 的交叉注意力与 AdaLN 权重，在保持文本生成运动能力的同时高效适配新模态。

## 实验与关键发现

### 主实验结果

OmniMotion 在文本、语音、音乐三个模态的运动生成基准上均取得了最优性能，验证了统一框架的跨模态泛化能力。

**文本生成运动。** 在 Motion-X 的 HumanML3D 子集上，OmniMotion 显著超越最强基线 **MotionCraft**（Bian et al., 2025）：Top-1 R-Precision 达到 0.704（MotionCraft 为 0.590，提升 19.3%），FID 降至 4.838（MotionCraft 为 8.477，改善 75.2%），如表 1 所示。此外，OmniMotion 在 Multimodal Distance、Diversity 等指标上也保持领先，表明其生成的全身运动既贴合文本语义，又保持合理的多样性。在原始 HumanML3D 基准上，OmniMotion 同样取得了具有竞争力的结果（Table 5），进一步验证了方法的鲁棒性。

**语音生成手势。** 在 BEAT2 数据集上，OmniMotion 在 FID_H（17.651 vs. MotionCraft 18.486）和 FID_B（25.923 vs. 26.132）上均优于现有方法，Beat Align Score 也从 8.098 提升至 8.377（Table 2）。这表明因果注意力与门控机制有效捕捉了语音节奏与手势动作之间的时序对齐关系。

**音乐生成舞蹈。** 在 FineDance 数据集上，OmniMotion 的 FID_H 降至 3.632（MotionCraft 为 3.858），FID_B 大幅改善至 71.930（MotionCraft 为 76.248），如表 3 所示。该结果说明框架能有效建模音乐节拍与舞蹈动作的长期依赖。

**混合训练设置。** 在 MotionCraft 提出的多模态混合训练设定下，OmniMotion 在文本、语音、音乐三个任务上均保持领先（Table 7-9），证明框架在多模态联合训练中不存在严重的模态间干扰。

### 消融实验

Table 4 系统消融了各核心组件的贡献，所有实验均在文本到运动及多模态任务上进行。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2510_14954/figures/008_Table_4.jpg]]
*Table 4: The ablation study of different model components*

**因果注意力的必要性。** 将因果注意力替换为视觉 MAR 中常用的双向注意力与随机重排策略后，模型性能显著下降。因果注意力强制模型遵循运动序列的时间顺序进行自回归预测，避免了双向注意力引入的未来信息泄露，从而生成更自然的运动过渡。

**DiT 扩散块的增益。** 将 DiT 替换为简单 MLP 预测头后，FID 明显上升。DiT 以掩码自回归 Transformer 的输出特征为条件进行扩散去噪，将丰富的上下文信息扩散到目标标记，显著提升了生成质量。

**门控线性注意力的作用。** 移除门控机制后，模型对关键动作帧的关注能力减弱，生成结果中出现更多冗余运动。门控信号 $g = \mathrm{sigmoid}(g_o(x))$ 自适应地调节注意力分布，使模型聚焦于语义重要的动作帧。

**RMSNorm 的稳定效果。** 异质多模态输入（文本、语音、音乐编码）具有不同的数值分布，RMSNorm 在此场景下比 LayerNorm 更有效地抑制了异常运动引起的梯度不稳定，对训练收敛和最终性能均有积极影响。

**交叉注意力的多模态注入。** 仅使用 AdaLN 注入多模态信号时，语音和音乐驱动任务的性能明显低于同时使用交叉注意力的配置。交叉注意力层显式建模了语音/音乐特征与运动序列之间的细粒度交互，对时序对齐要求高的任务尤为关键。

### 失败模式与局限性

尽管 OmniMotion 在多个基准上表现优异，分析揭示了以下不足：

1. **面部表情同步受限。** 语音驱动手势生成中，由于训练数据（Motion-X）的面部表情被平均化处理，模型在表情与语音内容的细粒度同步上落后于专用单模态方法（如 EMAGE）。这可能导致在需要精确唇形同步的应用场景中表现不佳。

2. **DiT 的计算开销。** DiT 模块虽然在生成质量上带来显著增益，但在训练和推理中引入了额外的前向/反向扩散步骤，增加了计算延迟。对于实时应用（如虚拟人驱动），该开销需要进一步优化。

3. **模态间数据不平衡。** 多模态训练依赖文本作为共享条件，缺乏文本标注的数据需生成伪标题，可能引入噪声。同时，不同模态的数据量差异可能导致模型偏向文本到运动任务，对次要模态的优化不够充分。

4. **未覆盖的模态。** 当前框架仅验证了文本、语音、音乐三个模态，对视频、生物信号等其他模态的泛化能力尚待验证。

### 定性结果

Figure 4 展示了文本驱动的全身运动生成结果，OmniMotion 能够根据复杂文本描述生成语义准确、动作自然的全身运动序列。Figure 5 和 Figure 6 分别展示了语音驱动和音乐驱动的生成结果，模型在保持节拍对齐的同时，生成了富有表现力的手势和舞蹈动作。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2510_14954/figures/005_Figure_4.jpg]]
*Figure 4: The qualitative results of text-driven motion generation*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2510_14954/figures/013_Figure_5.jpg]]
*Figure 5: The qualitative results of speech-driven motion generation*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2510_14954/figures/014_Figure_6.jpg]]
*Figure 6: The qualitative results of music-driven motion generation*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2510_14954/figures/009_Table_5.jpg]]
*Table 5: Results of text-to-motion on the original HumanML3D benchmark*

## 定位与知识库关联

### 1. 方法谱系：在离散量化与连续扩散之间的第三条路径

OmniMotion 的核心定位在于解决人体运动生成领域长期存在的“离散量化 vs. 连续回归”二元对立。理解其方法谱系，需要先厘清两类主流范式的根本分歧：

**离散量化路径**以 **T2M-GPT**（Zhang et al., 2023a）和 **Talkshow**（Yi et al., 2023）为代表。这类方法依赖 VQ-VAE 将连续运动序列映射为离散标记，再通过自回归 Transformer 逐帧预测。其优势在于继承了语言模型成熟的序列建模能力，但瓶颈同样致命：量化过程引入的不可恢复误差直接限制了运动精度上限，尤其对需要精细关节协调的全身体运动而言，这一损失在生成质量上表现为高频抖动和细节模糊。

**连续扩散路径**以 **MDM**（Tevet et al., 2023）、**MotionDiffuse**（Zhang et al., 2024b）和 **Edge**（Tseng et al., 2023）为代表。这类方法在原始运动空间直接进行扩散去噪，避免了量化损失，但代价是失去了自回归或掩码建模所具备的强时序约束能力——扩散模型的去噪过程本质上是并行而非因果的，难以显式建模运动序列中“前一帧决定后一帧”的物理因果链。

OmniMotion 试图在两者之间开辟第三条路径：**在连续运动空间中执行掩码自回归建模**。具体而言，它用连续自编码器（1D 卷积 + 残差块，下采样 4 倍）替代 VQ-VAE，将运动序列压缩为连续潜码，从而根除量化误差；同时，在潜码空间引入保持时间顺序的因果注意力（causal attention）进行掩码自回归预测，保留了时序建模能力。这一设计的关键洞察在于：**连续空间避免了信息损失，因果注意力保证了运动生成的物理合理性，二者的结合使得“高质量”与“强时序”不再互斥**。

与同样采用掩码策略的 **EMAGE**（Liu et al., 2024a）相比，OmniMotion 的根本差异在于 EMAGE 仍基于离散标记进行掩码建模，而 OmniMotion 在连续潜空间操作，因此天然规避了量化瓶颈。与 **MCM**（Ling et al., 2023）和 **MotionCraft**（Bian et al., 2025）等多模态框架相比，OmniMotion 的差异化优势在于其掩码自回归 Transformer 提供的强时序先验——MotionCraft 虽通过 ControlNet 实现多模态控制，但其核心仍是扩散模型，缺乏显式的因果时序约束。

### 2. 关键技术组件的定位与贡献分离

OmniMotion 的性能提升并非由单一模块驱动，而是四个相互协同的组件共同作用的结果。消融实验（Table 4）为每个组件的独立贡献提供了可验证的证据：

- **因果注意力替代双向注意力**：这是从视觉 MAR 范式迁移到运动生成时最关键的适配。运动序列具有严格的时序因果性——当前帧的生成应仅依赖历史帧，而非未来帧。Table 4 第 1/2 行对比表明，仅将双向注意力替换为因果注意力，即可显著提升运动自然度与 FID。这一改进的深层原因在于：双向注意力允许模型在训练时“偷看”未来帧，导致推理时的分布偏移；因果注意力则保证了训练与推理的一致性。

- **门控线性注意力**：标准自注意力对所有帧平等对待，但人体运动中存在大量冗余帧（如静止站立、匀速行走中的中间帧）。门控机制通过学习一个 sigmoid 门控信号 $g = \mathrm{sigmoid}(g_o(x))$，自适应地强化关键动作帧（如转身起始帧、手势峰值帧）的注意力权重，同时抑制冗余帧。Table 4 第 3/4 行的消融结果验证了这一机制对生成质量的提升，其本质是在注意力分布中引入了“稀疏性先验”。

- **RMSNorm 替代 LayerNorm**：在多模态场景下，文本、语音、音乐的嵌入分布差异巨大，LayerNorm 在异质输入下容易出现梯度不稳定。RMSNorm 通过仅对均方根进行归一化（而非同时中心化和缩放），在特征动态范围较大的场景中表现出更好的稳定性。这一改进虽看似微小，但在多模态联合训练中起到了关键的“稳定器”作用。

- **DiT 扩散块替代 MLP 预测头**：这是从“确定性回归”到“条件生成”的范式升级。MLP 预测头将掩码 Transformer 的输出直接映射为目标运动标记，本质上是一个确定性映射，缺乏对多模态分布的建模能力。DiT 则将 Transformer 输出特征 $\mathbf{z}^i$ 与时间嵌入相加作为扩散条件，通过迭代去噪生成目标标记，使得模型能够捕捉运动的多模态性（如同一文本描述可对应多种合理动作）。Table 4 第 2/3 行显示，DiT 的引入在多模态生成中进一步降低了 FID，验证了其强泛化能力。

### 3. 适用边界与失效模式

OmniMotion 的适用边界主要由以下约束定义：

**模态覆盖范围**：当前验证集中于文本、语音、音乐三个模态。对于视频驱动、生物信号（如 EMG、EEG）驱动等未见模态，模型的泛化能力尚未得到实验验证。多模态注入依赖 AdaLN 与交叉注意力层，其有效性建立在“条件信号可被编码为固定维度嵌入”的前提上——对于高维时空信号（如视频），这一假设可能不成立，需要额外的编码器设计。

**数据依赖与模态不平衡**：多模态训练以文本作为共享条件——语音和音乐驱动任务需要先将对应的语音/音乐信号与文本描述配对。对于缺乏文本标注的数据，模型依赖伪标题生成，这可能引入噪声。此外，不同模态的数据量差异可能导致模型偏向文本到运动任务，混合训练中对次要模态（如音乐到舞蹈）的优化可能不够充分。这一问题的直接证据来自语音手势生成任务：训练数据中面部表情被平均化处理，导致模型在表情同步上落后于专用单模态方法（如 **EMAGE**），这是数据层面而非方法层面的限制。

**计算开销**：DiT 模块虽然在生成质量上带来了显著增益，但在训练和推理中引入了额外的扩散步数开销。对于需要实时响应的应用场景（如虚拟主播的实时手势生成），DDIM 采样步数的压缩空间和推理延迟的优化仍是待解决的问题。

### 4. 局限与开放问题

**已知局限**：
1. **面部表情精度不足**：在 BEAT2 语音驱动手势任务中，由于训练数据的面部表情被平均化处理，OmniMotion 在表情同步指标上不及专用的单模态方法。这是数据预处理策略导致的系统性偏差，而非模型架构的根本缺陷。
2. **DiT 推理延迟**：扩散 Transformer 的迭代去噪过程在推理时引入了额外延迟，可能影响实时应用场景的部署。
3. **模态泛化未验证**：当前仅评估了文本、语音、音乐三个模态，对视频、生物信号等模态的泛化能力有待实验验证。
4. **伪标题噪声**：多模态训练依赖文本作为共享条件，缺乏文本标注的数据需生成伪标题，可能引入噪声并影响生成质量。

**开放问题**：
1. **多模态平衡机制**：在多模态联合训练中，如何设计动态的损失加权策略或梯度调控机制，以避免某一模态主导训练过程？当前方法对不同模态采用统一的训练目标，但不同模态的收敛速度和损失尺度可能存在显著差异。
2. **零样本模态组合**：模型能否在零样本场景下处理未见过的模态组合（如文本 + 音乐联合驱动）？这需要在条件注入层引入更灵活的模态融合机制，而非当前的简单拼接或加和。
3. **大规模语言模型融合**：将预训练的大语言模型（LLM）融入框架是否会进一步提升文本到运动的语义对齐能力？LLM 的文本理解能力可能帮助模型更好地解析复杂动作描述中的时序逻辑和空间关系。
4. **DiT 推理加速**：如何通过蒸馏、步数压缩或并行解码策略降低 DiT 模块的推理延迟，使其满足实时应用需求？这是从学术基准走向工业部署的关键瓶颈。

## 原文 PDF

![[paperPDFs/arxiv_2025/OmniMotion:_Multimodal_Motion_Generation_with_Continuous_Masked_Autoregression.pdf]]
