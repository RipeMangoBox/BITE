---
title: "IF-Prune: Information-Flow Guided Token Pruning for Efficient Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/IF_Prune_Information_Flow_Guided_Token_Pruning_for_Efficient_Vision_Language_Models.pdf
project_link: null
code_link: "https://github.com/snap-research/EVLM-IF-Prune"
aliases:
- IP
- IF-Prune
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过后验引导的信息瓶颈，利用小模型输出的 KL 散度对每个视觉令牌的信息量进行软量化，使剪枝信号同时感知查询和答案内容，为大型 VLM 保留更广泛的上下文线索而非仅答案相关令牌。
primary_logic: 将视觉令牌剪枝从答案驱动的启发式转换为摊销变分推断问题，使小型 VLM 学会输出令牌级后验分布，并以信息瓶颈正则化自动区分信息性令牌与冗余令牌，从而在极低令牌保留率下仍保持大型模型的强大推理能力。
claims:
- 在仅保留 5% 视觉令牌时，IF-Prune 仍能保持原模型 95.4% 的性能，超越 SGP 6.5 个百分点。
- IF-Prune 生成的令牌重要性图比 SGP 包含更广泛的上下文信息，避免仅聚焦于答案直接相关的少数令牌。
- 一个经过训练的小型 VLM 可以无需额外训练，便为同架构的大型 VLM（如从 1B 到 26B）提供有效的剪枝指引。
- InternVL2-26B (8 基准平均) 上 Score Ratio vs. Full Tokens = 95.41% (K=5%)
---

# IF-Prune: Information-Flow Guided Token Pruning for Efficient Vision-Language Models

> [!tip] 核心洞察
> 将视觉令牌剪枝从答案驱动的启发式转换为摊销变分推断问题，使小型 VLM 学会输出令牌级后验分布，并以信息瓶颈正则化自动区分信息性令牌与冗余令牌，从而在极低令牌保留率下仍保持大型模型的强大推理能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | IF-Prune：信息流引导的视觉令牌剪枝用于高效视觉语言模型 |
| 英文题名 | IF-Prune: Information-Flow Guided Token Pruning for Efficient Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Sun_IF-Prune_Information-Flow_Guided_Token_Pruning_for_Efficient_Vision-Language_Models_CVPR_2026_paper.html) · [Code](https://github.com/snap-research/EVLM-IF-Prune) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | IF-Prune |
| Dataset | InternVL2-26B, InternVL2-8B |

> [!tip] 效果简介
> - InternVL2-26B (8 基准平均) 上，Score Ratio vs. Full Tokens 95.41% (K=5%) vs 88.91% (SGP, K=5%) (+6.50%)。
> - InternVL2-8B (迁移实验) 上，Score % (K=5%) 94.03% vs 90.34% (SGP) (+3.69%)。
> - InternVL2-26B (效率) 上，总 FLOPs %（相对无剪枝基准） 62.9% (K=5%, L=2) vs 100% (无剪枝) (-37.1%)。

## 概述

视觉语言模型（VLM）的推理成本随输入图像分辨率的提升而急剧增长，视觉令牌剪枝成为降低计算开销的关键手段。然而，现有剪枝方法存在根本性瓶颈：以 **SGP**（Zhao et al., CVPR 2025）为代表的方案依赖小模型在自回归生成过程中积累的注意力权重来评估令牌重要性，这种答案驱动的机制在面对需要复杂视觉推理的查询时，生成的重要性图包含大量噪声，无法为大型 VLM 保留足够的上下文线索，导致推理精度大幅下降。

IF-Prune 将视觉令牌剪枝从启发式规则转化为**摊销变分推断问题**。其核心思想是：训练一个小型 VLM，通过后验引导的信息瓶颈，利用令牌级 KL 散度对每个视觉令牌的信息量进行软量化。剪枝信号同时感知查询和答案内容，为大型 VLM 保留更广泛的上下文信息，而非仅聚焦于答案直接相关的少数令牌。

在方法谱系中，IF-Prune 区别于三类基线：**SGP** 聚合全部生成令牌的注意力权重，**FastV**（Chen et al., ECCV 2024）仅使用首个生成令牌的交叉注意力逐步剪枝，**ToME**（Bolya et al., ICLR 2023）则在视觉编码器内部基于相似性合并令牌。IF-Prune 的关键创新在于：仅需小模型一次前向传播即可产生全部令牌的重要性分数，无需自回归生成，且引入通道级可学习门控以稳定后验均值估计。

主要实验结果确立了 IF-Prune 的有效性：在仅保留 **5%** 视觉令牌的极端条件下，大型 VLM（InternVL2-26B）仍保持原模型 **95.4%** 的性能，超越 SGP **6.5 个百分点**，同时总 FLOPs 降低约 **40%**。更重要的是，一个在 1B 模型上训练的剪枝指引可直接迁移至同架构的 8B 甚至 26B 模型，无需额外训练，展现出良好的泛化能力。

## 背景与动机

### 视觉令牌冗余：大型 VLM 的效率瓶颈

大型视觉语言模型（Large VLMs）通常将图像编码为数百至数千个视觉令牌，并将其与文本令牌拼接后送入大语言模型解码器。这种设计虽然赋予模型强大的多模态理解能力，但也带来了显著的计算开销——视觉令牌的数量直接决定了自注意力机制中键值缓存（KV Cache）的规模和计算量。随着模型规模从数十亿参数扩展到数百亿参数，冗余视觉令牌造成的算力浪费已成为限制 VLM 实际部署的核心瓶颈。

现有的令牌剪枝方法试图通过识别并丢弃不重要的视觉令牌来缓解这一问题。这些方法大致可分为两类：一类在视觉编码器内部操作，如 **ToME**（Bolya et al., ICLR 2023）通过合并编码器中相似令牌来减少数量；另一类在解码器端操作，利用交叉注意力权重判断令牌重要性，如 **FastV**（Chen et al., ECCV 2024）和 **SGP**（Zhao et al., CVPR 2025）。

### 答案驱动剪枝的固有缺陷

SGP 代表了当前的主流范式：使用一个预训练的小型 VLM 生成答案，在自回归生成过程中聚合所有生成令牌对视觉令牌的注意力权重，以此构建重要性图，然后将其应用于大型 VLM 的剪枝。这一策略的核心假设是——小模型关注的令牌就是大模型需要的令牌。

然而，这一假设存在根本性缺陷。小模型的推理能力有限，其生成的注意力分布高度偏向于直接支撑答案的少数令牌，形成一种**答案驱动（answer-driven）**的先验。当面对需要复杂视觉推理的查询时（如空间关系判断、多物体属性比较），这种狭窄的注意力聚焦会遗漏大量关键的上下文信息——那些虽不直接出现在答案中，但却是正确推理所必需的视觉线索。图 1(a) 直观地展示了这一问题：SGP 的重要性图仅高亮与答案词直接相关的少量区域，而忽略了支撑推理过程的广泛视觉上下文。

实验数据进一步证实了这一缺陷的严重性：在仅保留 5% 视觉令牌的激进剪枝设置下，SGP 仅能维持原模型 88.9% 的性能，而 FastV 更是急剧退化至 67.1%。这表明，将剪枝决策完全委托给一个能力有限的小模型，本质上是将大模型的推理能力限制在了小模型的“视野”之内。

### 从答案驱动到后验引导：范式逆转

IF-Prune 的核心动机在于**逆转这一范式**：不再要求小模型直接判断“哪些令牌对答案最重要”，而是训练小模型学习“每个令牌携带了多少查询相关的信息量”。这一转变将剪枝问题从启发式的注意力聚合，提升为一种有原则的**摊销变分推断（amortized variational inference）**问题。

具体而言，IF-Prune 在小型 VLM 的输出端引入一个轻量级的信息瓶颈投影模块，将每个视觉令牌映射到一个隐变量的后验高斯分布。该后验分布与一个可学习先验之间的 KL 散度，自然地量化了该令牌在给定查询条件下的信息贡献——信息量越大的令牌，其后验偏离先验越远，KL 散度越大。这一**后验引导（posterior-driven）**的机制使剪枝信号同时感知查询内容和视觉特征，而非仅聚焦于答案词，从而为大型 VLM 保留了更广泛的推理上下文（图 1(b)）。

这一设计的另一个关键优势在于效率：小模型仅需一次前向传播即可产生所有令牌的重要性分数，无需像 SGP 那样进行完整的自回归生成。这从根本上消除了小模型推理带来的额外延迟开销。

## 核心创新

IF-Prune 的核心创新在于将视觉令牌剪枝从一个**答案驱动的启发式任务**重构为**后验引导的摊销变分推断问题**。与现有方法相比，这一范式转变体现在三个关键维度的机制改进上。

### 从答案驱动到后验引导的重要性估计

现有剪枝方法，如 **SGP**（Zhao et al., CVPR 2025），通过聚合小模型自回归生成过程中所有输出令牌对视觉令牌的注意力权重来产生重要性图。这种机制本质上是**答案驱动的**——它依赖小模型先“想好”答案，再回溯哪些视觉令牌对生成该答案贡献最大。然而，当面对需要复杂视觉推理的查询时，小模型自身能力有限，其生成的答案可能不准确，导致重要性图包含大量噪声，无法为大型 VLM 保留关键上下文。

IF-Prune 彻底颠倒了这一范式：不再让小模型“决定”哪些令牌重要并强制大模型遵循，而是训练小模型学习输出每个视觉令牌的**后验分布**，并以该分布与可学习先验之间的 KL 散度作为令牌重要性的软量化信号。这一设计使剪枝信号同时感知查询和答案内容，为大型 VLM 保留更广泛的上下文线索，而非仅聚焦于答案直接相关的少数令牌。

### 令牌级变分信息瓶颈框架

IF-Prune 将视觉令牌重要性估计形式化为一个**令牌级变分信息瓶颈**问题。具体而言，方法引入了一个轻量级投影模块 $Q_\theta$，将小模型输出的查询感知视觉特征 $V'$ 映射为高斯后验参数：

$$Q_{\theta}(Z_i \mid V_i') = \mathcal{N}(\mu_{\theta}(V_i'), \sigma_{\theta}^2(V_i'))$$

每个视觉令牌的信息量通过其通道平均 KL 散度量化：

$$D_{\mathrm{KL}}(Q_{\theta}(\boldsymbol{Z}_i \mid \boldsymbol{V}_i') \| P(\boldsymbol{z})) = \frac{1}{d} \sum_{j=1}^{d} D_{\mathrm{KL}}(Q_{\theta}(\boldsymbol{Z}_i^{(j)} \mid \boldsymbol{V}_i'^{(j)}) \| P(\boldsymbol{z}^{(j)}))$$

这一框架的关键优势在于：KL 散度天然度量了令牌后验分布相对于无信息先验的偏离程度，偏离越大意味着该令牌包含的查询-图像交互信息越丰富，应当被保留。与 SGP 的注意力聚合相比，这种信息论度量不依赖小模型生成正确答案的能力，因此即使在小模型自身推理能力不足时，仍能为大模型提供有效的剪枝指引。

### 通道级门控后验均值估计

为确保训练的稳定性和后验推断的表达能力，IF-Prune 在投影模块中引入了**通道级可学习门控机制**：

$$\mu_{\theta}(V_i') = \sigma(I_{\theta}(V_i')) \odot (V_i' - \mu_p) + \mu_p$$

其中 $\sigma(\cdot)$ 为 sigmoid 函数，$I_{\theta}$ 为可学习的门控网络，$\mu_p$ 为可学习先验均值。该设计的双重作用在于：sigmoid 门控将后验均值相对先验的偏移量限制在可控范围内，防止训练初期后验坍塌；同时，通道级门控赋予模型对不同特征维度差异化建模的能力，使后验分布能够更精细地捕捉令牌的信息含量。消融实验证实，sigmoid 门控在整体得分上优于指数门控 0.97%（90.80% vs. 89.83%），验证了这一设计的有效性。

### 单次前向传播的高效剪枝指引

与 SGP 需要小模型自回归生成至结束令牌才能计算重要性分数不同，IF-Prune 仅需**一次小模型预填充前向传播**即可产生全部令牌的重要性分数。这一效率提升源于方法将重要性估计与答案生成解耦：KL 散度的计算仅依赖小模型对视觉和文本输入的编码结果，无需等待解码过程完成。在 InternVL2-26B 上的延迟测试显示，IF-Prune 的预填充延迟仅为 238.5 ms，而 SGP 高达 524.5 ms，效率提升超过 2 倍。

### 跨模型规模的剪枝指引迁移

IF-Prune 的另一个重要特性是**剪枝指引的可迁移性**：一个在 InternVL2.5-1B 上训练的信息瓶颈模块，可以直接为同架构的更大规模模型（如 InternVL2-8B、InternVL2-26B）提供剪枝指引，无需针对大模型进行额外训练。这是因为 KL 散度衡量的令牌信息量是模型架构相关的内在属性，而非特定于模型规模。迁移实验表明，在 InternVL2-8B 上，IF-Prune 以 5% 令牌保留率仍达到 94.03% 的性能，比 SGP 高出 3.69 个百分点，验证了该特性的实用价值。

## 整体框架

IF-Prune 的整体推理管线由三个串联模块构成，形成“小模型感知—信息瓶颈评分—大模型剪枝推理”的闭环。其核心设计在于将视觉令牌重要性估计从答案驱动的启发式转换为**后验引导的信息瓶颈**，使剪枝信号同时感知查询与答案内容，为大型 VLM 保留更广泛的上下文线索。

### 模块一：Small VLM（π_φ）——查询感知的视觉特征提取

管线首先调用一个轻量的小型视觉语言模型 **π_φ**，其参数初始化为预训练的 InternVL2.5-1B 并在后续微调中通过 LoRA 适配。对于给定的文本查询 **X** 和原始视觉令牌集 **V**，小模型执行一次前向传播（仅预填充，无需自回归生成），输出融合了查询信息的视觉嵌入 **V′**。由于序列到序列 LLM 中的因果注意力机制，**V′** 通过跨注意力自然融合了 **X** 的先验查询信息（见图 2 示意）。这一设计使得后续的重要性评分天然具备查询感知能力，同时避免了 SGP 等方法需要小模型自回归生成至结束令牌的高昂开销。

### 模块二：Information Bottleneck Projection Module（Q_θ）——令牌级后验推断与重要性评分

**V′** 随后被送入一个可学习的轻量投影模块 **Q_θ(·)**，该模块由两层 MLP 和两个可学习嵌入（先验均值 **μ_p** 和方差 **σ_p²**）组成。其作用是将每个视觉令牌映射为一个多元高斯后验分布：

$$Q_{\theta}(Z_i \mid V_i') = \mathcal{N}(\mu_{\theta}(V_i'), \sigma_{\theta}^2(V_i'))$$

其中后验均值通过通道级可学习门控进行约束：

$$\mu_{\theta}(V_i') = \sigma(I_{\theta}(V_i')) \odot (V_i' - \mu_p) + \mu_p$$

该门控使用 sigmoid 函数限制后验均值相对于可学习先验的偏移幅度，从而稳定训练并避免后验坍塌。随后，计算每个视觉令牌后验分布与先验之间的 KL 散度，作为该令牌的**信息量重要性分数**：

$$D_{\mathrm{KL}}(Q_{\theta}(\boldsymbol{Z}_i \mid \boldsymbol{V}_i') \| P(\boldsymbol{z})) = \frac{1}{d} \sum_{j=1}^{d} D_{\mathrm{KL}}(Q_{\theta}(\boldsymbol{Z}_i^{(j)} \mid \boldsymbol{V}_i'^{(j)}) \| P(\boldsymbol{z}^{(j)}))$$

这一分数的本质含义是：令牌后验偏离先验越远，其携带的查询-答案相关信息量越大，越应被保留。与 SGP 仅聚合注意力权重不同，该分数是**软量化的信息度量**，不依赖答案驱动的先验，因此能覆盖更广泛的感知上下文（见图 3 的可视化对比）。

### 模块三：Large VLM（L-VLM）——基于重要性分数的硬剪枝与最终推理

获得所有视觉令牌的重要性分数后，IF-Prune 按分数降序排列并执行 **Top-K% 硬剪枝**：仅保留分数最高的 K% 令牌及其对应的预计算位置嵌入，其余令牌被直接丢弃。剪枝操作在大型 VLM 解码器的第 L 层执行——视觉令牌在进入该层的交叉注意力之前被精简。之后，大型 VLM 在精简后的令牌集上完成剩余的前向传播并生成最终答案。

### 输入输出流总结

| 阶段 | 输入 | 处理 | 输出 |
|------|------|------|------|
| 小模型感知 | 文本查询 X + 原始视觉令牌 V | 小模型 π_φ 一次预填充前向 | 查询感知视觉嵌入 V′ |
| 信息瓶颈评分 | V′ | 投影模块 Q_θ 推断后验分布并计算 KL 散度 | 每个视觉令牌的重要性分数 |
| 大模型剪枝推理 | 原始 V + 重要性分数 | Top-K% 硬剪枝后送入大模型 | 最终答案 Y |

### 训练流程

训练阶段，小模型 **π_φ** 被调用两次（见图 2）：
1. **第一次前向**：输入 X 和 V，输出 V′ 经 Q_θ 映射为后验分布，计算 KL 散度；
2. **第二次前向**：通过重参数化技巧从后验分布采样隐变量 Z，输入 X 和 Z，计算预测答案与真实答案 Y 之间的交叉熵损失。

完整训练目标为：

$$\mathcal{L} = \mathbb{E}_{X,Y \sim \mathcal{D}, Z} [\log \pi_{\phi}(Y \mid X, Z)] - \frac{\beta}{m} \sum_{i=1}^{m} D_{\mathrm{KL}}(Q_{\theta}(Z_i \mid V_i') \| P(z))$$

其中第一项为重建损失（交叉熵），第二项为令牌级 KL 惩罚项，β 采用线性预热调度以稳定训练。消融实验表明，完整的训练目标（重建损失 + KL 惩罚 + sigmoid 门控）是实现有效剪枝的基础，移除 KL 项或使用指数门控均导致性能下降。

### 关键设计优势

与基线方法的根本差异在于：**SGP** 需要小模型自回归生成至结束令牌，聚合所有生成令牌的注意力权重作为重要性分数，其答案驱动的机制在面对复杂视觉推理时产生大量噪声（图 1a）；**FastV** 仅使用第一个生成令牌的交叉注意力进行逐步剪枝，信息源更为有限。IF-Prune 则通过**单次前向传播**即可产生全部令牌的重要性分数，预填充延迟仅为 238.5 ms（SGP 为 524.5 ms），且分数基于信息论原理而非启发式注意力聚合，在仅保留 5% 视觉令牌时仍能保持原模型 95.4% 的性能，超越 SGP 6.5 个百分点。

### 补充图表

![[assets/figures/papers/paper_list_l758_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_IF_Prune_Informati/figures/001_Figure_1.jpg]]
*Figure 1: (a) SGP utilizes a pre-trained VLM for the importance map prediction, but failed to provide helpful pruning guidance due to its answer-driven mechanism. (b) We fine-tuned an information bottleneck module to map the output visual embeddings from a small-VLM to a latent variable, which are used to compute the importance of each visual token given the provided text prompt. The pruning guidance is more helpful than SGP after top-K% pruning for the large-VLM*

## 核心模块与公式推导

### 问题形式化：令牌级变分信息瓶颈

IF-Prune 将视觉令牌重要性估计重新定义为**摊销变分推断问题**。其核心思想是：将每个视觉令牌视为一个随机隐变量，通过信息瓶颈框架自动量化其对下游任务的信息贡献。

给定输入图像令牌 $V = \{v_1, ..., v_m\}$ 和用户查询 $X$，小型 VLM $\pi_\phi$ 首先提取查询感知的视觉特征 $V' = \pi_\phi(X, V)$。随后，一个轻量级投影模块 $Q_\theta$ 将每个令牌特征 $V_i'$ 映射为高斯后验分布：

$$Q_{\theta}(Z_i \mid V_i') = \mathcal{N}(\mu_{\theta}(V_i'), \sigma_{\theta}^2(V_i'))$$

其中 $\mu_{\theta}(V_i')$ 和 $\sigma_{\theta}^2(V_i')$ 分别表示第 $i$ 个令牌的后验均值和方差。每个令牌相对于可学习先验 $P(z) = \mathcal{N}(\mu_p, \sigma_p^2)$ 的信息量，通过**通道平均 KL 散度**量化：

$$D_{\mathrm{KL}}(Q_{\theta}(\boldsymbol{Z}_i \mid \boldsymbol{V}_i') \| P(\boldsymbol{z})) = \frac{1}{d} \sum_{j=1}^{d} D_{\mathrm{KL}}(Q_{\theta}(\boldsymbol{Z}_i^{(j)} \mid \boldsymbol{V}_i'^{(j)}) \| P(\boldsymbol{z}^{(j)}))$$

该散度值即为每个视觉令牌的**重要性分数**：KL 散度越大，令牌包含的查询-答案相关信息越多，应被优先保留。

### 通道级门控后验均值

为防止后验均值在训练初期过度偏离先验导致不稳定，IF-Prune 引入了**通道级可学习门控机制**：

$$\mu_{\theta}(V_i') = \sigma(I_{\theta}(V_i')) \odot (V_i' - \mu_p) + \mu_p$$

其中 $I_{\theta}(\cdot)$ 为 MLP 投影输出，$\sigma(\cdot)$ 为 sigmoid 门控函数，$\mu_p$ 为可学习先验均值。该设计将后验均值的偏移量限制在 $[0, 1]$ 范围内，确保训练稳定性。消融实验证实，sigmoid 门控在整体得分上优于指数门控 0.97 个百分点（90.80% vs. 89.83%）。

### 训练目标与重参数化

训练目标由两部分组成——**重建损失**与**令牌级 KL 惩罚**：

$$\mathcal{L} = \mathbb{E}_{X,Y \sim \mathcal{D}, Z} [\log \pi_{\phi}(Y \mid X, Z)] - \frac{\beta}{m} \sum_{i=1}^{m} D_{\mathrm{KL}}(Q_{\theta}(Z_i \mid V_i') \| P(z))$$

其中第一项为交叉熵重建损失，确保剪枝后的隐变量 $Z$ 仍能支撑正确答案生成；第二项为信息瓶颈正则项，鼓励模型自动压缩冗余令牌。

为使梯度可反向传播，采用**重参数化技巧**从后验分布中采样隐变量：

$$Z_i = \mu_{\theta}(V_i') + \sigma_{\theta}(V_i') \cdot \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

### 自适应 KL 权重调度

KL 惩罚系数 $\beta$ 采用**线性预热调度**，在训练初期逐步增大惩罚力度：

$$\beta(s) = \tau_{max} - (\tau_{max} - \tau_{min}) \cdot \min(1, s / \gamma)$$

其中 $s$ 为当前训练步数，$\gamma$ 为预热步数。消融实验表明，采用线性调度 $T(0.2, 0.5)$ 的自适应 KL 权重比固定 $\beta=0.5$ 的整体得分高出 1.36%（91.19% vs. 89.83%），有效避免了后验坍塌。

### 模块架构

投影模块 $Q_\theta$ 由两层 MLP 和两个可学习嵌入（先验均值 $\mu_p$ 和方差 $\sigma_p^2$）组成。小型 VLM 初始化为预训练的 **InternVL2.5-1B**，并使用 LoRA 微调一个 epoch 以缓解领域偏移。训练流程如图 2 所示：小模型执行两次前向传播——第一次计算 KL 散度作为重要性分数，第二次利用采样隐变量计算重建损失。

### 补充图表

![[assets/figures/papers/paper_list_l758_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_IF_Prune_Informati/figures/004_Figure_3.jpg]]
*Figure 3: Visualization of visual token importance map proposed by SGP and IF-Prune (ours)*

## 实验与分析

### 核心性能对比

在 InternVL2-26B 上，IF-Prune 以极低的令牌保留率实现了与原模型高度一致的性能。当仅保留 5% 视觉令牌（K=5%）时，IF-Prune 在 8 个基准上的平均得分比率达到 **95.41%**，而 **SGP**（Zhao et al., CVPR 2025）和 **FastV**（Chen et al., ECCV 2024）分别降至 88.91% 和 67.1%（Table 1）。在更宽松的 20% 保留率下，IF-Prune 几乎无损地保持了 99.4% 的原始性能。这一结果表明，后验引导的剪枝信号比答案驱动的启发式方法更有效地保留了大型 VLM 推理所需的关键视觉上下文。

![[assets/figures/papers/paper_list_l758_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_IF_Prune_Informati/figures/005_Table_1.jpg]]
*Table 1: Comparison of InternVL2-26B with different visual token pruning methods. After obtaining the importance map using different methods, including FastV, SGP, and IF-Prune, we retain the top-K% (i.e., token ratio) of all input visual tokens and execute hard pruning at the*

### 迁移泛化能力

IF-Prune 展现出显著的跨模型迁移能力：一个在 InternVL2.5-1B 上训练的信息瓶颈模块，无需任何额外微调即可直接为 InternVL2-8B 提供剪枝指引。在 K=5% 的设置下，IF-Prune 在 InternVL2-8B 上达到 **94.03%** 的得分比率，较 SGP 的 90.34% 提升 3.69 个百分点（Table 2）。这验证了论文的核心主张——摊销变分推断学到的令牌重要性分布对同架构模型具有通用性。

![[assets/figures/papers/paper_list_l758_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_IF_Prune_Informati/figures/006_Table_2.jpg]]
*Table 2: Performance comparison of InternVL2-8B with different pruning methods including SGP and IF-Prune*

### 效率与延迟分析

IF-Prune 在计算效率上同样具有优势。在 K=5%、L=2 的配置下，总 FLOPs 降至无剪枝基线的 **62.9%**，即减少约 37% 的计算量，同时保持 95.41% 的性能（Table 3）。延迟方面，IF-Prune 仅需小模型一次预填充前向传播即可生成全部剪枝指引，预填充延迟为 **238.5 ms**，而 SGP 因需要自回归生成至结束令牌，延迟高达 524.5 ms，IF-Prune 在此项上降低约 55%（Table 4）。吞吐量也从 SGP 的 16.4 token/s 提升至 19.5 token/s。

![[assets/figures/papers/paper_list_l758_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_IF_Prune_Informati/figures/007_Table_3.jpg]]
*Table 3: Performance and FLOPs of different pruning methods. We prune 100 − K(%) of visual tokens at*

### 消融实验与关键设计选择

#### KL 惩罚权重调度

固定 KL 权重 β=0.5 时整体得分为 89.83%，而采用线性预热调度 T(0.2, 0.5) 可将得分提升至 **91.19%**（+1.36%）。这表明训练初期逐步增大 KL 惩罚有助于稳定后验学习，避免后验坍塌。调度公式为：

$$\beta(s) = \tau_{max} - (\tau_{max} - \tau_{min}) * \min(1, s / \gamma)$$

其中 s 为训练步数，γ 为预热步数。

#### 门控激活函数

后验均值的通道级门控采用 sigmoid 激活时整体得分为 **90.80%**，优于指数门控的 89.83%（+0.97%）。sigmoid 门控通过限制后验均值相对先验的偏移量，提供了更稳定的训练动态：

$$\mu_{\theta}(V_i') = \sigma(I_{\theta}(V_i')) \odot (V_i' - \mu_p) + \mu_p$$

#### 训练目标完整性

完整的训练目标由重建损失（交叉熵）和令牌级 KL 惩罚组成。消融显示，移除 KL 惩罚项或使用不合适的门控机制均导致性能显著下降，验证了信息瓶颈框架中压缩项与预测项平衡的必要性（Table 5）。

![[assets/figures/papers/paper_list_l758_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_IF_Prune_Informati/figures/009_Table_5.jpg]]
*Table 5: Ablation study of major components in our proposed objective function for training the information bottleneck. We report the results of InternVL2-26B after pruning guided by our small-VLM using IF-Prune with*

### 可视化分析

Figure 4 的性能-效率曲线表明，IF-Prune 在逐步提高剪枝比例时展现出更强的稳定性，精度衰减远小于 SGP 和 FastV。Figure 3 的重要性图可视化进一步揭示了性能差异的根源：SGP 生成的令牌重要性图过度聚焦于答案直接相关的少数令牌，而 IF-Prune 的后验引导分布覆盖了更广泛的感知上下文，为大型 VLM 保留了充分的视觉理解线索。

![[assets/figures/papers/paper_list_l758_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_IF_Prune_Informati/figures/003_Figure_4.jpg]]
*Figure 4: Performance–efficiency curve. IF-Prune demonstrates greater stability under progressively higher token pruning ratios, preserving accuracy more effectively*

### 失败模式与局限性

尽管 IF-Prune 在单图像任务上表现优异，其适用边界仍需注意。首先，方法要求小模型与大模型共享相同的视觉编码架构（如 InternVL 系列），对异构 VLM 的泛化性未经验证。其次，当前工作仅针对单图像场景设计，在视频、多模态序列或交互式对话场景下的有效性尚未探讨。此外，信息瓶颈模块的训练仍需一定量的微调数据和计算资源，剪枝超参数（K、L）可能需要根据具体下游任务进行调整。

### 补充图表

![[assets/figures/papers/paper_list_l758_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_IF_Prune_Informati/figures/008_Figure_5.jpg]]
*Figure 5: Comparison of the same large-VLM (L-VLM) with different pruning methods. For each visual input, we highlight the top-5% of all the visual tokens based on the importance map predicted by SGP and IF-Prune. Upper three: SGP provides answer-driven pruning guidance, impacting the large-VLM’s performance. Lower three: IF-Prune provides posterior-driven guidance, where the retained visual tokens are high query and answer relevance, allowing the L-VLM to perform sufficient visual understanding before answering*

## 方法谱系与知识库定位

### 1. 问题定位：从“答案驱动”到“信息驱动”的范式转换

现有视觉令牌剪枝方法的核心瓶颈在于其**重要性评估机制过度依赖答案驱动的先验知识**。以 **SGP**（Zhao et al., CVPR 2025）为代表的方法，通过聚合小模型自回归生成过程中所有输出令牌对视觉令牌的注意力权重来构建重要性图。这一机制的根本缺陷在于：小模型自身的推理能力有限，当面对需要复杂视觉推理的查询时，其生成的注意力图包含大量噪声，且天然倾向于仅关注与最终答案直接相关的少数令牌，而忽略了对大模型推理至关重要的上下文线索。类似地，**FastV**（Chen et al., ECCV 2024）仅使用解码器第二层中第一个生成令牌的交叉注意力权重进行逐步剪枝，其信息来源更为单一，在激进剪枝下性能退化尤为严重。**ToME**（Bolya et al., ICLR 2023）则绕过重要性评估，直接在视觉编码器内部基于令牌相似性进行合并，但该方法缺乏对下游查询内容的感知，无法区分任务相关与无关的视觉冗余。

IF-Prune 实现了根本性的范式转换：**不再要求小模型“判断”哪些令牌重要，而是训练小模型学习输出每个视觉令牌的后验分布，以信息瓶颈框架自动量化令牌的信息量**。这一转换将剪枝信号从“答案相关”拓展为“信息相关”，使保留的令牌集合能够覆盖更广泛的感知上下文，从而为大型 VLM 保留完整的视觉推理能力。

### 2. 方法谱系中的定位

IF-Prune 处于**摊销变分推断**与**视觉令牌剪枝**的交叉点。其方法论基础可追溯至变分信息瓶颈（Variational Information Bottleneck, VIB）框架，但 IF-Prune 首次将 VIB 扩展至**令牌级粒度**，并应用于跨模型剪枝场景。

在具体技术路径上，IF-Prune 与现有方法的差异体现在三个关键维度：

| 维度 | SGP (CVPR 2025) | FastV (ECCV 2024) | IF-Prune (本工作) |
|------|-----------------|-------------------|-------------------|
| **重要性信号来源** | 自回归生成过程的聚合注意力 | 首个生成令牌的单层交叉注意力 | 令牌级后验分布与先验的 KL 散度 |
| **推理开销** | 需小模型完整自回归生成 | 逐层逐步剪枝 | 仅一次小模型预填充前向传播 |
| **剪枝信号感知范围** | 答案驱动，偏向答案相关令牌 | 答案驱动，信息高度局部化 | 后验驱动，同时感知查询和答案内容 |

在架构设计层面，IF-Prune 引入的**通道级可学习门控机制**（sigmoid 门控约束后验均值偏离先验的幅度）是区别于标准 VIB 的重要创新。消融实验表明，sigmoid 门控在整体得分上优于指数门控 0.97 个百分点，验证了有界偏移设计对训练稳定性的关键作用。

### 3. 适用边界与迁移能力

IF-Prune 的适用边界受以下条件约束：

- **架构同构性要求**：当前方法要求小模型与大模型共享相同的视觉编码架构（如均属于 InternVL2 系列），因为剪枝指引的迁移依赖于视觉令牌表示空间的语义对齐。对于异构 VLM（如小模型使用 ViT-L，大模型使用 ViT-H 的不同变体），该方法的有效性未经实验验证。

- **单图像任务限定**：现有训练与评估均围绕单图像理解任务展开，其在视频理解、多模态序列或交互式对话场景下的适用性尚未探讨。

在迁移能力方面，实验提供了有力的正面证据：一个基于 InternVL2.5-1B 训练的剪枝模块，可直接为 InternVL2-8B 乃至 InternVL2-26B 提供有效的剪枝指引。在 5% 令牌保留率下，迁移至 8B 模型仍保持 94.03% 的性能，超越 SGP 3.69 个百分点。这表明**信息瓶颈模块学习到的“信息性”概念具有一定的模型规模不变性**，为一次训练、多模型部署提供了实践基础。

### 4. 局限与开放问题

**已知局限**：

1. **异构架构泛化未验证**：当小模型与大模型采用不同的视觉编码器架构时，令牌表示空间的语义对齐可能失效，剪枝指引的有效性需要进一步研究。
2. **超参数敏感性**：剪枝策略的关键超参数（保留率 K、剪枝层 L、KL 惩罚权重调度参数 τ_min/τ_max/γ）可能需要根据具体下游任务进行调整，缺乏自适应的自动化配置机制。
3. **训练代价**：尽管推理效率显著提升，信息瓶颈模块的训练仍需一定量的微调数据和计算资源（基于 InternVL2.5-1B 进行一轮 LoRA 微调）。

**开放问题**：

1. **跨模态信息瓶颈**：如何将令牌级变分信息瓶颈推广至多模态上下文（如同时处理文本、图像、音频令牌），实现跨模态的冗余消除与信息互补？这需要设计能够感知模态间交互的联合先验分布。
2. **时序一致性约束**：在链式推理和多轮对话场景中，不同轮次的剪枝决策可能存在上下文一致性问题。是否需要对信息瓶颈施加时间维度的约束（如时序 KL 正则化）以保持跨轮次的视觉上下文连贯性？
3. **端到端联合优化**：当前方法将小模型训练与大模型推理解耦。能否通过联合训练小模型的剪枝策略与大模型的推理过程，进一步减少微调代价并实现更紧凑的端到端优化？这可能涉及直通估计器（Straight-Through Estimator）等离散剪枝操作的梯度近似技术。
4. **先验分布的自适应学习**：当前先验分布 P(z) 为全局可学习参数，对所有令牌共享。引入上下文感知的先验（如基于查询类型动态调整先验方差）可能进一步提升信息量化的精度。

## 原文 PDF

![[paperPDFs/CVPR_2026/IF_Prune_Information_Flow_Guided_Token_Pruning_for_Efficient_Vision_Language_Models.pdf]]
