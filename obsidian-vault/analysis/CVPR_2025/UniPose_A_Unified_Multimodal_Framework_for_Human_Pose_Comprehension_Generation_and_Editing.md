---
title: "UniPose: A Unified Multimodal Framework for Human Pose Comprehension, Generation and Editing"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/UniPose_A_Unified_Multimodal_Framework_for_Human_Pose_Comprehension_Generation_and_Editing.pdf
project_link: null
code_link: https://github.com/liyiheng23/UniPose
aliases:
- UniPose
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过VQ-VAE姿态分词器将3D姿态量化为离散token，并将姿态专用视觉编码器与CLIP并行融合，同时在LLM中引入混合注意力机制（文本使用因果注意力，姿态使用双向注意力），使得单个模型能够统一处理七种姿态相关任务。
primary_logic: 将3D人体姿态视为一种可与文本共享词汇表的“语言”，利用离散化统一姿态与文本的表示；并通过混合视觉编码器和混合注意力机制，在保持大语言模型强文本生成能力的同时，显著提升了对姿态细粒度语义的感知和生成能力。
claims:
- UniPose首次在统一框架中集成7种姿态理解、生成与编辑核心任务。
- 姿态分词器将3D姿态压缩为离散token，使其能与文本在LLM中无缝融合。
- 混合注意力机制中双向注意力提升了姿态生成质量并大幅降低推理延迟。
- 加入姿态专用视觉编码器显著改善了细粒度姿态理解。
---

# UniPose: A Unified Multimodal Framework for Human Pose Comprehension, Generation and Editing

> [!tip] 核心洞察
> 将3D人体姿态视为一种可与文本共享词汇表的“语言”，利用离散化统一姿态与文本的表示；并通过混合视觉编码器和混合注意力机制，在保持大语言模型强文本生成能力的同时，显著提升了对姿态细粒度语义的感知和生成能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniPose：面向人体姿态理解、生成与编辑的统一多模态框架 |
| 英文题名 | UniPose: A Unified Multimodal Framework for Human Pose Comprehension, Generation and Editing |
| 会议/期刊 | CVPR 2025 |
| Links | [Code](https://github.com/liyiheng23/UniPose) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | UniPose |
| Dataset | PoseScript, PoseFix, ImageScript, 3DPW |

> [!tip] 效果简介
> - PoseScript 上，R-Precision Top-1 (Pose-to-Text) 85.6 vs 91.6 (PoseScript) (-6.0)。
> - PoseFix 上，R-Precision Top-1 (Pose-Diff) 67.9 vs 64.6 (PoseFix) (+3.3)。
> - ImageScript 上，R-Precision Top-1 (Image-to-Text) 24.5 vs 17.7 (GPT4V) (+6.8)。

## 概要

人体姿态理解、生成与编辑是构建具身智能和人机交互系统的关键能力。然而，现有方法通常将这些任务孤立处理，缺乏一个统一的表示空间来桥接3D姿态、文本和图像三种模态。与此同时，以CLIP为代表的通用视觉编码器难以捕捉精细化的姿态细节，导致多模态大语言模型（MLLM）在姿态相关任务上的表现受限。

针对上述瓶颈，本文提出**UniPose**——首个在统一框架内集成七种核心姿态任务的模型，涵盖姿态描述、姿态差异描述、文本到姿态生成、图像到姿态生成、姿态估计、姿态编辑以及基于推理的姿态估计。UniPose的核心洞察在于：**将3D人体姿态视为一种可与文本共享词汇表的“语言”**。通过VQ-VAE姿态分词器将连续姿态参数量化为离散token，姿态得以与文本token在统一的词汇空间中无缝融合。在此基础上，UniPose引入混合视觉编码器（CLIP-ViT + 姿态专用ViT）以增强细粒度姿态感知，并在大语言模型中采用混合注意力机制——文本使用因果注意力以保持生成质量，姿态使用双向注意力以提升生成精度并大幅降低推理延迟。

实验结果表明，UniPose在多个基准上达到了与专用模型相当甚至更优的性能：在PoseScript的姿态描述任务上取得85.6%的Top-1检索精度；在文本到姿态生成任务上MPJPE降至308.6 mm，优于专用模型PoseScript的318.0 mm；在3DPW和Human3.6M的姿态估计任务上，MPJPE分别达到94.7 mm和69.2 mm，显著优于MLLM基线ChatPose（分别降低68.9 mm和56.8 mm）。消融实验进一步验证了混合视觉编码器和混合注意力机制的关键贡献。值得注意的是，作为通用框架，UniPose在姿态估计精度上仍与专用回归方法存在差距（3DPW上94.7 vs 67.5），这为后续研究指明了方向。



人体姿态理解与生成是计算机视觉领域的核心问题，涵盖姿态估计、文本到姿态生成、姿态描述生成、姿态差异描述及姿态编辑等多项任务。这些任务在具身智能、人机交互、运动分析与数字内容创作中具有广泛的应用前景。然而，现有方法通常孤立地处理这些任务，各自依赖专用的模型架构与表示空间，缺乏跨3D姿态、文本和图像的统一框架。这种碎片化的研究范式不仅增加了系统集成的复杂性，也阻碍了不同任务间的知识共享与迁移。

具体而言，在姿态理解方面，**PoseScript** 等专用模型能够从3D姿态生成自然语言描述，**PoseFix** 则专注于描述两帧姿态之间的差异并执行编辑操作，但这些方法均针对单一任务设计，无法泛化到其他姿态相关任务。在姿态生成方面，**ChatPose** 和 **ChatHuman** 等近期工作尝试利用大语言模型（LLM）处理多模态人体数据，但其任务覆盖范围仍然有限。通用多模态大语言模型如 **LLaVA**、**Qwen-VL** 和 **GPT4V** 虽然具备强大的视觉语言理解能力，但由于其视觉编码器（如CLIP）难以捕捉精细化的3D姿态细节，在姿态相关的细粒度感知与生成任务上表现欠佳。与此同时，**HMR**、**HMR2.0** 和 **TokenHMR** 等专用姿态估计方法虽在重建精度上领先，却完全不具备语言交互与多任务泛化能力。

这一现状揭示了一个核心瓶颈：**现有方法缺乏一个能够统一表示3D姿态、文本和图像的共享语义空间**。3D姿态本质上是连续的结构化数据，而文本是离散的符号序列，二者之间的模态鸿沟使得通用视觉语言模型难以直接建立精确的对应关系。此外，通用视觉编码器在预训练阶段通常面向通用物体识别，对关节角度、肢体方向等细粒度姿态属性的感知能力不足，进一步限制了多模态大语言模型在姿态任务上的表现。

为突破上述局限，UniPose提出了一个根本性的视角转换：**将3D人体姿态视为一种可与文本共享词汇表的“语言”**。通过VQ-VAE姿态分词器将连续3D姿态压缩为离散token序列，姿态便可在LLM的统一词汇空间中与文本token无缝融合。在此基础上，UniPose引入混合视觉编码器（CLIP-ViT + 姿态专用ViT）和混合注意力机制（文本使用因果注意力，姿态使用双向注意力），在保持大语言模型强文本生成能力的同时，显著提升了对姿态细粒度语义的感知和生成能力。这一设计使得单个模型能够统一处理七种姿态相关任务，包括姿态描述生成、姿态差异描述、图像到文本描述、文本到姿态生成、姿态估计、姿态编辑以及基于推理的姿态估计，首次在统一框架中实现了姿态理解、生成与编辑的全面覆盖。



## 核心方法与创新机理

UniPose的核心创新在于通过三个关键设计，首次将人体姿态的理解、生成与编辑任务统一到一个多模态大语言模型框架中，其本质是将3D人体姿态视为一种可与文本共享词汇表的“语言”。

### 1. 姿态离散化：将3D姿态转化为语言Token

现有方法通常以连续特征或分离编码的方式处理3D姿态，难以与基于离散token的大语言模型无缝融合。UniPose的核心突破之一是**姿态分词器（Pose Tokenizer）**，它基于VQ-VAE架构，将连续的3D SMPL姿态参数压缩为离散的姿态token序列，并将其纳入LLM的统一词汇表。这一设计使得姿态与文本在表示层面实现了真正的统一——姿态token与文本token可以混合输入、联合建模，为后续的多任务统一处理奠定了基础。

量化过程可形式化地描述为：将编码器输出的潜在向量 $\boldsymbol{z}$ 替换为可学习码本 $\mathcal{B}_p$ 中距离最近的条目：

$$\widehat{\boldsymbol{z}} = \underset{b_m \in \mathcal{B}_p}{\arg\min} \| \boldsymbol{z} - b_m \|_2$$

进而将量化后的潜在向量映射为离散码本索引，得到姿态token序列 $\mathbf{u}$。

### 2. 混合视觉编码器：弥补通用编码器的细粒度感知缺陷

通用视觉语言模型通常仅依赖CLIP视觉编码器，但CLIP在预训练中缺乏对精细人体姿态的感知能力，导致姿态理解任务表现受限。UniPose提出**混合视觉编码器（Mixture-of-Visual-Encoders）**，在保留CLIP-ViT的同时，引入一个专门为姿态估计任务预训练的姿态专用ViT（Pose-ViT）。两者并行提取特征后融合，使模型既能保持通用语义理解能力，又能捕捉细粒度的姿态细节。

消融实验（Table 6）证实，加入姿态专用视觉编码器后，UniPose在所有姿态理解指标上均获得显著提升，验证了这一设计的有效性。

### 3. 混合注意力机制：文本与姿态的分治建模

传统LLM对所有token统一施加因果注意力（causal attention），这在处理姿态token时存在两个问题：一是姿态token之间并非严格时序依赖，因果注意力限制了信息流动；二是逐token自回归生成导致推理延迟较高。UniPose创新性地引入**混合注意力机制（Mixed Attention）**：对文本token保持因果注意力以维持语言生成质量，对姿态token则采用双向注意力（bidirectional attention），使所有姿态token能够并行生成。

这一设计带来了双重收益：在文本到姿态生成任务上，Top-1检索精度从9.0提升至13.8；同时推理延迟从2.5秒大幅降至0.2秒（Table 7）。值得注意的是，混合注意力在姿态描述任务上BLEU-4略有下降，这提示文本与姿态的注意力需求存在内在张力，是一个值得进一步探索的开放问题。

### 创新总结

上述三个“changed slots”构成了UniPose区别于已有工作的核心差异：**姿态表示**从连续特征变为离散token，**视觉编码器**从单一CLIP扩展为混合架构，**注意力机制**从统一因果注意力分化为文本因果/姿态双向的混合模式。三者协同作用，使得单个模型能够覆盖7种姿态相关任务，并在大多数任务上达到接近甚至超越专用模型的性能。



UniPose 的整体架构由三大核心组件串联构成：**姿态分词器 (Pose Tokenizer)**、**视觉处理器 (Visual Processor)** 和**姿态感知大语言模型 (Pose-Aware LLM)**。其设计目标是将 3D 人体姿态视为一种可与文本共享词汇表的“语言”，从而在统一的多模态骨干网络中联合处理姿态理解、生成与编辑任务。

### 数据流与模块协作

整个框架的输入可以是文本指令、图像或 3D 姿态参数，输出则为姿态描述文本、修正后的 3D 姿态或从图像中恢复的 3D 姿态。数据流如下：

1. **姿态输入路径**：原始 3D 姿态参数（SMPL 格式）首先进入姿态分词器，被压缩为离散的姿态 token 序列。这些 token 通过统一词汇表直接送入 LLM，与文本 token 共享表示空间。

2. **视觉输入路径**：输入图像同时送入两个并行的视觉编码器——CLIP 视觉编码器和姿态专用视觉编码器。前者提供通用语义特征，后者通过姿态估计预训练捕获细粒度姿态细节。两者的输出融合后经投影层映射到 LLM 的输入空间，形成视觉嵌入。

3. **LLM 处理与输出**：LLM 接收文本 token、姿态 token 和视觉嵌入的混合输入，通过混合注意力机制进行处理——**文本 token 使用因果注意力**以保持自回归生成能力，**姿态 token 使用双向注意力**以实现单步并行生成所有姿态 token，从而大幅降低推理延迟。输出端根据任务类型生成文本描述或姿态 token 序列，后者经姿态分词器的解码器还原为连续 3D 姿态参数。

### 统一词汇表机制

UniPose 的核心创新之一是将姿态离散化后纳入 LLM 的词汇表。姿态分词器基于 VQ-VAE 构建，包含编码器、解码器和可学习码本 $\mathcal{B}_p = \{b_m\}_{m=1}^M$。编码器将 3D 姿态映射为潜在向量 $\boldsymbol{z}$，再通过最近邻查找量化为码本条目：

$$\widehat{\boldsymbol{z}} = \underset{b_m \in \mathcal{B}_p}{\arg\min} \| \boldsymbol{z} - b_m \|_2$$

量化后的潜在向量被映射为离散码本索引，形成姿态 token 序列 $\mathbf{u}$。这些姿态 token 的词汇表 $\mathcal{V}_p$ 与原始文本词汇表 $\mathcal{V}_t$ 合并，构成统一词汇表 $\mathcal{V} = \{\mathcal{V}_t, \mathcal{V}_p\}$。这使得 LLM 能够以处理文本的方式处理 3D 姿态，实现跨模态的联合建模。

### 训练范式

UniPose 采用四阶段训练策略（Figure 3）：
- **阶段一**：独立训练姿态分词器，使用重建损失、嵌入损失和承诺损失的组合 $\mathcal{L}_{vq} = \mathcal{L}_r + \mathcal{L}_e + \mathcal{L}_c$。
- **阶段二**：姿态-文本对齐预训练，在文本描述数据上训练 LLM 理解姿态 token 与文本的对应关系。
- **阶段三**：视觉投影器预训练，对齐视觉嵌入与 LLM 的输入空间。
- **阶段四**：指令微调，在所有七种任务上联合训练，总损失为各子任务损失之和 $\mathcal{L} = \mathcal{L}_1 + \mathcal{L}_2 + \mathcal{L}_3 + \mathcal{L}_4$，分别对应单姿态理解、姿态对差异理解、姿态生成和姿态编辑。

![[assets/figures/papers/paper_list_l1869_UniPose_A_Unified_Multimodal_Framework_for_Human_Pose_Comprehension_Gene/figures/004_Figure_3.jpg]]
*Figure 3: The training paradigm of UniPose*

![[assets/figures/papers/paper_list_l1869_UniPose_A_Unified_Multimodal_Framework_for_Human_Pose_Comprehension_Gene/figures/014_Figure_3.jpg]]
*Figure 3: Prompt to query GPT-4 for refining text in the ImageDiff dataset*

### 推理流程

在姿态生成和编辑任务中，当模型预测到姿态起始 token `<p>` 后，系统会向条件文本 token 追加 $L_p$ 个预定义的姿态查询 token，LLM 据此并行预测对应的姿态 token 序列，再经解码器恢复为 3D 姿态。这种双向注意力下的并行生成机制将推理延迟从 2.5 秒降至 0.2 秒，同时将文本到姿态的 Top-1 检索精度从 9.0 提升至 13.8（Table 7）。

### 补充图表

![[assets/figures/papers/paper_list_l1869_UniPose_A_Unified_Multimodal_Framework_for_Human_Pose_Comprehension_Gene/figures/003_Figure_2.jpg]]
*Figure 2: Method overview: UniPose comprises a Pose Tokenizer, Visual Processor and a pose-aware language LLM. Combining Pose Tokens learned by pose tokenizer, Visual Embeddings from visual processor and Text Tokens from text tokenizer, UniPose enables joint modeling of pose comprehension, generation and editing within a unified visual-language backbone*

![[assets/figures/papers/paper_list_l1869_UniPose_A_Unified_Multimodal_Framework_for_Human_Pose_Comprehension_Gene/figures/001_Figure_1.jpg]]
*Figure 1: UniPose can handle pose comprehension, generation and editing tasks under different instructions within a unified framework*



UniPose 由三大核心组件构成：**姿态分词器** (Pose Tokenizer)、**视觉处理器** (Visual Processor) 和**姿态感知大语言模型** (Pose-Aware LLM)。三者协同工作，将3D人体姿态、图像和文本统一在同一框架内处理。

### 3.1 姿态分词器

姿态分词器的目标是将连续的3D人体姿态压缩为离散token序列，使姿态能够像文本一样被LLM处理。该模块基于VQ-VAE架构构建，包含编码器 $E$、解码器 $D$ 和可学习码本 $\mathcal{B}_p = \{b_m\}_{m=1}^M$。

**量化过程**：编码器将输入的SMPL姿态参数映射为潜在向量 $\boldsymbol{z}$，随后通过最近邻查找将每个潜在向量替换为码本中最接近的条目：

$$ \widehat{\boldsymbol{z}} = \underset{b_m \in \mathcal{B}_p}{\arg\min} \| \boldsymbol{z} - b_m \|_2 $$

量化后的潜在向量被映射为离散码本索引，形成姿态token序列：

$$ \mathbf{u} = \underset{m \in \{1, \dots, M\}}{\arg\min} \| z - b_m \|_2 $$

**训练损失**：姿态分词器的训练目标由三部分组成——加权L2重建损失、嵌入损失和承诺损失：

$$ \mathcal{L}_{vq} = \mathcal{L}_r + \mathcal{L}_e + \mathcal{L}_c $$

其中重建损失 $\mathcal{L}_r$ 同时约束姿态参数、网格顶点和关键点的重建精度：

$$ \mathcal{L}_r = \lambda_1 \|\widehat{\pmb{p}} - \pmb{p}\|_2 + \lambda_2 \|\widehat{\pmb{v}} - \pmb{v}\|_2 + \lambda_3 \|\widehat{\pmb{j}} - \pmb{j}\|_2 $$

嵌入损失 $\mathcal{L}_e = \|sg[z] - \widehat{z}\|_2^2$ 强制码本嵌入向编码器输出对齐，承诺损失 $\mathcal{L}_c = \|z - sg[\widehat{z}]\|_2^2$ 则约束编码器输出向码本嵌入靠拢（$sg[\cdot]$ 表示停止梯度算子）。

### 3.2 视觉处理器

视觉处理器采用**混合视觉编码器**设计，并行融合两个视觉编码器的输出：原始的CLIP-ViT用于保持通用视觉语义理解，额外引入的姿态专用ViT则专门针对姿态估计任务预训练，用于捕获细粒度姿态细节。这一设计解决了通用视觉编码器难以感知精细姿态信息的关键瓶颈。

### 3.3 姿态感知LLM与混合注意力

**统一词汇表**：将LLM的原始文本词汇表 $\mathcal{V}_t$ 扩展，加入姿态词汇表 $\mathcal{V}_p$，形成统一的文本-姿态词汇表 $\mathcal{V} = \{\mathcal{V}_t, \mathcal{V}_p\}$。这使得姿态token和文本token可以在同一自回归框架中被LLM处理。

**多任务训练目标**：UniPose通过四个损失函数联合优化，覆盖七种姿态相关任务：

- **单姿态理解损失** $\mathcal{L}_1$：最大化给定视觉或姿态token时，姿态描述文本的条件对数似然：

$$ \mathcal{L}_{1} = \sum_{i=1}^{L_t} \log p_{\theta} \left( t^{i} | \mathbf{v} / \mathbf{u}, t^{< i} \right) $$

- **姿态对理解损失** $\mathcal{L}_2$：最大化给定姿态对或图像对时，姿态差异描述的条件对数似然：

$$ \mathcal{L}_{2} = \sum_{i=1}^{L_d} \log p_{\theta} \left( d^{i} | \left( \mathbf{v}_{1}, \mathbf{v}_{2} \right) / \left( \mathbf{u}_{1}, \mathbf{u}_{2} \right), d^{< i} \right) $$

- **姿态生成损失** $\mathcal{L}_3$：最大化给定视觉或文本条件及姿态查询 $\mathcal{Q}$ 时，完整姿态token序列的条件概率：

$$ \mathcal{L}_{3} = p_{\theta} \left( \mathbf{u} | \mathbf{v} / \mathbf{t}, \mathcal{Q} \right) $$

- **姿态编辑损失** $\mathcal{L}_4$：最大化给定初始姿态和修正指令时，修正后姿态的条件概率：

$$ \mathcal{L}_{4} = p_{\theta} \left( \mathbf{u}_{2} | \mathbf{u}_{1}, \mathbf{d}, \mathcal{Q} \right) $$

总训练损失为上述四项之和：$\mathcal{L} = \mathcal{L}_1 + \mathcal{L}_2 + \mathcal{L}_3 + \mathcal{L}_4$。

**混合注意力机制**：这是UniPose的核心设计创新之一。LLM对文本token使用标准因果注意力（保证自回归生成的因果性），而对姿态token使用双向注意力。推理时，当模型预测到姿态起始标记 `<p>` 后，系统将 $L_p$ 个预定义的姿态查询追加到条件文本token之后，LLM通过双向注意力一次性并行预测所有姿态token，将推理延迟从2.5秒大幅降至0.2秒。

### 3.4 训练范式

UniPose的训练分为四个阶段：姿态分词器训练、姿态-文本对齐预训练、视觉投影器预训练和指令微调。多阶段训练策略确保了各组件在统一框架中的协同优化，但也增加了训练流程的复杂性——这是该方法的一个已知局限。



## 实验与关键发现

### 实验设置与评估基准

UniPose在七个核心姿态任务上进行了系统性评估，涵盖姿态理解（姿态描述生成、姿态差异描述、图像描述、图像差异描述）、姿态生成（文本到姿态生成）和姿态编辑。评估数据集包括PoseScript、PoseFix，以及新构建的ImageScript和ImageDiff数据集。姿态估计任务在3DPW和Human3.6M基准上进行评测。主要对比基线包括专用模型（PoseScript、PoseFix、HMR、HMR2.0、TokenHMR）和通用多模态模型（ChatPose、ChatHuman、LLaVA、Qwen-VL、GPT4V）。训练采用四阶段范式：姿态分词器训练、姿态-文本对齐预训练、视觉投影器预训练和指令微调。

### 姿态理解任务性能

在姿态理解任务上，UniPose展现出与专用模型相当甚至更优的性能，同时保持了统一框架的多任务能力。具体而言，在PoseScript数据集的姿态到文本检索任务上，UniPose取得了85.6的Top-1 R-Precision（Table 2），虽略低于专用模型PoseScript的91.6，但考虑到UniPose同时支持六种其他任务，这一差距是可接受的。在PoseFix的姿态差异描述任务上，UniPose以67.9的Top-1 R-Precision超越了专用模型PoseFix的64.6，提升3.3个百分点。

![[assets/figures/papers/paper_list_l1869_UniPose_A_Unified_Multimodal_Framework_for_Human_Pose_Comprehension_Gene/figures/005_Table_2.jpg]]
*Table 2: Comparisons on pose comprehension tasks. We compare the pose-retrieval precision (R-Precision) and linguistic metrics on various datasets. UniPose † represents training UniPose on the single corresponding task*

值得关注的是，在图像到文本描述任务（ImageScript）上，UniPose取得了24.5的Top-1 R-Precision，显著优于GPT4V的17.7（+6.8），验证了姿态专用视觉编码器对细粒度姿态感知的关键作用。Figure 4的定性示例进一步表明，UniPose能够准确感知图像中人物的朝向信息，而通用视觉语言模型常出现方向性错误。

### 文本到姿态生成与姿态编辑性能

在文本到姿态生成任务上（Table 3），UniPose在PoseScript数据集上取得了73.7的Top-5 R^{T2P}，与专用模型PoseScript的73.3基本持平。在重建精度方面，UniPose的MPJPE为308.6，优于PoseScript的318.0（-9.4），表明离散姿态token在保持语义一致性的同时，能够有效保留3D姿态的几何精度。

![[assets/figures/papers/paper_list_l1869_UniPose_A_Unified_Multimodal_Framework_for_Human_Pose_Comprehension_Gene/figures/006_Table_3.jpg]]
*Table 3: Comparisons on Text-to-Pose generation task. The retrieval and reconstruction metrics are reported on PoseScript [14] dataset*

在姿态编辑任务上（Table 5），UniPose能够根据文本指令对输入姿态进行修正，其重建指标在PoseFix数据集上表现出竞争力。编辑任务的核心挑战在于模型需要同时理解原始姿态、修正指令，并生成符合指令的修正姿态，这要求姿态token之间的双向信息交互。

![[assets/figures/papers/paper_list_l1869_UniPose_A_Unified_Multimodal_Framework_for_Human_Pose_Comprehension_Gene/figures/009_Table_5.jpg]]
*Table 5: Comparisons on pose editing task. Reconstruction metrics are reported on PoseFix [13] dataset*

### 姿态估计性能

在姿态估计任务上（Table 4），UniPose作为通用多模态框架，在3DPW数据集上取得了94.7的MPJPE，在Human3.6M上取得了69.2的MPJPE。虽然与专用回归方法TokenHMR（3DPW上67.5）仍有差距，但UniPose显著优于其他多模态大语言模型方法——在3DPW上相比ChatPose的163.6降低了68.9（降幅达42.1%），在Human3.6M上相比ChatPose的126.0降低了56.8。这一结果表明，姿态专用视觉编码器的引入大幅缩小了通用MLLM与专用姿态估计方法之间的性能鸿沟。

![[assets/figures/papers/paper_list_l1869_UniPose_A_Unified_Multimodal_Framework_for_Human_Pose_Comprehension_Gene/figures/007_Table_4.jpg]]
*Table 4: Comparisons on pose estimation task. Reconstruction metrics are reported on the 3DPW and Human3.6M datasets*

### 消融实验

#### 混合视觉编码器的关键作用

Table 6的消融实验系统验证了视觉处理器各组件的贡献。将CLIP视觉编码器替换为姿态专用ViT（Pose-ViT）后，模型在所有姿态理解指标上均获得显著提升，证实了姿态估计预训练对于捕获细粒度姿态细节的必要性。仅使用CLIP视觉编码器时，模型在图像到文本任务上的性能明显受限，这解释了为何通用视觉语言模型（如GPT4V、LLaVA）在姿态相关任务上表现不佳——它们的视觉编码器缺乏对3D人体结构的专门感知能力。

#### 混合注意力机制的权衡

Table 7的消融实验揭示了混合注意力机制的深层权衡。在文本到姿态生成任务上，双向注意力将Top-1检索精度从9.0提升至13.8（提升53.3%），同时将推理延迟从2.5秒大幅降至0.2秒（加速12.5倍），这是因为双向注意力允许所有姿态token并行生成，而非逐token自回归解码。然而，在姿态描述生成任务上，混合注意力导致BLEU-4指标略有下降。这一现象可能源于：姿态token的双向注意力虽然增强了姿态内部的语义一致性，但可能干扰了文本token的因果生成过程，导致语言流畅性轻微受损。这提出了一个开放问题：如何设计注意力机制以同时优化姿态生成质量和文本生成质量。

#### 多任务联合训练的知识迁移

单任务训练与多任务联合训练的对比实验表明，多任务联合训练在所有任务上均优于单任务训练，验证了统一框架内部存在有效的知识迁移。例如，姿态理解任务中学习到的细粒度语义表征能够辅助姿态生成任务，而姿态编辑任务中学习到的姿态间差异建模能力则反向增强了姿态差异描述的性能。

### 零样本能力分析

Figure 5展示了UniPose的一项涌现能力：通过输入姿态描述文本，可以增强姿态估计的准确性。这一零样本迁移能力源于训练过程中姿态-文本对齐预训练阶段建立的跨模态语义关联——模型学会了将文本描述中的语义概念（如“左手抬起”）与姿态token中的对应几何模式相关联，从而在推理时利用文本信息约束姿态估计的解空间。这种能力的内部机制仍有待深入研究。

### 局限性与失败模式

尽管UniPose在统一多任务框架方面取得了显著进展，但仍存在以下局限：

1. **与专用姿态估计方法的差距**：在3DPW上，UniPose的MPJPE（94.7）与专用方法TokenHMR（67.5）之间存在27.2的差距。这一差距可能源于冻结的视觉编码器限制了精细姿态特征的提取能力——专用方法可以对视觉编码器进行端到端微调以适应姿态估计任务，而UniPose为了保持多任务能力，冻结了视觉编码器参数。

2. **训练流程的复杂性**：四阶段训练范式需要大量多任务数据，且需额外训练姿态分词器，增加了训练流程的工程复杂度。姿态分词器的重建精度直接影响下游任务的性能上限。

3. **注意力机制的固有冲突**：混合注意力在提升姿态生成质量的同时损害了文本生成质量，表明当前设计尚未完全解决文本与姿态两种模态在注意力模式上的本质冲突。

4. **姿态分词器的表示保真度**：将连续3D姿态量化为离散token的过程不可避免地引入信息损失，对于极端或复杂姿态，离散token可能无法完全保留精细的关节角度信息。

### 补充图表

![[assets/figures/papers/paper_list_l1869_UniPose_A_Unified_Multimodal_Framework_for_Human_Pose_Comprehension_Gene/figures/002_Table_1.jpg]]
*Table 1: Comparison of recent methods across various pose comprehension, generation and editing tasks*

![[assets/figures/papers/paper_list_l1869_UniPose_A_Unified_Multimodal_Framework_for_Human_Pose_Comprehension_Gene/figures/010_Table_7.jpg]]
*Table 7: Ablation study on different attention mechanisms*

![[assets/figures/papers/paper_list_l1869_UniPose_A_Unified_Multimodal_Framework_for_Human_Pose_Comprehension_Gene/figures/011_Figure_5.jpg]]
*Figure 5: Enhance pose estimation with input pose description*

![[assets/figures/papers/paper_list_l1869_UniPose_A_Unified_Multimodal_Framework_for_Human_Pose_Comprehension_Gene/figures/021_Figure_5.jpg]]
*Figure 5: Qualitative comparison on reasoning-based pose estimation task. We evaluate the model’s reasoning capabilities in multi-person images*



## 定位与知识库关联

### 1. 任务统一性定位：从专用模型到通用框架

人体姿态理解、生成与编辑长期由专用模型分别处理。**PoseScript** 专注于姿态描述生成（Pose-to-Text），**PoseFix** 专注于姿态差异描述与编辑（Pose-Diff），两者均采用检索-排序范式，在各自任务上表现优异（例如 PoseScript 在 Pose-to-Text 上达到 91.6 R-Precision Top-1），但无法跨任务迁移。**ChatPose** 首次将姿态生成引入大语言模型框架，支持文本到姿态生成，但在姿态估计上 MPJPE 高达 163.6（3DPW）和 126.0（Human3.6M），细粒度感知能力薄弱。**ChatHuman** 扩展了多模态人体对话能力，但任务覆盖仍不完整。通用多模态大语言模型如 **LLaVA**、**Qwen-VL** 和 **GPT4V** 虽具备强大的视觉-语言对齐能力，但在姿态相关的细粒度语义捕捉上表现不足——例如 GPT4V 在 Image-to-Text 任务上仅取得 17.7 R-Precision Top-1，远低于 UniPose 的 24.5。

**UniPose 的核心定位**：首次在统一框架中集成七种姿态理解、生成与编辑核心任务（Table 1），包括单姿态描述、姿态差异描述、文本到姿态生成、图像到姿态生成、姿态估计、姿态编辑以及基于推理的姿态估计。这一统一性并非简单的任务堆砌，而是通过将 3D 姿态量化为离散 token 并纳入 LLM 共享词汇表，使得姿态与文本在同一个自回归框架中无缝融合。

### 2. 技术架构谱系：VQ-VAE 离散化 + 混合视觉编码 + 混合注意力

UniPose 的技术架构可沿三条线索定位：

**（1）姿态离散化谱系**：姿态分词器基于 **VQ-VAE** 将连续 3D SMPL 姿态参数压缩为离散 token 序列，这一思路与 **TokenHMR** 等基于 token 的姿态估计方法共享离散化理念，但 UniPose 的离散化目标并非仅服务于姿态估计，而是将姿态 token 作为 LLM 的输入/输出单元，使姿态生成与编辑成为条件自回归生成问题。量化过程通过最近邻查找将潜在向量 $\widehat{\boldsymbol{z}}$ 映射为码本条目（Eq. 1），再将码本索引 $\mathbf{u}$ 作为离散姿态 token（Eq. 2），训练目标包含重建损失、嵌入损失和承诺损失（Eq. 7）。

**（2）视觉编码器谱系**：通用 MLLM（如 LLaVA）通常仅依赖 CLIP 视觉编码器，这导致姿态细节感知不足。UniPose 引入**混合视觉编码器**（mixture-of-visual-encoders），在 CLIP-ViT 基础上并行接入一个在姿态估计任务上预训练的**姿态专用 ViT**。消融实验（Table 6）证实，加入 Pose-ViT 在所有姿态理解指标上均有显著提升——这是 UniPose 在 Image-to-Text 任务上超越 GPT4V（+6.8）的关键因素。但需注意，该 Pose-ViT 被冻结，这可能是 UniPose 在姿态估计上与专用回归方法（如 HMR2.0 在 3DPW 上 MPJPE 67.5 vs UniPose 94.7）仍有差距的原因之一。

**（3）注意力机制谱系**：标准 LLM 对所有 token 使用因果注意力，但姿态 token 之间不存在严格的时序依赖。UniPose 提出**混合注意力**：文本 token 使用因果注意力，姿态 token 使用双向注意力。这一设计在文本到姿态生成上将 Top-1 检索精度从 9.0 提升至 13.8，并将推理延迟从 2.5 秒降至 0.2 秒（Table 7），因为双向注意力支持所有姿态 token 单步并行生成。然而，混合注意力在姿态描述任务上 BLEU-4 略有下降——这一“跷跷板效应”的深层原因尚待探究。

### 3. 训练范式定位：四阶段渐进对齐

UniPose 的训练分为四个阶段（Figure 3）：姿态分词器训练、姿态-文本对齐预训练、视觉投影器预训练、指令微调。这一多阶段策略与当前 MLLM 的主流训练范式（如 LLaVA 的两阶段训练）一脉相承，但增加了姿态-文本对齐的独立阶段，确保离散姿态 token 与文本 token 在嵌入空间中先行对齐，再接入视觉模态。多任务联合训练在所有任务上均优于单任务训练（Table 2 中 UniPose vs UniPose†），验证了统一框架内的知识迁移效应。

### 4. 适用边界与局限

**（1）姿态估计精度天花板**：作为通用 MLLM 方法，UniPose 在姿态估计上显著优于其他 MLLM（如 ChatPose 在 3DPW 上 -68.9 MPJPE），但仍落后于专用回归方法（如 HMR2.0 在 3DPW 上 -27.2 MPJPE）。冻结的视觉编码器可能限制了精细姿态特征的提取，这是通用框架与专用方法之间的固有张力。

**（2）训练流程复杂性**：四阶段训练需要大量多任务数据（附录 Table 1），且需额外训练姿态分词器和检索模型（BBC loss, Eq. 8），增加了工程复杂度。

**（3）混合注意力的任务间权衡**：双向注意力在提升姿态生成质量的同时轻微损害姿态描述性能，这一现象暗示姿态理解与生成可能对注意力模式有不同偏好，当前统一设计尚未完全解耦。

### 5. 开放问题

1. **姿态分词器的表示保真度**：离散 token 如何应对极端姿态、遮挡或多人场景下的姿态复杂度？码本大小与重建精度的权衡关系如何？
2. **混合注意力的内部机制**：为何双向注意力有利于生成却不利于理解？是否存在更优的注意力分配策略？
3. **零样本迁移机制**：从姿态描述到姿态估计的零样本增强（Figure 5）的内部机理是什么？LLM 是否隐式学习了文本-姿态的跨模态映射？
4. **视觉编码器融合**：如何更有效地整合 CLIP 和 Pose-ViT 的特征，以缩小与专用姿态估计方法的差距？是否需要对 Pose-ViT 进行端到端微调？



## 原文 PDF

![[paperPDFs/CVPR_2025/UniPose_A_Unified_Multimodal_Framework_for_Human_Pose_Comprehension_Generation_and_Editing.pdf]]
