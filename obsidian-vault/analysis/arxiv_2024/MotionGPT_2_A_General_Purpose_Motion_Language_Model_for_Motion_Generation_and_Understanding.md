---
title: "MotionGPT-2: A General-Purpose Motion-Language Model for Motion Generation and Understanding"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/MotionGPT_2_A_General_Purpose_Motion_Language_Model_for_Motion_Generation_and_Understanding.pdf
aliases:
- M2
- MotionGPT-2
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过将连续人体运动量化为离散token，并扩展LLM词汇表以统一运动与语言表示，利用LoRA高效微调，使LLM能够以自回归方式处理多模态控制信号并解决多种运动相关任务。
primary_logic: 将运动和文本统一在LLM的离散token空间中，能够自然地借助LLM的通用知识实现运动生成与理解的多任务泛化；而Part-Aware VQ-VAE通过身体和手部分层离散编码，解决了全身运动的精细协调表示问题。
claims:
- MotionGPT-2 通过将运动和文本 token 纳入统一的 LLM 词汇，实现了多模态控制条件的统一表示。
- Part-Aware VQ-VAE 使用两级离散代码本分别编码身体和手部运动，减少歧义并实现更精细的离散化表示。
- 联合训练多个运动相关任务显著提高了所有任务的性能指标，验证了统一运动-语言微调范式的有效性。
- MotionGPT-2 仅使用 1% 的可训练参数（LoRA）即可达到竞争性能，训练时间仅为其他方法的 10%。
---

# MotionGPT-2: A General-Purpose Motion-Language Model for Motion Generation and Understanding

> [!tip] 核心洞察
> 将运动和文本统一在LLM的离散token空间中，能够自然地借助LLM的通用知识实现运动生成与理解的多任务泛化；而Part-Aware VQ-VAE通过身体和手部分层离散编码，解决了全身运动的精细协调表示问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionGPT-2：面向运动生成与理解的通用运动语言模型 |
| 英文题名 | MotionGPT-2: A General-Purpose Motion-Language Model for Motion Generation and Understanding |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2410.21747) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MotionGPT-2 |
| Dataset | HumanML3D, Motion-X |

> [!tip] 效果简介
> - HumanML3D 上，R-Precision Top-1 0.496 vs 0.491 (T2M-GPT) (+0.005)；FID 0.191 vs 0.116 (T2M-GPT) (+0.075)。
> - Motion-X 上，R-Precision Top-1 0.398 (PA-VQVAE LLaMA 3.1-8B) vs 0.387 (VQVAE LLaMA 3.1-8B) (+0.011)。

## 概述

### 问题瓶颈

现有运动生成方法面临三重瓶颈：**控制条件单一**，绝大多数仅支持文本驱动，难以融合初始姿态、关键帧等多元信号；**框架任务特定**，不同任务（生成、补全、描述）需独立模型，无法利用大语言模型（LLM）的通用世界知识实现跨任务泛化；**运动表示不完整**，仅关注身体运动而忽略手部细节，导致全身运动质量不足。

### 核心思路

MotionGPT-2 的核心洞察在于：**将连续人体运动量化为离散 token，并与文本 token 统一纳入 LLM 的词汇空间**，从而借助 LLM 的通用知识实现运动生成与理解的多任务泛化。其关键调控机制包括：

- **Part-Aware VQ-VAE**：采用身体和手部分层离散编码，解决全身运动的精细协调表示问题。
- **统一运动-语言词汇**：将运动 token 和特殊标记融入 LLM 词汇表，实现多模态控制信号的统一表示。
- **LoRA 高效微调**：仅需约 1% 的可训练参数即可达到竞争性能，训练时间仅为其他方法的 10%。

### 方法谱系与知识库定位

MotionGPT-2 属于**基于 LLM 的统一运动语言模型（LMLM）**，其方法谱系可追溯至两条主线：

| 维度 | 传统方法 | MotionGPT-2 |
|------|----------|-------------|
| 运动表示 | 身体-only 连续运动序列 | 身体-手分离的离散运动 token 序列 |
| 控制条件 | 单一文本或姿势 | 多模态统一控制（文本+初始/关键帧姿势） |
| 模型架构 | 任务特定 Diffusion/GPT 模型 | 基于 LLM 的统一运动语言模型 |
| 词汇空间 | 仅文本 | 扩展为文本+运动 token 的统一词汇 |
| 训练策略 | 两阶段训练 | 三阶段训练（加入运动-语言对齐） |

相比基线方法，**T2M-GPT**（Zhang et al., CVPR 2023）和 **MoMask**（Guo et al., CVPR 2024）专注于文本到运动的单一任务；**MDM**（Tevet et al., ICLR 2023）基于扩散模型但缺乏多任务泛化能力；**MotionGPT**（Jiang et al., NeurIPS 2023）首次尝试统一运动-语言模型，但受限于身体-only 表示和两阶段训练。MotionGPT-2 在此基础上通过 Part-Aware VQ-VAE 和三阶段训练实现了关键改进。

### 主要结果

在 **HumanML3D** 基准上，MotionGPT-2 的 R-Precision Top-1 达到 0.496，略优于 T2M-GPT 的 0.491；FID 为 0.191，虽不及 T2M-GPT 的 0.116，但考虑到其多任务统一框架的优势，这一差距是可接受的。在 **Motion-X** 全身运动数据集上，Part-Aware VQ-VAE 相比标准 VQ-VAE 将 R-Precision Top-1 从 0.387 提升至 0.398，FID 从 0.666 降至 0.619，验证了分层离散编码的有效性。

消融实验进一步揭示：联合训练多个运动相关任务可将 FID 从 0.523 降至 0.482，R-Precision Top-3 从 0.604 提升至 0.683；引入初始帧或关键帧姿势控制条件后，FID 进一步降至 0.183/0.182，表明多模态控制信号对运动质量有增益作用。

### 局限与开放问题

当前方法仅依赖运动学特征，未考虑动力学约束，可能导致物理不真实的动作（如脚步滑动）；Part-Aware VQ-VAE 仍未覆盖脸部表情和手指细节。未来方向包括：显式建模身体-手部协调关系、融合视觉信息实现场景感知运动生成、探索更大规模 LLM 的性能边界与推理效率平衡，以及向实时交互场景的拓展。

## 背景与动机

### 问题背景：运动生成与理解的统一化需求

人体运动生成与理解是计算机视觉与图形学中的核心问题，涵盖文本到运动生成、运动字幕生成、运动预测、运动补全等多种任务。这些任务长期被独立建模，导致方法碎片化、知识难以复用。近年来，随着大语言模型（LLM）在通用推理与多模态对齐中展现出强大的知识迁移能力，研究者开始探索将人体运动纳入语言模型的统一框架，以实现多任务泛化。

然而，现有运动生成方法仍面临三个根本性瓶颈：

1.  **控制条件单一化**：大多数方法仅支持纯文本或单一姿势作为输入条件，无法同时处理文本、初始帧姿势、关键帧姿势等多模态控制信号。这限制了实际应用中精细控制运动的需求。
2.  **任务特定框架缺乏通用知识**：传统方法为每个任务设计独立的扩散模型或GPT模型，无法利用LLM中蕴含的世界知识（如物理常识、动作语义关联），导致生成运动的语义保真度和多样性受限。
3.  **身体-手部运动表示割裂**：现有工作主要关注身体运动生成，忽略手部细节，难以产出协调的全身运动。即使部分方法引入手部建模，也缺乏统一的身体-手部分层离散表示，导致运动歧义和精细度不足。

### 现有方法缺口

在文本到运动生成领域，**T2M-GPT**（Zhang et al., CVPR 2023）和**MoMask**（Guo et al., CVPR 2024）等基于VQ-VAE与自回归Transformer的方法取得了领先性能，但它们本质上是任务特定模型，无法迁移到运动理解任务。**MDM**（Tevet et al., ICLR 2023）和**MotionDiffuse**等扩散模型虽能生成高质量运动，但推理速度慢且难以融入多模态控制条件。

在统一运动-语言建模方向上，**MotionGPT**（Jiang et al., NeurIPS 2023）首次将运动token与文本token纳入同一词汇表，利用LLM实现多任务处理。然而，MotionGPT仍存在两阶段训练中运动-语言对齐不足、仅支持身体运动而忽略手部、以及未充分探索多模态控制条件统一表示等问题。

### 本文动机

针对上述瓶颈，MotionGPT-2提出以下核心思路：

-   **统一多模态控制表示**：将文本、初始帧姿势、关键帧姿势等多种控制信号统一表示为LLM词汇表中的token序列，使模型能够以自回归方式同时处理运动生成与理解任务。
-   **借助LLM通用知识实现任务泛化**：以LLaMA等预训练LLM为骨干，通过LoRA高效微调仅1%的可训练参数，使模型在保持LLM世界知识的同时，获得运动领域的生成与推理能力。
-   **全身运动精细离散化**：设计Part-Aware VQ-VAE，使用两级离散代码本分别编码身体和手部运动，减少身体-手部联合表示的歧义，实现更精细的全身运动合成。

通过这些设计，MotionGPT-2旨在构建一个通用运动语言模型，在多种运动相关任务上达到竞争性能，同时保持极低的训练成本（仅需其他方法10%的训练时间）。

## 核心创新

MotionGPT-2 的核心创新在于将**连续人体运动量化为离散 token**，并将其与自然语言 token 统一纳入 LLM 的词汇空间，从而构建一个**任务无关的通用运动语言模型（LMLM）**。这一设计从根本上改变了运动生成与理解的范式，其关键创新体现在以下四个层面。

### 1. 统一多模态控制表示

现有方法通常针对单一控制条件（如纯文本或单一姿势）设计任务特定框架，缺乏多任务泛化能力。MotionGPT-2 将文本描述、初始帧姿势、关键帧姿势等多种控制信号统一表示为 token 序列，使 LLM 能够以**自回归方式同时处理多模态输入**（Fig. 1, Fig. 3）。这种统一表示消除了不同任务间的架构壁垒，使得同一个模型可以执行文本生成运动、运动描述生成、运动补全、运动预测等多种任务。

### 2. Part-Aware VQ-VAE：身体-手部分层离散编码

传统运动生成方法仅关注身体运动，忽略手部细节，导致全身运动质量不足。MotionGPT-2 提出 **Part-Aware VQ-VAE**（Fig. 4），使用两级离散代码本分别编码身体运动 $\mathbf{m}^B$ 和手部运动 $\mathbf{m}^H$：

- **手部优先量化**：手部嵌入 $\mathbf{e}_h$ 首先通过手部代码本 $B_h$ 量化，然后与身体 token 融合后，再进行身体嵌入 $\mathbf{e}_b$ 的量化。这种级联设计使手部精细动作能够显式影响身体的离散表示。
- **减少表示歧义**：分离的代码本避免了身体和手部运动在单一离散空间中的相互干扰，实现了更精细的全身运动离散化。

消融实验（Table XI）验证了该设计的有效性：在 Motion-X 数据集上，Part-Aware VQ-VAE 相比标准 VQ-VAE，R-Precision Top-1 从 0.387 提升至 0.398，FID 从 0.666 降至 0.619（LLaMA 3.1-8B）。

### 3. 统一运动-语言词汇与 LLM 微调

MotionGPT-2 将原始 LLM 的文本词汇 $B_t$ 扩展为包含运动 token $B_m$ 和特殊 token $B_s$ 的统一词汇 $\boldsymbol{B} = \{B_t, B_m, B_s\}$（Section IV-B）。这一设计使得 LLM 能够**原生地理解并生成运动 token**，从而借助 LLM 预训练中蕴含的通用世界知识来指导运动生成。

在微调策略上，MotionGPT-2 采用 **LoRA 高效微调**，仅需约 **1% 的可训练参数**即可达到竞争性能，训练时间仅为其他方法的 **10%**（Section I）。损失函数为标准的自回归交叉熵：

$$\mathcal{L}_{\mathrm{LoRA}} = -\sum \log p_{\theta}(x_t \mid x_{<t}, \mathcal{T}, c)$$

其中 $\mathcal{T}$ 为任务感知指令模板，$c$ 为多模态控制条件。

### 4. 三阶段训练与多任务联合优化

相比 MotionGPT 的两阶段训练，MotionGPT-2 引入了**运动-语言对齐阶段**（Stage 2），在指令微调之前先通过混合运动-语言数据对齐两种模态的特征空间（Section IV-D）。随后的多任务联合训练（Table VIII）表明，将运动生成、描述生成、运动补全等任务联合训练，相比独立训练可显著提升所有任务的性能指标——在 HumanML3D 上，FID 从 0.523 降至 0.482，R-Precision Top-3 从 0.604 提升至 0.683。

### 创新总结

| 创新维度 | 基线方法 | MotionGPT-2 |
|---------|---------|------------|
| 运动表示 | 身体-only 连续运动序列 | 身体-手分离的离散运动 token（Part-Aware VQ-VAE） |
| 控制条件 | 单一文本或姿势 | 多模态统一控制（文本+初始/关键帧姿势） |
| 模型架构 | 任务特定 Diffusion/GPT | 基于 LLM 的统一运动语言模型 |
| 词汇空间 | 仅文本 | 文本+运动 token 的统一词汇 |
| 训练策略 | 两阶段（MotionGPT） | 三阶段（加入运动-语言对齐） |

这些创新共同构成了一个**高度泛化、参数高效、多任务统一**的运动语言框架，为通用人体运动智能奠定了基础。

## 整体框架

MotionGPT-2 构建了一个以大型语言模型（LLM）为核心枢纽的统一运动语言框架，其设计目标是将多模态控制信号（文本、初始姿势、关键帧姿势）与人体运动统一在离散 token 空间中，从而以任务无关的方式解决运动生成、理解、预测等多种下游任务。整个 pipeline 由三个核心模块串联而成：**运动离散化（Motion Tokenizer）**、**多模态统一词汇表（Unified Motion-Language Vocabulary）** 和 **基于 LLM 的运动语言模型（Motion-Language Model）**，并通过任务感知的指令模板（Instruction Prompting）引导模型执行特定任务，如 Fig. 3 所示。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2410_21747/figures/003_Figure_3.jpg]]
*Figure 3: The overview pipeline of our MotionGPT-2. MotionGPT-2 is composed of multi-modal tokenizers (Section III-A) and a versatile motion-language model (Section IV-B). With unified multimodal vocabulary and task-aware instructions (Section III-B), MotionGPT-2 enables to accept multiple control conditions (Section IV-C) and solve various motion-related tasks. MotionGPT-2 is learned by the Motion-Language Alignment stage and Instruction Tuning stage (Section IV-D)*

### 输入输出流

框架接受两类输入：
- **文本输入** $T_{\text{in}}$：自然语言描述或任务指令；
- **运动输入** $M_{\text{in}}$：可选的初始帧、关键帧或完整运动序列，作为控制条件。

输出同样为两类：
- **运动输出** $M_{\text{out}}$：生成的连续人体运动序列；
- **文本输出** $T_{\text{out}}$：运动描述或回答。

整体映射关系可形式化为：
$$M_{\text{out}}, T_{\text{out}} = f(T_{\text{in}}, \text{task}, M_{\text{in}})$$

### 模块关系与数据流

**1. Motion Tokenizer（运动离散化）**

连续人体运动首先通过运动 VQ-VAE 编码为离散 token 序列。对于全身运动，MotionGPT-2 引入 **Part-Aware VQ-VAE**（Fig. 4），将基于 SMPL-X 的人体表示拆分为身体运动 $\mathbf{m}^B$ 和手部运动 $\mathbf{m}^H$，分别使用独立的码本 $\mathcal{B}_b$ 和 $\mathcal{B}_h$ 进行量化。手部嵌入 $\mathbf{e}_h$ 先经由手部码本量化，再与身体 token 拼接融合后，对身体嵌入 $\mathbf{e}_b$ 进行量化。这一分层离散化策略减少了身体与手部运动间的表示歧义，实现了更精细的全身运动编码。VQ-VAE 的训练目标包含重建损失、码本损失和承诺损失：
$$\mathcal{L}_{\mathrm{VQVAE}} = \| \mathcal{D}(\mathcal{E}(\mathbf{m})) - \mathbf{m} \|^2 + \| \mathrm{sg}[\mathcal{E}(\mathbf{m})] - \mathbf{e} \|_2^2 + \beta \| \mathcal{E}(\mathbf{m}) - \mathrm{sg}[\mathbf{e}] \|_2^2$$

**2. 统一词汇表构建**

LLM 的原始文本词汇表 $\mathcal{B}_t$ 被扩展为统一词汇表：
$$\boldsymbol{B} = \{ B_t, B_m, B_s \}$$
其中 $B_m$ 为运动 token（来自 VQ-VAE 码本），$B_s$ 为特殊标记（用于标识运动序列边界、任务类型等）。通过将运动离散 token 直接纳入 LLM 的词汇空间，文本和运动在同一个自回归生成框架中获得了统一表示。

**3. LLM 运动语言模型与指令微调**

核心模型采用 **LLaMA 3.1-8B** 作为基础 LLM，通过 LoRA 进行参数高效微调（仅增加约 1% 可训练参数）。任务感知的指令模板 $\mathcal{T}$ 将任务描述、控制条件与输入数据组织为统一的问题格式，引导 LLM 以自回归方式预测目标运动 token 序列或文本回答。微调损失为标准交叉熵：
$$\mathcal{L}_{\mathrm{LoRA}} = -\sum \log p_{\theta}(x_t \mid x_{<t}, \mathcal{T}, c)$$

**4. 三阶段训练策略**

MotionGPT-2 采用三阶段训练流程以保证各模块协同优化：
- **阶段一**：独立训练 Motion Tokenizer（VQ-VAE），学习运动离散表示；
- **阶段二**：运动-语言对齐（Motion-Language Alignment），在混合运动-语言数据上使用 LoRA 微调 LLM，使运动和文本特征空间对齐；
- **阶段三**：指令微调（Instruction Tuning），在多任务数据上进一步微调 LLM，使其能够根据指令灵活切换运动生成、运动描述、运动补全等任务。

消融实验证实，联合训练多个任务（而非独立训练）能显著提升所有任务的性能指标——在 HumanML3D 上，FID 从 0.523 降至 0.482，R-Precision Top-3 从 0.604 提升至 0.683（Table VIII），验证了统一运动-语言微调范式的有效性。

### 与前作的关键差异

相比前作 **MotionGPT**（Jiang et al., NeurIPS 2023），MotionGPT-2 的核心改进体现在三个层面：
1. **表示层面**：从仅处理身体运动扩展到身体-手部分离的全身运动表示（Part-Aware VQ-VAE）；
2. **控制层面**：从单一文本条件扩展到支持文本、初始帧、关键帧姿势等多模态统一控制；
3. **训练层面**：从两阶段训练升级为三阶段训练，新增运动-语言对齐阶段以提升跨模态融合质量。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2410_21747/figures/001_Figure_1.jpg]]
*Figure 1: This paper proposes a versatile motion-language framework via fine-tuned LLMs given different instructions, named MotionGPT-2. Compared with the previous MotionGPT [1], our MotionGPT-2 not only retains the unique capability of accommodating multiple control conditions, but also solve various motion-related tasks using a unified model*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2410_21747/figures/002_Figure_2.jpg]]
*Figure 2: The pipeline of MotionGPT, a Motion General-Purpose generaTor. Given text and poses as an input example, we organize task descriptions (Instruction) and multiple control conditions (Input) within a question template. MotionGPT fine-tunes an LLM to generate the corresponding motion answer, which can then be decoded into human motions using a VQ-VAE decoder*

## 核心模块与公式推导

MotionGPT-2 的核心架构由三个关键模块构成：**运动离散化分词器（Motion VQ-VAE Tokenizer）**、**统一运动-语言词汇表（Unified Motion-Language Vocabulary）**，以及**基于 LLM 的运动语言模型（Motion-Language Model）**。三者协同实现从连续运动到离散 token 的转换，并将运动 token 与文本 token 统一在同一 LLM 词汇空间中，使 LLM 能够以自回归方式处理多模态控制信号并解决多种运动相关任务（图3）。

### 运动 VQ-VAE 分词器

运动 VQ-VAE 分词器负责将连续人体运动序列离散化为 token 序列，由运动编码器 $\mathcal{E}$、运动解码器 $\mathcal{D}$ 和代码本 $\mathcal{B}_m = \{b_1, b_2, \dots, b_N\}$ 组成（III-A）。给定运动序列 $\mathbf{m}$，编码器将其映射为嵌入向量，随后在代码本中寻找最近邻条目作为量化向量：

$$\mathbf{e} = \underset{b_k \in \mathcal{B}}{\arg\min} \| \mathcal{E}(\mathbf{m}) - b_k \|_2$$

对应的离散索引为：

$$p = \underset{k}{\arg\min} \| \mathcal{E}(\mathbf{m}) - b_k \|_2$$

VQ-VAE 的训练目标包含三项损失——重建损失、代码本损失和承诺损失：

$$\mathcal{L}_{\mathrm{VQVAE}} = \| \mathcal{D}(\mathcal{E}(\mathbf{m})) - \mathbf{m} \|^2 + \| \mathrm{sg}[\mathcal{E}(\mathbf{m})] - \mathbf{e} \|_2^2 + \beta \| \mathcal{E}(\mathbf{m}) - \mathrm{sg}[\mathbf{e}] \|_2^2$$

其中 $\mathrm{sg}[\cdot]$ 表示停止梯度操作，$\beta$ 为承诺损失权重。代码本采用指数移动平均（EMA）和代码本重置技术进行优化（III-A）。

### Part-Aware VQ-VAE：身体-手部分层离散编码

为克服标准 VQ-VAE 仅编码身体运动而忽略手部细节的局限，MotionGPT-2 提出 **Part-Aware VQ-VAE**（IV-A，图4）。该模块将基于 SMPL-X 的人体运动表示拆分为身体运动序列 $\mathbf{m}^B \in \mathbb{R}^{T \times d}$ 和手部运动序列 $\mathbf{m}^H \in \mathbb{R}^{T \times \bar{d}}$，分别使用独立的代码本 $B_b$ 和 $B_h$ 进行离散化。

关键设计在于：手部嵌入 $\mathbf{e}_h$ 先经由手部代码本 $B_h$ 量化，随后通过拼接操作与身体 token 融合，再对身体嵌入 $\mathbf{e}_b$ 进行量化。这种“手部先量化、身体后量化”的顺序确保了精细的手部信息在融合前得到充分离散化，从而减少身体-手部联合表示中的歧义（IV-A）。

### 统一运动-语言词汇表

为实现 LLM 对运动和文本的统一处理，MotionGPT-2 将 LLM 的原始文本词汇表 $B_t$ 扩展为包含运动 token $B_m$ 和特殊 token $B_s$ 的统一词汇表（IV-B）：

$$\boldsymbol{B} = \{ B_t, B_m, B_s \}$$

运动 token 来自 VQ-VAE 代码本中的离散索引，特殊 token 用于标记任务边界、控制条件位置等。这一设计使 LLM 能够像处理文本一样自回归地生成运动 token 序列，自然借助 LLM 的通用世界知识实现多任务泛化。

### LoRA 高效微调

MotionGPT-2 采用低秩适配（LoRA）对 LLM 进行微调（III-C），仅引入约 1% 的可训练参数。给定指令模板 $\mathcal{T}$ 和控制条件 $c$，模型以自回归方式预测下一个 token $x_t$，优化目标为交叉熵损失：

$$\mathcal{L}_{\mathrm{LoRA}} = -\sum \log p_{\theta}(x_t \mid x_{x_{<t}}, \mathcal{T}, c)$$

### 三阶段训练策略

MotionGPT-2 采用三阶段训练流程（IV-D）：
1. **运动分词器训练**：独立训练 VQ-VAE，学习运动的离散表示。
2. **运动-语言对齐**：使用混合运动-语言数据，以 LoRA 微调 LLaMA，对齐运动与语言的特征空间。
3. **指令微调**：在统一词汇表下，使用任务感知指令对 LLM 进行多任务联合微调。

消融实验（Table VIII）表明，联合训练多个运动相关任务（生成、描述、补全）相比独立训练，在 HumanML3D 上 FID 从 0.523 降至 0.482，R-Precision Top-3 从 0.604 提升至 0.683，验证了三阶段训练策略的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2410_21747/figures/004_Figure_4.jpg]]
*Figure 4: The framework overview of our proposed Part-Aware VQVAE for body-hand motion tokenization. The Part-Aware VQVAE splits SMPL-X-based human representations into body-hand motions*

## 实验与分析

### 1. 主要性能评估

MotionGPT-2 在 **HumanML3D** 和 **KIT-ML** 两个基准上进行了文本驱动运动生成的定量评估，结果如 Table I 和 Table II 所示。在 HumanML3D 上，MotionGPT-2 的 R-Precision Top-1 达到 **0.496**，略优于此前最优的 T2M-GPT (0.491)，但 FID 为 **0.191**，劣于 T2M-GPT 的 0.116 和 MoMask 的 0.045。这表明该方法在语义匹配精度上具有竞争力，但在生成运动的整体分布质量上与专用扩散/掩码模型仍存在差距——这可能是 VQ-VAE 离散化引入的信息损失与 LLM 自回归解码的累积误差共同作用的结果。

在 **Motion-X** 全身运动数据集上，Part-Aware VQ-VAE 结合 LLaMA 3.1-8B 取得了 R-Precision Top-1 **0.398**、FID **0.619**，相比标准 VQ-VAE 的 0.387 和 0.666 均有改善，验证了身体-手部分离离散编码对全身运动质量的增益。

Table IV 展示了运动描述生成任务的结果。MotionGPT-2 在 BLEU、CIDEr 等语言指标上全面超越 MotionGPT（Jiang et al., NeurIPS 2023），且生成描述在语义丰富度上更接近真实标注（见 Figure 6）。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2410_21747/figures/010_Figure_6.jpg]]
*Figure 6: Comparison of the state-of-the-art method on the motion captioning task. The results demonstrate that our MotionGPT-2 outperforms the MotionGPT on the HumanML3D [20], generating more conceptually and semantically rich motion descriptions. Specific words are marked to highlight the semantic similarity of the generated captions and the real one. Best viewed in color*

### 2. 消融研究

**联合训练的有效性**（Table VIII）：将运动生成、描述生成、运动补全等多任务联合训练，相比独立训练在 HumanML3D 上 FID 从 **0.523** 降至 **0.482**，R-Precision Top-3 从 **0.604** 提升至 **0.683**。这一结果强有力地支持了核心洞见——统一运动-语言微调范式使 LLM 能够跨任务共享表征，从而提升各任务的泛化性能。

**Part-Aware VQ-VAE 的贡献**（Table XI）：在 Motion-X 上，PA-VQVAE 相比标准 VQVAE 在 LLaMA 3.1-8B 下 R-Precision Top-1 提升 **+0.011**，FID 降低 **-0.047**。手部运动与身体运动在动态范围和语义粒度上的差异天然导致共享代码本的歧义问题；分层编码通过独立代码本缓解了这一瓶颈，使全身运动的离散化表示更精细。

**LLM 类型与规模的影响**（Table V）：在 HumanML3D 上，从 T5-base 到 LLaMA 3-8B 再到 LLaMA 3.1-8B，R-Precision 和 FID 持续改善，表明更大规模、更强语言能力的 LLM 能提供更丰富的先验知识，有利于运动token的序列建模。

**LoRA 超参数的影响**（Table XII）：固定 α=16 时，增加 LoRA rank r 持续提升性能，r=32 时 FID 达到 **0.191**，R-Precision 全面改善。这表明更大的低秩适配维度能更好地捕捉运动-语言跨模态映射的复杂性。

**多控制条件的增益**（Table III / Table VII）：在 HumanML3D 上，加入初始帧或关键帧姿势作为控制条件，相比纯文本生成，FID 进一步降低至 **0.183** / **0.182**（纯文本为 0.191），同时姿势一致性指标显著优于基线。这验证了统一多模态控制表示的有效性——LLM 能够自然地利用额外的运动token约束来生成更可控、更连贯的运动序列。

**指令设计的影响**（Table IX）：不同指令模板对生成质量有显著影响，精心设计的任务感知指令能有效引导 LLM 的行为，提升语义匹配精度。

### 3. 定性分析

Figure 5 展示了 HumanML3D 上的可视化对比。MotionGPT-2 生成的“踢腿”、“转身行走”等动作在语义保真度和自然度上与 MDM、T2M-GPT 相当，但部分复杂动作（如“像松鼠一样行动”）的物理合理性仍显不足——这与仅依赖运动学特征、未引入动力学约束的局限性一致。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2410_21747/figures/008_Figure_5.jpg]]
*Figure 5: Showcase of visualization results for the text-based motion generation task using the HumanML3D [20] dataset. We compare our MotionGPT-2 with the state-of-the-art method, i.e., MDM [59], T2M-GPT [14], MotionGPT [1]. Compared with these methods, our MotionGPT-2 perform admirably to generate vivid human motions and preserve the semantic fidelity*

Figure 7 展示了 Motion-X 上的全身运动生成结果。模型能生成“弹钢琴”、“挥手告别”等包含手部交互的动作，体现了 Part-Aware VQ-VAE 对手部细节的捕捉能力。然而，手指级别的精细动作（如“比OK手势”）仍不够精确，面部表情完全缺失，这与方法局限性中“缺乏脸部表情和手指细节建模”的分析一致。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2410_21747/figures/012_Figure_7.jpg]]
*Figure 7: Qualitative results of our proposed method on the Motion-X [28] dataset. Utilizing the world knowledge of LLMs, our MotionGPT-2 demonstrates the capability to generate realistic body motions while effectively capturing lifelike hand interactions, e.g., making the OK gesture, plays the piano, saying goodbye*

Figure 9 展示了多控制条件下的生成图集。给定初始帧或关键帧姿势，模型能生成物理上连贯的后续运动，验证了统一多模态控制框架的实用性。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2410_21747/figures/018_Figure_9.jpg]]
*Figure 9: Gallery showcasing the results of generated human motions by MotionGPT-2 with multiple control conditions on the HumanML3D dataset [20], i.e., Text+Initial Motion Token, Text+Last Motion Token, and Text+Random Key Motion Token. With these diverse control signals, our MotionGPT-2 demonstrates the ability to generate physically realistic human motions. TABLE X: Evaluation of motion prediction and in-betweening on part of the AMASS [62] dataset, considering only motion data. FID reflects the quality of the generated motions, while Diversity quantifies the motion variability within each condition. ADE and FDE represent the distance between generated joint positions and the ground truth*

### 4. 失败模式与局限

实验揭示的主要失败模式包括：
- **物理不真实**：部分生成动作出现脚步滑动等违反物理约束的现象，根源在于仅使用运动学特征，未考虑地面接触、动量守恒等动力学约束。
- **手部细节不足**：尽管 PA-VQVAE 改善了全身运动，但手指级别的精细交互（如弹钢琴的指法）仍不够准确。
- **数据依赖**：模型在 HumanML3D 和 Motion-X 上表现良好，但对数据稀缺的动作类型泛化能力有限，这需要在更广泛的数据集上进行验证。

### 5. 效率分析

MotionGPT-2 仅使用 **1%** 的可训练参数（通过 LoRA 微调 LLaMA），训练时间仅为其他方法的 **10%**，在参数效率与训练成本上具有显著优势。这得益于将运动生成问题转化为 LLM 词汇空间内的自回归token预测，从而充分利用了预训练 LLM 的现有能力，避免了对大规模运动生成模型的从头训练。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2410_21747/figures/005_Table.jpg]]
*Table: I: Quantitative results of text-based motion generation on the HumanML3D dataset. $\mathrm { \Delta ^ { 6 6 } \mathrm { { a l } ^ { 5 } } }$ denotes the results computed with GT motions. “→” indicates metrics that are better when closer to “Real” distribution. “MultiModal Dist.” denotes the Multi-Modality Distance. We conduct each evaluation 20 times, presenting the average metric and a 95% confidence interval, with the top scores marked in bold*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2410_21747/figures/006_Table.jpg]]
*Table: II: Quantitative results of text-based motion generation on the KIT-ML dataset. “Real” denotes the results computed with GT motions. “→” indicates metrics that are better when closer to “Real” distribution. TABLE III: Assessment of motion generation on the HumanML3D and KIT-ML test subsets across diverse control conditions. With initial or key tokens, MotionGPT-2 demonstrate superior performance compared to the text-only version*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2410_21747/figures/007_Table.jpg]]
*Table: IV: Experiments of motion captioning task on the HumanML3D benchmark. Results marked with * are from MotionGPT, and were computed using unprocessed ground truth texts for linguistic metrics*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2410_21747/figures/009_Table.jpg]]
*Table: V: Ablations on the effects of LLM types and scales on text-based motion generation, evaluated on the HumanML3D benchmark. In addition to full fine-tuning of the encoder-decoder T5-base model, LoRA-based fine-tuning is used for optimizing other decoder-only LLMs*

## 方法谱系与知识库定位

### 1. 与基线方法的关系定位

MotionGPT-2 的核心定位是**通用运动语言模型（Large Motion-Language Model, LMLM）**，其技术路线与现有运动生成方法存在根本性差异。理解这一差异的关键在于“表示空间”与“模型架构”两个维度的变革。

#### 1.1 相对于任务特定扩散/自回归模型的演进

传统运动生成方法，如 **MDM**（Tevet et al., ICLR 2023）、**MotionDiffuse** 和 **MoMask**（Guo et al., CVPR 2024），通常为单一任务（如文本到运动）设计专用框架。它们直接在连续运动空间上操作，使用扩散模型或掩码Transformer进行生成。这类方法的瓶颈在于：**控制条件单一**（通常仅文本），且**无法利用大型语言模型（LLM）中蕴含的通用世界知识**来理解复杂的运动语义。

MotionGPT-2 通过将连续运动量化为离散token，使运动序列与文本序列在表示层面统一。这一转变使得模型可以：
- 将多模态控制信号（文本、初始帧姿势、关键帧姿势）统一编码为LLM可理解的token序列；
- 借助LLM的语义理解和推理能力，生成物理上更合理、语义上更贴切的运动。

从表 I（HumanML3D）的结果来看，MotionGPT-2 在 R-Precision Top-1 上达到 0.496，略高于 **T2M-GPT**（Zhang et al., CVPR 2023）的 0.491，但在 FID 上（0.191 vs. 0.116）仍有差距。这表明离散化表示在文本-运动匹配精度上具有竞争力，但连续运动的重建保真度仍有提升空间。

#### 1.2 相对于第一代运动语言模型的改进

**MotionGPT**（Jiang et al., NeurIPS 2023）首次提出将运动生成视为LLM的语言建模任务，但其存在三个关键局限：
1. **仅生成身体运动**，忽略手部细节，无法实现全身运动生成；
2. **两阶段训练策略**（先训练运动tokenizer，再微调LLM）缺乏显式的运动-语言对齐阶段；
3. **控制条件有限**，难以处理多模态输入。

MotionGPT-2 针对上述局限进行了系统性改进，形成三个关键“变化槽”（changed slots）：

| 变化维度 | MotionGPT (基线) | MotionGPT-2 (改进) |
|---------|-----------------|-------------------|
| **运动表示** | 身体-only连续运动序列 | 身体-手分离的离散运动token序列（Part-Aware VQ-VAE） |
| **词汇空间** | 仅文本 | 扩展为文本+运动token的统一词汇 |
| **训练策略** | 两阶段训练 | 三阶段训练（加入Motion-Language Alignment） |

Part-Aware VQ-VAE 的引入是表示层面的关键创新。它使用两个独立的离散代码本 $B_b$ 和 $B_h$ 分别编码身体和手部运动，并在手部量化后将手部token与身体嵌入融合，再进行身体量化。这一设计减少了身体与手部运动表示之间的歧义，使模型能够生成具有精细手部交互的全身运动（如 OK 手势、弹钢琴等），见 Figure 7。

三阶段训练策略中新增的**运动-语言对齐阶段**（Stage 2），通过在混合运动-语言数据上以无监督和有监督方式微调LLaMA，显式地对齐运动和语言的特征空间。消融实验（Table VIII）证实，联合训练多个任务（运动生成、captioning、运动补全）相比独立训练，在 HumanML3D 上 FID 从 0.523 降至 0.482，R-Precision Top-3 从 0.604 提升至 0.683。这一结果验证了统一运动-语言微调范式的有效性。

#### 1.3 相对于其他统一模型的方法论差异

与 **MotionLLM** 等其他统一运动语言模型相比，MotionGPT-2 的差异化优势在于：
- **LoRA 高效微调**：仅使用 1% 的可训练参数即可达到竞争性能，训练时间仅为其他方法的 10%。这一参数效率使得在消费级 GPU 上微调 8B 级别的 LLM 成为可能。
- **多模态控制统一**：通过将初始帧/关键帧姿势编码为运动token并融入指令模板，实现了文本+姿势的联合控制，而无需额外的条件编码器。

### 2. 适用边界与能力范围

#### 2.1 能力范围

MotionGPT-2 在以下任务上展现出统一的处理能力：
- **文本到运动生成**（text-to-motion）：在 HumanML3D 和 KIT-ML 上达到 competitive 水平；
- **运动 captioning**（motion-to-text）：生成语义丰富的运动描述，优于 MotionGPT；
- **运动预测与中间帧生成**（motion prediction & in-betweening）：在 AMASS 子集上验证；
- **多控制条件运动生成**：支持文本+初始帧、文本+末尾帧、文本+随机关键帧等组合。

#### 2.2 适用边界

以下场景超出当前方法的能力范围：
- **动力学约束**：模型仅依赖运动学特征（关节位置/旋转），未考虑物理动力学，可能导致脚步滑动等不真实动作；
- **脸部表情与手指细节**：尽管 Part-Aware VQ-VAE 改善了手部运动，但尚未对脸部表情和手指级精细动作建模；
- **数据稀缺领域**：训练依赖大规模运动-文本对（HumanML3D、Motion-X），对特定运动风格或领域的泛化能力有限；
- **实时交互**：所有任务以离线方式处理，未探讨低延迟场景的可行性。

### 3. 局限与开放问题

#### 3.1 已验证的局限

1. **运动学表示的天花板**：当前模型仅使用 SMPL-X 的运动学参数，缺乏对物理约束的显式建模。这可能导致生成的步态存在滑动伪影，在需要精确物理交互的场景（如机器人控制）中不足以直接使用。
2. **全身表示的粒度不足**：Part-Aware VQ-VAE 将手部作为整体进行离散化，但手指的独立运动（如弹钢琴时的指法）仍难以精确捕捉。脸部表情则完全未被纳入表示。
3. **数据依赖性**：模型性能高度依赖训练数据的质量和多样性。在 HumanML3D 上 FID 仍有 0.191（与 Real 的 0.002 差距显著），表明离散化表示在运动细节保真度上存在固有损失。

#### 3.2 开放问题

1. **身体-手部协调的显式建模**：Part-Aware VQ-VAE 通过简单拼接融合身体和手部token，缺乏对两者协调关系的显式建模。如何设计注意力机制或图结构来捕捉身体-手部的空间-时间依赖，可能进一步提升运动自然度。
2. **视觉信息的融入**：当前模型仅处理文本和姿势输入。能否将视频帧或场景图像融入 MotionGPT-2 的指令模板，实现场景感知的运动生成（如“在这个房间里坐下”）？这需要扩展统一词汇表以包含视觉token。
3. **更大规模 LLM 的潜力与成本平衡**：Table V 的消融显示，更大规模的 LLM（如 LLaMA 3.1-8B）带来性能提升。但如何利用 GPT-4 级别的模型进一步突破性能上限，同时控制推理成本和延迟，是一个工程与算法兼顾的挑战。
4. **实时应用可行性**：在游戏、虚拟人等实时动画场景中，自回归生成+运动解码的延迟是否可接受？可能需要探索非自回归解码或模型蒸馏方案。
5. **真正的全身数字人驱动**：将脸部表情（如 FLAME 参数）和手指级动作纳入统一表示，实现面部-身体-手部的联合生成，是通往完整数字人驱动的关键一步。这需要设计更细粒度的 Part-Aware 量化方案，并获取相应的全身运动-文本配对数据。

## 原文 PDF

![[paperPDFs/arxiv_2024/MotionGPT_2_A_General_Purpose_Motion_Language_Model_for_Motion_Generation_and_Understanding.pdf]]