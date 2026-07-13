---
title: "UniCompress: Token Compression for Unified Vision-Language Understanding and Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UniCompress_Token_Compression_for_Unified_Vision_Language_Understanding_and_Generation.pdf
project_link: null
code_link: null
aliases:
- UniCompress
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入少量可学习的全局元令牌捕捉场景级语义，并以此引导自回归解压缩器恢复密集令牌细节，从而在缩减令牌序列的同时保真生成质量。
primary_logic: 在现成的离散令牌化器周围插入轻量级压缩器与解压缩器，通过全局令牌提供结构约束，使得压缩后的紧凑视觉表示既能支持理解任务，又能通过自回归重建实现高质量生成，实现即插即用的统一高效建模。
claims:
- 在多种统一模型上，压缩后理解性能下降≤3个百分点，生成FID增加≤5点，视觉令牌减少4倍。
- 在UNITOK上，生成推理时间从32.25分钟降至18.96分钟，减少约41.2%。
- 全局令牌数量Ng=4在精度与效率间达到最佳平衡；去除全局令牌（Ng=0）使FID升至约21.4。
- 可学习全局元令牌相较于平均池化或CLS令牌，在生成质量（FID/CLIP）上具有一致且明显的优势。
---

# UniCompress: Token Compression for Unified Vision-Language Understanding and Generation

> [!tip] 核心洞察
> 在现成的离散令牌化器周围插入轻量级压缩器与解压缩器，通过全局令牌提供结构约束，使得压缩后的紧凑视觉表示既能支持理解任务，又能通过自回归重建实现高质量生成，实现即插即用的统一高效建模。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniCompress：面向统一视觉-语言理解与生成的令牌压缩 |
| 英文题名 | UniCompress: Token Compression for Unified Vision-Language Understanding and Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.11320) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | UNICOMPRESS |
| Dataset | GQA, MME Cognition, POPE, Image Generation |

> [!tip] 效果简介
> - GQA 上，Accuracy UNITOK-COMPRESSED 53.07 vs UNITOK 55.71 (-2.64)。
> - MME Cognition 上，Score BAGEL-COMPRESSED 274.50 vs BAGEL 277.80 (-3.30)。
> - POPE 上，Accuracy UNITOK-COMPRESSED 79.36 vs UNITOK 82.66 (-3.30)。

## 概要

### 问题背景

统一视觉-语言模型（Unified Vision-Language Models）在理解和生成任务上展现了巨大潜力，但其视觉令牌数量庞大——典型配置为 32×32=1024 个令牌——导致计算和内存开销极高。简单压缩策略（如朴素降采样或均匀剪枝）虽能缩减序列长度，却会严重损害图像生成质量，性能下降超过 15%，成为统一模型走向高效实用的核心瓶颈。

### 核心方案

UNICOMPRESS 提出了一种即插即用的令牌压缩框架，在现成的离散视觉令牌化器周围插入两个轻量级模块：**压缩器**与**全局引导的解压缩器**。其核心洞察在于：引入少量可学习的全局元令牌（Global Meta Tokens）捕捉场景级语义约束，配合平均池化压缩器将密集令牌网格缩减为紧凑序列；在生成阶段，自回归解压缩器以全局令牌和压缩令牌为条件，逐步恢复密集令牌的细节信息。这种设计使得压缩后的紧凑视觉表示既能支撑理解任务，又能通过自回归重建实现高质量生成，无需修改语言模型（LLM）本身。

### 方法定位

UNICOMPRESS 属于**视觉令牌压缩**方法，区别于以下两类工作：

- **令牌剪枝/选择类方法**：通过重要性评分丢弃部分令牌，但在生成任务中往往丢失关键细节。
- **统一模型架构改进**：如 UNITOK（Ma et al., arXiv 2025）、VILA-U（Wu et al., arXiv 2024）、BAGEL（Deng et al., arXiv 2025）等，直接设计新型令牌化器或训练范式，但未专门解决令牌冗余问题。

UNICOMPRESS 以插件形式适配多种统一模型，通过两阶段训练（先冻结 LLM 训练压缩令牌化器，再冻结令牌化器微调 LLM）实现高效集成。

### 主要结果

在多个统一模型（UNITOK、VILA-U、BAGEL 等）上的实验表明：

- **令牌缩减**：视觉令牌数量减少 4 倍（如 256→64）。
- **理解性能**：GQA 准确率下降 ≤3 个百分点，MME Cognition 等指标下降 ≤3.3 分。
- **生成性能**：FID 增加 ≤5 点（BAGEL-COMPRESSED 为 +4.49），CLIP 下降 ≤3.2 分。
- **推理效率**：在 UNITOK 上，生成推理时间从 32.25 分钟降至 18.96 分钟，减少约 41.2%；训练时间缩短 15.4%。

消融研究进一步揭示：全局元令牌数量 $N_g=4$ 在精度与效率间达到最佳平衡；去除全局令牌（$N_g=0$）使 FID 升至约 21.4，验证了全局语义约束对生成保真的关键作用。理解任务对令牌保留比例较为鲁棒，而生成质量随保留比例减小急剧下降，表明生成任务对令牌压缩更为敏感。



统一视觉-语言模型（Unified Vision-Language Models）旨在以单一架构同时处理视觉理解与图像生成任务，其核心范式是将图像离散化为令牌序列，交由自回归语言模型统一建模。然而，这一范式面临一个根本性的效率瓶颈：**视觉令牌数量庞大**。典型设置下，一张图像被编码为 32×32=1024 个离散令牌，远超过对应的文本令牌数量，导致 Transformer 的计算和内存开销呈平方级增长。简单压缩策略——如朴素降采样或均匀剪枝——虽能缩减序列长度，却会严重损害图像生成质量，性能下降可超过 15 个百分点。

现有统一模型在令牌效率方面存在明显缺口。**UNITOK**（Ma et al., arXiv 2025）、**VILA-U**（Wu et al., arXiv 2024）、**VARGPT**（Zhuang et al., arXiv 2025）等工作沿用密集令牌网格，未引入显式的压缩机制；**UNIFORK**（Li et al., arXiv 2025）和 **OPENUNI**（Wu et al., arXiv 2025）虽采用不同令牌化策略，但同样未解决令牌冗余问题。这些方法在理解与生成任务上取得了可观性能，却以高昂的计算代价为前提——例如 UNITOK 在生成推理时需耗时 32.25 分钟。

本文的动机源于一个关键观察：**视觉令牌中同时存在局部细节和全局语义两类信息，二者对理解和生成任务的贡献不同**。理解任务更依赖全局语义，对局部细节的丢失相对鲁棒；生成任务则要求精确恢复密集令牌，否则重建质量急剧恶化。这一不对称性暗示，压缩策略应当有选择地保留场景级约束，而非均匀丢弃信息。

基于此，本文提出 **UNICOMPRESS**，一种即插即用的令牌压缩算法。其核心思路是：在现成的离散令牌化器周围插入轻量级压缩器与解压缩器，引入少量可学习的**全局元令牌**捕捉场景级语义，并以此引导自回归解压缩器恢复密集令牌细节。压缩后的紧凑视觉表示既能支撑理解任务，又能通过自回归重建实现高质量生成，在将视觉令牌减少 4 倍的同时，将理解性能下降控制在 3 个百分点以内，生成 FID 增加不超过 5 点。



## 核心方法与创新机理

UNICOMPRESS 的核心创新并非提出一种全新的统一模型架构，而是在**现成的离散视觉令牌化器与语言模型之间插入一组轻量级模块**，以极小的性能代价实现视觉令牌的显著压缩。其设计围绕一个关键洞察展开：理解与生成任务对视觉信息的需求存在根本性不对称——理解任务仅需场景级语义，而生成任务则要求保留密集的局部细节。为此，UNICOMPRESS 在令牌化器周围引入了三个协同工作的模块，构成了一条“压缩-解压缩”管线。

### 全局元令牌：场景级语义的结构化约束

与朴素降采样或均匀剪枝直接丢弃信息不同，UNICOMPRESS 引入了一组**可学习的全局元令牌**（global meta tokens）来显式捕捉场景级语义。具体而言，系统维护少量可学习的元查询令牌 $\mathbf{Q}$，通过单向交叉注意力从原始图像令牌 $\mathbf{X}$ 中提取图像特定的全局令牌 $\mathbf{G}$：

$$\mathbf{G} = \mathrm{MHA}\bigl(\mathbf{Q} W_Q, \mathbf{X} W_K, \mathbf{X} W_V\bigr)$$

随后施加残差连接与层归一化：

$$\mathbf{G} \gets \mathrm{LN}(\mathbf{Q} + \mathbf{G})$$

这一设计的因果作用在于：全局令牌为后续的解压缩过程提供了**结构化的场景约束**，使得压缩后的紧凑表示不至于丢失生成所需的高层语义框架。消融实验（Figure 7）为此提供了决定性证据：当全局令牌数量 $N_g = 0$ 时，生成 FID 飙升至约 21.4，显著恶化；而 $N_g = 4$ 时达到精度-效率的最佳平衡点。此外，Figure 4 表明，相较于平均池化令牌或 CLS 令牌，可学习元令牌在生成质量（FID/CLIP）上具有一致且明显的优势，验证了“显式读取全局信息”这一机制的必要性。

### 池化压缩器：保留局部显著性

在局部令牌层面，UNICOMPRESS 采用**非重叠平均池化**将高分辨率令牌网格 $\mathbf{X}$ 压缩为低分辨率序列：

$$\hat{\mathbf{X}}^{\mathrm{cont}} = \mathrm{AvgPool}(\mathbf{X}, s), \quad \tilde{T} = T / s^2$$

默认设置 $s = 2$ 即可实现 4 倍令牌缩减（如 $32 \times 32 = 1024$ 降至 $16 \times 16 = 256$）。Table 4 的消融显示，平均池化相较于 TopK 等基于选择的压缩器，在理解与生成任务上均取得更优性能。其原理在于：池化操作对局部窗口内的信息进行了平滑聚合，保留了区域显著性，而选择类方法容易因离散决策引入不可逆的信息丢失。

### 自回归解压缩器：从紧凑表示恢复密集细节

这是 UNICOMPRESS 区别于现有压缩方法的关键模块。在生成阶段，一个轻量级的自回归 Transformer 解压缩器以全局令牌 $\hat{\mathbf{G}}$ 和压缩令牌 $\hat{\mathbf{X}}^{\mathrm{deq}}$ 为条件，逐步恢复密集令牌序列：

$$\mathbf{x}_t = f_{\mathrm{dec}}\big(\mathbf{X}_{<t}^{\mathrm{dense}}, \hat{\mathbf{X}}^{\mathrm{deq}}, \hat{\mathbf{G}}\big)$$

解压缩器的训练目标结合了回归损失与码本一致性损失：

$$\mathcal{L}_{\mathrm{recon}} = \mathcal{L}_{\mathrm{reg}} + \lambda_{\mathrm{cb}} \mathcal{L}_{\mathrm{cb}}$$

Figure 5 的可视化对比直观展示了该模块的作用：缺少全局令牌或使用朴素解压缩时，重建图像出现明显失真；而完整的 UNICOMPRESS 管线能够有效保留视觉信息。这一设计使得语言模型在生成时只需输出紧凑域的目标，由解压缩器负责恢复像素级细节，从而大幅降低了 LLM 的序列长度负担。

### 两阶段训练：解耦压缩与语言建模

UNICOMPRESS 采用两阶段训练策略：第一阶段冻结 LLM，训练压缩令牌化器（含全局提取器、压缩器和解压缩器）；第二阶段冻结令牌化器，微调 LLM 以适应紧凑视觉序列。这种解耦设计确保压缩模块的优化不干扰语言模型的预训练知识，同时使 LLM 能够平滑迁移至压缩域。需要注意的是，该方法依赖对令牌化器的修改，无法直接用于完全冻结的预训练统一模型，这是一个需要手动验证的适用性边界。

### 创新总结

综上，UNICOMPRESS 相对于基线统一模型（如 **UNITOK** (Ma et al., arXiv 2025)、**VILA-U** (Wu et al., arXiv 2024)、**BAGEL** (Deng et al., arXiv 2025) 等）的核心 changed slots 可归纳为：将密集令牌网格替换为“压缩令牌 + 全局元令牌”的紧凑表示；以可学习元查询令牌的交叉注意力替代隐式全局建模；引入自回归解压缩器桥接压缩域与密集生成域；并通过两阶段训练实现压缩模块与 LLM 的解耦优化。这些创新共同实现了“即插即用”的统一高效建模：在多种统一模型上，压缩后理解性能下降 ≤ 3 个百分点，生成 FID 增加 ≤ 5 点，视觉令牌减少 4 倍（Table 1, Table 2），生成推理时间最高降低 41.2%（Table 3）。



UNICOMPRESS 采用即插即用的设计范式，在不修改语言模型（LLM）本身的前提下，围绕现成的离散视觉令牌化器插入三个轻量级模块：**全局令牌提取器**、**令牌压缩器**和**自回归解压缩器**（Figure 2）。其核心思想是将密集的 H×W 令牌网格转化为一个紧凑的视觉序列，同时保留理解任务所需的语义信息和生成任务所需的细节重建能力。

![[assets/figures/papers/paper_list_l2228_https_arxiv_org_abs_2603_11320/figures/002_Figure_2.jpg]]
*Figure 2: Overview of UNICOMPRESS. The tokenizer is augmented with three modules: a global token extractor, a token compressor, and an autoregressive decompressor. The language model consumes a compact visual sequence for understanding and produces compresseddomain targets for generation*

### 数据流与模块协作

整个管道的数据流分为编码（压缩）和解码（解压缩）两条路径，分别服务于理解和生成任务：

1. **编码阶段**：视觉编码器输出的密集令牌图 $\mathbf{X} \in \mathbb{R}^{T \times d}$ 同时流入两个并行分支。**全局令牌提取器**通过一组可学习的元查询令牌 $\mathbf{Q}$，以单向交叉注意力机制从 $\mathbf{X}$ 中提取场景级全局语义令牌 $\mathbf{G}$（公式 1）；**令牌压缩器**则通过非重叠平均池化将 $\mathbf{X}$ 的空间分辨率按因子 $s$ 缩减，生成压缩后的局部令牌 $\hat{\mathbf{X}}^{\text{cont}}$（公式 3）。最终，LLM 接收拼接后的紧凑序列 $\{\mathbf{G}, \hat{\mathbf{X}}^{\text{cont}}\}$ 执行理解任务。

2. **解码阶段**：对于生成任务，LLM 在压缩域输出离散令牌索引。**自回归解压缩器**以全局令牌 $\hat{\mathbf{G}}$ 和压缩令牌 $\hat{\mathbf{X}}^{\text{deq}}$ 为条件，逐步预测完整的密集令牌序列（公式 7），再通过离散码本映射回图像空间。

### 关键设计决策

- **全局令牌的角色**：全局元令牌充当场景级结构约束，为解压缩器提供缺失的全局上下文。消融实验表明，去除全局令牌（$N_g = 0$）会导致生成 FID 从约 16.3 急剧恶化至约 21.4（Figure 7），证实了其在重建保真度中的关键作用。

- **压缩器的选择**：采用平均池化而非基于选择的压缩方法（如 TopK），因为池化保留了空间连续性，为解压缩器提供了更规整的局部证据网格。Table 4 显示，池化策略在理解和生成两项任务上均优于选择类方法。

- **两阶段训练**：第一阶段冻结 LLM，仅训练令牌化器的压缩-解压缩管道（重建损失 $\mathcal{L}_{\text{recon}}$ 结合回归损失与码本一致性损失，公式 8）；第二阶段冻结令牌化器，微调 LLM 以适应紧凑视觉表示。这种解耦训练确保了压缩质量与 LLM 适配的独立性。

### 效率与性能的权衡

以默认配置 $s=2, N_g=4$ 为例，视觉令牌数量减少 4 倍（如 256→64）。在理解任务上，GQA 准确率仅下降约 2.6 个百分点（UNITOK-COMPRESSED: 53.07 vs. UNITOK: 55.71, Table 1）；在生成任务上，FID 增加控制在 5 点以内（BAGEL-COMPRESSED: 17.22 vs. BAGEL: 12.73, Table 2），同时生成推理时间减少约 41.2%（UNITOK: 32.25 分钟 → 18.96 分钟, Table 3）。这一框架的即插即用特性使其可适配多种统一模型架构（UNITOK、VILA-U、BAGEL 等），无需修改 LLM 接口。



UNICOMPRESS 在现成的离散视觉令牌化器周围插入三个轻量级模块，而不改变语言模型（LLM）的内部结构：**全局令牌提取器**、**令牌压缩器**和**自回归解压缩器**。整个管道将密集的 $H \times W$ 令牌网格转化为紧凑的视觉表示，供 LLM 在理解和生成任务中统一使用。

### 全局令牌提取器

该模块引入一小批可学习的元查询令牌 $\mathbf{Q} \in \mathbb{R}^{N_g \times d}$，通过单向交叉注意力从图像令牌 $\mathbf{X} \in \mathbb{R}^{T \times d}$ 中提取场景级全局语义：

$$\mathbf{G} = \mathrm{MHA}\bigl(\mathbf{Q} W_Q, \mathbf{X} W_K, \mathbf{X} W_V\bigr) \tag{1}$$

其中 $W_Q$、$W_K$、$W_V$ 为可学习的投影矩阵，$\mathrm{MHA}$ 表示多头注意力。随后对全局令牌施加残差连接与层归一化：

$$\mathbf{G} \gets \mathrm{LN}(\mathbf{Q} + \mathbf{G}) \tag{2}$$

这种设计的核心直觉在于：压缩后的局部令牌携带显著的空间细节，而全局元令牌提供场景级结构约束，二者互补以保真重建。

### 令牌压缩器

局部令牌压缩采用非重叠平均池化，以步长 $s$ 对 $H \times W$ 网格进行空间降采样：

$$\hat{\mathbf{X}}^{\mathrm{cont}} = \mathrm{AvgPool}(\mathbf{X}, s), \quad \tilde{T} = T / s^2 \tag{3}$$

压缩后的连续令牌 $\hat{\mathbf{X}}^{\mathrm{cont}}$ 随后通过离散码本量化为索引序列 $\hat{\mathbf{X}}^{\mathrm{deq}}$，用于生成任务的重建目标。默认配置 $s=2$ 将令牌数减少至原始的 $1/4$。

### 自回归解压缩器

在生成阶段，LLM 输出压缩域中的离散令牌索引。自回归解压缩器以全局令牌 $\hat{\mathbf{G}}$ 和压缩令牌 $\hat{\mathbf{X}}^{\mathrm{deq}}$ 为条件，逐步恢复密集令牌序列：

$$\mathbf{x}_t = f_{\mathrm{dec}}\bigl(\mathbf{X}_{<t}^{\mathrm{dense}}, \hat{\mathbf{X}}^{\mathrm{deq}}, \hat{\mathbf{G}}\bigr) \tag{7}$$

其中 $\mathbf{X}_{<t}^{\mathrm{dense}}$ 表示已生成的前 $t-1$ 个密集令牌。解压缩器的训练目标结合回归损失与码本一致性损失：

$$\mathcal{L}_{\mathrm{recon}} = \mathcal{L}_{\mathrm{reg}} + \lambda_{\mathrm{cb}} \mathcal{L}_{\mathrm{cb}} \tag{8}$$

$\mathcal{L}_{\mathrm{reg}}$ 约束连续特征重建精度，$\mathcal{L}_{\mathrm{cb}}$ 确保量化后的离散索引与原始码本分布一致。

### 管道集成

最终，LLM 接收紧凑的视觉序列 $\{\mathbf{G}, \hat{\mathbf{X}}^{\mathrm{cont}}\}$ 执行理解任务，或自回归生成压缩域目标索引，再由解压缩器恢复为密集令牌完成图像生成。整个设计保持 LLM 接口不变，实现了即插即用的统一高效建模。

### 补充图表

![[assets/figures/papers/paper_list_l2228_https_arxiv_org_abs_2603_11320/figures/007_Figure_4.jpg]]
*Figure 4: Ablation on global token type. Results use*

![[assets/figures/papers/paper_list_l2228_https_arxiv_org_abs_2603_11320/figures/009_Figure_5.jpg]]
*Figure 5: UNICOMPRESS preserves the most visual information under compression by using global meta tokens and autoregressive decompressor*

![[assets/figures/papers/paper_list_l2228_https_arxiv_org_abs_2603_11320/figures/012_Figure_7.jpg]]
*Figure 7: Effect of the number of global tokens*



## 实验与关键发现

### 核心瓶颈与评估逻辑

统一视觉-语言模型将图像离散化为令牌网格后送入大语言模型（LLM），但密集的 $H \times W$ 令牌（如 $32 \times 32 = 1024$ 个）导致自注意力计算量随序列长度平方增长，训练与推理开销极高。简单压缩策略（朴素降采样或均匀剪枝）会严重损害图像生成质量——分析指出性能下降超过15%。因此，实验评估的核心逻辑围绕一个关键权衡展开：**在将视觉令牌减少4倍的条件下，理解与生成性能能否同时保持在可接受范围内**。

实验在多个现成的统一模型上插入 UNICOMPRESS，保持 LLM 接口不变，从理解基准、生成质量、推理效率三个维度验证方法有效性，并通过消融实验揭示各模块的因果贡献。

---

### 理解任务：轻量退化，部分指标接近无损

Table 1 汇总了在 GQA、MME Cognition、POPE、Seed-bench 等视觉理解基准上的对比结果。以 UNITOK（Ma et al., arXiv 2025）为骨干时，压缩版本在 GQA 上仅从 55.71 降至 53.07（-2.64），POPE 从 82.66 降至 79.36（-3.30）。在 BAGEL（Deng et al., arXiv 2025）上，MME Cognition 得分从 277.80 降至 274.50（-3.30）。这些退化幅度均控制在 3 个百分点以内，表明**压缩后的紧凑视觉表示仍保留了理解所需的关键语义信息**。

![[assets/figures/papers/paper_list_l2228_https_arxiv_org_abs_2603_11320/figures/003_Table_1.jpg]]
*Table 1: Unified model performance on visual understanding benchmarks (higher is better). XXX-COMPRESSED denotes the same backbone with our plug-in token compression*

值得注意的是，OPENUNI（Wu et al., arXiv 2025）的 Seed-bench 得分仅从 48.39 微降至 47.51，几乎无损。这暗示当基础模型本身对视觉令牌冗余度较高时，压缩带来的影响更小。定性示例（Figure 3）进一步显示，基于压缩令牌生成的图像描述与密集令牌版本在语义一致性上高度吻合。

![[assets/figures/papers/paper_list_l2228_https_arxiv_org_abs_2603_11320/figures/006_Figure_3.jpg]]
*Figure 3: Understanding task examples: generating the texts that describe the image*

---

### 生成任务：FID 增幅可控，但存在模型间差异

Table 2 报告了在 MJHQ-30K 上的图像生成质量。UNITOK-COMPRESSED 的 FID 为 16.33，与原始 UNITOK 的 16.14 几乎持平（+0.19），CLIP 得分也仅从 31.0 微降至 30.7。这表明**在 UNITOK 框架下，全局令牌引导的自回归解压缩器能够有效恢复生成所需的密集细节**。

![[assets/figures/papers/paper_list_l2228_https_arxiv_org_abs_2603_11320/figures/004_Table_2.jpg]]
*Table 2: Performance of the original and compressed unified models on image generation benchmarks. XXX-COMPRESSED inserts UNICOMPRESS without changing the LM interface. Lower FID and higher CLIP indicate better quality*

然而，BAGEL-COMPRESSED 的 FID 从 12.73 升至 17.22（+4.49），CLIP 从 32.0 降至 28.8（-3.2），退化幅度明显大于 UNITOK。这一差异揭示了一个重要边界条件：**UNICOMPRESS 的生成保真度与基础模型的令牌化器特性密切相关**。BAGEL 结合了扩散模型，其原始令牌分布可能对压缩引入的量化误差更敏感。该点需在推广至其他扩散类统一模型时手动验证。

---

### 效率收益：推理时间减少超40%

Table 3 对比了挂钟时间。在生成任务上，UNITOK-COMPRESSED 的推理时间从 32.25 分钟降至 18.96 分钟，减少约 **41.2%**；训练时间从 27.02 分钟降至 23.18 分钟，减少约 14.2%。理解任务同样受益：GQA 推理时间减少约 15.4%。效率提升直接源于令牌序列长度缩减——压缩因子 $s=2$ 将令牌数从 $T$ 降至 $T/4$，LLM 的自注意力计算量显著下降。

![[assets/figures/papers/paper_list_l2228_https_arxiv_org_abs_2603_11320/figures/005_Table_3.jpg]]
*Table 3: Wall-clock time with/without plug-in token compression. Understanding: ShareGPT4V PT (train), GQA (inference). Generation: JDB (train), MJHQ-30K (inference). Lower is better. Although the model is trained on the two datasets jointly in other experiments, the training times in this table were measured by training on each dataset separately*

---

### 消融实验：全局令牌与池化策略的因果证据

**全局令牌类型**（Figure 4）：对比了平均池化令牌、CLS 令牌和可学习元令牌三种全局上下文提取方式。在理解任务上三者性能相当，但在生成任务上，可学习元令牌在 FID 和 CLIP 上均一致且明显优于其他两种方案。这验证了核心设计直觉：**通过交叉注意力主动“读取”全图并写入图像特定语义的元令牌，为解压缩器提供了更强的结构约束**。

**全局令牌数量**（Figure 7）：$N_g=4$ 在精度与效率间达到最佳平衡。当 $N_g=0$（完全移除全局令牌）时，FID 升至约 21.4，生成质量显著恶化。这直接证明了全局令牌是解压缩器重建密集细节的**必要因果组件**，而非冗余附加。

**本地令牌压缩方式**（Table 4）：在相同令牌预算（4倍压缩）下，平均池化在理解和生成任务上均优于 TopK 等基于选择的压缩方法。池化保留了空间邻域的平均信息，而选择类方法丢弃了被剪枝位置的全部细节，导致解压缩器缺乏足够的局部证据。

**令牌保留比例**（Figure 6）：理解任务对保留比例较为鲁棒——即使保留 1/16 的令牌，GQA 仍接近 49。但生成任务的 CLIP 随保留比例减小急剧下降。这揭示了两类任务对视觉信息粒度的根本差异：**理解仅需高层语义，而生成依赖细粒度空间细节**。

---

### 失败模式与局限

1. **极低保留率下的生成衰退**：当压缩因子过大（如 $s=4$，保留 1/16 令牌）时，生成 CLIP 急剧下降，自回归解压缩器难以从严重退化的压缩表示中恢复可信纹理。
2. **模型依赖性**：BAGEL 等结合扩散模型的统一框架上 FID 退化（+4.49）明显大于纯自回归框架（UNITOK +0.19），方法的即插即用普适性在扩散类模型上需要额外验证。
3. **两阶段训练约束**：方法需对令牌化器进行修改并执行两阶段训练（先冻结 LLM 训练压缩令牌化器，再冻结令牌化器微调 LLM），无法直接应用于完全冻结的预训练统一模型。
4. **超参数敏感性**：全局令牌数量 $N_g$ 需根据具体模型和数据集调节，当前结论基于 1B 参数 LLM 和小规模数据集（JDB、ShareGPT4V），向更大规模模型的推广性待验证。

### 补充图表

![[assets/figures/papers/paper_list_l2228_https_arxiv_org_abs_2603_11320/figures/008_Table_4.jpg]]
*Table 4: Ablation on local token compression (pooling/selection). All rows target the same token budget $(\times 4$.0 ) as our default setting with s=2 . Results use*

![[assets/figures/papers/paper_list_l2228_https_arxiv_org_abs_2603_11320/figures/010_Figure_6.jpg]]
*Figure 6: Effect of token keep ratio on accuracy. GQA (understanding) vs. MJHQ-30K CLIP (generation)*



## 定位与知识库关联

### 统一视觉-语言模型中的令牌效率瓶颈

UNICOMPRESS 直接回应了统一视觉-语言模型中一个日益突出的结构性矛盾：离散视觉令牌化器在赋能统一自回归建模的同时，产生了数量庞大的视觉令牌序列。以典型的 32×32 网格为例，单张图像即产生 1024 个令牌，使得基于 Transformer 的语言模型在训练和推理阶段承受显著的计算与内存压力。现有的应对策略大致分为两条路径：一是设计更紧凑的令牌化器本身，如降低网格分辨率或采用语义级压缩，但这通常以牺牲生成质量为代价；二是在语言模型输入端进行令牌剪枝或选择，然而简单降采样或均匀剪枝会严重损害图像生成质量——文中指出性能下降可超过 15%。

UNICOMPRESS 的方法学定位在于：它不改变底层令牌化器的离散码本结构，也不修改语言模型的接口与参数，而是在令牌化器周围插入轻量级的压缩-解压缩模块，形成一个即插即用的中间层。这一设计哲学与 **UNITOK**（Ma et al., arXiv 2025）、**VILA-U**（Wu et al., arXiv 2024）、**VARGPT**（Zhuang et al., arXiv 2025）等统一模型形成互补关系——这些工作聚焦于统一架构本身的设计，而 UNICOMPRESS 则作为通用加速层叠加于其上。同时，它也区别于 **UNIFORK**（Li et al., arXiv 2025）通过替换令牌化器来提升效率的思路，以及 **OPENUNI**（Wu et al., arXiv 2025）和 **BAGEL**（Deng et al., arXiv 2025）结合扩散模型实现生成的方案——后者的生成管道天然避开了离散令牌的自回归解码开销，但牺牲了统一自回归建模的简洁性。

### 核心机制的知识贡献

从知识库定位来看，UNICOMPRESS 的核心贡献在于揭示了“全局语义约束”在令牌压缩-重建过程中的关键作用。具体而言，该方法引入一组可学习的全局元令牌（默认数量 $N_g=4$），通过单向交叉注意力从完整图像令牌中提取场景级语义信息：

$$\mathbf{G} = \mathrm{MHA}\bigl(\mathbf{Q} W_Q, \mathbf{X} W_K, \mathbf{X} W_V\bigr)$$

随后对局部令牌进行非重叠平均池化压缩：

$$\hat{\mathbf{X}}^{\mathrm{cont}} = \mathrm{AvgPool}(\mathbf{X}, s), \quad \tilde{T} = T / s^2$$

在生成阶段，一个自回归解压缩器以全局令牌和压缩令牌为条件，逐步恢复密集令牌序列：

$$\mathbf{x}_t = f_{\mathrm{dec}}\big(\mathbf{X}_{<t}^{\mathrm{dense}}, \hat{\mathbf{X}}^{\mathrm{deq}}, \hat{\mathbf{G}}\big)$$

这一设计的因果机制在于：压缩令牌携带局部显著证据，而全局元令牌提供结构约束，二者协同使得紧凑表示既能支撑理解任务中的语义检索，又能通过自回归重建保真生成质量。消融实验为此提供了有力证据：当全局令牌数量 $N_g=0$ 时，生成 FID 升至约 21.4，显著恶化；可学习元令牌在生成质量（FID/CLIP）上一致且明显地优于平均池化令牌或 CLS 令牌（Figure 4）；平均池化压缩器相较于 TopK 等基于选择的压缩器，在理解和生成任务上均取得更优性能（Table 4）。

### 适用边界与局限

尽管 UNICOMPRESS 在多个统一模型上展现出良好的即插即用特性，其适用边界同样清晰。第一，方法依赖对令牌化器进行修改并采用两阶段训练（第一阶段冻结 LLM 训练压缩令牌化器，第二阶段冻结令牌化器微调 LLM），这意味着它无法直接应用于完全冻结的预训练统一模型，对部署灵活性构成约束。第二，在极低令牌保留率（如 1/16）下，生成质量的衰退仍然显著——Figure 6 显示，虽然理解任务对令牌保留比例较为鲁棒（保留 1/16 时 GQA 仍接近 49），但生成任务的 CLIP 随保留比例减小急剧下降，表明压缩-重建管道在极端压缩比下仍存在信息瓶颈。第三，全局令牌数量 $N_g$ 需要根据具体模型和数据集调节，当前最优值 $N_g=4$ 的普适性尚待跨任务验证。第四，现有实验主要基于较小规模数据集（JDB、ShareGPT4V）和 1B 参数 LLM（Llama-3.2-1B），向更大规模模型的推广性有待进一步检验。

### 开放问题与未来方向

从知识库演进的视角，UNICOMPRESS 开启了若干值得追踪的研究方向。其一，该方法能否泛化至视频等序列模态的统一模型，是检验其机制通用性的关键试金石——视频的时序冗余可能为压缩提供额外杠杆，但自回归解压缩的时序依赖也将面临更严峻的计算挑战。其二，压缩后的令牌表示是否适用于检索或可控生成等更广泛的下游任务，决定了该方法在统一模型生态中的实际渗透力。其三，是否存在更高效的全局上下文提取机制（如线性注意力）以进一步降低计算成本，是方法本身持续优化的空间。其四，在高度结构化图像（如文本、图表）上，压缩重建是否会引入额外的失真，这一问题在当前实验中尚未得到系统回答，但对文档理解等实际应用场景至关重要。



## 原文 PDF

![[paperPDFs/CVPR_2026/UniCompress_Token_Compression_for_Unified_Vision_Language_Understanding_and_Generation.pdf]]
