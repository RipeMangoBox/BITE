---
title: "LivePhoto: Real Image Animation with Text-guided Motion Control"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/LivePhoto_Real_Image_Animation_with_Text_guided_Motion_Control.pdf
project_link: https://xavierchen34.github.io/LivePhoto-Page/
code_link: null
aliases:
- LivePhoto
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "引入运动强度参数化和文本重加权机制，将运动强度作为可调控的补充条件降低歧义，并通过学习文本嵌入权重强化运动描述。"
primary_logic: "通过参数化运动强度（基于SSIM估计）为模型提供额外的运动速度/幅度信息，可以有效解决文本到运动映射的歧义；同时利用自适应文本重加权抑制内容描述、放大运动描述，实现了兼容图像内容的更强运动控制。"
claims:
- "仅使用参考潜在变量不足以保持后续帧的身份，内容编码器和先验反转显著提升了帧一致性（DINO从82.3到90.8，CLIP从91.7到95.2）。"
- "运动强度引导和文本重加权均对帧一致性有贡献，结合两者达到最佳DINO 90.8和CLIP 95.2；单独去除任一项均导致分数下降。"
- "用户研究中，LivePhoto在文本一致性（4.7）和运动质量（3.9）上显著优于VideoComposer、GEN-2和Pikalabs，证明其文本运动控制的有效性。"
- "文本重加权模块成功为运动相关词分配更高权重，例如在“a baby dinosaur is waving its hand”中，“waving”获得最高权重，从而强化了运动控制。"
---

# LivePhoto: Real Image Animation with Text-guided Motion Control

> [!tip] 核心洞察
> 通过参数化运动强度（基于SSIM估计）为模型提供额外的运动速度/幅度信息，可以有效解决文本到运动映射的歧义；同时利用自适应文本重加权抑制内容描述、放大运动描述，实现了兼容图像内容的更强运动控制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | LivePhoto：基于文本引导运动控制的真实图像动画 |
| 英文题名 | LivePhoto: Real Image Animation with Text-guided Motion Control |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2312.02928) · [Project](https://xavierchen34.github.io/LivePhoto-Page/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | LivePhoto |
| Dataset | WebVID validation set (定量消融), 用户研究（5类图像，800样本） |

> [!tip] 效果简介
> - WebVID validation set (定量消融) 上，DINO Score (↑) 为 90.8 (LivePhoto 完整版)，对比 82.3 (仅参考潜在变量)，变化 +8.5。
> - WebVID validation set (定量消融) 上，CLIP Score (↑) 为 95.2 (LivePhoto 完整版)，对比 91.7 (仅参考潜在变量)，变化 +3.5。
> - 用户研究（5类图像，800样本） 上，Text Consistency (Π(C_text), 1-5评分) 为 4.7 (LivePhoto)，对比 2.5 (GEN-2) / 2.7 (Pikalabs) / 3.5 (VideoComposer)，变化 较最优 baseline +1.2。

## 概要

**核心问题**：真实图像的文本引导动画生成存在一个关键瓶颈——文本指令本身难以精确描述运动的速度与幅度，导致文本到运动的映射具有高度歧义。同时，文本中混杂的内容描述（如物体外观）在与参考图像内容冲突时会被整体抑制，进一步削弱运动控制能力。

**核心思路**：LivePhoto 通过两个相互配合的机制来解决上述问题。其一，引入**运动强度参数化**，基于结构相似度（SSIM）将运动幅度量化为1–10级的可调控系数，作为文本之外的补充条件，降低运动歧义。其二，提出**自适应文本重加权**，通过学习预测每个文本token的运动重要性权重，抑制内容描述、放大运动描述，使文本与图像内容兼容地实现更强的运动控制。

**方法定位**：LivePhoto 以 Stable Diffusion v1.5 为基础，冻结其权重并插入可学习的运动模块（Motion Modules）以捕获帧间时序关系。在此基础上，模型集成了三个关键组件：参考潜在变量与内容编码器（DINOv2）共同提供像素级和全局内容引导；运动强度嵌入作为附加条件输入 UNet；文本重加权模块在 CLIP 文本编码器之后预测逐token权重。与 **VideoComposer**（Wang et al., NeurIPS 2023）等学术方法及 **GEN-2**、**Pikalabs** 等商业产品相比，LivePhoto 在保持图像身份的同时，显著提升了对文本运动指令的遵循能力。

**主要结果**：
- 在 WebVID 验证集上，完整 LivePhoto 的帧一致性指标达到 DINO 90.8、CLIP 95.2，较仅使用参考潜在变量的基线分别提升 +8.5 和 +3.5（Table 1, Table 2）。
- 用户研究中，LivePhoto 在文本一致性（4.7/5）和运动质量（3.9/5）上显著优于 VideoComposer、GEN-2 和 Pikalabs，验证了其文本运动控制的有效性（Table 3）。
- 消融实验证实，运动强度引导和文本重加权各自独立贡献于帧一致性提升；文本重加权成功为运动相关词（如“waving”）分配更高权重，从而强化运动控制（Table 2, Figure 6）。

**局限性**：当前实现基于 Stable Diffusion v1.5，输出分辨率仅为 256×256；运动强度采用离散化 10 级表示，可能无法覆盖所有运动幅度需求。与商业产品相比，LivePhoto 在视频平滑度和空间分辨率上仍有差距，论文推测这源于训练数据规模和超分辨率后处理的差异。



将静态图像转化为动态视频是视觉内容创作中的核心需求，但现有方案在运动控制能力上存在显著瓶颈。文本驱动的图像动画任务面临一个根本性困难：**文本指令天然缺乏对运动速度和幅度的精确描述能力**。例如，“一只熊在跳舞”这样的提示既可以对应缓慢摇摆，也可以对应剧烈扭动，这种文本到运动映射的高度歧义使得模型难以稳定生成符合预期的运动。

更棘手的是，文本中往往混杂着内容描述（如“一只棕色的熊”）和运动描述（如“在跳舞”）。当内容描述与输入图像的信息冲突时，模型倾向于整体抑制文本的影响，导致运动指令被一并忽略——用户写了“挥手”，模型却输出一个几乎静止的视频。这一现象的本质是**文本嵌入中内容语义与运动语义的耦合**，现有方法缺乏有效机制将两者解耦并分别处理。

从方法层面审视，当前主流方案可分为两类。一类是以 **VideoComposer**（Wang et al., NeurIPS 2023）为代表的学术方法，它通过组合式条件控制实现了基本的图像到视频生成，但在运动幅度控制上仍依赖文本的模糊描述。另一类是商业产品如 **GEN-2**（Runway, 2023）和 **Pikalabs**（PikaLabs, 2023），它们虽然在图像一致性和视频平滑度上表现出色，但其运动控制能力同样受限于文本输入的固有歧义。开源项目如 **I2VGEN-XL**、**AnimateDiff-I2V** 和 **Talesofai** 则普遍面临身份保持困难或运动生成不足的问题。

上述缺口指向一个明确的研究动机：**能否引入一种显式的运动强度控制机制，将运动幅度从文本歧义中解放出来，同时设计一种文本重加权策略，让模型学会区分“该看什么”和“该怎么动”？** LivePhoto 正是沿着这一思路展开，通过运动强度参数化和自适应文本重加权两个核心模块，在保持图像内容一致性的前提下大幅提升了文本运动控制的精确性。



## 核心方法与创新机理

LivePhoto 的核心创新在于针对文本驱动的真实图像动画任务，系统性地解决了文本到运动映射中的两个根本性瓶颈：**运动歧义**与**文本-内容冲突**。通过引入两个正交且互补的机制——运动强度参数化引导与自适应文本重加权——该方法在不牺牲图像内容保真度的前提下，显著增强了文本对运动行为的控制能力。

### 瓶颈分析：文本到运动映射的双重困境

文本指令在描述运动时存在固有的信息缺失。同一段文字（如“熊在跳舞”）可以对应从轻微晃动到剧烈摇摆的多种运动幅度，仅凭文本嵌入难以区分这些差异，导致生成结果要么静止不动，要么迅速模糊（见 Figure 5）。这是文本到运动映射的**高度歧义性**问题。

与此同时，CLIP 编码的文本嵌入中混杂着内容描述词（如“baby dinosaur”）与运动描述词（如“waving its hand”）。当内容描述与输入参考图像的内容产生冲突时，模型倾向于整体抑制文本信号，而非选择性地保留运动指令。消融实验证实，未加权的文本嵌入会使模型完全忽略运动描述，或过度聚焦于内容词（Figure 6）。这是文本信号与图像信号之间的**兼容性冲突**。

### 创新机制一：运动强度参数化引导

为降低运动歧义，LivePhoto 将运动强度显式参数化为一个可调控的补充条件。具体而言，训练时根据视频片段相邻帧的平均 SSIM 计算运动强度，并将其离散化为 1 至 10 共十个等级；推理时该强度可由用户直接指定。强度信息以 1 通道嵌入的形式与噪声潜在变量、参考潜在变量、帧嵌入拼接为 10 通道张量，一并输入 UNet 进行去噪（Figure 2）。

这一设计的因果逻辑在于：运动强度作为额外的速度/幅度信息源，弥补了文本描述在运动量级上的信息缺口，从而将原本一对多的歧义映射转化为条件明确的生成过程。消融实验（Table 2）验证了其独立贡献：移除运动强度引导后，DINO 帧一致性分数从 90.8 降至 90.3，CLIP 分数从 95.2 降至 94.8。用户可通过调节强度等级精细控制运动幅度——等级 2 生成几乎静止的画面，等级 10 则可能引入运动模糊，默认等级 5 提供适中的运动表现（Figure 5）。

### 创新机制二：自适应文本重加权

为解决文本-内容冲突，LivePhoto 在 CLIP 文本编码器之后附加了一个可学习的重加权模块。该模块由三层 Transformer 编码器和逐帧线性层构成，为每个文本 token 预测一个运动重要性权重，经 Sigmoid 归一化后与原始嵌入相乘（Figure 3）。其核心作用是**抑制内容描述词的权重，放大运动描述词的权重**，使文本信号能够与图像内容兼容地注入去噪过程。

Figure 3 和 Figure 6 的权重可视化直接证实了这一机制的有效性：在提示词“a baby dinosaur is waving its hand”中，“waving”被赋予最高权重，而“baby”和“dinosaur”等内容词被显著抑制。消融实验（Table 2）表明，移除文本重加权会导致 DINO 分数降至 90.1、CLIP 分数降至 93.9，降幅大于移除运动强度引导，说明文本重加权在维持帧一致性方面发挥着更为关键的作用。

### 创新协同：从冲突抑制到运动增强

两个创新机制在功能上形成互补：运动强度引导从**量级维度**消除歧义，文本重加权从**语义维度**增强运动信号的纯度。Table 2 的完整消融显示，同时部署两者时达到最优 DINO 90.8 和 CLIP 95.2，单独移除任一项均导致分数下降，验证了二者的独立贡献与协同效应。用户研究（Table 3）进一步从感知层面佐证了这一设计的优势：LivePhoto 在文本一致性（4.7/5）和运动质量（3.9/5）上显著优于 **VideoComposer**（Wang et al., NeurIPS 2023）、GEN-2 和 Pikalabs，证明了文本运动控制能力的实质性提升。

值得注意的是，LivePhoto 在图像一致性（3.6/5）上略低于商业产品 GEN-2（3.7）和 Pikalabs（3.9），论文推测这源于商业产品在训练数据规模、超分辨率后处理等方面的资源优势，而非方法设计层面的缺陷。这也意味着，当前创新在运动控制与图像保真度之间取得了有利的权衡——以微小的保真度代价换取了大幅领先的运动可控性。



![[assets/figures/papers/paper_list_l45_LivePhoto_Real_Image_Animation_with_Text_guided_Motion_Control/figures/002_Figure_2.jpg]]
*Figure 2: Overall pipeline of LivePhoto. Besides taking the reference image and text as input, LivePhoto leverages the motion intensity as a supplementary condition. The image and the motion intensity (from level 1 to 10) are obtained from the ground truth video during training and customized by users during inference. The reference latent is first extracted as local content guidance. We concatenate it with the noise latent, a frame embedding, and the intensity embedding. This 10-channel tensor is fed into the UNet for denoising. During inference, we use the inversion of the reference latent instead of the pure Gaussian to provide content priors. At the top, a content encoder extracts the visual toke...*

LivePhoto 的整体 pipeline 以一张参考图像、一段文本描述以及一个运动强度系数作为输入，输出一段 16 帧、分辨率为 256×256 的视频，其核心架构围绕 Stable Diffusion v1.5 的 UNet 展开，并在其基础上插入可学习的运动模块以捕获帧间时序关系（Figure 2）。

**输入处理与条件注入。** 参考图像首先通过 VAE 编码器提取参考潜在变量（reference latent），与噪声潜在变量、帧嵌入（frame embedding）以及运动强度嵌入（intensity embedding）在通道维度拼接，形成一个 10 通道的张量作为 UNet 的输入。这一设计将像素级内容引导直接注入去噪过程，为后续帧的身份保持提供了基础锚点。与此同时，一个冻结的 DINOv2 作为内容编码器（content encoder）提取参考图像的 patch token，经可学习的线性投影后，通过交叉注意力（cross-attention）注入 UNet 的各个阶段，提供全局内容引导。

**运动强度作为补充条件。** 文本描述天然存在对运动速度和幅度的表达歧义——同一句“熊在跳舞”既可能对应缓慢摇摆，也可能对应剧烈扭动。LivePhoto 引入运动强度参数化来解决这一瓶颈：训练时，根据视频片段中相邻帧的结构相似度（SSIM）均值计算运动强度，并离散化为 1–10 级；推理时，用户可直接指定强度等级，以单通道嵌入的形式参与去噪过程。这一机制将原本高度歧义的文本到运动映射，转化为文本与可调控强度系数的联合条件，显著降低了映射的不确定性。

**文本重加权模块。** 文本中往往混杂着内容描述（如“a baby dinosaur”）和运动描述（如“waving its hand”），直接使用 CLIP 文本嵌入会导致内容词与图像内容冲突时整体被抑制，运动指令随之丢失。LivePhoto 在冻结的 CLIP 文本编码器之后附加三层 Transformer 编码器和一个逐帧线性层，为每个文本 token 预测一个 [0, 1] 范围内的权重，经 Sigmoid 后与原始嵌入逐元素相乘。该模块通过学习自动抑制内容描述词、放大运动相关词（Figure 3），使文本条件与图像内容兼容，从而实现更强的运动控制。

**先验反转。** 在推理阶段，LivePhoto 并非从纯高斯噪声开始去噪，而是将参考潜在变量的 DDIM 反转结果按比例 $\boldsymbol{\alpha}^n$ 与噪声混合：
$$\tilde{\mathbf{z}}_T^n = \boldsymbol{\alpha}^n \cdot \mathrm{Inv}(\mathbf{r}_0) + (1 - \boldsymbol{\alpha}^n) \cdot \mathbf{z}_T^n$$
其中 $\boldsymbol{\alpha}^n$ 从首帧到末帧线性衰减。这一操作为初始帧提供了强外观先验，与内容编码器协同作用，大幅提升了帧间身份一致性（Table 1：DINO 从 82.3 提升至 90.8，CLIP 从 91.7 提升至 95.2）。

**训练与推理流程。** 训练阶段，运动强度由真实视频的 SSIM 计算得到，文本重加权模块与运动模块同步学习。推理阶段，用户提供任意参考图像、文本指令和可选的运动强度等级（默认等级 5），模型在零样本设定下生成动画视频。整个 pipeline 中，Stable Diffusion 的基础权重和 DINOv2 编码器保持冻结，仅运动模块、文本重加权模块和内容编码器的线性投影层参与训练。



LivePhoto 在 Stable Diffusion v1.5 的文本到视频扩散框架基础上，围绕“文本到运动的歧义性”这一核心瓶颈，引入了三个关键设计：**参考图像内容引导**、**运动强度参数化**和**文本重加权**。以下逐一拆解其机理与公式。

### 1. 扩散基础

LivePhoto 沿用标准的前向扩散与去噪训练范式。给定视频帧的 VAE 潜在变量 $\mathbf{z}_0$，前向过程逐步注入高斯噪声：

$$\mathbf{z}_t = \sqrt{\bar{\alpha_t}} \mathbf{z}_0 + \sqrt{1 - \bar{\alpha_t}} \epsilon$$

其中 $\epsilon \sim \mathcal{N}(0, \mathbf{I})$，$\bar{\alpha_t}$ 为累计噪声系数。去噪网络 $\epsilon_\theta$ 以文本条件 $\mathbf{c}$ 和时刻 $t$ 为条件预测所加噪声，训练目标为最小化预测噪声与真实噪声的均方误差：

$$\mathbb{E}_{\mathbf{z}, \mathbf{c}, \epsilon, t} \big( \| \epsilon_{\theta}(\mathbf{z}_t, \mathbf{c}, t) - \epsilon \|_2^2 \big)$$

### 2. 参考图像内容引导

为保持生成视频与参考图像的身份一致性，LivePhoto 从两个粒度注入视觉信息：

- **像素级引导**：提取参考图像的 VAE 潜在变量 $\mathbf{r}_0$，将其与噪声潜在变量、帧嵌入、运动强度嵌入拼接为 10 通道张量，直接输入 UNet。
- **全局语义引导**：使用冻结的 DINOv2 提取参考图像的 patch token，经可学习的线性投影后，通过交叉注意力注入 UNet 各层。

推理阶段，LivePhoto 进一步引入**先验反转**，将纯高斯噪声替换为参考潜在变量的反转结果与噪声的混合：

$$\tilde{\mathbf{z}}_T^n = \boldsymbol{\alpha}^n \cdot \mathrm{Inv}(\mathbf{r}_0) + (1 - \boldsymbol{\alpha}^n) \cdot \mathbf{z}_T^n$$

其中 $\boldsymbol{\alpha}^n$ 为从首帧到尾帧线性衰减的混合系数，使得早期去噪步骤获得更强的内容先验。消融实验（Table 1）证实：仅使用参考潜在变量拼接时 DINO 仅 82.3、CLIP 仅 91.7；加入内容编码器后升至 85.9/93.2；再加入先验反转达到 90.8/95.2，验证了全局引导与先验反转的互补增益。

### 3. 运动强度参数化

文本指令难以精确描述运动的速度和幅度，这是文本到运动映射歧义的根本原因。LivePhoto 的解决方案是引入一个显式的运动强度系数作为补充条件。

**训练阶段**，运动强度从真实视频中自动估计。对于包含 $n$ 帧的视频片段 $\mathbf{X}^n$，计算所有相邻帧的结构相似度均值：

$$\mathbf{I}(\mathbf{X}^n) = \frac{1}{n} \sum_{i=0}^{n-2} \mathrm{SSIM}(\mathbf{x}^i, \mathbf{x}^{i+1})$$

其中 SSIM 定义为亮度 $l$、对比度 $c$ 和结构 $s$ 三个差异指标的加权乘积：

$$\operatorname{SSIM}(\mathbf{x}, \mathbf{y}) = l(\mathbf{x}, \mathbf{y})^{\alpha} \cdot c(\mathbf{x}, \mathbf{y})^{\beta} \cdot s(\mathbf{x}, \mathbf{y})^{\gamma}$$

默认 $\alpha = \beta = \gamma = 1$。计算得到的连续强度值被离散化为 1-10 级，以 1 通道嵌入形式与帧嵌入拼接后输入 UNet。选择 SSIM 而非光流等指标的原因在于，SSIM 与人类对运动幅度的感知最为一致（Sec. 3.4）。

**推理阶段**，用户可直接指定强度等级，实现运动幅度的精细调控：等级 2 生成几乎静止的视频，默认等级 5 提供适中运动，等级 10 可能引入过度运动模糊（Figure 5）。

### 4. 文本重加权

文本描述中混杂的内容词（如“baby dinosaur”）与运动词（如“waving”）之间存在竞争：当内容描述与图像内容冲突时，模型倾向于整体抑制文本条件，导致运动指令失效。文本重加权模块的目标是学习一个 token 级的权重，抑制内容描述、放大运动描述。

具体实现：在冻结的 CLIP 文本编码器之后，附加三层 Transformer 编码器和一个逐帧线性层。对于每个文本 token，线性层输出一个标量，经 Sigmoid 激活后作为权重与原始嵌入相乘。训练过程中，该模块通过端到端优化自动学习哪些 token 对运动控制更关键。Figure 3 的可视化表明，在“a baby dinosaur is waving its hand”中，“waving”获得了最高权重，验证了模块的有效性。

消融实验（Table 2）量化了运动强度引导与文本重加权的独立贡献：移除运动强度引导导致 DINO 从 90.8 降至 90.3、CLIP 从 95.2 降至 94.8；移除文本重加权导致 DINO 降至 90.1、CLIP 降至 93.9。文本重加权的降幅更大，表明其对帧一致性的影响更为显著——这与“文本歧义是核心瓶颈”的论断一致。



## 实验与关键发现

### 核心瓶颈与因果机制

LivePhoto 要解决的根本矛盾在于：**文本指令天然难以精确描述运动的速度和幅度**，导致文本到运动的映射存在高度歧义。例如，“挥手”这一指令无法区分快速挥动与缓慢挥动。更棘手的是，文本中混杂的内容描述（如“一只恐龙宝宝”）在与图像内容冲突时会被模型整体抑制，进一步削弱运动控制能力。

针对这一瓶颈，LivePhoto 引入了两个因果调控旋钮。第一，**运动强度参数化**：通过 SSIM 估计相邻帧的结构相似度，将运动强度量化为 1–10 级的离散系数，作为文本之外的补充条件注入 UNet，直接降低运动幅度描述的不确定性。第二，**文本重加权机制**：在 CLIP 文本编码器之后附加可学习的 Transformer 层，预测每个 token 的运动重要性权重，经 Sigmoid 后与嵌入相乘，抑制内容描述词、放大运动描述词，使文本条件与图像内容兼容地协同工作。

### 消融实验：图像内容引导组件逐步验证

图像内容保持是真实图像动画的基础能力。论文通过逐步添加组件的方式，在 WebVID 验证集上以 DINO 和 CLIP 分数衡量帧一致性，清晰展示了各组件的因果贡献。

**仅使用参考潜在变量**（将参考图像的 VAE 潜在变量与噪声潜在变量拼接输入 UNet）时，DINO 仅为 82.3，CLIP 为 91.7，模型难以保持后续帧的身份一致性。**加入内容编码器**（冻结的 DINOv2 提取参考图像 patch token，经可学习线性层后通过交叉注意力注入 UNet）后，DINO 提升至 85.9，CLIP 提升至 93.2，说明全局内容引导显著增强了身份保持能力。**进一步加入先验反转**（将参考潜在变量的反转结果与噪声潜在变量按比例混合，为初始帧提供外观先验）后，DINO 达到 90.8，CLIP 达到 95.2，达到最佳帧一致性。

这一消融链条的因果逻辑清晰：参考潜在变量提供像素级局部引导，内容编码器补充全局语义引导，先验反转为早期去噪步骤提供内容锚定——三者协同，逐层加固了帧间身份一致性。定性结果（Figure 4）也印证了这一点：仅拼接参考潜在变量时，生成帧的身份漂移明显；逐步加入内容编码器和先验反转后，细节质量和身份保持持续改善。

![[assets/figures/papers/paper_list_l45_LivePhoto_Real_Image_Animation_with_Text_guided_Motion_Control/figures/004_Figure_4.jpg]]
*Figure 4: Ablations for the image content guidance. Only concatenating the reference latent with the model input meets challenges in preserving the identity. The content encoder and prior inversion gradually enhance the performance*

### 消融实验：运动强度引导与文本重加权的独立贡献

为验证两个核心新模块的独立贡献，论文在完整模型基础上分别移除运动强度引导和文本重加权，结果汇总于 Table 2。

![[assets/figures/papers/paper_list_l45_LivePhoto_Real_Image_Animation_with_Text_guided_Motion_Control/figures/008_Table_2.jpg]]
*Table 2: Quatitative analysis for novel modules. Frame consistency is measured by DINO and CLIP scores. Motion intensity guidance and text re-weighting both make contributions*

移除运动强度引导（w/o Motion Intensity）后，DINO 从 90.8 降至 90.3，CLIP 从 95.2 降至 94.8。移除文本重加权（w/o Text Re-weighting）后，DINO 降至 90.1，CLIP 降至 93.9。两项指标在移除任一模块后均出现一致下降，验证了两个模块各自对帧一致性的正向贡献。值得注意的是，文本重加权的移除导致 CLIP 下降幅度更大（-1.3 vs -0.4），暗示该模块对文本-视觉对齐的影响更为显著。

定性分析（Figure 6）进一步揭示了文本重加权的因果作用。以提示词“a baby dinosaur is waving its hand”为例，无重加权时模型倾向于忽略文本中的运动指令，或过度关注内容描述“baby dinosaur”，导致生成的视频缺乏“挥手”动作。加入重加权后，内容描述被抑制，运动描述“waving its hand”获得最高权重，模型成功生成相应的挥手动作。Figure 3 右侧的权重可视化也证实：运动相关词（如“waving”）被赋予显著更高的权重，而内容词被有效抑制。

### 运动强度引导的控制能力

运动强度等级（1–10）为用户提供了精细的运动幅度控制。Figure 5 的定性示例显示，等级 2 生成几乎静止的视频，默认等级 5 提供适中运动，而等级 10 可能产生过度运动模糊。这一离散化设计虽然直观易用，但论文也坦诚其局限性：离散等级可能无法覆盖所有运动幅度需求，连续或更自适应的强度表示可能更优。

![[assets/figures/papers/paper_list_l45_LivePhoto_Real_Image_Animation_with_Text_guided_Motion_Control/figures/006_Figure_5.jpg]]
*Figure 5: Illustrations of motion intensity guidance. The prompt is “The bear is dancing”. Without intensity guidance, the generated video tends to either keep still or quickly become blurry. With the option to set varying intensity levels, users can finely control the motion range and speed. It should be noted that excessively high intensity levels might induce motion blur, as observed in the last case*

### 用户研究：与商业及学术方法的综合对比

用户研究在 5 类图像、800 样本的统一基准上进行，从四个维度评估：图像一致性 Π(C_image)、文本一致性 Π(C_text)、内容质量 Π(Q_cont) 和运动质量 Ω(Q_mot)。每个方法生成 8 个结果并人工筛选最优，一定程度上减轻了随机生成的影响。

**文本一致性**方面，LivePhoto 获得 4.7 分，显著优于 VideoComposer（3.5）、GEN-2（2.5）和 Pikalabs（2.7），较最优 baseline 提升 +1.2。这直接验证了运动强度引导和文本重加权在文本-运动对齐上的有效性——商业产品虽然在生成质量上更优，但在精确遵循文本运动指令方面明显逊色。

**运动质量**方面，LivePhoto 获得 3.9 分，优于 VideoComposer（3.6）、GEN-2（3.3）和 Pikalabs（3.1），较最优 baseline 提升 +0.3。这表明 LivePhoto 生成的运动在适宜性上更具优势。

**图像一致性**方面，LivePhoto 获得 3.6 分，略低于 Pikalabs（3.9）和 GEN-2（3.7），但显著高于 VideoComposer（2.8）。论文推测商业产品在图像一致性上的优势得益于更优质的大规模训练数据以及超分辨率后处理组件，而 LivePhoto 作为基于 SD1.5 的学术方法，在输出分辨率（256×256）和视频平滑度上存在固有差距。

### 与开源方法的定性比较

Figure 8 展示了 LivePhoto 与 I2VGEN-XL、AnimateDiff-I2V 和 Talesofai 等开源项目的比较。I2VGEN-XL 仅生成与参考图像“相关”的内容，而非真正的动画；AnimateDiff-I2V 生成的视频几乎不包含运动；Talesofai 无法保持真实照片的身份一致性。LivePhoto 在三者中唯一实现了身份保持与文本运动控制的兼顾。

### 已知局限与待验证问题

论文坦承两个主要局限。其一，LivePhoto 基于 Stable Diffusion v1.5 实现，输出分辨率仅 256×256，采用更高分辨率基础模型（如 SD-XL）有望大幅提升性能。其二，运动强度的离散化虽便于用户调节，但可能无法覆盖所有运动幅度需求。

以下问题需要后续工作验证或用户自行评估：运动强度估计是否应与文本语义动态绑定，使不同动作描述自动映射到合理强度范围；文本重加权模块在长尾或复合运动描述上的泛化能力；LivePhoto 能否扩展到 16 帧以上并保持时序一致性；当用户输入图像与训练数据分布差异较大时，强度引导是否仍然有效。

### 补充图表

![[assets/figures/papers/paper_list_l45_LivePhoto_Real_Image_Animation_with_Text_guided_Motion_Control/figures/001_Figure.jpg]]

![[assets/figures/papers/paper_list_l45_LivePhoto_Real_Image_Animation_with_Text_guided_Motion_Control/figures/005_Table_1.jpg]]
*Table 1: Quatitative analysis for image content guidance. We assess frame consistency using DINO and CLIP scores. The content encoder and prior inversion bring steady improvements*

![[assets/figures/papers/paper_list_l45_LivePhoto_Real_Image_Animation_with_Text_guided_Motion_Control/figures/011_Table_3.jpg]]
*Table 3: Results of user study. We let annotators rate from four perspectives: Image consistency $\mathbf { \Pi } ( \mathbf { C } _ { \mathrm { i m a g e } }$ ) evaluates the capability to maintain the identity of the reference image. Text consistency $\mathbf { \Pi } ( \mathbf { C } _ { \mathrm { t e x t } }$ ) measures the adherence to the textual descriptions in directing motion. Content quality $\mathbf { \Pi } ( \mathbf { Q } _ { \mathrm { c o n t } }$ ) focuses on the interframe coherence and resolutions. Motion quality $\mathbf { \Omega } ( \mathbf { Q } _ { \mathrm { m o t } }$ ) evaluates appropriateness of motions



## 定位与知识库关联

### 1. 问题定位与核心瓶颈

LivePhoto 试图解决的核心问题是**真实图像的文本驱动动画生成**：给定一张真实参考图像和一段文本运动描述，生成一段保持图像身份、同时精确遵循文本运动指令的视频。该任务面临两个关键瓶颈：

**瓶颈一：文本到运动的映射歧义。** 文本指令难以精确描述运动的速度和幅度——例如“挥手”这一描述本身无法区分快速挥动与缓慢摆动。这种高度歧义使得模型容易产生运动幅度失控（过弱导致静止，过强导致模糊）的问题。

**瓶颈二：文本中内容描述与运动描述的冲突。** 典型的文本提示往往同时包含内容描述（如“baby dinosaur”）和运动描述（如“waving its hand”）。当内容描述与参考图像的内容冲突时，模型倾向于整体抑制文本的引导作用，导致运动控制能力被连带削弱。

LivePhoto 通过两个核心机制回应上述瓶颈：（1）引入**运动强度参数化**，将运动幅度作为可调控的补充条件，降低文本到运动映射的歧义；（2）提出**文本重加权**，通过学习自适应地抑制内容词、放大运动词，使文本嵌入与图像内容兼容地引导运动。

### 2. 方法在知识谱系中的位置

#### 2.1 基础架构继承

LivePhoto 建立在 **Stable Diffusion v1.5**（SD1.5）的潜在扩散框架之上，继承了其预训练的文本到图像生成能力。在此基础上，论文构造了一个图像到视频（I2V）的基线架构：

- **运动模块（Motion Modules）**：在冻结的 SD1.5 UNet 各阶段后插入可学习的时间层，捕获帧间时序关系。这一设计沿袭了 AnimateDiff 等工作的思路。
- **参考潜在变量拼接**：将参考图像的 VAE 潜在变量与噪声潜在变量、帧嵌入拼接为 10 通道张量输入 UNet，提供像素级内容引导。
- **内容编码器（Content Encoder）**：使用冻结的 **DINOv2** 提取参考图像的 patch token，经可学习线性层后通过交叉注意力注入 UNet，提供全局内容引导。

这一基线架构本身即融合了潜在扩散模型、时序运动建模和图像条件注入三条技术路线。

#### 2.2 与现有工作的差异化贡献

相较于已有方法，LivePhoto 的独特贡献在于**将运动控制从隐式的文本条件中解耦，显式地建模运动强度并强化文本中的运动语义**：

| 方法 | 运动控制方式 | 文本处理策略 |
|------|-------------|-------------|
| **VideoComposer** (Wang et al., NeurIPS 2023) | 多条件组合（文本、草图、运动向量等） | 标准 CLIP 文本嵌入 |
| **GEN-2** (Runway, 2023) | 端到端黑盒（商业产品） | 未公开 |
| **Pikalabs** (PikaLabs, 2023) | 端到端黑盒（商业产品） | 未公开 |
| **I2VGEN-XL** | 文本条件 | 标准 CLIP 嵌入 |
| **AnimateDiff-I2V** | 文本条件 + 运动模块 | 标准 CLIP 嵌入 |
| **LivePhoto**（本方法） | **文本 + 运动强度参数化** | **自适应文本重加权** |

具体而言，LivePhoto 在以下两个“可替换槽位”上做出了改变：

- **槽位一：运动强度引导（Motion Intensity Guidance）**。基线方法仅依赖文本描述来隐式控制运动幅度，LivePhoto 则引入基于 SSIM 参数化的运动强度作为附加条件。训练时，根据视频相邻帧的平均 SSIM 计算运动强度并离散化为 1–10 级；推理时，用户可手动指定强度等级。该强度以 1 通道嵌入形式与噪声潜在变量拼接，为 UNet 提供显式的运动幅度信息。
- **槽位二：文本重加权（Text Re-weighting）**。基线方法直接使用 CLIP 文本编码器的输出嵌入，LivePhoto 则在 CLIP 编码器之后附加三层 Transformer 和逐帧线性层，预测每个 token 的运动重要性权重，经 Sigmoid 后与原始嵌入相乘。这使得模型能够自动抑制“baby dinosaur”等内容词、放大“waving”等运动词。

#### 2.3 与 baseline 的性能关系

在 WebVID 验证集上的定量消融表明，LivePhoto 的完整版（含运动强度引导和文本重加权）在帧一致性指标上达到 DINO 90.8、CLIP 95.2。相比之下，仅使用参考潜在变量的基线仅为 DINO 82.3、CLIP 91.7，逐步加入内容编码器和先验反转后提升至 DINO 90.8、CLIP 95.2（Table 1）。移除运动强度引导后 DINO 降至 90.3、CLIP 降至 94.8；移除文本重加权后 DINO 降至 90.1、CLIP 降至 93.9（Table 2），验证了两个模块的独立贡献。

在用户研究中（Table 3），LivePhoto 在**文本一致性**上以 4.7 分显著优于 VideoComposer（3.5）、GEN-2（2.5）和 Pikalabs（2.7），在**运动质量**上以 3.9 分领先于 VideoComposer（3.6）、GEN-2（3.3）和 Pikalabs（3.1），证明了其文本运动控制的有效性。然而，在**图像一致性**上，LivePhoto（3.6）略低于 GEN-2（3.7）和 Pikalabs（3.9），论文推测商业产品受益于更大规模的训练数据和超分辨率后处理组件。

### 3. 适用边界与局限

#### 3.1 已知局限

- **分辨率受限**：LivePhoto 基于 SD1.5 实现，输出分辨率为 256×256。论文明确指出，采用更高分辨率和更强的文本到图像基础模型（如 SD-XL）有望大幅提升性能，但受限于训练成本未实现。
- **运动强度离散化**：运动强度被离散化为 10 个等级，虽然方便用户调节，但可能无法覆盖所有运动幅度需求。实验显示，等级 2 生成几乎静止的视频，等级 10 可能产生过度运动模糊（Figure 5），连续或更自适应的强度表示可能更优。
- **与商业产品的差距**：在视频平滑度、空间分辨率和图像一致性上，LivePhoto 仍落后于 GEN-2 和 Pikalabs 等商业产品。论文承认这源于训练数据规模和超分辨率后处理的差异，而非方法本身的根本缺陷。
- **序列长度**：论文仅验证了 16 帧视频的生成，更长序列的时序一致性尚未验证。

#### 3.2 适用场景

LivePhoto 适用于以下场景：
- 需要**精确文本运动控制**的真实图像动画任务，尤其是运动描述与图像内容存在潜在冲突的情况。
- 用户希望**手动调节运动幅度**的交互式应用（通过运动强度等级 1–10）。
- **零样本**场景：模型无需针对特定图像或运动类型进行微调。

不适用或需谨慎使用的场景：
- 对**高分辨率输出**有刚性需求的应用。
- 需要**超长视频序列**（远超 16 帧）且对时序一致性要求极高的场景。
- 用户输入图像与训练数据分布差异极大时，运动强度引导的有效性可能下降（论文未对此进行验证）。

### 4. 开放问题

1. **运动强度与文本语义的绑定**：当前运动强度由用户手动指定或从训练视频的 SSIM 分布中估计，与文本语义解耦。是否应将运动强度与文本语义动态绑定，使得“快速奔跑”与“缓慢摇头”能自动映射到合理的强度范围？
2. **文本重加权的泛化性**：重加权模块在长尾或复合运动描述（如“边挥手边转圈”）上的泛化能力如何？是否会出现对某些高频运动词的过拟合？
3. **与商业产品的差距弥合**：如何在不损失文本运动控制能力的前提下，通过超分辨率后处理或更大规模训练缩小与商业产品在视频平滑度和分辨率上的差距？
4. **长序列扩展**：LivePhoto 能否扩展到更长序列（如 64 帧或更多）并保持时序一致性？先验反转机制中的线性衰减系数 $\alpha^n$ 在长序列下是否需要重新设计？
5. **跨分布泛化**：运动强度估计依赖训练视频的 SSIM 分布，当用户输入图像（如医学图像、遥感图像）与训练数据分布差异较大时，强度引导是否仍然有效？



## 原文 PDF

![[paperPDFs/ECCV_2024/LivePhoto_Real_Image_Animation_with_Text_guided_Motion_Control.pdf]]
