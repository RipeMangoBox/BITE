---
title: "Learning Like Humans: Analogical Concept Learning for Generalized Category Discovery"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Learning_Like_Humans_Analogical_Concept_Learning_for_Generalized_Category_Discovery.pdf
project_link: null
code_link: "https://github.com/zhou-9527/AnaLogical-GCD"
aliases:
- AGALGCD
- LLHACLGCD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入模仿人类类比推理的文本概念生成器（ATCG），从已标记的知识库中通过类比为未标记样本生成语义文本描述，将其与视觉特征融合，实现跨模态推理。
primary_logic: 将类别发现从纯视觉过程转变为视觉‑文本推理过程：通过融合类比生成的文本概念与视觉特征，显著增强了类别语义分离能力，尤其在细粒度场景下效果突出。
claims:
- 在六个基准数据集上，AL‑GCD 整体准确率平均提升 5.0％，细粒度数据集平均提升 7.1％（Abstract/Introduction）。
- 在 CUB 上，结合 SelEx‑CLIP 的 AL‑GCD 达到 84.1% 整体准确率，远超先前方法（Table 1）。
- 消融实验证实 ATCG 的初始层、堆叠层和视觉‑文本融合系数 α 均有贡献，其中 α=0.4 取得最佳平衡（Table 3,4, Fig 4）。
- All Datasets (CIFAR100, ImageNet100, CUB, Stanford Cars, FGVC-Aircraft, Herbari... 上 Average Overall Accuracy gain = +5.0%
---

# Learning Like Humans: Analogical Concept Learning for Generalized Category Discovery

> [!tip] 核心洞察
> 将类别发现从纯视觉过程转变为视觉‑文本推理过程：通过融合类比生成的文本概念与视觉特征，显著增强了类别语义分离能力，尤其在细粒度场景下效果突出。

| 字段 | 内容 |
|------|------|
| 中文题名 | 像人类一样学习：面向广义类别发现的类比概念学习 |
| 英文题名 | Learning Like Humans: Analogical Concept Learning for Generalized Category Discovery |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.19918) · [Code](https://github.com/zhou-9527/AnaLogical-GCD) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | AL-GCD (Analogical Learning for Generalized Category Discovery) |
| Dataset | All Datasets, Fine-grained datasets avg, CUB, CIFAR100 |

> [!tip] 效果简介
> - All Datasets (CIFAR100, ImageNet100, CUB, Stanford Cars, FGVC-Aircraft, Herbari... 上，Average Overall Accuracy gain +5.0% vs best existing methods (+5.0%)。
> - Fine-grained datasets avg 上，Average Overall Accuracy gain +7.1% vs best existing methods (+7.1%)。
> - CUB 上，All Acc. (%) 84.1 (with SelEx-CLIP) vs SelEx-CLIP (best baseline) (see Table 1)。

## 概要

**问题瓶颈**  
现有广义类别发现（GCD）方法主要依赖纯视觉特征进行聚类与分类，监督学习与新类别发现之间的耦合松散，导致已标记数据中的先验知识难以有效迁移到未标记样本。这一缺陷在视觉相似但语义不同的细粒度类别上尤为突出，模型边界脆弱。

**核心思路**  
本文提出 **AL‑GCD（Analogical Learning for Generalized Category Discovery）**，将类别发现从纯视觉过程转变为**视觉‑文本推理过程**。其关键创新是引入**类比文本概念生成器（ATCG）**——一个即插即用模块，从已标记数据构建的视觉‑文本知识库中通过类比推理，为未标记样本生成语义文本描述，并与视觉特征融合，实现跨模态推理。

**方法定位**  
AL‑GCD 采用两阶段训练框架：首先在伪 GCD 设置下训练 ATCG 的概念对齐能力，随后在实际 GCD 训练中将 ATCG 生成的类比文本嵌入与视觉嵌入通过融合头组合，再经由对比学习与参数化分类完成类别发现。相比现有 GCD 方法（如 **GCD** (Vaze et al., CVPR 2022)、**SimGCD** (Wen et al., ICCV 2023)、**CMS** (Choi et al., CVPR 2024)、**CPT** (Yang et al., IJCV 2025)、**GET** (Wang et al., CVPR 2025)、**SelEx** (Rastegar et al., ECCV 2024)），AL‑GCD 的核心差异在于**利用类比生成的文本语义增强视觉表征**，而非仅依赖视觉信号。

**主要结果**  
在六个基准数据集上，AL‑GCD 的整体准确率平均提升 **5.0%**，细粒度数据集平均提升 **7.1%**。在 CUB 数据集上结合 SelEx‑CLIP 骨干达到 **84.1%** 整体准确率，显著超越先前方法。消融实验证实 ATCG 的初始层、堆叠层以及视觉‑文本融合系数 α 均对性能有贡献，其中 α=0.4 在新旧类别间取得最佳平衡。



### 问题定义：广义类别发现（GCD）

广义类别发现（Generalized Category Discovery, GCD）要求模型在一个部分标注的数据集上，同时识别已知类别并发现未知的新类别。形式化地，给定已标记数据集 $\bar{\mathcal{D}}^l = \{(x_i^l, y_i^{\bar{l}})\} \subset \mathcal{X} \times \mathcal{Y}^l$ 和未标记数据集 $\mathcal{D}^u = \{x_i^u\} \subset \mathcal{X}$，其中未标记数据同时包含来自已知类别 $\mathcal{Y}^l$ 和未知类别 $\mathcal{Y}^u$ 的样本，且 $\mathcal{Y}^l \cap \mathcal{Y}^u = \emptyset$。模型需要为 $\mathcal{D}^u$ 中的每个样本分配一个类别标签，该标签可能来自 $\mathcal{Y}^l$ 或 $\mathcal{Y}^u$。

### 现有方法的瓶颈：纯视觉流水线的语义盲区

当前 GCD 方法（如 **GCD**（Vaze et al., CVPR 2022）、**SimGCD**（Wen et al., ICCV 2023）、**CMS**（Choi et al., CVPR 2024））主要依赖纯视觉特征进行聚类或参数化分类。即使基于 CLIP 的跨模态方法（如 **CPT**（Yang et al., IJCV 2025）、**GET**（Wang et al., CVPR 2025））引入了文本信息，其监督学习与新类别发现之间的耦合仍然松散——先验知识未能有效迁移到未标记数据。这一缺陷在视觉相似但语义不同的细粒度类别上暴露得尤为明显：例如，不同种类的鸟类或车型在视觉空间高度重叠，纯视觉特征难以构建清晰的决策边界。**SelEx**（Rastegar et al., ECCV 2024）通过自适应专家机制在细粒度 GCD 上取得进展，但本质上仍未跳出视觉单模态的限制。

### 核心动机：从“看”到“类比推理”

人类在面对新事物时，并不单纯依赖视觉外观进行分类——我们会通过类比（analogy），将新观察与已有知识建立语义关联。例如，看到一种未见过的小鸟，人会自然地将其与已知的相似鸟类进行对比，提取“喙的形状”“羽毛纹理”等语义概念，从而做出更精准的判断。受此启发，本文提出将 GCD 从纯视觉过程转变为**视觉‑文本推理过程**：通过构建一个从已标记数据中学习的类比机制，为未标记样本生成语义文本描述，并将其与视觉特征融合，从而显著增强类别语义分离能力。

### 方法定位：AL-GCD 的类比学习框架

AL-GCD（Analogical Learning for GCD）的核心创新在于引入**类比文本概念生成器（Analogical Textual Concept Generator, ATCG）**——一个即插即用的模块，它从已标记的视觉‑文本知识库中通过类比注意力机制，为每个未标记样本生成对齐的文本嵌入。这些文本嵌入随后与视觉特征融合，形成跨模态的融合表示，用于后续的对比学习和参数化分类。整个框架包含四个关键组件：视觉编码器、文本编码器、融合头投影器以及 ATCG，训练流程分为 ATCG 预训练和 GCD 训练两个阶段（Figure 2）。

在六个基准数据集上的实验表明，AL-GCD 的整体准确率平均提升 **5.0%**，在细粒度数据集上的平均提升达到 **7.1%**，验证了类比推理机制在突破纯视觉瓶颈方面的关键作用。



## 核心方法与创新机理

AL‑GCD 的核心创新在于将广义类别发现（GCD）从纯视觉匹配重新定义为**视觉‑文本类比推理过程**。其关键抓手是一个可插拔的**类比文本概念生成器（ATCG）**，该模块模仿人类“举一反三”的类比学习机制，从已标记数据构建的知识库中检索相关概念，为未标记样本生成语义文本描述，从而将先验知识有效迁移到新类别发现中。

与现有 GCD 方法相比，AL‑GCD 在以下四个关键维度上实现了根本性改变：

### 1. 特征表示：视觉嵌入 → 视觉‑文本融合嵌入

现有 GCD 流水线（如 **GCD** (Vaze et al., CVPR 2022)、**SimGCD** (Wen et al., ICCV 2023)、**CMS** (Choi et al., CVPR 2024)）仅依赖视觉编码器提取的图像特征进行聚类或分类。AL‑GCD 引入文本编码器，通过 ATCG 为每个未标记样本生成类比文本嵌入 $\tilde{\mathbf{t}}_i$，并通过融合系数 $\alpha$ 与视觉嵌入 $\mathbf{v}_i$ 加权组合：

$$\mathbf{h}_i = \alpha \cdot \mathbf{v}_i + (1-\alpha) \cdot \tilde{\mathbf{t}}_i$$

该融合表示经投影头 $g(\cdot)$ 映射后得到最终融合嵌入 $\mathbf{f}_i = g(\mathbf{h}_i)$，用于后续对比学习和参数化分类。这一设计使模型在视觉相似但语义不同的细粒度类别上获得了更强的语义分离能力——实验表明，在六个基准数据集上整体准确率平均提升 **5.0%**，细粒度数据集平均提升 **7.1%**。

### 2. 知识利用：无显式知识库 → 视觉‑文本知识库与类比检索

现有方法未构建显式知识库，已标记数据的先验信息仅通过监督损失间接影响模型。AL‑GCD 从已标记样本中提取图像‑文本嵌入对 $\{(\mathbf{v}_i^l, \mathbf{t}_i^l)\}$ 构建知识库 $\mathcal{K}$，ATCG 在处理未标记样本时，以其图像嵌入为查询，在知识库中检索相关的已知概念，通过类比注意力机制重组这些概念，生成与当前样本语义对齐的文本嵌入。这一机制将“已知类别知识”从隐式正则化提升为显式可检索、可迁移的符号化资源。

### 3. 训练流程：单一阶段 → 两阶段（ATCG 预训练 + GCD 训练）

AL‑GCD 的训练分为两个阶段：
- **ATCG 预训练阶段**：利用已标记数据构造伪 GCD 任务，训练 ATCG 生成类比文本嵌入的能力。具体地，从已标记数据中划分伪标记集和伪未标记集，ATCG 为伪未标记样本生成文本嵌入 $\tilde{\mathbf{t}}_j$，并通过类比损失 $\mathcal{L}_{\mathrm{AL}}$ 最小化其与真实文本嵌入的余弦距离，迫使 ATCG 学会“看到类似图像时联想相应文本概念”。
- **GCD 训练阶段**：固定训练好的 ATCG，为真实未标记数据生成文本嵌入，与视觉特征融合后进行对比学习和分类器训练。

这种解耦设计使 ATCG 的概念生成能力在进入实际 GCD 任务前得到充分预训练，避免了端到端联合训练中可能出现的模态不平衡问题。

### 4. 新样本处理：直接聚类/分类 → 类比文本概念引导的融合分类

现有方法对未标记样本直接基于视觉特征进行聚类（如 GCD）或参数化分类（如 SimGCD）。AL‑GCD 在未标记样本进入分类器之前，先通过 ATCG 生成类比文本嵌入，将其作为“语义先验”与视觉特征融合。消融实验证实了这一设计的有效性：仅添加 ATCG 的初始层（TIAA）已能提升性能，进一步增加堆叠层（TSA+TIAA）带来额外增益（Table 3）；ATCG 层数从 0 增加到 4 时，新颖类别准确率在 CIFAR100 上从 75.2% 提升至 86.8%（Table 4）。

### 5. 融合系数 $\alpha$ 的“已知‑未知”权衡机制

视觉‑文本融合系数 $\alpha$ 是 AL‑GCD 中一个关键的调控旋钮：$\alpha$ 越大，模型越依赖视觉特征，有利于已知类别识别；$\alpha$ 越小，文本概念的引导作用越强，有利于新类别发现。在 Stanford Cars 上的消融实验（Figure 4）表明，$\alpha=0.4$ 在已知和新类别准确率之间取得最佳平衡——当 $\alpha$ 从 0.4 增加到 0.7 时，已知类别准确率上升 1.8%，但新类别性能下降。这一发现揭示了 GCD 任务中视觉先验与语义先验的内在张力，AL‑GCD 通过可调节的融合系数为这一权衡提供了显式控制接口。



AL‑GCD 将广义类别发现（GCD）重新建模为一个**类比推理驱动的跨模态流程**，其核心思想是：让模型像人类一样，利用已掌握的概念去类比理解未见过的类别。整个框架由四个关键模块构成，按数据流依次为：

1. **视觉编码器** $f_v(\cdot)$ 与**文本编码器** $f_t(\cdot)$：分别提取图像嵌入和类别文本嵌入，为后续跨模态融合提供基础表示。
2. **知识库** $\mathcal{K}$：存储来自已标记数据的图像‑文本嵌入对 $\{(\mathbf{v}_i^l, \mathbf{t}_i^l)\}_{i\in\mathcal{D}^l}$，作为类比推理的“已知概念库”。
3. **类比文本概念生成器（ATCG）** $\varphi_{\text{ATCG}}(\cdot)$：以未标记样本的图像嵌入为查询，从知识库中检索并重组已知文本概念，生成该样本的**类比文本嵌入** $\tilde{\mathbf{t}}_i$。这是整个框架的因果枢纽——它将类别发现从纯视觉匹配转变为视觉‑语义类比推理。
4. **融合头投影器** $g(\cdot)$：通过可学习系数 $\alpha$ 对视觉嵌入 $\mathbf{v}_i$ 和类比文本嵌入 $\tilde{\mathbf{t}}_i$ 进行加权融合，得到中间表示 $\mathbf{h}_i = \alpha \cdot \mathbf{v}_i + (1-\alpha) \cdot \tilde{\mathbf{t}}_i$，再投影到最终融合嵌入 $\mathbf{f}_i = g(\mathbf{h}_i)$，供下游对比学习与分类使用。

训练过程分为**两个阶段**（见 Figure 2）：

![[assets/figures/papers/paper_list_l2128_https_arxiv_org_abs_2603_19918/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the AL-GCD Framework. The framework consists of two stages: (1) ATCG training, where the ATCG is trained using labeled images and text embeddings to acquire the ability to generate meaningful analogical text embeddings for unlabeled samples; (2) GCD Training, where ATCG generates text embeddings for unlabeled samples, which are fused with visual embeddings through a fusion head to produce fusion embeddings. These embeddings are optimized via contrastive learning*

- **阶段一：ATCG 训练（伪 GCD 预训练）**。在已标记数据上构造伪未标记样本，训练 ATCG 学习从图像嵌入到对应文本嵌入的类比映射能力，损失函数为生成的文本嵌入与真实文本嵌入之间的余弦距离（类比损失 $\mathcal{L}_{\text{AL}}$）。此阶段冻结视觉和文本编码器，仅优化 ATCG 参数。
- **阶段二：GCD 训练**。冻结训练好的 ATCG，将其接入完整流水线。对每个未标记样本，ATCG 生成类比文本嵌入，与视觉嵌入融合后，通过无监督对比损失 $\mathcal{L}_{\text{rep}}^u$ 和参数化分类损失 $\mathcal{L}_{\text{cls}}$ 联合优化融合头及分类器。分类损失对有标签数据使用标准交叉熵，对无标签数据使用自蒸馏伪标签并辅以熵正则项 $\epsilon H(\overline{\mathbf{p}})$ 防止平凡解。

值得注意的是，ATCG 本身采用**初始层 + 堆叠层**的递进架构（Figure 3）：初始层通过跨模态注意力建立初步的视觉‑文本关联，堆叠层则迭代精化文本嵌入，使类比结果逐步对齐到目标样本的语义空间。消融实验证实，仅添加初始层已能带来显著增益，进一步增加堆叠层可继续提升新类别准确率，但会伴随已知类别准确率的轻微下降，呈现出可控的“已知‑未知”权衡。



### 整体框架与两阶段训练

AL‑GCD 框架由四个核心组件构成：视觉编码器 $f_v(\cdot)$、文本编码器 $f_t(\cdot)$、融合头投影器 $g(\cdot)$ 以及类比文本概念生成器 $\varphi_{\mathrm{ATCG}}(\cdot)$（Figure 2）。训练分为两个阶段：

1. **ATCG 训练阶段**：利用已标记数据训练类比文本概念生成器，使其获得为未标记样本生成有意义类比文本嵌入的能力。
2. **GCD 训练阶段**：冻结 ATCG，为所有未标记样本生成文本嵌入，通过融合头与视觉嵌入结合，在融合嵌入上进行对比学习和参数化分类。

### 视觉与文本嵌入提取

对于已标记样本 $(x_i^l, y_i^l)$，分别通过预训练的视觉编码器和文本编码器提取嵌入：

$$\mathbf{v}_i^l = f_v(x_i^l), \quad \mathbf{t}_i^l = f_t(\mathrm{text}(y_i^l))$$

其中 $\mathrm{text}(y_i^l)$ 是将类别标签转换为文本描述（如 “a photo of a [class]”）的函数。这些图像‑文本嵌入对被存入知识库 $\mathcal{K} = \{(\mathbf{v}_i^l, \mathbf{t}_i^l)\}_{i \in \mathcal{D}^l}$，供后续类比检索使用。

### 类比文本概念生成器（ATCG）

ATCG 是 AL‑GCD 的核心创新模块（Figure 3），其设计灵感来源于人类类比学习机制：人类通过回忆已知概念并将其与新观察关联，形成对新事物的理解。ATCG 模拟这一过程，从未标记样本的图像嵌入出发，在知识库中检索相似的已标记概念，通过类比注意力重组已知文本嵌入，生成未标记样本的文本概念嵌入。

![[assets/figures/papers/paper_list_l2128_https_arxiv_org_abs_2603_19918/figures/003_Figure_3.jpg]]
*Figure 3: Architecture of the Analogical Textual Concept Generator (ATCG), illustrating its input–output tensor structure*

**伪 GCD 训练中的类比生成**：在 ATCG 训练阶段，将已标记数据划分为伪已标记集 $\mathcal{D}_{\mathrm{P}}^l$ 和伪未标记集。对于伪未标记样本 $x_j^l$，ATCG 利用其图像嵌入 $\mathbf{v}_j^l$ 和伪已标记集的参考嵌入对，生成类比文本嵌入：

$$\tilde{\mathbf{t}}_j = \varphi_{\mathrm{ATCG}}\big(\mathbf{v}_j^l, \{\mathbf{v}_i\}_{i\in\mathcal{D}_{\mathrm{P}}^l}, \{\mathbf{t}_i\}_{i\in\mathcal{D}_{\mathrm{P}}^l}\big)$$

**类比损失**：通过最小化生成的文本嵌入与真实文本嵌入之间的余弦距离，训练 ATCG 的概念对齐能力：

$$\mathcal{L}_{\mathrm{AL}} = \frac{1}{n}\sum_{j=1}^{n}\big(1 - \frac{\tilde{\mathbf{t}}_j \cdot \mathbf{t}_j^{l^{T}}}{\Vert\tilde{\mathbf{t}}_j\Vert \cdot \Vert\mathbf{t}_j^l\Vert}\big)$$

**堆叠层精化**：ATCG 由初始层（TIAA）和多个堆叠层（TSA + TIAA）构成。在堆叠层中，跨模态注意力机制迭代精化文本嵌入：

$$\tilde{\mathbf{t}}_j^{n} = \mathrm{softmax}\big(\frac{Q_{\mathrm{TIAA}} \cdot K_{\mathrm{TIAA}}^T}{\sqrt{2d}}\big) \cdot V_{\mathrm{TIAA}}$$

其中 $Q_{\mathrm{TIAA}} = \mathrm{Concat}[\tilde{\mathbf{t}}_j^{\mathrm{TSA}}, \mathbf{v}_j^u]$ 将 TSA 精化后的文本嵌入与未标记图像嵌入拼接作为查询，$K_{\mathrm{TIAA}} = \mathrm{Concat}[\{\mathbf{t}_i^l\}_{i\in\mathcal{D}^l}, \{\mathbf{v}_i^l\}_{i\in\mathcal{D}^l}]$ 将所有已标记文本和图像嵌入拼接作为键。通过 $n$ 层迭代，ATCG 计算未标记与已标记样本之间的类比相似度，重组已知文本概念，生成对齐的文本嵌入。

### 视觉‑文本融合

在 GCD 训练阶段，对于每个样本 $x_i$，将其视觉嵌入 $\mathbf{v}_i$ 与 ATCG 生成的类比文本嵌入 $\tilde{\mathbf{t}}_i$ 通过系数 $\boldsymbol{\alpha}$ 加权融合，得到中间融合表示：

$$\mathbf{h}_i = \boldsymbol{\alpha} \cdot \mathbf{v}_i + (1-\boldsymbol{\alpha}) \cdot \tilde{\mathbf{t}}_i$$

随后通过融合头投影器映射到最终融合嵌入空间：

$$\mathbf{f}_i = g(\mathbf{h}_i)$$

融合系数 $\alpha$ 控制视觉与文本信息的贡献比例：较高的 $\alpha$ 有利于已知类别识别，但可能削弱新类别发现能力；$\alpha=0.4$ 在二者之间取得良好平衡（Figure 4）。

### 对比学习与分类损失

在融合嵌入 $\mathbf{f}_i$ 上施加无监督对比损失，使同一样本的不同增强视图表示接近：

$$\mathcal{L}_{\mathrm{rep}}^u = -\frac{1}{|B|}\sum_{i\in B}\log\frac{\exp(\mathbf{f}_i \cdot \mathbf{f}_i'/\tau)}{\sum_{j\ne i}\exp(\mathbf{f}_i \cdot \mathbf{f}_j/\tau)}$$

参数化分类损失包含有监督和无监督两部分。对有标签数据使用标准交叉熵 $\mathcal{L}_{\mathrm{cls}}^s = \frac{1}{|B_l|}\sum_{i\in B_l} \mathcal{H}(y_i, p_i)$；对无标签数据使用自蒸馏生成的伪标签并添加熵正则项，防止所有样本被分配到单一类别：

$$\mathcal{L}_{\mathrm{cls}}^u = \frac{1}{|B|}\sum_{i\in B} \mathcal{H}(q_i', p_i) - \epsilon H(\overline{\mathbf{p}})$$

其中 $\overline{\mathbf{p}} = \frac{1}{2|B|}\sum_{i\in B}(\mathbf{p}_i + \bar{\mathbf{p}_i'})$ 是一个批次内预测的均值，$H(\overline{\mathbf{p}}) = -\sum_k \overline{\mathbf{p}}^{(k)}\log\overline{\mathbf{p}}^{(k)}$ 为其熵。最终分类损失为 $\mathcal{L}_{\mathrm{cls}} = (1-\lambda)\mathcal{L}_{\mathrm{cls}}^u + \lambda\mathcal{L}_{\mathrm{cls}}^s$，总训练目标为 $\mathcal{L} = \mathcal{L}_{\mathrm{rep}} + \mathcal{L}_{\mathrm{cls}}$。

### 补充图表

![[assets/figures/papers/paper_list_l2128_https_arxiv_org_abs_2603_19918/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of an example of human Analogical Learning mechanism and the proposed Analogical Textual Concept Generator (ATCG)*



## 实验与关键发现

### 主实验结果

AL‑GCD 在六个基准数据集上进行了全面评估，涵盖通用分类数据集（CIFAR‑100、ImageNet‑100）和四个细粒度数据集（CUB、Stanford Cars、FGVC‑Aircraft、Herbarium 19）。实验采用 CLIP 视觉编码器作为骨干网络，与现有 GCD 方法进行系统对比。

**Table 1** 展示了在已知类别数 $K$ 未知设定下的详细结果。在最具挑战性的 CUB 数据集上，AL‑GCD 结合 SelEx‑CLIP 达到 84.1% 整体准确率（Old 79.7%，New 86.3%），显著超越先前最佳方法。相较于 CMS‑CLIP，AL‑GCD 在 CUB 上实现 +8.1% 整体提升（Old +5.1%，New +9.7%），表明类比文本概念生成器在细粒度视觉场景中具有突出的语义分离能力。

**Table 2** 汇总了各方法在细粒度平均、分类平均和全数据集平均三个维度上的表现。AL‑GCD 在所有数据集上的平均整体准确率提升 **+5.0%**，在细粒度数据集上平均提升 **+7.1%**。这一结果验证了核心洞察：将类别发现从纯视觉过程转变为视觉‑文本推理过程，能够显著增强类别语义分离能力，尤其在视觉相似但语义不同的细粒度场景下效果突出。

### 消融实验

消融研究系统考察了 ATCG 各组件的贡献以及关键超参数的影响。

**ATCG 组件消融**（Table 3）：实验对比了仅使用初始层（TIAA）、仅使用堆叠层（TSA+TIAA）以及完整 ATCG 的配置。结果表明，仅添加 TIAA 初始层已能带来性能提升，进一步引入堆叠层可提供额外增益，证实了迭代类比推理机制的有效性。

**ATCG 层数消融**（Table 4）：在 CIFAR‑100 上，将 ATCG 层数从 0 增加到 4 时，新颖类别准确率从 75.2% 提升至 86.8%（+11.6%），整体准确率同步增长。但已知类别准确率出现轻微下降，揭示了“已知‑未知”权衡：更深的类比推理有利于发现新类别，但可能对已知类别的识别产生轻微负面影响。6 层时性能趋于平台，表明 4 层在效果与效率间取得较好平衡。

**融合系数 $\alpha$ 消融**（Figure 4）：在 Stanford Cars 上考察了视觉‑文本融合权重 $\alpha$ 的影响。$\alpha$ 控制融合嵌入中视觉特征的占比（$\mathbf{h}_i = \alpha \cdot \mathbf{v}_i + (1-\alpha) \cdot \tilde{\mathbf{t}}_i$）。当 $\alpha$ 从 0.4 增至 0.7 时，已知类别准确率上升 1.8%，但新颖类别准确率下降。$\alpha=0.4$ 在已知和新颖类别间取得最佳平衡，验证了文本概念对新颖类别发现的关键作用。

### 失败模式与局限性

尽管 AL‑GCD 在整体和细粒度场景下均取得显著提升，仍存在以下局限：

1. **已知‑未知权衡**：增加 ATCG 层数时，已知类别准确率可能出现平台或轻微下降，表明优化偏向新类别可能对已知类别识别产生轻微负面影响。这一权衡在 Table 4 和 Figure 4 中均有体现。

![[assets/figures/papers/paper_list_l2128_https_arxiv_org_abs_2603_19918/figures/008_Table_4.jpg]]
*Table 4: Ablation study on the number of ATCG layers*

![[assets/figures/papers/paper_list_l2128_https_arxiv_org_abs_2603_19918/figures/007_Figure_4.jpg]]
*Figure 4: Ablation study of the α on Stanford Cars*

2. **语义源受限**：当前仅使用 CLIP 文本编码器从类别标签生成文本嵌入，尚未整合更强大的大型语言模型或更丰富的语义描述，可能限制了类比推理的表达能力。

3. **静态设定局限**：实验仅在静态 GCD 设定下进行，未在持续学习或开放世界发现等更复杂的动态场景中验证方法的鲁棒性和泛化能力。

### 关键图表结论

- **Table 1**：AL‑GCD 在多个数据集上一致超越现有方法，细粒度场景优势尤为突出。
- **Table 2**：全数据集平均提升 +5.0%，细粒度平均提升 +7.1%，验证跨模态类比推理的通用有效性。
- **Table 3 & Table 4**：ATCG 的初始层和堆叠层均有正向贡献，4 层配置在性能与效率间取得最优平衡。
- **Figure 4**：$\alpha=0.4$ 在已知与新类别准确率间取得最佳权衡，证实文本概念对新类别发现的核心价值。

![[assets/figures/papers/paper_list_l2128_https_arxiv_org_abs_2603_19918/figures/004_Table_1.jpg]]
*Table 1: Comparison with the state of the art on GCD. The best results are in bold, the second best are underlined. † denotes reproduced results. △ denotes results from the CMS Appendix [6]*

![[assets/figures/papers/paper_list_l2128_https_arxiv_org_abs_2603_19918/figures/005_Table_2.jpg]]
*Table 2: Comparison on Fine-grained Avg, Classification Avg, and All Datasets Avg with CLIP backbone. The best values are in bold and the second best are underlined. † denotes reproduced results. △ denotes results from the CMS appendix [6]*

![[assets/figures/papers/paper_list_l2128_https_arxiv_org_abs_2603_19918/figures/006_Table_3.jpg]]
*Table 3: Ablation study results for ATCG with various initial and stacked layer settings across different datasets*



## 定位与知识库关联

### 问题定位与瓶颈

AL‑GCD 面向广义类别发现（Generalized Category Discovery, GCD）问题：给定部分已标记样本，要求模型同时识别已知类别并发现未知类别。现有 GCD 流水线主要依赖视觉特征，监督学习与新类别发现之间的耦合松散，导致先验知识无法有效迁移到未标记数据，在视觉相似但语义不同的细粒度类别上边界脆弱。

### 与基线方法的关系

AL‑GCD 的方法谱系可沿两条轴线梳理：纯视觉 GCD 方法与引入文本模态的 CLIP‑based GCD 方法。

**纯视觉 GCD 基线。** **GCD**（Vaze et al., CVPR 2022）首次形式化 GCD 问题，基于对比学习区分已知与未知类别。**SimGCD**（Wen et al., ICCV 2023）引入参数化分类器与原型分类，将自蒸馏机制用于无标签数据。**CMS**（Choi et al., CVPR 2024）提出对比均值平移学习，增强特征表征的类间分离能力。这些方法的共同局限在于仅利用视觉信号，缺乏语义层面的类别概念引导。

**CLIP‑based GCD 基线。** **CPT**（Yang et al., IJCV 2025）基于 CLIP 进行一致性提示调优，将视觉‑语言预训练知识引入 GCD。**GET**（Wang et al., CVPR 2025）采用双分支架构联合学习视觉与文本分支。**SelEx**（Rastegar et al., ECCV 2024）面向细粒度 GCD 设计自适应专家选择机制。这些方法虽然利用了 CLIP 的跨模态能力，但文本分支主要服务于已知类别的分类，未为未标记样本显式生成语义概念。

AL‑GCD 的核心推进在于将 GCD 从“视觉匹配”转变为“视觉‑文本类比推理”：通过类比文本概念生成器（ATCG），从已标记知识库中检索相关概念，为每个未标记样本生成类比文本嵌入，再与视觉特征融合。这一范式转变使模型在细粒度场景下获得显著的语义分离增益。

### 适用边界

1. **依赖 CLIP 文本编码器。** ATCG 生成的文本嵌入质量受限于 CLIP 文本编码器的语义表达能力。对于 CLIP 预训练中覆盖不足的领域（如高度专业化的医学图像），类比概念的语义准确性可能下降。
2. **静态 GCD 设定。** 当前方法仅在标准静态 GCD 设定下验证，即所有未标记数据一次性可用。在持续学习或开放世界发现等动态场景中，知识库需要增量更新，ATCG 的类比机制能否有效应对分布漂移尚待验证。
3. **已知‑未知权衡。** 消融实验表明，增加 ATCG 层数以增强类比能力时，已知类别准确率可能出现平台或轻微下降（Table 4），存在微小的“已知‑未知”权衡，需根据应用场景调整层数。

### 局限与开放问题

**已确认局限：**

- 增加 ATCG 层数时，已知类别准确率可能平台或轻微下降，显示优化偏向新类别可能对已知类别识别产生轻微负面影响（Table 4）。
- 当前仅使用 CLIP 文本编码器生成文本嵌入，尚未整合更强大的大型语言模型或更丰富的语义来源。
- 实验仅在静态 GCD 设置下进行，未在持续学习或开放世界发现等更复杂的动态场景中验证。

**开放问题：**

- 如何设计更具表达力的类比推理机制，以进一步提升细粒度类别的分离能力？
- 如何将大规模语言模型等更丰富的语义源无缝集成到 ATCG 框架中？
- 如何将类比学习范式扩展到持续学习和开放世界发现场景，以应对数据分布漂移？



## 原文 PDF

![[paperPDFs/CVPR_2026/Learning_Like_Humans_Analogical_Concept_Learning_for_Generalized_Category_Discovery.pdf]]
