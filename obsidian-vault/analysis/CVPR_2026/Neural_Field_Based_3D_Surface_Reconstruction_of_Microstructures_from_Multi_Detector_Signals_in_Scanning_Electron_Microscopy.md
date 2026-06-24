---
title: Neural Field-Based 3D Surface Reconstruction of Microstructures from Multi-Detector Signals in Scanning Electron Microscopy
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Neural_Field_Based_3D_Surface_Reconstruction_of_Microstructures_from_Multi_Detector_Signals_in_Scanning_Electron_Microscopy.pdf
project_link: null
code_link: "https://github.com/zju3dv/NFH-SEM"
aliases:
- Neural_Field-Bas
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 将可学习的BSE前向模型嵌入神经场联合优化，以自校准方式提取几何信息并迭代分离阴影，从而突破传统限制。
primary_logic: 通过引入可学习的BSE前向模型取代固定经验公式，并与SDF神经场协同优化，NFH-SEM实现了无需参考样品的参数自校准、自动阴影分离和高保真微观表面重建。
claims:
- NFH-SEM在真实样品上一致优于传统多视图与单视图方法，精确恢复478 nm打印层和微米级断裂台阶等细节。
- 在模拟数据集上，NFH-SEM的平均Chamfer距离为17.48 nm、法向角度误差为3.70°，远超单视图光度立体（512.22 nm, 12.99°）和粗初始化（25.11 nm, 7.85°）。
- 阴影分离模块实现平均阴影检测准确率81.7%，自动排除遮挡区域，提升重建精度。
- 与NeuS、2DGS等学习型重建方法相比，NFH-SEM因嵌入SEM物理模型而显著减少表面畸变和缺失几何。
---

# Neural Field-Based 3D Surface Reconstruction of Microstructures from Multi-Detector Signals in Scanning Electron Microscopy

> [!tip] 核心洞察
> 通过引入可学习的BSE前向模型取代固定经验公式，并与SDF神经场协同优化，NFH-SEM实现了无需参考样品的参数自校准、自动阴影分离和高保真微观表面重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于神经场的扫描电镜多探测器信号三维微结构表面重建 |
| 英文题名 | Neural Field-Based 3D Surface Reconstruction of Microstructures from Multi-Detector Signals in Scanning Electron Microscopy |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2508.04728) · [Code](https://github.com/zju3dv/NFH-SEM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | NFH-SEM |
| Dataset | Simulated TPL dataset, Real-world NFH-SEM dataset |

> [!tip] 效果简介
> - Simulated TPL dataset (Wukong, Lucy, Lion) 上，Chamfer distance (nm)↓ 17.48 (avg.) vs 25.11 (Input coarse) / 512.22 (Single-view PS) (-7.63 nm / -494.74 nm)。
> - Real-world NFH-SEM dataset (TPL, pollen, SiC) 上，Qualitative accuracy (local details, overall shape) 高保真，恢复478 nm层、782 nm纹理、1.559 μm台阶 vs 多视图过平滑/缺失细节，单视图全局畸变 (显著改善)。
> - Real-world NFH-SEM dataset (learning-based comparison) 上，Reconstruction completeness and surface distortion 完整且准确的表面 vs NeuS/2DGS/PGSR等产生严重畸变和不完整几何 (定性大幅领先)。

## 概述

扫描电子显微镜（SEM）是材料科学、生物学和微纳制造领域不可或缺的成像工具，但传统SEM三维重建方法长期受制于**无纹理区域匹配困难、阴影伪影干扰、探测器校准依赖参考样品**三大瓶颈。多视图立体方法在平滑表面区域缺乏可匹配特征，单视图光度立体方法则因依赖固定经验公式而易产生全局畸变，而新兴的学习型重建方法因缺乏SEM物理先验与领域数据而无法泛化至微观尺度。

**NFH-SEM** 针对上述问题提出了一条根本性解决路径：将可学习的背散射电子（BSE）前向模型嵌入SDF神经场联合优化框架，以**自校准**方式从四象限BSE信号中提取几何信息，并**迭代分离阴影**区域。其核心洞察在于——用数据驱动的四阶多项式发射项替代传统固定解析模型，使探测器参数与表面几何在统一优化中协同收敛，从而在无需参考样品、无需手动阴影剔除的条件下实现高保真微观表面重建。

在方法谱系上，NFH-SEM位于**物理驱动神经场重建**与**多探测器信号融合**的交叉点。相较于 **Agisoft Metashape** 等传统多视图管线，它利用BSE信号补偿纹理缺失区域的几何细节；相较于经典单视图光度立体方法（4Q-BSE梯度积分），它通过可微前向模型避免了梯度估计的误差累积；相较于 **NeuS**、**2DGS** 等通用学习型重建方法，它嵌入的SEM成像物理使其在领域迁移时保持几何完整性，显著减少表面畸变。

实验验证覆盖模拟与真实两类数据。在模拟数据集上，NFH-SEM的平均Chamfer距离为**17.48 nm**、法向角度误差为**3.70°**，相比单视图光度立体（512.22 nm, 12.99°）和粗初始化（25.11 nm, 7.85°）有数量级提升。在真实样品上，NFH-SEM一致优于传统多视图与单视图方法，精确恢复**478 nm**打印层、**782 nm**表面纹理和微米级断裂台阶等细节。阴影分离模块实现平均检测准确率**81.7%**，自动排除遮挡区域对训练的干扰。

**局限与开放问题**：当前模型假设均匀电子发射系数（依赖样品涂层），对无涂层或低导电率样品可能因充电效应导致图像漂移；极端遮挡下所有BSE象限均无信号时无法恢复几何；缺乏真实微纳尺度真值限制了非TPL样品的绝对精度验证。未来方向包括：扩展为材料感知的发射模型以适应多相样品、直接在SEM数据上联合优化相机位姿、融合SE信号边缘效应作为额外几何线索，以及将物理模拟约束反哺到训练中。

## 背景与动机

### 微观三维表面重建的科学需求

在材料科学、生物力学和微纳制造等领域，精确获取微结构的三维表面形貌是理解其功能机制的关键。图 1 展示了花粉纹理、断裂表面等多种材料中具有重要功能角色的微观结构——这些结构直接影响花粉对传粉者的附着能力、固体中的裂纹扩展行为等核心科学问题。然而，在微米至纳米尺度下实现高保真的表面重建，对成像技术与重建算法提出了严苛挑战。

### 扫描电镜成像的物理特性与重建机遇

扫描电子显微镜（SEM）凭借其纳米级分辨率和灵活的成像模式，成为微观形貌表征的主流工具。其中，二次电子（SE）信号对表面形貌敏感，常用于多视图立体重建；而背散射电子（BSE）信号携带更强的方向性几何信息，尤其是四象限BSE探测器能够从四个方位角方向捕获电子发射强度，为单视图光度立体提供了物理基础。

传统BSE强度模型将探测器信号 $I_i(n)$ 描述为表面法向 $n$ 的函数：

$$I_i(n) = \mathbf{R}_0(\theta_n) \left[ d_i \cos(\varphi_i - \varphi_n) \sin(\theta_n) + c_i \cos(\theta_n) \right]$$

其中 $\mathbf{R}_0(\theta)=\sec(\theta)$ 为固定形式的发射放大项，$\theta_n$ 和 $\varphi_n$ 分别为法向的极角和方位角，$d_i$ 和 $c_i$ 为探测器象限 $i$ 的响应参数。消去 $\sec$ 项后，可进一步从相邻象限的强度差中直接估计表面梯度：

$$\frac{\partial z}{\partial x} = \frac{c}{d} \frac{I_A(n) - I_B(n)}{I_A(n) + I_B(n)}$$

这一公式构成了传统单视图SEM光度立体重建的理论基础。

### 现有方法的瓶颈

尽管SEM多探测器信号蕴含丰富的几何线索，现有重建方法面临三重瓶颈：

**无纹理区域失效。** 传统多视图立体重建（如Agisoft Metashape）依赖SE图像的纹理匹配，在SEM典型的大面积无纹理或重复纹理区域（如抛光截面、均匀涂层表面）中，特征匹配失效导致深度估计空洞或噪声严重，重建表面过度平滑，丢失亚微米级细节。

**阴影伪影与校准依赖。** 单视图光度立体方法利用BSE的方向性信号恢复表面梯度，但四象限探测器固有的几何遮挡会产生阴影区域——当某一象限被遮挡时，其信号不携带有效几何信息，直接使用会导致梯度估计严重失真。此外，传统模型中的参数 $c$ 和 $d$ 需要通过参考样品标定，这在实际操作中繁琐且难以适应不同材料和成像条件。

**学习型方法的领域鸿沟。** 近年来，基于神经辐射场（如NeuS）和3D Gaussian Splatting（如2DGS、PGSR）的通用重建方法在自然场景中取得了突破性进展。然而，这些方法隐式或显式地依赖自然图像的光照与反射模型，完全忽略了SEM的电子-物质相互作用物理。当直接应用于SEM数据时，缺乏物理先验导致严重的表面畸变、几何缺失和伪影，无法泛化至微观尺度。

### 核心动机与突破思路

本文的核心洞察在于：**SEM成像物理不应被视为需要标定的“障碍”，而应被建模为可学习的“资产”**。通过将可微的BSE前向模型嵌入到神经场的联合优化框架中，我们可以在无需参考样品的情况下实现探测器参数的自校准，同时利用四象限信号的方向性约束迭代分离阴影区域并提取高保真几何信息。

这一思路催生了NFH-SEM——一个将多视图粗几何先验与多探测器光度线索在连续神经场中融合的混合重建框架。其关键创新在于：以可学习的四阶多项式发射项 $\mathbf{R}(\theta) = 1 + p_1 \theta + p_2 \theta^2 + p_3 \theta^3 + p_4 \theta^4$ 替代固定的 $\sec(\theta)$ 模型，并与象限独立参数 $(c_i, d_i, e_i)$ 一同在训练中优化，从而突破了传统方法对经验公式和人工标定的依赖。

## 核心创新

### 瓶颈与突破

现有SEM三维重建方法面临三重困境：**传统多视图方法**（如Agisoft Metashape）在无纹理或重复纹理区域失效，产生过度平滑的表面；**单视图光度立体方法**依赖固定的经验BSE模型（含$\sec(\theta)$放大项），需要参考样品进行探测器校准，且对阴影遮挡毫无抵抗能力；**通用学习型重建方法**（如NeuS、2DGS、PGSR等）则因完全缺乏SEM物理先验，在微观尺度产生严重的表面畸变和不完整几何。其根本瓶颈在于：**BSE信号的物理生成过程未被有效建模为可学习的组件**，导致几何推断与探测器特性、阴影效应之间无法协同优化。

NFH-SEM的核心突破在于将这一物理过程**内嵌为可学习的BSE前向模型**，使其与SDF神经场联合优化，从而在无需参考样品的情况下实现探测器参数的自校准、阴影区域的自动分离，以及高保真微观表面重建。

### 关键创新点

**创新一：可学习BSE前向模型替代固定经验公式**

传统方法使用固定的$\mathbf{R}_0(\theta)=\sec(\theta)$作为电子发射放大项（Eq.1），这一简化假设无法准确描述真实BSE响应。NFH-SEM将其替换为**四阶可学习多项式**（Eq.5）：

$$\mathbf{R}(\theta) = 1 + p_1\theta + p_2\theta^2 + p_3\theta^3 + p_4\theta^4$$

同时为每个探测器象限引入**独立参数**$(c_i, d_i, e_i, p)$（Eq.6），使模型能够自适应地拟合不同象限的增益、偏置和发射特性。消融实验（Table 1）证实：移除多项式项（w/o Poly-R）导致Chamfer距离从17.48 nm升至19.96 nm，BSE模型误差高达7.16；强制象限共享参数（w/o 4Q-Var）使BSE模型误差升至1.35。这表明独立象限参数和灵活发射项对于精确建模BSE信号至关重要。

**创新二：隐式梯度提取与自校准机制**

传统单视图PS方法显式计算梯度（Eq.4）并直接积分，误差累积严重。NFH-SEM**不显式提取梯度**，而是通过可学习前向模型将预测法向映射为BSE强度，以渲染损失（Eq.9）反向传播梯度至神经场。这一设计使几何优化与探测器参数学习形成闭环：**探测器参数在无参考样品的情况下自校准**，几何推断同时受益于多视图深度先验和多探测器光度约束。消融中移除BSE前向模型（w/o BSE-F）、直接使用单视图梯度监督，Chamfer距离飙升至135.61 nm，法向误差升至7.48°，证明了隐式联合优化的决定性作用。

**创新三：迭代动态阴影分离**

BSE图像中因几何遮挡产生的阴影区域在传统方法中直接污染梯度估计。NFH-SEM通过**迭代动态阴影掩码**（与参数$d$自适应联动）自动识别并排除遮挡像素：根据前向模型残差生成软掩码$S_{ij}$，在BSE损失中屏蔽无效监督（Eq.9）。该模块在模拟数据上实现平均**81.7%的阴影检测准确率**（Figure 6c），消融中关闭阴影分离（w/o S-Mask）使Chamfer距离升至29.38 nm，证实了阴影处理对重建精度的关键贡献。

**创新四：三阶段渐进式融合策略**

NFH-SEM采用**三阶段训练策略**（Eq.11）逐步融合多源信息：阶段I仅用加权深度损失$\mathcal{L}_d$建立粗几何；阶段II引入BSE损失$\mathcal{L}_{\text{BSE}}$进行光度细化；阶段III激活阴影掩码，在排除遮挡的同时精调表面细节。这种渐进式融合避免了早期阶段BSE噪声对几何初始化的干扰，使模型能够稳健地从粗糙多视图先验收敛至高保真表面。

### 创新本质总结

NFH-SEM的方法论创新可归结为一个核心范式转换：**将SEM成像物理从固定的预处理步骤转变为可学习的、与几何表示协同优化的组件**。这一转变使得原本需要人工校准、易受阴影干扰、依赖经验公式的BSE信号，成为神经场优化中的有效几何线索。与通用学习型方法（NeuS、2DGS、PGSR等）的本质区别在于：NFH-SEM并非在通用视觉先验上做领域迁移，而是将SEM特有的电子散射物理直接编码进网络优化循环，从而在微观尺度上实现了通用方法无法企及的精度和鲁棒性。

## 整体框架

NFH-SEM 构建了一条 **多视图初始化 → 神经场联合优化 → 高保真表面提取** 的三阶段混合重建管线，其核心设计在于将可学习的 SEM 物理前向模型嵌入 SDF 神经场的优化循环中，使多视图几何与多探测器光度信息在统一框架下相互增强。

### 输入与数据流

管线的输入端包含两组互补信号（Figure 2a-b）：
1. **多视图 SE 图像**：通过电机驱动样品台在不同倾斜角度下采集的二次电子图像，用于恢复粗尺度几何。
2. **4Q-BSE 图像**：四象限背散射电子探测器同步获取的方向性信号，每个象限对应不同的照明方向，天然携带表面法向信息，同时伴随由几何遮挡引起的阴影区域。

### 三阶段处理流程

**阶段 I — 多视图几何初始化。** 利用 SE 图像经由传统多视图立体重建管线（Agisoft Metashape）生成带位姿的粗深度图及逐像素置信度权重（Figure 2c）。这一步为后续神经场提供了必要的空间锚定，避免了从零开始优化时的收敛困难。

**阶段 II — SDF 神经场与可学习 BSE 前向模型的联合构建。** 这是框架的核心创新层（Figure 2d）：
- **几何表示**：采用基于多分辨率哈希编码的 MLP 隐式建模 SDF，通过体积渲染沿每条 SEM 像素的反投影射线采样 3D 点，预测深度与法向。
- **物理前向模型**：不再使用传统的固定解析公式（如 $\sec(\theta)$ 放大项），而是引入一个可学习的四阶多项式发射项 $\mathbf{R}(\theta)$ 与象限独立参数 $(c_i, d_i, e_i, p_k)$，将预测法向映射为 4Q-BSE 强度。该模型在训练中自校准，无需参考样品标定。
- **损失驱动**：粗深度图以加权 L1 损失 $\mathcal{L}_d$ 提供几何监督；BSE 图像以 L1 损失 $\mathcal{L}_{\mathrm{BSE}}$ 提供法向监督；同时施加 SDF 梯度单位模正则 $\mathcal{R}_s$ 与前向模型参数正则 $\mathcal{R}_{\Phi}$。

**阶段 III — 迭代阴影分离与精细优化。** 在优化后期，框架自动检测 BSE 前向模型残差较大的像素，生成动态软掩码 $S_{ij}$ 排除遮挡区域（Figure 2b 中的阴影），使 $\mathcal{L}_{\mathrm{BSE}}$ 仅作用于有效信号。这一机制将阴影从“噪声源”转化为“遮挡线索”，显著提升重建鲁棒性。

### 输出

最终从收敛的 SDF 场中提取零水平集，获得高保真三维表面网格（Figure 2e）。整个训练过程约需 2 分钟 / 样品（3,000 次迭代），输出结果可精确恢复亚微米级特征（如 478 nm 打印层、782 nm 表面纹理和 1.559 μm 断裂台阶）。

### 与传统和学习型方法的本质区别

与“多视图重建 + 单视图光度立体后处理”的传统范式相比，NFH-SEM 将几何与法向线索在神经场内部统一优化，避免了误差累积；与 NeuS、2DGS 等通用学习型重建方法相比，其嵌入的 SEM 物理前向模型赋予了框架对电子散射过程的归纳偏置，从而在无纹理微观表面上显著抑制畸变与缺失几何。

### 补充图表

![[assets/figures/papers/paper_list_l2088_https_arxiv_org_abs_2508_04728/figures/008_Figure.jpg]]
*Figure: A1. Overview of the SEM imaging setup for multi-view and multi-detector scanning. External photograph of the SEM system used in our experiments and internal chamber views with the motorized specimen stage in flat and tilted positions*

![[assets/figures/papers/paper_list_l2088_https_arxiv_org_abs_2508_04728/figures/002_Figure_2.jpg]]
*Figure 2: Workflow of NFH-SEM. (a) Multi-view and multi-detector SEM scanning of a sample mounted on a motorized stage. (b) 4Q-BSE images provide directional illumination with shadows caused by geometric occlusion. (c) Multi-view reconstruction initialization. (d) The posed depth maps and 4Q-BSE images jointly supervise an SDF-based neural field. A learnable BSE forward model is self-calibrated during training. (e) The reconstructed surface extracted from the neural field exhibits high geometric fidelity and rich surface details*

## 核心模块与公式推导

### 3.1 BSE信号形成的物理模型

NFH-SEM的核心创新在于将SEM成像物理显式嵌入神经场优化框架。理解这一设计需从四象限背散射电子（4Q-BSE）探测器的信号形成机制出发。

当电子束以入射角 $\theta_n$ 轰击样品表面时，BSE信号强度与表面局部法向 $n$ 存在确定性几何关系。传统模型将第 $i$ 象限探测器接收的信号描述为：

$$I_i(n) = \mathbf{R}_0(\theta_n) \left[ d_i \cos(\varphi_i - \varphi_n) \sin(\theta_n) + c_i \cos(\theta_n) \right]$$

其中 $\varphi_i$ 为第 $i$ 象限的方位角（A、B、C、D四象限分别对应0°、180°、90°、270°），$\varphi_n$ 为表面法向的方位分量，$c_i$ 和 $d_i$ 为探测器象限的响应参数。$\mathbf{R}_0(\theta) = \sec(\theta)$ 为固定发射放大项，表征倾斜表面因电子逃逸路径缩短而增强的信号强度。

传统单视图光度立体方法通过消去 $\sec$ 项简化该模型，从A、B象限信号推导表面梯度：

$$\frac{\partial z}{\partial x} = \frac{c}{d} \frac{I_A(n) - I_B(n)}{I_A(n) + I_B(n)}$$

然后通过梯度积分重建高度图。这一范式存在三重瓶颈：（1）$\sec(\theta)$ 的固定形式无法适配真实BSE角响应；（2）$c/d$ 比值需参考样品标定，缺乏自校准能力；（3）阴影区域直接破坏梯度估计，无有效分离机制。

### 3.2 可学习BSE前向模型

NFH-SEM将上述解析模型重构为**可学习前向模型**，与SDF神经场联合优化，实现参数自校准与阴影自动分离。

**多项式发射项**替代固定 $\sec(\theta)$，以四阶多项式灵活适配真实BSE角响应：

$$\mathbf{R}(\theta) = 1 + p_1 \theta + p_2 \theta^2 + p_3 \theta^3 + p_4 \theta^4$$

完整可学习前向模型为：

$$\mathcal{F}_i(n) = \mathbf{R}(\theta_n) \big[ d_i \cos(\varphi_i - \varphi_n) \sin(\theta_n) + c_i \cos(\theta_n) \big] + e_i$$

其中可学习参数 $\Phi = \{p_{1:4}, c_i, d_i, e_i\}_{i=A,B,C,D}$ 包含：四个象限独立的线性响应参数 $c_i, d_i$、偏置项 $e_i$，以及共享的多项式系数 $p_{1:4}$。该设计的关键在于**象限独立参数**——消融实验中强制四象限共享参数导致BSE模型误差从最优值升至1.35（Table 1, Ours w/o 4Q-Var），验证了独立建模的必要性。

**阴影分离机制**与前向模型联动：当某象限预测值 $\mathcal{F}_i$ 与观测值 $b_{ij}$ 的残差异常大时，该像素被判定为阴影遮挡，生成软掩码 $S_{ij}$ 排除无效监督。这一迭代过程无需人工标注，平均阴影检测准确率达81.7%（Figure 6c）。

### 3.3 三阶段优化策略

神经场以SDF隐式表示几何，通过多分辨率哈希编码和MLP预测SDF值，经体积渲染输出深度和法向。训练分三阶段逐步融合几何线索：

**阶段I（仅深度监督）**：利用多视图SE图像经Agisoft Metashape生成的粗深度图 $z_j$ 和置信度权重 $w_j$ 监督：

$$\mathcal{L}_d = \frac{1}{M} \sum_j^M w_j |\widehat{z_j} - z_j|$$

辅以SDF梯度正则化 $\mathcal{R}_s = \frac{1}{MN} \sum_{j,k}^{M,N} (\lVert \nabla s_{jk} \rVert - 1)^2$，确保隐式场的良态性。

**阶段II（加入BSE监督）**：激活BSE损失，使用全1掩码（即无阴影排除）：

$$\mathcal{L}_{\mathrm{BSE}} = \frac{1}{4M} \sum_i^{A,B,C,D} \sum_j^M S_{ij} \odot |\mathcal{F}_i(\widehat{n}_j; \widehat{\Phi}) - b_{ij}|$$

此时神经场从前向模型隐式提取法向梯度信息，同时探测器参数 $\Phi$ 开始自校准。

**阶段III（激活阴影掩码）**：将 $S_{ij}$ 替换为自适应阴影软掩码，排除遮挡区域的噪声监督。三阶段总目标统一为：

$$\mathcal{L} = \begin{cases} \lambda_1 \mathcal{L}_d + \lambda_2 \mathcal{R}_s & \text{Stage I} \\ \lambda_1 \mathcal{L}_d + \lambda_2 \mathcal{R}_s + \lambda_3 \mathcal{L}_{\mathrm{BSE}}(1) + \lambda_4 \mathcal{R}_{\Phi} & \text{Stage II} \\ \lambda_1 \mathcal{L}_d + \lambda_2 \mathcal{R}_s + \lambda_3 \mathcal{L}_{\mathrm{BSE}}(S) + \lambda_4 \mathcal{R}_{\Phi} & \text{Stage III} \end{cases}$$

其中 $\mathcal{R}_{\Phi}$ 为探测器参数的轻量正则项。这一渐进式融合策略使神经场在粗几何先验的基础上，逐步吸收BSE信号的高频法向信息，同时避免阴影区域的梯度污染。

### 补充图表

![[assets/figures/papers/paper_list_l2088_https_arxiv_org_abs_2508_04728/figures/003_Figure_3.jpg]]
*Figure 3: Emission of the BSE signal from the sample surface and its detection by the 4Q-BSE detector*

## 实验与分析

### 模拟数据集定量评估

NFH-SEM在模拟TPL数据集（Wukong、Lucy、Lion）上进行了系统的定量消融实验，结果汇总于**Table 1**。完整模型取得了**平均Chamfer距离17.48 nm**、**法向角度误差3.70°**的优异表现，相较输入粗深度图（25.11 nm, 7.85°）分别提升7.63 nm和4.15°。与单视图光度立体基线（512.22 nm, 12.99°）相比，误差降低达**96.6%**，凸显多视图几何先验与BSE物理模型联合优化的决定性作用。

![[assets/figures/papers/paper_list_l2088_https_arxiv_org_abs_2508_04728/figures/007_Table_1.jpg]]
*Table 1: Quantitative ablation results on simulated dataset. Results are scaled to the physical dimensions of real TPL microstructures, and chamfer distances are reported in nm. The BSE model error is defined as the MAE between the estimated BSE intensity–θ mapping curve and the ground-truth curve, measuring how accurately the BSE forward model is learned (see supplementary material). Missing values are denoted by “–” because the corresponding methods do not estimate the BSE forward model. Best results are highlighted in bold*

消融实验揭示了各模块的因果贡献：

- **移除可学习BSE前向模型（w/o BSE-F）**：直接使用单视图光度立体梯度监督神经场，Chamfer距离骤升至**135.61 nm**，法向误差升至7.48°。这表明传统梯度集成方法在无纹理区域和阴影伪影下严重退化，而联合优化框架通过隐式梯度提取有效规避了这些瓶颈。
- **替换多项式发射项为固定解析模型（w/o Poly-R）**：Chamfer距离增至19.96 nm，BSE模型误差高达7.16。四阶多项式$R(\theta) = 1 + p_1\theta + p_2\theta^2 + p_3\theta^3 + p_4\theta^4$能够灵活适配真实BSE响应曲线，而固定$\sec(\theta)$项无法准确建模电子发射的角分布。
- **强制象限参数共享（w/o 4Q-Var）**：BSE模型误差升至1.35，证明各象限独立参数$\{c_i, d_i, e_i\}$对精确建模探测器响应至关重要。
- **关闭阴影分离（w/o S-Mask）**：Chamfer距离升至29.38 nm，遮挡区域的噪声BSE信号显著干扰几何优化，验证了迭代动态阴影掩码的必要性。

### 真实样品定性对比

在真实NFH-SEM数据集上，**Figure 4**展示了与两类传统方法的定性对比：

![[assets/figures/papers/paper_list_l2088_https_arxiv_org_abs_2508_04728/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison with conventional SEM 3D reconstruction methods on real-world dataset. Red boxes highlight 10μm enlarged normal maps. Red lines in SE images indicate the cross-sectional profiles, where the zoomed-in segments are marked between vertical gray lines. NFH-SEM faithfully reconstructs the overall geometry and fine surface details, consistent with SEM observations*

**多视图基线（Agisoft Metashape）**虽能恢复整体形状，但表面过度平滑，丢失了关键微观细节。以TPL打印结构为例，NFH-SEM精确恢复了**478 nm的逐层打印台阶**和**782 nm的表面纹理**，而多视图重建完全无法分辨这些特征。SiC断裂表面的**1.559 μm台阶**在NFH-SEM结果中清晰可辨，与已知断裂力学特征一致。

**单视图基线（4Q-BSE梯度积分）**产生严重的全局畸变，在花粉样品上表面曲率明显失真，无法保持生物结构的真实形态。这源于传统方法对$\sec(\theta)$放大项和阴影区域的敏感性，而NFH-SEM通过自校准前向模型和阴影分离从根本上解决了该问题。

### 与学习型方法的对比

**Figure 5**对比了NFH-SEM与五类学习型重建方法：

- **NeuS**（基于SDF的神经场重建）和**2DGS/PGSR/DN-Splatter**（基于3D Gaussian Splatting）在SEM域均产生严重的表面畸变和不完整几何。这些方法缺乏SEM成像物理先验，无法从多探测器信号中提取有效的几何约束。
- **VGGT/MapAnything**等前馈式模型同样失败，因为其训练数据域与SEM微观图像存在本质差异。

NFH-SEM通过嵌入可学习BSE前向模型$\mathcal{F}_i(n) = R(\theta_n)[d_i\cos(\varphi_i-\varphi_n)\sin(\theta_n) + c_i\cos(\theta_n)] + e_i$，将物理先验注入神经场优化，实现了跨材料（TPL聚合物、花粉、SiC）的鲁棒重建。

### 阴影分离与仿真验证

**Figure 6**验证了方法的物理合理性：

- **Figure 6a**：仿真BSE图像与真实观测高度一致，证明仿真管线准确复现了SEM成像过程。
- **Figure 6b**：学习的前向模型$R(\theta)$曲线与蒙特卡洛模拟真值高度吻合，验证了多项式参数化的充分性。
- **Figure 6c**：阴影分离模块实现**平均检测准确率81.7%**，自动排除遮挡区域，避免无效BSE监督污染几何优化。

### 失败模式与局限性

尽管NFH-SEM在多数场景下表现优异，仍存在以下已知失败模式：

1. **充电效应干扰**：当前模型假设均匀电子发射系数（依赖样品涂层），对无涂层或低导电率样品，充电效应可能导致图像漂移，破坏多视图对齐精度。
2. **材料混淆**：发射系数变异可能混淆几何与成分对比，目前尚未建模材料感知的发射模型。
3. **极端遮挡**：当所有BSE象限均被遮挡时，该区域完全丧失几何信息，无法恢复表面。
4. **真实真值缺失**：对于花粉、SiC等非TPL样品，缺乏微纳尺度真值，仅能通过定性视觉和语义验证（如已知打印层厚）评估精度。

### 补充图表

![[assets/figures/papers/paper_list_l2088_https_arxiv_org_abs_2508_04728/figures/006_Figure_6.jpg]]
*Figure 6: Simulation results. (a) Our simulated 4Q-BSE images are highly consistent with real 4Q-BSE observations, demonstrating our accurate modeling of BSE signal formation. (b) These curves are obtained by fixing φ and the learned parameters in Eq. (6) to derive the relationship between BSE intensity and θ. The estimated BSE forward model closely matches the ground truth across all detector quadrants. (c) NFH-SEM automatically separates most shadowed regions in the 4Q-BSE images, producing shadow intensity maps that align well with the ground truth. The percentage at the bottom right denotes the shadow detection accuracy (see supplementary material)*

![[assets/figures/papers/paper_list_l2088_https_arxiv_org_abs_2508_04728/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison with learning-based 3D reconstruction methods on real-world dataset. NFH-SEM achieves more accurate reconstructions than approaches that neglect the SEM signal generation model or lack generalization to SEM domains*

![[assets/figures/papers/paper_list_l2088_https_arxiv_org_abs_2508_04728/figures/010_Figure.jpg]]
*Figure: G3. Evaluation of learning-based MVS methods and robustness of NFH-SEM to different initializations. (a, c) Surface reconstructions of GeoMVSNet and MVSFormer++. (b, d) NFH-SEM reconstructions initialized with (a) and (c), respectively*

![[assets/figures/papers/paper_list_l2088_https_arxiv_org_abs_2508_04728/figures/017_Figure.jpg]]
*Figure: G7. Simulated BSE images acquired using a three-quadrant BSE detector*

![[assets/figures/papers/paper_list_l2088_https_arxiv_org_abs_2508_04728/figures/009_Figure.jpg]]
*Figure: E2. Comparison between real and simulated 4Q-BSE images. The simulated quadrant responses closely match the real detector signals, validating both the accuracy of our learned BSE forward model and the correctness of the BSE signal formulation used in our simulation pipeline*

![[assets/figures/papers/paper_list_l2088_https_arxiv_org_abs_2508_04728/figures/012_Figure.jpg]]
*Figure: G5. Comparison of BSE gradient extraction strategies for TPL microstructure reconstruction*

![[assets/figures/papers/paper_list_l2088_https_arxiv_org_abs_2508_04728/figures/013_Figure.jpg]]

## 方法谱系与知识库定位

### 1. 问题定位：SEM三维重建的瓶颈与范式转移

扫描电子显微镜（SEM）三维表面重建长期受困于一个核心矛盾：传统多视图方法依赖纹理特征匹配，在SEM特有的无纹理微观表面和电子束阴影下极易失效；而单视图光度立体方法虽然利用了探测器信号中的几何线索，却依赖固定的经验物理模型（如 `sec(θ)` 发射项）和参考样品校准，对复杂真实样品缺乏泛化能力。近年来涌现的学习型重建方法（如NeuS、3D Gaussian Splatting系列）在自然场景取得突破，但因缺乏SEM成像物理先验和领域训练数据，在微观尺度上产生严重表面畸变和几何缺失（Figure 5）。

NFH-SEM的核心突破在于识别出真正的瓶颈并非数据量或网络容量，而是**SEM成像物理与几何优化之间的割裂**。其因果机制可概括为：将可学习的BSE前向模型嵌入SDF神经场的联合优化框架，以自校准方式从多探测器信号中提取几何信息，同时迭代分离阴影区域，从而绕开了传统方法对固定经验公式和参考样品的依赖。

### 2. 方法谱系中的坐标定位

NFH-SEM处于三条技术路线的交汇点，但与每条路线中的代表方法存在本质差异：

| 技术路线 | 代表方法 | 与NFH-SEM的关系 | 关键差异 |
|---------|---------|----------------|---------|
| 传统多视图SEM重建 | Agisoft Metashape | 继承其多视图初始化流程 | NFH-SEM仅将其作为粗几何先验，后续通过BSE物理模型深度细化 |
| 单视图SEM光度立体 | 4Q-BSE梯度积分法 | 共享BSE信号模型的理论基础 | NFH-SEM将固定解析模型替换为可学习多项式发射项，实现自校准 |
| 学习型神经场重建 | NeuS, 2DGS, PGSR, DN-Splatter | 共享SDF/神经场表示框架 | NFH-SEM嵌入SEM物理前向模型，而通用方法缺乏领域特定物理约束 |

具体而言：

- **相对于传统多视图方法**：Agisoft Metashape等商业软件在SEM图像上常因无纹理区域和阴影伪影导致重建过度平滑或缺失细节。NFH-SEM保留了多视图重建的全局几何约束，但通过神经场连续表示和BSE光度监督，将精度从微米级提升至亚微米级（如恢复478 nm打印层厚、782 nm表面纹理）。

- **相对于传统单视图PS方法**：经典的4Q-BSE梯度积分方法（基于Eq.3-4）依赖`c/d`比值标定和`sec(θ)`放大项假设。NFH-SEM将固定发射项替换为可学习的四阶多项式（Eq.5），并为每个探测器象限引入独立参数`(c_i, d_i, e_i, p_{1:4})`（Eq.6），在无参考样品条件下实现参数自校准。消融实验（Table 1）表明，移除可学习前向模型（w/o BSE-F）导致Chamfer距离从17.48 nm飙升至135.61 nm，法向误差从3.70°升至7.48°，证明物理模型学习化的决定性作用。

- **相对于学习型重建方法**：NeuS（基于SDF的神经场重建）、2DGS/PGSR/DN-Splatter（基于3D Gaussian Splatting）、VGGT/MapAnything（前馈式模型）等方法在自然场景表现优异，但在SEM领域因缺乏物理约束而失效。Figure 5的定性对比显示，这些方法在微观表面产生严重畸变、孔洞和不完整几何。NFH-SEM的关键优势在于将SEM信号生成过程显式建模为可微前向模型，使网络在优化过程中遵守物理规律，而非纯数据驱动。

- **相对于学习型MVS方法**：GeoMVSNet和MVSFormer++等学习型多视图立体方法也被测试作为初始化替代方案（Figure G3），但其重建质量极差。值得注意的是，NFH-SEM即使从这些极差的初始化出发，仍能收敛到高保真表面，证明其优化框架的鲁棒性主要来源于BSE物理模型而非初始化质量。

### 3. 技术贡献的结构化拆解

NFH-SEM相对于基线的四个关键改进槽位（changed slots）构成了其技术贡献的核心：

1. **BSE前向模型可学习化**：将固定解析模型（`sec(θ)`放大项，无独立象限参数）替换为可学习的四阶多项式发射项（Eq.5）与象限独立参数（Eq.6）。消融实验（w/o Poly-R）显示，简化为解析模型后Chamfer距离升至19.96 nm，BSE模型误差高达7.16，证明多项式灵活性的必要性。

2. **梯度提取方式隐式化**：传统单视图PS直接使用Eq.4从象限强度比估计梯度，然后监督神经场。NFH-SEM通过可学习前向模型计算BSE图像并与观测比较，在联合优化中隐式提取梯度信息，避免了显式梯度估计的噪声放大问题。消融（w/o BSE-F）验证了这一转变的关键性。

3. **阴影处理动态化**：传统方法无阴影分离机制，直接使用全部BSE像素导致遮挡区域噪声污染重建。NFH-SEM引入迭代动态阴影掩码（与参数`d`自适应联动），实现平均阴影检测准确率81.7%（Figure 6c）。关闭阴影分离（w/o S-Mask）后Chamfer距离升至29.38 nm。

4. **探测器校准自主化**：传统方法需参考样品标定`c/d`比值。NFH-SEM将象限参数`(c_i, d_i, e_i)`作为可学习变量与神经场共同优化，实现自校准。强制所有象限共享参数（w/o 4Q-Var）导致BSE模型误差升至1.35，证明独立参数的重要性。

### 4. 适用边界与局限性

NFH-SEM的适用边界由以下假设和限制定义：

- **样品涂层假设**：当前模型假设均匀电子发射系数，适用于常规SEM观察中经过导电涂层处理的样品。对无涂层或低导电率样品，充电效应可能导致图像漂移，影响多视图对齐精度。这一限制在论文中被明确提及，但尚未定量评估其影响程度。

- **材料均匀性假设**：BSE前向模型不区分材料成分差异，将BSE强度变化完全归因于几何。对于多相材料样品，材料依赖的发射变异性可能混淆几何与成分对比。论文将此列为开放问题，提出未来可扩展为材料感知的发射模型。

- **极端遮挡失效**：当所有BSE象限均无信号时（如深孔底部），该区域无法恢复几何信息。这是BSE信号的本质限制，而非方法缺陷。

- **真实真值缺失**：模拟数据集虽可提供定量评估（Chamfer距离17.48 nm，法向误差3.70°），但真实样品（如花粉、SiC断裂面）缺乏微纳尺度真值，限制了对非TPL样品的绝对精度验证。当前真实数据评估以定性视觉和语义验证为主（如已知打印层厚478 nm）。

- **位姿依赖**：当前流程依赖离线SfM（Agisoft Metashape）进行相机位姿估计。论文将此列为开放问题，探讨是否可直接在SEM数据上联合优化位姿。

### 5. 开放问题与未来方向

论文明确或隐含提出了以下开放问题：

1. **材料感知扩展**：能否将前向模型扩展为材料感知的发射模型，以处理多相样品？这需要建立BSE信号的材料依赖性模型，可能通过引入材料参数或从SE信号中提取成分信息。

2. **端到端位姿优化**：是否可直接在SEM数据上联合优化相机位姿，避免对离线SfM的依赖？这将使方法更适用于原位实验和动态过程观察。

3. **成像参数鲁棒性**：方法对不同加速电压、工作距离和探测器配置的鲁棒性如何？Figure G7-G8展示了三象限BSE配置的初步适应性，但系统性参数敏感性研究仍是空白。

4. **多信号融合**：能否融合SE信号的边缘效应作为额外的几何线索？SE信号对表面形貌敏感，可能补充BSE在特定区域的不足。

5. **物理模拟闭环**：如何利用重建表面进行物理模拟（如断裂分析），并将物理约束反哺到训练中？这代表了从“重建用于分析”到“分析指导重建”的范式升级。

6. **探测器配置泛化**：Figure G7-G8初步展示了方法对三象限BSE探测器的适应性，但更广泛的探测器几何（如环形探测器、不同象限角分布）下的性能尚未系统验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/Neural_Field_Based_3D_Surface_Reconstruction_of_Microstructures_from_Multi_Detector_Signals_in_Scanning_Electron_Microscopy.pdf]]