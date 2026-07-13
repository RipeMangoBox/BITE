---
title: "QUANTIPHY: A Quantitative Benchmark Evaluating Physical Reasoning Abilities of Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/QUANTIPHY_A_Quantitative_Benchmark_Evaluating_Physical_Reasoning_Abilities_of_Vision_Language_Models.pdf
project_link: "https://quantiphy.stanford.edu/"
code_link: "https://github.com/Paulineli/QuantiPhy"
aliases:
- QUANTIPHY
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 决定模型回答准确性的关键变量是“输入忠实度”——即模型是否真正使用提供的物理先验（尺寸/速度/加速度）和视频观测到的像素运动来推导未知量，而不是依赖内部记忆。这一可控变量可通过对比“视频+先验”与“仅先验”条件下的性能来显式检验，并通过反事实先验实验予以证实。
primary_logic: QUANTIPHY通过要求输出带单位的连续数值，首次量化了VLM在物理推理中“定性合情性与定量准确性之间的巨大鸿沟”。尽管从物理原理上仅需简单的比例关系即可精确求解，现有VLM仍大量产生“数值幻觉”，其推理更接近“记忆与猜测”而非“观测与计算”，这为迈向真正物理世界的AI系统指明了关键差距。
claims:
- 在“仅先验（无视频）”条件下，多数VLM的性能与提供完整视频输入时非常接近，表明模型严重依赖先验知识而非视觉信息。例如SmolVLM-Instruct在Video+Prior下MRA=32.7，而在Prior only下仍为38.9，视频并未带来实质性帮助。
- 反事实先验实验中，几乎所有模型的MRA下降约80%，最强模型也下降70%，直接证明模型根本没有利用视觉信号，而是被文本先验所支配。例如Qwen3-VL-32B的MRA从正常条件的50.1骤降至34.0。
- 链式思维提示仅对个别模型有效，绝大多数模型性能反而下降（如ChatGPT-5.1从56.1降至27.7），表明当前VLM难以通过文本自引导正确执行多步数值推理。
- 即使是最强专有模型（ChatGPT-5.1综合MRA 53.1）也未能超过人类平均水平（55.6），且远低于理论上可达到的精确上限，说明定量物理推理对VLM而言仍是开放挑战。
---

# QUANTIPHY: A Quantitative Benchmark Evaluating Physical Reasoning Abilities of Vision-Language Models

> [!tip] 核心洞察
> QUANTIPHY通过要求输出带单位的连续数值，首次量化了VLM在物理推理中“定性合情性与定量准确性之间的巨大鸿沟”。尽管从物理原理上仅需简单的比例关系即可精确求解，现有VLM仍大量产生“数值幻觉”，其推理更接近“记忆与猜测”而非“观测与计算”，这为迈向真正物理世界的AI系统指明了关键差距。

| 字段 | 内容 |
|------|------|
| 中文题名 | QUANTIPHY：评估视觉语言模型物理推理能力的量化基准 |
| 英文题名 | QUANTIPHY: A Quantitative Benchmark Evaluating Physical Reasoning Abilities of Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.19526) · [Project](https://quantiphy.stanford.edu/) · [Code](https://github.com/Paulineli/QuantiPhy) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | QUANTIPHY定量物理推理基准与评估协议 |
| Dataset | QUANTIPHY Overall, QUANTIPHY 2D-Dynamic, QUANTIPHY 3D-Dynamic |

> [!tip] 效果简介
> - QUANTIPHY Overall 上，MRA 53.1 (ChatGPT-5.1) vs 55.6 (Human Baseline) (-2.5)；MRA 46.0 (Qwen3-VL-32B) vs 53.1 (ChatGPT-5.1) (-7.1)。
> - QUANTIPHY 2D-Dynamic 上，MRA 56.2 (ChatGPT-5.1) vs 59.1 (Human) (-2.9)。
> - QUANTIPHY 3D-Dynamic 上，MRA 58.3 (ChatGPT-5.1) vs 57.9 (Human) (+0.4)。

## 概要

QUANTIPHY是首个系统性评估视觉语言模型（VLM）对视频中物体运动学属性进行**定量推理**能力的基准，发表于CVPR 2026。与现有物理推理基准（如PhysBench、VSI-Bench、STAR等）依赖定性视觉问答或多选题的范式不同，QUANTIPHY要求模型输出**带物理单位的连续数值**，并以**平均相对准确率（MRA）** 衡量预测值与真值在多个容差阈值下的接近程度，从而首次量化了VLM在物理推理中“定性合情”与“定量准确”之间的巨大鸿沟。

**核心发现**：当前VLM在定量物理推理中的主要瓶颈并非视觉感知能力不足，而是缺乏将像素级运动信息与文本先验进行精确数值换算的推理机制。决定性证据来自消融实验——在“仅提供先验、移除视频”的条件下，多数模型的MRA与完整视频输入时几乎持平（如SmolVLM-Instruct在Video+Prior下MRA=32.7，Prior only下反而为38.9）；反事实先验实验进一步表明，几乎所有模型的MRA下降约80%，最强模型也下降70%。这直接证明模型严重依赖预训练语料中的“世界知识”生成答案，而非忠实地从视频帧中提取目标物体的像素轨迹并依据给定先验进行比例计算。即使是最强的专有模型（ChatGPT-5.1，综合MRA 53.1），也未能超过人类平均水平（55.6），且链式思维提示（CoT）对绝大多数模型反而造成性能下降，表明当前VLM难以通过文本自引导正确执行多步数值推理。

**方法定位**：QUANTIPHY构建了一个包含Blender仿真、多视角实验室捕捉和互联网筛选三种来源的视频数据集，经分割、标注后为每个视频生成多个（先验，提问，真值）三元组，并归类为2D/3D与静态/动态四个核心任务组合。任务要求模型在给定单一物理先验（尺寸/速度/加速度）的条件下，推断目标物体在世界空间的相应运动学量——从物理原理上仅需简单的比例关系即可精确求解，但现有VLM仍大量产生“数值幻觉”，其推理更接近“记忆与猜测”而非“观测与计算”，为迈向真正物理世界的AI系统指明了关键差距。



### 物理推理：从定性到定量的范式跃迁

理解物理世界中的运动规律是通用具身智能系统的核心能力之一。现实场景中，物体的尺寸、速度、加速度等运动学属性通过物理定律相互关联：给定任一属性的先验值，理论上即可通过比例关系精确推导其余未知量。这一看似简单的推理链条——从视频中提取像素级运动信息，结合给定的物理先验进行数值换算——构成了定量物理推理的基本逻辑。

然而，现有视觉语言模型（VLM）的物理推理评估长期停留在**定性层面**。以 **PhysBench** 为代表的现有基准采用多选题或描述性问答形式，仅考察模型是否“大致理解”物理现象，而非能否给出精确的数值答案。即便是最先进的专有模型，在 PhysBench 上的准确率也仅约 60%。**VSI-Bench** 和 **Super-VSI** 虽引入了数值空间理解任务，但局限于静态场景，未能触及动态物理推理的核心挑战。**STAR** 等综合基准同样未将定量精度作为评估目标。

这一评估范式的缺失掩盖了一个关键问题：**VLM 在物理推理中究竟是在“观测与计算”，还是在“记忆与猜测”？**

### 核心瓶颈：输入忠实度的缺失

QUANTIPHY 的设计直指当前 VLM 物理推理的根本瓶颈——并非视觉感知能力不足，而是**缺乏将像素级运动信息与文本先验进行精确数值换算的推理机制**。模型倾向于激活预训练语料中的“世界知识”（如典型物体尺寸、重力加速度）来生成答案，而非忠实地从视频帧中提取目标物体的像素轨迹，并依据给定先验进行比例计算。

这一判断得到了多维度实验的有力支持：

- **视频消融实验**：在“仅提供先验、移除视频”的条件下，多数 VLM 的性能与完整输入条件非常接近。例如 SmolVLM-Instruct 在 Video+Prior 下 MRA 为 32.7，而在 Prior only 下反升至 38.9——视频并未带来实质性帮助（Table 2）。
- **反事实先验实验**：当提供与真实物理世界相悖的先验值时，几乎所有模型的 MRA 下降约 80%，最强模型也下降 70%。例如 Qwen3-VL-32B 的 MRA 从正常条件的 50.1 骤降至 34.0（Table 2 counterfactual column）。这表明模型将给定先验视为绝对真理，完全忽视视觉证据。
- **链式思维提示失效**：CoT 提示仅对极个别模型有正面效果，绝大多数模型性能反而下降（如 ChatGPT-5.1 从 56.1 降至 27.7），说明当前 VLM 的多步数值推理能力不足以支撑定量计算（Table 2 CoT column）。

### 人类参照系：定量推理仍是开放挑战

即便在任务设计上仅需简单的比例换算，最强专有模型 ChatGPT-5.1 的综合 MRA 也仅为 53.1，未能超越人类平均水平 55.6，且远低于理论上可达到的精确上限（Table 1）。值得注意的是，人类参与者多具备技术背景，其表现可能已被高估，但模型与人类在**忠实利用视觉线索**上的根本差异仍然显著——模型依赖记忆，人类依赖观测。

这一“定性合情性与定量准确性之间的巨大鸿沟”构成了 QUANTIPHY 的核心洞察，也为迈向真正物理世界的 AI 系统指明了关键差距。



## 核心方法与创新机理

QUANTIPHY的核心创新在于将VLM物理推理能力的评估从**定性VQA范式**彻底转向**定量数值回归范式**。这一转变并非简单的输出格式调整，而是对模型“是否真正理解物理运动”这一问题的重新定义——从“能否选对答案”变为“能否算对数值”。

### 范式转变：从选择题到数值计算

现有物理推理基准（如**PhysBench**、**STAR**）均采用多选题或定性描述作为输出格式，模型只需在离散选项中做出选择即可获得高分。QUANTIPHY则要求模型输出**带物理单位的连续数值**（如米、米/秒、米/秒²），并通过**平均相对准确率（MRA）** 在多个容差阈值下评估预测值与真值的接近程度。这一设计直接暴露了当前VLM的核心缺陷：模型在定性判断上表现尚可，但在需要精确数值换算时大量产生“数值幻觉”。

### 任务设计：运动学推断的统一框架

QUANTIPHY定义了统一的**运动学推断任务**：给定一段视频和一个关于源物体的单一物理先验（尺寸、速度或加速度），模型需要推断目标物体在世界空间中的未知运动学属性。这一任务设计的精妙之处在于，从物理原理上仅需简单的比例关系即可精确求解——先验提供了将像素空间测量值映射到世界空间的尺度因子γ：

$$\gamma = \begin{cases} S^{world}/S^{pixel}, & \text{尺寸先验} \\ |V_{t0}^{world}|/|V_{t0}^{pixel}|, & \text{速度先验} \\ |A_{t0}^{world}|/|A_{t0}^{pixel}|, & \text{加速度先验} \end{cases}$$

这意味着任务本身的**计算复杂度极低**，理论上任何具备基本代数能力的系统都应能完美求解。然而实验结果表明，即使是最强专有模型（ChatGPT-5.1综合MRA 53.1）也未能超越人类平均水平（55.6），揭示了VLM在“观测与计算”这一基本能力上的根本性不足。

### 覆盖维度：2D/3D与静态/动态的系统组合

QUANTIPHY通过**维度（2D/3D）** 和**先验类型（静态/动态）** 的交叉组合，构建了四种核心任务类别：2D-静态、2D-动态、3D-静态、3D-动态。这一设计使得基准能够系统性地考察模型在不同感知难度（2D仅需平面运动理解，3D还需深度估计）和不同推理需求（静态先验仅需空间比例，动态先验还需时序信息提取）下的表现差异，从而精确定位VLM的能力瓶颈所在。

### 数据构建：仿真-实验室-互联网的三源融合

为兼顾可控性与真实性，QUANTIPHY从三个维度收集原始视频：**Blender仿真**提供完全可控的环境和精确的真值标注；**多视角实验室捕捉**通过定制动作捕捉系统获取真实物体的物理属性；**互联网筛选**引入自然场景的多样性。这种三源融合策略确保了基准既具有精确的定量真值，又覆盖了真实世界的视觉复杂性。



QUANTIPHY 的整体框架围绕一个核心命题展开：**评估视觉语言模型（VLM）能否利用给定的单一物理先验，从视频中观测到的像素运动出发，定量推断目标物体的运动学属性**。该框架并非提出新的模型架构，而是构建了一套从数据生成到模型评估的标准化流程，用以系统性地暴露当前 VLM 在“定性合情”与“定量准确”之间的鸿沟。

### 任务定义与输入输出流

基准的核心任务被形式化为一个**运动学推断问题**。给定一段视频和一个关于源物体的单一物理先验（尺寸、速度或加速度），模型需要推断目标物体在世界空间中的对应物理量。这一设定利用了运动学量之间的互推关系：在已知一个先验的条件下，通过从视频中提取像素空间的尺寸、速度或加速度，再经由比例因子 $\gamma$ 换算，即可精确求解未知量。

具体而言，像素空间的运动量通过有限差分近似获得：

$$ \mathbf{V}_t^{pixel} \approx \frac{\mathbf{X}_{t+\mathrm{d}t}^{pixel} - \mathbf{X}_t^{pixel}}{\mathrm{d}t} $$

$$ \mathbf{A}_t^{pixel} \approx \frac{\mathbf{X}_{t+2\mathrm{d}t}^{pixel} - 2\mathbf{X}_{t+\mathrm{d}t}^{pixel} + \mathbf{X}_t^{pixel}}{\mathrm{d}t^2} $$

世界空间与像素空间之间通过标量因子 $\gamma$ 关联：

$$ S^{world} = \gamma S^{pixel}, \quad \mathbf{V}_t^{world} = \gamma \mathbf{V}_t^{pixel}, \quad \mathbf{A}_t^{world} = \gamma \mathbf{A}_t^{pixel} $$

$\gamma$ 由提供的先验类型决定：

$$ \gamma = \begin{cases} S^{world}/S^{pixel}, & \text{尺寸先验} \\ |V_{t0}^{world}|/|V_{t0}^{pixel}|, & \text{速度先验} \\ |A_{t0}^{world}|/|A_{t0}^{pixel}|, & \text{加速度先验} \end{cases} $$

从原理上看，这仅需简单的比例计算即可精确求解。然而，这正是 QUANTIPHY 设计的精妙之处：**通过将任务简化为数学上可精确求解的形式，它排除了“任务本身太难”这一干扰因素，从而将瓶颈直接锁定在 VLM 的推理机制上**。

### 评估范式与指标

与现有物理推理基准（如 **PhysBench**、**STAR** 等采用定性 VQA 或多选题的形式）不同，QUANTIPHY 要求模型输出**带物理单位的连续数值**。这一范式转变使得评估从“选对选项”升级为“算对数值”，从而能够更精细地刻画模型的推理能力。

评估采用**平均相对准确率（Mean Relative Accuracy, MRA）**作为核心指标：

$$ \mathrm{MRA} = \frac{1}{10} \sum_{\theta \in \mathcal{C}} \mathbb{1}\left( \frac{|\hat{y} - y|}{|y|} < 1 - \theta \right) $$

其中 $\mathcal{C}$ 为一系列容差阈值。MRA 在多个宽松程度上评估预测值与真值的接近程度，相比简单的精确匹配或单一阈值，能更全面地反映模型的定量推理质量。

### 基准构建的三阶段流水线

QUANTIPHY 的构建遵循一个三阶段流水线（Figure 4），确保数据的多样性、标注的精确性以及任务的系统性。

![[assets/figures/papers/paper_list_l2747_https_arxiv_org_abs_2512_19526/figures/004_Figure_4.jpg]]
*Figure 4: The construction of QUANTIPHY proceeds in three sequential stages. First, we collect diverse raw videos from three different sources. Additionally, we segment these videos with solid plain background (described in subsection 3.2). Second, we obtain high-quality annotations, employing distinct labeling methods tailored to each data source to accurately capture the object’s physical properties. Finally, we formulate the benchmark tasks by associating each video with multiple (prior, question, ground truth) triplets. Each triplet is then categorized as either 2D or 3D, depending on the object’s movement relative to the camera*

#### 阶段一：数据采集

数据来源覆盖三个互补的维度，兼顾可控性与现实适用性：

- **Blender 仿真**：提供对环境的完全控制和精确的真值标注。仿真涵盖物理驱动运动（如保龄球碰撞的刚体动力学模拟）和关键帧动画（如漂浮游泳圈的手动动画曲线）两类，后者视觉上合理但非物理导出，用于检验模型是否真正理解物理规律。
- **多视角实验室捕捉**：使用定制的运动捕捉系统在受控环境中录制真实物体的运动，通过多目立体重建获取精确的三维轨迹和尺寸信息。
- **互联网筛选**：从开源平台收集真实场景视频，并辅以自录制视频（身份信息已移除），增加场景的开放性和多样性。

#### 阶段二：数据标注

针对不同数据源采用差异化的标注策略以获取精确物理属性：

- Blender 数据直接从仿真引擎导出真值。
- 实验室数据通过多目立体重建和定制工具（如深度值采集 UI）获取像素级测量。
- 互联网数据则依赖人工像素测量工具进行标注，包括目标物体的关键点追踪和尺寸标定。

此外，所有视频均经过分割处理，将前景物体与背景分离，以便后续替换背景、控制场景复杂性。

#### 阶段三：问题构建

每个视频被关联多个 `(先验, 提问, 真值)` 三元组。根据目标物体相对于相机的运动方式，每个三元组被归类为 2D 或 3D 任务；根据提供的先验类型，又分为静态先验（尺寸）和动态先验（速度/加速度）。由此形成四类核心任务组合：2D-静态、2D-动态、3D-静态、3D-动态。Figure 3 展示了数据集在这四类上的分布统计。

![[assets/figures/papers/paper_list_l2747_https_arxiv_org_abs_2512_19526/figures/003_Figure_3.jpg]]
*Figure 3: QUANTIPHY Statistics. The collected data and curated QA pairs are among four main setups with further breakdowns*

### 模型评估流程

所有模型均通过统一的标准化提示模板进行询问，设置温度参数为 0 以确保确定性输出。模型输出的原始文本经过分层解析提取数值答案，随后计算 MRA。这一流程保证了不同模型之间的公平可比性。

### 框架的核心洞察

QUANTIPHY 框架的设计本身即蕴含了一个关键的可控变量：**输入忠实度**——模型是否真正使用提供的物理先验和视频观测到的像素运动来推导未知量，而非依赖内部记忆。通过在后续实验中对比“视频+先验”与“仅先验”条件下的性能，以及引入反事实先验，这一框架能够显式地检验 VLM 的推理机制是否忠实于输入。正如后续实验所揭示的，现有 VLM 的推理更接近“记忆与猜测”而非“观测与计算”，这正是 QUANTIPHY 框架所瞄准的根本性问题。

### 补充图表

![[assets/figures/papers/paper_list_l2747_https_arxiv_org_abs_2512_19526/figures/001_Figure_1.jpg]]
*Figure 1: On a crowded city street, a bird’s nest falls from a branch, a car rushes by, an eagle flits over a building, and a person walks in a crosswalk — the real world is full of complex physical motion. To enable AI to understand and navigate this environment, it is essential for generalist embodied systems to reason about physical properties quantitatively. Because objects obey common laws of physics, their kinematic properties (such as size, velocity, and acceleration) are interrelated. This interdependence makes it possible for visual AI to systematically reason about these properties with respect to available priors. In this work, we present QUANTIPHY, the first benchmark to evaluate the reas...*



QUANTIPHY基准的核心目标并非提出新的模型架构，而是定义一套可量化评估VLM物理推理能力的任务范式与评测协议。其“方法”本质上由**任务形式化**、**数据构建流水线**与**评估指标**三个关键模块构成。

### 任务形式化：运动学推断问题

QUANTIPHY将物理推理建模为一个**定量运动学推断任务**：给定一段视频和一个关于源物体的单一物理先验（尺寸、速度或加速度），要求模型推断目标物体在世界空间中的对应物理量。该任务设计的核心洞察在于：同一场景中的物体遵循共同的物理定律，其运动学属性通过一个统一的**尺度因子** $\gamma$ 相互关联，因此理论上仅需一个先验即可通过简单的比例关系精确求解所有未知量。

任务空间由两个维度交叉定义：
- **维度性**：2D（物体在相机平面内运动）与3D（物体有显著的深度方向运动）。
- **先验类型**：静态先验（如物体尺寸）与动态先验（如某时刻的速度或加速度）。

由此形成四种核心任务组合：2D-静态、2D-动态、3D-静态、3D-动态。这种设计使得基准能够系统地考察模型在不同信息条件下的推理能力。

### 核心公式与变量含义

QUANTIPHY任务背后隐含的物理关系可通过以下公式精确描述。这些公式并非模型需要显式输出的内容，而是定义了从像素观测到世界空间物理量的理论求解路径，同时也是生成真值标注的数学基础。

**像素空间运动估计**：模型首先需要从视频帧中提取目标物体的像素轨迹，并通过有限差分近似其运动学量。

像素空间速度的有限差分近似：
$$\mathbf{V}_t^{pixel} \approx \frac{\mathbf{X}_{t+\mathrm{d}t}^{pixel} - \mathbf{X}_t^{pixel}}{\mathrm{d}t}$$

像素空间加速度的有限差分近似：
$$\mathbf{A}_t^{pixel} \approx \frac{\mathbf{X}_{t+2\mathrm{d}t}^{pixel} - 2\mathbf{X}_{t+\mathrm{d}t}^{pixel} + \mathbf{X}_t^{pixel}}{\mathrm{d}t^2}$$

其中 $\mathbf{X}_t^{pixel}$ 表示物体在 $t$ 时刻的像素坐标，$\mathrm{d}t$ 为帧间时间间隔。

**世界空间尺度转换**：世界空间中的物理量与像素空间中的观测量通过标量尺度因子 $\gamma$ 线性关联：
$$S^{world} = \gamma S^{pixel},\quad \mathbf{V}_t^{world} = \gamma \mathbf{V}_t^{pixel},\quad \mathbf{A}_t^{world} = \gamma \mathbf{A}_t^{pixel}$$

**尺度因子的确定**：$\gamma$ 是连接像素观测与世界真值的关键桥梁，可根据提供的先验类型直接计算：
$$\gamma = \begin{cases} S^{world}/S^{pixel}, & \text{尺寸先验} \\ |V_{t0}^{world}|/|V_{t0}^{pixel}|, & \text{速度先验} \\ |A_{t0}^{world}|/|A_{t0}^{pixel}|, & \text{加速度先验} \end{cases}$$

一旦从给定先验中求得 $\gamma$，即可将其应用于任意目标物体的像素测量值，得到所求的世界空间物理量。这一求解路径在数学上是精确且确定的，因此理论上任何具备像素测量和比例计算能力的系统都应能达到极高的准确率。

**评估指标：平均相对准确率（MRA）**：为量化模型预测值与真值的接近程度，QUANTIPHY采用MRA作为主指标，其定义为在一组容差阈值上的平均准确率：
$$\mathrm{MRA} = \frac{1}{10} \sum_{\theta \in \mathcal{C}} \mathbb{1}\left( \frac{|\hat{y} - y|}{|y|} < 1 - \theta \right)$$

其中 $\hat{y}$ 为模型预测值，$y$ 为真值，$\mathcal{C}$ 为从宽松到严格的10档容差阈值集合。MRA的设计避免了单一阈值对模型能力的片面评判，能够更全面地反映模型在不同精度要求下的表现。

### 数据构建流水线

QUANTIPHY的数据构建遵循三阶段流水线，如图4所示：

**第一阶段：多源数据采集**。从三个互补渠道收集原始视频：(1) Blender仿真渲染，提供完全可控的环境和精确的真值标注，涵盖物理驱动运动（如刚体碰撞）和关键帧动画两类；(2) 多视角实验室捕捉，使用定制的动作捕捉系统录制真实物体的平移运动；(3) 互联网筛选，收集真实场景中的运动视频。所有视频均假设相机固定且物体做平移运动，以保证运动学关系的可解性。

**第二阶段：分层数据标注**。针对不同数据源采用差异化标注策略：Blender数据直接从仿真引擎导出物理属性；实验室数据通过多目立体重建和人工像素测量获取精确尺寸与轨迹；互联网数据则通过人工像素级测量工具标注。对于3D任务，额外提供深度信息以支持深度方向的推理。

**第三阶段：问题构建**。为每个视频生成多个（先验，提问，真值）三元组。每个三元组指定一个源物体的物理先验值，并提出一个关于目标物体物理量的定量问题。三元组按2D/3D和静态/动态两个维度分类，确保基准覆盖全面的任务类型。此外，通过对视频进行分割处理并替换背景，系统性地控制了场景复杂度（纯色背景、简单纹理背景、复杂背景）和目标数量（单目标、多目标），为后续的细粒度分析提供条件。



## 实验与关键发现

### 主要结果：定量物理推理的巨大鸿沟

QUANTIPHY在涵盖2D/3D、静态/动态先验的四类运动学推断任务上，对22个VLM及人类基线进行了系统评估。核心发现是：**当前最强VLM的定量物理推理能力仍不及人类平均水平，且存在严重的“数值幻觉”问题。**

从Table 1的整体MRA来看，人类基线达到55.6%，而最强专有模型**ChatGPT-5.1**仅取得53.1%的MRA，差距为-2.5个百分点。在开源权重模型中，**Qwen3-VL-32B**以46.0%的MRA位居榜首，但与ChatGPT-5.1仍有7.1个百分点的显著差距。值得注意的是，在3D-Dynamic子任务上，ChatGPT-5.1（58.3%）略微超越人类（57.9%），但这更多反映了该子任务对深度信息利用的特殊性，而非模型具备鲁棒的物理推理能力。

更关键的是，这一性能水平远非理论上可达到的上限。QUANTIPHY的任务设计在物理原理上极为简洁——给定一个先验物理量（如目标物体的尺寸、某时刻速度或加速度），通过像素空间的比例关系即可精确求解未知量。然而，模型的实际表现与这一理论上可达的精确上限之间存在巨大鸿沟，表明**当前VLM的推理机制更接近“记忆与猜测”，而非“观测与计算”**。

### 消融分析：输入忠实度的关键证据

#### 视频消融：视觉信息几乎未被利用

Table 2的“Prior only”条件直接揭示了核心瓶颈：当移除视频、仅提供文本先验时，多数模型的MRA与完整输入（Video+Prior）相比变化极小。例如，**SmolVLM-Instruct**在Video+Prior下MRA为32.7%，而在Prior only条件下反而升至38.9%——视频输入不仅未提供帮助，反而引入了噪声。这一现象在多个模型上反复出现，强有力地证明：**VLM在定量物理推断中严重依赖预训练语料中的“世界知识”（如典型物体尺寸、重力加速度），而非从视频帧中提取像素级运动信息。**

#### 反事实先验：模型将文本先验视为绝对真理

反事实先验实验提供了更直接的因果证据。当提供与视频实际内容矛盾的先验（如将真实速度5 m/s替换为50 m/s）时，几乎所有模型的MRA骤降约80%，即使最强模型也下降约70%。例如，**Qwen3-VL-32B**的MRA从正常条件的50.1%暴跌至34.0%。这一结果确证：**模型将给定的文本先验视为不可动摇的“锚点”，完全忽视视频中的视觉证据，其推理忠实性严重缺失。**

#### 链式思维提示：多步推理能力不足

链式思维（CoT）提示的效果进一步暴露了模型内部数值计算能力的缺陷。Table 2显示，CoT仅在极少数模型上有正面效果，绝大多数模型性能反而显著下降——**ChatGPT-5.1**从56.1%骤降至27.7%，降幅超过一半。这表明当前VLM难以通过文本自引导正确执行多步数值推理，简单的提示工程无法弥补架构层面的计算能力不足。

#### 场景因素：背景复杂性与多目标效应

Figure 5分析了场景背景复杂度和物体数量对性能的影响。结果显示，背景复杂度的影响微弱，但多目标场景（MX、MS、MC）普遍比单目标场景（SX、SS、SC）带来更高的MRA。这一现象暗示：**VLM能从场景中的额外参考物获益**，可能通过物体间的相对大小关系辅助比例估算，而非单纯依赖精确的像素测量。

#### 参数规模扩展效应

同一模型家族内的参数规模扩展对动态类任务（2D-Dynamic、3D-Dynamic）的提升较为明显，但对缩小与人类差距的作用有限，仍存在明显的性能天花板。这进一步说明，仅靠扩展模型规模不足以解决定量物理推理中的忠实性缺失问题。

### 失败模式与根本瓶颈

综合以上消融证据，QUANTIPHY揭示的失败模式可归纳为三个层次：

1. **视觉忽略**：模型在推理时几乎不提取视频中的像素轨迹信息，而是激活预训练语料中的统计先验生成答案。视频消融与反事实先验实验共同确证了这一模式。

2. **数值幻觉**：即使物理原理上仅需简单的比例关系即可精确求解，模型仍大量产生偏离真值的数值输出。这并非感知能力不足，而是缺乏将像素运动信息与文本先验进行精确数值换算的推理机制。

3. **多步推理崩溃**：链式思维提示未能改善性能，反而导致大幅下降，说明模型内部缺乏可靠的多步数值计算能力，文本自引导不足以弥补这一架构缺陷。

这些失败模式共同指向一个根本瓶颈：**当前VLM在定量物理推理中缺乏“输入忠实度”——即真正使用提供的物理先验和视频观测到的像素运动来推导未知量的能力。** 这一瓶颈的解决可能需要超越提示工程的方案，如引入外部工具（点追踪、深度估计）或设计专门的训练机制来强制模型执行输入忠实的比例计算。

### 人类基线对照

人类研究（Figure 39）显示，参与者平均MRA为55.6%，且2D任务（59.1%）与3D任务（57.9%）表现接近。需要注意的是，人类参与者多具备技术背景，其表现可能高于一般人群，但即便如此，最强VLM仍未超越这一基线。更重要的是，人类在利用视觉线索进行比例估算方面展现出VLM所不具备的忠实性——这正是QUANTIPHY所量化的核心差距。

![[assets/figures/papers/paper_list_l2747_https_arxiv_org_abs_2512_19526/figures/045_Figure_39.jpg]]
*Figure 39: Distribution of human quantitative reasoning performance. Horizontal boxplots summarize participant-level mean MRA scores for the 2D (top) and 3D (bottom) survey conditions*

### 补充图表

![[assets/figures/papers/paper_list_l2747_https_arxiv_org_abs_2512_19526/figures/005_Table_1.jpg]]
*Table 1: Evaluation results on QUANTIPHY. We report Mean Relative Accuracy (MRA %) on four kinematic categories (2S, 2D, 3S, 3D) and their average. Dark cell marks the best overall model and light cell marks the best open-weight model*

![[assets/figures/papers/paper_list_l2747_https_arxiv_org_abs_2512_19526/figures/006_Table_2.jpg]]
*Table 2: Extensive results on an analysis subset. We report Mean Relative Accuracy (MRA) in %. Rows follow the same model order as in Table 1*

![[assets/figures/papers/paper_list_l2747_https_arxiv_org_abs_2512_19526/figures/007_Figure_5.jpg]]
*Figure 5: Effect of scene context. We plot the MRA (%) scores for all benchmark models on different categories, sorted in descending order according to their average MRA performance*

![[assets/figures/papers/paper_list_l2747_https_arxiv_org_abs_2512_19526/figures/008_Figure_6.jpg]]
*Figure 6: Case 1: Faithful pixel–prior reasoning*

![[assets/figures/papers/paper_list_l2747_https_arxiv_org_abs_2512_19526/figures/010_Figure_7.jpg]]
*Figure 7: Case 2: Counterfactual prior breaks faithfulness*

![[assets/figures/papers/paper_list_l2747_https_arxiv_org_abs_2512_19526/figures/009_Figure_8.jpg]]
*Figure 8: Case 3: Video ablation reveals reliance on priors*

![[assets/figures/papers/paper_list_l2747_https_arxiv_org_abs_2512_19526/figures/011_Figure_9.jpg]]
*Figure 9: Case 4: Strong gravitational prior overrides counterfactual physics*

![[assets/figures/papers/paper_list_l2747_https_arxiv_org_abs_2512_19526/figures/012_Figure_10.jpg]]
*Figure 10: Distribution of MRA by model. One caveat to note is that the Avg. MRA in Table 1 reflects the mean MRA across inference task categories for each model (i.e., the average MRA of 2D-Static, 2D-Dynamic, 3D-Static, and 3D-Dynamic). In contrast, the mean in this distribution plot represents the average MRA at the individual-question level for each model*



## 定位与知识库关联

### 从定性问答到定量数值回归的范式转变

QUANTIPHY的出现标志着VLM物理推理评估从“定性合理”到“定量精确”的关键跃迁。在它之前，物理推理基准主要采用多选题或二分类的VQA范式：**PhysBench**要求模型判断物理现象是否合理，**STAR**通过综合选择题评估多维度物理理解，而**VSI-Bench**和**Super-VSI**虽然触及数值空间理解，但局限于静态场景且未涉及视频中的运动学推断。这些基准的共同局限在于：它们只能检测模型是否“大致知道”物理规律，却无法揭示模型是否真正从视觉输入中提取精确信息进行推理。

QUANTIPHY通过四个关键设计打破了这一局限：

1. **输出类型**：从离散选项或描述转向带物理单位的连续数值，迫使模型给出可量化验证的答案。
2. **评估指标**：从准确率/精确匹配转向平均相对准确率（MRA），通过多档容差阈值（$\theta \in \mathcal{C}$）评估预测值与真值的接近程度，既惩罚严重偏离又容忍合理误差。
3. **任务设计**：从静态场景理解转向基于视频的运动学量推断——给定目标物体的单一物理先验（尺寸/速度/加速度），要求模型从视频中提取像素运动并利用比例关系计算未知量。
4. **评估范式**：从定性VQA彻底转向定量数值回归，将物理推理从“常识判断”重新定义为“观测与计算”问题。

### 理论可解性与实际性能的鸿沟

QUANTIPHY任务的理论可解性建立在一个简洁的物理事实上：在相机固定、物体做平移运动的条件下，世界空间与像素空间通过标量因子$\gamma$关联：

$$S^{world} = \gamma S^{pixel}, \quad \mathbf{V}_t^{world} = \gamma \mathbf{V}_t^{pixel}, \quad \mathbf{A}_t^{world} = \gamma \mathbf{A}_t^{pixel}$$

其中像素空间的速度和加速度可通过有限差分直接从视频帧中提取：

$$\mathbf{V}_t^{pixel} \approx \frac{\mathbf{X}_{t+\mathrm{d}t}^{pixel} - \mathbf{X}_t^{pixel}}{\mathrm{d}t}$$

$$\mathbf{A}_t^{pixel} \approx \frac{\mathbf{X}_{t+2\mathrm{d}t}^{pixel} - 2\mathbf{X}_{t+\mathrm{d}t}^{pixel} + \mathbf{X}_t^{pixel}}{\mathrm{d}t^2}$$

给定任一先验（如目标尺寸$S^{world}$），只需从视频中测量对应像素量$S^{pixel}$即可求得$\gamma$，进而推算出所有其他运动学量。这一过程在数学上仅涉及简单的比例运算，理论上任何具备基本视觉感知能力的系统都应能达到极高精度。

然而，实验揭示的现实与理论形成尖锐对比：最强专有模型ChatGPT-5.1的综合MRA仅为53.1，未能超越人类平均水平（55.6），且远低于精确求解的理论上限。更关键的是，消融实验直接证明了模型并未真正执行这一“观测→测量→比例计算”的推理链条。

### 适用边界与根本局限

QUANTIPHY的设计本身划定了清晰的适用边界，这些边界既是其精确性的保证，也构成了当前评估范围的约束：

**运动类型限制**：基准仅覆盖平移运动且假设相机固定，未涉及旋转、形变、碰撞或流体等复杂物理现象。这意味着当前评估无法直接推广到更一般的物理推理场景，例如判断旋转物体的角动量或预测碰撞后的轨迹分布。

**数据来源的混合性质**：基准融合了Blender仿真、多视角实验室捕捉和互联网筛选视频三类数据，其中仿真数据提供完全精确的真值标注，但可能与真实世界的视觉统计存在分布偏移；互联网视频虽具有生态效度，但其标注依赖于人工像素测量，可能引入标注误差。

**先验依赖的结构性假设**：任务设计假设模型能够且应当利用给定的单一先验进行推理。这一假设在反事实实验中暴露出深层问题——模型将文本先验视为绝对真理而忽视视觉证据，表明当前VLM的推理机制本质上缺乏“输入忠实度”。

### 开放问题与未来方向

QUANTIPHY揭示的核心矛盾——模型在理论可精确求解的任务上仍大量产生“数值幻觉”——指向了若干关键开放问题：

**训练与架构层面的忠实度强制**：如何设计训练目标或架构机制，使VLM在推理时可靠地条件化于显式数值先验和像素级视觉证据，而非依赖语料记忆？当前的链式思维提示实验表明，单纯依赖文本自引导无法解决这一问题，可能需要引入显式的视觉测量模块或比例计算约束。

**外部工具的协同整合**：能否通过引入点追踪、深度估计等专用视觉工具与VLM协同，弥补模型在精确像素测量上的不足？这一方向将物理推理分解为“视觉感知”（由专用工具完成）和“符号推理”（由VLM完成）两个阶段，可能绕过当前端到端模型的精度瓶颈。

**基准的扩展维度**：对于更复杂的物理场景（如旋转、碰撞、流体），定量基准应如何扩展以全面评估模型对物理原理的掌握？这需要在保持数值可验证性的同时引入更丰富的物理现象，可能涉及多体动力学、非刚体运动等新任务类型。

**人类-模型差异的本质**：尽管人类平均MRA仅略高于最强模型，但人类和模型在“如何得出答案”上存在根本差异——人类参与者能够忠实利用视觉线索进行比例估算，而模型则被文本先验所支配。理解这一差异的认知根源，将是构建真正物理世界AI的关键一步。



## 原文 PDF

![[paperPDFs/CVPR_2026/QUANTIPHY_A_Quantitative_Benchmark_Evaluating_Physical_Reasoning_Abilities_of_Vision_Language_Models.pdf]]
