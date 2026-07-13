---
title: "RoMo: A Large-Scale, Richly Organized Dataset and Semantic Taxonomy for Human Motion Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RoMo_A_Large_Scale_Richly_Organized_Dataset_and_Semantic_Taxonomy_for_Human_Motion_Generation.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_RoMo_A_Large-Scale_Richly_Organized_Dataset_and_Semantic_Taxonomy_for_CVPR_2026_paper.html
project_link: https://davidzhang73.github.io/romo-website
code_link: null
aliases:
- RoMo
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 引入分层语义分类体系（类别-子类别-原子动作）并以此为指导构建自适应过滤流水线（动态评分 + 类别感知阈值），从大规模视频中筛选出高质量、高动态且语义均衡的运动数据。
primary_logic: 通过构建覆盖广泛的人类运动分类法，并以该分类法为骨架驱动视频采集、语义分割、3D运动估计和自适应质量过滤，能够系统性地打破数据规模与质量之间的权衡，产出兼具多样性、动态性和精确语义标注的大规模运动数据集，从而显著提升运动生成模型的保真度、多样性和文本理解能力。
claims:
- RoMo数据集包含820K核心剪辑（1237.8小时），远超此前最大规模数据集MotionMillion的560K核心剪辑。
- RoMo的动态评分（Dynamic Score）均值比MotionMillion高41.4%，表明运动质量显著提升。
- RoMo的子类别覆盖比MotionMillion多61.7%，尤其在长尾类别上覆盖更优。
- 在RoMo上训练的扩散模型MDM和自回归模型MMGPT均取得了SOTA的保真度和多样性（见表2），且分类别评估揭示了模型在不同动作上的盲点。
---

# RoMo: A Large-Scale, Richly Organized Dataset and Semantic Taxonomy for Human Motion Generation

> [!tip] 核心洞察
> 通过构建覆盖广泛的人类运动分类法，并以该分类法为骨架驱动视频采集、语义分割、3D运动估计和自适应质量过滤，能够系统性地打破数据规模与质量之间的权衡，产出兼具多样性、动态性和精确语义标注的大规模运动数据集，从而显著提升运动生成模型的保真度、多样性和文本理解能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | RoMo：大规模精细组织的人体运动生成数据集与语义分类体系 |
| 英文题名 | RoMo: A Large-Scale, Richly Organized Dataset and Semantic Taxonomy for Human Motion Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_RoMo_A_Large-Scale_Richly_Organized_Dataset_and_Semantic_Taxonomy_for_CVPR_2026_paper.html) · [Project](https://davidzhang73.github.io/romo-website) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | RoMo数据集构建与分类感知过滤流水线 |
| Dataset |  |

> [!tip] 效果简介
> - 数据集规模与多样性对比 上，核心剪辑数量 / 时长 820K / 1237.8h vs MotionMillion: 560K / 726.5h (+46% 剪辑 / +70% 时长)。
> - 子类别覆盖对比 上，Subcategory coverage improvement vs MotionMillion RoMo vs MotionMillion (+61.7%)。
> - 运动动态性对比 上，Mean Dynamic Score improvement vs MotionMillion RoMo vs MotionMillion (+41.4% (higher is better))。

## 概要

人体运动生成领域长期面临一个根本性瓶颈：现有大规模“in-the-wild”运动数据集虽然数据量庞大，但缺乏精细的组织与管理，导致静态、低质量序列占据主导，且没有结构化的分类体系。这种数据层面的缺陷严重制约了扩散模型、自回归模型等生成方法的性能上限——模型无法从杂乱无章的数据中充分学习高质量、多样化的运动表征。

针对这一瓶颈，RoMo提出了一个系统性的解决方案：**以语义分类体系为骨架，驱动从视频采集到运动过滤的全流程**。具体而言，RoMo构建了一个三层语义分类体系（54个类别 → 2,065个子类别 → 28,874个原子动作），并以此为指导设计了自适应过滤流水线——通过动态评分（Dynamic Score）与类别感知阈值（top-P percentile），从125.3K小时的原始视频中仅筛选出1%的高质量运动数据，最终产出包含820K核心剪辑、1,237.8小时的运动数据集。

RoMo的核心贡献在于打破了数据规模与质量之间的传统权衡。实验表明，RoMo的子类别覆盖比此前最大规模数据集MotionMillion多出61.7%，动态评分均值高出41.4%，尤其在长尾类别上覆盖更优。在RoMo上训练的扩散模型MDM和自回归模型MMGPT均取得了SOTA的保真度与多样性，验证了高质量数据对生成模型性能的决定性作用。

### 人体运动生成的数据瓶颈

人体运动生成（Human Motion Generation）旨在根据文本描述等控制信号合成逼真的三维人体动作序列，在动画制作、虚拟现实、游戏开发和机器人学习等领域具有广泛的应用前景。近年来，扩散模型和自回归模型等生成式架构在运动生成任务上取得了显著进展，但其性能上限在很大程度上受制于训练数据的规模、质量和组织方式。

当前领域面临的核心瓶颈在于：**现有大规模in-the-wild人体运动数据集缺乏精细的管理与组织**。具体表现为三个相互交织的问题：

1. **静态与低质量序列主导**：从互联网视频中提取的运动数据包含大量静止站立、缓慢移动或姿态估计伪影严重的片段，这些低动态序列不仅消耗存储和计算资源，还会在训练过程中向生成模型注入噪声，降低合成运动的逼真度和物理合理性。
2. **缺乏结构化分类体系**：现有数据集通常以无序或无分类的方式组织运动序列，缺少从粗粒度类别到细粒度原子动作的分层语义结构。这使得数据分布不透明，难以评估和保证动作类别的覆盖均衡性。
3. **规模与质量的权衡未打破**：尽管已有MotionMillion等大规模数据集尝试扩充数据量，但其过滤策略依赖固定阈值或无过滤，无法在保留长尾类别的同时有效剔除低质量样本，导致“规模增长—质量稀释”的困境持续存在。

### 现有数据集的局限

表1系统对比了RoMo与现有公开三维运动数据集的关键指标。此前最大规模的in-the-wild数据集MotionMillion拥有约560K核心剪辑（726.5小时），但其文本标注丰富度仅为每段1-3个说明，且未提供语义分类体系。HumanML3D等高质量数据集虽然具备精细的文本标注，但规模受限（约15K序列），难以支撑大规模生成模型的训练需求。这种“大规模无组织”与“小规模高质量”之间的割裂，严重制约了运动生成模型在保真度、多样性和文本理解能力上的协同提升。

### 本文动机与核心思路

针对上述缺口，本文提出**RoMo**——一个大规模精细组织的人体运动生成数据集与语义分类体系。其核心动机在于：**以分层语义分类体系为骨架，驱动从视频采集到质量过滤的全流水线，系统性地打破数据规模与质量之间的权衡**。

具体而言，RoMo引入了一个三层语义分类法（54类别、2,065子类别、28,874原子动作），并以此为指导构建了分类感知的自适应过滤流水线。该流水线通过动态评分（Dynamic Score）量化运动质量，并采用类别感知的Top-P百分位过滤策略，确保在激进清洗99%原始素材的同时，仍能保留长尾类别的代表性样本。最终产出的数据集包含820K核心剪辑（1237.8小时），每段配备5个多样化文本描述，兼具大规模、高动态性和精确语义标注三重优势，为运动生成模型的训练和评估提供了更坚实的数据基础。

## 核心方法与创新机理

### 1. 分层语义分类体系：从无序到结构化组织

RoMo 的核心创新在于首次为大规模人体运动数据集构建了一套完整的**三层语义分类体系**（Category → Subcategory → Atomic-action），包含 **54 个类别、2,065 个子类别和 28,874 个原子动作**。这一体系从根本上改变了运动数据的组织方式——此前的大规模数据集（如 MotionMillion）缺乏结构化的类别划分，运动序列处于无序状态。

该分类体系的底层原子动作被定义为简短的现在时动词短语（如 *Swing racket* 或 *Climb stairs*），可包含物体或身体部位但避免修饰语和标点，确保标注的标准化与可扩展性。这种设计使得每个运动片段都能被精确映射到语义空间中的特定节点，为后续的类别感知过滤和生成模型的细粒度评估提供了骨架支撑。

### 2. 类别感知的自适应过滤：打破质量与多样性的权衡

传统数据集通常采用固定阈值或无过滤策略，导致静态、低质量序列大量留存，或对微小动作类别造成过度清洗。RoMo 提出了**基于动态评分的类别感知 Top-P 过滤**机制，这是实现高质量与高多样性兼得的关键。

具体而言，RoMo 设计了一个混合动态评分 $S_{\text{Dynamic}}$，综合时间分量（瞬时速度强度）和空间分量（关节轨迹覆盖范围）：

$$S_{\text{temporal}} = \frac{1}{F \cdot J} \sum_{t=1}^{F} \sum_{j=1}^{J} \| \mathbf{v}_{t,j} \|_2$$

$$S_{\text{spatial}} = \frac{1}{J} \sum_{j=1}^{J} \left\| \max_t \mathbf{p}_{t,j} - \min_t \mathbf{p}_{t,j} \right\|_2$$

$$S_{\text{Dynamic}} = w_v \cdot S_{\text{temporal}} + w_r \cdot S_{\text{spatial}}$$

其中 $w_v = 0.7$，$w_r = 0.3$。该评分在**每个类别内部独立计算**，然后选取各类别中的 Top-P 百分位序列，而非使用全局统一阈值。这一设计保证即使是微小的动作类别（如手指精细操作）也能保留其高质量代表样本，避免了常规过滤对长尾类别的系统性清除。

### 3. 语义驱动的视频分割：从固定切片到原子动作对齐

传统数据集通常采用固定长度切片处理视频，导致运动片段语义不完整或跨动作混合。RoMo 引入**语义驱动的时序分割**，利用多模态视觉语言模型 Qwen3-VL，将分类法节点与可用的原子动作词汇表一同输入模型，使视频被精确切分为与原子动作对齐的片段。这一改进使得每个数据单元都具有明确的语义边界，提升了文本-运动对齐的精度。

### 4. 丰富的文本标注：从稀疏说明到多角度描述

相比此前数据集每个运动仅提供 1-3 条说明，RoMo 为**每个运动片段生成 5 条多样化文本描述**，且这些描述与分类标签对齐。这种多角度标注策略增强了文本-运动对的语义丰富度，为生成模型提供了更强的条件信号。

### 创新总结

RoMo 的四项创新构成一个相互增强的系统：**分类体系**为数据组织提供骨架，**语义分割**确保数据单元与分类节点对齐，**动态评分**量化运动质量，**类别感知过滤**在保持多样性的前提下剔除低质量数据。这一闭环使得 RoMo 在规模（820K 核心剪辑，1237.8 小时）、多样性（子类别覆盖比 MotionMillion 多 61.7%）和动态性（动态评分均值高 41.4%）三个维度上均显著超越此前最大规模的数据集。

> **需人工核实**：动态评分公式中权重 $w_v=0.7$、$w_r=0.3$ 的选择依据及 Top-P 百分位 P 的具体取值，论文未提供深入的消融分析，其对下游生成模型性能的影响尚待量化验证。

RoMo 的数据构建流程围绕一个核心理念展开：以**分层语义分类体系为骨架**，驱动从大规模网络视频中系统性地提取、过滤和标注高质量人体运动数据。整个流水线遵循“查询—清洗—分割—估计—过滤—标注”的级联架构，最终从约 125.3K 小时的原始视频中蒸馏出仅 1% 的高质量运动片段（Figure 3），形成 820K 核心剪辑、1237.8 小时的运动数据集。

### 流水线模块关系与数据流

Figure 2 展示了完整的端到端流水线，其模块间的输入输出关系可概括为以下六个阶段：

![[assets/figures/papers/paper_list_l23_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RoMo_A_Large_Sca/figures/003_Figure_2.jpg]]
*Figure 2: Data Pipeline. RoMo is extracted from a large web video corpus. We query human motion videos, filter single-human scenes, and segment them into atomic actions. We then apply a 3D camera and pose estimation, remove low-quality motions, and caption and categorize the results using our hierarchical taxonomy. Overall, the pipeline performs uncompromising large-scale filtering that processes 125K hours of raw footage and distills 1% into high-quality, well-annotated motions*

1. **视频查询与元数据过滤**：以预定义的三层分类体系（54 类别 → 2,065 子类别 → 28,874 原子动作）为查询种子，从大规模视频平台检索候选视频，并利用 LLM 对视频元数据（标题、标签等）进行初筛，剔除明显不相关的视频。

2. **场景与单人检测**：对通过初筛的视频进行场景转场检测，将长视频切分为场景一致的片段；随后移除静态片段（如固定机位的空镜），并使用 YOLOv8 进行单人检测，确保画面中仅存在单一可辨识的人体主体。

3. **时序语义分割**：采用多模态视觉语言模型 **Qwen3-VL** 对清洗后的视频片段进行语义驱动的时序分割。模型接收当前视频所属的分类法节点及允许的原子动作词汇表，输出与原子动作对齐的时序边界，将连续视频切分为语义完整的原子动作片段。

4. **3D 运动估计**：对每个原子动作片段，使用 **GVHMR** 模型估计 SMPL 格式的 3D 人体运动参数，包括全局位移、根节点旋转和 24 个关节角度，为后续质量评估和生成模型训练提供标准化的运动表征。

5. **运动评估与自适应过滤**：计算每个运动片段的**动态评分**（Dynamic Score），该评分由时间分量 $S_{\mathrm{temporal}}$ 和空间分量 $S_{\mathrm{spatial}}$ 加权合成。流水线采用**类别感知的 Top-P 过滤策略**——在每个语义类别内部按动态评分排序，仅保留前 P 百分位的样本，从而在保证整体运动质量的同时，避免对微小动作类别的过度清洗。

6. **文本描述与分类标注**：Qwen3-VL 为每个保留的运动片段生成 5 条多样化的文本描述，并将其映射到分类体系中对应的类别、子类别和原子动作标签，实现运动数据与语义标签的精确对齐。

### 关键设计决策

流水线的两个核心设计突破了传统运动数据集构建中“规模与质量不可兼得”的瓶颈：

- **分类体系驱动的全流程指导**：分类体系不仅是最终数据的组织框架，更深度嵌入流水线的每个环节——从视频查询的关键词生成、语义分割时的词汇表约束，到过滤阶段的类别感知阈值设定，确保了数据采集的覆盖均衡性和语义一致性。

- **自适应而非一刀切的过滤**：传统的固定阈值过滤容易导致高动态类别（如“跳跃”）样本泛滥而低动态类别（如“书写”）被误删。RoMo 的类别感知 Top-P 过滤在每个类别内部独立排序筛选，保证了长尾动作类别也能保留足够的高质量样本，这是数据集在子类别覆盖上比 MotionMillion 多 61.7% 的关键机制（Figure 5）。

### 流水线压缩效率

Figure 3 以柱状图形式量化了各过滤模块的数据压缩效果：从原始视频查询的 125.3K 小时开始，经过元数据过滤、场景检测、单人过滤、语义分割、运动质量过滤等逐级筛选，最终输出约 1.3K 小时的高质量运动数据，整体保留率仅为 1%。这种激进的过滤策略是 RoMo 在动态评分上比 MotionMillion 均值高 41.4% 的直接原因（Figure 6）。

### 流水线架构

RoMo 的数据构建流水线遵循“分类法驱动采集 → 语义分割 → 运动估计 → 自适应过滤”的级联架构，最终从 125.3K 小时的原始视频中仅保留约 1% 的高质量运动序列（Figure 2, Figure 3）。流水线包含六个核心模块：

![[assets/figures/papers/paper_list_l23_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RoMo_A_Large_Sca/figures/004_Figure_3.jpg]]
*Figure 3: Aggressive filtering. Filtering out 99% of total input duration in our data pipeline. The chart shows the input (red) and output (green) hours for each filtering module, demonstrating a reduction from 125.3K to 1.3K total hours*

1. **视频查询与元数据过滤**：基于三层语义分类体系（类别 → 子类别 → 原子动作）构造查询词，从大规模视频平台检索候选视频，并利用 LLM 过滤标题、标签等元数据不相关的视频。
2. **场景与单人检测**：通过场景转场检测将视频切分为连续镜头，移除静态片段；使用 YOLOv8 进行单人检测，确保每帧仅包含一个清晰可见的主体。
3. **时序语义分割**：以 Qwen3-VL 多模态大模型对清洗后的片段进行语义驱动的原子动作分割，模型接收分类法节点及允许的原子动作词汇表，输出动作对齐的时间片段。
4. **3D 运动估计**：采用 GVHMR 模型从视频片段中提取 SMPL 格式的 3D 人体运动，输出包含全局位移、根节点朝向及 24 个关节角度。
5. **文本描述与分类标注**：Qwen3-VL 为每个动作片段生成 5 条多样化描述，并将其映射到分类体系中的对应标签。
6. **运动评估与过滤**：计算动态评分并执行类别感知的自适应 Top-P 过滤，确保各动作类别的高质量与均衡覆盖。

### 动态评分公式

为量化运动序列的质量与动态性，RoMo 设计了一个混合评分函数，综合时间活跃度与空间覆盖范围两个维度。

**时间分量**衡量逐帧运动的瞬时强度，计算所有关节速度幅值的均值：

$$S_{\mathrm{temporal}} = \frac{1}{F \cdot J} \sum_{t=1}^{F} \sum_{j=1}^{J} \| \mathbf{v}_{t,j} \|_2$$

其中 $F$ 为序列帧数，$J$ 为关节数量，$\mathbf{v}_{t,j}$ 表示第 $t$ 帧第 $j$ 个关节的速度向量。

**空间分量**捕捉运动在空间中的整体延展程度，通过每个关节轨迹的范围来度量：

$$S_{\mathrm{spatial}} = \frac{1}{J} \sum_{j=1}^{J} \left\| \max_t \mathbf{p}_{t,j} - \min_t \mathbf{p}_{t,j} \right\|_2$$

其中 $\mathbf{p}_{t,j}$ 为第 $t$ 帧第 $j$ 个关节的位置向量，$\max_t \mathbf{p}_{t,j}$ 与 $\min_t \mathbf{p}_{t,j}$ 分别表示该关节在整个序列中沿各坐标轴的最大值与最小值。

**动态评分**以加权和的形式融合两个分量：

$$S_{\mathrm{Dynamic}} = w_v \cdot S_{\mathrm{temporal}} + w_r \cdot S_{\mathrm{spatial}}$$

权重设定为 $w_v = 0.7$，$w_r = 0.3$，赋予时间活跃度更高的权重，以优先保留具有显著动态变化的运动序列。该权重选择未提供深入的消融分析，其最优性需进一步验证。

### 类别感知自适应过滤

传统固定阈值过滤会系统性淘汰微小动作类别（如“挥手”“点头”），导致长尾类别覆盖不足。RoMo 的过滤策略将全局阈值替换为类别内 Top-P 百分位选择：在每个原子动作类别内独立计算动态评分分布，仅保留评分位于前 $P$ 百分位的序列。这一设计保证了即使动态幅度较小的精细动作也能在数据集中得到充分保留，从而在质量与多样性之间取得平衡。论文未量化 $P$ 的具体取值及其对下游生成模型性能的敏感性。

## 实验与关键发现

### 数据集规模与质量基准

RoMo 数据集与现有公开 3D 运动数据集的系统对比见 Table 1。RoMo 在核心剪辑数量（820K）和总时长（1237.8 小时）两个维度均显著超越此前最大规模的 MotionMillion 数据集（560K 核心剪辑，726.5 小时），剪辑数量提升 46%，时长提升 70%。在文本标注丰富度方面，RoMo 为每个运动序列提供 5 条多样化描述，远超现有数据集通常的 1-3 条说明。RoMo 是首个同时集成大规模层级化语义分类体系与海量运动数据的数据集。

![[assets/figures/papers/paper_list_l23_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RoMo_A_Large_Sca/figures/002_Table_1.jpg]]
*Table 1: Comparison of RoMo with existing publicly available 3D motion datasets with free-form text annotations. RoMo is the first to integrate both a large-scale hierarchical semantic taxonomy and a massive-scale dataset, featuring 820K core clips (1237.8 hours). For clarity, in the table: ‘Text diversity’ refers to the number of captions per motion sequence. ‘Clip Number’ reports both the core set (new motion sequences proposed in that work) and the total clips*

### 类别覆盖与多样性优势

Figure 5 展示了 RoMo 与 MotionMillion 在类别覆盖上的对比。RoMo 的子类别覆盖比 MotionMillion 多 61.7%，尤其在长尾类别上表现突出——Figure 5(b) 显示 RoMo 在低频类别上的序列数量远多于 MotionMillion，证实了分类感知过滤策略在维持数据均衡性方面的有效性。Figure 7 的 t-SNE 分析进一步表明，与 MotionMillion 和 HumanML3D 相比，RoMo 在运动特征空间中具有更广的覆盖范围，且“Sports”类别内部按子类别呈现清晰的语义聚类，验证了分类体系的质量。

![[assets/figures/papers/paper_list_l23_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RoMo_A_Large_Sca/figures/006_Figure_5.jpg]]
*Figure 5: Superior diversity and coverage. Comparison of sequence counts per category between our RoMo and MotionMillion (a). The bottom figure (b) shows the “tail” of the distribution of both datasets on the same plot, demonstrating how our dataset provides better coverage of these less frequent categories*

![[assets/figures/papers/paper_list_l23_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RoMo_A_Large_Sca/figures/008_Figure_7.jpg]]
*Figure 7: t-SNE analysis. (left) Comparison of RoMo (ours) and MotionMillion and HumanML3D, showing improved coverage. (right) Semantic clustering of ’Sports’ category, where points are colored by subcategory, confirming our Taxonomy’s quality*

### 运动动态性评估

为量化运动质量，RoMo 引入动态评分（Dynamic Score）指标，综合时间分量 $S_{\mathrm{temporal}} = \frac{1}{F \cdot J} \sum_{t=1}^{F} \sum_{j=1}^{J} \| \mathbf{v}_{t,j} \|_2$ 与空间分量 $S_{\mathrm{spatial}} = \frac{1}{J} \sum_{j=1}^{J} \left\| \max_t \mathbf{p}_{t,j} - \min_t \mathbf{p}_{t,j} \right\|_2$，以权重 $w_v=0.7$ 和 $w_r=0.3$ 合成最终评分 $S_{\mathrm{Dynamic}}$。Figure 6 显示，RoMo 在大多数类别上的动态评分均值比 MotionMillion 高 41.4%，表明其过滤流水线有效剔除了静态和低质量序列，保留了高动态性的运动片段。

### 生成模型性能验证

为验证 RoMo 对下游任务的价值，作者在 RoMo 上训练了两类代表性生成模型：扩散模型 MDM 和自回归模型 MMGPT，结果见 Table 2。在 FID 指标上，MMGPT 达到 12.80，显著优于 MDM 的 20.63（降低 7.83）；在 Matching Score 上，MMGPT 也以 22.08 优于 MDM 的 12.06。然而，在物理合理性方面，MDM 的 Foot Skating 指标为 $1.70\times10^{-3}$，远低于 MMGPT 的 $92.0\times10^{-3}$，且 Diversity 指标上 MDM 同样占优。这表明两类模型在保真度与多样性之间存在不同权衡，RoMo 为分析这种模型行为差异提供了充分的测试基础。

![[assets/figures/papers/paper_list_l23_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RoMo_A_Large_Sca/figures/010_Table_2.jpg]]
*Table 2: Motion generation performance for MDM (diffusion) and MMGPT (GPT) models on RoMo*

### 分类别评估揭示模型盲点

Figure 9 展示了 MDM 在 RoMo 各动作类别上的分类别评估热力图。传统聚合指标掩盖了模型在不同动作类别上的显著性能差异——某些类别上模型表现优异，而另一些类别则存在明显盲点。这一分析凸显了 RoMo 精细分类体系在诊断生成模型能力边界方面的独特价值，为后续针对性改进提供了方向指引。

### 过滤流水线效率

Figure 3 量化了 RoMo 数据流水线的过滤强度：从原始 125.3K 小时视频输入，经各模块逐级过滤后，最终仅保留约 1.3K 小时高质量运动数据，整体保留率约 1%。这一激进过滤策略是 RoMo 在数据质量上取得优势的关键机制，但也意味着对 3D 姿态估计算法（GVHMR）和语义分割模型（Qwen3-VL）的准确性有较强依赖——若上游模块存在系统性误差，下游数据质量将受到传导影响。论文未对动态评分公式的权重选择（$w_v=0.7$, $w_r=0.3$）及自适应过滤的 Top-P 百分位选择提供消融分析，这些超参数对最终数据分布的影响仍需进一步验证。

## 定位与知识库关联

### 问题定位与领域瓶颈

RoMo 切入的是**大规模in-the-wild人体运动生成的数据瓶颈**。现有数据集面临三重困境：

1. **规模-质量权衡失效**：MotionMillion（约560K核心剪辑）虽在规模上取得突破，但其数据源自未经过滤的互联网视频，导致静态、低质量序列占据主导。RoMo的分析表明，其动态评分均值比MotionMillion高41.4%（Figure 6），说明后者存在大量“伪运动”片段。

2. **语义组织缺位**：HumanML3D、KIT-ML等早期数据集规模有限且依赖人工标注，无法覆盖长尾动作类别；而大规模数据集缺乏结构化的分类体系，使得生成模型难以建立文本-运动的精细映射。RoMo的子类别覆盖比MotionMillion多61.7%，尤其在长尾类别上优势明显（Figure 5）。

3. **过滤策略粗暴**：固定阈值过滤会系统性地清除微小但重要的动作类别（如精细手部操作），导致类别分布失衡。RoMo提出的**类别感知自适应过滤**（top-P percentile）是解决这一矛盾的关键机制。

### 核心方法贡献：分类体系驱动的数据生产范式

RoMo的方法论贡献不在于提出新的生成模型架构，而在于**重新定义了大规模运动数据的生产方式**——以语义分类体系为骨架，驱动从视频采集到质量过滤的全链路。这一范式包含三个相互耦合的创新点：

#### 1. 三层语义分类体系作为数据骨架

RoMo构建了54类别 → 2065子类别 → 28874原子动作的三层层次化分类法（Section 3.1）。与传统的扁平标签体系不同，该分类法具有以下特性：

- **原子动作的动词短语形式**：如“Swing racket”或“Climb stairs”，避免修饰词和标点，确保文本-运动对齐的精确性。
- **可执行性**：分类法直接驱动视频查询（基于类别/子类别关键词）和VLM时序分割（将分类节点与原子动作词汇表输入Qwen3-VL），实现了从语义到数据的闭环。

#### 2. 自适应类别感知过滤

RoMo的动态评分由时间分量和空间分量加权合成：

$$S_{\mathrm{Dynamic}} = w_v \cdot S_{\mathrm{temporal}} + w_r \cdot S_{\mathrm{spatial}}$$

其中 $S_{\mathrm{temporal}} = \frac{1}{F \cdot J} \sum_{t=1}^{F} \sum_{j=1}^{J} \| \mathbf{v}_{t,j} \|_2$ 度量瞬时运动强度，$S_{\mathrm{spatial}} = \frac{1}{J} \sum_{j=1}^{J} \| \max_t \mathbf{p}_{t,j} - \min_t \mathbf{p}_{t,j} \|_2$ 度量关节轨迹的空间覆盖范围（权重 $w_v=0.7$, $w_r=0.3$）。

关键创新在于**在每个类别内部独立选取top-P百分位**，而非使用全局统一阈值。这保证了“瑜伽”、“冥想”等低动态类别中的高质量样本不会被错误清除，同时“跑酷”、“搏击”等高动态类别中的低质序列能被有效过滤。

#### 3. 语义驱动的时序分割

传统方法使用固定长度滑窗切分视频，导致动作边界错位。RoMo采用Qwen3-VL多模态大模型，以分类法中的原子动作词汇表为约束进行语义时序分割（Section 3.3），使每个数据片段精确对应一个原子动作。这一设计直接提升了文本-运动对齐的粒度。

### 与现有工作的关系

#### 数据集层面的定位

| 维度 | HumanML3D | MotionMillion | RoMo |
|------|-----------|---------------|------|
| 规模 | 14.6K核心 | 560K核心 | 820K核心 |
| 分类体系 | 无 | 无 | 三层层次化（54/2065/28874） |
| 文本多样性 | 3-4条/motion | 1条/motion | 5条/motion |
| 过滤策略 | 人工筛选 | 基础清洗 | 类别感知自适应过滤 |
| 3D估计 | 多方法融合 | 未明确 | GVHMR统一估计 |

RoMo在规模上超越MotionMillion 46%（核心剪辑数）和70%（总时长），同时首次将大规模数据与精细语义组织结合。

#### 生成模型验证的定位

RoMo在两种代表性生成范式上验证了数据集的有效性（Table 2）：

- **扩散模型MDM**：FID 20.63，在物理合理性指标（Foot Skating 1.70e-3）上显著优于MMGPT，体现了扩散模型在捕捉连续运动细节上的优势。
- **自回归模型MMGPT**（基于3B Llama）：FID 12.80，Matching Score 22.08，在文本-运动对齐上表现更优，但物理合理性较差（Foot Skating 92.0e-3）。

这种互补性揭示了RoMo作为**多范式评估基准**的价值：不同架构在不同维度上各有盲点，分类别评估（Figure 9热力图）进一步暴露了模型在特定动作类别上的系统性失败，为后续研究提供了明确的改进方向。

### 适用边界与局限

1. **3D姿态估计依赖**：RoMo的运动质量受限于GVHMR的估计精度。在严重遮挡、极端视角或多人交互场景下，重建误差可能被传播到数据集中。论文未提供针对这些failure case的系统分析。

2. **分类体系的静态性**：当前分类法是人工构建的，虽然覆盖广泛，但难以自动适应新出现的人类活动（如新兴运动、VR交互）。如何实现分类法的自动扩展是一个开放问题。

3. **过滤权重的未验证性**：动态评分中 $w_v=0.7$ 和 $w_r=0.3$ 的选择，以及top-P百分位P的取值，均未提供消融实验验证其对下游生成任务的影响。这些超参数可能对不同类别的适用性存在差异。

4. **数据源偏差**：大规模互联网视频不可避免地携带文化、地域和人口统计学偏见。论文未讨论RoMo是否可能放大这些偏见，以及如何缓解。

### 开放问题

- 如何量化自适应过滤中top-P选择对生成模型性能的影响，并建立P值与类别特性的关系模型？
- 分类体系能否通过主动学习或LLM辅助实现半自动扩展，以适应动态变化的人类活动空间？
- 在极端场景（遮挡、密集人群、非标准视角）下，如何评估并提升数据质量的下限？
- RoMo的5条多样化说明是否在所有类别上均保持质量一致？不同类别的文本标注难度是否存在系统性差异？

## 原文 PDF

![[paperPDFs/CVPR_2026/RoMo_A_Large_Scale_Richly_Organized_Dataset_and_Semantic_Taxonomy_for_Human_Motion_Generation.pdf]]
