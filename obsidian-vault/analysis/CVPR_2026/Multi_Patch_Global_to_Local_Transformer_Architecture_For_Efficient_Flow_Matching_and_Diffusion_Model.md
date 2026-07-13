---
title: Multi-Patch Global-to-Local Transformer Architecture For Efficient Flow Matching and Diffusion Model
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Multi_Patch_Global_to_Local_Transformer_Architecture_For_Efficient_Flow_Matching_and_Diffusion_Model.pdf
project_link: null
code_link: null
aliases:
- MP
- MPGLTAEFMDM
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: Multi-Patch
primary_logic: Multi-Patch
claims:
- Multi-Patch
---

# Multi-Patch Global-to-Local Transformer Architecture For Efficient Flow Matching and Diffusion Model

> [!tip] 核心洞察
> Multi-Patch

| 字段 | 内容 |
|------|------|
| 中文题名 | Multi-Patch Global-to-Local Transformer Architecture For Efficient Flow Matching and Diffusion Model |
| 英文题名 | Multi-Patch Global-to-Local Transformer Architecture For Efficient Flow Matching and Diffusion Model |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.26357) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method |  |
| Dataset | ImageNet |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

本文提出 **MPDiT (Multi-Patch Diffusion Transformer)**，一种面向图像生成的分层扩散 Transformer 架构，旨在解决标准 DiT 中高分辨率生成的计算瓶颈。核心思路是采用**从全局到局部（Global-to-Local）的多尺度 patch 策略**：早期 Transformer 块使用大 patch（如 p=4）捕捉全局上下文，后期通过上采样模块扩展为小 patch（p=2）细化局部细节，从而在不牺牲生成质量的前提下显著降低计算量。

方法层面，MPDiT 在 DiT 基础上改动了三个关键模块：(1) **多尺度 patch 嵌入与上采样模块**，通过线性投影加 pixel-unshuffle 实现 token 序列的粗到细扩展；(2) **FNO（Fourier Neural Operator）时间嵌入**，替代传统正弦时间嵌入以提供更平滑的时序表示；(3) **多 token 类别嵌入**与共享 AdaIN 调制。该架构属于扩散 Transformer 的**高效推理**改进路线，与 MDT、MaskDiT 等掩码扩散方法互补。

在 ImageNet 256×256 上，MPDiT-XL 以 59.3 GFLOPs 达到 FID 2.05，计算量仅为 DiT/SiT 的约 8.8%；在 ImageNet 512×512 上，以 228.4 GFLOPs 达到 FID 2.47，计算量约为 DiT/SiT 的 8.7%。消融实验表明，多 patch 设计可降低最多 50% 的 GFLOPs，FNO 时间嵌入带来约 4 个点的 FID 提升。

扩散模型已在图像生成领域取得显著进展，其中基于 Transformer 的扩散主干网络（如 DiT）凭借可扩展性和灵活性展现出强大潜力。然而，现有 DiT 架构在计算效率与生成质量之间仍存在明显张力。

**核心瓶颈**在于传统的单尺度补丁（patch）标记化策略。DiT 将输入图像统一划分为固定大小的补丁，所有 Transformer 块在相同分辨率的标记序列上操作。这种设计迫使模型在全部深度上以相同粒度处理视觉信息，导致两个相互矛盾的问题：较大的补丁虽然计算高效，但丢失了精细的局部纹理；较小的补丁能保留细节，却使自注意力的计算复杂度随序列长度平方增长，显著增加了计算开销。

**因果机制**上，这一瓶颈源于视觉信息的多尺度特性与模型架构的单尺度处理之间的矛盾。自然图像包含从全局语义到局部纹理的层次化结构，高效的表征应当在早期阶段捕获粗粒度的全局上下文，在后期阶段逐步细化局部细节。然而，传统 DiT 无法在推理过程中动态调整表征粒度，只能在训练前固定补丁大小，从而在效率与质量之间做出折中。

此外，现有方法在时间嵌入和条件注入方面也存在改进空间。传统 DiT 使用简单的线性层处理正弦时间特征，难以充分捕捉扩散过程中时间步之间的平滑过渡关系；条件信息（如类别标签）的注入方式也较为单一，限制了模型对条件信号的利用效率。

**本文动机**正是针对上述缺口，提出一种从粗到细的层次化 Transformer 架构，使模型能够在早期块中使用大补丁高效捕获全局上下文，在后期块中通过上采样模块将大补丁标记扩展为更多的小补丁标记以细化局部细节。同时，引入基于傅里叶神经算子（FNO）的时间嵌入模块，以更平滑地建模时间步之间的过渡关系。这一设计在保持生成质量的同时，显著降低了计算成本。

## 核心方法与创新机理

MPDiT 的核心创新在于将传统 DiT 的**各向同性全分辨率架构**重构为**全局到局部的层次化多尺度架构**，并通过三个关键模块的协同设计，在显著降低计算开销的同时保持甚至提升生成质量。

### 1. 全局-局部多尺度 Transformer 架构

传统 DiT 在所有 Transformer 块中均使用统一的小 patch（$p=2$）对图像进行 token 化，导致自注意力计算的全序列长度始终为 $256$（对 $32\times 32$ latent）。MPDiT 的核心洞察是：**早期层仅需捕获粗粒度的全局上下文，精细的局部细节可由后期层负责**。

具体而言，MPDiT 将 $N$ 个 Transformer 块分为两个阶段：
- **早期阶段**（前 $N-k$ 块）：采用更大的 patch size（$p=4$），将 token 序列长度从 $256$ 降至 $64$，大幅降低自注意力的计算复杂度。
- **后期阶段**（后 $k$ 块）：通过一个 **Upsample Block** 将大 patch token 上采样为 $256$ 个小 patch token（$p=2$），恢复空间分辨率以进行局部细节的精细化建模。

这一设计直接改变了 DiT 的 **patch embedding 模块**和**序列长度**两个关键 slot，在架构层面实现了计算量与建模能力的解耦。

### 2. Upsample Block：从粗到细的 token 扩展

Upsample Block 是实现两阶段衔接的关键组件。其操作流程为：
1. 将输入的 token 序列分离为 class token 和图像 token；
2. 对图像 token 进行线性投影，扩展通道维度；
3. 应用 **pixel-unshuffle** 操作，将空间压缩的通道信息重新映射为更多的空间 token，从而将序列长度从 $64$ 恢复至 $256$。

这一设计避免了简单插值带来的信息损失，通过可学习的投影实现从粗粒度表示到细粒度表示的有效过渡。

### 3. FNO 时间嵌入

传统 DiT 使用两个线性层对正弦时间特征进行处理，作者指出这种线性嵌入难以捕获时间步之间的平滑过渡。MPDiT 将其替换为**基于 Fourier Neural Operator（FNO）的时间嵌入模块**，由多个 MixedFNO 块组成，能够提供更丰富的时间表示。消融实验表明，仅此一项改进即可带来约 **4 个点的 FID 提升**。

### 4. 多 token 类别嵌入与共享 AdaIN

MPDiT 还引入了两个辅助创新：
- **多 token 类别嵌入**：将传统的单一类别向量扩展为 $m$ 个可学习的类别 token（$m=4$），使条件信息能够更充分地与图像 token 交互。
- **共享 AdaIN**：将 DiT 中每个 Transformer 块独立的 AdaIN 调制替换为全局共享的 AdaIN，作用于合并后的时间与类别嵌入。这一改动减少了约 **30% 的参数量**（从 130M 降至 90M），同时通过消融实验证实对性能无负面影响。

### 创新点总结

| 创新模块 | 改变的 Slot | 作用机制 | 证据强度 |
|---------|------------|---------|---------|
| 多尺度 patch 架构 | patch size、序列长度 | 早期大 patch 降计算，后期小 patch 保精度 | 强（Table 1-4） |
| Upsample Block | token 扩展方式 | 线性投影 + pixel-unshuffle 实现粗-细转换 | 强（Table 7） |
| FNO 时间嵌入 | 时间编码模块 | Fourier 算子捕获平滑时间表示 | 强（Table 5，~4 FID 提升） |
| 多 token 类别嵌入 | 条件注入方式 | $m$ 个 token 增强条件交互 | 强（Table 3/6，~7 FID 提升） |
| 共享 AdaIN | 调制机制 | 全局共享替代逐块 AdaIN，减参 30% | 强（Table 3） |

整体而言，MPDiT 通过**层次化多尺度架构**这一主线创新，配合 FNO 时间嵌入、多 token 条件注入等辅助改进，在 ImageNet 256×256 上以 **50% 的 GFLOPs 削减**实现了 **cfg FID 2.05** 的优异性能，验证了“全局-局部”解耦设计的有效性。

MPDiT 的整体架构遵循一种**由粗到细的全局-局部处理范式**，其核心思想是将标准各向同性 DiT 的单一分辨率 patch 序列替换为两级层次化 token 流。整个 pipeline 由三个主要功能阶段串联而成：**大 patch 嵌入与全局编码**、**上采样模块**、以及**小 patch 精细解码**。

具体而言，输入潜变量图像首先通过一个**大 patch 嵌入模块**被切分为较大的 patch（例如 $p=4$ 而非标准的 $p=2$），从而大幅减少输入 token 数量。这些大 patch token 经过前 $(N-k)$ 个 DiT 块，在低分辨率空间高效捕获全局上下文和粗粒度结构信息。

此后，token 流进入**上采样模块**。该模块首先将图像 token 与类别 token 分离，对图像 token 执行线性投影后接 **pixel-unshuffle** 操作，将序列长度从 64 token 扩展至 256 token，实现从大 patch 表示到小 patch 表示的空间分辨率提升。上采样后的 token 与类别 token 重新拼接，送入最后 $k$ 个 DiT 块，在完整分辨率下对局部细节进行精细建模。

在时间条件注入方面，MPDiT 用 **FNO 时间嵌入**取代了传统的线性时间嵌入，以更平滑地捕捉时间步之间的过渡。时间嵌入与类别嵌入合并后，通过**共享 AdaIN** 机制统一注入所有 DiT 块，而非为每个块单独设置 AdaIN 层——这一设计使参数量减少约 30%。

整个架构的信息流可概括为：**输入潜变量 → 大 patch 嵌入 → (N-k) 个全局 DiT 块 → 上采样模块 → k 个局部 DiT 块 → 输出预测速度**。这种全局-局部的层次化设计使得模型在保持生成质量的同时，将计算量（GFLOPs）降低了最多 50%。

![[assets/figures/papers/paper_list_l900_https_arxiv_org_abs_2603_26357/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of MPDiT, which consists of (a) the Global-Local MultiPatch Diffusion Transformer, (b) DiT Block with shared time embedding, (c) The Upsample Module and (d) The FNO Time Embedding*

### 3.1 训练框架：流匹配目标

MPDiT 基于修正流（Rectified Flow）框架进行训练。其核心训练目标为流匹配损失（Flow Matching Loss），定义为预测速度与目标速度之间的 L2 距离：

$$L_{FM} = \sum_{z, t, n, \epsilon} || f_{\theta}(z_t, t, c) - (n - z)||_2^2$$

其中，$z_t$ 为当前时间步 $t$ 的噪声潜在表示，$n$ 为噪声，$z$ 为干净潜在表示，$c$ 为条件信息（如类别标签），$f_{\theta}$ 为待学习的速度场。该公式直接驱动模型学习从噪声到数据的线性插值路径。

### 3.2 全局-局部多尺度 Patch 架构

MPDiT 的核心创新在于其层次化的 Patch 处理策略，将标准 DiT 的等距 patch 划分替换为粗到细的多尺度设计：

- **大 Patch 嵌入**：前 $N-k$ 个 Transformer Block 使用 $p=4$ 的大 patch 尺寸，将输入 token 数量从标准 $p=2$ 的 256 个降至 64 个，以极低的计算代价捕获全局上下文。
- **上采样模块（Upsample Block）**：在全局阶段与局部阶段之间，通过线性投影与 pixel-unshuffle 操作将 64 个大 patch token 扩展为 256 个小 patch token，实现序列长度的 4 倍增长。
- **小 Patch 精炼**：最后 $k$ 个 Transformer Block 在 $p=2$ 的全分辨率 token 上运行，专注于局部细节的精细化生成。

### 3.3 多 Token 类别嵌入

为增强条件信息的表达能力，MPDiT 采用多 token 类别表示。给定类别索引 $c \in \{1, \ldots, C\}$ 和类别 token 数量 $m$，学习一个类别嵌入矩阵 $E_{cls} \in \mathbb{R}^{C \times (m D)}$，然后通过 reshape 操作将其转换为 $m$ 个维度为 $D$ 的 token：

$$T_{cls} = \text{reshape}(E_{cls}[c], (m, D))$$

这些类别 token 与图像 token 拼接后一同输入 Transformer Block，使模型能够从多个表示子空间吸收类别信息。

### 3.4 FNO 时间嵌入

传统时间嵌入仅对正弦时间特征施加两层线性变换。MPDiT 将其替换为基于傅里叶神经算子（FNO）的时间嵌入模块，通过多个 MixedFNO Block 在频域对时间特征进行变换，以捕获时间步之间更平滑的过渡关系，为模型提供更丰富的时间表征。该模块的结构如图 Fig. 2(d) 所示。

### 3.5 共享 AdaIN 策略

标准 DiT 在每个 Transformer Block 中独立使用自适应实例归一化（AdaIN）注入条件和时间信息。MPDiT 将 AdaIN 操作前置为共享模块：先将类别嵌入与时间嵌入合并，统一施加 AdaIN，再将结果分发至各 Block。此设计使参数量从 130M 降至约 90M，减少约 30%，同时保持了生成质量。

## 实验与关键发现

### 主实验结果

MPDiT 在 ImageNet 256×256 上的定量结果汇总于 Table 1。MPDiT-XL 在无分类器引导（non-cfg）设置下，经 240 个 epoch 训练后达到 **FID 7.36**；引入引导后，MPDiT-XL-G 以 cfg-scale 1.4 取得 **FID 2.05**。作为对比，SiT 基线需要 1400 个 epoch 才达到 FID 9.35，MPDiT 在训练效率和生成质量上均有显著优势。

![[assets/figures/papers/paper_list_l900_https_arxiv_org_abs_2603_26357/figures/003_Table_1.jpg]]
*Table 1: Quantitative performance of MPDiT on ImageNet 256*

在计算效率方面，MPDiT-XL 的层次化设计将 GFLOPs 从 DiT 的 23 降至 **16.6**，降幅约 28%；若将最后 k 个 block 的 patch size 也设为 p=4（即全部 block 使用大 patch），GFLOPs 可进一步降至 **11.8**，降幅达 **50%**，但会牺牲部分生成质量。Table 2 给出了不同 MPDiT 变体的完整配置与计算开销。

![[assets/figures/papers/paper_list_l900_https_arxiv_org_abs_2603_26357/figures/004_Table_2.jpg]]
*Table 2: Model configuration and computational cost of MPDiT*

ImageNet 512×512 的结果见 Table 8 和 Table 9，MPDiT 在该分辨率下同样保持了竞争力，定性结果如 Figure 3 所示。

![[assets/figures/papers/paper_list_l900_https_arxiv_org_abs_2603_26357/figures/010_Table_8.jpg]]
*Table 8: Quantitative results of ImageNet 512 with*

![[assets/figures/papers/paper_list_l900_https_arxiv_org_abs_2603_26357/figures/012_Figure_3.jpg]]
*Figure 3: Qualitative Result of Imagenet 512 with cfg=4*

### 消融实验

消融实验系统性地验证了 MPDiT 各组件贡献，所有消融模型均在相同设置下训练 80 个 epoch。

**组件贡献拆解（Table 3）**：以 DiT-XL/2（FID 35.31）为基线，逐步叠加各改进：
- **Shared AdaIN**：将逐块 AdaIN 替换为共享 AdaIN，作用于合并后的时间与类别嵌入，参数量从 130M 降至 90M（约 **30%** 缩减），FID 基本持平；
- **Multi-token class embedding**：将单 token 类别嵌入扩展为 m 个可学习 token，FID 从 35.31 降至 **28.56**，约 **7 个点**的提升；
- **FNO time embedding**：替换传统线性时间嵌入，FID 进一步降至 **24.10**，额外贡献约 4 个点；
- **Global-to-Local 架构**：最终引入多 patch 层次化设计，FID 降至 **21.86**。

**层次化深度 k 的影响（Table 4）**：k 表示使用小 patch（p=2）的最后若干个 transformer block 数量。k=6 时在质量与效率间取得最佳平衡；k 过小则细节不足，k 过大则计算开销回升。

**时间嵌入模块设计（Table 5）**：对比传统线性时间嵌入（两层 Linear + 正弦特征），FNO 时间嵌入使用 3 个 MixedFNO block，在 FID 上获得稳定增益。增加 Linear 层数或 MixedFNO block 数量未带来进一步显著提升。

**类别 token 数量 m（Table 6）**：增大 m 可提升类别信息的表达能力，但边际收益递减。需根据模型规模选择合适的 m。

**Upsample Block 设计（Table 7）**：消融了 MLP ratio r 及上采样策略。线性投影配合 pixel-unshuffle 操作将 token 数从 64 扩展至 256，是层次化架构的关键衔接模块，设计选择直接影响信息传递质量。

### 关键结论

1. **瓶颈与因果机制**：DiT 等标准扩散 Transformer 的均匀 patch 划分导致浅层 block 在细粒度 token 上浪费大量计算，而全局上下文捕获不足。MPDiT 通过“大 patch 捕获全局 → 上采样 → 小 patch 精修局部”的 coarse-to-fine 流程，在降低约 30–50% GFLOPs 的同时提升生成质量。核心因果旋钮在于**层次化 patch 粒度与对应 transformer block 的分配比例 k**。

2. **证据强度**：主结果和消融实验覆盖了 FID、GFLOPs、参数量等多维度指标，训练设置统一（80 epoch 消融，240 epoch 主结果），结论可信度较高。但所有实验均在 ImageNet 单一数据集上完成，跨域泛化性需进一步验证。

3. **失败模式与局限**：当全部 block 使用大 patch（k=0）时，计算量最低但 FID 显著恶化，表明后期的小 patch 精修对细节生成不可或缺。此外，论文主要在 class-conditional 生成场景下验证，未涉及 text-to-image 等更复杂的条件生成任务。

![[assets/figures/papers/paper_list_l900_https_arxiv_org_abs_2603_26357/figures/005_Table_3.jpg]]
*Table 3: Ablation on MPDiT components. All models are trained for 80 epochs under the same settings. Note that in the second row (shared AdaIN), we still apply AdaIN to the combined class and time embeddings as original DiT*

## 定位与知识库关联

### 与基线方法的关系

MPDiT 的架构建立在 **DiT**（Peebles & Xie, ICCV 2023）的基础之上，DiT 是首个将纯 Transformer 架构引入扩散模型骨干的里程碑工作。DiT 采用各向同性（isotropic）设计，所有 Transformer 块在固定 patch 大小（p=2）和固定序列长度上运行，以 AdaIN 方式将时间条件和类别条件注入每个块。MPDiT 保留了 DiT 的核心 Transformer 块结构，但对其三个关键设计槽位进行了系统性替换：

1. **全局到局部的多 patch 层次化架构**：DiT 的全分辨率各向同性设计导致计算量与序列长度的平方成正比，成为效率瓶颈。MPDiT 引入 coarse-to-fine 的视觉处理范式——前 N−k 个块在 p=4 的大 patch 上运行（序列长度 64），经 Upsample Block 扩展后，最后 k 个块在 p=2 的小 patch 上运行（序列长度 256）。这一设计将 GFLOPs 从 DiT-XL/2 的 23 降至 16.6，降幅约 28%，同时保持生成质量。

2. **共享 AdaIN 与条件注入重构**：DiT 在每个 Transformer 块内独立执行 AdaIN 调制，参数冗余度高。MPDiT 将时间嵌入与类别嵌入在进入 Transformer 块之前先合并，再通过共享的 AdaIN 层注入所有块，参数量从 130M 降至 90M（约 30% 缩减）。

3. **FNO 时间嵌入替换线性时间嵌入**：DiT 使用两层 MLP 处理正弦时间特征。MPDiT 将其替换为基于傅里叶神经算子（FNO）的 MixedFNO 块，在频域和时域交替操作，捕获更平滑的跨时间步表示。消融实验表明该替换带来约 4 个 FID 点的提升。

与 **MaskDiT**（Zheng et al., ICCV 2023）相比，后者在 DiT 上引入掩码建模训练策略，但在 p=2 的 patch 大小下 FID 约 100（75% 掩码率），而 DiT-XL/4 仅使用大 patch 即可达约 40 FID。这一观察直接启发了 MPDiT 的多 patch 设计——大 patch 在早期提供高效全局建模，小 patch 在后期恢复细节。

与 **SiT**（Ma et al., ECCV 2024）相比，SiT 同样采用 DiT 架构但使用插值框架，需要 1400 个 epoch 达到 FID 9.35。MPDiT-XL 在仅 240 个 epoch 下即达到无分类器引导（non-cfg）FID 7.36，cfg FID 2.05（cfg scale 1.4），在训练效率和最终质量上均显著超越。

与 **U-ViT**（Bao et al., CVPR 2023）和 **MDT**（Gao et al., ICCV 2023）等同样探索 Transformer 扩散骨干的工作相比，MPDiT 的独特贡献在于通过 patch 粒度的层次化设计而非 UNet 式的跳跃连接来实现全局到局部的信息流动，保持了纯 Transformer 的简洁性。

### 适用边界与局限

尽管 MPDiT 在 ImageNet 256×256 和 512×512 的类别条件生成上展现了强大的性能与效率，其适用边界和局限值得关注：

- **类别条件生成的依赖**：MPDiT 的多 token 类别嵌入设计（m 个可学习 token 表示每个类别）在类别条件生成中贡献显著（消融显示降低约 7 个 FID 点）。该设计是否适用于文生图等更复杂的条件场景，或无条件生成，论文未提供证据，需要手动验证。

- **固定层次结构的刚性**：MPDiT 的 patch 大小切换点（p=4→p=2）和块数分配（N−k 与 k）是预定义的超参数。消融实验仅探索了 k 值（最后使用小 patch 的块数），但未研究多级层次（如 p=8→p=4→p=2）或自适应切换策略。在需要更灵活的多尺度建模的场景中，这种固定二分结构可能不够充分。

- **分辨率扩展的泛化性**：论文在 ImageNet 512 上验证了 MPDiT 的可扩展性，但未讨论更高分辨率（如 1024×1024）下 patch 大小和块数分配的最优策略。当前设计中的 p=4 大 patch 在 512 分辨率下产生 128×128 个 token，序列长度已显著增长，可能需要引入额外的层次级别。

- **与最新扩散框架的集成**：MPDiT 基于 flow matching 框架实现，但消融和对比实验主要围绕架构组件展开，未深入探讨其与不同采样器、蒸馏技术或引导策略的交互效应。

### 开放问题

1. **多级层次的扩展**：当前 MPDiT 仅使用两级 patch 粒度（p=4 和 p=2）。引入三级甚至多级层次（如 p=8→p=4→p=2）能否在高分辨率生成中进一步释放效率与质量的权衡？如何自动确定最优的层次深度和每层的块数分配？

2. **patch 切换的可学习性**：Upsample Block 当前使用固定的线性投影加 pixel-unshuffle 操作。是否可以让模型学习何时以及如何执行 token 上采样，实现数据自适应的层次切换？

3. **与其他高效 Transformer 技术的兼容性**：MPDiT 的层次化设计与稀疏注意力、线性注意力、状态空间模型等高效序列建模技术是否正交？组合使用能否实现进一步的效率提升？

4. **视频生成的适用性**：全局到局部的多 patch 设计天然适合视频的时空层次结构。在视频扩散 Transformer 中，时空 patch 的层次化策略如何设计？时间维度和空间维度的 patch 粒度是否需要独立控制？

5. **FNO 时间嵌入的理论解释**：消融实验表明 FNO 时间嵌入带来约 4 个 FID 点的提升，但其工作机制尚缺乏深入的理论分析。频域操作是否有助于解耦不同频率的时间动态？这种优势在更长的采样步数或不同的噪声调度下是否保持？

## 原文 PDF

![[paperPDFs/CVPR_2026/Multi_Patch_Global_to_Local_Transformer_Architecture_For_Efficient_Flow_Matching_and_Diffusion_Model.pdf]]
