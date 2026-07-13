---
title: "ArtLLM: Generating Articulated Assets via 3D LLM"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ArtLLM_Generating_Articulated_Assets_via_3D_LLM.pdf
project_link: "https://authoritywang.github.io/artllm"
code_link: "https://github.com/hiyouga/LLaMA-Factory"
aliases:
- ArtLLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将铰接结构预测转化为语言建模问题，对连续参数进行离散量化，使3D大语言模型能够自回归地同时预测可变数量的零件布局和关节，从而统一了几何与运动结构的推理。
primary_logic: 通过将零件轴对齐包围盒和关节参数表示为离散token序列，并利用大规模铰接数据集进行多任务多阶段监督微调，3D LLM能够学习强大的零件几何先验和运动学关系，克服了传统方法中连续值回归不稳定的问题。
claims:
- ArtLLM在PartNet-Mobility数据集上显著超越现有方法：mIoU达0.6884（次优方法Singapo*仅0.4705），关节类型准确率90.84%，图准确率77.41%，且推理速度(19s)远快于基线。
- 消融实验验证，连续值直接预测导致性能大幅下降，去除多任务设置恶化所有指标，去除数据增强降低零件IoU，去除多阶段训练损害零件和关节预测准确率。
- 物理约束限位校正能有效消除自碰撞，使铰接运动平稳无碰撞，提升了仿真物理合理性。
- PartNet-Mobility 7 categories (SINGAPO split) 上 mIoU = 0.6884
---

# ArtLLM: Generating Articulated Assets via 3D LLM

> [!tip] 核心洞察
> 通过将零件轴对齐包围盒和关节参数表示为离散token序列，并利用大规模铰接数据集进行多任务多阶段监督微调，3D LLM能够学习强大的零件几何先验和运动学关系，克服了传统方法中连续值回归不稳定的问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | ArtLLM：利用3D大语言模型生成铰接资产 |
| 英文题名 | ArtLLM: Generating Articulated Assets via 3D LLM |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.01142) · [Project](https://authoritywang.github.io/artllm) · [Code](https://github.com/hiyouga/LLaMA-Factory) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ArtLLM |
| Dataset | PartNet-Mobility 7 categories |

> [!tip] 效果简介
> - PartNet-Mobility 7 categories (SINGAPO split) 上，mIoU 0.6884 vs Singapo* (0.4705) (+0.2179)。
> - PartNet-Mobility 7 categories 上，Type Acc 0.9084 vs Singapo* (0.9065) (+0.0019)；Graph Acc 0.7741 vs Singapo* (0.6851) (+0.0890)；Joint-Axis-Err 0.1271 vs Singapo* (0.2463) (-0.1192)。

## 概要

现有铰接物体生成方法面临两大根本瓶颈：优化重建范式需要逐物体缓慢拟合关节参数，且通常局限于简单单关节结构；检索式方法则从固定零件库中组装，导致几何重复、泛化能力差，且几何与运动结构之间缺乏统一推理。针对这些限制，**ArtLLM** 提出将铰接结构预测转化为语言建模问题——通过对连续参数进行离散量化，使3D大语言模型能够自回归地同时预测可变数量的零件布局与关节，从而统一了几何与运动结构的推理过程。

核心思路是将零件轴对齐包围盒和关节参数表示为离散token序列，并利用大规模铰接数据集进行多任务多阶段监督微调，使3D LLM学习强大的零件几何先验与运动学关系，克服传统连续值回归不稳定的问题。在PartNet-Mobility数据集上，ArtLLM的mIoU达到0.6884（次优方法Singapo*仅0.4705），关节类型准确率90.84%，图准确率77.41%，且推理速度（19s）远快于基线方法（84s）。消融实验进一步验证了离散量化、多任务设置、数据增强及多阶段训练等关键设计的必要性。物理约束限位校正模块能有效消除自碰撞，使铰接运动平稳无碰撞，提升了仿真物理合理性。



三维铰接物体的自动生成是计算机图形学、具身智能和机器人仿真的核心需求。从日常家具（抽屉、门、剪刀）到复杂机械装置，铰接物体的功能行为由零件的几何形状与运动学结构共同决定——不仅需要精确的零件外形，还需要正确的关节类型、轴方向和运动范围。然而，传统生成方法长期受限于两大范式：

**优化重建方法**通过对输入点云或图像进行逐物体的关节拟合来恢复铰接结构。这类方法通常需要缓慢的迭代优化过程，且受限于预设的运动学模板，难以处理具有可变数量零件和关节的复杂多关节物体。**检索式方法**则从固定的零件库中检索并组装已知零件，例如 **URDFormer** 基于固定模板预测外框与内部零件（仅限5个类别），**SINGAPO** 从预定义零件库检索并预测布局和关节，**Articulate-Anything** 则依赖 GPT-4o 进行检索式组装。这类方法虽然推理速度较快，但零件库的封闭性导致几何重复严重，泛化能力差，且无法对未见过的物体类别生成合理的铰接结构。

更深层的问题在于，上述方法均缺乏对几何与运动结构的统一推理。优化方法将零件形状与关节参数解耦处理，检索方法则完全割裂了几何生成与运动学预测——零件来自固定库，关节参数独立回归。这种分离使得模型无法学习零件间的空间关系和运动学约束，导致生成的铰接结构在物理上不一致：零件碰撞、关节轴错位、运动范围不合理等问题频繁出现。

近年来，大语言模型（LLM）在统一多模态推理方面展现出强大能力，3D LLM 的出现为三维理解与生成开辟了新路径。然而，将铰接结构预测——涉及可变数量的连续参数（包围盒坐标、关节轴方向、运动范围）——转化为语言建模问题面临根本挑战：连续值的直接回归在自回归框架下极不稳定，而简单的离散化又会引入量化误差。

ArtLLM 正是在这一背景下提出，其核心动机是通过将铰接结构预测重新定义为离散 token 序列的自回归生成问题，使 3D LLM 能够统一推理零件的几何布局与运动学关系。这一范式转变的关键在于：对连续参数进行精心设计的离散量化，并利用大规模铰接数据集进行多任务多阶段监督微调，从而让语言模型学习强大的零件几何先验和运动学约束。结合物理驱动的关节限位校正，ArtLLM 旨在实现从单张图像或文本快速生成物理合理、仿真就绪的铰接资产。



## 核心方法与创新机理

ArtLLM 的核心创新在于将铰接结构预测从传统的优化重建或检索组装范式，根本性地转化为**3D大语言模型的自回归语言建模问题**。这一范式转换通过以下关键设计实现，直接回应了现有方法的瓶颈。

### 1. 离散量化的统一表示

现有方法（如 SINGAPO 等检索式方法）从固定零件库中检索组装，导致几何重复且泛化能力差；而优化重建方法则需缓慢的逐物体关节拟合。ArtLLM 将连续几何与运动学参数全部转化为离散 token 序列（Sec. 3.1）：零件轴对齐包围盒坐标归一化后量化为 128 bins，关节方向采用分层方向码本，位置和限位分别量化为 48/64 bins。这一设计使得 3D LLM 能够自回归地同时预测可变数量的零件布局和关节参数，从而**统一了几何与运动结构的推理**，克服了传统连续值回归不稳定的问题。消融实验（Table 3, Experiment A）证实，直接预测连续值将显著降低坐标和方向相关属性的预测能力。

### 2. 多任务多阶段监督微调

传统方法通常采用单阶段端到端训练，缺乏对几何先验的充分挖掘。ArtLLM 提出**渐进式两阶段训练策略**（Sec. 3.1）：第一阶段仅在零件布局预测任务上训练，建立鲁棒的几何基础；第二阶段初始化点编码器后，在全部三个任务（零件布局、关节参数、层次结构）上进行监督微调。消融实验（Table 3, Experiment D）表明，去除多阶段训练直接使用 P3SAM 初始化点编码器进行完整训练，会损害零件和关节预测精度；而 Experiment B 证实，去除多任务设置将恶化除轴方向外的所有指标。

### 3. 物理驱动的关节限位校正

现有方法通常缺乏对关节运动物理合理性的显式建模。ArtLLM 引入**基于碰撞检测的限位校正模块**（Sec. 3.4），通过层次搜索定位导数尖峰来确定初始接触角，从而有效消除自碰撞。Figure 5 的定性结果表明，校正前预测的关节范围在铰接运动过程中会导致明显的自碰撞，而校正后零件运动平滑无碰撞，显著提升了仿真物理合理性。

### 4. 从检索到生成：条件式零件几何合成

不同于从固定零件库检索的基线方法（如 SINGAPO、URDFormer、Articulate-Anything），ArtLLM 将 LLM 预测的包围盒蓝图作为条件，驱动**零件感知生成模型 XPart**（Sec. 3.3）合成高保真零件几何。这一设计从根本上摆脱了对预定义零件库的依赖，实现了几何的多样性和输入一致性。Figure 4 的定性对比显示，检索式方法因零件库限制常无法恢复准确几何，而 ArtLLM 生成的几何与输入点云高度匹配。

这些创新共同构成了从“检索组装”到“语言建模+条件生成”的范式跃迁，使得 ArtLLM 在 PartNet-Mobility 数据集上以 mIoU 0.6884 显著超越次优方法（SINGAPO 0.4705），同时将推理时间从 84s 压缩至 19s（Table 2）。



ArtLLM 的整体流水线由三个核心阶段构成，形成“结构推理→几何合成→物理校正”的闭环。给定单张图像或多视角重建的点云，系统首先通过 3D 大语言模型自回归地预测铰接蓝图，然后利用该蓝图条件化零件感知生成模型以合成高保真零件几何，最后通过物理驱动的关节限位校正消除自碰撞，输出仿真就绪的铰接资产（图 2）。

**输入与编码**：输入点云经 **Point Transformer v3**（PTv3）编码为几何特征，随后通过一个 **2 层 MLP 投影器** 映射到 LLM 的嵌入空间，实现 3D 几何与语言的桥接。

**核心推理**：投影后的特征被送入基于 **Qwen3 0.6B** 的语言模型，该模型自回归地生成离散 token 序列，同时预测可变数量的零件轴对齐包围盒与关节参数。关键在于，所有连续几何与运动学参数均通过离散量化转换为 token 表示——包围盒坐标归一化至 $[-1,1]$ 后量化为 128 个 bin，关节方向采用分层方向码本，从而将不稳定的连续值回归转化为标准的语言建模问题。

**几何合成**：预测的铰接蓝图随后条件化 **XPart** 零件感知生成模型，该模型根据每个零件的包围盒约束合成高保真零件几何，而非从固定零件库检索，避免了检索式方法的几何重复问题。

**物理校正**：最后，**物理驱动的关节限位校正模块** 通过碰撞检测算法定位初始接触角，对预测的关节运动范围进行精细化调整，确保铰接运动平稳无自碰撞，使生成的资产可直接用于仿真环境。

整个框架通过多任务多阶段监督微调进行训练：第一阶段仅训练零件布局预测任务以建立鲁棒的几何基础，第二阶段对所有三个任务（零件布局、关节参数、图结构）进行联合监督微调。点云编码器使用在 P3SAM 大规模零件分割任务上预训练的权重进行初始化，进一步增强几何理解能力。

### 补充图表

![[assets/figures/papers/paper_list_l2371_https_arxiv_org_abs_2603_01142/figures/002_Figure_2.jpg]]
*Figure 2: Architecture Overview. Given an input point cloud, ArtLLM first predicts a tokenized articulation blueprint that specifies part layouts and kinematic structures. This blueprint then conditions a part-aware generative model to synthesize high-fidelity link geometries, followed by a physics-based joint-limit correction module refines the articulation, producing simulation-ready articulated assets*

![[assets/figures/papers/paper_list_l2371_https_arxiv_org_abs_2603_01142/figures/001_Figure_1.jpg]]
*Figure 1: We propose ArtLLM, a novel framework capable of rapidly generating articulation assets from images or text. By using a 3D LLM to jointly predict part layouts and joints, and integrating state-of-the-art part generation methods, our approach can produce high-quality, physically grounded articulation assets*



ArtLLM 的核心架构由五个模块串联构成，其关键创新在于将铰接结构预测转化为语言建模问题，并对连续参数进行离散量化。

**点云编码器 (Point Cloud Encoder)** 采用 Point Transformer v3，负责从输入点云中提取几何特征。该编码器使用在大规模零件分割任务上预训练的 P3SAM 权重初始化，从而为后续的零件布局预测提供强几何先验。编码器输出的点云特征随后通过一个 **编码器-投影器 (Encoder-Projector)**，即一个 2 层 MLP，投影到语言模型的嵌入空间。

**语言模型 (Language Model)** 基于 Qwen3 0.6B，是整个框架的推理核心。它以自回归方式生成一个“铰接蓝图”的 token 序列，该序列同时编码了可变数量的零件布局和关节结构。这一设计的关键在于将所有连续几何与运动学参数离散化为 token 表示：

- **零件包围盒参数化**：每个零件由其轴对齐包围盒定义：
  $$\mathbf{bbox}\_id = \mathbf{BBox}(x_{min}, y_{min}, z_{min}, x_{max}, y_{max}, z_{max})$$
  包围盒坐标归一化到 $[-1,1]$ 后，按以下方式量化为 128 个离散 bin：
  $$\hat{c}_{\min} = \lfloor \frac{(c_{\min} + 1)}{2} \times 128 \rfloor, \quad \hat{c}_{\max} = \lceil \frac{(c_{\max} + 1)}{2} \times 128 \rceil$$

- **旋转关节定义**：每个旋转关节由父/子零件 ID、转轴方向、原点位置和运动范围定义：
  $$\mathrm{joint.}id = Revolute\mathrm{Joint}(parent, child, dir, pos, limit)$$
  关节参数同样通过离散量化处理，其中方向向量使用分层方向码本进行 token 化。

这种离散化策略是本工作的核心因果调控点：它避免了传统方法中直接回归连续浮点数的不稳定性，使 LLM 能够稳定地同时推理几何布局与运动学关系。

**零件感知生成模型 (Part-Aware Generative Model)** XPart 接收语言模型预测的包围盒作为条件，合成每个零件的高保真几何。该模块将抽象的布局 token 转化为具体的 3D 网格，使最终资产既符合预测的空间位置，又具备细节丰富的几何形态。

**关节限位校正模块 (Joint-Limit Correction Module)** 是后处理环节，针对生成几何后可能出现的自碰撞问题进行物理驱动的优化。其核心机制是通过碰撞检测计算零件间距离的导数尖峰，从而精确定位初始接触角，并将关节运动范围截断至该安全区间。这一过程无需额外训练，直接提升了铰接运动在仿真环境中的物理合理性。

### 补充图表

![[assets/figures/papers/paper_list_l2371_https_arxiv_org_abs_2603_01142/figures/003_Figure_3.jpg]]
*Figure 3: Physical limit calcualtion. Illustration for our physical based limit correction process*



## 实验与关键发现

### 数据集与评估协议

ArtLLM的训练数据来自一个大规模、多样化的铰接物体集合，涵盖43个类别、共计20,673个物体（Table 1）。主实验在PartNet-Mobility数据集上进行评估，沿用SINGAPO划分的7个类别测试集。评估指标从两个维度衡量生成质量：

![[assets/figures/papers/paper_list_l2371_https_arxiv_org_abs_2603_01142/figures/004_Table_1.jpg]]
*Table 1: Statistics of our curated dataset for ArtLLM training*

- **零件布局精度**：mIoU（3D交并比，见公式(4)）衡量预测包围盒与真实包围盒的重叠程度。
- **关节结构准确性**：包括关节类型准确率（Type Acc）、图准确率（Graph Acc，衡量父子零件关系的层次结构正确性）、关节轴误差（Joint-Axis-Err，见公式(7)）、关节位置误差（Joint-Pos-Err）和关节运动范围IoU（Joint-Range-IoU）。

为保证公平性，对比实验中移除了检索式基线方法零件库中的真实零件，并将SINGAPO在相同数据集上重新训练。

### 主要定量结果

在PartNet-Mobility 7类测试集上，ArtLLM在所有核心指标上均显著超越现有方法（Table 2）：

![[assets/figures/papers/paper_list_l2371_https_arxiv_org_abs_2603_01142/figures/005_Table_2.jpg]]
*Table 2: Quantitative Comparison. We evaluate all methods on the seven categories of the PartNet-Mobility dataset (splitted by SIN-GAPO [26]). Metrics are computed per category, and the final score is obtained by an average over all seven categories. * denotes retraining on our dataset. Our method attains high performance, highlighting its strong ability to recover accurate articulated structures*

| 方法 | mIoU ↑ | Type Acc ↑ | Graph Acc ↑ | Joint-Axis-Err ↓ | Time(s) ↓ |
|------|--------|------------|-------------|-------------------|-----------|
| URDFormer | 0.3198 | 0.7722 | 0.5556 | 0.5201 | 12 |
| Singapo* | 0.4705 | 0.9065 | 0.6851 | 0.2463 | 84 |
| ArtLLM (Ours) | **0.6884** | **0.9084** | **0.7741** | **0.1271** | **19** |

ArtLLM的mIoU达到0.6884，较次优方法Singapo*（0.4705）提升46.3%，表明其在零件布局预测上具有压倒性优势。在关节结构建模上，图准确率77.41%（+8.9个百分点）和关节轴误差0.1271（降低48.4%）的显著改善，验证了统一推理几何与运动结构的有效性。此外，ArtLLM推理仅需19秒，远快于Singapo*的84秒。

分各类别的详细对比（Table 4）进一步显示，基线方法在复杂类别中频繁预测错误的关节类型（以“-”标记），而ArtLLM在所有类别上均保持稳定的关节预测能力。

![[assets/figures/papers/paper_list_l2371_https_arxiv_org_abs_2603_01142/figures/010_Table_4.jpg]]
*Table 4: Quantitative Comparison. We show the metrics on each category of the 3 method against our method. The ’-’ denotes that no limit is predicted due to the error joint type*

### 消融实验

Table 3的系统性消融实验揭示了各设计选择的因果贡献：

- **连续值量化（实验A）**：直接预测连续浮点数（去除离散token化）导致坐标和方向相关属性预测能力大幅下降，验证了将连续参数离散量化为128/48/64 bins是稳定训练的关键。
- **多任务训练（实验B）**：去除多任务设置、仅进行端到端训练，会恶化除轴方向外的所有指标——关节类型准确率从0.898降至0.825，图准确率从0.780降至0.737，证明零件布局、关节类型和层次结构三项任务的联合建模相互促进。
- **数据增强（实验C）**：去除随机缩放和旋转增强会降低零件IoU，说明几何不变性先验对包围盒预测至关重要。
- **多阶段训练（实验D）**：去除两阶段策略（即直接用P3SAM初始化点编码器进行完整训练），零件和关节预测精度均下降。第一阶段在零件布局上的预训练为后续关节预测提供了稳健的几何基础。

### 物理限位校正的定性验证

Figure 5展示了物理驱动限位校正的效果。校正前，预测的关节运动范围导致零件在铰接运动过程中发生明显的自碰撞；应用基于碰撞检测的限位优化后，铰接零件运动平滑且无碰撞，验证了该方法能有效提升生成资产的物理合理性。该模块通过分层搜索精确定位初始接触角，将碰撞检测信号中的导数尖峰映射为安全的关节限位值。

### 失败模式分析

Figure 9揭示了ArtLLM的主要失败模式：

1. **类别泛化不足**：训练数据中物体类别多样性有限，模型对车辆、机器人等复杂类别难以准确预测其运动学结构，需要人工验证。
2. **内部遮挡**：单张图像或单视角点云无法完整捕捉内部遮挡结构，导致生成的资产缺失内部零件细节。
3. **物理属性缺失**：框架未联合建模质量、摩擦等物理属性，生成的运动学结构虽几何准确，但缺乏物理感知能力。

这些失败模式直接对应了论文提出的开放问题：扩展开放词汇类别覆盖、联合建模物理属性、以及改进生成模型以重建被遮挡的内部结构。

### 补充图表

![[assets/figures/papers/paper_list_l2371_https_arxiv_org_abs_2603_01142/figures/006_Table_3.jpg]]
*Table 3: Quantitative Ablation. Ablation experiments evaluating the impact of our key components*

![[assets/figures/papers/paper_list_l2371_https_arxiv_org_abs_2603_01142/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative result for physical limit correction. Before correction, the predicted joint ranges cause noticeable selfcollisions during articulation. After applying our physics-based limit refinement, the articulated parts move smoothly without collision, yielding physically plausible and stable motion*

![[assets/figures/papers/paper_list_l2371_https_arxiv_org_abs_2603_01142/figures/008_Figure_6.jpg]]
*Figure 6: We teleoperate a Franka Panda robot to execute three articulation tasks and record its pose trajectories. Using ArtLLM, we reconstruct the corresponding articulated assets from real scenes and replay the trajectories in simulation. The simulated objects reproduce the real articulation behavior, showing that our generated assets accurately capture real-world kinematics and joint constraints*



## 定位与知识库关联

### 1. 问题域定位：铰接物体生成的方法论断层

铰接物体（Articulated Objects）的生成是三维视觉、机器人学和图形学的交叉难题。现有方法沿两条技术路线演进，但均存在根本性瓶颈：

- **优化重建路线**：通过对输入点云或图像进行逐物体关节拟合，能够恢复精确的运动学结构，但计算代价高昂（需缓慢的逐物体优化），且通常仅能处理简单单关节物体。
- **检索组装路线**：从预定义的固定零件库中检索并组装零件，如 **URDFormer**（仅限5个类别）、**SINGAPO** 和基于GPT-4o的 **Articulate-Anything**。此类方法速度较快，但因零件库覆盖有限，导致几何重复、泛化能力差，且几何与运动结构之间缺乏统一推理。

ArtLLM 正是在这一断层上提出新范式：将铰接结构预测转化为语言建模问题，使3D大语言模型能够自回归地同时预测可变数量的零件布局和关节，从而统一了几何与运动结构的推理。

### 2. 方法谱系中的关键变革点

ArtLLM 相对于现有基线方法在以下维度上实现了范式迁移：

| 变革维度 | 基线方法（检索/优化） | ArtLLM 方案 | 证据强度 |
|---------|---------------------|-------------|---------|
| **预测范式** | 优化重建或检索组装 | 3D LLM自回归生成离散token表示的零件布局和关节 | 强（Table 2, Figure 2） |
| **零件生成方式** | 从固定零件库检索 | 基于预测的包围盒条件合成零件几何（XPart模型） | 强（Sec.3.3） |
| **连续参数处理** | 直接回归浮点数 | 离散量化为128/48/64 bins的token + 分层方向码本 | 强（Table 3 Exp A） |
| **训练策略** | 单阶段端到端训练 | 多任务多阶段训练：阶段一零件布局预训练，阶段二全部任务SFT | 强（Table 3 Exp D） |
| **关节限位优化** | 无或简单规则 | 物理驱动的碰撞检测限位校正，通过导数尖峰定位初始接触角 | 中强（Figure 5） |

核心洞察在于：将零件轴对齐包围盒和关节参数表示为离散token序列，并利用大规模铰接数据集进行多任务多阶段监督微调，使3D LLM能够学习强大的零件几何先验和运动学关系，克服了传统方法中连续值回归不稳定的问题。

### 3. 适用边界与局限性

尽管 ArtLLM 在 PartNet-Mobility 数据集上取得了显著优势，其适用边界受以下因素制约：

1. **类别覆盖有限**：训练数据中物体类别多样性有限，对车辆、机器人等复杂类别泛化能力不足。当前模型在训练分布外的复杂铰接结构上可能退化。
2. **物理属性缺失**：框架未联合建模物理属性（如质量、摩擦等），生成的铰接资产在动力学仿真中可能缺乏物理真实性。
3. **遮挡结构不完整**：内部遮挡结构无法从单张图像中完整捕捉，导致生成资产缺失内部细节（如抽屉内部结构）。
4. **依赖点云输入质量**：方法以点云为输入，对传感器噪声和点云稀疏性的鲁棒性尚未充分验证。

### 4. 未来方向与开放问题

基于上述局限，以下方向值得探索：

- **开放词汇类别扩展**：如何扩展模型以支持开放词汇类别，提升类别覆盖率，使其能处理训练中未见过的铰接物体类型？
- **物理感知铰接预测**：如何联合建模质量、摩擦等物理属性，实现物理感知的铰接结构预测，使生成资产直接适用于动力学仿真？
- **遮挡结构补全**：如何改进生成模型以重建被遮挡的内部结构，从单视图或多视图输入中恢复完整的铰接几何？
- **多模态条件扩展**：当前方法以点云为主要输入，如何有效融合文本描述或图像等多模态条件，提升控制的灵活性和精度？



## 原文 PDF

![[paperPDFs/CVPR_2026/ArtLLM_Generating_Articulated_Assets_via_3D_LLM.pdf]]
