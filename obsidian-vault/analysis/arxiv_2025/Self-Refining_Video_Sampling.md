---
title: Self-Refining Video Sampling
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Self-Refining_Video_Sampling.pdf
project_link: "https://agwmon.github.io/self-refine-video/"
code_link: https://github.com/agwmon/self-refine-video
aliases:
- PPPPUAPP
- SRVS
tags:
- arxiv_2025
- topic/vision_multimodal_applications
core_operator: 将流匹配生成器重新解释为时间条件去噪自编码器（DAE），在推理时通过预测-扰动（Predict-and-Perturb）迭代循环进行自精炼，无需外部验证器或额外训练。
primary_logic: 利用预训练视频生成器内部的丰富运动与结构先验，通过伪吉布斯采样在推理阶段迭代地将视频潜变量向数据流形高密度区域拉拢，从而改善时序一致性和物理合理性；并引入基于自一致性预测差异的不确定性感知掩膜，选择性精炼运动区域，避免静态背景过度精炼带来的伪影。
claims:
- 在 Dynamic-bench 人类评估中，我们的方法在运动质量上以 73.57% 的偏好率显著超过默认采样器。
- 在机器人抓取成功率上，我们的方法比 Cosmos-Predict-2.5 基线提升了 11.0 个百分点（89.6 vs 79.2），且明显优于基于外部验证器的 rejection sampling (best-of-4)。
- 在 VideoPhy2 硬子集的物理合理性评估中，我们的方法在物理常识 (PC) 指标和人类评估中均大幅优于所有基线，人类评估对基线的偏好率达到 84%。
- Dynamic-bench 上 Human Eval Motion (preference rate for Ours) = 73.57%
---

# Self-Refining Video Sampling

> [!tip] 核心洞察
> 利用预训练视频生成器内部的丰富运动与结构先验，通过伪吉布斯采样在推理阶段迭代地将视频潜变量向数据流形高密度区域拉拢，从而改善时序一致性和物理合理性；并引入基于自一致性预测差异的不确定性感知掩膜，选择性精炼运动区域，避免静态背景过度精炼带来的伪影。

| 字段 | 内容 |
|------|------|
| 中文题名 | 自精炼视频采样 |
| 英文题名 | Self-Refining Video Sampling |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2601.18577) · [Project](https://agwmon.github.io/self-refine-video/) · [Code](https://github.com/agwmon/self-refine-video) |
| Topic | #topic/vision_multimodal_applications |
| Method | Predict-and-Perturb (P&P) with Uncertainty-aware P&P |
| Dataset | Dynamic-bench, PAI-Bench-G, VideoPhy2, PhyWorldBench |

> [!tip] 效果简介
> - Dynamic-bench 上，Human Eval Motion (preference rate for Ours) 73.57% vs Wan2.2 T2V default sampler (大幅领先，超过 70% 偏好率)；VBench Motion↑ 98.41 vs 98.01 (Wan2.2 T2V default) (+0.40)；VBench Consistency↑ 91.33 vs 90.68 (Wan2.2 T2V default) (+0.65)。
> - PAI-Bench-G (Robotics I2V) 上，Grasp Success Rate↑ (Cosmos-Predict-2.5 base) 89.6 vs 79.2 (Cosmos-Predict-2.5) (+11.0)；Grasp Success Rate↑ (Wan2.2-I2V base) 85.7 vs 77.3 (Wan2.2-I2V) (+8.4)；Robot-QA Accuracy↑ (Wan2.2-I2V) 80.3 vs 77.4 (Wan2.2-I2V) (+2.9)。
> - VideoPhy2 (Physics Alignment) 上，Human Eval (preference rate for Ours) 84.29% (physical commonsense preference) vs Wan2.2 T2V default sampler (大幅领先，84% 偏好率)。

## 概述

现代视频生成模型在复杂物理动态和运动连贯性方面仍存在明显不足。现有改进方案通常依赖外部验证器（如基于大语言模型的视频评分器）或需要额外训练，不仅计算成本高昂，而且域适应能力有限，难以捕捉细粒度的运动因果和物理合理性。

本文提出**自精炼视频采样（Self-Refining Video Sampling）**，一种无需外部验证器、无需额外训练的视频生成推理方法。其核心思想是将预训练的流匹配（Flow Matching）视频生成器重新解释为**时间条件去噪自编码器（DAE）**，在推理阶段通过**预测-扰动（Predict-and-Perturb, P&P）**迭代循环，将视频潜变量逐步拉向数据流形的高密度区域，从而改善时序一致性和物理合理性。在此基础上，引入基于模型自一致性预测差异的**不确定性感知掩膜**，对运动区域进行选择性精炼，避免静态背景的过度精炼伪影。

主要实验结果如下：

- **运动连贯性**：在 Dynamic-bench 人类评估中，本方法以 **73.57%** 的偏好率显著超过默认采样器（Table 1）。
- **物理合理性**：在 VideoPhy2 硬子集上，人类评估对基线的偏好率达到 **84%**；在 PhyWorldBench 的物理常识（PC）指标上，比 Wan2.2 T2V 默认采样器提升 **+10.7** 分（Table 3）。
- **机器人视频生成**：在 PAI-Bench-G 抓取成功率上，本方法比 Cosmos-Predict-2.5 基线提升 **11.0 个百分点**（89.6 vs 79.2），且明显优于基于外部验证器的拒绝采样（Table 2）。
- **空间一致性**：在 Wan2.2 T2V 上，SSIM 从 0.401 提升至 **0.485**（Table 5）。

本方法在流匹配和扩散模型上均展现出通用性，且仅引入约 40% 的额外推理时间开销。但需注意，P&P 本质上是局部搜索策略，对于需要全局规划的视觉推理任务（如迷宫求解）提升有限，且过度增加迭代次数可能导致模式坍塌。

## 背景与动机

### 视频生成的核心瓶颈：物理动态与运动连贯性

现代视频生成模型在规模化的图文数据训练下，已能产出视觉质量令人印象深刻的视频。然而，当场景涉及复杂物理动态——如体操动作的时序衔接、物体自由落体的轨迹合理性、机器人抓取操作的因果连贯——生成结果往往暴露出运动扭曲、物理违背和时间不一致等缺陷。这些失败并非源于模型容量的绝对不足，而是因为**标准采样过程未能充分利用预训练生成器内部已编码的丰富运动与结构先验**。

问题的本质在于：流匹配（Flow Matching）等主流生成范式在推理时依赖一阶常微分方程（ODE）求解器沿确定性轨迹推进，每一步仅做局部线性外推。当采样步数受限或噪声水平较高时，这种贪心策略容易偏离数据流形的高密度区域，导致生成的视频在细粒度运动因果和物理合理性上出现偏差。

### 现有解决方案的局限

针对上述问题，学术界和工业界提出了几类改进方案，但各自存在明显短板：

- **增加推理计算量（NFE×2）**：简单加倍函数评估次数（NFE）能部分缓解离散化误差，但边际收益递减，且未改变采样策略的本质缺陷。
- **无训练引导方法（FlowMo, CFG-Zero）**：通过梯度信号或改进的无分类器引导来增强运动连贯性，但依赖手工设计的能量函数或启发式规则，域适应能力有限，且梯度计算引入额外推理开销。
- **外部验证器拒绝采样（Cosmos-Reason1 7B）**：利用独立训练的视频评判模型从多个候选视频中择优，如 NVIDIA 的 Cosmos-Reason1 采用 best-of-4 策略。然而，这类方法需要额外训练和维护一个高质量验证器，计算成本高，且验证器的偏好偏差可能限制生成多样性。

上述方法的共同痛点在于：**它们或依赖于外部监督信号，或需要额外的训练阶段，未能直接挖掘生成器自身的自纠正潜力**。一个关键洞察被忽略了——预训练视频生成器本身就是一个强大的时间条件去噪自编码器（Denoising Autoencoder, DAE），其内部已经隐式学习了数据流形的几何结构。

### 本文动机：从“外部验证”到“内部自精炼”

本文的核心动机源于对**流匹配目标函数的重新审视**。通过数学推导，流匹配的损失函数可以等价地重写为加权去噪自编码器目标：

$$\mathcal{L}_{\mathrm{FM}}(\theta) = \mathbb{E}_{t, z_0, z_1} \left[ \frac{1}{(1-t)^2} \left\| \hat{z}_1^\theta - z_1 \right\|_2^2 \right]$$

其中 $\hat{z}_1^\theta = z_t + (1-t) u_\theta(z_t, t)$ 是生成器从噪声隐变量 $z_t$ 预测的干净样本。这一视角揭示了一个被忽视的事实：**流匹配生成器在所有噪声水平上都经过了去噪重建训练**，天然具备将偏离数据流形的样本“拉回”高密度区域的能力。

基于此，作者提出一个直接而优雅的问题：能否在推理时，让生成器**以自身为精炼器**，通过迭代的自纠正机制逐步改善生成质量，而无需任何外部验证器或额外训练？这一思路催生了**自精炼视频采样（Self-Refining Video Sampling）** 方法，其核心操作——预测-扰动（Predict-and-Perturb, P&P）循环——正是对上述 DAE 视角的自然利用：在固定噪声水平上交替执行预测（去噪重建）和扰动（重新加噪），形成伪吉布斯采样，将视频隐变量逐步拉向数据流形的高密度区域（图1示意了这一概念）。

### 关键设计动机

在实现自精炼的过程中，作者进一步识别出两个关键问题：

1. **精炼范围的选择**：视频中运动主体（如人物、物体）往往是物理错误和运动伪影的高发区域，而静态背景通常已经生成良好。对全视频无差别精炼不仅浪费计算，还可能在背景区域引入过饱和等伪影。因此，需要一种**不确定性感知的精炼策略**，自动识别并仅精炼高不确定性的运动区域。

2. **精炼时机的把握**：视频生成的不同噪声水平阶段承担不同功能——早期高噪声阶段主要确定粗粒度的运动轨迹和空间结构，后期低噪声阶段则负责细节纹理的生成。将精炼集中在**早期推理步**（噪声水平 $t < 0.2$）即可在运动连贯性上获得显著增益，同时避免对后期细节的不必要干预。

这两个设计动机直接塑造了后续的方法架构：**不确定性感知的预测-扰动（Uncertainty-aware P&P）** 采样算法，其技术细节将在方法章节中展开。

## 核心创新

本工作的核心创新在于将**推理时的自精炼能力内建于预训练视频生成器**，无需外部验证器、无需额外训练，也无需修改模型权重。其关键洞察在于：流匹配（Flow Matching）生成器可以被重新解释为时间条件去噪自编码器（time-conditioned DAE），从而在推理阶段激活一个伪吉布斯采样链，将视频隐变量逐步拉向数据流形的高密度区域。

### 方法本质：从 ODE 求解到伪吉布斯采样

传统流匹配推理依赖 ODE 求解器沿时间轴单向推进：

$$z_{t_{i+1}} = z_{t_i} + (t_{i+1} - t_i) u_\theta(z_{t_i}, t_i)$$

每个时间步仅做一次向量场评估，缺乏对生成质量的自我审视与修正能力。本方法的核心重构在于：将流匹配目标重新表达为加权去噪自编码器损失：

$$\mathcal{L}_{\mathrm{FM}}(\theta) = \mathbb{E}_{t, z_0, z_1} \left[ \frac{1}{(1-t)^2} \left\| \hat{z}_1^\theta - z_1 \right\|_2^2 \right]$$

其中 $\hat{z}_1^\theta = z_t + (1-t) u_\theta(z_t, t)$ 是模型对干净样本的预测。这一视角揭示了生成器内部蕴含的**预测-重建能力**，进而催生了 Predict-and-Perturb（P&P）迭代精炼机制。

### Changed Slots：四个维度的推理时干预

相对于默认 ODE 采样器，本方法在以下四个关键环节引入了结构性改变：

**1. 内部自我精炼机制（从无到有）**

在每个推理时间步内，引入 Predict-and-Perturb 循环，交替执行两个操作：
- **Predict**：$D_{\theta}(z_t, t) := z_t + (1 - t) u_{\theta}(z_t, t)$，将当前噪声隐变量映射为干净样本预测；
- **Perturb**：$R_{\epsilon}(z, t) := t z + (1 - t) \epsilon$，在相同噪声水平上对预测结果施加扰动。

两者组合形成单次 P&P 迭代：

$$z_t^{(k+1)} = R_{\epsilon_k}(D_{\theta}(z_t^{(k)}, t), t)$$

这一过程本质上是**在固定噪声水平上的伪吉布斯采样**，利用生成器自身的重建能力将预测端点 $\hat{z}_1$ 拉向数据流形，从而改善时序一致性和物理合理性。2D 合成数据集上的验证实验（Figure 2）表明，P&P 生成的样本比 Euler 求解器更贴近真实数据流形，且固定时间步下的迭代 P&P 能持续将预测拉向流形高密度区。

**2. 精炼作用范围（从全时间步到仅早期时间步）**

实验发现，视频的粗粒度运动与结构主要在推理的前约 20% 噪声水平（$t < 0.2$）内确定。将 P&P 仅应用于这些早期步骤即可显著改善运动连贯性，而在后期步骤施加精炼的增益微小（见 Figure 17）。这一发现大幅降低了计算开销——默认设置下，额外推理时间仅约 40%。

**3. 精炼区域选择（从全局统一到不确定性感知）**

对整个隐变量统一施加 P&P 精炼会导致静态背景区域的过度饱和伪影（Figure 9）。本方法引入**不确定性感知掩膜**，利用模型自一致性预测差异来识别需要精炼的运动区域：
- 计算相邻两次 P&P 迭代中预测结果的通道平均 L1 差异，得到不确定性图 $\mathbf{U}$；
- 通过阈值 $\tau$ 将不确定性图二值化为精炼掩膜 $M_{t_i}^{(k)}$；
- 仅对高不确定性区域（运动主体）使用精炼后的隐变量，低不确定性区域（背景）保留上一次迭代结果：

$$z_{t_{i+1}}^{(k)} \gets M_{t_i}^{(k)} \odot z_{t_{i+1}}^{(k)} + (1 - M_{t_i}^{(k)}) \odot z_{t_{i+1}}^{(k-1)}$$

Figure 3 的可视化证实，不确定性图在运动相关区域呈现高值，背景区域为低值，验证了该信号对运动区域的自然选择性。

**4. 每时间步采样策略（从单步到精炼后步进）**

标准 ODE 步直接使用当前隐变量进行向量场评估。本方法在每个 ODE 步之前，先通过 $K_f$ 次 P&P 迭代得到精炼隐变量 $z_{t_i}^*$，再执行：

$$z_{t_{i+1}} = z_{t_i}^* + \Delta t \cdot u_\theta(z_{t_i}^*, t_i)$$

默认 $K_f=3$ 在质量与开销之间取得平衡（Figure 16 消融实验）。值得注意的是，算法中不确定性图的计算复用了已有预测结果，不引入额外的函数评估次数（NFE）。

### 创新的理论根基与边界

本方法的理论基础可追溯至广义去噪自编码器的伪吉布斯马尔可夫链（Bengio et al., 2013），但在视频生成领域首次将其与流匹配框架结合，并引入不确定性感知的选择性精炼策略。与依赖外部验证器的拒绝采样方法（如 **Cosmos-Reason1 7B**，Azzolini et al., 2025）相比，本方法完全依赖生成器内部先验，避免了外部模型的域适应问题和额外计算成本；与基于梯度的免训练引导方法（如 **FlowMo**，Shaulov et al., 2025）相比，本方法无需反向传播计算梯度，推理效率更高。

**需要手动验证的点**：论文声称 P&P 可迁移至扩散模型（在 CogVideoX 上的初步验证见 Figure 23），但该验证仅为定性展示，其在各类扩散架构上的最优超参数设置和鲁棒性尚缺乏系统性研究。此外，论文未报告与公平性（如不同群体、场景下的表现差异）相关的实验或讨论。

## 整体框架

自精炼视频采样（Self-Refining Video Sampling）将预训练的流匹配视频生成器重新解释为一个时间条件去噪自编码器（DAE），在推理阶段通过**预测-扰动（Predict-and-Perturb, P&P）**迭代循环，利用模型内部的运动与结构先验实现自我精炼，无需外部验证器或额外训练。

### 核心思想

流匹配模型的标准 ODE 采样步为：

$$z_{t_{i+1}} = z_{t_i} + (t_{i+1} - t_i) u_\theta(z_{t_i}, t_i)$$

该过程沿概率流路径从噪声逐步生成视频潜变量。然而，现代视频生成器在处理复杂物理动态和运动连贯性方面仍存在不足——采样轨迹可能偏离数据流形的高密度区域，导致运动不连贯或物理不合理。

本文的核心洞察在于：流匹配目标可以等价地表示为加权去噪自编码器目标：

$$\mathcal{L}_{\mathrm{FM}}(\theta) = \mathbb{E}_{t, z_0, z_1} \left[ \frac{1}{(1-t)^2} \left\| \hat{z}_1^\theta - z_1 \right\|_2^2 \right]$$

其中 $\hat{z}_1^\theta = z_t + (1-t) u_\theta(z_t, t)$。这意味着预训练的向量场 $u_\theta$ 本质上在所有噪声水平 $t$ 上都充当了一个去噪自编码器。基于这一视角，方法利用广义 DAE 的伪吉布斯马尔可夫链，在每个离散推理时间步上交替进行“重建”与“破坏”，将预测结果逐步拉向数据流形。

### Pipeline 模块与数据流

整体推理 pipeline 由以下模块构成，其输入输出关系如 Algorithm 1 所示：

**1. Predict（去噪预测）**

给定当前噪声隐变量 $z_t$ 和噪声水平 $t$，利用训练好的向量场 $u_\theta$ 将其映射为干净样本的预测：

$$D_{\theta}(z_t, t) := z_t + (1 - t) u_{\theta}(z_t, t)$$

该模块复用预训练生成器的前向传播，不引入额外参数。

**2. Perturb（噪声扰动）**

在相同的噪声水平 $t$ 上，对预测结果进行线性插值扰动，将其重新拉回噪声空间：

$$R_{\epsilon}(z, t) := t z + (1 - t) \epsilon$$

其中 $\epsilon \sim \mathcal{N}(0, I)$ 为随机采样的高斯噪声。Predict 与 Perturb 交替执行构成一次 P&P 迭代：

$$z_t^{(k+1)} = \mathrm{P\&P}_{\epsilon_k}(z_t^{(k)}, t) := R_{\epsilon_k}(D_{\theta}(z_t^{(k)}, t), t)$$

经过 $K_f$ 次迭代后得到精炼隐变量 $z_{t_i}^*$，再送入标准 ODE 求解器：

$$z_{t_{i+1}} = z_{t_i}^* + \Delta t \cdot u_\theta(z_{t_i}^*, t), \quad \Delta t = t_{i+1} - t_i$$

**3. Uncertainty Map Computation（不确定性图计算）**

为选择性精炼运动区域、避免静态背景过度精炼带来的伪影，方法计算相邻两次预测之间的通道平均 L1 差异：

$$\mathbf{U}(z_{t_i}^{(k-1)}, z_{t_i}^{(k)}) := \frac{1}{C} \| D_{\theta}(z_{t_i}^{(k-1)}, t_i) - D_{\theta}(z_{t_i}^{(k)}, t_i) \|_1$$

该不确定性图在运动主体区域呈现高值，在静态背景区域呈现低值（见 Figure 3）。

**4. Uncertainty Mask Generation（不确定性掩膜生成）**

通过阈值 $\tau$ 将连续的不确定性图二值化为精炼/保留掩膜：

$$M_{t_i}^{(k)} := \mathbb{1}\left( \mathbf{U}(z_{t_i}^{(k-1)}, z_{t_i}^{(k)}) > \tau \right)$$

默认 $\tau = 0.25$ 能稳健地分离运动区域和静态区域。

**5. Masked ODE Update（掩膜化 ODE 更新）**

对高不确定性区域（$M=1$）采用 P&P 精炼后的隐变量，对低不确定性区域（$M=0$）保留上一次迭代的隐变量，融合后送入 ODE 求解器：

$$z_{t_{i+1}}^{(k)} \gets M_{t_i}^{(k)} \odot z_{t_{i+1}}^{(k)} + (1 - M_{t_i}^{(k)}) \odot z_{t_{i+1}}^{(k-1)}$$

该设计的关键在于：Lines 5 和 10 中不确定性图的计算复用已有预测结果，不引入额外 NFE。

### 关键设计决策

**精炼作用范围**：P&P 仅在前约 20% 的噪声水平（$t < 0.2$）上应用。消融实验（Figure 17）表明，粗粒度的运动与结构主要在早期推理步确定，后期步的精炼增益微小。这一设计显著降低了计算开销——默认设置下仅引入约 40% 的额外推理时间。

**不确定性感知**：消融实验（Figure 9）显示，不带不确定性掩膜的多次 P&P（$K_f > 3$）会在背景等静态区域造成过饱和伪影，而 Uncertainty-aware P&P 通过选择性精炼有效抑制了该问题。

**通用性**：P&P 不仅适用于流匹配模型（如 Wan2.2、Cosmos-Predict-2.5），也可迁移至扩散模型（如 CogVideoX），在修复截断光剑等伪影上同样有效（Figure 23）。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2601_18577/figures/001_Figure_1.jpg]]
*Figure 1: Concept of the self-refining video sampling. Within the same noise level, the video latent zt is refined as the predicted endpoint zˆ1 is pulled toward the data manifold*

## 核心模块与公式推导

### 4.1 流匹配作为时间条件去噪自编码器

自精炼视频采样的理论根基在于对**流匹配（Flow Matching）**目标的重新解释。标准流匹配训练一个向量场 $u_\theta(z_t, t)$，使其逼近从噪声分布到数据分布的最优传输路径。其训练目标为：

$$
\mathcal{L}_{\mathrm{FM}}(\theta) = \mathbb{E}_{t, z_0, z_1} \left[ || u_\theta(z_t, t) - (z_1 - z_0) ||_2^2 \right] \tag{2}
$$

其中 $z_t = t z_1 + (1 - t) z_0$，$z_0 \sim \mathcal{N}(0, I)$ 为纯噪声，$z_1$ 为数据样本，$t \in [0, 1]$ 为噪声水平。

**核心洞察**：该目标可等价地重写为加权去噪自编码器（DAE）形式：

$$
\mathcal{L}_{\mathrm{FM}}(\theta) = \mathbb{E}_{t, z_0, z_1} \left[ \frac{1}{(1-t)^2} \left\| \hat{z}_1^\theta - z_1 \right\|_2^2 \right] \tag{3}
$$

其中 $\hat{z}_1^\theta = z_t + (1-t) u_\theta(z_t, t)$ 是从噪声隐变量 $z_t$ 对干净样本 $z_1$ 的预测。这意味着：**一个训练好的流匹配生成器，实质上是一个在所有噪声水平上联合训练的时间条件去噪自编码器**。这一视角为推理阶段的自精炼提供了理论许可——生成器内部已经蕴含了丰富的运动与结构先验，可以在推理时被激活用于自我修正。

### 4.2 Predict-and-Perturb（P&P）迭代精炼

基于上述 DAE 视角，论文提出 **Predict-and-Perturb（P&P）** 循环，在推理的每个离散时间步上执行伪吉布斯采样，将视频隐变量拉向数据流形的高密度区域。

**Predict 算子**（去噪预测）：

$$
D_{\theta}(z_t, t) := z_t + (1 - t) u_{\theta}(z_t, t) \tag{5}
$$

将当前噪声隐变量 $z_t$ 映射为干净样本的预测 $\hat{z}_1$。

**Perturb 算子**（加噪扰动）：

$$
R_{\epsilon}(z, t) := t z + (1 - t) \epsilon \tag{6}
$$

在噪声水平 $t$ 上，用新采样的噪声 $\epsilon \sim \mathcal{N}(0, I)$ 对样本 $z$ 进行线性插值扰动，使其回到带噪状态。

**单次 P&P 迭代**：

$$
z_t^{(k+1)} = \mathrm{P\&P}_{\epsilon_k}(z_t^{(k)}, t) := R_{\epsilon_k}(D_{\theta}(z_t^{(k)}, t), t) \tag{8}
$$

交替执行 Predict 和 Perturb，构成一条马尔可夫链。在固定噪声水平 $t$ 上迭代 $K_f$ 次后，得到精炼隐变量 $z_t^*$，再送入标准 ODE 求解器执行时间推进：

$$
z_{t_{i+1}} = z_{t_i}^* + \Delta t \cdot u_{\theta}(z_{t_i}^*, t_i), \quad \Delta t = t_{i+1} - t_i \tag{9}
$$

**精炼作用范围**：P&P 仅在推理的前约 20% 噪声水平（$t < 0.2$）上应用。这是因为粗粒度的运动轨迹和空间结构主要在早期去噪步中确定，后期步的精炼增益微小（见 Figure 17 消融验证）。默认迭代次数 $K_f = 3$，在质量提升与额外计算开销之间取得平衡。

### 4.3 不确定性感知的 P&P（Uncertainty-aware P&P）

直接对所有空间-时间位置进行 P&P 精炼会导致**静态背景区域的过饱和伪影**（见 Figure 9）。为解决此问题，论文引入基于模型自一致性预测差异的不确定性掩膜机制。

**不确定性图计算**：在第 $k$ 次 P&P 迭代中，计算相邻两次 Predict 输出之间的通道平均 L1 差异：

$$
\mathbf{U}(z_{t_i}^{(k-1)}, z_{t_i}^{(k)}) := \frac{1}{C} \| D_{\theta}(z_{t_i}^{(k-1)}, t_i) - D_{\theta}(z_{t_i}^{(k)}, t_i) \|_1
$$

其中 $C$ 为隐变量通道数。该值衡量模型对每个空间-时间位置预测的**自一致性**——运动主体区域因动态变化大，预测波动剧烈，呈现高不确定性；静态背景区域预测稳定，呈现低不确定性（见 Figure 3 可视化）。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2601_18577/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of uncertainty maps, showing higher values in motion-related regions. Maps are computed at*

**二值掩膜生成**：通过全局阈值 $\tau$ 将连续不确定性图二值化：

$$
M_{t_i}^{(k)} := \mathbb{1}\left( \mathbf{U}(z_{t_i}^{(k-1)}, z_{t_i}^{(k)}) > \tau \right) \tag{10}
$$

默认 $\tau = 0.25$，能稳健地分离运动区域与静态区域。

**掩膜融合的 ODE 更新**：在时间推进时，仅对高不确定性区域使用当前 P&P 精炼后的隐变量，低不确定性区域保留上一次迭代的结果：

$$
z_{t_{i+1}}^{(k)} \gets M_{t_i}^{(k)} \odot z_{t_{i+1}}^{(k)} + (1 - M_{t_i}^{(k)}) \odot z_{t_{i+1}}^{(k-1)} \tag{11}
$$

该设计实现了**选择性精炼**：运动区域通过 P&P 修正物理不一致和抖动伪影，背景区域保持不变以避免过度精炼引入的失真。值得注意的是，算法中不确定性图计算所需的 Predict 输出可复用已有结果，不引入额外的函数评估次数（NFE）。

### 4.4 方法谱系与知识库定位

**核心创新定位**：P&P 属于**训练无关的推理时采样策略**，与以下工作形成差异化对比：

- **标准 ODE 求解器**（如 **UniPC**，Zhao et al., 2023）：沿单一向量场轨迹推进，缺乏对数据流形的迭代逼近能力。
- **基于梯度的引导方法**（如 **FlowMo**，Shaulov et al., 2025）：通过额外梯度计算引导生成，引入显著推理开销（Table 1 标注额外推理时间）。
- **外部验证器拒绝采样**（如 **Cosmos-Reason1 7B**，Azzolini et al., 2025）：依赖独立训练的验证模型筛选候选视频，域适应能力受限，且 best-of-4 策略在机器人抓取任务上显著弱于 P&P（Table 2：89.6 vs 79.2）。
- **CFG 改进变体**（如 **CFG-Zero**，Fan et al., 2025）：优化引导强度，但不涉及隐变量在固定噪声水平上的迭代精炼。

P&P 的独特优势在于**完全利用生成器自身的内部先验**，无需外部模型、无需额外训练、无需梯度回传，仅通过推理时的预测-扰动循环即可显著改善运动连贯性和物理合理性。该方法在流匹配模型（**Wan2.2 T2V/I2V**、**Cosmos-Predict-2.5**）和扩散模型（**CogVideoX**，Yang et al., 2025b）上均得到验证，具备跨架构通用性。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2601_18577/figures/030_Figure_23.jpg]]
*Figure 23: P&P is also applicable to diffusion-based video generation models (e.g., CogVideoX (Yang et al., 2025b)), where it corrects video artifacts, such as a truncated lightsaber and distortions around the teddy bear’s mouth. (Image credit: MuDI (Jang et al., 2024))*

## 实验与分析

### 核心评估设计

论文在四个维度上验证自精炼视频采样的有效性：运动连贯性、物理合理性、空间一致性，以及机器人领域的物理真实性。评估覆盖文本到视频（T2V）和图像到视频（I2V）两种生成范式，基座模型包括 **Wan2.2-A14B T2V/I2V**（Wang et al., 2025a）和 **Cosmos-Predict-2.5**（Ali et al., 2025）。对比基线包括默认 ODE 求解器 **UniPC**（Zhao et al., 2023）、加倍函数评估次数的 NFE×2、改进分类器自由引导的 **CFG-Zero**（Fan et al., 2025）、基于梯度的免训练引导方法 **FlowMo**（Shaulov et al., 2025），以及基于外部验证器 **Cosmos-Reason1 7B**（Azzolini et al., 2025）的拒绝采样策略（best-of-4）。

### 运动连贯性

在 Dynamic-bench 人类评估中，自精炼采样以 **73.57%** 的偏好率显著超过 Wan2.2 T2V 默认采样器（Table 1 left），表明人类评估者在复杂运动场景下强烈倾向于本方法生成的视频。在 VBench 自动指标上，本方法在 Motion 指标上达到 **98.41**（默认采样器 98.01，+0.40），在 Consistency 指标上达到 **91.33**（默认采样器 90.68，+0.65），均取得最优结果（Table 1 right）。值得注意的是，FlowMo 虽引入了梯度计算带来的额外推理时间，但运动连贯性指标仍低于本方法。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2601_18577/figures/004_Table_1.jpg]]
*Table 1: Dynamic-bench results measuring motion coherence for challenging motions using Wan2.2-A14B T2V. Human evaluation shows the percentage of votes favoring ours. Additional inference time (*) of FlowMo is introduced by gradient computation*

定性对比（Figure 4）展示了体操等复杂运动场景下，默认采样器产生运动模糊或肢体错位，而自精炼采样显著改善了动作的连贯性和结构完整性。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2601_18577/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison on challenging motion generation*

### 物理合理性

在 VideoPhy2 硬子集上，自精炼采样在物理常识（PC）人类评估中以 **84.29%** 的偏好率大幅领先所有基线（Table 3）。在 PhyWorldBench 上，使用 Gemini 3 Flash 自动评分的 PC 指标达到 **40.0**，较默认采样器的 29.3 提升 **+10.7**，远超其他免训练方法。这表明 P&P 循环能有效将视频潜变量拉向物理合理的数据流形区域。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2601_18577/figures/012_Table_3.jpg]]
*Table 3: Videophy2 and PhyWorldBench evaluation results using Wan2.2-A14B T2V. Human evaluation shows the percentage of votes favoring ours*

在 PisaBench 自由落体实验中（Table 4），本方法在 L2 距离（0.128 vs 0.132）、Chamfer 距离（0.338 vs 0.348）和 IoU（0.074 vs 0.069）上全面优于 Wan2.2 I2V 基线，进一步验证了物理动态建模的改善。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2601_18577/figures/013_Table_4.jpg]]
*Table 4: PisaBench evaluation. (Left) Quantitative results on the full real dataset. (Right) Visualization of 32 generated free-fall trajectories. Physically implausible falls are shown in red*

### 机器人物理真实性

在 PAI-Bench-G 机器人抓取评估中（Table 2），基于 Cosmos-Predict-2.5 的自精炼采样将抓取成功率从 **79.2** 提升至 **89.6**（+11.0 个百分点），基于 Wan2.2-I2V 的抓取成功率从 77.3 提升至 **85.7**（+8.4 个百分点）。Robot-QA 准确率也从 77.4 提升至 **80.3**（+2.9）。关键发现是，本方法不仅显著优于默认采样器，还明显超过基于外部验证器的拒绝采样策略（best-of-4），证明内部自精炼在物理交互建模上比外部验证器选择更有效。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2601_18577/figures/009_Table_2.jpg]]
*Table 2: PAI-Bench-G evaluation results on robotics I2V generation. Grasp is measured by Gemini 3 Flash, and Robot-QA is measured by Qwen2.5-VL-72B*

### 空间一致性

在空间一致性评估中（Table 5），自精炼采样将 SSIM 从 **0.401** 提升至 **0.485**（+0.084）。该评估通过相机姿态变换后的视角重访，测量帧对之间的结构保持程度，表明 P&P 精炼有助于维持场景几何的一致性。

### 消融实验

**不确定性感知策略的关键作用**（Figure 9）：不带不确定性掩膜的多次 P&P（K_f > 3）会在静态背景区域造成过饱和伪影，而 Uncertainty-aware P&P 通过选择性精炼运动区域有效抑制了该问题。这验证了基于自一致性预测差异的不确定性掩膜在分离运动主体与静态背景上的有效性。

**P&P 作用阶段的敏感性**（Figure 17）：仅在早期推理步（α < 0.2，即前约 20% 的噪声水平）应用 P&P 即可显著改善运动连贯性；在后期步应用 P&P 的增益微小。这与“粗粒度运动与结构主要在早期噪声水平确定”的核心假设一致。

**超参数 K_f 和 τ 的影响**（Appendix A.7, Figure 16）：增加 P&P 迭代次数 K_f 会加强精炼效果，但额外 NFE 随之增加，且样本与基线的偏离更大；默认 K_f=3 在质量-开销间取得平衡。不确定性阈值 τ 主要控制背景外观和整体色调的保留，τ=0.25 能稳健地分离运动区域和静态区域。

**方法通用性**（Appendix B.6, Figure 23）：P&P 在扩散模型 CogVideoX（Yang et al., 2025b）上也成功修复了截断光剑等伪影，证明该方法对流匹配和扩散模型均适用，具备跨架构迁移能力。

### 失败模式与局限性

1. **局部搜索的边界**：P&P 本质上是局部搜索策略，对于需要全局规划的视觉推理任务提升有限。Figure 8 显示，在图遍历任务中自精炼将成功率从 0.1 提升至 0.8，但在迷宫求解任务中成功率仍接近零——因为迷宫求解需要长程规划能力，局部精炼无法弥补这一缺陷。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2601_18577/figures/014_Figure_8.jpg]]
*Figure 8: Examples of self-refinement applied to visual reasoning tasks: (Top) graph traversal and (Bottom) maze solving from Wiedemer et al. (2025). We use Wan2.2-A14B I2V as the base model. For graph traversal, self-refinement yields a dramatic improvement in the success rate from 0.1 to 0.8. For maze solving, self-refinement does not yield meaningful gain, with success remaining near zero*

2. **过度精炼与模式坍塌**：增加 P&P 迭代次数虽能加强精炼效果，但会导致模式坍塌（mode-seeking behavior），尤其在图像生成中更为明显。论文指出在精炼强度与多样性之间的更优平衡仍待探索。

3. **计算开销**：默认设置下约引入 40% 的额外推理时间，在资源受限场景中仍需进一步降低。通过保持总 NFE 不变的方式可部分缓解，但效率-性能的帕累托改进仍需后续工作。

4. **超参数保守性**：保守的超参数设置可能削弱精炼效果，需要更大的 K_f 才能达到同等强度。自适应的时间依赖阈值 τ_t 可能是改进方向。

5. **扩散模型适配**：在 CogVideoX 上的初步验证显示 P&P 可迁移，但各类扩散架构上的最优设置和鲁棒性尚需系统研究。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2601_18577/figures/024_Figure_16.jpg]]
*Figure 16: Ablation studies on the hyperparameters Kf and τ*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2601_18577/figures/025_Figure_17.jpg]]
*Figure 17: Ablation studies on the hyperparameter α. Gray blocks indicate Euler method and orange blocks indicate P&P. P&P significantly improves motion coherence when applied in earlier steps (b-c), while providing only marginal gains at later steps (d-e)*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2601_18577/figures/002_Figure_2.jpg]]
*Figure 2: Sampling comparison on a 2D synthetic dataset. (ab) P&P generates samples closer to the data manifold than the Euler solver. (c-d) With a fixed timestep, iterative P&P pulls the prediction*

## 方法谱系与知识库定位

### 核心突破：将生成器重新解释为自精炼器

本工作的核心创新在于对**流匹配（Flow Matching）视频生成器**的功能重新解释。传统上，流匹配模型在推理时仅作为从噪声到数据的单向 ODE 求解器使用。本文证明，流匹配的训练目标可以等价地重新表述为**时间条件去噪自编码器（Time-conditioned DAE）** 的加权损失（Eq. 3），从而在推理阶段解锁了生成器的**自精炼能力**。

这一重新解释使得预训练的生成器无需任何外部验证器或额外训练，即可通过**预测-扰动（Predict-and-Perturb, P&P）** 循环执行伪吉布斯采样，将视频潜变量迭代地拉向数据流形的高密度区域。这从根本上区别于以下现有方法：

- **外部验证器方法**：如基于 **Cosmos-Reason1 7B**（Azzolini et al., 2025）的 rejection sampling，需要额外训练视频批评模型，计算成本高且域适应能力受限。本文在 PAI-Bench-G 机器人抓取任务上的实验表明，P&P 的抓取成功率（89.6）显著优于 best-of-4 rejection sampling（Table 2），且无需外部模型。
- **梯度引导方法**：如 **FlowMo**（Shaulov et al., 2025）通过计算额外梯度来改善运动连贯性，引入显著的额外推理时间。P&P 仅需约 40% 的额外推理开销，且无需反向传播。
- **改进求解器方法**：如 **UniPC**（Zhao et al., 2023）或增加函数评估次数（NFE×2），仅改变 ODE 求解精度，无法利用生成器内部的运动与结构先验进行主动精炼。在 Dynamic-bench 上，P&P 以 73.57% 的人类偏好率大幅超越默认 UniPC 采样器（Table 1）。

### 知识来源与理论根基

P&P 的理论基础可追溯到**广义去噪自编码器（Generalized DAE）** 的伪吉布斯马尔可夫链（Bengio et al., 2013），但本文首次将其成功应用于**大规模视频生成模型的推理阶段**。关键洞察在于：

1. **流匹配的 DAE 等价性**：流匹配损失 $\mathcal{L}_{\mathrm{FM}}(\theta)$ 可重写为 $\mathbb{E}_{t, z_0, z_1} \left[ \frac{1}{(1-t)^2} \left\| \hat{z}_1^\theta - z_1 \right\|_2^2 \right]$，其中 $\hat{z}_1^\theta = z_t + (1-t) u_\theta(z_t, t)$ 即为干净样本的预测（Eq. 3）。这意味着预训练的向量场 $u_\theta$ 天然具备去噪重建能力。

2. **噪声水平作为精炼阶段**：在流匹配中，噪声水平 $t$ 控制着从纯噪声（$t=0$）到干净数据（$t=1$）的过渡。P&P 在固定的 $t$ 上交替执行 Predict（$D_\theta$，Eq. 5）和 Perturb（$R_\epsilon$，Eq. 6），形成局部精炼循环。实验表明，仅在早期噪声水平（$t < 0.2$，即前约 20% 的推理步）应用 P&P 即可显著改善运动连贯性，因为粗粒度的运动和结构在此阶段确定（Figure 17）。

3. **不确定性感知的自适应精炼**：本文进一步引入**不确定性掩膜**机制（Eq. 10-11），利用连续两次预测的 L1 差异 $\mathbf{U}(z_{t_i}^{(k-1)}, z_{t_i}^{(k)})$ 衡量模型在每个空间-时间位置的自一致性。高不确定性区域（通常对应运动主体）被选择性精炼，而低不确定性区域（静态背景）被保留，有效避免了过度精炼导致的背景过饱和伪影（Figure 9）。

### 在视频生成知识库中的定位

P&P 在视频生成知识库中占据了一个独特的位置——**训练无关的推理时自精炼方法**。与现有工作的关系可总结如下：

| 方法类别 | 代表工作 | 核心机制 | P&P 的差异 |
|---------|---------|---------|-----------|
| 外部验证器 | Cosmos-Reason1 (Azzolini et al., 2025) | 训练视频批评模型进行 rejection sampling | 无需外部模型，利用生成器内部先验 |
| 梯度引导 | FlowMo (Shaulov et al., 2025) | 通过梯度优化改善运动 | 无需反向传播，计算开销更低 |
| 改进求解器 | UniPC (Zhao et al., 2023) | 高阶 ODE 求解 | 主动精炼潜变量，而非仅提高求解精度 |
| CFG 改进 | CFG-Zero (Fan et al., 2025) | 改进无分类器引导 | 正交于引导策略，可与 CFG 叠加使用 |

P&P 的适用边界涵盖多个视频生成基座模型：
- **流匹配模型**：在 **Wan2.1/Wan2.2 T2V & I2V**（Wang et al., 2025a）和 **Cosmos-Predict-2.5**（Ali et al., 2025）上均取得显著提升。
- **扩散模型**：初步验证显示 P&P 可迁移至 **CogVideoX**（Yang et al., 2025b），能够修复截断光剑等伪影（Figure 23），但其在各类扩散架构上的最优设置尚需系统研究。

### 局限与开放问题

尽管 P&P 在运动连贯性、物理合理性和空间一致性上表现出色，但存在以下边界和待解决问题：

**已知局限**：
1. **局部搜索的固有限制**：P&P 本质上是局部精炼，对于需要全局规划的推理任务（如迷宫求解）提升有限——在迷宫任务中成功率接近零（Figure 8）。这需要结合全局搜索策略或外部验证器来弥补。
2. **模式坍塌风险**：过度增加 P&P 迭代次数 $K_f$ 会导致 mode-seeking behavior，尤其在图像生成中更为明显。默认 $K_f=3$ 在质量-开销间取得平衡（Appendix A.7），但更优的多样性控制策略仍待探索。
3. **计算开销**：默认设置引入约 40% 的额外推理时间。虽然通过保持总 NFE 不变可部分缓解，但效率-性能的帕累托改进仍需后续工作。
4. **超参数敏感性**：保守的超参数设置可能削弱精炼效果，需要更大的 $K_f$ 才能达到同等强度。不确定性阈值 $\tau=0.25$ 能稳健分离运动与静态区域（Figure 16），但全局固定阈值可能无法适应不同噪声水平下的精炼需求。

**开放问题**：
- 能否设计**自适应时间依赖阈值 $\tau_t$**，以更精细地控制不同噪声水平下的精炼区域？
- 如何将**外部验证器或全局规划信号**与 P&P 有机结合，以改善离散推理和长期依赖任务的性能？
- 能否通过**知识蒸馏或推测性采样**进一步降低自精炼的计算开销，使其适用于资源受限的场景？
- P&P 在**更长视频、更高分辨率以及多模态条件**（如音频-视频联合生成）下的性能和鲁棒性如何？
- 是否可以通过分析 P&P 的**能量景观**来解释其收敛特性，并为超参数选择提供理论指导？
- 能否采用**异构模型或专门微调的模型**来承担精炼角色，以进一步提高跨域泛化能力？

## 原文 PDF

![[paperPDFs/arxiv_2025/Self-Refining_Video_Sampling.pdf]]