---
title: "Uni-HOI: A Unified framework for Learning the Joint distribution of Text and Human-Object Interaction"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/Uni_HOI_A_Unified_Framework_for_Learning_the_Joint_Distribution_of_Text_and_Human_Object_Interaction.pdf
project_link: null
code_link: null
aliases:
- UH
- Uni-HOI
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入两个运动专用VQ-VAE将异构运动数据离散化为LLM兼容的token序列，并与文本token合并为统一词表，利用预训练LLM进行自回归建模；配合两阶段训练策略（多任务预训练+任务特定微调），使模型能接受任意模态子集作为条件生成剩余模态。
primary_logic: 将人体运动和物体运动视为两种“外语”，通过离散词表与自然语言对齐，借助LLM强大的序列建模能力捕获跨模态依赖，从而在单一框架下实现多种HOI任务的统一处理。
claims:
- Uni-HOI是第一个在HOI领域实现文本、人体运动和物体运动联合分布对齐的统一框架。
- 两个运动专用VQ-VAE将人体运动与物体运动转化为离散token，使其能与LLM输入兼容。
- 两阶段训练策略（大规模多任务预训练后接任务特定微调）显著提升模型在多种HOI任务上的性能。
- 在FullBodyManipulation和BEHAVE等基准上，Uni-HOI的FID等指标超越了专门设计的文本驱动HOI基线方法（ROG、HOI-Diff）。
---

# Uni-HOI: A Unified framework for Learning the Joint distribution of Text and Human-Object Interaction

> [!tip] 核心洞察
> 将人体运动和物体运动视为两种“外语”，通过离散词表与自然语言对齐，借助LLM强大的序列建模能力捕获跨模态依赖，从而在单一框架下实现多种HOI任务的统一处理。

| 字段 | 内容 |
|------|------|
| 中文题名 | Uni-HOI：学习文本与人物交互联合分布的统一框架 |
| 英文题名 | Uni-HOI: A Unified framework for Learning the Joint distribution of Text and Human-Object Interaction |
| 会议/期刊 | arXiv 2026 |
| Links |  [paper](https://arxiv.org/abs/2604.27491)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Uni-HOI |
| Dataset | FullBodyManipulation, BEHAVE, GRAB |

> [!tip] 效果简介
> - FullBodyManipulation (text-to-HOI) 上，FID 5.13 vs 5.35 (ROG) (-0.22)；Top-1 R-precision 0.45 vs 0.42 (ROG) (+0.03)。
> - BEHAVE (text-to-HOI) 上，FID 0.37 vs 0.42 (ROG) (-0.05)。
> - FullBodyManipulation (object-to-human w/ text) 上，HandJPE 27.56 vs not explicitly reported (—)。

## 概要

### 问题瓶颈

人物交互（Human-Object Interaction, HOI）生成是具身AI与数字人建模的核心问题，涵盖文本驱动的交互生成、物体运动引导的人体运动合成、以及人体运动驱动的物体姿态预测等多种子任务。现有方法普遍采用任务特定架构——例如**ROG**（Xue et al., CVPR 2025）和**HOI-Diff**（Peng et al., CVPR 2025）专注于文本到HOI的扩散生成，**OMOMO**（Li et al., TOG 2023）处理物体运动到人体运动的映射，**ObjPOP**（Petrov et al., CVPR 2023）则面向人体到物体的姿态预测——这些方法各自为政，无法以单一模型灵活处理多种条件输入组合。其根本瓶颈在于：缺乏对文本、人体运动与物体运动三模态联合分布的统一建模，导致跨任务知识无法共享，模型泛化能力受限。

### 核心方法

**Uni-HOI**提出了一个学习文本与人物交互联合分布的统一框架。其核心洞察是将人体运动和物体运动视为两种“外语”，通过离散词表与自然语言对齐，借助大语言模型（LLM）强大的序列建模能力捕获跨模态依赖。具体而言，方法包含三个关键设计：

1. **运动离散化**：引入两个运动专用VQ-VAE，分别将SMPL-H参数化的人体运动序列（$D_h=159$）和物体6D姿态序列（$D_o=6$）编码为离散token序列，使其与文本token兼容于同一词汇表。
2. **统一自回归骨干**：基于Qwen3-8B构建统一Transformer，将文本token、人体运动token、物体运动token及物体几何特征token合并为单一输入序列，以自回归方式建模条件概率$p_\theta(\mathbf{X}_t|\mathbf{X}_s)$。
3. **两阶段训练**：第一阶段在多任务设定下进行大规模预训练——从三模态集合$Q=\{T,H,O\}$中随机选取子集作为条件，其余作为目标，学习联合分布；第二阶段在特定子任务上进行LoRA微调，进一步提升任务针对性性能。

### 主要结果

在FullBodyManipulation和BEHAVE两个基准数据集上，Uni-HOI以单一统一框架在多项HOI任务上达到或超越了专门设计的基线方法：

- **文本驱动HOI生成**：在FullBodyManipulation上，FID达到5.13（ROG为5.35），Top-1 R-precision达到0.45（ROG为0.42）；在BEHAVE上，FID为0.37（ROG为0.42）。
- **物体运动驱动人体运动生成**：在FullBodyManipulation上，HandJPE降至27.56，显著优于对比方法。
- **人体运动驱动物体运动预测**：在GRAB数据集上，物体平移误差$E_c$降至0.024，大幅领先ObjPOP。

定性可视化进一步表明，Uni-HOI生成的交互在物理合理性上优于基线，减少了不合理的穿透或脱离现象。此外，Uni-HOI还展示了从参考视频中的人体运动预测合理物体运动的4D HOI合成能力，验证了框架的实用拓展性。



### 问题域：人物交互（HOI）中的多模态建模

人物交互（Human-Object Interaction, HOI）是具身智能与视觉运动生成中的核心问题，其本质在于捕捉文本描述、人体运动与物体运动三个模态之间的复杂依赖关系。例如，“用双手将椅子推开”这一简短指令，同时约束了人体的全身姿态、手部轨迹以及椅子的平移与旋转。因此，理想的HOI模型需要理解并生成这三个模态的联合行为。

### 现有方法的瓶颈：任务特定架构与模态割裂

当前HOI研究呈现出明显的“任务分割”特征：文本驱动HOI生成（如**ROG** [Xue et al., CVPR 2025]、**HOI-Diff** [Peng et al., CVPR 2025]）、物体运动驱动人体运动生成（如**OMOMO** [Li et al., TOG 2023]）、人体运动驱动物体姿态预测（如**ObjPOP** [Petrov et al., CVPR 2023]）各自采用独立的模型架构与训练范式。这些方法虽然在其专攻任务上取得了进展，但存在根本性局限——它们无法以单一模型灵活处理多种条件输入组合。其深层原因在于：**现有方法缺乏对文本、人体运动与物体运动三模态联合分布的统一建模**，每个模型仅学习条件分布的一个特定切片（如 $p(H,O|T)$ 或 $p(H|O)$），模态间的共享结构与互补信息未能被系统性利用。

### 核心洞察：将运动视为“外语”，借助LLM统一建模

本文的核心洞察是：人体运动和物体运动可以分别被视为两种“外语”，通过离散词表与自然语言对齐，即可借助大型语言模型（LLM）强大的序列建模能力捕获跨模态依赖。这一思路将异构的运动数据（连续关节角、6D姿态）转化为LLM可消费的统一token序列，从而将多模态HOI生成问题规约为条件序列建模问题。

### 本文动机与目标

基于上述洞察，本文提出**Uni-HOI**——首个在HOI领域实现文本、人体运动与物体运动联合分布对齐的统一框架。其设计目标为：**以单一模型接受任意模态子集作为条件，生成剩余模态**，从而在同一框架下支撑文本驱动交互生成、物体引导人体运动生成、人体驱动物体运动预测等多类HOI任务。为实现这一目标，Uni-HOI引入两个运动专用VQ-VAE将连续运动离散化，并与文本token合并为统一词表，利用预训练LLM进行自回归建模，配合两阶段训练策略（大规模多任务预训练 + 任务特定微调）实现跨任务的性能提升。



## 核心方法与创新机理

Uni-HOI 的核心创新在于**首次将文本、人体运动与物体运动三模态的联合分布建模统一于单一框架之中**，从而突破了现有 HOI 方法各自为政、任务特定架构的瓶颈。其关键设计围绕以下三个层面展开：

### 1. 异构运动数据的离散化与 LLM 对齐

现有方法通常以连续参数化方式分别处理人体运动（如 SMPL-H 关节角）与物体运动（如 6D 姿态），导致不同模态的表示空间相互割裂，难以在同一模型内融合。Uni-HOI 引入两个运动专用 VQ-VAE，将人体运动序列 $H = \{ h_i \} \in \mathbb{R}^{L \times 159}$ 与物体运动序列 $O = \{ o_i \} \in \mathbb{R}^{L \times 6}$ 分别编码为离散 token 序列。量化操作通过最近邻查找实现：

$$\mathbf{z}_i = Q(\hat{\mathbf{z}}_i) := \arg\min_{\mathbf{z}_k \in \mathcal{Z}} \|\hat{\mathbf{z}}_i - \mathbf{z}_k\|_2$$

这一设计的本质是将人体运动和物体运动视为两种“外语”，通过离散码本与自然语言 token 对齐，使得三种模态能够共享统一的词汇表 $V = \{V_t, V_h, V_o\}$，进而被同一个 LLM 骨干（Qwen3-8B）以自回归方式处理。这从根本上解决了多模态输入表示异构的问题，是统一框架得以成立的基础。

### 2. 统一自回归 Transformer 架构

与现有方法采用任务特定扩散模型（如 **ROG**、**HOI-Diff**）或分离式条件编码不同，Uni-HOI 将所有模态的 token 置于同一序列中，由 Qwen3-8B 的自回归 decoder 逐 token 预测条件概率分布：

$$p_\theta(\mathbf{X}_t | \mathbf{X}_s) = \prod_{i=0}^{L-1} p_\theta(x_{t_i} \mid x_t^{<i}, \mathbf{X}_s)$$

训练目标为最大化目标 token 的对数似然：

$$\mathcal{L}_{\mathrm{LM}} = - \sum_{i=0}^{L-1} \log p_\theta(x_{t_i} \mid x_t^{<i}, \mathbf{X}_s)$$

此外，物体几何信息通过 MLP 网络从静态点云中提取特征，作为特殊的 `<object geometry token>` 插入输入序列，替代了传统方法中需要专用点云编码器的做法。这一统一架构使得模型能够以任意模态子集作为条件，生成剩余模态，覆盖 $\mathcal{T} = \{ (X, y) \mid X \subset Q, y = Q \setminus X \}$ 中所有可行的 HOI 任务组合。

### 3. 两阶段训练策略

传统方法通常针对单个任务从零开始训练，缺乏跨任务的泛化能力。Uni-HOI 采用两阶段训练策略：

- **第一阶段**：在多任务设定下进行大规模预训练，随机组合模态作为条件与目标，使模型学习三模态的联合分布；
- **第二阶段**：在特定子任务上使用更小的 LoRA rank 和 scaling coefficient 进行微调，进一步提升任务特定性能。

这一策略使模型既能从多任务学习中获益，又能在特定任务上精细优化，在 FullBodyManipulation 和 BEHAVE 等基准上超越了专门设计的基线方法（如 ROG 的 FID 5.35 vs. Uni-HOI 的 5.13）。

### 关键创新总结

| 设计维度 | 现有方法 | Uni-HOI |
|---------|---------|---------|
| 运动表示 | 连续参数化或独立编码器 | 两个 VQ-VAE 离散化为统一 token |
| 融合架构 | 任务特定扩散模型 | 统一自回归 Transformer (Qwen3-8B) |
| 训练范式 | 单任务从头训练 | 多任务预训练 + 任务特定 LoRA 微调 |
| 物体几何注入 | 专用点云编码器 | MLP 提取特征作为特殊 token |



Uni-HOI 的核心设计动机源于一个根本瓶颈：现有 HOI 方法均为任务特定架构，无法以单一模型灵活处理文本驱动、物体运动驱动等多种条件输入，缺乏对文本、人体运动与物体运动三模态联合分布的统一建模。为解决这一问题，Uni-HOI 提出将人体运动和物体运动视为两种“外语”，通过离散词表与自然语言对齐，借助预训练大语言模型的序列建模能力捕获跨模态依赖，从而在单一框架下实现多种 HOI 任务的统一处理。

### 三模态统一表示

框架的输入空间由三个模态构成：文本描述 $T$、人体运动序列 $H$ 和物体运动序列 $O$。人体运动采用 SMPL-H 模型参数化，维度 $D_h = 159$；物体运动由平移和旋转变换表示，维度 $D_o = 6$。两者均以长度为 $L$ 的序列形式存在：

$$H = \{ h_i \} \in \mathbb{R}^{L \times D_h}, \quad O = \{ o_i \} \in \mathbb{R}^{L \times D_o}$$

为将这些异构的连续运动数据纳入语言模型的离散 token 空间，Uni-HOI 分别预训练了两个运动专用 VQ-VAE，作为人体运动分词器（Human Motion Tokenizer）和物体运动分词器（Object Motion Tokenizer）。每个 VQ-VAE 将运动序列编码为隐向量后，通过最近邻查找在码本 $\mathcal{Z}$ 中进行离散量化：

$$\mathbf{z}_i = Q(\hat{\mathbf{z}}_i) := \arg\min_{\mathbf{z}_k \in \mathcal{Z}} \|\hat{\mathbf{z}}_i - \mathbf{z}_k\|_2$$

量化后的离散索引序列即为 LLM 可消费的运动 token。两个分词器的码本大小均设置为 $K \in \mathbb{R}^{512 \times 4096}$。VQ-VAE 的总训练损失由重建损失、嵌入损失、承诺损失和速度正则化四项构成：

$$\mathcal{L}_V = \mathcal{L}_r + \mathcal{L}_e + \mathcal{L}_c + \mathcal{L}_v$$

### 统一词表与序列构建

在获得运动 token 后，Uni-HOI 将文本 token 表 $\mathcal{V}_t$、人体运动 token 表 $\mathcal{V}_h$ 和物体运动 token 表 $\mathcal{V}_o$ 合并为统一词表 $\mathcal{V} = \{\mathcal{V}_t, \mathcal{V}_h, \mathcal{V}_o\}$。此外，为注入物体的静态几何信息，框架设计了一个 MLP 网络从输入物体点云（340 点）中提取特征，并将其作为特殊的 `<object geometry token>` 插入输入序列。这一设计替代了传统方法中将点云送入专用编码器或条件扩散模型的做法，实现了几何信息与序列建模的轻量融合。

### 骨干网络与自回归生成

Uni-HOI 采用 **Qwen3-8B** 作为底层 Transformer 骨干。给定源序列 $\mathbf{X}_s$（条件模态），解码器以自回归方式逐时间步预测目标序列 $\mathbf{X}_t$ 的概率分布：

$$p_\theta(\mathbf{X}_t | \mathbf{X}_s) = \prod_{i=0}^{L-1} p_\theta(x_{t_i} \mid x_t^{<i}, \mathbf{X}_s)$$

训练目标为最大化目标 token 的对数似然：

$$\mathcal{L}_{\mathrm{LM}} = - \sum_{i=0}^{L-1} \log p_\theta(x_{t_i} \mid x_t^{<i}, \mathbf{X}_s)$$

### 任务空间与两阶段训练

Uni-HOI 的建模任务空间 $\mathcal{T}$ 覆盖了从三模态集合 $\mathcal{Q} = \{T, H, O\}$ 中选取任意非空真子集作为条件、其余作为目标的所有可行划分：

$$\mathcal{T} = \{ (X, y) \mid X \subset \mathcal{Q}, y = \mathcal{Q} \setminus X, X \notin \{\emptyset, \mathcal{Q}\} \}$$

统一训练目标在所有模态划分上最小化期望损失：

$$\theta^* = \arg\min_\theta \sum_{(X, y) \in \mathcal{T}} \mathbb{E}_{(P, T, H, O) \sim \mathcal{D}} \left[ \ell( \mathcal{Y}, U_\theta(P, X) ) \right]$$

训练采用两阶段策略。第一阶段进行大规模多任务预训练，随机组合模态作为条件与目标，在最大规模的 HOI 数据集上训练 110K 迭代；第二阶段针对特定任务进行 LoRA 微调，采用更小的秩和缩放系数，训练 50K 迭代。两个阶段均使用 8 张 NVIDIA GeForce RTX 4090 GPU，学习率为 1e-6，批次大小为 128。

### 支持的 HOI 任务

基于上述统一架构，Uni-HOI 可根据不同的条件配置灵活切换三种核心 HOI 任务（见图 2）：
- **文本驱动 HOI 生成** $U(H, O \mid T)$：给定文本描述，同时生成人体运动与物体运动。
- **物体运动驱动人体运动生成** $U(H \mid O[, T])$：给定物体运动序列（可选附加文本），生成相应的人体运动。
- **人体运动驱动物体运动预测** $U(O \mid H)$：给定人体运动序列，预测物体的 6D 姿态轨迹。

### 补充图表

![[assets/figures/papers/paper_list_l1706_Uni_HOI_A_Unified_Framework_for_Learning_the_Joint_Distribution_of_Text/figures/001_Figure_1.jpg]]
*Figure 1: Uni-HOI learns the joint distribution of text and human-object interaction, thus it can serve multiple HOI-related tasks including text-driven interaction generation, object-guided motion generation(optionally with text) and object motion prediction. T, H and O represent the text, human motion and object motion*

![[assets/figures/papers/paper_list_l1706_Uni_HOI_A_Unified_Framework_for_Learning_the_Joint_Distribution_of_Text/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our Uni-HOI framework. Based on different task specifications, Uni-HOI can serve a variety of HOI tasks, including text-driven HOI generation (U(H,O|T)), human motion generation guided by object motion(optionally with text)(U(H|O[,T])) and object motion prediction guided by human motion(U(O|H))*



### 3.1 运动表示与问题形式化

Uni-HOI 将人体运动与物体运动统一表示为时序序列。人体运动采用 SMPL-H 参数化，每帧包含 $D_h = 159$ 维姿态参数；物体运动由平移与旋转变换组成，每帧 $D_o = 6$ 维。给定长度为 $L$ 的序列，人体运动与物体运动分别记为：

$$H = \{ h_i \} \in \mathbb{R}^{L \times D_h}, \quad O = \{ o_i \} \in \mathbb{R}^{L \times D_o}$$

文本描述 $T$ 与上述两种运动模态共同构成 Uni-HOI 的三模态空间 $Q = \{T, H, O\}$。

### 3.2 运动分词器（VQ-VAE）

为将异构运动数据转化为 LLM 可处理的离散 token，Uni-HOI 预训练了两个运动专用的 VQ-VAE，分别作为人体运动分词器 $V_h$ 和物体运动分词器 $V_o$。每个 VQ-VAE 由编码器、离散码本和解码器组成：编码器将运动序列映射为隐向量 $\hat{\mathbf{z}}_i$，随后通过最近邻查找量化到码本 $\mathcal{Z}$ 中：

$$\mathbf{z}_i = Q(\hat{\mathbf{z}}_i) := \arg\min_{\mathbf{z}_k \in \mathcal{Z}} \|\hat{\mathbf{z}}_i - \mathbf{z}_k\|_2$$

解码器从量化后的隐向量重建原始运动序列。VQ-VAE 的训练总损失由四项构成：

$$\mathcal{L}_V = \mathcal{L}_r + \mathcal{L}_e + \mathcal{L}_c + \mathcal{L}_v$$

其中 $\mathcal{L}_r$ 为重建损失，$\mathcal{L}_e$ 为嵌入损失，$\mathcal{L}_c$ 为承诺损失，$\mathcal{L}_v$ 为速度正则化项，用于约束相邻帧运动变化的光滑性。两个 VQ-VAE 的码本大小均设为 $K \in \mathbb{R}^{512 \times 4096}$，即 4096 个 512 维码向量。

### 3.3 统一自回归框架

**统一词表构建。** 将文本 token 词表 $V_t$、人体运动 token 词表 $V_h$ 和物体运动 token 词表 $V_o$ 合并为统一词表 $V = \{V_t, V_h, V_o\}$。此外，为注入物体几何先验，Uni-HOI 设计了一个 MLP 网络从输入物体点云（340 点）中提取特征，作为特殊的 `<object geometry token>` 插入输入序列。

**任务空间定义。** 从三模态集合 $Q = \{T, H, O\}$ 中选取非空真子集作为条件 $X$，剩余模态作为目标 $y$，覆盖所有可行的 HOI 任务：

$$\mathcal{T} = \{ (X, y) \mid X \subset Q,\; y = Q \setminus X,\; X \notin \{\emptyset, Q\} \}$$

**自回归建模。** 以 Qwen3-8B 为骨干 Transformer 解码器，在给定源序列 $\mathbf{X}_s$ 的条件下，目标序列 $\mathbf{X}_t$ 的条件概率按时间步自回归分解：

$$p_\theta(\mathbf{X}_t \mid \mathbf{X}_s) = \prod_{i=0}^{L-1} p_\theta(x_{t_i} \mid x_t^{<i}, \mathbf{X}_s)$$

训练时最大化目标 token 的对数似然：

$$\mathcal{L}_{\mathrm{LM}} = - \sum_{i=0}^{L-1} \log p_\theta(x_{t_i} \mid x_t^{<i}, \mathbf{X}_s)$$

统一训练目标在所有模态划分上最小化期望损失：

$$\theta^* = \arg\min_\theta \sum_{(X, y) \in \mathcal{T}} \mathbb{E}_{(P, T, H, O) \sim \mathcal{D}} \left[ \ell( \mathcal{Y}, U_\theta(P, X) ) \right]$$

其中 $P$ 代表物体点云几何信息，$U_\theta$ 为 Uni-HOI 模型。

### 3.4 两阶段训练策略

**第一阶段：多任务预训练。** 在大规模 HOI 数据集上，随机采样不同的 $(X, y)$ 模态划分进行多任务学习，使模型初步捕获三模态间的联合分布。

**第二阶段：任务特定微调。** 在具体子任务（如文本驱动 HOI 生成 $U(H,O|T)$、物体引导人体运动生成 $U(H|O[,T])$、人体驱动物体运动预测 $U(O|H)$）上使用 LoRA 进行适配微调。两阶段均采用 LoRA 算法，第二阶段采用更小的秩和缩放系数以保留预训练知识。第一阶段共 110K 次迭代，第二阶段 50K 次迭代，学习率 $1 \times 10^{-6}$，在 8 块 NVIDIA GeForce RTX 4090 GPU 上完成训练。



## 实验与关键发现

### 核心实验设计

Uni-HOI 的实验验证覆盖三类核心 HOI 任务：文本驱动 HOI 生成（text-to-HOI）、物体运动驱动人体运动生成（object-to-human，可选附文本）、以及人体运动驱动物体运动预测（human-to-object）。评测基准包括 **FullBodyManipulation**、**BEHAVE** 和 **GRAB** 三个公开数据集，指标涵盖分布质量（FID）、检索精度（R-precision）、关节误差（HandJPE、MPJPE）和接触精度（Cprec、Crec、Cacc、c%）等维度。

训练采用两阶段策略：第一阶段在最大规模 HOI 数据集上进行多任务预训练（110K 迭代），第二阶段针对各子任务进行 LoRA 微调（50K 迭代），其中第二阶段使用更小的秩和缩放系数。所有模型在 8 张 NVIDIA GeForce RTX 4090 GPU 上训练，学习率 1e-6，batch size 128。人体 VQ-VAE 和物体 VQ-VAE 的码本均设为 $\mathbf{K} \in \mathbb{R}^{512 \times 4096}$。

### 文本驱动 HOI 生成

Table 1 给出了在 FullBodyManipulation 和 BEHAVE 上的定量对比。Uni-HOI 在所有指标上均优于或匹配专门设计的文本驱动基线方法：

![[assets/figures/papers/paper_list_l1706_Uni_HOI_A_Unified_Framework_for_Learning_the_Joint_Distribution_of_Text/figures/003_Table_1.jpg]]
*Table 1: Quantitative experimental results for the task of text-driven HOI generation on FullBodyManipulation and BEHAVE dataset. → means results closer to the real distribution are better*

- **FullBodyManipulation**：FID 达到 5.13，优于 **ROG**（Xue et al., CVPR 2025）的 5.35 和 **HOI-Diff**（Peng et al., CVPR 2025）的 11.25；Top-1 R-precision 为 0.45，高于 ROG 的 0.42；接触精度 Cacc 为 8.07，显著优于 HOI-Diff 的 10.05。这表明 Uni-HOI 生成的交互在分布匹配、文本-运动对齐和接触合理性上均具优势。
- **BEHAVE**：FID 为 0.37，低于 ROG 的 0.42；c% 为 0.37，同样优于 ROG 的 0.42。Uni-HOI 在此数据集上的优势幅度较小，可能与 BEHAVE 的交互复杂度更高有关。

定性可视化（Figure 3）进一步揭示：ROG 和 HOI-Diff 在某些交互中产生不合理的接触（图中红色圈出），而 Uni-HOI 生成的交互在肢体-物体空间关系上更自然。

![[assets/figures/papers/paper_list_l1706_Uni_HOI_A_Unified_Framework_for_Learning_the_Joint_Distribution_of_Text/figures/004_Figure_3.jpg]]
*Figure 3: Visualization of comparative results for the task of text-driven HOI generation on the FullBodyManipulation and BEHAVE datasets. Irrational interactions are circled in red*

### 物体运动驱动人体运动生成

Table 2 展示了在 FullBodyManipulation 上的结果。在仅给定物体运动（w/o text）条件下，Uni-HOI 取得 HandJPE 29.87、MPJPE 17.63、Cacc 0.84、c% 0.70；当附加文本条件（w/ text）时，性能进一步提升至 HandJPE 27.56、MPJPE 16.82、Cacc 0.83、c% 0.71。这一结果表明文本信息为人体运动生成提供了有效的语义约束，尤其在降低手部关节误差上作用明显。

![[assets/figures/papers/paper_list_l1706_Uni_HOI_A_Unified_Framework_for_Learning_the_Joint_Distribution_of_Text/figures/005_Table_2.jpg]]
*Table 2: Quantitative experimental results for the task of human motion generation guided by object motion(optionally with text) on the FullBodyManipulation dataset*

与基线 **OMOMO**（Li et al., TOG 2023）的对比显示，Uni-HOI 在接触精度和关节误差上均表现更优，验证了统一框架在多模态条件融合上的有效性。

### 人体运动驱动物体运动预测

Table 3 报告了在 GRAB 和 BEHAVE 上的物体运动预测结果。在 GRAB 上，Uni-HOI 的物体平移误差 Ec 为 0.024，显著优于 **ObjPOP**（Petrov et al., CVPR 2023）等基线方法（原文未提供精确值，但声称显著超越）。在 BEHAVE 上同样保持优势。

![[assets/figures/papers/paper_list_l1706_Uni_HOI_A_Unified_Framework_for_Learning_the_Joint_Distribution_of_Text/figures/007_Table_3.jpg]]
*Table 3: Quantitative comparison for human motion-driven object motion prediction on GRAB and BEHAVE datasets*

Figure 5 的定性对比显示，Uni-HOI 预测的物体姿态与人体动作在时序和空间上的一致性更高，尤其在抓取、放置等精细操作中表现更合理。Figure 6 进一步展示了 Uni-HOI 的 4D HOI 合成能力：给定参考视频中的人体运动，模型能预测出合理的物体运动轨迹，实现完整的交互序列生成。

![[assets/figures/papers/paper_list_l1706_Uni_HOI_A_Unified_Framework_for_Learning_the_Joint_Distribution_of_Text/figures/008_Figure_5.jpg]]
*Figure 5: Visualization of comparative results for human motion-driven object motion prediction on the BEHAVE and GRAB datasets*

![[assets/figures/papers/paper_list_l1706_Uni_HOI_A_Unified_Framework_for_Learning_the_Joint_Distribution_of_Text/figures/009_Figure_6.jpg]]
*Figure 6: 4D HOI synthesis. Uni-HOI can predict reasonable object motion for human in the reference videos*

### 消融实验

消融研究揭示了两个关键设计选择的影响：

1. **LLM 骨干规模**：对比 Qwen3-1B、Qwen3-4B 和 Qwen3-8B 三种配置，更大的模型（8B）在所有任务上均取得更好性能，验证了大规模预训练语言模型对跨模态序列建模的增益。这一发现与 LLM 的缩放定律一致——更大的参数容量有助于捕获文本与双运动模态间的复杂依赖。

2. **第二阶段任务特定微调**：仅使用第一阶段多任务预训练的模型在各项指标上均低于经过第二阶段微调的版本。这表明通用多任务预训练虽然提供了良好的初始化，但针对特定条件-目标映射进行适配仍对性能有显著提升。LoRA 微调以较小的计算代价实现了这一适配。

### 失败模式与局限性

尽管 Uni-HOI 在多数任务上表现优异，仍存在以下限制：

- **固定模态组合**：当前框架仅探索了预定义的模态划分（如 $P(H,O|T)$、$P(H|O[,T])$、$P(O|H)$），尚未验证更灵活的联合条件生成能力，例如同时以人体运动和文本为条件预测物体姿态 $P(O|H,T)$，或从交互序列反向生成文本描述 $P(T|H,O)$。
- **接触建模缺失**：Uni-HOI 未显式引入手-物接触嵌入（如距离场、接触图），在需要精细接触判断的场景中可能出现穿透或悬空等物理不合理现象。Figure 3 中虽优于基线，但部分复杂交互仍存在接触偏差。
- **泛化边界未明**：对未见物体类别或超长时序交互的泛化能力尚未系统评估，这在实际部署中可能成为瓶颈。

### 实验结论

综合来看，Uni-HOI 通过将异构运动数据统一为离散 token 并借助 LLM 的自回归建模能力，在单一框架下实现了多种 HOI 任务的统一处理。其在文本驱动生成、物体引导生成和物体运动预测三个方向上的领先结果，验证了联合分布建模相较于任务特定架构的优越性。两阶段训练策略被证明是平衡通用性与任务精度的有效手段。然而，接触建模的缺失和模态组合的有限性为后续改进指明了方向。

### 补充图表

![[assets/figures/papers/paper_list_l1706_Uni_HOI_A_Unified_Framework_for_Learning_the_Joint_Distribution_of_Text/figures/006_Figure_4.jpg]]
*Figure 4: Visualization of comparative results for the task of human motion generation guided by object motion(optionally with text) on the FullBodyManipulation dataset*



## 定位与知识库关联

### 核心瓶颈与突破路径

现有HOI生成方法普遍采用任务特定架构，文本驱动HOI生成（如 **ROG** (Xue et al., CVPR 2025)、**HOI-Diff** (Peng et al., CVPR 2025)）、物体运动驱动人体运动生成（如 **OMOMO** (Li et al., TOG 2023)）和人体运动驱动物体姿态预测（如 **ObjPOP** (Petrov et al., CVPR 2023)）各自依赖独立的模型设计，无法以单一框架灵活处理多种条件输入组合。这一碎片化格局的根本瓶颈在于缺乏对文本、人体运动与物体运动三模态联合分布的统一建模能力。

Uni-HOI通过一个关键因果调节变量打破上述限制：将人体运动和物体运动视为两种“外语”，利用两个运动专用VQ-VAE将异构连续运动数据离散化为LLM兼容的token序列，并与文本token合并为统一词表。借助预训练LLM（Qwen3-8B）的自回归序列建模能力，模型能够捕获跨模态依赖，从而在单一框架下实现多种HOI任务的统一处理。配合两阶段训练策略（大规模多任务预训练+任务特定LoRA微调），模型可接受任意模态子集作为条件生成剩余模态。

### 方法谱系中的位置

在HOI生成方法谱系中，Uni-HOI代表从“任务特定架构”向“统一多模态自回归建模”的范式迁移：

- **相对于文本驱动HOI方法**：ROG和HOI-Diff均采用扩散模型架构，分别通过接触引导和交互先验实现文本到人体-物体运动的生成。Uni-HOI以自回归Transformer替代扩散过程，将文本token与运动token置于同一序列中进行端到端条件生成，在FullBodyManipulation上FID达到5.13（ROG为5.35，HOI-Diff为11.25），Top-1 R-precision达到0.45（ROG为0.42），验证了LLM骨干在跨模态对齐上的优势。

- **相对于物体运动驱动人体生成方法**：OMOMO采用分离式条件编码，将物体运动作为附加输入引导人体运动扩散。Uni-HOI则将物体运动token直接拼接至输入序列，通过LLM的自注意力机制隐式学习人体-物体运动耦合关系，在FullBodyManipulation的object-to-human任务上HandJPE达到27.56（附文本条件）。

- **相对于人体运动驱动物体预测方法**：ObjPOP专注于从人体运动预测物体姿态，采用专用网络架构。Uni-HOI在同一框架内完成该任务，在GRAB数据集上接触误差Ec达到0.024，显著优于ObjPOP。

- **相对于通用运动生成模型**：MDM*（Tevet et al., 2022）作为人体运动扩散模型的改编版本被纳入文本驱动HOI对比，但其缺乏对物体运动的显式建模，性能显著落后于Uni-HOI，印证了联合建模三模态的必要性。

### 适用边界与局限

Uni-HOI的统一架构虽在多项HOI任务上取得领先，但存在以下适用边界和已知局限：

1. **模态组合的探索不充分**：当前工作仅覆盖了固定模态组合（文本→人体+物体运动、物体运动→人体运动、人体运动→物体运动），尚未验证更复杂的条件组合能力，例如同时以人体运动和文本为条件预测物体姿态（P(O|H,T)），或从交互序列反向生成自然语言描述（P(T|H,O)）。这些任务的可行性取决于LLM是否能在训练中习得相应的条件依赖关系，目前缺乏实验证据。

2. **接触建模的隐式性**：Uni-HOI未显式建模人体与物体的接触嵌入（如距离场、接触图），而是依赖LLM从运动token序列中隐式学习交互约束。这可能导致接触精细度不足——在定性可视化中，基线方法常出现手部穿透物体等不合理交互（Figure 3中红色标注），Uni-HOI虽有改善但仍未完全消除。引入显式接触信息是否能进一步降低HandJPE并提升接触精确度，是待验证的开放问题。

3. **泛化边界未系统评估**：论文仅在FullBodyManipulation、BEHAVE和GRAB三个数据集上验证，对未见物体类别或长序列交互的泛化能力缺乏系统消融。物体几何信息通过MLP从点云提取为单个特殊token，该紧凑表示是否足以区分不同物体的交互语义，在更复杂场景下可能成为瓶颈。

4. **计算资源需求**：两阶段训练需在8张NVIDIA RTX 4090 GPU上完成（第一阶段110K迭代，第二阶段50K迭代），骨干为Qwen3-8B。消融实验表明使用更小的LLM骨干（Qwen3-4B、Qwen3-1B）会导致性能下降，说明统一框架的性能与LLM规模正相关，可能限制其在资源受限场景下的部署。

### 开放问题

1. **反向生成能力**：能否仅由给定的交互序列（人体运动+物体运动）自动生成自然语言描述（P(T|H,O)）？这需要验证LLM在运动token到文本token的跨模态翻译能力，目前尚无实验证据。

2. **多物体与长序列扩展**：将框架扩展至更复杂的多物体交互场景（如双手操作不同物体）或更长时序生成将面临token序列长度增长带来的自回归误差累积和注意力复杂度挑战。

3. **接触建模增强**：引入显式的手-物接触信息（如距离场、接触图）作为额外条件token，是否能提升接触精确度并降低关节误差，是值得探索的方向。

4. **数据规模效应**：当前多任务预训练依赖FullBodyManipulation数据集（论文称其为“largest collected HOI dataset”），更大规模的多模态HOI数据能否进一步释放LLM的跨模态对齐能力，尚待验证。



## 原文 PDF

![[paperPDFs/arxiv_2026/Uni_HOI_A_Unified_Framework_for_Learning_the_Joint_Distribution_of_Text_and_Human_Object_Interaction.pdf]]
