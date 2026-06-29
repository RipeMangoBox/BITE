---
title: "DifferSketching: How Differently Do People Sketch 3D Objects?"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/DifferSketching_How_Differently_Do_People_Sketch_3D_Objects.pdf
project_link: null
code_link: "https://github.com/chufengxiao/DifferSketching"
aliases:
- DifferSketching
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_animation_interaction
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过在同一参考图像上同时采集专业与新手用户的草图，并引入三层配准（草图级、笔画级、像素级），实现空间与时间维度上的量化差异分析，揭示了绘画技能导致的具体差异因素。
primary_logic: 专业与新手用户绘制三维物体时，在笔画级的内属性（形状、比例）和外属性（位置、旋转、缩放）上存在显著差异；专业用户的笔画精确度更高，但两者在绘制顺序和整体内容感知上相似。新手用户在全局缩放、局部笔画放置和比例一致性方面尤为困难。这些差异可用于指导手绘风格合成和三维重建的评估基准。
claims:
- 专业与新手用户在三层配准下的旋转、平移、缩放误差均存在显著差异（LMM检验，p<0.001）。
- "新手用户在笔画级缩放误差上显著更大：仅23%的笔画缩放因子在[0.9, 1.1]范围内，专业为45%。"
- 辅助线能显著降低新手和专业用户的全局缩放误差与像素级误差（p<0.001），且更多辅助线与新手更低像素误差相关（r=-0.18, p<0.001）。
- 手绘风格合成方法在感知研究中能达到与真实用户草图相当的欺骗率（U-test p=0.32，与用户草图无显著差异）。
---

# DifferSketching: How Differently Do People Sketch 3D Objects?

> [!tip] 核心洞察
> 专业与新手用户绘制三维物体时，在笔画级的内属性（形状、比例）和外属性（位置、旋转、缩放）上存在显著差异；专业用户的笔画精确度更高，但两者在绘制顺序和整体内容感知上相似。新手用户在全局缩放、局部笔画放置和比例一致性方面尤为困难。这些差异可用于指导手绘风格合成和三维重建的评估基准。

| 字段 | 内容 |
|------|------|
| 中文题名 | DifferSketching：不同绘画经验者如何不同地绘制三维物体草图 |
| 英文题名 | DifferSketching: How Differently Do People Sketch 3D Objects? |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://chufengxiao.github.io/DifferSketching/) · [Code](https://github.com/chufengxiao/DifferSketching) |
| Topic | #topic/graphics_animation_interaction #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DifferSketching 数据集与三层分析方法 |
| Dataset |  |

> [!tip] 效果简介
> - 组间差异分析 (Novice vs. Professional) 上，旋转/平移/缩放误差（三层） 专业用户在三层均显著优于新手（p<0.001） vs 新手用户误差更大 (例如像素级平移误差：新手8.67±14.14像素，专业5.17±8.94像素)。
> - 辅助线影响分析 上，全局平移误差 E_GT，缩放误差 E_GS，像素级误差 E_P 使用辅助线后E_GT、E_GS、E_P显著降低（p<0.001） vs 未使用辅助线 (新手E_GT: 130.79→104.06; 专业E_GT: 97.98→76.83)。
> - 手绘风格合成感知研究 上，平均投票率（被选为最不真实的比例） 合成图投票率与用户草图无显著差异（p=0.32） vs 描摹图投票率显著不同（p=1.4e-7） (合成图能有效欺骗观察者)。

## 概要

现有手绘草图数据集规模小、对象类别少，且主要来自专业用户，缺少专业与新手用户的直接对比。同时，训练用草图多采用与三维模型严格对应的算法生成线稿，导致基于学习的方法对新手用户的抽象与变形草图泛化能力差。

本文提出 **DifferSketching** 数据集与三层分析方法。作者同时招募 70 名新手与 38 名专业用户，对 136 个三维模型的 362 个多视角参考图像进行手绘，每人每图由 5 名新手与 5 名专业用户绘制，共收集 3,620 幅手绘草图。在此基础上，引入三层配准框架——草图级相似变换、笔画级相似变换、像素级迭代优化——从空间与时间维度量化两组用户在旋转、平移、缩放等方面的差异。

主要发现：专业与新手用户在笔画级的内属性（形状、比例）和外属性（位置、旋转、缩放）上存在显著差异（LMM 检验，p<0.001）；新手在局部笔画缩放上尤为困难，仅 23% 的笔画缩放因子处于合理范围，而专业用户为 45%；辅助线能显著降低两组的全局缩放与像素级误差。此外，基于配准笔画的三阶段学习式扰动方法可合成具有手绘风格的草图，在感知研究中与真实用户草图无显著差异。专业用户草图在单视图三维重建任务中比新手草图获得更优的定量指标。

方法定位上，DifferSketching 在用户群体（专业+新手）、数据集规模（362 提示 × 10 次重复）和配准方案（三层配准）三个关键维度上区别于仅含专业用户的小规模数据集（如 OpenSketch、SpeedTracer），为手绘风格分析与三维重建评估提供了新的基准。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

现有手绘草图数据集存在三重结构性缺陷：**用户群体单一**（仅专业用户）、**规模小且类别少**（通常≤24个提示）、**训练数据依赖算法生成线稿**（如Canny边缘、Suggestive Contours）。这导致基于学习的方法对新手用户的抽象与变形草图泛化能力极差，因为算法线稿在笔画形状、比例、抖动等方面与真实手绘存在系统性偏差（Fig. 2, Fig. 10）。

本文的核心洞察在于：专业与新手用户在绘制三维物体时，差异主要体现在**笔画级的内属性**（形状、比例）和**外属性**（位置、旋转、缩放），而非整体内容感知或绘制顺序。通过在同一参考图像上同时采集两组用户的草图，并引入**三层配准体系**，可以将这些差异量化为可测量、可比较的参数，进而指导手绘风格合成和三维重建评估。

### 改变的三个关键设计槽位

**槽位1：数据采集用户群体**。基线方法（如Princeton sketch dataset、OpenSketch、SpeedTracer）仅招募专业用户或未区分技能水平。本工作同时招募70名新手与38名专业用户，按绘画经验年限划分组别（Table 3），确保每个参考图像由5名新手和5名专业用户绘制，形成配对比较基础。

**槽位2：数据集规模与多视角覆盖**。基线数据集通常≤24个提示且重复数低。本工作从9个类别选取136个三维模型，在2-3个视角下渲染得到362个参考图像，最终收集3,620幅手绘草图，规模比同类数据集大一个数量级（Table 1）。

**槽位3：配准方案**。基线方法仅使用像素级或点级配准，无法分离全局与局部误差。本工作提出三层配准体系：草图级相似变换（全局姿态）、笔画级相似变换（局部姿态）、像素级迭代优化（精细对齐），使得空间维度上的差异可在不同粒度上独立分析。

### 方法流水线与模块因果关系

整个方法框架包含**数据采集→配准→分析→合成→评估**五个阶段，模块间的因果关系如下：

#### 模块1：数据采集界面（Fig. 3）

参与者在平板上观察左侧参考图像，在右侧画布上自由绘制。系统记录矢量笔画序列（包含时间戳、笔压、坐标），不限制绘制顺序或笔画数。同时，另招募一组参与者对相同参考图像进行**描摹**（tracing），描摹结果作为后续配准的基准（fiducial），因为描摹能最大程度保留参考图像的几何结构。

#### 模块2：像素级配准（Fig. 4）

![[assets/figures/papers/paper_list_l43_https_chufengxiao_github_io_DifferSketching/figures/007_Figure_4.jpg]]
*Figure 4: Examples of vector-sketch registration process. Given the model prompts in (a), (b) and (c) shows the corresponding tracings and users’ drawings (from Novice 8 (Top) and Novice 18 (Bottom)). (d) illustrates the pipeline of our proposed pixel-level registration, which registers a sequence of vector strokes to the corresponding tracings by iteratively alternating rasterization and point-to-point registration. (e) visualizes the registered results of each iteration, where the drawing pixels that have not been registered correctly are in red and the tracing pixels to be registered by the drawings are in blue, while the pixels overlapped by them are in black. The bottom text of each image indica...*

这是三层配准的**基础层**，解决手绘草图与描摹基准之间的非刚性对齐问题。核心机制是**迭代光栅化-优化循环**：

1. 将矢量笔画光栅化为二值图像，初始线宽为$w_0$。
2. 使用点对点配准方法（扩展自SpeedTracer）将光栅化笔画与描摹基准对齐。
3. 计算精度$P_i = \frac{o\_num_i}{reg\_num_i}$（重叠像素占已配准像素的比例）和召回率$R_i = \frac{o\_num_i}{trac\_num}$（重叠像素占描摹像素的比例）。
4. 若当前迭代的加权得分$E = \omega P_i + R_i$未收敛，则**动态增大线宽**$w$后重新光栅化，使更多未对齐区域参与下一次优化。
5. 选择使$E$最大的迭代次数$i^*$作为最优配准结果：

$$i^{*} = \underset{i}{\operatorname{argmax}} E = \underset{i}{\operatorname{argmax}} \omega P_{i} + R_{i}$$

该策略的关键创新在于**自动选取最优迭代次数**，避免手动调参，同时通过动态线宽机制防止优化陷入局部极小。

#### 模块3：草图级与笔画级配准（Fig. 5）

在像素级配准基础上，引入两个额外的配准方案以**分离全局与局部变形**：

- **草图级配准**：对整个草图估计一个相似变换（旋转$R$、均匀缩放$S$、平移$T$），最小化与描摹基准的点点距离：

$$[ R_s^* | T^* ] = \arg_{[R_s|T]} \sum_i \| dst[i] - R_s \, src[i]^T - T \|^2$$

- **笔画级配准**：对每个独立笔画估计相似变换，但变换参数是**相对于草图级变换的残差**，从而剥离全局姿态影响，聚焦于局部笔画的放置精度和比例控制。

这一设计使得三类误差可被独立量化：旋转误差$E_R = R$、平移误差$E_T = T$、缩放误差$E_S = |S - 1|$。

#### 模块4：外参扰动器（Extrinsic Disturber）

手绘风格合成的第一阶段。输入为描摹笔画，使用MLP预测每个笔画的相似变换参数（旋转、平移、缩放）。MLP的训练数据来自笔画级配准中提取的专业/新手用户的外参误差分布，因此可以**分别学习两种技能水平的扰动模式**。

#### 模块5：内参扰动器（Intrinsic Disturber）

合成的第二阶段。对经过外参变换的Bézier曲线控制点施加MLP预测的变形，模拟手绘笔画的形状不规则性（如直线变弯、圆变扁）。训练数据来自像素级配准后笔画形状与描摹基准的残差。

#### 模块6：点扰动器（Point Disturber）

合成的第三阶段。在笔画路径上添加高斯噪声，模拟手部微颤导致的**高频抖动**。噪声水平可调节，控制合成草图的“手绘感”强度（Supplemental Fig. 7）。

#### 模块7：布局优化（Layout Refinement）

上述三阶段扰动是逐笔画独立进行的，可能导致笔画间关系不协调。布局优化模块通过最小化位置、形状和平滑度三项能量来调整整体布局：

- **位置项**：约束相邻笔画的相对位置保持合理。
- **形状项**：防止笔画过度变形。
- **平滑度项**：基于笔画间距的Softmax权重$w_j = \text{softmax}_{j<i}(1 / (dist(t_i^\alpha, t_j^\beta) + 1))$，使后续笔画的位置受已绘制笔画的平滑影响。

### 从配准到分析的因果链

三层配准不仅是合成方法的训练数据来源，更直接支撑了空间维度的差异分析：

1. **像素级配准**揭示两组用户在精细对齐后的残余像素距离分布（Fig. 6），发现整体分布相似，但专业用户在细节部位一致性更高。
2. **笔画级配准**揭示新手在局部缩放上错误显著更多：仅23%的笔画缩放因子在[0.9, 1.1]合理范围内，专业为45%（Section 5.2）。
3. **草图级配准**揭示新手在全局缩放和放置上的系统性偏差，尤其是对复杂三维结构的比例感知困难。

![[assets/figures/papers/paper_list_l43_https_chufengxiao_github_io_DifferSketching/figures/027_Figure_6.jpg]]
*Figure 6: The pipeline of our freehand-style sketch synthesis method. Each two rows of images show novice-style and professional-style generation, both of which are fed with the same noise levels (??1=??2). Each stroke of the sketches is color-coded to highlight their changes*

### 训练与推理路径

- **配准算法**：无需训练，为优化驱动的迭代过程。描摹基准作为半自动初始化（人工标注关键点），随后自动迭代至收敛。
- **手绘风格合成**：外参和内参扰动器的MLP在配准数据上监督训练（输入为描摹笔画特征，输出为变换参数/变形向量）；推理时输入任意描摹笔画，依次经过三个扰动器和一个布局优化，输出具有目标技能风格的手绘草图。
- **三维重建评估**：使用预训练的PSGN、Pixel2Mesh等方法，直接以用户草图为输入，不涉及额外训练。

### 边界条件与失效模式

配准算法对**高度抽象或透视严重错误**的草图可能失败（如新手将三维物体画成完全扁平的二维符号），此类数据在预处理阶段被剔除。手绘风格合成方法**依赖已配准的描摹笔画**作为起点，无法直接从三维模型端到端生成，限制了全自动化程度。辅助线分析基于用户自述使用情况（Table 4），未进行随机对照实验，因果推断需谨慎。

![[assets/figures/papers/paper_list_l43_https_chufengxiao_github_io_DifferSketching/figures/015_Figure_11.jpg]]
*Figure 11: (a) The pipeline of our freehand-style sketch synthesis method. The two rows of images show novice-style and professional-style generation, both of which are fed with the same noise levels*

## 实验与关键发现

DifferSketching 的实验设计围绕一个核心问题展开：专业与新手用户在绘制三维物体时，究竟在哪些维度上存在可量化的差异？为此，作者构建了一个包含 3,620 张手绘草图的配对数据集，并通过三层配准框架（草图级、笔画级、像素级）对两组用户的绘制行为进行空间与时间维度的系统比较。实验证据的强度由线性混合模型（LMM）的显著性检验和效应量支撑，关键发现如下。

### 1. 三层配准下的组间差异分析

作者对每一张用户草图与对应的描摹基准（tracing）进行三层配准，分别提取旋转误差 $E_R$、平移误差 $E_T$ 和缩放误差 $E_S$，并通过 LMM 检验组间差异。Table 2（主文）报告了核心统计结果：专业用户在所有三个配准层级上的误差均显著低于新手用户（p < 0.001）。以像素级配准后的平移误差为例，新手用户的平均误差为 8.67 ± 14.14 像素，而专业用户为 5.17 ± 8.94 像素，后者不仅均值更低，方差也更小，表明专业用户的绘制一致性更高。

![[assets/figures/papers/paper_list_l43_https_chufengxiao_github_io_DifferSketching/figures/005_Table_2.jpg]]
*Table 2: Category-level statistics for our DifferSketching. We show the basic quantity of the collected dataset*

**笔画级分析揭示了更为精细的差异模式。** 在草图级配准消除全局变换后，笔画级配准捕捉到的是局部笔画相对于整体布局的偏差。统计显示，新手用户仅有 23% 的笔画其缩放因子落在 [0.9, 1.1] 的合理区间内，而专业用户这一比例为 45%。这意味着新手用户在局部笔画的比例控制上存在系统性困难——他们倾向于将某些笔画绘制得过大或过小，破坏了物体各部分之间的比例关系。旋转和平移误差在笔画级同样呈现显著的组间差异，但缩放误差的效应最为突出，构成了区分两组技能水平的关键特征。

像素级分析进一步补充了上述发现。Figure 6(a) 展示了新手与专业用户像素级最近距离的直方图分布，两条曲线形状相似，表明两组用户在整体绘制内容的覆盖范围上并无本质区别——他们都试图描绘参考图像的相同语义区域。然而，Figure 6(c) 的定性对比显示，专业用户在细节部位（如机械零件的边缘、动物的四肢关节）的绘制一致性明显更高，新手用户的笔画在这些区域往往出现位置漂移或形状失真。

### 2. 辅助线的影响

辅助线（scaffold lines）是用户在绘制前自行绘制的参考线，用于规划物体的比例和布局。Table 4 报告了有无辅助线条件下两组用户的误差对比。核心发现是：辅助线能显著降低新手和专业用户的全局平移误差 $E_{GT}$ 和全局缩放误差 $E_{GS}$（p < 0.001）。以新手用户为例，使用辅助线后，$E_{GT}$ 从 130.79 降至 104.06，$E_{GS}$ 也有明显改善。像素级误差 $E_P$ 同样显著降低。

更重要的是，补充材料中的 Spearman 相关性分析显示，辅助线数量与新手用户的像素级误差呈显著负相关（r = -0.18, p < 0.001），即绘制更多辅助线的新手用户，其草图的像素级精度更高。这一发现揭示了辅助线作为一种认知补偿策略的有效性——新手用户通过外化空间参考框架，部分弥补了其内在比例感知能力的不足。

**需要指出的是，辅助线分析存在方法学局限。** 参与者是否使用辅助线完全基于自述，未进行随机分组强制干预，因此结果可能受到自我选择偏差的影响——那些本身空间感知能力较强的用户可能更倾向于绘制辅助线，而辅助线本身并非唯一的因果因素。这一结论需要后续的对照实验来验证。

### 3. 手绘风格合成的感知验证

作者提出了一种三阶段学习式框架，将描摹笔画转化为具有手绘风格的草图：外参扰动器（MLP 预测旋转、平移、缩放）、内参扰动器（MLP 变形 Bézier 曲线路径）、点扰动器（高斯噪声模拟抖动），并通过布局优化目标函数保证笔画间关系的平滑性。

为验证合成草图的逼真度，作者进行了感知研究：48 名参与者被要求从三张草图中选出“最不像是人手绘”的一张，三张图分别为描摹图、真实用户草图、合成草图。Figure 11(b) 报告了平均投票率——描摹图被选出的比例显著高于用户草图和合成草图（U-test p = 1.4e-7），而合成草图与用户草图的投票率无显著差异（p = 0.32）。这意味着观察者无法可靠地区分合成草图与真实用户草图，合成方法成功捕捉了手绘风格的关键视觉特征。

### 4. 单视图草图的三维重建评估

Table 5 报告了四种代表性单视图三维重建方法（Pixel2Mesh、3D-R2N2、Occ-Net、PSGN）分别以新手草图（N）和专业草图（P）为输入时的定量指标。在所有方法中，PSGN 取得了最低的倒角距离（Chamfer Distance, CD），其中专业输入的结果（CD = 1.911 × 10⁻³）优于新手输入（CD = 2.168 × 10⁻³）。IoU 指标同样显示专业草图能带来更高的重建质量。

**但这一评估存在重要的适用边界。** 所有重建网络均使用算法生成的线稿（如 Canny 边缘、Suggestive Contours）进行训练，而非真实手绘草图。这意味着训练分布与测试分布之间存在系统性偏移——网络从未见过手绘草图的抽象、变形和抖动特征。因此，Table 5 的结果反映的是“网络对专业草图中更接近算法线稿的几何特征的利用能力”，而非“网络对手绘风格的理解能力”。这一发现实际上揭示了现有三维重建方法在处理非专业用户输入时的泛化瓶颈，而非证明了专业草图的固有优越性。

### 5. 数据集规模的对比定位

Table 1 将 DifferSketching 与现有手绘草图数据集进行了多维度对比。相较于 Princeton Sketch Dataset（Cole et al., 2008）的 24 个提示、OpenSketch（Gryaditskaya et al., 2019）的专业设计师 CAD 草图、SpeedTracer（Wang et al., 2021）的仅专业用户数据，DifferSketching 在提示数量（362 个多视角提示）、用户技能覆盖（专业+新手）、重复绘制次数（每提示 5 名专业 + 5 名新手）三个维度上均实现了数量级的扩展。这一规模优势使得组间统计比较具有足够的统计效力，能够检测到中等效应量的差异。

![[assets/figures/papers/paper_list_l43_https_chufengxiao_github_io_DifferSketching/figures/003_Table_1.jpg]]
*Table 1: Comparisons of the closely related freehand sketch datasets from various perspectives. The “User” column indicates the drawing skill levels of the participants involved in the data collection: “N/A” means no clear indication or specific requirement of the types of the users; “P” and “N” represent professional and novice users, respectively. The “Repetition” column reports the number of times for each prompt drawn by different users in each dataset. In the “View” column, “S” represents single views mostly used for data collection while “M” means the collection of multi-view sketches. “N/A” in the “Category” column means that there is no clear categorical division in the corresponding dataset...*

### 6. 失败模式与适用边界

尽管实验证据整体稳健，以下边界条件值得关注：

- **配准失败**：对于高度抽象或透视严重错误的草图，迭代光栅化配准算法可能无法收敛到合理的对齐结果。作者在数据清洗阶段剔除了这些样本，但未报告剔除比例，这可能引入幸存者偏差——被保留的草图本身具有更好的可配准性，从而可能低估了新手用户的真实困难程度。
- **文化背景局限**：参与者主要来自香港地区，其视觉教育和绘画传统可能影响结果的跨文化普适性。
- **类别覆盖有限**：数据集仅包含 9 个类别 136 个三维模型，对于具有复杂拓扑或非刚性结构的物体类别，现有结论的推广需要谨慎。
- **合成方法的依赖链**：手绘风格合成依赖已配准的描摹笔画作为输入，无法从三维模型端到端生成，限制了其在自动化数据增强场景中的应用。

![[assets/figures/papers/paper_list_l43_https_chufengxiao_github_io_DifferSketching/figures/014_Figure_10.jpg]]
*Figure 10: Comparison between the algorithm-generated line drawings and the freehand sketches with different registration strategies. (a) shows qualitative comparisons of two sets of drawings by different methods. We dilated the generated results for clear demonstration in this figure. For the user sketches shown on the right, the three columns (from left to right) represent the sketch-level, stroke level, and pixel-level registered versions of the original sketches, respectively; the upper row and the lower row illustrate sketches from novices and professionals, respectively. (b), (c), and (d) illustrate the precision (Top) and recall (Bottom) comparisons between different levels (sketch-level, strok...*

## 定位与知识库关联

DifferSketching 在现有手绘草图研究版图中的核心定位是：**首次系统构建了同时包含专业与新手用户、在统一参考图像条件下采集的大规模多视角三维物体手绘草图数据集**，并以此为基础揭示了绘画技能差异在空间与时间维度上的具体表现。其本质改变在于将数据采集的“用户群体”这一关键 slot 从“仅专业用户”扩展为“专业+新手双群体对比”，从而使得技能差异的量化分析成为可能。

### 相对已有数据集的本质差异

在手绘草图数据集谱系中，早期里程碑工作如 **Princeton sketch dataset**（Cole et al., SIGGRAPH 2008）首次提供了笔画级标注的专业用户草图，但其参与者全部为经过筛选的艺术家/设计师，且仅覆盖 20 个对象类别。**OpenSketch**（Gryaditskaya et al., TOG 2019）将规模扩展至多视图 CAD 设计草图，但同样仅面向专业设计师群体，且缺乏明确的语义类别划分。**SpeedTracer**（Wang et al., 2021）虽引入了描摹与手绘的对比分析框架，其参与者仍限定为专业用户。这些数据集的共同局限在于：无法回答“专业与新手在绘制同一三维物体时究竟有何不同”这一基础问题，导致基于此类数据训练的算法（如三维重建网络）对新手用户的抽象、变形草图泛化能力不足。

DifferSketching 改变的 slot 具体包括：
- **用户群体**：从“仅专业用户”变为“70 名新手 + 38 名专业用户”，每组用户按绘画经验年限明确划分（专业用户平均 8.6 年经验，新手用户平均 1.2 年）。
- **数据集规模与重复性**：从“≤24 个提示、低重复数”变为“362 个多视角提示，每个提示由 5 名新手 + 5 名专业用户绘制”，总计 3,620 幅手绘草图，规模较同类笔画级数据集提升一个数量级。
- **配准方案**：从“仅像素级或点级配准”变为“三层配准——草图级相似变换、笔画级相似变换、像素级迭代优化”，使得差异分析可在全局布局、局部笔画形状、逐像素精度三个粒度上展开。
- **对比基准**：引入另一组参与者对参考图像进行描摹（tracing），作为配准的 fiducial 基准，替代了传统方法中直接使用算法生成线稿（如 Canny 边缘、Suggestive Contours）作为 ground truth 的做法。

### 知识库挂载点

该工作可挂载至以下知识库节点：

1. **手绘草图数据集谱系**（Sketch Dataset Taxonomy）。DifferSketching 填补了“双技能群体对比”这一空白维度，可作为后续研究的基准数据集。其三层配准框架为其他技能差异研究（如医学草图、儿童绘画发展）提供了可复用的分析范式。

2. **手绘风格分析与合成**（Freehand Style Analysis & Synthesis）。论文揭示的专业—新手差异因素（笔画级缩放误差分布、外参与内参扰动的统计特性）直接指导了手绘风格合成方法的设计。该合成框架的三阶段扰动策略（外参扰动器 → 内参扰动器 → 点扰动器）将技能差异建模为可学习的变换分布，为“从描摹生成特定技能水平的手绘草图”提供了可操作的 pipeline。

3. **单视图三维重建的鲁棒性评估**（Single-View 3D Reconstruction Robustness）。论文以新手和专业草图分别作为输入，评估了四种代表性重建方法（Pixel2Mesh、3D-R2N2、Occ-Net、PSGN），结果表明专业输入在所有方法上均获得更优的 IoU 和 Chamfer Distance。这一发现为三维重建方法的鲁棒性测试提供了新的评估维度：不应仅在算法生成线稿或专业草图上评估，还需考虑新手用户的输入退化。

### 适用边界与局限

DifferSketching 的适用性受以下因素制约：
- **类别与对象覆盖有限**：数据集仅包含 9 个语义类别、136 个三维模型，且模型选择偏向人造物体（如椅子、飞机、汽车），未覆盖有机形态或复杂场景。将其分析结论推广至更广泛的物体类别时需要谨慎。
- **参与者群体偏差**：参与者主要来自香港地区，其视觉文化与绘画训练背景可能影响结果的跨文化普适性。专业/新手的划分基于自述的绘画经验年限，未采用标准化的绘画能力测试。
- **配准方法边界**：像素级迭代配准虽通过动态线宽增量和自动停止准则（$i^{*} = \underset{i}{\operatorname{argmax}} \omega P_{i} + R_{i}$）提高了鲁棒性，但对于透视严重错误或高度抽象化的草图仍可能失败，导致部分数据被剔除（具体剔除比例需查证原文）。
- **辅助线分析的因果性不足**：辅助线使用基于用户自述，未进行随机对照实验，因此“辅助线降低误差”的结论仅能解释为相关性而非因果效应，可能受自我选择偏差影响。
- **合成方法的自动化限制**：手绘风格合成依赖已配准的描摹笔画作为输入，无法直接从三维模型端到端生成，限制了其在大规模数据增强场景中的应用。

### 后续研究启发

基于 DifferSketching 的分析发现，若干后续方向具有明确的研究价值：
- **技能自适应三维重建**：利用合成的大规模手绘草图数据集微调预训练网络，使重建模型能根据输入草图的技能特征（如笔画缩放分布、局部变形程度）自适应调整解码策略，提升对新手输入的鲁棒性。
- **更细粒度的几何差异度量**：论文当前使用旋转、平移、缩放作为主要差异指标，后续可引入线条平行度、圆度、曲率单调性等更高级的几何度量，进一步细分专业与新手的感知与执行差异。
- **语义感知的配准与评估**：结合三维模型上的语义标注（如部件分割）作为配准基准，可研究不同技能用户在透视感知和部件比例描绘上的具体困难，为计算机辅助绘画教学提供诊断工具。
- **跨文化验证与扩展**：在不同文化背景和年龄段群体中复现该研究范式，验证技能差异的普适性，并探索文化因素（如书写系统、艺术教育传统）对手绘策略的影响。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/DifferSketching_How_Differently_Do_People_Sketch_3D_Objects.pdf]]