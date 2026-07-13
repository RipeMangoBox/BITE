---
title: Delta Rectified Flow Sampling for Text-to-Image Editing
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Delta_Rectified_Flow_Sampling_for_Text_to_Image_Editing.pdf
project_link: null
code_link: "https://github.com/Harvard-AI-and-Robotics-Lab/DeltaRectifiedFlowSampling"
aliases:
- DRFSD
- DRFSTIE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 时间依赖的偏移系数 c_t，该系数控制编辑路径的直线程度、更新幅度和误差传播。c_t=0 还原 DDS，c_t=t 还原 FlowEdit，而中间值实现了保持背景细节与语义对齐的最佳平衡。
primary_logic: 通过显式建模源和目标速度场之间的残差差异（而非仅目标速度），DRFS 消除了共享分量，从而保留未编辑区域；同时引入基于 c_t 的偏移项，将噪声潜在变量推向目标分布的正确轨迹，减轻模型-数据不匹配并稳定优化。
claims:
- DRFS 通过引入源-目标残差能量函数，使梯度在不相关区域抵消，缓解过度平滑。
- 偏移项 c_t 显著改善编辑质量：c_t=0 时背景保留最佳但语义对齐不足，c_t ≃ (1-t)t 实现最佳平衡。
- DRFS 统一了 DDS 和 FlowEdit：设置 c_t=0 还原 DDS，设置 c_t=t 还原 FlowEdit，提供归纳性理论支持。
- 在 PIE 基准上，DRFS 在 SD3 上实现了最佳的编辑区域 CLIP 相似性（23.83），同时背景保留（LPIPS 93.81）远优于 iRFDS（186.39）。
---

# Delta Rectified Flow Sampling for Text-to-Image Editing

> [!tip] 核心洞察
> 通过显式建模源和目标速度场之间的残差差异（而非仅目标速度），DRFS 消除了共享分量，从而保留未编辑区域；同时引入基于 c_t 的偏移项，将噪声潜在变量推向目标分布的正确轨迹，减轻模型-数据不匹配并稳定优化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 用于文本到图像编辑的Delta校正流采样 |
| 英文题名 | Delta Rectified Flow Sampling for Text-to-Image Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2509.05342) · [Code](https://github.com/Harvard-AI-and-Robotics-Lab/DeltaRectifiedFlowSampling) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Delta Rectified Flow Sampling (DRFS) |
| Dataset | PIE Benchmark, PIE |

> [!tip] 效果简介
> - PIE Benchmark (SD3) 上，LPIPS ×10³ (↓) 93.81 vs 186.39 (iRFDS) (-92.58)；MSE ×10⁴ (↓) 67.49 vs 179.76 (iRFDS) (-112.27)；SSIM ×10² (↑) 84.85 vs 74.59 (iRFDS) (+10.26)。
> - PIE (Change Object Pose, SD3) 上，LPIPS ×10³ (↓) 91.4 vs 102.6 (FlowEdit) (-11.2)。
> - PIE (Change Image Style, SD3) 上，CLIP edited (↑) 23.26 vs 22.87 (FlowEdit) (+0.39)。

## 概要

文本到图像编辑的核心挑战在于：如何在根据目标文本语义修改图像内容的同时，最大限度地保留源图像中不应被编辑区域的细节与结构。现有基于校正流（Rectified Flow）模型的编辑方法，如 RFDS，通过直接优化目标速度场与理想数据动态之间的差异来驱动编辑，但这一过程会不加区分地优化整幅图像，导致严重的**过度平滑**与**细节丢失**（Figure 1）。

本文提出 **Delta Rectified Flow Sampling (DRFS)**，从两个层面解决上述瓶颈：

1. **残差能量函数**：DRFS 不再单独匹配目标速度，而是显式建模源速度场与目标速度场之间的**残差差异**。由于源与目标在未编辑区域共享相同的速度分量，残差计算使这些共享分量的梯度相互抵消，从而天然地保护背景区域不被修改。

2. **时间依赖的偏移项**：DRFS 在目标潜在变量的前向加噪过程中引入由系数 $c_t$ 控制的偏移项 $\hat{x}_t^{\mathrm{tgt}} = a_t x_0^{\mathrm{tgt}} + b_t \varepsilon + c_t (x_0^{\mathrm{tgt}} - x_0^{\mathrm{src}})$。该偏移将评估点推向目标分布的正确轨迹，缓解模型-数据分布不匹配，使优化过程更稳定、编辑路径更直接。

DRFS 在方法谱系中占据独特位置：它统一了此前两种重要的校正流编辑范式——当 $c_t=0$ 时 DRFS 退化为 **DDS**，当 $(a_t, b_t, c_t) = (1-t, t, t)$ 时退化为 **FlowEdit**。这意味着 DRFS 为这些方法提供了归纳性的理论框架，并通过调节 $c_t$ 在“背景保真度”与“语义对齐度”之间实现了它们各自无法达到的最优平衡。

在 **PIE 基准**上的定量评估表明，DRFS 在 SD3 模型上取得了编辑区域 CLIP 相似性 23.83 的最佳成绩，同时背景保留指标 LPIPS 仅为 93.81，远优于同类蒸馏编辑方法 iRFDS 的 186.39（Table 1）。消融实验进一步证实：$c_t \simeq (1-t)t$ 的抛物线调度是实现编辑质量与保真度最佳折中的关键因素，而降序时间步调度器则通过由粗到细的优化策略进一步提升了结果的一致性。

### 从扩散模型到校正流：编辑范式的演进

文本到图像编辑的核心挑战在于，如何在精确修改目标语义的同时，最大限度地保留源图像的无关区域与纹理细节。早期方法主要建立在扩散模型（Diffusion Models）之上，通过反演（inversion）将源图像映射回噪声空间，再以目标提示为条件进行去噪重建。代表性工作包括 **PnP-Inv**、**P2P**、**Null-text Inv** 等，它们依赖注意力注入或空文本优化来维持结构一致性。然而，扩散模型的反演过程本身存在不可忽视的重建误差——即使不改变提示，反演-重建循环也会引入伪影和细节丢失。这一瓶颈催生了基于校正流模型（Rectified Flow Models）的编辑方法。

校正流模型将生成过程定义为常微分方程（ODE）：$\mathrm{d}x_t = v_\theta(x_t, t)\,\mathrm{d}t$，其中 $t:1\to0$，$x_1\sim p_1$。其训练目标为条件流匹配损失：

$$\mathcal{L}(\theta) = \mathbb{E}_{t,x_t}\left[\left\|v_\theta(a_t x_0 + b_t x_1, t) - (\dot{a}_t x_0 + \dot{b}_t x_1)\right\|^2\right]$$

由于校正流在噪声与数据之间学习了一条近乎直线的传输路径，其反演精度显著优于扩散模型（见原文 Figure S.1 的重建误差对比）。这一特性催生了 **RF-Inv**、**RF-Solver**、**FireFlow** 等基于校正流的反演编辑方法，以及无需反演的 **FlowEdit**、**FTEdit**、**DNAEdit** 等直接编辑方法。

### RFDS 的过度平滑困境

在诸多校正流编辑方法中，Rectified Flow Distillation Sampling（RFDS）及其蒸馏变体 **iRFDS** 通过优化能量函数直接更新目标潜在变量 $x_0^{\mathrm{tgt}}$，无需完整的反演-采样循环。其能量函数最小化目标速度场 $v_\theta(x_t^{\mathrm{tgt}})$ 与数据动力学 $\dot{x}_t^{\mathrm{tgt}}$ 之间的差异：

$$\mathcal{E}_{\mathrm{RFDS}} = \mathbb{E}\left[\left\|v_\theta(x_t^{\mathrm{tgt}}) - \dot{x}_t^{\mathrm{tgt}}\right\|^2\right]$$

然而，这一设计的根本缺陷在于：**能量函数不加区分地优化整个图像**。当编辑任务仅需修改局部区域（如将“棕马”变为“斑马”）时，RFDS 的梯度同时作用于编辑区域和背景区域，导致后者被不必要的更新所破坏。如 Figure 1 所示，RFDS 编辑结果呈现出明显的过度平滑（over-smoothing）和纹理丢失——马匹的毛发细节、草地的纹理在编辑过程中被抹平。定量上，iRFDS 在 PIE 基准上的背景保留指标 LPIPS 高达 186.39（越低越好），远劣于本文提出的 DRFS（93.81），印证了这一问题的严重性。

### 模型-数据不匹配：被忽视的分布偏移

RFDS 过度平滑的深层原因在于**模型-数据不匹配（model-data mismatch）**。具体而言，RFDS 在源潜在变量 $x_t^{\mathrm{src}}$ 的位置上评估目标速度场 $v_\theta(\cdot)$，但该位置实际上位于源分布的前向轨迹上，而非理想编辑结果 $x_0^\star$ 所对应的目标分布轨迹。这种“在错误位置问正确问题”的做法，使得速度预测本身就带有系统性偏差，优化过程因此将噪声和误差持续注入 $x_0^{\mathrm{tgt}}$，最终表现为细节丢失。

### DRFS 的动机与核心思路

针对上述两个瓶颈，本文提出 **Delta Rectified Flow Sampling（DRFS）**，其设计动机可概括为两点：

1. **消除共享分量，保护未编辑区域**：通过显式建模源速度场 $v_\theta(x_t^{\mathrm{src}})$ 与目标速度场 $v_\theta(\hat{x}_t^{\mathrm{tgt}})$ 之间的**残差差异**（delta），而非仅优化目标速度本身，DRFS 使梯度在不相关区域自然抵消。如 Figure S4 所示，DRFS 梯度在背景区域趋近于零，仅在编辑区域产生有效更新。

2. **引入时间依赖偏移，校正分布轨迹**：DRFS 引入一个由系数 $c_t$ 控制的偏移项 $c_t(x_0^{\mathrm{tgt}} - x_0^{\mathrm{src}})$，将目标潜在变量的评估点推向目标分布的正确轨迹（见 Figure 2 示意）。这一偏移项直接缓解了模型-数据不匹配问题，使速度场评估更加精确，从而稳定优化过程并提升编辑质量。

值得注意的是，DRFS 在理论上统一了两种看似迥异的方法：当 $c_t=0$ 时，DRFS 退化为 DDS（Delta Denoising Score）；当 $c_t=t$ 时，DRFS 退化为 FlowEdit。这一统一性不仅提供了归纳性的理论支撑，也揭示了偏移系数 $c_t$ 作为**编辑路径直线度与更新幅度的控制旋钮**的关键角色（见 Figure 3）。通过选择中间值 $c_t \simeq (1-t)t$，DRFS 在语义对齐与背景保留之间取得了最佳平衡。

## 核心方法与创新机理

DRFS 的核心创新在于两个相互协同的设计：**残差式能量函数**与**时间依赖的偏移项**。二者共同解决了校正流编辑中过度平滑与语义对齐不足的矛盾。

### 残差式能量函数：消除共享分量，保留背景

RFDS 的能量函数仅最小化目标速度场与数据动力学之间的残差，即 $\mathcal{E}_{\mathrm{RFDS}} = \mathbb{E}[||v_\theta(x_t^{\mathrm{tgt}}) - \dot{x}_t^{\mathrm{tgt}}||^2]$。这种不加区分的优化方式将编辑梯度施加于整幅图像，导致未编辑区域同样被修改，产生过度平滑和细节丢失（Figure 1）。

DRFS 将能量函数重构为源-目标速度场的**残差差异**：

$$\mathcal{E}_{\mathrm{DRFS}} = \mathbb{E}_{t,\varepsilon}\Big[||v_\theta(\hat{x}_t^{\mathrm{tgt}}) - v_\theta(x_t^{\mathrm{src}}) - (\dot{\hat{x}}_t^{\mathrm{tgt}} - \dot{x}_t^{\mathrm{src}})||^2\Big]$$

其核心机理在于：源与目标速度场中共享的分量（对应未编辑区域）在相减时相互抵消，梯度仅在编辑相关区域保持活跃。Figure S4 的可视化证实了 DRFS 梯度在不相关区域自然抵消。这一设计使 DRFS 在 PIE 基准上实现背景保留指标的显著提升——LPIPS 从 iRFDS 的 186.39 降至 93.81，MSE 从 179.76 降至 67.49，SSIM 从 74.59 升至 84.85（Table 1）。

### 偏移项 $c_t$：校正模型-数据不匹配，平衡保留与对齐

编辑过程中，目标潜在变量 $\hat{x}_t^{\mathrm{tgt}}$ 的评估点并不位于理想编辑轨迹的前向后验上，导致模型-数据不匹配。DRFS 在标准前向加噪的基础上引入偏移项：

$$\hat{x}_t^{\mathrm{tgt}} = a_t x_0^{\mathrm{tgt}} + b_t \varepsilon + c_t (x_0^{\mathrm{tgt}} - x_0^{\mathrm{src}})$$

其中 $c_t$ 是时间依赖的偏移系数，控制编辑路径的直线程度、更新幅度和误差传播。实际采用 $c_t = \frac{k}{T}t \simeq (1-t)t$ 的调度策略——优化初期 $c_t \approx 0$，允许大范围几何变化；中期 $c_t$ 增大，将潜在变量推向目标分布的正确轨迹，稳定优化。

消融实验（Table 2）揭示了 $c_t$ 的关键调节作用：
- **$c_t = 0$**：背景保留最优（PSNR 28.63, LPIPS 44.66），但语义对齐不足（Edited CLIP 22.53），因为缺少将编辑路径推向目标分布的驱动力。
- **$c_t \simeq (1-t)t$**：在语义对齐（Edited CLIP 23.83）与背景保留之间取得最佳平衡，实现最高的编辑区域 CLIP 相似性。
- **$c_t = t$**：退化为 FlowEdit，编辑强度增大但背景保留下降。

Figure 3 从几何角度量化了这一效应：更大的 $c_t$ 产生更直的编辑轨迹（路径-弦比 $S_R$ 降低），同时放大更新幅度 $||v_\theta(\hat{x}_t^{\mathrm{tgt}}) - v_\theta(x_t^{\mathrm{src}})||^2$。

### 理论统一：DDS 与 FlowEdit 的特例

DRFS 提供了对现有方法的归纳性理论支持。通过噪声-速度等价关系，可以证明：
- **$c_t = 0$ 时 DRFS 还原为 DDS**：残差能量函数退化为标准扩散模型的得分蒸馏损失。
- **$(a_t, b_t, c_t) = (1-t, t, t)$ 时 DRFS 还原为 FlowEdit**：偏移项完全补偿了评估点偏差，等价于 FlowEdit 的 ODE 编辑动力学 $dx_0^{\mathrm{tgt}}(t) = [v_\theta(x_0^{\mathrm{tgt}}(t) + x_t^{\mathrm{src}} - x_0^{\mathrm{src}}, t, \varphi^{\mathrm{tgt}}) - v_\theta(x_t^{\mathrm{src}}, t, \varphi^{\mathrm{src}})]dt$。

这一统一框架揭示了 DDS 和 FlowEdit 分别是偏移系数空间中的两个端点，而 DRFS 通过中间值 $c_t \simeq (1-t)t$ 实现了二者的优势互补。

### 辅助设计：降序时间步调度

DRFS 采用从高噪声（$t \approx 1$）到低噪声（$t \approx 0$）的降序时间步调度，替代 DDS 的均匀随机采样。这一由粗到细的优化策略允许早期进行大范围几何变化，后期细化颜色和纹理细节，产生更一致的编辑结果（Figure 6）。

### 局限与待验证方向

- DRFS 仅适用于校正流模型，无法直接迁移至标准扩散模型。
- $c_t$ 的调度仍依赖经验设计，缺乏自动适应机制。
- 当编辑需要大幅改变结构或面对分布外图像时，编辑强度不足。

DRFS 是一个无需训练的文本驱动图像编辑方法，专为校正流（Rectified Flow）模型设计。其整体流程以源图像和一对文本提示为输入，通过迭代优化目标潜在变量 $x_0^{\mathrm{tgt}}$ 来生成编辑结果。核心 pipeline 由以下模块串联构成：

**1. 任务定义与初始化。** 用户提供源图像 $x_0^{\mathrm{src}}$、源提示 $\varphi^{\mathrm{src}}$ 和目标提示 $\varphi^{\mathrm{tgt}}$。目标潜在变量 $x_0^{\mathrm{tgt}}$ 被初始化为 $x_0^{\mathrm{src}}$ 的副本，优化过程直接在该潜在空间中进行（$\Theta = x_0^{\mathrm{tgt}}$）。

**2. 偏移状态构造。** 在每一步优化中，随机采样时间步 $t$ 和噪声 $\varepsilon$，根据公式
$$\hat{x}_t^{\mathrm{tgt}} = a_t x_0^{\mathrm{tgt}} + b_t \varepsilon + c_t (x_0^{\mathrm{tgt}} - x_0^{\mathrm{src}})$$
构造偏移后的目标潜在变量。其中 $a_t, b_t$ 为校正流的标准前向加噪系数，$c_t$ 是本文引入的时变偏移系数，其作用是将评估点推向目标分布的正确轨迹，缓解模型-数据不匹配。源潜在变量 $x_t^{\mathrm{src}}$ 则按标准方式构造（$c_t=0$）。

**3. DRFS 能量函数计算。** 将 $\hat{x}_t^{\mathrm{tgt}}$ 和 $x_t^{\mathrm{src}}$ 分别送入预训练的校正流速度场 $v_\theta$，在目标提示和源提示条件下计算速度预测。能量函数定义为源-目标速度残差的差异：
$$\mathcal{E}_{\mathrm{DRFS}} = \mathbb{E}_{t,\varepsilon} \Big[ \big\| v_\theta(\hat{x}_t^{\mathrm{tgt}}) - v_\theta(x_t^{\mathrm{src}}) - (\dot{\hat{x}}_t^{\mathrm{tgt}} - \dot{x}_t^{\mathrm{src}}) \big\|^2 \Big]$$
该设计的核心洞察是：通过显式建模源与目标速度场的残差差异，共享的速度分量被抵消，梯度在不相关区域自然衰减，从而保留未编辑区域的细节。

**4. 梯度近似与更新。** 遵循现有实践，将网络雅可比近似为单位矩阵，得到简化梯度：
$$\nabla_{\Theta} \mathcal{E}_{\mathrm{DRFS}} = \mathbb{E}_{t,\varepsilon} \Big[ w_{\mathrm{DRFS}}(t) \big( v_\theta(\hat{x}_t^{\mathrm{tgt}}) - v_\theta(x_t^{\mathrm{src}}) - (\dot{a}_t + \dot{c}_t)(x_0^{\mathrm{tgt}} - x_0^{\mathrm{src}}) \big) \Big]$$
其中 $w_{\mathrm{DRFS}}(t) = 2(a_t + c_t - \dot{a}_t - \dot{c}_t)$ 为时间依赖的权重函数。该梯度直接用于通过 SGD 优化器更新 $x_0^{\mathrm{tgt}}$。

**5. 降序时间步调度。** 时间步从高噪声（$t \approx 1$）到低噪声（$t \approx 0$）降序采样，实现由粗到细的优化：早期允许大幅度几何变化，后期细化颜色和纹理。

**6. 关键控制变量 $c_t$。** 偏移系数采用递增调度 $c_t = \frac{k}{T} t \simeq (1-t)t$，其中 $k$ 为当前优化步数，$T$ 为总步数。该设计在优化初期保持低偏移（$c_t \approx 0$），此时 DRFS 退化为 DDS，最大化背景保留；随着优化推进，$c_t$ 逐渐增大，增强编辑路径的直线性和更新幅度，提升语义对齐。消融实验证实，$c_t=0$ 时背景保留最佳但语义对齐不足（Edited CLIP 22.53），$c_t \simeq (1-t)t$ 在语义对齐（Edited CLIP 23.83）与背景保留之间取得最佳平衡。

**输入输出流总结：** 输入为源图像、源提示、目标提示；输出为编辑后的图像 $x_0^{\mathrm{tgt}}$。整个流程无需训练、无需模型结构修改、无需反演，仅通过迭代优化单一潜在变量完成编辑。

![[assets/figures/papers/paper_list_l2304_https_arxiv_org_abs_2509_05342/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between RFDS and DRFS (ours). Source prompt: Brown horse walking in a grassy meadow with an autumn forest backdrop and target prompt: Zebra walking in a grassy meadow with an autumn forest backdrop. As shown in (b) and (c), RFDS results in over-smoothing and detail loss. In contrast, DRFS (d) preserves textures*

### 问题定位：RFDS 为何导致过度平滑？

DRFS 的出发点是对 **RFDS（Rectified Flow Distillation Sampling）** 编辑失败的诊断。在 RFDS 框架下，编辑能量函数仅匹配目标提示下的速度场：

$$ \mathcal{E}_{\mathrm{RFDS}} = \mathbb{E}_{t,\varepsilon}\left[\|v_\theta(x_t^{\mathrm{tgt}}) - \dot{x}_t^{\mathrm{tgt}}\|^2\right] $$

该能量函数不加区分地优化整个图像，将源图像的所有像素推向目标分布。其梯度包含两个分量：一个驱动编辑的“信号”项，和一个对所有区域（包括应保持不变的背景）都施加更新的“噪声”项。由于后者在空间上均匀作用，RFDS 不可避免地在编辑区域之外产生**过度平滑**和**细节丢失**（见图 1 中 RFDS 结果）。

### 核心模块一：Delta 能量函数——残差差异建模

DRFS 的核心创新是用**源-目标速度残差的差异**替代 RFDS 中的绝对目标速度匹配。定义源残差与目标残差：

$$ r^{\mathrm{src}} = v_\theta(x_t^{\mathrm{src}}) - \dot{x}_t^{\mathrm{src}}, \quad r^{\mathrm{tgt}} = v_\theta(x_t^{\mathrm{tgt}}) - \dot{x}_t^{\mathrm{tgt}} $$

DRFS 能量函数惩罚两者之差：

$$ \mathcal{E}_{\mathrm{DRFS}} = \mathbb{E}_{t,\varepsilon}\left[\|r^{\mathrm{tgt}} - r^{\mathrm{src}}\|^2\right] $$

展开后得到等价形式：

$$ \mathcal{E}_{\mathrm{DRFS}}(x_0^{\mathrm{tgt}}, x_0^{\mathrm{src}}, \varphi^{\mathrm{tgt}}, \varphi^{\mathrm{src}}) = \mathbb{E}_{t,\varepsilon}\left[\|v_\theta(\hat{x}_t^{\mathrm{tgt}}) - v_\theta(x_t^{\mathrm{src}}) - (\dot{\hat{x}}_t^{\mathrm{tgt}} - \dot{x}_t^{\mathrm{src}})\|^2\right] \tag{7} $$

其中各变量含义：
- $v_\theta(\cdot)$：校正流模型预测的速度场
- $x_t^{\mathrm{src}}$：源图像沿前向加噪路径的潜在变量，$x_t^{\mathrm{src}} = a_t x_0^{\mathrm{src}} + b_t \varepsilon$
- $\hat{x}_t^{\mathrm{tgt}}$：偏移校正后的目标潜在变量（见下节）
- $\dot{x}_t^{\mathrm{src}}, \dot{\hat{x}}_t^{\mathrm{tgt}}$：对应前向路径的解析时间导数
- $\varphi^{\mathrm{src}}, \varphi^{\mathrm{tgt}}$：源提示与目标提示的文本嵌入

**关键机制**：当源与目标的速度场共享分量时（如背景区域），$v_\theta(x_t^{\mathrm{tgt}}) - v_\theta(x_t^{\mathrm{src}})$ 中这些共享分量相互抵消，梯度仅作用于编辑相关区域。Figure S4 的可视化证实了 DRFS 梯度在不相关区域的抵消效应，从根本上缓解了过度平滑。

### 核心模块二：偏移项——校正模型-数据不匹配

直接使用 $x_t^{\mathrm{tgt}}$ 评估目标速度场存在一个隐含问题：$x_t^{\mathrm{tgt}}$ 沿源图像的前向路径构造，而理想编辑结果的前向路径应更接近目标分布。这种**模型-数据不匹配**导致速度评估不准确，优化不稳定。

DRFS 引入一个时间依赖的偏移项，将目标潜在变量推向更合理的位置：

$$ \hat{x}_t^{\mathrm{tgt}} = a_t x_0^{\mathrm{tgt}} + b_t \varepsilon + c_t (x_0^{\mathrm{tgt}} - x_0^{\mathrm{src}}) \tag{6} $$

其中：
- $a_t, b_t$：校正流的前向加噪系数（如 $a_t=1-t, b_t=t$）
- $c_t$：**偏移系数**，控制沿源-目标差异方向 $(x_0^{\mathrm{tgt}} - x_0^{\mathrm{src}})$ 的偏移量
- $x_0^{\mathrm{tgt}}$：当前优化的目标潜在变量（初始化为 $x_0^{\mathrm{src}}$）
- $\varepsilon \sim \mathcal{N}(0, I)$：标准高斯噪声

**$c_t$ 的控制作用**（见图 2 和图 3）：
- $c_t = 0$：无偏移，退化为 DDS 形式，背景保留最佳但语义对齐不足
- $c_t > 0$：将 $\hat{x}_t^{\mathrm{tgt}}$ 推向目标分布轨迹，使速度评估更准确，编辑路径更直（图 3a），更新幅度增大（图 3b）
- 实际采用 $c_t = \frac{k}{T}t \simeq (1-t)t$，随优化步数 $k$ 从 0 线性增长到 $t$，实现早期保守、中期有效引导的平衡

### 核心模块三：梯度近似与优化

为直接优化目标潜在变量 $x_0^{\mathrm{tgt}}$，DRFS 对能量函数求导并省略网络雅可比（遵循 DDS 等工作的标准做法，以单位矩阵近似）：

$$ \nabla_{\Theta}\mathcal{E}_{\mathrm{DRFS}} = \mathbb{E}_{t,\varepsilon}\left[w_{\mathrm{DRFS}}(t)\left(v_\theta(\hat{x}_t^{\mathrm{tgt}}) - v_\theta(x_t^{\mathrm{src}}) - (\dot{a}_t + \dot{c}_t)(x_0^{\mathrm{tgt}} - x_0^{\mathrm{src}})\right)\right] \tag{8} $$

其中权重函数 $w_{\mathrm{DRFS}}(t) = 2(a_t + c_t - \dot{a}_t - \dot{c}_t)$，$\Theta = x_0^{\mathrm{tgt}}$。

梯度包含三项：
1. **速度差** $v_\theta(\hat{x}_t^{\mathrm{tgt}}) - v_\theta(x_t^{\mathrm{src}})$：驱动编辑的核心信号
2. **漂移项** $-(\dot{a}_t + \dot{c}_t)(x_0^{\mathrm{tgt}} - x_0^{\mathrm{src}})$：由残差差异推导出的校正流特有项，约束编辑方向
3. **权重** $w_{\mathrm{DRFS}}(t)$：时间依赖的缩放因子

### 核心模块四：降序时间步调度

DRFS 采用从高噪声到低噪声的**降序时间步调度**（$t \approx 1 \to t \approx 0$），而非均匀随机采样。这一设计实现了**由粗到细（coarse-to-fine）**的优化：早期大时间步允许大幅几何和结构变化，后期小时间步精细调整颜色和纹理（见图 6 的消融对比）。

### 统一框架：DRFS 对 DDS 和 FlowEdit 的归纳

DRFS 提供了统一的理论框架：
- **$c_t = 0$** 时，利用噪声-速度等价关系 $\varepsilon_\theta(x,t,\varphi) = \frac{a_t}{\dot{b}_t a_t - \dot{a}_t b_t}(v_\theta(x,t,\varphi) - \frac{\dot{a}_t}{a_t}x)$，DRFS 能量函数严格退化为 DDS 能量函数
- **$(a_t, b_t, c_t) = (1-t, t, t)$** 时，DRFS 退化为 FlowEdit 的编辑动力学

这种统一性不仅提供了理论解释，也使得 DRFS 可以通过调节 $c_t$ 在 DDS（强背景保留）和 FlowEdit（强语义对齐）之间连续插值，实现灵活的最优平衡。

![[assets/figures/papers/paper_list_l2304_https_arxiv_org_abs_2509_05342/figures/002_Figure_2.jpg]]
*Figure 2: Visual comparison of the sampling strategies for editing. When*

## 实验与关键发现

### 核心性能瓶颈与设计动机

DRFS 的设计直接针对校正流编辑中一个被反复观察却未被系统解决的失效模式：**RFDS 在编辑过程中产生过度平滑（over-smoothing）和细节丢失**。其根本原因在于，RFDS 的能量函数不加区分地优化整个图像，无法分离需要编辑的区域和应保留的背景区域。DRFS 通过两个核心机制来破解这一瓶颈：

1. **残差能量函数**：显式建模源速度场与目标速度场之间的差异（而非仅优化目标速度），使得梯度在不相关区域自然抵消，从而保留未编辑区域的纹理和结构。
2. **时间依赖的偏移项 $c_t$**：将噪声潜在变量推向目标分布的正确轨迹，减轻模型-数据不匹配并稳定优化过程。$c_t$ 是 DRFS 的**因果调节旋钮**——$c_t=0$ 还原 DDS，$c_t=t$ 还原 FlowEdit，而中间值 $(1-t)t$ 实现了背景保留与语义对齐的最佳平衡。

### 主要定量结果

在 **PIE Benchmark** 上，DRFS 在 SD3 骨干网络上与多种扩散和校正流基线进行了系统对比（Table 1）。核心发现如下：

![[assets/figures/papers/paper_list_l2304_https_arxiv_org_abs_2509_05342/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison on the PIE benchmark. The best and second-best results are shown in bold and underlined, respectively*

- **编辑语义对齐最优**：DRFS 在编辑区域的 CLIP 相似性上达到 **23.83**，为所有 SD3/SD3.5 方法中最高，表明其编辑结果与目标文本描述最为一致。
- **背景保留大幅领先同类方法**：与同属校正流蒸馏路线的 iRFDS 相比，DRFS 在背景保留指标上取得显著优势——LPIPS 从 186.39 降至 **93.81**（↓49.7%），MSE 从 179.76 降至 **67.49**（↓62.5%），SSIM 从 74.59 提升至 **84.85**（↑13.8%）。这一差距直接验证了残差能量函数在抑制不相关区域梯度方面的有效性。
- **结构保持能力**：在“改变物体姿态”（Change Object Pose）等挑战性子任务上，DRFS 的 LPIPS 为 **91.4**，优于 FlowEdit 的 102.6，显示出更强的结构保持能力（Table S2）。

![[assets/figures/papers/paper_list_l2304_https_arxiv_org_abs_2509_05342/figures/013_Table_S.2.jpg]]
*Table S.2: Category-level PIE results on challenging edits (SD3). Lower LPIPS indicates better structural preservation, higher CLIP indicates stronger semantic alignment*

**效率方面**，DRFS 在 700 次编辑任务上的平均耗时与主要基线可比，且无需训练或模型结构修改（Table S1）。

### 消融实验：偏移系数 $c_t$ 的关键作用

偏移系数 $c_t$ 是 DRFS 框架中最关键的调节变量，其消融结果（Table 2）揭示了清晰的权衡规律：

- **$c_t = 0$（等价于 DDS）**：背景保留指标最佳（PSNR 28.63, LPIPS 44.66），但编辑语义相似性下降至 Edited CLIP 22.53，表明编辑强度不足，语义对齐不充分。
- **$c_t = t$（等价于 FlowEdit）**：编辑强度增强，但背景保留明显退化。
- **$c_t \simeq (1-t)t$（DRFS 默认调度）**：在语义对齐（Edited CLIP 23.83）与背景保留之间取得**最佳平衡点**。该调度起始于 0（早期保守，保护背景），随优化步数 $k$ 线性增大至 $t$（后期增强编辑强度），形成近似抛物线形状。

Figure 3 从几何角度解释了 $c_t$ 的作用机制：更大的 $c_t$ 产生更直的编辑路径（子图 a），同时通过放大 $\|v_\theta(\hat{x}_t^{tgt}) - v_\theta(x_t^{src})\|^2$ 增加更新幅度（子图 b）。这验证了偏移项在“直线化”编辑轨迹和“增强驱动力”方面的双重功能。

### 时间步调度器与优化器选择

**降序调度（descending scheduler）** 是实现由粗到细优化的关键设计。Figure 6 的定性对比显示，随机均匀采样时间步会导致编辑结果不一致，而降序调度（从高噪声 $t \approx 1$ 到低噪声 $t \approx 0$）允许早期进行大幅度几何变化、后期细化颜色和纹理，产生更稳定的编辑效果。

**优化器选择**上，SGD 优于 Adam（Table S4）。分析指出，Adam 的自适应归一化会放大异常梯度并削弱一致的信息梯度，导致编辑强度不足；SGD 的均匀更新更有利于保持编辑方向的一致性。

**批次大小**方面，$B=5$ 进一步改善了结构距离（21.50）和背景保留（LPIPS 87.68），但即使在 $B=1$ 时 DRFS 已优于所有基线（Table S3），表明方法本身具有较强的鲁棒性。

### 定性分析与失败模式

Figure 5 展示了 DRFS 在多种编辑任务上的定性结果，包括物体替换、风格迁移、姿态改变等。与 Figure 1 中 RFDS 的过度平滑对比，DRFS 在保持源图像纹理细节（如动物毛发、背景植被）的同时，实现了目标语义的有效注入。

![[assets/figures/papers/paper_list_l2304_https_arxiv_org_abs_2509_05342/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative edits produced by our DRFS. Each pair indicates the source image (left) and edited result (right)*

然而，DRFS 存在以下已知失败模式：

1. **大幅结构改变困难**：当编辑需要显著改变物体几何结构或面对分布外（OOD）图像时，编辑强度不足，容易失败。
2. **模型适用范围受限**：DRFS 仅适用于校正流模型（Rectified Flow），无法直接应用于标准扩散模型。
3. **$c_t$ 调度的经验性**：当前 $(1-t)t$ 调度虽在实践中有效，但缺乏自动适应不同编辑难度的机制，仍需手动调节。

### 方法谱系与知识库定位

DRFS 在编辑方法谱系中占据独特位置。与基于扩散模型的 **P2P**、**Null-text Inversion** 等注意力注入方法不同，DRFS 无需反演（inversion-free），直接在校正流模型的 ODE 轨迹上优化。在校正流编辑路线内部，DRFS 统一了 **DDS**（$c_t=0$）和 **FlowEdit**（$c_t=t$）两个端点方法，并通过引入残差能量函数和可调偏移系数提供了更灵活的编辑控制。与同期的 **iRFDS** 相比，DRFS 在背景保留上取得质的提升，证明了显式建模源-目标差异而非蒸馏的优越性。

DRFS 为知识库贡献了以下可迁移洞察：**在生成模型编辑中，通过构造源-目标残差能量函数来抵消共享分量，是缓解过度平滑的通用策略**；**时间依赖的偏移项为调节编辑强度与背景保留提供了连续可控的旋钮**。这些洞察对视频编辑、3D 编辑等更广泛的生成编辑任务具有潜在指导意义。

![[assets/figures/papers/paper_list_l2304_https_arxiv_org_abs_2509_05342/figures/004_Figure_6.jpg]]
*Figure 6: Qualitative edits produced by our DRFS with different schedulers. For each triplet: left = source, center = random scheduler, right = descending scheduler*

## 定位与知识库关联

### 编辑范式谱系中的位置

DRFS 处于**校正流模型（Rectified Flow）上的无需求反演编辑**这一支线。与基于扩散模型的经典编辑方法（如 **P2P**、**PnP-Inv**、**Null-text Inv**）不同，DRFS 不依赖 DDIM 反演或注意力注入，而是直接在流模型的 ODE 轨迹上优化目标潜在变量。与同属校正流编辑家族的 **RF-Inv**、**RF-Solver**、**FireFlow** 等方法相比，DRFS 摒弃了反演步骤，转而采用能量函数优化的蒸馏范式。

在无需求反演的校正流编辑方法中，DRFS 与 **FlowEdit**、**FTEdit**、**DNAEdit** 以及 **iRFDS** 构成直接竞争关系。DRFS 的理论贡献在于通过统一的能量函数框架将 **DDS**（扩散模型上的 Delta Denoising Score）和 **FlowEdit** 同时纳入特例：当偏移系数 $c_t = 0$ 时 DRFS 退化为 DDS 在流模型上的对应形式，当 $(a_t, b_t, c_t) = (1-t, t, t)$ 时 DRFS 还原为 FlowEdit 的编辑动力学。这一归纳性理论支撑使 DRFS 成为该支线中具有统一视角的方法。

### 核心改进与因果机制

DRFS 针对 **RFDS**（Rectified Flow Distillation Sampling）的两个根本缺陷进行了定向修复：

1. **过度平滑问题**：RFDS 的能量函数仅最小化目标速度场与数据动力学的差异，导致梯度不加区分地作用于整幅图像，使得未编辑区域的纹理细节被抹平。DRFS 将能量函数重构为源-目标速度场的**残差差异**：
   $$\mathcal{E}_{\mathrm{DRFS}} = \mathbb{E}_{t,\varepsilon}\Big[\big\| v_\theta(\hat{x}_t^{\mathrm{tgt}}) - v_\theta(x_t^{\mathrm{src}}) - (\dot{\hat{x}}_t^{\mathrm{tgt}} - \dot{x}_t^{\mathrm{src}}) \big\|^2\Big]$$
   源和目标共享的速度分量在减法中抵消，梯度仅作用于真正需要编辑的区域，从而在机制层面缓解了过度平滑。

2. **模型-数据不匹配**：目标潜在变量 $x_0^{\mathrm{tgt}}$ 在优化过程中逐步偏离源分布，导致在标准前向加噪点 $x_t^{\mathrm{tgt}}$ 处评估的速度场 $v_\theta$ 不再对应理想编辑轨迹的后验分布。DRFS 引入时间依赖的**偏移项** $c_t(x_0^{\mathrm{tgt}} - x_0^{\mathrm{src}})$，将评估点推向目标分布的正确轨迹：
   $$\hat{x}_t^{\mathrm{tgt}} = a_t x_0^{\mathrm{tgt}} + b_t \varepsilon + c_t (x_0^{\mathrm{tgt}} - x_0^{\mathrm{src}})$$
   这一偏移同时产生两个可量化的效应（见 Figure 3）：增大 $c_t$ 使编辑路径更直（路径-弦比 $S_R$ 下降），同时放大更新幅度（$\|v_\theta(\hat{x}_t^{\mathrm{tgt}}) - v_\theta(x_t^{\mathrm{src}})\|^2$ 增大），从而在保持背景的同时增强编辑强度。

### 适用边界与局限

DRFS 的适用性受以下边界约束：

- **模型依赖**：DRFS 仅适用于校正流模型（如 SD3、SD3.5），无法直接迁移到标准扩散模型（如 SDXL、SD1.5）。这是由其能量函数中速度场残差的计算方式决定的——扩散模型的噪声预测 $\varepsilon_\theta$ 虽可通过等价关系转换为速度 $v_\theta$，但 DRFS 的偏移项设计和梯度近似均针对流模型的 $a_t$、$b_t$ 系数族进行了定制。
- **编辑幅度限制**：当编辑任务要求大幅改变物体结构（如姿态剧烈变化、物体替换）或处理分布外（OOD）图像时，DRFS 的编辑强度不足，容易失败。这是因为能量函数本质上约束的是源和目标速度场的差异，当目标分布与源分布距离过远时，速度场残差提供的梯度信号不足以驱动足够的几何变化。
- **偏移系数的手动调度**：$c_t = \frac{k}{T}t \simeq (1-t)t$ 的调度策略虽在实践中表现良好，但其设计依赖经验——优化早期 $c_t \approx 0$ 保持背景，中期 $c_t$ 增大提供编辑引导，后期 $c_t$ 再次减小以细化细节。缺乏自动适应不同编辑任务难度的机制，可能在某些场景下导致编辑不足或过度。

### 与邻近方法的互补空间

DRFS 目前尚未探索与以下技术的结合，这些方向可能进一步扩展其能力边界：

- **注意力注入**：P2P 等方法通过操纵交叉注意力图实现对编辑区域的精细控制。将 DRFS 的速度场残差优化与注意力注入结合，可能在大幅度结构编辑任务中提供额外的空间可控性。
- **多步平均策略**：FTEdit 通过多步编辑结果的平均减少伪影，这一技术与 DRFS 的 SGD 优化天然兼容（消融实验已证实 Batch Size B=5 可改善结构距离和背景保留），但尚未在方法论层面进行系统整合。
- **通用生成模型扩展**：如何将源-目标残差差异的思想推广到扩散模型或其他生成范式（如自回归模型、一致性模型），是 DRFS 理论贡献泛化的关键开放问题。

### 实验证据强度评估

DRFS 的核心声明均有强证据支撑：

- **过度平滑缓解**：Figure 1 的定性对比和 Table 1 中 DRFS 在背景保留指标上对 iRFDS 的显著优势（LPIPS: 93.81 vs 186.39, MSE: 67.49 vs 179.76, SSIM: 84.85 vs 74.59）构成强证据链。
- **偏移项有效性**：Table 2 的消融实验系统验证了 $c_t \simeq (1-t)t$ 在编辑语义对齐（Edited CLIP 23.83）与背景保留之间的最佳平衡，$c_t=0$ 时背景保留最佳但语义对齐下降，$c_t=t$ 时编辑强度最大但背景损失增加。
- **理论统一性**：Section 4.1 的数学推导严格证明了 DRFS 对 DDS 和 FlowEdit 的归纳关系，置信度高。

需要手动验证的点：DRFS 在 SD3.5 上的性能虽在 Table 1 中有所体现，但论文未提供与 SD3 结果同样详尽的子任务分解，SD3.5 上的优势幅度和一致性需要对照完整数据确认。

## 原文 PDF

![[paperPDFs/CVPR_2026/Delta_Rectified_Flow_Sampling_for_Text_to_Image_Editing.pdf]]
