---
title: "PoseScript: Linking 3D Human Poses and Natural Language"
type: paper
paper_level: A
venue: TPAMI
year: 2024
pdf_ref: paperPDFs/TPAMI_2024/PoseScript_Linking_3D_Human_Poses_and_Natural_Language.pdf
aliases:
- PoseScript
tags:
- TPAMI_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过自动生成大规模带细粒度posecode标注的文本描述（PoseScript-A）进行预训练，再在人工标注数据（PoseScript-H）上微调，显著提升跨模态检索与生成性能。"
primary_logic: "将低层3D姿态信息分解为少量可组合的posecode，并结合语言规则生成多样化自然语言描述，从而在数据规模和语义丰富度上弥补人工标注的不足。"
claims:
- "在自动描述上预训练后，再在人工描述上微调，使得跨模态检索平均召回率从23.0%提升至40.9%（+78%）"
- "增加自动描述预训练数据量持续提升检索性能，而仅用人工数据则很快饱和。"
- "文本条件姿态生成模型在预训练后FID从0.29大幅降至0.04。"
- "PoseScript-H test 上 mRecall (平均召回率) = 40.9 ± 0.1"
---

# PoseScript: Linking 3D Human Poses and Natural Language

> [!tip] 核心洞察
> 将低层3D姿态信息分解为少量可组合的posecode，并结合语言规则生成多样化自然语言描述，从而在数据规模和语义丰富度上弥补人工标注的不足。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | PoseScript: 连接三维人体姿态与自然语言 |
| 英文题名 | PoseScript: Linking 3D Human Poses and Natural Language |
| 会议/期刊 | TPAMI 2024 |
| Links | [paper](https://arxiv.org/abs/2210.11795); [Project](https://europe.naverlabs.com/research/computer-vision/posescript/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PoseScript (带自动描述管线的数据集) |
| Dataset | PoseScript-H test |

> [!tip] 效果简介
> - PoseScript-H test 上，mRecall (平均召回率) 为 40.9 ± 0.1，对比 23.0 ± 0.6，变化 +17.9。
> - PoseScript-H test 上，text-to-pose R@10 为 57.9 ± 0.3，对比 35.7 ± 0.9，变化 +22.2。
> - PoseScript-H test 上，pose generation FID 为 0.04，对比 0.29，变化 -0.25。

## 概述

**问题瓶颈**：现有三维人体姿态数据集普遍缺乏细粒度的自然语言描述，导致姿态数据的语义理解停留在数值层面，难以支撑跨模态检索、文本条件生成等需要丰富语义对齐的下游任务。

**核心思路**：PoseScript 通过构建一个自动标注管线，将归一化的 3D 关键点姿态分解为少量可组合的底层语义原子——posecode（涵盖角度、距离、相对位置、倾斜/滚转、地面接触五类关系），再经选择、聚合与语言模板转换，生成多样化的大规模自然语言描述（PoseScript-A）。这套自动描述与少量人工精标注数据（PoseScript-H）相结合，形成“预训练 + 微调”的数据驱动范式。

**方法定位**：PoseScript 本质上是一个**数据构造方法论**而非单一模型。其自动标注管线（Fig. 5）将姿态的结构化语义显式编码为文本，使后续的跨模态检索、文本条件姿态生成和姿态描述生成模型能够从中受益。在方法谱系上，该工作属于**基于规则的知识引导型数据增强**，与依赖纯人工标注或端到端学习的传统路线形成互补。

**决定性证据**：
- 在 PoseScript-H 测试集上，经 PoseScript-A 预训练再微调的跨模态检索模型，平均召回率（mRecall）从从头训练的 **23.0 → 40.9**（+78%）；文本到姿态的 R@10 从 35.7 提升至 57.9（TABLE II）。
- 文本条件姿态生成模型在预训练后，FID 从 **0.29 大幅降至 0.04**（TABLE III）。
- 增加自动描述预训练数据量可持续提升检索性能，而仅增加人工标注数据则迅速饱和（Fig. 15），验证了自动管线在数据规模上的关键作用。

**主要结果一览**：PoseScript 支持三类多模态应用（Fig. 1）：文本到姿态检索、文本条件姿态生成、以及姿态描述生成。在跨模态检索任务上，结合 Transformer 文本编码器与镜像增强后，mRecall 可达 45.3；生成模型在预训练策略加持下实现了高保真的文本条件姿态合成。整体上，PoseScript 以极低的人工标注成本（每姿态约 3 分钟，共约 6,000 条人工描述）撬动了显著的性能增益，为三维人体姿态的语义理解提供了可复用的数据基础。

## 背景与动机

三维人体姿态理解是计算机视觉与图形学的核心问题，其应用涵盖动作识别、运动生成、人机交互等领域。近年来，大规模运动捕捉数据集（如 AMASS）的出现极大地推动了对人体运动的建模能力，但这些数据集普遍存在一个关键缺口：**缺乏与三维姿态对应的细粒度自然语言描述**。现有的文本-姿态配对数据要么仅提供粗粒度的动作标签（如“行走”“跳跃”），要么局限于特定场景的简短指令，无法捕捉姿态层面丰富的空间关系和身体部位配置信息。

这一缺口的后果是双重的。首先，它限制了**跨模态检索**的能力——用户无法通过自然语言精确查询具有特定身体姿态的三维数据。其次，它制约了**文本条件姿态生成**的质量，因为模型缺乏足够的语义监督来学习从语言到姿态空间的映射。尽管 CLIP（Radford et al., ICML 2021）等大规模视觉-语言模型在图像领域取得了突破性进展，但三维人体姿态的语义粒度远超通用图像描述所能覆盖的范围，需要专门的数据集和建模策略。

人工标注是获取高质量姿态描述的直接途径，但面临两个根本性挑战。其一，**标注成本极高**：姿态描述需要标注者同时具备空间推理能力和精确的语言表达技巧，标注一个姿态的描述往往需要数分钟。其二，**语义覆盖有限**：人工标注者倾向于关注显著的姿态特征，容易忽略细微但判别性强的身体部位关系，导致描述多样性和信息密度不足。

PoseScript 正是在这一背景下提出的。其核心动机是：**能否通过自动化管线，从三维关键点数据中提取结构化的语义信息，并据此生成大规模、多样化的自然语言描述，从而弥补人工标注在规模和覆盖度上的不足？** 这一思路的关键洞察在于，三维姿态的底层几何关系（关节角度、相对位置、身体部位接触等）可以被分解为少量可组合的语义基元（称为 posecode），再通过语言规则组合成自然语言句子。这种“从几何到语义再到语言”的管线，使得以极低成本生成数十万条姿态描述成为可能，为后续的跨模态预训练提供了数据基础。

## 核心创新

PoseScript 的核心创新在于通过 **changed slots** 策略，系统性地解决了三维人体姿态与自然语言之间的语义鸿沟问题，其关键突破体现在以下三个层面：

### 1. 预训练数据槽位：从人工标注到大规模自动描述

传统方法依赖少量人工标注数据训练跨模态模型，但人工描述成本高昂且难以覆盖姿态的多样性。PoseScript 的核心改变是将预训练数据槽位从“无（从头训练）”替换为“大规模自动描述 PoseScript-A 预训练”。这一改变的因果机制在于：自动描述管线能够以极低成本（为 100,000 个姿态各生成 3 条描述仅需不到 10 分钟）产生海量、多样化的文本-姿态对，为模型提供了丰富的语义监督信号。

**决定性证据**：
- 在 PoseScript-H 测试集上，仅使用人工数据从头训练的模型平均召回率（mRecall）仅为 23.0%，而先在 PoseScript-A 上预训练再在 PoseScript-H 上微调后，mRecall 跃升至 40.9%，**相对提升 78%**（Table II）。
- 文本条件姿态生成任务中，预训练使 FID 从 0.29 大幅降至 0.04（Table III），表明生成质量显著提高。
- 数据量消融实验（Fig. 15）显示，增加自动描述预训练数据量持续提升检索性能，而仅增加人工数据则很快饱和，证实了自动描述作为预训练槽位的不可替代性。

### 2. 文本编码器槽位：从循环网络到 Transformer

在文本编码器选择上，PoseScript 将基线 GloVe + bi-GRU 替换为 Transformer（冻结的 DistilBERT 嵌入）。这一改变利用了预训练语言模型的语义理解能力，使模型能够更好地捕捉自然语言描述中的复杂语义关系。

**决定性证据**：
- Table II 显示，使用 Transformer 文本编码器后，mRecall 从 35.1 提升至 44.5，提升幅度达 26.8%，证明了更强文本编码器对跨模态对齐的关键作用。

### 3. 数据增强槽位：镜像翻转与侧边文字替换

PoseScript 引入了针对人体姿态对称性的数据增强策略：对姿态进行镜像翻转，同时将描述中的“左/右”等侧边文字对应替换。这一改变利用了人体结构的对称性先验，在不增加额外标注成本的情况下扩充了训练数据。

**决定性证据**：
- Table II 显示，在已使用 Transformer 编码器的基础上，镜像增强进一步将 mRecall 从 44.5 提升至 45.3，虽幅度较小但方向一致，验证了该增强的有效性。

### 创新机制的内在联系

上述三个 changed slots 并非孤立存在，而是形成了互补的增强链条：**自动描述管线**提供了规模化的语义监督基础，**Transformer 编码器**提升了模型对复杂语义的建模能力，**镜像增强**则利用领域先验进一步挖掘数据潜力。三者的协同作用使得 PoseScript 在跨模态检索和生成任务上均取得了显著超越基线的性能。

## 整体框架

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2210_11795/figures/002_Figure_2.jpg]]
*Figure 2: Examples of pose descriptions from PoseScript, produced by human annotators (left) and by our automatic captioning pipeline (right)*

PoseScript 的核心贡献是构建了一条连接 3D 人体姿态与自然语言的双向通路，其整体框架由**数据管线**与**多模态应用模型**两大层级构成，二者通过统一的 posecode 语义表示紧密耦合。

### 数据管线：从姿态到结构化描述

数据管线（Fig. 5）将归一化的 3D 人体姿态转换为自然语言描述，分为四个串行模块：

1. **Posecode 提取**：从 SMPL-H 骨架的 52 个关节旋转（轴角表示）出发，计算五类底层语义关系——角度、距离、相对位置、倾斜/滚转以及地面接触，形成一组可组合的 posecode。
2. **Posecode 选择**：剔除平凡、非必要及冗余的 posecode，保留具有区分力的子集。
3. **Posecode 聚合**：按实体、对称性、关键点或语义解释对 posecode 进行合并（如将同一身体部位的多个属性合并为复合描述），减少冗余并提升自然度。
4. **Posecode 转句子**：选择主语、套用句式模板并引入随机排列，生成最终的结构化描述文本。

该管线在约 10 分钟内即可为 100,000 个姿态各生成 3 条描述，形成 **PoseScript-A**（自动描述数据集）。与之互补的 **PoseScript-H** 则通过两阶段 AMT 人工标注收集了 6,283 条高质量描述（平均长度 54.2 tokens，平均描述 6.2 个身体部位）。

### 多模态应用模型：检索、生成与描述

在数据管线之上，PoseScript 框架支持三类多模态应用，共享相同的 posecode 语义空间：

- **跨模态检索**（Fig. 7）：采用双编码器架构——文本编码器（bi-GRU + GloVe 或 Transformer + DistilBERT 冻结嵌入）与姿态编码器（VPoser 编码器）将文本和姿态映射到联合嵌入空间，通过 Batch-Based Classification（BBC）损失训练：
  $$\mathcal{L}_{\mathrm{BBC}} = -\frac{1}{B} \sum_{i=1}^{B} \log \frac{\exp\left(\gamma \sigma(x_i, y_i)\right)}{\sum_{j} \exp\left(\gamma \sigma(x_i, y_j)\right)}$$
  其中 $\sigma(x, y)$ 为 L2 归一化嵌入的余弦相似度。

- **文本条件姿态生成**（Fig. 10）：基于 VAE 架构，姿态编码器输出后验分布 $\mathcal{N}_p$，文本编码器输出先验分布 $\mathcal{N}_c$，训练损失为重建项与 KL 散度正则项之和：
  $$\mathcal{L} = \mathcal{L}_R(p, \hat{p}) + \mathcal{L}_{KL}(\mathcal{N}_p, \mathcal{N}_c)$$
  重建损失覆盖旋转矩阵、关节点位置和顶点位置。

- **姿态描述生成**（Fig. 13）：通过 cross-attention 将姿态信息注入文本 Transformer，以交叉熵损失自回归地生成描述文本。

### 输入输出流

整个框架的输入端为 AMASS 运动捕捉数据库中的 3D 人体姿态（经最远点采样选取 100,000 个高多样性姿态），输出端涵盖：给定自然语言查询的 3D 姿态检索结果、给定文本条件的 3D 姿态生成样本，以及给定姿态的自然语言描述。**核心因果机制**在于：大规模自动描述预训练（PoseScript-A）弥补了人工标注的规模瓶颈，再在人工描述（PoseScript-H）上微调，使检索平均召回率从 23.0% 提升至 40.9%（+78%），生成 FID 从 0.29 降至 0.04。

## 核心模块与公式推导

### 1. 自动标注管线（Captioning Pipeline）

PoseScript 的核心贡献之一是一套从归一化 3D 姿态自动生成结构化自然语言描述的管线，由四个级联模块构成（Fig. 5）：

**Posecode 提取（Posecode extraction）**
从 SMPL-H 骨架的 52 个关节旋转（axis-angle 表示）出发，计算五类底层语义关系：角度（如膝关节弯曲程度）、距离（如双手之间的距离）、相对位置（如左手相对于头部的位置）、倾斜/滚转（pitch/roll，如躯干前倾程度）、地面接触（如左脚是否着地）。这些关系被离散化为若干类别（如“slightly bent”、“completely bent”），形成结构化的 posecode。

**Posecode 选择（Posecode selection）**
并非所有提取的 posecode 都有信息量。该模块依次执行三步过滤：① 删除处于“平凡”状态的 posecode（如直立时躯干 pitch 为 neutral）；② 随机丢弃部分非必要 posecode 以增加多样性；③ 删除冗余 posecode（如已被其他 posecode 隐含表达的属性）。

**Posecode 聚合（Posecode aggregation）**
为减少冗余并提升生成文本的自然度，对保留的 posecode 进行合并。聚合策略包括：实体聚合（同一身体部位上的多个属性合并描述，如“左膝弯曲且左腿外展”）、基于对称性或关键点的合并、以及基于语义解释的合并（对同一类属性但作用于不同关节集的 posecode 进行统一表述）。消融实验（TABLE V）表明，启用聚合可提升检索性能，其中 N3 版本取得最优平均召回率 39.8。

**Posecode 到句子的转换（Posecode conversion into sentences）**
分两步完成：首先为每个 posecode 选择主语（如“the person”、“his left knee”），然后套用预定义的句式模板并将所有句子组合，通过随机排列生成多样化描述。管线的每一步均引入了随机化，使得同一姿态可生成多版不同表述，天然形成数据增强。

### 2. 跨模态检索模型

检索模型采用双编码器架构（Fig. 7），将文本和姿态分别映射到共享嵌入空间：

- **文本编码器**：输入标注文本经分词后，可选两种编码方案——GloVe 词嵌入 + 双向 GRU，或冻结的 DistilBERT 词嵌入 + Transformer。消融实验证实 Transformer 方案显著优于 GRU（mRecall 44.5 vs 35.1，Table II）。
- **姿态编码器**：将 52 个关节的 axis-angle 旋转矩阵展平为向量，输入 VPoser 编码器获得姿态嵌入。

训练损失采用 Batch-Based Classification (BBC) loss，公式如下：

$$\mathcal{L}_{\mathrm{BBC}} = -\frac{1}{B} \sum_{i=1}^{B} \log \frac{\exp\left(\gamma \sigma(x_i, y_i)\right)}{\sum_{j} \exp\left(\gamma \sigma(x_i, y_j)\right)}$$

其中 $B$ 为批次大小，$x_i$ 与 $y_i$ 分别为第 $i$ 个样本的文本嵌入和姿态嵌入，$\gamma$ 为温度缩放因子，$\sigma(x, y)$ 为余弦相似度：

$$\sigma(x, y) = x^{\top} y / (\|x\|_2 \times \|y\|_2)$$

该损失的目标是最大化正样本对（同一姿态-描述对）的相似度，同时最小化负样本对（批次内其他组合）的相似度，本质是在批次内执行分类任务。

### 3. 文本条件姿态生成模型

生成模型基于条件变分自编码器（Conditional VAE）架构（Fig. 10）：

- **姿态编码器** 将姿态 $p$ 映射为后验分布 $\mathcal{N}_p$（输出均值 $\mu(p)$ 和方差 $\Sigma(p)$）。
- **文本编码器** 从描述文本生成先验分布 $\mathcal{N}_c$，该分布独立于姿态本身。
- 训练时从 $\mathcal{N}_p$ 采样隐变量 $z$，解码器据此重建姿态 $\hat{p}$。

总损失函数为：

$$\mathcal{L} = \mathcal{L}_R(p, \hat{p}) + \mathcal{L}_{KL}(\mathcal{N}_p, \mathcal{N}_c)$$

其中 $\mathcal{L}_R$ 为重建损失，由三部分组成：旋转矩阵的高斯对数似然损失、关节位置损失、顶点位置损失；$\mathcal{L}_{KL}$ 为后验分布与先验分布之间的 KL 散度正则项，迫使文本条件先验逼近姿态后验。实验还尝试了额外的正则项 $\mathcal{L}_{reg}$（将 $\mathcal{N}_p$ 和 $\mathcal{N}_c$ 分别拉向标准高斯），在自动标注数据上略有帮助（FID 从 0.12 降至 0.07，Table III），但在人工数据上效果不显著。

### 4. 预训练-微调范式

上述两个下游模型均遵循统一的训练策略：先在大规模自动描述数据 PoseScript-A（约 100k 姿态 × 3 描述）上预训练，再在人工标注数据 PoseScript-H（6,283 条描述）上微调。这是本文最关键的因果调节变量——仅用人工数据从头训练时，检索平均召回率仅 23.0%，而预训练后微调可提升至 40.9%（+78%）；姿态生成 FID 从 0.29 大幅降至 0.04。数据量消融实验（Fig. 15）进一步表明，增加自动标注数据量持续提升检索性能，而仅增加人工数据则很快饱和，验证了大规模自动标注预训练的核心价值。

## 实验与分析

### 核心实验设置

PoseScript 的实验围绕三个下游任务展开：**文本到姿态检索**（text-to-pose retrieval）、**文本条件姿态生成**（text-conditioned pose generation）和**姿态描述生成**（caption generation）。数据集划分为训练集/验证集/测试集，关键公平性保障包括：同一 AMASS 序列中的姿态归属同一子集以避免数据泄漏，所有结果报告 3 次运行的平均值 ± 标准差，超参数统一（详见 TABLE VI）。

检索模型采用双编码器架构：文本编码器可选 GloVe + bi-GRU 或 Transformer（冻结 DistilBERT 嵌入），姿态编码器使用 VPoser 编码器处理 52 个 SMPL-H 关节的轴角表示（52×3 矩阵）。训练损失为 **Batch-Based Classification (BBC) loss**：

$$
\mathcal{L}_{\mathrm{BBC}} = -\frac{1}{B} \sum_{i=1}^{B} \log \frac{\exp\left(\gamma \sigma(x_i, y_i)\right)}{\sum_{j} \exp\left(\gamma \sigma(x_i, y_j)\right)}
$$

其中 $\sigma(x, y) = x^{\top} y / (\|x\|_2 \times \|y\|_2)$ 为 L2 归一化后的余弦相似度，$\gamma$ 为温度参数。

生成模型基于 VAE 框架，训练损失为：

$$
\mathcal{L} = \mathcal{L}_R(p, \hat{p}) + \mathcal{L}_{KL}(\mathcal{N}_p, \mathcal{N}_c)
$$

其中 $\mathcal{L}_R$ 包含旋转矩阵、关节位置和顶点位置的重建损失，$\mathcal{L}_{KL}$ 为姿态编码器后验分布与文本编码器先验分布之间的 KL 散度。

### 主要结果

#### 跨模态检索

TABLE II 报告了核心检索结果。在 PoseScript-H 测试集上：

- **从头训练**（仅用人工标注）：平均召回率 mRecall 仅 23.0 ± 0.6，文本到姿态 R@10 为 35.7 ± 0.9。
- **预训练 + 微调**（PoseScript-A 预训练后在 PoseScript-H 上微调）：mRecall 跃升至 **40.9 ± 0.1**（+78%），文本到姿态 R@10 达到 **57.9 ± 0.3**（+22.2 个百分点）。

这组数据直接验证了核心因果机制——大规模自动描述预训练提供了丰富的语义先验，使模型在稀缺的人工标注上能有效泛化。

进一步改进：
- 将文本编码器从 GloVe + bi-GRU 替换为 **Transformer**（冻结 DistilBERT 嵌入），mRecall 从 35.1 提升至 44.5。
- 加入**镜像数据增强**（侧边文字替换），mRecall 再提升至 45.3 ± 0.4。

#### 文本条件姿态生成

TABLE III 展示了生成模型的评估结果。关键指标为 FID（Fréchet Inception Distance）：

- 在 PoseScript-H 上从头训练：FID = 0.29。
- 在 PoseScript-A 上预训练后在 PoseScript-H 上微调：FID 降至 **0.04**，降幅达 86%。

额外正则化项 $\mathcal{L}_{reg}$（向标准高斯分布的 KL 散度）在 PoseScript-A 上有轻微帮助（FID 从 0.12 降至 0.07），但在微调场景下影响不显著。

### 消融实验

#### 自动标注管线消融（TABLE V）

对自动标注管线的各组件进行消融，考察不同 caption 版本对检索性能的影响：


![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2210_11795/figures/018_Table.jpg]]
*Table: IV CAPTION GENERATION RESULTS. THE TOP BLOCK SHOWS SOME REFERENCE MEASURES WHILE THE LOWER BLOCK EVALUATES THE GENERATED TEXTS FOR POSESCRIPT-H. RESULTS ARE AVERAGED OVER 3 RUNS. TABLE V*

- **Posecode 聚合**（Implicitness）：启用聚合（N3 版本）取得最优 mRecall 39.8，相比无聚合版本有明显提升。聚合通过实体合并和语义合并减少冗余，使生成文本更接近自然语言分布。
- **句式随机化**：管线各步骤的随机化作为数据增强手段，对泛化有正向贡献。

#### 数据量缩放实验（Fig. 15）

Fig. 15 展示了不同训练数据量对检索性能的影响，这是支撑核心洞察的关键证据：

- **仅用人工标注**（紫色曲线）：数据量增加带来的收益迅速饱和，受限于人工标注的规模（6,283 条）。
- **增加自动标注预训练数据**（绿色曲线）：随着 PoseScript-A 数据量增加，检索性能持续提升，未见明显饱和。
- 这一对比清晰表明：自动标注管线解决了人工标注的规模瓶颈，是性能提升的根本驱动力。

#### 预训练配置对比（TABLE X）

TABLE X 对比了不同预训练配置（均在 PoseScript-H 微调前评估，使用 GloVe-biGRU 配置）：

- EXP-0（无预训练）：mRecall 基准线。
- EXP-3（PoseScript-A 预训练）：mRecall 显著提升，与 TABLE II 的最终微调结果形成完整证据链。

#### 文本编码器与数据增强

- **Transformer vs. GloVe-biGRU**：Transformer 文本编码器带来约 9.4 个百分点的 mRecall 提升（44.5 vs 35.1），归因于预训练语言模型提供的更丰富语义表示。
- **镜像增强**：额外贡献约 0.8 个百分点（45.3 vs 44.5），收益虽小但一致。

### 失败模式与局限性

1. **稀有姿态的生成幻觉**：生成式描述模型在倒立等稀有姿态上易产生幻觉（Fig. 14），原因在于训练数据中此类姿态占比极低，模型缺乏足够的统计支撑。

2. **旋转信息的缺失**：当前自动标注管线未涵盖旋转相关姿态信息（如前臂扭转），因为 posecode 主要基于角度、距离和位置关系。可通过新增基于关节旋转的 posecode 扩展（Appendix B 已讨论方案）。

3. **否定表达的缺失**：自动标注不含否定表达（如 “not touching”），虽因人工描述中否定句比例极低（<5%）而影响有限，但在某些精确描述场景下可能造成语义偏差。

4. **单人姿态限制**：数据集仅覆盖单人姿态，未涉及多人交互场景，限制了模型在社交行为理解等任务上的应用。

5. **环境上下文缺失**：仅依赖 BABEL 的动作标签，未建模物理环境约束，无法处理 “靠墙站立” 等需要环境上下文的条件生成。

### 重要图表结论

- **TABLE II**：预训练 + 微调策略使 mRecall 从 23.0 提升至 40.9，是全文最核心的定量证据。
- **TABLE III**：预训练使生成 FID 从 0.29 降至 0.04，验证了自动描述对生成任务同样有效。
- **Fig. 15**：自动标注数据量的持续收益 vs 人工标注的快速饱和，直观展示了规模效应的因果关系。
- **TABLE V**：Posecode 聚合（N3 版本）取得最优结果，验证了管线中语义压缩模块的有效性。
- **Fig. 8**：文本到姿态检索的定性结果展示了模型对细粒度语义约束（如 “左膝微曲、右手举过头顶”）的捕捉能力。

### 补充图表

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2210_11795/figures/003_Figure_3.jpg]]
*Figure 3: Origin of the selected poses. The top bar plot shows the proportion of sequences that are eventually used in PoseScript with respect to available sequences in AMASS. A sequence is ‘used’ if it provided at least one pose to PoseScript. The bottom bar plot shows the distribution of the PoseScript poses over the AMASS sub-datasets*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2210_11795/figures/004_Figure_4.jpg]]
*Figure 4: Interface presented to the AMT annotators in order to collect discriminative descriptions of the blue pose following a two-step process*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2210_11795/figures/022_Figure.jpg]]

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2210_11795/figures/030_Figure_17.jpg]]
*Figure 17: Statistics on categorizations of distance posecodes, obtained over the poses of PoseScript-A20. The first four columns of dots from the top block show distance posecodes between the left and right corresponding body parts; other columns of dots study the distance between a left or right body part and another left or right body part (when the side of the second body part is not specified, it is the same as for the first body part). Letters ‘L’ and ‘R’ refer to left and right body parts respectively. The dot size varies with the proportion of poses that fit to the given categorization. The dot color indicates unskippable (orange), skippable (blue), and ignored (grey) posecodes, based on their...*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2210_11795/figures/031_Figure_18.jpg]]
*Figure 18: Statistics on categorizations of relative position posecodes along the X axis, obtained over the poses of PoseScript- $\mathrm { A _ { 2 0 } }$ . Letters ‘L’ and $\cdot _ { \mathrm { R } } \cdot$ refer to left and right body parts respectively. When unspecified, pairs of body parts are from the same side of the body. The dot size varies with the proportion of poses that fit to the given categorization. The dot color indicates unskippable (orange), skippable (blue), and ignored (grey) posecodes, based on their scarcity. Black dots are ignored because of their inherent ambiguity. For instance, it appears that, for less than 6% of the poses (orange dots), body extremities (hand, foot) are crisscro...

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2210_11795/figures/035_Figure_21.jpg]]
*Figure 21: Statistics on categorizations of pitch & roll posecodes, obtained over the poses of PoseScript-A20. Letters ‘L’ and ‘R’ refer to left and right body parts respectively. The word ‘backdiag’ refers to the segment between the pelvis and the shoulder, ‘hands’ (resp. ‘feet’) to the segment between the two hands (resp. feet), and ‘torso’ to the segment between the neck and the pelvis. The dot size varies with the proportion of poses that fit to the given categorization. The dot color indicates unskippable (orange), skippable (blue), and ignored (grey) posecodes, based on their scarcity. Black dots are ignored because of their inherent ambiguity. Some of these posecodes are considered only for sup...*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2210_11795/figures/006_Table.jpg]]
*Table: I SEMANTIC ANALYSIS ON 115 POSESCRIPT ANNOTATIONS*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2210_11795/figures/010_Table.jpg]]
*Table: II TEXT-TO-POSE AND POSE-TO-TEXT RETRIEVAL RESULTS ON THE TEST SPLIT OF THE POSESCRIPT DATASET. FOR HUMAN-WRITTEN CAPTIONS (POSESCRIPT-H), WE EVALUATE MODELS TRAINED ON EACH SPECIFIC CAPTION SET ALONE, AND ONE PRETRAINED ON AUTOMATIC CAPTIONS (POSESCRIPT-A) THEN FINETUNED (FT) ON HUMAN CAPTIONS. UNLESS SPECIFIED OTHERWISE, MODELS ALL HAVE THE GLOVE-BIGRU CONFIGURATION. RESULTS ARE AVERAGED OVER 3 RUNS*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2210_11795/figures/013_Table.jpg]]
*Table: III EVALUATION OF THE TEXT-CONDITIONED GENERATIVE MODEL ON POSESCRIPT-A FOR A MODEL WITHOUT OR WITH \mathcal { L } _ { r e g } (TOP) AND ON POSESCRIPT-H WITHOUT OR WITH PRETRAINING ON POSESCRIPT-A (BOTTOM). UNLESS SPECIFIED OTHERWISE, MODELS ALL HAVE THE GLOVE-BIGRU CONFIGURATION. RESULTS ARE AVERAGED OVER 3 RUNS. THE VARIABILITY OF R/G (RESP. G/R) MRECALL IS DUE TO THE RANDOM SELECTION OF A GENERATED POSE SAMPLE AT TEST (RESP. TRAINING) TIME. FOR COMPARISON, THE MRECALL WHEN TRAINING AND TESTING ON REAL POSES IS 72.8 WITH POSESCRIPT-A AND 45.3 ON POSESCRIPT-H*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2210_11795/figures/020_Table.jpg]]
*Table: SUMMARY OF THE AUTOMATIC CAPTION VERSIONS. ✓ SYMBOLS INDICATE WHEN CHARACTERISTICS APPLY TO EACH CAPTION VERSION. ALL MODELS WERE TRAINED ON A POOL OF 3 CAPTIONS PER POSE (MULTIPLICITY). MEAN RECALL RESULTS ARE AVERAGED OVER 3 RUNS OF MODELS TRAINED WITH THE BI-GRU CONFIGURATION*


## 方法谱系与知识库定位

### 核心瓶颈与设计动机

现有三维人体姿态数据集（如 AMASS 的各类子集）虽然提供了丰富的运动捕捉数据，但普遍缺乏细粒度的自然语言描述。这一缺口直接限制了需要语义理解的跨模态学习任务——文本到姿态检索、文本条件姿态生成、姿态描述生成——的性能上限。PoseScript 的核心洞察在于：**将低层 3D 姿态信息分解为少量可组合的 posecode，并结合语言规则生成多样化自然语言描述**，从而在数据规模和语义丰富度上弥补人工标注的不足。

### 方法沿革与关系定位

PoseScript 的自动描述管线建立在 **posebits**（Pons-Moll et al., 2017）的基础上，将其二元或离散的身体部位关系扩展为更细粒度的分类关系（如“膝盖轻微弯曲/相对弯曲/完全弯曲”）。与 posebits 仅输出离散标签不同，PoseScript 的管线将 posecode 通过句法模板转化为完整的自然语言句子，并引入随机化机制实现数据增强。

在跨模态检索任务上，PoseScript 采用的训练范式与 **CLIP**（Radford et al., ICML 2021）共享核心理念——通过双编码器将文本和姿态映射到联合嵌入空间，并使用对比损失进行训练。但 PoseScript 面临的关键挑战是人工标注数据极为稀缺（仅约 6,000 条），直接使用 CLIP 式的从头训练策略会导致严重的过拟合。PoseScript 的解决方案是**先在自动生成的大规模描述数据（PoseScript-A）上预训练，再在人工标注数据（PoseScript-H）上微调**，这一“自动预训练 + 人工微调”的策略构成了其区别于通用对比学习方法的独特贡献。

### 关键设计选择与消融证据

PoseScript 管线的四个模块——posecode 提取、选择、聚合、转换为句子——各自包含可调节的设计选择，其影响通过消融实验得到验证：

| 设计选择 | 基线配置 | 改进配置 | 效果 | 证据锚点 |
|---------|---------|---------|------|---------|
| 预训练数据 | 无（从头训练） | PoseScript-A 预训练 | mRecall 23.0 → 40.9 (+78%) | Table II |
| 文本编码器 | GloVe + bi-GRU | Transformer (DistilBERT) | mRecall 35.1 → 44.5 | Table II |
| 数据增强 | 无 | 镜像翻转（侧边文字替换） | mRecall 44.5 → 45.3 | Table II |
| Posecode 聚合 | 无聚合（N1） | 实体合并 + 语义合并（N3） | mRecall 提升至 39.8（最优） | Table V |

值得注意的是，**增加自动描述预训练数据量持续提升检索性能，而仅用人工数据则很快饱和**（Fig. 15）。这一发现直接验证了核心因果机制：大规模自动标注数据提供了丰富的语义多样性，使模型能够学习到可迁移的文本-姿态对齐能力。

### 适用边界与局限

PoseScript 的设计存在以下已知局限性，需要在应用中审慎评估：

1. **旋转相关姿态信息缺失**：当前 posecode 主要基于角度、距离、相对位置等关系，未涵盖前臂扭转等旋转相关姿态信息。论文指出可通过新增基于关节旋转的 posecode 扩展（Appendix B），但该扩展尚未实现和验证。

2. **否定表达缺失**：自动描述管线不生成否定句（如“手未接触地面”）。虽然人工描述中否定句比例很低（<5%），但在需要精确排除特定姿态的场景下，这一缺失可能造成语义不完整。

3. **环境/上下文信息未建模**：管线仅依赖 BABEL 的动作标签，未建模物理环境约束（如“靠着墙”）。这类信息超出当前方法范围（Appendix C）。

4. **稀有姿态泛化不足**：生成式描述模型在倒立等稀有姿态上易出现幻觉（Fig. 14, Section VI），说明 posecode 的覆盖度和语言模板的泛化能力仍有提升空间。

5. **仅覆盖单人姿态**：数据集和管线均未涉及多人交互场景（Section VIII conclusion），无法直接应用于需要描述人际空间关系的任务。

### 开放问题与未来方向

基于上述局限，以下方向值得进一步探索：

- **多人交互扩展**：如何将 posecode 体系从单人扩展至多人场景，描述相对位置、接触关系等交互语义？
- **大规模多模态模型利用**：能否借助文本-图像等大规模多模态模型（如 CLIP 的图像分支）填补活动语义、环境上下文等数据缺口？
- **稀有姿态处理**：如何通过数据增强、课程学习或生成式建模改进对自接触、倒立等稀有姿态的覆盖和生成质量？
- **下游任务迁移**：基于文本的身体语义先验在动作识别、运动预测、人机交互等下游任务中的应用前景如何？PoseScript 的文本条件姿态生成模型已初步展示了在 SMPL 拟合中作为语义先验的潜力（Fig. 12），但系统性的下游评估仍有待开展。

## 原文 PDF

![[paperPDFs/TPAMI_2024/PoseScript_Linking_3D_Human_Poses_and_Natural_Language.pdf]]
