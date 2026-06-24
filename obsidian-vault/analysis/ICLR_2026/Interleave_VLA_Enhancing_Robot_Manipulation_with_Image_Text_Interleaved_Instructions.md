---
title: "Interleave-VLA: Enhancing Robot Manipulation with Image-Text Interleaved Instructions"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Interleave_VLA_Enhancing_Robot_Manipulation_with_Image_Text_Interleaved_Instructions.pdf
openreview_forum_id: ULTWUuGhC3
aliases:
- IV
- Interleave-VLA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入图文交错指令（interleaved image-text instructions），通过上下文视觉线索为任务目标提供显式视觉定位。"
primary_logic: "通过在VLA模型的tokenizer中引入特殊分隔符（<BOI>/<EOI>），使得现有VLA架构无需修改即可原生处理图文交错输入，从而缓解注意力幻觉，在保持In-Domain性能的同时大幅提升Out-of-Domain泛化（2-3倍）。"
claims:
- "Interleave-VLA (Full) achieves 2× better performance on semantically out-of-domain tasks compared to Text-VLA on SimplerEnv."
- "Interleave-VLA achieves 2-3× higher out-of-domain success rate in real-robot experiments."
- "Interleave-VLA improves generalization capacity of OpenVLA by over 2× on VIMA-Bench across all levels."
- "Interleave-VLA substantially reduces attentional hallucination compared to Text-VLA, as shown by quantitative failure analysis."
---

# Interleave-VLA: Enhancing Robot Manipulation with Image-Text Interleaved Instructions

> [!tip] 核心洞察
> 通过在VLA模型的tokenizer中引入特殊分隔符（<BOI>/<EOI>），使得现有VLA架构无需修改即可原生处理图文交错输入，从而缓解注意力幻觉，在保持In-Domain性能的同时大幅提升Out-of-Domain泛化（2-3倍）。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Interleave-VLA：利用图文交错指令增强机器人操作 |
| 英文题名 | Interleave-VLA: Enhancing Robot Manipulation with Image-Text Interleaved Instructions |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ULTWUuGhC3) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Interleave-VLA |
| Dataset | SimplerEnv Out-of-Domain (Semantic Generalization Avg.), SimplerEnv Novel Category, Real-robot Out-of-Domain Food Lift (Avg.), Real-robot Out-of-Domain Kitchenware Pick&Place (Avg.) |

> [!tip] 效果简介
> - SimplerEnv Out-of-Domain (Semantic Generalization Avg.) 上，Success Rate (%) 为 60.6 ± 1.1 (Interleave-VLA Full)，对比 39.5 ± 0.5 (π0 Text-VLA)，变化 +21.1。
> - SimplerEnv Novel Category 上，Success Rate (%) 为 57.3 ± 2.8 (Interleave-VLA Full)，对比 19.3 ± 1.5 (π0 Text-VLA)，变化 +38.0。
> - Real-robot Out-of-Domain Food Lift (Avg.) 上，Success Rate (%) 为 71% (Interleave-VLA w/ PT)，对比 13% (Text-VLA w/ PT)，变化 +58%。

## 概述

### 问题瓶颈

当前主流的视觉‑语言‑动作（VLA）模型普遍采用纯文本指令作为任务描述。然而，在面对训练分布之外的未见物体与场景时，纯文本指令暴露出一个深层瓶颈：**注意力幻觉**。具体表现为三种典型失效模式——注意力泄露（目标被部分关注，但焦点溢出至无关背景或干扰物）、注意力分散（注意力广泛散布而无主导焦点）、注意力偏差（注意力集中于显著干扰物而非真实目标）。这些幻觉根源于语言本身的歧义性以及训练分布偏差，严重制约了模型的语义泛化能力。

### 核心方法

**Interleave‑VLA** 提出了一种轻量级、可迁移的图文交错指令范式，其核心操作为：在现有 VLA 模型的 tokenizer 中引入特殊分隔符 `<BOI>` 和 `<EOI>`，使骨干架构无需任何修改即可原生处理任意交错的图像‑文本指令序列。该方法包含三个关键模块：

- **轻量级适配模块**：仅更新输入处理器以支持交错格式，核心 VLA 架构保持不变。
- **规模化训练流水线**：利用自动构建的大规模交错具身数据集（210k episodes，13M 帧，覆盖 3,500+ 物体类别）进行训练，保留原始超参与流匹配目标。
- **通用推理接口**：测试时支持纯文本或任意来源的图文交错指令（摄像头裁剪、网络图片、手绘草图），实现零样本指令跟随。

### 方法定位

Interleave‑VLA 作为一种**骨干无关的即插即用范式**，区别于现有方案的关键特征在于：不依赖外部数据采集或仿真引擎，仅通过重用已有机器人数据集自动生成交错指令；同时保持对多种 VLA 骨干（π0、OpenVLA）的兼容性，骨干替换带来的性能影响可忽略。

### 核心结论

- **仿真泛化**：在 SimplerEnv 基准上，Interleave‑VLA 在 Out‑of‑Domain 语义泛化任务中平均成功率达 **60.6%**，较 Text‑VLA 的 39.5% 提升 **+21.1 个百分点**；在 Novel Category 子集上差距更为悬殊（57.3% vs 19.3%），实现约 **3 倍**提升。
- **真实机器人泛化**：在 FANUC 机械臂的真实实验中，Interleave‑VLA 在 Out‑of‑Domain 食物抓取任务上平均成功率达 **71%**，而 Text‑VLA 仅 **13%**；厨房用品 Pick&Place 任务上为 **38% vs 21%**，提升 **2‑3 倍**。值得注意的是，预训练数据不包含 FANUC 平台数据，展示了强跨实体迁移能力。
- **注意力幻觉缓解**：定量失败分析表明，Interleave‑VLA 显著降低了高层意图错误（Jitter、Wrong Intention），残余失败主要来自底层动作执行，而 Text‑VLA 在分布外场景中表现出更多的高层幻觉。
- **骨干可扩展性**：将 Interleave‑VLA 应用于 OpenVLA 后，在 VIMA‑Bench 的 L1‑L3 泛化层级上均实现 **2 倍以上**提升（L3: 64.00 vs 23.86），验证了范式的通用性。

## 背景与动机

### 语言指令的歧义与注意力幻觉

当前主流的视觉-语言-动作（VLA）模型——如 **π0**（Black et al., 2024）、**OpenVLA**（Kim et al., 2024）、**RT-1-X**（Brohan et al., 2022）和 **Octo**（Team et al., 2024）——普遍采用纯文本指令作为任务描述。尽管这些模型在已知场景中展现了强大的操作能力，但在面对未见物体和新类别时，其泛化性能急剧下降。

核心瓶颈在于**语言歧义**与**训练分布偏差**共同导致的**注意力幻觉**（attentional hallucination）。如图5所示，当文本指令描述一个训练中未见的物体时，模型无法将抽象的语言标签与视觉观测中的具体物体正确关联，从而产生三类典型的注意力失效：

1. **注意力泄露**（Attention Leakage）：模型部分关注目标，但注意力同时溢出到无关背景或干扰区域。
2. **注意力分散**（Diffused Attention）：注意力广泛散布，缺乏主导焦点，表明模型对目标位置的不确定性。
3. **注意力偏差**（Attentional Bias）：注意力集中在某个显著干扰物上，而非真正的任务目标。

定量分析（Figure 11）进一步证实：Text-VLA的失败主要源于高层意图错误（如错误意图、抖动），而非低层执行失败（如抓取失败、放置失败）。在Out-of-Domain场景中，这类高层幻觉尤为严重，直接限制了模型的语义泛化上限。

### 现有方法的局限

现有改进路径存在明显局限。**π0.5**（Intelligence et al., 2025）通过额外的物体定位和检测VQA数据预训练来增强视觉理解，但这一策略依赖外部数据采集，且无法从根本上解决文本指令固有的指代歧义。**Spatial-VLA**（Qu et al., 2025）引入空间推理能力，但仍以文本为唯一指令模态。更关键的是，这些方法通常与特定模型骨干深度绑定，缺乏跨架构的可迁移性。

### 核心动机：图文交错指令

Interleave-VLA的出发点是：**如果人类在描述一个陌生物体时，最自然的方式是直接展示其图像，那么机器人也应该能够接受图文交错的指令**。通过在指令序列中嵌入任务目标的视觉线索，模型可以在上下文中获得显式的视觉定位信息，从而绕过纯文本指令的语义鸿沟。

该范式的关键设计原则是**轻量适配**：不改变VLA模型的核心架构，仅在tokenizer中引入特殊分隔符（`<BOI>`/`<EOI>`）来区分图像与文本token，使现有VLA能够原生处理图文交错输入（Figure 2）。这一设计使Interleave-VLA成为一个骨干无关的插件式方案，可适配π0、OpenVLA等多种VLA架构（Table 1）。

## 核心创新

Interleave-VLA 的核心创新在于**将图文交错指令（interleaved image-text instructions）引入视觉‑语言‑动作（VLA）模型**，在不改变模型架构的前提下，通过上下文视觉线索缓解文本指令VLA在未见物体和场景上的注意力幻觉，从而大幅提升泛化能力。其关键设计围绕四个 changed slots 展开。

### 1. 指令输入格式：从纯文本到图文交错序列

现有文本指令VLA（如 π0, OpenVLA）仅接受单一文本指令，当面对训练分布外的未见物体或场景时，语言歧义和分布偏移导致模型无法准确定位任务目标。Interleave-VLA 将指令格式从纯文本扩展为**图文任意交错的序列**：

$$\mathcal{T} = ( u_1, \dotsc, u_M ), \quad u_j \in \mathcal{V}_{\text{text}} \cup \mathcal{V}_{\text{img}}$$

其中 $\mathcal{T}$ 为有序的文本或图像 token 序列（Section 3.1）。这一格式允许在指令中嵌入任务目标的视觉示例（如裁剪图像、网络图片、手绘草图），为模型提供显式的视觉定位线索。消融实验（Table 6）表明，图文交错格式相比纯文本和纯视觉目标格式，在未见物体和类别上泛化更优，且能有效避免“Move Near”等模糊目标的歧义。

### 2. Tokenizer 特殊分隔符：零架构修改的适配机制

为实现上述输入格式，Interleave-VLA 在现有 VLA 的 tokenizer 中引入 **`<BOI>` 和 `<EOI>` 特殊分隔符**，用以区分图像与文本 token（Section 3.2, Appendix D.1）。这一轻量级适配模块仅修改输入处理器，核心 VLA 架构（如 π0 的 Paligemma 骨干）完全保持不变。该设计使 Interleave-VLA 成为一个**骨干无关的即插即用插件**（Table 1），可无缝适配 π0、OpenVLA 等不同 VLA 模型，且骨干替换对性能影响可忽略（Table 11）。

### 3. 训练数据指令类型：自动流水线生成的交错图文指令

传统 VLA 训练仅使用文本标签，Interleave-VLA 则通过**自动流水线**从现有机器人数据集中生成交错图文指令（Section 3.3, Appendix J）。流水线包含三步：
1. **指令解析**：使用 Qwen2.5 从语言指令中提取关键物体；
2. **开放词汇检测**：使用 OWLv2 在轨迹帧中定位并裁剪目标物体；
3. **数据质量验证**：使用 Qwen2.5-VL 验证检测结果，必要时提供关键点供 Segment Anything 进行更精确分割。

该流水线综合准确率达 95.6%（OWLv2 单独为 82.6%），最终构建了包含 210k episodes、13M 帧、覆盖 3,500 个独特物体的开放交错具身数据集。训练时保留原始 VLA 的超参数和流匹配目标，仅将指令替换为交错格式。

### 4. 模型架构：骨干不变，仅适配输入层

Interleave-VLA 的架构创新在于**不改变 VLA 骨干**，仅通过输入处理器适配交错序列（Figure 2, Figure 8）。这使其区别于需要修改核心架构或依赖额外预训练任务的方法（如 π0.5 需要额外的物体定位和检测 VQA 数据）。训练和推理流程保持统一：

$$a_t \sim \pi_{\theta}( \cdot \mid s_t ), \quad s_t = ( I_t, \mathbf{q}_t, \mathcal{T} )$$

其中 $I_t$ 为当前视觉观测，$\mathbf{q}_t$ 为本体感知状态，$\mathcal{T}$ 为交错指令序列。推断时，模型支持灵活使用文本或交错指令，可接受任意来源的指令图像（摄像头裁剪、网络图片、手绘草图），展现出零样本泛化能力（Section 4.3.2）。

### 创新总结

上述四个 changed slots 构成了 Interleave-VLA 的核心创新闭环：**通过 tokenizer 层的轻量适配，使现有 VLA 原生处理图文交错输入，从而在保持架构和训练目标不变的前提下，利用上下文视觉线索消除注意力幻觉，实现 2‑3 倍的 Out‑of‑Domain 泛化提升**。这一范式在 SimplerEnv 语义泛化任务（Table 2: +21.1%）、真实机器人实验（Table 3: +58% 食物提升）和 VIMA‑Bench（Table 14: +40.14% L3）上均得到强证据支持。

## 整体框架

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_ULTWUuGhC3/figures/004_Table_1.jpg]]

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_ULTWUuGhC3/figures/005_Figure_2.jpg]]
*Figure 2: Overview of the Interleave-VLA paradigm, featuring an extendable adaptation of Text-VLA to handle interleaved inputs, scalable training on a constructed large interleaved dataset, and versatile inference that supports a wide range of interleaved instructions*

Interleave-VLA 的核心设计动机源于一个已被定量验证的瓶颈：**现有纯文本指令 VLA 模型在处理未见物体和场景时，因语言歧义与训练分布偏移，系统性地产生注意力幻觉（注意力偏差、注意力分散、注意力泄露），严重制约泛化能力**（Figure 5, Figure 11）。为解决这一问题，Interleave-VLA 引入**图文交错指令**作为因果调节变量——通过在指令序列中嵌入目标物体的视觉线索，为模型提供显式的上下文视觉定位，从而在不改变核心 VLA 架构的前提下，大幅缓解注意力幻觉。

### 范式总览

Interleave-VLA 被设计为一个**轻量级、可迁移的即插即用范式**（Table 1），其整体架构由三个关键模块构成（Figure 2）：

1. **轻量级适配模块（Adaptation Module）**：在基础 VLA 模型的 tokenizer 中引入特殊分隔符 `<BOI>` 和 `<EOI>`，使现有架构能够原生区分图像 token 与文本 token，而无需修改骨干网络或训练目标。
2. **交错数据集训练流水线（Scalable Training Pipeline）**：利用大规模开放交错具身数据集（210k episodes，13M frames，覆盖 3,500+ 独特物体）进行训练，完全保留原始 VLA 的超参数和流匹配目标。
3. **通用推理接口（Versatile Inference Interface）**：测试时灵活支持纯文本或任意图文交错指令，可接受摄像头裁剪、网络图片乃至手绘草图等任意来源的指令图像。

### 输入输出流与形式化定义

Interleave-VLA 的策略形式化定义为：

$$a_t \sim \pi_{\theta}( \cdot \mid s_t )$$

其中状态 $s_t$ 包含三个组成部分：

$$s_t = ( I_t, \mathbf{q}_t, \mathcal{T} )$$

- $I_t$：当前时刻的视觉观测
- $\mathbf{q}_t$：本体感知状态（关节角度等）
- $\mathcal{T}$：**图文交错指令序列**，定义为有序的 token 序列：

$$\mathcal{T} = ( u_1, \dotsc, u_M ), \quad u_j \in \mathcal{V}_{\mathrm{text}} \cup \mathcal{V}_{\mathrm{img}}$$

每个 $u_j$ 可以是文本 token 或图像 token，二者通过 `<BOI>`/`<EOI>` 分隔符在序列中明确区分。这一设计使得指令形式极其灵活——例如 “Pick up the <BOI><image><EOI> and place it in the drawer” 可以在文本中任意位置嵌入目标物体的视觉参考。

### 模块间协作关系

三个模块形成闭环协作：

- **适配模块**是架构层面的最小侵入式修改，它使得 tokenizer 能够解析交错序列，将图像 token 与文本 token 分别编码后送入共享的 Transformer 骨干。骨干网络本身（如 π0 的 Paligemma 或 OpenVLA 的 Prismatic）不做任何改动。
- **训练流水线**负责生成大规模交错指令数据。其自动生成流程（Figure 3）包含三个步骤：(1) 用 Qwen2.5 从原始文本指令中解析关键物体；(2) 用 OWLv2 进行开放词汇检测并裁剪目标物体区域；(3) 用 Qwen2.5-VL 验证检测质量，必要时结合 Segment Anything 进行精细分割。该流水线的综合准确率达 95.6%。
- **推理接口**利用适配模块的能力，在测试时接受任意形式的交错指令。模型在训练期间从未见过手绘草图或网络图片，但推理时可直接处理这些模态，展现出涌现式的零样本泛化能力（Table 4）。

### 与基线方法的关键差异

相比现有 VLA 方法，Interleave-VLA 的独特之处在于（Table 1）：

| 特性 | Text-VLA（π0, OpenVLA 等） | Interleave-VLA |
|------|---------------------------|----------------|
| 指令模态 | 纯文本 | 图文任意交错 |
| 外部数据依赖 | 部分方法需仿真/互联网数据 | 仅复用现有具身数据集 |
| 骨干侵入性 | — | 零侵入（仅修改 tokenizer） |
| 可迁移性 | — | 已验证 π0 和 OpenVLA 双骨干 |

### 推断效率

尽管输入中增加了图像 token，推断延迟的增长高度可控。在输入图像数量 $n < 10$ 时，延迟近似为 $t = 1.2 n^{2} + 1.5 n + 221$ 秒（Figure 9），二次项系数极小，实际使用中额外开销几乎可忽略。

## 核心模块与公式推导

### 问题形式化

Interleave-VLA 将机器人操作建模为条件动作生成问题。策略 $\pi_\theta$ 在状态 $s_t$ 下生成动作 $a_t$：

$$a_t \sim \pi_{\theta}( \cdot \mid s_t )$$

其中状态由三部分组成——当前视觉观测 $I_t$、本体感知状态 $\mathbf{q}_t$、以及交错指令序列 $\mathcal{T}$：

$$s_t = ( I_t, \mathbf{q}_t, \mathcal{T} )$$

交错指令序列 $\mathcal{T}$ 定义为有序的 token 序列，每个 token 来自文本词表 $\mathcal{V}_{\mathrm{text}}$ 或图像词表 $\mathcal{V}_{\mathrm{img}}$：

$$\mathcal{T} = ( u_1, \dotsc, u_M ), \quad u_j \in \mathcal{V}_{\mathrm{text}} \cup \mathcal{V}_{\mathrm{img}}$$

这一形式化将指令从单一文本模态扩展为图文任意交错的序列，使任务目标获得显式视觉定位，是后续所有模块设计的数学基础。

### 轻量级适配模块（Adaptation Module）

该模块是 Interleave-VLA 的核心技术杠杆。其关键设计在于**仅修改 tokenizer 而不改动 VLA 骨干架构**：在 tokenizer 中引入一对特殊分隔符 `<BOI>`（Begin of Image）和 `<EOI>`（End of Image），用于在 token 序列中显式标记图像 token 的边界。这使得现有 VLA 模型无需任何架构变更即可原生区分文本 token 与图像 token，从而处理图文交错输入。

适配模块的工作流程如下（见 Figure 2）：
1. **输入处理器更新**：接收交错指令序列，在图像 token 前后插入 `<BOI>` / `<EOI>` 分隔符，形成带标记的统一 token 流。
2. **骨干保持不变**：带标记的 token 流送入原有 VLA 骨干（如 π0 的 Paligemma 架构），模型通过分隔符隐式学习图文模态的对齐与区分。
3. **训练目标保留**：训练沿用原始 VLA 的流匹配目标（flow matching objective）和超参数，不引入额外损失项。

该设计的因果机制在于：分隔符为模型提供了模态边界信号，使注意力机制能够在推理时将视觉提示图像与观测图像进行跨模态对齐，从而缓解纯文本条件下的注意力幻觉。

### 交错数据集训练流水线（Scalable Training Pipeline）

训练流水线由三个自动步骤构成（见 Figure 3），用于将大规模开放具身数据集转化为交错图文指令训练数据：

1. **指令解析（Instruction Parsing）**：使用 Qwen2.5 从原始文本指令中提取关键目标物体名称。
2. **开放词汇检测（Open-Vocabulary Detection）**：使用 OWLv2 在轨迹帧中定位并裁剪目标物体区域，生成任务特定图像。
3. **数据质量验证（Data Quality Verification）**：使用 Qwen2.5-VL 验证检测结果，必要时通过 Segment Anything 进行更精确的分割。

该流水线在 210k 个 episode、1300 万帧数据上运行，覆盖约 3500 个独特物体。OWLv2 单独检测准确率为 82.6%，结合 VLM 验证和分割后综合准确率提升至 95.6%。训练时，模型使用该交错数据集进行标准训练，不修改原始 VLA 的超参数或流匹配目标。

### 通用推理接口（Versatile Inference Interface）

推理接口的核心能力是在测试时灵活接受任意来源的指令图像——包括摄像头实时裁剪、网络图片、手绘草图——而无需在训练中见过这些模态。接口将任意图像编码后插入 `<BOI>` / `<EOI>` 之间，与文本指令拼接为交错序列送入模型。

关于推断延迟，当输入图像数量 $n < 10$ 时，延迟 $t$（秒）近似为：

$$t = 1.2 n^{2} + 1.5 n + 221$$

二次项系数极小（1.2），表明在实用图像数量范围内，增加指令图像带来的额外延迟开销有限。

### 关键公式汇总

| 公式 | 含义 | 锚点 |
|------|------|------|
| $a_t \sim \pi_{\theta}( \cdot \mid s_t )$ | 策略条件动作生成 | Section 3.1 |
| $s_t = ( I_t, \mathbf{q}_t, \mathcal{T} )$ | 状态包含视觉、本体感知、交错指令 | Section 3.1 |
| $\mathcal{T} = ( u_1, \dotsc, u_M )$ | 图文交错 token 序列 | Section 3.1 |
| $t = 1.2 n^{2} + 1.5 n + 221$ | 推断延迟与图像数量的关系 | Figure 9, Appendix D.3 |

### 模块间因果链路

三个模块形成闭环：适配模块提供模态区分能力（分隔符）→ 训练流水线提供大规模多模态监督信号（交错数据）→ 推理接口将训练获得的跨模态对齐能力泛化到未见指令形式。这一链路的核心因果机制是：**通过分隔符在 token 空间显式标记图像边界，使注意力机制在推理时能够将指令中的视觉线索与观测中的目标物体对齐，从而消除纯文本条件下的注意力幻觉**——这是 Interleave-VLA 在 OOD 任务上实现 2-3 倍泛化提升的根本原因。

## 实验与分析

### 核心瓶颈验证：注意力幻觉的定量解构

Interleave-VLA的核心主张在于，图文交错指令能够有效缓解纯文本VLA模型在分布外场景下的注意力幻觉。Figure 11提供了这一因果链条的直接证据：在SimplerEnv的所有任务类别上，Text-VLA的失败案例中高层意图错误（Jitter、Wrong Intention）占比显著更高，尤其在语义泛化任务上，这些错误直接源于模型对目标物体的注意力偏差、注意力分散或注意力泄露。相比之下，Interleave-VLA将绝大多数残余失败压缩至低层执行错误（Grasp Failed、Place Failed），高层幻觉被大幅抑制。这一定量解构表明，**注意力幻觉是文本VLA泛化失败的主要瓶颈，而交错视觉线索通过提供显式上下文定位，从根源上切断了这一失效路径**。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_ULTWUuGhC3/figures/028_Figure_11.jpg]]
*Figure 11: Quantitative hallucination analysis of $\pi _ { 0 }$ with text-only instructions (Text-VLA) and interleaved image–text instructions (Interleave-VLA). Across all task categories, Interleave-VLA achieves higher overall success rates. Each failed rollout is attributed to a single failure mode: highlevel intention errors (Jitter, Wrong Intention) or low-level execution errors (Grasp Failed, Place Failed). Interleave-VLA substantially reduces high-level hallucinations, with most residual failures arising from low-level action generation. In contrast, Text-VLA exhibits significantly more highlevel intention errors, particularly in out-of-domain scenarios, leading to reduced overall success*

### 主结果：分布外泛化的2–3倍增益

**SimplerEnv仿真基准（Table 2）** 构成了最系统的对比证据。在In-Domain的4项任务上，Interleave-VLA（Full）与Text-VLA（π₀）性能基本持平（73.0 vs 72.8），证明交错训练未损害已知任务能力。真正的分化出现在三组Out-of-Domain评估套件上：

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_ULTWUuGhC3/figures/008_Table_2.jpg]]
*Table 2: Interleave-VLA and Text-VLA comparison on SimplerEnv. In-Domain includes 4 tasks following SimplerEnv-Bridge setup. We add 3 Out-of-Domain evaluation suites, namely: Visual, Novel Object, and Novel Category. $\pi _ { 0 }$ with full adaptation (Interleave-VLA Full) performs better than $\pi _ { 0 }$ with no adaptation (Text-VLA) by over 2 $\times$ in out-of-domain semantic generalization tasks. It also outperforms $\pi _ { 0 . 5 }$ which enjoys additional pretraining with additonal object grounding and detection VQA data. Results are evaluated on 3 seeds. We use bold and underline to represent the $1 ^ { s t }$ and $2 ^ { n d }$ highest. For quantitative breakdown of failure modes, please refer to Figur...

- **Visual Generalization**：Interleave-VLA Full达到60.0，较Text-VLA的50.6提升约9个百分点，表明视觉线索对未见场景的鲁棒性贡献。
- **Novel Object**：53.8 vs 48.5，增益相对温和，因为已知类别的未见物体仍与训练分布存在语义关联。
- **Novel Category**：57.3 vs 19.3，差距急剧扩大至**约3倍**。这是全文最具决定性的证据——当任务涉及训练中完全未见的物体类别时，纯文本指令因语言歧义和分布偏移导致注意力幻觉全面爆发，而交错图像指令通过直接展示目标外观，从根本上消除了歧义。

综合Out-of-Domain平均成功率，Interleave-VLA Full达到60.6±1.1，Text-VLA仅为39.5±0.5，提升幅度超过53%。值得注意的是，Interleave-VLA Partial（训练时使用交错数据但测试时仅用文本指令）在Out-of-Domain上也达到43.6±0.6，说明**交错训练本身已通过跨模态学习改善了模型的语义理解**，但完整的交错推理才能释放全部泛化潜力。

**真实机器人实验（Table 3）** 进一步验证了这一结论在物理世界中的可迁移性。在FANUC LRMate 200iD/7L平台上，当两者均经过开放交错具身数据集预训练（PT）后：

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_ULTWUuGhC3/figures/010_Table_3.jpg]]
*Table 3: Comparison of success rates (Succ) and correct object picking rates (Acc) in real-robot experiments. All the baselines use the base VLA model π0. Interleave-VLA adapted achieves 2- 3× higher out-of-domain performance compared to Text-VLA. “PT” indicates pretraining on our interleaved dataset built in Section 3.3. Notably, although the pretraining dataset does not include FANUC robot arm data, it still enables strong cross-embodiment transfer to FANUC*

- **Out-of-Domain Food Lift**：Interleave-VLA平均成功率达71%，Text-VLA仅为13%，增益约5.5倍。
- **Out-of-Domain Kitchenware Pick&Place**：Interleave-VLA为38%，Text-VLA为21%，增益约1.8倍。

关键公平性说明：预训练数据**不包含**FANUC机器人平台数据，因此这些增益体现了跨实体迁移能力。此外，In-Domain任务上两者差距有限（Food Lift 83% vs 75%，Kitchenware 67% vs 58%），再次确认交错范式不会损害已知场景性能。

**VIMA-Bench跨模型验证（Table 14，Figure 6）** 排除了骨干模型特异性。将Interleave-VLA范式应用于OpenVLA后，在所有四个泛化级别上均取得约2倍提升：L1（物体放置）从53.71跃升至83.14，L2（新颖组合）从23.00升至58.14，L3（新颖物体）从23.86升至64.00，L4（新颖任务）从4.29升至17.29。这一跨骨干、跨任务套件的证据强烈支持Interleave-VLA的**模型无关性**。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_ULTWUuGhC3/figures/030_Table_14.jpg]]
*Table 14: Detailed VIMA-Bench results for L1, L2, and L3 level generalization evaluations. Interleave-VLA generally outperforms other VLA models and improves the generalization capacity of OpenVLA (Kim et al., 2024) by over 2×*

### 消融：指令格式与提示图像多样性的解耦

Table 6通过对比三种指令格式，分离了**格式效应**与**内容效应**：

- **Text指令**在Unseen Object和Unseen Category上分别仅取得29.0和25.8，构成性能下界。
- **Visual Goal指令**（仅提供目标图像，无文本交错）将两项指标提升至41.8和42.9，证明了显式视觉目标信息对分布外泛化的直接驱动作用。
- **Interleaved Img-Text指令**进一步将指标推高至53.9和54.2，揭示了交错格式的**互补增益**：文本提供任务语义框架，图像提供目标定位锚点，两者协同避免了"Move Near"等模糊指令的歧义。

Table 5则揭示了训练数据中提示图像多样性的关键作用。在Out-of-Domain场景下，仅使用任务特定裁剪图像（Task-specific Only）取得67.1，仅使用互联网图像（Internet Only）取得69.1，而**混合两者**（Mixed）达到71.7。这表明多样化的视觉提示来源（涵盖不同视角、背景和成像条件）是模型学习鲁棒视觉定位的关键规模化因素。

### 零样本指令模态泛化

Interleave-VLA展现出训练期间未见过的指令模态的零样本处理能力（Section 4.3.2，Table 4）。在真实机器人场景中，模型可直接接受：

- **手绘草图**：用户快速绘制的目标物体简笔画
- **用户裁剪图像**：从实时摄像头画面中手动裁剪的目标区域
- **互联网照片**：从网络检索的同类物体参考图像

Table 8（原文Table 7）的草图鲁棒性测试提供了更精细的刻画：对于清晰草图（Normal、OCR、Quick），模型成功率和意图准确率保持在81%–96%的高位；但当草图高度抽象（Abstract）或系统性误导（Mislead）时，性能急剧下降至15%–56%，揭示了当前多模态推理在处理**语义矛盾或高度符号化视觉输入**时的脆弱性。

### 推理效率与骨干鲁棒性

Figure 9给出了推理延迟与输入图像数量的关系：$t \approx 1.2n^2 + 1.5n + 221$（毫秒级），其中二次项系数极小。在1–2张图像的典型使用场景下，推理成本与纯文本VLA相当；即使扩展到10张图像，延迟增长仍保持在可控范围内（约355 ms）。Table 11进一步证实，将Interleave-VLA适配到不同VLM骨干（如OpenVLA的不同视觉编码器）时，性能差异可忽略，验证了其**骨干无关的即插即用特性**。

### 失败模式与局限性

尽管整体性能提升显著，定量分析仍揭示了明确的失效边界：

1. **低层执行错误的残余**：Figure 11显示，即使高层意图正确，Grasp Failed和Place Failed仍是Interleave-VLA的主要失败来源，说明视觉定位的改善无法弥补动作生成的底层缺陷。
2. **误导性视觉提示的脆弱性**：Table 8中Mislead草图的意图准确率骤降至20.8%，表明模型在面对文本-图像语义矛盾时倾向于信任图像线索，缺乏有效的跨模态冲突消解机制。
3. **纯文本评估的提升有限**：Interleave-VLA Partial在Out-of-Domain上仅比Text-VLA提升约4个百分点（Table 2），说明交错视觉线索的**测试时提供**是泛化增益的必要条件，而非充分条件。
4. **数据生成流水线的边界**：尽管OWLv2与Qwen-VL协同检测的综合错误率低至4.4%，极端视角、光照或遮挡场景下的检测失败仍可能引入噪声训练样本，影响模型对特定物体类别的学习质量。

## 方法谱系与知识库定位

### 问题定位与核心瓶颈

现有视觉-语言-动作（VLA）模型在机器人操作任务中的泛化能力受限于一个关键瓶颈：**注意力幻觉**（attentional hallucination）。当面对训练分布之外的未见物体和场景时，纯文本指令 VLA 模型（Text-VLA）由于语言歧义和训练分布偏差，表现出三种系统性的注意力失效模式（Figure 5）：

1. **注意力偏差**（Attentional Bias）：模型将注意力错误地集中在显著的干扰物上，而非真实目标物体。
2. **注意力分散**（Diffused Attention）：注意力广泛散布而无主导焦点，表明模型对目标存在不确定性。
3. **注意力泄露**（Attention Leakage）：目标被部分关注，但注意力溢出到无关背景或干扰区域。

定量分析（Figure 11）证实：Text-VLA 的失败主要源于高层意图错误（错误意图、抖动），而非底层执行失败（抓取失败、放置失败）。这一发现揭示了问题本质是**语义理解与视觉定位的脱节**，而非动作生成的精度不足。

### 方法谱系：Interleave-VLA 的定位

Interleave-VLA 在现有 VLA 方法谱系中占据独特位置。Table 1 将其与代表性方法进行了系统对比：

**纯文本 VLA 基线**：
- **RT-1-X**（Brohan et al., 2022）、**Octo**（Team et al., 2024）：早期通用机器人策略，仅接受文本指令输入，缺乏视觉目标定位能力。
- **π0 (Text-VLA)**（Black et al., 2024）：本文的直接基线，使用 Paligemma 骨干的标准 VLA 架构，仅支持文本指令。在语义分布外任务上泛化严重受限（SimplerEnv Novel Category 仅 19.3%，Table 2）。
- **π0.5**（Intelligence et al., 2025）：π0 的增强版本，额外使用目标定位和检测 VQA 数据进行预训练。尽管性能有所提升，但在语义泛化上仍显著弱于 Interleave-VLA（Table 2：Novel Category 40.7 vs 57.3）。
- **OpenVLA**（Kim et al., 2024）：另一先进 Text-VLA 模型，Interleave-VLA 将其在 VIMA-Bench 上的泛化能力提升超过 2 倍（Table 14：L3 从 23.86 提升至 64.00），证明了范式的骨干无关性。

**视觉目标 VLA 方法**：
- **Spatial-VLA**（Qu et al., 2025）：具备空间推理能力的 VLA 模型，但依赖于固定的骨干架构。
- **VIMA 系列**（Jiang et al., 2023）：包括 **VIMA-Gato**、**VIMA-Flamingo**、**VIMA-GPT**，支持多模态提示但依赖任务特定设计。Interleave-VLA 在 VIMA-Bench 上不依赖任何任务特定设计即取得最优性能（Figure 6）。

**Interleave-VLA 的差异化优势**（Table 1）：
- **即插即用**：作为骨干无关的插件运行，无需修改核心架构。
- **无外部数据依赖**：复用现有机器人数据集，不依赖外部数据采集或仿真引擎。
- **自动数据增强**：通过自动流水线从现有数据生成图文交错指令。
- **灵活推理**：支持文本、裁剪图像、网络图片、手绘草图等任意模态组合的零样本推理。

### 因果机制：图文交错如何缓解注意力幻觉

Interleave-VLA 的核心洞察在于：通过在 VLA 模型的 tokenizer 中引入特殊分隔符 `<BOI>` 和 `<EOI>`，使现有架构无需修改即可原生处理图文交错输入。这一轻量级适配（Section 3.2, Appendix D.1）改变了三个关键槽位：

| 槽位 | 基线值（Text-VLA） | Interleave-VLA 值 |
|------|-------------------|-------------------|
| 指令输入格式 | 单文本指令 | 图文交错指令序列（图像-文本任意交错） |
| Tokenizer 特殊标记 | 无 | `<BOI>` / `<EOI>` 分隔符区分图像与文本 token |
| 训练数据指令类型 | 仅文本标签 | 自动生成的交错图文指令（含任务特定裁剪 + 互联网图像） |
| 模型架构 | 标准 VLA 骨干 | 骨干不变，仅修改输入处理器 |

因果链条可归纳为：
1. **上下文视觉线索** → 为任务目标提供显式视觉定位，消除语言歧义。
2. **跨模态训练** → 模型学习对齐文本语义与视觉外观，增强对未见物体的鲁棒性。
3. **注意力聚焦** → 视觉提示引导注意力集中于目标区域，系统性减少注意力偏差、分散和泄露。

消融实验（Table 6）进一步揭示了**格式**与**内容**的互补贡献：视觉目标线索通过提供显式图像信息驱动分布外泛化，而交错格式提供额外增益并防止模糊目标（如“Move Near”）的任务歧义。

### 适用边界与局限

**已知局限**（论文明确指出的失效模式）：

1. **纯文本评估增益有限**：当测试时不提供任何交错图像指令，Interleave-VLA（Partial）仅表现出有限提升（Table 2：Out-of-Domain Avg 43.6 vs 39.5）。交错视觉线索的提供是泛化增益的关键前提。

2. **缺乏历史感知能力**：当前架构未考虑历史观察，难以处理需要时间记忆的任务。扩展到历史感知的交错指令场景是明确的未来方向。

3. **多模态推理的脆弱性**：对高度抽象、误导或模糊的草图指令，模型性能急剧下降。Table 7 显示：正常草图成功率 95.8%，但抽象草图降至 56.3%，误导性草图仅 14.6%。这表明模型在多模态推理中仍存在脆弱性，尤其当图文信息矛盾时。

4. **数据流水线的边缘案例**：数据生成流水线依赖 OWLv2 和 Qwen-VL 的协同检测。尽管综合错误率低至 4.4%（Section 3.3），但在极端视角、光照或遮挡场景下仍有失败案例，影响训练数据质量。

5. **任务与平台覆盖有限**：实验主要在有限类别的桌面操作任务上进行（SimplerEnv 的 4 个域内任务 + 3 个分布外套件，真实机器人 2 类物体操作）。更大规模、更多样化的跨实体测试和真正零样本在线部署尚未充分验证。

**适用边界推断**：
- **强适用场景**：目标物体视觉外观可获取（摄像头裁剪、参考图像、清晰草图）、需要区分视觉相似但语义不同的物体、分布外泛化需求突出的场景。
- **弱适用场景**：目标无法通过静态图像有效描述（如动态操作序列）、高度依赖语言抽象推理的任务、无法提供任何视觉参考的纯文本指令场景。

### 开放问题

1. **鲁棒多模态推理**：如何为交错指令 VLA 模型设计更强的推理机制，以稳健处理不明确或系统性误导的视觉提示（例如错误关联的草图）？当前模型在图文矛盾时表现出脆弱性（Table 7），需要更深入的跨模态对齐与冲突消解机制。

2. **时序扩展**：交错指令范式如何扩展到需要历史记忆和长期规划的任务？例如在指令中包含多步图文指示，或利用历史观察帧作为上下文线索。

3. **数据流水线鲁棒性**：自动流水线如何处理原始文本指令中的歧义或噪声，尤其在长文本描述的数据集上？当前流水线依赖 LLM 解析，其对复杂指令的鲁棒性有待系统评估。

4. **因果量化**：如何量化注意力幻觉的减少与泛化性能提升之间的因果关系？Figure 11 提供了定性证据，但缺乏严格的因果中介分析。不同模态分布偏移下的泛化极限也尚未被理论刻画。

5. **缩放规律**：在更大规模、更多样化的机器人和任务中，交错图文指令的多模态缩放规律是什么？Table 17 的协同训练实验表明跨数据集扩展能进一步提升性能，但数据规模、模态多样性与性能之间的定量关系尚未建立。

## 原文 PDF

![[paperPDFs/ICLR_2026/Interleave_VLA_Enhancing_Robot_Manipulation_with_Image_Text_Interleaved_Instructions.pdf]]
