---
title: "LLM DNA: Tracing Model Evolution via Functional Representations"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/LLM_DNA_Tracing_Model_Evolution_via_Functional_Representations.pdf
project_link: https://pypi.org/project/llm-dna/
code_link: https://github.com/Xtra-Computing/LLM-DNA
openreview_forum_id: UIxHaAqFqQ
aliases:
- LDTMEFR
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "利用Johnson-Lindenstrauss引理保证的存在性，通过随机高斯投影将LLM功能映射到满足双利普希茨条件的低维DNA空间，使得功能相似的模型具有相近的DNA表示，且提取过程无需训练，独立于架构与分词器。"
primary_logic: "将LLM视为从有限输入到logits向量的函数，赋予其Hilbert空间结构；随机投影能保持该空间的距离信息，由此构造的DNA天然满足遗传性（微调产生相似DNA）和遗传决定性（相似DNA对应相似功能），并可直接用于关系检测与谱系重建。"
claims:
- "LLM DNA的正式存在性由JL引理保证，且可通过随机线性投影实际构造。"
- "在305个异构LLM上，基于DNA的关系检测达到AUC 0.992，大幅优于PhyloLM等基线。"
- "DNA距离与模型参数规模无关（点双列相关系数不显著），确保表示的公平性。"
- "基于DNA构建的谱系树反映了从编码器-解码器到仅解码器架构的转变，并与时间演化一致。"
---

# LLM DNA: Tracing Model Evolution via Functional Representations

> [!tip] 核心洞察
> 将LLM视为从有限输入到logits向量的函数，赋予其Hilbert空间结构；随机投影能保持该空间的距离信息，由此构造的DNA天然满足遗传性（微调产生相似DNA）和遗传决定性（相似DNA对应相似功能），并可直接用于关系检测与谱系重建。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | LLM DNA：通过功能表示追踪模型演化 |
| 英文题名 | LLM DNA: Tracing Model Evolution via Functional Representations |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=UIxHaAqFqQ) · [GitHub](https://github.com/Xtra-Computing/LLM-DNA) · [Project](https://pypi.org/project/llm-dna/) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | RepTrace |
| Dataset | LLM关系检测 (Relation Detection over 305 models), LLM关系检测, 模型路由 (Model Routing), 随机输入下的关系检测 |

> [!tip] 效果简介
> - LLM关系检测 (Relation Detection over 305 models) 上，AUC 为 0.992 ±0.023，对比 0.788 ±0.060 (PhyloLM+SVM)，变化 +0.204。
> - LLM关系检测 上，F1 为 0.940 ±0.050，对比 0.766 ±0.057 (PhyloLM+SVM)，变化 +0.174。
> - 模型路由 (Model Routing) 上，Accuracy 为 0.672 ±0.008，对比 0.665 ±0.003 (EmbedLLM)，变化 +0.007。

## 概要

大语言模型（LLM）的快速迭代与大规模分发使得追踪其演化关系、检测衍生模型、理解功能相似性变得日益困难。现有方法存在根本性瓶颈：基于token分布的方法（如PhyloLM）受限于分词器差异且忽略语义，基于学习嵌入的方法（如EmbedLLM）依赖固定模型集并需重新训练，难以应对海量异构LLM的演化分析需求。

本文提出**LLM DNA**——一种通用的、任务无关、可扩展的低维功能指纹，并给出其形式化定义与提取框架**RepTrace**。核心洞察在于将LLM视为从有限输入到logits向量的函数，赋予其Hilbert空间结构；利用Johnson-Lindenstrauss引理保证的存在性，通过随机高斯投影将LLM功能映射到满足双利普希茨条件的低维DNA空间，使得功能相似的模型具有相近的DNA表示。该方法无需训练，独立于架构与分词器，每个LLM可独立计算DNA，新模型可直接加入而不改变已有表示。

实验覆盖305个异构LLM，主要结果如下：

- **关系检测**：DNA达到AUC 0.992 ±0.023，F1 0.940 ±0.050，大幅优于PhyloLM（AUC 0.788，F1 0.766）。
- **模型路由**：DNA准确率0.672 ±0.008，与EmbedLLM（0.665）相当，但无需训练。
- **鲁棒性**：使用随机输入提取的DNA仍保持高性能（F1 0.952），且DNA距离与模型参数规模无显著相关性（p>0.05），确保表示的公平性。
- **谱系重建**：基于DNA距离构建的谱系树反映了从编码器-解码器到仅解码器架构的转变，并与时间演化一致，同时揭示了多项未记录的模型关系。

方法局限包括：DNA子序列尚缺乏数学意义，提取依赖外部句子嵌入模型的质量，以及对API模型拒绝随机输出和自适应攻击的鲁棒性不足。

大语言模型（LLM）的快速迭代与广泛分发，催生了一个高度异构的模型生态：同一基座模型经微调、合并、量化、蒸馏后衍生出大量变体，其中许多变体之间的演化关系并未被公开记录。理解这些模型之间的功能亲缘关系，对于模型选择、版权归属、安全审计以及生态治理具有基础性意义。然而，现有的模型表征方法在应对这一需求时暴露出结构性缺陷。

基于 token 分布的方法，如 **PhyloLM**（Yax et al., 2025），通过比较模型输出分布的遗传距离来推断关系。这类方法存在两个根本性局限：其一，距离计算依赖分词器的严格对齐，异构架构下分词器差异会导致不可比较的距离度量；其二，token 级分布本质上忽略语义信息——两个模型可能因分词偏好不同而产生差异巨大的分布，即使它们对同一输入给出语义等价的回答。

基于学习嵌入的方法，如 **EmbedLLM**（Zhuang et al., 2025），试图通过训练将模型映射到统一表示空间。但该方法要求在一个固定模型集上端到端训练编码器，当新模型加入时需重新学习全部参数，无法满足海量异构 LLM 持续涌现场景下的可扩展性需求。更关键的是，训练过程将表示空间锚定在特定任务分布上，破坏了表示的通用性。

上述瓶颈指向一个核心问题：**缺乏一种通用、任务无关、可扩展的低维功能指纹**，能够在不依赖分词器对齐、无需训练的前提下，稳定地表征任意 LLM 的功能行为，并使得功能相似的模型具有相近的表示。

RepTrace 从这一缺口切入，其核心洞察是将 LLM 视为从有限输入空间到 logits 向量空间的函数，并赋予该函数空间 Hilbert 空间结构。借助 Johnson-Lindenstrauss 引理保证的存在性，通过随机高斯投影将该高维功能空间压缩到低维“DNA”空间，同时保持功能距离的双利普希茨条件——即 DNA 距离与真实功能距离之间存在定量的上下界约束。这意味着 DNA 天然满足两个关键性质：**遗传性**（微调产生相似 DNA）和**遗传决定性**（相似 DNA 对应相似功能），使其可直接用于关系检测与谱系重建，而无需任何训练步骤。

## 核心方法与创新机理

LLM DNA 的核心创新在于将 LLM 功能空间的几何结构通过随机投影压缩为低维向量表示，从而绕开了现有方法的根本性瓶颈。与 PhyloLM（Yax et al., 2025）依赖 token 级分布距离、EmbedLLM（Zhuang et al., 2025）需在固定模型集上训练任务特定嵌入不同，RepTrace 提出了一条全新的技术路径，其关键创新体现在以下三个维度。

**从 token 分布到语义功能的表示粒度跃迁。** PhyloLM 的遗传距离基于输出 token 分布的直接比较，这使其天然受限于分词器差异——不同模型的词汇表不兼容时，距离度量即失去意义。RepTrace 通过引入句子嵌入模型（如 Qwen3-Embedding-8B）将每个 LLM 的文本响应映射为固定维度的语义向量，再将这些向量串联形成函数表示 $E_f$（Algorithm 1）。这一设计将比较对象从表面的 token 分布提升至深层语义空间，使得跨架构、跨分词器的模型比较成为可能。消融实验证实，即使使用随机词语作为输入，提取的 DNA 仍能有效区分模型关系（Table 3，F1 达 0.952），表明方法捕获的是模型的功能行为而非输入分布的统计特征。

**完全无训练、任务无关的可扩展性设计。** EmbedLLM 的核心缺陷在于其嵌入空间依赖于对固定模型集合的联合训练——新增模型意味着整个表示空间需要重新学习，这在大规模 LLM 生态中不可持续。RepTrace 则利用了 Johnson-Lindenstrauss 引理保证的存在性：对任意有限模型集合 $\mathcal{F}_K$，存在一个随机高斯投影矩阵 $A$，将高维函数表示 $E_f$ 映射到低维 DNA 向量 $\tau_f = A E_f$，且该映射天然满足双利普希茨条件（Theorem 3.3, Corollary 3.4）。这意味着每个 LLM 的 DNA 可以完全独立计算，新模型可直接加入而不改变已有表示，实现了真正的“即插即用”。DNA 维度 $L$ 的下界由 $L = O\left(\left[(c_2 + c_1)/(c_2 - c_1)\right]^2 \log K\right)$ 给出，实验进一步表明 $L=128$ 附近性能即收敛（Figure 10），验证了理论指导下的实际效率。

**基于期望采样的功能距离近似。** 由于 LLM 的函数空间理论上无限维，直接计算功能距离不可行。RepTrace 定义了随机功能距离 $d_f(f_1, f_2) := \mathbb{E}_{S_t \sim \mu} \left[ \sqrt{ \sum_{x_j \in S_t} \| f_1(x_j) - f_2(x_j) \|_2^2 } \right]$（Definition 4.1），并通过集中不等式（Lemma 4.2）保证了有限提示采样下经验估计的可靠性。这一设计使得 DNA 提取既不需要对模型内部参数的访问，也不依赖特定任务数据分布——Mantel 检验显示，从两个不相交数据集提取的 DNA 距离高度相关（Figure 3，Pearson-r = 0.7797, p < 0.0001），证明了表示的跨数据集稳定性。

上述三个 changed slots 共同构成了 RepTrace 相对于基线方法的根本性差异：**语义粒度**解决了跨分词器比较的障碍，**无训练设计**消除了可扩展性瓶颈，**期望近似**提供了理论保证下的实际可计算性。这三者的协同使得 DNA 能够在 305 个异构 LLM 上实现 AUC 0.992 的关系检测性能（Table 1），同时保持与模型参数规模无关的公平性（Table 6，所有 p 值 > 0.05）。

RepTrace的核心理念是将LLM视为从有限输入空间到logits向量的函数，赋予其Hilbert空间结构，然后通过随机高斯投影将该函数映射到一个低维DNA空间。这个映射满足双利普希茨条件（Definition 3.2），保证功能相似的模型具有相近的DNA表示，而功能差异大的模型其DNA距离也相应增大。

整个提取流水线（Algorithm 1, Figure 1）由五个顺序模块构成，输入为$t$个提示文本，输出为每个LLM的$L$维DNA向量：

**1. Prompt Sampling（提示采样）**  
从数据集中抽取$t$个代表性提示，构成输入集$S_t$。这些提示可以是标准基准数据集，也可以是随机词语（Table 3表明随机输入同样有效，甚至在某些指标上略优于标准数据集）。

**2. LLM Inference（模型推理）**  
对每个提示$x_i$调用目标LLM $f$，生成文本响应$y_i \leftarrow f(x_i)$。对于指令微调模型，可选择移除聊天模板以消除特殊格式引入的偏差（Table 4显示移除模板后关系预测准确性提升1-3个百分点）。

**3. Semantic Embedding（语义嵌入）**  
使用预训练句子嵌入模型$\phi$（如Qwen3-Embedding-8B）将每个响应$y_i$映射为固定维度$p$的语义向量$e_i \leftarrow \phi(y_i)$。这一步将token级输出转化为语义级表示，从根源上规避了分词器差异问题。

**4. Concatenation（拼接）**  
将所有$t$个响应嵌入串联，形成一个$t \times p$维的函数表示$E_f \leftarrow [e_1, e_2, \ldots, e_t]$。这个高维向量捕获了LLM在多个输入上的整体功能行为。

**5. Random Gaussian Projection（随机高斯投影）**  
通过随机高斯矩阵$A \in \mathbb{R}^{L \times (t \cdot p)}$将$E_f$投影到$L$维空间，得到最终的DNA向量$\tau_f \leftarrow A E_f$。这一步的理论保证来自Johnson-Lindenstrauss引理（Theorem 3.3），它证明了存在这样的投影使得DNA距离与功能距离之间满足双利普希茨条件，且目标维度$L = O\left(\left[(c_2 + c_1)/(c_2 - c_1)\right]^2 \log K\right)$，仅与模型数量$K$和允许的失真常数有关。

**输入输出流**：流水线的输入是一组提示文本和一个待分析的LLM，输出是该LLM的低维DNA向量。每个LLM的DNA可以独立计算，新增模型无需重新训练或改变已有表示。DNA向量随后可直接用于关系检测（通过SVM分类器）或谱系重建（通过Neighbor-Joining算法计算DNA间的$\ell_2$距离）。

**关键设计选择**：
- 句子嵌入维度$p$对DNA质量影响微小（Figure 9），即使使用较小维度也可获得相近性能。
- DNA维度$L$在128附近性能收敛（Figure 10），继续增大无显著增益。
- 随机高斯矩阵$A$在提取时固定，保证所有模型的投影一致且公平。
- 整个流程完全无训练、任务无关，不依赖模型架构或分词器。

### 5.1 核心流水线模块

RepTrace的DNA提取流水线由五个顺序模块构成（Algorithm 1），整体无需训练，每个LLM可独立计算：

**Prompt Sampling**：从数据集中抽取 $t$ 个代表性提示，构成输入集 $S_t$。提示的选择对DNA质量影响较小——实验表明，即使使用随机词语输入，DNA仍能有效区分模型关系（Table 3, F1达0.952），说明方法对输入分布不敏感。

**LLM Inference**：对每个提示 $x_i$ 调用目标LLM $f$ 生成文本响应 $y_i \leftarrow f(x_i)$。对于指令微调模型，移除聊天模板可提升跨家族比较的公平性，关系预测准确性提升1–3个百分点（Table 4）。

**Semantic Embedding**：使用预训练句子嵌入模型 $\phi$（默认Qwen3-Embedding-8B）将每个响应映射为固定维度 $p$ 的语义向量 $e_i \leftarrow \phi(y_i)$。这一模块是捕获功能语义的关键——它使得DNA独立于分词器，解决了PhyloLM等基于token分布方法的跨架构障碍。消融实验表明，嵌入输出维度 $p$ 对DNA质量影响微小（Figure 9）。

**Concatenation**：将所有响应嵌入串联形成高维函数表示 $E_f \leftarrow [e_1, e_2, \dots, e_t]$，维度为 $t \times p$。

**Random Gaussian Projection**：通过随机高斯矩阵 $A \in \mathbb{R}^{L \times (t \cdot p)}$ 将 $E_f$ 投影到 $L$ 维空间，得到DNA向量 $\tau_f \leftarrow A E_f$。这是理论核心——Johnson-Lindenstrauss引理保证该投影以高概率保持函数空间的距离结构（Theorem 3.3）。维度 $L$ 在128附近性能收敛（Figure 10）。

### 5.2 关键公式与推导

#### 5.2.1 双利普希茨条件（Definition 3.2）

DNA空间与LLM函数空间之间必须满足双利普希茨条件：

$$c_1 \cdot d_H(f_1, f_2) \leq d_\tau(\tau_{f_1}, \tau_{f_2}) \leq c_2 \cdot d_H(f_1, f_2)$$

其中 $d_H$ 是Hilbert空间中的功能距离，$d_\tau$ 是DNA空间的欧氏距离，$0 < c_1 \leq c_2$ 为常数。该条件保证：功能相似的模型DNA相近（遗传性），DNA相近的模型功能相似（遗传决定性）。

#### 5.2.2 DNA存在性定理（Theorem 3.3）

Johnson-Lindenstrauss引理直接保证：对于任意 $K$ 个LLM的有限集合，存在线性映射将功能表示嵌入到维度为

$$L = O\left(\left[\frac{c_2 + c_1}{c_2 - c_1}\right]^2 \log K\right)$$

的DNA空间，满足上述双利普希茨条件。该定理同时给出了DNA维度的理论下界——$L$ 与模型数量 $K$ 呈对数关系，与失真容忍度 $c_2/c_1$ 呈二次关系。

#### 5.2.3 随机功能距离（Definition 4.1）

由于无法直接计算Hilbert空间中的功能距离，RepTrace引入随机功能距离作为可计算的代理：

$$d_f(f_1, f_2) := \mathbb{E}_{S_t \sim \mu} \left[ \sqrt{ \sum_{x_j \in S_t} \| f_1(x_j) - f_2(x_j) \|_2^2 } \right]$$

该定义将功能距离表示为对随机提示集 $S_t$ 采样下的期望拼接嵌入距离，使实际计算成为可能。

#### 5.2.4 经验估计的集中不等式（Lemma 4.2）

经验功能距离 $\hat{d}_f$ 对真实Hilbert距离 $d_H$ 的估计误差由Hoeffding不等式控制：

$$P\left( \left| \frac{1}{t} \hat{d}_f^2 - d_H^2 \right| \geq \epsilon \right) \leq 2 \exp\left( - \frac{2 t \epsilon^2}{C_{\max}^2} \right)$$

其中 $C_{\max}$ 是单个提示下响应嵌入范数的上界。该不等式保证：随提示数量 $t$ 增加，经验估计以指数速率收敛到真实值，为有限采样下的DNA可靠性提供了理论保障。

### 5.3 理论-实践对应

| 理论组件 | 实践实现 | 验证证据 |
|---------|---------|---------|
| JL引理保证的随机投影 | 随机高斯矩阵 $A$ | Figure 10: $L=128$ 收敛 |
| 双利普希茨条件 | DNA距离与功能距离的保持 | Figure 3: Mantel检验 $r=0.78$ |
| 集中不等式 | 有限提示采样的可靠性 | Table 3: 随机输入仍有效 |
| 维度下界 $O(\log K)$ | $L$ 不随模型数线性增长 | 305模型仅需128维 |

## 实验与关键发现

### 核心实验设置

实验覆盖305个异构LLM，涵盖不同架构（编码器-解码器、仅解码器）、参数规模和组织来源。DNA提取采用**RepTrace**流水线：从数据集中采样$t$个提示，调用LLM生成响应，通过句子嵌入模型（默认Qwen3-Embedding-8B）将每个响应映射为固定维度语义向量，串联后经随机高斯矩阵投影至$L$维DNA空间。关系检测任务中，正样本对来自同一模型家族（如微调、合并、蒸馏关系），负样本对为独立训练的模型。评估指标包括AUC、F1和准确率，所有实验重复5个随机种子报告均值与标准差。

### 关系检测主结果

**Table 1**展示了DNA在LLM关系检测上的表现。DNA（BGE嵌入器）配合SVM分类器达到**AUC 0.992 ±0.023**，F1为**0.940 ±0.050**，相比PhyloLM+SVM的AUC 0.788 ±0.060和F1 0.766 ±0.057，分别提升**+0.204**和**+0.174**。这一差距的核心原因在于：PhyloLM基于token级分布距离，对分词器差异敏感，且忽略语义信息；而DNA通过句子级语义嵌入捕获功能行为，配合随机投影保持功能空间的距离结构，天然跨分词器、跨架构可比。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_UIxHaAqFqQ/figures/015_Figure_10.jpg]]
*Figure 10: Relationship prediction performance (Table 1) under different DNA dimensions L. Results are averaged over five random seeds; error bars denote standard deviation*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_UIxHaAqFqQ/figures/004_Table_1.jpg]]
*Table 1: DNA LLM-relation detection test performance (mean ±standard deviation across five seeds)*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_UIxHaAqFqQ/figures/014_Figure_9.jpg]]
*Figure 9: Relationship prediction performance (Table 1) under different output dimensions p of the sentence-embedding model. Results are averaged over five random seeds; error bars denote standard deviation*

DNA的区分能力在**Figure 2**中得到直观验证：以Llama-2-7B-hf为参照，公开文档标注为"相关"和"独立"的两类模型，其DNA在RBF核SVM下形成清晰分离的决策边界，表明DNA能够有效编码模型间的功能亲缘关系。

### 模型路由任务

**Table 2**报告了DNA在模型路由上的表现。DNA（冻结表示）达到**准确率0.672 ±0.008**，略优于EmbedLLM的0.665 ±0.003（+0.007）。值得注意的是，EmbedLLM需要在固定模型集上训练表示，新增模型需重新学习；而DNA完全无训练、任务无关，每个模型独立计算，可直接扩展。在此前提下仍能取得可比甚至更优性能，验证了DNA作为通用功能指纹的实用价值。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_UIxHaAqFqQ/figures/005_Table_2.jpg]]
*Table 2: DNA-based routing accuracy on test set*

### 输入分布鲁棒性

**Table 3**展示了使用随机词语输入（而非标准数据集）提取DNA的关系预测性能。DNA（Qwen3）达到F1 **0.952 ±0.048**，甚至略优于使用标准基准数据的结果，且大幅领先PhyloLM的0.766 ±0.057（+0.186）。这表明DNA对输入分布不敏感，其功能表征能力不依赖于精心设计的提示集，进一步验证了随机投影框架的泛化性。

### 聊天模板消融

**Table 4**比较了有无聊天模板的DNA提取效果。移除聊天模板后，Qwen3嵌入器的关系预测准确率提升1-3个百分点。原因在于：指令微调模型使用的特定聊天格式（如`<|user|>`标记）引入了与功能无关的表面差异，对跨家族比较构成偏差。无模板提取消除了这一混淆因素，使得仅解码器的指令模型与基础模型之间的功能距离更加公平可比。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_UIxHaAqFqQ/figures/008_Table_4.jpg]]
*Table 4: DNA relation prediction performance: with vs without chat templates*

### DNA维度与嵌入器维度分析

**Figure 10**显示DNA目标维度$L$的影响：当$L$从2增至128时，关系预测性能快速收敛，继续增大至1024无显著增益。这与定理3.3一致——所需维度仅需$O(\log K)$量级即可保持功能空间的距离信息。**Figure 9**表明句子嵌入模型的输出维度$p$对DNA质量影响微小，即使使用较小维度也可获得相近性能，说明语义嵌入本身的信息冗余度较高，随机投影能有效压缩。

### 嵌入器一致性

**Figure 8**展示了三种不同句子嵌入模型（Qwen3-Embedding-8B、BGE、E5）生成DNA的Mantel检验结果。不同嵌入器产生的DNA距离矩阵之间高度相关，表明DNA表示的核心结构不依赖于特定嵌入器的选择，方法具有良好的嵌入器鲁棒性。

### 规模无关性验证

**Table 6**通过点双列相关系数检验了模型参数规模与DNA分类准确性之间的关系。所有嵌入器配置下的$p$值均大于0.05，不显著，证明DNA捕获的是功能行为而非模型规模。这一性质对于公平比较不同规模的模型至关重要，避免了"大模型天然更相似"的虚假关联。

### 同分词器条件下的验证

**Table 7**在仅使用Qwen2Tokenizer的模型子集上评估DNA性能，结果依然保持高水平。这排除了"DNA仅靠分词器差异区分模型"的替代解释，证明功能语义捕获是性能的核心驱动力。

### 微调对DNA的影响

**Figure 5**追踪了Llama3-8B-Instruct在不同规模OpenMathInstruct-2子集上全参数微调后的DNA偏移。DNA的L2距离随微调数据量从10样本时的0.69单调增至10,000样本时的0.80，呈现渐进漂移而非突变。这验证了DNA的"遗传性"——微调产生的功能变化在DNA空间中表现为连续轨迹，而非跳跃到无关区域。

### 谱系树构建

**Figure 6**展示了基于DNA ℓ₂距离、采用Neighbor-Joining算法构建的LLM家族谱系树。谱系树清晰反映了从编码器-解码器架构向仅解码器架构的历史转变，模型按组织来源和时间演化自然聚类。**Table 5**列举了DNA发现的未记录模型关系示例，表明DNA不仅能验证已知关系，还能揭示文档中未声明的潜在亲缘（如未公开的微调来源或模型合并），具有实际取证价值。

### DNA稳定性检验

**Figure 3**通过Mantel检验评估了DNA在不相交数据集上的稳定性。两个独立数据集提取的DNA距离矩阵之间Pearson相关系数达0.7797（$p < 0.0001$），表明DNA表示对提示采样的具体选择具有高度稳定性，这是其作为可靠模型指纹的前提条件。

### 全局可视化

**Figure 4**展示了305个模型DNA的t-SNE投影，按发布组织着色。同一组织的模型形成紧密聚类，而不同组织占据不同区域，背景区域通过局部DBSCAN勾勒。该可视化直观确认了DNA能够无监督地恢复模型的谱系结构，无需任何组织标签或架构信息。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_UIxHaAqFqQ/figures/018_Table_8.jpg]]
*Table 8: Full list of used 305 models, including their architectures, parameter counts, and licenses*

## 定位与知识库关联

### 1. 核心瓶颈与突破

现有LLM表征方法在追踪模型演化时面临两个根本性瓶颈。第一，**基于token分布的方法**（如 **PhyloLM** (Yax et al., 2025)）通过计算模型输出token分布的遗传距离来推断关系，但该方法受限于分词器差异——不同模型使用不同分词器时，token空间无法直接对齐，且token级距离天然忽略语义等价性（同一语义可由不同token序列表达）。第二，**基于学习嵌入的方法**（如 **EmbedLLM** (Zhuang et al., 2025)）需在固定模型集合上训练路由嵌入，新增模型时必须重新训练整个嵌入空间，无法应对海量异构LLM持续涌现的演化分析需求。

RepTrace的核心突破在于将LLM视为从有限输入集到logits向量的**函数**，赋予其Hilbert空间结构，并利用**Johnson-Lindenstrauss引理**保证的存在性，通过随机高斯投影将该函数映射到满足双利普希茨条件的低维DNA空间。这一构造使得功能相似的模型天然具有相近的DNA表示，且提取过程**无需训练、独立于架构与分词器**，每个LLM可独立计算DNA，新模型可直接加入而不改变已有表示。

### 2. 方法差异的关键维度

与现有方法相比，RepTrace在三个关键维度上实现了根本性转变：

**表示粒度与语义捕获**。PhyloLM使用token级分布距离，EmbedLLM学习任务特定的嵌入。RepTrace则采用句子级语义嵌入——通过预训练句子嵌入模型（如Qwen3-Embedding-8B）将LLM响应映射为固定维度的语义向量，从根本上规避了分词器差异问题，同时捕获了功能语义而非表面形式。

**可扩展性与训练需求**。EmbedLLM需在固定模型集上训练，新增模型需重新学习整个嵌入空间；PhyloLM难以有效处理异构架构与分词器。RepTrace完全无训练、任务无关，每个LLM独立计算DNA，天然支持大规模、持续增长的模型集合分析。

**距离度量近似方法**。基线方法直接计算输出分布或嵌入相似度。RepTrace引入随机功能距离——通过有限提示采样的期望拼接嵌入来近似Hilbert空间中的函数距离，并由集中不等式（Lemma 4.2）保证经验估计的可靠性。这一设计使得DNA提取在计算上可行，同时保持理论上的距离保持性质。

### 3. 适用边界与局限

尽管RepTrace在305个异构LLM上展现出卓越的关系检测能力（AUC 0.992），其适用边界受以下因素制约：

**外部嵌入模型的依赖性**。DNA提取依赖外部句子嵌入模型（如Qwen3-Embedding-8B、BGE），其质量和领域偏移可能影响最终表示。消融实验表明，不同嵌入模型生成的DNA在Mantel检验中高度一致（Figure 8），但极端领域偏移下的鲁棒性尚未充分验证。

**DNA子序列的语义缺失**。目前无法为DNA子序列赋予数学意义，难以描述特定功能特质（如数学推理能力、安全对齐程度）如何由不同演化操作（领域微调、蒸馏、合并）影响。这限制了DNA从“关系检测”向“功能归因”的深化。

**API模型的输出获取障碍**。对于拒绝响应随机字符串的API模型，当前管道无法强制获取有效输出，导致无法提取DNA。这一问题在闭源商业模型的演化追踪中尤为突出。

**自适应攻击的脆弱性**。方法未针对自适应攻击进行鲁棒性设计——攻击者可能通过针对性训练使模型在保持功能的同时逃避谱系检测，这一问题在模型版权和溯源场景中具有实际威胁。

### 4. 开放问题

**DNA子序列的功能语义化**。如何为DNA子序列赋予数学意义，量化特定演化操作（如领域微调、蒸馏、模型合并）对功能特质的影响？这需要建立DNA空间中的方向性与功能变化之间的映射关系，可能涉及对投影矩阵A的列向量进行功能归因分析。

**适应性攻击的防御**。如何使DNA提取抵御适应性攻击，防止攻击者通过训练使模型逃避血统检测？这可能需要引入对抗性投影或认证鲁棒性机制，确保DNA在对抗扰动下的距离保持性质。

**非文本生成模型的扩展**。当前框架依赖文本响应作为功能表征的媒介。是否能够将DNA框架扩展至仅编码器模型（如BERT系列）以及多模态模型？对于仅编码器模型，可能需要重新定义“功能”的度量空间；对于多模态模型，则需要统一的跨模态语义嵌入。

**API模型的功能探测**。如何处理API模型拒绝随机字符串输出，导致无法获取功能表示的情况？可能的解决方向包括设计“无害但信息丰富”的探测提示集，或利用模型在拒绝响应中的行为模式作为替代功能信号。

## 原文 PDF

![[paperPDFs/ICLR_2026/LLM_DNA_Tracing_Model_Evolution_via_Functional_Representations.pdf]]
