---
title: "MoMask: Generative Masked Modeling of 3D Human Motions"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/MoMask_Generative_Masked_Modeling_of_3D_Human_Motions.pdf
project_link: https://ericguo5513.github.io/momask/
code_link: null
aliases:
- MoMask
tags:
- CVPR_2024
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "采用残差矢量量化（RVQ）构建多层离散运动令牌以逐步减少量化误差，并引入掩码双向Transformer（M-Transformer）进行并行基座层预测，配合残差Transformer（R-Transformer）逐层生成精细令牌，实现高效且高保真的运动生成。"
primary_logic: "将图像生成中的生成式掩码建模范式迁移至运动生成，结合残差量化，显著降低量化噪声，实现双向并行解码，在15次迭代内生成长序列的高质量运动。"
claims:
- "MoMask在HumanML3D上达到FID 0.045，大幅优于T2M-GPT的0.141，刷新SOTA。"
- "移除残差量化（w/o RQ）导致FID从0.051升至0.093，验证RVQ的关键作用。"
- "仅需15次迭代即可生成完整运动序列，远少于离散扩散模型的数百次迭代。"
- "用户研究中MoMask被偏好率最高，甚至相对真实运动也有42%的偏好。"
---

# MoMask: Generative Masked Modeling of 3D Human Motions

> [!tip] 核心洞察
> 将图像生成中的生成式掩码建模范式迁移至运动生成，结合残差量化，显著降低量化噪声，实现双向并行解码，在15次迭代内生成长序列的高质量运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoMask：基于掩码建模的3D人体运动生成 |
| 英文题名 | MoMask: Generative Masked Modeling of 3D Human Motions |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2312.00005) · [Project](https://ericguo5513.github.io/momask/) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | MoMask |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，FID↓ 为 0.045，对比 0.141 (T2M-GPT)，变化 -0.096。
> - HumanML3D 上，R Precision Top1↑ 为 0.521，对比 0.510 (ReMoDiffuse)，变化 +0.011。
> - HumanML3D 上，MultiModal Dist↓ 为 2.958，对比 2.974 (ReMoDiffuse)，变化 -0.016。

## 概要

### 问题与瓶颈

文本到3D人体运动生成的核心挑战在于同时实现高保真度、高文本对齐度和高推理效率。现有主流方法主要分为两类：基于矢量量化（VQ）的自回归Transformer（如**T2M-GPT**，Zhang et al., arXiv 2023）和基于扩散的生成模型（如**MDM**，Tevet et al., arXiv 2022；**MLD**，Chen et al., CVPR 2023；**MotionDiffuse**，Zhang et al., arXiv 2022）。前者通过VQ将运动压缩为离散令牌，再以单向自回归方式逐令牌生成，但**单次VQ引入的逼近误差较大**，且单向解码限制了全局上下文建模，导致误差累积；后者虽能生成较高质量的运动，但**迭代去噪过程通常需要数百步**，推理速度慢，难以满足实时交互需求。

### 核心方法

MoMask首次将**生成式掩码建模范式**从图像生成领域迁移至文本到运动生成，并设计了**层次化残差矢量量化（RVQ）**与**双Transformer架构**来解决上述瓶颈：

- **残差矢量量化（RVQ-VAE）**：将运动序列编码为多层离散令牌（基础层 + V层残差令牌），通过递归量化残差逐步逼近原始运动表示，显著降低单层VQ的量化噪声。
- **掩码双向Transformer（M-Transformer）**：以文本为条件，采用迭代掩码预测策略并行生成基础层令牌序列，仅需约10次迭代即可完成，远少于扩散模型的数百步。
- **残差Transformer（R-Transformer）**：以前序层令牌和文本为条件，逐层渐进预测高层残差令牌，恢复运动细节。

整个推理流程从全掩码序列出发，M-Transformer在L次迭代内生成基础令牌，随后R-Transformer一次性预测各残差层，总计约15步即可生成完整运动序列。

### 主要结果

MoMask在HumanML3D和KIT-ML两个主流基准上均取得SOTA性能，尤其在运动保真度指标上大幅领先：

| 基准 | 指标 | MoMask | 最强基线 | 提升 |
|------|------|--------|----------|------|
| HumanML3D | FID↓ | **0.045** | 0.141 (T2M-GPT) | -0.096 |
| HumanML3D | R Precision Top1↑ | **0.521** | 0.510 (ReMoDiffuse) | +0.011 |
| HumanML3D | MultiModal Dist↓ | **2.958** | 2.974 (ReMoDiffuse) | -0.016 |
| KIT-ML | FID↓ | **0.204** | 0.514 (T2M-GPT) | -0.310 |

消融实验证实，**移除残差量化（w/o RQ）使FID从0.051升至0.093**，验证了RVQ对生成质量的关键贡献。用户研究中，MoMask相对其他模型的偏好率均超过50%，甚至相对真实运动也有42%的偏好率。推理效率方面，MoMask在单张Nvidia 2080Ti上以远低于扩散模型的推理时间达到最优FID，实现了质量与速度的最佳平衡。

### 方法定位

MoMask属于**离散令牌空间中的生成式掩码建模**方法，与自回归VQ方法（T2M-GPT）共享离散表示的思想，但以双向并行解码替代单向自回归；与扩散方法（MDM、MLD）共享迭代生成的框架，但将迭代次数从数百步压缩至15步以内。其层次化残差量化设计借鉴了图像生成中的RQ-VAE思路，但在运动生成领域首次与掩码Transformer结合，形成了“基座并行预测 + 残差渐进细化”的高效生成范式。



### 问题背景

文本驱动的3D人体运动生成旨在根据自然语言描述合成逼真的动作序列，在动画制作、虚拟现实和具身智能等领域具有广泛的应用前景。高质量的运动生成需要同时满足两个核心要求：**高保真度**，即生成的运动在视觉上自然且符合物理规律；以及**精确的文本语义对齐**，即动作能够准确反映文本中的细微语义线索，如“踉跄”（stumble）、“蹑手蹑脚”（sneak）或“侧身走”（walk sideways）等。

### 现有方法的瓶颈

当前主流的文本到运动生成方法主要沿两条技术路线展开，但各自面临根本性的局限：

**矢量量化（VQ）路线**以 **T2M-GPT**（Zhang et al., arXiv 2023）为代表，将运动序列编码为离散令牌后，采用单向自回归Transformer逐令牌生成。该方法存在两重瓶颈：其一，单次矢量量化引入较大的逼近误差，难以保留运动的精细细节；其二，单向解码限制了全局上下文建模能力，导致误差在长序列生成中逐步累积，且推理效率低下——生成一段运动需要与序列长度成正比的解码步数。

**扩散模型路线**以 **MDM**（Tevet et al., arXiv 2022）、**MotionDiffuse**（Zhang et al., arXiv 2022）和 **MLD**（Chen et al., CVPR 2023）为代表，通过迭代去噪生成运动。尽管这些方法在保真度上有所提升，但其推理过程通常需要数百次甚至上千次去噪迭代，计算开销巨大。**ReMoDiffuse**（Zhang et al., arXiv 2023）通过检索增强进一步提升了对齐精度，但未能根本解决扩散模型固有的推理效率问题。

### 核心洞察与动机

本文的关键洞察来自图像生成领域的范式迁移：**生成式掩码建模**（Generative Masked Modeling）已在图像合成中展现出双向并行解码的优势，能够在极少的迭代次数内生成长序列的高质量内容。将这一范式迁移至运动生成，有望同时解决VQ路线的误差累积问题和扩散模型的效率瓶颈。

然而，直接将掩码建模应用于运动生成面临一个关键挑战：运动序列的连续性与离散令牌表示之间的矛盾。单层VQ的量化噪声会严重损害生成质量，而掩码建模又天然依赖离散令牌空间。为此，本文提出**残差矢量量化（RVQ）** 构建多层离散运动令牌，通过逐层量化残差来逐步逼近原始运动，将量化误差分散到多个层次，从而在保留离散令牌便利性的同时显著降低整体逼近误差。在此基础上，引入**掩码双向Transformer**进行并行基座层预测，配合**残差Transformer**逐层生成精细令牌，形成高效且高保真的运动生成框架——**MoMask**。



## 核心方法与创新机理

MoMask 的核心创新在于将**生成式掩码建模（generative masked modeling）**范式从图像生成迁移至文本驱动的3D人体运动生成，并通过**残差矢量量化（RVQ）**替代传统的单层矢量量化，构建了一套“多层离散运动令牌+双向并行解码”的生成框架。相对于现有方法，其关键改动集中在以下三个维度。

### 1. 从单层VQ到多层残差矢量量化（RVQ）

现有基于VQ的运动生成方法（如 **T2M-GPT**，Zhang et al., arXiv 2023）通常采用单次矢量量化，将运动序列压缩为一组离散令牌。这种单层量化存在较大的逼近误差，限制了运动重建的精度。

MoMask 引入**残差矢量量化（Residual VQ, RVQ）**，将运动隐空间表示递归地量化为 V+1 层有序的离散码本序列：

$$\mathbf{b}^v = \operatorname{Q}(\mathbf{r}^v), \quad \mathbf{r}^{v+1} = \mathbf{r}^v - \mathbf{b}^v$$

其中第一层（基座层）捕获运动的粗粒度结构，后续残差层逐层补充精细细节。训练目标为运动重建损失与各层隐空间嵌入损失的加权和：

$$\mathcal{L}_{rvq} = \|\mathbf{m} - \hat{\mathbf{m}}\|_1 + \beta \sum_{v=1}^{V} \|\mathbf{r}^v - \mathrm{sg}[\mathbf{b}^v]\|_2^2$$

这一改动使运动表征从“单一粒度”升级为“多分辨率层次化表征”，显著降低了量化噪声。消融实验直接验证了其关键性：移除残差量化（w/o RQ）后，HumanML3D 上的生成 FID 从 0.051 升至 0.093（Table 2）。

### 2. 从单向自回归解码到双向掩码并行解码

传统方法（如 T2M-GPT）采用**单向自回归 Transformer** 逐令牌生成运动序列，存在两个固有缺陷：（1）无法建模全局上下文，导致误差累积；（2）推理效率受限于序列长度，需串行解码。

MoMask 将基座层令牌的生成任务转化为**掩码预测问题**，引入**掩码双向 Transformer（M-Transformer）**：训练时随机遮蔽基座层令牌，以文本条件预测被遮蔽位置；推理时从全遮蔽序列出发，通过迭代式置信度调度逐步填充，在约 10–15 次迭代内并行生成完整序列。训练目标为最大化被遮蔽令牌的负对数似然：

$$\mathcal{L}_{mask} = \sum_{\tilde{t}_k^0 = [\mathrm{MASK}]} -\log p_\theta(t_k^0 | \tilde{t}^0, c)$$

这一设计将解码复杂度从 O(N) 降至 O(L)（L 为迭代次数，远小于序列长度 N），同时双向注意力使每个令牌的预测可利用全局上下文，有效抑制了误差累积。

### 3. 逐层渐进式残差令牌生成

对于基座层之外的 V 层残差令牌，MoMask 设计了**残差 Transformer（R-Transformer）**，以前序层的令牌序列和文本条件为输入，逐层预测当前层的残差令牌：

$$\mathcal{L}_{res} = \sum_{j=1}^{V} \sum_{i=1}^{n} -\log p_{\phi}(t_i^j | t_i^{1:j-1}, c, j)$$

推理时，R-Transformer 在基座层令牌生成后，按层序逐步预测各残差层令牌，最终将所有层令牌求和后经 RVQ-VAE 解码器恢复为运动序列。这种“基座层并行生成 + 残差层渐进细化”的策略，在保持推理高效的同时实现了高保真运动重建。

### 4. 辅助机制：量化丢弃与无分类器引导

为进一步提升训练稳定性和文本控制能力，MoMask 引入了两项辅助机制：

- **量化丢弃（QDropout）**：训练时随机丢弃部分残差层的量化结果，迫使模型学习更鲁棒的运动表征。消融实验表明，QDropout 能降低运动重建的 MPJPE 并提升生成质量（Table 2）。
- **无分类器引导（Classifier-Free Guidance）**：推理时同时计算条件与无条件 logits，通过引导尺度 s 加权融合：

$$\omega_g = (1 + s) \cdot \omega_c - s \cdot \omega_u$$

该机制增强了文本条件对生成运动的控制精度，引导尺度 s ≈ 4 时达到保真度与文本对齐的最佳平衡（Figure 7 top）。

### 创新总结

MoMask 的 changed slots 可归纳为：

| 组件 | 基线方案 | MoMask 方案 | 核心优势 |
|------|---------|------------|---------|
| 运动量化 | 单层 VQ | 多层 RVQ（V+1 层） | 降低量化误差，保留精细运动细节 |
| 生成骨干 | 单向自回归 Transformer | 双向掩码 Transformer（M-Transformer） | 全局上下文建模，并行解码 |
| 解码策略 | 逐令牌串行采样 | 迭代掩码预测 + 置信度调度 | 推理仅需 10–15 次迭代 |
| 残差生成 | 无 | 残差 Transformer（R-Transformer） | 逐层渐进细化，高保真重建 |

这些创新协同作用，使 MoMask 在 HumanML3D 上取得 FID 0.045 的 SOTA 结果（对比 T2M-GPT 的 0.141），同时在用户研究中获得了显著高于基线方法的偏好率，甚至相对真实运动也有 42% 的偏好（Figure 5b）。



MoMask 将文本到运动生成问题建模为**分层离散令牌的生成式掩码预测**，整体 pipeline 由三个核心模块串联构成：残差矢量量化器（RVQ‑VAE）、掩码双向Transformer（M‑Transformer）和残差Transformer（R‑Transformer）。

### 数据流与模块关系

**阶段一：运动到多层令牌的编码。**
原始运动序列 $\mathbf{m}$ 首先经过一维卷积编码器映射为隐空间嵌入序列，随后进入 $V+1$ 层残差矢量量化（RVQ）。第 0 层为基础量化层（即标准 VQ），产生基础层令牌序列 $\mathbf{t}^0$；后续 $V$ 层对残差 $\mathbf{r}^v$ 递归量化，逐层生成残差令牌序列 $\mathbf{t}^1, \ldots, \mathbf{t}^V$。递归过程遵循：
$$\mathbf{b}^v = \operatorname{Q}(\mathbf{r}^v), \quad \mathbf{r}^{v+1} = \mathbf{r}^v - \mathbf{b}^v$$
最终运动序列可由各层量化嵌入求和后经解码器重建。RVQ‑VAE 的训练目标为运动重构损失与各层隐空间嵌入损失之和：
$$\mathcal{L}_{rvq} = \|\mathbf{m} - \hat{\mathbf{m}}\|_1 + \beta \sum_{v=1}^{V} \|\mathbf{r}^v - \mathrm{sg}[\mathbf{b}^v]\|_2^2$$
其中 $\mathrm{sg}[\cdot]$ 为停止梯度操作。这一分层量化设计是 MoMask 降低逼近误差的关键——消融实验表明，移除残差量化（w/o RQ）会使 HumanML3D 上的生成 FID 从 0.051 升至 0.093。

**阶段二：基础层令牌的并行生成。**
给定文本条件 $c$（由冻结的 CLIP 文本编码器提取特征），M‑Transformer 以双向掩码建模方式生成基础层令牌序列 $\mathbf{t}^0$。训练时，对 $\mathbf{t}^0$ 施加随机掩码，掩码比例按余弦调度 $\gamma(\tau) = \cos(\pi\tau/2)$ 变化，被掩码位置遵循 BERT 的替换策略（80% [MASK]、10% 随机令牌、10% 保持不变）。训练目标为最大化被掩码令牌的负对数似然：
$$\mathcal{L}_{mask} = \sum_{\tilde{t}_k^0 = [\mathrm{MASK}]} -\log p_\theta(t_k^0 | \tilde{t}^0, c)$$
推理时，从全掩码序列出发，通过 $L$ 次迭代逐步预测并替换低置信度令牌，实现并行解码。实验显示 $L=10$ 时 FID 已饱和，仅需约 15 次迭代即可生成完整运动令牌集。

**阶段三：残差令牌的逐层渐进预测。**
获得基础层令牌 $\mathbf{t}^0$ 后，R‑Transformer 以前序层令牌 $\mathbf{t}^{0:j-1}$、文本条件 $c$ 和层索引 $j$ 为条件，逐层预测第 $j$ 层残差令牌 $\mathbf{t}^j$。训练目标为：
$$\mathcal{L}_{res} = \sum_{j=1}^{V} \sum_{i=1}^{n} -\log p_{\phi}(t_i^j | t_i^{1:j-1}, c, j)$$
推理时，R‑Transformer 在固定步数内依次生成所有残差层令牌序列 $\mathbf{t}^{1:V}$。

**阶段四：运动解码。**
完整的 $V+1$ 层令牌序列 $\mathbf{t}^{0:V}$ 经 RVQ‑VAE 解码器一次性投影回运动空间，输出最终运动序列 $\hat{\mathbf{m}}$。

### 推理中的文本控制

两个 Transformer 在推理时均采用无分类器引导（classifier‑free guidance），通过引导尺度 $s$ 融合条件与无条件 logits：
$$\omega_g = (1 + s) \cdot \omega_c - s \cdot \omega_u$$
引导尺度 $s \approx 4$ 时在保真度与文本对齐之间取得最佳平衡。

### 与既有范式的关键差异

相比以 T2M‑GPT 为代表的单向自回归 VQ‑VAE 方案，MoMask 在两个维度上进行了根本性改造：

| 组件 | 基线方法 | MoMask |
|------|---------|--------|
| 运动量化 | 单层 VQ，一次产生一组令牌 | 多层 RVQ，$V+1$ 层残差令牌逐步逼近 |
| 生成骨干 | 单向自回归 Transformer | 双向掩码 M‑Transformer（基座层）+ R‑Transformer（残差层） |
| 解码策略 | 逐令牌自回归采样 | 迭代掩码预测，15 次迭代内并行生成全部令牌 |

这种设计使得 MoMask 在 HumanML3D 上达到 FID 0.045，显著优于 T2M‑GPT 的 0.141，同时在推理效率上远优于需要数百次迭代的离散扩散模型。

### 补充图表

![[assets/figures/papers/paper_list_l3_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions/figures/003_Figure_2.jpg]]
*Figure 2: Approach overview. (a) Motion sequence is tokenized through vector quantization $\left( \mathrm { V Q } \right$) , also referred to as the base quantization layer, as well as a hierarchy of multiple layers for residual quantization. (b) Parallel prediction by the Masked Transformer: the tokens in the base layer $t ^ { 0 }$ are randomly masked out with a variable rate, and then a text-conditioned masked transformer is trained to predict the masked tokens in the sequence simultaneously. (c) Layer-by-layer progressive prediction by the Residual Transformer. A text-conditioned residual transformer learns to progressively predict the residual tokens $t ^ { j > 0 }$ from the tokens in previous layers,...



### 1. 残差矢量量化（RVQ-VAE）

MoMask的运动表示核心是一个残差矢量量化变分自编码器（RVQ-VAE）。给定运动序列 $\mathbf{m}$，首先通过1D卷积编码器映射为隐空间嵌入序列 $\tilde{\mathbf{b}}$，随后经过 $V+1$ 层矢量量化递归产生多层离散令牌。

**量化递归过程**：令第 $v$ 层的残差输入为 $\mathbf{r}^v$（首层 $\mathbf{r}^0 = \tilde{\mathbf{b}}$），每层执行最近邻查找：

$$\mathbf{b}^v = \operatorname{Q}(\mathbf{r}^v), \quad \mathbf{r}^{v+1} = \mathbf{r}^v - \mathbf{b}^v$$

其中 $\operatorname{Q}(\cdot)$ 在对应层的码本 $\mathcal{C}^v$ 中查找最近码向量，$\mathbf{b}^v$ 为量化后的嵌入，$\mathbf{r}^{v+1}$ 为传递至下一层的残差。最终运动重构由所有量化嵌入之和经解码器得到：$\hat{\mathbf{m}} = \operatorname{Decoder}(\sum_{v=0}^{V} \mathbf{b}^v)$。

**训练损失**：RVQ-VAE的优化目标包含运动重构损失与各层的隐空间嵌入损失：

$$\mathcal{L}_{rvq} = \|\mathbf{m} - \hat{\mathbf{m}}\|_1 + \beta \sum_{v=1}^{V} \|\mathbf{r}^v - \mathrm{sg}[\mathbf{b}^v]\|_2^2$$

其中 $\mathrm{sg}[\cdot]$ 表示停止梯度操作，$\beta$ 为嵌入损失权重。第一项确保运动重构精度，第二项约束各层残差嵌入接近其量化码向量，从而降低量化噪声。

### 2. 掩码Transformer（M-Transformer）

基础层令牌 $\mathbf{t}^0$ 的生成由双向掩码Transformer完成。训练时，对 $\mathbf{t}^0$ 按余弦调度 $\gamma(\tau) = \cos(\frac{\pi \tau}{2}) \in [0,1]$ 随机掩码，其中 $\tau \sim \mathcal{U}(0,1)$。被选中掩码的令牌按BERT策略处理：80%替换为 `[MASK]`，10%替换为随机令牌，10%保持不变。

训练目标为最大化被掩码令牌的负对数似然，以文本条件 $c$ 和损坏序列 $\tilde{\mathbf{t}}^0$ 为条件：

$$\mathcal{L}_{mask} = \sum_{\tilde{t}_k^0 = [\mathrm{MASK}]} -\log p_\theta(t_k^0 \mid \tilde{\mathbf{t}}^0, c)$$

文本条件 $c$ 由冻结的CLIP文本编码器提取特征，通过交叉注意力注入Transformer各层。

### 3. 残差Transformer（R-Transformer）

残差层令牌 $\mathbf{t}^{j}$（$j \in \{1, \dots, V\}$）由残差Transformer逐层渐进预测。给定前序层令牌 $\mathbf{t}_i^{1:j-1}$ 和文本条件 $c$，模型学习预测第 $j$ 层第 $i$ 个位置的令牌：

$$\mathcal{L}_{res} = \sum_{j=1}^{V} \sum_{i=1}^{n} -\log p_{\phi}(t_i^j \mid t_i^{1:j-1}, c, j)$$

该模块的因果机制在于：基础层提供运动的粗粒度结构，残差层逐步补充精细细节，每层仅需建模当前层令牌对前序层的条件依赖，避免了单层高码本容量的量化困难。

### 4. 推理阶段的无分类器引导

推理时，M-Transformer和R-Transformer均采用无分类器引导（Classifier-Free Guidance）。令 $\omega_c$ 为条件logits，$\omega_u$ 为无条件logits，引导尺度 $s$ 控制文本对齐强度：

$$\omega_g = (1 + s) \cdot \omega_c - s \cdot \omega_u$$

M-Transformer从全 `[MASK]` 序列出发，经 $L$ 次迭代并行解码，每次迭代以置信度最高的预测令牌替换部分掩码位置，逐步生成基础层令牌 $\mathbf{t}^0$。随后R-Transformer以前序层令牌为条件，逐层预测残差令牌 $\mathbf{t}^{1:V}$，最终由RVQ-VAE解码器将多层令牌之和映射回运动序列。



## 实验与关键发现

### 主实验结果

MoMask在HumanML3D和KIT-ML两个标准基准上均取得了最优性能，验证了生成式掩码建模范式在文本驱动运动生成任务上的有效性。

在HumanML3D数据集上，MoMask的FID达到**0.045**，相比此前最优的T2M-GPT（FID 0.141）降低了0.096，相对提升约68%。这一显著差距表明，残差矢量量化（RVQ）结合双向掩码Transformer的并行解码策略，在运动保真度上大幅超越了传统的单向自回归VQ-VAE方案。在文本-运动对齐指标上，MoMask同样表现最优：R Precision Top-1达到**0.521**，MultiModal Dist降至**2.958**，分别优于此前最佳的ReMoDiffuse（0.510和2.974），说明掩码生成范式并未牺牲语义对齐能力。

在KIT-ML数据集上，MoMask保持了同样的领先趋势：FID为**0.204**（T2M-GPT为0.514），R Precision Top-1为**0.433**（ReMoDiffuse为0.427），MultiModal Dist为**2.779**（ReMoDiffuse为2.814）。跨数据集的一致性优势说明该方法具有良好的泛化性。

值得关注的是，仅使用基座层令牌的MoMask（base）版本已具备竞争力，在HumanML3D上FID为**0.051**，仍优于所有基线方法。这证明双向掩码Transformer本身即具备强大的生成能力，而残差层的引入是在此基础上的进一步精细化提升。

### 推理效率与用户偏好

推理效率是MoMask的另一核心优势。如Figure 5(a)所示，在相同Nvidia 2080Ti GPU上，MoMask以极低的推理时间取得了最优FID，在FID-推理代价散点图中最接近原点。核心原因在于：掩码解码仅需**10-15次迭代**即可生成完整序列，而离散扩散模型通常需要数百次迭代。这一效率优势使MoMask在实际部署中更具可行性。

用户研究（Figure 5(b)）进一步验证了生成质量的主观感知：MoMask相对所有对比方法均获得超过50%的偏好率，甚至相对真实运动也有**42%**的偏好。这意味着在部分场景下，用户认为MoMask生成的样本比真实数据更符合文本描述，侧面反映了该方法在文本控制精度上的优势。

![[assets/figures/papers/paper_list_l3_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions/figures/001_Figure.jpg]]

![[assets/figures/papers/paper_list_l3_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions/figures/007_Figure_5.jpg]]
*Figure 5: (a) Comparison of inference time costs. All tests are conducted on the same Nvidia2080Ti. The closer the model is to the origin, the better. (b) User study results on the HumanML3D dataset. Each bar represents the preference rate of MoMask over the compared model. Overall, MoMask is preferred over the other models most of the time. The dashed line marks 50%*

### 消融实验

Table 2系统拆解了各设计组件的贡献。

**残差矢量量化（RVQ）的核心作用**：移除残差量化（w/o RQ）后，HumanML3D上的生成FID从0.051升至**0.093**，降幅达45%。这直接证实了多层离散令牌对减少量化逼近误差的关键作用——单层VQ的表示能力不足以捕捉运动细节，而RVQ通过逐层残差补偿显著提升了重建精度。

**与现有运动VQ方案的对比**：MoMask的RVQ设计在运动重建（MPJPE）和生成（FID）两个维度上均优于T2M-GPT、TM2T和MDM所使用的VQ方案。这表明RVQ不仅是简单的层数堆叠，其训练策略（如停止梯度操作、隐空间嵌入损失）对最终性能同样重要。

**量化丢弃（QDropout）**：设置q=0.2的量化丢弃率进一步改善了MPJPE和生成FID。该机制在训练时随机丢弃部分残差层，迫使模型学习更鲁棒的基座层表示，从而在推理时获得更好的泛化能力。

**替换与重掩码（RRmask）**：该策略对运动重建和生成保真度均有正向贡献。遵循BERT的掩码策略（80% [MASK]、10%随机令牌、10%保持不变）使模型在训练中接触到更丰富的上下文模式，增强了双向建模能力。

**残差量化层数**：V=5时生成FID达到最优，超过5层后性能反而下降。这一现象说明过深的量化层次可能引入冗余或噪声，最优层数需要在表示精度和模型复杂度之间取得平衡。

**掩码解码迭代数**：如Figure 7（底部）所示，L=10时FID已趋于饱和，进一步增加迭代次数几乎不带来性能增益。这解释了MoMask为何能以极少的迭代次数实现高质量生成——掩码预测策略在10步内即可完成对基座层令牌的全局优化。

### 失败模式与局限性

尽管整体性能优异，MoMask仍存在若干可辨识的不足：

1. **运动多样性受限**：模型在极端姿态或罕见动作上表现保守，倾向于生成高概率的“安全”运动。这是生成式掩码建模的固有特性——双向并行解码虽提升了保真度，但也可能抑制了低概率模式的探索。

2. **快速根运动处理不足**：对旋转、急转弯等高频根运动，VQ表示可能无法充分捕捉动态细节。这与VQ-VAE对高频信号的压缩损失有关，残差量化虽有所缓解但未根本解决。

3. **运动时长控制不精确**：文本到运动长度的采样问题尚未完全解决，生成的持续时间控制仍存在偏差。

4. **模态扩展能力有限**：当前框架仅支持文本条件，缺乏对音频、音乐等其他模态的直接扩展机制。

### 关键图表结论

- **Table 1**：MoMask在HumanML3D和KIT-ML上全面刷新SOTA，FID分别降至0.045和0.204，同时保持最优的文本-运动对齐。
- **Table 2**：RVQ是性能提升的最大贡献者，移除后FID恶化45%；QDropout和RRmask提供额外增益；最优RQ层数为5。
- **Figure 5(a)**：MoMask实现FID与推理效率的双重最优，验证了掩码生成范式的高效性。
- **Figure 5(b)**：用户偏好率全面领先，甚至42%的样本被认为优于真实运动。
- **Figure 7**：引导尺度s=4、掩码迭代数L=10为最佳推理配置，10次迭代即可收敛。

![[assets/figures/papers/paper_list_l3_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions/figures/005_Table_1.jpg]]
*Table 1: Quantitative evaluation on the HumanML3D and KIT-ML test set. ± indicates a 95% confidence interval. MoMask (base) means that MoMask only uses base-layer tokens. Bold face indicates the best result, while underscore refers to the second best*

![[assets/figures/papers/paper_list_l3_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions/figures/008_Table_2.jpg]]
*Table 2: Comparison of our RVQ design vs. motion VQs from previous works [16, 23, 49], and further analysis on residual quantization (RQ), quantization dropout (QDropout), and replacing & remasking (RRmask). V and q are the number of RQ and QDropout ratio, respectively. MPJPE is measured in millimeters*



## 定位与知识库关联

### 1. 与基线工作的关系

MoMask 的提出直接针对文本驱动运动生成领域两类主流范式的结构性瓶颈：**矢量量化（VQ）自回归模型**与**扩散模型**。

**相对于 VQ 自回归模型（以 T2M-GPT 为代表）**  
T2M-GPT（Zhang et al., arXiv 2023）采用单层 VQ-VAE 将运动序列压缩为离散令牌，再通过单向自回归 Transformer 逐令牌生成。该范式存在两个根本缺陷：单次矢量量化引入的逼近误差较大，且单向解码限制了全局上下文建模，导致误差累积。MoMask 在三个关键环节上做出了系统性改进：

1. **运动量化槽位**：从单层 VQ 升级为多层残差矢量量化（RVQ），构建 $V+1$ 层递进的离散令牌序列。消融实验（Table 2）表明，移除残差量化（w/o RQ）使 HumanML3D 上的生成 FID 从 0.051 恶化至 0.093，验证了 RVQ 对降低量化噪声的决定性贡献。
2. **生成骨架槽位**：将单向自回归 Transformer 替换为双向掩码 Transformer（M-Transformer），使基座层令牌的生成能够同时利用全局上下文。这一设计直接源自图像生成中 MaskGIT 等生成式掩码建模范式的迁移。
3. **解码策略槽位**：从逐令牌自回归采样转为迭代式掩码预测（并行解码，配合置信度调度），仅需 15 次迭代即可生成完整序列，远少于离散扩散模型的数百次迭代。

**相对于扩散模型（以 MDM、MLD、MotionDiffuse、ReMoDiffuse 为代表）**  
扩散模型（MDM, Tevet et al., arXiv 2022；MotionDiffuse, Zhang et al., arXiv 2022）通过在连续隐空间或原始运动空间中进行逐步去噪生成运动，通常需要数百步采样。MLD（Chen et al., CVPR 2023）将扩散过程移至 VAE 隐空间以加速，但仍受限于扩散范式的迭代开销。ReMoDiffuse（Zhang et al., arXiv 2023）引入了检索增强机制提升生成质量，但其底层仍是扩散框架。MoMask 的掩码生成范式在推理效率上具有天然优势：Figure 5(a) 的 FID-推理代价散点图显示，MoMask 在 FID 和推理时间两个维度上均占据帕累托前沿，更接近原点（更优）。在 HumanML3D 上，MoMask 的 FID 达到 0.045，显著优于 T2M-GPT 的 0.141 和 ReMoDiffuse 的 0.053（Table 1）。

**相对于其他 VQ 运动模型（T2M、TM2T）**  
T2M（Guo et al., CVPR 2022）使用时间 VAE 进行运动生成，TM2T（Guo et al., ECCV 2022）引入随机令牌化 Transformer。MoMask 的 RVQ 设计与这些工作中的单层 VQ 形成对比。Table 2 的消融实验直接比较了 MoMask 的 RVQ 与先前运动 VQ 设计（来自文献 [16, 23, 49]），验证了多层残差量化的优越性。

### 2. 方法适用边界

MoMask 在当前框架下的有效范围存在明确边界：

- **输入模态边界**：仅支持文本条件（通过冻结的 CLIP 文本编码器提取特征），缺乏对其他模态（如音频、音乐、视频）的直接扩展能力。这是框架设计层面的限制，而非训练数据不足所致。
- **运动多样性边界**：尽管生成保真度达到 SOTA，模型在探索极端姿态或罕见动作时表现保守。用户研究（Figure 5(b)）中 MoMask 相对真实运动仍有 42% 的偏好率，从侧面反映出生成运动在“规范性”上可能超越了真实数据的多样性——但这同时也暗示多样性可能受限。
- **高频动态边界**：对快速变化的根运动（如旋转、急转弯）的处理能力不足，VQ 表示可能难以捕捉高频动态。这在 Figure 4 的视觉对比中有所体现：MoMask 对“stumble”“sneak”等细腻语义的把握优于基线，但未见对快速转向等极端动态的专门验证。
- **时长控制边界**：文本到运动长度的采样问题尚未完全解决，生成的持续时间控制仍不够精确。这是一个领域共性问题，MoMask 未提出专门的解决方案。
- **零样本泛化边界**：训练过程依赖大规模运动-文本对，对新领域的零样本泛化能力有限。这与其监督训练范式一致，不同于某些具备少样本能力的元学习或检索增强方法。

### 3. 局限与开放问题

**已识别的局限**

1. **多样性-保真度权衡**：Figure 7 的超参数扫描显示，引导尺度 $s$ 在 4 附近存在保真度-多样性的平衡点，增大 $s$ 虽提升文本对齐但可能进一步压缩多样性。模型缺乏显式的多样性控制机制（如隐变量或噪声注入）。
2. **残差层数饱和**：消融实验（Table 2）表明，残差量化层数 $V=5$ 时生成 FID 最佳，超过 5 层后性能下降。这说明更深层的残差令牌可能引入噪声而非有用信息，RVQ 的信息增益存在上限。
3. **掩码迭代饱和**：Figure 7 底部显示，掩码解码迭代数 $L=10$ 时 FID 已饱和，更多迭代不再带来显著增益。这意味着并行解码的潜力在当前框架下已被充分挖掘。

**开放问题**

1. **多模态条件扩展**：如何将掩码生成框架扩展到音乐、视频等多模态条件，以实现更丰富的运动控制？这需要重新设计条件注入机制，可能涉及跨模态对齐学习。
2. **多样性增强**：能否在保持生成质量的同时引入可控的多样性机制？例如在掩码预测过程中注入结构化噪声，或引入条件变分自编码器的隐变量层。
3. **高频动态建模**：如何改进 VQ 表示以更好地处理快速根运动和细粒度肢体运动？可能的路径包括引入频域分解、混合分辨率令牌化，或在 VQ 编码器中增加高频保留机制。
4. **检索增强融合**：是否可以融合 ReMoDiffuse 所用的检索增强技术来进一步提升生成保真度和文本对齐？检索增强与掩码生成的结合方式（如检索到的运动作为额外的条件令牌）值得探索。
5. **跨任务泛化**：掩码生成范式能否用于其他时间序列生成任务，如手势生成、全身交互动作合成或运动预测？MoMask 的层次化离散表示和双向解码策略具有通用性，但需要针对不同任务的特点调整令牌化方案和条件设计。



## 原文 PDF

![[paperPDFs/CVPR_2024/MoMask_Generative_Masked_Modeling_of_3D_Human_Motions.pdf]]
