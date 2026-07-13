---
title: "SpaceTools: Tool-Augmented Spatial Reasoning via Double Interactive RL"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SpaceTools_Tool_Augmented_Spatial_Reasoning_via_Double_Interactive_RL.pdf
project_link: null
code_link: null
aliases:
- DDIRL
- SpaceTools
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将训练分解为教学阶段（基于单工具IRL教师与前沿模型的多工具轨迹进行SFT）和探索阶段（在良好初始化下进行全工具IRL），通过两阶段课程式训练实现稳定且有效的多工具协调。
primary_logic: 单工具指向性IRL可高效教授空间定位基础，为多工具IRL提供足够好的策略初始化；在此基础上，交互式探索能将多工具推理泛化到复杂任务，而不会因动作空间爆炸而崩溃。
claims:
- 移除IRL训练的教师模型导致RoboSpatial和RefSpatial性能大幅下降，尤其是在需要精细空间定位的任务上。
- 直接在全任务、全工具上进行IRL（Direct IRL All.）各项指标均大幅落后于DIRL，验证了搜索空间过大导致学习失败。
- 第二阶段交互式RL（S2-IRL）在所有任务上均带来显著提升，是最终多工具协调能力的关键。
- 仅有 SFT 的工具调用（Tool SFT）和仅有非交互式 RL 的工具训练（Tool NIRL）远弱于 DIRL，证明交互式探索不可替代。
---

# SpaceTools: Tool-Augmented Spatial Reasoning via Double Interactive RL

> [!tip] 核心洞察
> 单工具指向性IRL可高效教授空间定位基础，为多工具IRL提供足够好的策略初始化；在此基础上，交互式探索能将多工具推理泛化到复杂任务，而不会因动作空间爆炸而崩溃。

| 字段 | 内容 |
|------|------|
| 中文题名 | 双重交互强化学习驱动的工具增强空间推理 |
| 英文题名 | SpaceTools: Tool-Augmented Spatial Reasoning via Double Interactive RL |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.04069) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DIRL (Double Interactive Reinforcement Learning) |
| Dataset | RoboSpatial-Home, BLINK, BOP-ASK Pose, BOP-ASK Grasp |

> [!tip] 效果简介
> - RoboSpatial-Home (Overall) 上，归一化准确率 (%) 70.00 vs 62.50 (Gemini-ER 1.5) (+7.5)。
> - BLINK (relative depth) 上，归一化准确率 (%) 90.32 vs 88.71 (RoboRefer-8B-SFT) (+1.61)。
> - BOP-ASK Pose 上，归一化 IoU (%) 34.37 vs 1.67 (Claude Sonnet 4.5) (+32.70)。

## 概要

### 问题背景

视觉-语言模型（VLM）在通用场景理解上取得了显著进展，但在需要精确三维空间推理的任务中仍表现不足——例如判断物体相对深度、估计六自由度姿态、预测可执行抓取姿态等。这些任务在机器人操控、增强现实和具身智能中至关重要。现有方案通常依赖固定的工具管线或预计算上下文，训练时模型并不真正调用工具并观察其输出，导致多工具协调能力薄弱、泛化性差。

### 核心瓶颈

直接在所有任务上使用全部工具进行交互式强化学习（IRL）会产生极大的搜索空间，导致探索失败；而纯监督微调（SFT）则使模型在工具协调上缺乏鲁棒性和泛化能力。这一矛盾构成了训练工具增强空间推理模型的核心挑战。

### 方法定位

SpaceTools 提出 **DIRL（Double Interactive Reinforcement Learning，双重交互强化学习）** 训练范式，将学习过程分解为两个阶段：

- **教学阶段（Teaching Phase）**：利用单工具 IRL 教师与前沿闭源模型的多工具轨迹进行 SFT，为模型注入基本的工具使用能力与空间定位先验。
- **探索阶段（Exploration Phase）**：在良好初始化的基础上，使用 GRPO 算法在全任务、全工具下进行交互式 RL，精炼多工具协调策略。

这一“教学-探索”课程设计的关键洞察在于：单工具指向性 IRL 可高效教授空间定位基础，为多工具 IRL 提供足够好的策略初始化；在此基础上，交互式探索能将多工具推理泛化到复杂任务，而不会因动作空间爆炸而崩溃。

训练基础设施方面，SpaceTools 引入了 **Toolshed**——一个分布式工具服务平台，负责管理多个计算密集型视觉与机器人工具实例，提供异步并行调用与资源隔离，支撑训练和推理过程中的真实工具交互。

### 主要结果

- **空间推理基准**：基于 Qwen2.5-VL-3B 的 SpaceTools 在 RoboSpatial-Home 上达到 70.00% 归一化准确率，超越 Gemini-ER 1.5（62.50%）等所有闭源与开源基线；在 BLINK 相对深度任务上达到 90.32%；在 BOP-ASK 姿态估计上达到 34.37%，远超 Claude Sonnet 4.5 的 1.67%。
- **真实机器人操控**：SpaceTools 在抓取-放置任务上达到 86% 成功率，在关系抓取任务上达到 83%，分别超出搭载 Toolshed 的 Claude Sonnet 4.5 基线 7 和 33 个百分点。
- **消融验证**：移除 IRL 教师导致 RoboSpatial 从 70.00 降至 61.14、RefSpatial 从 53.07 降至 29.60；直接在全任务全工具上进行 IRL（Direct IRL All.）均值仅 19.79，远低于 DIRL 的 52.48，充分验证了两阶段课程训练的必要性。

### 方法谱系与知识库定位

SpaceTools 的 DIRL 范式在训练监督与工具交互性两个维度上区别于现有工作。传统工具增强方法（如 **LLaVA-NeXT-8B** Liu et al., 2024a、**RoboPoint-13B** Yuan et al., 2024）在训练时使用预计算工具输出或固定管线，模型不参与真实的工具调用-反馈循环；而 DIRL 在训练过程中引入交互式工具调用，使策略直接从工具输出中学习协调行为。在强化学习层面，DIRL 采用 GRPO 进行策略优化，结合 KL 正则化约束策略更新幅度，与标准 RLHF 管线形成互补而非替代关系。在基础设施层面，Toolshed 为多工具 RL 训练提供了工程基础，其设计借鉴了分布式推理服务的资源隔离思想，但针对视觉工具的密集 I/O 特征进行了专门优化。



### 空间推理：从视觉理解到物理交互的关键瓶颈

空间推理——理解三维场景中物体的位置、深度、姿态与空间关系——是视觉语言模型（VLM）从感知走向真实世界交互的核心能力。无论是机器人抓取、场景导航，还是增强现实中的物体定位，都要求模型不仅能“看懂”图像，更能精确量化空间中的几何关系。然而，当前通用 VLM 在处理这类任务时面临根本性困难：它们缺乏对三维几何的显式建模能力，仅依赖从二维图像中隐式学习到的空间先验，导致在需要精确深度判断、姿态估计或空间关系推理时频繁出错。

这一困境催生了工具增强空间推理的研究方向：通过让 VLM 调用外部视觉工具（如分割模型、深度估计器、指向模型等），将复杂的空间推理分解为可计算的子任务。但现有方法存在一个关键缺陷——**训练过程中工具调用的交互性不足**。如 Table 1 所示，此前的工具增强方法要么在训练时完全不使用工具，仅依靠预定义的固定管线或预计算上下文，要么仅支持单一工具的离线轨迹监督。这意味着模型从未在训练中真正体验过“调用工具→接收结果→调整推理”的闭环过程，导致其在面对需要动态协调多个工具的复杂场景时缺乏鲁棒性和泛化能力。

### 核心瓶颈：多工具交互强化学习的探索灾难

一个直接的想法是：既然交互式工具调用如此重要，为什么不直接在训练中让模型自由调用所有工具，并通过强化学习（RL）优化其策略？答案在于**动作空间的组合爆炸**。当模型同时面对多个视觉工具（分割、深度、指向、抓取预测等）和多个任务（深度比较、姿态估计、空间兼容性判断等）时，可能的工具调用序列数量呈指数级增长。在这种情况下，RL 的探索过程几乎必然失败——模型无法在巨大的搜索空间中找到有效的工具协调策略，表现为训练不收敛或性能崩溃。

Table 13 的实验结果直接验证了这一瓶颈：在全任务、全工具上直接应用交互式强化学习（Direct IRL All.），模型在 RoboSpatial、RefSpatial 和 Pose 任务上的准确率分别仅为 52.86%、3.25% 和 3.26%，平均准确率仅 19.79%，远低于完整 DIRL 方法的 52.48%。这表明，**未经精心课程设计的全量 IRL 实际上比不训练更差**。

### 监督微调的局限：学会“模仿”而非“推理”

如果 RL 探索太难，能否退而求其次，仅用监督微调（SFT）来教授工具使用？SFT 确实可以让模型学会基本的工具调用格式和单步操作，但其根本局限在于：模型学到的是对教师轨迹的“模仿”，而非对工具协调策略的真正理解。当遇到训练中未见过的工具组合或需要错误恢复时，纯 SFT 模型缺乏自主探索和策略调整的能力。

Table 4 的消融实验清晰地展现了这一缺口：仅使用 SFT 进行工具训练（Tool SFT）的变体，其平均准确率仅为 39.19%，而包含第二阶段交互式 RL 的 SpaceTools 达到 52.48%。更值得注意的是，即使是非交互式 RL（Tool NIRL，仅基于格式和工具调用匹配的二元奖励），其平均准确率也仅为 38.06%，甚至略低于 SFT。这说明**交互式探索——而非简单的奖励信号——是学习有效工具协调的关键**。

### 本文动机：从“教学”到“探索”的两阶段课程

上述分析揭示了一个根本矛盾：多工具 IRL 是必要的，但直接进行会因搜索空间过大而失败；SFT 可以安全地建立基础能力，但无法培养真正的策略泛化能力。SpaceTools 的核心动机正是解决这一矛盾：**能否设计一种训练范式，先用“教学”为模型提供足够好的策略初始化，再通过“探索”让模型在可控的搜索空间内精炼多工具协调能力？**

这一思路的直觉来源是：虽然全工具 IRL 的搜索空间极大，但单工具 IRL 的空间是可管理的。如果先训练一个擅长单工具指向的“教师”模型，再用其轨迹和前沿模型的多工具轨迹共同进行 SFT，就能为模型注入基本的空间定位能力和多工具协调的初始策略。在此基础上，第二阶段的全工具 IRL 不再需要从零开始探索，而是在一个已经“知道大概怎么做”的策略附近进行精细优化，从而避免探索崩溃。

### 基础设施挑战：训练时工具调用的工程复杂性

除了算法层面的挑战，让 VLM 在训练过程中实时调用多个计算密集型视觉工具还面临严重的工程瓶颈。传统方案通常采用简单的 HTTP 服务部署工具，但这种方式存在资源竞争、环境冲突和通信开销大等问题。当多个训练样本同时请求工具服务时，端到端延迟会急剧增加，使得交互式训练在实践中不可行。

Toolshed 平台的引入正是为了解决这一基础设施问题。它通过资源隔离、环境管理和异步并行调用，使得在训练循环中高效部署多种视觉和机器人工具成为可能。这不仅是工程上的优化，更是 DIRL 方法得以实现的前提条件——没有低延迟、高吞吐的工具服务平台，交互式 RL 的训练效率将低到不可接受。

### 总结：从工具增强推理到工具增强训练

SpaceTools 的核心动机可以概括为一次范式转变：**从“推理时工具增强”走向“训练时工具增强”**。现有工作大多关注如何在推理阶段给模型配备工具，但忽略了训练阶段的交互性对模型策略质量的根本影响。DIRL 通过两阶段课程设计（教学阶段 SFT → 探索阶段 IRL），在保持训练稳定性的同时，首次实现了在真实交互环境中对多工具协调策略的端到端优化。这一设计使得一个仅 3B 参数的小型 VLM（基于 Qwen2.5-VL-3B-Instruct）能够在多个空间推理基准上超越远大于其规模的前沿模型，并在真实机器人操控任务中展现出强大的泛化能力。



## 核心方法与创新机理

### 问题瓶颈：多工具交互式空间推理的训练困境

空间推理任务（如物体定位、姿态估计、抓取预测）本质上需要精确的三维理解，而视觉语言模型（VLM）自身的空间感知能力有限。引入外部视觉工具可以弥补这一缺陷，但训练一个能够灵活协调多种工具的 VLM 面临两难困境：

- **纯监督微调（SFT）**：模型仅模仿教师行为，缺乏对工具调用后果的交互式反馈，导致工具协调策略脆弱、泛化能力差。
- **直接全工具交互式强化学习（Direct IRL All.）**：在所有任务上同时暴露全部工具进行探索，动作空间呈指数级膨胀，探索失败。实验证实，Direct IRL All. 在 RoboSpatial/RefSpatial/Pose 上的准确率仅分别为 52.86/3.25/3.26，均值 19.79，远低于 SpaceTools 的 70.00/53.07/34.37（均值 52.48）——见 Table 13，置信度 0.99。

这一瓶颈的本质是：**多工具协调的学习信号过于稀疏，模型无法从零开始在巨大的工具-任务组合空间中建立有效的策略**。

### 核心洞察：从“单工具指向”到“多工具泛化”的课程式路径

SpaceTools 的核心洞察在于将多工具空间推理分解为两个可解耦的学习阶段：

1. **单工具指向性 IRL 可以高效教授空间定位基础**：指向（pointing）是所有空间推理任务的原子操作——无论是深度比较、姿态估计还是抓取预测，最终都需要在图像中定位关键点或区域。通过在单工具（指向工具）上进行交互式强化学习，模型能快速习得可靠的空间定位能力，为后续多工具学习提供高质量的策略初始化。

2. **在良好初始化下，全工具 IRL 能将多工具推理泛化到复杂任务**：当模型已经具备基本的空间定位和工具调用能力后，再引入全工具、全任务的交互式探索，搜索空间从“无限可能”缩减为“如何组合已知工具”，使得 GRPO 策略优化能够有效收敛。

这一洞察直接催生了 DIRL（Double Interactive Reinforcement Learning）的两阶段训练范式。

### 关键创新点：三个 changed slots

#### Changed Slot 1：训练阶段的工具交互方式——从“离线模仿”到“在线交互”

| 维度 | 基线方法 | DIRL (SpaceTools) |
|------|----------|-------------------|
| 工具调用方式 | 训练时使用预计算输出或固定管线，模型不实际调用工具 | 训练过程中真实调用工具，模型实时接收工具输出并据此调整后续推理 |
| 反馈机制 | 仅通过 SFT 损失模仿教师序列 | GRPO 基于任务奖励（如 IoU、NNDC）优化策略，模型从工具成功/失败中学习 |
| 典型基线 | Tool SFT（均值 39.19）、Tool NIRL（均值 38.06） | SpaceTools（均值 52.48） |

**证据锚点**：Table 1 对比了现有工作在训练监督与工具调用交互性方面的差异；Table 4 中 Tool SFT 和 Tool NIRL 的消融实验（置信度 0.95）证实，仅靠模仿或非交互式 RL 无法习得鲁棒的多工具协调策略。

这一 changed slot 的因果机制是：交互式工具调用使模型能够感知工具输出的质量与不确定性，从而学会**自适应工具选择**（如任务简单时跳过工具、工具失败时回退到自估计）和**错误恢复行为**——这些能力无法通过观察静态轨迹习得。

#### Changed Slot 2：多工具 RL 的初始化策略——从“冷启动”到“教学-探索”课程

| 维度 | 基线方法 | DIRL (SpaceTools) |
|------|----------|-------------------|
| 初始化方式 | 随机初始化或单工具训练后直接扩展到多工具 | 两阶段课程：教学阶段（Phase-1 SFT）注入教师策略 → 探索阶段（Phase-2 IRL）精炼 |
| 教师组成 | 单一来源 | 双教师混合：单工具 IRL 教师（空间定位基础）+ 通用教师 Claude（多工具轨迹） |
| 探索崩溃风险 | 高（Direct IRL All. 均值仅 19.79） | 低（SpaceTools 均值 52.48） |

**证据锚点**：
- **移除 IRL 教师**：RoboSpatial 从 70.00 降至 61.14，RefSpatial 从 53.07 骤降至 29.60（Table 4，置信度 0.95），证明单工具指向 IRL 是空间定位能力的关键先验。
- **移除通用教师**：Pose 任务从 34.37 降至 18.75（Table 4，置信度 0.95），证明多工具轨迹监督对学习复杂工具链（如姿态估计需要组合检测、深度、3D 拟合等多工具）不可或缺。
- **移除第二阶段 IRL**：Tool SFT（39.19）和 Tool NIRL（38.06）远低于 SpaceTools（52.48），证明交互式探索在全工具协调中不可替代。

这一 changed slot 的设计逻辑是：**教学阶段提供“可行解空间”的边界，探索阶段在该空间内通过试错发现更优策略**。双教师机制确保模型同时获得“单工具精确定位”和“多工具组合推理”两种能力的初始化。

#### Changed Slot 3：强化学习基础设施——从“单工具脚本”到“分布式工具平台 + GRPO”

| 维度 | 基线方法 | DIRL (SpaceTools) |
|------|----------|-------------------|
| 工具基础设施 | 无专用平台，通常仅支持单一简单工具或离线预计算 | Toolshed：分布式工具服务平台，支持异步并行调用、资源隔离、实例弹性伸缩 |
| RL 算法 | 无或简单奖励匹配 | GRPO：多轨迹 rollout + 相对优势估计 + KL 正则化 |
| 奖励设计 | 二进制匹配或简单距离 | 任务特定归一化奖励：NNDC（指向）、MIoU（2D 框）、IoU（姿态）、NNCE（抓取），配合裁剪稳定训练 |

**证据锚点**：
- Toolshed 通过资源隔离和异步并行，在多工具推理管线中实现近线性加速（Table 8, Table 9），尤其在大输入/输出工具（SAM、深度估计）上优势明显（Table 10）。
- GRPO 损失函数为 $\mathcal{L}_{\mathtt{GRPO}}(\theta) = \mathbb{E}_i \big[ -\min \big( \rho_i A_i, \mathrm{clip}(\rho_i, 1-\epsilon, 1+\epsilon) A_i \big) + \beta \mathrm{KL}(\pi_\theta \| \pi_{\mathrm{ref}}) \big]$，通过裁剪优势估计和 KL 正则化防止策略崩溃（Appendix C.1）。
- 奖励归一化与裁剪对稳定训练至关重要：NNDC 配合裁剪达到 35.25 的 pointing 准确率，而 w/o Norm. 直接降为 0（Table 14，置信度 0.95）。

这一 changed slot 解决了“交互式训练在工程上不可行”的问题——多工具的真实调用会产生显著的 I/O 延迟和资源竞争，Toolshed 的分布式设计使得在训练循环中嵌入真实工具调用成为可能。

### 创新总结：DIRL 的因果链路

```
单工具 IRL 教师 ──→ 空间定位基础能力 ──┐
                                        ├──→ Phase-1 SFT（策略初始化）──→ Phase-2 IRL（GRPO 精炼）──→ 多工具协调策略
通用教师 (Claude) ──→ 多工具组合轨迹 ──┘         ↑                              ↑
                                          Toolshed 平台                  Toolshed 平台
                                          (真实工具调用)                 (真实工具调用 + 奖励计算)
```

三个 changed slots 形成闭环：**交互式工具调用**（Slot 1）提供真实反馈，**课程式初始化**（Slot 2）将搜索空间约束在可行域内，**分布式基础设施 + GRPO**（Slot 3）使大规模交互式训练在工程上可行。三者缺一不可——消融实验证实，移除任何一个组件都会导致性能显著退化。



SpaceTools 提出了一种名为 **DIRL（Double Interactive Reinforcement Learning，双重交互强化学习）** 的训练范式，将空间推理建模为 VLM 策略与外部工具之间的序列决策问题。其核心设计围绕一个两阶段课程展开，并通过 **Toolshed** 分布式服务平台支撑训练与推理中的密集工具调用。

### 训练流程：教学-探索双阶段课程

DIRL 的训练流程由两个互补的阶段构成，旨在解决直接在全工具空间上进行交互式 RL 所面临的搜索空间爆炸问题。

**阶段一：教学阶段（Teaching Phase）**
该阶段通过监督微调（SFT）为模型注入基本的工具使用能力。训练数据来自两类教师轨迹的混合：
1. **单工具 IRL 教师轨迹**：针对空间定位基础任务（如指向、二维框定位），使用交互式 RL 单独训练一个教师策略，生成高质量的单工具调用轨迹。这为模型提供了精细的空间定位先验。
2. **通用教师多工具轨迹**：利用前沿闭源模型（如 Claude）在全部工具可用的情况下生成多工具协调轨迹，教授模型如何组合多种视觉工具完成复杂推理链。

SFT 使用交叉熵损失对多轮对话中所有助手回合进行下一 token 预测，使模型在进入交互式探索前获得足够好的策略初始化。

**阶段二：探索阶段（Exploration Phase）**
在 SFT 初始化基础上，模型进入全任务、全工具的交互式 RL 阶段。采用 **GRPO（Group Relative Policy Optimization）** 算法进行策略优化：

$$\mathcal{L}_{\mathtt{GRPO}}(\theta) = \mathbb{E}_i \Big[ -\min \big( \rho_i A_i, \mathrm{clip}(\rho_i, 1-\epsilon, 1+\epsilon) A_i \big) + \beta \mathrm{KL}(\pi_\theta \| \pi_{\mathrm{ref}}) \Big]$$

每次 rollout 生成 $N$ 条轨迹，用相对优势 $A_i$ 更新策略，并通过 KL 散度正则化防止策略偏离参考模型过远。此阶段使模型在真实工具反馈中精炼多工具协调策略，同时避免因动作空间过大导致的探索崩溃。

### 推理流程：多轮工具交互

推理时，VLM 策略 $\pi_\theta$ 与外部工具集 $\mathcal{Q}_{tools}$ 进行多轮交互。如 Algorithm 1 所示，模型交替进行推理（生成思考文本）与工具调用（执行视觉/机器人工具并接收输出），直至产生最终答案。这一过程使模型能够根据中间工具输出动态调整后续推理路径，展现出任务自适应的工具选择策略——例如，对于空间关系任务主要依赖指向工具，对于相对深度任务调用深度估计，对于抓取任务则组合目标检测、姿态估计和抓取预测等多种工具。

### 基础设施：Toolshed 分布式平台

**Toolshed** 是为支撑 DIRL 训练和推理而设计的分布式工具服务平台，解决多工具并行调用带来的计算瓶颈。其核心特性包括：
- **资源与环境隔离**：每个工具实例运行在独立环境中，避免依赖冲突。
- **异步并行调用**：支持模型同时发起多个工具请求，显著降低端到端延迟。
- **模块化工具托管**：统一管理视觉工具（分割、指向、单目深度、3D 框拟合、抓取预测等）和机器人工具（图像采集、抓取执行、物体放置等）。

Toolshed 在竞争负载下通过增加工具实例实现近线性加速（Table 8），并在多工具推理管线中将端到端延迟和吞吐量均优于朴素 HTTP 部署方案（Table 9），尤其在大输入/输出工具（如 SAM、深度估计）上优势明显（Table 10）。

### 奖励设计

DIRL 的探索阶段依赖任务特定的归一化奖励函数来提供密集训练信号：
- **二维框定位**：平均 IoU 奖励 $R_{\mathrm{MIoU}} = \frac{1}{N} \sum_{i=1}^{N} \max_{j} \mathrm{IoU}(\hat{B}_i, B_j)$
- **指向任务**：归一化负距离奖励 $R_{\mathrm{NNDC}} = \frac{\exp(-5d) - \exp(-5\sqrt{2})}{1 - \exp(-5\sqrt{2})}$，与二进制精度取最大值
- **姿态估计**：预测与真值 2D 投影角点凸包的交并比 $R_{\mathrm{IoU}} = \mathrm{IoU}(\hat{C}, C)$
- **抓取预测**：归一化接触点误差 $R_{\mathrm{NNCE}} = 1 - \frac{1}{\delta_{\mathrm{max}}} \min(\delta_{\mathrm{max}}, \frac{1}{N} \sum_{i=1}^{N} \frac{\|\hat{p}_i - p_i\|_2}{d})$，$\delta_{\mathrm{max}}=10$

消融实验（Table 14）证实，奖励归一化与裁剪对稳定训练至关重要——未归一化时指向准确率直接降为 0。

### 关键设计决策的消融验证

Table 4 的训练配方消融揭示了 DIRL 各组件的因果贡献：
- **移除 IRL 教师**（仅用通用教师）：RoboSpatial 从 70.00 降至 61.14，RefSpatial 从 53.07 降至 29.60，证明单工具指向 RL 是空间定位能力的关键先验。
- **移除通用教师**（仅用 IRL 教师）：Pose 任务从 34.37 降至 18.75，说明多工具轨迹监督对学习复杂工具链不可或缺。
- **省略第二阶段 IRL**（仅 SFT 或非交互式 RL）：Tool SFT 和 Tool NIRL 的平均准确率分别为 39.19 和 38.06，远低于完整 DIRL 的 52.48，证明交互式探索在全工具协调中不可替代。

Table 13 进一步表明，直接在全任务、全工具上应用 IRL（Direct IRL All.）的平均准确率仅 19.79，验证了未经课程化训练的全量 IRL 确实因搜索空间过大而失败。

### 补充图表

![[assets/figures/papers/paper_list_l2724_https_arxiv_org_abs_2512_04069/figures/012_Figure_7.jpg]]
*Figure 7: System prompt. Instructional prompt guiding the model’s reasoning, tool-call, and answer process*



### DIRL 双阶段训练范式

SpaceTools 的核心方法 DIRL（Double Interactive Reinforcement Learning）将多工具空间推理建模为序列决策问题：VLM 策略 $\pi_\theta$ 在每一轮中交替进行推理与工具调用，最终给出答案。DIRL 的关键创新在于将训练分解为**教学阶段**与**探索阶段**，以此解决直接在全任务、全工具上进行交互式强化学习（IRL）时搜索空间爆炸导致探索崩溃的根本瓶颈。

**教学阶段（Teaching Phase）** 通过监督微调（SFT）为模型注入基本的工具使用能力。SFT 数据由两类教师轨迹混合构成：① 单工具 IRL 教师轨迹——在单一工具（如指向工具）上训练出的策略所生成的交互轨迹，为模型提供精确空间定位的先验；② 通用教师轨迹——由前沿模型（Claude）在全部工具上生成的多工具协调示例，教授复杂工具链的使用模式。该阶段使用标准的交叉熵下一词元预测损失，对所有助手轮次进行优化。

**探索阶段（Exploration Phase）** 在 SFT 提供的良好初始化基础上，使用 GRPO 算法在全任务、全工具下进行交互式强化学习。每次 rollout 生成 $N$ 条完整轨迹，模型在推理与工具调用之间交替进行，最终输出答案并获得任务奖励。策略更新采用以下 GRPO 损失函数：

$$\mathcal{L}_{\mathtt{GRPO}}(\theta) = \mathbb{E}_i \Big[ -\min \big( \rho_i A_i, \mathrm{clip}(\rho_i, 1-\epsilon, 1+\epsilon) A_i \big) + \beta \mathrm{KL}(\pi_\theta \| \pi_{\mathrm{ref}}) \Big]$$

其中 $\rho_i$ 为新旧策略的概率比，$A_i$ 为基于组内相对表现计算的优势函数，$\epsilon$ 控制裁剪范围，$\beta$ 调节与参考策略 $\pi_{\mathrm{ref}}$ 的 KL 散度正则化强度。这一设计既鼓励探索优质策略，又防止策略偏离过远导致训练不稳定。

### Toolshed 分布式工具平台

Toolshed 是为支撑交互式训练与推理而设计的可扩展工具服务平台，其核心功能包括：① 为每个视觉/机器人工具提供独立的资源与运行环境隔离，避免工具间冲突；② 支持异步并行调用，多个工具实例可同时处理请求；③ 通过实例池化与负载均衡，在高并发场景下实现近线性加速（Table 8-10 验证）。Toolshed 托管了包括 SAM 分割、单目深度估计、3D 框拟合、抓取预测、指向定位、机器人抓取执行等在内的模块化视觉与机器人工具。

### 任务奖励函数设计

DIRL 针对不同空间推理任务设计了专门的归一化奖励函数，以提供密集且稳定的训练信号。

**2D 框定位奖励** 采用平均交并比（Mean IoU）：

$$R_{\mathrm{MIoU}} = \frac{1}{N} \sum_{i=1}^{N} \max_{j} \mathrm{IoU}(\hat{B}_i, B_j)$$

对每个预测框 $\hat{B}_i$ 计算与所有真值框 $B_j$ 的最大 IoU，再取均值。

**指向任务奖励** 使用归一化负距离到质心（NNDC）：

$$R_{\mathrm{NNDC}} = \frac{\exp(-5d) - \exp(-5\sqrt{2})}{1 - \exp(-5\sqrt{2})}$$

其中 $d$ 为预测点到目标区域质心的归一化距离。该奖励与二进制精度取最大值作为最终奖励，配合归一化与裁剪对训练稳定性至关重要——消融实验显示，取消归一化直接导致指向准确率降为 0（Table 14）。

**姿态估计奖励** 基于 2D 投影角点集的凸包 IoU：

$$R_{\mathrm{IoU}} = \mathrm{IoU}(\hat{C}, C)$$

仅当预测角点集 $\hat{C}$ 与真值角点集 $C$ 均有效（各 8 个点）时计算，否则为 0。

**抓取估计奖励** 采用归一化负坐标误差（NNCE）：

$$R_{\mathrm{NNCE}} = 1 - \frac{1}{\delta_{\mathrm{max}}} \min\left(\delta_{\mathrm{max}}, \frac{1}{N} \sum_{i=1}^{N} \frac{\|\hat{p}_i - p_i\|_2}{d}\right)$$

其中 $\hat{p}_i$ 与 $p_i$ 分别为预测和真值的抓取接触点，$d$ 为物体尺度归一化因子，$\delta_{\mathrm{max}}=10$ 用于截断极大误差。对应的评估指标 MACE 综合了抓取中心定位误差与手指方向角误差：

$$\mathrm{MACE} = 1 - \frac{1}{2} \left( \frac{\|\hat{c} - c\|_2}{w} + \frac{1}{4} \sum_{k=1}^{4} \frac{1 - \cos(\hat{r}_k, r_k)}{2} \right)$$

### 消融实验中的对照奖励

在验证交互式 RL 必要性的实验中，非交互式 RL（Tool NIRL）使用二元工具调用奖励：

$$r = \begin{cases} 1, & \text{if FormatCorrect} \land \text{ToolCallMatch} \\ 0, & \text{otherwise} \end{cases}$$

该奖励仅在工具调用格式和参数完全匹配真值时给予 1，否则为 0。实验表明 Tool NIRL 平均准确率仅 38.06，远低于完整 DIRL 的 52.48（Table 4），证明仅靠模仿工具调用模式而缺乏交互式探索无法获得有效的多工具协调能力。



## 实验与关键发现

### 核心瓶颈与因果机制

空间推理中工具增强大模型的训练面临一个根本性矛盾：**直接在所有任务上使用全部工具进行交互式强化学习（IRL）会产生极大搜索空间，导致探索失败**；而纯监督微调（SFT）虽然能教会模型基本的工具调用格式，却使模型在工具协调上缺乏鲁棒性和泛化能力。Table 13 直接验证了这一瓶颈——Direct IRL All. 在 RoboSpatial/RefSpatial/Pose 上的归一化准确率分别仅为 52.86/3.25/3.26，均值 19.79，而 SpaceTools 为 70.00/53.07/34.37，均值 52.48。

![[assets/figures/papers/paper_list_l2724_https_arxiv_org_abs_2512_04069/figures/022_Table_13.jpg]]
*Table 13: Direct IRL on all tasks (Direct IRL All.) with all tools compared with our method*

SpaceTools 的核心因果调控变量是将训练分解为**教学阶段**（Teaching Phase）与**探索阶段**（Exploration Phase）的课程式设计。教学阶段通过 SFT 注入两类教师策略：单工具 IRL 教师提供的指向性空间定位基础，以及前沿模型（Claude）在多工具组合下的完整推理轨迹。探索阶段则在良好初始化基础上进行全工具 GRPO 交互式 RL，使多工具协调策略得以泛化到复杂任务，而不会因动作空间爆炸而崩溃。

### 主要结果

Table 2 汇总了 SpaceTools 在多个空间推理基准上的性能。基于 Qwen2.5-VL-3B-Instruct 微调的 SpaceTools-3B 在绝大多数指标上达到最优或次优：

![[assets/figures/papers/paper_list_l2724_https_arxiv_org_abs_2512_04069/figures/004_Table_2.jpg]]
*Table 2: Performance comparison across spatial reasoning benchmarks. All values are normalized accuracy (%). Bold indicates the best performance within each column, and underline denotes the second-best result. Values of 0 indicate the model either fails to produce valid responses, outputs answers in wrong formats, or produces entirely incorrect predictions, reflecting an inability to handle that task type*

- **RoboSpatial-Home (Overall)**：SpaceTools 达到 70.00%，超过最强闭源基线 Gemini-ER 1.5（62.50%）**+7.5 个百分点**，远超同基础模型的无工具 SFT（~58%）和无工具 RL 变体。
- **BLINK 相对深度**：90.32%，超过 RoboRefer-8B-SFT（88.71%）+1.61 个百分点。
- **BOP-ASK 姿态估计**：34.37%，远超 Claude Sonnet 4.5（1.67%）**+32.70 个百分点**，体现了工具增强对精确三维理解的决定性作用。
- **BOP-ASK 抓取预测**：MACE 指标 43.06%（超过 GPT-5 的 39.59%），成功率 50.00%（超过 GPT-5 的 41.67%）。
- **RefSpatial**：53.07%，超过 RoboRefer-8B-SFT（48.37%）+4.70 个百分点。

在真实机器人操控任务中（Table 3），SpaceTools 同样展现出显著优势：Pick & Place 成功率达 86%（Claude Sonnet 4.5 + Toolshed 为 79%），Relation Pick 成功率达 83%（Claude 仅为 50%），**相对提升达 +33 个百分点**。Table 7 的逐任务分解进一步证实了这一优势在不同子任务上的一致性。

![[assets/figures/papers/paper_list_l2724_https_arxiv_org_abs_2512_04069/figures/007_Table_3.jpg]]
*Table 3: Real-world robotic manipulation performance of SpaceTools and zero-shot VLM baselines equipped with Toolshed. Values are success rates (%) for Pick and Relation Pick tasks, partial success rates (%) for Pick & Place, and seconds for Time-to-First-Movement (TTFM)*

![[assets/figures/papers/paper_list_l2724_https_arxiv_org_abs_2512_04069/figures/014_Table_7.jpg]]
*Table 7: Per-task breakdown of the real-world manipulation results, comparing Ours (SpaceTools), Claude Sonnet 4.5 and GPT-5*

### 消融实验：训练配方的因果贡献

Table 4 系统消融了 DIRL 训练配方的三个核心组件，揭示了清晰的因果链条：

![[assets/figures/papers/paper_list_l2724_https_arxiv_org_abs_2512_04069/figures/008_Table_4.jpg]]
*Table 4: Ablation on training recipes. IRL-T denotes the IRL-trained teacher; Univ-T denotes the universal (frontier-model) teacher; S2-IRL denotes the Stage-2 interactive RL phase. Checkmarks indicate which components are included*

1. **移除 IRL 教师（w/o IRL Teacher）**：仅使用通用教师（Claude）的多工具轨迹进行 SFT，在 RoboSpatial 上降至 61.14（完整 SpaceTools 为 70.00），RefSpatial 更是从 53.07 暴跌至 29.60。这表明单工具指向性 IRL 教师教授的空间定位基础是多工具协调的**必要先验**，通用教师的轨迹无法弥补这一缺失。

2. **移除通用教师（w/o Univ Teacher）**：仅使用 IRL 教师的单工具轨迹进行 SFT，在依赖多工具组合的 Pose 任务上从 34.37 降至 18.75。这说明多工具轨迹监督对学习复杂工具链至关重要，单工具经验无法自动泛化到多工具场景。

3. **省略第二阶段 IRL（Tool SFT / Tool NIRL）**：仅进行 SFT 或非交互式 RL（Tool NIRL 仅奖励格式匹配，见公式 $r = \begin{cases} 1, & \text{if FormatCorrect} \land \text{ToolCallMatch} \\ 0, & \text{otherwise} \end{cases}$），平均准确率分别为 39.19 和 38.06，远低于 SpaceTools 的 52.48。这证明**交互式探索在全工具协调中不可替代**——模型必须通过真实工具反馈来学习何时调用何种工具、如何处理工具失败。

### 奖励设计与数据组成

Table 14 的奖励消融揭示了指向任务中奖励函数设计的关键性：NNDC（Normalized Negative Distance to Centroid）配合归一化与裁剪达到 35.25 的 pointing 准确率，而移除归一化后直接降为 0。格式奖励未带来实质提升，表明几何对齐信号远比输出格式规范重要。

![[assets/figures/papers/paper_list_l2724_https_arxiv_org_abs_2512_04069/figures/023_Table_14.jpg]]
*Table 14: Ablation on reward and prompt design for the pointing task as introduced in Appendix C.2. Norm. indicates whether normalization to range [0, 1] is applied to the reward function. Clip. indicates whether binary clipping is applied. Format indicates whether the format reward is applied. Example in Prompt indicates whether two tool-use examples are added in the prompt. Checkmarks indicate which components are included for each variant*

Table 15 的数据组成消融表明，在训练集中加入二维框定位数据（grounding）能够改善非定位任务（如 compatibility）的表现——移除 grounding 后 RoboSpatial-Home 全面准确率从 69.10 降至 56.90。这揭示了一个重要规律：**数据类型多样性比纯粹扩大同质数据量更重要**。

![[assets/figures/papers/paper_list_l2724_https_arxiv_org_abs_2512_04069/figures/024_Table_15.jpg]]
*Table 15: Evaluation on RoboSpatial-Home using models trained with Tool IRL under different data compositions drawn from the four RoboSpatial data types. Config. refers to configuration data, Compat. to compatibility data, Ground. to grounding (2D bounding box) data, and Vacant to vacant-space localization data. Each entry in the middle columns indicates the number of samples included for that data category. Overall Acc. reports the final accuracy on RoboSpatial-Home*

### 失败模式与局限性

Table 16 按主要错误来源对失败案例进行分类统计，揭示了一个结构性弱点：**抓取估计任务中绝大多数失败源于工具误差**（如目标检测错误、姿态估计不准确），而非规划或推理错误。Figure 12 展示了典型失败案例：(a) 错误的对象定位导致抓取目标错误，(b) 不准确的姿态估计导致抓取姿态不可执行。

在真实机器人操控中，Figure 9 展示了一个代表性失败案例：模型虽然找到了有效的空闲区域，但选点过于靠近边界，导致物体放置在箱子边缘失败。这表明 **2D 点预测与物理可行性之间缺乏紧密耦合**，模型尚未学会在工具输出基础上进行物理合理性校验。

当前模型在工具协调和选点策略上仍有明显局限：无法在工具失败时进行足够鲁棒的错误恢复；对动态环境或更长时序任务的评估缺失；持续学习新工具而避免灾难性遗忘的能力尚未深入探索。这些构成了后续研究的关键开放问题。

### 工具基础设施的性能增益

Table 5 展示了 Toolshed 对前沿闭源模型的即时赋能效果：Claude、GPT-5 等模型在接入 Toolshed 后空间推理性能显著提升，验证了工具增强范式的通用价值。Table 8 和 Table 9 进一步量化了 Toolshed 的系统性能优势：在 8 个并发 RoboRefer 调用下，3 实例 Toolshed 相比单实例 HTTP 部署大幅降低端到端延迟；多工具推理管线中，Toolshed 在 SAM、深度估计等大输入/输出工具上优势尤为明显（Table 10），同时保持所有步骤的低开销。

![[assets/figures/papers/paper_list_l2724_https_arxiv_org_abs_2512_04069/figures/009_Table_5.jpg]]
*Table 5: Comparison of proprietary models with and without the Toolshed enhancement across robotic spatial reasoning benchmarks. Values are normalized accuracy (%)*

![[assets/figures/papers/paper_list_l2724_https_arxiv_org_abs_2512_04069/figures/015_Table_8.jpg]]
*Table 8: Benefit of scaling tool instances with Toolshed under contention. We measure 8 simultaneous RoboRefer tool calls. Compared with a naive HTTP-based deployment using a single instance, Toolshed with 3 instances substantially reduces end-to-end latency*

![[assets/figures/papers/paper_list_l2724_https_arxiv_org_abs_2512_04069/figures/016_Table_9.jpg]]
*Table 9: Pipeline execution latency for answering “Is bok choy or clock closer?” using 2× RoboRefer*

### 补充图表

![[assets/figures/papers/paper_list_l2724_https_arxiv_org_abs_2512_04069/figures/002_Table_1.jpg]]
*Table 1: Comparison of related work for training supervision and tool-call interactivity during training. ‘-’ indicates that only a single tool is used*



## 定位与知识库关联

### 1. 工具增强空间推理的方法谱系

**SpaceTools** 所提出的 **DIRL**（双重交互式强化学习）范式，在工具增强空间推理领域占据了一个独特的方法学位置。为理解这一位置，需要从训练监督形式与工具调用交互性两个维度梳理相关工作的谱系。

**表1**（见实验与分析部分）系统对比了现有工作在这两个维度上的差异。传统空间推理模型（如 **SpaceLLaVA-13B** (Chen et al., 2024a)、**RoboPoint-13B** (Yuan et al., 2024)、**Molmo-7B** (Deitke et al., 2025)）通常采用固定工具管线或预计算上下文进行训练，工具调用在训练时是非交互式的——模型并不真实调用工具并接收实时输出，而是基于预先提取的特征或标注进行学习。这类方法的训练监督形式通常局限于SFT或离线RL。

与之形成对比的是，DIRL在训练过程中实现了**真实的交互式工具调用**：模型在每次rollout中实际调用外部视觉或机器人工具，接收工具输出，并据此调整后续推理步骤。这一设计使得训练分布与推理分布高度一致，避免了训练-推理分布偏移问题。

在交互式训练这一维度上，DIRL进一步通过**两阶段课程式训练**（教学阶段→探索阶段）解决了直接在全任务、全工具上进行交互式RL所面临的搜索空间爆炸问题。教学阶段利用两类教师轨迹进行SFT初始化：（1）**IRL教师**——在单工具上通过交互式RL训练的模型，提供高质量的单工具空间定位轨迹；（2）**通用教师**（如Claude Sonnet 4.5, Anthropic 2025）——在全部工具上的多工具协调轨迹。探索阶段则基于这一良好初始化，使用GRPO算法进行全工具交互式RL微调。

### 2. 与关键基线的方法学关系

#### 2.1 与通用VLM的关系

**SpaceTools**以**Qwen2.5-VL-3B-Instruct** (Bai et al., 2025)为基础模型，但通过DIRL训练赋予了其工具调用与协调能力。实验表明，未经DIRL训练的Qwen2.5-VL-3B即使配备Toolshed工具平台（即零样本工具增强推理），其空间推理性能也远低于经过DIRL训练的SpaceTools（参见Table 11）。这验证了交互式训练对于工具协调能力的必要性，而非单纯依赖推理时的工具接入。

前沿闭源模型（**GPT-4o** (OpenAI, 2024)、**GPT-5** (OpenAI, 2025)、**Claude Sonnet 4.5**、**Gemini-ER 1.5** (Google, 2025)）虽然具备强大的通用推理能力，但在精细空间任务上表现不佳。Table 2显示，这些模型在姿态估计任务上几乎完全失败（GPT-5为0.00，Claude Sonnet 4.5为1.67），而SpaceTools达到34.37%。值得关注的是，当这些闭源模型配备Toolshed工具平台后（Table 5），性能普遍提升，但仍不及经过DIRL训练的SpaceTools——这进一步说明，工具接入本身不足以解决空间推理问题，**面向工具协调的交互式训练**才是关键瓶颈。

#### 2.2 与专用空间VLM的关系

专用空间VLM（如**RoboRefer-8B-SFT** (Zhou et al., 2025)、**RoboBrain2.0-7B** (Team, 2025a)）在特定空间任务上表现强劲，但通常局限于单一工具或固定工具管线。SpaceTools的关键区分点在于其**多工具动态协调能力**：模型学会了根据任务需求自适应选择工具组合，并在工具失败时进行纠错（如回退到自估计或切换替代工具）。这种能力源于DIRL的交互式探索阶段，而非通过SFT或非交互式RL所能获得。

#### 2.3 与视觉-语言-动作模型的关系

在机器人操控维度，**π0.5** (Black et al., 2025)等视觉-语言-动作模型直接输出动作，而SpaceTools将机器人本身视为一种工具，通过统一的工具调用接口实现感知-推理-动作的闭环。Table 3显示，SpaceTools在真实机器人拾取-放置任务上达到86%成功率，在关系拾取任务上达到83%，较配备Toolshed的Claude Sonnet 4.5分别提升+7%和+33%。这表明DIRL训练使模型学会了将感知工具输出与动作工具调用有效衔接。

### 3. 适用边界与局限

#### 3.1 工具误差依赖

SpaceTools的抓取估计准确率仍然偏低（Grasp-MACE为43.06%），Table 16的失败分析表明，绝大多数失败源于工具误差（如目标检测错误、姿态估计不准确），而非规划或推理错误。这揭示了当前方法的根本局限：**模型缺乏对工具输出质量的感知与验证能力**，无法在工具失败时进行足够鲁棒的错误恢复。Figure 12展示了典型失败案例——错误的物体定位或不准确的姿态估计直接导致抓取失败。

#### 3.2 2D预测与物理可行性的脱节

在机器人操控中，模型有时会选择靠近边界的放置点（Figure 9），导致放置失败。这表明当前方法在2D点预测与物理可行性之间缺乏紧密耦合。NNDC奖励函数虽然鼓励预测点接近目标区域质心，但未考虑放置稳定性、碰撞避免等物理约束。

#### 3.3 训练数据与任务覆盖

DIRL的训练依赖于高质量工具使用轨迹。当前SFT数据集仅包含8k条轨迹，虽然通过数据多样性（Table 15显示，加入二维框定位数据能改善非定位任务表现）实现了较好的泛化，但面对全新工具或任务类型时仍需部分重训练（Table 12）。持续学习方法在工具扩展上的能力尚未深入探索。

#### 3.4 动态环境与长时序任务

论文未评估模型在动态环境或更长时序任务中的表现。当前实验主要基于静态图像和单步/少步任务，未集成实时反馈以纠正执行过程中的错误。真实机器人任务中的Time-to-First-Movement（TTFM）指标（Table 3）显示SpaceTools为6.3秒，虽优于闭源基线，但仍不适用于高速实时控制场景。

### 4. 开放问题

1. **工具错误感知与自动恢复**：如何让模型学会感知工具输出的不确定性，并在工具失败时自动切换策略或回退到自估计？当前模型已展现出初步的纠错行为（如切换替代指向工具），但这一能力尚处于萌芽阶段，缺乏系统性的错误恢复机制。

2. **物理可行性约束的集成**：如何在奖励函数或训练过程中整合物理可行性约束（如抓取稳定性、放置安全性），使2D预测与3D物理世界建立更紧密的耦合？NNDC和NNCE等几何奖励函数是必要的，但不足以解决放置边界问题。

3. **持续工具学习**：如何实现新工具的持续学习而无需大量计算开销，并保持原有能力不灾难性遗忘？Table 12展示了DIRL在添加新工具时的高效适配方案，但这一能力在多样化工具扩展场景下的鲁棒性尚待验证。

4. **工具视觉输出的深度推理**：当前模型主要依赖工具提取的标量或坐标结果（如距离、IoU、边界框），而非直接推理工具的视觉输出（如深度图、分割掩膜）。让VLM学会理解和利用工具生成的视觉中间表示，可能进一步提升空间推理精度。

5. **Toolshed的实时优化**：如何优化Toolshed的调度、缓存和批处理策略，以在实时机器人循环中保证低延迟的工具调用？Table 8-10展示了Toolshed在并发负载下的性能优势，但面向毫秒级实时控制场景仍需进一步优化。

6. **长时序多阶段任务的拓展**：如何将工具增强的空间推理拓展到复杂装配、多步骤人机交互等长时序任务？这需要模型具备更强的任务规划、状态追踪和错误恢复能力，超出了当前单轮/少轮交互的范畴。



## 原文 PDF

![[paperPDFs/CVPR_2026/SpaceTools_Tool_Augmented_Spatial_Reasoning_via_Double_Interactive_RL.pdf]]
