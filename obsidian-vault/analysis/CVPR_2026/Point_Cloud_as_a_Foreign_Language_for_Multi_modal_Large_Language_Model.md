---
title: Point Cloud as a Foreign Language for Multi-modal Large Language Model
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Point_Cloud_as_a_Foreign_Language_for_Multi_modal_Large_Language_Model.pdf
code_link: "https://github.com/snehaputul/SAGE3D"
aliases:
- SSAGMSS
- PCAFLMMLLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 用可学习的轻量级3D tokenizer完全替代预训练编码器，通过最远点采样、近邻聚合和向量量化将点云转化为离散token序列，使LLM将3D数据视为“外语”直接处理；并引入基于语义对齐的偏好优化策略（GRPO + 语义/长度奖励）提升复杂3D问答的推理质量。
primary_logic: 将点云视为一种“外语”，利用离散token扩展LLM词汇表，实现无编码器的端到端多模态学习，从根本上消除几何-语言空间的对齐鸿沟，同时大幅提升计算效率和分辨率鲁棒性。
claims:
- SAGE是首个不依赖预训练3D编码器的端到端3D MLLM。
- 轻量级tokenizer通过几何采样、邻域聚合和向量量化将点云转换为离散token，使LLM将3D数据视为外语。
- SAGE-7B推理延迟仅100ms，比PointLLM-7B快2.3倍，吞吐量提升至10.0 samples/s。
- 向量量化（离散嵌入）相比连续嵌入在S-BERT评分上提升2.44分。
---

# Point Cloud as a Foreign Language for Multi-modal Large Language Model

> [!tip] 核心洞察
> 将点云视为一种“外语”，利用离散token扩展LLM词汇表，实现无编码器的端到端多模态学习，从根本上消除几何-语言空间的对齐鸿沟，同时大幅提升计算效率和分辨率鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 点云作为一种外语用于多模态大型语言模型 |
| 英文题名 | Point Cloud as a Foreign Language for Multi-modal Large Language Model |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.09173) · [Code](https://github.com/snehaputul/SAGE3D) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | SAGE (Spatial-Aware GEnerative model)；变体 SAGE∗（无偏好优化）与 SAGE（含偏好优化） |
| Dataset | Objaverse Captioning, Objaverse Classification, MM-Vet 3D VQA, Runtime Efficiency |

> [!tip] 效果简介
> - Objaverse Captioning (3D对象描述) 上，GPT-4 score 50.98 (SAGE-7B) / 52.87 (SAGE-13B) vs 44.85 (PointLLM-7B) / 48.94 (ShapeLLM-13B) (+6.13 / +3.93)。
> - Objaverse Classification (开集3D物体分类) 上，GPT-4 score 57.11 (SAGE-7B) / 58.48 (SAGE-13B) vs 54.50 (ShapeLLM-7B) / 54.00 (ShapeLLM-13B) (+2.61 / +4.48)。
> - MM-Vet 3D VQA 上，GPT-4 score 49.53 (SAGE-7B) / 54.89 (SAGE-13B) vs 47.40 (ShapeLLM-7B) / 53.10 (ShapeLLM-13B) (+2.13 / +1.79)。

## 概述

### 问题瓶颈

现有3D多模态大语言模型（3D MLLM）普遍依赖预训练的点云编码器（如PointBERT）来提取几何特征，这一范式带来三个核心瓶颈：

1. **语义错位**：编码器输出的是连续几何嵌入，与LLM的离散语言空间存在本质差异，导致跨模态对齐困难。
2. **分辨率脆弱**：编码器假设固定输入点数，对密度变化的真实扫描点云鲁棒性差。
3. **计算冗余**：大型编码器引入显著的推理延迟和显存开销，制约实际部署效率。

### 核心思路

本文提出**SAGE**（Spatial-Aware GEnerative model），将点云视为一种“外语”，从根本上消除对预训练3D编码器的依赖。其关键创新在于：

- 用**轻量级可学习3D tokenizer**替代传统编码器，通过最远点采样（FPS）、近邻聚合（KNN）和向量量化（VQ），将原始点云直接转化为离散token序列，作为LLM词汇表的自然扩展。
- 引入基于**语义对齐的偏好优化**策略（GRPO + 语义/长度奖励），提升复杂3D问答的推理质量。

这一设计使LLM能够以端到端方式直接“阅读”点云，无需经过中间编码器桥接，从根本上消除了几何-语言空间的对齐鸿沟。

### 方法定位

SAGE是**首个不依赖预训练3D编码器的端到端3D MLLM**。与PointLLM、ShapeLLM等依赖编码器的基线方法相比，SAGE的方法谱系发生根本性转变：

- **3D编码**：从“预训练编码器提取连续特征”转变为“轻量tokenizer直接生成离散token”。
- **训练管道**：在传统的“特征对齐 + 指令微调”两阶段基础上，新增第三阶段偏好优化（GRPO）。
- **输入表示**：从固定分辨率连续嵌入转变为可变分辨率点云的离散标记序列。

### 主要结果

SAGE在多个3D理解基准上以更小的计算代价取得领先性能：

- **3D对象描述**（Objaverse Captioning）：SAGE-7B GPT-4评分达50.98，超越PointLLM-7B（44.85）和ShapeLLM-13B（48.94）；SAGE-13B进一步提升至52.87。
- **开集3D分类**（Objaverse Classification）：SAGE-7B得分57.11，优于ShapeLLM-7B（54.50）。
- **3D视觉问答**（MM-Vet 3D VQA）：SAGE-7B得分49.53，SAGE-13B达54.89。
- **推理效率**：SAGE-7B延迟仅100 ms，比PointLLM-7B（239 ms）快2.4倍，吞吐量从4.2提升至10.0 samples/s。

消融实验证实，向量量化（离散嵌入）是性能关键——移除码本后S-BERT评分下降2.44分；最大池化聚合、码本大小8192、点标记数量512构成最优配置。

### 局限与展望

当前训练数据规模有限（主要基于Objaverse），偏好优化的潜在增益可能尚未完全释放。tokenizer与LLM的规模仍较小，向场景级3D理解或更复杂推理任务扩展时的效率与性能优势有待验证。此外，如何利用大规模无标注3D数据预训练tokenizer以降低标注依赖，是未来值得探索的方向。

## 背景与动机

### 3D多模态大模型的兴起与核心瓶颈

随着大语言模型（LLM）在文本理解与生成上的突破性进展，研究者开始将LLM的强大推理能力扩展至三维物理世界。3D多模态大语言模型（3D MLLM）应运而生，旨在使模型能够理解点云、网格等三维表示，并完成3D描述、问答、分类等任务。然而，现有3D MLLM普遍存在一个根本性瓶颈：**依赖预训练的3D编码器来提取点云特征**。

这一设计带来了三重困境：

1. **语义错位**：预训练编码器通常通过自监督几何任务（如掩码重建）获得表征能力，其输出嵌入空间与LLM的语言空间之间存在天然的语义鸿沟。即使经过对齐训练，几何特征与语言语义的错位仍难以根本消除，限制了模型对3D对象的深层语义理解。

2. **分辨率刚性**：现有编码器假设固定输入点数（如8192点），对密度变化的真实点云鲁棒性差。当输入点云稀疏或稠密程度偏离训练设定时，编码器提取的特征质量急剧下降，导致模型性能显著退化。

3. **计算冗余**：大容量3D编码器（如PointBERT等Transformer架构）引入显著的计算开销和推理延迟，成为端到端部署的瓶颈。在实时交互场景中，编码器带来的延迟往往占据总推理时间的相当比例。

### 从“编码器桥接”到“外语习得”的范式转变

上述困境的根源在于现有方法将3D编码器视为连接点云与LLM的“翻译器”——一种在几何域和语言域之间进行特征转换的中间件。本文提出了一种根本不同的思路：**将点云视为一种“外语”，通过离散token直接扩展LLM的词汇表，实现无编码器的端到端多模态学习**。

这一范式的核心洞见在于：LLM本质上是一个离散token序列的生成模型。如果能够将原始点云转化为离散token序列，那么3D数据就可以像一种新语言一样被LLM直接“阅读”和“理解”，无需任何中间编码器的翻译。这从根本上消除了几何-语言空间的对齐鸿沟，同时大幅提升了计算效率和分辨率鲁棒性。

### 本文动机与目标

基于上述观察，本文提出**SAGE（Spatial-Aware GEnerative model）**，旨在实现以下目标：

- **架构革新**：设计轻量级3D tokenizer，通过几何采样、邻域聚合和向量量化，将原始点云直接转化为离散token序列，完全替代预训练编码器。
- **端到端学习**：使LLM直接将3D数据视为“外语”处理，在统一的next-token prediction框架下进行端到端优化。
- **推理质量提升**：引入基于语义对齐的偏好优化策略，通过GRPO和语义/长度奖励函数，提升复杂3D问答的推理质量。
- **效率与鲁棒性**：显著降低推理延迟和显存占用，同时使模型能够自然适应不同分辨率的点云输入。

## 核心创新

SAGE 的核心创新在于**彻底移除预训练 3D 编码器**，将点云视为一种“外语”，通过端到端可学习的离散 token 化策略，从根本上消除几何嵌入与 LLM 语言空间之间的语义错位。以下从三个关键“changed slot”展开分析。

### 从连续编码器到离散 3D Tokenizer

现有 3D MLLM（如 **PointLLM**、**ShapeLLM**）普遍依赖预训练 3D 编码器（如 PointBERT）提取连续几何特征，再将特征投影到 LLM 嵌入空间。这一范式存在三个结构性瓶颈：

1. **语义错位**：编码器的几何表示空间与 LLM 的语言空间之间存在天然鸿沟，仅靠线性投影难以弥合。
2. **分辨率刚性**：编码器假设固定输入点数（如 8192 点），对密度变化的真实点云鲁棒性差。
3. **计算冗余**：大编码器引入显著的推理延迟和显存开销。

SAGE 的解决方案是用一个**轻量级 3D tokenizer** 完全替代预训练编码器。该 tokenizer 依次执行最远点采样（FPS）、K-近邻分组、局部聚合、线性投影和向量量化（VQ），将点云直接转化为离散 token 序列。核心公式为：

$$\mathbf{H} = \mathbf{Z} \mathbf{W} \in \mathbb{R}^{M \times d_{\mathrm{llm}}}$$

$$q(\mathbf{h}_i) = \arg \min_k \| \mathbf{h}_i - \mathbf{e}_k \|_2^2, \quad \mathbf{H}_q = \{ \mathbf{e}_{q(\mathbf{h}_i)} \}_{i=1}^M$$

其中 $\mathbf{Z}$ 为局部几何特征，$\mathbf{W}$ 为可学习投影矩阵，$\mathbf{e}_k$ 为码本向量。量化后的离散 token 直接与文本 token 拼接，形成混合模态输入序列：

$$[ \text{<p-start>}, e_{q(h_1)}, ..., e_{q(h_M)}, \text{<p-end>}, w_1, ..., w_L ]$$

这一设计的**因果机制**在于：离散 token 本质上扩展了 LLM 的词汇表，使 LLM 将 3D 数据视为一种“外语”直接处理，而非通过外部编码器的翻译层间接理解。消融实验证实了这一机制的有效性——移除向量量化（使用连续嵌入）导致 S-BERT 评分下降 2.44 分（Table A7：连续 47.67 vs 离散 50.11），证明离散化是实现几何-语言空间对齐的关键。

### 三阶段训练管道与偏好优化

SAGE 在典型两阶段训练（特征对齐 + 指令微调）的基础上，引入了第三阶段**偏好优化**，形成三阶段训练管道（见 Figure 3）：

- **Stage 1（3D Tokenizer 预热）**：联合训练 tokenizer 与部分 LLM 层，使用下一 token 预测目标在 3D 描述数据集上对齐几何 token 与语言表示空间。
- **Stage 2（指令微调）**：端到端指令微调，增强跨模态推理与指令跟随能力。
- **Stage 3（偏好优化）**：采用组相对策略优化（GRPO），利用基于语义相似度和长度正则化的奖励函数提升复杂 3D 问答的推理质量。

GRPO 的核心思想是：对同一问题生成 $m=8$ 个响应，以归一化优势 $A_i$ 鼓励模型提升相对高质量响应的生成概率：

$$\mathcal{L}_{\mathrm{GRPO}}(\theta) = -\frac{1}{m}\sum_{i=1}^m A_i \log \pi_\theta(y_i \mid q, \mathcal{P})$$

奖励函数由两部分组成——语义相似度奖励（以 Sentence-BERT 计算生成响应与参考响应的余弦相似度）和长度正则奖励（基于长度偏差的高斯惩罚）：

$$s_i^{(\mathrm{sem})} = \frac{\mathcal{E}(y_i) \cdot \mathcal{E}(y_{\mathrm{ref}})}{\|\mathcal{E}(y_i)\|_2 \|\mathcal{E}(y_{\mathrm{ref}})\|_2}$$

$$s_i^{(\mathrm{len})} = \exp\left(-\frac{(L_i - L_{\mathrm{ref}})^2}{2\sigma^2}\right)$$

这一设计直击 3D 推理中的**输出质量瓶颈**：标准指令微调仅优化逐 token 预测，缺乏对整体语义一致性和输出长度的显式约束。实验表明，SAGE（含偏好优化）在 Objaverse 描述任务上 GPT-4 评分达 50.98（7B）和 52.87（13B），分别超越 SAGE∗（无偏好优化）和所有现有方法（Table 1）。

### 可变分辨率输入与计算效率的联合提升

SAGE 的 tokenizer 通过 FPS 采样固定数量点（$N_s = 512$），天然支持可变分辨率输入。这一特性解决了传统编码器对固定输入点数的刚性依赖——当输入点云密度变化时，编码器性能显著退化，而 SAGE 在不同点云分辨率下保持描述性能稳定（Figure 4）。

消融实验进一步验证了 tokenizer 设计的合理性：点标记数量 512 达到精度与计算量的最佳平衡（128→48.98，512→50.11，1024 无提升）；码本大小 8192 取得最佳性能（继续增大至 16384 导致得分下降）；最大池化聚合优于平均池化和注意力池化（50.11 vs 49.89 vs 49.03）。

在计算效率方面，SAGE-7B 推理延迟仅 100 ms，比 PointLLM-7B（239 ms）快 2.4 倍，吞吐量从 4.2 提升至 10.0 samples/s（Table 2）。这一增益的根源在于：轻量级 tokenizer 消除了大编码器的前向计算开销，离散 token 使 LLM 的输入处理更加高效。

### 创新边界与待验证假设

尽管 SAGE 在对象级 3D 理解上取得了突破，但其创新存在明确边界：当前 tokenizer 和 LLM 规模仍较小，扩展到场景级 3D 理解（如室内场景）时，离散 token 对精细几何细节（如薄壁、锐利边缘）是否存在信息丢失尚不明确。此外，偏好优化中的语义相似度奖励是否足以捕捉复杂 3D 语义（如物理属性、功能关系），以及能否利用大规模无标注 3D 数据预训练 tokenizer 以降低标注依赖，均为开放问题，需进一步验证。

## 整体框架

SAGE 的整体设计遵循一个核心隐喻：**将点云视为一种“外语”**，从而让 LLM 无需任何预训练 3D 编码器即可直接理解三维几何信息。整个 pipeline 围绕一个轻量级、可端到端训练的 **3D Geometry Tokenizer** 展开，该 tokenizer 将原始点云转化为离散 token 序列，与文本 token 拼接后送入 LLM 主干进行联合推理。

### 数据流与模块关系

系统由三个关键模块串联构成，形成从原始点云到文本响应的完整数据流：

1. **3D Geometry Tokenizer**：接收任意分辨率的原始点云，依次执行最远点采样（FPS）、最近邻分组（KNN）、局部几何聚合、线性投影和向量量化（VQ），最终输出一组离散的 3D token。这一过程将无序、连续的三维坐标转化为 LLM 可理解的离散符号序列，从根本上消除了传统方法中几何嵌入与语言空间之间的语义错位。

2. **混合模态序列构建**：量化后的 3D token 嵌入与文本 token 嵌入直接拼接，并在点云片段前后插入特殊标记 `<p_start>` 和 `<p_end>`，形成统一的混合模态输入序列。LLM 将 3D token 视为其词汇表的自然扩展，以处理外语的方式理解三维结构信息。

3. **LLM 主干**：采用基于 LLaMA 的解码器架构，初始化自 Vicuna-7B/13B 检查点。LLM 接收混合模态序列，通过自回归方式生成文本响应，完成从三维感知到语言输出的端到端映射。

### 训练流程

整个框架通过三阶段训练逐步建立几何-语言的语义对齐（参见 Figure 3）：

- **阶段一：3D Tokenizer 预热**。联合训练 tokenizer 与 LLM 的部分层（实验表明 4 层最优），使用 3D 描述数据的下一 token 预测目标，初步对齐几何 token 与语言表示空间。
- **阶段二：指令微调**。在多模态指令-响应对上进行端到端微调，增强模型的跨模态推理与指令跟随能力。
- **阶段三：偏好优化**。引入基于 GRPO 的偏好优化策略，使用语义相似度奖励（Sentence-BERT 余弦相似度）和长度正则化奖励的组合函数，引导模型在复杂 3D 问答中生成更高质量的响应。

### 关键设计选择

- **离散化而非连续嵌入**：向量量化是框架的核心设计。消融实验表明，移除码本（使用连续嵌入）导致 S-BERT 评分下降 2.44 分，验证了离散 token 表示对几何-语言空间对齐的关键作用。
- **固定采样而非固定输入**：tokenizer 对输入点云执行 FPS 采样至固定数量（$N_s=512$），使模型天然支持可变分辨率输入，对密度变化的真实点云具有鲁棒性。
- **轻量级设计**：整个 tokenizer 仅包含可学习的投影矩阵和码本向量，无任何预训练编码器。这使得 SAGE-7B 的推理延迟仅 100 ms，比 PointLLM-7B 快 2.4 倍，吞吐量从 4.2 samples/s 提升至 10.0 samples/s。

### 补充图表

![[assets/figures/papers/paper_list_l2406_https_arxiv_org_abs_2603_09173/figures/001_Figure_1.jpg]]
*Figure 1: Our proposed encoder-free 3D Multimodal Large Language Model efficiently captures 3D information from point clouds without relying on any pretrained 3D encoder. The figure on the left illustrates the overall architecture, while the figure on the right shows an example conversation about an object generated by our model*

## 核心模块与公式推导

### 3D几何分词器（3D Geometry Tokenizer）

SAGE的核心创新在于用可学习的轻量级3D tokenizer完全替代传统的预训练几何编码器。该tokenizer将原始点云视为一种“外语”，通过几何采样、邻域聚合与向量量化，将连续的三维空间信息转化为离散的token序列，从而直接扩展LLM的词汇表。

**工作流程：**

1. **几何采样与分组**：对输入点云执行最远点采样（FPS），选取 $M$ 个锚点；对每个锚点，通过K近邻（KNN）搜索构建局部邻域，捕获局部几何结构。
2. **局部聚合**：在每个邻域内进行特征聚合（实验表明最大池化效果最优），得到局部几何特征矩阵 $\mathbf{Z} \in \mathbb{R}^{M \times d}$。
3. **投影到LLM空间**：通过可学习矩阵 $\mathbf{W}$ 将几何特征投影到LLM的嵌入维度：

$$\mathbf{H} = \mathbf{Z} \mathbf{W} \in \mathbb{R}^{M \times d_{\mathrm{llm}}}$$

4. **向量量化**：将每个投影特征 $\mathbf{h}_i$ 量化到可学习码本 $\{\mathbf{e}_k\}_{k=1}^K$ 中最近的向量，得到离散表示：

$$q(\mathbf{h}_i) = \arg \min_k \| \mathbf{h}_i - \mathbf{e}_k \|_2^2, \quad \mathbf{H}_q = \{ \mathbf{e}_{q(\mathbf{h}_i)} \}_{i=1}^M$$

向量量化损失由码本损失和承诺损失两部分组成，使用停止梯度操作 $\mathrm{sg}[\cdot]$ 分别约束：

$$\mathcal{L}_{\mathrm{VQ}} = \| \mathrm{sg}[\mathbf{H}] - \mathbf{H}_q \|_2^2 + \beta \| \mathbf{H} - \mathrm{sg}[\mathbf{H}_q] \|_2^2$$

其中 $\beta$ 为承诺损失权重。消融实验证实，离散嵌入（含码本）相比连续嵌入在S-BERT评分上提升2.44分（50.11 vs 47.67），验证了向量量化对语义对齐的关键作用。

### 混合模态序列构建

量化后的离散3D token直接与文本token拼接，并插入特殊边界标记，形成LLM的混合模态输入序列：

$$[ \texttt{<p\_start>}, \mathbf{e}_{q(\mathbf{h}_1)}, \dots, \mathbf{e}_{q(\mathbf{h}_M)}, \texttt{<p\_end>}, w_1, \dots, w_L ]$$

这种设计使LLM能够将3D几何信息与自然语言统一处理，从根本上消除了传统方法中几何嵌入与语言空间之间的语义错位。

### 总训练损失

框架采用端到端优化，总损失为下一token预测损失与向量量化损失的加权和：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{NTP}} + \lambda \mathcal{L}_{\mathrm{VQ}}$$

其中 $\lambda$ 平衡语言建模与几何离散化两个目标。

### 偏好优化中的奖励函数

在第三阶段偏好优化中，SAGE引入基于语义对齐的复合奖励函数，用于GRPO（组相对策略优化）。

**语义相似度奖励**：使用Sentence-BERT编码器 $\mathcal{E}$ 计算生成响应 $y_i$ 与参考响应 $y_{\mathrm{ref}}$ 的余弦相似度：

$$s_i^{(\mathrm{sem})} = \frac{\mathcal{E}(y_i) \cdot \mathcal{E}(y_{\mathrm{ref}})}{\|\mathcal{E}(y_i)\|_2 \|\mathcal{E}(y_{\mathrm{ref}})\|_2}$$

**长度正则奖励**：基于生成响应长度 $L_i$ 与参考长度 $L_{\mathrm{ref}}$ 的偏差，使用高斯函数鼓励输出长度适中：

$$s_i^{(\mathrm{len})} = \exp\left(-\frac{(L_i - L_{\mathrm{ref}})^2}{2\sigma^2}\right)$$

**GRPO优化目标**：对每个输入问题 $q$ 和点云 $\mathcal{P}$，生成 $m$ 个候选响应，利用归一化优势 $A_i$ 鼓励模型提升高质量响应的生成概率：

$$\mathcal{L}_{\mathrm{GRPO}}(\theta) = -\frac{1}{m}\sum_{i=1}^m A_i \log \pi_\theta(y_i \mid q, \mathcal{P})$$

实验设置 $m=8$，在指令微调数据上训练1个epoch。

### 补充图表

![[assets/figures/papers/paper_list_l2406_https_arxiv_org_abs_2603_09173/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of our proposed method, encoder-free 3D Multimodal Large Language Model*

![[assets/figures/papers/paper_list_l2406_https_arxiv_org_abs_2603_09173/figures/003_Figure_3.jpg]]
*Figure 3: The proposed training pipeline of our model. The model is trained in three stages — each stage focusing on a specific training objective*

## 实验与分析

### 核心性能突破：无编码器范式的主基准验证

SAGE在Objaverse描述任务上建立了显著的性能优势。**SAGE-7B**的GPT-4评分达到**50.98**，相比PointLLM-7B（44.85）提升**+6.13**，甚至超越参数量更大的ShapeLLM-13B（48.94）达+2.04分。扩展至13B参数后，**SAGE-13B**进一步提升至**52.87**，较PointLLM-13B（48.15）领先**+4.72**。这一结果表明，用轻量级tokenizer替代预训练编码器不仅消除了几何-语言空间的语义错位，还释放了更强的跨模态描述能力。

在开集3D物体分类任务上，SAGE-7B获得**57.11**分，超越ShapeLLM-7B（54.50）达+2.61；SAGE-13B以**58.48**分领先ShapeLLM-13B（54.00）达+4.48。MM-Vet 3D VQA基准上，SAGE-7B（**49.53**）和SAGE-13B（**54.89**）分别超越对应基线2.13和1.79分，证明该范式在复杂3D推理场景中同样有效。

值得注意的是，**SAGE∗**（不含偏好优化）已在多数基准上匹配或超越现有依赖预训练编码器的方法，这直接验证了“点云作为外语”这一核心洞察的有效性——仅凭离散token扩展LLM词汇表，即可实现端到端的几何-语言对齐。

### 效率革命：推理延迟与吞吐量的数量级提升

SAGE的效率优势是其另一决定性证据。在NVIDIA H100 GPU、8K输入点的相同条件下，**SAGE-7B推理延迟仅100 ms**，而PointLLM-7B需要239 ms，实现了**2.4倍加速**。吞吐量方面，SAGE-7B达到**10.0 samples/s**，是PointLLM-7B（4.2 samples/s）的**2.4倍**。这一效率增益源于完全消除重型预训练编码器的计算开销，使SAGE在实际部署中具备显著优势。

### 消融实验：离散化与架构选择的关键性

消融实验揭示了方法设计的因果机制：

- **向量量化的决定性作用**：移除码本、使用连续嵌入直接输入LLM时，S-BERT评分从50.11降至47.67（-2.44），明确证明离散化是消除语义错位的核心操作。连续嵌入无法迫使tokenizer学习紧凑、结构化的表示空间，导致LLM难以将几何特征“理解”为可操作的token。

- **码本大小的最优平衡**：码本从4096增至8192时性能提升1.23分，但继续扩大至16384反而导致性能下降。这表明8192的离散空间在表达能力与泛化性之间达到了最优折衷——过大的码本可能引入稀疏性，使训练不稳定。

- **点标记数量的效率-精度权衡**：采样128点得分仅48.98，512点提升至50.11，继续增至1024点无额外增益。512个点标记在捕获足够几何信息的同时，保持了序列长度的可控性，是计算效率与描述精度的最佳平衡点。

- **聚合策略的选择**：最大池化（50.11）优于平均池化（49.89）和注意力池化（49.03）。最大池化对局部几何特征的显著性选择更契合点云的稀疏结构，而注意力池化可能因数据量有限而欠拟合。

- **阶段1可训练层数的过拟合边界**：训练4层LLM效果最优，继续增加可训练层数导致性能下降，说明在有限数据下过度放开LLM参数会破坏预训练语言知识，引发过拟合。

### 分辨率鲁棒性：对密度变化的天然适应

SAGE天然支持可变分辨率输入，这是其相对于依赖固定输入编码器方法的关键优势。Figure 4显示，在Objaverse描述任务上，SAGE在不同点云分辨率下保持稳定的GPT-4评分，而传统编码器方法在点数偏离训练设定时性能急剧下降。这一鲁棒性源于tokenizer的采样机制——无论输入点云原始密度如何，FPS始终采样固定数量（512）的代表性点，使模型对稀疏或稠密输入均能保持一致的几何理解。

### 定性分析：描述质量的结构化优势

Table 3的定性对比显示，SAGE生成的描述在几何细节的精确性上显著优于基线。例如，对复杂形状物体，SAGE能准确描述“弯曲的扶手”和“锥形底座”，而PointLLM常出现几何属性混淆（如将“圆形”误述为“方形”）。这表明离散token表示迫使模型学习更结构化的几何-语义映射，而非依赖编码器提取的模糊连续特征。

### 偏好优化的增益与局限

Stage 3的GRPO偏好优化在SAGE∗基础上进一步提升性能，但其增益幅度（约1-2分）相对有限。这主要受限于训练数据规模——Objaverse数据集虽包含大量3D对象，但每个对象的文本描述相对简短，限制了语义相似度奖励区分高质量与低质量响应的能力。此外，长度正则项权重α=1.0时性能下降，说明完全依赖长度惩罚会抑制模型生成详细描述，最优α值需针对任务精细调节。这一发现提示，在更大规模、更多样化的3D指令数据上进行偏好优化可能释放更大潜力，但当前设定下该阶段的贡献需谨慎解读。

### 补充图表

![[assets/figures/papers/paper_list_l2406_https_arxiv_org_abs_2603_09173/figures/004_Table_1.jpg]]
*Table 1: Performance comparison on various 3D downstream tasks. Here, the Objaverse dataset is used for 3D object captioning and recognition tasks, and the MM-Vet dataset is used for 3D VQA. In addition to our full model (SAGE), we provide the results without the preference optimization (SAGE∗). Additional comparisons with existing methods on different datasets are provided in the Appendix A3*

![[assets/figures/papers/paper_list_l2406_https_arxiv_org_abs_2603_09173/figures/005_Figure_4.jpg]]
*Figure 4: Performance of SAGE on diverse ranges of point cloud resolution on 3D captioning task on Objaverse dataset*

![[assets/figures/papers/paper_list_l2406_https_arxiv_org_abs_2603_09173/figures/006_Table_2.jpg]]
*Table 2: Runtime Complexity Comparison. Inference latency (ms) and memory (GB) on H100 GPU, 8K points, and Objaverse dataset*

![[assets/figures/papers/paper_list_l2406_https_arxiv_org_abs_2603_09173/figures/007_Table_3.jpg]]
*Table 3: Qualitative results on Objaverse. We adopt this table from [68], and compare our proposed model’s generated description for the specific 3D object samples*

![[assets/figures/papers/paper_list_l2406_https_arxiv_org_abs_2603_09173/figures/010_Figure.jpg]]
*Figure: A1. Fig. (Left) Impact of the number of LLM trainable layers during the stage 1 training. Fig. (Middle) Impact of the number of LLM trainable layers during stage 1 training. Fig(Right) Impact of group normalization coefficient on performance of SAGE-7B*

![[assets/figures/papers/paper_list_l2406_https_arxiv_org_abs_2603_09173/figures/015_Figure.jpg]]
*Figure: (a) Codebook size. (b) Number of point tokens. (c) Types of pooling layers. Figure A2. Dialogues between PointLLM and a human user*

![[assets/figures/papers/paper_list_l2406_https_arxiv_org_abs_2603_09173/figures/016_Table.jpg]]
*Table: A7. Impact of discrete vs. continuous point embeddings*

![[assets/figures/papers/paper_list_l2406_https_arxiv_org_abs_2603_09173/figures/009_Table.jpg]]
*Table: A2. Performance comparison with existing methods. We adopt the following table from and follow the notations and categorization defined by them. Here, “Specialist Model” refers to models specifically designed for individual tasks such as 3D question answering, 3D dense captioning, or referring segmentation. “Finetuned 3D MLLMs” denotes models that are jointly trained and subsequently fine-tuned on each dataset before evaluation. “3D MLLMs” represents models trained on multiple tasks without task-specific fine-tuning. “PC” stands for point cloud, and “I” denotes multi-view images. Note that the results of LEO on ScanQA are shown in gray and excluded from direct comparison, as the m...*

![[assets/figures/papers/paper_list_l2406_https_arxiv_org_abs_2603_09173/figures/014_Table.jpg]]
*Table: A5. Performance comparison across three runs on (SAGE) and (SAGE∗) on 7B parameters. Here, the Objaverse dataset is used for 3D object captioning and recognition tasks, and the MM-Vet dataset is used for 3D VQA. Table A6. Sensitivity study on different model-specific parameters on ModelNet40*

## 方法谱系与知识库定位

### 与现有工作的关系

**SAGE** 在3D多模态大语言模型（3D MLLM）领域引入了一个根本性的架构转向：将点云视为一种“外语”，通过离散token直接扩展LLM的词汇表，从而完全摒弃了预训练3D编码器。这一设计使其与依赖编码器的现有工作形成了清晰的方法论分界线。

*   **相对于编码器依赖型3D MLLM（如 PointLLM, ShapeLLM）**：现有主流方法遵循“预训练3D编码器提取连续几何特征 → 特征投影 → LLM处理”的范式。例如，**PointLLM** 依赖预训练的PointBERT等编码器将点云转换为连续嵌入，再通过一个投影层与LLM的文本空间对齐。**SAGE** 的核心颠覆在于用可学习的轻量级3D tokenizer替代了整个预训练编码器。该tokenizer通过“最远点采样（FPS）+ K近邻聚合（KNN）+ 向量量化（VQ）”的流程，将点云直接转化为离散的token序列。这一改变从根源上消除了几何嵌入与LLM语言空间之间可能存在的语义错位（semantic misalignment），因为离散token本身就是LLM词汇表的一部分，无需额外的对齐步骤。实验表明，即使是不含偏好优化的SAGE*变体，其性能也已匹配或超越了依赖广泛预训练的现有方法，而完整的SAGE模型则在多个基准上全面领先。

*   **相对于通用多模态指令跟随模型（如 LLaVA, InstructBLIP）**：这些模型主要面向2D图像-文本多模态任务，其架构通常包含一个预训练的视觉编码器（如ViT）。SAGE将这一思路拓展至3D领域，但并未简单地将图像编码器替换为3D编码器，而是选择了更激进的“无编码器”路线，证明了对于3D数据，离散token化是一条高效且高性能的可行路径。

*   **相对于向量量化（VQ）在3D表征学习中的应用**：VQ方法在3D形状生成和自监督学习中已有探索，但SAGE是首次将其作为连接原始3D数据和LLM的核心桥梁，并系统地验证了其在多模态理解任务中的有效性。消融实验提供了决定性证据：移除向量量化（即使用连续嵌入）会导致S-BERT评分下降2.44分（从50.11降至47.67），强有力地证明了离散化对于对齐几何与语言空间的关键作用。

### 适用边界与局限

尽管SAGE在效率和性能上展现出显著优势，但其当前设计仍存在明确的适用边界和局限，需在实际应用中审慎考量。

1.  **训练数据规模与泛化性**：当前模型的训练主要基于Objaverse数据集。虽然该数据集规模可观，但相较于互联网规模的图文数据，其多样性和数量仍相对有限。这可能导致模型在处理训练分布之外的、具有罕见几何结构或复杂语义的3D对象时，性能出现下降。偏好优化阶段的潜在增益也可能因数据量有限而未能完全释放。在更大规模、更多样化的3D数据上的表现有待进一步验证。

2.  **对比公平性**：论文明确指出，与某些现有方法的直接对比存在不公平性，因为部分工作可能使用了额外的训练数据或不同的预训练任务。本文的所有比较均在相同的训练数据（Objaverse + Cap3D）和评估协议下进行，以确保结论的可靠性，但这也意味着SAGE的优势是在一个相对受控的设定下建立的。

3.  **偏好优化的超参敏感性**：偏好优化阶段的奖励函数由语义相似度和长度正则化两项加权构成。消融实验发现，当长度正则项的权重 α=1.0 时，模型性能反而下降，这表明长度奖励是必要的，但其最优权重需要针对不同任务进行仔细调节，可能无法作为一个通用的固定超参。

4.  **场景级理解的扩展性**：目前的tokenizer和LLM规模（7B/13B）主要针对物体级别的3D理解任务（如Objaverse描述和分类）。当任务扩展到场景级点云（如室内场景S3DIS、ScanNet）或更复杂的3D推理（如功能性推理、物理属性判断）时，固定采样点数（如512点）的tokenizer可能无法充分捕获大尺度、高复杂度的几何信息。如何在不显著增加计算成本的前提下扩展tokenizer的能力，仍是一个开放问题。

### 开放问题

基于SAGE当前的设计和局限，以下几个方向构成了未来研究的关键开放问题：

*   **如何高效扩展至大规模场景？** 当前的tokenizer设计（FPS + KNN）在处理包含数十万点的场景点云时，计算成本会显著增加。探索层次化tokenization、稀疏注意力机制或可学习的场景分块策略，是将其能力从物体级推向场景级理解的关键。
*   **离散token能否保留精细几何细节？** 向量量化本质上是一种有损压缩。对于薄壁、锐利边缘等精细几何特征，是否存在信息丢失？能否通过引入可学习的动态码本调整机制，或结合残差量化（Residual VQ）来弥补这一潜在缺陷？
*   **语义奖励是否足够捕捉复杂3D语义？** 当前的偏好优化仅使用基于Sentence-BERT的语义相似度作为奖励。对于物理属性（如“是否稳定”）、功能关系（如“能否用于坐”）等更深层的3D语义，这种奖励信号可能不够结构化。是否需要引入物理模拟器反馈、功能可供性（affordance）标注等更丰富的奖励信号？
*   **能否利用无标注3D数据进行预训练？** 当前训练pipeline依赖配对的3D-文本数据。能否设计自监督任务，利用大规模无标注点云数据来预训练3D tokenizer，从而降低对昂贵文本标注的依赖，并提升模型的泛化能力？
*   **框架能否无缝迁移至其他3D任务？** 该端到端框架目前主要验证了3D描述、分类和VQA任务。对于3D定位（3D grounding）、指代表达理解（referring expression comprehension）等需要细粒度空间指代的任务，是否需要定制化的tokenizer设计或奖励函数？这是验证其通用性的重要一步。

## 原文 PDF

![[paperPDFs/CVPR_2026/Point_Cloud_as_a_Foreign_Language_for_Multi_modal_Large_Language_Model.pdf]]