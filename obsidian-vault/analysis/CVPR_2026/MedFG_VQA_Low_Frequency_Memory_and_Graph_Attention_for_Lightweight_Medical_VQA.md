---
title: "MedFG-VQA: Low-Frequency Memory and Graph Attention for Lightweight Medical VQA"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MedFG_VQA_Low_Frequency_Memory_and_Graph_Attention_for_Lightweight_Medical_VQA.pdf
project_link: null
code_link: "https://github.com/NUST-Machine-Intelligence-Laboratory/MedFG"
aliases:
- MV
- MedFG-VQA
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 频率域低中层特征增强与图结构感知的多模态融合：通过可学习的频率记忆库注入全局结构先验，并利用KNN图卷积与交叉注意力共同建模跨模态语义和局部空间关系。
primary_logic: DCT低频分量编码图像的全局结构和语义，通过可学习记忆库进行残差融合可增强轻量模型对结构性医学问题的泛化能力；同时，跨模态注意力与动态KNN图卷积的混合设计能够高效对齐文本与细粒度视觉特征。
claims:
- MedFG-VQA在SynMedVQA上以795M参数量取得最高总体得分（0.6441），超过包括Gemma3-4B、Qwen3-VL-4B在内的所有对比大模型。
- 消融实验表明，同时使用FMF和GACA模块将准确率从0.627提升至0.6441，验证了频率记忆和图注意力的协同增益。
- 在公开基准SLAKE上，MedFG-VQA开放域问答准确率达到0.9595，优于基于大规模数据和预训练的其他医学VLM。
- SynMedVQA 上 Average Accuracy (Open + Close) = 0.6441
---

# MedFG-VQA: Low-Frequency Memory and Graph Attention for Lightweight Medical VQA

> [!tip] 核心洞察
> DCT低频分量编码图像的全局结构和语义，通过可学习记忆库进行残差融合可增强轻量模型对结构性医学问题的泛化能力；同时，跨模态注意力与动态KNN图卷积的混合设计能够高效对齐文本与细粒度视觉特征。

| 字段 | 内容 |
|------|------|
| 中文题名 | MedFG-VQA：面向轻量级医学视觉问答的低频记忆与图注意力 |
| 英文题名 | MedFG-VQA: Low-Frequency Memory and Graph Attention for Lightweight Medical VQA |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Gu_MedFG-VQA_Low-Frequency_Memory_and_Graph_Attention_for_Lightweight_Medical_VQA_CVPR_2026_paper.html) · [Code](https://github.com/NUST-Machine-Intelligence-Laboratory/MedFG) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | MedFG-VQA |
| Dataset | SynMedVQA, SLAKE, PathVQA |

> [!tip] 效果简介
> - SynMedVQA 上，Average Accuracy (Open + Close) 0.6441 vs Qwen3-VL (4B) ≈0.549 (+9.5%)。
> - SLAKE (Open-ended) 上，Accuracy 0.9595 vs LLaVA-Med (7B) (约+2.3%)。
> - PathVQA (Closed) 上，Accuracy 0.7865 vs Previous best model (e.g., LLaVA-Med)。

## 概要

医学视觉问答（Medical VQA）面临一个关键瓶颈：标注数据稀缺与大型模型高计算需求之间的矛盾，使得现有方法难以在临床可部署的轻量级配置下保持强诊断能力。针对这一问题，本文提出 **MedFG-VQA**，一种轻量级医学VQA框架，其核心思路是通过频率域的低中层特征增强与图结构感知的多模态融合，在不依赖大规模模型的前提下提升结构性医学问题的回答质量。

方法上的关键创新体现在两个层面。第一，**FMF（频率记忆融合）模块**利用离散余弦变换（DCT）提取图像的低频分量，这些分量编码了医学图像的全局结构和语义信息；随后通过一个可学习的频率记忆库检索全局先验，并以残差加权方式将其注入视觉特征。第二，**GACA（图感知交叉注意力）模块**在跨模态注意力对齐文本与视觉特征之后，基于注意力输出构建动态KNN图，利用图卷积聚合局部空间上下文，最终通过门控机制自适应融合语义表征与结构聚合表征。

在实验验证上，MedFG-VQA以仅795M的参数量，在合成数据集 **SynMedVQA**（205.9万问答对，涵盖9种成像模态、10大器官）上取得0.6441的最高总体得分，超过包括 **Gemma3-4B**、**Qwen3-VL-4B** 在内的所有对比大模型。在公开基准 **SLAKE** 上，开放域问答准确率达到0.9595，优于 **LLaVA-Med（7B）** 等基于大规模预训练的医学VLM。消融实验进一步证实，FMF与GACA模块的协同使用将准确率从0.627提升至0.6441，验证了频率记忆与图注意力联合设计的有效性。

在方法谱系中，MedFG-VQA定位于“轻量级视觉编码器 + 参数高效多模态融合 + 小型语言模型”的技术路线，区别于 **LLaVA-Med**（Li et al., NeurIPS 2023）等依赖7B级语言模型的全量微调方案，也与 **Gemma3**（Gemma Team, arXiv 2025）、**Qwen3-VL**（Yang et al., arXiv 2025）等通用大模型的医学适配路径形成差异。其知识贡献在于揭示了DCT低频分量在医学VQA中的结构先验价值，以及跨模态注意力与动态图卷积混合设计在轻量级配置下的高效对齐能力。

当前工作的主要局限在于：模型仅处理单视图医学图像，尚未涉及多视图、多模态影像的联合推理；SynMedVQA数据集完全由GPT-4o生成，问答质量受底层大模型能力制约，可能存在事实性错误或领域偏见。

医学视觉问答（Medical VQA）旨在根据医学影像和自然语言问题自动生成准确答案，是临床辅助决策与医学教育中的关键技术。近年来，通用视觉语言模型（VLMs）在自然图像理解上取得了显著进展，但其在医学领域的迁移面临一个核心矛盾：**标注数据的稀缺与大型模型高计算需求之间的冲突**。医学影像的标注高度依赖专家知识，获取成本极高，导致可用的训练数据远少于通用领域；与此同时，参数规模达数十亿的大型VLM（如 **Gemma3** (Gemma Team, arXiv 2025) 的4B版本、**Qwen3-VL** (Yang et al., arXiv 2025) 的4B版本、**LLaVA-Med** (Li et al., NeurIPS 2023) 的7B版本）虽然在零样本或少样本场景下展现出一定潜力，但其推理所需的计算资源与存储开销严重制约了在临床边缘设备上的可部署性。

现有轻量级VLM在医学VQA任务上的表现普遍不足，其瓶颈可归结为两个层面：其一，视觉编码器提取的特征缺乏对医学影像全局结构与语义先验的有效建模，导致对需要结构性推理的问题（如器官定位、病变范围判断）泛化能力薄弱；其二，视觉与文本模态的融合多采用标准交叉注意力或直接拼接，未能充分捕获医学影像中细粒度局部区域之间的空间依赖关系，使得模型在回答涉及局部病灶特征的问题时容易出现定位偏差或遗漏。

针对上述缺口，本文提出 **MedFG-VQA**——一个以轻量级大语言模型（**SmolLM2-360M-Instruct**）为核心、总参数量仅约795M的医学VQA框架。其设计动机源于一个关键洞察：**图像的离散余弦变换（DCT）低频分量天然编码了全局结构与语义信息**，通过可学习的频率记忆库（Frequency Memory Bank）对这一分量进行检索与残差融合，能够以极低的计算代价为轻量模型注入结构先验；同时，**跨模态注意力与动态KNN图卷积的混合设计**可以在不显著增加参数的前提下，高效对齐文本语义与视觉局部空间关系，从而弥合轻量模型与大型VLM之间的性能鸿沟。

## 核心方法与创新机理

MedFG-VQA的核心创新围绕一个关键矛盾展开：医学VQA需要强诊断能力，但临床可部署的轻量级配置下，现有方法难以同时保持高性能。论文通过两个**changed slots**——低中层特征增强与多模态特征融合——实现了突破，其因果链条清晰：**频率域全局先验注入**解决了轻量模型对结构性医学问题的泛化瓶颈，而**图结构感知的跨模态融合**则高效对齐了文本与细粒度视觉特征。

### 创新一：频率记忆融合（FMF）——低频全局先验的注入

传统视觉编码器（如SigLIP2-so400m）直接输出特征图，缺乏对医学图像中全局结构和语义的显式建模。FMF模块的洞察在于：**DCT低频分量天然编码图像的全局结构和语义信息**，通过可学习记忆库进行残差融合，可以增强轻量模型对结构性医学问题的泛化能力。

具体机制分为三步：
1. **频域分解**：对视觉编码器输出的特征图进行DCT变换，提取低频分量 $\mathbf{F}_{\mathrm{low}}$。
2. **记忆检索与融合**：从可学习的记忆库 $\mathbf{M}_k$ 中检索全局先验，通过加权残差融合生成增强的低频表示：
   $$\mathbf{F}_{\mathrm{low}}^{\mathrm{fused}} = \lambda \mathbf{F}_{\mathrm{low}} + (1-\lambda) (\mathrm{Softmax}(\mathbf{S}_k) \cdot \mathbf{M}_k)$$
3. **门控精炼**：融合后的低频特征通过IDCT重建回空间域，再与原始输入进行自适应门控融合：
   $$\mathbf{X}_{\mathrm{out}} = \mathbf{X} + \alpha \cdot f_{\theta}([\mathbf{X}, \mathbf{X}_{\mathrm{rec}}])$$

为保证记忆库的表示多样性，引入多样性损失：
$$\mathcal{L}_{\mathrm{div}} = \frac{1}{N(N-1)} \sum_{i \neq j} (\mathbf{m}_i^{\mathsf{T}} \mathbf{m}_j)^2$$

消融实验（Table 5）验证了频域变换策略的选择：**FFT在实验中表现优于DCT**，这一点需要手动核实原文的具体数值对比。

### 创新二：图感知交叉注意力（GACA）——语义与结构的双视角融合

标准交叉注意力仅建模全局跨模态语义，忽略了医学图像中局部视觉块之间的空间连贯性。GACA模块的核心设计是**混合两种视角**：跨模态注意力生成语义表征，动态KNN图卷积聚合局部结构，最终通过门控机制自适应融合。

具体流程：
1. **跨模态注意力**：以文本特征为Query、图像特征为Key/Value，生成语义对齐的视觉表征 $\mathbf{I}_{\mathrm{attn}}$。
2. **动态图构建与卷积**：基于 $\mathbf{I}_{\mathrm{attn}}$ 的特征相似度构建KNN图，邻接矩阵定义为：
   $$A_{ij} = \begin{cases} 1, & \text{if } j \in \mathrm{KNN}(i,k) \\ 0, & \text{otherwise} \end{cases}$$
   随后通过图卷积聚合邻居节点的信息，增强局部上下文连贯性：
   $$\mathbf{I}_{\mathrm{enh}} = \sigma(f_{\theta}(\tilde{\mathbf{A}} \mathbf{I}_{\mathrm{attn}}))$$
3. **门控融合**：用学习到的门控权重 $\mathbf{G}$ 动态平衡两种视角：
   $$\mathbf{I}_{\mathrm{fused}} = \mathbf{G} \odot \mathbf{I}_{\mathrm{enh}} + (1-\mathbf{G}) \odot \mathbf{I}_{\mathrm{attn}}$$

### 协同增益的实证支撑

消融实验（Table 4(a)）给出了最直接的因果证据：同时移除FMF和GACA模块后，准确率从**0.6441降至0.627**；单独使用任一模块均可带来提升，但联合使用的增益最大，验证了两个模块的协同效应。此外，GACA相对于标准交叉注意力的优势也在消融中得到确认（Table 5）。

### 方法定位与谱系

MedFG-VQA在方法谱系上位于“轻量级VLM + 医学领域适配”的交叉点。与**LLaVA-Med**（Li et al., NeurIPS 2023）等通过大规模医学预训练和7B级LLM实现性能提升的路线不同，MedFG-VQA仅使用**795M参数**（视觉编码器约400M + SmolLM2-360M-Instruct），通过频率域先验和图结构融合这两个轻量级模块，在SynMedVQA上超越了包括**Gemma3-4B**（Gemma Team, arXiv 2025）和**Qwen3-VL-4B**（Yang et al., arXiv 2025）在内的所有对比大模型（Table 2, Figure 1），证明了“结构先验注入”可以部分替代“参数规模扩张”的效能。

**需要手动核实**：FFT优于DCT的具体数值差异、以及GACA模块中KNN的k值选择，建议查阅原文Table 5和§3.2的完整描述。

MedFG-VQA 的整体设计遵循“轻量视觉编码 → 频率域特征增强 → 图感知多模态融合 → 小语言模型生成”的流水线架构，如图2所示。该架构的核心目标是：在冻结视觉编码器与轻量大语言模型（LLM）的前提下，通过两个可插拔的轻量级模块——**频率记忆融合（FMF）**与**图感知交叉注意力（GACA）**——弥合视觉底层特征与高层语义推理之间的表达能力差距。

### 流水线模块与数据流

系统由四个核心模块串联构成，数据流自上而下单向传递：

1. **视觉编码器（SigLIP2-so400m）**：接收输入医学图像，提取视觉特征图。视觉编码器在训练期间**参数完全冻结**，不参与梯度更新，以保留预训练视觉知识的完整性并控制计算开销。

2. **FMF（频率记忆融合模块）**：对视觉编码器输出的特征图执行**离散余弦变换（DCT）**，提取低频分量——这些分量编码了图像的全局结构与语义信息。随后，模块从一个**可学习的频率记忆库**中检索与当前低频特征最相似的记忆向量，并通过残差加权融合生成增强的低频表示。最终，增强后的低频特征经逆DCT重建回空间域，以**门控残差**的形式叠加到原始特征上，完成特征精炼。该模块仅作用于视觉特征，不涉及文本模态。

3. **GACA（图感知交叉注意力模块）**：接收FMF增强后的视觉特征与文本查询（问题）嵌入。模块内部执行两条并行的处理路径：
   - **跨模态注意力路径**：以文本为Query、视觉为Key/Value，生成语义对齐的视觉表征 $`\mathbf{I}_{\mathrm{attn}}`$；
   - **KNN图卷积路径**：基于 $`\mathbf{I}_{\mathrm{attn}}`$ 的特征相似度构建动态KNN图，通过图卷积聚合邻居节点的局部空间上下文，输出结构增强的视觉表征 $`\mathbf{I}_{\mathrm{enh}}`$。
   两条路径的输出通过**可学习的门控权重**进行自适应融合，平衡全局语义与局部结构信息。

4. **模态投影（Sub-pixel CNN）与LLM（SmolLM2-360M-Instruct）**：GACA输出的融合视觉令牌经模态投影层降维并映射至LLM的嵌入空间，与文本令牌拼接后送入LLM，自回归生成最终答案。

### 模块间的协同关系

FMF和GACA并非独立工作，而是形成**层级递进的增强链路**。FMF在视觉编码器之后、跨模态交互之前，注入从记忆库中习得的全局结构先验，使后续的跨模态注意力能够在更丰富的视觉表征上进行对齐。GACA则在跨模态对齐的基础上，进一步利用图结构建模视觉块之间的局部空间关系，弥补标准交叉注意力对空间上下文建模不足的缺陷。消融实验（Table 4(a)）证实了这一协同设计：单独使用FMF或GACA均可带来性能提升，但**同时使用两者将准确率从0.627提升至0.6441**，验证了频率记忆与图注意力之间的互补增益。

### 训练策略概要

训练总损失由两部分线性组合构成：
$$`\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{text}} + \lambda \mathcal{L}_{\mathrm{div}}`$$

其中 $`\mathcal{L}_{\mathrm{text}}`$ 为LLM生成答案的标准交叉熵损失，$`\mathcal{L}_{\mathrm{div}}`$ 为记忆多样性损失，通过最小化记忆向量间的非对角相似度来鼓励记忆库中的表示保持多样性。平衡系数 $`\lambda=0.5`$ 时达到最优性能（Table 4(c)）。训练采用分层学习率策略：LLM为5e-5，模态投影为0.003，FMF与GACA模块为0.0015，在SynMedVQA数据集上训练2个epoch。

![[assets/figures/papers/paper_list_l765_https_openaccess_thecvf_com_content_CVPR2026_html_Gu_MedFG_VQA_Low_Frequ/figures/003_Figure_2.jpg]]
*Figure 2: The overall architecture of MedFG-VQA. The model consists of a vision encoder, a FreqMemoryFusion(FMF) module, a Graph-Aware Cross-Attention(GACA) module and a LLM*

MedFG‑VQA 在冻结的视觉编码器与大语言模型之间插入两个轻量级核心模块——**FMF（频率记忆融合）** 与 **GACA（图感知交叉注意力）**，分别解决低频全局先验注入和多模态细粒度对齐问题。整体架构如 Figure 2 所示，视觉令牌依次经过 FMF 增强、GACA 融合后送入 LLM 生成答案。

### FMF：频率记忆融合模块

医学图像的全局结构与语义信息集中于 DCT 低频分量。FMF 模块将视觉编码器输出的特征图进行分块 DCT 变换，提取低频系数 $\mathbf{F}_{\mathrm{low}}$，随后从一个可学习的记忆库中检索与当前低频特征最相关的全局先验，并通过残差加权融合进行增强。

**残差加权融合**（§3.1, Eq.1）：

$$\mathbf{F}_{\mathrm{low}}^{\mathrm{fused}} = \lambda \mathbf{F}_{\mathrm{low}} + (1-\lambda) (\mathrm{Softmax}(\mathbf{S}_k) \cdot \mathbf{M}_k)$$

其中 $\mathbf{S}_k$ 为低频特征与记忆库 $\mathbf{M}$ 中 top‑$k$ 个记忆向量的相似度得分，$\lambda$ 为平衡原始特征与检索先验的融合系数。融合后的低频表示通过逆 DCT 重建回空间域，再经门控残差融合与原始输入 $\mathbf{X}$ 整合：

$$\mathbf{X}_{\mathrm{out}} = \mathbf{X} + \alpha \cdot f_{\theta}([\mathbf{X}, \mathbf{X}_{\mathrm{rec}}])$$

$\alpha$ 为可学习的门控参数，$f_{\theta}$ 为小型卷积网络，$[\cdot,\cdot]$ 表示通道拼接。这一设计使模型能自适应地决定注入多少全局结构先验。

**多样性损失**（§3.1, Eq.3）用于防止记忆库退化：

$$\mathcal{L}_{\mathrm{div}} = \frac{1}{N(N-1)} \sum_{i \neq j} (\mathbf{m}_i^{\mathsf{T}} \mathbf{m}_j)^2$$

该损失惩罚记忆向量间的非对角相似度，鼓励记忆库保持表示多样性。总训练损失为文本生成交叉熵与多样性损失的线性组合：$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{text}} + \lambda \mathcal{L}_{\mathrm{div}}$（§3.3, Eq.7）。

### GACA：图感知交叉注意力模块

GACA 模块同时建模跨模态语义对齐与视觉局部空间结构。输入为文本查询 $\mathbf{Q}$ 和 FMF 增强后的视觉特征 $\mathbf{I}$。

首先通过标准交叉注意力生成语义感知的视觉表示 $\mathbf{I}_{\mathrm{attn}}$。随后基于 $\mathbf{I}_{\mathrm{attn}}$ 构建动态 KNN 图，邻接矩阵定义为（§3.2, Eq.4）：

$$A_{ij} = \begin{cases} 1, & \text{if } j \in \mathrm{KNN}(i,k) \\ 0, & \text{otherwise} \end{cases}$$

即在特征空间中为每个视觉令牌选取 $k$ 个最近邻作为图边。通过图卷积层沿图边聚合邻居信息，得到结构增强的表示（§3.2, Eq.5）：

$$\mathbf{I}_{\mathrm{enh}} = \sigma(f_{\theta}(\tilde{\mathbf{A}} \mathbf{I}_{\mathrm{attn}}))$$

其中 $\tilde{\mathbf{A}}$ 为归一化邻接矩阵，$\sigma$ 为激活函数。最后通过可学习的门控权重 $\mathbf{G}$ 自适应融合两种视角（§3.2, Eq.6）：

$$\mathbf{I}_{\mathrm{fused}} = \mathbf{G} \odot \mathbf{I}_{\mathrm{enh}} + (1-\mathbf{G}) \odot \mathbf{I}_{\mathrm{attn}}$$

$\odot$ 表示逐元素乘法。该门控机制使模型能根据具体样本动态平衡全局语义对齐与局部空间结构聚合。

> **关键设计要点**：FMF 的可学习记忆库与多样性损失共同保证了低频先验的全局性与判别力；GACA 的 KNN 图是动态构建的——每个样本的图结构都基于其自身特征即时计算，无需预定义拓扑，这使得模块能适应不同成像模态和解剖结构的视觉布局。

## 实验与关键发现

### 主实验结果

#### SynMedVQA基准

MedFG-VQA在自建的SynMedVQA数据集上以仅795M的参数量取得了0.6441的平均准确率（开放域与封闭域均值），显著超越所有对比基线。具体而言，该结果比4B级大型视觉语言模型**Qwen3-VL**（Yang et al., arXiv 2025）高出约9.5个百分点，比**Gemma3-4B**（Gemma Team, arXiv 2025）和**LLaVA-Med-7B**（Li et al., NeurIPS 2023）等更大规模模型亦保持明显优势（Table 2, Figure 1）。这一结果表明，面向医学影像的结构化先验注入（低频记忆）与细粒度多模态对齐（图感知交叉注意力）可以有效弥补轻量级模型在参数量上的劣势，在临床可部署的配置下实现强诊断能力。

![[assets/figures/papers/paper_list_l765_https_openaccess_thecvf_com_content_CVPR2026_html_Gu_MedFG_VQA_Low_Frequ/figures/007_Table_2.jpg]]
*Table 2: Comparison of model performance on SynMedVQA. All baseline models use their publicly available pretrained weights*

![[assets/figures/papers/paper_list_l765_https_openaccess_thecvf_com_content_CVPR2026_html_Gu_MedFG_VQA_Low_Frequ/figures/002_Figure_1.jpg]]
*Figure 1: Illustration of VLMs evaluated on the SynMedVQA dataset. Among the 6 VLMs, MedFG-VQA achieves the highest overall score. Qualitative VQA comparison between two models, showcasing the effectiveness of MedFG-VQA*

#### 公开医学VQA基准

在三个公开基准上的迁移评估进一步验证了模型的泛化性（Table 3）。在SLAKE开放域问答上，MedFG-VQA达到0.9595的准确率，优于LLaVA-Med（7B）约2.3个百分点。在PathVQA封闭域任务上取得0.7865的准确率，与当前最佳水平相当。在规模最小的VQA-RAD上，模型同样表现出竞争力。需要注意的是，SLAKE和VQA-RAD上的优势相对有限，部分原因在于这些数据集的规模较小，且模型未在对应领域进行充分微调。

### 消融实验

#### 模块贡献分析

Table 4(a)报告了FMF与GACA模块的消融结果。移除两个模块后，模型退化为仅依赖视觉编码器与LLM的基线配置，准确率从0.6441降至0.627。单独引入FMF或GACA均可带来稳定提升，而联合使用二者产生了协同增益——验证了全局频率先验与局部图结构建模在医学VQA中具有互补性。

![[assets/figures/papers/paper_list_l765_https_openaccess_thecvf_com_content_CVPR2026_html_Gu_MedFG_VQA_Low_Frequ/figures/009_Table_4.jpg]]
*Table 4: Ablation studies of the contribution of FMF and GACA, the effect of the memory bank size in FMF, and the impact of the loss balance coefficient λ*

#### 记忆库规模与损失系数

FMF模块中记忆库大小设为64时，在性能和计算开销之间取得最佳平衡（Table 4(b)）。过小的记忆库（如16或32）限制了全局先验的表达能力，而过大的记忆库（如128）带来的边际收益递减且增加了计算负担。多样性损失平衡系数λ=0.5达到最优准确率0.6441（Table 4(c)），表明适度的多样性约束对防止记忆向量坍塌至关重要。

#### 频域策略与交叉注意力变体

Table 5展示了频域变换策略的对比。FFT在实验中表现优于DCT，但论文未提供该现象的系统性分析，此结论需结合具体实现细节进行人工验证。GACA模块相较于标准交叉注意力的优势得到了实验支持，验证了图卷积聚合局部空间上下文对多模态对齐的有效性。

### 失败模式与局限性

尽管整体性能优异，模型仍存在以下可识别的失败模式：

1. **单视图限制**：当前模型仅处理单张医学影像，无法进行多视图或多模态影像的联合推理。在真实临床场景中（如多序列MRI或PET-CT融合诊断），这一限制会导致模型无法利用跨模态互补信息，可能产生片面或错误的判断。

2. **合成数据质量瓶颈**：SynMedVQA数据集完全由GPT-4o生成。虽然经过了质量控制和人工校验，但问答对的质量仍受底层大模型能力的制约。GPT-4o可能引入事实性错误、领域偏见或不恰当的简化，这些缺陷会通过训练过程传播至MedFG-VQA。目前缺乏对生成质量上限的定量评估方法，最差情况下可能导致模型在特定亚领域（如罕见病或复杂鉴别诊断）出现系统性偏差。

3. **频域方法的选择依据**：消融实验显示FFT优于DCT，但论文未深入解释该现象背后的机制（如相位信息保留、频谱分辨率差异等）。这一结论的泛化性需要更多验证。

![[assets/figures/papers/paper_list_l765_https_openaccess_thecvf_com_content_CVPR2026_html_Gu_MedFG_VQA_Low_Frequ/figures/008_Table_5.jpg]]
*Table 5: Ablation studies on different frequency-domain transformation strategies and module against standard cross-attention*

![[assets/figures/papers/paper_list_l765_https_openaccess_thecvf_com_content_CVPR2026_html_Gu_MedFG_VQA_Low_Frequ/figures/010_Figure_5.jpg]]
*Figure 5: Qualitative results against (a) Gemma3-4B , (b) Qwen3-VL-4B, and (c) LLaVA-Med v1.5. Responses are abridged for brevity*

## 定位与知识库关联

### 1. 在医学VQA领域中的位置

医学视觉问答（Medical VQA）长期面临**标注数据稀缺**与**大型模型高计算需求**之间的矛盾。现有主流方案大致分为两条路线：

- **大型VLM微调路线**：以 **LLaVA-Med** (Li et al., NeurIPS 2023, 7B)、**Gemma3** (Gemma Team, arXiv 2025, 4B)、**Qwen3-VL** (Yang et al., arXiv 2025, 4B)、**MiniCPM-V 4.0** (Yao et al., arXiv 2024, 4B) 和 **InternVL3.5** (Wang et al., arXiv 2025, 1B) 为代表，依赖大规模预训练与领域微调，在多个公开基准上取得领先性能，但推理成本高昂，难以在临床可部署的轻量级配置下保持强诊断能力。
- **轻量级专用模型路线**：以BiomedCoOp等为代表，参数量小但通常缺乏对医学图像全局结构与跨模态语义的精细建模，在复杂结构性问题上泛化不足。

MedFG-VQA（795M参数）处于两条路线的交叉地带：它以轻量级架构（SigLIP2-so400m视觉编码器 + SmolLM2-360M-Instruct语言模型）实现了对4B-7B级大模型的性能超越，证明了**轻量级架构配合领域特化模块设计**可以弥合效率与精度之间的鸿沟。

### 2. 核心技术创新与差异化

MedFG-VQA相对于既有方法的关键差异化体现在两个可插拔模块上：

| 技术槽位 | 基线方案 | MedFG-VQA方案 | 差异本质 |
|---------|---------|-------------|---------|
| 低中层特征增强 | 无（直接使用视觉编码器输出） | **FMF模块**：DCT分解提取低频分量，从可学习记忆库检索全局先验并残差融合 | 将频率域的结构先验显式注入特征流，弥补轻量编码器对全局语义捕获不足的短板 |
| 多模态特征融合 | 标准交叉注意力或直接拼接 | **GACA模块**：跨模态注意力生成语义表征 + 动态KNN图卷积聚合局部结构 + 门控融合 | 同时建模跨模态语义对齐与局部空间关系，避免标准交叉注意力对细粒度结构信息的丢失 |
| 训练数据 | 公开小规模医学VQA数据集（SLAKE、PathVQA等） | **SynMedVQA**：205.9万GPT-4o合成问答对，覆盖9种成像模态、10大器官 | 以大规模合成数据缓解医学VQA标注瓶颈，但引入生成质量依赖问题 |

**FMF模块**的核心机制是通过DCT将视觉特征分解为低频（全局结构）和高频（局部细节）分量，仅对低频分量进行记忆库检索与加权融合（见公式 $\mathbf{F}_{\mathrm{low}}^{\mathrm{fused}} = \lambda \mathbf{F}_{\mathrm{low}} + (1-\lambda) (\mathrm{Softmax}(\mathbf{S}_k) \cdot \mathbf{M}_k)$），再通过可学习门控参数 $\alpha$ 与原始特征残差融合。这一设计与传统的通道注意力或空间注意力形成互补——它操作在频率域，且引入了**可学习的全局结构原型**，而非仅依赖输入特征的自适应重标定。

**GACA模块**的差异化在于将图结构引入多模态融合：在跨模态注意力生成语义表征 $\mathbf{I}_{\mathrm{attn}}$ 后，基于其构建动态KNN图（$A_{ij}=1$ 当 $j \in \mathrm{KNN}(i,k)$），通过图卷积聚合邻居节点的局部上下文，最后以门控权重 $\mathbf{G}$ 自适应融合语义视角与结构视角（$\mathbf{I}_{\mathrm{fused}} = \mathbf{G} \odot \mathbf{I}_{\mathrm{enh}} + (1-\mathbf{G}) \odot \mathbf{I}_{\mathrm{attn}}$）。这比标准交叉注意力多了一条**显式的局部空间建模通路**。

### 3. 适用边界与局限

**适用场景**：
- 单视图医学图像的开放域与封闭域问答
- 覆盖9种成像模态（X光、CT、MRI、病理等）和10大器官类别
- 对推理延迟和显存占用敏感的临床部署场景

**已知局限**（需在后续工作中验证）：
1. **单视图限制**：当前模型仅处理单视图医学图像，尚未涉及多视图或多模态影像数据的联合推理，而真实临床诊断常需跨模态信息整合（如CT+MRI联合判读）。
2. **合成数据质量依赖**：SynMedVQA完全由GPT-4o生成，虽然经过了质量校验流程，但问答质量仍受底层大模型能力制约。GPT-4o生成问答对的质量上限如何定量评估，以及其对下游任务的最差情况影响，目前尚未有系统性分析。可能存在事实性错误或领域偏见未被充分暴露。
3. **频率域策略的泛化性**：消融实验表明FFT在SynMedVQA上略优于DCT（Table 5），说明最优频率变换策略可能随任务和数据分布变化，当前选择DCT的泛化依据需要更多跨数据集的验证。

### 4. 开放问题与后续方向

1. **多视图/多模态扩展**：如何将FMF和GACA模块扩展至多视图输入场景，并实现跨模态的联合推理？这可能需要设计跨视图的频率记忆共享机制或图结构对齐策略。
2. **合成数据质量边界**：GPT-4o生成问答对的事实准确性如何系统评估？是否存在某些亚领域（如罕见病、复杂鉴别诊断）生成质量显著下降？这直接影响SynMedVQA作为训练集的可靠性上限。
3. **记忆库的可解释性**：FMF中的可学习记忆向量是否对应可解释的医学结构原型（如特定器官形态、病变模式）？若能建立这种对应关系，将显著增强模型的临床可信度。
4. **与其他轻量级技术的组合**：FMF和GACA作为可插拔模块，能否与量化、蒸馏、剪枝等其他轻量化技术协同，进一步降低部署门槛？

## 原文 PDF

![[paperPDFs/CVPR_2026/MedFG_VQA_Low_Frequency_Memory_and_Graph_Attention_for_Lightweight_Medical_VQA.pdf]]
