---
title: "Teller: Real-Time Streaming Audio-Driven Portrait Animation with Autoregressive Motion Generation"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Teller_Real_Time_Streaming_Audio_Driven_Portrait_Animation_with_Autoregressive_Motion_Generation.pdf
code_link: null
project_link: https://teller-avatar.github.io
aliases:
- Teller
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "采用自回归Transformer与残差向量量化（RVQ）将运动离散化为token，结合Whisper音频编码实现流式映射；引入高效时序模块（ETM）通过单步时序自注意力细化细微运动，保证物理一致性。"
primary_logic: "将面部运动分解为离散token并使用自回归下一个token预测，可在极低延迟下产生多样逼真的动画；辅以单步时序细化，显著提升身体和配饰运动的真实感。"
claims:
- "Teller推理速度0.92s生成1秒视频，远超Hallo的20.93s，实时性达25 FPS。"
- "在HDTF和RAVDESS上，Teller的FVD和唇音同步指标均优于当前最优方法。"
- "人类评估表明Teller在唇音同步、身体运动真实感和时序连贯性上显著领先。"
- "消融实验证实ETM模块和RVQ压缩对运动细节与实时性至关重要。"
---

# Teller: Real-Time Streaming Audio-Driven Portrait Animation with Autoregressive Motion Generation

> [!tip] 核心洞察
> 将面部运动分解为离散token并使用自回归下一个token预测，可在极低延迟下产生多样逼真的动画；辅以单步时序细化，显著提升身体和配饰运动的真实感。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Teller：基于自回归运动生成的实时流式音频驱动人像动画 |
| 英文题名 | Teller: Real-Time Streaming Audio-Driven Portrait Animation with Autoregressive Motion Generation |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2503.18429) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Teller |
| Dataset | HDTF |

> [!tip] 效果简介
> - HDTF 上，FVD 为 173.463，对比 174.191 (Hallo)，变化 -0.728。
> - HDTF 上，Sync-C 为 7.696，对比 7.497 (Hallo)，变化 +0.199。
> - HDTF 上，Sync-D 为 7.536，对比 7.741 (Hallo)，变化 -0.205。

## 概要

音频驱动的人像动画旨在根据语音输入生成逼真的说话面部视频，在虚拟助手、数字人等场景有广泛应用。该领域的核心瓶颈在于：现有主流方法（如扩散模型或GAN）生成一秒钟视频往往需要数十秒，无法满足实时交互需求；同时，这些方法普遍忽略项链、耳环、颈部肌肉等身体部位和配饰的自然运动，导致动画僵硬或夸张失真。

针对上述问题，**Teller** 提出首个基于自回归运动生成的实时流式音频驱动人像动画框架。其核心洞察是：将面部运动分解为离散token，利用自回归Transformer进行下一token预测，可在极低延迟下产生多样且逼真的动画；辅以单步时序细化，能显著提升身体和配饰运动的物理一致性。

在方法定位上，Teller 采用 **自回归Transformer + 残差向量量化（RVQ）** 替代传统的扩散或GAN生成范式，将运动离散化为token序列，结合 **Whisper音频编码器** 实现流式映射；同时引入 **高效时序模块（ETM）** 通过单步时序自注意力修正细微运动。这一设计使其在推理速度上实现质的飞跃：生成1秒视频仅需0.92秒（25 FPS实时流式），而扩散模型 **Hallo**（Xu et al., arXiv 2024）需要20.93秒。

在HDTF和RAVDESS基准上，Teller的FVD和唇音同步指标（Sync-C）均优于当前最优方法；人类评估进一步表明其在唇音同步、身体运动真实感和时序连贯性上显著领先。消融实验证实ETM模块和RVQ压缩策略对运动细节与实时性至关重要。

**局限与展望**：Teller依赖LivePortrait作为运动表示基础，可能继承其对极端姿态的处理缺陷；训练数据经过严格过滤，对大幅度运动的泛化能力未经验证；目前仅支持单人物正面动画，长视频生成的自回归误差累积问题也尚待解决。未来可探索将该框架扩展至全身动画或集成到多模态大语言模型中。

音频驱动的肖像动画旨在根据输入语音生成逼真且时序同步的说话人视频，在数字人、虚拟主播、在线教育等领域具有广泛应用。近年来，该领域涌现出多种方法，包括基于GAN的**SadTalker**（Zhang et al., CVPR 2023）和**AniPortrait**（Wei et al., arXiv 2024），以及基于扩散模型的**Hallo**（Xu et al., arXiv 2024）和**EchoMimic**（Chen et al., arXiv 2024）。这些方法在图像质量上取得了显著进展，但仍面临两个核心瓶颈。

**实时性瓶颈**。扩散模型和GAN方法通常需要多步去噪或复杂的生成流程，导致推理速度难以满足实时交互需求。以Hallo为例，生成1秒视频需要20.93秒，远无法达到流式传输的实时性要求。在直播、视频会议等场景中，低延迟的流式生成能力是实际部署的前提条件。

**身体与配饰运动缺失**。现有方法普遍聚焦于面部区域和唇音同步，却忽略了项链、耳环、颈部肌肉等身体部位和配饰的自然运动。这种忽视导致生成的动画出现两类典型问题：一是身体部位僵硬静止，与活跃的面部表情形成割裂感；二是配饰运动与头部运动缺乏物理一致性，呈现不自然的漂浮或错位。这些问题严重损害了动画的整体真实感。

上述瓶颈的根源在于生成范式的选择。扩散模型虽然生成质量高，但其迭代去噪过程天然与实时性相悖；而GAN方法缺乏对时序依赖关系的显式建模，难以捕捉细微的物理运动规律。因此，探索一种既能保证极低推理延迟、又能精确建模全身运动细节的新范式，成为推动该领域发展的关键动机。Teller正是在这一背景下，首次将自回归Transformer引入肖像动画，通过离散运动token预测和单步时序细化，同时解决实时性和运动真实感两大难题。

## 核心方法与创新机理

Teller 的核心创新在于将音频驱动人像动画从传统的扩散/生成对抗范式转向**自回归离散运动生成**，并辅以**单步时序细化**解决身体配饰运动失真问题。具体而言，其关键创新点体现在以下四个“changed slots”：

1.  **运动生成主干：从扩散/生成对抗到自回归Transformer + 残差向量量化**
    现有方法（如 **Hallo** (Xu et al., arXiv 2024)、**SadTalker** (Zhang et al., CVPR 2023)）普遍采用扩散模型或生成对抗网络生成连续运动参数，导致推理延迟极高（如 Hallo 生成1秒视频需20.93秒），无法满足实时交互需求。Teller 将面部运动分解为离散 token，采用**自回归Transformer**进行下一个 token 预测，将运动生成转化为序列建模问题。其关键瓶颈突破在于：通过**残差向量量化**将每4帧的25×3运动隐变量压缩为32个离散 token，大幅降低序列长度，使得自回归生成在保持运动质量的同时实现0.92秒生成1秒视频（25 FPS）的实时性能。这一“连续→离散”的表示转换是实时性的核心因果杠杆。

2.  **时序细化模块：从无专门后处理到高效时序模块 + 区域掩码损失**
    现有方法常忽略项链、耳环、颈部肌肉等身体部位和配饰的自然运动，导致动画僵硬或夸张。Teller 引入**高效时序模块**，通过单步时序自注意力对第一阶段生成的运动进行细化。其创新在于：仅对后5帧进行时序建模（前5帧作为条件），并通过 Mediapipe 关键点定义的**区域掩码损失**，强制模型关注身体配饰区域的物理一致性，而非全图重建。消融实验证实，ETM 能够修正第一阶段缺失的耳环摆动、颈部肌肉等细微运动。

3.  **音频编码器：从TTS编码器到ASR编码器**
    现有方法多使用针对语音合成优化的编码器（如 funCodec），Teller 改用**Whisper 编码器**（自动语音识别模型）提取音频条件。消融实验表明，这一选择显著提升了唇音同步指标：Sync-C 从4.286跃升至7.696，Sync-D 从10.373降至7.536。其因果机制在于：ASR模型天然擅长捕捉音素级别的发音特征，比TTS模型更适合驱动唇形生成。

4.  **推理速度：从20秒级到亚秒级实时流式**
    这是前述创新的直接结果。Teller 将1秒视频的推理时间从 Hallo 的20.93秒压缩至0.92秒，实现了**25 FPS的实时流式生成**。这一数量级差异源于自回归架构避免了扩散模型的迭代去噪过程，以及双头token并行预测设计进一步减少了自回归步数。

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2503_18429/figures/001_Figure_1.jpg]]
*Figure 1: Teller framework is the first autoregressive framework for real-time, audio-driven portrait animation, achieving up to 25 FPS while preserving realistic body part and accessory movements. Demo can be found at https://teller-avatar.github.io/*

Teller 提出了一种两阶段级联架构，首次将自回归生成范式引入实时音频驱动人像动画任务。其核心设计动机源于一个关键瓶颈：现有扩散或GAN方案（如 **Hallo** (Xu et al., arXiv 2024)、**SadTalker** (Zhang et al., CVPR 2023)）生成1秒视频需20秒以上，且普遍忽略项链、耳环、颈部肌肉等身体部位和配饰的自然运动，导致动画僵硬或夸张。Teller 通过将面部运动离散化为token并采用自回归下一个token预测，在极低延迟下产生多样逼真的动画；辅以单步时序细化模块，显著提升身体和配饰运动的真实感。

整体pipeline由两个核心模块串联构成：

1. **面部运动隐变量生成（Facial Motion Latent Generation, FMLG）**：负责将流式音频输入映射为驱动人像的离散运动token序列。
2. **高效时序模块（Efficient Temporal Module, ETM）**：对FMLG生成的初步动画进行时序细化，修正身体部位和配饰的运动缺陷。

**数据流与模块关系**

```
音频流 → Whisper编码器 → AR Transformer + RVQ解码 → 运动隐变量 → LivePortrait驱动 → 初步视频帧 → VAE编码 → ETM时序细化 → VAE解码 → 最终视频
```

具体而言，FMLG阶段首先使用 **Whisper编码器** 将流式音频块编码为条件嵌入 $c$。运动生成被建模为自回归下一个token预测任务 $P(t_i \mid c, t_{<i})$：一个自回归Transformer基于音频条件和先前token，逐步预测下一对运动token。这些token由 **残差向量量化器（RVQ）** 编码得到——RVQ将每4帧的25×3运动隐变量压缩为32个离散token，在重构损失与推理速度之间取得最优平衡（见Figure 11）。预测出的token经 **运动解码器** 恢复为运动隐变量（关键点变形、头部姿态、表情变形），送入LivePortrait生成初步视频帧。

ETM阶段则对初步视频帧进行时序一致性修复。首先由 **VAE编码器** 将视频帧映射到隐空间，随后ETM沿时序维度执行自注意力操作，捕捉帧间依赖关系，并通过残差连接将时序特征融合回空间特征。ETM的训练采用区域特定掩码损失 $\mathcal{L}_{\mathrm{ETM}}$，仅对Mediapipe关键点定义的边界框内区域（身体部位和配饰）计算重构损失，迫使模型专注修正耳环摆动、颈部肌肉运动等FMLG阶段缺失的细微运动。最终由 **VAE解码器** 将细化后的隐变量恢复为像素空间视频。

**关键设计选择**

- **双头预测**：AR Transformer的每个位置同时处理并预测一对token（Figure 3），相比逐token预测速度翻倍。训练时引入平衡正则项 $\lVert \mathcal{L}_{\mathrm{head0}} - \mathcal{L}_{\mathrm{head1}} \rVert_2^2$ 防止双头训练失衡。
- **Whisper编码器**：消融实验证实，相比TTS导向的funCodec编码器，ASR导向的Whisper编码器在唇音同步指标上显著更优（Sync-C 7.696 vs. 4.286），原因在于ASR特征更直接地捕获了音素-口型对应关系。
- **单步时序细化**：ETM仅需单步自注意力即可完成时序修正，避免多步扩散或迭代带来的计算开销，是实现25 FPS实时流式推理的关键保障。

**推理流程**

推理时，Teller以流式方式处理音频：Whisper编码器对音频块实时编码，AR Transformer根据已生成的token和当前音频条件预测下一对运动token，RVQ解码后驱动LivePortrait生成帧，ETM实时细化后输出。整个流程生成1秒视频仅需0.92秒（Hallo为20.93秒），达到25 FPS实时性能。

Teller 的实时流式音频驱动人像动画框架由两个核心模块构成：**面部运动隐变量生成（FMLG）** 和 **高效时序模块（ETM）**。FMLG 负责将音频信号映射为离散的面部运动 token，实现极低延迟的流式生成；ETM 则对生成的运动进行单步时序细化，修正项链、耳环、颈部肌肉等身体部位和配饰的运动，保证物理一致性。

### 3.1 统一运动隐变量

Teller 将面部运动表示为一个统一的隐变量 $m$，其定义为 21 个关键点变形、3 个头部姿态旋转向量和 1 个表情变形向量的拼接：

$$m = [\delta_1, \delta_2, \ldots, \delta_{21}, r_1, r_2, r_3, t]$$

其中 $\delta_i$ 为第 $i$ 个关键点的二维变形，$r_1, r_2, r_3$ 为头部姿态的旋转向量，$t$ 为表情变形。该隐变量的维度为 $25 \times 3$。一段 $T$ 帧的视频对应的运动序列为 $M = [m_1, m_2, \ldots, m_T]$。

### 3.2 残差向量量化（RVQ）与运动 token 化

FMLG 的核心是将连续的运动隐变量压缩为离散 token，以便自回归 Transformer 进行下一个 token 预测。Teller 采用残差向量量化（Residual Vector Quantization, RVQ）实现这一目标。

经过帧间冗余分析，Teller 选择每 4 帧压缩为 32 个离散 token，即在压缩率与重建精度之间取得最佳平衡（见 Figure 11）。RVQ 的训练损失函数为：

$$\mathcal{L}_{vq} = \sum_{t=1}^{T} \left[ || m - \mathrm{FFN}_{dec}(z_t + \mathrm{sg}[\hat{z}_t - z_t]) ||_2^2 + || z_t - \mathrm{sg}[\hat{z}_t] ||_2^2 \right]$$

该损失包含两项：第一项为重构损失，通过前馈解码器 $\mathrm{FFN}_{dec}$ 将量化后的隐变量重建为原始运动 $m$；第二项为承诺损失（commitment loss），约束编码器输出 $z_t$ 靠近量化向量 $\hat{z}_t$。$\mathrm{sg}[\cdot]$ 表示停止梯度算子。

经过 RVQ 压缩后，运动序列被转换为离散 token 序列：

$$T_m = [t_1, t_2, \dots, t_{T/4}]$$

其中每个 $t_i$ 对应 4 帧的 32 个运动 token。

### 3.3 自回归运动生成

运动生成被建模为基于音频条件的下一个 token 预测任务：

$$P(t_i \mid c, t_{<i})$$

其中 $c$ 为 Whisper 编码器提取的音频嵌入，$t_{<i}$ 为已生成的前序 token。Teller 的自回归 Transformer 采用双头设计（Figure 3）：每个位置同时处理一对 token，两个预测头各负责一个 token，从而将预测步数减半，加速推理。

双头预测的总损失为：

$$\mathcal{L}_{ar} = \sum_{j=1}^{I/2} \left[ \mathcal{L}_{\mathrm{head0}_j} + \mathcal{L}_{\mathrm{head1}_j} + \lVert \mathcal{L}_{\mathrm{head0}_j} - \mathcal{L}_{\mathrm{head1}_j} \rVert_2^2 \right]$$

其中第三项为平衡正则项，约束两个预测头的损失保持一致，防止某一头主导训练。

### 3.4 高效时序模块（ETM）

ETM 作为第二阶段，对 FMLG 生成的粗粒度运动进行时序细化。其核心操作是沿时间维度执行自注意力（self-attention），捕捉帧间的运动依赖关系，并通过残差连接将时序特征融合回空间特征。

ETM 的训练采用带区域掩码的重构损失，仅对 Mediapipe 关键点定义的边界框内区域计算损失，从而专注于身体部位和配饰的运动修正：

$$\mathcal{L}_{\mathrm{ETM}} = \sum_{i=6}^{10} \left\| x_{\mathrm{gt}_i} \odot \mathrm{mask}_i - f(x_i | x_{\mathrm{gt}_{<6}}) \odot \mathrm{mask}_i \right\|_2^2$$

其中 $x_{\mathrm{gt}_i}$ 为第 $i$ 帧的真值，$f(x_i | x_{\mathrm{gt}_{<6}})$ 为基于前 6 帧真值对第 $i$ 帧的预测。二值掩码 $\mathrm{mask}(i,j)$ 定义为：

$$\mathrm{mask}(i,j) = \left\{ \begin{array}{ll} 1, & \mathrm{if } (i,j) \text{ is within BB}(x) \\ 0, & \mathrm{otherwise} \end{array} \right.$$

其中 $\mathrm{BB}(x)$ 为由关键点确定的边界框区域。该设计使得 ETM 能够精准修正 Stage 1 中缺失的耳环摆动、颈部肌肉运动等细微动态（Figure 10 消融实验证实），而不会干扰已生成良好的面部区域。

## 实验与关键发现

### 核心性能对比

Teller在HDTF和RAVDESS两个主流基准上全面超越现有方法，尤其在推理速度上形成断崖式领先。**Table 1**汇总了HDTF数据集上的定量结果：Teller的FVD降至173.463，优于**Hallo**（Xu et al., arXiv 2024）的174.191；唇音同步指标Sync-C达到7.696，显著高于Hallo的7.497。更具决定性的是推理效率——生成1秒25 FPS视频，Teller仅需0.92秒，而Hallo需要20.93秒，速度提升超过22倍。这一差距源于自回归Transformer的单步前向推理替代了扩散模型的迭代去噪过程，使得实时流式生成（25 FPS）成为可能。

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2503_18429/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison with existing portrait image animation approaches on the HDTF dataset. T ime stands for the averaging time cost of generating one second of 25 fps video. Table 2. Quantitative comparison with existing portrait image animation approaches on the RAVDESS dataset*

在RAVDESS情感数据集上，Teller同样取得最优FVD（429.288）和Sync-C（4.496），但需注意原文未给出对比方法在该数据集上的精确数值，该结论的置信度略低于HDTF结果（置信度0.85）。

### 人类评估

主观评价（**Figure 9**）从三个维度验证了客观指标的提升：唇音同步准确性、身体运动真实感、时序连贯性。Teller在所有维度上均获最高评分，证实了ETM模块对项链、耳环、颈部肌肉等细微运动的修正能力被人类感知为显著的质感提升。但评估参与人数未公开，样本量可能有限。

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2503_18429/figures/007_Figure_9.jpg]]
*Figure 9: Human evaluation results among our proposed Teller and other SoTA methods*

### 消融实验

消融研究揭示了三个关键设计选择的有效性：

**音频编码器选择（Table 3）**：将Whisper（ASR模型）替换为funCodec（TTS模型）后，唇音同步指标急剧恶化——Sync-C从7.696降至4.286，Sync-D从7.536升至10.373。这表明ASR模型提取的语音特征比TTS特征更适配唇形映射任务，可能因为ASR编码器对音素边界的表示更精确。

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2503_18429/figures/010_Table_3.jpg]]
*Table 3: Comparison of synchronization for audio conditions using funcodec and Whisper in ASR and TTS tasks on HDTF. Table 4. Comparison of performance between Single-Head and Multi-Head on the HDTF dataset*

**架构设计（Table 4）**：单头（Single-Head）架构在同步指标上略优于多头（Multi-Head），Sync-C为7.790 vs. 7.696。这一反直觉结果说明，在双token并行预测的设计下，共享参数可能比独立头更有利于捕获token间的耦合关系。

**两阶段贡献（Figure 10）**：仅使用Stage 1（FMLG）生成的动画在面部表情上已基本准确，但耳环摆动、颈部肌肉运动等细节缺失或僵硬。Stage 2（ETM）通过单步时序自注意力和区域掩码损失，有效修正了这些配饰和身体部位的物理一致性。

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2503_18429/figures/012_Figure_10.jpg]]
*Figure 10: Visualization of the generation images with different stages and the differences between stages. Figure 11. Tradeoff between performance (loss) and different compression(tokens/frame ) ratios*

**压缩率权衡（Figure 11）**：RVQ压缩实验中，选择4帧压缩为32 token（即8 token/帧）在重构损失与实时性之间取得最佳平衡。更高压缩率导致运动细节丢失，更低压缩率则增加自回归序列长度，损害推理速度。

### 失败模式与局限性

尽管整体性能优异，Teller存在以下已知局限：

1. **运动范围受限**：训练数据经过严格过滤（Mediapipe检测面部移动超过50%即剔除），导致模型对大幅度头部转动或极端表情的泛化能力未经验证。
2. **自回归累积误差**：长视频生成中，自回归预测的误差可能逐帧累积，论文未对此进行专项评估。
3. **2D表示瓶颈**：依赖LivePortrait的2D关键点表示，无法处理大角度头部转动时的容貌变形和遮挡。
4. **数据偏差**：Sync-C/Sync-D过滤可能引入选择偏差，使模型倾向于生成“安全”但缺乏表现力的运动。
5. **语言泛化未知**：训练数据以英语为主，中文等多语言音频效果未测试。

### 公平性说明

推理时间在4块H800 GPU上测得，其他硬件条件下的实时性需重新验证。对比方法使用论文原始权重推理，但可能未完全复现其最佳性能。所有方法共享相同的Mediapipe和Sync-C/Sync-D过滤流程，但过滤本身可能对不同方法产生不等价影响。

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2503_18429/figures/008_Figure_6.jpg]]
*Figure 6: Top-k selection (k=15) in FMLG produces diverse facial expressions and actions with accurate lip sync on the HDTF*

## 定位与知识库关联

### 与现有方法的关系

Teller 的核心贡献在于将音频驱动人像动画从扩散/生成对抗网络范式迁移到自回归离散token预测范式，从而在实时性与运动真实感之间建立了新的平衡点。理解其定位需要从运动生成主干、时序细化机制和音频编码器三个维度与现有工作对比。

**扩散模型路线的性能瓶颈。** **Hallo** (Xu et al., arXiv 2024) 是扩散模型路线的代表性方法，在 HDTF 上取得了 FVD 174.191、Sync-C 7.497 的强结果，但其推理时间高达 20.93 秒生成1秒视频（Table 1），本质上无法满足实时流式需求。Teller 以自回归 Transformer 替代扩散去噪过程，将推理时间压缩至 0.92 秒，达到 25 FPS 的实时性能，同时将 FVD 降至 173.463、Sync-C 提升至 7.696。这种加速并非以牺牲质量为代价——自回归框架通过残差向量量化（RVQ）将运动隐变量离散化为 token，使得下一个 token 预测任务天然适配流式生成，而扩散模型的多步去噪在实时场景下存在根本性延迟瓶颈。

**GAN/运动表示路线的细节缺失。** **SadTalker** (Zhang et al., CVPR 2023)、**EchoMimic** (Chen et al., arXiv 2024) 和 **AniPortrait** (Wei et al., arXiv 2024) 等基于 GAN 或运动表示的方法虽然速度较快，但普遍忽略了项链、耳环、颈部肌肉等身体部位和配饰的自然运动，导致动画僵硬或夸张（Figure 7）。Teller 通过引入高效时序模块（ETM）作为第二阶段细化，对这一短板进行了针对性补强。ETM 在 VAE 潜空间沿时序维度执行单步自注意力，并结合区域特定掩码损失，专门优化 Mediapipe 关键点定义的边界框内区域（Equation 10-11），从而修正第一阶段 FMLG 自回归生成中缺失的细微运动（Figure 10 消融可视化证实了这一点）。

**音频编码器的选择差异。** 现有方法多使用 funCodec 等 TTS 导向的编码器，而 Teller 选择 Whisper 编码器（ASR 模型）作为音频条件。消融实验（Table 3）表明这一选择对唇音同步至关重要：Whisper 条件下 Sync-C 为 7.696、Sync-D 为 7.536，而 funCodec 条件下 Sync-C 骤降至 4.286、Sync-D 恶化至 10.373。这暗示 ASR 模型提取的语音特征比 TTS 特征更精准地捕捉了与唇形相关的音素信息。

**架构设计的消融洞察。** 单头与多头的对比（Table 4）显示，单头架构在同步指标上略优（Sync-C 7.790 vs. 7.696），表明在双 token 并行预测的设计下，共享参数的单头结构可能比独立双头更有利于学习 token 对之间的协同关系。此外，RVQ 压缩率的选择（Figure 11）揭示了4帧压缩为32 token 是重构损失与实时性之间的最优平衡点——更激进的压缩会损害运动细节，更保守的压缩则增加自回归步数。

### 适用边界

**正面近景人像的约束。** Teller 的运动表示建立在 LivePortrait 的隐式关键点模型之上，将21个表情变形关键点、3个头部姿态旋转向量和1个表情变形向量拼接为 25×3 的隐变量（Equation 1）。这一表示天然适用于正面或近正面单人物场景，但大角度头部转动时的容貌变形、多人场景和复杂背景均未在论文中进行验证。

**数据过滤引入的选择偏差。** 训练和验证数据经过双重过滤：Mediapipe 人脸检测剔除面部移动超过50%的样本，Sync-C/Sync-D 进一步排除唇音得分低的样本。这意味着模型在训练阶段未充分暴露于大幅度运动或低质量音频场景，其对极端姿态、遮挡或嘈杂音频的泛化能力存在不确定性。

**硬件依赖与部署限制。** 推理时间在4块 H800 GPU 上测得，其他硬件条件下的实时性能未经验证。论文未讨论移动端或边缘设备的部署可行性及优化策略，这在流式应用的实际落地中是一个关键缺口。

### 局限与开放问题

**自回归框架的固有风险。** 自回归模型存在错误累积问题——早期 token 的预测误差可能沿序列传播并放大。论文未对长视频生成（如数分钟持续动画）的一致性进行专项评估，这一风险在流式场景中尤为关键。

**运动表示的上限。** 依赖 LivePortrait 意味着 Teller 可能继承其对极端姿态或遮挡的处理缺陷。2D 动画框架无法处理大角度头部转动时的容貌变形，这限制了其在需要自然转头交互场景（如虚拟会议）中的应用。

**多语言与跨域泛化。** 训练数据以英语语音为主（AV Speech 662小时），中文等多语言音频的效果未知。此外，跨域人脸动画（不同种族、年龄、风格）是否可以直接泛化而不需要 fine-tuning，论文未给出答案。

**开放研究问题。** 论文结论部分指出 Teller 的自回归 Transformer 架构与现有统一多模态语言模型兼容，这暗示了未来将音频驱动动画集成到端到端多模态大模型中的可能性。其他值得探索的方向包括：将自回归框架扩展至全身或手势动画、结合文本情感描述实现多模态可控动画、以及在长视频生成中引入全局一致性约束以缓解误差累积。

## 原文 PDF

![[paperPDFs/CVPR_2025/Teller_Real_Time_Streaming_Audio_Driven_Portrait_Animation_with_Autoregressive_Motion_Generation.pdf]]
