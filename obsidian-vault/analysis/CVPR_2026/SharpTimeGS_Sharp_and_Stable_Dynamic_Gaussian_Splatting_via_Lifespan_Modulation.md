---
title: "SharpTimeGS: Sharp and Stable Dynamic Gaussian Splatting via Lifespan Modulation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SharpTimeGS_Sharp_and_Stable_Dynamic_Gaussian_Splatting_via_Lifespan_Modulation.pdf
project_link: "https://liaozhanfeng.github.io/SharpTimeGS"
code_link: null
aliases:
- SharpTimeGS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 每个高斯原语的可学习寿命参数（寿命方差 σ_t 和寿命半径 r），以及基于寿命调制的可见性函数（平顶轮廓）和运动公式（幅值缩放），从根本上拆分静态和动态行为。
primary_logic: 高斯原语的运动幅度和时间可见性与其寿命强相关：长寿命原语应保持稳定、时间不变，短寿命原语则可具有较大运动和快速淡入淡出。通过将寿命作为可学习的每原语属性并分别引入不透明度公式（平顶核）和运动公式（除法放大/抑制），可以自然统一静态和动态表示——长寿命原语自动冻结，短寿命原语保留充分的表现力。
claims:
- 引入可学习半径 r 的平顶可见性函数使单个高斯原语即可完全表示阶梯状寿命，避免了多个高斯近似（图1(b)）。
- 寿命调制的运动公式允许静态原语完全静止，无漂移，而短寿命原语保持大运动幅度（图1(d)）。
- 在 Neural3DV、ENeRF-Outdoor 和 SelfCap 三个基准上，SharpTimeGS 在所有指标（PSNR、SSIM、LPIPS）上均优于所有基线方法（表1）。
- 消融实验证明寿命调制、速度感知初始化、密集化策略和完整的4D表示各自均对最终质量有显著贡献（表2，图5）。
---

# SharpTimeGS: Sharp and Stable Dynamic Gaussian Splatting via Lifespan Modulation

> [!tip] 核心洞察
> 高斯原语的运动幅度和时间可见性与其寿命强相关：长寿命原语应保持稳定、时间不变，短寿命原语则可具有较大运动和快速淡入淡出。通过将寿命作为可学习的每原语属性并分别引入不透明度公式（平顶核）和运动公式（除法放大/抑制），可以自然统一静态和动态表示——长寿命原语自动冻结，短寿命原语保留充分的表现力。

| 字段 | 内容 |
|------|------|
| 中文题名 | SharpTimeGS: 通过寿命调制实现清晰稳定的动态高斯泼溅 |
| 英文题名 | SharpTimeGS: Sharp and Stable Dynamic Gaussian Splatting via Lifespan Modulation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.02989) · [Project](https://liaozhanfeng.github.io/SharpTimeGS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SharpTimeGS |
| Dataset | Neural3DV, ENeRF-Outdoor, SelfCap |

> [!tip] 效果简介
> - Neural3DV 上，PSNR / SSIM² / LPIPS 33.57 / 0.977 / 0.031 vs see Table 1。
> - ENeRF-Outdoor 上，PSNR / SSIM² / LPIPS 25.82 / 0.872 / 0.233 vs see Table 1。
> - SelfCap 上，PSNR / SSIM² / LPIPS 28.14 / 0.960 / 0.192 vs see Table 1。

## 概要

动态场景的新视角合成面临一个根本性瓶颈：现有基于运动的高斯泼溅方法对时间可见性和运动建模采用无差别统一公式——高斯形衰减与无约束线性运动。这迫使表示平坦的长时间可见性需要多个重叠原语，优化过程会反复插入新高斯；同时，静止原语必须学习极小速度以避免累积漂移，但实际优化无法收敛到绝对零速度，残余运动长期累积造成显著空间偏移。静态与动态区域因此难以在同一表示中获得高质量重建。

SharpTimeGS 的核心洞察是：高斯原语的运动幅度和时间可见性应与其寿命强相关。长寿命原语应保持稳定、时间不变，短寿命原语则可具有较大运动和快速淡入淡出。基于这一洞察，方法为每个高斯原语引入可学习的寿命参数——寿命方差 $\sigma_t$ 和寿命半径 $r$，并据此重新设计两个关键公式：

- **平顶时间可见性**：在 $|t-T| \leq r$ 内恒为 1，超出后指数衰减，使单个原语即可完整表示阶梯状寿命，避免多个高斯近似（Figure 1(b)）。
- **寿命调制运动**：$X_t = X + \frac{v}{f(\sigma_t, r)}(t-T)$，其中 $f(\sigma_t, r) = 1.0 + \max\{1.0, (\sigma_t + r)^2\}$ 自适应缩放运动幅度——长寿命原语运动被抑制至接近冻结，短寿命原语保留充分表现力（Figure 1(d)）。

配合速度感知初始化（利用 RAFT 光流和 SAM2 分割动静区域并赋予差异化先验）和寿命-速度感知密集化策略（在固定容量下优先为短寿命高速区域分配原语），SharpTimeGS 在 Neural3DV、ENeRF-Outdoor 和 SelfCap 三个基准上全面超越现有方法，同时保持 4K 分辨率 ≥100 FPS 的实时渲染能力（RTX 4090）。

在方法谱系中，SharpTimeGS 属于显式 4D 高斯表示路线，与 Deformable-3DGS（Yang et al., CVPR 2024）的形变场方法、Ex4DGS（Lee et al., NeurIPS 2024）和 4DGS（Yang et al., ICLR 2024）的 4D 运动方法、STGS（Li et al., CVPR 2024）的时空特征方法以及 FreeTimeGS（Wang et al., CVPR 2025）的自由运动方法形成对比。其关键区别在于通过可学习寿命参数从根本上拆分静态与动态行为，而非在统一公式下通过优化间接逼近。消融实验证实，寿命调制、速度感知初始化、密集化策略和完整 4D 表示各自均对最终质量有显著贡献（Table 2, Figure 5）。



动态视角合成（dynamic view synthesis）的核心挑战在于同时保持静态区域的长期稳定性和动态区域的瞬时表现力。近年来，基于3D高斯泼溅（3D Gaussian Splatting, 3DGS）的方法因其显式表示和实时渲染能力受到广泛关注，并已从静态场景扩展到4D动态场景。然而，现有运动基础方法（motion-based methods）在统一处理静态与动态区域时暴露出一个根本性瓶颈。

**现有方法的统一公式困境。** 当前主流方法——包括基于形变场的 **Deformable-3DGS**（Yang et al., CVPR 2024）、显式4D高斯 **Ex4DGS**（Lee et al., NeurIPS 2024）、4D高斯运动 **4DGS**（Yang et al., ICLR 2024）、时空高斯特征 **STGS**（Li et al., CVPR 2024）以及自由高斯运动 **FreeTimeGS**（Wang et al., CVPR 2025）——均采用不分行为差异的统一公式来建模高斯原语的时间可见性和运动。具体而言，时间可见性采用高斯形不透明度衰减（钟形曲线），运动则采用无约束的线性运动 $X_t = X + v \cdot (t-T)$。这种“一刀切”的建模方式在两个方向上同时失效（图1）：

1. **静态区域的漂移问题。** 对于应保持静止的长寿命原语，优化过程无法将其速度收敛到绝对零值。残余速度随时间累积，造成显著的空间偏移（图1(c)）。在长时间序列中，这种累积漂移会严重破坏背景的稳定性。
2. **动态区域的表达效率低下。** 对于应呈现阶梯状寿命（即在一段时间内完全可见、之后迅速消失）的动态原语，高斯形衰减需要多个重叠原语才能近似平坦的可见性轮廓（图1(a)）。这不仅浪费表示容量，还导致优化过程反复插入新高斯以弥补近似误差，造成表示冗余和运动拖影。

**瓶颈的本质：静态与动态的纠缠。** 上述问题的根源在于，现有方法缺乏一个能够区分原语行为模式的机制——长寿命原语应当稳定、时间不变，短寿命原语则可具有较大运动和快速淡入淡出。在统一公式下，这两类行为相互干扰：为动态区域优化的运动幅度会泄漏到静态区域，而为静态区域压制的速度又会限制动态区域的表现力。

**SharpTimeGS的动机。** 本文提出一个核心洞察：高斯原语的运动幅度和时间可见性应当与其寿命强相关。通过引入可学习的寿命参数并据此调制可见性函数和运动公式，可以自然地将静态和动态行为解耦——长寿命原语自动冻结，短寿命原语保留充分的表现力。这一设计从根本上消除了静态漂移与动态近似冗余之间的冲突，使得同一表示框架能够同时实现清晰的静态背景和锐利的动态前景。



## 核心方法与创新机理

SharpTimeGS 的核心创新在于引入**可学习的寿命参数**（lifespan parameters），从根本上重构了动态高斯泼溅中两个纠缠的建模环节——时间可见性轮廓与运动公式，从而将静态与动态区域的表示解耦到统一的框架内。

### 瓶颈诊断：统一公式引发的“动静冲突”

现有基于运动的高斯方法（如 **Deformable-3DGS** (Yang et al., CVPR 2024)、**Ex4DGS** (Lee et al., NeurIPS 2024)、**4DGS** (Yang et al., ICLR 2024)、**STGS** (Li et al., CVPR 2024)、**FreeTimeGS** (Wang et al., CVPR 2025)）对所有高斯原语采用无差别的统一公式：时间可见性遵循钟形高斯衰减，运动遵循无约束的线性位移 $X_t = X + v \cdot (t-T)$。这种“一刀切”的处理方式在两个方向上同时产生问题：

1. **静态区域漂移**：静止原语理论上需要学习 $v \approx 0$ 以避免累积位移，但优化过程无法收敛到绝对零速度。微小的残余速度 $v_{\text{residual}}$ 在长时间跨度的 $t-T$ 放大下，造成显著的空间偏移，使本该固定的背景区域出现模糊或拖影（Figure 1(c)）。
2. **动态区域容量浪费**：对于具有阶梯状寿命的动态原语（如快速移动后消失的物体），高斯形衰减需要多个重叠原语来近似平坦的可见性区间，导致表示冗余；同时，优化过程会反复插入新高斯来填补衰减造成的“空洞”，进一步加剧容量竞争（Figure 1(a)）。

这种**动静纠缠**使得同一表示难以同时保证静态背景的高保真和动态前景的充分表现力。

### 因果调节旋钮：寿命调制的可见性与运动

SharpTimeGS 为每个高斯原语引入两个可学习的寿命参数——寿命方差 $\sigma_t$ 和寿命半径 $r$，并基于这两个参数分别重新设计可见性函数和运动公式，从根本上拆分静态与动态行为。

**Changed Slot 1：时间可见性轮廓——从高斯衰减到平顶核**

基线方法使用钟形高斯衰减控制不透明度，导致可见性在时间轴上缓慢下降。SharpTimeGS 将其替换为基于可学习半径 $r$ 的**平顶轮廓**（flat-top profile）：

$$O_t = O \cdot l(t), \quad l(t) = \begin{cases} 1, & |t-T| \leq r \\ \exp\left(-\left(\frac{|t-T|-r}{\sigma_t}\right)^2\right), & |t-T| > r \end{cases}$$

在核心区间 $|t-T| \leq r$ 内，原语保持完全不透明（$l(t)=1$）；超出半径后，不透明度才以 $\sigma_t$ 为尺度指数衰减。这一设计使得**单个高斯原语即可完整表示阶梯状寿命**，无需多个原语近似（Figure 1(b)），从而大幅减少动态区域的表示冗余。

**Changed Slot 2：运动公式——从无约束线性到位移缩放**

基线方法的线性运动 $X_t = X + v \cdot (t-T)$ 对所有原语施加相同的位移规则。SharpTimeGS 引入**寿命调制的运动缩放**：

$$X_t = X + \frac{v}{f(\sigma_t, r)} (t - T), \quad f(\sigma_t, r) = 1.0 + \max\{1.0, (\sigma_t + r)^2\}$$

缩放因子 $f(\sigma_t, r)$ 随寿命参数自适应变化：长寿命原语（$\sigma_t$ 和 $r$ 较大）对应较大的 $f$ 值，运动幅度被显著抑制，逼近完全静止；短寿命原语（$\sigma_t$ 和 $r$ 较小）对应 $f \approx 2.0$，运动幅度基本不受约束（Figure 1(d)）。这种“除法放大/抑制”机制使得**静态原语天然冻结、动态原语保持充分表现力**，无需依赖优化过程将速度强制归零。

### 配套创新：寿命-速度感知的密集化与初始化

为充分发挥寿命调制的优势，SharpTimeGS 进一步在密集化策略和初始化阶段引入寿命与速度的先验：

**Changed Slot 3：密集化策略**——从无差别分配到容量倾斜。基线方法（如 AbsGS）在密集化时不区分动静区域。SharpTimeGS 采用两阶段密集化：第一阶段预集到固定容量 $N$；第二阶段根据综合得分 $s = \lambda_e E + \lambda_o O + \lambda_l (1 - \exp(-\frac{\|v\|+1}{f(\sigma_t, r)}))$ 替换低不透明度原语。得分中的寿命-速度项使**短寿命、高速度的动态区域获得更高的替换权重**，从而在固定总容量下向动态区域倾斜分配高斯原语。

**Changed Slot 4：初始化**——从统一 COLMAP 到速度感知分离。基线方法使用 COLMAP 统一初始化所有点云，速度为零。SharpTimeGS 利用 RAFT 光流估计和 SAM2 分割动态物体，为静态和动态区域分别赋予不同的位置、速度（$v_{\text{init}}$）和寿命先验（$\sigma_t$ 覆盖三帧），使优化从物理合理的初始状态开始。

### 创新本质

SharpTimeGS 的创新并非在现有框架上叠加新模块，而是通过**重新定义高斯原语的时间行为**，将“寿命”确立为连接可见性与运动的统一控制变量。这一设计使得长寿命原语自动收敛为稳定的静态表示，短寿命原语保留充分的动态表现力，从而在同一4D高斯表示中自然解耦动静建模——这是对现有动态高斯方法“统一公式”范式的根本性修正。



SharpTimeGS 的整体流程围绕“寿命调制”这一核心思想构建，将动态场景表示为一系列具有时间感知能力的4D高斯原语，并通过四个关键模块协同完成从多视角视频到新视角渲染的端到端优化。图2展示了方法的完整流水线。

**输入与初始化。** 系统的输入是多视角同步视频帧。首先进入**速度感知初始化**模块：利用 RAFT 光流估计帧间运动，结合 SAM2 分割动态物体，再通过 COLMAP 重建稀疏点云并为每个点估计初速度。该模块将场景点明确区分为静态区域和动态区域，并分别为其赋予差异化的寿命方差 $\sigma_t$ 和速度 $v$ 先验——静态点获得极小的初始速度和较大的寿命参数，动态点则相反。这一步为后续的动静统一表示提供了物理合理的起点。

**核心表示：寿命调制的4D高斯。** 初始化后的每个高斯原语携带一组可学习参数：中心位置 $X$、协方差、不透明度 $O$、球谐系数 $C_{lm}$、中心时间戳 $T$，以及本文引入的两个关键寿命参数——寿命方差 $\sigma_t$ 和寿命半径 $r$。给定任意查询时间 $t$，该模块通过两个公式将4D原语转换为3D高斯以供渲染：

1. **寿命调制运动**（公式1）：$X_t = X + \frac{v}{f(\sigma_t, r)}(t - T)$，其中 $f(\sigma_t, r) = 1.0 + \max\{1.0, (\sigma_t + r)^2\}$。调制函数 $f$ 根据原语的寿命自适应缩放运动幅度：长寿命原语的 $f$ 值极大，运动被抑制至近乎静止；短寿命原语的 $f$ 值接近1，保留充分的运动表现力。这从根本上解决了现有方法中静态原语因残余速度累积漂移的问题（图1c-d）。

2. **平顶时间可见性**（公式2）：$O_t = O \cdot l(t)$，其中 $l(t)$ 在 $|t-T| \leq r$ 区间内恒为1，超出后以 $\exp(-((|t-T|-r)/\sigma_t)^2)$ 快速衰减。这一平顶轮廓使得单个高斯原语即可完整表示阶梯状的寿命区间，无需像现有方法那样用多个重叠原语近似（图1a-b），从而避免优化过程中反复插入新原语导致的表示冗余。

颜色计算遵循标准3DGS的球谐模型（公式3）：$C_t = \sum_{l=0}^{L} \sum_{m=-l}^{l} C_{lm} Y_{lm}(\mathbf{d}(X_t))$，在移动后的位置 $X_t$ 处计算视角相关颜色。

**容量分配：寿命-速度感知密集化。** 为在固定总原语容量下高效分配表示资源，该模块采用两阶段策略。第一阶段将原语预密集化至预设数量 $N$；第二阶段根据得分 $s$（公式4）动态替换低不透明度原语：
$$s = \lambda_e E + \lambda_o O + \lambda_l \left(1 - \exp\left(-\frac{\|v\|+1}{f(\sigma_t, r)}\right)\right)$$
该得分综合了重建误差 $E$、不透明度 $O$ 以及归一化的速度-寿命比。短寿命、高速度的动态原语获得更高的替换权重，确保动态区域获得充足的表示容量，而静态区域保持紧凑。

**可微渲染与优化。** 转换后的3D高斯通过标准可微光栅化管线渲染为图像，并与真值计算复合损失函数 $\mathcal{L} = \mathcal{L}_{\text{recon}} + \mathcal{L}_{\text{reg}} + \mathcal{L}_e$，其中重建损失为 L1、SSIM 和感知损失的加权组合。梯度通过渲染管线反向传播，联合优化所有高斯参数（包括寿命参数 $\sigma_t$ 和 $r$）。

**模块间的因果流。** 速度感知初始化提供了动静分离的先验，使寿命调制的运动与可见性公式能够有效发挥作用；寿命-速度感知密集化则根据优化过程中实际涌现的寿命和速度模式动态调整容量分配，进一步强化了静态区域的稳定性和动态区域的细节表现力。三个模块形成闭环：初始化提供起点，核心表示实现动静统一，密集化优化资源分配，共同支撑了在多个基准上对静态背景和快速运动物体的高质量重建。

### 补充图表

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2602_02989/figures/002_Figure_2.jpg]]
*Figure 2: The pipeline of our method. We represent a dynamic scene using Gaussian primitives whose temporal visibility adapts to the actual lifespan of each point. To achieve this, we introduce a lifespan-dependent parameter r that modulates the temporal Gaussian, allowing a single primitive to accurately model its full lifespan. Moreover, through the modulation terms*



SharpTimeGS 的核心设计围绕一个关键洞察展开：高斯原语的运动幅度和时间可见性应与其寿命强相关。长寿命原语（静态区域）应保持稳定、时间不变；短寿命原语（动态区域）则可具有较大运动和快速淡入淡出。为此，方法引入可学习的每原语寿命参数，并重构了时间可见性轮廓与运动公式，从根本上拆分静态与动态行为。

### 寿命调制的运动公式

现有运动基础方法（如 **FreeTimeGS**，Wang et al., CVPR 2025）采用无约束的线性运动 $X_t = X + v \cdot (t - T)$，导致静态原语必须学习极小速度以避免累积漂移，但实际优化中无法收敛到绝对零速度，残余运动长期累积造成显著空间偏移。

SharpTimeGS 引入寿命调制函数 $f(\sigma_t, r)$ 自适应缩放运动幅度：

$$X_t = X + \frac{v}{f(\sigma_t, r)} (t - T), \quad f(\sigma_t, r) = 1.0 + \max\{1.0, (\sigma_t + r)^2\}$$

其中 $\sigma_t$ 为寿命方差，$r$ 为寿命半径。当原语寿命较长（$\sigma_t + r$ 大）时，$f(\sigma_t, r)$ 取值大，运动幅度被抑制，原语趋于冻结；当原语寿命较短时，$f(\sigma_t, r) \approx 2.0$，运动幅度保持充分。该设计使静态原语完全静止无漂移，而短寿命原语保留大运动幅度（Figure 1(d)）。

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2602_02989/figures/001_Figure_1.jpg]]
*Figure 1: (a) Temporal visibility in existing motion-based methods. A step-like lifespan (blue line) requires multiple Gaussian primitives for approximation. (b) With a learnable radius r, our visibility function allows a single Gaussian primitive to represent a step-like lifespan (blue line). (c) In existing motion-based methods (e.g., FreeTimeGS [41]), residual velocities accumulate over time, causing drift in static regions. (d) With our lifepan modulation term*

### 平顶时间可见性函数

现有方法采用高斯形不透明度衰减（钟形曲线），导致表示平坦的长时间可见性需要多个重叠原语近似（Figure 1(a)），优化会反复插入新高斯，造成表示冗余。

SharpTimeGS 引入可学习寿命半径 $r$，构建平顶轮廓的可见性函数：

$$O_t = O \cdot l(t), \quad l(t) = \begin{cases} \exp\left(-\left(\frac{|t-T|-r}{\sigma_t}\right)^2\right), & |t-T| > r \\ 1, & |t-T| \leq r \end{cases}$$

在寿命核心区间 $|t - T| \leq r$ 内，不透明度恒为 1；超出区间后按高斯函数快速衰减。这使得单个高斯原语即可完整表示阶梯状寿命，避免了多原语近似（Figure 1(b)），同时消除了运动拖影，产生更清晰的时间边界。

### 球谐颜色与渲染

在移动后的位置 $X_t$ 处，视角相关颜色通过球谐函数计算：

$$C_t = \sum_{l=0}^{L} \sum_{m=-l}^{l} C_{lm} Y_{lm}(\mathbf{d}(X_t))$$

将时间 $t$ 下的 4D 高斯转换为 3D 高斯后，通过标准 3DGS 可微渲染管线渲染，并计算损失。

### 寿命-速度感知密集化

为在固定总容量下有效分配高斯原语，方法设计了寿命-速度感知的两阶段密集化策略。第一阶段预集到固定数量 $N$；第二阶段根据替换得分 $s$ 移除低不透明度原语：

$$s = \lambda_e E + \lambda_o O + \lambda_l \left(1 - \exp\left(-\frac{\|v\|+1}{f(\sigma_t, r)}\right)\right)$$

该得分综合了重建误差 $E$、不透明度 $O$ 和归一化速度/寿命比。短寿命高速原语获得更高替换权重，从而优先为动态区域分配容量，增强其表达能力。



## 实验与关键发现

### 主实验结果

SharpTimeGS 在三个覆盖室内外、不同动态复杂度的基准数据集上均取得了最优性能（Table 1）。在 **Neural3DV** 数据集上，本方法达到 **33.57 dB PSNR / 0.977 SSIM² / 0.031 LPIPS**；在 **ENeRF-Outdoor** 数据集上达到 **25.82 dB PSNR / 0.872 SSIM² / 0.233 LPIPS**；在 **SelfCap** 数据集上达到 **28.14 dB PSNR / 0.960 SSIM² / 0.192 LPIPS**。相比所有基线方法——包括形变场基线 **Deformable-3DGS**（Yang et al., CVPR 2024）、显式4D高斯基线 **Ex4DGS**（Lee et al., NeurIPS 2024）、4D高斯运动基线 **4DGS**（Yang et al., ICLR 2024）、时空高斯特征基线 **STGS**（Li et al., CVPR 2024）以及自由高斯运动基线 **FreeTimeGS**（Wang et al., CVPR 2025）——SharpTimeGS 在所有指标上一致领先。

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2602_02989/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison on Neural3DV [19] Dataset, ENeRF-Outdoor [22] Dataset, and SelfCap [46] Dataset. We report PSNR, SSIM2 [42], and LPIPS [50] to evaluate the rendering quality. Values in boldface denote the best result in the corresponding column*

定性结果（Figure 3, Figure 4）进一步揭示了性能优势的来源。在 SelfCap 数据集中，本方法对远距离静态区域（如书架、墙壁）和快速运动区域（如头发、球）均展现出更清晰的重建质量，而基线方法在这些区域常出现模糊或拖影。ENeRF-Outdoor 数据集的对比同样表明，本方法在保持远距离静态背景高保真度的同时，对快速运动前景的渲染更为锐利。作者将此归因于寿命调制机制保留了 3DGS 对静态场景的强大建模能力，同时速度感知初始化与寿命-速度感知密集化策略为动态区域分配了充足的表示容量。

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2602_02989/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparison on the SelfCap Dataset [46]. Our method achieves the rendering quality compared with baseline methods, especially for distant static regions (e.g., books and wall) and fast-moving dynamic regions (e.g., hairs and ball)*

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2602_02989/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison on the ENeRF-Outdoor Dataset [22]. Our method achieves the best rendering quality compared with baseline methods, especially for distant static regions and fast-moving dynamic regions*

### 消融实验

为验证各组件的独立贡献，作者在 SelfCap 数据集上进行了系统消融（Table 2, Figure 5）。完整模型达到 **27.36 dB PSNR / 0.947 SSIM² / 0.244 LPIPS**。

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2602_02989/figures/007_Table_2.jpg]]
*Table 2: Ablation study on SelfCap [46] Dataset (Partial). We report PSNR, SSIM2, and LPIPS to evaluate the rendering quality*

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2602_02989/figures/005_Figure_5.jpg]]
*Figure 5: Ablation study on the SelfCap Dataset [46]. Our full model achieves the best rendering quality, especially for distant static regions and fast-moving dynamic regions*

- **移除4D表示（w/o 4D representation）**：用耦合的4DGS表示替代本文的解耦表示，PSNR 从 27.36 dB 降至 **25.96 dB**。这表明解耦的寿命-运动表示对重建质量至关重要。
- **移除寿命半径 r（w/o lifespan r）**：将平顶可见性函数退化为纯高斯衰减，PSNR 降至 **26.76 dB**。这验证了平顶轮廓使单个高斯原语即可完整表示阶梯状寿命、避免多原语近似带来的冗余和模糊。
- **移除寿命-速度感知密集化（w/o Densification）**：PSNR 降至 **26.82 dB**，证明基于运动幅度和寿命动态分配容量的密集化策略有效提升了动态区域的表达能力。
- **移除速度感知初始化（w/o Initialization）**：不分离动静区域且速度初始化为零，PSNR 降至 **26.83 dB**，说明物理合理的初始速度和动静分离先验对收敛和最终质量有显著贡献。

定性消融（Figure 5）与量化结果一致：完整模型在远距离静态区域和快速运动区域均保持最佳渲染质量，而各消融变体在这些关键区域出现不同程度的退化。

### 失败模式与局限性

尽管 SharpTimeGS 在渲染质量和实时性上取得了领先结果（4K 分辨率下≥100 FPS，RTX 4090），作者明确指出以下局限：

1. **训练非实时**：将多视角视频转换为4D表示仍需数小时，无法满足实时重建需求。
2. **仅支持视角合成**：当前表示不包含材质和反射属性，因此不支持重照明等高级应用。作者指出可通过引入材质和反射属性扩展框架，但这需要进一步研究。

### 开放问题

作者提出了两个值得后续探索的方向：

1. 如何利用更强的几何先验或正则化加速训练，实现更快速的场景重建？
2. 如何在保持表示质量的同时集成材质和反射属性以支持重照明？



## 定位与知识库关联

### 1. 技术脉络与基线关系

SharpTimeGS 处于**显式4D高斯泼溅**（explicit 4D Gaussian splatting）这一技术路线中。该路线以 3DGS（Kerbl et al., SIGGRAPH 2023）为基础，直接将高斯原语扩展到时间维度，避免了神经场方法（如 NeRF、K-Planes）的隐式表示和昂贵体渲染。在此路线内部，SharpTimeGS 与以下基线形成直接对比：

- **4DGS**（Yang et al., ICLR 2024）：将高斯原语赋予时间中心 $T$ 和速度 $v$，通过线性运动 $X_t = X + v \cdot (t - T)$ 描述动态。SharpTimeGS 继承了这一“运动基础”范式，但指出其**无约束线性运动**导致静止原语必须学习极小的速度来避免漂移，而实际优化中无法收敛到绝对零速度，残余运动长期累积造成空间偏移。
- **FreeTimeGS**（Wang et al., CVPR 2025）：同样采用自由高斯运动，但时间可见性使用高斯形衰减（钟形曲线）。SharpTimeGS 指出，这种**统一的高斯衰减**迫使表示平坦的阶梯状寿命时需要多个重叠原语逼近（Figure 1(a)），优化中会反复插入新高斯，导致表示冗余和运动拖影。
- **Deformable-3DGS**（Yang et al., CVPR 2024）：通过形变场将规范 3DGS 映射到各时刻，本质是隐式运动建模。SharpTimeGS 的显式运动路线与之正交，但共享“动静分离”的动机。
- **Ex4DGS**（Lee et al., NeurIPS 2024）：显式4D高斯表示的另一变体，同样面临静态漂移和动态容量不足的问题。
- **STGS**（Li et al., CVPR 2024）：引入时空高斯特征，属于特征增强路线，与 SharpTimeGS 的运动-寿命调制路线互补。

SharpTimeGS 的核心突破在于**将寿命作为每原语的可学习属性**，并以此统一调制时间可见性和运动幅度，从根本上解耦了静态和动态行为。这一思想在现有基线中未见先例。

### 2. 知识库定位

#### 2.1 核心贡献定位

SharpTimeGS 在动态场景表示领域做出了以下可定位的贡献：

| 贡献维度 | 具体内容 | 知识库定位 |
|----------|----------|------------|
| **时间可见性建模** | 将高斯形衰减替换为基于可学习寿命半径 $r$ 的平顶轮廓（公式2） | 首次在显式4DGS中引入平顶时间核，解决了“多原语逼近单寿命”的冗余问题 |
| **运动-寿命耦合** | 通过 $f(\sigma_t, r)$ 自适应缩放运动幅度（公式1），使长寿命原语自动冻结、短寿命原语保持表现力 | 首次将运动幅度与时间持久性显式耦合，消除了静态漂移与动态表达之间的权衡 |
| **容量分配策略** | 寿命-速度感知密集化（公式4），在固定总容量下优先为短寿命高速区域分配原语 | 为动态场景的显式表示提供了新的容量分配准则 |
| **初始化策略** | 利用 RAFT 光流和 SAM2 分割实现动静分离和速度先验初始化 | 将视觉基础模型（SAM2）引入4DGS初始化流程 |

#### 2.2 适用边界

**适用场景**：
- 多视角视频的**视角合成**任务（novel view synthesis）
- 包含显著动静混合的场景（如人体运动、户外交通）
- 需要实时渲染的应用（4K 分辨率 ≥100 FPS，RTX 4090）

**不适用/未验证场景**：
- **重照明**（relighting）：当前表示仅建模视角相关颜色，不含材质和反射属性。论文明确指出可通过引入 BRDF 属性扩展，但尚未实现。
- **训练效率**：将多视角视频转换为4D表示仍需数小时，未达到实时/近实时重建。
- **极长时序**：寿命参数 $\sigma_t$ 和 $r$ 的可学习范围是否足以覆盖极长视频（如数分钟以上）尚未验证。

#### 2.3 局限与开放问题

**已确认局限**：
1. **训练非实时**：从多视角视频到可渲染4D表示的转换过程仍需数小时，限制了交互式应用场景。
2. **表示能力受限**：仅支持视角合成，不支持材质编辑和重照明，但论文指出可通过引入材质和反射属性扩展。

**开放问题**：
1. **训练加速**：如何利用更强的几何先验（如深度估计、多视图立体匹配）或正则化手段加速训练，实现更快速的场景重建？
2. **材质扩展**：如何在保持表示质量和渲染效率的同时，集成材质和反射属性以支持重照明？
3. **寿命先验的泛化性**：当前速度感知初始化依赖 RAFT 和 SAM2，这些模型在极端运动模糊或遮挡场景下的鲁棒性如何？寿命先验的质量对最终重建的影响边界在哪里？
4. **理论分析**：寿命调制函数 $f(\sigma_t, r) = 1.0 + \max\{1.0, (\sigma_t + r)^2\}$ 的设计是否存在更优的参数化形式？平顶核的锐利边界是否会在某些场景引入时间不连续性伪影？

### 3. 证据强度评估

| 主张 | 证据类型 | 强度 | 备注 |
|------|----------|------|------|
| 平顶可见性消除多原语逼近 | 定性对比（Figure 1(a,b)）+ 消融实验（Table 2, w/o lifespan r） | 强 | 消融中移除 $r$ 导致 PSNR 下降 0.60 dB |
| 寿命调制消除静态漂移 | 定性对比（Figure 1(c,d)）+ 系统级验证 | 中强 | 漂移消除的量化指标未单独报告，需结合整体质量提升推断 |
| 全指标 SOTA | 三个基准的量化对比（Table 1） | 强 | Neural3DV、ENeRF-Outdoor、SelfCap 上 PSNR/SSIM²/LPIPS 均最优 |
| 各模块贡献 | 消融实验（Table 2） | 强 | 四个模块分别消融，均有显著下降 |
| 实时渲染能力 | 单卡 FPS 报告 | 中 | 仅报告了 4K 分辨率 ≥100 FPS，未提供多分辨率/多场景的系统性测试 |



## 原文 PDF

![[paperPDFs/CVPR_2026/SharpTimeGS_Sharp_and_Stable_Dynamic_Gaussian_Splatting_via_Lifespan_Modulation.pdf]]
