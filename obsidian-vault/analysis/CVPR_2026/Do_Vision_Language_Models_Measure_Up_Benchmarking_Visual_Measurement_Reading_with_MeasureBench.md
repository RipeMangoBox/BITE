---
title: Do Vision-Language Models Measure Up? Benchmarking Visual Measurement Reading with MeasureBench
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Do_Vision_Language_Models_Measure_Up_Benchmarking_Visual_Measurement_Reading_with_MeasureBench.pdf
project_link: "https://flageval-baai.github.io/MeasureBenchPage/"
code_link: null
aliases:
- DVLMMUBVMRM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 精准的指针/指示器定位和刻度数值映射能力
primary_logic: 视觉测量读数任务的核心挑战在于需要从仪器图像中精确提取空间信息（指针角度、刻度对应关系），这一过程要求高度精细的视觉感知和轻量算术，而当前前沿VLM的失败主要源于微小的感知错误（如错位一个刻度），而非高层次推理或知识匮乏。
claims:
- 单位识别准确率普遍超过90%，但值准确率极低（如Gemini 2.5 Pro：单位96.2% vs值30.7%），证明瓶颈在数值读取而非文本理解。
- 启用inference-time思考对性能提升甚微，有时甚至会降低表现，说明文本推理不能弥补感知缺陷。
- 提供逐步阅读指导或特定提示对性能提升有限，证明模型缺少的不是如何读的知识，而是视觉精度。
- 案例分析表明多数错误源于指针定位的微小偏差（如一个刻度的左右偏移），而非大范围理解失败。
---

# Do Vision-Language Models Measure Up? Benchmarking Visual Measurement Reading with MeasureBench

> [!tip] 核心洞察
> 视觉测量读数任务的核心挑战在于需要从仪器图像中精确提取空间信息（指针角度、刻度对应关系），这一过程要求高度精细的视觉感知和轻量算术，而当前前沿VLM的失败主要源于微小的感知错误（如错位一个刻度），而非高层次推理或知识匮乏。

| 字段 | 内容 |
|------|------|
| 中文题名 | 视觉语言模型能胜任测量读数吗？基于MeasureBench的基准测试 |
| 英文题名 | Do Vision-Language Models Measure Up? Benchmarking Visual Measurement Reading with MeasureBench |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.26865) · [Project](https://flageval-baai.github.io/MeasureBenchPage/) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | 基于合成数据的GRPO强化微调方法 |
| Dataset | MeasureBench |

> [!tip] 效果简介
> - MeasureBench (真实图像子集) 上，整体准确率 (Overall Acc.) Gemini-2.5-Pro: 30.2% vs Qwen2.5-VL-7B: 14.6% (多种模型差距明显)；经过GRPO微调后的整体准确率 (Qwen2.5-VL-7B) 19.7% (+34.9%) vs 未微调: 14.6% (提升5.1个百分点)。
> - MeasureBench (合成图像子集) 上，整体准确率 (Overall Acc.) Gemini-2.5-Pro: 26.3% vs Qwen2.5-VL-7B: 10.9% (合成图像仍更具挑战性)；经过GRPO微调后的整体准确率 (Qwen2.5-VL-7B) 35.2% (+222.9%) vs 未微调: 10.9% (大幅提升)。

## 概述

视觉测量读数——从仪表、量具等仪器图像中精确提取数值与单位——是工业巡检、实验室记录和日常场景中的基础感知任务。尽管当前视觉语言模型（VLM）在诸多视觉理解基准上表现亮眼，但它们在需要细粒度空间定位和精确数值映射的测量读数任务上是否同样可靠，仍是一个悬而未决的问题。为此，本文构建了 **MeasureBench**，一个包含 2,442 个图像-问题对的专用基准，系统评估前沿 VLM 的测量读数能力。

核心发现具有明确的诊断性：**瓶颈不在“理解”，而在“看见”**。所有模型在单位识别上的准确率普遍超过 90%（如 Gemini 2.5 Pro 达 96.2%），但数值读取准确率极低（同模型仅 30.7%），表明模型知道该读什么单位，却无法精确定位指针或辨别刻度。启用推理时思考（inference-time thinking）对性能提升甚微，有时甚至造成退化；提供详细的读表操作指南也收效有限。案例分析进一步揭示，大多数错误源于微小的感知偏差——例如指针错位一个刻度——而非高层次推理失败或任务知识缺失。

在方法层面，本文提出了一个**混合合成数据框架**，通过 2D 程序化渲染和 3D 物理渲染（Blender）生成多样化、标签精确的测量仪器图像，并以此为基础，采用 **GRPO（Group Relative Policy Optimization）强化微调**方法，在合成数据上对 Qwen2.5-VL 系列模型进行训练。该方法使用规则奖励函数（$R_{\mathrm{eval}} = \alpha c_{\mathrm{all}} + (1 - \alpha) c_{\mathrm{fmt}}$，$\alpha=0.9$），兼顾读数正确性与输出格式规范性。主要实验结果如下：

- **最强闭源模型 Gemini 2.5 Pro** 在真实图像子集上整体准确率仅 **30.2%**，合成子集上仅 **26.3%**。
- **GRPO 微调** 使 Qwen2.5-VL-7B 在真实图像上从 14.6% 提升至 **19.7%**（+34.9%），在合成图像上从 10.9% 大幅提升至 **35.2%**（+222.9%）。
- 消融实验证实：监督微调（SFT）会过拟合合成数据、损害真实图像性能，而 GRPO 对两者均有提升；早期专用指针检测系统在 MeasureBench 上的泛化能力远逊于通用 VLM。

综上，MeasureBench 揭示了一个关键洞察：当前 VLM 的视觉测量读数能力受限于**几何精度的系统性缺陷**，而非语义理解不足。合成数据驱动的强化微调虽能带来显著改善，但合成到真实的域差仍未消除，复合仪表等极端精细的感知场景仍是开放挑战。

## 背景与动机

视觉测量读数——从温度计、压力表、电表等仪器图像中自动提取数值和单位——是工业巡检、实验室记录和日常场景中广泛存在的基础视觉任务。与自然图像理解不同，该任务要求模型同时具备精细的空间感知能力（如指针角度定位、刻度线对应关系辨识）和轻量数值映射能力，将连续的几何信号转化为离散的读数输出。

近年来，视觉语言模型（VLMs）在通用视觉问答、文档理解等任务上取得了显著进展，展现出强大的图像理解和文本生成能力。然而，这些模型在需要精确几何感知的细粒度视觉任务上的表现尚不明确。一个核心问题是：**当前前沿VLM的失败究竟源于对测量任务的语义理解不足，还是源于视觉感知精度的系统性缺陷？**

本文通过构建MeasureBench基准测试，系统性地揭示了这一瓶颈。关键证据表明：

- **单位识别准确率普遍超过90%，但数值准确率极低**。以表现最好的Gemini 2.5 Pro为例，其在真实图像上的单位准确率达96.2%，而整体读数准确率仅为30.7%。这证明模型完全理解任务语义和单位概念，瓶颈在于数值读取的视觉精度。
- **推理时思考（inference-time thinking）几乎无效**。启用链式思考对性能提升甚微，有时甚至降低表现，说明文本推理无法弥补感知缺陷。
- **提供详细操作指导收益有限**。即使明确告知模型如何读取特定仪器，真实图像上的性能增益也极为有限（如Gemini 2.5 Pro仅从30.2%提升至31.8%），证明模型缺少的不是“如何读”的知识，而是精准定位指针和刻度的视觉能力。
- **案例分析揭示微小感知错误主导失败**。多数错误源于指针定位的微小偏差（如错位一个刻度导致读数从4.4 A变为4.5 A），而非大范围的理解失败。

上述发现表明，视觉测量读数任务构成了一个独特的“感知探针”：它剥离了高层语义推理的干扰，直接暴露VLM在精细空间感知上的能力边界。这一定位使得MeasureBench不仅是一个领域基准，更成为诊断VLM视觉编码质量的有效工具。

为应对这一挑战，本文进一步探索了基于合成数据的强化微调（GRPO）方法，通过在3,900张程序化生成的合成仪器图像上训练，使Qwen2.5-VL-7B在真实图像子集上的准确率从14.6%提升至19.7%（+34.9%），在合成子集上从10.9%大幅提升至35.2%（+222.9%）。然而，合成到真实的泛化差距仍未完全消除，复合仪表（如多表盘电表）几乎全军覆没，表明极精细几何推理仍是VLM面临的核心障碍。

## 核心创新

### 1. 问题定位：从“知识瓶颈”到“感知瓶颈”

现有视觉语言模型（VLM）在通用视觉问答上表现强劲，但本文揭示了一个被忽视的系统性缺陷：**细粒度视觉感知能力严重不足**。决定性证据来自MeasureBench的评估结果——各模型单位识别准确率普遍超过90%，但数值读取准确率极低（如Gemini 2.5 Pro：单位96.2% vs 数值30.7%），证明瓶颈不在于“不知道读什么单位”，而在于“读不准指针指向哪个刻度”。进一步地，启用推理时思考（inference-time thinking）对性能提升甚微甚至有害，提供逐步阅读指导也只能带来极其有限的增益（Table 4），说明文本推理无法弥补几何感知精度的缺失。案例分析表明，多数错误源于指针定位的微小偏差（如错位一个刻度），而非高层次理解失败。

### 2. 核心因果机制：指针定位与刻度映射

测量读数任务的核心挑战在于从仪器图像中精确提取空间信息——指针角度、刻度对应关系——并完成轻量算术映射。这一过程的因果旋钮（causal knob）是**精准的指针/指示器定位和刻度数值映射能力**。当前VLM的失败模式并非缺乏任务知识，而是视觉编码器在前向传播中丢失了关键的细粒度空间信号，导致后续语言解码器即使“知道”读数规则，也无法基于错误的视觉特征得出正确答案。

### 3. 方法创新：changed slots 对比

本文提出的方法并非全新架构，而是通过**合成数据驱动的GRPO强化微调**，在现有VLM基础上针对上述感知瓶颈进行靶向增强。与基线模型**Qwen2.5-VL-7B**（Bai et al., 2025）相比，核心变更体现在以下三个维度：

| 变更维度 | 基线方法 | 本文方法 | 设计意图 |
|---------|---------|---------|---------|
| **训练数据** | 通用图文预训练数据 | 3,900张合成测量仪器图像（39种外观 × 100样本） | 提供密集的细粒度几何-数值映射监督信号 |
| **训练目标** | 语言建模损失 | GRPO算法 + 规则奖励（$R_{\mathrm{eval}} = \alpha c_{\mathrm{all}} + (1-\alpha) c_{\mathrm{fmt}}$，$\alpha=0.9$） | 直接优化读数正确性，而非语言似然 |
| **输出格式** | 自由文本回答 | 要求模型在`<think>`标签内输出推理过程，随后给出最终答案 | 强制模型显式化感知-推理链路，便于奖励信号传导 |

其中，奖励函数设计是方法的关键创新点：

- **$c_{\mathrm{all}} = \mathbb{I} \{ \hat{y} \in I \wedge \hat{u} = u \}$**：数值落在真实区间内且单位正确的布尔指标，直接对应任务目标。
- **$c_{\mathrm{fmt}} = \mathbb{I} \{ \tilde{p} : \text{matches the schema } \mathcal{F} \}$**：格式匹配指标，确保输出可解析。
- **$R_{\mathrm{eval}} = \alpha c_{\mathrm{all}} + (1-\alpha) c_{\mathrm{fmt}}$**：加权组合，$\alpha=0.9$ 保证正确性占主导。

这一设计避免了传统SFT在合成数据上的过拟合问题——实验表明SFT会过拟合合成模式导致真实图像性能下降，而GRPO在合成和真实子集上均实现提升（Table 6）。

### 4. 合成数据生成管线：支撑创新的基础设施

为获得可规模化、标签精确的训练数据，本文构建了混合合成框架，包含两个互补后端：

- **2D程序化渲染器**：利用LLM编写代码生成多样布局的2D仪器图像，完全控制字体和几何参数，确保标签零误差。
- **3D物理渲染器（Blender）**：使用Blender资产生成具有真实光照、材质和遮挡的3D仪器图像，通过随机化背景、指针角度、刻度范围和相机位姿增强多样性。
- **生成器注册系统**：统一接口管理所有仪器生成器，每个生成器返回渲染图像及标准化标签（数值、单位、读数设计类型）。

该管线的核心价值在于：**以零人工标注成本，为细粒度感知任务提供无限量、高精度的监督信号**，直接针对VLM的感知短板进行数据增强。

### 5. 创新边界与未解决问题

尽管GRPO微调在合成数据上带来显著提升（Qwen2.5-VL-7B从10.9%升至35.2%，+222.9%），但对真实图像的泛化仍然有限（从14.6%升至19.7%，仅+5.1个百分点），说明合成到真实的域差未完全消除。复合仪表（如多表盘电表）几乎全军覆没，语言模型先验（如“10:10”倾向、整数偏好）虽有所减弱但未根除。这些限制指向更深层的开放问题：**是否需要更紧密的视觉-语言交互机制或更高分辨率的视觉编码器，才能从根本上解决细粒度感知问题？**

## 整体框架

MeasureBench 的构建与评测围绕一个“数据生成—基准测试—诊断分析—强化微调”的闭环框架展开，旨在系统性地暴露并缓解 VLM 在视觉测量读数任务中的感知瓶颈。

### 框架总览

整个工作流由四个核心模块串联而成：

1. **混合合成数据生成器**：通过 2D 程序化渲染与 3D 物理渲染两条互补管线，生成覆盖 39 种仪器外观的合成训练与评测数据。
2. **MeasureBench 基准数据集**：整合 1,272 张人工标注的真实仪器图像与 1,170 张合成图像，按四种读数设计（Dial / Digital / Linear / Composite）组织，共计 2,442 个图像–问题对。
3. **多维度诊断评估**：从整体准确率、数值准确率、单位准确率、读数设计、仪器类别等维度对前沿 VLM 进行细粒度诊断，定位“单位识别强、数值读取弱”的系统性缺陷。
4. **GRPO 强化微调**：以合成数据为训练集，采用规则奖励（$\alpha=0.9$ 的正确性奖励 + $0.1$ 的格式奖励）驱动 GRPO 算法对 Qwen2.5-VL 系列进行微调，在不损害通用能力的前提下提升测量读数性能。

### 数据生成管线

合成数据生成是整个框架的基础设施，其设计目标是“多样性 × 可控性 × 真实感”的平衡。如图 3 所示，该管线包含两条互补的后端：

- **2D 程序化渲染器**：通过 LLM 根据模板提示编写代码，生成具有多样布局的 2D 仪器图像。该后端对字体、几何形状和刻度分布拥有完全控制权，适合快速生成大规模、高变异度的训练数据。
- **3D 物理渲染器（Blender）**：利用 Blender 资产，通过随机化背景、指针角度、量程范围和相机位姿，生成具有真实光照、材质和遮挡的逼真仪器图像。该后端弥补了 2D 渲染在真实感上的不足，有助于缩小合成到真实的域差。

两条管线通过统一的**生成器注册系统**进行管理：每个仪器名称映射到一个生成器，生成器返回渲染图像及标准化标签（数值、单位、读数设计类型），确保数据格式的一致性。

### 训练与评测闭环

在合成数据生成的基础上，框架进入“评测—反馈—微调”的闭环：

- **基准评测**：在 MeasureBench 的真实和合成子集上对 VLM 进行零样本评估，输出整体、数值、单位及按仪表类型的准确率矩阵（Table 2），同时通过消融实验（禁用思考、不同提示设置、SFT vs. GRPO 对比）定位瓶颈。
- **GRPO 强化微调**：以 3,900 张合成图像（39 种仪器 × 100 样本）为训练数据，采用 verl 库实现 GRPO 算法。奖励函数 $R_{\mathrm{eval}} = \alpha c_{\mathrm{all}} + (1-\alpha) c_{\mathrm{fmt}}$ 同时优化读数正确性（$c_{\mathrm{all}}$）和输出格式规范性（$c_{\mathrm{fmt}}$），并要求模型在 `<think>...</think>` 标签内输出推理过程。
- **泛化验证**：微调后在 MeasureBench 真实子集和通用基准（Table 5）上分别验证，确保测量读数能力的提升不以牺牲通用视觉语言能力为代价。

### 关键设计决策

框架的几项设计直接服务于核心洞察——“瓶颈在感知精度，而非任务知识”：

- **合成数据的随机化策略**：在生成过程中随机化刻度、指针角度、背景、光照和相机位姿，避免模型记忆特定外观模式，迫使模型学习真正的指针定位和刻度映射能力。
- **区间匹配评估**：采用区间匹配而非精确值匹配作为评估标准，以容纳测量读数的自然容忍误差，使评估更贴近实际应用场景。
- **GRPO 优于 SFT 的训练策略选择**：实验表明 SFT 会过拟合合成数据的视觉模式，导致真实图像性能下降；而 GRPO 通过奖励信号引导模型关注数值正确性而非表面纹理，在两个子集上均实现提升（Table 6）。

这一框架的局限性在于：合成到真实的域差未能完全消除（真实子集提升约 5 个百分点，远低于合成子集的 20+ 个百分点），且复合仪表（如多表盘电表）的读数几乎全军覆没，表明极精细的几何推理仍是当前 VLM 架构的障碍。

### 补充图表

![[assets/figures/papers/paper_list_l2737_https_arxiv_org_abs_2510_26865/figures/004_Figure_3.jpg]]
*Figure 3: Left: A hybrid measuring instrument synthesis framework. Right: Examples of synthetic images*

![[assets/figures/papers/paper_list_l2737_https_arxiv_org_abs_2510_26865/figures/018_Figure_9.jpg]]
*Figure 9: Additional examples of synthetic measuring instruments generated by our pipeline*

## 核心模块与公式推导

### 混合合成数据生成框架

为解决真实测量仪器图像采集与标注成本高、多样性受限的问题，本文提出了一套混合合成框架，包含两条互补的渲染管线：

- **2D程序化渲染器**：通过提示模板指定仪器类型与读数约束，利用LLM编写代码生成多样布局的2D仪器图像。该方案可完全控制字体和几何属性，适合快速生成风格化、布局多变的合成样本。
- **3D物理渲染器（Blender）**：基于Blender资产生成具有真实光照、材质和遮挡的3D仪器图像。通过随机化背景、仪器读数（如指针角度、刻度范围）和相机位姿，产生照片级真实感的训练数据。
- **生成器注册系统**：统一接口管理所有仪器生成器，每个生成器返回渲染图像及标准化标签（包含数值、单位和读数设计类型）。

该框架覆盖39种仪器外观，为后续强化微调提供了3,900张合成图像-问题对。

### GRPO强化微调模块

为提升VLM在测量读数任务上的细粒度视觉感知能力，本文采用GRPO算法（Shao et al., 2024）对Qwen2.5-VL系列模型进行强化微调（RFT）。核心设计包括：

**奖励函数**：采用规则奖励，兼顾读数正确性与输出格式规范性：

$$R_{\mathrm{eval}} = \alpha c_{\mathrm{all}} + (1 - \alpha) c_{\mathrm{fmt}} \quad (\alpha = 0.9)$$

其中：

- **$c_{\mathrm{all}}$**：完整正确性指标，指示预测数值落在真实区间内且单位正确：

$$c_{\mathrm{all}} = \mathbb{I} \{ \hat{y} \in I \wedge \hat{u} = u \}$$

- **$c_{\mathrm{fmt}}$**：格式正确性指标，指示模型输出是否符合指定格式（包含`<think>`标签内的推理过程和最终答案）：

$$c_{\mathrm{fmt}} = \mathbb{I} \{ \tilde{p} : \mathrm{matches} : \mathrm{the} : \mathrm{schema} : \mathcal{F} \}$$

**输出格式约束**：要求模型在`<think>...</think>`标签内输出推理过程，随后给出最终答案，以引导模型显式进行逐步感知与推理。

**训练配置**：基于verl库实现，在3,900张合成图像上进行训练。消融实验表明，GRPO相比SFT具有更好的泛化性——SFT会过拟合合成数据模式导致真实图像性能下降，而GRPO在合成和真实两个子集上均取得提升。

### 评估指标中的软间隔得分（消融用）

为探索更平滑的奖励信号，本文还定义了软间隔部分得分，用于消融实验：

**到真实区间的距离**：

$$d ( \hat { y } , I ) = \left\{ \begin{array} { l l } { 0 , } & { \hat { y } \in [ l , r ] , } \\ { \operatorname* { m i n } ( | \hat { y } - l | , | \hat { y } - r | ) , } & { \mathrm { o t h e r w i s e } } \end{array} \right.$$

**软间隔边距**：

$$m ( I ) = \left\{ \begin{array} { l l } { r - l , } & { r > l , } \\ { 0 . 0 5 l , } & { \mathrm { o t h e r w i s e } } \end{array} \right.$$

**软间隔部分得分**（线性衰减，鼓励接近正确答案的预测）：

$$s _ { \mathrm { s m } } ( \hat { y } ; I ) = \frac { 1 } { 2 } \operatorname* { m a x } \Bigl \{ 0 , 1 - \frac { d ( \hat { y } , I ) } { m ( I ) + \varepsilon } \Bigr \}$$

消融结果显示，软间隔奖励与原始硬间隔奖励性能几乎相同，说明原始奖励设计已足够有效。

## 实验与分析

### 核心瓶颈：视觉感知而非知识理解

MeasureBench 的评测结果揭示了一个清晰且反直觉的发现：**当前 VLM 在测量读数任务上的失败根源于细粒度视觉感知缺陷，而非任务知识或文本理解的不足**。这一结论由多条强证据链支撑：

1. **单位识别与数值读取的巨大鸿沟**：所有模型在单位识别上的准确率普遍超过 90%（如 Gemini 2.5 Pro 在真实图像上单位准确率达 96.2%），但数值准确率极低（仅 30.7%）。这表明模型完全理解“该读什么”，却无法精确“读出多少”。

2. **推理时思考（inference-time thinking）几乎无效**：如 Figure 5 所示，启用思考过程对性能提升甚微，有时甚至导致表现下降。这说明增加文本推理链条无法弥补视觉定位的微小误差。

![[assets/figures/papers/paper_list_l2737_https_arxiv_org_abs_2510_26865/figures/007_Figure_5.jpg]]
*Figure 5: Performance and efficiency analysis of various large vision-language models. The accuracy against the average token count is plotted to show the performance-cost trade-off*

3. **逐步操作指引收效甚微**：即使提供详细的仪表阅读步骤指导（Table 4），在真实图像上的性能提升极为有限（如 Gemini-2.5-Pro 仅从 30.2% 提升至 31.8%）。模型缺少的不是“如何读”的知识，而是“看清指针位置”的视觉精度。

![[assets/figures/papers/paper_list_l2737_https_arxiv_org_abs_2510_26865/figures/010_Table_4.jpg]]
*Table 4: the same readout design and instrument-specific guidance. As shown in Table 4, even with explicit guidance on how to read the instruments, the performance gain on real-world MeasureBench is very limited. Adding in-context examples does not seem to help either, suggesting that the bottleneck lies in fine-grained visual perception rather than a lack of procedural knowledge*

4. **案例分析揭示典型失败模式**：多数错误源于指针定位的微小偏差——仅错位一个刻度就导致读数完全错误（例如将 4.4 A 误读为 4.5 A），而非大范围的理解失败。

### 主要实验结果

Table 2 报告了各模型在 MeasureBench 真实与合成子集上的全面表现。**最佳模型 Gemini-2.5-Pro 在真实图像上的整体准确率仅为 30.2%，合成图像上更低至 26.3%**，凸显该任务的极高挑战性。

![[assets/figures/papers/paper_list_l2737_https_arxiv_org_abs_2510_26865/figures/005_Table_2.jpg]]
*Table 2: Performance on real and synthetic images. We report accuracy (%) for each model: overall (Ovr), value (Val), unit (Unit), and by readout type—Dial, Digital (Dig), Linear (Lin), Composite (Com)*

按仪表类别细分（Figure 4），模型在不同类别间表现差异显著：简单数字读数相对较好，而复合仪表（如多表盘电表）几乎全军覆没。值得注意的是，合成图像对模型的挑战普遍大于真实图像，说明合成数据的视觉分布与真实场景仍存在域差。

![[assets/figures/papers/paper_list_l2737_https_arxiv_org_abs_2510_26865/figures/006_Figure_4.jpg]]
*Figure 4: Model accuracies on real images by instrument category (categories with ≥20 samples)*

在提示策略方面（Table 3），使用特定仪器名称进行提示对单位准确率有中等正向影响，但对整体准确率无实质差异。这说明模型虽能利用类别先验推断单位，却无法将其转化为精确的数值读取能力。

![[assets/figures/papers/paper_list_l2737_https_arxiv_org_abs_2510_26865/figures/008_Table_3.jpg]]
*Table 3: Model performance under different prompt settings*

### GRPO 强化微调的效果与局限

在合成数据上对 Qwen2.5-VL 系列进行 GRPO 强化微调取得了显著但有限的提升（Table 8）：

![[assets/figures/papers/paper_list_l2737_https_arxiv_org_abs_2510_26865/figures/014_Table_8.jpg]]
*Table 8: Results of Qwen2.5-VL series with GRPO on real-world and synthetic subsets*

- 对 **Qwen2.5-VL-7B**，合成子集整体准确率从 10.9% 跃升至 35.2%（+222.9%），真实子集从 14.6% 提升至 19.7%（+34.9%）。
- 对比 SFT（监督微调），GRPO 展现出更好的泛化能力：SFT 会过拟合合成数据的视觉模式，导致真实图像性能下降；而 GRPO 同时提升了两个子集的表现（Table 6）。

![[assets/figures/papers/paper_list_l2737_https_arxiv_org_abs_2510_26865/figures/012_Table_6.jpg]]
*Table 6: Comparison of GRPO and SFT training on Qwen2.5-VL-7B. SFT overfits to synthetic patterns, degrading real-world performance, while GRPO improves both*

然而，**合成到真实的泛化鸿沟依然显著**：真实图像上的绝对提升仅约 5 个百分点，远低于合成数据上超过 20 个百分点的增幅。这表明合成数据虽能有效教授基础读数技能，但真实场景中的光照、遮挡、磨损等复杂因素仍未被充分覆盖。

此外，GRPO 训练未损害模型通用能力。Table 5 显示，在合成测量数据上训练后，Qwen2.5-VL-7B 在通用基准上的表现与训练前相当，说明该微调策略具有良好的任务特异性。

![[assets/figures/papers/paper_list_l2737_https_arxiv_org_abs_2510_26865/figures/011_Table_5.jpg]]
*Table 5: To assess potential negative transfer from reinforcement finetuning on synthetic measurement data, we evaluate Qwen2.5-VL-7B before and after GRPO training on popular general-purpose benchmarks. As shown in Table 5, GRPO training on synthetic data yields comparable performance on these benchmarks with no degradation, indicating that the model retains its general capabilities*

### 消融实验与关键发现

- **软边际奖励与硬边际奖励效果相当**（Table 9）：使用基于距离的软部分得分并未带来额外增益，说明原始规则奖励设计已足够有效。
- **早期专用系统泛化能力极差**（Table 7）：在 MeasureBench 的指针仪表子集上，专用指针读数系统的准确率远低于通用 VLM，部分系统甚至完全失败（N/A），验证了通用模型在该任务上的相对优势。
- **语言模型先验难以根除**：模型表现出明显的“10:10”钟表偏好（Table 10）和整数输出倾向，这些先验虽可通过 RFT 减弱，但并未完全消除。

![[assets/figures/papers/paper_list_l2737_https_arxiv_org_abs_2510_26865/figures/013_Table_7.jpg]]
*Table 7: Model accuracy (%) for VLMs and prior special-purpose systems*

### 失败模式总结

1. **指针定位偏差**：最常见的错误类型，模型在辨识指针精确指向时存在系统性偏差，常偏移一至两个刻度。
2. **刻度线辨别困难**：密集或细小的刻度线导致模型无法正确映射数值。
3. **复合仪表理解失败**：多表盘、多指针的复杂仪器（如电表）对当前 VLM 构成极大挑战，准确率趋近于零。
4. **合成域过拟合**：SFT 训练的模型过度适应合成图像的视觉特征（如简洁背景、规整字体），在真实图像上反而性能退化。

> **注意**：上述失败模式基于论文提供的案例分析（Figure 6）和统计分布（Figure 8、Figure 13、Figure 14），具体错误样本的定量分布需查阅原文图表确认。

![[assets/figures/papers/paper_list_l2737_https_arxiv_org_abs_2510_26865/figures/009_Figure_6.jpg]]
*Figure 6: Case studies. Text in green marks statements consistent with the image; yellow marks contradictions*

## 方法谱系与知识库定位

### 任务定位：视觉测量读数作为细粒度感知基准

MeasureBench 将视觉测量读数（visual measurement reading）系统化为一类独立的视觉语言理解任务，其核心要求是从仪器图像中提取精确的空间信息（指针角度、刻度对应关系），并完成轻量算术映射。这与传统 OCR、场景文本识别或通用 VQA 存在本质区别：后者的成功通常依赖语义理解与文本先验，而测量读数任务的关键瓶颈在于**几何精度的感知能力**，而非高层推理或知识检索。

论文通过一系列消融实验确立了这一判断：
- **单位识别 vs. 数值读取的显著差距**：所有测试模型在单位识别上的准确率普遍超过 90%（如 Gemini 2.5 Pro 在真实图像上达到 96.2%），但数值准确率极低（仅 30.7%），证明模型完全理解“该读什么”，却无法“读对数值”。
- **推理时思考（inference-time thinking）几乎无效**：启用链式思考（chain-of-thought）对性能提升甚微，有时甚至导致性能下降（Figure 5），说明文本推理无法弥补视觉感知的缺陷。
- **逐步操作指令收益极低**：即使提供详细的仪表阅读指南（如“观察指针指向的刻度”），真实图像上的性能增益也十分有限（Table 4），进一步确认模型欠缺的不是“如何读”的知识，而是视觉精度本身。

### 与现有基准和方法的关系

**与通用 VLM 基准的区别**。现有主流 VLM 基准（如 MME、MMBench、MMMU）侧重语义理解、知识推理或粗粒度视觉问答，而 MeasureBench 首次将细粒度空间感知作为独立维度进行压力测试。这一设计填补了当前评估体系中对“精确几何感知”覆盖不足的空白。

**与专用仪表读数系统的对比**。早期工作（如指针仪表读数专用系统）依赖手工设计的检测流水线（指针分割、霍夫变换等），在特定仪表类型上可取得较高精度，但泛化能力极差。论文在 Table 7 中验证：这些专用系统在 MeasureBench 的指针仪表子集上几乎全部失效（标记为 N/A），而通用 VLM 虽整体精度不高，但至少能在部分样本上给出合理回答，展现出更强的跨仪表泛化潜力。

**与合成数据驱动训练的关系**。论文提出的 GRPO（Group Relative Policy Optimization）强化微调方法基于合成数据进行训练，属于“合成数据 + 强化学习”的范式。与监督微调（SFT）相比，GRPO 在合成数据上大幅提升（+222.9%），同时在真实数据上也获得正向迁移（+34.9%），而 SFT 则过拟合合成模式、导致真实图像性能退化（Table 6）。这一结果表明，基于规则奖励的强化学习比直接模仿合成答案更适合处理合成-真实域差。

### 适用边界与局限

**合成数据泛化的天花板**。尽管 GRPO 在合成子集上实现了超过 35% 的准确率，但在真实图像上仅提升约 5 个百分点（从 14.6% 到 19.7%），合成到真实的域差远未消除。论文指出，合成数据训练的收益主要集中在简单仪表（单指针表盘、数字读数），对复合仪表（如多表盘电表）几乎无效。

**复合仪表仍是系统性障碍**。多指针、多表盘的复合读数任务（Composite 类别）在几乎所有模型上表现极差，表明极精细的几何推理——同时定位多个指针并分别映射到不同刻度——仍是当前 VLM 架构的盲区。

**语言模型先验的残留影响**。模型表现出明显的先验偏好，如倾向于回答“10:10”（钟表图像的常见训练数据偏差）或输出整数值。论文通过 RFT 在一定程度上减弱了这些偏差，但并未根除（Table 10）。

**未探索的架构改进空间**。论文明确指出，未探索更大规模合成数据或更强视觉编码器（如高分辨率特征提取、可微分指针检测模块）是否能根本性解决细粒度感知问题。这为后续工作留下了明确的改进方向。

### 开放问题

1. **推理时思考为何失效？** 当前 VLM 的链式思考机制主要针对文本推理优化，缺乏对视觉注意力区域的精确引导。是否需要设计更紧密的视觉-语言交互机制（如视觉定位增强的思维链），使模型能够“看向正确的位置”而非仅“思考正确的步骤”？

2. **是否存在更好的视觉表示？** 高分辨率特征图、可微分的指针/刻度检测头、或专门的几何编码模块是否能从根本上提升 VLM 的仪表读数能力？这指向了视觉编码器架构层面的改进需求。

3. **合成到真实的泛化鸿沟如何弥合？** 增加合成数据的多样性（更多光照、材质、遮挡变化）是否能进一步缩小域差？或者必须借助少量真实标注数据进行域适应（domain adaptation）？

4. **能否实现通用视觉感知-数值映射模块？** 当前方法对每种仪表类型依赖独立的合成数据生成器。是否存在一种统一的感知-映射架构，使 VLM 能够泛化到训练中完全未见过的全新仪表类型？

## 原文 PDF

![[paperPDFs/CVPR_2026/Do_Vision_Language_Models_Measure_Up_Benchmarking_Visual_Measurement_Reading_with_MeasureBench.pdf]]
