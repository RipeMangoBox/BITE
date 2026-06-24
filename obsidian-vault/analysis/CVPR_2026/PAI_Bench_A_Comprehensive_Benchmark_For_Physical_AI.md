---
title: "PAI-Bench: A Comprehensive Benchmark For Physical AI"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PAI_Bench_A_Comprehensive_Benchmark_For_Physical_AI.pdf
project_link: null
code_link: "https://github.com/shi-labs/physical-ai-bench-leaderboard"
huggingface_link: "https://huggingface.co/collections/alibaba-pai/wan22-fun"
aliases:
- PB
- PAI-Bench
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 通过设计一个统一且基于真实世界数据的物理AI评估基准（PAI-Bench），从视频生成质量、控制信号保真度、视频理解三个维度量化模型的物理感知与预测能力，从而暴露现有模型在物理上的不足。
primary_logic: 尽管视频生成模型的视觉保真度不断提升，它们仍然无法遵守基本物理定律或模拟复杂的现实动态；同样，MLLMs在物理推理上落后人类超过30个百分点。提升物理合理性将是实现Physical AI的关键挑战。
claims:
- VGMs achieve quality scores on par with source videos but significantly lower domain scores.
- Multi-signal conditioning yields highest quality score for Cosmos-Transfer models.
- GPT-5 achieves only 61.8% overall accuracy vs human 93.2% on PAI-Bench-U.
- Thinking mode boosts GPT-5 by 8.0 points but degrades Qwen3-VL-32B by 2.2 points.
---

# PAI-Bench: A Comprehensive Benchmark For Physical AI

> [!tip] 核心洞察
> 尽管视频生成模型的视觉保真度不断提升，它们仍然无法遵守基本物理定律或模拟复杂的现实动态；同样，MLLMs在物理推理上落后人类超过30个百分点。提升物理合理性将是实现Physical AI的关键挑战。

| 字段 | 内容 |
|------|------|
| 中文题名 | PAI-Bench：面向物理AI的全面基准测试 |
| 英文题名 | PAI-Bench: A Comprehensive Benchmark For Physical AI |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.01989) · [Code](https://github.com/shi-labs/physical-ai-bench-leaderboard) · [HuggingFace](https://huggingface.co/collections/alibaba-pai/wan22-fun) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | PAI-Bench |
| Dataset | PAI-Bench-G, PAI-Bench-U, PAI-Bench-C |

> [!tip] 效果简介
> - PAI-Bench-G 上，Overall Score Source Videos vs Veo3 (-1.7)；Overall Score Source Videos vs Wan2.2-I2V-A14B (-1.6)。
> - PAI-Bench-U 上，Overall Accuracy Human vs GPT-5 (-31.4)；Overall Accuracy Human vs Qwen3-VL-235B-A22B (-28.5)。
> - PAI-Bench-C 上，Quality Score (All Multi-Signal Condition) Cosmos-Transfer2.5-2B (All) vs Cosmos-Transfer2.5-2B (Blur) (+0.53)。

## 概述

**问题瓶颈**：当前视频生成模型（VGMs）在视觉保真度上已逼近真实视频，但在物理一致性上表现极差；多模态大语言模型（MLLMs）在物理理解与预测任务中准确率远低于人类（GPT-5 仅 61.8% vs. 人类 93.2%），揭示模型缺乏对物理世界动态的深度建模与因果推理能力。

**核心思路**：PAI-Bench 通过构建一个统一且基于真实世界数据的物理 AI 评估基准，从视频生成质量、控制信号保真度和视频理解三个维度，系统量化模型的物理感知与预测能力，从而暴露现有模型在物理合理性上的不足。

**方法定位**：PAI-Bench 是首个专为 Physical AI 领域设计的全面基准（见 Table 1），包含三条评估轨道——PAI-Bench-G（文本条件视频生成）、PAI-Bench-C（条件视频生成）和 PAI-Bench-U（视频理解），覆盖自动驾驶、机器人、工业、人类活动、物理现象和常识推理六大领域（见 Figure 1）。评估体系引入 Domain Score（物理合规性评分）与 Quality Score（视觉质量评分）的双维度指标，并通过竞技场式人类研究验证了自动指标与人类偏好的高度对齐（Pearson r = 0.918）。

**主要结果**：在 PAI-Bench-G 上，领先 VGMs 的 Quality Score 已接近源视频，但 Domain Score 存在显著差距（Veo3 整体分差 -1.7，Wan2.2-I2V-A14B 分差 -1.6）；在 PAI-Bench-U 上，最强 MLLM（GPT-5）仍落后人类超过 30 个百分点；在 PAI-Bench-C 上，多信号联合控制（All）相比单一控制信号可显著提升生成质量（Cosmos-Transfer2.5-2B 质量分提升 +0.53）。消融实验进一步表明，思维链推理模式对 GPT-5 有 +8.0 点的显著增益，但对 Qwen3-VL-32B 反而造成 -2.2 点的退化，且模型性能在 8 帧输入时即饱和。

## 背景与动机

### 物理AI的评估困境

构建能够在真实物理世界中感知、推理和行动的具身智能体，是人工智能迈向通用化的关键一步。这一目标要求模型不仅理解静态的视觉世界，还需掌握物理规律、因果机制与时空动态。然而，当前AI系统在这方面的能力评估严重滞后：现有基准大多聚焦于视频的视觉质量或狭窄的语义理解，缺乏对**物理合理性**的系统性度量。

视频生成模型（VGMs）的进展尤为典型。以Veo3、Wan2.2-I2V-A14B等为代表的SOTA模型，在视觉保真度上已逼近真实视频，但在遵守基本物理定律和模拟复杂现实动态方面表现极差——这一“视觉逼真但物理荒谬”的鸿沟，正是当前Physical AI发展的核心瓶颈。与此同时，多模态大语言模型（MLLMs）在物理常识推理和具身推理任务中，准确率落后人类超过30个百分点，暴露出深层时空推理能力的缺失。

### 现有基准的缺口

现有评估框架存在三个结构性缺陷：

1. **领域覆盖面窄**：VBench、EvalCrafter等视频生成基准主要关注美学质量、运动平滑度等通用指标，几乎不涉及自动驾驶、机器人操作、工业场景等物理AI核心应用领域。Video-MME、MVBench等视频理解基准则以日常活动识别为主，缺乏对物理因果链、力学约束的专门测试。

2. **评估维度割裂**：生成质量评估与物理理解评估长期分离。VGMs的评估只看“画得像不像”，MLLMs的评估只看“答得对不对”，两者从未在一个统一的物理AI框架下被联合审视。

3. **缺乏真实世界锚定**：多数基准使用合成数据或经过人工筛选的短视频片段，无法反映物理世界的复杂性——包括多物体交互、长时序因果依赖、控制信号保真度等关键维度。

### PAI-Bench的动机与设计哲学

针对上述缺口，PAI-Bench提出了一个统一且基于真实世界数据的物理AI评估基准。其核心动机是：**通过多维度、多轨道的系统评估，量化暴露现有模型在物理感知、生成与预测能力上的不足，为Physical AI的研究提供清晰的改进方向**。

PAI-Bench遵循三条设计原则：
- **物理意义优先**：所有评估任务均锚定在自动驾驶、具身操作、工业场景等真实物理AI应用中，而非泛化的视频理解；
- **生成与理解统一**：同时覆盖文本/条件驱动的视频生成（PAI-Bench-G/C）和视频理解（PAI-Bench-U），形成闭环评估；
- **真实数据驱动**：数据集来自AgiBot、OpenDV、Ego-Exo-4D等真实世界视频源，确保评估的生态效度。

PAI-Bench的发布，标志着Physical AI评估从“视觉质量竞赛”转向“物理合理性验证”的范式转变。

## 核心创新

PAI-Bench 的核心创新不在于提出新的模型架构或训练范式，而在于**构建了首个专门面向 Physical AI 的统一评估基准**，通过一套系统化的评估框架，将物理世界理解和生成能力的评测从“视觉质量”这一单一维度中解放出来，直接暴露当前模型在物理一致性上的根本缺陷。

### 创新点一：将“物理合理性”量化为独立评估维度

传统视频生成评估基准（如 VBench、EvalCrafter）主要关注像素级保真度、时序一致性和美学质量，而物理合规性长期处于“靠人眼判断”的灰色地带。PAI-Bench 的核心突破在于**将物理合理性（Domain Score）从视觉质量（Quality Score）中解耦**，使其成为一个可量化、可对比的独立指标。

具体而言，PAI-Bench-G 的 Domain Score 使用 **Qwen3-VL-235B-A22B-Instruct** 作为自动裁判，通过为每个视频设计 5–6 组物理常识问答对（QA pair）来评估模型是否生成符合物理规律的内容。这些 QA 对覆盖常识物理（Common Sense）、自动驾驶（Autonomous Vehicle）、机器人（Robot）、工业（Industry）、人体运动（Human）和物理现象（Physics）六大领域（Figure 2）。模型生成的视频需要经受这些结构化问题的检验，答对比例越高，Domain Score 越高。

这一设计的深层逻辑在于：**视觉质量高不等于物理合理**。实验证据表明，当前最先进的视频生成模型（如 Veo3、Wan2.2-I2V-A14B）的 Quality Score 已接近甚至超越源视频，但 Domain Score 却存在显著差距（Table 3）。这一发现直接印证了核心瓶颈：模型学会了“画得像”，但并未学会“物理世界如何运作”。

### 创新点二：多信号条件生成的控制保真度评估

PAI-Bench-C 是首个系统评估**条件视频生成模型对不同控制信号保真度**的基准。与以往仅关注文本条件的基准不同，PAI-Bench-C 同时考察模糊（Blur）、边缘（Edge）、深度（Depth）和分割（Segmentation）四种控制信号，以及它们的多信号组合（All condition）。

评估指标设计具有明确的因果指向性：
- **Blur SSIM** 衡量模糊信号的结构保真度
- **Edge F1** 捕捉边缘轮廓的对齐精度
- **Depth si-RMSE** 量化深度空间的一致性
- **Mask mIoU** 评估语义分割的准确性

关键发现是：**多信号联合条件（All condition）显著优于任何单一控制信号**。以 Cosmos-Transfer2.5-2B 为例，All condition 的 Quality Score 达到 9.24，比单一 Blur 条件高出 0.53 分（Table 4）。这表明物理世界生成需要多维度的空间约束，单一信号无法充分编码场景的物理结构。

### 创新点三：视频理解中的物理常识与具身推理评测

PAI-Bench-U 的创新在于将视频理解评估从传统的“描述-问答”范式推进到**物理常识推理和具身推理**层面。其任务本体包含两个层次：

1. **物理常识推理**：涵盖空间关系（Space）、时序逻辑（Time）和物理世界规律（Physical World）三个子领域
2. **具身推理**：包括动作效果预测（Predicting Action Effects）和物理约束遵守（Adherence to Physical Constraints）

这一设计的核心洞察是：**当前多模态大语言模型在物理推理上与人类存在巨大鸿沟**。GPT-5 的总体准确率仅为 61.8%，而人类表现为 93.2%，差距超过 30 个百分点（Table 5）。即使是表现最好的 Qwen3-VL-235B-A22B，也落后人类 28.5 个百分点。这说明模型缺乏对物理世界动态的深层因果建模能力，而非简单的感知不足。

### 创新点四：评估指标的人类对齐验证

PAI-Bench 的另一关键创新是**通过竞技场式人类研究验证自动指标的可靠性**。研究者组织参与者对生成视频进行成对比较，分别从视频质量和物理合理性两个维度打分，并计算 ELO 分数。自动指标得分与人类 ELO 分数的 Pearson 相关系数达到 **r = 0.918**（Figure 6），证明了 Domain Score 和 Quality Score 的评估有效性。

这一验证步骤至关重要：它确保了自动评估框架不是“自说自话”，而是真正反映了人类对物理合理性的判断标准。

### 与现有基准的本质差异

Table 1 的对比清晰展示了 PAI-Bench 的差异化定位：现有基准要么只关注视频质量（如 VBench），要么只关注视频理解（如 Video-MME），要么覆盖的物理场景极为有限。**PAI-Bench 是首个将视频生成质量、条件控制保真度和物理理解推理统一在 Physical AI 框架下的基准**，覆盖自动驾驶、工业、具身智能、自我中心视角等实际应用场景。

### 边界与局限

尽管 PAI-Bench 在评估维度上实现了突破，其自动评估仍依赖 MLLM 作为裁判，而 MLLM 本身在时序动态理解上存在固有局限。此外，当前基准未覆盖交互式行为评估，无法衡量模型在闭环决策中的物理推理能力。这些限制指向了未来工作的方向：**将评估信号转化为训练信号，直接指导模型提升物理合理性**。

## 整体框架

PAI‑Bench 围绕一个核心诊断命题展开：**当前视频生成模型（VGM）与多模态大语言模型（MLLM）在视觉保真度上已逼近真实视频，但在物理一致性、因果推理与动态建模上存在系统性缺陷**。为量化这一瓶颈，PAI‑Bench 设计为三条独立但互补的评估轨道，分别从**生成质量、控制保真度、视频理解**三个维度对物理 AI 能力进行细粒度解构。

### 三轨道架构与模块关系

**PAI‑Bench‑G（文本条件生成评估）** 接收文本提示与参考源视频，输出两个核心指标：
- **Quality Score**：由八项子指标组成，分为“通用生成质量”（主体一致性、背景一致性、运动平滑度、美学质量等）和“参考保真度”（基于 DINO、CLIP、LAION 美学预测器、MUSIQ 等模型），评估视觉连贯性与真实感。
- **Domain Score**：以 **Qwen3‑VL‑235B‑A22B‑Instruct** 作为自动裁判，通过视频‑问答对（平均每视频 5‑6 组 QA）对生成视频在六个物理领域（常识、自动驾驶、机器人、工业、人体、物理）的合规性进行评分。

**PAI‑Bench‑C（条件生成评估）** 输入控制信号（模糊、边缘、深度、分割掩码）与对应源视频，评估生成视频在控制保真度、视觉质量与多样性上的表现。保真度指标针对不同模态分别设计：模糊信号使用 SSIM，边缘使用 F1，深度使用尺度不变 RMSE，分割掩码使用 mIoU。

**PAI‑Bench‑U（视频理解评估）** 输入视频片段与对应问题，评估 MLLM 在两个认知层次上的表现：
- **物理常识推理**：覆盖空间、时间、物理世界三个子域。
- **具身推理**：包括动作效果预测与物理约束遵守两个子任务。

三条轨道共享统一的设计原则：**所有评估均锚定在真实世界数据与物理意义上明确的任务上**，从而避免纯语言先验或视觉表面线索对评估的污染。

### 输入输出流与评估闭环

整体流程可概括为：
1. **数据准备**：从真实世界视频源（如 AgiBot、OpenDV、Ego‑Exo‑4D 等）采集并标注，生成文本提示、控制信号、问答对。
2. **模型推理**：待评估模型（VGM 或 MLLM）根据输入条件生成视频或回答问题。
3. **自动指标计算**：各轨道使用专用指标模块计算得分，其中 Domain Score 和部分 Quality Score 依赖 MLLM 裁判。
4. **人类对齐验证**：通过竞技场式人类研究（pairwise comparison + ELO 评分）验证自动指标与人类偏好的对齐程度——在 PAI‑Bench‑G 上，自动指标 ELO 与人类 ELO 的 Pearson 相关系数达到 **r = 0.918**，为自动评估提供了可靠性锚点。

这种“自动指标 + 人类锚定”的双层设计，使得 PAI‑Bench 既能在大规模模型评估中保持效率，又能确保评估结果与人类对物理合理性的判断高度一致。

### 补充图表

![[assets/figures/papers/paper_list_l2049_https_arxiv_org_abs_2512_01989/figures/001_Figure_1.jpg]]
*Figure 1: | Overview of PAI-Bench framework. PAI-Bench is a comprehensive bench designed for diverse topics in Physical AI, including evaluation for text and condition to physical World Generation, and physical world understanding*

![[assets/figures/papers/paper_list_l2049_https_arxiv_org_abs_2512_01989/figures/002_Table_1.jpg]]
*Table 1: | Comparison with existing benchmarks. Our PAI-Bench is designed with comprehensive domains in Physical AI. Specifically, we focus on scenarios involving practical applications, such as autonomous vehicles (AV), industry, embodied AI, and ego-centric views*

![[assets/figures/papers/paper_list_l2049_https_arxiv_org_abs_2512_01989/figures/004_Figure_3.jpg]]
*Figure 3: | Examples of PAI-Bench. PAI-Bench focuses on Physical AI application scenarios across six domains, where only the first frame of each video is shown for brevity. For PAI-Bench-C, we present the blurred, edge, segmentation, and depth videos that serve as control signals. For PAI-Bench-U, we show the questions used for video understanding. For PAI-Bench-G, we show the input captions used for generation and a derived prompt used for Domain Score evaluation*

## 核心模块与公式推导

### 评估框架的三轨架构

PAI-Bench 围绕物理 AI 的核心能力缺口，构建了三个独立的评估轨道，每个轨道针对不同的模型能力维度：

- **PAI-Bench-G（文本条件生成）**：评估文本到视频生成模型在视觉质量与物理合理性两个轴上的表现。其核心创新在于将评估分解为 **Quality Score**（视觉保真度与连贯性）和 **Domain Score**（物理合规性）两个独立指标，而非传统基准中将其混为一谈。
- **PAI-Bench-C（条件生成）**：评估条件视频生成模型对多种控制信号（模糊、边缘、深度、分割）的保真度、生成质量与多样性。该轨道揭示了不同控制信号类型对生成效果的因果影响。
- **PAI-Bench-U（视频理解）**：评估多模态大语言模型在物理常识推理（空间、时间、物理世界）和具身推理（动作效果预测、物理约束遵守）方面的能力，直接暴露 MLLMs 与人类在物理推理上的巨大差距。

三条轨道共享统一的设计原则：将评估锚定在具有物理意义的任务和真实世界数据上，而非依赖合成场景或语言捷径。

### PAI-Bench-G 的八项质量指标

Quality Score 由八个指标组成，分为两组：

**通用生成质量组**（评估视频的内在视觉属性）：

- **Subject Consistency**（主体一致性）：使用 DINO 特征衡量视频帧间主体身份的稳定性。对于长度为 $T$ 的视频，第 $t$ 帧的 DINO 特征记为 $d_t$，则：

$$S_{\mathrm{sub}} = \frac{1}{T-1} \sum_{t=2}^{T} \frac{1}{2} (\langle d_1, d_t \rangle + \langle d_{t-1}, d_t \rangle)$$

该公式计算每帧与首帧及前一帧的余弦相似度的平均值，捕捉主体在时序上的身份保持程度。

- **Background Consistency**（背景一致性）：使用 CLIP 特征 $c_t$ 评估背景时序稳定性：

$$S_{\mathrm{background}} = \frac{1}{T-1} \sum_{t=2}^{T} \frac{1}{2} (\langle c_1, c_t \rangle + \langle c_{t-1}, c_t \rangle)$$

- **Motion Smoothness**（运动平滑度）：通过子采样视频帧、插值重建并计算逐像素 MAE 来量化运动连贯性。设原始帧为 $f_t$，子采样后插值重建的帧为 $\hat{f}_t$：

$$S_{\mathrm{smoothness}} = \frac{1}{T/2} \sum_{t=1}^{T/2} \lVert f_{2t-1} - \hat{f}_{2t-1} \rVert_1$$

该值经归一化至 $[0,1]$ 区间，越低表示运动越平滑。

- **Aesthetic Quality**：使用 LAION 美学预测器（LAION-AI, 2022）评估帧级美学分数。
- **Imaging Quality**：采用 MUSIQ 评估单帧成像质量（噪声、模糊、压缩伪影等）。

**参考保真度组**（评估生成视频与源视频的相似度）：

- **ViCLIP 整体一致性**：使用 ViCLIP 视频-文本基础模型评估生成视频与文本提示的语义对齐。
- **DINO 帧相似度**：衡量生成帧与源帧在 DINO 特征空间的相似度。
- **CLIP 帧相似度**：衡量生成帧与源帧在 CLIP 特征空间的相似度。

对于图像到视频（I2V）任务，Subject Consistency 公式调整为以输入图像特征 $s_{\mathrm{img}}$ 替代首帧特征：

$$S_{\mathrm{i2v\_subject}} = \frac{1}{T-1} \sum_{t=2}^{T} \frac{1}{2} (\langle s_{\mathrm{img}}, s_t \rangle + \langle s_{t-1}, s_t \rangle)$$

### Domain Score 评估器

Domain Score 是 PAI-Bench 区别于现有基准的关键创新。它使用 **Qwen3-VL-235B-A22B-Instruct** 作为自动裁判，通过为每个视频设计的 QA 对（平均 5-6 对/视频，共 5,636 对）来评估生成视频的物理合规性。裁判模型需要回答诸如“物体是否遵循重力方向？”“车辆是否保持在车道内？”等问题，其准确率直接映射为 Domain Score。这一设计将物理合理性从主观判断转化为可量化的问答任务。

### PAI-Bench-C 的控制保真度指标

PAI-Bench-C 针对四种控制信号类型设计了专门的保真度指标：

- **Blur SSIM**：对模糊控制信号，计算生成视频与目标视频在像素空间的 SSIM。
- **Edge F1**：对边缘控制信号，提取边缘图后计算 F1 分数，评估边缘结构的保持度。
- **Depth si-RMSE**：对深度控制信号，计算尺度不变均方根误差（scale-invariant RMSE）。
- **Mask mIoU**：对分割控制信号，计算分割掩码的平均交并比。

此外，多样性指标通过以下公式计算：在相同控制信号 $c$ 下生成 $K$ 个样本 $\hat{X}^{(i)}$，计算成对 LPIPS 距离的平均值：

$$Div_c \gets \frac{2}{K(K-1)} \sum_{i<j} LPIPS(\hat{X}^{(i)}, \hat{X}^{(j)})$$

该值越高表示模型在给定控制约束下的生成多样性越强。

### 人类偏好对齐验证

为验证自动指标的可靠性，PAI-Bench 进行了竞技场式人类研究：参与者对视频对进行质量和物理合理性两个维度的偏好判断，据此计算 ELO 分数。自动指标与人类 ELO 评分的 **Pearson 相关系数达到 0.918**（Figure 6），表明所提指标与人类判断高度一致，为大规模自动化评估提供了可信基础。

### 补充图表

![[assets/figures/papers/paper_list_l2049_https_arxiv_org_abs_2512_01989/figures/003_Figure_2.jpg]]
*Figure 2: | Distribution of videos and QA pairs in PAI-Bench-G. These pairs facilitate Domain Score evaluation with an average density of 5-6 QA pairs per video*

## 实验与分析

### 4.1 指标可靠性验证

为确保自动评估指标与人类偏好一致，作者针对 PAI-Bench-G 进行了竞技场式人类研究。参与者对生成视频进行成对比较，分别从视频质量（对应 Quality Score）和物理合理性（对应 Domain Score）两个维度做出判断，据此计算 ELO 评分。**Figure 6** 展示了自动指标综合得分与人类 ELO 评分之间的 Pearson 相关性分析：相关系数达到 **r = 0.918**，红色阴影区域表示 0.95 置信区间。这一强相关性验证了所提评估框架的有效性，表明自动指标能够可靠地替代人类评估。

![[assets/figures/papers/paper_list_l2049_https_arxiv_org_abs_2512_01989/figures/009_Figure_6.jpg]]
*Figure 6: | Pearson correlation analysis on PAI-Bench-G. The red shaded regions indicate the 0.95 confidence intervals*

### 4.2 PAI-Bench-G：文本条件视频生成评估

**Table 3** 报告了 15 个视频生成模型（VGM）在 PAI-Bench-G 上的完整评估结果。核心发现如下：

**视觉质量与物理合理性严重脱节。** 大多数领先的 VGM 在 Quality Score 上与源视频（Source Videos, Overall 83.9）高度接近，例如 **Veo3** 达到 Overall 82.2（差距仅 -1.7），**Wan2.2-I2V-A14B** 达到 Overall 82.3（差距 -1.6）。然而，在 Domain Score 上，所有模型与源视频之间存在显著鸿沟——源视频的 Domain Score 天然代表物理世界真实分布，而生成模型在这一维度上表现极差。这揭示了一个关键瓶颈：当前 VGM 虽然能够生成高保真视觉内容，但缺乏对基本物理定律的遵守和对复杂现实动态的建模能力。

**Domain Score 的细粒度分析**（涵盖 Common Sense、Autonomous Vehicle、Robot、Industry、Human、Physics 六个子领域）显示，模型在不同物理场景下的表现差异明显，但整体均远低于真实视频水平。Quality Score 的八个子指标（Subject Consistency、Background Consistency、Motion Smoothness、Dynamic Degree、Aesthetic Quality、Imaging Quality、Temporal Consistency、Overall Video-Text Alignment）则显示模型在主体一致性、背景稳定性和运动平滑度等方面已接近真实视频。

### 4.3 PAI-Bench-C：条件视频生成评估

**Table 4** 展示了 4 个条件 VGM 在 PAI-Bench-C 上的评估结果，涵盖五种控制信号设置：Blur、Edge、Depth、Mask 以及 All（多信号组合）。主要结论：

**多信号条件显著提升生成质量。** 以 **Cosmos-Transfer2.5-2B** 为例，All 条件下的 Quality Score 达到 9.24，相比单一 Blur 条件（8.71）提升 **+0.53**，显著优于任何单一控制信号。这一趋势在 Cosmos-Transfer 系列模型中一致成立，表明多模态控制信号的融合为模型提供了更丰富的物理场景约束，从而提升了生成视频的整体质量。

**控制保真度指标**（Blur SSIM、Edge F1、Depth si-RMSE、Mask mIoU）揭示了不同控制信号下模型的对齐能力差异。各模型在 Blur 和 Edge 条件下的保真度普遍较高，而在 Depth 和 Mask 条件下的空间对齐精度仍有较大提升空间。Diversity Score（基于成对 LPIPS 距离）则显示多信号条件并未牺牲生成多样性。

### 4.4 PAI-Bench-U：视频理解评估

**Table 5** 报告了 16 个多模态大语言模型（MLLM）在 PAI-Bench-U 上的评估结果，涵盖物理常识推理（Space、Time、Physical World）和具身推理（Predicting Action Effects、Adherence to Physical Constraints）两大维度，以及 BridgeData、RoboVQA、RoboFail、Agibot、HoloAssist、Autonomous Vehicle 六个具身子领域。

**MLLM 与人类存在巨大差距。** 人类总体准确率达到 **93.2%**，而表现最好的 MLLM——**GPT-5**——仅达到 **61.8%**（差距 **-31.4 个百分点**）。排名第二的 **Qwen3-VL-235B-A22B** 为 64.7%（差距 -28.5 个百分点）。这一超过 30 个百分点的差距表明，即使是最先进的多模态模型，在物理世界的时空推理和因果理解方面仍远未达到人类水平。

**物理常识推理是普遍短板。** 在 Space、Time 和 Physical World 三个子领域中，所有模型的准确率均显著低于人类，尤其在需要精细时序推理的 Time 维度上表现最弱。具身推理任务中，Predicting Action Effects 的准确率普遍高于 Adherence to Physical Constraints，说明模型在预测动作结果方面相对擅长，但在判断行为是否符合物理约束时更为困难。

### 4.5 消融实验

**Thinking Mode 的影响。** **Table 6** 展示了思维链推理模式对不同 MLLM 性能的消融结果。关键发现呈现两极分化：**GPT-5** 在开启 Thinking Mode 后 Overall Accuracy 提升 **+8.0 个百分点**，表明显式推理过程显著增强了其物理理解能力。然而，**Qwen3-VL-30B-A3B** 在相同设置下性能下降 **-2.2 个百分点**，说明思维链推理并非对所有模型架构都有效，可能引入推理偏差或过度思考导致错误累积。

**输入帧数的影响。** **Figure 7** 和 **Figure 9** 分析了不同输入帧数对 PAI-Bench-U 性能的影响。实验表明，模型性能在 **8 帧**时趋于饱和，继续增加帧数并未带来准确率的进一步提升。更重要的是，**零帧（纯文本）条件下模型性能降至随机猜测水平**，这验证了 PAI-Bench-U 的设计成功消除了语言先验的干扰——模型必须依赖视频中的视觉时序信息才能正确回答物理推理问题，而非利用文本中的统计相关性进行猜测。

### 4.6 失败模式分析

综合三个轨道的实验结果，当前模型在 Physical AI 评估中暴露出以下系统性失败模式：

1. **物理合理性崩溃**：VGMs 虽然在像素级视觉质量上接近真实视频，但在 Domain Score 上表现极差，生成的视频常违反基本物理定律（如物体穿模、不合理的运动轨迹、重力方向错误等）。这源于模型在训练过程中缺乏对物理因果关系的显式建模。

2. **保守生成策略**：部分 VGMs 倾向于生成静态或低动态复杂度的视频以保证视觉保真度，导致 Motion Smoothness 和 Dynamic Degree 指标得分偏低。模型优先保证主体一致性和背景稳定性，牺牲了运动的自然性和多样性。

3. **时空推理盲区**：MLLMs 在需要精细时序理解的物理常识推理任务中表现最差，尤其在 Time 维度上准确率远低于 Space 维度。模型难以捕捉视频中事件的时间顺序、速度变化和因果链条。

4. **物理约束判断薄弱**：在具身推理的 Adherence to Physical Constraints 子任务中，模型经常无法识别违反物理规律的行为（如不稳定的堆叠、不可能的力交互），说明模型缺乏对物理世界基本约束的内化表征。

5. **推理模式的不确定性**：Thinking Mode 对不同模型的影响方向相反，表明当前 MLLM 的推理能力高度依赖架构和训练策略，尚未形成稳定可靠的物理推理机制。

### 补充图表

![[assets/figures/papers/paper_list_l2049_https_arxiv_org_abs_2512_01989/figures/008_Table_3.jpg]]
*Table 3: | Evaluation results of 15 VGMs on PAI-Bench-G. Metrics in Domain Score: Common Sense (CS), Autonomous Vehicle (AV), Robot (RO), Industry (IN), Human (HU), Physics (PH); and Quality Score: Subject Consistency (SC), Background Consistency (BC), Motion Smoothness (MS), Aesthetic Quality (AQ), Imaging Quality (IQ), Overall Consistency (OC), I2V Subject (IS), I2V Background (IB). Blue means the best across open-source models*

![[assets/figures/papers/paper_list_l2049_https_arxiv_org_abs_2512_01989/figures/010_Table_4.jpg]]
*Table 4: | Evaluation results of 4 conditional VGMs on PAI-Bench-C. For each model, the control signal settings consist of either a single video or a combination of multiple signal videos. Green means the best across control signal settings for each model*

![[assets/figures/papers/paper_list_l2049_https_arxiv_org_abs_2512_01989/figures/011_Table_5.jpg]]
*Table 5: | Evaluation of 16 MLLMs on PAI-Bench-U. Embodied reasoning domains: BridgeData (BD), RoboVQA (RV), RoboFail (RF), Agibot (AB), HoloAssist (HA), Autonomous Vehicle (AV). Red denotes the best result across either proprietary or open-source models*

![[assets/figures/papers/paper_list_l2049_https_arxiv_org_abs_2512_01989/figures/012_Figure_7.jpg]]
*Figure 7: | Performance comparison across different frame counts on PAI-Bench-U*

![[assets/figures/papers/paper_list_l2049_https_arxiv_org_abs_2512_01989/figures/013_Table_6.jpg]]
*Table 6: | Ablation study on thinking mode across different MLLMs on PAI-Bench-U. Performance gains and degradations are highlighted*

![[assets/figures/papers/paper_list_l2049_https_arxiv_org_abs_2512_01989/figures/017_Figure_9.jpg]]
*Figure 9: | Accuracy versus number of input frames on PAI-Bench-U. The input frames are uniformly sampled from the video. The dashed horizontal lines denote the random-guess baselines*

![[assets/figures/papers/paper_list_l2049_https_arxiv_org_abs_2512_01989/figures/041_Figure_22.jpg]]
*Figure 22: | Radar chart visualizations of model capabilities across PAI-Bench tracks*

## 方法谱系与知识库定位

### 1. 与现有基准的关系

PAI-Bench 的定位是**首个专门面向 Physical AI 领域的全面基准**（见 Table 1 对比）。现有视频生成评估基准主要聚焦于通用视觉质量或文本-视频对齐，而 PAI-Bench 将评估维度系统性地扩展到物理合规性、控制信号保真度和具身推理。

**与视频生成基准的差异**：传统基准（如 VBench、EvalCrafter）侧重美学质量、运动平滑度等通用指标，但未显式建模物理约束。PAI-Bench-G 引入 **Domain Score**，通过 MLLM 裁判（Qwen3-VL-235B-A22B-Instruct）对生成视频进行物理合规性 QA 评分，将评估从“是否好看”推进到“是否物理合理”。这一设计直接暴露了当前 SOTA VGMs 的核心瓶颈：**视觉质量已接近源视频（Quality Score 差距仅约 1.6-1.7 分），但 Domain Score 存在显著差距**（Table 3）。

**与视频理解基准的差异**：现有 MLLM 基准（如 Video-MME、MVBench）评估通用视频理解，而 PAI-Bench-U 聚焦物理常识推理和具身推理两个子领域。其关键设计创新在于：通过控制输入帧数消融实验（Figure 7），证实零帧（纯文本）条件下模型性能降至随机猜测水平，从而**有效中和了语言先验的干扰**，确保评估的是真正的视觉-物理推理能力。

### 2. 方法适用边界

**评估范式的覆盖范围**：PAI-Bench 三轨设计覆盖了 Physical AI 的生成、条件生成和理解三个核心维度，但其评估边界存在以下限制：

- **静态评估为主**：PAI-Bench-G/C 评估的是开环生成质量，未涉及闭环交互式行为评估。这意味着基准无法衡量模型在动态反馈环境中的决策能力——这是 Physical AI 走向实际部署的关键缺口。
- **领域覆盖有限**：当前六个领域（常识、自动驾驶、机器人、工业、人体、物理）虽具代表性，但论文明确承认“基准覆盖领域仍有限，未来可扩展更多 Physical AI 子场景”，例如流体模拟、柔性物体操作等复杂物理交互场景。
- **控制信号类型固定**：PAI-Bench-C 仅支持四种控制信号（模糊、边缘、深度、分割），对更复杂的控制模态（如 3D 关键点、光流、文本驱动的运动描述）未提供评估支持。

**评估指标的鲁棒性边界**：Domain Score 依赖 MLLM 裁判，其可靠性受限于裁判模型本身的物理推理能力。论文坦承“尽管采用先进 MLLM 作为自动评委评估高层语义，自动评估仍处于发展阶段，尤其在解释视频中的时序动态方面存在固有限制”。此外，整体一致性指标依赖 ViCLIP 等视频-文本基础模型，在处理长文本和复杂指令时存在鲁棒性不足的问题。

### 3. 关键局限与失败模式

**生成模型的“安全保守”策略**：论文观察到“部分视频生成模型采取保守策略，优先保证静态保真度而牺牲动态复杂性，导致运动生成缺乏风险尝试”。这意味着当前 VGMs 在 PAI-Bench-G 上的 Domain Score 低分可能部分源于模型倾向于生成静态或低动态场景以规避物理违规，而非真正缺乏物理建模能力——这是基准设计本身难以区分的混淆因素。

**MLLM 的时空推理鸿沟**：PAI-Bench-U 揭示的最显著失败模式是 MLLMs 与人类之间的巨大差距——GPT-5 总体准确率仅 61.8%，而人类达 93.2%（Table 5），差距超过 31 个百分点。更值得注意的是，Thinking mode 消融实验（Table 6）显示推理模式对不同模型的影响方向相反：GPT-5 提升 8.0 分，而 Qwen3-VL-32B 反而下降 2.2 分，说明当前推理增强技术缺乏跨模型的一致性收益，其有效性高度依赖基座模型的架构特性。

**帧数饱和现象**：PAI-Bench-U 的性能在 8 帧输入时即达到饱和（Figure 7, Figure 9），继续增加帧数不再提升准确率。这表明当前 MLLMs 无法有效利用长时序信息进行物理推理，存在时序建模能力的天花板。

### 4. 开放问题与未来方向

论文明确提出的开放问题包括：

1. **更鲁棒的自动化物理评价指标**：如何设计不依赖 MLLM 裁判、能够直接捕获物理合理性（如运动学约束、动量守恒等）的评价指标？
2. **动态运动与视觉质量的平衡**：如何设计训练信号或生成策略，鼓励 VGMs 在保证视觉质量的前提下进行更具冒险性的动态运动生成？
3. **MLLM 时空推理能力提升**：如何通过架构改进或训练数据设计，缩小 MLLMs 在物理推理上与人类 30+ 百分点的差距？
4. **评估到训练的闭环**：能否将 PAI-Bench 的评估信号转化为物理世界学习信号，直接指导模型训练？这将是 Physical AI 从“评估诊断”走向“能力提升”的关键一步。
5. **交互式行为评估**：当前基准未覆盖闭环决策能力评估，如何设计能够评估 Physical AI 在动态环境中交互式行为质量的基准？

### 5. 知识库定位

PAI-Bench 在 Physical AI 研究生态中扮演**诊断工具**的角色：它不提出新的生成或理解模型，而是通过统一、可复现的评估框架，系统性地暴露当前 SOTA 模型在物理一致性上的集体短板。其核心贡献在于将 Physical AI 的评估从定性讨论推进到定量测量，为后续研究提供了可操作的改进方向——提升 Domain Score 和缩小 MLLM 与人类的物理推理差距将成为该领域的核心攻关目标。

## 原文 PDF

![[paperPDFs/CVPR_2026/PAI_Bench_A_Comprehensive_Benchmark_For_Physical_AI.pdf]]
