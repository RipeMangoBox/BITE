---
title: "RoadSceneBench: A Lightweight Benchmark for Mid-Level Road Scene Understanding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RoadSceneBench_A_Lightweight_Benchmark_for_Mid_Level_Road_Scene_Understanding.pdf
project_link: null
code_link: "https://github.com/XiyanLiu/RoadSceneBench"
aliases:
- RoadSceneBench
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 提出 MapVLM 框架及其核心的层次化关系奖励传播与时序一致性训练机制（HRRP-T），将 VLM 的推理过程建模为结构化决策序列，通过帧级层次奖励（场景层/关系层/语义层）和时序一致性奖励（平滑性+语义合理性）进行强化学习，迫使模型内化道路几何逻辑和时序平滑性。
primary_logic: 通过将中级道路语义定义为结构相互依赖的推理任务，并利用层次化奖励信号与时序约束联合优化，可以将 VLM 从静态预测器升级为几何感知且时序连贯的道路场景推理代理，从而可靠地填补感知与规划之间的语义鸿沟。
claims:
- "MapVLM 在 RoadSceneBench 上取得 Overall Precision 75.78% 和 Recall 72.17%，大幅超越最强基线 Gemini 2.5 Pro (P:60.61%, R:52.70%)，且在 Ego-lane Index 和 Lane Change Feasibility 等最困难任务上表现优异。"
- 引入 HRRP-T 后，Ego-lane Index 准确率从 SFT 的 69.34% 提升至 75.44%，召回率从 50.37% 猛增至 84.67%，证明了层次化时序奖励对结构化推理困难任务的有效性。
- 在遮挡场景下，SFT+HRRP-T 能够利用时序证据保持车道数和自车车道预测的一致性，而仅 SFT 的模型则出现逐帧漂移，直观展示了时序一致性奖励的作用。
- RoadSceneBench 上 Overall Precision = 75.78
---

# RoadSceneBench: A Lightweight Benchmark for Mid-Level Road Scene Understanding

> [!tip] 核心洞察
> 通过将中级道路语义定义为结构相互依赖的推理任务，并利用层次化奖励信号与时序约束联合优化，可以将 VLM 从静态预测器升级为几何感知且时序连贯的道路场景推理代理，从而可靠地填补感知与规划之间的语义鸿沟。

| 字段 | 内容 |
|------|------|
| 中文题名 | RoadSceneBench：面向中层级道路场景理解的轻量级基准 |
| 英文题名 | RoadSceneBench: A Lightweight Benchmark for Mid-Level Road Scene Understanding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.22466) · [Code](https://github.com/XiyanLiu/RoadSceneBench) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | MapVLM |
| Dataset | RoadSceneBench |

> [!tip] 效果简介
> - RoadSceneBench 上，Overall Precision 75.78 vs 60.61 (Gemini 2.5 Pro) (+15.17)；Overall Recall 72.17 vs 52.70 (Gemini 2.5 Pro) (+19.47)；Ego-lane Index Accuracy (SFT vs SFT+HRRP-T) 75.44 (SFT+HRRP-T) vs 69.34 (SFT) (+6.10)。

## 概述

当前自动驾驶场景理解基准主要面向检测、分割等低级感知任务，缺乏对车道拓扑、换道可行性等**中级道路语义**的结构化推理与一致性评估。这一断层导致视觉语言模型（VLM）难以将感知结果可靠地桥接至决策规划，成为制约端到端自动驾驶系统鲁棒性的关键瓶颈。

为此，本文提出 **MapVLM**——一个面向中级道路场景理解的 VLM 训练框架。其核心在于**层次化关系奖励传播与时序一致性机制（HRRP-T）**：将 VLM 的推理过程建模为结构化决策序列，通过帧级层次奖励（场景层/关系层/语义层）和时序一致性奖励（平滑性+语义合理性）进行强化学习，迫使模型内化道路几何逻辑与时序平滑性。该框架将 VLM 从静态预测器升级为几何感知且时序连贯的道路场景推理代理。

同时，本文构建了 **RoadSceneBench**——首个专为中级道路语义设计的轻量级基准，覆盖场景级、关系级和语义级多帧推理任务。

实验结果表明，MapVLM 在 RoadSceneBench 上取得 **Overall Precision 75.78%** 和 **Recall 72.17%**，大幅超越最强基线 Gemini 2.5 Pro（Precision 60.61%, Recall 52.70%）。消融实验进一步揭示，HRRP-T 使最困难的 Ego-lane Index 任务召回率从 50.37% 跃升至 84.67%，并在遮挡场景下展现出显著的时序一致性优势。

> **需注意**：基准数据仅采集自中国境内 20 个城市，对境外道路结构的泛化性有待验证；HRRP-T 当前仅针对短期（5 帧）时序建模，对突发动态事件的适应能力尚未测试。

## 背景与动机

自动驾驶场景理解的研究长期聚焦于低级感知任务，如目标检测、语义分割和车道线检测。现有基准（如 nuScenes、Waymo Open Dataset）提供了丰富的感知标注，但几乎不涉及中级道路语义的结构化推理——例如车道拓扑关系、自车车道索引、换道可行性判断以及交通标志与车道的关联。这种评估体系的偏斜导致两个后果：其一，视觉语言模型（VLM）在道路场景上的能力被低估或误判，因为通用 VQA 基准无法揭示其几何推理与关系推理的深层缺陷；其二，感知模块的输出难以可靠地桥接至决策规划，形成从“看见”到“理解”的语义鸿沟。

RoadSceneBench 正是针对这一缺口提出的轻量级基准。它覆盖 20 个中国城市、9 种道路类型和 6 种交通密度，为每帧图像提供场景级、关系级和语义级三层标注，并引入多帧序列以考察时序一致性。基准的核心设计理念是：中级道路语义具有天然的结构相互依赖性——车道数、自车位置、换道可行性等任务共享底层几何约束，孤立评估将掩盖模型是否真正内化了道路逻辑。

在此基准上，现有 VLM 暴露出显著瓶颈。即便是最强的闭源模型 **Gemini 2.5 Pro**，在 RoadSceneBench 上的整体精确率仅为 60.61%、召回率 52.70%；开源模型如 **Qwen2.5-VL-3B**、**DeepSeek-VL2** 和 **InternVL3** 表现更弱。定性分析显示，这些模型的错误并非随机噪声，而是系统性地违反道路几何约束——例如在遮挡场景下车道数预测逐帧漂移，或在匝道入口处混淆自车车道索引。这表明，仅靠大规模预训练和静态监督微调（SFT）无法迫使模型习得道路场景的结构化推理能力。

本文的动机由此明确：需要一种训练范式，将 VLM 从单帧静态预测器升级为几何感知且时序连贯的道路场景推理代理。核心思路是将推理过程建模为结构化决策序列，并通过层次化奖励信号与时序一致性约束进行强化学习优化，从而填补感知与规划之间的语义鸿沟。

## 核心创新

MapVLM 的核心创新并非引入新的视觉编码器或语言模型架构，而是将视觉‑语言模型（VLM）对中级道路场景的理解，重新定义为一个**结构相互依赖、时序受约束的推理问题**，并通过一套专门的强化学习训练范式来求解。相较于现有 VLM 仅对单帧图像进行静态预测的常规范式，MapVLM 的关键突破体现在以下三个维度。

### 1. 训练范式：从监督微调到层次化时序强化学习

现有 VLM 基线（如 **Qwen2.5‑VL‑7B**、**GPT‑4o**、**Gemini 2.5 Pro**）在道路场景理解上，通常仅依赖监督微调（SFT）或上下文提示，优化目标为逐 token 的交叉熵损失。这使模型只能学习单帧图像到文本的映射，无法内化道路语义中固有的几何逻辑和时序平滑性。

MapVLM 将训练范式升级为 **SFT + 层次化关系奖励传播与时序一致性（HRRP‑T）强化学习**。其核心思路是：将 VLM 的推理过程建模为一个结构化决策序列，在 SFT 建立基础推理能力后，通过 GRPO 策略优化一个精心设计的奖励函数，迫使模型在强化学习阶段内化道路场景的几何约束和时序连贯性。

### 2. 优化目标：层次化奖励信号替代逐 Token 损失

HRRP‑T 的奖励函数是 MapVLM 最关键的因果调节旋钮。与基线方法单一的交叉熵损失不同，HRRP‑T 构建了一个三层级、双维度的奖励体系：

- **帧级层次奖励**（公式 1）：
  $$\mathcal{R}_{frame}^{t} = \alpha R_{sce}^{t} + \beta \mathcal{R}_{rel}^{t} + \gamma \mathcal{R}_{sem}^{t}$$
  其中 $R_{sce}^{t}$、$\mathcal{R}_{rel}^{t}$、$\mathcal{R}_{sem}^{t}$ 分别对第 $t$ 帧的场景层（如车道数）、关系层（如自车车道索引）和语义层（如换道可行性）预测进行独立评估，通过超参数 $\alpha, \beta, \gamma$ 加权组合。这种分层设计使模型必须同时满足从几何拓扑到语义决策的多粒度一致性，而非仅追求表面正确的文本输出。

- **时序级奖励**（公式 2）：
  $$\mathcal{R}_{temporal} = \lambda \mathcal{R}_{smooth} + (1 - \lambda) \mathcal{R}_{plausible}$$
  其中平滑性奖励 $\mathcal{R}_{smooth}$（公式 3）惩罚相邻帧预测值的突变，语义合理性奖励 $\mathcal{R}_{plausible}$（公式 4）统计时序上语义过渡合理的帧对比例。二者联合约束模型在多帧序列上保持连贯推理。

最终训练目标（公式 5）为帧级与时序奖励的加权组合：
$$\mathcal{R}_{\mathrm{HRRP-T}} = \lambda_{frame} \frac{1}{T} \sum_{t=1}^{T} \mathcal{R}_{frame}^{t} + \lambda_{temporal} \mathcal{R}_{temporal}$$

这一奖励设计直接驱动了 MapVLM 在困难任务上的性能跃升——Ego‑lane Index 的召回率从 SFT 的 50.37% 猛增至 84.67%，准确率从 69.34% 提升至 75.44%，证明了层次化时序奖励对结构化推理中漏检和歧义问题的有效缓解。

### 3. 推理时域范围：从单帧快照到多帧联合推理

基线 VLM 的推理基于单帧图像，面对遮挡或歧义场景时只能逐帧独立猜测，容易产生预测漂移。MapVLM 通过 HRRP‑T 显式引入了**多帧序列联合推理**的能力——在训练阶段，模型被要求对短时序片段（5 帧）同时输出预测，并接受时序一致性奖励的约束。这使得模型学会利用时序证据（如前几帧清晰的车道布局）来稳定后续被遮挡帧的预测。定性实验直观展示了这一机制：在拥堵城市场景中，SFT+HRRP‑T 能够保持车道数和自车车道预测的连贯性，而仅 SFT 的模型则出现逐帧漂移。

综上，MapVLM 的创新本质在于**将 VLM 从静态预测器升级为几何感知且时序连贯的道路场景推理代理**，其 changed slots 清晰聚焦于训练范式、优化目标和推理时域范围三个相互耦合的维度，从而可靠地填补了感知与规划之间的中级语义鸿沟。

## 整体框架

MapVLM 的整体训练范式采用两阶段流水线：**监督微调（SFT）** 建立基础推理能力，随后通过 **层次化关系奖励传播与时序一致性（HRRP-T）** 强化学习框架对模型进行结构化对齐。该流水线的核心设计动机在于：现有 VLM 在静态单帧推理中缺乏对道路几何逻辑的内化，且无法利用跨帧时序证据维持预测一致性。

### 两阶段训练流水线

**第一阶段：监督微调。** 以 Qwen2.5-VL-7B 为基座模型，通过 LoRA 进行参数高效微调。输入为高分辨率道路图像，输出为覆盖场景级、关系级和语义级的中层结构化推理答案。该阶段使模型获得对 RoadSceneBench 任务格式和基础语义的初始对齐能力。

**第二阶段：HRRP-T 强化学习。** 在 SFT 模型基础上，引入层次化奖励信号和时序约束，通过 GRPO 策略进行自批判式强化学习优化。与 SFT 仅依赖逐 token 交叉熵损失不同，HRRP-T 将推理过程建模为结构化决策序列，迫使模型内化道路拓扑逻辑并维持跨帧预测的时序平滑性。

### 奖励模块的核心结构

HRRP-T 的奖励信号由两个互补维度构成：

- **帧级层次奖励** $\mathcal{R}_{frame}^{t}$：对第 $t$ 帧的推理结果进行三层评估——场景层（如车道数）、关系层（如自车车道索引）和语义层（如换道可行性），加权组合为 $\mathcal{R}_{frame}^{t} = \alpha R_{sce}^{t} + \beta \mathcal{R}_{rel}^{t} + \gamma \mathcal{R}_{sem}^{t}$。

- **时序级奖励** $\mathcal{R}_{temporal}$：对连续帧序列的预测进行跨帧约束，包含平滑性奖励 $\mathcal{R}_{smooth}$（惩罚相邻帧预测值的突变）和语义合理性奖励 $\mathcal{R}_{plausible}$（统计时序上语义过渡合理的帧对比例），加权组合为 $\mathcal{R}_{temporal} = \lambda \mathcal{R}_{smooth} + (1 - \lambda) \mathcal{R}_{plausible}$。

最终训练目标为两者的联合优化：

$$\mathcal{R}_{\mathrm{HRRP-T}} = \lambda_{frame} \frac{1}{T} \sum_{t=1}^{T} \mathcal{R}_{frame}^{t} + \lambda_{temporal} \mathcal{R}_{temporal}$$

### 推理时的输入输出流

推理阶段，模型接收多帧道路图像序列（典型长度为 5 帧），通过 Qwen2.5-VL 的视觉编码器提取特征，语言模型基于结构化查询生成中层语义推理结果。与基线 VLM 的单帧静态推理不同，MapVLM 经 HRRP-T 训练后能够利用时序证据维持预测的几何一致性和语义连贯性——这一能力在遮挡场景下尤为关键：如图 5 所示，当后三帧因拥堵导致车道线被部分遮挡时，SFT+HRRP-T 能够基于前两帧的清晰观测维持五车道拓扑和自车车道索引的一致性，而仅经 SFT 的模型则出现逐帧漂移。

### 模块关系总结

整个框架的模块依赖关系为：视觉编码器和语言模型构成推理主干，LoRA 适配器提供参数高效的领域适配，HRRP-T 奖励模块作为外部优化信号驱动模型从“静态预测器”向“几何感知且时序连贯的道路场景推理代理”升级。该设计的关键因果机制在于：层次化奖励迫使模型关注结构化推理的正确性，而时序一致性奖励则通过跨帧约束抑制单帧歧义带来的预测漂移，二者协同作用使得模型在 Ego-lane Index 等最困难任务上取得显著提升（准确率从 69.34% 提升至 75.44%，召回率从 50.37% 猛增至 84.67%）。

### 补充图表

![[assets/figures/papers/paper_list_l2721_https_arxiv_org_abs_2511_22466/figures/008_Figure_3.jpg]]
*Figure 3: Framework of dataset construction and MapVLM*

![[assets/figures/papers/paper_list_l2721_https_arxiv_org_abs_2511_22466/figures/001_Figure_1.jpg]]
*Figure 1: Overview of RoadSceneBench. The benchmark spans Scene-, Relational-, and Semantic-level tasks with multi-frame reasoning. Furthermore, we benchmark various open- and closed-source models*

## 核心模块与公式推导

MapVLM 的核心方法论由两阶段训练范式构成：**监督微调 (SFT)** 建立基础推理能力，随后通过 **层次化关系奖励传播与时序一致性 (HRRP-T)** 强化学习框架对模型进行结构化对齐。以下聚焦 HRRP-T 的关键模块与数学形式。

### 1. 基础模型与监督微调

MapVLM 以 **Qwen2.5-VL-7B** 为基座模型，采用 **LoRA** 进行参数高效微调，使 VLM 初步具备中级道路语义的结构化输出能力。此阶段使用逐 token 交叉熵损失，为后续强化学习提供初始化策略。

### 2. HRRP-T 奖励框架

HRRP-T 将道路场景推理建模为结构化决策序列，通过 **帧级层次奖励** 和 **时序一致性奖励** 的加权组合，利用 **GRPO** 策略进行自批判式强化学习优化。其核心奖励结构如下：

#### 2.1 帧级层次奖励

对于第 $t$ 帧，帧级奖励定义为场景层、关系层和语义层奖励的加权和：

$$\mathcal{R}_{frame}^{t} = \alpha R_{sce}^{t} + \beta \mathcal{R}_{rel}^{t} + \gamma \mathcal{R}_{sem}^{t}$$

其中：
- $R_{sce}^{t}$：场景层奖励，评估车道数、道路类型等全局属性的预测准确性；
- $\mathcal{R}_{rel}^{t}$：关系层奖励，评估自车车道索引、车道拓扑等结构关系；
- $\mathcal{R}_{sem}^{t}$：语义层奖励，评估换道可行性等高层决策语义；
- $\alpha, \beta, \gamma$ 为平衡各层重要性的超参数。

该设计将单帧推理分解为从粗到细的层次化评估，迫使模型内化道路几何逻辑，而非仅拟合表面文本模式。

#### 2.2 时序一致性奖励

时序奖励由平滑性奖励和语义合理性奖励组合而成：

$$\mathcal{R}_{temporal} = \lambda \mathcal{R}_{smooth} + (1 - \lambda) \mathcal{R}_{plausible}$$

**平滑性奖励** 惩罚相邻帧预测值的突变：

$$\mathcal{R}_{smooth} = 1 - \frac{1}{T - 1} \sum_{t=1}^{T-1} |y_t - y_{t-1}|$$

其中 $y_t$ 为第 $t$ 帧的预测值，$T$ 为序列帧数。该奖励鼓励相邻帧输出平滑过渡，抑制因局部遮挡或歧义导致的逐帧漂移。

**语义合理性奖励** 统计时序上语义过渡合法的帧对比例：

$$\mathcal{R}_{plausible} = \frac{1}{T - 1} \sum_{t=1}^{T-1} \mathbb{I}(\mathbf{V}(y_t, y_{t+1}))$$

其中 $\mathbb{I}(\cdot)$ 为指示函数，$\mathbf{V}(y_t, y_{t+1})$ 判断从 $y_t$ 到 $y_{t+1}$ 的语义状态转移是否符合道路逻辑（例如，换道可行性不应在无变道条件下频繁切换）。该奖励引入先验知识约束，防止模型生成物理上不可能的时序推理链。

#### 2.3 总奖励函数

HRRP-T 训练的最终奖励为帧级奖励均值与时序奖励的加权组合：

$$\mathcal{R}_{\mathrm{HRRP-T}} = \lambda_{frame} \frac{1}{T} \sum_{t=1}^{T} \mathcal{R}_{frame}^{t} + \lambda_{temporal} \mathcal{R}_{temporal}$$

其中 $\lambda_{frame}$ 和 $\lambda_{temporal}$ 控制单帧准确性与时序一致性的权衡。该复合奖励通过 GRPO 策略优化模型参数，使 VLM 从静态预测器升级为几何感知且时序连贯的道路场景推理代理。

### 3. 关键设计动机

HRRP-T 的因果调节机制在于：**层次化奖励传播** 将结构化推理的压力从单一 token 级损失解耦为多粒度语义评估，而 **时序一致性约束** 则利用相邻帧的冗余信息作为自监督信号，缓解遮挡和歧义场景下的推理退化。消融实验表明，引入 HRRP-T 后 Ego-lane Index 召回率从 50.37% 跃升至 84.67%，验证了时序一致性信号对结构化困难任务的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l2721_https_arxiv_org_abs_2511_22466/figures/011_Figure_5.jpg]]
*Figure 5: Comparison of SFT and SFT+HRRP-T on a 5-frame congested urban scene. The ego vehicle stays in the same lane: the first two frames clearly show a five-lane layout, whereas the last three frames are partially occluded. SFT reacts to these ambiguous observations with frame-wise drift in lane count and ego-lane index. SFT+HRRP-T leverages temporal evidence and preserves consistent ego-lane predictions with a coherent five-lane topology*

## 实验与分析

### 核心瓶颈与验证逻辑

当前自动驾驶场景理解基准主要面向检测、分割等低级感知任务，忽略了车道拓扑、换道可行性等中级道路语义的结构化推理与一致性评估需求。本实验的核心验证逻辑是：**MapVLM 框架通过层次化关系奖励传播与时序一致性训练机制 (HRRP-T)，能否将 VLM 从静态预测器升级为几何感知且时序连贯的道路场景推理代理**，从而在 RoadSceneBench 上可靠地填补感知与规划之间的语义鸿沟。

### 主实验结果

Table 2 给出了 MapVLM 与多个闭源/开源 VLM 在 RoadSceneBench 上的全面定量对比。MapVLM (SFT+HRRP-T) 取得 **Overall Precision 75.78%** 和 **Recall 72.17%**，大幅超越表现最强的闭源基线 Gemini 2.5 Pro（P: 60.61%, R: 52.70%），精度提升 **+15.17 个百分点**，召回率提升 **+19.47 个百分点**。

![[assets/figures/papers/paper_list_l2721_https_arxiv_org_abs_2511_22466/figures/009_Table_2.jpg]]
*Table 2: Quantitative comparison of baseline VLMs (closed- and open-source) against our MapVLM on the RoadSceneBench*

| 模型 | Overall Precision | Overall Recall |
|------|-------------------|----------------|
| Gemini 2.5 Pro（最强闭源基线） | 60.61% | 52.70% |
| GPT-4o | — | — |
| Qwen2.5-VL-3B | — | — |
| Qwen3-VL | — | — |
| DeepSeek-VL2 | — | — |
| InternVL3 | — | — |
| **MapVLM (SFT+HRRP-T)** | **75.78%** | **72.17%** |

值得注意的是，MapVLM 在 **Ego-lane Index** 和 **Lane Change Feasibility** 这两项被识别为最困难的任务上表现尤为突出。这两类任务要求模型同时理解自车与道路结构的空间关系以及动态可行性约束，属于典型的结构化推理瓶颈。MapVLM 在该类任务上的优势直接验证了 HRRP-T 中层次化奖励设计（场景层/关系层/语义层）对结构化语义内化的有效性。

### 消融实验：HRRP-T 的因果贡献

消融分析聚焦于 SFT 基线（仅监督微调的 Qwen2.5-VL-7B）与 SFT+HRRP-T 在 Ego-lane Index 任务上的对比，该任务是 RoadSceneBench 中最具挑战性的子任务之一。

- **SFT 基线**：Ego-lane Index Accuracy 69.34%，Recall 50.37%
- **SFT+HRRP-T**：Ego-lane Index Accuracy **75.44%** (+6.10)，Recall **84.67%** (+34.30)

召回率从 50.37% 到 84.67% 的跃升（**+34.30 个百分点**）是本次消融最关键的因果信号。这表明 SFT 模型在遮挡、歧义等困难场景下存在严重漏检——模型倾向于“不确定就不回答”，而 HRRP-T 的时序一致性奖励（平滑性奖励 $\mathcal{R}_{smooth}$ 和语义合理性奖励 $\mathcal{R}_{plausible}$）通过跨帧证据积累，迫使模型在单帧信息不足时仍能给出连贯的结构化预测。

### 时序一致性奖励的失效模式分析

Figure 5 展示了 SFT 与 SFT+HRRP-T 在一个 5 帧拥堵城市场景中的定性对比，该场景中自车保持在同一车道，但后三帧存在部分遮挡。这一对比揭示了两种典型的失效模式：

1. **SFT 的逐帧漂移失效**：SFT 模型对遮挡帧的歧义观测产生逐帧响应漂移，表现为车道数预测和自车车道索引的帧间不一致。这说明纯 SFT 模型缺乏对时序上下文的内部建模能力，每一帧被独立处理，无法利用前帧的清晰观测来约束后帧的歧义推理。

2. **SFT+HRRP-T 的时序证据利用**：加入 HRRP-T 后，模型能够利用前两帧清晰的五车道布局信息，在遮挡帧中保持连贯的自车车道预测和五车道拓扑结构。这直接验证了 HRRP-T 的时序奖励设计——平滑性奖励 $\mathcal{R}_{smooth} = 1 - \frac{1}{T-1}\sum_{t=1}^{T-1}|y_t - y_{t-1}|$ 抑制帧间预测突变，语义合理性奖励 $\mathcal{R}_{plausible}$ 约束相邻帧的语义过渡符合道路逻辑——在遮挡场景下的因果作用。

### 挑战性场景的定性分析

Figure 4 展示了 RoadSceneBench 中多个代表性挑战场景及模型预测对比（红色标注错误）。这些案例覆盖了复杂路口拓扑、多车道分合流、部分遮挡等真实驾驶中的困难情境，进一步印证了：

![[assets/figures/papers/paper_list_l2721_https_arxiv_org_abs_2511_22466/figures/010_Figure_4.jpg]]
*Figure 4: Visualization of representative cases from RoadSceneBench that highlight the complexities of real-world driving scenarios. Red text indicates prediction errors, underscoring both the benchmark’s difficulty and the superior reasoning of our model*

- 闭源大模型（如 Gemini 2.5 Pro）虽在通用 VLM 任务上表现强劲，但在需要精确几何理解和结构化关系推理的中级道路语义任务上存在系统性短板；
- MapVLM 通过 HRRP-T 的层次化奖励信号，在关系层（如车道拓扑）和语义层（如换道可行性）上展现出更强的结构化推理能力。

### 公平性说明与泛化局限

实验中对比了多种闭源和开源 VLM，训练设置统一，但需注意以下限制：

1. **部分基线调用细节未完全公开**：闭源模型（Gemini 2.5 Pro、GPT-4o）的内部推理机制和可能的提示工程优化无法完全对齐，实际性能差距可能受调用方式影响。
2. **数据地理偏差**：RoadSceneBench 数据采集仅限中国境内 20 个城市，道路结构、标线样式和交通规则可能与其他国家/地区存在差异，MapVLM 在境外场景的泛化性有待独立验证。
3. **时序建模范围有限**：HRRP-T 当前仅针对短期（5 帧）时序一致性设计，对于突发道路施工、交通事故等需要更长时序依赖的动态事件，其建模能力尚未测试。

### 补充图表

![[assets/figures/papers/paper_list_l2721_https_arxiv_org_abs_2511_22466/figures/002_Table_1.jpg]]
*Table 1: Comparison of autonomous driving scene benchmarks. RoadSceneBench uniquely provides self-collected data with per-frame mid-level semantics, bridging the gap between low-level perception and high-level reasoning*

![[assets/figures/papers/paper_list_l2721_https_arxiv_org_abs_2511_22466/figures/007_Figure_2.jpg]]
*Figure 2: Visualization of representative annotation types in RoadSceneBench. All examples highlight the mid-level semantics connecting perception and structural reasoning*

![[assets/figures/papers/paper_list_l2721_https_arxiv_org_abs_2511_22466/figures/016_Figure_6.jpg]]
*Figure 6: Examples of RoadSceneBench. Each row displays the images contained in a clip along with their corresponding annotation information*

## 方法谱系与知识库定位

### 任务谱系：从低级感知到中级语义的结构化推理

当前自动驾驶场景理解的主流基准（如 nuScenes、Waymo Open Dataset）主要围绕**目标检测、语义分割、跟踪**等低级感知任务设计，评估指标以 mAP、IoU 为主。这些基准虽推动了感知模型的进步，却系统性地忽略了一个关键瓶颈：**低级感知结果如何可靠地桥接至决策规划所需的中级道路语义**——例如车道拓扑结构、自车车道索引、换道可行性判断等。

RoadSceneBench 的定位正是填补这一空白。如 Table 1 所示，该基准与现有自动驾驶数据集的根本差异在于：它提供**逐帧标注的中级语义标签**，涵盖场景级（道路类型、交通状况）、关系级（车道数、自车车道索引）和语义级（换道可行性、驾驶场景）三层结构，并要求模型在**多帧序列**上进行联合推理。这种设计将评估重心从“看到了什么”转向“理解了什么结构”，使基准成为感知与规划之间的语义桥梁。

### 方法谱系：VLM 在道路场景推理中的进化路径

在 RoadSceneBench 上评估的基线模型构成了一个清晰的能力谱系：

**开源 VLM 基线**（Qwen2.5-VL-3B/7B、Qwen3-VL、DeepSeek-VL2、InternVL3）代表通用视觉语言模型在零样本或少样本设置下的道路语义推理能力。这些模型在场景级任务（如道路类型识别）上表现尚可，但在关系级和语义级任务上普遍乏力，暴露出**缺乏结构化道路几何推理能力**的根本缺陷。

**闭源 VLM 基线**（GPT-4o、Gemini 2.5 Pro）凭借更大的模型规模和更强的指令遵循能力，整体表现显著优于开源基线。其中 Gemini 2.5 Pro 取得 Overall Precision 60.61%、Recall 52.70%，成为最强基线。然而，其在 Ego-lane Index 和 Lane Change Feasibility 这两个最困难任务上的低 Precision 和 Recall（Table 2）表明，**即使是最先进的通用 VLM，也缺乏对道路拓扑结构和时序一致性的显式建模**。

**MapVLM** 的核心贡献在于，它不依赖更大的模型规模，而是通过**训练范式的根本转变**来弥补上述缺陷：将 VLM 的推理过程从单帧静态预测升级为**结构化决策序列的强化学习**。具体而言，MapVLM 在 SFT 基础上引入 HRRP-T 框架，通过三层层次化奖励（场景层、关系层、语义层）和时序一致性奖励（平滑性 + 语义合理性）联合优化，迫使模型内化道路几何逻辑和时序平滑性。这一范式转变的本质是：**将道路语义推理从“模式匹配”提升为“约束满足”**——模型不仅需要输出正确答案，还需要满足帧内拓扑一致性和帧间时序连贯性的结构化约束。

### 与相关工作的横向对比

MapVLM 的 HRRP-T 框架与以下研究方向形成对话：

- **强化学习驱动的 VLM 对齐**：与 RLHF 类方法（如 InstructGPT）不同，HRRP-T 的奖励信号并非来自人类偏好标注，而是**自动从结构化标注中传播**——场景层奖励检查全局属性，关系层奖励验证拓扑约束，语义层奖励评估推理合理性。这种可自动计算的层次化奖励设计，使得大规模强化学习训练无需昂贵的人工反馈。

- **时序一致性建模**：与视频理解中的时序平滑约束（如光流一致性损失）不同，HRRP-T 的时序奖励同时包含**平滑性**（鼓励相邻帧预测值连续变化）和**语义合理性**（统计时序上语义过渡合理的帧对比例），后者是专门为道路场景中离散语义状态（如车道数突变、换道状态切换）设计的，避免了盲目平滑导致的语义错误。

- **参数高效微调**：MapVLM 基于 Qwen2.5-VL-7B 并使用 LoRA 适配器，保持了轻量级部署的可行性。这与当前“大模型 + 全参数微调”的主流路线形成对比，证明了**在特定领域通过结构化奖励设计，小模型可以达到甚至超越大模型的效果**。

### 适用边界与局限性

尽管 MapVLM 在 RoadSceneBench 上取得了显著优势，其适用边界和局限值得明确：

1. **地理泛化性未验证**：RoadSceneBench 的数据采集仅覆盖中国境内 20 个城市，道路结构、标线样式和交通规则可能与其他国家或地区存在系统性差异。模型对境外道路场景的泛化能力需要独立验证。

2. **时序建模范围有限**：HRRP-T 当前针对短期（5 帧）时序一致性设计，对于更长期的动态事件（如突发道路施工、交通事故导致的临时改道）的建模能力尚未测试。奖励函数中的平滑性假设在突变场景下可能反而成为约束过强的先验。

3. **任务覆盖的边界**：基准目前聚焦于道路拓扑和自车状态的中级语义，尚未扩展到物体级定位和交互层面推理（如车辆-行人交互意图、多智能体轨迹预测）。这些任务可能引入额外的结构化约束，需要扩展层次化奖励的设计空间。

### 开放问题

基于上述分析，以下问题值得进一步探索：

- **动态事件建模**：HRRP-T 如何处理动态道路事件（如短时施工或交通事故）带来的时序模式突变？是否需要在奖励函数中引入“突变检测”机制，允许模型在识别到场景剧变时自适应地放松平滑性约束？

- **基准扩展方向**：RoadSceneBench 是否能扩展以包含物体级定位和交互层面推理（如车辆-行人交互意图）？如果可以，层次化奖励结构需要如何调整以适应新的语义层级？

- **奖励权重的自动化**：当前 HRRP-T 中的 α、β、γ、λ 等超参数需要手动调节。是否存在基于任务难度或模型训练动态的自适应权重调整策略，以减少人工调参负担并提升训练效率？

- **跨域迁移**：MapVLM 在 RoadSceneBench 上学到的结构化推理能力，是否能迁移到其他需要拓扑推理的领域（如室内导航、机器人操作场景理解）？这需要构建跨域的中级语义基准来验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/RoadSceneBench_A_Lightweight_Benchmark_for_Mid_Level_Road_Scene_Understanding.pdf]]
