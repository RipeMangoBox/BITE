---
title: "FlashVID: Efficient Video Large Language Models via Training-free Tree-based Spatiotemporal Token Merging"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/FlashVID_Efficient_Video_Large_Language_Models_via_Training_free_Tree_based_Spatiotemporal_Token_Merging.pdf
openreview_forum_id: H6rDX4w6Al
aliases:
- FlashVID
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "联合建模时空冗余是核心控制变量：FlashVID 通过树形时空令牌合并（TSTM）灵活捕捉帧间动态对应关系，并结合注意力与多样性令牌选择（ADTS）筛选信息量大且多样的视觉令牌，从而实现高效且保真的压缩。"
primary_logic: "视频中语义最相关的视觉元素在时空位置上会发生动态变化，因此时空冗余压缩不应强制固定空间匹配，而应采用基于相似性的树结构跨帧连接，在保留关键语义的前提下消除冗余。"
claims:
- "现有加速框架独立压缩时空冗余，忽略时空关系导致次优性能。"
- "TSTM 通过树形结构联合压缩时空冗余，有效捕捉视频动态。"
- "ADTS 通过校准的最大最小多样性问题选择信息量大的令牌。"
- "在 LLaVA-OneVision 上保留 10% 视觉令牌即可维持 99.1% 的相对精度。"
---

# FlashVID: Efficient Video Large Language Models via Training-free Tree-based Spatiotemporal Token Merging

> [!tip] 核心洞察
> 视频中语义最相关的视觉元素在时空位置上会发生动态变化，因此时空冗余压缩不应强制固定空间匹配，而应采用基于相似性的树结构跨帧连接，在保留关键语义的前提下消除冗余。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | FlashVID：基于免训练树形时空令牌合并的高效视频大语言模型 |
| 英文题名 | FlashVID: Efficient Video Large Language Models via Training-free Tree-based Spatiotemporal Token Merging |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=H6rDX4w6Al); [GitHub](https://github.com/Fanziyang-v/FlashVID) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FlashVID |
| Dataset | VideoMME / EgoSchema / LongVideoBench / MVBench（五基准平均）, Qwen2.5-VL 固定令牌预算（VideoMME / EgoSchema / LongVideoBench / MLVU） |

> [!tip] 效果简介
> - VideoMME / EgoSchema / LongVideoBench / MVBench（五基准平均） 上，Avg. Rel. Acc (%) 为 99.1 (FlashVID, R=10%)，对比 97.8 (FastVID, R=10%)，变化 +1.3%。
> - Qwen2.5-VL 固定令牌预算（VideoMME / EgoSchema / LongVideoBench / MLVU） 上，Avg. Rel. Acc (%) 为 108.6 (FlashVID, 160 帧, R=10%)，对比 100.0 (Vanilla, 16 帧)，变化 +8.6%。

## 概述

视频大语言模型（VLLMs）在长视频理解中面临严重的计算瓶颈：视觉令牌数量随帧数线性增长，使得自注意力的二次复杂度成为推理加速的核心障碍。现有训练无关加速框架——如 **FastV**（Chen et al., 2024）、**VisionZip**（Yang et al., 2025c）、**PruneVID**（Huang et al., 2025）和 **FastVID**（Shen et al., 2025）——通常将空间压缩与时间压缩解耦处理，依赖固定的空间位置对应关系进行时序令牌合并（TTM）。然而，视频中语义相关的视觉元素在时空位置上会发生动态变化，强制固定匹配不仅会引入噪声，还导致时空压缩效果次优。

针对这一瓶颈，本文提出 **FlashVID**，一种免训练的混合压缩框架。其核心控制变量是**联合建模时空冗余**：通过两个协同模块，在保留关键语义的前提下实现高效压缩。具体而言：

- **注意力与多样性令牌选择（ADTS）** 将令牌筛选建模为帧级校准的最大最小多样性问题（MMDP），利用 [CLS] 注意力与事件相关性两项校准项，优先保留信息量大且特征多样的视觉令牌。
- **树形时空令牌合并（TSTM）** 构建时空冗余树，允许每帧令牌与前一帧中最相似的令牌建立跨帧连接（当余弦相似度超过阈值 $T_\tau$ 时），从而灵活捕捉帧间动态对应关系，实现细粒度的时空冗余消除。

FlashVID 属于混合压缩范式，在 LLM 前通过 ADTS 与 TSTM 进行两级压缩，并在 LLM 深层（第 20 层）进行令牌剪枝以匹配预设的平均令牌预算。

**核心实验结果：**

- 在 LLaVA-OneVision 上，仅保留 10% 视觉令牌即可维持 **99.1%** 的相对精度；当保留率提升至 15%–25% 时，性能甚至超越使用全部令牌的原始模型。
- 在固定计算预算下，FlashVID 使 Qwen2.5-VL 能够处理 **10 倍**帧数（160 帧 vs. 16 帧），相对性能提升 **8.6%**。
- 在 LLaVA-Video 上实现 **5.3×** 预填充加速和 **1.9×** 首令牌延迟（TTFT）加速，同时保持 95.9% 相对精度。

**方法定位：** FlashVID 属于训练无关的混合压缩方法，其核心贡献在于将时空冗余建模从解耦的固定匹配范式推进到基于相似性树的联合压缩范式，并通过多样性感知的令牌选择机制进一步提升压缩质量。

## 背景与动机

视频大语言模型（VLLMs）将视觉编码器与大语言模型（LLM）结合，在视频理解任务中展现出强大能力。然而，其推理成本极高——视觉编码器将每帧视频转换为数百个视觉令牌，多帧输入导致送入 LLM 的令牌数量急剧膨胀，使得自注意力的计算复杂度随序列长度 $n$ 呈二次增长：

$$\mathrm{FLOPs} = L \times (4 n d^2 + 2 n^2 d + 2 n d m)$$

其中 $L$ 为层数，$d$ 为隐藏维度，$m$ 为 FFN 中间维度。这种计算瓶颈严重制约了 VLLMs 处理长视频或高帧率视频的能力。

### 现有加速框架及其局限

为缓解上述瓶颈，研究者提出了一系列免训练的推理加速方法，按压缩位置可分为三类（Figure 2）：**LLM前压缩**（如 **VisionZip**, Yang et al., 2025c）、**LLM内剪枝**（如 **FastV**, Chen et al., 2024）以及**混合压缩**（如 **PruneVID**, Huang et al., 2025；**FastVID**, Shen et al., 2025）。这些方法的核心思路是通过减少视觉令牌数量来降低计算量。

然而，现有框架存在一个共同的结构性缺陷：**它们将空间冗余压缩与时间冗余压缩视为两个独立步骤**。典型的做法是先在每帧内部进行空间令牌合并或剪枝，再基于固定的空间位置对应关系（如相同网格坐标）进行跨帧的时序令牌合并（Temporal Token Merging, TTM）。这种解耦策略忽略了一个关键事实——视频中语义相关的视觉元素在时空位置上会随物体运动、镜头移动等因素发生动态变化，强制固定空间匹配会导致语义不相关的令牌被错误合并，同时遗漏真正的时空冗余（Figure 1a, Figure 3b）。

### 核心动机：联合建模时空冗余

FlashVID 的核心动机源于一个直接观察：**视频冗余本质上是时空耦合的**。同一物体在连续帧间可能发生位移、缩放或旋转，其对应的视觉令牌在空间网格上的位置随之改变。因此，有效的压缩不应依赖僵化的空间对应关系，而应基于语义相似性在时空维度上灵活建立连接。

Figure 3 的定量分析验证了这一判断：在相同合并阈值下，FlashVID 提出的树形时空令牌合并（TSTM）比传统 TTM 合并了更多令牌，且跨帧合并的平均相似度更高——这说明 TSTM 能够捕捉到 TTM 因固定空间约束而遗漏的细粒度时空冗余。

### 双重目标：保真压缩与长帧增益

FlashVID 的设计追求两个递进目标：

1. **高保真压缩**：在极端压缩率下维持模型性能。实验表明，仅保留 10% 视觉令牌时，FlashVID 可保持 LLaVA-OneVision 原始性能的 99.1%（Figure 1b）。
2. **长帧增益**：在相同计算预算下，通过高效压缩释放空间以处理更多帧。FlashVID 使 Qwen2.5-VL 能够处理 10 倍帧数（160 帧 vs. 16 帧），在固定令牌预算下相对性能提升 8.6%（Figure 1c）。

这两个目标通过两个协同模块实现：**注意力与多样性令牌选择（ADTS）**负责筛选信息量大且多样的令牌作为基础视频表示，**树形时空令牌合并（TSTM）**在此基础上联合消除帧间与帧内的时空冗余。二者的设计细节将在方法部分详细展开。

## 核心创新

FlashVID 的核心创新在于首次将**时空冗余联合建模**引入免训练的视频大语言模型加速框架，通过两个协同模块——**注意力与多样性令牌选择（ADTS）**和**树形时空令牌合并（TSTM）**——从根本上改变了现有方法对空间和时间冗余独立压缩的范式。

### 从独立压缩到联合建模：TSTM 的树形结构设计

现有加速框架（如 **FastV**（Chen et al., 2024）、**FastVID**（Shen et al., 2025））通常将空间压缩（帧内令牌合并/剪枝）与时间压缩（跨帧令牌合并）解耦处理。时间维度的压缩普遍采用**时序令牌合并（TTM）**，即强制相同空间位置的令牌跨帧匹配。然而，视频中语义相关的视觉元素在时空位置上会发生动态变化——物体可能移动、缩放或旋转——固定空间对应关系会错误地将语义不相关的令牌合并，既引入噪声又无法充分消除冗余。

FlashVID 的 TSTM 模块以**相似性驱动的树结构**替代固定空间匹配：对于每对相邻帧，计算所有视觉令牌间的成对余弦相似度矩阵 $S^{(f)} = \cos(E_v^{(f)}, E_v^{(f+1)})$，每个令牌链接到前一帧中最相似的令牌，只要相似度超过合并阈值 $T_\tau$。这一过程自然形成跨越帧的“时空冗余树”，树内令牌通过聚合操作 $c^{(i)} = \mathrm{Agg}(\mathcal{T}^{(i)})$ 压缩为单一表示。与 TTM 相比，TSTM 在相同阈值下合并更多令牌，且跨帧合并相似度更高（Figure 3），证明其能更灵活地捕捉细粒度视频动态。

### 从单一选择到注意力-多样性联合选择：ADTS 的校准 MMDP 框架

令牌选择的另一个关键瓶颈在于：现有方法或仅依赖注意力（如 FastV 基于文本-视觉注意力筛选令牌），或仅基于密度（如 FastVID），缺乏对所选令牌**多样性**的显式约束，可能导致冗余信息残留。

ADTS 将每帧的令牌选择形式化为一个**校准的最大最小多样性问题（MMDP）**，在最大化所选令牌间最小特征距离的同时，引入两项校准项：

- **[CLS] 注意力校准**：从视觉编码器自注意力矩阵 $A = \mathrm{Softmax}(Q K^T / \sqrt{d})$ 中提取 [CLS] 令牌对其他令牌的注意力权重，优先保留视觉编码器认为重要的区域；
- **事件相关性校准**：通过全局平均池化帧嵌入计算事件相关性矩阵 $\bar{\mathbf{S}}_e = \frac{1}{F} \sum_{i=1}^{F} (E_v \cdot {f_v}^{\top})[:, :, i]$，筛选与视频整体事件最相关的令牌。

消融实验（Table 4）证实，ADTS 显著优于单独的注意力选择（ATS）或多样性选择（DTS），且两项校准均带来额外增益。

### 两阶段协同压缩的平衡设计

FlashVID 将 ADTS 与 TSTM 串联为两阶段流水线：ADTS 首先筛选信息量大且多样的令牌作为基础视频表示，TSTM 随后在剩余令牌上构建时空冗余树进行细粒度合并。两模块的保留比 $\alpha$ 控制着信息筛选与冗余消除的平衡——消融表明 $\alpha = 0.7$ 时综合性能最优（Table 5），说明两个模块缺一不可，且需精确配比。

### 创新效果的关键证据

这一联合建模策略的效果在关键指标上得到验证：在 LLaVA-OneVision 上仅保留 10% 视觉令牌即可维持 99.1% 的相对精度（Table 1）；在 Qwen2.5-VL 上，相同计算预算下处理 10 倍帧数（160 帧 vs. 16 帧），相对性能提升 8.6%（Table 3）。值得注意的是，当保留率 $R \in \{15\%, 20\%, 25\%\}$ 时，FlashVID 甚至**超越**了使用全部视觉令牌的原始 LLaVA-OneVision，揭示了“少即是多”的现象——过度冗余的视觉令牌可能反而损害模型性能（Figure 6）。

## 整体框架

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_H6rDX4w6Al/figures/004_Figure_4.jpg]]
*Figure 4: Overview of our FlashVID. FlashVID compresses visual tokens by two synergistic modules: (1) ADTS prioritizes spatiotemporally informative tokens while ensuring feature diversity by solving a calibrated Max-Min Diversity Problem (MMDP); (2) TSTM models redundancy by spatiotemporal redundancy trees, which effectively capture fine-grained video dynamics*

FlashVID 采用**混合压缩范式**，将视觉令牌压缩置于大语言模型（LLM）之前，并在 LLM 内部进行补充剪枝，从而在效率与精度之间取得平衡。其核心流程为：视频帧经视觉编码器提取令牌后，依次通过两个协同模块——**注意力与多样性令牌选择（ADTS）**和**树形时空令牌合并（TSTM）**——进行压缩，随后送入 LLM，并在 LLM 深层进行最终剪枝以匹配预设令牌预算。

### 模块协作关系

FlashVID 将视频冗余压缩划分为两个阶段，分别由 ADTS 和 TSTM 承担，二者通过保留比 α 控制令牌分配比例：

1. **ADTS（第一阶段）**：在每一帧内，将令牌选择形式化为一个校准的**最大最小多样性问题（MMDP）**，筛选出既包含丰富时空信息又保持特征多样性的令牌，构成基础视频表示。校准项包括视觉编码器的 [CLS] 注意力和事件相关性，用以增强所选令牌与视频语义的关联。

2. **TSTM（第二阶段）**：在 ADTS 筛选后的令牌上，构建**时空冗余树**。每棵树的根节点位于首帧，子节点通过跨帧相似性连接——当相邻帧间令牌的余弦相似度超过合并阈值 $T_\tau$ 时建立父子关系。树内令牌经聚合（如均值池化）后得到压缩表示，实现帧间与帧内的联合冗余消除。

3. **LLM 内剪枝**：在 LLM 的第 20 层执行令牌剪枝，使各层平均保留令牌数满足预设预算。该层选择基于实证发现：VLLM 的深层具备较强的视觉感知能力，可准确识别关键帧，因而在深层剪枝对性能影响较小。

### 输入输出流

- **输入**：视频 $V$ 经视觉编码器得到 $F$ 帧的视觉令牌序列 $E_v \in \mathbb{R}^{F \times N_v \times d}$，其中 $N_v$ 为每帧令牌数，$d$ 为隐藏维度。
- **ADTS 输出**：每帧保留 $\alpha \cdot R \cdot N_v$ 个令牌（$R$ 为总保留率），形成信息量大且多样的令牌子集。
- **TSTM 输出**：对 ADTS 输出中剩余 $(1-\alpha) \cdot R \cdot N_v$ 的令牌进行树形合并，聚合为紧凑表示。
- **LLM 输入**：压缩后的视觉令牌与文本令牌拼接，送入 LLM 进行推理。
- **LLM 内剪枝**：在第 20 层将视觉令牌数进一步削减至 $R \cdot N_v$，确保与预设的平均令牌预算对齐，满足方程 $\bar{R} L = M K + R (L - K)$（其中 $\bar{R}$ 为平均每层保留率，$M$ 为进入 LLM 的令牌比例，$K$ 为剪枝层索引）。

### 关键设计考量

- **保留比 α**：控制 ADTS 与 TSTM 的令牌分配。消融实验表明，α=0.7 时综合性能最优，说明两模块需保持适当平衡——ADTS 确保信息覆盖，TSTM 消除冗余。
- **合并阈值 $T_\tau$**：决定 TSTM 的压缩强度。$T_\tau=0.8$ 时性能最佳；阈值过低会引入噪声（将不同实体的令牌错误合并），过高则压缩不足。
- **扩大因子 $f_e$**：在 ADTS 的 MMDP 求解中控制候选集规模。$f_e=1.25$ 在效率与性能间达到最佳平衡。

## 核心模块与公式推导

FlashVID 的核心由两个协同模块构成：**注意力与多样性令牌选择（ADTS）** 和 **树形时空令牌合并（TSTM）**。前者负责在每帧内筛选出信息量大且特征多样的代表性令牌，后者则跨帧联合建模时空冗余，实现细粒度的令牌压缩。

### 树形时空令牌合并（TSTM）

TSTM 的设计出发点是打破传统时序令牌合并（TTM）中“固定空间位置对应”的刚性约束。在视频中，语义相关的视觉元素会随时间发生位置、尺度和朝向的变化，强制空间对齐容易将不相关的令牌合并，引入噪声（Figure 3 展示了 TTM 合并相似度低于 TSTM 的定量证据）。

TSTM 通过构建**时空冗余树**来灵活捕捉帧间动态对应关系。具体而言，对于相邻帧 $f$ 和 $f+1$，首先计算所有视觉令牌之间的成对余弦相似度矩阵：

$$S^{(f)} = \cos(E_v^{(f)}, E_v^{(f+1)}) \in \mathbb{R}^{N_v \times N_v}$$

其中 $E_v^{(f)}$ 表示第 $f$ 帧的视觉令牌特征，$N_v$ 为每帧令牌数。基于该相似度矩阵，每个令牌会链接到前一帧中与其最相似的令牌，但仅当相似度超过合并阈值 $T_\tau$ 时才建立连接。由此形成的树结构将时空上高度冗余的令牌组织在一起，随后通过聚合操作得到压缩表示：

$$c^{(i)} = \mathrm{Agg}(\mathcal{T}^{(i)})$$

其中 $\mathcal{T}^{(i)}$ 为第 $i$ 棵时空冗余树中的令牌集合，$\mathrm{Agg}(\cdot)$ 通常采用均值池化。这种基于相似性的动态连接机制使得 TSTM 能够自适应地追踪视频中的运动模式，而非依赖预设的空间对应关系。

### 注意力与多样性令牌选择（ADTS）

TSTM 消除了冗余，但仍需确保进入 LLM 的令牌本身具有足够的判别力。ADTS 将令牌选择形式化为一个**逐帧校准的最大最小多样性问题（MMDP）**，同时兼顾令牌的重要性和多样性。

首先，定义第 $f$ 帧内视觉令牌的成对特征不相似度矩阵：

$$D^{(f)} = 1 - \cos(E_v^{(f)}, E_v^{(f)})$$

该矩阵用于度量令牌之间的特征差异，是多样性选择的基础。为引入重要性先验，ADTS 引入了两个校准项：

1. **[CLS] 注意力校准**：从视觉编码器的自注意力权重中提取 [CLS] 令牌对各视觉令牌的关注度：
   $$A = \mathrm{Softmax}(Q K^T / \sqrt{d})$$
   高注意力令牌通常与全局语义更相关。

2. **事件相关性校准**：通过全局平均池化帧嵌入计算每个令牌与视频整体事件的关联强度：
   $$\bar{\mathbf{S}}_e = \frac{1}{F} \sum_{i=1}^{F} (E_v \cdot {f_v}^{\top})[:, :, i]$$
   其中 $f_v$ 为帧级嵌入。该机制确保与视频核心事件高度相关的令牌被优先保留（Figure 8 可视化了有无事件校准时的令牌选择差异）。

MMDP 在最大化所选令牌集合中最小成对距离的同时，利用上述校准项加权，最终输出既具代表性又覆盖广泛语义区域的令牌子集。

### 两阶段压缩流程

FlashVID 采用先选择后合并的两阶段策略（Figure 4）：ADTS 首先在每帧内保留比例为 $\alpha$ 的令牌（消融实验表明 $\alpha=0.7$ 时综合性能最优，Table 5），随后 TSTM 对保留的令牌进行跨帧合并，进一步消除时空冗余。这种分工使两个模块各司其职——ADTS 保证信息密度，TSTM 负责冗余压缩，最终在仅保留 10% 视觉令牌的条件下仍能维持 99.1% 的相对精度（Table 1）。

## 实验与分析

### 主实验结果

FlashVID 在三种代表性 VLLM（LLaVA‑OneVision、LLaVA‑Video、Qwen2.5‑VL）和五个视频理解基准（VideoMME、EgoSchema、LongVideoBench、MVBench、MLVU）上，与四种训练无关的 SOTA 加速方法（**FastV**（Chen et al., 2024）、**VisionZip**（Yang et al., 2025c）、**PruneVID**（Huang et al., 2025）、**FastVID**（Shen et al., 2025））进行了系统比较。所有方法均采用统一的令牌预算对齐策略（Eq. 13），确保每个 Transformer 层处理相同平均数量的视觉令牌。

#### 不同保留率下的性能保持

在 LLaVA‑OneVision 上（Table 1），FlashVID 在所有保留率下均取得最优结果。当仅保留 10% 视觉令牌（R=10%）时，FlashVID 仍保持原始模型 99.1% 的相对精度，而次优方法 FastVID 为 97.8%，领先幅度达 +1.3%。更值得注意的是，当 R∈{15%, 20%, 25%} 时，FlashVID 的相对精度分别达到 100.2%、100.5% 和 100.3%，**超越了使用全部视觉令牌的原始 LLaVA‑OneVision**，呈现出“少即是多”（less‑is‑more）的效应（Figure 6 的定性案例进一步佐证了这一点）。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_H6rDX4w6Al/figures/005_Table_1.jpg]]
*Table 1: Comparison of state-of-the-art methods on LLaVA-OneVision and LLaVA-Video. Our FlashVID consistently outperforms previous state-of-the-art methods by a large margin under different retention ratios across multiple benchmarks and VLLMs. Notably, FlashVID surpasses vanilla LLaVA-OneVision with full visual tokens input when R ∈ {15%, 20%, 25%}*

在 LLaVA‑Video 上（Table 1），FlashVID 在 R=20% 时取得 Avg. Score 59.3，R=10% 时为 58.2，均显著优于所有基线方法。在 Qwen2.5‑VL 上（Table 2），FlashVID 在 R=20% 时达到 97.7% 的相对精度，R=10% 时为 95.6%，同样全面超越已有方法。

#### 固定令牌预算下的长帧处理增益

Table 3 展示了更有实际意义的结果：在相同的计算令牌预算下，FlashVID 使 Qwen2.5‑VL 能够处理 10 倍帧数（从 16 帧扩展到 160 帧），整体相对性能提升 8.6%（从 100.0% 到 108.6%）。这一增益的因果机制在于：FlashVID 通过 TSTM 联合压缩时空冗余，在固定预算内释放出更多令牌容量用于容纳额外帧，从而让模型获得更丰富的时间上下文信息（Figure 7 的定性分析直观展示了长帧处理带来的答案准确性提升）。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_H6rDX4w6Al/figures/021_Figure_7.jpg]]
*Figure 7: Qualitative comparison of Qwen2.5-VL with and without FlashVID. The vanilla model processes only 16 sampled frames, which limits its ability to capture sufficient temporal information. In contrast, Qwen2.5-VL can handle 160 (10×) frames with FlashVID while maintaining the overall computational budget, yielding more accurate predictions by leveraging longer temporal context*

#### 效率分析

在 LLaVA‑OneVision 上（Table 6），FlashVID 显著降低了预填充时间和首令牌延迟（TTFT）。在 LLaVA‑Video 上（Table 10），FlashVID 实现了 5.3× 预填充加速和 1.9× TTFT 加速，同时保持 95.9% 的相对精度。效率提升的根源在于 TSTM 大幅削减了进入 LLM 的视觉令牌数量，直接降低了自注意力计算中 $n^2$ 项的开销（参见 Eq. 3 中的 FLOPs 公式）。

### 消融研究

消融实验在 LLaVA‑OneVision 上以 R=10% 进行，系统验证了 FlashVID 各模块的贡献和关键超参数的影响。

#### ADTS 组件消融（Table 4）

Table 4 将 ADTS 与仅基于注意力的选择（ATS）和仅基于多样性的选择（DTS）进行了对比。结果表明：ADTS 在四个基准上的绝对分数和平均相对精度（99.1%）均大幅领先 ATS 和 DTS，验证了注意力与多样性联合建模的必要性。进一步引入 [CLS] 注意力校准（C.A）和事件相关性校准（E.R）两个校正项后，性能获得额外增益——这两个校正项分别从视觉编码器的自注意力权重（Eq. 7）和帧嵌入的全局平均池化（Eq. 8）中提取信号，引导令牌选择偏向与视频事件最相关的区域。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_H6rDX4w6Al/figures/008_Table_4.jpg]]
*Table 4: Ablation study on ADTS. ATS, DTS, and ADTS denote attention-, diversity-, and attention-diversity-based token selection, respectively.‘C.A’ and ‘E.R.’ denote [CLS] attention and event relevance calibration terms in ADTS. Table 5: Ablation study on α in visual token compression before LLM. α controls the retained ratio of ADTS and TSTM, where α = 0 and α = 1 indicate TSTM and ADTS only*

#### ADTS 与 TSTM 的保留比 α 消融（Table 5）

α 控制进入 LLM 前的视觉令牌压缩中 ADTS 与 TSTM 的保留比例（α=0 表示仅用 TSTM，α=1 表示仅用 ADTS）。实验表明 α=0.7 时取得最佳综合性能（相对精度 99.1%），说明两个模块的平衡至关重要：ADTS 负责筛选信息量大且多样的令牌，TSTM 负责消除冗余，二者协同才能达到最优压缩效果。

#### TSTM 合并阈值 T_τ 消融（Table 13）

T_τ 控制跨帧令牌合并的相似度阈值，较低的 T_τ 意味着更强的压缩。实验显示 T_τ=0.8 时性能最优：阈值过低（如 0.7）会引入噪声——将语义不够相似的令牌错误合并，导致信息混淆；阈值过高（如 0.9）则压缩不足，无法有效消除冗余。这一发现与 Figure 9 展示的 TSTM 失败案例一致：当不同实体但语义相似的令牌被合并时，会产生语义混淆。

#### 扩大因子 f_e 消融（Table 14）

f_e 控制 ADTS 阶段候选令牌集的扩展比例，直接影响进入 TSTM 的令牌基数。f_e=1.25 在效率和性能间达到最佳平衡；f_e=1.30 时性能持平但效率略低，表明过度扩展候选集带来的边际收益递减。

#### 树深度与树宽度约束消融（Table 11 & Table 12）

对 TSTM 施加最大树深度（限制合并跨越的时间范围）或最大树宽度（限制合并跨越的空间区域）约束，均未带来性能增益。这表明合并阈值 T_τ 已能有效控制合并范围，额外的显式约束是冗余的。

### 失败模式与局限性

1. **语义混淆合并**：TSTM 在合并时可能将不同实体但语义相似的令牌错误合并，导致信息混淆。Figure 9 可视化了此类失败案例，其根因在于 TSTM 仅依赖特征余弦相似度（Eq. 4）进行连接决策，缺乏对实体边界的显式建模。

2. **超参数敏感性**：方法依赖 T_τ、f_e、α 等多个超参数，这些参数的最优值可能随数据集或模型架构变化而需要重新调整。当前实验仅在三种 VLLM 上验证，扩展到更多架构时的泛化性仍需探索。

3. **极低保留率退化**：R<10% 场景下的性能退化尚未充分研究，此时 ADTS 选择的令牌数量可能不足以覆盖关键语义信息。

4. **长视频扩展性未验证**：当前实验的视频帧数最多为 160 帧，该方法能否无缝扩展到小时级视频或实时视频流任务仍是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_H6rDX4w6Al/figures/001_Figure_1.jpg]]
*Figure 1: Performance of FlashVID. (a) TTM may merge less correlated visual tokens, failing to capture fine-grained video dynamics. (b) FlashVID can enable Qwen2.5-VL to process 10× video frames, significantly improving the relative performance by 8.6% while maintaining overall computational budget. (c) FlashVID significantly outperforms current SOTA acceleration frameworks (e.g., FastV, VisionZip, FastVID) on three representative VLLMs*

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_H6rDX4w6Al/figures/002_Figure_2.jpg]]
*Figure 2: Efficient inference paradigms. State-of-the-art acceleration frameworks can be mainly divided into three categories: 1) Before-LLM Compression; 2) Inner-LLM Pruning; and 3) Hybrid Compression, where the hybrid compression can be viewed as a trade-off of the Before-LLM Compression and Inner-LLM Pruning strategy*

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_H6rDX4w6Al/figures/003_Figure_3.jpg]]
*Figure 3: (a) Number of merged tokens per frame with TSTM (orange) and TTM (blue) under the same threshold, with average merging similarity differences between TSTM and TTM shown in green. Tree-based Spatiotemporal Token Merging (TSTM) Figure 3: Comparison of spatiotemporal redundancy compression. (a) TSTM merges more tokens than TTM under the same threshold and achieves higher inter-frame merging similarity by flexibly capturing fine-grained video dynamics. (b) TTM enforces rigid spatial correspondences, often overlooking dynamic variations in videos and merging less correlated visual tokens. (c) TSTM models video redundancy via spatiotemporal redundancy trees, capturing fine-grained spatiotemporal...*

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_H6rDX4w6Al/figures/016_Table_13.jpg]]
*Table 13: Ablation study on the $T _ { \tau } T _ { \tau }$ controls the merging strength, in which a lower $T _ { \tau }$ indicates stronger compression. Table 14: Ablation study on $f _ { e }$ . \ $f _ { e }$ controls the expansion ratio, in which a large $f _ { e }$ may lead to computational inefficiency, while a low value may lose critical information

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_H6rDX4w6Al/figures/017_Figure_5.jpg]]
*Figure 5: Visualizations of Tree-based Spatiotemporal Token Merging (TSTM). We select three consecutive video frames that show obvious variations in spatial locations, scale, and orientation for each case to illustrate the advantages of our TSTM in FlashVID. TSTM jointly models spatial and temporal redundancy via spatiotemporal redundancy trees for capturing fine-grained spatiotemporal relationships; thus, it achieves better spatiotemporal redundancy compression*

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_H6rDX4w6Al/figures/020_Figure_8.jpg]]
*Figure 8: Comparisons of ADTS with and without event relevance calibration. ADTS employs event relevance calibration terms to identify the tokens most relevant to the video event*

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_H6rDX4w6Al/figures/022_Figure.jpg]]
*Figure: (a) Visualization of TSTM (Example 1)*

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_H6rDX4w6Al/figures/025_Figure.jpg]]
*Figure: Question: Which of the following is visible in the background of the video when the miniature bottle is shown empty?*

## 方法谱系与知识库定位

### 高效 VLLM 推理范式中的位置

FlashVID 属于**混合压缩**范式，即在 LLM 输入前进行令牌压缩，同时在 LLM 内部进行剪枝，兼顾效率与性能。当前主流训练无关加速框架可归为三类（Figure 2）：

1. **LLM 前压缩**：在视觉编码器输出后、LLM 输入前完成压缩，如 **VisionZip**（Yang et al., 2025c）利用 [CLS] 注意力进行令牌剪枝与空间合并。
2. **LLM 内剪枝**：在 LLM 的预填充阶段根据文本-视觉注意力动态丢弃令牌，如 **FastV**（Chen et al., 2024）。
3. **混合压缩**：结合前两类策略，如 **PruneVID**（Huang et al., 2025）在 LLM 内同时进行时空令牌合并与注意力选择；**FastVID**（Shen et al., 2025）基于密度进行时空令牌剪枝。

FlashVID 与上述方法的根本差异在于**时空冗余建模方式**。现有混合方法（如 PruneVID、FastVID）通常将帧内空间压缩与帧间时序压缩解耦处理，帧间合并依赖固定的空间位置对应关系（即 TTM, Temporal Token Merging）。这种刚性匹配忽略了视频中语义特征随时间的空间位移、尺度变化和旋转等动态特性，容易将语义不相关的令牌强行合并，引入噪声（Figure 1a, Figure 3b）。FlashVID 通过**树形时空令牌合并（TSTM）** 打破了这一限制——它基于帧间令牌的余弦相似度动态构建跨帧连接，允许令牌在相邻帧中寻找语义最相似的对应方，而非强制绑定相同空间位置。这一设计使时空冗余压缩从“位置驱动”转向“语义驱动”，是该方法的核心创新。

### 关键机制对比

| 方法 | 时空压缩策略 | 令牌选择机制 | 训练需求 |
|------|-------------|-------------|---------|
| **FastV** (Chen et al., 2024) | 无显式时空压缩 | 文本-视觉注意力选择 | 无 |
| **VisionZip** (Yang et al., 2025c) | 帧内空间合并 | [CLS] 注意力选择 | 无 |
| **PruneVID** (Huang et al., 2025) | TTM（固定位置对应） | 注意力选择 | 无 |
| **FastVID** (Shen et al., 2025) | 密度剪枝（独立时空） | 密度评分 | 无 |
| **FlashVID** (本文) | TSTM（语义驱动树形合并） | ADTS（注意力+多样性校准） | 无 |

ADTS 模块通过**校准的最大最小多样性问题（MMDP）** 在每帧内选择令牌，同时引入 [CLS] 注意力和事件相关性两项校准项，确保所选令牌既信息量大又具有多样性。这与 FastV 的单一注意力选择或 FastVID 的密度评分形成对比——后者缺乏多样性约束，容易在相似区域重复选择冗余令牌。

### 适用边界与局限

**适用场景**：
- 适用于基于 Transformer 的视频大语言模型，已在 **LLaVA-OneVision**、**LLaVA-Video** 和 **Qwen2.5-VL** 三种架构上验证。
- 在保留率 R ≥ 10% 时性能稳定，R ∈ {15%, 20%, 25%} 时在 LLaVA-OneVision 上甚至超越全令牌输入的原始模型（Table 1），呈现“少即是多”现象（Figure 6）。
- 固定令牌预算下，可通过压缩换取更长帧输入（如 10× 帧数），在需要长时序理解的场景（如 EgoSchema、LongVideoBench）中收益显著。

**已知局限**：
- **语义混淆合并**：TSTM 在相似度阈值较低时可能将不同实体但语义特征相近的令牌错误合并（Figure 9 展示了失败案例）。这是基于特征相似度的合并方法的固有风险。
- **超参数敏感性**：合并阈值 $T_\tau$、扩大因子 $f_e$、ADTS 与 TSTM 的保留比 $\alpha$ 等均需调优。消融实验表明 $T_\tau=0.8$、$f_e=1.25$、$\alpha=0.7$ 为最优配置（Table 13, Table 14, Table 5），但这些值可能随数据集或模型变化需重新调整。
- **极低保留率未充分探索**：R < 10% 时的性能退化程度尚未系统研究。
- **架构泛化性**：当前仅在三种 VLLMs 上验证，扩展到不同规模的 LLM 骨干或其他多模态架构时的效果仍需探索。

### 开放问题

1. **语义混淆的进一步缓解**：是否可引入实体级别的约束（如目标检测边界框、分割掩码）来辅助 TSTM 区分语义相近但实体不同的令牌？
2. **自适应阈值**：能否根据输入视频的动态程度（如运动幅度、场景切换频率）自适应调整 $T_\tau$ 和保留率，避免静态视频过度压缩或动态视频压缩不足？
3. **长视频扩展**：TSTM 的树结构在极长视频（如小时级）中可能导致树深度过大，是否需引入层次化合并或时间窗口截断机制？
4. **跨任务泛化**：ADTS 和 TSTM 的设计是否适用于视频问答以外的任务（如视频定位、时序动作检测）或其他多模态组合（如图文检索）？

## 原文 PDF

![[paperPDFs/ICLR_2026/FlashVID_Efficient_Video_Large_Language_Models_via_Training_free_Tree_based_Spatiotemporal_Token_Merging.pdf]]
