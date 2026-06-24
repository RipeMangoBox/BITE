---
title: "SVAG-Bench: A Large-Scale Benchmark for Multi-Instance Spatio-temporal Video Action Grounding"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/SVAG_Bench_A_Large_Scale_Benchmark_for_Multi_Instance_Spatio_temporal_Video_Action_Grounding.pdf
aliases:
- SVAG-Bench
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 时间优先门控策略（temporal-first gating）：先执行时间定位确定动作区间，再将空间跟踪限定在该窗口内，从而避免无关帧产生虚假轨迹。
primary_logic: 为衡量迈向具身智能的进展，需要统一时空多实例动作定位任务，并建立高密度、动作驱动的基准来暴露模型在组合推理上的系统性失败。
claims:
- SVAGFormer在所有数据集的联合时空指标m-HIoU上（13.52）大幅领先最佳专有LVLM GPT-5.4（10.78）和最佳开源模型EgoMask（5.25），显示了时间优先门控的优势。
- 现有的空间或时间专家模型均无法产生完整的m-HIoU分数，表明孤立子任务优化无法组合为统一时空推理。
- 所有LVLM在MOT20上的空间定位HOTA均为零（Table 28），证明当前视觉语言模型无法应对极长时和密集场景的空间跟踪。
- 使用预训练权重和增大记忆长度可显著提升空间关联准确度，验证了模型对时间记忆的依赖。
---

# SVAG-Bench: A Large-Scale Benchmark for Multi-Instance Spatio-temporal Video Action Grounding

> [!tip] 核心洞察
> 为衡量迈向具身智能的进展，需要统一时空多实例动作定位任务，并建立高密度、动作驱动的基准来暴露模型在组合推理上的系统性失败。

| 字段 | 内容 |
|------|------|
| 中文题名 | SVAG-Bench：大规模多实例时空视频动作定位基准 |
| 英文题名 | SVAG-Bench: A Large-Scale Benchmark for Multi-Instance Spatio-temporal Video Action Grounding |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2510.13016) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SVAGFormer |
| Dataset | SVAG-Bench, OVIS, MOT17, MOT20 |

> [!tip] 效果简介
> - SVAG-Bench (Overall) 上，m-HIoU 13.52 vs 10.78 (GPT-5.4) (+2.74)。
> - OVIS 上，HOTA 22.73 vs 11.63 (GPT-5.4) (+11.10)。
> - MOT17 上，HOTA 0.60 vs 0.09 (GPT-5.4) (+0.51)。

## 概述

**问题瓶颈**：现有视频理解模型在时空多实例动作定位上存在根本性推理鸿沟——空间定位与时间定位被孤立优化，无法在长时、密集、多行动者场景中联合推理。所有专有与开源大视觉语言模型（LVLM）在极长密集视频（MOT20）上的空间跟踪指标 HOTA 均为零（Table 28），直接暴露了当前视觉语言模型在组合时空推理上的系统性失败。

**核心思路**：SVAGFormer 提出**时间优先门控策略**（temporal-first gating），将时空联合定位分解为“先时间、后空间”的级联范式：先通过 FlashVTG 执行时间定位，确定动作发生的候选时间窗口；再将空间跟踪（TempRMOT）严格限定在该窗口内执行，从而避免无关帧产生虚假轨迹，从机制上抑制了全视频空间跟踪的噪声放大问题。

**任务定位**：SVAG 任务统一了空间视频定位（SVG）、时空视频定位（STVG）和视频时间定位（VTG）三个孤立范式，要求模型同时输出“哪些对象在何时执行了查询动作”的完整时空轨迹。SVAG-Bench 是该任务的大规模基准，基于 OVIS、MOT17、MOT20 三个多目标跟踪数据集构建，标注密度（28.47 queries/video, 14.22 tracks/video）和动作多样性（903 个不同动词）均显著优于已有基准（Table 1）。

**主要结果**：SVAGFormer 在统一时空指标 m-HIoU 上达到 13.52，领先最佳专有 LVLM **GPT-5.4**（OpenAI, 2026）的 10.78（+2.74），并大幅超越最佳开源模型 **EgoMask**（Liang et al., 2025）的 5.25（Table 2）。在空间跟踪子任务上，SVAGFormer 在 OVIS 上的 HOTA 为 22.73，而 GPT-5.4 仅为 11.63（+11.10）；在 MOT17 和 MOT20 上，所有 LVLM 的空间定位能力接近失效，SVAGFormer 分别以 0.60 和 0.43 的 HOTA 保持微弱但一致的优势。消融实验进一步证实，预训练权重和增大时间记忆长度可显著提升空间关联准确度（Table 10, Table 11），验证了模型对时间记忆的依赖。

**局限与挑战**：当前 SVAGFormer 采用模块化分离设计，缺乏端到端的联合推理；基准领域局限于城市、交通和动物监控，尚未覆盖具身交互场景；在 MOT20 等极端拥挤长时场景中，绝对性能仍接近零，距离实用水平存在根本性差距。

## 背景与动机

### 视频动作定位的范式演进与根本瓶颈

视频理解领域长期存在一个核心矛盾：**空间定位、时间定位与多实例推理被割裂为独立任务**，导致任何单一模型都无法回答“谁在何时何地执行了什么动作”这一完整查询。Figure 1 清晰地揭示了这一鸿沟：

- **空间视频定位 (SVG)** 仅关注目标对象的空间位置，完全缺失时间推理能力；
- **时空视频定位 (STVG)** 虽联合建模时空维度，但只能处理单个对象，无法应对多主体交互场景；
- **视频时间定位 (VTG)** 仅识别动作发生的时间段，却丢弃了空间位置信息。

现有的视频模型无法联合进行时空多实例的动作定位，尤其在长时、密集、多行动者的场景中，存在巨大的推理鸿沟。这一瓶颈直接阻碍了视频理解技术向具身智能等真实应用场景的迁移。

### 现有基准的覆盖盲区

Table 1 的系统对比揭示了当前基准数据集的结构性缺陷。尽管 VidSTG 拥有最大的总体规模，但其每视频查询数（2.72）和轨迹数（1.72）远低于实际需求。相比之下，**SVAG-Bench** 以每视频 28.47 个查询和 14.22 条轨迹的标注密度，以及 903 个独特动词的动作多样性，创造了首个高密度、动作驱动的多实例时空定位基准。这一设计直接回应了一个关键问题：现有基准的稀疏标注无法暴露模型在组合推理上的系统性失败。

### 本文动机与核心思路

为衡量迈向具身智能的进展，需要统一时空多实例动作定位任务，并建立高密度、动作驱动的基准来暴露模型在组合推理上的系统性失败。本文据此提出两个核心贡献：

1. **SVAG-Bench**：首个大规模多实例时空视频动作定位基准，整合 OVIS、MOT17 和 MOT20 三个多目标跟踪数据集，覆盖从短时多样（OVIS，平均 67.7 秒）到极长密集（MOT20，平均 2232.8 秒）的难度谱系。
2. **SVAGFormer**：采用**时间优先门控策略**的模块化基线——先执行时间定位确定动作区间，再将空间跟踪限定在该窗口内，从而避免无关帧产生虚假轨迹。这一设计选择直接回应了“孤立子任务优化无法组合为统一时空推理”的核心洞察。

## 核心创新

本工作的核心创新在于**任务定义与方法设计两个层面的根本性重构**，共同指向一个此前未被充分建模的瓶颈：长时、密集、多行动者场景下的联合时空推理。

### 任务层创新：从孤岛式定位到统一时空多实例接地

现有视频接地任务存在根本性的割裂（见 Figure 1）：空间视频接地（SVG）缺失时间推理，时空视频接地（STVG）无法处理多实例交互，视频时间接地（VTG）则完全忽略空间定位。这种割裂导致孤立优化的子任务无法组合为完整的时空推理能力——实验证据（Table 2）表明，空间专家模型（如 **DKGTrack**，Li et al., ICCV 2025；**TransRMOT**，Wu et al., CVPR 2023）和时间专家模型（如 **LD-DETR**，Zhao et al., 2025；**R²-Tuning**，Liu et al., ECCV 2024）均无法独立产生统一的 m-HIoU 分数，揭示了**子任务孤立优化的组合性失败**。

SVAG 任务将这一瓶颈显式化：给定自然语言动作查询，模型需同时回答“谁在执行动作”“在何处”“在何时”，并为所有满足条件的实例输出完整的时空轨迹。SVAG-Bench 作为首个支持该任务的大规模基准，在标注密度（每视频 28.47 个查询、14.22 条轨迹）和动作多样性（903 个不同动词）上均超越现有数据集（Table 1），为暴露模型的组合推理鸿沟提供了充分的压力测试。

### 方法层创新：时间优先门控策略

SVAGFormer 的核心设计选择是**时间优先门控策略**（temporal-first gating），这也是其相对于所有 baseline 的 changed slot（见 Figure 3）：

| 策略维度 | Baseline 做法 | SVAGFormer 做法 |
|---------|-------------|---------------|
| 时空集成顺序 | 在全视频上执行空间跟踪，再与时间定位结果合并；或独立输出空间和时间结果 | 先执行时间定位确定动作区间，再将空间跟踪限定在该窗口内 |

这一设计背后的因果机制清晰：在全视频上执行空间跟踪会引入大量无关帧的虚假轨迹，尤其在长时视频中，这些噪声轨迹会严重干扰后续的轨迹关联与匹配。时间优先门控通过将时间定位输出（来自 **FlashVTG** 的粗到细动作分段）作为门控信号，使空间跟踪模块（**TempRMOT**）仅在动作发生的窗口内运行，从根本上切断了无关帧产生虚假轨迹的路径。

消融实验为这一机制提供了有力的因果证据：
- 在 OVIS 上，SVAGFormer 的 HOTA 达到 22.73，而最佳专有 LVLM **GPT-5.4**（OpenAI, 2026）仅为 11.63，差距达 +11.10（Table 2）。
- 在极具挑战的 MOT20 长时密集场景上，所有 LVLM 的空间定位 HOTA 均为零（Table 28），而 SVAGFormer 通过时间优先门控仍可获得 0.43 的 HOTA，证明了该策略在极端条件下的鲁棒性优势。
- 预训练权重（TempRMOT 从 Refer-KITTI-V2 初始化）使 OVIS 上关联准确度 AssA 从 46.6 提升至 51.6（Table 10），增大时间记忆长度从 5 到 8 进一步将 HOTA 从 24.214 提升至 24.611（Table 11），表明时间窗口内的空间跟踪质量高度依赖时间上下文的充分建模。

### 创新边界与局限

需要指出，SVAGFormer 的模块化设计（FlashVTG + TempRMOT + 时间门控）虽然有效，但**时空模块分离**意味着信息仅在门控信号处单向传递，缺乏端到端的联合推理。这可能是其在 MOT20 上 HOTA 仍仅 0.43 的结构性原因——在极端拥挤场景中，时间定位的错误会不可逆地传播至空间跟踪模块。此外，当前基准领域覆盖仅限于多目标跟踪数据集（OVIS、MOT17、MOT20），尚未扩展到更一般的具身场景，这一限制需在后续工作中突破。

## 整体框架

SVAGFormer 采用**时间优先门控（temporal-first gating）**策略，将多实例时空视频动作定位分解为两个级联阶段，以解决全视频空间跟踪带来的虚假轨迹问题。

### Pipeline 流程

1. **输入**：一段完整视频与一条自然语言动作查询（如 “A person is dancing in the open area”）。
2. **时间定位（Temporal Grounding）**：由 **FlashVTG** 模块对全视频进行粗到细的动作时序分割，输出一个或多个动作候选时间窗口。
3. **时间优先门控（Temporal-First Gating）**：将时间定位的输出作为门控信号，**空间跟踪仅在动作窗口内执行**，避免在无动作帧上产生虚假轨迹。
4. **空间跟踪（Spatial Tracking）**：由 **TempRMOT** 模块在受限的时间窗口内进行多目标跟踪，为所有满足查询的动作执行者输出边界框轨迹。
5. **输出**：每个查询对象在动作时段内的完整时空轨迹（时间窗口 + 空间框序列）。

### 模块关系

各模块间为**串行级联**关系，时间定位的输出直接约束空间跟踪的搜索空间。这种设计的关键因果机制在于：先确定“何时发生动作”，再将“谁在执行动作”的跟踪限定在该窗口内，从而将时空多实例定位从联合搜索问题转化为条件搜索问题。

### 设计动机

现有 LVLM 及专家模型在长时、密集、多行动者场景中面临根本性推理鸿沟——空间跟踪在全视频上执行时，无关帧产生的虚假关联会严重破坏轨迹一致性（Table 28 显示所有 LVLM 在 MOT20 上空间定位 HOTA 均为零）。时间优先门控通过**压缩空间跟踪的时间域**，缓解了这一瓶颈，使模型能够以较低的时空复杂度实现可用的联合定位。

### 补充图表

![[assets/figures/papers/paper_list_l75_https_arxiv_org_abs_2510_13016/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of existing video grounding paradigms with our proposed Spatio-temporal Video Action Grounding (SVAG) task. (a) SVG: Spatial Video Grounding focuses only on spatial localization and lacks temporal reasoning. (b) STVG: Spatio-Temporal Video Grounding jointly localizes objects over time but cannot handle multiple interacting instances. (c) VTG: Video Temporal Grounding identifies temporal segments but misses spatial localization. (d) Ours (SVAG): Unifies temporal and spatial grounding to detect and track multiple referent objects performing the queried action across time*

![[assets/figures/papers/paper_list_l75_https_arxiv_org_abs_2510_13016/figures/004_Figure_3.jpg]]
*Figure 3: Overview of the SVAGFormer pipeline. Given a natural language query (e.g., “A person is dancing in the open area”), temporal grounding first narrows the full video (frames 1–2782) to two temporal candidates (2543–2782) and (2557–2772). Spatial grounding then operates exclusively within this window, returning bounding box tracks for all actors satisfying the query*

## 核心模块与公式推导

### 任务统一形式

SVAG 任务将时间定位与空间跟踪统一为单一查询驱动框架。给定视频 $V$ 和自然语言查询 $Q$（描述“谁在执行什么动作”），模型需输出所有满足条件的实例的时空轨迹集合 $\{T_k\}$，其中每条轨迹 $T_k = \{(b_t, c_t)\}_{t=t_s}^{t_e}$ 包含从起始帧 $t_s$ 到结束帧 $t_e$ 的边界框序列及置信度。

### SVAGFormer 流水线模块

SVAGFormer 采用模块化设计，核心由三个组件构成（Figure 3）：

**1. 时间定位模块（FlashVTG）**
基于 Zhao et al. (2025) 的 FlashVTG，通过时序特征分层与自适应分数精炼，产生粗到细的动作候选时间段。该模块接收完整视频特征和查询文本，输出一组候选时间窗口 $\{[t_s^{(i)}, t_e^{(i)}]\}$。

**2. 时间优先门控（Temporal-First Gating）**
这是 SVAGFormer 的核心策略变更。传统方法在全视频上执行空间跟踪后与时间定位结果合并，而 SVAGFormer 先将 FlashVTG 的输出作为门控信号，将空间跟踪严格限定在已识别的时间窗口内。这一设计避免了无关帧产生虚假轨迹，是方法在长时视频上获得优势的关键因果机制。

**3. 空间跟踪模块（TempRMOT）**
在门控后的时间窗口内，TempRMOT 执行多目标跟踪，输出每个满足查询的实例的边界框轨迹。该模块基于 Refer-KITTI-V2 预训练权重初始化，利用时间记忆机制维持跨帧关联。

### 核心评价指标公式

SVAG 任务的联合评价指标 m-HIoU 由空间定位质量（HOTA）和时间定位质量（mIoU）平均得到。

**HOTA 指标**（空间定位质量）：
$$\mathrm{HOTA} = \frac{1}{|\mathcal{A}|} \sum_{\alpha \in \mathcal{A}} \mathrm{HOTA}_{\alpha}$$

其中 $\mathcal{A} = \{0.05, 0.10, ..., 0.95\}$ 为定位阈值集合，共 19 个阈值。每个阈值下的 $\mathrm{HOTA}_{\alpha}$ 可进一步分解为检测准确度 DetA 和关联准确度 AssA 的几何平均：
$$\mathrm{HOTA}_{\alpha} = \sqrt{\mathrm{DetA}_{\alpha} \cdot \mathrm{AssA}_{\alpha}}$$

**mIoU 指标**（时间定位质量）：计算预测时间段与真实时间段在各交并比阈值下的平均交并比。

**m-HIoU 联合指标**：
$$\mathrm{m\text{-}HIoU} = \frac{1}{3} \sum_{d \in \{\text{OVIS, MOT17, MOT20}\}} \frac{\mathrm{HOTA}_d + \mathrm{mIoU}_d}{2}$$

该指标在三个子数据集上分别计算 HOTA 和 mIoU 的均值，再跨数据集平均，作为统一的排名指标。

### 评估协议中的关键设计

SVAGEval 评估框架针对多参考对象场景进行了专门设计：

- **身份映射策略**：对每个真实轨迹 ID，统计各预测 ID 出现的帧数频率，选择频率最高的预测 ID 进行匹配（多数投票），确保时空维度对齐一致。
- **假阳性惩罚**：预测到未提及参考物体的轨迹计为假阳性，确保评估聚焦于查询相关对象。
- **时序对构建**：基于最终的 track_id 映射构建时序预测与真实值对，用于时间定位评估。

### 补充图表

![[assets/figures/papers/paper_list_l75_https_arxiv_org_abs_2510_13016/figures/005_Figure_4.jpg]]
*Figure 4: Flowchart for processing evaluation. Spatial and temporal evaluations are conducted separately on the OVIS, MOT17, and MOT20. The results are averaged and combined to form the final result. Threshold α controls the relative importance of detection and association accuracy in HOTA*

## 实验与分析

### 统一时空评估协议

为衡量时空多实例动作定位能力，作者设计了 **SVAGEval** 评估框架，将空间定位与时间定位分别评估后通过身份映射策略对齐。空间定位采用 **HOTA**（Higher Order Tracking Accuracy）指标，该指标定义为检测准确度与关联准确度的几何平均，并在 0.05 到 0.95 的定位阈值 α 上取均值：

$$\mathrm{HOTA} = \frac{1}{|\mathcal{A}|} \sum_{\alpha \in \mathcal{A}} \mathrm{HOTA}_{\alpha}$$

时间定位采用 R1@0.5 和 mIoU 两个指标。最终的综合指标 **m-HIoU** 定义为三个子数据集（OVIS、MOT17、MOT20）上 HOTA 与 mIoU 的均值，作为主要排名依据。评估中特别设计了多参考对象处理规则：预测到未提及参考物体的轨迹计为假阳性，确保评估聚焦于查询相关对象。

### 主实验结果

Table 2 汇总了各方法在三个子数据集上的统一对比。核心发现如下：

![[assets/figures/papers/paper_list_l75_https_arxiv_org_abs_2510_13016/figures/006_Table_2.jpg]]
*Table 2: Unified comparison across spatial and temporal grounding subtasks on OVIS, MOT17, and MOT20 test sets. HOTA measures spatial grounding quality; R1@0.5 and mIoU measure temporal grounding quality. m-HIoU is the unified joint metric computed as the mean of HOTA and mIoU averaged across all three datasets, and serves as the primary ranking metric. “–” indicates the method addresses only one subtask or lacks both scores required for m-HIoU. Bold and underline indicate the best and second-best results per column. Full per-metric breakdowns are provided in the supplementary material*

**SVAGFormer 在所有方法中取得最优综合性能**，m-HIoU 达到 13.52，显著领先最佳专有 LVLM **GPT-5.4**（OpenAI, 2026）的 10.78（+2.74），以及最佳开源时空模型 **EgoMask**（Liang et al., 2025）的 5.25。这一差距验证了时间优先门控策略的有效性。

**空间定位方面**，SVAGFormer 在 OVIS 上取得 HOTA 22.73，远超 GPT-5.4 的 11.63（+11.10）。在更具挑战性的 MOT17 和 MOT20 上，SVAGFormer 的 HOTA 分别为 0.60 和 0.43，而 GPT-5.4 仅为 0.09 和 0.02。值得注意的是，**所有 LVLM 在 MOT20 上的空间定位 HOTA 均为零**（Table 28），这揭示了当前视觉语言模型在极长时、密集场景下空间跟踪的根本性失败。

**时间定位方面**，专业时间定位模型如 **LD-DETR**（Zhao et al., 2025）和 **R²-Tuning**（Liu et al., ECCV 2024）在短时 OVIS 视频上表现竞争力，但在 MOT17 和 MOT20 上性能急剧下降。这印证了核心瓶颈：**孤立优化的子任务无法组合为统一的时空推理能力**。

**现有模型族均无法可靠回答“谁在执行动作、在哪里、何时发生”**。空间专家模型（如 **DKGTrack** Li et al., ICCV 2025; **TransRMOT** Wu et al., CVPR 2023）缺乏时间定位能力，无法产生完整的 m-HIoU 分数；时间专家模型缺乏空间跟踪能力；LVLM 则在长时密集场景中全面失效。

### 消融实验

**预训练权重的关键作用**（Table 10）：使用 Refer-KITTI-V2 预训练的 TempRMOT 权重，使 OVIS 上 HOTA 提升约 2%，关联准确度（AssA）从 46.6 提升至 51.6。这验证了模型对高质量时空表征预训练的依赖。

**时间记忆长度的影响**（Table 11）：将时间记忆长度从 5 增加到 8，OVIS 上 HOTA 进一步提升（24.214 → 24.611），表明更长的时序上下文有助于空间关联。

**NMS 阈值调优**（Table 14）：在 FlashVTG 中应用 NMS=0.5 可显著提升 MOT17 上的 R10@0.5（+10.42%），但对 OVIS 的 R1@X 和 mIoU 仅有轻微改善，说明时间候选的冗余处理需根据场景密度调整。

### 失败模式分析

**LVLM 在 MOT20 上的系统性失败**（Table 28）：无论使用何种输入配置（原始帧、检测框叠加、文本描述），Qwen2.5-VL 等 LVLM 在 MOT20 上的空间定位 HOTA 始终为零。MOT20 具有极长视频长度和密集人群场景，当前 LVLM 的视觉编码器丢失了细粒度时空信息，无法维持多目标身份关联。

**时间定位的“全时覆盖”倾向**（Figure 5 定性分析）：在 MOT 场景中，最佳时间预测往往几乎覆盖真值的全部时间范围，这反映在 R5 和 R10 指标上表现尚可，但 R1 精确度极低。模型倾向于输出宽泛的时间窗口而非精确定位动作边界。

**密集场景中的假阳性惩罚**：由于 SVAG-Bench 的稀疏标注特性，模型检测到的满足查询但未被标注的目标会被计为假阳性，这在拥挤场景中尤为严重（Figure 5）。

### 数据集统计与难度分层

三个子数据集的视频长度差异显著（Table 5）：OVIS 视频最短，MOT20 最长。性能与视频长度呈强负相关——OVIS 上 HOTA 可达 22.73，MOT20 上仅 0.43。SVAG-Bench 以 28.47 条查询/视频和 14.22 条轨迹/视频的标注密度（Table 1），以及 903 个不同动词的动作多样性，暴露了模型在组合推理上的系统性差距。

![[assets/figures/papers/paper_list_l75_https_arxiv_org_abs_2510_13016/figures/002_Table_1.jpg]]
*Table 1: Comparison of video grounding datasets. Refer-Youtube-VOS and GroOT belong to the SVG domain, while VidSTG and HC-STVG are STVG datasets. Although VidSTG has the largest overall scale, SVAG-Bench achieves the highest annotation density (queries and tracks per video) and the broadest action diversity (distinct verbs), making it particularly suited for fine-grained, multi-object spatio-temporal grounding*

![[assets/figures/papers/paper_list_l75_https_arxiv_org_abs_2510_13016/figures/011_Table_5.jpg]]
*Table 5: Comparison of video lengths in different datasets. The video length of MOT20 is the longest, while OVIS is the shortest*

### 补充图表

![[assets/figures/papers/paper_list_l75_https_arxiv_org_abs_2510_13016/figures/017_Table_10.jpg]]
*Table 10: Performance on the different datasets using TempRMOT [57] with weight from rk2. HOTA increases by approximately 2% on OVIS and MOT17. Pretraining substantially improves association accuracy across dataset*

![[assets/figures/papers/paper_list_l75_https_arxiv_org_abs_2510_13016/figures/018_Table_11.jpg]]
*Table 11: Different lengths for inference on OVIS. Increasing memory length from 5 to 8 improves HOTA, DetA, and AssA. However, the gains are not strictly monotonic*

![[assets/figures/papers/paper_list_l75_https_arxiv_org_abs_2510_13016/figures/037_Table_28.jpg]]
*Table 28: Spatial grounding ablation on MOT20 test set (Qwen2.5-VL). All configurations score zero, confirming that MOT20 poses an intractable challenge for current LVLMs under spatial grounding*

![[assets/figures/papers/paper_list_l75_https_arxiv_org_abs_2510_13016/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative examples for each subdataset. From top to bottom: OVIS, MOT17, MOT20. For OVIS, the zebra is performing a fine-grained action: tilting its head to the left across the grass. The object can be localized, even with subtle action. Detections not labeled but satisfying the query will be marked as false positives, leading to worse performance on sparse annotations in the crowd scenes. For MOT, best temporal predictions often nearly cover the full time range of the ground-truth, reflected in metrics R5 and R10, but perform poorly on R1*

![[assets/figures/papers/paper_list_l75_https_arxiv_org_abs_2510_13016/figures/021_Table_14.jpg]]
*Table 14: Performance on the different datasets using FlashVTG [3]. Datasets marked with † use NMS 0.7. Datasets marked with § use NMS 0.5. The higher score is highlighted in bold. Lower NMS thresholds apply stronger suppression, reducing redundant predictions, leading to better performance*

![[assets/figures/papers/paper_list_l75_https_arxiv_org_abs_2510_13016/figures/003_Figure_2.jpg]]
*Figure 2: Statistics of SVAG-Bench. The majority of queries fall within the range of 6 to 10 words*

## 方法谱系与知识库定位

### 任务谱系：从单维定位到时空联合多实例推理

SVAG-Bench 所定义的 **时空视频动作定位（Spatio-temporal Video Action Grounding, SVAG）** 任务，在视频理解领域填补了一个关键空白。传统视频定位任务长期处于割裂状态（见 Figure 1）：

- **空间视频定位（SVG）**：仅关注空间定位，缺乏时间推理能力，代表数据集包括 Refer-Youtube-VOS 和 GroOT。
- **时空视频定位（STVG）**：联合定位单个对象在时空中的位置，但无法处理多个交互实例，代表数据集包括 VidSTG 和 HC-STVG。
- **视频时间定位（VTG）**：仅识别时间片段，完全忽略空间定位。

SVAG 首次将时间定位与空间多目标跟踪统一为单一任务：给定自然语言查询，模型需同时回答“谁在执行动作、在何处、在何时”，且支持同一查询对应多个参照对象。这一设定使任务复杂度从单实例定位跃升至**多实例、密集、长时的联合时空推理**，直接暴露了现有模型在组合推理上的系统性失败。

### 基线方法矩阵：三类模型的适用边界与失败模式

根据 Table 2 的综合对比，现有方法可分为三个层次，各自展现出清晰的适用边界：

**第一层：空间跟踪专家模型（Spatial Trackers）**
包括 **DKGTrack**（Li et al., ICCV 2025）和 **TransRMOT**（Wu et al., CVPR 2023）。这类模型在空间定位子任务上表现突出，尤其是 DKGTrack 在 OVIS 上 HOTA 达到 21.42，几乎与 SVAGFormer（22.73）持平。然而，它们完全不具备时间定位能力，无法产生 mIoU 分数，因此无法独立完成 SVAG 任务。这一现象揭示了一个关键瓶颈：**孤立优化的子任务能力无法自动组合为统一时空推理**（confidence 0.95，Table 2 及 Section 5.4）。

**第二层：时间定位专家与 LVLM 模型（Temporal Specialists & LVLMs）**
时间定位专家如 **LD-DETR**（Zhao et al., 2025）和 **R²-Tuning**（Liu et al., ECCV 2024）在短时视频（OVIS）上取得有竞争力的 mIoU，但在 MOT17 和 MOT20 上性能急剧崩溃。LVLM 模型如 **VTimeLLM**（Huang et al., CVPR 2024）和 **Qwen2.5-VL**（Qwen Team, 2025）虽然具备语言理解优势，但在空间跟踪上表现极弱。最致命的是，**所有 LVLM 在 MOT20 上的空间定位 HOTA 均为零**（Table 28，confidence 0.95），证明当前视觉语言模型在极长时和密集场景中完全丧失了空间跟踪能力，无论采用何种输入配置。

**第三层：专有与开源时空 LVLM（Proprietary & Open-source Spatiotemporal LVLMs）**
**GPT-5.4**（OpenAI, 2026）作为最强专有模型，在联合指标 m-HIoU 上达到 10.78，是唯一接近 SVAGFormer 的基线。开源模型 **EgoMask**（Liang et al., 2025）仅达到 5.25，差距近一倍。这表明即使是当前最先进的大规模视觉语言模型，在统一时空多实例推理上仍存在巨大的推理鸿沟。

### SVAGFormer 的核心创新：时间优先门控策略

SVAGFormer 在方法谱系中的独特位置源于其**时间优先门控策略（temporal-first gating）**（Section 4，confidence 0.95）。与基线方法要么独立执行空间跟踪、要么在全视频上联合推理不同，SVAGFormer 采用模块化但因果顺序明确的流水线：

1. **时间定位（FlashVTG）**：首先识别动作发生的时间窗口，产生候选时间段。
2. **空间跟踪（TempRMOT）**：仅在时间定位确定的窗口内执行多目标跟踪，将空间推理严格限定在有动作发生的区间。

这一策略的因果逻辑在于：**避免无关帧产生虚假轨迹**。在长时视频中，全视频空间跟踪会产生大量与查询动作无关的轨迹，导致假阳性激增和关联混乱。时间优先门控通过将时间定位输出作为门控信号，从根本上切断了这一噪声源。

消融实验验证了这一设计的有效性：
- 使用预训练权重（TempRMOT from Refer-KITTI-V2）使 OVIS 上 HOTA 提高约 2%，关联准确度 AssA 从 46.6 提升至 51.6（Table 10，confidence 0.95）。
- 将时间记忆长度从 5 增加到 8，OVIS 上 HOTA 进一步提高（24.214→24.611）（Table 11，confidence 0.95）。

这表明模型对**时间记忆的依赖**是性能提升的关键因素，也侧面印证了时间优先门控策略的合理性。

### 适用边界与根本局限

尽管 SVAGFormer 在所有数据集上均取得最优 m-HIoU（13.52 vs. GPT-5.4 的 10.78，Table 2，confidence 0.98），其绝对性能仍然极低，尤其在 MOT17（HOTA 0.60）和 MOT20（HOTA 0.43）上接近零。这揭示了当前方法的几个根本局限：

1. **领域覆盖有限**：基准数据集主要来自多目标跟踪领域（MOT17、MOT20、OVIS），覆盖场景仅限于城市街道、交通监控和动物观测，尚未扩展到具身智能、机器人操作或人机交互等更一般的场景。

2. **模块化设计的可扩展性瓶颈**：SVAGFormer 的时空模块是分离的，缺乏端到端的联合推理。在长时密集视频中，时间定位的错误会不可逆地传播到空间跟踪阶段，且两个模块无法相互校正。这限制了模型在更复杂场景中的可扩展性。

3. **极长时密集场景的根本性失败**：MOT20 上所有方法的空间定位接近零（Table 28），表明当前视觉表示和跟踪架构在处理极长序列（数千帧）和高密度人群时存在根本性局限。定性结果（Figure 5）显示，最佳时间预测往往几乎覆盖整个时间范围（在 R5 和 R10 指标上表现尚可），但在精确时间边界（R1）上表现极差，说明模型缺乏细粒度的时间边界感知能力。

4. **评价指标的潜在不足**：当前联合指标 m-HIoU 是 HOTA 和 mIoU 在三数据集上的简单平均，可能无法充分反映真实场景中细粒度动作理解、多智能体交互质量以及组合推理的深度。

### 开放问题与未来方向

基于上述局限，SVAG 任务向社区提出了以下关键开放问题：

1. **如何突破极长时密集视频的时空定位瓶颈？** 当前所有方法在 MOT20 上的性能接近零，需要全新的视觉表示和记忆机制，使模型能够在数千帧中保持精确的多目标身份关联。

2. **能否设计端到端的统一架构？** 将时间定位、空间跟踪和多实例推理融合为单一可微分模型，避免模块间的信息损失和错误传播，是实现实用性能的关键路径。

3. **如何扩展任务边界至具身场景？** SVAG 当前限于监控领域，将其扩展到机器人操作、人机交互等具身场景，并开发对应的基准数据集，是衡量迈向具身智能进展的必要步骤。

4. **当前 LVLM 的视觉表示是否丢失了细粒度的时空信息？** LVLM 在空间跟踪上的全面失败暗示，其视频编码器可能过度压缩了精确位置和身份信息。如何压缩视频表示同时保留多目标跟踪所需的时空精度，是一个核心架构问题。

5. **评价体系是否需要更细粒度的组合性评估？** m-HIoU 作为单一标量可能掩盖模型在不同维度（时间精度、空间关联、多实例处理）上的能力差异，需要开发分解式评估协议来诊断具体失败模式。

## 原文 PDF

![[paperPDFs/arxiv_2025/SVAG_Bench_A_Large_Scale_Benchmark_for_Multi_Instance_Spatio_temporal_Video_Action_Grounding.pdf]]
