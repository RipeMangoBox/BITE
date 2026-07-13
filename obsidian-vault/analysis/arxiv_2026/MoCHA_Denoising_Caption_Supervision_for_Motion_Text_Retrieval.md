---
title: "MoCHA: Denoising Caption Supervision for Motion-Text Retrieval"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/MoCHA_Denoising_Caption_Supervision_for_Motion_Text_Retrieval.pdf
project_link: null
code_link: null
aliases:
- MMCHAR
- MoCHA
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 标题规范化算子 C(t)，将原始标题投影到仅保留运动可恢复语义 s 而去除噪音 a 的规范形式，并配合混合训练平衡规范化和原始视图。
primary_logic: 通过去除标题中的非运动学噪音（标注者风格、推断上下文），可以收紧同一运动的文本嵌入分布，降低正样本梯度方差，从而使对比学习产生更紧密的聚类和更准确的排序，同时显著改善跨数据集迁移能力。
claims:
- 规范化使 HumanML3D 的同一运动文本嵌入方差降低 11%，KIT-ML 降低 19%，证实 a 引入了可测量的噪声。
- 规范化使对比损失的梯度方差降低 11.1%，梯度余弦一致性提高 30.2%，将输入噪声的减少传递到训练信号。
- MoCHA 在 HumanML3D 和 KIT-ML 上均实现最先进的检索性能，T2M R@1 分别达到 13.91%（+3.11pp）和 24.30%（+10.28pp），且在所有 recall 级别均保持增益。
- 规范化改善了嵌入空间几何：同类标题相似度在 H3D 提升 7.5%、在 KIT 提升 24%，分离比（Sep Ratio）提升 8%~25%。
---

# MoCHA: Denoising Caption Supervision for Motion-Text Retrieval

> [!tip] 核心洞察
> 通过去除标题中的非运动学噪音（标注者风格、推断上下文），可以收紧同一运动的文本嵌入分布，降低正样本梯度方差，从而使对比学习产生更紧密的聚类和更准确的排序，同时显著改善跨数据集迁移能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoCHA：面向运动-文本检索的去噪标题监督 |
| 英文题名 | MoCHA: Denoising Caption Supervision for Motion-Text Retrieval |
| 会议/期刊 | arXiv 2026 |
| Links |  [paper](https://arxiv.org/abs/2603.23684)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | MoCHA (Motion Canonicalization for Human Action retrieval) |
| Dataset | HumanML3D, KIT-ML, Cross-dataset H→K, Cross-dataset K→H |

> [!tip] 效果简介
> - HumanML3D (DsPair) 上，T2M R@1 13.91 vs 10.80 (MoPa) (+3.11)；M2T R@1 14.37 vs 11.25 (MoPa) (+3.12)。
> - KIT-ML (DsPair) 上，T2M R@1 24.30 vs 14.02 (MoPa) (+10.28)。
> - Cross-dataset H→K 上，T2M R@1 26.59 (MoCHA LLM) vs 13.74 (MoPa) (+12.85)。

## 概要

运动-文本检索的核心瓶颈并非模型架构或训练规模不足，而在于**对比训练中的监督噪声**：同一运动的多条人工标注（标题）混合了运动可恢复的语义 $s$ 和标注者特有的风格噪音 $a$，标准对比学习将每条标题视为确定性正样本，导致同一运动的文本嵌入方差大、正样本聚类松散，削弱了对齐信号。

**MoCHA**（Motion Canonicalization for Human Action retrieval）针对这一瓶颈提出了一个轻量、即插即用的文本规范化框架。其核心操作是**标题规范化算子 $C(t)$**，通过大语言模型提示将原始标题投影为仅保留运动可恢复语义的规范形式，去除标注者风格、推断性上下文等非运动学噪音。训练时采用**混合损失** $\mathcal{L}_{\text{mix}} = \lambda \mathcal{L}(C(t)) + (1-\lambda) \mathcal{L}(t)$，以规范标题锚定语义对齐，以原始标题作为正则化，在收紧正样本分布的同时保持对自然语言查询的泛化能力。

**核心发现**：

- **噪声可测量**：规范化使 HumanML3D 和 KIT-ML 的同一运动文本嵌入方差分别降低 11% 和 19%，证实标注者噪音 $a$ 确实引入了可量化的监督噪声（Table 1）。
- **信号传导**：噪声减少直接传递到训练信号——对比损失的梯度方差降低 11.1%，梯度余弦一致性提高 30.2%。
- **性能全面提升**：MoCHA 在 HumanML3D 上 T2M R@1 达到 13.91%（+3.11pp），在 KIT-ML 上达到 24.30%（+10.28pp），且所有 recall 级别和检索方向均保持增益（Table 3）。
- **嵌入空间改善**：同类标题相似度在 H3D 提升 7.5%、KIT 提升 24%，分离比提升 8%–25%（Table 2）。
- **跨数据集迁移**：规范化去除数据集特定的标注风格，使 H→K 跨数据集检索的 R@1 相对提升 94%（Table 4）。

**方法定位**：MoCHA 属于**监督去噪**范式，与数据增强（如释义扩充）有本质区别——增强扩大了标题分布方差，可能损害 R@1；规范化则通过收缩方差全面提升所有 recall 级别。该框架仅作用于文本通道，不修改运动或文本编码器，可无缝适配现有对比检索架构（如 MoPa、TMR）。规范化器通过 LLM 提示实现，并蒸馏为 FlanT5 模型以消除推理时的外部 LLM 依赖，蒸馏版本性能与 LLM 相当且方差更小。

**局限与开放问题**：固定且不可微的规范化算子偶尔会过度压缩（如将姿态细节错误转换）；当前 $s/a$ 边界偏向粗粒度动作描述，部分可恢复的细粒度特征未被纳入规范形式；跨数据集 K→H 的检索绝对值仍然较低，表明仅靠语言规范化无法弥补运动覆盖的不足。未来方向包括联合优化规范化与检索损失、形式化界定 $s/a$ 边界，以及探索规范化表示向运动生成等其他任务的迁移。

### 运动-文本检索中的监督噪声问题

运动-文本检索任务旨在根据自然语言描述检索对应的 3D 人体运动序列，或反之由运动检索文本。近年来，基于对比学习的检索方法通过最大化匹配对之间的相似度、最小化非匹配对的相似度，取得了显著进展。然而，标准对比训练范式存在一个被长期忽视的根本性缺陷：它将每条标题视为运动的确定性正样本，而忽略了标题本身的随机生成特性。

真实标注过程中，同一段运动会被不同标注者以不同方式描述。每条标题 $t$ 实际上是从一个条件分布中采样得到的：

$$t \sim p(t \mid s, a), \quad a \sim p(a).$$

其中，$s$ 代表从运动中可恢复的语义内容（如动作类型、身体部位、运动方向、重复次数等），而 $a$ 则是标注者特有的噪音因素——包括个人语言风格、冗余修饰、不确定性的推断性描述等。对噪音 $a$ 积分后，同一运动语义 $s$ 下的标题分布为：

$$p(t \mid s) = \int p(t \mid s, a) p(a) \mathrm{d} a.$$

标准对比训练将每个 $t$ 作为独立的确定性正样本，迫使文本编码器将同一运动的不同标题映射到嵌入空间中的同一目标点。然而，由于不同标题携带了相互冲突的噪音信号，这一目标在训练过程中产生了高方差的正样本键，导致对比损失的梯度方向不一致、正样本聚类松散，从而削弱了对齐信号的质量。

### 现有方法的局限性

现有的运动-文本检索方法主要沿着两条技术路线展开。以 **TMR**（Petrovich et al., 2023）为代表的早期工作将对比学习与 VAE 正则化相结合，但并未显式建模标题中的噪音结构。以 **MoPa**（MotionPatches）为代表的近期方法采用 ViT 架构处理 3D 关节序列，在 HumanML3D 和 KIT-ML 等基准上取得了较强的性能，但其训练范式仍然将原始标题直接送入文本编码器，完全继承了监督噪音的问题。

这些方法面临的核心瓶颈可归纳为三点：

1. **嵌入方差过大**：同一运动的不同标题在文本嵌入空间中分布分散，正样本聚类松散，削弱了对比目标的收敛信号。
2. **梯度信号不一致**：由标题噪音引起的正样本键方差直接传递到对比损失的梯度中，导致训练过程中梯度方向频繁震荡。
3. **跨数据集迁移能力弱**：不同数据集（如 HumanML3D 和 KIT-ML）具有不同的标注风格 $p(a)$，模型在训练时学习到了数据集特定的语言偏差，在跨数据集测试时性能急剧下降。

### MoCHA 的核心动机

本文的核心洞察是：通过去除标题中与运动无关的标注者噪音 $a$，仅保留运动可恢复语义 $s$，可以收紧同一运动的文本嵌入分布，降低正样本梯度方差，从而使对比学习产生更紧密的聚类和更准确的排序。这一思路将问题从“如何设计更强的编码器”转化为“如何净化监督信号本身”，开辟了一条与现有工作正交的改进路径。

基于此，MoCHA 提出了标题规范化算子 $C(t)$，将原始标题投影为仅保留运动可恢复内容的规范形式：

$$C(t) \approx \phi(s).$$

该算子完全作用于文本通道，不修改运动编码器或文本编码器的架构，因此可以作为即插即用的模块应用于任何现有的对比检索框架。为平衡去噪与自然语言查询的泛化能力，MoCHA 进一步引入了混合训练策略，同时利用规范化标题和原始标题进行对比学习。

## 核心方法与创新机理

MoCHA 的核心创新在于将运动-文本检索中的**标题监督噪声问题**形式化为一个可操作的因果框架，并提出**标题规范化（Caption Canonicalization）**作为解决方案。与以往方法将每个标题视为确定性正样本不同，MoCHA 识别出标题由运动可恢复语义 $s$ 和标注者特定噪音 $a$ 混合生成的分布特性，并通过规范化算子 $C(t)$ 将标题投影为仅保留 $s$ 的规范形式，从而从根源上收紧对比学习的正样本分布。

### 关键 changed slots 与创新机制

**1. 标题预处理：从原始标题到规范化投影**

基线方法（如 **MoPa**）直接将原始标题输入文本编码器作为对比学习的正样本键，这导致同一运动的多个标注产生分散的文本嵌入，削弱对齐信号。MoCHA 引入规范化算子 $C(t)$，其设计目标为：

$$C(t) \approx \phi(s)$$

该算子将标题 $t$ 映射为仅依赖于运动语义 $s$ 的规范文本表示，去除标注者风格、推断上下文等噪音 $a$。这一改变的直接效果是：同一运动的文本嵌入方差在 HumanML3D 上降低 11.1%，在 KIT-ML 上降低 18.7%（Table 1），证实了 $a$ 确实引入了可测量的监督噪声。

**2. 训练目标：混合训练平衡规范与原始视图**

基线仅使用原始标题计算对称 InfoNCE 损失。MoCHA 提出混合训练损失：

$$\mathcal{L}_{\mathrm{mix}} = \lambda \mathcal{L}_{\mathrm{InfoNCE}}(\{(m_i, C(t_i))\}) + (1-\lambda) \mathcal{L}_{\mathrm{InfoNCE}}(\{(m_i, t_i)\})$$

其中规范项锚定语义对齐，降低梯度方差；原始项作为正则化，保持对自然语言查询的泛化能力。实验表明，规范化使对比损失的梯度方差降低 11.1%，梯度余弦一致性提高 30.2%，将输入噪声的减少有效传递到训练信号中。

**3. 规范化实现：从 LLM 到蒸馏模型的实用化路径**

规范化算子 $C$ 首先通过 GPT-5.2（LLM）以少量示例提示实现，随后蒸馏为 FlanT5-base 模型以实现无 LLM 推理。蒸馏后的 FlanT5 规范化器性能与 LLM 相当，且在多随机种子下测试时方差更小（H3D 上 0.87 vs 1.19，KIT 上 0.98 vs 2.18），更适合实际部署。

### 创新点的因果链条

MoCHA 的创新形成一个完整的因果链：**识别噪音源**（$s$-$a$ 分解）→ **设计去噪算子**（$C(t)$ 投影）→ **优化训练策略**（混合损失平衡）→ **验证下游效果**（嵌入质量提升 → 检索性能提升 → 跨数据集迁移增强）。这一链条的核心洞察在于：通过去除标题中的非运动学噪音，可以收紧同一运动的文本嵌入分布，降低正样本梯度方差，从而使对比学习产生更紧密的聚类和更准确的排序。

### 与数据增强路线的本质区别

MoCHA 的创新与常见的文本增强策略（如释义生成、回译）有本质区别。释义增强扩大了 $p(t \mid s)$ 的分布，在三种设置中的两种损害了分布内 R@1（Table 5）；回译作为保留标注风格的负对照，在四种条件中的三种表现持平或低于基线（Table 6）。这证明核心改进因子是**去噪**而非任意文本转换——规范化通过缩小方差而非扩大方差来提升所有 recall 级别的性能。

MoCHA 是一个**完全作用于文本通道的监督去噪框架**，其核心目标是在不修改运动编码器与文本编码器架构的前提下，消除对比训练信号中的标注者特定噪音，从而提升运动-文本检索的嵌入空间质量。整个框架由三个关键模块串联构成，形成“规范化—编码—混合训练”的闭环。

### 核心动机：标题的 (s, a) 分解

MoCHA 的设计起点是对运动-文本数据集中标题生成过程的概率建模。给定一个运动，其对应的标题并非确定性的，而是由两个独立因素共同决定：

- **运动可恢复语义 s**：标题中描述动作、身体部位、方向、重复次数等可直接从运动序列推断的内容。这部分是检索任务真正需要对齐的信号。
- **标注者特定噪音 a**：标题中混入的标注者个人风格、推断性上下文、冗余修饰等与运动本身无关的变异。a 服从标注者群体的分布 p(a)。

标题的生成过程可形式化为：

$$t \sim p(t \mid s, a), \quad a \sim p(a).$$

对噪音 a 积分后，同一运动语义 s 下所有可能标题的分布为：

$$p(t \mid s) = \int p(t \mid s, a) p(a) \mathrm{d} a.$$

标准对比训练（如 InfoNCE）将每个标题视为该运动的唯一确定性正样本，忽视了这一分布特性。其后果是：同一运动的多个标题在嵌入空间中散布较大，正样本键的梯度方差升高，对齐信号被稀释。MoCHA 的解决思路是**在文本进入编码器之前，将每个标题投影到仅保留 s 的规范形式**，从而将分布 p(t|s) 压缩为近似确定性的正样本。

### 模块一：标题规范化算子 C(t)

规范化算子是 MoCHA 的核心模块，其作用是将原始标题 t 映射为仅依赖于运动语义 s 的规范文本表示：

$$C(t) \approx \phi(s).$$

C 的设计目标是**去除 a 而保留 s**。具体实现采用大语言模型（LLM）提示的方式：通过少量示例提示，引导 LLM 从标题中提取动作、身体部位、方向、重复等运动可恢复内容，同时丢弃标注者风格、冗余描述和推断性语言。

为消除推理时对外部 LLM 的依赖，MoCHA 进一步将 LLM 的规范化能力蒸馏至 FlanT5-base 模型，形成 FlanT5-PPT 变体。蒸馏后的规范化器在性能上与 LLM 相当，且多随机种子测试下方差更小（HumanML3D 上标准差 0.87 vs. LLM 的 1.19，KIT-ML 上 0.98 vs. 2.18），更适合实际部署。

### 模块二：运动与文本编码器

MoCHA 不对编码器架构做任何改动，直接沿用 MoPa 的双塔结构：

- **运动编码器**：ViT-B/16 作用于 22 个关节的 3D 序列，输出 256 维运动嵌入。
- **文本编码器**：DistilBERT，取 CLS token 输出 256 维文本嵌入。

规范化发生在文本编码之前，因此编码器接收的是已去噪的规范标题 C(t)（或原始标题 t，取决于训练阶段），而非原始标注文本。

### 模块三：混合训练策略

仅使用规范化标题进行训练虽能锚定语义对齐，但可能使模型过度适应规范文本的简洁风格，降低对自然语言查询的泛化能力。为此，MoCHA 引入**混合训练损失**，同时利用规范化和原始标题：

$$\mathcal{L}_{\mathrm{mix}} = \lambda \mathcal{L}_{\mathrm{InfoNCE}}(\{(m_i, C(t_i))\}) + (1-\lambda) \mathcal{L}_{\mathrm{InfoNCE}}(\{(m_i, t_i)\}).$$

其中 λ 为混合系数，控制两个视图的权重。规范项 $\mathcal{L}_{\mathrm{InfoNCE}}(C(t))$ 将文本嵌入锚定在运动语义 s 附近，降低正样本梯度方差；原始项 $\mathcal{L}_{\mathrm{InfoNCE}}(t)$ 作为正则化，保持模型对自然语言查询的兼容性。

训练采用**先规范后原始的混合再版策略**：初期以规范标题为主，帮助嵌入空间快速形成紧致的语义聚类；后期逐步引入原始标题，使模型适应自然语言的多样性。

### 数据流总览

1. **训练阶段**：原始标题 t 经规范化算子 C 生成 C(t)；C(t) 和 t 分别经文本编码器得到嵌入，与对应运动嵌入共同计算 InfoNCE 损失，按 λ 加权求和后反向传播。
2. **推理阶段**：查询标题（文本查询或运动对应的标题）经 C 规范化后进入文本编码器，在共享嵌入空间中与运动嵌入进行最近邻检索。

整个流程的核心特征是**去噪发生在监督信号层面而非模型架构层面**：编码器不变，损失函数形式不变，唯一改变的是正样本键的文本来源。这使得 MoCHA 具有高度的架构无关性——论文实验表明，将混合训练策略应用于 TMR 架构同样有效，TMR Blend 在 HumanML3D 上将 T2M R@1 从 8.96% 提升至 13.64%。

![[assets/figures/papers/paper_list_l87_MoCHA_Denoising_Caption_Supervision_for_Motion_Text_Retrieval/figures/002_Figure_2.jpg]]
*Figure 2: MoCHA overview. (a) Motivated by the (s, a) decomposition (Section 3.1), C(·) projects each caption onto s by stripping stylistic variation a (red). C is implemented via LLM and distilled into FlanT5 for LLM-free inference. (b) Blend training balances both views: the denoised C(ti) anchors embeddings around s to reduce gradient variance, while the original ti regularizes for natural-language queries*

### 3.1 标题噪声的形式化分解

MoCHA 的核心洞见在于将运动-文本检索中的标题建模为一个**条件分布**，而非确定性正样本。给定一段运动，其可恢复的运动语义（motion-recoverable semantics）记为 $s$，而标注者特有的噪音因素（annotator-specific nuisance factors）记为 $a$，其中 $a \sim p(a)$。一个标题 $t$ 的生成过程可表示为：

$$t \sim p(t \mid s, a), \quad a \sim p(a).$$

对噪音因素 $a$ 积分，可得到同一运动语义 $s$ 下所有可能标题的**语义边际分布**：

$$p(t \mid s) = \int p(t \mid s, a) p(a) \mathrm{d} a.$$

标准对比训练（如 InfoNCE）将每个标题 $t$ 视为唯一的正样本键，忽略了 $p(t \mid s)$ 的分布特性。这导致同一运动的多个标题在嵌入空间中散布，正样本聚类松散，梯度方差增大，削弱了对齐信号。MoCHA 的核心设计目标就是消除 $a$ 的干扰，将标题投影到仅依赖 $s$ 的规范表示上。

### 3.2 标题规范化算子 C

为去除标注者噪音 $a$，MoCHA 引入一个**标题规范化算子** $C(t)$，将原始标题映射为仅保留运动可恢复语义的规范形式：

$$C(t) \approx \phi(s),$$

其中 $\phi(s)$ 表示仅依赖于运动语义 $s$ 的文本表示，对标注者风格、推断性上下文等噪音因素 $a$ 保持不变。该算子的设计遵循以下原则：

- **保留运动可恢复内容**：动作名称、身体部位、方向、重复次数等可直接从运动序列推断的信息。
- **剥离标注者噪音**：风格化表达、主观推断（如“看起来像在跳舞”）、冗余修饰等非运动学内容。

在实现层面，$C(t)$ 首先通过大语言模型（GPT-5.2）以少量示例提示的方式实现，随后蒸馏至 FlanT5-base 模型，实现无 LLM 依赖的推理。这种蒸馏方案在保持规范化质量的同时，消除了对外部 API 的依赖，更适合实际部署。

### 3.3 混合训练策略

仅使用规范化标题训练可能导致模型对自然语言查询的泛化能力下降，因为推理时的用户查询通常包含噪音因素 $a$。为此，MoCHA 采用**混合训练损失**，同时利用规范化和原始标题：

$$\mathcal{L}_{\mathrm{mix}} = \lambda \mathcal{L}_{\mathrm{InfoNCE}}(\{(m_i, C(t_i))\}) + (1-\lambda) \mathcal{L}_{\mathrm{InfoNCE}}(\{(m_i, t_i)\}),$$

其中 $\lambda$ 为混合系数。规范项 $\mathcal{L}_{\mathrm{InfoNCE}}(\{(m_i, C(t_i))\})$ 将嵌入锚定在运动语义 $s$ 周围，降低正样本梯度方差；原始项 $\mathcal{L}_{\mathrm{InfoNCE}}(\{(m_i, t_i)\})$ 作为正则化，保持对自然语言查询的适应性。默认采用**先规范后原始**的混合再版策略（blend replay），在训练的不同阶段动态调整两项的权重。

### 3.4 标题嵌入方差的形式化度量

为量化规范化对监督噪声的削减效果，MoCHA 定义了同一运动下标题嵌入的方差度量。设运动 $m$ 有 $K$ 个标题，其文本嵌入为 $\mathbf{t}_1, \ldots, \mathbf{t}_K$，则平均成对不相似度 $V(m)$ 定义为：

$$V(m) = 1 - \frac{1}{\binom{K}{2}} \sum_{i<j} \cos(\mathbf{t}_i, \mathbf{t}_j).$$

进一步，由标题选择引起的正样本键 $\mathbf{k}_+$ 的嵌入方差可分解为：

$$\mathrm{Var}_{\mathrm{text}}[\mathbf{k}_+] = \frac{1}{K} \sum_{k=1}^{K} \lVert T(c_k) - \bar{\mathbf{t}}_m \rVert^2 = \frac{K-1}{K} V(m),$$

其中 $T(c_k)$ 为文本编码器对标题 $c_k$ 的输出嵌入，$\bar{\mathbf{t}}_m$ 为 $K$ 个标题嵌入的均值。该公式建立了标题间语义差异 $V(m)$ 与对比训练中正样本键方差之间的直接联系——$V(m)$ 越大，梯度更新方向越不稳定。规范化通过降低 $V(m)$，从源头减少了对比训练的监督噪声。

## 实验与关键发现

### 核心瓶颈验证：标题噪声的测量与消除

MoCHA 的核心假设是：同一运动的多个标题之所以在嵌入空间中分散，是因为标注者特定的噪音 $a$ 引入了可测量的方差。为验证这一点，作者定义了同一运动 $m$ 下 $K$ 个标题嵌入的平均成对不相似度 $V(m)$：

$$V(m) = 1 - \frac{1}{\binom{K}{2}} \sum_{i<j} \cos(\mathbf{t}_i, \mathbf{t}_j)$$

并由此推导出正样本键的嵌入方差：

$$\mathrm{Var}_{\mathrm{text}}[\mathbf{k}_+] = \frac{K-1}{K} V(m)$$

**Table 1** 的结果直接支持了这一假设：在 HumanML3D 上，规范化使 $V(m)$ 降低 11.1%，在 KIT-ML 上降低 18.7%。这表明原始标题中确实存在标注者噪音 $a$，而规范化算子 $C(t)$ 能有效将其剥离。

更重要的是，这种输入层面的噪声减少传递到了训练信号中。直接梯度方差测量显示，规范化使对比损失的梯度方差降低 11.1%（从 79.72 降至 70.89），梯度余弦一致性提升 30.2%。同时，MoCHA 训练出的模型产生更集中的 InfoNCE 分布，softmax 熵从基线的 6.29 降至 6.03。这构成了从“标题去噪 → 梯度信号稳定 → 嵌入空间改善”的完整因果链。

### 嵌入空间几何分析

**Table 2** 从四个维度量化了规范化对嵌入空间几何的改善：

- **Intra Similarity（同类标题相似度）**：HumanML3D 上从 0.413 提升至 0.444（+7.5%），KIT-ML 上从 0.396 提升至 0.491（+24.0%），表明同一运动的标题嵌入更紧密地聚类。
- **Alignment（文本-运动对齐度）**：规范化后文本嵌入与其对应运动嵌入的余弦相似度在两个数据集上均有提升。
- **Separation Ratio（分离比）**：提升 8%~25%，说明正样本与最近负样本的边界更清晰。

这些改善与理论预测一致：去除 $a$ 后，正样本键的方差减小，对比学习的梯度方向更一致，从而产生更紧凑的类内分布和更好的类间分离。

### 分布内检索主结果

**Table 3** 报告了 MoCHA 在 HumanML3D 和 KIT-ML 上的分布内检索性能。MoCHA (LLM) 变体在两个数据集上均达到最优：

- **HumanML3D**：T2M R@1 达到 13.91%（较 MoPa 基线 +3.11pp），M2T R@1 达到 14.37%（+3.12pp）。
- **KIT-ML**：T2M R@1 达到 24.30%（+10.28pp），M2T R@1 达到 24.50%（+9.70pp）。

关键观察是增益覆盖所有 recall 级别（R@1、R@5、R@10），排除了精度-召回率权衡的可能性。这证实被去除的内容确实是噪音 $a$ 而非有用的语义 $s$——如果是后者，高 recall 级别应出现性能下降。

MoCHA (T5) 变体（使用蒸馏的 FlanT5 规范化器，完全无需 LLM 推理）同样表现强劲：HumanML3D 上 T2M R@1 +2.5pp，KIT-ML 上 +8.1pp。值得注意的是，T5 变体在多随机种子测试中方差更小（HumanML3D 上标准差 0.87 vs LLM 的 1.19，KIT-ML 上 0.98 vs 2.18），更适合实际部署。

### 跨数据集迁移

**Table 4** 揭示了规范化最显著的优势：跨数据集检索。当模型在 HumanML3D 上训练、在 KIT-ML 上测试时（H→K），MoCHA (LLM) 的 T2M R@1 从基线的 13.74% 跃升至 26.59%，相对提升 94%。反向迁移（K→H）同样有增益（+0.96pp），但绝对值仍然较低（约 2-3%）。

这一现象与 $(s, a)$ 分解的理论预测高度一致：基线模型学习了数据集特定的标注风格 $p(a)$，当测试集的 $a$ 分布与训练集不同时性能骤降；规范化剥离了 $p(a)$，使表示更具迁移性。跨数据集增益比例远大于分布内增益，进一步证实了噪音去除的核心作用。

### 去噪 vs. 增强：机制对比

**Table 5** 将规范化与释义增强进行了对比。释义增强扩大了 $p(t \mid s)$ 的分布宽度，在三种设置中的两种损害了分布内 R@1，仅在部分条件下改善 R@5/R@10——表现为典型的平滑效应。相反，规范化通过压缩方差在所有 recall 级别均带来提升。这表明 MoCHA 的增益来自“去噪”而非“文本变换”本身。

**Table 6** 的消融实验进一步确认了这一结论：

- **规则化停用词剥离**：改善了跨数据集迁移（H→K +2.9pp），但在分布内失败，说明粗粒度噪声去除在复杂标题中会丢失判别细节。
- **回译（backtranslation）**：作为负对照，保留了标注风格但变换了表面形式，在四种条件中的三种表现持平或低于基线，证明核心改进因子是去噪而非任意文本转换。

### 规范化器的泛化性

MoCHA 的规范化策略对不同检索架构具有泛化性。**Table 11** 显示，将规范化应用于 TMR（基于 VAE 的对比检索方法）同样有效：TMR Blend 在 HumanML3D 上将 T2M R@1 从 8.96% 提升至 13.64%，在 KIT-ML 上从 11.62% 提升至 19.69%。

![[assets/figures/papers/paper_list_l87_MoCHA_Denoising_Caption_Supervision_for_Motion_Text_Retrieval/figures/013_Table_11.jpg]]
*Table 11: Canonicalization on TMR (DsPair T2M R@1, canonical text at test). Evaluated at best validation epoch. †KIT baseline corrected after fixing case-sensitivity in mirror-caption grouping*

### 失败模式与局限性

尽管整体表现优异，规范化算子 $C(t)$ 存在以下已知失败模式：

1. **过度压缩**：固定且不可微的 $C(t)$ 偶尔会将细粒度运动信息错误去除。例如，将 “person with both knees bended” 转换为 “move both feet side to side”，丢失了关键的姿态信息。
2. **s/a 边界偏向粗粒度**：当前提示设计倾向于保留粗粒度动作描述，某些可恢复的细粒度特征（如 “elderly gait”）未被纳入规范形式。
3. **跨数据集 K→H 绝对值低**：即使经过规范化，K→H 的 R@1 仍仅约 2-3%，表明仅靠语言规范化无法弥补运动覆盖的不足。
4. **超参数敏感性**：混合训练的 $\lambda$ 需要手动调节；推理时仍需蒸馏模型以避免外部 LLM 依赖。

这些失败模式指向了开放问题：能否将 $C(t)$ 与对比检索损失联合优化，使其自适应地学习去噪策略？如何形式化地界定 $s$ 和 $a$ 的边界以减少过度压缩？

![[assets/figures/papers/paper_list_l87_MoCHA_Denoising_Caption_Supervision_for_Motion_Text_Retrieval/figures/006_Table_3.jpg]]
*Table 3: In-distribution retrieval results (C2). MoCHA achieves state-of-theart on both benchmarks, with consistent gains across all recall ranks and retrieval directions—ruling out a precision-recall tradeoff and confirming that the removed content was a, not useful s. Full ablations in Appendix G.1*

![[assets/figures/papers/paper_list_l87_MoCHA_Denoising_Caption_Supervision_for_Motion_Text_Retrieval/figures/009_Table_6.jpg]]
*Table 6: Canonicalization mechanism ablation (T2M R@1 %). Even rule-based stopword stripping improves transfer, while backtranslation (which transforms without denoising) does not—confirming that canonicalization is a general principle (C1): the gains stem from projecting onto s, not from any particular model’s language understanding*

![[assets/figures/papers/paper_list_l87_MoCHA_Denoising_Caption_Supervision_for_Motion_Text_Retrieval/figures/015_Table_13.jpg]]
*Table 13: BABEL cross-dataset retrieval (Threshold T2M protocol per TMR++). X→B comparisons use last epoch as BABEL R@1 is unstable due to caption duplicity. BABEL numbers are inflated by 86% caption duplication (see text). H→K and K→H results without BABEL are reported in the main paper (Table 4)*

![[assets/figures/papers/paper_list_l87_MoCHA_Denoising_Caption_Supervision_for_Motion_Text_Retrieval/figures/016_Table_14.jpg]]
*Table 14: Test-time text mode ablation (DsPair T2M R@1, epoch 50). Each row is a different training strategy (LLM-trained models); columns show performance under each test-time text mode. Note: Main Table 3 MoCHA (T5) reports a separatelytrained FlanT5-PPT Blend model (13.30%/22.14%); see Appendix G.1 for all FlanT5- PPT variants*

## 定位与知识库关联

### 核心改进：从“确定性正样本”到“去噪监督”

标准运动-文本对比检索方法（如 **TMR** (Petrovich et al., 2023) 及 **MoPa**）将每个标题视为运动的确切描述，直接作为 InfoNCE 损失的正样本键。这一做法的隐含假设是：同一运动的所有标注在语义上等价。然而，MoCHA 揭示了一个被忽视的结构性瓶颈——标题并非由运动语义 $s$ 唯一确定，而是从条件分布 $t \sim p(t \mid s, a), a \sim p(a)$ 中采样，其中 $a$ 是标注者特有的噪音因素（风格、推理上下文、冗余描述）。这导致同一运动的文本嵌入在对比空间中散布，正样本梯度方差增大，削弱了对齐信号的质量。

MoCHA 的方法论创新在于将问题从“更好的编码器架构”重新定义为“更干净的监督信号”：通过标题规范化算子 $C(t) \approx \phi(s)$ 在编码前去除 $a$，并配合混合训练损失 $\mathcal{L}_{\mathrm{mix}} = \lambda \mathcal{L}_{\mathrm{InfoNCE}}(\{(m_i, C(t_i))\}) + (1-\lambda) \mathcal{L}_{\mathrm{InfoNCE}}(\{(m_i, t_i)\})$ 平衡规范化和原始视图。这一设计使 MoCHA 成为一个“文本通道上的即插即用监督去噪框架”，运动编码器和文本编码器本身保持不变。

### 在运动-文本检索谱系中的位置

相较于现有方法，MoCHA 的独特定位体现在三个维度：

| 维度 | 先前方法 | MoCHA |
|------|----------|-------|
| 改进对象 | 编码器架构、损失函数形式、负样本挖掘 | 正样本的语义纯度 |
| 对标注噪音的假设 | 忽略或视为不可约减 | 显式建模为 $s/a$ 分解并主动去除 |
| 跨数据集迁移 | 依赖域适应或联合训练 | 通过去除数据集特定标注风格 $p(a)$ 自然实现 |

具体而言，**TMR** (Petrovich et al., 2023) 通过 VAE 正则化约束嵌入空间，但未触及标题侧的噪音问题；**MoPa** 基于 ViT 架构在 HumanML3D 上取得了 10.80% 的 T2M R@1，但其性能受限于原始标题中的标注者差异。MoCHA 在 MoPa 架构上叠加规范化后，将同一指标提升至 13.91%（+3.11pp），且在所有 recall 级别均保持增益——这排除了精度-召回权衡的可能性，证实被去除的是噪音 $a$ 而非有用的语义 $s$。

### 与数据增强方法的本质区别

MoCHA 的规范化与常见的文本增强策略存在根本性差异。释义增强（paraphrase augmentation）扩大了 $p(t \mid s)$ 的分布宽度，在 HumanML3D 的三种设置中有两种损害了分布内 R@1（Table 5），本质上是一种平滑操作，以牺牲 R@1 换取 R@5/R@10 的提升。回译（backtranslation）保留了标注风格，在四种条件中的三种表现持平或低于基线（Table 6），证明核心改进因子是去噪而非任意文本转换。规范化通过坍缩方差而非增加方差，在所有 recall 级别同时提升性能。

### 适用边界与已知局限

1. **固定且不可微的规范化器**：$C(t)$ 由 LLM 提示实现并蒸馏为 FlanT5，在训练期间不参与梯度更新。这偶尔导致过度压缩——例如将“person with both knees bended”错误转换为“move both feet side to side”，丢失了运动可恢复的细粒度信息。

2. **$s/a$ 边界的粗粒度偏向**：当前提示设计倾向于提取粗粒度动作描述，某些可恢复的细粒度特征（如“elderly gait”）未被纳入规范形式。这限制了规范化在需要精细运动区分场景下的上限。

3. **跨数据集迁移的非对称性**：虽然 H→K 的 T2M R@1 相对提升达 94%（26.59% vs. 13.74%），但 K→H 的绝对值仍然较低（约 2-3%）。这表明仅靠语言规范化无法弥补运动覆盖的不足——KIT-ML 的运动多样性远低于 HumanML3D，模型在 KIT 上训练时见过的运动模式有限，即使文本侧噪音被去除，运动编码器仍缺乏对 HumanML3D 中丰富动作的表征能力。

4. **混合系数 $\lambda$ 需手动调节**：$\mathcal{L}_{\mathrm{mix}}$ 中的 $\lambda$ 控制规范化和原始标题的平衡，当前采用先规范后原始的混合再版策略，但最优值可能依赖于数据集和任务。

5. **推理时的蒸馏依赖**：为避免外部 LLM 调用，规范化器需蒸馏为 FlanT5-base。虽然蒸馏模型性能与 LLM 相当且方差更小（H3D 上标准差 0.87 vs. 1.19，KIT 上 0.98 vs. 2.18），但蒸馏过程本身引入了额外的数据准备和训练成本。

### 开放问题

1. **可学习的规范化**：能否将 $C(t)$ 与对比检索损失联合优化，使其自适应地学习去噪策略？当前固定提示的方法无法根据下游任务反馈调整 $s/a$ 边界。

2. **$s/a$ 边界的形式化界定**：如何形式化地定义哪些文本元素属于运动可恢复语义、哪些属于标注者噪音？这直接影响提示设计的系统性和规范化器的鲁棒性。

3. **跨任务迁移**：规范化的文本表示能否作为通用增强迁移到其他运动-语言任务（如运动生成、动作分割、时序定位）？初步证据（MoCHA 对 TMR 架构同样有效，将 T2M R@1 从 8.96% 提升至 13.64%）表明规范化具有架构无关性，但其任务无关性尚未验证。

4. **多语言与极端噪音**：当前实验限于英文标注。在更多语言和更极端的数据集噪音（如口语描述、多模态输入、非专业标注）下，规范化的效果是否仍然稳健？公平性方面，规范化去除了标注者风格，可能减少数据集特定的语言偏差，但未直接评估对不同语言或人口统计群体的迁移性。

### 知识库定位总结

MoCHA 在运动-文本检索领域引入了**监督信号去噪**这一新的方法论维度，与编码器设计、损失函数改进、负样本挖掘等传统方向形成互补。其核心洞察——对比学习的正样本应锚定在运动可恢复语义上而非标注者特定表达——具有跨领域的可迁移性，适用于任何存在标注者风格差异的多模态对比学习场景。当前版本受限于固定的规范化器设计和粗粒度的 $s/a$ 划分，但蒸馏版本的稳定性和跨数据集迁移的大幅提升表明，该方向具有从研究原型走向实际部署的潜力。

## 原文 PDF

![[paperPDFs/arxiv_2026/MoCHA_Denoising_Caption_Supervision_for_Motion_Text_Retrieval.pdf]]
