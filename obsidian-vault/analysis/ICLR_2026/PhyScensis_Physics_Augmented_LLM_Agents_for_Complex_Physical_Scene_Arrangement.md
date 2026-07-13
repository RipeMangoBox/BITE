---
title: "PhyScensis: Physics-Augmented LLM Agents for Complex Physical Scene Arrangement"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/PhyScensis_Physics_Augmented_LLM_Agents_for_Complex_Physical_Scene_Arrangement.pdf
project_link: https://physcensis.github.io
code_link: null
openreview_forum_id: aCVfhY4Qen
aliases:
- PhyScensis
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入物理引擎和概率规划，使得物体放置能够符合真实物理约束，并允许用户通过参数精细控制稳定性和空间关系。"
primary_logic: "将物理仿真与基于LLM的智能体闭环框架相结合，通过迭代谓词生成、求解与反馈，能够在无需训练数据的情况下生成物理准确、高度复杂且强可控的3D场景。"
claims:
- "在VQA Score、GPT Ranking和Settle Distance三个指标上，PhyScensis均显著优于Architect和3D-Generalist。"
- "消融实验验证了反馈系统对于提升场景生成效率的关键作用，完整反馈系统大幅降低重试次数。"
- "基于PhyScensis生成的数据训练的机器人策略，在人类设计的未见场景中达到9/10的到达成功率和3/10的放置成功率，优于所有基线。"
- "用户研究报告在文本对齐、自然性与物理合理性、复杂度三个维度上，PhyScensis得分分别为4.04、3.98、3.82，远高于基线（~2.5-3.0）。"
---

# PhyScensis: Physics-Augmented LLM Agents for Complex Physical Scene Arrangement

> [!tip] 核心洞察
> 将物理仿真与基于LLM的智能体闭环框架相结合，通过迭代谓词生成、求解与反馈，能够在无需训练数据的情况下生成物理准确、高度复杂且强可控的3D场景。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | PhyScensis：面向复杂物理场景布置的物理增强大语言模型智能体 |
| 英文题名 | PhyScensis: Physics-Augmented LLM Agents for Complex Physical Scene Arrangement |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=aCVfhY4Qen) · [Project](https://physcensis.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PhyScensis |
| Dataset | Custom scene generation prompts, Robot pick-and-place task |

> [!tip] 效果简介
> - Custom scene generation prompts 上，VQA Score ↑ 为 0.704 ± 0.425，对比 Architect: 0.493, 3D-Generalist: 0.578，变化 相对3D-Generalist提升21.8%。
> - Custom scene generation prompts 上，GPT Ranking ↓ 为 1.429 ± 0.562，对比 Architect: 2.607, 3D-Generalist: 1.946，变化 相对3D-Generalist降低26.5%。
> - Custom scene generation prompts 上，Settle Distance ↓ 为 0.003 ± 0.008，对比 Architect: 0.405, 3D-Generalist: 0.033，变化 物理稳定度接近完美。

## 概要

现有3D场景生成方法在物体放置时普遍忽略接触、支撑、平衡、包含等物理交互，导致生成结果无法保证物理准确性，严重限制了其在复杂机器人操作环境中的应用。针对这一瓶颈，PhyScensis提出将物理引擎与基于大语言模型（LLM）的智能体闭环框架相结合，通过迭代谓词生成、求解与反馈，在不依赖训练数据的前提下，生成物理准确、高度复杂且强可控的3D场景。

该方法的核心机制在于引入概率规划来量化与控制场景稳定性，同时通过空间求解器（基于凸包的碰撞检测）和物理求解器（体素占位网格加物理仿真）实现复杂堆叠与容器放置。完整的反馈系统则负责检测失败原因，报告空区域与场景质量指标，驱动LLM智能体进行迭代优化。

主要实验结果表明，PhyScensis在场景生成质量与物理稳定性上显著优于现有基线。在VQA Score上达到0.704，相对3D-Generalist提升21.8%；GPT Ranking降至1.429，相对降低26.5%；Settle Distance仅为0.003，物理稳定度接近完美（Table 1）。消融实验验证了反馈系统对提升生成效率的关键作用，完整反馈大幅降低了重试次数（Table 2），而纯LLM预测放置由于缺乏碰撞检查与物理约束，导致最高的Settle Distance，证实了物理求解器的必要性（Table 3）。在机器人拾取-放置任务中，基于PhyScensis生成数据训练的策略在人类设计的未见场景上达到9/10的到达成功率和3/10的放置成功率，均优于所有基线（Table 1）。用户研究进一步表明，PhyScensis在文本对齐、自然性与物理合理性、复杂度三个维度上的得分分别为4.04、3.98、3.82，远高于基线方法的约2.5–3.0（Table 4）。

在方法谱系上，PhyScensis区别于Architect（Wang et al., 2024b）基于图像修复的单步生成和3D-Generalist（Sun et al., 2025b）的VLM驱动2D像素级放置，首次将物理引擎集成进LLM智能体的闭环框架，实现了从“碰撞避免”到“物理真实性保证”的质变。与LayoutVLM（Sun et al., 2025a）的房间级布局生成和ClutterGen（Jia & Chen, 2024）的强化学习杂乱场景创建相比，PhyScensis通过开放词汇资产检索与文本到3D生成管道，在资产多样性和场景覆盖范围上具有明显优势。

当前方法的主要局限在于依赖物理仿真导致的计算开销较大，尤其在生成极端不稳定场景时迭代成本高；资产库的规模与质量直接影响多样性，对罕见物品的检索不够鲁棒；LLM Agent的谓词质量受提示工程影响，可能出现语法错误或不符合物理常识的布局要求。此外，系统目前仅针对静态场景布置，尚未涉及动态交互或时序任务。

### 问题背景：3D场景生成的物理真实性缺口

在机器人操作、具身智能和虚拟环境构建中，生成逼真且物理合理的3D场景是核心需求。现有3D场景生成方法主要关注视觉外观和空间布局，却普遍忽略物体间的物理交互——包括接触、支撑、平衡和包含关系。这一缺陷导致生成场景在物理上不可靠：物体可能悬浮、穿透或处于力学上不可能的姿态，严重限制了其在复杂机器人操作环境中的应用。

### 现有方法的局限

当前主流的场景生成范式存在以下结构性瓶颈：

**缺乏物理真实性保障。** 以 **Architect**（Wang et al., 2024b）为代表的基于图像修复的方法，以及 **3D-Generalist**（Sun et al., 2025b）等VLM驱动的2D像素级物体放置方法，仅依赖碰撞避免或深度估计来约束物体位置，无法保证支撑、堆叠和容器放置等复杂交互的物理合理性。**LayoutVLM**（Sun et al., 2025a）专注于房间级布局，同样缺乏对物体间物理约束的建模。**ClutterGen**（Jia & Chen, 2024）通过强化学习创建杂乱场景，但生成的场景密度和物理交互复杂度有限。

**单步生成，缺乏纠错能力。** 现有方法通常采用单步生成策略，一旦输出结果存在物理冲突或布局错误，系统无法进行诊断和修正。这种开环设计在面对复杂场景描述时，容易产生不可用的输出。

**空间与物理表征粗糙。** 基线方法多使用轴对齐包围盒进行简单的2D碰撞避免，难以处理需要精确3D几何推理的堆叠、容器放置和部分支撑等场景。这从根本上限制了生成场景的复杂度和物理精度。

**资产多样性受限。** 依赖固定、人工预定义的资产库，难以覆盖开放词汇描述的多样化场景需求，对罕见物品的处理能力不足。

### 核心动机

针对上述缺口，本文提出 **PhyScensis**——一个物理增强的大语言模型智能体框架。核心动机在于：将物理仿真与基于LLM的智能体闭环框架相结合，通过迭代谓词生成、求解与反馈，在无需训练数据的情况下生成物理准确、高度复杂且强可控的3D场景。具体而言，PhyScensis旨在实现三个关键目标：

1. **物理准确性**：集成物理引擎进行真实仿真，并通过概率规划量化与控制稳定性，使物体放置符合真实物理约束。
2. **高复杂度与强可控性**：支持用户通过细粒度文本描述和数值参数精细控制场景的稳定性、空间关系和杂乱程度。
3. **开放词汇适应性**：结合开放词汇资产检索与文本到3D生成管道，扩大场景覆盖范围，适配多样化的下游任务（如机器人策略训练）。

## 核心方法与创新机理

PhyScensis 的核心创新在于首次将**物理仿真引擎**与**基于 LLM 的智能体闭环框架**深度耦合，系统性地解决了现有 3D 场景生成方法中“物理交互缺失”这一根本瓶颈。与仅依赖碰撞避免或深度估计的基线方法不同，PhyScensis 通过以下关键机制实现了物理准确、高度复杂且强可控的场景布置。

### 1. 物理交互保证：从碰撞避免到真实仿真与概率规划

现有方法如 **Architect** (Wang et al., 2024b) 和 **3D-Generalist** (Sun et al., 2025b) 仅能保证物体间不发生碰撞，或通过深度估计进行简单的空间推理，无法处理接触、支撑、平衡、包含等真实物理交互。PhyScensis 的核心突破在于：

- **集成物理引擎进行真实仿真**：系统通过物理求解器（Physical Solver）调用物理引擎，对堆叠、支撑、容器放置等复杂物理谓词进行真实动力学仿真，确保生成的场景在物理上是可行的（Section 3.3）。
- **概率规划量化与控制稳定性**：引入概率规划框架，通过采样扰动向量 $x = \left[ \Delta p , \Delta \bar{r} , \Delta c , \Delta \mu , \Delta m \right] \in \mathbb{R}^{d}$（$d=11$，包含位置、旋转、质心、摩擦和质量偏移）评估场景的局部失败概率 $p_{\mathrm{fail}}(x) = s(x) / n(x)$，使用马氏距离 $d_{M}(x, x_{j})^{2} = (x_{j} - x)^{\top} \Sigma^{-1} (x_{j} - x)$ 进行加权。这使得用户可以通过参数精细控制场景的稳定程度，甚至生成极端不稳定的场景（Figure 15），这在先前方法中完全无法实现（Appendix A.4.4）。

这一创新的决定性证据来自 Table 1：PhyScensis 的 Settle Distance 仅为 $0.003 \pm 0.008$，而 3D-Generalist 为 0.033，Architect 高达 0.405，表明 PhyScensis 的场景物理稳定度接近完美，而基线方法存在严重的物理不稳定性。

### 2. 生成框架：从单步生成到迭代闭环修正

现有方法采用单步生成范式，缺乏错误检测与纠正机制，一旦生成失败即产生不可用的结果。PhyScensis 引入了**LLM 智能体驱动的迭代闭环框架**，由三个核心模块构成（Figure 2）：

- **LLM Agent**（Section 3.2）：接收用户提示，迭代生成空间/物理谓词和资产描述，而非直接预测物体位姿。这种谓词层面的抽象使 LLM 能够专注于语义推理，将具体的空间计算交由求解器完成。
- **Solver**（Section 3.3）：由空间求解器和物理求解器组成，分别处理空间谓词（2D 位置与朝向）和物理谓词（堆叠、支撑、容器放置等 3D 交互），采用凸包碰撞检测和体素占位网格启发式搜索实现精确放置。
- **Feedback System**（Section 3.4）：检测生成失败原因，报告空区域和场景质量指标（如表面覆盖率、紧凑度、物体数量），反馈给 LLM Agent 驱动迭代优化。

消融实验（Table 2）验证了这一设计的有效性：完整的反馈系统在重试次数和时间成本上均显著优于无反馈版本（Ours w/o feedback）和无空区域报告版本（Ours w/o report），证明了闭环反馈对于提升生成效率的关键作用。

### 3. 空间与物理表示：从轴对齐包围盒到凸包与体素网格

基线方法通常使用轴对齐包围盒（AABB）进行简单的 2D 碰撞避免，无法处理复杂形状物体的精确放置。PhyScensis 引入了更精细的表示：

- **空间求解器**采用**凸包碰撞检测**，实现任意形状物体的非穿透放置（Section 3.3）。
- **物理求解器**使用**体素占位网格**进行启发式搜索，结合物理仿真验证，支持复杂堆叠和容器放置（Figure 4）。放置重叠比定义为 $\text{overlap} = \frac{\text{area}(A.\text{bottom} \cap B.\text{top})}{\text{area}(A.\text{bottom})}$，用于精确控制接触区域（Appendix A.4.2）。

### 4. 资产多样性：从固定资产库到开放词汇检索与生成

先前方法依赖固定、人工预定义的资产库，场景覆盖范围受限。PhyScensis 通过**开放词汇资产检索**配合**文本到 3D 生成管道**，显著扩大了场景的多样性和覆盖范围（Section 3.1, Appendix A.4.1），使其能够适配开放词汇的场景描述。

### 5. 关键证据总结

上述创新的有效性由以下决定性证据支撑（置信度 ≥ 0.95）：

- **场景质量**：VQA Score 达到 $0.704 \pm 0.425$，相对 3D-Generalist 提升 21.8%；GPT Ranking 降至 $1.429 \pm 0.562$，相对 3D-Generalist 降低 26.5%（Table 1）。
- **物理稳定性**：Settle Distance 接近完美（$0.003 \pm 0.008$），远优于所有基线（Table 1）。
- **机器人任务迁移**：基于 PhyScensis 生成数据训练的策略，在人类设计的未见场景中达到 9/10 的到达成功率和 3/10 的放置成功率，显著优于 Architect（3/10, 0/10）和 3D-Generalist（4/10, 1/10）（Table 1）。
- **用户研究**：在文本对齐（4.04）、自然性与物理合理性（3.98）、复杂度（3.82）三个维度上，PhyScensis 得分远高于基线（~2.5-3.0）（Table 4）。
- **消融验证**：完整反馈系统大幅降低重试次数（Table 2）；纯 LLM 预测放置（LLM-Only）导致最高的 Settle Distance，验证了物理求解器的必要性（Table 3）。

### 6. 局限性

尽管取得了显著突破，PhyScensis 仍存在以下局限：物理仿真带来较大计算开销，尤其在极端不稳定场景的生成中需要大量迭代；资产库规模和质量直接影响场景多样性，对罕见物品的检索和生成可能不够鲁棒；LLM Agent 的谓词质量受提示工程影响，可能出现语法错误或不符合物理常识的布局要求；系统目前主要针对静态场景布置，未涉及动态交互或时序任务。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_aCVfhY4Qen/figures/012_Figure_2.jpg]]
*Figure 2: Our framework consists of three components: (a) an LLM agent that takes a user prompt and generates spatial and physical predicates, along with object descriptions for retrieval; (b) a solver that computes the final scene using a physics engine for physical predicates and a sample-based constraint solver for spatial predicates; and (c) a feedback system that reports success or diagnoses failure, allowing the LLM agent to iteratively refine and regenerate predicates*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_aCVfhY4Qen/figures/014_Figure_3.jpg]]
*Figure 3: Examples of placements generated by physical solvers. Figure 4: The stacking generation pipeline uses an occupancy-grid-based heuristic to efficiently compute candidate placement locations via grid search, which are then ranked by user requirements. A physics simulator verifies physical validity (e.g., whether an object will fall), and probabilistic programming further assesses stability, enabling control over the robustness of valid states*

PhyScensis 采用**LLM 智能体 + 物理求解器 + 反馈系统**的三组件闭环架构，将场景布置问题形式化为迭代的谓词生成、求解与修正过程。系统的输入是用户提供的自然语言场景描述，输出是物理准确、高度可控的 3D 场景配置。

### 三阶段流水线

框架的运行流程分为三个核心阶段，如 Figure 2 所示：

1. **LLM Agent（谓词生成）**：接收用户提示，生成一组物体描述（用于资产检索）以及对应的**空间谓词**和**物理谓词**。空间谓词指定物体在 x-y 平面上的 2D 位置或朝向关系，物理谓词则捕捉堆叠、支撑、包含等复杂 3D 交互关系（Section 3.2）。

2. **Solver（场景求解）**：由**空间求解器**和**物理求解器**组成。空间求解器通过基于凸包的碰撞检测与参数优化，确定物体的 2D 位置和朝向；物理求解器则利用体素占位网格启发式搜索和物理引擎，解析堆叠、容器放置等物理谓词，并采用概率规划方法评估和控制场景稳定性（Section 3.3, Appendix A.4.3–A.4.4）。

3. **Feedback System（反馈修正）**：检测生成失败的原因，报告空区域和场景质量指标（包括表面覆盖率、紧凑度、物体数量等），将这些信息反馈给 LLM Agent，驱动其判断当前场景是否满意或需要进行调整和重采样，从而实现迭代优化（Section 3.4）。

### 关键设计决策

与现有基线方法的核心差异体现在两个层面：

- **物理交互保证**：基线方法（如 Architect、3D-Generalist）仅使用碰撞避免或深度估计，无法保证物理真实性。PhyScensis 集成物理引擎进行真实仿真，并通过概率规划量化与控制稳定性，使物体放置符合接触、支撑、平衡、包含等真实物理约束。

- **闭环生成框架**：基线方法通常采用单步生成，缺乏错误纠正机制。PhyScensis 通过 LLM Agent 迭代生成放置谓词，并利用语法检查、失败诊断和空间反馈实现闭环修正，显著提升了生成成功率和场景质量。

### 资产与求解器协同

为支持开放词汇的场景描述，系统采用开放词汇资产检索配合文本到 3D 生成管道，扩大了场景覆盖范围（Section 3.1, Appendix A.4.1）。空间求解器与物理求解器分工明确：前者处理 2D 平面内的位置与朝向约束，后者处理涉及 3D 空间和物理仿真的复杂交互，两者协同完成从谓词到最终场景配置的映射。

### 3.1 流水线总览

PhyScensis 框架由三个核心模块构成闭环（Figure 2）：

| 模块 | 功能 | 证据锚点 |
|------|------|----------|
| **LLM Agent** | 接收用户提示，迭代生成空间/物理谓词及资产描述 | Section 3.2 |
| **Solver** | 包含空间求解器与物理求解器，将谓词转化为3D场景配置 | Section 3.3 |
| **Feedback System** | 检测失败原因，报告空区域与场景质量指标，驱动迭代优化 | Section 3.4 |

流水线工作流：LLM Agent 生成谓词 → Solver 计算场景 → Feedback System 评估并反馈 → LLM Agent 修正谓词，形成闭环迭代。

### 3.2 LLM Agent：谓词生成

LLM Agent 的核心输出是两类谓词：

- **空间谓词（Spatial Predicates）**：指定物体在 x–y 平面内的二维位置或旋转关系。
- **物理谓词（Physical Predicates）**：捕捉三维交互，如堆叠（stacking）、支撑（supporting）或容纳（containment）。

同时，Agent 生成物体描述用于开放词汇资产检索，结合文本到3D生成管道扩大场景覆盖范围（Section 3.1, Appendix A.4.1）。

### 3.3 Solver：空间求解器与物理求解器

Solver 由两个子模块组成（Section 3.3）：

**空间求解器** 解析空间谓词，通过基于凸包的碰撞检测和参数优化，确定物体的二维位置和朝向。这避免了基线方法中仅使用轴对齐包围盒进行简单碰撞避免的局限。

**物理求解器** 处理物理谓词，借助物理引擎构建复杂的支撑和堆叠行为。其关键机制包括：

- **占位网格启发式搜索**：通过体素化场景和物体，在网格上高效搜索候选放置位置，然后由物理引擎验证（Figure 4）。
- **概率规划稳定性评估**：通过采样扰动向量评估放置的局部失败概率，实现对稳定性的精细控制。

物理求解器支持 **PLACE-ON** 谓词，其放置重叠比定义为：

$$\text{overlap} = \frac{\text{area}(A.\text{bottom} \cap B.\text{top})}{\text{area}(A.\text{bottom})}$$

该公式控制物体 A 底面与支撑物 B 顶面的接触区域占比（Appendix A.4.2）。

### 3.4 概率稳定性评估的核心公式

稳定性评估采用基于扰动的概率规划方法（Appendix A.4.4）。定义扰动向量：

$$x = \left[ \Delta p , \Delta \bar{r} , \Delta c , \Delta \mu , \Delta m \right] \in \mathbb{R}^{d}$$

其中 $d=11$，包含三维位置偏移 $\Delta p$、旋转偏移 $\Delta \bar{r}$、质心偏移 $\Delta c$、摩擦系数偏移 $\Delta \mu$ 和质量偏移 $\Delta m$。

对于查询点 $x$ 与采样点 $x_j$，计算马氏距离：

$$d_{M}(x, x_j)^{2} = (x_j - x)^{\top} \Sigma^{-1} (x_j - x)$$

其中 $\Sigma$ 为协方差矩阵。基于此计算加权局部失败概率：

$$p_{\mathrm{fail}}(x) = s(x) / n(x)$$

其中 $s(x)$ 为加权失败计数，$n(x)$ 为加权总计数。该概率量化了在给定扰动分布下放置配置的不稳定程度，使用户可通过参数精细控制场景稳定性（Figure 15 展示了不同稳定度级别的放置示例）。

### 3.5 Feedback System：闭环修正

Feedback System 在每次求解后检测失败原因，向 LLM Agent 报告空区域位置和场景质量指标（如表面覆盖率、紧凑度、物体数量）。Agent 据此判断当前场景是否满意，或需要进一步调整与重采样（Section 3.4）。消融实验（Table 2）验证了完整反馈系统在降低重试次数和时间成本上的关键作用——无反馈版本（Ours w/o feedback）和无空区域报告版本（Ours w/o report）均显著劣于完整系统。

## 实验与关键发现

### 主实验结果

PhyScensis 在场景生成的视觉质量、物理准确性和下游机器人任务上均显著优于现有基线。Table 1 报告了与 **Architect**（Wang et al., 2024b）和 **3D-Generalist**（Sun et al., 2025b）的定量对比，所有方法使用相同的 3D 资产库并统一渲染条件以确保公平性。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_aCVfhY4Qen/figures/015_Table_1.jpg]]
*Table 1: Quantitative comparison of PhyScensis with baselines*

在场景质量指标上，PhyScensis 的 **VQA Score** 达到 0.704 ± 0.425，相对 3D-Generalist（0.578）提升 21.8%，相对 Architect（0.493）提升 42.8%。**GPT Ranking** 得分为 1.429 ± 0.562（越低越好），较 3D-Generalist（1.946）降低 26.5%，较 Architect（2.607）降低 45.2%。反映物理稳定性的 **Settle Distance** 仅为 0.003 ± 0.008，接近完美稳定，而 Architect 和 3D-Generalist 分别为 0.405 和 0.033，表明基线方法生成的场景在重力作用下会发生显著物体位移。

在机器人抓取与放置任务中，使用 PhyScensis 生成数据训练的策略在人类设计的未见场景上达到 **9/10 的到达成功率**和 **3/10 的放置成功率**，远优于 Architect（3/10, 0/10）和 3D-Generalist（4/10, 1/10）。放置成功率的绝对值提升为 20-30 个百分点，验证了物理准确场景对训练鲁棒操作策略的关键作用。

用户研究（Table 4）进一步证实了 PhyScensis 的感知优势：在文本对齐（4.04 vs 2.68/2.54）、自然性与物理合理性（3.98 vs 2.65/2.72）、复杂度（3.82 vs 2.69/3.04）三个维度上，PhyScensis 的 1-5 分制评分均大幅领先基线。

与 **LayoutVLM**（Sun et al., 2025a）的补充对比（Table 5）同样显示 PhyScensis 在所有指标上保持领先，验证了物理仿真框架相对于纯视觉语言模型布局方法的优势。

### 消融实验

消融实验围绕两个核心设计展开：反馈系统的有效性，以及谓词-求解器架构相对于简化替代方案的优势。

**反馈系统消融**（Table 2）对比了完整系统（Ours）、无反馈版本（Ours w/o feedback）和无空区域报告版本（Ours w/o report）。完整反馈系统在重试次数和时间成本上均显著优于消融版本，证明失败诊断与空区域报告对提升生成效率至关重要。无反馈的 LLM 智能体缺乏错误纠正能力，导致更多迭代和无效放置。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_aCVfhY4Qen/figures/018_Table_2.jpg]]
*Table 2: Comparison with ablated versions on time-cost and retry times. Table 3: Comparison with ablated versions on scene quality*

**放置设计消融**（Table 3）将 PhyScensis 与 Random（随机放置）和 LLM-Only（纯 LLM 预测 3D 位置）进行对比。LLM-Only 由于缺乏碰撞检查和物理约束，Settle Distance 在所有方法中最高，直接验证了物理求解器的必要性。Random 放置的视觉质量和物理稳定性均远低于 PhyScensis，说明谓词驱动的结构化放置是场景质量的核心保障。

### 定性分析

Figure 5 展示了 PhyScensis 与基线在不同场景下的定性对比。Architect 生成的场景物体稀疏、缺乏物理交互；3D-Generalist 虽能放置更多物体，但出现穿透和悬浮等物理错误。PhyScensis 则能生成高密度、多层次的复杂场景，包括堆叠、支撑和容器放置等精细物理交互。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_aCVfhY4Qen/figures/017_Figure_5.jpg]]
*Figure 5: Qualitative comparison of PhyScensis with baselines for different generating scenarios*

Figure 15 展示了系统对不同稳定度级别的精确控制能力：通过调节概率规划中的稳定性参数，PhyScensis 可以生成从完全稳定到极端不稳定的放置配置，后者对训练鲁棒机器人策略具有独特价值。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_aCVfhY4Qen/figures/046_Figure_15.jpg]]
*Figure 15: Generated placements for different stability level*

### 失败模式与局限性

尽管 PhyScensis 在物理准确性上大幅领先，仍存在以下失败模式：
1. **计算开销**：物理仿真和概率规划在需要大量迭代的极端不稳定场景中耗时显著，Table 2 中完整系统的平均时间成本反映了这一瓶颈。
2. **资产覆盖**：对于罕见物品，开放词汇检索和文本到 3D 生成管道的鲁棒性不足，可能导致场景多样性受限。
3. **谓词质量**：LLM 智能体生成的谓词偶尔出现语法错误或不符合物理常识的布局要求，需依赖反馈系统进行多轮修正。
4. **静态局限**：当前框架仅处理静态场景布置，无法应对涉及物体运动和时序交互的动态任务。

## 定位与知识库关联

### 与已有方法的关系

PhyScensis 处于 3D 场景生成与物理感知布局的交叉地带。与现有工作相比，其核心差异在于**首次将物理引擎仿真与 LLM 智能体的闭环迭代框架深度耦合**，从而在无需训练数据的前提下实现了物理准确、高度复杂且强可控的场景布置。

**基于图像修复的场景生成**：**Architect**（Wang et al., 2024b）采用图像修复范式生成场景，本质上缺乏对物体间物理交互的显式建模。与其相比，PhyScensis 通过空间求解器的凸包碰撞检测和物理求解器的体素占位网格搜索，直接解决了接触、支撑、平衡、包含等物理谓词的实现问题。定量结果（Table 1）表明，Architect 的 Settle Distance 高达 0.405，而 PhyScensis 仅为 0.003，物理稳定度差距超过两个数量级。

**VLM 驱动的像素级物体放置**：**3D-Generalist**（Sun et al., 2025b）利用视觉-语言模型在 2D 像素空间进行物体放置，其物理约束仅限于深度估计和简单的碰撞避免。PhyScensis 则通过物理求解器的概率规划机制（见 Appendix A.4.4），将稳定性量化为局部失败概率 $p_{\mathrm{fail}}(x)$，并允许用户通过参数精细控制稳定度级别（Figure 15）。在 GPT Ranking 指标上，PhyScensis 相对 3D-Generalist 降低 26.5%（1.429 vs. 1.946），表明整体场景质量有质的提升。

**房间级布局生成**：**LayoutVLM**（Sun et al., 2025a）专注于房间级场景的宏观布局，其空间表示以轴对齐包围盒和 2D 碰撞避免为主。PhyScensis 的物理求解器则支持更精细的凸包碰撞检测和 3D 堆叠、容器放置等复杂交互（Figure 3, Figure 4），场景复杂度远超房间布局范畴。

**强化学习驱动的杂乱场景创建**：**ClutterGen**（Jia & Chen, 2024）通过强化学习生成杂乱场景，但其物理真实性受限于训练环境和奖励设计。PhyScensis 直接集成物理引擎进行真实仿真，避免了对训练数据的依赖，同时通过反馈系统实现了迭代修正能力。

### 适用边界

PhyScensis 的适用场景具有明确的边界条件：

1. **静态场景布置**：系统目前仅处理静态场景的物体放置，不涉及物体的动态运动、时序交互或操作序列规划。对于需要物体运动和交互的动态场景生成，框架尚无法直接适配。

2. **资产依赖**：场景多样性的上限受限于资产库的规模和质量。系统通过开放词汇检索配合文本到 3D 生成管道（Section 3.1）扩大了覆盖范围，但对于罕见物品的检索和生成仍可能不够鲁棒。

3. **计算开销**：物理仿真和概率规划带来显著的计算成本，尤其在需要大量迭代的极端不稳定场景生成中。Table 2 的消融实验表明，完整反馈系统虽然大幅降低重试次数，但单次生成的时间成本仍然不可忽视。

4. **谓词质量受提示工程影响**：LLM Agent 生成的谓词可能出现语法错误或不符合物理常识的布局要求，反馈系统可以部分缓解此问题，但无法完全消除。

### 局限与开放问题

**已知局限**：

- 物理仿真依赖带来的计算开销限制了实时或大规模场景生成的效率。
- 资产库的覆盖范围直接影响场景多样性，罕见物品的生成质量缺乏保证。
- LLM Agent 的谓词生成质量受提示工程影响，存在语法错误和物理不合理布局的风险。
- 系统仅支持静态场景，未涉及动态交互或时序任务。

**开放问题**：

1. **动态场景扩展**：能否将框架扩展至包含物体运动和交互的动态场景生成？这需要引入时序谓词和动态物理仿真，对求解器和反馈系统的设计提出更高要求。

2. **谓词生成质量提升**：如何利用强化学习或偏好数据进一步提升 LLM Agent 的谓词生成质量？当前反馈系统仅提供失败诊断，引入偏好优化可能使 Agent 主动学习更合理的布局策略。

3. **计算效率优化**：物理仿真和概率规划的计算效率是否有进一步提升的空间？更高效的采样策略（如自适应采样或主动学习）可能在不牺牲稳定性的前提下降低计算成本。

4. **极端场景的机器人训练价值**：系统生成的高度不稳定的极端场景（Figure 15），对训练鲁棒的机器人策略是否有独特价值？初步机器人实验（Table 1, Reaching 9/10, Placing 3/10）已显示正向信号，但更系统的研究仍有待开展。

5. **规模扩展**：框架是否能够适配更大规模的资产库和更复杂的场景描述？随着资产数量和场景复杂度的增长，求解器的搜索空间和物理仿真的计算需求将指数级上升，需要更高效的索引和剪枝策略。

## 原文 PDF

![[paperPDFs/ICLR_2026/PhyScensis_Physics_Augmented_LLM_Agents_for_Complex_Physical_Scene_Arrangement.pdf]]
