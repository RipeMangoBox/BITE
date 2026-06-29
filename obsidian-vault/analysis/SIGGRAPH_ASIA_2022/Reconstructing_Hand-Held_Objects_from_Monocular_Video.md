---
title: Reconstructing Hand-Held Objects from Monocular Video
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Reconstructing_Hand_Held_Objects_from_Monocular_Video.pdf
project_link: null
code_link: null
aliases:
- HHHOR
- RHHOFMV
tags:
- SIGGRAPH_ASIA_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 采用隐式神经表面表示（SDF）结合可微分体渲染，并在优化过程中同时精炼相机姿态（pose refinement）、补偿手物微小相对运动（deformation field）、通过物体掩码引导采样（semantics-guided sampling），使网络聚焦物体区域。
primary_logic: 手部运动自然地提供多视角，利用手部姿态跟踪器可靠估计物体运动，从而将手持物体重建转化为多视角几何重建问题，无需任何物体先验。
claims:
- 本方法在HOD数据集上取得平均Chamfer Distance 0.249，远低于NeuS (3.391) 等基线方法。
- 消融实验证明相机优化、形变场和语义引导采样三个模块各自带来显著的几何改善，最终PSNR从vanilla的18.10提升至27.27。
- 手参数共享策略使手部跟踪在严重遮挡下保持鲁棒，并将1800帧的拟合时间从4600秒降至420秒。
- HOD dataset (Sculptures + Daily Objects) 上 Chamfer Distance (mean, lower is better) = 0.249
---

# Reconstructing Hand-Held Objects from Monocular Video

> [!tip] 核心洞察
> 手部运动自然地提供多视角，利用手部姿态跟踪器可靠估计物体运动，从而将手持物体重建转化为多视角几何重建问题，无需任何物体先验。

| 字段 | 内容 |
|------|------|
| 中文题名 | 从单目视频重建手持物体 |
| 英文题名 | Reconstructing Hand-Held Objects from Monocular Video |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://dihuangdh.github.io/hhor/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | HHOR (Hand-Held Object Reconstruction) |
| Dataset | HOD dataset |

> [!tip] 效果简介
> - HOD dataset (Sculptures + Daily Objects) 上，Chamfer Distance (mean, lower is better) 0.249 vs 3.391 (NeuS) / 3.163 (ObMan) / 6.802 (IHOI) (相对NeuS降低约92.7%)。

## 概要

从单目视频重建手持未知物体面临手物独立运动、剧烈遮挡与低纹理等挑战，传统多视角几何方法在此场景下失效。本文提出**HHOR**，核心思想是将手部运动视为天然的多视角来源：通过手部姿态跟踪器可靠估计相机运动，将手持物体重建转化为可微分隐式神经表面重建问题，无需任何物体形状先验。方法引入三项关键改进——相机姿态在线精炼、补偿手物微小相对运动的可学习形变场，以及基于语义掩码的自适应采样策略——使网络聚焦物体区域并消除几何伪影。在自建HOD数据集上，HHOR取得平均Chamfer Distance **0.249**，相较NeuS（3.391）降低约92.7%；消融实验证实三个模块各自贡献显著，PSNR从18.10提升至27.27。该方法定位为“利用手部跟踪驱动多视角优化”的通用手持物体重建框架，适用于固定相机、单一抓握姿态下的无先验重建场景。

## 核心方法与创新机理

### 问题瓶颈与核心思想

从单目视频重建手持物体的根本困难在于：传统多视角重建（SfM/MVS）假设场景刚性且依赖纹理，而手持场景中存在**手与物体的独立运动**、**剧烈遮挡**以及物体常见的**低纹理特性**，导致标准方法完全失效。学习型方法（如ObMan、GF、IHOI）则依赖物体形状先验，无法泛化到未见过的物体类别。

本文的核心洞察在于：**手部运动天然地提供了物体的多视角观测**，且手部姿态跟踪器可以可靠地估计手部运动，从而将手持物体重建转化为一个多视角几何重建问题。基于此，整个方法无需任何物体形状先验知识，仅利用单目RGB视频即可重建任意未知物体。

### 方法框架总览

整个流水线分为两个阶段（Figure 2）：**手部跟踪（Hand Tracking）** 和**稠密重建（Dense Reconstruction）**。第一阶段通过MANO手部模型拟合恢复手部姿态和相机运动，为第二阶段提供初始相机姿态；第二阶段采用基于隐式神经表面表示（SDF）的可微分体渲染框架，并在优化过程中引入三个关键模块——相机姿态精炼、形变场和语义引导采样——以克服手持场景的特殊挑战。

![[assets/figures/papers/paper_list_l81_https_dihuangdh_github_io_hhor/figures/002_Figure_2.jpg]]
*Figure 2: The pipelineofourapproach,whichconsistsoftwo stages.Handtracking:byminimizingthereprojectionerrorofhand keypointsdetectedyaleareddetectorthe3Dhandposeandthecameramotionrelativetoitarerecovered.Densereconstructionan implicitneuralrepresentation-basedmethodisemployedtoreconstructtheSDFandcolorfeldsoftehandndbject.Treaditional modulesareproposed:theposeadjustmenttocompensateforimprecisehandposetracking,thedeformatiofeldtomodelterelative motion between the hand and object,and the semantics-guided sampling to improve object reconstruction quality*

### 第一阶段：手部跟踪与相机运动恢复

手部跟踪的目标是从视频帧中恢复MANO手部模型参数序列 $\mathbf{M} = \{\mathbf{M}_t\}_{t=1}^{N_T}$，其中每个 $\mathbf{M}_t = \{\theta_t, \beta_t, \mathbf{R}_t, \mathbf{T}_t\}$ 包含手部姿态 $\theta_t$、形状 $\beta_t$、全局旋转 $\mathbf{R}_t$ 和平移 $\mathbf{T}_t$。优化目标为最小化以下能量函数：

$$\mathbf{M} = \operatorname*{min}_{\mathbf{M}} (E_{2D} + \omega_1 E_t + \omega_2 E_{reg}) \quad (1)$$

其中 $E_{2D}$ 为2D重投影误差，度量投影的3D手部关键点与检测的2D关节点之间的差异：

$$E_{2D} = \sum_t || \pi(J(\mathbf{M}_t)) - J_t ||_2^2 \quad (2)$$

$E_t$ 为时间平滑项，$E_{reg}$ 为姿态和形状的正则化项，权重 $\omega_1=10^{-4}$、$\omega_2=5\times10^{-4}$。

**手参数共享策略**是此阶段的关键创新。由于手物遮挡严重，逐帧独立跟踪极易失败。本文提出在整个视频序列上**共享手部姿态和形状参数**（$\theta_1=\theta_2=...=\theta_t$，$\beta_1=\beta_2=...=\beta_t$），仅允许全局旋转和平移逐帧变化。这一设计利用了“同一视频中手部姿态和形状不变”的先验，将优化变量从每帧独立参数大幅缩减，不仅使跟踪在严重遮挡下保持鲁棒（Figure 7），还将1800帧的拟合时间从4600秒降至420秒（Appendix C）。恢复的相机运动 $\{\mathbf{R}_t, \mathbf{T}_t\}$ 直接作为第二阶段稠密重建的初始相机姿态。

### 第二阶段：基于隐式SDF的稠密重建

#### 基础表示与可微分渲染

稠密重建采用隐式神经表面表示。MLP网络 $F$ 以空间位置 $\mathbf{p}$ 和视线方向 $\mathbf{d}$ 为输入，预测SDF值 $s$ 和颜色 $c$：

$$[ s ( {\mathbf{p}} ) , c ( {\mathbf{p}} , {\mathbf{d}} ) ] = F ( {\mathbf{p}} , {\mathbf{d}} ) \quad (5)$$

为从SDF进行可微分渲染，本文沿用NeuS（Wang et al. 2021a）的技术。沿相机光线 $\mathbf{p}(z) = \mathbf{o} + z\mathbf{d}$ 累积颜色和密度得到像素颜色：

$$\hat{C} = \int_{z_n}^{z_f} \omega(z) c(\mathbf{p}(z), \mathbf{d}) dz \quad (6)$$

其中权重 $\omega(z)$ 由体渲染透射率决定。关键创新在于从SDF推导**无偏且遮挡感知的密度函数** $\rho(z)$：

$$\rho(z) = \operatorname*{max}{\biggl(}{\frac{-{\frac{d\Phi_h}{dz}}(s(\mathbf{p}(z)))}{\Phi_h(s(\mathbf{p}(z)))}}, 0{\biggr)} \quad (8)$$

其中 $\Phi_h$ 为以 $h$ 为参数的标准Logistic密度分布的累积分布函数。该密度函数确保渲染权重在表面附近达到峰值，且对遮挡关系建模准确，是高质量几何重建的基础。

#### 三个关键创新模块（Changed Slots）

在基础NeuS框架之上，本文引入三个针对性模块以解决手持场景的特殊问题：

**模块一：相机姿态精炼（Camera Pose Refinement, Section 4.2.2）**

手部跟踪提供的相机姿态存在误差，直接使用会导致重建表面出现尖锐伪影。本文将相机姿态作为可优化变量，与SDF网络 $F$ 联合优化。具体而言，每帧的6DoF姿态 $\{\mathbf{R}_t, \mathbf{T}_t\}$ 在训练过程中通过梯度下降微调，使得渲染图像与观测图像在颜色和掩码上更一致。该模块消除了由姿态不准确导致的几何畸变，是后续模块发挥作用的前提。

**模块二：形变场（Deformation Field, Section 4.2.3）**

手持过程中手与物体之间存在微小相对运动（如手指滑动、物体轻微晃动），破坏刚性假设。本文引入一个可学习的形变场 $W: \mathbb{R}^3 \to \mathbb{R}^3$，将观测空间中的采样点映射到规范空间：

$$\mathbf{p}_{\text{canonical}} = \mathbf{p} + W(\mathbf{p})$$

网络 $F$ 在规范空间中查询SDF和颜色。形变场由一个小型MLP实现，并通过正则化项 $L_d$ 约束形变幅度，防止过度扭曲。该模块有效去除了因相对运动产生的不规则锐边。

**模块三：语义引导采样（Semantics-guided Sampling, Section 4.2.4）**

手持场景中，物体区域通常只占图像的一小部分，均匀采样光线会导致网络将大量容量浪费在背景和手部区域。本文利用手部分割和前景掩码生成语义引导的采样权重：对物体区域的光线赋予更高采样概率。同时，网络额外输出语义logits $l(\mathbf{p}, \mathbf{d})$，通过体渲染得到每像素语义logits $\hat{L}$：

$$\hat{L} = \int_{z_n}^{z_f} \omega(z) l(\mathbf{p}(z), \mathbf{d}) dz$$

并用检测的语义掩码监督（损失项 $L_l$）。该模块使网络聚焦于物体区域，显著提升物体重建细节。

#### 训练损失与后处理

总损失函数联合优化所有模块：

$$L = L_c + \lambda_m L_m + \lambda_e L_e + \lambda_l L_l + \lambda_d L_d$$

其中 $L_c$ 为颜色重建损失，$L_m$ 为掩码损失，$L_e$ 为Eikonal正则化（强制SDF梯度范数为1），$L_l$ 为语义logits损失，$L_d$ 为形变正则化。训练完成后，通过Marching Cubes提取网格，并使用**Poisson Reconstruction进行后处理**（Section 4.2.6），填补手部遮挡造成的空洞。

### 模块间因果关系

三个模块之间存在清晰的因果链：**相机姿态精炼**是基础，消除系统性姿态偏差；**形变场**在此基础上补偿残余的非刚性运动，进一步规整几何；**语义引导采样**则在前两者保证几何合理性的前提下，将网络容量集中于物体区域，大幅提升细节恢复。消融实验（Table 5）量化验证了这一递进关系：vanilla NeuS的PSNR为18.10，加入相机优化后提升至19.69，加入形变场后提升至20.50，最终加入语义引导采样后跃升至27.27。

![[assets/figures/papers/paper_list_l81_https_dihuangdh_github_io_hhor/figures/008_Figure_7.jpg]]
*Figure 7: Effectiveness of parameters sharing during hand tracking.We compare our hand tracking system with and without sharing hand pose (0)and shape (β) parameters.Without sharing hand parameters, the hand tracking module easily tracks wrong hand poses due to heavy hand-object occlusions.In contrast, by sharing hand parameters across the entire video,the tracking module is able to get the correct hand poses even in extreme cases*

![[assets/figures/papers/paper_list_l81_https_dihuangdh_github_io_hhor/figures/009_Figure_8.jpg]]
*Figure 8: Experiments of different moving speeds.We do experiments to validate the robustness of our method at different grasping motion speeds. Our method is able to generate highquality 3D geometry for the Slow and Normal,and only cause small artifacts for the Fast.The‘CD'refers to the Chamfer Distance of object reconstruction*

## 实验与关键发现

### 主定量结果

本方法在自建HOD数据集上进行了系统评估。HOD数据集包含5个无纹理雕塑（Sculptures）和多种日常物体（Daily Objects），覆盖复杂几何细节与不同纹理材质（Figure 6）。评估指标采用Chamfer Distance（CD，越低越好），在Sculptures和Daily Objects两个子集上分别统计均值。

**Table 1** 展示了核心定量对比。本方法（HHOR）在整体平均CD上达到 **0.249**，显著优于所有基线方法：
- 相比基于隐式SDF的多视图重建方法 **NeuS**（CD=3.391），CD降低约 **92.7%**。NeuS虽使用相同的视频帧和相机姿态作为输入，但因缺乏对相机姿态的精炼和手物相对运动的建模，产生严重尖锐伪影和错误形状。
- 相比单视图学习方法 **ObMan**（CD=3.163），本方法CD降低约92.1%。ObMan依赖物体形状先验，无法泛化到未见物体类别。
- 相比单视图手物联合重建方法 **IHOI**（CD=6.802），本方法优势更为显著。IHOI以参考帧为输入，同样受限于训练类别先验。
- 单视图方法 **GF** 在HOD数据集上完全失败（CD=68.682），进一步验证了无先验知识下多视图信息的关键作用。

需要指出，所有学习型基线方法在训练阶段均未见过HOD数据集的物体类别，保证了比较的公平性。

### 与静态物体捕捉的对比

一个关键问题是：手持动态捕捉的重建质量能否媲美传统静态物体扫描？**Figure 4** 和 **Table 4** 给出了答案。将本方法的重建结果与在桌面上静态放置物体拍摄视频后使用COLMAP和NeuS重建的结果进行对比：
- 本方法的重建质量**高于**静态捕捉下的COLMAP（传统MVS流程在低纹理物体上难以建立可靠匹配）。
- 但本方法**无法恢复**静态捕捉下NeuS所能重建的精细细节。这一定量差距揭示了手持场景中手部遮挡和残余运动估计误差对重建精度的固有限制。

![[assets/figures/papers/paper_list_l81_https_dihuangdh_github_io_hhor/figures/004_Figure_4.jpg]]
*Figure 4: Comparison with static object capture.Note that the inputs to COLMAP and NeuS are videos of static object capture by putting the object on a table,while our inputs are videos of handheld object capture by moving the object in front of the camera*

此外，**Figure 10** 展示了手持捕捉的独特优势：对于无法直立放置的物体或底面严重遮挡的物体，静态扫描难以获取完整几何，而手持操作自然暴露多视角，本方法能够重建出更完整的物体表面。

### 消融实验：各模块的因果贡献

消融实验从vanilla NeuS基线出发，逐步叠加三个核心模块，通过物体区域的PSNR定量衡量重建质量（**Table 5**），并通过可视化展示几何改善（**Figure 5**）：

![[assets/figures/papers/paper_list_l81_https_dihuangdh_github_io_hhor/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative results of ablation study.vanilla indicates the mesh reconstructed with original NeuS,+camera indicates the camera refinement introduced in Section 4.2.2,+deformation indicates the deformation field introduced in Section 4.2.3,and +guiding indicates the semantics-guided sampling introduced in Section 4.2.4*

1. **Vanilla NeuS（PSNR=18.10）**：直接使用手部跟踪估计的相机姿态进行SDF重建。由于手部跟踪存在累积误差，重建表面出现严重尖锐伪影和几何失真。

2. **+相机姿态精炼（PSNR=19.69）**：在与SDF网络联合优化过程中同时精炼6DoF相机姿态。该模块消除了手部跟踪引入的姿态漂移，PSNR提升1.59，重建表面尖锐伪影明显减少，但仍有不规则锐边残留。

3. **+形变场（PSNR=20.50）**：添加可学习形变场 $W$ 补偿手物微小相对运动。该模块进一步去除了不规则锐边，PSNR再提升0.81，验证了即使“刚性抓握”假设下仍存在不可忽略的微小相对运动。

4. **+语义引导采样（PSNR=27.27）**：基于物体掩码的自适应采样策略使网络聚焦物体区域光线。该模块带来**最大幅度的PSNR提升（+6.77）**，物体细节显著丰富，纹理恢复更加清晰。这表明在手持场景中，手部区域占据大量像素，均匀采样会严重稀释物体区域的优化信号，语义引导采样是提升物体重建质量的关键瓶颈突破点。

### 手部跟踪的鲁棒性与效率

手参数共享策略是手部跟踪阶段的关键设计。**Figure 7** 的消融对比显示：不共享手部姿态参数 $\theta$ 和形状参数 $\beta$ 时，在严重手物遮挡下跟踪器容易陷入错误姿态；而共享参数后，即使极端遮挡情况仍能恢复正确手部姿态。

效率方面，参数共享将1800帧视频的MANO拟合时间从 **4600秒降至420秒**（约**10.9倍加速**），使整个流程在计算上更加可行。

### 鲁棒性边界与失败模式

**运动速度鲁棒性（Figure 8）**：在慢速（Slow）和正常（Normal）抓握运动速度下，本方法均能生成高质量3D几何；快速运动（Fast）下仅产生轻微伪影，CD值仍保持较低水平。这表明方法对运动速度具有一定容忍度，但极端快速运动会导致运动模糊和跟踪失败。

**抓握手势影响（Figure 9）**：当抓握手势仅覆盖物体小部分区域时，联合重建和物体单独重建均保持高保真度；当手势覆盖物体大面积区域时，联合重建质量依然较高，但后处理Poisson Reconstruction难以填充大面积手部遮挡留下的空洞，导致最终物体网格出现偏差。这是方法的一个固有局限——依赖后处理填补遮挡区域，而非从多视角观测中直接恢复。

**相机姿态初始化必要性（Figure 11）**：若无手部跟踪提供的相机姿态初始化，直接从随机姿态开始联合优化，重建的法线图质量严重下降。这表明手部跟踪为先的初始化策略对于优化收敛至关重要。

**其他限制**：方法假设固定相机和单一抓握姿态，无法处理相机运动或多段抓握序列拼接；对无纹理或薄结构物体的重建仍具挑战性；整体优化流程计算代价较高，难以实时应用。

![[assets/figures/papers/paper_list_l81_https_dihuangdh_github_io_hhor/figures/005_Table_1.jpg]]
*Table 1: Quantitative results of object reconstruction. The metric is the Chamfer Distance*

## 定位与知识库关联

本文的核心定位是**将手持物体重建从“需要物体先验的单视图/多视图重建”重新定义为“利用手部运动作为多视角来源的无先验神经隐式重建”**。这一转变改变了传统重建管线中的三个关键 slot，并在知识库中建立了新的挂载点。

**改变的 slot 与本质差异**

相对于已有方法，本工作改变了以下三个 slot：

1. **相机姿态获取 slot：从“已知/固定姿态”变为“与几何外观联合优化”**。传统多视图重建方法（如 **NeuS** (Wang et al., NeurIPS 2021)、COLMAP）假设相机姿态已精确标定或通过 SfM 恢复，但在手持场景中手物独立运动破坏了这一假设。本方法将相机姿态作为可优化变量，与 SDF 网络同时精炼（Section 4.2.2），使重建能容忍手部跟踪的初始误差。消融实验中，仅加入相机优化就将 PSNR 从 vanilla 的 18.10 提升至 19.69（Table 5），验证了这一 slot 改变的必要性。

2. **手物关系建模 slot：从“刚性连接”变为“可学习形变场补偿微小相对运动”**。基于学习的方法（如 **IHOI** (Ye et al., 2022)、**ObMan** (Hasson et al., 2019)、**GF** (Karunratanakul et al., 2020)）或隐式假设手物刚性连接，或需要物体形状先验才能推理。本方法引入形变场 $W$（Section 4.2.3），在不依赖先验的前提下建模手物间的微小相对运动，消除了刚性假设导致的尖锐伪影，PSNR 进一步提升至 20.50。这一 slot 的改动是连接“手部跟踪”与“多视图几何”的关键桥梁。

3. **采样策略 slot：从“均匀光线采样”变为“语义掩码引导的自适应采样”**。标准体渲染方法（如 NeuS）对图像光线均匀采样，在手持场景中大量采样点落在背景或手部区域，浪费计算资源且干扰物体重建。本方法基于语义掩码加权采样，使网络聚焦物体区域（Section 4.2.4），PSNR 显著跃升至 27.27，物体细节大幅改善。这是将“语义先验”（从手部分割获得）注入几何重建的轻量但高效的方式。

**知识库挂载点**

本工作在知识库中的挂载点位于**多视图几何重建**与**手物交互感知**的交叉地带：

- **挂载到神经隐式重建**：直接继承 NeuS 的可微分 SDF 渲染框架（SDF MLP $F$、体渲染公式、Eikonal 正则），但将其从“已知姿态的静态场景重建”拓展到“姿态未知的动态手持场景”。这一拓展的关键在于将相机姿态和形变场纳入优化循环，使神经隐式表示首次适用于非刚性手持配置。

- **挂载到手部姿态估计**：利用 MANO 模型和 2D 关键点检测器获得初始相机运动估计，但通过“手参数共享策略”（$\theta_1 = \theta_2 = ... = \theta_t$，$\beta_1 = \beta_2 = ... = \beta_t$）解决了严重遮挡下的跟踪鲁棒性问题，并将 1800 帧的拟合时间从 4600 秒压缩至 420 秒（Appendix C）。这为后续工作提供了“利用时序一致性增强手部跟踪”的参考范式。

- **挂载到语义引导的几何重建**：将手物分割掩码作为“免费”的语义先验，通过语义 logits 渲染和加权采样引导网络聚焦物体区域。这一思路可推广到其他“已知前景/背景分割”的重建任务，如人体-物体交互重建。

**适用边界与限制**

本方法的适用边界明确：**(1) 需要固定相机**，无法处理移动相机场景；**(2) 假设单一抓握姿态**，手物相对运动必须微小，形变场能力有限，无法处理大幅度滑动或换手操作；**(3) 依赖可靠的 2D 手部关键点检测和 MANO 拟合**，在极端遮挡或非标准手型下可能退化；**(4) 需要后处理（Poisson Reconstruction）填补手部遮挡造成的空洞**，可能引入偏差；**(5) 优化过程计算代价高**，难以实时应用。

**后续启发与知识库价值**

本工作为知识库贡献了以下可复用的洞察：

1. **“手部运动即多视角”范式**：证明了手部跟踪器可以替代传统 SfM 提供多视图几何所需的相机姿态，为无先验手持物体重建开辟了新路径。后续工作可探索更鲁棒的手部跟踪器或联合优化手物姿态。

2. **模块化设计中的因果链**：消融实验清晰展示了“相机优化 → 形变场 → 语义引导采样”的递进关系，每个模块解决一个特定失败模式（姿态误差、相对运动、采样效率），为后续方法提供了明确的改进方向。

3. **开放问题**：如何消除固定相机和单一抓握姿态的限制？如何在不依赖后处理的情况下处理大孔洞和薄结构？如何利用更高效的神经表示（如 Instant-NGP）实现实时重建？这些问题定义了该方向的后续研究议程。

**对比总结**

与需要物体先验的学习方法（ObMan、GF、IHOI）相比，本方法在 HOD 数据集上取得了 Chamfer Distance 0.249，相对 NeuS（3.391）降低约 92.7%，证明了无先验优化的可行性。与静态捕捉下的 COLMAP 和 NeuS 相比，本方法在手持场景下质量更高，但精细细节恢复仍弱于静态 NeuS（Figure 4），说明手物相对运动补偿仍有提升空间。本工作建立了“手部跟踪 + 神经隐式重建 + 联合优化”的基线框架，后续改进可沿上述开放问题展开。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Reconstructing_Hand_Held_Objects_from_Monocular_Video.pdf]]