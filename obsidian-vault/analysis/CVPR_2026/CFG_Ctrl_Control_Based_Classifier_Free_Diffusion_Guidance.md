---
title: "CFG-Ctrl: Control-Based Classifier-Free Diffusion Guidance"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CFG_Ctrl_Control_Based_Classifier_Free_Diffusion_Guidance.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Wang_CFG-Ctrl_Control-Based_Classifier-Free_Diffusion_Guidance_CVPR_2026_paper.html
project_link: https://hanyang-21.github.io/CFG-Ctrl
code_link: null
aliases:
- SCSMCC
- CFG-Ctrl
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将 CFG 重新建模为一阶反馈控制系统，引入滑模控制（SMC），在语义误差空间中定义指数型滑模面 s(t)=ė(t)+λe(t) 并加入切换校正项 Δe = -k·sign(s(t))，以非线性方式强制生成轨迹沿滑模面快速收敛至语义平衡点。
primary_logic: 将扩散引导视为控制问题，利用滑模控制的鲁棒性和有限时间收敛特性，解决了线性引导在高增益下的非线性发散，从而在保持语义对齐的同时提升生成质量和稳定性。
claims:
- 标准 CFG 在 (e, ė) 平面上表现为理想线性收敛，但在实际高 w 下出现强烈振荡和发散。
- SMC-CFG 定义的滑模面 s(t)=ė(t)+λe(t) 在 Lyapunov 稳定性框架下保证单调能量衰减，且切换控制律 k·sign(s) 确保有限时间收敛至 s=0。
- 在 SD3.5、Flux-dev 和 Qwen-Image 三个主干上，SMC-CFG 在 FID、CLIP Score、ImageReward、MPS 等指标上均一致优于标准 CFG 及其他变体。
- 消融实验表明，适中的超参数 λ 和 k（如 λ=5, k=0.4）可在语义对齐（CLIP）和生成质量（FID/美学）之间取得最佳平衡。
---

# CFG-Ctrl: Control-Based Classifier-Free Diffusion Guidance

> [!tip] 核心洞察
> 将扩散引导视为控制问题，利用滑模控制的鲁棒性和有限时间收敛特性，解决了线性引导在高增益下的非线性发散，从而在保持语义对齐的同时提升生成质量和稳定性。

| 字段 | 内容 |
|------|------|
| 中文题名 | CFG-Ctrl：基于控制的免分类器扩散引导 |
| 英文题名 | CFG-Ctrl: Control-Based Classifier-Free Diffusion Guidance |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_CFG-Ctrl_Control-Based_Classifier-Free_Diffusion_Guidance_CVPR_2026_paper.html) · [Project](https://hanyang-21.github.io/CFG-Ctrl) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SMC-CFG (Sliding Mode Control CFG) |
| Dataset | MS-COCO 2017 / Stable Diffusion 3.5, MS-COCO 2017 / Flux-dev, MS-COCO 2017 / Qwen-Image |

> [!tip] 效果简介
> - MS-COCO 2017 / Stable Diffusion 3.5 上，FID↓ 20.044 vs 21.421 (CFG) (-1.377)；CLIP↑ 0.3694 vs 0.3681 (CFG) (+0.0013)；ImageReward↑ 0.9486 vs 0.8889 (CFG) (+0.0597)。
> - MS-COCO 2017 / Flux-dev 上，FID↓ 26.398 vs 27.323 (CFG) (-0.925)；CLIP↑ 0.3743 vs 0.3692 (CFG) (+0.0051)。
> - MS-COCO 2017 / Qwen-Image 上，FID↓ 33.371 vs 35.431 (CFG) (-2.060)。

## 概要

扩散模型（特别是基于流匹配的文本到图像生成模型）在语义对齐与生成质量之间长期存在张力。标准免分类器引导（CFG）通过线性外推条件与无条件速度场来增强文本一致性，但其本质上是一个**固定增益的比例控制器**，在高引导尺度下会引发强非线性振荡、色彩过饱和及语义发散——这一瓶颈在模型容量持续增大的趋势下愈发突出。

本文提出 **CFG-Ctrl**，一个将扩散引导重新建模为一阶反馈控制系统的统一理论框架。在此框架下，各类 CFG 变体被解释为不同的控制策略：标准 CFG 为比例控制（P-control），权重调度为增益调度，APG 与 CFG-Zero* 为投影控制，Rectified-CFG++ 为模型预测控制。基于这一控制视角，作者进一步提出 **SMC-CFG**（滑模控制 CFG），在语义误差空间中定义指数型滑模面 $ \mathbf{s}(t) = \dot{\mathbf{e}}(t) + \lambda \mathbf{e}(t) $，并引入非线性切换校正项 $ \Delta\mathbf{e} = -\mathbf{K} \cdot \mathrm{sign}(\mathbf{s}(t)) $，强制生成轨迹沿滑模面快速收敛至语义平衡点。Lyapunov 稳定性分析证明了该机制的有限时间收敛特性，为引导过程提供了理论保障。

在 **Stable Diffusion 3.5、Flux-dev 和 Qwen-Image** 三个主流主干上的实验表明，SMC-CFG 在 FID、CLIP Score、ImageReward、MPS 等多维度指标上一致优于标准 CFG 及其他变体。例如，在 SD3.5 上 FID 从 21.421 降至 20.044，ImageReward 从 0.8889 提升至 0.9486；在 Flux-dev 上 CLIP 从 0.3692 提升至 0.3743。消融实验进一步揭示了滑模面参数 λ 与切换增益 k 的权衡机制：适中的 λ（如 5）和 k（如 0.4）可在语义对齐与生成质量之间取得最佳平衡，而极端取值则会导致收敛缓慢或采样抖振。

该方法的核心贡献在于：将扩散引导从启发式线性外推提升为具有理论收敛保证的非线性反馈控制，为解决高引导尺度下的生成稳定性问题提供了新的范式。

### 扩散生成中的引导范式

流匹配（Flow Matching）和扩散模型已成为文本到图像生成的核心范式，其采样过程可视为从噪声分布到数据分布的连续时间演化。为了提升生成结果对文本条件的忠实度，**免分类器引导（Classifier-Free Guidance, CFG）**（Ho & Salimans, arXiv 2022）通过线性插值条件与无条件速度场来增强条件信号：

$$\hat{\mathbf{v}}_{\theta}(\mathbf{x}_t, t, \mathbf{c}) = \mathbf{v}_{\theta}(\mathbf{x}_t, t, \emptyset) + w \cdot \big( \mathbf{v}_{\theta}(\mathbf{x}_t, t, \mathbf{c}) - \mathbf{v}_{\theta}(\mathbf{x}_t, t, \emptyset) \big)$$

其中 $w$ 为引导权重，控制条件信息对采样轨迹的影响强度。这一简单而有效的机制已成为扩散生成的事实标准。

### 线性引导的瓶颈

尽管 CFG 在实践中广泛应用，其本质是一个**固定增益的比例控制器（P-control）**。当引导权重 $w$ 增大以追求更强的语义对齐时，生成动力学表现出显著的非线性特征。在 $(e, \dot{e})$ 相平面上（其中 $e(t) = \mathbf{v}_{\theta}(\mathbf{x}_t, t, \mathbf{c}) - \mathbf{v}_{\theta}(\mathbf{x}_t, t, \emptyset)$ 为语义误差），标准 CFG 的理想线性收敛轨迹在**高引导尺度下退化为强烈的振荡甚至发散**（见 Figure 1 左侧），具体表现为：

- **色彩过饱和与伪影**：过强的条件外推破坏图像的自然统计特性；
- **语义不一致**：振荡导致生成内容偏离文本描述的结构与空间关系；
- **缺乏收敛保证**：线性控制律无理论稳定性保障，完全依赖启发式调参。

### 现有变体的局限

为缓解上述问题，研究者提出了多种 CFG 变体，但均未从根本上突破线性控制的框架：

| 方法 | 控制类型 | 核心策略 | 局限 |
|------|----------|----------|------|
| **Weight Scheduler**（Wang et al., TMLR 2024） | 时变增益比例控制 | 引入 $w(t)$ 调度引导强度 | 仍为线性反馈，无法抑制高增益振荡 |
| **APG**（Sadat et al., ICLR 2024） | 投影反馈控制 | 抑制平行分量过饱和 | 仅做方向约束，未改变线性收敛动力学 |
| **CFG-Zero\***（Fan et al., arXiv 2025） | 投影反馈控制 | 针对流匹配优化引导尺度 | 同上，缺乏对系统动态的主动调控 |
| **Rectified-CFG++**（Saini et al., arXiv 2025） | 模型预测控制风格 | 结合校正流 | 计算开销大，理论收敛性未严格证明 |

这些方法可统一归纳为 $\mathbf{u}_t = K_t \Pi_t(\mathbf{e}(t))$ 的形式——即通过增益调度矩阵 $K_t$ 和方向算子 $\Pi_t$ 对误差信号做**线性或投影变换**，但控制律本身始终保持在比例控制的范畴内。当模型容量增大、引导强度提升时，系统的非线性发散问题依然存在。

### 本文动机

上述分析揭示了一个核心矛盾：**扩散引导本质上是一个动态系统的反馈控制问题，而现有方法却始终局限于线性控制范式**。本文从控制理论的视角重新审视 CFG，提出 **CFG-Ctrl** 统一框架，将引导过程建模为对一阶连续时间生成流的加性控制：

$$\frac{d\mathbf{x}_t}{dt} = \mathbf{v}_{\theta}(\mathbf{x}_t, t) + \mathbf{u}_t$$

其中控制输入 $\mathbf{u}_t$ 以语义误差 $\mathbf{e}(t)$ 为反馈信号。在这一框架下，本文的核心动机是：**引入非线性控制机制，利用滑模控制（Sliding Mode Control, SMC）的鲁棒性和有限时间收敛特性，从根本上解决线性引导在高增益下的稳定性缺陷**。

## 核心方法与创新机理

CFG-Ctrl 的核心创新在于将扩散模型的免分类器引导（CFG）重新建模为一阶反馈控制系统，并以**非线性滑模控制（Sliding Mode Control, SMC）**替代传统线性比例控制，从根本上解决了高引导尺度下的生成不稳定性问题。

### 从线性控制到非线性滑模控制

现有 CFG 及其变体本质上都是**线性反馈控制器**的不同实现形式（见 Table 1）。标准 CFG 等价于一个固定增益的比例控制器（P-control），其引导速度由条件-无条件速度差 $\mathbf{e}(t)$ 线性放大得到：

$$\hat{\mathbf{v}}_\theta(\mathbf{x}_t, t, \mathbf{c}) = \mathbf{v}_\theta(\mathbf{x}_t, t, \emptyset) + w \cdot \mathbf{e}(t)$$

后续改进如 Weight Scheduler（时变增益 $w(t)$）、APG（投影矩阵控制）等，虽然调整了增益调度 $K_t$ 或方向算子 $\Pi_t$，但控制律本质上仍保持线性结构。这种线性控制在模型容量增大或引导权重 $w$ 较高时，生成动力学呈现强非线性，导致在 $(\mathbf{e}, \dot{\mathbf{e}})$ 平面上出现**振荡、过冲、色彩过饱和及语义不一致**等发散行为（Figure 1 左）。

SMC-CFG 的关键突破在于引入**非线性切换控制**，在语义误差空间中定义指数型滑模面：

$$\mathbf{s}(t) = \dot{\mathbf{e}}(t) + \lambda \mathbf{e}(t)$$

该滑模面编码了理想的误差动力学 $\dot{\mathbf{e}} = -\lambda \mathbf{e}$，即语义误差应沿指数衰减轨迹收敛至零。当系统状态偏离滑模面（$\mathbf{s}(t) \neq 0$）时，SMC-CFG 通过切换校正项强制系统向滑模面趋近：

$$\Delta\mathbf{e}(t) = -\mathbf{K} \cdot \mathrm{sign}(\mathbf{s}(t))$$

这一非线性校正注入到语义误差中（$\mathbf{e}(t) \leftarrow \mathbf{e}(t) + \Delta\mathbf{e}(t)$），使生成轨迹沿滑模面快速收敛至语义平衡点（Figure 1 右）。

### 理论保证：Lyapunov 稳定性与有限时间收敛

与现有方法的启发式设计不同，SMC-CFG 提供了严格的**Lyapunov 稳定性分析**。通过构造 Lyapunov 函数 $V(\mathbf{s}) = \frac{1}{2}\|\mathbf{s}\|^2$，可证明 $\dot{V} = \mathbf{s}^\top \dot{\mathbf{s}} < 0$，保证滑模面能量单调衰减。切换控制律 $\mathbf{K} \cdot \mathrm{sign}(\mathbf{s})$ 进一步确保系统在**有限时间内**收敛至 $\mathbf{s}=0$，而非渐进收敛。这一理论保障使 SMC-CFG 在高引导尺度下仍能维持稳定的生成质量，从根本上解决了线性引导的非线性发散问题。

### Changed Slots 总结

| 控制维度 | 基线方法 | SMC-CFG |
|---------|---------|---------|
| 控制律类型 | 线性比例控制（固定/时变增益）或投影线性组合 | 非线性滑模控制，叠加切换项 $\Delta\mathbf{e} = -\mathbf{K} \cdot \mathrm{sign}(\mathbf{s}(t))$ |
| 误差信号处理 | 直接使用条件-无条件速度差 $\mathbf{e}(t)$ | 误差经滑模面校正：$\mathbf{e}(t) \leftarrow \mathbf{e}(t) + \Delta\mathbf{e}(t)$ |
| 收敛保证 | 无理论收敛保证，启发式设计 | Lyapunov 稳定性分析证明有限时间收敛 |

这些 changed slots 使 SMC-CFG 在保持语义对齐的同时，显著提升了生成质量和稳定性，尤其在 SD3.5、Flux-dev 和 Qwen-Image 三个主流主干模型上，FID、CLIP Score、ImageReward 等指标均一致优于标准 CFG 及其他变体（Table 2）。

CFG-Ctrl 将流匹配模型中的免分类器引导（CFG）重新建模为一个连续时间一阶反馈控制系统。其核心思想是：将条件速度与无条件速度之差定义为**语义误差信号** $\mathbf{e}(t) = \mathbf{v}_{\theta}(\mathbf{x}_t, t, \mathbf{c}) - \mathbf{v}_{\theta}(\mathbf{x}_t, t, \emptyset)$，并将该误差作为反馈控制器的输入，通过设计不同的控制律来调节采样过程的动力学行为。

### 统一控制框架

整个 pipeline 建立在受控常微分方程之上：

$$
\frac{d\mathbf{x}_t}{dt} = \mathbf{v}_{\theta}(\mathbf{x}_t, t) + \mathbf{u}_t,
$$

其中 $\mathbf{u}_t$ 是加性控制输入。该控制输入被统一分解为两个组件的组合：

$$
\mathbf{u}_t = K_t \cdot \Pi_t\big(\mathbf{e}(t)\big),
$$

- **引导调度矩阵 $K_t$**：决定控制增益的幅值与时间演化。标准 CFG 使用恒定标量增益 $w$，而变体方法可引入时变调度 $w(t)$ 或矩阵增益。
- **方向算子 $\Pi_t$**：决定误差信号在速度空间中的投影与重塑方式。标准 CFG 使用恒等映射 $\Pi_t = I$，而 APG 等方法则引入投影矩阵以选择性增强特定方向分量。

这一分解将现有 CFG 变体统一纳入控制理论视角：标准 CFG 等价于**固定增益比例控制器（P-control）**，Weight Scheduler 属于**增益调度比例控制**，APG 和 CFG-Zero* 属于**投影反馈控制**，Rectified-CFG++ 则近似于**模型预测控制**（见 Table 1）。

### SMC-CFG 的模块化流程

本文提出的 SMC-CFG 在上述框架内引入非线性滑模控制律，其采样过程由以下模块串联构成：

1. **条件/无条件速度预测**：在当前状态 $\mathbf{x}_t$ 和时间步 $t$，分别计算条件速度 $\mathbf{v}_{\theta}(\mathbf{x}_t, t, \mathbf{c})$ 和无条件速度 $\mathbf{v}_{\theta}(\mathbf{x}_t, t, \emptyset)$。

2. **语义误差计算**：取两者之差得到误差信号 $\mathbf{e}(t)$。

3. **滑模面构造**：利用当前误差与历史误差构建指数型滑模面 $\mathbf{s}(t) = \dot{\mathbf{e}}(t) + \lambda \mathbf{e}(t)$，其中 $\lambda > 0$ 控制理想误差动力学的收敛速率。滑模面 $\mathbf{s}(t) = 0$ 定义了期望的语义平衡流形。

4. **切换控制计算**：根据滑模面符号生成非线性校正项 $\Delta\mathbf{e}(t) = -k \cdot \mathrm{sign}(\mathbf{s}(t))$，其中 $k > 0$ 为切换增益，决定趋近滑模面的强度。

5. **误差校正**：将校正项叠加至原始误差：$\mathbf{e}(t) \leftarrow \mathbf{e}(t) + \Delta\mathbf{e}(t)$。

6. **引导速度合成**：以校正后的误差合成最终采样速度 $\hat{\mathbf{v}}_t = \mathbf{v}_{\theta}(\emptyset) + w \cdot \mathbf{e}(t)$。

7. **ODE 更新**：利用 $\hat{\mathbf{v}}_t$ 执行一步 ODE 积分，得到下一状态 $\mathbf{x}_{t-1}$。

### 从线性到非线性的关键转变

标准 CFG 的线性比例控制在高引导尺度下存在根本性局限：当 $w$ 较大时，生成轨迹在 $(\mathbf{e}, \dot{\mathbf{e}})$ 平面上出现强烈振荡和发散，表现为色彩过饱和、结构畸变和语义不一致（见 Figure 1 左侧）。SMC-CFG 通过切换控制项 $\Delta\mathbf{e}$ 引入非线性强制作用，将系统状态驱动至滑模面 $\mathbf{s}=0$ 并沿该流形快速收敛至语义平衡点。Lyapunov 稳定性分析（$V(\mathbf{s}) = \frac{1}{2}\|\mathbf{s}\|^2$，$\dot{V} < 0$）保证了这一过程的有限时间收敛性，从而在维持语义对齐的同时抑制高增益下的非线性发散。

![[assets/figures/papers/paper_list_l9_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_CFG_Ctrl_Control/figures/001_Figure_1.jpg]]
*Figure 1: Phase diagram in the e-e˙ plane. We schematically illustrate the convergence patterns of CFG and the proposed SMC-CFG. Left: CFG’s ideal linear convergence trajectory and the strong oscillatory divergence under high guidance scales. Right: the proposed SMC-CFG, through a switching-forcing mechanism, drives the system states toward the sliding mode surface governed by parameter λ, achieving robust and rapid convergence*

> **注意**：Lyapunov 分析依赖速度场可微性假设，实际大规模潜在扩散模型中雅可比矩阵计算开销较大，论文未给出高效近似方案，该理论保障在实际部署中的严格性需要进一步验证。

SMC-CFG 的核心在于将扩散引导重新建模为**一阶反馈控制系统**，并在语义误差空间中引入**非线性滑模控制**，以替代传统 CFG 的线性比例控制。整个方法可分解为以下关键模块。

### 3.1 语义误差信号与受控流动力学

首先，定义**语义预测误差**作为反馈控制的核心信号：

$$
\mathbf{e}(t) = \mathbf{v}_{\boldsymbol{\theta}}(\mathbf{x}_t, t, \mathbf{c}) - \mathbf{v}_{\boldsymbol{\theta}}(\mathbf{x}_t, t, \boldsymbol{\varnothing})
$$

其中 $\mathbf{v}_{\boldsymbol{\theta}}(\mathbf{x}_t, t, \mathbf{c})$ 和 $\mathbf{v}_{\boldsymbol{\theta}}(\mathbf{x}_t, t, \boldsymbol{\varnothing})$ 分别为条件和无条件速度场预测。该误差直接编码了条件信息与无条件先验之间的语义差异。

在此基础上，流匹配的采样过程被建模为带加性控制输入的连续时间动力系统：

$$
\frac{d\mathbf{x}_t}{dt} = \mathbf{v}_{\theta}(\mathbf{x}_t, t) + \mathbf{u}_t
$$

控制输入 $\mathbf{u}_t$ 被分解为**引导调度矩阵** $K_t$ 和**方向算子** $\Pi_t$ 的组合，统一解释了各类 CFG 变体：

$$
\mathbf{u}_t = K_t \Pi_t \big( \mathbf{e}(t) \big)
$$

在此框架下，标准 CFG 等价于一个**固定增益的比例控制器**（$K_t = w$, $\Pi_t = I$），仅对误差进行线性缩放，这在高引导尺度下必然导致非线性发散。

### 3.2 滑模面构造

为克服线性控制的局限性，SMC-CFG 在 $( \mathbf{e}, \dot{\mathbf{e}} )$ 相平面中设计了一个**指数型滑模面**：

$$
\mathbf{s}(t) = \dot{\mathbf{e}}(t) + \lambda \mathbf{e}(t)
$$

其中 $\lambda > 0$ 为滑模面参数，决定了理想误差动力学 $\dot{\mathbf{e}} = -\lambda \mathbf{e}$ 的收敛速率。当系统状态位于滑模面 $\mathbf{s}(t) = 0$ 上时，语义误差将沿该流形以指数速率衰减至零，实现期望的语义对齐。

### 3.3 切换控制律与误差校正

为强制系统状态趋近并维持在滑模面上，SMC-CFG 引入**切换控制律**，对语义误差施加非线性校正：

$$
\Delta \mathbf{e}(t) = -\mathbf{K} \cdot \mathrm{sign}\big( \mathbf{s}(t) \big)
$$

其中 $\mathbf{K}$ 为切换增益矩阵（实际实现中简化为标量增益 $k$），$\mathrm{sign}(\cdot)$ 为逐元素符号函数。该校正项根据滑模面符号产生不连续的“推拉”力，驱动状态穿越滑模面并产生高频切换，从而在有限时间内收敛至 $\mathbf{s}=0$。

校正后的误差 $\mathbf{e}(t) \leftarrow \mathbf{e}(t) + \Delta \mathbf{e}(t)$ 随后用于合成最终引导速度：

$$
\hat{\mathbf{v}}_{\theta}(\mathbf{x}_t, t, \mathbf{c}) = \mathbf{v}_{\theta}(\mathbf{x}_t, t, \varnothing) + w \cdot \mathbf{e}(t)
$$

### 3.4 稳定性保障：Lyapunov 有限时间收敛

SMC-CFG 的收敛性由 **Lyapunov 稳定性分析**严格保证。定义 Lyapunov 能量函数：

$$
V(\mathbf{s}) = \frac{1}{2} \|\mathbf{s}\|^2, \quad \dot{V} = \mathbf{s}^{\top} \dot{\mathbf{s}} < 0
$$

在切换控制律作用下，可证明 $\dot{V} \leq -\eta \|\mathbf{s}\|$（$\eta > 0$ 与增益 $k$ 相关），从而保证滑模面在**有限时间**内收敛至零。这一理论保障是 SMC-CFG 区别于所有启发式 CFG 变体的根本优势——它不依赖经验调参来避免发散，而是通过非线性结构从机制层面确保引导过程的稳定性。

> **注意**：该 Lyapunov 分析假设模型速度场可微，实际大规模潜在扩散模型中计算雅可比矩阵开销较大，论文未给出高效近似方案，这是实际部署的关键挑战。

![[assets/figures/papers/paper_list_l9_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_CFG_Ctrl_Control/figures/002_Table_1.jpg]]
*Table 1: Typical CFG variants under CFG-Ctrl formulation. We summarize the key components of various methods under the control formulation, along with their corresponding types of control interpretations*

## 实验与关键发现

### 一、主实验结果

CFG-Ctrl 在三个主流文本到图像（T2I）流匹配模型上进行了系统评估：Stable Diffusion 3.5、Flux-dev 和 Qwen-Image。所有方法均使用相同的评估设置与 MS-COCO 2017 验证集提示，确保比较公平。**Table 2** 汇总了多维度的定量对比，覆盖生成质量、语义对齐、人类偏好和美学评分共七项指标。

![[assets/figures/papers/paper_list_l9_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_CFG_Ctrl_Control/figures/003_Table_2.jpg]]
*Table 2: Quantitative evaluation of CFG methods. Lower (↓) FID and higher (↑) CLIP, Aesthetic, ImageReward, PickScore, HPSv2, HPSv2.1 and MPS scores indicate better performance. Note that Qwen-Image preserves natural image statistics, yielding the lowest FID*

**Table 2 定量评估结果**

在 Stable Diffusion 3.5 主干上，SMC-CFG 的 FID 从标准 CFG 的 21.421 降至 **20.044**（降幅 1.377），CLIP Score 从 0.3681 微升至 **0.3694**，ImageReward 则从 0.8889 显著提升至 **0.9486**（增幅 0.0597）。这一趋势在 Flux-dev 上得到复现：FID 从 27.323 降至 **26.398**，CLIP Score 从 0.3692 升至 **0.3743**。在 Qwen-Image 上，SMC-CFG 的 FID 从 35.431 降至 **33.371**，降幅达 2.060，为所有模型中最大。需要注意的是，Qwen-Image 本身在无条件生成时保留了更自然的图像统计特性，因此其基础 FID 较低，不同模型间的 FID 不可直接横向比较，但各模型内部的相对提升趋势一致，验证了方法的跨模型有效性。

除 FID 和 CLIP Score 外，SMC-CFG 在 Aesthetic Score、PickScore、HPSv2、HPSv2.1 和 MPS 等指标上也一致优于标准 CFG 及其他变体，表明该方法在提升语义对齐的同时，并未以牺牲图像美学质量为代价。

**定性视觉对比**

**Figure 2** 展示了不同 T2I 模型上 CFG 与 SMC-CFG 的生成效果对比。SMC-CFG 在位置关系、文本生成和细节物体表现方面均展现出明显优势。**Figure 3** 进一步比较了 SMC-CFG 与其他流匹配引导变体在复杂提示上的鲁棒性：在涉及相对位置、服装风格和人体动作等挑战性场景中，基线方法容易产生不合理输出，而 SMC-CFG 保持了稳健的文本一致性。

### 二、引导尺度鲁棒性分析

标准 CFG 在高引导尺度 w 下容易出现色彩过饱和、伪影和语义退化，这是线性比例控制在高增益下的固有缺陷。**Figure 4** 给出了不同 CFG 尺度下的视觉对比：随着 w 增大，标准 CFG 的图像逐渐出现过饱和和结构扭曲，而 SMC-CFG 在相同尺度范围内保持了稳定的图像质量和语义一致性。这一结果直接验证了滑模控制的非线性校正机制在抑制高增益振荡方面的有效性——切换项 $-\mathbf{K} \cdot \mathrm{sign}(\mathbf{s}(t))$ 在误差偏离滑模面时施加强制校正，将生成轨迹约束在稳定语义流形附近。

### 三、消融实验

**Table 3** 报告了滑模面参数 $\lambda$ 和切换增益 $k$ 的消融结果，涵盖 FID、CLIP、Aesthetic 和 ImageReward 四项指标。

**滑模面参数 $\lambda$ 的影响**

$\lambda$ 控制理想误差动力学 $\dot{\mathbf{e}}(t) = -\lambda \mathbf{e}(t)$ 的收敛速率。实验表明：
- $\lambda$ 过小（如 $\lambda=1$）时，收敛速度慢，语义对齐提升有限，CLIP Score 偏低；
- $\lambda$ 过大（如 $\lambda=10$）时，滑模面过于陡峭，切换控制的强制校正过于激进，破坏引导稳定性，导致 FID 和 Aesthetic Score 下降；
- $\lambda=5$ 在 FID 和 CLIP 上取得最佳综合效果，验证了适中的收敛速率可在语义对齐与生成质量之间取得平衡。

**切换增益 $k$ 的影响**

$k$ 主导趋近律的强度，直接决定切换控制项 $\Delta\mathbf{e} = -k \cdot \mathrm{sign}(\mathbf{s}(t))$ 的校正幅度：
- $k=0.1$ 时校正过弱，语义对齐提升有限；
- $k=0.4$ 时达到最佳平衡，ImageReward 和 CLIP Score 均显著改善；
- $k \geq 0.7$ 时，过强的切换控制引起采样过程中的抖振（chattering），导致 Aesthetic Score 下降，尽管语义对齐指标仍保持较高水平。

这一消融结果揭示了 SMC-CFG 的核心权衡机制：适中的超参数配置（$\lambda=5, k=0.4$）能够在滑模面的收敛速度与切换控制的平滑性之间取得最优折中。

### 四、方法与基线对比分析

**Table 1** 在 CFG-Ctrl 统一框架下对各方法进行了控制论解读。标准 CFG 本质上是固定增益的比例控制器（P-control）；Weight Scheduler（Wang et al., TMLR 2024）引入时变增益 $w(t)$，属于增益调度比例控制；APG（Sadat et al., ICLR 2024）通过投影矩阵 $\Pi_t$ 选择性增强条件方向分量，属于基于投影的反馈控制；CFG-Zero\*（Fan et al., arXiv 2025）和 Rectified-CFG++（Saini et al., arXiv 2025）分别对应投影反馈控制和模型预测控制风格的引导。

SMC-CFG 与上述方法的本质区别在于引入了**非线性滑模控制**：通过在语义误差上叠加切换校正项 $\Delta\mathbf{e} = -k \cdot \mathrm{sign}(\mathbf{s}(t))$，将线性反馈升级为具有有限时间收敛保证的非线性控制律。Lyapunov 稳定性分析（Eq. 20）证明，在速度场可微的假设下，滑模面 $\mathbf{s}(t)$ 的能量函数 $V(\mathbf{s}) = \frac{1}{2}\|\mathbf{s}\|^2$ 单调衰减，系统状态将在有限时间内收敛至 $\mathbf{s}=0$，即理想语义平衡流形。

### 五、局限性与失败模式

尽管 SMC-CFG 在多个指标上表现优异，但存在以下局限：

1. **超参数敏感性**：性能对 $\lambda$ 和 $k$ 较为敏感，需针对不同模型和任务进行调参。消融实验已表明，极端参数值（如 $\lambda$ 过大或 $k \geq 0.7$）会导致引导不稳定或图像质量下降。
2. **理论假设与实际部署的差距**：Lyapunov 稳定性分析依赖模型速度场的可微性假设，而实际大规模潜在扩散模型中计算速度雅可比矩阵开销较大。论文未给出高效近似方法，这在高维潜在空间中的实际部署构成关键挑战。
3. **计算开销**：SMC-CFG 需要维护历史误差以构造滑模面 $\mathbf{s}(t) = \dot{\mathbf{e}}(t) + \lambda \mathbf{e}(t)$（离散近似为 $\mathbf{s}(t) = (\mathbf{e}(t) - \mathbf{e}(t+1)) + \lambda \cdot \mathbf{e}(t+1)$），相比标准 CFG 增加了少量额外计算和存储开销，但论文未对此进行定量分析。

![[assets/figures/papers/paper_list_l9_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_CFG_Ctrl_Control/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative comparison with baseline methods. For challenging scenarios including relative positions, clothing styles, and human actions, baseline methods produce irrational outputs, while SMC-CFG preserves robust text consistency*

![[assets/figures/papers/paper_list_l9_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_CFG_Ctrl_Control/figures/006_Table_3.jpg]]
*Table 3: Ablation study on hyperparameter λ and k. We conduct ablation across various hyperparameter settings in four metrics: FID, CLIP, Aesthetic (Aesth), and ImageReward (ImgRwd), respectively measuring generation quality, semantic alignment, aesthetic level, and human preference*

## 定位与知识库关联

### 1. 控制理论视角下的 CFG 方法谱系

CFG-Ctrl 的核心贡献在于将流匹配模型中的免分类器引导重新建模为一阶反馈控制系统，并以此统一框架解读现有 CFG 变体的控制本质。在此框架下，引导过程被抽象为三个关键组件：**语义误差信号** e(t)（条件与无条件速度差）、**引导调度矩阵** K_t（增益结构）和**方向算子** Π_t（误差投影方式），最终控制律表示为 u_t = K_t Π_t(e(t))（Eq. 10）。

基于这一统一视角，现有方法可被清晰地归入以下控制类型谱系（参见 Table 1）：

| 控制类型 | 代表方法 | 核心机制 | 局限性 |
|---------|---------|---------|--------|
| **比例控制（P-Control）** | 标准 CFG（Ho & Salimans, arXiv 2022） | 固定标量增益 w，K_t = w, Π_t = I | 高增益下非线性发散、过饱和 |
| **增益调度（Gain Scheduling）** | Weight Scheduler（Wang et al., TMLR 2024） | 时变标量增益 w(t)，K_t = w(t), Π_t = I | 仍为线性控制，未改变系统动力学结构 |
| **投影控制（Projection Control）** | APG（Sadat et al., ICLR 2024） | 矩阵增益 K_t = w[I, ηI]，方向算子 Π_t = I - P_t，抑制平行分量过饱和 | 本质仍为线性组合，无法处理强非线性振荡 |
| **投影控制（流匹配优化）** | CFG-Zero*（Fan et al., arXiv 2025） | 针对流匹配的投影反馈，优化引导尺度 | 同样受限于线性投影框架 |
| **模型预测控制风格** | Rectified-CFG++（Saini et al., arXiv 2025） | 结合校正流的模型预测控制风格引导 | 计算开销较大，缺乏收敛性理论保证 |
| **滑模控制（Sliding Mode Control）** | **SMC-CFG（本文）** | 非线性切换控制，在误差上叠加 Δe = -k·sign(s(t))，强制系统沿滑模面收敛 | 对超参数敏感，需手动调参 |

**关键区分**：上述所有基线方法均属于**线性反馈控制**范畴——无论是固定增益、时变增益还是投影矩阵，控制输入始终是误差信号的线性函数。SMC-CFG 首次引入**非线性切换控制**，通过符号函数 sign(s(t)) 产生不连续的控制力，从根本上改变了系统的收敛动力学。

### 2. 从线性到非线性：控制机制的质变

标准 CFG 及其变体在 (e, ė) 相平面上的理想行为是线性收敛至原点（Figure 1 左），但在实际高引导尺度下，生成动力学呈现强非线性，导致沿相平面的**振荡**、**过冲**和**发散**。这一现象的根本原因在于：线性控制器无法在高增益下抑制模型容量增大带来的非线性效应。

SMC-CFG 通过定义**指数型滑模面** s(t) = ė(t) + λe(t)（Eq. 19），将控制目标从“驱动误差至零”转变为“驱动系统状态至滑模面 s=0”。一旦系统到达滑模面，误差动力学自动退化为 ė = -λe，即理想的指数收敛。切换控制律 Δe = -k·sign(s(t)) 的作用是：无论当前状态偏离滑模面多远，始终施加指向滑模面的最大校正力，确保**有限时间到达**。

这一设计的理论保障来自 **Lyapunov 稳定性分析**（Eq. 20）：定义能量函数 V(s) = ½‖s‖²，其导数 V̇ = sᵀṡ < 0 保证单调能量衰减，从而证明系统状态必然在有限时间内收敛至滑模面 s=0，并沿该流形滑向语义平衡点。

### 3. 适用边界与约束条件

**模型兼容性**：SMC-CFG 在 SD3.5、Flux-dev 和 Qwen-Image 三个不同架构的流匹配主干上均取得一致提升（Table 2），表明该方法对模型架构具有较好的泛化性。但需注意，Qwen-Image 本身在无条件生成时保留了更自然的图像统计特性，因此其基础 FID 较低，跨模型间的 FID 绝对值不可直接比较，相对提升趋势才是有效信号。

**引导尺度鲁棒性**：SMC-CFG 在较宽的引导尺度范围内保持稳定的图像质量和语义一致性，缓解了标准 CFG 在高 w 下的过饱和与伪影问题（Figure 4）。这一特性对于需要强语义控制的应用场景（如复杂组合提示、文本渲染）尤为重要。

**计算开销**：SMC-CFG 仅在标准 CFG 的基础上增加了滑模面构造和切换控制计算两步（Algorithm 1 lines 10-12），不涉及额外的模型前向传播或梯度计算，因此推理开销几乎与标准 CFG 持平。但 Lyapunov 分析依赖模型速度场的可微性假设，实际大规模潜在扩散模型中计算雅可比矩阵开销较大，论文未给出高效近似方法，这在高维潜在空间的实际部署中仍是一个开放挑战。

### 4. 局限性与开放问题

**超参数敏感性**：消融实验（Table 3）表明，SMC-CFG 的性能对滑模面参数 λ 和切换增益 k 较为敏感。λ 过小则收敛缓慢，过大则滑模面过于陡峭，破坏引导稳定性；k 过小（0.1）校正效果微弱，k 过大（≥0.7）则引起采样过程的“抖振”（chattering），降低美学评分。当前需针对不同模型和任务手动调参，缺乏自适应机制。

**控制视角的推广潜力**：将扩散引导视为控制问题的视角是否可推广至视频生成、3D 生成等多模态模型，并在更高维的状态空间中保持稳定性保障，是一个值得探索的方向。

**自适应滑模设计**：能否设计根据当前误差状态在线调节 λ 和 k 的自适应机制，是减少手动调参负担、提升方法实用性的关键。这需要在不显著增加计算开销的前提下，实现对滑模面参数和切换增益的动态优化。

**高维雅可比近似**：SMC-CFG 的理论分析依赖速度场可微性，但在实际高维潜在空间中高效计算或近似滑模面所需的速度雅可比矩阵，是推动该方法从理论走向大规模部署的核心工程挑战。

## 原文 PDF

![[paperPDFs/CVPR_2026/CFG_Ctrl_Control_Based_Classifier_Free_Diffusion_Guidance.pdf]]
