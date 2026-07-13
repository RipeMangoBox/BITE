---
title: Unified Spatiotemporal Token Compression for Video-LLMs at Ultra-Low Retention
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Unified_Spatiotemporal_Token_Compression_for_Video_LLMs_at_Ultra_Low_Retention.pdf
project_link: null
code_link: null
aliases:
- USTCUTAM
- USTCVLAULR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入统一的全局时空令牌保留池，联合注意力权重与语义相似度进行令牌筛选，通过聚类合并回收池令牌并在LLM内部进行文本感知的二次压缩，在极端压缩下维持高信息密度。
primary_logic: 通过全局选择高贡献、低冗余的视觉令牌，并在LLM内部基于查询相关性进行补充压缩，可以突破传统两阶段方法在极低保留率下的性能瓶颈。
claims:
- 在2%令牌保留率下，我们的方法保持原始模型约90.1%的性能，同时将FLOPs降低至约2.6%。
- 相比HoliTom在2%保留率下仅保持87.7%性能，我们的方法保持90.1%性能。
- 在5%令牌保留率下，我们的方法保持了原始性能的95.4%，优于其他基线方法。
- Multiple (MVBench, EgoSchema, MLVU, LongVideoBench, VideoMME) 上 Average Score % (retention vs. original) = 90.1% (2% retention with inner merging)
---

# Unified Spatiotemporal Token Compression for Video-LLMs at Ultra-Low Retention

> [!tip] 核心洞察
> 通过全局选择高贡献、低冗余的视觉令牌，并在LLM内部基于查询相关性进行补充压缩，可以突破传统两阶段方法在极低保留率下的性能瓶颈。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向视频大语言模型的超低保留率统一时空令牌压缩 |
| 英文题名 | Unified Spatiotemporal Token Compression for Video-LLMs at Ultra-Low Retention |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.21957) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Unified Spatiotemporal Token Compression (USTC) with Text-Aware Merging |
| Dataset | Multiple, LLaVA-OneVision-7B, LLaVA-Video-7B, Qwen2.5-VL-7B |

> [!tip] 效果简介
> - Multiple (MVBench, EgoSchema, MLVU, LongVideoBench, VideoMME) 上，Average Score % (retention vs. original) 90.1% (2% retention with inner merging) vs 56.3 avg score (LLaVA-OV-7B full model) (+90.1% performance preserved)。
> - LLaVA-OneVision-7B 上，FLOPs 约2.6% of original FLOPs (2% retention) vs 41.4T FLOPs (减少约97.4%)。
> - LLaVA-Video-7B 上，Average Score % 80.6% (1% retention with merging) vs 58.8 avg score (性能保留80.6%)。

## 概要

视频大语言模型（Video-LLMs）通过处理大量视觉令牌来理解视频内容，但随之而来的计算开销严重制约了其实际部署。现有令牌压缩方法普遍采用**两阶段时空分离压缩**策略——先进行空间压缩，再进行时间压缩。这一假设在令牌保留率较高时尚可维持，但当保留率降至极低水平（≤5%）时，时空冗余的耦合性导致关键视觉信息被系统性丢弃，资源分配失衡，模型性能急剧退化。

本文提出**统一时空令牌压缩（Unified Spatiotemporal Token Compression, USTC）** 方法，将令牌压缩重新定义为全局保留池内的时空联合分配任务。核心思路是：在一个统一的全局保留池中，联合注意力权重与语义相似度进行令牌筛选，保留高贡献、低冗余的令牌；对未选中的令牌通过聚类合并回收其语义信息，而非直接丢弃；在LLM内部进一步引入**文本感知合并**机制，基于查询相关性进行二次压缩。整个方法无需训练，即插即用。

实验表明，该方法在极端压缩条件下展现出显著优势：在仅保留约**2%**视觉令牌的情况下，USTC在多个基准上保持了原始模型约**90.1%**的性能，同时将FLOPs降低至原始模型的约**2.6%**；在5%保留率下，性能保留率达到**95.4%**。该方法在LLaVA-OneVision-7B、LLaVA-Video-7B和Qwen2.5-VL-7B等多个骨干模型上均表现出一致的有效性。

视频大语言模型（Video-LLMs）在复杂视频理解任务上展现出强大能力，但其推理成本随输入视频帧数和每帧视觉令牌数呈二次增长。以 **LLaVA-OneVision-7B** 为例，处理一个典型视频时，LLM 前向过程的 FLOPs 高达 41.4T，其中视觉令牌的计算开销占据主导。因此，视觉令牌压缩成为降低推理成本、推动 Video-LLMs 实际部署的关键技术路径。

现有令牌压缩方法普遍采用**两阶段时空分离**策略：先沿时间维度去除帧间冗余，再在空间维度筛选高贡献令牌。代表性工作如 **FastVID** 通过密度聚类进行帧内令牌融合，**HoliTom** 则使用动态规划对令牌分组并执行时空分离的剪枝与合并。这种“先时间后空间”的流水线假设时空冗余是可分解的，然而在**极低保留率**（≤5%）下，该假设暴露出两个结构性缺陷：

1. **关键信息丢失**：分离式压缩无法全局感知令牌的时空联合重要性，容易在早期阶段丢弃对最终问答至关重要的视觉线索。如 Figure 1(d) 所示，HoliTom 在 5% 保留率下保留了冗余令牌却遗漏了关键令牌，导致模型产生错误理解。
2. **资源分配失衡**：两阶段方法缺乏统一的全局资源调度机制，难以在极端压缩下实现信息密度最大化。部分令牌虽在单一维度上贡献较低，但其时空组合信息可能对推理不可或缺，分离式筛选无法捕获此类跨维度依赖。

上述瓶颈的根源在于：**时空冗余并非天然可分离**。一个令牌的“冗余性”取决于它在整个时空上下文中的语义贡献和注意力响应，而非仅由时间邻近性或空间相似性决定。因此，突破极低保留率下的性能瓶颈，需要从根本上重新设计压缩范式——从分离式筛选转向**统一时空分配**，在全局范围内联合评估每个令牌的贡献度与冗余度。

本文的核心动机正是回应这一需求：**通过构建全局时空令牌保留池，联合注意力权重与语义相似度进行统一筛选，并在 LLM 内部引入文本感知的二次压缩，实现在 2% 极端保留率下仍能维持约 90% 的原始性能**。这一目标不仅要求压缩策略本身的高效性，更要求压缩后的令牌集合能够最大程度保留对查询响应至关重要的视觉语义信息。

## 核心方法与创新机理

本文提出**统一时空令牌压缩（Unified Spatiotemporal Token Compression, USTC）**，其核心创新在于打破现有方法“先空间后时间”或“先时间后空间”的两阶段分离范式，将令牌压缩重新定义为**全局时空保留池中的统一分配任务**。围绕这一范式转移，方法在四个关键维度上引入了 changed slots：

### 1. 从两阶段分离压缩到统一时空压缩

现有方法（如 **FastVID**、**HoliTom**）假设时空冗余可独立消除，依次进行空间和时间维度的令牌剪枝或合并。这种分离策略在极低保留率（≤5%）下会导致关键视觉信息丢失和资源分配失衡（见 Figure 1）。USTC 维护一个**全局令牌保留池**，同时对所有视觉令牌进行时空联合筛选，从机制上避免了分离式压缩的累积误差。

### 2. 联合注意力与语义相似度的统一筛选标准

传统方法通常仅依赖注意力分数（如 **FastV**）或语义相似性（如 **LLaVA-Scissor**）单一指标进行令牌选择。USTC 提出**联合筛选机制**：对每个候选令牌，同时评估其多头注意力分数（衡量对文本的贡献度）和与保留池中已有令牌的最大余弦相似度（衡量语义冗余度），仅将“高贡献、低冗余”的令牌纳入保留池。消融实验表明，仅使用相似性作为筛选标准会导致性能显著下降，而加入相似性剪枝在 2% 保留率下可提升约 14% 的性能。

### 3. 回收池聚类合并：保留语义完整性

未被选中的令牌并非直接丢弃，而是进入**回收池**，通过基于密度的聚类算法（DPC-KNN）进行合并。聚类中心令牌被补充回保留池，使得压缩后的令牌集合在语义上更加完整。实验显示，聚类合并模块在 2% 保留率下额外贡献约 1.3% 的性能提升。

### 4. LLM 内部的文本感知二次合并

不同于 **FastV** 等仅在 LLM 内部基于最后令牌注意力进行剪枝的策略，USTC 在 LLM 前向传播的某一层引入**文本感知合并（Text-Aware Merging）**。该机制利用文本到视觉令牌的交叉注意力分布与余弦相似性，计算综合决策分数 $I(v_i) = (1-\lambda) \cdot A_m^{\mathrm{norm}}(v_i) + \lambda \cdot S_m^{\mathrm{norm}}(v_i)$，优先保留与用户查询高度相关的视觉令牌，同时将低相关令牌合并到语义最近的保留令牌中。这一设计在 5% 保留率下将平均性能保留率从 93.8% 提升至 95.4%。

### 5. 即插即用的免训练设计

整个 USTC 模块无需任何训练或微调，可作为即插即用组件直接集成到现有 Video-LLMs（如 LLaVA-OneVision、LLaVA-Video、Qwen2.5-VL）中，具备跨 backbone 的强迁移性。

该方法将视频令牌压缩重新表述为一个在**全局时空保留池**中进行的统一分配任务，而非传统的“先空间后时间”两阶段流水线。其整体架构由两个协同工作的模块组成：一个位于 LLM 外部的**统一时空压缩模块（Unified Spatiotemporal Compression Module）**，以及一个嵌入 LLM 内部层的**文本感知合并模块（Text-Aware Merging Module）**。两个模块均无需训练，以即插即用的方式兼容现有 Video-LLMs。

**输入输出流与模块关系**（参见 Figure 2）：

1. **视觉令牌输入**：视频经均匀帧采样后，由视觉编码器提取每帧的视觉令牌（如 LLaVA-OneVision-7B 默认采样 32 帧，每帧 196 个令牌，共 6272 个令牌）。
2. **外部统一时空压缩**：该模块接收全部视觉令牌，通过联合注意力分数与语义相似度进行全局筛选，将令牌划分为**保留池（retention pool）**和**回收池（recycle pool）**。保留池中的令牌是“高贡献、低冗余”的核心视觉信息载体；回收池中的令牌则通过基于密度的聚类（DPC-KNN）进行合并，以保持语义完整性，随后补充回保留池。最终输出的令牌序列经重新排序后送入 LLM，令牌数量被压缩至目标保留率。
3. **LLM 内部文本感知合并**：在 LLM 的特定中间层（最优剪枝层 K=18），该模块利用文本令牌到视觉令牌的交叉注意力分布与余弦相似度，计算每个视觉令牌的综合决策分数，识别与当前查询最相关的视觉令牌予以保留，并将相关性较低的令牌合并到语义最近的保留令牌中。这一步在不丢失查询关键信息的前提下，进一步降低 LLM 前向传播中的视觉令牌数量。
4. **文本输出**：LLM 基于压缩后的视觉令牌与文本查询生成最终回答。

该框架的核心设计逻辑在于：**在外部阶段消除时空冗余、保留语义完整的高信息密度令牌；在内部阶段根据查询需求进行二次压缩，确保极端低保留率下关键视觉证据不被丢弃**。Figure 1 通过定性示例对比了两阶段方法与统一方法在 5% 保留率下的行为差异——HoliTom 保留了大量冗余令牌却遗漏了关键令牌导致理解错误，而该方法有效缓解了这一问题。

![[assets/figures/papers/paper_list_l951_https_arxiv_org_abs_2603_21957/figures/003_Figure_2.jpg]]
*Figure 2: Overview of our method. 1) The Unified Spatiotemporal Compression module filters tokens with high contribution and low semantic redundancy, incorporating them into the retention pool. At the same time, it performs clustering and merging on tokens in the recycle pool to preserve the integrity of visual semantic information. 2) The Text-Aware Merging mechanism further enhances answer accuracy by guiding the LLM to focus on visual tokens that are most relevant to the input query*

### 方法总览：两阶段统一压缩框架

本方法提出一种无需训练的即插即用模块，将视频令牌压缩重新定义为**全局时空分配任务**。整体框架由两个核心模块构成：

1.  **统一时空压缩模块（外部）**：在视觉令牌进入LLM之前，通过全局保留池与回收池机制，联合筛选高贡献、低冗余的令牌，并对回收池令牌进行聚类合并以保持语义完整性（见 Figure 2）。
2.  **文本感知合并模块（LLM内部）**：在LLM的特定中间层，基于文本查询与视觉令牌的交叉注意力及语义相似性，进行二次压缩，优先保留与查询最相关的视觉信息（见 Figure 3）。

![[assets/figures/papers/paper_list_l951_https_arxiv_org_abs_2603_21957/figures/004_Figure_3.jpg]]
*Figure 3: The Text-Aware Merging mechanism further enhances answer accuracy by guiding the LLM to focus on visual tokens that are most relevant to the input query*

---

### 模块一：统一时空压缩

该模块将传统的“先空间后时间”两阶段压缩替换为**全局联合筛选**，核心流程如下：

1.  **全局保留池与回收池构建**：将所有帧的视觉令牌视为一个全局候选集。通过联合评估每个令牌的**注意力贡献**和**语义冗余度**，将高贡献、低冗余的令牌选入保留池，其余落入回收池。

2.  **联合筛选标准**：
    - **注意力贡献**：利用视觉编码器或LLM某一层的多头注意力分数，衡量令牌对全局上下文的重要性。对于第 $h$ 个头，注意力分数矩阵为：
      $$A_h = \mathrm{Softmax}\left(\frac{Q_h K_h^{\top}}{\sqrt{d}}\right) \quad \text{(Eq. 1)}$$
      其中 $Q_h, K_h$ 分别为查询和键矩阵，$d$ 为维度。取所有头中对该令牌的最大注意力分数作为其贡献度指标。
    - **语义冗余检测**：对于候选令牌 $c$，计算其与当前保留池 $\mathcal{P}$ 中所有令牌的最大余弦相似度：
      $$S = \sin(c, \mathcal{P}) = \max_{p \in \mathcal{P}} \frac{c \cdot p}{\|c\| \|p\|} \quad \text{(Eq. 2)}$$
      若该相似度超过阈值 $\tau$，则认为 $c$ 是冗余令牌，不进入保留池。

3.  **回收池令牌的聚类合并（DPC-KNN）**：为避免直接丢弃回收池令牌造成的信息损失，采用基于密度峰值的聚类算法（DPC-KNN）对回收令牌进行合并，将合并后的代表性令牌补充回保留池。
    - **局部密度**：通过 $k$ 近邻距离计算令牌 $v_i$ 的局部密度：
      $$\rho_i = \exp\left(-\frac{1}{k} \sum_{v_j \in \mathrm{kNN}(v_i)} d(v_i, v_j)^2\right) \quad \text{(Eq. 3)}$$
    - **最小距离**：计算 $v_i$ 到密度更高的令牌的最小距离：
      $$\delta_i = \begin{cases} \max_{j \neq i} d(v_i, v_j) & \text{if } \rho_i = \max_k \rho_k \\ \min_{j: \rho_j > \rho_i} d(v_i, v_j) & \text{otherwise} \end{cases} \quad \text{(Eq. 4)}$$
      综合 $\rho_i$ 和 $\delta_i$ 确定聚类中心，将回收令牌分配到最近的聚类中心进行合并，最终保留池中的令牌按原始时空顺序重新排列后输入LLM。

---

### 模块二：文本感知合并

在LLM内部（如第 $K$ 层），对已压缩的视觉令牌进行**查询感知的二次压缩**，确保与问题相关的视觉信息不被后续层丢弃。

- **决策分数**：对于每个视觉令牌 $v_i$，综合其**最大文本注意力** $A_m^{\mathrm{norm}}(v_i)$ 和**与文本的最大语义相似度** $S_m^{\mathrm{norm}}(v_i)$，计算保留优先级：
  $$I(v_i) = (1-\lambda) \cdot A_m^{\mathrm{norm}}(v_i) + \lambda \cdot S_m^{\mathrm{norm}}(v_i) \quad \text{(Eq. 9)}$$
  其中 $\lambda$ 为平衡权重。
  - $A_m(v_i)$ 从文本到视觉令牌的交叉注意力矩阵中提取，表示所有文本令牌对该视觉令牌的最大注意力值。
  - $S_m(v_i)$ 计算 $v_i$ 与所有文本令牌嵌入的最大余弦相似度。

- **合并策略**：根据 $I(v_i)$ 分数保留前 $R\%$ 的视觉令牌，剩余令牌通过语义相似性合并到最近的保留令牌中，而非直接剪枝，从而在极低保留率下维持信息密度。

## 实验与关键发现

### 主要结果：极端压缩下的性能保持

USTC 在多个 Video-LLM 基准上展现出显著的压缩-性能权衡优势。以 LLaVA-OneVision-7B 为主干模型，**Table 1** 展示了不同令牌保留率下的综合性能对比。在仅保留 2% 视觉令牌的极端条件下，USTC（含文本感知合并）保持了原始模型约 90.1% 的平均性能，同时将 FLOPs 降低至原始模型的约 2.6%。相比之下，HoliTom 在同等保留率下仅保持 87.7% 的性能，且 USTC 在 5% 保留率下进一步将性能保持率提升至 95.4%（不含内部合并为 94.9%）。当保留率放宽至 10% 时，USTC 几乎无损地保持了 98.4% 的原始性能。

![[assets/figures/papers/paper_list_l951_https_arxiv_org_abs_2603_21957/figures/005_Table_1.jpg]]
*Table 1: Comparison of State-of-The-Art Methods on LLaVA-OneVision-7B. The A%/B% retention ratio indicates that A% of the LLM input tokens are retained, and subsequently compressed to B% during the LLM forward pass. Best results are in bold, second best underlined. “(w/o M)” means our method without inner-LLM merging*

跨主干模型的迁移实验（**Table 2**）验证了方法的即插即用特性。在 LLaVA-OneVision-0.5B 上，2% 保留率下性能保持率达 90.7%；在 LLaVA-Video-7B 上，1% 保留率下仍保持约 80.6% 的性能。在 Qwen2.5-VL-7B 上，2% 保留率下性能保持率为 85.5%（**Table S.1**），进一步证明了方法的跨架构鲁棒性。

![[assets/figures/papers/paper_list_l951_https_arxiv_org_abs_2603_21957/figures/007_Table_2.jpg]]
*Table 2: Cross-backbone Method Comparison. Performance comparison of our method against state-of-the-art methods across different backbones, demonstrating consistent effectiveness*

### 消融实验：各模块贡献解耦

**Table 5** 的模块消融揭示了统一时空压缩各组件的作用机制。仅使用令牌相似性作为筛选标准时，性能显著下降，表明基于注意力的贡献评估是必要的。在注意力筛选基础上引入相似性剪枝，在 2% 保留率下带来约 14% 的性能提升，这源于对高注意力但语义冗余令牌的有效剔除。聚类合并模块（DPC-KNN）进一步贡献约 1.3% 的性能增益，其作用在于回收被筛选掉但包含完整语义信息的令牌。文本感知合并模块在 5% 保留率下将平均性能保持率从 93.8% 提升至 95.4%，证明了 LLM 内部基于查询相关性的二次压缩对答案准确性的关键影响。

超参数消融（**Figure 5**）确定了最优配置：令牌相似性阈值 τ=0.7、聚类比例 0.3、文本感知决策权重 λ=0.5、剪枝层 K=18、保留比例 R=50%。

![[assets/figures/papers/paper_list_l951_https_arxiv_org_abs_2603_21957/figures/011_Figure_5.jpg]]
*Figure 5: Ablation Experiment Results for Each Parameter*

### 效率与性能权衡

**Table 6** 对比了各方法的推理效率。USTC 在预处理、预填充和首令牌延迟上均展现出显著优势，同时保持更高的吞吐量。这得益于统一时空筛选避免了分阶段处理的额外开销，以及聚类合并减少了送入 LLM 的冗余令牌数量。

### 帧采样率敏感性分析

**Table 3** 展示了不同帧采样率下 USTC 在 2% 保留率时的性能稳定性。方法在不同帧数配置下均保持一致的性能优势，表明统一时空压缩策略对视频帧密度变化具有鲁棒性。然而，当前方法仍依赖均匀帧采样，这可能对长视频中的关键稀疏片段或短视频中的冗余帧处理不够理想。

### 高保留率下的性能

**Table 4** 表明，即使在较高令牌保留率下，USTC 仍持续优于对比方法。这验证了统一时空筛选机制不仅在极端压缩下有效，在宽松压缩条件下同样能更精准地保留信息密度高的令牌。

### 失败模式与局限

尽管 USTC 在离线视频压缩上表现优异，但存在以下局限：首先，方法仅支持固定离线视频处理，缺乏实时流式令牌压缩能力；其次，均匀帧采样策略可能导致短视频中保留冗余帧，或长视频中遗漏关键片段；最后，帧选择与令牌压缩尚未联合优化，这可能是进一步提升极端低保留率下性能的潜在方向。上述局限需要在实际部署中手动评估其对特定应用场景的影响。

![[assets/figures/papers/paper_list_l951_https_arxiv_org_abs_2603_21957/figures/010_Table_5.jpg]]
*Table 5: Module Ablations for Unified Spatiotemporal Token Compression*

## 定位与知识库关联

### 1. 问题定位：极低保留率下的瓶颈突破

现有视频大语言模型（Video-LLMs）的令牌压缩方法普遍遵循**两阶段时空分离**范式：先沿时间轴去除帧间冗余，再在空间维度筛选高贡献令牌。典型工作如 **FastVID**（密度聚类帧内融合）、**HoliTom**（动态规划令牌分组与两阶段剪枝合并）以及 **DyToK**（动态令牌合并），均假设时空冗余可独立处理。这一假设在中等压缩率下成立，但在**超低保留率（≤5%）**下暴露出结构性缺陷：分离式压缩导致关键视觉信息丢失，且资源分配在时空维度间失衡，难以维持高性能视频问答。

本工作将令牌压缩重新定义为**全局时空保留池内的统一分配任务**，提出**统一时空令牌压缩（Unified Spatiotemporal Token Compression, USTC）**，从根本上打破两阶段范式的性能天花板。

### 2. 方法谱系定位

#### 2.1 外部压缩：从分离到统一的范式跃迁

| 维度 | 两阶段方法（FastVID, HoliTom 等） | 本工作（USTC） |
|------|----------------------------------|----------------|
| 压缩策略 | 先时间后空间，独立处理 | 全局保留池，联合时空冗余消除 |
| 筛选标准 | 注意力分数或相似性，单一维度 | 注意力权重 + 语义相似度，联合阈值筛选 |
| 丢弃令牌 | 直接丢弃 | 聚类合并（DPC-KNN）后回收补充 |

具体而言，USTC 的外部压缩模块维护一个**全局保留池**，通过联合评估每个视觉令牌的注意力贡献（多头注意力分数 $A_h$）和语义冗余度（与保留池内令牌的最大余弦相似度 $S = \max_{p \in \mathcal{P}} \frac{c \cdot p}{\|c\| \|p\|}$），筛选出高贡献、低冗余的令牌。未入选的令牌并非简单丢弃，而是进入**回收池**，经过基于密度峰值的 KNN 聚类（DPC-KNN）合并后补充回保留池，确保语义完整性。

#### 2.2 内部压缩：从注意力剪枝到文本感知合并

LLM 内部层的令牌压缩，现有方法如 **FastV** 和 **PDrop** 通常基于视觉令牌对最后文本令牌的注意力分数进行剪枝。这种策略忽略了查询内容与视觉令牌之间的细粒度语义关联。

本工作引入**文本感知合并（Text-Aware Merging）**，在 LLM 内部层利用文本到视觉令牌的交叉注意力分布与余弦相似性，构建综合决策分数：

$$I(v_i) = (1-\lambda) \cdot A_m^{\mathrm{norm}}(v_i) + \lambda \cdot S_m^{\mathrm{norm}}(v_i)$$

其中 $A_m(v_i)$ 为视觉令牌 $v_i$ 对所有文本令牌的最大注意力分数，$S_m(v_i)$ 为最大语义相似度。该机制优先保留与查询高度相关的视觉令牌，将低相关令牌合并至语义最近邻，实现基于查询相关性的二次压缩。

#### 2.3 与相关工作的关系

- **FastV**：仅利用 LLM 内部注意力剪枝，缺乏外部压缩和语义冗余感知，在极低保留率下信息损失严重。
- **VisionZip / LLaVA-Scissor**：专注于空间令牌压缩，未处理时间维度冗余，且筛选标准单一。
- **HoliTom**：两阶段方法的代表，动态规划分组虽优于简单剪枝，但时空分离假设在 ≤2% 保留率下导致关键令牌遗漏（Figure 1d 示例）。
- **DyToK**：动态令牌合并，但缺乏全局保留池的统一调度机制。
- 本工作的 USTC 可视为对上述方法的**系统性综合与范式升级**：保留 FastV 的 LLM 内部压缩思想但扩展为文本感知合并，继承 VisionZip 的语义冗余检测但引入注意力联合筛选，借鉴 HoliTom 的合并回收思路但打破时空分离限制。

### 3. 适用边界与局限性

#### 3.1 已验证的适用场景

- **固定离线视频理解**：在 MVBench、EgoSchema、MLVU、LongVideoBench、VideoMME 等多个基准上验证，覆盖长视频、短视频、自我中心视频等多种场景。
- **多 backbone 兼容**：在 LLaVA-OneVision-7B/0.5B、LLaVA-Video-7B、Qwen2.5-VL-7B 上均表现出一致有效性，证明其即插即用特性。
- **极端压缩率**：在 1%-5% 令牌保留率下性能保持率显著优于所有基线方法。

#### 3.2 明确局限性

1. **不支持实时流式压缩**：当前方法假设完整视频已编码为令牌序列，缺乏对在线流视频的增量压缩能力。
2. **帧采样策略未联合优化**：采用均匀帧采样，可能导致短视频冗余帧或长视频漏掉关键片段，帧选择与令牌压缩的联合优化尚未探索。
3. **超参数敏感性**：最佳性能依赖精细的超参数调优（$\tau=0.7$, cluster ratio=0.3, $\lambda=0.5$, $K=18$, $R=50\%$），在不同 backbone 或视频类型间可能需要重新校准。

### 4. 开放问题

1. **实时流扩展**：如何将 USTC 的全局保留池机制适配为滑动窗口或增量更新模式，支持实时视频流的令牌压缩？
2. **帧-令牌联合优化**：能否设计端到端的可学习策略，联合优化帧采样率和令牌保留率，进一步提升极端低保留率下的信息密度？
3. **跨模态泛化**：统一时空压缩的思想是否可推广至图像-文本多模态模型（如图像集合理解、多图对话），以应对多图像场景下的令牌爆炸问题？
4. **动态保留率**：当前保留率为固定预设值，能否根据视频内容复杂度自适应调整保留率，实现更智能的资源分配？

## 原文 PDF

![[paperPDFs/CVPR_2026/Unified_Spatiotemporal_Token_Compression_for_Video_LLMs_at_Ultra_Low_Retention.pdf]]
