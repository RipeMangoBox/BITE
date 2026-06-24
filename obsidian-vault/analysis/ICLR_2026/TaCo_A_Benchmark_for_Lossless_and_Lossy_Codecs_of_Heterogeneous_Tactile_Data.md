---
title: "TaCo: A Benchmark for Lossless and Lossy Codecs of Heterogeneous Tactile Data"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/TaCo_A_Benchmark_for_Lossless_and_Lossy_Codecs_of_Heterogeneous_Tactile_Data.pdf
openreview_forum_id: 1PYXFkS6Hy
aliases:
- TLTL
- TaCo
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "通过大量触觉数据端到端训练数据驱动的神经编解码器，使模型能够捕获异构触觉信号（视觉触觉图像、力向量）的本征分布与结构化冗余，从而最大化压缩比并保留下游任务关键信息。"
primary_logic: "将异构触觉数据统一映射为二维图像格式，复用成熟的图像/视频压缩框架；在此基础上，利用触觉数据特有的模态分布对神经编解码器进行全量训练（TaCo-LL和TaCo-L），能够大幅超越跨模态预训练的通用模型，在无损存储、人类可视化、分类与灵巧抓取四项任务上实现当前最优性能。"
claims:
- "TaCo-LL-96M在所有五个数据集上达到最佳无损压缩，bits/Byte低至0.360（22×压缩比）。"
- "TaCo-L在四个数据集上的有损BD-Rate下降19.2%–61.8%，远超其他编解码器。"
- "TaCo-L在124×压缩比下，TouchandGo分类SVM准确率仅下降1.51%。"
- "TouchandGo 上 bits/Byte (↓) = 0.447 (TaCo-LL-96M)"
---

# TaCo: A Benchmark for Lossless and Lossy Codecs of Heterogeneous Tactile Data

> [!tip] 核心洞察
> 将异构触觉数据统一映射为二维图像格式，复用成熟的图像/视频压缩框架；在此基础上，利用触觉数据特有的模态分布对神经编解码器进行全量训练（TaCo-LL和TaCo-L），能够大幅超越跨模态预训练的通用模型，在无损存储、人类可视化、分类与灵巧抓取四项任务上实现当前最优性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | TaCo：异构触觉数据无损与有损编解码器基准测试 |
| 英文题名 | TaCo: A Benchmark for Lossless and Lossy Codecs of Heterogeneous Tactile Data |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=1PYXFkS6Hy) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | TaCo-LL（无损压缩）和TaCo-L（有损压缩） |
| Dataset | TouchandGo, ObjTac, YCB-Slide |

> [!tip] 效果简介
> - TouchandGo 上，bits/Byte (↓) 为 0.447 (TaCo-LL-96M)，对比 1.199 (JPEG-XL)，变化 -0.752。
> - ObjTac 上，bits/Byte (↓) 为 0.360 (TaCo-LL-96M)，对比 1.309 (JPEG-XL)，变化 -0.949。
> - TouchandGo 上，BD-Rate (%) (↓) 为 -61.8% (TaCo-L)，对比 0% (HM-Intra)，变化 -61.8%。

## 概述

实时机器人遥操作与灵巧操作依赖高带宽触觉感知，但触觉传感器产生的异构数据（视觉触觉图像、力向量）体量庞大，传输与存储成本高昂。现有压缩方案碎片化严重：通用编解码器（gzip、PNG、JPEG-XL、HEVC/VVC等）未针对触觉信号的统计特性与时空冗余进行设计，压缩效率低下；而触觉专用编解码器缺乏系统性基准测试，难以比较优劣。

TaCo是首个面向异构触觉数据编解码器的综合基准测试，覆盖5个公开触觉数据集（超25万帧）、30种编解码器（14种无损、16种有损），以及4类下游任务：无损存储、人类可视化、材料/物体分类和灵巧抓取。核心发现是：**将触觉数据统一映射为图像格式后，使用触觉数据端到端训练的神经编解码器能够捕获异构信号的本征分布与结构化冗余，从而在压缩比与任务保真度上大幅超越跨模态预训练的通用模型**。

基于此，本文提出TaCo-LL（无损）和TaCo-L（有损）两种数据驱动的触觉编解码器。TaCo-LL将触觉帧分割为16×16×3 patches，通过自回归概率模型与算术编码器实现无损熵编码；TaCo-L采用分析-合成变换与超先验自编码器，在率失真目标下进行有损压缩。两者均在触觉数据集上从头训练，不依赖自然图像或文本预训练。

主要结果如下：

- **无损压缩**：TaCo-LL-96M在所有五个数据集上取得最低bits/Byte，其中ObjTac数据集低至0.360（22×压缩比），TouchandGo为0.447（18×），远超JPEG-XL等最优通用编解码器（Table 2）。
- **有损压缩**：TaCo-L在四个数据集上BD-Rate下降19.2%–61.8%，其中TouchandGo达-61.8%，YCB-Slide达-27.4%，显著优于VTM-Intra、JPEG-XL等传统编码器及预训练神经编解码器（Table 4）。
- **下游任务保真度**：在124×压缩比下，TouchandGo材料分类SVM准确率仅从76.63%降至75.12%（-1.51%）；在190×压缩比下，YCB-Slide物体分类准确率从99.35%降至98.01%（-1.34%）（Table 6）。灵巧抓取任务中，TaCo-L在0.025 BPP极低码率下平均成功率62.2%，与未压缩数据（24 BPP，63.8%）相差仅1.6个百分点（Table 7）。

这些结果表明，数据驱动的触觉专用编解码器在存储效率与任务性能之间实现了当前最优的权衡，为机器人系统的实时触觉传输提供了可行路径。

## 背景与动机

触觉感知是机器人灵巧操作与环境交互的核心模态，视觉触觉传感器（如GelSight、DIGIT）和力传感器能够捕获接触几何、纹理与三维力分布等关键信息。然而，高分辨率触觉数据产生巨大的数据吞吐量——单个视觉触觉传感器每秒可产生数百MB的原始数据——在实时遥操作、多模态记录与边缘推理等场景中，传输带宽与存储成本成为瓶颈。因此，高效的触觉数据压缩成为机器人系统实用化的关键使能技术。

现有压缩方法的根本缺口在于**碎片化与跨模态不适配**。一方面，通用无损压缩器（gzip、zstd、bzip2）仅利用一维符号冗余，无法利用触觉数据的二维空间结构；通用图像/视频编解码器（PNG、JPEG-XL、HEVC/VVC）虽能捕获空间与时空冗余，但其设计假设（自然图像统计、人类视觉系统感知）与触觉信号的分布特性存在本质差异。另一方面，神经编解码器（如ELIC、LALIC、DCVC系列）在自然图像上表现优异，但均基于ImageNet等视觉数据集预训练，其学到的先验分布无法迁移至触觉域——触觉图像具有独特的局部几何纹理、接触边界和力场结构，这些模式在自然图像语料中几乎不存在。

上述碎片化格局导致三个关键问题悬而未决：（1）缺乏统一的触觉压缩基准，无法系统比较不同范式在异构触觉数据上的压缩效率；（2）尚未有方法针对触觉数据分布进行端到端训练，数据驱动的压缩潜力未被挖掘；（3）压缩对下游机器人任务（如材质分类、灵巧抓取）的影响缺乏量化评估。

针对这些缺口，TaCo基准测试提出两条核心思路。**第一**，构建覆盖5个异构触觉数据集、30个编解码器、4类评估任务的系统性评测框架，统一度量无损压缩、面向人类可视化的有损压缩、面向机器分类与抓取的任务保持压缩。**第二**，首次引入纯数据驱动的触觉编解码器TaCo-LL（无损）和TaCo-L（有损），在触觉数据上端到端训练，使其学习异构触觉信号的本征分布与结构化冗余，从而在压缩比与任务保真度两个维度上建立新的基准。

## 核心创新

TaCo-LL 和 TaCo-L 的核心创新并非提出全新的压缩架构，而是通过**训练数据域的迁移**和**触觉信号的表征定制**，将成熟的图像/视频压缩范式适配到异构触觉数据上，从而释放数据驱动压缩在触觉领域的潜力。

### 关键创新点：从跨模态迁移到域内端到端训练

现有神经编解码器（如 DLPR、ELIC、LALIC、DCVC 系列）均在自然图像或视频上预训练，其学到的统计先验与触觉数据存在根本性分布偏移。TaCo 的核心操作是将训练数据域从 ImageNet/LLM 语料切换为异构触觉数据集（Touch and Go 和 ObjectFolder 的 70% 子集），对 DualComp-I 和 LALIC 进行端到端重训练（Section 3.2.2）。这一 changed slot 是性能跃升的因果枢纽：

- **无损压缩**：TaCo-LL-96M 在所有五个数据集上达到最优 bits/Byte，ObjTac 上低至 0.360（22× 压缩比），远超 JPEG-XL（1.309）等通用编解码器（Table 2）。预训练的神经无损方法（DLPR、P2LLM）在触觉数据上甚至不如 gzip，进一步验证了域适配的必要性。
- **有损压缩**：TaCo-L 在四个数据集上的 BD-Rate 下降 19.2%–61.8%，其中 TouchandGo 上 -61.8% 的码率节省远超第二名 VTM-SCC（Table 4）。这一优势源于模型在训练中捕获了触觉数据的本征低维流形，而非依赖通用的图像纹理先验。

### 触觉信号表征的定制化映射

将异构触觉数据统一映射为图像格式是复用成熟压缩框架的前提，但 TaCo 在表征层面做了模态特定的设计（Figure 3）：

- **视觉触觉数据**：将 RGB 值按子像素顺序展开为 16×16×3 的 patch，保留局部空间相关性，而非简单地将整帧视为自然图像。
- **力向量数据**：将三轴力信号映射为 RGB 三通道，沿时间维度堆叠生成 T×60 的“力图像”。这一映射使得力信号的时序冗余可被图像压缩框架捕获。

这种表征策略本身不改变压缩模型结构，但确保了触觉信号的物理结构（空间接触几何、力方向分量）在 tokenization 阶段被保留，而非被通用的图像 patch 划分方式破坏。

### 有损压缩的输入尺寸统一

TaCo-L 引入了一个看似微小但实际关键的 changed slot：将输入统一裁剪或零填充至 256×256 分辨率（Section 3.2.2）。触觉数据集的分辨率差异极大（从 GelSight 的 480×640 到 DIGIT 的 240×320），LALIC 原生支持不定尺寸输入，但统一的输入尺寸消除了分辨率差异带来的码率分配偏差，确保模型专注于学习触觉内容本身的冗余模式，而非尺寸缩放引入的伪影。

### 创新边界与验证局限

上述 changed slots 的有效性已在五个数据集和四项任务上得到验证，但需注意：训练数据仅覆盖 GelSight 和 DIGIT 两种视觉触觉传感器及一种力传感器，对其他传感器类型（如 BioTac、TacTip）的泛化能力尚未验证。此外，TaCo-L 的 63.2M 参数量使其在嵌入式平台上的部署仍需进一步压缩或蒸馏。

## 整体框架

![[assets/figures/papers/iclr26_0009_1PYXFkS6Hy_TaCo_A_Benchmark_for_Lossless_and_Lossy_Codecs_o/figures/001_Figure_1.jpg]]
*Figure 1: The motivation of our TaCo benchmark, established through an extensive evaluation on tactile codecs across multiple dimensions. First, we assess 30 off-the-shelf and neural codecs on 5 heterogeneous tactile datasets with more than 250K frames. Second, we introduce purely-trained TaCo-LL and TaCo-L codecs to explore the data-driven approaches in the field of lossless and lossy tactile data compression. Finally, we evaluate the coding performance on 4 distinct task types designed to serve for human, machine, and robotics*

TaCo 基准测试的核心动机源于一个现实瓶颈：实时机器人应用（如灵巧抓取、远程操作）亟需高效的触觉数据压缩，但现有编解码器碎片化严重，通用图像/视频压缩方法难以适配异构触觉数据的统计学特性与时空冗余。为此，TaCo 构建了一个涵盖 5 个异构触觉数据集、30 种编解码器、4 类下游任务的系统化评估框架，并在此基础上引入首个完全数据驱动的触觉编解码器 TaCo-LL 与 TaCo-L，其整体 pipeline 如图 1 所示。

### 数据流与统一表征

pipeline 的输入端为两类异构触觉信号：视觉触觉数据（如 GelSight、DIGIT 传感器采集的 RGB 形变图像）与力触觉数据（三轴力向量序列）。所有信号首先经过**统一表征映射**，转换为标准化的二维图像格式：

- **视觉触觉图像**：直接保留其 RGB 三通道空间结构，按 16×16×3 的 patch 进行分割，patch 内 RGB 子像素按光栅扫描顺序展开为离散符号序列。
- **力触觉信号**：将每个时间步的三轴力向量 $(f_x, f_y, f_z)$ 映射为 RGB 像素的三个颜色通道，并沿时间维度堆叠 $T$ 个读数，生成分辨率为 $T \times 60$ 的力触觉图像。

这一映射策略使得后续压缩模块能够复用成熟的图像/视频压缩框架，同时保留了触觉信号的本征空间与时空结构。

### 压缩分支：无损与有损

统一表征后的数据进入两条并行的压缩分支：

**TaCo-LL（无损分支）** 采用自回归概率建模范式。输入触觉帧经 patch tokenization 分割为 16×16×3 的离散符号序列后，依次通过：
1. **自回归概率模型** $f_a$：基于已编码符号 $\boldsymbol{x}_{<i}$ 预测下一符号 $x_i$ 的概率分布 $p(x_i | \boldsymbol{x}_{<i})$；
2. **算术编码器**：利用预测分布进行无损熵编码。

训练目标为最小化负对数似然的期望，即熵下界：
$$\mathcal{L} = \mathbb{E}[-\log_2(p(x_i | \boldsymbol{x}_{<i}))]$$

**TaCo-L（有损分支）** 采用率失真优化的神经压缩范式，架构基于 LALIC 模型，包含：
1. **分析变换** $g_a$：将 256×256 输入触觉图像映射到潜在表示 $\boldsymbol{y}$（含 4 次下采样）；
2. **量化模块** $Q$：将连续潜在变量离散化为 $\hat{\boldsymbol{y}}$；
3. **超先验自编码器**（$h_a$ / $h_s$）：生成边信息 $\hat{z}$ 以精确估计 $\hat{\boldsymbol{y}}$ 的分布；
4. **算术编码器**：对 $\hat{\boldsymbol{y}}$ 进行熵编码；
5. **合成变换** $g_s$：从 $\hat{\boldsymbol{y}}$ 重建触觉图像 $\hat{\boldsymbol{x}}$（含 4 次上采样）。

训练目标为率失真联合损失：
$$\mathcal{L} = \lambda \times \mathcal{D}(\pmb{x}, \hat{\pmb{x}}) + \mathbb{E}[-\log_2(p_{\hat{\pmb{y}}|\hat{z}}(\hat{\pmb{y}}|\hat{z}))]$$
其中 $\lambda$ 控制重建失真 $\mathcal{D}$ 与码率的权衡。

### 关键设计决策

TaCo-LL 与 TaCo-L 与通用预训练编解码器的核心差异在于**训练数据域**：两者均在 Touch and Go 与 ObjectFolder 数据集上端到端训练，使模型能够捕获触觉数据的本征分布与结构化冗余，而非依赖 ImageNet 等自然图像预训练权重。这一因果控制变量（causal knob）是 TaCo 系列在压缩效率上大幅超越跨模态预训练模型（如 DLPR、ELIC、DCVC-DC）的根本原因——证据显示，TaCo-LL-96M 在所有五个数据集上达到最优无损压缩（bits/Byte 低至 0.360，对应 22× 压缩比），TaCo-L 在四个数据集上的有损 BD-Rate 下降 19.2%–61.8%。

### 评估出口

压缩后的码流最终服务于四类下游任务，构成 pipeline 的评估出口：
- **无损存储**：评估原始比特率节省；
- **人类可视化**：评估有损重建的 PSNR 质量；
- **机器分类**：在 TouchandGo、ObjectFolder、YCB-Slide 上测试 SVM / Random Forest / K-NN 等分类器的准确率保持；
- **灵巧抓取**：在 Nvidia IsaacSim 仿真环境中，使用配备 11 个触觉传感器的 DexHand13 灵巧手，评估压缩对抓取成功率的影响。

这一多任务评估体系确保了编解码器的性能不仅体现在信号保真度指标上，更直接关联到机器人与人类使用场景的实际效用。

## 核心模块与公式推导

### 3.1 触觉信号的图像化表征

异构触觉数据的核心瓶颈在于其模态异质性——视觉触觉传感器（如GelSight、DIGIT）输出RGB图像，而力传感器输出三维力向量。TaCo通过统一的图像化映射策略消除这一差异：

- **视觉触觉数据**：直接保留原始RGB三通道图像格式，将空间分辨率统一映射为标准图像张量。
- **力触觉数据**：将每个三维力向量 $(f_x, f_y, f_z)$ 映射为一个RGB像素的三个颜色通道，并沿时间维度堆叠 $T$ 个采样点，生成 $T \times 60$ 分辨率的伪图像。这一映射将一维时序信号的结构化冗余转化为二维空间冗余，使成熟的图像/视频压缩框架可直接复用。

### 3.2 数据驱动编解码器架构

TaCo-LL和TaCo-L分别针对无损和有损压缩场景，其架构设计遵循数据驱动压缩的基本范式（Figure 2）：

#### 3.2.1 TaCo-LL：无损压缩管线

TaCo-LL的压缩流程由三个核心模块串联构成：

1. **Patch Tokenization（分块分词）**：将输入触觉帧划分为 $16 \times 16 \times 3$ 的patch，按光栅扫描顺序展开为一维符号序列 $\{x_1, x_2, \dots, x_n\}$。该分块策略在保留局部空间相关性的同时，将连续像素值离散化为可熵编码的符号单元。

2. **Autoregressive Probability Model（自回归概率模型）**：基于已编码的历史符号 $\boldsymbol{x}_{<i}$，通过神经网络 $f_a$ 预测当前符号 $x_i$ 的条件概率分布 $p(x_i \mid \boldsymbol{x}_{<i})$。模型参数量可在12M、48M、96M三档配置间扩展。

3. **Arithmetic Coder（算术编码器）**：利用预测概率分布对符号序列执行无损熵编码，将符号流压缩为紧凑的比特流。解码端通过相同的自回归模型和算术解码器恢复原始序列。

**训练目标**：最小化下一符号预测的负对数似然期望，即编码长度的熵下界：

$$\mathcal{L} = \mathbb{E}[-\log_2(p(x_i \mid \boldsymbol{x}_{<i}))] \tag{1}$$

该损失函数直接优化码率，无需显式重建约束。

#### 3.2.2 TaCo-L：有损压缩管线

TaCo-L采用基于超先验的变换编码架构，其网络结构继承自LALIC模型，包含以下模块：

1. **Analysis Transform $g_a$（分析变换）**：通过四次下采样操作将输入触觉图像 $\boldsymbol{x}$ 映射到潜在表示 $\boldsymbol{y}$。输入统一裁剪或零填充至 $256 \times 256$ 分辨率，三通道设计同时兼容视觉触觉和力触觉数据。

2. **Hyperprior Autoencoder（超先验自编码器）**：由分析变换 $h_a$ 和合成变换 $h_s$ 组成，从 $\boldsymbol{y}$ 中提取边信息 $\boldsymbol{z}$，用于估计潜在变量的空间分布 $p_{\hat{\boldsymbol{y}} \mid \hat{z}}$，从而提升熵编码效率。

3. **Quantization $Q$ & Arithmetic Coder（量化与算术编码）**：将连续潜在表示 $\boldsymbol{y}$ 离散化为 $\hat{\boldsymbol{y}}$，随后利用超先验估计的分布进行算术编码。

4. **Synthesis Transform $g_s$（合成变换）**：通过四次上采样操作从 $\hat{\boldsymbol{y}}$ 重建触觉图像 $\hat{\boldsymbol{x}}$。

**训练目标**：采用率失真联合优化：

$$\mathcal{L} = \lambda \times \mathcal{D}(\boldsymbol{x}, \hat{\boldsymbol{x}}) + \mathbb{E}[-\log_2(p_{\hat{\boldsymbol{y}} \mid \hat{z}}(\hat{\boldsymbol{y}} \mid \hat{z}))] \tag{2}$$

其中 $\mathcal{D}(\cdot, \cdot)$ 为重建失真（以PSNR度量），$\lambda$ 为控制码率-失真权衡的超参数。第二项为潜在表示的编码比特率期望。

### 3.3 训练数据域的关键变更

相较于通用神经压缩模型在ImageNet等自然图像上的预训练，TaCo-LL和TaCo-L的核心差异在于**训练数据域的端到端适配**：仅使用Touch and Go和ObjectFolder数据集的70%帧进行训练，使模型直接学习触觉信号的本征分布（如GelSight的压痕纹理模式、力向量的时序相关性），而非依赖跨模态迁移。这一策略是TaCo系列在压缩效率上大幅超越预训练基线（如DLPR、ELIC、DCVC系列）的根本原因。

## 实验与分析

### 核心瓶颈与因果机制

实时机器人遥操作与灵巧抓取对触觉数据的传输带宽提出严苛要求，但现有压缩方法面临双重瓶颈：**通用图像/视频编解码器（如JPEG-XL、VTM-Intra）无法有效捕获异构触觉信号的统计特性与结构化冗余**，而**触觉领域长期缺乏系统性基准测试**，导致方法碎片化、性能天花板不明确。

TaCo的核心因果杠杆在于**端到端数据驱动训练**：通过在触觉数据集（Touch and Go、ObjectFolder）上进行全量训练，TaCo-LL和TaCo-L能够学习视觉触觉图像与力向量信号的本征分布，而非依赖自然图像预训练的归纳偏置。这一设计直接转化为压缩效率的阶跃式提升——TaCo-LL-96M在ObjTac数据集上达到0.360 bits/Byte（22×压缩比），较最强通用无损编解码器JPEG-XL（1.309 bits/Byte）降低72.5%（Table 2）。

![[assets/figures/papers/iclr26_0009_1PYXFkS6Hy_TaCo_A_Benchmark_for_Lossless_and_Lossy_Codecs_o/figures/005_Table_2.jpg]]
*Table 2: Comparison of lossless compression performance (bits/Byte) on five tactile datasets. The best results are highlighted in bold blue, second-best in bold, and third to fifth in underline. For TaCo, 12M/48M/96M denotes the model parameter. To show the compression performance more clearly, we also list the compression ratios relative to the uncompressed data (8 bits/Byte) in parentheses only for the best and second best results*

### 无损压缩：数据驱动范式主导

**Table 2** 汇总了14种无损编解码器在五个异构触觉数据集上的压缩性能。TaCo-LL-96M在所有数据集上取得最优结果，bits/Byte范围为0.360–2.709，对应压缩比8×–22×。关键发现如下：

- **模型规模单调增益**：从12M到96M参数，TaCo-LL在TouchandGo上bits/Byte从0.542降至0.447（Table 2），验证了更大容量模型对触觉数据冗余的建模能力持续增强。
- **跨模态预训练失效**：基于自然图像/文本预训练的神经编解码器（DLPR、P2LLM、DualComp-I）在触觉数据上表现不佳。例如，DLPR在ObjTac上的bits/Byte为1.740，远高于TaCo-LL-96M的0.360。这揭示了**域偏移的严重性**——自然图像的统计先验无法迁移至触觉信号的纹理与形变模式。
- **通用工具的上限**：传统通用压缩器（gzip、zstd、bzip2）仅消除一维符号冗余，bits/Byte普遍高于1.0；图像格式（PNG、FLIF、JPEG-XL）虽能利用二维空间冗余，但在ObjectFolder数据集上JPEG-XL仍高达7.915 bits/Byte，几乎无压缩效果。

**Table 3** 揭示了数据驱动方法的代价：TaCo-LL-96M的编码速度（FPS）显著低于gzip等传统工具，在ObjTac上仅为0.0003 FPS（MacBook Pro CPU），需GPU加速才能达到实用水平。这是**计算复杂度与压缩效率的经典权衡**，部署时需根据机器人平台的算力预算进行取舍。

### 有损压缩：率失真性能全面领先

**Table 4** 以BD-Rate（Bjøntegaard Delta Rate）为指标，评估帧内有损编解码器性能。TaCo-L在四个数据集上取得最优BD-Rate：

![[assets/figures/papers/iclr26_0009_1PYXFkS6Hy_TaCo_A_Benchmark_for_Lossless_and_Lossy_Codecs_o/figures/007_Table_4.jpg]]
*Table 4: Evaluation of lossy compression performance on five tactile datasets leveraging intra-frame compressors. The best results are shown in blue bold, the second-best in bold, and the third-best in underline. For the reference, the bandwidth consumption of the anchor HEVC-intra is approximately 2Mbps at the quality of 40dB, which is calculated by 0.22 bit per pixel ×640 × 480 × 30fps×10−6 for Touch and Go dataset, as Fig. 4*

- TouchandGo: **-61.8%**（相对HM-Intra锚点）
- ObjectFolder: **-24.3%**
- SSVTP: **-19.2%**
- YCB-Slide: **-27.4%**

仅在ObjTac数据集上，VTM-SCC以-21.9%的BD-Rate略优于TaCo-L的-18.5%。**Figure 4** 的率失真曲线直观展示了TaCo-L在TouchandGo数据集上的优势：在所有码率点上，TaCo-L的PSNR均高于VTM-Intra、JPEG-XL和LALIC，且曲线斜率更陡，表明边际码率收益更高。

![[assets/figures/papers/iclr26_0009_1PYXFkS6Hy_TaCo_A_Benchmark_for_Lossless_and_Lossy_Codecs_o/figures/010_Figure_4.jpg]]
*Figure 4: Rate-distortion curves on TouchandGo dataset, when applying intra-frame compression methods*

**Table 5** 的复杂度对比显示，TaCo-L的63.2M参数量与LALIC相当，但编码FPS在GPU上可达0.03–0.08，仍远低于VTM-Intra等传统编解码器。这构成**实际部署的主要障碍**，尤其对于需要实时闭环控制的灵巧操作场景。

### 下游任务保真度：分类与抓取

压缩的终极检验在于下游任务性能的保留程度。**Table 6** 展示了有损压缩后的材料/物体分类精度：

![[assets/figures/papers/iclr26_0009_1PYXFkS6Hy_TaCo_A_Benchmark_for_Lossless_and_Lossy_Codecs_o/figures/011_Table_6.jpg]]
*Table 6: Material classification results on TouchandGo, ObjectFolder-1.0 and object classification results on YCB-Slide. Best results are in blue bold, the second-best results are in bold, and the third-best in underline*

- **TouchandGo分类**：TaCo-L在124×压缩比下，SVM准确率仅从76.63%降至75.12%（-1.51%），而JPEG-XL在相似压缩比下准确率跌幅更大。
- **YCB-Slide分类**：TaCo-L在190×压缩比下，SVM准确率保持98.01%，与未压缩数据的99.35%几乎持平（-1.34%）。这证明**触觉数据的任务关键信息高度可压缩**，数据驱动编解码器能够保留判别性特征。

**Table 7** 的灵巧抓取实验进一步验证了这一点。在0.025 BPP的极低码率下（约960×压缩），TaCo-L的平均抓取成功率（S_lift）为62.2%，仅比未压缩数据（24 BPP，63.8%）低1.6个百分点。相比之下，VTM-Intra在相近码率下成功率降至59.8%。值得注意的是，在易变形物体（deformable）子集上，TaCo-L的成功率损失更为显著（-3.4% vs 刚性物体的-0.5%），提示**形变交互的触觉信号对压缩失真更敏感**。

![[assets/figures/papers/iclr26_0009_1PYXFkS6Hy_TaCo_A_Benchmark_for_Lossless_and_Lossy_Codecs_o/figures/012_Table_7.jpg]]
*Table 7: Evaluation results on the dexterous grasping. Best results are shown in blue bold, the second-best results are denoted in bold, and the third-best in underline. We also list the accuracy loss relative to the uncompressed data (8 bits/Byte) in parentheses*

### 消融与失败模式

- **模型规模消融**（Table 2）：TaCo-LL从12M到96M的bits/Byte单调递减，但边际收益递减——48M到96M在TouchandGo上仅降低0.018 bits/Byte，表明进一步增大模型可能收益有限。
- **训练数据域限制**：当前训练集仅覆盖GelSight和DIGIT两种视觉触觉传感器，对其他传感器模态（如BioTac、电容式阵列）的泛化能力未经验证。这是**结论外推的主要风险点**。
- **计算瓶颈**：TaCo-L的63.2M参数和TaCo-LL的96M参数在嵌入式平台（如Jetson Orin）上的实时性存疑，Table 3/5的FPS数据均在A100 GPU上测得，需手动验证在边缘设备上的实际性能。

### 证据强度总结

| 核心主张 | 证据锚点 | 置信度 |
|---------|---------|--------|
| TaCo-LL-96M在5个数据集上无损压缩最优 | Table 2 | 高（0.98） |
| TaCo-L在4/5数据集上有损BD-Rate最优 | Table 4 | 高（0.99） |
| TaCo-L在124×压缩下分类精度损失<2% | Table 6 | 中高（0.95） |
| 灵巧抓取成功率在960×压缩下仅降1.6% | Table 7 | 中（0.95） |

**需手动验证的点**：TaCo-L在ObjTac数据集上BD-Rate未达最优（-18.5% vs VTM-SCC的-21.9%），论文未深入分析原因，可能与该数据集的力信号统计特性有关。此外，Table 7的抓取实验仅在仿真环境（IsaacSim）中进行，sim-to-real差距未量化。

## 方法谱系与知识库定位

### 在触觉数据压缩领域中的位置

TaCo 是首个系统性触觉数据编解码器基准测试，其核心贡献在于填补了“通用压缩算法直接迁移至异构触觉数据”与“专用触觉编解码器缺失”之间的鸿沟。在此之前，触觉数据的存储与传输主要依赖三类方法：通用无损压缩（gzip、zstd、bzip2）、图像/视频编解码器（PNG、JPEG-XL、HEVC/VVC）以及预训练的神经压缩模型（ELIC、DCVC-DC等）。这些方法均非为触觉信号设计，其根本缺陷在于无法捕获触觉数据的本征分布——视觉触觉图像的空间纹理统计与自然图像显著不同，力向量的时域演化模式也与视频帧间运动存在结构性差异。

TaCo-LL 和 TaCo-L 的方法学定位是**数据驱动的触觉专用编解码器**。其设计哲学并非发明全新的压缩架构，而是将触觉数据统一映射为二维图像格式后，复用成熟的图像/视频压缩框架，并通过在触觉数据集上的端到端训练使模型适配触觉信号的统计特性。这一策略的关键因果机制在于：预训练模型（如基于 ImageNet 训练的 LALIC）的潜在空间分布与触觉数据的分布存在系统性偏移，而全量触觉训练（purely-trained）能够消除这一偏移，使率失真优化目标直接对齐触觉信号的本征冗余结构。

### 与基线方法的谱系关系

**通用无损压缩器（gzip/zstd/bzip2）** 仅消除一维符号序列的统计冗余，无法利用触觉数据中固有的二维空间相关性和帧间时域冗余。Table 2 显示，gzip 在 ObjTac 上的 bits/Byte 高达 4.614，而 TaCo-LL-96M 仅需 0.360，压缩效率差距超过 12 倍。这一差距的根源在于通用压缩器将触觉帧视为无结构的字节流，完全忽略了像素间的空间邻接关系。

**图像无损编解码器（PNG/FLIF/JPEG-XL）** 虽能利用二维空间冗余，但其预测模型和熵编码上下文是为自然图像的光滑梯度与边缘统计设计的。视觉触觉图像（如 GelSight 的形变纹理）包含大量高频细节和重复模式，与自然图像的统计特性存在本质差异。Table 2 中 JPEG-XL 在 TouchandGo 上达到 1.199 bits/Byte，已显著优于 gzip 的 4.664，但仍比 TaCo-LL-96M 的 0.447 高出 2.7 倍，表明通用图像编解码器的先验假设在触觉域中效率不足。

**预训练神经压缩模型（ELIC/LALIC/TCM/DCVC系列）** 是 TaCo 最直接的方法学前驱。这些模型在自然图像/视频上预训练，具备强大的非线性变换和熵建模能力，但其潜在空间的先验分布与触觉数据不匹配。TaCo 的关键改动在于将训练数据域从 ImageNet 替换为触觉数据集（Touch and Go 和 ObjectFolder 的 70% 训练划分），使模型学习触觉信号特有的模态分布。Table 4 中，预训练 LALIC 在 TouchandGo 上的 BD-Rate 为 -37.1%，而全量触觉训练的 TaCo-L 达到 -61.8%，码率节省提升了 24.7 个百分点，直接验证了域内训练的关键作用。

**视频编解码器（VTM-SCC/VVenC/x265）** 在利用帧间冗余方面具有优势，但 TaCo 的评估表明，对于某些触觉数据集（如 ObjTac），屏幕内容编码（VTM-SCC）甚至优于数据驱动的 TaCo-L（Table 4 中 VTM-SCC 的 BD-Rate 为 -22.1%，TaCo-L 为 -9.8%）。这揭示了当前数据驱动方法的一个边界：当触觉数据的帧间模式与传统视频编码的块运动补偿假设高度吻合时，专用训练的优势可能被削弱。

### 适用边界与限制条件

**传感器类型的覆盖范围**是当前方法的首要边界。TaCo-LL 和 TaCo-L 的训练数据仅包含 GelSight 和 DIGIT 两种视觉触觉传感器，以及一种三轴力传感器。对于其他触觉模态（如基于磁场的触觉传感器、压阻阵列、电容式触觉皮肤），现有模型能否直接泛化尚未验证。这些传感器的信号统计特性（空间分辨率、动态范围、噪声模式）可能与训练分布存在显著差异，需要重新训练或架构调整。

**计算复杂度的部署约束**限制了 TaCo-L 在嵌入式机器人平台上的直接应用。Table 5 显示 TaCo-L 的参数量为 63.2M，编码速度在 A100 GPU 上仅为 0.7–1.3 FPS（ObjectFolder），远低于 JPEG-XL 在 CPU 上的 1.2–4.3 FPS。对于需要实时闭环控制的灵巧操作任务，这一延迟可能不可接受。模型压缩、知识蒸馏或专用硬件部署是实际应用的必要补充。

**码率-任务耦合的缺失**是当前框架的另一局限。TaCo-L 的率失真优化以 PSNR 作为失真度量，但下游任务（材料分类、灵巧抓取）对压缩伪影的敏感区域可能与 PSNR 的均匀加权假设不一致。Table 6 显示，在 124× 压缩比下，TouchandGo 的 SVM 分类准确率仅下降 1.51%，表明当前压缩策略在保留下游任务信息方面表现良好，但这一耦合是经验性的，缺乏自适应的码率控制机制来根据任务需求动态调整压缩参数。

### 开放问题与后续工作方向

**统一触觉编解码框架**的缺失是领域内的核心开放问题。当前 TaCo-LL 和 TaCo-L 需要为每种传感器类型进行独立训练，这限制了其在大规模多传感器机器人系统中的可扩展性。一个可能的突破方向是设计传感器无关的触觉表征学习框架，将异构触觉信号映射到共享的潜在空间，使单一编解码器能够处理多种传感器输出。这需要更大规模的多模态触觉数据集（如 FoTa）作为训练基础。

**触觉压缩与机器人策略的联合优化**可能带来超越独立压缩-推理流水线的性能增益。在极低带宽（如 0.01 BPP）下，Table 7 显示 TaCo-L 的灵巧抓取成功率（62.2%）与未压缩数据（63.8%）差距仅为 1.6%，但这一结果基于固定的压缩-解压-策略执行流水线。若将压缩的率失真目标与下游策略的任务奖励直接耦合，系统可能学会在保留任务关键信息的同时实现更高的压缩比，这对远程操作和触觉遥在场景具有重要价值。

**新一代触觉表征范式**的探索可能从根本上改变压缩方法的设计空间。当前 TaCo 依赖二维图像映射，但触觉信号本质上是对接触物理过程的采样。基于神经辐射场（NeRF）或隐式神经表示（INR）的方法可能直接对触觉信号的连续函数进行压缩，避免离散像素网格的冗余。这类方法在压缩比和重建质量上可能超越当前图像范式，但其计算复杂度和实时解码能力仍需实质性突破。

## 原文 PDF

![[paperPDFs/ICLR_2026/TaCo_A_Benchmark_for_Lossless_and_Lossy_Codecs_of_Heterogeneous_Tactile_Data.pdf]]
