---
title: Illumination-Consistent Human-Scene Reconstruction from Monocular Video
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Illumination_Consistent_Human_Scene_Reconstruction_from_Monocular_Video.pdf
project_link: null
code_link: null
aliases:
- ICHSRFO
- ICHSRFMV
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入可学习的光体积（light volume）提供空间变化的局部光照线索，结合隐式阴影估计模块解耦并合成人体投射的软阴影，从而实现光照一致的渲染。
primary_logic: 通过统一框架联合推断几何、材质和空间变化光照，首次从日常单目视频中实现光照一致的人体-场景重建，并支持重光照和场景迁移等下游应用。
claims:
- 在NeuMan数据集的六个序列上，全场景PSNR/SSIM/LPIPS均显著超过HUGS等强基线（例如Seattle PSNR 29.56 vs. HUGS 25.934，LPIPS 0.051 vs. 0.093）。
- 在人体区域上也取得最佳结果（Seattle PSNR 22.90 vs. HUGS 19.06），说明光照建模提升了对人物的还原。
- 消融实验表明，去除光体积和阴影估计模块均会导致PSNR下降（完整模型22.18 vs 无阴影21.59），验证了各组件的重要性。
- NeuMan - Seattle 上 PSNR = 29.56
---

# Illumination-Consistent Human-Scene Reconstruction from Monocular Video

> [!tip] 核心洞察
> 通过统一框架联合推断几何、材质和空间变化光照，首次从日常单目视频中实现光照一致的人体-场景重建，并支持重光照和场景迁移等下游应用。

| 字段 | 内容 |
|------|------|
| 中文题名 | 光照一致的单目视频人体-场景重建 |
| 英文题名 | Illumination-Consistent Human-Scene Reconstruction from Monocular Video |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zheng_Illumination-Consistent_Human-Scene_Reconstruction_from_Monocular_Video_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Illumination-Consistent Human-Scene Reconstruction Framework (Ours) |
| Dataset | NeuMan - Seattle, NeuMan - Lab |

> [!tip] 效果简介
> - NeuMan - Seattle 上，PSNR 29.56 vs 25.934 (HUGS) (+3.626)；SSIM 0.931 vs 0.852 (HUGS) (+0.079)；LPIPS 0.051 vs 0.093 (HUGS) (-0.042)。
> - NeuMan - Lab 上，PSNR 28.604 vs 25.994 (HUGS) (+2.610)。

## 概要

从单目视频中同时重建可驱动的人体与静态场景是计算机视觉中的一项核心挑战，其关键瓶颈在于**光照与阴影的建模缺失**。现有方法——无论是基于NeRF的**NeuMan**（Jiang et al., ECCV 2022）还是基于3D高斯泼溅的**HUGS**——均假设无穷远单一环境光照，无法捕捉空间变化的局部照明以及人体投射到场景上的动态阴影，导致渲染结果中人体外观与场景光照不一致，严重制约了真实感和下游应用潜力。

本文提出了一个**光照一致的人体-场景重建框架**，以3D高斯泼溅（3DGS）为基础，首次在统一管线中联合推断几何、材质与空间变化光照。方法核心包含三个创新设计：**可学习的光体积**以空间分布的光探测点提供局部入射光线索；**基于物理的渲染**使人体高斯具备反照率、粗糙度、金属度等材质属性，实现可重光照的人体外观；**隐式阴影估计模块**解耦并合成人体投射的软阴影，调制场景高斯的球谐系数。整个框架采用两阶段训练策略，先初始化几何与颜色，再引入物理光照建模。

在NeuMan数据集的六个序列上，本方法在全场景PSNR、SSIM、LPIPS上均显著超越HUGS等强基线（例如Seattle序列PSNR 29.56 vs. 25.934，LPIPS 0.051 vs. 0.093）；人体区域同样取得最优结果（Seattle PSNR 22.90 vs. 19.06）。消融实验证实，移除光体积或阴影估计模块均导致性能下降，验证了各组件的独立贡献。此外，方法还支持人体重光照与场景迁移等下游应用。

从单目视频中联合重建可动画的人体与静态场景，是计算机视觉与图形学中长期存在的挑战。这一任务不仅要求恢复场景和人物的精确几何与外观，还需保证两者在视觉上无缝融合。近年来，以 **NeuMan**（Jiang et al., ECCV 2022）为代表的 NeRF 驱动方法和以 **HUGS** 为代表的 3D 高斯泼溅（3DGS）方法，在人体-场景联合重建上取得了显著进展。然而，这些方法的共同瓶颈在于**忽视了光照与阴影效果**：它们通常假设人体与场景共享单一的环境贴图（即无穷远光照），无法建模空间变化的局部照明，更缺乏对人体投射阴影的显式处理。

这一瓶颈导致了两个层面的问题。其一，**人体外观不一致**——当人物在场景中移动时，其表面接收的入射光应随位置变化而改变，但现有方法无法捕捉这种空间变化，导致渲染结果缺乏真实感。其二，**场景真实度下降**——人体在场景中投射的软阴影是视觉真实性的关键线索，而现有方法完全缺失这一效果，使得合成画面显得“漂浮”且不自然。

上述问题的根源在于，单目视频本身提供了极其有限的观测——仅有一个视角、未知且可能变化的光照条件。要从这样的输入中同时解耦几何、材质和光照，是一个高度欠约束的逆渲染问题。现有方法要么完全回避光照建模（仅回归颜色），要么采用全局均匀的光照假设，无法刻画真实世界中光照的空间异质性和人体-场景间的阴影交互。

本文的动机正是填补这一空白：**首次从日常单目视频中实现光照一致的人体-场景重建**。核心思路是引入一种可学习的光体积（light volume）表示，为场景中任意位置提供局部光照线索，并结合隐式阴影估计模块解耦并合成人体投射的软阴影。通过这一统一框架，方法不仅提升了重建的视觉质量，还天然支持重光照、场景迁移等下游应用，为单目视频的人体-场景理解开辟了新的可能性。

## 核心方法与创新机理

本工作围绕“从单目视频中实现光照一致的人体-场景重建”这一目标，在现有3D高斯泼溅（3DGS）人体-场景重建框架的基础上，引入了三个关键创新，分别解决**空间变化光照表示**、**物理材质-光照解耦**和**动态阴影合成**三个瓶颈问题。

### 1. 光体积：从全局环境贴图到空间变化光照

现有方法（如**NeuMan**，Jiang et al., ECCV 2022；**HUGS**）普遍采用单一环境贴图表示场景光照，该假设隐含“无穷远光源”的前提，无法建模室内场景中常见的局部光照变化（如聚光灯衰减、墙壁反射）。本文提出**可学习的光体积（Light Volume）**，将场景空间划分为规则网格，每个网格顶点作为一个光探测点（light probe），存储球谐系数和潜在阴影特征。对于空间中的任意人体高斯点，通过查询其k近邻光探测点并插值，获得该位置处的入射光辐射：

$$L_i(\mathbf{x}, \omega_i) \approx \frac{\sum_k^n w_k(\mathbf{x}) L_k(p_k, \omega_i)}{\sum_k^n w_k(\mathbf{x})}$$

这一设计将光照表示从“全局均匀”升级为“空间变化”，使得人体在不同空间位置可获得差异化的光照，是实现光照一致渲染的核心机制。

### 2. 物理渲染管线：从纯颜色到材质-光照解耦

传统人体高斯（如**Vid2Avatar**、**4DGS**）直接预测颜色，材质与光照耦合在一起，无法支持重光照和场景迁移。本文将人体外观模型切换为**基于物理的渲染（PBR）管线**：通过哈希编码器从细化后的SMPL顶点预测反照率、粗糙度（$r$）和金属度（$m$）：

$$\{m, r\} = \mathcal{F}_m(\pmb{v})$$

同时引入**姿态感知的可见性估计器** $vis = \mathcal{F}_{vis}(v, \theta, \phi)$，缓解自遮挡带来的材质-光照解耦歧义。人体高斯的最终颜色通过蒙特卡洛积分计算：

$$c'(\omega_o) = \sum_{i=0}^{N_l} (f_d + f_s(\omega_o, \omega_i)) V(\omega_i) L_i(\omega_i) (\omega_i \cdot n) \Delta\omega_i$$

该公式中，$f_d$和$f_s$分别表示漫反射和镜面反射BRDF分量，$L_i$来自光体积插值，$V$为可见性项。材质与光照的显式分离使人体可被重光照或迁移至新场景。

### 3. 隐式阴影估计：从无阴影到动态软阴影

现有方法完全忽略人体在场景上投射的阴影，导致合成结果缺乏真实感。本文提出**隐式阴影估计模块**，利用光体积特征与空间描述符（相对位置编码$\gamma(\mathbf{r})$、方向编码$\gamma(\delta)$、深度$z$）预测遮挡因子：

$$ao = \mathcal{F}_{ao}(\gamma(\mathbf{r}), \gamma(\delta), z)$$

该遮挡因子直接调制周围场景高斯的球谐系数：

$$\mathcal{SH}' = ao \cdot \mathcal{SH}$$

这一轻量设计无需显式光线追踪，即可高效生成人体投射的动态软阴影，且阴影随人体姿态变化而自适应更新。

### 创新点之间的因果联动

三个创新并非孤立存在：光体积为PBR管线提供空间变化的光照输入，PBR管线输出的人体颜色与场景高斯通过阴影模块建立遮挡关系，最终在统一的泼溅渲染中合成光照一致的图像。消融实验证实了这一联动关系：移除光体积或阴影模块均导致PSNR显著下降（完整模型22.18 vs 无阴影21.59），验证了各组件的必要性和协同效应。

本方法的核心目标是从单目视频中联合重建光照一致的可驱动人体与静态场景，其整体框架围绕3D高斯泼溅（3D Gaussian Splatting）构建，并通过引入可学习的光体积（light volume）与基于物理的渲染（PBR）管线，首次实现了空间变化光照下的外观一致性建模。

### 两阶段重建策略

如图3（Figure 3）所示，人体重建采用两阶段策略，以逐步解耦几何、材质与光照：

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_Illumination_Con/figures/004_Figure_3.jpg]]
*Figure 3: Pipeline of human reconstruction. We use a two-stage strategy to model the human, with the yellow and black arrows representing the first and second stages, respectively*

- **第一阶段（黄色箭头）**：聚焦于几何初始化与颜色学习。基于SMPL网格定义标准空间（canonical space）中的人体高斯，通过线性混合蒙皮（LBS）将其变形到观察空间（observation space）。此阶段通过哈希编码器学习SMPL顶点的偏移量，得到细化的人体网格，并直接预测每个高斯的颜色属性，为后续物理建模提供稳定的几何先验。
- **第二阶段（黑色箭头）**：引入物理光照建模。在细化几何的基础上，进一步预测材质属性（金属度 $m$、粗糙度 $r$）与姿态感知可见性 $vis$，并通过光体积查询入射光辐射，执行基于物理的渲染来计算人体高斯的最终颜色。两阶段的解耦设计有效缓解了材质-光照的歧义性。

### 模块化Pipeline

整体推理流程（Figure 2）由四个核心模块串联构成：

**a) 人体高斯变换（Human Gaussian Transformation）**
在标准空间中，每个人体高斯绑定于细化后的SMPL网格顶点。通过K近邻（KNN）插值，从对应网格顶点获取材质属性 $\{m, r\}$、法向量 $n$、可见性 $vis$ 及LBS权重 $\mathbf{w} \in \mathbb{R}^{24}$。随后利用LBS将高斯从标准空间变形到当前姿态下的观察空间（Sec. 3.1）。

**b) 光体积查询与插值（Light Volume Query & Interpolation）**
光体积被设计为覆盖场景的空间网格，每个网格顶点作为一个光探测点（light probe），存储球谐系数以编码局部入射光分布。对于观察空间中的每个人体高斯，查询其 $k$ 个最近邻光探测点，通过距离加权插值得到该位置的入射光辐射 $L_i(\mathbf{x}, \omega_i)$（Eq. 6）。这一设计使光照能够随空间位置连续变化，突破了传统单一环境贴图假设无穷远光照的局限。

**c) 基于物理的渲染（Physically-Based Rendering）**
在获得入射光辐射后，对每个人体高斯执行蒙特卡洛积分，计算PBR颜色（Eq. 7）：
$$c'(\omega_o) = \sum_{i=0}^{N_l} (f_d + f_s(\omega_o, \omega_i)) V(\omega_i) L_i(\omega_i) (\omega_i \cdot n) \Delta \omega_i$$
其中 $f_d$ 为漫反射项，$f_s$ 为基于简化Disney BRDF的镜面反射项，$V$ 为可见性项。这一过程将人体外观从“纯颜色”提升为物理驱动的光照响应。

**d) 场景阴影估计（Scene Shadow Estimation）**
为建模人体投射到场景上的动态阴影，引入隐式阴影估计模块。对于每个场景高斯，解码器 $\mathcal{F}_{ao}$ 接收其相对人体的位置编码 $\gamma(\mathbf{r})$、方向编码 $\gamma(\delta)$ 以及从光体积提取的潜在阴影特征 $z$，预测遮挡因子 $ao$（Eq. 8）。随后将场景高斯的球谐系数 $\mathcal{SH}$ 调制为 $\mathcal{SH}' = ao \cdot \mathcal{SH}$（Eq. 9），从而在不增加显式几何计算的条件下高效合成动态软阴影。

**e) 联合泼溅与渲染（Joint Splatting & Rendering）**
最终，经过光照调制的人体高斯与场景高斯被合并，通过光栅化（splatting）渲染出RGB图像与深度图（Figure 2d）。这一联合渲染确保了人体与场景在光照和阴影上的一致性。

### 输入输出流

- **输入**：单目RGB视频序列，以及对应的SMPL姿态参数与人体分割掩码。
- **输出**：静态场景的3D高斯表示、可驱动人体（支持新姿态、新视角渲染）、空间变化的光体积、以及人体材质（反照率、粗糙度、金属度）。
- **下游应用**：框架天然支持人体重光照（relighting）与场景迁移（human-scene transfer），即在新环境光照条件下渲染人体，或将重建人体置入不同场景并匹配目标光照（Figure 8, Figure 9）。

> **注意**：该方法仍依赖SMPL姿态估计与人体分割的准确性，在极端姿态或严重遮挡下可能退化。光体积的建模能力受单目视频视角限制，未观察方向的光照估计存在不确定性。此外，隐式阴影模块目前仅处理人体对场景的单向投射阴影，未建模场景互反射等全局光照效果。

### 3.1 人体高斯表示与几何细化

人体高斯在**标准空间（canonical space）**中基于细化的SMPL网格定义，随后通过线性混合蒙皮（LBS）变形到观察空间。为获得更精确的几何，方法首先利用哈希编码器学习SMPL顶点的偏移和颜色：

$$\pmb{v}' = \pmb{v} + \mathcal{F}_\Delta(\pmb{v}),\quad \pmb{c} = \mathcal{F}_c(\pmb{v}) \tag{1}$$

其中 $\pmb{v}$ 为原始SMPL顶点，$\mathcal{F}_\Delta$ 预测顶点偏移量，$\mathcal{F}_c$ 预测顶点颜色。在细化网格基础上，进一步通过哈希编码器预测材质属性（金属度 $m$ 和粗糙度 $r$）：

$$\{m, r\} = \mathcal{F}_m(\pmb{v}) \tag{2}$$

**姿态感知可见性估计**是该模块的关键设计。由于单目视频中的人体自遮挡会带来材质-光照解耦的歧义性，方法引入可见性预测器，以顶点位置 $v$、姿态 $\theta$ 和视线方向 $\phi$ 为输入，预测每顶点可见性：

$$vis = \mathcal{F}_{vis}(v, \theta, \phi) \tag{3}$$

最终，每个人体高斯的材质属性 $(m, r)$、法向 $n$、可见性 $vis$ 和LBS权重 $w \in \mathbb{R}^{24}$ 均通过K近邻（KNN）从对应的网格顶点插值获得。

### 3.2 光体积与物理渲染

**瓶颈分析：** 现有方法普遍采用单一环境贴图假设无穷远光照，无法建模空间变化的局部照明效果（如室内多光源、近场遮挡）。本文的核心创新在于提出**可学习光体积（light volume）**，将场景空间离散为三维网格，每个网格顶点作为一个光探测点（light probe），存储球谐系数以编码该位置的入射光分布。

对于人体高斯表面点 $\mathbf{x}$，其入射光辐射通过查询 $k$ 个最近光探测点并插值获得：

$$L_i(\mathbf{x}, \omega_i) \approx \frac{\sum_k^n w_k(\mathbf{x}) L_k(p_k, \omega_i)}{\sum_k^n w_k(\mathbf{x})} \tag{6}$$

其中 $w_k(\mathbf{x})$ 为基于距离的权重，$L_k(p_k, \omega_i)$ 为第 $k$ 个探测点在方向 $\omega_i$ 上的辐射度。

在获得空间变化的入射光照后，人体高斯的渲染采用基于物理的渲染管线。渲染方程描述了从表面点 $\mathbf{x}$ 向方向 $\omega_o$ 出射的辐射度：

$$L_o(\omega_o, \mathbf{x}) = \int_{\Omega} f(\omega_o, \omega_i, \mathbf{x}) V(\omega_i, \mathbf{x}) L_i(\omega_i, \mathbf{x}) (\omega_i \cdot \mathbf{n}) d\omega_i \tag{4}$$

实际计算中采用简化的Disney BRDF和蒙特卡洛积分：

$$c'(\omega_o) = \sum_{i=0}^{N_l} (f_d + f_s(\omega_o, \omega_i)) V(\omega_i) L_i(\omega_i) (\omega_i \cdot n) \Delta\omega_i \tag{7}$$

其中 $f_d$ 为漫反射项，$f_s$ 为镜面反射项（由粗糙度 $r$ 和金属度 $m$ 参数化），$V(\omega_i)$ 为可见性项，$N_l$ 为采样方向数。

### 3.3 隐式阴影估计

人体在场景中投射的软阴影是光照一致性的关键，但直接物理模拟计算量过大。本文提出**隐式阴影估计模块**，通过解码器从光体积中提取光照特征，并结合空间描述符预测遮挡因子（ambient occlusion）：

$$ao = \mathcal{F}_{ao}(\gamma(\mathbf{r}), \gamma(\delta), z) \tag{8}$$

其中 $\gamma(\mathbf{r})$ 为场景高斯位置的频率编码，$\gamma(\delta)$ 为人体与场景高斯之间相对方向的编码，$z$ 为从光体积中提取的潜在阴影特征。预测的遮挡因子 $ao \in [0, 1]$ 直接调制周围场景高斯的球谐系数：

$$\mathcal{SH}' = ao \cdot \mathcal{SH} \tag{9}$$

这一设计的因果机制在于：将人体投射阴影的估计与场景高斯的颜色表示解耦，通过简单的乘法调制即可高效生成动态软阴影，避免了重新计算场景辐射传输的昂贵开销。

### 3.4 两阶段训练策略

为稳定地解耦几何、材质和光照，方法采用**两阶段训练策略**（Fig. 3）：

- **第一阶段（几何与颜色初始化）：** 仅优化人体高斯的几何（顶点偏移）和直接颜色属性，不涉及PBR和光体积，快速建立粗糙的人体形状和外观。
- **第二阶段（物理光照建模）：** 冻结几何参数，引入光体积、PBR渲染和阴影估计模块，联合优化材质属性、光照表示和阴影解码器，实现光照一致的渲染。

消融实验（Table 4）验证了各模块的因果贡献：完整模型在Lab序列上PSNR达22.18；移除阴影估计模块后降至21.59；进一步移除光体积和探测点损失后指标全面下降，证实空间变化光照表示和动态阴影建模均为性能的关键支撑。

## 实验与关键发现

### 核心瓶颈与因果机制

现有单目视频人体-场景重建方法（如 **NeuMan** (Jiang et al., ECCV 2022)、**HUGS**）普遍采用单一环境贴图假设无穷远光照，无法建模空间变化的局部照明与人体投射的动态阴影。这导致两个连锁问题：（1）人体外观在场景不同位置缺乏光照一致性；（2）场景表面缺失人体遮挡产生的软阴影，降低整体真实感。本文的因果干预点在于将光照表示从全局环境贴图升级为**可学习的光体积（light volume）**，同时引入**隐式阴影估计模块**解耦并合成投射阴影，从而在渲染管线中重建光照-几何-材质的物理耦合。

### 主实验结果

#### NeuMan 数据集全场景评估

Table 1 报告了在 NeuMan 数据集六个序列上的全场景定量结果。本文方法在所有序列上均显著超越基于 3DGS 的 **HUGS** 和基于 NeRF 的 **NeuMan** 等基线。以 Seattle 序列为例，PSNR 达到 29.56（HUGS 为 25.934，提升 +3.626），SSIM 0.931（HUGS 0.852），LPIPS 降至 0.051（HUGS 0.093）。Lab 序列同样取得 PSNR 28.604（对比 HUGS 25.994，+2.610）。这些提升的核心驱动力来自光体积提供的空间变化光照线索，使人体与场景的融合在光度上更一致。

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_Illumination_Con/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison on the NeuMan dataset [21]. Our method achieves state-of-the-art performance in all sequences*

#### NeuMan 数据集人体区域评估

Table 2 进一步剥离出人体区域的定量对比。在 Seattle 序列上，本文方法 PSNR 22.90，显著优于 HUGS 的 19.06（+3.84）和 NeuMan 的 16.79。SSIM 和 LPIPS 同样全面领先。该结果表明，基于物理的渲染（PBR）结合光体积插值的人体外观建模，不仅改善了场景级融合，也直接提升了人体本身的还原质量——尤其是在衣物褶皱、面部细节等需要精确光照交互的区域（见 Figure 4 绿框标注）。

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_Illumination_Con/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison of ours method with baseline mehods on the NeuMan dataset [21] over the human regions. Our method significantly outperforms NeRF-based and Gaussian-based baselines on all metrics*

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_Illumination_Con/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative results comparing our method with baseline methods. Our work shows better reconstruction quality both human and scene. Furthermore, our approach captures more human details (green boxes), lighting (blue boxes) and shadow effects (red boxes)*

#### ZJU-MoCap 数据集评估

Table 3 展示了在 ZJU-MoCap 多视角数据集上的新视角合成结果。本文方法取得 PSNR 30.73、SSIM 0.9705，超越现有 SOTA 方法。这验证了光体积和 PBR 管线在受控多视角场景下同样具备竞争力，且不依赖特定的单目视频假设。

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_Illumination_Con/figures/008_Table_3.jpg]]
*Table 3: Quantitative comparison of our method with SOTA methods on the ZJU-MoCap dataset [47]*

### 消融实验

Table 4 在 NeuMan Lab 序列上进行了系统的消融分析，逐一验证各组件的因果贡献：

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_Illumination_Con/figures/011_Table_4.jpg]]
*Table 4: Ablation study on several designs. All methods are trained and rendered on Lab sequence of NeuMan dataset*

- **移除光体积（w/o light volume）**：PSNR 从完整模型的 22.18 显著下降，同时 SSIM 和 LPIPS 均恶化。这直接证实空间变化光照表示是性能提升的核心瓶颈——回退到全局光照假设后，人体在场景不同位置的外观一致性被破坏。
- **移除隐式阴影估计模块（w/o shadow）**：PSNR 降至 21.59（-0.59），表明人体投射阴影的建模对场景真实感有不可忽略的贡献。该模块通过预测遮挡因子调制场景高斯的球谐系数（SH' = ao · SH），以轻量方式高效生成动态软阴影。
- **移除两阶段训练策略（w/o 2-stage training）**：性能同样下降，说明先优化几何与颜色、再引入物理光照建模的分阶段策略有助于稳定训练，避免材质-光照解耦中的歧义性。

### 定性分析

Figure 4 的定性对比直观展示了本文方法在三个维度上的优势：（1）人体细节（绿框）——衣物纹理和面部特征更清晰；（2）光照效果（蓝框）——人体肤色和服装亮度随场景位置自然变化；（3）阴影效果（红框）——人体在地面和周围物体上投射的软阴影被准确合成。这些视觉差异直接归因于光体积的局部光照线索和隐式阴影模块的遮挡推理。

### 下游应用验证

Figure 8 展示了人体-场景迁移结果：从 Lab 和 Bike 序列重建的人体被渲染到不同场景中，光照条件随目标场景自动适配。Figure 9 展示了重光照结果：同一人体在不同环境光照下呈现物理合理的明暗变化。这些应用的成功执行反向验证了光照分解的有效性——材质（反照率、粗糙度、金属度）与光照被成功解耦。

### 失败模式与局限性

尽管整体性能优异，方法仍存在以下已知局限：（1）依赖 SMPL 网格的姿态估计和人体分割，在极端姿态或严重遮挡下可能失效，导致人体高斯变形异常；（2）光体积的建模能力受单目视频视角限制，未观察到的方向照明可能不准确，在室外多光源场景中鲁棒性有待验证；（3）隐式阴影模块目前仅处理人体对场景的单向投射阴影，未建模场景互反射、间接光照等全局光照效果；（4）当前框架尚未扩展到多人交互或动态场景物体的光照建模。上述局限在原文中已被明确承认，需在实际部署中加以注意。

## 定位与知识库关联

### 方法沿革与基线关系

本文工作处于**单目视频人体-场景联合重建**这一研究脉络中，该脉络经历了从隐式神经表达到显式高斯泼溅的范式迁移。

**早期隐式方法**以 **NeuMan**（Jiang et al., ECCV 2022）为代表，采用 NeRF 驱动的人体-场景联合重建框架。这类方法虽能在一定程度上分离人体与场景，但受限于体渲染的计算开销，且缺乏显式光照建模，导致人体外观与场景光照脱节。**Vid2Avatar** 等后续工作进一步推进了从视频重建 3D 人体的隐式方法，但同样未解决光照一致性问题。

**基于 3DGS 的方法**近年来成为主流。**4DGS** 将 3D 高斯泼溅扩展到动态场景，实现了高效的动态重建；**HUGS** 则专门针对人体-场景分离重建设计，在渲染速度和质量上均有显著提升。然而，这些方法在光照建模上仍沿用单一环境贴图（假设无穷远光照），无法捕捉空间变化的局部光照效应和动态阴影。

本文方法的**核心突破**在于：在 3DGS 框架内首次引入完整的物理光照管线，将光照表示从“全局环境贴图”升级为“空间变化的光体积”，并配套设计了隐式阴影估计模块。这一改进使得人体外观与场景光照实现物理一致，从根本上解决了此前方法中人体“浮于场景之上”的外观割裂问题。

### 技术谱系定位

从技术组件角度，本文方法可视为以下三条技术路线的交汇点：

| 技术路线 | 继承来源 | 本文创新 |
|---------|---------|---------|
| **人体高斯表示** | 3DGS + SMPL 网格变形（继承自 HUGS 等） | 在标准空间定义高斯，通过 LBS 变形到观察空间 |
| **物理渲染（PBR）** | Disney BRDF 简化模型 + 蒙特卡洛积分 | 首次将 PBR 引入单目视频人体-场景联合重建 |
| **空间变化光照** | 光探针/光体积思想（借鉴图形学传统方法） | 可学习的光体积 + 球谐系数编码 + 隐式阴影解耦 |

值得强调的是，本文的**光体积**并非简单的光照存储结构，而是与人体高斯渲染管线深度耦合的**可学习表示**：每个光探测点存储球谐系数和潜在阴影特征，在渲染时通过 k 近邻插值为每个人体高斯提供局部入射光辐射。这一设计使得光照可以随空间位置平滑变化，突破了环境贴图“全局均匀光照”的假设。

### 适用边界

本文方法在以下条件下表现最优：

1. **单目固定相机视频**：输入为静态相机拍摄的单段视频，场景几何在拍摄期间保持不变。
2. **单人场景**：仅包含单个人体主体，人体分割和姿态估计能够可靠获取。
3. **相对可控的光照环境**：室内或室外阴影场景，光照主要来源于有限方向，光体积的探测点能够覆盖有效光照范围。
4. **SMPL 可拟合的姿态范围**：人体姿态需在 SMPL 模型的表达能力范围内，无极端自遮挡或非自然姿态。

### 局限与开放问题

**已知局限**（原文明确指出的）：

1. **姿态估计依赖**：方法仍依赖 SMPL 网格的姿态估计和人体分割作为初始化，对于极端姿态或严重遮挡场景可能失效。这是单目人体重建领域的共性问题。
2. **视角覆盖受限**：光体积的建模能力受单目视频的有限视角约束，未观察到的方向照明可能不准确，导致从不可见视角渲染时出现光照伪影。
3. **全局光照缺失**：隐式阴影模块目前仅处理人体在场景上的投射阴影（cast shadow），未建模场景互反射、间接光照等全局光照效果，在强间接光照场景中可能产生偏差。

**开放问题**（值得后续工作关注的方向）：

1. **复杂光照环境的鲁棒性**：如何在多光源、室外强光、动态光照变化等更复杂条件下保证光照分解的稳定性和准确性？当前光体积的球谐表示可能不足以捕获高频光照细节。
2. **透明/半透明物体**：是否可以将光体积与神经渲染场结合，处理透明衣物、玻璃等半透明材质的光照传输？这需要突破当前 PBR 管线的材质模型限制。
3. **多人交互场景**：当前方法假设单人场景，推广到多人交互时，人体间的相互遮挡和阴影投射将显著增加光照建模的复杂度，需要更高效的遮挡计算策略。
4. **动态场景物体**：场景中的动态物体（如移动的家具、车辆）同样会影响光照分布，如何将光体积扩展为时变表示是一个具有挑战性的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Illumination_Consistent_Human_Scene_Reconstruction_from_Monocular_Video.pdf]]
