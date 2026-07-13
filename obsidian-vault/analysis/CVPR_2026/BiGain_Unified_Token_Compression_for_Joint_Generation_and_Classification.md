---
title: "BiGain: Unified Token Compression for Joint Generation and Classification"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/BiGain_Unified_Token_Compression_for_Joint_Generation_and_Classification.pdf
project_link: null
code_link: "https://github.com/Greenoso/BiGain"
aliases:
- BBTLGBTIK
- BiGain
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 频率感知的令牌保留策略：利用拉普拉斯滤波器计算局部频率幅度，引导令牌合并优先在平滑区域进行，同时保护高频边缘/纹理令牌；在注意力下采样中通过可控插值-外推保留查询分辨率，从而平衡高频细节与低频语义。
primary_logic: 将特征映射至频率感知表示，解耦高频细节（边缘、纹理）与低频/中频内容（形状、布局、语义），通过平衡频谱保留实现兼顾生成保真度与判别效用的压缩——合并低频冗余、保留高频判别信息。
claims:
- 在ImageNet-1K上，使用SD 2.0并在70%令牌合并率下，BiGain_TM将分类准确率提高7.15%，同时生成FID改善0.34（1.85%）。
- 在Oxford-IIIT Pets上同等FLOPs减少下，BiGain_TM保留78.38% Top-1准确率，而ToMe仅72.96%，将准确率损失降低27-78%。
- 拉普拉斯门控合并保留了更多类判别结构（如猫的边缘），而ToMe在90%融合率下导致主要结构丢失。
- 频率感知KV选择实验证明，仅保留高频或低频令牌均严重损害分类（Acc@1分别降至26.56和45.58），验证了平衡频谱的必要性。
---

# BiGain: Unified Token Compression for Joint Generation and Classification

> [!tip] 核心洞察
> 将特征映射至频率感知表示，解耦高频细节（边缘、纹理）与低频/中频内容（形状、布局、语义），通过平衡频谱保留实现兼顾生成保真度与判别效用的压缩——合并低频冗余、保留高频判别信息。

| 字段 | 内容 |
|------|------|
| 中文题名 | BiGain：面向联合生成与分类的统一令牌压缩 |
| 英文题名 | BiGain: Unified Token Compression for Joint Generation and Classification |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.12240) · [Code](https://github.com/Greenoso/BiGain) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | BiGain (包含 BiGain_TM 即 L-GTM，BiGain_TD 即 IE-KVD) |
| Dataset | Oxford-IIIT Pets, ImageNet-100, ImageNet-1K, COCO-2017 |

> [!tip] 效果简介
> - Oxford-IIIT Pets 上，Acc@1 BiGain_TM 78.38% (10% FLOPs reduction) vs ToMe 72.96% (+5.42%)；Acc@1 BiGain_TD 79.90% (14.2% FLOPs reduction) vs ToDo 79.15% (+0.75%)。
> - ImageNet-100 (DiT-XL/2, 2× downsampling) 上，Acc@1 BiGain_TD 78.42% vs ToDo 69.34% (+9.08%)。
> - ImageNet-1K (2K subset, SD-2.0, 70% merging) 上，Acc@1 BiGain_TM 44.50% vs ToMe 37.35% (+7.15%)。

## 概要

扩散模型在生成任务上表现卓越，但其高昂的计算成本催生了多种令牌压缩加速方法。现有方案（如 **ToMe** (Bolya et al., 2023)、**ToDo** (Smith et al., 2024?)）仅以生成质量为优化目标，忽略了模型潜在的判别能力——当压缩率升高时，分类准确率急剧恶化，而生成视觉质量仍可接受。这一瓶颈源于压缩策略对高频判别信息（边缘、纹理）的无差别丢弃。

**BiGain** 的核心洞察是将特征映射至频率感知表示，解耦高频细节与低频/中频语义，通过平衡频谱保留实现生成保真度与判别效用的双重收益。具体而言，BiGain 引入两个免训练、即插即用的算子：

- **拉普拉斯门控令牌合并 (L-GTM / BiGain\_TM)**：利用 2-D 拉普拉斯滤波器计算局部频率幅度，引导合并在平滑（低频）区域进行，同时保护携带判别信息的高频令牌。
- **插值-外推 KV 下采样 (IE-KVD / BiGain\_TD)**：通过可控的最近邻与平均池化线性组合，在保持查询全分辨率的同时下采样键值，降低注意力计算量。

两者均采用时间步局部、无跨步缓存的确定性压缩，适配扩散分类器的蒙特卡洛估计协议。

主要实验结果表明：

- 在 **ImageNet-1K** 上，使用 Stable Diffusion 2.0 并以 70% 令牌合并率，BiGain\_TM 将分类准确率提升 **7.15%**，同时生成 FID 改善 **0.34**（1.85%）。
- 在 **Oxford-IIIT Pets** 上，同等 FLOPs 减少下，BiGain\_TM 保留 **78.38%** Top-1 准确率（仅下降 2.65%），而 ToMe 仅 **72.96%**，将准确率损失降低 27–78%。
- 在 **ImageNet-100** (DiT-XL/2, 2× 下采样) 上，BiGain\_TD 达到 **78.42%**，比 ToDo 的 69.34% 提升 **9.08%**。
- 频率感知 KV 选择消融证实：仅保留高频或低频令牌均导致分类崩溃（Acc@1 分别仅 26.56% 和 45.58%），验证了平衡频谱保留的必要性。

BiGain 为扩散模型在联合生成与判别场景下的高效部署提供了统一的压缩范式，但其联合使用增益非叠加，且超参数需手动调节，自适应机制仍有待探索。

### 扩散模型的生成与判别双重角色

扩散模型（Diffusion Models）已成为视觉生成领域的核心范式。其基本框架包含正向加噪过程与反向去噪过程：正向过程将干净数据 $\mathbf{x}_0$ 逐步注入高斯噪声，形成噪声版本 $\mathbf{x}_t$：

$$q(\mathbf{x}_t \mid \mathbf{x}_0) = \mathcal{N}(\mathbf{x}_t; \sqrt{\bar{\alpha}_t} \mathbf{x}_0, (1 - \bar{\alpha}_t) \mathbf{I})$$

反向过程则训练一个去噪网络 $\epsilon_\theta$ 预测所加噪声，训练目标为均方误差损失：

$$\mathcal{L}(\theta) = \mathbb{E}[\|\epsilon - \epsilon_\theta(\mathbf{x}_t, c, t)\|_2^2]$$

其中 $c$ 为条件信息（如文本提示或类别标签）。值得关注的是，这一去噪误差天然蕴含判别信息：给定条件类别 $c$ 和噪声样本 $(t_s, \epsilon_s)$，逐样本损失 $\ell(\mathbf{x}, c; t_s, \epsilon_s) = \|\epsilon_s - \epsilon_\theta(\mathbf{x}_{t_s}, c, t_s)\|_2^2$ 衡量了条件类别对噪声样本的解释能力。通过聚合多个蒙特卡洛样本的得分并取最小值，扩散模型可直接作为分类器使用：

$$\widehat{L}(\mathbf{x}, c) = \frac{1}{S} \sum_{s=1}^S \ell(\mathbf{x}, c; t_s, \epsilon_s), \quad \widehat{y}(\mathbf{x}) = \arg\min_{c \in \mathcal{C}} \widehat{L}(\mathbf{x}, c)$$

这意味着扩散模型本质上同时具备生成与判别能力。然而，当对模型施加令牌压缩（Token Compression）以加速推理时，这一双重能力面临严重失衡。

### 令牌压缩的困境：生成与判别的失衡

扩散模型的推理计算量巨大，主要瓶颈在于U-Net或DiT骨干网络中自注意力层的二次复杂度。为加速推理，研究者提出了一系列令牌压缩方法，可归为两类：

- **令牌合并（Token Merging）**：以 **ToMe**（Bolya et al., 2023）为代表，基于余弦相似度贪婪合并相似令牌，减少后续注意力计算量。
- **令牌下采样（Token Downsampling）**：以 **ToDo**（Smith et al., 2024?）为代表，通过最近邻或平均池化下采样键值对（K/V）的序列长度。

这些方法在设计时仅以生成质量（如FID）为优化目标，忽略了对模型判别能力的保护。实验揭示了一个关键矛盾（见Figure 2）：在COCO-2017上，随着合并率或下采样因子的增大，基线方法的生成质量（FID）仍可维持在可接受水平，但分类准确率却急剧崩溃。例如，**ToMe**在Oxford-IIIT Pets数据集上，在10% FLOPs减少下准确率降至72.96%，而**ToDo**在14.2% FLOPs减少下准确率为79.15%（Table 1）。这一现象表明，现有压缩策略在追求生成保真度的同时，系统性地丢弃了对分类至关重要的判别信息。

### 核心洞察：频率感知的判别信息保护

BiGain的核心洞察在于**频率分离**：将特征空间信号映射到频率感知表示，解耦高频细节（边缘、纹理）与低频/中频内容（形状、布局、语义）。具体而言：

- **低频区域**（平滑背景、均匀纹理）包含大量冗余信息，适合进行激进的令牌合并以节省计算。
- **高频区域**（物体边缘、纹理交界）携带关键的类判别结构，必须被保留以维持分类能力。
- **平衡频谱**的保留是实现生成保真度与判别效用兼顾的前提——仅保留高频或低频令牌均会导致分类性能崩溃（Table 12消融实验证实：仅保留高频时Acc@1降至26.56%，仅保留低频时降至45.58%）。

基于此洞察，BiGain提出两个训练无关（training-free）、即插即用（plug-and-play）的频率感知算子：**拉普拉斯门控令牌合并（Laplacian-Gated Token Merging, L-GTM / BiGain_TM）** 和**插值-外推KV下采样（Interpolate-Extrapolate KV-Downsampling, IE-KVD / BiGain_TD）**。前者利用拉普拉斯滤波器计算局部频率幅度，引导合并在平滑区域进行，同时保护高频令牌；后者通过可控的插值-外推参数在保持查询（Q）全分辨率的同时下采样键值（K/V），兼顾精确定位与计算效率。

### 方法定位与知识库定位

BiGain处于扩散模型加速与判别能力保护的交叉点，与现有工作的关系如下：

| 方法类别 | 代表工作 | 核心策略 | 局限性 |
|---------|---------|---------|--------|
| 令牌合并 | **ToMe** (Bolya et al., 2023) | 余弦相似度贪婪合并 | 忽略频率结构，损害判别力 |
| 令牌修剪 | **SiTo** | 基于重要性分数修剪 | 同样缺乏频率感知 |
| 模型修剪 | **DiP-GO** (Zhu et al., 2024?)、**MosaicDiff** | 结构化去除冗余层/通道 | 粒度较粗，难以精细保护判别信息 |
| 令牌下采样 | **ToDo** (Smith et al., 2024?) | 最近邻/平均池化下采样 | 未区分高低频令牌的判别价值 |

BiGain的独特贡献在于：首次将频率感知原则系统性地引入扩散模型的令牌压缩，通过拉普拉斯滤波器实现无训练的频谱感知，同时兼顾生成与判别双重目标。该方法不依赖额外训练或模型架构修改，可直接插入现有的U-Net和DiT骨干网络。

## 核心方法与创新机理

BiGain 的核心创新在于将**频率感知**引入扩散模型的令牌压缩，通过解耦高频细节与低频语义，首次在加速推理的同时**兼顾生成保真度与判别效用**。现有加速方法（如 ToMe、ToDo）仅以生成质量为目标，导致压缩后分类准确率急剧下降（例如 COCO-2017 上基线方法准确率崩坏），而 BiGain 通过两个训练无关（training‑free）的即插即用算子逆转了这一困境。

### 创新点一：拉普拉斯门控令牌合并（L‑GTM / BiGain TM）

**基线对比**：ToMe（Bolya et al., 2023）采用余弦相似度贪婪合并，完全忽略令牌的频谱属性，在高合并率下会无差别地融合边缘与纹理令牌，导致类判别结构丢失。

**改进机制**：L‑GTM 引入空间拉普拉斯滤波器计算每个令牌的局部频率幅度：

$$\mathbf{F} = \operatorname{Reduce}_c\left(\left| X * L \right|\right), \quad L = \begin{bmatrix} 0 & 1 & 0 \\ 1 & -4 & 1 \\ 0 & 1 & 0 \end{bmatrix}$$

基于频率分数，算法在低频区域选择锚点（destination token），通过二分图匹配将高频令牌排除在合并之外，仅合并频谱平滑的源令牌。合并后通过 unmerge 恢复原始分辨率，确保高频细节（边缘、纹理）得以保留。这一设计直接响应了核心瓶颈：**合并低频冗余、保护高频判别信息**。

**证据强度**：在 Oxford‑IIIT Pets 上同等 FLOPs 减少（~10%）下，BiGain TM 保留 78.38% Top‑1 准确率，而 ToMe 仅 72.96%，将准确率损失降低 27–78%（Table 1）。在 ImageNet‑1K（SD 2.0，70% 合并率）上，BiGain TM 将分类准确率提升 7.15%，同时生成 FID 改善 0.34（1.85%）（Abstract, Table 4）。可视化进一步证实，在 90% 极端合并率下，拉普拉斯门控合并仍能保留猫的边缘等判别结构，而 ToMe 则导致主要结构丢失（Figure 6）。

### 创新点二：插值‑外推 KV 下采样（IE‑KVD / BiGain TD）

**基线对比**：ToDo（Smith et al., 2024?）使用最近邻下采样，平均池化基线则完全丢失精确定位能力。

**改进机制**：IE‑KVD 通过可控线性组合实现键（K）和值（V）的下采样，同时保持查询（Q）全分辨率：

$$\mathcal{D}_{\alpha, s}(Z)[i] = \alpha Z[\mathrm{nearest}(i)] + (1-\alpha) \frac{1}{|\mathcal{N}_s(i)|} \sum_{j \in \mathcal{N}_s(i)} Z[j]$$

参数 α 在最近邻（保留高频定位）与平均池化（保留低频语义）之间插值‑外推。当 α > 1 时进入外推模式，进一步增强高频保留。这一设计在降低注意力计算成本的同时，保持了查询的精确空间对应关系，避免判别信息在粗糙下采样中丢失。

**证据强度**：在 Oxford‑IIIT Pets 上，BiGain TD 以 14.2% FLOPs 减少达到 79.90% 准确率，优于 ToDo 的 79.15%（Table 1）。在 ImageNet‑100（DiT‑XL/2，2× 下采样）上，BiGain TD 准确率达 78.42%，较 ToDo 的 69.34% 提升 9.08%（Table 3）。消融实验表明，仅保留高频或低频令牌均导致分类崩溃（Acc@1 分别仅 26.56% 和 45.58%），验证了平衡频谱保留的必要性（Table 12）。

### 创新点三：扩散分类器友好的无缓存压缩调度

**基线对比**：部分令牌压缩方法依赖跨时间步缓存以降低计算开销，但这与扩散分类器的蒙特卡洛估计器不兼容——分类需对每个样本独立采样不同的 (t, ε) 对。

**改进机制**：BiGain 的两个算子均采用**时间步局部、无缓存、确定性压缩**，每个去噪步骤独立计算合并/下采样映射，确保扩散分类器的成对估计有效，且所有类别共享相同压缩调度以保证公平比较。

**证据强度**：该设计使 BiGain 能够无缝集成到基于扩散模型的分类流程中，在多个数据集和骨干网络（SD 2.0、DiT‑XL/2）上均展现出稳定的双重收益。

### 频率感知设计的核心洞察

所有创新的共同基础是**将特征映射至频率感知表示，解耦高频细节与低频/中频语义**。拉普拉斯滤波器作为令牌评分在所有合并率下均优于全局统计量、频谱 DFT 和余弦相似度（Table 8），直接验证了频率感知设计的必要性。这一洞察使 BiGain 成为首个在扩散模型加速中明确以**平衡频谱保留**为设计准则的框架，而非仅追求生成质量的单目标优化。

BiGain 是一个免训练、即插即用的统一令牌压缩框架，旨在同时保留扩散模型的生成质量与判别能力。其核心洞察在于**频率分离**：将隐藏特征映射至频率感知表示，解耦高频细节（边缘、纹理）与低频/中频内容（形状、布局、语义），从而在压缩过程中实现**平衡频谱保留**——合并低频冗余令牌，保护承载判别信息的高频令牌。

### 框架总览

BiGain 由两个独立的频率感知算子构成：

1. **拉普拉斯门控令牌合并（Laplacian-Gated Token Merging, L-GTM / BiGain_TM）**：通过空间拉普拉斯滤波器计算每个令牌的局部频率幅度，引导合并操作优先在频谱平滑区域进行，同时抑制高对比度令牌的合并，从而保留类判别结构。
2. **插值-外推 KV 下采样（Interpolate-Extrapolate KV-Downsampling, IE-KVD / BiGain_TD）**：通过可控的线性组合减少键（K）和值（V）的空间维度，同时保持查询（Q）的全分辨率，以降低注意力计算成本并保留精确定位能力。

两个算子均遵循统一的设计原则：
- **免训练、即插即用**：无需对扩散模型进行任何微调或架构修改。
- **无跨时间步缓存**：压缩操作在单个去噪时间步内独立完成，避免引入跨步依赖，确保与扩散分类器的蒙特卡洛估计协议兼容。
- **确定性压缩**：基于频率分数的确定性选择机制，而非随机采样，保证结果可复现。

### 令牌压缩的通用形式

BiGain 的压缩操作可纳入统一的令牌压缩框架。给定扩散 Transformer 层中的隐藏令牌序列 $\mathbf{X} \in \mathbb{R}^{N \times d}$（$N$ 为令牌数，$d$ 为通道维度），压缩流程为：

$$\mathbf{X} \xrightarrow{\tilde{\mathbf{X}} = M\mathbf{X}} \mathbf{Z} = F(\tilde{\mathbf{X}}) \xrightarrow{\tilde{\mathbf{X}} = U\mathbf{Z}} \tilde{\mathbf{X}} \in \mathbb{R}^{N \times d}$$

其中 $M$ 为合并/下采样算子（减少令牌数量），$F$ 为 Transformer 块的前向计算，$U$ 为解合并/恢复算子（恢复原始令牌数量）。BiGain_TM 和 BiGain_TD 分别对应不同的 $M$/$U$ 设计。

### 模块关系与输入输出流

#### BiGain_TM：拉普拉斯门控令牌合并

**输入**：U-Net 自注意力层前的隐藏令牌序列 $\mathbf{X} \in \mathbb{R}^{N \times d}$。

**处理流程**（详见 Figure 1）：
1. **频率评分**：对 $\mathbf{X}$ 的每个空间位置应用 2-D 拉普拉斯核 $L = \begin{bmatrix} 0 & 1 & 0 \\ 1 & -4 & 1 \\ 0 & 1 & 0 \end{bmatrix}$，计算局部频率幅度 $\mathbf{F} = \operatorname{Reduce}_c(|X * L|)$，得到逐令牌的频率分数。
2. **目的地选择**：在每个空间步长（spatial stride）内，选择频率分数最低的令牌作为**目的地令牌**（锚点），其余令牌构成**源令牌集合**。这一策略确保合并发生在频谱平滑区域。
3. **二分图匹配**：全局收集所有目的地令牌与源令牌，基于令牌特征相似度构建二分图，为每个目的地选择最相似的源令牌进行合并。
4. **合并与解合并**：通过加权平均将源令牌信息融合至目的地令牌，减少令牌总数；在 Transformer 块计算完成后，通过 unmerge 操作将信息广播回原始空间位置，恢复分辨率。

**输出**：与输入同形状的令牌序列 $\tilde{\mathbf{X}} \in \mathbb{R}^{N \times d}$，但经过频率感知的信息聚合。

**快速变体**：
- **自适应块合并（Adaptive Block Merging, ABM）**：按块聚合频率分数，直接合并整个低频块，避免逐令牌匹配，在高分辨率阶段额外加速。
- **缓存赋值合并（Cached Assignment Merge）**：在 U-Net 最高分辨率阶段的第一注意力块计算合并/解合并映射并复用，减少重复计算开销。

#### BiGain_TD：插值-外推 KV 下采样

**输入**：自注意力层中的查询 $\mathbf{Q}$、键 $\mathbf{K}$、值 $\mathbf{V}$。

**处理流程**：
1. **保持 Q 全分辨率**：查询 $\mathbf{Q}$ 不做下采样，保留其原始空间分辨率，以维持精确的注意力定位能力。
2. **K/V 下采样**：对 $\mathbf{K}$ 和 $\mathbf{V}$ 应用插值-外推算子 $\mathcal{D}_{\alpha, s}$：
   $$\mathcal{D}_{\alpha, s}(\mathbf{Z})[i] = \alpha \mathbf{Z}[\text{nearest}(i)] + (1-\alpha) \frac{1}{|\mathcal{N}_s(i)|} \sum_{j \in \mathcal{N}_s(i)} \mathbf{Z}[j]$$
   其中 $\alpha$ 为插值-外推因子，$s$ 为下采样步长，$\mathcal{N}_s(i)$ 为位置 $i$ 的邻域。当 $\alpha=1$ 时退化为最近邻下采样，$\alpha=0$ 时为平均池化；通过调节 $\alpha$ 可控制高频与低频信息的保留比例。

**输出**：降采样后的 $\tilde{\mathbf{K}}$、$\tilde{\mathbf{V}}$ 与全分辨率 $\mathbf{Q}$ 送入标准注意力计算，显著降低计算复杂度。

### 扩散分类器集成

BiGain 的压缩模块无缝嵌入扩散分类器的推理管线。对于输入图像 $\mathbf{x}$ 和候选类别 $c$：
1. 在多个共享的蒙特卡洛样本 $(t_s, \epsilon_s)$ 上，对每个去噪时间步应用统一的压缩调度。
2. 计算逐样本损失 $\ell(\mathbf{x}, c; t_s, \epsilon_s) = \|\epsilon_s - \epsilon_\theta(\mathbf{x}_{t_s}, c, t_s)\|_2^2$。
3. 聚合得分 $\widehat{L}(\mathbf{x}, c) = \frac{1}{S} \sum_{s=1}^S \ell(\mathbf{x}, c; t_s, \epsilon_s)$，取最小得分类别作为预测。

所有类别共享相同的噪声样本和压缩调度，确保成对比较的有效性。两个算子均避免跨时间步缓存，保证蒙特卡洛估计的无偏性。

![[assets/figures/papers/paper_list_l841_https_arxiv_org_abs_2603_12240/figures/001_Figure_1.jpg]]
*Figure 1: Framework of our BiGainTM method. A Laplacian filter is applied to hidden-state tokens to compute local frequency scores. In each spatial stride, the lowest-scoring token is selected as a destination token, while the others form the source set. Destination and source tokens are gathered globally, and a bipartite matching selects top source-destination pairs*

### 3.1 扩散模型预备与分类协议

扩散模型的前向过程逐步向干净图像 $\mathbf{x}_0$ 注入高斯噪声，其条件分布为：

$$q(\mathbf{x}_t \mid \mathbf{x}_0) = \mathcal{N}(\mathbf{x}_t; \sqrt{\bar{\alpha}_t} \mathbf{x}_0, (1 - \bar{\alpha}_t) \mathbf{I})$$

其中 $\bar{\alpha}_t$ 为累积噪声调度参数。去噪器 $\epsilon_\theta$ 通过预测注入噪声进行训练，优化目标为：

$$\mathcal{L}(\theta) = \mathbb{E}[\|\epsilon - \epsilon_\theta(\mathbf{x}_t, c, t)\|_2^2]$$

当扩散模型用于分类时，对给定图像 $\mathbf{x}$ 和类别条件 $c$，定义逐样本损失：

$$\ell(\mathbf{x}, c; t_s, \epsilon_s) = \|\epsilon_s - \epsilon_\theta(\mathbf{x}_{t_s}, c, t_s)\|_2^2$$

通过 $S$ 个蒙特卡洛样本聚合类别得分并取最小得分类别作为预测：

$$\widehat{L}(\mathbf{x}, c) = \frac{1}{S} \sum_{s=1}^S \ell(\mathbf{x}, c; t_s, \epsilon_s), \quad \widehat{y}(\mathbf{x}) = \arg\min_{c \in \mathcal{C}} \widehat{L}(\mathbf{x}, c)$$

该协议要求压缩操作在时间步间独立、无缓存，以确保蒙特卡洛估计的无偏性。

### 3.2 令牌压缩框架

BiGain 将令牌压缩形式化为通用的合并-处理-解合并管线：

$$\mathbf{X} \xrightarrow{\tilde{\mathbf{X}} = M\mathbf{X}} \mathbf{Z} = F(\tilde{\mathbf{X}}) \xrightarrow{\tilde{\mathbf{X}} = U\mathbf{Z}} \tilde{\mathbf{X}} \in \mathbb{R}^{N \times d}$$

其中 $M$ 为合并算子（减少令牌数），$F$ 为 Transformer 块的前向计算，$U$ 为解合并算子（恢复原始空间分辨率）。BiGain 包含两个训练无关、即插即用的频率感知算子：(i) 拉普拉斯门控令牌合并（L-GTM / BiGain_TM），(ii) 插值-外推 KV 下采样（IE-KVD / BiGain_TD）。二者的核心设计原则是**平衡频谱保留**：保留高频细节（边缘、纹理）与低频/中频内容（形状、布局、语义），在生成保真度与判别效用之间取得最优权衡。两个算子均避免跨时间步缓存，与扩散分类器的蒙特卡洛估计协议完全兼容。

### 3.3 拉普拉斯门控令牌合并（L-GTM）

**核心动机**：现有令牌合并方法（如 ToMe 的余弦相似度贪婪合并）仅关注生成质量，在高合并率下会破坏类判别结构（如物体边缘），导致分类准确率崩溃。L-GTM 将特征映射至频率感知表示，引导合并在平滑（低频）区域进行，同时保护高频细节令牌。

**频率分数计算**：对隐藏状态令牌 $\mathbf{X}$，通过 2-D 拉普拉斯滤波器 $L$ 计算每个空间位置的局部频率幅度：

$$\mathbf{F} = \operatorname{Reduce}_c\left(\left| X * L \right|\right), \quad L = \begin{bmatrix} 0 & 1 & 0 \\ 1 & -4 & 1 \\ 0 & 1 & 0 \end{bmatrix}$$

其中 $*$ 表示空间卷积，$\operatorname{Reduce}_c$ 沿通道维度求和，$\mathbf{F} \in \mathbb{R}^{N}$ 为每个令牌的标量频率分数。分数越低表示令牌位于平滑区域，越适合作为合并目的地；分数越高表示令牌携带边缘/纹理等高频信息，应被保留。

**合并流程**：在空间步长内，选择频率分数最低的令牌作为目的地令牌，其余令牌构成源集合。通过全局二分图匹配，将源令牌与目的地令牌配对合并。合并后通过解合并操作恢复原始分辨率，确保后续层可继续访问完整空间结构。

**快速变体**：
- **自适应块合并（ABM）**：按块聚合频率分数，直接合并整个低频块，避免逐令牌匹配，在高分辨率阶段额外加速。
- **缓存赋值合并**：在 U-Net 最高分辨率阶段的第一注意力块计算合并/解合并映射并复用，减少重复计算开销。

### 3.4 插值-外推 KV 下采样（IE-KVD）

**核心动机**：现有令牌下采样方法（如 ToDo 的最近邻下采样、平均池化）在降低计算量的同时会丢失判别信息。IE-KVD 通过可控的线性组合在下采样的键（K）和值（V）中保留平衡频谱，同时保持查询（Q）的全分辨率以维持精确定位能力。

**下采样算子**：对特征图 $\mathbf{Z}$，定义下采样算子 $\mathcal{D}_{\alpha, s}$：

$$\mathcal{D}_{\alpha, s}(Z)[i] = \alpha Z[\mathrm{nearest}(i)] + (1-\alpha) \frac{1}{|\mathcal{N}_s(i)|} \sum_{j \in \mathcal{N}_s(i)} Z[j]$$

其中 $s$ 为下采样因子，$\mathcal{N}_s(i)$ 为位置 $i$ 的局部邻域，$\alpha \in [0, 1]$ 为插值-外推因子。当 $\alpha = 1$ 时退化为最近邻下采样（保留高频）；当 $\alpha = 0$ 时退化为平均池化（保留低频）。通过调节 $\alpha$ 可在高频细节与低频语义之间灵活权衡。

**注意力计算**：在自注意力层中，仅对键 $K$ 和值 $V$ 应用 $\mathcal{D}_{\alpha, s}$，查询 $Q$ 保持全分辨率：

$$Q_{\text{full}}, \quad K_{\downarrow} = \mathcal{D}_{\alpha, s}(K), \quad V_{\downarrow} = \mathcal{D}_{\alpha, s}(V)$$

这使注意力计算量从 $O(N^2)$ 降至 $O(N \cdot N/s^2)$，同时保留查询的细粒度定位能力。消融实验表明 $\alpha \in [0.8, 1.0]$ 时分类准确性最强；生成任务中采用线性时间步调度（早期步 $\alpha$ 较低以保留低频语义，后期步 $\alpha$ 较高以保留高频细节）可获得鲁棒的 FID 表现。

![[assets/figures/papers/paper_list_l841_https_arxiv_org_abs_2603_12240/figures/012_Figure_6.jpg]]
*Figure 6: Comparison of token merging schemes. Left: ToMe [4]; Right: Our BiGainTM. Merging is applied with a merge ratio 90% at the highest-resolution latent layer of the U-Net transformer in Stable Diffusion 2.0 at denoising step t = 200. Grayscale indicates merged tokens*

## 实验与关键发现

### 核心发现：频率感知压缩实现生成与判别的双重增益

BiGain 的核心主张——通过频谱平衡保留同时提升压缩扩散模型的生成质量与分类准确率——在多项基准上得到一致验证。在 ImageNet-1K 上使用 Stable Diffusion 2.0 骨干、70% 令牌合并率下，BiGain_TM 将分类准确率提高 **7.15%**（从 37.35% 提升至 44.50%），同时生成 FID 改善 **0.34**（1.85%）（Table 4；Abstract）。这一“双赢”现象打破了现有加速方法（如 ToMe、ToDo）仅优化生成而牺牲判别的固有瓶颈。

![[assets/figures/papers/paper_list_l841_https_arxiv_org_abs_2603_12240/figures/008_Table_4.jpg]]
*Table 4: SD-2.0 Token Merging: Classification (Acc@1 on Pets, ImageNet-100/1K; Acc@1 and mAP on COCO-2017) and generation fidelity (FID ↓) vs. Token Merging Ratio*

### 分类准确率：大幅缩小与未压缩模型的差距

**令牌合并场景**（Table 1, Table 4）：在 Oxford-IIIT Pets 数据集上，控制 FLOPs 减少约 10%，BiGain_TM 保留 **78.38%** Top-1 准确率（仅比未压缩基线下降 2.65%），而 ToMe 仅保留 72.96%（下降 8.07%），BiGain_TM 将准确率损失削减了 **27%～78%**。在更具挑战性的 ImageNet-1K 子集（2000 张图像）上，70% 合并率下 BiGain_TM 达到 44.50%，显著优于 ToMe 的 37.35%（Table 14 验证了子集稳健性，95% Wilson 置信区间排除偶然波动）。在 COCO-2017 多标签场景下，BiGain_TM 在 Acc@1 和 mAP 上同样全面领先（Table 4）。

**令牌下采样场景**（Table 1, Table 2, Table 3）：在 14.2% FLOPs 减少下，BiGain_TD 在 Oxford-IIIT Pets 上达到 **79.90%**（仅下降 1.13%），优于 ToDo 的 79.15%。在 ImageNet-100 上使用 DiT-XL/2 骨干、2× 下采样时，BiGain_TD 达到 **78.42%**，远超 ToDo 的 69.34%，提升幅度达 **9.08%**（Table 3）。COCO-2017 上 BiGain_TD 同样在 Acc@1（72.04% vs. 71.66%）和 mAP（46.97 vs. 46.59）上小幅领先（Table 2）。

### 生成质量：维持甚至改善 FID

BiGain 在生成质量上未付出代价，反而在某些设置下略微改善。SD-2.0 令牌合并下，BiGain_TM 在各合并率（30%～70%）下的 FID 与 ToMe 持平或略优（Table 4）。令牌下采样下，BiGain_TD 的 FID 在多数设置下优于 ToDo 和 Avg-pooling（Table 2, Table 3）。定性可视化（Figure 3, Figure 4）显示，BiGain 在高压缩率下仍能保持图像结构完整性，而基线方法出现明显退化。

![[assets/figures/papers/paper_list_l841_https_arxiv_org_abs_2603_12240/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparison of*

![[assets/figures/papers/paper_list_l841_https_arxiv_org_abs_2603_12240/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison of*

### 消融实验：验证频率感知设计的必要性

**令牌评分启发式**（Table 8）：拉普拉斯滤波器（ℓ₁）作为令牌评分在所有合并率下均优于全局统计量（均值偏离、ℓ₁/ℓ₂ 范数）、信道方差、频谱 DFT 和余弦相似度。这直接验证了局部频率感知引导是分类性能提升的关键——全局或频谱度量无法有效区分高频判别信息与低频冗余。

**频率基 KV 选择**（Table 12）：在 ImageNet-100 上，若仅保留低频令牌（最高拉普拉斯分数），Acc@1 崩溃至 **45.58%**；仅保留高频令牌，Acc@1 仅 **26.56%**。这确证了“平衡频谱保留”的必要性——单纯偏向任何一端都会严重损害分类能力。

**合并位置**（Table 6）：仅将令牌合并应用于自注意力层（SA）获得最佳质量-效率权衡。引入交叉注意力（CA）或 MLP 压缩会损害提示保真度或引入额外偏差。

**IE-KVD 参数敏感性**（Table 15, Table 16）：插值-外推因子 α 在 [0.8, 1.0] 范围内分类准确性最强；生成 FID 对线性时间步调度（从早期偏低频到后期偏高频）表现鲁棒。

### 加速变体与效率分析

BiGain 提供两种快速变体以进一步降低计算开销（Table 7）：自适应块合并（ABM）按块聚合频率分数，直接合并整个低频块，避免逐令牌匹配；缓存赋值合并在 U-Net 最高分辨率阶段复用合并/解合并映射。在 70% 合并率下，标准拉普拉斯合并、缓存赋值和 ABM 的 GFLOPs 分别为 51.3、50.8 和 49.5（Table 7），实际推理时间测量（Table 11, Table 18）确认了加速效果。

### 失败模式与局限

1. **模块联合使用的非叠加性**（Table 17）：L-GTM 与 IE-KVD 联合使用在 Pets 数据集上未超越最佳单模块设置，增益非叠加，需要手动选择适用模块。
2. **极高压缩率下的退化**：在 90% 合并率下，生成质量仍会出现可见退化（Figure 6 显示 ToMe 在此设置下丢失主要结构，BiGain_TM 保留更多但并非完美）。
3. **跨骨干泛化**：当前评估限于 U-Net（SD-2.0）和 DiT-XL/2，尚未在视频扩散或更大型基础模型上验证（需人工确认）。
4. **超参数依赖**：α、合并率 r、下采样系数 s 需根据任务和模型手动调整，缺乏自动化选择机制。

![[assets/figures/papers/paper_list_l841_https_arxiv_org_abs_2603_12240/figures/010_Table_6.jpg]]
*Table 6: Ablation of token-merging locations in Stable Diffusion 2.0 on Pets. Self-Attention (SA) is always merged; Cross-Attention (CA) and MLP are toggled. Results reported at merge ratios*

## 定位与知识库关联

### 核心问题定位：扩散模型加速中的“判别-生成”失衡

BiGain 针对的是一个此前被忽视的关键瓶颈：现有扩散模型加速方法（如 ToMe、ToDo）在设计时仅以生成质量（FID）为优化目标，完全忽略了模型的潜在判别能力。当这些方法应用于扩散分类器（diffusion classifier）时，分类准确率出现灾难性下降——例如在 COCO-2017 上，基线方法的准确率在压缩后崩坏，而生成视觉质量仍可接受（见 Figure 2）。这一现象揭示了一个深层矛盾：**生成保真度与判别效用在令牌压缩中并非同构优化目标**。

BiGain 的因果调节旋钮是**频率感知的令牌保留策略**：通过拉普拉斯滤波器计算局部频率幅度，引导令牌合并在平滑（低频）区域优先进行，同时保护承载边缘/纹理的高频令牌；在注意力下采样中通过可控插值-外推保留查询分辨率，从而平衡高频细节与低频语义。其核心洞察在于将特征映射至频率感知表示，解耦高频细节（边缘、纹理）与低频/中频内容（形状、布局、语义），通过**平衡频谱保留**实现兼顾生成保真度与判别效用的压缩——合并低频冗余、保留高频判别信息。

### 基线方法谱系与差异化定位

BiGain 在令牌压缩方法谱系中占据了一个独特位置：它是首个**同时以生成质量和判别准确率为联合优化目标**的训练无关压缩框架。以下从两个技术路线梳理其与基线工作的关系。

#### 令牌合并路线（Token Merging）

- **ToMe**（Bolya et al., 2023）：基于余弦相似度的贪婪令牌合并，是当前令牌合并的事实标准。其核心假设是相似令牌可无差别合并，但这导致高频判别结构（如物体边缘）被错误融合，在扩散分类场景下准确率严重退化。在 Oxford-IIIT Pets 上同等 FLOPs 减少下，ToMe 仅保留 72.96% Top-1 准确率，而 BiGain_TM 保留 78.38%，将准确率损失降低 27–78%（Table 1）。
- **SiTo**：令牌合并/修剪方法，具体技术细节需手动核实，但论文将其作为对比基线，BiGain_TM 在同等条件下显著优于该方法。

BiGain_TM 的差异化在于引入**拉普拉斯门控机制**（L-GTM）：通过 2-D 拉普拉斯滤波器计算频率分数，仅合并在低频区域并通过二分图匹配保留高频令牌（Eq. 7, Algorithm 2）。可视化证据（Figure 6）表明，在 90% 极高合并率下，拉普拉斯门控合并仍保留了猫的边缘等类判别结构，而 ToMe 导致主要结构丢失。

#### 令牌下采样路线（Token Downsampling）

- **ToDo**（Smith et al., 2024?）：采用最近邻下采样策略，是令牌下采样的代表性方法。在 Oxford-IIIT Pets 上 14.2% FLOPs 减少下，ToDo 达到 79.15% Acc@1；BiGain_TD 达到 79.90%，提升 0.75 个百分点（Table 1）。在 ImageNet-100（DiT-XL/2, 2× 下采样）上差距更为显著：BiGain_TD 78.42% vs. ToDo 69.34%，提升 9.08 个百分点（Table 3）。
- **Avg-pooling**：平均池化下采样基线，BiGain_TD 在所有设置下均优于该方法。

BiGain_TD 的差异化在于**插值-外推 KV 下采样**（IE-KVD）：通过可控参数 α 混合最近邻与平均池化（Eq. 8），保持查询（Q）全分辨率以保留精确定位能力，仅下采样键（K）和值（V）（Algorithm 4）。α 在 [0.8, 1.0] 范围内分类准确性最强（Table 15）；生成 FID 对线性时间步调度鲁棒（Table 16）。

#### 模型修剪路线

- **DiP-GO**（Zhu et al., 2024?）、**MosaicDiff**：属于模型结构修剪方法，与令牌压缩正交。BiGain 作为训练无关的即插即用框架，可与这些方法互补使用。

### 技术贡献的边界与适用条件

#### 适用边界

1. **骨干架构**：当前验证限于 U-Net（Stable Diffusion 2.0）和 DiT（DiT-XL/2）两类骨干，尚未在视频扩散模型或更大型基础模型上验证。
2. **任务范围**：分类任务依赖类条件扩散分类器协议（Eq. 3–4），采用蒙特卡洛估计器聚合多时间步噪声样本得分；未考虑细粒度分类或少样本场景。
3. **压缩调度**：采用时间步局部、无缓存、确定性压缩策略（Section 3.3），避免跨时间步缓存以适配扩散分类器的蒙特卡洛估计器——这是与部分现有加速方法的关键架构差异。

#### 已知局限

1. **模块联合使用的非叠加性**：L-GTM 与 IE-KVD 联合使用兼容但增益非叠加，未超越最佳单模块设置（Table 17），需手动选择适用模块。
2. **极高压缩率下的退化**：在 90% 合并率下生成质量仍出现可见退化，但退化程度显著优于基线方法（Figure 6）。
3. **超参数敏感性**：α、合并率 r、下采样系数 s 需根据任务和模型手动调整，缺乏自动化选择机制。
4. **额外计算开销**：拉普拉斯频率分数计算引入额外开销（Table 11, Table 18 提供了实际推理时间对比），在实时部署中的可接受性需进一步评估。

### 消融实验的关键因果验证

以下消融实验为 BiGain 的设计决策提供了强因果证据：

- **频率评分函数的选择**：拉普拉斯滤波器（ℓ₁）作为令牌评分在所有合并率下均优于全局统计量、频谱 DFT 和余弦相似度（Table 8），验证了局部频率感知设计的必要性。
- **频谱平衡的必要性**：频率感知 KV 选择实验证明，仅保留高频或低频令牌均严重损害分类——Acc@1 分别降至 26.56% 和 45.58%（Table 12），验证了平衡频谱保留的核心设计规则。
- **压缩位置的优化**：仅将令牌合并应用于自注意力层（SA）获得最佳质量-效率权衡；引入交叉注意力或 MLP 压缩会损害提示保真度或引入偏差（Table 6）。

### 开放问题与未来方向

1. **自适应压缩调度**：如何根据输入图像内容动态选择最优合并率和下采样系数，替代当前的手动调参？
2. **跨架构迁移**：频率感知压缩原理是否可迁移到自回归 Transformer、Flow Matching 等生成式架构，或视频生成任务？
3. **规模化验证**：在更大规模、更少类别的设置下，平衡频谱保留规则是否仍能保持双重收益？
4. **学习型压缩融合**：能否将拉普拉斯门控与学习型压缩结合，实现端到端的自适应频率感知压缩？
5. **实时部署优化**：频率分数计算的额外开销在实时场景中是否可接受？是否需要高效近似算法（如 Adaptive Block Merging 和 Cached Assignment Merge 的进一步优化）？

### 知识库定位总结

BiGain 在扩散模型压缩研究中的定位可概括为：**首次将“判别-生成联合优化”引入训练无关令牌压缩，通过频率感知机制填补了现有方法在判别能力保留上的空白**。其技术贡献不是对现有合并/下采样算子的替代，而是为这些算子引入了**频谱感知的门控机制**，从而在不牺牲生成质量的前提下显著提升判别效用。这一思路为扩散模型在统一生成与理解任务中的应用提供了新的技术路径。

## 原文 PDF

![[paperPDFs/CVPR_2026/BiGain_Unified_Token_Compression_for_Joint_Generation_and_Classification.pdf]]
