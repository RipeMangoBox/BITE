---
title: "AC-Foley: Reference-Audio-Guided Video-to-Audio Synthesis with Acoustic Transfer"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AC_Foley_Reference_Audio_Guided_Video_to_Audio_Synthesis_with_Acoustic_Transfer.pdf
aliases:
- AF
- AC-Foley
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "引入参考音频作为直接控制信号，通过预训练VAE编码器保留其完整的频谱/音色特征，而非仅依赖语义级CLAP编码；并采用两阶段训练迫使模型学习将参考声学特性适配到视频时序上下文，避免简单的\"复制粘贴\"行为。"
primary_logic: "以音频自身作为控制条件绕过了文本描述的语义歧义，同时通过重叠/非重叠两阶段训练利用视频内部的声学自相似性，使模型既能提取精细的声学线索，又能在新的时序场景中泛化，从而生成既忠于参考音色又与画面严格同步的声音。"
claims:
- "两阶段训练（Stage I重叠条件，Stage II非重叠条件）是解决参考音频\"复制粘贴\"与泛化矛盾的关键，非重叠条件使FD_PaSST从80.07降至56.00（↓30.1%）。"
- "直接使用VAE编码的音频潜在特征而非CLAP语义特征，可将MCD从14.63大幅降至11.37（↓22.3%），证明保留完整声学签名对精细控制至关重要。"
- "在人工评估中，AC‑Foley（带音频条件）相比纯视觉‑文本的MMAudio‑L‑V2在声学保真度上赢率达到83.5%，表明参考音频控制能生成更贴近目标音色的声音。"
- "移除同步条件（synchformer特征）导致DeSync从0.465退化至1.240，突显多模态条件中时序对齐信号的必要性。"
---

# AC-Foley: Reference-Audio-Guided Video-to-Audio Synthesis with Acoustic Transfer

> [!tip] 核心洞察
> 以音频自身作为控制条件绕过了文本描述的语义歧义，同时通过重叠/非重叠两阶段训练利用视频内部的声学自相似性，使模型既能提取精细的声学线索，又能在新的时序场景中泛化，从而生成既忠于参考音色又与画面严格同步的声音。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AC-Foley：基于参考音频引导的视频到音频合成与声学迁移 |
| 英文题名 | AC-Foley: Reference-Audio-Guided Video-to-Audio Synthesis with Acoustic Transfer |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=URPXhnWdBF) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | AC-Foley |
| Dataset | VGGSound test set (curated, 8, 676 videos), VGGSound test set, Greatest Hits (timbre transfer) |

> [!tip] 效果简介
> - VGGSound test set (curated, 8,676 videos) 上，FD_PaSST (↓) 为 56.00，对比 64.90 (MMAudio+CLAP)，变化 -8.90 (-13.7%)。
> - VGGSound test set 上，MCD (↓) 为 11.37，对比 14.63 (MMAudio+CLAP)，变化 -3.26 (-22.3%)。
> - VGGSound test set 上，DeSync (↓) 为 0.465，对比 0.558 (MMAudio+CLAP)，变化 -0.093 (-16.7%)。

## 概述

现有视频到音频生成方法大多依赖文本提示控制音效语义，但文本无法精确描述冲击瞬态、共振衰减等微声学特征，加之训练数据的粗粒度标注（如将所有狗叫声统一标为"barking"），导致生成结果难以体现创作者要求的细粒度音色变体。针对这一瓶颈，本文提出 **AC‑Foley**，一种以参考音频为直接控制信号的条件视频到音频合成框架，通过保留完整频谱/音色签名和两阶段课程训练，实现声学迁移：既忠于参考音频的音色、音质，又与画面事件严格同步。

方法的核心思路在于，用预训练音频 VAE 编码器代替仅提取语义信息的 CLAP 编码器，将参考音频压缩为紧凑的声学潜在向量，完整保留其频谱和音色特征；同时将视频、文本和音频条件整合为统一的多模态条件向量，通过自适应层归一化（adaLN）注入条件流匹配 Transformer 网络，生成目标音频的梅尔频谱，再由声码器恢复波形。训练策略上，第一阶段利用与目标音频重叠的参考片段（**重叠条件**）引导模型提取精细声学线索；第二阶段切换到与目标音频不重叠的参考片段（**非重叠条件**），迫使网络利用视频内部的声学自相似性泛化，避免简单的"复制‑粘贴"行为。

在 VGGSound 测试集上，AC‑Foley 与同架构的音频条件基线 MMAudio+CLAP 相比，分布匹配指标 FD_PaSST 从 64.90 降至 **56.00**（↓13.7%），声学失真 MCD 从 14.63 降至 **11.37**（↓22.3%）；用户研究显示，其对纯视觉‑文本方法 MMAudio‑L‑V2 的声学保真度赢率达 **83.5%**。消融实验进一步证实，两阶段训练是实现非复制式声学迁移的关键（FD_PaSST 从仅重叠条件的 80.07 骤降 30.1%），而同步条件与音频条件分别负责时序对齐和音质控制，二者不可偏废。该方法还支持跨音源音色迁移和零样本生成，展现了灵活的音效创作能力。

## 背景与动机

自动生成与无声视频时空同步、听觉逼真的音效（Foley）是影视制作、游戏开发和虚拟现实等领域的关键需求。近期的视频到音频合成方法主要依赖文本提示作为语义控制信号，将视频帧与自然语言描述联合送入生成模型。然而，文本作为控制接口存在根本性的粒度限制：它几乎无法刻画声音的微声学特征，例如冲击瞬态的尖锐程度、材质共振的衰减模式、或音色的细微差别。训练数据的标注粗糙化进一步加剧了这一问题——在常用数据集中，所有犬吠声通常被统一归类为"barking"，这使得模型没有能力区分吉娃娃尖细的叫声与大型犬低沉的咆哮，更无法根据创作者的意图生成指定变体。因此，现有工作本质上难以实现对输出声音细粒度、可定制的声学控制，产生了"语义正确但听觉偏离目标"的严重缺口。

针对此瓶颈，AC‑Foley 提出的核心洞察是以音频自身作为控制条件，绕开文本描述的歧义边界。具体来说，方法引入用户提供的参考音频，并要求模型既保留参考音色的完整声学签名，又将该签名适配到视频的时序场景中，而非简单地"复制粘贴"参考片段。这一思路面临的关键矛盾在于：若直接使用参考音频与目标音频高度重叠的条件片段，模型容易退化到直接拷贝；若条件与目标在时间上完全不重叠，则模型难以从中剥离合用的声学线索。AC‑Foley 通过两阶段课程训练解决了这一矛盾：第一阶段在目标音频内随机采样2秒重叠片段作为条件，让模型学会从局部声学线索中提取精细的音色与频谱特征；第二阶段强制使用最后2秒的非重叠条件，迫使模型利用视频内部（如相同材质、相同动作产生的）声学自相似性，将已学到的声学特性推广到全新时序场景。这一设计使模型既能从参考音频中捕获足以重建目标声音的声学信息，又能避免条件泄露引发的退化复制（消融实验中，仅用重叠条件导致分布匹配指标 FD_PaSST 高达80.07，切换为非重叠模式后骤降至56.00，降幅30.1%；Table 4）。在声学编码器的选择上，使用预训练音频VAE的潜在特征（经平均池化）来保留完整频谱/音色信息，而非依赖仅捕捉语义的CLAP编码器，这在实验中带来了梅尔倒谱失真（MCD）从14.63到11.37的显著改善（↓22.3%），进一步证明了完整声学签名对精细控制的必要性（Table 1）。人工评估亦显示，配备参考音频条件的AC‑Foley相比纯视觉‑文本的系统（MMAudio‑L‑V2）在声学保真度上赢率为83.5%，表明创作者可以通过更换参考音频直观、可靠地切换目标音色（Table 3）。

综上，本文的动机在于打破文本控制的上限，构建一个能够跟随音频样例进行声学迁移的视频到音频生成框架。其技术核心在于通过保留完整声学特征的编码方式与两阶段课程设计，使模型既能精确提取参考音频中的声学细节，又能灵活适配到新的视觉时序中，最终生成既忠于参考音色又与画面严格同步的声音。该框架同时兼容文本描述和同步信号，通过多模态条件融合（Equation 3）共同引导生成过程，为可控的细粒度音效合成提供了新的范式。

## 核心创新

现有视频到音频生成方法的核心瓶颈在于：文本提示无法刻画微声学特征（如冲击瞬态、衰减共振），且训练数据将不同犬种叫声统统标为"barking"，导致生成结果差异性不足。AC‑Foley 的解决方案是 **以参考音频自身作为直接控制条件**，并通过 **两阶段训练策略** 与 **多模态同步融合** 两个关键设计解耦"声学复制"与"场景泛化"的矛盾。

### 1. 从语义到声学的条件编码升级

以往基于音频条件的方法（如 MMAudio+CLAP）使用 CLAP 模型提取语义特征（Table 1），仅保留粗粒度的类别信息，无法传递音色、频谱包络等精细声学线索。AC‑Foley 改用预训练的音频 VAE 编码器直接压缩参考波形，得到紧凑声学向量，完整保留频谱/音色签名。这一改动使生成音频与参考音色的 Mel Cepstral Distortion（MCD）从 **14.63 降至 11.37（↓22.3%）**（Table 1），直接证明了保留完整声学签名对精细控制的决定性作用。进一步消融表明，即使随机挑选参考音频，MCD 也始终远低于无音频条件的基线（Table 7），说明 VAE 编码确实传递了有效的声学引导信息，而非语义层面的类别复制。

### 2. 两阶段课程训练：从"复制粘贴"到泛化适配

仅更换编码器仍无法避免模型直接将参考片段"粘贴"到输出中——尤其是在条件片段与目标时序完全重叠时，模型会退化为直连拷贝（Table 4 中 Stage I 的 FD_PaSST 高达 **80.07**）。AC‑Foley 引入两阶段训练（Figure 3）：

- **Stage I（重叠条件）**：随机采样目标音频中的 2 秒作为参考，迫使模型学习提取声学特征（如音色、响度包络）。
- **Stage II（非重叠条件）**：将参考片段切换为时间上完全不重叠的后 2 秒，此时模型无法直接复制，必须 **利用视频内部的自相似性** 将提取到的声学模式适配到全新的时序上下文。

这一策略让 FD_PaSST 驟降至 **56.00（↓30.1%）**（Table 4），说明模型成功学会了泛化而不再是简单拼接。随后在音画高度对应子集上微调 40k 步（ImageBind > 0.3），进一步将语义一致性（IB）提升至 **37.1** 并将时序偏移压至 **0.465**（Table 4），形成了"特征提取—泛化适配—质量精炼"的完整训练闭环。

### 3. 多模态条件融合与同步锚点

为确保生成的音频既忠顺参考音色又严格对齐画面时序，AC‑Foley 构建了包含四项信号的条件向量 **c**：

- **音频声学特征**（VAE 池化输出）
- **文本语义特征**（CLIP 平均池化）
- **视频帧语义特征**（CLIP 平均池化）
- **同步特征**（Synchformer 重采样）

该向量通过自适应层归一化（adaLN）注入 Transformer 的每一层：

$$\operatorname{adaLN}(f, c) = \mathrm{LayerNorm}(f) \cdot \mathbf{W}_{\gamma}(c) + \mathbf{W}_{\beta}(c)$$

消融实验强烈佐证了这一融合方案的必要性：**移除同步条件（w/o sync）** 导致 DeSync 从 0.465 飙升至 **1.240**，Onset Acc 从 0.2832 锐减至 **0.2100**（Table 6），表明 Synchformer 提供的时序锚点是不可替代的；而移除音频条件虽略微改善同步（DeSync 0.410），却让分布匹配指标 FD_PaSST 从 56.00 回升至 64.90（Table 6），再度验证声学与同步控制缺一不可。

### 4. 创新效果的全局验证

上述三个模块的协同作用在综合评估中体现为显著优势：在 VGGSound 测试集上，AC‑Foley 面向音频条件的基线 MMAudio+CLAP 取得 **FD_PaSST 降低 13.7%、MCD 降低 22.3%**（Table 1）；且以 83.5% 的赢率在人工声学保真度判断中碾压最强视觉‑文本基线 MMAudio‑L‑V2（Table 3）。即使在未参与训练的 Greatest Hits 数据集上进行跨域音色迁移，仍以 **Onset Acc 0.3948 vs. 0.3906** 超越专门训练于该数据集的 CondFoley（Table 2），显示出两阶段训练赋予的强泛化性。这些证据共同证实：以音频自身为条件、结合渐进式课程训练与多模态同步融合，是当前视频到音频生成中实现细粒度可控、时序高对齐的核心创新路径。

## 整体框架

![[assets/figures/papers/iclr26_0005_URPXhnWdBF_AC-Foley_Reference-Audio-Guided_Video-to-Audio_S/figures/004_Figure_2.jpg]]
*Figure 2: Overview of our method. Different modalities (video, text, and audio) jointly interact in the multimodal transformer network. Multimodal conditioning with audio injects semantic, temporal and acoustic information for more precise control*

AC‑Foley 的整体流程以无声视频 **V**、参考音频 **A**_c 和可选的文本提示 **T** 为输入，输出一段与画面同步且保留参考声学特征的音频 **A**_t。其核心是一个在条件流匹配范式下工作的多模态 Transformer，整体生成过程可归结为

$$
{\bf A}_t = \mathcal{G}_{\boldsymbol{\theta}}\big({\bf V}, {\bf A}_c, {\bf T}\big).
$$

整个 pipeline 由以下模块串联而成，各模块负责不同模态的特征提取与多模态控制信息注入：

- **视觉编码器（CLIP‑ViT）**：从视频帧中提取帧级别的语义特征，用于描述画面的视觉内容。
- **文本编码器（CLIP‑Text）**：将文本提示 **T** 编码为语义向量，提供高层次的类别或意图信息。
- **音频 VAE 编码器（预训练）**：将参考音频波形压缩为紧凑的声学潜在向量。该编码器保留了完整的频谱/音色信息，而不像 CLAP 那样仅保留语义属性，使模型能准确再现冲击瞬态、共振衰减等细节。
- **同步特征提取器（Synchformer）**：从视频流中提取 24 fps 的音画同步特征，并通过最近邻插值匹配音频潜在表示的帧率，为 Transformer 提供细粒度的时序对齐信号。
- **多模态条件融合（AdaLL 调制层）**：上述视频、文本、音频、同步特征被组合成一个多模态条件向量 **c**。在 Transformer 的每一层中，**c** 通过自适应层归一化调制输入 **f**：
  $$
  \operatorname{adaLN}(f, c) = \operatorname{LayerNorm}(f) \cdot \mathbf{W}_{\gamma}(c) + \mathbf{W}_{\beta}(c),
  $$
  其中 $\mathbf{W}_\gamma$、$\mathbf{W}_\beta$ 为由多模态条件预测的缩放与偏移量。这使得生成过程同时受到语义、声学和时序信号的控制。
- **多模态 Transformer**：由 7 个多模态块和 14 个单模态块堆叠而成，是核心生成网络。在条件流匹配目标
  $$
  \mathbb{E}_{t, q(x_0), q(x_1, \mathcal{C})} \| v_\theta(t, \mathcal{C}, x_t) - (x_1 - x_0) \|^2
  $$
  的指导下，Transformer 学习预测从噪声 $x_0$ 到目标音频潜在表示 $x_1$ 的速度场 $v_\theta$，从而生成与视觉内容匹配的频谱表示。
- **声码器（HiFi‑GAN）**：将 Transformer 输出的梅尔频谱转换为 44.1 kHz 的时域波形，得到最终的合成音频。

训练时，AC‑Foley 采用两阶段课程学习策略来解决"复制粘贴"与泛化的矛盾：**第一阶段**从与目标音频重叠的片段中随机抽取 2 秒作为参考条件，强制模型提取细粒度声学特征；**第二阶段**切换为非重叠的尾部 2 秒作为条件，迫使模型利用视频内的声学自相似性进行泛化，从而在不牺牲时序同步的前提下实现可控的音色迁移与细粒度声音生成。

## 核心模块与公式推导

### 核心机制

AC‑Foley 的核心控制逻辑基于一个关键发现：文本描述无法精确刻画微声学特征（如冲击瞬态、共振衰减），而直接将参考音频的完整频谱/音色特征作为条件信号，可以绕过语义歧义，实现对生成声音的精细控制。通过两阶段训练迫使模型学习将参考声学特性适配到视频时序上下文，避免简单的"复制粘贴"行为。

### 关键模块

模型以多模态 Transformer 为核心生成网络，由 7 个多模态块和 14 个单模态块堆叠而成，整体流程如下：

1. **视觉编码器**：CLIP‑ViT 提取视频帧级视觉语义特征
2. **文本编码器**：CLIP‑Text 提取文本提示的语义特征
3. **音频 VAE 编码器**：将参考音频波形压缩为紧凑的声学潜在向量，经平均池化得到保留完整频谱/音色特征的紧凑表示，而非仅依赖语义级 CLAP 编码
4. **同步特征提取器 (Synchformer)**：提取音画同步特征（24fps），经最近邻插值匹配音频潜在表示帧率
5. **多模态条件融合**：将上述音频声学特征、文本语义特征（CLIP 平均池化）、视频特征（CLIP 平均池化）、同步特征拼接为统一的条件向量 $c$
6. **AdaLL 调制层**：利用条件向量 $c$ 对输入 $f$ 进行自适应层归一化，注入多模态控制信息
7. **Flow Matching 解码器**：从噪声通过 ODE 解轨迹生成目标音频潜在表示
8. **声码器 (HiFi‑GAN)**：将生成的梅尔频谱转换为 44.1kHz 时域波形

### 三个基本公式

**条件流匹配目标**：

$$
\mathbb { E } _ { t , q ( x _ { 0 } ) , q ( x _ { 1 } , \mathcal { C } ) } \| v _ { \theta } ( t , \mathcal { C } , x _ { t } ) - ( x _ { 1 } - x _ { 0 } ) \| ^ { 2 }
$$

其中 $x_0$ 为噪声，$x_1$ 为目标音频潜在表示，$\mathcal{C}$ 为多模态条件（视频、参考音频、文本），$v_\theta$ 是待训练的速度场，目标是从噪声到目标的路径与最优输运路径对齐。

**音频生成公式**：

$$
{\bf A}_t = \mathcal { G } _ { \boldsymbol { \theta } } \big ( {\bf V}, {\bf A}_c , {\bf T} \big )
$$

变量含义：$\mathbf{V}$ 为无声视频输入，$\mathbf{A}_c$ 为参考音频输入，$\mathbf{T}$ 为文本提示，$\mathcal{G}_\theta$ 为生成模型，输出合成音频 $\mathbf{A}_t$。

**自适应层归一化 (adaLN)**：

$$
\operatorname { a d a L N } ( f , c ) = \operatorname { L a y e r N o r m } ( f ) \cdot \mathbf { W } _ { \gamma } ( c ) + \mathbf { W } _ { \beta } ( c )
$$

变量含义：对输入 $f$ 进行标准层归一化后，由条件向量 $c$ 经 MLP 预测尺度因子 $\mathbf{W}_\gamma(c)$ 和偏移量 $\mathbf{W}_\beta(c)$ 进行调制。该机制是多模态条件注入 Transformer 的核心操作。

### 训练策略的两阶段差异

- **Stage I（重叠条件）**：从 8 秒目标音频中随机采样 2 秒片段作为条件音频，学习提取声学特征——但若仅停留于此，模型倾向于"复制粘贴"，FD_PaSST 高达 80.07
- **Stage II（非重叠条件）**：使用最后 2 秒非重叠片段作为条件，迫使模型利用视频内部的声学自相似性来泛化，FD_PaSST 骤降至 56.00（↓30.1%）
- **高对应子集微调**：在 ImageBind 音画对应分数 >0.3 的子集上微调 40k 迭代，进一步提升语义一致性（IB 37.1）和时序对齐（DeSync 0.465）

### 条件设计的关键性

消融实验显示，移除同步条件（w/o sync）使 DeSync 从 0.465 升至 1.240，严重破坏时间对齐；而去掉音频条件虽略微改善时序，却使 FD_PaSST 从 56.00 升至 64.90。这表明**同步条件负责时序对齐，音频条件负责音质与声学保真度，二者不可相互替代**。

## 实验与分析

AC‑Foley 以参考音频自身作为声学控制信号，绕过了文本语义模糊性对微声学特征（冲击瞬态、共振衰减等）的描述局限。以下实验系统验证了该设计对生成声音的音色保真度、时序同步性及跨场景泛化能力的提升，并进一步通过消融实验揭示各组件间的因果分工。

### 主实验结果

**定量对比（VGGSound，表 1）。**  
在筛选后的 8 676 个 VGGSound 测试视频上，AC‑Foley 相比基于 CLAP 语义编码的音频条件基线（MMAudio+CLAP）在所有关键指标上均大幅领先：  

![[assets/figures/papers/iclr26_0005_URPXhnWdBF_AC-Foley_Reference-Audio-Guided_Video-to-Audio_S/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison of video-to-audio generation methods across multiple metrics. Best results are bolded; second-best results are underlined*

- 分布匹配：FD$_{\text{PaSST}}$ 从 64.90 降至 **56.00**（↓13.7%），表明生成音频的全局声学统计更接近真实分布；  
- 频谱质量：MCD 从 14.63 降至 **11.37**（↓22.3%），验证了直接使用 VAE 保留完整频谱/音色特征（而非仅 CLAP 语义）的必要性；  
- 时序对齐：DeSync 从 0.558 降至 **0.465**（↓16.7%），得益于多模态融合中显式注入的同步特征（Synchformer）。  

与当前无音频条件的最优方法相比（表 1 下半部分），AC‑Foley 同样在分布匹配类指标上取得最优或次优，说明参考音频控制下的生成质量已超越纯视觉‑文本范式。

**跨数据集音色迁移（Greatest Hits，表 2）。**  
AC‑Foley **未使用** Greatest Hits 参与训练，仅在 VGGSound 上训练后直接推理，仍在该数据集的音色迁移任务上超越专训方法 CondFoley（Onset Acc. 0.3948 vs 0.3906，MCD 3.39 vs 4.18）。这表明模型通过两阶段训练习得的"参考声学特征适配视频上下文"能力可跨域泛化，并非对训练分布的简单记忆。

**人工评估（表 3）。**  
以 16 个高音画对应度的视频为样本，要求被试从 AC‑Foley 和纯视觉‑文本基线 MMAudio‑L‑V2 中，就"声学相似度"和"同步性"分别选择更优者。结果：声学保真度上 AC‑Foley 赢率高达 **83.5%**（95 %CI ±3.4%），而时序对齐赢率为 61.6% 并有 21.8% 的样本被判定为"两者均同步良好/难以区分"。这印证了参考音频控制的核心增益在于音色忠实度，而同步性能受限于模型对视频事件节奏的固有建模能力（该能力在较强基线中已具备一定基础）。


![[assets/figures/papers/iclr26_0005_URPXhnWdBF_AC-Foley_Reference-Audio-Guided_Video-to-Audio_S/figures/010_Table_3.jpg]]
*Table 3: Comparison of our method and MMAudio-L-V2 in terms of temporal alignment and acoustic fidelity. We show our win rate and the tie rate of temporal alignment, and our win rate of acoustic fidelity. 95% confidence intervals are reported in gray*

### 消融实验

**两阶段训练机制（表 4）。**  
仅使用重叠条件片段（Stage I）时，FD$_{\text{PaSST}}$ 高达 80.07，表明模型倾向于直接"复制粘贴"参考音频，失去与视频的时序适配。切换为非重叠条件（Stage II）后，该指标骤降至 **56.00**（↓30.1%），说明模型被迫利用视频内部的声学自相似性来生成匹配的未知部分，从而获得泛化。在此基础上对高音画对应子集（ImageBind 分数 > 0.3）微调 40k 迭代，进一步将语义一致性（IB）提升至 37.1，DeSync 降至 0.465，证实两阶段课程训练是解决"复制粘贴"与泛化矛盾的决定性机制。


![[assets/figures/papers/iclr26_0005_URPXhnWdBF_AC-Foley_Reference-Audio-Guided_Video-to-Audio_S/figures/011_Table_4.jpg]]
*Table 4: Performance comparison of audio conditioning approaches (overlapping/non-overlapping segments) and finetuning strategies across distribution matching (FD/KL), semantic consistency (IB), temporal alignment (DeSync), and spectral quality (MCD) metrics*

**条件组件必要性（表 6）。**  
推理时分别屏蔽音频、同步、视频、文本条件：  

![[assets/figures/papers/iclr26_0005_URPXhnWdBF_AC-Foley_Reference-Audio-Guided_Video-to-Audio_S/figures/013_Table_6.jpg]]
*Table 6: Results when we mask out different conditioning components during inference*

- 移除音频条件使 FD$_{\text{PaSST}}$ 从 56.00 升至 64.90，声学匹配严重退化，而 DeSync 却略微改善（0.410），再次证明音频条件负责音色保真度、同步条件负责时序对齐，二者分工清晰、不可偏废；  
- 移除同步条件（w/o sync）导致 DeSync 从 0.465 激增至 **1.240**，Onset Acc. 从 0.2832 跌至 0.2100，暴露了 Synchformer 特征在提供细粒度时间对齐信号上的关键作用。

**池化策略与条件有效性（表 5、表 7）。**  
平均池化与注意力池化性能相当（前者训练更稳定、计算成本更低），验证了紧凑声学向量已能良好保留音色、音高等关键特征。进一步地，当以学习到的空嵌入向量替代真实参考音频作为条件时（固定视频输入），使用五种随机参考音频所生成的音频 MCD 均显著更低（如 Ref. D：12.20 vs 22.74），排除偶然性，确证参考音频驱动了音色控制。

### 失败模式与局限性

1. **多并发声源**：当视频中包含对话、环境噪声与物体交互等多重声源时，模型无法显式将某一参考声源精确对齐到对应视觉触发器，可能出现声源分配错误。  
2. **节奏极端失配**：参考音频的节奏模式与视频事件节奏严重冲突（例如慢速猫叫声驱动快速键盘敲击画面）时，生成质量下降，表明时序适配机制仍有上限。  
3. **评估指标偏差**：同步指标 DeSync 基于 Synchformer（上下文窗口仅 4.8 s），且真实音频本身存在约 0.558 s 的平均偏移，可能低估长序列的细粒度对齐性能，需谨慎解读。

### 关键图表要点提示

- **表 1** 与 **表 4** 共同勾勒因果链条：VAE 声学编码 → 非重叠两阶段训练 → 声学保真与泛化兼得。  
- **表 6** 是理解"同步负责时间，音频负责音色"的抓手，定义了多模态条件的职责边界。  
- **定性结果（Figure 4）**：针对同一视频，三种不同参考音频生成出音色鲜明可辨的音频，直观验证了模型对微声学特征的精细化控制能力。

### 补充图表

![[assets/figures/papers/iclr26_0005_URPXhnWdBF_AC-Foley_Reference-Audio-Guided_Video-to-Audio_S/figures/006_Figure_3.jpg]]
*Figure 3: Illustration of the two-stage training process for audio generation. (a) Stage I: Overlapping Conditioning. The random 2 seconds of the 8-second target audio are used as the conditional audio, allowing the model to learn the utilization of acoustic features from overlapping audio segments. (b) Stage II: Non-overlapping Conditioning. The non-overlapping last 2 seconds of the 10-second video clip are used as the conditional audio, leveraging inherent audio self-similarity within the video to enhance model generalization*


## 方法谱系与知识库定位

### 1. 在视频到音频生成谱系中的定位

AC‑Foley 的核心创新在于将控制信号从**语义层级**下推至**声学特征层级**，这使其处于传统"视频‑文本到音频"方法与"跨模态音色迁移"方法的交汇点上。

**与纯视觉‑文本基线（MMAudio, FoleyCrafter, V‑AURA）的关系。** 这些方法依赖文本提示指定期望的声音类别（如"狗叫"），但文本描述的固有歧义导致生成结果仅能覆盖类别层面的统计平均，无法区分同类别内的微声学差异（如大狗低沉吠叫 vs 小狗尖细吠叫）。AC‑Foley 通过引入参考音频作为直接控制条件，将生成目标从 $p(\text{audio} | \text{video}, \text{text_label})$ 转变为 $p(\text{audio} | \text{video}, \text{reference_audio})$，绕过了文本瓶颈。这一转变的实验证据来自 MMAudio+CLAP 与 AC‑Foley 的对比：当用预训练 VAE 编码器替代 CLAP 语义编码器后，MCD 从 14.63 骤降至 11.37（↓22.3%, Table 1），直接证明了保留完整声学签名对精细控制的必要性。

**与音频条件方法（Video‑Foley, CondFoley）的关系。** Video‑Foley 首次尝试了音频条件生成，但性能较弱。CondFoley 利用参考视频‑音频对进行音色控制，但其训练配置与评估框架更接近单数据集内的监督学习。AC‑Foley 与 CondFoley 的关键区别在于**训练策略**和**跨数据集泛化能力**：CondFoley 直接训练于 Greatest Hits 数据集，而 AC‑Foley 未使用该数据集训练，却在 Greatest Hits 的零样本音色迁移任务上以 Onset Acc. 0.3948 优于 CondFoley 的 0.3906（Table 2），展示了更好的泛化性。然而需要指出，这一对比并非完全公平——CondFoley 在评估集上具有分布内优势，AC‑Foley 的微小优势（+1.1%）需要谨慎解读。

### 2. 核心机制的因果分析

**瓶颈识别与因果开关。** 现有方法的根本瓶颈在于：训练数据将所有狗叫声统一标注为"barking"，导致模型无法学习同类别内的声学变体分布。AC‑Foley 的双重因果开关在于：（a）用 VAE 编码器替换 CLAP，保留频谱/音色完整信息（而非仅语义）；（b）两阶段训练解决"复制粘贴"与泛化的矛盾。两者的因果效应均有强消融证据支撑——仅 VAE 编码替换已带来 22.3% 的 MCD 降低；而两阶段训练的单独贡献体现在 Table 4：纯重叠条件导致 FD_PaSST 停留在 80.07（模型简单复制条件片段），切换为非重叠条件后骤降至 56.00（↓30.1%），说明非重叠阶段强制模型利用视频内部的声学自相似性进行泛化。

**同步条件的独立作用。** 消融实验揭示了一个关键的**功能解耦**：同步特征（Synchformer）与音频条件各自负责不同维度的生成质量。移除同步条件使 DeSync 从 0.465 退化至 1.240，Onset Acc. 从 0.2832 跌至 0.2100；而去掉音频条件虽略微改善 DeSync（0.410），却使 FD_PaSST 从 56.00 升至 64.90（Table 6）。这表明**时序对齐与音色保真度分别由同步特征和音频条件主导**，二者不可相互替代。这一发现对后续多模态融合设计具有指导意义：不应期望单一条件组件同时解决多个正交目标。

### 3. 适用边界与泛化能力

**强泛化场景。** 人工评估中 83.5% 的声学保真度赢率（vs MMAudio‑L‑V2, Table 3）以及跨数据集的 Greatest Hits 零样本迁移结果表明，当目标声音与参考音频共享相似的物理产生机制（如敲击、摩擦、吠叫的共振腔特征）时，AC‑Foley 能有效提取并适配声学线索。模型似乎学习到了一种"声学材质"的抽象表示，而非简单的频谱模式匹配。

**已知局限与失效模式。**
- **多声源混叠。** 当视频同时包含多个独立声源（对话 + 环境噪声 + 物体交互）时，模型无法将不同参考声源显式分配给对应视觉触发器。这是架构层面的限制：当前设计使用全局条件向量 $\mathbf{c}$ 经 adaLN 统一调制所有帧，缺乏空间/对象的局部化控制机制。
- **时序模式极端不匹配。** 用慢速猫叫声驱动快速键盘敲击画面时，模型需要在保留参考音色和适配视频节奏之间做出权衡，但当前框架缺乏显式的节奏映射机制——同步损失（DeSync）和声学保真度损失可能相互冲突。
- **评估指标的潜在偏差。** 同步评估依赖 Synchformer，其上下文窗口仅 4.8 秒，且 GT 音频本身存在 0.558 秒的平均偏移。这意味着：评估偏向短时对齐而忽略长期漂移；0.465 的"最优"DeSync 可能部分源自指标局限而非真正的完美对齐。该点需要后续研究者注意，不宜直接将 AC‑Foley 的 DeSync 值视为同步性的绝对上限。

### 4. 开放问题与未来方向

**对象级声源分配。** 最具挑战性的开放问题是如何实现细粒度的声源‑对象绑定。一个可能的扩展方向是引入视觉对象分割先验，使条件向量 $\mathbf{c}$ 空间化，让不同区域受不同参考音频调制。但这要求训练数据具有对象级声源标注，当前数据生态尚不支持。

**节奏冲突的仲裁机制。** 当参考音频节奏与视频事件节奏冲突时，应以何者为主？从拟音实践看，画面同步通常优先于音色保真度，但自动化系统中需要显式设计损失权重或门控机制来仲裁这一冲突。该问题在用户研究中已有暗示：虽然声学保真度赢率达 83.5%，但同步性的"两者皆好/难以选择"选项占 21.8%，说明存在部分样本中音色和同步的张力。

**同步评估指标的改进需求。** Synchformer 的 4.8 秒上下文窗口和 GT 偏移问题表明，社区需要更可靠的长序列同步评估方案。可能的替代方向包括基于学习对齐的动态时间规整指标或基于自监督对比的跨模态排序损失，但目前尚无成熟的即插即用方案。

**跨域泛化的上限。** AC‑Foley 在 Greatest Hits（敲击类声音）上的成功是否可推广至持续音（如引擎轰鸣、风声）和非刚性材质交互（如布料摩擦、液体倾倒）？敲击类声音具有明确的瞬态起始点，易于检测和建模；持续音和柔性材质交互的声学特征更依赖长期频谱演化，对当前基于单样本参考的编码方式提出了不同挑战——该方向需要在更广泛的数据集（如 AudioSet 的细分类别或专业音效库）上进行系统性评估。

**多声道空间音频扩展。** 当前方法生成单声道音频，如何将参考音频控制扩展至空间音频（如环绕声、双耳音频）是一个自然延伸。这需要额外的空间条件（如声源方位角、房间脉冲响应），且参考音频本身需携带空间信息，架构复杂度将显著增加。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/AC_Foley_Reference_Audio_Guided_Video_to_Audio_Synthesis_with_Acoustic_Transfer.pdf

![[paperPDFs/ICLR_2026/AC_Foley_Reference_Audio_Guided_Video_to_Audio_Synthesis_with_Acoustic_Transfer.pdf]]
