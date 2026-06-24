---
title: "Control-A-Video: Controllable Text-to-Video Diffusion Models with Motion Prior and Reward Feedback Learning"
type: paper
paper_level: A
venue: arXiv
year: 2023
pdf_ref: paperPDFs/arxiv_2023/Control_A_Video_Controllable_Text_to_Video_Diffusion_Models_with_Motion_Prior_and_Reward_Feedback_Learning.pdf
aliases:
- CV
- Control-A-Video
tags:
- arxiv_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将运动感知噪声初始化与奖励反馈优化相结合，是提升帧间一致性与视频质量的关键控制杠杆。
primary_logic: 通过第一帧内容先验解耦内容与运动建模，利用残差/光流驱动的运动先验保持帧间相关性，并引入时空奖励反馈学习（ST-ReFL）联合优化美学质量、技术质量与运动一致性，可显著提升可控视频生成的整体表现。
claims:
- 第一帧条件方案将图像域的生成能力迁移到视频生成，有效分离内容与运动建模。
- 基于像素残差和光流的噪声初始化为帧间噪声引入运动先验，保持帧相关性，减少闪烁。
- ST-ReFL算法利用多种奖励模型对视频质量和运动一致性进行打分，并优化扩散模型，显著改善视频质量。
- 定量实验表明Control-A-Video在MUSIQ和ImageReward分数上分别比先前最佳模型提高+2.3和+0.36，且用户研究显示最佳文本对齐和一致性。
---

# Control-A-Video: Controllable Text-to-Video Diffusion Models with Motion Prior and Reward Feedback Learning

> [!tip] 核心洞察
> 通过第一帧内容先验解耦内容与运动建模，利用残差/光流驱动的运动先验保持帧间相关性，并引入时空奖励反馈学习（ST-ReFL）联合优化美学质量、技术质量与运动一致性，可显著提升可控视频生成的整体表现。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于运动先验与奖励反馈学习的可控文本到视频扩散模型 |
| 英文题名 | Control-A-Video: Controllable Text-to-Video Diffusion Models with Motion Prior and Reward Feedback Learning |
| 会议/期刊 | arXiv 2023 |
| Links | [paper](https://arxiv.org/abs/2305.13840) · [Project](https://controlavideo.github.io) · [arXiv](https://arxiv.org/abs/2210.14896) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Control-A-Video |
| Dataset |  |

> [!tip] 效果简介
> - 可控视频生成（自建测试集） 上，MUSIQ (技术质量) 73.3 vs ~71.0 (先前最佳模型) (+2.3)。
> - 可控视频生成 上，ImageReward (人类偏好) 1.03 vs ~0.67 (先前最佳模型) (+0.36)；Prompt CLIP Score (文本对齐) 0.290 vs 未明确指定最佳分数，但我们的方法最高 (最优)；Depth Map Error (控制一致性) 0.089 vs 未明确指定最佳分数，但我们的方法最低 (最低误差)。
> - 用户研究 上，一致性平均分 (1-5) 4.5 vs 未提供其他方法具体分，但我们的方法最佳 (最佳)。

## 概述

文本到视频（T2V）扩散模型虽已在生成质量上取得长足进步，但现有方法在**可控条件**下仍面临严峻瓶颈：帧间闪烁、物体外观不一致、运动失真等问题普遍存在，难以同时满足高质量与高一致性的要求。Control-A-Video（2023）针对这一困境，提出了一条**将内容与运动解耦**的技术路线，核心包含三个相互协同的杠杆：

1. **第一帧条件生成**：将视频生成转化为“文本到图像（T2I）→ 图像到视频（I2V）”的流水线，以第一帧作为内容先验，使模型继承图像域的成熟生成能力，同时将时间建模聚焦于运动而非内容。
2. **运动自适应噪声初始化**：摒弃逐帧独立高斯噪声，通过像素残差或光流从参考视频中提取运动先验，注入到后续帧的初始噪声中，从扩散过程的起点就保持帧间相关性，从根本上抑制闪烁。
3. **时空奖励反馈学习（ST-ReFL）**：在标准去噪损失之上，引入多奖励模型（技术质量、美学质量、运动一致性）对扩散输出进行打分并反馈优化，形成一个闭环的质量提升机制。

**方法定位**：Control-A-Video 建立在图像扩散模型 LDM 和 ControlNet 之上，通过插入可训练的 1D 时间层和时空自注意力机制实现时间建模。在方法谱系中，它区别于 **AnimateDiff**（Guo et al., arXiv 2023）的通用运动模块注入、**Text2Video-Zero**（Khachatryan et al., arXiv 2023）的零样本帧间约束、以及 **VideoComposer**（Wang et al., ICCV 2023）的组合式合成，其独特之处在于将运动先验注入噪声初始化阶段，并用奖励反馈直接优化生成质量。

**主要结果**：在可控视频生成基准上，Control-A-Video 的 MUSIQ（技术质量）分数达到 **73.3**，比先前最佳模型提升 **+2.3** 分；ImageReward（人类偏好）分数达到 **1.03**，提升 **+0.36** 分。用户研究进一步验证其在文本对齐和一致性上的最优表现（一致性平均分 4.5/5）。消融实验确认，去除运动先验会导致明显闪烁和伪影，而 ST-ReFL 的加入显著提升了清晰度和美观度。

## 背景与动机

文本到视频（Text-to-Video, T2V）生成旨在根据自然语言描述合成逼真且时序连贯的视频序列。随着扩散模型在图像生成领域的突破性进展，研究者开始将其扩展至视频域，涌现出如 **AnimateDiff**（Guo et al., arXiv 2023）、**Text2Video-Zero**（Khachatryan et al., arXiv 2023）和 **VideoComposer**（Wang et al., ICCV 2023）等代表性工作。然而，现有方法面临一个核心瓶颈：**难以同时保证生成视频的高质量与运动一致性**，尤其在引入额外控制条件（如深度图、边缘图）时，帧间闪烁和物体不一致问题尤为突出。

这一瓶颈的深层原因在于两个方面的建模困难。其一，视频生成需要同时建模空间内容与时间动态，而直接从噪声生成全部视频帧的方案将二者耦合在一起，使得模型难以继承图像域已有的强大生成能力。其二，标准扩散模型在初始化时采用逐帧独立的高斯噪声，缺乏对帧间运动关系的先验约束，导致去噪过程中相邻帧的潜在表示趋于发散，进而引发闪烁和背景扭曲。

针对上述问题，Control-A-Video 的动机在于寻找一个因果控制杠杆，将**内容建模与运动建模解耦**，并在噪声初始化阶段注入**运动先验**以维持帧间相关性。具体而言，该工作提出以第一帧作为内容先验，将图像域的生成能力迁移至视频生成，使后续帧的建模聚焦于运动变化；同时，通过基于像素残差或光流的运动自适应噪声初始化，为去噪过程提供帧间运动线索。在此基础上，进一步引入时空奖励反馈学习（ST-ReFL），利用多种奖励模型对视频的美学质量、技术质量与运动一致性进行联合打分并反馈优化，从而系统性地提升可控视频生成的整体表现。

## 核心创新

Control-A-Video 的核心创新在于将可控视频生成分解为两个解耦的子问题——内容生成与运动建模——并分别通过**第一帧内容先验**和**运动自适应噪声初始化**加以解决，最后引入**时空奖励反馈学习（ST-ReFL）**对整体质量进行联合优化。这一设计形成了“内容先验 → 运动注入 → 反馈精调”的三阶段闭环，显著提升了帧间一致性与视觉质量。

### 创新点一：第一帧内容先验与 T2I-I2V 流水线

传统文本到视频（T2V）扩散模型从纯噪声直接生成全部视频帧，导致内容与运动建模高度耦合，难以继承图像域已有的高质量生成能力。Control-A-Video 提出**第一帧条件方案**：将视频生成重新定义为“先生成高质量第一帧，再以该帧为条件生成后续帧”的 T2I-I2V 流水线。

具体而言，训练时模型学习在第一帧潜在表示 $\mathcal{E}(v^1)$ 的条件下预测噪声：

$$\min_{\theta} ||\epsilon - \epsilon_{\theta}(x_t, t, c_p, c_f, \mathcal{E}(v^1))||_2^2$$

推理时，第一帧由预训练的可控 T2I 模型生成（$v^1 = ControlT2I(x^1, c_p, c_f^1)$），后续帧则以 $\mathcal{E}(v^1)$ 为条件通过视频扩散模型生成。这一设计的**因果杠杆**在于：它将图像域成熟的生成能力完整迁移至视频生成，使模型只需专注于学习帧间运动关系，而非同时处理内容与运动。证据显示，该方案有效分离了内容与运动建模（confidence 0.95）。

### 创新点二：运动自适应噪声初始化

标准扩散模型使用逐帧独立的高斯噪声初始化，帧间噪声缺乏相关性，导致生成视频出现闪烁和物体不一致。Control-A-Video 提出两种将**运动先验注入初始噪声**的策略：

1. **残差噪声初始化（Residual-based）**：计算相邻帧像素残差，对超过阈值 $R_{thres}$ 的区域，将当前帧噪声替换为前一帧噪声与残差的组合，使噪声分布继承帧间运动信息。
2. **光流噪声初始化（Flow-based）**：基于源视频的光流场将前一帧噪声扭曲到当前帧位置，直接编码运动轨迹。

t-SNE 可视化（Figure 3）表明，相比于高斯噪声初始化，运动自适应噪声使各帧的噪声潜在表示分布更加聚集且保持有序结构，从几何上证明了运动先验的有效性。定性消融（Figure 5）进一步显示：去除运动先验后，视频出现明显闪烁和背景扭曲；而引入光流或残差先验后，背景保持稳定，主体运动连贯。定量消融（Table 2）亦验证了两种噪声初始化策略均优于基线（confidence 0.95）。

### 创新点三：时空奖励反馈学习（ST-ReFL）

传统扩散模型仅使用噪声预测损失进行训练，缺乏对视频整体质量和运动一致性的显式优化信号。Control-A-Video 提出 **ST-ReFL 算法**，在基础去噪训练完成后，引入多种奖励模型对生成视频进行打分，并通过反馈学习进一步微调模型。

ST-ReFL 的损失函数由两部分组成：

- **运动一致性损失**：结合残差运动奖励 $R_{mr}$ 和光流运动奖励 $R_{mf}$，鼓励生成视频与参考视频在运动模式上保持一致：
  $$L_{motion} = -\lambda_{mr} \cdot R_{mr}(v, v') - \lambda_{mf} \cdot R_{mf}(v, v')$$

- **质量损失**：利用 MUSIQ 技术质量评分 $R_{qt}$ 和美学预测器评分 $R_{qa}$，通过 ReLU 阈值机制鼓励视频质量超越预设边界：
  $$L_{quality} = \lambda_{qt} \cdot ReLU(b_{qt} - R_{qt}(v')) + \lambda_{qa} \cdot ReLU(b_{qa} - R_{qa}(v'))$$

总时空奖励损失为 $\mathcal{L}_{ST} = L_{motion} + L_{quality}$。定性消融（Figure 6）显示，加入 ST-ReFL 后视频清晰度和美观度显著提升；定量消融（Table 3）表明，组合所有奖励信号的完整 ST-ReFL 在所有指标上达到最优（confidence 0.95）。

### 创新点四：时空自注意力与可训练时间层

在架构层面，Control-A-Video 在预训练的图像扩散模型（LDMs）和 ControlNet 中插入了**可训练的 1D 时间层**，并引入**时空自注意力机制**。该机制将来自所有 $N$ 帧的 token 拼接为键 $K$ 和值 $V$，使每一帧的查询 $Q$ 能够感知全局时空上下文：

$$Q = W^Q \bar{v}_i, \quad K = W^K[\bar{v}_0,...,\bar{v}_{N-1}], \quad V = W^V[\bar{v}_0,...,\bar{v}_{N-1}]$$

这一设计使得模型能够在保持预训练图像生成能力的同时，高效捕获帧间依赖关系（confidence 0.9）。

### 方法谱系与知识库定位

Control-A-Video 处于**可控文本到视频扩散模型**的方法谱系中。其核心基线包括：

| 方法 | 核心差异 | 关键局限 |
|------|----------|----------|
| **AnimateDiff**（Guo et al., arXiv 2023） | 通过注入运动模块将个性化 T2I 模型适配为视频生成 | 缺乏显式控制信号，帧间一致性有限 |
| **Text2Video-Zero**（Khachatryan et al., arXiv 2023） | 零样本 T2V，利用跨帧注意力实现运动 | 无法利用视频数据进行训练优化 |
| **VideoComposer**（Wang et al., ICCV 2023） | 组合式视频合成，支持多模态条件 | 运动建模依赖组合空间，复杂运动下一致性不足 |

Control-A-Video 相对于上述方法的**关键 changed slots** 为：

1. **噪声初始化**：从逐帧独立高斯噪声 → 运动自适应噪声（残差/光流驱动），将运动先验前移至扩散过程的起点。
2. **生成范式**：从噪声直接生成全视频 → 第一帧条件生成（T2I-I2V），实现内容与运动的解耦。
3. **训练目标**：从仅标准去噪损失 → 标准损失 + ST-ReFL 反馈优化，引入多维度视频质量信号。
4. **时间建模**：从无额外时间层或简单时间注意力 → 可训练 1D 时间层 + 时空自注意力，增强帧间全局感知。

这些创新共同构成了一个从“内容生成 → 运动注入 → 质量精调”的完整可控视频生成框架，在 MUSIQ（+2.3）和 ImageReward（+0.36）等指标上显著超越先前最佳模型（confidence 0.98）。

## 整体框架

Control-A-Video 的整体 pipeline 围绕三个核心设计展开：**第一帧内容先验**、**运动自适应噪声初始化**与**时空奖励反馈学习（ST-ReFL）**。这三个组件构成一个从内容解耦、运动注入到质量对齐的级联优化闭环。

### 两阶段训练与推理流程

模型采用两阶段训练策略（Figure 2）。第一阶段为**噪声预测训练**：以第一帧的潜在表示作为内容先验，对后续帧施加运动感知噪声，训练时空去噪网络学习帧间依赖。第二阶段为**ST-ReFL 训练**：冻结第一阶段权重，将去噪输出的视频送入多个奖励模型（运动一致性奖励、技术质量奖励、美学质量奖励），以奖励信号反向优化扩散模型，实现质量与一致性的联合提升。

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2305_13840/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of the Control-A-Video pipeline. Architecture: Spatialtemporal self-attention and trainable temporal layers are applied to the UNet and ControlNet.(Temp denotes Temporal). (1) Noise Prediction Training: We add motion-aware noise to video latents (except the first frame) and train the model to predict the subsequent noise conditioned on the first frame, control maps, and text prompt. (2)ST-ReFL Training: A reward feedback loop optimizes the video diffusion model using (Aesthetic and Technical) Quality and Motion Rewards. It involves sampling*

推理时遵循 **T2I-I2V 流水线**：先用预训练的可控 T2I 模型从文本提示和控制图生成高质量第一帧 $v^1 = \text{ControlT2I}(x^1, c_p, c_f^1)$，再以该帧为条件，通过运动自适应噪声初始化和时空去噪网络生成后续帧 $v = \text{ControlT2V}(x, c_p, c_f, \mathcal{E}(v^1))$。

### 关键模块与数据流

1. **时空去噪网络**：在 LDM 和 ControlNet 的基础上插入可训练的 1D 时间层，并将空间自注意力扩展为时空自注意力机制。查询 $Q$ 来自第 $i$ 帧，键 $K$ 和值 $V$ 由所有 $N$ 帧的 token 拼接而成：
   $$Q = W^Q \bar{v}_i,\quad K = W^K[\bar{v}_0,...,\bar{v}_{N-1}],\quad V = W^V[\bar{v}_0,...,\bar{v}_{N-1}]$$
   这使得每一帧的去噪都能感知全部帧的时空上下文。

2. **运动自适应噪声初始化**：不再使用逐帧独立高斯噪声，而是从参考视频中提取运动先验注入初始噪声。残差噪声初始化计算相邻帧像素残差，对残差大于阈值 $R_{\text{thres}}$ 的区域传播运动信息；光流噪声初始化则基于光流场将前一帧噪声扭曲到下一帧位置。t-SNE 可视化（Figure 3）表明，这两种策略使噪声潜在表示在帧间保持更强的相关性，从而减少闪烁和背景扭曲。

3. **ST-ReFL 反馈优化**：总损失由运动一致性损失和质量损失加权组合：
   $$\mathcal{L}_{ST} = \underbrace{-\lambda_{mr} R_{mr} - \lambda_{mf} R_{mf}}_{L_{motion}} + \underbrace{\lambda_{qt} \cdot \text{ReLU}(b_{qt} - R_{qt}) + \lambda_{qa} \cdot \text{ReLU}(b_{qa} - R_{qa})}_{L_{quality}}$$
   其中 $R_{mr}$、$R_{mf}$ 分别为残差运动奖励和光流运动奖励，$R_{qt}$ 为 MUSIQ 技术质量分数，$R_{qa}$ 为美学预测器分数。ReLU 阈值机制鼓励模型超越预设的质量边界，而非无上限优化。

### 瓶颈与因果机制

现有视频扩散模型的核心瓶颈在于帧间闪烁和物体不一致——这源于独立噪声初始化破坏了帧间相关性，以及标准去噪损失无法显式约束时间一致性。Control-A-Video 的因果杠杆在于：**第一帧条件方案**将图像域的生成能力迁移到视频域，解耦内容与运动建模；**运动先验噪声**在扩散起点就注入帧间相关性，降低后续去噪的难度；**ST-ReFL** 则通过多维度奖励信号直接优化视频输出的感知质量和运动平滑度。三者协同作用，使得模型在 MUSIQ（+2.3）和 ImageReward（+0.36）上显著超越先前最佳模型。

## 核心模块与公式推导

### 整体架构：时空去噪网络

Control‑A‑Video 以预训练的图像扩散模型 **LDM** 和可控生成模型 **ControlNet** 为基础，在 UNet 与 ControlNet 中分别插入可训练的 **1D 时间层**，使模型具备时序建模能力。每一帧的特征先经过 2D 卷积层或空间注意力层，随后所有帧的帧级特征被拼接送入可训练的 1D 卷积层，实现帧间信息交互。

在此基础上，模型引入 **时空自注意力机制**，将空间与时间依赖关系联合建模，使每一帧的查询（Query）能够感知所有帧的键（Key）和值（Value），从而捕获跨帧的全局上下文。

### 时空自注意力

时空自注意力的核心公式为：

$$SelfAttn(Q,K,V) = Softmax(\frac{QK^T}{\sqrt{d}})V$$

其中，查询 $Q$、键 $K$、值 $V$ 由所有帧的 token 拼接而成：

$$Q = W^Q \bar{v}_i, \quad K = W^K[\bar{v}_0,...,\bar{v}_{N-1}], \quad V = W^V[\bar{v}_0,...,\bar{v}_{N-1}]$$

- $\bar{v}_i$：第 $i$ 帧的 token 表示；
- $[\bar{v}_0,...,\bar{v}_{N-1}]$：所有 $N$ 帧 token 的拼接；
- $W^Q, W^K, W^V$：可学习的投影矩阵；
- $d$：特征维度，用于缩放点积。

该设计的核心优势在于：查询来自当前帧，而键和值来自全部帧，使得每一帧在去噪过程中都能显式地参考其他帧的信息，从而增强帧间一致性。

### 第一帧条件生成

为解耦内容建模与运动建模，Control‑A‑Video 将第一帧作为内容先验。训练时，模型以第一帧的潜在表示 $\mathcal{E}(v^1)$ 为条件，学习去噪过程：

$$\min_{\theta} ||\epsilon - \epsilon_{\theta}(x_t, t, c_p, c_f, \mathcal{E}(v^1))||_2^2$$

- $\epsilon$：真实噪声；
- $\epsilon_{\theta}$：预测噪声；
- $x_t$：时间步 $t$ 的加噪潜在变量；
- $c_p$：文本提示条件；
- $c_f$：控制图条件（如深度图、边缘图）；
- $\mathcal{E}(v^1)$：第一帧的潜在编码。

推理时采用 **T2I‑I2V 流水线**：先用预训练的可控 T2I 模型生成第一帧 $v^1$，再以该帧为条件生成后续帧：

$$v^1 = ControlT2I(x^1, c_p, c_f^1)$$

$$v = ControlT2V(x, c_p, c_f, \mathcal{E}(v^1))$$

该方案将图像域的生成能力迁移至视频域，有效保证了首帧物体的内容一致性。

### 无分类器视频引导

为同时控制视频的整体平滑度和文本对齐度，论文设计了结合视频引导与文本引导的采样公式：

$$\hat{\epsilon}_{\theta}(x_t, t, c_p, c_f) = \epsilon_{\theta I}(x_t, t, \varnothing, c_f) + \omega_v (\epsilon_{\theta}(x_t, t, \varnothing, c_f) - \epsilon_{\theta I}(x_t, t, \varnothing, c_f)) + \omega_t (\epsilon_{\theta}(x_t, t, c_p, c_f) - \epsilon_{\theta}(x_t, t, \varnothing, c_f))$$

- $\epsilon_{\theta I}$：独立帧预测（仅以控制图为条件）；
- $\epsilon_{\theta}(x_t, t, \varnothing, c_f)$：无文本提示的视频预测；
- $\epsilon_{\theta}(x_t, t, c_p, c_f)$：完整条件的视频预测；
- $\omega_v$：视频引导尺度，控制帧间平滑度；
- $\omega_t$：文本引导尺度，控制文本对齐度。

该公式将无文本的视频预测与独立帧预测的差异作为视频引导项，将完整条件与无文本条件的差异作为文本引导项，实现解耦控制。

### 运动自适应噪声初始化

为在初始噪声中注入运动先验，论文提出两种互补策略：

**（1）基于像素残差的噪声初始化（Residual‑based Noise Initialization, RNI）**：计算相邻帧之间的像素残差，将残差超过阈值 $R_{thres}$ 的区域视为运动区域，仅在这些区域将当前帧噪声替换为前一帧噪声与残差的组合。阈值 $R_{thres}=0.1$ 被证明能在运动平滑性与非静态区域多样性之间取得平衡。

**（2）基于光流的噪声初始化（Optical Flow‑based Noise Initialization, FNI）**：利用参考视频的光流场将前一帧噪声扭曲到当前帧位置，使噪声模式随物体运动而传播。

两种策略均通过 Algorithm 1 实现，其核心思想是打破逐帧独立高斯噪声的假设，使相邻帧的初始噪声具有运动相关性，从而减少去噪过程中的帧间闪烁。

### 时空奖励反馈学习（ST‑ReFL）

在标准噪声预测训练完成后，Control‑A‑Video 引入 ST‑ReFL 对模型进行奖励驱动的微调。总损失由运动一致性损失和质量损失组成：

$$\mathcal{L}_{ST} = L_{motion} + L_{quality}$$

**运动一致性损失**：

$$L_{motion} = -\lambda_{mr} \cdot R_{mr}(v, v') - \lambda_{mf} \cdot R_{mf}(v, v')$$

- $R_{mr}$：基于像素残差的运动奖励模型；
- $R_{mf}$：基于光流的运动奖励模型；
- $v$：真实视频，$v'$：生成视频；
- $\lambda_{mr}, \lambda_{mf}$：权重超参数。

**质量损失**：

$$L_{quality} = \lambda_{qt} \cdot ReLU(b_{qt} - R_{qt}(v')) + \lambda_{qa} \cdot ReLU(b_{qa} - R_{qa}(v'))$$

- $R_{qt}$：基于 MUSIQ 的技术质量评分器；
- $R_{qa}$：基于美学预测器的美学质量评分器；
- $b_{qt}, b_{qa}$：质量阈值，通过 ReLU 鼓励生成视频超越该边界；
- $\lambda_{qt}, \lambda_{qa}$：权重超参数。

ST‑ReFL 的核心机制在于：利用多个预训练奖励模型对生成视频的帧级质量和时序一致性进行打分，并将这些信号反向传播以优化扩散模型参数，从而在不增加推理开销的前提下显著提升视频的清晰度、美观度和运动连贯性。

### 补充图表

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2305_13840/figures/003_Figure_3.jpg]]
*Figure 3: Motion-adaptive Noise Prior: t-SNE plot of noisy latents for video frames. Red: original video*

## 实验与分析

### 主要定量结果

Control-A-Video 在可控视频生成任务上全面超越现有基线方法。Table 1 汇总了与 **AnimateDiff** (Guo et al., arXiv 2023)、**Text2Video-Zero** (Khachatryan et al., arXiv 2023) 和 **VideoComposer** (Wang et al., ICCV 2023) 的定量对比，覆盖自动评估指标与用户研究两个维度。

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2305_13840/figures/005_Table_1.jpg]]
*Table 1: Comparison with other models. “Img-Re” is short for ImageReward and “Aespred” refers to Aesthetic-predictor*

在自动指标方面，Control-A-Video 在六项指标中的四项取得最优：**MUSIQ**（技术质量）达到 73.3，比先前最佳模型提升 +2.3 分；**ImageReward**（人类偏好）达到 1.03，提升 +0.36 分；**Prompt CLIP Score**（文本对齐）为 0.290，在所有方法中最高；**Depth Map Error**（控制一致性）为 0.089，在所有方法中最低。这表明模型在视频技术质量、人类偏好对齐、文本语义匹配以及控制信号保真度四个关键维度上均具备显著优势。

用户研究进一步验证了自动指标的结论。人类评估者对视频一致性进行 1-5 分评分，Control-A-Video 获得 4.5 的平均分，在所有对比方法中表现最佳。需要注意的是，用户研究仅报告了平均分，未提供标准差或显著性检验结果，统计可靠性需谨慎解读。

### 消融实验

#### 运动自适应噪声先验

噪声初始化策略的消融结果（Table 2）揭示了运动先验对视频质量的关键作用。以仅使用深度图控制的基础模型为基线，分别引入基于像素残差的噪声初始化（RNI）和基于光流的噪声初始化（FNI）。两种策略在各项指标上均优于基线，验证了运动自适应噪声先验的有效性。

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2305_13840/figures/007_Table_2.jpg]]
*Table 2: Quantitative ablation comparison for our noise initialization strategies in the first training stage. The baseline indicates the model trained with depth maps as control. RNI and FNI correspond to pixel residual-based and optical flow-based noise initialization*

定性消融（Figure 5）进一步展示了运动先验的视觉影响：去除运动先验后，生成视频出现明显的帧间闪烁和背景伪影；引入光流先验或残差先验后，背景保持稳定，主体运动连贯一致。残差噪声初始化中的阈值选择对运动平滑度与非静态区域多样性之间的平衡至关重要，论文指出阈值 0.1 能够有效兼顾两者，但该阈值在不同运动类型下的自适应调整机制尚未探索。

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2305_13840/figures/006_Figure_5.jpg]]
*Figure 5: Ablation study of motion-adaptive noise prior. (a) Input video. (b) Without motion prior, exhibiting flickering and artifacts. (c) With Optical Flow-based prior, maintaining consistency. (d) With Residual-based prior, stable background and coherent subject motion*

#### 时空奖励反馈学习（ST-ReFL）

ST-ReFL 的消融实验从两个层面展开。定性层面（Figure 6），对比引入 ST-ReFL 前后的三组视频示例，奖励反馈优化显著提升了视频的清晰度、美观度和帧间一致性，验证了运动奖励模型与质量奖励模型联合优化对扩散模型输出质量的改善效果。

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2305_13840/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative ablation study of ST-ReFL optimization. Three examples before and after ST-ReFL show improved consistency and quality through feedback tuning from motion and quality reward models*

定量层面（Table 3），系统消融了不同奖励信号组合的影响。仅使用基础模型（无奖励反馈）时各项指标最低；单独加入运动奖励或质量奖励均带来提升，但完整 ST-ReFL（联合运动奖励与质量奖励）在所有指标上达到最佳。这一结果证明，运动一致性奖励与美学/技术质量奖励之间存在互补效应，联合优化是实现高质量可控视频生成的必要条件。

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2305_13840/figures/009_Table_3.jpg]]
*Table 3: Ablation studies of different reward signals. The best scores are in bold and the second best scores are underlined*

#### 方法组件贡献总结

综合消融结果，Control-A-Video 的三个核心设计——第一帧条件生成方案、运动自适应噪声初始化、ST-ReFL 奖励反馈学习——各自贡献明确：第一帧条件方案将图像域生成能力迁移至视频域，解耦内容与运动建模；运动噪声先验维持帧间相关性，消除闪烁伪影；ST-ReFL 通过多维度奖励信号进一步精炼视频质量和运动一致性。三者协同作用，缺一不可。

### 失败模式与局限性

尽管 Control-A-Video 在整体表现上优势明显，仍存在若干值得关注的局限性：

1. **参考视频依赖**：运动自适应噪声先验的质量高度依赖参考视频。当参考视频本身存在运动模糊或不符合物理规律时，注入的运动先验可能引入不真实运动，导致生成视频出现物理不一致。

2. **奖励模型的静态评估偏差**：ST-ReFL 使用的奖励模型（MUSIQ 技术质量评估器、美学预测器）均基于静态图像评估设计，可能无法完全捕捉视频特有的时间质量缺陷，如时序抖动、运动模糊的连贯性等。

3. **训练数据规模限制**：训练仅使用约 0.1M 视频片段和 0.1M 图像-文本对，在更大规模、更多样化数据集上的泛化能力尚待验证。

4. **长视频生成挑战**：自回归方式生成长视频时，误差累积和一致性维持可能面临挑战。论文提及该方向但未给出系统性评估，该点需要手动验证。

5. **实验公平性考量**：基线方法的超参数调整细节未明确报告，可能影响对比公平性。用户研究未提供统计显著性检验，结论的统计可靠性需进一步确认。

### 开放问题

- 残差噪声初始化的阈值如何在复杂运动场景下自适应选择，是否需要动态调整？
- ST-ReFL 能否与基于人类反馈的强化学习（RLHF）相结合，进一步提升与人类偏好的对齐程度？
- 该方法对训练中未见过的控制图类型（如语义分割、姿态关键点）的泛化能力如何？
- 在实时或低延迟应用场景中，ST-ReFL 训练和推理流程的计算开销是否可接受？

### 补充图表

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2305_13840/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative Comparison: (a) Input video, (b) Animatediff, (c) Text2Video-Zero, (d) Videocomposer, (e) Ours. We showcase a challenging scenario of a fastmoving dog(left) and slow-moving(right) camel. Compared to other models, our method demonstrates superior performance in generating high-quality, temporally consistent results that accurately align with the given text prompt*

## 方法谱系与知识库定位

### 方法定位与核心贡献

Control-A-Video 处于文本到视频（T2V）扩散模型的可控生成分支，其核心设计思路是将图像域的可控生成能力迁移至视频域，同时引入运动先验与奖励反馈优化来解决帧间一致性这一瓶颈。该方法的技术基因可追溯至两条主线：

**图像扩散模型的视频化扩展。** 模型骨架基于 **LDM**（Rombach et al., CVPR 2022）与 **ControlNet**（Zhang & Agrawala, ICCV 2023），在 UNet 和 ControlNet 中插入可训练的 1D 时间层，并将空间自注意力替换为时空自注意力——这一架构选择与同期视频扩散模型（如 AnimateDiff, Guo et al., arXiv 2023）共享相似的设计范式。关键差异在于 Control-A-Video 采用**第一帧条件生成**策略（T2I→I2V 流水线），将内容建模与运动建模解耦：首帧由预训练 ControlT2I 生成，后续帧以首帧潜在表示为条件进行去噪。这一设计使模型得以继承图像域成熟的生成质量，同时将时间一致性的挑战聚焦于帧间运动建模。

**运动先验注入机制。** 区别于逐帧独立高斯噪声初始化的常规做法，Control-A-Video 提出两种运动自适应噪声初始化策略——基于像素残差的噪声初始化（RNI）和基于光流的噪声初始化（FNI）。其核心洞察在于：通过参考视频的帧间运动信息来构造初始噪声的帧间相关性，使去噪过程天然倾向于生成时间一致的帧序列。t-SNE 可视化（Figure 3）表明，残差噪声和光流噪声在扩散过程中维持了与原始视频更接近的潜在表示分布，而高斯噪声则迅速偏离。

**奖励反馈学习的引入。** ST-ReFL 算法将奖励模型驱动的反馈优化引入视频扩散模型训练，这是对图像域奖励反馈学习（如 ImageReward, Xu et al., NeurIPS 2023）的视频化延伸。ST-ReFL 联合优化四个奖励信号：基于残差的运动奖励 $R_{mr}$、基于光流的运动奖励 $R_{mf}$、MUSIQ 技术质量评分 $R_{qt}$ 和美学预测器评分 $R_{qa}$。总损失为运动一致性损失与质量损失的加权和：

$$L_{motion} = -\lambda_{mr} \cdot R_{mr}(v, v') - \lambda_{mf} \cdot R_{mf}(v, v')$$

$$L_{quality} = \lambda_{qt} \cdot \text{ReLU}(b_{qt} - R_{qt}(v')) + \lambda_{qa} \cdot \text{ReLU}(b_{qa} - R_{qa}(v'))$$

$$\mathcal{L}_{ST} = L_{motion} + L_{quality}$$

这种设计将视频质量的多维目标（技术质量、美学质量、运动平滑度）显式编码为可优化的损失项，而非仅依赖隐式的扩散去噪损失。

### 与同期方法的对比定位

| 方法 | 控制信号 | 运动建模策略 | 优化目标 | 关键差异 |
|------|---------|-------------|---------|---------|
| **AnimateDiff** (Guo et al., arXiv 2023) | 文本 | 时间注意力微调 | 标准扩散损失 | 无显式控制图，无运动先验注入 |
| **Text2Video-Zero** (Khachatryan et al., arXiv 2023) | 文本+控制图 | 跨帧注意力+光流变形 | 标准扩散损失 | 零样本，但缺乏训练阶段的运动建模 |
| **VideoComposer** (Wang et al., ICCV 2023) | 文本+多模态控制 | 组合式条件融合 | 标准扩散损失 | 多模态控制，但无奖励反馈优化 |
| **Control-A-Video** (本文) | 文本+控制图 | 运动自适应噪声初始化+时空自注意力 | 标准扩散损失+ST-ReFL | 首帧条件解耦+运动先验+奖励反馈 |

Control-A-Video 的独特优势在于将三个设计要素——**首帧条件解耦**、**运动自适应噪声先验**和**时空奖励反馈学习**——整合为统一的训练-推理框架。定量对比（Table 1）显示，该方法在 MUSIQ 技术质量（+2.3）和 ImageReward 人类偏好（+0.36）上显著超越先前最佳模型，且用户研究中一致性评分达到 4.5/5.0。

### 适用边界与局限

**数据依赖性。** 运动自适应噪声初始化依赖参考视频的帧间运动质量。当参考视频本身存在运动模糊、剧烈抖动或不符合物理规律的运动时，注入的运动先验可能引入不真实运动模式。论文未系统评估参考视频质量退化对生成结果的影响。

**奖励模型的静态偏差。** ST-ReFL 使用的 MUSIQ 和美学预测器均基于静态图像质量评估训练，可能无法完全捕捉视频特有的时间质量缺陷（如闪烁、跳帧、运动伪影）。尽管引入了运动奖励模型作为补充，但运动奖励本身也基于参考视频的帧间差异计算，存在循环依赖风险。

**训练数据规模。** 训练仅使用约 0.1M 视频片段和 0.1M 图像-文本对，远小于大规模视频生成模型（如 Sora 级别的数据规模）。在更广泛场景下的泛化性尚待验证。

**长视频生成。** 论文提及自回归生成长视频的可能性，但未给出系统性评估。在自回归范式下，误差累积和长程一致性维持可能面临挑战。

**控制图类型泛化。** 实验主要验证了深度图、Canny 边缘和 HED 边缘三种控制图类型。对未见的控制图类型（如语义分割、姿态关键点、法线图）的泛化能力未被评估。

### 开放问题

1. **自适应阈值选择。** 残差噪声初始化中的阈值（论文选择 0.1）如何在不同运动类型（快速运动 vs. 缓慢运动、刚性运动 vs. 非刚性形变）下自适应调整？是否存在基于运动幅度的动态阈值策略？

2. **与 RLHF 的整合。** ST-ReFL 目前使用预定义奖励模型，能否与基于人类反馈的强化学习（RLHF）框架结合，通过人类标注者对视频质量和一致性的偏好反馈来进一步对齐人类感知？

3. **多控制图融合。** 当同时提供多种控制图（如深度图+边缘图）时，如何协调不同控制信号之间的潜在冲突？首帧条件方案是否足以处理多模态控制信号的融合？

4. **实时性约束。** ST-ReFL 训练需要额外的奖励模型前向传播和梯度回传，推理时的分类器自由引导（视频引导+文本引导）也增加了采样步数的计算开销。在实时或低延迟应用场景中，这些额外开销是否可接受？是否存在模型蒸馏或一步采样的加速方案？

5. **运动先验的物理合理性。** 基于残差和光流的运动先验本质上是数据驱动的统计先验，不包含物理约束（如刚体运动约束、碰撞检测）。在生成物理交互场景（如物体碰撞、流体运动）时，是否会出现违反物理规律的运动？

---

**证据强度说明：** 上述方法定位和比较分析基于论文提供的定量实验（Table 1, Table 2, Table 3）和定性消融（Figure 4-6），置信度较高。关于局限和开放问题的讨论部分基于论文自身的局限性声明，部分基于方法设计的逻辑推演，置信度中等，需后续工作验证。

## 原文 PDF

![[paperPDFs/arxiv_2023/Control_A_Video_Controllable_Text_to_Video_Diffusion_Models_with_Motion_Prior_and_Reward_Feedback_Learning.pdf]]