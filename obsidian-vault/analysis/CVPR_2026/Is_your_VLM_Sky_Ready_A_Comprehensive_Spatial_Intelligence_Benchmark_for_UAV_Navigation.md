---
title: Is your VLM Sky-Ready? A Comprehensive Spatial Intelligence Benchmark for UAV Navigation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Is_your_VLM_Sky_Ready_A_Comprehensive_Spatial_Intelligence_Benchmark_for_UAV_Navigation.pdf
project_link: null
code_link: "https://github.com/linglingxiansen/SpatialSKy"
aliases:
- SV
- IYVSRCSIBUN
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 通过构建覆盖13种空间推理任务的大规模多模态数据集（SpatialSky-Dataset），并引入监督微调+基于GRPO的强化微调两阶段训练，赋予VLM无人机场景特有的空间推理能力。
primary_logic: 专门针对无人机视角的空间推理训练能大幅提升VLM的环境感知与场景理解能力，Sky-VLM在SpatialSky-Bench上取得SOTA，验证了领域数据与强化微调的关键作用。
claims:
- Sky-VLM在SpatialSky-Bench总体平均分达到53.30，较最佳基线GPT-5（23.07）提升139.6%，且在所有13项子任务上均领先。
- 两阶段训练（SFT后接GRPO强化微调）使总平均分从48.29提升至53.30，证明RFT能显著增强空间决策能力。
- 移除点定位奖励后环境感知平均分从60.33骤降到53.77，表明任务特定奖励（特别是点定位）对空间推理精度至关重要。
- SpatialSky-Bench 上 总体平均分 (Avg.) = 53.30
---

# Is your VLM Sky-Ready? A Comprehensive Spatial Intelligence Benchmark for UAV Navigation

> [!tip] 核心洞察
> 专门针对无人机视角的空间推理训练能大幅提升VLM的环境感知与场景理解能力，Sky-VLM在SpatialSky-Bench上取得SOTA，验证了领域数据与强化微调的关键作用。

| 字段 | 内容 |
|------|------|
| 中文题名 | 天空就绪？面向无人机导航的VLM空间智能基准测试 |
| 英文题名 | Is your VLM Sky-Ready? A Comprehensive Spatial Intelligence Benchmark for UAV Navigation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.13269) · [Code](https://github.com/linglingxiansen/SpatialSKy) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | Sky-VLM |
| Dataset | SpatialSky-Bench |

> [!tip] 效果简介
> - SpatialSky-Bench 上，总体平均分 (Avg.) 53.30 vs GPT-5 23.07 (+139.6%)；边界框定位 (Box mIoU) 42.68 vs SpaceR 7.44 (+473%)；颜色识别 (Color) 79.00 vs SpatialVLM 50.00 (+58%)。

## 概要

**核心问题：** 现有视觉语言模型（VLM）在无人机（UAV）俯视视角下普遍缺乏空间智能——难以准确理解物体间的深度、高度、相对位置等三维空间关系，导致在UAV导航任务中表现不佳。当前主流VLM（如GPT-5、Gemini-2.5、InternVL3.5等）在该场景下的空间推理能力存在明显短板。

**核心贡献：** 本文提出了一套完整的“数据—基准—模型”解决方案：
1. **SpatialSky-Dataset**：一个覆盖13种空间推理任务的大规模多模态数据集（100万样本），整合RGB图像、语义分割、LiDAR深度和UAV位姿信息，通过自动化流水线生成多样化问答对。
2. **SpatialSky-Bench**：首个专门面向UAV导航场景的VLM空间智能评测基准，涵盖环境感知（8项子任务）与场景理解（5项子任务）两大类别。
3. **Sky-VLM**：基于Qwen2.5-VL-7B，采用“监督微调（SFT）+ GRPO强化微调（RFT）”两阶段训练策略，并引入任务特定奖励函数（点定位L1距离、边界框IoU、选择题精确匹配）来显著提升空间决策精度。

**核心结论：** Sky-VLM在SpatialSky-Bench上取得SOTA，总体平均分达53.30，较最佳基线GPT-5（23.07）提升139.6%，且在全部13项子任务上均领先。消融实验证实：两阶段训练（SFT→RFT）使总分从48.29提升至53.30；移除点定位奖励后环境感知平均分从60.33骤降至53.77，验证了任务特定奖励对空间推理精度的关键作用。数据规模律进一步显示，训练样本从30万增至100万时，SFT准确率从30.43跃升至48.29，经RFT后进一步提升至53.30，表明领域数据规模与强化学习之间存在显著的协同增益。

**方法定位：** 本文工作属于“领域特定空间推理能力注入”范式——不改变基础VLM架构，而是通过大规模无人机视角空间推理数据与强化微调的组合，将通用VLM适配为具备俯视空间智能的专用模型。该方法在空间VLM谱系中填补了无人机导航场景的空白，与SpatialVLM（Chen et al., CVPR 2024）和SpaceR（Ouyang et al., arXiv 2025）等地面空间推理工作形成互补。

无人机（UAV）在物流配送、灾害救援、农业监测等领域的应用日益广泛，其自主导航能力高度依赖对三维空间环境的精确理解。视觉语言模型（VLM）在通用场景的视觉推理上取得了显著进展，然而，当将其直接应用于无人机俯视视角时，一个关键的瓶颈浮现：现有VLM普遍缺乏该视角下的空间智能，难以准确理解物体间的深度、高度、相对位置等关系，导致在导航相关任务中表现不佳。

这一缺口的根源在于领域数据的缺失与训练范式的错配。通用VLM的训练语料以地面平视或斜视图像为主，缺乏大规模、多模态的无人机场景标注数据来注入俯视空间推理的先验。同时，标准的监督微调策略仅优化语言生成目标，无法显式地约束模型输出精确的空间坐标或几何关系，使得模型在需要米级精度或像素级定位的任务上难以收敛至可用水平。

为系统性地诊断并填补这一空白，本文构建了**SpatialSky-Bench**，一个覆盖环境感知与场景理解两大类别、共13项细粒度子任务的综合基准。在此基础上，本文进一步提出**Sky-VLM**——基于Qwen2.5-VL-7B构建、专为无人机空间推理设计的视觉语言模型。其核心动机在于验证一个假设：通过大规模领域数据注入与任务特定奖励信号的联合驱动，VLM能够从“地面通才”跃迁为“天空专家”，在俯视空间智能上取得质的突破。

## 核心方法与创新机理

Sky‑VLM 的核心创新并非提出全新的模型架构，而是系统性地解决了 **VLM 在无人机俯视视角下空间智能缺失** 这一瓶颈。其创新链由三个紧密耦合的 changed slots 构成：**领域专用数据集 → 两阶段训练策略 → 任务特定奖励设计**。

### 1. 领域数据：从通用视觉到无人机空间感知

现有 VLM 的训练数据以通用图文对为主，缺乏无人机场景特有的俯视视角、深度关系和空间交互标注。Sky‑VLM 构建了 **SpatialSky‑Dataset**（100 万样本），覆盖 13 种空间推理任务，其关键创新在于：

- **多模态真值融合**：同时利用 RGB 图像、语义分割掩码、LiDAR 点云和无人机位姿信息，通过 VLM 辅助生成与人工专家验证的流水线自动产生高质量问答对（Figure 3）。
- **空间关系的形式化建模**：利用分割掩码质心计算物体间角度与欧氏距离（公式 $\theta_{ij} = \arctan \left( \frac{\bar{y}_j - \bar{y}_i}{\bar{x}_j - \bar{x}_i} \right), \quad d_{ij} = \| c_i - c_j \|_2$），以及 LiDAR 点云计算物体在相机坐标系下的平均深度（$d_{\mathrm{obj}} = \frac{1}{|\mathcal{P}_{\mathrm{obj}}|} \sum_{p_k \in \mathcal{P}_{\mathrm{obj}}} z_k^{\mathrm{cam}}$），为空间推理提供精确的数值监督信号。

这一数据集使模型首次从“看图像”转变为“理解三维空间中的物体关系”，是后续训练增益的基础。

### 2. 训练策略：SFT 奠基 + GRPO 强化微调

基线方法通常仅采用单阶段监督微调。Sky‑VLM 引入 **两阶段训练**：

- **第一阶段 SFT**：在 100 万样本上以标准交叉熵损失（仅计算答案部分）训练，使模型获得无人机视角的基本空间推理能力和任务特定输出格式。
- **第二阶段 RFT with GRPO**：在 SFT 模型基础上，对点定位、边界框和选择题等关键空间决策任务施加强化微调，优化目标为最大化任务奖励的同时约束与参考策略的 KL 散度（$\mathcal{L}_{\mathrm{GRPO}} = -\mathbb{E}_{\pi_\theta} \left[ R(y) \cdot \log \frac{\pi_\theta(y|x)}{\pi_{\mathrm{ref}}(y|x)} \right] + \beta \cdot \mathbf{KL}(\pi_\theta || \pi_{\mathrm{ref}})$）。

消融实验（Table 2）直接验证了这一创新的因果效应：SFT 使总平均分从 30.43 提升至 48.29，而 RFT 进一步推高至 53.30，表明强化微调能显著增强空间决策精度。

### 3. 奖励设计：任务特定奖励函数

通用 VLM 训练仅依赖语言建模损失，无法直接优化空间定位精度。Sky‑VLM 的核心创新在于为不同任务设计了 **可微分的奖励信号**：

- **点定位奖励**：基于 L1 距离的阈值奖励（$R_{\mathrm{point}} = \begin{cases} 1, & \text{if } |x_{\mathrm{pred}} - x| + |y_{\mathrm{pred}} - y| \leq 50, \\ 0, & \text{otherwise.} \end{cases}$），直接优化像素级定位精度。
- **边界框奖励**：基于预测框与真值框的 IoU 计算奖励。
- **选择题奖励**：精确匹配正确答案给予奖励。

奖励消融实验（Table 3）揭示了这一设计的决定性作用：**移除点定位奖励后，环境感知平均分从 60.33 骤降至 53.77**，证明点定位奖励对精确空间感知的贡献最大。

### 创新协同效应

三个 changed slots 并非孤立改进，而是形成正向协同：领域数据提供了空间推理的“原料”，SFT 将其转化为基础能力，RFT 的任务奖励则像“精准调校器”，在关键决策点上进一步缩小误差。数据规模律（Figure 7）显示，训练数据从 30 万增至 100 万时，SFT 准确率从 30.43 跃升至 48.29，经 RFT 后达 53.30，验证了数据规模与强化学习的协同增益。

### 创新边界与局限

需注意该创新链的适用范围：
- 训练数据源自 UAVScenes 数据集，对极端场景或新型物体的泛化能力有待验证。
- 仅基于 Qwen2.5‑VL‑7B 进行训练，未探索更大规模模型或不同架构的影响。
- RFT 仅覆盖点定位、边界框和选择题任务，其他开放式任务未获得奖励信号的直接优化。

Sky-VLM 的整体框架围绕“无人机俯视视角下的空间智能”这一核心瓶颈设计，采用**数据生成—监督微调—强化微调**三阶段流水线，将通用 VLM 转化为具备 13 种空间推理能力的 UAV 导航专家模型。

### 数据生成流水线：SpatialSky-Dataset

训练数据的质量与覆盖面是整个框架的基石。SpatialSky-Dataset 的生成流水线（Figure 3）以多模态输入为起点，包括 RGB 图像、语义分割掩码、LiDAR 点云、UAV 位姿信息以及物体边界框。生成过程分为两步：

1. **自动标注与问题生成**：利用 VLM 驱动的自动化方法，基于上述多模态真值生成多样化的问答对。例如，空间关系类别通过计算两物体掩码质心间的角度 $\theta_{ij}$ 和欧氏距离 $d_{ij}$ 来判定（公式(1)），物体深度则从 LiDAR 点云计算相机坐标系下的平均深度 $d_{\mathrm{obj}}$（公式(2)）。
2. **人工专家验证**：对自动生成的数据进行质量审核，确保标注准确性和任务合理性。

该流水线最终产出 **100 万样本**，覆盖 **13 种空间推理任务**，分为环境感知（8 项：距离、反向点定位、自由空间、空间关系、计数、功能识别、高度估计、颜色识别）和场景理解（5 项：着陆安全评估、路径规划等）两大类，包含开放式问答、选择题、点定位和边界框等多种标注格式。

### 两阶段训练框架：SFT → RFT

Sky-VLM 以 **Qwen2.5-VL-7B** 为基础模型，采用两阶段训练策略（Figure 4）：

![[assets/figures/papers/paper_list_l2152_https_arxiv_org_abs_2511_13269/figures/006_Figure_4.jpg]]
*Figure 4: Overview of our Sky-VLM. Sky-VLM adopts a two-stage training approach. In the first stage, we involve supervised finetuning (SFT) on the entire SpatialSky-Dataset to develop the basic spatial reasoning capabilities. In the second stage, we use reinforcement fine-tuning (RFT), utilizing task-specific reward functions to enhance decision-making accuracy for key spatial tasks*

**第一阶段：监督微调（SFT）**
在完整的 100 万样本 SpatialSky-Dataset 上进行监督微调。损失函数仅对答案部分（位置 $k$ 到 $n$）计算交叉熵：

$$\mathcal{L}_{\mathrm{SFT}} = -\frac{1}{n-k+1} \sum_{i=k}^{n} \log P(t_i | \mathbf{V}, t_1, ..., t_{i-1}; \theta)$$

这一设计使模型专注于学习正确答案的生成模式，而非浪费容量在问题部分的语言建模上。SFT 阶段使用 8 块 H200 GPU，AdamW 优化器，学习率 1e-5，每设备批次大小 2，梯度累积步数 2，训练 1 个 epoch。此阶段赋予模型基础的无人机视角空间推理能力，SFT 后模型在 SpatialSky-Bench 上的总平均分达到 48.29。

**第二阶段：强化微调（RFT）with GRPO**
在 SFT 基础上，使用 GRPO（Group Relative Policy Optimization）对 3 万样本进行强化微调，引入任务特定的奖励函数来优化决策精度：

- **点定位奖励**：基于 L1 距离的硬阈值奖励，当预测坐标与真值的曼哈顿距离不超过 50 像素时给予正向奖励。
- **边界框奖励**：基于预测框与真值框的 IoU 计算奖励信号。
- **选择题奖励**：精确匹配正确答案时给予奖励。

GRPO 优化目标在最大化任务奖励的同时，通过 KL 散度约束 $\beta \cdot \mathbf{KL}(\pi_\theta || \pi_{\mathrm{ref}})$ 防止新策略过度偏离参考策略，保证训练稳定性。RFT 阶段使用学习率 1e-6，权重衰减 0.1，KL 系数 $\beta = 0.01$。

### 模块间关系与信息流

整个框架的信息流为：**多模态原始数据 → 自动标注生成 → 100 万训练样本（SpatialSky-Dataset）→ SFT 获得基础空间推理 → RFT 优化关键任务决策 → Sky-VLM 推理模型**。两阶段训练形成递进关系：SFT 提供广泛的领域知识覆盖，RFT 则通过奖励信号对点定位、边界框和选择题等可精确评估的任务进行针对性强化。消融实验表明，移除点定位奖励后环境感知平均分从 60.33 骤降至 53.77，验证了任务特定奖励在框架中的关键作用。

![[assets/figures/papers/paper_list_l2152_https_arxiv_org_abs_2511_13269/figures/001_Figure_1.jpg]]
*Figure 1: Overview of SpatialSky-Bench. Our benchmarks are divided into two categories: Environmental Perception and Scene Understanding, covering a total of 13 subcategories. We evaluated the VLM’s spatial intelligence capabilities across these UAV navigation tasks*

### 3.1 空间感知数据生成模块

Sky-VLM的核心能力源于SpatialSky-Dataset的构建，该数据集通过自动化流水线从多模态输入中生成覆盖13种空间推理任务的问答对。其关键模块如下：

- **多模态输入融合**：流水线接收RGB图像、语义分割掩码、LiDAR点云和无人机位姿信息，为每个物体实例提供丰富的空间属性。
- **环境感知任务生成**：基于物体掩码质心和深度信息，自动生成8类细粒度空间推理问题，包括距离估计、反向定位、自由空间判断、空间关系分类、颜色识别、计数、物体尺寸和高度估计。
- **场景理解任务生成**：涵盖5类高层认知任务，如着陆安全评估、功能推理、路径规划、场景描述和异常检测，要求对航拍场景进行整体推理。

### 3.2 空间关系量化公式

为判定两个物体间的空间关系类别，系统首先计算掩码质心间的几何关系：

$$
\theta_{ij} = \arctan \left( \frac{\bar{y}_j - \bar{y}_i}{\bar{x}_j - \bar{x}_i} \right), \quad d_{ij} = \| c_i - c_j \|_2
$$

其中 $c_i = (\bar{x}_i, \bar{y}_i)$ 为物体 $i$ 的分割掩码质心坐标，$\theta_{ij}$ 为两物体间的方向角，$d_{ij}$ 为欧氏距离。根据角度和距离阈值，将空间关系划分为“左/右/前/后/近/远”等离散类别。

### 3.3 深度与高度估计公式

物体深度通过LiDAR点云在相机坐标系下的投影计算：

$$
d_{\mathrm{obj}} = \frac{1}{|\mathcal{P}_{\mathrm{obj}}|} \sum_{p_k \in \mathcal{P}_{\mathrm{obj}}} z_k^{\mathrm{cam}}
$$

其中 $\mathcal{P}_{\mathrm{obj}}$ 为属于该物体的LiDAR点集，$z_k^{\mathrm{cam}}$ 为点在相机坐标系下的深度值。

高度估计则利用无人机位姿变换矩阵 $\mathbf{T}_{4\times4}$ 将LiDAR点转换到世界坐标系，通过计算物体点云在世界坐标系下的 $z$ 轴极差得到物体真实高度。这一过程依赖无人机提供的精确位姿信息，是俯视视角下高度感知的关键。

### 3.4 边界框定位评估指标

边界框定位任务采用平均交并比（mIoU）作为评估指标：

$$
\mathrm{mIoU} = \frac{1}{N} \sum_{i=1}^{N} \frac{|B_{\mathrm{pred}}^i \cap B_{\mathrm{gt}}^i|}{|B_{\mathrm{pred}}^i \cup B_{\mathrm{gt}}^i|}
$$

其中 $B_{\mathrm{pred}}^i$ 和 $B_{\mathrm{gt}}^i$ 分别为第 $i$ 个实例的预测边界框与真值边界框，$N$ 为实例总数。

### 3.5 监督微调损失函数

在SFT阶段，模型仅对答案部分计算交叉熵损失，使训练聚焦于生成正确答案：

$$
\mathcal{L}_{\mathrm{SFT}} = -\frac{1}{n-k+1} \sum_{i=k}^{n} \log P(t_i | \mathbf{V}, t_1, ..., t_{i-1}; \theta)
$$

其中 $\mathbf{V}$ 为输入图像，$t_1,...,t_n$ 为完整的目标序列，答案部分从位置 $k$ 到 $n$，$\theta$ 为模型参数。该设计避免了模型在问题描述部分浪费学习容量。

### 3.6 强化微调奖励函数

RFT阶段采用GRPO算法，针对不同任务类型设计特定奖励：

- **点定位奖励**：基于L1距离的二元奖励，阈值为50像素：

$$
R_{\mathrm{point}} = \begin{cases} 1, & \text{if } |x_{\mathrm{pred}} - x| + |y_{\mathrm{pred}} - y| \leq 50, \\ 0, & \text{otherwise.} \end{cases}
$$

- **边界框奖励**：采用预测框与真值框的IoU作为连续奖励信号。
- **选择题奖励**：精确匹配正确选项时给予奖励。

GRPO的优化目标在最大化任务奖励的同时，通过KL散度约束防止策略过度偏离参考策略：

$$
\mathcal{L}_{\mathrm{GRPO}} = -\mathbb{E}_{\pi_\theta} \left[ R(y) \cdot \log \frac{\pi_\theta(y|x)}{\pi_{\mathrm{ref}}(y|x)} \right] + \beta \cdot \mathbf{KL}(\pi_\theta || \pi_{\mathrm{ref}})
$$

其中 $\pi_\theta$ 为当前策略，$\pi_{\mathrm{ref}}$ 为SFT后的参考策略，$\beta$ 为KL正则化系数（设为0.01）。消融实验证实，点定位奖励对环境感知能力的贡献最为显著——移除该奖励后环境感知平均分从60.33骤降至53.77（Table 3）。

### 3.7 两阶段训练流水线

Sky-VLM的训练分为两个阶段（Figure 4）：

1. **SFT阶段**：在100万样本上以学习率1e-5、批量大小2（每设备）、2步梯度累积训练1个epoch，使用8张H200 GPU和AdamW优化器。此阶段赋予模型基础的无人机视角空间推理能力和任务特定输出格式。
2. **RFT阶段**：在3万样本上以学习率1e-6、权重衰减0.1进行GRPO强化微调，利用任务特定奖励优化点定位、边界框和选择题的决策精度。两阶段训练使总平均分从48.29提升至53.30（Table 2），验证了强化微调对空间决策能力的增强作用。

## 实验与关键发现

### 主要结果：SpatialSky-Bench 全局对比

Sky-VLM 在 SpatialSky-Bench 的 13 项子任务上全面超越现有 VLM，确立了无人机空间推理的新 SOTA。Table 1 汇总了各模型在环境感知与场景理解两大类别下的表现，核心发现如下：

![[assets/figures/papers/paper_list_l2152_https_arxiv_org_abs_2511_13269/figures/008_Table_1.jpg]]
*Table 1: Comparison Results of Various VLMs on SpatialSky-Bench. Our Sky-VLM achieves SOTA performance. Dist., Rev., Free., Sp. Rel., Cou., Fun., Land., Avg., denote distance, reverse point, freespace, spatial relation, counting, function, landing and total average*

- **总体平均分**：Sky-VLM 达到 **53.30**，较最强基线 GPT-5 的 23.07 提升 **139.6%**。开源模型中，InternVL3.5 仅获 19.36，Qwen2.5-VL-7B（基础模型）仅 12.97，说明通用 VLM 在俯视空间推理上存在严重能力短板。
- **边界框定位（Box mIoU）**：Sky-VLM 取得 **42.68**，相较 SpaceR 的 7.44 提升 **473%**。该任务要求模型直接输出目标边界框坐标，对空间精度要求极高，多数基线几乎完全失效。
- **颜色识别（Color）**：Sky-VLM 达 **79.00**，较 SpatialVLM 的 50.00 提升 58%，表明领域训练有效克服了俯视视角下的属性感知退化。
- **空间关系（Sp. Rel.）**：Sky-VLM 获 **70.00**，较 InternVL3.5 的 50.63 提升 38.3%，证明模型习得了俯视场景中物体间方位与距离的判别能力。
- **着陆安全（Land.）**：Sky-VLM 达 **61.40**，较 Qwen-VL-Max 的 56.11 提升 9.4%。该任务涉及综合场景理解，提升幅度相对较小，反映出高层决策任务的固有难度。

值得注意的是，闭源模型 GPT-5 与 Gemini-2.5 在多项任务上表现优于开源基线，但在边界框定位等精确空间输出任务上同样表现不佳，说明仅靠模型规模无法弥补领域空间知识的缺失。

### 消融实验：训练策略的贡献

Table 2 揭示了两阶段训练中各组件的独立贡献：

![[assets/figures/papers/paper_list_l2152_https_arxiv_org_abs_2511_13269/figures/009_Table_2.jpg]]
*Table 2: Ablation Study of Multi-Stage Training*

- **仅 SFT** 阶段后，模型总平均分为 **48.29**，已大幅超越所有基线。
- **SFT + RFT（GRPO 强化微调）** 将总平均分进一步提升至 **53.30**，净增 5.01 分。这表明强化微调能在监督学习的基础上，通过任务奖励信号精细优化空间决策精度。

Figure 7 展示了数据规模律：当训练样本从 30 万增至 100 万时，SFT 准确率从 30.43 跃升至 48.29；再经 RFT 后达到 53.30。数据量与强化学习之间存在明显的协同增益效应。

### 奖励函数消融

Table 3 针对 RFT 阶段的任务奖励进行了组件消融：

![[assets/figures/papers/paper_list_l2152_https_arxiv_org_abs_2511_13269/figures/012_Table_3.jpg]]
*Table 3: Ablation Study of Reward Model*

- **移除点定位奖励**后，环境感知平均分从 60.33 骤降至 **53.77**，降幅达 6.56 分。该奖励基于 L1 距离阈值（≤50 像素），直接约束模型的空间输出精度，是环境感知任务的核心驱动信号。
- 边界框奖励（基于 mIoU）和选择题奖励（精确匹配）的移除同样导致对应子任务性能下降，但影响幅度小于点定位奖励。

这一发现说明，在无人机俯视场景中，**精确的点级空间定位能力是其他高层推理任务的基础**，任务特定奖励设计对强化微调的成功至关重要。

### 定性分析与失败模式

Figure 6 展示了不同 VLM 在典型场景下的定性对比。Sky-VLM 在距离估计、空间关系判断等任务上输出更接近真值，而基线模型常出现方向颠倒、深度误判等系统性错误。

![[assets/figures/papers/paper_list_l2152_https_arxiv_org_abs_2511_13269/figures/010_Figure_6.jpg]]
*Figure 6: Qualitative Results of Different VLMs on SpatialSky-Bench*

结合 limitations 中的分析，当前方法的主要失败模式包括：

1. **泛化边界受限**：训练数据源自 UAVScenes 数据集，对极端天气、光照条件或未见物体类别的鲁棒性未经验证，实际部署中可能出现性能退化。
2. **开放式任务未直接优化**：RFT 仅覆盖点定位、边界框和选择题，计数、功能判断等开放式任务未获得奖励信号，其性能提升完全依赖 SFT 阶段的迁移，可能存在上限。
3. **单一模型架构**：仅基于 Qwen2.5-VL-7B 验证，未探索更大规模模型或不同视觉编码器的影响，方法在其他架构上的可迁移性需进一步验证。
4. **自动评估偏差**：开放式任务的评分依赖 GPT-4o 作为评判器，虽经人工验证，但在边缘案例上仍可能引入系统性偏差。

### 关键图表索引

- **Table 1**：各 VLM 在 SpatialSky-Bench 13 项子任务上的完整对比，Sky-VLM 全面领先。
- **Table 2**：多阶段训练消融，验证 SFT→RFT 的递进增益。
- **Table 3**：奖励函数组件消融，揭示点定位奖励的核心作用。
- **Figure 6**：定性对比示例，直观展示不同模型的输出差异。
- **Figure 7**：数据规模律曲线，展示训练数据量与准确率的 scaling 关系。

## 定位与知识库关联

### 与基线方法的关系

Sky-VLM 的方法定位是“无人机俯视视角下的专用空间推理 VLM”，其能力边界与通用 VLM 及现有空间 VLM 形成鲜明对比。在 SpatialSky-Bench 上，所有对比基线均表现不佳，根本原因在于它们缺乏无人机场景特有的俯视空间理解训练：

- **通用闭源 VLM**（**GPT-5**、**Gemini-2.5** (Comanici et al., arXiv 2025)、**Qwen-VL-Max**）在总体平均分上均未超过 24 分，尤其在需要精确像素级定位的任务（如边界框定位 mIoU 接近 0）上几乎完全失效。这表明即使是最强的通用多模态模型，在未曾见过的俯视视角空间关系上也缺乏零样本泛化能力。
- **开源 VLM**（**Qwen2.5-VL-7B** (Bai et al., arXiv 2025)、**InternVL3.5** (Wang et al., arXiv 2025)）同样表现不佳，Qwen2.5-VL-7B 作为 Sky-VLM 的基础模型，其 SFT 前在基准上的得分极低，进一步验证了领域数据的关键作用。
- **专用空间 VLM**（**SpatialVLM** (Chen et al., CVPR 2024)、**SpaceR** (Ouyang et al., arXiv 2025)）虽针对空间推理设计，但其训练数据以地面视角为主，在无人机俯视场景下同样出现严重的领域偏移。SpaceR 在边界框定位任务上仅得 7.44 mIoU，而 Sky-VLM 达到 42.68，提升 473%。

Sky-VLM 的突破并非来自架构创新，而是通过 **SpatialSky-Dataset（100 万俯视视角多模态样本）+ 两阶段训练（SFT → GRPO 强化微调）** 的组合，将通用 VLM 的表示能力“锚定”到无人机空间推理这一特定领域。

### 适用边界

Sky-VLM 的适用边界由以下要素共同划定：

1. **视角依赖性**：模型的空间推理能力高度依赖俯视视角。训练数据全部来自 UAVScenes 数据集的航拍图像，对于地面视角、倾斜视角或极端低空/高空视角的空间理解能力未经验证。
2. **物体类别覆盖**：训练数据覆盖 22 个物体类别，主要面向城市场景中的常见地物（建筑、道路、车辆、植被等）。对于未见过的物体类别或高度专业化的场景（如搜救、工业巡检中的特定设备），泛化能力存疑。
3. **静态图像推理**：当前 Sky-VLM 仅处理单帧静态图像的空间推理，不涉及视频流的时序信息或连续导航决策。从静态空间理解到动态导航规划之间存在关键的能力缺口。
4. **基础模型规模**：仅基于 Qwen2.5-VL-7B（7B 参数）进行训练，未探索更大规模模型（如 13B、34B）或不同视觉编码器架构的影响。更大模型是否能在该任务上获得更好的数据效率或更强的泛化能力仍是开放问题。

### 局限与开放问题

**已知局限**（来自论文自身披露与实验分析）：

- **数据来源单一**：训练数据仅来自 UAVScenes 数据集，可能限制了对极端天气、光照条件、地理区域或新型物体的泛化能力。
- **强化微调覆盖不全**：GRPO 强化微调仅应用于点定位、边界框和选择题三类任务，其他开放式任务（如自由空间描述、功能推理）未获得奖励信号的直接优化，其性能提升主要依赖 SFT 阶段的表示学习。
- **自动评估偏差**：基准中的开放式任务评分依赖 GPT-4o 作为自动评估器，可能引入评估偏差，尽管论文提到有人工专家验证数据生成质量，但未对评估环节进行类似的人工校准。

**开放问题**：

1. **从静态到动态的扩展**：如何将 Sky-VLM 的空间推理能力从单帧图像扩展到在线视频流和实时导航决策？这需要引入时序建模和动作预测模块，同时保持空间理解的精度。
2. **跨具身迁移**：所提出的俯视空间智能能否迁移到地面机器人、自动驾驶等其他具身智能任务？视角变换带来的领域偏移程度需要系统评估。
3. **多模态融合优化**：当前方法将 RGB、LiDAR、位姿信息作为输入生成文本标注，但训练时 VLM 仅接收 RGB 图像和文本问答对。更高效的多模态传感器对齐方法（如直接融合深度图或点云特征）是否能进一步提升空间推理精度？
4. **真实部署的鲁棒性**：在真实无人机飞行环境中部署时，模型的推理延迟、对传感器噪声的鲁棒性以及安全关键场景下的可靠性如何保证？这需要从系统层面进行端到端验证。
5. **奖励设计的泛化性**：当前点定位奖励使用固定的 L1 距离阈值（50 像素），这一阈值在不同分辨率、不同飞行高度下的适用性需要进一步研究。自适应奖励函数或基于物理距离的奖励设计可能是改进方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Is_your_VLM_Sky_Ready_A_Comprehensive_Spatial_Intelligence_Benchmark_for_UAV_Navigation.pdf]]
