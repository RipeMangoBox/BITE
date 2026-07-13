---
title: "UniMotion: Unifying 3D Human Motion Synthesis and Understanding"
type: paper
paper_level: A
venue: 3DV
year: 2025
pdf_ref: paperPDFs/3DV_2025/UniMotion_Unifying_3D_Human_Motion_Synthesis_and_Understanding.pdf
code_link: null
project_link: https://coral79.github.io/uni-motion
aliases:
- UniMotion
tags:
- 3DV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过将帧级文本与运动在时间维度上对齐并引入独立的多模态扩散过程（可分别控制运动和文本的扩散时间步），模型能够统一采样多种条件分布与联合分布。"
primary_logic: "时间对齐的多模态联合扩散使单一Transformer模型同时具备运动合成和帧级运动理解的能力，支持从无、部分或全部模态条件中进行灵活采样，从而实现层级文本控制、运动文本联合生成、运动编辑等新任务。"
claims:
- "在帧级文本到运动任务上，UniMotion 显著优于所有基线模型，尤其在结合序列级和帧级文本（f+s）时，各项语义和真实性指标均大幅提升。"
- "多模态联合训练带来了跨模态泛化能力：即使在推理时仅使用帧级文本，利用多数据集（HML+BABEL）训练的模型也明显优于仅在 BABEL 上训练的模型。"
- "与 backbone MDM 相比，引入多模态扩散和联合训练后，序列级文本到运动生成质量大幅提高。"
- "HumanML3D/BABEL 帧级文本到运动生成（Per-seq Realism） 上 FID_tmr++ ↓ = 0.133 ± 0.004 (Ours HML-BABEL f+s)"
---

# UniMotion: Unifying 3D Human Motion Synthesis and Understanding

> [!tip] 核心洞察
> 时间对齐的多模态联合扩散使单一Transformer模型同时具备运动合成和帧级运动理解的能力，支持从无、部分或全部模态条件中进行灵活采样，从而实现层级文本控制、运动文本联合生成、运动编辑等新任务。

| 字段 | 内容 |
| ------- | ----------------------------------------------------------------------------------------------------------------- |
| 中文题名 | UniMotion：统一三维人体运动合成与理解 |
| 英文题名 | UniMotion: Unifying 3D Human Motion Synthesis and Understanding |
| 会议/期刊 | 3DV 2025 |
| Links | [paper](https://coral79.github.io/uni-motion/paper/unimotion.pdf) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | UniMotion |
| Dataset | HumanML3D/BABEL 帧级文本到运动生成（Per-seq Realism）, 序列级文本到运动生成（Ablation vs MDM）, 帧级文本到运动生成（Per-crop语义正确性） |

> [!tip] 效果简介
> - HumanML3D/BABEL 帧级文本到运动生成（Per-seq Realism） 上，FID_tmr++ ↓ 为 0.133 ± 0.004 (Ours HML-BABEL f+s)，对比 0.211 ± 0.002 (FlowMDM BABEL f)，变化 -0.078。
> - 序列级文本到运动生成（Ablation vs MDM） 上，FID ↓ 为 0.133 ± 0.003 (Ours HML-BABEL f+s)，对比 0.449 ± 0.025 (MDM HML s)，变化 -0.316。
> - 帧级文本到运动生成（Per-crop语义正确性） 上，R-Prec@3 ↑ 为 0.679 ± 0.006 (Ours HML-BABEL f+s)，对比 0.618 ± 0.007 (FlowMDM BABEL f)，变化 +0.061。

## 概要

### 问题瓶颈

现有运动生成方法面临一个根本性断层：序列级文本（如“一个人向前走然后转身”）提供全局语义控制，而帧级文本（如“第1-30帧：向前走；第31-60帧：转身”）提供局部细粒度描述，但尚无模型能同时处理这两种层级并建立时间对齐。更关键的是，已有方法缺乏**时间感知的运动理解能力**——它们无法为生成的运动输出每一帧对应的文字说明，导致无法实现真正的层级控制和细粒度编辑。

### 核心方法

UniMotion 提出**时间对齐的多模态联合扩散**框架，核心思路是将帧级文本嵌入与运动姿态在时间维度上对齐后共同输入 Transformer 扩散模型，并对运动和文本分别设置独立的扩散时间步 $t^x$、$t^y$。这使得单一模型能统一采样多种条件分布与联合分布——从仅给定序列级文本生成运动，到同时生成运动及其帧级描述，再到给定运动反推帧级标注。模型联合使用 HumanML3D（序列级标注）和 BABEL（帧级标注）进行训练，利用二者的重叠序列实现跨层级监督。

### 方法谱系与知识库定位

UniMotion 以 **MDM**（扩散运动生成模型）为 backbone，将其从单纯的运动扩散扩展为运动-文本多模态扩散。在帧级文本到运动任务上，对比基线包括自回归模型 **TEACH**、扩散采样方法 **DoubleTake**、基于 MDM 后处理的 **STMC** 以及混合位置编码的扩散模型 **FlowMDM**。在运动理解方面，与 **MotionGPT** 对比，后者缺乏帧级时间感知能力。UniMotion 是首个统一建模运动与帧级文本所有条件分布的概率模型，填补了层级文本控制与时间感知运动理解之间的空白。

### 主要结果

- **帧级文本到运动生成**：在结合序列级和帧级文本（f+s）时，UniMotion 的语义正确性（R-Prec@1 达 0.450）和真实性（FID 降至 0.133）均显著优于所有基线，较 FlowMDM 的 FID 0.211 降低约 37%。
- **序列级文本到运动生成**：即使仅使用序列级文本输入，UniMotion 的 FID（0.195）也远优于 backbone MDM（0.449），表明多模态联合训练本身带来了正则化收益。
- **跨模态泛化**：多数据集联合训练使模型即使在推理时仅用帧级文本，语义指标也一致优于仅在 BABEL 上训练的版本（R-Prec@3 从 0.636 升至 0.668）。
- **新能力解锁**：UniMotion 首次实现了运动与帧级文本的联合生成、运动到帧级文本的理解、以及通过编辑文本再生成来编辑运动等新任务。

### 局限与展望

当前模型依赖 AMASS 数据集上的有限标注，对罕见动作和超长序列的泛化能力尚不明确；帧级文本通过 PCA 降维和 KNN 匹配生成，可能丢失语义细节；推理速度受限于扩散模型的多步采样。未来工作可探索将层级控制扩展到更长时序、引入更先进的文本解码方式、以及融合物理约束或多模态信号（如音乐、唇语）以拓展运动创作的可能性。

### 问题背景：三维人体运动合成的层级控制困境

三维人体运动合成旨在根据自然语言描述生成逼真的人体动作序列。近年来，基于扩散模型的方法（如 **MDM**）在**序列级文本到运动**（Sequence-Level Text-to-Motion）任务上取得了显著进展——给定一句全局描述（如“一个人向前走然后转身”），模型能够生成与之匹配的完整运动序列。然而，这种粗粒度的控制方式存在根本性局限：用户无法对运动序列的**特定时间片段**施加精确的语义约束。

与此相对，**帧级文本到运动**（Frame-Level Text-to-Motion）任务试图解决这一问题——给定一组按时间对齐的局部文本描述（如第1-2秒“走路”，第3-5秒“挥手”），生成符合每段语义的运动序列。现有方法在此方向上的尝试可分为两类：一类以 **TEACH** 为代表，采用自回归模型逐段生成运动，但存在误差累积和长程一致性差的问题；另一类以 **DoubleTake** 和 **FlowMDM** 为代表，利用扩散模型进行采样，但缺乏对全局序列级语义的同步建模能力。此外，**STMC** 虽然尝试通过后处理方式将层级文本控制引入 MDM，但其本质是对已生成运动的“修补”，而非端到端的统一建模。

### 核心瓶颈：时间感知缺失与模态割裂

上述方法的共同缺陷可归结为两个相互关联的瓶颈：

1. **无法同时处理全局与局部文本控制**：现有模型要么仅支持序列级文本输入（如 MDM），要么仅支持帧级文本输入（如 FlowMDM），缺乏一种统一的框架来融合两种粒度的语义条件。这导致用户无法在保持全局运动主题一致性的同时，对特定片段进行细粒度编辑。

2. **缺乏时间感知的运动理解能力**：当前的运动生成模型是“单向”的——它们能够从文本生成运动，但无法反过来为给定的运动序列输出每一帧对应的文字描述。换言之，模型不理解“运动在何时发生了什么”。**MotionGPT** 虽然尝试通过语言模型范式实现运动理解，但由于其将运动量化为离散 token 后丢失了精确的时间对齐信息，实际上无法完成帧级的时间感知任务（参见 Figure 11：MotionGPT 只能输出整个序列的错误时长估计，而非逐段描述）。

### 动机：统一运动合成与理解的必要性

上述瓶颈揭示了一个更深层的需求：**运动合成与运动理解不应当是两个独立的问题**。一个真正具备时间感知能力的运动模型，应当能够对运动序列和帧级文本的联合分布 $p(\mathbf{x}, \mathbf{y} \mid c)$ 进行建模，从而在统一的概率框架下支持从任意条件子集中进行采样——包括从文本生成运动、从运动生成文本、以及二者的联合生成。

这种统一建模一旦实现，将解锁一系列现有方法无法完成的任务：层级文本到运动（同时给定全局和局部文本）、运动到帧级文本（自动为动作序列添加时间对齐的语义标注）、无条件联合生成（从噪声中同时产生运动及其描述）、以及运动编辑（修改局部文本后重新生成对应片段）。这正是 UniMotion 的核心动机——构建**首个统一的多任务概率运动模型**，通过时间对齐的多模态联合扩散，弥合运动合成与理解之间的鸿沟。

## 核心方法与创新机理

UniMotion 的核心创新在于将传统仅支持序列级文本条件的运动扩散模型（MDM）重构为**时间对齐的多模态联合扩散框架**，从而在一个统一的 Transformer 模型中同时实现对运动的层级文本控制与帧级时间感知理解。这一重构通过三个关键的“changed slots”实现。

### 1. 从单模态到时间对齐的多模态联合扩散

原始 MDM 仅对运动序列 $\mathbf{x}$ 施加统一时间步 $t$ 的扩散与去噪过程。UniMotion 将帧级文本嵌入 $\mathbf{y}$ 引入扩散空间，并对运动与文本分别设置**独立的扩散时间步** $t^x$ 与 $t^y$，将去噪网络扩展为 $G_\theta(\mathbf{x}_{t^x}, \mathbf{y}_{t^y}; t^x, t^y, c)$（$c$ 为序列级文本条件）。这一设计使得模型能够灵活采样多种条件分布与联合分布——

- **$t^x > 0, t^y = 0$**：已知帧级文本，生成运动（Frame-Level Text-to-Motion）；
- **$t^x = 0, t^y > 0$**：已知运动，生成帧级文本描述（Motion-to-Text）；
- **$t^x = t^y = t$**：从噪声中联合生成运动与帧级文本（Unconditional Joint Generation）。

这种多模态扩散机制是 UniMotion 统一多种任务的**因果旋钮**（causal knob），直接支撑了方法谱系中从“单一条件生成”到“任意条件组合采样”的范式跃迁。

### 2. 时间对齐的文本-运动编码

与仅将序列级文本作为全局条件注入的方法不同，UniMotion 将帧级文本嵌入与 263 维运动特征在时间维度上对齐后拼接，作为 Transformer 的联合输入。这一**时间对齐策略**是模型获得帧级时间感知能力的关键——它使每一帧运动都与对应的语义标签显式关联，从而让模型能够理解“在何时发生了何种动作”。

此外，为缓解高维 CLIP 嵌入（256 维）带来的容量压力，UniMotion 引入 PCA 将文本嵌入降至约 50 维（保留约 70% 方差），显著提升了训练效率与生成质量。推理时，生成的 PCA 嵌入通过 KNN 在预计算数据库中检索匹配，恢复为可读的自然语言描述。

### 3. 跨标注层级的联合训练

现有帧级文本到运动方法通常仅在 BABEL 数据集上训练，受限于其有限的标注规模。UniMotion 利用 HumanML3D 与 BABEL 在 AMASS 上的时间对应关系，**直接联合使用两个数据集进行训练**：以 HumanML3D 的序列级标注作为全局条件 $c$，以 BABEL 的帧级标注作为 $\mathbf{y}^{1:N}$。这一策略带来了显著的跨模态泛化增益——即使推理时仅使用帧级文本（f），联合训练的模型在语义正确性上仍一致优于仅在 BABEL 上训练的模型（R-Prec@3 从 0.636 升至 0.668），证明多数据集联合训练为帧级运动理解提供了有效的正则化与知识迁移。

### 创新总结

上述三个 changed slots 共同构成了 UniMotion 相对于 MDM 及现有帧级方法的本质突破：**通过时间对齐的多模态扩散与跨标注层级联合训练，首次使单一模型同时具备层级文本控制（序列级 + 帧级）与帧级运动理解能力**，并在统一框架下支持运动编辑、文本/运动变体生成等新任务。这一设计不仅解决了“无法同时处理全局与局部文本控制”的瓶颈，也为运动生成与理解的统一建模提供了可扩展的范式。

![[assets/figures/papers/paper_list_l2_https_coral79_github_io_uni_motion_paper_unimotion_pdf/figures/002_Figure_2.jpg]]
*Figure 2: Overview of UniMotion. UniMotion is a transformer-based diffusion model (Model) that can be input conditioned on a) human motion, b) clip embedded frame-level text, or c) sequence-level text (Input) or any subsets thereof or none, and instead supplied with noise. At it’s core it allows to diffuse motion and text individually, implemented via separate denoising timesteps t ^ { x } and t ^ { y } . . After training with Frame-level text Losses and Motion losses (Loss), see Sec. 4.1. UniMotion can output clean, noise-free motion, and frame-level text descriptions explaining the generated motions. (Output)*

UniMotion 以 MDM 的 Transformer 扩散主干为基础，将其从仅处理运动序列的单模态扩散扩展为同时处理**运动序列**与**帧级文本嵌入**的多模态联合扩散模型。其设计核心在于：通过时间维度上的模态对齐与独立的扩散时间步控制，使单一模型能够统一采样运动与文本的联合分布及所有条件分布，从而支撑层级文本控制、运动理解、联合生成与编辑等多种任务（Figure 2）。

### 输入与模态表示

模型接收三类可选输入，任意子集或全部均可被替换为噪声，实现从无、部分或全部条件中进行灵活采样：

1. **序列级文本 c**：作为全局条件注入 Transformer，提供高层语义指导（如“一个人向前走并挥手”）。
2. **帧级文本 y^{1:N}**：将每一帧对应的局部动作描述（如“抬起右手”）通过预训练 CLIP 文本编码器转换为 256 维嵌入，再经 PCA 降维至约 50 维，以控制模型容量消耗并提升性能。
3. **运动序列 x^{1:N}**：每帧由 263 维特征表示（包含关节旋转、位置、速度等），与降维后的帧级文本嵌入在时间维度上对齐并拼接，形成联合编码输入 Transformer。

### 多模态扩散机制

不同于 MDM 仅对运动序列施加统一扩散时间步，UniMotion 为运动与帧级文本分别引入独立的扩散时间步 t^x 与 t^y。这使得模型可以：

- 在运动完全加噪、文本保持干净时，从文本条件采样运动（帧级/层级文本到运动）；
- 在文本完全加噪、运动保持干净时，从运动条件采样文本（运动理解）；
- 在两者同时加噪时，从噪声中联合生成运动与文本（无条件联合生成）；
- 在推理时自由组合 t^x 与 t^y 的取值，实现运动编辑、文本变化等衍生任务。

### 去噪网络与训练目标

去噪网络 G_θ 基于 MDM 的 Transformer 架构，接收带噪的运动-文本联合编码及其各自的时间步 t^x、t^y，以及全局条件 c，直接预测干净的运动 x_0 和 PCA 压缩的文本嵌入 y_0。训练目标为最小化预测值与真实值之间的 L2 距离：

$$
\min_\theta \mathbb{E}_{(\mathbf{x}_0,\mathbf{y}_0), t^x, t^y} \mathbb{E}_{\mathbf{x}_{t^x},\mathbf{y}_{t^y}} \| G_\theta(\mathbf{x}_{t^x},\mathbf{y}_{t^y}; t^x, t^y, c) - (\mathbf{x}_0,\mathbf{y}_0) \|_2^2
$$

该损失同时约束运动重建与文本嵌入重建，隐式地要求模型学习两种模态在时间轴上的细粒度对应关系。

### 训练数据与联合训练策略

UniMotion 联合使用 HumanML3D（仅序列级标注）和 BABEL（帧级标注）进行训练。对于二者重叠的运动序列，模型以 HumanML3D 的序列级文本作为全局条件 c，以 BABEL 的帧级文本序列作为 y^{1:N}。这种跨数据集联合训练不仅使模型获得了帧级时间感知能力，还通过多目标学习带来了正则化效益——即使仅在推理时使用序列级文本，生成质量也显著优于仅在 HumanML3D 上训练的原始 MDM（Table 2）。

### 输出与后处理

模型输出为干净的运动序列 x_0 与 PCA 压缩的帧级文本嵌入 \hat{y}_0。运动序列可直接用于可视化或下游任务；文本嵌入则通过 KNN 在预计算的 CLIP 嵌入数据库中检索最近邻，恢复为可读的自然语言描述。这一设计绕开了直接生成高维文本嵌入的困难，但也在一定程度上限制了文本输出的精度与开放性（见局限性讨论）。

### 统一能力总结

通过上述流水线，UniMotion 在单一 Transformer 模型中统一了以下任务（Figure 1）：
- **层级文本到运动**：同时接收序列级文本 c 与帧级文本 y，生成符合全局语义且精确执行局部指令的运动。
- **运动到文本**：输入运动 x，输出每一帧的文字描述，实现时间感知的运动理解。
- **无条件联合生成**：从纯噪声中同时生成运动与配套的帧级文本标注。
- **运动编辑与变化**：利用双向条件分布，先生成文本再重新生成运动（或反之），在保持语义的前提下改变内容。

### 3.1 多模态联合扩散框架

UniMotion 的核心创新在于将 MDM 的单模态运动扩散扩展为**运动-文本多模态联合扩散**。其关键操作是对运动序列 $\mathbf{x}^{1:N}$ 和帧级文本嵌入 $\mathbf{y}^{1:N}$ 分别设置独立的扩散时间步 $t^x$ 和 $t^y$，使去噪网络能够同时接收两个模态的带噪版本及其各自的时间步信息：

$$G_\theta(\mathbf{x}_{t^x}, \mathbf{y}_{t^y}; t^x, t^y, c)$$

其中 $c$ 为序列级文本条件。这一设计使得模型可以灵活地采样多种条件分布与联合分布：当 $t^y=0$（文本无噪声）时，模型执行文本到运动生成；当 $t^x=0$ 时，执行运动到文本理解；当 $t^x=t^y$ 时，执行无条件联合生成。

训练目标直接预测干净数据，联合损失函数为：

$$\min_\theta \mathbb{E}_{(\mathbf{x}_0,\mathbf{y}_0), t^x, t^y} \mathbb{E}_{\mathbf{x}_{t^x},\mathbf{y}_{t^y}} \| G_\theta(\mathbf{x}_{t^x},\mathbf{y}_{t^y}; t^x, t^y, c) - (\mathbf{x}_0,\mathbf{y}_0) \|_2^2$$

该损失同时最小化预测的运动序列和帧级文本嵌入与真实数据之间的 L2 距离，隐式地强制运动与文本在时间维度上的对齐一致性。

### 3.2 时间对齐与输入构建

模块实现的关键在于**时间维度对齐**。具体做法是将降维后的帧级文本嵌入与 263 维运动特征按帧拼接，形成沿时间轴的联合编码序列，作为 Transformer 去噪网络的输入。论文明确指出：“temporal alignment to be the key. A simple, yet effective implementation is the concatenation of motion and text into joint encodings along the temporal dimension”（时间对齐是关键，将运动与文本沿时间维度拼接为联合编码是一种简单而有效的实现）。

### 3.3 文本嵌入压缩与恢复

帧级文本通过 CLIP Text Encoder 编码为 256 维嵌入，但直接使用该高维嵌入会过度消耗模型容量。UniMotion 采用 **PCA 降维**将嵌入压缩至约 50 维（保留约 70% 方差），显著提升了性能。在生成阶段，扩散模型输出的是 PCA 空间的嵌入向量，需通过 **KNN 文本检索**在预计算的嵌入数据库中匹配最近邻，恢复为可读的自然语言描述。

### 3.4 采样过程

推理时根据任务需求选择不同的采样策略。以文本到运动生成为例，给定帧级文本嵌入 $\mathbf{y}_0$ 和序列级文本条件 $c$，单步去噪更新为：

$$\mathbf{x}_0^{t-1} = \epsilon_{\theta}^x(\sqrt{\overline{\alpha}_{t^x}} \mathbf{x}_0^t + \sqrt{1 - \overline{\alpha}_{t^x}} \epsilon, \mathbf{y}_0, t, 0, c)$$

其中 $t^y=0$ 表示文本模态无需去噪。无条件联合生成则同时对两个模态进行去噪：

$$\mathbf{x}_0^{t-1}, \mathbf{y}_0^{t-1} = \epsilon_{\theta}(\sqrt{\overline{\alpha}_{t^x}} \mathbf{x}_0^t + \sqrt{1 - \overline{\alpha}_{t^x}} \epsilon^x, \sqrt{\overline{\alpha}_{t^y}} \mathbf{y}_0^t + \sqrt{1 - \overline{\alpha}_{t^y}} \epsilon^y, t, t, c)$$

### 3.5 多数据集联合训练

UniMotion 利用 HumanML3D（序列级标注）和 BABEL（帧级标注）的重叠序列进行联合训练：HumanML3D 的序列级文本作为全局条件 $c$，BABEL 的帧级文本序列作为 $\mathbf{y}^{1:N}$。对于仅有序列级标注的样本，帧级文本分支输入纯噪声，模型仅优化运动预测损失。这一策略使模型在推理时即使仅使用帧级文本条件，也能从多数据集联合训练中获益（Table 1 中 Ours HML-BABEL f 相比 Ours BABEL f 的语义指标一致提升）。

## 实验与关键发现

### 瓶颈验证：层级文本控制与时间感知的统一

UniMotion 的核心主张是：通过将帧级文本与运动在时间维度上对齐，并引入独立的多模态扩散过程（运动扩散时间步 $t^x$ 与文本扩散时间步 $t^y$），单一 Transformer 模型能够统一采样多种条件分布与联合分布，从而解决现有方法无法同时处理全局序列级文本控制和局部帧级文本描述的根本瓶颈。实验部分围绕三个递进层次展开验证：(1) 帧级文本到运动生成是否显著优于专用基线；(2) 多模态联合训练是否带来跨模态泛化增益；(3) 引入多模态扩散后，backbone 模型（MDM）的序列级运动生成质量是否同步提升。

#### 帧级文本到运动：语义正确性与真实感的全面领先

在帧级文本到运动任务上，UniMotion 在所有语义和真实性指标上均显著优于现有基线。Table 4（Per-crop 语义正确性）显示，当同时使用帧级文本和序列级文本作为条件（f+s）时，UniMotion 在 HML-BABEL 联合训练设置下达到 R-Prec@1 = 0.450，M2M = 0.706，而最强的帧级专用基线 FlowMDM（仅使用 BABEL 帧级文本）的对应指标为 R-Prec@1 = 0.418，M2M = 0.677。在 Per-seq 真实感评估（Table 5）中，UniMotion 的 FID_tmr++ 降至 0.133，远低于 FlowMDM 的 0.211，降幅达 0.078。这表明时间对齐的联合扩散不仅提升了局部语义匹配精度，还显著改善了整体运动的自然度。

![[assets/figures/papers/paper_list_l2_https_coral79_github_io_uni_motion_paper_unimotion_pdf/figures/014_Table_5.jpg]]
*Table 5: Frame-level Text2Motion generation per-crop and per-sequence realism evaluation. Crop-level realism measures the metrics within each atomic crop, while Seq-level realism measures the fidelity of the overall motion. Symbols $\downarrow$ , and → indicate that lower, or values closer to the ground truth (GT) are better, respectively*

值得注意的是，Table 1 揭示了多模态联合训练带来的跨模态泛化效应：即使在推理时仅使用帧级文本（f），在 HML 和 BABEL 联合数据上训练的模型（Ours HML-BABEL f）也明显优于仅在 BABEL 上训练的模型（Ours BABEL f）。例如 R-Prec@3 从 0.636 升至 0.668，M2M 从 0.677 升至 0.698。这一现象说明，序列级文本标注（HumanML3D）的引入为帧级文本到运动任务提供了有益的语义正则化，即使这些序列级标注在推理时未被显式使用。

![[assets/figures/papers/paper_list_l2_https_coral79_github_io_uni_motion_paper_unimotion_pdf/figures/003_Table_1.jpg]]
*Table 1: Frame-Level to Text evaluation. Per-crop refers to text segment level evaluation. Training Set specifies the dataset used for training. Input specifies the type of text input. f : frame-level text, s: sequence-level text. f+s demonstrates that combining multi-level conditioning signals can enhance model performance in terms of semantic correspondence. The evaluation is repeated 10 times, and ± indicates the 95% confidence intervals*

#### 消融实验：多模态引入对 backbone 的反哺效应

Table 2 的消融实验直接比较了 UniMotion 与其 backbone 模型 MDM 在序列级文本到运动生成上的表现。结果令人瞩目：UniMotion HML-BABEL f+s 的 FID 降至 0.133，而 MDM 的 FID 为 0.449，降幅高达 0.316；R-Prec@1 从 0.376 提升至 0.424。即使 UniMotion 在推理时仅使用序列级文本（s），其 FID（0.195）和 R-Prec@3（0.655）也显著优于 MDM（0.449 和 0.639）。这证明多目标联合训练（同时预测运动和帧级文本）本身构成了一种有效的正则化，使模型学习到更鲁棒的运动表征，即使在下游仅使用序列级条件时也能受益。

![[assets/figures/papers/paper_list_l2_https_coral79_github_io_uni_motion_paper_unimotion_pdf/figures/005_Table_2.jpg]]
*Table 2: Ablation Study on Sequence-level Text2Motion generation. In this table, we compare with our backbone model MDM[37] to study whether introducing multi-modality helps the motion generation performance. Symbols ↓, and → indicate that lower, or values closer to the ground truth (GT) are better, respectively. The evaluation is repeated 10 times, and ± indicates the 95% confidence interval*

层级控制的有效性在 Table 4 中得到进一步验证：在推理时同时提供帧级文本和序列级文本（f+s）在所有指标上均优于仅使用一种文本条件。例如 Ours HML-BABEL f+s 相比 Ours HML-BABEL f，R-Prec@1 从 0.427 升至 0.450，M2M 从 0.698 升至 0.706。这证实了模型能够有效融合不同粒度的文本信号，而非简单依赖单一条件。

#### 评估公平性：TMR++ 的作用

帧级文本到运动评估的一个关键挑战在于评估模型本身的可靠性。先前工作常使用仅在 HumanML3D 上训练的 Guo et al. 模型，但 Table 3 显示 TMR++（在 HumanML3D 和 BABEL 上联合训练）在 ground-truth 运动-文本匹配上明显优于 Guo et al. 模型，尤其是在跨数据集场景下。本文统一采用 TMR++ 作为评估模型，避免了因评估器偏差导致的指标不可比问题，确保了与 FlowMDM、STMC 等基线的公平比较。

![[assets/figures/papers/paper_list_l2_https_coral79_github_io_uni_motion_paper_unimotion_pdf/figures/011_Table_3.jpg]]
*Table 3: Ground-truth matching score comparison across evaluation modals. In this table, we compare the matching scores across different evaluation models for ground-truth motion and text, averaging over batches of 32 random samples. The results demonstrate that TMR++ is a more reliable model within our evaluation setup*

### 失败模式与局限性

尽管 UniMotion 在主要指标上表现优异，但其设计存在若干固有限制，需要在应用时审慎考虑：

1. **训练数据依赖性**：模型依赖 AMASS 数据集上的 BABEL（帧级标注）和 HumanML3D（序列级标注）进行训练。由于 BABEL 的帧级标注数量有限且动作类型分布不均，模型对罕见动作或超长序列的泛化能力尚不明确。在 OOD 场景下，生成的运动可能出现语义漂移或动作不连贯。

2. **文本输出精度损失**：帧级文本的生成流程为：扩散模型输出 PCA 降维后的 CLIP 嵌入，再通过 KNN 在预计算数据库中检索原始文本标签。PCA 降维（256 维降至约 50 维）虽保留了约 70% 方差，但仍会丢失部分语义细节；KNN 匹配在嵌入空间稀疏区域可能产生不精确甚至错误的描述。这一流水线并非端到端可微的文本生成，其输出质量上限受限于数据库覆盖度。

3. **推理效率**：作为扩散模型，UniMotion 的生成过程需要多步采样（运动与文本可设置不同的扩散步数，但每一步均需通过 Transformer 前向传播）。论文未提供具体的推理延迟数据，也未在实时交互场景中验证，这限制了其在需要低延迟反馈的应用（如在线运动编辑）中的实用性。

4. **单人运动假设**：当前模型仅处理单人运动序列，未考虑多人交互或人与环境物体的交互。这限制了其在社交场景、体育分析等需要多人协同建模的任务中的应用。

5. **编辑忠实度缺乏定量验证**：虽然 Figure 9 展示了运动变化和文本变化的应用案例，但论文缺乏定量的编辑前后一致性指标（如编辑区域外的运动保持度、编辑指令的精确执行率）。编辑功能的可靠性仍需进一步研究。

![[assets/figures/papers/paper_list_l2_https_coral79_github_io_uni_motion_paper_unimotion_pdf/figures/013_Figure_9.jpg]]
*Figure 9: Text variation (a) and motion variation (b) are direct applications that leverage the two conditional distributions modeled by UniMotion. Motion variation (b) is achieved by generating frame-level text descriptions from a motion sequence, and then using these Motion to Text Unconditional Joint Generationiondescriptions to create a new, semantically similar motion with different content. Text variation (a) is produced by reversing this process to Input Motioncreate diverse text annotations. Table 4. Per-crop semantic correctness evaluation for frame-level Text2Motion generation. Training Set specifies the dataset used for training, including BABEL, HumanML3D(HML), or the union/intersection o...*

### 重要图表结论摘要

- **Figure 3**：定性对比显示，UniMotion 在复杂局部文本指令（如“Ginga dance”）下能准确执行指定动作，而 STMC 退化为普通行走，FlowMDM 无法同时接受全局和局部文本条件。这直观验证了层级控制的有效性。
- **Figure 5**：联合生成任务中，仅 UniMotion 能同时输出运动序列和帧级文字标注，MDM 和 FlowMDM 只能生成运动。这证明了多模态联合扩散在运动理解能力上的独特优势。
- **Figure 4**：UniMotion 成功为 MoCap 数据和 YouTube 视频（经 3D 姿态估计提升）生成帧级文字描述，展示了其向真实世界数据泛化的潜力，但需注意姿态估计误差会传播至文本生成。
- **Table 5**：Per-seq 真实感指标（FID_tmr++）显示 UniMotion 的生成质量在整体序列层面同样领先，表明局部帧级对齐的改善并未以牺牲全局连贯性为代价。

## 定位与知识库关联

### 核心瓶颈与因果机制

现有运动生成方法面临一个结构性瓶颈：**无法同时处理全局序列级文本控制和局部帧级文本描述**。具体而言，主流扩散模型（如 **MDM**）仅支持序列级文本到运动的生成，缺乏时间感知能力，无法输出每一帧对应的文字说明。这导致两个关键缺口：第一，用户不能对运动进行层级控制（例如先用一句话定调，再对特定片段做精细编辑）；第二，模型无法从运动序列中反向理解其细粒度语义。UniMotion 的因果调节变量是**时间对齐的多模态联合扩散**——将帧级文本嵌入与姿态特征按时间维度拼接后输入 Transformer，并对运动和文本分别设置独立的扩散时间步 $t^x, t^y$。这一设计使单一模型能够统一采样多种条件分布与联合分布，从而同时具备运动合成和帧级运动理解能力。

### 与基线工作的关系

UniMotion 的直接技术前身是 **MDM**（基于 Transformer 的运动扩散模型），后者仅建模运动模态的单一扩散过程。UniMotion 在三个关键维度上扩展了 MDM：

| 设计维度 | MDM | UniMotion |
|---------|-----|-----------|
| 文本输入模态 | 仅序列级文本 | 序列级文本（全局条件）+ 帧级文本（时间对齐嵌入） |
| 扩散过程 | 单一运动扩散时间步 | 运动 $t^x$ 与文本 $t^y$ 独立扩散时间步 |
| 训练数据 | 单数据集（HumanML3D） | 联合 HumanML3D（序列级标注）与 BABEL（帧级标注） |

在帧级文本到运动任务上，UniMotion 与以下基线形成对比：

- **TEACH**：自回归模型，逐帧生成运动但缺乏全局一致性约束。
- **DoubleTake**：基于扩散采样的帧级生成方法。
- **STMC**：基于 MDM 的后处理方法，通过外部模块将帧级文本注入已生成的序列，而非端到端联合建模。
- **FlowMDM**：扩散模型，使用混合位置编码处理帧级文本，但无法同时接受序列级和帧级文本条件。

实验表明，UniMotion 在帧级文本到运动任务上显著优于所有基线。以最全面的条件组合（帧级文本 + 序列级文本，记为 f+s）为例，在 Per-seq 真实感指标 FID_tmr++ 上达到 0.133，远低于 FlowMDM 的 0.211（Table 5）；在 Per-crop 语义正确性 R-Prec@3 上达到 0.679，比 FlowMDM 的 0.618 提升 6.1 个百分点（Table 4）。与 backbone MDM 相比，即使仅使用序列级文本输入，UniMotion 的 FID 也从 0.449 降至 0.195，验证了多模态联合训练本身带来的正则化收益（Table 2）。

在运动理解方面，**MotionGPT** 虽能执行运动描述和问答，但因缺乏时间感知，无法将运动分解为带时间边界的帧级语义片段。UniMotion 首次实现了语义和时间双重感知的运动理解（Figure 11）。

### 适用边界

1. **数据依赖**：模型依赖 AMASS 数据集上的 BABEL（帧级标注）和 HumanML3D（序列级标注）联合训练。对于罕见动作或超长序列（如几分钟的运动剧本），泛化能力尚不明确。
2. **单人运动假设**：当前模型仅处理单人运动，未考虑多人交互或人与环境物体的交互场景。
3. **文本输出精度**：帧级文本通过 PCA 降维（256 维降至约 50 维，保留约 70% 方差）和 KNN 匹配生成，在分布外（OOD）情况下可能产生不精确的描述。
4. **推理效率**：基于扩散模型的生成需要多步采样，未在实时交互场景中验证。

### 开放问题

- **长时序扩展**：如何将层级文本控制扩展到更长的时间线（如几分钟的运动剧本）并保持全局一致性？
- **多人交互**：UniMotion 的多模态框架能否推广到多人交互运动合成与理解？
- **文本解码改进**：能否使用比 PCA + KNN 更先进的文本解码方式（例如轻量级自回归头）来提升帧级文本的生成质量？
- **扩散调度优化**：运动与文本的扩散时间步分离（$t^x$ vs $t^y$）是否存在更优的调度策略？
- **物理约束集成**：如何将该工作与基于物理的模拟器结合，使生成的运动满足物理约束？
- **多模态扩展**：是否可以引入音乐、唇语等其他时间对齐信号，实现更丰富的多模态运动创作？

## 原文 PDF

![[paperPDFs/3DV_2025/UniMotion_Unifying_3D_Human_Motion_Synthesis_and_Understanding.pdf]]
