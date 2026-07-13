---
title: Applying Guidance in a Limited Interval Improves Sample and Distribution Quality in Diffusion Models
type: paper
paper_level: A
venue: NEURIPS
year: 2024
pdf_ref: paperPDFs/NeurIPS_2024/Applying_Guidance_in_a_Limited_Interval_Improves_Sample_and_Distribution_Quality_in_Diffusion_Models.pdf
project_link: null
code_link: https://github.com/kynkaat/guidance-interval
aliases:
- GI
- AGLIISDQDM
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将引导权重限制在采样链的中间连续区间内（通过设定上界 σ_hi 和下界 σ_lo），在高噪声和低噪声区域关闭引导。
primary_logic: 引导的正向作用主要集中在中等噪声水平，可锐化图像细节；而在高噪声阶段会破坏整体布局与多样性，低噪声阶段则几乎无益。仅在中段施加引导可同时提升生成质量和推理速度。
claims:
- 在 ImageNet-512 上，限制引导区间将 EDM2-XXL 的 FID 从 1.81 显著降低至 1.40，FDDINOv2 从 33.09 降至 29.16。
- 1D 玩具实验表明，仅在高 σ 禁用引导即可恢复条件分布的两个模式，而全域引导导致严重的模式丢失。
- 与标准 CFG 相比，限制引导区间在 DINOv2 特征空间中显著提升召回率 (Recall) 而不损害精确率 (Precision)。
- 在 SD-XL 上，限制引导区间在保持图像细节的同时避免了传统 CFG 中常见的过度饱和与构图简化，并带来超过 20% 的推理加速。
---

# Applying Guidance in a Limited Interval Improves Sample and Distribution Quality in Diffusion Models

> [!tip] 核心洞察
> 引导的正向作用主要集中在中等噪声水平，可锐化图像细节；而在高噪声阶段会破坏整体布局与多样性，低噪声阶段则几乎无益。仅在中段施加引导可同时提升生成质量和推理速度。

| 字段 | 内容 |
|------|------|
| 中文题名 | 限定引导区间改善扩散模型样本与分布质量 |
| 英文题名 | Applying Guidance in a Limited Interval Improves Sample and Distribution Quality in Diffusion Models |
| 会议/期刊 | NEURIPS 2024 |
| Links | [paper](https://openreview.net/forum?id=nAIhvNy15T) · [Code](https://github.com/kynkaat/guidance-interval) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Guidance Interval |
| Dataset | ImageNet-512 |

> [!tip] 效果简介
> - ImageNet-512 (EDM2-S) 上，FID 1.68 vs 2.23 (-0.55)；FDDINOv2 46.25 vs 52.32 (-6.07)。
> - ImageNet-512 (EDM2-XXL) 上，FID 1.40 vs 1.81 (-0.41)；FDDINOv2 29.16 vs 33.09 (-3.93)。
> - ImageNet-512 (DiT-XL/2) 上，FID 2.40 vs 3.04 (-0.64)。

## 概要

扩散模型在图像生成中广泛采用**无分类器引导（Classifier-Free Guidance, CFG）**来提升样本的保真度与条件对齐性，但传统做法是在整个采样链上施加恒定的引导权重。本文揭示这一策略存在根本性缺陷：**在高噪声水平（大 σ）阶段，引导会严重截断分布、导致模式丢失；在低噪声水平（小 σ）阶段，引导的正面作用微弱，却增加了不必要的计算开销**。

核心洞察在于，引导的正向效应集中在采样链的中间噪声区间——此时引导可以锐化图像细节，而不会破坏整体布局与多样性。基于此，作者提出一种极简而高效的改进方案：**将引导权重限制在采样链的中间连续区间内**（通过设定上界 σ_hi 和下界 σ_lo），在区间外完全关闭引导（即权重置为 1）。该方法仅需在采样 ODE 中将恒定引导权重替换为分段常数函数，不改变模型结构、无需重新训练。

实验表明，限制引导区间带来了显著的分布质量与推理效率双重提升。在 ImageNet-512 上，EDM2-XXL 的 FID 从 1.81 降至 **1.40**，FDDINOv2 从 33.09 降至 **29.16**；在 DiT-XL/2 上同样取得一致改善。定性分析进一步证实，该方法在 SD-XL 等文本到图像模型中能有效避免传统 CFG 常见的过度饱和与构图简化问题，同时带来超过 20% 的推理加速。引导区间的超参数对采样步数变化表现出良好的鲁棒性，且可通过顺序搜索高效确定。

扩散模型通过逐步去噪将高斯噪声转化为数据样本，其采样过程可描述为一个关于噪声水平 $\sigma$ 的常微分方程（ODE）：

$$
\mathrm{d}\mathbf{x}/\mathrm{d}\sigma = -\big(D_{\theta}(\mathbf{x};\sigma) - \mathbf{x}\big)/\sigma
$$

其中 $D_{\theta}$ 为训练得到的去噪器。对于条件生成任务，**Classifier-free guidance (CFG)**（Ho & Salimans, NeurIPS 2021）通过将条件与无条件去噪器的预测进行线性组合来构造引导版 ODE，从而增强生成样本对条件的符合度。其核心操作是在整个采样链上以恒定权重 $w$ 施加引导，引导后的 ODE 可写为条件与无条件 ODE 的加权组合。

然而，这种全域恒定引导策略存在严重的隐性问题。**核心瓶颈在于**：引导的正向效果并非均匀分布于所有噪声水平。在高噪声阶段（$\sigma$ 较大），样本尚未形成有意义的结构，此时施加引导会迫使采样轨迹偏离数据分布的高概率区域，导致分布截断与模式丢失——生成结果虽然更“符合条件”，却丧失了多样性。在低噪声阶段（$\sigma$ 极小），图像结构已基本定型，引导的作用微乎其微，却仍需额外计算条件去噪器的前向传播，造成不必要的计算开销。

这一现象可通过 1D 合成实验直观验证（见 Figure 2）：当条件分布具有双峰结构时，全域引导（$w=6$）导致采样轨迹在早期被推离分布支撑区域，最终仅恢复单一模式，发生灾难性模式丢失。而仅在高噪声区域关闭引导，即可完整恢复两个模式。相反，在低噪声区域关闭引导则几乎不影响生成质量，却可节省计算。

上述观察揭示了 CFG 的根本矛盾：**引导的有效性与危害性随噪声水平呈现非对称分布**——中等噪声水平是引导发挥正面作用（锐化细节、增强条件一致性）的关键区间，而高噪声和低噪声区域分别是引导产生破坏和浪费计算的主要来源。这一矛盾在传统 CFG 框架下无法调和，因为恒定权重策略将引导强制施加于所有噪声水平，牺牲了分布质量与推理效率。

**本文动机**正是基于这一洞察：通过将引导限制在采样链中间的连续区间内，在保持引导正面效果的同时消除其负面影响。该方法无需修改模型架构或训练流程，仅需在采样时引入两个额外的区间端点超参数 $(\sigma_{\mathrm{lo}}, \sigma_{\mathrm{hi}})$，即可同时提升生成质量与推理速度。

## 核心方法与创新机理

本文的核心创新在于对扩散模型中无分类器引导（classifier-free guidance, CFG）的施加方式进行了根本性的重新审视，提出了一种简单而高效的**引导区间（Guidance Interval）**策略。其关键洞察是：引导的正向作用并非均匀分布于整个采样链，而是主要集中在中等噪声水平区间；在高噪声阶段施加引导会破坏样本的整体布局与多样性，而在低噪声阶段施加引导则收效甚微且增加不必要的计算开销。

基于这一洞察，方法的核心改变体现在以下两个关键槽位（changed slots）上：

### 引导权重函数 $w(\sigma)$：从恒定标量到分段常函数

在标准 CFG（Ho & Salimans, NeurIPS 2021）中，引导权重 $w$ 在整个采样过程中保持恒定。本文将其替换为一个依赖于噪声水平 $\sigma$ 的分段常函数：

$$w(\sigma) = \begin{cases} w & \text{if } \sigma \in (\sigma_{\mathrm{lo}}, \sigma_{\mathrm{hi}}] \\ 1 & \text{otherwise} \end{cases}$$

这意味着引导仅在噪声水平处于区间 $(\sigma_{\mathrm{lo}}, \sigma_{\mathrm{hi}}]$ 内时被激活（使用指定的引导权重 $w$），而在高噪声区域（$\sigma > \sigma_{\mathrm{hi}}$）和低噪声区域（$\sigma \leq \sigma_{\mathrm{lo}}$）完全关闭引导（即 $w=1$，等价于无条件生成）。修改后的采样 ODE 为：

$$\mathrm{d}\mathbf{x}/\mathrm{d}\sigma = -\Big(w(\sigma) D_{\theta}(\mathbf{x}|\mathbf{c};\sigma) + (1 - w(\sigma)) D_{\theta}(\mathbf{x};\sigma) - \mathbf{x}\Big)/\sigma$$

### 引导调度超参数：从单一权重到三元组 $(w, \sigma_{\mathrm{lo}}, \sigma_{\mathrm{hi}})$

标准 CFG 仅需调节一个超参数 $w$，而引导区间方法引入了两个额外的区间端点 $\sigma_{\mathrm{lo}}$ 和 $\sigma_{\mathrm{hi}}$，构成三元组 $(w, \sigma_{\mathrm{lo}}, \sigma_{\mathrm{hi}})$。论文通过系统的消融实验表明：

- **上界 $\sigma_{\mathrm{hi}}$ 至关重要**：1D 合成实验（Figure 2）直观展示了在高 $\sigma$ 阶段施加引导会导致灾难性的模式丢失（mode drop），而仅在该阶段禁用引导即可恢复条件分布的全部模式。在 ImageNet-512 上，$\sigma_{\mathrm{hi}}$ 的选取对 FID 有显著影响（Figure 5 左）。
- **下界 $\sigma_{\mathrm{lo}}$ 的影响较小**：在大部分低噪声区域关闭引导对生成质量几乎无影响（Figure 5 右），但可显著减少无条件模型评估次数，带来超过 20% 的推理加速。
- **区间对采样步数具有鲁棒性**：当采样步数减半或加倍时，最优引导区间保持不变，表明该方法对采样调度具有良好的泛化能力。

### 设计选择的简洁性

值得注意的是，论文尝试了在引导区间内使用各种平滑权重函数来替代二元开关，但**这些测试并未改善结果**（Section 4.2）。这表明引导区间带来的收益源于“在何处施加引导”这一结构性的调度决策，而非权重函数的精细调节。这一简洁的设计选择使得方法易于实现和集成——仅需修改采样循环中的引导逻辑，无需重新训练模型或改变模型架构。

本文提出的方法在概念和实现上均极为简洁：**将无分类器引导（Classifier-Free Guidance, CFG）的作用范围从整个采样链缩减为一个连续的噪声水平区间**。该方法不修改模型结构、不重新训练网络、不引入新的损失函数，仅以即插即用的方式替换标准 CFG 的恒定引导权重。

### 核心流程

方法的完整采样 pipeline 由以下步骤构成：

1. **输入**：预训练的去噪模型 $D_\theta$（同时支持条件预测 $D_\theta(\mathbf{x}|\mathbf{c};\sigma)$ 和无条件预测 $D_\theta(\mathbf{x};\sigma)$）、条件信息 $\mathbf{c}$、总采样步数 $N$、噪声水平序列 $\{\sigma_t\}_{t=1}^N$。

2. **超参数设定**：指定三个标量超参数——引导权重 $w$、引导区间下界 $\sigma_{\mathrm{lo}}$、引导区间上界 $\sigma_{\mathrm{hi}}$。论文给出了各模型的最优区间参考值（如 EDM2-XXL 上 $\sigma \in (0.19, 1.61]$，SD-XL 上 $\sigma \in (0.28, 5.42]$），并指出 $\sigma_{\mathrm{lo}}$ 和 $\sigma_{\mathrm{hi}}$ 可分别独立搜索确定，无需进行二维网格搜索。

3. **采样循环（Guidance Interval Sampler）**：在每一步采样中，根据当前噪声水平 $\sigma_t$ 是否落入区间 $(\sigma_{\mathrm{lo}}, \sigma_{\mathrm{hi}}]$ 决定是否施加引导：
   - 若 $\sigma_t \in (\sigma_{\mathrm{lo}}, \sigma_{\mathrm{hi}}]$：同时计算条件和无条件去噪输出，按权重 $w$ 进行线性组合，即使用完整的 CFG 向量场。
   - 若 $\sigma_t$ 在区间外（高噪声区域 $\sigma > \sigma_{\mathrm{hi}}$ 或低噪声区域 $\sigma \leq \sigma_{\mathrm{lo}}$）：仅使用无条件去噪输出（等价于 $w=1$），跳过条件模型的前向传播。

   对应的引导区间 ODE 为：
   $$
   \frac{\mathrm{d}\mathbf{x}}{\mathrm{d}\sigma} = -\frac{w(\sigma) D_\theta(\mathbf{x}|\mathbf{c};\sigma) + \big(1 - w(\sigma)\big) D_\theta(\mathbf{x};\sigma) - \mathbf{x}}{\sigma}
   $$
   其中分段权重函数定义为：
   $$
   w(\sigma) = \begin{cases} w & \text{if } \sigma \in (\sigma_{\mathrm{lo}}, \sigma_{\mathrm{hi}}] \\ 1 & \text{otherwise} \end{cases}
   $$

4. **输出**：最终生成的样本 $\mathbf{x}(\sigma=0)$。

### 模块关系与设计逻辑

该方法仅涉及一个可插拔模块——**引导区间调度器**，其设计直接源于对引导作用机制的因果分析：

- **高噪声阶段（$\sigma > \sigma_{\mathrm{hi}}$）关闭引导**：1D 玩具实验（Figure 2）清晰表明，在高噪声阶段施加引导会将采样轨迹推向分布外区域，导致灾难性的模式丢失。关闭引导使采样轨迹保持在无条件分布的支持集内，从而保留整体布局与多样性。

- **低噪声阶段（$\sigma \leq \sigma_{\mathrm{lo}}$）关闭引导**：当噪声水平足够低时，引导对图像细节的增强效果微弱，此时关闭引导几乎不损害质量，但可显著减少计算开销（跳过无条件模型的前向传播）。

- **中间噪声阶段施加引导**：引导的正向作用——锐化细节、增强条件一致性——集中在这一区间。限制引导区间后，可使用比标准 CFG 更高的 $w$ 值而不会引发过度饱和或构图简化（Figure 6, Figure 9）。

### 与标准 CFG 的对比

| 组件 | 标准 CFG | 本文方法 |
|------|---------|---------|
| 引导权重函数 $w(\sigma)$ | 恒定标量 $w$，对所有 $\sigma$ 生效 | 分段常数：区间内为 $w$，区间外为 $1$ |
| 超参数 | 仅 $w$ | $w$、$\sigma_{\mathrm{lo}}$、$\sigma_{\mathrm{hi}}$ |
| 计算开销 | 每步均需条件+无条件两次前向 | 区间外仅需一次无条件前向，带来 >20% 推理加速 |
| 对高 $w$ 的容忍度 | 高 $w$ 导致模式丢失和过度饱和 | 可安全使用更高 $w$，且对权重选择更鲁棒（Figure 3） |

论文同时验证了在引导区间内使用平滑权重函数（如线性衰减）并不能进一步改善结果，因此最终方案保持了简单的二元开关设计。

### 背景：去噪扩散ODE

扩散模型的采样过程可描述为样本 $\mathbf{x}$ 随噪声水平 $\sigma$ 演化的常微分方程（ODE）：

$$
\mathrm{d}\mathbf{x}/\mathrm{d}\sigma = -\big(D_{\theta}(\mathbf{x};\sigma) - \mathbf{x}\big)/\sigma
$$

其中 $D_{\theta}(\mathbf{x};\sigma)$ 为去噪器，$\sigma$ 从高到低递减，对应从纯噪声逐步去噪至干净图像的过程。

标准无分类器引导（Classifier-Free Guidance, CFG）通过线性组合条件与无条件ODE来强化条件信号：

$$
\mathrm{d}\mathbf{x}/\mathrm{d}\sigma = -\Big(w D_{\theta}(\mathbf{x}|\mathbf{c};\sigma) + (1 - w) D_{\theta}(\mathbf{x};\sigma) - \mathbf{x}\Big)/\sigma
$$

其中 $w$ 为恒定的引导权重（$w > 1$ 时增强条件控制）。该公式在整个采样链上均匀施加引导。

### 核心改进：分段引导权重函数

本文的核心改动是将恒定的引导权重 $w$ 替换为**分段常数函数** $w(\sigma)$，仅在噪声水平的中间区间内启用引导，区间外关闭引导（即 $w = 1$，退化为无条件采样）：

$$
w(\sigma) = \begin{cases} w & \text{if } \sigma \in (\sigma_{\mathrm{lo}}, \sigma_{\mathrm{hi}}] \\ 1 & \text{otherwise} \end{cases}
$$

对应的修改后ODE为：

$$
\mathrm{d}\mathbf{x}/\mathrm{d}\sigma = -\Big(w(\sigma) D_{\theta}(\mathbf{x}|\mathbf{c};\sigma) + \big(1 - w(\sigma)\big) D_{\theta}(\mathbf{x};\sigma) - \mathbf{x}\Big)/\sigma
$$

### 变量含义与设计动机

| 符号 | 含义 | 作用 |
|------|------|------|
| $w$ | 引导权重 | 控制条件信号的强度，仅在区间内生效 |
| $\sigma_{\mathrm{hi}}$ | 引导区间上界 | 在高噪声阶段关闭引导，避免破坏整体布局与模式多样性 |
| $\sigma_{\mathrm{lo}}$ | 引导区间下界 | 在低噪声阶段关闭引导，减少不必要的计算开销 |
| $D_{\theta}(\mathbf{x}|\mathbf{c};\sigma)$ | 条件去噪器 | 基于类别或文本条件 $\mathbf{c}$ 预测去噪方向 |
| $D_{\theta}(\mathbf{x};\sigma)$ | 无条件去噪器 | 不依赖条件，仅基于噪声图像预测去噪方向 |

**设计动机**：1D合成实验（Figure 2）揭示，在高 $\sigma$ 阶段施加引导会导致采样轨迹偏离分布支撑集，造成灾难性的模式丢失（catastrophic mode drop）；而在低 $\sigma$ 阶段引导效果微弱。引导的正向作用集中在中等噪声水平，可有效锐化图像细节。因此，仅在 $(\sigma_{\mathrm{lo}}, \sigma_{\mathrm{hi}}]$ 区间内启用引导，可同时提升生成质量和推理速度。

### 超参数引入

相较于标准CFG仅需调节 $w$，本方法引入两个额外超参数 $\sigma_{\mathrm{lo}}$ 和 $\sigma_{\mathrm{hi}}$。论文提出二者可通过**顺序搜索**独立确定（先固定下界搜索上界，再固定上界搜索下界），无需进行二维网格搜索。实验表明，最优引导区间对采样步数的变化具有鲁棒性——步数减半或加倍时，最优区间保持不变。

### 消融：平滑权重函数

论文尝试在引导区间内使用各种平滑权重函数替代二元开关，但**未获得进一步改善**，表明简单的分段常数方案已足够有效。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_nAIhvNy15T/figures/002_Figure_2.jpg]]
*Figure 2: causing the unexpected detour in low-probability areas and a mode drop. See Figure 2 for details and comparison to our approach*

## 实验与关键发现

### 核心定量结果：ImageNet-512 类别条件生成

Table 1 汇总了在 ImageNet-512 上将标准 CFG 替换为所提引导区间方法后的 FID 与 FDDINOv2 指标变化。实验覆盖 EDM2-S、EDM2-XXL 和 DiT-XL/2 三种架构，所有对比使用相同的预训练模型和默认采样参数，仅修改引导应用区间。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_nAIhvNy15T/figures/004_Table_1.jpg]]
*Table 1: Quantitative results on ImageNet-512. Limiting the classifier-free guidance (CFG) to an interval improves both FID and*

**EDM2-XXL** 上，限制引导区间将 FID 从 1.81 降至 **1.40**，FDDINOv2 从 33.09 降至 **29.16**，这是该基准上的最优报告结果。**EDM2-S** 上 FID 从 2.23 降至 1.68，FDDINOv2 从 52.32 降至 46.25。**DiT-XL/2** 同样获得一致增益：FID 从 3.04 降至 2.40，FDDINOv2 从 51.97 降至 43.94。所有改进均不增加模型复杂度，且因在区间外关闭无条件模型评估，采样计算量略有下降。

### 引导权重敏感性分析

Figure 3 展示了 FID 和 FDDINOv2 随引导权重 $w$ 变化的曲线。标准 CFG（橙色/红色）对 $w$ 高度敏感：$w$ 偏离最优值时指标迅速恶化，且 FID 与 FDDINOv2 的最优 $w$ 不一致。限制引导区间后（蓝色/绿色），两条曲线变得平坦，允许使用更高的引导权重而不损害分布质量，且 FID 与 FDDINOv2 的最优 $w$ 趋于一致。这意味着引导区间方法降低了对权重选择的调参需求，同时释放了更大引导强度带来的细节锐化潜力。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_nAIhvNy15T/figures/005_Figure_3.jpg]]
*Figure 3: FID and*

### 分布覆盖：精确率-召回率分析

Figure 4 在 DINOv2 特征空间中绘制了精确率-召回率曲线。标准 CFG 在提高引导权重时精确率上升但召回率急剧下降，表明生成样本虽更“典型”却严重丢失了类内多样性。限制引导区间后，召回率曲线显著上移，在不牺牲精确率的前提下大幅提升了分布覆盖。最优 FDDINOv2 点（彩色三角）从标准 CFG 的低召回区域移动到高召回区域，直接验证了方法缓解模式丢失的因果机制——在高噪声阶段关闭引导避免了采样轨迹被推出分布外。

### 区间端点消融

Figure 5 分别扫描了上界 $\sigma_{\text{hi}}$ 和下界 $\sigma_{\text{lo}}$ 对 FID 的影响。上界 $\sigma_{\text{hi}}$ 存在明显的最优值：过低则引导不足，图像模糊；过高则重新引入高噪声阶段的破坏效应，FID 回升。下界 $\sigma_{\text{lo}}$ 对 FID 影响较弱，在较大范围内保持稳定，这意味着可以在大部分低噪声区域关闭引导以减少计算开销，同时不损害质量。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_nAIhvNy15T/figures/007_Figure_5.jpg]]
*Figure 5: Sensitivity of FID to the chosen guidance interval. Left: Sweep over*

此外，论文报告平滑权重函数（如高斯窗、余弦衰减）未能超越简单的二元开关，说明引导的正向作用天然集中在中间噪声带，而非权重连续过渡。

### 采样步数鲁棒性

将 EDM2-S 的采样步数减半（16 步）或加倍（64 步），最优引导区间 $(\sigma_{\text{lo}}, \sigma_{\text{hi}}]$ 保持不变。16 步下 FID 从 2.49 降至 1.84，64 步下从 2.27 降至 1.70，表明区间超参数对采样预算变化具有强鲁棒性，无需因步数调整而重新搜索。

### 文本条件生成：SD-XL 定性验证

在 SD-XL 上的定性实验揭示了限制引导区间的视觉效应。标准 CFG 在低 $w$ 时图像多样但模糊，提高 $w$ 虽增加清晰度却导致过度饱和与构图简化（Figure 6）。限制引导区间后，高 $w$ 可锐化细节、增强纹理定义感，同时保持色彩调性和整体构图不变（Figure 7 顶部）。Figure 8 的消融进一步显示：降低 $\sigma_{\text{hi}}$ 使图像趋于模糊、细节减少；提高 $\sigma_{\text{lo}}$ 则重新引入过度饱和与色彩偏移。此外，由于低噪声和部分高噪声区域关闭了无条件模型评估，该方法在 SD-XL 上带来超过 20% 的推理加速。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_nAIhvNy15T/figures/008_Figure_6.jpg]]
*Figure 6: Traditional CFG vs. our method. Left: Low w yields diverse but fuzzy images that lack detail. Middle: Increasing w adds crispness, but reduces diversity and oversaturates the colors. Right: Our method reduces these effects while retaining the crisp look*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_nAIhvNy15T/figures/011_Figure_8.jpg]]
*Figure 8: Effect of changing the guidance interval*

### 失败模式与局限

该方法引入了两个额外超参数 $\sigma_{\text{lo}}$ 和 $\sigma_{\text{hi}}$，尽管论文提出了顺序搜索策略（先定 $\sigma_{\text{hi}}$ 再定 $\sigma_{\text{lo}}$），但在新模型或新任务上仍需额外调参开销。验证范围目前限于类别条件生成（ImageNet）和文本条件生成（SD-XL），尚未在视频、音频等其他生成模态上进行充分评估。

## 定位与知识库关联

### 与基线方法的关系

本工作的核心基线是 **Classifier-Free Guidance (CFG)**（Ho & Salimans, NeurIPS 2021），其在整个采样链上施加恒定的引导权重 $w$。CFG 通过线性组合条件与无条件去噪 ODE 来增强样本的条件一致性，但存在一个被忽视的权衡：在高噪声水平（大 $\sigma$）时，引导会迫使采样轨迹偏离数据分布支撑集，导致严重的模式丢失和分布截断；在低噪声水平（小 $\sigma$）时，引导的边际收益趋近于零，却持续消耗计算资源。

本文提出的 **Guidance Interval** 方法并非引入新的引导机制，而是对 CFG 的**调度策略**进行最小化改造：将引导权重函数 $w(\sigma)$ 从全局常量修改为仅在中间噪声区间 $(\sigma_{\mathrm{lo}}, \sigma_{\mathrm{hi}}]$ 内生效的分段常数函数（Equation 6），区间外直接将 $w(\sigma)$ 置为 1（即关闭引导，退化为无条件采样）。这一改造仅涉及采样阶段的控制逻辑，**无需重新训练模型，不增加模型复杂度**，可直接应用于任何已支持 CFG 的预训练扩散模型。

从因果调控的角度看，本方法识别出的可操作因果旋钮是**引导生效的噪声水平区间**，而非引导权重本身的大小。这一发现与直觉相悖：传统上，研究者倾向于通过调整 $w$ 的全局大小来平衡多样性与质量，而本文揭示出 $w$ 的作用在采样链的不同阶段存在质变——在高噪声阶段有害，在中噪声阶段有益，在低噪声阶段冗余。因此，简单地“关掉有害和冗余的引导”比精细调节全局权重更有效。

### 方法适用边界

**已验证的适用范围：**
- **图像生成任务**：在 ImageNet-512 的类别条件生成（EDM2-S、EDM2-XXL、DiT-XL/2）和 Stable Diffusion XL 的文本条件生成上均取得一致且显著的改善。
- **采样器类型**：方法基于 ODE 采样框架推导，在确定性采样（如 Euler、Heun 等）上已验证有效。论文指出该方法同样适用于 SDE 采样器（如 stochastic DDIM），但未提供定量消融验证。
- **模型架构**：覆盖 EDM2（基于 U-Net 的像素空间扩散）和 DiT（基于 Transformer 的潜空间扩散）两类主流架构，显示出架构无关性。

**已知局限与未验证场景：**
- **额外超参数引入**：方法引入了 $\sigma_{\mathrm{lo}}$ 和 $\sigma_{\mathrm{hi}}$ 两个新区间端点超参数。虽然论文提出了顺序搜索策略（先固定 $\sigma_{\mathrm{lo}}$ 搜索 $\sigma_{\mathrm{hi}}$，再反向微调），且实验表明下界 $\sigma_{\mathrm{lo}}$ 对结果影响较小（Figure 5 右），但在实际部署中仍需额外的调参工作。这与 CFG 仅需调节单一 $w$ 的简洁性形成对比。
- **模态覆盖不足**：当前验证仅限于图像生成（类别条件和文本条件）。该方法在视频生成、音频生成、3D 生成等其他扩散模型应用模态上的有效性尚未得到评估。
- **极端采样步数**：虽然实验表明最优引导区间对步数减半或加倍具有鲁棒性（Section 4.2），但在极少步数（如 4-8 步）的蒸馏采样场景下的表现未经验证。

### 开放问题

1. **引导区间的自动化推导**：当前 $\sigma_{\mathrm{lo}}$ 和 $\sigma_{\mathrm{hi}}$ 依赖网格搜索确定。能否从 ODE 的动力学性质或训练得到的去噪器的非理想性中自动推导出最优引导区间，而不需要经验性搜索？论文在结论中明确将此列为开放问题。

2. **去噪器非理想性的角色**：论文在 1D 合成实验中揭示了“理想”条件下引导在高噪声阶段的破坏性机制，但作者指出，实际训练得到的去噪器存在非理想性（non-idealities），这些非理想性在引导区间的作用中扮演何种角色尚不清楚。这暗示最优引导区间可能与模型训练质量、数据集特性存在耦合。

3. **与“物种形成区间”的关联**：Biroli 等人在扩散模型中发现了一个“speciation interval”（物种形成区间），即在此噪声水平区间内，生成样本的类别身份被确定。本文的引导有效区间是否与该物种形成区间相重合？这一理论联系若被建立，将为引导区间的选择提供原则性依据。

4. **平滑权重函数的失效原因**：论文尝试在引导区间内使用各种平滑权重函数替代二元开关，但均未改善结果（Section 4.2）。这一反直觉现象背后的理论原因值得深入探究——它暗示引导的破坏性作用可能在区间边界处存在突变，而非渐进变化。

### 知识库定位

本工作属于**扩散模型采样策略优化**方向，具体定位于 **CFG 的调度改进**子领域。与以下研究方向形成互补或对比：

- **负向提示（Negative Prompting）**：通过将无条件模型替换为负向提示条件模型来增强引导效果。本方法与负向提示正交，可在其基础上叠加使用。
- **动态引导权重调度**：一些工作尝试让 $w$ 随采样步数变化（如线性衰减、余弦调度）。本文表明，在噪声水平坐标（$\sigma$）上而非时间步坐标上进行调度更为本质，且简单的分段常数函数已足够。
- **蒸馏与少步采样**：本方法通过关闭低噪声区域的引导减少了无条件模型评估次数，在 SD-XL 上带来超过 20% 的推理加速（Section 4.3），与蒸馏方法在加速目标上形成互补，但实现路径完全不同——本方法不改变模型权重，仅优化采样控制流。

## 原文 PDF

![[paperPDFs/NeurIPS_2024/Applying_Guidance_in_a_Limited_Interval_Improves_Sample_and_Distribution_Quality_in_Diffusion_Models.pdf]]
