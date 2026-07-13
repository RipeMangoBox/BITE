---
title: "Inter-X: Towards Versatile Human-Human Interaction Analysis"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/Inter_X_Towards_Versatile_Human_Human_Interaction_Analysis.pdf
project_link: https://liangxuy.github.io/inter-x/
code_link: null
aliases:
- IXDB
- Inter-X
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 构建一个大规模、高精度的多模态人-人交互数据集Inter-X，通过光学与惯性组合运动捕捉、SMPL-X参数化，并赋予细粒度文本、交互顺序和社交/个性标注，为多种下游任务提供统一基准。
primary_logic: 同时提供准确的全身（含手部）运动、细粒度文本、因果交互顺序及社交/个性信息，能够消除现有数据集的碎片化缺陷，使一个统一的数据集即可驱动文本生成、动作识别、反应生成等不同性质的任务，从而系统性地推动人-人交互分析的发展。
claims:
- Inter-X是当前最大的人-人交互数据集，包含约11K段交互序列、8.1M帧，并提供手部姿态和细粒度文本。
- 在文本条件下的人-人交互生成任务中，InterGen在R Precision和FID上均取得最佳表现，验证了细粒度文本标注的有效性。
- 在动作条件生成、反应生成和交互识别任务上，现有模型在Inter-X上均建立了基准性能，其中MS-G3D获得最高交互识别准确率83.30%。
- Inter-X 上 R Precision Top1 = 0.207 (InterGen)
---

# Inter-X: Towards Versatile Human-Human Interaction Analysis

> [!tip] 核心洞察
> 同时提供准确的全身（含手部）运动、细粒度文本、因果交互顺序及社交/个性信息，能够消除现有数据集的碎片化缺陷，使一个统一的数据集即可驱动文本生成、动作识别、反应生成等不同性质的任务，从而系统性地推动人-人交互分析的发展。

| 字段 | 内容 |
|------|------|
| 中文题名 | Inter-X：面向多功能的人-人交互分析 |
| 英文题名 | Inter-X: Towards Versatile Human-Human Interaction Analysis |
| 会议/期刊 | CVPR 2024 |
| Links | [Project](https://liangxuy.github.io/inter-x/) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Inter-X Dataset and Benchmark |
| Dataset | Inter-X |

> [!tip] 效果简介
> - Inter-X 上，R Precision Top1 0.207 (InterGen) vs 0.117 (TEMOS) (+0.090)；FID↓ 5.207 (InterGen) vs 14.415 (TEMOS) (-9.208)。
> - Inter-X (action-cond.) 上，FID↓ 8.067 (Actformer) vs 10.522 (ACTOR) (-2.455)。
> - Inter-X (reaction gen.) 上，FID↓ 4.386 (AGRoL) vs 6.648 (InterGen) (-2.262)。

## 概要

### 问题与瓶颈

人-人交互（Human-Human Interaction, HHI）分析旨在理解、建模并生成两人之间的非语言交流行为，其应用贯穿具身智能、虚拟人动画、社交机器人等前沿领域。然而，该方向长期受困于数据层面的结构性缺陷：现有数据集普遍依赖低精度运动捕捉（如单目RGB估计或稀疏骨架），缺乏手部姿态这一交互核心通道；文本描述粗粒度且数量稀少，难以支撑文本驱动的生成任务；更关键的是，交互的因果顺序（谁主动、谁反应）、人际关系与个性等社交语义标注几乎完全缺失。这些碎片化缺陷导致**没有一个统一的数据集能够同时支持感知（识别、推理）与生成（文本/动作条件生成）两大类任务**，严重阻碍了人-人交互分析的系统性进展。

### 核心方案与洞察

针对上述瓶颈，本文的核心贡献是构建了**Inter-X**——一个大规模、高精度、多模态的人-人交互数据集与基准。其核心洞察在于：**同时提供准确的全身运动（含手部）、细粒度文本描述、因果交互顺序及社交/个性信息，能够消除现有数据集的碎片化缺陷，使一个统一的数据集即可驱动文本生成、动作识别、反应生成等不同性质的任务。**

Inter-X包含约11,000段交互序列、超过810万帧数据，通过**光学-惯性组合运动捕捉系统**（OptiTrack光学相机 + Noitom惯性手套）同步获取身体关键点与手部姿态，并拟合为SMPL-X参数化表示。数据集赋予四层标注：
- **细粒度文本**：覆盖人体部件级别（如“左手握手”“右手挥手”）的语义描述；
- **40类交互动作标签**：涵盖日常社交与对抗性动作；
- **交互顺序**：明确标注演员（Actor）与反应者（Reactor）的因果角色；
- **社交关系与个性评分**：为推理任务提供高层语义监督。

### 方法谱系与知识库定位

Inter-X本身是一个数据集与基准工作，其方法贡献在于**数据构建管线**与**任务映射体系**，而非提出新的算法模型。在评估层面，论文将多个现有模型适配到双人交互场景，建立基准性能：

- **文本条件交互生成**：将**TEMOS**（Petrovich et al., ECCV 2022）、**MDM**（Tevet et al., arXiv 2022）、**MotionDiffuse**（Zhang et al., arXiv 2022）等单人扩散模型扩展为双人版本，并与专为交互设计的**InterGen**（Liang et al., arXiv 2023）对比。
- **动作条件生成与反应生成**：评估**Actformer**（Xu et al., ICCV 2023）与**AGRoL**（Tanaka & Fujiwara, ICCV 2023）等交互专用模型。
- **骨架交互识别**：测试**ST-GCN**（Yan et al., AAAI 2018）、**CTR-GCN**（Chen et al., ICCV 2021）、**HD-GCN**（Lee et al., ICCV 2023）等图卷积网络。

适配策略包括：将运动表示统一为SMPL-X参数、扩展输入/输出维度至双人、保留全局平移以维持相对位置、采用6D连续旋转表示替代欧拉角，以及使用1000步训练配合5步DDIM采样的扩散框架。

### 主要实证结果

Inter-X作为统一基准，揭示了当前方法在不同任务上的能力边界：

| 任务 | 最佳方法 | 核心指标 | 数值 |
|------|---------|---------|------|
| 文本条件交互生成 | InterGen | R Precision Top1 / FID↓ | 0.207 / 5.207 |
| 动作条件交互生成 | Actformer | FID↓ | 8.067 |
| 反应生成 | AGRoL | FID↓ | 4.386 |
| 骨架交互识别 | MS-G3D | Top-1 Accuracy | 83.30% |

在文本条件生成任务上，InterGen的FID（5.207）相比TEMOS（14.415）大幅降低9.208，验证了细粒度文本标注对生成质量的关键作用。然而，交互识别的最佳准确率仅为83.30%，表明即便在高质量数据上，细粒度手势与多样反应的识别仍存在显著挑战。

### 局限与开放问题

Inter-X的构建仍存在若干边界：**未包含面部表情**，限制了情感-交互关联分析；所有数据采集于**室内受控环境**，缺乏野外真实场景的泛化性；交互片段为**原子级短序列**，未覆盖长时多阶段交互。由此衍生出关键开放问题：引入面部表情能否显著提升交互理解与风格化生成？如何将Inter-X的高质量运动迁移到无约束RGB场景？长序列连续交互的数据构建与建模范式应如何设计？这些问题的探索将决定人-人交互分析从受控基准走向开放世界的可行路径。



人-人交互（Human-Human Interaction, HHI）分析是计算机视觉与图形学中的核心课题，其目标是从运动数据中理解、建模并生成两个个体之间的交互行为。这一能力对于虚拟现实、人机交互、具身智能以及社交行为模拟等应用至关重要。然而，该领域长期受困于**数据基础设施的碎片化**——现有数据集在运动捕捉精度、模态覆盖范围以及标注粒度上存在系统性缺陷，无法支撑从感知到生成的统一研究范式。

当前人-人交互数据集的瓶颈可归纳为三个层面。**第一，运动捕捉精度不足。** 多数数据集仅提供稀疏的骨架关节点（skeleton），缺少手部姿态（hand gestures）的精确记录，而手部交互恰恰是握手、击掌、推搡等大量交互动作的关键组成部分。**第二，文本标注匮乏。** 现有数据集要么完全不具备文本描述，要么仅有粗粒度的动作类别标签，缺乏对交互过程中身体部件运动、动作序列顺序以及交互双方关系的细粒度语言刻画。这直接限制了文本驱动的交互生成（text-conditioned generation）和交互字幕（captioning）等跨模态任务的发展。**第三，交互语义标注缺失。** 交互并非对称的——在“推搡”动作中，一方是主动的“演员”（actor），另一方是被动的“反应者”（reactor）；此外，交互双方的社会关系（如朋友、陌生人）和个性特征（如支配性、友好度）也会深刻影响运动模式。现有数据集普遍忽略了这些因果顺序和社交/个性标注，使得交互推理和风格化生成任务无从开展。

这些碎片化缺陷导致了一个恶性循环：研究者只能在不同数据集上针对单一任务进行孤立探索，无法在一个统一的基准上系统性地比较和推进多种下游任务。例如，**InterHuman**（Liang et al., arXiv 2023）虽然提供了较大规模的交互数据，但缺少手部姿态和细粒度文本；**NTU RGB+D**（Shahroudy et al., CVPR 2016）和**NTU RGB+D 120**（Liu et al., TPAMI 2019）虽广泛用于骨架动作识别，但其交互子集规模有限且无文本标注。这种局面使得“构建一个多功能的统一交互分析基准”成为亟待解决的核心问题。

为打破上述瓶颈，**Inter-X** 的构建动机在于：通过一次性构建一个**大规模、高精度、多模态标注完备**的人-人交互数据集，消除现有数据集的碎片化缺陷，使得文本生成、动作识别、反应生成、因果推断、关系/个性推理等不同性质的任务能够在统一的数据基础上协同推进。其核心假设是：**同时提供准确的全身运动（含手部）、细粒度文本描述、因果交互顺序以及社交/个性信息，能够系统性地推动人-人交互分析从孤立的任务探索走向整体性的能力提升。**



## 核心方法与创新机理

Inter-X 的核心创新并非提出全新的算法架构，而是通过系统性地构建一个多模态、高精度的人-人交互数据集，从根本上改变了任务的输入/输出空间和运动表示，从而驱动了一系列下游任务的统一基准建立。其关键创新点体现在以下几个维度：

### 1. 运动表示的范式升级：从骨架到 SMPL-X 全身参数化

现有人-人交互数据集普遍仅提供稀疏骨架关键点（如 NTU RGB+D 系列），且多数缺失手部姿态。Inter-X 通过组合光学运动捕捉（OptiTrack）与惯性手套（Noitom）的方案，首次在交互数据集中提供了包含手部关节的 **SMPL-X 参数化表示**。这一表示升级直接改变了所有下游模型的输入/输出模态——在将单人生成模型扩展至双人场景时，作者明确将运动表示从原模型的表示替换为 SMPL-X 参数（Section 6.1）。这意味着模型不再仅学习身体关节的轨迹，而是可以捕捉到握手时手指的弯曲、指向动作中手部的精细姿态等关键交互细节。

### 2. 输入/输出维度的结构性扩展：单人模型到双人交互的适配

Inter-X 的第二个关键创新在于为现有模型定义了统一的维度扩展策略。在将 **TEMOS**（Petrovich et al., ECCV 2022）、**MDM**（Tevet et al., arXiv 2022）、**MotionDiffuse**（Zhang et al., arXiv 2022）等单人生成模型迁移至交互场景时，作者采用了三方面的结构性修改（Section 6.1）：

- **维度翻倍**：将输入和输出维度从单人扩展为双人，使模型同时预测两位交互者的运动。
- **全局平移保留**：不同于单人生成中常丢弃全局位置信息，交互场景下必须保留两位交互者的全局平移，以维持其相对空间关系（如面对面、并排等）。
- **旋转表示统一**：采用 6D 连续旋转表示替代欧拉角等表示，避免万向节锁等问题，提升旋转预测的连续性。

这一维度扩展策略使得多个原本仅适用于单人的扩散模型无需架构重设计即可直接应用于双人交互生成，形成了可复现的基准对比框架。

### 3. 多模态标注的因果链注入：交互顺序与社交语义

Inter-X 最被低估的创新在于其为交互序列赋予了因果结构和社交语义标注。传统交互数据集仅提供动作类别标签，而 Inter-X 额外标注了：

- **演员-反应者交互顺序**（$l_c$）：明确区分“谁先发起、谁后响应”，使反应生成任务 $F_{c2m}(l_c, \pmb{x}) \mapsto \pmb{y}$ 得以形式化定义（Section 5.3, Equation 5）。
- **人际关系与个性评分**（$\{l_r, l_p\}$）：从运动序列推断社交关系，开辟了交互推理任务 $F_{m2s}(\pmb{m}) \mapsto \{l_r, l_p\}$（Section 5.4, Equation 8）。

这些标注将交互分析从单纯的“动作识别”推向了“因果理解”和“社交推理”，使数据集能够支撑文本生成、动作识别、反应生成、因果推断、关系推理等四类性质迥异的下游任务（Figure 1）。

### 4. 扩散模型采样效率的实用优化

在将扩散模型应用于交互生成时，作者采用了 **1000 步训练、5 步 DDIM 采样**的策略（Section 6.1）。这一设计并非理论创新，但在交互场景下具有实用意义——双人运动序列的维度是单人的两倍，若采样步数过多将导致推理效率急剧下降。5 步 DDIM 采样在保持生成质量的同时大幅降低了推理成本，使得交互生成在实际应用中更具可行性。

### 创新边界与局限

需指出，Inter-X 的创新集中于数据层面和任务定义层面，其基准模型本身（InterGen、Actformer、AGRoL 等）均是对现有架构的维度扩展适配，并未提出专门针对交互特性的新型网络结构。此外，数据集未包含面部表情、所有采集均在室内环境完成、交互片段为原子级短序列，这些限制意味着在情感交互、野外泛化、长时多阶段交互等方向仍存在显著的创新空间。



Inter-X 的整体框架围绕“高精度多模态数据采集 → 统一参数化表示 → 多任务映射”这一主线构建，旨在用一个数据集同时支撑交互生成、识别、推理等不同性质的下游任务。

### 数据采集与参数化管线

框架的输入端是一套**光学-惯性混合运动捕捉系统**（Figure 2）。身体关键点由 OptiTrack 光学相机以亚毫米精度采集，手部姿态则通过 Noitom 惯性手套在遮挡场景下补全——两者通过三角定位支架在空间上固连，在时间上取交集实现同步。这一设计直接回应了现有数据集“身体精度不足、手部缺失”的结构性瓶颈。

![[assets/figures/papers/paper_list_l1720_Inter_X_Towards_Versatile_Human_Human_Interaction_Analysis/figures/003_Figure_2.jpg]]
*Figure 2: An overview of the Inter-X capture system. (a). The optical MoCap clothing together with the inertial gloves are spatially integrated via a triangular bracket of reflective markers; (b). The details of the markers setup; (c). The body and hands are temporally synchronized in the whole-body MoCap framework*

采集到的原始关节点随后被拟合为统一的 **SMPL-X 参数**。拟合目标函数为：

$$E(\theta, t) = \lambda_1 \frac{1}{N} \sum_{j \in \mathcal{I}} \lambda_p ||\pmb{J}_j(\mathbb{M}(\theta, t)) - \pmb{g}_j||_2^2 + \lambda_2 ||\theta||_2^2$$

其中 $\mathbb{M}(\theta,t)$ 为 SMPL-X 模型，$\pmb{g}_j$ 为捕捉到的关节点位置，加权项 $\lambda_p$ 对不同关节赋予不同置信度，正则项 $||\theta||_2^2$ 抑制异常姿态。这一步将异构传感数据统一为可微、可编辑的参数空间，是整个 pipeline 的表示基础。

### 多模态标注层

在参数化运动之上，框架叠加了四类标注，构成任务定义的语义层：

- **细粒度文本描述**：覆盖身体部件级别的交互语义，用于文本-运动双向生成（Eq.1-2）。
- **40 类交互动作标签**：支持动作条件生成与识别（Eq.3-4）。
- **演员-反应者交互顺序**：明确因果方向，使反应生成（Eq.5）和顺序推理（Eq.6）成为可能。
- **人际关系与个性评分**：从社交维度拓展交互理解（Eq.8）。

这些标注并非孤立存在，而是通过**任务映射函数**与运动序列关联——每个任务被形式化为一个从特定模态到运动（或反向）的映射，使得同一批数据可以驱动文本生成、动作识别、反应生成等不同性质的下游任务，消除了以往“一个数据集只服务一类任务”的碎片化问题。

### 模型适配策略

在将现有单人模型迁移到双人交互场景时，框架采用了一组统一的**维度与表示适配**策略：将输入/输出维度扩展为双人，运动表示切换为 SMPL-X 参数，旋转采用 6D 连续表示，并保留全局平移以维持两人相对位置。扩散模型统一使用 1000 步训练、5 步 DDIM 采样。这一适配层确保不同基线模型（TEMOS、MDM、MotionDiffuse、Actformer、AGRoL 等）可在同一基准上公平比较，而无需为每个模型单独设计输入输出逻辑。



Inter-X数据集的核心技术链路包含四个关键模块，从原始运动捕捉到多模态标注生成，最终映射为下游任务的学习目标。

### 1. 光学与惯性运动捕捉系统

为解决纯光学方案在手部被遮挡时的失效问题，系统采用**混合捕捉架构**（Figure 2）：身体运动由OptiTrack光学相机通过反光标记点捕捉，手部姿态则由Noitom惯性手套独立记录。两者通过一个**三角形定位支架**在空间上刚性集成——支架上安装反光标记点以获取腕部在光学坐标系下的旋转，惯性手套则共享该腕部旋转实现空间对齐。时间维度上，取身体姿态序列与手部姿态序列的**交集**完成同步。这一设计使得身体运动的高精度与手部手势的抗遮挡能力得以兼得。

### 2. SMPL-X参数拟合与时空对齐

捕捉到的关节点需转化为统一的参数化人体表示，以便进行运动生成与分析。拟合过程求解以下优化目标（Section 4.1）：

$$E(\theta, t) = \lambda_1 \frac{1}{N} \sum_{j \in \mathcal{I}} \lambda_p ||\pmb{J}_j(\mathbb{M}(\theta, t)) - \pmb{g}_j||_2^2 + \lambda_2 ||\theta||_2^2$$

其中：
- $\theta$ 为SMPL-X的姿态参数，$t$ 为全局平移；
- $\mathbb{M}(\theta, t)$ 表示SMPL-X模型的正向运动学映射；
- $\pmb{J}_j$ 为模型输出的第$j$个关节位置，$\pmb{g}_j$ 为对应捕捉到的关键点位置；
- $\mathcal{I}$ 为参与拟合的关节点索引集，$\lambda_p$ 为各关节的**差异化权重**（身体关节与手部关节采用不同权重以平衡精度）；
- $\lambda_1$ 控制数据项强度，$\lambda_2$ 为正则化系数，约束姿态参数的$L_2$范数以抑制异常姿态。

拟合完成后，身体与手部在SMPL-X参数空间中自然统一，无需额外后处理。

### 3. 多模态标注生成

在原始运动数据之上，Inter-X叠加了四层语义标注：

- **细粒度文本描述**：针对交互序列生成人类部件级（body-part-level）的自然语言描述，覆盖动作类型、接触部位、交互方式等细节。
- **40类交互动作标签**：涵盖握手、拥抱、推搡等常见人-人交互类别，作为动作条件生成与识别任务的监督信号。
- **演员-反应者交互顺序**：明确标注每段交互中谁是主动发起者（actor）、谁是被动响应者（reactor），使得因果顺序推理和反应生成成为可能。
- **人际关系与个性评分**：为交互对标注社交关系类型（如朋友、陌生人）和个性特征评分，支撑社会信号理解任务。

### 4. 任务映射函数

上述标注通过一组形式化映射函数与运动序列关联，定义了Inter-X基准所支持的各类下游任务（Section 5）：

| 任务 | 映射函数 | 含义 |
|------|----------|------|
| 文本→运动生成 | $F_{t2m}(l_t) \mapsto m$ | 从文本描述$l_t$生成交互序列$m$ |
| 运动→文本描述 | $F_{m2t}(\boldsymbol{m}) \mapsto l_t$ | 从交互序列生成文本描述 |
| 动作标签→运动生成 | $F_{a2m}(l_a) \mapsto m$ | 从动作类别$l_a$生成交互序列 |
| 运动→动作识别 | $F_{m2a}(m) \mapsto l_a$ | 从交互序列识别动作类别 |
| 反应生成 | $F_{c2m}(l_c, \pmb{x}) \mapsto \pmb{y}$ | 给定顺序$l_c$和演员运动$\pmb{x}$，生成反应者运动$\pmb{y}$ |
| 因果顺序推断 | $F_{m2c}(\pmb{m}) \mapsto l_c$ | 从交互序列推断actor-reactor顺序 |
| 关系与个性推断 | $F_{m2s}({\pmb m}) \mapsto \{l_r, l_p\}$ | 从运动推断社交关系$l_r$和个性$l_p$标签 |

这些映射函数构成了Inter-X统一基准的理论骨架——同一数据集通过不同的输入-输出配对即可驱动文本生成、动作识别、反应生成、社交推理等性质迥异的下游任务，消除了以往各任务依赖碎片化数据集的痛点。



## 实验与关键发现

### 文本条件交互生成

文本条件交互生成任务要求模型从细粒度文本描述直接合成双人交互运动序列。实验将多个基线方法适配到Inter-X数据集上，统一使用SMPL-X参数表示、6D连续旋转表示，并保留全局平移以维持相对位置关系。所有扩散模型均采用1000步训练、5步DDIM采样。

**Table 2** 给出了定量对比结果。**InterGen**（Liang et al., arXiv 2023）在R Precision Top 1上达到**0.207**，显著优于第二名的TEMOS（Petrovich et al., ECCV 2022）的0.117，提升约**+0.090**；在FID指标上，InterGen取得**5.207**，较TEMOS的14.415大幅降低**-9.208**。这表明细粒度文本标注能够有效引导模型生成更符合语义且更真实的交互运动。然而，InterGen在MM Dist指标上并非最优，提示文本-运动对齐的细粒度匹配仍有改进空间。

MotionDiffuse（Zhang et al., arXiv 2022）和MDM（Tevet et al., arXiv 2022）在R Precision和FID上表现居中，ComMDM则相对落后，说明简单的双人维度扩展不足以充分捕获交互语义。

**Figure 4** 的定性对比进一步揭示了数据集质量对生成结果的影响。在InterHuman数据集上训练的模型生成的“握手”动作中，手部仅以球体示意且无手指姿态；而在Inter-X上训练的模型则能生成完整的手部交互细节。这直接验证了Inter-X引入手部姿态标注的核心价值。

### 动作条件生成与反应生成

动作条件交互生成以离散动作标签为条件合成运动。**Table 3** 显示，**Actformer**（Xu et al., ICCV 2023）在FID上取得**8.067**，优于ACTOR的10.522（Δ = -2.455），动作识别准确率达到0.945。这表明Actformer的Transformer架构在条件信号利用上具有优势。

![[assets/figures/papers/paper_list_l1720_Inter_X_Towards_Versatile_Human_Human_Interaction_Analysis/figures/007_Table_3.jpg]]
*Table 3: Experimental results of action-conditioned interaction generation on the Inter-X dataset. Bold for best results*

反应生成任务给定演员运动和交互顺序，生成反应者运动。**Table 4** 中，**AGRoL**（Tanaka & Fujiwara, ICCV 2023）在所有指标上均取得最优：FID **4.386**、动作识别准确率0.925、多样性12.204、多模态20.199。相较于InterGen在该任务上的FID 6.648，AGRoL的FID降低了**-2.262**，说明专门设计的反应生成架构比通用交互生成模型更适合该任务。

![[assets/figures/papers/paper_list_l1720_Inter_X_Towards_Versatile_Human_Human_Interaction_Analysis/figures/008_Table_4.jpg]]
*Table 4: Experimental results of human reaction generation based on action labels on the Inter-X dataset. Bold for best results*

### 骨架交互识别

交互识别任务从骨架序列中预测交互动作类别。**Table 5** 汇总了多个主流骨架识别模型在Inter-X上的表现。**MS-G3D** 取得最高Top-1准确率**83.30%**，优于CTR-GCN（Chen et al., ICCV 2021）的80.48%（Δ = +2.82%）和HD-GCN（Lee et al., ICCV 2023）的82.17%。ST-GCN（Yan et al., AAAI 2018）和2s-AGCN（Shi et al., CVPR 2019）作为早期方法，准确率分别为72.15%和75.63%，反映出多尺度时空图卷积对交互建模的增益。

![[assets/figures/papers/paper_list_l1720_Inter_X_Towards_Versatile_Human_Human_Interaction_Analysis/figures/009_Table_5.jpg]]
*Table 5: Experimental results of skeleton-based human interaction recognition on the Inter-X dataset. Bold for best results*

值得注意的是，83.30%的最高准确率在40类交互识别任务中仍不理想。论文明确指出，细粒度手势和多样反应/动作模式是当前识别精度的主要瓶颈——手部姿态的细微差异和交互风格的多样性使得类别边界模糊，现有模型尚不能充分捕获这些细粒度判别特征。

### 关键实验结论

1. **细粒度文本标注的有效性**：InterGen在文本条件生成任务上的显著优势（R Precision +0.090，FID -9.208）直接证明了Inter-X细粒度文本标注对条件生成任务的驱动作用。
2. **手部姿态的重要性**：Figure 4中InterHuman与Inter-X的生成对比，以及识别任务中精度瓶颈的分析，共同表明手部姿态是交互理解与生成的关键维度。
3. **任务特化架构的必要性**：反应生成任务中AGRoL显著优于通用InterGen（FID -2.262），说明针对特定交互任务设计专用架构比简单扩展单人模型更有效。
4. **交互识别仍有较大挑战**：最优准确率83.30%表明，在涵盖细粒度手势和多样反应的40类交互识别上，现有模型仍存在明显不足，需要进一步的方法创新。

### 补充图表

![[assets/figures/papers/paper_list_l1720_Inter_X_Towards_Versatile_Human_Human_Interaction_Analysis/figures/002_Table_1.jpg]]
*Table 1: Dataset comparisons. We compare our Inter-X dataset with the existing human-human interaction datasets. Motions: The number of the motion clips; Frames: The frame number of the 3D human motions; Texts: The number of the textual descriptions; Scheme: The strategy to obtain the motion data; Modality: The representation of the motion data and “Skel.” denotes skeleton; Hands, Asyn. and Rel.&Pst. refer to the components of hand gestures, asymmetry annotations, human-human relationships and personalities*

![[assets/figures/papers/paper_list_l1720_Inter_X_Towards_Versatile_Human_Human_Interaction_Analysis/figures/005_Table_2.jpg]]
*Table 2: Experimental results of text-conditioned interaction generation on the Inter-X dataset, where ± indicates 95% confidence interval and → means the closer the better. Bold indicates best results*

![[assets/figures/papers/paper_list_l1720_Inter_X_Towards_Versatile_Human_Human_Interaction_Analysis/figures/006_Figure_4.jpg]]
*Figure 4: Visualization results of the generated results on the InterHuman [54] and Inter-X dataset via ait-viewer [1]. From top to bottom, the action categories are “Handshake”, “Wave” and “Shoulder to shoulder”, respectively. Please zoom in for the details*

![[assets/figures/papers/paper_list_l1720_Inter_X_Towards_Versatile_Human_Human_Interaction_Analysis/figures/001_Figure_1.jpg]]
*Figure 1: An overview of the data and task taxonomy of our proposed Inter-X dataset, which is a large-scale human-human interaction MoCap dataset with ∼11K interaction sequences and more than 8.1M frames. The fine-grained textual descriptions, semantic action categories, interaction order, and relationship and personality annotations allow for 4 categories of downstream tasks*



## 定位与知识库关联

### 1. 与现有工作的关系与继承

Inter-X 的核心贡献在于构建了一个统一、多模态的人-人交互基准，其方法论定位并非提出全新的生成或识别模型，而是通过数据集的质量与标注维度，将多个原本孤立的单人模型适配到双人交互场景，并系统性地揭示现有模型的能力边界。

**与单人运动模型的继承关系。** 在文本条件交互生成任务中，论文将四个代表性的单人文本-运动生成模型扩展至双人设定：**TEMOS**（Petrovich et al., ECCV 2022）、**MDM**（Tevet et al., arXiv 2022）、**MotionDiffuse**（Zhang et al., arXiv 2022）以及专门为双人交互设计的 **InterGen**（Liang et al., arXiv 2023）。扩展的核心技术槽位包括：将运动表示统一替换为 SMPL-X 参数、将输入/输出维度从单人扩展为双人、保留全局平移以维持交互双方的相对位置、采用 6D 连续旋转表示替代 Euler 角，并将扩散模型的采样策略统一为 1000 步训练与 5 步 DDIM 采样（Section 6.1）。这一系列改造使得原本面向单人的生成模型能够直接处理双人交互序列，从而在统一基准上进行公平比较。

**与动作条件生成及反应生成模型的关系。** 在动作条件交互生成任务中，基线方法包括 **Actformer**（Xu et al., ICCV 2023）和 **ACTOR** 等。在反应生成任务中，**AGRoL**（Tanaka & Fujiwara, ICCV 2023）被改造为以演员运动为条件、以反应者运动为输出的架构。这些改造均遵循相同的范式：保留原模型的核心生成机制，仅通过维度调整和条件注入使其适配双人交互场景。

**与骨架交互识别模型的关系。** 在交互识别任务上，论文直接沿用了经典的骨架动作识别模型，包括 **ST-GCN**（Yan et al., AAAI 2018）、**2s-AGCN**（Shi et al., CVPR 2019）、**CTR-GCN**（Chen et al., ICCV 2021）、**MS-G3D** 以及 **HD-GCN**（Lee et al., ICCV 2023）。这些模型在 Inter-X 上的性能表现（最高 Top-1 准确率 83.30%，由 MS-G3D 取得）直接反映了现有图卷积架构在处理细粒度手势和多样化交互时的瓶颈。

### 2. 适用边界与泛化性分析

Inter-X 数据集及基于其建立的基准具有明确的适用边界，这些边界直接源于其采集方式和标注设计。

**室内受控环境的局限。** 所有运动数据均通过光学与惯性组合系统在室内动作捕捉环境中采集。尽管这保证了运动精度和手部姿态的完整性，但也意味着数据分布无法覆盖户外真实场景中的光照变化、遮挡、背景干扰等因素。因此，当前基准上的模型性能不能直接外推至无约束的野外交互分析任务。

**原子级交互片段的粒度限制。** 数据集中的交互序列均为短时、原子级别的片段（约 11K 段序列），未包含长时、多阶段的复杂交互过程。这意味着当前基准主要评估模型对孤立交互动作的建模能力，而非对连续交互流中上下文依赖和意图演变的捕捉。

**面部表情的缺失。** 数据集未包含面部表情信息，这限制了其在情感感知、社交信号理解以及风格化交互生成等任务上的适用性。对于需要将情感状态与运动模式关联的分析场景，Inter-X 无法提供直接支持。

**手部姿态的精度折衷。** 尽管集成了 Noitom 惯性手套以捕捉手部姿态，但惯性传感器固有的漂移问题可能导致手部手势存在误差累积。在需要极高手指精度（如手语理解、精细操作分析）的任务中，这一局限需要被审慎评估。

### 3. 局限性与开放问题

**局限性的因果溯源。** 从方法论角度看，Inter-X 的核心局限并非数据集规模或标注质量不足，而是其作为“统一基准”的定位本身带来的权衡：为了覆盖文本生成、动作识别、反应生成等多种任务，数据集在单一维度的深度上（如长序列、野外场景、情感标注）必然有所妥协。此外，当前交互识别最高准确率仅 83.30%，表明即使是最优的骨架图卷积模型，在面对 Inter-X 中丰富的细粒度手势和多样反应时仍存在显著性能缺口——这本质上反映了现有模型对双人交互中空间关系与时间因果性的建模能力不足。

**开放问题。**

1. **面部表情的整合价值。** 引入面部表情后，能否显著提升交互理解（如意图推断）和风格化生成（如情感一致的动作合成）的质量？这需要构建包含面部、身体、手部三者同步的新数据集，并设计相应的多模态融合架构。

2. **从室内到野外的迁移。** 如何将 Inter-X 的高质量运动先验转移到野外 RGB 场景中？可能的路径包括：利用 Inter-X 数据训练运动先验模型，再通过域适应或知识蒸馏将其注入到基于 RGB 视频的交互分析模型中。

3. **长序列连续交互建模。** 当交互从原子片段扩展到分钟级的多阶段过程时，模型需要同时捕捉短期动作语义和长期意图演化。这要求数据构建方案引入层次化的时间标注，以及模型架构具备记忆与规划能力。

4. **交互识别精度的突破方向。** 当前 83.30% 的准确率天花板是否可以通过自监督预训练或引入文本-运动对比学习来突破？这本质上是在问：是否需要更强的表示学习范式，而非仅仅改进图卷积的拓扑设计。

5. **个性与社交关系的可解释建模。** 论文提出了从运动推断关系与个性标签的任务（$F_{m2s}(\pmb m) \mapsto \{l_r, l_p\}$），但个性和社交关系对运动模式的细微影响如何被可解释地建模并应用于条件生成，仍是一个开放的因果推断问题——需要回答“是什么运动特征揭示了关系类型”而非仅仅“能否分类准确”。



## 原文 PDF

![[paperPDFs/CVPR_2024/Inter_X_Towards_Versatile_Human_Human_Interaction_Analysis.pdf]]
