---
title: "Seeing Across Views: Benchmarking Spatial Reasoning of Vision-Language Models in Robotic Scenes"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Seeing_Across_Views_Benchmarking_Spatial_Reasoning_of_Vision_Language_Models_in_Robotic_Scenes.pdf
project_link: https://aaronfengzy.github.io/MV-RoboBench-Webpage/
code_link: https://github.com/microsoft/MV-RoboBench
openreview_forum_id: jXDZJAfRZB
aliases:
- MR
- SAVBSRVLMRS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "显式引入几何先验（深度估计、新视角合成）和结构化思维链（CoT）推理能在具备足够容量的模型中显著提升多视角空间对齐与一致性判断；模型容量是有效利用增强信息的关键门槛。"
primary_logic: "通用单视图空间推理能力不能可靠地迁移至多视图机器人操作场景；空间感知与机器人执行在多视图条件下呈正相关，但仅当模型具备足够的跨视角融合能力时才会显现，因此亟需专门的 embodied 多视图评测基准。"
claims:
- "最先进的 GPT-5 在 MV-RoboBench 上仅获得 56.41% 的平均准确率，而人类可达 91.04%；非推理模型在 3D 空间一致性等任务中接近随机猜测 (19.07%)。"
- "多视图输入对强模型（GPT-5）的 Distance Judgement 提升达 +18.90%，但对小模型（Qwen2.5-vl-32b）几乎无正面影响，证明多视图融合能力存在容量门槛。"
- "在 OmniSpatial 单视图基准测试上表现良好的模型，在 MV-RoboBench 的多视图空间与机器人任务上仍接近随机水平，表明单视图能力无法转移。"
- "CoT 风格的增强（深度先验、新视角合成）仅对具有足够容量的模型带来显著提升，而对小模型无效甚至有害，说明浅层提示增强不能替代显式的几何推理。"
---

# Seeing Across Views: Benchmarking Spatial Reasoning of Vision-Language Models in Robotic Scenes

> [!tip] 核心洞察
> 通用单视图空间推理能力不能可靠地迁移至多视图机器人操作场景；空间感知与机器人执行在多视图条件下呈正相关，但仅当模型具备足够的跨视角融合能力时才会显现，因此亟需专门的 embodied 多视图评测基准。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 跨视角观察：面向机器人场景的多视角空间推理基准测试 |
| 英文题名 | Seeing Across Views: Benchmarking Spatial Reasoning of Vision-Language Models in Robotic Scenes |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=jXDZJAfRZB) · [GitHub](https://github.com/microsoft/MV-RoboBench) · [Project](https://aaronfengzy.github.io/MV-RoboBench-Webpage/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | MV-RoboBench |
| Dataset | MV-RoboBench (Overall), MV-RoboBench (3D Spatial Consistency), MV-RoboBench (Action Planning) |

> [!tip] 效果简介
> - MV-RoboBench (Overall) 上，Accuracy (%) 为 56.41 (GPT-5, highest model)，对比 19.71 (Random Choice)，变化 +36.70。
> - MV-RoboBench (Overall) 上，Accuracy (%) 为 56.41 (GPT-5)，对比 91.04 (Human upper bound)，变化 -34.63 (gap to human)。
> - MV-RoboBench (3D Spatial Consistency) 上，Accuracy (%) 为 82.35 (GPT-5)，对比 19.07 (Random Choice)，变化 +63.28。

## 概要

当前视觉–语言模型（VLMs）在融合多视角输入以构建统一三维表示方面能力薄弱，常依赖屏幕位置、表观尺寸等二维启发式进行判断，而非真正的三维推理。这导致模型在深度模糊、遮挡和跨视角一致性等任务上表现接近随机水平。通用单视图空间推理能力无法可靠地迁移至多视图机器人操作场景——在单视图基准上表现良好的模型，在多视图机器人任务中仍可能接近随机猜测。

MV-RoboBench 是首个面向具身机器人操作场景的多视角空间推理基准，基于 AgiWorld 和 BridgeV2 真实机器人操作数据集构建，包含 1.7K 人工精标注的多选题样本，覆盖空间理解与机器人执行两大领域的八个子任务。与现有基准相比，MV-RoboBench 在三个关键维度上形成差异化：支持完全同步的多视图输入（现有基准多为单视图或仅部分多视图）、将评测从纯空间理解拓展至机器人执行规划、采用真实机器人操作场景替代通用室内或网络图像（Table 1）。

最先进的 GPT-5 在 MV-RoboBench 上仅获得 56.41% 的平均准确率，而人类可达 91.04%，差距达 34.63 个百分点（Table 2）。非推理模型在 3D 空间一致性等任务中准确率低至 19.07%，接近随机猜测水平。多视图输入对强模型存在显著增益——GPT-5 在距离判断任务上提升 +18.90%——但对小模型几乎无正面影响，揭示多视图融合存在明显的模型容量门槛（Table 7）。显式引入几何先验（深度估计、新视角合成）的结构化思维链增强仅在具备足够容量的模型上带来提升，对小模型无效甚至有害（Table 3），表明浅层提示增强不能替代真正的几何推理能力。



### 视觉–语言模型的空间推理困境

视觉–语言模型（VLMs）近年来在通用视觉理解任务上取得了显著进展，但其空间推理能力——尤其是面向机器人操作场景的空间推理——仍处于早期探索阶段。现有空间推理基准测试，如 **EmbSpatial-Bench**（Du et al., 2024）、**Visual Spatial**（Liu et al., 2023a）和 **RoboSpatial**（Song et al., 2025a），主要聚焦于单视图场景下的空间关系判断。这些基准测试的典型任务包括：给定单张图像，判断物体的相对位置、方向或空间布局。然而，机器人操作本质上是一个多视图问题——机械臂需要在多个摄像头视角之间建立一致的 3D 空间表示，才能完成精确的抓取、放置和路径规划。

### 现有基准测试的结构性缺口

当前空间推理基准测试存在三个结构性缺口，严重限制了它们对 embodied 场景的适用性：

**第一，多视图支持的缺失。** 绝大多数现有基准测试仅提供单视图输入（Table 1）。少数声称支持多视图的基准测试，如 **All-Angles Bench**（Yeh et al., 2025），其多视图样本仅占数据集的子集，且缺乏与机器人操作的耦合。这意味着模型可以在不进行跨视角对齐的情况下完成大部分任务，无法评估真正的多视图融合能力。

**第二，领域覆盖的割裂。** 现有基准测试要么专注于抽象空间推理（如互联网图像中的物体关系判断），要么专注于机器人任务（如 **ShareRobot**，Ji et al., 2025），但缺乏将空间理解与机器人执行统一起来的评测框架。这种割裂导致一个关键问题被忽视：模型在空间推理上的能力是否能可靠地迁移到机器人操作任务中？

**第三，场景真实性的不足。** 现有基准测试多使用通用室内场景、互联网图像或第一人称视频，而非真实的机器人操作环境。这些场景缺乏机器人操作特有的视觉复杂性：多摄像头同步、机械臂遮挡、操作台面的深度模糊以及抓取视角的非规范性。

### 核心问题：单视图能力能否迁移至多视图 embodied 场景？

上述缺口指向一个根本性的研究问题：**通用单视图空间推理能力能否可靠地迁移至多视图机器人操作场景？** 初步证据表明答案是否定的。在 **OmniSpatial** 单视图基准测试上表现良好的模型，在 MV-RoboBench 的多视图空间与机器人任务上仍接近随机水平（Figure 6）。这表明，单视图空间推理依赖的 2D 启发式策略——如屏幕位置、表观尺寸——无法自动转化为真正的三维几何推理。

### 瓶颈机制：2D 启发式与 3D 推理的错配

当前 VLM 在多视图场景下的核心瓶颈在于：模型倾向于使用 2D 启发式而非构建统一的 3D 表示。这导致在以下任务上表现接近随机猜测：

- **深度模糊任务**：当物体在 2D 投影中位置相近但深度差异显著时，模型无法利用多视图视差信息进行正确判断。
- **遮挡场景**：当关键物体在某一视图中被遮挡时，模型缺乏跨视图补全的能力。
- **跨视角一致性**：当需要判断两个视图中是否包含同一物体或同一空间配置时，模型缺乏显式的几何对齐机制。

最先进的 GPT-5 在 MV-RoboBench 上的平均准确率仅为 56.41%，而人类可达 91.04%（Table 2）。非推理模型在 3D 空间一致性等任务中准确率低至 19.07%，与随机猜测（19.71%）几乎无异。

### 本文动机与贡献定位

针对上述缺口，本文提出 **MV-RoboBench**——首个面向机器人操作场景的多视图空间推理基准测试。MV-RoboBench 的设计遵循三个原则：

1. **完全同步的多视图输入**：所有样本均来自真实机器人操作场景的多个同步摄像头（AgiWorld 和 BridgeV2 数据集），强制模型进行跨视角融合。
2. **空间理解与机器人执行的统一**：基准测试包含 8 个子任务，分为空间理解（跨视图匹配、距离判断、视角识别、3D 空间一致性）和机器人执行（动作规划、步骤执行、轨迹选择、可供性识别）两个领域，共 1.7K 人工标注的 QA 对。
3. **严格的标注质量控制**：采用多阶段人工标注与交叉验证流程，确保答案的准确性和选项的均衡性，避免模型利用位置或颜色偏见。

MV-RoboBench 不仅是评测工具，更是诊断平台：通过系统性的消融实验（CoT 增强、单/多视图对比、图像方向鲁棒性测试），揭示 VLM 在多视图空间推理中的能力边界与失败模式，为未来架构设计提供实证依据。



## 核心方法与创新机理

MV-RoboBench 的核心创新在于系统性地填补了现有空间推理基准的两个关键空白：**多视图输入支持**与**机器人执行场景覆盖**。此前的主流基准（如 EmbSpatial-Bench、Visual Spatial、RoboSpatial、ShareRobot）均局限于单视图空间理解或非具身的多视图感知，无法评估 VLMs 在真实机器人操作场景中融合多摄像头视角进行三维推理的能力（表 1）。MV-RoboBench 通过以下 changed slots 实现了范式转变：

**多视图同步输入。** 基准中的每个问题均提供完全同步的多摄像头视图，而非部分混合单视图样本（表 1）。这迫使模型必须进行跨视图信息融合，而非依赖单视图启发式（如屏幕位置、表观尺寸）。实验表明，这一设计至关重要：强模型（GPT-5）在多视图条件下于 Distance Judgement 任务上获得 +18.90% 的显著增益，而小模型（Qwen2.5-vl-32b）几乎无正面影响，揭示了多视图融合能力存在明确的容量门槛（表 7）。

**空间理解与机器人执行的双域覆盖。** 不同于仅关注空间感知的 All-Angles Bench，MV-RoboBench 将评测维度扩展至机器人操作执行，涵盖 Action Planning、Step Execution、Trajectory Selection 和 Affordance Recognition 四类具身任务（表 6）。这一设计揭示了一个关键发现：单视图空间推理能力无法可靠迁移至多视图机器人场景——在 OmniSpatial 单视图基准上表现良好的模型，在 MV-RoboBench 上仍接近随机水平（图 6）。

**真实机器人场景与严格人工标注。** 基准构建于 AgiWorld 和 BridgeV2 真实机器人操作数据集之上，采用全人工专家标注配合多轮交叉验证，并对答案正确性与颜色索引进行显式均衡（表 1，Section F.9）。这与依赖模板或半自动标注的先前工作形成对比，确保了评测的公平性与难度真实性。



![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_jXDZJAfRZB/figures/012_Figure_2.jpg]]
*Figure 2: Construction pipeline of MV-RoboBench, consisting of three stages: data collection, QA generation, and human-in-the-loop quality review*

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_jXDZJAfRZB/figures/001_Table_1.jpg]]
*Table 1: Comparison of spatial reasoning benchmarks. Prior datasets emphasize single-view relations, abstract reasoning, or non-embodied multi-view perception. The “Partial” in “Multi-View” indicates that these datasets contain only a subset of multi-view samples, mixed with single-view inputs. MV-RoboBench uniquely targets multi-view spatial reasoning within robotic manipulation scenarios, combining embodiment with multi-view perception*

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_jXDZJAfRZB/figures/042_Table_6.jpg]]
*Table 6: Overview of the eight subtasks in our benchmark. Spatial tasks focus on multi-view scene understanding, while robotic tasks extend this foundation to manipulation planning and execution*

MV‑RoboBench 的构建遵循一条严格的多阶段流水线，旨在从真实机器人操作数据中生成高质量、多视角、无偏的问答对。该流水线由三个核心模块串联而成：**数据采集**、**问答生成**与**人工闭环质量审核**（Figure 2）。

### 数据采集

原始数据来源于两个真实机器人操作数据集——**AgiWorld** (Bu et al., 2025) 与 **BridgeV2** (Walke et al., 2023)，二者均提供同步的多摄像头视角。采集阶段首先通过规则过滤筛选出满足基本多视角同步条件的图像对，随后利用 **GPT‑4.1** 作为辅助过滤器，判断候选对是否至少符合八项子任务定义中的一项。需注意，GPT‑4.1 仅用于候选分流，不参与任何问答内容的生成。

### 问答生成

针对每一项子任务，研究者设计了任务专属模板。经培训的标注人员依据模板，从已筛选的图像对中构建五选一的多项选择题，并手工撰写干扰项。所有任务均统一为多项选择格式，以答案准确率作为评测指标。基准共包含约 **1.7K** 个经人工精标的问答样本，覆盖 **8 项子任务**，分为空间理解与机器人执行两大领域（Table 6）。

### 人工闭环质量审核

为确保标注质量与公平性，MV‑RoboBench 实施了多轮迭代的人工审核。多名标注者交叉验证每个问答对的对齐性与合理性，歧义项被剔除或修正。答案分布经过显式均衡处理，兼顾正确选项与颜色索引的平衡，防止模型利用位置或颜色偏见进行投机。

### 探索性增强模块（CoT 启发）

在基准评测之外，研究者还探索了三类 Chain‑of‑Thought 风格的输入增强，用于测试模型能否借助额外信息提升多视角推理能力：

1. **文本描述增强**：由 GPT‑4.1 生成场景文字描述，作为显式的文本化空间上下文。
2. **新视角合成**：通过 **VGGT** (Wang et al., 2025a) 生成额外的合成视点，提供视觉层面的跨视角对齐证据。
3. **深度先验注入**：使用 **MoGe‑2** (Wang et al., 2025b) 估计深度图，引入几何约束以降低 3D 推理的歧义性。

这三类增强分别对应文本、视觉与结构化的 CoT 范式，但其效果高度依赖模型容量（详见实验分析部分）。

### 输入输出流

- **输入**：同步多摄像头图像对（来自真实机器人操作场景），可选附加文本描述、合成视点或深度图。
- **输出**：模型需从五个候选项中选出唯一正确答案；评测指标为准确率。基准同时提供随机猜测基线（约 19.7%）与人类上限（91.0%）作为参照。

### 与现有基准的关键差异

Table 1 系统对比了 MV‑RoboBench 与 12 个现有空间推理基准。其独特性体现在三个维度：

| 维度 | 现有基准 | MV‑RoboBench |
|------|----------|--------------|
| 多视角支持 | 多数仅单视角；少数含部分多视角样本 | **全同步多视角** |
| 任务领域 | 仅空间理解 | **空间理解 + 机器人执行** |
| 场景来源 | 通用室内、互联网图片、自我中心视频 | **真实机器人操作场景** |

这一设计使得 MV‑RoboBench 成为首个同时覆盖多视角感知与 embodied 操作的基准，直接暴露了当前 VLM 在跨视角融合与 3D 推理上的结构性短板。



MV-RoboBench 本身是一个基准测试而非算法模型，其核心模块体现在**数据构建流水线**与**探索性思维链增强**两个层面，而非传统的公式推导环节。以下分别阐述。

---

### 数据构建流水线

基准测试的构建遵循三阶段人工闭环流程（Figure 2）：

**阶段一：数据采集。** 从真实机器人操作数据集 **AgiWorld**（Bu et al., 2025）和 **BridgeV2**（Walke et al., 2023）中提取同步多摄像头图像对。首先通过规则过滤剔除质量不足的帧对，再使用 GPT-4.1 作为辅助筛选器，检查图像对是否满足至少一个预定义子任务的定义。需注意，GPT-4.1 仅用于候选分流，不参与任何 QA 内容的生成。

**阶段二：QA 生成。** 针对每个子任务设计专用模板，由经过培训的标注人员从筛选后的图像对中构建五选一的多项选择题，并生成四个干扰项。

**阶段三：人工质量审查。** 采用多标注者交叉验证与迭代修正机制，确保问题对齐准确、答案分布均衡、歧义项被剔除或修正。最终产出约 1.7K 条高质量 QA 样本。

---

### 探索性思维链增强

为探究显式几何先验对多视图推理的影响，研究设计了三类 CoT 风格的输入增强（Section 2.3）：

1. **文本化场景描述（Textual CoT）：** 使用 GPT-4.1 生成场景的文本描述，将隐式的空间上下文显式化。
2. **新视角合成（Visual CoT）：** 采用 **VGGT**（Wang et al., 2025a）进行新视角合成，为跨视图对齐提供额外的视觉证据。
3. **深度先验（Structural CoT）：** 采用 **MoGe-2**（Wang et al., 2025b）进行深度估计，引入几何约束以减少 3D 推理中的歧义。

这些增强的效果因模型容量而异——深度先验对 GPT-4.1 带来 +3.25% 的平均提升，但对小模型几乎无效；新视角合成在多数模型上反而导致性能下降（Table 3）。

---

### 坐标系定义

为统一多视图空间推理的参照系，基准测试明确定义了以重力方向为基准的相机坐标系（Section E.3）：

**z 轴（垂直方向）：**

$$\hat{\mathbf{z}} = -\frac{\mathbf{g}}{\|\mathbf{g}\|}$$

其中 $\mathbf{g}$ 为重力加速度向量，$+\hat{\mathbf{z}}$ 指向重力反方向（即上方）。

**y 轴（相机前方投影）：**

$$\hat{\mathbf{y}} = \frac{\mathbf{c}_{\perp}}{\|\mathbf{c}_{\perp}\|}$$

其中 $\mathbf{c}_{\perp}$ 为相机前方方向在水平面上的投影分量，$+\hat{\mathbf{y}}$ 指向相机前方。

**x 轴（相机右侧）：**

$$\hat{\mathbf{x}} = \hat{\mathbf{y}} \times \hat{\mathbf{z}}$$

由右手定则确定，$+\hat{\mathbf{x}}$ 指向相机右侧。

这一显式坐标系定义为跨视图的空间一致性判断（如 3D Spatial Consistency 子任务）提供了统一的几何参照基础。

---

### 关键设计要点

- **答案均衡：** 所有子任务的正确答案选项和颜色索引均经过显式均衡处理，防止模型利用位置或颜色偏见进行捷径猜测（Section F.9）。
- **零-shot 统一提示：** 所有模型评估采用统一的多项选择提示格式，避免模型特异性的提示工程带来的不公平比较（Section 3.1）。
- **“以上均非”拒绝机制：** 通过修改数据集使正确答案变为“以上均非”，测试模型识别无效选项的能力，揭示出 GPT-5 等强模型存在严重的过度服从问题——准确率从 56% 骤降至 13%（Table 9）。



## 实验与关键发现

### 主结果：模型表现与人类基准的巨大鸿沟

MV‑RoboBench 采用统一的零‑shot 多项选择评测协议，以准确率作为核心指标。Table 2 汇总了 26 个以上视觉–语言模型在全部八个子任务上的表现，揭示出从感知型系统到显式推理架构的递进趋势，但整体结果与人类水平之间仍存在显著差距。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_jXDZJAfRZB/figures/015_Table_2.jpg]]
*Table 2: Evaluation on MV-RoboBench under a unified zero-shot prompt. denotes the best score and the second-best within each column. Qwen2.5-vl-72B leads among open-source models, while GPT-5 ranks highest overall but still remains far below human accuracy*

- **总体表现**：最先进模型 **GPT‑5** 仅取得 **56.41%** 的平均准确率，远低于人类参与者的 **91.04%**，而随机选择基线仅为 19.71%。这一 34.63 pp 的差距表明，当前 VLM 在多视图机器人空间推理上仍处于初级阶段。
- **任务维度的分化**：在 **3D 空间一致性**（3D Spatial Consistency）和 **动作规划**（Action Planning）任务上，GPT‑5 分别达到 82.35% 和 79.41%，显著高于随机水平（19.07% 和 19.41%），说明推理型模型在需要显式几何约束的任务中具备一定能力。然而，在 **跨视图匹配**（Cross‑View Match）、**距离判断**（Distance Judgement）等更依赖细粒度多视图对齐的子任务上，多数非推理模型表现接近甚至低于随机猜测。
- **开源模型的上限**：开源模型中 **Qwen2.5‑vl‑72B** 以 24.29% 的平均准确率领先，但与闭源推理模型相比差距悬殊，进一步凸显模型容量与推理能力在多视图场景中的关键作用。

Figure 4 以雷达图形式对比了各模型家族最佳代表与人类在八项子任务上的表现：人类在所有维度上均接近满分，而模型在“跨视图匹配”和“距离判断”两个子任务上尤为薄弱，形成明显的性能塌陷区域。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_jXDZJAfRZB/figures/016_Figure_4.jpg]]
*Figure 4: Best-per-group model performance across MV-RoboBench subtasks*

### 消融实验：多视图增益的容量门槛

为验证多视图输入的实际贡献，Table 7 对比了单视图与多视图设置在五个代表性子任务上的表现差异。核心发现是**多视图增益高度依赖模型容量**：

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_jXDZJAfRZB/figures/043_Table_7.jpg]]
*Table 7: Comparison of Single-View vs. Multi-View performance on selected subtasks. The values represent Multi-View accuracy, and values in parentheses indicate the change (∆) compared to the Single-View baseline. Positive ∆ indicates that multi-view inputs improve performance. Bold indicates the best performance in each category*

- **强模型显著受益**：GPT‑5 在距离判断任务上多视图相对单视图提升 **+18.90%**，在动作规划上提升 **+8.82%**，证明其具备有效的跨视图信息融合能力。
- **小模型几乎无增益甚至退化**：Qwen2.5‑vl‑32B 在相同任务上多视图带来的变化微乎其微或为负值，表明容量不足的模型无法利用多视图提供的额外几何线索，甚至可能因信息冗余而受到干扰。

这一发现直接支撑了核心瓶颈判断：**多视图融合存在明确的容量门槛**，简单的输入拼接不能替代显式的几何推理架构。

### CoT 增强的异质性效果

Table 3 系统评估了三种 CoT 风格增强策略的效果：文本描述增强（w text）、新视角合成（w vggt）和深度先验（w depth）。结果表明，增强效果因模型而异，且呈现非单调特征：

- **深度先验的正面效应**：GPT‑4.1 在引入深度先验后平均准确率提升 **+3.25%**（从 29.87% 升至 33.12%），表明几何约束对具备足够容量的模型具有辅助作用。
- **新视角合成的普遍损害**：VGGT 合成的新视角在多数模型上导致性能下降，说明当前新视角合成技术产生的伪影或不一致性可能引入额外噪声，反而干扰跨视图对齐。
- **小模型的负面响应**：Qwen2.5‑vl‑7B 在所有增强条件下均出现退化，深度先验使其从 20.84% 降至更低水平，验证了“浅层提示增强不能替代显式几何推理”的论断。

### 失败模式分析：方向敏感性与过度服从

两项诊断性实验揭示了当前 VLM 在鲁棒性方面的系统性缺陷：

**图像倒置的脆弱性**（Table 8）：将输入图像翻转 180° 后，GPT‑5 的平均准确率骤降 **−18.73 pp**，而 GPT‑4.1‑mini 几乎不受影响（−0.04 pp）。这一反差表明，高性能推理模型可能过度依赖训练数据中的规范视觉方向，缺乏真正的视角不变 3D 理解能力。

**“以上均非”拒绝能力**（Table 9）：当正确答案被强制设为“以上均非”时，GPT‑5 的准确率从 56% 暴跌至 **13%**，暴露出严重的过度服从（over‑compliance）问题——模型倾向于在给定选项中强行选择，而非识别无效候选项。

### 单视图能力的迁移失效

Figure 6 将模型在单视图空间推理基准 **OmniSpatial** 上的表现与 MV‑RoboBench 进行对比。散点图显示，在 OmniSpatial 上取得较高准确率的模型，在 MV‑RoboBench 的空间和机器人子任务上仍可接近随机水平。这一发现直接否定了“通用单视图空间推理能力可自然迁移至多视图 embodied 场景”的假设，证明**多视图机器人空间推理需要专门的评测与训练范式**。

### 空间推理与机器人执行的正相关

Figure 5 展示了各模型在空间任务与机器人任务上的准确率分布。开源 VLM 普遍聚集在左下角随机猜测区域，而闭源推理模型沿对角线呈单调上升趋势。这一正相关关系表明，**在多视图条件下，空间感知能力是机器人执行能力的前提**，但仅当模型具备足够的跨视图融合能力时，这种耦合才会显现。



## 定位与知识库关联

### 与现有基准的关系

MV‑RoboBench 的定位可从 Table 1 的六维对比中清晰识别。现有空间推理基准主要分为三类：

**单视图空间推理基准**。**EmbSpatial‑Bench**（Du et al., 2024）、**Visual Spatial**（Liu et al., 2023a）和 **RoboSpatial**（Song et al., 2025a）均以单张图像或视频帧为输入，考察模型对物体相对位置、朝向、距离等空间关系的理解。这些基准的共性局限在于：它们不要求模型跨视角整合信息以形成一致的 3D 表征。实验证据表明，在 OmniSpatial 等单视图基准上表现优异的模型，在 MV‑RoboBench 上仍接近随机猜测水平（Figure 6），说明单视图空间推理能力无法直接迁移至多视图 embodied 场景。

**非 embodied 多视图基准**。**All‑Angles Bench**（Yeh et al., 2025）引入了多视角输入，但缺乏机器人操作语境，其任务聚焦于通用场景理解而非操控规划与执行。**ShareRobot**（Ji et al., 2025）虽覆盖机器人推理，但不支持多视图。

**MV‑RoboBench 的独特增量**体现在三个维度：（1）**完全同步的多视图支持**——所有样本均包含来自多个标定摄像头的同步图像，而非“部分多视图”（Table 1 中其他基准标注为 Partial）；（2）**领域覆盖**——同时包含空间理解与机器人执行两大任务类别，使感知与动作落地的联合评估成为可能；（3）**场景真实性**——数据源自 AgiWorld 和 BridgeV2 的真实机器人操作场景，而非通用室内图像或互联网图片。

### 核心瓶颈与因果机制

当前 VLMs 在多视图空间推理上的根本瓶颈并非单一能力的缺失，而是 **2D 启发式与真正 3D 推理之间的系统性错配**。决定性证据来自 Table 2：非推理模型在 3D 空间一致性任务上接近随机猜测（19.07%），而 GPT‑5 可达 82.35%，差距高达 63.28 个百分点。这表明弱模型倾向于依赖屏幕位置、表观尺寸等 2D 线索，而非构建跨视角一致的 3D 表示。

多视图融合存在明确的**容量门槛**。Table 7 的单/多视图消融实验揭示了这一非线性效应：GPT‑5 在多视图条件下 Distance Judgement 提升 +18.90%，Action Planning 提升 +8.82%；而 Qwen2.5‑vl‑32b 等多视图增益几乎为零甚至为负。这意味着多视图信息本身不是“免费午餐”——只有当模型具备足够的表示容量时，额外的视角才能被有效整合为 3D 几何约束，否则只会增加噪声。

CoT 风格增强（Table 3）进一步验证了这一机制。深度先验（通过 MoGe‑2 估计）对 GPT‑4.1 带来 +3.25% 的增益，但对 Qwen2.5‑vl‑7B 等小模型无效甚至有害；新视角合成（通过 VGGT 生成）在所有模型上普遍降低性能。这表明**浅层提示增强不能替代显式的几何推理架构**——合成视角可能引入伪影，而小模型缺乏利用深度线索的表示能力。

### 适用边界与局限

MV‑RoboBench 的评估范式存在以下边界条件：

1. **零‑shot 多项选择格式**：所有评估采用统一零‑shot 提示，避免模型特异性提示工程，但这也意味着结果反映的是模型的“开箱即用”能力，而非经过领域微调后的潜力。

2. **规模与覆盖**：基准包含约 1.7K 人工标注 QA 样本，覆盖八个子任务，但可能无法穷尽真实操作场景的复杂性。更大规模、更多样化的多摄像头数据集仍是开放需求。

3. **非规范视角鲁棒性**：Table 8 显示，图像倒置使 GPT‑5 平均准确率下降 18.73 个百分点，而 GPT‑4.1‑mini 几乎不受影响（‑0.04）。这表明高性能推理模型反而更依赖规范的视觉方向假设，在非规范条件下脆弱。

4. **“以上均非”拒绝能力**：Table 9 显示，当正确答案为“以上均非”时，GPT‑5 的准确率从 56% 骤降至 13%，暴露了模型过度服从选项框架、无法识别无效答案的深层问题。

### 开放问题

从上述瓶颈和局限出发，以下方向值得后续工作关注：

- **架构层面**：如何设计能显式编码几何先验（如多视图几何约束、深度一致性）并强制跨视角一致性的 VLM 架构，而非依赖浅层提示增强？
- **训练层面**：如何在训练流程中实现感知与动作落地的高效对齐，使多视图空间推理能力能可靠地迁移至机器人执行？
- **数据层面**：如何构建更大规模、能反映真实操作复杂度的多摄像头数据集，以覆盖更丰富的视角配置和操作场景？
- **效率层面**：小型模型如何在资源受限下有效融合多视图信息，避免退化为单视图偏见？当前 CoT 增强对小模型无效的事实表明，需要更根本的架构创新而非简单的信息注入。
- **鲁棒性层面**：如何使模型在非规范视觉方向（倒置、倾斜）下仍保持稳健的 3D 空间推理能力？GPT‑5 在倒置条件下的显著退化暗示，当前模型的 3D 理解可能部分依赖于与训练分布一致的视觉统计，而非真正的几何推理。



## 原文 PDF

![[paperPDFs/ICLR_2026/Seeing_Across_Views_Benchmarking_Spatial_Reasoning_of_Vision_Language_Models_in_Robotic_Scenes.pdf]]
