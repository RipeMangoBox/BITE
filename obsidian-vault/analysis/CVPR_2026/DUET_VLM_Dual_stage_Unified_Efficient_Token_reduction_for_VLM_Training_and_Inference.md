---
title: "DUET-VLM: Dual stage Unified Efficient Token reduction for VLM Training and Inference"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DUET_VLM_Dual_stage_Unified_Efficient_Token_reduction_for_VLM_Training_and_Inference.pdf
project_link: null
code_link: "https://github.com/AMD-AGI/DUET-VLM"
aliases:
- DV
- DUET-VLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过联合优化视觉冗余感知的token合并（基于V2V注意力的局部聚类）和文本引导的逐层token丢弃（T2V显著性裁剪），可以在保持关键语义的同时大幅减少视觉token数量，且两个阶段协同适配不同压缩率。
primary_logic: 耦合早期结构合并与后期语义裁剪：在视觉编码器侧用局部聚类代替全局平均，保留细粒度视觉信息并丢弃大量冗余；在语言模型侧利用显著性文本token的跨注意力指导逐层丢弃，使深层仅关注语义相关区域，从而在极低token预算下保持高精度。
claims:
- DUET-VLM在LLaVA-1.5-7B推理时，67% token压缩下保持99.0%平均准确率，显著优于VisionZip (97.7%)和PyramidDrop (96.4%)。
- 在Video-LLaVA-7B上，DUET-VLM在53.1% token压缩下超越基线（100.8%），在93.4%极端压缩下仍保持97.6%准确率。
- 训练时间减少31%的同时，准确率仅下降<1% (99.1%平均准确率保留)。
- 局部聚类聚合是一种即插即用的压缩策略，能够一致提升VisionZip和DUET-VLM的性能，特别是在低token预算下增益更明显。
---

# DUET-VLM: Dual stage Unified Efficient Token reduction for VLM Training and Inference

> [!tip] 核心洞察
> 耦合早期结构合并与后期语义裁剪：在视觉编码器侧用局部聚类代替全局平均，保留细粒度视觉信息并丢弃大量冗余；在语言模型侧利用显著性文本token的跨注意力指导逐层丢弃，使深层仅关注语义相关区域，从而在极低token预算下保持高精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | DUET-VLM：面向VLM训练与推理的双阶段统一高效Token压缩 |
| 英文题名 | DUET-VLM: Dual stage Unified Efficient Token reduction for VLM Training and Inference |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.18846) · [Code](https://github.com/AMD-AGI/DUET-VLM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DUET-VLM |
| Dataset | LLaVA-1.5-7B, Qwen-2.5-VL-7B, LLaVA-1.5-7B trained, Video-LLaVA-7B |

> [!tip] 效果简介
> - LLaVA-1.5-7B (five benchmarks: POPE, SQAI, VQAT, MME, GQA) 上，相对平均准确率 (Avg%) 99.0% (192 tokens, ↓67%); 98.1% (128 tokens, ↓78%); 95.4% (64 tokens, ↓89%) vs 100.0% (576 tokens) (-1.0% at 67% reduction, -1.9% at 78%, -4.6% at 89%)。
> - Qwen-2.5-VL-7B (five benchmarks: POPE, SQAI, VQAT, MME, GQA) 上，相对平均准确率 (Avg%) 99.9% (640 tokens); 99.8% (320 tokens); 98.4% (160 tokens) vs 100.0% (dynamic tokens) (-0.1% at 640, -0.2% at 320, -1.6% at 160 tokens)。
> - LLaVA-1.5-7B trained (five benchmarks: POPE, SQAI, VQAT, MME, GQA) 上，相对平均准确率 (Avg%) 99.7% (192 tokens); 99.1% (128 tokens); 97.2% (64 tokens) [DUET-VLM (C)] vs 100.0% (576 tokens LLaVA-1.5-7B) (-0.3% at 192, -0.9% at 128, -2.8% at 64 tokens)。

## 概要

视觉语言模型（VLM）在理解多模态内容方面取得了长足进步，但其高昂的计算开销——根源在于密集的视觉分词——严重制约了实际部署。以 **LLaVA-1.5-7B**（Liu et al., CVPR 2024）为例，单张图像产生576个视觉token，而 **LLaVA-NeXT** 更是超过2800个token，导致计算和内存成本随分辨率平方级增长。现有压缩方法或过早合并造成细粒度信息损失（如 **VisionZip**, Yang et al., CVPR 2025），或采用统一丢弃策略缺乏语义适应性（如 **PyramidDrop**, Xing et al., CVPR 2025），未能联合优化冗余消除与上下文感知保留这一核心矛盾。

**DUET-VLM** 针对上述瓶颈，提出一种即插即用的双阶段统一token压缩框架。其核心洞察在于：**耦合早期结构合并与后期语义裁剪**——在视觉编码器侧，利用V2V自注意力驱动的局部聚类替代全局平均，保留细粒度视觉信息的同时大幅消除冗余；在语言模型侧，利用显著性文本token的跨注意力指导逐层丢弃，使深层仅关注语义相关区域。两个阶段协同优化，在不同压缩率下均能保持关键语义。

主要结果验证了这一设计的有效性：

- **推理场景**：在LLaVA-1.5-7B上，DUET-VLM以67%的token压缩率保持99.0%平均准确率，显著优于VisionZip（97.7%）和PyramidDrop（96.4%）；在89%的极端压缩下仍保持95.4%准确率（Table 1）。在Qwen-2.5-VL-7B上，仅需640 token即达到99.9%的相对准确率（Table 2）。
- **训练场景**：训练时间减少31%的同时，准确率仅下降不到1%（99.1%平均准确率保留），实现了精度与效率的优异平衡（Table 6, Figure 1b）。
- **视频扩展**：在Video-LLaVA-7B上，53.1% token压缩下准确率超越基线（100.8%），93.4%极端压缩下仍保持97.6%（Table 4）。

消融实验进一步揭示：局部聚类聚合是一种即插即用的压缩策略，能够一致提升VisionZip和DUET-VLM的性能，在低token预算下增益尤为明显（Table 7, Table 10）；文本引导的token选择（显著性token或全部查询token）优于仅依赖最后一个文本token的方案（Table 8, Table 11）。

### 视觉语言模型的Token膨胀困境

当前主流的大规模视觉语言模型（VLM）普遍采用密集的视觉分词策略，将输入图像编码为大量视觉token后送入语言模型进行跨模态推理。例如，**LLaVA-1.5-7B**（Liu et al., CVPR 2024）使用576个视觉token，而**LLaVA-NeXT**的token数量更超过2800个。这种密集表示带来了一个根本性瓶颈：视觉token的计算和内存开销随图像分辨率呈平方级增长，严重制约了VLM在实际部署中的效率。

### 现有压缩方法的结构性缺陷

为缓解上述瓶颈，研究者提出了多种视觉token压缩方法，但它们在设计上存在两类典型的结构性缺陷：

**过早合并导致信息损失。** 以**VisionZip**（Yang et al., CVPR 2025）为代表的视觉侧压缩方法，在视觉编码器输出端通过注意力分数选择主导token并对残差token进行全局平均合并。这种“一刀切”的全局聚合策略忽略了视觉token之间的局部语义关联，导致细粒度空间信息在压缩过程中被不可逆地抹除，尤其在低token预算下性能退化显著。

**统一丢弃缺乏语义适应性。** 以**PyramidDrop**（Xing et al., CVPR 2025）为代表的语言侧压缩方法，利用最后一个文本token的交叉注意力分数在LLM的多个层逐层丢弃视觉token。该方法仅依赖单一的文本token作为显著性信号，缺乏对文本语义多样性的感知，无法根据具体查询内容自适应地保留关键视觉区域。

**更根本的问题在于，现有方法未能联合优化冗余消除与上下文感知保留。** 视觉侧的冗余合并与语言侧的语义裁剪本质上是互补的——前者消除视觉编码器输出中的空间冗余，后者根据文本语义筛选对推理真正关键的视觉信息。然而，此前的所有工作均将二者视为独立策略，导致压缩效率与语义保真度之间存在难以调和的矛盾。

### 本文动机：双阶段联合压缩

基于上述分析，本文提出核心洞察：**耦合早期结构合并与后期语义裁剪**，可以在极低token预算下保持高精度。具体而言：

- **在视觉编码器侧**，用局部聚类代替全局平均，将残差token按V2V自注意力相似性分组到小簇内局部聚合，既丢弃了大量冗余，又保留了细粒度视觉信息；
- **在语言模型侧**，利用显著性文本token（而非仅最后一个token）的跨注意力指导逐层丢弃，使深层仅关注与语义查询相关的视觉区域。

这种双阶段设计——**DUET-VLM**——将视觉冗余感知的token合并（V2V局部聚类）与文本引导的逐层token丢弃（T2V显著性裁剪）协同组合，两个阶段互补适配不同压缩率，从而在推理和训练两个场景下均实现优异的精度-效率权衡。

## 核心方法与创新机理

DUET-VLM 的核心创新在于首次将**视觉冗余感知的token合并**与**文本引导的逐层token丢弃**耦合为一个统一的双阶段压缩框架，从根本上改变了现有VLM中视觉token压缩的范式。与先前方法仅在编码器侧或语言模型侧进行单点压缩不同，DUET-VLM通过两个互补阶段的协同优化，在极低token预算下实现了高精度保持。

### 从单侧压缩到双阶段联合优化

现有视觉token压缩方法可归为两类：**视觉侧合并**与**语言侧丢弃**，二者各自存在结构性缺陷：

- **视觉侧合并方法**（如**VisionZip**，Yang et al., CVPR 2025）在视觉编码器输出端基于V2V自注意力分数选择主导token，并对残差token进行全局平均以构造上下文token。这一策略虽能有效减少token数量，但**全局平均会稀释细粒度视觉信息**，且压缩决策完全独立于下游语言模型的语义需求。
- **语言侧丢弃方法**（如**PyramidDrop**，Xing et al., CVPR 2025）在LLM内部利用最后一个文本token的交叉注意力分数，逐层丢弃低分视觉token。该方法虽然引入了文本引导，但**仅依赖单一文本token的注意力信号**，对复杂查询的语义覆盖不足，且未在输入端消除视觉冗余。

DUET-VLM的关键洞察在于：**早期结构合并与后期语义裁剪具有天然的互补性**——视觉编码器输出的密集token中存在大量空间冗余，可通过局部聚类高效压缩；而语言模型内部的跨模态注意力则提供了文本相关的显著性信号，可指导深层token的精准保留。将二者耦合，使压缩过程同时具备“冗余感知”与“语义感知”双重能力。

### 第一阶段：局部聚类聚合替代全局平均

在视觉编码器侧，DUET-VLM对VisionZip的token合并策略进行了根本性改进。VisionZip采用**全局平均**构造上下文token：将所有未被选为主导的残差token进行整体平均，得到一个全局上下文向量。这一操作虽然简单，但会导致不同空间位置的视觉信息被无差别混合，损失了细粒度的空间结构。

DUET-VLM提出**局部聚类聚合**：基于V2V自注意力图，从残差token中选取 $k_2$ 个聚类质心，对每个质心仅聚合其 $w$ 个最近邻（基于注意力分数的TopK选择），形成 $k_2$ 个局部上下文token。未被任何簇覆盖的残差token则直接丢弃。这一设计的因果机制在于：

1. **保留空间局部性**：限制簇宽度 $w$ 强制每个上下文token仅编码局部邻域信息，避免远距离token的错误混合；
2. **注意力驱动的聚类**：质心选择和邻居分配均基于V2V自注意力分数，使聚类结果与视觉编码器自身的冗余感知一致；
3. **即插即用**：该局部聚类策略可直接替换VisionZip的全局平均模块，无需修改模型架构或训练流程。

消融实验（Table 7, Table 10）验证了局部聚类的有效性：在LLaVA-1.5-7B和LLaVA-NeXT-7B上，采用局部聚类的VisionZip变体（VZ (C)）在所有token预算下均持续优于原始VisionZip，尤其在低token预算下增益更为显著。

### 第二阶段：显著性文本token引导的逐层丢弃

在语言模型侧，DUET-VLM对PyramidDrop的丢弃策略进行了关键改进。PyramidDrop仅使用**最后一个文本token**的交叉注意力分数来评估视觉token的重要性，这一选择基于“最后一个token聚合了全部上下文信息”的假设。然而，该假设在实际复杂查询中并不总是成立——不同文本token可能关注图像的不同区域。

DUET-VLM探索了两种更优的文本token选择方案：

- **显著性文本token**：选取交叉注意力分数最高的若干文本token，综合其注意力信号进行视觉token排名；
- **全部查询token**：使用所有文本token的注意力分数进行综合评估。

在LLM的多个阶段（如第8、16、24层），DUET-VLM根据选定的文本token与视觉token的T2V交叉注意力分数对视觉token排序，按预设比例 $\lambda$ 逐层丢弃低分token。这一设计的因果机制在于：

1. **语义聚焦**：显著性文本token能更精准地捕捉与查询相关的视觉区域，使深层仅保留语义关键token；
2. **层级递进**：逐层丢弃使压缩过程与LLM的层级抽象能力对齐——浅层保留更多视觉细节，深层聚焦语义核心；
3. **灵活性**：文本token选择策略可根据任务特点调整，在通用性与针对性之间取得平衡。

消融实验（Table 8, Table 9）表明，在LLaVA-1.5-7B上，使用显著性文本token或全部查询token均优于仅用最后一个token；在LLaVA-NeXT-7B上，显著性token方案在低预算下表现更佳。此外，将这一文本token选择策略应用于PyramidDrop内部（Table 11），同样带来了性能提升，进一步验证了文本引导的价值。

### 双阶段协同的压缩机制

DUET-VLM的两个阶段并非简单叠加，而是通过**压缩率分配**实现协同优化。第一阶段通过局部聚类将视觉token从 $N$ 压缩至 $k_1 + k_2$，消除空间冗余；第二阶段在LLM内部进一步将token从 $k_1 + k_2$ 逐层压缩至目标预算。两个阶段的压缩比例可通过调整 $k_1$、$k_2$、$w$ 和逐层丢弃比例 $\lambda$ 灵活配置。

灵敏度分析（Figure 7, Figure 8）揭示了两个阶段之间的权衡关系：在192 token预算下，增加主导token数量 $k_1$ 持续提升性能；而在128 token预算下，采用中等的主导-上下文比例（$k_1 \approx 160$）达到最佳平衡。这表明双阶段压缩需要根据总预算动态调整各阶段的压缩强度，而非固定分配。

### 训练与推理的统一适用

DUET-VLM的另一个关键创新在于**训练与推理阶段的统一**。现有压缩方法大多仅针对推理阶段设计，在训练中应用会导致信息损失累积。DUET-VLM通过在训练流程中同时启用双阶段压缩，使模型在训练过程中即适应压缩后的token分布，从而在保持高压缩率的同时实现更优的精度保留。

实验结果表明（Table 3, Table 6），在LLaVA-1.5-7B训练中启用DUET-VLM，可在67% token压缩下保持99.7%平均准确率，同时训练时间减少31%。这一“训练即压缩”的范式为高效VLM训练提供了新的技术路径。

DUET-VLM 提出了一种**双阶段统一视觉分词压缩框架**，将视觉语言模型的 token 压缩分解为两个互补且可协同优化的阶段：在视觉编码器侧进行**冗余感知的 token 合并**，随后在语言模型侧进行**文本引导的逐层 token 丢弃**。该框架以即插即用的方式工作，无需修改底层 VLM 架构。

### 流程总览

整个 pipeline 由五个核心模块串联构成（见图 2）：

1. **Vision Encoder（CLIP/SigLIP）**：输入图像被编码为 $N$ 个视觉 token，同时输出嵌入表示和最后一层的 V2V 自注意力图 $A_{v2v}$。
2. **V2V Merging（局部聚类聚合）**：基于 $A_{v2v}$ 的注意力分数，选出 $k_1$ 个**主导 token**（dominant tokens），并对剩余残差 token 进行局部聚类，生成 $k_2$ 个**上下文 token**（contextual tokens）。最终输出 $k_1 + k_2$ 个压缩后的视觉 token。
3. **MLP Adapter**：将压缩后的视觉 token 投影到与语言模型匹配的嵌入维度，完成模态对齐。
4. **Language Backbone（LLM）**：将压缩视觉 token 与文本 token 拼接输入大语言模型，在多个 transformer 层中执行跨模态推理。
5. **T2V Pruning（文本引导逐层丢弃）**：在 LLM 的选定 stage（如第 8、16、24 层），根据显著性文本 token 与视觉 token 的 T2V 交叉注意力分数进行排序，按预设比例 $\lambda$ 逐层丢弃低分视觉 token。

### 双阶段协同机制

两个阶段在功能上形成**耦合互补**：

- **阶段一（V2V Merging）** 在跨模态融合之前消除视觉冗余。其核心创新在于用**局部聚类聚合**替代 VisionZip 等方法的全局平均，将残差 token 限制在宽度为 $w$ 的小簇内进行局部平均，未分配到任何簇的 token 直接丢弃。这保留了细粒度视觉线索，避免了全局平均造成的信息稀释。
- **阶段二（T2V Pruning）** 在语言模型内部利用文本语义进行上下文感知的 token 筛选。与 PyramidDrop 仅使用最后一个文本 token 不同，DUET-VLM 支持使用**显著性文本 token（C+S）**或**全部查询 token（C+all）**来计算 T2V 交叉注意力，使丢弃决策更具语义针对性。深层 token 的逐步移除使得模型在推理后期仅关注与文本语义高度相关的视觉区域。

### 关键公式

V2V Merging 阶段的核心操作定义如下：

- **主导选择**：所有 token 到 token $i$ 的注意力权重之和衡量其重要性：
  $$s_i = \sum_{j=1}^{N} A_{v2v}^{j,i}$$
- **聚类质心选择**：从残差 token 集合 $\mathcal{R}$ 中按 $s_i$ 选出 $k_2$ 个质心：
  $$\mathcal{C} := \mathrm{TopK}(\{s_i\}_{i \in \mathcal{R}}, k_2)$$
- **邻居分配**：对每个质心 $c$，基于 $A_{v2v}$ 从残差 token 中选择 $w$ 个最近邻：
  $$\mathcal{N}_c = \mathrm{TopK}(A_{v2v}^{c,\mathcal{R}}, w)$$
- **上下文 token 构造**：簇内邻居取平均：
  $$\mathbf{z}_c = \sum_{j \in \mathcal{N}_c} \mathbf{x}_j / |\mathcal{N}_c|$$
- **最终输出**：主导 token 与上下文 token 的并集：
  $$\mathbf{X}_{\mathrm{out}} = \mathbf{X}_{\mathrm{dom}} \cup \mathbf{X}_{\mathrm{comp}}$$

### 配置灵活性

DUET-VLM 通过调节三个关键超参数适配不同的压缩率需求：主导 token 数 $k_1$、上下文 token 数 $k_2$ 和簇宽度 $w$。例如，在 LLaVA-1.5-7B 上，目标 192 tokens 时使用 $k_1=144, k_2=48$；128 tokens 时使用 $k_1=96, k_2=32$；64 tokens 时使用 $k_1=48, k_2=16$（见表 12）。LLM 侧的丢弃比例 $\lambda$ 和丢弃层位置也根据模型和预算进行定制（如 Qwen-2.5-VL-7B 在第 14 和 21 层分别丢弃 50% 和 25% 的视觉 token，见表 15）。

> **注意**：关于 T2V Pruning 中显著性文本 token 的具体选取算法（如如何从所有文本 token 中筛选出“显著性”子集），原文未给出公式化定义，仅在实验部分以“C+S”变体形式出现。该细节需要查阅代码仓库（https://github.com/AMD-AGI/DUET-VLM）进行确认。

![[assets/figures/papers/paper_list_l2218_https_arxiv_org_abs_2602_18846/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed pipeline. An input image is first encoded into N visual tokens by the Vision Encoder. (A) Based on the V2V self-attention map*

DUET-VLM 的核心由一个双阶段压缩管线构成：**视觉侧冗余感知的局部聚类合并**（Stage 1）与**语言侧文本引导的逐层token丢弃**（Stage 2）。两者协同工作，在消除冗余的同时保留语义关键的视觉信息。

### Stage 1：V2V局部聚类合并

视觉编码器（CLIP/SigLIP）将输入图像编码为 $N$ 个视觉token后，Stage 1 基于视觉编码器最后一层的V2V自注意力图进行压缩。其流程如 Algorithm 1 所示，分为三个关键步骤：

**步骤一：主导token选择。** 对每个视觉token $i$，计算其被所有token关注的注意力分数之和：

$$s_i = \sum_{j=1}^{N} A_{v2v}^{j,i}$$

其中 $A_{v2v}^{j,i}$ 表示token $j$ 对token $i$ 的注意力权重。按 $s_i$ 降序排列，选取前 $k_1$ 个作为主导token集合 $\mathbf{X}_{\text{dom}}$，其余token构成残差集合 $\mathcal{R}$。

**步骤二：局部聚类质心选择与邻居分配。** 从残差集合 $\mathcal{R}$ 中选取 $k_2$ 个聚类质心：

$$\mathcal{C} := \mathrm{TopK}(\{s_i\}_{i \in \mathcal{R}}, k_2)$$

对每个质心 $c \in \mathcal{C}$，基于V2V注意力矩阵从残差token中选择 $w$ 个最近邻：

$$\mathcal{N}_c = \mathrm{TopK}(A_{v2v}^{c,\mathcal{R}}, w)$$

**步骤三：上下文token构造。** 对每个质心 $c$，将其邻域内的token取平均，形成该簇的上下文token：

$$\mathbf{z}_c = \sum_{j \in \mathcal{N}_c} \mathbf{x}_j / |\mathcal{N}_c|$$

最终输出token集由主导token与上下文token的并集构成：

$$\mathbf{X}_{\mathrm{out}} = \mathbf{X}_{\mathrm{dom}} \cup \mathbf{X}_{\mathrm{comp}}$$

其中 $\mathbf{X}_{\mathrm{comp}} = \{\mathbf{z}_c\}_{c \in \mathcal{C}}$，总输出token数为 $k_1 + k_2$。未分配给任何质心的残差token被直接丢弃。

**关键设计动机：** 与VisionZip的全局平均不同，局部聚类聚合通过限制簇宽度 $w$，将残差token分组到多个小簇内进行局部平均。这避免了全局平均造成的细粒度视觉信息稀释，同时利用V2V注意力图作为相似性度量，确保语义相关的token被合并到同一上下文token中。消融实验（Table 7, Table 10）证实，局部聚类作为即插即用策略，能一致提升VisionZip和DUET-VLM的性能，尤其在低token预算下增益更为显著。

### Stage 2：T2V文本引导逐层丢弃

压缩后的视觉token经MLP Adapter投影后，与文本token拼接输入语言模型（LLM）。Stage 2 在LLM的多个预设层（如第8、16、24层）执行文本引导的视觉token丢弃。

**核心机制：** 在每个丢弃阶段，利用显著性文本token与视觉token之间的T2V交叉注意力分数作为重要性度量。具体而言，对每个视觉token，计算所有选定的显著性文本token（或全部查询token）对其的交叉注意力之和，按该分数降序排列，保留前 $\lambda$ 比例的视觉token，丢弃其余低分token。该“排序-丢弃”过程在多个阶段重复执行，使深层仅需关注与文本语义高度相关的视觉区域。

**文本token选择策略：** DUET-VLM探索了三种文本token选择方案：
- **C**：仅使用最后一个文本token（与PyramidDrop一致）
- **C+S**：使用显著性文本token（如问句中的关键实体词）
- **C+all**：使用全部查询文本token

消融实验（Table 8, Table 9）表明，C+S和C+all在多数设置下优于仅用最后一个token的方案，验证了更丰富的文本引导信号对视觉token裁剪的积极作用。Figure 4 和 Figure 6 的注意力热力图进一步可视化展示，显著性文本token在第9层和第24层分别聚焦于图像中的语义相关区域，证实了文本引导丢弃的合理性。

**深层丢弃的灵敏度分析：** Figure 5 显示，在语言模型的最后阶段（第24层之后）完全丢弃视觉token对性能影响极小，表明此时相关视觉信息已被充分提取到隐藏状态中。这一发现为激进压缩提供了理论支撑。

## 实验与关键发现

### 核心实验设计

DUET-VLM的实验体系围绕三个核心维度展开：**推理侧压缩**（inference-only，不训练直接压缩）、**训练侧压缩**（trained，在训练中融入压缩策略）以及**跨架构泛化**（Qwen-2.5-VL、Video-LLaVA）。所有实验均在8块AMD Instinct MI325 GPU的单节点上运行。评估基准覆盖POPE、SQAI、VQAT、MME和GQA五个标准视觉语言任务，以**相对平均准确率**（Avg%，以无压缩基线为100%）作为主要指标。

方法变体命名约定如下（见Sec. 4.1）：
- **DUET-VLM (C)**：采用局部聚类聚合（Local Clustering），语言侧使用最后一个文本token指导剪枝。
- **DUET-VLM (C+all)**：局部聚类 + 全部查询文本token指导剪枝。
- **DUET-VLM (C+S)**：局部聚类 + 显著性文本token指导剪枝。

公平性说明：PyramidDrop作者未公开匹配平均token预算所需配置且未报告POPE结果，其Avg%基于剩余基准计算；VisionZip结果来自其论文或相应配置的复现。

### 主结果：推理侧压缩

**LLaVA-1.5-7B上的推理压缩**（Table 1）是全文最核心的基准对比。在576 tokens的无压缩基线（**LLaVA-1.5-7B**，Liu et al., CVPR 2024）上，DUET-VLM (C) 在三个压缩档位均取得最优：

| Token预算 | 压缩率 | DUET-VLM (C) Avg% | VisionZip Avg% | PyramidDrop Avg% |
|-----------|--------|-------------------|----------------|------------------|
| 192       | ↓67%   | **99.0%**         | 97.7%          | 96.4%            |
| 128       | ↓78%   | **98.1%**         | —              | —                |
| 64        | ↓89%   | **95.4%**         | —              | —                |

关键发现：在仅保留三分之一视觉token（192 tokens）时，DUET-VLM几乎无损（99.0%）；即使在极端89%压缩下（64 tokens），仍保持95.4%的基线准确率。相比**VisionZip**（Yang et al., CVPR 2025）和**PyramidDrop**（Xing et al., CVPR 2025）这两个代表性单侧压缩方法，DUET-VLM的双阶段联合策略在各预算下均显著领先，验证了视觉冗余合并与文本引导丢弃的协同效应。

**Qwen-2.5-VL-7B上的跨架构泛化**（Table 2）进一步证实了方法的鲁棒性。DUET-VLM (C)在640、320、160 tokens三档分别达到99.9%、99.8%和98.4%的相对准确率，证明局部聚类与文本引导剪枝的组合不依赖于特定LLaVA架构，可有效迁移至Qwen系列模型。

**Video-LLaVA-7B上的视频理解**（Table 4）展示了方法在时序维度上的适应性。在2048 tokens基线（100%）上，DUET-VLM (C)在960 tokens（↓53.1%）时达到**100.8%**的平均准确率，超越无压缩基线；在136 tokens（↓93.4%）的极端压缩下仍保持97.6%。这表明V2V合并阶段有效去除了视频帧间的冗余，而T2V剪枝阶段保留了时序关键帧的语义信息。

### 主结果：训练侧压缩

**Table 3**报告了在训练流程中集成DUET-VLM的结果。DUET-VLM (C)在192、128、64 tokens下分别达到99.7%、99.1%和97.2%的相对准确率，与推理侧压缩相比，训练侧在极低预算下（64 tokens）有约1.8个百分点的额外提升（97.2% vs 95.4%），说明训练过程中模型可以自适应调整对压缩token的利用策略。

**训练效率**（Table 6和Figure 1(b)）是DUET-VLM的另一关键优势：

| Token预算 | 训练时间减少 | 相对准确率 |
|-----------|-------------|-----------|
| 192       | 26%         | 99.7%     |
| 128       | 31%         | 99.1%     |
| 64        | 36%         | 95.4%     |

在128 tokens配置下，31%的训练时间减少仅带来0.9%的准确率损失，实现了效率与精度的优异平衡。

### 推理速度

**Table 5**报告了推理延迟对比。DUET-VLM (C)在降低token预算的同时实现了显著的推理加速，在精度-延迟权衡曲线上优于VisionZip和PyramidDrop。具体延迟数值需查阅原文表格，但总体趋势表明：双阶段压缩的额外计算开销（局部聚类和交叉注意力排名）远小于减少token带来的自注意力计算节省。

### 消融研究

#### 局部聚类聚合的有效性

**Table 7**（LLaVA-1.5-7B）和**Table 10**（LLaVA-NeXT-7B）系统验证了局部聚类聚合作为即插即用模块的价值。将局部聚类应用于VisionZip（VZ (C)）后，其在各token预算下均超越原始VisionZip，尤其在低预算下增益更明显。类似地，DUET-VLM的vanilla变体（DV (V)，使用全局平均）在替换为局部聚类后（C）性能持续提升。这证实了核心洞察：**限制簇宽度w的局部平均能保留细粒度视觉线索，避免全局平均造成的信息稀释**。

#### 文本token选择策略

**Table 8**（LLaVA-1.5-7B）和**Table 9**（LLaVA-NeXT-7B）对比了三种T2V剪枝的文本token选择方案：
- **C**：仅用最后一个文本token（与PyramidDrop一致）
- **C+all**：使用全部查询文本token
- **C+S**：使用显著性文本token

在LLaVA-1.5-7B上，C+all和C+S均优于C，说明更丰富的文本信号能更准确地识别语义相关视觉区域。在LLaVA-NeXT-7B上，C+S在低预算下表现最佳，验证了“选择性聚焦”策略在更高分辨率场景下的优势。

**Table 11**进一步将这一发现推广到PyramidDrop本身：在PyramidDrop内部，使用全部文本token（PDrop (all)，99.5% Avg）或显著性token（PDrop (S)，99.4% Avg）进行排名，均优于原始仅使用最后一个token的方案（PDrop，99.2% Avg），独立验证了文本引导剪枝范式的普适价值。

#### 簇宽度与主导token配置

**Figure 3**展示了簇宽度w对VQAT性能的影响。过小的w限制了上下文聚合范围，过大的w则退化为全局平均，存在一个最优区间使得局部信息保留与冗余消除达到平衡。

**Figure 7**（192 token budget）和**Figure 8**（128 token budget）分析了主导token数量k1的敏感性。在192 budget下，增加k1持续提升性能；在128 budget下，中等的主导-上下文比例（k1≈160）达到最佳平衡。这表明在不同压缩率下，主导信息保留与上下文聚合的资源配置需要差异化调整。

#### 语言模型侧丢弃层配置

**Figure 5**分析了在语言模型不同层丢弃视觉token的影响。红色叉号标记在最终层之前完全移除所有视觉token的配置，这些配置对性能影响极小，表明**在深层（第24层之后），相关视觉信息已被充分提取到隐藏状态中**，此时丢弃token几乎无损。这一发现为设计高效的逐层丢弃策略提供了依据。

**Figure 4**和**Figure 6**分别展示了第9层和第24层的显著性文本token对视觉token的交叉注意力热力图。第9层注意力仍集中在语义相关区域，而第24层注意力趋于均匀扩散，进一步佐证了深层丢弃的合理性。

### 失败模式与局限性

1. **极端压缩下的语义丢失**：在64 tokens（↓89%）时，准确率下降至95.4%（推理侧）或97.2%（训练侧），表明极低token预算下某些细粒度视觉问答任务（如VQAT）开始出现语义信息不足。这是所有压缩方法的共性瓶颈，DUET-VLM已将其推至更极端的压缩率。

2. **未进行逐层细粒度分析**：当前T2V剪枝在固定的stage（如第8、16、24层）执行，但未精确量化每层丢弃token的独立影响，可能错失更优的层间分配策略。

3. **视频扩展有限**：训练流程中的视频模型实验缺失，且仅在短时域视频上测试推理，长视频场景下的时序一致性保持尚待验证。

4. **跨模态泛化未探索**：双阶段压缩范式在音频-语言或纯文本模型上的适用性仍是开放问题。

### 关键图表结论汇总

- **Table 1**：推理侧，DUET-VLM (C)在所有压缩档位全面超越VisionZip和PyramidDrop，67%压缩下保持99.0%准确率。
- **Table 2**：跨架构泛化成功，Qwen-2.5-VL-7B上98.4%–99.9%准确率保持。
- **Table 4**：视频场景下，53%压缩时超越基线（100.8%），93%极端压缩仍保持97.6%。
- **Table 6**：训练时间减少31%的同时准确率仅降0.9%。
- **Table 7/Table 10**：局部聚类聚合是通用有效的即插即用模块，可独立提升VisionZip和DUET-VLM。
- **Table 11**：文本引导token选择的价值在PyramidDrop上得到独立验证。
- **Figure 5**：语言模型深层丢弃视觉token几乎无损，为逐层剪枝策略提供理论支撑。

![[assets/figures/papers/paper_list_l2218_https_arxiv_org_abs_2602_18846/figures/003_Table_1.jpg]]
*Table 1: Comparison of inference-only methods on LLaVA-1.5-7B. We report results across five benchmarks under different average token budgets, corresponding to 67%, 78%, and 89% token reduction. DUET-VLM (C) achieves the highest average performance across all settings, maintaining over 99% of the baseline accuracy while using significantly fewer tokens*

![[assets/figures/papers/paper_list_l2218_https_arxiv_org_abs_2602_18846/figures/004_Table_2.jpg]]
*Table 2: Comparison of inference-only methods on Qwen-2.5-VL-7B. We report results across five benchmarks under different average token budgets. DUET-VLM (C) achieves the highest average performance across all settings, maintaining over 98% of the baseline accuracy while using significantly fewer tokens*

![[assets/figures/papers/paper_list_l2218_https_arxiv_org_abs_2602_18846/figures/006_Table_4.jpg]]
*Table 4: Comparison of different methods on Video-LLaVA-7B. We evaluate performance across three benchmarks to demonstrate that DUET-VLM preserves accuracy even under substantial token compression*

![[assets/figures/papers/paper_list_l2218_https_arxiv_org_abs_2602_18846/figures/009_Table_6.jpg]]
*Table 6: Training time comparison on LLaVA-1.5-7B. DUET-VLM (C) offers favorable accuracy–efficiency trade-offs with over 30% reduction in training time while still maintaining over 99% accuracy*

![[assets/figures/papers/paper_list_l2218_https_arxiv_org_abs_2602_18846/figures/011_Table_7.jpg]]
*Table 7: Comparison showing benefts of our local cluster aggregation on LLaVA-1.5-7B across 6 benchmarks. We report numbers for different methods (M): LLaVA-1.5-7B (Base), Vanilla (V), VisionZip (VZ), VisionZip with our proposed clustering (VZ (C)), and DUET-VLM (Vanilla) (DV (V)) variants defined in Sec. 4.1*

## 定位与知识库关联

### 核心创新与差异化定位

DUET-VLM 的核心贡献在于首次将**视觉冗余感知的token合并**与**文本引导的逐层token丢弃**耦合为一个统一的即插即用双阶段压缩框架。现有方法或仅在视觉编码器侧进行早期一次性压缩（如VisionZip），或仅在语言模型侧进行分层丢弃（如PyramidDrop），二者均未能联合优化冗余消除与语义保留。DUET-VLM 的关键突破在于：

1. **局部聚类聚合替代全局平均**：VisionZip 将残差token全局平均为一个上下文token，导致细粒度视觉线索被稀释。DUET-VLM 引入基于V2V自注意力分数的局部聚类机制——以高注意力分数的token为质心，限制簇宽度 $w$，仅对簇内邻居进行局部平均，未分配token直接丢弃。这一改进在LLaVA-1.5-7B和LLaVA-NeXT-7B上均持续提升性能，尤其在低token预算下增益显著（Table 7, Table 10），证明了其作为即插即用模块的有效性。

2. **显著性文本token引导的逐层丢弃**：PyramidDrop 仅使用最后一个文本token的交叉注意力指导视觉token剪枝，忽略了查询中不同文本token对视觉区域的差异化关注。DUET-VLM 实验了多种文本token选择策略（最后一个token、全部查询token、显著性文本token），发现使用显著性文本token（C+S）或全部查询token（C+all）均优于原始方案（Table 8, Table 9）。在PyramidDrop内部复现该改进，同样验证了文本引导的价值（Table 11）。

### 与基线方法的关系网络

DUET-VLM 建立在两条互补的技术路线之上，并对其进行了实质性改进：

**视觉侧压缩路线（VisionZip 继承与超越）**：
- **VisionZip** (Yang et al., CVPR 2025)：通过V2V注意力分数选择主导token，将残差token全局平均为单个上下文token。DUET-VLM 保留其主导选择机制，但将全局平均替换为局部聚类聚合，解决了信息稀释问题。
- **PruMerge** (Shang et al., ICCV 2025)：基于注意力稀疏性聚类合并token，但未与语言侧压缩协同。
- **SparseVLM** (Zhang et al., ICLR 2025)：视觉token稀疏化方法，侧重于静态稀疏模式而非动态语义适应。

**语言侧压缩路线（PyramidDrop 继承与超越）**：
- **PyramidDrop** (Xing et al., CVPR 2025)：利用最后一个文本token的交叉注意力，在LLM的多个stage逐层丢弃低分视觉token。DUET-VLM 将其文本token选择策略从单一token扩展为多token显著性聚合，并在更早的视觉编码器阶段引入冗余消除，形成完整的双阶段流水线。
- **FastV** (Chen et al., ECCV 2024)：自适应注意力掩码剪枝，但缺乏分层策略。
- **HiRED** (Li et al., AAAI 2025)：基于CLS引导显著性的固定token预算分配，缺少文本引导的动态适应性。
- **FitPrune** (Ye et al., AAAI 2025)：训练无关的注意力分布匹配剪枝，侧重分布保持而非语义引导。

**基线模型**：
- **LLaVA-1.5-7B** (Liu et al., CVPR 2024)：使用576个固定视觉token，作为无压缩基线。
- **LLaVA-NeXT-7B**：动态token数量超过2800，计算开销更高。
- **Qwen-2.5-VL-7B**：动态token分配，验证DUET-VLM的跨架构泛化能力。
- **Video-LLaVA-7B**：视频领域扩展，使用2048个视觉token。

### 适用边界与泛化能力

**已验证的适用场景**：
- **静态图像理解**：在LLaVA-1.5-7B、LLaVA-NeXT-7B、Qwen-2.5-VL-7B三种不同架构上验证，覆盖固定token和动态token两种范式（Table 1, Table 2, Table 9）。
- **视频理解**：在Video-LLaVA-7B上，53.1% token压缩下超越基线（100.8%相对准确率），93.4%极端压缩下仍保持97.6%（Table 4）。
- **训练与推理双阶段**：推理时作为即插即用模块无需重新训练；训练时集成双阶段压缩可实现31%训练时间减少，准确率仅下降<1%（Table 6）。
- **压缩率范围**：从67%到93.4% token减少均保持高精度，覆盖中等至极端压缩场景。

**已知局限与未验证边界**：
- **架构覆盖有限**：未在LLaVA-NeXT以外的其他最新VLM架构（如InternVL、MiniCPM-V等）上进行广泛验证，跨架构泛化性证据尚不完整。
- **视频时序一致性**：视频实验仅在Video-LLaVA-7B上进行推理测试，未在训练流程中验证，也未探索更长时域视频的时序一致性保持问题。
- **模态扩展未探索**：双阶段压缩范式（局部聚类+文本引导丢弃）能否迁移到音频-语言模型、文本-语言模型等其他模态组合，仍为开放问题。
- **细粒度层分析缺失**：未进行精确的逐层丢弃影响量化，无法确定最优丢弃层配置的理论依据，当前配置依赖经验搜索。
- **推断延迟细节不足**：虽然报告了训练时间减少和推理速度提升（Table 5），但缺乏详细的延迟分解分析（如V2V合并开销、T2V剪枝开销各自占比）。

### 开放问题与未来方向

1. **自适应压缩策略**：当前 $k_1$、$k_2$、$w$ 等超参数需手动配置（Table 12-15）。能否学习一个轻量级控制器，根据输入图像的复杂度动态调整各阶段的压缩率？

2. **更细粒度的逐层稀疏化**：Figure 5 显示在LLM最后阶段完全丢弃视觉token对性能影响极小，暗示存在更优的非均匀层间分配策略。能否通过可微分搜索或强化学习自动发现最优的逐层保留比例？

3. **训练范式集成**：DUET-VLM 当前作为即插即用模块应用于推理或标准训练流程。能否将其无缝嵌入指令微调的不同阶段（如渐进式压缩课程学习），在训练早期保留更多token、后期逐步压缩？

4. **视频时序一致性**：对于视频输入，局部聚类和文本引导丢弃如何保持帧间token选择的一致性？是否需要引入时序正则化或光流引导的聚类约束？

5. **跨模态泛化验证**：局部聚类聚合和显著性引导丢弃的核心思想——基于自注意力冗余的局部合并与基于跨注意力语义的逐层剪枝——在音频-语言、点云-语言等模型中是否同样有效？

6. **与其他加速技术的协同**：DUET-VLM 的token压缩与KV缓存压缩、模型量化、投机解码等技术是否存在叠加增益或冲突？联合优化的帕累托前沿尚未探索。

7. **理论分析**：局部聚类聚合为何优于全局平均？是否存在信息论角度的解释（如互信息保留量）？文本引导丢弃的收敛性质如何？这些理论问题有助于指导更优的算法设计。

## 原文 PDF

![[paperPDFs/CVPR_2026/DUET_VLM_Dual_stage_Unified_Efficient_Token_reduction_for_VLM_Training_and_Inference.pdf]]
