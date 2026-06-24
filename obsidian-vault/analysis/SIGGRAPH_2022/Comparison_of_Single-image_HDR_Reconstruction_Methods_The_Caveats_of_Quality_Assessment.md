---
title: Comparison of Single-image HDR Reconstruction Methods — The Caveats of Quality Assessment
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Comparison_of_Single_image_HDR_Reconstruction_Methods_The_Caveats_of_Quality_Assessment.pdf
project_link: "https://www.cl.cam.ac.uk/research/rainbow/projects/sihdr_benchmark/"
code_link: null
aliases:
- CCCBEP
- CSIHRMCQA
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 在计算全参考质量指标前，对重建图像进行CRF校正（通过拟合全局多项式颜色映射），消除CRF反演误差带来的色调/颜色偏移，从而使指标聚焦于饱和区域的重建质量。
primary_logic: 引入一个简单但有效的CRF校正步骤，可以显著提升现有质量指标与主观评价的相关性；但即使最佳指标也需要至少3.5 dB的PU21-PSNR差值才能可靠区分方法优劣，揭示了仅依赖客观指标进行SI-HDR评估的局限性。
claims:
- 只有两个SI-HDR方法平均而言比未处理的SDR图像更受偏好，其余四种方法倾向于降低质量。
- CRF校正后，PU21-PSNR与主观评分的Spearman相关性从0.62提升至0.79。
- 要确信一个方法优于另一个，PU21-PSNR的差异至少需要3.5 dB。
- 无参考指标PU21-PIQE在不进行CRF校正的情况下仍达到0.83的相关性。
---

# Comparison of Single-image HDR Reconstruction Methods — The Caveats of Quality Assessment

> [!tip] 核心洞察
> 引入一个简单但有效的CRF校正步骤，可以显著提升现有质量指标与主观评价的相关性；但即使最佳指标也需要至少3.5 dB的PU21-PSNR差值才能可靠区分方法优劣，揭示了仅依赖客观指标进行SI-HDR评估的局限性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 单图像HDR重建方法比较——质量评估的误区 |
| 英文题名 | Comparison of Single-image HDR Reconstruction Methods — The Caveats of Quality Assessment |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://www.cl.cam.ac.uk/research/rainbow/projects/sihdr_benchmark/) · [arXiv](http://arxiv.org/abs/1712.03686) · [Project](https://www.cl.cam.ac.uk/research/rainbow/projects/sihdr_benchmark/") |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | CRF校正评估协议（CRF Correction-based Evaluation Protocol） |
| Dataset | 新构建的SI-HDR数据集（27张图像用于主观实验）, 主观实验与客观指标相关性（27张图像）, 全验证集（183张图像）方法排名可靠性 |

> [!tip] 效果简介
> - 新构建的SI-HDR数据集（27张图像用于主观实验） 上，主观偏好（JOD，相对于SDR输入） SingleHDR、Mask-HDR 平均JOD>0 vs SDR输入图像（JOD=0） (其余四种方法平均JOD<0，质量退化)。
> - 主观实验与客观指标相关性（27张图像） 上，Spearman ρ PU21-PSNR (CRF校正后): 0.79; PU21-VSI (校正后): 0.78; 最佳期望相关性0.87 vs PU21-PSNR (直接): 0.62; 其他常用指标<0.64 (+0.17 ~ +0.25)。
> - 全验证集（183张图像）方法排名可靠性 上，最小可区分差异（PU21-PSNR） 需至少3.5 dB差异才能可靠断言一个方法优于另一个（α=0.05） vs 许多现有论文报告的提高幅度低于该阈值 (N/A)。

## 概要

单图像HDR（SI-HDR）重建方法的客观评估长期受困于一个被忽视的瓶颈：重建图像与参考图像之间因相机响应函数（CRF）反演不准确而产生的大幅色调和颜色差异，淹没了对饱和区域真实HDR重建质量的衡量，导致现有全参考质量指标与主观评价的相关性极低。

本文提出了一种引入CRF校正的评估协议——在计算全参考质量指标前，对重建HDR图像施加全局多项式颜色映射（包括PQ空间亮度三阶多项式和u'v'色度空间三阶多项式），以消除CRF反演误差带来的系统性偏移。基于新构建的SI-HDR数据集和14名参与者的主观偏好实验，研究发现：六种主流方法中仅**SingleHDR**和**Mask-HDR**平均而言优于未处理的SDR输入，其余四种方法反而降低了图像质量。CRF校正后，PU21-PSNR与主观评分的Spearman相关性从0.62跃升至0.79，最佳指标组合（PU21-VSI、HDR-VDP-3）可逼近期望上界0.87。然而，即使最佳指标也需至少3.5 dB的PU21-PSNR差值才能可靠区分方法优劣，揭示了仅依赖客观指标进行SI-HDR评估的根本局限。无参考指标PU21-PIQE无需任何校正即可达到0.83的相关性，为实际部署提供了替代方案。

## 核心方法与创新机理

### 问题瓶颈：CRF反演误差淹没HDR重建质量评估

单图像HDR（SI-HDR）重建任务的核心挑战在于从单张8-bit SDR图像恢复高动态范围信息，尤其是在饱和区域。然而，本研究发现，评估这一任务时存在一个被长期忽视的系统性瓶颈：**相机响应函数（CRF）反演误差**。SI-HDR方法在从SDR图像反推线性HDR值时，通常无法精确逆转拍摄时的CRF，导致重建图像的色调和颜色与参考HDR图像存在系统性偏差。这种偏差并非真正的HDR信息重建失真，却在全参考质量指标计算中占据主导地位，淹没了对饱和区域重建质量的真实评估信号。

具体而言，当直接比较重建HDR图像与参考HDR图像时，CRF反演误差造成的颜色/色调偏移往往远大于饱和区域重建的细微差异，导致现有全参考客观质量指标与主观评价的相关性普遍低于0.64（见Figure 5a）。这意味着，即使一个SI-HDR方法在饱和区域重建上取得了实质进步，只要其CRF反演不够精确，客观指标就可能给出负面评价，反之亦然。这一发现揭示了仅依赖现有指标进行SI-HDR评估的根本局限性。

### 核心创新：CRF校正评估协议

针对上述瓶颈，本文提出的核心创新并非一个新的SI-HDR重建方法，而是一个**改进的评估协议**：在计算全参考质量指标之前，引入一个轻量级的CRF校正步骤。该协议的核心思想是：通过拟合一个全局多项式颜色映射，消除重建HDR图像与参考HDR图像之间因CRF反演不精确导致的系统性色调/颜色差异，从而使质量指标能够聚焦于饱和区域的重建质量这一真正有意义的评估维度。

Figure 1清晰地展示了这一评估协议的改进逻辑：传统协议（蓝色阴影框）直接将重建HDR与参考HDR比较，由于CRF反演误差导致的色调/颜色差异，这种比较不可靠；而新协议（绿色阴影框）在计算质量指标前先进行CRF校正，显著提升了指标的可靠性。

### Changed Slots：评估预处理步骤的根本性改变

相对于传统评估流程，本协议在**评估预处理步骤**这一关键环节做出了根本性改变：

- **基线做法**：直接比较重建HDR图像与参考HDR图像，可能采用简单的线性缩放或对数映射进行亮度对齐，但未系统性地消除CRF反演误差。
- **所提做法**：在计算任何全参考质量指标之前，先对重建HDR图像进行全局多项式CRF校正，包括PQ空间亮度三阶多项式映射和u'v'色度空间三阶多项式映射（考虑通道交叉），再在校正后的图像对上计算质量指标。

这一改变之所以有效，在于它切断了CRF反演误差到质量指标的错误传导路径。校正后的图像对在色调和颜色上实现了全局对齐，使得指标对饱和区域重建差异的敏感度显著提升。

### 方法框架与模块顺序

所提评估协议由四个顺序模块构成，形成一条清晰的推理链路：

1. **PQ编码亮度校正**
2. **u'v'色度校正**
3. **正则化最小二乘求解器**
4. **多指标质量计算**

下面对各模块的机理和因果关系进行详细展开。

#### 模块一：PQ编码亮度校正

该模块的目标是校正重建HDR图像在亮度域上的CRF反演误差。具体做法是：首先将重建HDR图像和参考HDR图像均转换到PQ（Perceptual Quantizer）传输编码空间，然后拟合一个从重建PQ亮度到参考PQ亮度的三阶多项式映射。

其优化目标为：

$$\arg \operatorname*{min}_{w_1,\dots,w_4} \left\| \begin{bmatrix} \hat{P}_1^3 & \hat{P}_1^2 & \hat{P}_1 & 1 \\ \vdots & \vdots & \vdots & \vdots \\ \hat{P}_N^3 & \hat{P}_N^2 & \hat{P}_N & 1 \end{bmatrix} \begin{bmatrix} w_1 \\ w_2 \\ w_3 \\ w_4 \end{bmatrix} - \begin{bmatrix} P_1 \\ \vdots \\ P_N \end{bmatrix} \right\|$$

其中，$\hat{P}_i$表示重建HDR图像第$i$个像素的PQ编码亮度值，$P_i$表示参考HDR图像对应像素的PQ编码亮度值，$w_1,\dots,w_4$为待求解的三阶多项式系数。选择PQ空间进行校正的原因在于，PQ编码本身就是为HDR内容设计的感知均匀空间，在该空间进行多项式拟合能够更好地匹配人眼对亮度差异的感知特性。

值得注意的是，该模块采用无正则化（$\lambda=0$）的最小二乘求解，因为亮度校正涉及的参数较少（4个系数），过拟合风险低。

#### 模块二：u'v'色度校正

亮度校正完成后，还需校正颜色域上的CRF反演误差。该模块在CIE u'v'色度空间进行操作，拟合一个考虑通道交互的三阶多项式映射，将重建HDR的色度坐标映射到参考HDR的色度坐标。

其优化目标为：

$$\underset{w_{1,1},\ldots,w_{8,2}}{\arg\min} \left\| \begin{bmatrix} \hat{u}_1'^3 \hat{v}_1'^3 & \hat{u}_1'^2 \hat{v}_1'^2 & \hat{u}_1'^2 \hat{v}_1' & \hat{u}_1' \hat{v}_1'^2 & \hat{u}_1' \hat{v}_1' & \hat{u}_1' & \hat{v}_1' & 1 \\ \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots \end{bmatrix} \begin{bmatrix} w_{1,1} & w_{1,2} \\ \vdots & \vdots \\ w_{8,1} & w_{8,2} \end{bmatrix} - \begin{bmatrix} u_1' & v_1' \\ \vdots & \vdots \\ u_N' & v_N' \end{bmatrix} \right\|$$

其中，$\hat{u}_i'$和$\hat{v}_i'$分别表示重建HDR图像第$i$个像素的u'和v'色度坐标，$u_i'$和$v_i'$为参考HDR图像的对应色度坐标。色度校正矩阵$\mathbf{W}$的维度为$8 \times 2$，包含16个待求解系数，其中8个基函数项包含了$\hat{u}'$和$\hat{v}'$的交叉项（如$\hat{u}'^2 \hat{v}'$、$\hat{u}' \hat{v}'^2$等），以捕捉颜色通道间的耦合效应。

选择u'v'空间而非其他色度空间（如xy色度）的原因在于，u'v'空间具有更好的感知均匀性，能够更准确地反映人眼对颜色差异的敏感度。色度校正在亮度校正之后进行，因为亮度对齐可以减少颜色校正的负担，避免颜色映射被迫补偿亮度差异。

#### 模块三：正则化最小二乘求解器

色度校正涉及16个参数，且某些图像可能包含极端的颜色值，直接使用普通最小二乘可能导致过拟合或产生不合理的颜色映射。为此，该模块引入Tikhonov正则化，通过带正则项的闭合解稳定地求解多项式系数：

$$\hat{\mathbf{W}} = (\mathbf{X}^T \mathbf{X} + \lambda \mathbf{I})^{-1} (\mathbf{X}^T \mathbf{Y} + \lambda \mathbf{W}_0)$$

其中，$\mathbf{X}$为设计矩阵（包含所有基函数项），$\mathbf{Y}$为目标值矩阵（参考色度坐标），$\lambda$为正则化参数，$\mathbf{W}_0$为先验均值矩阵。对于色度校正，正则化参数设置为$\lambda = 0.01 N/K$，其中$N$为像素数，$K$为基函数数量（此处$K=8$）。这一设置使得正则化强度与数据量自适应匹配：像素越多，正则化相对越弱，允许更精细的拟合；像素越少，正则化相对越强，防止过拟合。

先验矩阵$\mathbf{W}_0$被设置为恒等映射（即假设校正前色度已经是合理的），这相当于向无校正方向收缩，避免在数据不足时产生极端的颜色变换。亮度校正由于参数少（4个系数），过拟合风险低，因此设置$\lambda=0$，不使用正则化。

#### 模块四：多指标质量计算

在校正后的图像对上，计算多种全参考和无参考质量指标。本研究系统性地评估了包括PU21-PSNR、PU21-SSIM、PU21-VSI、HDR-VDP-2、HDR-VDP-3、FovVideoVDP、PU21-PIQE等在内的多种指标（完整列表见Table 1）。这些指标在计算前均需应用PU21变换，将线性RGB值映射到近似感知均匀的空间，以考虑眩光和对比度敏感度等视觉特性。

### 模块间的因果关系

四个模块之间存在清晰的因果依赖关系：

1. **亮度校正 → 色度校正**：亮度校正是色度校正的前提。如果亮度未对齐，色度校正将被迫同时补偿亮度差异，导致颜色映射不准确。先校正亮度可以消除这一干扰，使色度校正专注于颜色域的CRF反演误差。

2. **色度校正 → 正则化求解器**：色度校正的复杂性（16个参数、通道交叉项）使得正则化成为必要。正则化求解器为色度校正提供了稳定性保障，防止在极端图像上产生不合理的颜色映射。

3. **校正模块 → 质量计算**：前三个模块的输出是一对色调/颜色对齐的HDR图像，质量计算模块在此基础上运行。校正的质量直接决定了后续指标的有效性：校正越充分，指标对饱和区域重建差异的敏感度越高。

### 推理路径与使用方式

该评估协议的推理路径清晰且轻量：对于每一对待评估的重建HDR图像和参考HDR图像，依次执行亮度校正和色度校正（均通过闭合解一次性完成，无需迭代），然后在校正后的图像对上计算所需的质量指标。整个校正过程无需训练、无需GPU，计算开销极低，可轻松集成到任何SI-HDR评估流程中。

需要强调的是，该协议仅用于**评估阶段**，不改变SI-HDR方法本身的训练或推理过程。它是一种评估预处理手段，旨在消除CRF反演误差对质量指标的污染，使评估结果更真实地反映方法在饱和区域重建上的能力。

![[assets/figures/papers/paper_list_l4_https_www_cl_cam_ac_uk_research_rainbow_projects_sihdr_benchmark/figures/001_Figure_1.jpg]]
*Figure 1: Existing protocols for evaluating single-image HDR reconstruction methods directly compare the reconstructed HDR images with the reference, as depicted by the blue shaded rectangle. This is unreliable due to large tone and color differences between the reference and reconstructed HDR images. We demonstrate that the accuracy of metrics can be much improved if we correct for camera-response-curve inversion errors before computing image quality using existing full-reference metrics as shown in the green shaded rectangle. Still, the metrics can detect only very large image differences in this task and conducting a controlled experiment is the recommended option*

## 实验与关键发现

### 主观实验：多数SI-HDR方法并未真正提升视觉质量

论文构建了一个包含27张多样化HDR场景的主观评估数据集（Figure 2），涵盖人像、自然、城市、室内外、昼夜等场景，并通过成对比较实验收集了14名参与者的偏好数据。实验采用ASAP主动采样策略，确保每个条件至少比较14次，结果以JOD（Just-Objectionable-Difference）单位报告，基线为未处理的SDR输入图像（JOD=0）。

![[assets/figures/papers/paper_list_l4_https_www_cl_cam_ac_uk_research_rainbow_projects_sihdr_benchmark/figures/002_Figure_2.jpg]]
*Figure 2: The subset of HDR images from SI-HDR dataset used for the subjective evaluation, tone mapped with a global operator [Mantiuk et al. 2008] for visualization. We selected a wide variety of content covering nature, portraits, cities, indoor and outdoor, dalight and night scenes*

**核心发现**（Figure 3）：在六种被评估的SI-HDR方法中，仅**SingleHDR**（Liu et al., CVPR 2020）和**Mask-HDR**（Santos et al., ACM Trans. Graph. 2020）的平均JOD值大于0，即主观上优于原始SDR图像。其余四种方法——**DrTMO**（Endo et al., 2017）、**HDR-CNN**（Eilertsen et al., 2017）、**ExpandNet**（Marnerides et al., 2018）和**HDR-GAN**（Lee et al., ECCV 2018）——的平均JOD均为负值，意味着它们产生的HDR图像在视觉上反而不如未处理的SDR输入。从质量分布来看（Figure 3右），即使表现最好的方法，也仅在约40-50%的图像上产生了可感知的改进，而在相当比例的图像上质量持平甚至退化。这一结果直接挑战了此前仅依赖客观指标（如PSNR、SSIM）报告SI-HDR方法“显著提升”的论文结论。

### 客观指标与主观评价的相关性：CRF校正是关键瓶颈

论文系统评估了包括PU21-PSNR、HDR-VDP-2/3、FovVideoVDP、PU21-VSI、PU21-SSIM、PU21-NIMA、PU21-PIQE等在内的十余种全参考和无参考质量指标（Table 1），分别在**直接比较**和**CRF校正后比较**两种条件下计算其与主观JOD分数的Spearman秩相关系数。

![[assets/figures/papers/paper_list_l4_https_www_cl_cam_ac_uk_research_rainbow_projects_sihdr_benchmark/figures/004_Table_1.jpg]]
*Table 1: List of quality metrics used in our evaluation*

**直接比较的失效**：在不进行CRF校正的情况下，几乎所有全参考指标与主观评价的相关性均低于0.64（Figure 5a）。这一低相关性验证了论文的核心诊断——CRF反演误差导致的色调和颜色偏移淹没了真实的HDR信息重建失真，使得客观指标无法有效区分方法优劣。

**CRF校正的效果**（Figure 5b）：引入全局多项式CRF校正（包括PQ空间亮度三阶多项式映射和u'v'色度空间三阶多项式映射）后，全参考指标的相关性得到显著提升：
- **PU21-PSNR**的Spearman ρ从0.62跃升至**0.79**，提升幅度达0.17；
- **PU21-VSI**达到**0.78**，HDR-VDP-3达到**0.74**；
- 最佳期望相关性（unbiased mean correlation）约为**0.87**，表明经过CRF校正后，这些指标已接近主观实验本身的统计上限。

**无参考指标的意外表现**：值得注意的是，无参考指标**PU21-PIQE**在不进行任何CRF校正的情况下即达到**0.83**的相关性（Figure 5a），优于所有全参考指标在直接比较下的表现，甚至与校正后的最佳全参考指标持平。论文推测这是因为PU21-PIQE不依赖于与参考图像的逐像素比较，因而天然免疫于CRF反演误差的干扰。

**不推荐使用的指标**：PU21-SSIM和PU21-NIMA在CRF校正后相关性仍然较低（<0.5），论文明确建议在SI-HDR评估中避免使用这些指标。

### 指标预测误差与最小可区分差异：3.5 dB的可靠性门槛

尽管CRF校正大幅提升了指标相关性，论文进一步揭示了仅依赖客观指标进行方法比较的根本性局限。通过对27张主观实验图像的bootstrap重采样，论文估计了四种代表性指标（PU21-PSNR、PU21-VSI、HDR-VDP-3、FovVideoVDP）的**预测误差分布**（Figure 7）。

![[assets/figures/papers/paper_list_l4_https_www_cl_cam_ac_uk_research_rainbow_projects_sihdr_benchmark/figures/008_Figure_7.jpg]]
*Figure 7: Estimated prediction error for 4 selected metrics. Similar to Figure 5, the distributions were obtained by bootstrapping the experiment results over the subset of 27 images. The improvement in quality metric values reported in many papers falls below the expected accuracy of each metric*

**关键定量结论**：要确信一个方法的PU21-PSNR高于另一个方法意味着其主观质量确实更好（显著性水平α=0.05），两者的PU21-PSNR差异至少需要达到**3.5 dB**。这意味着许多现有论文中报告的1-2 dB的PSNR提升在统计上并不可靠——这些小幅改进很可能落在指标的预测误差范围内，无法真实反映主观质量的差异。

Figure 7的累积分布曲线直观地展示了这一困境：大量论文声称的改进幅度（通常<2 dB）远低于各指标的预期精度。即使使用最佳指标组合，SI-HDR领域的客观评估仍面临“信噪比”不足的问题。

### 全验证集上的方法排名与置信区间

论文在包含183张图像的全验证集上计算了各方法的PU21-PSNR排名分布（Figure 6），并通过bootstrap获得了95%置信区间。结果显示：
- 方法之间的排名存在大量重叠区间，仅少数方法对（如最优与最差方法之间）能实现统计显著的区分；
- 红色误差条标注的“最小可测量增量”（minimum measurable increment）进一步表明，当前指标的区分能力远不足以可靠地排列所有方法的优劣顺序。

![[assets/figures/papers/paper_list_l4_https_www_cl_cam_ac_uk_research_rainbow_projects_sihdr_benchmark/figures/007_Figure_6.jpg]]
*Figure 6: Ranking bootstrapped distributions for SI-HDR methods on the validation dataset. For each distribution, small dashes denote 95% confidence intervals, while the red errors bars show the minimum measurable increment in quality for selected metrics (described in Section 7.4)*

### 定性分析：饱和区域重建仍是核心难点

Figure 4展示了不同方法在典型场景下的重建效果对比。在包含大面积饱和区域的场景（如高光、光源）中，**ExpandNet**、**HDR-CNN**和**Mask-HDR**能产生中等程度的改进，而**DrTMO**和**HDR-GAN**则引入了明显的伪影（如颜色偏移、光晕）。即使是表现最好的SingleHDR，在极端高光区域仍可能产生不自然的纹理或色调。这些定性观察与主观JOD分数的分布一致——SI-HDR方法的核心挑战在于饱和区域的信息重建，而CRF反演误差的干扰使得这一挑战在传统评估中被掩盖。

### 实验的适用边界与公平性说明

**方法未重新训练**：所有被评估的SI-HDR方法均使用作者发布的预训练模型，未在统一数据集上重新训练。这意味着某些方法可能因训练数据分布与新测试集不匹配而处于不利地位，结果反映的是“开箱即用”的性能而非最优性能。

**CRF校正的局限**：所提出的CRF校正为全局颜色映射，无法完全补偿局部的或非全局的CRF反演误差。在存在空间变化的色调偏移或复杂光照的场景中，校正后的图像仍可能与参考存在系统性差异，进而影响全参考指标的准确性。

**显示条件依赖性**：主观实验和部分显示相关指标（如HDR-VDP系列）基于特定的HDR显示设备（峰值亮度约1000 cd/m²）和观看条件（77 ppd）。在不同显示设备或观看距离下，绝对数值可能发生变化，但论文的方法论框架和核心结论（CRF校正的必要性、3.5 dB门槛）具有较强的通用性。

**数据集规模**：主观实验仅覆盖27张图像，虽然内容多样性经过精心设计，但可能未能穷尽所有极端场景（如极低光、极高动态范围场景）。全验证集（183张图像）的客观评估部分弥补了这一不足。

![[assets/figures/papers/paper_list_l4_https_www_cl_cam_ac_uk_research_rainbow_projects_sihdr_benchmark/figures/003_Figure_3.jpg]]
*Figure 3: Preference of the SI-HDR method results. Left: The bars indicate the preference in JOD units, relative to the source SDR image. Negative values indicate that on average the method produced less preferable result than the nonprocessed source image. Right: The bars indicate the percentage of images in which the method produced better, same or worse image than the input SDR image*

## 定位与知识库关联

本文并非提出一种新的单图像HDR（SI-HDR）重建方法，而是对SI-HDR评估协议的**元评估与修正**。其核心贡献在于揭示并缓解了一个被领域长期忽视的评估陷阱：相机响应函数（CRF）反演误差主导了全参考质量指标的输出，使得指标无法真正衡量HDR信息重建的质量。因此，本文在知识库中的定位是**SI-HDR评估基准与协议设计**，而非重建算法本身。

### 改变的Slot：评估预处理步骤

相对现有SI-HDR评估实践，本文唯一改变的slot是**全参考质量指标计算前的预处理步骤**。

- **Baseline（现有协议）**：将SI-HDR方法输出的重建HDR图像与参考HDR图像直接比较，或仅做简单线性缩放/对数映射后计算质量指标。该做法隐含假设重建图像与参考图像在色调和颜色上已对齐，差异仅来自HDR信息恢复的优劣。
- **Proposed（本文协议）**：在计算任何全参考质量指标之前，对重建HDR图像施加全局多项式CRF校正——在PQ编码亮度空间拟合三阶多项式（Eq. 3），在u'v'色度空间拟合带通道交互的三阶多项式（Eq. 4），并通过Tikhonov正则化闭合解（Eq. 6）稳定求解映射系数。校正后，指标计算聚焦于饱和区域等真正与HDR重建相关的失真。

这一slot的修改揭示了现有评估体系的根本缺陷：**CRF反演误差导致的色调/颜色偏移淹没了真实的HDR重建失真**。如图5所示，直接比较时绝大多数全参考指标与主观评价的Spearman相关性低于0.64，而CRF校正后PU21-PSNR的相关性从0.62跃升至0.79，PU21-VSI达到0.78。这表明，领域此前通过客观指标报告的方法改进，可能主要反映的是CRF反演精度的差异，而非HDR重建能力的提升。

### 知识库挂载点

本文挂载于以下知识库节点：

1. **SI-HDR重建方法评估**：作为基准评估协议，直接服务于六种代表性SI-HDR方法的公平比较，包括**DrTMO**（Endo et al., ACM TOG 2017）、**HDR-CNN**（Eilertsen et al., ACM TOG 2017）、**ExpandNet**（Marnerides et al., CGF 2018）、**HDR-GAN**（Lee et al., ECCV 2018）、**SingleHDR**（Liu et al., CVPR 2020）和**Mask-HDR**（Santos et al., ACM TOG 2020）。本文揭示，这些方法中仅SingleHDR和Mask-HDR平均而言比未处理的SDR输入更受偏好（JOD > 0），其余四种方法倾向于降低质量。

2. **HDR质量指标验证**：系统评估了包括PU21-PSNR、HDR-VDP-2/3、FovVideoVDP、PU21-VSI、PU21-PIQE等在内的多种全参考和无参考指标。推荐组合为PU21-PSNR（简洁且性能良好）、PU21-VSI和HDR-VDP-3（可能表现优异），以及PU21-PIQE（无需CRF校正即可达到ρ=0.83的无参考指标）。

3. **感知质量评估的统计可靠性**：本文引入bootstrap方法量化指标预测误差，发现即使最佳指标也需要至少**3.5 dB的PU21-PSNR差异**才能以α=0.05的置信度断言一个方法优于另一个（Figure 7）。这一发现对领域具有深远警示意义——许多已发表论文中报告的小幅指标提升（如1–2 dB）落在指标预期误差范围内，无法可靠支撑“方法改进”的结论。

### 适用边界与局限

1. **CRF校正的全局性假设**：校正映射为全局多项式，无法补偿局部或不一致的CRF反演误差。对于产生空间非均匀色调偏移的方法，校正效果有限。

2. **主观实验的规模约束**：仅27张图像和14名参与者，虽通过ASAP主动采样保证每个条件至少比较14次，但内容覆盖和统计效力仍有限。

3. **显示模型的依赖性**：结果基于特定HDR显示设备（77 ppd观看条件），可能影响依赖显示模型的指标（如HDR-VDP系列）的绝对数值。

4. **方法未重新训练**：所有SI-HDR方法使用作者发布的预训练模型，在未见过的数据集上评估。训练数据分布差异可能使某些方法处于不利地位，结果不完全反映其最优性能。

5. **指标预测误差的下限**：即使CRF校正后，指标预测误差仍较大（PU21-PSNR需3.5 dB差异才能可靠区分方法）。这意味着**仅依赖客观指标进行SI-HDR方法比较本质上是不可靠的**，控制的主观实验仍是推荐选项。

### 后续启发与开放问题

1. **评估协议的推广**：本文的CRF校正框架是否适用于其他逆问题（如超分辨率、去噪、去模糊）的公平比较？这些任务中，颜色/色调偏移同样是常见的混淆变量。

2. **指标设计的改进方向**：PU21-PIQE作为无参考指标，无需CRF校正即可达到0.83的相关性，暗示设计对CRF反演误差鲁棒的指标是可行的。如何将这种鲁棒性融入全参考指标设计，是一个有价值的开放问题。

3. **统计报告规范的建立**：本文呼吁领域采用更严格的统计报告规范——不仅报告指标均值，还应报告置信区间或最小可区分差异，以避免将噪声误读为改进。

4. **SI-HDR方法的改进方向**：主观结果显示多数SI-HDR方法反而降低质量，表明领域需要从追求指标数字转向关注饱和区域重建的真实感和视觉偏好，可能通过对抗训练或更强的感知损失来实现。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Comparison_of_Single_image_HDR_Reconstruction_Methods_The_Caveats_of_Quality_Assessment.pdf]]