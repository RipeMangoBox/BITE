---
title: "CoMo: Controllable Motion Generation through Language Guided Pose Code Editing"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/CoMo_Controllable_Motion_Generation_through_Language_Guided_Pose_Code_Editing.pdf
aliases:
- CoMo
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 将运动分解为语义有意义、可解释的离散姿态代码（pose codes），使大语言模型（LLM）能够直接理解并编辑运动序列的时空属性。
primary_logic: 通过预定义的身体部位语义代码本（pose codebook）将运动时空分解为 K-hot 姿态代码，并利用 LLM 的常识推理能力，在无需微调的情况下实现零样本的细粒度运动编辑，同时支持自回归生成。
claims:
- CoMo 在 HumanML3D 和 KIT 数据集上的运动生成指标上排名前三，并在多样性（Diversity）指标上取得最佳成绩（9.936），验证了语义姿态代码表示的有效性。
- 在包含 54 名参与者的用户研究中，超过 70% 的标注者偏好 CoMo 的编辑结果，显著优于基于文本重生成的基线方法（T2M-GPT、FineMoGen）。
- LLM 能够通过调整姿态代码直接干预运动编辑，无需任何微调，实现零样本的细粒度控制。
- HumanML3D 上 Diversity ↑ = 9.936 ± 0.066
---

# CoMo: Controllable Motion Generation through Language Guided Pose Code Editing

> [!tip] 核心洞察
> 通过预定义的身体部位语义代码本（pose codebook）将运动时空分解为 K-hot 姿态代码，并利用 LLM 的常识推理能力，在无需微调的情况下实现零样本的细粒度运动编辑，同时支持自回归生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | CoMo：通过语言引导的姿态代码编辑实现可控运动生成 |
| 英文题名 | CoMo: Controllable Motion Generation through Language Guided Pose Code Editing |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2403.13900) · [Project](https://yh2371.github.io/como/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | CoMo |
| Dataset | HumanML3D, KIT-ML, Human Evaluation on Motion Editing |

> [!tip] 效果简介
> - HumanML3D 上，Diversity ↑ 9.936 ± 0.066 vs 9.761 ± 0.081 (T2M-GPT) (+0.175)。
> - KIT-ML 上，R-Precision Top-1 ↑ 0.422 ± 0.009 vs 0.432 ± 0.006 (FineMoGen) (-0.010)。
> - Human Evaluation on Motion Editing 上，Human Preference Rate >70% prefer CoMo vs <30% prefer baselines (T2M-GPT, FineMoGen) (显著更高)。

## 概述

现有文本到运动生成模型通常将运动编码为隐式潜在向量，虽然能够生成符合全局文本描述的运动序列，但缺乏对运动细节的细粒度控制能力。用户无法直观地修改特定身体部位的动作、在特定时刻插入新姿势或调整运动风格，因为这些隐式表示不具备可解释的编辑接口。这一瓶颈限制了运动生成在交互式内容创作中的应用。

CoMo 提出了一种新的解决路径：**将运动时空分解为语义可解释的离散姿态代码（pose codes）**。具体而言，CoMo 预定义一个基于启发式骨架解析器的语义姿态代码本，每个代码对应一个身体部位的基本运动学状态（如“左膝微曲”），从而将连续运动序列转化为 K-hot 姿态代码序列。这一表示使得大语言模型（LLM）能够直接“读懂”并“修改”运动——LLM 根据自然语言编辑指令，识别目标帧和身体部位对应的姿态代码，调整其激活值，再通过解码器重构出编辑后的运动，全程无需任何微调。

CoMo 的核心贡献在于构建了一个统一的文本驱动运动生成与编辑框架，包含三个模块：运动编解码器（Motion Encoder-Decoder）、运动生成器（Motion Generator）和运动编辑器（Motion Editor）。生成器采用自回归变换器，在文本描述和 LLM 生成的细粒度身体部位关键词的共同条件下预测姿态代码序列；编辑器则通过三步顺序提示策略，让 LLM 零样本地完成细粒度运动编辑。

在 HumanML3D 和 KIT 两个标准基准上，CoMo 的运动生成指标排名前三，其中**多样性（Diversity）指标达到 9.936，为所有对比方法中最高**。更重要的是，在一项包含 54 名参与者的用户研究中，**超过 70% 的标注者偏好 CoMo 的编辑结果**，显著优于基于文本重生成的基线方法（T2M-GPT、FineMoGen），验证了语义姿态代码表示在细粒度运动编辑中的有效性。

## 背景与动机

### 问题背景：文本到运动生成的细粒度控制困境

文本驱动的人体运动生成旨在根据自然语言描述合成逼真的三维人体动作序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。近年来，基于扩散模型和自回归变换器的方法在运动生成质量上取得了显著进展，但一个根本性瓶颈始终存在：**现有模型缺乏对生成运动的细粒度控制能力**。

具体而言，当用户希望修改动作中的细微姿态——例如“让角色挥手的幅度更大”或“在行走的特定时刻插入一个跳跃动作”——现有方法几乎无法胜任。这是因为主流方法将运动编码为隐式的潜在向量（如 VQ-VAE 的离散编码或扩散模型的连续潜在表示），这些表示虽然有利于重建和生成，却**不可解释**，无法提供可供用户或系统直接操作的编辑界面。

### 现有方法的缺口

当前文本到运动编辑的典型做法是“重生成”范式：用户修改文本提示，系统根据新提示重新生成整个运动序列。以 FineMoGen 为代表的方法即采用此策略。这种方式存在三个核心缺陷：

1. **丧失源运动特征**：重生成会丢弃原始运动的大部分细节（如风格、节奏、非目标身体部位的动作），导致编辑结果与源运动产生不必要的偏离。
2. **缺乏精确时空控制**：文本提示本质上是全局描述，难以精确指定“第 30 帧到第 50 帧的左臂”这一级别的修改。
3. **不可迭代编辑**：每次编辑都是独立的生成过程，无法在保持前次编辑结果的基础上进行增量修改。

### 核心动机：可解释的运动表示作为编辑接口

CoMo 的核心动机源于一个关键洞察：**如果运动能够被分解为语义有意义、可解释的离散单元，那么不仅人类可以理解这些单元，大语言模型（LLM）也可以直接“阅读”和“编辑”它们**。

这一思路将运动编辑问题转化为序列编辑问题：将运动表示为一串“姿态代码”（pose codes），每个代码对应一个身体部位在某一时刻的运动学状态（如“左膝微弯”、“右臂前伸”）。LLM 凭借其强大的常识推理和指令遵循能力，可以在零样本条件下理解编辑指令，定位需要修改的代码，并输出编辑后的代码序列——整个过程无需对 LLM 进行任何微调。

### 技术挑战

实现上述愿景需要解决两个关键挑战：

- **如何定义语义姿态代码？** 代码必须既具有足够的表达能力以覆盖多样的人体姿态，又保持语义的可解释性，使 LLM 能够理解每个代码的含义。这需要设计一个预定义的姿态代码本（pose codebook），而非依赖从数据中学习的隐式代码本。
- **如何让 LLM 可靠地编辑代码序列？** LLM 需要理解运动序列的时空结构，准确识别编辑目标，并在修改局部代码时保持序列的全局一致性。这要求精心设计提示策略和代码表示格式。

CoMo 通过三个协同组件——运动编解码器（Motion Encoder-Decoder）、运动生成器（Motion Generator）和运动编辑器（Motion Editor）——系统性地回应了这些挑战，构建了首个统一的文本驱动运动生成与细粒度编辑框架。

## 核心创新

CoMo 的核心创新在于将运动生成与编辑问题重新定义为**可解释的语义姿态代码（pose codes）操作问题**，从而弥合了隐式潜在表示与细粒度可控性之间的鸿沟。其关键突破可归纳为以下三个层面的设计转变：

### 1. 从隐式编码到语义姿态代码的表示层创新

现有文本到运动模型（如 T2M-GPT、MotionGPT、FineMoGen）普遍采用 VQ-VAE 学习的隐式代码本，这些代码本虽然压缩效率高，但缺乏可解释性，无法为编辑提供明确的语义抓手。CoMo 的核心改变在于**预定义了一个基于启发式骨架解析器的语义姿态代码本**（Section 3.1），将运动在时空维度上分解为离散的、语义有意义的 K-hot 姿态代码。

具体而言，CoMo 借鉴 PoseScript 的姿态描述逻辑，为人体 10 个部位（如“左膝微曲”“右臂前伸”）分别构建代码本条目，通过关节角度和距离的阈值条件将连续运动帧映射为可读的代码序列。这一表示将运动编辑从“在隐空间中搜索”转变为“直接修改代码”，使 LLM 能够像理解自然语言一样理解运动的结构化语义。

### 2. 从重生成到零样本代码编辑的交互范式创新

传统运动编辑方法（如 FineMoGen）依赖于修改文本提示后**重新生成整个运动序列**，这种方式不仅计算开销大，还容易丢失源运动的细节特征。CoMo 提出了**基于 LLM 的零样本姿态代码编辑范式**（Section 3.3），无需任何微调即可实现细粒度编辑。

编辑流程采用三步顺序提示策略：首先将源运动编码为姿态代码序列并作为上下文提供给 LLM，然后由 LLM 根据编辑指令识别需要修改的目标代码段，最后将编辑后的代码段与未修改部分拼接，通过解码器重建运动。这一设计使得用户可以对特定身体部位、特定时间段的运动进行精确干预（如“在第 2 秒到第 4 秒抬高右手”），同时保持源运动的整体特征不变。

### 3. 从全局文本到细粒度身体部位条件的信息增强

现有方法通常仅使用全局文本描述作为生成条件，缺乏对身体部位级别的细粒度约束。CoMo 引入了**LLM 生成的细粒度关键词增强机制**（Section 3.2）：利用 GPT-4 为每个身体部位生成一个描述性关键词（如“弯曲的左膝”“放松的肩膀”）以及一个整体情绪关键词，并通过 CLIP 嵌入将这些关键词注入自回归运动生成器。

消融实验（Table 3）验证了这一设计的有效性：在 HumanML3D 数据集上，去除细粒度关键词后 Top-1 精度从 0.502 降至 0.487，表明身体部位级别的语义对齐对提升文本-运动一致性具有显著贡献。

### 创新总结

| 改变维度 | 基线方案 | CoMo 方案 | 创新性质 |
|---------|---------|----------|---------|
| 运动表示 | 隐式 VQ 编码（T2M-GPT, MotionGPT） | 语义姿态代码（基于启发式解析器） | 表示层范式转换 |
| 编辑机制 | 修改文本后重生成（FineMoGen） | LLM 零样本直接操作代码 | 交互范式创新 |
| 条件粒度 | 全局文本描述 | 身体部位级关键词 + CLIP 嵌入 | 信息增强 |
| 代码本来源 | 端到端学习（T2M-GPT） | 预定义语义代码本（PoseScript 启发） | 知识注入方式改变 |

这些创新共同构成了 CoMo 的核心竞争力：**以语义姿态代码为桥梁，将 LLM 的常识推理能力引入运动生成与编辑，在保持生成质量的同时实现了前所未有的细粒度可控性**。用户研究（54 名参与者，超过 70% 偏好 CoMo 编辑结果）和自动指标（HumanML3D 上 Diversity 9.936 为所有方法最佳）均支撑了这一设计理念的有效性。

## 整体框架

CoMo 是一个面向文本驱动人体运动生成与细粒度编辑的统一框架，其核心设计理念在于：**将运动分解为语义有意义、可解释的离散姿态代码（pose codes），使大语言模型（LLM）能够直接理解并编辑运动序列的时空属性**。如图 2 和图 3 所示，整个 pipeline 由三个关键模块串联构成：

1. **Motion Encoder‑Decoder（运动编解码器）**：负责运动表示与重构的闭环。编码端利用预定义的语义姿态代码本（pose codebook），将原始运动序列 $X$ 通过骨架解析器 $\mathcal{P}$ 编码为 $K$-hot 姿态代码序列 $Z$；解码端则从激活的代码本项求和得到潜在特征 $\hat{Z}$，经一维卷积解码器重构回运动 $X_{\mathrm{rec}}$。该模块是整个框架的**表示基础**——它将连续的运动信号量化为离散、可解释的符号空间，为后续生成与编辑提供结构化接口。

2. **Motion Generator（运动生成器）**：一个仅解码器的自回归变换器，负责从文本描述生成姿态代码序列。其输入不仅包含全局文本描述，还引入了由 GPT‑4 为 10 个身体部位及整体情绪生成的细粒度关键词，结合 CLIP 嵌入作为条件信号。生成器按帧自回归预测 $K$-hot 姿态代码，生成的代码序列再送入已训练好的解码器还原为 3D 运动。该模块实现了**从文本到运动的可控生成**，细粒度关键词的引入显著增强了文本‑运动的一致性。

3. **Motion Editor（运动编辑器）**：基于 LLM 的零样本编辑模块，无需任何微调。给定源运动及其编码后的姿态代码序列，以及用户的编辑指令，LLM 通过三步顺序提示策略（理解指令 → 定位目标代码 → 修改代码）直接操作姿态代码，编辑后的代码序列经解码器还原为最终运动。该模块使 CoMo 区别于仅通过修改文本提示重新生成运动的基线方法（如 **T2M‑GPT** 和 **FineMoGen**），实现了**对源运动序列的直接解释与操控**。

三个模块之间的数据流关系清晰：Motion Encoder‑Decoder 提供了运动 ↔ 姿态代码的双向映射能力，Motion Generator 和 Motion Editor 均依赖这一映射——前者从文本生成代码再解码为运动，后者将运动编码为代码、经 LLM 编辑后再解码。这种设计使生成与编辑共享同一表示空间，保证了框架的统一性与可扩展性。

## 核心模块与公式推导

CoMo 的核心架构由三个模块构成：运动编解码器（Motion Encoder-Decoder）、运动生成器（Motion Generator）和运动编辑器（Motion Editor）。其设计的关键在于将运动分解为语义可解释的离散姿态代码，使后续的生成与编辑均可直接操作这些代码。

### 运动编解码器

运动编解码器负责在原始运动序列与姿态代码序列之间建立双向映射。其核心是一个预定义的语义姿态代码本（pose codebook），遵循 **PoseScript** 的构建方式，包含 $N$ 个代码，每个代码封装了特定身体部位的语义信息（如“左膝微曲”）。

**编码过程**：给定运动序列 $X$，编码器 $\mathcal{E}$ 通过骨架解析器 $\mathcal{P}$ 将每个下采样帧 $x_{i \times l}$ 映射为 $K$-hot 姿态代码向量：

$$Z = \mathcal{E}(X) = \left\{ \left\{ \mathcal{P}(c_n, x_{i \times l}) \right\}_{n=1}^{N} \right\}_{i=1}^{L}$$

其中 $L$ 为下采样后的序列长度，$l$ 为下采样率，$\mathcal{P}(c_n, x)$ 返回代码 $c_n$ 对帧 $x$ 的激活概率。这意味着每一帧由多个语义代码的联合激活来表示，实现了运动在时间和空间上的可解释分解。

**量化与解码**：为得到解码器可用的潜在特征，将激活的代码本项进行加权求和：

$$\hat{Z} = \left\{ \sum_{n=1}^{N} \mathcal{P}(c_n, x_{i \times l}) \cdot c_n \right\}_{i=1}^{L}$$

解码器采用一维卷积架构，从 $\hat{Z}$ 重构运动序列 $X_{\text{rec}}$。重构损失结合了位置和速度的平滑 L1 损失：

$$\mathcal{L}_{\mathrm{rec}} = \mathcal{L}_1(X, X_{\mathrm{rec}}) + \lambda \cdot \mathcal{L}_1(V(X), V(X_{\mathrm{rec}}))$$

其中 $V(\cdot)$ 为速度计算函数，$\lambda$ 为平衡权重。速度损失项的引入有助于保持运动的时间连续性。

### 运动生成器

运动生成器是一个仅解码器的自回归变换器，根据文本描述预测姿态代码序列。为增强文本与运动的绑定，CoMo 使用 GPT-4 为 10 个身体部位各生成一个细粒度关键词，并额外生成一个描述整体情绪的关键词，将这些关键词的 CLIP 嵌入与原始文本嵌入拼接作为条件。

给定文本条件 $t$，姿态代码序列的似然函数为：

$$P(Z | t) = \prod_{i=1}^{L} \prod_{n=1}^{N+1} p( z_i^n | t, z_{1:i-1}^{1:N+1})$$

其中 $z_i^n$ 为第 $i$ 帧第 $n$ 个代码的激活状态，$N+1$ 包含一个特殊的结束标记。由于每帧的姿态代码为多标签预测，训练采用二元交叉熵损失：

$$\mathcal{L}_{\mathrm{gen}} = -\frac{1}{L(N+1)} \sum_{i=1}^{L} \sum_{n=1}^{N+1} \mathbb{E}_{z_i^n \sim Ber(z_i^n)} [\log p( z_i^n | t, z_{1:i-1}^{1:N+1})]$$

### 运动编辑器

运动编辑器利用大语言模型（LLM）的常识推理能力，通过三步顺序提示策略实现零样本运动编辑：首先将源运动编码为姿态代码序列并转为文本表示；然后 LLM 根据编辑指令识别需修改的目标代码并更新；最后将编辑后的代码序列通过预训练的解码器重构为运动。整个过程无需对 LLM 进行任何微调。

### 补充图表

![[assets/figures/papers/motion_editing_inpainting_20260603_como/figures/001_Figure_1.jpg]]
*Figure 1: CoMo, a language-guided human motion synthesis model, enables controllable generation from text inputs. CoMo allows for the control of individual body part movements, facilitates fine-grained editing of each joint and frame, and supports iterative editing that preserves the essence of the original motions*

![[assets/figures/papers/motion_editing_inpainting_20260603_como/figures/002_Figure_2.jpg]]
*Figure 2: Overview of CoMo for text-driven motion generation. Motion Encoder-Decoder (left) utilizes a predefined codebook to encode motions into pose codes and learns a decoder to reconstruct the motions. Motion Generator (right), a transformer-based model, predicts pose codes autoregressively, conditioned on the text descriptions and LLM-generated fine-grained keywords. The generated pose codes are then decoded back into motions using the previously trained decoder*

## 实验与分析

### 文本驱动运动生成主结果

CoMo 在 HumanML3D 和 KIT-ML 两个标准基准上进行了文本驱动运动生成的系统评估。**Table 1** 报告了 HumanML3D 测试集上的五指标对比，CoMo 在所有指标上均达到最佳或次佳水平。其中，多样性（Diversity）得分 9.936 ± 0.066，超过此前最优的 **T2M-GPT**（9.761 ± 0.081），验证了语义姿态代码表示在覆盖运动分布宽度上的优势。R-Precision Top-1 达到 0.502 ± 0.003，FID 降至 0.262 ± 0.006，MM-DIST 为 3.032 ± 0.008，表明生成运动与文本描述之间建立了更强的语义绑定。

![[assets/figures/papers/motion_editing_inpainting_20260603_como/figures/004_Table_1.jpg]]
*Table 1: Comparison with the state-of-the-art methods on the HumanML3D test set. The best performance is bold, and the second best is underlined*

值得注意的是，CoMo 的 MModality 得分（1.013）相对较低——这意味着对于同一文本提示，模型生成的多个运动样本之间变化较小。这一现象与方法的核心理念一致：语义姿态代码对文本-运动对应关系施加了强约束，从而牺牲了一定的生成多样性。这与 **MDM**（2.799）等扩散模型形成鲜明对比，后者在多样性上表现更好但文本一致性较弱。

**Table 2** 的 KIT-ML 测试集结果进一步印证了这一趋势。CoMo 在六个指标中排名前三，其中 R-Precision Top-1 为 0.422 ± 0.009，略低于 **FineMoGen** 的 0.432 ± 0.006，但 FID（0.322）和 Diversity（10.356）均保持竞争力。KIT 数据集规模较小、动作类型相对集中，CoMo 在此场景下仍能维持稳定的生成质量。

**Figure 4** 的定性对比揭示了 CoMo 相对于 **T2M-GPT** 和 **FineMoGen** 的关键优势：红色框标注的文本-运动不对齐区域在 CoMo 中显著减少，尤其在涉及特定身体部位动作（如“抬起左臂”“弯腰”）的描述上，CoMo 的生成结果更准确地匹配了文本语义。

### 细粒度运动编辑评估

运动编辑是 CoMo 的核心贡献场景。论文设计了包含 54 名参与者的用户研究，评估四种编辑类型：身体部位修改、速度变化、风格/情感变化、动作添加/删除。**Figure 5** 展示了人工偏好评分结果：在所有五种编辑类型（含平均）上，超过 70% 的标注者偏好 CoMo 的编辑结果，显著优于基于文本重生成的基线方法 **T2M-GPT** 和 **FineMoGen**。

![[assets/figures/papers/motion_editing_inpainting_20260603_como/figures/007_Figure_5.jpg]]
*Figure 5: Human preference on Motion Editing by comparing CoMo with T2M-GPT and FineMoGen. We report the scores on five editing types and average results*

这一优势的根源在于编辑机制的本质差异。**T2M-GPT** 和 **FineMoGen** 通过修改文本提示后重新生成整个运动序列来实现“编辑”，这导致源运动的关键特征（如未编辑肢体的姿态、运动节奏）难以保留。而 CoMo 通过 LLM 直接定位并修改目标帧的姿态代码，仅改变编辑指令指定的部分，其余帧保持不变。**Figure 6** 的定性示例佐证了这一点：绿色标注的成功编辑区域与红色标注的未对齐区域形成对比，CoMo 在准确执行编辑指令的同时，最大程度地保留了源运动的本质特征。

![[assets/figures/papers/motion_editing_inpainting_20260603_como/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative examples of Motion Editing on the HumanML3D test set. The green words/boxes highlight successful edits. The red words/boxes identify misalignments between edited and source motions. Compared to other methods, CoMo achieves accurate edits while preserving key characteristics of the source motion*

需要指出的是，用户研究的 Fleiss' kappa 一致性系数为 0.4，属于中等水平，表明标注者对编辑质量的判断存在一定主观差异。此外，参与者均为研究生群体，可能存在人群偏差，结果的泛化性需进一步验证。

### 消融实验

#### 细粒度关键词的作用

**Table 3** 报告了 LLM 生成的身体部位关键词消融结果。去除 GPT-4 生成的细粒度关键词后（−Fine），HumanML3D 上的 R-Precision Top-1 从 0.502 降至 0.487，FID 从 0.262 升至 0.320，KIT 上同样观察到一致的性能退化。这表明，将全局文本描述分解为 10 个身体部位关键词和 1 个整体情绪关键词，有效增强了运动生成器对局部动作语义的建模能力。CLIP 嵌入的引入进一步强化了关键词与视觉运动模式的关联。

#### 代码本尺寸选择

姿态代码本的大小 N 直接决定了运动分解的语义粒度。**Table 4** 在 HumanML3D 验证集上对比了不同 N 值下的重构性能。N=392 在 Top-1 精度（0.517）和 FID（0.034）上取得最佳平衡。过小的代码本（如 N=196）导致语义表达能力不足，重构质量下降；过大的代码本（如 N=588）则引入冗余代码，增加模型复杂度而未带来显著性能提升。论文指出，角度/距离阈值的数量决定了关节位置解析的粒度，392 个代码对应 70 个姿态代码类别（参见附录 Table A6）的合理展开。

![[assets/figures/papers/motion_editing_inpainting_20260603_como/figures/010_Table_4.jpg]]
*Table 4: Ablation study of different codebook sizes N. We report the reconstruction performance on the HumanML3D validation set. The number of angle/distance cutoffs stands for the granularity of parsing the joint position*

#### 下采样率的影响

**Table 5** 考察了时序下采样率 l 对重构性能的影响。l=4 在模型复杂度和性能之间取得良好折衷，验证集上重构 Top-1 为 0.508。更小的下采样率（l=2）保留了更多时序细节但显著增加了序列长度和计算开销；更大的下采样率（l=8）则丢失了关键的运动动态信息，导致重构精度下降。

### 失败模式与局限性

尽管 CoMo 在细粒度编辑上表现突出，但分析揭示了若干系统性失败模式：

1. **全局属性编辑受限**：姿态代码主要描述局部运动学属性（如关节角度、相对位置），对情绪、速度等全局属性的编辑效果有限。LLM 难以准确将“让动作更悲伤”或“加快一倍速度”等全局指令映射为具体的局部代码修改。附录失败案例 C14 展示了此类编辑的典型失效场景。

2. **快速复杂运动的帧范围估计偏差**：对于快速、复杂的运动序列，LLM 在编辑提示的第二步（帧范围识别）中倾向于选择过宽的时间窗口，导致非目标帧被误修改，编辑精度下降。论文建议用户在此类场景下手动指定编辑帧范围以改善效果。

3. **生成多样性与一致性的权衡**：如前所述，CoMo 的 MModality 得分偏低，反映了语义姿态代码强绑定策略的内在代价——模型在追求文本-运动精确对齐时，牺牲了对同一文本描述的多样化诠释能力。

### 推理效率

附录 Table A9 报告了在 NVIDIA RTX A6000 GPU 上的推理时间对比。CoMo 的每句平均推理时间处于可接受范围，具体数值需查阅原表确认（此处证据仅提及该表存在，未提供具体数据）。自回归生成范式使得推理时间与生成序列长度线性相关，下采样率 l=4 的设计在一定程度上缓解了长序列生成的效率压力。

### 补充图表

![[assets/figures/papers/motion_editing_inpainting_20260603_como/figures/017_Figure.jpg]]
*Figure: Fig. A9: Prompt template for identifying the frames for editing. Fig. A10: Prompt template for identifying the body parts/joints for editing (above) and the prompt for executing the edits (below)*

![[assets/figures/papers/motion_editing_inpainting_20260603_como/figures/023_Figure.jpg]]
*Figure: Fig. C14: Failure cases in motion editing. Left: The edited motion does not depict the target emotion adequately. Right: The edited motion mistakenly added the ’sidestep’ near the start of the motion rather than in between the two exercises*

![[assets/figures/papers/motion_editing_inpainting_20260603_como/figures/005_Table_2.jpg]]
*Table 2: Comparison with the state-of-the-art methods on the KIT test set. The best performance is bold, and the second best is underlined, the third best is italic*

![[assets/figures/papers/motion_editing_inpainting_20260603_como/figures/009_Table_3.jpg]]
*Table 3: Ablation study of LLM-generated fine-grained keywords on HumanML3D and KIT. −Fine stands for the model without augmented keywords*

![[assets/figures/papers/motion_editing_inpainting_20260603_como/figures/011_Table_5.jpg]]
*Table 5: Ablation study of different sampling rates l. We report the reconstruction performance on the HumanML3D validation set*

![[assets/figures/papers/motion_editing_inpainting_20260603_como/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative examples of Motion Generation on the HumanML3D test set. The motion sequences progress from left to right. The red boxes identify misalignments between the generated motion sequence and the text description. CoMo achieves competitive results in motion generation compared to T2M-GPT and FineMoGen. More visual results are available in the Appendix*

## 方法谱系与知识库定位

### 一、问题定位：从隐式生成到可解释编辑

现有文本到运动（Text-to-Motion）模型的核心瓶颈在于**缺乏细粒度的可控性**：无论是基于 VQ-VAE 的 **T2M-GPT**、基于扩散模型的 **MDM** 与 **MotionDiffuse**，还是基于潜在扩散的 **MLD**，均将运动压缩为隐式潜在编码。这些编码虽然能支撑高质量的全局生成，却无法提供可解释的编辑界面——用户无法指定“左膝微屈”或“在第 30 帧加快挥手速度”这类时空细粒度修改。**FineMoGen** 虽尝试通过修改文本提示并重生成来实现编辑，但本质上仍是“重新生成”而非“直接编辑”，难以保留源运动的无关特征。

CoMo 的方法论转向在于：**将运动表示从隐式连续编码切换为显式、离散、语义可解释的姿态代码（pose codes）**。这一转向使得大语言模型（LLM）能够直接理解并操纵运动序列的时空属性，从而将运动编辑从“文本重生成”范式推进到“代码直接编辑”范式。

### 二、核心技术路径：语义姿态代码本与 LLM 编辑

CoMo 的技术架构由三个模块构成，每个模块对应一个关键设计选择：

1. **运动编解码器（Motion Encoder-Decoder）**：通过预定义的启发式骨架解析器，将每帧运动分解为 $K$-hot 姿态代码。代码本的设计借鉴了 **PoseScript** 的语义姿态描述思路，但将其系统化为基于关节角度和距离阈值的离散代码集合。这与 **T2M-GPT** 和 **MotionGPT** 等通过自编码器学习代码本的方式形成根本差异——CoMo 的代码本是**人工预定义且语义可读的**（如“left knee slightly bent”），而非隐式学习得到的不可解释向量。

2. **运动生成器（Motion Generator）**：采用仅解码器的自回归 Transformer，以文本描述和 GPT-4 生成的细粒度身体部位关键词为条件，逐帧预测姿态代码序列。该设计在形式上与 **T2M-GPT** 的自回归生成框架相似，但关键区别在于预测目标是语义姿态代码而非 VQ 码本索引，且条件信号引入了 CLIP 嵌入增强的细粒度部位描述。

3. **运动编辑器（Motion Editor）**：这是 CoMo 最具区分度的模块。通过三步顺序提示策略（识别目标帧→定位目标代码→修改代码值），LLM 能够在**零样本、无微调**的条件下直接编辑运动。这与 **FineMoGen** 的“修改文本→重生成”策略形成鲜明对比：CoMo 编辑的是源运动的代码表示，因此能最大程度保留未编辑部分的运动特征。

### 三、在文本到运动领域中的位置

从方法谱系看，CoMo 处于以下几条技术路线的交汇处：

| 维度 | 基线方法 | CoMo 的差异 |
|------|----------|-------------|
| 运动表示 | **T2M-GPT**（VQ 隐式编码）、**MotionGPT**（统一 token 化） | 语义预定义姿态代码，可解释且可被 LLM 直接操作 |
| 生成范式 | **MDM**（扩散）、**T2M-GPT**（自回归） | 自回归生成，但预测目标为语义代码 |
| 编辑机制 | **FineMoGen**（文本重生成） | LLM 零样本直接编辑姿态代码 |
| 条件信息 | 全局文本描述 | 全局文本 + GPT-4 生成的逐部位关键词 + CLIP 嵌入 |

在 HumanML3D 和 KIT 数据集上，CoMo 的运动生成指标排名前三，且在多样性（Diversity = 9.936）上达到最优，验证了语义姿态代码表示的有效性。然而，其 MModality 得分相对较低（1.013），表明强文本-运动绑定牺牲了一定的生成多样性——这是显式语义表示带来的固有权衡。

### 四、适用边界与局限

CoMo 的能力边界受限于其姿态代码的**局部运动学属性**：

- **全局编辑能力不足**：姿态代码主要描述关节角度和部位位置等局部运动学特征，对情绪、速度、风格等全局属性的编辑效果有限。LLM 可能无法准确将“让动作更悲伤”这类全局指令映射为具体的局部代码修改（附录失败案例 C14 提供了相关证据）。

- **快速复杂运动的编辑精度下降**：对于快速、复杂的运动序列，LLM 倾向于选择过宽的帧范围进行编辑，导致精度损失。用户可能需要手动指定编辑帧来弥补这一不足。

- **LLM 依赖**：零样本编辑的质量高度依赖 LLM 的常识推理能力。在更长、更复杂的编辑指令下，模型的可靠性和自一致性尚未得到充分验证。

- **用户研究局限**：54 名参与者的用户研究中，Fleiss' kappa 一致性系数为 0.4（中等一致性），且参与者仅限于研究生群体，可能存在人群偏差。

### 五、开放问题

1. **全局属性的语义化**：如何将运动速度、风格、轨迹等全局描述符有效融入姿态代码框架？可能的路径包括引入额外的全局代码标记或分层代码结构。

2. **物理合理性约束**：能否引入物理先验（如动力学约束、接触一致性）来引导 LLM 推理，确保编辑后的运动在物理上合理且平滑？这对于避免生成违反物理规律的运动至关重要。

3. **时序细粒度控制**：当前姿态代码主要描述空间姿态，如何扩展表示以支持更细粒度的时序调控（如动作重复次数、节奏变化、过渡时长）？

4. **LLM 推理的可靠性**：在更长、更复杂的编辑指令链下，LLM 的多步推理是否保持自一致性？是否需要引入验证或自纠正机制？

5. **与物理仿真引擎的集成**：编辑后的运动能否与物理仿真环境对接，实现更真实的交互式运动编辑？

## 原文 PDF

![[paperPDFs/ECCV_2024/CoMo_Controllable_Motion_Generation_through_Language_Guided_Pose_Code_Editing.pdf]]
