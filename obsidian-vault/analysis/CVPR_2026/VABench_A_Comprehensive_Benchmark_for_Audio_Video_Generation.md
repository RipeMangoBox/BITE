---
title: "VABench: A Comprehensive Benchmark for Audio-Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VABench_A_Comprehensive_Benchmark_for_Audio_Video_Generation.pdf
project_link: null
code_link: null
aliases:
- VABench
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 通过构建覆盖多任务、多内容类别、多维度且自动化的双轨评估体系（专家模型+MLLM），提供可解释且与人类偏好一致的量化指标，揭示模型在语义、同步与真实性的冲突。
primary_logic: VABench 整合了 T2AV、I2AV 和立体声三大任务，涵盖七类内容和 15 个细粒度指标，首次全面揭示端到端 AV 模型整体优于解耦 V+A 方案，同时暴露在语义一致性、同步性和真实性之间难以同时达到最优的困境，为未来统一音视频建模提供了量化指引。
claims:
- "VABench contains three primary task types: T2AV, I2AV, and stereo audio-video generation."
- VABench incorporates 15 fine-grained metrics, including 8 based on expert models and 7 based on MLLMs.
- "VABench covers seven major content categories: animals, human sounds, music, environmental sounds, synchronous physical sounds, complex scenes, and virtual worlds."
- "The evaluation framework uses a dual-track approach: Expert Model-based Evaluation and MLLM-based Evaluation."
---

# VABench: A Comprehensive Benchmark for Audio-Video Generation

> [!tip] 核心洞察
> VABench 整合了 T2AV、I2AV 和立体声三大任务，涵盖七类内容和 15 个细粒度指标，首次全面揭示端到端 AV 模型整体优于解耦 V+A 方案，同时暴露在语义一致性、同步性和真实性之间难以同时达到最优的困境，为未来统一音视频建模提供了量化指引。

| 字段 | 内容 |
|------|------|
| 中文题名 | VABench：一个综合的音视频生成基准测试 |
| 英文题名 | VABench: A Comprehensive Benchmark for Audio-Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.09299) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | VABench |
| Dataset | VABench T2AV, VABench I2AV, VABench Audio QA |

> [!tip] 效果简介
> - VABench T2AV 上，Audio-Aes (audio aesthetic score) Veo3 (3.543) vs Sora2 (2.867) (+0.676)；Lip-Sync (higher better) Wan2.5 (3.671) vs Sora2 (2.655) (+1.016)。
> - VABench I2AV 上，Desync↓ (lower better) Wan2.5 (0.3539) vs Sora2 (0.9171) (-0.5632)；Alignment (coarse-grained MLLM score, 1-5) Seedance+MMAudio (4.918) vs Sora2 (4.885) (+0.033)。
> - VABench Audio QA (fine-grained) 上，Animals category QA accuracy Veo3 (approx. 0.83) vs Wan2.5 (approx. 0.79) (+0.04)。

## 概要

音视频（AV）生成领域近年来发展迅猛，但系统化评估手段的缺失严重制约了模型能力的客观比较与迭代方向的选择。现有基准或聚焦于单模态质量，或依赖粗粒度人工打分，普遍忽略**跨模态时序耦合**、**物理合理性**和**情感表达性**等决定生成体验的关键维度。VABench 正是针对这一瓶颈构建的首个综合性音视频生成基准，其核心目标是以可量化、可复现的方式揭示不同模型架构在语义对齐、同步精度与感知真实性之间的冲突与权衡。

VABench 的评估体系围绕三大任务展开：**文本到音视频（T2AV）**、**图像到音视频（I2AV）** 以及**立体声音视频生成**，覆盖动物、人类声音、音乐、环境声、同步物理声、复杂场景和虚拟世界七类内容。为了兼顾专业精度与语义理解，VABench 提出**双轨评估框架**：专家模型轨道通过专用模型量化单模态质量、跨模态语义对齐和时序同步（如音频美学分、唇音同步、去同步误差等）；多模态大语言模型（MLLM）轨道则从粗粒度 1–5 分评分和细粒度 QA 对两个层面模拟人类对复杂音视频语义的判断。整套体系共包含 15 项细粒度指标，并针对立体声生成引入声场宽度、相位一致性、单声道兼容性等九项声学指标。

主要实验结论揭示了一条清晰的模式：**端到端 AV 模型在整体表现上普遍优于“解耦视频生成 + 独立音频生成”的 V+A 方案**，但没有任何单一模型能在语义一致性、同步性和真实性三个维度上同时取得最优。例如，在 T2AV 任务中，Veo3 的音频美学分显著领先 Sora2（3.543 vs. 2.867），但 Wan2.5 在唇音同步上反超（3.671 vs. 2.655）；在 I2AV 任务中，Wan2.5 的去同步误差远低于 Sora2（0.3539 vs. 0.9171），而 Seedance+MMAudio 在粗粒度对齐评分上略占优势（4.918 vs. 4.885）。立体声生成方面，当前模型普遍无法从文本提示中可靠分离声道，多数输出近乎单声道，空间音效仍处于早期阶段。

VABench 的评估结果与人类偏好之间展现出较强的相关性（Pearson 系数在各维度上均有标注），验证了自动化指标的可信度。同时，论文也坦承若干局限：MLLM 在艺术性等主观维度上仍需要专业评估者校准；数据集中观察到的种族外貌偏差（Veo3 偏向高加索人种特征，Seedance 倾向亚洲人种特征）反映了训练数据的固有偏见；当前评估集中在约 5 秒的短视频片段，长视频中的时序一致性和累积误差尚未纳入考量。这些发现为未来统一音视频建模和更全面的评估体系提供了明确的量化指引。

### 问题背景

音视频生成（Audio-Video Generation）旨在从文本或图像等条件中同时合成视觉画面与同步音频，是通向沉浸式内容创作的关键技术。近年来，扩散模型与自回归模型在单模态生成上取得了显著进展，但将视听双模态联合建模仍面临根本性挑战：视觉与听觉信号在时间轴上必须保持精确的因果耦合（如敲击声与物体碰撞瞬间的对齐），在语义层面需要共享一致的概念空间（如“小提琴演奏”需同时呈现乐器外观与弦乐音色），而在物理真实性上还需满足声学传播的客观规律。这些跨模态约束交织在一起，使得同步音视频生成的质量评估远比单模态任务复杂。

### 现有方法缺口

当前领域面临的核心瓶颈是：**缺乏一个能够系统评估同步音视频生成质量的综合基准**。现有的评估实践存在三重缺口：

1. **任务覆盖碎片化**。多数基准仅关注单一生成范式（如文本到视频），忽略了文本到音视频（T2AV）、图像到音视频（I2AV）以及立体声生成等关键任务的统一评估需求，导致不同模型在异构设定下的性能无法横向比较。

2. **评估维度单一**。现有指标往往聚焦于视觉质量或音频质量的独立评价，严重忽略了跨模态时序耦合（如唇音同步、事件同步）、物理合理性（如声源定位与空间成像）以及情感表达性等高阶语义维度。这些被忽略的维度恰恰是决定用户体验“真实感”的关键因素。

3. **自动化与人类偏好脱节**。传统客观指标（如PSNR、FID）与人类感知判断之间的相关性较弱，而纯人工评估成本高昂且难以复现。领域亟需一套既能自动化执行、又能与人类偏好保持高度一致的评估框架。

### 本文动机

为填补上述缺口，VABench 提出了一个**覆盖多任务、多内容类别、多维度且自动化的双轨评估体系**。该基准整合了 T2AV、I2AV 和立体声三大生成任务，涵盖动物、人类声音、音乐、环境声、同步物理声、复杂场景和虚拟世界七类内容，并通过专家模型与多模态大语言模型（MLLM）两条互补路径，在 15 个细粒度指标上量化模型在语义一致性、同步性和真实性之间的权衡。VABench 的核心洞察在于：**端到端音视频模型（AV）在整体表现上普遍优于解耦的视频+音频级联方案（V+A），但所有模型都面临语义对齐、时序同步与物理真实性难以同时达到最优的困境**——这一发现为未来统一音视频建模提供了明确的量化指引。

## 核心方法与创新机理

VABench 的核心创新并非提出一个新的音视频生成模型，而是构建了首个系统评估同步音视频生成质量的综合基准，其关键突破在于填补了跨模态时序耦合、物理合理性与情感表达性等维度的评估空白。

### 1. 三维任务与七类内容的覆盖设计

现有音视频生成评估通常局限于单一任务或狭窄的内容类型，无法反映模型在真实场景下的泛化能力。VABench 首次将三类核心任务——文本到音视频（T2AV）、图像到音视频（I2AV）和立体声音视频生成——统一纳入同一基准，并覆盖七大类内容：动物、人类声音、音乐、环境声、同步物理声、复杂场景和虚拟世界（见 Figure 3）。这种设计使得评估能够揭示模型在不同声学语义和视觉复杂度下的差异化表现，例如在动物类别中 Veo3 的细粒度音频 QA 准确率约为 0.83，而 Wan2.5 约为 0.79（Figure 6a），差异虽小但反映了模型对特定声学模式的理解差异。

### 2. 双轨评估体系的因果机制

VABench 的核心洞察在于：单一评估范式无法同时捕捉感知质量与语义理解。为此，它提出了**专家模型评估 + MLLM 评估**的双轨框架，形成互补的量化信号。

**专家模型轨道**负责精确量化单模态质量、跨模态语义对齐和时序同步。其中，音频美学分数通过聚合内容享受度（CE）、内容有用度（CU）、制作质量（PQ）和制作复杂度（PC）得出：

$$\mathrm{S_{audioaesthetic} = \frac{CE + CU + PQ - PC}{4}}$$

PC 与感知质量负相关，因此被减去——这一设计直接反映了“复杂不等于好听”的声学感知规律。此外，Desync 指标专门量化音视频时序偏移，揭示了解耦 V+A 方案的关键瓶颈：在 I2AV 任务中，Wan2.5 的 Desync 为 0.3539，而 Sora2 高达 0.9171（Table 2），说明端到端 AV 模型在时序同步上具有显著优势。

**MLLM 轨道**则模拟人类对复杂音视频语义的整体判断，在粗粒度（1–5 分）和细粒度（QA 对）两个层面评估对齐度、艺术性、表现力和真实感。细粒度评估的整体准确率定义为：

$$S = \frac{1}{N} \sum_{i=1}^{N} \frac{C_i}{K_i}$$

其中 $N$ 为样本数，$K_i$ 为每样本的细节问题数，$C_i$ 为被判定满足要求的问题数。这一指标直接量化了模型对音视频细节的理解精度，而非仅依赖宏观印象分。

### 3. 立体声评估的声学维度创新

立体声生成是音视频领域的前沿难题，此前缺乏系统化的评估手段。VABench 基于九个核心声学指标，从**空间成像质量**和**信号完整性与兼容性**两个维度评估立体声生成。这些指标包括声场宽度（Mid/Side 能量比）、相位一致性（低频/中频/高频）、单声道兼容性、瞬态同步、电平稳定性、包络相关性和成像稳定性（Figure 7）。论文明确指出，当前模型无一能从文本提示中可靠生成立体声分离，多数输出近乎单声道，这一发现直接暴露了现有方法在空间音效建模上的根本性缺陷。

### 4. 揭示的模型能力冲突

VABench 最具洞察力的贡献在于揭示了音视频生成中**语义一致性、同步性与真实性之间的不可能三角**。以 Sora2 为例，它在视觉真实感（Visual Realism 4.805）和音频真实感（Audio Realism 4.375）上表现突出，但在音频美学（2.867）和唇音同步（Lip-Sync 2.655）上显著落后于 Veo3（Table 1）。这种冲突表明，当前模型在追求单一维度极致性能时，往往以牺牲其他维度为代价，而 VABench 的多维评估体系首次为这一权衡提供了可量化的证据。

### 5. 与人类偏好的对齐验证

自动化指标的可靠性取决于其与人类判断的一致性。VABench 通过 Pearson 相关系数验证了其评估结果与人类偏好的对齐程度（Figure 8），为自动化评估的可信度提供了统计依据。但需注意，在艺术性等高度主观的维度上，MLLM 评估仍可能无法完全反映人类感知，这一点论文自身也明确承认，需要人工校准作为补充。

### 方法谱系与知识库定位

VABench 属于**生成模型评估基准**类别，其方法谱系可追溯至图像生成领域的 FID、CLIP Score 等自动化指标，以及视频生成领域的 VBench 等多维评估框架。但与这些前序工作不同，VABench 首次将评估焦点从单模态质量扩展到跨模态时序耦合和立体声空间属性，填补了音视频同步生成评估的空白。其双轨设计（专家模型 + MLLM）与 VBench 的“能力维度分解”思路有方法论上的延续性，但 VABench 在声学维度和立体声评估上的创新是独有的。需要注意的是，当前基准主要针对 5 秒左右的短视频，长视频中的时序一致性和累积误差尚未纳入评估范围，这是未来扩展的重要方向。

VABench 围绕“条件生成 → 双轨评估”这一核心流程构建，旨在系统性地量化音视频生成模型在语义对齐、时序同步与感知真实性三个关键维度上的表现。框架整体由三大组件构成：**任务定义与数据构建**、**专家模型评估** 以及 **MLLM 评估**，三者形成从输入条件到多粒度评分的完整闭环。

### 任务体系与数据构建

VABench 覆盖三类主流音视频生成任务：**文本到音视频（T2AV）**、**图像到音视频（I2AV）** 以及**立体声音视频生成**。为支撑多维评估，基准测试构建了覆盖七大内容类别的条件数据集——动物、人声、音乐、环境声、同步物理声、复杂场景和虚拟世界。数据构建采用双路径策略：T2AV 分支利用大语言模型生成结构化文本提示，I2AV 分支则借助视觉-语言模型从图像中提取语义条件，两条路径均经过严格的人工验证以确保语义准确性与音视频一致性。

### 双轨评估架构

评估体系采用“专精 + 全局”的双轨设计，分别对应专家模型评估与多模态大语言模型评估两个模块。

**专家模型评估**聚焦于可量化的感知质量指标，覆盖三个核心维度：
- **单模态质量**：通过语音清晰度、音频美学评分等指标独立评估音频与视频的生成质量。其中音频美学分数由内容享受度、内容有用度、制作质量与制作复杂度四项子指标聚合得出，公式为：

$$S_{\text{audioaesthetic}} = \frac{CE + CU + PQ - PC}{4}$$

- **跨模态语义对齐**：分别计算文本-视频、文本-音频以及音视频之间的语义对齐分数，衡量生成内容与输入条件的一致性。
- **时序同步**：通过去同步检测和唇音同步指标评估音视频在时间轴上的耦合精度。

**MLLM 评估**则模拟人类对复杂音视频语义的整体判断，在两个粒度上展开：
- **粗粒度**：对对齐度、表现力、视觉真实感、音频真实感等宏观维度进行 1–5 分制打分。
- **细粒度**：通过结构化的 QA 对，逐样本检验生成内容在细节层面的准确性。细粒度整体得分定义为所有样本的平均准确率：

$$S = \frac{1}{N} \sum_{i=1}^{N} \frac{C_i}{K_i}$$

其中 $N$ 为样本数，$K_i$ 为第 $i$ 个样本的细节问题总数，$C_i$ 为被判定满足要求的问题数。

### 立体声专项分析

针对立体声音视频生成任务，框架引入基于九项核心声学指标的专项分析，从**空间成像质量**和**信号完整性与兼容性**两个维度进行评估，涵盖声场宽度、相位一致性、单声道兼容性等关键参数。

### 输入输出流

整体流程可概括为：**条件输入**（文本/图像）→ **生成模型推理** → **双轨评估**。评估模块并行接收生成结果，专家模型输出客观量化分数，MLLM 输出语义级评分与细粒度准确率，最终汇总为覆盖 15 个维度的综合评估报告。这一架构使得不同模型在语义一致性、同步精度和感知真实性之间的权衡关系得以显式暴露，为模型诊断与改进提供可解释的量化依据。

### 补充图表

![[assets/figures/papers/paper_list_l803_https_arxiv_org_abs_2512_09299/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the VABench framework, illustrating its three main components: (1) The audio-video generation tasks being evaluated (T2AV, I2AV, and stereo), (2) the detailed taxonomy of evaluation contexts (e.g., human sounds, complex scenes), and (3) the evaluation pipeline*

![[assets/figures/papers/paper_list_l803_https_arxiv_org_abs_2512_09299/figures/004_Figure_4.jpg]]
*Figure 4: Overview of the pipeline for benchmark data curation. This process is used to generate the text conditions for T2AV tasks and the image conditions for I2AV tasks*

![[assets/figures/papers/paper_list_l803_https_arxiv_org_abs_2512_09299/figures/003_Figure_3.jpg]]
*Figure 3: VABench’s seven content categories, illustrated with example text prompts and representative images*

VABench 的评估体系围绕一个双轨框架构建，将专用模型的精确量化与多模态大语言模型（MLLM）的整体语义理解相结合。该框架由三个核心评估模块组成：专家模型评估、MLLM 评估和立体声分析。

### 专家模型评估模块

该模块针对三个关键维度进行量化：单模态质量、跨模态语义对齐和时序同步。其核心指标包括语音清晰度与自然度（Speech Q&N）、音频美学质量（Audio Aesthetic）、文本-视频/文本-音频/音视频对齐度（T-V/T-A/A-V Align）、失同步度（Desync）和唇音同步度（Lip-Sync）。

其中，音频美学分数通过一个聚合公式计算，综合了四个感知维度：

$$ \mathrm{S_{audioaesthetic} = \frac{CE + CU + PQ - PC}{4}} $$

其中，$CE$ 表示内容享受度（Content Enjoyment），$CU$ 表示内容有用度（Content Usefulness），$PQ$ 表示制作质量（Production Quality），$PC$ 表示制作复杂度（Production Complexity）。由于制作复杂度与感知质量呈负相关，该项在聚合时被减去。

### MLLM 评估模块

MLLM 评估在两个互补层级上进行：粗粒度宏观评分（1–5 分）和细粒度微观问答。宏观评分覆盖对齐度（Alignment）、表现力（Expressiveness）、视觉真实感（Visual Realism）和音频真实感（Audio Realism）等维度。微观层面则通过细节问答对来检验模型对音视频内容的理解精度，其整体准确率计算公式为：

$$ S = \frac{1}{N} \sum_{i=1}^{N} \frac{C_i}{K_i} $$

其中，$N$ 为样本总数，$K_i$ 为第 $i$ 个样本的细节问题数量，$C_i$ 为该样本中被判定为满足要求的问题数量。该公式本质上计算了所有样本上细节问题正确率的平均值。

### 立体声分析模块

针对立体声音视频生成任务，该模块从空间成像质量和信号完整性/兼容性两个维度，设计了九个核心声学指标进行评估，包括：低频/中频/高频相位一致性（Coh Low/Mid/High）、单声道兼容性（Mono Compat）、声场宽度（Width）、瞬态同步性（Transient Sync）、电平稳定性（Level Stability）、包络相关性（Env Corr）和成像稳定性（Imaging Stability）。这些指标共同刻画了立体声生成在空间定位、相位保真度和下混兼容性方面的表现。

## 实验与关键发现

### 评估设置与基线模型

VABench 在 T2AV 和 I2AV 两项核心任务上对两类生成系统进行了全面评测：端到端音视频模型（AV）与解耦式视频+音频方案（V+A）。端到端模型包括 **Veo3-fast**、**Wan2.5 Preview** 和 **Sora2**；解耦方案则由视频生成器（如 **Seedance 1.0**、**Wan2.2**、**Kling 2.5**）与音频生成器（**MMAudio**）组合而成。所有视频输出统一设置为 720P 分辨率，帧率和时长遵循各模型默认配置，音频则通过各模型原生接口生成。

### T2AV 主结果：端到端模型的整体优势与维度间冲突

Table 1 汇总了 T2AV 任务的完整评测结果。端到端 AV 模型在多数指标上展现出对解耦 V+A 方案的系统性优势，但不同模型在语义一致性、同步性与真实性三个维度之间呈现出明显的“不可能三角”特征。

![[assets/figures/papers/paper_list_l803_https_arxiv_org_abs_2512_09299/figures/005_Table_1.jpg]]
*Table 1: T2AV evaluation results. The results for AV and V+A models are separated by a horizontal line. Underlined scores indicate the highest within each category (AV or V+A), and bolded scores indicate the overall best for each metric*

**Veo3** 在音频美学质量（Audio-Aes 3.543）和音频问答（Audio QA 0.8314）上取得最优，较 Sora2 的 Audio-Aes（2.867）提升 +0.676，表明其在音质感知和音频语义理解方面具有显著领先性。然而，Veo3 在视觉真实性（Visual Realism 4.614）上不及 Sora2（4.805），在跨模态对齐指标（T-V Align 0.2607, A-V Align 0.2712）上亦非最优。

**Wan2.5** 在唇音同步（Lip-Sync 3.671）和去同步检测（Desync↓ 0.4387）上表现最佳，Lip-Sync 较 Sora2（2.655）领先 +1.016，Desync 远低于 Sora2（0.7167），说明其时序耦合能力突出。但 Wan2.5 的音频美学（2.882）和音频真实性（3.612）相对薄弱。

**Sora2** 在视觉真实性（4.805）和视觉问答（Visual QA 0.8249）上占据优势，但音频美学（2.867）和同步性（Lip-Sync 2.655, Desync 0.7167）均明显落后，形成“真实但不协调”的典型模式。

解耦 V+A 方案中，**Seedance+MMAudio** 在粗粒度对齐（Alignment 4.918）和表现力（Expressiveness 4.601）上表现突出，甚至超越了部分端到端模型，但在细粒度音频问答（0.7421）和视觉问答（0.6890）上存在明显短板，反映出解耦方案在跨模态细粒度语义耦合上的固有局限。

### I2AV 主结果：时序同步成为关键区分维度

Table 2 展示了 I2AV 任务的评测结果。与 T2AV 相比，I2AV 场景下模型间的差异在同步性维度上更为显著。

![[assets/figures/papers/paper_list_l803_https_arxiv_org_abs_2512_09299/figures/006_Table_2.jpg]]
*Table 2: I2AV evaluation results, following the same presentation protocol as Tab. 1 (T2AV)*

**Wan2.5** 在去同步指标上以 Desync↓ 0.3539 大幅领先 Sora2（0.9171），差值达 -0.5632，再次验证其在时序对齐上的核心能力。同时，Wan2.5 的音频美学（3.196）和音频问答（0.7980）亦处于较高水平。

**Veo3** 在音频美学（3.201）和音频真实性（4.529）上表现稳健，但 Desync（0.7738）显著高于 Wan2.5，说明其在视觉条件输入下的时序同步仍有改善空间。

解耦方案 **Seedance+MMAudio** 在粗粒度对齐（4.918）上继续领先，但其 Desync（0.5478）和细粒度音频问答（0.7421）同样暴露了跨模态精细对齐的不足。

### 细粒度类别分析：音频语义理解的差异化能力

Figure 6 按七类音频内容（Animals, Human Sounds, Music, Environmental, Synchronous Physical Sounds, Complex Scenes, Virtual Worlds）展示了各模型的细粒度 QA 准确率。

![[assets/figures/papers/paper_list_l803_https_arxiv_org_abs_2512_09299/figures/008_Figure_6.jpg]]
*Figure 6: Fine-grained QA evaluation across seven audio categories for different model architectures*

在音频 QA 维度（Figure 6a），**Veo3** 在 Animals 类别上取得最高准确率（约 0.83），较 Wan2.5（约 0.79）领先约 +0.04，体现了其对动物声学特征的精准捕捉。**Sora2** 在七类内容上表现最为均衡，无明显弱项，但在 Music 类别上各模型普遍偏低，反映出音乐生成中对旋律、和声等结构化声学语义的理解仍是共同瓶颈。

视觉 QA 维度（Figure 6b）上，Sora2 凭借其视觉真实性的整体优势在多数类别中领先，但各模型在 Virtual Worlds 类别上的视觉问答准确率均相对较低，说明对非真实感渲染场景的语义理解仍有待提升。

### 立体声生成评估：空间音效尚处早期阶段

Figure 7 以雷达图形式对比了 Veo3、Sora2 和 Wan2.5 在九个声学指标上的表现，涵盖声场宽度（Width）、相位一致性（Coh Low/Mid/High）、单声道兼容性（Mono Compat）、瞬态同步（Transient Sync）、电平稳定性（Level Stability）、包络相关性（Env Corr）和成像稳定性（Imaging Stability）。

![[assets/figures/papers/paper_list_l803_https_arxiv_org_abs_2512_09299/figures/010_Figure_7.jpg]]
*Figure 7: Comparative radar chart of three models: Phase Coherence (Coh Low/Mid/High), Mono Compatibility (Mono Compat), Soundstage Width (Width), Transient Synchronization (Transient Sync), Level Stability, Envelope Correlation (Env Corr), and Imaging Stability. Higher values indicate better performance*

三款模型在声场宽度和相位一致性上均未展现出成熟的立体声分离能力，多数指标接近单声道水平。论文明确指出，当前模型无一能从文本提示中可靠生成立体声分离，空间音效生成整体仍处于初级阶段。Veo3 和 Sora2 在部分指标上略有分化，但优势幅度有限，立体声生成仍是该领域的核心开放问题。

### 人类偏好一致性验证

Figure 8 展示了 VABench 自动化评分与人类偏好在各评估维度上的相关性。每个子图对应一个评测维度，数据点表示各模型在人类评估（x 轴）和 VABench 评分（y 轴）上的胜率，Pearson 相关系数（ρ）标注于图中。各维度的相关性均达到较高水平，验证了 VABench 双轨评估框架（专家模型+MLLM）与人类判断的一致性，为自动化基准测试的可靠性提供了实证支撑。

![[assets/figures/papers/paper_list_l803_https_arxiv_org_abs_2512_09299/figures/009_Figure_8.jpg]]
*Figure 8: Human preference consistency validation. Each subplot shows one evaluation dimension, where each point denotes a model’s win rate (x: human, y: VABench). A reference line indicates their correlation, with the Pearson coefficient (ρ) annotated*

### 定性对比：典型成功与失败模式

Figure 5 展示了 I2AV、Stereo 和 T2AV 三类任务上的成对定性对比，通过关键视频帧和音频波形直观呈现模型差异。

![[assets/figures/papers/paper_list_l803_https_arxiv_org_abs_2512_09299/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison of model performance. We visualize pairwise comparisons across three tasks (I2AV, Stereo, T2AV) by showing key video frames and audio waveforms*

在 T2AV 场景中，Veo3 生成的音频波形在节奏和能量分布上与视觉内容高度匹配，而 Sora2 虽视觉质量优异，但音频波形与画面动作的时序对应存在可察觉偏差。在 I2AV 场景中，Wan2.5 展现出精准的唇音同步和动作-声效对齐，而解耦方案 Seedance+MMAudio 在复杂场景下偶现声画错位。立体声场景的波形对比进一步印证了定量结论：各模型输出的左右声道差异微弱，空间定位信息不足。

### 偏差与局限性观察

论文附录（Figure 21）揭示了生成模型存在人口统计学偏差：Veo3 生成的面孔主要呈现高加索人种特征，而 Seedance 生成的面孔倾向亚洲人种特征。这一偏差源于训练数据分布的不均衡，论文建议未来需对此进行定量分析和缓解。

![[assets/figures/papers/paper_list_l803_https_arxiv_org_abs_2512_09299/figures/023_Figure_21.jpg]]
*Figure 21: Demographic tendencies in generated human subjects across models. This figure illustrates appearance biases observed during manual inspection*

此外，当前评估主要针对约 5 秒的短视频片段，长视频中的时序一致性和累积误差尚未纳入评测体系。MLLM 评估在艺术性等主观维度上虽与人类偏好相关，但仍可能无法完全捕捉专业领域的细微感知差异，需依赖专业评估者校准。

### 补充图表

![[assets/figures/papers/paper_list_l803_https_arxiv_org_abs_2512_09299/figures/012_Table_4.jpg]]
*Table 4: The attributes of the videos generated by each model*

## 定位与知识库关联

### 1. 基准设计的知识定位

VABench 的提出根植于当前音视频生成评估领域的系统性空白。现有的评估手段主要沿两条路径展开：一是对视频和音频模态分别进行独立的质量打分（如 FVD、FAD），完全忽略跨模态时序耦合；二是依赖单一维度的整体评分（如整体偏好投票），无法定位模型在语义对齐、同步精度、物理合理性等关键维度上的具体瓶颈。VABench 通过构建覆盖 **T2AV、I2AV 和立体声生成**三大任务、**七类内容**（动物、人声、音乐、环境声、同步物理声、复杂场景、虚拟世界）和 **15 个细粒度指标**的综合基准，首次填补了这一评估体系的空缺。

其核心设计理念——双轨评估框架——体现了对评估可靠性问题的深层洞察：**专家模型评估**（Expert Model-based Evaluation）利用专用模型在单模态质量、跨模态语义对齐和时序同步三个维度上提供精确量化，例如通过公式

$$\mathrm{S_{audioaesthetic} = \frac{CE + CU + PQ - PC}{4}}$$

聚合音频美学分数，其中 PC（制作复杂度）与感知质量负相关故被减去；**MLLM 评估**（MLLM-based Evaluation）则在粗粒度（1–5 分宏观评分）和细粒度（基于 QA 对逐项核验，整体准确率由 $S = \frac{1}{N} \sum_{i=1}^{N} \frac{C_i}{K_i}$ 给出）两个层面模拟人类对复杂音视频语义的判断。这种“专用精度 + 整体理解”的组合策略，与单纯依赖人工评分或单一自动化指标的已有工作形成鲜明对比。

### 2. 与已有方法的谱系关系

从评估范式来看，VABench 的专家模型评估模块可视为对传统单模态评估指标（如用于音频的 SpeechClarity、用于视频的视觉质量评分）的跨模态扩展和系统化整合。其 MLLM 评估模块则借鉴了近期多模态大模型在图文理解评估中的成功经验（如利用全模态 LLM 进行开放式语义判断），并将其首次系统性地应用于音视频联合生成场景。

在立体声评估方面，VABench 引入了九个核心声学指标（声场宽度、相位一致性、单声道兼容性、瞬态同步等），构建了空间成像质量和信号完整性两个维度的量化体系。这一设计填补了现有生成模型评估中几乎完全忽略空间音效维度的空白。

需要指出的是，论文中并未明确列出与 VABench 直接可比的完整基准工作（如某个已发表的音视频生成评估框架）作为对比基线。VABench 本身定位为**基准测试基础设施**而非生成模型，其“baseline”实际上是它所评估的各类生成系统——包括端到端 AV 模型（Veo3、Wan2.5 Preview、Sora2）和解耦 V+A 模型（如 Seedance + MMAudio 等组合）。这种设计使 VABench 更接近于 ImageNet 之于图像分类、EvalCrafter 之于视频生成的定位，即通过统一且多维度的评估框架来驱动领域进展。

### 3. 适用边界与核心局限

VABench 的评估能力存在明确的边界约束：

- **时长限制**：当前评估主要针对约 5 秒的短视频片段，长视频中的时序一致性累积误差、长程语义跟踪和场景切换音效连贯性等关键问题尚未覆盖。
- **立体声生成的评估深度**：尽管引入了九个声学指标，论文明确指出当前模型无一能从文本提示中可靠生成立体声分离，多数输出仍近乎单声道。这意味着立体声评估模块目前主要用于暴露模型的空间音效缺陷，而非衡量成熟能力。
- **主观维度的评估保真度**：MLLM 评估在艺术性、表现力等主观维度上仍可能无法完全反映人类感知。尽管论文通过人类偏好一致性验证（Figure 8）展示了较强的 Pearson 相关性，但在专业音乐理论、声学物理等领域知识的评估上仍依赖评估者的校准。
- **数据偏差的传递**：论文附录观察到生成模型存在人口统计学偏差——Veo3 生成的面孔主要呈现高加索人种特征，而 Seedance 生成的面孔倾向亚洲人种特征（Figure 21）。这种偏差反映了训练数据的偏见，VABench 的评估结果也因此可能受到这些系统性偏差的污染。

### 4. 开放问题与未来方向

VABench 的评估结果揭示了当前音视频生成领域的若干结构性困境，为后续研究指明了方向：

**语义-同步-真实性的三维冲突**：实验表明，端到端 AV 模型整体优于解耦 V+A 方案，但无一模型能在语义一致性、同步性和真实性三个维度上同时达到最优。例如 Sora2 在真实感上表现突出，却在音频美学和同步性上明显落后；Veo3 综合表现最强，但在某些内容类别（如复杂场景）的细粒度 QA 上仍有明显短板。如何在模型架构层面调和这三个维度的内在冲突，是尚未解决的核心问题。

**立体声生成的突破路径**：当前模型几乎无法从文本提示中实现稳定的立体声分离和动态声源空间定位。Veo3 和 Sora2 虽展现出一定的空间化能力，但其训练数据来源和实现机制仍不透明。未来需要探索能够显式建模声场几何的生成架构，以及包含空间标注的训练数据集。

**高阶跨模态耦合的评估指标**：面向复杂场景的多源动态交互和不可见声源的生成，现有的跨模态对齐指标是否足以捕捉这些高阶耦合？例如，一个视频中同时存在多个发声物体时，模型是否正确地将每个声音分配到对应的视觉源，当前的 A-V Align 指标可能无法充分区分。

**领域知识增强的评估可靠性**：能否通过引入音乐理论、声学物理、电影音效设计等专业知识来增强 MLLM 评估的可靠性和可解释性，是一个值得探索的方向。这可能需要构建包含专业标注的校准数据集，或设计基于规则的辅助验证模块。

**长视频与开放式场景的扩展**：将 VABench 的评估框架扩展到分钟级长视频，并覆盖更多开放式场景（如对话、叙事、纪录片风格），将是对其方法论泛化能力的重要检验。

## 原文 PDF

![[paperPDFs/CVPR_2026/VABench_A_Comprehensive_Benchmark_for_Audio_Video_Generation.pdf]]
