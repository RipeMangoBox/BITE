---
title: "MoMu-Diffusion: On Learning Long-Term Motion-Music Synchronization and Correspondence"
type: paper
paper_level: A
venue: NEURIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/MoMu_Diffusion_On_Learning_Long_Term_Motion_Music_Synchronization_and_Correspondence.pdf
project_link: https://momu-diffusion.github.io/
code_link: https://github.com/gudgud96/
aliases:
- MD
- MoMu-Diffusion
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 双向对比节奏变分自编码器 (BiCoR-VAE) 显式对齐运动与音乐的节奏模式，配合基于Transformer的扩散模型捕捉长期依赖关系。
primary_logic: 通过潜在空间的节奏对比学习强制运动和音乐表征在时序与节拍上对齐，并利用Transformer的全局建模能力，可以生成长时间、节拍同步且多样化的运动或音乐序列。
claims:
- BiCoR-VAE能够提取运动与音乐的模态对齐潜在表示，实现节奏对齐。
- MoMu-Diffusion在运动到音乐的生成质量和节拍匹配指标上全面超越现有的最先进方法（如LORIS）。
- 节奏对比学习显著提升了节拍匹配性能（F1），消融实验证明移除该组件会导致F1大幅下降。
- 基于Transformer的扩散架构（FFT）相比U-Net进一步提升了合成质量（FAD/FID）。
---

# MoMu-Diffusion: On Learning Long-Term Motion-Music Synchronization and Correspondence

> [!tip] 核心洞察
> 通过潜在空间的节奏对比学习强制运动和音乐表征在时序与节拍上对齐，并利用Transformer的全局建模能力，可以生成长时间、节拍同步且多样化的运动或音乐序列。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoMu-Diffusion：学习长期运动-音乐同步与对应 |
| 英文题名 | MoMu-Diffusion: On Learning Long-Term Motion-Music Synchronization and Correspondence |
| 会议/期刊 | NEURIPS 2024 |
| Links | [Project](https://momu-diffusion.github.io/) · [Code](https://github.com/gudgud96/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MoMu-Diffusion |
| Dataset | AIST++ Dance, Floor Exercise-25s, Figure Skating-25s, BHS Dance |

> [!tip] 效果简介
> - AIST++ Dance (motion-to-music) 上，BCS↑ 97.5 vs 96.5 (LORIS) (+1.0)；BHS↑ 98.6 vs 90.8 (LORIS) (+7.8)。
> - Floor Exercise-25s (motion-to-music) 上，BCS↑ 66.6 vs 58.8 (LORIS) (+7.8)。
> - Figure Skating-25s (motion-to-music) 上，F1↑ 69.0 vs 62.7 (LORIS) (+6.3)。

## 概要

**核心问题**：长序列运动与音乐的跨模态生成面临两大瓶颈——高计算成本使得长时域建模困难，且现有方法缺乏在潜在空间中显式对齐时序同步与节奏的能力。

**方法定位**：本文提出 **MoMu-Diffusion**，一个面向运动-音乐双向生成与多模态联合生成的统一框架。其核心创新是 **双向对比节奏变分自编码器（BiCoR-VAE）**，通过节奏对比学习（Rhythmic Contrastive Learning）在潜在空间中强制对齐运动与音乐的节拍模式；在此基础上，采用基于 Transformer 的扩散模型（DiT 架构）捕捉长程依赖，并设计无需额外训练的交叉引导采样策略实现多模态联合生成。

**主要结论**：
- 在运动到音乐生成任务上，MoMu-Diffusion 的节拍匹配指标显著超越现有最先进方法 **LORIS**（AIST++ Dance 上 BHS 提升 7.8 个百分点，Floor Exercise 上 BCS 提升 7.8 个百分点），同时生成质量指标 FAD 全面占优。
- 在音乐到运动生成任务上，FID 相较 **D2M** 降低 10.0（7.3 vs 17.3），节拍 F1 相较 **DiffGesture** 提升 9.2 个百分点。
- 消融实验证实：移除节奏对比学习导致节拍 F1 大幅下降（音乐端从 98.1 降至 93.1，运动端从 45.4 降至 37.9）；用 U-Net 替换 Transformer 使 FAD 和 FID 明显劣化。

**方法谱系与知识库定位**：MoMu-Diffusion 属于 **潜在空间对齐 + 扩散生成** 范式。与仅依赖时间对比或独立生成的运动-音乐方法（如 LORIS、D2M-GAN、CDCD）不同，BiCoR-VAE 显式建模节奏同步，使扩散模型能在对齐的紧凑潜在空间中高效生成。其 Transformer 扩散架构区别于 U-Net 系方法（如 DiffGesture），更适合长序列全局建模。交叉引导采样则提供了一种即插即用的多模态联合生成方案，无需额外训练。

### 运动与音乐生成的核心瓶颈

运动与音乐的联合生成是跨模态理解与合成中的关键问题，其目标是在时序上实现两种模态的精确同步与语义对应。现有方法面临两个相互耦合的根本性瓶颈：

**长序列建模的计算成本**。运动序列和音乐信号本质上都是高维长序列数据。原始音频波形的采样率极高（通常 16–44.1 kHz），直接建模会导致序列长度呈指数级膨胀，使生成模型（尤其是基于扩散的方法）在训练和推理时面临难以承受的计算开销。

**潜在空间中的时序同步缺失**。大多数现有工作将运动与音乐分别编码到独立的潜在空间后，依赖简单的时间对齐或隐式条件进行跨模态生成。然而，这些方法并未在潜在表示层面显式地强制运动与音乐在节奏模式上的对齐——即运动的“击节”（kinematic beats）与音乐的“节拍”（musical beats）之间的对应关系。缺乏这种显式对齐机制，模型难以捕捉运动-音乐在节拍层级上的细粒度同步，导致生成结果在节奏一致性上表现不佳。

### 现有方法缺口

**运动到音乐生成**。现有方法可大致分为基于 GAN 的方法（如 **D2M-GAN**）、基于 Transformer 的可控音乐生成方法（如 **CMT**）以及基于扩散模型的方法（如 **CDCD** 和 **LORIS**）。其中，**LORIS** 作为当前最先进的层级扩散方法，在生成质量和节拍匹配上表现突出，但其依然缺乏在潜在空间中对运动与音乐节奏模式进行显式对比对齐的机制。

**音乐到运动生成**。该方向的方法包括基于分解-组合策略的 **D2M** 和基于 U-Net 扩散的 **DiffGesture** 等。这些方法通常将运动生成视为条件序列生成任务，但同样未在潜在空间中显式建模音乐节拍与运动节奏之间的对应关系。

**共性缺口**。综合来看，现有方法的共性缺口在于：缺少一个统一的潜在空间，能够将运动与音乐的节奏模式进行显式对齐，从而为下游的扩散生成模型提供模态对齐的表示基础。此外，大多数扩散模型仍采用 U-Net 架构，其在捕捉长序列中的全局时序依赖方面能力有限。

### 本文动机

针对上述瓶颈与缺口，本文提出 **MoMu-Diffusion**，其核心动机可归纳为两个层面：

1. **通过节奏对比学习实现潜在空间对齐**。设计一个双向对比节奏变分自编码器（BiCoR-VAE），利用运动幅度指示器（kinematic amplitude indicator）作为节奏代理信号，在潜在空间中强制运动与音乐在节拍层级上对齐。这一机制使模型能够显式捕捉跨模态的节奏对应关系，为后续生成提供结构化的潜在表示。

2. **利用 Transformer 扩散架构实现长序列全局建模**。采用基于 Transformer 的扩散模型（DiT 架构）替代传统 U-Net，以更好地捕捉运动与音乐序列中的长期时序依赖。配合交叉引导采样策略，模型能够在无需额外训练的情况下实现多模态联合生成，并支持变长序列的灵活合成。

## 核心方法与创新机理

MoMu-Diffusion 针对长序列运动-音乐生成中**高计算成本**与**缺乏显式时序同步能力**的双重瓶颈，提出了三个层次的创新，构成了一套从潜在空间对齐到跨模态生成的完整技术方案。

### 创新一：双向对比节奏变分自编码器 (BiCoR-VAE)

这是整个框架的核心创新，直接回应了“如何在潜在空间中显式对齐运动与音乐的节奏模式”这一关键问题。BiCoR-VAE 由运动 VAE、音乐 VAE 和**节奏对比学习 (Rhythmic Contrastive Learning, RCL)** 三个组件构成，其设计逻辑如下：

**运动幅度指示器。** 不同于直接使用原始关键点坐标，MoMu-Diffusion 首先从 2D 姿态关键点的一阶差分构建**运动直接图 (directogram)**，将运动变化量按角度分桶聚合，量化运动的空间分布。在此基础上，逐帧计算直接图差值的正部分，得到**运动幅度指示器** $Q(r)$，用于捕捉运动的节奏性变化：

$$Q(r) = \sum_{k=1}^{K} \max(0, |D(r,k)| - |D(r-1,k)|)$$

**节奏对比损失。** 在获得运动幅度指示器后，BiCoR-VAE 从运动潜在序列和音乐潜在序列中采样片段并进行最大池化，得到片段级表征 $c_m$ 和 $c_a$。然后通过双向对比损失强制同时刻的运动-音乐对在潜在空间中靠近，不同时刻或不同节奏的对远离：

$$\mathcal{L}_{\mathrm{contrast}} = -\frac{1}{2}\log\frac{\exp(sim(c_a^i, c_m^j)/\tau)}{\sum_{c=1}^{N_C}\exp(sim(c_a^i, c_m^c)/\tau)} - \frac{1}{2}\log\frac{\exp(sim(c_a^i, c_m^j)/\tau)}{\sum_{c=1}^{N_C}\exp(sim(c_a^c, c_m^j)/\tau)}$$

**消融实验直接验证了这一创新的因果作用。** 移除节奏对比学习后，节拍匹配指标 F1 出现显著下降：音乐端从 98.1 降至 93.1，运动端从 45.4 降至 37.9（Table 7）。这说明 RCL 是 BiCoR-VAE 实现模态对齐的关键机制，而非 VAE 架构本身的附带效果。

### 创新二：基于 Transformer 的扩散架构 (FFT)

传统扩散模型在运动-音乐生成中普遍采用 U-Net 架构。MoMu-Diffusion 转向 **Transformer (DiT) 架构**，利用其全局自注意力机制捕捉长序列中的长期依赖关系。这一设计选择的动机在于：运动与音乐的同步不仅需要局部节拍对齐，还需要理解整个序列的节奏结构和情感走向。

消融实验表明，用 U-Net 替换 Transformer 后，合成质量指标 FAD 从 8.1 上升至 11.0，FID 从 8.8 上升至 11.6（Table 7），证实了 Transformer 架构在长序列生成任务中的优势。

### 创新三：交叉引导采样策略

MoMu-Diffusion 提出了一种**无需额外训练**的多模态联合生成机制。在采样过程中，前 $T_c$ 步执行无条件生成，之后利用估计的干净潜在表示进行条件生成，通过无分类器引导实现跨模态约束：

$$\hat{\epsilon}_{\theta_a}(z_a(t), t, z_m) = \epsilon_{\theta_a}(z_a(t), t, \emptyset) + s \cdot (\epsilon_{\theta_a}(z_a(t), t, z_m) - \epsilon_{\theta_a}(z_a(t), t, \emptyset))$$

这一策略的关键优势在于：可以将独立训练的运动到音乐和音乐到运动两个专家模型组合起来，实现多模态联合生成，而无需重新训练。消融实验显示，交叉引导步长 $T_c$ 在 $0.5T$ 时达到生成质量与跨模态对齐的最佳折衷（Table 10）。

### 辅助创新：Mel-spectrogram 替代原始波形

MoMu-Diffusion 使用 mel-spectrogram 替代原始波形作为音频表示，有效缩短了序列长度，缓解了长序列建模的计算压力。消融实验中，使用原始波形导致 FAD 从约 8.1 上升至 12.8（Table 7），验证了这一设计选择的有效性。

### 创新总结

| 创新点 | 基线方案 | MoMu-Diffusion 方案 | 证据强度 |
|--------|----------|---------------------|----------|
| 时序对齐机制 | 无专门对齐或简单时间对比 | 节奏对比学习 (RCL)，基于运动幅度指示器 | 强 (消融实验 F1 大幅下降) |
| 扩散模型架构 | U-Net | Transformer (DiT) | 强 (消融实验 FAD/FID 显著劣化) |
| 多模态联合生成 | 独立训练的单模态模型 | 交叉引导采样 (无需额外训练) | 中等 (超参数 $T_c$ 需调优) |
| 音频特征表示 | 原始波形 | Mel-spectrogram | 强 (消融实验 FAD 上升) |

这些创新共同构成了 MoMu-Diffusion 的技术壁垒：BiCoR-VAE 解决了“对齐”问题，Transformer 扩散模型解决了“长序列建模”问题，交叉引导采样解决了“多模态联合生成”问题，三者协同作用，使模型在运动-音乐双向生成任务上全面超越现有方法。

MoMu-Diffusion 的整体 pipeline 围绕一个核心瓶颈展开：**长序列运动与音乐的跨模态生成需要同时解决高计算成本与显式时序同步两大难题**。为此，框架将任务分解为两个紧密耦合的阶段，形成从原始模态输入到最终生成输出的端到端流程。

### 框架总览

整个框架由两大核心组件构成（见图 2）：

1. **双向对比节奏变分自编码器 (BiCoR-VAE)**：负责学习运动与音乐的模态对齐潜在表示，是整个系统的对齐基础。
2. **基于 Transformer 的扩散模型 (FFT/DiT)**：在 BiCoR-VAE 构建的对齐潜在空间之上，执行跨模态条件生成，捕捉长序列中的全局依赖关系。

此外，框架引入了**交叉引导采样策略**，使得多个专家模型无需额外训练即可协同完成多模态联合生成。

### 数据流与模块关系

#### 输入预处理

- **运动模态**：从视频中提取 2D 关键点（OpenPose），并计算运动直接图（directogram）与运动幅度指示器 $Q(r)$，用于后续节奏对比学习。
- **音乐模态**：提取 mel-spectrogram 作为音频表示，替代原始波形以缓解序列长度带来的计算压力。

#### 第一阶段：BiCoR-VAE 的潜在空间对齐

BiCoR-VAE 采用两阶段训练策略构建对齐的潜在空间：

- **阶段一**：训练音乐 VAE，使用 VAE 损失与 GAN 损失联合优化，防止 mel-spectrogram 的过度平滑：
  $$\mathcal{L}_{stage1} = \mathcal{L}_{recon} + \lambda_{1} \mathcal{L}_{KL} + \lambda_{2} \mathcal{L}_{GAN}$$
  
- **阶段二**：固定音乐 VAE，训练运动 VAE，并引入节奏对比损失实现跨模态对齐：
  $$\mathcal{L}_{stage2} = \mathcal{L}_{recon} + \lambda_{3} \mathcal{L}_{KL} + \lambda_{4} \mathcal{L}_{contrast}$$

运动 VAE 将 2D 关键点编码为潜在表示 $z_m = E_m(m) \in \mathbb{R}^{T_{zm} \times d}$，音乐 VAE 将 mel-spectrogram 编码为 $z_a = E_a(a) \in \mathbb{R}^{T_{za} \times d}$。节奏对比学习的核心机制是：通过运动幅度指示器 $Q(r)$ 识别运动中的节奏峰值，与音乐的节拍点形成正样本对，最大化同时刻运动-音乐对的相似度，最小化不同时刻对的相似度，从而在潜在空间中显式对齐两者的时序与节拍模式。

#### 第二阶段：Transformer 扩散模型的跨模态生成

在对齐的潜在空间中，框架部署基于 Transformer 的扩散模型（DiT 架构）进行条件生成。与传统的 U-Net 扩散架构相比，Transformer 的自注意力机制能够更有效地捕捉长序列中的全局依赖关系。

训练时，扩散模型学习从带噪潜在表示中恢复干净信号。以运动到音乐生成为例，前向扩散过程逐步向音乐潜在表示添加噪声：
$$q(z_a(t)|z_a(t-1)) = \mathcal{N}(z_a(t); \sqrt{\alpha_t} z_a(t-1), (1-\alpha_t) \mathbf{I})$$

训练目标为最小化噪声预测误差：
$$\mathcal{L}_{\mathrm{m2a}} = ||\epsilon_{\theta_a}(z_a(t), t, z_m) - \epsilon||_2^2$$

音乐到运动方向的训练目标 $\mathcal{L}_{\mathrm{a2m}}$ 结构对称。

#### 第三阶段：交叉引导采样与多模态联合生成

推理时，框架采用无分类器引导采样：
$$\hat{\epsilon}_{\theta_a}(z_a(t), t, z_m) = \epsilon_{\theta_a}(z_a(t), t, \emptyset) + s \cdot (\epsilon_{\theta_a}(z_a(t), t, z_m) - \epsilon_{\theta_a}(z_a(t), t, \emptyset))$$

对于多模态联合生成，交叉引导采样策略在扩散步长 $t > T_c$ 时执行无条件逆向采样，在 $t \leq T_c$ 时引入跨模态条件引导。具体而言，从带噪潜在变量估计干净潜在表示 $\hat{z_a}$，用以条件化另一模态的生成过程。消融实验表明，$T_c = 0.5T$ 时在生成质量与跨模态对齐之间取得最佳折衷。

#### 输出解码

- **音乐输出**：扩散模型生成的 mel-spectrogram 潜在表示经音乐 VAE 解码器还原为 mel-spectrogram，再通过 BigvGAN Vocoder 转换为高保真音频波形。
- **运动输出**：生成的潜在表示经运动 VAE 解码器还原为 2D 关键点序列。

### 关键设计决策的因果链

整个框架的设计逻辑遵循一条清晰的因果链：

1. **瓶颈识别**：长序列生成的高计算成本 + 缺乏显式时序对齐能力 → 需要压缩表示与对齐机制。
2. **因果调节变量**：BiCoR-VAE 的节奏对比学习显式对齐运动与音乐的节奏模式 → 节拍匹配性能的根本保障（消融实验中移除 RCL 导致音乐端 F1 从 98.1 降至 93.1，运动端 F1 从 45.4 降至 37.9）。
3. **架构选择**：Transformer 替代 U-Net → 全局依赖建模能力提升，FAD 从 11.0 降至 8.1，FID 从 11.6 降至 8.8。
4. **表示选择**：mel-spectrogram 替代原始波形 → 序列长度压缩，FAD 从 12.8 降至约 8.1。

这一设计使得 MoMu-Diffusion 能够支持三种生成模式：**跨模态生成**（运动→音乐、音乐→运动）、**多模态联合生成**（同时生成运动与音乐）以及**变长序列生成**，在统一的框架下实现了长时间、节拍同步且多样化的运动-音乐合成。

### 补充图表

![[assets/figures/papers/paper_list_l1914_MoMu_Diffusion_On_Learning_Long_Term_Motion_Music_Synchronization_and_Co/figures/003_Figure_2.jpg]]
*Figure 2: An overview of the proposed MoMu-Diffusion framework. MoMu-Diffusion contains two integral components: a bidirectional contrastive rhythmic Variational Autoencoder (BiCoR-VAE) designed to learn the aligned latent space, and a Transformer-based diffusion model responsible for sequence generation. This framework is adept at facilitating both cross-modal and multi-modal joint generations, offering a robust approach to the integrated synthesis of motion and music*

![[assets/figures/papers/paper_list_l1914_MoMu_Diffusion_On_Learning_Long_Term_Motion_Music_Synchronization_and_Co/figures/001_Figure_1.jpg]]
*Figure 1: The pipeline of MoMu-Diffusion. MoMu-Diffusion integrates the alignment of motion and music through the novel Bidirectional Contrastive Rhythmic Auto-Encoder (BiCoR-VAE). Leveraging the aligned latent space, MoMu-Diffusion facilitates both cross-modal and multi-modal generations*

### 双向对比节奏变分自编码器 (BiCoR-VAE)

MoMu-Diffusion 的核心对齐能力源自 BiCoR-VAE，它由三个紧密耦合的子模块构成：运动 VAE、音乐 VAE 和节奏对比学习（RCL）。其设计目标是在潜在空间中显式对齐运动与音乐的时序同步与节拍模式，为下游扩散模型提供模态对齐的紧凑表示。

**运动 VAE** 以 2D 关键点序列作为输入，编码为潜在表示 $z_m = E_m(m) \in \mathbb{R}^{T_{zm} \times d}$。**音乐 VAE** 以 mel-spectrogram 作为输入，编码为潜在表示 $z_a = E_a(a) \in \mathbb{R}^{T_{za} \times d}$。两者共享相同的潜在维度 $d$，为后续对比学习提供统一的度量空间。

训练采用两阶段策略：第一阶段训练音乐 VAE，使用 VAE 损失与 GAN 损失的组合以防止 mel-spectrogram 过平滑；第二阶段固定音乐 VAE 参数，训练运动 VAE 并联合节奏对比损失，迫使运动潜在空间向音乐节奏模式对齐。

### 运动幅度指示器

节奏对比学习需要一个能够表征运动强度的标量信号。论文从运动直接图（directogram）出发，构造了运动学幅度指示器。

首先，对每一帧的运动关键点计算一阶差分，并按方向角度分桶聚合，得到 2D 运动直接图：

$$D(r,\theta) = \sum_{j=1}^{J} ||F(r,j)||_2 \mathbb{1}_{\theta}(\angle F(r,j)), \quad \mathrm{where } \mathbb{1}_{\theta}(\phi) := \begin{cases} 1, & |\theta-\phi| \le 2\pi/K, \\ 0, & \mathrm{otherwise}. \end{cases}$$

其中 $F(r,j)$ 表示第 $r$ 帧第 $j$ 个关键点的一阶差分向量，$K$ 为角度分桶数。该公式将运动变化量按 $K$ 个方向区间聚合，量化运动的空间分布。

在此基础上，逐帧计算直接图差值的正部分之和，得到运动学幅度指示器：

$$Q(r) = \sum_{k=1}^{K} \max(0, |D(r,k)| - |D(r-1,k)|)$$

$Q(r)$ 捕捉了相邻帧之间运动变化量的净增量，作为该帧运动强度的代理信号。该信号随后用于指导对比学习中的正负样本选择。

### 节奏对比损失

为建立运动与音乐在节奏层面的显式对齐，论文从潜在序列中采样片段并进行最大池化，构建对比学习样本：

$$c_a^{r_s:r_c} = P_{\max}(z_a^{r_s}:z_a^{r_c}), \quad c_m^{r_s:r_c} = P_{\max}(z_m^{r_s}:z_m^{r_c}), \quad Q(r_s:r_e) = \max(Q(r_s):Q(r_e))$$

正样本对定义为同一时间窗口内运动幅度与音乐能量均处于高位的片段，负样本对则为时间窗口不匹配或节奏强度不匹配的片段。

双向对比损失函数为：

$$\mathcal{L}_{\mathrm{contrast}} = -\frac{1}{2}\log\frac{\exp(sim(c_a^i, c_m^j)/\tau)}{\sum_{c=1}^{N_C}\exp(sim(c_a^i, c_m^c)/\tau)} - \frac{1}{2}\log\frac{\exp(sim(c_a^i, c_m^j)/\tau)}{\sum_{c=1}^{N_C}\exp(sim(c_a^c, c_m^j)/\tau)}$$

其中 $sim(\cdot,\cdot)$ 为余弦相似度，$\tau$ 为温度系数。该损失同时最大化正样本对的相似度，并最小化负样本对的相似度，从运动和音乐两个方向施加约束，迫使潜在空间在节奏维度对齐。

### Transformer 扩散模型

在获得模态对齐的潜在表示后，MoMu-Diffusion 采用基于 Transformer 的扩散模型（DiT 架构）进行跨模态条件生成。相比传统的 U-Net 架构，Transformer 的自注意力机制能够更有效地捕捉长序列中的全局依赖关系。

前向扩散过程逐步向音乐潜在表示添加高斯噪声：

$$q(z_a(t)|z_a(t-1)) = \mathcal{N}(z_a(t); \sqrt{\alpha_t} z_a(t-1), 1-\alpha_t \mathbf{I})$$

跨模态生成的训练目标为预测添加的噪声：

$$\mathcal{L}_{\mathrm{m2a}} = ||\epsilon_{\theta_a}(z_a(t), t, z_m) - \epsilon||_2^2, \quad \mathcal{L}_{\mathrm{a2m}} = ||\epsilon_{\theta_m}(z_m(t), t, z_a) - \epsilon||_2^2$$

其中 $\mathcal{L}_{\mathrm{m2a}}$ 为运动到音乐的损失，$\mathcal{L}_{\mathrm{a2m}}$ 为音乐到运动的损失。两个方向的扩散模型独立训练，分别学习以另一模态为条件的去噪过程。

### 交叉引导采样策略

为实现多模态联合生成（同时生成运动与音乐），论文提出交叉引导采样策略，无需额外训练即可组合两个专家模型。其核心思想是：在扩散采样的早期阶段（$T \geq t > T_c$）进行无条件生成，在后期阶段（$T_c \geq t$）引入交叉条件引导。

无条件逆向步骤的均值和方差定义为：

$$\mu_{\theta_a}(z_a(t), t, \emptyset) = \frac{1}{\sqrt{\alpha_t}} (z_a(t) - \frac{1-\alpha_t}{\sqrt{1-\overline{\alpha}_t}} \epsilon_{\theta_a}(z_a(t), t, \emptyset)), \quad \sigma^2 = \frac{1-\overline{\alpha}_{t-1}}{1-\overline{\alpha}_t} (1-\alpha_t)$$

进入交叉引导阶段后，首先从带噪潜在变量估计干净潜在表示：

$$\hat{z_a} = \frac{z_a(t)}{\sqrt{\overline{\alpha}_t}} - \frac{\sqrt{1-\overline{\alpha}_t}}{\sqrt{\overline{\alpha}_t}} \epsilon_{\theta_a}(z_a(t), t, \emptyset)$$

然后使用无分类器引导进行条件生成：

$$\hat{\epsilon}_{\theta_a}(z_a(t), t, z_m) = \epsilon_{\theta_a}(z_a(t), t, \emptyset) + s \cdot (\epsilon_{\theta_a}(z_a(t), t, z_m) - \epsilon_{\theta_a}(z_a(t), t, \emptyset))$$

其中 $s$ 为引导强度。交叉引导步 $T_c$ 是一个关键超参数——消融实验表明 $T_c = 0.5T$ 时能在生成质量与跨模态一致性之间取得最佳折衷。

### 训练损失汇总

BiCoR-VAE 的两阶段训练目标分别为：

第一阶段（音乐 VAE + GAN）：

$$\mathcal{L}_{stage1} = \mathcal{L}_{recon} + \lambda_{1} \mathcal{L}_{KL} + \lambda_{2} \mathcal{L}_{GAN}$$

第二阶段（运动 VAE + 对比学习）：

$$\mathcal{L}_{stage2} = \mathcal{L}_{recon} + \lambda_{3} \mathcal{L}_{KL} + \lambda_{4} \mathcal{L}_{contrast}$$

其中 $\mathcal{L}_{recon}$ 为重建损失，$\mathcal{L}_{KL}$ 为 KL 散度正则项，$\mathcal{L}_{GAN}$ 为对抗损失，$\mathcal{L}_{contrast}$ 为前述节奏对比损失。$\lambda_1$ 至 $\lambda_4$ 为各损失项的权重系数。

### 关键模块的因果作用链

BiCoR-VAE 的节奏对比学习是本文最核心的因果调节旋钮。消融实验直接验证了其作用：移除 RCL 后，音乐端节拍匹配 F1 从 98.1 降至 93.1，运动端 F1 从 45.4 降至 37.9。这表明 RCL 是连接运动幅度模式与音乐节拍结构的关键桥梁，缺失该组件会导致潜在空间失去节奏同步能力。

Transformer 架构（FFT）替代 U-Net 进一步提升了合成质量——FAD 从 11.0 降至 8.1，FID 从 11.6 降至 8.8——说明全局自注意力机制对长序列运动-音乐生成的时序一致性有显著增益。

## 实验与关键发现

### 核心实验设计与评估框架

MoMu-Diffusion在三个互补维度上接受检验：**节拍匹配精度**（BCS、BHS、CSD、HSD、F1）、**生成质量**（FAD/FID、Diversity、Mean KLD）以及**人类主观评价**。实验覆盖运动到音乐（motion-to-music）和音乐到运动（music-to-motion）两个方向，数据集包括AIST++ Dance、Floor Exercise、Figure Skating和BHS Dance，序列长度从短片段延伸至25s和50s的长序列，直接检验模型对长期依赖的建模能力。

评估中存在两个重要的公平性说明：音乐到运动任务的BCS和BHS基于合成运动的节奏点与参考音乐节拍的匹配，而非与真实运动节拍的匹配；运动到音乐评估中使用了改进的音频起始检测算法，以避免长序列中节奏向量稀疏和BHS超过1的问题。

### 运动到音乐生成：节拍与质量双维度碾压

在AIST++ Dance数据集上，MoMu-Diffusion在所有节拍匹配指标上全面超越现有方法（Table 2）。与当时的最先进方法**LORIS**相比，BCS从96.5提升至97.5（+1.0），而BHS的差距更为显著——从90.8跃升至98.6（+7.8），CSD从11.0降至5.2（-5.8），F1从93.2提升至98.1（+4.9）。这表明BiCoR-VAE的节奏对比学习机制使生成的音乐节拍与运动节奏的同步精度获得了质的飞跃。

![[assets/figures/papers/paper_list_l1914_MoMu_Diffusion_On_Learning_Long_Term_Motion_Music_Synchronization_and_Co/figures/004_Table_2.jpg]]
*Table 2: Motion-to-music with beat-matching metrics*

生成质量方面（Figure 3），MoMu-Diffusion在FAD指标上显著优于LORIS，同时保持了更高的Diversity分数。这意味着模型并非通过牺牲多样性来换取质量提升，而是在两者之间取得了更好的平衡。

![[assets/figures/papers/paper_list_l1914_MoMu_Diffusion_On_Learning_Long_Term_Motion_Music_Synchronization_and_Co/figures/005_Figure_3.jpg]]
*Figure 3: Motion-to-music with generation quality metrics: FAD↓ and Diversity↑*

长序列场景是检验模型可扩展性的试金石。在Floor Exercise数据集的25s和50s变体上（Table 3），MoMu-Diffusion的优势进一步扩大：25s条件下BCS达到66.6（LORIS为58.8，+7.8），50s条件下BCS为62.7（LORIS为52.9，+9.8）。在Figure Skating数据集上（Table 4），F1从62.7提升至69.0（+6.3）。这些结果直接验证了核心洞察——基于Transformer的扩散架构能够有效捕捉长序列中的时序依赖，而节奏对比学习确保了即使在长时间跨度下，节拍对齐也不会漂移。

![[assets/figures/papers/paper_list_l1914_MoMu_Diffusion_On_Learning_Long_Term_Motion_Music_Synchronization_and_Co/figures/006_Table_3.jpg]]
*Table 3: Results on the Floor Exercise dataset with beat-matching metrics*

### 音乐到运动生成：质量与同步的协同提升

在音乐到运动任务上，MoMu-Diffusion同样展现出跨模态生成能力的优势。在AIST++ Dance和BHS Dance两个数据集上（Table 5），节拍匹配指标全面领先：BHS Dance数据集上F1达到59.5，相比**DiffGesture**的50.3提升9.2个百分点；AIST++数据集上F1为46.2，相比**D2M**的42.5提升3.7个百分点。

生成质量指标（Table 6）进一步强化了这一结论。在AIST++ Dance上，MoMu-Diffusion的FID降至7.3，而D2M为17.3（-10.0），Mean KLD从3.0降至2.2，Diversity从6.5提升至7.6。在BHS Dance上，FID从7.3降至5.1，Mean KLD从2.8降至1.9。这些数据表明，BiCoR-VAE学到的模态对齐潜在空间不仅服务于节拍同步，也为运动序列的真实感和多样性提供了更强的表示基础。

![[assets/figures/papers/paper_list_l1914_MoMu_Diffusion_On_Learning_Long_Term_Motion_Music_Synchronization_and_Co/figures/011_Table_6.jpg]]
*Table 6: It is observable that MoMu-Diffusion reports better FID, Mean KLD, and Diversity scores on both the AIST++ and BHS Dance datasets. It demonstrates that MoMu-Diffsuion can generate more realistic and high-quality motion sequences while maintaining the capability of diverse generations. We further present a qualitative example of music-to-motion beat-matching in Figure 5. We can find the kinematic beats of synthesized motion are highly associated with the reference musical beats. Additionally, the generated dance exhibits a high degree of diversity, encompassing lateral movements, rotations, squats, and so on*

人类评估（Figure 6）提供了主观维度的佐证：在运动到音乐和音乐到运动两个方向上，MoMu-Diffusion在同步性、质量和整体偏好三个维度上均获得最高评分。

![[assets/figures/papers/paper_list_l1914_MoMu_Diffusion_On_Learning_Long_Term_Motion_Music_Synchronization_and_Co/figures/013_Figure_6.jpg]]
*Figure 6: Results of human evaluation on motion-to-music and music-to-motion generations*

### 消融实验：逐组件验证设计选择

消融实验（Table 7）系统拆解了MoMu-Diffusion的四个关键设计选择，每个结论都有明确的因果指向：

**节奏对比学习（RCL）是节拍对齐的支柱。** 移除RCL后，音乐端F1从98.1骤降至93.1（-5.0），运动端F1从45.4降至37.9（-7.5）。这一降幅在所有消融项中最为剧烈，直接证实了节奏对比损失是BiCoR-VAE实现模态对齐的核心机制，而非VAE结构的附带效果。

**Mel-spectrogram表示优于原始波形。** 使用原始波形替代mel-spectrogram后，音乐FAD从约8.1升至12.8（+4.7），同时F1从98.1降至95.4。这验证了mel-spectrogram在降低序列长度的同时保留了足够的节奏信息，对扩散模型的训练效率和生成质量都有实质性贡献。

**Transformer架构（FFT）显著优于U-Net。** 将Transformer替换为U-Net后，FAD从8.1升至11.0（+2.9），FID从8.8升至11.6（+2.8）。这证实了Transformer的全局自注意力机制对于长序列运动-音乐生成中的长期依赖建模至关重要，U-Net的局部卷积感受野在此任务中构成瓶颈。

**交叉引导步数存在最优区间。** 对交叉引导步数Tc的消融（Table 10）显示，Tc=0.5T时F1达到最优（运动到音乐98.1，音乐到运动45.4），而Tc过小（0.1T）或过大（0.9T）均导致F1下降。这揭示了一个有趣的权衡：过早引入交叉引导会过度约束生成过程损害质量，过晚引入则对齐强度不足；0.5T恰好平衡了无条件生成的多样性与条件引导的对齐精度。

### 失败模式与局限性

论文展示了三类失败案例及修正结果（Figure 7），揭示了方法的边界条件：

![[assets/figures/papers/paper_list_l1914_MoMu_Diffusion_On_Learning_Long_Term_Motion_Music_Synchronization_and_Co/figures/017_Figure_7.jpg]]
*Figure 7: Three failure cases and the corrected results*

1. **骨骼长度异常**：生成的骨骼长度偶尔偏离合理范围，需要阈值后处理修正，但后处理无法完全消除该问题。这表明运动VAE在解码阶段对运动学约束的隐式学习仍不完善。
2. **节奏对齐在极端长序列中退化**：虽然50s序列的结果仍优于基线，但相比25s序列的指标已有明显下降，说明Transformer的全局建模能力在超长序列上仍面临挑战。
3. **预处理误差累积**：模型依赖OpenPose关键点提取和mel-spectrogram转换，这些预处理步骤的误差可能在下游任务中被放大，构成端到端性能的隐性上限。

### 关键图表结论速览

- **Table 2 & Figure 3**：运动到音乐任务上，MoMu-Diffusion在节拍匹配（BHS +7.8）和生成质量（FAD显著优于LORIS）两个维度上同时达到最优，证明对齐与质量可以协同提升而非彼此折衷。
- **Table 3 & Table 4**：在Floor Exercise和Figure Skating的长序列场景中，MoMu-Diffusion的优势随序列长度增加而扩大，验证了Transformer架构对长期依赖的建模能力。
- **Table 7**：消融实验建立了清晰的因果链——RCL驱动节拍对齐，mel-spectrogram提升训练效率，FFT保障长序列质量，三者缺一不可。
- **Table 10**：交叉引导步数Tc=0.5T是最优折衷点，为多模态联合生成的采样策略设计提供了经验性指导。

![[assets/figures/papers/paper_list_l1914_MoMu_Diffusion_On_Learning_Long_Term_Motion_Music_Synchronization_and_Co/figures/016_Table_10.jpg]]
*Table 10: Ablation study of the cross-guidance step*

### 补充图表

![[assets/figures/papers/paper_list_l1914_MoMu_Diffusion_On_Learning_Long_Term_Motion_Music_Synchronization_and_Co/figures/002_Table_1.jpg]]
*Table 1: Comparison with the state-of-the-art audio-visual generation works, including but not limited to motion-music generation*

## 定位与知识库关联

### 与现有方法的区别与改进

MoMu-Diffusion 在运动-音乐生成领域相对于现有基线方法，在三个关键维度上做出了结构性改进：**时序对齐机制**、**扩散模型架构**和**多模态联合生成策略**。

**时序对齐：从隐式到显式的节奏对比学习。** 此前的运动-音乐生成方法（如 LORIS、D2M-GAN、CDCD 等）或缺乏专门的时序对齐模块，或仅依赖简单的时间对比损失。MoMu-Diffusion 提出的 **BiCoR-VAE**（双向对比节奏变分自编码器）首次在潜在空间层面显式建模运动与音乐的节奏同步关系。其核心创新在于引入基于 2D 直接图（directogram）的运动幅度指示器 $Q(r)$，通过双向对比损失（Eq 4）强制同一时刻的运动-音乐潜在片段在表示空间中靠近，而不同时刻或不同节奏的片段相互远离。这一设计的因果逻辑是：节奏是运动与音乐之间最本质的共享结构，显式对齐节奏模式能够从根本上解决长序列生成中的节拍漂移问题。

**扩散架构：从 U-Net 到 Transformer（DiT）。** 传统扩散生成方法（如 DiffGesture、D2M）普遍采用 U-Net 作为骨干网络。MoMu-Diffusion 选择 Transformer 架构（FFT），利用其全局自注意力机制捕捉长序列中的远距离依赖关系。这一选择与长序列运动-音乐生成的需求高度匹配：U-Net 的局部卷积感受野难以建模跨越数秒甚至数十秒的节奏周期和音乐结构，而 Transformer 天然适合处理此类时序全局依赖。

**多模态联合生成：交叉引导采样策略。** 现有方法通常独立训练单模态生成模型，无法实现运动与音乐的联合生成。MoMu-Diffusion 提出的交叉引导采样策略（cross-guidance sampling）通过组合独立训练的专家模型，在不需要额外训练的前提下实现多模态联合生成。其核心机制是在扩散逆向过程的 $T_c$ 步之后，利用估计的干净潜在表示（$\hat{z_a}$）进行无分类器引导的条件生成。这一策略的巧妙之处在于将对齐任务从训练阶段解耦到采样阶段，既保持了各模态生成模型的独立性，又实现了跨模态一致性。

**音频表示优化。** 与使用原始波形的基线方法（如 Foley Music、CMT）相比，MoMu-Diffusion 采用 mel-spectrogram 作为音乐表示，显著缩短了序列长度，降低了扩散模型的计算开销，同时借助 BigvGAN Vocoder 实现高质量波形重建。

### 适用边界与局限

**数据规模与泛化边界。** MoMu-Diffusion 在 AIST++ Dance、Floor Exercise、Figure Skating 和 BHS Dance 四个数据集上进行了验证，这些数据集均属于舞蹈或体育表演领域，具有明确的节奏结构和运动-音乐同步关系。模型在更大规模、更多样化数据集（如日常活动、社交媒体视频）上的泛化性能尚未验证。论文明确指出“由于运动-音乐数据有限和计算资源的限制，模型的缩放定律未在超大规模数据集上测试”，这意味着模型的性能上限和扩展行为仍是一个开放问题。

**预处理依赖与误差累积。** 模型依赖于两个关键预处理步骤：OpenPose 提取 2D 关键点用于运动编码，以及 mel-spectrogram 提取用于音乐编码。这些预处理模块可能引入误差累积，尤其在遮挡、低光照或复杂背景场景下，关键点提取的精度下降会直接影响运动幅度指示器 $Q(r)$ 的计算质量，进而损害节奏对比学习的效果。

**骨骼生成的物理合理性。** 在音乐到运动生成任务中，模型生成的骨骼长度有时出现异常，需要阈值后处理修正。论文指出“后处理无法完全解决该问题”，这表明模型在运动学约束的隐式学习方面仍有不足，生成的姿态可能违反人体骨骼的刚性约束。

**节奏评估指标的局限性。** 音乐到运动任务的击节匹配指标（BCS、BHS）基于合成运动的节奏点与参考音乐节拍的匹配，而非与真实运动节拍的匹配。这意味着高 BHS 分数不一定代表生成的运动与真实运动在节奏上一致，而仅代表与音乐节拍同步。此外，BHS 在某些情况下可能超过 1，需要特殊处理以适应长序列评估。

### 开放问题

**端到端对齐的可能性。** 当前方法依赖预处理提取的节奏信息进行对比学习。能否在不需要显式节奏提取的情况下，实现端到端的运动-音乐对齐？这需要模型在训练过程中自动发现并利用跨模态的节奏共现模式，可能通过更强大的自监督学习框架实现。

**交叉引导步数的理论指导。** 交叉引导采样策略中的超参数 $T_c$ 控制无条件生成与条件生成的切换时机。消融实验表明 $T_c = 0.5T$ 在生成质量与跨模态对齐之间取得最佳折衷，但这一选择目前缺乏理论指导。$T_c$ 的最优值可能与序列长度、节奏复杂度、模态差异程度等因素相关，需要更系统的理论分析。

**规模化训练的潜力。** 论文未在超大规模数据集上验证模型，而扩散模型和 Transformer 架构通常受益于数据规模的扩大。MoMu-Diffusion 在更大规模、更多样化数据集上的性能表现和缩放行为是一个重要的开放问题。

**多模态联合生成的质量-一致性权衡。** 交叉引导采样策略在生成质量与跨模态一致性之间引入了可调节的权衡，但如何在不同应用场景下自动选择最优权衡仍然未解决。未来工作可能需要探索自适应引导强度或基于反馈的采样策略。

## 原文 PDF

![[paperPDFs/NEURIPS_2024/MoMu_Diffusion_On_Learning_Long_Term_Motion_Music_Synchronization_and_Correspondence.pdf]]
