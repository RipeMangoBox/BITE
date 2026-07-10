---
title: HGM Hierarchical Generative Masked Motion Modeling with Hard Token Mining
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/MMM_Generative_Masked_Motion_Model.pdf
aliases:
- MGMMM
- HHGMMMHTM
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将生成范式从扩散/自回归转换为掩码运动建模（Masked Motion Model）。通过条件掩码 Transformer 的双向注意力实现多标记并行解码，训练中随机掩码赋予模型以掩码标记进行运动编辑的先天能力，从而同时提升速度、质量和编辑灵活性。
primary_logic: 将文本到运动生成构建为掩码标记预测任务，利用 Transformer 捕获运动标记间的双向依赖关系，并通过渐进式并行解码在极少迭代次数内生成高质量运动；统一的掩码机制使得运动中间帧生成、身体部件修改和长序列合成等编辑任务无需额外训练即可完成。
claims:
- MMM 在 HumanML3D 上以 FID 0.080、MM-Dist 2.998 取得最优生成质量，AITS 仅 0.081 秒，比可编辑的扩散模型 MDM（28.112 秒）快两个数量级。
- 通过掩码机制，MMM 在运动中间帧生成和上半身编辑任务上全面优于扩散模型 MDM，过渡更平滑自然。
- 消融实验证实，8192 码本 + 因子分解与余弦掩码调度是高质量快速生成的关键设计。
- HumanML3D 上 FID (↓) = 0.080
---

# HGM Hierarchical Generative Masked Motion Modeling with Hard Token Mining

> [!tip] 核心洞察
> 将文本到运动生成构建为掩码标记预测任务，利用 Transformer 捕获运动标记间的双向依赖关系，并通过渐进式并行解码在极少迭代次数内生成高质量运动；统一的掩码机制使得运动中间帧生成、身体部件修改和长序列合成等编辑任务无需额外训练即可完成。

| 字段 | 内容 |
|------|------|
| 中文题名 | MMM：生成式掩码运动模型 |
| 英文题名 | HGM Hierarchical Generative Masked Motion Modeling with Hard Token Mining |
| 会议/期刊 | CVPR 2024 |
| Links | [Project](https://anonymous-ai-agent.github.io/MMMM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MMM (Generative Masked Motion Model) |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，FID (↓) 0.080 vs 0.112 (AttT2M) (-0.032)；MM-Dist (↓) 2.998 vs 3.038 (AttT2M) (-0.040)；Top-1 R-Precision (↑) 0.504 vs 0.499 (AttT2M) (+0.005)。
> - KIT-ML 上，FID (↓) 0.080 vs 0.116 (T2M-GPT) (-0.036)。
> - HumanML3D (Inference Speed) 上，AITS (seconds, ↓) 0.081 vs 28.112 (MDM) (-28.031)。

## 概述

**核心问题**：现有文本到运动生成方法面临“不可能三角”——扩散模型（如 **MDM**）虽可编辑但推理极慢（单次生成需 28.11 秒），自回归模型（如 **T2M-GPT**）质量高但无法编辑且速度受限，而潜在空间扩散模型（如 **MLD**）虽快却牺牲了编辑灵活性。三者均未能在实时速度、高保真度与运动可编辑性之间取得平衡。

**核心方法**：MMM 将生成范式从扩散去噪/自回归解码转换为**掩码运动建模**（Masked Motion Model）。通过条件掩码 Transformer 的双向注意力实现多标记并行解码，训练中随机掩码赋予模型以 `[MASK]` 标记进行运动编辑的先天能力，从而同时提升速度、质量和编辑灵活性。

**方法定位**：MMM 属于离散标记空间中的并行生成范式，区别于运动空间扩散（MDM）、潜在空间扩散（MLD）和自回归序列建模（T2M-GPT）。其关键模块包括：运动标记器（VQ-VAE with 8192 码本 + 因子分解）、条件掩码 Transformer、CLIP 文本编码器及长度预测器。

**核心结论**：
- **质量最优**：在 HumanML3D 上取得 FID 0.080、MM-Dist 2.998，超越此前最优的 **AttT2M**（FID 0.112）；在 KIT-ML 上 FID 0.080，优于 **T2M-GPT**（0.116）。
- **速度极快**：平均推理时间（AITS）仅 0.081 秒，比可编辑的 MDM（28.112 秒）快两个数量级，亦快于 MLD。
- **原生可编辑**：无需额外训练即可支持运动中间帧生成、上半身部件编辑和长序列合成，编辑质量全面优于扩散修补方法 MDM。

**关键证据**：Table 1（HumanML3D 主结果）、Table 7（速度与可编辑性对比）、Table 3 与 Figure 7（编辑任务评估）构成核心支撑；消融实验证实 8192 码本、余弦掩码调度和 10 次迭代解码是高性能的关键设计。

## 背景与动机

### 文本到运动生成的核心瓶颈

文本到运动生成（Text-to-Motion Generation）旨在根据自然语言描述生成逼真的 3D 人体运动序列，在动画制作、游戏开发和虚拟现实等领域具有广泛应用。然而，现有主流方法在**实时速度、高保真度和运动可编辑性**三者之间始终难以兼得，构成了该领域的核心瓶颈。

当前方法主要分为两大范式：
- **扩散模型**（如 MDM、MotionDiffuse）：直接在冗余的原始运动序列上进行逐步去噪，虽然具备一定的运动编辑能力，但推理速度极慢。例如，MDM 在单张 NVIDIA RTX A5000 GPU 上生成单个运动平均耗时 **28.11 秒**，难以满足实时交互需求。
- **自回归模型**（如 T2M-GPT、AttT2M）：将运动生成建模为单向顺序解码过程，虽然生成质量较高，但逐标记预测的方式不仅限制了推理速度，更使其天然缺乏运动编辑能力——模型无法“回看”或修改已生成的帧。

这种“质量-速度-可编辑性”的三元悖论，使得现有方法在实际部署中面临严重局限：扩散模型太慢，自回归模型不可编辑，而基于潜空间的扩散模型（如 MLD）虽然通过压缩运动表示提升了速度，却牺牲了编辑灵活性。

### MMM 的动机与核心思路

MMM（Generative Masked Motion Model）的提出正是为了打破上述三元悖论。其核心动机在于：**将文本到运动生成重新构建为掩码运动建模（Masked Motion Modeling）任务**，而非传统的扩散去噪或自回归序列预测。

这一范式转换的关键洞察在于：
1. **双向注意力实现并行解码**：条件掩码 Transformer 利用双向注意力机制捕获运动标记间的全局依赖关系，使得多个标记可以同时预测，从而大幅减少推理所需迭代次数（仅需 **10 次迭代**即可收敛）。
2. **掩码机制天然支持运动编辑**：训练阶段随机掩码部分运动标记，使模型学会根据未掩码标记和文本条件预测被掩码内容。推理时，用户只需在目标位置放置 `[MASK]` 标记，即可无需额外训练地完成运动中间帧生成、身体部件修改和长序列合成等编辑任务。

通过这一统一的掩码框架，MMM 旨在同时实现**最优生成质量、极快推理速度（比可编辑扩散模型快两个数量级）和原生运动编辑能力**，填补现有方法的根本性缺口。

## 核心创新

MMM 将文本到运动生成从主流的扩散去噪和自回归序列预测范式，根本性地转换为**掩码运动建模**（Masked Motion Modeling）。这一范式迁移解决了现有方法在速度、质量与可编辑性三者之间的“不可能三角”，其关键创新体现在以下四个核心维度。

### 1. 生成范式：从单向/迭代去噪到双向并行掩码建模

现有方法受限于各自的生成机制：扩散模型（如 **MDM**）直接在冗余的原始运动序列上执行数百步迭代去噪，导致推理速度极慢（单次生成需 28.11 秒）；自回归模型（如 **T2M-GPT**）依赖单向顺序解码，不仅速度受限，且天然缺乏对运动序列的双向上下文感知能力，难以进行运动编辑。

MMM 将生成任务重新定义为**掩码标记预测**：训练时随机掩码部分运动标记，要求模型基于未掩码标记和文本条件双向预测被掩码的内容（损失函数见公式 `L_mask`）。推理时，模型从一个全掩码的“空白画布”开始，通过条件掩码 Transformer 的双向注意力机制并行解码多个高置信度标记，在仅 **10 次迭代**内即可收敛到高质量运动序列。这一设计同时实现了：
- **实时推理**：AITS 仅 0.081 秒，比可编辑的 MDM 快两个数量级（Table 7）。
- **双向上下文建模**：Transformer 可同时关注运动序列的前后文，生成质量（FID 0.080）超越所有扩散和自回归基线（Table 1）。

### 2. 码本设计：8192 码本 + 因子分解 + 死码本重置

运动标记化（Motion Tokenizer）的质量直接决定了生成性能的上限。与常规 VQ-VAE 采用较小码本（如 512 条目）不同，MMM 进行了三项关键改进：

- **超大码本容量**：将码本大小从 512 扩充至 **8192**，同时将码向量维度从 512 降至 **32**。消融实验（Table 6）证实，这一设计显著降低了嵌入量化过程中的信息损失，重建 FID 和生成 FID 均获得大幅改善。
- **因子分解编码**：对码本进行因子分解，进一步提升了离散表示的表达效率。
- **死码本重置**：引入移动平均更新和死码本重置机制，确保码本中所有条目均被充分利用，避免训练崩溃（Table 8 验证了重置频率的影响）。

### 3. 推理策略：余弦掩码调度与迭代并行解码

推理时的掩码调度策略是平衡速度与质量的关键控制旋钮。MMM 采用**余弦掩码调度函数**：

$$n_M(t) = L \cdot \cos\left(\frac{\pi t}{2 T_{dyn}}\right)$$

其中 $t$ 为当前迭代步数，$T_{dyn}$ 为总迭代次数。该调度使早期迭代快速确定运动整体结构（大量标记被掩码），后期迭代精细填充细节（少量标记被掩码）。消融实验（Table 10）表明，余弦调度在 10 次迭代时取得 FID 0.089，显著优于线性和平方根调度。同时，迭代次数设为 10 即可在保持 AITS 0.081s 的同时达到最优生成质量（Table 5）。

### 4. 原生运动编辑能力：统一掩码机制

掩码机制赋予了 MMM **无需额外训练**即可执行多种运动编辑任务的先天能力——只需在目标位置放置 `[MASK]` 标记即可。这与扩散模型（如 MDM）需要定制化的修补（inpainting）流程形成鲜明对比。MMM 支持三类编辑任务（Figure 4）：

- **运动中间帧生成**（Motion In-betweening）：给定首尾关键帧和文本描述，填充中间过渡运动。Table 3 显示 MMM 在所有指标上全面优于 MDM，且过渡更平滑自然（Figure 7）。
- **身体部件编辑**（Upper Body Editing）：固定下半身运动，根据新文本提示修改上半身动作。训练时通过专门的上半身编辑损失（公式 `L_up`）进行微调，Table 3 证实其编辑质量显著优于 MDM（Figure 6）。
- **长序列合成**（Long Sequence Generation）：按故事线（文本提示序列）逐段生成运动，模型自动“幻觉”出段落间的自然过渡帧，无需在过渡数据集上显式训练。

### 创新总结

| 创新维度 | 基线方法 | MMM 方案 | 关键证据 |
|:---|:---|:---|:---|
| 生成范式 | 扩散去噪 / 自回归解码 | 掩码运动建模 + 双向并行解码 | Table 1, Table 7 |
| 码本设计 | 512 码本，标准 VQ | 8192 码本 + 因子分解 + 死码本重置 | Table 6, Table 8 |
| 推理策略 | 固定步数扩散 / 单步自回归 | 余弦掩码调度的迭代并行解码（10 步） | Table 5, Table 10 |
| 运动编辑 | 需定制化修补或不可编辑 | 原生支持，放置 `[MASK]` 即可 | Table 3, Figure 4 |

这四项创新协同作用，使 MMM 成为首个在生成质量、推理速度和运动可编辑性三个维度同时达到最优的文本到运动生成框架（Figure 2 直观展示了这一优势）。

## 整体框架

MMM 的整体框架将文本到运动生成重新构建为一个**掩码运动建模**任务，其核心设计思想是将扩散模型与自回归模型的顺序生成范式，替换为基于双向注意力的并行掩码预测范式。如图 3 所示，系统由两个关键模块串联构成：**运动分词器（Motion Tokenizer）** 和**条件掩码 Transformer（Conditional Masked Transformer）**，并辅以 CLIP 文本编码器与长度预测器完成文本条件的注入与序列长度的确定。

### 训练流程

训练采用**两阶段策略**：

1. **第一阶段**：运动分词器基于 VQ-VAE 框架进行预训练，将原始 3D 人体运动序列编码为离散运动标记序列。该阶段的目标是学习一个紧凑的离散隐空间，使得量化后的标记能够保留丰富的运动语义信息，同时大幅压缩运动表示的冗余度。
2. **第二阶段**：条件掩码 Transformer 以文本嵌入和部分掩码的运动标记序列为输入，通过双向自注意力机制预测被掩码位置的标记。训练时，运动标记序列中随机比例的位置被替换为 `[MASK]` 标记，模型学习以未掩码标记和文本条件为上下文进行重建。

### 推理流程

推理过程从一个完全由 `[MASK]` 标记组成的“空白画布”开始。在每一步迭代中，模型并行预测所有掩码位置的标记分布，并根据置信度选取部分高置信度标记进行填充，剩余位置继续保持掩码状态。掩码数量按照**余弦调度函数**逐步递减：

$$n_M(t) = L \cdot \cos\left(\frac{\pi t}{2 T_{dyn}}\right)$$

其中 $L$ 为预测的运动序列长度，$t$ 为当前迭代步数，$T_{dyn}$ 为总迭代次数。仅需约 10 次迭代，模型即可完成从全掩码到完整运动序列的渐进式并行解码。

### 模块关系与数据流

- **CLIP 文本编码器**接收文本描述，提取句子级特征（全局语义）和单词级特征（局部语义），分别作为条件掩码 Transformer 的全局条件与交叉注意力条件。
- **长度预测器**根据输入文本预估目标运动序列的长度 $L$，该长度决定了掩码标记序列的初始规模。
- **运动分词器**的编码器将原始运动序列压缩为隐向量，经向量量化后映射到大小为 8192 的码本中，输出离散标记序列；解码器则负责将标记序列恢复为连续运动。在生成阶段，仅使用分词器的解码器部分。
- **条件掩码 Transformer** 是生成的核心，它在训练时学习双向上下文依赖，在推理时以并行方式逐步解码，天然支持通过放置 `[MASK]` 标记实现运动中间帧生成、身体部件编辑和长序列合成等编辑任务，无需额外训练。

这种“分词-掩码-并行解码”的架构，使得 MMM 在保持高保真度生成的同时，将平均推理时间压缩至 0.081 秒，比可编辑的扩散模型 MDM（28.112 秒）快两个数量级，同时具备原生的运动编辑能力。

### 补充图表

![[assets/figures/papers/paper_list_l1849_HGM_Hierarchical_Generative_Masked_Motion_Modeling_with_Hard_Token_Minin/figures/003_Figure_3.jpg]]
*Figure 3: Overall architecture of MMM. (a) Motion Tokenizer transforms the raw motion sequence into discrete motion tokens according to a learned codebook. (b) Conditional Masked Transformer learns to predict masked motion tokens, conditioned on word and sentence tokens obtained from CLIP text encoders. (c) Motion Generation starts from an empty canvas and the masked transformer concurrently and progressively predicts multiple highconfidence motion tokens*

## 核心模块与公式推导

MMM 由一个两阶段训练框架构成：第一阶段预训练**运动分词器**（Motion Tokenizer），第二阶段训练**条件掩码 Transformer**（Conditional Masked Transformer）。推理时，通过余弦掩码调度实现并行迭代解码。

### 运动分词器

运动分词器基于 VQ-VAE 架构，将原始 3D 运动序列 $\mathbf{X} \in \mathbb{R}^{L \times D}$ 编码为离散运动标记序列 $\mathbf{Y} = \{y_i\}_{i=1}^{L}$。编码器将运动映射到潜在嵌入 $\mathbf{z}$，随后通过向量量化将其映射到学习到的码本 $\mathbf{E} = \{\mathbf{e}_k\}_{k=1}^{K}$ 中最近的条目。量化过程为：

$$\mathbf{e} = \arg\min_{\mathbf{e}_k \in \mathbf{E}} \|\mathbf{z} - \mathbf{e}_k\|_2^2$$

训练损失为标准的 VQ 损失，包含码本损失和承诺损失：

$$L_{VQ} = \| \operatorname{sg}(\mathbf{z}) - \mathbf{e} \|_2^2 + \beta \| \mathbf{z} - \operatorname{sg}(\mathbf{e}) \|_2^2$$

其中 $\operatorname{sg}(\cdot)$ 为停止梯度操作，$\beta$ 为承诺损失权重。

**关键设计选择**：MMM 采用超大码本（$K=8192$ 条目）并配合低嵌入维度（$d=32$），以在量化过程中减少信息损失。消融实验证实，将码本从 512 扩充至 8192 并降低嵌入维度，显著改善了重建质量和生成 FID（Table 6）。此外，采用指数移动平均更新码本条目，并定期执行死码本重置，以维持码本利用率。

### 条件掩码 Transformer

第二阶段训练一个双向 Transformer，以文本特征和部分掩码的运动标记序列为输入，预测被掩码的标记。文本条件来自 CLIP 编码器，包含句子级特征和词级特征，后者通过交叉注意力层注入 Transformer。

训练时，从运动标记序列 $\mathbf{Y}$ 中随机采样掩码 $\mathbf{M}$，掩码比率从均匀分布 $\mathcal{U}(0.3, 1)$ 中采样。掩码后的序列记为 $Y_{\overline{\mathbf{M}}}$。模型以未掩码标记和文本 $W$ 为条件，预测所有掩码位置上的原始标记。训练目标为负对数似然：

$$\mathcal{L}_{\mathrm{mask}} = - \mathbb{E}_{\mathbf{Y} \in \mathcal{D}} \left[ \sum_{\forall i \in [1, L]} \log p(y_i \mid Y_{\overline{\mathbf{M}}}, W) \right]$$

其中 $\mathcal{D}$ 为训练数据集，$L$ 为运动序列长度。双向注意力机制使模型能够同时捕获运动标记的前后双向依赖，这是 MMM 区别于自回归模型（如 T2M-GPT）的核心能力来源。

### 运动编辑训练损失

MMM 的掩码机制天然支持运动编辑任务，无需额外架构修改。对于上半身编辑，训练时同时掩码上半身和下半身标记，损失函数为：

$$\mathcal{L}_{\mathrm{up}} = - \sum_{\mathbf{Y} \in \mathcal{D}} \left[ \sum_{y i \in [1, L]} \log p(y_i^{up} \mid Y_{\overline{\mathbf{M}}}^{up}, Y_{\overline{\mathbf{M}}}^{down}, W) \right]$$

其中 $Y_{\overline{\mathbf{M}}}^{up}$ 和 $Y_{\overline{\mathbf{M}}}^{down}$ 分别为被掩码的上半身和下半身标记，$W$ 为文本条件。该设计使模型学会在给定下半身运动约束和文本描述的条件下，生成与之协调的上半身运动。

### 推理：余弦掩码调度与并行解码

推理从全掩码序列（空画布）开始，通过迭代并行解码逐步揭示高置信度标记。第 $t$ 步的掩码数量由余弦调度函数决定：

$$n_M(t) = L \cdot \cos\left(\frac{\pi t}{2 T_{dyn}}\right)$$

其中 $T_{dyn}$ 为总迭代次数（默认 10 次）。每步保留置信度最高的 $L - n_M(t)$ 个预测标记，其余位置重新掩码。消融实验表明，余弦调度在 10 次迭代时取得 FID 0.089 的最优质量，优于线性和平方根调度（Table 10）。采样时引入温度参数 $\beta$ 控制多样性：

$$p(y_i \mid Y_{\bar{M}}, W) = \frac{\exp(e_i / \beta)}{\sum_{i \in E} \exp(e_i / \beta)}$$

实验发现 $\beta=1$ 且 Top-K=100%（即标准 softmax 采样）时生成性能最佳（Table 11, Table 12）。运动序列长度 $L$ 由预训练的长度预测器根据输入文本估计。

### 补充图表

![[assets/figures/papers/paper_list_l1849_HGM_Hierarchical_Generative_Masked_Motion_Modeling_with_Hard_Token_Minin/figures/004_Figure_4.jpg]]
*Figure 4: Motion Editing. (Left) Motion in-betweening. (Middle) Long Sequence Generation. (Right) Upper Body Editing. “M” refers to mask token*

## 实验与分析

### 核心性能对比

MMM 在两个主流文本到运动生成基准上均取得了最优或次优的综合性能。

在 **HumanML3D** 数据集上，MMM 以 **FID 0.080** 和 **MM-Dist 2.998** 刷新了生成质量记录（Table 1）。与先前的 SOTA 方法 AttT2M（FID 0.112, MM-Dist 3.038）相比，FID 降低 0.032，MM-Dist 降低 0.040，表明生成运动的分布更接近真实数据且语义匹配更精准。在 R-Precision 指标上，MMM 的 Top-1 准确率达到 **0.504**，略优于 AttT2M 的 0.499，证实了文本条件控制的有效性。

![[assets/figures/papers/paper_list_l1849_HGM_Hierarchical_Generative_Masked_Motion_Modeling_with_Hard_Token_Minin/figures/008_Table_1.jpg]]
*Table 1: Comparison of text-conditional motion synthesis on HumanML3D [12] test set. For each metric, we repeat the evaluation 20 times and report the average with 95% confidence interval. The right arrow (→) indicates that the closer the result is to real motion, the better. Red and Blue indicate the best and the second best result. § reports results using ground-truth motion length*

在 **KIT-ML** 数据集上，MMM 取得了 **FID 0.080** 的最优结果，超越此前最佳的 T2M-GPT（FID 0.116），降幅达 0.036（Table 2）。MM-Dist 为 9.411，位列第二。该结果验证了掩码建模范式在小规模数据集上的泛化能力。

![[assets/figures/papers/paper_list_l1849_HGM_Hierarchical_Generative_Masked_Motion_Modeling_with_Hard_Token_Minin/figures/009_Table_2.jpg]]
*Table 2: Comparison of text-conditional motion synthesis on KIT-ML [24] test set. For each metric, we repeat the evaluation 20 times and report the average with 95% confidence interval. The right arrow (→) indicates that the closer the result is to real motion, the better. Red and Blue indicate the best and the second best result. § reports results using ground-truth motion length*

**速度与可编辑性的帕累托最优**：Figure 2 以 FID 为纵轴、平均推理时间（AITS）为横轴，直观展示了各方法的质量-速度权衡。MMM 位于最接近原点的位置，实现了质量与速度的双重最优。具体而言，MMM 的 AITS 仅为 **0.081 秒**，而可编辑的扩散模型 MDM 需 **28.112 秒**，速度提升约 **347 倍**（Table 7）。即使与以速度见长的潜空间扩散模型 MLD 相比，MMM 在保持可编辑性的同时仍具有更短的推理时间。

### 运动编辑任务评估

MMM 通过统一的掩码机制原生支持三类编辑任务，无需额外训练（Table 3）：

1. **运动中间帧生成**：给定首尾关键帧和文本描述，MMM 生成的中间过渡运动在 FID 指标上全面优于扩散修补方法 MDM。Figure 7 的定性对比显示，MMM 的生成帧与条件帧之间过渡更平滑自然，在帧 146-147 处无明显跳跃，而 MDM 存在可见的不连贯。

![[assets/figures/papers/paper_list_l1849_HGM_Hierarchical_Generative_Masked_Motion_Modeling_with_Hard_Token_Minin/figures/007_Figure_7.jpg]]
*Figure 7: Qualitative comparison of motion in-betweening, generating 50% motion in the middle (frame 50-146) based on the text “a man throws a ball” conditioned on first 25% and last 25% of motion of “a person walks backward, turns around and walks backward the other way.”. Compared with MDM, MMM achieves smoother and more natural transitions between the conditioned and generated motions (at frames 146 and 147)*

2. **上半身编辑**：固定下半身运动，根据新文本生成上半身动作。Table 3 中 MMM 在所有指标上均优于 MDM。Figure 6 以“a man throws a ball”编辑上半身、“a man rises from the ground, walks in a circle and sits back down on the ground.”保持下半身的案例，展示了 MMM 生成的上半身投掷动作与下半身行走坐立动作的自然融合。

![[assets/figures/papers/paper_list_l1849_HGM_Hierarchical_Generative_Masked_Motion_Modeling_with_Hard_Token_Minin/figures/006_Figure_6.jpg]]
*Figure 6: Qualitative comparison of upper body editing, generating upper body part based on the text “a man throws a ball” conditioned on lower body part of “a man rises from the ground, walks in a circle and sits back down on the ground.”*

3. **长序列合成**：通过连续文本提示生成任意长度运动序列，MMM 在相邻提示之间“幻觉”出平滑过渡帧（Figure 4 Middle），无需显式训练过渡数据集。

### 关键设计消融

**码本规模与维度**（Table 6）：将码本从 512 扩充至 **8192** 并降低嵌入维度至 32，是提升重建质量和生成 FID 的关键。大码本减少了向量量化过程中的信息损失，使得运动标记保留更丰富的语义信息。码本重置频率消融（Table 8）表明，适当的死码本重置策略对训练稳定性至关重要。

**掩码比率采样**（Table 4）：训练阶段掩码比率从均匀分布 **U(0.3, 1)** 采样时，模型取得 FID 0.089 和 Top-1 R-Precision 0.520 的最佳平衡。过低的掩码比率上限会削弱模型对高掩码率推理场景的适应能力。

**推理迭代次数与掩码调度**（Table 5, Table 10）：推理迭代次数设为 **10 次**时，在保持 AITS 0.081s 的同时取得 FID 0.089 的最优质量。进一步增加迭代次数对 FID 改善有限，但会线性增加推理时间。在调度函数选择上，**余弦调度**在 10 次迭代时取得 FID 0.089，优于线性调度（FID 0.102）和平方根调度（FID 0.096），验证了余弦函数在解码早期快速减少掩码、后期精细调整的优势。

**交叉注意力层数**（Table 9）：适当数量的词级交叉注意力层可提升 R-Precision，但过多会损害 FID。这表明细粒度文本条件有助于语义对齐，但过度注入词级信息可能干扰运动序列的全局一致性。

**采样策略**（Table 11, Table 12）：温度参数 β=1 且 Top-K=100%（等效于标准 softmax）时生成性能最佳，说明训练良好的掩码 Transformer 在标准采样下已能产生高质量运动，无需温度调节或截断采样的后处理。

### 失败模式与局限性

1. **长文本细粒度渲染不足**：对于包含多个细粒度动作的单句长描述，模型可能无法完整渲染所有细节。这受限于训练数据中最长运动序列仅 196 帧（约 10 秒），模型缺乏超长序列的建模先验。

2. **多人交互运动缺失**：当前框架仅支持单人运动生成，无法处理涉及多个个体的交互式运动场景。扩展至多人场景需要重新设计运动表征和交互建模机制。

3. **长度预测依赖**：生成质量部分依赖于预训练长度预测器的准确性。错误估计的运动长度会导致序列截断或冗余填充，影响整体自然度。

### 补充图表

![[assets/figures/papers/paper_list_l1849_HGM_Hierarchical_Generative_Masked_Motion_Modeling_with_Hard_Token_Minin/figures/014_Table_7.jpg]]
*Table 7: Comparison of the inference speed and quality of generation on text-to-motion along with the editable capability of each model. ‘✓’ means editable while ‘✗’ is not and ‘−’ refers to has-capability but no application provided. We calculate the Average Inference Time per Sentence (AITS) on the test set of HumanML3D [12] without model or data loading parts. All tests are performed on a single NVIDIA RTX A5000*

![[assets/figures/papers/paper_list_l1849_HGM_Hierarchical_Generative_Masked_Motion_Modeling_with_Hard_Token_Minin/figures/013_Table_6.jpg]]
*Table 6: Ablation results on quality influenced by the number of codes and the code dimension*

![[assets/figures/papers/paper_list_l1849_HGM_Hierarchical_Generative_Masked_Motion_Modeling_with_Hard_Token_Minin/figures/022_Table_10.jpg]]
*Table 10: Ablation results on different numbers of inference iterations with cosine, linear, and square root mask scheduling functions*

![[assets/figures/papers/paper_list_l1849_HGM_Hierarchical_Generative_Masked_Motion_Modeling_with_Hard_Token_Minin/figures/011_Table_4.jpg]]
*Table 4: Ablation results on the masking ratio during training*

![[assets/figures/papers/paper_list_l1849_HGM_Hierarchical_Generative_Masked_Motion_Modeling_with_Hard_Token_Minin/figures/012_Table_5.jpg]]
*Table 5: Ablation results on speed and quality influenced by the mask scheduling during inference*

![[assets/figures/papers/paper_list_l1849_HGM_Hierarchical_Generative_Masked_Motion_Modeling_with_Hard_Token_Minin/figures/002_Figure_2.jpg]]
*Figure 2: The motion generation quality (FID score) and speed (AITS) comparisons between MMM and SOTA methods on HumanML3D dataset. The model closer to the origin is better. MMM achieves the best FID score (0.08) and the highest speed (0.081 AITS), while preserving motion editability. “⃝” represents editibility and “×” otherwise. All tests are performed on a single NVIDIA RTX A5000*

## 方法谱系与知识库定位

### 1. 生成范式转换：从扩散/自回归到掩码运动建模

文本到运动生成领域长期被两条技术路线主导：**运动空间扩散模型**与**自回归序列模型**。MMM 的核心贡献在于将问题重新构建为**掩码运动建模**，从而在速度、质量和编辑性三个维度上同时取得突破。

**扩散模型**（如 **MDM**、**MotionDiffuse**、**Fg-T2M**）直接在冗余的原始运动序列上执行逐步去噪，虽然具备一定的编辑能力（通过扩散修补），但推理速度极慢——MDM 在单张 NVIDIA RTX A5000 上生成一条运动的平均推理时间（AITS）高达 28.112 秒。**MLD** 将扩散过程迁移到潜空间以加速推理，但牺牲了运动编辑的灵活性。

**自回归模型**（如 **T2M-GPT**、**AttT2M**）将运动生成视为单向序列预测任务，虽然生成质量较高（AttT2M 在 HumanML3D 上 FID 达 0.112），但受限于顺序解码的固有约束：推理速度难以大幅提升，且无法原生支持运动中间帧生成或身体部件修改等编辑操作。

MMM 通过**条件掩码 Transformer** 的双向注意力机制，将生成转化为并行掩码标记预测任务。训练阶段随机掩码运动标记，赋予模型以掩码标记为条件的双向推理能力；推理阶段从全掩码序列出发，通过**余弦掩码调度**逐步并行解码，仅需 10 次迭代即可收敛，AITS 仅 0.081 秒——比可编辑的 MDM 快两个数量级，同时 FID 达到 0.080，优于所有现有方法。

### 2. 码本设计：大容量离散表示的关键作用

MMM 的运动分词器基于 VQ-VAE 框架，但其设计选择与以往工作形成显著差异。早期方法通常采用较小码本（如 512 条目），标准 VQ 训练容易遭遇码本坍缩和表示能力不足的问题。MMM 将码本扩充至 **8192 条目**，并将嵌入维度降低至 32，配合**因子分解编码**、**移动平均更新**和**死码本重置**策略，在重建质量和生成质量之间取得平衡。消融实验（Table 6）证实，从 512 扩充至 8192 码本显著改善了重建 FID 和生成 FID，是高质量生成的关键设计。

### 3. 编辑能力的范式性优势

运动编辑是 MMM 区别于其他方法的标志性能力。扩散模型（MDM、MotionDiffuse）虽可通过修补实现编辑，但需要定制化的扩散过程设计，且编辑质量受限于去噪步数。自回归模型（T2M-GPT、AttT2M）则完全不具备编辑能力。

MMM 的掩码机制天然支持三种编辑模式：
- **运动中间帧生成**：在给定首尾关键帧的条件下，通过掩码中间帧并由模型预测填充，实现平滑过渡。
- **上半身编辑**：固定下半身运动标记，掩码上半身标记，根据新文本提示生成修改后的上半身运动。
- **长序列合成**：将多段文本提示对应的运动序列通过掩码过渡帧连接，模型“幻觉”出自然的运动过渡。

定量评估（Table 3）显示，MMM 在运动中间帧生成和上半身编辑任务上全面优于 MDM，过渡更平滑自然（Figure 7）。

### 4. 适用边界与局限

**适用场景**：MMM 最适合需要**实时生成**且**支持灵活编辑**的应用场景，如交互式角色动画、游戏引擎中的运动合成、以及需要根据文本指令快速修改运动的创作工具。

**已知局限**：
- **长文本细粒度控制不足**：对于极长的单句文本描述，模型可能难以渲染所有细粒度细节。这源于训练数据中最长运动序列仅 196 帧（约 10 秒），限制了模型对复杂长时序语义的建模能力。
- **不支持多人交互**：当前框架仅处理单人体运动生成，无法建模涉及多个个体的交互式运动（如双人舞蹈、对抗性运动）。

### 5. 开放问题与后续方向

1. **长序列生成的文本切分**：如何整合大语言模型将长文本描述自动切分为适合模型的多段提示，以实现更长的运动序列生成？这需要解决提示边界与运动过渡的自然对齐问题。

2. **多人交互运动生成**：如何扩展当前掩码运动建模框架以支持多人交互式运动生成？可能的路径包括引入空间-时间联合掩码机制，或在码本中编码多人运动的空间关系。

3. **码本表示的理论理解**：8192 码本 + 因子分解为何在运动域表现优异？是否存在更优的码本大小与维度的理论指导原则，而非依赖经验消融？

4. **与大规模预训练的整合**：掩码运动建模范式是否可扩展至更大规模的运动数据集，并与文本-运动对比预训练结合，进一步缩小文本与运动模态之间的语义鸿沟？

## 原文 PDF

![[paperPDFs/CVPR_2024/MMM_Generative_Masked_Motion_Model.pdf]]