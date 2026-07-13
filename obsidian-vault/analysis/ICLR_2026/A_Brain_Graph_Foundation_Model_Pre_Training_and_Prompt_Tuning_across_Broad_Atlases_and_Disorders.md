---
title: "A Brain Graph Foundation Model: Pre-Training and Prompt-Tuning across Broad Atlases and Disorders"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Brain_Graph_Foundation_Model_Pre_Training_and_Prompt_Tuning_across_Broad_Atlases_and_Disorders.pdf
project_link: null
code_link: https://github.com/weixinxu666/BrainGFM
aliases:
- BGFMPTPTABAD
- BrainGFM
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "引入图结构表示、多图谱预训练、图提示与语言提示联合调优，以及元学习优化。"
primary_logic: "通过将fMRI数据构建为脑图，并利用图对比学习与图掩码自编码器进行预训练，结合元学习优化的图提示和语言提示，BrainGFM能够在多种图谱、疾病和任务上实现高效的全样本、少样本和零样本迁移。"
claims:
- "BrainGFM在10种脑疾病上达到最先进性能，例如在Schaefer100图谱上AUC达70.3±1.6，ACC达70.5±1.5。"
- "结合图提示、元学习和语言提示在少样本和零样本设置下逐步提升准确率。"
- "使用所有8种图谱进行预训练（All Atlases）在ABIDE II上达到最佳性能（FT Acc 70.5/73.3），优于单一图谱或单一分辨率预训练。"
- "结合GCL和GMAE的预训练方法优于单独使用其中任何一种。"
---

# A Brain Graph Foundation Model: Pre-Training and Prompt-Tuning across Broad Atlases and Disorders

> [!tip] 核心洞察
> 通过将fMRI数据构建为脑图，并利用图对比学习与图掩码自编码器进行预训练，结合元学习优化的图提示和语言提示，BrainGFM能够在多种图谱、疾病和任务上实现高效的全样本、少样本和零样本迁移。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 脑图基础模型：跨广泛图谱与疾病的预训练与提示调优 |
| 英文题名 | A Brain Graph Foundation Model: Pre-Training and Prompt-Tuning across Broad Atlases and Disorders |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=PeGHkAaRxs) · [GitHub](https://github.com/weixinxu666/BrainGFM) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | BrainGFM |
| Dataset | ABIDE II (ASD vs. NC), ADHD200 (ADHD vs. NC), ADNI 2 (AD vs. NC) |

> [!tip] 效果简介
> - ABIDE II (ASD vs. NC) 上，AUC 为 73.3，对比 70.5 (BrainLM)，变化 +2.8。
> - ABIDE II (ASD vs. NC) 上，ACC 为 70.5，对比 68.2 (BrainLM)，变化 +2.3。
> - ADHD200 (ADHD vs. NC) 上，AUC 为 71.2，对比 68.5 (BrainLM)，变化 +2.7。

## 概要

本文提出**脑图基础模型（BrainGFM）**，旨在解决现有fMRI基础模型受限于单一脑图谱、无法有效整合异构数据且缺乏少样本/零样本适应能力的瓶颈。核心思路是将fMRI数据构建为脑图（节点为ROI，边为功能连接），通过**图对比学习（GCL）** 与**图掩码自编码器（GMAE）** 进行预训练，并引入**图提示**与**语言提示**联合调优，辅以**元学习**优化，从而在冻结骨干网络的前提下实现高效迁移。

方法定位上，BrainGFM区别于时间序列模型（如BrainLM、BrainBERT）和连接组/FC模型（如BrainNetCNN），采用图Transformer骨架与随机游走结构编码（RWSE），并在预训练阶段整合了8种图谱（功能性如Schaefer系列、解剖性如AAL系列），覆盖27个数据集、25种脑疾病、超过25,000名受试者与60,000次fMRI扫描。

主要结果方面：在Schaefer100图谱上，BrainGFM在10种脑疾病上达到最先进性能，例如ABIDE II（ASD分类）AUC达73.3±1.4，ADNI 2（AD分类）AUC达80.3±2.6，均显著优于BrainLM等基线。消融实验表明，使用全部8种图谱预训练优于单一图谱或单一分辨率方案，且GCL与GMAE联合预训练优于单独使用任何一种。在少样本和零样本设置下，逐步引入图提示、元学习与语言提示可带来持续的准确率提升，验证了该方法在数据稀缺场景下的有效性。

功能性磁共振成像（fMRI）已成为研究大脑功能连接和精神疾病生物标志物的核心工具。然而，现有fMRI基础模型面临一个根本性瓶颈：它们几乎完全依赖于**单一脑图谱/分区方案**。无论是基于时间序列的模型（如BrainLM、BrainBERT）还是基于连接组/功能连接（FC）的模型（如BrainNetCNN），其数据表示形式——时间序列或ROI级特征——都隐含地绑定于特定的图谱定义。这导致模型无法有效整合来自不同图谱的异构数据，严重限制了其泛化能力。更关键的是，这些模型缺乏对**少样本（few-shot）和零样本（zero-shot）**场景的适应能力，而临床实践中常面临标记数据稀缺甚至完全无标签的新疾病诊断任务。

为解决上述问题，BrainGFM引入了一个因果性的设计转变：**将fMRI数据统一表示为脑图（brain graph）**，其中节点为脑区（ROI），边为功能连接强度。这一表示形式天然地与图谱解耦，使模型能够处理不同分区方案下的数据。在此基础上，论文提出了一个三阶段框架：首先，利用**图对比学习（GCL）**和**图掩码自编码器（GMAE）**在跨8种图谱、27个数据集、25种疾病的超大规模数据上进行预训练（覆盖超过25,000名受试者、60,000次fMRI扫描、400,000个图样本）；其次，引入**图提示调优（graph prompt-tuning）**，通过元学习优化可学习的节点和边提示，冻结骨干网络，实现高效的少样本迁移；最后，结合**语言提示（language prompts）**，使用BioClinicalBERT编码疾病/任务和图谱/分区的文本描述，实现零样本泛化。

核心洞察在于：通过将fMRI数据转化为图谱无关的图结构，并利用图级预训练策略学习跨图谱的通用脑连接表征，BrainGFM能够突破单一图谱的局限性。实验证据支持这一设计：在Schaefer100图谱上，BrainGFM在10种脑疾病上达到最先进性能（平均AUC 70.3±1.6，ACC 70.5±1.5），显著优于BrainLM等基线；使用所有8种图谱进行预训练在ABIDE II上达到最佳性能（FT Acc 70.5/73.3），优于仅使用功能图谱或解剖图谱；结合GCL和GMAE的预训练方法优于单独使用任何一种。值得注意的是，图提示调优（乘法插入+边提示）在ABIDE II上甚至超越了全微调（ACC 71.2 vs. 70.5，AUC 73.5 vs. 73.3），展示了参数高效调优的潜力。

然而，当前证据存在一些缺口：论文未提供完整的对比损失和MSE损失的具体公式；部分消融实验（如不同预训练方法比较）的置信度标注为0.9，表明可能存在不确定性；模型在罕见疾病上的详细性能仅展示了HBN数据集上的两个不常见疾病，缺乏更全面的评估；未分析不同年龄、性别或扫描仪型号对模型性能的影响。这些点需要后续工作或手动验证。

## 核心方法与创新机理

BrainGFM的核心创新在于**将fMRI分析从“单图谱、全微调”范式转向“多图谱预训练+提示调优”的统一框架**，解决了现有fMRI基础模型受限于单一脑图谱/分区方案、无法有效整合异构数据、且缺乏少样本和零样本适应能力的瓶颈。

**关键变更槽位 (Changed Slots)：**

1.  **数据表示形式**：现有基线（如BrainLM、BrainBERT）使用原始时间序列或ROI级功能连接（FC）作为输入；BrainGFM则构建**脑图**，以ROI为节点、功能连接为边。节点特征定义为该ROI与所有其他ROI的皮尔逊相关性剖面（$\\mathbf{x}_i = \\mathbf{A}_{i,:}$），邻接矩阵通过二值化皮尔逊相关得到（$\\mathbf{A}_{ij} = \\frac{\\operatorname{Cov}(\\mathbf{t}_i, \\mathbf{t}_j)}{\\sigma(\\mathbf{t}_i) \\cdot \\sigma(\\mathbf{t}_j)}$）。这一表示将时间序列数据转换为结构化的图数据，为后续的图级预训练和提示调优奠定了基础。

2.  **预训练数据规模与多样性**：现有模型通常只在单一图谱（如Schaefer100）上预训练；BrainGFM使用了**8种不同的功能性和解剖性图谱/分区方案**，覆盖27个数据集、25种疾病、超过25,000名受试者和60,000次fMRI扫描。消融实验（Table 2）明确显示：使用所有8种图谱进行预训练（All Atlases）在ABIDE II上达到最佳性能（FT Acc 70.5/AUC 73.3），显著优于仅使用功能图谱（70.2/72.8）或仅使用解剖图谱（69.5/72.0）。这一设计直接针对“无法有效整合异构数据”的瓶颈。

3.  **下游适应策略**：现有模型依赖全参数微调（Full Fine-Tuning）；BrainGFM引入了**图提示调优（Graph Prompt Tuning）** 和**语言提示调优（Language Prompt Tuning）**，在冻结预训练骨干网络的前提下，仅更新少量可学习参数。图提示调优通过乘法插入（multiplicative insertion）方式注入可学习的节点和边提示向量，并在少样本场景下使用元学习（MAML风格）优化提示。语言提示调优则使用BioClinicalBERT编码疾病/任务的文本描述，生成语义丰富的文本嵌入作为提示。Table 5显示，图提示调优（乘法插入+边提示）在ABIDE II上达到最佳性能（ACC 71.2, AUC 73.5），甚至优于全微调（70.5/73.3）。

4.  **少样本/零样本能力**：现有模型不支持少样本或零样本迁移；BrainGFM通过**元学习优化的图提示**支持少样本学习，通过**语言提示**支持零样本迁移。Figure 2展示了在ABIDE II、ADHD 200和ADNI 2三个数据集上，从基础FM到加入图提示、元学习、再到语言提示的渐进式性能提升，尤其是在少样本和零样本设置下提升最为显著。

**核心洞察 (Core Insight)**：BrainGFM的成功表明，fMRI基础模型的关键在于**将异质性的图谱信息编码为统一的图表示**，并通过**提示调优**而非全微调来适应下游任务。预训练阶段采用图对比学习（GCL）和图掩码自编码器（GMAE）的联合策略，分别捕获全局表示和局部结构信息（Figure 5显示两者结合优于单独使用）。位置编码方面，随机游走结构编码（RWSE）在ABIDE II上取得最佳性能（ACC 70.5, AUC 73.3），优于拉普拉斯PE、节点度PE和脑梯度PE（Table 7），表明图结构信息的编码方式对脑图表示学习至关重要。

**因果机制**：多图谱预训练 → 学习图谱无关的通用脑功能连接模式 → 图提示调优保留这些通用模式 → 元学习优化提示适应少样本任务 → 语言提示实现零样本迁移。这一链条的每一步都有消融实验支撑，因果链条清晰。

BrainGFM 的完整 pipeline 包含四个核心阶段，如图 Figure 1 所示：**(a) 大规模 fMRI 脑图数据集构建** → **(b) 多图谱图预训练** → **(c) 元学习优化的图提示调优 (少样本)** → **(d) 语言提示引导的零样本迁移**。该设计旨在解决现有 fMRI 基础模型受限于单一脑图谱、无法有效整合异构数据，且缺乏少样本/零样本适应能力的根本瓶颈。

**阶段 (a): fMRI 脑图构建**。原始 fMRI 时间序列被转换为图结构数据。具体地，对于每个受试者，依据选定的脑图谱（共 8 种，涵盖功能性与解剖性分区方案）将大脑划分为 N 个 ROI（感兴趣区域）。节点特征向量定义为该 ROI 与所有其他 ROI 的皮尔逊相关性剖面 ( $\mathbf{x}_i = \mathbf{A}_{i,:}$ )，其中邻接矩阵 $\mathbf{A}_{ij}$ 由 ROI i 和 j 时间序列的皮尔逊相关系数计算得到（公式见 Appendix H）。边则通过对该相关系数矩阵进行 top-K 二值化稀疏化得到，以构建功能连接图。此步骤将原始的 4D fMRI 数据统一为图结构表示，为后续多图谱预训练奠定基础。预训练数据集规模庞大，涵盖 27 个数据集、25 种疾病、超过 25,000 名受试者、60,000 次 fMRI 扫描，并生成了 400,000 个图样本。

**阶段 (b): 多图谱图预训练**。这是 BrainGFM 的核心能力来源。模型采用 Graph Transformer (Yun et al., 2019) 作为骨干网络，并引入随机游走结构编码 (RWSE) 作为位置编码策略。预训练过程联合使用了两种自监督方法：
1.  **图对比学习 (GCL)**：通过对输入脑图随机丢弃节点和边来生成正负样本对，并使用 NT-Xent 损失函数最大化正样本对（同一图的不同增强视图）的相似度，同时最小化与负样本对（不同图）的相似度。该方法侧重于捕获脑图的全局表征。
2.  **图掩码自编码器 (GMAE)**：随机掩码输入脑图中的节点和边，然后通过编码器-解码器架构重建被掩码部分，使用均方误差 (MSE) 损失进行优化。该方法侧重于学习局部结构细节。

GCL 和 GMAE 共享同一个编码器，该编码器构成了 BrainGFM 的核心。一个关键创新是引入了**图谱/分区 Token [A/P]**。这些可学习的 token 被附加到每个图的输入中，用于编码该图源自特定图谱（如 Schaefer100、AAL116）的信息。这使得模型能够在一个统一的框架内学习来自不同图谱的异构数据，从而在预训练阶段捕获跨图谱的通用脑网络表征。消融实验（Table 2）证实，使用所有 8 种图谱进行预训练（All Atlases）在 ABIDE II 上取得了最佳性能（FT Acc 70.5/73.3），显著优于仅使用单一图谱或单一类型图谱的预训练。

**阶段 (c): 图提示调优 (少样本)**。在下游任务适应阶段，BrainGFM 采用参数高效的提示调优策略，而非全模型微调。具体地，向预训练并冻结的骨干网络输入层注入一组可学习的**图提示**，包括可学习的节点提示向量和边提示矩阵。这些提示通过模型的前向传播与原始输入交互，以引导模型适应特定任务。为了在极少量样本（如每类 1-5 个样本）下也能有效优化这些提示，论文引入了**元学习框架**（基于 MAML）。元学习在多个由不同疾病和分区方案定义的任务上进行训练，目标是学习一个提示初始化，使其能够通过少量几步梯度更新就快速适应新任务。实验（Figure 2, Table 5）表明，结合图提示和元学习（G-Prompt + Meta L.）在少样本设置下显著提升了准确率，并且乘法插入方式的图提示优于加法插入。

**阶段 (d): 语言提示调优 (零样本)**。为实现对完全未见过的疾病、数据集或图谱的零样本迁移，BrainGFM 进一步引入了**语言提示**。该阶段冻结了模型骨干网络和已学习到的图提示。具体地，使用预训练的语言模型 BioClinicalBERT 对下游任务的文本描述（例如，疾病描述“Autism Spectrum Disorder”和“Typical Control”）进行编码，生成**任务/疾病 Token [T/D]**。同样，对目标图谱或分区的文本描述进行编码，生成**图谱/分区 Token [A/P]**。这些富含语义的文本嵌入被注入到冻结的图模型中，作为上下文引导模型进行预测，而无需任何目标域的标注样本。实验（Figure 2）证明，在零样本设置下，语言提示（Lan. Prompt）的加入带来了进一步的性能提升。

**整体输入输出流**：原始 fMRI 数据 → 脑图构建（节点特征 + 邻接矩阵）→ 输入 Graph Transformer 编码器（结合 RWSE 和 [A/P] Token）→ 输出图级表征。下游任务时，该表征可结合图提示（少样本）或语言提示（零样本）用于分类。整个框架在性能和效率之间取得了最佳平衡（Figure 4），优于时间序列基础模型（如 BrainLM, BrainBERT）和连接组/FC 基础模型（如 BrainNetCNN, BrainGNN）。

### 1. fMRI脑图构建

BrainGFM将原始fMRI时间序列转化为图结构数据。每个脑图谱/分区方案的每个ROI视为一个节点，节点特征为该ROI与所有其他ROI的功能连接剖面，边由二值化的功能连接强度定义。

**邻接矩阵（功能连接）**：ROI i与ROI j之间的皮尔逊相关系数

$$ \mathbf { A } _ { i j } = \frac { \operatorname { C o v } ( \mathbf { t } _ { i } , \mathbf { t } _ { j } ) } { \sigma ( \mathbf { t } _ { i } ) \cdot \sigma ( \mathbf { t } _ { j } ) } \in [ - 1 , 1 ] $$

其中 $\mathbf{t}_i$ 和 $\mathbf{t}_j$ 分别为ROI i和j的fMRI时间序列，$\sigma(\cdot)$ 为标准差。该值衡量两个脑区之间的功能连接强度。

**节点特征向量**：节点i的特征定义为该ROI与所有其他ROI的相关性剖面：

$$ \mathbf { x } _ { i } = \mathbf { A } _ { i , : } \in \mathbb { R } ^ { N } $$

即邻接矩阵的第i行，维度为N（ROI总数）。这种设计使每个节点包含其与全脑的功能连接模式。

**图稀疏化**：对邻接矩阵进行Top-K二值化处理，仅保留每个节点最强的K个连接，将边设为0/1二值。消融实验（Table 3）显示，Pearson Top-K方法在HBN数据集MDD诊断中达到85.5%准确率，优于KNN（86.7%）、偏相关（84.8%）、互信息（83.9%）和动态连接（85.7%）。

### 2. 位置编码

由于Graph Transformer不具备序列位置概念，BrainGFM引入图结构位置编码。消融实验（Table 7）表明，随机游走结构编码（RWSE）在ABIDE II上取得最佳性能（ACC 70.5, AUC 73.3）。

**归一化拉普拉斯矩阵**（用于拉普拉斯位置编码）：

$$ L = I - D^{-1/2} A D^{-1/2} $$

其中D为度矩阵，A为邻接矩阵。该矩阵的特征向量编码了图的全局结构信息。

**随机游走结构编码（RWSE）**：

$$ \text{PE}_{\text{RWSE}}(v_i) = [(P^1)_{ii}, (P^2)_{ii}, ..., (P^T)_{ii}] $$

其中P为归一化邻接矩阵，$(P^t)_{ii}$ 为从节点i出发经过t步随机游走后返回节点i的概率。该编码捕获节点的局部结构角色（如是否属于稠密子图），且计算效率高于拉普拉斯特征分解。

### 3. 图掩码自编码器预训练（GMAE）

GMAE随机掩码输入图的节点和边，通过编码器-解码器架构重建被掩码的部分。

**掩码节点特征矩阵**：定义每个节点的输入特征

$$ \tilde { \mathbf { x } } _ { i } = \left\{ \begin{array} { l l } { \mathbf { x } _ { [ M ] } , } & { \mathrm { i f } \ v _ { i } \in \mathscr { V } _ { M } } \\ { \mathbf { x } _ { i } , } & { \mathrm { o t h e r w i s e } } \end{array} \right. $$

若节点i被掩码（属于掩码节点集合 $\mathscr{V}_M$），其原始特征 $\mathbf{x}_i$ 被替换为可学习的掩码token $\mathbf{x}_{[M]}$；否则保留原始特征。

**损坏的邻接矩阵**：对边进行随机丢弃

$$ \tilde { \mathbf { A } } = \mathbf { A } \odot \mathbf { M } _ { e } $$

其中 $\mathbf{M}_e$ 为从伯努利分布采样的二值掩码矩阵，$\odot$ 为元素级乘法。该操作模拟边缺失，迫使模型学习图的结构鲁棒性。

**重建损失（MSE）**：仅在掩码节点上计算

$$ \mathcal { L } _ { \mathrm { r e c } } = \frac { 1 } { | \mathcal { V } _ { M } | } \sum _ { v _ { i } \in \mathcal { V } _ { M } } \| \hat { \mathbf { x } } _ { i } - \mathbf { x } _ { i } \| _ { 2 } ^ { 2 } $$

其中 $\hat{\mathbf{x}}_i$ 为解码器对节点i的预测特征，$\mathbf{x}_i$ 为原始特征。该损失迫使模型学习节点间的功能连接模式，从而理解脑区间的协同关系。

### 4. 图对比学习预训练（GCL）

GCL通过随机丢弃节点和边生成同一图的两个增强视图作为正样本对，不同图的增强视图作为负样本对，使用NT-Xent损失进行对比学习。

**NT-Xent对比损失**：

$$ \mathcal { L } _ { \mathrm { C L } } = - \frac { 1 } { B } \sum _ { b = 1 } ^ { B } \log \frac { \exp ( \sin ( z _ { q } ^ { ( b ) } , z _ { k } ^ { ( b ) } ) / \tau ) } { \sum _ { b ^ { \prime } = 1 } ^ { B } \mathcal { k } _ { [ b ^ { \prime } \neq b ] } \exp ( \sin ( z _ { q } ^ { ( b ) } , z _ { k } ^ { ( b ^ { \prime } ) } ) / \tau ) } $$

其中B为批次大小，$z_q^{(b)}$ 和 $z_k^{(b)}$ 分别为第b个样本的查询和键表示（来自同一图的两个增强视图），$\sin(\cdot,\cdot)$ 为余弦相似度，$\tau$ 为温度参数，$\mathcal{k}_{[b' \neq b]}$ 为指示函数（负样本对）。该损失最大化正样本对的相似度，最小化与负样本对的相似度，迫使模型学习图级别的判别性表示。

**GCL与GMAE的互补性**：消融实验（Figure 5, 置信度0.9）显示，结合GCL和GMAE的预训练方法优于单独使用任何一种。GCL侧重于全局表示，GMAE侧重于局部结构重建，两者共享同一编码器，形成互补。

### 5. 图谱/分区Token与任务/疾病Token

BrainGFM引入两类可学习token来编码元信息：

- **图谱/分区Token [A/P]**：在预训练阶段，为每个图谱/分区方案分配一个可学习的token，与脑图节点特征拼接。这使得模型能够区分来自不同图谱的输入，实现多图谱统一预训练。
- **任务/疾病Token [T/D]**：在下游适应阶段，为每个疾病/任务分配一个可学习的token，引导模型关注特定疾病的脑网络模式。

### 6. 预训练与下游适应流程

BrainGFM的核心编码器为Graph Transformer，预训练阶段通过GCL和GMAE联合优化共享编码器。下游适应时，冻结编码器参数，仅更新图提示（可学习的节点和边向量）和语言提示（由BioClinicalBERT编码的文本描述）。元学习（MAML风格）用于优化少样本设置下的图提示，语言提示则支持零样本迁移至未见过的疾病和数据集。

**关键设计因果链**：多图谱脑图构建 → 统一图表示 → GCL+GMAE联合预训练 → 图谱无关的鲁棒编码器 → 图提示+语言提示冻结调优 → 跨图谱、跨疾病、跨任务泛化。

## 实验与关键发现

### 主结果：跨10种脑疾病的最优性能

BrainGFM在Schaefer100图谱上对10种脑疾病的分类任务中全面超越现有基线，包括时间序列基础模型（BrainLM, BrainBERT）、连接组/FC基础模型（BrainNetCNN）以及图神经网络方法（BrainGNN, fMRI-GNN）。关键指标见表1：在ABIDE II（ASD vs. NC）上，BrainGFM的AUC达到73.3±1.4，ACC为70.5±1.5，分别比最强基线BrainLM高出2.8和2.3个百分点；在ADHD 200上AUC为71.2±1.9（+2.7），在ADNI 2（AD vs. NC）上AUC为80.3±2.6（+3.8），在HBN（MDD vs. NC）上AUC为79.9±1.6（+3.8）。这一致胜模式在全部10个任务中成立，证明图结构表示+多图谱预训练的核心瓶颈突破是有效的——时间序列模型无法利用ROI间的拓扑关系，而连接组模型受限于单一图谱。

![[assets/figures/papers/iclr26_0002_PeGHkAaRxs_A_Brain_Graph_Foundation_Model_Pre-Training_and/figures/002_Table_1.jpg]]
*Table 1: Comparison among different methods on 10 brain disorders on Schaefer100 atlas. Pink indicates the best performance*

Figure 4进一步展示了性能与效率的权衡：BrainGFM在AUC上显著高于所有基线，同时推理速度（ms/样本）与计算成本（GFLOPs）处于可接受范围，优于时间序列模型（BrainLM/BrainBERT）和连接组模型（BrainNetCNN），实现了最佳平衡点。

### 少样本与零样本：提示调优与元学习的增量收益

Figure 2系统展示了在ABIDE II、ADHD 200、ADNI 2三个数据集上，从全样本到少样本（每类5样本）再到零样本设置下的性能演进。核心发现：仅使用预训练模型直接微调（FM）在少样本下性能急剧下降；引入图提示（G-Prompt）后，少样本准确率提升约5-10个百分点；进一步加入元学习（Meta L.）优化图提示，再提升约3-5个百分点；最终加入语言提示（Lan. Prompt）实现零样本迁移，在零样本设置下达到约60-65%准确率（随机基线50%）。这一渐进式增益证实了因果链路的有效性：图提示提供结构先验，元学习优化少样本适应，语言提示桥接未见任务。

Figure 9在HBN数据集的两个不常见疾病（预训练阶段未见）上复现了这一模式，表明模型对真正未见疾病的零样本泛化能力是可靠的，而非仅对预训练疾病的重排。

### 消融研究：预训练数据与策略的贡献

**图谱多样性（Table 2）**：在ABIDE II上，使用全部8种图谱（All Atlases）预训练达到最高性能（FT Acc 70.5, AUC 73.3），优于仅用功能图谱（70.2/72.8）或仅用解剖图谱（69.5/72.0）。关键洞察：混合不同分辨率（如Schaefer 100+200+300）与混合不同图谱（Schaefer100+AAL116）性能相当（68.5/71.3 vs. 68.8/71.6），说明图谱多样性比单一图谱的多分辨率更重要。单一分辨率功能图谱（如Schaefer100）优于单一解剖图谱（AAL116），但都显著低于多图谱组合。

![[assets/figures/papers/iclr26_0002_PeGHkAaRxs_A_Brain_Graph_Foundation_Model_Pre-Training_and/figures/003_Table_2.jpg]]
*Table 2: BrainGFM ! 70.3±1.6 70.5±1.5 67.0±1.7 71.4±2.1 71.2±1.9 73.5±1.4 70.4±1.5 69.8±1.7 80.3±2.6 81.9±2.2 76.2±1.5 84.4±1.7 79.9±1.6 82.0±1.7 83.2±1.6 79.2±1.9 85.2±1.6 86.3±2.1 87.7±1.9 82.6±1.7*

**预训练方法（Figure 5）**：联合使用图对比学习（GCL）和图掩码自编码器（GMAE）优于单独使用任何一种——GCL捕捉全局表征，GMAE学习局部结构重建，两者互补。单独GCL或GMAE的性能差距较小，但联合训练的效果增益稳定（置信度0.9，需注意论文未提供误差条）。

**图构建方法（Table 3）**：在HBN的MDD诊断上，Pearson Top-K稀疏化（85.5%准确率）与KNN图（86.7%）性能接近，优于偏相关（84.8%）、互信息（83.9%）和动态连接（85.7%）。KNN略优但差异在1个百分点内，表明图构建方法不是主要瓶颈。

![[assets/figures/papers/iclr26_0002_PeGHkAaRxs_A_Brain_Graph_Foundation_Model_Pre-Training_and/figures/026_Table_3.jpg]]
*Table 3: Comparison of different brain graph construction methods on HBN dataset for MDD diagnosis. Our approach uses top-k sparsification of the Pearson correlation matrix to construct brain graphs. We also compare it with KNN-based graph construction. The numbers in the table represent classification accuracy*

**位置编码（Table 7）**：随机游走结构编码（RWSE）在ABIDE II上取得最佳性能（ACC 70.5, AUC 73.3），优于拉普拉斯PE（69.2/71.3）、节点度PE（67.8/70.1）和脑梯度PE（66.5/69.2）。无预训练+无位置编码时性能最低（65.2/67.1），说明两者都是必要组件。拉普拉斯PE计算成本高但性能不及RWSE。

**调优方法（Table 5）**：图提示调优（乘法插入+边提示）在ABIDE II上达到ACC 71.2, AUC 73.5，优于全微调（70.5/73.3）和PEFT方法（如Adapter, LoRA）。冻结骨干网络仅更新提示向量，在提升性能的同时大幅降低参数量，验证了提示调优在脑图基础模型上的有效性。

![[assets/figures/papers/iclr26_0002_PeGHkAaRxs_A_Brain_Graph_Foundation_Model_Pre-Training_and/figures/028_Table_5.jpg]]
*Table 5: Comparison of Different Tuning Methods on ABIDE II (ASD Classification)*

### 跨图谱迁移分析

Figure 3展示了预训练图谱与下游图谱的匹配效应：当预训练图谱与下游图谱类型一致（如功能-功能）时迁移效果最好；混合预训练（功能+解剖）在所有下游图谱上均达到最优，且对解剖图谱的增益尤为显著（从约65%提升至70%+）。Table 4在ADNI 2上进一步量化：跨图谱迁移的改进幅度为2.7%-3.3%，低于同图谱迁移（约4-5%），但混合预训练（Schaefer200+AAL116→Schaefer100）的增益（3.2%）接近同图谱水平，说明多图谱预训练可以部分弥合图谱差异。

![[assets/figures/papers/iclr26_0002_PeGHkAaRxs_A_Brain_Graph_Foundation_Model_Pre-Training_and/figures/027_Table_4.jpg]]
*Table 4: Ablation experiments on the ADNI2 dataset for Alzheimer’s disease (AD) classification. The reported improvements (%) indicate the performance gain over models without pre-training*

### 失败模式与未分析维度

论文未报告年龄、性别或扫描仪型号对模型性能的调节效应，尽管数据集覆盖5-89岁且平衡了性别（Table 17）。预训练数据全部来自公开数据集，罕见疾病的样本量有限（仅HBN两个不常见疾病有分析）。Figure 5的置信度标注为0.9，表明GCL+GMAE联合训练的增益可能存在波动。整体上，模型在少样本（每类5样本）下性能仍显著低于全样本（约10-15个百分点差距），提示在极低数据场景下仍有改进空间。

![[assets/figures/papers/iclr26_0002_PeGHkAaRxs_A_Brain_Graph_Foundation_Model_Pre-Training_and/figures/010_Table_2.jpg]]
*Table 2: Effect of different atlases on pre-training (ABIDE II, ASD)*

## 定位与知识库关联

BrainGFM 定位为图结构脑基础模型（Graph-based Brain Foundation Model），其核心瓶颈在于现有 fMRI 基础模型受限于单一脑图谱/分区方案，无法有效整合异构数据，且缺乏对少样本和零样本场景的适应能力。为解决这一问题，BrainGFM 引入了图结构表示、多图谱预训练、图提示与语言提示联合调优，以及元学习优化四个关键因果机制。

**与基线方法的关系**：BrainGFM 在方法谱系上同时挑战了两类基线——时间序列基础模型（BrainLM、BrainBERT）和连接组/FC 基础模型（BrainNetCNN），以及传统图神经网络（BrainGNN、fMRI-GNN）。其关键差异体现在三个维度：（1）**数据表示形式**从时间序列或 ROI 级特征（连接组/FC）转变为脑图（节点为 ROI，边为功能连接）；（2）**预训练数据规模与多样性**从单一图谱/分区扩展至 8 种图谱/分区（功能性和解剖性），覆盖 27 个数据集、25 种疾病；（3）**下游适应策略**从全参数微调转变为图提示调优 + 语言提示调优（冻结骨干网络）。这种设计使得 BrainGFM 成为唯一能够同时处理全样本、少样本和零样本场景的模型。

**适用边界**：实验证据表明，BrainGFM 在 10 种脑疾病上达到最先进性能（例如在 Schaefer100 图谱上 AUC 达 70.3±1.6，ACC 达 70.5±1.5），且结合图提示、元学习和语言提示在少样本和零样本设置下逐步提升准确率。消融实验进一步确认了三个关键设计选择的有效性：（1）使用所有 8 种图谱进行预训练优于单一图谱或单一分辨率预训练（ABIDE II 上 FT Acc 70.5/73.3 vs. 仅功能图谱 70.2/72.8）；（2）结合 GCL 和 GMAE 的预训练方法优于单独使用任何一种；（3）图提示调优（乘法插入+边提示）优于全微调和 PEFT 方法（ABIDE II 上 ACC 71.2, AUC 73.5 vs. 全微调 70.5/73.3）。在效率维度，BrainGFM 在性能和效率之间取得了最佳平衡，优于时间序列和连接组/FC 基础模型。

**局限**：尽管 BrainGFM 展示了强大的跨图谱迁移能力，但仍存在若干未解决的问题。首先，论文未提供完整的对比损失和 MSE 损失的具体公式，仅描述了概念，这增加了复现的难度。其次，部分实验（如 Figure 5 中不同预训练方法的比较）的置信度标注为 0.9，表明可能存在一定的不确定性。第三，预训练数据主要来自公开数据集，可能无法完全代表真实临床场景的多样性。第四，论文未分析不同年龄、性别或扫描仪型号对模型性能的影响，尽管所有下游任务均平衡了男性和女性样本数量。最后，模型在完全未见过的疾病（如罕见病）上的零样本性能仅展示了 HBN 数据集上的两个不常见疾病，缺乏更全面的评估。

**开放问题**：基于当前证据，以下方向值得进一步探索：（1）如何进一步扩展数据集，例如纳入完整的 OpenNeuro 存储库和 UK Biobank 数据集？（2）结合任务态和静息态 fMRI 数据能否带来更全面的脑动态表征？（3）不同的文本编码器（如 GPT 系列）对语言提示性能有何影响？（4）模型如何扩展到更大的图谱或更高分辨率的分区方案？（5）模型在完全未见过的疾病（如罕见病）上的零样本性能如何？这些问题的解决将有助于推动脑图基础模型向更普适、更鲁棒的临床诊断工具发展。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Brain_Graph_Foundation_Model_Pre_Training_and_Prompt_Tuning_across_Broad_Atlases_and_Disorders.pdf

![[paperPDFs/ICLR_2026/A_Brain_Graph_Foundation_Model_Pre_Training_and_Prompt_Tuning_across_Broad_Atlases_and_Disorders.pdf]]
