---
title: "ChArtist: Generating Pictorial Charts with Unified Spatial and Subject Control"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ChArtist_Generating_Pictorial_Charts_with_Unified_Spatial_and_Subject_Control.pdf
project_link: "https://chartist-ai.github.io/"
code_link: null
aliases:
- ChArtist
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过仅编码数据维度的骨架空间控制表示，并利用空间门控注意力机制建立空间与主题条件之间的显式依赖关系，从而在生成过程中实现结构保真与视觉自由度的平衡。
primary_logic: 骨架表示通过抽象图表的数据编码维度，为参考图像的语义注入提供了结构自由度和数据保真度之间的最佳平衡。空间门控注意力通过动态调节主题信号，实现了空间约束对主题影响的顺序主导。
claims:
- 在空间对齐（Task 1）和双控制（Task 1+2）任务中，ChArtist 在数据准确率（Data Acc）和视觉一致性（DINO）上均超越所有基线方法。
- 人类评估中，ChArtist 在空间和主题问题上的平均排名均位居前二，且在主题一致性上显著优于 InContext（p < 0.001）。
- 消融实验证明空间门控注意力（Spatially-Gated Attention）对维持数据准确性至关重要，β=0.3 时数据准确率最高（0.927），而 β=0.9 时产生严重背景泄漏。
- 提出的骨架表示在控制谱系中占据“甜点”，既忠实编码主数据维度，又为风格注入留有充分空间。
---

# ChArtist: Generating Pictorial Charts with Unified Spatial and Subject Control

> [!tip] 核心洞察
> 骨架表示通过抽象图表的数据编码维度，为参考图像的语义注入提供了结构自由度和数据保真度之间的最佳平衡。空间门控注意力通过动态调节主题信号，实现了空间约束对主题影响的顺序主导。

| 字段 | 内容 |
|------|------|
| 中文题名 | ChArtist：统一空间与主题控制的象形图生成 |
| 英文题名 | ChArtist: Generating Pictorial Charts with Unified Spatial and Subject Control |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.14209) · [Project](https://chartist-ai.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ChArtist |
| Dataset | Human Evaluation, Line Chart, Bar Chart |

> [!tip] 效果简介
> - Human Evaluation (Spatial Alignment, 300 participants) 上，Average Rank (lower is better) 2.957 (2nd) vs SDEdit 2.897 (1st) (+0.06 (not significant))。
> - Human Evaluation (Subject Consistency, 300 participants) 上，Average Rank 2.845 (2nd) vs ControlNet-Depth 2.822 (1st); significantly better than InContext (p<0.001) (+0.023)。
> - Line Chart (Dual Control, Task 1+2) 上，DINO (visual consistency) 0.931 vs 次优方法 (Paint-by-Example or ControlNet-Depth+IP-Adapter) (未提供具体基线数值)。

## 概要

象形图（pictorial chart）将柱、线、扇区等图表基元替换为具象视觉元素，是数据叙事中兼具信息密度与表现力的载体。然而，自动生成此类图表面临一个核心瓶颈：现有控制表示要么过于密集（如Canny边缘、深度图），限制了视觉元素的灵活注入；要么过于稀疏（如边界框），无法提供足够的结构指导。这种矛盾导致生成结果难以同时保持数据准确性和视觉表现力。

**ChArtist** 通过两个关键设计突破上述瓶颈：（1）**骨架表示**——仅编码数据维度的抽象线条（如柱高、折线趋势、扇区角度），在控制谱系中占据结构保真与视觉自由度之间的“甜点”；（2）**空间门控注意力**——在推理时从骨架条件动态构建空间掩码，并以此门控主题信号，建立空间约束对主题影响的顺序主导，解决并行LoRA组合带来的结构错位与风格泄漏。

实验表明，在空间对齐任务中，ChArtist的数据准确率（Data Acc）达到0.894，超越所有基线；在双控制任务中，视觉一致性（DINO）达0.931，同样领先。300人受控人工评估进一步确认，ChArtist在空间和主题维度上的平均排名均位居前二，且在主题一致性上显著优于InContext（p < 0.001）。消融实验揭示，空间门控注意力对数据保真度至关重要——当控制因子β=0.3时数据准确率最高（0.927），而β=0.9时出现严重背景泄漏。当前方法主要支持条形图、折线图和饼图，向更复杂图表拓扑的推广仍是开放问题。



象形图（pictorial chart）将传统图表的数据编码元素（如柱状图中的矩形条、折线图中的线段、饼图中的扇形）替换为与数据主题相关的视觉对象（如用树木代替柱条表示森林覆盖率），从而在传递数据信息的同时增强视觉叙事力。然而，手工设计高质量的象形图需要设计师同时处理数据准确性与视觉表现力，过程耗时且依赖专业技能。因此，自动生成象形图成为一个具有实际价值的研究问题。

### 现有方法的困境：密集控制与稀疏控制的矛盾

象形图自动生成的核心挑战在于**同时实现空间结构控制与主题外观控制**。空间控制要求生成图像严格遵循原始图表的数据编码结构（如柱高、折线趋势、扇区角度），而主题控制则要求将参考图像的视觉风格和语义特征注入生成结果。现有的条件生成方法在这两类控制之间存在根本性矛盾：

- **密集像素级控制表示**（如 Canny 边缘图和深度图）能够提供精确的结构指导，但其过于刚性的轮廓约束严重限制了参考视觉元素的灵活注入。当试图将主题外观融入密集控制下的生成过程时，模型往往难以在结构保真与视觉自由度之间取得平衡。
- **稀疏布局控制表示**（如边界框）虽然为视觉注入保留了充分空间，但缺乏足够的结构信息来保证生成图表的数据准确性，容易导致数据编码维度的失真。

这一矛盾在象形图生成中尤为突出：图表的数据准确性是不可妥协的硬约束，而视觉表现力又是象形图区别于普通图表的本质特征。**现有控制表示在复杂度谱系中缺乏一个“甜点”位置**——既能忠实编码核心数据维度，又为风格注入留有充分空间。

### 多条件交互的干扰问题

当空间控制与主题控制同时作用于扩散模型时，还存在**跨条件干扰**问题。现有方法通常采用并行 LoRA 组合策略，即各条件适配器独立处理其对应的控制信号后直接合并。然而，这种并行合并缺乏条件间的显式依赖关系，导致两种典型的生成伪影（Figure 5）：

1. **结构错位**：主题适配器的信号干扰空间控制，使生成图像偏离图表骨架结构；
2. **风格泄漏**：主题适配器在空间约束范围之外引入额外的视觉元素，破坏数据编码的清晰性。

### ChArtist 的动机与核心思路

针对上述瓶颈，ChArtist 提出两条核心设计原则：

- **骨架表示（Skeleton-based Representation）**：仅编码图表的数据维度信息（如柱状图的高度、折线图的趋势走向、饼图的扇区角度），将图表的非数据编码部分（如颜色、纹理、装饰元素）完全释放给主题控制。这种最小化抽象在控制表示谱系中占据了结构保真与视觉自由度之间的最优平衡点（Figure 3）。
- **空间门控注意力（Spatially-Gated Attention）**：在推理阶段建立空间条件对主题条件的顺序依赖关系——先由空间控制确定数据编码区域，再通过动态计算的空间掩码门控主题注意力的作用范围，从而解决并行 LoRA 合并带来的跨条件干扰。

通过这两项设计，ChArtist 实现了**统一的空间与主题控制**，在保证数据准确性的同时赋予生成过程充分的视觉表现力。



## 核心方法与创新机理

ChArtist 的核心创新在于针对象形图生成中“结构保真”与“视觉自由度”之间的矛盾，提出了两个相互协同的 changed slots：**骨架控制表示**与**空间门控注意力机制**。这两个设计共同解决了现有方法在密集控制（如 Canny 边缘）与稀疏控制（如边界框）之间的两难困境。

### 骨架控制表示：在控制谱系中寻找“甜点”

现有控制表示存在一个根本性瓶颈：**Canny 边缘和深度图等密集像素级表示**（如 **ControlNet-Canny** 与 **ControlNet-Depth**, Zhang et al., ICCV 2023）虽然能精确约束图表结构，但其刚性轮廓严重限制了参考图像中视觉元素的灵活注入；而**边界框等稀疏布局表示**则缺乏足够的结构指导，难以维持数据准确性。这种矛盾导致象形图生成中难以同时保证数据保真度和视觉表现力（Figure 3）。

ChArtist 提出的**骨架表示**（skeleton-based representation）在控制复杂度谱系中占据了一个关键“甜点”位置（Figure 3）：它仅编码图表的数据编码维度，而有意省略非必要的视觉轮廓。具体而言：
- **条形图**：每根柱子用单条垂直线表示，编码柱高这一核心数据维度；
- **折线图**：用多段线追踪数据趋势，编码折线的走向和拐点；
- **饼图**：用两条彩色径向线指示扇区的顺时针起止角度。

这种极简抽象（minimal abstraction）的因果效应是双重的：一方面，骨架忠实编码了主数据维度，确保生成结果的数值准确性；另一方面，其结构上的极简性为参考图像的语义或风格注入留下了充分的空间自由度。这从根本上解决了密集表示“过约束”与稀疏表示“欠约束”之间的矛盾。

### 空间门控注意力：建立空间到主题的顺序依赖

当同时施加空间控制（骨架）和主题控制（参考图像）时，ChArtist 面临第二个核心挑战：**多条件间的相互干扰**。基线方法（如 ControlNet + IP-Adapter）通常采用并行 LoRA 组合策略，各条件独立处理，缺乏显式的交互机制。这导致两个典型伪影（Figure 5）：
- **结构错位**（structure misalignment）：主题 LoRA 扭曲了空间控制信号，使生成结果偏离图表骨架；
- **风格泄漏**（style leakage）：主题 LoRA 在空间约束区域之外引入额外的视觉元素。

ChArtist 提出的**空间门控注意力**（Spatially-Gated Attention）是一个训练无关（training-free）的推理机制，其核心因果逻辑是建立空间条件对主题条件的**顺序主导关系**。具体而言，该机制首先从骨架查询 $Q_S$ 与图像潜变量键 $K_X$ 的交叉注意力中构建空间掩码 $M$：

$$W_{SX} = \mathrm{softmax}\left(\frac{Q_S K_X^T}{\sqrt{d_k}}\right), \quad M = \sum_{i \in I_S} (W_{S \to X})_i$$

随后，空间掩码 $M$ 被用于动态门控主题注意力 $W_{XR}$，通过控制因子 $\beta$ 调节背景区域的主题表现力：

$$W_{XR}' = M \odot W_{XR} + \beta \cdot (1 - M) \odot W_{XR}$$

这一设计的核心洞见在于：**空间掩码使骨架区域内的主题信号得以完整保留（确保数据编码区域的主题一致性），而背景区域的主题影响被 $\beta$ 抑制**，从而在推理时实现了空间约束对主题影响的顺序主导。消融实验（Table 4, Figure 8b）证实了这一机制的关键作用：$\beta=0.3$ 时数据准确率达到最高的 0.927，而 $\beta=0.9$ 时出现严重的背景泄漏——这直接证明了空间门控注意力对于双控制下数据保真度的不可或缺性。

### 两个 changed slots 的协同效应

骨架表示与空间门控注意力并非孤立创新，而是形成了因果闭环：骨架表示为空间门控注意力提供了构建掩码 $M$ 所需的精确数据编码区域定位；空间门控注意力则使骨架表示的结构约束力得以在主题注入过程中持续生效，防止主题信号反噬空间结构。二者的协同使得 ChArtist 能够“先确定数据框架，后注入视觉语义”，从而在数据准确性与视觉表现力之间实现此前方法无法达成的平衡（Table 3, Figure 8a）。



ChArtist 的整体架构以预训练的 DiT 扩散模型（基于 FLUX）为生成骨干，通过两条并行的条件 LoRA 适配器分别注入空间控制与主题控制，并在推理阶段引入无需训练的空间门控注意力机制来协调二者的交互。Figure 4 给出了架构全貌。

![[assets/figures/papers/paper_list_l2448_https_arxiv_org_abs_2603_14209/figures/004_Figure_4.jpg]]
*Figure 4: The whole architecture of ChArtist consists of (A) a pretrained DiT-based diffusion model with two conditional-LoRAs with different positional encoding on the image inputs, where (B) one is for spatial control*

**输入序列构建**  
模型接收一个统一的序列输入，由文本提示、噪声图像潜变量和条件令牌拼接而成。空间条件由骨架表示编码，主题条件由参考图像经编码后注入，二者以不同的位置编码在序列中加以区分。

**双 LoRA 适配器**  
- **LoRA_S（空间控制适配器）**：从骨架 S 学习空间控制信号，使用 RoPE 位置编码与图像潜变量对齐，确保生成图像忠实遵循图表的数据编码维度（如柱高、折线趋势、扇区角度）。  
- **LoRA_R（主题控制适配器）**：从参考图像 R 注入主题外观信息，其位置编码引入偏移量 Δ，以在序列中与空间条件形成区分，避免直接冲突。

**推理时的空间门控注意力**  
并行合并多个 LoRA 会引发结构错位和风格泄漏（见 Figure 5），因此 ChArtist 在推理阶段采用 Spatially-Gated Attention 机制。该机制的核心流程为：
1. 计算骨架查询 $Q_S$ 与图像潜变量键 $K_X$ 之间的缩放点积注意力图：
   $$W_{S X} = \mathrm{softmax}\left(\frac{Q_S K_X^T}{\sqrt{d_k}}\right)$$
2. 对数据编码骨架令牌的注意力进行聚合，形成空间掩码：
   $$M = \sum_{i \in I_S} (W_{S \to X})_i$$
3. 使用空间掩码 $M$ 对原始主题注意力 $W_{X R}$ 进行门控，通过控制因子 $\beta$ 调节背景中的主题表现力：
   $$W_{X R}' = M \odot W_{X R} + \beta \cdot (1 - M) \odot W_{X R}$$

这一机制在无需额外训练的前提下，建立了空间约束对主题影响的顺序主导关系——在数据编码区域（$M$ 高）保持主题信号的完整注入，在背景区域通过 $\beta$ 抑制主题泄漏，从而在结构保真与视觉自由度之间取得平衡。

### 补充图表

![[assets/figures/papers/paper_list_l2448_https_arxiv_org_abs_2603_14209/figures/001_Figure_1.jpg]]
*Figure 1: Illustrations of pictorial charts generated by ChArtist. We convert chart primitives such as bars, lines, and segments into vivid visual elements. With user-provided text or reference images, ChArtist combines spatial and subject control to maintain data fidelity while achieving visual consistency*



ChArtist 的核心架构由四个关键模块构成，围绕“骨架表示—双 LoRA 条件注入—空间门控注意力”这一主线协同工作，其整体架构如 Figure 4 所示。

### 4.1 骨架控制表示

**设计动机**：现有控制表示存在“过约束”与“欠约束”的两难困境。密集像素级表示（如 Canny 边缘、深度图）虽然提供精确的结构引导，却过度约束了视觉元素的注入空间；稀疏布局（如边界框）虽给予语义自由，却无法保证图表的数据保真度。ChArtist 在控制表示谱系中找到了一个“甜点”（sweet spot）——骨架表示（Figure 3）。

**表示定义**：骨架表示仅编码图表的数据编码维度，摒弃了填充、颜色、纹理等非结构化信息。针对三种图表类型分别定义：
- **条形图**：每根柱子由一条垂直线段表示，其高度编码数据值；
- **折线图**：一条折线追踪数据趋势，由关键数据点连接而成；
- **饼图**：两条彩色径向线分别指示每个扇区的顺时针起止角度。

这种最小化抽象使生成模型在忠实保留数据维度的同时，获得最大化的视觉注入自由度。

### 4.2 双 LoRA 条件注入

ChArtist 基于预训练的 DiT 扩散模型（FLUX 架构）构建，通过两个独立的低秩适配器（LoRA）分别注入空间控制信号与主题控制信号：

- **LoRA_S（空间控制适配器）**：从骨架图 $S$ 学习空间约束，使用 RoPE 位置编码与图像潜变量对齐，确保生成的视觉元素遵循图表的数据结构。
- **LoRA_R（主题控制适配器）**：从参考图像 $R$ 注入主题外观信息，其位置编码引入偏移量 $\Delta$ 以与空间条件在序列维度上区分。

两个 LoRA 在训练阶段独立优化，避免了联合训练中的条件耦合问题。然而，推理时若简单并行合并多个 LoRA，会产生严重的跨条件干扰：LoRA_R 的主题信号会扭曲空间结构（结构错位），并在空间约束区域之外引入额外的视觉元素（风格泄漏），如 Figure 5 所示。

![[assets/figures/papers/paper_list_l2448_https_arxiv_org_abs_2603_14209/figures/005_Figure_5.jpg]]
*Figure 5: Artifacts observed when merging multiple LoRAs in parallel*

### 4.3 空间门控注意力机制

**问题形式化**：设潜变量 $X$ 与骨架令牌 $S$ 之间的注意力图为 $W_{SX}$，与参考令牌 $R$ 之间的注意力图为 $W_{XR}$。并行 LoRA 合并时，$W_{XR}$ 对 $W_{SX}$ 构成无约束干扰，导致数据保真度下降。

**核心思想**：建立空间条件对主题条件的顺序依赖关系——空间约束决定“在哪里画”，主题信号决定“画什么”。具体而言，从空间注意力中提取掩码，再用该掩码动态门控主题注意力的影响范围。

**公式推导**：

第一步，计算骨架查询 $Q_S$ 与潜变量键 $K_X$ 之间的缩放点积注意力，构建空间注意力图：

$$W_{SX} = \mathrm{softmax}\left(\frac{Q_S K_X^T}{\sqrt{d_k}}\right)$$

第二步，对数据编码骨架令牌的注意力进行聚合，形成空间掩码 $M$：

$$M = \sum_{i \in I_S} (W_{S \to X})_i$$

其中 $I_S$ 为数据编码骨架令牌的索引集合。掩码 $M$ 中的高响应区域对应图表的数据结构位置（如柱体区域、折线路径），低响应区域对应背景。

第三步，使用空间掩码 $M$ 对原始主题注意力 $W_{XR}$ 进行门控：

$$W_{XR}' = M \odot W_{XR} + \beta \cdot (1 - M) \odot W_{XR}$$

其中 $\odot$ 表示逐元素乘法，$\beta \in [0, 1]$ 为控制因子，调节背景区域的主题表现力：
- 在 $M$ 高响应区域（数据结构位置），主题注意力保持原始强度，确保视觉元素准确填充图表结构；
- 在 $M$ 低响应区域（背景），主题注意力被 $\beta$ 缩放：$\beta=0$ 时背景完全不受主题影响，$\beta=1$ 时退化为无门控的并行合并。

**关键特性**：该机制是训练无关的（training-free），仅在推理时作用于注意力图，无需额外训练即可解决跨条件干扰。消融实验（Table 4）表明，$\beta=0.3$ 时数据准确率达到最优（0.927），而 $\beta=0.9$ 时出现严重的背景泄漏，验证了空间门控对数据保真度的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l2448_https_arxiv_org_abs_2603_14209/figures/003_Figure_3.jpg]]
*Figure 3: The spectrum of control representation based on their complexity. Top: Existing control representations for natural image; Bottom: Our proposed skeleton-based representations for pictorial chart generation, where charts (blue) are represented as skeletons (red and green lines)*



## 实验与关键发现

### 核心瓶颈与因果机制

象形图生成的根本矛盾在于**控制表示的粒度选择**：传统密集表示（如Canny边缘、深度图）虽能精确约束空间结构，却严重抑制了视觉元素的灵活注入；而稀疏表示（如边界框）虽留有风格自由度，却无法提供足够的结构指导。ChArtist 通过一条因果链解决此矛盾——**骨架表示**仅编码数据维度（如柱高、折线趋势、扇区角度），在结构保真与视觉自由度之间占据“甜点”位置；**空间门控注意力**则建立空间条件对主题条件的顺序依赖，用空间掩码动态调节主题信号，从而在推理时实现“结构先行、风格注入”的协调机制。

### 空间对齐任务（Task 1）

Table 1 和 Figure 7 展示了仅空间控制条件下的定量与定性对比。在柱状图上，ChArtist 的数据准确率（Data Acc）达到 **0.894**，文本对齐度（CLIP-T）为 **0.304**，均超越 ControlNet-Canny、ControlNet-Depth、SDEdit 和 Inpainting 等基线。定性结果（Figure 7）进一步显示，Canny 和深度图控制下的生成结果在柱体轮廓处产生僵硬边缘，限制了风格化表现；而骨架表示在保持柱高精度的同时，允许生成结果在柱体内部和背景区域自由融入视觉元素。

![[assets/figures/papers/paper_list_l2448_https_arxiv_org_abs_2603_14209/figures/007_Figure_7.jpg]]
*Figure 7: Result of spatially aligned evaluation with different control representations. (Task 1)*

![[assets/figures/papers/paper_list_l2448_https_arxiv_org_abs_2603_14209/figures/008_Table_1.jpg]]
*Table 1: Quantitative comparison of spatially aligned evaluation*

在折线图和饼图上的趋势一致：骨架表示在数据编码维度（折线趋势、扇区角度）上保持高保真度，同时为非数据编码区域保留了充分的表现力空间。**这一结果直接验证了骨架表示在控制谱系中的“甜点”假设**（Figure 3）。

### 人工评估

Table 2 和 Table S.1 报告了 300 名参与者的受控在线研究结果。在空间对齐问题上，ChArtist 的平均排名为 **2.957**（第 2 名），与第 1 名 SDEdit（2.897）的差异不显著；在主题一致性问题上，ChArtist 的平均排名为 **2.845**（第 2 名），仅次于 ControlNet-Depth（2.822），且**显著优于 InContext（p < 0.001）**。这表明 ChArtist 在空间保真和视觉表现力两个维度上均达到了顶尖水平，且是唯一在两个维度上同时进入前二的方法。

![[assets/figures/papers/paper_list_l2448_https_arxiv_org_abs_2603_14209/figures/009_Table_2.jpg]]
*Table 2: Human evaluation results from controlled online study (300 participants). Average rank ranges from 1 (best) to N (worst)*

### 双控制任务（Task 1+2）

Table 3 报告了同时施加空间和主题约束的定量结果。在折线图上，ChArtist 的 DINO（视觉一致性）达到 **0.931**，Data Acc 达到 **0.892**，均超越所有双控制基线（ControlNet-Canny + IP-Adapter、ControlNet-Depth + IP-Adapter）及主题驱动方法（Paint-by-Example、InContext）。Figure 8a 的定性对比显示，基线方法常出现结构错位或风格泄漏——例如 IP-Adapter 组合会在图表背景中引入参考图像的元素，破坏数据可读性；而 ChArtist 通过空间门控注意力将主题信号精确约束在数据编码区域，背景保持干净。

![[assets/figures/papers/paper_list_l2448_https_arxiv_org_abs_2603_14209/figures/010_Table_3.jpg]]
*Table 3: Quantitative comparison result of dual control of spatial and subject (Task 1 + Task 2)*

### 消融实验：空间门控注意力的关键作用

**并行 LoRA 合并的失效模式**（Figure 5）：当直接将空间 LoRA（$\text{LoRA}_S$）和主题 LoRA（$\text{LoRA}_R$）并行合并时，出现两类典型伪影——**结构错位**（$\text{LoRA}_R$ 干扰空间控制，使生成结果偏离图表结构）和**风格泄漏**（主题信号溢出到空间约束之外的区域）。这揭示了多条件生成中“条件干扰”的根本问题：独立训练的条件模块在并行组合时缺乏显式依赖关系。

**控制因子 β 的消融**（Table 4, Figure 8b）：空间门控注意力的核心公式为：

$$W_{X R}' = M \odot W_{X R} + \beta \cdot (1 - M) \odot W_{X R}$$

其中 $M$ 为从骨架注意力聚合得到的空间掩码，$\beta$ 控制背景区域的主题表现力。当 $\beta = 0.3$ 时，数据准确率达到最高的 **0.927**，主题信号被严格限制在数据编码区域；当 $\beta = 0.9$ 时，出现严重的背景泄漏，数据准确率显著下降。这证明空间门控注意力通过动态调节主题信号的空间范围，是实现双控制下数据保真度的**必要条件**。

### 公平性说明与局限

需注意以下评估局限性：双控制任务中，部分基线（ControlNet + IP-Adapter）基于 SDXL 架构，而 ChArtist 基于 FLUX 架构，基础模型的生成能力差异可能影响对比公平性。此外，评估所用的 CHARTIST-30K 数据集为程序化合成，其对真实场景中参考图像多样性的覆盖程度尚待验证。

当前方法的主要失败模式包括：对极端拓扑变形（如高度弯曲的折线）难以完美保留参考对象的所有视觉特征；$\beta$ 超参数需根据场景手动调整，缺乏自动化机制；骨架表示目前仅支持条形图、折线图和饼图三种图表类型。

### 补充图表

![[assets/figures/papers/paper_list_l2448_https_arxiv_org_abs_2603_14209/figures/006_Figure_6.jpg]]
*Figure 6: Illustrations of the data accuracy metric. We construct a distance field based on the chart skeleton. Then we randomly sample the points based on the ranges on the distance field, and calculate the accuracy based on a weighted F1 Score*

![[assets/figures/papers/paper_list_l2448_https_arxiv_org_abs_2603_14209/figures/011_Figure_8.jpg]]
*Figure 8: (a) Dual-control generation results conditioned on both spatial structure and subject reference. (b) Results of ChArtsit with different β showcases the importance of Spatially Gated Attention of dual control in ensuring the data accuracy*

![[assets/figures/papers/paper_list_l2448_https_arxiv_org_abs_2603_14209/figures/013_Table_4.jpg]]
*Table 4: Ablation on control factor*

![[assets/figures/papers/paper_list_l2448_https_arxiv_org_abs_2603_14209/figures/012_Figure_9.jpg]]
*Figure 9: Comparison with current SoTA image editing models*



## 定位与知识库关联

### 1. 核心瓶颈与设计动机

象形图生成的核心矛盾在于**结构保真度**与**视觉自由度**之间的冲突。现有控制表示形成了两个极端：密集像素级表示（如Canny边缘、深度图）虽然提供精确的结构约束，却严重限制了参考图像的语义注入空间；稀疏布局表示（如边界框）虽然灵活，却无法为图表的数据维度提供足够的结构指导。ChArtist的设计正是围绕这一瓶颈展开，通过两个关键机制实现平衡：

- **骨架表示**：仅编码图表的数据编码维度（如柱高、折线趋势、扇区角度），在控制谱系中占据“甜点”位置——既忠实编码主数据维度，又为风格注入留有充分空间（Figure 3, Section 4.1）。
- **空间门控注意力**：在推理时建立空间到主题的顺序依赖关系，用空间掩码动态调节主题信号的影响范围，解决并行LoRA组合产生的结构错位与风格泄漏问题（Figure 5, Section 4.3）。

### 2. 与基线方法的关系定位

#### 2.1 空间控制基线

ChArtist在空间对齐任务中与三类基线方法形成对比：

- **密集控制方法**：**ControlNet-Canny** 和 **ControlNet-Depth**（Zhang et al., ICCV 2023）使用Canny边缘或深度图作为控制表示。这些方法在数据准确率上具有竞争力（Table 1），但密集的像素级约束使得后续注入参考图像语义时产生严重冲突——生成结果要么保留原始图表外观，要么在强行注入主题时破坏数据结构。
- **图像编辑方法**：**SDEdit** 和 **Inpainting** 通过噪声扰动或区域修复实现空间控制。SDEdit在人类评估的空间对齐排名中位居第一（平均排名2.897，Table 2），但其编辑范式缺乏对图表数据维度的显式建模，在双控制任务中难以维持数据保真度。
- **骨架表示的优势**：ChArtist的骨架表示在条形图空间对齐中达到Data Acc 0.894（Table 1），同时保持CLIP-T 0.304的文本对齐能力，证明稀疏而精确的控制表示能够在数据保真度与语义表达之间取得更好的平衡。

#### 2.2 双控制基线

在同时要求空间对齐和主题一致性的双控制任务中，ChArtist对比了两类方法：

- **并行LoRA组合**：**ControlNet-Canny + IP-Adapter** 和 **ControlNet-Depth + IP-Adapter** 将空间控制适配器与主题适配器并行合并。Figure 5揭示了这种策略的固有缺陷——主题LoRA会干扰空间控制，导致结构错位（生成元素偏离骨架位置）和风格泄漏（在图表背景区域引入不应出现的视觉元素）。
- **主题驱动生成**：**Paint-by-Example** 和 **InContext** 以参考图像为条件进行生成或编辑。InContext在人类评估的主题一致性上显著劣于ChArtist（p < 0.001，Table 2），表明通用图像编辑方法缺乏对图表数据结构的理解。
- **ChArtist的解决方案**：通过分别训练LoRA_S和LoRA_R，并在推理时使用空间门控注意力建立顺序依赖，ChArtist在折线图双控制中达到Data Acc 0.892和DINO 0.931（Table 3），实现了结构保真与视觉一致性的协同优化。

#### 2.3 方法谱系定位

从控制表示的复杂度谱系（Figure 3）来看：

- **左侧（高复杂度）**：Canny边缘、深度图等密集表示，提供强结构约束但限制视觉自由度。
- **右侧（低复杂度）**：边界框、关键点等稀疏表示，提供高自由度但缺乏结构精度。
- **ChArtist的骨架表示**：位于谱系中段，通过仅编码数据维度（条形图的垂直线、折线图的多段线、饼图的径向线）实现结构精度与语义灵活性的最优权衡。

从多条件交互机制来看，ChArtist的空间门控注意力区别于主流的并行LoRA组合范式，引入了**训练无关的推理时动态门控**，为多条件扩散模型的协调控制提供了新的思路。

### 3. 适用边界与局限

#### 3.1 图表类型覆盖

当前骨架表示仅支持三种图表类型：
- 条形图：单条垂直线表示每根柱子
- 折线图：多段线追踪数据趋势
- 饼图：两条彩色径向线指示扇区的顺时针起止角度

尚未扩展到散点图、雷达图、热力图、箱线图等更复杂的图表拓扑。这些图表类型的数据编码维度与当前骨架范式存在本质差异，需要重新设计控制表示。

#### 3.2 数据分布偏差

训练数据集CHARTIST-30K为程序化合成，虽然保证了骨架-图像对的精确对齐，但可能无法涵盖真实世界中参考图像的多样性和复杂性。模型在以下场景中的泛化能力需要进一步验证：
- 参考图像包含复杂纹理或非典型光照条件
- 图表风格与训练分布显著偏离
- 多图表类型混合的复合可视化

#### 3.3 极端拓扑变形

对于高度弯曲的折线或极端长宽比的条形图，模型有时难以完美保留参考对象的所有视觉特征。这表明骨架表示在极端几何条件下的鲁棒性仍有提升空间。

#### 3.4 超参数敏感性

双控制下的数据准确率受控制因子β的显著影响（Table 4, Figure 8b）：
- β=0.3时数据准确率最高（0.927），空间约束占主导
- β=0.9时出现严重背景泄漏，主题信号过度渗透到非数据区域
- 当前β需根据具体场景手动调整，缺乏自适应机制

### 4. 开放问题与后续方向

#### 4.1 骨架表示的泛化

如何将骨架表示的设计哲学推广到更广泛的图表类型？对于散点图（点位置编码数据）、雷达图（多边形顶点编码数据）、桑基图（流量宽度编码数据）等，需要定义新的骨架原语，同时保持“仅编码数据维度”的设计原则。

#### 4.2 空间门控注意力的迁移

空间门控注意力机制的核心思想——从空间条件推导掩码并动态门控其他条件的影响——能否推广到其他需要严格多条件协调的生成任务？例如：
- 文本驱动的布局到图像生成（空间布局+语义描述）
- 多模态条件生成（深度图+语义分割+文本）
- 视频生成中的时空一致性控制

#### 4.3 自动评估指标的改进

当前的数据准确率度量依赖骨架距离场和加权F1分数（Figure 6），虽然比人工评估更高效，但在以下方面仍有局限：
- 仅评估数据编码区域，无法检测非数据区域的伪影
- 对图表美学质量的评估能力有限
- 与人类感知的一致性需要更大规模验证

开发更精确的自动评估指标来衡量象形图的数据保真度和视觉质量，是减少对人工评估依赖的关键。

#### 4.4 用户交互与动态控制

在实际设计工作流中（Figure S2展示了ChArtist在设计平台中的插件界面），用户对数据准确性与视觉表现力之间存在动态权衡需求。如何实现更直观的控制机制——例如通过滑块实时调节β参数，或通过画笔标记需要严格保持数据精度的区域——是提升实用性的重要方向。

#### 4.5 生成创造性的进一步提升

在保持数据准确性的前提下，如何进一步增强生成结果的视觉创造性？可能的路径包括：
- 引入对抗训练或奖励模型来优化美学质量
- 扩展参考图像库的多样性，增强风格泛化能力
- 探索多参考图像融合，实现更丰富的视觉组合

---

**注意**：部分基线方法（如SDEdit、Inpainting、Paint-by-Example、InContext）的具体作者/会议/年份信息在已核实材料中未提供，建议读者查阅原文获取完整引用。ControlNet-Canny和ControlNet-Depth的引用信息（Zhang et al., ICCV 2023）已在分析中确认。



## 原文 PDF

![[paperPDFs/CVPR_2026/ChArtist_Generating_Pictorial_Charts_with_Unified_Spatial_and_Subject_Control.pdf]]
