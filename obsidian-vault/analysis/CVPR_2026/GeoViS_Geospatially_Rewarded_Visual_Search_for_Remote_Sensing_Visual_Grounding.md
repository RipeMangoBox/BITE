---
title: "GeoViS: Geospatially Rewarded Visual Search for Remote Sensing Visual Grounding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GeoViS_Geospatially_Rewarded_Visual_Search_for_Remote_Sensing_Visual_Grounding.pdf
project_link: null
code_link: "https://github.com/Zhang-Peirong/GeoVis"
huggingface_link: "https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct"
aliases:
- GeoViS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过地理空间奖励驱动的蒙特卡洛树搜索（MCTS）逐步聚焦于语义相关且空间一致的子区域，提供高分辨率局部视觉线索，显著提高有效分辨率并引导精确定位。
primary_logic: 将视觉定位重新定义为一种受地理空间奖励引导的逐步搜索与推理过程：先通过层次化探索识别包含目标的候选子区域，再联合全局与局部线索进行条件定位，从而在保持全局理解的同时克服极端尺度和复杂空间关系带来的挑战。
claims:
- 在DIOR-RSVG上，GeoViS的Pr@0.5达到79.8%，较最强基线提升约10个百分点，较通用MLLM提升近30个百分点。
- 消融实验（Table 3）表明，提供局部视觉线索（Global+Local）将Pr@0.5从71.2%提升至82.9%，证明有效分辨率是核心瓶颈。
- 跨数据集泛化实验（Table 5）显示，在DIOR-RSVG上训练后直接评估VRSBench，GeoViS达到49.0%，大幅优于微调基线（39.3%），证实搜索策略的泛化能力。
- DIOR-RSVG 上 Pr@0.5 = 79.8
---

# GeoViS: Geospatially Rewarded Visual Search for Remote Sensing Visual Grounding

> [!tip] 核心洞察
> 将视觉定位重新定义为一种受地理空间奖励引导的逐步搜索与推理过程：先通过层次化探索识别包含目标的候选子区域，再联合全局与局部线索进行条件定位，从而在保持全局理解的同时克服极端尺度和复杂空间关系带来的挑战。

| 字段 | 内容 |
|------|------|
| 中文题名 | GeoViS：地理空间奖励驱动的遥感视觉搜索与定位 |
| 英文题名 | GeoViS: Geospatially Rewarded Visual Search for Remote Sensing Visual Grounding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.02715) · [Code](https://github.com/Zhang-Peirong/GeoVis) · [HuggingFace](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | GeoViS |
| Dataset | DIOR-RSVG, VRSBench, RSVG-HR, OPT-RSVG |

> [!tip] 效果简介
> - DIOR-RSVG 上，Pr@0.5 79.8 vs 70.1 (GeoChat, approx.) (+9.7)。
> - VRSBench 上，Pr@0.5 68.5 vs 63.0 (strongest RS MLLM, approx.) (+5.5)。
> - RSVG-HR 上，Pr@0.5 51.5 vs Prior best (approx. 45.0) (+6.5)。

## 概述

遥感视觉定位（Remote Sensing Visual Grounding）面临一个核心瓶颈：图像中的目标通常极其微小，与广阔背景形成极端尺度差异，导致模型的有效分辨率极低，难以在感知全局场景的同时捕捉判别性细节；此外，查询语句往往涉及复杂的多目标空间关系和上下文依赖，传统的单步全局预测策略极易出错。

针对这一瓶颈，GeoViS 将视觉定位重新定义为一种**地理空间奖励驱动的逐步搜索与推理过程**。其核心思路是：先通过蒙特卡洛树搜索（MCTS）在层次化探索中识别出语义相关且空间一致的候选子区域，再联合全局与局部高分辨率线索进行条件定位，从而在保持全局理解的前提下，克服极端尺度和复杂空间关系带来的挑战。

**主要结果概览**：

- 在 DIOR-RSVG 基准上，GeoViS 的 Pr@0.5 达到 **79.8%**，较最强基线（约 70.1%）提升约 10 个百分点，较通用多模态大模型提升近 30 个百分点（Table 1）。
- 在 VRSBench 和 RSVG-HR 上分别达到 **68.5%** 和 **51.5%**，较现有最佳方法提升 5–6 个百分点以上（Table 1, Table 2）。
- 消融实验证实，提供目标附近的局部视觉线索（Global+Local）可将 Pr@0.5 从 71.2% 提升至 **82.9%**，直接验证了有效分辨率是核心性能瓶颈（Table 3）。
- 跨数据集泛化实验表明，仅在 DIOR-RSVG 上训练的 GeoViS 在 VRSBench 上达到 **49.0%**，大幅优于微调基线（39.3%），证实搜索策略具备良好的迁移能力（Table 5）。

**方法谱系与知识库定位**：

GeoViS 位于遥感视觉定位和推理型多模态大模型（MLLM）的交汇处。与现有遥感专用 MLLM（如 **GeoChat**（Kuckreja et al., CVPR 2024））和通用 MLLM（如 **GPT-4o**（Hurst et al., arXiv 2024））相比，GeoViS 的关键差异在于将定位策略从“单步全局预测”升级为“奖励驱动的 MCTS 层次搜索 + 条件定位”，并引入结构化地理空间上下文解析（对象/位置/关系三元组）来显式指导空间推理。其统一 VisualRAG 模型同时承担奖励评估、动作引导和条件定位三项能力，区别于传统的单任务定位架构。该框架的搜索范式为将 MCTS 与多模态奖励函数结合用于视觉推理提供了新的设计范式，对需要精细空间感知的遥感理解任务具有参考价值。

## 背景与动机

遥感视觉定位（Remote Sensing Visual Grounding, RSVG）要求模型根据自然语言查询，在大尺度遥感图像中精确预测目标边界框。与自然图像的视觉定位不同，RSVG面临两个核心挑战：

**极端尺度失衡与低有效分辨率。** 遥感图像中目标通常极小（如几十像素的车辆或飞机），而背景场景覆盖数平方公里的地理范围。现有单步方法将整幅高分辨率图像缩放或切分后输入模型，导致目标区域的有效分辨率极低，模型难以同时感知全局场景和判别性细节。这一瓶颈被本文定义为**有效分辨率（effective resolution）**问题——模型实际“看到”的目标像素数远不足以支撑精确的空间定位。

**复杂多目标空间关系与上下文依赖。** 遥感查询往往涉及多个对象之间的空间关系（如“停在跑道左侧第三架飞机”）、地理属性约束（如“靠近河流交叉口”）以及层级化的场景理解。单步全局预测方法缺乏显式的空间推理机制，在面对此类复合查询时容易产生定位漂移或语义混淆。

现有方法可大致归为三类：**专家模型**（如基于Faster R-CNN的模块化管线）依赖手工设计的视觉-语言对齐，泛化能力有限；**通用多模态大语言模型**（如GPT-4o）虽具备强文本理解能力，但因缺乏遥感专用空间先验而表现不佳；**遥感专用MLLM**（如**GeoChat**, Kuckreja et al., CVPR 2024）改进了遥感场景适配，但仍采用单步全局预测范式，未从根本上解决有效分辨率瓶颈。

GeoViS的核心动机在于：将视觉定位**重新定义为一种受地理空间奖励引导的逐步搜索与推理过程**。通过层次化探索识别包含目标的候选子区域，再联合全局与局部线索进行条件定位，从而在保持全局理解的同时克服极端尺度和复杂空间关系带来的挑战。这一思路将定位从“单步答案生成”转变为“多步证据收集与空间收敛”，使模型能够在搜索过程中主动获取高分辨率局部视觉线索。

## 核心创新

### 问题重构：从单步预测到地理空间奖励驱动的视觉搜索

遥感视觉定位（Remote Sensing Visual Grounding）的核心瓶颈在于图像中目标极小且与背景尺度悬殊，导致有效分辨率极低，模型难以同时感知全局场景和判别性细节；此外，查询常涉及复杂的多目标空间关系和上下文依赖，单步定位极易出错。现有方法——无论是遥感专用MLLM（如**GeoChat**, Kuckreja et al., CVPR 2024）还是通用MLLM（如**GPT-4o**, Hurst et al., arXiv 2024）——均采用**单步全局预测**策略，仅依靠全局图像编码进行一次性边界框回归，缺乏对空间关系的显式推理，且受限于全局图像的低有效分辨率。

GeoViS的核心创新在于**将视觉定位重新定义为受地理空间奖励引导的逐步搜索与推理过程**。该方法将定位任务分解为两个序贯阶段：**MCTS视觉搜索（Visual Search）** 与**条件定位（Conditional Grounding）**。在搜索阶段，模型通过蒙特卡洛树搜索（MCTS）在图像空间中层次化探索，逐步聚焦于语义相关且空间一致的子区域；在定位阶段，模型联合全局图像与搜索得到的高分辨率局部子区域作为视觉线索，进行条件化的边界框预测。这一策略在保持全局理解的同时，显著提高了对微小目标的有效分辨率。

### 关键创新维度（Changed Slots）

#### 1. 定位策略：从单步全局预测到奖励驱动的层次搜索 + 条件定位

| 维度 | 基线方法 | GeoViS |
|------|----------|--------|
| 定位策略 | 单步全局预测（one-shot prediction over entire image） | 奖励驱动的MCTS层次搜索 + 条件定位（two-stage: visual search + conditional grounding） |
| 空间推理与有效分辨率 | 仅依靠全局图像编码，低有效分辨率，无显式空间推理 | 结构化地理空间上下文解析，并通过QA和IoU奖励引导 zoom-in/zoom-out 动作，逐步聚焦高分辨率子区域 |
| 模型架构 | 单任务MLLM（仅输出边界框） | 统一VisualRAG模型，同时执行奖励评估、动作引导和条件定位三项能力 |

**证据支撑**：消融实验（Table 3）直接验证了有效分辨率是核心瓶颈——仅使用全局图像时Pr@0.5为71.2%，额外提供目标附近裁剪区域作为视觉线索后跃升至82.9%，提升幅度达11.7个百分点。这一结果强有力地证明了GeoViS通过搜索获取高分辨率局部视觉线索的策略是性能提升的关键因果机制。

#### 2. 空间推理机制：结构化地理空间上下文解析

GeoViS引入了一个**结构化查询解析模块（Φ）**，将自然语言查询显式分解为三元组 $\hat{T} = \Phi(T) = \{o, p, r\}$，分别对应目标对象（object）、空间属性（position）和关系引用（relation）。这一解析为后续的MCTS搜索提供了可解释的地理空间上下文，使模型能够根据语义结构引导搜索方向，而非盲目地在全图中漫游。

在此基础上，搜索过程被形式化为**马尔可夫决策过程（MDP）** $\mathcal{M} := (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R})$，其中：
- 状态空间 $\mathcal{S}$ 表示候选图像子区域；
- 动作空间 $\mathcal{A}$ 包含 **Zoom-in**（将当前区域按3×3网格划分并选择子区域 $s_{t+1} = \mathcal{T}_{\mathrm{in}}(s_t, a_t) = R_{i,j}(s_t)$）和 **Zoom-out**（按固定缩放因子λ扩大区域 $s_{t+1} = \mathcal{T}_{\mathrm{out}}(s_t, a_t) = \lambda \cdot s_t$）；
- MCTS通过UCT选择准则 $a^{*} = \arg\max_{a \in \mathcal{A}(s)} \left[ Q(s,a) + c \sqrt{\frac{\ln N(s)}{N(s,a) + \varepsilon}} \right]$ 平衡探索与利用。

#### 3. 地理空间奖励函数：语义与空间联合引导

GeoViS设计了**组合地理空间奖励函数**，同时考虑语义一致性和空间对齐：

$$r_t = \alpha r_{\mathrm{QA}} + (1 - \alpha) r_{\mathrm{IoU}}, \quad r_t \in [0,1]$$

其中 $r_{\mathrm{QA}}$ 验证三元组语义一致性（目标对象、空间属性、关系引用是否在候选区域中得到满足），$r_{\mathrm{IoU}}$ 衡量预测框在候选区域内的空间紧凑性。奖励平衡系数 $\alpha$ 的消融实验（Figure 4）表明，$\alpha = 0.1$ 时达到最佳性能，说明空间一致性（IoU奖励）在引导搜索中比纯语义验证更为关键，需要赋予较高权重。

#### 4. 统一VisualRAG模型：三项能力协同

GeoViS的核心架构是一个统一的**VisualRAG多模态大语言模型**（基于Qwen2.5-VL-3B微调），同时提供三项关键能力：
- **奖励评估**：对候选区域进行QA语义验证和IoU空间对齐评分；
- **动作引导**：预测下一Zoom-in动作应选择的子网格；
- **条件定位**：以全局图像 $I_g$ 和搜索到的最优子区域 $I(s^{\star})$ 为条件，预测最终边界框 $B = \mathcal{G}(I_g, T \mid I(s^{\star}))$。

这种三合一的设计避免了多模型级联带来的误差累积，使搜索引导和最终定位共享同一视觉-语言表征空间。

### 创新意义与泛化能力

GeoViS的搜索策略展现出显著的跨数据集泛化能力（Table 5）：在DIOR-RSVG上训练后直接评估VRSBench，GeoViS达到49.0%，大幅优于微调基线（39.3%），证实了搜索策略本身——而非对特定数据分布的过拟合——是性能提升的根本原因。这为遥感视觉定位领域提供了一种新的范式：将“一次性全局预测”转变为“奖励驱动的序贯搜索与推理”，其核心思想有望泛化到其他需要处理极端尺度差异和多目标空间关系的视觉定位任务。

## 整体框架

GeoViS 将遥感视觉定位重新定义为**地理空间奖励驱动的多步搜索与推理过程**，整体流程分为两个顺序阶段：**MCTS 视觉搜索**与**条件定位**。其核心思想是：与其在整幅大幅面遥感图像上一次性预测目标边界框，不如让模型先通过层次化探索逐步锁定最具信息量的子区域，再联合全局上下文与局部高分辨率线索进行精确定位。

### Pipeline 总览

整个框架围绕一个统一的 **VisualRAG 模型**构建，该模型同时承担三项能力：**奖励评估**（判断候选区域与查询的语义及空间一致性）、**动作引导**（预测下一步 Zoom-in 应聚焦的子网格单元）和**最终定位推理**（联合全局与局部图像输出目标边界框）。

具体流程如下（参见 Figure 2）：

![[assets/figures/papers/paper_list_l2125_https_arxiv_org_abs_2512_02715/figures/002_Figure_2.jpg]]
*Figure 2: Overview of GeoViS. Complex queries are structured into object, position, and relation cues. GeoViS first performs MCTS-based visual search to identify the most informative subregion, where each node represents a candidate region, and then conducts conditional grounding using the global image and the selected subregion. The VisualRAG model supports the entire pipeline by providing action guidance, reward evaluation, and final localization*

1. **查询结构化解析**  
   输入的自然语言查询 $T$ 首先通过解析器 $\Phi$ 被分解为结构化三元组 $\hat{T} = \{o, p, r\}$，分别对应目标对象（object）、空间属性（position）和关系引用（relation）。这一步将模糊的语言描述转化为可操作的地理空间上下文线索，为后续的奖励评估和搜索引导提供语义基础。

2. **MCTS 视觉搜索阶段**  
   搜索过程被建模为马尔可夫决策过程（MDP），状态 $s_t$ 表示当前关注的图像子区域，动作空间包含 **Zoom-in**（在当前区域的 $3 \times 3$ 网格中选择一个子区域进行局部细化）和 **Zoom-out**（以固定缩放因子 $\lambda$ 扩大当前区域以恢复全局上下文）。  
   MCTS 通过 UCT 选择策略在搜索树上平衡探索与利用，每次模拟中 VisualRAG 模型为候选节点计算组合奖励：
   $$r_t = \alpha r_{\mathrm{QA}} + (1 - \alpha) r_{\mathrm{IoU}}$$
   其中 $r_{\mathrm{QA}}$ 验证子区域内容与三元组 $\hat{T}$ 的语义一致性，$r_{\mathrm{IoU}}$ 衡量预测框在该区域内的空间紧凑性。搜索收敛到最优节点 $s^\star$ 后，其对应的高分辨率子区域 $I(s^\star)$ 被保留为视觉提示。

3. **条件定位阶段**  
   将全局图像 $I_g$ 与搜索得到的最优子区域 $I(s^\star)$ 联合输入 VisualRAG 模型，以条件生成的方式预测最终目标边界框：
   $$B = \mathcal{G}(I_g, T \mid I(s^\star))$$
   这种设计使模型既能保持对全局场景的理解，又能获得目标附近的高分辨率细节，克服了单步全局预测中有效分辨率不足的核心瓶颈。

### 模块关系与数据流

- **VisualRAG 模型**是贯穿两阶段的统一骨干，在搜索阶段提供奖励信号和动作建议，在定位阶段输出最终预测。三者共享同一多模态大语言模型，通过全参数微调（视觉塔、多模态投影器和语言骨干均解冻）获得这三种能力。
- **MCTS 搜索器**作为外层控制循环，调用 VisualRAG 的奖励和动作预测来构建和评估搜索树，不参与梯度更新。
- **查询解析器 $\Phi$** 在流程开始时执行一次，将自然语言转换为结构化表示，后续所有奖励计算和动作引导均基于该结构化三元组进行。

### 推理时的交互机制

推理时，MCTS 每次查询执行 10 次模拟，最大搜索深度设为 5。VisualRAG 模型在搜索过程中被反复调用以评估候选区域并建议 Zoom-in 目标，搜索收敛后仅执行一次最终定位推理。这种“搜索时多次评估、定位时一次生成”的策略，将计算开销集中在信息获取阶段，而最终定位则利用搜索积累的局部线索实现高精度输出。

## 核心模块与公式推导

GeoViS 将遥感视觉定位重新定义为**地理空间奖励驱动的视觉搜索问题**，其核心由四个紧密协作的模块构成：结构化查询解析、MCTS 视觉搜索、地理空间奖励函数以及统一 VisualRAG 模型。

### 结构化查询解析 (Φ)

遥感定位查询通常涉及复杂的多目标空间关系（如“停车场东北角的白色汽车”）。为提供可解释的地理空间上下文，GeoViS 首先将自然语言查询 $T$ 解析为结构化三元组：

$$\hat{T} = \Phi(T) = \{o, p, r\}$$

其中 $o$ 表示目标对象类别，$p$ 描述空间属性（如方位、布局），$r$ 捕获对象间的关系引用。这一分解为后续的奖励评估和动作引导提供了明确的语义锚点。

### MCTS 视觉搜索模块

视觉搜索被形式化为马尔可夫决策过程 $\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R})$：
- **状态** $s_t \in \mathcal{S}$ 表示当前观察的图像子区域；
- **动作空间** $\mathcal{A}$ 包含 Zoom-in 和 Zoom-out 两种操作；
- **状态转移** $\mathcal{T}$ 根据动作更新观察区域；
- **奖励函数** $\mathcal{R}$ 量化当前状态-动作对的定位潜力。

搜索树通过 **UCT 选择策略**平衡探索与利用，在节点 $s$ 处选择子节点 $a^*$：

$$a^{*} = \arg\max_{a \in \mathcal{A}(s)} \left[ Q(s,a) + c \sqrt{\frac{\ln N(s)}{N(s,a) + \varepsilon}} \right]$$

其中 $Q(s,a)$ 为状态-动作对的累积奖励均值，$N(s)$ 和 $N(s,a)$ 分别为节点与边的访问次数，$c$ 控制探索权重，$\varepsilon$ 防止除零。

### 动作空间设计

**Zoom-in** 将当前区域 $s_t$ 按 $3 \times 3$ 网格划分，动作引导模型预测目标最可能所在的子网格 $R_{i,j}$：

$$s_{t+1} = \mathcal{T}_{\mathrm{in}}(s_t, a_t) = R_{i,j}(s_t)$$

**Zoom-out** 以固定缩放因子 $\lambda > 1$ 扩大当前区域，恢复全局上下文：

$$s_{t+1} = \mathcal{T}_{\mathrm{out}}(s_t, a_t) = \lambda \cdot s_t$$

### 地理空间奖励函数

奖励函数组合**语义一致性**与**空间紧凑性**双重信号：

$$r_t = \alpha r_{\mathrm{QA}} + (1 - \alpha) r_{\mathrm{IoU}}, \quad r_t \in [0,1]$$

- $r_{\mathrm{QA}}$ 为 QA 语义奖励，验证当前子区域是否满足结构化三元组 $\{o, p, r\}$ 的语义约束；
- $r_{\mathrm{IoU}}$ 为 IoU 空间奖励，衡量预测框在当前区域内的紧凑程度，鼓励搜索聚焦于目标附近；
- $\alpha$ 为平衡系数。消融实验表明 $\alpha = 0.1$ 时最优，说明空间一致性在引导搜索中比纯语义验证更为关键。

### VisualRAG 模型

VisualRAG 是基于 Qwen2.5-VL-3B 微调的统一多模态大语言模型，同时承担三项能力：
1. **奖励评估**：为 MCTS 节点计算 $r_{\mathrm{QA}}$ 和 $r_{\mathrm{IoU}}$；
2. **动作引导**：预测下一 Zoom-in 步骤的目标子网格；
3. **条件定位**：联合全局图像 $I_g$ 和搜索收敛到的最优子区域 $I(s^\star)$，预测最终边界框：

$$B = \mathcal{G}(I_g, T \mid I(s^\star))$$

训练时，视觉编码器、多模态投影器和语言骨干全参数解冻。推理阶段，MCTS 每查询执行 10 次模拟，最大搜索深度为 5，搜索收敛后以 $I(s^\star)$ 作为视觉提示进行条件定位。

### 补充图表

![[assets/figures/papers/paper_list_l2125_https_arxiv_org_abs_2512_02715/figures/001_Figure_1.jpg]]
*Figure 1: Complex queries with multi-object relations and tiny targets make remote sensing grounding challenging. While existing one-step methods that resize or divide images often fail, Geo-ViS parses structured semantics and performs reward-guided subregion exploration to achieve accurate localization*

## 实验与分析

### 核心瓶颈验证：有效分辨率是关键

遥感视觉定位的核心困难在于目标极小且与背景尺度悬殊，导致模型在全局图像上的有效分辨率极低，难以同时感知场景上下文和判别性细节。GeoViS通过MCTS驱动的逐步搜索，聚焦于语义相关且空间一致的子区域，从而提供高分辨率局部视觉线索。

消融实验直接验证了这一瓶颈。在DIOR-RSVG上，仅使用全局图像（Global only）训练的模型Pr@0.5为71.2%；当额外提供目标附近裁剪区域（Global+Local）作为视觉线索时，性能跃升至82.9%（Table 3）。这11.7个百分点的提升明确表明，有效分辨率不足是制约定位性能的核心因素，而GeoViS的搜索机制正是通过自动发现并利用这些高分辨率局部区域来克服这一瓶颈。

![[assets/figures/papers/paper_list_l2125_https_arxiv_org_abs_2512_02715/figures/007_Table_3.jpg]]
*Table 3: Ablation on effective resolution using DIOR-RSVG. “Global only” trains on full-scene images, while “Global+Local” additionally provides cropped regions near the target. The clear gains demonstrate the value of localized visual cues*

### 主实验结果

**DIOR-RSVG数据集。** GeoViS在DIOR-RSVG上取得79.8%的Pr@0.5和70.1%的Pr@0.7（Table 1），较遥感专用MLLM基线**GeoChat**（Kuckreja et al., CVPR 2024）提升约10个百分点，较通用MLLM（如GPT-4o）提升近30个百分点。这一差距在Pr@0.7这一更严格的指标上依然保持，表明GeoViS不仅定位更准，预测框的精度也更高。

**VRSBench数据集。** GeoViS达到68.5% Pr@0.5，超过最强遥感MLLM约5.5个百分点（Table 1）。VRSBench的查询类型和场景分布与DIOR-RSVG不同，GeoViS在此数据集上的优势验证了搜索策略的跨场景鲁棒性。

**RSVG-HR和OPT-RSVG数据集。** 在RSVG-HR上，GeoViS取得51.5% Pr@0.5，较此前最优方法提升约6.5个百分点；在OPT-RSVG上达到70.3% Pr@0.5，提升约5.3个百分点（Table 2）。值得注意的是，RSVG-HR以极高分辨率图像和极小目标著称，GeoViS在该数据集上的显著优势进一步印证了逐步聚焦高分辨率子区域策略的有效性。

### 消融实验

**原子操作贡献分解。** Table 4在简化训练设置下逐步叠加GeoViS的核心组件，量化了各原子操作的累积增益。从基础模型开始，依次加入QA奖励、IoU奖励和Zoom-in动作，每一步均带来正向提升，完整模型在DIOR-RSVG上取得74.5% Pr@0.5。其中，IoU空间奖励的加入带来的增益最为显著，说明空间对齐信号在引导搜索中比纯语义验证更为关键。

**奖励平衡系数α的敏感性。** Figure 4展示了奖励组合权重α在DIOR-RSVG上的影响。α=0.1时性能达到最优，此时IoU奖励权重（1-α=0.9）远高于QA奖励权重。这一结果表明，在搜索过程中，预测框与候选区域的空间紧凑性比语义一致性验证更能有效引导模型收敛到正确子区域。当α过大（过度依赖QA奖励）时，性能明显下降，因为语义验证本身可能不准确，引入噪声引导。

**跨数据集泛化能力。** Table 5展示了更具说服力的泛化实验：模型仅在DIOR-RSVG上训练，直接评估VRSBench和OPT-RSVG。GeoViS在VRSBench上达到49.0% Pr@0.5，大幅优于微调基线（39.3%）；在OPT-RSVG上同样保持优势。这表明GeoViS学到的是一种可迁移的搜索策略，而非对特定数据集分布的死记硬背——MCTS驱动的层次探索框架本身赋予了模型跨数据集的泛化能力。

### 公平性说明

需要指出的是，GeoViS基于Qwen2.5-VL-3B微调，而部分对比方法可能使用不同的视觉骨干和训练范式，绝对数值对比需谨慎解读。Table 1和Table 2中部分基线模型的具体数值在原文中未明确报告，此处引用的近似值基于论文叙述推算，存在一定不确定性。此外，消融实验（Table 3/4）因训练配置与主表不同，数值不能直接横向对比。

### 定性分析

Figure 3展示了基线与GeoViS在DIOR-RSVG、OPT-RSVG和RSVG-HR上的定位可视化对比。GeoViS在处理多目标空间关系查询（如“位于A左侧的B”）和极小目标场景时，预测框与真实框的重合度明显优于单步预测的Qwen2.5-VL-3B基线，直观验证了逐步搜索策略在复杂空间推理中的优势。

### 补充图表

![[assets/figures/papers/paper_list_l2125_https_arxiv_org_abs_2512_02715/figures/003_Table_1.jpg]]
*Table 1: Results on DIOR-RSVG, VRSBench, and GeoChat. GeoViS is trained on Qwen2.5-VL-3B. Best and second-best results are bolded and underlined. Blank entries denote unreported metrics, and models marked with * use evaluation results sourced from [28]*

![[assets/figures/papers/paper_list_l2125_https_arxiv_org_abs_2512_02715/figures/005_Table_2.jpg]]
*Table 2: Results on RSVG-HR and OPT-RSVG. GeoViS is trained on Qwen2.5-VL-3B. Best and second-best scores are highlighted. Missing values denote metrics unreported by the original papers*

![[assets/figures/papers/paper_list_l2125_https_arxiv_org_abs_2512_02715/figures/006_Table_4.jpg]]
*Table 4: Ablation of atomic operations on the DIOR-RSVG dataset. Each component provides a measurable gain*

![[assets/figures/papers/paper_list_l2125_https_arxiv_org_abs_2512_02715/figures/009_Table_5.jpg]]
*Table 5: Cross-dataset generalization results. Models are trained on DIOR-RSVG and evaluated on VRSBench and OPT-RSVG. GeoViS demonstrates strong transferability across datasets, outperforming fine-tuned baselines by a clear margin*

![[assets/figures/papers/paper_list_l2125_https_arxiv_org_abs_2512_02715/figures/008_Figure_4.jpg]]
*Figure 4: Ablation on the reward balance ratio α on DIOR-RSVG. The vertical axis shows the relative performance change (%) normalized to the maximum value for better visualization*

![[assets/figures/papers/paper_list_l2125_https_arxiv_org_abs_2512_02715/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative results on DIOR-RSVG, OPT-RSVG, and RSVG-HR comparing baseline (Qwen-2.5-VL-3B) with GeoViS*

## 方法谱系与知识库定位

### 遥感视觉定位的范式演进

遥感视觉定位（Remote Sensing Visual Grounding, RSVG）的核心挑战在于遥感图像中目标极小且与背景尺度悬殊，导致有效分辨率极低，模型难以同时感知全局场景和判别性细节。现有方法可依其定位策略划分为三大范式：

**单步全局预测范式**是当前主流。此类方法将整幅遥感图像缩放到固定分辨率后直接输入模型，一次性输出目标边界框。代表工作包括遥感专用MLLM **GeoChat**（Kuckreja et al., CVPR 2024）和通用MLLM **GPT-4o**（Hurst et al., arXiv 2024）。该范式的根本缺陷在于：全局缩放导致微小目标的有效分辨率极低（例如一个20×20像素的目标在1024×1024的全局图像中仅占约0.04%的面积），模型缺乏足够的判别性视觉线索，在涉及多目标空间关系和复杂语义查询时定位精度急剧下降。Figure 1中的动机示例直观展示了单步方法在微小目标和复杂空间查询场景下的失效模式。

**网格划分+逐格预测范式**试图通过将大图切分为若干子图以提升局部分辨率，但面临两个固有问题：一是网格划分破坏了目标的完整性和空间连续性，跨网格目标难以处理；二是缺乏智能的子区域选择机制，计算资源被浪费在大量不包含目标的区域上。

**GeoViS的搜索-定位范式**将视觉定位重新定义为地理空间奖励驱动的逐步搜索与推理过程。其核心创新在于将定位任务分解为两个序贯阶段：首先通过蒙特卡洛树搜索（MCTS）在全局图像上执行奖励引导的层次化探索，逐步聚焦于语义相关且空间一致的子区域；然后在搜索到的最优子区域条件下进行条件定位。这一设计使模型在保持全局理解的同时获得了目标区域的高分辨率局部线索，从根本上解决了有效分辨率瓶颈。

### 与基线方法的关键差异

GeoViS与现有方法的核心差异体现在定位策略、空间推理机制和模型架构三个维度：

| 维度 | 单步全局预测基线 | GeoViS |
|------|-----------------|--------|
| **定位策略** | 单步全局预测（one-shot prediction over entire image） | 奖励驱动的MCTS层次搜索 + 条件定位（two-stage: visual search + conditional grounding） |
| **空间推理与有效分辨率** | 仅依靠全局图像编码，低有效分辨率，无显式空间推理 | 结构化地理空间上下文解析（object/position/relation），通过QA和IoU奖励引导zoom-in/zoom-out动作，逐步聚焦高分辨率子区域 |
| **模型架构** | 单任务MLLM（仅输出边界框） | 统一VisualRAG模型，同时执行奖励评估、动作引导和条件定位三项能力 |

**定位策略差异**：基线模型**Qwen2.5-VL-3B**直接对整个图像进行编码并预测边界框，其性能受限于全局图像中目标信息的稀疏性。GeoViS则通过MCTS搜索过程（每次查询执行10次模拟，最大搜索深度为5）主动探索图像空间，选择最具信息量的子区域作为定位条件。消融实验（Table 3）提供了决定性证据：仅使用全局图像（Global only）时Pr@0.5为71.2%，而额外提供目标附近裁剪区域（Global+Local）作为视觉线索后，性能跃升至82.9%，直接证明了有效分辨率是核心瓶颈。

**空间推理差异**：GeoViS引入了结构化查询解析模块Φ，将自然语言查询分解为对象(o)、空间属性(p)、关系(r)三元组（$\\hat{T} = \\Phi(T) = \\{o, p, r\\}$），使模型具备可解释的地理空间上下文理解能力。这一设计与仅依赖隐式视觉-语言对齐的基线方法形成鲜明对比。

**模型架构差异**：GeoViS的VisualRAG模型是一个统一的多模态大语言模型，同时提供奖励评估（验证候选区域的语义和几何一致性）、动作引导（预测下一Zoom-in子网格）和最终定位三项能力，而非基线的单一预测功能。模型基于Qwen2.5-VL-3B进行全参数微调（视觉塔、多模态投影器和语言骨干全部解冻），初始学习率为$1 \\times 10^{-5}$。

### 适用边界与泛化能力

GeoViS在以下条件下展现出显著优势：

1. **极小目标定位**：当目标在全局图像中占比极小时，搜索机制能有效提升有效分辨率。在DIOR-RSVG数据集上，GeoViS的Pr@0.5达到79.8%，较最强遥感MLLM基线提升约10个百分点，较通用MLLM提升近30个百分点（Table 1）。

2. **多目标空间关系查询**：涉及“位于...左侧”“在...之间”等复杂空间关系的查询，结构化查询解析提供了明确的语义指导。

3. **跨数据集泛化**：Table 5的跨数据集泛化实验显示，在DIOR-RSVG上训练后直接评估VRSBench，GeoViS达到49.0%，大幅优于微调基线（39.3%），证实搜索策略本身具有强泛化能力，不依赖于特定数据集的分布特征。

然而，GeoViS的适用边界同样明确：

- **计算开销**：MCTS搜索过程在推理时需执行多次模型前向传播（每次模拟涉及奖励评估和动作引导），推理延迟显著高于单步方法。论文未提供具体的推理时间对比数据，该点需手动验证。

- **搜索深度限制**：当前最大搜索深度固定为5，对于目标分布在极深层级嵌套场景中的情况，可能无法充分探索。

- **动作空间刚性**：Zoom-in采用固定3×3网格划分，Zoom-out采用固定缩放因子λ，在处理极端长宽比目标或稀疏分布目标时可能不够灵活。

### 局限与开放问题

基于分析，GeoViS存在以下局限和待探索方向：

1. **自适应搜索深度**：MCTS搜索过程的深度与模拟次数目前为固定超参数（深度5，模拟10次），如何根据图像复杂度和查询语义自适应调整搜索预算，是提升效率的关键。简单场景可能只需2-3次模拟即可定位，而复杂多目标查询可能需要更深的探索。

2. **奖励函数的自身准确性**：QA和IoU奖励基于VisualRAG模型自身预测，其准确性直接影响搜索引导质量。当模型对候选区域的语义验证或空间预测存在系统性偏差时，搜索可能被引导至次优区域。论文未定量评估奖励预测误差对最终定位性能的影响，这一耦合关系值得深入研究。

3. **动态动作空间设计**：固定3×3网格划分和固定缩放因子λ在处理极端场景时缺乏灵活性。可能的改进方向包括：基于查询语义动态调整网格粒度（如目标描述为“大型建筑”时使用粗粒度，“小型车辆”时使用细粒度），或引入自适应缩放因子以匹配目标尺度。

4. **框架泛化潜力**：GeoViS的搜索-定位框架目前仅验证于遥感图像定位任务。其核心思想——通过奖励驱动的层次化搜索逐步聚焦信息丰富子区域——具有向其他视觉定位任务泛化的潜力，如自然图像中的指代表达理解（Referring Expression Comprehension）、视频目标定位、三维点云中的目标检测等。这些场景同样面临全局-局部信息权衡的挑战，但动作空间和奖励函数需要针对性重新设计。

5. **训练数据依赖性**：GeoViS的训练依赖于具有边界框标注的遥感定位数据集，而此类数据的标注成本远高于自然图像。如何利用弱监督或自监督信号训练搜索策略，降低对精确框标注的依赖，是推动方法实际应用的重要方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/GeoViS_Geospatially_Rewarded_Visual_Search_for_Remote_Sensing_Visual_Grounding.pdf]]
