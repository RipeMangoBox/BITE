---
title: Qwen3-VL Technical Report
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Qwen3_VL_Technical_Report.pdf
project_link: https://likaixin2000.github.io/papers/ScreenSpot\_Pro.pdf
code_link: https://github.com/QwenLM/Qwen3-VL
aliases:
- QV
- QVTR
tags:
- arxiv_2025
- topic/other_unclear
- topic/other_unclear/general
core_operator: 交错 MRoPE（Interleaved MRoPE）、DeepStack 多层视觉特征注入、文本化时间戳（text-based timestamps）、平方根重加权损失（square-root reweighting）。
primary_logic: 通过平衡频谱均匀分配空间‑时间维度的频率、跨层注入多级视觉特征以及引入显式文本时间戳，Qwen3‑VL 在不牺牲语言能力的情况下强化了多模态时空建模与视觉‑语言对齐，并采用平方根重加权损失进一步平衡文本与多模态训练信号。
claims:
- Interleaved MRoPE 通过均匀分配 t/h/w 频率克服原有频谱倾斜，提升长视频位置编码能力。
- DeepStack 将 ViT 多层视觉特征注入 LLM 前三层，显著提升细粒度视觉理解（InfoVQA 71.9→74.2，DocVQA 89.5→91.1）。
- 文本化时间戳取代 T‑RoPE，提供更直接的时间表示，便于视频定位。
- 平方根重加权 per‑token loss 改善多模态与文本训练平衡，提升多模态性能且不损害文本能力。
---

# Qwen3-VL Technical Report

> [!tip] 核心洞察
> 通过平衡频谱均匀分配空间‑时间维度的频率、跨层注入多级视觉特征以及引入显式文本时间戳，Qwen3‑VL 在不牺牲语言能力的情况下强化了多模态时空建模与视觉‑语言对齐，并采用平方根重加权损失进一步平衡文本与多模态训练信号。

| 字段 | 内容 |
|------|------|
| 中文题名 | Qwen3-VL 技术报告 |
| 英文题名 | Qwen3-VL Technical Report |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2512.00435) · [Code](https://github.com/QwenLM/Qwen3-VL) · [paper](https://arxiv.org/abs/2501.00321) · [Project](https://likaixin2000.github.io/papers/ScreenSpot\_Pro.pdf) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Qwen3-VL |
| Dataset | MMLU‑Pro, HallusionBench, MIA‑Bench |

> [!tip] 效果简介
> - MMLU‑Pro 上，Accuracy 78.6 vs 71.9 (Qwen3‑32B‑Instruct) (+6.7)。
> - HallusionBench 上，Accuracy 66.7 vs 60.4 (Claude opus 4.1) (+6.3)。
> - MMLU‑Pro (Thinking) 上，Accuracy 82.1 vs 79.1 (Qwen3‑32B‑Thinking) (+3.0)。

## 概要

Qwen3-VL 是通义千问团队推出的新一代多模态大模型，其核心目标是在不牺牲纯文本语言理解能力的前提下，强化视觉‑语言对齐与长视频时空建模。此前，多模态训练普遍存在一个关键瓶颈：引入视觉数据容易损害模型原有的纯文本能力，同时长视频中的时序对齐也面临显著困难。Qwen3-VL 通过四项关键设计来应对这一挑战：

1. **交错 MRoPE（Interleaved MRoPE）**：将时间、高度、宽度三个维度的位置编码均匀交错分配到低高频带，解决了原版 MRoPE 将维度分块导致的频谱倾斜问题，从而获得更均衡的位置表示，提升长视频时空建模能力。
2. **DeepStack 多层视觉注入**：选取视觉编码器三个不同深度的中间层特征，经专用融合模块分别注入大语言模型的前三层，在不增加上下文长度的情况下实现多层级视觉‑语言融合，显著增强细粒度视觉理解。
3. **文本化时间戳**：用显式的时间文本标记（如 `<3.0 seconds>`）替代 Qwen2.5-VL 中通过位置编码实现的绝对时间对齐，为视频帧组提供更直接的时间表示，简化视频定位任务。
4. **平方根重加权损失**：将训练损失从 per‑sample 转为平方根归一化的 per‑token 损失，更均衡地分配文本与多模态数据的训练信号，在提升多模态性能的同时保持甚至增强纯文本能力。

在方法谱系上，Qwen3-VL 延续了 Qwen2.5-VL 的三模块架构（视觉编码器 → MLP 视觉‑语言融合器 → 大语言模型），但在位置编码、视觉融合深度、视频时间表示和训练损失四个关键维度上进行了系统性改进。视觉编码器采用 SigLIP‑2 架构并支持动态分辨率，大语言模型基于 Qwen3 系列，覆盖从 2B 到 235B-A22B 的密集与 MoE 变体。

实验结果表明，Qwen3-VL 在多项基准上取得了显著提升：旗舰模型（235B-A22B）在 HallusionBench 上以 66.7 的准确率超越 Claude opus 4.1（60.4），在 MIA‑Bench 上以 92.7 略超 Gemini‑2.5‑Pro（92.3）；中等模型（32B）在 MMLU‑Pro 上达到 78.6，较纯文本基线 Qwen3‑32B‑Instruct（71.9）提升 6.7 个百分点，验证了多模态训练对语言能力的保持。消融实验进一步证实，DeepStack 使平均基准评分从 74.7 提升至 76.0，视频 Needle‑in‑a‑Haystack 测试在 256K token（约 30 分钟）内达到 100% 准确率。

值得注意的是，报告中仍存在若干待验证的开放问题：Interleaved MRoPE 在不同视频长度和帧率下的增益是否均匀、DeepStack 引入的额外参数与推理延迟对部署效率的影响、文本化时间戳在超长视频（超过 1 小时）中的有效性，以及平方根重加权损失与其他缩放策略的直接对比等，这些均需进一步消融或实际部署验证。

视觉语言模型（VLM）在通用视觉理解、文档解析和视频分析等任务上已取得显著进展，但两个核心瓶颈始终制约着模型的进一步突破：

**多模态训练对纯文本能力的侵蚀。** 当 LLM 被扩展为 VLM 后，视觉数据的引入往往会损害其原有的语言理解与推理能力。如何在强化视觉感知的同时保持文本基座模型的完整能力，是多模态训练中一个长期被低估却至关重要的问题。

**长视频时空对齐的频谱偏差。** 现有方法（如 Qwen2.5-VL 采用的 MRoPE）将位置编码维度按时间（t）、高度（h）、宽度（w）分块分配频率，导致频谱在不同维度间倾斜分布，使模型在长视频场景下的时序定位和跨帧理解能力受限。此外，基于位置编码的绝对时间对齐（T‑RoPE）提供的时间信号过于隐式，不利于模型直接建模视频的时间结构。

Qwen3‑VL 的动机正是围绕这两个瓶颈展开：**在不牺牲语言能力的前提下，通过架构创新强化多模态时空建模与视觉‑语言对齐**。具体而言，报告提出了四项关键设计——交错 MRoPE（Interleaved MRoPE）均匀分配空间‑时间维度的频率以消除频谱偏差；DeepStack 多层视觉特征注入以增强细粒度视觉理解；文本化时间戳替代 T‑RoPE 以提供更直接的时间表示；以及平方根重加权 per‑token 损失以平衡文本与多模态训练信号。这些设计共同构成了一套从位置编码、特征融合到训练策略的系统性改进方案。

## 核心方法与创新机理

Qwen3-VL 的核心创新围绕一个中心矛盾展开：**多模态训练容易损害纯文本语言理解能力，且长视频时序对齐困难**。针对这一瓶颈，Qwen3-VL 在 Qwen2.5-VL 的基础上进行了四项关键改进，在不牺牲语言能力的前提下强化了多模态时空建模与视觉‑语言对齐。

### 1. 交错 MRoPE：平衡频谱的位置编码

Qwen2.5-VL 采用的 MRoPE 将位置编码维度按时间（t）、高度（h）、宽度（w）分块分配，导致频谱能量向低频倾斜，限制了长视频位置建模能力。Qwen3-VL 提出 **Interleaved MRoPE**，将 t、h、w 三个分量在嵌入维度上交错排列，均匀分布在低频频带与高频频带之间。

> **原文锚点**：*"we redesign the frequency allocation by interleaving the t, h, and w components across the embedding dimensions ... The resulting balanced spectrum mitigates the original spectral bias."*（置信度 0.96）

这一改进的因果逻辑在于：均匀的频率分配使模型能够同时捕捉长程时间依赖（低频）和细粒度空间变化（高频），从而在视频理解任务中获得更忠实的时空位置表征。

### 2. DeepStack：多层视觉特征注入

Qwen2.5-VL 仅使用 ViT 最后一层输出作为视觉 token，导致浅层纹理、边缘等细粒度信息丢失。Qwen3-VL 引入 **DeepStack 机制**：选取视觉编码器三个不同深度的中间层特征，经专用 vision–language merger 投影后，直接注入 LLM 的前三层。

> **原文锚点**：*"we select features from three distinct levels of the vision encoder ... dedicated vision–language merger modules project these multi-level features into visual tokens, which are then added directly to the corresponding hidden states of the first three LLM layers."*（置信度 0.97）

消融实验证实，DeepStack 将平均基准评分从 74.7 提升至 76.0（Table 12），细粒度理解任务提升尤为显著：InfoVQA 从 71.9 升至 74.2，DocVQA 从 89.5 升至 91.1（置信度 0.98）。其设计优势在于：通过残差连接注入多层特征，不增加额外上下文长度，避免了长序列场景下的效率损失。

### 3. 文本化时间戳：显式时间编码

Qwen2.5-VL 通过 T‑RoPE 位置编码实现绝对时间对齐，但这种隐式方式对视频时刻定位不够直接。Qwen3-VL 改用 **基于文本令牌的时间编码**：每个视频时间片段前缀一个格式化的时间戳字符串，如 `<3.0 seconds>`，同时支持秒和时分秒（HMS）两种格式。

> **原文锚点**：*"we replace the absolute-time alignment via positional encoding used in Qwen2.5-VL with explicit timestamp tokens to mark frame groups, providing a simpler and more direct temporal representation."*（置信度 0.95）

这一设计将时间信息从隐式的位置编码空间迁移到显式的文本语义空间，使 LLM 能够像理解自然语言一样理解时间戳，显著简化了视频定位任务的对齐难度。

### 4. 平方根重加权损失：平衡多模态与文本训练信号

多模态训练中，不同模态样本的 token 数量差异巨大，传统 per‑sample loss 会导致长序列（如视频）主导梯度更新，损害纯文本能力。Qwen3-VL 将损失函数从 **per‑sample loss** 改为 **平方根归一化 per‑token loss**。

> **原文锚点**：*"we move from a per-sample loss to a square-root-normalized per-token loss, which better balances the contributions of text and multimodal data during training."*（置信度 0.95）

该策略的核心在于：对每个 token 的损失进行平方根缩放后再求和，抑制了长序列样本的梯度幅值，使文本样本与多模态样本的训练信号趋于均衡。实验表明，这一改进在提升多模态性能的同时，保持了与纯文本 Qwen3 基线（Yang et al., 2025a）相当的语言理解能力（如 MMLU‑Pro 78.6 vs Qwen3‑32B‑Instruct 71.9，Table 7）。

---

**待验证的开放问题**：上述四项创新的消融分析尚不完整。Interleaved MRoPE 在不同视频长度和帧率下的增益均匀性未展开；DeepStack 引入的额外参数与推理延迟未量化；文本化时间戳在超长视频（>1 小时）中的表现及上下文开销未知；平方根重加权与对数平滑等其他缩放策略缺少直接对比。这些点需要后续实验补充验证。

Qwen3‑VL 采用标准的三模块架构：**视觉编码器（Vision Encoder）**、**MLP 视觉‑语言融合器（Vision‑Language Merger）** 以及 **大语言模型（LLM）**。文本、图像和视频三类输入经统一处理后，最终由 LLM 自回归生成回答。其核心设计目标是在不牺牲纯文本语言能力的前提下，强化多模态时空建模与细粒度视觉‑语言对齐。

### 输入处理流

1. **文本输入**：直接经 tokenizer 转换为文本 token 序列，送入 LLM。
2. **图像输入**：以动态分辨率送入视觉编码器，输出多尺度视觉特征图。随后通过两层 MLP 融合器，将每 2×2 空间块压缩为单个视觉 token，并映射到 LLM 的隐空间维度。视觉 token 与文本 token 拼接后共同输入 LLM。
3. **视频输入**：按固定帧率采样为帧序列，每帧独立经视觉编码器提取特征。与 Qwen2.5‑VL 不同，Qwen3‑VL 放弃了通过位置编码实现的绝对时间对齐（T‑RoPE），改为在每组帧的视觉 token 前显式插入**文本化时间戳**（如 `<3.0 seconds>`），同时支持秒和 HMS 格式。这一设计提供了更直接的时间表示，便于视频定位与长程时序理解。

### 位置编码：Interleaved MRoPE

为统一编码文本、图像和视频的位置信息，Qwen3‑VL 在 MRoPE 基础上提出 **Interleaved MRoPE**。原有 MRoPE 将嵌入维度划分为时间（t）、高度（h）、宽度（w）三个连续块，导致频谱能量向低频倾斜。Interleaved MRoPE 将 t、h、w 分量在嵌入维度上交错排列，使三者均匀分布在低、中、高频带上，形成平衡的频谱分布，从而缓解了频谱偏差，提升了长视频位置编码能力。

### 视觉‑语言深度融合：DeepStack

传统 VLM 通常仅使用视觉编码器最后一层的输出作为视觉 token。Qwen3‑VL 引入 **DeepStack 机制**，从视觉编码器中选取三个不同深度的中间层特征，分别通过专用的视觉‑语言融合模块投影为视觉 token，再以残差连接的方式直接注入 LLM 的前三层。这种跨层注入在不增加上下文长度的前提下，实现了多层级的视觉特征融合，显著增强了细粒度视觉理解。

### 训练损失重加权

为平衡文本与多模态训练信号的贡献，Qwen3‑VL 将 per‑sample 损失替换为**平方根归一化的 per‑token 损失**。该重加权策略抑制了长样本（尤其是多模态样本）在训练中的主导效应，从而在不损害纯文本语言能力的同时提升多模态性能。

### 整体数据流示意

Figure 1 给出了完整的框架图：视觉编码器处理动态分辨率的图像/视频帧，经 DeepStack 多层注入与 Interleaved MRoPE 位置编码后，视觉 token 与文本 token 及时间戳 token 共同输入 LLM 进行自回归生成。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2512_00435/figures/003_Figure_1.jpg]]
*Figure 1: The Qwen3-VL framework integrates a vision encoder and a language model decoder to process multimodal inputs, including text, images, and video. The vision encoder is specifically designed to handle dynamic, native-resolution visual inputs, mapping them to visual tokens of variable length. To enhance perceptual capability and preserve rich visual information, we incorporate the pioneering DeepStack mechanism, which injects visual tokens from multiple layers of the vision encoder into corresponding layers of the LLM. Furthermore, we adopt Interleaved MRoPE to encode positional information for multimodal inputs with a balanced frequency spectrum, and introduce text-based timestamp tokens to m...*

### 视觉编码器与动态分辨率处理

Qwen3‑VL 采用 **SigLIP‑2** 架构作为视觉编码器（Tschannen et al., 2025），并在训练中持续使用动态输入分辨率。视觉编码器内部使用 **2D‑RoPE**，根据实际输入尺寸插值绝对位置嵌入，从而原生支持可变分辨率的图像与视频帧输入。视觉编码器输出的特征图经 **两层 MLP 视觉‑语言融合器** 压缩：将每 $2 \times 2$ 的视觉特征块映射为一个视觉 token，使其维度与 LLM 的隐藏层对齐。

### Interleaved MRoPE：平衡频谱的多模态位置编码

针对视频理解中空间‑时间位置编码的频谱倾斜问题，Qwen3‑VL 设计了 **交错 MRoPE（Interleaved MRoPE）**。与 Qwen2.5‑VL 中将位置嵌入维度划分为独立的时间（t）、高度（h）、宽度（w）块的做法不同，Interleaved MRoPE 将 t、h、w 三个分量**均匀交错分布**在嵌入维度的所有频带上。这一设计使得低频和高频区域都能同时承载时间与空间信息，产生**平衡的频谱**，从而缓解原有频谱倾斜对长视频位置建模的损害。该模块是提升视频时序对齐能力的关键因果旋钮。

### DeepStack：多层视觉特征注入

**DeepStack** 机制从视觉编码器中选取三个不同深度的中间层特征，通过各自专用的视觉‑语言融合模块投影为视觉 token，再以残差连接的方式**直接注入 LLM 的前三层**隐藏状态中。不同于仅使用 ViT 最后一层输出的传统方案，DeepStack 将浅层的局部纹理、中层的部件结构和高层的语义信息同时馈入 LLM，在不增加上下文长度的前提下强化了多层级视觉‑语言对齐。消融实验表明，该机制将平均基准评分从 74.7 提升至 76.0，并在细粒度理解任务上带来显著增益（InfoVQA: 71.9→74.2, DocVQA: 89.5→91.1）。

### 文本化时间戳编码

Qwen3‑VL 摒弃了 Qwen2.5‑VL 中通过位置编码实现的 T‑RoPE 绝对时间对齐，转而采用**基于文本令牌的时间编码策略**。每个视频时间片段被前缀一个格式化的时间戳文本字符串（如 `<3.0 seconds>`），同时支持秒和 HMS 格式。这种显式的文本时间表示提供了更直接的时间语义，便于模型通过语言理解能力进行视频定位，同时简化了时间建模的工程复杂度。

### 平方根重加权损失

为平衡文本数据与多模态数据在训练中的贡献，Qwen3‑VL 将损失函数从 **per‑sample loss** 改为**平方根归一化的 per‑token loss**。具体而言，每个 token 的损失按其所属样本的 token 数量的平方根进行重加权，有效抑制了长序列多模态样本对梯度的过度主导，从而在不损害纯文本语言能力的前提下提升多模态性能。该设计是维持文本‑多模态训练平衡的核心机制。

> **注意**：本报告未提供上述模块的具体数学公式推导，原文中亦未给出显式公式定义。若需详细的公式表达与推导，需手动查阅原始技术报告或源码实现。

## 实验与关键发现

### 核心性能验证

Qwen3-VL 在多模态和纯文本基准上均展现了强大的竞争力。旗舰模型 Qwen3-VL-235B-A22B 在视觉基准上与 **Gemini-2.5-Pro**、**GPT-5** 和 **Claude opus 4.1** 等顶级模型进行了全面对比（Table 2）。在 HallusionBench 上，Qwen3-VL 达到 66.7，显著优于 Claude opus 4.1 的 60.4（+6.3）；在 MIA-Bench 上以 92.7 略超 Gemini-2.5-Pro 的 92.3。中等规模模型（30B-A3B/32B）同样表现出色（Table 3），而小模型（2B/4B/8B）在与 GPT-5-nano 的对比中也展现了竞争力（Table 4）。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2512_00435/figures/005_Table_2.jpg]]
*Table 2: Performance of Qwen3-VL-235B-A22B and top-tier models on visual benchmarks. The highest scores of the reasoning and non-reasoning models are shown in bold and underlined, respectively. Results marked with an ∗ are sourced from the technical report. + denotes results with tool use*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2512_00435/figures/006_Table_3.jpg]]
*Table 3: Performance of medium-sized Qwen3-VL models and previous models on visual benchmarks. The highest scores are shown in bold. Results marked with an ∗ are sourced from the technical report. + denotes results with tool use*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2512_00435/figures/008_Table_4.jpg]]
*Table 4: Performance of small-sized Qwen3-VL models and GPT-5-nano on visual benchmarks*

一个关键的验证点是**多模态训练对纯文本能力的保持**。在 MMLU-Pro 上，Qwen3-VL-32B-Instruct 达到 78.6，相比纯文本基线 Qwen3-32B-Instruct 的 71.9 提升了 **+6.7** 点（Table 7），表明模型不仅没有牺牲语言理解，反而实现了增益。在思考模式下，Qwen3-VL-32B-Thinking 在 MMLU-Pro 上达到 82.1，超越纯文本思考基线 Qwen3-32B-Thinking 的 79.1（+3.0，Table 8）。这一现象的核心机制在于**平方根重加权 per-token loss**：通过从 per-sample loss 切换为平方根归一化的 per-token loss，模型在训练中更均衡地分配文本与多模态数据的梯度信号，从而避免多模态数据“淹没”文本能力。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2512_00435/figures/011_Table_7.jpg]]
*Table 7: Comparison among Qwen3-VL-32B-Instruct, Qwen3-VL-30B-A3B-Instruct, and corresponding baselines*

多语言 OCR 能力方面，在自建测试集的 39 种语言中，模型在 32 种语言上达到 70% 以上的准确率（Figure 2），验证了其广泛的实用多语言覆盖。

### 关键消融分析

**1. DeepStack 多层视觉注入的有效性**

DeepStack 机制将 ViT 三个中间层的视觉特征通过专用 merger 注入 LLM 前三层。在基于内部 15B-A2B LLM 的消融实验中（Table 12），加入 DeepStack 使平均基准评分从 74.7 提升至 76.0。在细粒度视觉理解任务上增益尤为显著：InfoVQA 从 71.9 提升至 74.2（+2.3），DocVQA 从 89.5 提升至 91.1（+1.6）。这表明跨层多级视觉特征注入有效强化了视觉-语言对齐，尤其对需要精细视觉感知的文档和图表理解任务。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2512_00435/figures/016_Table_12.jpg]]
*Table 12: Ablation on DeepStack. We conduct the ablation study on the DeepStack using an internal 15B-A2B LLM, with all experiments pretrained on 200 billion tokens. We directly evaluate these pretrained models on the validation sets, without any post-training*

**2. Qwen3-ViT 视觉编码器的改进**

与 SigLIP-2 的对比消融（Table 11）显示，在 CLIP 预训练阶段，Qwen3-ViT 已展现出更好的表征能力。在下游 VLM 阶段（均搭配相同的 1.7B Qwen3 LLM），Qwen3-ViT 在 OmniBench 上达到 45.5，相比 SigLIP-2 的 36.9 提升了 **+8.6** 点，验证了自研视觉编码器的显著优势。

**3. 视频长时理解能力**

视频 Needle-in-a-Haystack 测试（Figure 3）显示，在 256K token（约 30 分钟）以内的视频中，模型在不同时间位置的检索准确率均达到 100%，证明 Interleaved MRoPE 和文本化时间戳机制有效解决了长视频时序对齐问题。

### 公平性评估设置

报告对评估的公平性做了明确约束：
- **检测任务**：在 ODinW-13 上固定检测置信度为 1.0，确保与开源检测专业模型的可比性。
- **3D grounding**：统一到虚拟相机坐标系，固定置信度 1.0，IoU 阈值 0.15。
- **视频评估**：统一采样帧率（Charades-STA 为 4 fps，其余 2 fps），并限制每帧最大 visual tokens。
- **推理设置**：思考模型与指令模型使用不同的采样温度、top-p/top-k 设置，以保证各自模式下的合理比较。

### 待验证的开放问题

尽管主实验和消融结果有力，以下问题仍需进一步验证：
- Interleaved MRoPE 在不同视频长度和帧率下的消融未详细展开，其增益是否在所有场景下均匀尚不明确。
- DeepStack 引入的额外参数、通信和推理延迟未提供量化分析，实际部署效率影响未知。
- 文本化时间戳在极长视频（超过 1 小时）中是否仍优于 T-RoPE，以及引入的上下文长度开销是否可控，缺乏实验支撑。
- 平方根重加权损失与其他缩放策略（如对数平滑）未做直接对比消融。
- Thinking 模型在安全性和幻觉控制方面的鲁棒性未在报告中讨论。

## 定位与知识库关联

### 与先前工作的关系

Qwen3‑VL 在 **Qwen2.5‑VL**（Bai et al., 2025）的基础上进行了四项关键架构改进，同时继承了其动态分辨率视觉编码和 MLP‑based vision‑language merger 的基本框架。

**位置编码的演进**：Qwen2.5‑VL 采用的 MRoPE 将位置嵌入维度按 t（时间）、h（高度）、w（宽度）划分为三个连续块，导致高频维度被某单一成分主导，产生频谱倾斜。Qwen3‑VL 以 **Interleaved MRoPE** 取代这一方案，将 t/h/w 成分在嵌入维度上交错排布，使三者均匀覆盖低、中、高频带，从而在图像和视频场景中均获得更忠实的空间‑时间位置表征。这一改动直接针对长视频位置编码能力不足的瓶颈。

**视觉‑语言融合的深化**：Qwen2.5‑VL 仅使用 ViT 最后一层输出作为视觉 token。Qwen3‑VL 引入 **DeepStack** 机制，从 ViT 的三个不同深度层提取特征，经专用 vision‑language merger 投影后，以残差方式注入 LLM 的前三层。该设计在不增加上下文长度的前提下，将多尺度视觉信息直接融入语言模型的早期处理阶段，强化了细粒度视觉理解。

**视频时间编码的简化**：Qwen2.5‑VL 通过 T‑RoPE 以位置编码方式实现绝对时间对齐。Qwen3‑VL 转而采用**基于文本令牌的时间戳**（如 `<3.0 seconds>`），在视频时间块前显式插入格式化文本字符串，同时支持秒和 HMS 两种格式。这种更直接的时间表示方式降低了模型对时间信息的隐式推理负担，便于视频定位任务。

**训练损失的重新平衡**：Qwen2.5‑VL 使用 per‑sample loss。Qwen3‑VL 迁移到**平方根归一化的 per‑token loss**，通过平方根重加权缓解文本数据与多模态数据在训练中的贡献失衡，使多模态性能提升的同时不损害纯文本语言理解能力——这是多模态训练中的核心瓶颈之一。

### 与同期旗舰模型的对比定位

在视觉基准上，Qwen3‑VL‑235B‑A22B 与 **Gemini‑2.5‑Pro**、**GPT‑5** 和 **Claude opus 4.1** 等旗舰模型形成竞争。在 HallusionBench 上，Qwen3‑VL 以 66.7 的准确率领先 Claude opus 4.1（60.4）达 6.3 点；在 MIA‑Bench 上以 92.7 略胜 Gemini‑2.5‑Pro（92.3）。在纯文本基准上，Qwen3‑VL‑235B‑A22B 的 Instruct 和 Thinking 变体在 MMLU‑Pro 等指标上分别达到 78.6 和 82.1，相比同规模的纯文本 Qwen3‑32B 基线（71.9 和 79.1）均有显著提升，验证了多模态训练未损害语言能力的设计目标。

### 适用边界与局限

**视觉编码器的依赖**：Qwen3‑VL 的视觉编码器基于 **SigLIP‑2**（Tschannen et al., 2025）架构，并持续以动态分辨率训练。消融实验（Table 11）表明，在 1.7B LLM 规模下，Qwen3‑ViT 在 OmniBench 上相比 SigLIP‑2 提升 8.6 点（45.5 vs 36.9），但该优势是否随模型规模扩大而保持尚未验证。

**DeepStack 的效率成本**：DeepStack 引入额外参数和跨层通信，其推理延迟和内存开销未在报告中量化。在 15B‑A2B 的内部消融中，DeepStack 将平均基准评分从 74.7 提升至 76.0（Table 12），但实际部署中的性价比权衡需要手动评估。

**视频理解的上下文边界**：视频 Needle‑in‑a‑Haystack 实验（Figure 3）显示，模型在 256K token（约 30 分钟）以内达到 100% 准确率。超过该时长后性能是否退化，以及文本化时间戳在极长视频（>1 小时）中是否仍优于 T‑RoPE，报告未提供数据。

**公平性评估的约束**：报告在 ODinW‑13 上固定检测置信度为 1.0、在 3D grounding 中统一虚拟相机坐标系并固定 IoU 阈值 0.15，这些标准化设置保证了与专业检测模型的可比性，但也意味着模型在实际应用中可能需要额外的后处理调优。

### 开放问题

1. **Interleaved MRoPE 的场景依赖性**：不同视频长度和帧率下的消融未展开，其增益是否在所有时序场景下均匀分布尚不明确。
2. **DeepStack 的部署效率**：额外参数、跨层通信和推理延迟缺乏量化分析，对实际系统集成的影响未知。
3. **文本化时间戳的扩展性**：在超过 1 小时的视频中是否持续优于 T‑RoPE，以及引入的上下文长度开销是否可控，需要进一步验证。
4. **损失重加权策略的比较**：平方根重加权与对数平滑等其他缩放策略之间缺少直接对比消融。
5. **Thinking 模型的鲁棒性**：报告未讨论 Thinking 变体在安全性、幻觉控制和对抗鲁棒性等方面的表现。

## 原文 PDF

![[paperPDFs/arxiv_2025/Qwen3_VL_Technical_Report.pdf]]
