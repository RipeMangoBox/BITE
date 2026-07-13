---
title: "Thinking with Video: Video Generation as a Promising Multimodal Reasoning Paradigm"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Thinking_with_Video_Video_Generation_as_a_Promising_Multimodal_Reasoning_Paradigm.pdf
project_link: null
code_link: "https://github.com/tongjingqi/Thinking-with-Video"
huggingface_link: "https://huggingface.co/datasets/OpenMOSS-Team/VideoThinkBench"
aliases:
- TV
- TVVGAPMRP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 引入视频生成作为推理链的媒介，通过在视频帧中绘制、操作视觉元素并嵌入文字，实现动态推理与多模态融合。
primary_logic: 视频生成模型天然具备动态渲染与空间操作能力，能够将文本逻辑与视觉想象融合在同一时间序列中，构成一种统一的类人多模态推理范式。
claims:
- 在视觉中心的眼球谜题（Eyeballing Puzzles）上，Sora‑2 的平均准确率显著超越 GPT‑5（领先约 10%），证明其通过绘制与想象进行空间推理的优势。
- 在文本中心的 MATH-500 基准上，Sora‑2 的音频回答准确率达到 92.0%，接近或可比肩顶级 VLM；在 GSM8K 上达 98.9%。
- Sora‑2 的文本中心推理能力很大程度上源于其内部 Prompt Rewriter，禁用重写后 Wan 2.5 的推理能力几乎消失。
- Sora‑2 具备少样本学习能力，提供更多示例（few‑shot）相比单示例（1‑shot）能显著提升 ARC‑AGI‑2 上的像素准确率。
---

# Thinking with Video: Video Generation as a Promising Multimodal Reasoning Paradigm

> [!tip] 核心洞察
> 视频生成模型天然具备动态渲染与空间操作能力，能够将文本逻辑与视觉想象融合在同一时间序列中，构成一种统一的类人多模态推理范式。

| 字段 | 内容 |
|------|------|
| 中文题名 | 用视频思考：视频生成作为一种有前景的多模态推理范式 |
| 英文题名 | Thinking with Video: Video Generation as a Promising Multimodal Reasoning Paradigm |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.04570) · [Code](https://github.com/tongjingqi/Thinking-with-Video) · [HuggingFace](https://huggingface.co/datasets/OpenMOSS-Team/VideoThinkBench) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | Thinking with Video |
| Dataset | Eyeballing Puzzles, MATH‑500, GSM8K, MathVista |

> [!tip] 效果简介
> - Eyeballing Puzzles (Vision‑Centric) 上，Average Accuracy (%) 44.7 (Point) / 38.0 (Line) / 34.5 (Shape) vs GPT‑5 high: 33.6 / 24.0 / 32.5 (约 +10%（Point）)。
> - MATH‑500 (Text‑Centric, Audio) 上，Accuracy (%) 92.0 vs GPT‑5 high: 99.0 (-7.0%)。
> - GSM8K (Text‑Centric, Audio) 上，Accuracy (%) 98.9 vs GPT‑5 high: 100.0 (-1.1%)。

## 概要

### 1. 问题背景与瓶颈

当前主流的多模态推理范式可概括为“用文本思考（Thinking with Text）”和“用图像思考（Thinking with Images）”。这两条路线存在两个根本性瓶颈：

*   **静态表征的局限**：图像只能捕捉瞬间快照，无法表达连续的动态过程与因果变化。
*   **模态割裂**：文本与视觉通常作为分离的模态产生，通过交叉注意力等机制进行隐式交互，难以实现像素级的统一理解与生成。

### 2. 核心主张：用视频思考

本文提出了一种新的推理范式——“用视频思考（Thinking with Video）”。其核心思想是**利用视频生成模型（如 Sora-2）将视频帧作为推理链的统一媒介**。模型在连续的视频帧中动态绘制、操作视觉元素并直接嵌入文字，从而将逻辑推理与视觉想象融合在同一时间序列中，模拟类人的多模态思考过程。

### 3. 方法谱系与知识库定位

该方法在推理媒介和多模态融合方式上对现有范式做出了根本性改变：

*   **推理链媒体格式**：从纯文本步级（Chain-of-Thought 文本）或静态图像，转变为**连续的视频帧**，包含动态绘制、空间操作与嵌入文字。
*   **多模态融合方式**：从文本与视觉的分离产生与隐式交互，转变为**在同一视频帧内直接绘制文字与图形**，实现像素级融合。

在基线对比方面，本文主要将 Sora-2 与当前顶级的纯文本及多模态 VLM（如 **GPT-5 high**、**Gemini 2.5 Pro**、**Claude Sonnet 4.5**）进行对比，同时也纳入了其他视频生成模型（如 **Veo 3.1**、**Wan 2.5**）作为参照。

### 4. 实验全景与关键证据

为验证该范式，作者构建了 **VideoThinkBench** 基准，涵盖视觉中心和文本中心两大类任务。主要发现如下：

*   **视觉中心推理优势**：在眼球谜题（Eyeballing Puzzles）上，Sora-2 的平均准确率显著超越 GPT-5（领先约 10%），证明其通过绘制与想象进行空间推理的优势。
*   **文本中心推理能力**：在 MATH-500 基准上，Sora-2 的音频回答准确率达到 **92.0%**，在 GSM8K 上达 **98.9%**，接近或可比肩顶级 VLM。
*   **能力来源辨析**：消融实验揭示，Sora-2 的文本推理能力很大程度上源于其内部的 **Prompt Rewriter**。当在 Wan 2.5 上禁用该组件后，其推理能力几乎消失，表明是重写器而非视频生成模型自身解决了大部分推理问题。
*   **测试时扩展潜力**：Sora-2 具备少样本学习能力，且通过**自一致性（self-consistency）与多帧投票**，可在可验证任务（如 Arc Connect 谜题）上将准确率从 56% 大幅提升至 90%。

### 5. 局限与待验证问题

尽管结果令人瞩目，但该范式仍存在显著局限：

*   **黑箱问题**：所有评估均基于闭源模型 Sora-2，无法深入分析其内部机制，结论难以泛化。
*   **推理链不可读**：尽管音频答案准确率高，但生成的视频解题过程常常混乱、不完整或包含逻辑错误，可解释性差。
*   **抽象推理薄弱**：在 ARC-AGI-2 等抽象规则归纳任务上，绝对准确率仍然极低。
*   **待解问题**：视频生成模型能否在缺乏内部文本重写器的情况下独立发展出强大的推理能力？该范式的测试时缩放策略在其他任务上的泛化性如何？这些问题均有待开源模型的进一步验证。

### 多模态推理的现状与瓶颈

当前主流的多模态推理范式可概括为两类：“用文本思考（Thinking with Text）”和“用图像思考（Thinking with Images）”。前者以纯文本链式思维（Chain-of-Thought）为代表，虽在数学、编程等符号推理任务上表现卓越，却天然缺乏对动态视觉过程的建模能力；后者通过静态图像扩展了视觉推理的边界，但单帧画面只能捕捉瞬间状态，无法表达连续变化、空间操作与时间演化。这两种范式共享一个结构性缺陷：文本与视觉作为分离的模态，通过交叉注意力等机制进行隐式交互，难以实现像素级别的统一理解与生成。

这一瓶颈在需要动态空间推理的任务中尤为突出。例如，在“眼球谜题（Eyeballing Puzzles）”这类要求精确判断光线反射路径或几何对齐的任务中，顶级视觉语言模型 GPT-5 的平均准确率仅为 33.6%（点定位）、24.0%（线段）和 32.5%（形状），暴露出静态视觉理解在动态过程推理上的根本局限。

### 视频作为推理媒介的潜力

视频生成模型的快速发展为突破上述瓶颈提供了新的可能。这类模型天然具备两项关键能力：**动态渲染**——在连续帧中可视化过程演变；**空间操作**——在像素级别绘制图形、移动元素、标记关键点。更重要的是，视频帧本身可以同时承载文字与图形，实现文本逻辑与视觉想象的像素级融合。

本文由此提出 **“用视频思考（Thinking with Video）”** 范式：将视频生成模型作为推理链的媒介，通过在视频帧中逐步绘制、操作视觉元素并嵌入文字，将推理过程转化为一段连续的、可观察的视频序列。这一范式旨在弥合文本与视觉之间的模态鸿沟，使模型能够像人类一样，在统一的时空画布上“边想边画、边画边想”，完成从符号推理到动态空间想象的完整认知闭环。

## 核心方法与创新机理

本文提出 **“用视频思考”（Thinking with Video）** 范式，其核心创新在于将**推理链的媒介格式**从纯文本或静态图像替换为**连续的视频帧**，并在此过程中实现**像素级的多模态融合**。这一转变的两个关键 changed slots 如下：

### 推理链媒体格式：从静态到动态

传统 Chain‑of‑Thought 推理以纯文本步骤展开，而“用图像思考”范式仅能捕捉静态瞬间。本文的方法让视频生成模型在视频帧中**动态绘制、操作视觉元素**，从而表达连续变化与过程推理。例如，在眼球谜题（Eyeballing Puzzles）的光线反射问题中，Sora‑2 在视频中准确绘制光路并定位目标点（Figure 1）。这一能力源于视频生成模型天然具备的**时空渲染与空间操作能力**，使推理不再受限于离散的文本符号或单帧图像。

### 多模态融合方式：从隐式交互到像素级融合

现有 VLM 通常将文本与图像分开编码，通过交叉注意力等机制实现隐含的多模态交互。本文的方法则**在同一视频帧内直接绘制文字与图形**，实现文本逻辑与视觉想象的像素级融合（Figure 6）。这种融合方式使模型能够像人类一样“边画边写边思考”，将语言推理与视觉推理统一在同一时空序列中。

### 关键支撑证据

- **视觉中心推理优势**：在眼球谜题上，Sora‑2 的平均准确率显著超越 **GPT‑5**（Point 子任务领先约 10%），证明视频生成在需要空间想象与绘制的任务上具有独特优势（Table 1）。
- **文本中心推理能力**：Sora‑2 在 MATH‑500 上音频准确率达 92.0%，在 GSM8K 上达 98.9%，接近或可比肩顶级 VLM（Table 2）。
- **推理来源的揭示**：消融实验表明，Sora‑2 的文本推理能力**主要源于其内部的 Prompt Rewriter**，而非视频生成模型本身。当禁用重写器后，**Wan 2.5** 的推理能力几乎消失（Table 6；Figure 16）。这意味着当前“用视频思考”范式中，文本推理仍依赖隐式的文本重写，视频生成模型自身尚未独立发展出强大的推理能力。

### 需要警惕的局限

尽管范式创新显著，但分析发现 Sora‑2 生成的视频解题过程**常常混乱、不可读或包含逻辑错误**——仅有 13.91% 的解法完全正确，43.48% 不可读或存在逻辑错误（Figure 7）。这表明模型并未真正在视觉模态中“推理”，而是依赖隐藏的文本重写器输出答案，视频更多扮演“展示”而非“思考”的角色。这一发现对范式的完整性提出了重要挑战，需要后续研究进一步验证视频生成模型能否独立承担推理功能。

**Thinking with Video** 的整体 pipeline 围绕一个核心闭环展开：将任意推理问题转化为视频生成任务，再从生成的视频中提取答案。该流程由四个关键模块串联构成，输入为文本问题与可选的参考图像，输出为经自动评判的最终答案。

### 模块关系与数据流

1. **Prompt Rewriter（提示重写器）** — 作为 Sora‑2 的内部组件（论文未公开其具体实现），该模块接收原始问题文本，将其自动转化为包含详细逐步解决指令的描述性提示。消融实验（Table 6, Figure 16）表明，当禁用该重写器后，Wan 2.5 的推理准确率几乎降至零，而启用后则大幅回升，说明文本推理能力主要源于此模块，而非视频生成模型本身。

2. **Video Generation Model（视频生成模型，Sora‑2）** — 接收重写后的文本提示与参考图像（如有），生成一段包含完整解题过程的视频及同步音频。视频帧中可同时包含动态绘制、空间操作与嵌入的文字，实现像素级的多模态融合（Figure 6）。该模型是整个范式实现“用视频思考”的媒介载体。

3. **Answer Extraction（答案提取）** — 从生成视频中通过两条独立路径提取答案：
   - **视频路径**：提取视频的最后一帧，从中识别标记为红色的选项或最终结果。
   - **音频路径**：使用 Whisper 对视频音频进行转录，获取口述答案。
   两条路径的答案独立评估，以交叉验证一致性（Section 2.2.2）。

4. **LLM‑as‑a‑Judge（自动评判器）** — 采用 GPT‑4o 作为评判模型，将提取的答案与标准答案进行比对，判定正确与否。该方法的可靠性已通过人工对齐检查验证（Appendix C.6）。

### 输入输出规范

- **输入**：文本形式的问题陈述，以及一张可选的参考图像（包含问题全貌）。
- **输出**：一段视频，其帧中展示解题的绘制过程与文字推理步骤，音频中口述最终答案；系统最终输出经 LLM 评判的答案正确性判定。

### 评估路径的分叉

对于不同类型的任务，评估路径有所分化：
- **视觉中心任务**（如 Eyeballing Puzzles、ARC‑AGI‑2）：主要采用 **Major Frame 评估**——从视频所有帧中选取与真值偏差最小的帧进行人工评判，或对多帧选项进行多数投票。
- **文本中心任务**（如 GSM8K、MATH‑500）：同时采用 **音频转录评估** 和 **最后一帧评估**，两条路径独立进行，以相互校验。

这种“重写—生成—提取—评判”的闭环设计，使得视频生成模型无需显式输出文本推理链，即可在视觉与文本两类任务上展现推理能力，但其内部推理过程的透明性仍受限于闭源模型的黑箱特性。

![[assets/figures/papers/paper_list_l2346_https_arxiv_org_abs_2511_04570/figures/001_Figure_1.jpg]]
*Figure 1: Examples of vision-centric and text-centric tasks in VideoThinkBench, and Sora-2’s “Thinking with Video” solutions. Vision-centric tasks are solved by reasoning about visual elements via drawing and imagination, including eyeballing puzzles, visual puzzles, ARC-AGI-2 and mazes. An example is shown for each. Typically, in the “ray reflection” problem from eyeballing puzzles, Sora-2 accurately draws the light path and finds the specific point it passes through. Text-centric tasks are solved by text-based reasoning, which are adapted from established benchmarks. A GSM8K example shows the model provides a written process and the answer in the video*

![[assets/figures/papers/paper_list_l2346_https_arxiv_org_abs_2511_04570/figures/019_Figure_11.jpg]]
*Figure 11: Overview of 21 eyeballing puzzle types. Based on the task requirement (constructing a point, a line, or a shape), we divide the puzzle types into Point, Line, and Shape categories. For each puzzle type, an input image and corresponding ground truth image is shown. All prompts: Section C.4*

### 2.1 方法流水线

“用视频思考”（Thinking with Video）范式的推理流水线由四个关键模块串联构成：

1.  **Prompt Rewriter（提示重写器）**  
    推测为 Sora‑2 内部组件，负责将原始问题文本转化为详细的逐步解决描述。该模块是文本中心推理能力的核心来源——消融实验表明，禁用重写器后 Wan 2.5 的推理准确率几乎降至 0%（Table 6; Figure 16）。

![[assets/figures/papers/paper_list_l2346_https_arxiv_org_abs_2511_04570/figures/037_Figure_16.jpg]]
*Figure 16: Visual comparison of Wan 2.5’s outputs with and without prompt rewriting on the same GSM8K problem. The dramatic difference demonstrates that the reasoning capability resides in the prompt rewriter rather than the video generation model itself*

2.  **Video Generation Model（视频生成模型，Sora‑2）**  
    接收文本提示和参考图像，生成包含解题过程与答案的视频及音频。模型在视频帧中直接绘制图形、操作视觉元素并嵌入文字，实现像素级的多模态融合（Figure 6）。

3.  **Answer Extraction（答案提取）**  
    从生成视频中独立提取两类答案：
    -   **音频答案**：通过 Whisper 转录视频中的语音回答；
    -   **视觉答案**：提取最后一帧中标记为红色的选项或最终绘制结果（Section 2.2.2; Figure 6）。

4.  **LLM‑as‑a‑Judge（LLM 评判器）**  
    使用 GPT‑4o 自动评判提取的答案与标准答案是否一致，实现规模化自动评估（Section 2.2.2）。

### 2.2 关键公式

以下公式用于视觉中心任务（Eyeballing Puzzles 与 Visual Puzzles）的自动评估，定义在 Appendix C.5。

**逐像素偏差总和（Deviation Value）**

$$
Diff = \Sigma_{x,y \in \mathrm{Puzzle\ Area}} \delta(\mathrm{Pixel}_{\mathrm{gen}}(x,y), \mathrm{Pixel}_{\mathrm{gt}}(x,y))
$$

其中 $\mathrm{Pixel}_{\mathrm{gen}}$ 为生成帧像素，$\mathrm{Pixel}_{\mathrm{gt}}$ 为真值像素，$\delta$ 为像素差异函数。该指标在谜题区域内求和，用于量化生成结果与真值的整体偏离程度。

**颜色差异（Color Difference）**

$$
\delta_{\mathrm{color}}(p,q) = \sqrt{(p_r - q_r)^2 + (p_g - q_g)^2 + (p_b - q_b)^2}
$$

RGB 空间中的欧氏距离，用于颜色填充类任务的像素级评估。

**形状差异（Shape Difference）**

$$
\delta_{\mathrm{shape}}(p,q) = \begin{cases} 1, & \mathrm{if\ Binarize}(p) \neq \mathrm{Binarize}(q) \\ 0, & \mathrm{otherwise} \end{cases}
$$

其中 $\mathrm{Binarize}(\cdot)$ 为阈值 245 的二值化操作。该指标衡量二值化后的覆盖差异，用于形状绘制类任务的评估。

## 实验与关键发现

### 核心结果：视觉中心推理

Sora‑2 在视觉中心任务上展现出显著超越最强 VLM 的空间推理能力。在眼球谜题（Eyeballing Puzzles）上，Sora‑2 的平均准确率达到 44.7%（Point）、38.0%（Line）和 34.5%（Shape），而 GPT‑5 high 仅为 33.6%、24.0% 和 32.5%，领先幅度约 10 个百分点（Table 1）。这一优势源于视频生成模型能够通过动态绘制与视觉想象来推理空间关系，而非仅依赖静态图像理解。

![[assets/figures/papers/paper_list_l2346_https_arxiv_org_abs_2511_04570/figures/002_Table_1.jpg]]
*Table 1: Summary table of accuracy (%) across all second-level tasks on the full test set of VideoThinkBench. For Sora-2: Eyeballing Puzzles uses Major Frame evaluation (see Section 2.1.1), and text-centric tasks use audio evaluation results (see Section 2.2.2). Evaluation results of more models are shown in the Appendix (Tables 7 and 8)*

在视觉谜题（Visual Puzzles）上，Sora‑2 在对称性任务上与 Claude Sonnet 4.5 表现相当，但在梯度与组合性任务上仍存在差距。在 ARC‑AGI‑2 的严格像素匹配评估中，Sora‑2 的精确准确率仅为 1.3%，远低于 Claude Sonnet 4.5 的 5.3%（Table 11），表明其在抽象规则归纳与精确图形生成上仍面临根本性困难。

### 核心结果：文本中心推理

Sora‑2 在文本中心推理任务上展现出与 SOTA VLM 可比肩的性能。在 GSM8K 上音频准确率达 98.9%，在 MATH‑500 上达 92.0%，在 MathVista 上达 75.7%，甚至超越 GPT‑5 high 的 67.5%（Table 2）。然而，在更具挑战性的数据集上，Sora‑2 明显落后：AIME 上仅 46.7%，MMMU 上 69.2%，而 GPT‑5 high 分别为 99.0% 和 82.6%。

![[assets/figures/papers/paper_list_l2346_https_arxiv_org_abs_2511_04570/figures/008_Table_2.jpg]]
*Table 2: Accuracy (%) on subsets of text-only and multimodal reasoning benchmarks used for the text-centric tasks. The † symbol represents that the results are Avg@4. Sora-2 overall shows impressive reasoning capabilities, achieving performance comparable to SOTA VLMs on GSM8K, MATH-500, MathVista and MMBench in terms of audio accuracy, though noticeably lagging behind on more challenging datasets like AIME, GPQA, and MMMU*

值得注意的是，Sora‑2 的视频评估（最后一帧）准确率系统性低于音频评估。例如，在 MATH‑500 上，最后一帧准确率仅为 84.6%，而音频准确率为 92.0%（Table 2）。这一差异暗示模型在视频帧中生成的文字答案可能不如音频中表达的答案可靠，视频中的视觉推理过程与最终答案之间存在不一致。

### 少样本学习能力

Sora‑2 展现出明确的少样本学习能力。在 ARC‑AGI‑2 上，提供更多示例（few‑shot）相比单示例（1‑shot）显著提升了高准确率样本的数量：像素准确率在 [0.65, 1.0] 区间的样本数从 95 增至 130，而在 [0, 0.35] 低准确率区间的样本数从 170 降至 145（Table 3）。这表明视频生成模型能够从上下文中提取并应用抽象变换规则，具备一定的归纳推理潜力。

### 测试时缩放：自一致性与多帧投票

在可验证的视频生成推理任务上，自一致性（self‑consistency）与测试时缩放策略展现出显著效果。以 Arc Connect 谜题为例：
- 单次生成的最后一帧准确率仅为 56%；
- 采用多帧投票（Major Frame）方法，从视频中采样多帧并取多数选项，准确率提升至 68%；
- 进一步进行 5 次独立生成并投票（Vote Accuracy），准确率跃升至 90%（Table 4）。

这一结果表明，视频生成模型在推理过程中存在帧间不一致性，但通过聚合多个推理路径的共识，可以大幅提高最终答案的可靠性。Major Frame 方法本质上起到了去噪滤波器的作用，捕捉模型最一致的信念状态。

### 推理过程质量分析

尽管 Sora‑2 在多个基准上取得了令人瞩目的准确率，但其生成的视频解题过程质量堪忧。对文本中心任务中正确回答样本的解题过程进行分类发现（Figure 7）：
- 仅 **13.91%** 的解法完全正确且可读；
- **43.48%** 的解法不可读或包含逻辑错误；
- 其余样本的解题过程部分正确但不完整。

这一发现揭示了一个关键瓶颈：Sora‑2 能够输出正确答案，但其在视频帧中生成的推理链往往混乱、不连贯或存在明显错误。这意味着模型并非真正在视觉模态中进行逐步推理，而是可能依赖其他隐藏机制（如内部 Prompt Rewriter）来获得答案。

### 关键消融：Prompt Rewriter 的决定性作用

对文本中心推理能力来源的消融实验揭示了核心机制。使用 Wan 2.5 进行对比实验（Table 6）：
- **启用 Prompt Rewriter** 时，Wan 2.5 在 GSM8K 上准确率达 78.4%，在 MMLU 上达 74.1%；
- **禁用 Prompt Rewriter** 时，准确率几乎归零：GSM8K 降至 0.0%，MMLU 降至 0.0%，MMMU 仅 2.0%。

![[assets/figures/papers/paper_list_l2346_https_arxiv_org_abs_2511_04570/figures/013_Table_6.jpg]]
*Table 6: Wan 2.5’s performance on text-centric tasks with and without prompt rewriting. Its reasoning ability almost vanishes when the prompt rewriter model is disabled, indicating that the rewriter solves the reasoning problems for the video generation component*

这一对比（Figure 16 直观展示了有无重写器时生成视频的差异）强有力地证明：**Sora‑2 的文本中心推理能力主要源于其内部的 Prompt Rewriter 组件，而非视频生成模型本身**。重写器将原始问题转化为详细的逐步解决描述，视频生成模型仅负责执行这些指令并渲染视觉输出。这解释了为何视频中的解题过程常常不可读——模型并未在视频帧中“思考”，而是将思考外包给了隐藏的文本重写器。

### 数据泄露排除

为排除测试集泄露的可能性，研究者对数学推理问题进行了数值改写（GSM8K‑Derived 和 MATH‑500‑Derived）。Sora‑2 在改写后问题上的表现与原题一致（Table 5），表明其推理能力并非来自记忆训练数据中的具体题目，而是具备一定的泛化能力。然而，结合 Prompt Rewriter 的消融结果，这种泛化能力更可能归属于重写器而非视频生成模型本身。

### 失败模式与局限性

1. **视觉推理的精确性不足**：在 ARC‑AGI‑2 等需要精确像素级输出的任务上，Sora‑2 常常无法正确修改输出网格，生成的图形与真值存在显著偏差。
2. **推理过程不可解释**：视频中的解题过程多数不可读或包含错误，限制了模型的可解释性与可信度。
3. **闭源黑箱限制**：所有分析基于闭源模型 Sora‑2，无法深入探究 Prompt Rewriter 的具体实现机制，也无法确定结论是否适用于其他视频生成模型。
4. **任务覆盖有限**：基准构建依赖自动化程序，尚未覆盖主观推理或开放性推理场景。

## 定位与知识库关联

### 1. 范式定位：从“文本思维”到“视频思维”

当前主流的多模态推理范式可划分为两条路线：

- **用文本思考（Thinking with Text）**：以 Chain‑of‑Thought 为代表，推理链完全由纯文本步级构成。代表性模型包括 **GPT‑5**、**Gemini 2.5 Pro**、**Claude Sonnet 4.5** 等 VLM。这类方法在数学推理（GSM8K、MATH‑500）上表现强劲，但面对需要动态空间想象的任务（如眼球谜题中的光线反射路径绘制）时，文本描述天然存在信息带宽瓶颈——图像仅能捕捉静态瞬间，无法表达连续变化过程。
- **用图像思考（Thinking with Images）**：部分工作尝试将视觉生成引入推理循环，但文本与视觉仍作为分离模态产生，通过交叉注意力等机制进行隐式交互，未能实现像素级的统一融合。

本文提出的 **Thinking with Video** 范式在推理链媒体格式和多模态融合方式两个关键维度上做出了根本性改变：

| 设计维度 | 基线范式 | Thinking with Video |
|----------|----------|---------------------|
| 推理链媒体格式 | 纯文本步级或静态图像 | 连续视频帧，包含动态绘制、空间操作与嵌入文字 |
| 多模态融合方式 | 文本与视觉分离产生，隐含交互 | 同一视频帧内直接绘制文字与图形，像素级融合 |

这一范式转变的核心洞察在于：视频生成模型天然具备动态渲染与空间操作能力，能够将文本逻辑与视觉想象融合在同一时间序列中，构成一种统一的类人多模态推理模式。

### 2. 与现有视频生成模型的比较

本文的实证分析主要围绕闭源模型 **Sora‑2** 展开，同时引入 **Wan 2.5** 作为对比对象进行消融研究。关键发现是：Sora‑2 在文本中心推理任务上的强大表现，主要源于其内部的 **Prompt Rewriter** 组件，而非视频生成模型本身的推理能力。当禁用重写器后，Wan 2.5 的推理准确率几乎归零（GSM8K 从 78.4% 降至 0.0%，MMLU 从 74.1% 降至 0.0%），这揭示了当前视频生成模型在独立文本推理上的根本性局限。

在视觉中心任务上，Sora‑2 与 **Veo 3.1** 等视频生成模型形成直接对比。眼球谜题（Eyeballing Puzzles）的评估显示，Sora‑2 通过 Major Frame 评估方法达到 40.2% 的平均准确率，在 Point 子任务上领先 GPT‑5 约 10 个百分点，证明了视频生成在空间推理上的独特优势。

### 3. 适用边界与关键局限

**适用场景**：
- 需要动态空间想象与视觉操作的任务（眼球谜题、视觉谜题中的对称性与渐变推理）
- 可通过自一致性（self‑consistency）与多帧投票进行测试时缩放的可验证推理任务
- 少样本学习场景：提供更多示例可显著提升 ARC‑AGI‑2 上的像素准确率

**关键局限**：

1. **推理过程不可解释**：尽管 Sora‑2 的音频答案准确率在 GSM8K 上达 98.9%、MATH‑500 上达 92.0%，但对其解题过程的分类分析显示，仅有 13.91% 的解法完全正确，43.48% 不可读或存在逻辑错误。这意味着模型并未真正在视觉模态中“推理”，视频更多是结果的展示媒介而非推理载体。

2. **严格图形匹配能力薄弱**：在 ARC‑AGI‑2 上，Sora‑2 的精确像素匹配准确率仅为 1.3%，远落后于 Claude Sonnet 4.5 的 5.3%，且常无法修改输出网格。这表明模型在抽象规则归纳与精确图形生成之间存在显著鸿沟。

3. **闭源黑箱限制**：所有评估均基于闭源模型 Sora‑2，无法访问其内部机制。Prompt Rewriter 的具体实现方式（是否依赖外部 LLM）仍不明确，结论不能直接推广到其他视频生成模型。

4. **评估覆盖面有限**：基准构建依赖自动化程序与适配，某些主观或开放性推理任务尚未覆盖。答案提取依赖 Whisper 转录与最后一帧分析，可能引入额外的评估噪声。

### 4. 开放问题

1. **Prompt Rewriter 的内部机制**：Sora‑2 内部的 Prompt Rewriter 如何将原始问题转换为详细的逐步解决方案？是否依赖外部 LLM 进行推理重写？这一组件是“用视频思考”范式的核心瓶颈。

2. **视频生成模型的独立推理能力**：在缺乏内部文本重写器的情况下，视频生成模型能否通过大规模训练或架构改进，独立发展出强大的文本推理能力？这是该范式能否成立的根本问题。

3. **测试时缩放的泛化性**：多帧投票与多次生成在 Arc Connect 谜题上展示了显著的性能提升（从 56% 到 90%），但这种方法在其他视频生成推理任务上的泛化性和计算开销尚未系统评估。

4. **开源模型的可行性**：开源视频生成模型（如 Hunyuan‑Video、Wan 系列）能否通过类似的提示重写与微调策略达到 Sora‑2 级别的多模态推理能力？这决定了该范式的生态可复制性。

5. **可信评估的设计**：如何设计更严格的评估协议，使生成的视频解题过程既正确又具备可读性，而不仅仅依赖音频或最后一帧的结果？这需要同时推进生成质量与评估方法的改进。

## 原文 PDF

![[paperPDFs/CVPR_2026/Thinking_with_Video_Video_Generation_as_a_Promising_Multimodal_Reasoning_Paradigm.pdf]]
