---
title: "CFG++: Manifold-constrained Classifier Free Guidance for Diffusion Models"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/CFG_Manifold_constrained_Classifier_Free_Guidance_for_Diffusion_Models.pdf
aliases:
- CMCCFGDM
tags:
- ICLR_2025
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: CFG 的重噪声步骤使用条件噪声估计，引入了从真实数据流形偏离的偏移量 Δ^ω，结合大尺度外推，使后验均值估计脱离流形。
primary_logic: "将文本引导重新定义为最小化文本条件评分匹配损失（SDS 损失）的逆问题，利用分解扩散采样（DDS）将去噪与重噪声解耦，从而在重噪声步骤中使用无条件噪声估计，引导尺度缩小到插值区间 [0,1]，既保持流形约束，又实现平滑的条件-无条件过渡与可逆性。"
claims:
- "CFG++ 在重噪声步骤中使用无条件噪声 $\\hat{\\epsilon}_{\\emptyset}(x_t)$ 而非 CFG 的条件噪声，从而产生更平滑的生成轨迹。"
- "CFG++ 的引导尺度 λ ∈ [0,1] 使去噪估计成为无条件与条件估计的插值，避免外推导致离流形。"
- CFG++ 直接最小化文本条件评分匹配损失，相比 CFG 在推理过程中损失更平滑且更低，证明更好的文本对齐。
- 在 COCO 10k 上的 50 步 DDIM T2I 中，CFG++ 在所有引导尺度上均获得更低的 FID，且 CLIP 相似度相当或更高。
---

# CFG++: Manifold-constrained Classifier Free Guidance for Diffusion Models

> [!tip] 核心洞察
> 将文本引导重新定义为最小化文本条件评分匹配损失（SDS 损失）的逆问题，利用分解扩散采样（DDS）将去噪与重噪声解耦，从而在重噪声步骤中使用无条件噪声估计，引导尺度缩小到插值区间 [0,1]，既保持流形约束，又实现平滑的条件-无条件过渡与可逆性。

| 字段 | 内容 |
|------|------|
| 中文题名 | CFG++：基于流形约束的无分类器引导的扩散模型 |
| 英文题名 | CFG++: Manifold-constrained Classifier Free Guidance for Diffusion Models |
| 会议/期刊 | ICLR 2025 |
| Links | [paper](https://openreview.net/forum?id=E77uvbOTtp) · [Project](https://cfgpp-diffusion.github.io) · [Code](https://github.com/crowsonkb/k-diffusion) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | CFG++ |
| Dataset | COCO 10k, SDXL-Turbo, SDXL-Lightning |

> [!tip] 效果简介
> - COCO 10k (50 NFE DDIM T2I, SD v1.5) 上，FID 12.75 vs 13.84 (-1.09)；CLIP 0.303 vs 0.298 (+0.005)；FID 20.88 vs 21.23 (-0.35)。
> - SDXL-Turbo (6 NFE, distilled model) 上，ImageReward 0.968 vs 0.777 (+0.191)。
> - SDXL-Lightning (6 NFE, distilled model) 上，ImageReward 0.829 vs 0.691 (+0.138)。

## 概述

扩散模型在文本到图像（T2I）生成中取得了显著成功，但其主流采样方法——**无分类器引导（Classifier-Free Guidance, CFG）**——存在一个根本性瓶颈：标准 CFG 使用大于 1 的引导尺度 ω 进行外推，导致采样轨迹偏离真实数据流形，即**离流形（off-manifold）现象**。这一现象破坏了 DDIM 的可逆性，引发模态坍塌、颜色过饱和及结构性伪影等严重问题。

针对这一瓶颈，**CFG++** 提出了一种流形约束的引导范式。其核心洞察在于：将文本引导重新定义为最小化文本条件评分匹配损失（即 SDS 损失）的逆问题，并利用**分解扩散采样（Decomposed Diffusion Sampling, DDS）**将去噪与重噪声解耦。由此，CFG++ 在重噪声步骤中使用**无条件噪声估计**替代 CFG 的条件噪声估计，将引导尺度从外推区间（ω > 1）压缩到插值区间 λ ∈ [0, 1]，既保持了流形约束，又实现了从无条件到条件采样的平滑过渡与可逆性。

该方法在多个维度展现了显著优势。在 COCO 10k 的 50 步 DDIM T2I 任务中，CFG++ 在所有引导尺度上均获得更低的 FID，且 CLIP 相似度相当或更高。在 DDIM 反演重建任务中，CFG++ 显著提升了 PSNR 并降低了 RMSE，同时编辑结果更加忠实。在蒸馏加速模型（SDXL-Turbo、SDXL-Lightning）上，CFG++ 的 ImageReward 评分分别提升 0.191 和 0.138，且有效消除了 CFG 常见的伪影（如不自然的肢体、错误的文字渲染等）。

在方法谱系上，CFG++ 根植于扩散模型逆问题求解框架，与 **PSLD**（Rout et al., 2024）等潜在扩散逆问题求解器共享 DDS 的理论基础，但其贡献在于将这一思想系统性地引入文本引导采样，并以简洁的算法修改（仅改变重噪声步骤的噪声来源和引导尺度范围）实现了对标准 CFG 的实质性改进。消融实验表明，当重噪声步骤的条件噪声权值从 0（CFG++）逐渐增大到 1（CFG）时，图像质量（FID、ImageReward）持续恶化，验证了无条件重噪声对流形约束的关键作用。

CFG++ 的局限性主要包括：在极低 NFE（如 20 步 DPM++ 2M）采样中未展现出一致优势；反演仍基于 DDIM 近似假设，大步长下可能存在误差累积；以及需要在实际部署中通过 LPIPS 距离匹配合适的引导尺度 λ。其流形约束思想能否作为通用组件插入其他基于评分的生成框架，仍有待进一步探索。

## 背景与动机

扩散模型已成为文本到图像（T2I）生成的主流框架，其核心在于通过逐步去噪将高斯噪声转化为符合数据分布的样本。为了在采样过程中注入文本条件控制，**分类器自由引导（Classifier-Free Guidance, CFG）** 已成为事实上的标准技术。CFG 通过在推理时外推条件与无条件评分估计的差异来增强文本对齐：

$$\hat{\epsilon}_c^{\omega}(x_t) = \hat{\epsilon}_{\emptyset}(x_t) + \omega [ \hat{\epsilon}_c(x_t) - \hat{\epsilon}_{\emptyset}(x_t) ]$$

其中引导尺度 $\omega > 1.0$（典型值 2.0–30）控制条件信号的强度。尽管 CFG 在实践中广泛使用，但其工作机制存在一个根本性的瓶颈：**外推操作导致采样轨迹偏离真实数据流形（off-manifold phenomenon）**。

这一离流形现象源自两个相互叠加的因素。其一，$\omega > 1.0$ 的外推使去噪估计超出无条件与条件估计所张成的凸组合区间，在几何上偏离了数据流形的分段线性结构（见 Figure 3）。其二，CFG 在重噪声步骤（renoising step）中使用了条件噪声估计 $\hat{\epsilon}_c^{\omega}(\mathbf{x}_t)$，这引入了从真实流形偏离的非零偏移量 $\Delta^{\omega}$。两者共同作用，破坏了 DDIM 等确定性采样器的可逆性，并在实际生成中表现为**模态坍塌、过度颜色饱和、伪影以及不自然的人体结构**（如 Figure 1 中 SDXL-Turbo 生成的皮划艇图像出现明显伪影）。

从优化视角审视，CFG 在逆向扩散过程中并未显式优化任何与文本条件相关的损失函数。这导致其文本条件评分匹配损失（SDS loss）在采样早期出现剧烈波动，表明条件信号与样本质量之间存在不稳定的权衡（见 Figure 4）。这一问题在低步数采样（如蒸馏模型的 6 NFE 采样）中尤为突出，CFG 引导的图像往往伴随严重的结构失真。

针对上述缺陷，**CFG++** 从扩散模型逆问题求解器（DIS）的最新进展中获得启发，将文本引导重新定义为**以文本条件评分匹配损失为目标函数的逆问题**。该方法利用分解扩散采样（Decomposed Diffusion Sampling, DDS）将去噪与重噪声解耦，从而在重噪声步骤中使用无条件噪声估计 $\hat{\epsilon}_{\emptyset}(\mathbf{x}_t)$，并将引导尺度缩小到插值区间 $\lambda \in [0.0, 1.0]$。这一设计既保持了流形约束，又实现了从无条件到条件采样的平滑过渡，同时恢复了 DDIM 的可逆性，为图像反演与编辑等下游任务提供了更可靠的基础。

## 核心创新

### 问题本质：CFG 的离流形困境

标准分类器自由引导（CFG）通过外推条件与无条件评分之差来强化文本对齐：

$$
\hat{\epsilon}_c^{\omega}(x_t) = \hat{\epsilon}_{\emptyset}(x_t) + \omega [ \hat{\epsilon}_c(x_t) - \hat{\epsilon}_{\emptyset}(x_t) ]
$$

当引导尺度 $\omega > 1.0$（典型值 2.0–30）时，该外推操作将去噪估计推离真实数据流形。如图 3 所示，这一离流形（off-manifold）现象源于两个机制性瓶颈：

1. **外推偏离**：$\omega > 1$ 使后验均值估计沿条件方向过度偏移，脱离分段线性数据流形。
2. **重噪声偏移累积**：CFG 在重噪声步骤中使用条件噪声估计 $\hat{\epsilon}_c^{\omega}(x_t)$，引入非零偏移量 $\Delta^\omega$，使采样轨迹持续偏离正确流形。

这些因素共同导致 CFG 在采样早期出现剧烈损失波动（图 4），破坏 DDIM 的可逆性，并引发模态坍塌、颜色过饱和与结构性伪影。

### 核心洞察：引导即逆问题

CFG++ 的根本创新在于**将文本引导重新定义为逆问题**。具体而言，文本条件生成被形式化为最小化文本条件评分匹配损失（即 SDS 损失）的优化问题：

$$
\ell_{sds}(x) := \| \epsilon_{\theta}(\sqrt{\bar{\alpha}_t} x + \sqrt{1 - \bar{\alpha}_t} \epsilon, c) - \epsilon \|_2^2
$$

利用分解扩散采样（DDS）规避评分雅可比计算，CFG++ 将去噪与重噪声解耦：

$$
\mathbf{x}_{t-1} \simeq \sqrt{\bar{\alpha}_{t-1}} \left( \hat{\boldsymbol{x}}_{\emptyset} - \gamma_t \nabla_{\hat{\boldsymbol{x}}_{\emptyset}} \ell(\hat{\boldsymbol{x}}_{\emptyset}) \right) + \sqrt{1 - \bar{\alpha}_{t-1}} \hat{\boldsymbol{\epsilon}}_{\emptyset}
$$

这一重构带来了三个关键改变（changed slots），构成 CFG++ 的核心创新体系。

### Changed Slot 1：引导尺度从外推到插值

| 维度 | CFG | CFG++ |
|------|-----|-------|
| 引导尺度范围 | $\omega > 1.0$（外推） | $\lambda \in [0.0, 1.0]$（插值） |
| 去噪估计构成 | $\hat{x}_c^{\omega} = (1-\omega)\hat{x}_{\emptyset} + \omega\hat{x}_c$ | $\hat{x}_c^{\lambda} = (1-\lambda)\hat{x}_{\emptyset} + \lambda\hat{x}_c$ |

CFG++ 将引导尺度从外推区间压缩至插值区间 $[0,1]$，使去噪估计始终位于无条件估计与条件估计的凸组合内。这从根本上避免了外推导致的流形偏离——$\lambda=0$ 对应纯无条件采样，$\lambda=1$ 对应最大条件强度，过渡平滑且始终保持在数据流形上。实验表明，$\lambda=1.0$ 在 50 NFE DDIM 下的引导效果约等效于 CFG 的 $\omega \sim 12.5$，但无需承受外推伪影。

### Changed Slot 2：重噪声步骤从条件噪声到无条件噪声

CFG++ 最简洁却最关键的改变在于重噪声步骤的噪声源切换（图 2）：

- **CFG**：使用条件引导噪声 $\hat{\epsilon}_c^{\omega}(\mathbf{x}_t)$ 进行重噪声，携带离流形偏移量 $\Delta^\omega$。
- **CFG++**：使用无条件噪声 $\hat{\epsilon}_{\emptyset}(\mathbf{x}_t)$ 进行重噪声，保持流形约束。

CFG++ 的 DDIM 单步更新因此变为：

$$
\mathbf{x}_{t-1} = \sqrt{\bar{\alpha}_{t-1}} \hat{\boldsymbol{x}}_c^{\lambda}(\mathbf{x}_t) + \sqrt{1 - \bar{\alpha}_{t-1}} \hat{\boldsymbol{\epsilon}}_{\emptyset}(\mathbf{x}_t)
$$

这一改变使条件信号仅通过去噪估计 $\hat{\boldsymbol{x}}_c^{\lambda}$ 注入，而重噪声过程始终锚定在无条件流形上。消融实验（Table 4）证实，将重噪声步骤的条件噪声权值从 0（CFG++）逐渐增至 1（CFG）时，FID 和 ImageReward 均持续恶化，验证了无条件重噪声对流形保持的决定性作用。

### Changed Slot 3：优化目标从隐式引导到显式损失最小化

CFG 通过评分外推间接增强条件对齐，缺乏显式的优化目标。CFG++ 则直接最小化文本条件评分匹配损失，使条件对齐成为采样过程的内在优化目标。图 4 的损失曲线揭示了这一差异的实质影响：

- **CFG**：采样早期损失剧烈波动，对应图 1 底部所示的去噪估计突变与颜色过早饱和。
- **CFG++**：损失平滑下降，去噪估计从低分辨率到高分辨率平稳过渡，无突变或伪影累积。

这种平滑性源于 DDS 框架将条件损失梯度直接作用于去噪估计，而非通过噪声空间的外推间接影响。CFG++ 的后验均值演化可分解为：

$$
d\hat{\boldsymbol{x}}_c^{\lambda}(\mathbf{x}_t) = \frac{\sqrt{1-\bar{\alpha}_t}}{\sqrt{\bar{\alpha}_t}} d\hat{\boldsymbol{\epsilon}}_{\emptyset}(\mathbf{x}_t) + \lambda \Delta(\mathbf{x}_t, \mathbf{c})
$$

其中条件偏移 $\lambda \Delta$ 被严格控制在插值范围内，避免了 CFG 中 $\omega \Delta$ 的过度放大。

### 创新协同效应

三个 changed slots 形成闭环：**插值尺度**（Slot 1）确保去噪估计不脱离流形，**无条件重噪声**（Slot 2）阻断偏移累积，**显式损失最小化**（Slot 3）提供平滑的条件对齐信号。三者共同实现了 CFG++ 的核心承诺——在保持或提升文本对齐（CLIP 相似度相当或更高）的同时，显著降低 FID（COCO 10k 上从 13.84 降至 12.75），并恢复 DDIM 的可逆性以支持高质量反演与编辑。

## 整体框架

CFG++ 的整体 pipeline 建立在一个核心洞察之上：**标准 CFG 的离流形现象源于重噪声步骤使用了条件噪声估计**，而 CFG++ 通过将文本引导重新定义为逆问题优化，在保持去噪估计条件化的同时，将重噪声步骤的噪声源替换为无条件噪声估计，从而将整个采样过程约束在数据流形附近。

### 模块构成与数据流

CFG++ 的采样流程由四个紧密耦合的模块组成，其输入为纯噪声 `x_T ~ N(0, I)` 和文本条件 `c`，输出为生成图像 `x_0`。

**1. 引导噪声计算**  
该模块接收当前噪声样本 `x_t` 和时间步 `t`，分别通过无条件评分网络 `ε̂_∅(x_t)` 和条件评分网络 `ε̂_c(x_t)` 获得两个噪声估计。与标准 CFG 直接对噪声估计进行外推不同，CFG++ 在此阶段**仅记录两个噪声估计**，实际的引导操作被推迟到去噪估计模块中完成。这一设计选择是 CFG++ 与 CFG 在算法层面的首个关键分叉点——CFG 在此步骤即产生引导噪声 `ε̂_c^ω(x_t) = ε̂_∅(x_t) + ω[ε̂_c(x_t) - ε̂_∅(x_t)]`，而 CFG++ 保留了两个独立的噪声源。

**2. 去噪估计**  
利用 Tweedie 公式，将两个噪声估计分别转换为干净样本的预测：

- 无条件预测：`x̂_∅(x_t) = (x_t - √(1-ᾱ_t) ε̂_∅(x_t)) / √ᾱ_t`
- 条件预测：`x̂_c(x_t) = (x_t - √(1-ᾱ_t) ε̂_c(x_t)) / √ᾱ_t`

随后，CFG++ 在**干净样本空间**进行插值，而非在噪声空间进行外推：

```
x̂_c^λ(x_t) = (1 - λ) x̂_∅(x_t) + λ x̂_c(x_t)
```

其中 `λ ∈ [0, 1]` 为引导尺度。这一插值操作是 CFG++ 流形约束的几何基础：当 `λ = 0` 时退化为无条件采样，当 `λ = 1` 时完全采用条件估计，中间值则在两个数据流形点之间进行凸组合，**天然保证结果位于数据流形的凸包内**，避免了 CFG 因 `ω > 1` 外推导致的离流形偏移。

**3. 重噪声及下一步采样**  
这是 CFG++ 与 CFG 最关键的差异点。CFG 的重噪声步骤使用条件引导噪声 `ε̂_c^ω(x_t)`，在流形上引入了非零偏移量 `Δ^ω`（见 Figure 3）；而 CFG++ 的重噪声步骤**完全使用无条件噪声估计 `ε̂_∅(x_t)`**，以 DDIM 为例的更新公式为：

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_E77uvbOTtp/figures/002_Figure_3.jpg]]
*Figure 3: Off-manifold phenomenon of CFG arise from: (a) the typical CFG scale*

```
x_{t-1} = √ᾱ_{t-1} x̂_c^λ(x_t) + √(1 - ᾱ_{t-1}) ε̂_∅(x_t)
```

这一设计的因果机制在于：条件信息已通过去噪估计 `x̂_c^λ(x_t)` 注入到干净样本预测中，重噪声步骤仅需将样本推回扩散轨迹的正确噪声水平，使用无条件噪声即可保持流形一致性。Figure 2 的算法对比清晰展示了这一差异——CFG++ 仅需将 CFG 算法中重噪声步骤的 `ε̂_c^ω(x_t)` 替换为 `ε̂_∅(x_t)`，即可实现流形约束。

**4. 文本条件评分匹配损失**  
CFG++ 将文本引导重新定义为最小化 SDS 损失的逆问题：

```
ℓ_sds(x) := ‖ε_θ(√ᾱ_t x + √(1-ᾱ_t) ε, c) - ε‖₂²
```

通过分解扩散采样（DDS）求解该优化问题，避免了评分雅可比矩阵的计算。DDS 的核心思想是将去噪步骤与重噪声步骤解耦，使得条件损失仅影响去噪估计，而重噪声保持扩散过程的固有动力学。Figure 4 的损失曲线验证了这一设计的有效性：CFG++ 在整个逆向扩散过程中的文本条件评分匹配损失始终低于 CFG，尤其在早期步骤中，CFG 的损失出现剧烈波动，而 CFG++ 保持平滑下降，表明其更稳定地逼近文本条件分布。

### 与 CFG 的流程对比

| 模块 | CFG | CFG++ |
|------|-----|-------|
| 噪声估计 | `ε̂_c^ω(x_t) = ε̂_∅ + ω(ε̂_c - ε̂_∅)` | 保留 `ε̂_∅` 和 `ε̂_c` 两个独立估计 |
| 去噪估计 | `x̂_c^ω = (1-ω)x̂_∅ + ωx̂_c`（ω > 1 外推） | `x̂_c^λ = (1-λ)x̂_∅ + λx̂_c`（λ ∈ [0,1] 插值） |
| 重噪声 | 使用条件噪声 `ε̂_c^ω(x_t)` | 使用无条件噪声 `ε̂_∅(x_t)` |
| 引导尺度范围 | ω > 1.0（典型 2.0–30） | λ ∈ [0.0, 1.0] |

### 通用求解器扩展

CFG++ 不仅适用于 DDIM，还可推广到一般 ODE 采样器。对于通用求解器，其更新形式为：

```
x_i = x̂_c^λ(x_{i-1}) + a_i x̂_∅(x_{i-1}) + b_i x̂_∅(x_{i-2}) + c_i x_{i-1} + d_i ε
```

其中系数 `a_i, b_i, c_i, d_i` 由具体求解器决定。该扩展保持了 CFG++ 的核心原则：去噪估计使用条件插值，而所有重噪声项均使用无条件估计，确保流形约束在不同采样器下的一致性。

### 反演流程

CFG++ 的流形约束特性使其天然支持 DDIM 反演。由于重噪声使用无条件噪声，反演过程可通过近似公式实现：

```
x̂_c^λ(x_t) ≃ (x_{t-1} - √(1-ᾱ_{t-1}) ε̂_∅(x_{t-1})) / √ᾱ_{t-1}
```

CFG++ 反演的误差界 `‖ε_cfg++‖ = λ‖δ ε̂_c(x_t) - δ ε̂_c(x_{t-1})‖` 严格小于 CFG 反演误差，这为图像编辑等需要精确反演的任务提供了理论优势。实验表明，CFG++ 在反演重建任务中显著提升了 PSNR 并降低了 RMSE（Figure 6b），编辑结果也更加忠实于原始图像结构。

## 核心模块与公式推导

### 问题重构：文本引导作为逆问题优化

CFG++ 的核心思路是将文本条件引导重新定义为以**文本条件评分匹配损失**（即 SDS 损失）为目标的逆问题优化。不同于标准 CFG 直接对条件与无条件评分进行外推插值，CFG++ 通过显式最小化该损失来实现条件对齐：

$$\ell_{sds}(x) := \| \epsilon_{\theta}(\sqrt{\bar{\alpha}_t} x + \sqrt{1 - \bar{\alpha}_t} \epsilon, c) - \epsilon \|_2^2$$

其中 $x$ 为待优化的干净图像估计，$\epsilon_{\theta}$ 为预训练扩散模型，$c$ 为文本条件，$\epsilon \sim \mathcal{N}(0, I)$ 为注入噪声。该损失度量了当前估计在条件模型下的评分匹配误差，直接驱动生成结果向文本描述对齐。

### 关键模块一：分解扩散采样（DDS）求解器

为避免直接优化 SDS 损失时所需的评分雅可比计算，CFG++ 采用**分解扩散采样**（Decomposed Diffusion Sampling, DDS）策略。DDS 将去噪估计与重噪声过程解耦，其单步更新形式为：

$$\mathbf{x}_{t-1} \simeq \sqrt{\bar{\alpha}_{t-1}} \left( \hat{\boldsymbol{x}}_{\emptyset} - \gamma_t \nabla_{\hat{\boldsymbol{x}}_{\emptyset}} \ell(\hat{\boldsymbol{x}}_{\emptyset}) \right) + \sqrt{1 - \bar{\alpha}_{t-1}} \hat{\boldsymbol{\epsilon}}_{\emptyset}$$

其中 $\hat{\boldsymbol{x}}_{\emptyset}$ 为无条件去噪估计（由 Tweedie 公式给出），$\gamma_t$ 为步长参数，$\hat{\boldsymbol{\epsilon}}_{\emptyset}$ 为无条件噪声估计。该分解使得条件损失的梯度仅作用于去噪估计 $\hat{\boldsymbol{x}}_{\emptyset}$，而重噪声步骤始终使用无条件噪声，从而将采样过程约束在数据流形附近。

### 关键模块二：引导噪声计算与去噪估计插值

CFG++ 的引导机制通过引入引导尺度 $\lambda \in [0, 1]$ 实现无条件与条件估计之间的**插值**，而非 CFG 的 $\omega > 1$ 外推。去噪估计的插值形式为：

$$\hat{x}_c^{\lambda}(\mathbf{x}_t) = (1 - \lambda) \hat{x}_{\emptyset}(\mathbf{x}_t) + \lambda \hat{x}_c(\mathbf{x}_t)$$

其中 $\hat{x}_{\emptyset}$ 和 $\hat{x}_c$ 分别为无条件和条件去噪估计。当 $\lambda = 0$ 时退化为纯无条件采样，$\lambda = 1$ 时等价于强条件引导（实验中约对应 CFG 的 $\omega \sim 12.5$）。这一插值设计确保了去噪估计始终位于无条件与条件估计的张成空间内，从根本上避免了外推导致的离流形现象。

### 关键模块三：重噪声与采样步（DDIM 形式）

CFG++ 的 DDIM 采样步在重噪声阶段**使用无条件噪声估计** $\hat{\boldsymbol{\epsilon}}_{\emptyset}(\mathbf{x}_t)$，而非 CFG 中使用的条件引导噪声 $\hat{\boldsymbol{\epsilon}}_c^{\omega}(\mathbf{x}_t)$：

$$\mathbf{x}_{t-1} = \sqrt{\bar{\alpha}_{t-1}} \hat{\boldsymbol{x}}_c^{\lambda}(\mathbf{x}_t) + \sqrt{1 - \bar{\alpha}_{t-1}} \hat{\boldsymbol{\epsilon}}_{\emptyset}(\mathbf{x}_t)$$

这一替换是 CFG++ 与 CFG 的本质差异（见 Figure 2, Algorithm 2）。CFG 的重噪声因使用条件噪声而引入非零偏移量 $\Delta^{\omega}$，将后验均值推离数据流形；CFG++ 通过使用无条件噪声消除了该偏移，使得采样轨迹始终保持流形约束。

### 关键模块四：通用 ODE 求解器扩展

CFG++ 可推广至一般 ODE 采样器，其通用更新形式为：

$$\mathbf{x}_i = \hat{x}_c^{\lambda}(\mathbf{x}_{i-1}) + a_i \hat{x}_{\emptyset}(\mathbf{x}_{i-1}) + b_i \hat{x}_{\emptyset}(\mathbf{x}_{i-2}) + c_i \mathbf{x}_{i-1} + d_i \epsilon$$

其中 $a_i, b_i, c_i, d_i$ 由具体求解器决定，$\epsilon \sim \mathcal{N}(0, I)$ 为随机噪声。该形式保持了去噪估计的条件插值与重噪声的无条件特性，可适配 DPM-Solver 等加速采样器。

### 关键模块五：DDIM 反演

CFG++ 的流形约束特性使其支持近似的 DDIM 反演。给定生成图像 $\mathbf{x}_{t-1}$，可近似恢复 $\mathbf{x}_t$：

$$\hat{\boldsymbol{x}}_c^{\lambda}(\mathbf{x}_t) \simeq (\mathbf{x}_{t-1} - \sqrt{1 - \bar{\alpha}_{t-1}} \hat{\boldsymbol{\epsilon}}_{\emptyset}(\mathbf{x}_{t-1})) / \sqrt{\bar{\alpha}_{t-1}}$$

CFG++ 反演误差 $\| \varepsilon_{cfg++} \| = \lambda \| \delta \hat{\epsilon}_c(\mathbf{x}_t) - \delta \hat{\epsilon}_c(\mathbf{x}_{t-1}) \|$ 显著小于 CFG 反演误差，因为 CFG 的误差项包含额外的 $\omega$ 缩放因子，在大引导尺度下被急剧放大。

### 核心机制总结

CFG++ 的五个关键模块协同实现流形约束引导：**SDS 损失**提供文本对齐的优化目标；**DDS 求解器**解耦去噪与重噪声，避免雅可比计算；**去噪插值**（$\lambda \in [0,1]$）替代外推，消除离流形风险；**无条件重噪声**消除 CFG 中的偏移量 $\Delta^{\omega}$；**DDIM 反演**因误差受控而显著改善重建与编辑质量。整个框架仅修改了重噪声步骤的噪声来源和引导尺度的取值范围，即可在保持计算开销不变的前提下获得平滑的生成轨迹和更低的文本条件评分匹配损失（见 Figure 4）。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_E77uvbOTtp/figures/003_Figure_4.jpg]]
*Figure 4: Text-conditioned score matching loss throughout the reverse diffusion sampling for both CFG and CFG++ in SDXL. Avg. loss computed with 55 prompts from (Chen et al., 2024)*

### 补充图表

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_E77uvbOTtp/figures/010_Figure_9.jpg]]
*Figure 9: Continuous transition between CFG and CFG++ schedule*

## 实验与分析

### 核心定量结果：T2I 生成质量与文本对齐

CFG++ 在标准文本到图像（T2I）生成基准上展现出对 CFG 的一致优势。在 COCO 10k 验证集上使用 SD v1.5 模型进行 50 步 DDIM 采样，CFG++ 在所有引导尺度上的 FID 均低于 CFG，同时 CLIP 相似度相当或更高（Table 1）。具体而言，当 CFG 使用典型引导尺度 ω=2.0 时，CFG++ 在匹配的 λ=0.2 下将 FID 从 13.84 降至 12.75（降幅 1.09），CLIP 从 0.298 提升至 0.303。在强引导条件下（ω=12.5 vs λ=1.0），CFG++ 同样保持 FID 优势（20.88 vs 21.23）。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_E77uvbOTtp/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation of 50 NFE DDIM T2I with SD v1.5 on COCO 10k*

在加速采样场景中，CFG++ 的优势更为显著。在 SDXL-Turbo（蒸馏模型，6 NFE）上，CFG++ 将 ImageReward 指标从 0.777 提升至 0.968（提升 0.191）；在 SDXL-Lightning 上，从 0.691 提升至 0.829（提升 0.138）（Table 2）。这表明流形约束引导对低步数采样同样有效，且能显著改善生成图像的审美质量与文本一致性。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_E77uvbOTtp/figures/005_Table_2.jpg]]
*Table 2: Quant. eval. on accelerated T2I sampling*

### 流形约束的可视化验证

Figure 1 提供了三个层面的定性证据：（1）T2I 结果中，CFG 引导的图像出现明显伪影，而 CFG++ 版本显著减少；（2）DDIM 反演结果中，CFG 在不同引导尺度下均产生可察觉的噪声伪影，CFG++ 大幅缓解；（3）去噪估计演化轨迹显示，CFG 在逆向扩散早期出现突变的颜色饱和与剧烈偏移，而 CFG++ 呈现从低分辨率到高分辨率的平滑过渡。这一现象与 Figure 4 的文本条件评分匹配损失曲线一致：CFG++ 的损失在整个逆向扩散过程中平滑下降，而 CFG 在早期阶段出现剧烈波动，验证了 CFG++ 直接优化该损失带来的文本对齐优势。

### 离流形现象的因果消融

Figure 3 揭示了 CFG 离流形现象的双重根源：（a）引导尺度 ω>1.0 导致外推，使估计偏离分段线性的数据流形；（b）重噪声步骤引入非零偏移量 Δ^ω，进一步将后验均值推离正确流形。CFG++ 通过将引导尺度限制在插值区间 λ∈[0,1] 并在重噪声步骤使用无条件噪声估计 $\hat{\epsilon}_{\emptyset}(x_t)$，从根本上消除这两个因素。

Table 4 的插值消融实验提供了因果证据：通过调整重噪声步骤中的条件噪声权值 ω' 从 0（CFG++）到 1（CFG）进行连续过渡，图像质量指标（FID、ImageReward）随 ω' 增大而逐渐恶化。这直接证明了重噪声步骤使用无条件噪声是 CFG++ 性能提升的关键操作。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_E77uvbOTtp/figures/011_Table_4.jpg]]
*Table 4: Quantitative results of COCO-1k by interpolating between CFG and CFG++*

### 反演与编辑任务中的可逆性恢复

CFG++ 恢复了 DDIM 的可逆性，这在反演-重建-编辑流程中至关重要。Figure 6（b）的定量对比显示，CFG++ 在重建任务中显著提升 PSNR 并降低 RMSE。理论分析表明，CFG++ 的反演误差范数 $||\epsilon_{cfg++}|| = \lambda ||\delta \hat{\epsilon}_c(x_t) - \delta \hat{\epsilon}_c(x_{t-1})||$ 严格小于 CFG 的对应误差，因为 λ∈[0,1] 而 CFG 的等效系数为 ω>1.0 的外推值。Figure 6（c）的图像编辑对比进一步证实，CFG++ 的编辑结果更加忠实于原始图像结构，避免了 CFG 常见的伪影累积。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_E77uvbOTtp/figures/007_Figure_6.jpg]]
*Figure 6: Inversion and editing results. (a) Reconstructed samples after inversion by CFG and CFG++. (b) Quantitative comparison between CFG and CFG++ for reconstruction. (c) Image editing comparison via SDXL*

### 逆问题求解器上的泛化验证

CFG++ 作为即插即用的引导策略，可直接集成到现有的扩散模型逆问题求解器中。在 PSLD（Rout et al., 2024）框架下，CFG++ 在多种逆问题（超分辨率、修复、去模糊等）上均展现出优于 CFG 的重建质量（Figure 7）。Table 3 的定量指标（FID、LPIPS、PSNR）表明，PSLD+CFG++ 在所有任务上均优于 PSLD+CFG 和原始 PSLD，验证了流形约束引导在更广泛生成场景中的有效性。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_E77uvbOTtp/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative comparison on various inverse problems using PSLD (Rout et al., 2024) under CFG and CFG++. For more results, please refer to the Appendix F*

### 失败模式与局限性

尽管 CFG++ 在多数场景下表现优异，但存在以下已知边界：

1. **低 NFE 求解器兼容性**：在 20 步 DPM++ 2M 采样中，CFG++ 并未一致优于 CFG。这可能与该求解器的步长策略与 CFG++ 的重噪声机制存在未调和的交互有关，需要进一步验证。

2. **反演近似误差**：CFG++ 的 DDIM 反演仍基于近似公式 $\hat{x}_c^{\lambda}(x_t) \simeq (x_{t-1} - \sqrt{1-\bar{\alpha}_{t-1}}\hat{\epsilon}_{\emptyset}(x_{t-1}))/\sqrt{\bar{\alpha}_{t-1}}$，在大步长或极低 NFE 下可能存在误差累积。

3. **超参数匹配成本**：实验中通过 LPIPS 距离匹配 CFG 的 ω 与 CFG++ 的 λ，实际部署时可能需要针对不同模型和任务调整引导尺度。

4. **模型架构依赖**：CFG++ 依赖明确的无条件评分通道 $\hat{\epsilon}_{\emptyset}$，对于无此通道的模型需要额外适配。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_E77uvbOTtp/figures/006_Figure_5.jpg]]
*Figure 5: T2I using SDXL-{turbo, lightning}, 6 NFE, CFG vs CFG++*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_E77uvbOTtp/figures/013_Figure_10.jpg]]
*Figure 10: Enhanced T2I results by SDXL (ω = 9.0, λ = 0.8) with CFG++. Under CFG, the lion cub is not visible (top-left), the dog appears with two tails (top-right), the goggles have an unusual shape (bottom-left), and the tree trunk is folded (bottom-right). These artifacts are absent in those produced by CFG++*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_E77uvbOTtp/figures/015_Figure_11.jpg]]
*Figure 11: T2I using SD v1.5, CFG vs CFG++ (ω = 9.0, λ = 0.8). Unnatural depictions of human hands, and incorrect renderings of the text by CFG are corrected in CFG++*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_E77uvbOTtp/figures/014_Figure_12.jpg]]
*Figure 12: T2I using SDXL-Turbo, 6 NFE, CFG vs CFG++. The overall image quality and sophistication have improved with CFG++. DreamShaper XL was used for both images and metrics in main part*

## 方法谱系与知识库定位

### 与标准分类器自由引导（CFG）的继承与突破

CFG++ 直接建立在标准分类器自由引导（Classifier-Free Guidance, CFG）的采样框架之上，但对其核心机制进行了根本性重构。CFG 通过在每一步去噪过程中对条件与无条件评分进行外推（典型引导尺度 ω > 1.0），以牺牲样本多样性与流形一致性为代价换取文本对齐度的提升。CFG++ 保留了 CFG 同时调用条件与无条件模型的架构，但将引导机制从“评分外推”转变为“优化驱动的插值”：它将文本引导重新定义为最小化文本条件评分匹配损失（即 SDS 损失）的逆问题，并借助分解扩散采样（DDS）在重噪声步骤中使用无条件噪声估计，从而将引导尺度 λ 约束在 [0, 1] 的插值区间内。

这一转变的核心差异体现在三个关键槽位上：

| 组件 | CFG（基线） | CFG++（本文） |
|------|------------|--------------|
| 重噪声步骤的噪声估计 | $\hat{\boldsymbol{\epsilon}}_c^{\omega}(\mathbf{x}_t)$（条件噪声） | $\hat{\boldsymbol{\epsilon}}_{\emptyset}(\mathbf{x}_t)$（无条件噪声） |
| 引导尺度范围 | ω > 1.0（典型 2.0–30） | λ ∈ [0.0, 1.0]（插值因子） |
| 去噪估计构成 | $\hat{x}_c^{\omega} = (1-\omega)\hat{x}_{\emptyset} + \omega\hat{x}_c$（外推） | $\hat{x}_c^{\lambda} = (1-\lambda)\hat{x}_{\emptyset} + \lambda\hat{x}_c$（插值） |

重噪声步骤从条件噪声切换为无条件噪声是 CFG++ 实现流形约束的关键：标准 CFG 在重噪声时引入了偏离真实数据流形的偏移量 $\Delta^{\omega}$（见 Figure 3），而 CFG++ 通过使用无条件噪声消除了这一偏移，使采样轨迹始终保持在数据流形附近。引导尺度从外推区间改为插值区间则进一步确保去噪估计不会“脱离”干净数据流形——这是 CFG 在高 ω 下产生颜色饱和、模态坍塌和伪影的结构性根源。

### 与扩散逆问题求解器的关系

CFG++ 的方法论灵感直接来源于扩散模型逆问题求解器（Diffusion Inverse Solvers, DIS）领域的最新进展。其核心推导路径是：将文本条件评分匹配损失 $\ell_{sds}(x)$ 作为优化目标，然后应用分解扩散采样（DDS）来避免评分雅可比矩阵的计算。DDS 本身是逆问题求解中用于高效近似梯度下降的技术，CFG++ 将其引入文本引导采样，实现了条件损失最小化与采样效率的统一。

在逆问题场景中，CFG++ 被作为 **PSLD**（Rout et al., 2024）这一潜在扩散逆问题求解器的替代引导策略进行了验证。实验表明，将 PSLD 中的标准 CFG 替换为 CFG++ 后，在多种退化类型（超分辨率、修复、去模糊等）上均取得一致的性能提升（Table 3, Figure 7）。这说明 CFG++ 的流形约束思想并非局限于文本到图像生成，而是可以作为通用组件插入基于评分的逆问题求解框架。

### 适用边界与部署约束

CFG++ 的适用性受以下条件约束：

1. **模型架构依赖**：该方法要求扩散模型具有明确的无条件评分通道 $\hat{\epsilon}_{\emptyset}$。对于未训练无条件通道的模型，需要额外适配或微调。
2. **引导尺度匹配**：实际部署时需通过 LPIPS 距离等感知度量将 CFG++ 的 λ 与目标 CFG 的 ω 进行匹配，超参数调整并非完全自动化。
3. **采样器兼容性**：在 50 NFE DDIM 采样中优势显著，但在极低 NFE（如 20 步）的 DPM++ 2M 采样中并未展现出一致改进，表明该方法对采样器类型和步数存在一定敏感性。
4. **应用场景验证范围**：目前仅在文本到图像生成、DDIM 反演、图像编辑和线性逆问题上进行了验证，尚未在视频扩散模型、3D 生成或一致性模型等更广泛的生成框架中测试。

### 局限性与开放问题

**已识别的局限**：

- CFG++ 的 DDIM 反演仍基于近似假设（Eq. 19），对于大步长或极低 NFE 场景可能存在误差累积，尽管其反演误差在理论上小于 CFG（$\|\varepsilon_{cfg++}\| = \lambda \|\delta \hat{\epsilon}_c(x_t) - \delta \hat{\epsilon}_c(x_{t-1})\| < \|\varepsilon_{cfg}\|$）。
- 在蒸馏模型（如 SDXL-Turbo/Lightning）上的加速采样实验中，CFG++ 在 ImageReward 指标上大幅领先 CFG（SDXL-Turbo: 0.968 vs 0.777; SDXL-Lightning: 0.829 vs 0.691），但 FID 和 CLIP 的对比数据在 Table 2 中未完整报告，需进一步验证整体质量-文本对齐的权衡。

**待探索的开放问题**：

1. **采样器-步数交互机制**：为何 CFG++ 在 20 NFE DPM++ 2M 中未展现一致改进，而在 50 NFE DDIM 中优势明显？这可能与高阶求解器的误差传播特性有关，需要更深入的理论分析。
2. **引导尺度函数的优化**：CFG++ 使用的凸形引导尺度调度函数（Figure 9）如何具体影响样本多样性与保真度的权衡？是否存在更优的调度策略？
3. **跨框架泛化**：CFG++ 的流形约束思想能否作为通用组件插入一致性模型（Consistency Models）或其他基于评分的生成框架？
4. **高分辨率与视频扩展**：在极高分辨率生成或视频扩散模型中的表现尚未验证，这些场景对流形一致性的要求可能更高。
5. **理论收敛性**：能否从理论上更严格地刻画 CFG++ 的收敛性以及与 CFG 之间的误差界？目前的反演误差分析仅提供了上界比较，缺乏收敛速率或渐进性质的分析。

> **注意**：CFG++ 在文本对齐损失（Figure 4）上的平滑性与更低绝对值提供了其优化目标有效性的直接证据，但该损失曲线仅基于 55 个提示词计算，统计显著性需要更大规模验证。消融实验（Table 4）通过插值重噪声步骤中的条件噪声权值 ω' 从 0（CFG++）到 1（CFG）确认了无条件重噪声的关键作用，但该实验仅在 COCO-1k 子集上进行，结论的泛化性需要进一步确认。

## 原文 PDF

![[paperPDFs/ICLR_2025/CFG_Manifold_constrained_Classifier_Free_Guidance_for_Diffusion_Models.pdf]]