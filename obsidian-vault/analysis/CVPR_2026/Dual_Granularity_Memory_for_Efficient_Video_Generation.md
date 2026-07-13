---
title: Dual-Granularity Memory for Efficient Video Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Dual_Granularity_Memory_for_Efficient_Video_Generation.pdf
project_link: null
code_link: null
aliases:
- DGMCMLCAM
- DGMEVG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 通过添加极少量可学习的'汇聚列'（sink columns）作为全局持久锚点，并保留前一块的少量位置作为边界缓冲（boundary buffers），模型获得了跨块信息传递的能力。
primary_logic: 借鉴语言模型中注意力沉没（attention sinks）的思想，将全局上下文压缩到少量可学习位置并适配到循环结构的有向因果传播中；同时利用潜在空间的语义相似性实现跨段记忆检索，避免了相机位姿和帧重建的依赖。
claims:
- Context Memory 通过可学习的汇聚列和边界缓冲维持块内全局上下文，仅增加不足0.1%参数。
- Latent Context-as-Memory (LCaM) 在潜在空间中存储和检索历史嵌入，实现跨段一致性而无需相机注释。
- 双记忆方法在保持与注意力模型相当质量的同时，推理速度提升1.54倍。
- WanVideo-1.3B (8 frames × 480 × 832, 33K tokens) 上 推理延迟 (s) = 67
---

# Dual-Granularity Memory for Efficient Video Generation

> [!tip] 核心洞察
> 借鉴语言模型中注意力沉没（attention sinks）的思想，将全局上下文压缩到少量可学习位置并适配到循环结构的有向因果传播中；同时利用潜在空间的语义相似性实现跨段记忆检索，避免了相机位姿和帧重建的依赖。

| 字段 | 内容 |
|------|------|
| 中文题名 | 高效视频生成的双粒度记忆机制 |
| 英文题名 | Dual-Granularity Memory for Efficient Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Dual-Granularity_Memory_for_Efficient_Video_Generation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | Dual-Granularity Memory (Context Memory + Latent Context-as-Memory) |
| Dataset | WanVideo-1.3B |

> [!tip] 效果简介
> - WanVideo-1.3B (8 frames × 480 × 832, 33K tokens) 上，推理延迟 (s) 67 vs ~103 (基于1.54×加速估算) (-36s (1.54× speedup))。

## 概要

视频生成模型在追求效率时面临一个根本性瓶颈：循环架构（如GSTPN）通过分块并行化实现加速，但这会切断块间的信息流动，导致**块隔离（chunk isolation）**，严重破坏长程时序一致性。**Dual-Granularity Memory**（双粒度记忆机制）针对这一问题，以极低的参数代价（不足0.1%）在分块传播中重建了跨块、跨段的信息通路。

核心思路借鉴了语言模型中**注意力沉没（attention sinks）**的思想——将全局上下文压缩到少量可学习位置，并适配到视频生成的有向因果传播结构中。具体而言，该方法包含两个互补的记忆层次：

- **上下文记忆（Context Memory）**：在单个处理块内部，通过可学习的**汇聚列（sink columns）**作为持久全局锚点，并保留前一块的**边界缓冲（boundary buffers）**维持局部连续性，从而在不破坏并行性的前提下解决块间隔离。
- **潜在上下文记忆（Latent Context-as-Memory, LCaM）**：在视频段之间，维护一个历史潜在嵌入的FIFO内存库，通过基于内容的余弦相似性检索相关历史段，并以交叉注意力融合，实现跨段一致性。该机制完全在潜在空间中运行，无需相机位姿标注或帧重建。

在**WanVideo-1.3B**（8帧×480×832，33K tokens）上，该方法以67秒完成推理，相比全注意力基线（约103秒）实现**1.54倍加速**，同时保持了有竞争力的视觉质量。消融实验表明，汇聚列数量$N_{\text{sink}}=3$、边界缓冲$N_{\text{buf}}=2$、分块大小$L=200$、检索Top-K=3、相似性阈值$T=0.3$为最优配置。

### 视频生成中的效率瓶颈：从注意力机制到循环传播

扩散模型已成为高质量视频生成的主流范式，但其核心计算模块——多头自注意力（Multi-head Self-Attention）——随序列长度呈二次复杂度增长。对于典型的视频生成任务（如8帧×480×832分辨率，约33K tokens），全注意力模型**WanVideo-1.3B**（Team Wan et al., arXiv 2025）的推理延迟高达约103秒，严重制约了实际部署。

为缓解这一问题，研究者提出了一系列高效替代方案：**Videomamba**（Li et al., arXiv 2024）引入状态空间模型，**Dig**（Zhu et al., CVPR 2025）和**Sparse Video-gen**（Xi et al., ICML 2025）分别探索稀疏注意力与线性化注意力。然而，这些方法在降低计算开销的同时，普遍面临一个根本性困境——**时序一致性的退化**。

### 循环传播的核心缺陷：分块隔离与上下文断裂

本文选择在**广义时空传播网络（GSTPN）**（Wang et al., CVPR 2025）的基础上进行改进。GSTPN将自注意力替换为线性复杂度的循环传播，通过将4D视频张量沿不同方向展开为2D序列并进行逐行/逐列的状态传递，实现了显著的计算效率提升。

然而，GSTPN的原始设计存在一个关键瓶颈：**分块隔离（chunk isolation）**。为支持并行化推理，GSTPN必须将长序列切分为多个独立处理的块（chunks），每个块内部的传播被严格限制在块内依赖范围内：

$$\mathcal{D}(j,w) = \{(j',w') \mid w' \in [\lfloor w/L \rfloor \cdot L, w]\}$$

这一约束意味着块与块之间**不存在任何信息传递通道**——前一块的尾部状态完全无法被后一块感知。当视频内容涉及持续的运动轨迹、跨段物理交互或长程场景一致性时，分块隔离直接导致时序断裂和视觉伪影。

### 跨段记忆的缺失：现有方法的局限

更宏观地看，即使解决了块内上下文传递问题，长视频生成还面临**跨段记忆**的挑战。当视频被切分为多个生成段（segments）时，后续段需要访问前序段的视觉上下文以维持全局一致性。现有方法通常依赖以下途径：

- **相机位姿注入**：需要额外的3D标注信息，限制了方法的通用性；
- **帧级重建与检索**：在像素空间存储和匹配历史帧，带来显著的存储和计算开销。

这些方案要么依赖外部标注，要么在效率上做出妥协，缺乏一种**纯潜在空间、无需标注、基于语义相似性的轻量记忆机制**。

### 本文动机：双粒度记忆的协同设计

针对上述两个层次的信息断裂问题，本文提出**双粒度记忆（Dual-Granularity Memory）**框架，从两个互补的粒度切入：

1. **块内粒度**：借鉴语言模型中“注意力沉没”（attention sinks）的思想，在GSTPN的循环传播中引入极少量可学习的**汇聚列（sink columns）**作为全局持久锚点，同时保留前一块的尾部位置作为**边界缓冲（boundary buffers）**，以不足0.1%的参数开销打通块间信息流。

2. **跨段粒度**：设计**潜在上下文记忆（Latent Context-as-Memory, LCaM）**，在潜在空间中维护历史段嵌入的FIFO内存库，通过余弦相似性检索语义相关的历史上下文，并利用交叉注意力进行融合——全程无需相机位姿，也无需帧重建。

这一协同设计使得模型在保持与全注意力基线相当生成质量的前提下，实现**1.54倍推理加速**（67s vs. ~103s），为高效视频生成提供了新的技术路径。

## 核心方法与创新机理

### 瓶颈洞察：从分块隔离到双粒度记忆

循环视频生成模型（如 GSTPN）在并行化时被迫将序列划分为固定大小的块进行处理，这带来了**块间上下文丢失（chunk isolation）** 的根本性瓶颈——每个块只能访问自身范围内的信息，无法感知全局时序依赖，导致长程一致性的退化。本文提出的双粒度记忆机制正是针对这一瓶颈的因果性解决方案：通过**块内上下文记忆（Context Memory）** 和**跨段潜在记忆（Latent Context-as-Memory, LCaM）** 两个互补层级，以极低的参数代价（不足 0.1%）重建了被分块破坏的信息通路。

### Changed Slots：核心计算模块的范式替换

| 替换维度 | 基线方案 | 本文方案 | 创新性质 |
|----------|----------|----------|----------|
| **核心计算模块** | 多头自注意力（Full-Attention WanVideo-1.3B） | GSTPN + 双粒度记忆 | 架构级替换 |
| **块间上下文** | 无（分块隔离） | 汇聚列（sink columns）作为全局持久锚点 | 机制创新 |
| **块边界连续性** | 无 | 边界缓冲（boundary buffers）保留前块尾部信息 | 机制创新 |
| **跨段记忆** | 无 | LCaM：潜在空间相似性检索 + 交叉注意力融合 | 机制创新 |

### Context Memory：汇聚列与边界缓冲的协同设计

Context Memory 包含两个互补组件，共同解决块内传播的上下文断裂问题：

**汇聚列（Sink Columns）** 借鉴了语言模型中“注意力沉没”（attention sinks）的思想，将其适配到循环网络的有向因果传播结构中。具体而言，每个块的前 $N_{\text{sink}}$ 个位置（消融实验确定最优值为 3）被指定为**可学习的全局锚点**，在整个生成过程中持续存在。在 GSTPN 的行传播过程中，汇聚列通过扩展的传播公式向所有后续位置注入全局上下文：

$$h_{j,w} = w_j h_{j-1,w-1} + \lambda_j \odot x_{j,w} + \sum_{i \in S} G_{\text{sink}}[j,i] \odot h_{j,i}$$

其中 $S$ 为汇聚列索引集合，$G_{\text{sink}}$ 为汇聚列到当前行的变换矩阵。这使得每个位置都能直接访问块外的全局信息，从根本上打破了分块隔离。

**边界缓冲（Boundary Buffers）** 则保留前一个块的最后 $N_{\text{buf}}$ 个位置（消融确定最优值为 2），作为当前块的“历史前缀”。这为块间过渡提供了局部连续性，平滑了分块边界处的信息断裂。

两个组件的参数总量仅约 15 万（不足总参数的 0.1%），却带来了显著的质量提升：汇聚列从 0 到 3 列使 VBench 得分提升 +4.4 分，边界缓冲进一步贡献 +0.7 分。

### Latent Context-as-Memory：免相机标注的跨段记忆

LCaM 是本文最具辨识度的创新之一。与现有方法依赖相机位姿估计和帧重建来实现跨段一致性不同，LCaM **完全在潜在空间中操作**，通过三个关键设计实现了轻量且高效的跨段记忆：

1. **FIFO 内存库**：维护最近 $M$ 个视频段的潜在嵌入队列 $\mathcal{M}_{t} = \{ z_{\tau} \mid \tau \in [\max(1, t-M), t-1] \}$，以先进先出策略保证 $O(M)$ 的内存复杂度。

2. **内容相似性检索**：通过时空平均池化将每个潜在段压缩为固定维度的全局描述子 $\mathcal{F}(z)$，利用余弦相似度 $s(z_t, z_{\tau})$ 进行语义匹配，在超过阈值 $T=0.3$ 的候选中选取 Top-K（$K=3$）最相似的历史段。该阈值下检索命中率达 74%，精度达 79%。

3. **门控交叉注意力融合**：检索到的历史上下文通过多头交叉注意力以门控残差方式注入当前潜在：
   $$z_t^{\text{cond}} = z_t + \sigma(g) \cdot \text{Unflatten}(\mathbf{O})$$
   其中可学习门控参数 $g$ 控制记忆信息的融入强度，避免无关上下文干扰生成质量。

LCaM 的理论压缩比 $\rho = 3s^2 / C_z$（$s$ 为 VAE 下采样倍数，$C_z$ 为潜在通道数）远优于存储原始帧的方案，且完全规避了相机位姿标注的工程负担。

### 创新总结

双粒度记忆的核心创新在于**以因果性思维解决循环网络的并行化困境**：Context Memory 通过汇聚列将全局上下文压缩到极少量可学习位置，实现了块内的信息贯通；LCaM 则利用潜在空间的语义相似性实现了跨段记忆检索，将时序一致性的维护从显式的几何约束解放为隐式的语义匹配。两者协同，使得 GSTPN 在保持 1.54× 推理加速的同时，达到了与全注意力模型相当的生成质量。

Dual-Granularity Memory 框架围绕一个核心矛盾展开：循环传播网络（GSTPN）天然适配并行分块计算，但分块操作会切断块间的时序信息流，即**块隔离（chunk isolation）**问题。为解决这一瓶颈，该框架在 GSTPN 架构中注入了两层互补的记忆机制——**上下文记忆（Context Memory）**负责块内全局锚定与块间边界平滑，**潜在上下文记忆（Latent Context-as-Memory, LCaM）**负责跨视频段的长期一致性。

### 总体流水线

整个框架建立在 **WanVideo-1.3B**（Team Wan et al., arXiv 2025）之上，将其全部自注意力层替换为增强型 GSTPN 模块。输入为 4D 视频张量 $X \in \mathbb{R}^{C \times F \times H \times W}$，流水线按以下阶段运作：

1. **多方向时空扫描**：将 4D 张量沿三种互补方向重塑为 2D 投影，分别捕获不同的时空依赖关系：
   - **ST（空间-时间）**：$(C, F, H, W) \mapsto (C, HW, F)$
   - **WTH（宽-时间-高）**：$(C, F, H, W) \mapsto (C, WF, H)$
   - **HTW（高-时间-宽）**：$(C, F, H, W) \mapsto (C, HF, W)$

   三种投影各自经过带上下文记忆的 GSPN 传播，再通过可学习权重 $\alpha_o = \frac{e^{\beta_o}}{\sum_{o'} e^{\beta_{o'}}}$ 加权融合，经 MLP $\Psi$ 得到该层的输出。

2. **上下文记忆（Context Memory）**：嵌入在每一个 GSTPN 层内部，由两个组件构成：
   - **汇聚列（sink columns）**：将每个分块的前 $N_{\text{sink}}$ 个位置（通常 2–4 个）设为全局可访问的持久锚点。传播公式扩展为：
     
$$
h_{j,w} = w_j h_{j-1,w-1} + \lambda_j \odot x_{j,w} + \sum_{i \in S} G_{\text{sink}}[j,i] \odot h_{j,i}
$$

     其中 $S$ 为汇聚列索引集。这些锚点在整个生成过程中持续存在，打破了分块依赖约束 $\mathcal{D}(j,w) = \{(j',w') \mid w' \in [\lfloor w/L \rfloor \cdot L, w]\}$ 带来的信息隔离。
   - **边界缓冲（boundary buffers）**：保留前一个分块的尾部 $N_{\text{buf}}$ 个位置（通常 2 个），为当前块提供局部连续性，平滑块间过渡。

   这两个组件仅增加约 15 万参数（不足总参数的 0.1%），几乎不引入计算开销。

3. **潜在上下文记忆（LCaM）**：在 GSTPN 层之上运行，维护一个 FIFO 记忆库 $\mathcal{M}_t$，存储最近 $M$ 个视频段的潜在嵌入 $z_\tau$。其工作流程为：
   - **全局描述子提取**：通过时空平均池化将每个潜在段压缩为固定维度向量：
     
$$
\mathcal{F}(z) = \frac{1}{T H' W'} \sum_{f=1}^{T} \sum_{h=1}^{H'} \sum_{w=1}^{W'} z[:,f,h,w]
$$

   - **相似性检索**：计算当前段与记忆库中所有段的余弦相似度，筛选出超过阈值 $T$ 的候选项，取 Top-K 最相似段构成检索集 $\mathcal{R}_t$。
   - **交叉注意力融合**：将检索到的历史潜在嵌入作为上下文，通过多头交叉注意力与当前潜在交互，并以可学习门控 $g$ 进行残差注入：
     
$$
z_t^{\text{cond}} = z_t + \sigma(g) \cdot \text{Unflatten}(\mathbf{O})
$$

   
   LCaM 完全在潜在空间操作，无需相机位姿标注或帧重建，利用潜在空间的语义相似性实现跨段一致性。

4. **训练目标**：总损失函数联合三项：
   
$$
\mathcal{L} = \mathcal{L}_{\text{distil}}(\hat{z}_t, z_t^{\text{teach}}) + \lambda_{\text{align}} \mathcal{L}_{\text{align}}(\mathcal{D}(\hat{z}_t), x_t^{\text{teach}}) + \mathbb{1}_{|\mathcal{M}_t|>0} \mathcal{L}_{\text{mem}}
$$

   - $\mathcal{L}_{\text{distil}}$：从全注意力教师模型蒸馏。
   - $\mathcal{L}_{\text{align}}$：可选的像素空间对齐损失。
   - $\mathcal{L}_{\text{mem}} = \lambda_{\text{mem}} \| \hat{z}_t^{\text{cond}} - \text{sg}(\hat{z}_t) \|_F^2$：内存一致性正则项，鼓励条件化输出不偏离原始预测，防止检索噪声引入伪影。

### 模块间关系

两层记忆机制形成**粒度互补**：Context Memory 解决单个视频段内部的块间隔离，属于细粒度时序一致性保障；LCaM 跨越多个视频段，通过潜在检索实现粗粒度的长期语义一致性。二者共享 GSTPN 的循环传播骨干，LCaM 的检索与融合发生在 GSTPN 层间，而 Context Memory 则嵌入在每一层的传播过程中。这种分层设计使得模型在保持 1.54 倍推理加速（67s vs. ~103s，WanVideo-1.3B 8帧 480×832 设定）的同时，在 VBench 各维度上达到与全注意力基线相当的质量。

### 问题背景：循环生成中的分块隔离

循环视频生成模型（如 GSTPN）具有天然的因果结构，适合逐帧自回归生成。然而，当需要并行加速时，模型被迫将长序列切分为多个块（chunk）独立处理，每个块内部的前驱依赖被截断至块内，导致**块间上下文丢失**（chunk isolation），破坏了长程时序一致性。本文的核心挑战在于：如何在保持循环传播高效性的同时，为分块并行注入跨块信息传递能力。

### 基础模块：广义时空传播网络（GSTPN）

GSTPN 是本文的底层计算骨架，用于替代标准的多头自注意力。其核心思想是将 2D 线性传播推广到视频的时空维度。

**行传播公式**（2D 线性传播基础）：

$$h_{i}^{c} = w_{i}^{c} h_{i-1}^{c} + \lambda_{i}^{c} \odot x_{i}^{c}$$

其中 $h_{i}^{c}$ 是第 $i$ 行第 $c$ 通道的隐藏状态，$w_{i}^{c}$ 是传播权重，$\lambda_{i}^{c}$ 是输入调制门，$x_{i}^{c}$ 是输入特征。该公式刻画了沿序列方向的信息累积过程：当前状态由上一状态加权传播与当前输入的调制叠加构成。

**全局变换矩阵**：将上述逐行传播展开为全局线性变换 $Y = GX$，其中变换矩阵 $G$ 具有分块下三角结构：

$$G_{ij} = \left\{ \begin{array}{ll} \left( \prod_{\tau=j+1}^{i} w_{\tau} \right) \lambda_{j}, & j < i, \\ \lambda_{j}, & i = j. \end{array} \right.$$

这一结构保证了因果性（位置 $i$ 只能看到 $j \leq i$ 的信息），同时揭示了传播权重 $w$ 和输入门 $\lambda$ 如何共同决定长程依赖的强度。

**权重归一化**：为保证传播稳定性，权重矩阵的每一行满足随机性质（非负且和为 1）：

$$w_{i,j,k} = \frac{\sigma(\tilde{w}_{i}^{k})}{\sum_{k'} \sigma(\tilde{w}_{i}^{k'})}$$

其中 $\sigma$ 为 sigmoid 函数，$\tilde{w}_{i}^{k}$ 为无约束可学习参数。该归一化使得传播过程具有收缩性，避免梯度爆炸。

**分块依赖约束**：在分块并行模式下，每个位置的可见前驱被限制在当前块内：

$$\mathcal{D}(j,w) = \{(j',w') \mid w' \in [\lfloor w/L \rfloor \cdot L, w]\}$$

其中 $L$ 为块大小。这一约束直接导致了块间信息隔离，是本文双粒度记忆机制要解决的核心矛盾。

### 核心模块一：上下文记忆（Context Memory）

上下文记忆在 GSTPN 的块内传播中嵌入两类可学习位置，以极低的参数代价（约 15 万参数，不足总参数的 0.1%）恢复跨块信息流。

**汇聚列（Sink Columns）**：借鉴语言模型中“注意力沉没”（attention sinks）的思想，在每个块的前 $N_{\text{sink}}$ 个位置（通常 2-4 个）设置全局可访问的锚点。这些位置不参与正常的因果传播，而是作为持久化的全局上下文载体，在所有块中共享。带汇聚列的传播公式为：

$$h_{j,w} = w_j h_{j-1,w-1} + \lambda_j \odot x_{j,w} + \sum_{i \in S} G_{\text{sink}}[j,i] \odot h_{j,i}$$

其中 $S$ 为汇聚列索引集合，$G_{\text{sink}}$ 为汇聚列到当前行的专用变换矩阵。第三项使得每个位置都能直接从汇聚列中读取全局信息，打破了块边界的因果隔离。

**边界缓冲（Boundary Buffers）**：每个块保留前一块尾部的 $N_{\text{buf}}$ 个位置（通常 2 个）作为缓冲，为块间过渡提供局部连续性。这些缓冲位置存储的是前一块的真实隐藏状态，而非可学习参数，因此不引入额外参数量。

**设计直觉**：汇聚列提供“全局锚点”（粗粒度），边界缓冲提供“局部平滑”（细粒度），二者互补地解决了块隔离问题。汇聚列的有效性源于：全局上下文可以被压缩到极少量的可学习位置中，而无需存储完整的块间依赖矩阵。

### 核心模块二：潜在上下文记忆（LCaM）

LCaM 将记忆机制从块内扩展到段间，在潜在空间中维护历史信息并实现跨段检索与融合，无需相机位姿标注或帧重建。

**内存库定义**：维护一个容量为 $M$ 的 FIFO 队列，存储最近 $M$ 个视频段的潜在表示：

$$\mathcal{M}_{t} = \{ z_{\tau} \ | \ \tau \in [ \max(1, t-M), t-1 ] \cap \mathbb{Z}^{+} \}$$

当新段 $z_t$ 生成后，触发 FIFO 替换：$\mathcal{M}_{t+1} = (\mathcal{M}_{t} \setminus \{z_{t-M}\}) \cup \{z_t\}$，保证内存复杂度为 $O(M)$。

**理论压缩比**：相比存储原始帧，潜在空间存储具有显著优势：

$$\rho = \frac{S_{\mathrm{raw}}}{S_{\mathrm{latent}}} = \frac{3 s^{2}}{C_{z}}$$

其中 $s$ 为 VAE 下采样倍数，$C_z$ 为潜在通道数。这一压缩使得在有限显存下维护长程历史成为可能。

**全局描述子与检索**：对每个潜在段进行时空平均池化，得到固定维度的描述向量：

$$\mathcal{F}(z) = \frac{1}{T H' W'} \sum_{f=1}^{T} \sum_{h=1}^{H'} \sum_{w=1}^{W'} z[:,f,h,w]$$

基于余弦相似度进行内容检索：

$$s(z_{t}, z_{\tau}) = \frac{\langle \mathcal{F}(z_{t}), \mathcal{F}(z_{\tau}) \rangle}{\|\mathcal{F}(z_{t})\|_{2} \|\mathcal{F}(z_{\tau})\|_{2}}$$

检索集为满足相似度阈值 $T$ 的候选段中 Top-K 最相似者：

$$\mathcal{R}_{t} = \mathrm{TopK}(\mathcal{C}_{t}; s(z_{t}, \cdot))$$

其中候选集 $\mathcal{C}_{t} = \{z_{\tau} \in \mathcal{M}_{t} \mid s(z_t, z_{\tau}) \geq T\}$。

**交叉注意力融合**：检索到的历史潜在段通过多头交叉注意力融入当前段，并采用门控残差连接：

$$z_{t}^{\mathrm{cond}} = z_{t} + \sigma(g) \cdot \mathrm{Unflatten}(\mathbf{O})$$

其中 $\mathbf{O}$ 为交叉注意力输出，$\sigma(g)$ 为可学习门控标量，控制记忆信息的注入强度。门控机制允许模型在不需要记忆信息时自动衰减其影响。

### 多方向时空扫描

为捕获视频中复杂的时空依赖，GSTPN 将 4D 视频张量 $(C, F, H, W)$ 分解为三种 2D 投影：

$$\mathcal{T}_{\mathrm{ST}}(X): (C,F,H,W) \mapsto (C,HW,F)$$
$$\mathcal{T}_{\mathrm{WTH}}(X): (C,F,H,W) \mapsto (C,WF,H)$$
$$\mathcal{T}_{\mathrm{HTW}}(X): (C,F,H,W) \mapsto (C,HF,W)$$

三种投影分别在“空间-时间”、“宽度-时间-高度”、“高度-时间-宽度”三个方向上执行线性传播，捕获互补的时空依赖模式。三个方向的输出通过可学习权重融合：

$$Y = \Psi(\bigoplus_o \alpha_o Y_o; \Theta), \quad \alpha_o = \frac{e^{\beta_o}}{\sum_{o'} e^{\beta_{o'}}}$$

其中 $\alpha_o$ 为 softmax 归一化的方向权重，$\Psi$ 为 MLP 融合网络。消融实验证实，三种方向组合（ST+WTH+HTW）相比单一方向显著提升整体 VBench 得分至 83.5（Table 2）。

### 训练目标

总损失函数联合知识蒸馏与内存一致性正则化：

$$\mathcal{L} = \mathcal{L}_{\mathrm{distil}}(\hat{z}_{t}, z_{t}^{\mathrm{teach}}) + \lambda_{\mathrm{align}} \mathcal{L}_{\mathrm{align}}(\mathcal{D}(\hat{z}_{t}), x_{t}^{\mathrm{teach}}) + \mathbb{1}_{|\mathcal{M}_{t}|>0} \mathcal{L}_{\mathrm{mem}}$$

其中 $\mathcal{L}_{\mathrm{distil}}$ 为与教师模型（**Full-Attention WanVideo-1.3B**，Team Wan et al., arXiv 2025）潜在空间的蒸馏损失，$\mathcal{L}_{\mathrm{align}}$ 为可选的像素空间对齐损失，$\mathcal{L}_{\mathrm{mem}}$ 为内存一致性损失：

$$\mathcal{L}_{\mathrm{mem}} = \lambda_{\mathrm{mem}} \| \hat{z}_{t}^{\mathrm{cond}} - \mathrm{sg}(\hat{z}_{t}) \|_{F}^{2}$$

该损失鼓励 LCaM 条件化后的输出与原始输出保持一致，防止检索到的历史信息引入不相关干扰，起到正则化作用。$\mathrm{sg}(\cdot)$ 为停止梯度算子，仅更新条件化分支。

## 实验与关键发现

### 主结果：质量与效率的权衡

Table 1 展示了在 WanVideo-1.3B（8帧 × 480 × 832，约33K tokens）上，Dual-Granularity Memory 与全注意力基线及高效模型基线的对比。核心发现如下：

![[assets/figures/papers/paper_list_l862_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Dual_Granularity/figures/002_Table_1.jpg]]
*Table 1: Qualityandefciencycomparisonon WanVideo-1.3B(8frames×480×832,33Ktokens).Boldindicatesbestamongefcient methods*

- **推理速度**：本方法达到 67s 的推理延迟，相比全注意力 WanVideo-1.3B 基线实现 **1.54× 加速**，是所有对比方法中推理最快的。
- **生成质量**：在 VBench 各项指标上，本方法在成像质量（IQ: 62.3）上领先于其他高效方法，同时在语义一致性（SC: 92.8）、视频时序一致性（VT: 81.0）等维度保持竞争力，视觉质量与全注意力模型相当。
- **参数开销**：Context Memory 仅增加约 150K 可学习参数（不足总参数量 0.1%），几乎不带来额外计算负担。

这一结果表明，GSTPN + 双粒度记忆的组合成功打破了循环模型分块处理带来的“块间隔离”瓶颈——Context Memory 的汇聚列和边界缓冲维持了块内全局上下文，LCaM 则跨越视频段提供历史语义锚定，二者协同使得线性复杂度的传播网络在质量上逼近平方复杂度的全注意力。

### 消融实验

#### 扫描方向组合

Table 2 的消融实验考察了多方向扫描对生成质量的影响。单一方向（仅 ST）的 VBench 总分最低；加入 WTH 或 HTW 后质量逐步提升；**三种方向联合（ST + WTH + HTW）** 取得最佳总分 83.5。这验证了不同投影方向捕获互补时空依赖的假设——ST 扫描建模空间-时间耦合，WTH 和 HTW 则分别从宽度-时间和高度-时间维度补充信息。

![[assets/figures/papers/paper_list_l862_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Dual_Granularity/figures/004_Table_2.jpg]]
*Table 2: Ablation on scanning orientations.Three orientations achieve best quality through complementary spatiotemporal coverage.Quality represents overall VBench score*

#### 汇聚列数量与边界缓冲

Figure 2 展示了 Context Memory 两个关键超参数的消融曲线：

- **汇聚列数量 $N_{\text{sink}}$**：从 0 增加到 3 时，VBench 质量得分急剧提升 **+4.4 分**；继续增加到 5 或更多时收益递减并趋于平台。这表明 3 个可学习汇聚位置已足以提供有效的全局锚点，更多列反而引入冗余。
- **边界缓冲大小 $N_{\text{buf}}$**：$N_{\text{buf}} = 2$ 时质量提升 **+0.7 分**，有效平滑了块间过渡；更大的缓冲未带来额外收益，说明保留前一块尾部 2 个位置的信息即可满足局部连续性需求。

#### 分块大小

Table 3 考察了分块大小 $L$ 对质量-效率权衡的影响。$L = 200$ 取得了最佳平衡：过小的块（如 $L = 100$）导致过多的块间边界，累积上下文损失；过大的块（如 $L = 400$）虽减少边界数量，但单块内传播路径过长，反而削弱了并行化收益。

![[assets/figures/papers/paper_list_l862_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Dual_Granularity/figures/005_Table_3.jpg]]
*Table 3: Ablation on chunk size*

#### 检索 Top-K 与相似性阈值

LCaM 的检索机制受两个超参数控制：

- **Top-K**（Table 4）：$K = 3$ 取得最佳质量和人类偏好评分。当 $K$ 增大到 5 或更多时，检索到的段平均相似度下降，引入不相关上下文反而损害生成质量。
- **相似性阈值 $T$**（Table 5）：$T = 0.3$ 最优，此时检索命中率 74%、精度 79%，在检索数量与质量间取得平衡。过高阈值导致检索过少、跨段记忆失效；过低阈值则引入噪声。

![[assets/figures/papers/paper_list_l862_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Dual_Granularity/figures/007_Table_4.jpg]]
*Table 4: Ablation on retrieval top-K.K = 3 achieves optimal quality and human preference.Higher K includes less relevant segments (declining average similarity)*

![[assets/figures/papers/paper_list_l862_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Dual_Granularity/figures/008_Table_5.jpg]]
*Table 5: ．Ablation on similarity threshold.T = O.3 optimally balances retrieval quantity and quality.Precision based on manual annotation of 10o samples*

### 定性分析

Figure 3 展示了复杂动态和大运动场景下的生成效果。在“熊猫冲浪”场景中，波浪动态和水花效果准确且时序一致；“猫喝水”场景中水面涟漪传播自然连贯；“双人舞蹈”场景中即使存在大幅度姿态变化，空间结构仍保持一致。这些案例表明，双粒度记忆框架（Context Memory + LCaM）使模型能够跨时间段建模物理交互和大幅运动，避免了分块处理常见的时序断裂和物体畸变。

![[assets/figures/papers/paper_list_l862_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Dual_Granularity/figures/006_Figure_3.jpg]]
*Figure 3: Qualitative results on complex dynamics and large motions. Our method captures diverse challenging scenarios. Top:A panda surfing with accurate wave dynamics and water splash efects. Middle: A cat drinking from a bowl generating realistic water ripples that propagate consistently. Bottom: Two dancers performing with large-scale movements,demonstrating maintained spatial coherence despite significant pose variations. The dual-memory framework (Context Memory + LCaM) enables coherent modeling across temporal segments for both physical interactions and large movements*

### 失败模式与局限性

尽管整体表现优异，分析中未提供系统性的失败案例讨论。从方法设计可推断以下潜在局限需人工验证：

1. **长视频生成中的记忆饱和**：LCaM 的 FIFO 内存库容量 $M$ 固定，当视频长度远超 $M$ 个段时，早期语义信息将被彻底遗忘，可能导致长程一致性退化。
2. **相似性检索的语义歧义**：基于潜在空间余弦相似度的检索在语义相似但视觉不相关的场景（如重复纹理、相似背景）中可能误检索，阈值 $T$ 的调节无法完全消除此类错误。
3. **汇聚列的泛化能力**：汇聚列作为可学习参数在训练分布内有效，但在分布外（如极端分辨率、非常规帧率）的迁移能力未经检验。

## 定位与知识库关联

### 1. 技术脉络与基线关系

本工作处于**高效视频生成模型**的研究脉络中，其核心动机源于对循环式时空传播网络（GSTPN）分块并行化所导致的“块隔离”问题的解决。论文的基线体系可分为三个层次：

**（1）注意力基线：Full-Attention WanVideo-1.3B（Team Wan et al., arXiv 2025）**
作为教师模型和性能上界，完整自注意力机制保证了全局时空交互，但推理延迟高达约103秒（33K tokens场景）。本方法将其作为知识蒸馏的目标，在保持竞争性生成质量的同时实现1.54倍加速。

**（2）无记忆循环基线：vanilla GSTPN（Wang et al., CVPR 2025）**
GSTPN通过三对角传播矩阵替代自注意力，将复杂度从二次降为线性。然而，分块并行化强制将序列切分为独立块，切断了块间的信息流动。本方法正是在此基础上引入了双粒度记忆机制，直接修补了这一结构性缺陷。

**（3）同期高效模型基线**
- **Videomamba**（Li et al., arXiv 2024）：基于状态空间模型的高效视频生成方法，代表了不同于传播网络的另一技术路线。
- **Dig**（Zhu et al., CVPR 2025）和 **Sparse Video-gen**（Xi et al., ICML 2025）：在注意力稀疏化或选择性计算方面探索效率提升，但均未显式建模跨块/跨段的持久记忆。

本方法的独特定位在于：**在保持GSTPN线性复杂度优势的前提下，通过极轻量（<0.1%参数）的记忆机制恢复被分块破坏的全局上下文**，而非重新引入昂贵的全局注意力。

### 2. 核心机制的知识来源与创新

**（1）Attention Sinks 的迁移与适配**
上下文记忆（Context Memory）中的汇聚列（sink columns）设计直接借鉴了语言模型中“注意力沉没”（attention sinks）现象的发现——即少数初始token在注意力分布中吸收了不成比例的权重。本工作将这一思想从Transformer的自注意力机制迁移到循环传播网络中，将其重新解释为**可学习的全局锚点**，并通过有向因果传播结构进行适配。创新点在于：汇聚列不再是注意力计算中的被动现象，而是主动设计的持久信息载体，在每块处理时注入全局上下文。

**（2）潜在空间记忆的语义检索范式**
潜在上下文记忆（LCaM）区别于两类常见的跨段一致性方案：
- **基于相机位姿的方案**：需要显式的3D几何信息，限制了应用场景。
- **基于帧重建的方案**：在像素或解码空间进行匹配，计算开销大且易受低层纹理干扰。

LCaM的独特之处在于**在潜在空间中完成“存储-检索-融合”的全流程**：利用VAE潜在编码的语义紧凑性，通过时空平均池化获得全局描述子，以余弦相似度进行内容检索，再通过门控交叉注意力将历史上下文融入当前生成。这一设计既避免了相机标注的依赖，又通过潜在空间的压缩比（理论值 $\rho = 3s^2 / C_z$）大幅降低了存储开销。

### 3. 适用边界与条件

基于论文的实验设置和消融分析，本方法的适用边界可归纳如下：

**（1）分块场景的必要性**
上下文记忆的收益与分块大小直接相关。Table 3显示，当分块大小 $L=200$ 时达到最佳平衡；若不分块（全序列处理），汇聚列和边界缓冲的增益将消失。因此，该方法特别适用于长序列生成场景，其中分块并行化是必要的加速手段。

**（2）检索质量的阈值依赖**
LCaM的有效性依赖于检索精度。Table 5表明，相似性阈值 $T=0.3$ 时检索命中率74%、精度79%，这是基于100个样本人工标注的经验最优值。当潜在空间中语义相似的段在视觉上并不连贯时（例如场景切换），检索可能引入不相关上下文，此时门控机制（$\sigma(g)$）可部分抑制其影响，但无法完全消除。

**（3）教师模型的质量上限**
本方法通过知识蒸馏从Full-Attention WanVideo-1.3B迁移知识，其生成质量受教师模型能力约束。在教师模型本身表现不佳的场景（如极复杂物理交互），学生模型无法超越。

### 4. 局限与开放问题

**（1）检索机制的场景敏感性**
LCaM基于潜在空间的余弦相似度进行检索，隐式假设“语义相似”等价于“时序上可复用”。在包含重复性动作（如舞蹈、运动）的场景中该假设成立，但在叙事性强、场景持续变化的视频中，检索到的历史段可能与当前上下文产生语义冲突。论文未提供此类失败案例的分析。

**（2）汇聚列的静态性质**
汇聚列作为全局锚点是可学习的，但在生成过程中保持固定（不随内容更新）。这可能限制了其对动态变化上下文的适应能力。是否需要引入内容依赖的汇聚列更新机制，是一个开放问题。

**（3）多段生成的累积误差**
LCaM的FIFO内存库维护最近M个段的潜在表示。随着生成长度增加，早期段的潜在表示被逐出内存库，可能导致长程一致性逐渐衰减。论文未讨论M值（内存容量）与生成长度之间的关系，需人工验证。

**（4）泛化到其他架构**
本方法深度嵌入GSTPN的传播框架，汇聚列和边界缓冲的设计依赖于行传播的有向因果结构。将其迁移到其他高效架构（如Mamba类状态空间模型）的可行性尚未得到验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/Dual_Granularity_Memory_for_Efficient_Video_Generation.pdf]]
