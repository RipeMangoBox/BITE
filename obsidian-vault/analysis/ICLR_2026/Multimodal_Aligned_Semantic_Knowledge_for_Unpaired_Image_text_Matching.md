---
title: "Multimodal Aligned Semantic Knowledge for Unpaired Image-text Matching"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Multimodal_Aligned_Semantic_Knowledge_for_Unpaired_Image_text_Matching.pdf
project_link: null
code_link: null
openreview_forum_id: d3CISVVO6v
aliases:
- MASKUITM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "利用预训练词嵌入作为桥梁，通过语义关系为OOD词构造原型视觉表示，并引入原型一致性对比学习损失以结构正则化特征空间，显著缓解分布方差带来的负面影响。"
primary_logic: "将词嵌入空间与视觉原型空间进行关系保持的等距映射（MTM），使区域表示能够捕捉词间的语义结构，从而即使在非配对场景下也能为未见词生成有意义且判别力强的视觉原型。"
claims:
- "MASK利用词嵌入作为桥梁将词与对应原型关联，并为OOD词基于语义关系构造原型"
- "原型一致性对比学习损失L_cl能够显著降低类内方差，提升性能贡献最大"
- "MASK在Flickr30K和MSCOCO非配对匹配上均取得最优性能"
- "通过重排序，MASK能够进一步提升预训练模型（CLIP/ALBEF）的零样本匹配性能"
---

# Multimodal Aligned Semantic Knowledge for Unpaired Image-text Matching

> [!tip] 核心洞察
> 将词嵌入空间与视觉原型空间进行关系保持的等距映射（MTM），使区域表示能够捕捉词间的语义结构，从而即使在非配对场景下也能为未见词生成有意义且判别力强的视觉原型。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向非配对图文匹配的多模态对齐语义知识 |
| 英文题名 | Multimodal Aligned Semantic Knowledge for Unpaired Image-text Matching |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=d3CISVVO6v) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | MASK |
| Dataset | Flickr30k, MSCOCO, Flickr30k (CLIP re-rank) |

> [!tip] 效果简介
> - Flickr30k 上，R@1 Image Retrieval 为 4.8，对比 3.8 (MACK^{VG-M})，变化 +1.0。
> - Flickr30k 上，R@1 Image Annotation 为 12.1，对比 10.4 (MACK^{VG-M})，变化 +1.7。
> - MSCOCO 上，Rs (sum of all recalls) 为 209.5，对比 205.2 (MACK^{VG-M})，变化 +4.3。

## 概要

**核心问题**：非配对图文匹配（Unpaired Image-Text Matching）无需成对标注数据，但现有方法面临两个关键瓶颈——无法为训练中未见的分布外（OOD）词构建语义对应的视觉原型，且忽略了不同词关联的视觉区域表示存在显著的分布方差差异，导致匹配精度受限。

**核心思路**：本文提出多模态对齐语义知识框架 **MASK**，以预训练词嵌入为桥梁建立视觉原型空间与语义空间的等距映射，使区域表示能够捕捉词间的语义结构。对于OOD词，利用词嵌入的局部线性属性，基于语义相似度从已知视觉原型中加权构造其原型表示；同时引入原型一致性对比学习损失对特征空间进行结构正则化，有效缓解分布方差带来的负面影响。

**方法定位**：MASK属于基于知识的非配对匹配方法，区别于 **MACK**（Huang et al., 2022）等直接建立区域-单词一对一关联的范式。其核心改动在于：1）通过模态传递模型（MTM）实现关系保持的跨模态对齐；2）为OOD词提供语义驱动的原型构造机制；3）以原型为类中心的对比学习正则化。该方法同时可作为重排序模块，与CLIP、ALBEF等预训练模型结合以提升零样本匹配性能。

**主要结果**：在Flickr30K和MSCOCO两个标准基准上，MASK在非配对设置下均取得最优性能——Flickr30K图像检索R@1达到4.8（较MACK^VG-M提升1.0），MSCOCO的Rs达到209.5（提升4.3）。作为重排序模块时，CLIP+MASK在Flickr30K上Rs达534.3，ALBEF+MASK在MSCOCO上Rs达436.2，均显著优于原始模型及其他重排序方法。消融实验表明，原型一致性对比损失对性能贡献最大，OOD词原型构造机制同样带来可观的增益。



图文匹配（Image-Text Matching）是跨模态理解的核心任务，其目标是在图像与文本之间建立语义对应关系。传统配对匹配方法依赖大规模人工标注的图文对进行训练，但此类数据的获取成本高昂，且覆盖的视觉概念有限。为突破这一限制，非配对图文匹配（Unpaired Image-Text Matching）逐渐成为研究热点——它仅需独立收集的图像和文本数据，无需成对标注。

现有非配对匹配方法可大致分为两类：基于模型的方法与基于知识的方法。基于模型的方法（如 **CHAN** (Pan et al., 2023)、**DSRLN** (Wu et al., 2024)、**CORA** (Pham et al., 2024)、**BOOM** (Li et al., 2024a)、**3SHNet** (Ge et al., 2024)）试图通过隐式跨模态对齐来学习匹配函数，但它们在面对训练数据中未出现的视觉概念时泛化能力有限。基于知识的方法（如 **MACK** (Huang et al., 2022)、**MACK^{VG-M}** (Huang et al., 2024b)）通过构建“词-视觉原型”的知识库来进行匹配，将每个词与一组检测到的视觉区域原型关联，从而在非配对设置下实现更透明的语义桥接。

然而，现有基于知识的方法存在两个关键瓶颈：

**瓶颈一：分布外（OOD）词无法获得有效的视觉原型。** 当测试文本中包含训练知识库中未出现的词时，现有方法缺乏为这些OOD词构造语义对应视觉表示的能力。它们仅依赖已有原型进行匹配，导致对OOD词的语义理解完全缺失，匹配精度因此受限。

**瓶颈二：忽略不同词关联的视觉区域表示存在分布方差差异。** 同一词对应的不同视觉实例（如不同姿态、外观的“狗”）在特征空间中的分布方差可能显著不同，而现有方法未对此进行结构化约束。这种方差差异使得原型表示不够紧凑、判别力不足，进而影响匹配质量。

上述瓶颈的根源在于：现有方法未能充分利用词嵌入空间与视觉原型空间之间的语义结构对应关系。词嵌入（如GloVe）天然编码了词间的语义相似性——例如“狗”与“犬”、“猫”在嵌入空间中距离相近。若能建立一种机制，使视觉原型空间保持与词嵌入空间一致的语义拓扑结构，那么即使对于未见过的OOD词，也可通过其与已知词在词嵌入空间中的语义邻近关系，推断出对应的视觉原型。

基于这一洞察，本文提出**MASK（Multimodal Aligned Semantic Knowledge）**框架，核心思路是：以预训练词嵌入为桥梁，通过关系保持的等距映射将视觉原型空间与词嵌入空间对齐，从而为OOD词构造有意义的视觉原型，并引入原型一致性对比学习来结构正则化特征空间，显著缓解分布方差带来的负面影响。



## 核心方法与创新机理

MASK 的核心创新在于将预训练词嵌入作为跨模态语义对齐的桥梁，系统性地解决了非配对图文匹配中两个相互关联的瓶颈：**分布外（OOD）词无法获得有意义的视觉原型**，以及**不同词关联的视觉区域表示存在显著的分布方差差异**。

### 创新一：词嵌入桥接的语义对齐机制

现有基于知识的方法（如 **MACK**，Huang et al., 2022）直接将检测到的区域原型与单词进行一对一关联，缺乏对词间语义关系的建模。MASK 的关键突破在于引入**模态传递模型（Modality Transfer Model, MTM）**，将视觉区域表示映射到词嵌入空间，并通过关系保持的等距映射条件约束该映射：

$$
d_s(f(\mu_i;\Theta_f), f(\mu_j;\Theta_f)) \propto d_s(\mu_i, \mu_j)
$$

这一设计使得区域表示能够“继承”词嵌入空间中的语义结构——语义相近的词（如“dog”与“puppy”）在视觉原型空间中也被拉近，而语义无关的词则被推远。跨模态对齐损失 $\mathcal{L}_{cm}$ 同时优化两个目标：拉近预测词嵌入与真实词嵌入的余弦相似度，并保持区域表示间的语义关系一致性。t-SNE 可视化（Figure 3）定性地证实了这一效果：MASK 的原型区域表示在语义上呈现清晰的聚类结构，而 MACK 的原型则混杂无序。

### 创新二：基于语义关系的 OOD 词原型构造

非配对场景下，测试文本中必然包含训练知识库未覆盖的 OOD 词。现有方法对此无能为力，因为其原型构造完全依赖已知视觉区域。MASK 利用词嵌入空间的局部线性属性，通过 top-m 最近邻的语义相似度加权求和，为 OOD 词构造视觉原型：

$$
v_{out} = \sum_{q=1}^{m} s_q \cdot v_q, \quad \{s_q\}_{q=1}^{m} = \operatorname{softmax}(w_{out} \cdot \{w_q\}_{q=1}^{m})
$$

这一机制的有效性在消融实验中得到验证：移除 OOD 词后，Flickr30k 图像检索 R@1 从 4.8 降至 4.5（Table 3），表明 OOD 原型构造对匹配精度有实质性贡献。采样大小 $m=10$ 时性能最优，过小会引入信息不足，过大则会引入语义噪声（Table 5）。

### 创新三：原型一致性对比学习的特征空间正则化

不同词关联的视觉区域在表示空间中存在显著的分布方差差异——常见物体（如“person”）的区域表示高度分散，而特定物体（如“giraffe”）则相对集中。这种方差差异使得基于原型相似度的匹配分数不可比。MASK 引入**原型一致性对比学习损失** $\mathcal{L}_{cl}$，以每个词的原型为类中心，最大化类内区域表示与原型的一致性，同时最小化类间相似度：

$$
\mathcal{L}_{cl} = -\frac{1}{B} \sum_{k=1}^{B} \log \frac{\exp(v_k \cdot \mu_+ / \tau)}{\sum_{n=1}^{B} \exp(v_k \cdot \mu_n / \tau)}
$$

消融实验表明，$\mathcal{L}_{cl}$ 对性能的贡献最大（Table 3），移除该损失后 Rs 显著降低。这一结果揭示了方差正则化在非配对匹配中的关键作用——仅靠语义对齐不足以弥合不同词类间的分布差异。

### 创新四：重排序框架的零样本扩展

MASK 的知识获取与匹配过程独立于任何下游图文对，因此可作为即插即用的重排序模块，与预训练模型（CLIP、ALBEF）的相似度分数进行 Z-Score 归一化后加权融合：

$$
\hat{s}^k = ZS(\tilde{s}^k) + \alpha \cdot ZS(s^k)
$$

当 $\alpha=0.15$ 时取得最佳性能（Table 6），CLIP+MASK 在 Flickr30k 上达到 534.3 Rs，较原始 CLIP 提升 8.8 点（Table 2）。这一扩展将 MASK 从独立的匹配方法升级为通用的跨模态检索增强工具。

### 与 baseline 的关键差异总结

| 维度 | 现有方法（MACK 等） | MASK |
|------|---------------------|------|
| 语义对齐 | 直接关联词与原型，无语义桥接 | 词嵌入作为桥梁，MTM 保持关系等距映射 |
| OOD 处理 | 仅依赖已知原型，无法处理 OOD 词 | 基于词嵌入相似度加权构造 OOD 原型 |
| 特征正则化 | 无原型级对比学习 | $\mathcal{L}_{cl}$ 以原型为中心降低类内方差 |
| 区域表示 | 直接使用 Faster-RCNN 原始特征 | PAE+FRM 提取高内聚低耦合表示并保留信息 |



![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_d3CISVVO6v/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between existing matching paradigms and our proposed unpaired framework*

MASK框架的核心设计动机源于非配对图文匹配中的两个关键瓶颈：其一，现有方法无法为分布外（OOD）词构造有意义的视觉原型；其二，不同词关联的区域表示之间存在显著的分布方差差异，导致匹配判别力不足。为解决上述问题，MASK以预训练词嵌入作为跨模态语义桥梁，将视觉原型空间与词嵌入空间进行关系保持的对齐，使区域表示能够继承词间的语义结构。

### 两阶段流水线

MASK的整体流水线分为**知识获取**与**知识匹配**两个阶段，如Figure 2所示。在知识获取阶段，框架从外部多模态数据中提取语义概念的原型视觉表示，并通过跨模态对齐损失和原型一致性对比损失进行结构化训练；在知识匹配阶段，利用已获取的多模态知识作为桥梁，将图像区域表示与文本单词原型进行匹配，并支持对OOD词的语义原型构造。

### 核心模块与数据流

**原始区域特征提取**：采用在Visual Genome上预训练的Faster-RCNN（BUTD）检测器提取图像区域特征 $r_j$，作为后续所有视觉表示的初始输入。

**Prototype-Aware Encoder (PAE)**：PAE模型 $h$ 以原始区域表示 $R$ 为输入，提取高内聚、低耦合的区域表示 $\mu$ 及其方差 $\sigma$：
$$\mu, \sigma = h(R; \Theta_h)$$
PAE由一个全连接层和三个自注意力层组成，旨在生成更具判别力的区域表示。

**Feature Restoration Module (FRM)**：FRM模型 $g$ 从隐空间 $(\mu, \sigma, z)$ 重建原始区域表示 $R'$，以保留信息完整性：
$$R' = g(\mu, \sigma, z; \Theta_g)$$
FRM包含一个自注意力层和两个全连接层，与PAE通过信息保留损失 $\mathcal{L}_{ir}$ 联合训练。

**Modality Transfer Model (MTM)**：MTM $f$ 将区域表示 $\mu$ 映射到词嵌入空间，得到预测的词嵌入 $V'$：
$$V' = f(\mu; \Theta_f)$$
该映射需满足关系保持等距条件——映射前后区域表示间的距离成比例，从而确保视觉空间中的语义结构忠实反映词嵌入空间中的语义关系。

**原型计算与OOD构造**：对于知识库中的每个词 $k$，其原型区域表示 $v_k$ 为所有相关区域表示 $\mu_j$ 的均值：
$$v_k = \frac{1}{J_k} \sum_{j=1}^{J_k} \mu_j$$
对于知识库之外的OOD词，MASK利用词嵌入的局部线性属性，通过top-m最近邻的语义相似度加权构造其视觉原型：
$$\{s_q\}_{q=1}^{m} = \operatorname{softmax}(w_{out} \cdot \{w_q\}_{q=1}^{m})$$
$$v_{out} = \sum_{q=1}^{m} s_q \cdot v_q$$

**匹配与重排序**：在知识匹配阶段，通过max-mean pooling操作 $\rho(\cdot)$ 计算图像区域表示 $\boldsymbol{\mu}$ 与单词原型矩阵 $\boldsymbol{U}$ 的全局相似度：
$$s = \rho(\boldsymbol{\mu} \cdot \boldsymbol{U}^T)$$
MASK还可作为重排序模块，将自身相似度与现有模型（如CLIP、ALBEF）的相似度通过Z-Score归一化后按因子 $\alpha$ 融合：
$$\hat{s}^k = ZS(\tilde{s}^k) + \alpha \cdot ZS(s^k)$$

### 训练目标

整体训练损失由三项加权组成：
$$\mathcal{L} = \mathcal{L}_{ir} + \lambda_1 \mathcal{L}_{cm} + \lambda_2 \mathcal{L}_{cl}$$
其中 $\mathcal{L}_{ir}$ 为信息保留损失（推动隐分布趋向标准正态并最小化重建误差），$\mathcal{L}_{cm}$ 为跨模态对齐损失（拉近预测词嵌入与真实词嵌入，同时保持区域表示间的语义关系），$\mathcal{L}_{cl}$ 为原型一致性对比损失（以原型为类中心最大化类内相似度、最小化类间相似度）。消融实验表明，$\mathcal{L}_{cl}$ 对性能的贡献最大，且 $\lambda_1 = \lambda_2$ 时取得最佳整体性能。



MASK 框架的核心由四个关键模块构成：Prototype-Aware Encoder (PAE)、Feature Restoration Module (FRM)、Modality Transfer Model (MTM) 以及 OOD Prototype Construction。这些模块协同工作，将非配对场景下的视觉区域表示与词嵌入空间进行语义对齐，并为分布外词构造有意义的视觉原型。

### 3.1 原型感知编码器与特征恢复模块

PAE 的目标是从原始区域表示中提取高内聚、低耦合的表示，同时显式建模每个区域表示的分布方差。给定一批原始区域表示 $R$，PAE 模型 $h$ 输出均值 $\mu$ 和方差 $\sigma$：

$$\mu, \sigma = h(R; \Theta_h) \tag{Eq.3}$$

其中 $\Theta_h$ 为 PAE 的可学习参数。PAE 由一个全连接层和三层自注意力层组成，其输出 $\mu$ 即为后续用于匹配的区域表示。

为防止信息丢失，FRM 模型 $g$ 从隐空间重建原始区域表示：

$$R' = g(\mu, \sigma, z; \Theta_g) \tag{Eq.4}$$

其中 $z$ 为随机噪声向量，$\Theta_g$ 为 FRM 的可学习参数。FRM 由一层自注意力层和两层全连接层构成。

信息保留损失 $\mathcal{L}_{ir}$ 由两部分组成：KL 散度项推动隐分布趋向标准正态分布，重建误差项最小化输入与重建表示之间的差异：

$$\mathcal{L}_{ir} = D_{KL}(\mathcal{N}(\mu, \sigma^2) \| \mathcal{N}(0,1)) + \mathbb{E}_{(r_n, r_n') \sim (R, R')} [\|r_n - r_n'\|_2^2] \tag{Eq.5}$$

### 3.2 原型一致性对比学习损失

为缓解不同词关联的区域表示之间存在分布方差差异的问题，MASK 引入原型一致性对比学习损失 $\mathcal{L}_{cl}$。该损失以每个词的原型区域表示 $v_k$ 为类中心，最大化原型与其相关区域表示 $\mu_+$ 的相似度，同时最小化与其他原型区域表示的相似度：

$$\mathcal{L}_{cl} = -\frac{1}{B} \sum_{k=1}^{B} \log \frac{\exp(v_k \cdot \mu_+ / \tau)}{\sum_{n=1}^{B} \exp(v_k \cdot \mu_n / \tau)} \tag{Eq.6}$$

其中 $B$ 为批次大小，$\tau$ 为温度系数。消融实验证实，$\mathcal{L}_{cl}$ 对性能的贡献最大（Table 3）。

### 3.3 模态传递模型与跨模态对齐

MTM 模型 $f$ 将区域表示 $\mu$ 映射到词嵌入空间，得到预测的词嵌入 $V'$：

$$V' = f(\mu; \Theta_f) \tag{Eq.7}$$

该映射需满足关系保持的等距条件，即映射前后区域表示之间的语义距离成比例：

$$d_s(f(\mu_i;\Theta_f), f(\mu_j;\Theta_f)) \propto d_s(\mu_i, \mu_j) \tag{Eq.8}$$

跨模态对齐损失 $\mathcal{L}_{cm}$ 同时约束两个目标：一是拉近预测词嵌入与真实词嵌入之间的余弦相似度，二是保持区域表示间的语义关系与词嵌入间的关系一致：

$$\mathcal{L}_{cm} = \mathbb{E}[(1 - \cos(\frac{w_i}{\|w_i\|_2}, \frac{w_i'}{\|w_i'\|_2}))] + \mathbb{E}[((\cos(\frac{w_i'}{\|w_i'\|_2}, \frac{w_j'}{\|w_j'\|_2}) - \cos(\frac{\mu_i}{\|\mu_i\|_2}, \frac{\mu_j}{\|\mu_j\|_2})))^2] \tag{Eq.9}$$

### 3.4 OOD 词原型构造

对于不在知识库中的 OOD 词，MASK 利用词嵌入的局部线性属性，基于语义相似度从已知原型中加权构造其视觉原型。首先计算 OOD 词嵌入 $w_{out}$ 与 top-$m$ 个最近邻已知词嵌入的 softmax 相似度：

$$\{s_q\}_{q=1}^{m} = \operatorname{softmax}(w_{out} \cdot \{w_q\}_{q=1}^{m}) \tag{Eq.11}$$

然后通过加权求和得到 OOD 词的原型区域表示：

$$v_{out} = \sum_{q=1}^{m} s_q \cdot v_q \tag{Eq.12}$$

消融实验表明，采样大小 $m=10$ 时性能最佳，过高或过低会分别引入噪声或信息不足（Table 5）。

### 3.5 全局匹配分数与总体损失

给定图像的区域表示矩阵 $\boldsymbol{\mu}$ 和文本中词的原型表示矩阵 $\boldsymbol{U}$，全局图文匹配分数通过 max-mean pooling 计算：

$$s = \rho({\boldsymbol{\mu}} \cdot {\boldsymbol{U}}^T) \tag{Eq.10}$$

其中 $\rho(\cdot)$ 为 max-mean pooling 操作。

总体训练损失由信息保留损失、跨模态对齐损失和原型对比损失加权组合：

$$\mathcal{L} = \mathcal{L}_{ir} + \lambda_1 \mathcal{L}_{cm} + \lambda_2 \mathcal{L}_{cl} \tag{Eq.14}$$

超参数分析表明，$\lambda_1 = \lambda_2 = 3$ 时取得最佳整体性能，说明两个损失项需均衡优化（Table 15）。

### 3.6 重排序扩展

MASK 可无缝扩展为重排序方法。将现有模型的相似度向量 $\tilde{s}^k$ 与 MASK 的相似度向量 $s^k$ 经 Z-Score 归一化后按因子 $\alpha$ 融合：

$$\hat{s}^k = ZS(\tilde{s}^k) + \alpha \cdot ZS(s^k) \tag{Eq.15}$$

消融实验确定 $\alpha = 0.15$ 时取得最佳重排序性能（Table 6）。



## 实验与关键发现

### 非配对图文匹配主结果

MASK在Flickr30K和MSCOCO两个标准基准上均取得最优非配对匹配性能。与基于知识的方法相比，MASK在Flickr30K图像检索R@1上达到4.8，较此前最强的**MACK^{VG-M}**（Huang et al., 2024b）的3.8提升1.0个点；在图像标注R@1上达到12.1，提升1.7个点。在MSCOCO上，MASK以209.5的Rs总分超越MACK^{VG-M}的205.2（Table 1）。与基于模型的匹配方法相比，MASK在Flickr30K上同样全面超越**CORA**（Pham et al., 2024）、**BOOM**（Li et al., 2024a）和**3SHNet**（Ge et al., 2024）等方法，验证了语义知识对齐策略在非配对场景下的有效性。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_d3CISVVO6v/figures/003_Table_1.jpg]]
*Table 1: Performance comparison between model-based matching and knowledge-based matching on the Flickr30k and MSCOCO datasets for the unpaired image-text matching*

### 零样本重排序实验

MASK可作为即插即用的重排序模块提升预训练模型的零样本匹配性能。在Flickr30K上，CLIP+MASK以534.3的Rs超越原始CLIP的525.5（+8.8），并优于**CLIP+MACK**（Huang et al., 2022）、**CLIP+LeaP RR**（Qu et al., 2023）和**CLIP+FR**（Wei et al., 2025）等重排序方法。在MSCOCO上，ALBEF+MASK达到436.2 Rs，较原始ALBEF的428.3提升7.9个点（Table 2）。跨数据集重排序实验（Table 9）进一步表明MASK学到的语义知识具有良好的泛化性。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_d3CISVVO6v/figures/004_Table_2.jpg]]
*Table 2: Zero-shot image-text matching by re-ranking two state-of-the-art models on the Flickr30k and MSCOCO datasets*

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_d3CISVVO6v/figures/012_Table_9.jpg]]
*Table 9: Cross-dataset image-text matching by re-ranking existing models on the Flickr30k and MSCOCO Datasets*

### 消融实验与损失贡献分析

消融实验（Table 3）揭示了各损失项的贡献权重：

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_d3CISVVO6v/figures/006_Table_3.jpg]]
*Table 3: Ablation of the overall loss and the impact of OOD words on unpaired image-text matching*

- **原型一致性对比学习损失 $\mathcal{L}_{cl}$ 贡献最大**：移除该损失后，Flickr30K图像检索R@1从4.8骤降至3.9，MSCOCO Rs从209.5降至196.8，证实了以原型为类中心的结构化正则化对于抑制分布方差的关键作用。
- **跨模态对齐损失 $\mathcal{L}_{cm}$ 贡献次之**：移除后Flickr30K R@1降至4.3，MSCOCO Rs降至200.1，说明词嵌入桥接的对齐机制是性能的核心支撑。
- **信息保留损失 $\mathcal{L}_{ir}$ 贡献相对较小**：移除后性能仍优于多数基线，但其对PAE-FRM联合训练的稳定性不可或缺。
- **OOD词处理机制有效但增益有限**：移除OOD词后，Flickr30K R@1从4.8降至4.5，MSCOCO Rs从209.5降至205.7，表明基于词嵌入语义相似度构造OOD原型能够为分布外词提供有意义的视觉表示，但当前增益主要集中在少数OOD名词上。

### 超参数灵敏度

**损失权重比例**（Table 4）：当 $\lambda_1 = \lambda_2$ 时取得最佳整体性能，Flickr30K Rs达到122.8。$\lambda_1/\lambda_2 = 0.3$ 时性能优于3.0（112.7 vs 109.2），说明跨模态对齐损失的权重略高于对比损失时更有利于训练，但极端偏斜会破坏两项约束的平衡。进一步细化搜索（Table 15）确认$\lambda_1=\lambda_2=3$为最优配置。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_d3CISVVO6v/figures/007_Table_4.jpg]]
*Table 4: Unpaired image-text matching by MASK using different $\lambda _ { 1 } / \lambda _ { 2 }$ on the Flickr30k and MSCOCO datasets

**OOD采样大小**（Table 5）：采样最近邻数量 $m=10$ 时性能最优，Flickr30K图像检索R@1达到5.0。$m$ 过小（如5）则语义信息不足，$m$ 过大（如50）则引入噪声原型，性能均有所下降。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_d3CISVVO6v/figures/008_Table_5.jpg]]
*Table 5: Unpaired image-text matching by MASK using different sampling sizes m on the Flickr30k and MSCOCO datasets*

**重排序平衡因子**（Table 6）：$\alpha=0.15$ 时CLIP+MASK取得最佳零样本性能，Flickr30K图像检索R@1达到67.3。$\alpha$ 过大会过度依赖MASK的语义知识而削弱预训练模型的判别能力，$\alpha$ 过小则无法充分引入语义对齐信息。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_d3CISVVO6v/figures/009_Table_6.jpg]]
*Table 6: Zero-shot image-text matching by MASK (CLIP) using different α on the Flickr30k and MSCOCO datasets*

### 关键组件有效性验证

**检测器选择**（Table 11）：BUTD（Faster-RCNN在Visual Genome上预训练）是MASK正常工作的必要条件。替换为DETR或DINO后性能急剧下降，即使这些检测器在目标检测任务上表现更优，但其区域特征缺乏对视觉概念的良好聚类特性，无法为原型构建提供高质量表示。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_d3CISVVO6v/figures/014_Table_11.jpg]]
*Table 11: Unpaired image-text matching using different detectors on the Flickr30k dataset*

**模型架构**（Table 12）：增加自注意力层可提升性能，但增加全连接层反而显著降低性能。这表明自注意力机制有助于捕获区域间的语义关系，而过多的非线性变换会破坏特征空间的结构信息。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_d3CISVVO6v/figures/015_Table_12.jpg]]
*Table 12: Unpaired image-text matching using different model architectures on the Flickr30k dataset*

**词向量选择**（Table 13）：GloVe词向量优于Word2Vec和FastText，更适合跨模态语义对齐任务。这可能归因于GloVe在全局词共现统计上的建模优势，使其编码的语义关系更稳定地迁移到视觉原型空间。

### t-SNE可视化分析

Figure 3对比了MACK与MASK的原型区域表示经t-SNE降维后的语义分布。MASK的表示呈现出更清晰的语义聚类结构：语义相关的词（如"man""woman""child"与"boy""girl""people"）在空间中形成紧密的簇，且簇间边界分明。相比之下，MACK的表示分布更为分散，语义相关词之间的耦合较弱。这一可视化直接验证了跨模态对齐损失 $\mathcal{L}_{cm}$ 中关系保持等距映射的效果——区域表示成功继承了词嵌入空间中的语义结构。

### 失败模式与局限性

1. **非名词词类处理不足**：MASK仅有效利用名词进行匹配，形容词、副词和代词等词类无法对应到具体视觉区域，强行构造原型会引入语义噪声。Table 10的定性示例中，OOD词标记主要集中在名词上，而"very""excited"等修饰词未被有效利用，导致部分负样本重排序错误。

2. **检测器依赖性**：MASK对BUTD检测器的强依赖限制了其与更先进视觉主干的兼容性。DETR/DINO等Transformer检测器即使经过VG预训练，性能仍远低于BUTD，这成为端到端训练的瓶颈。

3. **时态与复数变体**：当前框架将不同时态和复数形式的词视为独立词条，可能导致OOD词误判。例如"dogs"若不在知识库中，其原型由"dog"的语义近邻构造，但复数形式本身可能对应不同的视觉模式（如多只狗的场景）。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_d3CISVVO6v/figures/010_Table_7.jpg]]
*Table 7: Notation used in the paper*

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_d3CISVVO6v/figures/011_Table_8.jpg]]
*Table 8: Overview of the model architectures integrated into the MASK framework*



## 定位与知识库关联

### 1. 与非配对图文匹配方法的关系

MASK 属于**基于知识的非配对图文匹配**（knowledge-based unpaired image-text matching）范式。该范式的核心思想是：在不使用目标数据集配对图文对的前提下，利用外部知识库（如Visual Genome）中检测到的视觉概念构建跨模态语义桥梁，将图像区域与文本单词关联起来。

在此范式中，MASK 的直接前驱是 **MACK**（Huang et al., 2022）及其增强版本 **MACK^{VG-M}**（Huang et al., 2024b）。MACK 首次提出将每个单词与一个原型区域表示对齐，并通过原型桥接计算图文相似度。然而，MACK 存在两个关键瓶颈：

- **OOD词处理缺失**：MACK 仅依赖已知视觉原型进行匹配，对于知识库中未出现的分布外（OOD）词，无法构造有意义的视觉表示，导致匹配时这些词的信息被完全丢弃。
- **区域表示分布方差未控制**：MACK 未对不同单词关联的区域表示进行结构正则化，导致类内方差过大，原型判别力不足。

MASK 在这两个维度上做出了根本性改进：

1. **词嵌入桥接与关系保持映射**：MASK 引入预训练词嵌入（GloVe）作为中间桥梁，通过模态传递模型（MTM）将视觉区域表示映射到词嵌入空间，并强制该映射满足关系保持等距条件（Eq.8）。这使得区域表示能够继承词嵌入空间中的语义结构，为后续 OOD 词的原型构造提供了基础。

2. **OOD词原型构造**：基于词嵌入的局部线性属性，MASK 利用 OOD 词与已知词的词嵌入余弦相似度作为权重，对已知视觉原型进行加权求和，构造 OOD 词的代理原型（Eq.11-12）。这一机制使得 MASK 能够为训练时未见过的词生成有意义的视觉表示。

3. **原型一致性对比学习**：MASK 引入原型一致性对比损失 $\mathcal{L}_{cl}$（Eq.6），以每个单词的原型为类中心，最大化该单词关联区域表示与原型之间的相似度，同时最小化与其他单词原型的相似度。消融实验表明，$\mathcal{L}_{cl}$ 对性能的贡献最大（Table 3），是缓解分布方差负面影响的核心机制。

与基于模型的方法（如 **CHAN** (Pan et al., 2023)、**DSRLN** (Wu et al., 2024)、**CORA** (Pham et al., 2024)、**BOOM** (Li et al., 2024a)、**3SHNet** (Ge et al., 2024)）相比，MASK 不依赖目标数据集的配对图文对进行训练，而是从外部视觉基因组中提取可迁移的跨模态知识。这使得 MASK 具有更强的泛化能力，可在零样本设置下直接应用于新数据集。

### 2. 与预训练视觉-语言模型的关系

MASK 还可作为一种**重排序（re-ranking）插件**，与现有预训练视觉-语言模型协同工作。具体而言，MASK 将自身计算的知识驱动相似度分数与预训练模型（如 CLIP、ALBEF）的相似度分数通过 Z-Score 归一化后按因子 $\alpha$ 融合（Eq.15），对初始检索结果进行重排序。

与现有重排序方法（如 **CLIP + MACK** (Huang et al., 2022)、**CLIP + LeaP RR** (Qu et al., 2023)、**CLIP + FR** (Wei et al., 2025)）相比，MASK 的优势在于其知识库中包含了 OOD 词的视觉原型，能够补充预训练模型可能忽略的细粒度视觉语义信息。实验表明，CLIP+MASK 在 Flickr30k 上达到 534.3 Rs，ALBEF+MASK 在 MSCOCO 上达到 436.2 Rs，均显著优于其他重排序方法（Table 2）。

### 3. 适用边界与局限

尽管 MASK 在非配对匹配和零样本重排序任务上取得了最优性能，其方法设计存在以下明确边界：

- **检测器依赖瓶颈**：MASK 的原始区域特征提取完全依赖在 Visual Genome 上预训练的 Faster-RCNN（BUTD）模型。当替换为 DETR 或 DINO 等更先进的检测器时，性能急剧下降（Table 11）。这表明 MASK 对检测器的预训练数据分布和区域提议质量高度敏感，尚未形成检测器无关的通用框架。

- **词类覆盖局限**：当前 MASK 仅有效利用名词进行图文匹配。形容词、副词、代词等非名词词类由于缺乏明确的视觉对应区域，无法被纳入知识对齐体系。这导致 MASK 在处理包含丰富修饰语的复杂文本时匹配能力受限。定性分析显示，对于 “very”、“excited” 等抽象词，强行构造原型会引入语义噪声，导致负样本重排序错误（Table 10）。

- **OOD词时态/复数变体未处理**：MASK 未设计针对 OOD 单词时态变化（如 “running” vs “run”）和复数形式（如 “dogs” vs “dog”）的特殊处理机制，可能将这些变体误识别为需要独立构造原型的语义概念。

### 4. 开放问题

基于上述分析，MASK 框架的后续演进方向包括：

1. **全词类语义对齐**：能否设计一种机制，将形容词、副词和代词等非名词词类也纳入知识对齐体系，例如通过场景级属性编码或关系三元组建模，实现全词级别的匹配精度提升？

2. **检测器无关的视觉编码**：DETR/DINO 等 Transformer 检测器在 VG 预训练后性能仍低于 BUTD，如何弥补其区域提取质量的差距？是否可以用 ViT 等视觉主干网络替换 Faster-RCNN，构建端到端可训练的视觉原型提取模块？

3. **词形变化的鲁棒处理**：如何有效处理 OOD 单词的时态和复数变体，避免将其误认为是具有独立视觉意义的新词？可能的方案包括引入子词级（subword）嵌入或词形还原（lemmatization）预处理。

4. **跨数据集迁移的稳定性**：MASK 在跨数据集重排序实验中（Table 9）的性能表现需要进一步验证其在不同数据分布下的稳定性，特别是在域差异较大的场景中，知识库的覆盖度可能成为瓶颈。



## 原文 PDF

![[paperPDFs/ICLR_2026/Multimodal_Aligned_Semantic_Knowledge_for_Unpaired_Image_text_Matching.pdf]]
