---
title: "OrienPose: Orientation-Guided Novel View Synthesis for Single-Image Unseen Object Pose Estimation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/OrienPose_Orientation_Guided_Novel_View_Synthesis_for_Single_Image_Unseen_Object_Pose_Estimation.pdf
project_link: null
code_link: "https://github.com/pubyLu/OrienPose"
aliases:
- OrienPose
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过向新视角合成网络显式注入参考物体的方向先验（OAG），并在几何层面施加方向一致性约束（OCL），将病态变换转化为由起始方向和终止方向定义的明确变换，从而生成几何对齐的合成视图，提升姿态估计精度与鲁棒性。
primary_logic: 物体的内在方向作为一个对退化鲁棒的几何线索，可以定义视角变换过程的起点和终点，将原本病态的视角变换约束为有界问题；方向先验的注入与一致性监督形成闭环，使合成视图保留精确的几何结构与纹理。
claims:
- 在ShapeNet 10个未见类别上，OrienPose平均ACC30达59.6%，中值误差20.4°，相较于NOPE分别提升7.3%和降低7.3°。
- 在真实数据集NAVI上，OrienPose平均ACC30为50.9%，显著优于NOPE的36.8%。
- 消融实验表明，同时引入OAG和L_OC相比单独使用二者之一能带来持续的性能提升，验证了各模块的有效性与互补性。
- 在图像模糊和遮挡等退化条件下，OrienPose仍保持较高的精度，例如在bus类别40%模糊下ACC30达56.0%，显示出利用方向先验带来的鲁棒性。
---

# OrienPose: Orientation-Guided Novel View Synthesis for Single-Image Unseen Object Pose Estimation

> [!tip] 核心洞察
> 物体的内在方向作为一个对退化鲁棒的几何线索，可以定义视角变换过程的起点和终点，将原本病态的视角变换约束为有界问题；方向先验的注入与一致性监督形成闭环，使合成视图保留精确的几何结构与纹理。

| 字段 | 内容 |
|------|------|
| 中文题名 | OrienPose: 基于方向引导的新视角合成的单图像未见过物体姿态估计 |
| 英文题名 | OrienPose: Orientation-Guided Novel View Synthesis for Single-Image Unseen Object Pose Estimation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Liu_OrienPose_Orientation-Guided_Novel_View_Synthesis_for_Single-Image_Unseen_Object_Pose_CVPR_2026_paper.html) · [Code](https://github.com/pubyLu/OrienPose) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | OrienPose |
| Dataset | ShapeNet, NAVI |

> [!tip] 效果简介
> - ShapeNet (10 unseen categories) 上，ACC30 ↑ | Median error (°) ↓ 59.6 | 20.4 vs 52.3 | 27.7 (NOPE) (+7.3 | -7.3)。
> - NAVI (5 real-world instances) 上，ACC30 ↑ 50.9 vs 36.8 (NOPE) (+14.1)。

## 概要

从单张参考图像估计未见物体的三维姿态，是机器人抓取与场景理解中的核心挑战。现有方法多采用“生成-比较”范式：先通过新视角合成（NVS）从参考视图生成多个候选视角图像，再与查询图像进行模板匹配以确定姿态。然而，这一范式存在一个根本性的病态问题——参考图像的起始方向未被定义，导致 NVS 中的几何变换缺乏明确起点，仅靠像素级监督无法保证合成视图的几何正确性，常出现结构失真与纹理模糊，进而使模板匹配不可靠。

OrienPose 的核心洞察在于：**物体的内在方向是一个对退化鲁棒的几何线索，可以定义视角变换的起点与终点，将病态变换转化为有界问题**。基于此，方法通过两个关键设计实现几何对齐的新视角合成：

- **方向感知引导（OAG）**：显式地将参考物体的方向概率分布注入参考视图的潜在特征，为 NVS 提供明确的起始方向先验。
- **方向一致性损失（L_OC）**：在几何层面以 KL 散度监督合成视图与目标视图的方向分布一致性，形成“注入-监督”的闭环约束。

在 ShapeNet 的 10 个未见类别上，OrienPose 平均 ACC30 达 **59.6%**，中值误差 **20.4°**，相较基线 NOPE（Nguyen et al., CVPR 2024）分别提升 7.3% 和降低 7.3°。在真实数据集 NAVI 上，平均 ACC30 为 **50.9%**，显著优于 NOPE 的 36.8%。消融实验证实，OAG 与 L_OC 缺一不可且互补，同时引入两者才能获得最优性能。此外，在图像模糊和遮挡等退化条件下，方向先验的注入使模型仍能保持较高的姿态估计精度，展现出对退化场景的鲁棒性。

在方法谱系上，OrienPose 属于“生成-比较”类单图像姿态估计方法，与直接回归相对姿态的 PIZZA（Du et al., 3DV 2022）、基于关键点匹配的 MicKey（Barroso-Laguna et al., CVPR 2024）以及概率姿态估计的 RelPose（Zhang et al., ECCV 2022）和 RelPose++（Lin et al., 3DV 2024）等形成对比。其核心差异在于首次将物体方向作为显式几何先验引入 NVS 流程，从源头上解决了视角变换的病态性问题，而非仅改进匹配或回归策略。



单图像未见过物体的三维姿态估计是机器人抓取与增强现实中的核心挑战。给定一张参考图像和一张查询图像，系统需要在不依赖物体CAD模型的前提下，估计两帧之间物体的相对三维旋转。近年来，基于生成-比较范式的方法——即先通过新视角合成（Novel View Synthesis, NVS）从参考视图生成一组候选模板，再与查询图像进行匹配——展现出较强的零样本泛化潜力，代表性工作如 **NOPE**（Nguyen et al., CVPR 2024）。

然而，这类方法存在一个根本性的瓶颈：**参考图像的起始方向未被定义**。新视角合成网络仅接收相对相机姿态变化 $\Delta R$ 作为条件信号，却无从知晓参考视图中物体原本朝向何处。这使得从参考视图到目标视图的几何变换本质上是一个病态问题——像素级 $L_2$ 监督只能约束生成图像的表观相似性，无法保证底层三维几何变换的正确性。其直接后果是合成视图出现结构失真与纹理模糊，进而导致下游的模板匹配不可靠，严重限制了姿态估计精度。

本文的核心洞察在于：**物体的内在方向作为一个对退化鲁棒的几何线索，可以定义视角变换过程的起点和终点**。若能显式获取参考视图中物体的方向先验，并以之锚定变换的起始状态，则原本病态的视角变换将被约束为一个由起始方向 $O_{ref}$ 和终止方向 $O_{syn}$ 共同定义的明确变换 $O_{ref} + \Delta R = O_{syn}$。这一从“猜测”到“定义”的范式转换，构成了本文方法设计的根本动机。



## 核心方法与创新机理

OrienPose 的核心创新在于将单图像未见过物体姿态估计中“视角变换”这一环节，从一个**病态的猜测问题**重新定义为一个**由方向先验显式约束的几何变换问题**。现有方法（如 **NOPE**，Nguyen et al., CVPR 2024）仅依赖像素级监督和相机姿态条件 $\Delta R$ 来驱动新视角合成，但由于参考图像的起始方向未被定义，网络只能“猜测”从参考视图到目标视图的几何变换，导致合成视图出现结构失真和纹理模糊。OrienPose 通过两个相互配合的机制——**方向感知引导（OAG）** 和 **方向一致性损失（$L_{OC}$）**——将这一病态变换转化为由起始方向 $O_{ref}$ 和终止方向 $O_{syn}$ 共同定义的明确变换，形成 $O_{ref} + \Delta R = O_{syn}$ 的几何一致性闭环。

具体而言，OrienPose 在以下三个关键环节引入了方向先验：

**1. 视角变换引导（从隐式相机条件到显式方向注入）**

基线方法 NOPE 仅通过相机姿态 $\Delta R$ 条件控制生成过程，网络缺乏关于参考物体自身朝向的信息。OrienPose 通过 **OAG 模块**将参考图像中物体的方向概率分布 $E_{orient}$ 显式注入参考视图的潜在特征 $E_{ref}$。该模块首先利用预训练的方向估计器（Orient-Anything）提取参考图像中物体的方位角 $\alpha$、平面内旋转 $\theta$ 和仰角 $\omega$ 的概率分布，经 MLP 嵌入后通过交叉注意力机制注入编码器提取的图像特征中，产生方向感知的潜在表示 $E_{ref}'$。这一设计使得视角变换的起点被明确定义，网络不再需要从像素中隐式推断物体朝向。

**2. 几何监督损失（从纯像素级约束到方向一致性约束）**

基线方法仅使用 $L_2$ 像素级损失监督合成视图，缺乏对几何变换正确性的显式约束。OrienPose 引入**方向一致性损失** $L_{OC}$，基于 KL 散度分别计算合成视图与目标视图在三个角度上的方向分布差异：

$$L_{\mathrm{OC}} = \mu_1 D_{KL}(P_{gt}^{\alpha}, P_{ref}^{\alpha}) + \mu_2 D_{KL}(P^{\theta}_{gt}, P^{\theta}_{ref}) + \mu_3 D_{KL}(P^{\omega}_{gt}, P^{\omega}_{ref})$$

总损失为 $\mathcal{L} = \lambda_1 L_2 + \lambda_2 L_{OC}$。这一设计在几何层面监督变换过程，确保合成视图不仅在像素上相似，更在物体朝向层面与目标一致，从而强制生成几何对齐的合成视图。

**3. 模板匹配相似度（从单一外观匹配到外观-方向联合匹配）**

基线方法仅使用潜在特征的 $L_2$ 距离衡量模板与查询图像的相似度。OrienPose 提出**方向感知相似度** $S_{OA}^k$，融合外观一致性与方向一致性：

$$S_{OA}^{k} = -\| E_{tmp}^{k} - E_{qry} \|_{2}^{2} - D_{KL}( O_{qry} \| O_{tmp}^{k} )$$

该度量同时考虑合成模板与查询图像在潜在空间中的特征距离和方向分布差异，使得模板匹配过程对几何畸变更加敏感，从而提升姿态检索的准确性。

**模块间的协同效应**

消融实验证实，同时引入 OAG 和 $L_{OC}$ 相比单独使用二者之一能带来持续的性能提升，验证了方向先验的注入与一致性监督之间存在互补关系：OAG 提供变换的起点约束，$L_{OC}$ 提供变换的终点监督，二者共同将病态问题转化为有界问题。这种闭环设计是 OrienPose 相较于 NOPE 在 ShapeNet 未见类别上 ACC30 提升 7.3%（59.6% vs. 52.3%）、中值误差降低 7.3°（20.4° vs. 27.7°）的核心驱动力。



OrienPose 的整体框架围绕一个核心洞察构建：**将物体的内在方向作为几何先验，把新视角合成中原本病态的变换过程转化为由明确起点和终点定义的闭环**。如图 2 所示，系统由四个关键模块串联而成：方向估计器（OEM）、方向感知引导（OAG）、新视角合成网络（NVS）以及方向感知模板匹配。

### 输入输出流

给定一张参考图像 $I_{ref}$ 和一组预定义的候选视角变换 $\{\Delta R_k\}_{k=1}^N$，系统首先通过编码器提取参考图像的潜在特征 $E_{ref}$。与此同时，方向估计器从 $I_{ref}$ 中估计物体的方向概率分布（方位角 $\alpha$、平面内旋转 $\theta$、仰角 $\omega$），经 MLP 嵌入后得到方向嵌入 $E_{orient}$。OAG 模块通过交叉注意力机制将 $E_{orient}$ 注入 $E_{ref}$，输出方向感知的参考嵌入 $E'_{ref}$。NVS 网络以 $E'_{ref}$ 和目标视角嵌入 $E_{pose}$ 为条件，生成目标视角的潜在表示 $E'_{tgt}$。在姿态估计阶段，系统为每个候选视角生成模板的潜在特征 $E_{tmp}^k$，并与查询图像的嵌入 $E_{qry}$ 进行方向感知相似度匹配，得分最高的模板对应的视角即为最终估计的姿态。

### 模块协作关系

四个模块形成一条从“方向感知”到“几何对齐”再到“鲁棒匹配”的因果链：

- **OEM** 提供原始的方向先验，是整个框架的感知入口。论文采用 Orient-Anything 模型作为方向估计器，输出三个角度的离散概率分布。
- **OAG** 将方向先验显式编码进参考视图的潜在空间，使 NVS 网络在生成时拥有明确的变换起点。这是解决“起始方向未定义”这一瓶颈的关键设计。
- **NVS** 在方向感知嵌入和视角条件 $\Delta R_k$ 的共同驱动下生成目标视图。其训练不仅依赖像素级 $L_2$ 损失，还引入了**方向一致性损失** $L_{OC}$——通过 KL 散度约束合成视图与真值视图在三个方向角上的分布一致性，从而在几何层面施加闭环监督。
- **模板匹配** 采用融合外观与方向的双重相似度度量 $S_{OA}^k = -\|E_{tmp}^k - E_{qry}\|_2^2 - D_{KL}(O_{qry} \| O_{tmp}^k)$，相比仅依赖潜在特征 $L_2$ 距离的匹配方式，对几何畸变具有更强的判别力。

### 与基线方法的本质差异

以 **NOPE**（Nguyen et al., CVPR 2024）为代表的现有生成-比较方法，其 NVS 过程仅通过相机姿态条件 $\Delta R$ 控制生成，缺乏对参考物体自身方向的感知。这导致视角变换的起点是未定义的，网络只能在像素级监督下“猜测”几何变换，合成视图容易出现结构失真和纹理模糊。OrienPose 的改进在于：将原本缺失的“方向”信息作为显式条件注入生成过程，并通过方向一致性损失在几何层面闭合监督回路，从而将病态变换转化为有界问题。消融实验证实，同时引入 OAG 和 $L_{OC}$ 相比单独使用其一能带来持续的性能提升，验证了两者在“注入先验”与“几何监督”上的互补性。

### 补充图表

![[assets/figures/papers/paper_list_l2557_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_OrienPose_Orientat/figures/002_Figure_2.jpg]]
*Figure 2: Overview. (a) The orientation-guided NVS framework takes a reference image*

![[assets/figures/papers/paper_list_l2557_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_OrienPose_Orientat/figures/001_Figure_1.jpg]]
*Figure 1: Our goal is to predict the 3D pose of objects via Novel View Synthesis (NVS) from a reference view. Top: Existing NVS methods can only guess the geometric transformation from reference to synthesized view under pixel-level supervision due to undefined starting orientation, causing geometry-distorted synthesis. In contrast, our framework explicitly defines this transformation by actively introducing orientation priors, achieving geometry-aligned synthesis and more accurate pose estimation. Bottom: We show the nature of problems by visualizing the latent space representation (green background) and the final predicted pose through rendering with the help of a 3D model (blue background)*



### 核心瓶颈与设计动机

单图像新视角合成（NVS）用于未见过物体姿态估计时面临一个根本性的病态问题：参考图像的起始方向未被定义，导致几何变换“起始方向 + 相对旋转 = ?”成为无解方程。现有方法（如 **NOPE**, Nguyen et al., CVPR 2024）仅依赖像素级 L₂ 损失进行监督，网络只能“猜测”视角变换，合成视图常出现结构失真和纹理模糊，进而使模板匹配不可靠。

OrienPose 的核心洞察在于：**物体的内在方向是一个对退化鲁棒的几何线索**，可以显式定义视角变换的起点和终点，将病态问题转化为有界问题。具体而言，通过向 NVS 网络注入参考物体的方向先验（起点），并在几何层面施加方向一致性约束（终点），形成闭环监督，使合成视图保留精确的几何结构与纹理。

### 方向概率分布建模

物体方向由三个角度定义：方位角 $\alpha$、平面内旋转 $\theta$ 和仰角 $\omega$。每个角度被建模为离散的一维概率分布：

$$
\left\{ \begin{array} { l l } { P _ { r e f } ^ { \alpha } ( x | \alpha , \sigma _ { \alpha } ) = \frac { 1 } { 2 \pi B _ { 0 } ( 1 / \sigma _ { \alpha } ^ { 2 } ) } e ^ { \frac { c o s ( x - \alpha ) } { \sigma _ { \alpha } ^ { 2 } } } } \\ { P _ { r e f } ^ { \theta } ( y | \theta , \sigma _ { \theta } ) = \frac { 1 } { 2 \pi B _ { 0 } ( 1 / \sigma _ { \theta } ^ { 2 } ) } e ^ { \frac { c o s ( y - \theta ) } { \sigma _ { \theta } ^ { 2 } } } } \\ { P _ { r e f } ^ { \omega } ( z | \omega , \sigma _ { \omega } ) = \frac { 1 } { \sum _ { n = 1 } ^ { 1 8 0 } e ^ { - \frac { ( n - \omega ) ^ { 2 } } { 2 \sigma _ { \omega } ^ { 2 } } } } e ^ { - \frac { ( z - \omega ) ^ { 2 } } { 2 \sigma _ { \omega } ^ { 2 } } } } \end{array} \right.
$$

其中，$\alpha$ 和 $\theta$ 采用 Von Mises 分布（圆周上的高斯分布），$B_0(\cdot)$ 为零阶修正贝塞尔函数；$\omega$ 采用截断高斯分布，范围 $[1°, 180°]$。$\sigma$ 参数控制分布的集中程度，反映方向估计的不确定性。

### 方向感知引导（OAG）

OAG 模块将物体方向先验显式注入参考图像的潜在表示中，其流程如下：

1. **方向估计**：使用预训练的 Orient-Anything 模型作为方向估计器（OEM），从参考图像 $I_{ref}$ 中提取方向概率分布 $P_{ref}^{\alpha}, P_{ref}^{\theta}, P_{ref}^{\omega}$。
2. **方向嵌入**：通过 MLP 将方向分布编码为方向嵌入 $E_{orient}$。
3. **交叉注意力注入**：$E_{orient}$ 通过交叉注意力机制注入参考图像的潜在特征 $E_{ref}$，输出方向感知的嵌入 $E_{ref}'$。

数学上，这一过程可表示为：

$$E_{ref}' = \text{CrossAttn}(E_{ref}, E_{orient})$$

该嵌入随后与目标视点的相对旋转 $\Delta R_k$ 的嵌入 $E_{pose}$ 一起输入 NVS 网络，生成目标视角的潜在表示 $E_{tgt}'$。

### 方向一致性损失（$L_{OC}$）

为在几何层面强化监督，OrienPose 在标准 L₂ 损失之外引入方向一致性损失。总损失函数为：

$$\mathcal{L} = \lambda_1 L_2 + \lambda_2 L_{OC}$$

其中 $L_{OC}$ 基于 KL 散度，分别计算合成视图与真值视图在三个角度上的分布差异：

$$L_{\mathrm{OC}} = \mu_1 D_{KL}(P_{gt}^{\alpha}, P_{ref}^{\alpha}) + \mu_2 D_{KL}(P_{gt}^{\theta}, P_{ref}^{\theta}) + \mu_3 D_{KL}(P_{gt}^{\omega}, P_{ref}^{\omega})$$

- $D_{KL}(\cdot\|\cdot)$ 为 KL 散度，度量两个概率分布之间的距离。
- $\mu_1, \mu_2, \mu_3$ 为各角度损失分量的权重。
- 该损失强制合成视图的物体方向与目标真值一致，形成“注入-监督”闭环。

### 方向感知相似度度量

在模板匹配阶段，OrienPose 提出融合外观与方向一致性的相似度分数：

$$S_{OA}^{k} = -\| E_{tmp}^{k} - E_{qry} \|_{2}^{2} - D_{KL}( O_{qry} \| O_{tmp}^{k} )$$

- 第一项为潜在特征的负 L₂ 距离，衡量外观相似度。
- 第二项为方向的负 KL 散度，衡量几何一致性。
- $E_{tmp}^{k}$ 和 $O_{tmp}^{k}$ 分别为第 $k$ 个模板的潜在特征和方向分布；$E_{qry}$ 和 $O_{qry}$ 为查询图像的对应量。

匹配时选择 $S_{OA}^{k}$ 最大的模板，其对应的姿态即为最终估计结果。相比仅使用 L₂ 距离的基线，该度量在退化条件下（模糊、遮挡）具有更强的判别力。

### 补充图表

![[assets/figures/papers/paper_list_l2557_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_OrienPose_Orientat/figures/003_Figure_3.jpg]]
*Figure 3: Pose estimation pipeline. Given N viewpoints*



## 实验与关键发现

### 实验设置简述

OrienPose 在两个基准上进行了评估：**ShapeNet** 的 10 个未见过类别（合成数据）和 **NAVI** 真实世界数据集（5 个实例）。所有测试类别和实例在训练期间完全未见过，确保对未见物体的零样本泛化评估是公平的。评价指标采用 **ACC30**（角度误差 ≤30° 的比例，↑）和 **中值角度误差**（Median error，°, ↓）。基线方法包括生成-比较范式的 **NOPE**（Nguyen et al., CVPR 2024）、直接回归方法的 **PIZZA**（Du et al., 3DV 2022）、关键点匹配的 **MicKey**（Barroso-Laguna et al., CVPR 2024）、概率姿态估计的 **RelPose**（Zhang et al., ECCV 2022）与 **RelPose++**（Lin et al., 3DV 2024），以及基于扩散模型的新视角合成强基线 **Free3D**（Zheng and Vedaldi, CVPR 2024）。需注意，**GigaPose** 因需要已知 CAD 模型作为输入，其结果在性能排名中不予考虑，仅作参考。

### 主实验结果

#### ShapeNet 未见过类别

在 ShapeNet 的 10 个未见过类别上，OrienPose 取得了显著优势。如 Table 1 所示，OrienPose 的平均 ACC30 达到 **59.6%**，中值误差降至 **20.4°**，相较于 NOPE（52.3% / 27.7°）分别提升 **+7.3%** 和降低 **-7.3°**。这一结果表明，方向感知的引导与监督有效解决了 NOPE 中因起始方向未定义而导致的几何变换病态问题，使合成视图保留了更精确的几何结构。

![[assets/figures/papers/paper_list_l2557_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_OrienPose_Orientat/figures/004_Table_1.jpg]]
*Table 1: Quantitative results on the ShapeNet, where bold and underlined indicate the best and second-best performances, respectively. Note that since only GigaPose requires a CAD model input, its results are not included during performance ranking*

在具体类别上，OrienPose 在大多数类别上均优于 NOPE 和其他基线。Figure 4 的可视化进一步印证了这一结论：OrienPose 估计的姿态分布（红色）更紧密地聚集在真值（绿色）周围，而 NOPE（蓝色）的分布则较为分散；渲染结果也显示 OrienPose 的合成视图与真值视图的几何一致性更高。

![[assets/figures/papers/paper_list_l2557_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_OrienPose_Orientat/figures/005_Figure_4.jpg]]
*Figure 4: Visualization results of the best and second best performers for the ShapeNet test set. The arrow (last columns for each object) indicates the estimated pose distribution on a unit sphere, where green, red, and blue represent the ground-truth, ours, and NOPE, respectively, best viewed in zoomed-in. The predicted poses (3rd and 4th columns for each object) of NOPE and Ours are visualized by rendering the object from these poses. The 3D model is only used for visualization, not as input to the methods*

#### NAVI 真实世界数据集

在更具挑战性的真实世界场景 NAVI 数据集上，OrienPose 的优势更加突出。如 Table 2 所示，OrienPose 的平均 ACC30 达到 **50.9%**，显著优于 NOPE 的 **36.8%**（提升 **+14.1%**）。这表明方向先验的引入不仅在合成数据上有效，在真实世界的纹理、光照变化下同样具有强泛化能力，因为物体的内在方向作为一种对退化鲁棒的几何线索，能够稳定地约束视角变换过程。

![[assets/figures/papers/paper_list_l2557_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_OrienPose_Orientat/figures/006_Table_2.jpg]]
*Table 2: Results on NAVI, where bold and underlined indicate the best and second-best performances, respectively. Similarly, the results of GigaPose are excluded during ranking*

### 消融实验

为验证各模块的贡献，论文在 ShapeNet 的 `bus` 类别上进行了消融研究（Figure 6）。

![[assets/figures/papers/paper_list_l2557_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_OrienPose_Orientat/figures/010_Figure_6.jpg]]
*Figure 6: Ablation studies on OAG and*

**OAG 与 L_OC 的互补性**：单独引入 Orientation-Aware Guidance（OAG）或方向一致性损失（L_OC）均能带来性能提升，但同时使用两者时性能增益持续增加，且提升幅度大于单独使用任一模块。这验证了方向先验的注入（OAG）与几何层面的方向一致性监督（L_OC）形成闭环——OAG 将病态变换转化为由起始方向和终止方向定义的明确变换，L_OC 则确保合成结果在几何层面与目标方向对齐，两者缺一不可且互补。

**方向感知相似度**：将模板匹配的相似度从纯潜在特征 L₂ 距离替换为方向感知相似度 S_OA（融合外观距离与方向 KL 散度），进一步提升了匹配精度，验证了在检索阶段同时考虑外观一致性和方向一致性对姿态估计的重要性。

### 鲁棒性分析

为评估方法在退化条件下的表现，论文在 `bus` 类别上进行了模糊和遮挡实验（Table 3, Figure 5）。

![[assets/figures/papers/paper_list_l2557_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_OrienPose_Orientat/figures/007_Table_3.jpg]]
*Table 3: Quantitative result of robustness on bus*

![[assets/figures/papers/paper_list_l2557_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_OrienPose_Orientat/figures/009_Figure_5.jpg]]
*Figure 5: Results under blur (top) and occlusion (bottom). The rendered images of predicted pose are combined with their difference maps with GT, where darker colors indicate smaller differences*

**模糊条件下**：在 40% 模糊程度下，OrienPose 仍保持 **56.0%** 的 ACC30 和 **24.9°** 的中值误差，而 NOPE 在相同条件下性能下降更为显著。OrienPose 通过将模糊图像投影到方向感知的潜在空间，仍能学习到足够的方向先验来约束视角变换。

**遮挡条件下**：类似地，在遮挡场景中，OrienPose 凭借方向先验的鲁棒性，估计误差显著低于 NOPE。Figure 5 的差异图可视化显示，OrienPose 的渲染结果与真值的差异（更深的颜色表示更小的差异）明显小于 NOPE。

这些结果表明，物体的内在方向作为一种对图像退化不敏感的几何线索，能够在模糊和遮挡等不利条件下为姿态估计提供稳定的约束。

### 大视角变化下的表现

Figure 7 展示了大视角变化（方位角差 > 90°）下的定性结果。尽管 OrienPose 在此类极端条件下仍能保持优于 NOPE 的合成质量，但论文明确指出，当参考视图与查询视图之间的视角变化过大时，合成质量会下降，导致姿态估计精度明显降低。这是 OrienPose 的一个已知局限——方向先验虽能约束变换的有界性，但在极端视角差异下，单视图信息的内在不足仍难以完全弥补。

![[assets/figures/papers/paper_list_l2557_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_OrienPose_Orientat/figures/008_Figure_7.jpg]]
*Figure 7: Results for large viewpoint changes*

### 失败模式与局限

综合实验与分析，OrienPose 的主要失败模式包括：

1. **极端视角变化**：当方位角差超过约 90° 时，新视角合成网络难以生成高质量的合成视图，导致模板匹配不可靠，姿态估计误差增大。这是单图像新视角合成范式的固有限制。
2. **严重遮挡与极度模糊**：尽管方向先验带来了显著的鲁棒性提升，但在严重遮挡或极度模糊情况下，估计误差仍高于普通场景，表明方向估计器本身在这些条件下也可能产生不准确的先验。
3. **坐标框架不统一**：方向估计器（Orient-Anything）的坐标框架与物体的规范坐标框架之间缺乏显式对齐，这使得方向先验目前仅用于相对变换的约束，而无法直接用于绝对位姿恢复。



## 定位与知识库关联

### 任务定位与问题边界

OrienPose 解决的是**单图像未见过物体的3D姿态估计**问题，属于零样本物体姿态估计（zero-shot object pose estimation）的子领域。其核心设定是：给定一张参考图像和一张查询图像，估计查询图像中物体相对于参考图像的3D旋转，且测试物体在训练期间完全不可见。该任务的关键难点在于，仅凭单张2D图像恢复3D姿态本身是一个病态问题，而未见过的物体类别进一步加剧了外观与几何的泛化难度。

OrienPose 的方法边界明确：它依赖一个预训练的**方向估计器**（Orient-Anything）来提取物体方向先验，依赖一个预训练的**图像编码器**来提取潜在特征，并需要预定义的**离散视角集合**来生成模板。该方法不要求已知物体的CAD模型（与 GigaPose 形成对比），不依赖3D标注的训练数据，也不假设物体类别已知。其适用场景受限于：参考视图与查询视图之间的视角变化不宜过大（方位角差超过90°时精度显著下降），且严重遮挡或极度模糊条件下误差仍高于正常情况。

### 与生成-比较范式的继承与革新

OrienPose 直接继承自**生成-比较（generation-and-comparison）范式**，其最直接的基线是 **NOPE**（Nguyen et al., CVPR 2024）。NOPE 的核心思路是：给定参考图像和目标相机姿态变化 ΔR，通过新视角合成网络（NVS）生成目标视角的潜在表示，再通过模板匹配找到与查询图像最相似的合成视图，输出对应姿态。这一范式将姿态估计转化为“生成-匹配”问题，避免了对物体类别先验的依赖，天然适合零样本泛化。

然而，NOPE 存在一个根本性的瓶颈：**参考图像的起始方向未被定义**。在 NVS 训练中，网络仅通过像素级 L₂ 损失来学习视角变换，但“从哪个方向开始变换”这一关键信息缺失，导致视角变换成为病态问题——网络只能“猜测”变换的起点，合成视图容易出现结构失真和纹理模糊。这正是 OrienPose 的核心突破点。

OrienPose 的革新体现在两个层面：

1. **方向感知引导（OAG）**：通过向 NVS 网络显式注入参考物体的方向概率分布（由 OEM 估计的方位角 α、平面内旋转 θ、仰角 ω 的 von Mises/离散分布），将原本病态的变换转化为由“起始方向 + ΔR = 目标方向”定义的明确几何变换。这一设计将方向先验作为视角变换的锚点，使网络不再需要从像素中隐式推断起始方向。

2. **方向一致性损失（L_OC）**：在几何层面施加监督，通过 KL 散度约束合成视图的方向分布与真值方向分布一致。这形成了“方向注入—方向监督”的闭环，确保合成视图不仅外观逼真，而且几何结构对齐正确。

从方法谱系来看，OrienPose 在 NOPE 的框架上进行了两个关键槽位的替换：将“无方向引导的潜在特征”替换为“方向感知的潜在特征”（OAG），将“纯像素级监督”替换为“像素级+几何级联合监督”（L₂ + L_OC）。这种改造保持了生成-比较范式的零样本泛化优势，同时从根本上解决了视角变换的病态性问题。

### 与其他技术路线的对比

除生成-比较范式外，单图像物体姿态估计还存在其他技术路线，OrienPose 与它们的关系如下：

- **直接回归方法**：如 **PIZZA**（Du et al., 3DV 2022），直接从图像对回归相对姿态。这类方法通常需要类别级训练数据，泛化到未见过的物体类别时性能下降明显。OrienPose 通过生成-匹配的间接策略绕过了对类别先验的依赖。

- **关键点匹配方法**：如 **MicKey**（Barroso-Laguna et al., CVPR 2024），通过检测和匹配2D关键点来恢复相对姿态。这类方法在纹理丰富物体上表现良好，但对无纹理或弱纹理物体（ShapeNet 中的许多合成物体）鲁棒性不足。OrienPose 的潜在特征匹配不依赖显式关键点，对纹理变化更为鲁棒。

- **概率姿态估计方法**：如 **RelPose**（Zhang et al., ECCV 2022）和 **RelPose++**（Lin et al., 3DV 2024），通过建模姿态的概率分布来处理不确定性。OrienPose 同样使用了概率分布（方向分布），但其创新在于将方向分布作为 NVS 的条件输入和几何监督信号，而非直接用于姿态回归。

- **扩散模型新视角合成**：如 **Free3D**（Zheng and Vedaldi, CVPR 2024），使用扩散模型进行新视角合成。OrienPose 在实验中以 Free3D 作为 NVS 骨干网络的强基线，验证了方向引导策略可以提升不同 NVS 架构的性能。这表明 OAG 和 L_OC 的设计具有一定的架构无关性。

### 关键设计的互补性与消融证据

消融实验揭示了 OAG 和 L_OC 的互补关系：单独添加 OAG 或单独添加 L_OC 均能带来性能提升，但同时引入两者时提升幅度持续增大。这表明：

- **OAG 提供前向引导**：在 NVS 的输入端注入方向先验，约束变换的起点。
- **L_OC 提供反向监督**：在 NVS 的输出端施加几何一致性约束，确保变换的终点正确。

两者形成闭环，缺一不可。此外，方向感知相似度度量 $S_{OA}^{k} = -\| E_{tmp}^{k} - E_{qry} \|_{2}^{2} - D_{KL}( O_{qry} \| O_{tmp}^{k} )$ 将外观匹配与方向一致性统一在同一个分数中，进一步强化了方向先验在推理阶段的作用。

### 鲁棒性边界与退化条件

OrienPose 在模糊和遮挡条件下展现出优于 NOPE 的鲁棒性。例如，在 bus 类别上施加40%模糊时，OrienPose 仍能达到56.0%的 ACC30（中值误差24.9°），而 NOPE 的性能下降更为剧烈。论文将此归因于方向感知潜在空间的学习：即使图像质量退化，方向先验仍能为 NVS 提供足够的几何约束。

然而，两个退化条件构成了该方法的**适用边界**：

1. **大视角变化**（方位角差 > 90°）：合成质量下降导致姿态估计精度明显降低。这是因为大视角变化意味着需要生成大量不可见内容，NVS 的生成能力成为瓶颈。
2. **严重遮挡与极度模糊**：尽管方向先验带来鲁棒性提升，但估计误差仍高于正常情况，表明方向估计器本身的精度在极端条件下也会受到影响。

### 开放问题与未来方向

从方法谱系的角度，OrienPose 留下了若干值得探索的方向：

1. **多视图先验的引入**：当前方法仅使用单张参考图像，在大视角变化下合成质量受限。引入多视图先验或底层3D几何信息（如隐式神经表示）可能进一步增强大视角变换的控制能力。

2. **坐标框架的统一**：OrienPose 使用方向估计器（Orient-Anything）提取物体方向，但该方向定义在估计器自身的坐标框架中，与物体的规范坐标框架未必一致。统一这两个坐标框架可能使方向先验直接用于绝对位姿恢复，而非仅用于相对变换约束。

3. **方向估计器的联合优化**：当前 OEM 是冻结的预训练模型，未与 NVS 网络联合优化。端到端的联合训练可能进一步提升方向先验与视角合成的一致性。

4. **向类别级方法的迁移**：OAG 和 L_OC 的设计思想——显式注入几何先验并施加几何一致性监督——可能对类别级姿态估计方法也有借鉴价值，尤其是在处理类内几何变异时。



## 原文 PDF

![[paperPDFs/CVPR_2026/OrienPose_Orientation_Guided_Novel_View_Synthesis_for_Single_Image_Unseen_Object_Pose_Estimation.pdf]]
