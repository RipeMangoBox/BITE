---
title: "SpatialReward: Verifiable Spatial Reward Modeling for Fine-Grained Spatial Consistency in Text-to-Image Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SpatialReward_Verifiable_Spatial_Reward_Modeling_for_Fine_Grained_Spatial_Consistency_in_Text_to_Image_Generation.pdf
project_link: null
code_link: "https://github.com/LivingFutureLab/SpatialReward"
aliases:
- SpatialReward
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 可验证的空间奖励模型，通过Prompt Decomposer提取结构化约束、专家检测器提供准确视觉证据、VLM进行链式推理，为RL训练提供可靠的细粒度空间反馈。
primary_logic: 将规则化可验证奖励从逻辑推理扩展到视觉空间评估，利用提示分解、专家检测和链式推理协同工作，能够显著提升T2I模型的空间一致性，且奖励信号与人类判断高度相关。
claims:
- 在SD3.5-M上，GenEval整体准确率从0.67提升至0.95，SpatRelBench从0.23提升至0.42；在FLUX1-dev上分别提升+0.21和+0.18。
- 移除专家检测阶段导致GenEval准确率从95.2%骤降至70.3%，移除排除约束使SpatRelBench降至25.9%，移除CoT降至27.9%，证实各组件的关键作用。
- SpatialReward与人类空间判断的相关性最高，Spearman ρ达到0.63。
- GenEval (SD3.5-M, 80-Obj) 上 Overall accuracy = 0.95
---

# SpatialReward: Verifiable Spatial Reward Modeling for Fine-Grained Spatial Consistency in Text-to-Image Generation

> [!tip] 核心洞察
> 将规则化可验证奖励从逻辑推理扩展到视觉空间评估，利用提示分解、专家检测和链式推理协同工作，能够显著提升T2I模型的空间一致性，且奖励信号与人类判断高度相关。

| 字段 | 内容 |
|------|------|
| 中文题名 | SpatialReward：面向文本到图像生成中细粒度空间一致性的可验证空间奖励建模 |
| 英文题名 | SpatialReward: Verifiable Spatial Reward Modeling for Fine-Grained Spatial Consistency in Text-to-Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.22228) · [Code](https://github.com/LivingFutureLab/SpatialReward) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | SpatialReward |
| Dataset | GenEval, SpatRelBench, Human spatial consistency judgments |

> [!tip] 效果简介
> - GenEval (SD3.5-M, 80-Obj) 上，Overall accuracy 0.95 vs 0.67 (+0.28)。
> - SpatRelBench (SD3.5-M, 1k-Obj) 上，Overall accuracy 0.42 vs 0.23 (+0.19)。
> - GenEval (FLUX1-dev) 上，Overall improvement N/A vs N/A (+0.21 over FLUX1-dev baseline)。

## 概述

文本到图像（T2I）生成模型近年来取得了显著进展，但在细粒度空间一致性方面仍存在根本性瓶颈。现有奖励模型（如基于CLIP的评分器或VLM整体评估器）侧重于全局语义对齐和视觉质量，却忽略了物体定位、方向、深度顺序及空间关系等关键维度，导致生成图像虽然“看起来合理”，却频繁出现物体位置错误、方向不对、文本与物体空间关系错乱等问题。

**核心洞察**在于：将规则化可验证奖励从逻辑推理领域扩展到视觉空间评估，通过提示分解、专家检测与链式推理三阶段协同，能够为强化学习训练提供可靠的细粒度空间反馈信号。这一思路的关键因果杠杆是**可验证性**——每个空间约束都有明确的视觉证据支撑，而非依赖黑箱模型的隐式判断。

基于此，本文提出**SpatialReward**，一种多阶段可验证空间奖励模型。其工作流程为：（1）**Prompt Decomposer**将自由格式提示解析为结构化约束集（包含/排除约束、属性、空间关系）；（2）**专家检测器**（物体检测、颜色分类、方向估计、深度估计、OCR）提供准确的视觉证据；（3）**VLM链式推理**以检测证据为锚点，逐步推理空间关系并聚合最终奖励分数。将该奖励模型集成到Flow-GRPO强化学习框架中，对Stable Diffusion 3.5-M和FLUX1-dev进行对齐训练。

**主要结果**：在SD3.5-M上，GenEval整体准确率从0.67提升至0.95（+0.28），SpatRelBench从0.23提升至0.42（+0.19）；在FLUX1-dev上分别提升+0.21和+0.18。SpatialReward与人类空间判断的Spearman相关系数达到0.63，显著优于现有奖励模型。消融实验证实，移除专家检测阶段导致GenEval准确率从95.2%骤降至70.3%，移除排除约束和链式推理分别使SpatRelBench降至25.9%和27.9%，验证了各组件的关键作用。

**方法定位**：SpatialReward属于**可验证奖励建模**范式，将细粒度空间评估从固定格式提示（如GenEval）扩展到自由格式提示，覆盖物体方向、深度顺序、文本放置及复杂多物体空间关系。与PickScore（NeurIPS 2023）、ImageReward（NeurIPS 2023）、HPSv2（arXiv 2023）等全局评分器相比，其核心差异在于**显式空间约束验证**而非隐式语义匹配。

## 背景与动机

文本到图像（T2I）生成模型近年来取得了显著进展，能够根据自由形式的文本描述生成高质量、语义合理的图像。然而，现有模型在**细粒度空间一致性**方面仍存在根本性瓶颈：生成图像往往在全局语义上看似合理，却在物体定位、相对方向、深度顺序、文本放置等空间关系上频繁出错。例如，提示要求“左边的猫比右边的狗大”，模型可能生成大小关系颠倒的图像；要求“杯子上的文字是‘Hello’”，生成的文字可能错位或内容不符。

这一瓶颈的根源在于当前主流的奖励模型（Reward Model）和评估指标的设计缺陷。以 **CLIP-L/14**（Radford et al., ICML 2021）、**PickScore**（Kirstain et al., NeurIPS 2023）、**ImageReward**（Xu et al., NeurIPS 2023）、**HPSv2**（Wu et al., arXiv 2023）为代表的奖励模型，以及 **UnifiedReward**（arXiv 2025）、**VisionReward**（arXiv 2024）等较新的方法，主要关注**全局语义对齐**和**整体视觉质量**，缺乏对物体定位、方向、深度顺序、排除约束等细粒度空间关系的显式验证能力。这导致强化学习（RL）训练过程中，生成模型接收到的反馈信号无法有效区分“空间正确”与“空间错误”的样本，从而难以针对性地优化空间一致性。

从因果机制来看，问题的关键“控制旋钮”在于：**需要一个可验证的空间奖励模型，能够将自由形式的提示分解为结构化的空间约束，并基于准确的视觉证据进行逐条验证，最终为RL训练提供可靠的细粒度空间反馈**。SpatialReward正是围绕这一核心洞察展开设计，将规则化可验证奖励从逻辑推理领域扩展到视觉空间评估，通过提示分解、专家检测和链式推理三阶段协同工作，显著提升T2I模型的空间一致性，且奖励信号与人类判断高度相关（Spearman ρ达到0.63）。

## 核心创新

SpatialReward 的核心创新在于将**可验证奖励**从逻辑推理领域系统性地引入视觉空间评估，构建了一个多阶段、可解释的细粒度空间反馈机制。与现有T2I奖励模型仅关注全局语义对齐和整体视觉质量不同，SpatialReward 直接面向物体定位、朝向、深度顺序、文本嵌入位置以及排除性约束等细粒度空间关系，填补了当前奖励信号在空间一致性维度上的结构性空白。

### 从全局评分到可验证空间约束

现有奖励模型（如 **PickScore** (NeurIPS 2023)、**ImageReward** (NeurIPS 2023)、**HPSv2** (arXiv 2023)、**CLIP-L/14** (ICML 2021) 等）本质上是对图像-文本的整体匹配度进行标量评分，缺乏对空间关系正确性的显式建模。其根本瓶颈在于：评分信号是“黑箱”的，无法区分“物体存在但位置错误”与“物体完全缺失”这两种截然不同的失败模式。SpatialReward 将奖励信号分解为可独立验证的结构化约束，使每项空间要求都能获得明确的、基于视觉证据的反馈。

这一转变体现在两个关键的 **changed slots** 上：

1. **奖励模型设计范式**：从“全局语义/整体评分器”转变为“多阶段可验证奖励”。基线方法依赖 CLIP 类模型或 VLM 进行端到端评分，而 SpatialReward 采用提示分解 → 专家检测 → 链式推理的流水线架构，每个阶段提供可审计的中间结果。

2. **空间评估粒度**：从“粗糙的物体存在性检查”跃升至“细粒度的空间关系验证”。GenEval 等基准仅覆盖固定格式的简单提示，而 SpatialReward 能够处理物体朝向、三维深度顺序、文本与物体的空间包含关系以及复杂的多物体排除约束。

### 三阶段协同架构

SpatialReward 的创新性集中体现在其流水线的三个协同模块上（参见 Figure 2）：

**阶段一：Prompt Decomposer（提示分解器）**  
基于微调的 Qwen2.5-VL-7B，将自由形式的提示 $P$ 解析为结构化约束集 $\mathcal{C} = \mathcal{D}(P) = (\mathrm{tag}, \mathcal{C}_{\mathrm{inc}}, \mathcal{C}_{\mathrm{exc}})$，显式分离包含约束 $\mathcal{C}_{\mathrm{inc}}$ 和排除约束 $\mathcal{C}_{\mathrm{exc}}$。这一步将模糊的自然语言指令转化为可机器验证的规范，是后续所有验证的基础。

**阶段二：Expert Detectors（专家检测器）**  
调用目标检测、CLIP 色彩分类器、朝向估计器、深度估计器和 OCR 等专业模型，对生成图像中的物体存在性、数量、颜色、朝向、文本内容及其空间位置进行独立验证。例如，文本奖励 $\mathcal{R}_{\mathrm{text}}$ 要求生成文本不仅内容匹配目标字符串，还必须通过 $\mathrm{IoA}$ 度量确认其位于正确的物体边界框内。这一阶段提供了**准确的视觉证据锚点**，大幅降低了后续推理的幻觉风险。

**阶段三：Chain-of-Thought Reasoning（链式推理）**  
以 Qwen2.5-VL 为骨干，将检测阶段提供的边界框、属性和空间信号作为 grounding，进行逐步推理以评估复杂空间关系。空间一致性奖励 $\mathcal{R}_{\mathrm{spatial}}$ 由 VLM 基于目标关系 $r$、边界框 $B_A/B_B$ 和已验证属性进行解析得出。最终总奖励 $\mathcal{R}_{\mathrm{total}} = \sum_{c \in \mathcal{C}_{\mathrm{inc}}} \mathcal{R}_{\mathrm{spatial}}^{+}(c) - \sum_{c \in \mathcal{C}_{\mathrm{exc}}} \mathcal{R}_{\mathrm{spatial}}^{-}(c)$ 汇总所有包含约束的正向奖励和排除约束的惩罚。

### 创新有效性的决定性证据

消融实验（Table 4）揭示了三个模块各自的关键贡献：移除专家检测阶段导致 GenEval 准确率从 95.2% 骤降至 70.3%，证实视觉证据锚定是不可或缺的；去除链式推理使 SpatRelBench 准确率从 37.1% 降至 27.9%，说明纯检测匹配无法处理复杂空间语义；移除排除约束使 SpatRelBench 进一步降至 25.9%，验证了负向约束建模的必要性。

与人类判断的相关性评估（Table 3）进一步表明，SpatialReward 的 Spearman $\rho$ 达到 0.63，在所有对比奖励模型中最高，证明其细粒度空间评估与人类空间感知高度一致。

## 整体框架

SpatialReward 的整体设计围绕一个核心命题展开：**如何为文本到图像（T2I）生成模型提供可验证的细粒度空间反馈**。现有奖励模型（如 CLIP-L/14、ImageReward、PickScore 等）擅长评估全局语义对齐与整体视觉质量，却对物体定位、朝向、深度顺序、文本嵌入位置等空间关系“视而不见”。SpatialReward 通过一个多阶段可验证奖励管道，将自由形式的文本提示逐步转化为结构化空间约束，并在生成图像上进行逐条核验，最终输出一个与人类空间判断高度相关的奖励信号（Spearman ρ = 0.63）。

### 管道总览

整个系统由三个串联阶段构成，形成“分解—检测—推理”的闭环：

1. **Prompt Decomposer（提示分解器）**：将自由形式提示解析为结构化约束集。
2. **Expert Detectors（专家检测器）**：在生成图像上对物体存在性、数量、颜色、朝向、深度、文本等属性进行可验证检测。
3. **Chain-of-Thought Reasoning（链式推理）**：以检测结果为视觉锚点，驱动视觉语言模型（VLM）逐步推理空间关系，聚合最终奖励分数。

该奖励模型被嵌入 **Flow-GRPO** 强化学习框架中，用于微调 SD3.5-M 和 FLUX1-dev 等基础 T2I 模型。训练采用 LoRA 进行参数高效微调（rank r=32，scaling factor α=64），KL 正则化系数 β=0.04，采样时间步 T=10，组大小 G=24，噪声水平 a=0.7，固定分辨率 512×512。

### 阶段一：提示分解

Prompt Decomposer $\mathcal{D}$ 基于微调的 Qwen2.5-VL-7B，将自由形式提示 $P$ 映射为结构化约束集：

$$\mathcal{C} = \mathcal{D}(P) = (\mathrm{tag}, \mathcal{C}_{\mathrm{inc}}, \mathcal{C}_{\mathrm{exc}})$$

其中 $\mathrm{tag}$ 标识评估类别（如单物体、双物体、复杂空间关系等），$\mathcal{C}_{\mathrm{inc}}$ 为包含约束（必须满足的空间与属性要求），$\mathcal{C}_{\mathrm{exc}}$ 为排除约束（必须避免的内容）。这一分解将模糊的自然语言指令转化为可被下游检测器逐条验证的形式化规约，是整个可验证奖励链条的起点。

### 阶段二：专家检测验证

对于每个包含约束 $c \in \mathcal{C}_{\mathrm{inc}}$，系统调用专门的专家模型在生成图像上提取视觉证据。核心检测类型包括：

- **物体检测**：使用目标检测器获取候选边界框集合 $D_c = \{ (B_j, s_j) \}_{j=1}^k$，经置信度阈值 $\tau_{\mathrm{det}}$ 筛选后得到已验证检测框 $\mathcal{B}_c$。
- **存在性与计数奖励**：存在性奖励 $\mathcal{R}_{\mathrm{presence}}(c) = \mathbb{I}(\hat{N}_c > 0)$，计数奖励 $\mathcal{R}_{\mathrm{count}}(c) = \exp(-|\hat{N}_c - N_c^*|)$，对数量偏差进行指数惩罚。
- **属性验证**：包括基于 CLIP 的颜色分类器、朝向估计器、深度估计器。
- **文本奖励**：通过 OCR 识别图像中的文本，结合内容相似度与空间包含度（IoA）计算：

$$\mathcal{R}_{\mathrm{text}}(T^*, B_{\mathrm{obj}}) = \max_{(T_j', B_j') \in \mathcal{T}_{\mathrm{rec}}} \left[ \sin(T^*, T_j') \cdot \mathrm{IoA}(B_j', B_{\mathrm{obj}}) \right]$$

$$\mathrm{IoA}(B_{\mathrm{text}}, B_{\mathrm{obj}}) = \frac{\mathrm{Area}(B_{\mathrm{text}} \cap B_{\mathrm{obj}})}{\mathrm{Area}(B_{\mathrm{text}})}$$

仅当生成文本在内容上匹配目标字符串且空间上位于正确物体边界框内时，才给予高奖励，确保嵌入文本任务的提示保真度。

### 阶段三：链式推理与奖励聚合

前两阶段提供了可验证的“硬证据”（边界框、属性标签、文本匹配结果），但空间关系（如“A 在 B 左侧”“A 面向 B”）本质上需要语义推理。第三阶段以 Qwen2.5-VL 为推理骨干，将检测证据作为视觉锚点输入，通过链式推理（CoT）判断关系是否成立：

$$\mathcal{R}_{\mathrm{spatial}} = \mathcal{P}_{\mathrm{score}} \left( \mathcal{F}_{\mathrm{vlm}} ( P_{\mathrm{CoT}}(r, B_A, B_B, \mathrm{attributes}) ) \right)$$

推理过程综合边界框位置、物体朝向、场景语义等信息，有效避免了纯检测匹配在空间关系判断上的失败（如 Figure 5 所示）。

最终总奖励为包含约束的正向奖励之和减去排除约束的惩罚之和：

$$\mathcal{R}_{\mathrm{total}} = \sum_{c \in \mathcal{C}_{\mathrm{inc}}} \mathcal{R}_{\mathrm{spatial}}^{+}(c) - \sum_{c \in \mathcal{C}_{\mathrm{exc}}} \mathcal{R}_{\mathrm{spatial}}^{-}(c)$$

### 关键设计决策与瓶颈突破

该框架的核心洞察在于**将可验证奖励从逻辑推理领域扩展到视觉空间评估**。传统奖励模型直接端到端评分，缺乏可解释的中间证据，导致空间错误的反馈信号不可靠。SpatialReward 通过“分解—检测—推理”的协同设计，使每个奖励分量都有明确的视觉证据支撑，既提升了奖励信号与人类判断的一致性，也为 RL 训练提供了更精准的梯度方向。

消融实验（Table 4）证实了这一设计的必要性：移除专家检测阶段导致 GenEval 准确率从 95.2% 骤降至 70.3%；去除链式推理使 SpatRelBench 从 37.1% 降至 27.9%；移除排除约束则降至 25.9%。这些结果表明，三个阶段各自承担不可替代的功能——检测提供证据，推理赋予语义，排除约束防止错误生成。

### 局限与依赖

需要注意的是，该管道的奖励质量高度依赖外部专家模型的精度。若目标检测器对特定类别或视角表现不佳，或 OCR 在艺术化字体上失效，可能导致不准确的奖励信号。此外，多阶段串联增加了计算开销，在实时或资源受限场景下可能成为瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l2151_https_arxiv_org_abs_2603_22228/figures/002_Figure_2.jpg]]
*Figure 2: Overall framework of our approach. (a) Standard Flow-GRPO [40] reinforcement learning pipeline for text-to-image generation. (b) The proposed SpatialReward, which parses prompts into structured spatial and attribute constraints, verifies them on generated images via expert detection, and uses vision–language chain-of-thought reasoning to produce the final reward score*

## 核心模块与公式推导

SpatialReward 采用三阶段可验证奖励管道，将自由形式的文本提示转化为结构化的空间约束，并通过专家检测与视觉语言推理生成可微分的奖励信号。整体框架如 Figure 2 所示。

### 3.1 提示分解器（Prompt Decomposer）

第一阶段由基于微调 Qwen2.5-VL-7B 的提示分解器 $\mathcal{D}$ 完成，将自由形式提示 $P$ 解析为结构化约束集：

$$\mathcal{C} = \mathcal{D}(P) = (\mathrm{tag}, \mathcal{C}_{\mathrm{inc}}, \mathcal{C}_{\mathrm{exc}})$$

其中：
- $\mathrm{tag}$：评估类别标签（如单物体、双物体、计数等）
- $\mathcal{C}_{\mathrm{inc}}$：包含约束集，指定图像中必须出现的物体及其属性、空间关系
- $\mathcal{C}_{\mathrm{exc}}$：排除约束集，指定图像中不得出现的物体

每个包含约束 $c \in \mathcal{C}_{\mathrm{inc}}$ 进一步被解析为 $(N_c^*, \mathcal{A}_c, \mathcal{R}_c)$，分别表示目标数量、属性需求（颜色、文本、朝向）和空间关系需求（如"在左边""在上方"等）。

### 3.2 专家检测器可验证奖励（Expert Detector Verifiable Rewards）

第二阶段利用外部专家模型对生成图像进行精确的视觉证据提取，产生可验证的基础奖励信号。

**物体检测与存在/计数奖励。** 对每个约束类别 $c$，物体检测器输出候选边界框集合：

$$D_c = \{ (B_j, s_j) \}_{j=1}^k$$

经置信度阈值 $\tau_{\mathrm{det}}$ 过滤后得到验证检测集 $\mathcal{B}_c$。存在奖励定义为：

$$\mathcal{R}_{\mathrm{presence}}(c) = \mathbb{I}(\hat{N}_c > 0)$$

计数奖励对检测数量 $\hat{N}_c$ 与目标数量 $N_c^*$ 的偏差进行指数惩罚：

$$\mathcal{R}_{\mathrm{count}}(c) = \exp(-|\hat{N}_c - N_c^*|)$$

**属性可验证奖励。** 颜色奖励通过 CLIP 分类器在检测到的物体区域上验证颜色属性；朝向奖励通过朝向估计器判断物体朝向是否与提示一致；深度奖励通过深度估计模型验证物体间的相对深度顺序。

**文本空间奖励。** 针对包含嵌入文本的提示，文本奖励要求生成文字既匹配目标字符串 $T^*$，又正确位于指定物体边界框内：

$$\mathcal{R}_{\mathrm{text}}(T^*, B_{\mathrm{obj}}) = \max_{(T_j', B_j') \in \mathcal{T}_{\mathrm{rec}}} \left[ \sin(T^*, T_j') \cdot \mathrm{IoA}(B_j', B_{\mathrm{obj}}) \right]$$

其中 $\sin(\cdot,\cdot)$ 为文本相似度，IoA（Intersection over Area）衡量文本框被物体包围框包含的程度：

$$\mathrm{IoA}(B_{\mathrm{text}}, B_{\mathrm{obj}}) = \frac{\mathrm{Area}(B_{\mathrm{text}} \cap B_{\mathrm{obj}})}{\mathrm{Area}(B_{\mathrm{text}})}$$

### 3.3 链式推理空间奖励（Chain-of-Thought Spatial Reasoning）

第三阶段将第二阶段提取的视觉证据（边界框 $B_A, B_B$、已验证属性）作为 grounding 输入 Qwen2.5-VL，通过链式推理对空间关系进行逐层判断。推理过程显式组合物体位置、朝向、场景语义等信息，输出空间一致性评分：

$$\mathcal{R}_{\mathrm{spatial}} = \mathcal{P}_{\mathrm{score}} \left( \mathcal{F}_{\mathrm{vlm}} ( P_{\mathrm{CoT}}(r, B_A, B_B, \mathrm{attributes}) ) \right)$$

其中 $r$ 为目标空间关系，$P_{\mathrm{CoT}}$ 为链式推理提示模板，$\mathcal{F}_{\mathrm{vlm}}$ 为 VLM 推理函数，$\mathcal{P}_{\mathrm{score}}$ 将推理结论解析为标量奖励。

**关键设计：** 专家检测信号作为 grounding 输入，显著降低了 VLM 的幻觉风险。消融实验证实，移除专家检测阶段导致 GenEval 准确率从 95.2% 骤降至 70.3%（Table 4），移除链式推理使 SpatRelBench 准确率从 37.1% 降至 27.9%。

### 3.4 奖励聚合

最终空间奖励为所有包含约束的正向奖励之和减去所有排除约束的惩罚之和：

$$\mathcal{R}_{\mathrm{total}} = \sum_{c \in \mathcal{C}_{\mathrm{inc}}} \mathcal{R}_{\mathrm{spatial}}^{+}(c) - \sum_{c \in \mathcal{C}_{\mathrm{exc}}} \mathcal{R}_{\mathrm{spatial}}^{-}(c)$$

其中 $\mathcal{R}_{\mathrm{spatial}}^{+}(c)$ 和 $\mathcal{R}_{\mathrm{spatial}}^{-}(c)$ 分别对应包含约束和排除约束的链式推理奖励。该总奖励被集成到 Flow-GRPO 框架中，作为强化学习优化 T2I 模型的奖励信号。

### 补充图表

![[assets/figures/papers/paper_list_l2151_https_arxiv_org_abs_2603_22228/figures/008_Figure_5.jpg]]
*Figure 5: Effect of CoT reasoning in spatial relations. CoT combines bounding boxes, orientation, and scene semantics, yielding correct classifications where detected-only matching fails*

## 实验与分析

### 瓶颈与核心实验设定

现有T2I奖励模型（如**PickScore** (NeurIPS 2023)、**ImageReward** (NeurIPS 2023)、**HPSv2** (arXiv 2023)等）侧重于全局语义和视觉质量，忽略物体定位、方向、深度顺序等细粒度空间关系，导致生成图像看似合理却存在空间错误。SpatialReward通过可验证的三阶段空间奖励建模——提示分解、专家检测、VLM链式推理——为RL训练提供可靠的细粒度空间反馈。

实验采用Flow-GRPO框架，对**SD3.5-M**和**FLUX1-dev**进行强化学习微调。训练配置为：采样时间步 $T=10$，组大小 $G=24$，噪声水平 $a=0.7$，固定分辨率 $512 \times 512$，使用LoRA进行参数高效微调（秩 $r=32$，缩放因子 $\alpha=64$），KL正则化系数 $\beta=0.04$。

### 主要结果

**Table 1** 展示了SpatialReward与其他奖励模型在GenEval（80类物体）和SpatRelBench（1k类物体）上的定量对比。

在SD3.5-M上，SpatialReward取得GenEval整体准确率 **0.95**（基线0.67，提升+0.28），SpatRelBench整体准确率 **0.42**（基线0.23，提升+0.19）。在FLUX1-dev上，SpatialReward同样带来显著增益：GenEval提升+0.21，SpatRelBench提升+0.18。这些结果表明，SpatialReward在细粒度空间一致性上的优势可跨模型架构迁移。

**Figure 1** 直观对比了SD3.5-M在SpatialReward与基线奖励模型下的性能差异，SpatialReward在所有空间相关子任务上均表现最优或次优。

**Figure 4** 和 **Table 2** 的通用质量指标显示，SpatialReward在Wise、DPG、PickScore等指标上匹配或超越基线，仅在Aesthetic指标上略有下降（SD3.5-M + SpatialReward为5.23 vs 基线5.39），表明空间一致性的提升以轻微的审美损失为代价，但整体生成质量保持竞争力。

### 与人类判断的相关性

**Table 3** 报告了各奖励模型与人类空间一致性判断的相关性。SpatialReward的Spearman $\rho$ 达到 **0.63**，在所有对比奖励模型中最高，且在阈值 $\tau=0.8$ 下的准确率同样领先。这一结果验证了可验证空间奖励信号与人类空间感知的高度一致性，是该方法可信度的关键证据。

### 消融实验

**Table 4** 系统消融了SpatialReward的三个核心组件：

- **移除专家检测阶段**：GenEval准确率从95.2%骤降至70.3%，降幅达24.9个百分点。这证实了基于检测的视觉证据对空间判断至关重要——单纯依赖VLM进行端到端评分会产生严重幻觉。
- **去除链式推理（CoT）**：SpatRelBench准确率从37.1%降至27.9%。**Figure 5** 的案例表明，CoT能够结合边界框、方向和场景语义进行综合推理，纠正仅靠检测匹配产生的错误分类。
- **移除排除约束**：SpatRelBench准确率从37.1%降至25.9%，说明显式建模“不应出现”的物体对空间一致性评估不可或缺。

### 失败模式与局限性

1. **外部模型依赖**：奖励质量受限于检测、OCR、深度估计等专家模型的精度。若检测模型对特定类别或视角表现不佳，可能产生不准确的奖励信号，进而误导RL训练。
2. **计算开销**：多阶段管道（提示分解→多专家检测→VLM推理）增加了推理成本，可能不适合实时或资源受限场景。
3. **基准覆盖**：SpatRelBench主要覆盖常见物体和部分空间关系，可能无法完全代表所有复杂空间场景，评价指标依赖自动化检测流程，存在评估偏差风险。
4. **审美退化**：Table 2中Aesthetic分数的轻微下降表明，当前奖励设计在空间一致性与审美质量之间存在权衡，需进一步优化。

### 补充图表

![[assets/figures/papers/paper_list_l2151_https_arxiv_org_abs_2603_22228/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of T2I generation models aligned with different reward models. Results are on GenEval(80-Obj) and SpatRelBench(1k-Obj), where parentheses indicate the number of object categories. S-Obj: Single object, T-Obj: Two objects, Cnt: Counting, Pos: Positions, Attr-C: Attribute (Color), P-Text: Position-Text OCR, C-Text: Counting-Text OCR, Cpx: Complex spatial relations, Ori: Orientation, 3DRel: 3D spatial relations, Overall: average score over all metrics in each dataset. Bold denotes the best score, and underline denotes the second best*

![[assets/figures/papers/paper_list_l2151_https_arxiv_org_abs_2603_22228/figures/009_Table_4.jpg]]
*Table 4: Ablation results for SpatialReward. Scores (accuracy) are reported for GenEval, SpatRel: SpatialRelBench, and T2IComp: T2I-CompBench. T2I-CompBench values are averaged over its 2D and 3D spatial-consistency tasks*

![[assets/figures/papers/paper_list_l2151_https_arxiv_org_abs_2603_22228/figures/007_Table_3.jpg]]
*Table 3: Correlation and accuracy with human spatial-consistency judgments; accuracy measured at threshold τ = 0.8*

![[assets/figures/papers/paper_list_l2151_https_arxiv_org_abs_2603_22228/figures/001_Figure_1.jpg]]
*Figure 1: Performance comparison of SD3.5-M [16] optimized via RL using SpatialReward versus Baseline Rewards*

![[assets/figures/papers/paper_list_l2151_https_arxiv_org_abs_2603_22228/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison of generated image quality across different methods*

![[assets/figures/papers/paper_list_l2151_https_arxiv_org_abs_2603_22228/figures/003_Figure_3.jpg]]
*Figure 3: Overview of SpatRelBench, depicting benchmark tasks and their data distribution (a), the construction pipeline (b), and the evaluation methodology (c) designed to assess spatial relation understanding in text-to-image models*

## 方法谱系与知识库定位

### 与现有奖励模型的定位关系

当前文本到图像（T2I）生成的奖励模型主要沿着两条技术路线演进：**全局语义对齐**与**通用视觉质量评估**。以 **CLIP-L/14**（Radford et al., ICML 2021）为代表的对齐评分器通过图文匹配度提供训练信号，但其粒度停留在整体图像层面，无法区分“物体存在但位置错误”与“物体存在且位置正确”这两种截然不同的生成结果。后续工作如 **PickScore**（NeurIPS 2023）、**ImageReward**（NeurIPS 2023）和 **HPSv2**（arXiv 2023）通过人类偏好数据训练更精细的评分模型，**UnifiedReward**（arXiv 2025）和 **VisionReward**（arXiv 2024）进一步引入视觉语言模型（VLM）进行多维度评估，但这些方法的共同瓶颈在于：它们均将空间一致性隐式地融入整体评分，缺乏对物体定位、方向、深度顺序等细粒度空间关系的显式验证机制。

SpatialReward 的核心区分点在于将**可验证奖励**（verifiable reward）范式从逻辑推理领域迁移到视觉空间评估。与上述基线模型依赖端到端黑盒评分不同，SpatialReward 通过三阶段管道——提示分解、专家检测、链式推理——将空间一致性拆解为可独立验证的原子约束，使奖励信号具有可解释性和可审计性。这一设计直接回应了现有方法的根本缺陷：全局评分器可能在空间错误样本上给出与正确样本相近的分数，导致 RL 训练无法有效纠正空间偏差。

### 技术谱系中的继承与创新

SpatialReward 的方法论可以追溯到三个技术传统：

1. **结构化提示解析**：Prompt Decomposer 将自由形式提示映射为结构化约束集 $\mathcal{C} = \mathcal{D}(P) = (\mathrm{tag}, \mathcal{C}_{\mathrm{inc}}, \mathcal{C}_{\mathrm{exc}})$，这一思路继承了视觉问答和场景图中实体-关系抽取的技术路线，但将其适配到 T2I 奖励建模的特定需求——不仅提取“有什么”，还提取“不应有什么”（排除约束），这是现有奖励模型普遍缺失的能力。消融实验证实，移除排除约束后 SpatRelBench 准确率从 37.1% 降至 25.9%，表明负约束信号对空间一致性训练至关重要。

2. **专家检测器集成**：SpatialReward 在奖励计算中引入目标检测、颜色分类、方向估计、深度估计和 OCR 等专家模型，作为 VLM 推理的视觉证据锚点。这一设计借鉴了组合式视觉推理（compositional visual reasoning）的理念，但将其定位从“最终判断者”转变为“证据提供者”。消融实验的强证据表明，移除专家检测阶段导致 GenEval 准确率从 95.2% 骤降至 70.3%，说明纯 VLM 推理在没有精确视觉接地的情况下极易产生幻觉。

3. **链式推理奖励聚合**：SpatialReward 采用 Qwen2.5-VL 作为推理骨干，基于检测证据进行逐步空间关系推理，最终通过 $\mathcal{R}_{\mathrm{spatial}} = \mathcal{P}_{\mathrm{score}} \left( \mathcal{F}_{\mathrm{vlm}} ( P_{\mathrm{CoT}}(r, B_A, B_B, \mathrm{attributes}) ) \right)$ 解析出空间一致性奖励。这一设计将 VLM 的角色从“端到端评分器”重新定义为“证据驱动的推理器”，与 VisionReward 等直接使用 VLM 输出的方法形成鲜明对比。去除链式推理使 SpatRelBench 准确率从 37.1% 降至 27.9%，证实推理过程本身对复杂空间关系判断具有不可替代的价值。

### 适用边界与限制条件

SpatialReward 的有效性受以下边界条件约束：

**外部检测模型依赖**：方法的奖励质量高度依赖目标检测、OCR、深度估计等专家模型的准确性。若检测模型对特定类别（如稀有物体）或极端视角表现不佳，可能导致错误的奖励信号传播至 RL 训练。论文未对检测模型在不同类别上的性能差异进行系统分析，这一限制的实际影响需要进一步量化。

**计算开销**：三阶段管道（提示分解 + 多专家检测 + VLM 推理）显著增加了每次奖励计算的开销。在 Flow-GRPO 框架中，每组 24 个样本均需完整的 SpatialReward 评估，这使得该方法在实时或资源受限场景中的适用性受限。论文未报告具体的推理延迟数据。

**基准覆盖范围**：SpatRelBench 主要覆盖 COCO-80、ImageNet-1k 和 Objects365 等常见物体类别及部分空间关系类型。对于高度抽象的空间描述（如“物体 A 隐约在物体 B 后方”）、艺术化构图或超现实场景，当前分解与验证机制的有效性可能下降。这一限制在论文的开放问题中被明确提及。

**美学质量的轻微折损**：在通用质量指标上，SpatialReward 训练的模型在 Aesthetic 评分上出现轻微下降（SD3.5-M 上从 5.39 降至 5.23），提示细粒度空间约束的强化可能在一定程度上压缩了模型的美学探索空间。

### 开放问题与未来方向

SpatialReward 的工作为以下研究问题打开了空间：

1. **内生空间推理**：当前方法依赖外部奖励模型提供空间反馈，是否可以将可验证空间推理机制直接嵌入生成模型内部（如通过空间注意力约束或结构化潜变量），从而无需外部奖励模型即可实现空间一致性？这将从根本上消除检测模型依赖带来的级联误差风险。

2. **跨模态泛化**：SpatialReward 的空间验证框架是否适用于视频生成中的时空一致性评估、3D 场景生成中的深度关系验证，或布局到图像生成中的精确位置控制？论文未对此进行探索。

3. **抽象空间描述的鲁棒性**：面对“在晨雾中隐约可见的城堡”、“混乱中透出秩序”等高度抽象或主观的空间描述，当前基于检测和规则的验证机制可能失效。如何扩展可验证奖励范式以覆盖语义模糊的空间约束，是一个值得深入的方向。

4. **与人类判断的对齐上限**：尽管 SpatialReward 在人类空间判断相关性上达到 Spearman ρ = 0.63，为对比模型中的最高值，但这一数值仍表明存在可观的未解释方差。进一步分析人类空间判断中不可建模的成分（如文化背景、个人偏好）将有助于设定自动化评估的合理期望上限。

## 原文 PDF

![[paperPDFs/CVPR_2026/SpatialReward_Verifiable_Spatial_Reward_Modeling_for_Fine_Grained_Spatial_Consistency_in_Text_to_Image_Generation.pdf]]