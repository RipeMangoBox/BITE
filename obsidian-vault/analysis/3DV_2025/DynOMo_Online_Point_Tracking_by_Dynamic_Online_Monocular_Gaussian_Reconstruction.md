---
title: "DynOMo: Online Point Tracking by Dynamic Online Monocular Gaussian Reconstruction"
type: paper
paper_level: A
venue: 3DV
year: 2025
pdf_ref: paperPDFs/3DV_2025/DynOMo_Online_Point_Tracking_by_Dynamic_Online_Monocular_Gaussian_Reconstruction.pdf
project_link: https://jennyseidenschwarz.github.io/DynOMo.github.io/
code_link: null
aliases:
- DynOMo
tags:
- 3DV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "利用预训练的2D编码器（DINOv2特征、单目深度、语义分割）作为额外的重建监督信号，并结合基于特征相似度的邻域选择和正则化加权，使得运动可以在没有对应级别监督的情况下从3D重建中涌现。"
primary_logic: "通过增强静态2D编码器提取的特征、深度和语义信息，并将其融入动态3D高斯表示，可以在线重建动态场景并自然地产生点轨迹，且特征相似度比空间邻近度更适合引导运动正则化。"
claims:
- "DynOMo在没有运动信号监督的情况下在线跟踪点，通过增强的2D重建监督和3D正则化使物体运动自动涌现。"
- "为每个3D高斯扩展语义实例标签和视觉特征，以增强重建约束并指导正则化。"
- "基于特征相似度的高斯对加权（而非3D距离）显著提升了跟踪性能。"
- "在PanopticSports数据集上，DynOMo在单目设置下的2D中值平移误差（MTE）为6.3像素，大幅优于D-3DGS-Mono的23.3像素。"
---

# DynOMo: Online Point Tracking by Dynamic Online Monocular Gaussian Reconstruction

> [!tip] 核心洞察
> 通过增强静态2D编码器提取的特征、深度和语义信息，并将其融入动态3D高斯表示，可以在线重建动态场景并自然地产生点轨迹，且特征相似度比空间邻近度更适合引导运动正则化。

| 字段 | 内容 |
| ------- | ----------------------------------------------------------------------------------------------------------------- |
| 中文题名 | DynOMo：基于动态在线单目高斯重建的在线点追踪 |
| 英文题名 | DynOMo: Online Point Tracking by Dynamic Online Monocular Gaussian Reconstruction |
| 会议/期刊 | 3DV 2025 |
| Links | [paper](https://arxiv.org/abs/2409.02104) · [Project](https://jennyseidenschwarz.github.io/DynOMo.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DynOMo |
| Dataset | PanopticSports, TAPVid-DAVIS |

> [!tip] 效果简介
> - PanopticSports 上，MTE_2D (px) 为 6.3，对比 23.3 (D-3DGS-Mono)，变化 -17.0。
> - PanopticSports 上，MTE_3D (cm) 为 26.1，对比 56.0 (D-3DGS-Mono)，变化 -29.9。
> - TAPVid-DAVIS 上，AJ 为 45.8，对比 13.0 (SplaTAM)，变化 +32.8。

## 概要

单目在线点追踪面临一个根本性瓶颈：在未知相机位姿的条件下，系统仅能依赖稀疏的RGB信号，却需要同时完成动态场景重建、相机运动估计以及任意点的时空轨迹追踪。缺乏多视图几何约束和准确的深度信息，使得这一任务极具挑战。DynOMo的核心洞察在于，通过将预训练的2D编码器——包括DINOv2视觉特征、单目深度估计和语义分割——提取的丰富先验信息融入动态3D高斯表示，可以在不依赖任何运动标注或光流监督的情况下，使物体运动从重建过程中自动涌现。

在方法定位上，DynOMo属于“以重建驱动追踪”的在线框架。与需要大规模运动标注预训练的离线2D追踪器（如**TAPIR**、**CoTracker**）不同，也与依赖测试时优化和光流监督的离线方法（如**OmniMotion**）不同，DynOMo在无位姿、无运动监督的条件下在线运行，通过扩展3D高斯参数化（为每个高斯添加语义实例标签和视觉特征）并设计多模态重建损失与特征引导的3D正则化，使点轨迹自然产生。

实验表明，DynOMo在单目设置下显著优于降级为单目的基线方法。在PanopticSports数据集上，其2D中值平移误差（MTE）为6.3像素，远低于D-3DGS-Mono的23.3像素；3D MTE为26.1 cm，相比基线降低约53%。在TAPVid-DAVIS上，DynOMo以在线、无预训练的方式取得45.8的AJ，与具有预训练的离线方法性能相当。消融实验进一步验证了特征重建损失、深度损失、局部刚性正则化以及基于特征相似度的邻域加权策略的关键作用。



### 问题定义：单目在线点追踪

点追踪（Point Tracking）旨在给定视频中任意查询像素，恢复其在整个序列中的时空对应轨迹。传统方法多采用离线范式，假设完整视频可一次性访问，并依赖大量运动标注数据进行预训练或测试时优化。然而，许多现实应用——如机器人导航、增强现实和实时视频分析——要求系统以在线方式逐帧处理，且无法获取精确的相机位姿。这催生了**单目在线点追踪**这一更具挑战性的任务设定：从无位姿的单目视频流中，实时估计任意点的2D和3D运动轨迹。

### 现有方法的局限

当前点追踪方法存在三个结构性缺口。

**第一，离线依赖与运动监督需求。** 以 **TAPIR** 和 **CoTracker** 为代表的2D追踪器需要大规模运动标注数据进行预训练，**OmniMotion** 则执行测试时离线优化并依赖光流监督。这些方法无法满足在线场景的实时性要求，且对运动标签的依赖限制了其在无标注环境中的泛化能力。

**第二，多视图几何约束的缺失。** 在线动态场景重建方法如 **D-3DGS** 依赖多视图相机阵列提供强几何约束，当降级为单目设置时，其2D中值平移误差（MTE）高达23.3像素，性能急剧退化。根本原因在于单目条件下，仅凭稀疏的RGB信号同时重建场景、估计相机运动并追踪动态点，构成了一个高度欠定的联合优化问题。

**第三，2D先验与3D表示的割裂。** 以 **SplaTAM** 为代表的在线SLAM方法专注于静态场景重建，缺乏对动态物体的显式建模能力。**SpaTracker** 虽利用单目深度估计和三平面特征进行追踪，但其离线特性和对显式对应的依赖限制了在线扩展性。现有方法未能有效桥接2D视觉基础模型的丰富先验与3D动态表示之间的鸿沟。

### 核心动机：从重建中涌现运动

DynOMo的出发点是一个关键观察：**当通过精心设计的2D重建监督和3D正则化约束动态3D高斯表示时，物体运动可以从重建过程中自动涌现，而无需任何显式的运动信号监督**。这一洞察颠覆了传统“先检测对应、再追踪运动”的范式，转而采用“追踪即重建”（tracking-by-reconstruction）的策略。

具体而言，该动机建立在三个支柱之上：

1. **预训练2D编码器提供强先验。** 现代视觉基础模型（如DINOv2特征编码器、单目深度估计器、语义分割器）能够从单张RGB图像中提取丰富的场景理解信息。将这些2D先验作为额外的重建监督信号注入3D高斯优化过程，可以有效补偿单目条件下几何约束的不足。

2. **特征相似度优于空间邻近度。** 传统方法在正则化时倾向于按3D欧氏距离分组高斯，但动态场景中空间邻近的物体可能具有完全不同的运动模式。基于视觉特征相似度的分组策略更能反映物体语义边界，从而引导更合理的运动正则化。

3. **在线3D高斯表示支持轨迹自然提取。** 动态3D高斯表示将场景建模为一组可随时间演化的基元，每个高斯的均值轨迹直接对应3D点的运动路径。通过跟踪与查询像素关联的高斯均值，可以同时获得2D和3D轨迹，无需额外的轨迹估计模块。

### 技术挑战

实现上述动机面临多重挑战。在未知相机位姿下，系统必须同时优化相机运动和场景结构，两者高度耦合。深度预测噪声会降低重建质量，尤其对新添加的高斯造成不良初始化。极端相机运动、长时间遮挡和物体加速度变化会破坏前向传播假设，导致跟踪漂移或丢失。此外，在线处理的因果性约束意味着系统无法访问未来帧信息，必须依赖历史观测进行运动预测。DynOMo通过多模态重建损失、实例引导的邻域选择以及特征加权的运动传播机制，系统性地应对这些挑战，在无运动监督的条件下实现了具有竞争力的在线点追踪性能。



## 核心方法与创新机理

DynOMo 的核心创新在于**将静态2D编码器的先验知识深度融入动态3D高斯表示**，使点追踪能力从重建过程中自然涌现，而无需任何运动信号监督或预训练。具体而言，该方法在三个层面突破了现有基线：

### 1. 增强的3D高斯参数化

传统动态3D高斯仅包含几何与外观属性 $(\mu, q, s, c, o)$，DynOMo 为每个高斯额外扩展了两个参数（见 Sec. 3.1）：

$$G_i^\tau \equiv (\mu_i^\tau, q_i^\tau, s_i, c_i^\tau, o_i, g_i, f_i^\tau)$$

- **语义实例标签** $g_i \in \mathbb{R}$：将高斯与特定物体实例绑定，使正则化能在同一物体内部进行，避免跨物体运动耦合。
- **视觉特征** $f_i \in \mathbb{R}^D$：来自预训练DINOv2编码器，提供比RGB更强的语义一致性信号，同时作为后续正则化加权的依据。

这一扩展是后续所有创新机制的基础——特征相似度引导的邻域选择、前向传播和正则化加权均依赖于此。

### 2. 多模态重建监督替代运动监督

基线方法仅使用RGB重建损失 $\mathcal{L}_I$，而 DynOMo 构建了四路加权重建损失（Eq. 5）：

$$\mathcal{L}_{rec} = \lambda_I \mathcal{L}_I + \lambda_F \mathcal{L}_F + \lambda_D \mathcal{L}_D + \lambda_B \mathcal{L}_B$$

其中 $\mathcal{L}_F$（特征重建）、$\mathcal{L}_D$（深度重建）和 $\mathcal{L}_B$（背景mask重建）均来自预训练2D编码器的预测。消融实验（Table 3）表明，**移除 $\mathcal{L}_F$ 导致 AJ 从 45.8 骤降至 35.9，移除 $\mathcal{L}_D$ 降至 37.2**，验证了多模态监督是实现“运动涌现”的关键因果杠杆——这些损失迫使3D高斯在特征空间和深度空间保持一致性，从而间接约束了物体的运动模式。

### 3. 特征相似度驱动的3D正则化与运动传播

这是 DynOMo 最具区分度的设计选择：

- **邻域选择**：基线方法（如 D-3DGS）基于3D欧氏距离选择最近邻，而 DynOMo 利用实例标签限制邻域仅在同一物体内，并使用特征余弦相似度 $s_{i,j}$ 进行加权（$w_{i,j} = s_{i,j}$）。消融实验显示，**将特征相似度替换为3D距离加权时，AJ 从 45.8 下降至 42.1**（Table 3），证明语义一致性远优于空间邻近性。

- **前向传播**：高斯均值的传播采用基于特征相似度加权的kNN常数速度假设（Eq. 3）：
  $$\mu_i^{\tau+1} = \mu_i^{\tau} + \sum_{j \in \mathcal{N}_i} \sigma(s_{i,j}) (\mu_j^{\tau} - \mu_j^{\tau-1})$$
  其中 $\sigma(s_{i,j})$ 为特征相似度的 softmax 归一化。这一机制天然过滤了前一时刻的离群运动，增强了传播鲁棒性。

- **正则化损失**：局部刚性损失 $\mathcal{L}_{rigid}$、局部旋转相似性损失 $\mathcal{L}_{rot}$ 和长程局部等距损失 $\mathcal{L}_{iso}$ 均采用上述特征加权机制。移除 $\mathcal{L}_{rigid}$ 使 AJ 降至 37.9（Table 3），表明特征引导的正则化是维持物体结构完整性的核心。

### 创新总结

| 创新维度 | 基线做法 | DynOMo 做法 | 性能增益证据 |
|---------|---------|------------|------------|
| 高斯参数化 | 仅几何+外观 | 增加语义标签 $g_i$ 和视觉特征 $f_i$ | 固定 $f_i$ 导致 AJ 降至 30.8（Table 5） |
| 重建监督 | 仅RGB | 四路多模态损失（RGB+特征+深度+背景） | 移除 $\mathcal{L}_F$: AJ -9.9; 移除 $\mathcal{L}_D$: AJ -8.6 |
| 邻域选择 | 3D欧氏距离kNN | 实例内特征相似度kNN | 替换为距离加权: AJ -3.7 |
| 运动传播 | 无或简单假设 | 特征加权的kNN常数速度+常数旋转 | 核心组件，消融见正则化损失 |
| 正则化加权 | 均匀或距离加权 | 特征余弦相似度加权 | 移除 $\mathcal{L}_{rigid}$: AJ -7.9 |

这些创新共同使 DynOMo 在单目、无位姿、无运动监督的苛刻条件下，在 PanopticSports 上实现 2D MTE 6.3 px（对比 D-3DGS-Mono 的 23.3 px），在 TAPVid-DAVIS 上达到 AJ 45.8，**与需要大规模预训练和运动监督的离线方法性能相当**。



![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2409_02104/figures/002_Figure_2.jpg]]
*Figure 2: Tracking points with online dynamic monocular reconstruction: Our pipeline assumes an input video sequence, (predicted) depth maps, sparse segmentation masks as well as image features as input. In our online reconstruction pipeline we optimize for the camera pose C, add a set of new Gaussians based on the densification concept [14], optimize all Gaussians together and forward propagate G and C. Finally, we directly extract 3D point trajectories from single Gaussians G _ { p } and project them to the image plane to obtain 2D trajectories*

DynOMo 采用“以重建驱动追踪”（tracking-by-reconstruction）的在线范式，在无相机位姿、无运动标注信号的单目视频上同时完成场景重建、相机定位与点追踪。整体管道以时间戳 $\tau$ 为步进单位，每帧接收一组外部先验输入——RGB图像、单目深度图、稀疏语义分割掩码以及预训练的视觉特征（DINOv2），在动态3D高斯表示上交替优化相机位姿与高斯属性，并向前传播运动状态，最终从特定高斯的时间演化中直接提取2D与3D轨迹。

管道可概括为六个核心阶段：

1. **高斯与相机初始化**：首帧利用单目深度图将像素提升至3D空间，初始化一组3D高斯，相机位姿设为单位矩阵。
2. **相机位姿优化**：固定高斯参数，仅通过背景区域的重建损失优化当前帧的相机位姿，避免前景动态对象干扰位姿估计。
3. **新高斯添加**：根据像素密度掩码识别未充分观测的区域，动态添加新的高斯以扩展场景表示。
4. **高斯属性优化**：固定相机位姿，使用多模态重建损失与3D正则化损失联合优化所有高斯的属性。
5. **高斯与相机前向传播**：基于特征相似度加权的kNN常数速度假设传播高斯均值，基于常数旋转假设传播旋转量，同时用速度前向映射预测下一帧相机位姿，为下一帧提供初始估计。
6. **轨迹估计**：在查询帧选择与查询像素2D投影最近的高斯，随时间跟踪其3D均值，获得该点的3D轨迹与投影后的2D轨迹。

输入输出流清晰：输入端为视频序列、深度图、语义掩码与DINOv2特征图；输出端为在线更新的动态高斯世界模型、估计的相机位姿序列，以及任意查询点的2D/3D运动轨迹。整个管道的关键设计在于将静态2D编码器的先验知识（深度、语义、特征）注入3D高斯表示，使得物体运动在无对应级别监督的情况下从重建过程中自然涌现。

**Figure 2** 展示了管道示意图，清晰标注了从输入到轨迹输出的各模块衔接关系。**Figure 3** 定性展示了随着视频推进，高斯世界逐步增加的过程，验证了在线扩展场景表示的能力。



DynOMo 将在线单目点追踪形式化为一个**在线动态3D高斯重建**问题，核心思想是：通过精心设计的2D重建监督和3D正则化，让运动信号在没有显式光流或对应标签监督的情况下自动涌现。整个在线管道由七个关键模块串联构成，每帧依次执行。

### 3.1 动态3D高斯参数化

DynOMo 在标准3D高斯的基础上扩展了两个关键参数。在时间戳 $\tau$，每个动态高斯定义为：

$$G_i^\tau \equiv (\mu_i^\tau, q_i^\tau, s_i, c_i^\tau, o_i, g_i, f_i^\tau)$$

其中 $\mu_i^\tau \in \mathbb{R}^3$ 为均值（3D位置），$q_i^\tau$ 为旋转四元数，$s_i$ 为尺度，$c_i^\tau$ 为颜色，$o_i$ 为不透明度。**新增的两个参数**是：
- **语义实例标签** $g_i \in \mathbb{R}$：由预训练分割模型预测，用于将高斯分组到同一对象实例内，指导后续邻域选择和正则化。
- **视觉特征** $f_i \in \mathbb{R}^D$：来自预训练编码器（如DINOv2）的像素级特征描述子，用于两个目的：(i) 作为增强的2D重建监督信号，使重建在特征空间上保持一致；(ii) 为正则化和前向传播提供基于相似度的加权指导。

3D高斯分布的标准形式为：

$$G_i(x; \mu_i, \Sigma_i) = e^{-\frac{1}{2}(x-\mu_i)^{T} \Sigma_i^{-1} (x-\mu_i)}$$

其中协方差 $\Sigma_i$ 由旋转 $q_i$ 和尺度 $s_i$ 参数化。通过α混合将投影到图像平面的2D高斯合成为像素颜色：

$$C_p = \sum_{i \in H} T_i \alpha_i c_i$$

这里 $T_i$ 为累积透射率，$\alpha_i$ 为由2D高斯权重和不透明度计算得到的混合系数，$H$ 为与像素 $p$ 相交的排序高斯集合。

### 3.2 在线重建管道

每帧处理包含七个步骤：

**1. 高斯与相机初始化**：第一帧利用预测深度图将像素提升到3D空间以初始化高斯，相机位姿初始化为单位阵。

**2. 相机优化**：固定高斯参数，仅通过背景区域的重建损失优化当前帧的相机位姿 $W^\tau$。

**3. 添加新高斯**：根据像素密度掩码，在未充分观测的区域添加新高斯，使场景表示随视频推进逐步增长。

**4. 高斯优化**：固定相机位姿，使用总损失 $\mathcal{L}_{total} = \mathcal{L}_{rec} + \mathcal{L}_{3D}$ 优化所有高斯属性。

**5. 高斯前向传播**：为下一帧提供初始估计。高斯均值的前向传播基于**特征相似度加权的kNN-常数速度假设**：

$$\mu_i^{\tau+1} = \mu_i^{\tau} + \sum_{j \in \mathcal{N}_i} \sigma(s_{i,j}) (\mu_j^{\tau} - \mu_j^{\tau-1})$$

其中 $\mathcal{N}_i$ 为高斯 $i$ 在特征空间中的 $k$ 个最近邻，$s_{i,j}$ 为特征向量 $f_i^\tau$ 与 $f_j^\tau$ 的余弦相似度，$\sigma(\cdot)$ 为softmax归一化。这一设计的直觉是：特征相似的高斯更可能属于同一运动模式，其运动向量更可靠；softmax加权可自动抑制异常运动的影响。旋转量采用**常数旋转假设**传播：

$$q_i^{\tau+1} = \Delta q_i^{\tau-1 \to \tau} * q_i^\tau$$

其中 $\Delta q_i^{\tau-1 \to \tau}$ 为前一步的相对旋转。

**6. 相机前向传播**：采用速度前向映射预测下一帧相机位姿。

**7. 轨迹估计**：对于查询像素 $p$，选择与其2D投影最近的可见高斯：

$$G_p = \operatorname*{min}_{G_i \in \mathcal{G}_v^\tau} (||p - \Pi(W^\tau \mu_i^\tau)||_2)$$

高斯的可见性由相交像素上的α累积和决定：

$$v_i^\tau = \sum_{p \in P_{G_i}} T_i \alpha_i$$

随后通过跟踪该高斯的3D均值随时间的变化获得轨迹：

$$x_p^{3D,\tau} = \mu_p^\tau, \qquad x_p^{2D,\tau} = W^\tau \mu_p^\tau$$

### 3.3 多模态2D重建损失

重建损失是运动涌现的核心驱动力，它组合了四种监督信号：

$$\mathcal{L}_{rec} = \lambda_I \mathcal{L}_I + \lambda_F \mathcal{L}_F + \lambda_D \mathcal{L}_D + \lambda_B \mathcal{L}_B$$

其中 $\mathcal{L}_I$ 为RGB图像重建损失，$\mathcal{L}_F$ 为特征重建损失，$\mathcal{L}_D$ 为深度重建损失，$\mathcal{L}_B$ 为背景mask损失。所有属性的渲染通过统一的α混合公式完成：

$$A_p = \sum_{i \in H} T_i \alpha_i a_i$$

其中 $a_i$ 可为颜色 $c_i$、特征 $f_i$、深度值或背景标签。消融实验（Table 3）表明，$\mathcal{L}_F$ 和 $\mathcal{L}_D$ 是最关键的重建损失——移除特征损失导致 AJ 从 45.8 降至 35.9，移除深度损失使 AJ 降至 37.2。

### 3.4 实例引导的3D正则化

3D正则化损失 $\mathcal{L}_{3D}$ 包含三项：局部刚性损失 $\mathcal{L}^{rigid}$（强制相邻高斯保持相对距离）、局部旋转相似性损失 $\mathcal{L}^{rot}$、以及长程局部等距损失 $\mathcal{L}^{iso}$。每项损失在 $k$ 个最近邻上计算加权和：

$$\mathcal{L}^{x} = \frac{1}{k|\mathcal{G}|} \sum_{G_i \in \mathcal{G}} \sum_{G_j \in \mathcal{N}_i} w_{i,j} \mathcal{L}_{i,j}^{x}$$

关键的创新在于**邻域选择**和**加权机制**：
- **实例引导**：利用实例标签 $g_i$ 将邻域限制在同一对象内，避免跨对象的错误正则化。
- **特征相似度加权**：$w_{i,j} = s_{i,j}$，即特征余弦相似度，而非传统的3D欧氏距离。消融实验证实，将特征权重替换为3D距离权重时，AJ 从 45.8 下降至 42.1。这说明**特征相似度比空间邻近度更可靠地反映高斯的运动相关性**。

移除局部刚性损失 $\mathcal{L}^{rigid}$ 会使 AJ 降至 37.9，进一步验证了3D正则化对运动涌现的重要性。



## 实验与关键发现

### 核心实验设置与对比基准

DynOMo 在三个基准上接受评估：**PanopticSports**（多视图动态场景，我们降级为单目）、**TAPVid-DAVIS**（单目视频点追踪标准基准）和 **iPhone Dataset**（日常手持拍摄）。对比方法覆盖三类：在线3D重建方法（**D-3DGS-Mono**、**SplaTAM**）、离线2D点追踪器（**TAPIR**、**CoTracker**、**Pips**）以及测试时优化的离线方法（**OmniMotion**、**SpaTracker**）。需特别指出，DynOMo 未使用任何运动标签、对应监督或大规模预训练，而 TAPIR、CoTracker 等基线依赖大量运动标注数据预训练，OmniMotion 则执行测试时光流监督优化——DynOMo 处于明显不利的评估条件下。

### 主实验结果

**PanopticSports 数据集上的2D与3D追踪。** 在单目设置下，DynOMo 的2D中值平移误差（MTE₂D）为 **6.3 px**，大幅优于 D-3DGS-Mono 的 23.3 px（Table 1）。3D追踪同样显著领先：MTE₃D 为 **26.1 cm**，对比 D-3DGS-Mono 的 56.0 cm，误差降低约53%。这一差距的核心原因在于：D-3DGS 原版依赖27个多视图相机的丰富几何约束，降级为单目后丧失了深度和多视图一致性信息；DynOMo 通过预训练2D编码器（DINOv2特征、单目深度、语义分割）注入额外监督，弥补了单目信号的稀疏性。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2409_02104/figures/004_Table_1.jpg]]
*Table 1: Comparison on Panoptic Studio [24]: We compare our performance on PanopticSports as described in Sec. 4.1. D-3DGS-Mono represents the monocular setting of [24]. We observe that despite significantly more challenging setting, for 2D point tracking DynOMo outperforms [24]. Additionally, DynOMo outperforms D-3DGS-Mono considerably for 3D showing the effectiveness of our method. Finally, DynOMo⋆ shows that shows that there exists a 3D Gaussian that corresponds even better to the query point*

**TAPVid-DAVIS 上的2D追踪。** 在没有预训练和运动监督的条件下，DynOMo 取得 **AJ 45.8**、**δ_avg 63.1**、**OA 81.1**（Table 2）。该性能与离线且经大规模预训练的 OmniMotion（AJ 51.7）可比，且显著超越在线基线 SplaTAM（AJ 13.0）。值得注意的是，DynOMo 的 AJ 指标已接近 Pips（42.2）并超越部分早期离线方法，验证了“运动可从增强重建约束中涌现”这一核心主张。Oracle 版本 DynOMo⋆ 进一步达到 AJ 49.3，表明存在更优的高斯-查询点对应关系，轨迹估计模块仍有提升空间。

**iPhone Dataset 上的泛化能力。** 在手持拍摄的日常场景中，DynOMo 使用对齐后的 DepthAnything 深度图，3D端点误差（EPE）为 **0.161**，与使用真值位姿的 Deformable-3D-GS（0.151）和 SOM（0.082）相比具备竞争力（Table 4）。考虑到 DynOMo 同时在线优化相机位姿且无对应监督，这一结果证明了方法的鲁棒性和泛化潜力。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2409_02104/figures/007_Table_4.jpg]]
*Table 4: Iphone Dataset:. We compare the performance of DynOMo using the aligned DepthAnything [44] maps from [39] to other approaches on the Iphone dataset [10]. Note, prior approaches are all offline and mostly require correspondece-level supervisory signal for motion. We show DynOMo leads to emergent motion in 2D as well as in 3D. Additionally, we show that even with camera pose optimization our EPE is highly competitive compared to the other approaches that all use ground truth or refined camera pose information*

### 消融实验：设计选择的影响

Table 3 系统拆解了各模块的贡献，所有消融均在 TAPVid-DAVIS 上以 AJ 为主要指标：

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2409_02104/figures/006_Table_3.jpg]]
*Table 3: Ablation of Importance of Design Choices: We show the importance of the reconstruction as well as the 3D loss functions. We see that for the prior the embedding as well as the depth losse and for the latter the rigidity loss as well as the semantic weighting are the most important, respectively. We also show the importance of our Gaussian attibute regularizations*

**重建损失的关键性。** 移除特征重建损失 $L_F$ 导致 AJ 从 45.8 骤降至 **35.9**（-9.9），移除深度重建损失 $L_D$ 降至 **37.2**（-8.6）。这表明 DINOv2 特征提供的语义级稠密约束和单目深度提供的几何先验是运动涌现的基石——仅靠 RGB 重建无法在单目动态场景中建立可靠的跨帧对应。

**3D正则化的作用。** 移除局部刚性损失 $L_{rigid}$ 使 AJ 降至 **37.9**（-7.9），验证了“同一物体上的高斯应保持刚性运动”这一归纳偏置的必要性。更关键的是，将特征相似度加权替换为3D距离加权时，AJ 下降至 **42.1**（-3.7），直接证明了核心因果主张：**特征相似度比空间邻近度更适合引导运动正则化**。语义实例引导的邻域选择进一步强化了该机制——它确保正则化仅在同类物体内部传播，避免跨物体边界的错误平滑。

**高斯属性正则化。** 固定颜色 $c_i$、特征 $f_i$ 和背景掩码 $\mu_b$ 导致 AJ 暴跌至 **30.8**，说明在线优化中持续更新高斯外观属性对保持追踪一致性至关重要。使用各向同性高斯替代各向异性高斯使 AJ 降至 **42.7**，表明细粒度的形状表达能力有助于精确的3D定位。

**深度预测源的影响（Table 6）。** 在 PanopticSports 上，替换深度预测源（DepthAnything 与 D-3DGS 渲染深度）对2D追踪的总体指标影响较小，但高精度指标（如2D 1%距离内点比例）和3D追踪指标出现严重下降。这说明当前管道的2D追踪对深度噪声有一定容忍度，但精确的深度估计仍是提升3D追踪精度的关键瓶颈。

**轨迹估计策略（Table 7）。** 基于最近2D投影的高斯选择策略在2D追踪中表现最优；α-合成策略因逐帧独立选择高斯而无法保证时序一致性，性能明显落后。当可获取度量深度时，直接在3D空间选择最近高斯能提升3D追踪精度。

### 失败模式与局限性

Figure 4 和论文分析揭示了四类典型失败场景：

1. **极端遮挡**：长时间遮挡后，在线管道缺乏全局信息，难以恢复对被遮挡点的追踪，且像素密度掩码可能不会在遮挡物移除后及时添加新高斯。
2. **极端相机与物体运动**：当背景纹理不足且相机快速运动时，位姿估计和重建质量同时退化，与常规SLAM方法面临相同困境。
3. **极端加速度变化**：基于特征加权kNN的常数速度前向传播假设（Eq. 3）在物体突然加速或减速时失效，导致高斯均值预测偏离真实位置。
4. **新物体出现**：当新物体出现在先前已观测区域前方时，由像素密度决定的添加掩码可能不会为其分配新的高斯，造成重建空洞。
5. **旋转物体的新露面**：对旋转物体的新出现面无法高效填充高斯，可能导致重建不完整。
6. **深度预测噪声**：噪声深度图对新添加高斯的初始化质量影响显著，进而降低追踪鲁棒性。

### 关键图表结论

- **Table 1**：单目设置下2D追踪误差仅为多视图基线的27%，3D追踪误差降低53%，证明增强2D监督可有效替代多视图几何约束。
- **Table 2**：无预训练在线方法达到与离线预训练方法可比的AJ，验证“运动涌现”范式的有效性。
- **Table 3**：特征损失和深度损失是追踪性能的两大支柱，特征相似度加权显著优于距离加权，构成方法的核心因果机制。
- **Figure 3**：在线世界增长可视化表明，管道能随着视频推进逐步添加高斯，实现对场景的动态探索。
- **Figure 4**：失败案例揭示了常数速度假设、遮挡恢复和位姿估计在极端条件下的脆弱性，为后续改进指明了方向。

## 定位与知识库关联

### 方法谱系：从离线到在线、从多视图到单目

DynOMo 处于**在线单目点追踪**这一新兴任务节点，其核心思路是“以重建驱动追踪”（tracking-by-reconstruction），与当前主流方法存在显著范式差异。

**与离线 2D 追踪器的关系。** 当前点追踪领域的主流方法几乎全部依赖大规模运动标注数据的预训练，且以离线方式运行。**TAPIR**（Doersch et al., NeurIPS 2023）和 **CoTracker**（Karaev et al., ICCV 2023）利用 Transformer 架构建模轨迹间的相关性，在 TAPVid-DAVIS 上分别达到 56.2 和 48.7 的 AJ。**OmniMotion**（Qian et al., CVPR 2023）则采用测试时优化，以光流作为显式运动监督。DynOMo 在**不使用任何运动标签或对应监督、且无需预训练**的条件下，在 TAPVid-DAVIS 上取得 45.8 AJ，与 OmniMotion（51.7）差距仅约 6 个点，且显著超越 Pips（42.2）——这证明了“运动从 3D 重建中涌现”这一范式的可行性。

**与在线 SLAM/动态重建方法的关系。** 在在线方法中，**SplaTAM**（Keetha et al., CVPR 2024）是面向静态场景的密集 RGB-D SLAM 方法，直接用于动态点追踪时 AJ 仅为 13.0，暴露了静态假设的脆弱性。**D-3DGS**（Luiten et al., CVPR 2024）是目前最接近的工作——它同样基于动态 3DGS 进行在线重建和追踪，但原版依赖 27 个多视图相机。DynOMo 将其降级为单目版本 D-3DGS-Mono 作为对比基线：在 PanopticSports 上，DynOMo 的 2D 中值平移误差（MTE）为 6.3 像素，远优于 D-3DGS-Mono 的 23.3 像素；3D MTE 为 26.1 cm vs. 56.0 cm。这一差距的核心原因在于：多视图几何约束丧失后，D-3DGS 缺乏足够的重建监督信号，而 DynOMo 通过引入预训练 2D 编码器的特征、深度和语义信息弥补了这一缺陷。

**与离线 3D 追踪方法的关系。** **SpaTracker**（Xiao et al., ECCV 2024）依赖单目深度估计和三平面特征进行离线追踪；**Deformable-3D-GS**（Yang et al., 2023）和 **SOM**（Qi et al., 2023）则在 iPhone 数据集上展示了强大的 3D 追踪能力（EPE 分别为 0.151 和 0.082），但均需要真实或精修的相机位姿。DynOMo 在**同时优化相机位姿**的条件下取得 0.161 的 3D EPE，已具备竞争力，且是唯一无需位姿真值的在线方法。

### 适用边界与局限

DynOMo 的适用边界由其核心假设和外部依赖共同界定：

**适用场景。** 方法适用于具有适度相机运动和物体运动、背景纹理充足的单目视频。其在线特性使其天然适合流式处理场景，如机器人导航中的实时环境感知。对非刚性运动、遮挡和新物体出现具有一定鲁棒性（见 Figure 5 定性结果）。

**核心局限与失效模式。** 以下场景会导致性能显著下降（见 Figure 4）：

1. **极端相机运动与低纹理背景。** 当相机剧烈运动且背景缺乏纹理时，位姿优化和重建质量同时恶化——这是所有无回环检测的在线 SLAM 方法的共性瓶颈。
2. **长时间遮挡。** 在线特性意味着缺乏全局信息，被长时间遮挡的高斯无法从后续帧中恢复关联，导致跟踪中断。
3. **极端物体加速度。** 前向传播基于常数速度假设（Eq. 3），当物体加速度剧烈变化时，预测的高斯均值严重偏离真实位置，造成跟踪丢失。
4. **新物体出现在已观测区域前方。** 基于像素密度掩码的高斯添加策略可能无法为被遮挡的新物体分配新的高斯，导致其无法被跟踪。
5. **深度预测噪声。** 深度重建损失 L_D 对性能至关重要（移除后 AJ 从 45.8 降至 37.2），但单目深度估计的噪声会降低重建质量，尤其对新添加高斯的初始化造成不良影响，削弱跟踪鲁棒性。
6. **旋转物体的新露面。** 方法无法高效地为旋转物体的新出现面填充高斯，可能导致重建不完整。

### 开放问题

基于上述局限，以下方向值得进一步探索：

1. **实时性能。** 当前方法尚未达到实时运行速度，如何通过工程优化或轻量化设计实现真正的实时在线点跟踪，是混合现实和机器人应用的刚需。
2. **运动预测模型的升级。** 常数速度假设是失效的关键瓶颈——能否引入基于学习的运动预测（如物理启发的轨迹预测模块）替代简单的 kNN 加权外推，以应对极端加速度场景？
3. **长时记忆与重识别。** 在线框架中融入长时关联或记忆机制（如可学习的全局外观描述子），有望缓解长时间遮挡后的跟踪恢复问题。
4. **深度估计的改进。** 实验表明不同深度预测方法对 2D 跟踪影响较小，但对 3D 跟踪影响显著（Table 6）。未来更精确的单目深度模型（如 DepthAnything v2）可能大幅提升 3D 跟踪精度。
5. **旋转物体的全表面重建。** 能否利用零样本网格预测或前馈 3D 生成技术，为旋转物体快速生成全表面高斯，避免重建不完整？
6. **无监督涌现精度的上限。** 在完全无运动监督的条件下，涌现轨迹的精度能否进一步提升至与有监督方法相媲美？这可能需要更强大的 2D 编码器特征或更精巧的 3D 正则化设计。



## 原文 PDF

![[paperPDFs/3DV_2025/DynOMo_Online_Point_Tracking_by_Dynamic_Online_Monocular_Gaussian_Reconstruction.pdf]]
