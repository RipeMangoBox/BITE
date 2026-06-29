---
title: "Textured Mesh Quality Assessment: Large-scale Dataset and Deep Learning-based Quality Metric"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_2023/Textured_Mesh_Quality_Assessment_Large_scale_Dataset_and_Deep_Learning_based_Quality_Metric.pdf
project_link: null
code_link: "https://github.com/MEPP-team/Graphics-LPIPS"
aliases:
- GL
- TMQALSDDLBQM
tags:
- SIGGRAPH_2023
- topic/graphics_geometry_processing
- topic/graphics_rendering_materials
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过构建包含343k失真网格、3000个主观评分的大规模数据集，并设计基于渲染图块和预训练CNN的深度学习度量Graphics-LPIPS，实现对纹理网格视觉质量的准确预测。
primary_logic: 将3D图形质量评估转化为渲染图像的感知相似度任务，利用在图像上预训练的CNN特征提取器，通过学习局部图块的池化权重来逼近人类视觉感知，无需显式建模几何与纹理的交互作用。
claims:
- Graphics-LPIPS在纹理网格数据集上显著优于现有图像质量度量（PLCC、SROCC、AUC均最高）
- 在顶点颜色网格数据集上，Graphics-LPIPS达到PLCC=0.89, SROCC=0.88，优于其他度量
- 所构建数据集包含343k以上失真网格，3000个主观评分，是规模最大的纹理网格质量数据集
- Textured Mesh Dataset (View-Independent) 上 PLCC = 0.84
---

# Textured Mesh Quality Assessment: Large-scale Dataset and Deep Learning-based Quality Metric

> [!tip] 核心洞察
> 将3D图形质量评估转化为渲染图像的感知相似度任务，利用在图像上预训练的CNN特征提取器，通过学习局部图块的池化权重来逼近人类视觉感知，无需显式建模几何与纹理的交互作用。

| 字段 | 内容 |
|------|------|
| 中文题名 | 纹理网格质量评估：大规模数据集与基于深度学习的质量度量 |
| 英文题名 | Textured Mesh Quality Assessment: Large-scale Dataset and Deep Learning-based Quality Metric |
| 会议/期刊 | SIGGRAPH 2023 |
| Links | [paper](https://arxiv.org/abs/2202.02397) · [Code](https://github.com/MEPP-team/Graphics-LPIPS) |
| Topic | #topic/graphics_geometry_processing #topic/graphics_rendering_materials #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Graphics-LPIPS |
| Dataset | Textured Mesh Dataset, Vertex Color Mesh Dataset [Nehmé et al. 2021b] |

> [!tip] 效果简介
> - Textured Mesh Dataset (View-Independent) 上，PLCC 0.84 vs 0.69 (SSIM) (+0.15)；SROCC 0.83 vs 0.67 (SSIM) (+0.16)。
> - Vertex Color Mesh Dataset [Nehmé et al. 2021b] 上，PLCC 0.89 vs N/A (best other metric) (N/A)；SROCC 0.88 vs N/A (best other metric) (N/A)。

## 概要

纹理网格的质量评估长期受限于大规模主观评分数据集的缺失，导致基于深度学习的客观度量难以训练与验证。本文构建了包含超过343k失真网格、3000个主观评分（MOS）的大规模纹理网格质量数据集，并提出一种基于深度学习的图像域质量度量 **Graphics-LPIPS**。该方法将3D图形质量评估转化为渲染图像的感知相似度任务：从参考与失真模型的渲染视图中提取重叠图块，经预训练CNN（AlexNet）与可学习校准层提取特征后，以图块级L2距离的空间平均作为质量预测分数，无需显式建模几何与纹理的交互作用。在纹理网格数据集上，Graphics-LPIPS 的 PLCC 达到0.84、SROCC 达到0.83，显著优于 SSIM 等传统图像质量度量；在顶点颜色网格数据集上同样取得最优结果（PLCC=0.89, SROCC=0.88）。该方法可视为 LPIPS（Zhang et al., CVPR 2018）在3D图形领域的扩展，其核心定位在于以渲染图块为输入、以学习型特征校准替代手工特征的全参考图像质量评估范式。

## 核心方法与创新机理

### 问题瓶颈与转化思路

纹理网格质量评估的核心瓶颈在于：**缺乏大规模带有主观评分的公开数据集**，使得基于深度学习的客观质量度量难以训练和验证。现有3D质量数据集规模过小（仅数百个失真刺激），远不足以驱动深度度量学习。同时，几何失真（顶点量化、LoD简化）与纹理失真（压缩、子采样）之间存在复杂的交互效应，传统手工设计特征难以捕捉这种跨模态的感知退化。

本文的关键转化思路是：**将3D图形质量评估转化为渲染图像的感知相似度任务**。通过从固定视角渲染纹理网格获得2D图像，利用在自然图像上预训练的CNN作为特征提取器，学习局部图块的池化权重来逼近人类视觉感知，而无需显式建模几何与纹理的交互作用。这一思路的合理性在于：人类最终是通过观察渲染结果来评判3D内容质量的，因此渲染图像的质量退化直接反映了3D失真的感知影响。

### 方法框架：Graphics-LPIPS

所提出的Graphics-LPIPS是一个全参考（full-reference）的深度学习感知度量，其输入为参考渲染图像与失真渲染图像的图块对，输出为该图像对的感知距离。整个框架由以下模块按顺序构成：

**模块1：视角渲染**  
将参考3D模型与失真3D模型分别从预设视角渲染为2D图像。基础设置采用一个主视角（front view），扩展设置可采用4个均匀采样的视角以增强视角覆盖的鲁棒性。

**模块2：图块采样器**  
从渲染图像中提取重叠的64×64像素图块，滑动步幅为32像素。为排除背景区域的干扰，采样器会剔除背景像素占比较高的图块，仅保留包含有效模型内容的图块参与后续计算。

**模块3：特征提取器（AlexNet F）**  
采用在ImageNet上预训练的AlexNet作为骨干网络，从多个中间层提取特征图。对于每个输入图块，网络前向传播后获得各层的特征表示。这些预训练特征已编码了丰富的纹理和结构信息，构成了感知相似度计算的基础。

**模块4：校准层（1×1卷积）**  
这是Graphics-LPIPS相对于原始LPIPS的关键创新之一。在每个特征提取层之后，插入一个可学习的1×1卷积层，其权重 $w_l$ 用于对通道维度的特征进行重新校准。校准层的引入使得网络能够自适应地调整不同特征通道对感知距离的贡献，从而更好地拟合人类主观评分。

**模块5：图块距离计算**  
对于参考图块 $x^r$ 和失真图块 $x$，将其分别送入特征提取器与校准层后，在每一层 $l$ 获得校准后的特征向量 $\hat{y}^r_l$ 和 $\hat{y}_l$。图块间的感知距离定义为各层L2距离的加权和：

$$d(x^r, x) = \sum_l \frac{1}{H_l W_l} \sum_{h,w} \| w_l \odot (\hat{y}^r_{l,hw} - \hat{y}_{l,hw}) \|_2^2$$

其中 $H_l$、$W_l$ 为第 $l$ 层特征图的空间尺寸，$w_l$ 为校准层的通道权重，$\odot$ 表示逐通道乘法。

**模块6：空间池化（平均池化）**  
单张渲染图像的质量预测值 $\hat{Q}_I$ 由所有有效图块距离的平均值给出：

$$\hat{Q}_I = \frac{1}{N_p} \sum_{i=1}^{N_p} d(x_i^r, x_i)$$

其中 $N_p$ 为该图像的有效图块数量。消融实验表明，平均池化优于L2池化、L3池化或最大池化，因为平均池化能更稳定地聚合局部失真信息。

**模块7：视角聚合（多视角设置）**  
当采用多视角渲染时，对每个视角分别计算图像级质量分数，然后取平均得到刺激级质量预测值 $\hat{Q}_S$。这一简单聚合策略在实验中展现出良好的视角鲁棒性。

### 训练路径

Graphics-LPIPS的训练目标是最小化预测质量与主观平均意见分（MOS）之间的均方误差：

$$E_I = (\hat{Q}_I - MOS_I)^2$$

训练仅更新校准层的权重 $w_l$，而特征提取器AlexNet的权重保持冻结。这种设计既保留了预训练特征的通识感知能力，又通过轻量级校准层实现了对特定图形失真类型的适配。训练数据来自所构建的大规模纹理网格数据集，包含343k以上失真刺激，其中3000个刺激具有人工主观评分（MOS），其余刺激通过伪MOS进行标注。

### 推理路径

推理阶段，给定一对参考与失真的纹理网格模型：
1. 从指定视角（单视角或多视角）渲染获得图像对；
2. 对每张图像提取重叠图块，过滤背景图块；
3. 每个图块对通过冻结的AlexNet与训练好的校准层计算感知距离；
4. 图块距离取平均得到图像级质量分；
5. 若为多视角，各视角分数取平均得到最终质量预测值。

### 三个关键Changed Slots

**Changed Slot 1：校准层（相对于原始LPIPS）**  
原始LPIPS直接使用预训练网络的特征差异计算L2距离，仅在训练时学习各层的线性组合权重。Graphics-LPIPS在此基础上为每层增加了1×1卷积校准层，实现了**通道级**的自适应特征重加权。这一改进使得度量能够更精细地建模不同特征通道对图形失真感知的差异化贡献，是性能提升的核心机制之一。

**Changed Slot 2：图块化与池化策略**  
原始LPIPS对整张图像计算特征差异后进行空间平均。Graphics-LPIPS则将图像划分为64×64的重叠图块（步幅32），独立计算每个图块的感知距离后再取平均。这一策略的优势在于：局部图块能更敏感地捕获几何量化、纹理压缩等局部失真，同时通过去除背景图块避免了无关区域对质量预测的干扰。

**Changed Slot 3：输入模态**  
不同于通用图像质量度量直接处理整张自然图像，Graphics-LPIPS的输入是**从3D渲染管线获得的图块对**。这一设计将3D图形质量评估与渲染视角绑定，使得度量能够隐式地感知几何与纹理的交互失真——例如，LoD简化导致的几何退化在不同纹理复杂度下对渲染图像的影响差异，可通过图块级特征差异被捕获。

### 模块间因果关系

整个pipeline的因果链可概括为：**渲染视角选择**决定了哪些几何/纹理信息被投影到2D图像 → **图块采样**将全局失真问题分解为局部感知单元的集合 → **预训练CNN**提供通识的纹理与结构特征表示 → **校准层**将这些通用特征映射到图形失真特定的感知空间 → **图块距离**量化局部退化程度 → **平均池化**将局部退化聚合为全局质量判断。各模块的协同使得Graphics-LPIPS无需显式建模几何与纹理的交互，即可在纹理网格和顶点颜色网格两种不同类型的数据集上均取得最优性能。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2202_02397/figures/012_Figure_9.jpg]]
*Figure 9: Graphics-LPIPS architecture: to compute a distance*

## 实验与关键发现

### 数据集构建与主观实验

本工作构建了迄今规模最大的纹理网格质量评估数据集，包含 **55个源模型**（覆盖家具、动物、人体、交通工具、建筑等语义类别，顶点数从约1万到超过100万），通过几何量化、纹理坐标量化、LoD简化、纹理压缩与子采样等失真类型生成 **超过343k失真刺激**。从该全量刺激中，通过双伪MOS平面约束采样选取 **3000个刺激** 进行主观实验（Fig. 5），获得平均主观意见分（MOS）。主观评分分布（Fig. 7）覆盖了从几乎不可见失真到极度令人厌烦失真的完整质量范围，为训练和验证深度学习度量提供了可靠基础。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2202_02397/figures/007_Figure_5.jpg]]
*Figure 5: Selection of the test stimuli by constrained sampling of the plane formed by 2 pseudo-MOSs. The black dots refer to the pseudo-MOS values of all stimuli in the dataset, while the blue dots refer to those selected for the subjective experiment*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2202_02397/figures/011_Figure_7.jpg]]
*Figure 7: Distribution of (a) raw scores and (b) MOSs for the subset of 3000 stimuli rated in the subjective experiment*

### 主实验结果：纹理网格数据集

在视角无关（View-Independent）设置下，Graphics-LPIPS在测试集上显著优于所有对比的全参考图像质量度量。**Table 4** 报告了核心指标对比：

- **PLCC（皮尔逊线性相关系数）**：Graphics-LPIPS 达到 **0.84**，最优传统度量 SSIM 仅为 0.69，提升 **+0.15**；
- **SROCC（斯皮尔曼秩相关系数）**：Graphics-LPIPS 达到 **0.83**，SSIM 为 0.67，提升 **+0.16**；
- **AUC（区分失真/未失真刺激的能力）**：Graphics-LPIPS 同样最高。

Fig. 10 以五折交叉验证的平均值和标准差展示了这一优势：Graphics-LPIPS 在所有三个指标上均领先于 SSIM、MS-SSIM、VIF、VIFP、FSIM、GMSD、HDR-VDP2 以及原始 LPIPS（Zhang et al., CVPR 2018）。值得注意的是，**原始 LPIPS 在该数据集上表现并不突出**，说明直接迁移整图级感知度量无法有效捕获纹理网格的视觉退化特征，图块化与校准层是性能提升的关键。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2202_02397/figures/014_Figure_10.jpg]]
*Figure 10: Performance of our metric (Graphics-LPIPS) compared to stateof-the-art image metrics. The reported numbers are averages over our five folds while the error bars show the standard deviation over the folds*

Fig. 11 的 MOS-预测值散点图进一步显示，Graphics-LPIPS 的预测经 Logistic 回归后与主观评分高度一致，点云紧密分布在回归曲线两侧，表明度量对不同源模型和失真类型具有一致的相关性。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2202_02397/figures/013_Figure_11.jpg]]
*Figure 11: MOS vs. quality metric values for the test set of textured meshes. Each point represents a distorted stimulus identified by its source model. The curve shows the logistic regression*

### 跨数据集泛化：顶点颜色网格

在 Nehmé et al.（2021b）的顶点颜色网格数据集上，Graphics-LPIPS 同样取得最优表现（**Table 3**）：
- **PLCC = 0.89**，**SROCC = 0.88**；
- 对比的其他度量中，最优者为 MS-SSIM（PLCC = 0.82, SROCC = 0.81），Graphics-LPIPS 分别领先 +0.07 和 +0.07。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2202_02397/figures/016_Table_3.jpg]]
*Table 3: Performance comparison of different metrics on a dataset of meshes with vertex colors. For metrics marked with*

这一跨数据集验证表明，尽管 Graphics-LPIPS 在纹理网格数据上训练，其学到的图块级感知特征对顶点颜色网格的失真也具有良好泛化能力。但需注意，该数据集规模较小，且失真类型与纹理网格数据集存在差异，因此该结果仍需在更多样化的顶点颜色数据上进一步验证。

### 多视角聚合的影响

Table 4 同时报告了多视角设置下的性能。当每刺激使用 **4个均匀采样视角** 并取平均分数时，Graphics-LPIPS 的性能保持稳定且仍居最优。这表明：
1. 图块级特征提取对视角变化具有一定鲁棒性；
2. 简单的视角平均聚合策略在实际应用中可行，但更复杂的注意力加权机制（如学习不同视角的感知重要性）可能带来进一步提升，这仍是开放问题。

### 光照与材质鲁棒性

Fig. 12 展示了光照方向变化对度量性能的影响：当光源在水平或垂直方向偏离主视角的规范方向时，Graphics-LPIPS 的 PLCC/SROCC 仅有轻微波动，表现出良好的光照鲁棒性。Fig. 13 进一步测试了暗光、聚光灯、光泽材质和金属材质等非标准条件，预测分数仍保持与主观评分的较高相关性。但需注意，**这些测试均在单一漫反射纹理假设下进行**——数据集本身未包含金属度、粗糙度、法线贴图等 PBR 材质属性，因此该鲁棒性结论的边界在于：当材质属性显著偏离训练分布（如高光反射、复杂 BRDF）时，度量的可靠性仍需独立验证。

### 消融分析：池化策略

对图块距离的空间池化策略进行消融表明，**平均池化优于 L2、L3 或最大池化**（Section 5.1, Section 7）。这一结果暗示：纹理网格的视觉失真通常分布在多个局部区域，而非集中在单个最差图块；平均池化能更稳定地综合各图块的退化信息，避免最大池化对异常值的过度敏感。

### 关键失真类型的感知规律

数据集分析揭示了若干对图形压缩与传输具有指导意义的感知规律：

- **几何量化**（Fig. 14a）：顶点位置量化对 MOS 的影响在低比特量化时急剧上升，且该效应与模型的几何复杂度 $SI_{Geo}$ 正相关（Fig. 20a）——几何复杂度越高的模型，对位置量化的容忍度越低。
- **纹理坐标量化**（Fig. 14b）：纹理坐标量化的感知影响相对温和，但受颜色复杂度 $SI_{Col}$ 调节（Fig. 21）——颜色纹理越复杂的模型，对 UV 坐标量化的退化越敏感。
- **LoD简化**（Fig. 15）：随着面片数减少，MOS 单调下降，且该效应与位置量化存在交互作用（Fig. 17-18）——当位置已被严重量化时，进一步 LoD 简化的感知惩罚更为显著。
- **纹理压缩与子采样**（Fig. 16）：纹理压缩（如 JPEG 质量因子降低）和子采样均导致 MOS 下降，且两者存在交互效应（Fig. 19）——同时施加两种失真时，感知质量的恶化大于单独失真之和。

这些交互效应揭示了纹理网格质量评估中 **几何失真与纹理失真的耦合性**，也解释了为何简单的独立质量指标难以准确预测整体感知质量——这正是 Graphics-LPIPS 通过学习局部图块特征隐式建模这种耦合的优势所在。

### 失败模式与适用边界

尽管 Graphics-LPIPS 在现有数据集上表现优异，但其适用边界明确：

1. **材质假设限制**：训练数据仅包含单一漫反射纹理，不支持金属度、粗糙度、法线贴图等 PBR 材质。在光泽或金属材质（Fig. 13）上的测试仅为初步验证，未进行系统评估。
2. **注意力机制缺失**：当前度量对所有图块和视角赋予均等权重，忽略了人类视觉的选择性注意机制。在某些刺激上，失真集中在显著区域时，平均池化可能低估感知退化；反之，在背景区域失真时可能高估。
3. **与专用3D度量的比较有限**：论文未与 PCQM、MSDM2 等专用3D网格/点云度量进行充分对比，无法断言基于渲染图像的度量在所有场景下优于几何域度量。
4. **源模型多样性**：55个源模型虽覆盖多种语义类别，但对于真实世界3D内容的多样性而言仍显不足，尤其在有机形状、高细节雕刻等类别上可能存在覆盖盲区。
5. **交互式检查模式未涉及**：主观实验采用被动观察模式，而实际3D图形应用中用户常进行旋转、缩放等交互操作，不同检查模式对质量感知的影响尚不明确。

## 定位与知识库关联

### 1. 本质差异：从“图像质量度量”到“图形渲染感知度量”

Graphics-LPIPS 的核心定位是将 3D 纹理网格的质量评估问题**转化为渲染图像的局部感知相似度学习问题**。与现有工作的本质差异体现在以下 slot 的改变上：

| 改变的 Slot | 已有基线方法 | Graphics-LPIPS 的变更 |
|---|---|---|
| **输入表征** | 直接对整张渲染图像计算距离（如 **LPIPS** (Zhang et al., CVPR 2018)） | 将渲染图像切分为 64×64 重叠图块（步幅 32 像素），以图块对作为网络输入 |
| **空间池化策略** | LPIPS 对全图特征差异取空间平均或直接输出 | 学习图块级的 L2 距离后，对 $N_p$ 个图块距离取算术平均，得图像级质量分 $\hat{Q}_I = \frac{1}{N_p} \sum_{i=1}^{N_p} d(x_i^r, x_i)$ |
| **特征校准** | LPIPS 直接使用预训练 CNN 的特征通道差异 | 在特征提取后插入 1×1 卷积层，学习通道级权重 $\omega_0$ 以校准特征响应，提升与主观评分的相关性 |
| **训练监督** | LPIPS 在图像感知相似度数据集上训练（如 BAPPS） | 在自建的纹理网格主观评分数据集上，以 MSE 损失 $E_I = (\hat{Q}_I - MOS_I)^2$ 端到端训练 |

这一系列变更的因果链条是：**图块化**使得局部几何/纹理失真的感知信号不被整图平均所淹没；**1×1 校准层**赋予网络学习“哪些特征通道对图形失真更敏感”的能力；**MSE 监督**将度量直接锚定在 3D 图形的主观评分上，而非自然图像的感知相似度。

### 2. 知识库挂载点

Graphics-LPIPS 可挂载到以下知识库节点：

- **全参考图像质量评估（FR-IQA）**：继承自 SSIM（Wang et al., IEEE TIP 2004）、FSIM（Zhang et al., IEEE TIP 2011）、HDR-VDP2（Mantiuk et al., SIGGRAPH 2011）等经典度量，但将这些度量的手工特征替换为预训练 CNN 特征 + 可学习校准层。
- **深度感知相似度**：直接继承 **LPIPS**（Zhang et al., CVPR 2018）的特征提取架构，但将“整图感知相似度”迁移到“渲染图块感知质量”这一新任务域。
- **3D 图形质量评估数据集**：填补了现有数据集（如 Nehmé et al. 2021b 的顶点颜色网格数据集仅约数百个失真刺激）规模不足的空白，构建了包含 343k+ 失真网格、3000 个 MOS 的大规模数据集，为深度学习方法在 3D 图形质量评估领域的应用提供了数据基础。

### 3. 适用边界

- **材质范围**：仅支持单一漫反射纹理（diffuse texture），未考虑金属度、粗糙度、法线贴图等 PBR 材质属性。在光泽（glossy）或金属（metallic）材质上的泛化能力未经充分验证（Fig. 13 仅做了初步探索）。
- **失真类型**：训练和验证覆盖的失真类型包括几何量化、LoD 简化、纹理压缩、纹理子采样、纹理坐标量化及其组合。对于未见的失真类型（如网格平滑、纹理合成伪影），泛化性能需手动验证。
- **视角假设**：单视角模式假设渲染视角固定（主视角），多视角模式（4 个均匀采样视角）可提升鲁棒性，但未探索自由视角交互式检查场景。
- **注意力建模缺失**：当前度量对所有图块赋予等权（平均池化），忽略了人类视觉注意力机制。在注意力高度集中的场景（如人脸模型、文字纹理）中，预测精度可能下降。
- **数据集多样性**：源模型仅 55 个，覆盖 10 个语义类别。对于训练集语义分布之外的模型类别，度量性能的置信度较低。

### 4. 后续启发

Graphics-LPIPS 为以下研究方向提供了起点：

1. **注意力加权池化**：将视觉注意力模型（如 Salicon）集成到图块池化阶段，学习不同图块和视角的感知权重，替代当前的平均池化策略。这是论文明确指出的开放问题。
2. **多材质扩展**：将输入从漫反射纹理扩展到 GGX 参数化（法线、粗糙度、高光贴图），使度量适用于现代游戏和电影资产的完整材质评估。
3. **跨显示设备校准**：论文指出显示设备（桌面显示器 vs. VR/AR 头显）对感知质量的影响尚未研究，这是一个具有实用价值的知识空白。
4. **无参考度量的构建**：当前度量是全参考（需参考渲染图），但所构建的大规模数据集（含 340k+ 伪 MOS 标注）可直接用于训练无参考（NR）质量度量，这是数据集贡献的直接延伸。
5. **与专用 3D 度量的融合**：论文与专用 3D 网格度量（如 MSDM2、PCQM）的比较有限。将渲染图像感知特征与 3D 几何特征（如曲率、法线差异）融合，可能进一步提升对纯几何失真的敏感度。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2023/Textured_Mesh_Quality_Assessment_Large_scale_Dataset_and_Deep_Learning_based_Quality_Metric.pdf]]