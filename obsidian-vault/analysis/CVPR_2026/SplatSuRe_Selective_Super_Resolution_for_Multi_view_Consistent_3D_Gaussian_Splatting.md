---
title: "SplatSuRe: Selective Super-Resolution for Multi-view Consistent 3D Gaussian Splatting"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SplatSuRe_Selective_Super_Resolution_for_Multi_view_Consistent_3D_Gaussian_Splatting.pdf
project_link: "https://splatsure.github.io"
code_link: null
aliases:
- SplatSuRe
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 基于每高斯屏幕空间半径比的高斯保真度分数，以此生成选择性超分辨率权重图，调制SR在像素级的监督强度。
primary_logic: 多视图采样密度不均：近景LR视图可为远景提供高频监督，根据每高斯的观察半径比可精确识别欠采样区域，仅在需要处注入生成式细节，从而在保持多视图一致性的同时显著提升锐度。
claims:
- 高斯保真度分数能够量化每个3D区域在多视图中的高频信息充足程度，并通过渲染权重图实现选择性SR。
- 在Tanks & Temples和Deep Blending数据集上，SplatSuRe在PSNR、SSIM、LPIPS等多个指标上显著超过所有基线，且视觉质量更清晰。
- 消融实验表明，适度使用SR（τ=1.1）在锐度与一致性之间取得最佳折衷，过量SR反而降低质量。
- 选择性策略在不同SR模型上均一致优于统一应用的基线，不依赖于特定SR架构。
---

# SplatSuRe: Selective Super-Resolution for Multi-view Consistent 3D Gaussian Splatting

> [!tip] 核心洞察
> 多视图采样密度不均：近景LR视图可为远景提供高频监督，根据每高斯的观察半径比可精确识别欠采样区域，仅在需要处注入生成式细节，从而在保持多视图一致性的同时显著提升锐度。

| 字段 | 内容 |
|------|------|
| 中文题名 | SplatSuRe：面向多视图一致的3D高斯泼溅的选择性超分辨率 |
| 英文题名 | SplatSuRe: Selective Super-Resolution for Multi-view Consistent 3D Gaussian Splatting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.02172) · [Project](https://splatsure.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SplatSuRe |
| Dataset | Tanks & Temples, Deep Blending |

> [!tip] 效果简介
> - Tanks & Temples 上，PSNR 23.81 vs 23.32 (SRGS) (+0.49)；LPIPS 0.272 vs 0.286 (SRGS) (-0.014)。
> - Deep Blending 上，PSNR 29.01 vs 28.43 (Mip-Splatting) (+0.58)；SSIM 0.872 vs 0.861 (SRGS) (+0.011)。

## 概述

### 问题与瓶颈

基于3D高斯泼溅（3D Gaussian Splatting, 3DGS）的新视角合成在低分辨率（LR）输入下面临一个根本性矛盾：一方面，LR图像缺乏高频几何与纹理细节，导致渲染结果模糊；另一方面，若直接对每张LR图像应用单图超分辨率（SISR）再训练3DGS，会在已被其他视角充分采样的区域引入生成式伪影，破坏多视图一致性。现有方法（如 **SRGS** 联合LR与统一SR监督，或 **Mip-Splatting** 通过多尺度滤波缓解锯齿）均未区分场景中不同区域对SR的需求差异——它们要么全图统一施加SR，要么完全回避SR，难以在锐度与一致性之间取得最优平衡。

这一瓶颈的本质在于：**多视图采样密度在空间上高度不均**。近景LR视图可为远景渲染提供天然的高频监督，而某些区域（如背景树木、被遮挡的前景桌面）则缺乏任何视角的近距离观测。统一SR策略忽视了这种“信息冗余”与“信息缺失”并存的结构，导致不必要的生成式细节注入，反而损害渲染质量。

### 核心方法：选择性超分辨率

SplatSuRe 提出了一种**选择性超分辨率**框架，核心思想是：仅在3D场景中高频信息不足的区域引入SR生成式细节，而在已有充分多视图覆盖的区域保持LR重建的几何一致性。实现这一目标的关键机制是**高斯保真度分数（Gaussian Fidelity Score）**。

具体而言，方法首先在LR图像上预训练一个3DGS模型，获取每个高斯在每张训练视图中的屏幕空间半径。通过计算每个高斯在所有视图中最大半径与最小半径之比 $\rho^{i} = r_{max}^{i} / r_{min}^{i}$，可以近似该高斯对应的3D区域被多视图采样的相对频率。该半径比随后通过带阈值 $\tau$ 的Sigmoid函数映射为 $[0,1]$ 范围的保真度分数：

$$\operatorname{score}_{\mathcal{G}^{i}} = \sigma\left(\frac{\rho^{i} - \tau}{k}\right)$$

低分表示该高斯在多视图中被观测得极不均匀（某些视角很近、某些很远），即该区域缺乏可靠的高频信息，需要SR补充；高分则表示多视图采样充足，LR监督已足够。基于这些分数，方法为每张训练视图渲染一张空间权重图 $W_t$，在高分辨率3DGS训练时对SR损失（L1和D-SSIM）进行逐像素加权，最终与下采样LR重建损失联合优化。

### 方法定位

在3DGS超分辨率的方法谱系中，SplatSuRe 的独特贡献在于**将“是否需要SR”的决策从图像空间提升到3D场景表示空间**。与以下方法形成对比：

- **3DGS (LR)**：仅用LR图像训练，完全不加SR，结果模糊。
- **3DGS + StableSR**：先对每张LR图像独立超分，再训练3DGS，多视图一致性差。
- **SRGS + StableSR**：联合LR与SR监督，但对所有像素施加均匀SR损失，过度引入生成式细节。
- **Mip-Splatting**：通过3D高斯的多尺度滤波缓解锯齿，但不引入额外高频信息。

SplatSuRe 的选择性策略使SR成为3D重建的“按需补充”而非“全局覆盖”，在方法谱系中开辟了基于3D几何分析的自适应SR监督新路径。

### 主要结果

在 **Tanks & Temples**、**Deep Blending** 和 **Mip-NeRF 360** 三个数据集上的4×超分辨率实验中，SplatSuRe 在多项指标上显著超越所有基线：

- **Tanks & Temples**：PSNR 达 **23.81**（较SRGS提升0.49），LPIPS降至 **0.272**（降低0.014）。
- **Deep Blending**：PSNR 达 **29.01**（较Mip-Splatting提升0.58），SSIM达 **0.872**（较SRGS提升0.011）。

定性结果（Figure 5）显示，SplatSuRe 在文字细节、高频纹理和远景物体上均呈现更清晰、更忠实于真值的重建，同时减少了其他方法中常见的高斯伪影。消融实验进一步验证了选择性策略的核心作用：当阈值 $\tau=1.1$ 时，方法在锐度与一致性之间取得最佳折衷；过度使用SR（$\tau \to \infty$，即全图统一SR）反而导致指标下降。此外，该选择性框架不依赖特定SR架构——在 SwinIR 和 StableSR 上均一致优于SRGS，且在 StableSR 上获得更佳的感知质量。

### 局限与展望

当前方法在锐利边界或高对比度区域仍可能出现少量伪影，且仅基于屏幕空间半径比判定采样充足性，未考虑纹理频率本身。在场景多视图采样极度密集时（如Mip-NeRF 360数据），方法优势减弱。未来工作可探索多尺度或频域的高斯保真度评估、动态阈值调整，以及将该选择框架推广至其他神经渲染表示（如NeRF系列）。

## 背景与动机

### 3D高斯泼溅与多视图重建的困境

3D Gaussian Splatting（3DGS）已成为新视角合成的主流方法，通过显式3D高斯原语和可微光栅化实现高质量实时渲染。然而，3DGS的渲染质量高度依赖输入图像的分辨率——当训练视图为低分辨率（LR）图像时，模型缺乏足够的高频几何细节，导致渲染结果模糊，丢失纹理锐度与精细结构。

这一困境在多视图场景中尤为突出：**不同视角对同一三维区域的采样密度天然不均**。如Figure 3所示，近景相机的LR视图实际上已为远景区域提供了相对更高分辨率的观测信息；反之，某些区域在所有训练视角中都处于欠采样状态，无法从任何LR视图中获取充足的高频线索。

### 现有方案的局限：统一超分辨率的代价

为弥补LR输入的信息缺口，一个直接思路是引入单图超分辨率（Single-Image Super-Resolution, SISR）模型。现有方法大致分为两类：

- **预处理式**：先用SISR模型对所有LR图像逐帧超分，再以超分结果训练3DGS（如 **3DGS + StableSR**）。这种方式完全依赖SR模型输出，忽略了多视图间原有的几何一致性约束。
- **联合式**：在3DGS训练过程中同时施加LR重建损失与SR监督损失（如 **SRGS**）。这在一定程度上保留了场景几何，但其SR损失对**所有像素施加均等权重**，即统一地将生成式高频细节注入每个区域。

统一SR策略的根本缺陷在于：**在已由其他视角充分采样的区域，强行注入SR生成的细节会引入多视图不一致**。SR模型作为单图方法，缺乏跨视图的一致性保证，其在不同视图中对同一纹理可能生成不同的高频模式。当这些不一致的细节被均等地纳入3DGS优化时，会干扰场景的几何收敛，导致渲染中出现闪烁、伪影等跨视图不一致现象。

### 核心洞察：选择性注入生成式细节

SplatSuRe的动机源于一个关键观察：**多视图LR数据中蕴含的高频信息并非均匀缺失，而是呈现空间异质性**。具体而言：

- 某高斯原语在训练视图中的**屏幕空间半径**反映了该区域被“放大”观察的程度：半径越大，该视角对该区域的采样越密集，能提供的高频信息越丰富。
- 通过比较同一高斯在所有训练视图中的最大与最小屏幕半径之比 $\rho^{i} = r_{max}^{i} / r_{min}^{i}$，可以近似估计该三维区域在多视图中的**相对采样频率**。
- 比值 $\rho^{i}$ 较大的高斯意味着存在某些视角对其进行了更近距离的观测，其高频信息已隐含在LR数据中；比值接近1的高斯则表明所有视角对该区域的采样密度相近，缺乏额外的高频线索，**真正需要SR生成细节的正是这些区域**。

基于这一洞察，SplatSuRe提出了一种**选择性超分辨率**策略：首先从LR预训练的3DGS模型中提取每高斯的屏幕空间半径比，将其映射为**高斯保真度分数**，量化每个三维区域的高频信息充足程度；然后渲染为逐视图的空间权重图，仅在欠采样区域赋予高SR权重，在已充分采样区域抑制SR监督。这种“按需注入”的方式在保持多视图几何一致性的前提下，最大化地利用SR模型的生成能力来提升渲染锐度。

## 核心创新

SplatSuRe 的核心创新在于将单图超分辨率（SISR）以**选择性、视图一致的方式**注入 3D Gaussian Splatting（3DGS）的重建流程，而非简单地统一应用 SR。其关键洞察是：**低分辨率（LR）训练视图之间存在天然的采样密度差异**——近景视图中的某个区域在远景视图中可能呈现为高频细节，因此并非所有像素都需要等量的生成式 SR 监督。基于此，方法设计了一套从“三维高频充足性评估”到“二维空间加权监督”的完整机制，从根本上改变了 SR 与 3DGS 的交互方式。

### 核心因果旋钮

方法引入了一个可调节的**因果旋钮**：**基于每高斯屏幕空间半径比的高斯保真度分数**（Gaussian Fidelity Score）。该分数量化了每个 3D 高斯在多视图中的采样充足程度，并据此生成逐像素的**选择性 SR 权重图**，从而在训练过程中精确控制 SR 监督在空间上的强弱分布。

### 关键创新槽位

相较于将 SR 统一应用于所有像素的基线方法（如 SRGS），SplatSuRe 在以下三个关键槽位上做出了根本性改变：

| 创新槽位 | 基线做法 | SplatSuRe 做法 | 因果逻辑 |
|:---|:---|:---|:---|
| **三维区域高频充足性评估** | 无（不区分区域） | 计算每个高斯在所有训练视图中的最大与最小屏幕半径之比 $\rho^{i} = r_{max}^{i} / r_{min}^{i}$，通过带阈值 $\tau$ 的 Sigmoid 映射为 $[0,1]$ 的保真度分数 | 半径比近似了多视图采样频率：比值大意味着该高斯在某些视图中被“放大”观察，蕴含丰富高频信息；比值小则意味着该区域在所有视图中分辨率均不足，亟需 SR 注入 |
| **SR 监督的权重分布** | 统一（每个像素等权） | 将高斯保真度分数渲染为逐视图的空间权重图 $W_t$，在欠采样区域赋予高权重，充分采样区域赋予低权重 | 权重图实现了“按需分配”的 SR 监督：近景已充分观察的区域抑制 SR 以避免多视图不一致，远景或遮挡区域增强 SR 以补充缺失细节 |
| **SR 损失函数** | 对所有像素施加均匀 L1 和 D-SSIM 损失 | 使用权重图对 L1 和 D-SSIM 损失进行空间加权：$\mathcal{L}_{SR} = (1-\lambda)\mathcal{L}_1^{W}(R_{HR}, I_{SR}) + \lambda\mathcal{L}_{D\text{-SSIM}}^{W}(R_{HR}, I_{SR})$ | 加权损失确保优化信号集中在真正需要生成式细节的区域，避免在已有充分 LR 监督的区域引入 SR 模型可能产生的幻觉伪影 |

### 创新机制的因果链条

整个创新机制形成一条清晰的因果链：

1. **LR 预训练获取几何先验**：首先在 LR 图像上训练一个初始 3DGS 模型，获得场景的粗糙几何以及每个高斯在每视图中的屏幕空间半径 $r^{i}$。
2. **半径比量化采样充足性**：对每个高斯，计算其在所有训练视图中的最大与最小屏幕半径之比 $\rho^{i}$。该比值直观地反映了该 3D 区域在多视图中的“被放大观察”的程度——比值越大，说明存在某些视图对该区域提供了更高频的采样。
3. **Sigmoid 映射为保真度分数**：通过 $\operatorname{score}_{\mathcal{G}^{i}} = \sigma\left(\frac{\rho^{i} - \tau}{k}\right)$ 将半径比映射为 $[0,1]$ 分数。阈值 $\tau$ 是关键的**可控旋钮**：$\tau$ 越低，越多的区域被认为“采样充足”，SR 使用越保守；$\tau$ 越高，SR 使用越激进。
4. **渲染为空间权重图**：将保真度分数与最大半径视角指示结合，渲染为每张训练视图的 SR 权重图 $W_t$。权重图在欠采样区域（如远景背景、遮挡区域）呈现高亮，在充分采样区域（如近景主体）呈现暗色。
5. **加权 SR 损失引导优化**：在高分辨率 3DGS 训练时，权重图调制 SR 损失，与下采样的 LR 重建损失联合优化（$\mathcal{L} = (1-\gamma)\mathcal{L}_{LR} + \gamma\mathcal{L}_{SR}$），最终产出锐利且多视图一致的高分辨率渲染结果。

### 与基线方法的本质区别

- **vs. 统一 SR（如 SRGS）**：SRGS 对所有像素施加等权 SR 监督，在已由其他视角充分采样的区域引入不必要的生成式细节，导致多视图不一致。SplatSuRe 的选择性机制从根本上规避了这一问题。
- **vs. 先 SR 后重建（如 3DGS + StableSR）**：该基线在训练前对 LR 图像逐一超分，SR 模型的多视图不一致性被固化到输入中。SplatSuRe 将 SR 作为训练中的软约束，通过权重图灵活调节其影响。
- **vs. 仅用 LR（如 3DGS LR）**：完全放弃 SR 导致渲染模糊，缺乏高频几何细节。SplatSuRe 在需要处精准注入 SR，在不需要处保持 LR 监督的视图一致性，实现了锐度与一致性的最优折衷。

## 整体框架

SplatSuRe 的核心思路是 **“仅在高频信息不足的区域引入生成式超分辨率，其余区域由多视图低分辨率一致性约束”**。其整体流水线由五个紧密耦合的模块构成，形成一条从低分辨率几何估计到选择性超分监督的闭环。

### 1. 低分辨率 3DGS 预训练

流水线的起点是使用低分辨率（LR）图像训练一个基础的 3DGS 模型。这一阶段的目的并非直接获得高质量渲染，而是**利用 LR 输入恢复场景的粗略几何结构**，尤其是每个高斯在每张训练视图中的屏幕空间半径 $r^{i}$。该半径由投影后的 2D 协方差矩阵的特征值计算得出：

$$r^{i} = 3 \sqrt{\max(\lambda_{1}^{i}, \lambda_{2}^{i})}$$

其中 $\lambda_{1}^{i}, \lambda_{2}^{i}$ 是协方差矩阵 $\Sigma_{2D}^{i}$ 的两个特征值。屏幕半径直接反映了该高斯在当前视角下的空间采样密度——半径越大，意味着该区域在像素空间中占据更多样本，该视角对该高斯的观测越“近”越“清晰”（Figure 2 左侧 LR 3DGS 分支）。

![[assets/figures/papers/paper_list_l2600_https_arxiv_org_abs_2512_02172/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our SplatSuRe framework. A high-resolution (HR) 3D Gaussian Splatting (3DGS) model is trained using lowresolution (LR) and super-resolution (SR) inputs. We first train a 3DGS model on LR inputs to identify undersampled regions and render per-view weight maps that indicate where SR is needed. During training of the HR 3DGS model, the images produced by the frozen single-image super-resolution (SISR) model are spatially weighted by these maps to form the SR loss*

### 2. 高斯保真度分数计算

预训练完成后，SplatSuRe 对每个高斯计算一个**保真度分数**（Gaussian Fidelity Score），用以量化该三维区域在多视图中的高频信息充足程度。核心指标是**半径比**（radius ratio）：

$$\rho^{i} = r_{max}^{i} / r_{min}^{i}$$

其中 $r_{max}^{i}$ 和 $r_{min}^{i}$ 分别是高斯 $i$ 在所有训练视图中的最大和最小屏幕半径。直觉上，$\rho^{i}$ 近似于该高斯被多视图采样的频率比：若某高斯在所有视图中半径相近（$\rho^{i} \approx 1$），说明它被均匀采样，LR 视图已提供充足信息；若半径差异悬殊（$\rho^{i} \gg 1$），则表明存在某些视角极度欠采样，需要超分辨率补充细节。

半径比通过带阈值的 Sigmoid 函数映射为 $[0,1]$ 的分数：

$$\operatorname{score}_{\mathcal{G}^{i}} = \sigma\left(\frac{\rho^{i} - \tau}{k}\right)$$

其中 $\tau$ 是阈值参数（默认 $\tau=1.1$），$k=0.05$ 控制过渡平滑度。**分数越低，表示该高斯越需要超分辨率**；分数越高，表示 LR 多视图监督已足够。此外，可见视图数少于 3 的高斯分数被强制置零，因为这些区域在多视图中约束不足，不宜引入生成式细节。

### 3. 逐视图权重图渲染

有了每个高斯的保真度分数后，SplatSuRe 将其渲染回每张训练视图的像素空间，生成**空间自适应的超分辨率权重图** $W_t$。渲染过程结合了两部分信息：

- **保真度分数渲染**：$(1 - \mathrm{Render}(\mathbf{score}_{\mathcal{G}}))$，将低分（需超分）区域映射为高权重。
- **最大半径指示**：$\mathrm{Render}(\mathbf{1}_{\mathcal{M}(t)}(\mathcal{G}))$，其中 $\mathcal{M}(t)$ 是所有在视角 $t$ 中取得最大屏幕半径的高斯集合。这一项确保在某个视角中“看得最清楚”的区域不会被强行注入超分细节。

最终权重图经归一化后，**明亮区域表示需要生成式细节的欠采样区域，暗色区域表示已由其他 LR 视图充分采样的区域**（Figure 4 展示了拖拉机背景树林和宴会厅前景桌面的权重分布）。

### 4. 选择性 SR 加权损失

在高分辨率 3DGS 训练阶段，SplatSuRe 使用一个**冻结的单图超分模型**（如 StableSR）对 LR 图像进行超分，生成 $I_{SR}$。与 SRGS 等基线对所有像素施加均匀损失不同，SplatSuRe 用权重图 $W_t$ 对 L1 和 D-SSIM 损失进行空间调制：

$$\mathcal{L}_{SR} = (1 - \lambda) \mathcal{L}_{1}^{W}(R_{HR}, I_{SR}) + \lambda \mathcal{L}_{\mathrm{D-SSIM}}^{W}(R_{HR}, I_{SR})$$

其中 $R_{HR}$ 是高分辨率 3DGS 的渲染输出，$\lambda=0.2$。权重图使超分监督**集中于欠采样区域，而在多视图信息充足的区域被抑制**，从根本上避免了统一超分引入的多视图不一致。

### 5. 联合 LR + SR 优化

选择性 SR 损失并非孤立使用，而是与下采样的 LR 重建损失联合优化：

$$\mathcal{L}_{LR} = (1 - \lambda) \mathcal{L}_{1}(R_{HR}\!\downarrow, I_{LR}) + \lambda \mathcal{L}_{\mathrm{D-SSIM}}(R_{HR}\!\downarrow, I_{LR})$$

$$\mathcal{L} = (1 - \gamma) \mathcal{L}_{LR} + \gamma \mathcal{L}_{SR}$$

其中 $\gamma=0.4$ 控制 SR 损失的整体权重。**LR 损失提供全图一致的几何约束，SR 损失在欠采样区域注入高频细节**，两者互补。Figure 2 清晰展示了这一双分支架构：LR 分支（下采样后与 LR 真值比较）和 SR 分支（经权重图调制后与超分图像比较）共同驱动高分辨率 3DGS 的优化。

### 模块关系与数据流

整个流水线的数据流可概括为：

1. **LR 图像 → 预训练 3DGS**：提取每高斯屏幕半径 → 计算保真度分数
2. **保真度分数 + 最大半径指示 → 渲染权重图**：逐视图生成空间 SR 权重
3. **LR 图像 → 冻结 SR 模型 → $I_{SR}$**：生成超分参考图像
4. **权重图 × SR 损失 + LR 重建损失 → 联合优化 HR 3DGS**：输出高分辨率新视角渲染

消融实验表明，适度的 SR 使用（$\tau=1.1$）在锐度与一致性之间取得最佳折衷，而统一训练流程（合并预训练与微调）可在不牺牲性能的前提下减少训练开销（Table 6）。

## 核心模块与公式推导

SplatSuRe 的核心在于构建一个**空间自适应的超分辨率监督机制**，通过量化每个三维区域在多视图中的高频信息充足性，仅在欠采样区域注入生成式细节。整个流水线围绕三个关键模块展开：高斯保真度分数计算、逐视图权重图渲染、以及选择性 SR 损失加权。

### 高斯保真度分数：量化多视图采样充足性

该模块的目标是为场景中每个高斯分配一个 $[0,1]$ 的分数，反映该三维区域在训练视图中的相对采样频率。高分表示该区域已被充分观察，LR 真值本身即可提供足够的高频监督；低分则表示该区域在多视图中均未获得足够的分辨率覆盖，需要 SR 模型生成额外细节。

**步骤一：屏幕空间半径计算。** 首先在低分辨率图像上预训练一个 3DGS 模型，获取场景的几何先验。对于每个高斯 $i$，将其 3D 协方差投影到视图 $t$ 的像平面，得到 2D 协方差矩阵 $\Sigma_{2D}^{i}$。该矩阵的特征值刻画了高斯在屏幕上的扩散程度，其屏幕空间半径定义为：

$$r^{i} = 3 \sqrt{\max(\lambda_{1}^{i}, \lambda_{2}^{i})}$$

其中 $\lambda_{1}^{i}, \lambda_{2}^{i}$ 为 $\Sigma_{2D}^{i}$ 的特征值：

$$\lambda_{1}^{i}, \lambda_{2}^{i} = \frac{1}{2} \mathrm{tr}(\Sigma_{2D}^{i}) \pm \sqrt{\max\{0.1, \frac{1}{4} \mathrm{tr}^{2}(\Sigma_{2D}^{i}) - |\Sigma_{2D}^{i}|\}}$$

半径 $r^{i}$ 以像素为单位，反映了高斯 $i$ 在当前视图中的投影尺度——近景高斯半径大，远景高斯半径小。

**步骤二：半径比作为采样频率代理。** 对于每个高斯，在所有训练视图中找到其最大屏幕半径 $r_{max}^{i}$ 和最小屏幕半径 $r_{min}^{i}$，定义半径比：

$$\rho^{i} = r_{max}^{i} / r_{min}^{i}$$

这一比值近似了该高斯在多视图中的相对采样频率：若某高斯在所有视图中都被远距离观察（半径均小），则 $\rho^{i}$ 接近 1，表示采样不足；若存在近景视图使其半径显著增大，则 $\rho^{i}$ 远大于 1，表示该区域已被充分采样。

**步骤三：Sigmoid 映射为保真度分数。** 通过带阈值的 Sigmoid 函数将半径比映射为 $[0,1]$ 的分数：

$$\operatorname{score}_{\mathcal{G}^{i}} = \sigma\left(\frac{\rho^{i} - \tau}{k}\right)$$

其中 $\tau$ 为阈值参数（默认 $\tau=1.1$），控制 SR 介入的激进程度；$k=0.05$ 控制过渡平滑度。此外，对于在训练视图中出现次数少于 3 次的高斯，分数直接置零——这些区域在多视图中约束不足，其几何本身不可靠。

### 逐视图权重图渲染：将三维分数投影到二维空间

获得每高斯的保真度分数后，需要将其渲染为每张训练图像上的空间权重图，以指示哪些像素区域需要 SR 监督。

首先定义**最大半径视角集** $\mathcal{M}(t)$——所有在视图 $t$ 中取得最大屏幕半径的高斯集合：

$$\mathcal{M}(t) = \{\mathcal{G}^{i} \mid t = \operatorname{argmax}_{t' \in T} r_{t'}^{i}\}$$

直观上，若某高斯在视图 $t$ 中半径最大，说明 $t$ 是观察该区域的最佳视角。

逐视图的未归一化权重图 $W_{t}'$ 由两项合成：

$$W_{t}' = (1 - \mathrm{Render}(\mathbf{score}_{\mathcal{G}})) + \mathrm{Render}(\mathbf{1}_{\mathcal{M}(t)}(\mathcal{G}))$$

第一项将保真度分数通过可微渲染投影到图像空间，低分区域（欠采样）获得高权重；第二项为最大半径指示函数，确保在最佳视角中即使高分区域也保留一定 SR 监督。最终对 $W_{t}'$ 进行归一化，得到 $W_t$。

### 选择性 SR 加权损失：空间调制的监督信号

高分辨率 3DGS 训练时，总损失由两项加权组合：

$$\mathcal{L} = (1 - \gamma) \mathcal{L}_{LR} + \gamma \mathcal{L}_{SR}$$

其中 $\gamma=0.4$ 控制 SR 监督的全局强度。

**LR 重建损失** 对全图提供一致的基础监督，将 HR 渲染下采样后与 LR 真值比较：

$$\mathcal{L}_{LR} = (1 - \lambda) \mathcal{L}_{1}(R_{HR}\!\downarrow, I_{LR}) + \lambda \mathcal{L}_{\mathrm{D-SSIM}}(R_{HR}\!\downarrow, I_{LR})$$

其中 $\lambda=0.2$。

**选择性 SR 损失** 是方法的核心创新——使用权重图 $W_t$ 对 L1 和 D-SSIM 损失进行逐像素加权：

$$\mathcal{L}_{SR} = (1 - \lambda) \mathcal{L}_{1}^{W}(R_{HR}, I_{SR}) + \lambda \mathcal{L}_{\mathrm{D-SSIM}}^{W}(R_{HR}, I_{SR})$$

在权重图高亮区域（欠采样），SR 监督被放大，驱动模型学习生成式高频细节；在暗区（充分采样），SR 监督被抑制，模型主要依赖 LR 真值保持多视图一致性。这种选择性机制是 SplatSuRe 在锐度与一致性之间取得平衡的关键因果旋钮。

### 补充图表

![[assets/figures/papers/paper_list_l2600_https_arxiv_org_abs_2512_02172/figures/004_Figure_4.jpg]]
*Figure 4: Super-resolution weight maps. Bright regions indicate areas where generative detail is required, while dark regions correspond to areas well-sampled by other low-resolution views. Note that high weights are obtained in regions that are either not sampled closely, such as background trees behind the tractor, or where other views do not provide higher resolution information, such as the foreground table in the ballroom*

## 实验与分析

### 核心定量结果

SplatSuRe 在三个主流基准上均取得一致的指标领先。在 **Tanks & Temples** 的 4× SR 设定下，方法以 PSNR **23.81**、SSIM **0.784**、LPIPS **0.272** 超过所有基线（Table 1）。相比最强的先前方法 SRGS，PSNR 提升 **+0.49**，LPIPS 降低 **0.014**。在 **Deep Blending** 上优势更为显著：PSNR **29.01**（较 Mip-Splatting 的 28.43 提升 +0.58），SSIM **0.872**（较 SRGS 的 0.861 提升 +0.011），且在所有指标上均取得最优（Table 2）。在 **Mip-NeRF 360** 上，方法同样超过 SRGS，但在该数据集上优势收窄——这与场景本身多视图采样极度密集、LR 图像已保留大部分细节的特性一致。

![[assets/figures/papers/paper_list_l2600_https_arxiv_org_abs_2512_02172/figures/006_Table_1.jpg]]
*Table 1: Quantitative results on Tanks & Temples [15]. Experiments are performed at 4× super-resolution using ratio threshold τ =1.1. The best , second best and third best entries are highlighted. Our SplatSuRe method achieves the strongest results across most metrics*

![[assets/figures/papers/paper_list_l2600_https_arxiv_org_abs_2512_02172/figures/007_Table_2.jpg]]
*Table 2: Quantitative results on Deep Blending [8] and Mip-NeRF 360 [1]. Our SplatSuRe method achieves the strongest results across all metrics on Deep Blending and outperforms SRGS [6] on Mip-NeRF 360. Appendix A.1 and A.3 present 8× SR and per-scene results*

定性结果（Figure 5）印证了指标趋势：SplatSuRe 在文字细节（卡车红色框）、高频纹理（地毯黄色框、托盘绿色框）以及远景物体（教堂壁画蓝色框）上均呈现更锐利、更忠实于真值的重建，同时有效减少了其他方法中出现的高斯伪影（橙色箭头）。

![[assets/figures/papers/paper_list_l2600_https_arxiv_org_abs_2512_02172/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative results on Tanks & Temples [15], Deep Blending [8], and Mip-NeRF 360 [1]. Experiments are performed at 4× super-resolution with ratio threshold τ =1.1. Compared to Mip-Splatting [33] and SRGS [6], our method produces sharper, more faithful reconstructions that better align with ground truth while maintaining cross-view consistency. It preserves finer details in text (red box on truck), high-frequency patterns (yellow box on carpet and green box on tray) and distant objects observed in other views (blue box on church mural). Notably, it reduces Gaussian artifacts (orange arrow) observed in other methods. Additional results in Appendix A.4*

8× SR 设定下的结果进一步验证了方法的可扩展性：在 Tanks & Temples 上，SplatSuRe 在大多数指标上保持最优（Table 4）；在 Deep Blending 和 Mip-NeRF 360 上，几乎全部指标取得最强结果（Table 5）。

![[assets/figures/papers/paper_list_l2600_https_arxiv_org_abs_2512_02172/figures/010_Table_4.jpg]]
*Table 4: Quantitative results on Tanks & Temples [15] at 8× super-resolution. Experiments are performed using ratio threshold τ =1.1. The best , second best and third best entries are highlighted. Our SplatSuRe method achieves the strongest results on most metrics*

![[assets/figures/papers/paper_list_l2600_https_arxiv_org_abs_2512_02172/figures/011_Table_5.jpg]]
*Table 5: Quantitative results on Deep Blending [8] and Mip-NeRF 360 [1] at 8× super-resolution. Experiments are performed using ratio threshold τ =1.1. Our SplatSuRe method achieves the strongest results on almost all metrics*

### 消融实验

**阈值 τ 的选择**（Figure 6, Section 7.1）是方法的核心控制旋钮。τ=0 对应不使用 SR（纯 LR 监督），τ=∞ 对应全图均匀使用 SR。实验表明，适度引入 SR（τ=1.1）在锐度与多视图一致性之间取得最佳折衷——PSNR、SSIM、LPIPS 均达到峰值。SR 使用不足导致模糊，而过量使用则引入多视图不一致，使指标反而下降。这一趋势在大多数场景中一致出现（Figure 7），验证了“选择性施加 SR 优于均匀施加”的核心假设。少数场景（如 Mip-NeRF 360 的 bicycle、garden、stump）在过量 SR 下指标持平或微升，原因是这些场景的输入图像本身已包含丰富高频细节，SR 主要表现为简单的锐化或边缘增强，而非生成新结构，均匀应用的危害较小（Figure 8）。

**SR 模型的独立性**（Table 3, Section 7.2）：将底层 SR 模型从 StableSR 替换为 SwinIR 后，SplatSuRe 的选择性策略仍然一致优于 SRGS。SwinIR 因其保守的重建特性取得更高 PSNR，而 StableSR 在感知质量上更优——方法对 SR 架构不敏感，验证了选择性框架的通用性。

**训练流程的简化**（Table 6, Appendix A.2）：将 LR 预训练与 SR 微调合并为统一流水线，在不牺牲性能的前提下减少了训练开销，表明两阶段并非必要。

### 失败模式与局限

尽管选择性策略有效抑制了多视图不一致，方法在以下场景仍存在局限：
- **锐利边界与高对比度区域**可能出现少量伪影，当前基于屏幕空间半径比的判定对这些区域的建模粒度不足。
- **极度密集采样的场景**（如 Mip-NeRF 360）中，方法优势减弱，因为 LR 输入本身已捕获大部分高频信息，SR 的边际收益有限。
- **对 SR 模型的依赖性**：若底层单图 SR 模型本身引入大量多视图不一致细节，选择性框架无法完全消除其影响。
- 当前仅在**静态场景**上验证，动态场景或视频输入未涉及。

### 补充图表

![[assets/figures/papers/paper_list_l2600_https_arxiv_org_abs_2512_02172/figures/008_Figure_6.jpg]]
*Figure 6: Effect of ratio threshold on Tanks & Temples [15]. Weight maps, where bright regions indicate higher SR influence, are shown below the corresponding ratio thresholds. τ =0 and τ =∞ correspond to zero and full use of super-resolution. SR is initially helpful in improving rendering quality, but excessive use worsens results. The effect of ratio threshold on different scenes is analyzed in Appendix A.3*

![[assets/figures/papers/paper_list_l2600_https_arxiv_org_abs_2512_02172/figures/009_Table_3.jpg]]
*Table 3: Comparison of SwinIR [16] and StableSR [27] on Tanks & Temples [15]. Experiments are performed at 4× superresolution using ratio threshold τ =1.1. Our method outperforms SRGS with either model. While SwinIR achieves higher PSNR due to its conservative reconstruction, we choose StableSR for our main experiments for its superior perceptual quality*

![[assets/figures/papers/paper_list_l2600_https_arxiv_org_abs_2512_02172/figures/012_Table_6.jpg]]
*Table 6: Quantitative comparison of our unified and two-stage pipelines at 4× SR across Tanks & Temples [15], Deep Blending [8], and Mip-NeRF 360 [1]. Experiments are performed using ratio threshold τ = 1.1. The best entry is bolded. The unified pipeline achieves similar performance to the two-stage approach while requiring less training time*

![[assets/figures/papers/paper_list_l2600_https_arxiv_org_abs_2512_02172/figures/013_Figure_7.jpg]]
*Figure 7: Representative scenes that benefit from an optimal amount of super-resolution. Top: Image quality vs. ratio threshold plots. Bottom: ground truth images illustrating scene structure for (a) ballroom from Tanks & Temples [15], (b) kitchen from Mip-NeRF 360 [1] and (c) francis from Tanks & Temples. Applying SR to the most poorly sampled regions yields large gains in image quality, whereas excessive SR introduces multi-view inconsistencies that sharply degrade quality. Most scenes exhibit this behavior, supporting our hypothesis that selectively applying SR is more beneficial than applying it uniformly*

![[assets/figures/papers/paper_list_l2600_https_arxiv_org_abs_2512_02172/figures/014_Figure_8.jpg]]
*Figure 8: Representative scenes that plateau in image quality or continue to benefit from increased amounts of super-resolution. Top: Image quality vs. ratio threshold plots. Bottom: ground truth images illustrating scene structure for (a) bicycle, (b) garden, and (c) stump from Mip-NeRF 360 [1]. Applying SR to the most poorly sampled regions yields large gains in image quality, while further increasing SR yields diminishing returns or no improvement. In particular, this occurs in scenes where the input images already contain substantial high-frequency detail and SR produces simpler sharpening or edge-enhancement effects rather than hallucinating new structure, making uniform application less harmful...*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

SplatSuRe 的核心问题锚点是**低分辨率（LR）输入下的多视图一致高分辨率渲染**。现有方法可沿两条轴线定位：**3DGS 的抗锯齿与频率增强**，以及**单图超分辨率（SISR）与 3D 重建的融合方式**。

**3DGS 内部增强路线**以 **Mip-Splatting** 为代表，它通过多尺度滤波缓解 3DGS 在缩放时的混叠伪影，但本质上是频率截断策略，无法从 LR 输入中恢复缺失的高频几何细节。SplatSuRe 与此类方法的根本差异在于，它引入了外部生成式细节而非仅对现有频率做滤波。

**SISR+3DGS 融合路线**以 **SRGS** 为直接前身。SRGS 将 SISR 模型的输出作为伪真值，与 LR 真值联合监督 3DGS 训练。其关键瓶颈在于**统一施加 SR 监督**——对所有像素赋予等权重的 L1 和 D-SSIM 损失。这在多视图场景中引入系统性矛盾：近景 LR 视图已为远景区域提供了充足的高频采样，统一 SR 会在这些区域注入生成式细节，导致跨视图不一致。

SplatSuRe 的突破在于将“是否施加 SR”从**全局二值决策**变为**像素级自适应调制**。这一转变依赖一个可验证的因果旋钮：**每高斯的屏幕空间半径比**。该比值近似了每个 3D 区域在多视图间的相对采样频率——半径比越大，表明该高斯在不同视图中的观察尺度差异越大，某些视图对其采样严重不足。通过带阈值的 Sigmoid 映射，该比值被转化为 [0,1] 的高斯保真度分数，进而渲染为逐视图的空间权重图，精确控制 SR 损失在每个像素的强度。

**与 3DGS (LR) 和 3DGS + StableSR 的关系**：前者仅用 LR 图像训练，是“无 SR”的下界；后者对每张 LR 图像独立超分后再训练 3DGS，是“全 SR 但无多视图一致性约束”的朴素基线。SplatSuRe 在两者之间建立了连续谱——通过阈值 τ 控制 SR 的介入程度，τ=0 退化为全 SR，τ→∞ 退化为无 SR，中间值实现选择性增强。

### 2. 适用边界与局限

**适用场景**：SplatSuRe 在**多视图采样密度不均**的场景中优势最显著。典型情况包括：近距离拍摄的物体与远距离背景共存（如 Tanks & Temples 的室外场景）；部分区域仅被少数视图覆盖。在这些场景中，LR 视图间的“高频信息互补”是方法有效性的前提——近景视图的 LR 图像天然包含远景区域的高频纹理，SplatSuRe 正是利用了这一跨视图信息差。

**性能退化条件**：
- **多视图采样极度密集**：当所有视图的采样密度趋于均匀（如 Mip-NeRF 360 数据集的某些场景），LR 图像本身已保留大部分高频细节，SR 的边际收益递减。Table 2 显示 SplatSuRe 在 Mip-NeRF 360 上对 SRGS 的优势小于 Deep Blending，验证了这一趋势。
- **SR 模型本身多视图一致性差**：SplatSuRe 的选择性机制可以抑制不一致细节的传播，但不能完全消除。若 SR 模型在欠采样区域生成的细节与 LR 真值存在结构性矛盾，仍可能影响最终质量。Table 3 显示 SwinIR（保守重建）在 PSNR 上优于 StableSR（感知质量优先），印证了 SR 模型特性对最终指标的影响。

**已知局限**（需手动验证）：
- 锐利边界或高对比度区域仍可能出现少量伪影，当前的选择性策略对这些区域的建模不够精细。
- 仅基于屏幕空间半径比判定采样充足性，未考虑纹理频率本身——低频纹理区域即使采样稀疏也不需要 SR，而高频纹理区域即使采样相对充分也可能受益于 SR。多尺度扩展可提升控制精度。
- 仅在静态场景上验证，动态场景或视频输入未涉及。

### 3. 开放问题

1. **多尺度/频域采样充足性度量**：当前的高斯保真度分数基于单一尺度的屏幕空间半径比。将其扩展为多尺度表示或频域分析，可更精细地区分“需要 SR 的高频缺失”与“仅需锐化的边缘增强”，有望进一步提升选择性精度。

2. **与扩散模型等强生成式 SR 的协同**：扩散模型（如 StableSR）能生成更丰富的感知细节，但多视图一致性更弱。SplatSuRe 的选择性框架天然适合约束这类模型——仅在欠采样区域激活强生成能力，在充分采样区域依赖 LR 真值。这一组合可能突破当前 SISR 模型在 3D 重建中的一致性瓶颈。

3. **阈值 τ 的自适应调节**：当前 τ 为全局超参数，需手动调节以平衡锐度与一致性。能否在训练过程中根据场景统计或损失动态自适应调整 τ，是提升方法易用性的关键问题。

4. **向其他神经渲染表示的推广**：高斯保真度分数的核心思想——基于多视图采样密度评估高频充足性——不依赖于 3DGS 的具体表示。该框架能否迁移到 NeRF 系列方法（通过沿光线的采样密度或射线覆盖范围定义类似度量），值得探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/SplatSuRe_Selective_Super_Resolution_for_Multi_view_Consistent_3D_Gaussian_Splatting.pdf]]