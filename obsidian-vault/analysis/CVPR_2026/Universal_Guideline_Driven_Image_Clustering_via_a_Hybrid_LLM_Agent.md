---
title: Universal Guideline-Driven Image Clustering via a Hybrid LLM Agent
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Universal_Guideline_Driven_Image_Clustering_via_a_Hybrid_LLM_Agent.pdf
project_link: "https://clustering-agent.github.io/"
code_link: null
aliases:
- GDICAGMT
- UGDICHLA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用多模态大模型将图像转化为指南驱动的概念代理文本描述，使聚类标准与视觉特征解耦；配合指令感知文本嵌入，实现训练无关的属性组合与语义聚焦，是多场景适应性提升的关键因果操作。
primary_logic: 通过生成式概念代理建模（GCPM）将图像转化为聚焦指定属性的描述，再编码为解耦嵌入，并借助基于最小生成树的LLM遍历算法仅在必要时进行语义合并，实现了训练无关、高效、跨任务通用的指南驱动图像聚类。
claims:
- GCPM‑G with K‑Means 在 ImageNet‑10 上达到 98.8% ACC，超越最佳训练基线 1.6% (Table 2)。
- MST Traversal 将 ImageNet‑10 的 ARI 从 0.3 提升至 72.1 (Table 2)。
- 概念代理描述（GCPM captions）相比直接图像嵌入，在多个数据集上一贯提升聚类精度 (Table 7)。
- MST Traversal 在保持高精度的同时大幅提升召回率，B‑Prec. 与 B‑Rec. 对比见 Table 6。
---

# Universal Guideline-Driven Image Clustering via a Hybrid LLM Agent

> [!tip] 核心洞察
> 通过生成式概念代理建模（GCPM）将图像转化为聚焦指定属性的描述，再编码为解耦嵌入，并借助基于最小生成树的LLM遍历算法仅在必要时进行语义合并，实现了训练无关、高效、跨任务通用的指南驱动图像聚类。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于混合LLM智能体的通用指南驱动图像聚类 |
| 英文题名 | Universal Guideline-Driven Image Clustering via a Hybrid LLM Agent |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhong_Universal_Guideline-Driven_Image_Clustering_via_a_Hybrid_LLM_Agent_CVPR_2026_paper.html) · [Project](https://clustering-agent.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Guideline-Driven Image Clustering Agent (GCPM + MST Traversal) |
| Dataset | ImageNet-10, CIFAR-10, STL-10, Fruit |

> [!tip] 效果简介
> - ImageNet-10 上，ACC 98.8 (GCPM‑G + K‑Means) vs 97.2 (IDCTCL) (+1.6)。
> - CIFAR-10 上，ACC 94.1 (GCPM‑G + K‑Means) vs 93.4 (LFSS) (+0.7)。
> - STL-10 上，ACC 98.8 (GCPM‑G + K‑Means) vs 97.4 (IC|TC) (+1.4)。

## 概要

图像聚类是视觉理解的基础任务，但现有方法面临一个根本性瓶颈：不同聚类场景（通用聚类、细粒度聚类、多准则聚类、长尾分布聚类）之间的任务差异导致方法高度碎片化，无法以统一、训练无关的方式灵活组合多种语义指南。传统基于视觉嵌入的方法难以解耦指南中隐含的复杂属性，导致视觉上相关但语义上无关的特征主导聚类结果，严重限制了跨场景的泛化能力。

针对这一问题，本文提出**Guideline-Driven Image Clustering Agent**——首个通用的指南驱动图像聚类框架。其核心洞察在于：通过**生成式概念代理建模（GCPM）**，利用多模态大语言模型（MLLM）将图像转化为聚焦于指定语义属性的文本描述，再经由指令感知嵌入模型编码为解耦的语义嵌入，从而将聚类标准与视觉特征解耦，实现训练无关的属性组合与语义聚焦。在此基础上，**基于最小生成树的LLM遍历算法（MST Traversal）**仅在必要时对初始聚类结果进行语义合并查询，大幅减少昂贵的LLM调用次数，同时显著提升召回率。

该方法在多个基准上取得领先性能：在ImageNet-10上，GCPM-G配合K-Means达到98.8%的聚类准确率（ACC），超越最佳训练基线IDCTCL（Liu et al., NeurIPS 2024）1.6个百分点；在CIFAR-10和STL-10上也分别以94.1%和98.8%的ACC取得最优结果。在多准则聚类场景中，Fruit数据集按颜色准则的NMI达到99.9%，超越Multi-Sub（Yao et al., CVPR 2024）1.4个百分点。在长尾分布的ABO-LC数据集上，MST Traversal将HDBSCAN的ARI从28.2大幅提升至51.5，提升幅度达23.3个点。消融实验进一步验证，概念代理描述相比直接图像嵌入在多个数据集上一致提升聚类精度，MST Traversal在保持高精度的同时大幅提升召回率，且LLM调用数量远低于样本数量，验证了方法的效率与有效性。

在方法谱系上，该工作区别于需要针对特定指南重新训练的深度聚类方法（如SCAN, Van Gansbeke et al., ECCV 2020；IDCTCL, Liu et al., NeurIPS 2024），也与仅支持单一文本条件的训练无关方法（如IC|TC, Kwon et al., arXiv 2023）形成对比。其训练无关、可即时切换多标准指南的特性，以及通过LLM混合推理实现自动簇数发现的机制，为图像聚类提供了一种灵活、高效且通用的新范式。

图像聚类旨在根据语义相似性自动将图像分组，是计算机视觉领域的基础任务。传统聚类方法通常依赖单一、隐式的语义标准，例如将“金毛犬”和“哈士奇”归为“狗”这一粗粒度类别。然而，现实世界的聚类需求远比这复杂——用户可能希望按“颜色”“材质”“品种”“使用场景”等不同指南对同一批图像进行划分，且这些指南往往需要灵活组合。这催生了**指南驱动图像聚类（Guideline-Driven Image Clustering）** 这一新范式。

### 现有方法的碎片化困境

当前图像聚类研究存在显著的碎片化问题。方法通常针对单一场景设计：**SCAN**（Van Gansbeke et al., ECCV 2020）和 **IDCTCL**（Liu et al., NeurIPS 2024）专注于通用聚类；**DiFiC**（Yang et al., arXiv 2024）面向细粒度聚类；**Multi-Sub**（Yao et al., CVPR 2024）尝试处理多标准聚类，但仍需针对每种新指南重新训练。**IC|TC**（Kwon et al., arXiv 2023）虽以训练无关的方式利用文本条件，却难以解耦指南中的复杂属性组合。

这些方法的根本瓶颈在于：**图像嵌入与语义指南的耦合过于紧密**。传统视觉编码器（如ResNet）提取的特征是“扁平”的——它们无法区分“形状”和“颜色”等不同属性维度。当指南要求按“花色”而非“点数”对扑克牌聚类时，视觉上更显著的数字布局会主导嵌入空间，导致聚类结果偏离用户意图。

### 核心动机：训练无关的统一框架

本文的动机源于一个关键观察：**多模态大模型（MLLM）具备将视觉内容转化为聚焦特定属性的文本描述的能力**。这一能力天然适合解耦指南中的复杂语义——MLLM可以“看”到一张扑克牌，并按指令只描述其“花色”而忽略“点数”。若能系统性地利用这种能力，就有望构建一个训练无关、可即时切换多标准的通用聚类框架。

具体而言，本文试图回答三个核心问题：
1. 如何将任意语义指南高效地注入图像嵌入，而无需针对每种指南重新训练？
2. 如何在未知簇数的情况下自动发现聚类结构，同时避免昂贵的逐样本LLM调用？
3. 如何使同一框架同时覆盖通用聚类、细粒度聚类、多标准聚类和长尾聚类等异构场景？

这些问题的解决将使得图像聚类从“单一标准、训练依赖”的范式转向“多标准、零训练”的新范式，显著降低实际部署的门槛。

## 核心方法与创新机理

本文的核心创新在于提出了一套**训练无关的混合LLM智能体框架**，首次实现以文本指南为统一接口的通用图像聚类。其关键因果操作体现在两个紧密协同的**changed slots**上，分别解决了现有方法在语义解耦与自适应聚类后处理上的根本瓶颈。

### 1. 语义解耦：从视觉嵌入到生成式概念代理建模（GCPM）

**瓶颈与因果机制。** 传统聚类方法直接对原始图像编码（如ResNet嵌入），导致视觉相关但语义无关的特征（如背景、纹理、布局）主导聚类结果，无法解耦指南中指定的复杂属性。例如，在按花色聚类扑克牌时，视觉嵌入会因牌面数字的视觉显著性而错误地将相同数字而非相同花色的牌聚在一起（见Figure 4）。GCPM通过**生成式概念代理**切断这一纠缠：先利用多模态大模型（MLLM）将图像转化为聚焦于指南属性的文本描述，再通过指令感知文本嵌入模型编码为语义向量。这一“图像→文本→嵌入”的间接路径，使得聚类标准从视觉特征中解耦，实现了对指南属性的精准聚焦。

**与基线的本质差异。** 现有训练相关方法（如**SCAN** (Van Gansbeke et al., ECCV 2020)、**IDCTCL** (Liu et al., NeurIPS 2024)）需针对每种聚类标准重新训练模型，而训练无关方法（如**IC|TC** (Kwon et al., arXiv 2023)）仅支持单一文本条件。GCPM则通过可即时切换的文本指南，无需任何训练即可组合多种语义属性，从根本上改变了特征表示与语义嵌入的构建方式。

**证据强度。** Table 7的消融实验证实，概念代理描述相比直接使用图像嵌入，在多个数据集上一致提升聚类精度。在扑克牌数据集的解耦测试中（Figure 4），GCPM-E（纯文本概念代理）成功按花色聚类，而基于图像嵌入的GME-Qwen则完全失败，直接验证了概念代理对视觉纠缠场景的关键作用。

### 2. 自适应合并：基于最小生成树的LLM遍历算法

**瓶颈与因果机制。** 传统密度聚类（如HDBSCAN）仅基于嵌入空间距离，倾向于产生大量语义一致但过度分裂的小簇，无法自动合并语义相同但嵌入距离较远的簇。朴素方案是让LLM对所有簇对进行合并判断，但调用成本与簇数平方成正比，不可行。本文提出的**MST遍历算法**将这一决策空间压缩至$O(M \log M)$：先对初始簇构建最小生成树（MST），再按Ward距离升序遍历边，仅对相邻且语义模糊的簇对查询LLM。这一设计将LLM的深度语义推理仅用于必要的模糊决策，大幅减少了调用次数。

**与基线的本质差异。** 传统HDBSCAN后处理（如密度阈值调整）缺乏语义理解能力，无法判断“外观差异大但语义相同”的簇是否应合并。MST遍历通过引入LLM的指南感知语义推理，从根本上改变了聚类后处理与适应机制，在保持高精度的同时大幅提升召回率。

**证据强度。** Table 6显示，MST遍历将ImageNet-10上HDBSCAN的B-Recall从极低水平提升至与精度匹配的水平，同时B-Precision几乎无损。Table 8进一步验证了效率：LLM调用次数远低于样本数量，例如在ImageNet-10上仅需数百次调用处理13,000个样本。在ABO-LC长尾电商数据集上（Table 5），MST遍历将ARI从28.2提升至51.5（+23.3），证明了其在复杂真实场景中的有效性。

### 创新协同效应

上述两个changed slots并非孤立改进，而是形成因果闭环：GCPM提供的解耦嵌入为MST遍历提供了高质量的语义距离基础，使得MST上的Ward距离能够更准确地反映指南相关的簇间相似性；而MST遍历则弥补了GCPM嵌入在细粒度语义区分上的残余模糊性。两者协同实现了**训练无关、指南驱动、跨任务通用**的图像聚类范式，覆盖从通用聚类到细粒度聚类、从全局准则到局部准则、从平衡分布到长尾分布的全场景（Figure 1）。

本文提出首个**通用指南驱动图像聚类框架**，其核心设计目标是解决现有方法因任务碎片化而无法以统一、训练无关的方式组合多种语义指南的瓶颈。如图1所示，框架将任意图像聚类需求抽象为文本指南 $G$ 驱动的统一范式：给定样本集 $X$ 和指南 $G$，输出符合该指南的聚类结果 $\mathcal{C} = f(G, X)$（Eq.1）。这一范式覆盖了从通用聚类到细粒度聚类、从全局准则到局部准则、从均衡分布到长尾分布的多种场景。

框架由两大核心模块串联构成，如图2所示：

**1. 生成式概念代理建模（Generative Concept Proxy Modeling, GCPM）**  
该模块负责将图像转化为指南驱动的语义嵌入，是使聚类标准与视觉特征解耦的关键因果操作。其流程为：
- **概念代理描述生成**：利用多模态大模型（MLLM）作为描述器 $f_{caption}$，根据指南 $A \subseteq G$ 从图像 $x_i$ 中提取聚焦于指定属性的文本描述 $c_i = f_{caption}(A, x_i)$（Eq.2）。这些描述充当图像的“概念代理”，显式地表达与聚类准则相关的语义，从而剥离视觉中无关但占主导的特征。
- **指令感知嵌入编码**：使用指令感知文本嵌入模型 $f_{embed}$ 将概念代理描述编码为语义嵌入 $h_i = f_{embed}(\mathcal{S}, c_i)$（Eq.3），其中 $\mathcal{S} \subseteq \mathcal{G}$ 指定聚类关注点。该嵌入直接支持后续的标准聚类算法 $\mathcal{C} = \mathrm{Clustering}(H)$（Eq.4）。

GCPM 的训练无关特性使其可即时切换不同指南，无需针对新准则重新训练，这是其多场景适应性的基础。

**2. 基于最小生成树的 LLM 遍历（MST-based LLM Traversal）**  
当簇数未知时，框架采用 HDBSCAN 对 GCPM 嵌入进行初始聚类 $\mathcal{C} = \mathrm{HDBSCAN}(H)$（Eq.5）。然而 HDBSCAN 倾向于产生一致但过度碎片化的小簇，难以合并语义同质的簇。为此，MST Traversal 引入混合策略：
- **MST 构建**：计算簇间 Ward 距离 $d(C_1, C_2)$（Eq.6），构建最小生成树 $T = \mathbf{MST}(D)$（Eq.7），优先连接嵌入空间中最接近的簇对。
- **选择性 LLM 合并**：沿 MST 边迭代查询 LLM 进行二值合并决策 $p = f_{merge}(G, C_i, C_j)$（Eq.8），仅在嵌入距离无法可靠判定语义同质性时才调用 LLM 推理。这种“嵌入负责常规决策、LLM 负责模糊语义决策”的混合设计，大幅减少了昂贵的 LLM 调用次数。

**输入输出流**：对于未提供显式指南的场景，框架首先利用 LLM 通过启发式提示自动生成聚类指南。随后，图像经 GCPM 转化为指南感知嵌入，输入 K-Means（已知簇数）或 HDBSCAN（未知簇数）进行初始聚类；若使用 HDBSCAN，则进一步经 MST Traversal 进行语义合并，输出最终聚类结果。

![[assets/figures/papers/paper_list_l2427_https_openaccess_thecvf_com_content_CVPR2026_html_Zhong_Universal_Guidel/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our Guideline-Driven Clustering Agent. We introduce the first universal clustering framework that handles diverse image clustering scenarios through textual guidelines, spanning from general to fine-grained tasks, from global to local criteria, and from balanced to long-tail distributions. Our training-free hybrid agent flexibly adapts across these diverse clustering requirements*

### 问题形式化

给定一组图像样本 $X = \{x_1, x_2, \dots, x_N\}$ 和一条语义聚类指南 $G$（如“按动物种类聚类”或“按产品颜色聚类”），目标是将样本划分为 $K$ 个簇 $\mathcal{C} = \{C_1, C_2, \dots, C_K\}$：

$$\mathcal{C} = f(G, X)$$

其中 $f$ 表示整个聚类过程。该形式化将聚类从固定的相似度函数中解放出来，使聚类标准由文本指南显式定义。

### 生成式概念代理建模（GCPM）

GCPM 是框架的核心嵌入模块，解决传统视觉嵌入无法根据指南解耦属性的瓶颈。其关键因果操作是：**先将图像转化为聚焦于指定属性的文本描述，再对文本编码**，从而绕过图像中视觉纠缠问题。

**概念代理描述生成**。使用多模态大语言模型（MLLM）作为描述生成器 $f_{caption}$，在指南子集 $A \subseteq G$ 的条件下为每张图像 $x_i$ 生成概念代理描述 $c_i$：

$$c_i = f_{caption}(A, x_i), \quad A \subseteq G$$

描述内容仅保留与指南相关的语义属性，显式忽略无关视觉特征。例如，当指南为“按花色分组”时，描述聚焦于花色而忽略卡牌数字。

**指令感知嵌入编码**。使用指令感知文本嵌入模型 $f_{embed}$ 将概念代理描述编码为语义嵌入 $h_i$：

$$h_i = f_{embed}(\mathcal{S}, c_i), \quad \mathcal{S} \subseteq \mathcal{G}$$

其中 $\mathcal{S}$ 指定聚类关注焦点（如“关注物体类别”），$\mathcal{G}$ 为指令空间。嵌入模型基于描述文本而非原始图像进行编码，天然实现属性解耦。

**聚类应用**。对嵌入集合 $H = \{h_1, \dots, h_N\}$ 应用标准聚类算法：

$$\mathcal{C} = \mathrm{Clustering}(H)$$

当簇数已知时使用 K‑Means，未知时使用 HDBSCAN。

### 基于 MST 的 LLM 遍历算法

HDBSCAN 在嵌入空间中倾向于生成一致的小簇，但难以将语义同质的簇合并为更大分组。MST 遍历算法通过在嵌入距离结构上选择性查询 LLM 来解决此问题。

**初始聚类与距离定义**。首先对嵌入 $H$ 应用 HDBSCAN 获得初始簇：

$$\mathcal{C} = \mathrm{HDBSCAN}(H)$$

定义任意两个簇 $C_1, C_2$ 之间的 Ward 距离：

$$d(C_1, C_2) = \frac{|C_1| \cdot |C_2|}{|C_1| + |C_2|} \| m_{C_1} - m_{C_2} \|^2$$

其中 $m_{C_1}, m_{C_2}$ 为簇的嵌入质心，$|\cdot|$ 为簇大小。Ward 距离同时考虑簇大小和质心分离度，优先合并小而近的簇。

**最小生成树构建**。基于成对 Ward 距离矩阵 $D$ 构建最小生成树 $T$：

$$T = \mathbf{MST}(D)$$

MST 的边连接了嵌入空间中最相似的簇对，为遍历合并提供结构化的候选顺序。

**LLM 选择性合并**。沿 MST 边遍历，对每条边 $(C_i, C_j)$ 查询 LLM 判断是否合并：

$$p = f_{merge}(G, C_i, C_j), \quad \forall (C_i, C_j) \in T$$

$f_{merge}$ 根据指南 $G$ 返回二值决策 $p \in \{0, 1\}$。该设计的关键效率优势在于：LLM 仅在语义模糊的簇对上被调用，而非对所有样本对进行判断。实验表明 LLM 调用次数远低于样本数量（Table 8），验证了选择性调用的有效性。

## 实验与关键发现

### 通用聚类性能

本文在三个标准聚类基准（CIFAR‑10、STL‑10、ImageNet‑10）上评估通用聚类性能。遵循主流设定，在已知簇数条件下采用 GCPM‑G + K‑Means，在未知簇数条件下采用 GCPM‑G + HDBSCAN + MST 遍历。Table 2 汇总了与代表性训练基线的对比结果。

![[assets/figures/papers/paper_list_l2427_https_openaccess_thecvf_com_content_CVPR2026_html_Zhong_Universal_Guidel/figures/005_Table_2.jpg]]
*Table 2: Performance comparison on general clustering. Baselines assume known number of clusters. KMS.: K-Means; HDBS.: HDBSCAN. Max ∆↑ measures improvements of MST Traversal*

**已知簇数设定。** GCPM‑G + K‑Means 在所有三个数据集上均取得最优 ACC。在 ImageNet‑10 上达到 98.8%，超越此前最佳训练基线 IDCTCL（Liu et al., NeurIPS 2024）的 97.2%，提升 1.6 个百分点；在 STL‑10 上以 98.8% 超越 IC|TC（Kwon et al., arXiv 2023）的 97.4%；在 CIFAR‑10 上以 94.1% 超越 LFSS 的 93.4%。这一一致提升表明，通过生成式概念代理建模将图像转化为指南驱动的文本描述，再编码为语义嵌入，能够有效解耦视觉特征与聚类标准，使聚类结果更聚焦于指定语义。

**未知簇数设定。** 当簇数未知时，HDBSCAN 直接应用于 GCPM‑G 嵌入的 ACC 显著下降（例如 ImageNet‑10 仅 0.3%），暴露出 HDBSCAN 倾向于将同质样本过度分割为大量小簇的固有问题。引入 MST 遍历后，ImageNet‑10 的 ACC 跃升至 72.1%，ARI 从接近零提升至 72.1，验证了基于最小生成树的 LLM 选择性合并策略在自动发现簇数场景下的关键作用。

**与训练无关基线的对比。** 同为训练无关方法的 IC|TC 在已知簇数设定下具有竞争力，但其依赖文本条件的直接嵌入，无法像 GCPM 那样灵活组合多语义指南。GCPM 的核心优势在于其训练无关的指南驱动范式：无需针对新任务重新训练，仅通过切换文本指南即可适配不同聚类标准。

### 多标准聚类性能

多标准聚类要求同一图像集在不同语义指南下产生不同的分组结果。Table 3 报告了在 Fruit、Cards 和 CIFAR10‑MC 三个数据集上的平均性能。GCPM‑G + K‑Means 在 Fruit 的颜色准则下取得 99.9% NMI，超越多标准基线 Multi‑Sub（Yao et al., CVPR 2024）的 98.5%；在 Cards 的形状准则下同样表现优异。关键因果机制在于 GCPM 的概念代理描述显式提取指南指定的属性，指令感知嵌入模型进一步将描述编码为与该属性对齐的语义向量，从而抑制了视觉上显著但语义无关的特征对聚类结果的干扰。

![[assets/figures/papers/paper_list_l2427_https_openaccess_thecvf_com_content_CVPR2026_html_Zhong_Universal_Guidel/figures/006_Table_3.jpg]]
*Table 3: Performance comparison on multiple clustering, criteria, and metrics with averaged results per dataset. Baselines compared all assume known number of clusters. KMS.: K-Means; HDBS.: HDBSCAN. Max ∆↑ measures improvements of MST Traversal*

### 细粒度与长尾聚类

细粒度聚类（CUB Birds、Stanford Cars、Stanford Dogs、Oxford Flowers）和长尾电商聚类（ABO‑LC）进一步检验了方法的鲁棒性。Table 4 显示，在细粒度场景下，GCPM‑G + K‑Means 在 Stanford Cars 上取得 62.0% ACC，超越细粒度基线 DiFiC（Yang et al., arXiv 2024）的 60.7%。Table 5 中，ABO‑LC 数据集包含 10,756 个产品，78.7% 的簇仅含两个或更少样本（Table 1, Figure 3），呈现极端长尾分布。GCPM‑E + HDBSCAN + MST 遍历取得 51.5% ARI，相比纯 HDBSCAN 的 28.2% 提升 23.3 个百分点，验证了 MST 遍历在长尾、簇数未知场景下的大幅召回率增益。

![[assets/figures/papers/paper_list_l2427_https_openaccess_thecvf_com_content_CVPR2026_html_Zhong_Universal_Guidel/figures/008_Table_4.jpg]]
*Table 4: Comparison on fine-grained clustering. Baselines except UFCL assume known cluster number. KMS.: K-Means; HDBS.: HDBSCAN. Max ∆↑ measures improvements of MST Traversal*

![[assets/figures/papers/paper_list_l2427_https_openaccess_thecvf_com_content_CVPR2026_html_Zhong_Universal_Guidel/figures/009_Table_5.jpg]]
*Table 5: Comparison on ABO-LC. Baseline IC|TC is based on known number of clusters. KMS.: K-Means; HDBS.: HDB-SCAN. Max ∆↑ measures improvements of MST Traversal*

### 消融研究

**MST 遍历的精度‑召回权衡。** Table 6 报告了 MST 遍历前后的 B‑Cubed 精度与召回率。在所有数据集上，MST 遍历在保持高精度的同时大幅提升召回率。例如在 ImageNet‑10 上，B‑Prec. 从 95.1 微降至 93.4，而 B‑Rec. 从 5.8 跃升至 69.7，验证了 LLM 仅对模糊语义边界进行选择性合并的设计有效避免了过度合并导致的精度崩塌。

**概念代理描述的关键作用。** Table 7 对比了不同描述策略对 K‑Means 聚类 ACC 的影响。使用 GCPM 概念代理描述（GCPM captions）相比直接使用图像嵌入（Image embeddings）在所有数据集上一致提升精度。在 CIFAR‑10 上，GCPM 描述较图像嵌入提升 8.7 个百分点；在细粒度 Stanford Cars 上提升 5.4 个百分点。这确证了概念代理建模是解耦视觉纠缠、聚焦语义属性的核心因果操作。

**视觉纠缠场景的解耦分析。** Figure 4 展示了卡片数据集上的典型案例：当使用 GME‑Qwen 直接对图像编码时，数字属性（视觉上更显著）主导聚类结果，导致按花色分组的准则失效。而 GCPM‑E 通过文本描述显式提取花色信息，成功解耦了数字与花色的视觉纠缠。该案例同时揭示了 GCPM‑G 在视觉属性高度纠缠场景下的失效模式，提示需根据场景选择合适的概念代理方式（GCPM‑E vs. GCPM‑G）。

**LLM 调用效率。** Table 8 统计了 MST 遍历中 LLM 的调用次数及其与样本数的比率。在 ImageNet‑10（13,000 样本）上，LLM 调用仅 1,215 次，比率为 9.3%；在 ABO‑LC（10,756 样本）上调用 2,350 次，比率为 21.8%。Figure 5 进一步可视化 ABO‑LC 上的调用比率，表明 MST 遍历通过仅对簇间语义模糊的边查询 LLM，将昂贵的 LLM 调用控制在远低于样本数量的水平，实现了效率与聚类质量的有效平衡。

### 局限性与失效模式

尽管整体性能优异，方法存在以下可识别的失效边界：第一，在视觉属性高度纠缠的数据集上，多模态 GCPM‑G 可能被视觉显著特征主导，此时需切换至纯文本解耦的 GCPM‑E，但该选择目前依赖人工判断；第二，细粒度聚类中保守的 LLM 合并提示可能损失部分召回率，Table 6 中部分数据集的 B‑Rec. 仍有提升空间；第三，方法依赖冻结的 MLLM 和嵌入模型，在极端专业领域（如医学影像）未经微调的性能可能受限；第四，MST 遍历在初始簇数极大时调用次数为 O(M log M)，实际部署成本不可完全忽略。以上边界需在具体应用中结合领域知识进行验证。

![[assets/figures/papers/paper_list_l2427_https_openaccess_thecvf_com_content_CVPR2026_html_Zhong_Universal_Guidel/figures/010_Table_6.jpg]]
*Table 6: Comparison of clustering results based on BCubed Precision (B-Prec.) and Recall (B-Rec.) before and after using MST Traversal upon HDBSCAN. # of clusters includes singletons*

## 定位与知识库关联

### 1. 与现有聚类范式的结构性差异

本文提出的 **Guideline-Driven Image Clustering Agent** 与当前图像聚类方法在三个核心维度上形成根本性差异：

**训练依赖 vs. 训练无关。** 主流方法如 **SCAN**（Van Gansbeke et al., ECCV 2020）和 **IDCTCL**（Liu et al., NeurIPS 2024）依赖对比学习或自监督训练来获取判别性嵌入，每当聚类准则发生变化时需重新训练。本文方法通过冻结的 MLLM 与指令感知嵌入模型实现训练无关的聚类，指南可即时切换而不需任何参数更新（见 Section 3.2, Table 3）。

**视觉嵌入 vs. 概念代理文本解耦。** 传统方法直接对原始图像编码（如 ResNet 特征），无法解耦指南中指定的语义属性与视觉中纠缠的无关特征。本文的 **生成式概念代理建模（GCPM）** 先将图像转化为聚焦于指南属性的文本描述，再编码为语义嵌入，实现属性级别的解耦与组合（Section 3.2, Eq.2–3）。这一设计在卡片数据集的解耦测试中尤为关键——直接使用多模态嵌入时，数字准则因视觉布局主导了花色准则，而 GCPM 通过文本代理成功解耦（Fig. 4）。

**密度聚类 vs. MST 引导的 LLM 遍历。** 现有方法通常直接应用 HDBSCAN 等密度聚类算法，但 HDBSCAN 倾向于产生一致的小簇，却无法合并语义同质的大簇（Section 3.3）。**IC|TC**（Kwon et al., arXiv 2023）虽支持文本条件聚类，但依赖已知簇数且缺乏自适应合并机制。本文的 MST 遍历算法在嵌入距离的基础上构建最小生成树，仅在语义模糊的簇对之间查询 LLM 进行合并决策，大幅减少 LLM 调用次数（Table 8），同时将召回率从极低水平提升至实用范围（Table 6）。

### 2. 方法谱系中的定位

该方法处于 **多模态大模型驱动的聚类** 与 **训练无关的指南驱动聚类** 的交汇点：

- 相较于 **Multi-Sub**（Yao et al., CVPR 2024）的多标准聚类，本文方法不依赖针对每种准则的独立训练，而是通过文本指南统一表达多种聚类标准，实现跨任务的通用性。
- 相较于 **DiFiC**（Yang et al., arXiv 2024）的细粒度聚类，本文在细粒度场景下仍保持训练无关特性，并通过 GCPM 的语义聚焦能力在 CUB Birds、Stanford Cars 等数据集上取得竞争性结果（Table 4）。
- 相较于 **IC|TC** 的文本条件聚类，本文引入了自动簇数发现机制（MST Traversal），使其在长尾分布场景（ABO-LC, Table 5）中显著优于仅依赖已知簇数的基线。

### 3. 适用边界与局限

**视觉属性高度纠缠的场景。** 当图像的视觉布局与聚类准则强相关时，GCPM 的多模态版本（GCPM‑G）可能失效。卡片数据集上，GCPM‑G 因视觉特征中数字信息占主导而无法按花色聚类，需切换至纯文本解耦的 GCPM‑E 才能恢复正确分组（Fig. 4, Section 4.2）。这表明方法需要根据场景选择合适的概念代理方式，缺乏自动适配机制。

**细粒度聚类的精度-召回权衡。** 细粒度聚类中使用的保守 LLM 合并提示倾向于优先保证精度，但可能损失部分召回率。Table 4 中 MST Traversal 的 Max ∆ 提升幅度在细粒度数据集上相对有限，说明在语义边界模糊的细粒度场景中，LLM 的合并决策仍需进一步优化。

**极端专业领域的性能受限。** 方法依赖冻结的 QWen2.5-VL-Instruct (7B) 和通用嵌入模型，未针对医学影像、工业检测等专业领域微调。在这些领域中，通用 MLLM 的概念代理描述可能缺乏领域特异性，导致嵌入质量下降。

**计算成本不可完全忽略。** MST 遍历的 LLM 调用次数虽远低于样本数量（Table 8），但在初始簇数极大时调用次数仍为 $O(M \log M)$。对于百万级样本的工业场景，实际 API 成本可能成为瓶颈。

### 4. 开放问题

1. **流式与增量聚类扩展。** 当前方法假设全量数据可用，如何将指南驱动的聚类范式扩展至数据流场景，在保持训练无关特性的同时支持增量更新，是一个待探索的方向。

2. **更小模型的可行性。** 能否利用更小的 MLLM（如 1–3B 参数）或优化提示工程进一步降低计算成本而不显著损失聚类质量？Table 7 的消融表明概念代理描述的质量对最终聚类精度至关重要，小模型能否生成同等质量的描述需要验证。

3. **无监督指南生成的有效性。** 在缺乏明确指南的全无监督环境中，LLM 启发式生成的指南（Section 3.1, Appendix C.1）能否达到专家指定的效果？当前实验主要在已知准则的数据集上进行，自动指南的质量评估缺乏系统对比。

4. **跨模态泛化能力。** 该方法的核心机制——概念代理建模与指令感知嵌入——在文本、视频等多模态聚类中的适用性如何？概念代理的生成范式是否可统一迁移至非图像模态，仍需进一步研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/Universal_Guideline_Driven_Image_Clustering_via_a_Hybrid_LLM_Agent.pdf]]
