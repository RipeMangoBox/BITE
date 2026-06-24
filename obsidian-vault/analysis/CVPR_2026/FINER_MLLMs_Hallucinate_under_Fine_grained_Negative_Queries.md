---
title: "FINER: MLLMs Hallucinate under Fine-grained Negative Queries"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FINER_MLLMs_Hallucinate_under_Fine_grained_Negative_Queries.pdf
project_link: "https://explainableml.github.io/finer-project/"
code_link: null
aliases:
- FT
- FINER
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过构造细粒度的否定查询数据（FINER基准），并使用直接偏好优化（DPO）训练模型区分肯定和否定查询中的正确与错误元素，可以有效减轻细粒度幻觉。
primary_logic: 细粒度查询中的幻觉源于模型无法同时处理多个语义元素（对象、属性、关系），并错误地将部分匹配视为完全匹配；利用场景图生成结构化否定示例，并在训练中同时使用肯定和否定查询对，可以增强模型对细粒度不正确声明的拒绝能力。
claims:
- FINER-Tuning在FINER-CompreCap的Multi-rel子集上为InternVL3.5-14B带来24.2%的绝对提升（从47.0%到71.2%）。
- 模型性能随查询粒度增加而急剧下降，例如InternVL3.5-14B在FINER-COMPRECAP上从~80%（级别1）降至~20%（级别5-7）。
- FINER-Tuning在多个其他幻觉基准（如DASH、HaloQuest）上也带来一致的改善，同时不损害通用能力。
- FINER-CompreCap (Multi-obj) 上 Acc_paired = 48.4 (LLaVA-1.6 +FINER-Tuning)
---

# FINER: MLLMs Hallucinate under Fine-grained Negative Queries

> [!tip] 核心洞察
> 细粒度查询中的幻觉源于模型无法同时处理多个语义元素（对象、属性、关系），并错误地将部分匹配视为完全匹配；利用场景图生成结构化否定示例，并在训练中同时使用肯定和否定查询对，可以增强模型对细粒度不正确声明的拒绝能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | FINER：多模态大语言模型在细粒度负面查询下的幻觉 |
| 英文题名 | FINER: MLLMs Hallucinate under Fine-grained Negative Queries |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.17662) · [Project](https://explainableml.github.io/finer-project/) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | FINER-Tuning |
| Dataset | FINER-CompreCap, FINER-DOCCI, DASH, MMHal-Bench |

> [!tip] 效果简介
> - FINER-CompreCap (Multi-obj) 上，Acc_paired 48.4 (LLaVA-1.6 +FINER-Tuning) vs 25.3 (LLaVA-1.6) (+23.1%)。
> - FINER-CompreCap (Multi-rel) 上，Acc_paired 71.2 (InternVL-3.5-14B +FINER-Tuning) vs 47.0 (InternVL-3.5-14B) (+24.2%)。
> - FINER-DOCCI (Multi-attr) 上，Acc_paired 52.2 (Qwen2.5-VL +FINER-Tuning) vs 47.5 (Qwen2.5-VL) (+4.7%)。

## 概述

多模态大语言模型（MLLM）在视觉理解任务中表现出色，但普遍存在“幻觉”问题——模型会生成与图像内容不符的描述。现有的幻觉基准主要关注**粗粒度查询**（如判断单一对象是否存在），却忽略了**细粒度查询**中涉及的多个对象、属性及关系的细微错误。这导致模型在面对“图中没有红色汽车和蓝色自行车”这类涉及多语义元素的否定声明时，容易产生**假阳性幻觉**——错误地将不正确的声明判断为正确。

针对这一瓶颈，本文提出了**FINER**（FIne-grained NEgative queRies）框架，包含两个细粒度负面查询基准（FINER-CompreCap 和 FINER-DOCCI）以及一种训练方法 **FINER-Tuning**。其核心思路是：利用场景图结构生成包含多对象、多属性、多关系的结构化否定示例，并通过直接偏好优化（DPO）训练模型同时处理肯定查询和否定查询，从而增强模型对细粒度错误声明的拒绝能力。

实验结果表明，FINER-Tuning 在多个前沿 MLLM 上均带来显著提升。例如，在 FINER-CompreCap 的 Multi-rel 子集上，InternVL3.5-14B 的成对准确率从 47.0% 跃升至 71.2%（+24.2%）；在 Multi-obj 子集上，LLaVA-1.6 也获得 23.1% 的绝对提升。此外，该方法在 DASH、MMHal-Bench 等其他幻觉基准上也表现出一致的改善，同时不损害模型的通用能力。这些结果验证了细粒度负面查询训练在缓解 MLLM 幻觉方面的有效性。

## 背景与动机

### 多模态大语言模型的幻觉困境

多模态大语言模型（MLLM）在视觉理解任务中取得了显著进展，但幻觉问题——即模型生成与图像内容不一致的描述——始终是其可靠部署的核心障碍。现有研究主要从两个维度衡量幻觉：**判别式基准**要求模型判断给定陈述的真伪，**生成式基准**则评估模型自由文本输出中的事实错误。

然而，当前幻觉基准存在一个关键盲区：它们主要关注**粗粒度查询**，例如“图像中是否存在某单一对象”。这类查询仅涉及单个语义元素，无法揭示模型在面对**细粒度负面查询**时的脆弱性——即要求模型同时处理多个对象、属性和关系，并识别其中细微错误的场景。

### 细粒度查询下的性能崩溃

论文通过动机实验揭示了这一问题的严重性。在FINER-COMPRECAP基准上，InternVL3.5-14B的性能随查询粒度的增加而急剧下降：在仅涉及单一语义元素的级别1，准确率约80%；但当查询涉及5-7个语义元素（级别5-7）时，准确率骤降至约20%（Figure 1）。这种性能崩溃表明，现有MLLM在面对细粒度不正确陈述时，倾向于将**部分匹配误认为完全匹配**，从而产生高比率的假阳性幻觉。

具体而言，细粒度负面查询要求模型同时验证多个语义约束——例如“图像中是否存在一只**白色**的猫**坐在**沙发上”？模型可能正确识别了猫和沙发，但忽略了颜色或空间关系的错误，从而给出错误的肯定回答。这种“只见树木不见森林”的认知缺陷，在粗粒度基准中完全无法暴露。

### 现有方法的局限性

当前减少幻觉的方法主要分为两类：**训练时干预**（如RLHF-V、RLAIF-V、OPA-DPO）和**推理时干预**。这些方法虽然在粗粒度基准上取得了进展，但存在两个共同缺陷：

1. **训练数据粒度不足**：现有方法使用的偏好数据或对齐数据通常仅涉及单一对象的存在与否，缺乏对多对象、多属性、多关系组合的细粒度覆盖。
2. **训练策略片面**：多数方法仅针对负面查询进行优化，忽略了模型同样需要在正面查询上保持正确性，导致“对齐税”——即减少幻觉的同时损害通用能力。

### 核心动机与解决思路

基于上述分析，论文的核心动机是：**构建细粒度的负面查询基准，以系统评估MLLM的幻觉脆弱性；并提出相应的训练方法，增强模型对细粒度不正确声明的拒绝能力。**

为此，论文引入**FINER（FIne-grained NEgative queRies）**概念，并同时提出两个互补的贡献：

- **FINER基准族**：包括FINER-CompreCap和FINER-DOCCI，通过场景图（Scene Graph）编码图像中的对象、属性和关系，生成结构化的细粒度负面多选题，覆盖Multi-obj、Multi-attr、Multi-rel和Wh四种查询类型。
- **FINER-Tuning训练方法**：利用直接偏好优化（DPO），在同时包含正面和负面查询的偏好数据上训练模型，使其既能正确接受真实陈述，又能准确拒绝细粒度的错误陈述。

这一双重设计旨在填补现有基准和训练方法在细粒度幻觉检测上的空白，推动MLLM向更可靠的多模态理解迈进。

## 核心创新

### 问题重定义：从粗粒度存在性到细粒度组合正确性

现有MLLM幻觉基准（如POPE）主要关注**粗粒度查询**——询问图像中是否存在某个单一对象。这种评测范式忽略了一类更隐蔽的幻觉：当查询涉及**多个对象、属性、关系的组合**时，模型容易将部分匹配误判为完全匹配，从而对包含细微错误的声明给出肯定回答（假阳性幻觉）。

FINER将这一问题定义为**细粒度负面查询**下的鲁棒性挑战。其核心发现是：模型性能随查询粒度增加而急剧下降——InternVL3.5-14B在FINER-COMPRECAP上从粒度级别1的约80%骤降至级别5-7的约20%（Figure 1），揭示出多模态大语言模型在同时处理多个语义元素时的根本性脆弱性。

### 方法创新：FINER-Tuning的双向偏好优化

针对上述瓶颈，FINER-Tuning在三个关键维度上区别于现有方法：

**1. 训练数据构造（changed slot: 训练数据）**

现有幻觉减少方法（如RLHF-V、OPA-DPO）通常依赖通用指令数据或粗粒度负面样本进行对齐训练。FINER-Tuning从Pixmo-caption长标题出发，构建了结构化的细粒度偏好数据集：

- **正面短语提取**：使用PHI-4-14B从长标题中提取四类语义短语——对象（$\Psi_{\mathrm{OBJ}}^+$）、属性（$\Psi_{\mathrm{ATTR}}^+$）、关系（$\Psi_{\mathrm{REL}}^+$）以及What类型（$\Psi_{\mathrm{WH}}^+$）
- **负面短语生成**：通过同一LLM修改正面短语，生成语义合理但错误的负面版本
- **正负查询对构建**：基于模板或LLM生成正面查询（期望回答“是”）和负面查询（期望回答“否”），形成偏好元组 $\{(x, q^+, a_+^+, a_+^-), (x, q^-, a_-^+, a_-^-)\}$

**2. 训练目标（changed slot: 训练目标）**

不同于仅最大化正例概率的标准SFT，FINER-Tuning采用DPO损失，显式优化模型对正确回答相对于错误回答的偏好：

$$\mathcal{L}_{\mathrm{DPO}}(\theta) = -\mathbb{E}_{(x,q,a^+,a^-)\sim\mathcal{D}} \left[ \log \sigma \left( \beta (\Delta_\theta - \Delta_{\mathrm{ref}}) \right) \right]$$

其中 $\beta=0.1$ 为逆温度参数。关键设计在于**同时覆盖正面和负面查询对**：消融实验（Table 4）表明，仅使用负面查询的DPO虽优于基线，但仍显著落后于同时使用正负查询的FINER-Tuning；而使用SFT替代DPO则导致Multi-obj性能相对基线下降36.7%，证明DPO框架对细粒度拒绝能力的训练至关重要。

**3. 查询粒度（changed slot: 查询粒度）**

FINER将评测从单一对象存在性扩展到多对象（Multi-obj）、多属性（Multi-attr）、多关系（Multi-rel）及What问题的组合查询。这种细粒度设计直接针对模型“部分匹配即完全匹配”的认知偏差，迫使模型学习区分正确与错误的语义组合。

### 与现有方法的关键差异

| 维度 | 现有方法（RLHF-V, OPA-DPO等） | FINER-Tuning |
|------|-------------------------------|--------------|
| 负面样本粒度 | 粗粒度（单一对象替换） | 细粒度（多对象/属性/关系组合修改） |
| 训练数据源 | 通用指令数据 | 从长标题提取的结构化语义短语 |
| 训练策略 | 仅负面查询或仅正面查询的偏好优化 | 正负查询对联合DPO训练 |
| 评测指标 | 单一维度准确率 | 成对准确率 $\mathrm{Acc}_{\mathrm{paired}}$（要求同时正确回答正负查询） |

### 证据强度

- **决定性证据**：FINER-Tuning在InternVL3.5-14B的FINER-CompreCap Multi-rel子集上带来24.2%的绝对提升（47.0% → 71.2%，Table 1），且在多个外部幻觉基准（DASH +6.2%、HaloQuest等）上一致改善（Table 2），同时不损害通用能力（Table 3，InternVL3.5-14B平均提升1.4%）
- **需注意的局限**：高细粒度案例和What问题对所有模型（包括InternVL-3.5-38B和Gemini-2.5-Flash）仍具挑战性；Multi-rel子集目前最多仅包含三个关系，扩展到更高阶关系是待解决问题

## 整体框架

FINER 的整体框架由两个紧密耦合的子系统构成：**细粒度负面查询基准（FINER Benchmarks）** 和 **基于直接偏好优化的训练方法（FINER-Tuning）**。二者的共同目标是揭示并缓解多模态大语言模型（MLLM）在面对包含多个语义元素的细粒度负面查询时产生的假阳性幻觉。

### 核心瓶颈与因果机制

现有 MLLM 幻觉基准主要关注粗粒度查询（如单一对象存在性），忽略了涉及多个对象、属性、关系的细粒度查询中的细微错误。这导致模型在面对细粒度否定查询时，倾向于将部分匹配误判为完全匹配，从而产生假阳性幻觉。FINER 的核心洞察在于：**通过场景图（Scene Graph）结构化地生成负面示例，并在训练中同时使用肯定和否定查询对进行直接偏好优化（DPO），可以迫使模型学习区分正确与错误语义元素的精确边界。**

### 系统架构与模块关系

整个框架的数据流与模块交互如图 2 和图 3 所示，分为基准构建和训练数据生成两条主线：

#### 基准构建流程（Figure 2）

![[assets/figures/papers/paper_list_l2102_https_arxiv_org_abs_2603_17662/figures/002_Figure_2.jpg]]
*Figure 2: Data construction pipeline for FINER benchmarks. For FINER-DOCCI, we extract the positive scene graph (SG) from DOCCI [34] captions, while for FINER-COMPRECAP, the SG is provided by CompreCap [31]. From the positive SG, we generate the negative SG using Qwen3-14B [51] as negatives generator for FINER-COMPRECAP and Gemini-2.0-Flash [41] for FINER-DOCCI. Finally, a rule-based query construction pipeline builds multiple choice questions. In practice, choices are shuffled in both benchmarks*

基准构建以场景图为核心数据结构，将图像内容编码为对象（OBJ）、属性（ATTR）和关系（REL）三元组：

1. **正向场景图提取**：对于 FINER-CompreCap，直接利用 CompreCap 提供的场景图标注；对于 FINER-DOCCI，则从 DOCCI 人工标注的长标题中，通过 Gemini-2.0-Flash 进行两阶段提取（Figure 8），先抽取对象和属性，再抽取并验证关系。
2. **负向场景图生成**：使用大语言模型（Qwen3-14B 用于 FINER-CompreCap，Gemini-2.0-Flash 用于 FINER-DOCCI）对正向场景图中的每个语义元素进行修改，生成语义上合理但错误的负面元素。
3. **多选题构建**：基于规则的方法将正负场景图转化为成对的多选题（MCQ），每个样本包含一个正向查询（正确答案为“是”）和一个负向查询（正确答案为“否”）。

![[assets/figures/papers/paper_list_l2102_https_arxiv_org_abs_2603_17662/figures/013_Figure_8.jpg]]
*Figure 8: Example positive scene graph (SG) extracted by Gemini-2.0-Flash [41]. Given a long human-annotated caption from DOCCI [34], we apply a two-stage extraction pipeline to obtain the positive SG*

#### 训练数据生成流程（Figure 3）

![[assets/figures/papers/paper_list_l2102_https_arxiv_org_abs_2603_17662/figures/003_Figure_3.jpg]]
*Figure 3: Training data generation pipeline for FINER-Tuning. (1) We adopt long captions from Pixmo [11] and extract diverse phrases with PHI-4-14B [1]. (2) We then prompt the same LLM to modify and generate negative phrases. (3) We construct both positive and negative query-answer tuples via template-based composition or LLM generation*

训练数据以 Pixmo 长标题为起点，通过三阶段流水线生成偏好元组：

1. **正向短语提取**：使用 PHI-4-14B 从 Pixmo 长标题中提取多样化的语义短语，覆盖四种类型：$\Psi^+ \in \{ \Psi_{\mathrm{OBJ}}^+, \Psi_{\mathrm{ATTR}}^+, \Psi_{\mathrm{REL}}^+, \Psi_{\mathrm{WH}}^+ \}$。
2. **负向短语生成**：由同一个 LLM 对正向短语进行修改，生成对应的负面短语。
3. **查询-答案对构建**：通过模板组合或 LLM 生成方式，构建正负查询及其对应的接受/拒绝答案，形成偏好数据 $\{ (x, q^+, a_+^+, a_+^-), (x, q^-, a_-^+, a_-^-) \}$。

### 训练目标与评估指标

FINER-Tuning 使用 DPO 损失函数进行优化：

$$\mathcal{L}_{\mathrm{DPO}}(\theta) = -\mathbb{E}_{(x,q,a^+,a^-)\sim\mathcal{D}} \left[ \log \sigma \left( \beta (\Delta_\theta - \Delta_{\mathrm{ref}}) \right) \right]$$

其中 $\beta=0.1$ 为逆温度参数，$\Delta_\theta$ 和 $\Delta_{\mathrm{ref}}$ 分别表示当前策略和参考策略对正负回答的隐式奖励差。训练同时覆盖正向和负向查询，使模型既能正确接受真实陈述，又能拒绝虚假陈述。

评估采用**成对准确率**作为核心指标，要求模型在同一图像的正向和负向多选题上同时回答正确：

$$\mathrm{Acc}_{\mathrm{paired}} = \frac{1}{N} \sum_{i=1}^{N} \Gamma(M(x_i, q_i^+)) \Gamma(M(x_i, q_i^-))$$

其中 $\Gamma(\cdot)$ 为指示函数，$M(x_i, q_i^+)$ 和 $M(x_i, q_i^-)$ 分别表示模型在正向和负向查询上的回答正确性。该指标有效避免了模型通过猜测或位置偏差获得虚高分数。

### 关键证据强度

- **决定性证据**：FINER-Tuning 在 FINER-CompreCap 的 Multi-rel 子集上为 InternVL3.5-14B 带来 24.2% 的绝对提升（从 47.0% 到 71.2%，Table 1），在 Multi-obj 子集上为 LLaVA-1.6 带来 23.1% 的提升（从 25.3% 到 48.4%，Table 1）。
- **支持性证据**：模型性能随查询粒度增加而急剧下降，例如 InternVL3.5-14B 在 FINER-COMPRECAP 上从级别 1 的约 80% 降至级别 5-7 的约 20%（Figure 1），验证了细粒度查询的区分力。
- **泛化证据**：FINER-Tuning 在 DASH、HaloQuest 等多个外部幻觉基准上也带来一致改善，同时不损害通用能力（Table 2, Table 3）。

### 已知局限

- 高细粒度案例和 What 问题对所有模型仍构成挑战，即使是 InternVL-3.5-38B 和 Gemini-2.5-Flash 也表现有限。
- FINER 基准并非完全由人工验证，存在一定的主观性和标注误差。
- Multi-rel 子集最多只包含三个关系，扩展到更高阶关系是未来方向。

## 核心模块与公式推导

### 3.1 细粒度查询下的幻觉度量：成对准确率

FINER基准的核心评估指标是**成对准确率**（Paired Accuracy），定义为模型在一对正/负多选题上同时答对的样本比例：

$$
\mathrm{Acc}_{\mathrm{paired}} = \frac{1}{N} \sum_{i=1}^{N} \Gamma(M(x_i, q_i^+)) \, \Gamma(M(x_i, q_i^-))
$$

其中：
- $x_i$ 为输入图像，$q_i^+$ 和 $q_i^-$ 分别为正面查询和负面查询；
- $M(\cdot)$ 为多模态大语言模型；
- $\Gamma(\cdot)$ 为指示函数，当模型输出正确选项时取1，否则取0。

**设计动机**：传统准确率仅评估单一查询类型，无法区分模型是“真能判别”还是“偏向某一选项”。成对准确率强制要求模型在正负两个方向上同时正确，从而消除位置偏差和猜测效应，更严格地衡量模型对细粒度语义元素的真伪辨别能力。

### 3.2 FINER-Tuning 训练数据生成流水线

FINER-Tuning 的训练数据构建流程（Figure 3）包含三个核心模块：

**模块一：正面短语提取**  
从 Pixmo-caption 的长标题中，使用 PHI-4-14B 提取四类细粒度正面短语 $\Psi^+$：
- $\Psi_{\mathrm{OBJ}}^+$：对象短语（如 “a red car”）
- $\Psi_{\mathrm{ATTR}}^+$：属性短语（如 “the wooden table is round”）
- $\Psi_{\mathrm{REL}}^+$：关系短语（如 “the cat sits on the sofa”）
- $\Psi_{\mathrm{WH}}^+$：What 类型短语（如 “the man is wearing a blue hat”）

**模块二：负面短语生成**  
对每类正面短语，提示同一 LLM 进行语义合理的修改，生成对应的负面短语 $\Psi^-$。例如，将 “a red car” 修改为 “a blue car”（对象替换），或将 “the cat sits on the sofa” 修改为 “the cat sits under the sofa”（关系替换）。

**模块三：查询-答案对构建**  
基于正/负短语对，通过模板组合或 LLM 生成构建训练元组：
$$
\{ (x, q^+, a_+^+, a_+^-), \; (x, q^-, a_-^+, a_-^-) \}
$$
其中：
- $q^+$ 为正面查询，$a_+^+$ 为正确接受答案，$a_+^-$ 为错误拒绝答案；
- $q^-$ 为负面查询，$a_-^+$ 为正确拒绝答案，$a_-^-$ 为错误接受答案。

**关键设计**：训练数据同时包含正面和负面查询对，使模型学习在两种场景下均能正确响应，而非仅学会拒绝。

### 3.3 直接偏好优化目标

FINER-Tuning 采用 DPO 损失函数进行训练：

$$
\mathcal{L}_{\mathrm{DPO}}(\theta) = -\mathbb{E}_{(x,q,a^+,a^-)\sim\mathcal{D}} \left[ \log \sigma \left( \beta (\Delta_\theta - \Delta_{\mathrm{ref}}) \right) \right]
$$

其中：
- $\theta$ 为当前策略模型参数，$\mathrm{ref}$ 为参考模型（冻结的基础模型）；
- $\Delta_\theta = \log \frac{\pi_\theta(a^+|x,q)}{\pi_\theta(a^-|x,q)}$，表示当前模型对正例相对于负例的对数概率比；
- $\Delta_{\mathrm{ref}}$ 为参考模型的对应比值；
- $\beta$ 为逆温度参数，控制偏好强度（实验中设为 $\beta=0.1$）；
- $\sigma(\cdot)$ 为 logistic 函数。

**训练机制**：DPO 直接最大化正确回答 $a^+$ 相对于错误回答 $a^-$ 的偏好概率，无需显式奖励模型。通过同时输入正面查询和负面查询的偏好对，模型被强制学习区分细粒度语义元素的真伪，从而在推理时能正确拒绝包含细微错误的声明。

## 实验与分析

### 细粒度负面查询下的性能瓶颈

Figure 1 清晰地揭示了当前多模态大语言模型在细粒度负面查询下的系统性脆弱性。以 InternVL3.5-14B 为基线，随着查询粒度的增加（从级别 1 到级别 7），模型在 FINER-COMPRECAP 上的成对准确率从约 80% 急剧下降至约 20%。这种性能衰减并非渐进式的，而是在涉及多对象、多属性、多关系的语义组合时出现断崖式下跌，表明模型的核心缺陷在于无法同时处理多个语义元素，倾向于将部分匹配误判为完全匹配。

![[assets/figures/papers/paper_list_l2102_https_arxiv_org_abs_2603_17662/figures/001_Figure_1.jpg]]
*Figure 1: We compare the performance InternVL3.5-14B [46] Questions (Baseline) with the one fine-tuned by FINER-Tuning under negative queries of seven different granularity levels*

这一发现直接挑战了现有幻觉基准的评估范式。传统的粗粒度查询（如单一对象存在性判断）掩盖了模型在细粒度场景下的真实能力边界，而 FINER 基准通过结构化场景图生成的多元素否定查询，有效暴露了这一隐藏瓶颈。

### FINER-Tuning 的主实验结果

Table 1 汇总了 FINER-Tuning 在四个基线模型上的核心提升。在所有细粒度子集上，FINER-Tuning 均带来显著且一致的增益：

![[assets/figures/papers/paper_list_l2102_https_arxiv_org_abs_2603_17662/figures/004_Table_1.jpg]]
*Table 1: Paired accuracy*

- **LLaVA-1.6** 在 FINER-CompreCap 的 Multi-obj 子集上从 25.3% 提升至 48.4%（+23.1%），在 Multi-rel 子集上从 24.5% 提升至 49.8%（+25.3%）。
- **InternVL-3.5-14B** 在 Multi-rel 子集上获得最大绝对提升，从 47.0% 跃升至 71.2%（+24.2%）。
- **Qwen2.5-VL** 在 FINER-DOCCI 的 Multi-attr 子集上从 47.5% 提升至 52.2%（+4.7%），增益相对有限，表明该模型在属性级细粒度判断上的改进空间更大。
- **InternVL-3.5-8B** 在 Multi-obj 子集上从 39.3% 提升至 60.6%（+21.3%）。

值得注意的是，FINER-Tuning 对 Multi-rel 子集的改善最为突出。这一现象与关系推理需要同时编码多个对象及其空间/语义关联的认知负荷一致，验证了 DPO 训练在强化多元素协同判断方面的有效性。

### 跨基准泛化能力

FINER-Tuning 的增益不仅局限于 FINER 系列基准。Table 2 显示，该方法在多个独立幻觉基准上同样带来一致的性能提升：

![[assets/figures/papers/paper_list_l2102_https_arxiv_org_abs_2603_17662/figures/006_Table_2.jpg]]
*Table 2: Results on hallucination benchmarks including discriminative (DASH [3], POPE [22], RePOPE [33], HallusionBench [16], AMBER [44], CRPE R [45]) and generative ones (MMHal-Bench [40], HaloQuest [47]). Sc.:Score (max. 6); HR.: Hallucination Rate*

- **DASH**：InternVL-3.5-8B 从 68.3% 提升至 74.5%（+6.2%），InternVL-3.5-14B 从 68.4% 提升至 73.9%（+5.5%）。
- **MMHal-Bench**：InternVL-3.5-14B 的幻觉率从 11.0% 降至 10.0%。
- **POPE、RePOPE、AMBER、HallusionBench** 等判别式基准上，FINER-Tuning 同样展现出正向迁移效果。

更重要的是，Table 3 表明 FINER-Tuning 不会引入“对齐税”。在六个通用多模态基准（MMStar、TextVQA、ChartQA、MMVP、NaturalBench、V* Bench）上，InternVL-3.5-14B 经 FINER-Tuning 后平均提升 1.4%，证明该方法在抑制幻觉的同时保持了模型的通用能力。

![[assets/figures/papers/paper_list_l2102_https_arxiv_org_abs_2603_17662/figures/008_Table_3.jpg]]
*Table 3: Results on six general purpose MLLM benchmarks. M.S.: MMStar [7]; Text: TextVQA [39]; Chart: ChartQA [32]; M.P.: MMVP [42]; N.B.: NaturalBench [21]; V∗: V∗ Bench [48]*

### 实体数量对性能的影响

Figure 4 进一步解构了性能与实体数量的关系。在 FINER-COMPRECAP 上，当对象数量增至 6 个时，InternVL3.5-14B 经 FINER-Tuning 后提升 8.3%；在 3 属性设置下提升 19.1%；在 3 关系设置下提升 28.1%。这一趋势表明，FINER-Tuning 对高复杂度场景（尤其是多关系）的改善最为显著，但即使在最高实体数量下，绝对准确率仍远未饱和，说明细粒度幻觉问题尚未完全解决。

![[assets/figures/papers/paper_list_l2102_https_arxiv_org_abs_2603_17662/figures/005_Figure_4.jpg]]

### 消融实验的关键发现

Table 4 的消融研究揭示了 FINER-Tuning 设计的三个关键要素：

![[assets/figures/papers/paper_list_l2102_https_arxiv_org_abs_2603_17662/figures/007_Table_4.jpg]]
*Table 4: Ablation study on different training strategies. SFT methods only use*

1. **正负查询对的重要性**：仅使用负面查询进行 DPO 训练优于基线模型，但仍显著落后于同时使用正面和负面查询的 FINER-Tuning。这表明模型需要同时学习“什么是正确的”和“什么是错误的”，才能在细粒度判断中建立稳健的决策边界。

2. **DPO 优于 SFT**：使用 SFT 训练正负查询对会导致 Multi-obj 性能相对基线下降 36.7%。这一反直觉的结果说明，简单的监督微调无法有效传递细粒度否定信号，反而可能破坏模型已有的判别能力。DPO 通过偏好对比机制，更精准地引导模型学习拒绝错误声明。

3. **全子集训练的均衡性**：Table 5 显示，在 Multi-obj、Multi-attr、Multi-rel 和 Wh 四个子集上联合训练可获得最均衡的结果。仅在单一子集上训练会导致其他子集性能下降，说明不同粒度的否定判断能力存在一定的正交性，需要多样化训练数据覆盖。

![[assets/figures/papers/paper_list_l2102_https_arxiv_org_abs_2603_17662/figures/009_Table_5.jpg]]
*Table 5: Training-on-subset ablation for FINER-Tuning with InternVL-3.5-8B [46]. Obj/Attr/Rel denote Multi-obj/Multiattr/Multi-rel for both training and evaluation*

### 失败模式与局限性

尽管 FINER-Tuning 取得了显著进展，但实验同时暴露了多个持续存在的失败模式：

- **Wh 问题的顽固困难**：即使是 InternVL-3.5-38B 和 Gemini-2.5-Flash 等大型模型，在 Wh 类型的细粒度否定查询上仍表现有限。这类问题要求模型识别“什么”被错误描述，涉及更复杂的语义推理，当前方法尚未有效解决。
- **高细粒度场景的饱和瓶颈**：随着实体数量增加，所有模型的绝对准确率仍处于较低水平，表明当前架构在同时处理多个语义元素时存在根本性限制。
- **基准的标注噪声**：FINER 基准并非完全人工验证，场景图提取和负面生成过程存在一定主观性，可能引入标注偏差。人类研究规模有限（每子集 20 道 MCQ），基准质量的完全验证需要更大规模的人工标注工作。
- **关系数量的扩展受限**：Multi-rel 子集最多仅包含三个关系，现实场景中的复杂关系网络远超此范围，方法的可扩展性有待验证。

### 与其他幻觉减少方法的对比

Table 16 将 FINER-Tuning 与 RLAIF-V、OPA-DPO、RLHF-V 等现有幻觉减少方法在 LLaVA-1.5-7B 上进行了对比。FINER-Tuning 在多个指标上取得最优或次优结果，尤其在细粒度场景下展现出独特优势。这一对比表明，针对细粒度否定查询的专门训练是现有方法的有效补充，而非简单替代。

![[assets/figures/papers/paper_list_l2102_https_arxiv_org_abs_2603_17662/figures/027_Table_16.jpg]]
*Table 16: Extended comparison with other hallucination reduction methods on LLaVA-1.5-7B [26]. HR.: Hallucination rate. The best results are bold while the second best results are underlined*

### 补充图表

![[assets/figures/papers/paper_list_l2102_https_arxiv_org_abs_2603_17662/figures/022_Table_12.jpg]]
*Table 12: Filtering to only keep natural images ablation for FINER-Tuning with InternVL-3.5-8B [46]. Obj/Attr/Rel denote Multi-obj/Multi-attr/Multi-rel for both training and evaluation. The best results are bold*

## 方法谱系与知识库定位

### 问题定位：从粗粒度到细粒度幻觉评估

现有的多模态大语言模型（MLLM）幻觉基准主要关注**粗粒度查询**——例如询问图像中是否存在某个单一对象（如“图中是否有猫？”）。这类查询无法揭示模型在**细粒度语义组合**层面的脆弱性：当负面声明涉及多个对象、属性或关系的交叉错误时，模型往往无法准确拒绝，表现为高假阳性率。

FINER 的核心洞察在于：MLLM 在细粒度负面查询下的幻觉源于模型**无法同时处理多个语义元素**（对象、属性、关系），并错误地将部分匹配视为完全匹配。这一瓶颈被 Figure 1 的动机实验直接证实——InternVL3.5-14B 在 FINER-COMPRECAP 上的成对准确率从细粒度级别 1 的约 80% 急剧下降至级别 5–7 的约 20%。

### 方法谱系：FINER-Tuning 与相关工作的关系

**与幻觉减少方法的对比。** 已有的 MLLM 幻觉缓解方法包括 **RLAIF-V**、**OPA-DPO**、**RLHF-V** 等，这些方法通常采用偏好优化或强化学习来减少模型生成错误内容的倾向。然而，它们的训练数据构造和评估范式仍以粗粒度查询为主——即关注“对象是否存在”这类二元判断。FINER-Tuning 的关键差异在于：

| 维度 | 已有方法（RLAIF-V、OPA-DPO 等） | FINER-Tuning |
|------|-------------------------------|--------------|
| 查询粒度 | 粗粒度（单一对象存在/不存在） | 细粒度（多对象/多属性/多关系组合） |
| 训练数据构造 | 基于现有幻觉基准或简单负样本 | 从长标题提取正负短语对，覆盖 OBJ/ATTR/REL/WH 四类 |
| 训练目标 | DPO 或 RLHF，通常仅用负面查询 | DPO 同时使用正面和负面查询对 |
| 评估指标 | 标准准确率或幻觉率 | 成对准确率（Acc_paired），要求正负查询同时正确 |

消融实验（Table 4）提供了关键证据：仅使用负面查询的 DPO 优于基线但仍不如 FINER-Tuning（同时使用正负查询对），而使用 SFT 训练会导致 Multi-obj 性能相对基线下降 36.7%。这表明**正负查询对的联合训练**是方法有效的核心机制。

**与基准模型的关系。** FINER-Tuning 在四个前沿 MLLM 上验证：LLaVA-1.6、Qwen2.5-VL、InternVL-3.5（8B 和 14B）。这些模型代表当前开源 MLLM 的主流架构和训练范式。此外，封闭源模型 Gemini-2.5-Flash 被用作对比参照点，但未参与 FINER-Tuning 训练。

### 方法适用边界

**有效范围。** FINER-Tuning 在以下条件下表现出稳定增益：
- **细粒度负面拒绝能力**：在 FINER-CompreCap 的 Multi-obj（+23.1%）、Multi-rel（+24.2%）子集上提升显著。
- **跨基准泛化**：在 DASH（+6.2%）、MMHal-Bench（幻觉率降低 1.0%）、HaloQuest 等其他幻觉基准上也有一致改善（Table 2）。
- **通用能力保持**：在六个通用 MLLM 基准上未观察到对齐税，InternVL3.5-14B 反而有 1.4% 的平均提升（Table 3）。

**失效边界。** 以下场景中方法效果有限或尚未验证：
- **高细粒度和 What 问题**：即使是大型模型（InternVL-3.5-38B、Gemini-2.5-Flash）在 What 类型查询上也表现困难，FINER-Tuning 的增益在此类问题上相对有限。
- **高阶关系**：Multi-rel 子集最多只包含三个关系，方法对更高阶关系查询的扩展性尚未验证。
- **更大模型与不同架构**：当前实验限于 14B 及以下规模的模型，FINER-Tuning 在更大模型或不同架构（如纯解码器架构）上的泛化能力仍是开放问题。

### 局限与开放问题

**已知局限。**
1. **基准噪声**：FINER 基准并非完全由人工验证，场景图提取和负面生成依赖 LLM（Qwen3-14B、Gemini-2.0-Flash），存在一定主观性和标注误差。完全人工标注的无噪基准是未来方向。
2. **人类研究规模**：人类性能评估仅覆盖每个子集 20 道 MCQ，不能完全代表基准质量。
3. **关系数量限制**：Multi-rel 子集的关系数量上限为 3，需要扩展到更高阶关系以匹配真实场景的复杂性。

**开放问题。**
1. **What 问题的本质困难**：为何 What 类型查询对所有模型都构成挑战？其困难是否源于开放生成与多选题之间的评估范式差异，还是模型在细粒度信息定位上的根本缺陷？
2. **可扩展性**：如何将方法扩展到更多关系、更高细粒度的查询？场景图复杂度增长时，负面生成的语义合理性如何保证？
3. **训练数据规模与多样性**：当前训练数据源自 Pixmo-caption，其在非自然图像（如文档、图表）上的覆盖有限（Table 12 的消融显示过滤非自然图像对结果影响不大，但该结论的泛化性需要进一步验证）。
4. **与推理时方法的结合**：FINER-Tuning 是一种训练时干预，它能否与推理时的幻觉检测策略（如自一致性、验证链）协同工作，形成更完整的幻觉防御体系？

### 知识库定位

FINER 在 MLLM 幻觉研究领域占据**细粒度负面查询评估与缓解**这一生态位。其贡献包括：
- **评估维度创新**：首次系统化定义和量化细粒度负面查询下的幻觉，补充了现有基准（POPE、AMBER、HallusionBench 等）在语义组合粒度上的空白。
- **训练范式验证**：证明正负查询对联合 DPO 训练是缓解细粒度幻觉的有效策略，为后续偏好优化方法提供了数据构造范式的参考。
- **开放资源**：FINER 基准和 FINER-Tuning 训练框架已开源，可作为后续研究的标准测试平台。

## 原文 PDF

![[paperPDFs/CVPR_2026/FINER_MLLMs_Hallucinate_under_Fine_grained_Negative_Queries.pdf]]
