---
title: Adaptive Auxiliary Prompt Blending for Target-Faithful Diffusion Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Adaptive_Auxiliary_Prompt_Blending_for_Target_Faithful_Diffusion_Generation.pdf
project_link: null
code_link: null
aliases:
- AAPBA
- AAPBTFDG
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在每个扩散步骤中，通过自适应系数γ_t^*动态调节辅助锚点提示（频繁概念或源提示）与目标提示的贡献比例，从而修正分数空间中的漂移。
primary_logic: 基于Tweedie等式的后验均值对齐：最小化混合去噪器与目标去噪器之间的后验均值距离，等价于最小化分数空间误差，由此推导出闭式自适应系数γ_t^*，实现无训练、逐步最优的稳定生成。
claims:
- 在RareBench上，AAPB（基于SD3）的平均GPT-4o T2I对齐分数达到84.1，比最强基线R2F高8.4个点，在所有单/多对象类别中均取得最佳或次佳。
- 在FlowEdit图像编辑任务中，AAPB的结构保持指标CLIP-I达到0.905，DINO 0.814，LPIPS/DreamSim均低至0.155，显著优于FlowEdit等基线，同时维持相当的文本对齐。
- 消融实验显示，自适应系数在所有固定γ_t值上均取得更高生成质量，且自适应方法的2-Wasserstein距离低于任何固定插值，验证了逐步自适应的必要性。
- RareBench 上 GPT-4o T2I Alignment Avg. = 84.1
---

# Adaptive Auxiliary Prompt Blending for Target-Faithful Diffusion Generation

> [!tip] 核心洞察
> 基于Tweedie等式的后验均值对齐：最小化混合去噪器与目标去噪器之间的后验均值距离，等价于最小化分数空间误差，由此推导出闭式自适应系数γ_t^*，实现无训练、逐步最优的稳定生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向目标忠实扩散生成的自适应辅助提示融合 |
| 英文题名 | Adaptive Auxiliary Prompt Blending for Target-Faithful Diffusion Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.19158) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Adaptive Auxiliary Prompt Blending (AAPB) |
| Dataset | RareBench, FlowEdit |

> [!tip] 效果简介
> - RareBench 上，GPT-4o T2I Alignment Avg. 84.1 vs 75.7 (R2F) (+8.4)。
> - FlowEdit 上，CLIP-I ↑ 0.905 vs 0.872 (FlowEdit) (+0.033)；DINO ↑ 0.814 vs 0.719 (FlowEdit) (+0.095)；LPIPS ↓ 0.155 vs 0.181 (FlowEdit) (-0.026)。

## 概要

扩散模型在生成常见语义概念时表现优异，但当目标概念位于训练分布的长尾低密度区域时，去噪过程会不可控地偏向高频语义模式，导致罕见属性被压制、组合性丢失以及结构不一致。针对这一瓶颈，**Adaptive Auxiliary Prompt Blending (AAPB)** 提出了一种统一且无需训练的解决方案：在每个扩散步骤中，通过自适应系数 $\gamma_t^*$ 动态调节辅助锚点提示（频繁概念或源提示）与目标提示的贡献比例，从而修正分数空间中的漂移，实现目标忠实的生成。

AAPB 的核心洞察建立在 **Tweedie等式** 之上——最小化混合去噪器与目标去噪器之间的后验均值距离，等价于最小化分数空间误差。基于此等价性，方法推导出闭式自适应系数 $\gamma_t^*$，无需启发式调度或手动调参，即可在每一步实现最优的锚点-目标平衡。该系数直接由目标分数、锚点分数与无条件分数的内积关系动态计算，兼具理论优雅性与计算可行性。

在实验验证层面，AAPB 展现出显著且一致的性能优势：

- **罕见概念生成**：在 RareBench 基准上，基于 SD3 的 AAPB 取得 GPT-4o T2I 对齐平均分 **84.1**，比最强基线 R2F 高出 **8.4** 个点，在所有单/多对象类别中均达到最佳或次佳（Table 1）。
- **图像编辑**：在 FlowEdit 数据集上，AAPB 的结构保持指标 CLIP-I 达到 **0.905**、DINO 达到 **0.814**，LPIPS 与 DreamSim 均低至 **0.155**，显著优于 FlowEdit 等基线，同时维持相当的文本对齐水平（Table 2）。
- **消融验证**：自适应系数在所有固定 $\gamma_t$ 值上均取得更高的生成质量，且其 2-Wasserstein 距离低于任何固定插值方案，直接验证了逐步自适应的必要性（Figure 5, Figure 2(d)）。

AAPB 的方法定位清晰：它不依赖额外训练或模型微调，通过扩展分类器自由引导（CFG）的分数混合范式，将条件分数重新定义为目标分数与锚点分数的动态加权组合。该方法可无缝集成至现有扩散管线（如 SDXL、SD3.0、IterComp），并在与 R2F+ 区域控制管线结合时，将 RareBench-Multi 上的一致性提升 **9.4∼19.9** 个点（Table 6）。当前的主要局限在于 CLIP 文本编码器在多属性组合场景下的绑定能力不足，以及三路分数评估带来的适度计算开销，但这些并不妨碍 AAPB 作为训练自由、理论完备的扩散生成增强框架的实用价值。



### 扩散生成中的长尾漂移困境

扩散模型在文本到图像生成中取得了显著成功，但其去噪过程隐含地依赖训练分布中的统计先验。当目标概念位于训练分布的长尾低密度区域时，模型在分数空间中的采样轨迹会**偏向高频语义模式**，导致罕见属性被压制、组合性丢失以及结构不一致。这一现象的本质在于：扩散模型学习到的分数函数 $s_\theta(x_t)$ 在高密度区域具有更强的梯度信号，使得去噪过程自然地向语义主导概念漂移（Figure 1）。

具体而言，对于罕见概念生成任务，如“一只蓝色的长颈鹿”或“穿宇航服的猫”，模型倾向于忽略“蓝色”或“宇航服”等罕见属性，生成标准的长颈鹿或猫。在图像编辑任务中，当编辑指令涉及罕见属性变更时，模型难以在保持源图像结构的同时忠实地执行编辑。

### 现有方法的局限

当前应对这一问题的训练无关方法主要分为两类：

**固定系数插值**：在目标提示与辅助提示（如频繁概念或源提示）之间采用固定权重进行分数混合。然而，不同扩散步骤对辅助引导的需求强度不同——早期步骤需要更强的结构锚定，后期步骤则需要更精确的目标对齐。固定系数无法适应这种动态需求，导致生成结果在语义准确性与结构保真度之间陷入次优权衡（Figure 2(d)）。

**启发式调度**：以 **R2F** 为代表的方法使用LLM将罕见概念分解为多步子提示，并通过交替步骤进行生成。这种方法存在两个关键缺陷：一是交替调度本质上是一种粗糙的启发式策略，缺乏对每步最优混合比例的精确建模；二是多步子提示的重构过程容易导致实体纠缠——多个罕见概念被错误地合并为单一实体（Figure 11）。

### 核心动机：从后验均值对齐到自适应混合

本工作的核心动机源于一个关键观察：**扩散模型在每步去噪中的后验均值 $\mathbb{E}[x_0 \mid x_t]$ 可以通过Tweedie等式与分数函数建立精确联系**：

$$\mathbb{E}[x_0 \mid x_t] = x_t + (1 - \alpha_t) \nabla_{x_t} \log p(x_t)$$

这意味着，若能使混合去噪器与目标去噪器在每步的后验均值保持一致，则等价于在分数空间中最小化对齐误差。基于这一洞察，我们将辅助提示混合问题转化为一个**逐步优化问题**：在每个扩散步骤 $t$，寻找最优混合系数 $\gamma_t^*$，使得混合分数 $\tilde{s}_\theta(x_t; w, \gamma_t)$ 与目标分数 $s_\theta(x_t, \tilde{c}_T)$ 的 $L_2$ 距离最小化。

这一思路的直接优势在于：$\gamma_t^*$ 具有**闭式解**，无需任何训练或额外网络，且能够根据当前噪声状态 $x_t$ 动态调整目标提示与锚点提示的贡献比例。相比固定插值和启发式调度，自适应混合能够精确修正分数空间中的漂移，在保持目标忠实度的同时避免过度依赖锚点导致的结构偏离。



## 核心方法与创新机理

AAPB 的核心创新在于将扩散模型去噪过程中的**辅助提示融合从启发式固定调度提升为逐步最优的自适应机制**。与现有方法（如 R2F 的交替步骤或手动设定固定混合系数）不同，AAPB 通过理论推导给出了闭式自适应系数 $\gamma_t^*(x_t)$，在每个扩散步动态平衡目标提示与锚点提示的贡献。

### 从固定插值到自适应投影

现有训练无关方法通常采用固定系数 $\gamma_t$ 对目标分数与锚点分数进行线性插值。然而，当目标概念位于训练分布的长尾低密度区域时，去噪轨迹会偏向高频语义模式，导致罕见属性被压制。图 2 的玩具实验清晰地揭示了这一瓶颈：在固定插值下，即使选择最优的 $\gamma_t \approx 0.8$，生成分布与目标分布之间的 2-Wasserstein 距离仍显著高于自适应方法（图 2d 红色虚线）。自适应投影 $p(x|\tilde{c}_A, \tilde{c}_T; \gamma_t^*)$ 在每一步动态修正漂移，使得生成样本更准确地落在目标区域（图 2c vs 图 2b）。

### 基于 Tweedie 对齐的闭式系数推导

AAPB 的理论根基在于 **Tweedie 等式的后验均值对齐**。作者指出，最小化混合去噪器与目标去噪器之间的后验均值距离，等价于最小化分数空间误差。基于这一等价性，定义分数空间对齐损失：

$$\mathcal{L}(\gamma_t) = \|\tilde{s}_{\theta}(x_t; w, \gamma_t) - s_{\theta}(x_t, \tilde{c}_T)\|_2^2$$

对该损失求导并令其为零，直接得到闭式自适应系数：

$$\gamma_t^*(x_t) = \frac{1 - w}{w} \cdot \frac{\langle s_{\theta}(x_t, \tilde{c}_T) - s_{\theta}(x_t), s_{\theta}(x_t, \tilde{c}_A) - s_{\theta}(x_t, \tilde{c}_T) \rangle}{\| s_{\theta}(x_t, \tilde{c}_A) - s_{\theta}(x_t, \tilde{c}_T) \|_2^2}$$

该系数具有明确的几何解释：它根据目标分数与锚点分数在当前噪声状态 $x_t$ 下的相对方向，动态决定锚点的介入程度。当锚点分数与目标分数方向一致时，$\gamma_t^*$ 增大以利用锚点的稳定引导；当两者方向偏离时，$\gamma_t^*$ 减小以避免语义稀释。

### 统一的引导公式扩展

AAPB 将标准 Classifier-Free Guidance 扩展为三路分数混合：

$$\tilde{s}_{\theta}(x_t; w, \gamma_t) = s_{\theta}(x_t) + w \big( (1 - \gamma_t) s_{\theta}(x_t, \tilde{c}_T) + \gamma_t s_{\theta}(x_t, \tilde{c}_A) - s_{\theta}(x_t) \big)$$

与标准 CFG 相比，关键变化在于**条件分数不再固定为目标提示分数**，而是替换为目标分数与锚点分数的动态加权混合。这一改动使得 AAPB 可以无缝集成到任何预训练扩散模型中，无需额外训练或微调。

### 提示重构策略的改进

在罕见概念生成任务中，R2F 将罕见概念分解为多步子提示并交替生成，容易导致多个罕见概念坍缩为单一实体（图 11）。AAPB 采用更直接的策略：为每个罕见概念显式配对其频繁对应物（如将 “a rare blue-feathered bird” 映射为 “bird” 作为锚点），然后一次性重构完整提示。这种二元对映射避免了实体纠缠，使得每个罕见概念都能在生成中得到独立保留。

### 自适应系数的任务适应性

值得注意的是，$\gamma_t^*$ 在不同任务中展现出差异化的演化模式。在图像编辑中，$\gamma_t^*$ 在去噪后期趋于饱和，因为源图像的结构引导逐渐占据主导（图 9）；而在罕见概念生成中，$\gamma_t^*$ 在整个去噪过程中保持相对稳定，反映出对锚点稳定化的持续需求（图 10）。这种任务自适应性是固定系数方法无法实现的。

### 与基线的关键差异总结

| 改进维度 | 基线方法 | AAPB |
|---------|---------|------|
| 混合系数调整 | 手动固定值或启发式调度（如 R2F 交替步骤） | 基于 Tweedie 对齐的闭式自适应系数 $\gamma_t^*$，每步动态计算 |
| 引导公式 | 标准 CFG，条件分数固定为目标提示分数 | 扩展 CFG，条件分数为目标与锚点分数的动态加权混合 |
| 提示处理 | R2F 将罕见概念分解为多步子提示交替生成 | 直接构建罕见概念与其频繁对应物的二元对，一次性重构完整提示 |

这些创新共同构成了 AAPB 的统一框架，使其在罕见概念生成和图像编辑两个任务上均取得显著提升——在 RareBench 上以 84.1 的平均 T2I 对齐分数超越最强基线 R2F 达 8.4 个点（表 1），在 FlowEdit 上以 CLIP-I 0.905、DINO 0.814 的结构保持指标显著优于 FlowEdit 等基线（表 2）。



AAPB 是一个统一的、免训练的自适应辅助提示融合框架，旨在解决扩散模型在目标概念位于训练分布长尾低密度区域时的生成漂移问题。其核心思想源自一个关键洞察：当目标概念罕见时，去噪过程会偏向高频语义模式，导致罕见属性被压制、组合性丢失及结构不一致。AAPB 通过在每个扩散步骤中动态调节辅助锚点提示与目标提示的贡献比例，修正分数空间中的漂移，从而实现目标忠实的生成。

### 问题形式化与分数空间对齐

框架的理论基础建立在 Tweedie 等式之上。在高斯噪声假设下，给定噪声状态 $x_t$ 的后验均值可通过分数函数解析表达：

$$\mathbb{E}[x_0 \mid x_t] = x_t + (1 - \alpha_t) \nabla_{x_t} \log p(x_t)$$

这一等式建立了去噪后验均值与分数函数之间的桥梁。AAPB 的核心优化目标是：**最小化混合去噪器与目标去噪器之间的后验均值距离**。通过 Tweedie 等式，该目标等价于最小化分数空间中的平方误差，从而将图像空间的对齐问题转化为分数空间的可解优化问题。

具体而言，定义分数空间对齐损失：

$$\mathcal{L}(\gamma_t) = \|\tilde{s}_{\theta}(x_t; w, \gamma_t) - s_{\theta}(x_t, \tilde{c}_T)\|_2^2$$

其中 $\tilde{s}_{\theta}(x_t; w, \gamma_t)$ 为混合引导分数，$s_{\theta}(x_t, \tilde{c}_T)$ 为目标提示条件分数。通过最小化该损失，可推导出闭式自适应系数 $\gamma_t^*$，实现逐步最优的稳定生成。

### 管线模块与数据流

AAPB 的整体管线由六个核心模块串联构成，数据流从噪声初始状态 $x_T$ 出发，经迭代去噪最终生成 $x_0$：

1. **无条件分数估计**：计算与条件无关的基础分数 $s_{\theta}(x_t)$，作为 CFG 框架中的无条件基准。

2. **目标条件分数估计**：计算目标提示 $\tilde{c}_T$ 的条件分数 $s_{\theta}(x_t, \tilde{c}_T)$。在罕见概念生成任务中，$\tilde{c}_T$ 由罕见概念与其频繁对应物的二元对重构而来；在图像编辑任务中，$\tilde{c}_T$ 为编辑后的目标提示。

3. **锚点条件分数估计**：计算辅助锚点提示 $\tilde{c}_A$ 的条件分数 $s_{\theta}(x_t, \tilde{c}_A)$。锚点的角色因任务而异——罕见概念生成中使用语义对齐的频繁概念提示，图像编辑中使用未编辑的源提示。

4. **自适应系数计算**：根据闭式公式在每个扩散步骤 $t$ 动态计算最优混合系数：

   $$\gamma_t^*(x_t) = \frac{1 - w}{w} \cdot \frac{\langle s_{\theta}(x_t, \tilde{c}_T) - s_{\theta}(x_t), s_{\theta}(x_t, \tilde{c}_A) - s_{\theta}(x_t, \tilde{c}_T) \rangle}{\| s_{\theta}(x_t, \tilde{c}_A) - s_{\theta}(x_t, \tilde{c}_T) \|_2^2}$$

   该系数通过分数向量的内积与范数运算，量化了锚点分数相对于目标分数的有效引导方向，无需任何启发式调度或手动设定。

5. **混合分数融合**：将三路分数按扩展 CFG 公式融合为最终引导分数：

   $$\tilde{s}_{\theta}(x_t; w, \gamma_t) = s_{\theta}(x_t) + w \big( (1 - \gamma_t) s_{\theta}(x_t, \tilde{c}_T) + \gamma_t s_{\theta}(x_t, \tilde{c}_A) - s_{\theta}(x_t) \big)$$

   其中 $w$ 为 CFG 尺度，$\gamma_t$ 为步骤 4 计算的自适应系数。该公式将标准 CFG 中的条件分数替换为目标与锚点分数的动态加权混合。

6. **去噪采样**：使用 DDIM 等标准采样器，从 $x_T$ 出发迭代应用混合引导分数，逐步去噪至 $x_0$。

### 与基线方法的关键差异

相较于现有方法，AAPB 在三个关键维度上实现了改进：

- **混合系数调整方式**：基线方法依赖手动设定的固定系数或启发式调度（如 R2F 的交替步骤），AAPB 则基于 Tweedie 对齐推导出闭式自适应系数 $\gamma_t^*$，每一步根据当前分数状态动态计算最优值。

- **引导公式**：标准 CFG 的条件分数固定为目标提示分数，AAPB 将其扩展为三路分数的动态加权混合，使去噪轨迹能够自适应地平衡目标忠实度与锚点稳定性。

- **提示处理**：R2F 将罕见概念分解为多步子提示并交替生成，容易导致实体纠缠；AAPB 直接构建罕见概念与其频繁对应物的二元对，一次性重构完整提示，避免属性-物体绑定错误（见图 11）。

### 补充图表

![[assets/figures/papers/paper_list_l2293_https_arxiv_org_abs_2603_19158/figures/001_Figure_1.jpg]]
*Figure 1: When the target concept lies in a low-density region, the generated samples tend to drift toward semantically dominant, high-density concepts [33] in the learned score space, resulting in the suppression of rare or compositional attributes. Our proposed adaptive coefficient*



### 问题形式化：从去噪漂移到分数空间对齐

扩散模型在低密度区域生成时，去噪过程会偏向训练分布中的高频语义模式，导致罕见属性被压制。AAPB的核心洞察在于：**通过最小化混合去噪器与目标去噪器之间的后验均值距离，可以等价地转化为分数空间误差最小化**，从而推导出闭式自适应系数。

关键桥梁是Tweedie等式，它建立了噪声观测下后验均值与分数函数的关系：

$$\mathbb{E}[x_0 \mid x_t] = x_t + (1 - \alpha_t) \nabla_{x_t} \log p(x_t) \quad \text{(Eq. 4)}$$

基于此，优化图像空间的目标忠实性等价于优化分数空间的对齐程度。

### 核心模块一：扩展分类器自由引导（Blended CFG）

标准CFG将条件分数与无条件分数线性组合。AAPB将条件分数重新定义为**目标提示分数与锚点提示分数的动态加权混合**，形成三路引导：

$$\tilde{s}_{\theta}(x_t; w, \gamma_t) = s_{\theta}(x_t) + w \big( (1 - \gamma_t) s_{\theta}(x_t, \tilde{c}_T) + \gamma_t s_{\theta}(x_t, \tilde{c}_A) - s_{\theta}(x_t) \big) \quad \text{(Eq. 8)}$$

其中：
- $s_{\theta}(x_t)$：无条件分数估计
- $s_{\theta}(x_t, \tilde{c}_T)$：目标提示的条件分数
- $s_{\theta}(x_t, \tilde{c}_A)$：辅助锚点提示的条件分数
- $w$：标准CFG引导尺度
- $\gamma_t$：锚点混合系数，控制锚点相对于目标的贡献比例

### 核心模块二：分数空间对齐损失

为确定最优的$\gamma_t$，定义混合分数与纯目标分数之间的平方误差：

$$\mathcal{L}(\gamma_t) = \|\tilde{s}_{\theta}(x_t; w, \gamma_t) - s_{\theta}(x_t, \tilde{c}_T)\|_2^2 \quad \text{(Eq. 12)}$$

该损失直接衡量当前混合策略偏离目标生成方向的程度。

### 核心模块三：闭式自适应系数推导

将Eq. (8)代入Eq. (12)，对$\gamma_t$求导并令导数为零，得到**每一步动态计算的最优系数**：

$$\gamma_t^*(x_t) = \frac{1 - w}{w} \cdot \frac{\langle s_{\theta}(x_t, \tilde{c}_T) - s_{\theta}(x_t), s_{\theta}(x_t, \tilde{c}_A) - s_{\theta}(x_t, \tilde{c}_T) \rangle}{\| s_{\theta}(x_t, \tilde{c}_A) - s_{\theta}(x_t, \tilde{c}_T) \|_2^2} \quad \text{(Eq. 13)}$$

**变量含义解析**：
- 分子中的内积项衡量**无条件偏离方向**与**锚点-目标差异方向**的一致性：当锚点分数恰好指向目标分数无法覆盖的区域时，内积增大，系数相应增大，锚点获得更高权重。
- 分母是锚点与目标分数差异的范数平方，起到归一化作用，防止锚点偏离过大时过度主导生成。
- 系数$\frac{1-w}{w}$反映了CFG强度对混合策略的约束：$w$越大，目标条件本身已足够强，锚点权重自动降低。

### 核心模块四：锚点质量度量

为评估锚点提示的有效性，定义位移度量，将锚点分数分解为相对于目标分数的平行分量和正交分量：

$$\mathrm{Displacement}(s_A) = \|\mathbf{d}^{\parallel}\| + \|\mathbf{d}^{\perp}\| \quad \text{(Eq. 43)}$$

- **平行分量**提供沿目标方向的引导增益
- **正交分量**引入偏离目标的稀释效应

消融实验（Table 3, Table 5）证实：GPT-4o生成的锚点达到最佳T2I对齐（87.9），且位移度量与T2I分数呈负相关，验证了该度量的锚点筛选能力。

### 核心模块五：提示重构与去噪采样

AAPB的完整管线包含两个预处理步骤和迭代采样：

1. **提示重构**：将罕见概念与其频繁对应物构建二元对，一次性重构完整提示，避免R2F中多步子提示导致的实体纠缠（Figure 11）
2. **自适应系数计算**：每步根据Eq. (13)动态计算$\gamma_t^*$
3. **混合分数合成**：按Eq. (8)融合三路分数
4. **去噪采样**：使用DDIM等标准采样器从$x_T$迭代去噪至$x_0$

![[assets/figures/papers/paper_list_l2293_https_arxiv_org_abs_2603_19158/figures/017_Figure_11.jpg]]
*Figure 11: Comparison of prompt reconstruction between R2F and our method. R2F often collapses multiple rare concepts into a single entity, leading to entangled generations. In contrast, our method explicitly preserves each rare concept by directly pairing it with its frequent counterpart, resulting in disentangled and faithful generations*

该管线无需训练，可直接集成至任意预训练扩散模型（SDXL、SD3.0、IterComp等），在Table 4中展示了跨骨干的一致鲁棒性。

### 补充图表

![[assets/figures/papers/paper_list_l2293_https_arxiv_org_abs_2603_19158/figures/010_Figure_9.jpg]]
*Figure 9: Evolution of the adaptive coefficient*

![[assets/figures/papers/paper_list_l2293_https_arxiv_org_abs_2603_19158/figures/013_Figure_10.jpg]]
*Figure 10: Evolution of the adaptive coefficient*



## 实验与关键发现

### 核心瓶颈与实验动机

扩散模型在生成罕见概念时，其去噪过程会向训练分布中的高频语义模式漂移，导致罕见属性被压制、组合性丢失以及结构不一致。这一现象在**RareBench**（涵盖Property、Shape、Texture、Action、Complex五类单对象罕见概念及多对象组合）和**FlowEdit**图像编辑任务中均有体现。AAPB通过在每个扩散步骤动态计算闭式自适应系数 $\gamma_t^*$，最小化混合分数与目标分数之间的对齐损失，从而修正这一漂移。以下实验围绕三个核心问题展开：(1) 自适应机制是否优于固定系数和启发式调度？(2) 锚点质量如何影响生成效果？(3) 方法在不同骨干模型和任务上的泛化性如何？

### 主结果：罕见概念生成与图像编辑

**RareBench罕见概念生成**（Table 1）：基于SD3.0的AAPB在GPT-4o T2I对齐平均分上达到**84.1**，比最强基线R2F（75.7）高出**8.4个点**，在所有单对象类别中均取得最佳或次佳。具体而言，Property类别达到96.9，Shape 89.4，Texture 87.5，Action 85.6，Complex 80.0。定性对比（Figure 3）显示，AAPB生成的罕见概念图像在属性绑定和结构一致性上显著优于SD3.0、R2F、SynGen、ELLA等基线。

**FlowEdit图像编辑**（Table 2）：AAPB在结构保持指标上全面领先——CLIP-I达到**0.905**（FlowEdit为0.872）、DINO **0.814**（FlowEdit为0.719）、LPIPS低至**0.155**（FlowEdit为0.181）、DreamSim **0.155**（FlowEdit为0.180），同时维持相当的文本对齐（CLIP-T 0.278 vs 0.277）。定性结果（Figure 4）表明，AAPB在应用编辑指令时更好地保留了源图像的结构信息。

**跨骨干泛化性**（Table 4）：将AAPB集成至SDXL、SD3.0和IterComp三种预训练骨干，在RareBench上均取得一致的T2I对齐提升，验证了方法的模型无关性。

### 自适应系数的消融验证

**固定系数 vs 自适应系数**（Figure 5）：在RareBench上，固定 $\gamma_t$ 从0.0到1.0的T2I对齐曲线呈凸型，最优值落在0.3-0.5区间，但自适应系数 $\gamma_t^*$ 在所有固定值上均取得更高T2I对齐。Figure 2(d)的玩具实验进一步显示，自适应方法的2-Wasserstein距离低于任何固定插值的最优点，验证了逐步自适应的必要性。

**系数演化模式**：罕见概念生成中，$\gamma_t^*$ 在整个去噪过程中保持稳定值（Figure 10），反映对锚点稳定化的持续需求；图像编辑中，$\gamma_t^*$ 在后期步骤出现明显饱和（Figure 9），此时源图像的结构引导占据主导。

**CFG尺度影响**（Figure 8, Figure 15）：在FlowEdit上，CFG尺度 $w$ 调节结构保持与文本对齐的权衡；在RareBench上，$w$ 的消融表明方法对引导强度具有鲁棒性。

### 锚点质量与提示重构

**锚点策略消融**（Table 3）：使用GPT-4o生成的锚点达到最佳T2I（87.9），但即使使用简单规则生成的锚点，AAPB仍一致优于R2F，表明自适应机制对锚点质量具有一定容忍度。

**锚点质量度量**（Table 5）：提出的位移度量 $\mathrm{Displacement}(s_A) = \|\mathbf{d}^{\parallel}\| + \|\mathbf{d}^{\perp}\|$（Eq. 43）与T2I呈负相关——位移越小，锚点越接近目标，生成质量越高。平行分量提供有效引导，正交分量则稀释目标语义。

**提示重构对比**（Figure 11）：R2F的交替调度容易将多个罕见概念纠缠为单一实体，而AAPB通过直接构建罕见概念与其频繁对应物的二元对，一次性重构完整提示，有效避免实体纠缠。

### 集成能力与失败模式

**与R2F+的集成**（Table 6）：将AAPB无缝集成至R2F+区域控制管线后，在RareBench-Multi上一致性提升**9.4~19.9个点**，证明自适应混合机制可与现有提示调度方法协同工作。

**计算开销**（Table 7）：AAPB需要每步评估三路分数（无条件、目标条件、锚点条件），罕见概念生成约需38秒（基线26秒），内存略高，但仍在可接受范围。

**失败案例**（Figure 13）：在RareBench的部分样本上，AAPB与R2F均出现属性-对象错配。这与CLIP文本编码器在组合性绑定上的已知局限一致——当目标涉及多属性、多物体组合时，编码器难以维持正确的属性-物体对应关系。

### 用户研究与人类偏好

**用户研究**（Table 8, Table 9）：参与者在不知模型身份的情况下，根据语义准确性和视觉一致性对生成图像进行评分。AAPB在多数提示上获得更高偏好。

**自动化偏好评估**（Table 10）：在LAION-aesthetic（视觉吸引力）、ImageReward（人类偏好）和PickScore（文本-图像对齐）三项指标上，AAPB均取得最佳或次佳，与GPT-4o评估和用户研究结论一致。

### 补充图表

![[assets/figures/papers/paper_list_l2293_https_arxiv_org_abs_2603_19158/figures/003_Table_1.jpg]]
*Table 1: Text-to-image alignment performances in the RareBench with other baselines with GPT-4o based evaluation. Best values are denoted with bold, second-best with underlined*

![[assets/figures/papers/paper_list_l2293_https_arxiv_org_abs_2603_19158/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison with state-of-the-art diffusion models on RareBench. All models are executed with the same random seed. Our method achieves stronger text-to-image alignment without additional training*

![[assets/figures/papers/paper_list_l2293_https_arxiv_org_abs_2603_19158/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison of image editing results using FlowEdit [15] and our method. All edits are performed with the same random seed. Compared to FlowEdit, our approach better preserves source content while faithfully applying the instructed edits*

![[assets/figures/papers/paper_list_l2293_https_arxiv_org_abs_2603_19158/figures/007_Figure_5.jpg]]
*Figure 5: Comparison between fixed*

![[assets/figures/papers/paper_list_l2293_https_arxiv_org_abs_2603_19158/figures/014_Table_5.jpg]]
*Table 5: Anchor quality comparison across different anchor generation strategies. Lower displacement indicates anchors closer to the target with fewer artifacts. T2I scores are evaluated using GPT-4o. All correlations are negative*

![[assets/figures/papers/paper_list_l2293_https_arxiv_org_abs_2603_19158/figures/015_Table_6.jpg]]
*Table 6: Quantitative comparison on RareBench-Multi between R2F+ and our method built upon the R2F+ baseline*

![[assets/figures/papers/paper_list_l2293_https_arxiv_org_abs_2603_19158/figures/021_Figure_13.jpg]]
*Figure 13: Failure results on RareBench where both ours and R2F exhibit attribute-object mismatches. This behaviors aligns with previously reported limitations in CLIP’s ability to bind compositional concpets faithfully [16]*

![[assets/figures/papers/paper_list_l2293_https_arxiv_org_abs_2603_19158/figures/002_Figure_2.jpg]]
*Figure 2: Toy Example of the target concept generation. (a) Training distributions: frequent samples*



## 定位与知识库关联

### 1. 问题定位：扩散模型在低密度区域的行为偏差

扩散模型的核心能力在于学习数据分布的高维分数场（score field），并通过逐步去噪将随机噪声映射至样本空间。然而，当目标概念（如“穿盔甲的刺猬”或“玻璃制成的自行车”）位于训练分布的长尾、低密度区域时，模型习得的分数场会呈现出显著的**语义漂移**（semantic drift）现象：去噪轨迹倾向于偏离目标分布，收敛至语义上占主导地位的高频模式（如“普通刺猬”或“金属自行车”），导致罕见属性被压制、组合性丢失以及结构不一致。这一瓶颈在**R2F**（Rare-to-Frequent, 2024）等工作中已被初步识别，其解决方案是通过LLM将罕见概念分解为多步子提示并交替调度，但该方法依赖于启发式的步骤分配策略，缺乏对去噪动力学的精细控制。

AAPB的切入点是：将这一漂移问题形式化为**分数空间中的最优插值问题**——在每个扩散步骤中，通过自适应系数动态调节辅助锚点提示（频繁概念或源提示）与目标提示的贡献比例，从而修正分数空间中的漂移，使去噪轨迹始终指向目标分布。

### 2. 方法坐标系：训练免引导方法的演进脉络

AAPB在方法谱系中处于**训练免引导（training-free guidance）**与**提示工程（prompt engineering）**的交汇点。其直接对话的基线包括：

- **R2F**（2024）：首次系统性地处理罕见概念生成，通过LLM将罕见概念映射为频繁对应物，并在去噪步骤间交替调度目标提示与锚点提示。AAPB继承了其“罕见-频繁二元对”的提示构建策略，但将交替调度替换为**逐步自适应混合**，从而在RareBench上实现了+8.4个点的GPT-4o T2I对齐分数提升（Table 1）。

- **FlowEdit**（2024）：基于无逆ODE的结构保持图像编辑方法，通过源提示与目标提示的插值实现编辑。AAPB将其编辑范式统一到同一自适应混合框架下，在结构保持指标上全面超越（CLIP-I: 0.905 vs 0.872; DINO: 0.814 vs 0.719; LPIPS: 0.155 vs 0.181），同时维持了相当的文本对齐水平（Table 2）。

- **SD3.0 / SDXL / IterComp**：作为预训练骨干，AAPB在这些模型上均表现出一致的增益（Table 4），验证了方法的模型无关性（model-agnostic）。

- **SynGen**（语言绑定方法）、**ELLA**（LLM引导扩散）、**iRFDS**（流蒸馏编辑）：作为辅助基线出现在RareBench和FlowEdit的比较中，AAPB在语义准确性和结构保真度上均取得最优或次优结果。

从更广的谱系看，AAPB可视为**Classifier-Free Guidance（CFG）**的自然扩展：标准CFG的引导公式为
$$\tilde{s}_{\theta}^{\mathrm{CFG}}(x_t, c; w) = w s_{\theta}(x_t, c) + (1-w) s_{\theta}(x_t)$$
而AAPB将其中的条件分数 $s_{\theta}(x_t, c)$ 重新定义为目标分数与锚点分数的动态加权混合：
$$s_{\theta}(x_t, c) = (1-\gamma_t) s_{\theta}(x_t, \tilde{c}_T) + \gamma_t s_{\theta}(x_t, \tilde{c}_A)$$
这一形式上的简洁扩展，使得AAPB能够无缝集成至任何基于CFG的扩散管线中，包括R2F+的区域控制管线（Table 6，在RareBench-Multi上一致性提升9.4~19.9个点）。

### 3. 核心机制：Tweedie对齐与闭式自适应系数

AAPB的理论基础建立在**Tweedie等式**之上——在高斯噪声假设下，后验均值 $\mathbb{E}[x_0 \mid x_t]$ 可通过分数函数解析表达：
$$\mathbb{E}[x_0 \mid x_t] = x_t + (1-\alpha_t) \nabla_{x_t} \log p(x_t)$$
这一等式建立了分数空间与图像空间之间的桥梁：**最小化混合去噪器与目标去噪器之间的后验均值距离，等价于最小化分数空间误差**。

基于此，AAPB定义了分数空间对齐损失：
$$\mathcal{L}(\gamma_t) = \|\tilde{s}_{\theta}(x_t; w, \gamma_t) - s_{\theta}(x_t, \tilde{c}_T)\|_2^2$$
并推导出闭式最优系数：
$$\gamma_t^*(x_t) = \frac{1-w}{w} \cdot \frac{\langle s_{\theta}(x_t, \tilde{c}_T) - s_{\theta}(x_t), s_{\theta}(x_t, \tilde{c}_A) - s_{\theta}(x_t, \tilde{c}_T) \rangle}{\| s_{\theta}(x_t, \tilde{c}_A) - s_{\theta}(x_t, \tilde{c}_T) \|_2^2}$$

这一推导的关键在于：$\gamma_t^*$ 并非预设的超参数，而是**每一步根据当前状态 $x_t$ 和分数场动态计算**的。其分子项度量了目标分数与锚点分数之间的“方向一致性”——当锚点分数的修正方向与目标分数的需求方向一致时，$\gamma_t^*$ 增大；反之则减小。这一机制在数学上保证了每一步的局部最优性。

消融实验（Figure 5, Figure 2(d)）强有力地验证了自适应的必要性：在所有固定 $\gamma_t$ 值（0.0至1.0）上，自适应系数均取得更高的生成质量；且自适应方法的2-Wasserstein距离低于任何固定插值，验证了逐步自适应的不可替代性。

### 4. 锚点质量与提示重构策略

AAPB的性能高度依赖于锚点提示的质量。论文提出了**位移度量**（Displacement）来量化锚点的有效性：
$$\mathrm{Displacement}(s_A) = \|\mathbf{d}^{\parallel}\| + \|\mathbf{d}^{\perp}\|$$
其中 $\mathbf{d}^{\parallel}$ 为锚点分数相对于目标分数的平行分量（提供有效引导），$\mathbf{d}^{\perp}$ 为正交分量（引入稀释效应）。实验表明（Table 5），GPT-4o生成的锚点达到最佳T2I对齐（87.9），且位移度量与T2I呈负相关，验证了该度量的有效性。

在提示重构策略上，AAPB与R2F存在关键差异：R2F将多个罕见概念合并为单一实体（如“穿盔甲的刺猬”），容易导致概念纠缠；AAPB则直接为每个罕见概念构建其频繁对应物的二元对（如“刺猬”与“穿盔甲的刺猬”），并一次性重构完整提示，从而避免了实体纠缠（Figure 11）。

### 5. 适用边界与失效模式

**适用场景**：
- **罕见概念生成**：目标概念位于训练分布长尾区域，需要锚点稳定去噪轨迹。
- **图像编辑**：需要保持源图像结构的同时应用语义编辑，锚点为源提示。
- **多骨干兼容**：已验证在SD3.0、SDXL、IterComp上的一致增益（Table 4）。

**失效模式与局限**：
1. **CLIP文本编码器的组合性限制**：在多属性、多物体组合场景下，CLIP难以维持正确的属性-物体绑定，导致生成中出现纠缠或属性泄露（Figure 13）。这是文本编码器层面的根本限制，非AAPB的引导机制所能克服。
2. **计算开销**：AAPB需要每步评估三路分数（无条件、目标条件、锚点条件），相比基线模型稍慢（罕见概念生成38秒 vs 26秒），内存占用略高（Table 7）。尽管在可接受范围内，但对于实时应用场景仍需优化。
3. **锚点依赖**：当前方法依赖于LLM生成锚点，锚点质量直接影响性能。对于LLM难以处理的细粒度或领域特定概念，可能需要人工设计锚点。

### 6. 开放问题与未来方向

1. **文本编码器的组合性瓶颈**：如何克服CLIP等文本编码器在组合性理解上的根本限制，以实现更鲁棒的属性-物体绑定？可能的路径包括引入LLM的推理能力进行提示分解与重组，或使用更强的视觉-语言对齐模型。
2. **训练场景的推广**：当前AAPB是纯粹的训练免方法。能否将自适应混合机制推广到有训练的场景，例如与LoRA微调或DreamBooth结合，在保持目标忠实度的同时进一步提升生成质量？
3. **锚点自动生成策略**：当前依赖LLM生成锚点，是否存在更高效的锚点自动生成策略？例如基于检索的锚点选择、或利用扩散模型自身的知识进行锚点合成。
4. **多概念场景的扩展**：当前框架主要处理单一罕见概念或单一编辑任务。如何将自适应混合机制扩展到多个罕见概念同时出现的场景，或需要多重编辑的复杂任务？



## 原文 PDF

![[paperPDFs/CVPR_2026/Adaptive_Auxiliary_Prompt_Blending_for_Target_Faithful_Diffusion_Generation.pdf]]
