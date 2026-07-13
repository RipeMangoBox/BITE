---
title: "Better Call SAL: Towards Learning to Segment Anything in Lidar"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/Better_Call_SAL_Towards_Learning_to_Segment_Anything_in_Lidar.pdf
code_link: https://github.com/nv-dvl/segment-anything-lidar
project_link: https://research.nvidia.com/labs/dvl/projects/sal
aliases:
- SSAL
- BCSTLSAL
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "利用SAM与CLIP等2D视觉基础模型生成伪标签，并通过Transformer解码器与CLIP token蒸馏，将2D知识迁移至3D激光雷达域，实现无需人工监督的零样本激光雷达分割。"
primary_logic: "通过类不可知分割与CLIP特征蒸馏解耦分割与识别，结合旨在处理部分伪标签的FrankenFrustum增强策略，SAL首次在无人工标注条件下实现了零样本激光雷达全景分割。"
claims:
- "使用伪标签训练的SAL在类不可知分割上可达完全监督模型91%的性能（62.8 vs 69.0 PQ），而伪标签仅覆盖14%的点云。"
- "SAL在零样本激光雷达全景分割上显著优于直接提升SAM掩码的基线（默认类别下33.1 vs 27.5 PQ）。"
- "语义蒸馏损失L_token成功将语义信息注入模型：线性探测实验中，使用L_token的模型PQ为33.1，而不使用时仅为20.0。"
- "DBSCAN替换策略有效提升伪标签质量，类不可知分割PQ由直接使用SAM掩码的46.0提升至48.7。"
---

# Better Call SAL: Towards Learning to Segment Anything in Lidar

> [!tip] 核心洞察
> 通过类不可知分割与CLIP特征蒸馏解耦分割与识别，结合旨在处理部分伪标签的FrankenFrustum增强策略，SAL首次在无人工标注条件下实现了零样本激光雷达全景分割。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SAL：面向激光雷达的通用目标分割 |
| 英文题名 | Better Call SAL: Towards Learning to Segment Anything in Lidar |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2403.13129) · [GitHub](https://github.com/nv-dvl/segment-anything-lidar) · [Project](https://research.nvidia.com/labs/dvl/projects/sal) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SAL (Segment Anything in Lidar) |
| Dataset | SemanticKITTI (Frustum Eval), SemanticKITTI (Full) |

> [!tip] 效果简介
> - SemanticKITTI (Frustum Eval) 上，PQ (类不可知分割) 为 70.7 (SAL)，对比 48.7 (SAM+DBS replace)，变化 +22.0。
> - SemanticKITTI (Frustum Eval) 上，PQ (零样本LPS, 默认类别) 为 33.1 (SAL)，对比 27.5 (SAM+DBS+CLIP)，变化 +5.6。
> - SemanticKITTI (Full) 上，PQ (零样本LPS, 默认类别) 为 24.8 (SAL)，对比 8.2 (SAM+DBS+CLIP)，变化 +16.6。

## 概要

激光雷达（Lidar）全景分割模型长期受限于预定义的固定类别词汇表，无法适应开放世界中动态变化的语义需求。与此同时，构建通用的三维分割模型面临一个根本性瓶颈：缺乏无需人工标注的大规模训练数据。**SAL**（Segment Anything in Lidar）正是在这一背景下提出的——它首次实现了无需任何人工监督的零样本激光雷达全景分割。

SAL的核心洞察在于**将分割与识别解耦**：利用2D视觉基础模型（SAM与CLIP）自动生成伪标签，再通过Transformer解码器与CLIP token蒸馏将2D知识迁移至3D激光雷达域。这一范式使得模型在测试时可通过任意文本提示进行零样本分类，而无需重新训练或微调。

在类不可知分割任务上，仅使用覆盖14%点云的伪标签训练的SAL，达到了完全监督模型**91%的性能**（62.8 vs 69.0 PQ）。在零样本激光雷达全景分割任务上，SAL在SemanticKITTI和nuScenes数据集上分别达到全监督基线的**42%**和**54%**，显著优于直接提升SAM掩码的基线方法。这些结果表明，通过蒸馏2D基础模型的知识，在3D领域实现通用、可提示的分割是可行的，为激光雷达感知从封闭集走向开放世界迈出了关键一步。



### 激光雷达全景分割的封闭世界困境

激光雷达（LiDAR）全景分割旨在对三维点云中的每个点同时进行实例分割和语义分类，是自动驾驶与机器人感知的核心任务。现有方法，如基于全监督学习的全景分割模型，虽然在固定类别词汇表上取得了显著进展，但其根本局限在于**预定义的封闭类别体系**。这些模型只能识别训练集中出现的特定物体类别（如“汽车”“行人”），无法适应开放世界中动态变化的语义需求——当场景中出现训练时未见过的物体类型，或用户需要按新的语义粒度（如“所有可移动物体”）进行查询时，模型完全失效。

这一封闭世界假设与真实自动驾驶场景的开放性之间存在根本矛盾。实际部署中，车辆可能遭遇异形障碍物、非常规交通参与者或需要按自由形式文本描述检索特定目标，而重新标注数据并训练模型以覆盖所有潜在类别在经济和时间上均不可行。

### 2D基础模型的启示与3D域的知识鸿沟

近年来，以**SAM**（Segment Anything Model）和**CLIP**（Contrastive Language-Image Pre-training）为代表的2D视觉基础模型展示了强大的零样本泛化能力——SAM能在图像中分割任意物体，CLIP能将视觉内容与自由形式文本对齐。这自然引发一个问题：能否将这些2D基础模型的知识迁移至3D激光雷达域，实现无需人工标注的激光雷达全景分割？

然而，直接“提升”（lift）2D输出到3D面临三重瓶颈：

1. **传感器域间隙**：2D图像分割掩码通过标定参数反投影到3D点云时，受限于摄像头视场、标定误差和多传感器同步精度，仅能覆盖部分点云（在SemanticKITTI上伪标签覆盖率仅约14%），且存在严重的空间错位和噪声。
2. **语义蒸馏困难**：CLIP特征在图像域表现优异，但直接将其反投影到稀疏、无序的激光雷达点云上，特征质量急剧下降，无法直接支撑可靠的零样本分类。
3. **部分标签训练挑战**：由于伪标签仅覆盖摄像头视锥内的部分点云，传统全监督训练范式无法直接适用——模型在部分标注数据上训练后，在完整点云上推理时会产生严重的域间隙。

### 本文动机：走向无需人工监督的通用激光雷达分割

针对上述瓶颈，本文提出**SAL（Segment Anything in Lidar）**，核心动机在于**构建首个无需任何人工标注、可响应任意文本提示的零样本激光雷达全景分割模型**。SAL的设计围绕两个关键洞察展开：

- **解耦分割与识别**：将全景分割拆解为类不可知（class-agnostic）的实例分割和基于文本提示的零样本分类两个子任务。分割部分仅需学习“物体性”（objectness），不依赖语义标签；分类部分通过蒸馏CLIP特征空间实现，在测试时可通过自由形式文本提示指定任意类别词汇表，无需重新训练。
- **从噪声伪标签中鲁棒学习**：设计伪标签引擎自动从SAM和CLIP生成训练信号，并通过多阈值DBSCAN几何精炼和FrankenFrustum数据增强策略，使模型能在仅14%点云被标注的条件下，学会对完整点云进行高质量分割。

这一范式的意义在于：SAL首次证明了**完全摆脱人工标注、仅依赖2D基础模型蒸馏即可在激光雷达域实现零样本全景分割**的可行性，为构建真正通用的3D感知基础模型开辟了新路径。



## 核心方法与创新机理

### 问题瓶颈与因果机制

现有激光雷达全景分割模型受限于预定义的固定类别词汇表，无法应对开放世界中动态变化的语义需求。更根本的困境在于：训练通用三维分割模型需要大规模人工标注数据，而激光雷达点云的人工标注成本极高，且难以覆盖任意物体类别。SAL的核心洞察是**将分割与识别解耦**——通过类不可知分割（class-agnostic segmentation）处理“物体在哪里”的问题，再通过CLIP特征蒸馏与文本提示匹配处理“物体是什么”的问题——从而在无需任何人工标注的条件下，首次实现了零样本激光雷达全景分割。

### 关键创新槽位

SAL相较全监督baseline（如MaskPLS等）在以下五个关键维度上实现了范式转换：

| 创新维度 | 基线方法 | SAL方案 | 证据锚点 |
|---------|---------|---------|---------|
| **伪标签来源** | 人工标注真值 | 2D基础模型生成的伪标签（SAM分割掩码 + CLIP语义特征 + DBSCAN几何细化） | Sec 3.3, Fig 3a |
| **训练数据完整性** | 完全标注点云 | 部分标注点云（覆盖率仅14%），配合FrankenFrustum增强 | Sec 4.2, Table 1 |
| **分类机制** | 固定分类头或提升的2D特征 | 预测CLIP token并通过与文本提示的点积匹配实现零样本分类 | Sec 3.4, Fig 3b |
| **伪标签细化** | 无（直接使用SAM掩码） | 多阈值DBSCAN集成替换策略，用具有足够重叠的DBSCAN聚类替换SAM掩码 | Sec 3.3, Fig 4 |
| **学习框架** | 全监督学习 | 自监督学习（仅依赖伪标签，无人工标注） | Sec 1, 4.2 |

### 创新一：伪标签引擎——从2D基础模型到3D的知识蒸馏

SAL的伪标签引擎（Fig. 3a）通过标定好的多模态传感器设置，将2D视觉基础模型的输出迁移至激光雷达域。其流程包含三个关键步骤：

1. **SAM掩码生成与展平**：对每帧相机图像，SAM生成层次化的重叠掩码集合。SAL通过非极大值抑制（NMS）以最小重叠阈值展平该层次结构，确保掩码互斥，抑制物体部件和子部件而保留完整物体。最终得到非重叠的二进制掩码 $m_i^k \in \{0,1\}^{W \times H}$。

2. **CLIP语义特征提取**：对每个SAM掩码，利用MaskCLIP在CLIP图像编码器特征空间中的相对掩码注意力机制，生成局部CLIP图像特征token $f_i^{\bar{k}} \in \mathbb{R}^{\bar{C}_t}$。

3. **反投影与几何细化**：将图像掩码通过标定参数反投影至激光雷达点云，得到初始激光雷达掩码 $\tilde{m}_i \in \{0,1\}^N$。由于传感器视差和标定误差，该过程产生“出血边缘”（bleeding edges）等伪影（Fig. 4b）。SAL提出**多阈值DBSCAN集成替换策略**：以不同密度阈值运行DBSCAN聚类，将具有足够相互重叠的DBSCAN聚类替换原始SAM掩码，有效改善定位精度。

**关键证据**：DBSCAN替换策略将类不可知分割PQ从直接使用SAM掩码的46.0提升至48.7（Table 4），且该改进可在Fig. 4c中直观验证。

### 创新二：部分标签训练与FrankenFrustum增强

伪标签的一个根本局限是仅覆盖摄像头视场内的点云——在SemanticKITTI上覆盖率仅为14%。直接在部分标注的点云上训练会导致严重的训练-推理域间隙。SAL提出两项关键策略解决此问题：

1. **Frustum Filter**：训练时裁剪所有不在摄像头视锥内的未标记点，使模型仅在有监督信号的区域学习。这一简单策略将PQ从22.2跃升至59.3（Table 1, rows 2-3），是处理部分标签的关键使能技术。

2. **FrankenFrustum增强**：通过沿z轴拼接多个部分标注的点云区域（Fig. A.2），模拟完整标注的训练样本。该增强有效减少训练-推理域间隙，将PQ从59.3进一步提升至62.5（Table 1, rows 3-4）。进一步混合不同扫描的点云可将PQ推至62.8。

**关键证据**：使用伪标签训练的SAL在类不可知分割上可达完全监督模型91%的性能（62.8 vs 69.0 PQ），而伪标签仅覆盖14%的点云（Table 1, row 5 vs row 1）。

### 创新三：CLIP Token蒸馏与零样本分类

SAL的分类机制是其零样本能力的核心。模型不预测固定类别的概率分布，而是通过**CLIP Token头**为每个查询预测CLIP空间中的特征token。训练时使用语义蒸馏损失 $\mathcal{L}_{token}$ 将MaskCLIP生成的图像token知识迁移至模型；推理时，通过计算预测token与文本提示编码之间的点积实现零样本分类。

**关键证据**：线性探测实验表明，使用 $\mathcal{L}_{token}$ 训练的模型PQ为33.1，而不使用时仅为20.0（Table 3），证明语义蒸馏损失成功将语义信息注入模型。文本提示工程（丰富同义词）可进一步大幅提升超类别零样本PQ，增益达+23.1（Table A.2）。

### 创新四：统一Transformer架构的类不可知分割

SAL模型（Fig. 3b）采用Minkowski U-Net稀疏卷积骨干网络提取点云特征，后接Transformer解码器。解码器通过交叉注意力从可学习查询中预测三个输出：物体性分数（objectness score）、二进制分割掩码、以及CLIP token。总损失函数为：

$$\mathcal{L}_{\mathtt{SAL}} = \mathcal{L}_{obj} + \mathcal{L}_{seg} + \mathcal{L}_{token}$$

该架构的关键优势在于其**通用性**：类不可知分割与语义分类完全解耦，使得模型既可以进行固定词汇表的全景分割，也可以对任意文本提示描述的物体进行零样本分割（Fig. 1, iii-iv）。

**关键证据**：在SemanticKITTI完整点云上，SAL的零样本全景分割PQ为24.8，达到全监督baseline（59.5 PQ）的42%；在nuScenes上PQ为38.4，达到全监督（70.5 PQ）的54%（Table 5）。在超类别设置下，SAL在SemanticKITTI完整点云上达到48.5 PQ，远超直接提升CLIP特征的基线（11.5 PQ），增益达+37.0（Table 4）。

### 方法谱系与知识库定位

SAL处于**2D基础模型驱动的3D自监督感知**这一新兴研究方向的交汇点。其方法谱系可追溯至：

- **SAM**（Kirillov et al., ICCV 2023）：提供类不可知图像分割能力，SAL将其作为伪标签引擎的核心分割模块。
- **MaskCLIP**（Dong et al., ECCV 2022）：实现从CLIP图像编码器中提取局部语义特征，SAL利用其生成每掩码的CLIP token。
- **CLIP**（Radford et al., ICML 2021）：提供视觉-语言对齐的联合嵌入空间，是SAL零样本分类能力的语义基础。
- **MinkowskiEngine**（Choy et al., CVPR 2019）：提供高效的3D稀疏卷积骨干网络。
- **MaskPLS**等全监督激光雷达全景分割方法：作为性能上界参考，SAL在无人工标注条件下达到其42%-54%的性能。

与直接提升SAM掩码和CLIP特征的简单基线（如SAM+DBS+CLIP）相比，SAL的核心差异在于**将噪声伪标签蒸馏至更强的3D原生模型**，而非直接使用提升的2D特征进行分类。这一蒸馏范式使模型能够学习3D几何先验，在完整点云上的零样本性能远超基线（+16.6 PQ on SemanticKITTI full）。

### 局限与开放问题

1. **伪标签覆盖率受限**：伪标签仅覆盖摄像头视场内的点云（14%覆盖率），且受限于摄像头视场和标定精度，部分物体类别（如被遮挡或超出视场的物体）无法获得监督信号。
2. **类间语义混淆**：零样本分类主要在超类内的相似类别上混淆（如car vs. other-vehicle），对歧义类名敏感，表明CLIP token的判别力仍有提升空间。
3. **计算开销**：伪标签生成需运行SAM等大型模型，计算开销大，总任务耗时较长。
4. **评估不一致**：现有数据集对stuff类的实例标注粒度与SAL的输出不一致，可能导致stuff性能被低估。
5. **传感器依赖**：方法依赖多模态标定传感器设置，标定误差和同步问题可能影响伪标签质量。能否扩展到其他传感器类型（如4D雷达）并实现跨传感器泛化，仍是一个开放问题。



![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2403_13129/figures/002_Figure_2.jpg]]
*Figure 2: SAL overview: Given a Lidar scan and a class vocabulary prompt, specified as a list of per-class free-form text descriptions (left), SAL segments and classifies objects (things and stuff classes). As labeled data for training such a model does not exist, we supervise SAL by distilling off-the-shelf vision foundation models to Lidar (right)*

SAL 的整体设计遵循一个清晰的“伪标签蒸馏—模型学习—文本提示推理”三阶段流水线，其核心思想是：既然没有人工标注的激光雷达全景分割数据，那就利用 2D 视觉基础模型自动生成伪标签，再将其知识蒸馏到一个原生 3D 模型中。

### 输入与输出

系统接受两类输入：
- **激光雷达点云** $P \in \mathbb{R}^{N \times 4}$，包含空间坐标与传感器强度；
- **类别词汇提示**（class vocabulary prompt），即一组自由形式的文本描述，如“car”、“pedestrian”、“road”等。

输出是一套全景分割结果：每个检测到的实例（things 类）或语义区域（stuff 类）同时拥有分割掩码和语义类别标签。关键在于，类别词汇可在测试时任意更换，无需重新训练或微调模型——这正是零样本能力的体现。

### 两大核心模块

SAL 由两个松耦合但协同工作的模块构成：

**模块一：伪标签引擎（Pseudo-label Engine）**
该引擎负责在没有人工标注的情况下，为激光雷达点云自动生成训练所需的伪标签。其工作流程为：
1. 对每帧相机图像运行 **SAM**，生成一组经过 NMS 去重后的互斥二值分割掩码 $m_i^k \in \{0,1\}^{W \times H}$；
2. 对每个 SAM 掩码，利用 **MaskCLIP** 在 CLIP 图像编码器特征空间中提取对应的 CLIP token $f_i^{\bar{k}} \in \mathbb{R}^{\bar{C}_t}$；
3. 通过已标定的传感器外参，将图像掩码反投影到激光雷达点云，得到初始 3D 伪标签 $\tilde{m}_i \in \{0,1\}^N$；
4. 使用多阈值 **DBSCAN** 集成对反投影结果进行几何细化，以缓解传感器视差和标定误差造成的边界渗色问题（bleeding edges）。

最终，伪标签引擎为每个点云输出一组带有 CLIP 语义 token 的类不可知分割掩码。这些伪标签仅覆盖点云的约 14%（受限于相机视场），且质量远逊于人工标注——但这正是 SAL 设计必须应对的现实约束。

**模块二：零样本激光雷达分割模型（SAL Zero-Shot Model）**
该模型从伪标签中学习，并在推理时支持文本提示的零样本分类。其架构为：
- **3D 稀疏卷积骨干**：采用 Minkowski U-Net 从原始点云提取多尺度特征；
- **Transformer 解码器**：一组可学习查询（learnable queries）通过交叉注意力与点云特征交互，每个查询负责预测一个潜在实例；
- **分割头**：预测每个查询对应的二值掩码（通过查询与点特征的点击）和物体性分数；
- **CLIP Token 头**：预测每个查询在 CLIP 语义空间中的 token 表示，用于后续与文本提示进行匹配。

### 训练与推理的数据流

训练阶段，伪标签引擎先生成伪标签，SAL 模型再通过联合优化三个损失项进行学习：
$$\mathcal{L}_{\mathtt{SAL}} = \mathcal{L}_{obj} + \mathcal{L}_{seg} + \mathcal{L}_{token}$$
其中 $\mathcal{L}_{obj}$ 监督物体性预测，$\mathcal{L}_{seg}$ 监督分割掩码，$\mathcal{L}_{token}$ 将伪标签中的 CLIP token 蒸馏到模型预测中——这是注入语义知识的关键通道。

值得注意的是，由于伪标签仅覆盖部分点云，训练时采用 **Frustum Filter** 裁剪掉未被标记的点，并配合 **FrankenFrustum** 增强（将部分标注区域沿 z 轴拼接模拟完整标注）来弥合训练-推理的域间隙。实验表明，这一策略是将类不可知分割 PQ 从 22.2 提升至 62.5 的决定性因素（Table 1）。

推理阶段，模型对输入点云预测一组实例掩码及其 CLIP token，然后将文本提示通过 CLIP 文本编码器编码，与预测 token 计算点积相似度，实现零样本分类。整个过程无需任何人工标注数据参与。



### 伪标签引擎 (Pseudo-label Engine)

SAL 的核心创新之一在于通过伪标签引擎将 2D 视觉基础模型的知识迁移至 3D 激光雷达域，从而摆脱对人工标注的依赖。该引擎由三个关键步骤构成：

1. **SAM 掩码生成与扁平化**：对每个摄像头视图 $k$，利用 SAM 生成一组重叠的分割掩码。随后通过非极大值抑制（NMS）与最小重叠阈值进行扁平化处理，确保掩码互斥，抑制物体部件和子部件，得到一组二进制掩码 $m_i^k \in \{0,1\}^{W \times H}$（见 Sec. 3.3）。

2. **CLIP 特征提取**：对每个 SAM 掩码，利用 MaskCLIP 的 relative mask attention 机制在 CLIP 图像编码器特征空间中提取局部化的图像特征 token $f_i^{\bar{k}} \in \mathbb{R}^{\bar{C}_t}$（见 Sec. 3.3）。

3. **反投影与几何细化**：通过标定好的传感器设置将图像掩码反投影至激光雷达点云，得到初始激光雷达掩码 $\tilde{m}_i \in \{0,1\}^N$。由于传感器标定误差和视差，反投影后的掩码存在“出血边缘”（bleeding edges）等噪声问题（见 Fig. 4b）。为此，SAL 采用多阈值 DBSCAN 集成策略进行几何细化：通过改变密度阈值生成多个 DBSCAN 聚类结果，并用与 SAM 掩码有足够重叠的 DBSCAN 聚类替换原始掩码（replace 策略），从而改善定位精度（见 Sec. 3.3, Fig. 4c）。

### 零样本分割模型 (Zero-Shot Model)

SAL 的零样本模型采用通用 Transformer 解码器架构（见 Fig. 3b），包含以下模块：

- **3D 稀疏卷积骨干网络**：采用 Minkowski U-Net 作为特征提取器，处理输入点云 $P \in \mathbb{R}^{N \times 4}$（空间坐标与强度），输出点级特征。

- **Transformer 解码器**：通过一组可学习查询（queries）与骨干网络提取的点云特征进行交叉注意力计算，为每个查询生成实例感知的表示。

- **分割头 (Segmentation Head)**：对每个查询预测二进制分割掩码，通过计算查询与点特征的 dot product 得到；同时预测物体性分数（objectness score），用于区分有效实例与背景。

- **CLIP Token 头**：预测每个查询在 CLIP 特征空间中的 token，用于后续零样本分类——通过计算预测 token 与文本提示编码之间的点积实现类别匹配。

### FrankenFrustum 增强

由于伪标签仅覆盖摄像头视锥可见的点云区域（SemanticKITTI 中覆盖率仅约 14%），直接训练会产生严重的训练-推理域间隙。FrankenFrustum 增强策略通过将多个部分标注的点云沿 z 轴拼接，模拟完整标注的训练样本（见 Sec. 3.4, Fig. A.2），有效缓解了部分标签训练问题。

### 关键公式

**SAL 总损失函数**（Equation (1)）：

$$\mathcal{L}_{\mathtt{SAL}} = \mathcal{L}_{obj} + \mathcal{L}_{seg} + \mathcal{L}_{token}$$

其中：
- $\mathcal{L}_{obj}$：物体性损失，监督模型区分有效实例与背景。
- $\mathcal{L}_{seg}$：分割掩码损失，监督二进制掩码预测与伪标签的一致性。
- $\mathcal{L}_{token}$：CLIP token 蒸馏损失，将伪标签引擎提取的 CLIP 图像特征 token 蒸馏至模型的 token 预测头，是实现零样本语义分类的核心驱动力。

**全景质量评估指标**（Section 4.1）：

$$PQ = RQ \times SQ$$

其中 $RQ$ 为识别质量（Recognition Quality），衡量实例匹配的正确性；$SQ$ 为分割质量（Segmentation Quality），衡量匹配实例的 IoU 均值。该指标用于统一评估 things 和 stuff 类的全景分割性能。



## 实验与关键发现

### 核心实验设计

SAL的实验评估围绕两个核心问题展开：（1）在无人工标注条件下，模型能否学会类不可知分割？（2）蒸馏得到的语义特征能否支持零样本全景分割？为此，作者在SemanticKITTI和nuScenes两个数据集上进行了系统验证。评估采用全景质量指数 $PQ = RQ \times SQ$，其中$RQ$衡量实例识别质量，$SQ$衡量分割质量。对于类不可知分割，引入语义Oracle（SO）和Stuff Merging（SM）策略以公平比较——因为现有数据集对stuff类的实例标注粒度与SAL的segment输出不一致。对于依赖图像特征的基线方法，部分实验仅在摄像头视锥可见的点子集上进行（Frustum Eval）。

### 部分标签训练：从14%覆盖到91%性能

SAL面临的核心训练挑战是伪标签仅覆盖点云的一小部分。在SemanticKITTI上，SAM反投影的伪标签仅覆盖14%的点云（Table 1）。直接使用这些部分标签训练会导致严重的训练-推理域间隙：模型在推理时面对完整点云，但训练时只见过被标注的局部区域。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2403_13129/figures/005_Table_1.jpg]]
*Table 1: Class-agnostic segmentation. Table 2: Scaling. By contrast to GT By cropping unlabeled points and performing data/labels, by increasing the number data augmentations (in combination with our of queries, SAL improves performance FrankenFrustum), SAL successfully learns to on stuff classes. By increasing the segment full point clouds even when only 14% amount of labeled data, we further imof points are (pseudo)-labeled. prove segmentation performance*

消融实验（Table 1）揭示了解决这一问题的关键路径：

1. **Frustum Filter（裁剪未标记点）**：训练时移除所有不在相机视锥内的未标记点，使训练分布与伪标签分布一致。这一操作将PQ从22.2跃升至59.3，是处理部分标签最关键的技术手段。

2. **FrankenFrustum增强**：通过沿z轴拼接多个扫描的可见区域，模拟完整标注的点云结构，有效减少训练-推理域间隙。该策略将PQ从59.3进一步提升至62.5。

3. **跨扫描混合**：混合不同扫描的点云进一步将PQ推至62.8。值得注意的是，使用伪标签训练的SAL在类不可知分割上达到了完全监督模型（GT标签，69.0 PQ）的91%性能，而伪标签仅覆盖14%的点云——这验证了蒸馏-学习范式的有效性。

### 查询数量与数据规模缩放

Table 2的缩放实验表明，增加Transformer解码器的可学习查询数量对stuff类分割有显著增益：从100查询增加到300查询，stuff类PQ（$PQ^{St}$）从47.8提升至58.3（+10.8）。这是因为stuff类（如道路、建筑）在点云中覆盖面积大但实例边界模糊，更多查询提供了更细粒度的分割能力。相比之下，things类（如车辆、行人）的增益较小，因其边界清晰、数量有限。

将伪标签训练集与测试集合并为bigtrain集进一步带来+2.5 PQ的提升（62.8→65.3），表明数据规模扩展仍有正向收益，尚未观察到明显的饱和点。

### 语义蒸馏的关键作用

Table 3的线性探测实验直接验证了语义蒸馏损失 $\mathcal{L}_{token}$ 的有效性。在该实验中，冻结训练好的SAL模型的骨干网络和解码器，仅用GT标签训练一个线性分类头来预测语义类别。使用 $\mathcal{L}_{token}$ 训练的模型在线性探测下达到33.1 PQ，而去除该损失后骤降至20.0 PQ。这表明 $\mathcal{L}_{token}$ 成功将CLIP语义信息注入了模型的token预测头，而非仅仅依赖分割质量。语义蒸馏是连接“类不可知分割”与“零样本分类”的桥梁。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2403_13129/figures/006_Table_3.jpg]]
*Table 3: Semantic distillation. We linearly probe the SAL model, trained with and without semantic distillation loss $\mathcal { L } _ { t o k e n }$ . We train a linear classifier with GT labels while keeping backbone and decoder features frozen. As can be seen, Ltoken successfully distills a notion of semantics into our model*

### 伪标签细化策略对比

Table 4系统比较了不同伪标签处理策略对下游性能的影响：

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2403_13129/figures/007_Table_4.jpg]]
*Table 4: Zero-shot panoptic segmentation. We utilize prior efforts in the image domain [31] and Lidar [58] domain to craft multiple baselines that only unproject segmentation masks and lift image features to Lidar. By contrast, SAL distills outputs of such baselines (pseudo-labels) into a stronger Lidar segmentation model. With Image Feat. we denote methods that require image features at inference time, and Frust. Eval. denotes the evaluation of a subset of points visible in the camera*

- **SAM（直接反投影）**：类不可知PQ仅46.0，问题在于相机-LiDAR标定误差导致的“出血边缘”和遮挡噪声。
- **SAM + DBSCAN（filter）**：过滤策略提升了things类精度（$PQ^{Th}$达76.8），但严重损害stuff类（$PQ^{St}$仅24.8），整体PQ降至46.7。这是因为DBSCAN过滤会错误移除大面积stuff区域的点。
- **SAM + DBSCAN（replace）**：替换策略（用DBSCAN聚类替换与SAM掩码有足够重叠的区域）在things和stuff之间取得更好平衡，类不可知PQ提升至48.7，成为最优伪标签基线。

SAL在这些伪标签上训练后，类不可知分割PQ跃升至70.7（+22.0），证明了蒸馏学习框架对伪标签噪声的鲁棒性。

### 零样本全景分割主要结果

Table 4的零样本LPS结果展示了SAL的核心能力：

- **Frustum Eval（视锥可见点）**：SAL在默认类别下达到33.1 PQ，显著优于直接提升SAM掩码+CLIP特征的基线（27.5 PQ，+5.6）。这验证了“蒸馏到强3D模型”策略优于“直接使用2D特征”策略。
- **Full Point Cloud（完整点云）**：差距更为显著——SAL达到24.8 PQ，而基线仅8.2 PQ（+16.6）。基线在完整点云上性能崩溃的原因是其依赖的2D特征仅存在于视锥区域，而SAL通过3D骨干网络学习到了全点云的特征表示。
- **超类别（super classes）**：将细粒度类别合并为粗粒度超类后，SAL在完整点云上达到48.5 PQ，基线仅11.5 PQ（+37.0）。这一巨大差距表明SAL的语义特征在粗粒度分类上更为可靠，细粒度混淆是主要瓶颈。

Table 5将零样本SAL与完全监督基线进行比较：在SemanticKITTI上达到全监督的42%（24.8 vs 59.5 PQ），在nuScenes上达到54%（38.4 vs 70.5 PQ）。nuScenes上相对性能更高，可能与其点云密度更高、相机覆盖更好有关。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2403_13129/figures/008_Table_5.jpg]]
*Table 5: Lidar Panoptic Segmentation (LPS) on SemanticKITTI and nuScenes validation sets. We prompt our zero-shot SAL model with the respective class vocabularies and compare its performance to fully-supervised baselines. On SemanticKITTI and nuScenes, we reach 42% and 54% of the fully-supervised model, respectively. This gap reduces significantly when we evaluate super classes*

### 失败模式与局限性

1. **类间混淆**：零样本分类的主要失败集中在超类内的相似类别，如car vs. other-vehicle。这是因为CLIP token在细粒度语义上的区分能力有限，且类名歧义（如“car”和“vehicle”在文本嵌入空间中高度相似）加剧了混淆。

2. **Stuff类评估困难**：现有数据集对stuff类的实例标注（如将整段道路标为一个实例）与SAL的segment输出粒度不一致。这导致stuff类指标可能被低估，且缺乏可靠的评估标准。

3. **伪标签覆盖局限**：伪标签仅覆盖相机视场内的点（SemanticKITTI上14%），激光雷达360°扫描中大量点无法获得伪标签监督。这限制了模型在相机盲区的分割能力。

4. **计算开销**：生成伪标签需要运行SAM（每帧多张图像）和CLIP，加上DBSCAN聚类，总耗时较长（Table B.5显示伪标签生成是训练流程的主要计算瓶颈）。

5. **传感器依赖**：方法依赖精确的多模态标定。标定误差和相机-LiDAR时间同步问题会直接降低伪标签质量，且这种误差在远距离点云上被放大。

### 文本提示工程的影响

Table A.2揭示了文本提示工程对零样本分类的显著影响。通过为每个类别提供丰富的同义词和多模板包装（如“a photo of a {class}”），超类别零样本PQ获得+23.1的增益。这表明CLIP token预测的质量高度依赖于训练时蒸馏的文本特征与测试时提示之间的对齐程度。简单使用单一类名会导致语义匹配失败，尤其对于数据集中的非自然类别名（如“other-vehicle”）。

### 关键图表结论

- **Table 1**：Frustum Filter是处理部分标签训练的核心技术，FrankenFrustum增强进一步缩小域间隙。伪标签训练可达GT性能的91%。
- **Table 3**：$\mathcal{L}_{token}$ 是将语义注入模型的必要条件，去除后线性探测PQ从33.1降至20.0。
- **Table 4**：SAL通过蒸馏学习显著超越直接使用2D伪标签的基线，在完整点云上优势尤为突出（+16.6 PQ）。
- **Table 5**：零样本SAL在nuScenes上达到全监督的54%，验证了方法的跨数据集泛化能力。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2403_13129/figures/004_Figure_4.jpg]]
*Figure 4: (c) SAM + DBSCAN Fig. 4: Refinement via clustering. After transferring image masks (Fig. 4a) to Lidar (Fig. 4b), we obtain pseudo-labels that suffer from sensory misalignment-related issues. Our geometric refinement (Fig. 4c) improves localization*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2403_13129/figures/012_Figure.jpg]]
*Figure: (b) FrankenFrustum Fig. A.2: Training on partial labels. Unprojecting image-based pseudo labels results in a partially (pseudo) labeled point cloud (Fig. A.2a). We construct supervisory signal by concatenating multiple partially labeled point clouds (Fig. A.2b)*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2403_13129/figures/021_Figure.jpg]]
*Figure: (a) Front-left camera (b) Front camera (c) Front-right camera Fig. E.2: Class-agnostic segmentation on Waymo Open [75] from first-person perspective. We visually outline the Lidar point cloud, where points are colored according to estimated instance IDs, estimated by SAL. We show corresponding camera views (not used for inference) for reference. As can be seen, SAL accurately segments a large variety of objects, including parking meters, potted trees (pots as well as trees), rooftop ladder, water hydrant, post box, traffic cone, traffic barrier, and more. Canonical objects, such as car, van, bus, and pedestrian are segmented as well. This class-agnostic segmentation is a basis for zero-shot...*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2403_13129/figures/029_Figure.jpg]]
*Figure: (h) Prompt: {curb} Fig. E.9: Zero-shot per-class prompting on Waymo Open [75]. SAL predicts a set of object instances (left), along with their objectness scores and distilled CLIP [67] features. We can use text prompts and query these instances for specific classes specified as prompts. On the right, we highlight several such examples that are outside of classvocabularies of SemanticKITTI, nuScenes, and Waymo Open datasets. As can be seen on the left, a basis for such zero-shot prompting is accurate and, importantly, diverse class-agnostic segmentation*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2403_13129/figures/009_Table.jpg]]
*Table: A.1: SAL hyperparameters. We show parameters for both components of our framework: (i) SAM model [31], which we use to generate segmentation masks in images; (ii) the pseudo-label generation engine and (iii) our zero-shot model. For the latter, we only highlight parameters that deviate from [45]*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2403_13129/figures/011_Table.jpg]]
*Table: A.2: CLIP token distillation and text prompt engineering. To evaluate our token prediction, we prompt the SemanticKITTI class vocabulary to generate labeled training data and train a non-zero-shot model (row 1). Furthermore, we demonstrate the insufficiency of vanilla class names (car) as text prompts and the boost from engineering a rich set of terms (car, jeep, SUV, van) as explained in Appendix A.3*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2403_13129/figures/013_Table.jpg]]
*Table: B.1: Pseudo-label statistics. We outline the label coverage of point clouds, the total, max, and mean number of instances per scan, and the ratio of things/stuff instances on the full point cloud and point cloud areas that overlap with the camera view frustum (Filter Frustum). As can be seen, due to the single-camera setup, pseudo-label coverage in SemanticKITTI [6] is very low (14% of points). Even though nuScenes [18] dataset provides 3 6 0 ^ { \circ } view coverage, only 48% are labeled due to blind spots. Even when only retaining points, that overlap with the camera view frustum (SemanticKITTI, Filter Frustum), we observe coverage of 89%. This can be explained by mistakes (e.g., false n...*



## 定位与知识库关联

### 1. 与基线方法的关系

SAL 的核心创新在于将激光雷达全景分割从“封闭类别监督学习”推向了“开放词汇零样本学习”。其技术路线与以下基线形成明确对比：

**直接提升2D掩码的基线。** 最直接的思路是将 SAM 生成的图像掩码通过标定参数反投影至点云，再利用 CLIP 特征进行零样本分类。该基线（SAM + DBSCAN + CLIP）在 SemanticKITTI 默认类别下仅取得 27.5 PQ（Table 4），且在全点云评估中骤降至 8.2 PQ。其根本瓶颈在于：图像掩码反投影引入的传感器对齐噪声（如边缘出血效应，Fig. 4b）以及 CLIP 特征在三维空间的语义表达力不足。

**SAL 的蒸馏策略。** SAL 并未直接使用上述基线的输出，而是将其作为“伪标签引擎”的原料，通过 Transformer 解码器与 CLIP token 蒸馏损失 $\mathcal{L}_{token}$ 将2D知识迁移至3D骨干网络。这一蒸馏过程带来了显著的性能增益：零样本 LPS 从 27.5 PQ 提升至 33.1 PQ（+5.6，Table 4），在全点云场景下增益更达 +16.6 PQ。线性探测实验（Table 3）直接证实了 $\mathcal{L}_{token}$ 的语义注入效果——去除该损失后 PQ 从 33.1 降至 20.0。

**与全监督方法的差距。** SAL 在 SemanticKITTI 和 nuScenes 上分别达到全监督基线的 42%（24.8 vs 59.5 PQ）和 54%（38.4 vs 70.5 PQ）（Table 5）。考虑到 SAL 完全无需人工标注，这一结果确立了自监督激光雷达全景分割的新基准。类不可知分割的差距更小：伪标签训练的 SAL 达到 GT 训练的 91%（62.8 vs 69.0 PQ，Table 1），表明分割能力的蒸馏已相当高效，主要瓶颈在于语义分类。

### 2. 方法适用边界

**传感器配置依赖性。** SAL 的伪标签引擎强依赖于标定的相机-激光雷达系统。标定误差、时间同步偏差以及相机视场限制会直接影响伪标签质量。Table B.1 显示伪标签仅覆盖 SemanticKITTI 点云的 14%，且类别分布偏向相机可见区域（如车辆类覆盖率达 68%，而 pole 类仅 2.7%，Table B.2）。在无相机或标定不佳的场景下，该方法无法直接适用。

**类别粒度与歧义敏感性。** 零样本分类在超类内细粒度类别上存在明显混淆（如 car vs. other-vehicle），且对文本提示的措辞敏感。Table A.2 显示，通过文本提示工程（丰富同义词），超类别 PQ 可提升 +23.1，表明 CLIP token 的语义空间在激光雷达域仍缺乏足够的判别力。

**计算开销。** 伪标签生成需对每帧图像运行 SAM 与 MaskCLIP，计算成本显著。该开销限制了方法在实时或资源受限场景中的部署。

**Stuff 类评估偏差。** 现有数据集（SemanticKITTI、nuScenes）对 stuff 类的实例标注粒度与 SAL 的分割输出不一致，导致评估时需引入语义 Oracle（SO）和 Stuff Merging（SM）等后处理。这意味着报告的 stuff 性能可能被低估，且评估协议本身缺乏标准化。

### 3. 局限与开放问题

**伪标签质量的固有限制。** DBSCAN 细化策略虽将类不可知 PQ 从 46.0 提升至 48.7（Table 4），但仍无法解决因遮挡、多路径反射或远距离稀疏导致的点云几何噪声。伪标签的覆盖率与精度之间存在权衡：过滤策略提升了 things 精度（PQ^Th 76.8）但严重损害 stuff（PQ^St 24.8），替换策略则相反（Table 4）。如何在无人工干预下自动平衡这一权衡仍是开放问题。

**跨传感器泛化。** SAL 当前仅验证于旋转式激光雷达（Velodyne HDL-64E）。能否将伪标签引擎适配至固态激光雷达、4D 成像雷达或其他主动传感器，并保持蒸馏模型的有效性，尚未探索。

**伪标签数据规模的饱和效应。** Table 2 显示，将训练数据从 train 集扩展至 bigtrain 集（拼接训练与测试集伪标签）带来 +2.5 PQ 增益。但数据量继续增加时性能是否饱和、是否存在伪标签噪声累积导致的性能退化，缺乏实验验证。

**完全无监督的评估范式。** 零样本 LPS 的评估目前仍依赖人工标注的真值。在完全无人工标注的开放世界中，如何客观评估分割质量（尤其是 stuff 类的实例粒度）是一个基础性难题。

**向其他3D任务的拓展。** SAL 的自监督蒸馏范式——利用2D基础模型生成伪标签，通过 Transformer 解码器蒸馏至3D骨干——是否可迁移至3D目标追踪、轨迹预测或4D场景理解，是值得探索的方向。



## 原文 PDF

![[paperPDFs/ECCV_2024/Better_Call_SAL_Towards_Learning_to_Segment_Anything_in_Lidar.pdf]]
