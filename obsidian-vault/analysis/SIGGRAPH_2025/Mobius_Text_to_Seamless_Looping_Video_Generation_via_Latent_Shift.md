---
title: "Mobius: Text to Seamless Looping Video Generation via Latent Shift"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/Mobius_Text_to_Seamless_Looping_Video_Generation_via_Latent_Shift.pdf
project_link: "http://mobius-diffusion.github.io"
code_link: "https://github.com/genmoai/models"
aliases:
- Mobius
tags:
- SIGGRAPH_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 潜在偏移策略：在去噪过程中构建一个首尾相连的潜在循环，并在每一步移动起始点，使每一帧都被平等对待，从而调动视频扩散模型的多帧一致性能力，实现无缝循环。
primary_logic: 利用视频扩散模型天然的多帧去噪与时间一致性，通过潜在循环和逐步偏移，使每一帧在生成过程中均被视为“第一帧”，从而在无训练条件下产出动态且无缝的循环视频；配合帧不变解码和RoPE插值，消除了第一帧压缩带来的伪影，并支持任意长度的视频生成。
claims:
- Mobius在自动评估中取得MSE 25.43、FVD 40.78、CLIP 32.24、Motion Smooth 0.9850、Dynamic Score 0.4722，全面优于对比方法。
- 在用户研究中，Mobius在时序一致性(4.30)、视觉质量(4.15)和视频动态(4.10)三个维度均获得最高评分。
- 在更长视频生成任务上，Mobius取得最优的FVD (29.89)、CLIP Score (32.43) 和运动平滑度 (98.04%)。
- Custom text prompts 上 MSE = 25.43
---

# Mobius: Text to Seamless Looping Video Generation via Latent Shift

> [!tip] 核心洞察
> 利用视频扩散模型天然的多帧去噪与时间一致性，通过潜在循环和逐步偏移，使每一帧在生成过程中均被视为“第一帧”，从而在无训练条件下产出动态且无缝的循环视频；配合帧不变解码和RoPE插值，消除了第一帧压缩带来的伪影，并支持任意长度的视频生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | Mobius：通过潜在偏移实现文本到无缝循环视频生成 |
| 英文题名 | Mobius: Text to Seamless Looping Video Generation via Latent Shift |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](http://arxiv.org/abs/2502.20307v1) · [Project](http://mobius-diffusion.github.io) · [Code](https://github.com/genmoai/models) · [paper](https://arxiv.org/abs/2412.03603) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | Mobius |
| Dataset | Custom text prompts, User Study, Longer Video Generation |

> [!tip] 效果简介
> - Custom text prompts 上，MSE 25.43；FVD 40.78；CLIP 32.24。
> - User Study 上，Temporal Consistency 4.30；Visual Quality 4.15；Video Dynamic 4.10。
> - Longer Video Generation 上，FVD 29.89。

## 概要

现有文本到视频扩散模型在生成无缝循环视频时面临根本瓶颈：模型受固定帧长度和首帧特殊处理的限制，无法直接产出任意长度且首尾连贯的动态循环内容。**Mobius** 提出一种训练自由的方法，通过**潜在偏移**策略重新激活预训练视频扩散模型的多帧一致性能力。其核心在于构建一个首尾相连的潜在循环，并在去噪过程中逐步移动起始点，使每一帧在生成过程中均被平等对待，从而产出无缝循环视频。配合帧不变解码和 RoPE 插值，该方法消除了首帧压缩伪影，并支持任意长度生成。

在自动评估中，Mobius 取得 MSE 25.43、FVD 40.78、CLIP 32.24、运动平滑度 0.9850 和动态得分 0.4722，全面优于对比方法；用户研究在时序一致性（4.30）、视觉质量（4.15）和视频动态（4.10）三个维度均获最高评分。在更长视频生成任务上，Mobius 同样取得最优的 FVD（29.89）、CLIP Score（32.43）和运动平滑度（98.04%）。该方法无需训练，可直接应用于预训练模型，为文本驱动的循环视频生成提供了一种简洁高效的解决方案。

## 核心方法与创新机理

### 瓶颈与核心机制

现有文本到视频扩散模型（如CogVideoX）在生成循环视频时面临两个根本约束：一是模型本身被训练为生成固定帧长的线性视频，无法直接产出首尾无缝衔接的循环内容；二是在多帧去噪过程中，第一帧往往受到特殊处理（如3D VAE的首帧压缩），导致循环闭合处出现明显伪影。Mobius通过一种**训练自由**的潜在偏移策略，在不修改预训练模型参数的前提下，重新调度去噪过程，使模型的多帧一致性能力被充分调用来生成动态丰富且无缝的循环视频。

核心机制可概括为：在潜在空间中构建一个首尾相连的循环列表，并在每个去噪步骤中逐步移动生成起点，从而让每一帧在生成过程中都被平等对待——没有哪一帧被固定为“第一帧”或“最后一帧”。这迫使扩散模型在每次去噪时都维持跨越循环边界的多帧时间一致性，最终产出任意长度且无缝的循环视频。

### 关键创新点

**1. 潜在循环构建与偏移去噪（Latent Shift）**

这是Mobius的核心操作。给定目标视频帧数 $N$ 和模型上下文窗口 $f$（CogVideoX中 $f=13$）：

- 首先将所有 $N$ 帧的初始噪声潜在向量组织成一个循环列表，即第 $N$ 帧与第 $1$ 帧在列表中相邻。
- 在去噪的第 $t$ 步，从循环列表中选取起始帧 $j = (t \times s) \bmod N$（$s$ 为每步偏移步长），将连续 $f$ 帧 $[z_t^j; \dots; z_t^{j+f-1}]$ 送入扩散模型进行去噪，得到 $[z_{t-1}^j; \dots; z_{t-1}^{j+f-1}]$。
- 随着 $t$ 从 $T$ 递减到 $0$，起始帧 $j$ 在循环上逐步滑动，使得每个帧位置都经历多次去噪，且每次去噪时都处于不同的上下文位置。

这一设计的关键在于：扩散模型在每一步都处理一个跨越循环边界的 $f$ 帧窗口，模型的多帧去噪能力被自然用于维持循环首尾的时间一致性。偏移步长 $s$ 控制每次移动的幅度——$s$ 过小会导致运动幅度不足，过大则可能引入不连贯，实验表明 $s=6$ 在视觉质量与运动幅度间取得平衡（见Fig. 6）。

**2. 帧不变解码（Frame-Invariant Decoding）**

CogVideoX使用的3D VAE对第一帧有特殊的压缩处理，这会导致循环视频在首帧处出现闪烁或跳变伪影。Mobius的解决方案是：在解码前，将循环潜在列表的最后3帧复制并插入到第一帧之前作为冗余帧，然后解码整个序列，最后丢弃这些冗余帧。这一操作使得原本的“第一帧”在VAE眼中不再是序列的起始帧，从而消除了首帧特殊压缩带来的伪影（见Fig. 3）。

**3. NTK感知的RoPE插值**

视频扩散模型中的旋转位置编码（RoPE）通过 $Q_m = q_m e^{im\theta}$、$K_n = k_n e^{in\theta}$ 为注意力机制注入绝对位置信息，注意力权重 $A_{m,n} = \text{Re}[q_m, k_n e^{i(m-n)\theta}]$ 仅依赖于相对位置 $m-n$。当生成视频长度超过训练时的最大帧数时，直接使用原始RoPE会导致位置编码外推失败。Mobius采用NTK-aware插值策略，通过缩放旋转基底 $b' = b \cdot k^{d/(d-2)}$ 来扩展位置编码的适用范围，使模型在无需额外训练的情况下支持更长视频的生成（见Fig. 4、Fig. 7）。

![[assets/figures/papers/paper_list_l9_http_arxiv_org_abs_2502_20307v1/figures/009_Figure_7.jpg]]
*Figure 7: Ablation study on RoPE-Interp. Under the implementation of latent shifting, different RoPE strategies can have a significant impact on the content of video generation*

### 方法框架

整体流程分为四个模块：

| 模块 | 功能 | 关键操作 |
|------|------|----------|
| 潜在循环构建 | 建立首尾相连的噪声序列 | 将第 $N$ 帧与第 $1$ 帧潜在向量在列表中相邻 |
| 潜在偏移去噪 | 多步去噪中逐步移动起点 | 每步按 $j = (t \times s) \bmod N$ 选取 $f$ 帧窗口 |
| 帧不变解码 | 消除VAE首帧压缩伪影 | 解码前插入冗余帧，解码后丢弃 |
| RoPE插值 | 支持超长视频生成 | NTK-aware缩放旋转基底 |

这些模块均作用于潜在空间或解码阶段，不涉及模型参数更新，因此Mobius可适配任何基于DiT架构的文本到视频扩散模型。

![[assets/figures/papers/paper_list_l9_http_arxiv_org_abs_2502_20307v1/figures/010_Figure_8.jpg]]
*Figure 8: Limitation. The generated results might not show a very smooth video in the customized domain, e.g., the illustration, restricted by the pretrained text-to-video diffusion model*

![[assets/figures/papers/paper_list_l9_http_arxiv_org_abs_2502_20307v1/figures/002_Figure_3.jpg]]
*Figure 3: Frame-invariance latent decoding reduces the artifacts caused by the 3D VAE decoding*

![[assets/figures/papers/paper_list_l9_http_arxiv_org_abs_2502_20307v1/figures/003_Figure_4.jpg]]
*Figure 4: We illustrate this with the example of the toy latent video diffusion model with a context window equal to 4. The utilized RoPE-Interp. enables longer video context without training by interpolation*

## 实验与关键发现

Mobius 在自动评估、用户研究和长视频生成三个层面均展现出显著优势，其核心效能源于潜在偏移策略对预训练视频扩散模型多帧一致性的充分调用。

### 主结果与对比分析

在自定义文本提示基准上，Mobius 在五项自动指标上全面领先对比方法（Table 1）。具体而言，MSE 低至 25.43，FVD 降至 40.78，CLIP 分数达 32.24，运动平滑度（Motion Smooth）为 0.9850，动态分数（Dynamic Score）为 0.4722。值得注意的是，对于基于插值的基线方法（Svd-Interp. 和 Cog-Interp.），实验设置中人为提供了相同的首帧和尾帧作为关键帧，使得其 MSE 被设为 oracle 值（MSE=0），这一公平性倾斜下 Mobius 仍表现出更大优势，说明潜在偏移生成的循环视频在时序一致性与动态丰富性之间达到了更优平衡。

![[assets/figures/papers/paper_list_l9_http_arxiv_org_abs_2502_20307v1/figures/006_Table_1.jpg]]
*Table 1: Quantitative experimental results for different methods under the numerical evaluation metrics. * for the interpolation-based method, we utilize our generated first frame for the start and end keyframe, thus the MSE between the two frames is the oracle value*

用户研究进一步验证了主观感知质量（Table 2）。Mobius 在时序一致性（4.30）、视觉质量（4.15）和视频动态（4.10）三个维度均获得最高评分，表明潜在循环构建和逐步偏移策略有效消除了首尾帧跳变伪影，同时保持了场景的动态演进。

![[assets/figures/papers/paper_list_l9_http_arxiv_org_abs_2502_20307v1/figures/005_Table_2.jpg]]
*Table 2: User Study Results*

### 长视频生成能力

Mobius 的潜在偏移策略天然支持超出训练上下文窗口的视频长度。在长视频生成任务上（Table 3），Mobius 取得最优 FVD（29.89）、CLIP Score（32.43）和运动平滑度（98.04%），对比方法包括 FreeNoise、Gen-L-Video、FIFO、Video-Infinity 和 DiTCtrl。这一结果表明，通过非循环的潜在位移配合 NTK-aware RoPE 插值，Mobius 能够在无训练条件下将预训练模型的多帧一致性能力泛化至任意长度。

### 关键消融

**潜在偏移步长的影响**（Fig. 6）：每个去噪步骤中潜在偏移的步数直接影响生成内容的视觉质量与运动幅度。当偏移 6 步时，生成结果在视觉质量和运动幅度之间取得平衡；偏移过小会导致运动不足，过大则可能引入时序不稳定。

**RoPE 插值策略**（Fig. 7）：在潜在偏移框架下，不同 RoPE 策略对长视频生成内容有显著影响。固定 RoPE-Interp 表现良好，明显优于无 RoPE 或原始 RoPE 设置。这验证了 NTK-aware 插值在扩展位置编码以适应超长序列时的必要性。

### 失败模式与适用边界

Mobius 的性能受限于底层预训练文本到视频扩散模型的能力边界。在定制领域（如插图风格），生成的视频可能不够平滑（Fig. 8），这是因为预训练模型在该领域的数据分布稀疏，多帧去噪过程中的时序一致性约束不足以补偿域偏移带来的生成质量下降。该问题并非潜在偏移策略本身的设计缺陷，而是训练自由方法对基模型质量的固有依赖。

## 定位与知识库关联

**问题定位与本质差异**

现有文本到视频（T2V）扩散模型在生成循环视频时面临两个根本性瓶颈：一是模型训练时依赖固定帧长和首帧特殊处理，难以直接产出任意长度的无缝循环；二是基于插值的方法（如 **LoopAnimate** (Wang et al., ACM MM Asia 2024)）或基于噪声重排的方法（如 **FreeNoise** (Qiu et al., 2023)）要么需要关键帧输入，要么在长视频生成中累积时序误差。Mobius 的核心差异在于：它不修改模型权重，不依赖关键帧，而是通过**构造潜在循环并逐步偏移去噪起点**，使预训练视频扩散模型的每一帧在生成过程中都被平等对待——这一机制从因果层面消除了首帧特殊性与循环断裂的矛盾。

**知识库挂载点**

Mobius 的方法组件可挂载到以下知识节点：

1. **训练自由的长视频生成**：与 **FreeNoise** (Qiu et al., 2023)、**Gen-L-Video** (Wang et al., 2023a)、**FIFO** (Kim et al., 2024)、**Video-Infinity** (Tan et al., 2024)、**DiTCtrl** (Cai et al., 2024) 等基于噪声调度或窗口注意力的训练自由方法并列。Mobius 区别于这些工作的关键在于：它不依赖局部窗口调度或噪声融合，而是利用潜在偏移将“多帧一致性去噪”能力自然扩展到循环场景，从而在长视频生成任务上取得更优的 FVD（29.89）和运动平滑度（98.04%，Table 3）。

2. **位置编码扩展**：Mobius 采用的 NTK-aware RoPE 插值策略（Sec. 3.4）与 LLM 上下文窗口扩展中的 RoPE 插值方法（如 NTK-aware scaling、YaRN 等）共享技术基因，但其应用场景是视频扩散模型中的时序注意力层，用于支持超出训练帧数的长视频生成。

3. **VAE 解码一致性问题**：Mobius 首次揭示了 3D VAE 对首帧的特殊压缩会引入循环视频解码伪影，并提出帧不变解码（Frame-Invariant Decoding）作为通用解决方案（Sec. 3.3, Fig. 3）。这一问题在现有视频生成文献中尚未被系统讨论，构成一个新的知识贡献点。

**适用边界**

- **模型依赖性**：Mobius 以 **CogVideoX** (Yang et al., 2024) 作为基础模型进行验证，但其设计仅修改潜在输入，理论上可迁移至任何基于 DiT 的文本到视频潜在扩散模型。然而，该方法对 VAE 的首帧压缩特性敏感，若目标模型的 3D VAE 不存在类似偏差，帧不变解码的增益可能减弱。
- **领域局限性**：受限于预训练模型的分布，Mobius 在定制领域（如插图风格）中生成的视频可能不够平滑（Fig. 8）。这意味着该方法的效果上限由基础 T2V 模型的生成能力决定，无法通过训练自由的方式弥补基础模型的领域缺陷。
- **循环质量依赖于偏移步长**：消融实验（Fig. 6）表明，每步去噪中的潜在偏移步长 $s$ 直接影响生成内容的视觉质量与运动幅度之间的平衡——步长过小导致运动不足，步长过大则引入时序不一致。该超参数可能需要根据具体场景手动调整。

**后续启发**

1. **对其他时序生成任务的迁移**：潜在偏移的核心思想——通过循环构造和起点偏移来消除边界特殊性——可推广到其他需要无缝时序生成的场景，如音频循环生成、运动重定向等。

2. **与可控生成方法的结合**：Mobius 当前仅支持文本引导，其循环生成框架与 ControlNet、IP-Adapter 等可控生成方法的结合是一个自然延伸方向，有望实现基于图像或结构化条件的无缝循环视频生成。

3. **VAE 设计的重新审视**：帧不变解码的提出暗示了当前 3D VAE 设计中对时序边界帧的不公平处理，这可能推动社区重新审视视频 VAE 的压缩策略，探索对循环生成更友好的潜在空间设计。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/Mobius_Text_to_Seamless_Looping_Video_Generation_via_Latent_Shift.pdf]]