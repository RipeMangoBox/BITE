---
title: "HIS-GPT: Towards 3D Human-In-Scene Multimodal Understanding"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/HIS_GPT_Towards_3D_Human_In_Scene_Multimodal_Understanding.pdf
project_link: null
code_link: https://github.com/ZJHTerry18/HumanInScene
aliases:
- HG
- HIS-GPT
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 联合编码3D场景和人体运动，并显式注入人-场景交互信息和时空位置编码。
primary_logic: 通过辅助交互任务（活动分类、空间关系检测、接触检测）和基于傅里叶变换的布局-轨迹位置编码，模型能够学习丰富的上下文表征，从而在多种人-场景理解任务上取得显著提升。
claims:
- Existing models fall short in HIS understanding, largely due to their insufficient capacity for jointly modeling human-scene characteristics.
- HIS-GPT achieves average 48.7 on HIS-Bench, outperforming GPT-4o (31.3) by 17.4 points.
- AInt and LTP modules jointly contribute a 5.7 point gain over the baseline.
- HIS-Bench 上 Average score (across 16 sub-tasks) = 48.7
---

# HIS-GPT: Towards 3D Human-In-Scene Multimodal Understanding

> [!tip] 核心洞察
> 通过辅助交互任务（活动分类、空间关系检测、接触检测）和基于傅里叶变换的布局-轨迹位置编码，模型能够学习丰富的上下文表征，从而在多种人-场景理解任务上取得显著提升。

| 字段 | 内容 |
|------|------|
| 中文题名 | HIS-GPT：面向三维场景中人体多模态理解 |
| 英文题名 | HIS-GPT: Towards 3D Human-In-Scene Multimodal Understanding |
| 会议/期刊 | arXiv 2025 |
| Links | [Code](https://github.com/ZJHTerry18/HumanInScene) · [paper](https://arxiv.org/abs/2503.12955) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | HIS-GPT |
| Dataset | HIS-Bench |

> [!tip] 效果简介
> - HIS-Bench 上，Average score (across 16 sub-tasks) 48.7 vs GPT-4o: 31.3 (+17.4)；Average score 48.7 vs Chat-Scene: 8.2 (+40.5)。

## 概要

### 问题定义

理解三维场景中的人类行为是构建具身智能体的关键能力。然而，现有模型普遍缺乏对3D场景几何与人体运动动态的**联合建模**能力，无法有效捕捉人-场景交互的丰富语义。具体而言，传统方法要么仅关注场景理解，要么仅处理孤立的人体运动，导致在需要复杂推理和上下文感知的任务——例如预测人与物体的空间关系、推断行为意图、评估动作安全性——上性能严重不足。

为系统评估这一能力缺口，本文定义了**HIS-QA（Human-In-Scene Question Answering）**任务：给定一个3D场景点云 $S$、一段人体运动序列 $M$ 以及自然语言问题 $Q$，模型需生成与真实答案 $A$ 一致的回复 $\hat{A}$。该问题可形式化为四元组 $\langle S, M, Q, A \rangle$。

### 核心结论

**HIS-GPT** 在涵盖16个子任务的 HIS-Bench 基准上取得平均分 **48.7**，相较通用视觉大模型 GPT-4o（31.3）提升 **17.4** 分，相较适配后的3D场景大模型 Chat-Scene（8.2）提升 **40.5** 分（Table 2）。这一显著差距印证了本文的核心论断：**联合编码场景与运动，并显式注入人-场景交互信息，是突破当前瓶颈的关键路径。**

### 方法定位

HIS-GPT 并非从头训练一个大模型，而是在预训练大语言模型（Vicuna-1.5）的基础上，通过两条核心设计实现人-场景的联合理解：

1.  **辅助交互模块（AInt）**：在编码阶段引入三个辅助任务——**活动分类**、**空间关系检测**和**接触检测**——迫使模型学习人与场景之间的细粒度交互线索。这些任务的监督信号来自自动标注，无需额外人工成本。

2.  **布局-轨迹位置编码（LTP）**：针对3D场景中物体的空间分布和人体运动的时间轨迹，分别设计**空间傅里叶变换**和**时间傅里叶变换**位置编码，替代传统的正弦位置编码，使模型感知“物体在哪里”和“人在何时移动到哪里”。

消融实验表明，AInt 和 LTP 模块联合贡献 **5.7** 分的增益（Table 3），验证了交互感知与时空位置信息对下游推理的因果性作用。

### 方法谱系与知识库定位

在方法谱系上，HIS-GPT 属于**多模态大语言模型（MLLM）在3D场景理解方向的延伸**。与以下工作形成直接对比：

-   **LL3DA**（Chen et al., CVPR 2024）和 **Chat-Scene**（Huang et al., NeurIPS 2023）：同为3D场景大模型，但仅处理静态场景，缺乏对人体运动的编码能力。在 HIS-Bench 上，Chat-Scene 仅获 8.2 分，暴露了单一模态理解的局限性。
-   **GPT-4o**（Hurst et al., 2024）、**Qwen-VL-max**（Bai et al., 2023）、**LLaVA-OV**（Li et al., TMLR 2024）：通用视觉大模型，虽具备广泛的视觉理解能力，但未针对3D空间结构和人-物交互进行专门设计，在需要精确空间推理的子任务上表现不佳。

HIS-GPT 的独特定位在于：**首次将3D场景编码器（Uni3D）、人体运动编码器（VQ-VAE）与大语言模型通过交互感知模块和时空位置编码进行深度融合**，构建了一个面向人-场景联合理解的基准模型。

### 主要结果概览

| 基准 | 指标 | HIS-GPT | 最强基线 | 提升 |
|:---|:---|:---:|:---:|:---:|
| HIS-Bench | 16子任务平均分 | **48.7** | GPT-4o: 31.3 | +17.4 |
| HIS-Bench | 16子任务平均分 | **48.7** | Chat-Scene: 8.2 | +40.5 |

即使在将基线模型在相同训练数据上进行微调后，HIS-GPT 仍保持显著领先（Table 8），表明其架构设计而非数据规模是性能差异的主因。此外，GPT-4 自动评估的可靠性经人工研究验证（Pearson 相关系数 0.54），并与 Qwen2.5-7B 评估器高度一致（相关系数 0.75），支撑了定量结论的可信度。



三维场景理解近年来取得了显著进展，大量工作聚焦于从点云数据中提取物体级特征并支持语言引导的问答与对话。然而，这些努力几乎完全忽略了场景中另一个关键要素——**人类**。现实世界中的三维空间往往与人类活动密不可分：人在沙发上坐下、在厨房操作台前准备食物、在办公室内穿行。理解这些“人-场景交互”（Human-Scene Interaction, HIS）对于具身智能、AR/VR、人机协作等应用至关重要。

当前领域存在一个核心瓶颈：**现有模型缺乏对三维场景和人体动作的联合理解能力**。具体而言，三维场景大语言模型（如 **LL3DA** (Chen et al., CVPR 2024)、**Chat-Scene** (Huang et al., NeurIPS 2023)）仅编码静态场景几何与语义，无法感知人体运动；而通用视觉大语言模型（如 **GPT-4o**、**Qwen-VL-max**、**LLaVA-OV**）虽能处理视频输入，但缺乏对三维空间结构和人-物交互关系的显式建模。这种割裂导致模型在需要复杂推理和上下文感知的任务上表现严重不足——例如，判断一个人是否“面向桌子”并“即将坐下”，需要同时理解场景布局、人体姿态序列以及二者之间的时空约束。

为填补这一空白，本文提出了 **HIS-QA** 任务——要求模型基于三维场景点云 $S$ 和人体运动序列 $M$，回答自然语言问题 $Q$ 并生成答案 $\hat{A}$。围绕该任务构建的 **HIS-Bench** 基准覆盖了从基础感知（活动识别、空间关系检测、接触检测）到高阶推理（意图预测、情境分析、导航规划）的多层次能力评估。这一设定直接暴露了现有方法的系统性缺陷：GPT-4o 在 HIS-Bench 上的平均得分仅为 31.3（满分 100），而专用三维场景 LLM 如 Chat-Scene 更是低至 8.2，表明**单纯依靠通用视觉-语言能力或静态场景编码远不足以实现可靠的人-场景联合理解**。

本文的动机由此明确：设计一个能够**联合编码三维场景与人体运动，并显式注入人-场景交互信息与时空位置编码**的模型，从而在 HIS-QA 任务上实现质的突破。这一思路直接催生了 **HIS-GPT**——一个集成场景编码器、运动编码器、辅助交互模块（AInt）和布局-轨迹位置编码（LTP）的多模态大语言模型。其核心洞察在于：通过辅助交互任务（活动分类、空间关系检测、接触检测）和基于傅里叶变换的时空位置编码，模型能够学习到丰富的上下文表征，从而在多种人-场景理解子任务上取得显著提升。



## 核心方法与创新机理

HIS-GPT 的核心创新在于将**人-场景交互的显式建模**与**时空结构位置编码**引入多模态大语言模型，从而突破现有方法在 3D 人-场景联合理解上的瓶颈。相比独立编码场景和人体运动、缺乏交互感知的 baseline，HIS-GPT 通过两个关键模块（AInt 和 LTP）实现了因果性的性能提升：消融实验表明，二者联合贡献了 **5.7 分**的 HIS-Bench 平均得分增益（Table 3）。

### 创新一：辅助交互模块（AInt）—— 显式建模人-场景交互

现有 3D 场景 LLM（如 **LL3DA**，Chen et al., CVPR 2024；**Chat-Scene**，Huang et al., NeurIPS 2023）仅对场景进行编码，缺乏对人-场景交互的感知能力。HIS-GPT 提出 **Auxiliary Interaction (AInt) 模块**，通过三个辅助任务强制模型学习人与环境的联合表征：

1. **活动分类（Activity Classification）**：对融合后的运动嵌入进行全局池化，经 MLP 预测整体人体活动类别，损失函数为交叉熵 $\mathcal{L}_{act}$（Eq. 2）。
2. **空间关系检测（Spatial Relation Detection）**：在每一帧预测人体与场景物体的空间关系（如“面向”、“左侧”等六类朝向），损失函数为 $\mathcal{L}_{spa}$（Eq. 3）。
3. **接触检测（Contact Detection）**：逐关节预测人体是否与物体接触，损失函数为二值交叉熵 $\mathcal{L}_{cont}$（Eq. 4）。

这三个任务共享一个核心操作：将每帧运动嵌入 $m_t$ 与其 $k$ 个最近邻物体嵌入进行平均融合，得到交互增强的运动表征 $\tilde{m}_t$（Eq. 1）。消融实验证实，仅 AInt 模块即可带来 **1.1 分**的提升（Table 3）。

### 创新二：布局-轨迹位置编码（LTP）—— 注入时空结构信息

传统位置编码（如标准正弦编码）无法区分场景物体的空间布局和人体运动的时序轨迹。HIS-GPT 提出 **Layout-Trajectory Position Encoding (LTP) 模块**，分别对场景和运动进行结构化编码：

- **空间傅里叶变换（Spatial Fourier-transform, SF）**：对场景物体的 3D 坐标 $\mu$ 进行傅里叶特征映射 $\mathrm{SF}(\mu) = \mathrm{sincos}(\phi_{SF} \cdot 2\pi\mu)$，编码空间布局信息（Eq. 5）。
- **时间傅里叶变换（Temporal Fourier-transform, TF）**：对运动序列的时间戳 $t$ 进行傅里叶特征映射 $\mathrm{TF}(t) = \mathrm{sincos}(\phi_{TF} \cdot 2\pi t)$，编码时序轨迹信息（Eq. 5）。

LTP 模块独立贡献 **3.0 分**的提升（Table 3），表明时空结构信息的注入对模型理解人-场景时空关系至关重要。

### 创新三：两阶段训练策略与数据构建

HIS-GPT 采用两阶段训练策略，并在第一阶段引入多模态对齐数据：

- **Stage 1（多模态对齐）**：使用 60k 视觉描述（含 HIS、场景、运动三类描述）训练投影层，使场景和运动嵌入与 LLM 的文本空间对齐。消融表明，同时使用三类描述比仅使用 HIS 描述提升 **2.9 分**（Table 4）。
- **Stage 2（指令微调）**：使用 700k 指令样本进行微调，仅优化 $\mathcal{L}_{llm}$，同时冻结 LLM 参数。冻结 LLM 的策略（48.7 分）显著优于 LoRA 微调（38.1 分），避免了灾难性遗忘（Table 9）。

### 与 Baseline 的本质差异

| 维度 | Baseline（LL3DA / Chat-Scene / GPT-4o） | HIS-GPT |
|------|------|------|
| **位置编码** | 标准正弦编码 | LTP：空间+时间傅里叶编码 |
| **交互建模** | 无（独立编码场景与运动） | AInt：活动分类、空间关系、接触检测 |
| **训练数据** | 场景或运动单一描述 | 联合 HIS 描述 + 场景/运动描述 |
| **推理能力** | 缺乏上下文感知，平均 8.2-31.3 分 | 显式交互推理，平均 48.7 分 |

综上，HIS-GPT 通过 **AInt 的显式交互建模**和 **LTP 的结构化时空编码**，首次实现了对 3D 场景和人体运动的联合深度理解，在 HIS-Bench 上以 48.7 分大幅超越最强通用 VLM **GPT-4o**（31.3 分）达 17.4 分，验证了专用人-场景交互架构的必要性。



HIS-GPT 的整体设计围绕一个核心命题展开：**联合理解 3D 场景与人体运动**，以支持开放式的、上下文感知的人-场景交互问答（HIS-QA）。其 pipeline 遵循“双编码器提取 → 交互增强 → 时空位置注入 → 大语言模型解码”的范式，将异构的视觉-运动信号转化为自然语言回答。

### 输入定义

模型接收一个 HIS-QA 实例，形式化为四元组 $\langle S, M, Q, A \rangle$：
- **$S$**：3D 场景点云，提供静态环境的结构化信息；
- **$M$**：3D 人体运动序列，描述随时间变化的姿态与位移；
- **$Q$**：自然语言问题，涵盖从基础感知（活动识别、空间关系）到高阶推理的 16 个子任务；
- **$A$**：真实答案，用于监督训练。

### 模块架构与数据流

整体架构如 **Figure 4(a)** 所示，包含以下核心模块：

![[assets/figures/papers/paper_list_l1683_HIS_GPT_Towards_3D_Human_In_Scene_Multimodal_Understanding/figures/005_Figure_4.jpg]]
*Figure 4: (a) HIS-GPT overall architecture. HIS-GPT uses separate pretrained encoders for scene and motion to extract embeddings, which are then combined with instructions and processed by the LLM. (b) Auxiliary Interaction (AInt) module: Enhance human-scene interactions through three auxillary sub-tasks. (c) Layout-Trajectory Position Encoding (LTP) module: Encode spatial and temporal relationships into position embeddings, injecting contextual knowledge to enhance HIS understanding*

1.  **3D 场景编码器**
    采用预训练的 **Uni3D**（Chen et al., CVPR 2024 引用）从点云 $S$ 中提取物体级别的特征 $\{s_i\}$。该编码器将场景离散化为可区分的物体实例，为后续的交互建模提供结构化的空间锚点。

2.  **运动编码器**
 采用预训练的 **VQ-VAE**（引用自 ）将人体姿态序列 $M$ 编码为离散的运动嵌入 $\{m_t\}$。这一过程将连续的运动流压缩为紧凑的 token 序列，便于与文本 token 统一处理。

3.  **辅助交互模块**
    这是 HIS-GPT 实现人-场景联合理解的关键机制。AInt 模块首先通过 **k-近邻融合** 将运动嵌入与场景物体特征在每一帧进行绑定：
    $$\tilde{m}_t = m_t + \mathrm{Avg}(s_{t_1}, ..., s_{t_k})$$
    即对于第 $t$ 帧的人体运动嵌入 $m_t$，在空间中找到与其距离最近的 $k$ 个场景物体，取其特征均值进行残差增强。这一操作使运动表征天然携带了周围环境的上下文信息。

    在此基础上，AInt 引入三个辅助训练目标，从不同粒度强制模型学习交互表征：
    - **活动分类**：对整段融合运动嵌入取平均后，通过 MLP 预测人体活动类别，使用交叉熵损失 $\mathcal{L}_{act}$（Eq. 2）；
    - **空间关系检测**：在每一帧预测人体与各物体的空间关系（如“坐在椅子上”），使用交叉熵损失 $\mathcal{L}_{spa}$（Eq. 3）；
    - **接触检测**：在每一帧预测人体各关节与物体的接触状态，使用二值交叉熵损失 $\mathcal{L}_{cont}$（Eq. 4）。

    如 **Figure 4(b)** 所示，这三个任务并行作用于融合后的表征，为模型注入细粒度的人-物交互线索。

4.  **布局-轨迹位置编码模块**
    为弥补标准正弦位置编码在空间-时间结构上的不足，LTP 模块（**Figure 4(c)**）引入显式的时空傅里叶编码：
    $$\mathrm{SF}(\mu) = \mathrm{sincos}(\phi_{SF} \cdot 2\pi\mu), \quad \mathrm{TF}(t) = \mathrm{sincos}(\phi_{TF} \cdot 2\pi t)$$
    其中 $\mu$ 为物体的 3D 坐标或人体关节位置，$t$ 为时间戳。SF 层编码场景中主要物体的空间布局，TF 层编码人体运动的时间轨迹。这些编码被注入到对应的场景和运动 token 中，使 LLM 能够感知物体的绝对位置与运动的时序变化。

5.  **大语言模型解码器**
    采用冻结的 **Vicuna-1.5** 作为文本生成核心。场景 token、运动 token 与指令 token 拼接后送入 LLM，最终自回归地生成答案 $\hat{A}$。

### 训练策略

HIS-GPT 采用两阶段训练：
- **Stage 1（视觉-语言对齐）**：使用 60k 视觉描述（涵盖场景、运动及联合 HIS 描述）进行预训练，建立视觉 token 与语言空间的初步对齐；
- **Stage 2（指令微调）**：在 700k 指令样本上进行微调，总损失为：
  $$\mathcal{L} = \mathcal{L}_{llm} + \lambda_{act}\mathcal{L}_{act} + \lambda_{spa}\mathcal{L}_{spa} + \lambda_{cont}\mathcal{L}_{cont}$$
  其中 $\mathcal{L}_{llm}$ 为标准的语言建模损失，其余三项为 AInt 模块的辅助损失。LLM 参数在此阶段保持冻结（实验证明冻结优于 LoRA 微调，Table 9），仅训练投影层和辅助任务头。

### 关键设计总结

| 设计选择 | 作用 |
|---------|------|
| 双编码器独立提取 | 保留场景与运动的模态特异性 |
| AInt 的 k-近邻融合 | 在表征层建立人-物空间关联 |
| 三项辅助任务 | 从活动、空间关系、接触三个粒度注入交互先验 |
| LTP 时空傅里叶编码 | 弥补 LLM 对 3D 坐标和时间结构的感知盲区 |
| 冻结 LLM 训练 | 避免灾难性遗忘，保持语言能力 |

消融实验（Table 3）验证了这一设计的有效性：AInt 和 LTP 模块联合贡献了 5.7 分的平均提升，其中 LTP 单独贡献 3.0 分，AInt 贡献 1.1 分，表明时空位置编码与交互建模存在互补效应。

### 补充图表

![[assets/figures/papers/paper_list_l1683_HIS_GPT_Towards_3D_Human_In_Scene_Multimodal_Understanding/figures/001_Figure_1.jpg]]
*Figure 1: (a) Illustration of HIS-QA task, which understands human behaviors in scene context. HIS-QA tasks span from basic perception tasks, such as recognizing human activity, interaction, and position in scene, to higher order functions like prediction, reasoning, planning, and navigation, facilitating embodied intelligence in real world. (b) Illustration of HIS-GPT. Unlike previous models that focus solely on either scene or human understanding, HIS-GPT could jointly perceive scene and human modalities to tackle the challenges of HIS-QA*



### 问题形式化

HIS-GPT 将人-场景理解任务形式化为四元组 $\langle S, M, Q, A \rangle$，其中 $S$ 为三维场景点云，$M$ 为人体运动序列，$Q$ 为自然语言问题，$A$ 为真实答案。模型需生成近似答案 $\hat{A} = \text{Agent}(S, M, Q)$。

### 整体架构

HIS-GPT 采用双编码器加 LLM 的解码架构（Figure 4）。场景编码器 Uni3D 从点云提取物体级特征，运动编码器 VQ-VAE 将人体姿态序列编码为离散嵌入。两类表征经融合后与指令文本拼接，送入大语言模型 Vicuna-1.5 生成回答。核心创新在于两个即插即用的模块：辅助交互模块和布局-轨迹位置编码模块。

### 辅助交互模块

该模块通过显式建模人-场景交互信号增强表征质量，包含三个并行的辅助任务。

**运动嵌入融合**：对时刻 $t$ 的运动嵌入 $m_t$，检索其 $k$ 个最近邻场景物体，以平均池化方式注入场景上下文：

$$\tilde{m}_t = m_t + \mathrm{Avg}(s_{t_1}, ..., s_{t_k})$$

**活动分类损失**：对全序列的融合运动嵌入取平均，经 MLP 和 Softmax 预测整体活动类别 $p^a$，以交叉熵监督：

$$\mathcal{L}_{act} = \mathrm{CE}\left(p^a, \mathrm{SM}\left(\mathrm{MLP}\left(\mathrm{Avg}(\tilde{m}_1, \dots, \tilde{m}_T)\right)\right)\right)$$

**空间关系检测损失**：逐帧计算人体与每个物体 $i$ 的空间关系概率 $p_{it}^s$，通过可学习的线性投影 $W_s^{spa}$ 和 $W_m^{spa}$ 将场景与运动嵌入映射到共享空间后做点积：

$$\mathcal{L}_{spa} = \sum_{i,t} \mathrm{CE}\left(p_{it}^s, \mathrm{SM}\left(W_s^{spa}(s_i) \cdot W_m^{spa}(m_t)\right)\right)$$

**接触检测损失**：以二元交叉熵监督每个关节与物体的接触状态 $p_{it}^c$，同样通过点积计算匹配分数，经 sigmoid 激活：

$$\mathcal{L}_{cont} = \sum_{i,t} \mathrm{BCE}\left(p_{it}^c, \sigma\left(W_s^{cont}(s_i) \cdot W_m^{cont}(m_t)\right)\right)$$

### 布局-轨迹位置编码模块

该模块为场景物体和人体运动注入结构化的时空位置信息。对三维空间坐标 $\mu$ 和时间戳 $t$，分别施加基于傅里叶变换的正余弦编码：

$$\mathrm{SF}(\mu) = \mathrm{sincos}(\phi_{SF} \cdot 2\pi\mu), \quad \mathrm{TF}(t) = \mathrm{sincos}(\phi_{TF} \cdot 2\pi t)$$

其中 $\phi_{SF}$ 和 $\phi_{TF}$ 为可学习频率参数。SF 编码捕获场景中主要物体的空间布局，TF 编码刻画人体运动的时间轨迹，二者共同为 LLM 提供物体位置和动作时序的结构化先验。

### 训练目标

总损失为语言建模损失与三个辅助损失的加权和：

$$\mathcal{L} = \mathcal{L}_{llm} + \lambda_{act}\mathcal{L}_{act} + \lambda_{spa}\mathcal{L}_{spa} + \lambda_{cont}\mathcal{L}_{cont}$$

训练分两阶段：第一阶段使用 60k 视觉描述进行模态对齐，第二阶段使用 700k 指令样本进行指令微调，仅优化 $\mathcal{L}_{llm}$ 以保证指令遵循质量。消融实验表明，冻结 LLM 参数优于 LoRA 微调（48.7 vs 38.1），AInt 与 LTP 模块联合贡献 5.7 分的提升。

### 补充图表

![[assets/figures/papers/paper_list_l1683_HIS_GPT_Towards_3D_Human_In_Scene_Multimodal_Understanding/figures/010_Figure_6.jpg]]
*Figure 6: Illustrations of the definition of human-object orientations. We define six types of orientations: ‘facing towards’, ‘on the left’, ‘on the right’, ‘facing away’, ‘at’, and ‘between’*



## 实验与关键发现

### 主实验结果

HIS-GPT在HIS-Bench上取得了48.7的平均分（满分100），显著优于所有基线方法。具体而言，相比通用视觉大语言模型中表现最好的GPT-4o（31.3分），HIS-GPT提升了17.4分；相对于3D场景专用大语言模型Chat-Scene（8.2分），提升幅度高达40.5分（Table 2）。这一巨大差距揭示了现有模型在3D人-场景联合理解上的根本性缺陷：通用视觉大语言模型虽具备一定的场景感知能力，但缺乏对人体运动时序信息的有效编码；而3D场景专用模型则完全缺失了对人体模态的建模能力。

![[assets/figures/papers/paper_list_l1683_HIS_GPT_Towards_3D_Human_In_Scene_Multimodal_Understanding/figures/006_Table_2.jpg]]
*Table 2: Quantitative evaluation results on HIS-Bench. We run the evaluation for three times and report the average score for each dimension. The full score for each dimension is 100. ‘Avg.’ is the average score across all 16 dimensions. The best and second-best results are boldfaced and underlined, respectively*

值得注意的是，即使将基线模型在相同训练数据上进行微调，HIS-GPT仍保持显著优势（Table 8），说明其性能提升并非单纯来自数据规模，而是源于架构设计中对人-场景交互机制的显式建模。

![[assets/figures/papers/paper_list_l1683_HIS_GPT_Towards_3D_Human_In_Scene_Multimodal_Understanding/figures/016_Table_8.jpg]]
*Table 8: The average scores of zero-shot and fine-tuned baseline methods on HIS-Bench. The fine-tuning data is consistent with HIS-GPT training data, as listed in Tab. 7. HIS-GPT does not have zero-shot version since it is trained with HIS data from scratch*

### 关键组件消融

Table 3系统剖析了AInt模块与LTP模块的贡献。以标准正弦位置编码为基线，单独引入AInt模块（包含活动分类、空间关系检测、接触检测三个子任务）带来1.1分的提升；单独引入LTP模块带来3.0分的提升；两者联合使用时，总增益达到5.7分。这一结果表明，精细化的交互建模与结构化的时空编码之间存在互补效应——AInt模块通过辅助损失迫使模型学习人-场景的细粒度关联，而LTP模块则为这种关联提供了空间布局和时间轨迹的先验结构。

在AInt模块内部，三个子任务的贡献并不均等。空间关系检测和接触检测对性能提升更为关键，因为它们直接建模了人与物体之间的瞬时空间配置和物理接触，这些信息对于回答“人正在触碰什么物体”或“人与桌子的空间关系是什么”等具体问题至关重要。

### 训练策略消融

Table 4考察了训练数据和策略的影响。在第一阶段对齐训练中，同时使用HIS描述、场景描述和运动描述三种数据，相比仅使用HIS描述，平均分提升2.9分。这表明多模态描述数据的混合训练有助于模型建立更稳健的跨模态对齐，场景和运动的单模态描述为后续的人-场景联合推理提供了基础语义锚点。

此外，Table 9显示冻结大语言模型（LLM）参数进行训练（48.7分）显著优于使用LoRA微调（38.1分）。这一反直觉的结果暗示，在HIS-GPT的两阶段训练框架下，保持预训练LLM的完整语言能力对于维持指令遵循和复杂推理的质量至关重要，而参数高效的微调方法可能破坏了LLM原有的语义空间。

### 评估可靠性验证

由于HIS-Bench采用GPT-4作为自动评分器，论文通过两项验证实验确认了评估的可靠性。人工评分与GPT-4评分的Pearson相关系数为0.54，表明两者具有中等程度的一致性；使用Qwen2.5-7B作为替代评分器时，与GPT-4评分的一致性达到0.75的相关系数（Table 6）。这些结果说明自动评估虽存在一定噪声，但能够可靠地反映模型的相对排序。

![[assets/figures/papers/paper_list_l1683_HIS_GPT_Towards_3D_Human_In_Scene_Multimodal_Understanding/figures/014_Table_6.jpg]]
*Table 6: The consistencies of HIS-Bench average scores on multiple baseline models and HIS-GPT, by using GPT-4 [46] and Qwen2.5-7B [7] as evaluators, respectively*

### 失败模式与局限性

尽管HIS-GPT在整体上表现优异，但在某些子任务上仍存在明显短板。从Table 2的细粒度维度来看，涉及复杂时序推理和长程依赖的任务（如动作序列理解和意图预测）得分相对较低。这源于模型对运动序列的编码依赖于固定长度的VQ-VAE离散嵌入，可能丢失了细粒度的时序细节。

更根本的局限在于，HIS-Bench本身仅覆盖31个场景和有限的运动类型，模型的泛化能力尚未在开放域的真实场景中得到验证。此外，模型依赖预训练的固定编码器（Uni3D和VQ-VAE），这些编码器在各自领域训练时可能引入了领域偏差，当面对与训练分布差异较大的场景-运动组合时，性能可能显著下降。

### 补充图表

![[assets/figures/papers/paper_list_l1683_HIS_GPT_Towards_3D_Human_In_Scene_Multimodal_Understanding/figures/008_Table_3.jpg]]
*Table 3: Ablations on the key components of HIS-GPT. ‘act’, ‘spa’ and ‘cont’ denotes the activity classification, spatial relation detection and human-scene contact detection task in AInt module. ‘PE’ denotes position encoding methods*

![[assets/figures/papers/paper_list_l1683_HIS_GPT_Towards_3D_Human_In_Scene_Multimodal_Understanding/figures/007_Table_4.jpg]]
*Table 4: Ablations on the training strategy of HIS-GPT. ‘HIS’, ‘Scene’ and ‘Motion’ denotes the usage of HIS, scene and motion data in stage 1 training*

![[assets/figures/papers/paper_list_l1683_HIS_GPT_Towards_3D_Human_In_Scene_Multimodal_Understanding/figures/021_Table_9.jpg]]
*Table 9: Ablations on the LLM tuning strategy of HIS-GPT*

![[assets/figures/papers/paper_list_l1683_HIS_GPT_Towards_3D_Human_In_Scene_Multimodal_Understanding/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative comparisons of HIS-GPT and other baselines on HIS-QA. Red/green color denotes wrong/correct outputs*

![[assets/figures/papers/paper_list_l1683_HIS_GPT_Towards_3D_Human_In_Scene_Multimodal_Understanding/figures/003_Table_1.jpg]]
*Table 1: Overview of existing benchmarks related to 3D scene and human. ‘mo.gen.’, ‘det.’, ‘cap.’ and ‘q.a.’ refers to motion generation, detection, caption, and question-answering, respectively*

![[assets/figures/papers/paper_list_l1683_HIS_GPT_Towards_3D_Human_In_Scene_Multimodal_Understanding/figures/004_Figure_3.jpg]]
*Figure 3: Text annotation pipeline for HIS data. For scene annotations, we segment the 3D scene to derive instance-level labels, bounding boxes, and reference expressions. For motion annotations, we obtain motion-level activities from existing labels or video MLLMs. Additionally, expert models and rules are used to generate frame-level annotations, including pose, human-scene contact, and human position*



## 定位与知识库关联

### 与现有方法的定位关系

HIS-GPT 处于 **3D 场景理解 LLM** 与 **人体运动分析** 的交叉地带，其核心贡献在于首次将两个模态的联合编码引入大语言模型框架。现有工作可大致分为三条线索：

**3D 场景 LLM**：以 **LL3DA**（Chen et al., CVPR 2024）和 **Chat-Scene**（Huang et al., NeurIPS 2023）为代表的工作将 3D 场景点云编码后接入 LLM，实现了场景级别的视觉问答。但这些模型仅处理静态场景，缺乏对人体动态的建模能力。在 HIS-Bench 上，Chat-Scene 仅取得 8.2 的平均分（Table 2），说明纯场景理解无法应对人-场景交互问答。

**通用视觉 LLM**：**GPT-4o**（Hurst et al., 2024）、**Qwen-VL-max**（Bai et al., 2023）和 **LLaVA-OV**（Li et al., TMLR 2024）等模型在通用视觉问答上表现突出，但面对 3D 场景与人体运动的联合输入时，缺乏结构化的空间-时间编码机制。GPT-4o 在 HIS-Bench 上取得 31.3 分，为视觉 LLM 中最优，但仍与 HIS-GPT 的 48.7 分存在 17.4 分的显著差距（Table 2）。**LLaVA-OV + GPT-4** 组合（用 LLaVA-OV 生成帧描述，再由 GPT-4 回答）同样表现不佳，说明间接的文本描述无法替代对 3D 几何和运动轨迹的直接建模。

**人体运动理解**：现有运动生成和识别方法（如 motion diffusion models）通常忽略场景上下文，而 HIS-GPT 通过 AInt 模块显式建模人-物空间关系和接触状态，填补了这一空白。

### 方法适用边界

**有效场景**：HIS-GPT 在以下条件下表现最优：
- 场景包含明确的可交互物体（家具、工具等），且物体与人体存在空间邻近关系
- 人体运动序列完整，包含足够的帧数以捕获动作语义
- 任务涉及空间关系推理、活动识别、接触判断等需要联合建模的能力

**性能衰减场景**（需人工验证）：
- 场景物体稀疏或运动幅度极小（如静坐），此时 AInt 模块的 k 近邻融合可能引入噪声
- 第一人称视角下的不完整观察——模型依赖完整的场景点云和人体关节序列，尚未针对遮挡或部分观测进行设计
- 训练数据覆盖 750+ 场景（Sec. 5.1），但 HIS-Bench 仅含 31 个场景，模型对全新场景-运动组合的泛化能力尚未充分验证

### 已知局限

1. **场景多样性有限**：HIS-Bench 仅包含 31 个场景和有限的运动类型，可能无法全面覆盖真实世界的多样性。模型在更广泛的开放场景中的表现需要进一步评估。

2. **评估噪声**：自动评估依赖 GPT-4 作为评分器。尽管与人工评价的 Pearson 相关系数为 0.54，且与 Qwen2.5-7B 评估器的一致性为 0.75，但自动评分仍存在系统性偏差的风险。

3. **编码器偏差继承**：模型依赖预训练的固定编码器（Uni3D 场景编码器、VQ-VAE 运动编码器），可能继承其在特定领域数据上的偏差，影响对边缘案例的处理。

4. **静态推理范式**：模型尚未在实时交互或动态变化的环境中进行测试，无法满足具身智能体对低延迟响应的需求。

### 开放问题

1. **泛化能力**：HIS-GPT 能否推广到未见过的场景-运动组合？当前训练数据与评测场景的重叠程度未明确报告，跨场景泛化的上下界尚不清楚。

2. **不完整观测**：如何适应第一人称视角下的遮挡和部分观测？这需要模型具备从局部信息推断全局交互的能力。

3. **实时性**：模型是否能够进行实时响应以满足具身智能体的需求？当前架构依赖 LLM 解码，推理延迟可能成为部署瓶颈。

4. **辅助任务组合**：AInt 模块的三个辅助任务（活动分类、空间关系检测、接触检测）联合贡献 1.1 点增益（Table 3），但它们的最优组合是否随下游任务变化？是否存在冗余或冲突的任务对？这一问题尚未被系统研究。

5. **Scaling 行为**：HIS-GPT 使用 Vicuna-1.5 作为 LLM 骨干，冻结 LLM 的效果优于 LoRA 微调（48.7 vs 38.1, Table 9）。更强的 LLM 骨干是否能带来线性增益，还是交互编码的质量会成为新瓶颈？



## 原文 PDF

![[paperPDFs/arxiv_2025/HIS_GPT_Towards_3D_Human_In_Scene_Multimodal_Understanding.pdf]]
