---
title: "LinVideo: A Post-Training Framework towards O(n) Attention in Efficient Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LinVideo_A_Post_Training_Framework_towards_O_n_Attention_in_Efficient_Video_Generation.pdf
project_link: null
code_link: null
aliases:
- LinVideo
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 通过可学习参数量化每个注意力层的线性化适宜性（选择性转移），并在训练中引入跨任意采样时刻的分布匹配目标（ADM），可控制模型在保持生成质量的前提下最大化线性注意力替换比例。
primary_logic: 不同深度的注意力层对线性化替换的敏感性存在显著差异，浅层替换更容易被后续层优化补偿；通过将层选择建模为二分类问题并动态分配线性注意力比例，同时匹配原始模型在采样轨迹上任意时刻的分布，可以在无需原始数据集的情况下几乎无损地将大量自注意力模块替换为线性注意力，实现大幅度加速。
claims:
- Figure 2 显示，相同数量层替换时，浅层线性化比深层线性化性能提升显著（Subject Consistency +2.86, Image Quality +6.31），且第一层替换导致严重性能下降。
- Table 1 表明 LINVIDEO 在 Wan 1.3B/14B 上分别取得 1.43×/1.71× 加速，且所有 VBench 质量指标均匹配或超过 FlashAttention2 基准。
- 消融实验证实选择性转移策略显著优于手动选择和启发式搜索，ADM 损失在效率和性能上明显优于 MSE 和 DMD 损失。
- VBench 上 Latency (s) / Speedup = 68.26 / 1.43× (Wan 1.3B)
---

# LinVideo: A Post-Training Framework towards O(n) Attention in Efficient Video Generation

> [!tip] 核心洞察
> 不同深度的注意力层对线性化替换的敏感性存在显著差异，浅层替换更容易被后续层优化补偿；通过将层选择建模为二分类问题并动态分配线性注意力比例，同时匹配原始模型在采样轨迹上任意时刻的分布，可以在无需原始数据集的情况下几乎无损地将大量自注意力模块替换为线性注意力，实现大幅度加速。

| 字段 | 内容 |
|------|------|
| 中文题名 | LinVideo: 一种面向O(n)注意力的高效视频生成后训练框架 |
| 英文题名 | LinVideo: A Post-Training Framework towards O(n) Attention in Efficient Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.08318) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | LINVIDEO |
| Dataset | VBench, VBench-2.0 |

> [!tip] 效果简介
> - VBench 上，Latency (s) / Speedup 68.26 / 1.43× (Wan 1.3B) vs 97.32 / 1.00× (FA2, Wan 1.3B) (1.43×)；Latency (s) / Speedup 1127 / 1.71× (Wan 14B) vs 1931 / 1.00× (FA2, Wan 14B) (1.71×)；Overall Consistency 26.52 (Wan 1.3B) vs 26.18 (FA2, Wan 1.3B) (+0.34)。
> - VBench-2.0 上，Total Score (Wan 1.3B) 56.74 (LINVIDEO) vs 56.74 (FA2) (0 (持平))；Total Score (Wan 14B) 59.62 (LINVIDEO) vs 59.85 (FA2) (-0.23)。
> - VBench (4-step distilled) 上，Latency / Speedup 6.11 / 15.9× (Wan 1.3B) vs 8.76 / 1.00× (FA2+DMD2, Wan 1.3B) (15.9×)。

## 概述

视频扩散模型已成为视觉内容生成的核心技术，但其核心组件——全序列自注意力——的计算复杂度随序列长度呈平方增长（$\mathcal{O}(n^2)$），导致推理阶段计算开销巨大，严重制约了高分辨率、长时长视频的生成效率。直接以线性注意力（$\mathcal{O}(n)$）替代全部二次注意力，尽管在理论上可将复杂度降至线性，却因线性注意力的表示能力不足以及视频时空建模的高度复杂性，导致生成质量严重退化；同时，数据驱动的后训练微调往往难以恢复这一性能损失。

针对上述瓶颈，本文提出 **LINVIDEO**，一个高效的数据免费后训练框架。其核心思路并非简单地“全部替换”，而是通过两个关键机制实现质量与效率的最优权衡：

1.  **选择性转移（Selective Transfer）**：将“哪些层应被替换为线性注意力”建模为一个可学习的二分类问题。每个注意力层被赋予一个可学习参数 $r \in [0,1]$，通过混合注意力训练和专门的约束/正则化损失，模型能够自动、渐进地将指定数量的二次注意力层替换为线性注意力，且优先选择对线性化不敏感的浅层进行替换，从而将性能损失降至最低。
2.  **任意时刻分布匹配（Anytime Distribution Matching, ADM）**：不同于仅匹配最终输出的朴素均方误差（MSE）损失，ADM 目标旨在匹配训练模型与原始预训练模型在扩散采样轨迹上**任意时刻** $t$ 的样本分布。该方法利用当前模型自身的评分函数估计来高效计算 KL 散度的梯度，无需额外的多步扩散模型，在显著提升生成质量的同时保持了训练效率。

在方法谱系上，LINVIDEO 区别于 **FlashAttention2** 等密集注意力基线（保持二次复杂度），也不同于 **DFA**、**XAttn**、**SVG**、**SVG2** 等静态或动态稀疏注意力方法。它开创性地将层级别的注意力机制选择与分布匹配后训练相结合，为视频扩散模型的加速提供了一条无需原始训练数据的新路径。

实验结果表明，LINVIDEO 在 Wan 1.3B 和 14B 模型上分别实现了 **1.43×** 和 **1.71×** 的推理加速，同时在 VBench 基准上的所有质量指标均匹配甚至超越了 FlashAttention2 基线。进一步结合少步蒸馏技术，4 步模型可实现高达 **15.9×** 的极速推理，仅伴随微小的视觉质量下降。消融研究证实，选择性转移策略显著优于手动选择或启发式搜索，而 ADM 损失在性能和训练效率上均明显优于 MSE 和 DMD 损失。

## 背景与动机

### 视频扩散模型的注意力瓶颈

视频扩散模型（Video Diffusion Models, VDMs）已成为文本到视频生成领域的主导范式。与图像生成不同，视频生成需要同时建模空间细节和时间动态，这通常通过将视频潜在表示展平为长序列，并施加全序列自注意力（full-sequence self-attention）来实现。然而，标准 softmax 注意力的计算复杂度随序列长度 $n$ 呈二次增长，即 $\mathcal{O}(n^2)$。对于高分辨率、长时视频，$n$ 可达数万甚至数十万，导致单次推理的注意力计算开销占据主导地位，严重制约了实际部署效率。

### 现有加速方案的局限

针对该瓶颈，现有工作主要沿两条路径展开：

**稀疏注意力**通过丢弃部分 token 间的交互来降低计算量，例如 **DFA (DiTFastAttn)**、**XAttn**、**SVG (Sparse VideoGen)** 和 **SVG2 (Sparse VideoGen 2)** 等方法。这些方案在保持一定加速比的同时，通常需要针对特定视频形状或硬件定制稀疏模式，且丢弃信息不可避免地导致生成质量损失。

**线性注意力**则利用核函数特征映射，通过矩阵乘法的结合律将复杂度降至 $\mathcal{O}(n)$，具有更优的理论加速潜力。但一个关键挑战长期被忽视：**直接将全部二次注意力层替换为线性注意力会导致生成质量严重退化**。其根源在于，线性注意力的表示能力弱于 softmax 注意力，而视频生成的时空联合建模对注意力质量高度敏感，简单的全量替换难以通过常规微调恢复性能。

### 关键洞察：层对线性化替换的敏感性差异

本文揭示了决定上述困境的核心规律：**不同深度的注意力层对线性化替换的敏感性存在显著差异**。实验表明（见 Figure 2），在替换相同数量注意力层的前提下，浅层线性化比深层线性化带来更优的性能表现——在 Subject Consistency 上提升 +2.86，Image Quality 上提升 +6.31。更值得注意的是，第一层的替换会导致严重的性能崩溃，说明部分关键层必须保留二次注意力。这一发现暗示，**并非所有层都适合线性化，而是一个“选择性”问题**——关键在于自动识别哪些层可以被安全替换，而非盲目全量或手动指定。

### 后训练微调的另一重困境

即使确定了替换目标，如何在不访问原始训练数据的前提下恢复模型性能仍是一个难题。预训练视频扩散模型的训练数据通常规模庞大且不公开，使得数据驱动的微调不可行。简单的输出 MSE 匹配（Eq. 7）虽可实现无数据微调，但容易导致生成样本出现严重的时序抖动（temporal jitter），无法有效恢复生成质量（见 Figure II）。

### 本文动机与核心思路

基于上述分析，本文聚焦一个核心问题：**能否通过高效的后训练框架，在不依赖原始数据的前提下，将尽可能多的二次注意力层替换为线性注意力，实现显著推理加速的同时保持生成质量无损？**

为此，本文提出 **LINVIDEO**，一个无数据的后训练框架，其核心包含两个协同组件：

1. **选择性转移（Selective Transfer）**：将层选择建模为二分类问题，为每个注意力层引入可学习参数 $r \in [0,1]$，通过混合注意力和约束/正则化损失，自动、渐进地将指定数量的 softmax 注意力层替换为线性注意力，最小化性能损失。

2. **任意时刻分布匹配（Anytime Distribution Matching, ADM）**：在采样轨迹上跨任意时刻 $t$ 匹配训练模型与原始模型的样本分布，利用当前模型自身的评分函数估计，无需额外多步扩散模型，实现高效且有效的分布对齐。

## 核心创新

### 瓶颈与动机

视频扩散模型中的全序列自注意力是推理计算的主要瓶颈，其时间复杂度为 $\mathcal{O}(n^2)$，其中 $n$ 为序列长度。直接以线性注意力（$\mathcal{O}(n)$）替换全部二次注意力模块看似可行，但面临两个根本性困难：（1）线性注意力与 softmax 注意力之间存在显著的表示能力差距；（2）视频生成的时空建模高度复杂，直接替换会导致生成质量严重退化，且数据驱动的后训练微调难以恢复性能。

### 关键洞察：层的线性化敏感性存在显著差异

LINVIDEO 的核心发现是：**不同深度的注意力层对线性化替换的敏感性存在本质差异**。如 Figure 2 所示，在相同数量的层被替换为线性注意力时，浅层线性化比深层线性化带来显著更高的性能恢复（Subject Consistency +2.86, Image Quality +6.31），而第一层的替换则导致严重的性能崩溃。这一现象揭示了浅层替换更容易被后续层的优化过程所补偿，为选择性替换策略提供了理论依据。

### 创新一：选择性转移（Selective Transfer）

基于上述洞察，LINVIDEO 将层选择建模为一个可学习的二分类问题。具体而言：

- **可学习参数** $r^{(l)} \in [0,1]$：为每个注意力层引入一个标量参数，通过混合注意力机制加权融合二次注意力和线性注意力：

$$o_i = r \sum_{j=1}^{n} \frac{\exp(\frac{q_i k_j^\top}{d})}{\sum_{j=1}^{n} \exp(\frac{q_i k_j^\top}{d})} v_j + (1-r) \frac{\phi(\pmb{q}_i)(\sum_{j=1}^{n} \phi(\pmb{k}_j)^\top \pmb{v}_j)}{\phi(\pmb{q}_i)(\sum_{j=1}^{n} \phi(\pmb{k}_j)^\top)}$$

- **约束损失** $\mathcal{L}_{\mathrm{con}} = \big( \sum_{l=1}^{N} \lceil r^{(l)} \rfloor - \mathrm{target} \big)^2$：强制替换层数达到目标数量。
- **正则化损失** $\mathcal{L}_{\mathrm{reg}} = \sum_{l=1}^{N} \big( 1 - |2 r^{(l)} - 1|^{\alpha} \big)$：推动 $r$ 向 0 或 1 收敛，其中 $\alpha$ 采用动态衰减策略（20→2），在训练初期允许 $r$ 灵活调整，后期强制二值化。

这一机制使得模型能够**自动且渐进地**选择最适合线性化的层，无需人工设计或启发式搜索。消融实验（Table 3）证实，选择性转移策略在所有 VBench 指标上均显著优于手动选择和启发式搜索，且移除正则化损失 $\mathcal{L}_{\mathrm{reg}}$ 会导致性能崩溃（Overall Consistency 仅 1.42），说明正则化对训练稳定性至关重要。

### 创新二：任意时刻分布匹配（Anytime Distribution Matching, ADM）

传统后训练方法通常仅匹配最终输出（如 MSE 损失 $\mathbb{E}[||\hat{\mathbf{x}}_0 - \mathbf{x}_0||^2]$），忽略了采样轨迹中间时刻的分布偏移。LINVIDEO 提出 ADM 目标，匹配训练模型与原始模型在**任意采样时刻** $t \in [0,1]$ 的样本分布：

$$\mathcal{L}_{\mathrm{ADM}} = \mathbb{E}_{\hat{\mathbf{x}}_t \sim q_t} \bigg[ \log \frac{q_t(\hat{\mathbf{x}}_t)}{p_t(\hat{\mathbf{x}}_t)} \bigg]$$

该目标的梯度可简化为利用当前模型自身评分函数估计的形式：

$$\frac{\partial \mathcal{L}_{\mathrm{ADM}}}{\partial \theta} = \mathbb{E}_{\hat{\mathbf{x}}_t \sim q_t} \left[ -\left( s_t(\hat{\mathbf{x}}_t) - \hat{s}_t(\hat{\mathbf{x}}_t) \right) \frac{\partial \hat{\mathbf{x}}_t}{\partial \hat{\mathbf{u}}_\theta} \frac{\partial \hat{\mathbf{u}}_\theta}{\partial \theta} \right]$$

其中评分差在整流流模型设定下可进一步简化为仅依赖模型输出差：

$$s_t(\hat{\mathbf{x}}_t) - \hat{s}_t(\hat{\mathbf{x}}_t) = -\frac{1-t}{t} \left( \pmb{u}_\theta(\hat{\mathbf{x}}_t) - \hat{\pmb{u}}_\theta(\hat{\mathbf{x}}_t) \right)$$

ADM 的核心优势在于：（1）无需额外多步扩散模型来估计评分函数，训练效率高；（2）通过匹配完整采样轨迹的分布，有效抑制了线性化引入的时序抖动。消融实验（Table 4, Figure 6）表明，ADM 在性能和训练效率上均显著优于 naive MSE 和 DMD 损失，训练速度比 DMD 快约 4.4 倍。

### 与 Baseline 的核心差异

| 维度 | 基线方法 | LINVIDEO |
|------|----------|----------|
| **注意力计算类型** | 全部层使用 softmax 注意力（$\mathcal{O}(n^2)$） | 部分层替换为 Hedgehog 线性注意力（$\mathcal{O}(n)$），具体层由可学习参数 $r$ 选择 |
| **层选择策略** | 无选择机制（全部 softmax） | 可学习二分类，自动且渐进地选择线性化层 |
| **后训练损失函数** | 简单输出 MSE 匹配 | ADM 损失，匹配任意时刻 $t$ 的样本分布 |

### 方法局限性

- 方法依赖原始预训练模型进行数据采集，虽无需外部数据集，但需离线生成大量样本，消耗一定计算资源和存储。
- 当 target 替换层数过大时（>18 层），性能退化较快，界限受模型容量和任务复杂度影响。
- ADM 目标的推导依赖整流流模型假设，对其他扩散框架（如 DDPM）的适用性尚未验证。
- 线性注意力加速目前基于 PyTorch 通用实现，相比专用 CUDA kernel 仍有优化空间。

## 整体框架

LINVIDEO 是一个**无数据后训练框架**，其核心目标是在不访问原始训练数据的前提下，将预训练视频扩散模型中尽可能多的二次复杂度自注意力模块替换为线性注意力，从而在保持生成质量的同时实现推理加速。整个 pipeline 由三个关键阶段构成：**数据准备**、**选择性转移**与**Anytime Distribution Matching (ADM) 训练**，最后可选的**加速蒸馏**进一步压缩采样步数。

### 数据准备：无数据微调的基石

框架的起点是一个已训练好的视频扩散模型（如 Wan 1.3B/14B）。数据准备阶段从该模型的采样轨迹中收集大量 $(\mathbf{x}_t, \mathbf{u}_t)$ 对作为训练集，其中 $\mathbf{x}_t$ 为带噪潜在视频变量，$\mathbf{u}_t$ 为原始模型在相应时刻的预测输出。这一策略使整个后训练过程完全摆脱对原始数据集的依赖，仅需利用预训练模型自身的生成能力即可构建训练信号。

### 选择性转移：自动层选择与渐进替换

选择性转移模块负责回答一个核心问题：**哪些注意力层应该被替换为线性注意力？** 其工作机制如下：

1. **混合注意力参数化**：为每个注意力层引入一个可学习标量 $r \in [0, 1]$，该层的实际注意力输出为二次注意力与线性注意力的加权混合（见 Eq. (8)）。当 $r=1$ 时完全使用二次注意力，$r=0$ 时完全使用线性注意力。

2. **约束与正则化驱动收敛**：约束损失 $\mathcal{L}_{\mathrm{con}}$ 强制所有层的 $r$ 值之和达到预设的目标替换层数 `target`（见 Eq. (9)）；正则化损失 $\mathcal{L}_{\mathrm{reg}}$ 则推动每个 $r$ 向 0 或 1 收敛，避免停留在中间态（见 Eq. (10)）。其中正则项采用动态衰减的 $\alpha$ 参数（如 20→2），在训练初期允许 $r$ 灵活探索，后期强制其二值化。

3. **自动发现层敏感性**：训练过程中，模型根据各层对线性化替换的适应能力自动分配 $r$ 值。实验表明（Figure 2），浅层替换后性能恢复更为容易，而深层替换对质量影响更大——选择性转移正是通过学习这一敏感性分布来实现最优的层选择。

### Anytime Distribution Matching：恢复生成性能

仅替换注意力层会导致新模型与原始模型在采样轨迹上的分布产生偏移，直接使用简单的输出 MSE 匹配难以有效恢复生成质量。ADM 模块通过最小化新模型分布 $p_t$ 与原始模型分布 $q_t$ 在**任意采样时刻 $t$** 上的 KL 散度来解决这一问题（见 Eq. (11)）。其关键设计在于：利用当前模型自身的评分函数估计来近似分布差异，无需额外的多步扩散模型参与计算，从而在保证训练效率的同时实现有效的分布对齐（见 Eq. (12)(13)）。

### 训练循环与可选蒸馏

最终训练目标将 ADM 损失与选择性转移的约束/正则化损失组合为 $\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{ADM}} + \lambda (\mathcal{L}_{\mathrm{con}} + \mathcal{L}_{\mathrm{reg}})$（见 Eq. (14)），联合优化模型参数与层选择参数 $r$。训练完成后，所有 $r$ 被二值化为 0 或 1，得到部分层使用线性注意力的加速模型。

在此之上，框架支持可选的**加速蒸馏**阶段：将 LINVIDEO 微调后的模型进一步应用 DMD2 少步蒸馏，可获得 4 步极速模型。消融实验证实（Table II），将选择性转移与蒸馏合并为单阶段训练会导致性能崩溃，而两阶段策略（先 LINVIDEO 后 DMD2）则稳定有效，在 Wan 1.3B 上实现 15.9× 加速，在 Wan 14B 上实现 20.9× 加速。

### 整体数据流

```
预训练视频DM → [采样轨迹收集] → (x_t, u_t) 训练集
                                    ↓
              [选择性转移] ← 混合注意力 + L_con + L_reg
                    ↓
              [ADM训练] ← KL散度最小化
                    ↓
              LINVIDEO模型 (部分层线性注意力)
                    ↓ (可选)
              [DMD2蒸馏] → 4步极速模型
```

整个框架在 Wan 1.3B 上实现 1.43× 加速，在 Wan 14B 上实现 1.71× 加速，且 VBench 质量指标与 FlashAttention2 密集注意力基线持平或略有提升（Table 1），验证了该 pipeline 在质量-效率权衡上的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l895_https_arxiv_org_abs_2510_08318/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed efficient data-free post-training framework, LINVIDEO. (a) This framework first applies selective transfer (Sec. 4.1), which assigns each layer a learnable score r and progressively, automatically replaces quadratic attention with linear attention while minimizing the resulting performance drop. This process also combines with*

## 核心模块与公式推导

### 问题形式化与注意力瓶颈

视频扩散模型的前向过程遵循标准噪声调度：

$$ \mathbf{x}_t = \alpha_t \mathbf{x}_0 + \sigma_t \mathbf{\epsilon} \tag{1} $$

其中 $\mathbf{x}_0$ 为干净潜在视频变量，$\mathbf{\epsilon} \sim \mathcal{N}(0, \mathbf{I})$ 为标准高斯噪声。模型 $\mathbf{u}_\theta$ 在训练时以流匹配目标学习预测速度场，推理时通过常微分方程求解器从噪声逐步生成视频。核心计算瓶颈在于 DiT 架构中全序列自注意力的二次复杂度 $\mathcal{O}(n^2)$，其中 $n$ 为视频帧数与空间 token 数的乘积。

标准 softmax 注意力计算为：

$$ \pmb{o}_i = \sum_{j=1}^{n} \frac{\mathrm{sim}(\pmb{q}_i, \pmb{k}_j)}{\sum_{j=1}^{n} \mathrm{sim}(\pmb{q}_i, \pmb{k}_j)} \pmb{v}_j \tag{4} $$

其中相似度函数 $\mathrm{sim}(\pmb{q}_i, \pmb{k}_j) = \exp(\pmb{q}_i \pmb{k}_j^\top / \sqrt{d})$。直接以线性注意力替代全部二次注意力会导致表示能力差距与时空建模复杂性带来的严重质量退化，且数据驱动的后训练微调难以恢复性能（见 Figure 2 层敏感性证据）。

![[assets/figures/papers/paper_list_l895_https_arxiv_org_abs_2510_08318/figures/002_Figure_2.jpg]]
*Figure 2: Performance on 4 VBench [21] dimensions for partial linearized (10 adjacent layers for each dot) Wan 1.3B [49] after 2K-step fine-tuning. The index range of the layers replaced with linear attention is indicated in the tick label of the x-axis. “*” denotes models further fine-tuned for 3K additional steps*

### 线性注意力与 Hedgehog 核

线性注意力通过核特征映射 $\phi(\cdot)$ 将相似度计算分解，利用矩阵乘法结合律将复杂度降至 $\mathcal{O}(n)$：

$$ o_i = \frac{\phi(\pmb{q}_i) (\sum_{j=1}^{n} \phi(\pmb{k}_j)^\top \pmb{v}_j)}{\phi(\pmb{q}_i) (\sum_{j=1}^{n} \phi(\pmb{k}_j)^\top)} \tag{5} $$

LINVIDEO 采用 Hedgehog 核作为特征映射：

$$ \phi(\pmb{q}) = \mathrm{softmax}(\pmb{q} \widetilde{W}_q) \oplus \mathrm{softmax}(-\pmb{q} \widetilde{W}_q) \tag{6} $$

其中 $\widetilde{W}_q$ 为可学习投影矩阵，$\oplus$ 表示向量拼接。消融实验证实 Hedgehog 核在 VBench 得分上优于 ReLU 和 Taylor 展开核，且延迟相近。

### 选择性转移（Selective Transfer）

核心洞察：不同深度的注意力层对线性化替换的敏感性存在显著差异——浅层替换更容易被后续层优化补偿，而深层替换（尤其是第一层）会导致严重性能下降（Figure 2）。基于此，LINVIDEO 将层选择建模为可学习的二分类问题。

为每个注意力层引入可学习标量 $r^{(l)} \in [0, 1]$，通过混合注意力计算实现软切换：

$$ o_i = r \sum_{j=1}^{n} \frac{\exp(\frac{q_i k_j^\top}{d})}{\sum_{j=1}^{n} \exp(\frac{q_i k_j^\top}{d})} v_j + (1-r) \frac{\phi(\pmb{q}_i)(\sum_{j=1}^{n} \phi(\pmb{k}_j)^\top \pmb{v}_j)}{\phi(\pmb{q}_i)(\sum_{j=1}^{n} \phi(\pmb{k}_j)^\top)} \tag{8} $$

训练过程中，$r$ 从 1（全二次注意力）逐渐向 0（全线性注意力）收敛。两个辅助损失引导这一过程：

**约束损失** 强制替换层数达到目标数量 target：

$$ \mathcal{L}_{\mathrm{con}} = \Big( \sum_{l=1}^{N} \lceil r^{(l)} \rfloor - \mathrm{target} \Big)^2 \tag{9} $$

其中 $\lceil \cdot \rfloor$ 为四舍五入取整，$N$ 为注意力层总数。

**正则化损失** 推动 $r$ 向 0 或 1 两极收敛，避免停留在模糊的中间状态：

$$ \mathcal{L}_{\mathrm{reg}} = \sum_{l=1}^{N} \big( 1 - |2 r^{(l)} - 1|^{\alpha} \big) \tag{10} $$

参数 $\alpha$ 采用动态衰减策略（20 → 2）：训练初期较大的 $\alpha$ 允许 $r$ 灵活探索，后期较小的 $\alpha$ 强制 $r$ 向两端收敛。消融实验表明，移除 $\mathcal{L}_{\mathrm{reg}}$ 会导致 $r$ 大量停留在 0.5 附近（Figure 3），性能崩溃至 Overall Consistency 仅 1.42。

![[assets/figures/papers/paper_list_l895_https_arxiv_org_abs_2510_08318/figures/003_Figure_3.jpg]]
*Figure 3: Values of r across layers and training steps. “w/*

### Anytime Distribution Matching（ADM）

常规后训练方法仅匹配模型最终输出（如 MSE 损失），忽略了采样轨迹中间时刻的分布偏移。ADM 目标匹配训练模型 $p_t$ 与原始模型 $q_t$ 在任意时刻 $t \in [0, 1]$ 的样本分布，最小化 KL 散度：

$$ \mathcal{L}_{\mathrm{ADM}} = \mathbb{E}_{\hat{\mathbf{x}}_t \sim q_t} \bigg[ \log \frac{q_t(\hat{\mathbf{x}}_t)}{p_t(\hat{\mathbf{x}}_t)} \bigg] \tag{11} $$

其梯度可借助评分函数表达：

$$ \frac{\partial \mathcal{L}_{\mathrm{ADM}}}{\partial \theta} = \mathbb{E}_{\hat{\mathbf{x}}_t \sim q_t} \left[ -\left( s_t(\hat{\mathbf{x}}_t) - \hat{s}_t(\hat{\mathbf{x}}_t) \right) \frac{\partial \hat{\mathbf{x}}_t}{\partial \hat{\mathbf{u}}_\theta} \frac{\partial \hat{\mathbf{u}}_\theta}{\partial \theta} \right] \tag{12} $$

在整流流模型设定下，评分差可简化为仅依赖模型输出之差的形式，无需额外多步扩散模型：

$$ s_t(\hat{\mathbf{x}}_t) - \hat{s}_t(\hat{\mathbf{x}}_t) = -\frac{1-t}{t} \left( \pmb{u}_\theta(\hat{\mathbf{x}}_t) - \hat{\pmb{u}}_\theta(\hat{\mathbf{x}}_t) \right) \tag{13} $$

其中 $\pmb{u}_\theta$ 为原始模型输出，$\hat{\pmb{u}}_\theta$ 为训练中模型输出。这一设计使 ADM 在训练速度上比 DMD 损失快约 4.4 倍（Figure 6），同时在 VBench 性能上显著优于 naive MSE 和 DMD 损失。

### 总训练目标

完整的训练损失组合 ADM、约束和正则化三项：

$$ \mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{ADM}} + \lambda \big( \mathcal{L}_{\mathrm{con}} + \mathcal{L}_{\mathrm{reg}} \big) \tag{14} $$

其中 $\lambda$ 为平衡超参数。训练数据完全来自预训练模型的采样轨迹，无需访问原始数据集，实现了“无数据”后训练。

### 训练流程

1. **数据收集**：从预训练视频 DM 的采样轨迹中收集大量 $(\mathbf{x}_t, \mathbf{u}_t)$ 对。
2. **选择性转移训练**：在 ADM 损失、约束损失和正则化损失的联合指导下，学习每层的 $r^{(l)}$ 和模型参数，自动且渐进地将 target 个 softmax 注意力层替换为线性注意力。
3. **可选加速蒸馏**：在 LINVIDEO 微调后，可进一步应用 DMD2 少步蒸馏获得 4 步极速模型。消融实验证实两阶段策略（先 LINVIDEO 再 DMD2）稳定有效，而单阶段直接结合会导致性能崩溃。

### 补充图表

![[assets/figures/papers/paper_list_l895_https_arxiv_org_abs_2510_08318/figures/011_Figure.jpg]]
*Figure: I. Effect of α on 1 - | 2 $r ^ { ( l ) }$ - 1 | ^ ${ \alpha }$ of Eq. (10)*

## 实验与分析

### 核心瓶颈验证：层深度决定线性化敏感性

在将二次注意力替换为线性注意力时，不同深度的注意力层表现出截然不同的敏感性。**Figure 2** 展示了在 Wan 1.3B 模型上，将 10 个相邻注意力层替换为线性注意力后，经过 2000 步微调的 VBench 性能对比。实验揭示了两个关键规律：

1. **浅层替换优于深层替换**：当替换层位于浅层区域（如层 0-9）时，模型能够通过后续层的优化补偿表示能力的损失，在 Subject Consistency 上提升 +2.86，Image Quality 上提升 +6.31。相比之下，替换深层（如层 20-29）时性能恢复明显更差。
2. **第一层替换导致严重退化**：替换包含第 0 层的区间（层 0-9）时，即使经过额外 3000 步微调（图中 `*` 标记），性能仍显著低于替换其他区间。这表明第一层对线性化极为敏感，可能承担着关键的全局信息聚合功能。

这一发现构成了 LINVIDEO 选择性转移策略的核心动机：并非所有层都应被线性化，需要一种自动化的层选择机制来最大化线性化比例同时保持生成质量。

### 主实验结果：加速与质量的双重保障

**Table 1** 展示了 LINVIDEO 在 VBench 基准上的综合性能对比。在 Wan 1.3B 模型上，LINVIDEO 实现了 **1.43× 加速**（延迟从 97.32s 降至 68.26s），同时 Overall Consistency 从 26.18 提升至 26.52（+0.34），表明线性化后的模型在部分维度上甚至超越了原始密集注意力基线。在 Wan 14B 模型上，加速比进一步提升至 **1.71×**（延迟从 1931s 降至 1127s），Overall Consistency 仅微降 0.01（26.17 → 26.16），几乎无损。

与其他稀疏注意力方法的对比进一步凸显了 LINVIDEO 的优势：
- **DFA (DiTFastAttn)**、**XAttn**、**SVG** 和 **SVG2** 等静态或动态稀疏注意力基线在延迟和 VBench 得分上均不如 LINVIDEO。SVG2 作为最强的稀疏基线，在 Wan 1.3B 上的 Overall Consistency 仅为 25.92，显著低于 LINVIDEO 的 26.52。
- 在 **VBench-2.0** 更全面的评估框架下（**Figure 4**），LINVIDEO 同样表现出色：Wan 1.3B 上 Total Score 与 FA2 基线持平（均为 56.74），远超 SVG2 的 55.81；Wan 14B 上 Total Score 为 59.62，略低于 FA2 的 59.85（-0.23），但仍明显优于 SVG2 的 58.74。

![[assets/figures/papers/paper_list_l895_https_arxiv_org_abs_2510_08318/figures/005_Figure_4.jpg]]
*Figure 4: Performance comparison with baselines on VBench-2.0 [70]. For Wan 1.3B, the total scores are 56.74 (FA2), 55.81 (SVG2), 56.74 (LINVIDEO), and 55.51 (LINVIDEO+DMD2); for Wan 14B, the total scores are 59.85 (FA2), 58.74 (SVG2), 59.62 (LINVIDEO), and 58.22 (LINVIDEO+DMD2). FA2 denotes FlashAttention2 [5]*

当 LINVIDEO 与 DMD2 少步蒸馏结合时，加速效果达到极致：Wan 1.3B 上实现 **15.9× 加速**（延迟 6.11s），Wan 14B 上实现 **20.9× 加速**，且视觉质量仅轻微下降（**Figure III** 和 **Figure IV** 提供了 480p 和 720p 的生成样本直观对比，验证了加速模型在时序一致性和细节保真度上的可用性）。

### 消融实验：选择性转移与 ADM 的关键作用

#### 替换层数的影响

**Table 2** 展示了不同 `target`（目标替换层数）下的性能与加速比变化。当 `target` ≤ 18 时，模型性能保持稳定，各项 VBench 指标与全密集注意力基线接近；当 `target` 超过 18 后，性能开始显著退化。这一消融实验明确了 LINVIDEO 的有效操作边界：在 Wan 1.3B 上，18 层是线性化比例的安全上限，超出此界限后模型容量不足以补偿表示能力的损失。

#### 选择性转移 vs. 手动/启发式选择

**Table 3** 直接对比了三种层选择策略：
- **手动选择**：基于 Figure 2 的敏感性分析手动指定替换层
- **启发式搜索**：基于层间梯度或激活统计量的启发式规则
- **LINVIDEO 选择性转移**：通过可学习参数 `r` 自动学习最优替换方案

结果显示，LINVIDEO 的自动选择策略在所有 VBench 指标上均取得最高分。特别值得注意的是，**移除正则化损失 L_reg**（`w/o L_reg`）导致性能崩溃，Overall Consistency 仅剩 1.42。这验证了正则化损失对于推动 `r` 收敛到 0/1 二值解、避免混合注意力在推理阶段引入额外开销和表示模糊性的关键作用（**Figure 3** 可视化了有无正则化时 `r` 值的收敛行为差异）。

#### ADM 损失的优越性

**Table 4** 对比了不同训练损失函数的效果：
- **Naive MSE**：简单匹配模型输出的均方误差，导致严重时序抖动（**Figure II** 展示了相邻帧间的抖动现象）
- **DMD 损失**：基于分布匹配蒸馏的损失，性能优于 MSE 但仍不及 ADM
- **ADM 损失**：在 VBench 得分上全面领先，且训练效率显著更高

**Figure 6** 进一步揭示了训练效率差异：ADM 损失的训练速度比 DMD 快约 **4.4 倍**。这是因为 ADM 仅需单步采样和评分函数估计，而 DMD 需要多步扩散模型的 rollout 计算。

#### 核函数与训练策略消融

**Table VII** 对比了 Hedgehog、ReLU 和 Taylor 展开三种线性注意力核函数。Hedgehog 核在 VBench 得分上优于其他核函数，且延迟相近，验证了其作为 LINVIDEO 默认核函数的合理性。

**Table II** 揭示了训练策略的关键选择：将选择性转移与少步蒸馏结合为单阶段训练（`ST + DMD2`）会导致性能崩溃，而两阶段策略（先 LINVIDEO 后 DMD2）稳定且有效。这表明线性化后的模型需要先恢复生成质量，才能作为蒸馏的良好教师模型。

**Table I** 关于 `α` 衰减策略的消融表明，动态衰减（20 → 2）比固定 `α`（4 → 4）能获得更好的性能，且对 `α` 的具体范围不敏感。这一设计允许 `r` 在训练初期灵活探索，后期强制收敛到二值解。

### 失败模式与局限性

尽管 LINVIDEO 在加速与质量保持上取得了显著成果，但实验和分析揭示了以下局限：

1. **大比例替换的性能边界**：当 `target` 超过 18 层时，模型性能快速退化（Table 2）。这一边界受模型容量和任务复杂度影响，在更大模型上可能有所放宽，但目前缺乏在 30B+ 规模上的验证。
2. **第一层敏感性**：Figure 2 明确显示第一注意力层对线性化极为敏感，LINVIDEO 的选择性转移策略在实验中也倾向于保留该层为密集注意力。这暗示第一层可能承担着不可替代的全局上下文建模功能。
3. **硬件优化空间**：LINVIDEO 使用 PyTorch 通用实现，相比专用 CUDA 内核（如 SLA 在 RTX 5090 上的实现）仍有优化空间。**Table VI** 的对比显示，SLA 在专用硬件上具有延迟优势，但受限于硬件兼容性和视频形状支持。
4. **数据收集成本**：虽然 LINVIDEO 是数据免费的（data-free），但需要从预训练模型的采样轨迹中离线收集大量 `(x_t, u_t)` 对，这一准备阶段需要一定的计算资源和存储开销。
5. **框架假设限制**：ADM 目标的推导依赖整流流（rectified flow）模型假设（Eq. 13 中的评分差形式），对于其他扩散框架（如 DDPM）的适用性尚未验证。

![[assets/figures/papers/paper_list_l895_https_arxiv_org_abs_2510_08318/figures/007_Table_2.jpg]]
*Table 2: Ablation results across different values of target*

### 补充图表

![[assets/figures/papers/paper_list_l895_https_arxiv_org_abs_2510_08318/figures/004_Table_1.jpg]]
*Table 1: Performance comparison with relevant baselines on 8 dimensions of VBench [21]. “+DMD2” denotes our 4-step distilled LINVIDEO model. We highlight the best score and the second score in bold and underlined formats, respectively. More results can be found in Sec. H and Sec. K*

![[assets/figures/papers/paper_list_l895_https_arxiv_org_abs_2510_08318/figures/010_Table_3.jpg]]
*Table 3: Ablation results of selective transfer. For LINVIDEO*

![[assets/figures/papers/paper_list_l895_https_arxiv_org_abs_2510_08318/figures/008_Table_4.jpg]]
*Table 4: Ablation results of ADM. “w/*

![[assets/figures/papers/paper_list_l895_https_arxiv_org_abs_2510_08318/figures/009_Figure_6.jpg]]
*Figure 6: Training hours across different objectives. Settings are the same as those in Tab. 4. FLOPs comparison can be found in Tab. IV*

![[assets/figures/papers/paper_list_l895_https_arxiv_org_abs_2510_08318/figures/012_Table.jpg]]
*Table: I. Ablation results of α. Our LINVIDEO employs 20 → 2 as the range of α*

![[assets/figures/papers/paper_list_l895_https_arxiv_org_abs_2510_08318/figures/013_Table.jpg]]
*Table: II. Performance for the few-step distilled linear attention Wan 1.3B. $\mathrm { ^ { * } L I N V I D E O } + \mathrm { D M D 2 ^ { , * } }$ denotes that we first employ LINVIDEO to obatin a linear attention DM and then use DMD2 to distill is to the 4-step version. $\mathrm { \mathrm { } ^ { 4 } }$ S $T + \mathrm { D M D }$ 2 $\mathrm { \mathrm { } ^ { 3 } }$ implies that we combine our selective transfer and DMD2 to obtain the 4-step linear attention model in a single training stage. Table III. Comparison on Wan 1.3B (all meth- Table IV. Training ods use 4-step DMD2). Due to resource lim- FLOPs (3K steps). its, we will add more results in the future. Method FLOPs↓*

## 方法谱系与知识库定位

### 1. 问题定位：视频扩散模型中的注意力瓶颈

视频扩散模型（Video Diffusion Models, Video DMs）的核心计算瓶颈在于全序列自注意力（self-attention）的二次时间复杂度 $O(n^2)$，其中 $n$ 为时空序列长度。对于高分辨率、长时域的视频生成任务，$n$ 可达数万甚至数十万，导致推理延迟极高。LINVIDEO 瞄准的关键矛盾是：**直接以线性注意力（$O(n)$）全面替换二次注意力会导致生成质量严重下降**，原因在于线性注意力的表示能力天然弱于 softmax 注意力，且视频生成中的时空建模复杂性使得这一差距难以通过简单的数据驱动微调弥合。

### 2. 与现有高效注意力方法的谱系关系

#### 2.1 稀疏注意力方法（静态/动态稀疏化）

LINVIDEO 与以下稀疏注意力基线形成直接对比：

- **DFA (DiTFastAttn)**：采用静态稀疏模式，在推理时固定地丢弃部分注意力连接。
- **SVG / SVG2 (Sparse VideoGen 1 & 2)**：同样属于静态稀疏注意力范畴，对视频生成中的注意力图进行结构化裁剪。
- **XAttn**：引入动态稀疏机制，根据输入内容自适应地选择注意力连接。

这些方法的共同特点是**在 softmax 注意力框架内进行稀疏化**，本质仍是 $O(n^2)$ 复杂度的近似加速，加速比受限于稀疏度与质量之间的权衡。LINVIDEO 则从根本上将部分层的注意力机制替换为 $O(n)$ 线性注意力，在理论上具备更高的加速上限。

#### 2.2 线性注意力方法

线性注意力通过核函数特征映射 $\phi(\cdot)$ 将注意力计算重写为：

$$o_i = \frac{\phi(\pmb{q}_i) (\sum_{j=1}^{n} \phi(\pmb{k}_j)^\top \pmb{v}_j)}{\phi(\pmb{q}_i) (\sum_{j=1}^{n} \phi(\pmb{k}_j)^\top)}$$

利用矩阵乘法的结合律将复杂度降至 $O(n)$。LINVIDEO 采用 **Hedgehog 核**作为特征映射：

$$\phi(\pmb{q}) = \mathrm{softmax}(\pmb{q} \widetilde{W}_q) \oplus \mathrm{softmax}(-\pmb{q} \widetilde{W}_q)$$

消融实验证实该核在 VBench 得分上优于 ReLU 核和 Taylor 展开核，且延迟相近。与直接将全部层替换为线性注意力的朴素方案不同，LINVIDEO 的核心创新在于**选择性转移（Selective Transfer）**——仅对部分层进行线性化。

#### 2.3 与 SLA 的关系

**SLA**（Sparse Linear Attention）将层内混合注意力与专用 CUDA 内核结合，在 RTX 5090 上实现了显著的推理加速。然而，SLA 的硬件专用性限制了其通用性，而 LINVIDEO 基于 PyTorch 通用实现，具有更广泛的部署兼容性。两者在思路上互补：SLA 聚焦于单层内部的注意力混合，LINVIDEO 聚焦于跨层的选择性替换，未来二者的结合有望进一步提升加速比。

### 3. 核心机制创新：选择性转移与分布匹配

#### 3.1 选择性转移（Selective Transfer）

LINVIDEO 的关键洞察来自 **Figure 2** 的层敏感性分析：在相同数量层替换的条件下，浅层线性化比深层线性化带来显著的性能提升（Subject Consistency +2.86, Image Quality +6.31），而第一层替换则导致严重性能下降。这表明不同深度的注意力层对线性化替换的敏感性存在本质差异。

基于此，LINVIDEO 将层选择建模为二分类问题：为每个注意力层引入可学习标量 $r \in [0,1]$，通过混合注意力计算：

$$o_i = r \sum_{j=1}^{n} \frac{\exp(\frac{q_i k_j^\top}{d})}{\sum_{j=1}^{n} \exp(\frac{q_i k_j^\top}{d})} v_j + (1-r) \frac{\phi(\pmb{q}_i)(\sum_{j=1}^{n} \phi(\pmb{k}_j)^\top \pmb{v}_j)}{\phi(\pmb{q}_i)(\sum_{j=1}^{n} \phi(\pmb{k}_j)^\top)}$$

训练中通过约束损失 $\mathcal{L}_{\mathrm{con}}$ 强制替换层数达到目标数量，通过正则化损失 $\mathcal{L}_{\mathrm{reg}}$ 推动 $r$ 向 0 或 1 收敛（采用动态 $\alpha$ 衰减策略：20→2）。消融实验（**Table 3**）证实，选择性转移策略自动选择的层显著优于手动选择和启发式搜索，且移除正则化损失会导致性能崩溃（Overall Consistency 降至 1.42）。

#### 3.2 Anytime Distribution Matching (ADM)

区别于简单的输出 MSE 匹配，ADM 目标匹配训练模型与原始模型在**任意采样时刻 $t$** 的样本分布：

$$\mathcal{L}_{\mathrm{ADM}} = \mathbb{E}_{\hat{\mathbf{x}}_t \sim q_t} \bigg[ \log \frac{q_t(\hat{\mathbf{x}}_t)}{p_t(\hat{\mathbf{x}}_t)} \bigg]$$

在整流流（Rectified Flow）模型设定下，评分函数差可简化为模型输出差：

$$s_t(\hat{\mathbf{x}}_t) - \hat{s}_t(\hat{\mathbf{x}}_t) = -\frac{1-t}{t} \left( \pmb{u}_\theta(\hat{\mathbf{x}}_t) - \hat{\pmb{u}}_\theta(\hat{\mathbf{x}}_t) \right)$$

消融实验（**Table 4, Figure 6**）表明 ADM 损失在性能上明显优于 naive MSE 和 DMD 损失，且训练速度比 DMD 快约 4.4 倍。MSE 损失导致严重的时序抖动（**Figure II**），而 ADM 通过全轨迹分布匹配有效抑制了这一问题。

### 4. 适用边界与局限

#### 4.1 已验证的适用范围

- **模型规模**：Wan 1.3B / 14B、CogVideoX-2B，尚未在 30B+ 规模上验证。
- **扩散框架**：基于整流流（Rectified Flow）的模型，ADM 目标的推导依赖该假设，对 DDPM 等框架的适用性未验证。
- **加速上限**：target ≤ 18 层时性能稳定，超过后显著退化（**Table 2**），界限受模型容量和任务复杂度影响。

#### 4.2 已知局限

1. **数据收集开销**：虽然方法本身是“数据免费”（data-free）的，但需要从预训练模型的采样轨迹中离线生成大量 $(x_t, u_t)$ 对作为训练集，消耗一定计算资源和存储。
2. **实现优化空间**：当前基于 PyTorch 通用实现，线性注意力加速未达硬件理论峰值，与专用 CUDA kernel（如 SLA 所用）相比仍有优化空间。
3. **与稀疏注意力的结合**：线性注意力与稀疏注意力结合的潜力尚未充分挖掘，目前仅验证了纯线性注意力替换。
4. **核函数通用性**：Hedgehog 核虽在实验中表现最优，但针对视频任务学习专用核函数的方向未被探索。

### 5. 开放问题

1. **层内混合注意力**：能否将选择性转移的跨层选择思想与 SLA 的层内混合注意力结合，在单层内部也进行二次/线性注意力的动态分配，进一步提升加速比与质量？
2. **大规模模型验证**：在 30B+ 参数规模的视频生成模型上，该方法的有效性是否依然保持？target 替换层数的上限是否会随模型容量增加而提升？
3. **跨模态泛化**：该方法能否推广到其他模态的扩散模型（如 3D 生成、音频生成、图像生成）？ADM 目标在非整流流框架下的适配方案是什么？
4. **可学习核函数**：是否可以针对视频数据的时空特性，端到端地学习线性注意力的核函数，以进一步缩小与 softmax 注意力的表示能力差距？
5. **与少步蒸馏的深度融合**：当前两阶段策略（先 LINVIDEO 再 DMD2）虽稳定有效，但单阶段结合会导致性能崩溃（**Table II**），是否存在更优雅的联合训练方案？

## 原文 PDF

![[paperPDFs/CVPR_2026/LinVideo_A_Post_Training_Framework_towards_O_n_Attention_in_Efficient_Video_Generation.pdf]]