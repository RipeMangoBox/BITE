---
title: "eRetinexGS: Retinex Modeling for Low-Light Scene Enhancement via Event Streams and 3D Gaussian Splatting"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/eRetinexGS_Retinex_Modeling_for_Low_Light_Scene_Enhancement_via_Event_Streams_and_3D_Gaussian_Splatting.pdf
project_link: "https://zju-bmi-lab.github.io/eRetinexGS-homepage/"
code_link: null
aliases:
- eRetinexGS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过自适应地结合事件的梯度信息（在暗区更可靠）和RGB的光度信息（在亮区更可靠），并利用事件的无触发区域暗示反射率平滑性先验，可同时抑制噪声并保留纹理，从而恢复高质量的正常光照辐射场。
primary_logic: 事件流与RGB帧在亮度量化上具有互补性：事件在暗区提供更精细的梯度，RGB在亮区提供更精确的色彩；同时，事件的无触发区域提供了反射率平滑性的几何先验，这使得Retinex分解在多视图中更加稳定和准确。
claims:
- 去除事件引导的反射率平滑损失和置信度融合后，合成数据集上的PSNR从23.45大幅下降至17.21
- eRetinexGS在合成数据集上取得了最佳PSNR、SSIM和LPIPS，显著优于现有图像增强、事件增强和3DGS方法
- 真实数据上的定性结果表明，事件和RGB的互补性有效恢复了暗区纹理和亮区色彩，避免了伪影和色彩失真
- Synthetic Low-Light Dataset (Input View) 上 PSNR / SSIM / LPIPS = 23.45 / 0.8312 / 0.0888
---

# eRetinexGS: Retinex Modeling for Low-Light Scene Enhancement via Event Streams and 3D Gaussian Splatting

> [!tip] 核心洞察
> 事件流与RGB帧在亮度量化上具有互补性：事件在暗区提供更精细的梯度，RGB在亮区提供更精确的色彩；同时，事件的无触发区域提供了反射率平滑性的几何先验，这使得Retinex分解在多视图中更加稳定和准确。

| 字段 | 内容 |
|------|------|
| 中文题名 | eRetinexGS：基于事件流与3D高斯泼溅的低光照场景增强Retinex建模 |
| 英文题名 | eRetinexGS: Retinex Modeling for Low-Light Scene Enhancement via Event Streams and 3D Gaussian Splatting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Yan_eRetinexGS_Retinex_Modeling_for_Low-Light_Scene_Enhancement_via_Event_Streams_CVPR_2026_paper.html) · [Project](https://zju-bmi-lab.github.io/eRetinexGS-homepage/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | eRetinexGS |
| Dataset | Synthetic Low-Light Dataset |

> [!tip] 效果简介
> - Synthetic Low-Light Dataset (Input View) 上，PSNR / SSIM / LPIPS 23.45 / 0.8312 / 0.0888 vs 次优方法 (LLNeRF等) (显著优于所有对比方法)。
> - Synthetic Low-Light Dataset (Novel View) 上，PSNR / SSIM / LPIPS 22.67 / 0.8152 / 0.1163 vs 次优方法 (显著优于)。

## 概述

极低光照条件下的多视图场景增强与重建面临一个根本瓶颈：RGB帧在暗区噪声严重、色彩与纹理信息近乎丢失，而事件相机虽具备高动态范围，其固有的传感器噪声与运动拖影同样使可靠信息提取变得困难——两种模态的恶化相互交织，阻碍了直接的跨模态互补。**eRetinexGS** 针对这一瓶颈，提出将事件流与低光照RGB帧通过3D高斯泼溅（3DGS）统一到Retinex分解框架中，核心思路是利用两种模态在亮度量化上的天然互补性——事件在暗区提供更精细的梯度结构，RGB在亮区提供更准确的色彩——同时将事件的“无触发区域”转化为反射率平滑性的几何先验，从而在多视图下实现稳定且准确的反射率-光照分解，最终恢复高质量的正常光照辐射场。

方法在场景表示层面进行了四个关键改造（详见方法谱系与知识库定位）：(1) 每个高斯显式分解为视角无关的反射率与视角相关的光照，通过alpha混合渲染R/L图后合成辐射；(2) 引入事件引导的掩膜总变分损失，在非事件区域强制反射率平滑，沿事件边缘保留不连续性；(3) 以恢复辐射的灰度为置信度图，自适应加权事件损失与图像损失，使暗区更信赖事件、亮区更信赖RGB；(4) 采用两个MLP分别学习事件与图像的退化映射，将含噪观测对齐到干净辐射场。

在合成数据集上，eRetinexGS在输入视图与新视图两个设定下均取得最优PSNR、SSIM和LPIPS（输入视图PSNR 23.45 dB），显著优于现有图像增强、事件增强及3DGS方法（Table 1）。消融实验表明，移除事件引导的反射率平滑损失和置信度融合后，PSNR从23.45大幅降至17.21（Table 2），验证了两条互补线索的决策性作用。真实数据上的定性结果进一步证实，事件与RGB的互补性有效恢复了暗区纹理和亮区色彩，避免了伪影与色彩失真。方法在渲染速度上可达83 FPS，训练约需1小时；主要局限包括COLMAP位姿不准时的失效风险、事件稀疏区域的边界模糊，以及对高光/非朗伯表面的Retinex假设偏差。

## 背景与动机

低光照条件下的场景增强与重建是计算机视觉中的一项核心挑战，广泛应用于夜间监控、自动驾驶和增强现实等领域。传统RGB相机在极暗环境下捕获的图像存在严重的噪声污染、色彩退化与纹理丢失，使得从单帧或多帧图像中恢复高质量的正常光照辐射场变得极为困难。

事件相机（event camera）作为一种新型的神经形态视觉传感器，具有微秒级时间分辨率和高动态范围（>120 dB），能够在极端光照变化下异步记录亮度变化的“事件流”。这一特性使其天然适合作为低光照场景的补充信息源。然而，事件相机仅提供稀疏的亮度变化信号，且自身也受到噪声和运动拖影的困扰——在低光照下，事件噪声与信号难以区分，直接将其与RGB帧进行简单融合往往导致色彩失真和细节丢失。

现有方法在面对这一问题时存在明显的缺口。**基于图像的低光照增强方法**（如**Retinexformer**, Cai et al., ICCV 2023）仅依赖单帧RGB信息，在暗区色彩信息近乎缺失时无法恢复可信的纹理；**基于NeRF的场景级增强方法**（如**LLNeRF**, Wang et al., ICCV 2023）虽然引入了多视图一致性，但其隐式神经辐射场缺乏对反射率与光照的显式建模，难以有效利用事件流的结构先验；**事件引导的视频增强方法**（如**Coherent Event Guided Low-light Video Enhancement**, Liang et al., ICCV 2023）则局限于2D时域处理，无法实现场景级的新视图合成。将事件与低光照帧直接送入标准**3DGS**（Kerbl et al., TOG 2023）同样不可行，因为3DGS仅建模颜色属性，无法刻画低光照下两种模态之间的退化关系与互补机制。

本文的核心动机源于一个关键观察：**事件流与RGB帧在亮度量化上具有天然的互补性**。如图1底部所示，事件相机在暗区提供比RGB更精细的梯度信息（Cue 2），而RGB在亮区提供更精确的色彩；同时，事件的无触发区域暗示了反射率平滑性的几何先验（Cue 1），这为在多视图下稳定地进行Retinex分解提供了独特线索。然而，要利用这两种互补线索，必须同时解决两个瓶颈：（1）如何将事件的结构先验嵌入到场景表示中，以约束反射率的分解；（2）如何自适应地融合事件与RGB的监督信号，使暗区更信赖事件、亮区更信赖图像。

本文提出**eRetinexGS**——一个基于3D高斯泼溅与Retinex理论的低光照场景增强框架。通过在3DGS中显式建模每个高斯的反射率与光照属性，并引入事件引导的反射率平滑损失与置信度引导的互补数据损失，eRetinexGS能够从多视角低光照帧与事件流中重建出细节丰富、色彩准确的正常光照辐射场，同时保持实时渲染能力（83 FPS）。

## 核心创新

eRetinexGS 的核心创新在于将 Retinex 分解显式嵌入 3DGS 场景表示，并利用事件流与低光照 RGB 帧的**双模态互补线索**来约束分解过程，从而在极低光照条件下恢复高质量的辐射场。相较于现有方法，其关键改动体现在四个维度：

### 1. 显式反射率-光照场景表示

标准 3DGS（Kerbl et al., TOG 2023）仅为每个高斯存储视角相关的颜色属性，而 eRetinexGS 将每个高斯显式分解为**视角无关的反射率 $r$** 和**视角相关的光照 $l$** 两个属性。通过 alpha 混合分别渲染反射率图 $R$ 和光照图 $L$，再以元素级乘积合成最终辐射：

$$R = \sum_{k \in \mathcal{N}} r_k \alpha_k \prod_{u=1}^{k-1} (1 - \alpha_u), \quad L = \sum_{k \in \mathcal{N}} l_k \alpha_k \prod_{u=1}^{k-1} (1 - \alpha_u)$$

$$I^r = R \odot L$$

这一设计将 Retinex 物理先验（场景反射率与光照可分离）从 2D 图像域迁移到 3D 场景表示中，使得多视图一致性可以天然地约束分解过程，而非依赖单帧估计的后处理融合。

### 2. 事件引导的反射率平滑先验

传统 Retinex 方法对反射率施加均匀平滑约束，容易模糊纹理边缘。eRetinexGS 利用事件流的高时间分辨率特性，从短时间切片事件中提取结构感知的平滑线索：**在事件未触发的区域强制反射率平滑，沿事件边缘保留不连续性**。具体通过事件掩膜 $M_e$ 加权的总变分损失实现：

$$\mathcal{L}_{\mathrm{tv}} = \frac{1}{H \times W} \sum_{\mathbf{u}} (1 - M_e(\mathbf{u})) \left\| \nabla R(\mathbf{u}) \right\|_1$$

这一设计的物理直觉在于：事件相机仅在亮度变化处触发，无事件区域意味着场景反射率在时序上稳定，因此应具有空间平滑性。消融实验表明，去除 $\mathcal{L}_{\mathrm{tv}}$ 后暗区细节显著丢失，PSNR 大幅下降（Tab. 2, Fig. 6(c)），验证了该先验对暗区纹理恢复的关键作用。

### 3. 置信度引导的自适应多模态融合

现有事件-图像融合方法通常采用固定加权或直接特征拼接，忽视了两种模态在不同亮度区域的**互补量化特性**：事件在暗区提供更精细的梯度信息，而 RGB 在亮区提供更准确的色彩（Fig. 3(b)）。eRetinexGS 以恢复辐射的灰度值 $I_t^{rg}$ 作为置信度代理，自适应加权事件损失 $\mathcal{L}_{ev}$ 和图像损失 $\mathcal{L}_{img}$：

$$\mathcal{L}_{\mathrm{data}} = (1 - \operatorname{sg}(I_t^{rg})) \odot \mathcal{L}_{ev} + \operatorname{sg}(I_t^{rg}) \odot \mathcal{L}_{img}$$

其中 $\operatorname{sg}(\cdot)$ 为停止梯度操作。这一机制使暗区更信赖事件的梯度监督，亮区更信赖 RGB 的色彩监督，避免了固定权重导致的暗区伪影或亮区色彩失真。消融实验证实，替换为固定权重后亮区色彩和暗区细节均出现退化（Fig. 6(c)）。

### 4. 双模态退化对齐

低光照条件下，RGB 图像受严重噪声和 ISP 非线性影响，事件流也存在噪声和时间量化误差。eRetinexGS 引入两个 MLP——**F-MLP** 和 **G-MLP**——分别学习事件和图像的退化映射，将含噪声的观测对齐到干净的辐射场：

$$\hat{I}^l = \mathcal{G}(I^r), \quad \hat{E} = \mathcal{F}(I^r)$$

这使得交叉模态监督信号在退化域中保持一致，而非错误地假设观测即为真值。去除退化对齐模块后，交叉模态损失变得不可靠，重建质量显著下降（Sec. 5.3, Fig. 7）。Fig. 7 在真实数据上可视化了两条退化映射曲线，展示了从干净辐射到低光照图像/事件信号的映射关系。

### 与 baseline 的本质差异

| 改动维度 | 现有方法 | eRetinexGS |
|---------|---------|------------|
| 场景表示 | 隐式 NeRF 或标准 3DGS 仅存颜色 | 每高斯显式存 $r$ 和 $l$，alpha 混合得 $R$、$L$ |
| 反射率约束 | 图像域均匀平滑假设 | 事件引导的掩膜 TV 损失，结构感知平滑 |
| 多模态融合 | 固定加权或特征拼接 | 辐射灰度置信度自适应加权 |
| 退化处理 | 假设观测无显著退化 | F/G MLP 分别建模事件和图像退化 |

这些改动共同构成了一个**自监督、场景级**的低光照增强框架：无需成对正常光照真值，而是通过多视图一致性和事件-图像互补线索联合优化场景表示。合成数据集上，eRetinexGS 在输入视图和新视图上分别取得 23.45/22.67 PSNR，显著优于 LLNeRF（Wang et al., ICCV 2023）、Retinexformer（Cai et al., ICCV 2023）及事件引导视频增强方法（Liang et al., ICCV 2023）等所有对比方法（Tab. 1）。

## 整体框架

eRetinexGS 构建了一条从多视角低光照 RGB 帧与事件流到正常光照新视图的端到端 pipeline，其核心是在 3D Gaussian Splatting（3DGS）框架内嵌入事件辅助的 Retinex 分解，并通过退化对齐与置信度融合实现跨模态互补。整体流程如 **Figure 2** 所示，可分为五个关键阶段。

![[assets/figures/papers/paper_list_l2477_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_eRetinexGS_Retinex/figures/002_Figure_2.jpg]]
*Figure 2: The pipeline of eRetinexGS. We propose a novel low-light scene enhancement method, named eRetinexGS, based on 3D Gaussian Splatting (3DGS) and Retinex theory[2, 55, 60], to reconstruct clear normal-light images {Iri } from multi-view captured lowlight frames{Ili} and event sequences E. In our approach, each Gaussian explicitly models reflectance and illumination, while event-guided reflectance smoothness and confidence-guided complementarity improve decomposition and multimodal supervision in low light*

**输入与位姿估计**  
系统输入为多视角低光照帧序列 $\{I^l\}$ 和对应的事件流 $E$。首先使用 COLMAP 从低光照帧中估计相机位姿，为后续多视图一致性提供几何基础。

**第一阶段：3DGS 几何与外观预热**  
采用标准 3DGS 对场景进行初步重建，获得粗糙的几何结构与外观先验。此阶段不涉及 Retinex 分解，仅为后续精细化提供初始高斯场。

**第二阶段：事件引导的 Retinex 分解与属性扩展**  
在预热后的高斯场上，每个高斯显式地存储两个新属性：视角无关的反射率 $r$ 和视角相关的光照 $l$。通过 alpha 混合分别渲染反射率图 $R$ 和光照图 $L$：

$$R = \sum_{k \in \mathcal{N}} r_k \alpha_k \prod_{u=1}^{k-1} (1 - \alpha_u), \quad L = \sum_{k \in \mathcal{N}} l_k \alpha_k \prod_{u=1}^{k-1} (1 - \alpha_u)$$

最终恢复的辐射场由两者逐元素乘积得到：$I^r = R \odot L$。这一显式分解使得反射率与光照可以分别接受来自事件和 RGB 的不同先验约束。

**事件引导的反射率平滑与置信度融合**  
系统引入两个互补线索来约束分解。第一，事件引导的掩膜总变分损失 $\mathcal{L}_{\mathrm{tv}}$ 利用事件的高时间分辨率：在事件未触发的区域强制反射率平滑，在事件边缘保留不连续性，从而抑制暗区噪声同时保持纹理。第二，置信度引导的数据损失 $\mathcal{L}_{\mathrm{data}}$ 以恢复辐射的灰度值 $I^{rg}_t$ 为置信度代理，自适应地加权事件损失 $\mathcal{L}_{ev}$ 和图像损失 $\mathcal{L}_{img}$——暗区更信赖事件梯度，亮区更信赖 RGB 光度。

**退化对齐模块**  
为弥合观测信号与渲染结果之间的退化鸿沟，系统引入两个轻量 MLP：$F$ 建模事件相机的亮度变化感知过程，$G$ 建模低光照图像的传感器噪声与 ISP 非线性。两者分别将渲染的干净辐射映射到观测空间，使得损失计算在物理上更可靠。

**联合优化与输出**  
总损失函数整合数据保真、亮度先验、灰色世界先验和事件引导平滑项：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{data} + \lambda_2 \mathcal{L}_{\mathrm{brightness}} + \lambda_3 \mathcal{L}_{\mathrm{gray}} + \lambda_4 \mathcal{L}_{\mathrm{tv}}$$

优化完成后，系统可从任意新视角渲染正常光照图像 $I^r$，实现场景级低光照增强与新视图合成。

**模块间的因果依赖**  
第一阶段预热为第二阶段提供几何初始化；Retinex 分解为反射率平滑损失和置信度融合提供操作对象；退化对齐 MLP 使跨模态损失计算具有物理意义；置信度融合则动态调节事件与 RGB 在优化中的主导权。消融实验证实，移除任一模块均会导致性能显著退化——例如去除事件引导平滑损失后，合成数据集 PSNR 从 23.45 骤降至约 17.21（**Table 2**, **Figure 6(c)**）。

### 补充图表

![[assets/figures/papers/paper_list_l2477_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_eRetinexGS_Retinex/figures/001_Figure_1.jpg]]
*Figure 1: Top: We enhance scene representation and synthesize normal-light novel views from low-light frames and event streams. (b) Frame-based methods [48] fail in regions lacking color information; (c) Directly applying events and low-light images to 3DGS [21] leads to color distortion and detail loss due to inaccurate modeling of their relationship under low-light conditions; (d) Our method aligns degraded images with noisy events, achieving color consistent and detail preserving reconstruction. Bottom: Cues for event–frame-based low-light enhancement. Cues1: event guided smoothness prior on reflectance in non-event regions; Cues2: complementary photometric cues, events provide reliable signals in...*

## 核心模块与公式推导

eRetinexGS 的核心思想是将 Retinex 分解嵌入 3D Gaussian Splatting 的可微渲染管线，并通过事件流提供的两种互补线索——反射率平滑性先验与光度置信度——来约束分解过程，同时引入退化对齐模块弥合观测与渲染之间的域差异。

### 场景表示与 Retinex 分解

方法在第一阶段使用标准 3DGS 进行预热，获得初步的场景几何与外观。第二阶段，每个高斯显式地存储两个属性：视角无关的反射率 $r$ 和视角相关的光照 $l$。通过 alpha 混合，在图像平面上渲染出反射率图 $R$ 和光照图 $L$：

$$
R = \sum_{k \in \mathcal{N}} r_k \alpha_k \prod_{u=1}^{k-1} (1 - \alpha_u), \quad
L = \sum_{k \in \mathcal{N}} l_k \alpha_k \prod_{u=1}^{k-1} (1 - \alpha_u)
\tag{2}
$$

最终恢复的正常光照辐射 $I^r$ 由两者逐元素乘积得到：

$$
I^r = R \odot L
\tag{3}
$$

这一显式分解使得后续的事件引导约束能够直接作用于反射率分量，而非整个辐射场。

### 事件引导的反射率平滑性

在极低光照下，RGB 图像的信噪比极低，难以可靠地推断反射率边界。事件相机的高时间分辨率提供了结构线索：事件触发区域对应亮度变化显著的边缘，而无事件区域则暗示反射率应保持平滑。基于此，设计事件引导的掩膜总变分损失 $\mathcal{L}_{\mathrm{tv}}$：

$$
\mathcal{L}_{\mathrm{tv}} = \frac{1}{H \times W} \sum_{\mathbf{u}} (1 - M_e(\mathbf{u})) \left\| \nabla R(\mathbf{u}) \right\|_1
\tag{4}
$$

其中 $M_e$ 为事件掩膜，在事件触发区域取 1，否则为 0。该损失仅在非事件区域惩罚反射率梯度，鼓励平滑；在事件边缘则保留不连续性，从而在抑制噪声的同时保护纹理结构。

### 置信度引导的互补融合

事件与 RGB 图像在亮度量化上具有天然互补性：事件在暗区提供更精细的梯度信息，而 RGB 在亮区提供更准确的色彩。为自适应地融合两种模态，以恢复辐射的灰度值 $I_t^{rg}$ 作为置信度代理，构建数据损失 $\mathcal{L}_{\mathrm{data}}$：

$$
\mathcal{L}_{\mathrm{data}} = (1 - \operatorname{sg}(I_t^{rg})) \odot \mathcal{L}_{ev} + \operatorname{sg}(I_t^{rg}) \odot \mathcal{L}_{img}
\tag{5}
$$

其中 $\operatorname{sg}$ 为停止梯度操作。当场景较暗（$I_t^{rg}$ 低）时，事件损失 $\mathcal{L}_{ev}$ 的权重增大；当场景较亮时，图像损失 $\mathcal{L}_{img}$ 的权重增大。这一机制使模型在暗区更信赖事件，在亮区更信赖 RGB。

### 退化对齐模块

低光照图像和事件流均存在显著的传感器退化，直接与干净辐射场对齐会产生系统性偏差。为此引入两个轻量 MLP：

- **F-MLP**：建模事件相机的退化过程，将渲染辐射 $I^r$ 映射到事件感知的亮度变化空间。
- **G-MLP**：建模低光照图像的退化过程，包括信号依赖噪声和 ISP 非线性：

$$
\hat{I}^l = \mathcal{G}(I^r)
\tag{7}
$$

图像损失 $\mathcal{L}_{img}$ 在退化后的渲染结果与真实低光照图像之间计算，采用 L1 与 D-SSIM 的组合：

$$
\mathcal{L}_{img} = \lambda_1 \mathcal{L}_1 (\mathcal{G}(I_t^r), I_t^l) + (1 - \lambda_1) \mathcal{L}_{\mathrm{D-SSIM}} (\mathcal{G}(I_t^r), I_t^l)
\tag{9}
$$

### 联合优化

总损失函数整合了数据保真、亮度先验、灰色世界假设和事件引导平滑性：

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{data} + \lambda_2 \mathcal{L}_{\mathrm{brightness}} + \lambda_3 \mathcal{L}_{\mathrm{gray}} + \lambda_4 \mathcal{L}_{\mathrm{tv}}
\tag{13}
$$

其中 $\lambda_1 = 0.8$，$\lambda_2 = 1.0$，$\lambda_3 = 0.1$，$\lambda_4 = 0.1$。亮度损失 $\mathcal{L}_{\mathrm{brightness}}$ 约束恢复辐射的整体亮度接近目标值，灰色世界损失 $\mathcal{L}_{\mathrm{gray}}$ 促进色彩平衡。

**瓶颈与机制总结**：核心瓶颈在于极低光照下两种模态同时恶化——RGB 噪声淹没纹理，事件噪声和拖影破坏结构。eRetinexGS 的因果调节路径是：事件梯度在暗区补偿 RGB 的纹理缺失（通过 $\mathcal{L}_{ev}$ 高权重），RGB 光度在亮区约束事件色彩（通过 $\mathcal{L}_{img}$ 高权重），同时事件的无触发区域为反射率提供几何平滑先验（通过 $\mathcal{L}_{\mathrm{tv}}$），三者协同使 Retinex 分解在多视图中稳定收敛。

### 补充图表

![[assets/figures/papers/paper_list_l2477_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_eRetinexGS_Retinex/figures/003_Figure_3.jpg]]
*Figure 3: Two cues for event–frame assisted decomposition. (a) Complementary structural cues from low-light frames and events: short-slice events preserve edges across illumination(a2), treating events as pseudo-gradients(a5) and fusing them with frames yields more reliable decomposition. (b) Frames and events represent two distinct quantizations of scene radiance: events (blue curve) provide finer granularity in dark regions, while frames (orange curve) offer more precision in bright areas*

![[assets/figures/papers/paper_list_l2477_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_eRetinexGS_Retinex/figures/009_Figure_7.jpg]]
*Figure 7: An example visualization of F and G degradation mapping curves on real-world data. (a) F mapping bridging the gap between the rendered real radiance and the brightness changes perceived by the event camera; (b) G mapping model the degradation process from real radiance to low-light images and handle color shifts by learning separate RGB channels*

## 实验与分析

### 实验设置与基准方法

实验在合成低光照数据集和真实采集数据上进行。合成数据通过公式 $I^{l,c} = \beta \cdot (\alpha I^n)^\gamma$ 对正常光照图像进行伽马校正和缩放生成。真实数据使用DAVIS346事件相机在极低光照条件下采集多视角帧序列和事件流，相机位姿由COLMAP估计。对于非场景级方法（如单帧图像增强、事件增强方法），首先使用它们增强所有输入视图，再将增强后的帧输入标准**3DGS**（Kerbl et al., TOG 2023）进行新视图合成，确保公平比较。所有方法使用相同的训练/测试视图划分和相机位姿。

对比方法涵盖三类：基于NeRF的无监督低光照增强方法**LLNeRF**（Wang et al., ICCV 2023）、基于Transformer的单帧Retinex增强方法**Retinexformer**（Cai et al., ICCV 2023）、事件引导的低光照视频增强方法（Liang et al., ICCV 2023），以及标准3DGS等。

### 合成数据集定量结果

Table 1给出了合成数据集上的定量对比。eRetinexGS在输入视图和新型视图合成上均取得最优性能：

- **输入视图合成**：PSNR 23.45，SSIM 0.8312，LPIPS 0.0888，显著优于所有对比方法。
- **新型视图合成**：PSNR 22.67，SSIM 0.8152，LPIPS 0.1163，同样全面领先。

这一优势源于两个关键机制：（1）事件与RGB帧在亮度量化上的互补性——事件在暗区提供更精细的梯度信息，RGB在亮区提供更精确的色彩信息；（2）事件引导的反射率平滑先验使Retinex分解在多视图间更加稳定。相比之下，纯图像方法在暗区细节丢失严重，纯事件方法存在亮度和色彩不准确问题，而直接将事件与低光照图像输入3DGS则产生色彩失真和伪影。

### 定性分析

Figure 4和Figure 5分别展示了合成数据和真实数据上的定性对比。在合成数据上，基于图像的方法在暗区无法恢复纹理细节，基于事件的方法在亮区出现色彩偏差，而eRetinexGS同时保持了暗区细节和亮区色彩准确性。在真实数据上，事件和RGB的互补性有效恢复了暗区纹理和亮区色彩，避免了伪影和色彩失真。

Figure 6(a)进一步对比了eRetinexGS与LLNeRF的Retinex分解结果。LLNeRF仅依赖图像进行分解，在暗区无法有效分离反射率和光照，导致反射率图中纹理丢失；eRetinexGS借助事件引导的平滑先验，在非事件区域强制反射率平滑、沿事件边缘保留不连续性，得到了更清晰的反射率图。

![[assets/figures/papers/paper_list_l2477_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_eRetinexGS_Retinex/figures/008_Figure_6.jpg]]
*Figure 6: (a) Comparison of decomposition results between our method and the image-based method (LLNeRF). (b) Event-guided reflectance smoothness analysis. (c) Visual ablation results: the quality of results is degraded as we remove any item*

### 消融实验

Table 2和Figure 6(c)给出了关键模块的消融分析：

1. **去除事件引导反射率平滑损失（w/o $\mathcal{L}_{tv}$）**：PSNR从23.45大幅下降至17.21，暗区细节严重丢失。这验证了事件掩膜 $M_e$ 提供的反射率平滑先验是恢复纹理的核心机制——在非事件区域惩罚反射率梯度，在事件触发区域保留边缘不连续性。

2. **去除置信度引导互补融合（w/o $\mathcal{L}_{data}$ 自适应权重）**：改为固定权重后，亮区出现色彩失真或暗区产生伪影。这证明了基于恢复辐射灰度构建置信度图、自适应加权事件损失和图像损失的必要性——暗区更信赖事件梯度，亮区更信赖RGB光度。

3. **去除退化对齐模块（F/G MLP）**：交叉模态损失变得不可靠，重建质量下降。F-MLP和G-MLP分别建模事件和图像的退化过程（公式(7)-(8)），将噪声图像和有噪声的事件对齐到干净的辐射场，是实现可靠多模态监督的基础。

Figure 7可视化了真实数据上F和G退化映射曲线：F映射桥接了渲染辐射与事件相机感知的亮度变化之间的差距；G映射建模了从真实辐射到低光照图像的退化过程，并通过学习分离的RGB通道处理色彩偏移。

### 失败模式与局限性

尽管eRetinexGS在合成和真实数据上均取得最优性能，仍存在以下局限：

1. **位姿敏感性**：当COLMAP位姿估计不准确时，方法可能失效，因为位姿错误会破坏多视图一致性和跨模态融合。这需要手动验证实际场景中的鲁棒性。

2. **事件稀疏区域**：在事件触发稀疏的区域，反射率平滑先验的约束较弱，可能导致边界模糊。

3. **非朗伯表面**：对于高光或非朗伯表面，Retinex建模的假设（反射率与光照可分离）可能不成立，导致色彩失真。

4. **训练效率**：训练时间约1小时，虽非实时，但渲染速度可达83FPS，满足交互式应用需求。

### 补充图表

![[assets/figures/papers/paper_list_l2477_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_eRetinexGS_Retinex/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison on the synthetic dataset. * indicates non-scene-based methods. Their outputs are used as input to 3DGS for fair comparison. In the Input column*

![[assets/figures/papers/paper_list_l2477_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_eRetinexGS_Retinex/figures/007_Table.jpg]]

![[assets/figures/papers/paper_list_l2477_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_eRetinexGS_Retinex/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison on real data. For visualization, input images are brightness-adjusted for clarity*

## 方法谱系与知识库定位

### 1. 方法坐标：场景级增强与新视角合成

eRetinexGS 处于**低光照场景增强**、**事件相机**与**3D高斯泼溅（3DGS）**的交叉点。与单帧图像增强或视频增强不同，该工作直接重建整个场景的3D辐射场，同时支持输入视角增强和新视角合成。其核心定位是：将事件流与低光照RGB帧作为互补观测，在3DGS框架内完成自监督的Retinex分解与辐射场恢复。

### 2. 与现有工作的关系

#### 2.1 相对于基于NeRF的低光照方法

**LLNeRF**（Wang et al., ICCV 2023）是无监督低光照NeRF的代表，但其隐式辐射场难以引入结构化的反射率先验，且渲染效率低。eRetinexGS继承了场景级增强的思路，但将表示从隐式NeRF切换为显式3DGS，并在每个高斯上显式分解反射率$r$与光照$l$（公式(2)-(3)），使Retinex分解在多视图中可优化。Figure 6(a)的分解对比表明，LLNeRF的反射率图在暗区存在噪声和伪影，而eRetinexGS借助事件引导的平滑先验获得了更干净的分解。

#### 2.2 相对于单帧/视频增强方法

**Retinexformer**（Cai et al., ICCV 2023）和**Coherent Event Guided Low-light Video Enhancement**（Liang et al., ICCV 2023）分别代表图像域和视频域的增强方案。这些方法处理的是2D观测，缺乏多视图一致性约束，且无法生成新视角。eRetinexGS的实验设计体现了这一差异：对于非场景级方法（Table 1中以*标记），先将所有输入视图逐帧增强，再送入标准3DGS进行新视角合成。结果表明，这种“增强+重建”的级联策略在PSNR上远低于eRetinexGS的端到端联合优化（23.45 vs. 次优方法），说明**多视图一致性与Retinex分解的协同**是性能增益的关键来源。

#### 2.3 相对于标准3DGS

标准**3DGS**（Kerbl et al., TOG 2023）仅建模颜色属性，在低光照条件下直接输入暗帧会导致重建失败（Figure 1(c)）。eRetinexGS在3DGS基础上增加了三个关键改造：
- **反射率-光照属性分解**：每个高斯存储$r$和$l$，替代单一颜色；
- **事件引导的反射率平滑**：$\mathcal{L}_{\mathrm{tv}}$利用事件的无触发区域作为平滑先验（公式(4)）；
- **置信度引导的多模态融合**：以恢复辐射灰度为置信度，自适应加权事件损失与图像损失（公式(5)）。

这些改造使得3DGS能够处理严重退化的低光照多模态输入。

### 3. 适用边界与假设

eRetinexGS的有效性建立在以下假设之上：

1. **静态场景**：方法假设场景在采集期间不发生运动。动态物体将破坏多视图一致性和事件-帧对齐。
2. **可靠的相机位姿**：使用COLMAP从低光照帧估计位姿。当位姿误差较大时，多视图融合和事件-帧对应关系均会失效，方法可能完全失败。
3. **朗伯表面假设**：Retinex建模将辐射分解为反射率与光照的乘积$I^r = R \odot L$。对于高光、镜面反射或非朗伯表面，该分解不再成立，可能导致色彩失真。
4. **事件密度充足**：事件引导的平滑先验依赖于事件触发区域来保留边缘。在事件稀疏的区域（如极暗且纹理缺失的表面），$\mathcal{L}_{\mathrm{tv}}$的约束力减弱，可能导致边界模糊。

### 4. 局限性与开放问题

#### 4.1 已知局限

- **位姿敏感**：COLMAP在极低光照下的位姿估计本身不可靠，这是整个管线的单点故障源。论文未提供位姿误差的鲁棒性分析。
- **训练效率**：训练时间约1小时（含两阶段优化），虽非实时但渲染速度可达83FPS。对于需要快速部署的场景，训练成本仍偏高。
- **退化模型泛化**：F-MLP和G-MLP分别建模事件和图像的退化过程（公式(7)-(8)），但这些MLP是场景特化的。跨场景泛化需要重新训练，且真实噪声的复杂性可能超出当前模型容量（Figure 7仅展示单场景拟合曲线）。

#### 4.2 开放问题

1. **动态场景扩展**：当前方法假设静态场景。如何将事件的高时间分辨率与动态3DGS表示结合，处理运动物体和光照变化，是一个重要方向。
2. **真实退化建模**：事件噪声（如热噪声、延迟噪声）和ISP管线的非线性远比合成数据复杂。能否学习通用的退化先验以减少场景特化训练？
3. **自适应超参数**：目标亮度$b_t$、损失权重$\lambda_2$–$\lambda_4$等超参数需手动设定。不同光照条件下自动调整这些参数，将提升方法的实用性。
4. **事件稀疏区域的边界保持**：当事件触发不足时，$\mathcal{L}_{\mathrm{tv}}$的掩膜$M_e$几乎全为零，退化为全局平滑，导致细节丢失。能否引入额外的结构先验（如来自RGB的梯度）来弥补？

### 5. 知识库贡献

eRetinexGS在以下方面提供了可迁移的方法论贡献：

- **事件引导的结构先验**：将事件流的时空稀疏性转化为反射率平滑的掩膜总变分约束，这一思路可推广到其他需要边缘保持平滑的逆问题（如深度补全、本征图像分解）。
- **置信度驱动的多模态融合**：基于恢复辐射的自适应加权策略，为异质传感器融合提供了一种无需标定的自监督方案。
- **3DGS的Retinex扩展**：在显式点云表示中嵌入物理启发的分解属性，为3DGS在计算摄影任务中的应用开辟了新的设计空间。

## 原文 PDF

![[paperPDFs/CVPR_2026/eRetinexGS_Retinex_Modeling_for_Low_Light_Scene_Enhancement_via_Event_Streams_and_3D_Gaussian_Splatting.pdf]]