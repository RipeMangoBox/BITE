---
title: "TOMGPT: Reliable Text-Only Training Approach for Cost-Effective Multi-modal Large Language Model"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/TOMGPT_Reliable_Text_Only_Training_Approach_for_Cost_Effective_Multi_modal_LLM.pdf
project_link: null
code_link: https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models/tree/Evaluation
aliases:
- TOMGPT
tags:
- arxiv_2025
- topic/other_unclear
- topic/other_unclear/general
core_operator: 在CLIP文本嵌入中加入高斯噪声以缓解模态差距，并采用两阶段纯文本训练范式（自监督预训练+指令微调），将对齐后的多模态嵌入空间映射到LLM的语义空间，从而仅通过替换编码器实现多模态推理。
primary_logic: 预训练的视觉-语言对比模型（CLIP）已具有耦合的共享嵌入空间；只需用纯文本数据训练一个投影模块，将文本嵌入映射到LLM的词嵌入空间，推理时将文本编码器替换为图像编码器，即可在不使用任何图像数据的情况下赋予LLM图像理解能力，大幅降低训练成本。
claims:
- TOMGPT在MME基准上感知总分951.44，认知总分262.14，显著优于基于图文对训练的LLaVA（502.82/214.64）并与Mini-GPT4（866.58/292.14）等模型相当或更优，证明纯文本训练方法的有效性。
- 在LVLM基准上TOMGPT总分198.93，在物体幻觉（70.67）和视觉常识（52.20）任务上表现突出，超越Mini-GPT4（192.62），显示其语义对齐能力。
- 消融实验表明，两阶段训练与添加高斯噪声显著提升MME分数（感知：951.44 vs 895.75；认知：262.14 vs 254.64），验证了模态差距缓解和训练范式的必要性。
- MME 上 Perception Total Score = 951.44
---

# TOMGPT: Reliable Text-Only Training Approach for Cost-Effective Multi-modal Large Language Model

> [!tip] 核心洞察
> 预训练的视觉-语言对比模型（CLIP）已具有耦合的共享嵌入空间；只需用纯文本数据训练一个投影模块，将文本嵌入映射到LLM的词嵌入空间，推理时将文本编码器替换为图像编码器，即可在不使用任何图像数据的情况下赋予LLM图像理解能力，大幅降低训练成本。

| 字段 | 内容 |
|------|------|
| 中文题名 | TOMGPT：面向高性价比多模态大语言模型的可靠纯文本训练方法 |
| 英文题名 | TOMGPT: Reliable Text-Only Training Approach for Cost-Effective Multi-modal Large Language Model |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2505.05606) · [paper](https://arxiv.org/abs/2306.13394) · [Code](https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models/tree/Evaluation) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | TOMGPT |
| Dataset | MME, LVLM |

> [!tip] 效果简介
> - MME 上，Perception Total Score 951.44 vs 866.58 (Mini-GPT4) (+84.86)；Cognition Total Score 262.14 vs 214.64 (LLaVA) (+47.50)。
> - LVLM 上，Overall Score 198.93 vs 192.62 (Mini-GPT4) (+6.31)；Object Hallucination 70.67 vs 50.67 (Mini-GPT4) (+20.00)。

## 概要

多模态大语言模型（MLLM）的研发长期受制于对海量、高质量图像-文本对数据的高度依赖，其采集与计算成本极其高昂，严重制约了模型的高效迭代与广泛应用。TOMGPT（ACM Transactions on Knowledge Discovery from Data, 2024）针对这一瓶颈，提出了一种**纯文本训练范式**：其核心洞察在于，预训练的视觉-语言对比模型（如CLIP）已经构建了一个耦合的共享嵌入空间，因此只需用纯文本数据训练一个投影模块，将该多模态对齐空间映射至大语言模型（LLM）的语义空间，推理时再将文本编码器替换为图像编码器，即可在不使用任何图像数据的情况下赋予LLM图像理解能力。

为实现这一目标，TOMGPT在CLIP文本嵌入中注入高斯噪声以缓解模态差距，并采用**两阶段训练策略**——第一阶段自监督预训练（指令为空，LLM预测输入文本），第二阶段指令微调——仅训练投影模块而冻结CLIP与LLM。实验表明，该方法在MME基准上取得感知总分951.44、认知总分262.14，显著优于基于图文对训练的LLaVA（Liu et al., NeurIPS 2023），并与Mini-GPT4（Zhu et al., ICLR 2024）等模型相当甚至更优；在LVLM基准上的物体幻觉任务中，TOMGPT得分70.67，远超Mini-GPT4的50.67。消融实验进一步验证了噪声注入与两阶段训练对性能的关键贡献，且整个训练过程仅需约2小时（8块A100），大幅降低了时间与数据成本。

该方法在方法谱系中定位于“**纯文本驱动的多模态对齐与投影**”，其训练时使用CLIP文本编码器、推理时切换至图像编码器的设计，使其区别于BLIP2（Li et al., ICML 2023）、mPLUG-Owl（Ye et al., arXiv 2023）等需要图文对训练的传统多模态模型。然而，TOMGPT在细粒度视觉理解任务（如计数、位置识别、文档细节）上表现较弱，且仅在7B规模的LLM上验证，向更大模型及其他模态的泛化能力仍待探索。

多模态大语言模型（MLLM）的快速发展使机器具备了同时理解视觉与语言的能力。然而，这一能力的获取代价高昂——当前主流MLLM的训练流程高度依赖海量、高质量的图像-文本对数据。例如，**BLIP2**（Li et al., ICML 2023）使用Q-Former连接图像编码器与LLM，**LLaVA**（Liu et al., NeurIPS 2023）借助GPT-4生成视觉指令数据进行微调，**Mini-GPT4**（Zhu et al., ICLR 2024）则冻结Q-Former并训练线性投影层。这些方法虽然在多模态理解上取得了显著进展，但图像-文本对的采集、清洗与存储成本极高，加之训练过程中图像编码的计算开销，严重制约了MLLM的高效研发与广泛普及。

**核心瓶颈**在于：现有范式将“图像数据”视为多模态能力获取的必要条件。这一假设导致训练成本与数据获取难度居高不下，使得资源受限的研究团队难以参与MLLM的迭代创新。

TOMGPT的提出正是为了打破这一瓶颈。其核心洞察源于一个被忽视的事实：预训练的视觉-语言对比模型（如CLIP）已经构建了一个耦合的共享嵌入空间，文本嵌入与图像嵌入在该空间中天然对齐。这意味着，**如果能够仅用纯文本数据训练一个投影模块，将CLIP的文本嵌入映射到LLM的词嵌入空间，那么在推理时只需将文本编码器替换为图像编码器，即可赋予LLM图像理解能力**——整个过程无需使用任何图像数据。

这一思路从根本上改变了多模态模型的训练范式：训练数据模态从“大量图像-文本对”转变为“纯文本数据”，训练时使用的编码器从“图像编码器”转变为“CLIP文本编码器”（推理时再替换为图像编码器）。通过在文本嵌入中注入高斯噪声以缓解模态差距，并采用两阶段纯文本训练策略（自监督预训练+指令微调），TOMGPT实现了与基于图文对训练的模型相当甚至更优的性能，同时将训练时间压缩至约2小时（8块A100），大幅降低了多模态大语言模型的研发门槛。

## 核心方法与创新机理

TOMGPT的核心创新在于**完全摒弃了对图像-文本对训练数据的依赖**，仅通过纯文本数据即可赋予大语言模型多模态理解能力。这一突破性设计围绕一个关键洞察展开：预训练的视觉-语言对比模型（如CLIP）已经构建了一个耦合的共享嵌入空间，文本嵌入与图像嵌入在语义上天然对齐。基于此，TOMGPT只需训练一个投影模块，将CLIP的文本嵌入映射到LLM的词嵌入空间，推理时直接将文本编码器替换为图像编码器，模型便获得了图像理解能力。

### 关键创新点

**1. 训练数据模态的根本性变革**

传统多模态大语言模型（如**BLIP2** (Li et al., ICML 2023)、**LLaVA** (Liu et al., NeurIPS 2023)、**Mini-GPT4** (Zhu et al., ICLR 2024)）的训练高度依赖海量高质量图像-文本对数据，数据采集与计算成本极高。TOMGPT将训练数据模态从“图像-文本对”替换为“纯文本数据”——具体包括GPT生成的自由格式文本（100万条）和少量指令数据（来自Alpaca数据集）。这一变革使得训练成本大幅降低：仅需约2小时（8块A100 GPU）即可完成训练，远少于需要图文对训练的同类模型（Table 6, Section 4.4）。

**2. 训练-推理编码器的非对称设计**

TOMGPT在训练和推理阶段使用不同的编码器，这是其方法论的标志性特征：
- **训练时**：使用CLIP文本编码器（$f_T$）对输入文本进行编码，得到与图像嵌入对齐的文本嵌入。
- **推理时**：将文本编码器替换为CLIP图像编码器（$f_I$），直接对输入图像进行编码。

这一设计的可行性根植于CLIP对比学习的本质——文本编码器和图像编码器在训练过程中已被强制映射到同一语义空间。TOMGPT仅需训练投影模块（Projection Module）来桥接CLIP嵌入空间与LLM词嵌入空间之间的差距，而CLIP编码器和LLM（Vicuna-7B）的参数全程冻结（Section 3.3）。

**3. 高斯噪声注入缓解模态差距**

尽管CLIP的文本嵌入与图像嵌入在语义上对齐，两者之间仍存在不可忽略的模态差距（modality gap）。TOMGPT提出了一种简洁有效的缓解策略：对归一化后的CLIP文本嵌入添加高斯噪声，并再次进行归一化处理（Section 3.2）。消融实验证实，这一操作显著提升了模型性能——MME感知分数从895.75提升至951.44，认知分数从254.64提升至262.14（Table 3, Section 4.4）。噪声注入迫使投影模块学习更具鲁棒性的映射，从而在推理时能够更好地适应来自图像编码器的嵌入分布。

**4. 两阶段纯文本训练范式**

TOMGPT采用自监督预训练与指令微调相结合的两阶段训练策略（Fig. 3, Section 3.3）：
- **第一阶段（预训练）**：指令为空，LLM直接预测CLIP文本编码器的输入文本。这迫使投影模块学习将CLIP文本嵌入准确映射到LLM能够理解的词嵌入空间，建立稳固的跨模态语义桥梁。
- **第二阶段（微调）**：指令为关于输入文本的问题，LLM预测对应答案。此阶段使模型习得遵循指令、生成合理响应的能力。

消融实验表明，两阶段训练相比仅预训练或仅微调均有显著提升（Table 3, Section 4.4），验证了该范式的必要性。第一阶段建立嵌入空间对齐的基础能力，第二阶段赋予模型指令遵循与任务泛化能力，两者协同作用。

### 与现有方法的本质区别

| 维度 | 传统MLLM（BLIP2/LLaVA/Mini-GPT4） | TOMGPT |
|------|-----------------------------------|--------|
| 训练数据 | 大量图像-文本对 | 纯文本（GPT生成 + 指令数据） |
| 训练编码器 | 图像编码器 | CLIP文本编码器 |
| 嵌入处理 | 直接投影原始嵌入 | 归一化 + 高斯噪声 + 再归一化 |
| 训练策略 | 单阶段或端到端微调 | 两阶段（自监督预训练 + 指令微调） |
| 可训练参数 | Q-Former/投影层/部分LLM | 仅投影模块（Q-Former + 线性层） |

TOMGPT的方法论本质上是一种**模态迁移学习**——通过在文本模态上训练投影模块，隐式地学习将多模态对齐空间映射到LLM语义空间的能力，从而在推理时实现对图像模态的零样本泛化。这一范式不仅大幅降低了数据获取与计算成本，还为多模态大语言模型的高效研发开辟了新路径。

TOMGPT的整体框架围绕一个核心假设展开：预训练的视觉-语言对比模型（如CLIP）已经构建了一个耦合的共享嵌入空间。因此，只需用纯文本数据训练一个投影模块，将该空间中的文本嵌入映射到大语言模型（LLM）的词嵌入空间，推理时将文本编码器替换为图像编码器，即可在不使用任何图像数据的情况下赋予LLM图像理解能力。这一设计将多模态模型的训练成本从“海量图文对采集与计算”压缩为“纯文本生成与轻量投影”，从根本上改变了MLLM的训练范式。

### 模块组成与数据流

框架由四个关键模块串联构成，形成训练与推理两条高度对称的流水线（Figure 2）：

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2505_05606/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our framework. The learning queries are a set of randomly initialized embeddings that can be updated during model training. We utilize OpenAi GPT-3.5 Turbo API to generate free-form yet diverse text training data from several seeds (we set N=1 million in our experiments). The text embeddings encoded by text encoder are projected into LLM’s word embedding space through cross-attention layers. These embeddings are concatenated with instructions, as input to LLM. During inference, the pipeline only replaces the text encoder with the corresponding image encoder*

1. **CLIP文本编码器（f_T）**：在训练阶段接收输入文本，输出与视觉嵌入对齐的文本嵌入向量。该编码器在整个训练过程中保持冻结，以保留其预训练获得的多模态对齐能力。
2. **高斯噪声注入**：对归一化后的文本嵌入添加高斯噪声，旨在缩小文本嵌入与图像嵌入之间的模态差距，并增强投影模块的鲁棒性。噪声注入是连接“文本训练”与“图像推理”的关键调控旋钮。
3. **投影模块（Projection Module）**：由一组可学习的查询向量（learnable queries）、交叉注意力层和线性投影层组成（采用Q-Former架构）。该模块将噪声增强后的文本嵌入映射到LLM的词嵌入空间，是框架中唯一需要训练的部分。推理时，该模块直接处理来自CLIP图像编码器（f_I）的图像嵌入，无需任何结构变更。
4. **大语言模型（Vicuna-7B）**：接收投影后的嵌入与指令嵌入的拼接结果，自回归生成文本响应。LLM同样保持冻结，仅作为语义解码器使用。

### 训练-推理对称性

框架的核心工程智慧在于训练与推理流程的对称设计。训练时，流水线为：

$$R_{pred} = f_{LLM}(concat[f_{PROJ}(f_T(T)), Emb(Instr)])$$

即文本T经文本编码器和投影模块处理后，与指令嵌入拼接，输入LLM预测响应，并通过交叉熵损失优化投影模块参数：

$$loss = CrossEntropyLoss(R_{gt}, R_{pred})$$

推理时，仅需将文本编码器替换为图像编码器f_I，其余模块完全复用：

$$R = f_{LLM}(concat[f_{PROJ}(f_I(I)), Emb(Instr)])$$

这种“训练用文本、推理用图像”的范式，使得模型在训练阶段完全无需接触图像数据，从而将数据采集成本降至近乎为零。

### 两阶段训练策略

投影模块的训练采用两阶段范式（Figure 3），以逐步建立文本嵌入到LLM语义空间的映射：

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2505_05606/figures/003_Figure_3.jpg]]
*Figure 3: Two-stage training and inference pipeline. In the pretraining stage, instruction is empty, and LLM predicts the input text of the CLIP text encoder. In the finetuning stage, instruction is a question about the input text, and LLM predicts the corresponding answer. The inference process is largely consistent with the training stage, with the sole exception being the replacement of the encoder*

- **第一阶段（自监督预训练）**：指令为空，LLM直接预测输入文本本身。此阶段使用由GPT-3.5 Turbo API迭代生成的100万条自由格式文本（Figure 4）以及从C4数据集中随机采样的句子，目标是让投影模块学会将CLIP文本嵌入忠实地“翻译”为LLM可理解的表示。
- **第二阶段（指令微调）**：指令为关于输入文本的问题，LLM需预测对应答案。此阶段使用经过过滤的Alpaca指令数据集，使模型获得遵循指令和生成合理响应的能力。

两阶段的递进设计确保了模型先掌握模态对齐的基本能力，再习得指令遵循的交互能力。消融实验证实，单独使用任一阶段均会导致MME感知和认知得分显著下降（Table 3），验证了该训练范式的必要性。

TOMGPT 的核心架构围绕一个关键洞察展开：预训练的视觉-语言对比模型（CLIP）已经构建了一个耦合的共享嵌入空间。因此，训练时无需使用图像数据，只需用纯文本训练一个投影模块，将 CLIP 文本嵌入映射到大语言模型（LLM）的词嵌入空间；推理时将文本编码器替换为图像编码器，即可赋予 LLM 图像理解能力。

### 关键模块

**1. CLIP 文本编码器 $f_T$ 与图像编码器 $f_I$**
这两个编码器均来自预训练的 CLIP 模型，在整个训练过程中参数被冻结。训练阶段仅使用文本编码器 $f_T$ 将输入文本编码为多模态对齐的文本嵌入；推理阶段则切换为图像编码器 $f_I$，将输入图像编码为与文本嵌入处于同一语义空间的图像嵌入（Section 3.1, Fig. 2）。

**2. 高斯噪声注入**
在将文本嵌入送入投影模块之前，先对其进行归一化处理，随后添加高斯噪声，并再次归一化。这一操作旨在模拟图像嵌入的分布特性，缩小文本嵌入与图像嵌入之间的模态差距（modality gap），同时增强模型的鲁棒性。消融实验证实，添加高斯噪声可使 MME 感知得分从 895.75 提升至 951.44（Section 3.2, Table 3）。

**3. 投影模块 $f_{PROJ}$（Q-Former + 线性投影）**
投影模块是 TOMGPT 中唯一需要训练的部分。它由一组随机初始化的可学习查询嵌入（learnable queries）与交叉注意力层（Q-Former）组成，后接一个线性投影层。其功能是将 CLIP 文本嵌入（或推理时的图像嵌入）映射到 LLM 的词嵌入空间。消融实验表明，使用 Q-Former 作为投影模块优于纯线性层或 MLP，在 MME 感知任务上取得最高分 951.44（Section 3.2, Table 4）。

**4. 大语言模型（Vicuna-7B）**
LLM 接收投影模块输出的嵌入与指令嵌入的拼接结果，自回归地生成文本响应。LLM 的参数在整个训练过程中同样被冻结（Section 3.1, Section 3.2）。

### 关键公式

**训练阶段预测公式**
$$R_{pred} = f_{LLM}(concat[f_{PROJ}(f_T(T)), Emb(Instr)])$$
其中 $T$ 为输入文本，$Instr$ 为指令，$f_T$ 为 CLIP 文本编码器，$f_{PROJ}$ 为投影模块，$Emb$ 为 LLM 的词嵌入层，$f_{LLM}$ 为大语言模型，$R_{pred}$ 为预测响应。该公式描述了从纯文本输入到模型预测输出的完整前向流程（Equation (1), Section 3.1）。

**训练损失函数**
$$loss = CrossEntropyLoss(R_{gt}, R_{pred})$$
训练目标是最小化真实响应 $R_{gt}$ 与预测响应 $R_{pred}$ 之间的交叉熵损失（Equation (2), Section 3.1）。

**推理阶段生成公式**
$$R = f_{LLM}(concat[f_{PROJ}(f_I(I)), Emb(Instr)])$$
推理时，文本编码器 $f_T$ 被替换为图像编码器 $f_I$，对输入图像 $I$ 和指令 $Instr$ 生成响应 $R$。这是 TOMGPT 实现“文本训练、图像推理”的核心机制（Equation (3), Section 3.1）。

**自回归概率分解**
$$P(x_{L+1}, \dots, x_{L+n}) = \prod_{t=1}^{n} P(x_{L+t} \mid x_{prefix}, x_{L+1}, \dots, x_{L+t-1})$$
该公式描述了 LLM 自回归生成 $n$ 个后续 token 的条件概率分解，条件为前缀 token $x_{prefix}$ 和已生成的 token 序列。这是 LLM 生成文本的标准数学表述（Equation (4), Section 3.2）。

## 实验与关键发现

### 主要结果：纯文本训练的竞争力验证

TOMGPT在两大主流多模态基准上的表现证明，纯文本训练范式能够达到与依赖海量图文对训练的模型相当甚至更优的水平。其核心优势源于CLIP共享嵌入空间的充分利用，以及两阶段训练与噪声注入对模态差距的有效缓解。

**MME基准（Table 1）** 上，TOMGPT感知总分达951.44，认知总分达262.14。这一结果显著超越了使用图文对训练的**LLaVA**（Liu et al., NeurIPS 2023，感知502.82/认知214.64），并与**Mini-GPT4**（Zhu et al., ICLR 2024，感知866.58/认知292.14）互有胜负。值得注意的是，TOMGPT在认知子任务上虽略低于Mini-GPT4，但其感知能力的大幅领先（+84.86）表明，纯文本训练在建立基础视觉语义映射方面具有出人意料的效能。与**mPLUG-Owl**（Ye et al., arXiv 2023）和**LLaMA-Adapter-V2**（Gao et al., arXiv 2023）等同期模型相比，TOMGPT同样表现出可比拟的综合能力。

**LVLM基准（Table 2）** 进一步揭示了TOMGPT的独特优势。模型在物体幻觉（Object Hallucination）任务上得分70.67，远超Mini-GPT4的50.67（+20.00），在视觉常识推理（Visual Commonsense）上也取得52.20的优异表现。这一结果暗示，纯文本训练可能天然地抑制了视觉-语言模型常见的“幻觉”倾向——由于训练过程中从未接触图像，投影模块必须学习将文本嵌入映射到LLM语义空间中一个更“泛化”的区域，而非过度拟合特定的视觉模式。TOMGPT的LVLM总分198.93，超越Mini-GPT4（192.62），进一步巩固了其竞争力。

综合来看，TOMGPT在不使用任何图像数据的前提下，仅凭GPT生成的自由文本和少量指令数据，便在两个核心基准上达到了与主流多模态模型相当的性能。这构成了该工作最具说服力的实证支撑。

### 消融实验：关键设计选择的作用机制

消融实验系统性地验证了TOMGPT三大核心设计要素的必要性与贡献度。

**两阶段训练范式（Table 3）**：仅进行预训练（自监督预测输入文本）或仅进行指令微调，均导致性能显著下降。完整的两阶段流程（预训练+微调）在MME感知上取得951.44，而仅预训练和仅微调的变体分别降至895.75和更低分数。这一对比表明：第一阶段的自监督预训练建立了CLIP嵌入空间到LLM词嵌入空间的基础映射，使投影模块学会“翻译”多模态嵌入；第二阶段的指令微调则赋予模型遵循人类指令的能力，二者缺一不可。

**高斯噪声注入（Table 3）**：向归一化后的文本嵌入添加高斯噪声，将MME感知分数从895.75提升至951.44（+55.69），认知分数也有相应改善。这一操作的核心机制是：在训练时模拟图像嵌入相对于文本嵌入的分布偏移，迫使投影模块学习对模态差异具有鲁棒性的映射。噪声充当了“模态差距的正则化器”，使推理时替换为图像编码器后，投影模块仍能产生有效的LLM输入。

**投影模块架构（Table 4）**：对比线性层、MLP和Q-Former三种投影结构，Q-Former在MME感知上取得最高分951.44。Q-Former的交叉注意力机制与可学习查询（learnable queries）的组合，提供了比简单前馈网络更强的跨模态信息压缩与对齐能力。进一步消融显示（Fig. 7），设置32个可学习查询token能在感知与认知性能之间取得最佳平衡——过少的token信息瓶颈过紧，过多的token则可能引入冗余噪声。

**预训练数据构成（Table 5）**：单独使用ChatGPT生成文本或C4网页抓取文本均不如二者联合使用。混合数据源在MME感知上达到974.75，优于任一单一来源。ChatGPT文本提供了流畅、结构化的语言模式，C4文本则贡献了真实世界的多样性与噪声，二者的互补性增强了投影模块的泛化能力。

**训练效率（Table 6）**：TOMGPT在8块A100 GPU上的训练时间仅约2小时，且所需图文对数据量为零。相比之下，BLIP2、LLaVA等模型需要数百万图文对和数倍于TOMGPT的训练时间。这一效率优势直接源于纯文本训练范式的设计——文本数据的获取与处理成本远低于图文对，且无需加载高分辨率图像带来的计算开销。

### 失败模式与局限性

尽管TOMGPT在整体基准上表现亮眼，但论文明确指出其在需要细粒度视觉理解的场景中存在系统性不足。具体表现为：

1. **计数与空间定位能力薄弱**：MME基准的Count和Position子任务得分相对较低。这是因为CLIP图像编码器将整张图像压缩为单一的768维全局向量，丢失了局部区域的空间信息和物体边界。投影模块无法从这一压缩表示中恢复精确的位置或数量信号。

2. **文档与OCR任务性能受限**：同样受限于全局编码的粒度，TOMGPT在识别图像中的文字、解析文档结构等任务上表现不佳。这类任务通常需要像素级或区域级的特征，而TOMGPT的架构缺乏相应的多尺度或局部注意力机制。

3. **认知评估的统计可靠性**：MME认知测试的图像数量有限，导致认知得分的方差较高。因此，认知子任务上的数值比较（如与Mini-GPT4的差距）需要谨慎解读，差异可能部分源于测试集的统计波动而非模型能力的本质差异。

4. **未探索的扩展性边界**：所有实验均在7B规模的Vicuna LLM上进行，投影模块的Q-Former权重从零开始随机初始化（未使用BLIP2的预训练权重）。这既是优点（证明了方法的自足性），也意味着更大规模LLM或预训练投影模块可能带来的性能增益尚未被量化。

这些失败模式共同指向一个根本性瓶颈：CLIP嵌入的信息压缩率。如何在保持纯文本训练低成本优势的同时，引入更丰富的视觉特征表示，是该范式进一步突破的关键。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2505_05606/figures/005_Table_1.jpg]]
*Table 1: Comparison with State-of-the-art Multi-modal Large Language Models on MME Benchmark, Here Highlight for the Best and Underline for the Second Best Results*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2505_05606/figures/006_Table_2.jpg]]
*Table 2: Comparison with State-of-the-art Multi-modal Large Language Models on LVLM Benchmark, Here Highlight for the Best and Underline for the Second Best Results*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2505_05606/figures/009_Table_3.jpg]]
*Table 3: Ablation Study on the Two-stage Training Paradigm and Adding Noise to Text Embedding*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2505_05606/figures/010_Table_4.jpg]]
*Table 4: Ablation Study on the Projection Module and Large Language Model*

## 定位与知识库关联

### 核心范式定位：纯文本驱动的多模态对齐投影

TOMGPT 提出了一种与主流多模态大语言模型（MLLM）截然不同的训练范式。传统 MLLM 的核心瓶颈在于对海量高质量图像-文本对数据的强依赖，导致数据采集与计算成本极高。TOMGPT 的核心洞察在于：预训练的视觉-语言对比模型（如 CLIP）已经构建了一个耦合的共享嵌入空间，因此无需在训练阶段引入任何图像数据。该方法仅使用纯文本数据训练一个投影模块，将 CLIP 文本嵌入映射到大语言模型（LLM）的词嵌入空间；推理时，只需将文本编码器替换为图像编码器，即可赋予 LLM 图像理解能力。这一范式将多模态对齐问题转化为一个纯文本空间到 LLM 语义空间的映射问题，从根本上绕开了对图像-文本对的需求。

### 与现有 MLLM 的方法论对比

TOMGPT 与当前主流 MLLM 在训练数据、编码器使用、嵌入处理流程和训练策略四个维度上存在根本性差异。以下从这些维度进行系统性对比，并标注具体基线工作的出处。

| 维度 | 传统 MLLM 基线 | TOMGPT 方案 |
|------|---------------|-------------|
| **训练数据** | 大量图像-文本对（如 **BLIP2** (Li et al., ICML 2023)、**LLaVA** (Liu et al., NeurIPS 2023)、**Mini-GPT4** (Zhu et al., ICLR 2024)） | 纯文本数据：GPT 生成的无格式文本 + 少量指令数据（Alpaca） |
| **训练时编码器** | 图像编码器（CLIP 视觉编码器） | CLIP 文本编码器（推理时替换为图像编码器） |
| **嵌入处理** | 直接投影原始嵌入 | 归一化 → 加高斯噪声 → 再次归一化 → 投影 |
| **训练策略** | 单阶段或端到端指令微调 | 两阶段：自监督预训练（指令为空，预测输入文本）→ 指令微调 |

具体而言，**BLIP2** (Li et al., ICML 2023) 使用 Q-Former 连接冻结的图像编码器与 LLM，依赖大量图文对进行训练；**LLaVA** (Liu et al., NeurIPS 2023) 利用 GPT-4 生成视觉指令数据进行端到端微调；**Mini-GPT4** (Zhu et al., ICLR 2024) 则冻结 Q-Former 并仅训练线性投影层，但同样需要高质量图文对齐数据。相比之下，TOMGPT 的投影模块（Q-Former + 线性层）完全从零开始随机初始化，仅通过文本数据学习将 CLIP 嵌入空间映射到 LLM 词嵌入空间，训练时间仅约 2 小时（8 块 A100），远低于需要图文对训练的模型（Table 6, Section 4.4）。

### 方法的关键创新点与因果机制

TOMGPT 的方法设计围绕一个因果调节变量展开：**在 CLIP 文本嵌入中注入高斯噪声以缓解模态差距**。CLIP 的文本嵌入和图像嵌入虽然共享同一潜在空间，但存在天然的模态差距（modality gap）。若直接投影文本嵌入，模型在推理时切换到图像嵌入时会产生分布偏移。通过在归一化后的文本嵌入上添加高斯噪声并再次归一化，TOMGPT 有效缩小了训练与推理时的嵌入分布差异，增强了投影模块的跨模态鲁棒性。消融实验（Table 3, Section 4.4）表明，添加噪声后 MME 感知得分从 895.75 提升至 951.44，认知得分从 254.64 提升至 262.14，验证了这一机制的必要性。

两阶段训练范式同样至关重要。第一阶段的自监督预训练（指令为空，LLM 预测 CLIP 文本编码器的输入文本）使投影模块学会将 CLIP 嵌入映射到 LLM 能理解的语义空间；第二阶段的指令微调则让模型适应问答格式。消融实验表明，仅预训练或仅微调均显著弱于两阶段方案，验证了该训练范式的必要性。

### 适用边界与局限性

尽管 TOMGPT 在多个基准上取得了与图文对训练模型相当甚至更优的性能，但其方法存在明确的适用边界：

1. **细粒度视觉理解能力不足**：模型在需要精确定位、计数、文档细节理解等任务上表现较差。这源于 CLIP 图像编码器将图像压缩为单一全局向量（768 维），丢失了局部细节信息。该瓶颈是 CLIP 架构的固有局限，而非训练范式本身的问题。

2. **认知评估的统计可靠性受限**：MME 认知评估的测试图像数量有限，导致认知得分的方差较高，分析价值受到一定制约。

3. **文本数据的多样性与真实性边界**：预训练文本主要来自 ChatGPT 生成和 C4 语料，其多样性与真实性受限于语言模型的能力和网页数据的质量。结合更多样化的文本源或弱监督图像-文本对可能进一步提升性能。

4. **投影模块的初始化策略**：TOMGPT 未使用 BLIP2 预训练的 Q-Former 权重，投影模块从零开始随机初始化，可能未充分发挥潜在性能。

5. **模型规模的验证范围**：当前仅在 7B 规模的 Vicuna 上验证，扩展到更大模型（如 13B、33B）时的训练稳定性与效果未知。

### 开放问题与未来方向

TOMGPT 开辟了纯文本训练 MLLM 的新路径，但以下关键问题有待探索：

1. **模态差距的进一步压缩**：如何设计更精细的噪声注入策略或对抗性训练方法，以进一步缩小 CLIP 的模态差距，从而提升细粒度视觉信息的迁移能力？

2. **跨模态泛化能力**：这种“训练用文本、推理用图像”的范式能否推广至视频、音频等其他模态？若能，将极大降低多模态模型的训练门槛。

3. **投影架构的改进**：当前 Q-Former 使用固定数量的学习查询（32 个），能否设计多尺度交叉注意力或层级化投影架构来保留更丰富的图像特征，从而突破单一全局向量的信息瓶颈？

4. **纯文本训练的性能极限**：纯文本训练的 MLLM 在大规模、复杂多模态任务下的性能上限在哪里？随着 LLM 规模的增长，纯文本训练是否能持续缩小与图文对训练模型的差距？

5. **语言模型偏见的系统性引入**：仅依赖文本数据是否会系统性地引入语言模型固有的文化、性别等偏见？如何量化与缓解这种偏见的跨模态迁移？论文未对训练数据或模型中的潜在社会偏见进行系统性评估，这一问题需要进一步研究。

## 原文 PDF

![[paperPDFs/arxiv_2025/TOMGPT_Reliable_Text_Only_Training_Approach_for_Cost_Effective_Multi_modal_LLM.pdf]]
