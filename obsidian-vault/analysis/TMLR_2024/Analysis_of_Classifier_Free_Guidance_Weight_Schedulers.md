---
title: Analysis of Classifier-Free Guidance Weight Schedulers
type: paper
paper_level: A
venue: TMLR
year: 2024
pdf_ref: paperPDFs/TMLR_2024/Analysis_of_Classifier_Free_Guidance_Weight_Schedulers.pdf
project_link: null
code_link: null
aliases:
- DGWS
- ACFGWS
tags:
- TMLR_2024
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 去噪过程中各时间步的引导权重 ω(t) 的分配策略（调度器形状与强度）。
primary_logic: 将引导权重设计为单调递增函数可以推迟高强度引导，降低早期生成与引导之间的冲突，从而在保持总引导量不变的条件下，整体提升样本的保真度、文本一致性与多样性。
claims:
- 在CIFAR‑10上移除早期时间步的引导可提升FID，而移除后期引导则严重降低FID，说明早期强引导有害。
- 单调递增的启发式调度器（线性、余弦）在CIFAR‑10和ImageNet上显著改善了FID与IS的折衷。
- 在SD1.5上，线性调度器在推荐权重ω=7.5下带来FID下降2.71（17%），CLIP‑Score提升0.004（16%），且用户研究偏好率超过60%。
- CIN-256 LDM (ImageNet 256×256, 50K 图像) 上 FID = 2.791 (线性调度, DDIM 200步)
---

# Analysis of Classifier-Free Guidance Weight Schedulers

> [!tip] 核心洞察
> 将引导权重设计为单调递增函数可以推迟高强度引导，降低早期生成与引导之间的冲突，从而在保持总引导量不变的条件下，整体提升样本的保真度、文本一致性与多样性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 无分类器引导权重调度分析 |
| 英文题名 | Analysis of Classifier-Free Guidance Weight Schedulers |
| 会议/期刊 | TMLR 2024 |
| Links | [paper](https://openreview.net/forum?id=SUMtDJqicd) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | 动态无分类器引导权重调度（Dynamic Guidance Weight Scheduling, 含单调递增启发式及参数化调度器） |
| Dataset | CIN-256 LDM, SD1.5 |

> [!tip] 效果简介
> - CIN-256 LDM (ImageNet 256×256, 50K 图像) 上，FID 2.791 (线性调度, DDIM 200步) vs 3.467 (静态 CFG, DDIM 200步) (−0.676 (−19.5%))；IS 223.2 (线性调度, DDIM 200步) vs 176.8 (静态 CFG, DDIM 200步) (+46.4)。
> - SD1.5 (COCO 10K, 零样本) 上，FID 线性调度 (ω=7.5 等效) vs 静态 CFG (ω=7.5) (−2.71 (17% 相对改善))；CLIP-Score 线性调度 (ω=7.5 等效) vs 静态 CFG (ω=7.5) (+0.004 (16% 相对改善))。

## 概要

扩散模型中的**无分类器引导（Classifier-Free Guidance, CFG）**通过一个恒定的引导权重 ω 组合条件与无条件噪声预测，以提升生成样本的保真度。然而，静态 CFG 面临一个根本性的两难：低引导权重产生细节丰富但模糊的图像，高引导权重产生锐利但过度简化、多样性差的图像（Figure 1）。近期工作尝试在去噪过程中动态调整引导权重，但缺乏系统性分析与理论依据。

本文的核心发现是：**静态 CFG 在去噪早期引入过强的引导，导致“生成项”与“引导项”之间产生严重的方向冲突**（冲突比例约 50%，Figure 5），从而损害保真度与多样性。基于此洞察，作者提出将引导权重设计为**单调递增函数 ω(t)**，将高强度引导推迟到去噪后期，在保持总引导量不变的条件下，显著降低早期冲突。

方法上，本文探索了两类动态调度器：
- **启发式调度器**：线性递增与余弦递增，参数自由、即插即用；
- **参数化调度器**：clamp-linear 与 powered-cosine（pcs），通过引入下界或形状参数进一步优化引导曲线。

实验覆盖类条件生成（CIFAR-10、ImageNet 256×256）与文本到图像生成（Stable Diffusion 1.5、SDXL），核心结果如下：
- 在 **ImageNet 256×256** 上，线性调度器将 FID 从 3.467 降至 2.791（−19.5%），IS 从 176.8 提升至 223.2；
- 在 **SD1.5** 零样本 COCO 评测中，线性调度器在推荐权重 ω=7.5 下带来 FID 下降 2.71（17%）、CLIP-Score 提升 0.004（16%），用户偏好率超 60%；
- 启发式调度器的增益在不同采样步数（50/100/200）下保持稳定，且无需额外训练或推理开销。

**方法谱系与知识库定位**：本研究属于扩散模型推理时引导策略的改进。与 **静态 CFG**（Ho & Salimans, 2021）相比，仅将恒定权重替换为时间依赖的 ω(t)，不改变模型结构与训练流程。相较于其他动态引导变体（如 Rescale CFG、PAG 等），本文首次通过“冲突度量”与负扰动分析揭示了单调递增调度器有效性的因果机制，为引导权重调度提供了可解释的理论框架。



扩散模型已成为当代图像生成的核心范式，其通过逐步去噪将高斯噪声转化为高保真样本。为了提升生成质量与文本一致性，**无分类器引导（Classifier‑Free Guidance, CFG）**（Ho & Salimans, 2021）被广泛采用。其标准形式为：

$$\hat{\epsilon}_{\theta}(x_t, c) = \epsilon_{\theta}(x_t, c) + \omega \bigl( \epsilon_{\theta}(x_t, c) - \epsilon_{\theta}(x_t) \bigr)$$

其中 $\omega$ 是一个全局恒定的引导权重，控制条件预测与无条件预测之间的插值强度。增大 $\omega$ 可以提升图像的清晰度和文本对齐度，但过强的引导会牺牲样本多样性与细节丰富度，形成“细节丰富但模糊”与“锐利但简单”之间的固有折衷（Figure 1）。

### 现有方法缺口

尽管近期有工作尝试在去噪过程中动态调整引导权重并报告了性能提升，但这些尝试普遍缺乏系统性的分析与原理解释——**为什么动态调度有效、什么样的调度形状最优，仍是不明确的问题**。静态 CFG 在整个去噪过程中施加相同强度的引导，忽视了不同时间步对生成质量影响的异质性。

### 核心瓶颈与动机

本工作的核心发现是：**静态 CFG 在去噪早期引入过强的引导，导致“生成项”与“引导项”之间产生严重的方向冲突**。通过量化冲突度量：

$$\Phi(\epsilon_1, \epsilon_2) = \frac{-2 \lvert \epsilon_1 \rvert_2 \lvert \epsilon_2 \rvert_2}{\lvert \epsilon_1 \rvert_2^2 + \lvert \epsilon_2 \rvert_2^2}$$

作者在 SD1.5 上观察到，静态引导下约 50% 的时间步存在高冲突（Figure 5），而采用单调递增的引导调度可以显著降低冲突比例与冲突幅度。进一步的负扰动分析（Figure 6b）在 CIFAR‑10 上证实：移除早期时间步的引导可改善 FID，而移除后期引导则严重损害 FID，直接表明**早期强引导是有害的**。

基于此洞察，本文提出将恒定权重 $\omega$ 替换为时间依赖的调度函数 $\omega(t)$，形成**动态无分类器引导**：

$$\hat{\epsilon}_{\theta}(x_t, c) = \epsilon_{\theta}(x_t, c) + \omega(t) \bigl( \epsilon_{\theta}(x_t, c) - \epsilon_{\theta}(x_t) \bigr)$$

核心动机在于：**将引导权重设计为单调递增函数，推迟高强度引导至去噪后期，从而在保持总引导量不变的条件下，系统性地降低早期冲突，整体提升保真度、文本一致性与多样性**。这一方法无需额外训练或微调，仅在推理时替换 $\omega(t)$，计算开销与静态 CFG 完全相同。



## 核心方法与创新机理

本文的核心创新在于将无分类器引导（CFG）中全局恒定的引导权重 $\omega$ 替换为**时间依赖的单调递增调度函数 $\omega(t)$**，从而在保持总引导量不变的条件下，显著改善生成样本的保真度、文本一致性与多样性。

### 问题根因：静态 CFG 的早期冲突

标准 CFG 公式在去噪全过程施加恒定引导：

$$
\hat{\epsilon}_{\theta}(x_t, c) = \epsilon_{\theta}(x_t, c) + \omega \bigl( \epsilon_{\theta}(x_t, c) - \epsilon_{\theta}(x_t) \bigr)
$$

其中 $\epsilon_{\theta}(x_t, c)$ 为条件噪声估计（生成项），$\omega(\epsilon_{\theta}(x_t, c) - \epsilon_{\theta}(x_t))$ 为引导项。作者通过负扰动分析（CIFAR-10 上按 50 步间隔将引导置零）揭示了关键因果机制：**移除早期时间步的引导可降低 FID，而移除后期引导则严重损害 FID**（Figure 6b）。这表明静态 CFG 在去噪早期引入的强引导与生成项产生方向冲突，是制约保真度与多样性的核心瓶颈。

进一步地，作者定义了冲突度量：

$$
\Phi(\epsilon_1, \epsilon_2) = \frac{-2 \lvert \epsilon_1 \rvert_2 \lvert \epsilon_2 \rvert_2}{\lvert \epsilon_1 \rvert_2^2 + \lvert \epsilon_2 \rvert_2^2}
$$

其中 $-1$ 表示无冲突，$0$ 表示最大冲突。在 SD1.5 上的可视化（Figure 5）显示，静态 CFG 的冲突比例约 50% 且冲突幅度较大，而线性递增调度器可显著降低冲突。

### 核心方案：动态引导权重调度

基于上述发现，作者将恒定 $\omega$ 替换为时变函数 $\omega(t)$，形成动态 CFG：

$$
\hat{\epsilon}_{\theta}(x_t, c) = \epsilon_{\theta}(x_t, c) + \omega(t) \bigl( \epsilon_{\theta}(x_t, c) - \epsilon_{\theta}(x_t) \bigr)
$$

**关键设计原则**：$\omega(t)$ 应为单调递增函数，在去噪早期施加较低引导以降低冲突，后期逐步增强引导以提升细节与文本对齐。

为保证公平比较，所有调度器均满足面积归一化约束 $\int_0^T \omega(t) dt = \omega T$，使总引导量与静态基线完全相等，仅改变引导在时间轴上的分配策略。

### Changed Slots：从静态到动态的权重替换

| 模块 | 基线方案（Ho & Salimans, 2021） | 本文方案 | 证据 |
|------|-------------------------------|---------|------|
| CFG 引导权重 | 全局恒定 $\omega$ | 时间依赖 $\omega(t)$，按单调递增调度变化 | Equation 4, Section 4 |

本文探索了两类 $\omega(t)$ 实现：

1. **启发式调度器（参数无关）**：线性调度 $\omega(t) = 2(1 - t/T)\omega$、余弦调度等，均为单调递增函数，无需额外调参即可在各类任务中稳定提升性能。

2. **参数化调度器**：包括 clamp-linear（$\omega_t = \max(c, \omega_t)$，为引导设置下界 $c$）和 powered-cosine（pcs，$\omega_t = \frac{1 - \cos \pi ((T-t)/T)^s}{2} \omega$，通过参数 $s$ 控制曲线形状）。参数化方案可通过网格搜索进一步超越启发式调度器，但其最优参数依赖具体模型与数据集，无法跨设定泛化。

### 创新本质

该创新的本质在于**识别并利用去噪过程中不同时间步对引导强度的差异化需求**：早期去噪阶段主要构建全局结构，过强引导会与生成项冲突；后期阶段需要精细对齐条件信息。通过将引导权重从“均匀分配”重构为“前轻后重”的单调递增分配，在不引入额外计算开销的前提下，系统性突破了静态 CFG 的保真度-多样性折衷瓶颈。



本文提出的动态无分类器引导权重调度方法，在标准扩散模型采样流程中仅替换一个核心控制量——引导权重 ω，将其从全局恒定的标量扩展为随时间步变化的函数 ω(t)。整体框架由四个串行模块构成，输入为文本提示与初始噪声，输出为最终生成图像。

**1. 条件嵌入（文本编码器）**
给定文本提示，通过预训练的 CLIP 或 OpenCLIP 文本编码器将其映射为条件嵌入 c。该嵌入作为条件信号贯穿整个去噪过程，模块本身不参与调度器的任何修改。

**2. UNet 去噪网络**
在每一个去噪时间步 t，UNet 同时输出两个噪声估计：条件噪声估计 ε_θ(x_t, c) 和无条件噪声估计 ε_θ(x_t)。这是无分类器引导的基础——通过单网络在训练时随机丢弃条件，使同一网络具备双重预测能力（Ho & Salimans, 2021）。该模块在推理时与静态 CFG 完全一致，无需重新训练或微调。

**3. 动态 CFG 组合模块**
这是方法的核心创新点。将静态 CFG 公式：
$$\hat{\epsilon}_{\theta}(x_t, c) = \epsilon_{\theta}(x_t, c) + \omega \bigl( \epsilon_{\theta}(x_t, c) - \epsilon_{\theta}(x_t) \bigr)$$
中的恒定权重 ω 替换为时间依赖的 ω(t)，得到动态引导公式：
$$\hat{\epsilon}_{\theta}(x_t, c) = \epsilon_{\theta}(x_t, c) + \omega(t) \bigl( \epsilon_{\theta}(x_t, c) - \epsilon_{\theta}(x_t) \bigr)$$

ω(t) 的具体形式由调度器决定，论文探索了两类调度器：
- **启发式调度器**（无参数）：包括线性递增、余弦递增、反线性、正弦、V 形等六种形状。其中单调递增的线性与余弦调度器被证明始终优于静态基线，且所有调度器均经过面积归一化（∫₀ᵀ ω(t) dt = ωT），保证总引导量与静态基线相等，消除引导总量差异带来的性能偏差。
- **参数化调度器**（含可调参数）：如 clamp-linear（为引导权重设下界 c）和 powered-cosine（pcs，通过参数 s 控制曲线形状），能够超越启发式调度器，但最优参数依赖模型与任务，无法跨设定泛化。

**4. 采样器**
基于组合后的噪声估计 ε̂_θ(x_t, c)，使用标准采样器（如 DDIM 或 DPM-Solver++）迭代去噪，从纯噪声 x_T 逐步生成最终图像 x₀。

**核心因果机制**
静态 CFG 在去噪早期（高噪声阶段）施加与后期相同的强引导，导致生成项 ε_θ(x_t, c) 与引导项 (ε_θ(x_t, c) − ε_θ(x_t)) 之间产生显著的方向冲突（冲突度量 Φ 接近 0）。单调递增调度器将高强度引导推迟到去噪后期，使早期阶段以生成项为主导，降低冲突，从而在总引导量不变的条件下整体提升保真度、文本一致性与多样性。这一机制在 CIFAR-10 负扰动分析中得到直接验证：移除早期时间步的引导可改善 FID，而移除后期引导则严重损害 FID（Figure 6b）。

整个框架的计算开销与静态 CFG 完全相同——仅在推理时替换 ω(t) 的取值，不引入额外网络、不增加采样步数、无需训练。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_SUMtDJqicd/figures/001_Figure_1.jpg]]
*Figure 1: Classifier-Free Guidance introduces a trade-off between detailed but fuzzy images (low guidance, top) and sharp but simplistic images (high guidance, middle). Using a guidance scheduler (bottom) is simple yet very effective in improving this trade-off*



### 静态CFG与动态引导调度

标准无分类器引导（CFG）在去噪过程中使用恒定的引导权重 ω 组合条件与无条件噪声估计。其核心公式为：

$$
\hat{\epsilon}_{\theta}(x_t, c) = \epsilon_{\theta}(x_t, c) + \omega \bigl( \epsilon_{\theta}(x_t, c) - \epsilon_{\theta}(x_t) \bigr)
$$

其中，$\epsilon_{\theta}(x_t, c)$ 为条件噪声估计，$\epsilon_{\theta}(x_t)$ 为无条件噪声估计，$\omega$ 为全局恒定的引导权重。该公式构成所有后续方法的基线（Ho & Salimans, 2021）。

本文的核心改动是将恒定权重替换为时间依赖的函数 $\omega(t)$，形成动态引导调度：

$$
\hat{\epsilon}_{\theta}(x_t, c) = \epsilon_{\theta}(x_t, c) + \omega(t) \bigl( \epsilon_{\theta}(x_t, c) - \epsilon_{\theta}(x_t) \bigr)
$$

这一改动不涉及任何模型重训练或微调，仅在推理时修改权重分配策略，计算开销与静态CFG完全相同。

### 启发式调度器族

论文首先定义了六种参数无关的启发式调度器，所有调度器均经过面积归一化（$\int_0^T \omega(t) dt = \omega T$），确保总引导量与静态基线相等，消除引导总量差异对性能比较的干扰：

- **线性（linear）**：$\omega(t) = 2\bigl(1 - \frac{t}{T}\bigr) \omega$，单调递增
- **余弦（cosine）**：$\omega(t) = \cos(\pi t/T) + 1$，单调递增
- **反线性（invlinear）**：$\omega(t) = 2(t/T) \omega$，单调递减
- **正弦（sine）**：$\omega(t) = \sin(\pi t/T - \pi/2) + 1$，单调递减
- **V形（V-shape）**：先递减后递增
- **倒V形（invV-shape）**：先递增后递减

初步分析（Figure 6a）表明，仅有单调递增的调度器（线性、余弦）在CIFAR‑10上显著改善了FID与IS的折衷，后续工作仅聚焦于单调递增类调度器。

### 参数化调度器

为进一步探索调度器形状的优化空间，论文引入了两类参数化调度器：

**powered-cosine调度器（pcs）**，通过可调参数 $s$ 控制余弦函数的形状：

$$
w_t = \frac{1 - \cos \pi \bigl(\frac{T-t}{T}\bigr)^s}{2} w
$$

**clamp调度器**，为引导权重设置下界 $c$，防止早期引导过弱导致结构崩塌：

$$
w_t = \max(c, w_t)
$$

clamp操作可与线性或余弦等基础调度器组合使用（如clamp-linear），形成具有两个自由度的参数化族。

### 冲突度量

为量化生成项与引导项之间的方向冲突，论文定义了冲突度量 $\Phi$：

$$
\Phi(\epsilon_1, \epsilon_2) = \frac{-2 \lvert \epsilon_1 \rvert_2 \lvert \epsilon_2 \rvert_2}{\lvert \epsilon_1 \rvert_2^2 + \lvert \epsilon_2 \rvert_2^2}
$$

其中 $\epsilon_1 = \epsilon_{\theta}(x_t, c)$ 为生成项，$\epsilon_2 = \epsilon_{\theta}(x_t, c) - \epsilon_{\theta}(x_t)$ 为引导项。$\Phi = -1$ 表示两项方向完全一致（无冲突），$\Phi = 0$ 表示方向完全相反（最大冲突）。该度量用于分析不同调度策略下的冲突程度，为单调递增调度器的有效性提供了定量解释。

### 关键模块与流程

整体推理管线由以下模块构成：

1. **条件嵌入（文本编码器）**：通过CLIP/OpenCLIP将文字提示编码为条件嵌入 $c$，输入UNet。
2. **UNet去噪网络**：同时估计条件噪声 $\epsilon_{\theta}(x_t, c)$ 与无条件噪声 $\epsilon_{\theta}(x_t)$，后者通过在训练时随机丢弃条件信息实现。
3. **动态CFG组合模块**：依据公式 $\hat{\epsilon}_{\theta}(x_t, c) = \epsilon_{\theta}(x_t, c) + \omega(t)(\epsilon_{\theta}(x_t, c) - \epsilon_{\theta}(x_t))$，使用时间变化权重 $\omega(t)$ 组合条件与无条件噪声估计。这是本文唯一修改的模块。
4. **采样器**：基于DDIM或DPM‑Solver++迭代去噪生成最终图像。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_SUMtDJqicd/figures/005_Figure_5.jpg]]
*Figure 5: Visualization of Conflicted Terms from SD1.5 Rombach et al. (2022) shows that static guidance presents conflicts, while a guidance scheduler reduces the conflict between generation and guidance terms*



## 实验与关键发现

### 核心瓶颈与因果机制

静态无分类器引导（CFG）在扩散模型的整个去噪过程中使用恒定的引导权重 ω，这一设计在早期时间步引入过强的引导信号，导致生成项 ε_θ(x_t, c) 与引导项 (ε_θ(x_t, c) − ε_θ(x_t)) 之间产生严重的方向冲突。论文通过冲突度量 Φ(ε₁, ε₂) = −2|ε₁|₂|ε₂|₂ / (|ε₁|₂² + |ε₂|₂²) 量化了这一现象：当 Φ 接近 0 时表示最大冲突，接近 −1 时表示无冲突。实验表明，静态 CFG 在 SD1.5 上的冲突比率高达约 50%，且冲突幅度较大（Figure 5）。这种早期高强度引导迫使生成过程在尚未建立合理全局结构时就过度拟合条件信号，从而损害生成样本的保真度与多样性。

本文的核心因果调节旋钮是去噪过程中各时间步的引导权重分配策略 ω(t)。通过将恒定权重替换为单调递增函数，可以推迟高强度引导至去噪后期，在保持总引导量（即 ∫₀ᵀ ω(t) dt = ωT）不变的条件下，显著降低早期生成与引导之间的冲突。Figure 5 的可视化直接证实：采用线性递增调度器后，冲突比率和冲突幅度均大幅下降。

### 启发式调度器的初步验证（CIFAR‑10）

论文首先在 CIFAR‑10 DDPM 上对六种启发式调度器进行了系统筛选（Figure 6a）。所有调度器均经过面积归一化，确保与静态基线具有相同的总引导量。结果表明：

- **单调递增调度器（线性、余弦）** 在 FID 与 IS 的折衷上显著优于静态基线，形成更优的帕累托前沿。
- **单调递减调度器（invlinear、sine）** 和 **非单调调度器（V‑shape、Λ‑shape）** 表现显著劣于静态基线，进一步佐证了“早期强引导有害”的假说。

为直接验证这一假说，论文进行了负扰动分析（Figure 6b）：在保持其余时间步使用静态引导的前提下，将特定 50 步区间内的引导权重设为零。结果显示，移除早期时间步（t 接近 T）的引导可降低 FID，而移除后期引导则严重恶化 FID。这一证据强有力地表明：早期强引导是制约生成质量的关键瓶颈，而后期引导对维持样本结构不可或缺。

基于上述发现，论文在后续所有实验中仅保留单调递增的线性与余弦调度器。

### 类条件生成主要结果（ImageNet 256×256）

在 CIN‑256 LDM（基于 ImageNet 256×256 的潜在扩散模型）上，单调递增调度器展现出显著且一致的增益（Figure 7d，Table 2）。以 DDIM 200 步采样为例：

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_SUMtDJqicd/figures/024_Table_2.jpg]]
*Table 2: Ablation on sampling steps DDIM. Experiment on CIN-256 and Latent Diffusion Model*

| 方法 | FID ↓ | IS ↑ |
|------|-------|------|
| 静态 CFG | 3.467 | 176.8 |
| 线性调度 | **2.791** | **223.2** |
| 余弦调度 | 2.856 | 218.1 |

线性调度器实现了 FID 相对降低 19.5%（−0.676），IS 提升 46.4。余弦调度器同样取得了相近的改进幅度。值得注意的是，这一增益在不同 DDIM 采样步数（50、100、200 步）下保持稳定（Table 2），表明动态调度与采样步数之间不存在敏感的耦合关系。

### 文本到图像生成主要结果（Stable Diffusion）

在更大规模的文本到图像生成任务上，单调递增调度器同样展现出跨模型、跨评估指标的鲁棒改进。

**SD1.5 零样本 COCO 评估（Figure 7a）**：在推荐权重 ω=7.5 的等效设定下，线性调度器实现了 FID 降低 2.71（17% 相对改善），CLIP‑Score 提升 0.004（16% 相对改善）。用户研究（Figure 7b）进一步表明，线性调度器生成的样本在超过 60% 的比较中被人评者偏好。

**SDXL 评估（Figure 7c）**：线性与余弦调度器在 FID 与 CLIP‑Score 的折衷曲线上均优于静态基线，验证了该方法对更大规模模型的泛化能力。

**多样性分析（Table 16，Table 17）**：在 SD1.5 和 SDXL 上，启发式调度器在提升 FID 的同时也改善了样本多样性（分别基于 CLIP 和 DINO‑v2 特征计算），表明增益并非以牺牲多样性为代价。

### 去噪末尾阶段的引导消融

论文进一步探究了去噪末尾阶段（最后 30% 时间步）的引导强度对生成质量的影响（Table 1）。在 SD1.5 上：

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_SUMtDJqicd/figures/018_Table_1.jpg]]
*Table 1: Impact of removing/boosting CFG at the end with SD1.5*

- **完全移除末尾引导**：FID 显著恶化（+3.31），CLIP‑Score 大幅下降（−0.012），表明后期引导对维持语义一致性至关重要。
- **适度提升末尾引导（1.5×）**：FID 进一步改善 0.54 至 0.80，且几乎不损伤 CLIP‑Score。

这一发现揭示了单调递增调度器的一个潜在改进方向：在去噪极早期使用极低引导以降低冲突，在末尾阶段适度提高引导以强化条件对齐，形成“低开高走”的非对称调度策略。

### 参数化调度器的表现与局限性

为突破启发式调度的性能上限，论文进一步探索了两类参数化调度器（Figure 10，Figure 11，Figure 17）：

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_SUMtDJqicd/figures/011_Figure_10.jpg]]
*Figure 10: Class-conditioned generation results of parameterized clamp-linear and pcs on (a) CIFAR-10-DDPM and (b) CIN-256-LDM. Optimising parameters improves performances but these parameters do not generalize across models and datasets*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_SUMtDJqicd/figures/012_Figure_11.jpg]]
*Figure 11: Text-to-image performance for two parameterized schedulers: clamp-linear and pcs. For clamp-linear, (a) shows the guidance curves for different parameters and (b,c) displays the FID vs. CS for SD1.5 and SDXL, respectively. For pcs, (d) shows the guidance curves and (e,f) depicts the FID vs. CS. Optimal parameters for either clamp or pcs outperform the static baseline for both SD1.5 and SDXL*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_SUMtDJqicd/figures/020_Figure_17.jpg]]
*Figure 17: Class-conditioned image generation results of two parameterized families (clamplinear, clamp-cosine and pcs) on CIFAR-10 and CIN-256. Optimising parameters of guidance results in performance gains, however, these parameters do not generalize across models and datasets*

- **clamp‑linear**：在线性递增基础上对引导权重设置下界 c，避免早期引导过弱导致结构崩塌。其定义为 w_t = max(c, w_t)。
- **powered‑cosine (pcs)**：引入可调参数 s 控制余弦函数的形状，定义为 w_t = (1 − cos π((T−t)/T)^s) / 2 · w。

实验结果表明：
- **参数化调度器可超越启发式调度器和静态基线**。在 CIFAR‑10 DDPM 上，clamp‑linear 在 c=1.1 时取得最优 FID 与 IS（Table 5）；在 SD1.5 和 SDXL 上，clamp 和 pcs 的最优参数组合均优于线性调度（Figure 11）。
- **最优参数不具跨设定泛化性**。例如，clamp 的最优下界在 SD1.5 上约为 c=2，在 SDXL 上约为 c=4；pcs 的最优 s 值同样因模型和任务而异。这意味着每次部署均需进行高代价的网格搜索，是该方法的实际瓶颈。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_SUMtDJqicd/figures/033_Table_5.jpg]]
*Table 5: Experiment of clamp-linear on CIFAR-10 DDPM. We evaluate the FID and IS results for the baseline, parameterized method as clamp-linear of 50K images FID. Best FID and IS are highlighted, the optimal parameter seems at c = 1.1*

### 失败模式分析

单调递增调度器在总体引导水平较低时存在过度抑制早期引导的风险（Figure 8）。当等效 ω 设置过低时，去噪初期几乎无引导信号，导致生成结果出现结构性错误，如多腿、空间错位等。参数化方法中不恰当的参数选择（如 clamp 下界过低或 pcs 的 s 值过大）同样会引发类似问题。这表明动态调度需要在“降低早期冲突”与“维持基本结构引导”之间取得精细平衡。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_SUMtDJqicd/figures/009_Figure_8.jpg]]
*Figure 8: Failure cases of parameter-free and parameterized approaches: monotonically increasing guidance may mute the guidance at the beginning (especially when overall guidance is low), causing structural errors; and incorrectly chosen parameters can lead to fuzzy details and low saturation problems*

### 图像到图像翻译的拓展验证

在 SD1.5 的图像到图像翻译任务上，线性调度器和 clamp‑linear 调度器同样改善了 FID 与 CLIP‑Score 的折衷（Figure 14），且生成图像在细节保真度和条件一致性上优于静态基线。这一结果拓展了动态调度方法的适用范围，表明其增益并非局限于纯生成任务。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_SUMtDJqicd/figures/015_Figure_14.jpg]]
*Figure 14: Image-to-image performance and qualitative results on SD1.5. We show that (a) both linear and clamp-linear guidance schedulers enhance the balance between FID and CLIP score (CS) of the image-to-image translation task, and (b) the generated images exhibit improved detail and higher fidelity*

### 实验公平性保障

所有实验均遵循严格的公平性控制：引导曲线经面积归一化使总引导量与静态基线相等；评估使用相同的零样本 COCO 测试集（10K 或 30K）和预处理流程；采样器配置与步数在比较中固定（SD1.5 使用 DDIM 50 步，SDXL 使用 DPM‑Solver++ 25 步）；所有方法仅在推理时替换 ω(t)，计算开销与静态 CFG 完全相同，无需额外训练或微调。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_SUMtDJqicd/figures/044_Table_16.jpg]]
*Table 16: Experiment on SD1.5 with Diversity measures of 10K images, comparison between the baseline and two increasing heuristic shapes, linear and cosine*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_SUMtDJqicd/figures/045_Table_17.jpg]]
*Table 17: Experiment on SDXL with Diversity., we present FID vs. CLIP-Score (CS) for SDXL of 10K images, and we see the similar trending to Table 16 that the heuristic methods outperform the baseline, both on FID and Diversity*



## 定位与知识库关联

### 1. 与静态CFG基线的关系

本工作的直接基线是 **静态无分类器引导**（Classifier-Free Guidance, CFG），由 Ho & Salimans (2021) 提出。其核心公式为：

$$\hat{\epsilon}_{\theta}(x_t, c) = \epsilon_{\theta}(x_t, c) + \omega \bigl( \epsilon_{\theta}(x_t, c) - \epsilon_{\theta}(x_t) \bigr)$$

其中引导权重 $\omega$ 在整个去噪过程中保持恒定。该方法的根本瓶颈在于：**去噪早期阶段，生成项与引导项之间存在严重的方向冲突**。论文通过冲突度量 $\Phi$ 量化了这一现象——静态CFG下约50%的时间步呈现高冲突状态，且冲突幅度较大（Figure 5）。这种早期强引导迫使模型在噪声尚占主导的阶段强行对齐条件信号，导致保真度与多样性之间的固有权衡：低 $\omega$ 产生细节丰富但模糊的图像，高 $\omega$ 产生锐利但过度简化的图像。

本工作提出的 **动态CFG权重调度** 仅对上述公式做一处修改——将恒定 $\omega$ 替换为时间依赖函数 $\omega(t)$：

$$\hat{\epsilon}_{\theta}(x_t, c) = \epsilon_{\theta}(x_t, c) + \omega(t) \bigl( \epsilon_{\theta}(x_t, c) - \epsilon_{\theta}(x_t) \bigr)$$

这一改动在**推理时零额外计算开销**的前提下，通过将高强度引导推迟到去噪后期，显著降低了早期冲突。所有调度器均经过面积归一化（$\int_0^T \omega(t) dt = \omega T$），确保总引导量与静态基线严格可比，排除了引导总量差异带来的混淆效应。

### 2. 方法谱系中的定位

本工作处于 **CFG权重调度** 这一新兴子方向的系统化分析节点。此前已有工作尝试在扩散过程中变化引导权重并报告了性能提升，但缺乏统一的机理解释和系统比较。本工作的贡献在于：

- **首次建立了“单调递增调度器最优”的经验规律**，并通过负扰动分析（Figure 6b）和冲突可视化（Figure 5）给出了因果解释：早期移除引导改善FID，后期移除则严重损害FID。
- **提出了启发式调度器族**（线性、余弦、反线性、正弦、V形等），并证明仅单调递增的形状（线性、余弦）能一致超越静态基线。其中线性调度器的归一化形式为 $\omega(t) = 2(1 - t/T)\omega$。
- **引入参数化调度器族**作为上限探索，包括 powered-cosine 调度器（pcs）：

$$w_t = \frac{1 - \cos \pi \bigl(\frac{T-t}{T}\bigr)^s}{2} w$$

以及 clamp-linear 调度器（$w_t = \max(c, w_t)$），后者通过设置下界 $c$ 防止早期引导过弱导致结构崩塌。

### 3. 适用边界与跨设定泛化

**启发式调度器的泛化性较强**：线性与余弦调度器在 CIFAR-10 DDPM、ImageNet 256×256 LDM、SD1.5、SDXL 等多个模型和数据集上均一致改善 FID/IS/CLIP-Score 折衷，且增益在不同 DDIM 采样步数（50/100/200）下保持稳定（Table 2）。

**参数化调度器的泛化性存在显著局限**：clamp-linear 和 pcs 的最优参数强烈依赖于具体模型与任务设定。例如，clamp 的最优下界 $c$ 在 SD1.5 上为 2，在 SDXL 上则为 4；pcs 的最优形状参数 $s$ 同样无法跨模型迁移（Figure 10, Figure 11）。这意味着参数化方案在每次部署时都需要进行代价高昂的网格搜索，限制了其实际应用的便捷性。

**低总引导量下的结构风险**：当总体引导水平较低时，单调递增调度器可能在去噪早期过度抑制引导信号，导致生成结果出现结构性错误（如多腿、空间错位），这是该方法的一个已知失效模式（Figure 8）。

### 4. 局限性与开放问题

**已确认的局限**：

1. **参数化调度器缺乏自动调参机制**：最优参数依赖模型、任务和数据集的组合，必须针对每种设定单独搜索，无法零样本泛化。
2. **冲突建模停留在经验层面**：论文使用基于余弦相似度的冲突度量 $\Phi$，但缺乏对冲突产生根源的严格理论建模，无法从第一性原理推导最优调度器形状。
3. **采样器交互未充分探索**：研究仅在 DDIM 和 DPM-Solver++ 上验证了调度器效果，未探讨与 DDPM 随机采样或其他高级 ODE 求解器之间的理论交互。

**待解决的开放问题**：

1. **最优参数跨模型差异的理论根源**：为什么 clamp 的最优下界在 SD1.5 和 SDXL 上差异如此显著？这是否与模型容量、训练数据分布或条件嵌入空间的结构有关？
2. **自动化参数选择**：能否设计一种与模型/数据集无关的自动参数选择策略（如基于去噪过程中冲突度量的自适应调整），避免每次部署都进行网格搜索？
3. **超越单调递增的最优形状**：是否存在比线性/余弦更优的单调递增函数族，能进一步降低早期冲突的同时兼顾后期退火？参数化调度器的初步结果表明这一方向存在提升空间。
4. **与采样策略的协同设计**：动态调度器是否可以与自适应步长或噪声调度相结合，在采样效率和生成质量上获得联合增益？
5. **理论最优调度器的形式化**：如何在理论上形式化生成项与引导项之间的冲突，并以此为指导推导调度器的最优形状？这可能需要建立冲突与去噪过程信息论特性之间的桥梁。



## 原文 PDF

![[paperPDFs/TMLR_2024/Analysis_of_Classifier_Free_Guidance_Weight_Schedulers.pdf]]
