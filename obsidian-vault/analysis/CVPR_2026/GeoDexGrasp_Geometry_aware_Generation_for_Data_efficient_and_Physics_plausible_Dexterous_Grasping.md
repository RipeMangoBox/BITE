---
title: "GeoDexGrasp: Geometry-aware Generation for Data-efficient and Physics-plausible Dexterous Grasping"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GeoDexGrasp_Geometry_aware_Generation_for_Data_efficient_and_Physics_plausible_Dexterous_Grasping.pdf
project_link: "https://xjtbinghan.github.io/GDG.github.io"
code_link: null
aliases:
- GeoDexGrasp
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 引入对象中心几何表示（形状、尺寸、姿态、交互方向）和 SIM(3) 等变网络，将生成过程解耦为几何表示学习、姿态引导旋转生成和形状引导抓取生成三个阶段，使模型从几何语义出发适应物体变化。
primary_logic: 利用 SIM(3) 等变编码与自监督解耦预训练对齐低层等变/不变特征与高层姿态/形状语义，在 SO(3) 流形与欧氏空间中解耦根旋转和手指关节生成，从而以极少的参数实现高数据效率、强物理合理性与尺寸泛化能力。
claims:
- GeoDexGrasp 在五个基准上将平均穿透深度降低 40%，并获得最高的物理合理性。
- 仅使用 DexGraspAnything 1/5 以下的参数（28.7M），取得与之可比甚至更优的平均抓取成功率（60.1%）。
- 在仅 25% 训练数据的条件下，GeoDexGrasp 仍保持较高抓取成功率，数据效率显著优于基线。
- 在尺寸泛化实验中，GeoDexGrasp 在所有形状和尺寸（包括 OOD）上的成功率均超过对比方法。
---

# GeoDexGrasp: Geometry-aware Generation for Data-efficient and Physics-plausible Dexterous Grasping

> [!tip] 核心洞察
> 利用 SIM(3) 等变编码与自监督解耦预训练对齐低层等变/不变特征与高层姿态/形状语义，在 SO(3) 流形与欧氏空间中解耦根旋转和手指关节生成，从而以极少的参数实现高数据效率、强物理合理性与尺寸泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | GeoDexGrasp：面向数据高效且物理合理灵巧抓取的几何感知生成 |
| 英文题名 | GeoDexGrasp: Geometry-aware Generation for Data-efficient and Physics-plausible Dexterous Grasping |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Han_GeoDexGrasp_Geometry-aware_Generation_for_Data-efficient_and_Physics-plausible_Dexterous_Grasping_CVPR_2026_paper.html) · [Project](https://xjtbinghan.github.io/GDG.github.io) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | GeoDexGrasp |
| Dataset | 5个基准数据集 |

> [!tip] 效果简介
> - 5个基准数据集 (DGN, UDG, etc.) 上，平均穿透深度 (Physical Plausibility, mm) 13.6 vs DexGraspAnything (~22.6) (降低约40%)。
> - 5个基准数据集 上，平均抓取成功率 (Success Rate, %) 60.1 vs DexGraspAnything (约60) (持平)；参数量 (M) 28.7 vs DexGraspAnything (约150M) (减少 >80%)。
> - 尺寸泛化 (OOD) - 小立方体 上，成功率 (%) 84.4 vs 所有基线 (显著优于基线)。

## 概述

灵巧抓取生成是机器人操作中的核心难题，其目标是为任意物体生成物理合理且可执行的手部姿态。现有数据驱动方法（如 **DexGraspAnything** (Zhong et al., CVPR 2025)、**UniDexGrasp** (Xu et al., CVPR 2023) 等）虽取得显著进展，但普遍忽视物体内在的几何先验，依赖海量数据进行统计学习，导致三个突出问题：**数据效率低下**、**物理合理性差**（严重的手-物体穿透与过抓取），以及**对未见尺寸的泛化能力不足**。

GeoDexGrasp 的核心洞察在于：物体的几何属性（形状、尺寸、姿态、交互方向）是抓取生成最本质的约束条件，而非应被隐式编码的无关变量。基于此，该方法引入 **SIM(3) 等变网络**与**自监督解耦预训练**，将生成过程解耦为三个语义清晰的阶段——几何表示学习、姿态引导旋转生成和形状引导抓取生成——使模型从几何语义出发适应物体变化，而非将每一变体视为全新样本。

这一设计带来了因果层面的性能跃升：在五个基准数据集上，GeoDexGrasp 将平均穿透深度降低约 40%，取得最高的物理合理性，同时以仅 28.7M 参数（不到 DexGraspAnything 的 1/5）实现与之可比甚至更优的平均抓取成功率（60.1%）。在数据效率实验中，仅使用 25% 训练数据仍保持较高成功率；在尺寸泛化实验中，对所有形状和尺寸（含分布外设置）的成功率均超越对比方法。消融研究进一步证实，SO(3) 旋转与欧氏空间手指关节的解耦生成策略，以及几何解耦预训练，是物理合理性与成功率提升的关键因素。

尽管成果显著，GeoDexGrasp 仍存在局限性：尺寸表示到灵巧手运动的映射高度非线性，全局尺度因子的显式提取带来的改进有限；在复杂拓扑形状（如玩具马）上，所有方法的成功率均很低；方法依赖外部 PointSO 模型提供交互方向，系统整体效果受上游模块制约。这些瓶颈为未来的细粒度几何建模与跨尺度抓取策略迁移指明了方向。

## 背景与动机

灵巧抓取是机器人操作领域的核心挑战，其目标是为任意物体生成物理合理且功能有效的多指手抓取姿态。近年来，数据驱动方法在该领域取得了显著进展，代表性工作包括 **DexGraspNet**（Wang et al., arXiv 2022）、**UniDexGrasp**（Xu et al., CVPR 2023）、**GenDexGrasp**（Li et al., arXiv 2022）、**D(R,O) Grasp**（Wei et al., arXiv 2024）、**UGG**（Lu et al., ECCV 2024）以及当前的SOTA方法 **DexGraspAnything**（Zhong et al., CVPR 2025）。这些方法通常将物体点云直接编码为隐式特征，随后通过生成模型在欧氏空间中联合预测手部根旋转、平移和手指关节角。

然而，这种“端到端隐式编码+联合生成”范式存在两个根本性瓶颈。**第一，数据效率低下。** 现有方法忽视物体内在的几何先验——如姿态、形状和尺寸——转而依赖海量数据中的统计相关性来隐式学习这些属性。当一个物体发生旋转或缩放时，模型将其视为全新样本，无法复用已学到的抓取语义，导致参数量膨胀（DexGraspAnything 约 150M 参数）且对训练数据规模高度敏感。**第二，物理合理性不足。** 由于缺乏对物体几何结构的显式建模，生成的抓取姿态常出现严重的手-物体穿透和过抓取现象，在仿真和真实世界中均难以可靠执行。

上述瓶颈的深层原因在于：灵巧抓取本质上是一个**几何敏感**问题——抓取策略应当随物体的姿态、形状和尺寸变化而协变，而非被当作孤立样本重新学习。因此，核心问题转化为：**如何将物体内在的几何先验显式地注入生成过程，使模型从几何语义出发适应物体变化，从而在极少参数和数据的条件下实现高物理合理性与尺寸泛化能力？**

GeoDexGrasp 正是围绕这一核心问题展开。该方法的核心洞察是：利用 SIM(3) 等变编码与自监督解耦预训练，将低层等变/不变特征与高层姿态/形状语义对齐，进而在 SO(3) 流形与欧氏空间中解耦根旋转和手指关节的生成。通过这种几何感知的生成范式，模型能够以 DexGraspAnything 不足 1/5 的参数（28.7M），在五个基准数据集上将平均穿透深度降低约 40%，同时取得与之可比甚至更优的抓取成功率，并在仅 25% 训练数据的条件下仍保持较高的数据效率。

## 核心创新

GeoDexGrasp 的核心创新在于**将灵巧抓取生成从“数据驱动的统计学习”范式转向“几何感知的语义生成”范式**。现有数据驱动方法（如 **DexGraspAnything** (Zhong et al., CVPR 2025)）将物体视为原始点云编码，依赖海量数据隐式学习手-物交互模式，导致数据效率低、物理合理性差（严重穿透与过抓取），且对物体姿态、形状和尺寸变化缺乏显式建模能力。

GeoDexGrasp 通过以下三个关键维度的创新，系统性地改变了这一范式：

### 1. 物体几何表征：从隐式编码到显式语义解耦

传统方法使用原始点云编码或隐式特征，缺乏显式几何语义。GeoDexGrasp 引入 **SIM(3) 等变网络**，将物体点云显式分解为四种可解释且可迁移的几何表示（Equation 1）：

$$
\Theta = \Phi ( X ) : = ( \Theta _ { \mathrm { e } } , \Theta _ { \mathrm { i } } , \Theta _ { \mathrm { c } } , \Theta _ { \mathrm { s } } )
$$

其中 $\Theta_{\mathrm{e}}$ 为旋转等变特征，$\Theta_{\mathrm{i}}$ 为旋转/平移/尺度不变特征，$\Theta_{\mathrm{c}}$ 为质心，$\Theta_{\mathrm{s}}$ 为尺度因子。这些表示在物体刚体变换下遵循严格的等变/不变关系（Equation 2）：

$$
\Gamma \Theta = ( \Theta _ { \mathrm { e } } R , \Theta _ { \mathrm { i } } , s \Theta _ { c } R + t , s \Theta _ { s } ) = \Phi ( s X R + t )
$$

**关键创新**在于：通过**自监督解耦预训练**，强制等变特征与高层姿态语义对齐、不变特征与高层形状语义对齐。具体而言，预训练通过姿态回归和形状重建两个分支，最小化原始点云与重建点云之间的双向 Chamfer 距离（Equation 3），使低层等变/不变特征获得明确的高层语义解释。

### 2. 生成空间解耦：SO(3) 流形与欧氏空间分离

现有方法在欧氏空间直接联合生成根旋转、平移和手指关节角，忽视了旋转的流形结构。GeoDexGrasp 将抓取概率分布显式分解（Equation 4）：

$$
p ( g \mid X , { \hat { \Theta } } ) = p ( R \mid \xi ) \cdot p ( t , \theta \mid X , R , \zeta )
$$

- **姿态引导旋转生成**：在 SO(3) 流形上利用 IPDF 独立建模根旋转的条件分布 $p(R \mid \xi)$，条件为融合交互方向与姿态表示的特征。IPDF 通过离散体积划分计算归一化概率密度（Equation 5），避免了欧氏空间直接回归旋转的拓扑失配问题。
- **形状引导抓取生成**：以旋转不变后的点云和形状/尺寸表示为条件，通过扩散模型在欧氏空间生成手指关节角与根平移（Equation 7），并施加接触鼓励与穿透惩罚。

这种解耦设计使模型在各自适合的空间中学习，消融实验证实：解耦策略（旋转 vs. 手指）使物理合理性和成功率均显著提升（Table 3）。

### 3. 外部几何先验注入：交互方向引导

GeoDexGrasp 引入 **PointSO 基础模型**，根据语言提示（如“杯子把手”）推断物体交互方向，为旋转生成提供明确的几何参考。这一显式方向引导稳定了 SO(3) 空间中的旋转生成过程，消融实验表明其对旋转生成质量有正向贡献（Table 3 & Section 4.4）。

### 创新带来的系统性优势

上述三个维度的创新形成协同效应，带来以下系统性优势：

- **数据效率**：显式几何先验使模型在仅 25% 训练数据下仍保持较高成功率（Figure 4），数据效率显著优于基线。
- **物理合理性**：形状–尺寸几何表示显著减少抓取穿透，在五个基准上将平均穿透深度降低约 40%（Table 1）。
- **尺寸泛化**：SIM(3) 等变框架使模型能适应物体尺寸变化，在分布外（OOD）尺寸上的成功率均超过对比方法（Table 2）。
- **参数效率**：仅使用 **DexGraspAnything** 1/5 以下的参数（28.7M vs. ~150M），取得与之可比甚至更优的平均抓取成功率（60.1%，Table 1）。

## 整体框架

GeoDexGrasp 将灵巧抓取生成建模为一个**几何感知的三阶段流水线**，其核心设计哲学是：当物体发生姿态、形状或尺寸变化时，模型应能根据内在几何语义自适应调整抓取，而非将每个变体视为全新案例。为此，整个框架将生成过程解耦为**几何表示学习与提取**、**姿态引导旋转生成**和**形状引导抓取生成**三个递进阶段（Figure 2）。

![[assets/figures/papers/paper_list_l2256_https_openaccess_thecvf_com_content_CVPR2026_html_Han_GeoDexGrasp_Geomet/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of GeoDexGrasp. When the object undergoes variations in pose, shape, or size, we expect the model to adapt its predictions accordingly rather than treating them as entirely new cases. GeoDexGrasp consists of three stages. Stage 1: Geometric representation learning and extraction. A SIM(3)-equivariant network is employed for self-supervised disentangled pretraining to obtain transferable geometric representations aligned with high-level semantics. Stage 2: Pose-guided rotation generation. Rotational distributions in SO(3) space are generated conditioned on pose representations and interaction directions. Stage 3: Shape-guided grasp generation. A diffusion model conditioned on object...*

**输入与输出定义。** 系统以物体原始点云 $X \in \mathbb{R}^{N \times 3}$ 为输入，输出完整的灵巧手抓取姿态 $g = (R, t, \theta)$，其中 $R \in SO(3)$ 为根旋转，$t \in \mathbb{R}^3$ 为根平移，$\theta \in \mathbb{R}^D$ 为 $D$ 维手指关节角。此外，系统可选地接受自然语言提示（如“杯子把手”）以获取交互方向先验。

**Stage 1：几何表示学习与提取。** 该阶段从原始点云中提取四类可解释且可迁移的几何表示——交互方向、姿态、形状和尺寸。具体而言，一个 SIM(3) 等变编码器 $\Phi$ 将点云分解为旋转等变特征 $\Theta_{\mathrm{e}}$、旋转/平移/尺度不变特征 $\Theta_{\mathrm{i}}$、质心 $\Theta_{\mathrm{c}}$ 和尺度因子 $\Theta_{\mathrm{s}}$：

$$\Theta = \Phi(X) := (\Theta_{\mathrm{e}}, \Theta_{\mathrm{i}}, \Theta_{\mathrm{c}}, \Theta_{\mathrm{s}})$$

这些表示在物体刚体变换下遵循明确的等变/不变规则：$\Gamma\Theta = (\Theta_{\mathrm{e}}R, \Theta_{\mathrm{i}}, s\Theta_{\mathrm{c}}R + t, s\Theta_{\mathrm{s}}) = \Phi(sXR + t)$。为将低层等变/不变特征与高层姿态和形状语义对齐，该阶段引入**自监督解耦预训练**：通过姿态回归和形状重建两个分支，以最小化双向 Chamfer 距离为目标，强制等变特征编码姿态信息、不变特征编码形状语义。此外，PointSO 基础模型根据语言提示推断物体交互方向，为后续旋转生成提供明确参考。

**Stage 2：姿态引导旋转生成。** 根旋转 $R$ 在 $SO(3)$ 流形上独立建模，与手指关节解耦。给定融合了交互方向与姿态表示的条件变量 $\xi$，采用 IPDF（Implicit-PDF）在 $SO(3)$ 上建模条件概率密度 $p(R \mid \xi)$，并通过负对数似然 $\mathcal{L}_{\mathrm{rot}} = -\log(p(R_{\mathrm{gt}} \mid \xi))$ 监督训练。这一设计使旋转生成天然适应物体姿态变化。

**Stage 3：形状引导抓取生成。** 在获得根旋转 $R$ 后，先将物体点云旋转至规范姿态，再以旋转不变后的点云 $\widehat{X}$ 和形状/尺寸表示 $\zeta$ 为条件，通过去噪扩散概率模型在欧氏空间中生成手指关节角 $\theta$ 与根平移 $t$：

$$p_{\theta}(h_{0:T} \mid \widehat{X}, \zeta) = p(h_T) \prod_{\tau=1}^{T} p_{\theta}(h_{\tau-1} \mid h_{\tau}, \widehat{X}, \zeta, \tau)$$

其中 $h_0 = (t, \theta)$ 为去噪输出。扩散模型的训练损失联合优化 MSE、接触鼓励和穿透惩罚三项：

$$\mathcal{L}_{\mathrm{grasp}} = \eta_1 \mathcal{L}_{\mathrm{MSE}} + \eta_2 \mathcal{L}_{\mathrm{c}} + \eta_3 \mathcal{L}_{\mathrm{p}}$$

**模块间数据流。** 三阶段呈串行依赖：Stage 1 输出的姿态表示与交互方向融合为 $\xi$，驱动 Stage 2 生成 $R$；$R$ 与形状/尺寸表示共同构成条件，输入 Stage 3 扩散模型生成 $(t, \theta)$。最终将 $R$、$t$、$\theta$ 组装为完整抓取 $g$。这种解耦设计使得旋转在 $SO(3)$ 流形上学习、手指关节在欧氏空间中学习，各自在其自然空间内建模，从而以仅 28.7M 参数（不足 DexGraspAnything 的 1/5）实现了可比的抓取成功率和显著更优的物理合理性。

### 补充图表

![[assets/figures/papers/paper_list_l2256_https_openaccess_thecvf_com_content_CVPR2026_html_Han_GeoDexGrasp_Geomet/figures/001_Figure_1.jpg]]
*Figure 1: We propose a data-efficient, size-generalizable and physics-plausible method for dexterous grasp generation, which achieves State-Of-The-Art (SOTA) physical plausibility and competitive grasping performance with a relatively small number of parameters compared to previous SOTA methods*

## 核心模块与公式推导

GeoDexGrasp 的核心架构由三个解耦阶段构成：**几何表示学习与提取**、**姿态引导旋转生成**和**形状引导抓取生成**。其设计根植于一个关键洞察——将灵巧抓取的概率分布按几何语义分解，使旋转在 SO(3) 流形上独立建模，而手指关节与平移在欧氏空间中条件生成。

### 几何表示学习与提取（Stage 1）

该阶段的目标是从原始物体点云中提取四种可解释且可迁移的几何表示：交互方向、姿态、形状和尺寸。方法引入 SIM(3) 等变编码器，将输入点云 $X \in \mathbb{R}^{N \times 3}$ 分解为四个分量：

$$\Theta = \Phi(X) := (\Theta_{\mathrm{e}}, \Theta_{\mathrm{i}}, \Theta_{\mathrm{c}}, \Theta_{\mathrm{s}}) \tag{1}$$

其中 $\Theta_{\mathrm{e}}$ 为旋转等变特征，$\Theta_{\mathrm{i}}$ 为旋转/平移/尺度不变特征，$\Theta_{\mathrm{c}}$ 为质心，$\Theta_{\mathrm{s}}$ 为全局尺度因子。这些表示在物体刚体变换下遵循严格的等变/不变关系：

$$\Gamma\Theta = (\Theta_{\mathrm{e}} R,\; \Theta_{\mathrm{i}},\; s\Theta_{\mathrm{c}} R + t,\; s\Theta_{\mathrm{s}}) = \Phi(s X R + t) \tag{2}$$

即等变特征随旋转同步变换，不变特征保持不变，质心与尺度按变换参数更新。

为使低层等变/不变特征与高层几何语义对齐，GeoDexGrasp 设计了**自监督解耦预训练**策略。预训练通过姿态回归和形状重建两个分支，最小化原始点云与重建点云之间的双向 Chamfer 距离：

$$\mathcal{L}_{\mathrm{pretrain}} = \sum_{x \in X} \min_{y \in Y} \|x - y\|_2^2 + \sum_{y \in Y} \min_{x \in X} \|y - x\|_2^2 \tag{3}$$

这一预训练强制等变特征编码姿态信息、不变特征编码形状信息，为后续生成提供语义明确的几何条件。此外，Stage 1 引入外部 PointSO 基础模型，根据语言提示（如“杯子把手”）推断物体交互方向，为旋转生成提供显式参考。

### 姿态引导旋转生成（Stage 2）

灵巧抓取中根旋转位于 SO(3) 流形，与欧氏空间中的手指关节具有本质不同的几何结构。GeoDexGrasp 将完整抓取分布显式分解为两个条件分布：

$$p(g \mid X, \hat{\Theta}) = p(R \mid \xi) \cdot p(t, \theta \mid X, R, \zeta) \tag{4}$$

其中 $\xi$ 为融合交互方向与姿态表示的条件特征，$\zeta$ 为形状与尺寸表示。根旋转的条件分布 $p(R \mid \xi)$ 通过 IPDF（Implicit-PDF）在 SO(3) 流形上建模，利用离散体积划分计算归一化概率密度：

$$p(R \mid \xi) = \frac{p(\xi, R)}{p(\xi)} \approx \frac{1}{V} \frac{\exp(f(\xi, R))}{\sum_{i=1}^{N} \exp(f(\xi, R_i))} \tag{5}$$

其中 $f(\cdot)$ 为可学习能量函数，$V$ 为 SO(3) 上离散划分的体积。旋转生成采用负对数似然监督：

$$\mathcal{L}_{\mathrm{rot}} = -\log(p(R_{\mathrm{gt}} \mid \xi)) \tag{6}$$

### 形状引导抓取生成（Stage 3）

在根旋转确定后，手指关节角 $\theta$ 与根平移 $t$ 在欧氏空间中通过去噪扩散概率模型生成。以旋转不变后的点云 $\widehat{X}$ 和形状/尺寸表示 $\zeta$ 为条件，扩散反向过程为：

$$p_{\theta}(h_{0:T} \mid \widehat{X}, \zeta) = p(h_T) \prod_{\tau=1}^{T} p_{\theta}(h_{\tau-1} \mid h_{\tau}, \widehat{X}, \zeta, \tau) \tag{7}$$

其中 $h_0 = (t, \theta)$ 为目标抓取参数，$h_T \sim \mathcal{N}(0, I)$。

扩散模型的训练损失为加权组合，联合优化 MSE、接触鼓励和穿透惩罚：

$$\mathcal{L}_{\mathrm{grasp}} = \eta_1 \mathcal{L}_{\mathrm{MSE}} + \eta_2 \mathcal{L}_{\mathrm{c}} + \eta_3 \mathcal{L}_{\mathrm{p}} \tag{9}$$

其中 $\mathcal{L}_{\mathrm{c}}$ 引导手部内点逼近物体表面以鼓励合理接触，$\mathcal{L}_{\mathrm{p}}$ 惩罚手-物体穿透。总损失为 $\mathcal{L}_{\mathrm{rot}}$ 与 $\mathcal{L}_{\mathrm{grasp}}$ 的联合优化。

### 设计逻辑总结

三个模块的解耦设计使模型在各自合适的几何空间中学习：SO(3) 流形上的 IPDF 处理旋转的非欧结构，欧氏空间中的扩散模型处理平移和关节角的连续变化。SIM(3) 等变编码器与自监督预训练为这一解耦提供了语义对齐的几何条件，使得模型能以 28.7M 参数（不足 DexGraspAnything 的 1/5）实现可比的抓取成功率和显著更优的物理合理性。

## 实验与分析

### 主实验结果：物理合理性与参数效率的双重突破

GeoDexGrasp 在五个基准数据集上进行了系统评估，与 **DexGraspAnything** (Zhong et al., CVPR 2025)、**UniDexGrasp** (Xu et al., CVPR 2023)、**DexGraspNet** (Wang et al., arXiv 2022)、**GenDexGrasp** (Li et al., arXiv 2022)、**D(R,O) Grasp** (Wei et al., arXiv 2024) 和 **UGG** (Lu et al., ECCV 2024) 等方法进行了全面对比。

**Table 1** 汇总了定量对比的核心结论。在物理合理性（以平均穿透深度衡量）上，GeoDexGrasp 取得 **13.6 mm** 的最优结果，相较前 SOTA 方法 DexGraspAnything（约 22.6 mm）**穿透深度降低约 40%**，在所有方法中排名第一。在抓取成功率上，GeoDexGrasp 达到 **60.1%**，与 DexGraspAnything 持平，但参数量仅为 **28.7M**——不足后者的 **1/5**（DexGraspAnything 约 150M）。这一结果直接验证了核心洞察：通过显式注入对象几何先验，模型可以用极少的参数实现与大规模数据驱动方法可比的抓取性能，同时大幅提升物理合理性。

需要指出，GeoDexGrasp 的结果基于 10 次运行平均，而其他基线方法的结果直接取自已发表报告，可能在实验条件上存在细微差异。此外，参数统计仅包含生成网络部分，不包括外部固定组件（如 PointSO 和 SAM3D）。

**Figure 3** 的定性对比进一步佐证了上述结论：GeoDexGrasp 生成的抓取姿态展现出明显更少的手-物体穿透和更自然的接触分布，尤其在复杂几何区域（如把手、边缘）表现更为突出。

### 数据效率实验：几何先验降低数据依赖

为验证几何感知设计对数据效率的提升，GeoDexGrasp 在仅使用 **25% 训练数据** 的条件下与基线方法进行了对比。**Figure 4** 的结果表明，当训练数据大幅缩减时，GeoDexGrasp 仍保持较高的抓取成功率，而对比方法的性能出现明显下降。这一现象揭示了方法的因果机制：SIM(3) 等变编码器与自监督解耦预训练使模型从几何语义出发理解物体变化，而非单纯依赖数据统计，从而在数据稀缺场景下展现出显著优势。

### 尺寸泛化实验：OOD 场景下的鲁棒性

**Table 2** 报告了尺寸泛化实验的定量结果。GeoDexGrasp 在多种形状（立方体、圆柱体、球体、玩具马）和尺寸（含分布外 OOD 设置）上的成功率均超过所有对比方法。在 OOD 小立方体上，GeoDexGrasp 的成功率达到 **84.4%**，显著优于基线；在 OOD 大立方体上，成功率为 **68.8%**，同样保持领先。**Figure 5** 的定性结果展示了 GeoDexGrasp 在极端尺寸下的抓取姿态，进一步印证了尺寸泛化能力。

值得注意的是，玩具马（Toy Horse）对所有方法都极具挑战性，所有成功率均很低。这暴露了当前方法在复杂拓扑形状上的共同瓶颈：全局形状表示难以捕捉细粒度局部几何特征（如腿部、颈部等非凸区域），导致抓取策略失效。

### 消融实验：解耦策略与几何预训练的关键作用

**Table 3** 的消融研究系统剖析了各设计组件的贡献，揭示了以下因果链条：

1. **解耦策略的贡献**：对比联合生成（row a）与解耦生成（row c），解耦策略使物理合理性（穿透距离）和成功率均得到提升。这验证了在 SO(3) 流形与欧氏空间中分别建模根旋转和手指关节的必要性——两个空间的几何结构本质不同，联合建模会引入不合理的归纳偏置。

2. **几何解耦预训练的增益**：在解耦策略基础上加入自监督解耦预训练（row c vs. row e），物理合理性进一步提升。这说明通过对齐等变/不变特征与高层姿态/形状语义，模型获得了比普通等变特征更强的几何理解能力。

3. **各几何表示的作用**：形状-尺寸表示对降低穿透贡献最大，这与直觉一致——穿透本质上是对物体几何边界的违反，精确的形状与尺寸感知是避免穿透的前提。显式交互方向（PointSO）则稳定了旋转生成，为 SO(3) 上的条件建模提供了明确的参考锚点。

### 失败模式与局限性

尽管 GeoDexGrasp 在多数场景下表现优异，实验也揭示了若干失败模式：

- **复杂拓扑适应性不足**：在玩具马等具有复杂拓扑的物体上，所有方法（包括 GeoDexGrasp）的成功率均很低，模型难以处理多分支、细长结构的抓取规划。
- **解耦的潜在代价**：旋转与手指关节的独立生成虽提升了数据效率，但在某些情况下可能忽视两者之间的依赖关系，导致次优抓取姿态。
- **外部依赖的限制**：方法依赖 PointSO 提供交互方向，其性能上限受限于该基础模型；真实世界实验中使用的 SAM3D 点云重建质量也会影响最终效果。

### 补充图表

![[assets/figures/papers/paper_list_l2256_https_openaccess_thecvf_com_content_CVPR2026_html_Han_GeoDexGrasp_Geomet/figures/003_Table_1.jpg]]
*Table 1: Quantitative results. Our results are averaged over 10 runs, while the results of other methods are taken from published reports. Bold indicates the best performance, and underline indicates the second best. Our method achieves the highest performance in terms of physical plausibility, while attaining a comparable success rate to DexGraspAnything—with less than 1/5 of its parameters*

![[assets/figures/papers/paper_list_l2256_https_openaccess_thecvf_com_content_CVPR2026_html_Han_GeoDexGrasp_Geomet/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison. Our method results in less hand–object penetration and more physics-plausible contact*

![[assets/figures/papers/paper_list_l2256_https_openaccess_thecvf_com_content_CVPR2026_html_Han_GeoDexGrasp_Geomet/figures/006_Table_2.jpg]]
*Table 2: Quantitative results of the size generalization experiment. Gray cells indicate OOD settings*

![[assets/figures/papers/paper_list_l2256_https_openaccess_thecvf_com_content_CVPR2026_html_Han_GeoDexGrasp_Geomet/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative results of the size generalization experiment*

![[assets/figures/papers/paper_list_l2256_https_openaccess_thecvf_com_content_CVPR2026_html_Han_GeoDexGrasp_Geomet/figures/008_Table_3.jpg]]
*Table 3: Ablation study results. Dec.: decoupling strategy. Pre.: disentanglement pretraining. SR: Success Rate. PP: Physical Plausibility, measured by penetration distance*

![[assets/figures/papers/paper_list_l2256_https_openaccess_thecvf_com_content_CVPR2026_html_Han_GeoDexGrasp_Geomet/figures/009_Figure_6.jpg]]
*Figure 6: Real-world Validation*

## 方法谱系与知识库定位

### 1. 在灵巧抓取生成谱系中的位置

GeoDexGrasp 处于**数据驱动灵巧抓取生成**与**几何等变学习**的交叉点。与现有主流方法相比，其核心差异在于将对象内在几何先验显式地注入生成过程，而非依赖大规模数据统计拟合。

**前代数据驱动方法**普遍将抓取生成建模为从点云到完整手部姿态的端到端映射：

- **DexGraspNet**（Wang et al., arXiv 2022）和 **GenDexGrasp**（Li et al., arXiv 2022）采用合成数据训练，但缺乏对物理合理性（穿透、过抓取）的显式约束。
- **UniDexGrasp**（Xu et al., CVPR 2023）引入接触优化，但仍在欧氏空间直接联合生成旋转与手指关节。
- **DexGraspAnything**（Zhong et al., CVPR 2025）作为此前 SOTA，将根旋转固定为单位矩阵以简化问题，依赖约 150M 参数和海量数据覆盖姿态变化，本质上是用数据规模换取泛化能力。
- **UGG**（Lu et al., ECCV 2024）和 **D(R,O) Grasp**（Wei et al., arXiv 2024）分别从语言引导和关系建模角度改进，但同样未显式利用对象的几何等变结构。

GeoDexGrasp 的突破在于**将 SIM(3) 等变性引入灵巧抓取**（Section 3.2），使潜在表示在物体旋转、平移和缩放变换下保持一致的变换行为。这使得模型能够从几何语义出发理解物体变化，而非将每个姿态/尺寸变体视为全新样本。

### 2. 关键设计决策与因果机制

GeoDexGrasp 的性能优势源于三个相互耦合的架构选择：

**（1）解耦生成空间：SO(3) 流形与欧氏空间的分离**

完整抓取分布被分解为两个条件分布（Equation 4）：

$$p(g \mid X, \hat{\Theta}) = p(R \mid \xi) \cdot p(t, \theta \mid X, R, \zeta)$$

根旋转在 SO(3) 流形上通过 IPDF 独立建模（Section 3.3），而手指关节角与根平移在欧氏空间通过扩散模型生成（Section 3.4）。消融实验（Table 3, row a vs. row c）证实：解耦策略同时提升了物理合理性（穿透距离降低）和成功率，验证了在各自原生空间中学习的重要性。

**（2）几何解耦预训练：对齐低层特征与高层语义**

自监督预训练通过姿态回归和形状重建两个分支，最小化双向 Chamfer 距离（Equation 3），强制等变特征与姿态语义对齐、不变特征与形状语义对齐。消融实验（Table 3, row c vs. row e）表明：几何解耦预训练进一步提升了整体性能，尤其是物理合理性，说明对齐后的等变/不变特征优于普通等变特征。

**（3）显式交互方向引导**

引入 PointSO 基础模型根据语言提示推断物体交互方向（如“杯子把手”），为旋转生成提供明确的功能语义参考。消融分析（Section 4.4）显示：交互方向信息稳定了旋转生成过程。

### 3. 适用边界与局限

尽管 GeoDexGrasp 在数据效率、物理合理性和尺寸泛化上表现优异，其适用边界存在以下约束：

**（1）全局尺度因子的表达能力有限**

尺寸表示到灵巧手运动的映射高度非线性，显式提取全局尺度因子带来的改进有限。在极端缩放场景下，接触模式可能发生根本性重构，当前框架未能充分建模跨尺度的抓取策略迁移（Section 4.4 讨论）。

**（2）复杂拓扑形状的适应性不足**

在玩具马（Toy Horse）等复杂拓扑形状上，所有方法（包括 GeoDexGrasp）的成功率均很低（Table 2），表明模型对非标准几何结构的泛化仍存在瓶颈。

**（3）对外部模块的依赖**

方法依赖 PointSO 提供交互方向，其性能上限受限于该基础模型；真实世界实验使用 SAM3D 进行点云重建（Figure 6），系统整体效果受上游模块影响。

**（4）解耦可能忽视旋转-手指依赖**

解耦生成虽提升了数据效率，但可能导致根旋转与手指关节之间的条件依赖关系被忽视，在某些情况下产生次优抓取（Section 5 讨论）。

### 4. 开放问题

1. **细粒度几何特征融合**：如何将全局形状表示与局部几何特征（如点级曲率、边缘）融合，以更精确地建模手-物体接触，实现更细粒度的功能性抓取？

2. **跨尺度抓取策略迁移**：当物体发生大尺度缩放时，如何在几何等变框架下更平滑地建模接触模式的重构？

3. **物理仿真反馈闭环**：能否将显式的物理仿真反馈（如抓取稳定性指标）引入几何表示学习循环，同时提升物理合理性和任务成功率？

4. **少样本/零样本扩展**：在仅依赖少量标注数据时，如何进一步利用 VLM 或基础模型提供更丰富的几何先验以引导未见物体的抓取？

5. **多指操作泛化**：当前的解耦设计是否可扩展到其他灵巧手架构或更复杂的多指操作任务？

## 原文 PDF

![[paperPDFs/CVPR_2026/GeoDexGrasp_Geometry_aware_Generation_for_Data_efficient_and_Physics_plausible_Dexterous_Grasping.pdf]]
