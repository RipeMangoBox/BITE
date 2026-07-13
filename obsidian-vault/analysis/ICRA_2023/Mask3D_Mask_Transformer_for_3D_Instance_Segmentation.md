---
title: "Mask3D: Mask Transformer for 3D Instance Segmentation"
type: paper
paper_level: A
venue: ICRA
year: 2023
pdf_ref: paperPDFs/ICRA_2023/Mask3D_Mask_Transformer_for_3D_Instance_Segmentation.pdf
code_link: null
project_link: https://jonasschult.github.io/Mask3D/
aliases:
- Mask3D
tags:
- ICRA_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "非参数实例查询与掩码交叉注意力（masked cross-attention）使得Transformer解码器能直接迭代地关注点云特征，无需手工几何先验。"
primary_logic: "将3D实例分割建模为集合预测问题，通过Transformer解码器产生的实例查询直接预测所有实例的二进制掩码和语义类别，消除了对手工投票和分组机制的依赖。"
claims:
- "Mask3D在多个数据集上超越先前方法，mAP提升显著（ScanNet test +6.2 mAP）"
- "非参数查询（FPS采样坐标，零初始化特征）优于参数查询"
- "掩码交叉注意力强制查询关注实例内部，提升分割质量"
- "加权组合Dice和BCE损失优于单独使用任一损失"
---

# Mask3D: Mask Transformer for 3D Instance Segmentation

> [!tip] 核心洞察
> 将3D实例分割建模为集合预测问题，通过Transformer解码器产生的实例查询直接预测所有实例的二进制掩码和语义类别，消除了对手工投票和分组机制的依赖。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Mask3D: 用于三维实例分割的掩码Transformer |
| 英文题名 | Mask3D: Mask Transformer for 3D Instance Segmentation |
| 会议/期刊 | ICRA 2023 |
| Links | [paper](https://arxiv.org/abs/2210.03105) · [Project](https://jonasschult.github.io/Mask3D/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Mask3D |
| Dataset | ScanNet v2 test, S3DIS 6-fold cross validation, ScanNet200 test, STPLS3D test |

> [!tip] 效果简介
> - ScanNet v2 test 上，mAP 为 56.6，对比 50.6 (SSTNet) / 50.4 (SoftGroup)，变化 +6.2 (claimed vs best prior)。
> - S3DIS 6-fold cross validation 上，mAP 为 64.5 (without pretrain) / 61.8 (with pretrain)，对比 ~54.4 (SoftGroup)，变化 +10.1 (claimed)。
> - ScanNet200 test 上，mAP 为 38.3 (head) / 26.3 (common) / 16.8 (tail)，对比 27.5 (LGround)，变化 +10.8 (claimed overall mAP improvement)。

## 概要

三维实例分割要求模型在点云中同时识别出每个对象的语义类别与精确的几何掩码。此前的主流方法大多依赖手工设计的投票中心、几何聚类或边界框优化等中间步骤，这些机制难以端到端优化，且对非凸形状、密集堆叠场景的泛化能力有限。Mask3D 将三维实例分割重新建模为**集合预测问题**：通过 Transformer 解码器产生的实例查询（instance query）直接并行预测所有实例的二进制掩码与语义类别，从而消除了对手工投票和分组机制的依赖。

核心因果调控点在于**非参数实例查询与掩码交叉注意力**。非参数查询由场景点的 FPS 采样坐标和零初始化特征构成，不依赖可学习的参数查询；掩码交叉注意力则强制每个查询仅关注其当前预测掩码内的体素，使查询能迭代地聚焦于实例内部特征。这一设计使得模型能够端到端地学习实例级表示，而无需注入几何先验。

Mask3D 在多个数据集上显著超越了先前方法：
- **ScanNet v2 test**：mAP 达到 56.6，较此前最佳方法提升 +6.2 mAP（Tab. I）。
- **S3DIS 6-fold**：mAP 达到 64.5（无预训练），较 SoftGroup 提升约 +10.1 mAP（Tab. II）。
- **ScanNet200 test**：整体 mAP 较大幅度领先 LGround 等基线（Tab. III）。
- **STPLS3D test**：mAP 57.3，较 SoftGroup 提升 +11.2 mAP（Tab. III）。

消融实验确认了关键设计的有效性：非参数查询优于参数查询（mAP 40.6 vs 39.7）；Dice + BCE 联合损失显著优于单一损失（Tab. IV）；增加 Transformer 解码器层数（≥12 层）可稳定提升性能（Fig. 3）。推理速度方面，Mask3D（339 ms）与当时最优的投票方法 SoftGroup（345 ms）相当，且模型参数主要来自特征主干（>90%），Transformer 解码器仅占约 1.76M 参数。

该方法仍存在局限性：注意力机制偶尔会合并相距较远但语义和几何相似的同类实例（如两个窗户），需借助可选的 DBSCAN 后处理进行空间分离，且其距离阈值需针对不同数据集单独调整。尽管如此，Mask3D 首次证明了纯 Transformer 架构在三维实例分割中的可行性与强大性能，为后续研究开辟了新的技术路径。



三维场景理解是计算机视觉的核心问题之一，而实例分割——同时识别并分割出场景中的每个独立物体——则是其中的关键挑战。与二维图像不同，三维点云具有稀疏性、无序性和复杂几何结构，使得实例分割任务尤为困难。

当前主流的3D实例分割方法普遍依赖手工设计的几何先验和中间表示。以**PointGroup**（Jiang et al., CVPR 2020）和**SoftGroup**（Vu et al., CVPR 2022）为代表的投票-聚类范式，首先预测每个点的语义标签和中心偏移量，再通过启发式分组机制将点聚合为实例。这类方法存在一个根本性瓶颈：投票和分组步骤不可微分，无法与特征提取器端到端联合优化，导致模型在面对非凸形状、尺度差异大的物体以及密集场景时泛化能力受限。此外，**3D-BoNet**（Yang et al., NeurIPS 2019）尝试直接预测固定数量的实例掩码，但缺乏灵活的实例表示和迭代细化机制。

从方法论角度看，这些方法的共同缺陷在于将实例分割视为自底向上的几何处理问题，而非直接的集合预测问题。手工设计的投票中心、亲和力矩阵或聚类半径本质上是对物体几何形态的简化假设，难以覆盖真实场景中物体的多样性和复杂性。

Mask3D的核心动机正是打破这一范式依赖。其核心洞察在于：将3D实例分割重新建模为集合预测问题，通过Transformer解码器产生的实例查询直接预测所有实例的二进制掩码和语义类别，从而彻底消除对手工投票和分组机制的依赖。这一思路借鉴了DETR在2D检测中的成功经验，但首次将其系统性地扩展到3D实例分割领域。



## 核心方法与创新机理

Mask3D的核心创新在于将3D实例分割重新定义为**集合预测问题**，通过Transformer解码器直接预测所有实例的掩码与语义类别，从而消除了传统方法对手工投票机制和几何聚类后处理的依赖。这一范式转换体现在以下四个关键维度的设计变革中。

### 实例表示：从几何中间产物到可学习的实例查询

传统方法（如**PointGroup** (Jiang et al., CVPR 2020)、**SoftGroup** (Vu et al., CVPR 2022)）依赖基于中心投票或点亲和力的中间表示来间接刻画实例，这些表示需要经过手工设计的聚类步骤才能转换为最终实例。Mask3D则采用**实例查询**直接编码每个实例的语义和几何信息。查询可采用两种形式：参数化查询（在训练中学习）或非参数查询（通过最远点采样选取场景中的点坐标，配合零初始化特征和位置编码）。实验表明，非参数查询因更贴合场景几何而优于参数化查询（mAP 40.6 vs 39.7，Tab. IV左），且推理时查询数量可灵活调整，无需重新训练即可在速度与性能间权衡。

### 掩码生成：从间接优化到端到端点积预测

传统方法通过聚类投票结果或边界框优化间接生成实例掩码，流程割裂且难以端到端优化。Mask3D的**Mask Module**将掩码生成简化为查询特征与点特征的点积运算，经Sigmoid激活和0.5阈值直接输出二进制掩码（Eq. 1）：

$$\mathbf{B} = \{ b_{i,j} = \big[ \sigma \big( \mathbf{F}_0 f_{\mathrm{mask}}(\mathbf{X})^T \big)_{i,j} > 0.5 \big] \}$$

这一设计使掩码预测完全可微分，为端到端训练奠定了基础。

### 上下文利用：从全局注意力到掩码交叉注意力

在查询细化过程中，Mask3D引入了**掩码交叉注意力**机制（Eq. 3），强制每个实例查询仅关注其当前预测掩码内的体素特征：

$$\mathbf{X} = \mathrm{softmax}(\mathbf{QK}^T / \sqrt{D} + \mathbf{B}') \mathbf{V} \;\text{with}\; \mathbf{B}_{ij}' = -\infty \cdot [\mathbf{B}_{ij} = 0]$$

这与标准交叉注意力形成互补：前者聚焦实例内部区域以提升分割精度，后者提供全局上下文。多尺度特征与自注意力的结合进一步增强了查询的表达能力。消融实验证实，掩码交叉注意力是模型性能的关键贡献者之一。

### 训练监督匹配：从固定分配到匈牙利最优匹配

传统方法通常采用最近邻匹配或固定分配策略建立预测与真值的对应关系，这在密集场景中容易产生次优匹配。Mask3D采用**匈牙利算法**进行最优二分图匹配，匹配成本函数联合考虑Dice损失、BCE损失和分类损失（Eq. 4）：

$$\mathcal{C}(k, \hat{k}) = \lambda_{\mathrm{dice}} \mathcal{L}_{\mathrm{dice}}(k, \hat{k}) + \lambda_{\mathrm{BCE}} \mathcal{L}_{\mathrm{BCE}_{\mathrm{max}}}(k, \hat{k}) + \lambda_{\mathrm{cl}} \mathcal{L}_{\mathrm{CE}_{\mathrm{cl}}}(k, \hat{k})$$

这一机制确保了训练过程中预测与真值的一对一最优对应，避免了手工分组带来的歧义。同时，掩码损失采用Dice与BCE的加权组合（Eq. 5），消融实验表明该组合显著优于单一损失（mAP 40.6 vs 38.0/27.0，Tab. IV右），且Dice单独使用已优于BCE。

### 创新本质：消除手工先验，实现端到端优化

上述四项变革共同构成了Mask3D的核心创新逻辑：**将3D实例分割从手工设计的几何流水线转变为数据驱动的集合预测框架**。实例查询替代了中心投票，点积掩码生成替代了聚类后处理，掩码交叉注意力替代了手工分组，匈牙利匹配替代了固定分配。这一系统性重构使得模型能够端到端地从数据中学习实例分割策略，在非凸形状物体和密集场景中展现出更强的泛化能力——这正是Mask3D在多个基准数据集上大幅超越先前方法（ScanNet test +6.2 mAP，S3DIS 6-fold +10.1 mAP）的根本原因。



Mask3D将三维实例分割建模为一个端到端的集合预测问题，其整体pipeline由四个核心模块串联构成：**稀疏特征主干网络** → **实例查询初始化** → **Transformer解码器迭代细化** → **掩码预测与置信度评分**。给定原始三维点云，模型直接并行输出所有实例的二进制掩码和语义类别，无需手工设计的投票中心或几何聚类步骤。

### 数据流与模块关系

**输入**：三维点云（坐标与可选颜色）。

**稀疏特征主干网络**（Sparse Convolutional Feature Backbone）采用基于MinkowskiEngine的对称U-Net架构（Res16UNet34C），从体素化点云中提取多尺度点特征 $\mathbf{F}$。主干输出5个层次的特征图，其中最高分辨率特征 $\mathbf{F}_0$ 用于后续掩码生成（Fig. 5）。

**实例查询初始化**（Query Initialization）生成一组固定数量的实例查询，每个查询由位置编码和特征向量组成。Mask3D支持两种查询类型：
- **参数查询**：可学习的嵌入向量，与场景内容无关。
- **非参数查询**：通过最远点采样（FPS）从输入点云中选取坐标，查询特征初始化为零，仅使用采样点的三维位置计算位置编码。非参数查询使模型能根据场景几何自适应地放置查询，且在推理时可动态调整查询数量以权衡速度与精度，无需重新训练。

**Transformer解码器**（Transformer Decoder）由 $L$ 层堆叠的查询细化层组成（默认共享权重），每层依次执行三种注意力操作：
1. **自注意力**（Self-Attention）：在查询之间交换上下文信息。
2. **交叉注意力**（Cross-Attention）：查询关注多尺度体素特征，聚合场景信息。
3. **掩码交叉注意力**（Masked Cross-Attention）：利用上一层预测的中间掩码 $\mathbf{B}$ 约束注意力范围，使每个查询仅关注其掩码内的体素，强制查询聚焦于实例内部区域（Eq. 3）。对于体素数量不定的场景，采用填充+掩码策略或采样策略处理变长输入。

**掩码模块**（Mask Module）在每个解码器层后，将细化后的查询特征 $\mathbf{X}$ 经线性投影 $f_{\text{mask}}$ 后，与主干特征 $\mathbf{F}_0$ 做点积，经Sigmoid激活和阈值0.5得到二进制实例掩码 $\mathbf{B}$（Eq. 1）。同时，查询特征经分类头预测语义类别。

$$
\mathbf{B} = \{ b_{i,j} = \big[ \sigma \big( \mathbf{F}_0 f_{\text{mask}}(\mathbf{X})^T \big)_{i,j} > 0.5 \big] \}
$$

**训练匹配与损失**：训练时，使用匈牙利算法在预测实例与真值实例之间建立最优二分图匹配，匹配代价联合考虑Dice损失、BCE损失和分类交叉熵（Eq. 4）。总损失对所有解码器层的辅助输出求和（Eq. 6），掩码损失为Dice与BCE的加权组合（Eq. 5）。

$$
\mathcal{L} = \Sigma_l^L \mathcal{L}_{\text{mask}}^l + \lambda_{\text{cl}} \mathcal{L}_{\text{CE}_{\text{cl}}}^l
$$

**推理与置信度**：推理时，最终置信度由类别置信度与掩码内平均置信度的乘积计算（Eq. 7）。可选地，使用DBSCAN按空间邻近性分离被错误合并的同类实例。

### 关键设计决策

- **非参数查询**：消融实验表明，非参数查询（FPS坐标+零特征初始化）的mAP为40.6，优于参数查询的39.7（Tab. IV左），验证了场景自适应查询初始化的有效性。
- **掩码交叉注意力**：通过将注意力限制在预测掩码内，模型迭代地关注实例内部点，是消除手工几何先验的核心机制。
- **多尺度特征融合**：解码器交叉注意力同时访问5个尺度的主干特征，使查询能捕获不同粒度的上下文信息（Fig. 5）。
- **可选的DBSCAN后处理**：注意力机制偶尔会合并相距较远但语义相似的实例（如两个窗户），DBSCAN以空间距离分离合并错误，但最优距离阈值需针对不同数据集单独调整（ScanNet: 0.9, S3DIS: 0.6）。

### 参数分布

模型参数主要集中于特征主干（>90%），Transformer解码器仅约1.76M参数，整体模型大小与当前顶级方法相当或略大（Tab. VI）。推理速度在TITAN X上为339 ms（不含后处理），与SoftGroup的345 ms相当（Tab. I）。



### 稀疏特征主干

Mask3D采用基于MinkowskiEngine的稀疏卷积U-Net作为特征主干（**Minkowski Res16UNet34C**），输出5个尺度的点云体素特征 $\mathbf{F}$。主干采用对称的编码器-解码器结构，将输入点云体素化后提取多尺度几何与语义特征，为后续Transformer解码器提供上下文基础。消融实验表明，即使将主干缩减为更轻量的Res16UNet18B，性能仅从40.9 mAP降至40.0 mAP，说明模型对特定主干的依赖程度较低（Tab. V）。

### 掩码模块

掩码模块是Mask3D的核心预测单元，负责从实例查询特征和点云特征直接生成实例掩码。给定主干输出的点特征 $\mathbf{F}_0 \in \mathbb{R}^{M \times D}$ 和细化后的实例查询特征 $\mathbf{X} \in \mathbb{R}^{N \times D}$，掩码模块首先通过线性投影 $f_{\text{mask}}$ 将查询特征映射到与点特征相同的维度空间，然后计算两者之间的点积相似度，经Sigmoid激活和阈值0.5二值化得到最终掩码：

$$\mathbf{B} = \{ b_{i,j} = \big[ \sigma \big( \mathbf{F}_0 f_{\text{mask}}(\mathbf{X})^T \big)_{i,j} > 0.5 \big] \}$$

其中 $M$ 为点云点数，$N$ 为实例查询数量，$D$ 为特征维度，$\sigma$ 为Sigmoid函数，$\mathbf{B}_{ij}$ 表示第 $i$ 个查询在第 $j$ 个点上的二进制掩码归属。这种点积机制将实例分割转化为特征空间中的相似度匹配问题，无需任何几何聚类或投票操作。

### 查询细化：掩码交叉注意力

Transformer解码器通过堆叠的 $L$ 层迭代细化实例查询，每层包含三个关键注意力操作。标准交叉注意力允许查询自由关注所有体素特征：

$$\mathbf{X} = \text{softmax}(\mathbf{QK}^T / \sqrt{D})\mathbf{V}$$

其中 $\mathbf{Q}$ 来自实例查询，$\mathbf{K}$、$\mathbf{V}$ 来自多尺度体素特征。在此基础上，Mask3D引入**掩码交叉注意力**，强制每个查询仅关注其当前预测掩码内的体素区域：

$$\mathbf{X} = \text{softmax}(\mathbf{QK}^T / \sqrt{D} + \mathbf{B}') \mathbf{V} \quad \text{with} \quad \mathbf{B}_{ij}' = -\infty \cdot [\mathbf{B}_{ij} = 0]$$

通过在注意力矩阵中为掩码外体素添加 $-\infty$ 偏置，Softmax后这些位置的权重趋近于零，从而实现空间约束。这一设计使得查询在细化过程中逐步聚焦于实例内部区域，提升分割边界的精确性。此外，查询间自注意力用于建模实例间的全局上下文关系。为处理不同场景的点数差异，解码器采用采样交叉注意力策略：当体素数量超过阈值时进行随机采样，并通过填充和掩码机制确保所有查询仍能访问完整空间信息。

### 训练匹配与损失函数

训练时采用匈牙利算法建立预测实例与真值实例之间的最优二分图匹配。匹配成本函数综合考虑掩码质量和语义分类：

$$\mathcal{C}(k, \hat{k}) = \lambda_{\text{dice}} \mathcal{L}_{\text{dice}}(k, \hat{k}) + \lambda_{\text{BCE}} \mathcal{L}_{\text{BCE}_{\text{max}}}(k, \hat{k}) + \lambda_{\text{cl}} \mathcal{L}_{\text{CE}_{\text{cl}}}(k, \hat{k})$$

其中 $\mathcal{L}_{\text{BCE}_{\text{max}}}$ 为逐像素二元交叉熵损失的最大值聚合形式。匹配完成后，仅对匹配成功的查询对计算掩码损失：

$$\mathcal{L}_{\text{mask}} = \lambda_{\text{BCE}} \mathcal{L}_{\text{BCE}} + \lambda_{\text{dice}} \mathcal{L}_{\text{dice}}$$

总损失对所有解码器层的辅助输出求和，实现深度监督：

$$\mathcal{L} = \Sigma_l^L \mathcal{L}_{\text{mask}}^l + \lambda_{\text{cl}} \mathcal{L}_{\text{CE}_{\text{cl}}}^l$$

消融实验证实，Dice与BCE的加权组合（mAP 40.6）显著优于单独使用BCE（27.0）或Dice（38.0），说明两种损失在优化目标上互补——Dice关注全局重叠度，BCE提供逐点精细梯度。

### 推理置信度

推理时，每个预测实例的最终置信度由语义类别置信度和掩码内平均置信度联合决定：

$$c = c_{\text{cl}} \cdot \big( \Sigma_i^M m_i \cdot [m_i > 0.5] \big) / \big( \Sigma_i^M [m_i > 0.5] \big)$$

其中 $c_{\text{cl}}$ 为Softmax分类概率，$m_i$ 为掩码模块输出的连续热力值。该设计有效抑制了高分类置信度但掩码质量差的假阳性预测。



## 实验与关键发现

### 主要结果

Mask3D在四个主流3D实例分割基准上均取得了当时最优性能，验证了Transformer架构在该任务上的有效性。

**ScanNet v2**（Tab. I）：在测试集上，Mask3D达到**56.6 mAP**和**78.0 mAP50**，相比此前最优方法**SoftGroup**（Vu et al., CVPR 2022）的50.4 mAP，提升**+6.2 mAP**；相比**SSTNet**（Liang et al., ICCV 2021）的50.6 mAP，同样优势显著。验证集上达到55.2 mAP和73.7 mAP50。推理速度方面，Mask3D在TITAN X GPU上单场景耗时**339 ms**（不含后处理），与SoftGroup的345 ms相当，表明性能提升未以推理效率为代价。

**S3DIS**（Tab. II）：在6折交叉验证上，Mask3D达到**64.5 mAP**（无预训练），相比SoftGroup的约54.4 mAP提升**+10.1 mAP**。从ScanNet预训练后微调，Area 5上mAP进一步提升约1.2个点（61.8 vs 60.6），说明模型具有良好的迁移能力。

**ScanNet200**（Tab. III左）：该基准包含200个类别，按样本频率分为head/common/tail三组。Mask3D在head类达到**38.3 mAP**，common类**26.3 mAP**，tail类**16.8 mAP**，整体mAP相比此前最优方法**LGround**（Rozenberszki et al., ECCV 2022）的27.5 mAP提升**+10.8 mAP**。这一结果证明Mask3D对长尾分布场景的适应能力明显优于依赖手工分组的方法。

**STPLS3D**（Tab. III右）：在室外航空点云数据集上，Mask3D达到**57.3 mAP**，相比SoftGroup的46.2 mAP提升**+11.2 mAP**，验证了方法对室外大尺度场景的泛化性。

### 消融实验

**查询类型（Tab. IVa）**：非参数查询（FPS采样坐标 + 零初始化特征）达到**40.6 mAP**，优于参数查询的39.7 mAP。这一结果表明，基于场景几何的自适应查询比学习固定查询模板更有效，且非参数查询允许推理时动态调整查询数量而无需重新训练。

**损失函数（Tab. IVb）**：Dice损失与BCE损失的加权组合（40.6 mAP）显著优于单独使用Dice（38.0 mAP）或BCE（27.0 mAP）。Dice损失单独使用已远优于BCE，说明区域重叠度量对掩码预测的优化更为关键，但两者互补可进一步提升分割质量。

**查询数量与解码器层数（Fig. 3）**：查询数量从100增至200带来轻微提升，但边际递减。Transformer解码器层数≥12时性能趋于稳定，表明深层迭代有助于查询逐步细化，但过深层数收益有限。

**特征主干对比（Tab. V）**：较小主干Res16UNet18B达到40.0 mAP，接近大主干Res16UNet34C的40.9 mAP，表明Mask3D的性能不严重依赖特定主干架构，Transformer解码器设计本身贡献了主要增益。模型参数分析（Tab. VI）显示，>90%的参数来自特征主干，Transformer解码器仅约1.76M参数。

**DBSCAN后处理（Tab. VII, Fig. 7）**：Mask3D偶尔将两个同类实例合并为单个掩码（如两个相邻窗户）。可选的DBSCAN后处理通过空间邻近性分割错误合并的实例，最优距离阈值ε在ScanNet为**0.9**，S3DIS Area5为**0.6**，STPLS3D为**14.0**。这一后处理有效缓解了合并错误，但引入了数据集依赖的超参数。

### 失败模式分析

Mask3D的主要失败模式是**同类实例合并**（Fig. 4左下、Fig. 7）。当两个同类物体（如窗户）在几何和语义特征上高度相似时，注意力机制可能将它们合并为单一实例。根本原因在于，掩码交叉注意力虽然约束查询关注其预测掩码内部，但当两个实例的点特征响应接近时，查询难以在特征空间中明确区分边界。DBSCAN后处理可部分缓解此问题，但最优阈值需针对数据集单独调整，说明模型尚未完全内化实例边界分离能力。

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2210_03105/figures/016_Figure_7.jpg]]
*Figure 7: Qualitative Analysis of DBSCAN Postprocessing. Mask3D occassionally predicts masks containing two instances of the same class. In (b), two windows are merged into a single instance since their underlying point cloud features result in a high response when convolved with the instance query (c.f. heatmap in (c)). In (d), we apply DBSCAN as a postprocessing routine to split erroneously merged instances based on spatial contiguity. We do not see this effect for voting-based methods as they explicitly encode geometric priors (e)-(f)*

### 关键图表结论

- **Fig. 1**：展示Mask3D端到端流程——输入点云经Transformer注意力机制直接输出所有实例的热力图和语义标签。
- **Fig. 2**：详细架构——稀疏体素主干提取多尺度特征，Transformer解码器迭代细化实例查询，掩码模块通过点积生成二进制掩码。
- **Fig. 5**：完整架构图，展示5个尺度特征层级和多层查询细化，比Fig. 2更详尽。
- **Fig. 6**：定性对比——Mask3D相比SoftGroup能更好地处理任意形状物体（如U形桌），不依赖手工几何先验（如中心点）和分组机制。
- **Tab. I–III**：四个基准上的一致大幅领先，验证了集合预测范式的通用性。
- **Tab. IV**：核心消融，确立了非参数查询和Dice+BCE联合损失的优越性。

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2210_03105/figures/014_Figure_6.jpg]]
*Figure 6: (e) Instance Prediction Fig. 6: Qualitative Comparison to SoftGroup [56]. We compare Mask3D with the current top-performing voting-based approach SoftGroup. The top example shows a scene containing a single large U-shaped table, see (e) in pink. SoftGroup is based on center-voting and tries to predict the instance center, shown in (b) in red. However, predicting centers of such very large non-convex shapes can be difficult for voting-based approaches. Indeed, SoftGroup fails to correctly segment the table and returns two partial instances (c). Our Mask3D, on the other side, does not rely on hand-selected geometric properties such as centers and can handle arbitrarily shaped and sized object...*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2210_03105/figures/009_Figure_5.jpg]]
*Figure 5: TABLE V: Feature Backbones. We experimented with convolutional and transformer-based feature backbones ( c . f . Fig. 5, ◻∎)*

### 补充图表

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2210_03105/figures/003_Table.jpg]]
*Table: I: 3D Instance Segmentation Scores on ScanNet v2. We report mean average precision (mAP) with different IoU threshold over 18 classes on the ScanNet validation and test set. The inference speed is averaged over the validation set and computed on a TITAN X GPU (c.f. ), excluding postprocessing. Test scores accessed on 13. September 2022. TABLE II: 3D Instance Segmentation Scores on S3DIS. We report mean average precision (mAP) with different IoU threshold (as in ) as well as mean precision (mPrec) and mean recall (mRec) with 50% IoU threshold (as in ) over 13 classes on S3DIS Area 5 and 6-fold cross validation. Scores in light gray are pre-trained on ScanNet and fine-t...*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2210_03105/figures/004_Table.jpg]]
*Table: III: 3D Instance Segmentation Scores on ScanNet200 and STPLS3D. We report mean average precision (mAP) with different IoU threshold over 14 classes on the STPLS3D test set. Hidden test scores accessed on 13. September 2022*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2210_03105/figures/006_Table.jpg]]
*Table: IV: Ablations. a) We explore two variants for query positions and features. Parametric queries 1 are learned during training. Non-parametric queries consist of FPS point positions 2 and potentially their features 3 , resembling scene-specific queries. b) We optimize the instance mask prediction using the binary crossentropy loss \mathcal { L } _ { C E } and the dice loss \mathcal { L } _ { d i c e } . A weighted combination of dice and cross-entropy loss results in best performance. a) Query Type b) Mask Loss*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2210_03105/figures/007_Figure_3.jpg]]
*Figure 3: Number of queries and decoder layers*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2210_03105/figures/012_Figure.jpg]]
*Figure: (d)Exemplary Heatmap (e) Instance Prediction (b） Center Votes (c) Instance Prediction*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2210_03105/figures/010_Table.jpg]]
*Table: VI: Model sizes. We compare Mask3D’s model size against recent top-performing methods. For all models, most parameters are in the feature backbone and only a small fraction is in the instance segmentation specific part of the models*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2210_03105/figures/011_Table.jpg]]
*Table: VII: Ablation on DBSCAN postprocessing. To split wrongly merged instances, we employ DBSCAN as an optional postprocessing routine. We report best scores around a minimal distance =0.9 (ScanNet) and =0.6 (S3DIS-A5)*



## 定位与知识库关联

### 从手工投票到端到端集合预测

在Mask3D之前，3D实例分割的主流范式经历了从**自底向上聚类**到**投票-分组**的演进，但始终未能摆脱对手工几何先验的依赖。早期工作如**SGPN**（Wang et al., CVPR 2018）学习逐点相似矩阵进行分组，**GSPN**（Yi et al., CVPR 2019）引入生成式提案网络，**3D-SIS**（Hou et al., CVPR 2019）和**3D-BoNet**（Yang et al., NeurIPS 2019）则分别从检测和直接掩码预测角度探索。这些方法的核心瓶颈在于：实例的获取依赖于非端到端的后处理步骤（如聚类、非极大抑制），使得优化目标与最终评估指标之间存在鸿沟。

投票-分组路线的代表性工作**PointGroup**（Jiang et al., CVPR 2020）和**HAIS**（Chen et al., CVPR 2021）通过学习偏移向量将点汇聚到实例中心，再结合语义分割进行聚类，显著提升了性能。**SoftGroup**（Vu et al., CVPR 2022）进一步引入自顶向下的分组策略，成为Mask3D出现前的SOTA（ScanNet test 50.4 mAP）。然而，这些方法的因果机制仍建立在“物体有明确几何中心”这一隐含假设之上，对于非凸形状（如L形桌子）或密集堆叠场景，中心投票的歧义性会导致系统性错误。

Mask3D的**核心范式转变**在于：将3D实例分割重新建模为**集合预测问题**。这一思路借鉴了2D领域的DETR和MaskFormer，但其关键创新在于针对3D点云的稀疏性和无序性设计了非参数实例查询与掩码交叉注意力机制。具体而言：

- **实例表示层面**：传统方法依赖中间几何表示（中心偏移、边界框），而Mask3D直接维护一组实例查询，每个查询编码一个完整实例的语义和几何信息。查询的初始化采用最远点采样（FPS）选取场景中的点坐标，特征初始化为零——即所谓的“非参数查询”。消融实验证实，这种场景感知的初始化优于可学习的参数查询（mAP 40.6 vs 39.7，Tab. IVa），表明让查询从场景几何出发比从随机向量出发更有利于收敛。

- **掩码生成层面**：传统方法通过聚类投票中心或优化边界框间接获得实例掩码，而Mask3D直接计算查询特征与点特征的点积，经Sigmoid后阈值化得到二进制掩码（Eq. 1）。这一设计消除了对“实例中心”这一几何概念的依赖，使模型能够处理任意形状的物体。定性对比（Fig. 6）显示，SoftGroup在处理U形大桌子时倾向于将其分割为多个实例，而Mask3D能够完整保留其连通结构。

- **训练匹配层面**：传统方法通常采用最近邻匹配或固定分配策略，而Mask3D引入匈牙利算法进行最优二分图匹配（Eq. 4），联合优化掩码和分类损失。这一机制确保了训练过程中预测实例与真值实例的一一对应，避免了手工匹配规则引入的偏差。

- **上下文利用层面**：掩码交叉注意力（Eq. 3）是Mask3D的关键设计——每个查询仅关注其当前预测掩码内的体素，屏蔽外部区域。这种“聚焦”机制强制查询在迭代细化过程中逐步收缩到实例内部，类似于2D MaskFormer中的masked attention，但针对3D稀疏体素进行了采样和填充适配。

### 与后续工作的关系与适用边界

Mask3D的出现推动了3D实例分割从“投票-分组”向“查询-掩码”范式的转移，其影响力体现在以下几个方面：

**方法层面的可迁移性**：Mask3D的非参数查询设计表明，Transformer解码器的查询不需要从可学习的嵌入出发，而可以从场景本身采样。这一发现为后续的开放词汇3D分割（如基于CLIP特征的多模态查询）提供了技术基础。论文中提到的**LGround**（Rozenberszki et al., ECCV 2022）已尝试将语言特征融入3D实例分割，Mask3D的查询机制天然适合此类扩展。

**数据集的泛化能力**：Mask3D在四个数据集上验证了其有效性——室内场景ScanNet（+6.2 mAP）、S3DIS（+10.1 mAP）、大规模长尾ScanNet200（+10.8 mAP整体提升）以及室外航拍STPLS3D（+11.2 mAP）。值得注意的是，在ScanNet200上，Mask3D在头部、常见、尾部类别上分别达到38.3、26.3、16.8 mAP，而此前最佳方法**CSC**（Hou et al., ECCV 2022）和LGround分别为27.5和27.5 mAP（Tab. III）。这表明基于注意力的实例查询对长尾分布具有较强的鲁棒性，因为查询的初始化不依赖类别先验。

**计算效率的权衡**：Mask3D的Transformer解码器仅占约1.76M参数，模型参数主要来自稀疏卷积主干（>90%）。推理速度（339 ms on TITAN X）与SoftGroup（345 ms）相当，但显著优于基于Transformer主干的变体。消融实验（Tab. V, supplementary）表明，即使使用较小的Res16UNet18B主干，性能下降有限（40.0 vs 40.9 mAP），说明模型不严重依赖特定主干架构。

然而，Mask3D的适用边界同样清晰：

**对空间后处理的残留依赖**：尽管Mask3D声称端到端，但注意力机制偶尔会合并语义和几何相似但空间分离的实例（如两个窗户）。论文引入DBSCAN后处理来分离此类错误合并（Fig. 7），其最优距离阈值需针对不同数据集单独调整（ScanNet: 0.9, S3DIS: 0.6, STPLS3D: 14.0, Tab. VII）。这引入了少量超参数，削弱了“完全端到端”的宣称。

**对稀疏体素主干的依赖**：Mask3D仍建立在MinkowskiEngine的稀疏卷积之上，对极高分辨率点云可能存在内存限制。论文未在室外自动驾驶数据集（如Waymo、nuScenes）上进行验证，这些场景的点云密度和范围远超室内环境。

**对静态场景的假设**：非参数查询的FPS采样基于单帧点云，未考虑时序一致性。在动态场景或在线处理中，如何利用帧间查询的延续性仍是开放问题。

### 局限与开放问题

基于论文明确指出的局限性和分析中揭示的边界，可提炼以下开放问题：

1. **合并错误的根本解决**：掩码交叉注意力能否通过改进查询设计或损失函数，完全消除对DBSCAN后处理的依赖？例如，引入对比损失惩罚不同查询之间的特征相似度，或在注意力中显式编码空间距离先验，可能从机制层面减少合并错误。

2. **大规模室外场景的扩展**：该方法如何扩展到自动驾驶等室外大规模点云而不显著增加计算成本？非参数查询的采样策略（FPS）在超大点云上的效率可能成为瓶颈，需要探索基于空间哈希或层次化查询的加速方案。

3. **多模态查询的潜力**：论文已验证了非参数查询优于参数查询，但查询的初始化方式仍有探索空间——能否将文本、图像或时序信息融入查询初始化，实现更灵活的条件实例分割？LGround已初步探索了语言接地，Mask3D的架构为此提供了更通用的框架。

4. **查询数量的自适应**：论文提到推理时可以使用与训练时不同数量的查询，但查询数量仍是一个全局超参数。能否设计自适应机制，根据场景复杂度动态决定查询数量，避免简单场景的冗余计算和复杂场景的漏检？

5. **与2D-3D联合模型的融合**：Mask3D的集合预测范式与2D的MaskFormer、Mask2Former高度兼容，未来工作可探索统一的2D-3D联合实例分割框架，利用多视角一致性进一步提升3D分割精度。



## 原文 PDF

![[paperPDFs/ICRA_2023/Mask3D_Mask_Transformer_for_3D_Instance_Segmentation.pdf]]
