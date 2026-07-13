---
title: Latent Implicit Visual Reasoning
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Latent_Implicit_Visual_Reasoning.pdf
project_link: "https://www.chuyishang.com/livr/"
code_link: "https://thinkingmachines.ai/blog/lora/"
aliases:
- LIVRL
- LIVR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过引入可学习的隐式token并施加视觉瓶颈注意力掩码，迫使模型将任务相关的视觉信息压缩到隐式token中，实现无显式监督的隐式视觉推理。
primary_logic: 视觉瓶颈机制能够端到端地训练模型发现和使用隐式视觉表征，避免手工设计中间步骤，从而使视觉推理更灵活、可扩展，适用于多种感知密集型任务。
claims:
- LIVR在九个视觉中心任务上一致超越直接监督微调（Direct SFT），在Qwen2.5-VL-3B上平均提升6.24%。
- 消融实验表明，隐式token和视觉瓶颈二者缺一不可，仅添加token而不做瓶颈训练无法带来性能提升。
- 在外部基准（VSP, SAT, BLINK, MMVP）上，LIVR无需任何显式中间监督，性能达到或超越当前最佳方法。
- 9视觉任务综合 (Qwen2.5-VL-3B) 上 平均准确率 = 67.85
---

# Latent Implicit Visual Reasoning

> [!tip] 核心洞察
> 视觉瓶颈机制能够端到端地训练模型发现和使用隐式视觉表征，避免手工设计中间步骤，从而使视觉推理更灵活、可扩展，适用于多种感知密集型任务。

| 字段 | 内容 |
|------|------|
| 中文题名 | 隐式潜在视觉推理 |
| 英文题名 | Latent Implicit Visual Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.21218) · [Project](https://www.chuyishang.com/livr/) · [Code](https://thinkingmachines.ai/blog/lora/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Latent Implicit Visual Reasoning (LIVR) |
| Dataset | 9视觉任务综合, SAT Val, MMVP, V* |

> [!tip] 效果简介
> - 9视觉任务综合 (Qwen2.5-VL-3B) 上，平均准确率 67.85 vs 61.61 (Direct SFT) (+6.24)。
> - 9视觉任务综合 (Qwen3-VL-4B) 上，平均准确率 77.55 vs 74.12 (Direct SFT) (+3.43)。
> - 多任务联合训练 (Qwen3-VL-4B, 6任务) 上，平均准确率 72.37 vs 69.60 (Direct SFT) (+2.77)。

## 概要

**问题瓶颈**：当前大型多模态模型（LMMs）的推理过程以文本为中心，难以形成复杂的视觉抽象。现有方法试图通过显式的中间视觉监督（如边界框、深度图、辅助图像）来弥补这一缺陷，但这类方案泛化性差、标注成本高昂，且在推理步骤本身难以定义时往往失效。

**核心方案**：本文提出**隐式潜在视觉推理（Latent Implicit Visual Reasoning, LIVR）**——一种任务无关的机制，通过向LMM引入可学习的隐式token并施加视觉瓶颈注意力掩码，迫使模型将任务相关的视觉信息压缩到隐式token中，从而在无需任何显式中间监督的条件下端到端地学习视觉推理。

**主要结果**：LIVR在九个以感知为核心的任务上一致超越直接监督微调（Direct SFT），在Qwen2.5-VL-3B上平均提升**6.24%**，在Qwen3-VL-4B和LLaVA-OneVision-1.5上分别提升**3.43%**和**5.60%**。在外部基准测试中，LIVR无需显式中间监督即达到或超越当前最佳方法：在SAT Val上达到**85.6%**（ViGoRL-3B为62.9%），在MMVP上达到**75.3%**（LVR-7B为71.7%），在VSP上达到**66.0%**（Mirage为46.0%）。消融实验证实，隐式token和视觉瓶颈二者缺一不可，且模型确实在推理中依赖隐式token——移除后准确率从83.61%骤降至76.23%。

**方法定位**：LIVR属于隐式视觉推理范式，与依赖文本链式思维（如ViGoRL）或显式视觉中间表示（如Mirage、LVR）的方法形成互补或替代关系。其核心贡献在于证明：通过精心设计的注意力瓶颈与可学习隐式表征，模型能够自主发现对任务有用的视觉结构，而无需人类手工设计中间步骤。

大型多模态模型（LMMs）在视觉理解任务上取得了显著进展，但其推理过程仍以文本为中心。当面对需要精细视觉感知的任务——例如判断两幅图像中对应点的语义匹配、在复杂场景中计数物体、或比较多个候选区域与参考图像的相似度——纯文本输出通道难以承载完整的视觉信息，容易引入歧义。这一瓶颈的根源在于：**标准LMM将视觉输入编码后直接送入语言模型解码，模型缺乏一个结构化的内部空间来形成复杂的视觉抽象**。

现有方法试图通过引入中间视觉监督来弥补这一缺陷。例如，一些工作让模型显式输出边界框坐标、深度图、分割掩码或辅助渲染图像，作为最终答案的推理步骤。然而，这类策略面临两个根本性困难：（1）**泛化性受限**——手工设计的中间表示高度依赖任务特性，难以迁移到新场景；（2）**标注成本高昂**——获取精确的中间监督信号（如像素级对应关系、三维空间关系标注）远比收集问答对困难。更关键的是，许多视觉推理任务的“中间步骤”本身难以被人类清晰定义——当人类判断两幅图像的相似性时，我们并不显式地列举特征点或计算几何变换，而是在隐式的视觉表征空间中完成比较。

上述困境指向一个核心需求：**能否让模型端到端地学习隐式的视觉推理表征，而无需任何显式的中间监督？** 这正是本文提出 Latent Implicit Visual Reasoning（LIVR）的出发点。LIVR 通过在 LMM 中引入可学习的隐式 token，并施加视觉瓶颈注意力掩码，迫使模型将任务相关的视觉信息压缩到隐式 token 中，从而实现无显式监督的隐式视觉推理。这一机制使模型能够自动发现对解题有用的视觉结构，而不依赖人类预设的推理路径。

## 核心方法与创新机理

### 问题瓶颈：文本中心的视觉推理困境

大型多模态模型（LMMs）在执行视觉推理任务时，本质上仍以文本为中心：它们将图像编码为视觉嵌入后直接送入语言模型，最终以文本形式输出答案。这一范式存在两个根本性缺陷：

1. **文本表达力受限**：许多视觉概念（如纹理相似度、空间布局、精细几何关系）难以用自然语言精确描述。当模型被要求判断“哪张图像与参考图最相似”时，纯文本输出无法捕捉所有视觉信息，容易引入歧义（见 Figure 1）。
2. **显式中间监督的不可扩展性**：现有改进方法（如 **Mirage** 生成辅助图像、**ViGoRL** 输出边界框坐标）依赖手工设计的显式中间视觉监督信号。这类方法不仅需要昂贵的标注成本，更根本的问题在于——当推理步骤本身难以被人类清晰定义时，显式监督就无从设计。

### 因果调节变量：隐式token + 视觉瓶颈

LIVR 的核心机制由两个相互依赖的组件构成，二者缺一不可：

**组件一：可学习的隐式token（Latent Tokens）**

在模型原有词汇表 $V$ 中新增 $K$ 个可学习的特殊token $\mathcal{L} = \{l_1, l_2, \cdots, l_K\}$，并将其嵌入行解冻。这些隐式token被附加在提示词之后，作为视觉信息的内部推理载体。与普通文本token不同，隐式token的语义完全由端到端任务的损失信号塑造，无需任何人工定义。

**组件二：视觉瓶颈注意力掩码（Bottleneck Attention Mask）**

这是 LIVR 最关键的机制创新。在训练的第一阶段（Stage 1），通过修改自回归模型的因果注意力掩码，强制实施如下约束：
- **答案token** 和 **提示token** 均不能直接关注图像token $I$，只能通过隐式token $\mathcal{L}$ 间接获取视觉信息。
- 这意味着所有任务相关的视觉特征必须被**压缩**到 $K$ 个隐式token中，形成信息瓶颈。

形式化地，给定图像 $I$ 和文本提示 $Q$，LMM 的前向传播为：

$$R = M(p(v(I)), l(Q))$$

其中 $v$ 为视觉编码器，$p$ 为投影器，$l$ 为文本嵌入。在 Stage 1 中，注意力掩码被修改为：答案token只能关注 $Q$ 和 $\mathcal{L}$，而不能关注 $I$。损失仅在答案token上计算标准负对数似然：

$$\mathcal{L} = -\frac{1}{|x|}\sum_{i=1}^{|x|}\log P(x_i \mid x_{<i})$$

### 核心洞察：端到端隐式视觉抽象的涌现

LIVR 的设计哲学在于**避免手工定义中间推理步骤**。传统方法需要人类预设“模型应该关注什么”（如边界框、深度图），而 LIVR 通过视觉瓶颈机制，迫使模型自主发现对下游任务有用的隐式视觉表征。

这一设计的精妙之处体现在三个层面：

1. **任务无关性**：同一套隐式token机制可直接应用于空间推理、语义对应、目标计数等多种感知密集型任务，无需为每个任务设计专门的中间表示。
2. **表征的灵活性**：隐式token学到的表征可以是人类难以显式定义的视觉概念（如整体纹理风格、多物体空间配置），这些概念通过可视化（Figure 3）呈现出与正确答案区域高度相关的注意力模式，但难以用规则或标注精确描述。
3. **两阶段训练策略**：Stage 1 的瓶颈训练迫使模型将视觉信息压缩到隐式token中；Stage 2 恢复标准注意力掩码进行联合微调，使隐式token与直接视觉通路协同工作。消融实验表明，仅添加隐式token而不做瓶颈训练（Latents only）性能与 Direct SFT 持平，证实了瓶颈机制是性能增益的根本来源。

### 与基线方法的关键差异

| 设计维度 | Direct SFT | Mirage / ViGoRL / LVR | **LIVR (本文)** |
|---------|-----------|----------------------|----------------|
| 中间监督 | 无 | 显式（辅助图、边界框、文本推理链） | **无（隐式学习）** |
| 视觉信息传递 | 直接关注图像token | 直接关注 + 生成中间输出 | **Stage 1: 仅通过隐式token瓶颈** |
| 新增参数 | 仅LoRA | 取决于方法 | **LoRA + K个隐式token嵌入** |
| 任务适配成本 | 低 | 高（需设计中间监督） | **低（统一框架）** |

LIVR 的实质贡献在于：它证明了**视觉推理能力可以通过结构化的信息瓶颈从端到端任务损失中涌现**，而不需要人类预设推理步骤。这一发现为构建更通用、更可扩展的视觉推理系统提供了新的方法论基础。

LIVR（Latent Implicit Visual Reasoning）的整体框架围绕一个核心设计展开：**在不引入任何显式中间监督的前提下，迫使大型多模态模型（LMM）将任务相关的视觉信息压缩到一组可学习的隐式token中，再基于这些隐式表征完成推理与答案生成**。

### 输入输出流与模块构成

系统的输入为一幅图像 $I$ 和一个文本提示 $Q$，输出为文本答案 $R$。整个pipeline由五个关键模块串联而成：

1. **视觉编码器（Visual Encoder，冻结）**：将输入图像 $I$ 编码为视觉特征 $v(I)$。
2. **投影器（Projector，冻结）**：将视觉特征映射到语言模型的嵌入空间，得到视觉嵌入 $p(v(I))$。
3. **隐式token（Latent Tokens，可学习嵌入）**：在模型原有词汇表 $V$ 中新增 $K$ 个特殊token $\mathcal{L} = \{l_1, l_2, \cdots, l_K\}$，其对应的嵌入行在训练中解冻。这些token被拼接到提示文本之后，作为视觉信息的“瓶颈”载体。
4. **瓶颈注意力掩码（Bottleneck Attention Mask）**：在Stage 1训练阶段，修改自回归注意力矩阵，使得**答案token和提示token均不能直接关注图像token**，只能通过隐式token间接获取视觉信息。这一强制路由机制是LIVR的核心因果干预。
5. **语言模型解码器（Language Model Decoder，LoRA微调）**：以自回归方式处理拼接后的序列 $[p(v(I)), l(Q), \mathcal{L}]$，生成最终答案 $R$。语言骨干通过LoRA进行参数高效微调，视觉编码器和投影器始终保持冻结。

### 两阶段训练调度

LIVR采用分阶段训练策略来平衡瓶颈约束与模型容量利用：

- **Stage 1（视觉瓶颈训练）**：应用上述瓶颈注意力掩码，强制模型将所有任务相关视觉信息压缩到隐式token中。此阶段仅对答案token计算负对数似然损失（NLL），训练4个epoch。
- **Stage 2（无瓶颈联合微调）**：移除瓶颈掩码，恢复标准因果注意力，使模型在保留隐式推理能力的同时充分利用全部视觉上下文。此阶段训练6个epoch。

消融实验证实，这一两阶段调度（4+6 epoch）在表达力与可学习性之间取得了最优平衡，单独使用任一阶段均会导致性能下降。

### 损失计算与参数更新

训练时仅对答案token计算标准负对数似然损失：

$$\mathcal{L} = -\frac{1}{|x|} \sum_{i=1}^{|x|} \log P(x_i \mid x_{<i})$$

可训练参数包括：LoRA适配器（作用于注意力层和MLP层）以及 $K$ 个隐式token的嵌入行。视觉编码器和投影器的全部参数保持冻结。这种轻量级设计使得LIVR能够以极低的额外参数量（仅新增 $K \times d_{\text{embed}}$ 个可学习参数）适配多种LMM骨干。

### 与基线方法的关键差异

相比于直接监督微调（Direct SFT），LIVR的核心改变在于引入了隐式token和瓶颈注意力掩码这两个协同组件。消融实验表明，**仅添加隐式token而不做瓶颈训练**（Latents only）的性能与Direct SFT持平，说明单纯的容量增加无法带来提升；**仅使用瓶颈掩码而不添加隐式token**（Mask only）同样逊于完整LIVR，说明额外的token容量是瓶颈机制生效的必要条件。二者缺一不可，共同构成了LIVR的完整因果链路。

### 补充图表

![[assets/figures/papers/paper_list_l2322_https_arxiv_org_abs_2512_21218/figures/002_Figure_2.jpg]]
*Figure 2: An illustration of our method and bottleneck attention masking. Latent tokens are appended to the prompt and losses are computed on the answer tokens. In our bottleneck attention masking, answers and prompt tokens cannot attend to image tokens*

### 3.1 基础前向传播框架

LIVR 建立在标准大型多模态模型（LMM）的推理范式之上。给定输入图像 $I$ 和文本提示 $Q$，模型的前向传播过程可形式化为：

$$R = M ( p ( v ( I ) ) , l ( Q ) )$$

其中，$v(\cdot)$ 为视觉编码器，将图像映射为视觉特征；$p(\cdot)$ 为投影器，将视觉特征映射到语言模型的嵌入空间；$l(\cdot)$ 为文本嵌入层；$M$ 为语言模型解码器，以自回归方式生成最终响应 $R$。在 LIVR 中，视觉编码器和投影器均保持冻结，仅对语言模型解码器施加 LoRA 微调。

### 3.2 隐式 Token 与损失函数

LIVR 的核心创新在于向模型的词汇表 $V$ 中引入 $K$ 个新的可学习特殊 token：

$$\mathcal{L} = \{l_1, l_2, \cdots, l_K\}$$

这些隐式 token 的嵌入向量在训练中被解冻，与 LoRA 参数一同优化，而模型其余参数保持不变。隐式 token 被追加在提示词之后、答案 token 之前，构成输入序列：`[图像 | 提示词 | 隐式token | 答案]`。

训练目标为仅在答案 token 上计算的负对数似然损失（NLL）：

$$\mathcal{L} = -\frac{1}{|x|} \sum_{i=1}^{|x|} \log P(x_i \mid x_{<i})$$

其中 $x$ 为答案 token 序列，$|x|$ 为其长度。模型通过最小化该损失，端到端地学习如何利用隐式 token 压缩并传递任务相关的视觉信息。

### 3.3 视觉瓶颈注意力掩码

视觉瓶颈机制是 LIVR 的关键设计，通过修改 Transformer 的因果注意力掩码实现信息流的强制路由。在标准自回归解码中，每个 token 可关注所有前序 token（包括图像 token）。LIVR 在训练的第一阶段（Stage 1）引入如下约束：

- **答案 token 与提示 token** 均不能直接关注图像 token $I$，只能关注提示 token $Q$ 和隐式 token $\mathcal{L}$；
- **隐式 token** 可以正常关注图像 token $I$ 和提示 token $Q$，充当视觉信息的唯一“通道”；
- **图像 token** 遵循标准因果掩码，仅关注自身及之前的图像 token。

这一掩码策略迫使模型将所有回答所需的视觉证据压缩到隐式 token 中，从而在无任何显式中间监督的情况下，端到端地学习隐式视觉推理表征。在第二阶段（Stage 2），移除瓶颈掩码，恢复标准因果注意力，对全部可训练参数进行联合微调，以释放模型的全部表达能力。

### 3.4 两阶段训练调度

LIVR 采用两阶段训练策略以平衡瓶颈约束与模型容量：

- **Stage 1（视觉瓶颈训练）**：应用上述瓶颈注意力掩码，训练 4 个 epoch，强制模型学习通过隐式 token 传递视觉信息；
- **Stage 2（联合微调）**：移除瓶颈掩码，恢复标准注意力，训练 6 个 epoch，使隐式 token 与文本 token 自由交互，进一步优化任务性能。

消融实验表明，该 4+6 的 epoch 分配在表达力与约束强度之间取得最优平衡；仅进行 Stage 2 训练（即不加瓶颈）的模型性能与 Direct SFT 持平，验证了瓶颈训练的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l2322_https_arxiv_org_abs_2512_21218/figures/001_Figure_1.jpg]]
*Figure 1: The model is asked to determine which image option is most similar to the reference image. Standard LMMs can only output text, which cannot capture all visual information and may introduce ambiguity. While methods using explicit supervision can train models to output intermediate reasoning steps, these approaches may fail when the reasoning steps themselves are unclear. Our approach allows the model to learn useful representations implicitly. Visualizing the attention maps of the latent tokens shows that the model has learned to recognize underlying visual structures relevant to answering the question that would have been hard for humans to design supervision for*

## 实验与关键发现

### 核心实验设置

LIVR 在九个视觉中心任务上进行了系统评估，涵盖定位、计数、语义对应、功能对应、空间推理、视觉空间规划、多模态视觉感知等多个类别。实验以三种大型多模态模型为骨干：**Qwen2.5-VL-3B**、**Qwen3-VL-4B** 和 **LLaVA-OneVision-1.5-4B**，均采用 LoRA 微调语言解码器，视觉编码器和投影器保持冻结。默认配置使用 K=16 个隐式 token，训练分为两阶段：4 个 epoch 的视觉瓶颈训练（Stage 1）加 6 个 epoch 的无瓶颈联合微调（Stage 2），损失仅计算于答案 token 上。

### 单任务微调主结果

Table 1 汇总了九个任务的单任务微调准确率。在 Qwen2.5-VL-3B 骨干上，LIVR 在所有任务上一致超越 Direct SFT，平均提升 **6.24%**（67.85 vs 61.61）。在 Qwen3-VL-4B 上平均提升 3.43%（77.55 vs 74.12），在 LLaVA-OneVision-1.5-4B 上平均提升 5.60%。值得注意的是，LIVR 在多个任务上不仅超越 Direct SFT，还大幅领先 Zero-shot 基线，验证了隐式视觉推理机制在单任务场景下的通用有效性。

![[assets/figures/papers/paper_list_l2322_https_arxiv_org_abs_2512_21218/figures/003_Table_1.jpg]]
*Table 1: Single-task fine-tuning accuracy*

### 多任务联合训练

Table 2 展示了在 Qwen3-VL-4B 上联合训练六个感知任务的结果。LIVR 在所有六个任务上均优于 Direct SFT，平均准确率从 69.60 提升至 **72.37**（+2.77%）。由于 LIVR 无需任务特定的辅助图像或中间标签，仅从端任务损失中隐式训练隐式 token，因此可直接应用于多任务设置，无需额外适配。

![[assets/figures/papers/paper_list_l2322_https_arxiv_org_abs_2512_21218/figures/004_Table_2.jpg]]
*Table 2: Multi-task fine-tuning accuracy on Qwen3-VL-4B-Instruct*

### 外部基准对比

在空间推理基准 SAT Val 上，LIVR-3B 以 **85.6** 的准确率大幅超越 ViGoRL-3B 的 62.9（+22.7），并在 RoboSpatial 上达到 77.8，优于 ViGoRL-3B 的 70.4（Table 3）。在视觉空间规划任务 VSP 上，LIVR-3B 达到 66.00，而 Mirage 仅为 46.00（+20.00）。

![[assets/figures/papers/paper_list_l2322_https_arxiv_org_abs_2512_21218/figures/005_Table_3.jpg]]
*Table 3: Comparison across spatial reasoning benchmarks. All rows except LIVR-3B (Ours) are reported from ViGoRL*

在多模态视觉感知基准 MMVP 上，LIVR-7B 以 **75.3** 超越 LVR-7B 的 71.7（+3.6）。在 V* 和 BLINK-5 上，LIVR-7B 分别取得 80.1 和 54.28，与 LVR-7B 的 80.6 和 55.37 基本持平（Table 4）。这些结果表明，LIVR 在完全无需显式中间监督的前提下，性能达到或超越了依赖文本推理或显式视觉中间表示的现有方法。

![[assets/figures/papers/paper_list_l2322_https_arxiv_org_abs_2512_21218/figures/006_Table_4.jpg]]
*Table 4: Comparison across MMVP, V*, and BLINK benchmarks. All rows except LIVR-7B (Ours) are reported from LVR*

### 消融实验

#### 隐式 Token 与视觉瓶颈的必要性

Table 5 的消融实验直接验证了两个核心组件的因果作用。仅添加隐式 token 而不做瓶颈训练（Latents only）的模型，性能与 Direct SFT 持平，表明单纯增加 token 容量无法带来提升。仅使用瓶颈掩码而不添加隐式 token（Mask only）同样逊于完整 LIVR，说明额外的 token 容量是瓶颈机制生效的前提。**二者缺一不可**。

![[assets/figures/papers/paper_list_l2322_https_arxiv_org_abs_2512_21218/figures/007_Table_5.jpg]]
*Table 5: Design ablations and additional controls*

#### 模型对隐式 Token 的依赖性

测试时移除隐式 token 的实验提供了因果证据：LIVR 在定位任务上准确率从 83.61 显著下降至 76.23，而仅加 token 不做瓶颈训练的模型移除 token 后性能几乎无变化。这证实 LIVR 模型确实依赖隐式 token 进行推理，而非仅仅将它们视为冗余参数。

#### 隐式 Token 设计选择

Table 6 系统消融了隐式 token 的关键设计维度：

![[assets/figures/papers/paper_list_l2322_https_arxiv_org_abs_2512_21218/figures/008_Table_6.jpg]]
*Table 6: Ablations of latent-token design choices on Qwen3-VL-4B-Instruct. All numbers are accuracies (%)*

- **放置位置**：隐式 token 放置在提示词之后优于放置在之前，平均提升约 2-3%。
- **掩码策略**：同时屏蔽答案-图像和提示-图像的注意力（默认方案）性能最高；仅屏蔽答案-图像注意力或仅屏蔽提示-图像注意力均导致性能下降。
- **嵌入共享**：非共享隐式嵌入（每个隐式 token 独立嵌入）显著优于共享嵌入，说明模型需要多样化的隐式表征空间。
- **Token 数量 K**：准确率随 K 从 4 增加到 16 而提升，K=16 在表达力与可学习性之间达到最佳平衡；K=32 时性能反而下降，可能存在过拟合或优化困难。
- **训练调度**：两阶段训练中，Stage 1 分配 4 个 epoch、Stage 2 分配 6 个 epoch 的调度效果最优。

### 可视化分析

Figure 3 展示了不同任务中隐式 token 到图像区域的注意力图。在语义对应任务中，模型自动关注与参考点对应的目标区域；在定位任务中，注意力集中在正确边界框内的物体上；在计数任务中，模型关注需要计数的物体实例。尽管存在部分注意力汇聚现象，主导模式与任务相关区域高度一致，表明隐式 token 在没有显式监督的情况下捕获了有意义的视觉结构。

![[assets/figures/papers/paper_list_l2322_https_arxiv_org_abs_2512_21218/figures/009_Figure_3.jpg]]
*Figure 3: An illustration of latent-to-image attention maps for different tasks. The left columns show the input images, and the right columns show the attention overlays. In the Semantic Correspondence task, the model identifies the option in the second image that aligns with the REF point in the first image. In the Localization task, it selects bounding boxes that best localize the motorcycle and the dog, and in the Counting task, it counts the cows and balloons. We observe that latent-to-image attention concentrates on regions corresponding to the correct answers or the visual evidence needed to resolve each task. Although some attention sinks persist, the dominant patterns align with task-relevan...*

Figure 4 的 t-SNE 降维可视化进一步显示，隐式 token 的嵌入主要分布在图像 token 区域，而非文本 token 区域，从表征空间角度佐证了隐式 token 确实承载了视觉信息。

![[assets/figures/papers/paper_list_l2322_https_arxiv_org_abs_2512_21218/figures/019_Figure_4.jpg]]
*Figure 4: t-SNE Visualization of Different Tokens*

### 失败模式与局限

尽管 LIVR 在多数任务上表现优异，但在 V* 和 BLINK-5 上未能超越 LVR-7B，提示隐式推理在某些需要精细空间关系或细节辨别的场景下可能不如显式中间表示有效。此外，方法对隐式 token 数量 K 和训练阶段比例较为敏感，需针对任务进行调优才能获得最佳性能。隐式 token 学到的具体表征难以直接解释，可视化仅提供定性分析，无法定量描述每个 token 的功能。当前实验主要在 3-7B 参数规模模型上进行，更大规模模型上的效果尚未验证。

### 补充图表

![[assets/figures/papers/paper_list_l2322_https_arxiv_org_abs_2512_21218/figures/015_Figure.jpg]]
*Figure: Semantic Correspondence*

## 定位与知识库关联

### 与显式中间监督方法的对比

LIVR 的核心定位是**无显式中间监督的隐式视觉推理**，与依赖显式中间表示的方法形成鲜明对比。现有方法通常需要手工设计的中间监督信号来引导视觉推理过程：

- **Mirage** 通过隐式 token 生成中间辅助图像（如深度图、分割掩码），再基于辅助图像进行最终推理。该方法需要为每个任务设计特定的辅助图像生成流程，泛化性受限。在 VSP（Visual Spatial Planning）基准上，Mirage 仅达到 46.00%，而 LIVR 在相同 Qwen2.5-VL-3B 骨干上达到 66.00%，提升 +20.00 个百分点，且无需任何辅助图像生成。

- **ViGoRL** 输出文本推理链与边界框坐标作为显式中间步骤，在 SAT Val 上达到 62.9%。LIVR 在相同基准上达到 85.6%（+22.7 个百分点），表明隐式推理机制在空间推理任务上具有显著优势。

- **LVR** 使用隐式视觉中间表示与强化学习相结合，在 MMVP 上达到 71.7%。LIVR-7B 在相同基准上达到 75.3%（+3.6 个百分点），在 BLINK-5 上达到 54.28%（与 LVR-7B 的 55.37% 基本持平），在 V* 上达到 80.1%（与 LVR-7B 的 80.6% 竞争力相当）。值得注意的是，LIVR 无需强化学习的复杂奖励设计，仅通过端到端监督微调即可达到或超越这些方法的性能。

### 与直接监督微调的关系

Direct SFT（标准监督微调）是 LIVR 最直接的基线。在完全相同的任务数据、LoRA 微调设置下，LIVR 通过引入隐式 token 和视觉瓶颈机制，在 9 个视觉任务上一致超越 Direct SFT：

- Qwen2.5-VL-3B：平均提升 **+6.24%**
- Qwen3-VL-4B：平均提升 **+3.43%**
- LLaVA-OneVision-1.5-4B：平均提升 **+5.60%**

在多任务联合训练设置下（6 个任务），LIVR 在 Qwen3-VL-4B 上达到 72.37%，相比 Direct SFT 的 69.60% 提升 **+2.77%**。这表明隐式 token 机制在不同任务间可共享视觉推理能力，无需为每个任务设计独立的中间表示。

### 与 Zero-shot 基线的对比

Zero-shot 基线（预训练指令模型，无任何任务微调）在多数任务上表现显著低于微调方法，LIVR 的微调增益主要来源于任务适应性训练，而非单纯的模型容量扩展。消融实验中的关键发现进一步佐证了这一点：仅添加隐式 token 而不做瓶颈训练（Latents only），性能与 Direct SFT 持平，表明**容量增加本身不足以带来提升**，瓶颈机制才是性能增益的核心来源。

### 适用边界与局限

1. **任务类型边界**：LIVR 在 9 个感知密集型视觉任务上验证有效，包括语义对应、功能对应、定位、计数、空间推理、多模态视觉感知等。这些任务的共同特点是需要从图像中提取精细的视觉信息进行推理。对于纯文本推理或简单视觉问答任务，LIVR 的增益可能有限，但尚未在论文中系统验证。

2. **模型规模边界**：实验主要在 3B-7B 参数规模的模型上进行（Qwen2.5-VL-3B、Qwen3-VL-4B、LLaVA-OneVision-1.5-4B、Qwen2.5-VL-7B），更大规模模型上的效果尚未验证。随着模型容量增大，隐式 token 的边际增益是否持续存在仍是开放问题。

3. **超参数敏感性**：隐式 token 数量 K 和两阶段训练比例对性能有明显影响。K=16 在表达力与可学习性之间取得最佳平衡，K=4/8 容量不足，K=32 性能下降。两阶段调度（4 epoch Stage1 + 6 epoch Stage2）效果最优。这些超参数可能需要针对新任务进行调优。

4. **可解释性局限**：隐式 token 学到的具体表征难以直接解释。论文通过注意力图可视化（Figure 3）和 t-SNE 降维（Figure 4）提供定性分析，显示隐式 token 主要分布在图像 token 区域，且注意力集中在任务相关区域，但无法定量描述每个 token 的具体功能。这种“黑箱”特性在实际部署中可能引发可信度问题。

5. **信息瓶颈的双面性**：视觉瓶颈机制强制模型通过有限数量的隐式 token 传递视觉信息，这既是优势也是潜在风险。瓶颈训练是否会丢失原始图像中的细节信息，尤其是在需要精细定位或小目标检测的任务中，尚未深入探讨。

### 开放问题

1. **隐式与显式推理的融合**：是否可以将 LIVR 与显式文本链式思维（Chain-of-Thought）结合，让模型在隐式视觉推理的基础上进行显式文本推理，实现更强的复合推理能力？

2. **可解释隐式表征的设计**：隐式 token 内部如何组织视觉信息？能否通过解耦训练或正则化约束，设计出具有可解释性的隐式表征（如每个 token 对应特定的视觉属性）？

3. **更大规模模型的验证**：该方法在 13B、34B 甚至更大规模多模态模型上的适用性如何？隐式 token 的增益是否随模型规模增大而递减？

4. **视觉输出任务的扩展**：LIVR 目前仅用于文本输出任务，能否将其用于需要生成视觉输出的任务（如视觉规划路径生成、图像编辑指令生成）？

5. **信息保留与压缩的平衡**：如何在瓶颈表达力与信息保留之间取得理论上的最优平衡？是否存在任务自适应的动态 token 数量机制？

6. **跨模态迁移**：隐式 token 学到的视觉推理能力能否迁移到其他视觉任务或甚至其他模态（如视频、3D 点云）？

## 原文 PDF

![[paperPDFs/CVPR_2026/Latent_Implicit_Visual_Reasoning.pdf]]
