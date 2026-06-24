---
title: "TMR: Text-to-Motion Retrieval Using Contrastive 3D Human Motion Synthesis"
type: paper
paper_level: A
venue: ICCV
year: 2023
pdf_ref: paperPDFs/ICCV_2023/TMR_Text_to_Motion_Retrieval_Using_Contrastive_3D_Human_Motion_Synthesis.pdf
aliases:
- TMR
tags:
- ICCV_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 在TEMOS框架中引入InfoNCE对比损失，联合训练动作生成与检索；同时利用MPNet计算文本相似度，过滤训练批次中的高相似度负样本对。
primary_logic: 保持动作生成分支（解码器）的同时进行对比训练，能有效改善跨模态嵌入空间的结构化程度；过滤语义相似的“错误负样本”可避免对比学习中的错误排斥，从而大幅提升检索性能。
claims:
- 在HumanML3D数据集上，TMR在四种评估协议下均显著优于TEMOS与Guo et al.，例如在全部测试集协议下，text-motion R@1从2.12提升至5.68，median rank从173降至28。
- 联合训练运动生成分支（解码器）与仅使用对比损失相比，显著提升检索性能（R@3从36.87提升到41.93）。
- InfoNCE对比损失比基于margin的损失更有效（R@1 41.93 vs 34.46）。
- 基于文本相似度（阈值0.8）过滤负样本，使检索性能达到最佳（R@3从36.02提升至41.93）。
---

# TMR: Text-to-Motion Retrieval Using Contrastive 3D Human Motion Synthesis

> [!tip] 核心洞察
> 保持动作生成分支（解码器）的同时进行对比训练，能有效改善跨模态嵌入空间的结构化程度；过滤语义相似的“错误负样本”可避免对比学习中的错误排斥，从而大幅提升检索性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | TMR：基于对比式3D人体动作合成的文本-动作检索 |
| 英文题名 | TMR: Text-to-Motion Retrieval Using Contrastive 3D Human Motion Synthesis |
| 会议/期刊 | ICCV 2023 |
| Links | [paper](https://arxiv.org/abs/2305.00976) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | TMR |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，R@1 (text-motion, protocol a) 5.68 vs 2.12 (TEMOS) (+3.56)；R@1 (text-motion, protocol b, with threshold) 11.60 vs 5.21 (TEMOS) (+6.39)。
> - KIT-ML 上，R@1 (text-motion, protocol b, with threshold) 24.58 vs 18.55 (TEMOS) (+6.03)；Median Rank (text-motion, protocol a) 17.00 vs 24.00 (TEMOS) (-7.00)。

## 概述

文本-动作检索任务旨在根据自然语言描述，从动作库中按相似度排序并返回最匹配的3D人体运动序列。该任务面临的核心挑战在于：文本与运动这两种模态之间存在显著的语义鸿沟，且动作描述往往涉及细粒度的时空差异（如“走路”与“跛行”），要求跨模态嵌入空间具备高度的结构化判别能力。

现有方法 **TEMOS** 基于VAE框架实现了文本-动作生成，但其跨模态嵌入空间仅利用正样本对进行训练，缺乏对负样本的有效利用，导致嵌入空间结构不佳，难以在大量候选动作中精准区分语义相近但实际不同的运动。**TMR** 的核心洞察在于：在保持运动生成分支（解码器）的前提下引入对比学习，能够显著改善跨模态嵌入空间的结构化程度；同时，通过过滤训练批次中文本语义高度相似的“错误负样本”，可避免对比损失对语义相近但确属不同实例的样本对施加错误排斥。

基于上述洞察，TMR在 **TEMOS** 框架中引入了对称形式的InfoNCE对比损失，联合训练动作生成与跨模态检索。此外，TMR利用预训练的MPNet计算文本相似度，将相似度高于阈值（0.8）的负样本对从对比损失中剔除。这一负样本过滤策略有效缓解了对比学习中因语义相近而导致的错误排斥问题。

实验结果表明，TMR在HumanML3D和KIT-ML两个基准数据集上均显著优于TEMOS与Guo et al.。以HumanML3D全测试集协议为例，文本-动作检索的R@1从2.12提升至5.68，中位排名从173降至28。消融实验进一步证实：联合训练运动解码器分支、采用InfoNCE对比损失、以及基于文本相似度的负样本过滤，三者对性能提升均具有关键贡献。此外，TMR展现出零样本的“瞬间检索”能力，即使未经过时序定位训练，也能在长序列中定位与文本描述匹配的动作片段。

## 背景与动机

### 文本驱动的3D人体动作理解

将自然语言描述与3D人体动作序列建立精确的跨模态对应关系，是计算机视觉与图形学领域的核心挑战之一。文本到动作检索（Text-to-Motion Retrieval）任务要求模型在给定自然语言查询时，从大规模动作库中按语义相似度对候选动作进行排序（Figure 1）。与传统的动作识别或分类任务不同，文本-动作检索面临两大固有困难：其一，动作描述具有高度细粒度性——例如“向前走三步然后挥右手”与“向前走两步然后挥左手”在语义上仅存在细微差异，却对应截然不同的动作序列；其二，自然语言与3D运动序列之间存在巨大的模态鸿沟，前者是离散的符号序列，后者是连续的高维时空数据。

### 现有方法的瓶颈：缺乏结构化嵌入空间

在TMR提出之前，文本-动作跨模态学习主要沿着两条技术路线展开。一条路线以**TEMOS**为代表，其基于变分自编码器（VAE）框架，通过运动编码器、文本编码器和运动解码器的联合训练实现文本到动作的生成。TEMOS的核心损失函数由三部分组成：运动重构损失 $\mathcal{L}_{\mathrm{R}}$、KL散度正则项 $\mathcal{L}_{\mathrm{KL}}$ 以及跨模态嵌入相似度损失 $\mathcal{L}_{\mathrm{E}}$，即：

$$\mathcal{L}_{\mathrm{TEMOS}} = \mathcal{L}_{\mathrm{R}} + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}} + \lambda_{\mathrm{E}} \mathcal{L}_{\mathrm{E}}$$

然而，TEMOS的嵌入相似度损失仅利用正样本对（匹配的文本-动作对）进行训练，完全忽略了负样本的作用。这导致其跨模态嵌入空间缺乏有效的结构化约束：正样本对虽然被拉近，但负样本对之间的边界并未被明确推开，使得嵌入空间中不同语义的动作簇之间界限模糊，难以区分细粒度的动作描述。

另一条路线以**Guo et al.** 的工作为代表，其首次将文本-动作检索作为独立任务提出，并采用基于margin的对比损失进行训练。虽然该方法引入了负样本的概念，但其使用的欧氏距离margin损失在表达能力上存在局限，且该工作本身是为评估动作生成质量而设计，并非专门优化检索性能。

### 核心动机：生成与检索的联合结构化学习

TMR的核心洞察在于：**保持动作生成能力的同时进行对比训练，可以有效改善跨模态嵌入空间的结构化程度**。具体而言，作者识别出两个关键改进方向：

1. **引入InfoNCE对比损失**：将TEMOS的仅正样本嵌入损失替换为对称形式的InfoNCE对比损失，充分利用批次内的负样本对嵌入空间施加全局结构化约束。InfoNCE损失通过温度参数 $\tau$ 控制分布的锐度，其对称形式为：

$$\mathcal{L}_{\mathrm{NCE}} = -\frac{1}{2N} \sum_i \left( \log \frac{\exp S_{ii}/\tau}{\sum_j \exp S_{ij}/\tau} + \log \frac{\exp S_{ii}/\tau}{\sum_j \exp S_{ji}/\tau} \right)$$

其中 $S_{ij}$ 为第 $i$ 个文本嵌入与第 $j$ 个运动嵌入之间的余弦相似度，对角线元素对应正样本对，非对角线元素对应负样本对。

2. **过滤“错误负样本”**：在标准对比学习中，批次内所有非配对样本均被视为负样本。然而，在文本-动作检索场景中，两个不同的动作可能拥有语义高度相似的文本描述（例如“一个人慢慢走路”与“一个人缓慢步行”），将它们作为互斥的负样本会向模型传递矛盾的训练信号。TMR提出使用预训练的MPNet模型计算训练批次内文本对之间的语义相似度，并将相似度高于阈值（0.8）的负样本对从InfoNCE损失的计算中排除（Figure 2），从而避免对比学习中的错误排斥。

通过上述两个改进，TMR在保留TEMOS运动解码器（生成分支）的前提下，实现了生成能力与检索能力的协同提升——解码器提供的重构损失迫使文本嵌入保留足够的运动细节信息，而对比损失则确保嵌入空间具有良好的全局可分性。

## 核心创新

TMR 的核心创新在于将文本-动作检索任务重新定位为**跨模态嵌入空间的结构化学习问题**，而非单纯的动作生成或简单的跨模态匹配。其关键洞察是：现有文本-动作生成模型（TEMOS）仅利用正样本对训练嵌入空间，缺乏对负样本的有效利用，导致嵌入空间结构不佳，难以区分细粒度的动作描述。TMR 通过三个关键改造解决了这一瓶颈。

### 1. 引入 InfoNCE 对比损失

TMR 在 TEMOS 的损失函数基础上，显式引入了对称形式的 InfoNCE 对比损失：

$$\mathcal{L}_{\mathrm{NCE}} = -\frac{1}{2N} \sum_i \left( \log \frac{\exp S_{ii}/\tau}{\sum_j \exp S_{ij}/\tau} + \log \frac{\exp S_{ii}/\tau}{\sum_j \exp S_{ji}/\tau} \right)$$

其中 $S$ 为批次内文本与运动嵌入的余弦相似度矩阵，$\tau$ 为温度参数。该损失同时最大化正样本对的相似度（对角线元素 $S_{ii}$）并最小化负样本对的相似度（非对角线元素），从而强制跨模态嵌入空间形成更结构化的分布。

消融实验（Table 3）验证了这一选择的决定性作用：InfoNCE 对比损失相比 Guo et al. 使用的基于 margin 的对比损失，将 text-motion R@1 从 34.46 提升至 41.93，表明 InfoNCE 对细粒度动作检索的适配性显著优于传统 margin-based 方法。

### 2. 联合保留运动生成分支

TMR 并未简单地抛弃 TEMOS 的运动解码器，而是**保持运动生成与对比检索的联合训练**。总损失函数为：

$$\mathcal{L}_{\mathrm{TMR}} = \mathcal{L}_{\mathrm{TEMOS}} + \lambda_{\mathrm{NCE}} \mathcal{L}_{\mathrm{NCE}}$$

其中 $\mathcal{L}_{\mathrm{TEMOS}} = \mathcal{L}_{\mathrm{R}} + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}} + \lambda_{\mathrm{E}} \mathcal{L}_{\mathrm{E}}$ 包含运动重构损失、KL 散度正则项和跨模态嵌入相似度损失。

这一设计的关键因果机制在于：运动解码器分支迫使文本嵌入保留足够的运动重建信息，防止对比训练过度压缩文本表示而丢失细粒度语义。消融实验（Table 3）证实，移除运动重建损失后，text-motion R@3 从 41.93 降至 36.87，降幅达 5.06 个百分点，充分说明生成任务对检索性能的正则化与信息保持作用。

### 3. 基于文本相似度的负样本过滤

TMR 识别出对比学习中的一个关键隐患：**批次内的高相似度文本对可能构成“错误负样本”**。例如，“一个人走路”和“一个人缓慢步行”在语义上高度相近，但传统对比损失会将其对应的运动嵌入强制推开，从而损害嵌入空间的结构合理性。

为解决此问题，TMR 引入预训练 MPNet 计算训练批次内所有文本对的相似度，并将相似度高于阈值（0.8）的负样本对从 InfoNCE 损失计算中排除。Table 4 的消融实验表明，这一过滤策略将 text-motion R@3 从 36.02（无过滤）提升至 41.93（阈值 0.8），验证了过滤“错误负样本”对对比学习效果的显著增益。

### 创新总结

TMR 的三个改造形成了协同效应：InfoNCE 损失提供结构化对比信号，运动解码器分支保留文本信息的完整性，负样本过滤消除对比学习中的语义冲突。这一组合使 TMR 在 HumanML3D 数据集上，text-motion R@1 从 TEMOS 的 2.12 提升至 5.68，median rank 从 173 降至 28（Table 1），实现了跨模态检索性能的跨越式提升。

## 整体框架

TMR 在 **TEMOS**（基于 Transformer 的文本-动作生成模型）的基础上引入对比学习范式，构建了一个**联合动作检索与合成**的统一框架。其核心设计思路是：在保留 TEMOS 原有动作生成能力（解码器分支）的同时，通过对比损失显式优化跨模态嵌入空间的结构化程度，使模型既能高质量地合成动作，又能精准地从大规模库中检索匹配动作。

### 框架组成与数据流

TMR 的 pipeline 由以下关键模块串联构成：

1. **双编码器（Motion Encoder & Text Encoder）**  
   运动编码器和文本编码器均采用 Transformer 编码器架构，并额外附加可学习的分布参数头。运动编码器将运动序列映射为高斯分布的均值 $\mu^M$ 和方差 $\Sigma^M$；文本编码器以冻结的 DistilBERT 提取的文本特征为输入，输出对应的高斯分布参数 $\mu^T$ 和 $\Sigma^T$。在检索阶段，直接使用均值嵌入作为跨模态表示，避免采样的随机性干扰排序。

2. **对比相似度矩阵（Contrastive Similarity Matrix）**  
   在一个训练批次内，计算所有文本嵌入与运动嵌入之间的余弦相似度矩阵 $S$，其中对角线元素 $S_{ii}$ 对应正样本对，非对角线元素 $S_{ij}$（$i \neq j$）为负样本对。该矩阵是 InfoNCE 对比损失的核心输入。

3. **负样本过滤（Negative Filtering）**  
   为避免语义高度相似的“错误负样本”被对比损失错误排斥，模块利用预训练的 MPNet 计算批次内所有文本对的语义相似度。当两个文本的相似度超过阈值（0.8）时，其对应的负样本对将从损失计算中剔除。这一过滤机制直接作用于相似度矩阵，仅保留语义差异足够大的负样本参与对比学习。

4. **运动解码器（Motion Decoder）**  
   继承自 TEMOS 的解码器分支，从潜在向量 $z$（可从文本嵌入或运动嵌入采样得到）重建完整的运动序列，支持变长生成。该分支的存在确保了文本信息在嵌入空间中被完整保留，而非被对比目标过度压缩。

### 训练目标

TMR 的总损失函数为 TEMOS 原有损失与 InfoNCE 对比损失的加权组合：

$$\mathcal{L}_{\text{TMR}} = \mathcal{L}_{\text{TEMOS}} + \lambda_{\text{NCE}} \mathcal{L}_{\text{NCE}}$$

其中 $\mathcal{L}_{\text{TEMOS}} = \mathcal{L}_{\text{R}} + \lambda_{\text{KL}} \mathcal{L}_{\text{KL}} + \lambda_{\text{E}} \mathcal{L}_{\text{E}}$，包含运动重构损失、KL 散度正则项和跨模态嵌入相似度损失。InfoNCE 对比损失采用对称形式：

$$\mathcal{L}_{\mathrm{NCE}} = -\frac{1}{2N} \sum_i \left( \log \frac{\exp S_{ii}/\tau}{\sum_j \exp S_{ij}/\tau} + \log \frac{\exp S_{ii}/\tau}{\sum_j \exp S_{ji}/\tau} \right)$$

该损失最大化正样本对的余弦相似度，同时最小化（经负样本过滤后的）负样本对相似度，温度 $\tau$ 控制分布的锐度。消融实验表明，$\lambda_{\text{NCE}}=0.1$、$\tau=0.1$ 的设置达到最优（Table 5）。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2305_00976/figures/007_Table_5.jpg]]
*Table 5: Hyperparameters of the contrastive training: We measure the sensitivity to the parameters τ (temperature), λc the weight of the contrastive loss, and the batch size. Note that the learning rate is proportionally altered when changing the batch size. We display a wide range of values to show the full trends*

### 关键设计决策

与基线方法相比，TMR 在三个关键维度上做出了差异化设计：

| 设计维度 | TEMOS | Guo et al. | TMR |
|---------|-------|-----------|-----|
| 对比损失 | 仅正样本嵌入相似度 | Margin 对比损失 | InfoNCE 对比损失 |
| 负样本处理 | 无对比机制 | 批次内所有非配对样本 | MPNet 过滤高相似度负样本 |
| 训练任务 | 纯生成 | 纯检索 | 联合生成与检索 |

消融实验（Table 3）验证了这些设计的必要性：InfoNCE 损失相比 margin 损失将 text-motion R@1 从 34.46 提升至 41.93；保留运动解码器分支进一步将 R@3 从 36.87 提升至 41.93。负样本过滤的阈值消融（Table 4）表明，0.8 的阈值在不过度丢弃负样本的前提下有效规避了错误排斥，使 R@3 从不过滤时的 36.02 跃升至 41.93。

## 核心模块与公式推导

TMR 在 **TEMOS** 的 VAE 框架之上引入对比学习机制，形成“生成-检索联合训练”架构。其核心模块与损失函数如下。

### 跨模态编码器

模型包含两个独立的 Transformer 编码器，分别处理运动序列与文本描述：

- **运动编码器（Motion Encoder）**：将运动序列编码为高斯分布参数 $(\mu^M, \Sigma^M)$。检索时直接使用均值嵌入 $\mu^M$ 作为运动的跨模态表征。
- **文本编码器（Text Encoder）**：基于冻结的 **DistilBERT** 提取文本特征，随后编码为高斯分布 $(\mu^T, \Sigma^T)$。检索时同样使用均值嵌入 $\mu^T$。

两个编码器输出的嵌入向量位于同一潜在空间，为后续的余弦相似度计算奠定基础。

### 运动解码器

运动解码器从潜在向量 $z$ 重建运动序列，支持变长生成。在检索任务中，解码器分支并非必需，但其引入的重建损失对维持文本信息的完整性至关重要——消融实验表明，移除解码器会导致检索性能显著下降。

### 对比相似度矩阵与 InfoNCE 损失

给定一个批次内 $N$ 对文本-运动样本，首先计算所有文本嵌入与运动嵌入之间的余弦相似度矩阵 $S \in \mathbb{R}^{N \times N}$，其中 $S_{ij}$ 表示第 $i$ 个文本与第 $j$ 个运动的相似度。在此基础上，引入对称形式的 **InfoNCE 对比损失**：

$$\mathcal{L}_{\mathrm{NCE}} = -\frac{1}{2N} \sum_i \left( \log \frac{\exp S_{ii}/\tau}{\sum_j \exp S_{ij}/\tau} + \log \frac{\exp S_{ii}/\tau}{\sum_j \exp S_{ji}/\tau} \right)$$

其中：
- $S_{ii}$：正样本对（配对文本-运动）的余弦相似度；
- $S_{ij}$（$i \neq j$）：负样本对的相似度；
- $\tau$：温度系数，控制相似度分布的锐度（实验确定最优值为 $\tau=0.1$）；
- 第一项为文本到运动的对比，第二项为运动到文本的对比，构成对称优化目标。

### 负样本过滤模块

批次内随机采样可能引入“错误负样本”——即文本语义高度相似但并非同一对的动作-文本对。为避免对比损失错误排斥这些样本，TMR 引入基于文本相似度的过滤机制：

- 使用预训练的 **MPNet** 计算训练批次内所有文本对的语义相似度；
- 对于相似度超过阈值 $\theta$ 的文本对，其对应的负样本对从 InfoNCE 损失计算中剔除；
- 消融实验表明，$\theta=0.8$ 时检索性能达到最优。

### 总损失函数

TMR 的总损失为 TEMOS 原始损失与 InfoNCE 对比损失的加权组合：

$$\mathcal{L}_{\mathrm{TMR}} = \mathcal{L}_{\mathrm{TEMOS}} + \lambda_{\mathrm{NCE}} \mathcal{L}_{\mathrm{NCE}}$$

其中 $\mathcal{L}_{\mathrm{TEMOS}}$ 本身由三项加权构成：

$$\mathcal{L}_{\mathrm{TEMOS}} = \mathcal{L}_{\mathrm{R}} + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}} + \lambda_{\mathrm{E}} \mathcal{L}_{\mathrm{E}}$$

- $\mathcal{L}_{\mathrm{R}}$：运动重建损失，由解码器分支提供；
- $\mathcal{L}_{\mathrm{KL}}$：KL 散度正则项，约束潜在分布接近标准高斯；
- $\mathcal{L}_{\mathrm{E}}$：跨模态嵌入相似度损失，仅使用正样本对。

对比损失权重 $\lambda_{\mathrm{NCE}}=0.1$ 在实验中表现最优。该联合训练策略使模型在保持运动生成能力的同时，显著改善了跨模态嵌入空间的结构化程度。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2305_00976/figures/009_Figure_4.jpg]]
*Figure 4: Moment retrieval: We plot the similarity between the temporally annotated BABEL text labels and the motions in a sliding window manner, and obtain a 1D signal over time (blue). We observe that a localization ability emerges from our model, even though it was not trained for temporal localization, and was not with the domain of BABEL labels. The ground-truth temporal span is denoted in green and the maximum similarity is marked with a dashed red line. More examples are provided in Appendix Figure A.2*

## 实验与分析

### 主实验结果

TMR 在两个主流文本-动作检索基准上均大幅超越现有方法。Table 1 展示了 HumanML3D 数据集上四种难度递减的评估协议结果。在最具挑战性的全测试集协议（a）下，TMR 的 text-motion R@1 达到 5.68，而 TEMOS 仅为 2.12，Guo et al. 为 1.80；motion-text R@1 达到 9.95，TEMOS 为 3.86，Guo et al. 为 2.92。Median Rank 从 TEMOS 的 173 降至 28，表明检索排序质量有根本性改善。在引入文本相似度阈值的协议（b）下，TMR 的 text-motion R@1 进一步提升至 11.60，相比 TEMOS 的 5.21 提升超过一倍。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2305_00976/figures/003_Table_1.jpg]]
*Table 1: Text-to-motion retrieval benchmark on HumanML3D: We establish four evaluation protocols as described in Section 4.1, with decreasing difficulty from (a) to (d). Our model TMR substantially outperforms the prior work of Guo et al. [15] and TEMOS [36], on the challenging H3D dataset*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2305_00976/figures/004_Table_2.jpg]]
*Table 2: Text-to-motion retrieval benchmark on KIT-ML: As in Table 1, we report the four evaluation protocols, this time on the KIT dataset. Again, TMR significantly improves over Guo et al. [15] and TEMOS [36] across all protocols and metrics*

Table 2 报告了 KIT-ML 数据集上的对应结果，趋势一致。在协议（b）下，TMR 的 text-motion R@1 达到 24.58，TEMOS 为 18.55，Guo et al. 为 18.55；Median Rank 从 TEMOS 的 24 降至 17。在难度最高的协议（a）下，TMR 的 text-motion R@1 为 7.23，TEMOS 为 4.58，Median Rank 从 24 降至 17。两个数据集上的一致提升验证了 TMR 框架的鲁棒性。

### 消融实验

**损失函数组合。** Table 3 揭示了两个关键设计选择。第一，联合训练运动重建分支（解码器）对检索性能至关重要：当移除运动解码器仅保留对比损失时，text-motion R@3 从 41.93 降至 36.87；R@1 从 29.59 降至 24.02。这表明运动重建损失通过解码器分支保留了更完整的文本语义信息，间接强化了嵌入空间的结构化程度。第二，InfoNCE 对比损失显著优于基于 margin 的对比损失：在相同条件下，InfoNCE 的 R@1 为 41.93，而 margin-based 损失仅为 34.46。InfoNCE 通过 softmax 归一化在嵌入空间中进行全局比较，比仅依赖固定 margin 的局部约束更有效。

**负样本过滤。** Table 4 展示了文本相似度阈值对负样本过滤效果的影响。不过滤时（阈值 1.0），text-motion R@3 仅为 36.02；阈值设为 0.8 时达到最佳 41.93；阈值过低（0.6）时性能下降至 40.19，因为过度过滤可能移除有效负样本。核心机制在于：训练批次中常存在语义高度相似但并非真正配对的样本（如“一个人走路”与“一个人缓慢行走”），若将其作为负样本强制推开，会破坏嵌入空间的语义连续性。基于 MPNet 的文本相似度过滤有效识别并排除这些“错误负样本”，使对比学习聚焦于真正需要区分的样本对。Table A.1 显示，阈值 0.8 时约 12% 的负样本对被过滤，阈值 0.6 时增至约 25%。

**超参数敏感性。** Table 5 分析了对比训练的三个关键超参数。温度 τ=0.1 时性能最优，τ 过大（1.0）会软化分布导致区分度下降，τ 过小（0.01）则使梯度过于稀疏。对比损失权重 λ_NCE=0.1 达到最佳平衡，权重过大（1.0）会压制 TEMOS 原始损失的作用。批次大小在 32 附近性能较好，过小（16）时负样本不足，过大（64）时学习率需按比例调整，性能基本持平。

**潜在空间维度。** Table A.3 表明嵌入维度 d=128 时性能最优，但本文其他实验沿用 TEMOS 的 d=256 设置以保持公平比较。

### 运动生成与检索的协同效应

Table A.2 通过交叉验证揭示了生成与检索的深层关系。以 TMR 作为生成器时，无论使用何种检索评估模型，其生成动作的检索性能均优于或持平于 Guo et al. 的生成方法，证明 TMR 没有因加入对比训练而牺牲生成质量。值得注意的是，同时具备生成能力的检索模型（TEMOS、TMR）在评估自身生成的动作时存在一定偏向性，部分生成动作的检索分数甚至超过真实动作，可能是因为生成动作有时更忠实地反映了输入文本，而真实动作的文本标注可能不够完整。

### 零样本瞬间检索能力

Figure 4 展示了 TMR 在 BABEL 数据集上的零样本时序定位能力。尽管模型未针对时序定位进行训练，也未曾接触 BABEL 的动作标注，但通过滑动窗口计算文本-动作相似度，模型能自发地对齐文本描述与动作片段的时间边界。Figure A.1 的定量评估显示，在 IoU 阈值为 0.3 时定位准确率约 40%，IoU 阈值为 0.5 时降至约 20%，表明零样本能力虽已涌现但精度仍有较大提升空间。Figure A.2 补充了更多定性示例，包括超长序列（500 帧以上）上的挑战性案例。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2305_00976/figures/016_Figure.jpg]]

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2305_00976/figures/017_Figure.jpg]]

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2305_00976/figures/015_Figure_4.jpg]]
*Figure 4: Figure A.2. Moment retrieval (qualitative): To complement Figure 4 of the main paper, (a) we provide six additional temporal localization results for various text queries on the BABEL dataset. (b) We further visualize six challenging examples when querying on very long motion sequences, i.e., more than 500 frames (25 seconds). (a) (b)*

### 失败模式与局限性

定性检索结果（Figure 3）揭示了模型的典型失败模式。第一行“演奏小提琴”的 Top-5 结果均正确且相似度 >0.80；第二行“倒立”查询仅 Top-1 正确，其余为语义相近但不同的“侧手翻”（相似度 <0.70）；第三行自由文本查询“有人在游泳”成功找到游泳动作，但 Top-2 为非游泳的俯卧动作。这表明模型在细粒度动作区分（如倒立 vs 侧手翻）和开放词汇理解上仍有不足。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2305_00976/figures/008_Figure_3.jpg]]
*Figure 3: Qualitative retrieval results: We demonstrate example queries on the left, and corresponding retrieved motions on the right, ranked by text-motion similarity. The similarity values are displayed on the top. For each retrieved motion, we also show their accompanying ground-truth text label; note that we do not use these descriptions, but only provide them for analysis purposes. The motions from the gallery are all from the test set (unseen during training). In the first row, all top-5 retrieved motions correspond visually to ‘playing violin’ and the similarity scores are high >0.80. In the second row, we correctly retrieve the ‘handstand’ motion at top-1, but the other motions mainly perform...*

更广泛的局限性包括：（1）训练数据限于有限的动作-文本配对，对野外动作的泛化能力受限；（2）检索阶段需存储全部候选动作的嵌入向量，内存占用随数据库规模线性增长；（3）动作生成分支在长时间序列或极端细节上可能出现脚步滑动等物理不真实现象；（4）瞬间检索为零样本涌现能力，定位精度远未达到实用水平。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2305_00976/figures/010_Table.jpg]]
*Table: A.1. Percentage of filtered negatives per batch in KIT: We compute the average percentage of negative pairs per batch that are discarded from the loss computation due to text similarity. The percentage decreases with higher thresholds as expected (top), but the batch size does not have a significant impact (bottom)*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2305_00976/figures/001_Figure_1.jpg]]
*Figure 1: Text-to-motion retrieval: We illustrate the task of text-based motion retrieval where the goal is to rank a gallery of motions according to their similarity to the given query in the form of a natural language description*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2305_00976/figures/005_Table_3.jpg]]
*Table 3: Losses: We experiment with various loss definitions (i) with/without the motion reconstruction, and (ii) the choice of the contrastive loss between InfoNCE and margin-based. We see that InfoNCE [34] is a better alternative to the contrastive loss with Euclidean margin [18] (employed by Guo et al. [15]). The reconstruction loss through the motion decoder branch further boosts the results*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2305_00976/figures/006_Table_4.jpg]]
*Table 4: Filtering negatives: We compare several threshold values for filtering negatives from the loss comparison due to having similar texts. We observe that removing negatives based on text similarity above 0.8 (from a scale between [0,1]) performs well overall*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

TMR 的核心技术路径是在 **TEMOS**（文本-动作合成模型）的框架上进行功能性扩展。TEMOS 本身是一个基于 Transformer VAE 的生成模型，其训练目标由三部分加权构成：运动重构损失 $\mathcal{L}_{\mathrm{R}}$、KL 散度正则项 $\mathcal{L}_{\mathrm{KL}}$ 以及跨模态嵌入相似性损失 $\mathcal{L}_{\mathrm{E}}$。该嵌入损失仅利用正样本对进行优化，缺乏对负样本的显式建模，导致其跨模态嵌入空间的结构化程度不足，难以胜任细粒度检索任务。

TMR 在此基础上的关键改造体现在三个层面：

- **对比损失的引入**：在 TEMOS 的总损失中直接加入对称形式的 InfoNCE 对比损失，形成联合优化目标 $\mathcal{L}_{\mathrm{TEMOS}} + \lambda_{\mathrm{NCE}} \mathcal{L}_{\mathrm{NCE}}$（权重 $\lambda_{\mathrm{NCE}}=0.1$）。这一改动将训练范式从“仅拉近正样本对”转变为“同时拉近正样本对、推远负样本对”，从根本上重塑了嵌入空间的几何结构。

- **负样本过滤机制**：标准的对比学习将批次内所有非配对样本视为负样本，但在文本-动作数据中，不同样本可能具有高度相似的语义描述（如“一个人向前走”与“一个人缓慢前行”），将其作为负样本排斥会造成错误的训练信号。TMR 利用预训练的 MPNet 计算批次内文本对的相似度，将相似度超过阈值 0.8 的负样本对从 InfoNCE 损失的计算中排除，从而避免“错误负样本”对嵌入空间结构的破坏。

- **生成分支的保留**：与纯粹的对比检索模型不同，TMR 保留了 TEMOS 的运动解码器分支，使模型同时具备动作生成能力。消融实验表明，这一生成分支的存在对检索性能本身也有显著贡献——移除运动重构损失后，text-motion R@3 从 41.93 降至 36.87。

与另一基线 **Guo et al.**（首个文本-动作检索模型）相比，TMR 在对比损失的选择上存在代际差异：Guo et al. 采用基于欧氏距离的 margin 对比损失，而 TMR 的消融实验直接证明 InfoNCE 损失在该任务上更为有效（R@1 为 41.93 vs 34.46）。

### 2. 适用边界

TMR 的设计和实验验证主要围绕以下边界条件展开：

- **数据域**：训练和评估均在 HumanML3D 和 KIT-ML 两个受控的动作-文本数据集上进行，动作数据源自 AMASS 运动捕捉数据库，文本标注为实验室环境下的规范描述。模型对野外动作（in-the-wild motions）和自由形式文本查询的泛化能力尚未经过系统验证。

- **检索模式**：模型的核心能力是全序列级别的文本-动作双向检索。虽然论文展示了在 BABEL 数据集上的零样本瞬间检索能力，但这一能力是未经过专门训练的涌现行为，定位精度（以 IoU 为指标）仍有较大提升空间。

- **嵌入空间维度**：论文主要在维度 $d=256$ 下进行实验（与 TEMOS 保持一致），消融实验显示 $d=128$ 在部分指标上更优，但整体结论在常用维度范围内保持稳健。

- **批次大小**：对比损失的超参数敏感性分析表明，批次大小在 32 附近时性能较好，过小或过大的批次均可能导致性能下降。

### 3. 局限性与已知问题

- **数据依赖性**：模型性能高度依赖有限的动作-文本配对数据的规模和质量。在数据稀缺的场景下，对比学习的负样本多样性和负样本过滤的准确性均会受到制约。

- **检索存储开销**：在实际部署中，需要为检索数据库中的所有运动序列预先计算并存储嵌入向量。当数据库规模较大时，这会导致显著的内存占用，论文未涉及压缩或近似最近邻搜索等工程优化方案。

- **动作生成质量**：尽管联合训练未显著损害生成性能（附录 Table A.2 的交叉验证表明 TMR 的生成质量与 Guo et al. 相当或更优），但动作解码器在极端细节（如脚步滑动）和长时间序列生成上仍可能存在不真实现象，这是基于 VAE 的动作生成方法的共性问题。

- **瞬间检索的精度**：零样本瞬间检索的定位精度有限，且该能力依赖于滑动窗口相似度计算的启发式策略，缺乏端到端的时序定位优化。

### 4. 开放问题

基于上述局限性和论文的技术路径，以下问题值得进一步探索：

- **数据扩展策略**：能否利用更大规模的弱标注数据或合成数据来提升模型在野外动作上的鲁棒性？合成动作数据生成与对比学习相结合是否可行？

- **检索效率优化**：有哪些嵌入压缩方法（如乘积量化、二值化）或近似最近邻搜索策略可以有效降低大规模检索时的内存占用和查询延迟，同时保持检索精度？

- **时序定位的端到端化**：是否可以在 TMR 的框架上引入时序提议网络或注意力机制，将瞬间检索从零样本涌现能力转化为经过端到端优化的显式能力？

- **对比学习范式的演进**：除 InfoNCE 外，SimCLR、BYOL、MoCo 等更先进的对比学习目标或架构是否能在文本-动作检索任务上带来额外收益？特别是 MoCo 的记忆库机制可能有助于缓解批次大小对负样本多样性的限制。

- **多模态融合深度**：当前模型在嵌入空间层面进行跨模态对齐，更深层次的特征交互（如跨模态 Transformer）是否能进一步提升细粒度检索能力，同时保持检索效率？

## 原文 PDF

![[paperPDFs/ICCV_2023/TMR_Text_to_Motion_Retrieval_Using_Contrastive_3D_Human_Motion_Synthesis.pdf]]