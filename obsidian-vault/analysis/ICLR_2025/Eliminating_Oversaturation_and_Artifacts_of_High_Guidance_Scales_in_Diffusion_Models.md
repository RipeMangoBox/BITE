---
title: Eliminating Oversaturation and Artifacts of High Guidance Scales in Diffusion Models
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/Eliminating_Oversaturation_and_Artifacts_of_High_Guidance_Scales_in_Diffusion_Models.pdf
project_link: http://probml.github.io/book2
code_link: null
aliases:
- APGA
- EOAHGSDM
tags:
- ICLR_2025
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: CFG更新方向中平行于条件预测的分量的强度（通过超参数η控制）；同时，重新缩放半径r和反向动量β也对更新幅度和多样性有关键影响。
primary_logic: 将CFG更新分解为平行于和正交于条件预测D_θ(z_t,t,y)的两个分量，发现正交分量是提升图像质量的主要来源，而平行分量只增加饱和度。通过降低平行分量权重并结合重新缩放与反向动量，可以在保持质量增益的同时显著缓解过饱和问题。
claims:
- 正交分量提升图像质量，平行分量主要引起过饱和（Figure 2）。
- 使用APG替代CFG后，在所有测试模型上FID、Recall和饱和度指标均得到显著改善，同时保持精度相当（Table 1）。
- 将投影应用于去噪预测而非噪声预测对于降低饱和度至关重要（Figure 12）。
- 移除投影、重新缩放或反向动量中任一组件均会导致FID恶化，其中投影主要影响饱和度（Table 2）。
---

# Eliminating Oversaturation and Artifacts of High Guidance Scales in Diffusion Models

> [!tip] 核心洞察
> 将CFG更新分解为平行于和正交于条件预测D_θ(z_t,t,y)的两个分量，发现正交分量是提升图像质量的主要来源，而平行分量只增加饱和度。通过降低平行分量权重并结合重新缩放与反向动量，可以在保持质量增益的同时显著缓解过饱和问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | 消除扩散模型高引导尺度下的过饱和与伪影 |
| 英文题名 | Eliminating Oversaturation and Artifacts of High Guidance Scales in Diffusion Models |
| 会议/期刊 | ICLR 2025 |
| Links | [paper](https://openreview.net/forum?id=e2ONKX6qzJ) · [Project](http://probml.github.io/book2) · [paper](https://arxiv.org/abs/2112.03111) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Adaptive Projected Guidance (APG) |
| Dataset | EDM2-S, DiT-XL/2, Stable Diffusion XL, EDM2-S across guidance scales |

> [!tip] 效果简介
> - EDM2-S (class-conditional ImageNet, w=4) 上，FID↓ 6.49 vs 10.42 (-3.93)；Recall↑ 0.62 vs 0.48 (+0.14)；Saturation↓ 0.33 vs 0.46 (-0.13)。
> - DiT-XL/2 (class-conditional ImageNet, w=4) 上，FID↓ 9.34 vs 19.14 (-9.80)。
> - Stable Diffusion XL (text-to-image, w=15) 上，FID↓ 25.35 vs 26.29 (-0.94)。

## 概要

扩散模型在高引导尺度下生成图像时普遍出现过饱和与不真实伪影，这一问题严重限制了**分类器自由引导**（Classifier-Free Guidance, CFG）的实际可用引导范围。本文揭示了一个关键瓶颈：CFG的更新方向可以分解为平行于和正交于条件模型预测的两个分量——正交分量是提升图像质量的主要来源，而平行分量仅增加饱和度且在高引导尺度下乘以大于1的增益因子，导致过饱和。基于此洞察，本文提出**自适应投影引导**（Adaptive Projected Guidance, APG），通过正交投影降低平行分量权重，辅以更新幅度重缩放和反向动量，在保持CFG质量增益的同时显著缓解过饱和问题。实验表明，APG在多种扩散模型（EDM2、DiT-XL/2、Stable Diffusion XL等）上一致改善FID、Recall和饱和度指标，且保持与CFG相当的精度，有效扩展了引导尺度的可用范围。



扩散模型已成为图像生成领域的核心范式，其采样过程可被统一描述为一个常微分方程（ODE）：

$$
\mathrm{d} z_t = -\dot{\sigma}(t)\sigma(t) \nabla_{z_t} \log p_t(z_t) \mathrm{d}t
$$

然而，直接从此ODE采样得到的图像往往缺乏细节和真实感。为解决这一问题，**分类器自由引导（Classifier-Free Guidance, CFG）**（Ho & Salimans, 2022）被广泛采用。CFG通过混合条件预测与无条件预测来增强条件对齐：

$$
\hat{D}_{\mathrm{CFG}}(z_t, t, y) = D_{\theta}(z_t, t, y_{\mathrm{null}}) + w (D_{\theta}(z_t, t, y) - D_{\theta}(z_t, t, y_{\mathrm{null}}))
$$

其中 $w$ 为引导尺度。当 $w > 1$ 时，CFG将采样推向条件分布的高密度区域，显著提升图像质量。但这一收益伴随着一个严重的代价：**在高引导尺度下，生成图像会出现过饱和（oversaturation）和不真实的伪影（artifacts）**，如Figure 1所示。这迫使实际使用中只能采用中等引导尺度，限制了CFG潜力的充分发挥。

### 现有方法的缺口

尽管已有一些工作尝试缓解CFG的副作用，例如 **CFG Rescale**（Lin et al., 2024a）专门针对过曝问题，但这些方法在高引导尺度下仍无法有效解决饱和度问题（见Figure 11对比）。更重要的是，**缺乏对CFG导致过饱和的根本原因的深入理解**，使得现有改进多为启发式调整，未能从机制层面解决问题。

### 本文动机

本文的核心动机源于一个关键观察：将CFG的更新项 $\Delta D_t = D_{\theta}(z_t, t, y) - D_{\theta}(z_t, t, y_{\mathrm{null}})$ 分解为平行于和正交于条件预测 $D_{\theta}(z_t, t, y)$ 的两个分量后，**正交分量是提升图像质量的主要来源，而平行分量仅增加饱和度**（Figure 2）。具体而言，平行分量相当于对条件预测乘以一个大于1的增益因子：

$$
D_{\theta}(z_t, t, y) + (w-1)\Delta D_t^{\parallel} = \left[1 + (w-1)\frac{\|\Delta D_t^{\parallel}\|}{\|D_{\theta}(z_t, t, y)\|}\right] D_{\theta}(z_t, t, y)
$$

这一发现揭示了CFG过饱和的因果机制：随着 $w$ 增大，平行分量的增益因子不断放大，导致像素值趋向饱和。基于此洞察，本文提出 **自适应投影引导（Adaptive Projected Guidance, APG）**，通过降低平行分量权重并结合重新缩放与反向动量，在保持CFG质量增益的同时显著缓解过饱和问题，从而大幅扩展扩散模型实际可用的引导尺度范围。



## 核心方法与创新机理

### 问题瓶颈：CFG 高引导尺度下的过饱和与伪影

分类器自由引导（Classifier-Free Guidance, CFG）是扩散模型生成高质量图像的核心技术，但在高引导尺度下会引发严重的过饱和现象和不真实的伪影。本文通过理论分析揭示了这一现象的根本原因：CFG 的更新方向可被分解为平行于和正交于条件模型预测的两个分量，其中**平行分量是导致过饱和的“元凶”**，而正交分量才是提升图像质量的主要驱动力。

具体而言，CFG 的更新项 $\Delta D_t = D_{\theta}(z_t, t, y) - D_{\theta}(z_t, t, y_{\mathrm{null}})$ 可被正交投影分解为：

$$\Delta D_t^{\parallel} = \frac{\langle \Delta D_t, D_{\theta}(z_t, t, y) \rangle}{\langle D_{\theta}(z_t, t, y), D_{\theta}(z_t, t, y) \rangle} D_{\theta}(z_t, t, y)$$

$$\Delta D_t^{\perp} = \Delta D_t - \Delta D_t^{\parallel}$$

当引导尺度 $w > 1$ 时，平行分量 $\Delta D_t^{\parallel}$ 实际上相当于对条件预测 $D_{\theta}(z_t, t, y)$ 乘以一个大于 1 的增益因子：

$$D_{\theta}(z_t, t, y) + (w-1)\Delta D_t^{\parallel} = \left[1 + (w-1)\frac{\|\Delta D_t^{\parallel}\|}{\|D_{\theta}(z_t, t, y)\|}\right] D_{\theta}(z_t, t, y)$$

这导致生成图像的像素值被持续推向饱和区域，而正交分量 $\Delta D_t^{\perp}$ 则独立地增强了图像的细节与真实感（Figure 2 提供了直观的消融证据：仅使用平行分量几乎不改变图像质量而仅增加饱和度，仅使用正交分量则能在不引起过饱和的前提下显著提升质量）。

### 核心方法：自适应投影引导（APG）

基于上述发现，本文提出了 **自适应投影引导（Adaptive Projected Guidance, APG）**，通过三个关键组件对标准 CFG 进行改造：

**1. 正交投影（Orthogonal Projection）—— 核心创新**

APG 将 CFG 的更新方向重构为平行分量与正交分量的加权组合：

$$\Delta D_t(\eta) = \Delta D_t^{\perp} + \eta \Delta D_t^{\parallel}$$

其中超参数 $\eta \leq 1$ 控制平行分量的强度。默认设置 $\eta = 0$ 意味着完全移除平行分量，仅保留质量增强的正交分量，从而在根本上阻断过饱和的产生路径。实验表明，增加 $\eta$ 会导致饱和度和 FID 同步上升（Table 9a），验证了平行分量的负面作用。

**2. 重新缩放（Rescaling）—— 更新幅度约束**

为防止单步更新过大导致采样轨迹漂移，APG 引入半径约束将更新限制在半径为 $r$ 的球内：

$$\Delta D_t \gets \Delta D_t \cdot \min\left(1, \frac{r}{\|\Delta D_t\|}\right)$$

适中的 $r$（如 2.5）可取得最佳 FID：过大则约束失效，过小则损害生成质量（Table 9b）。

**3. 反向动量（Reverse Momentum）—— 多样性增强**

APG 引入负动量系数 $\beta < 0$ 累积历史更新方向，使当前更新远离历史轨迹：

$$\Delta D_t \gets \Delta D_t + \beta \cdot \text{running\_average}$$

这一设计源于将 CFG 解释为目标函数 $f_{\mathrm{CFG}} = \frac{1}{2}\|D_{\theta}(z_t, t, y) - D_{\theta}(z_t, t, y_{\mathrm{null}})\|^2$ 的梯度上升过程，反向动量有助于逃离局部最优，提升样本多样性和探索性。实验表明 $\beta = -0.75$ 优于正动量或无动量设置（Table 9c）。

### 与基线方法的本质差异

| 设计维度 | CFG (Ho & Salimans, 2022) | CFG Rescale (Lin et al., 2024a) | APG (本文) |
|---------|--------------------------|--------------------------------|-----------|
| 更新方向 | 直接使用 $\Delta D_t$ | 对 CFG 输出进行整体缩放 | 分解为平行/正交分量，降权平行分量 |
| 过饱和控制 | 无专门机制 | 事后缩放缓解过曝 | 从更新方向根源阻断 |
| 更新幅度 | 无约束 | 无额外约束 | 半径 $r$ 球约束 |
| 历史信息 | 无 | 无 | 负动量推开历史方向 |

值得注意的是，APG 的投影操作必须作用于**去噪预测** $D_{\theta}(z_t, t, y)$ 而非噪声预测 $\epsilon_{\theta}(z_t, t, y)$。Figure 12 的消融实验表明，若将投影应用于噪声预测，输出结果与标准 CFG 几乎无异，无法有效降低饱和度——这揭示了投影空间选择的关键性。

### 消融验证：各组件的独立贡献

Table 2 的消融实验量化了三个组件的贡献（EDM2-S, $w=4$）：

- **完整 APG**：FID = 6.49，饱和度 = 0.33
- **移除投影**：FID 升至 6.63，饱和度升至 0.37 —— 投影主要影响饱和度控制
- **移除重新缩放**：FID 升至 7.93 —— 幅度约束对稳定性至关重要
- **移除反向动量**：FID 升至 6.85 —— 动量独立贡献于图像质量提升

三者协同作用，缺一不可。正交投影是解决过饱和的核心机制，重新缩放和反向动量则分别从稳定性和多样性维度进一步提升了生成质量。



APG（Adaptive Projected Guidance）是一种即插即用的采样端引导方法，旨在保持分类器自由引导（CFG）质量增益的同时，系统性地消除高引导尺度下的过饱和与伪影。其整体流程在标准扩散采样循环中嵌入三个串行模块，对CFG更新方向进行自适应调整，如图3所示。

**输入**：当前噪声潜变量 $z_t$、时间步 $t$、条件 $y$，以及预训练扩散模型 $D_\theta$（需支持条件与无条件双路推理）。

**核心处理流程**：

1. **双路去噪预测**：在每个采样步，并行计算条件去噪预测 $D_\theta(z_t, t, y)$ 和无条件去噪预测 $D_\theta(z_t, t, y_{\mathrm{null}})$，得到CFG更新方向 $\Delta D_t = D_\theta(z_t, t, y) - D_\theta(z_t, t, y_{\mathrm{null}})$。

2. **正交投影（Orthogonal Projection）**：将 $\Delta D_t$ 投影到条件预测 $D_\theta(z_t, t, y)$ 上，分解为平行分量 $\Delta D_t^{\parallel}$ 和正交分量 $\Delta D_t^{\perp}$。核心发现是：正交分量是提升图像质量的主要来源，而平行分量仅增加饱和度（参见Figure 2）。APG通过超参数 $\eta$ 控制平行分量强度，默认 $\eta=0$ 即完全移除平行分量：
   $$\Delta D_t(\eta) = \Delta D_t^{\perp} + \eta \Delta D_t^{\parallel}$$

3. **重新缩放（Rescaling）**：将组合后的更新 $\Delta D_t$ 限制在半径为 $r$ 的球内，防止单步更新过大导致采样轨迹漂移：
   $$\Delta D_t \gets \Delta D_t \cdot \min\left(1, \frac{r}{\|\Delta D_t\|}\right)$$

4. **反向动量（Reverse Momentum）**：引入负动量系数 $\beta$（默认 $\beta < 0$），累积历史更新方向，使当前更新远离历史方向以增强探索性和多样性：
   $$\Delta D_t \gets \Delta D_t + \beta \cdot \text{running\_average}$$

5. **最终引导输出**：将调整后的 $\Delta D_t$ 代入CFG公式，得到最终去噪预测 $\hat{D}_{\mathrm{APG}}(z_t, t, y) = D_\theta(z_t, t, y) + (w-1) \Delta D_t(\eta)$，然后按标准扩散采样步骤更新 $z_{t-1}$。

**输出**：经APG修正后的去噪预测，用于替代原始CFG更新，生成低饱和度、高真实感的图像。

**关键实现细节**：投影操作必须作用于去噪预测 $D_\theta(z_t, t, y)$ 而非噪声预测 $\epsilon_\theta(z_t, t, y)$，后者会导致结果几乎与标准CFG无异（Figure 12）。APG兼容各类扩散模型（EDM2、DiT、Stable Diffusion系列）、蒸馏模型（如SDXL-Lightning）以及多样性增强方法（CADS、IG），仅需在采样循环中替换CFG更新逻辑即可，无需重新训练或修改模型权重。

**与CFG的关系**：APG可视为CFG的通用超集——当 $\eta=1$、$r \to \infty$、$\beta=0$ 时退化为标准CFG。三个模块的协同作用使得APG在保持条件对齐精度（Precision）的同时，显著降低FID和饱和度（Table 1），且各组件对性能提升均有独立贡献（Table 2）。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_e2ONKX6qzJ/figures/003_Figure_2.jpg]]
*Figure 2: Influence of the parallel and orthogonal components*



### 问题定位：CFG 更新的几何分解

分类器自由引导（CFG）的标准更新公式为：

$$
\hat{D}_{\mathrm{CFG}}(z_t, t, \pmb{y}) = D_{\pmb{\theta}}(z_t, t, \pmb{y}) + (w-1) \Delta D_t
$$

其中 $\Delta D_t = D_{\theta}(z_t, t, y) - D_{\theta}(z_t, t, y_{\mathrm{null}})$ 是条件预测与无条件预测的差值，$w$ 为引导尺度。当 $w>1$ 时，$\Delta D_t$ 被放大并加到条件预测上。本文的核心发现是：**$\Delta D_t$ 中平行于条件预测 $D_{\theta}(z_t, t, y)$ 的分量是导致过饱和的元凶，而正交分量才是提升图像质量的关键**（Figure 2 提供了可视化消融证据）。

### 模块一：正交投影（Orthogonal Projection）

APG 的第一个核心操作是将 $\Delta D_t$ 投影到条件预测 $D_{\theta}(z_t, t, y)$ 上，分解为平行分量和正交分量。

平行分量的计算公式为：

$$
\Delta D_t^{\parallel} = \frac{\langle \Delta D_t, D_{\theta}(z_t, t, y) \rangle}{\langle D_{\theta}(z_t, t, y), D_{\theta}(z_t, t, y) \rangle} D_{\theta}(z_t, t, y)
$$

正交分量则为 $\Delta D_t^{\perp} = \Delta D_t - \Delta D_t^{\parallel}$。

**过饱和的因果机制**：将平行分量代入 CFG 更新后，条件预测 $D_{\theta}(z_t, t, y)$ 被乘以一个大于 1 的增益因子：

$$
D_{\theta}(z_t, t, y) + (w-1)\Delta D_t^{\parallel} = \left[1 + (w-1)\frac{\|\Delta D_t^{\parallel}\|}{\|D_{\theta}(z_t, t, y)\|}\right] D_{\theta}(z_t, t, y)
$$

该增益因子随 $w$ 线性增长，直接导致像素值向饱和区域集中（Figure 7 的核密度估计显示 CFG 生成图像在极端像素值处出现尖峰）。APG 的解决方案是引入超参数 $\eta \in [0, 1]$ 对平行分量降权，重构更新方向：

$$
\Delta D_t(\eta) = \Delta D_t^{\perp} + \eta \cdot \Delta D_t^{\parallel}
$$

默认设置 $\eta=0$，即完全移除平行分量。消融实验（Table 9a）表明，增大 $\eta$ 会导致饱和度和 FID 同步上升，验证了平行分量与过饱和之间的因果关联。

**关键实现细节**：投影必须作用于去噪预测 $D_{\theta}(z_t, t, y)$ 而非噪声预测 $\epsilon_{\theta}(z_t, t, y)$。Figure 12 显示，若对噪声预测做投影，输出几乎与标准 CFG 无异，无法有效降低饱和度。这是因为噪声预测与过饱和之间缺乏直接的几何对应关系。

### 模块二：重新缩放（Rescaling）

CFG 可以解释为对目标函数 $f_{\mathrm{CFG}} = \frac{1}{2}\|D_{\theta}(z_t, t, y) - D_{\theta}(z_t, t, y_{\mathrm{null}})\|^2$ 做梯度上升（Appendix A）。在此视角下，单步更新幅度过大会导致采样轨迹漂移。APG 引入球面约束，将 $\Delta D_t$ 限制在半径为 $r$ 的球内：

$$
\Delta D_t \gets \Delta D_t \cdot \min\left(1, \frac{r}{\|\Delta D_t\|}\right)
$$

当 $\|\Delta D_t\| \leq r$ 时不做修改；超出时按比例缩回球面。消融实验（Table 9b）显示，适中的 $r$（如 2.5）可取得最佳 FID；$r$ 过大等同于无缩放，过小则损害生成质量。移除该模块使 FID 从 6.49 升至 7.93（Table 2）。

### 模块三：反向动量（Reverse Momentum）

为进一步提升探索性和图像质量，APG 引入负动量系数 $\beta < 0$，累积历史更新方向并反向施加：

$$
\Delta D_t \gets \Delta D_t + \beta \cdot \text{running\_average}
$$

其直觉是：推开历史更新方向可以避免采样陷入局部模式，增强多样性。消融实验（Table 9c）表明，$\beta = -0.75$ 优于正动量或无动量设置；但过大的负动量（如 $\beta < -1$）会损害质量。移除该模块使 FID 升至 6.85（Table 2）。

### 完整算法流程

APG 在每步采样中依次执行：① 计算条件与无条件去噪预测，得到 $\Delta D_t$；② 对 $\Delta D_t$ 做正交投影，按 $\eta$ 降权平行分量；③ 施加重新缩放约束；④ 施加反向动量更新。三个模块协同作用：投影解决过饱和的根源，重新缩放防止单步漂移，反向动量提升多样性。Table 2 的消融实验证实，移除任一模块均导致 FID 恶化，其中投影对饱和度的影响最为显著。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_e2ONKX6qzJ/figures/014_Figure_12.jpg]]
*Figure 12: The importance of projecting onto the denoised samples. When performing projection w.r.t. the predicted noise (b), the outputs are barely different than standard CFG (a). However, projecting onto denoised samples (c) more effectively reduces saturation*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_e2ONKX6qzJ/figures/012_Figure_10.jpg]]
*Figure 10: Comparison of CFG and APG for text quality in generated images using Stable Diffusion 3 (Esser et al., 2024). In contrast to CFG, APG consistently produces correct spellings*



## 实验与关键发现

### 主实验结果

APG在类条件生成与文本到图像生成两大类任务上，均展现出对CFG的全面改进。Table 1汇总了多个主流模型上的定量对比，核心结论如下：

**类条件ImageNet生成**：在EDM2-S（w=4）上，APG将FID从10.42降至6.49（降低37.7%），Recall从0.48提升至0.62，同时饱和度指标从0.46降至0.33。在更大规模的EDM2-XXL上，APG同样将FID从8.65降至4.94。在DiT-XL/2上，FID从19.14大幅降至9.34，降幅接近50%。值得注意的是，APG在显著提升FID和Recall的同时，保持了与CFG相当甚至略优的Precision（例如EDM2-S上两者均为0.85），表明去饱和并未以牺牲单样本质量为代价。

**文本到图像生成**：在Stable Diffusion 2.1（w=7.5）上，APG将FID从27.53降至22.21，饱和度从0.31降至0.20。在Stable Diffusion XL（w=15）上，FID从26.29降至25.35，饱和度从0.28降至0.18。Precision在SD 2.1上从0.65升至0.67，在SD XL上从0.62升至0.64，进一步验证了APG在降低饱和度的同时不损害语义对齐质量。

**引导尺度鲁棒性**：Figure 8展示了随引导尺度增加的FID/Recall/Precision变化趋势。CFG在高引导尺度下FID急剧恶化、Recall持续下降，而APG在整个引导尺度范围内保持较低的FID和较高的Recall，Precision与CFG持平或更优。这表明APG显著扩展了可用的引导尺度范围，使高引导尺度采样变得可行。

### 消融实验

**组件重要性**（Table 2）：以EDM2-S（w=4）为基准，完整APG的FID为6.49。移除正交投影后FID升至6.63，饱和度从0.33升至0.37，验证了投影组件对饱和度控制的关键作用。移除重新缩放后FID显著升至7.93，表明更新幅度约束对采样稳定性至关重要。移除反向动量后FID升至6.85，说明负动量对提升图像质量有独立贡献。三个组件均对最终性能有正向贡献，其中重新缩放的贡献最为显著。

**超参数分析**（Table 9）：平行分量强度η从0增加至1时，FID和饱和度均呈上升趋势，η=0（完全移除平行分量）为最优设置，验证了平行分量主要贡献饱和度的核心洞察。重新缩放半径r在2.5附近取得最佳FID；r过小（如0.5）会过度约束更新导致质量下降，r过大（如5.0）则接近无缩放效果。动量系数β在负值范围内（-0.75）优于正值或无动量，但过大的负动量（如-0.9）会损害质量，表明适度的反向动量有助于探索性采样。

**投影对象选择**（Figure 12）：将投影应用于去噪预测D_θ(z_t,t,y)对于降低饱和度至关重要。若将投影应用于噪声预测ε_θ(z_t,t,y)，则输出与标准CFG几乎无异，无法有效缓解过饱和。这一发现说明去噪预测空间中的几何分解是APG有效性的关键前提。

### 兼容性与通用性

**蒸馏模型兼容性**（Figure 9）：APG可直接应用于蒸馏模型如SDXL-Lightning，在不降低输出质量的前提下替换CFG，无需额外调整。

**采样器兼容性**（Table 5）：在DiT-XL/2上测试多种流行采样器（DDIM、DPM-Solver等），APG在所有采样器上均取得优于CFG的指标，展现了良好的采样器无关性。

**与其他多样性增强方法的协同**（Table 4）：将APG与CADS（Sadat et al., 2024）或IG（Kynkäänniemi et al., 2024）结合使用时，FID优于各方法单独使用，表明APG的正交投影机制与其他多样性增强方法存在互补效应。

**条件对齐保持**（Table 8）：APG在降低饱和度的同时，条件对齐精度与CFG保持相当，未因降饱和度而牺牲语义一致性，这是其作为CFG直接替代方案的关键保障。

### 失败模式与局限

尽管APG在多数场景下表现优异，仍存在以下局限：

1. **采样成本未降低**：APG仍需每步查询两次去噪网络（条件与无条件），采样成本约为未引导采样的两倍。如何加速以使成本接近未引导采样仍是待解决问题。

2. **超参数手动调整**：APG引入了η、r、β三个额外超参数，需针对不同模型和引导尺度手动调整（Table 10给出了主实验中的推荐值）。目前缺乏自适应调整机制，可能增加实际部署的调参负担。

3. **极端引导尺度下的残余伪影**：虽然APG大幅缓解了高引导尺度下的过饱和问题，但在极端的引导尺度设置下，仍可能出现少量不自然的纹理或结构伪影，需要进一步研究。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_e2ONKX6qzJ/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison between CFG and APG. APG consistently improves FID, recall and color metrics while maintaining similar or better precision compared to CFG*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_e2ONKX6qzJ/figures/015_Table_2.jpg]]
*Table 2: Importance of different components in APG*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_e2ONKX6qzJ/figures/009_Figure_7.jpg]]
*Figure 7: Kernel density estimates of pixel and saturation values for two sets of samples generated with CFG and APG. Compared to CFG, images generated with APG show less concentration around saturated pixels, indicated by the spikes at the extreme values in both plots*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_e2ONKX6qzJ/figures/026_Table_9.jpg]]
*Table 9: Ablation study examining various design elements in APG*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_e2ONKX6qzJ/figures/013_Figure_11.jpg]]
*Figure 11: Comparison between APG and CFG Rescale using Stable Diffusion XL. CFG Rescale is unable to solve the saturation issue at high guidance scales compared with APG*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_e2ONKX6qzJ/figures/011_Figure_9.jpg]]
*Figure 9: Showcasing the compatibility of APG with distilled diffusion models using SDXL-Lightning. Compared to CFG, using APG does not result in degradation in the output quality*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_e2ONKX6qzJ/figures/018_Table_4.jpg]]
*Table 4: Compatibility of APG with CADS (Sadat et al., 2024a) and IG (Kynkäänniemi et al., 2024). Combining APG with other methods that improve diversity results in better FID than each method in isolation*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_e2ONKX6qzJ/figures/021_Table_5.jpg]]
*Table 5: Impact of using APG with popular diffusion samplers using the class-conditional ImageNet model (DiT-XL/2). Compared to CFG, APG showes improved metrics across all samplers*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_e2ONKX6qzJ/figures/024_Table_8.jpg]]
*Table 8: Condition alignment comparison between CFG and APG*



## 定位与知识库关联

### 核心基线：分类器自由引导（CFG）与过饱和瓶颈

APG 直接建立在 **Classifier-Free Guidance (CFG)**（Ho & Salimans, 2022）之上。CFG 通过在每一步采样中混合条件与无条件去噪预测来增强生成质量，其更新公式为：

$$\hat{D}_{\mathrm{CFG}}(z_t, t, y) = D_{\theta}(z_t, t, y_{\mathrm{null}}) + w (D_{\theta}(z_t, t, y) - D_{\theta}(z_t, t, y_{\mathrm{null}}))$$

其中引导尺度 $w$ 控制条件信号强度。CFG 的有效性已被广泛验证，但其在高引导尺度下的副作用——过饱和与不真实伪影——构成了本文的核心问题。

APG 的突破性洞察在于对 CFG 更新方向 $\Delta D_t = D_{\theta}(z_t,t,y) - D_{\theta}(z_t,t,y_{\mathrm{null}})$ 的几何分解。通过将 $\Delta D_t$ 正交投影到条件预测 $D_{\theta}(z_t,t,y)$ 上，得到平行分量 $\Delta D_t^{\parallel}$ 和正交分量 $\Delta D_t^{\perp}$：

$$\Delta D_t^{\parallel} = \frac{\langle \Delta D_t, D_{\theta}(z_t, t, y) \rangle}{\langle D_{\theta}(z_t, t, y), D_{\theta}(z_t, t, y) \rangle} D_{\theta}(z_t, t, y)$$

理论分析揭示：平行分量相当于对条件预测乘以大于1的增益因子，即 $[1 + (w-1)\frac{\|\Delta D_t^{\parallel}\|}{\|D_{\theta}(z_t,t,y)\|}] D_{\theta}(z_t,t,y)$，这正是过饱和的根源；而正交分量才是提升图像质量的主要驱动力（Figure 2）。这一发现将 CFG 的质量增益与饱和度副作用在几何上解耦，为针对性干预提供了理论锚点。

### 与 CFG Rescale 的对比

**CFG Rescale**（Lin et al., 2024a）是专门针对 CFG 过曝问题的基线方法。定性比较（Figure 11）表明，在高引导尺度下 CFG Rescale 无法有效解决饱和度问题，而 APG 通过直接降低平行分量权重实现了更彻底的饱和度控制。这一差异源于两种方法的作用机制不同：CFG Rescale 对整体更新进行启发式缩放，而 APG 基于几何分解精确定位并抑制过饱和的因果分量。

### 方法谱系中的定位

APG 在扩散模型引导方法的谱系中处于 **CFG 的解析改进层**。与以下方向形成互补而非替代关系：

- **蒸馏加速方法**：APG 兼容少步蒸馏模型，如 **SDXL-Lightning**（Figure 9），在保持加速优势的同时降低饱和度。
- **多样性增强方法**：APG 可与 **CADS**、**IG** 等方法联合使用，扩展了高引导尺度下的实用范围。
- **文本到图像生成**：在 **Stable Diffusion XL**（Podell et al., 2023）和 **Stable Diffusion 3**（Esser et al., 2024）上均验证有效，且能改善文本拼写质量（Figure 10）。

### 适用边界与局限性

1. **计算成本未降低**：APG 仍需在每步采样中查询两次去噪网络（条件与无条件），采样成本约为未引导采样的两倍。如何加速以接近未引导采样成本仍是待解决问题。

2. **超参数需手动调整**：APG 引入三个额外超参数——平行分量强度 $\eta$、重新缩放半径 $r$、反向动量 $\beta$——需针对不同模型和引导尺度手动设置（Table 10）。消融实验表明，$\eta=0$ 为推荐默认值，$r$ 适中（如 2.5）可取得最佳 FID，负动量 $\beta$（如 -0.75）优于正动量或无动量（Table 9），但缺乏自适应调节机制。

3. **投影对象的敏感性**：投影必须施加于去噪预测 $D_{\theta}(z_t,t,y)$ 而非噪声预测 $\epsilon_{\theta}(z_t,t,y)$，后者结果几乎与标准 CFG 无异（Figure 12）。这意味着 APG 依赖模型输出的特定参数化形式，在仅暴露噪声预测的 API 场景下需要额外转换步骤。

### 开放问题

1. **加速机制**：能否设计方法使 APG 的采样成本接近未引导采样，例如通过共享条件与无条件路径的中间特征，或利用蒸馏技术压缩双次查询？

2. **自适应超参数**：能否根据当前采样步的噪声水平、更新幅度等状态信息，自动调节 $\eta$、$r$ 和 $\beta$，消除手动调参负担？

3. **跨模态泛化**：APG 在视频生成、3D 生成等更多样化条件生成任务中的有效性尚未验证，其与新兴引导范式（如基于能量的引导、对比引导）的结合潜力也待探索。



## 原文 PDF

![[paperPDFs/ICLR_2025/Eliminating_Oversaturation_and_Artifacts_of_High_Guidance_Scales_in_Diffusion_Models.pdf]]
