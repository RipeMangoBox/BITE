---
title: ChainHOI Joint based Kinematic Chain Modeling for Human Object Interaction Generation
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/ChainHOI_Joint_based_Kinematic_Chain_Modeling_for_Human_Object_Interaction_Generation.pdf
project_link: null
code_link: https://github.com/qinghuannn/ChainHOI
aliases:
- CJBKCMHOIG
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入显式 HOI 关节图与运动学链，通过 GST-GCN 在关节级别捕捉细粒度交互，并通过 KIM 在运动学链级别强制执行链内与链间协调，从而直接控制生成动作的真实性和语义一致性。
primary_logic: 真实的人物交互生成必须显式同时建模关节级别和运动学链级别的交互，前者直接刻画关节与物体的几何关系，后者确保生物力学可行的协调运动，二者结合才能产生自然流畅的 HOI 序列。
claims:
- ChainHOI 在 BEHAVE 上 FID 为 0.095，远低于 HOI-Diff 的 0.457，证明显式建模大幅提升运动质量。
- 去除 KIM 或 SCM 导致 FID 从 0.095 恶化至 0.184–0.400，证实关节级与链级模块的必要性。
- KIM 的注意力可视化显示模型能够自适应关注与物体交互的关节，验证运动学链建模的有效性。
- BEHAVE 上 FID↓ = 0.095±.001
---

# ChainHOI Joint based Kinematic Chain Modeling for Human Object Interaction Generation

> [!tip] 核心洞察
> 真实的人物交互生成必须显式同时建模关节级别和运动学链级别的交互，前者直接刻画关节与物体的几何关系，后者确保生物力学可行的协调运动，二者结合才能产生自然流畅的 HOI 序列。

| 字段 | 内容 |
|------|------|
| 中文题名 | ChainHOI：基于关节的运动学链建模用于文本驱动的人物交互生成 |
| 英文题名 | ChainHOI Joint based Kinematic Chain Modeling for Human Object Interaction Generation |
| 会议/期刊 | CVPR 2025 |
| Links |  [Code](https://github.com/qinghuannn/ChainHOI)|
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ChainHOI |
| Dataset | BEHAVE, OMOMO |

> [!tip] 效果简介
> - BEHAVE 上，FID↓ 0.095±.001 vs HOI-Diff: 0.457±.003 (-0.362)；R-Precision Top1↑ 0.435±.009 vs HOI-Diff: 0.295±.003 (+0.140)；OCD↓ 0.091±.001 vs HOI-Diff: 0.148±.003 (-0.057)。
> - OMOMO 上，FID↓ 0.112±.004 vs HOI-Diff: 0.480±.001 (-0.368)；R-Precision Top1↑ 0.264±.005 vs HOI-Diff: 0.114±.002 (+0.150)。

## 概要

文本驱动的人物交互（Human-Object Interaction, HOI）生成要求根据自然语言描述和物体几何，合成真实、语义一致的人体运动序列。该任务的核心瓶颈在于：现有方法将全身姿态隐含地编码为统一的令牌表示，未能显式捕捉关节与物体之间的几何语义关系，且缺乏运动学链级别的协调建模，导致生成的动作不自然、交互不真实。

针对这一问题，本文提出 **ChainHOI**，一种基于扩散模型的 HOI 生成方法。其核心洞察是：**真实的 HOI 生成必须同时显式建模关节级别和运动学链级别的交互**——前者直接刻画关节与物体的几何关系，后者确保生物力学可行的协调运动，二者结合才能产生自然流畅的交互序列。

ChainHOI 的方法定位如下：在关节级别，通过引入显式的 HOI 关节图和生成时空图卷积网络（GST-GCN），捕捉关节与物体间的细粒度交互；在运动学链级别，通过运动学感知交互模块（KIM）强制执行链内与链间协调。这一“关节级 + 链级”双级别显式建模的设计，使 ChainHOI 在方法谱系中区别于仅使用隐式姿态令牌的现有方案（如 **HOI-Diff**），也区别于仅依赖后处理校正的方法（如 HOI-Diff + AIC）。

实验结果表明，ChainHOI 在 BEHAVE 和 OMOMO 两个基准数据集上均显著优于现有方法。在 BEHAVE 数据集上，ChainHOI 的 FID 达到 **0.095**，相比 HOI-Diff 的 0.457 降低了 **0.362**；R-Precision Top1 达到 **0.435**，提升了 **0.140**；接触距离（OCD）和脚部滑动率（FSR）也分别大幅降低。在 OMOMO 数据集上，ChainHOI 同样取得了 FID **0.112** 和 R-Precision Top1 **0.264** 的最优结果。消融研究进一步证实，去除运动学感知交互模块或语义一致模块会导致 FID 从 0.095 恶化至 0.400，验证了双级别建模的必要性。用户研究也显示，ChainHOI 生成的动作在真实性和交互质量上获得了显著高于对比方法的偏好率。

值得注意的是，ChainHOI 仍存在若干局限：由于输入数据采用 SMPL 人体模型，缺少手指关节信息，手部与物体可能出现穿透；对于椅子等复杂物体，模型难以学习正确的接触点和接触距离。这些问题为后续研究指明了方向。

### 任务背景

文本驱动的人物交互（Human-Object Interaction, HOI）生成旨在根据自然语言描述与目标物体几何，合成真实、合理的人体与物体协同运动序列。该任务在具身智能、机器人规划、虚拟数字人等领域具有重要应用价值，但其本质挑战在于：人体拥有高度冗余的自由度，而物体在交互过程中约束了人体的运动模式，生成系统必须同时满足语义对齐、物理接触精确与生物力学可行性三个层面的要求。

### 现有方法及其瓶颈

近年来，基于扩散模型的运动生成方法（如 **MDM**）在纯人体运动生成上取得了显著进展。为适配 HOI 生成，研究者沿两条路径进行了扩展：

1. **拼接式适配**：将物体 6-DoF 轨迹与人体运动拼接为统一表示，从零训练扩散模型（如 **MDM\***），或利用双人运动生成框架将其中一人替换为物体（如 **PriorMDM\***）。这类方法缺乏对关节与物体之间几何语义关系的显式建模，导致交互精度不足。

2. **隐式令牌建模**：**HOI-Diff** 等方法将全身姿态隐含地编码为 Transformer 令牌，通过注意力机制隐式学习交互关系。然而，这种隐式表示无法捕捉关节级别的细粒度几何约束，更缺失运动学链（kinematic chain）级别的协调建模。

上述方法的共同瓶颈在于：**未能显式建模关节与物体之间的几何语义关系，且缺乏运动学链级别的协调机制**。其直接后果包括：生成的动作不自然（如关节穿透物体、接触距离过大）、语义一致性差（动作与文本描述不匹配），以及生物力学不可行（链内关节运动缺乏协调）。定量证据表明，HOI-Diff 在 BEHAVE 数据集上的 FID 高达 0.457，接触距离指标 OCD 为 0.148，与真实交互序列存在显著差距（见 Table 1）。

### 核心洞察与动机

真实的人物交互本质上受两个层次的约束：

- **关节级约束**：特定关节（如手部、脚部）需要与物体建立精确的空间关系，这要求模型能够显式表征关节与物体几何之间的交互。
- **运动学链级约束**：人体关节并非独立运动，而是通过骨骼连接形成运动学链（如上肢链、下肢链）。链内关节的协调运动决定了动作的流畅性，链间协调则保证全身姿态的平衡与合理。

基于此，本文提出 **ChainHOI**，核心动机是：**真实的人物交互生成必须同时显式建模关节级别和运动学链级别的交互**。前者通过 HOI 关节图直接刻画关节与物体的几何关系，后者通过运动学感知交互模块强制执行链内与链间协调，二者结合才能产生自然流畅的 HOI 序列。这一设计从根源上解决了现有方法“隐式编码、全局建模”的结构性缺陷，为高质量文本驱动 HOI 生成提供了新的范式。

## 核心方法与创新机理

ChainHOI 的核心创新在于首次从**关节级**和**运动学链级**两个层次显式建模人物交互，解决了现有方法将全身姿态隐式编码为令牌而无法捕捉关节与物体间细粒度几何语义关系的瓶颈。这一思路通过三个关键模块实现，形成了从局部接触到全局协调的完整建模链路。

### 1. 从隐式令牌到显式 HOI 关节图

现有文本驱动 HOI 生成方法（如 **HOI-Diff**）将人体姿态与物体位姿拼接后送入 Transformer，由模型隐式学习关节与物体的关系。ChainHOI 则设计了一个**HOI 关节图**（Figure 3），将物体作为独立节点，显式连接到八个潜在交互关节（双手、双脚、头部等），同时引入足部接触节点以防止足部滑动。这一图结构直接编码了“哪些关节可能与物体发生接触”的先验，使模型无需从高维令牌中隐式推断交互关系。

在此基础上，ChainHOI 提出**生成时空图卷积网络（GST-GCN）** 进行关节级交互建模。GST-GCN 包含两个分支：ST-GCN 捕捉短期时空依赖，语义一致模块（Semantic-consistent Module）建模长时语义一致性。两者输出通过线性投影融合：

$$\mathbf{y} = \operatorname{Linear}([\mathbf{z}^l; \mathbf{z}^s])$$

这一设计使模型能够在关节级别显式推理每个关节与物体的几何关系，而非依赖全局令牌的隐式编码。

### 2. 从无约束生成到运动学链协调

更关键的创新在于**运动学链级别的交互建模**。现有方法完全缺乏对肢体链结构的显式约束，导致生成的动作可能出现生物力学上不合理的姿态（如手臂穿透躯干、接触关节与非接触关节运动不协调）。

ChainHOI 定义了五条内部运动学链（脊柱、左臂、右臂、左腿、右腿）和一条**人-物交互链**（Figure 5）。交互链由物体节点和八个潜在交互关节组成，显式建模关节与物体的协调关系。每条链对应一个可学习的运动学链令牌。

运动学感知交互模块（KIM）通过两个解码器实现链级建模：
- **上下文感知解码器**：结构与语义一致模块相同，但以可学习令牌为查询，编码文本语义和物体几何上下文，为每条运动学链规划目标。
- **运动学感知解码器**：先通过自注意力实现链间信息交换（式 3），再通过掩码交叉注意力实现链内精细建模（式 4）——每个运动学链令牌仅关注其对应链内的关节令牌，掩码 $M$ 阻止跨链信息泄漏。

$$\mathrm{KT'} = \mathrm{SelfAtt}(q=KT, k=KT, v=KT)$$

$$\bar{\mathrm{KT}} = \mathrm{CrossAtt}(q=KT', k=JT, v=JT, \operatorname{mask}=M)$$

这一设计直接强制执行了“同一肢体链内的关节应协调运动，不同链之间通过自注意力交换全局信息”的物理约束。

### 3. 从单一扩散损失到接触感知辅助损失

ChainHOI 在标准扩散损失之外，引入两个辅助损失直接约束交互质量：
- **人体接触损失** $\mathcal{L}_h$：基于接触标签加权，最小化八个交互关节到真实物体网格的距离。
- **物体位姿损失** $\mathcal{L}_o$：显式约束预测物体 6-DoF 与真实值的 L2 距离。

$$\mathcal{L} = \mathcal{L}_{diff} + \lambda_1 \mathcal{L}_h + \lambda_2 \mathcal{L}_o$$

消融实验（Table 2）证实，去除 $\mathcal{L}_h$ 和 $\mathcal{L}_o$ 后接触质量指标 OCD 从 0.091 恶化至 0.278，物体几何信息对精确接触至关重要。

### 创新验证

消融实验（Table 2）提供了因果证据：同时移除 KIM 和 SCM 后，FID 从 0.095 飙升至 0.400，OCD 从 0.091 升至 0.170，证实双级别建模的不可替代性。仅移除 KIM 中的注意力掩码（即取消显式运动学链结构）也使 FID 升至 0.184，表明链结构的显式建模本身对运动质量有显著贡献。运动学感知解码器的注意力可视化（Figure 11）进一步显示，模型能自适应地对与物体交互的关节赋予更高注意力分数，验证了链级建模的有效性。

ChainHOI 是一个基于扩散模型的文本驱动人物交互生成框架，其核心设计思想是将交互建模从隐式全身姿态令牌提升为**关节级**与**运动学链级**的双层显式建模。整体架构由 N 个结构相同的块堆叠而成，每个块包含两个关键模块：**生成时空图卷积网络（GST-GCN）** 和 **运动学感知交互模块（KIM）**，分别负责关节级的细粒度交互建模和运动学链级的协调建模。

### 输入输出流

框架的输入由三部分组成：噪声化的 HOI 序列 $\mathbf{m}_t$、文本描述嵌入以及目标物体的几何特征。HOI 序列在关节级别表示，包含人体关节的 3D 位置和物体的 6-DoF 位姿。前向扩散过程按式 (1) 逐步向干净数据添加高斯噪声，直到时间步 $T$ 时变为纯噪声：

$$q ( \mathbf { m } _ { t } \mid \mathbf { m } _ { 0 } ) = \mathcal { N } ( \mathbf { m } _ { t } ; \sqrt { \bar { \alpha } _ { t } } \mathbf { m } _ { 0 } , ( 1 - \bar { \alpha } _ { t } ) \mathbf { I } )$$

输入首先经过投影层，将噪声序列、文本嵌入和物体几何特征（通过 PointNet 提取）映射到统一的特征维度。随后，这些特征依次流经 N 个处理块，每个块的输出作为下一个块的输入。最终，输出投影层将处理后的特征映射回原始的 HOI 序列空间，得到去噪后的预测序列。

### 块内模块关系

在每个处理块内部，数据流经两个串行的核心模块：

1. **GST-GCN（关节级建模）**：该模块以 HOI 关节图为输入。关节图的设计如 Figure 3 所示，物体节点连接到八个潜在交互关节（双手、双脚、头部等），并额外引入足部接触节点以防止足部滑动。GST-GCN 内部包含两个子模块：
   - **ST-GCN**：捕捉短期时空依赖关系。
   - **语义一致模块（Semantic-consistent Module）**：以文本嵌入为引导，通过交叉注意力建模长期语义一致性。
   
   两者的输出通过拼接和线性投影融合：
   $$\mathbf { y } = \operatorname { L i n e a r } ( [ \mathbf { z } ^ { l } ; \mathbf { z } ^ { s } ] )$$
   其中 $\mathbf{z}^l$ 为长时特征，$\mathbf{z}^s$ 为短时特征。

2. **KIM（运动学链级建模）**：该模块接收 GST-GCN 的输出，并引入可学习的运动学链令牌（Kinetic Chain Tokens, KT）。KIM 包含两个解码器：
   - **上下文感知解码器（Context-aware Decoder）**：结构与语义一致模块相同，但以可学习的运动学链令牌作为查询，融合文本和物体几何上下文，为每条运动学链规划交互目标。
   - **运动学感知解码器（Kinematic-aware Decoder）**：首先通过自注意力在运动学链令牌之间交换信息，实现链间建模：
     $$\mathrm { K T ^ { \prime } } = \mathrm { S e l f A t t } ( q { = } K T , k { = } K T , v { = } K T )$$
     然后通过掩码交叉注意力，使每个运动学链令牌仅关注其对应链内的关节令牌，实现链内精细建模：
     $$\bar { \mathrm { K T } } = \displaystyle \mathrm { C r o s s A t t } ( q = K T ^ { \prime } , k = J T , v = J T , \operatorname* { m a s k } = M )$$
     其中 $M$ 为预定义的运动学链掩码矩阵。运动学链设计如 Figure 5 所示，包含五条人体内部链（如左右臂链、左右腿链、躯干链）和一条人-物交互链，后者由物体节点和八个潜在交互关节组成。

### 特征融合

KIM 输出的运动学链令牌经过展平、全连接层投影和整形后，与模块输入特征 $\bar{\mathbf{y}}_i$ 拼接，再通过线性层投影回原始维度：
$$\hat { \mathbf { y } } _ { i } = \operatorname { L i n e a r } ( [ \mathbf { v } ^ { \prime \prime } ; \bar { \mathbf { y } } _ { i } ] )$$

这种设计确保了关节级特征和链级特征的有效融合，使模型既能捕捉局部关节与物体的几何关系，又能维持全局的运动学协调性。

### 训练损失

ChainHOI 的训练损失由三部分组成：
$$\mathcal { L } = \mathcal { L } _ { d i f f } + \lambda _ { 1 } \mathcal { L } _ { h } + \lambda _ { 2 } \mathcal { L } _ { o }$$
其中 $\mathcal{L}_{diff}$ 为标准扩散损失，$\mathcal{L}_h$ 为接触距离损失（约束八个交互关节到真实物体网格的最小距离），$\mathcal{L}_o$ 为物体位姿损失（约束预测物体 6-DoF 与真实值的 L2 距离）。消融实验证实，辅助损失 $\mathcal{L}_h$ 和 $\mathcal{L}_o$ 能显著改善物理合理性（PS）和接触距离（OCD），最佳权重为 $\lambda_1=2, \lambda_2=1$（Table 7）。

![[assets/figures/papers/paper_list_l1731_ChainHOI_Joint_based_Kinematic_Chain_Modeling_for_Human_Object_Interacti/figures/002_Figure_2.jpg]]
*Figure 2: Overview of ChainHOI. ChainHOI is a diffusion-based model with N identical blocks. Each block contains a Generative Spatiotemporal GCN (GST-GCN) and a Kinematics-based Interaction Module (KIM) to model interactions at the joint and kinetic chain levels. GST-GCN, comprising an ST-GCN and a Semantic-consistent Module, captures short- and long-term information while ensuring semantic consistency. KIM includes a Context-aware Decoder and a Kinematic-aware Decoder to capture HOI context (textual and object geometry) and to model intra- and inter-kinetic chain interactions. Input and output projection layers are omitted for clarity*

ChainHOI 的核心架构由两个互补的交互建模模块构成：**生成时空图卷积网络（GST-GCN）** 在关节级别显式捕捉细粒度交互，**运动学感知交互模块（KIM）** 在运动学链级别强制执行链内与链间协调。二者通过融合模块整合特征，共同驱动扩散去噪过程。

### 扩散框架

ChainHOI 基于扩散模型构建。给定干净的 HOI 序列 $\mathbf{m}_0$，前向过程逐步注入高斯噪声：

$$q(\mathbf{m}_t \mid \mathbf{m}_0) = \mathcal{N}(\mathbf{m}_t; \sqrt{\bar{\alpha}_t} \mathbf{m}_0, (1 - \bar{\alpha}_t) \mathbf{I}) \tag{1}$$

其中 $\bar{\alpha}_t$ 为累积噪声调度参数。去噪网络由 $N$ 个相同块堆叠而成，每块包含一个 GST-GCN 和一个 KIM（Figure 2）。

### 关节级交互建模：GST-GCN

GST-GCN 由两个子模块构成：

- **ST-GCN**：在 HOI 关节图上执行时空图卷积，捕捉关节与物体节点间的短期时空依赖。
- **语义一致模块（Semantic-consistent Module）**：以可学习令牌为查询，对 HOI 序列进行交叉注意力建模，捕获长时语义一致性。

两个子模块的输出通过拼接与线性投影融合回原始维度：

$$\mathbf{y} = \operatorname{Linear}([\mathbf{z}^l; \mathbf{z}^s]) \tag{2}$$

其中 $\mathbf{z}^l$ 为语义一致模块的长时特征，$\mathbf{z}^s$ 为 ST-GCN 的短时特征。

### 运动学链级交互建模：KIM

KIM 包含两个解码器：

- **上下文感知解码器（Context-aware Decoder）**：结构与语义一致模块相同，但以可学习的运动学链令牌（Kinematic Chain Tokens, KT）作为查询，编码文本与物体几何上下文，为每条运动学链规划交互目标。
- **运动学感知解码器（Kinematic-aware Decoder）**：实现链间与链内双重建模。

**链间建模**通过运动学链令牌之间的自注意力实现信息交换：

$$\mathrm{KT'} = \mathrm{SelfAtt}(q = KT, k = KT, v = KT) \tag{3}$$

**链内建模**通过掩码交叉注意力实现，每个运动学链令牌仅关注其对应链内的关节令牌（JT），掩码矩阵 $M$ 强制约束注意力范围：

$$\bar{\mathrm{KT}} = \mathrm{CrossAtt}(q = KT', k = JT, v = JT, \operatorname{mask} = M) \tag{4}$$

运动学链设计包含五条人体内部链（如左右臂链、左右腿链、躯干链）和一条人-物交互链。交互链由物体节点与八个潜在交互关节（双手、双肘、双脚、双膝）构成，显式建模关节与物体的协调关系（Figure 5）。

### 特征融合

KIM 输出的运动学链令牌 $\mathbf{v}' \in \mathbb{R}^{6 D_t}$ 经展平、全连接层投影、重塑为 $\mathbf{v}'' \in \mathbb{R}^{(J+2) \times D_t}$ 后，与模块输入 $\bar{\mathbf{y}}_i$ 拼接并线性投影回原始维度：

$$\hat{\mathbf{y}}_i = \operatorname{Linear}([\mathbf{v}''; \bar{\mathbf{y}}_i]) \tag{5}$$

此融合机制确保关节级与链级信息在每一层去噪块中协同作用。

### 训练损失

总损失由扩散损失与两个辅助损失加权构成：

$$\mathcal{L} = \mathcal{L}_{diff} + \lambda_1 \mathcal{L}_h + \lambda_2 \mathcal{L}_o \tag{8}$$

其中 $\lambda_1 = 2$，$\lambda_2 = 1$。

**人体接触损失** $\mathcal{L}_h$ 约束八个交互关节到真实物体网格的最小距离，按接触标签 $a_{i,k}$ 加权：

$$\mathcal{L}_h = \sum_{i=1}^{L} \sum_{k=1}^{8} a_{i,k} \cdot \mathcal{G}\big(\phi_h(H_{i,k}), \psi(O_i^{gt})\big) \tag{6}$$

其中 $\mathcal{G}$ 计算预测关节与真实物体网格间的最小距离平方，$\phi_h$ 提取关节位置，$\psi$ 提取物体网格面。

**物体位姿损失** $\mathcal{L}_o$ 直接约束预测物体 6-DoF 与真实值的 L2 距离：

$$\mathcal{L}_o = \sum_{i=1}^{L} \big\| \phi_o(O_i^{pred}) - \phi_o(O_i^{gt}) \big\|_2^2 \tag{7}$$

消融实验证实，去除 $\mathcal{L}_h$ 和 $\mathcal{L}_o$ 会显著恶化接触精度（OCD）和物理合理性（PS），验证了辅助损失对精确交互生成的必要性（Table 7）。

## 实验与关键发现

### 核心性能对比

ChainHOI 在 BEHAVE 和 OMOMO 两个主流 HOI 数据集上全面超越现有方法。Table 1 显示，在 BEHAVE 上 ChainHOI 的 FID 达到 **0.095**，相较 HOI-Diff 的 0.457 降低 0.362，降幅达 79.2%；R-Precision Top1 从 0.295 提升至 0.435，相对提升 47.5%。在接触质量指标上，OCD 从 0.148 降至 0.091，FSR 从 0.125 降至 0.063，表明生成的交互序列在接触精度和脚部滑动抑制方面均有显著改善。

![[assets/figures/papers/paper_list_l1731_ChainHOI_Joint_based_Kinematic_Chain_Modeling_for_Human_Object_Interacti/figures/006_Table_1.jpg]]
*Table 1: Quantitative evaluation of the BEHAVE [5] and OMOMO [32] test sets. We repeated evaluation 20 times to calculate the average results with a 95% confidence interval (denoted by ±). The best result is in bold, and the second best is underlined. The Average Inference Time (AIT) is the mean over 100 samples on an RTX 3090. We evaluate the AIT of methods only on the BEHAVE dataset. Affordance-guided Interaction Correction (AIC) [48] is a post-processing method*

在 OMOMO 数据集上，ChainHOI 同样保持领先：FID 为 0.112（HOI-Diff 为 0.480），R-Precision Top1 为 0.264（HOI-Diff 为 0.114），验证了方法在不同场景和物体类别下的泛化能力。

值得注意的是，ChainHOI 的平均推理时间（AIT）显著低于现有方法，这得益于其显式建模避免了隐式令牌带来的冗余计算。结合 AIC 后处理方法后，ChainHOI + AIC 在 BEHAVE 上 OCD 进一步降至 0.072，为全局最优。

### 消融实验：双级别建模的必要性

Table 2 的消融实验直接验证了关节级与运动学链级建模的关键作用：

![[assets/figures/papers/paper_list_l1731_ChainHOI_Joint_based_Kinematic_Chain_Modeling_for_Human_Object_Interacti/figures/010_Table_2.jpg]]
*Table 2: Ablation Studies on the BEHAVE datset*

- **去除 KIM 和 SCM**（即同时移除运动学链模块和语义一致性模块）：FID 从 0.095 恶化至 0.400，OCD 从 0.091 升至 0.170。这一剧烈退化证明双级别建模是 ChainHOI 性能的核心支柱。
- **去除 KIM 中的注意力掩码**（保留 KIM 结构但取消显式运动学链约束）：FID 升至 0.184，表明即使保留模块骨架，缺乏链结构的显式引导也会严重损害运动质量。
- **去除物体几何输入**：OCD 从 0.091 飙升至 0.278，证实物体几何信息对精确接触建模不可或缺。

Figure 8 的可视化消融结果进一步印证了定量发现：移除关键模块后，生成的交互序列出现明显的穿透、接触距离过大或动作不自然等问题。

![[assets/figures/papers/paper_list_l1731_ChainHOI_Joint_based_Kinematic_Chain_Modeling_for_Human_Object_Interacti/figures/009_Figure_8.jpg]]
*Figure 8: Visualization Results of Ablation Studies. Ablating specific modules degrades the quality of the generated results*

### 关节图与运动学链设计的消融

Table 5 比较了不同 HOI 关节图设计：与离散图或完全图相比，本文设计的 HOI 关节图在 FID、OCD 和 PS（物理合理性）上均更优，仅在 R-Top1 上略低于完全图。这表明精心设计的稀疏连接图在捕捉交互关节关系的同时，避免了冗余连接引入的噪声。

![[assets/figures/papers/paper_list_l1731_ChainHOI_Joint_based_Kinematic_Chain_Modeling_for_Human_Object_Interacti/figures/014_Table_5.jpg]]
*Table 5: Evaluations of different HOI graph designs on the BEHAVE dataset*

Table 6 探究了运动学链设计的影响：引入额外的人-物交互链（human-object chain）后，OCD 和 FID 均有明显改善，证实了将物体与八个潜在交互关节显式归入同一条运动学链进行建模的有效性。

### 损失函数与超参数敏感性

辅助损失 $L_h$ 和 $L_o$ 对接触质量和物体运动精度有显著贡献。Table 7 的敏感性分析显示，最佳权重配置为 $\lambda_1=2, \lambda_2=1$，此时 PS 和 OCD 达到最优平衡。过大的 $\lambda_1$ 会导致模型过度关注接触而牺牲运动多样性，过小则接触质量下降。

### 失败模式与局限性

Figure 10 展示了 ChainHOI 的两类典型失败案例：

1. **手部穿透**：由于输入数据使用 SMPL 人体模型，缺少手指关节信息，ChainHOI 无法精确建模手指姿态，导致手部与物体出现穿透。这是数据表征层面的固有限制。
2. **复杂物体接触距离过大**：对于椅子等具有复杂几何结构的物体，模型难以学习正确的接触点和合适的接触距离，生成的交互序列中接触部位与物体表面距离偏大。

此外，当前方法依赖 PointNet 从物体几何中提取特征，无法处理非刚性物体，限制了在可变形物体交互场景中的应用。

### 运动学链注意力的可解释性

Figure 11 可视化了运动学感知解码器（Kinematic-aware Decoder）中的注意力分数。结果表明，ChainHOI 能够自适应地关注与目标物体实际交互的关节（如“坐椅子”时关注髋部和膝部关节），而对相关性低的潜在交互关节分配较低的注意力权重。这从机制层面验证了运动学链建模的有效性——模型学会了在链级别识别与当前交互语义相关的关节子集。

![[assets/figures/papers/paper_list_l1731_ChainHOI_Joint_based_Kinematic_Chain_Modeling_for_Human_Object_Interacti/figures/025_Figure_11.jpg]]
*Figure 11: Visualization of attention scores in our Kinematic-aware Decoder. We present two examples to demonstrate that our ChainHOI can adaptively focus on the joints interacting with the target object. For other potential interaction joints that have low relevance to the target object, lower attention scores are assigned. The results show that our method effectively captures the relationship between the target object and the precise interaction joints*

### 用户研究

Figure 7 报告了 24 名参与者的偏好选择结果。ChainHOI 相对于 MDMfinetuned、HOI-Diff 等方法的偏好率均超过 70%，表明人类评估者一致认为 ChainHOI 生成的交互序列更加自然、真实且语义一致。

## 定位与知识库关联

### 核心瓶颈与因果机制

现有文本驱动的人物交互（HOI）生成方法面临一个根本性瓶颈：它们将全身姿态隐含地编码为统一的令牌表示，通过通用 Transformer 架构进行建模，未能显式捕捉关节与物体之间的几何语义关系。这种隐式建模导致两个层面的缺失——**关节层面**无法精确刻画手部、肘部等关键部位与物体的空间关系；**运动学链层面**缺乏对人体内部链（如手臂链、腿链）及人-物交互链的协调约束，导致生成的动作在生物力学上不可行、交互不真实。

ChainHOI 的核心因果旋钮在于**双级别显式建模**：通过引入显式 HOI 关节图与生成时空图卷积网络（GST-GCN），在关节级别捕捉细粒度交互；通过运动学感知交互模块（KIM），在运动学链级别强制执行链内与链间协调。这两个级别形成互补——前者直接刻画关节与物体的几何关系，后者确保生物力学可行的协调运动，二者结合才能产生自然流畅的 HOI 序列。

### 方法谱系定位

ChainHOI 处于文本驱动 HOI 生成这一新兴任务的方法谱系中。该任务要求同时生成人体运动序列和物体 6-DoF 轨迹，其难度远超纯人体运动生成。

**纯人体运动生成方法的适配**：早期工作尝试将纯人体运动生成模型迁移至 HOI 场景。**MDM**（Tevet et al., ICCV 2023）在 HOI 数据集上微调后仅生成人体运动，不涉及物体；**MDM\*** 将物体 6-DoF 与人体运动简单拼接后从零训练，但缺乏针对交互的结构化建模；**PriorMDM\*** 将双人运动生成模型中的一人替换为物体，本质仍是隐式建模。这些方法在 BEHAVE 上的 FID 普遍较高（如 MDM\* 为 0.634），反映了通用架构面对细粒度交互需求时的根本局限。

**专用 HOI 生成方法的演进**：**InterDiff** 扩展通用运动扩散模型为文本条件 HOI 生成，但仍使用隐式令牌表示；**CHOIS\*** 去除路径点条件后仅用文本和初始状态生成 HOI，但缺乏显式交互建模；**HOI-Diff** 是 ChainHOI 之前最具代表性的文本驱动 HOI 方法，使用隐式姿态令牌通过 Transformer 建模，在 BEHAVE 上 FID 为 0.457。然而，其隐式表示无法捕捉关节级别的交互细节，且缺乏运动学链协调机制。HOI-Diff + AIC 结合了 Affordance-guided Interaction Correction 后处理，在 OCD 上有所改善（0.072），但后处理无法从根本上解决生成质量问题。

**ChainHOI 的差异化贡献**：ChainHOI 在三个关键维度上突破了上述方法的局限：

| 建模维度 | 基线方法 | ChainHOI |
|---------|---------|----------|
| 关节级交互 | 隐式全身姿态令牌（Transformer） | 显式 HOI 关节图 + GST-GCN |
| 运动学链级交互 | 无 | KIM（上下文感知解码器 + 运动学感知解码器，含可学习链令牌与掩码注意力） |
| 训练损失 | 仅扩散损失 | 扩散损失 + 接触距离损失 $\mathcal{L}_h$ + 物体位姿损失 $\mathcal{L}_o$ |

### 证据强度与适用边界

**决定性证据**：Table 1 显示 ChainHOI 在 BEHAVE 上 FID 为 0.095，较 HOI-Diff 的 0.457 降低 79.2%；在 OMOMO 上 FID 为 0.112，较 HOI-Diff 的 0.480 降低 76.7%。R-Precision Top1 在两个数据集上分别提升 14.0 和 15.0 个百分点。消融实验（Table 2）证实：去除 KIM 和 SCM 后 FID 从 0.095 恶化至 0.400，去除 KIM 中的注意力掩码（即取消显式运动学链建模）使 FID 升至 0.184，去除物体几何输入使 OCD 从 0.091 升至 0.278。KIM 的注意力可视化（Figure 11）进一步表明模型能够自适应关注与物体交互的关节，验证了运动学链建模的有效性。

**适用边界**：ChainHOI 的显式建模依赖于 SMPL 人体模型的关节定义和 PointNet 提取的物体几何特征。当前方法在以下场景存在局限：
1. **手指级交互**：由于 SMPL 模型不包含手指关节信息，ChainHOI 无法精确建模手指姿态，导致手部与物体可能出现穿透（Figure 10a-b）。
2. **复杂物体接触**：对于椅子等复杂物体，模型难以学习正确的接触点和合适的接触距离（Figure 10c）。
3. **非刚性物体**：PointNet 特征提取方式无法处理可变形物体，限制了在衣物、软体等交互场景中的应用。

### 开放问题

1. **手指穿透消减**：如何在不依赖手指关节数据的情况下，通过接触约束或物理先验消减手部与物体的穿透？
2. **复杂物体泛化**：如何提升模型对复杂物体接触几何的学习能力，尤其是在训练数据有限时？是否需要引入更丰富的物体表示（如隐式场）？
3. **非刚性物体扩展**：ChainHOI 的几何提取方式能否扩展至非刚性物体？需要何种表达或网络结构来建模可变形交互？
4. **运动学链先验增强**：运动学链令牌是否可以赋予更明确的解剖学约束（如关节角度限制）或物理先验（如力矩平衡），以进一步提升生成的真实性？

## 原文 PDF

![[paperPDFs/CVPR_2025/ChainHOI_Joint_based_Kinematic_Chain_Modeling_for_Human_Object_Interaction_Generation.pdf]]
