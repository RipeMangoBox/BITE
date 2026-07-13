---
title: "EvoComp: Learning Visual Token Compression for Multimodal Large Language Models via Semantic-Guided Evolutionary Labeling"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EvoComp_Learning_Visual_Token_Compression_for_Multimodal_Large_Language_Models_via_Semantic_Guided_Evolutionary_Labeling.pdf
project_link: null
code_link: null
aliases:
- EvoComp
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: EvoComp
primary_logic: EvoComp
claims:
- EvoComp
---

# EvoComp: Learning Visual Token Compression for Multimodal Large Language Models via Semantic-Guided Evolutionary Labeling

> [!tip] 核心洞察
> EvoComp

| 字段 | 内容 |
|------|------|
| 中文题名 | EvoComp: Learning Visual Token Compression for Multimodal Large Language Models via Semantic-Guided Evolutionary Labeling |
| 英文题名 | EvoComp: Learning Visual Token Compression for Multimodal Large Language Models via Semantic-Guided Evolutionary Labeling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.17087) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method |  |
| Dataset | GQA, MMBench, MMBench-CN, POPE, VQAv2, VizWiz |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

多模态大语言模型（MLLM）在视觉-语言理解任务上表现优异，但高分辨率图像或视频带来的大量视觉 token 严重推高了推理延迟和显存开销，限制了其在资源受限设备上的部署。现有视觉 token 压缩方法多依赖启发式规则或冻结的轻量模块，其保留决策与 MLLM 的任务损失缺乏直接对齐，导致压缩后性能退化显著。

EvoComp 提出了一种**语义引导的进化标注**框架来解决这一问题。其核心思路是：在 MLLM 的对齐模块与大语言模型之间插入一个可训练的轻量 Transformer 压缩器，该压缩器接收对齐后的视觉与文本嵌入，输出每个视觉 token 的保留概率；而训练该压缩器所需的监督信号，则由一个进化搜索算法生成——该算法在语义分组的约束下，搜索使 MLLM 任务损失最小化的二值掩码，从而将 token 保留决策与下游任务性能直接对齐。

在 LLaVA-1.5-7B 上，EvoComp 在 3 倍压缩（192 tokens）下保留了原始精度的 **99.3%**，在 9 倍压缩（64 tokens）下仍保留 **94.9%**，同时端侧推理实现最高 **1.6×** 加速。该方法在六个视觉-语言理解基准（GQA、MMB、MMB-CN、POPE、TextVQA、VizWiz）上验证了有效性，并展现出跨模型（LLaVA-1.5-13B、Qwen2.5-VL-7B）和跨架构（LLaVA-NeXT-7B 高分辨率场景）的迁移能力。

多模态大语言模型（MLLM）在视觉-语言理解任务上取得了显著进展，但其推理效率受到视觉标记数量过大的严重制约。以 LLaVA-1.5-7B 为例，每张输入图像经视觉编码器（如 CLIP ViT）处理后会产生 576 个视觉标记，这些标记与文本标记一同送入大语言模型（LLM）进行自回归生成。视觉标记的数量直接决定了 LLM 预填充阶段的计算量和 KV 缓存的内存占用，成为端侧部署和实时应用的核心瓶颈。

现有视觉标记压缩方法大致可分为两类。一类是基于聚类或采样的无训练方法，如直接对视觉标记进行空间下采样或基于相似度合并，这类方法虽无需额外训练，但压缩后的标记往往丢失关键语义信息，导致下游任务性能显著下降。另一类是基于可学习选择器的方法，通过引入轻量级模块预测每个视觉标记的重要性分数并据此筛选。然而，这类方法面临一个根本性难题：**缺乏高质量的真值监督信号**。由于无法直接获知哪些视觉标记对 MLLM 的任务输出最为关键，现有方法通常依赖启发式规则（如与文本标记的注意力权重）或自监督目标来训练选择器，这些代理信号与 MLLM 的实际任务损失之间存在不可忽视的偏差，限制了压缩率的进一步提升。

针对上述困境，本文提出 EvoComp，其核心动机是**直接以 MLLM 的任务损失为优化目标，通过进化搜索为视觉标记压缩提供语义感知的高质量真值标签**。具体而言，EvoComp 在视觉-语言对齐模块与 LLM 之间插入一个基于 Transformer 的轻量级压缩器，该压缩器接收对齐后的视觉和文本嵌入，输出每个视觉标记的保留概率。压缩器的训练监督信号并非来自人工标注或启发式规则，而是通过进化算法在语义分组约束下搜索最优二元掩码——该掩码最小化 MLLM 在保留标记子集上的任务损失，同时通过语义分组策略消除冗余标记。这一设计使得压缩器能够学习到与任务目标直接对齐的标记选择策略，从而在高压缩比下仍保持优异的性能保留。

## 核心方法与创新机理

EvoComp 的核心创新在于**将视觉 Token 压缩从启发式规则或静态剪枝，转变为一个与 MLLM 任务损失直接对齐的进化搜索驱动学习范式**。该方法围绕两个紧密耦合的 changed slots 展开：**监督标签的生成方式**与**压缩器的训练目标**。

### 1. 进化标签生成：将 Token 选择对齐到 MLLM 输出损失

传统压缩方法通常依赖注意力分数、CLIP 相似度等代理指标来决定 Token 的保留/丢弃，这些指标与 MLLM 最终的任务性能之间存在语义鸿沟。EvoComp 的关键突破在于提出了一种**进化标注策略**（Evolutionary Labeling）：对于每个训练样本，在视觉 Token 上搜索一个二值掩码 $\mathbf{m} \in \{0,1\}^n$，使得在仅保留 $\mathbf{m}$ 标记的视觉 Token 和全部文本 Token 的条件下，MLLM 在目标任务上的损失最小化。

搜索过程采用进化算法实现：维护一个大小为 $q=48$ 的候选掩码种群，每轮选取损失最低的 $p=12$ 个父代，通过交叉和变异生成子代，迭代 $L=10$ 轮后，将历史最低损失的候选作为该样本的监督标签。这一机制确保压缩器学习到的保留概率**直接与 MLLM 的下游任务性能因果对齐**，而非依赖任何间接的启发式信号。

### 2. 语义分组策略：显式建模 Token 冗余

在进化搜索中引入**语义分组**（Semantic Grouping）是该方法的第二个关键设计。具体而言，计算每个视觉 Token $\pmb{v}_i$ 与 LLM 词汇表嵌入 $\pmb{e}_j$ 的余弦相似度 $S_{ij}$，将共享同一最近词汇嵌入的视觉 Token 归入同一语义组。进化算法中的变异操作被约束为**以组为单位进行翻转**，即同一语义组内的 Token 倾向于被同时保留或丢弃。

这一设计的因果机制在于：语义相似的 Token 往往携带冗余信息，单独保留其中一部分即可维持任务性能，而冗余 Token 的剔除则直接转化为压缩率的提升。Figure 2 展示了语义分组的效果——三个代表性视觉 Token 子集分别与“person”、“car”、“traffic light”等词汇嵌入最近邻匹配，验证了分组的语义一致性。

### 3. 训练损失的针对性设计：GHM-C + 余弦相似度

压缩器训练面临两个独特挑战：(1) **难度不均衡**——大量“容易”的 Token（如背景区域）与少量“困难”的 Token（如关键物体）在损失中占比悬殊；(2) **Token 相似性**——语义相近的 Token 应获得相似的保留概率。EvoComp 通过组合损失函数解决这两个问题：

$$\mathcal{L}(\varphi, \psi) = \mathcal{L}_{\mathrm{GHM-C}}(\varphi, \psi) + \alpha \mathcal{L}_{\mathrm{CS}}(\varphi)$$

其中 $\mathcal{L}_{\mathrm{GHM-C}}$ 是梯度协调机制分类损失（GHM-C），通过梯度密度 $GD(g_i)$ 对每个 Token 的损失进行重加权，抑制极易分类和极难分类样本的梯度贡献，使训练聚焦于中等难度的判别性 Token。$\mathcal{L}_{\mathrm{CS}}$ 是余弦相似度损失，鼓励语义相近的视觉 Token 嵌入在压缩器特征空间中保持邻近，从而产生一致的保留决策。

### 4. 与 Baseline 的本质差异

相较于 FastV、PruMerge 等基于注意力或相似度排序的剪枝方法，EvoComp 的 changed slot 不在压缩器的网络结构（仍为轻量单层 Transformer + 线性分类器），而在于**监督信号的来源**和**冗余建模的方式**：

- **监督信号**：从代理指标（注意力分数、CLIP 相似度）变为 MLLM 任务损失驱动的进化搜索标签；
- **冗余建模**：从隐式的全局排序变为显式的语义分组约束，确保同一语义组内的 Token 被一致处理。

这一设计使得 EvoComp 在 3× 压缩（192 tokens）下，于 LLaVA-1.5-7B 的多基准平均准确率保留率达到 99.3%，仅比无压缩的 Vanilla（576 tokens）低 0.7 个百分点（Table 1）。值得注意的是，压缩器训练完成后，推理时的 Token 选择仅需一次前向传播，引入的计算开销可忽略不计。

EvoComp 的整体 pipeline 围绕一个核心设计展开：在 MLLM 的视觉对齐模块与大语言模型之间，插入一个可训练的轻量级压缩器（compressor），由该压缩器对视觉 token 进行“保留/丢弃”的二值选择，从而在进入 LLM 之前削减视觉 token 的数量。

### 模块关系与数据流

1. **视觉编码与对齐**：输入图像首先经过视觉编码器（如 CLIP-ViT）提取视觉特征，再通过一个对齐模块（如 MLP 投影层）将视觉特征映射到 LLM 的输入空间，得到对齐后的视觉 token 序列。这一部分沿用所搭载 MLLM（例如 LLaVA-1.5）的原有结构，EvoComp 不做修改。

2. **压缩器（Compressor）**：EvoComp 在对齐模块与 LLM 之间插入一个压缩器模块。该压缩器同时接收对齐后的视觉 token 和文本 token 作为输入，输出每个视觉 token 的**保留概率**。压缩器本身是一个单层 Transformer（其结构与对应 MLLM 中 LLM 层的结构一致，但做了两处改动：将因果注意力替换为双向注意力，并加入跳跃连接以促进梯度流动），后接一个线性分类头。训练完成后，压缩器仅需一次前向传播即可完成 token 选择，推理开销可忽略不计。

3. **Token 选择与 LLM 推理**：根据压缩器输出的保留概率，按预设的保留数量（如 192、128 或 64 个 token）选取概率最高的视觉 token，与全部文本 token 拼接后送入 LLM 进行下游任务的生成或推理。整个过程可概括为：

   **图像 → 视觉编码器 → 对齐模块 → 压缩器（保留/丢弃） → LLM**

### 训练监督的来源：进化标注

压缩器的训练需要高质量的 token 保留标签（即“哪些 token 该保留”），但这类标签无法直接获取。EvoComp 的核心创新在于**进化标注（Evolutionary Labeling）**策略：对每个训练样本，利用进化算法搜索一个二值掩码（0-1 向量，指示每个视觉 token 保留或丢弃），使得在该掩码下 MLLM 的任务损失最小，同时通过语义分组策略消除 token 间的冗余。搜索过程中，种群规模 q=48，父代数量 p=12，迭代 L=10 轮。最终选取损失最低的候选掩码作为该样本的监督标签，用于训练压缩器。

### 训练损失设计

压缩器训练的总损失为两项的加权和：

$$
\mathcal{L}(\varphi, \psi) = \mathcal{L}_{\mathrm{GHM-C}}(\varphi, \psi) + \alpha \mathcal{L}_{\mathrm{CS}}(\varphi)
$$

- **GHM-C 损失**：针对 token 保留任务中正负样本严重不均衡以及难易样本分布不均的问题，采用梯度协调机制（Gradient Harmonizing Mechanism）对分类损失进行重加权，抑制极易负样本和极难样本的梯度贡献。
- **余弦相似度损失**：对压缩器输出的视觉 token 嵌入施加约束，鼓励同组 token 的嵌入相互靠近，从而增强压缩器对语义冗余的感知能力。

### 推理流程

训练完成后，压缩器以即插即用的方式工作：给定输入图像和文本，对齐模块产生视觉 token，压缩器一次性输出所有视觉 token 的保留概率，按目标数量选取 top-k 个 token 送入 LLM。整个过程无需额外的进化搜索或迭代优化，保证了推理效率。

> **注意**：关于压缩器训练数据的规模、训练超参数（如学习率、batch size、训练轮次）以及 α 的具体取值，当前提供的分析材料中未给出明确数值，需查阅原文的 4.1 节进行手动核实。

![[assets/figures/papers/paper_list_l750_https_arxiv_org_abs_2604_17087/figures/001_Figure_1.jpg]]
*Figure 1: An overview of the EvoComp framework. Evolutionary Labeling (Right) searches for informative visual tokens that minimize the MLLM task loss, while ensuring non-redundancy by the semantic grouping strategy. Training Phase (Left Bottom) trains a lightweight compressor using the searched labels, optimized with a combination of GHM and cosine similarity loss. Inference Phase (Left Top) applies the trained compressor to filter tokens for efficient and accurate multimodal inference*

### 3.1 语义分组策略（Semantic Grouping）

进化搜索面临的核心瓶颈在于搜索空间随视觉 token 数量指数爆炸，且直接搜索 0-1 掩码容易保留大量语义冗余的 token。EvoComp 的解法是在搜索前引入**语义分组**，将视觉 token 按语义相似性聚合成若干组，进化算法仅在组级别进行选择，从而将搜索空间从 token 级压缩至组级，同时天然抑制冗余。

具体地，给定对齐后的视觉 token 嵌入 $\boldsymbol{v}_i$ 和 MLLM 词表嵌入 $\boldsymbol{e}_j$，计算两者间的余弦相似度：

$$S_{ij} = \frac{\boldsymbol{v}_i \cdot \boldsymbol{e}_j}{\|\boldsymbol{v}_i\|_2 \|\boldsymbol{e}_j\|_2}$$

若两个视觉 token $\boldsymbol{v}_i$ 和 $\boldsymbol{v}_k$ 共享同一个最近邻词表嵌入，即：

$$\arg \max_j S_{ij} = \arg \max_j S_{kj}$$

则将它们归入同一语义组。Figure 2 展示了分组结果示例——语义相近的视觉 token（如与“person”“car”“background”等词表嵌入最接近的 token）被自动聚合到同一组内。这一策略的因果逻辑是：**语义冗余是 token 级冗余的主要来源，在组粒度上做选择等价于强制去重，同时将搜索空间从 $2^N$ 降至 $2^G$（$G \ll N$）**。

![[assets/figures/papers/paper_list_l750_https_arxiv_org_abs_2604_17087/figures/002_Figure_2.jpg]]
*Figure 2: An example of semantic grouping result. Three representative subsets of visual tokens and their corresponding nearest vocabulary tokens are illustrated*

### 3.2 进化标注算法（Evolutionary Labeling）

语义分组完成后，EvoComp 使用进化算法为每个训练样本搜索最优的组级二值掩码，监督信号直接对齐 MLLM 的任务损失。算法流程如下（对应 Algorithm 1）：

1. **初始化种群**：随机生成 $q$ 个二值掩码候选解，每个掩码指示哪些语义组被保留。
2. **迭代进化**（共 $L$ 轮）：
   - 从当前种群中选取损失最低的 $p$ 个候选作为父代；
   - 通过交叉（crossover）和变异（mutation）生成新的子代候选；
   - 对每个候选，按掩码保留对应组的视觉 token，与全部文本 token 一同输入冻结的 MLLM，计算任务损失；
   - 用新生成的子代替换种群中损失较高的个体。
3. **标签选择**：$L$ 轮迭代结束后，取损失最低的候选掩码作为该训练样本的监督标签。

实验设置中，种群大小 $q=48$，父代数量 $p=12$，迭代轮数 $L=10$。该设计的核心因果机制在于：**进化搜索直接以 MLLM 输出损失为适应度函数，使得标签天然对齐下游任务需求，避免了手工启发式规则与任务目标之间的偏差**。

### 3.3 压缩器结构与训练损失

压缩器是一个轻量级模块，插入在对齐模块与 LLM 之间。其结构为**单层 Transformer + 线性分类头**，Transformer 的架构镜像自对应 MLLM 的 LLM 层，但有两处关键修改：① 因果注意力替换为双向注意力，使每个视觉 token 能感知全局上下文；② 引入残差连接，保证梯度流动的稳定性。压缩器接收对齐后的视觉和文本 token，输出每个视觉 token 的保留概率。

训练压缩器时面临两个技术挑战：**难度不均衡**（easy negative 和 extremely hard 样本主导梯度）和**token 相似性**（嵌入相近的 token 难以区分）。EvoComp 设计了组合损失函数来应对：

**GHM-C 损失**（Gradient Harmonizing Mechanism for Classification）通过梯度密度 $GD(g_i)$ 对每个 token 的交叉熵损失进行重加权：

$$GD(g_i) = \frac{1}{l_\epsilon(g_i)} \sum_{k=1}^{n} \delta_\epsilon(g_k, g_i)$$

$$\mathcal{L}_{\mathrm{GHM-C}}(\varphi, \psi) = \frac{1}{n} \sum_{i=1}^{n} \frac{n}{GD(g_i)} \ell(g_\psi(\boldsymbol{h}_i^v), y_i)$$

其中 $g_i$ 为 token $i$ 的梯度范数，$GD(g_i)$ 衡量梯度范数接近 $g_i$ 的 token 密度。该损失自动降低高密度区间（easy negative 和 extremely hard）样本的权重，使训练聚焦于中等难度的判别性 token。

**余弦相似度损失** $\mathcal{L}_{\mathrm{CS}}(\varphi)$ 惩罚被保留 token 之间的嵌入相似度，显式抑制冗余选择。

最终总损失为两者的加权和：

$$\mathcal{L}(\varphi, \psi) = \mathcal{L}_{\mathrm{GHM-C}}(\varphi, \psi) + \alpha \mathcal{L}_{\mathrm{CS}}(\varphi) \tag{6}$$

训练完成后，压缩器仅需一次前向传播即可完成 token 选择，引入的计算开销可忽略不计。

## 实验与关键发现

### 主结果：视觉 Token 压缩下的性能保持

EvoComp 在 LLaVA-1.5-7B 上进行了系统的视觉 token 压缩实验，评估基准涵盖 GQA、MMB、MMB-CN、POPE、TextVQA 和 VizWiz 六个视觉-语言理解任务。在 3× 压缩（保留 192 tokens，原始为 576 tokens）的设置下，EvoComp (l=2) 取得了 **99.3% 的平均准确率保持率**，相比未压缩的 Vanilla 基线（100%）仅下降 0.7%。当压缩率进一步提升至保留 128 tokens 时，平均保持率仍维持在 **98.0%**。这一结果表明，通过进化算法搜索得到的 token 保留标签能够有效识别对 MLLM 任务输出损失最关键的信息性视觉 token，从而在显著减少输入长度的同时几乎不牺牲模型的理解能力。

在更高压缩率的极端场景下，EvoComp 同样展现出稳健的性能退化曲线。在 LLaVA-NeXT-7B 的高分辨率图像处理中，当视觉 token 被压缩至仅 160 个时，EvoComp (l=0) 取得了 92.1% 的平均性能（相对于原始 94.4% 的基线）。此外，EvoComp 的 token 选择策略具有良好的模型间迁移性：在 LLaVA-1.5-7B 上训练的压缩器直接迁移至 LLaVA-1.5-13B 使用时，在保留 64 tokens 的极端压缩下仍能达到 94.4% 的平均性能，而 13B 模型的原始基线为 88.9%——这一反常的“超越基线”现象表明，进化标签策略筛选出的 token 子集可能起到了去噪或聚焦关键信息的作用，值得进一步验证。

### 推理加速与效率分析

EvoComp 的推理加速收益体现在端到端延迟的显著降低。在移动设备上的延迟评估显示，压缩器本身仅引入极小的计算开销（单层 Transformer + 线性分类器），而由于输入 LLM 的 token 数量大幅减少，自回归解码阶段的延迟得到有效削减。在 3× 压缩设置下，端到端推理实现了 **1.6× 加速**；在更高压缩率下，加速比可进一步提升至 **2.0×**。这一加速效果在 POPE 基准上的速度-性能曲线中得到了直观呈现——EvoComp 在保持高准确率的同时，推理延迟显著低于未压缩的 Vanilla 模型及部分现有压缩方法。

### 消融实验：进化迭代次数与损失函数设计

消融实验揭示了两个关键设计因素的影响：

1. **进化迭代次数 (l)**：将进化算法的迭代次数从 l=0（无进化，仅初始随机搜索）增加到 l=2，平均性能保持率从约 92% 提升至 99.3%，表明进化搜索过程对于找到任务对齐的 token 保留标签至关重要。迭代次数的增加使种群能够逐步逼近使 MLLM 输出损失最小化的最优二值掩码。

2. **损失函数组件**：总损失函数由 GHM-C 损失和余弦相似度损失加权组合而成（式 6）。消融结果表明，移除余弦相似度损失会导致性能下降，因为该损失通过惩罚保留 token 之间的相似性来促进非冗余选择；而 GHM-C 损失则通过梯度密度加权缓解了训练中简单负样本和极难样本的不平衡问题。两个组件的协同作用是压缩器有效训练的关键。

### 失败模式与局限性

尽管 EvoComp 在多数基准上表现出色，仍存在以下值得关注的局限：

- **进化标注的计算成本**：为每个训练样本运行完整的进化搜索（种群大小 48，父代 12，迭代 10 轮）以生成监督标签，这一过程需要多次前向传播 MLLM 以计算任务损失，训练阶段的标注成本较高。论文未给出标注阶段的具体时间开销，该点需人工核实。
- **压缩器结构的耦合性**：压缩器中的 Transformer 层结构镜像了对应 MLLM 的 LLM 层设计（仅将因果注意力替换为双向注意力并加入跳跃连接），这意味着更换底层 MLLM 时可能需要重新设计或微调压缩器结构，通用性受限。
- **极端压缩下的性能退化**：当 token 保留数量降至极低水平（如 64 tokens）时，部分基准上的性能出现较明显下降，表明语义分组策略在极度压缩下可能无法充分覆盖图像中的所有关键语义区域。

![[assets/figures/papers/paper_list_l750_https_arxiv_org_abs_2604_17087/figures/004_Table_1.jpg]]
*Table 1: Performance of EvoComp and other methods on visionlanguage understanding with LLaVA-1.5-7B under different number of retained tokens*

![[assets/figures/papers/paper_list_l750_https_arxiv_org_abs_2604_17087/figures/003_Table_2.jpg]]
*Table 2: Evaluation of extreme visual token compression for highresolution images with LLaVA-NeXT-7B*

![[assets/figures/papers/paper_list_l750_https_arxiv_org_abs_2604_17087/figures/005_Table_3.jpg]]
*Table 3: Evaluation of token selection transferability from LLaVA-1.5-7B to LLaVA-1.5-13B. The results of EvoComp are based on the transferred setting, whereas those of the other methods are derived from LLaVA-1.5-13B itself*

![[assets/figures/papers/paper_list_l750_https_arxiv_org_abs_2604_17087/figures/009_Table_5.jpg]]
*Table 5: Ablation study on vision-language understanding using LLaVA-1.5-7B*

## 定位与知识库关联

EvoComp 处于视觉 Token 压缩与多模态大模型效率优化的交叉地带。其核心定位是**训练一个轻量级压缩器，以进化搜索生成的二值掩码作为监督信号，在保留任务精度的前提下大幅削减视觉 Token 数量**。与现有工作的关系、适用边界及开放问题如下。

### 与 Baseline/Follow-up 的关系

**FastV** 和 **SparseVLM** 等早期工作采用无训练的启发式剪枝（如仅保留 CLS Token 或基于注意力分数排序），虽无需额外训练，但在高压缩比下精度衰减显著。EvoComp 的进化标签策略直接以 MLLM 的任务损失为优化目标，在 3× 压缩（192 tokens）下平均精度保留率达 99.3%，显著优于同压缩比下的无训练方法（Table 1 中 FastV 等 baseline 在同等压缩比下精度保留率明显更低）。

**LLaVA-PruMerge** 和 **TokenPacker** 引入了可学习的压缩模块，但前者依赖启发式重要性分数，后者将压缩视为重建任务，均未直接对齐 MLLM 的端任务损失。EvoComp 的关键区别在于：监督信号来自进化算法在 MLLM 输出损失空间中的搜索，使压缩器的训练目标与下游任务完全一致。

**MPGD**（He et al., CVPR 2023）等工作在单模态视觉任务中探索了梯度密度感知的损失重加权，EvoComp 将其扩展至多模态场景，并结合余弦相似度损失抑制冗余 Token 的选择，形成了 GHM-C + Cosine Similarity 的组合损失。

在跨架构迁移方面，EvoComp 展示了较强的泛化能力：在 LLaVA-1.5-7B 上训练的压缩器可直接迁移至 LLaVA-1.5-13B（Table 3，64 tokens 下 Avg. 94.4%）和 Qwen2.5-VL-7B（Figure 3），无需重新训练，这在实际部署中具有显著工程价值。

### 适用边界

1. **架构依赖**：压缩器结构镜像了对应 MLLM 的 LLM 层设计（单向注意力改为双向注意力，并加入跳跃连接），这意味着更换 MLLM 架构时需重新设计压缩器结构，但论文展示了跨规模迁移的可行性。
2. **压缩比范围**：论文验证了 3× 至 9× 压缩（192→64 tokens），在 9× 极端压缩下精度保留率约 94.9%。超出此范围的压缩效果未经验证。
3. **任务类型**：主要评估集中在视觉问答和视觉语言理解基准（GQA、MMB、POPE、TextVQA、VizWiz 等），在生成式任务（如图像描述、多轮对话）上的表现未充分覆盖。
4. **高分辨率场景**：在 LLaVA-NeXT-7B 的高分辨率多裁剪场景下（Table 2），EvoComp（l=0）在 160 tokens 时 Avg. 92.1%（相对 Vanilla 的 94.4% 下降约 2.3%），表明高分辨率多图场景下的压缩损失比标准分辨率场景更大，需进一步验证。

### 局限与开放问题

1. **进化搜索的计算开销**：进化标签生成需要在每个训练样本上运行多轮 MLLM 前向传播（种群大小 q=48，父代 p=12，迭代 L=10），训练阶段的算力需求显著高于无训练方法。论文未报告标签生成的具体时间成本。
2. **语义分组的粒度敏感性**：语义分组策略依赖视觉 Token 与词汇嵌入的余弦相似度，分组粒度的选择（通过最近邻词汇 Token 判定）对最终压缩效果的影响未做消融分析。
3. **压缩器的可解释性**：压缩器输出的保留概率虽可可视化，但其决策逻辑（为何某些 Token 被保留而相邻 Token 被丢弃）缺乏语义层面的解释，这在安全敏感应用中可能构成风险。
4. **移动端部署的全面性**：论文报告了在智能手机上 1.6× 的推理加速（Table 4），但仅测试了 LLaVA-1.5-7B 单一模型，且未对比其他压缩方法在相同硬件上的延迟表现。
5. **开放问题**：
   - 进化标签是否可以跨数据集预计算并复用，从而摊薄训练成本？
   - 压缩器能否与 MLLM 联合微调，进一步提升压缩比上限？
   - 在视频理解等多帧场景中，时序维度的 Token 压缩是否可复用该框架？

## 原文 PDF

![[paperPDFs/CVPR_2026/EvoComp_Learning_Visual_Token_Compression_for_Multimodal_Large_Language_Models_via_Semantic_Guided_Evolutionary_Labeling.pdf]]
