---
title: "The Shape of Adversarial Influence: Characterizing LLM Latent Spaces with Persistent Homology"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/The_Shape_of_Adversarial_Influence_Characterizing_LLM_Latent_Spaces_with_Persistent_Homology.pdf
project_link: null
code_link: null
openreview_forum_id: v2PglvLLKT
aliases:
- PHPBTALLS
- SAICLLSPH
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "对抗输入（如间接提示注入、后门微调）通过重塑潜在空间的拓扑结构，导致拓扑压缩——从紧凑、多样化的小尺度特征转变为更少但更主导的大尺度特征。"
primary_logic: "对抗输入在LLM潜在空间中诱导出一致的拓扑压缩：干净输入产生大量小尺度、短生命的拓扑特征（如致密连通分量、大量环），而对抗输入则产生更少、更晚形成且更持久的大尺度特征，该签名跨参数规模（3.8B–70B）、跨攻击模式、跨层（尤其早期层）稳健持续，并向局部信息流传递。"
claims:
- "干净与对抗激活的条码摘要主成分分析（PCA）在所有层均明显分离，说明拓扑特征本身就具有高判别性。"
- "基于修剪后的条码摘要训练的逻辑回归在所有模型和层上均达到100%的分类准确率和AUC–ROC，优于原始激活上的线性方法（如LDA、SVM、LR）。"
- "SHAP分析揭示0维条码的平均消亡时间（mean death of 0-bars）是区分干净与对抗的最重要特征：低消亡时间指向干净，高消亡时间指向对抗。"
- "局部神经元级PH分析显示干净输入初始拓扑复杂性高但随层深快速下降，对抗输入则从较简单开始复杂性上升，在约第12层出现显著分歧，表明信息流被重新配置。"
---

# The Shape of Adversarial Influence: Characterizing LLM Latent Spaces with Persistent Homology

> [!tip] 核心洞察
> 对抗输入在LLM潜在空间中诱导出一致的拓扑压缩：干净输入产生大量小尺度、短生命的拓扑特征（如致密连通分量、大量环），而对抗输入则产生更少、更晚形成且更持久的大尺度特征，该签名跨参数规模（3.8B–70B）、跨攻击模式、跨层（尤其早期层）稳健持续，并向局部信息流传递。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 对抗影响之形：用持久同调表征大语言模型潜在空间 |
| 英文题名 | The Shape of Adversarial Influence: Characterizing LLM Latent Spaces with Persistent Homology |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=v2PglvLLKT) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Persistent Homology (PH) based topological analysis of LLM latent spaces |
| Dataset | Mistral 7B TaskTracker (clean vs. poisoned activations), Layer 1, Six LLMs (Phi3-mini, Mistral 7B, LLaMA3 8B, Mixtral-8x7B, Phi3-medium, LLaMA3 70B), Mistral 7B neuron-level information flow (consecutive layers), LLMail-Inject adaptive attacks vs. clean on Mistral 7B (Layer 16) |

> [!tip] 效果简介
> - Mistral 7B TaskTracker (clean vs. poisoned activations), Layer 1 上，Classification Accuracy 为 1.000 (PH features + logistic regression)，对比 0.995 (LDA on raw activations) / 0.870 (LR on raw activations)，变化 +0.005 / +0.130。
> - Six LLMs (Phi3-mini, Mistral 7B, LLaMA3 8B, Mixtral-8x7B, Phi3-medium, LLaMA3 7... 上，Minimum cross-layer test accuracy of logistic regression on pruned barcode summaries 为 1.00，对比 N/A (no linear method achieves perfect minimum across layers)，变化 N/A。
> - Mistral 7B neuron-level information flow (consecutive layers) 上，Precision@5 for detecting layers with largest class separation (Total Persistence 1-bars) 为 0.8 **，对比 empirical chance level，变化 significant (p < .01)。

## 概要

### 问题背景

当前大语言模型（LLM）的可解释性研究主要依赖线性探针、主成分分析或稀疏自编码器等方法，这些手段擅长捕捉潜在空间中的线性方向或孤立特征，却忽略了一个关键事实：LLM的内部表征空间本质上是高维、关系型且非线性的。对抗输入——如间接提示注入、后门微调——所引发的内部状态变化，并非简单的偏移或缩放，而是**全局几何结构的系统性重塑**。现有方法无法有效揭示这种拓扑层面的形变，构成了该领域的一个核心瓶颈。

### 核心发现

本文通过持久同调（Persistent Homology, PH）对LLM潜在空间进行拓扑表征，揭示了一个跨模型、跨攻击模式、跨层稳健存在的**拓扑压缩**现象：

- **干净输入**在潜在空间中产生大量小尺度、短生命的拓扑特征——致密的连通分量、丰富的环结构，反映出多样化的内部表征。
- **对抗输入**则系统性地压缩了这一几何结构：连通分量的平均消亡时间显著增大，环的数量大幅减少，剩余环的出生尺度更大、生命周期更长，整体呈现为更少但更主导的大尺度特征。

这一拓扑签名在参数规模从3.8B到70B的六个指令调优模型中均被观测到，且在专门设计用于绕过现有激活防御的自适应攻击下依然牢固，表明其反映的是对抗影响的根本几何属性，而非特定防御的人为痕迹。

### 方法定位

与直接在原始激活上训练线性分类器（如LDA、SVM、逻辑回归）或结合稀疏自编码器降维的基线方法不同，本文方法的核心创新在于**表征形式的根本转变**：将高维激活点云转化为41维条码摘要特征向量，捕获多尺度拓扑结构（0维连通分量和1维环的生命周期）。这一坐标自由、噪声稳健的全局形状量化手段，使得原本被线性方法忽略的几何差异得以显式化。

在分析粒度上，本文同时构建了层内全局分析和跨层局部信息流分析两套管道。后者通过将相邻层同索引神经元的激活值构成2D点云并计算其持久同调，追踪拓扑复杂性沿层深的演变，揭示了对抗输入对信息通路的重新配置。

### 主要实证结果

1. **判别力**：基于修剪后条码摘要训练的逻辑回归在所有测试模型和层上均达到100%的分类准确率和AUC–ROC，显著优于原始激活上的线性方法。PCA投影显示干净与对抗激活的条码摘要在前两个主成分上明显分离。

2. **可解释性**：SHAP分析表明，0维条码的平均消亡时间是区分干净与对抗的最重要特征——低消亡时间指向干净输入，高消亡时间指向对抗输入，为拓扑压缩提供了可量化的物理解释。

3. **局部信息流**：神经元级PH分析揭示干净输入初始拓扑复杂性高但随层深快速下降，而对抗输入则从较低复杂性开始上升，在约第12层出现显著分歧，表明信息流被重新配置。

4. **鲁棒性**：在绕过TaskTracker防御的自适应攻击样本上，拓扑压缩签名依然显著——1维环数量从12降至4，出生时间从约69升至约85。

### 局限与展望

当前工作仅覆盖指令调优的解码器架构LLM，在其他模型类型上的泛化性尚待验证。条码摘要特征虽具有高判别力，但其本身并不直接关联语义内容，可解释性停留在形状层面。此外，PH计算虽通过GPU加速控制在可接受范围内（4×A100节点约5小时完成六个模型），但实时部署的延迟和资源需求仍构成挑战。未来方向包括：将PH技术与Transformer特有架构属性相结合以生成更具语义意义的特征，探索拓扑约束在模型训练中的正则化作用，以及构建轻量级拓扑监控器用于运行时安全检测。

### 大语言模型的可解释性困境

大语言模型（LLM）的内部表征空间是高维、非线性且高度关系化的，理解这些空间如何编码和处理信息是可解释性研究的核心挑战。当前LLM可解释性方法主要依赖线性探针（linear probes）、稀疏自动编码器（sparse autoencoders）或主成分分析（PCA）等技术，这些方法本质上是在高维空间中寻找线性方向或孤立特征，其核心假设是模型内部表征的几何结构可以被线性分解所捕获。

然而，这种线性范式存在一个根本性盲区：它忽略了潜在空间的全局拓扑结构——即数据点之间多尺度的、关系性的几何组织方式。当对抗输入（如间接提示注入、后门微调、越狱攻击）进入模型时，它们并非仅仅沿某一线性方向偏移几个激活值，而是可能系统性地重塑整个表征空间的形状。现有的线性方法难以捕捉这种全局形变，因为它们天然地缺乏对连通性、环结构、空洞等多尺度拓扑特征的感知能力。

### 对抗输入：从“点扰动”到“形状重塑”

对抗攻击对LLM安全构成了日益严峻的威胁。从间接提示注入（indirect prompt injection）到后门微调（backdoor fine-tuning），再到沙包攻击（sandbagging），这些攻击模式在机制上各不相同，但它们共享一个关键特征：它们改变了模型对输入的处理方式，从而改变了内部表征的几何分布。

现有防御方法（如基于激活的检测系统**TaskTracker**，Abdelnabi et al., 2024）虽然在一定程度上有效，但其设计通常针对特定攻击模式，且其检测逻辑本身依赖于线性或浅层统计特征。一个更深层的问题悬而未决：不同攻击模式是否在模型内部状态中留下了一个共同的、根本性的几何签名？如果存在这样的签名，它将为构建攻击模式无关的通用检测机制提供理论基础。

### 持久同调：一个被忽视的几何分析工具

持久同调（Persistent Homology, PH）是拓扑数据分析（Topological Data Analysis, TDA）的核心工具，它提供了一种坐标自由（coordinate-free）、多尺度（multiscale）、且可证明对噪声鲁棒的方法来量化点云的全局形状。与线性方法不同，PH不关心数据点在坐标系中的绝对位置，而是追踪数据在不同空间尺度下连通分量（0维同调）、环（1维同调）和空洞（更高维同调）的出生（birth）与消亡（death）过程，生成持久条码（persistence barcode）作为形状的完整拓扑签名。

PH已被成功应用于神经网络的权重空间分析、训练动态追踪等领域，但在LLM激活空间分析中的应用几乎空白。这一空白尤其值得关注，因为LLM表征空间的高维性和非线性恰恰是PH擅长处理的场景——PH的噪声鲁棒性（Cohen-Steiner et al., 2007）使其能够在高维噪声中提取稳健的拓扑信号，而其多尺度特性则允许同时捕获局部聚类和全局流形结构。

### 核心研究问题

本文的核心动机源于一个简洁而深刻的假设：**对抗输入会在LLM潜在空间中诱导出一致的、可检测的拓扑形变**。具体而言，我们提出以下研究问题：

1. **对抗输入是否在LLM表征空间中留下可量化的拓扑签名？** 即，干净输入与对抗输入的激活点云是否具有系统性不同的持久条码特征？
2. **该拓扑签名是否跨模型规模、跨攻击模式、跨层级稳健持续？** 如果签名仅在特定条件下出现，其实用价值将大打折扣。
3. **拓扑变化是否向局部信息流传递？** 即，对抗输入是否不仅改变单层激活的全局形状，还重塑了层间神经元到神经元的交互拓扑？
4. **该签名能否作为构建攻击模式无关检测机制的基础？** 特别是，在面对专门设计用于绕过现有防御的自适应攻击时，拓扑签名是否依然牢固？

通过将持久同调引入LLM可解释性研究，本文旨在打开一扇新的窗口：从“形状”的视角理解对抗影响，而非仅从“方向”或“幅度”的视角。

## 核心方法与创新机理

本工作的核心创新在于将**持久同调（Persistent Homology, PH）**这一拓扑数据分析工具引入LLM潜在空间的可解释性研究，从而突破了现有方法仅能捕获线性方向或孤立特征的局限。具体而言，该方法体系在以下四个关键维度上实现了对基线方法的系统性超越。

### 表征形式：从原始激活到拓扑特征向量

现有方法直接在原始隐藏状态上操作，或通过稀疏自动编码器（SAE）进行非线性降维后再分类。这些表征形式本质上仍以点式激活为载体，无法显式编码多点之间的几何关系。本工作将每个激活样本的持久条码转化为一个**41维的条码摘要特征向量**，该向量统计性地编码了0维连通分量和1维环在整个滤过过程中的出生、消亡与持久性分布。这一表征形式的核心优势在于：它将高维点云的全局形状信息压缩为一组可解释的拓扑统计量，使得后续的分类器能够直接利用“形状差异”而非“位置差异”进行判别。

实验证据表明，这一表征转换带来了显著的判别力提升。在Mistral 7B的TaskTracker数据集上，基于条码摘要的逻辑回归在Layer 1即达到**100%的分类准确率**，而原始激活上的线性判别分析（LDA）为99.5%，逻辑回归（LR）仅为87.0%（Table 1）。更关键的是，跨六个模型（Phi3-mini、Mistral 7B、LLaMA3 8B、Mixtral-8x7B、Phi3-medium、LLaMA3 70B）的测试中，修剪后的条码摘要特征在所有层上均实现了**最低1.00的测试准确率**，而没有任何线性方法能在所有层上达到完美分类（Table 2）。

### 几何分析尺度：从线性方向到多尺度全局拓扑

传统可解释性方法——无论是线性探针、PCA，还是SAE降维——本质上都在检测激活空间中的**线性方向**或**独立特征**。这些方法忽略了点云中蕴含的丰富关系型几何信息：连通分量的聚合方式、环结构的形成与消亡、特征在不同尺度下的生命周期。

本工作引入的Vietoris–Rips复形持久同调提供了一种**坐标自由、噪声稳健**的多尺度几何分析框架。其核心机制是：随着距离阈值ϵ从0增长到∞，点云中的点逐渐连接形成单纯复形，拓扑特征（连通分量、环）随之诞生和消亡。持久条码记录了每个特征的生命周期，使得研究者能够在统一的框架下比较不同层、不同模型、不同输入条件下的潜在空间形状。

这一尺度转换揭示了一个此前未被观测到的核心现象——**拓扑压缩**：对抗输入系统性地重塑了潜在空间的拓扑结构，使得表征从紧凑、多样化的小尺度特征转变为更少但更主导的大尺度特征。具体表现为：0维条码的平均消亡时间增大（连通分量需要更大的ϵ才能合并），1维环的数量减少但剩余环的持久性延长（Table 2）。该签名跨参数规模（3.8B–70B）、跨攻击模式、跨层（尤其是早期层）稳健持续。

### 信息流动研究：从单层分析到神经元级联拓扑追踪

现有方法通常分析单层激活或注意力权重，不直接测量跨层交互的拓扑变化。本工作提出了**局部信息流分析**方法：对于相邻层对，将相同索引神经元的激活值构成2D点云（坐标为$(v_i^{\ell}, v_i^{\ell'})$），然后计算该点云的持久同调条码，追踪拓扑复杂性随层深的演变。

这一分析揭示了一个关键的**结构性相变**：干净输入在初始层表现出较高的拓扑复杂性（大量1维环），但随着层深增加复杂性快速下降；而对抗输入则从较低的初始复杂性开始，在中间层复杂性反而上升，两者在约第12层出现显著分歧（Figure 10）。这表明对抗输入重新配置了网络的信息流路径，使得原本应被早期层压缩的拓扑结构在更深层才被处理。统计上，总1-维持久性的方差与干净-对抗差异幅度之间存在强相关性（Spearman's $r = 0.78^{**}$, Table 3），且Precision@5达到0.8，证实了拓扑特征对信息流异常的检测能力。

### 分类与解释工具：从黑箱判别到形状归因

在基线方法中，分类器直接在激活上训练，虽能区分干净与对抗输入，但无法解释“是什么几何差异驱动了这种区分”。本工作将条码摘要特征输入逻辑回归后，进一步通过**SHAP值分析**和**典范相关分析（CCA）**进行特征归因，实现了从“能否区分”到“为何能区分”的跨越。

SHAP分析揭示了驱动分类的最重要特征：**0维条码的平均消亡时间**——低消亡时间指向干净输入，高消亡时间指向对抗输入（Figure 19）。这一发现将分类器的决策与具体的拓扑机制直接关联：对抗输入使得激活点云中的连通分量需要更大的尺度才能合并，即点云更加“分散”而非“紧凑”。CCA分析进一步确认了这些关键特征与主成分之间的相关性，为拓扑压缩现象提供了统计验证。

### 鲁棒性验证：对抗自适应攻击的拓扑不变性

为排除拓扑压缩签名仅是特定防御机制的人工痕迹，本工作在专门设计用于绕过TASKTRACKER激活防御的自适应攻击样本上进行了验证。结果显示，拓扑压缩签名依然显著：1维环数量从干净输入的12个降至4个，环的中位出生时间从约69升至约85（Table 9）。这一结果表明，拓扑压缩反映的是对抗影响在几何层面的**根本属性**，而非特定攻击模式或防御机制的副产品。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_v2PglvLLKT/figures/007_Figure_3.jpg]]
*Figure 3: Pipeline for layer-wise topological analysis. Figure 4: Pipeline for local analysis*

本研究提出了一套基于持久同调（Persistent Homology, PH）的LLM潜在空间拓扑分析框架，旨在从全局形状和局部信息流两个尺度刻画对抗输入如何重塑模型的内部表征几何。该框架的核心思路是：将层激活视为高维点云，通过Vietoris–Rips滤过计算其持久条码（persistence barcode），再将条码向量化为可解释的拓扑特征，最终用于分类、可视化和归因分析。

整体pipeline由以下模块串联而成，如图3和图4所示：

1. **激活提取与子采样**：对于每个目标层，从干净和对抗输入的最后一个词元提取隐藏状态。为平衡统计稳健性与计算开销，对每层抽取 *K* = 64个子样本，每个子样本包含 *k* = 4096个激活向量。

2. **Vietoris–Rips条码计算**：对每个子样本的点云构建Vietoris–Rips复形，利用RIPSER++计算0维（连通分量）和1维（环）持久条码，捕获多尺度拓扑特征的出生与消亡。

3. **条码摘要向量化**：将每条条码转化为41维描述性特征向量，涵盖出生/消亡/持久性的均值、分位数、熵、总数等统计量，形成可直接用于机器学习任务的拓扑签名。

4. **特征修剪与判别分析**：通过相关性分析移除冗余特征（相关系数 > 0.5），得到修剪后的条码摘要。随后进行PCA降维可视化，并训练逻辑回归分类器以量化拓扑特征对干净/对抗输入的判别力。

5. **可解释性归因**：利用SHAP值量化各条码特征对分类的贡献方向与大小，结合典范相关分析（CCA）确认关键拓扑统计量（如0维条码的平均消亡时间）与主成分的相关性。

6. **局部信息流分析**：将相邻层中相同索引神经元的激活值构成2D点云，计算其Vietoris–Rips持久同调，追踪拓扑复杂性在层间的演变，揭示对抗输入如何重新配置信息流。

7. **局部离散比率（LDR）补充量化**：对每个样本的k近邻局部PCA特征值计算离散比率，作为全局PH分析的补充，量化对抗引发的局部几何变化。

该框架的关键设计优势在于：持久同调具有坐标自由和噪声稳健的特性，使得跨层、跨模型、跨攻击模式的拓扑比较成为可能，而无需依赖特定坐标系或线性假设。

### 全局层间拓扑分析管道

该方法的核心计算管道由三个关键模块串联构成：激活子采样、Vietoris–Rips条码计算、以及条码摘要特征提取。

**激活子采样** 对每个模型层，从干净和对抗输入中各抽取 $K = 64$ 个子样本，每个子样本包含 $k = 4096$ 个最后词元的隐藏状态向量。这一设计在统计稳健性与计算可行性之间取得平衡——直接对全量激活计算持久同调将面临组合爆炸，而子采样策略通过多次独立抽样覆盖激活空间的分布特征（Section 3.2）。

**Vietoris–Rips条码计算** 基于子采样得到的点云，利用RIPSER++库构建Vietoris–Rips滤过，计算0维和1维持久条码。Vietoris–Rips复形的定义为：

$$
\operatorname{VR}_{\epsilon}(S,d) := \{ \emptyset \neq \sigma \subset K : \operatorname{diam}(\sigma) \leq \epsilon \}
$$

其中 $S$ 为有限点集，$d$ 为距离度量，$\epsilon$ 为尺度参数。当点集的子集直径不超过 $\epsilon$ 时，该子集作为一个单纯形被纳入复形（Appendix A.1）。随着 $\epsilon$ 从0增长到无穷，复形逐步填充，连通分量（0维同调类）和环（1维同调类）随之诞生与消亡。持久同调通过条码形式记录每个拓扑特征的出生时间（birth）和消亡时间（death），提供坐标自由、噪声稳健的多尺度几何摘要。

**条码摘要特征提取** 将每条条码转化为一个41维描述性向量，涵盖连通分量（H₀）和环（H₁）的统计量：出生/死亡/持久性的均值、分位数、总数，以及基于生命周期长度分布计算的持久熵：

$$
E = - \sum_i p_i \ln(p_i + \epsilon)
$$

其中 $p_i$ 为第 $i$ 个条码的生命周期长度在总持久性中的占比，$\epsilon$ 为防止对数零值的微小常数。持久熵衡量条码生命周期分布的不均匀程度——熵越高表示生命周期越均匀分布（Appendix A.2）。

### 局部神经元级信息流分析

为追踪对抗输入如何重新配置跨层信息传递，该方法引入神经元级局部拓扑分析（Section 3.3）。对于相邻层对 $\ell$ 和 $\ell'$，将相同索引神经元的激活值构成2D点云：

$$
(v_i^{\ell}, v_i^{\ell'})
$$

其中 $v_i^{\ell}$ 为第 $i$ 个神经元在层 $\ell$ 的激活值。对该2D嵌入计算Vietoris–Rips持久同调，提取1维环的总持久性（total persistence）作为拓扑复杂性的度量。这一设计将信息流从高维空间投影到神经元对构成的二维几何中，使得对抗引发的结构变化可通过环的数量和生命周期直接量化。

### 局部离散比率分析

作为对持久同调的补充，该方法引入局部离散比率（Local Dispersion Ratio, LDR）量化对抗引发的局部几何变化（Appendix B.3）。对每个最后词元的激活向量，在各层中识别其 $k$ 近邻，对近邻点进行局部PCA，记特征值为 $\lambda_1 \geq \cdots \geq \lambda_{D'}$，则离散比率定义为：

$$
\frac{\sum_{j=2}^{D'} \lambda_j}{\lambda_1 + \epsilon}
$$

该比值反映方差在次要方向上的扩散程度——值越高表示局部点云在主方向之外的分散程度越高，即局部几何结构越不紧凑。

### 类间-类内距离比

为量化干净与对抗条码摘要簇的可分离性，定义类间距离与平均类内距离的比值（Appendix C.2）：

$$
r := \frac{d_{\mathrm{inter}}}{\frac{1}{2}\left(d_{\mathrm{intra}}^{\mathrm{clean}} + d_{\mathrm{intra}}^{\mathrm{poison}}\right)}
$$

其中 $d_{\mathrm{inter}}$ 为干净簇与对抗簇质心间的欧氏距离，$d_{\mathrm{intra}}$ 为各类内部样本到质心的平均距离。$r$ 越大表示两类在条码摘要空间中越可分离，该指标用于指导子采样超参数的选择与消融验证。

## 实验与关键发现

### 核心发现：拓扑压缩签名

对抗输入在LLM潜在空间中诱导出一致的**拓扑压缩**（topological compression）：干净输入产生大量小尺度、短生命的拓扑特征，而对抗输入则产生更少、更晚形成且更持久的大尺度特征。这一签名通过持久同调（Persistent Homology, PH）条码的统计摘要被量化，并在多个维度上得到验证。

**跨模型一致性**：Table 2总结了六个指令调优解码器模型（Phi3-mini、Mistral 7B、LLaMA3 8B、Mixtral-8x7B、Phi3-medium、LLaMA3 70B，参数规模3.8B至70B）上的拓扑压缩签名。对抗输入系统性地改变了三个关键拓扑指标：0维连通分量的平均死亡时间（$\bar{d}_{H_0}$）增加，1维环的数量（$\#H_1$）减少，剩余环的寿命（$\ell_{H_1}$）延长。这一模式跨参数规模和模型族保持稳健。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_v2PglvLLKT/figures/015_Table_2.jpg]]
*Table 2: Topological compression signature across models. Adversarial inputs reshape latent space geometry by increasing the mean death time of connected components ( $\bar { d } _ { H _ { 0 } }$ increases), reducing the number of loops $\bar$ ( \# $H _ { 1 }$ decreases), and extending the lifetime of remaining loops ( $\ell _ { H _ { 1 } }$ increases). Each cell indicates whether the adversarial condition matches this pattern (✓), is inconsistent across layers (∼), or shows the opposite (×). Acc. is the minimum logistic-regression test accuracy across layers. a Holds at L1–L24 but inverts at L32. b Direction varies across layers with no dominant trend

**PCA可视化分离**：Figure 7展示了修剪后的条码摘要特征在前两个主成分上的投影。干净与对抗激活在所有层（第1、8、16、24、32层）均明显分离，解释方差分别为0.59、0.49、0.52、0.96、0.83。这表明拓扑特征本身即具有高判别性，无需复杂后处理。

### 分类性能对比

**与线性方法的比较**：Table 1报告了Mistral 7B第1层上的分类准确率对比。基于修剪条码摘要的逻辑回归（PH + LR）达到100%准确率，优于直接在原始激活上训练的线性方法——LDA为99.5%，线性SVM为88.75%，逻辑回归仅为87.0%。即使先通过稀疏自动编码器（SAE, Cunningham et al., 2023）将激活降维至128维再应用线性分类器，SAE+LDA/SVM/LR的性能仍不及PH方法。这一优势在早期层尤为显著，因为早期层的原始激活中干净与对抗的线性可分性较弱。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_v2PglvLLKT/figures/013_Table_1.jpg]]
*Table 1: Comparison of predictive power with linear methods. Accuracy, with a 70/30 train/test split, of a linear discriminant analysis (LDA), a linear SVM and a logistic regression (LR) trained to distinguish 1000 raw clean activations from 1000 raw poisoned activations, with or without reducing the dimensionality of the data using a sparse autoencoder (SAE); and our method using PH*

**跨层完美分类**：Table 2进一步显示，基于修剪条码摘要的逻辑回归在所有六个模型的所有层上均达到100%的测试准确率，而没有任何线性方法能在所有层上达到完美分类。这表明拓扑特征捕获了线性方法无法获取的几何差异。

### 特征重要性解释

**SHAP分析揭示关键特征**：Figure 19（附录）的SHAP分析表明，0维条码的平均死亡时间（mean death of 0-bars）是区分干净与对抗输入的最重要特征。低死亡时间指向干净输入，高死亡时间指向对抗输入——这与拓扑压缩的假设一致：对抗输入中连通分量在更大的距离尺度上才合并消亡，反映了点云在空间中更分散的分布。

**典范相关分析（CCA）确认**：CCA载荷分析进一步确认了这些关键拓扑统计量与主成分之间的强相关性，排除了特征冗余导致的伪影。

### 局部信息流分析

**神经元级别的拓扑相变**：Figure 10展示了相邻层神经元对的2D嵌入的持久同调分析结果。干净输入在初始层表现出更高的拓扑复杂性（更大的1维总持久性），但随着层深增加复杂性快速下降；对抗输入则从较低的初始复杂性开始，在中间层复杂性上升，约在第12层出现显著分歧。这表明对抗输入从根本上重新配置了网络的信息流路径。

**峰值检测精度**：Table 3报告了利用拓扑特征的总方差峰值来检测类间分离最大层的精度。对于1维总持久性（Total Persistence 1-bars），Precision@5达到0.8（p < .01），且总方差与类间绝对差异的Spearman秩相关系数为0.78（p < .01）。这意味着无需标签即可通过拓扑特征的方差变化定位信息流被对抗影响最大的层。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_v2PglvLLKT/figures/017_Table_3.jpg]]
*Table 3: Peak analysis. Precision@k for k=1, 3, and 5 largest peaks in total variance, and their precision in detecting the largest peaks in absolute difference between the two classes. Spearman’s rank correlation (r) is reported in the last column. ∗, ∗∗ correspond to p-values \<.05 and .01, respectively*

### 消融与控制实验

**子采样超参数稳定性**：增大子样本大小n（100→1500）和子样本数量K（10→90）可稳定提高类间距离与类内距离之比（Figure 15–17）。在n=1000、K=64时，分类准确率和距离比已饱和，证明所选超参数能可靠分离干净与对抗分布。

**重抽样控制排除伪影**：局部离散比率（LDR）在Clean vs. Clean和Poisoned vs. Poisoned的重抽样控制实验中差异均趋近于零，而Mixed vs. Mixed呈现出与真实干净-对抗分离一致的系统性偏差（Figure 9、Figure 13）。这排除了采样噪声或随机划分造成的伪像。

**神经元索引随机排列**：将神经元索引随机排列后，局部PH分析所观察到的干净与对抗间的拓扑差异消失（Figure 56，附录D.2.1）。这证实差异源自特定神经元到神经元的交互通路，而非统计波动。

### 自适应攻击下的鲁棒性

**绕过TASKTRACKER防御的攻击**：Table 9展示了在专门设计用于绕过TASKTRACKER激活防御（Abdelnabi et al., 2024）的自适应攻击样本上的结果。在Mistral 7B第16层，对抗输入的1维环数量从干净的12个降至4个，环的中位出生时间从约69升至约85。拓扑压缩签名在面对刻意规避现有防御的攻击时依然显著，说明该签名反映的是对抗影响的根本几何属性，而非特定防御的人工痕迹。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_v2PglvLLKT/figures/095_Table_9.jpg]]
*Table 9: PH barcode statistics for clean vs. adaptive attack. Comparison of barcode summary statistics of clean vs. adaptive attack activations from the LLMail-Inject dataset on Mistral-7B (Layer 16)*

### 失败模式与局限性

尽管拓扑特征在分类任务上表现卓越，需注意以下局限：

1. **架构泛化性待验证**：所有实验均基于指令调优的解码器架构LLM，未包含仅编码器（如BERT）或编码器-解码器（如T5）架构。结论在其他模型类型上的适用性需要独立验证。

2. **语义可解释性有限**：条码摘要特征虽能高度判别干净/对抗输入，但其本身并不直接关联词汇或语义内容。SHAP分析揭示的是“平均死亡时间”等拓扑统计量的重要性，而非具体语义概念，在可解释性上仍有局限。

3. **计算资源需求**：持久同调计算虽通过GPU加速控制在合理开销内（单层约10分钟，整模型约50分钟，Table 8），但依赖高端GPU（4×A100），实时在线部署的可行性尚未探讨。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_v2PglvLLKT/figures/094_Table_8.jpg]]
*Table 8: Computational Costs. Per-barcode wall-clock time and GPU-memory consumption ( k = 4096, dimension $\leq$ 2 ) . Statistics over K = 64 barcodes drawn from the LLAMA-3 8B activations*

4. **对抗数据集覆盖有限**：研究基于特定安全基准（TaskTracker、sandbagging），对抗样本的覆盖范围和多样性可能有限。更多样化的投毒、后门或越狱攻击下的表现有待拓展。

## 定位与知识库关联

### 从线性探针到拓扑探针：表征形式的范式转换

当前LLM可解释性的主流范式建立在**线性探针**之上：在原始隐藏状态上训练线性判别分析（LDA）、线性支持向量机（SVM）或逻辑回归（LR），试图沿某一方向读出特定概念。这一思路的核心假设是，模型内部知识以近似线性的方式编码在激活空间中。然而，本研究的实验结果直接暴露了该假设的脆弱性——在Mistral 7B的第1层，LDA在原始激活上的分类准确率为0.995，而逻辑回归仅为0.870（Table 1），说明线性方法的性能高度依赖于分类器的选择和层的深度，缺乏一致的判别力。

更根本的瓶颈在于：线性探针只能捕获**孤立的方向性特征**，忽略了潜在空间中点与点之间的**关系型几何结构**。即使结合非线性降维——如通过稀疏自动编码器（SAE）（Cunningham et al., 2023）将激活压缩至128维再应用线性分类器——本质上仍是对独立特征的提取，未能揭示全局拓扑的形变模式。

本研究提出的**持久同调（Persistent Homology, PH）框架**将表征形式从“激活向量”转换为“持久条码摘要”——一个41维的拓扑特征向量，捕获连通分量（H0）和环（H1）在不同尺度下的出生、消亡与生命周期。这一转换具有三重方法论优势：

1. **坐标自由**：Vietoris–Rips复形仅依赖点间距离，不依赖任何特定基的选择，因此跨模型、跨层的条码摘要可以直接比较（Table 2验证了3.8B到70B六个模型的一致性）。
2. **多尺度**：条码同时编码了小尺度（早期消亡的短条）和大尺度（持久的长条）的拓扑结构，而线性方法只能感知单一尺度的方差方向。
3. **噪声鲁棒**：持久同调具有可证明的噪声稳定性（Cohen-Steiner et al., 2007），这对高维激活空间中不可避免的随机波动至关重要。

### 从单层激活到跨层信息流：分析尺度的扩展

现有工作通常聚焦于**单层激活的静态分析**，或通过注意力权重间接推断信息流动，缺乏对跨层交互的拓扑变化的直接测量。本研究的**局部神经元级PH分析**（Section 3.3）将分析尺度从“层内点云”扩展到“层间神经元对”：对相邻层的相同索引神经元构建2D嵌入 $(v_i^{\ell}, v_i^{\ell'})$，计算其Vietoris–Rips条码，从而追踪拓扑复杂性沿层深度的演变。

这一设计揭示了线性方法完全无法感知的**信息流相变**：干净输入在早期层呈现高拓扑复杂性（大量1维环），随后随层深快速简化；而对抗输入从较低的初始复杂性出发，在约第12层出现分歧，复杂性不降反升（Figure 10）。这种“交叉”模式表明，对抗攻击不仅改变了单层的几何形状，更**重新配置了信息在神经元通路中的传递方式**。随机排列神经元索引后该信号消失（Figure 56），排除了统计伪像的可能，确认了效应依赖于特定的神经元到神经元交互通路。

### 分类与解释工具的升级：从黑箱判别到形状归因

传统线性分类器虽能判别干净/对抗激活，却无法解释**几何差异的本质**——为什么某个样本被判定为对抗？本研究的管道将条码摘要输入逻辑回归后，进一步通过SHAP值量化每条拓扑特征的贡献方向与大小，并通过典范相关分析（CCA）确认关键特征与主成分的相关性。

SHAP分析揭示了最关键的拓扑签名：**0维条码的平均消亡时间（mean death of H0）**——低消亡时间指向干净输入（连通分量在小尺度快速合并），高消亡时间指向对抗输入（连通分量持续到大尺度才消失）（Figure 19）。这一发现将“对抗检测”从黑箱分类提升到了**有物理意义的形状解释**：对抗输入使得激活点在空间中更加分散，需要更大的距离阈值才能将点连接成连通分量。

### 与现有防御的关系：超越激活防御的拓扑不变性

现有针对间接提示注入的激活防御系统如**TaskTracker**（Abdelnabi et al., 2024）通过在激活空间训练分类器来检测攻击。本研究在专门设计用于绕过TaskTracker的**自适应攻击**样本（LLMail-Inject数据集）上进行了严峻的压力测试。结果表明，即使攻击成功绕过了激活层面的防御，拓扑压缩签名依然显著——1维环数量从12降为4，中位出生时间从约69升至约85（Table 9）。这证明拓扑签名反映的是**对抗影响的根本几何属性**，而非特定防御系统的人工痕迹，具有更高的鲁棒性。

### 适用边界与局限

**架构覆盖的局限**：当前验证仅限于指令调优的解码器架构LLM（Phi3-mini, Mistral 7B, LLaMA3 8B, Mixtral-8x7B, Phi3-medium, LLaMA3 70B）。对于仅编码器（如BERT系列）或编码器-解码器架构（如T5），拓扑压缩签名是否成立尚待验证——不同架构的激活空间可能具有本质不同的拓扑先验。

**语义可解释性的鸿沟**：条码摘要虽能高度判别干净/对抗输入（跨所有模型和层达到100%准确率，Table 2），但其特征本身——如“H0平均消亡时间”、“H1数量”——并不直接关联词汇、语义或知识单元。当前的可解释性是**形状层面**的，而非语义层面的。如何将拓扑特征与具体的语义内容建立映射，仍是开放挑战。

**计算开销与实时部署**：尽管通过GPU加速（Ripser++）和子采样策略（K=64, k=4096）将单层计算控制在约10分钟（4×A100），完整六模型分析约需5小时，但这一开销对于实时安全监控场景仍显沉重。轻量级拓扑监控器的构建尚未探索。

**攻击覆盖的多样性**：实验基于TaskTracker（间接提示注入）、sandbagging（后门微调）和LLMail-Inject（自适应攻击）三个数据集，未包含越狱攻击、数据投毒等更广泛的对抗类型。不同攻击模式是否共享同一拓扑不变量，抑或各自诱导独特的拓扑签名，仍是开放问题。

### 开放问题与未来方向

1. **拓扑-语义桥接**：能否将经典PH技术适配Transformer特有的架构属性（如自注意力的图结构、前馈网络的非线性），以生成既有形状感知又有语义意义的可解释特征？例如，在注意力图上而非激活空间上构建滤过。

2. **拓扑压缩的普适性**：该签名是否是一种通用的“模型失配”指标，能泛化到除提示注入和后门之外的其他对抗行为（如越狱、幻觉诱导）？跨攻击模式的拓扑不变量若存在，将成为检测未知攻击的基础。

3. **拓扑感知的训练与架构设计**：在预训练或微调阶段引入拓扑约束（如惩罚H0平均消亡时间的异常增长），是否能提高模型对对抗攻击的固有鲁棒性？拓扑正则化可能成为对抗训练的新维度。

4. **轻量级实时监控**：能否基于条码摘要中最具判别力的少数特征（如H0平均消亡时间）构建轻量级检测器，作为运行时安全监控的附加层？这需要将PH计算从批量分析压缩为在线流式处理。

5. **与线性方法的协同**：PH分析提供全局形状感知，线性探针提供方向性读出——两者能否协同工作，构建既有“方向感”又有“形状感”的模型内部状态描述？例如，在条码摘要分离出的子空间内进一步训练线性探针以提取语义。

6. **非相邻层的长程交互**：当前局部信息流分析仅检查相邻层对，但Transformer的残差连接使得非相邻层之间存在直接的信息传递。将这些长程交互纳入拓扑分析框架，可能揭示更深层的对抗影响机制。

## 原文 PDF

![[paperPDFs/ICLR_2026/The_Shape_of_Adversarial_Influence_Characterizing_LLM_Latent_Spaces_with_Persistent_Homology.pdf]]
