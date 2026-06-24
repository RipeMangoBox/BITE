---
title: "ReMoGPT: Part-Level Retrieval-Augmented Motion Language Models"
type: paper
paper_level: A
venue: AAAI
year: 2025
pdf_ref: paperPDFs/AAAI_2025/ReMoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models.pdf
aliases:
- ReMoGPT
tags:
- AAAI_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "引入基于身体部位细粒度特征的跨模态检索（PL-TMR），将多模态检索到的样本作为上下文融入运动语言模型的指令调优中，以补充外部知识并提升对罕见动作的泛化能力。"
primary_logic: "将人体运动按运动链拆分为六个部位（左右臂、左右腿、脊柱、根轨迹），用轻量级Transformer分别编码后拼接嵌入，能够捕获更细致的运动语义，从而在文本-运动跨模态检索中实现更精准的匹配，为生成模型提供更有信息量的参考样本，显著改善罕见和复杂动作的生成质量与多样性。"
claims:
- "PL-TMR检索优于文本-文本CLIP检索"
- "多模态检索相比单模态检索显著提升生成性能"
- "ReMoGPT在罕见动作生成上全面优于基线"
- "部位级检索提升了文本-运动检索的准确率"
---

# ReMoGPT: Part-Level Retrieval-Augmented Motion Language Models

> [!tip] 核心洞察
> 将人体运动按运动链拆分为六个部位（左右臂、左右腿、脊柱、根轨迹），用轻量级Transformer分别编码后拼接嵌入，能够捕获更细致的运动语义，从而在文本-运动跨模态检索中实现更精准的匹配，为生成模型提供更有信息量的参考样本，显著改善罕见和复杂动作的生成质量与多样性。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReMoGPT：基于部位级检索增强的运动语言模型 |
| 英文题名 | ReMoGPT: Part-Level Retrieval-Augmented Motion Language Models |
| 会议/期刊 | AAAI 2025 |
| Links | [paper](https://arxiv.org/abs/2412.08456) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | ReMoGPT |
| Dataset | HumanML3D (Rare Motion Generation), Motion-X (Text-to-Motion), HumanML3D (Motion-to-Text Captioning) |

> [!tip] 效果简介
> - HumanML3D (Rare Motion Generation) 上，MMDist 为 3.001，对比 3.113 (MotionDiffuse)，变化 -0.112。
> - HumanML3D (Rare Motion Generation) 上，Top 5% MMDist 为 3.563，对比 4.317 (ReMoDiffuse)，变化 -0.754。
> - Motion-X (Text-to-Motion) 上，RPrecision Top1 为 0.235，对比 0.188 (MotionGPT)，变化 +0.047。

## 概述

**核心问题**：现有统一运动语言模型（如 **MotionGPT**，Jiang et al., NeurIPS 2023）在生成罕见和多样化动作时性能不足，其根本瓶颈在于缺乏对外部知识的利用能力；而基于文本到文本的检索增强方法（如 **ReMoDiffuse**，Zhang et al., ICCV 2023）难以准确匹配运动与描述之间的语义差异，导致检索错误并限制生成质量。

**方法定位**：ReMoGPT 提出了一种基于身体部位级细粒度特征的跨模态检索机制（PL-TMR），将人体运动按运动链拆分为六个部位（左右臂、左右腿、脊柱、根轨迹），分别用轻量级 Transformer 编码后拼接嵌入。该部位级嵌入能够捕获更细致的运动语义，从而在文本-运动跨模态检索中实现更精准的匹配。检索到的多模态样本作为上下文直接融入运动语言模型的指令调优提示中，为生成过程补充外部知识。

**核心结论**：部位级检索显著提升了跨模态匹配准确率（PL-TMR 在 HumanML3D 上 text-to-motion R@1 达 11.00，对比 **TMR**（Petrovich et al., ICCV 2023）的 8.92）；多模态检索（文本-运动 + 运动-文本）相比单模态检索在生成和描述任务上均取得最佳性能；ReMoGPT 在罕见动作生成上全面优于基线，Top 5% MMDist 降至 3.563（对比 ReMoDiffuse 的 4.317），并在 Motion-X 基准上取得领先的文本到运动生成与运动描述结果。

## 背景与动机

将人类运动建模为可生成的内容是计算机视觉与图形学中的核心挑战之一，其应用涵盖动画制作、虚拟人交互和运动理解等多个领域。近年来，统一运动语言模型（如 **MotionGPT**，Jiang et al., NeurIPS 2023）通过将运动序列离散化为运动tokens，并与自然语言联合建模，在文本生成运动（text-to-motion）和运动描述（motion-to-text captioning）等任务上取得了显著进展。这类模型的核心优势在于：它们将异质的运动与语言模态统一到同一个自回归Transformer框架中，从而能够以统一的范式处理多种运动相关任务。

然而，现有统一运动语言模型面临一个关键瓶颈：**在生成罕见和多样化动作时性能显著不足**。这一问题根源于模型仅依赖训练数据中内化的知识，缺乏对外部知识的有效利用机制。当面对训练集中出现频次较低的动作类型（如复杂的舞蹈动作、特殊的体育姿态）时，模型往往倾向于生成“平均化”的常见动作，导致生成结果的多样性和准确性同时下降。

为缓解这一问题，研究者开始探索检索增强生成（Retrieval-Augmented Generation, RAG）范式。在运动生成领域，**ReMoDiffuse**（Zhang et al., ICCV 2023）率先将检索增强引入扩散模型框架，通过从外部数据库中检索相似样本来辅助生成。但ReMoDiffuse采用的是基于**文本-文本相似度**的检索策略（如使用CLIP编码文本后进行匹配），这带来了新的问题：**文本描述与运动序列之间存在天然的多样性差异**——同一段文字可能对应多种不同的运动实现方式，而相似的运动也可能被不同的文字描述。这种“语义鸿沟”使得纯文本检索难以准确匹配最相关的运动参考样本，检索错误会直接损害生成质量。

上述困境揭示了两个亟待解决的技术缺口：

1. **检索粒度不足**：现有方法（如 **TMR**，Petrovich et al., ICCV 2023；**MotionPatches**，Yu et al., CVPR 2024）通常将整个人体运动编码为单一嵌入向量，这难以捕获身体各部位的细粒度运动特征。例如，“右手举起”和“左手举起”在全身嵌入中可能难以区分，但对于动作语义而言却是关键差异。

2. **检索模态单一**：仅依赖文本-文本相似度进行检索，忽略了运动序列本身蕴含的丰富结构信息。跨模态检索（文本-运动、运动-文本）有望提供更互补的相似度信号，但在统一运动语言模型框架中尚未被系统探索。

针对上述问题，本文提出 **ReMoGPT**——一种基于部位级检索增强的统一运动语言模型。其核心动机在于：通过引入**身体部位级别的细粒度跨模态检索**（Part-Level Text-Motion Retrieval, PL-TMR），将多模态检索到的样本作为上下文融入运动语言模型的指令调优中，从而在保留统一生成框架优势的同时，有效补充外部知识并提升对罕见动作的泛化能力。这一设计使得模型在生成时能够“参考”与输入描述或运动最相关的真实样本，而非仅依赖参数化记忆。

## 核心创新

ReMoGPT 的核心创新在于将**部位级细粒度跨模态检索（PL-TMR）**与**检索增强的指令调优**相结合，系统性地解决了现有统一运动语言模型在罕见和多样化动作生成上的性能瓶颈。

### 1. 从全身嵌入到部位级运动表征

现有文本-运动检索方法（如 **TMR** (Petrovich et al., ICCV 2023)、**MotionPatches** (Yu et al., CVPR 2024)）通常将整个人体运动编码为单一嵌入向量，这导致细粒度动作细节容易被全局信息淹没。ReMoGPT 的关键洞察是：**按人体运动链将运动拆分为六个独立部位**——右臂、左臂、右腿、左腿、脊柱和根轨迹——分别用轻量级 Transformer 编码后再拼接为整体嵌入：

$$\mathcal{F}^M(m) = \mathrm{Concat}[\mathcal{F}_1^M(m_1), \dots, \mathcal{F}_P^M(m_P)]$$

这一设计使得每个部位的运动特征都能被独立捕捉，从而在跨模态检索中实现更精准的匹配。实验证据表明，PL-TMR 在 HumanML3D 的文本到运动检索任务上达到了 **R@1 = 11.00**，显著优于 TMR 的 8.92（Table 1），验证了部位级特征对检索精度的提升。

### 2. 从单模态到多模态检索

现有检索增强方法（如 **ReMoDiffuse** (Zhang et al., ICCV 2023)）依赖文本-文本相似度（如 CLIP 嵌入）进行检索，但文本描述与运动之间的多样性差异常导致匹配错误（Figure 2 展示了文本-文本检索与文本-运动检索的样本差异）。ReMoGPT 将检索扩展为**多模态相似度计算**，同时利用文本-运动和运动-文本两个方向的余弦相似度进行检索：

$$s_{m-t} = \frac{\hat{\mathcal{F}}^M(m) \cdot \hat{\mathcal{F}}^T(t)}{\|\hat{\mathcal{F}}^M(m)\| \|\hat{\mathcal{F}}^T(t)\|}$$

消融实验（Table 6）直接验证了这一设计的有效性：多模态检索（Both 1+1）在生成任务上达到 R-Top1 = 0.501、FID = 0.205，均优于仅使用文本或仅使用运动的单模态检索，证实了在运动和语言两个领域同时检索对生成质量的重要性。

### 3. 从扩散模型注入到语言模型上下文融合

不同于 ReMoDiffuse 将检索样本通过特征注入的方式融入扩散去噪过程，ReMoGPT 采用了更简洁的策略：**将检索到的运动-文本对直接作为上下文加入语言模型的提示（prompt）中**，通过指令调优让模型学会利用这些参考样本。训练目标为标准的自回归负对数似然损失，条件中增加了检索上下文 $x_{rag}$：

$$\mathcal{L}_{LM} = -\sum_{i=0}^{L_t-1} \log p_\theta \left( x_{out}^i \mid x_{out}^{<i}, x_{in}, x_{rag} \right)$$

这种设计使得检索增强与基础运动语言模型（基于 **MotionGPT** (Jiang et al., NeurIPS 2023) 的 T5 架构）无缝集成，模型在推理时能够显式参考检索到的相似运动示例，从而显著提升对罕见动作的泛化能力。在 HumanML3D 的罕见动作生成测试中（Table 8），ReMoGPT 的 Top 5% MMDist 降至 3.563，相比 ReMoDiffuse 的 4.317 降低了 0.754，充分体现了检索上下文对长尾动作生成的帮助。

### 创新链总结

三个 changed slots 构成了一个完整的创新链：**部位级编码**提供了更精准的检索基础 → **多模态检索**确保了匹配的可靠性 → **语言模型上下文融合**将检索结果直接转化为生成能力的提升。这条链路使得 ReMoGPT 在保持统一运动语言模型多任务能力的同时，通过外部知识检索弥补了罕见动作生成的短板。

## 整体框架

ReMoGPT 是一个以检索增强为核心、统一处理多种运动相关任务的运动语言模型。其整体框架由三条协同工作的流水线构成：**运动分词**、**部位级跨模态检索**和**检索增强的指令调优生成**，最终实现在统一的 Transformer 语言模型中对运动生成、运动描述等任务的覆盖。

### 1. 运动分词：连续运动到离散 Token 的桥梁

框架的底层基础是将连续人体运动序列转换为离散 token 的运动分词器。给定一段包含 $M$ 帧的运动序列 $m^{1:M}$，首先通过运动编码器 $\mathcal{E}$ 将其压缩为 $L = M/l$ 个运动 token $z^{1:L}$（其中 $l$ 为下采样率），再由解码器 $\mathcal{D}$ 负责从 token 重建回运动。该分词器基于 VQ-VAE 架构，使得运动与文本共享统一的离散符号空间——将原始文本词表 $V_t$ 与运动词表 $V_m$ 合并为联合词表 $V = \{V_t, V_m\}$，从而允许同一个语言模型同时理解和生成两种模态。

### 2. 部位级跨模态检索（PL-TMR）：细粒度外部知识获取

框架的核心创新在于如何从外部数据库中获取高质量的参考样本。ReMoGPT 摒弃了传统的文本-文本相似度检索（如 CLIP），转而提出**部位级文本-运动检索模型（PL-TMR）**。其关键设计是：将人体运动按运动链拆分为六个部位——右臂、左臂、右腿、左腿、脊柱和根轨迹，为每个部位独立训练轻量级 Transformer 编码器 $\mathcal{F}_p^M$，再将各部位嵌入拼接为整体运动表征：

$$\mathcal{F}^M(m) = \mathrm{Concat}[\mathcal{F}_1^M(m_1), \dots, \mathcal{F}_P^M(m_P)]$$

同时，文本描述由语言模型 $\mathcal{F}^T$ 编码为嵌入。经过投影层后，通过余弦相似度计算跨模态匹配分数：

$$s_{m-t} = \frac{\hat{\mathcal{F}}^M(m) \cdot \hat{\mathcal{F}}^T(t)}{\|\hat{\mathcal{F}}^M(m)\| \|\hat{\mathcal{F}}^T(t)\|}$$

这种部位级细粒度编码能够捕获全身单一嵌入容易忽略的局部运动语义，从而在文本-运动检索中实现更精准的匹配（Table 1 显示 PL-TMR 在 HumanML3D 上 text-to-motion R@1 达到 11.00，优于 TMR 的 8.92）。检索数据库直接使用全部训练数据构建，推理时根据相似度排序选取最相关的运动-文本对作为生成参考。

### 3. 检索增强的指令调优：将外部知识融入生成

框架的顶层是一个基于 T5 架构的运动语言模型。与 MotionGPT 等基线仅依赖模型内部参数不同，ReMoGPT 将 PL-TMR 检索到的运动-文本对作为上下文直接拼入提示（prompt），通过指令调优的方式让模型学会利用外部知识。具体而言，输入序列 $x_{in}$ 包含任务指令和待处理内容，检索样本 $x_{rag}$ 以 `<Motion Placeholder R1(R2)>` 等形式嵌入提示中，模型自回归地生成目标输出 $x_{out}$，训练损失为：

$$\mathcal{L}_{LM} = -\sum_{i=0}^{L_t-1} \log p_\theta \left( x_{out}^i \mid x_{out}^{<i}, x_{in}, x_{rag} \right)$$

这种设计使得模型在生成罕见或复杂动作时，能够显式参考数据库中语义相近的真实样本，从而弥补纯参数化模型对外部知识利用不足的瓶颈。消融实验证实，多模态检索（同时使用文本-运动和运动-文本相似度）显著优于单模态检索，在 HumanML3D 上 R-Precision Top1 达到 0.501、FID 降至 0.205（Table 6），且对检索样本数量不敏感，$k=1$（即总共两个检索样本）已足够取得良好性能。

### 4. 输入输出流总览

以文本生成运动任务为例：用户输入文本描述 → PL-TMR 在数据库中检索最匹配的运动-文本对 → 将任务指令、输入文本和检索样本组装为统一格式的提示 → 运动语言模型自回归生成运动 token → 运动解码器将 token 重建为连续运动序列。运动描述任务则反向对称执行。Figure 3 完整展示了这一生成与描述的双向流水线，Figure 5 给出了具体的提示构建示例。

![[assets/figures/papers/paper_list_l21_ReMoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models/figures/004_Figure_3.jpg]]
*Figure 3: An illustration of the motion generation and captioning pipeline in ReMoGPT. Specifcally, ReMoGPT trains a motion-language model to generate the output using the context of the retrieved motion-caption pairs. Figure 4: An overview of the proposed part-level motion encoder for text-motion retrieval*

## 核心模块与公式推导

ReMoGPT 的核心技术路线是在统一运动语言模型的基础上，引入基于身体部位细粒度特征的跨模态检索机制，将检索到的运动-文本对作为上下文融入语言模型的指令调优中，从而补充外部知识并提升对罕见动作的泛化能力。本节依次阐述其关键模块及对应的公式体系。

### 运动分词器

运动分词器基于 VQ-VAE 架构，将连续运动序列转换为离散运动 tokens，使其能够与自然语言 tokens 在同一词汇表中联合建模。给定一段包含 $M$ 帧的运动序列 $m^{1:M} = \{m^i\}_{i=1}^M$，首先通过运动编码器 $\mathcal{E}$ 编码，再经解码器 $\mathcal{D}$ 重建。下采样率为 $l$，得到 $L = M/l$ 个运动 tokens $z^{1:L} = \{z^i\}_{i=1}^L$。运动词汇表 $V_m = \{v_m^i\}_{i=1}^{K_m}$ 与文本词汇表 $V_t = \{v_t^i\}_{i=1}^{K_t}$ 合并为统一词汇表 $V = \{V_t, V_m\}$，实现运动与语言在同一自回归框架下的联合学习。

### 基础运动语言模型训练损失

运动语言模型采用 Transformer 架构（T5），以自回归方式生成目标序列。给定输入序列 $x_{in}$（文本描述或运动 tokens）和目标输出序列 $x_{out}$（长度为 $L_t$），基础训练损失为负对数似然：

$$\mathcal{L}_{LM} = - \sum_{i=0}^{L_t-1} \log p_\theta \left( x_{out}^i \mid x_{out}^{<i}, x_{in} \right)$$

其中 $p_\theta$ 为模型参数化的条件概率分布，$x_{out}^{<i}$ 表示第 $i$ 步之前已生成的所有 tokens。该损失驱动模型学习运动与语言之间的映射关系，是后续检索增强训练的基础。

### 部位级运动编码器

部位级文本-运动检索（PL-TMR）是 ReMoGPT 区别于现有检索增强方法的核心创新。其关键洞察在于：将人体运动按运动链拆分为六个独立部位（右臂、左臂、右腿、左腿、脊柱、根轨迹），分别用轻量级 Transformer 编码后拼接嵌入，能够捕获更细致的运动语义，从而在跨模态检索中实现更精准的匹配。

具体而言，对于运动序列 $m$，将其分解为 $P$ 个身体部位的运动子序列 $m_1, \dots, m_P$（$P=6$）。每个部位 $p$ 使用独立的运动编码器 $\mathcal{F}_p^M$ 进行编码，然后将所有部位嵌入拼接为整体运动嵌入：

$$\mathcal{F}^M(m) = \mathrm{Concat}[\mathcal{F}_1^M(m_1), \dots, \mathcal{F}_P^M(m_P)]$$

同时，使用文本编码器 $\mathcal{F}^T$ 将文本描述 $t$ 编码为 $\mathcal{F}^T(t)$。两个嵌入分别经过投影层后，计算余弦相似度作为跨模态匹配分数：

$$s_{m-t} = \frac{\hat{\mathcal{F}}^M(m) \cdot \hat{\mathcal{F}}^T(t)}{\|\hat{\mathcal{F}}^M(m)\| \|\hat{\mathcal{F}}^T(t)\|}$$

其中 $\hat{\mathcal{F}}^M$ 和 $\hat{\mathcal{F}}^T$ 分别为投影后的运动嵌入和文本嵌入。检索时，根据 $s_{m-t}$ 和 $s_{t-m}$ 的得分对数据库中所有样本排序，选取最相关的运动-文本对作为生成参考。值得注意的是，尽管引入了多个部位编码器，但由于采用轻量级 Transformer，PL-TMR 的总参数量反而小于 MotionPatches 等基线方法。

### 检索增强指令调优

检索模块从外部数据库（默认使用全部训练数据）中获取与输入最相关的运动-文本对，将其作为上下文 $x_{rag}$ 融入语言模型的提示中。训练时，目标序列的生成同时条件于输入 $x_{in}$ 和检索上下文 $x_{rag}$，损失函数扩展为：

$$\mathcal{L}_{LM} = -\sum_{i=0}^{L_t-1} \log p_\theta \left( x_{out}^i \mid x_{out}^{<i}, x_{in}, x_{rag} \right)$$

推理阶段同样依赖 $x_{rag}$ 辅助生成。检索采用多模态策略，同时利用文本-运动相似度和运动-文本相似度进行双向匹配，实验表明多模态检索（Both 1+1）在生成和描述任务上均显著优于仅使用文本或运动单一模态的检索方式。此外，该方法对检索样本数量不敏感，$k=1$（即总共两个检索样本）即可取得良好性能。

## 实验与分析

### 文本-运动跨模态检索性能

部位级文本-运动检索模型（PL-TMR）在HumanML3D基准上进行了全面评估。如Table 1所示，PL-TMR在文本到运动检索的R@1指标上达到11.00，显著优于基线方法**TMR**（Petrovich et al., ICCV 2023）的8.92和**MotionPatches**（Yu et al., CVPR 2024）的9.81。在运动到文本检索任务中，PL-TMR同样展现出竞争力，R@1达到11.60。值得注意的是，尽管PL-TMR为每个身体部位引入了独立的编码器，但由于采用了轻量级Transformer架构，其总参数量反而小于MotionPatches，实现了效率与性能的平衡。

### 文本到运动生成主结果

ReMoGPT在两个主流基准上进行了文本到运动生成评估。在HumanML3D数据集上（Table 2），ReMoGPT取得了FID 0.205的最优结果，RPrecision Top1达到0.534，MModality为2.988。相比基线**MotionGPT**（Jiang et al., NeurIPS 2023），检索增强带来了全面的性能提升。在更大规模的Motion-X数据集上（Table 3），ReMoGPT的RPrecision Top1达到0.235，显著优于MotionGPT的0.188，FID从0.571降至0.352，验证了检索增强策略在大规模场景下的有效性。

![[assets/figures/papers/paper_list_l21_ReMoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models/figures/007_Table_2.jpg]]
*Table 2: Results of text-to-motion generation on HumanML3D. MModality is empty for real motions because it is deterministic. The evaluation metrics are computed with the encoder used in (Guo et al. 2022a). The results of methods marked with † are re-evaluated with their offcial source code and released pre-trained models, and those marked with ‡ are re-trained with our codebase and tasks for fair comparison. Bold and underline indicate the best and the second best results. Table 3: Results of text-to-motion generation on Motion-X*

### 运动到文本描述生成

在运动描述任务上，ReMoGPT同样表现出色。在HumanML3D数据集上（Table 4），ReMoGPT的BertScore达到33.9，优于MotionGPT†的33.2。在Motion-X数据集上（Table 5），模型在BLEU、Rouge、CIDEr和BertScore等多个指标上均取得有竞争力的结果，证明了统一运动语言模型在双向生成任务上的能力。

![[assets/figures/papers/paper_list_l21_ReMoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models/figures/010_Table_4.jpg]]
*Table 4: Results of motion-to-text captioning on HumanML3D. Table 5: Results of motion-to-text captioning on Motion-X*

### 检索方法的消融分析

为验证多模态检索的有效性，Table 6对比了不同检索策略在HumanML3D上的生成和描述性能。结果表明，多模态检索（同时使用文本-运动和运动-文本检索，即“Both 1+1”）在RPrecision Top1（0.501）和FID（0.205）上均优于单模态检索（仅文本-文本或仅运动-运动）。这一发现证实了在运动和语言两个模态域中同时进行检索对生成质量至关重要。

### 外部数据库的影响

Table 7探索了使用不同外部数据库对检索增强生成的影响。当使用更大规模的Motion-X数据集作为HumanML3D任务的外部数据库时，FID进一步降至0.189，表明更大的外部知识库能为生成模型提供更丰富的参考信息。此外，消融实验发现方法对检索样本数量不敏感，k=1（即总共两个检索样本）已足以取得良好性能。

### 罕见动作生成

罕见动作生成是评估模型泛化能力的关键场景。Table 8的结果显示，ReMoGPT在HumanML3D的罕见动作子集上全面优于基线方法。在Top 5% MMDist指标上，ReMoGPT达到3.563，相比**ReMoDiffuse**（Zhang et al., ICCV 2023）的4.317降低了0.754，相比**MotionDiffuse**的4.317也有显著改善。在MMDist指标上，ReMoGPT的3.001优于MotionDiffuse的3.113。Figure 7的定性结果进一步展示了PL-TMR能够检索到与罕见动作语义更匹配的参考样本，从而引导生成模型产生更准确的动作序列。

### 失败模式与局限性

尽管ReMoGPT在多数场景下表现优异，但存在两个主要局限：首先，对于完全未知的新动作类型，即使将该动作的数据集作为外部数据库，如果不进行针对性训练，模型也难以生成相似的动作；其次，运动分词器（VQ-VAE）的泛化能力有限，当输入动作与训练数据分布差异很大时，解码器可能无法正确重建运动序列。这些局限性指向了未来改进方向——提升模型对分布外动作的泛化能力和改进运动分词器的鲁棒性。

### 补充图表

![[assets/figures/papers/paper_list_l21_ReMoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models/figures/006_Table_1.jpg]]
*Table 1: Results of text-to-motion and motion-to-text retrieval benchmark on HumanML3D*

![[assets/figures/papers/paper_list_l21_ReMoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models/figures/011_Table_8.jpg]]
*Table 8: Results of rare motion generation on the HumanML3D dataset*


![[assets/figures/papers/paper_list_l21_ReMoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models/figures/005_Figure_5.jpg]]
*Figure 5: Samples of prompt used for the instruction tuning in ReMoGPT. \<Motion Placeholder> denotes the motion tokens paired with the caption. \<Motion Placeholder R1(R2)> denote the motion tokens of multi-modal retrieved motion-caption pairs*

![[assets/figures/papers/paper_list_l21_ReMoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models/figures/008_Table.jpg]]

![[assets/figures/papers/paper_list_l21_ReMoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models/figures/013_Table_6.jpg]]
*Table 6: Comparison of the retrieval methods on the HumanML3D dataset in motion generation and captioning. Table 7: Comparison of the external database for retrieval*

![[assets/figures/papers/paper_list_l21_ReMoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models/figures/001_Figure_1.jpg]]
*Figure 1: ReMoGPT achieves the state-of-the-art performance in text-to-motion generation and motion-to-text captioning*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

ReMoGPT 处于**统一运动语言模型**与**检索增强生成**两条技术路线的交汇点，其设计直接回应了此前方法的两个核心瓶颈。

**统一运动语言模型基线的继承与超越。** ReMoGPT 以 **MotionGPT**（Jiang et al., NeurIPS 2023）作为基础架构，沿用了其 VQ-VAE 运动分词器与基于 T5 的自回归运动-语言联合建模范式。MotionGPT 将运动与文本统一为离散 token 序列，实现了文本到运动生成和运动描述的统一处理，但其性能受限于训练数据中隐含的知识——对于罕见动作和多样化描述，模型缺乏可调用的外部信息源。ReMoGPT 的核心改造在于**将检索增强机制嵌入该统一框架**：在保持原始 T5 架构和训练目标的前提下，通过向提示中注入检索到的运动-文本对作为上下文，使模型在生成时能够显式地参考外部知识。这一改造在 HumanML3D 数据集上带来了可观的性能提升——FID 从 MotionGPT 的 0.281 降至 0.205（Table 2），在 Motion-X 数据集上 RPrecision Top1 从 0.188 提升至 0.235（Table 3）。

**检索增强运动生成的范式差异。** 与 **ReMoDiffuse**（Zhang et al., ICCV 2023）相比，ReMoGPT 代表了检索增强运动生成的另一种技术路径。ReMoDiffuse 在扩散模型的去噪过程中通过交叉注意力或特征拼接注入检索样本的嵌入，检索增强与生成模型深度耦合。ReMoGPT 则采用了更松散的耦合方式：检索样本直接以 token 序列形式出现在语言模型的输入提示中，生成模型通过自注意力机制自行学习如何利用这些上下文信息。这种设计使得检索模块与生成模块可以独立优化——检索编码器（PL-TMR）专注于跨模态对齐，而生成模型（T5）专注于基于上下文的序列生成。消融实验（Table 6）表明，这种多模态检索增强策略在 HumanML3D 上优于不使用检索的基线，且多模态检索（文本+运动）相比单模态检索（仅文本或仅运动）在 RPrecision Top1 上达到 0.501，FID 降至 0.205。

**检索粒度的关键突破。** 在文本-运动检索这一子任务上，ReMoGPT 的 PL-TMR 模块与 **TMR**（Petrovich et al., ICCV 2023）和 **MotionPatches**（Yu et al., CVPR 2024）形成了直接对比。TMR 使用全身单一嵌入进行跨模态检索，MotionPatches 则通过将运动序列划分为时空 patches 来捕获局部特征。PL-TMR 的独特之处在于**基于运动链的解剖学先验**进行部位拆分——将人体运动按左右臂、左右腿、脊柱和根轨迹六个部分分别用轻量级 Transformer 编码后拼接。这一设计在 HumanML3D 的文本-运动检索基准上取得了 R@1 = 11.00（Table 1），优于 TMR 的 8.92。值得注意的是，尽管引入了多个部位编码器，由于使用了轻量级 Transformer，PL-TMR 的总参数量仍小于 MotionPatches。

### 2. 适用边界

**任务范围。** ReMoGPT 的已验证能力覆盖文本到运动生成（text-to-motion）和运动到文本描述（motion-to-text captioning）两个核心任务，在两个主流基准（HumanML3D 和 Motion-X）上均取得了有竞争力的结果。其统一的 token 化框架理论上可扩展至其他运动相关任务（如运动编辑、运动预测），但论文未提供相关实验证据。

**数据依赖。** 方法的检索增强机制依赖于外部数据库的质量和覆盖范围。当使用 Motion-X 作为外部数据库来辅助 HumanML3D 上的生成时，FID 进一步改善至 0.189（Table 7），表明更大规模、更多样化的检索库能够持续带来增益。然而，这也意味着方法的性能与检索库的构建密切相关——如果检索库中缺乏与输入文本语义匹配的样本，检索增强的收益将受到限制。

**运动类型覆盖。** 在罕见动作生成这一关键测试场景中，ReMoGPT 表现出相对于基线的明显优势：在 HumanML3D 的 Top 5% 最罕见动作上，MMDist 降至 3.563，显著优于 ReMoDiffuse 的 4.317（Table 8）。这表明部位级检索能够为低频动作提供更有信息量的参考样本。然而，这一优势建立在检索库中存在语义相近的样本的前提之上。

### 3. 局限与开放问题

**对全新动作的泛化困境。** 论文明确指出，当面对完全未知的新动作类型时，即使将该新动作的数据集作为外部数据库，如果不进行额外训练，模型也难以生成相似的动作。这一局限揭示了检索增强范式的根本边界：检索机制提供的是对已有知识的索引和重组，而非对新动作模式的创造性合成。运动分词器的泛化能力进一步加剧了这一问题——如果目标动作与训练数据的分布差异很大，VQ-VAE 解码器可能无法正确重建。

**部位级检索的适用性边界。** PL-TMR 基于运动链将人体拆分为六个独立部位分别编码，这一设计假设各部位的运动模式具有足够的独立性。然而，对于高度协调的全身动作（如舞蹈、武术套路），部位间的运动耦合极为紧密，独立编码后拼接的策略可能损失部位间的协同信息。目前尚无实验证据表明 PL-TMR 在此类场景下是否仍能保持相对于全身嵌入方法的优势。

**计算开销的实际影响。** 论文未报告 PL-TMR 与 CLIP 文本-文本检索在实际推理中的延迟对比。虽然参数量可控，但多部位编码器（六个轻量级 Transformer 的独立前向传播）加上跨模态相似度计算，可能在实际部署中引入不可忽略的延迟。对于实时运动生成场景，这一开销的接受度需要进一步评估。

**检索样本数量的敏感性。** 论文发现方法对检索样本数量不敏感，k=1（即总共两个检索样本）已足够取得良好性能。这一现象值得进一步探究：是模型从少量样本中提取信息的能力强，还是检索模块本身在 Top-1 之后的相关性下降较快？理解这一机制有助于优化检索增强策略的计算效率。

**运动分词器的分布外鲁棒性。** 作为整个 pipeline 的入口模块，VQ-VAE 运动分词器的泛化能力直接影响下游生成质量。论文承认该模块在处理分布外动作时存在局限，但未提出针对性的改进方案。这是整个统一运动语言模型路线的共同挑战，也是未来研究的重要方向。

## 原文 PDF

![[paperPDFs/AAAI_2025/ReMoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models.pdf]]
