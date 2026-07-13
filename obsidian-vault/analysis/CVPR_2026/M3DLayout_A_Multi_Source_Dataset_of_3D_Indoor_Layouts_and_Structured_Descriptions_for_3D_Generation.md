---
title: "M3DLayout: A Multi-Source Dataset of 3D Indoor Layouts and Structured Descriptions for 3D Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/M3DLayout_A_Multi_Source_Dataset_of_3D_Indoor_Layouts_and_Structured_Descriptions_for_3D_Generation.pdf
project_link: null
code_link: "https://github.com/Graphic-Kiliani/M3DLayout-code"
aliases:
- MDTCLGMDMAM
- M3DLayout
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 通过整合真实扫描、专业CAD设计与程序化生成三类互补数据源，并为每个布局标注多层级结构化文本描述，大幅提升了训练数据的规模、多样性和语义丰富度。
primary_logic: 将多源3D布局与结构化文本配对，使模型能够学习从全局场景组织到细粒度小物体布置的复杂空间模式，从而在文本驱动下生成细节更丰富、更可控的室内场景布局。
claims:
- M3DLayout包含21,367个布局和超过433k个物体实例，来自三种互补数据源，带有详细的结构化描述。
- 在Inf3DLayout基准上，DIFF-M3DLayout的FID较DiffuScene降低31.27（降幅约30%），AR-M3DLayout的FID更低至57.90，同时CLIP-Score超越所有基线。
- Inf3DLayout 上 FID (×0.001) = 70.85 (DIFF-M3DLayout)
- Inf3DLayout 上 KID (×0.001) = 50.94 (DIFF-M3DLayout)
---

# M3DLayout: A Multi-Source Dataset of 3D Indoor Layouts and Structured Descriptions for 3D Generation

> [!tip] 核心洞察
> 将多源3D布局与结构化文本配对，使模型能够学习从全局场景组织到细粒度小物体布置的复杂空间模式，从而在文本驱动下生成细节更丰富、更可控的室内场景布局。

| 字段 | 内容 |
|------|------|
| 中文题名 | M3DLayout：面向3D生成的多源三维室内布局及结构化描述数据集 |
| 英文题名 | M3DLayout: A Multi-Source Dataset of 3D Indoor Layouts and Structured Descriptions for 3D Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2509.23728) · [Code](https://github.com/Graphic-Kiliani/M3DLayout-code) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | M3DLayout Dataset and Text-Conditioned Layout Generation Models (DIFF-M3DLayout & AR-M3DLayout) |
| Dataset | Inf3DLayout, Overall |

> [!tip] 效果简介
> - Inf3DLayout 上，FID (×0.001) 70.85 (DIFF-M3DLayout) vs 102.12 (DiffuScene) (-31.27 (-30.6%))；KID (×0.001) 50.94 (DIFF-M3DLayout) vs 75.49 (DiffuScene) (-24.55 (-32.5%))；FID (×0.001) 57.90 (AR-M3DLayout) vs 102.12 (DiffuScene) (-44.22 (-43.3%))。
> - Overall 上，CLIP-Score 0.2026 (AR-M3DLayout) vs 0.1982 (DiffuScene) (+0.0044 (+2.2%))。

## 概要

3D室内场景生成是计算机视觉与图形学的核心挑战，其目标是根据文本描述自动合成合理的三维房间布局。然而，现有工作面临一个根本性瓶颈：**训练数据规模小、来源单一、缺乏高质量的结构化文本标注**。主流数据集如3D-FRONT主要来源于专业CAD设计，场景多样性有限，且小物体占比极低（仅0.2%），导致文本条件生成模型难以学习丰富的空间与语义关系，生成的场景细节匮乏、控制力弱。

针对这一瓶颈，本文提出 **M3DLayout**——一个面向文本驱动3D室内布局生成的大规模多源数据集，并在此基础上构建了两种互补的文本条件生成模型 **DIFF-M3DLayout** 和 **AR-M3DLayout**。核心思路是：**将多源3D布局与结构化文本配对，使模型能够学习从全局场景组织到细粒度小物体布置的复杂空间模式**。

M3DLayout数据集包含 **21,367个布局** 和超过 **433k个物体实例**，整合了三类互补数据源：真实扫描（Matterport3D）、专业CAD设计（3D-FRONT）和程序化生成场景（Infinigen）。每个布局均配有三级结构化文本描述——全局场景描述、大家具描述和小物体描述，通过规则模板与GPT-4o多视图生成并经人工验证构建。

实验表明，在Inf3DLayout基准上，DIFF-M3DLayout的FID较 **DiffuScene**（Tang et al., CVPR 2024）降低31.27（降幅约30%），AR-M3DLayout的FID更低至57.90（降幅约43%），同时CLIP-Score超越所有基线。消融实验证实，多源混合训练与Inf3DLayout子集提供的大量小物体信息是提升生成细节复杂度的关键因素。

> **注意**：本文未提供会议/期刊发表信息，数据集中部分描述由GPT-4o生成并经人工抽检，可能存在少量标注噪声。



### 问题背景

三维室内场景生成是计算机视觉与图形学中的核心任务之一，其目标是根据给定条件自动合成具有合理空间关系的室内物体布局。近年来，文本条件的三维场景合成逐渐兴起，使得用户能够通过自然语言描述来驱动场景生成，大幅降低了专业建模的门槛。然而，该方向的发展严重受限于现有数据集的规模与质量。

### 现有数据集的结构性缺口

当前用于三维室内布局生成的数据集存在三个相互关联的瓶颈，共同制约了文本驱动模型的性能上限：

**第一，数据来源单一，场景多样性不足。** 现有数据集大多仅依赖单一数据源，如仅使用专业CAD设计（如3D-FRONT）或仅来自真实扫描。单一来源导致场景风格、复杂度与物体组成高度同质化，模型难以学习到泛化的空间组织模式。例如，专业设计场景往往布局规整但缺乏生活气息，而真实扫描场景虽自然但物体标注稀疏、噪声较大。

**第二，小物体覆盖率极低，场景细节匮乏。** 如表1所示，3D-FRONT数据集中小物体占比仅为0.2%，这意味着绝大多数训练样本中几乎不存在台灯、书籍、装饰品等细节物件。这直接导致生成模型倾向于输出仅有大家具的“空壳”场景，缺乏真实室内环境的丰富性与层次感。

**第三，缺乏结构化文本描述，语义对齐困难。** 现有数据集或完全不具备文本标注，或仅提供简单的场景类别标签。这使文本条件的布局生成模型难以学习文本语义与空间配置之间的精细映射关系——模型无法理解“床的左侧放置一个床头柜”这类包含空间关系与物体属性的复合指令。即便使用CLIP等视觉-语言模型进行弱监督，缺乏显式的结构化文本配对仍会导致生成结果与输入提示之间出现语义漂移。

### 核心动机

上述三个缺口的叠加效应形成了一个恶性循环：数据规模小且多样性低，导致模型无法学习复杂空间模式；小物体缺失使生成场景细节贫乏；文本标注匮乏则切断了语义控制通道。本文的核心动机正是同时打破这三个瓶颈——通过构建**多源融合、小物体丰富、结构化文本配对**的大规模数据集，为文本条件的三维室内布局生成提供更高质量的训练信号，从而推动模型在场景丰富度、语义对齐度和可控性上实现质的飞跃。



## 核心方法与创新机理

M3DLayout的核心创新不在于提出全新的生成模型架构，而在于**构建了首个大规模、多源、多层级文本标注的3D室内布局数据集**，并通过该数据集驱动文本条件布局生成模型实现质的跃迁。其创新本质可归结为三个相互耦合的“changed slots”，分别针对现有工作的数据瓶颈、标注瓶颈和细节瓶颈。

### 数据来源：从单一到多源互补

现有3D室内场景数据集普遍依赖单一来源——要么是专业CAD设计（如3D-FRONT），要么是真实扫描（如Matterport3D），要么是程序化生成。这种单一性导致模型学到的空间模式存在系统性偏差：专业设计数据布局规整但缺乏真实感，真实扫描数据场景多样但规模受限，程序化生成数据灵活但往往缺乏语义合理性。

M3DLayout的核心突破在于**将三种互补数据源首次系统整合**：来自**3D-FRONT**的专业设计布局提供规整的空间组织范式，来自**Matterport3D**的真实扫描场景注入生活化的不规则性与多样性，而来自**Infinigen**的程序化生成场景则通过大规模合成（经房间划分与过滤后形成Inf3DLayout子集）填补了前两者在场景数量和物体密度上的不足。三者融合后，数据集规模达到21,367个布局、超过433k个物体实例，在场景数量、物体多样性和布局复杂度上均远超现有数据集（Table 2）。

消融实验（Table 7）直接验证了这一设计的因果效应：仅使用单一数据源训练时，模型在对应测试源上表现最优，但跨源泛化能力显著下降；而多源混合训练在多个测试源上取得了最佳平衡。这表明多源融合不仅增加了数据量，更关键的是提供了**互补的空间模式信号**，迫使模型学习更具泛化性的布局表征。

### 文本标注：从无标注到三层结构化描述

此前的3D布局数据集要么完全没有文本标注，要么仅有简单的类别标签或场景类型标识，无法支撑文本条件生成模型的训练。M3DLayout首次为每个布局提供了**三层结构化文本描述**：

- **全局场景描述（Global Scene Description）**：概括房间类型、整体风格、空间尺寸及大致的家具配置。
- **大家具描述（Large Furniture Description）**：刻画沙发、床、餐桌等大型家具之间的相对空间关系（如“床位于房间中央，左侧放置床头柜”）。
- **小物体描述（Small Object Description）**：精细描述台灯、抱枕、书籍等小物体的摆放位置与附着关系（如“台灯放置于床头柜上”）。

这三层描述并非简单的自然语言标注，而是通过**规则模板与VLM多视图生成相结合**的混合流水线构建：对3D-FRONT场景，系统提取物体包围盒与语义标签，检测空间关系后通过预定义模板生成结构化文本；对Matterport3D和Inf3DLayout场景，则渲染俯视图、侧视图及小物体特写图，由GPT-4o多视图理解后生成描述。所有自动生成的描述均经过**抽样人工审核**以确保质量。

这种多层级结构的因果价值在于：它使文本条件生成模型能够**在不同粒度上建立文本-空间的对齐**。全局描述引导场景的整体组织，大家具描述约束主体布局的合理性，小物体描述则驱动细节的丰富性——三者共同作用，使得模型生成的布局在文本对齐度和场景丰富度上显著超越仅使用简单文本条件的基线（Figure 4，Figure 6）。

### 小物体覆盖：从被忽略到核心关注

现有数据集中小物体（如装饰品、小型家电、桌面物品）的占比极低——3D-FRONT中小物体仅占0.2%，几乎可以忽略。这导致现有模型生成的布局往往只有“骨架”（大型家具），缺乏“血肉”（小物体），场景细节严重匮乏。

M3DLayout通过Inf3DLayout子集从根本上改变了这一局面：该子集包含13,929个场景、373,136个物体实例，其中**小物体占比高达68.5%**（Table 1）。这一数据分布的革命性变化直接转化为模型能力的跃迁：消融实验表明，缺失Inf3DLayout子集将导致生成布局趋于简单，而包含该子集的完整M3DLayout训练使模型能够生成细节更丰富、更接近真实场景复杂度的布局。

### 方法谱系与知识库定位

本文提出的DIFF-M3DLayout和AR-M3DLayout在方法架构上并未引入全新的生成范式，而是分别沿用了**DiffuScene**（Tang et al., CVPR 2024）的扩散去噪框架和经典的自回归Transformer架构。其真正的方法论贡献在于**将多源多层级文本-布局配对数据系统性地注入现有架构**，验证了“数据驱动”路线在3D布局生成任务上的巨大潜力。

具体而言，DIFF-M3DLayout在扩散模型的反向过程中引入文本条件$c^{\mathrm{text}}$：

$$p_{\theta}(\boldsymbol{x}_{t-1} \mid \boldsymbol{x}_t, c^{\mathrm{text}}) = \mathcal{N}(\boldsymbol{x}_{t-1}; \mu_{\theta}(\boldsymbol{x}_t, t, c^{\mathrm{text}}), \boldsymbol{\Sigma}_{\theta}(\boldsymbol{x}_t, t))$$

通过噪声预测目标训练：

$$\mathcal{L}_{\mathrm{DM}} = \mathbb{E}_{{x}_0, {c}^{\mathrm{text}}, t, \epsilon} \left[ \Vert \epsilon - \epsilon_{\theta}({x}_t, t, {c}^{\mathrm{text}}) \Vert_2^2 \right]$$

AR-M3DLayout则将布局生成分解为物体序列的条件概率连乘：

$$p_{\theta}(x \mid c^{\mathrm{text}}) = \prod_{i=1}^{N} p_{\theta}(o_i \mid o_{<i}, c^{\mathrm{text}})$$

其中每个物体$o_i$表示为一个带语义类别、中心坐标、尺寸和偏航角的有向包围盒：

$$o_i = (c_i, x_i, y_i, z_i, w_i, h_i, d_i, \theta_i)$$

这两种架构在M3DLayout数据集上训练后，均展现出远超基线的性能：DIFF-M3DLayout在Inf3DLayout基准上的FID较DiffuScene降低31.27（降幅约30%），AR-M3DLayout的FID更低至57.90（降幅约43%），同时CLIP-Score超越所有基线（Table 3）。这表明M3DLayout的数据创新具有架构通用性——无论是扩散模型还是自回归模型，均能从多源多层级文本标注中显著获益。

**与现有工作的关系**：相较于仅关注模型架构改进的**InstructScene**（Lin and Mu, 2024），M3DLayout从数据端切入，解决了“巧妇难为无米之炊”的根本问题；相较于依赖单一数据源的**DiffuScene**，M3DLayout通过多源融合和结构化文本标注，使相同架构的模型获得了质的性能提升。这一“数据驱动”路线为3D室内场景生成领域提供了新的方法论范式。



M3DLayout 的整体框架围绕一个核心目标构建：**将多源三维室内布局与多层级结构化文本描述配对**，为文本条件的布局生成模型提供大规模、高多样性的训练基础。该框架由两条并行主线交织而成——数据集的构建流水线与下游生成模型的训练范式。

### 数据集构建流水线

数据集构建遵循“多源摄入→布局规整与过滤→分层文本标注→人工质量审查”的四阶段流水线（Figure 2）。

![[assets/figures/papers/paper_list_l2237_https_arxiv_org_abs_2509_23728/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline for Constructing the M3DLayout Dataset. Our framework integrates multi-source data, including the professional designs dataset 3D-FRONT, real-world scans from Matterport3D, and procedurally generated scenes from Infinigen. The construction process involves: meticulously generating, partitioning, and filtering layouts to create the Inf3DLayout subset; performing template-based rules to produce formatted text; and employing global and local rendering for vision-language models (VLM) to produce structured descriptions. This pipeline results in a large-scale, richly-annotated text-3D layout paired dataset*

**多源数据摄入**是框架的起点。M3DLayout 从三类互补数据源收集原始布局：专业 CAD 设计数据集 **3D-FRONT**、真实环境扫描数据集 **Matterport3D**，以及基于 **Infinigen** 的程序化生成场景。这三类数据源在场景风格、物体密度和布局复杂度上形成互补——3D-FRONT 提供规整的专业设计布局，Matterport3D 带来真实世界的空间噪声与多样性，Infinigen 则贡献了包含大量小物体的高复杂度场景（小物体占比达 68.5%，见表 1）。

**布局划分与过滤**模块专门针对 Infinigen 的原始输出进行处理。由于 Infinigen 生成的是完整房屋而非独立房间，框架需要对其进行房间划分，并剔除布局异常（如物体严重堆叠或空间关系不合理）的样本，最终形成 **Inf3DLayout** 子集（13,929 个场景，373,136 个物体实例）。

**分层文本标注**是框架最具创新性的模块，其输出直接决定了模型可学习的语义粒度。M3DLayout 采用三层结构化描述架构：
- **全局场景描述**：概括房间类型、整体风格与空间组织；
- **大家具描述**：刻画大型家具（如床、沙发、餐桌）的类别、位置及相对空间关系；
- **小物体描述**：细粒度地记录小型摆件（如枕头、花瓶、遥控器）的布置信息。

针对不同数据源，标注策略有所分化。对于 3D-FRONT，框架采用**基于模板的规则方法**：提取物体级包围盒与语义标签，检测物体间的相对空间关系（如“左侧”“上方”“相邻”），再通过预定义模板将结构化信息合成为连贯的自然语言描述。对于 Matterport3D 和 Inf3DLayout，则采用**VLM 多视图生成方法**：渲染场景的俯视图、侧视图以及小物体特写图像，交由 GPT-4o 模型根据多视图信息生成结构化文本描述。最后，所有自动生成的标注均经过**抽样人工审查**，以保障标注质量。

### 问题形式化与生成模型

在数据集之上，框架将文本条件的室内布局生成形式化为一个条件生成问题。每个 3D 物体被表示为一个带语义类别、中心坐标、尺寸和偏航角的有向包围盒：

$$o _ { i } = ( c _ { i } , x _ { i } , y _ { i } , z _ { i } , w _ { i } , h _ { i } , d _ { i } , \theta _ { i } )$$

给定文本条件 $c^{\mathrm{text}}$，目标是生成由 $N$ 个物体组成的场景布局 $\{o_1, o_2, \ldots, o_N\}$。

框架提供了两种互补的生成范式：

**DIFF-M3DLayout** 基于扩散模型，遵循去噪扩散概率框架（与 **DiffuScene**（Tang et al., CVPR 2024）类似）。其反向去噪过程以文本为条件：

$$p _ { \theta } ( \boldsymbol { x } _ { t - 1 } \mid \boldsymbol { x } _ { t } , c ^ { \mathrm { t e x t } } ) = \mathcal { N } ( \boldsymbol { x } _ { t - 1 } ; \mu _ { \theta } ( \boldsymbol { x } _ { t } , t , c ^ { \mathrm { t e x t } } ) , \boldsymbol { \Sigma } _ { \theta } ( \boldsymbol { x } _ { t } , t ) )$$

训练目标为标准的噪声预测损失：

$$\mathcal { L } _ { \mathrm { D M } } = \mathbb { E } _ { { x } _ { 0 } , { c } ^ { \mathrm { t e x t } } , { t } , \epsilon } \left[ \Vert \epsilon - \epsilon _ { \theta } ( { x } _ { t } , { t } , { c } ^ { \mathrm { t e x t } } ) \Vert _ { 2 } ^ { 2 } \right]$$

**AR-M3DLayout** 则采用自回归 Transformer，将布局生成分解为物体序列的条件概率连乘：

$$p _ { \theta } ( x \mid c ^ { \mathrm { t e x t } } ) = \prod _ { i = 1 } ^ { N } p _ { \theta } ( o _ { i } \mid o _ { < i } , c ^ { \mathrm { t e x t } } )$$

两种范式共享同一套 M3DLayout 数据集进行训练，但生成机制不同：扩散模型一次性去噪出完整布局，自回归模型则逐个物体地构建场景，后者在文本-布局对齐（CLIP-Score）上表现更优。

### 数据流与模块耦合

框架的数据流可概括为：**多源原始布局** → **布局清洗与统一表示** → **多层级文本标注** → **文本-布局配对数据集** → **条件生成模型训练**。其中，文本标注的质量直接决定了生成模型的上界——消融实验表明，缺失 Inf3DLayout 子集（即缺失大量小物体及其对应描述）会导致生成布局趋于简单，跨源泛化能力显著下降（见表 7）。这一因果链验证了框架设计的核心洞察：**多源数据与结构化文本的耦合，是模型学习从全局场景组织到细粒度物体布置的关键使能因素**。



### 物体表示

M3DLayout 将每个 3D 物体统一表示为一个带语义类别的有向包围盒：

$$o _ { i } = ( c _ { i } , x _ { i } , y _ { i } , z _ { i } , w _ { i } , h _ { i } , d _ { i } , \theta _ { i } )$$

其中 $c_i$ 为语义类别，$(x_i, y_i, z_i)$ 为中心坐标，$(w_i, h_i, d_i)$ 为包围盒尺寸，$\theta_i$ 为偏航角。这一简洁的参数化形式是整个布局生成框架的基础，所有后续模块均在此表示上操作。

### 扩散模型（DIFF-M3DLayout）

DIFF-M3DLayout 沿用了与 **DiffuScene**（Tang et al., CVPR 2024）类似的去噪扩散概率框架，核心差异在于训练数据源——完整 M3DLayout 数据集提供的多源布局与结构化文本配对。

**反向扩散过程**以文本条件 $c^{\mathrm{text}}$ 为引导，从纯噪声逐步恢复布局参数：

$$p _ { \theta } ( \boldsymbol { x } _ { t - 1 } \mid \boldsymbol { x } _ { t } , c ^ { \mathrm { t e x t } } ) = \mathcal { N } ( \boldsymbol { x } _ { t - 1 } ; \mu _ { \theta } ( \boldsymbol { x } _ { t } , t , c ^ { \mathrm { t e x t } } ) , \boldsymbol { \Sigma } _ { \theta } ( \boldsymbol { x } _ { t } , t ) )$$

其中 $\mu_\theta$ 为参数化均值函数，$\boldsymbol{\Sigma}_\theta$ 为协方差矩阵，$t$ 为扩散时间步。

**训练目标**采用标准的噪声预测损失：

$$\mathcal { L } _ { \mathrm { D M } } = \mathbb { E } _ { { x } _ { 0 } , { c } ^ { \mathrm { t e x t } } , { t } , \epsilon } \left[ \Vert \epsilon - \epsilon _ { \theta } ( { x } _ { t } , { t } , { c } ^ { \mathrm { t e x t } } ) \Vert _ { 2 } ^ { 2 } \right]$$

模型 $\epsilon_\theta$ 学习预测在时间步 $t$ 加入的噪声 $\epsilon$，从而在推理阶段通过迭代去噪生成符合文本描述的布局。

### 自回归模型（AR-M3DLayout）

AR-M3DLayout 采用自回归 Transformer 架构，将场景布局生成分解为物体序列的条件概率连乘：

$$p _ { \theta } ( x \mid c ^ { \mathrm { t e x t } } ) = \prod _ { i = 1 } ^ { N } p _ { \theta } ( o _ { i } \mid o _ { < i } , c ^ { \mathrm { t e x t } } )$$

其中 $x = \{o_1, o_2, \ldots, o_N\}$ 为场景中所有物体的序列，$o_{<i}$ 表示已生成的前 $i-1$ 个物体。模型以文本条件 $c^{\mathrm{text}}$ 为全局引导，依次预测每个物体的类别、位置、尺寸和朝向。

两种生成范式形成互补：扩散模型擅长全局空间一致性的建模，自回归模型则在序列化决策中天然支持可变长度的场景生成。在 Inf3DLayout 基准上，AR-M3DLayout 取得了更优的 FID（57.90 vs. DIFF-M3DLayout 的 70.85），而 DIFF-M3DLayout 在跨数据集泛化方面表现更稳健（见 Table 3）。

### 结构化文本条件注入

无论是扩散模型还是自回归模型，文本条件 $c^{\mathrm{text}}$ 均来自 M3DLayout 的三层结构化描述（全局场景描述、大家具描述、小物体描述）。这一多层级语义信息的注入是模型能够生成细粒度布局的关键——尤其是 Inf3DLayout 子集提供的 68.5% 小物体占比（Table 1），使模型得以学习在文本驱动下布置台灯、靠垫等小物件的复杂空间模式。



## 实验与关键发现

### 主要定量结果

为验证M3DLayout数据集对文本条件布局生成的有效性，作者基于扩散模型与自回归模型两种主流范式，分别构建了**DIFF-M3DLayout**与**AR-M3DLayout**，并在多源测试集上进行了系统评估。核心结论是：在M3DLayout上训练的模型在布局真实度与文本对齐度两个维度上均显著超越现有基线。

在Inf3DLayout测试子集上，DIFF-M3DLayout的FID达到**70.85**，较**DiffuScene**（Tang et al., CVPR 2024）的102.12降低**31.27**（降幅约30.6%）；KID同样从75.49降至50.94，降幅达32.5%（Table 3）。这一差距直接反映了M3DLayout中Inf3DLayout子集带来的关键增益——该子集包含13,929个场景与373,136个物体实例，其中小物体占比高达**68.5%**（Table 1），而传统数据集（如3D-FRONT）中小物体占比仅0.2%。丰富的细粒度物体分布使模型能够学习更复杂的空间配置，从而生成更接近真实分布的布局。

![[assets/figures/papers/paper_list_l2237_https_arxiv_org_abs_2509_23728/figures/006_Table_3.jpg]]
*Table 3: Quantitative comparison. Lower FID/KID (×0.001) and higher Clip Score indicate better synthesis quality. FID and KID are computed with respect to the real layouts from 3D-FRONT, Matterport, and Inf3DLayout. We train InstructScene following the public implementation. The optimal result is shown in bold, and the sub-optimal result is shown with an underline*

![[assets/figures/papers/paper_list_l2237_https_arxiv_org_abs_2509_23728/figures/004_Table_1.jpg]]
*Table 1: Quantitative analysis of three data sources (3D-FRONT, Matterport3D, Inf3DLayout) in M3DLayout*

自回归模型AR-M3DLayout在Inf3DLayout上的FID进一步降至**57.90**，较DiffuScene降低44.22（降幅43.3%），同时CLIP-Score达到**0.2026**，超越所有基线（Table 3）。这表明自回归分解在捕捉物体间长程依赖关系上具有优势，尤其适合M3DLayout中高密度、多类别物体的场景。

在Matterport3D真实扫描子集上，DIFF-M3DLayout同样取得10%–32%的FID/KID改善（Table 3）。值得注意的是，在3D-FRONT子集上，M3DLayout训练模型的FID/KID反而劣于仅在3D-FRONT上训练的DiffuScene。这一“退化”现象并非模型能力不足，而是因为3D-FRONT场景本身物体密度较低、布局相对规整，而M3DLayout的多源混合训练使模型倾向于生成更丰富、更接近真实世界复杂度的布局，与3D-FRONT的简单分布产生系统性偏移（Table 7）。这一失败模式在消融实验中得到了明确验证。

![[assets/figures/papers/paper_list_l2237_https_arxiv_org_abs_2509_23728/figures/015_Table_7.jpg]]
*Table 7: Ablation studys of diffusion-based methods trained on different datasets. Lower FID/KID (×0.001) and higher Clip Score indicate better synthesis quality. FID and KID are computed with respect to the real layouts from 3D-FRONT, Matterport, and Inf3DLayout*

### 消融实验：数据源贡献分解

Table 7的消融实验揭示了各数据源对模型性能的因果贡献。当仅使用单一数据源训练时，模型在对应测试源上取得最优FID/KID，但跨源泛化能力急剧下降。例如，仅用3D-FRONT训练时，在3D-FRONT测试集上FID为68.51，但在Inf3DLayout上飙升至142.36；仅用Inf3DLayout训练时，在Inf3DLayout上FID降至64.74，但在3D-FRONT上升至109.72。完整M3DLayout的多源混合训练在三个测试源上取得了最佳的整体平衡——这证实了多源互补策略对于提升模型泛化能力的关键作用。

进一步分析表明，Inf3DLayout子集是提升生成场景细节复杂度的决定性因素。缺失该子集时，模型生成的布局趋于简单，小物体布置的多样性和合理性显著下降。这一发现与Table 1中小物体占比数据形成因果闭环：高比例的小物体覆盖为模型提供了学习细粒度空间关系的充分监督信号。

### 定性分析与可控性

Figure 4展示了在卧室、餐厅、客厅三类场景上的生成对比。在相同文本提示下，M3DLayout训练的模型生成的布局包含更丰富的物体类别与更合理的空间配置，而DiffuScene和**InstructScene**（Lin and Mu, 2024）的生成结果则相对稀疏、细节匮乏。Figure 5进一步展示了密度可控性：通过微调提示文本中最后一句关于物体密度的描述，模型能够生成从低密度到高密度的渐变布局，表明结构化文本描述与布局空间之间存在可被模型捕捉的连续映射。

用户研究（Figure 6）从六个维度（文本匹配度MT、视觉质量VQ、场景丰富度SR、位置连贯性LC-P、朝向连贯性LC-O、总体偏好OP）对生成结果进行主观评价，M3DLayout训练的模型在所有维度上均优于DiffuScene和InstructScene，尤其在场景丰富度与文本匹配度上优势显著。

![[assets/figures/papers/paper_list_l2237_https_arxiv_org_abs_2509_23728/figures/009_Figure_6.jpg]]
*Figure 6: User case study results. The charts compare our method against DiffuScene and InstructScene across diverse rooms. Bars represent the average user score for six metrics: Match with Text (MT), Visual Quality (VQ), Scene Richness (SR), Layout Coherence (Position) (LC-P), Layout Coherence (Orientation) (LC-O), and Overall Preference (OP)*

### 生成效率

Table 5对比了各方法的生成效率。DIFF-M3DLayout在保持扩散模型生成质量优势的同时，推理时间与DiffuScene相当；AR-M3DLayout虽然生成质量更优，但自回归序列解码导致推理时间略长，这是自回归范式的固有取舍。

### 关键图表索引

- **Table 3**：主要定量结果，包含FID/KID/CLIP-Score的完整对比。
- **Table 7**：消融实验，展示不同数据源组合对模型性能的影响。
- **Table 1**：三数据源的定量特征，重点关注小物体占比差异。
- **Figure 4**：定性生成对比，直观展示细节丰富度差异。
- **Figure 5**：密度可控性演示，验证文本-布局的连续映射能力。
- **Figure 6**：用户研究结果，六维主观评价的量化对比。

![[assets/figures/papers/paper_list_l2237_https_arxiv_org_abs_2509_23728/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative comparison of different methods on diverse room types. From top to bottom: bedroom, dining room, and living room generation results. Each row shows the input prompt and generated layouts from DiffuScene, InstructScene, and our method. Trained on the M3DLayout dataset, our method produces richer layout details from text descriptions*

![[assets/figures/papers/paper_list_l2237_https_arxiv_org_abs_2509_23728/figures/008_Figure_5.jpg]]
*Figure 5: Density controllability in layout generation with different input texts. The first row presents input prompts for our layout generation model, showcasing variations in objects density from low to high, with minor changes in the last sentence. The second row illustrates the corresponding output results generated by our model, which adapt based on the prompt density*

### 补充图表

![[assets/figures/papers/paper_list_l2237_https_arxiv_org_abs_2509_23728/figures/005_Table_2.jpg]]
*Table 2: Comparisons between existing 3D indoor scene datasets. For the column of Layout Collecton, RS denotes real scanned and PD denotes professionally designed .For the column of Variation in Object Sizes, “N/A” denotes “not available”, “L” and “S” denote Large and Small objects in the scene, respectively*

![[assets/figures/papers/paper_list_l2237_https_arxiv_org_abs_2509_23728/figures/011_Table_4.jpg]]
*Table 4: DiffuScene and Our DIFF-M3DLayout*

![[assets/figures/papers/paper_list_l2237_https_arxiv_org_abs_2509_23728/figures/012_Table_5.jpg]]
*Table 5: Comparison of generation efficiency with state-of-the-art methods*

![[assets/figures/papers/paper_list_l2237_https_arxiv_org_abs_2509_23728/figures/013_Table_6.jpg]]
*Table 6: M3DLayout with 3D-FRONT comparison*

![[assets/figures/papers/paper_list_l2237_https_arxiv_org_abs_2509_23728/figures/019_Figure_11.jpg]]
*Figure 11: Our generated layouts exhibit strong adherence to the provided textual guidance*



## 定位与知识库关联

### 数据集层面的谱系定位

M3DLayout 的核心贡献在于构建了一个多源、多层级文本标注的 3D 室内布局数据集，其数据来源与现有数据集形成明确的互补与扩展关系。从数据构成来看，该数据集整合了三种性质迥异的来源：来自 **3D-FRONT** 的专业 CAD 设计、来自 **Matterport3D** 的真实世界扫描，以及基于 **Infinigen** 程序化生成的场景（经房间划分与过滤后形成 Inf3DLayout 子集）。这一多源融合策略直接回应了现有数据集的瓶颈——**Table 2** 的系统对比显示，此前的主流数据集如 3D-FRONT 和 ScanNet 在布局复杂度、小物体覆盖和结构化文本描述方面均存在明显短板。具体而言，3D-FRONT 尽管规模较大（6,813 个场景），但其小物体占比仅 0.2%，且缺乏结构化文本描述；Matterport3D 虽为真实扫描，但同样未提供文本标注。M3DLayout 通过引入 Inf3DLayout 子集（13,929 个场景，小物体占比 68.5%），将小物体的覆盖密度提升了两个数量级以上（**Table 1**），从而为模型学习细粒度物体布置提供了数据基础。

在文本标注层面，M3DLayout 的三层结构化描述（全局场景描述、大家具描述、小物体描述）填补了此前数据集的语义空白。与仅提供简单类别标签或场景级标题的现有数据集不同，M3DLayout 通过规则模板（针对 3D-FRONT）与 GPT-4o 多视图生成（针对 Matterport3D 和 Inf3DLayout）相结合的方式，为每个布局生成了包含空间关系、物体属性和布局逻辑的详细文本，并经过人工抽样审核以确保标注质量（**Figure 2**）。这种标注模式使得文本条件的布局生成模型能够学习从宏观空间组织到微观物体摆放的完整语义链。

### 生成模型的谱系定位

论文基于 M3DLayout 数据集训练了两类文本条件生成模型：基于扩散的 **DIFF-M3DLayout** 和基于自回归 Transformer 的 **AR-M3DLayout**，二者在方法论上分别沿袭了不同的技术路线。

DIFF-M3DLayout 的扩散框架与 **DiffuScene**（Tang et al., CVPR 2024）一脉相承，均采用去噪扩散概率模型进行场景布局生成。其核心差异在于训练数据的替换：DiffuScene 基于 3D-FRONT 训练，而 DIFF-M3DLayout 在 M3DLayout 的多源数据上训练，并引入了结构化文本作为条件信号。物体表示采用统一的 8 维有向包围盒参数化：

$$o _ { i } = ( c _ { i } , x _ { i } , y _ { i } , z _ { i } , w _ { i } , h _ { i } , d _ { i } , \theta _ { i } )$$

其中 $c_i$ 为语义类别，$(x_i, y_i, z_i)$ 为中心坐标，$(w_i, h_i, d_i)$ 为尺寸，$\theta_i$ 为偏航角。文本条件通过 $c^{\mathrm{text}}$ 注入反向扩散过程：

$$p _ { \theta } ( \boldsymbol { x } _ { t - 1 } \mid \boldsymbol { x } _ { t } , c ^ { \mathrm { t e x t } } ) = \mathcal { N } ( \boldsymbol { x } _ { t - 1 } ; \mu _ { \theta } ( \boldsymbol { x } _ { t } , t , c ^ { \mathrm { t e x t } } ) , \boldsymbol { \Sigma } _ { \theta } ( \boldsymbol { x } _ { t } , t ) )$$

训练目标为标准的噪声预测损失：

$$\mathcal { L } _ { \mathrm { D M } } = \mathbb { E } _ { { x } _ { 0 } , { c } ^ { \mathrm { t e x t } } , { t } , \epsilon } \left[ \Vert \epsilon - \epsilon _ { \theta } ( { x } _ { t } , { t } , { c } ^ { \mathrm { t e x t } } ) \Vert _ { 2 } ^ { 2 } \right]$$

AR-M3DLayout 则采用自回归生成范式，将布局生成分解为物体序列的条件概率连乘：

$$p _ { \theta } ( x \mid c ^ { \mathrm { t e x t } } ) = \prod _ { i = 1 } ^ { N } p _ { \theta } ( o _ { i } \mid o _ { < i } , c ^ { \mathrm { t e x t } } )$$

这种序列化生成方式天然适合捕捉物体间的空间依赖关系，尤其在多物体、高密度的 Inf3DLayout 场景中展现出更强的建模能力。

另一相关基线 **InstructScene**（Lin and Mu, 2024）采用指令驱动范式，但在 M3DLayout 的复杂场景上表现显著弱于本文方法——其在 Inf3DLayout 上的 FID 高达 159.27（×0.001），远高于 DIFF-M3DLayout 的 70.85（**Table 3**），说明单纯的指令跟随机制难以处理大规模、细粒度的室内布局生成任务。

### 适用边界与局限

M3DLayout 数据集及其配套模型在以下场景中展现出明确的适用性优势：（1）需要高密度小物体布置的复杂室内场景生成；（2）文本驱动的布局可控生成，尤其是对物体密度和空间关系的精细控制（**Figure 5** 展示了通过微调文本中最后一句即可实现从低密度到高密度的连续控制）；（3）跨风格、跨来源的场景合成，多源训练使模型具备一定的泛化能力。

然而，该方法存在若干明确的局限：

**分布外泛化的退化**。消融实验（**Table 7**）揭示了一个关键现象：当仅在单一数据源（如 3D-FRONT）上训练时，模型在该源上达到最优 FID/KID，但跨源泛化能力显著下降。完整 M3DLayout 的多源混合训练在多个测试源上取得了最佳平衡，但这种平衡是以牺牲单源最优性能为代价的。这一发现暗示多源数据的分布差异可能导致模型学习到某种“折中”表示，而非对每个分布的最优拟合。

**简单场景上的过生成倾向**。论文明确指出，在简单布局（如 3D-FRONT 的低物体密度场景）上，模型倾向于生成超过真实场景复杂度的布局，导致 FID/KID 指标劣化。这表明模型从 Inf3DLayout 的高密度数据中习得的“丰富性偏好”在简单场景上反而成为偏差源，暴露出当前训练策略在场景复杂度校准方面的不足。

**标注噪声的残余风险**。尽管采用了规则模板、GPT-4o 多视图生成和人工抽样审核的三重质量保障，但面对 21,367 个布局的海量标注规模，仍可能存在少量标注噪声。论文对此有清醒认知，但未提供定量的标注质量评估指标（如标注者间一致性系数），这一点需要读者注意。

**评估范式的局限**。目前基准仅评估布局级生成质量（FID、KID、CLIP-Score），尚未端到端地与最终 3D 网格/纹理生成联合验证。这意味着布局层面的改进能否有效转化为最终视觉质量的提升，仍是一个开放问题。此外，CLIP-Score 的提升幅度相对有限（从 DiffuScene 的 0.1982 到 AR-M3DLayout 的 0.2026，仅提升约 2.2%），提示文本-布局对齐的度量方法本身可能需要进一步细化。

**计算效率的权衡**。**Table 5** 的生成效率对比显示，DIFF-M3DLayout 和 AR-M3DLayout 在推理速度上的表现需要结合具体应用场景评估。扩散模型的迭代去噪过程与自回归模型的序列生成过程在效率-质量权衡上各有侧重，论文未深入讨论这一维度的设计选择依据。

### 开放问题

1. **多源数据的最优融合策略**：当前采用简单的混合训练，消融实验已揭示单源最优与跨源泛化之间的张力。是否可以通过数据加权、域自适应或课程学习等策略，在保持跨源泛化能力的同时逼近单源最优性能？

2. **布局生成到完整 3D 场景的闭环**：M3DLayout 目前止步于布局级评估，如何将生成的布局与 3D 物体检索、放置和场景渲染管线无缝衔接，形成端到端的文本到 3D 场景生成系统，是下一步的关键工程挑战。

3. **标注质量的量化度量**：当前依赖人工抽样审核，缺乏系统性的标注质量报告。引入标注者间一致性、自动验证规则覆盖率等量化指标，将增强数据集的可信度。

4. **密度控制的形式化边界**：Figure 5 展示了令人印象深刻的密度可控性，但这种控制能力的上下界、对文本措辞的敏感性、以及在极端密度条件下的行为，均缺乏系统的量化刻画。



## 原文 PDF

![[paperPDFs/CVPR_2026/M3DLayout_A_Multi_Source_Dataset_of_3D_Indoor_Layouts_and_Structured_Descriptions_for_3D_Generation.pdf]]
