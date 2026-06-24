---
title: "SemGeoMo: Dynamic Contextual Human Motion Generation with Semantic and Geometric Guidance"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/SemGeoMo_Dynamic_Contextual_Human_Motion_Generation_with_Semantic_and_Geometric_Guidance.pdf
project_link: https://4dvlab.github.io/project_page/semgeomo
aliases:
- SemGeoMo
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 多层级语义与几何引导（LLM生成文本、可供性图、关节位置）与两阶段解耦架构。
primary_logic: 通过从粗到细的可供性与关节位置预测，将接触几何生成与运动生成解耦，并利用LLM自动生成细粒度文本描述，从而提升交互运动的语义合理性与几何精度。
claims:
- 在FullBodyManipulation数据集上，SemGeoMo（生成文本）相比OMOMO将HandJPE从33.18降至30.35，FID从1.98降至1.05，证明语义与几何引导大幅提升运动质量。
- 消融实验显示，移除可供性图导致FID从1.03升至2.21，移除关节位置导致FID升至3.52，移除文本引导导致FID升至1.78，证明多层级引导是性能关键。
- 在未见对象数据集HoDome上，SemGeoMo的HandJPE为44.22，远超最强基线OMOMO的86.12，证明方法具备强泛化能力。
- FullBodyManipulation 上 HandJPE↓ (cm) = 30.35 (Gen text)
---

# SemGeoMo: Dynamic Contextual Human Motion Generation with Semantic and Geometric Guidance

> [!tip] 核心洞察
> 通过从粗到细的可供性与关节位置预测，将接触几何生成与运动生成解耦，并利用LLM自动生成细粒度文本描述，从而提升交互运动的语义合理性与几何精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | SemGeoMo：融合语义与几何引导的动态上下文人体运动生成 |
| 英文题名 | SemGeoMo: Dynamic Contextual Human Motion Generation with Semantic and Geometric Guidance |
| 会议/期刊 | CVPR 2025 |
| Links |  [Project](https://4dvlab.github.io/project_page/semgeomo)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | SemGeoMo |
| Dataset | FullBodyManipulation, BEHAVE, IMHD2, HoDome |

> [!tip] 效果简介
> - FullBodyManipulation 上，HandJPE↓ (cm) 30.35 (Gen text) vs 33.18 (OMOMO) (-2.83)；FID↓ 1.05 (Gen text) vs 1.98 (OMOMO) (-0.93)。
> - BEHAVE 上，HandJPE↓ (cm) 27.91 (Gen text) vs 35.41 (MDM-PC) (-7.50)。
> - IMHD2 上，HandJPE↓ (cm) 35.43 (Gen text) vs 39.40 (OMOMO) (-3.97)。

## 概述

动态上下文下的人体运动生成（例如人-物交互）面临一个关键瓶颈：现有方法缺乏文本语义引导和细粒度的几何表征，导致生成的运动在语义连贯性和几何准确性上均存在不足。SemGeoMo 针对这一瓶颈，提出**多层级语义与几何引导**与**两阶段解耦架构**，核心思路是将接触几何生成与人体运动生成分离，并利用大语言模型（LLM）自动生成从粗到细的文本描述，从而提升交互运动的语义合理性与几何精度。

方法层面，SemGeoMo 包含三个核心模块：（1）**LLM Annotator**，从顺序点云自动生成粗到细的文本描述，提供语义引导；（2）**SemGeo 分层引导生成**，在第一阶段通过扩散模型联合生成可供性图与手部关节位置，形成分层几何引导；（3）**SemGeo 引导的运动生成**，在第二阶段利用 Motion ControlNet 与损失引导，融合语义与几何信息生成完整人体运动。

实验结果表明，SemGeoMo 在多个数据集上均取得显著提升。在 FullBodyManipulation 数据集上，SemGeoMo（使用生成文本）将 HandJPE 从 OMOMO 的 33.18 cm 降至 30.35 cm，FID 从 1.98 降至 1.05（Table 1）。在未见对象数据集 HoDome 上，HandJPE 为 44.22 cm，远超最强基线 OMOMO 的 86.12 cm（Table 4），展现了强泛化能力。消融实验进一步证实，移除可供性图、关节位置或文本引导均会导致 FID 显著上升（Table 5），验证了多层级引导的关键作用。

总体而言，SemGeoMo 通过将语义与几何信息有机融入两阶段扩散框架，在动态上下文人体运动生成任务上实现了当前最优性能，并为后续研究提供了可自动标注语义引导的新范式。

## 背景与动机

动态场景下的人体交互运动生成是计算机视觉与图形学中的核心挑战，其目标是根据交互目标（如移动的物体或人）的序列点云，合成语义合理、几何精确且自然流畅的人体运动。这一任务在虚拟现实、机器人仿真、具身智能等领域具有广泛的应用前景。

现有方法在解决该问题时面临两个关键瓶颈。**第一，语义连贯性不足。** 多数工作仅依赖原始点云或场景几何作为条件，缺乏对交互意图和动作语义的显式建模。例如，**OMOMO** 仅利用点云特征预测手部关节与运动，**CHOIS** 虽然引入了文本条件，但需要人工标注的真实文本，成本高昂且难以规模化。**第二，几何准确性受限。** 现有方法通常采用单阶段联合生成范式，直接从点云特征映射到完整人体运动，缺少对接触几何的细粒度表征。这导致生成的运动在接触区域（如手部抓取、脚部着地）容易出现穿透、滑移或悬浮等几何伪影。

上述瓶颈的深层原因在于：**语义引导的缺失**使模型难以区分外观相似但交互意图不同的场景（如“推开椅子”与“拉近椅子”）；**几何表征的粗糙**则使模型无法精准捕捉交互目标的空间可供性（affordance）——即物体表面哪些区域适合接触、以何种姿态接触。

针对上述问题，**SemGeoMo** 提出了一种融合多层级语义与几何引导的动态上下文运动生成框架。其核心洞察是：通过从粗到细的可供性与关节位置预测，将接触几何生成与运动生成解耦为两阶段流水线；同时利用大语言模型（LLM）自动生成细粒度文本描述，从而在无需人工标注的前提下，显著提升交互运动的语义合理性与几何精度。

## 核心创新

SemGeoMo 的核心创新在于将**动态上下文人体运动生成**从单一的几何条件驱动，升级为**多层级语义与几何协同引导**的范式，并通过**两阶段解耦架构**实现。相较于现有基线，其关键改进可归纳为以下四个 changed slots：

### 1. 语义引导：从无文本或人工标注到 LLM 自动生成

现有方法要么完全缺乏文本语义引导（如 OMOMO、SceneDiff），要么依赖人工标注的真实文本（如 CHOIS、MDM-PC），成本高昂且难以规模化。SemGeoMo 引入 **LLM Annotator**，直接从顺序点云自动生成粗到细的文本描述，消除了对手动标注的依赖（Section 3.2, Figure 3）。这一设计使模型能够利用细粒度语义信息约束运动的合理性与连贯性，在 FullBodyManipulation 数据集上，仅向 OMOMO 增加文本引导（OMOMO-Text）即可将 FID 从 1.98 降至 1.26（Table 9），验证了文本语义的普遍价值。

### 2. 几何引导：从单一原始点云到分层可供性与关节位置

基线方法通常仅使用原始点云特征作为几何条件（如 OMOMO、SceneDiff），缺乏对交互接触区域的显式建模。SemGeoMo 提出**分层几何引导**：第一阶段同时预测**可供性图**（affordance map）和**手部关节位置**，分别提供粗粒度接触区域和细粒度接触点信息（Section 3.3）。可供性图定义为归一化距离场：

$$\mathbf{Affordance}(n, j) = \exp\left(-\frac{1}{2}\frac{\mathbf{d}(n, j)}{\sigma^2}\right)$$

消融实验表明，移除可供性图导致 FID 从 1.03 升至 2.21，接触 F1 从 0.77 降至 0.73；移除关节位置预测则使 FID 飙升至 3.52（Table 5），证明分层几何引导是性能的关键支撑。

### 3. 架构：从单阶段联合生成到两阶段解耦

现有方法多采用单阶段架构，将接触几何与人体运动联合生成（如 OMOMO、AffordMotion），导致两个子任务相互干扰。SemGeoMo 采用**两阶段解耦框架**（Figure 2）：
- **第一阶段（SemGeo Hierarchical Guidance Generation）**：以文本和顺序点云为条件，通过双分支扩散模型联合生成可供性图与手部关节位置，捕获二者的相互影响。
- **第二阶段（SemGeo-guided Motion Generation）**：利用 Motion ControlNet 和损失引导，基于第一阶段输出的几何引导与文本语义，生成完整人体运动。

这种解耦设计使接触几何预测与运动生成各司其职，在 FullBodyManipulation 上将 HandJPE 从 OMOMO 的 33.18 降至 30.35，FID 从 1.98 降至 1.05（Table 1）。

### 4. 条件融合：从简单拼接/注意力到交叉注意力融合

在融合关节特征与可供性特征时，SemGeoMo 采用**交叉注意力机制**（mutual cross-attention），以关节特征作为查询，可供性特征作为键和值：

$$F_{fusion} = \mathrm{CrossAttention}(MLP(\mathbf{J}_{h}^{\prime})_{q}, F_{k}, F_{v})$$

相比简单的拼接或单向注意力，这种设计更有效地建模了细粒度关节位置与粗粒度可供性区域之间的空间对应关系（Section 3.4, Equation 5）。配合关节引导损失 $L_{\mathrm{joint}}$ 和脚部稳定性损失 $L_{\mathrm{foot}}$，进一步提升了接触精度与运动物理合理性（Table 6）。

## 整体框架

SemGeoMo 的目标是仅以交互目标物体的 4D 顺序点云为条件，生成符合语义且几何精确的响应式人体交互运动。为达成这一目标，该工作提出了一个两阶段解耦框架，将接触几何的预测与人体运动生成分离，并引入大语言模型自动标注器提供语义引导。整体流水线如 **Figure 2** 所示，由三个核心模块串联构成：LLM Annotator、SemGeo Hierarchical Guidance Generation 和 SemGeo‑guided Motion Generation。

![[assets/figures/papers/paper_list_l1748_SemGeoMo_Dynamic_Contextual_Human_Motion_Generation_with_Semantic_and_Ge/figures/002_Figure_2.jpg]]
*Figure 2: The pipeline of our two-stage framework. LLM Annotator provides the semantic guidance. SemGeo Hierarchical Guidance Generation takes textual information and sequential point cloud as condition and generate affordance-level and joint-level guidance. Then SemGeo-guided Motion Generation utlizes semantic and geometric information to generate responsive human motion*

### 输入与数据表示

系统输入为时变的交互目标物体点云序列，即 4D 顺序点云。在进入生成流水线之前，原始数据被组织为三种表示形式：
- **顺序点云特征**：从原始点云中提取的时空几何特征。
- **可供性图（Affordance Map）**：编码目标物体表面点与人体骨架关节之间空间关系的归一化距离图，定义为：
  $$
  \mathbf{Affordance}(n, j) = \exp\left(-\frac{1}{2}\frac{\mathbf{d}(n, j)}{\sigma^2}\right)
  $$
  其中 $\mathbf{d}(n, j)$ 为目标点 $n$ 与骨架关节 $j$ 之间的距离。
- **手部关节位置**：作为细粒度几何引导信号，用于后续运动生成阶段的损失约束。

### 模块关系与数据流

整个框架的数据流遵循“语义引导先行、几何引导分层、运动生成在后”的设计逻辑：

1. **LLM Annotator（语义引导生成）**  
   该模块以顺序点云为输入，通过精心设计的提示词与微调策略，自动生成从粗到细的文本描述（**Figure 3**）。粗描述推断交互的宏观语义（如“人正在搬运箱子”），细描述则融合关节位置和几何特征，生成更精确的交互细节（如“双手托住箱子底部”）。这些文本描述作为语义条件，注入后续两个阶段。

2. **SemGeo Hierarchical Guidance Generation（第一阶段：分层几何引导生成）**  
   该阶段是一个条件扩散模型，接收文本描述和顺序点云作为联合条件，同时生成两个层次的几何引导信息：
   - **可供性图**：提供粗粒度的接触区域概率分布。
   - **手部关节位置**：提供细粒度的接触关节坐标。  
   模型采用双分支 Transformer 架构，在去噪过程中捕捉可供性与关节位置之间的相互影响，实现从粗到细的接触几何预测。

3. **SemGeo‑guided Motion Generation（第二阶段：运动生成）**  
   以第一阶段生成的可供性图和关节位置作为几何引导，结合 LLM 提供的文本语义引导，通过 Motion ControlNet 生成完整的人体运动序列。该阶段引入两类损失函数进行引导：
   - **关节引导损失 $L_{\mathrm{joint}}$**：对接触关节的预测位置与目标位置施加掩码 L2 损失，掩码基于距离阈值 $\tau$ 定义。
   - **脚部稳定性损失 $L_{\mathrm{foot}}$**：惩罚脚部高度偏离地面、速度突变和加速度异常，确保运动物理合理性。

   在条件融合层面，该阶段采用交叉注意力机制，将关节特征作为查询向量，与可供性特征进行交互融合，使几何引导信息有效渗透到运动生成过程中。

### 关键设计决策

- **两阶段解耦**：将接触几何生成与运动生成分离，避免单阶段联合建模中语义与几何信号相互干扰的问题。消融实验证实，移除可供性图模块导致 FID 从 1.03 升至 2.21，移除关节位置预测导致 FID 升至 3.52，证明分层几何引导对运动质量至关重要（**Table 5**）。
- **LLM 自动化文本标注**：消除了对手动文本标注的依赖，使方法可规模化应用。在 FullBodyManipulation 数据集上，使用生成文本的 SemGeoMo 相比仅依赖几何条件的 OMOMO，FID 从 1.98 降至 1.05（**Table 1**）。
- **多层级几何引导**：同时提供可供性图和关节位置，形成粗到细的几何约束链，显著提升接触精度与运动自然度。

## 核心模块与公式推导

### 数据表征：可供性图

SemGeoMo 的核心几何表征之一是**可供性图（Affordance Map）**，它将交互目标点云与人体骨架关节之间的空间关系编码为归一化距离图。给定目标点云中的点 $n$ 和骨架关节 $j$，可供性图定义为：

$$\mathbf{Affordance}(n, j) = \exp\left(-\frac{1}{2}\frac{\mathbf{d}(n, j)}{\sigma^2}\right)$$

其中 $\mathbf{d}(n, j)$ 表示点 $n$ 与关节 $j$ 之间的欧氏距离，$\sigma$ 为控制距离敏感度的超参数。该公式将空间邻近性映射为 $(0, 1]$ 区间的激活值，距离越近激活越强，从而为后续的接触几何预测提供细粒度的空间先验。

### 第一阶段：条件扩散模型与双分支生成

SemGeo 层级引导生成阶段采用**条件扩散模型**，其核心是学习从高斯噪声逐步恢复干净信号的反向过程。反向扩散过程建模为：

$$p_{\theta}\left(x^{t-1} \mid x^{t}, c\right) := \mathcal{N}\left(x^{t-1}; \mu_{\theta}\left(x^{t}, t, c\right), \sigma_{t}^{2} I\right)$$

其中 $x^t$ 为第 $t$ 步的噪声信号，$c$ 为条件信息（文本嵌入与顺序点云特征），$\mu_\theta$ 为可学习的去噪网络。训练时，模型通过最小化预测信号 $\hat{x}_\theta$ 与真实信号 $x^0$ 之间的 L1 距离来优化：

$$\mathcal{L} = \mathbb{E}_{\pmb{x}^{0}, t} \left\| \hat{x}_{\theta}\left(\boldsymbol{x}^{t}, t, \boldsymbol{c}\right) - x^{0} \right\|_{1}$$

该阶段采用**双分支 Transformer 架构**，同时生成可供性图和手部关节位置，并通过分支间的交叉注意力捕获从粗到细的相互影响。

### 时序特征提取与交叉注意力融合

在第二阶段，模型需要将第一阶段生成的几何引导（可供性图与关节位置）与原始点云特征融合。首先进行时序特征提取：

$$F = \mathrm{TemporalTransformer}(MLP(F_{pc} \oplus \mathbf{A}^{\prime}))$$

其中 $F_{pc}$ 为点云特征，$\mathbf{A}^{\prime}$ 为生成的可供性图，$\oplus$ 表示拼接操作，经 MLP 和时序 Transformer 后得到潜在特征 $F$。

随后，通过**互交叉注意力**融合关节特征与可供性特征：

$$F_{fusion} = \mathrm{CrossAttention}(MLP(\mathbf{J}_{h}^{\prime})_{q}, F_{k}, F_{v})$$

其中 $\mathbf{J}_{h}^{\prime}$ 为第一阶段生成的手部关节位置，作为 Query；$F$ 同时作为 Key 和 Value。该机制使运动生成网络能够显式关注接触区域的几何信息。

### 损失引导：关节接触与足部稳定性

第二阶段在推理时采用两类物理合理性损失进行引导优化：

**关节引导损失**对接触关节施加掩码 L2 约束：

$$L_{\mathrm{joint}} = \frac{1}{J} \sum_{i=1}^{L} |\mathbf{J}_{\mathrm{pred}_i} - \mathbf{J}_{\mathrm{h}_i}^{\prime}|_{2} \cdot \mathbf{Mask}_{i}$$

其中 $\mathbf{Mask}_i$ 根据预测关节与目标点云的距离阈值 $\tau$ 定义，仅对判定为接触的关节施加损失，$J$ 为接触关节数，$L$ 为序列长度。

**足部稳定性损失**惩罚脚部离地高度、速度及加速度异常：

$$L_{\mathrm{foot}} = \frac{1}{L} \sum_{i=1}^{L} \left( (y_i - h_g)^2 + \alpha \mathbf{M}_c(v_i^2) + \beta \mathbf{M}_c(a_i^2) \right)$$

其中 $y_i$ 为脚部高度，$h_g$ 为地面高度，$v_i$ 和 $a_i$ 分别为脚部速度和加速度，$\mathbf{M}_c$ 为接触掩码，$\alpha$ 和 $\beta$ 为平衡系数。该损失确保脚部在接触地面时保持稳定，避免滑动或漂浮伪影。

### 补充图表

![[assets/figures/papers/paper_list_l1748_SemGeoMo_Dynamic_Contextual_Human_Motion_Generation_with_Semantic_and_Ge/figures/003_Figure_3.jpg]]
*Figure 3: LLM Annotator pipeline. It first takes a sequential point cloud to infer a coarse text description. Then uses joint positions, the coarse text, and geometric features to generate a fine-grained sentence with a designed prompt*

## 实验与分析

### 主实验结果

SemGeoMo在四个基准数据集上均取得最优性能，涵盖分布内与分布外场景。在FullBodyManipulation数据集上（Table 1），SemGeoMo使用LLM生成的文本（Gen text）将HandJPE从OMOMO的33.18降至30.35，FID从1.98降至1.05；使用真实文本（GT text）时，HandJPE进一步降至27.84，MPJPE降至16.62，接触F1达0.77。这验证了语义与几何引导对运动质量的双重提升。

![[assets/figures/papers/paper_list_l1748_SemGeoMo_Dynamic_Contextual_Human_Motion_Generation_with_Semantic_and_Ge/figures/005_Table_1.jpg]]
*Table 1: Human motion generation result on FullBodyManipulation*

在BEHAVE数据集上（Table 2），SemGeoMo的HandJPE为27.91，相比MDM-PC的35.41降低7.50。在IMHD2数据集上（Table 3），HandJPE为35.43，优于OMOMO的39.40。在未见对象数据集HoDome上（Table 4），SemGeoMo的HandJPE为44.22，远超最强基线OMOMO的86.12和CHOIS的76.74，降幅达32.52–42.52，证明了方法在分布外场景下的强泛化能力。

![[assets/figures/papers/paper_list_l1748_SemGeoMo_Dynamic_Contextual_Human_Motion_Generation_with_Semantic_and_Ge/figures/008_Table_4.jpg]]
*Table 4: Human motion generation result on HoDome*

![[assets/figures/papers/paper_list_l1748_SemGeoMo_Dynamic_Contextual_Human_Motion_Generation_with_Semantic_and_Ge/figures/006_Table_2.jpg]]
*Table 2: Human motion generation result on Behave*

![[assets/figures/papers/paper_list_l1748_SemGeoMo_Dynamic_Contextual_Human_Motion_Generation_with_Semantic_and_Ge/figures/007_Table_3.jpg]]
*Table 3: Human motion generation result on IMHD2*

定性结果（Figure 4）显示，基线方法常出现粉色圈标注的接触不良区域和绿色圈标注的扭曲运动，而SemGeoMo生成的交互运动在接触精度和运动自然度上均显著更优。

![[assets/figures/papers/paper_list_l1748_SemGeoMo_Dynamic_Contextual_Human_Motion_Generation_with_Semantic_and_Ge/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative results on the FullBodyManipulation dataset. We circle areas of low contact performance in pink and instances of contorted motion in green*

### 消融实验

消融实验（Table 5）揭示了多层级引导各自的关键作用。移除可供性图模块导致FID从1.03升至2.21，接触F1从0.77降至0.73；移除关节位置预测导致FID升至3.52；移除文本引导导致FID升至1.78，R-score从0.66降至0.58。三者同时移除时性能最差，证明语义与几何引导缺一不可。

![[assets/figures/papers/paper_list_l1748_SemGeoMo_Dynamic_Contextual_Human_Motion_Generation_with_Semantic_and_Ge/figures/009_Table_5.jpg]]
*Table 5: Ablation studies on the impact of semantic and geometric information with our model design*

损失引导消融（Table 6）表明，仅用关节损失时FID为1.15，仅用脚部稳定性损失时FID为0.93，两者联合使用时FID达最优1.03，验证了接触关节约束与脚部物理合理性约束的互补性。

![[assets/figures/papers/paper_list_l1748_SemGeoMo_Dynamic_Contextual_Human_Motion_Generation_with_Semantic_and_Ge/figures/010_Table_6.jpg]]
*Table 6: Ablation study on guidance loss*

跨基线消融（Table 9）显示，在OMOMO基础上增加文本引导（OMOMO-Text）使FID从1.98降至1.26，表明文本语义信息对不同架构具有普适增益。

![[assets/figures/papers/paper_list_l1748_SemGeoMo_Dynamic_Contextual_Human_Motion_Generation_with_Semantic_and_Ge/figures/015_Table_9.jpg]]
*Table 9: Ablation study on different baselines*

### 文本生成与用户研究

LLM Annotator生成的文本质量评估（Table 7）表明，生成文本与真实文本在语义相似度上表现良好。用户研究（Table 8）进一步确认，人类评估者在运动自然度、语义连贯性和接触合理性三个维度上均显著偏好SemGeoMo的生成结果。

![[assets/figures/papers/paper_list_l1748_SemGeoMo_Dynamic_Contextual_Human_Motion_Generation_with_Semantic_and_Ge/figures/014_Table_8.jpg]]
*Table 8: User study for human motion generation result on Full-BodyManipulation*

![[assets/figures/papers/paper_list_l1748_SemGeoMo_Dynamic_Contextual_Human_Motion_Generation_with_Semantic_and_Ge/figures/013_Table_7.jpg]]
*Table 7: Text generation result on FullBodyManipulation*

### 失败模式与局限性

尽管整体性能优越，分析揭示了若干失败模式。在极端物体形状（如非常规几何体）或高度动态的人人交互场景下，接触预测精度可能下降，表现为手部穿透或悬空。LLM生成的文本描述偶尔与细粒度交互动作不完全对齐，导致语义引导偏差。此外，两阶段架构和交叉注意力模块的计算开销尚未量化评估，其实时适用性有待验证。

## 方法谱系与知识库定位

### 1. 与基线方法的关系与增量贡献

SemGeoMo 的核心贡献在于将**多层级语义与几何引导**引入动态上下文人体运动生成，并通过**两阶段解耦架构**实现接触几何预测与运动生成的分离。相较于现有基线，其增量体现在以下四个维度：

**（1）语义引导的自动化与细粒度化。** 现有方法如 **CHOIS** 和 **MDM-PC** 虽支持文本条件，但依赖人工标注的真实文本（GT text），成本高昂且难以规模化。**OMOMO** 和 **AffordMotion** 则完全放弃文本引导，仅依赖点云或可供性图，导致语义连贯性不足。SemGeoMo 引入 **LLM Annotator**，利用大语言模型从顺序点云自动生成粗到细的文本描述（Figure 3），在无需人工标注的条件下，使 FID 从 OMOMO 的 1.98 降至 1.05（Table 1）。这一设计将文本引导从“昂贵的外部监督”转化为“可自动获取的内部条件”，显著降低了语义引导的获取门槛。

**（2）几何引导的层次化与精细化。** **SceneDiff** 和 **OMOMO** 仅使用原始点云特征作为几何条件，缺乏对接触区域的显式建模。SemGeoMo 提出 **SemGeo Hierarchical Guidance Generation**，在第一阶段联合生成可供性图（affordance map）和手部关节位置，形成从粗到细的几何引导。可供性图编码目标点与骨架关节的空间关系（Equation 1），关节位置则提供精确的接触锚点。消融实验（Table 5）表明，移除可供性图使 FID 从 1.03 升至 2.21，移除关节位置使 FID 升至 3.52，验证了层次化几何引导的必要性。

**（3）两阶段解耦架构。** 现有方法多为单阶段联合生成，如 **OMOMO** 直接从点云预测运动，**CHOIS** 在单一扩散过程中融合文本与场景条件。SemGeoMo 将接触几何生成与运动生成解耦：第一阶段扩散模型预测可供性图和关节位置，第二阶段 **Motion ControlNet** 以此为条件生成完整人体运动（Figure 2）。这种解耦使模型能分别优化接触精度与运动质量，在 FullBodyManipulation 上将 HandJPE 从 OMOMO 的 33.18 降至 30.35（Table 1）。

**（4）条件融合机制。** 相较于简单拼接或单向注意力，SemGeoMo 在第二阶段采用**交叉注意力融合**（Equation 5），以关节特征为询问（query）、可供性特征为键值（key-value），实现语义与几何信息的双向交互。这一设计使模型能动态权衡不同模态的贡献，在复杂交互场景中保持几何准确性与语义合理性。

### 2. 适用边界与能力范围

**适用场景：**
- **动态上下文人-物交互运动生成**：给定顺序点云序列，生成与之交互的完整人体运动。在 FullBodyManipulation、BEHAVE、IMHD2 三个数据集上均取得最优性能（Table 1-3）。
- **未见对象的泛化**：在 HoDome 数据集上，SemGeoMo 的 HandJPE 为 44.22，远超最强基线 OMOMO 的 86.12（Table 4），证明方法对未见物体形状具备强泛化能力。
- **人人交互扩展**：Figure 8 展示了方法在人人交互场景下的定性结果，表明框架可扩展至更广泛的交互类型。
- **文本-运动对齐**：LLM Annotator 生成的细粒度文本与生成运动高度对齐（Figure 9），使方法适用于需要语义描述的下游任务。

**能力限制：**
- **极端物体形状与高度动态场景**：论文未在极端非刚性物体或剧烈形变场景下进行系统评估，泛化性能可能有限。
- **计算开销未量化**：从粗到细接触预测和交叉注意力模块的计算成本未报告，实时性存疑。
- **LLM 生成文本的可靠性**：LLM 生成的文本描述偶尔可能不准确，影响语义引导质量（Table 7 展示了文本生成质量，但未量化错误率）。
- **单目标交互假设**：当前框架假设交互目标为单一对象，多对象协同交互场景未覆盖。

### 3. 局限与开放问题

**已识别局限：**
1. **计算效率未验证**：论文未讨论模型参数量、推理延迟或训练成本，两阶段扩散框架和 LLM Annotator 的实际部署可行性需进一步验证。
2. **LLM 文本质量依赖**：语义引导的质量高度依赖 LLM 的生成能力，在复杂交互语义下可能出现描述偏差，进而影响运动生成质量。
3. **极端场景泛化未充分测试**：HoDome 实验虽展示了跨数据集泛化能力，但物体形状和运动模式的多样性仍有限，更极端的场景（如柔性物体、快速动态交互）未覆盖。
4. **损失函数调参敏感**：Table 6 显示仅用关节损失时 FID 为 1.15，仅用脚部损失时 FID 为 0.93，同时使用两者达最优 1.03，表明损失权重需精细调参。

**开放问题：**
1. **如何提升 LLM 生成文本的准确性与细粒度？** 当前 LLM Annotator 依赖精心设计的提示词和微调，但文本质量仍可能波动。能否引入视觉-语言对齐的反馈机制，使文本生成与视觉观察相互校验？
2. **两阶段框架能否合并为端到端训练？** 当前解耦设计虽提升了可控性，但可能损失端到端优化的潜力。联合训练第一阶段接触预测与第二阶段运动生成是否能进一步提升性能？
3. **如何扩展到多对象与长时序交互？** 当前框架假设单目标交互，多对象场景（如搬运多个物体）需要更复杂的注意力机制和接触建模。长时序交互（分钟级）则对扩散模型的生成效率提出挑战。
4. **几何引导能否从关节级扩展到表面级？** 当前关节位置预测提供了稀疏接触锚点，若能预测手部/身体表面的密集接触点，有望进一步提升接触精度与物理合理性。

## 原文 PDF

![[paperPDFs/CVPR_2025/SemGeoMo_Dynamic_Contextual_Human_Motion_Generation_with_Semantic_and_Geometric_Guidance.pdf]]