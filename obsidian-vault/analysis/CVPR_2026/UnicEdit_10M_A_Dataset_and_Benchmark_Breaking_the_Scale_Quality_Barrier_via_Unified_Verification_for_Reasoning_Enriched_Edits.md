---
title: "UnicEdit-10M: A Dataset and Benchmark Breaking the Scale-Quality Barrier via Unified Verification for Reasoning-Enriched Edits"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UnicEdit_10M_A_Dataset_and_Benchmark_Breaking_the_Scale_Quality_Barrier_via_Unified_Verification_for_Reasoning_Enriched_Edits.pdf
project_link: null
code_link: null
aliases:
- UDCPQV
- UnicEdit-10M
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 统一后验证与双任务专家模型 Qwen-Verify 的结合：通过一个 7B 模型高效地同时完成失败检测与指令重描述，无需昂贵的 API 调用，即可在高吞吐量下保证语义对齐和视觉质量，从而突破规模-质量壁垒。
primary_logic: 将原本依赖大型模型的后验证任务蒸馏为小型化、语义感知的专家模型，通过动态视觉差异上下文（c_v）和 D²PO 偏好优化，使模型能精准捕捉细微的编辑差异并生成精确匹配的指令，实现可扩展的高质量数据制造。
claims:
- UnicEdit-10M 在 VIEScore Overall 和 Aesthetic 上均取最优，且人脸一致性（0.89）远优于 GPT-Image-Edit-1.5M（0.30），直接验证了统一后验证对数据保真度的显著提升。
- Qwen-Verify 在所有验证类别（Normal, No Edit, Hallucination）的准确性均超越 Qwen2.5-VL-72B，同时计算成本大幅降低，证明小模型在专用验证任务上可以超越通用大模型。
- UnicBench 评估揭示：几乎所有模型在 RA（推理准确性）上的表现远低于其他指标，说明复杂推理编辑是当前模型的共同短板，突显了针对性数据和基准的必要性。
- 细粒度指标 NC（非编辑一致性）能够发现 VIEScore 忽略的非目标区域意外变化（如误删人物、文字篡改），提供更具诊断性的评估（Fig. 8）。
---

# UnicEdit-10M: A Dataset and Benchmark Breaking the Scale-Quality Barrier via Unified Verification for Reasoning-Enriched Edits

> [!tip] 核心洞察
> 将原本依赖大型模型的后验证任务蒸馏为小型化、语义感知的专家模型，通过动态视觉差异上下文（c_v）和 D²PO 偏好优化，使模型能精准捕捉细微的编辑差异并生成精确匹配的指令，实现可扩展的高质量数据制造。

| 字段 | 内容 |
|------|------|
| 中文题名 | UnicEdit-10M：通过统一验证打破规模-质量壁垒的推理丰富编辑数据集与基准 |
| 英文题名 | UnicEdit-10M: A Dataset and Benchmark Breaking the Scale-Quality Barrier via Unified Verification for Reasoning-Enriched Edits |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.02790) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | UnicEdit Data Curation Pipeline with Qwen-Verify |
| Dataset | UnicEdit-10M Dataset Quality, UnicBench, Post-Verification Accuracy |

> [!tip] 效果简介
> - UnicEdit-10M Dataset Quality (vs GPT-Image-Edit-1.5M) 上，VIEScore Overall 8.0768 vs 7.7451 (+0.3317)。
> - UnicBench (Closed-source Best vs Second) 上，Overall-EN Score GPT-Image-1: 8.3546 vs Seedream 4.0: 8.0428 (+0.3118)。
> - UnicBench (Open-source Top vs Weakest) 上，Overall-EN Score Qwen-Image-Edit: 7.7273 vs InstructPix2Pix: 2.9221 (显著提升)。

## 概要

图像编辑数据集长期面临规模与质量不可兼得的困境。人工标注虽能保证高质量，但成本高昂、难以扩展；自动化流水线虽可大规模生产数据，却充满噪声——多工具链的错误累积、后验证的缺失或不完整，导致大量编辑失败样本混入训练集。与此同时，现有基准对复杂推理编辑（如视角变换、文本修改、知识推理）缺乏细粒度诊断，掩盖了模型在这些关键维度上的系统性短板。

针对上述瓶颈，本文提出**UnicEdit-10M**——一个覆盖22个子任务、规模达千万级的高质量图像编辑数据集，以及配套的细粒度评估基准**UnicBench**。其核心突破在于**统一后验证机制**与**双任务专家模型Qwen-Verify**的协同设计：通过训练一个7B参数的小型专家模型，同时完成失败检测与指令重描述两项任务，在无需昂贵API调用的前提下，实现高吞吐量下的语义对齐与视觉质量双重保障。

方法层面的关键创新是将原本依赖大规模通用模型的后验证任务蒸馏为语义感知的专用模型。具体而言，Qwen-Verify基于Qwen2.5-VL-7B进行两阶段训练——先通过监督微调建立基础验证能力，再通过**差分直接偏好优化**引入视觉差异上下文，使模型能精准捕捉编辑前后的细微变化并生成精确匹配的指令，从而突破规模-质量壁垒。

实验验证了该方案的多方面有效性：

- **数据集质量**：UnicEdit-10M在VIEScore Overall（8.0768）和Aesthetic上均取得最优，人脸一致性（0.89）远优于GPT-Image-Edit-1.5M（0.30），直接验证了统一后验证对数据保真度的显著提升（Table 2）。
- **验证模型效率**：Qwen-Verify在所有验证类别上的准确性全面超越Qwen2.5-VL-72B，同时计算成本大幅降低，证明专用小模型可在特定验证任务上超越通用大模型（Table 5）。
- **基准诊断力**：UnicBench揭示几乎所有模型在推理准确性指标上的表现远低于其他维度，说明复杂推理编辑是当前模型的共同短板；其细粒度指标非编辑一致性能够发现VIEScore忽略的非目标区域意外变化，提供更具诊断性的评估（Table 4, Fig. 8）。

在方法谱系中，UnicEdit区别于**InstructPix2Pix**等缺乏质量验证的合成数据流水线，也超越了**SEED-Data-Edit**、**UltraEdit**、**ImgEdit**等依赖多工具链且后验证不完整的方案，以及**GPT-Image-Edit-1.5M**仅做指令重描述而缺失失败检测的策略。其统一后验证框架为图像编辑数据生产提供了一种可扩展的高质量范式。

当前工作的主要局限包括：数据集质量受限于所使用的编辑模型能力，复杂编辑任务的样本比例和模型表现仍有提升空间，验证模型的跨任务泛化性未经检验，以及基准规模有限可能无法完全代表真实世界编辑指令的多样性。



图像编辑作为视觉内容创作的核心任务，正经历从传统工具向基于扩散模型的指令驱动编辑范式的深刻转变。用户通过自然语言指令即可实现对图像中物体、场景乃至复杂语义关系的修改，这极大地降低了创作门槛。然而，这一范式的高效落地依赖于大规模、高质量的对齐数据，即“源图像-编辑指令-目标图像”三元组。

当前图像编辑数据集面临**规模与质量的双重困境**。一方面，人工标注虽能保证高质量的对齐，但成本高昂且难以扩展，无法满足数据驱动模型日益增长的规模需求。另一方面，现有的自动化数据流水线（如 **InstructPix2Pix**、**SEED-Data-Edit**、**UltraEdit**、**ImgEdit**、**NHR-Edit**）虽能实现大规模数据生成，却普遍存在以下结构性缺陷：

- **错误传播与噪声累积**：多工具链分段调用的架构使得上游模块的误差在下游被逐级放大，最终生成的三元组中充斥着语义不对齐、视觉伪影等问题。例如，**ImgEdit** 和 **SEED-Data-Edit** 的自动化流水线已被证实容易产生错误传播，导致编辑图像与指令之间存在显著的语义偏差。
- **后验证不全面**：现有方法的后验证机制要么完全缺失，要么仅覆盖单一维度。**NHR-Edit** 仅进行失败检测而不涉及指令优化；**GPT-Image-Edit-1.5M** 虽使用 GPT-4o 进行指令重描述，却缺少失败检测环节，且其人脸一致性得分仅 0.30，远低于 UnicEdit-10M 的 0.89，暴露出昂贵 API 调用在细粒度语义保真度上的不足。
- **推理编辑能力缺失**：现有基准缺少对复杂推理和空间编辑的细粒度诊断。UnicBench 的评估结果揭示了一个关键瓶颈：几乎所有模型在推理准确性（RA）上的表现远低于指令遵循（IF）和视觉质量（VQ）等传统指标，说明复杂推理编辑是当前模型的共同短板。

上述困境的根本原因在于**缺乏一个统一、高效且语义感知的后验证机制**。传统像素级度量（如 SSIM）无法区分“微小有效编辑”与“完全无编辑”之间的语义差异——它会对包含细微编辑的图像给出高相似度分数，而对无编辑样本反而降低分数，这恰恰与编辑验证的需求背道而驰。同时，依赖 GPT-4o 等大规模 API 的方案虽具备语义理解能力，却面临推理成本高、吞吐量受限、且无法针对编辑任务进行专门优化的难题。

基于此，本文的核心动机是：**能否将原本依赖大型模型的后验证任务蒸馏为一个紧凑的专家模型，通过统一失败检测与指令重描述的双任务设计，在可控的计算成本下实现可扩展的高质量数据制造？** 这一思路直接推动了 UnicEdit-10M 数据集和 Qwen-Verify 专家模型的诞生，旨在打破图像编辑数据领域长期存在的规模-质量壁垒。



## 核心方法与创新机理

UnicEdit 的核心创新在于将**统一后验证**与**小型化专家模型**深度耦合，打破了图像编辑数据集长期面临的“规模-质量”双重困境。其关键突破体现在以下三个相互关联的维度。

### 1. 统一后验证：从单维过滤到双任务联合优化

现有数据流水线在质量控制上存在结构性缺陷：**InstructPix2Pix** 完全依赖合成数据而无验证，**ImgEdit** 等多工具链流水线缺乏后验证导致错误累积，**NHR-Edit** 仅做失败检测而不涉及指令优化，**GPT-Image-Edit-1.5M** 虽进行指令重描述却缺失失败检测且依赖昂贵的 GPT-4o API。这些方案将失败检测与指令优化割裂为独立甚至缺失的环节，无法形成闭环的质量保障。

UnicEdit 提出**集失败检测与指令重描述于一体的统一后验证框架**，以思维链推理驱动，在单次推理中同时完成两项任务：首先判断编辑是否成功（区分正常编辑、无编辑、幻觉编辑三类），然后对有效编辑重新生成精确匹配视觉变化的指令。这一设计使质量控制的覆盖度和一致性发生质变——流水线过滤了约 26% 的失败编辑（Tab. 3），最终保留约 11.6M 高质量三元组，在 VIEScore Overall（8.0768 vs. 7.7451）和人脸一致性（0.89 vs. 0.30）上显著超越 **GPT-Image-Edit-1.5M**（Tab. 2, Tab. 8）。

### 2. Qwen-Verify 专家模型：小模型超越大模型的专用验证

后验证的传统思路是调用 GPT-4o 等大规模 API，成本高昂且吞吐量受限。UnicEdit 的关键洞察在于：**将验证能力从通用大模型蒸馏为语义感知的专用小模型**，通过针对性训练实现“小而精”。

Qwen-Verify 基于 Qwen2.5-VL-7B 进行两阶段训练：首先通过监督微调（SFT）建立基础验证能力，随后引入**差分直接偏好优化（D²PO）**进行偏好对齐。D²PO 的核心机制是引入视觉差分上下文 $c_v = \mathcal{V}(I_o, I_e)$——从原始图像与编辑图像中提取的编辑动态潜在表示，使模型能精准捕捉细微的视觉变化。训练目标基于 Bradley-Terry 偏好模型，通过最大化偏好指令与拒绝指令之间的优势边界来对齐人类判断：

$$\mathcal{L}_{\mathrm{D}^2\mathrm{PO}} = -\mathbb{E}_{(c_v, p_w, p_l) \sim \mathcal{D}} [\log \sigma (\mathcal{A}_{\pi_\theta, \pi_{\mathrm{ref}}}(p_w, c_v) - \mathcal{A}_{\pi_\theta, \pi_{\mathrm{ref}}}(p_l, c_v))]$$

其中优势函数 $\mathcal{A}_{\pi_\theta, \pi_{\mathrm{ref}}}(p, c_v) = \beta \log \frac{\pi_\theta(p|c_v)}{\pi_{\mathrm{ref}}(p|c_v)}$ 衡量可训练策略相对于冻结参考策略在给定视觉上下文下生成指令的质量。

实验结果直接验证了这一策略的有效性：Qwen-Verify 在所有验证类别上全面超越 **Qwen2.5-VL-72B**——Normal 准确性 6.32 vs. 5.25，No Edit 准确性 9.80 vs. 9.60，Hallucination 准确性 6.22 vs. 6.12（Tab. 5）。值得注意的是，D²PO 阶段对幻觉抑制尤为关键，将 Hallucination 准确性从仅 SFT 的 5.47 提升至 6.22。同时，语义敏感的专家模型在“无编辑”检测上显著优于传统像素级 SSIM——SSIM 对微小有效编辑给出高相似度，却对无编辑样本降低分数（Fig. 6），证明了深度学习验证的必要性。

### 3. 端到端编辑执行：消除多工具链的错误累积

与 **SEED-Data-Edit**、**UltraEdit** 等依赖多工具链分段调用的方案不同，UnicEdit 采用端到端编辑模型（FLUX.1-Kontext、Qwen-Image-Edit）直接生成编辑图像，从根本上消除了工具链间的错误传播。这一设计简化了流水线结构，使后验证能够作用于完整的编辑结果而非中间产物，进一步保障了数据质量。

三个创新点形成协同效应：端到端编辑提供干净的数据基础，统一后验证实现全面的质量把控，小型专家模型则使这一流程在低成本下可规模化运行——这正是 UnicEdit 突破“规模-质量”壁垒的因果机制。



UnicEdit-10M 的数据构建采用**三阶段流水线**架构，将图像编辑数据的生产从传统的多工具链分段调用转变为一个端到端、质量可控的系统。该流水线的核心设计理念是通过**统一后验证**机制，在保证高吞吐量的同时突破规模与质量的双重困境。

### 三阶段流水线设计

整个数据构建流程由三个顺序衔接的阶段组成：

**阶段一：指令生成 (Instruction Generation)**。以内部高美学得分图像库作为源图像池，利用 Qwen2.5-VL-72B 作为图像感知的指令生成器。系统根据预定义的编辑分类法（覆盖 22 个子任务，横跨基础编辑与复杂推理编辑），对每张源图像自动生成 3–7 条多样化的编辑指令。这种基于分类法的生成策略确保了指令在任务类型、难度和语义上的广泛覆盖。

**阶段二：图像编辑 (Image Editing)**。摒弃了传统流水线中多工具链分段调用（如先分割再修复）的范式，转而采用端到端编辑模型直接根据指令-图像对生成编辑结果。具体使用的编辑模型包括 FLUX.1-Kontext 和 Qwen-Image-Edit。端到端设计避免了多工具链中错误累积传播的问题，同时简化了流程复杂度。

**阶段三：后验证与优化 (Post-Verification & Refinement)**。这是整个流水线的关键创新所在。该阶段由双任务专家模型 **Qwen-Verify**（基于 Qwen2.5-VL-7B 训练）统一执行两项任务：
- **失败检测**：识别并过滤无编辑变化（No Edit）或编辑错误（Hallucination）的样本；
- **指令重描述**：对有效编辑样本，根据实际编辑结果重新生成精确匹配的指令，修正原始指令与编辑结果之间的语义偏差。

两项任务通过思维链推理统一驱动，无需分别调用不同的验证模块或昂贵的 API。根据 Table 3 的统计，后验证阶段过滤了约 26% 的失败编辑，最终从初始的约 15.7M 候选样本中保留了约 11.6M 个高质量三元组（源图像、精炼指令、编辑图像）。

### 输入输出流

流水线的数据流清晰且线性：
1. **输入**：源图像 $I_o$ + 基于分类法生成的初始编辑指令 $p_{init}$
2. **编辑执行**：端到端模型生成编辑图像 $I_e$
3. **后验证**：Qwen-Verify 对 $(I_o, I_e, p_{init})$ 三元组进行判断
   - 若检测为失败编辑，直接丢弃
   - 若检测为有效编辑，输出精炼指令 $p_{refined}$，形成最终三元组 $(I_o, p_{refined}, I_e)$

### 与现有流水线的关键差异

相较于现有数据构建方法，UnicEdit 流水线在三个关键维度上实现了改进：

| 维度 | 现有方法 | UnicEdit 方法 |
|------|---------|--------------|
| **编辑执行** | 多工具链分段调用（如 InstructPix2Pix 的合成数据流水线、SEED-Data-Edit 的多工具组合），错误易累积 | 端到端编辑模型直接生成，流程简洁且避免错误传播 |
| **后验证** | 无统一验证（如 UltraEdit 仅有部分后过滤），或仅含失败检测（如 NHR-Edit），或仅做指令优化（如 GPT-Image-Edit-1.5M 使用 GPT-4o API 重描述但无失败检测） | 失败检测与指令重描述双任务统一，由紧凑的 7B 专家模型执行 |
| **质量控制成本** | 依赖昂贵的大规模 API 调用（如 GPT-4o）或像素级度量（如 SSIM），前者成本高，后者语义感知弱 | Qwen-Verify 7B 专家模型，通过 SFT 和 D²PO 偏好优化实现语义感知验证，计算成本大幅降低 |

这种设计使得 UnicEdit-10M 在 VIEScore Overall（8.0768）和 Aesthetic 分数上均优于使用 GPT-4o API 的 GPT-Image-Edit-1.5M（7.7451），同时人脸一致性达到 0.89，远超后者的 0.30，直接验证了统一后验证对数据保真度的显著提升。

### 补充图表

![[assets/figures/papers/paper_list_l798_https_arxiv_org_abs_2512_02790/figures/001_Figure_1.jpg]]
*Figure 1: UnicEdit-10M covers 22 edit tasks spanning basic and complex edits, with a unified post-verification stage that filters failures and refines instructions to yield high-quality triplets. We also introduce UnicBench with fine-grained metrics for comprehensive evaluation*

![[assets/figures/papers/paper_list_l798_https_arxiv_org_abs_2512_02790/figures/004_Figure_3.jpg]]
*Figure 3: Data curation pipeline with three stages: (1) data preparation, (2) image editing, (3) post verification performing failed edits filtration and recaption*



### 统一后验证框架

UnicEdit 的核心创新在于将原本分离且昂贵的后验证操作统一为一个紧凑的双任务专家模型。传统流水线（如 **ImgEdit**、**UltraEdit**）要么仅进行失败检测，要么依赖 GPT-4o 等大规模 API 进行指令重描述，两者割裂且计算成本高昂。Qwen-Verify 以 Qwen2.5-VL-7B 为基座，通过两阶段训练同时完成**失败检测**与**指令重描述**两项任务，在单一前向传播中输出失败判定或精确对齐编辑结果的优化指令。

该双任务设计的因果机制在于：失败检测迫使模型理解编辑是否真正发生以及是否产生幻觉；指令重描述则要求模型精准捕捉编辑前后的语义差异。两者共享视觉编码器提取的编辑动态特征，形成了相互增强的优化信号。

### D²PO：差异感知的直接偏好优化

#### 动机与问题

监督微调（SFT）阶段赋予模型基础的验证与重描述能力，但模型在幻觉检测和细微编辑差异的指令匹配上仍存在偏差。传统像素级度量（如 SSIM）无法区分“无编辑”与“微小有效编辑”（见 Fig. 6），而通用大模型（如 Qwen2.5-VL-72B）在专用验证任务上准确率有限。为此，论文提出 **D²PO（Differential Direct Preference Optimization）**，将偏好优化适配到视觉差异理解这一特殊挑战。

![[assets/figures/papers/paper_list_l798_https_arxiv_org_abs_2512_02790/figures/012_Figure_6.jpg]]
*Figure 6: Examples of No Edit filtration. The left side shows four examples with detection results from SSIM [39] and Qwen-Verify. The top-left example has a clear edit (red dashed box) but receives a high SSIM [39] score, while the other three visually unchanged pairs receive lower scores. The right side provides a quantitative comparison, confirming that Qwen-Verify performs best at identifying failed edits*

#### 核心公式

**视觉差异上下文**。视觉编码器 $\mathcal{V}$ 从原始图像 $I_o$ 和编辑图像 $I_e$ 中提取编辑动态的潜在表示，作为后续偏好优化的条件输入：

$$c _ { v } = \mathcal { V } ( I _ { o } , I _ { e } )$$

$c_v$ 编码了编辑前后的语义与视觉变化，是 D²PO 区别于标准 DPO 的关键——标准 DPO 仅依赖文本上下文，而 D²PO 将图像对的差异信息显式注入优化过程。

**策略优势函数**。给定视觉差异上下文 $c_v$，可训练策略 $\pi_\theta$ 相对于冻结参考策略 $\pi_{\mathrm{ref}}$ 在生成指令 $p$ 上的对数概率比，由温度系数 $\beta$ 缩放：

$$\mathcal { A } _ { \pi _ { \theta } , \pi _ { \mathrm { r e f } } } ( p , c _ { v } ) = \beta \log \frac { \pi _ { \theta } ( p | c _ { v } ) } { \pi _ { \mathrm { r e f } } ( p | c _ { v } ) }$$

该函数衡量模型对特定指令的偏好强度：$\mathcal{A} > 0$ 表示当前策略比参考策略更倾向于生成该指令。

**D²PO 损失函数**。基于 Bradley-Terry 偏好模型，通过最大化偏好指令 $p_w$ 与拒绝指令 $p_l$ 之间的优势边界来对齐模型与人类判断：

$$\mathcal { L } _ { \mathrm { D } ^ { 2 } \mathrm { P O } } = - \mathbb { E } _ { ( c _ { v } , p _ { w } , p _ { l } ) \sim \mathcal { D } } [ \log \sigma \left( \mathcal { A } _ { \pi _ { \theta } , \pi _ { \mathrm { r e f } } } ( p _ { w } , c _ { v } ) - \mathcal { A } _ { \pi _ { \theta } , \pi _ { \mathrm { r e f } } } ( p _ { l } , c _ { v } ) \right) ]$$

其中 $\sigma$ 为 sigmoid 函数，$\mathcal{D}$ 为偏好数据集。该损失驱动模型在给定视觉差异上下文 $c_v$ 时，显著提升偏好指令 $p_w$ 的相对概率，同时抑制拒绝指令 $p_l$。

#### 消融验证

D²PO 阶段对指令质量的提升具有决定性作用。Tab. 5 显示，仅经过 SFT 的模型在 Hallucination 类别上的对齐准确率为 5.47，而加入 D²PO 后提升至 6.22，表明偏好对齐能有效减少幻觉指令的生成。同时，Qwen-Verify 在所有验证类别（Normal: 6.32, No Edit: 9.80, Hallucination: 6.22）上全面超越 Qwen2.5-VL-72B（5.25 / 9.60 / 6.12），证明了小模型在专用验证任务上通过 D²PO 可以超越通用大模型。

### 编辑评分聚合

UnicBench 采用几何平均聚合多维度指标，确保任一维度的严重失败都会显著拉低总分：

$$\mathrm { S c o r e } = \left( \prod _ { m \in \mathcal { M } } m \right) ^ { 1 / | \mathcal { M } | }$$

其中 $\mathcal{M}$ 为适用指标集合：基本编辑任务取 $\{IF, NC, VQ\}$，复杂编辑任务额外加入推理准确性 $RA$，即 $\{IF, NC, VQ, RA\}$。该设计避免了算术平均对低分维度的掩盖效应，使评估更具诊断性。

### 补充图表

![[assets/figures/papers/paper_list_l798_https_arxiv_org_abs_2512_02790/figures/005_Figure_4.jpg]]
*Figure 4: Post-verification examples of the expert model. Base denotes Qwen2.5-VL-7B; SFT denotes Base model after Stage-1 SFT; Ours denotes the dual-task expert model Qwen-Verify*



## 实验与关键发现

### 数据集质量对比：统一后验证的规模-质量突破

UnicEdit-10M 在数据质量上显著优于现有开源和闭源数据集。如 Table 2 所示，在 VIEScore 综合指标上，UnicEdit-10M 取得 **8.0768** 分，优于 GPT-Image-Edit-1.5M 的 7.7451 分（+0.3317），且美学得分（Aesthetics Source 8.00）同样领先。更具诊断性的是人脸一致性指标：UnicEdit-10M 达到 **0.89**，而依赖昂贵 GPT-4o API 进行指令重描述但缺少失败检测的 GPT-Image-Edit-1.5M 仅为 0.30（Table 8）。这一巨大差距直接验证了统一后验证对数据保真度的关键作用——仅重描述指令而不过滤失败编辑，会导致大量身份不一致的样本污染数据集。

![[assets/figures/papers/paper_list_l798_https_arxiv_org_abs_2512_02790/figures/006_Table_2.jpg]]
*Table 2: Overall dataset quality comparison between UnicEdit-10M and other datasets. VIEScore reports Semantic Consistency (SC) and Perceptual Quality (PQ) with their Overall score. Aesthetics columns give the aesthetic scores for the Source (original) and Target (edited) images. Best results are in bold, and second best are underlined*

![[assets/figures/papers/paper_list_l798_https_arxiv_org_abs_2512_02790/figures/017_Table_8.jpg]]
*Table 8: Comparison of facial consistency between GPT-Image-Edit-1.5M [38] and UnicEdit-10M*

从数据构建效率看，Table 3 揭示了后验证阶段的过滤强度：初始约 15.7M 个编辑结果中，约 26% 被判定为失败编辑（无变化或错误编辑）而丢弃，最终保留约 11.6M 个高质量三元组。这一过滤率说明，若不引入统一后验证，数据集中将有超过四分之一的噪声样本。

![[assets/figures/papers/paper_list_l798_https_arxiv_org_abs_2512_02790/figures/007_Table_3.jpg]]
*Table 3: Data volume statistics at each stage of our pipeline. Ratio indicates the percentage change from the previous stage, and Gen. abbreviates Generation. FLUX and Qwen refer to FLUX.1- Kontext [3] and Qwen-Image-Edit [41], respectively*

### UnicBench 模型性能全景：复杂推理编辑是共同短板

Table 4 汇总了主流模型在 UnicBench 上的综合表现。闭源模型中，**GPT-Image-1** 以 Overall-EN 8.3546 分领先，Seedream 4.0 以 8.0428 分居次（差距 0.3118）。开源模型中，**Qwen-Image-Edit** 取得 7.7273 分，而 InstructPix2Pix 仅为 2.9221 分，差距悬殊。

![[assets/figures/papers/paper_list_l798_https_arxiv_org_abs_2512_02790/figures/008_Table_4.jpg]]
*Table 4: Overall performance of different model on UnicBench. The performance of open-source and closed-source models is separately marked with the best performance in bold, and the second best underlined*

细粒度分析揭示了关键瓶颈：几乎所有模型在 **RA（推理准确性）** 维度上的得分远低于 IF（指令遵循）、NC（非编辑一致性）和 VQ（视觉质量）。以 Figure 11 中复杂编辑子任务（如视角变换、文本修改、知识推理）为例，RA 得分普遍处于低位，表明当前模型在需要空间推理和语义理解的编辑上存在系统性缺陷。这验证了 UnicBench 作为诊断工具的价值：传统评估指标（如 VIEScore）无法暴露此类细粒度能力差异。

![[assets/figures/papers/paper_list_l798_https_arxiv_org_abs_2512_02790/figures/020_Figure_11.jpg]]
*Figure 11: Performance of four evaluation dimensions for each sub-task. The top row shows results for EN tasks, and the bottom row shows results for CN tasks. All results are evaluated by GPT-4.1*

### Qwen-Verify 专家模型验证：小模型超越大模型

Table 5 展示了后验证专家模型 Qwen-Verify 与基线的准确性对比。在三个验证类别上，Qwen-Verify 均超越 72B 规模的通用大模型 Qwen2.5-VL-72B：Normal 类别 6.32 vs 5.25，No Edit 类别 9.80 vs 9.60，Hallucination 类别 6.22 vs 6.12。这证明通过专门化训练，7B 小模型可在特定验证任务上超越通用大模型，同时大幅降低计算成本。

![[assets/figures/papers/paper_list_l798_https_arxiv_org_abs_2512_02790/figures/009_Table_5.jpg]]
*Table 5: Performance of post-verification expert model*

消融实验进一步揭示了 D²PO 训练阶段的关键作用：加入 D²PO 偏好对齐后，Hallucination 准确性从仅 SFT 的 5.47 提升至 6.22（Table 5），表明偏好优化能有效减少模型在验证时的幻觉倾向。此外，与像素级度量 SSIM 的对比（Fig. 6）表明，SSIM 对微小有效编辑给出高相似度分数，而对无编辑样本却可能降低分数，缺乏语义感知能力。这从反面证明了训练语义感知验证模型的必要性。

### 评估指标的有效性验证

细粒度指标 **NC（非编辑一致性）** 展现出超越传统综合指标的诊断能力。Fig. 8 的案例分析表明，NC 能够发现 VIEScore 忽略的非目标区域意外变化，如误删人物、文字篡改等。这验证了 UnicBench 采用的多维度、任务自适应评估策略（基本编辑使用 IF、NC、VQ 的几何平均，复杂编辑额外加入 RA）的合理性——任一维度的严重失败都会通过几何平均机制显著拉低总分，避免了算术平均对弱项的掩盖效应。

![[assets/figures/papers/paper_list_l798_https_arxiv_org_abs_2512_02790/figures/015_Figure_8.jpg]]
*Figure 8: Comparison between GEdit-Bench’s [23] metrics and UnicBench’s metrics. (a) compares scoring for a case with an unexpected removal. (b) compares scoring for a case with an unexpected text change*

### 公平性说明与局限

需要注意的是，UnicBench 的所有评估均基于 GPT-4.1 或 Qwen2.5-VL-72B 作为 VLM 评判器，可能引入评判器自身的偏好偏差。RA 指标依赖推理点（reasoning points）的完备性，若推理点覆盖不全，评分可能存在变异性。此外，基准规模（1100 样本）有限，复杂编辑任务的样本比例仍有提升空间，模型在空间推理和文本修改等任务上的表现仍不理想。

### 补充图表

![[assets/figures/papers/paper_list_l798_https_arxiv_org_abs_2512_02790/figures/018_Figure_10.jpg]]
*Figure 10: Overall score of each model on the sub-tasks in UnicBench, for EN (left) and CN (right) instructions. All results are evaluated by GPT-4.1*



## 定位与知识库关联

### 1. 数据构建范式的演进与定位

图像编辑数据集长期面临**规模与质量的双重困境**：人工标注质量高但不可扩展，自动化流水线则充满噪声且后验证不全面。UnicEdit-10M 的构建管线在以下维度上区别于既有工作：

**端到端编辑 vs. 多工具链**：早期自动化流水线如 **InstructPix2Pix** 依赖合成数据但缺少质量验证；**SEED-Data-Edit**、**UltraEdit**、**ImgEdit** 等采用多工具链分段调用，错误容易在模块间累积传播。UnicEdit 管线以端到端编辑模型（FLUX.1-Kontext、Qwen-Image-Edit）替代多工具链，从源头减少错误累积。

**统一后验证 vs. 单维度后处理**：**NHR-Edit** 仅进行失败检测的后过滤；**GPT-Image-Edit-1.5M** 使用昂贵的 GPT-4o API 进行指令重描述，但缺少失败检测且人脸一致性仅 0.30。UnicEdit 的核心创新在于将**失败检测与指令重描述统一为双任务框架**，由一个紧凑的 7B 专家模型 Qwen-Verify 执行，在语义对齐和视觉质量上同时取得突破（VIEScore Overall 8.08，人脸一致性 0.89）。

**蒸馏式验证 vs. 通用大模型调用**：Qwen-Verify 的设计哲学是将原本依赖大型模型的后验证任务蒸馏为小型化、语义感知的专家模型。实验表明，Qwen-Verify 在所有验证类别（Normal 6.32、No Edit 9.80、Hallucination 6.22）的准确性均超越 Qwen2.5-VL-72B（5.25 / 9.60 / 6.12），证明专用小模型在特定验证任务上可以超越通用大模型，同时大幅降低计算成本。

### 2. 核心机制：D²PO 偏好优化

Qwen-Verify 的训练采用两阶段策略：监督微调（SFT）建立基础能力，随后通过 **Differential Direct Preference Optimization（D²PO）** 进行偏好对齐。D²PO 的关键设计在于引入**视觉差异上下文** $c_v = \mathcal{V}(I_o, I_e)$，即从原始图像 $I_o$ 和编辑图像 $I_e$ 中提取的编辑动态潜在表示，作为策略优化的条件输入。

基于 Bradley-Terry 偏好模型，D²PO 通过最大化偏好指令和拒绝指令之间的优势边界来对齐模型与人类判断：

$$\mathcal{L}_{\mathrm{D^2PO}} = -\mathbb{E}_{(c_v, p_w, p_l) \sim \mathcal{D}} [\log \sigma \left( \mathcal{A}_{\pi_\theta, \pi_{\mathrm{ref}}}(p_w, c_v) - \mathcal{A}_{\pi_\theta, \pi_{\mathrm{ref}}}(p_l, c_v) \right)]$$

其中策略优势函数定义为：

$$\mathcal{A}_{\pi_\theta, \pi_{\mathrm{ref}}}(p, c_v) = \beta \log \frac{\pi_\theta(p | c_v)}{\pi_{\mathrm{ref}}(p | c_v)}$$

消融实验证实 D²PO 阶段至关重要：加入 D²PO 后，Hallucination 准确性从 SFT 的 5.47 提升至 6.22，表明偏好对齐能有效减少幻觉。语义敏感的专家模型在 No Edit 检测上显著优于传统像素级 SSIM——SSIM 对微小有效编辑给出高相似度，而对无编辑样本却降低分数，证明了深度学习验证的必要性。

### 3. 评估体系的差异化贡献

UnicBench 的评估体系在以下方面提供了独特的诊断能力：

**几何平均评分**：编辑分数采用几何平均 $\mathrm{Score} = (\prod_{m \in \mathcal{M}} m)^{1/|\mathcal{M}|}$，基本编辑使用 {IF, NC, VQ}，复杂编辑增加 {RA}。几何平均的惩罚特性使得任一维度严重失败均会大幅拉低总分，避免算术平均掩盖短板。

**细粒度非编辑一致性（NC）**：NC 指标能够发现 VIEScore 忽略的非目标区域意外变化（如误删人物、文字篡改），提供更具诊断性的评估。

**推理准确性（RA）瓶颈揭示**：UnicBench 评估揭示几乎所有模型在 RA 上的表现远低于其他指标，说明复杂推理编辑是当前模型的共同短板。这一发现直接验证了针对性数据和基准的必要性，也为后续研究指明了方向。

### 4. 适用边界与局限

尽管 UnicEdit-10M 在规模和质量上取得突破，以下边界条件值得注意：

- **编辑模型依赖性**：数据集质量依赖于所使用的编辑模型（FLUX.1-Kontext、Qwen-Image-Edit）的能力，可能继承其固有偏见和限制。
- **任务覆盖不均衡**：尽管覆盖 22 个任务，复杂编辑（尤其是空间推理和文本修改）的样本比例和质量仍有提升空间，模型在该类任务上的表现仍不理想。
- **验证模型泛化性**：Qwen-Verify 仅针对图像编辑任务训练，其泛化到其他视觉对齐任务的能力未经验证。
- **基准规模限制**：UnicBench 仅含 1100 个样本，可能无法完全代表真实世界编辑指令的多样性和难度。
- **评判器偏差**：所有评估均基于 GPT-4.1 或 Qwen2.5-VL-72B 作为 VLM 评判器，可能引入评判器自身的偏好和偏差。RA 指标依赖推理点的完备性，若推理点覆盖不全，则可能导致评分变异性。

### 5. 开放问题

1. **复杂推理能力的突破路径**：如何利用 UnicEdit-10M 训练下一代开源图像编辑模型，以在复杂推理能力上逼近甚至超越闭源模型？复杂编辑任务的性能瓶颈究竟是来自模型架构、训练数据还是评估方式本身？
2. **验证框架的跨任务泛化**：能否将统一后验证框架扩展至视频编辑、3D 编辑等更广泛的视觉生成任务，以低资源实现高质量数据生产？
3. **无模型评估方法**：当前评估仍依赖 VLM 评判器，如何设计更客观、无模型的自动化评估方法，特别是针对推理准确性？
4. **数据分布与真实场景的对齐**：数据集源图像来自内部高美学得分库，可能过度代表特定风格或分布，未见低光照等困难场景的显式覆盖。如何在保持质量的同时扩大数据分布的覆盖面？



## 原文 PDF

![[paperPDFs/CVPR_2026/UnicEdit_10M_A_Dataset_and_Benchmark_Breaking_the_Scale_Quality_Barrier_via_Unified_Verification_for_Reasoning_Enriched_Edits.pdf]]
