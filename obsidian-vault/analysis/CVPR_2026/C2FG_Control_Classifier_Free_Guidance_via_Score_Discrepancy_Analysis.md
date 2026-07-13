---
title: "C^2FG: Control Classifier-Free Guidance via Score Discrepancy Analysis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/C_2FG_Control_Classifier_Free_Guidance_via_Score_Discrepancy_Analysis.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Gao_C2FG_Control_Classifier-Free_Guidance_via_Score_Discrepancy_Analysis_CVPR_2026_paper.html
project_link: null
code_link: null
aliases:
- CCFGCF
- C2CCFGSDA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 时间依赖的引导强度控制函数 ω(t) = ω₀ exp(λ (1 - t/t_max))，它根据扩散时间自适应地缩放条件与无条件评分的差值。
primary_logic: 在扩散模型的前向过程中，条件评分与无条件评分的差异随时间指数衰减；因此，在逆向生成过程中，引导强度应从高噪声阶段（早期）向清晰阶段（晚期）逐渐降低，从而更有效地结合条件信息。
claims:
- 定理1和定理2严格证明了VP-SDE和VE-SDE下条件评分与无条件评分的均方误差上界随时间衰减（式8、11）。
- 图1通过实验验证了评分MSE随前向时间指数增长（后向时间则指数下降）以及余弦相似度逐渐降低，与理论一致。
- 在Class-Conditional ImageNet 256×256上，C2FG在DiT-XL/2上FID从2.29降至2.07，在SiT-XL/2 (REPA)上从1.80降至1.51（表1）。
- C2FG是训练无关（training-free）的即插即用方法，可无缝集成到多种扩散框架（SD、EDM2、U-ViT、DiT、SiT）中，且不增加额外的模型评估开销。
---

# C^2FG: Control Classifier-Free Guidance via Score Discrepancy Analysis

> [!tip] 核心洞察
> 在扩散模型的前向过程中，条件评分与无条件评分的差异随时间指数衰减；因此，在逆向生成过程中，引导强度应从高噪声阶段（早期）向清晰阶段（晚期）逐渐降低，从而更有效地结合条件信息。

| 字段 | 内容 |
|------|------|
| 中文题名 | C^2FG：基于评分差异的控制式无分类器引导 |
| 英文题名 | C^2FG: Control Classifier-Free Guidance via Score Discrepancy Analysis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Gao_C2FG_Control_Classifier-Free_Guidance_via_Score_Discrepancy_Analysis_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Control Classifier-Free Guidance (C²FG) |
| Dataset | Class-Conditional ImageNet 256×256, Class-Conditional ImageNet 256×256 (SiT-XL/2 (REPA), 250 steps), MS-COCO, ImageNet-64 |

> [!tip] 效果简介
> - Class-Conditional ImageNet 256×256 (DiT-XL/2, 250 steps) 上，FID 2.07 vs 2.29 (0.22)。
> - Class-Conditional ImageNet 256×256 (SiT-XL/2 (REPA), 250 steps) 上，FID 1.51 vs 1.80 (0.29)。
> - MS-COCO (U-ViT, latent space) 上，FID 5.28 vs 5.37 (0.09)。

## 概要

扩散模型中的**无分类器引导（Classifier-Free Guidance, CFG）** 是提升条件生成质量的核心技术，但其传统实现依赖固定的引导权重，忽略了扩散过程的内在动态特性。本文揭示了这一问题的根本瓶颈：**条件分布与无条件分布之间的评分差异（score discrepancy）在扩散前向过程中随时间呈指数级衰减**，而固定权重策略未能匹配这一衰减趋势，导致早期引导过强或后期引导不足，限制了生成质量。

针对上述问题，本文提出 **C²FG（Control Classifier-Free Guidance）**，一种基于评分差异分析的训练无关、即插即用方法。其核心机制是将固定的引导权重替换为**时间依赖的指数衰减控制函数** ω(t) = ω₀ exp(λ (1 − t/t_max))，使引导强度从高噪声阶段向清晰阶段逐步降低，从而更有效地结合条件信息。

理论层面，本文通过定理严格证明了 VP-SDE 和 VE-SDE 下条件与无条件评分均方误差的上界随时间衰减，并通过实验验证了该衰减趋势在实践中的一致性。方法层面，C²FG 无需额外训练，可无缝集成到多种扩散框架（如 DiT、SiT、U-ViT、EDM2）中，且不增加模型评估开销。

实验结果表明，C²FG 在多个基准上取得一致且显著的改进：在 Class-Conditional ImageNet 256×256 上，DiT-XL/2 的 FID 从 2.29 降至 2.07，SiT-XL/2 (REPA) 的 FID 从 1.80 降至 1.51；在 MS-COCO 和 ImageNet-64 上同样获得提升。消融研究进一步验证了该方法对采样器类型和推理步数的鲁棒性，在低步数场景下优势更为突出。

扩散模型已成为视觉生成的主流范式，其核心在于学习逆转一个逐步加噪的前向过程。给定数据分布 $p(x_0)$，前向过程由一个随机微分方程（SDE）描述：

$$\mathrm{d}x_t = f(x_t, t)\mathrm{d}t + g(t)\mathrm{d}w_t$$

其中 $f$ 为漂移项，$g$ 为扩散项，$w_t$ 为标准维纳过程。生成过程则通过求解逆向SDE实现，其关键组件是评分函数 $\nabla_{x_t} \log p(x_t, t)$，通常由一个去噪网络 $\epsilon_\theta$ 来近似。

在条件生成场景中，目标是从条件分布 $p(x|y)$ 中采样。**无分类器引导（Classifier-Free Guidance, CFG）**（Ho, NeurIPS 2022）通过贝叶斯定理推导出一种简洁的机制，在推理时对条件预测与无条件预测进行线性插值：

$$\hat{\epsilon}(x_t, t, y) = \omega \left[\epsilon_\theta(x_t, t, y) - \epsilon_\theta(x_t, t, \varnothing)\right] + \epsilon_\theta(x_t, t, \varnothing)$$

其中 $\omega$ 是一个固定的标量引导权重。当 $\omega > 1$ 时，条件信号被放大，生成样本的保真度与条件对齐度得以提升。

### 固定引导权重的根本缺陷

尽管CFG在实践中广泛有效，但其使用固定 $\omega$ 的策略存在一个被长期忽视的瓶颈：**它完全忽略了扩散过程的内在动态特性**。具体而言，随着前向过程推进（噪声水平升高），条件分布与无条件分布之间的评分差异（score discrepancy）并非恒定，而是随时间呈指数级衰减。这意味着，在逆向生成的早期（高噪声阶段），条件信号与无条件信号的差异本身就很小；而到了后期（低噪声阶段），两者的差异才逐渐显现。

固定权重策略无法匹配这一衰减趋势：在早期，过大的 $\omega$ 会过度放大微弱的评分差异，导致生成轨迹偏离合理路径；在后期，固定的 $\omega$ 又可能不足以充分利用已经显著分化的条件信息。这从根本上限制了生成质量的上限。

### 现有动态策略的不足

一些近期工作尝试引入动态引导策略来缓解上述问题。**区间引导（Interval Guidance）**（Kynkäänniemi et al., NeurIPS 2024）采用分段常数调度，在选定区间 $[t_l, t_h]$ 内使用固定 $\omega_0 > 1$，区间外恢复为1。**β-CFG**（Malarz et al., arXiv 2025）则引入了时间依赖的引导形式。然而，这些方法的设计缺乏对评分差异衰减规律的理论洞察，其调度函数的选择更多依赖启发式经验，未能从根本上揭示“何时引导、引导多强”的最优原则。

### C²FG的动机与核心洞察

本文的核心洞察在于：**条件评分与无条件评分的差异在扩散前向过程中随时间指数衰减，因此逆向生成过程中的引导强度应从高噪声阶段向清晰阶段逐步降低**。这一洞察得到了严格的理论支撑——定理1和定理2分别证明了在VP-SDE与VE-SDE框架下，评分均方误差的上界随时间递减（见公式8和公式11），且重参数化后的VP-SDE界大致呈 $O(e^{-t})$ 衰减（公式9）。实验验证（图1）进一步确认了评分MSE随前向时间指数增长、余弦相似度随逆向时间逐渐降低的规律。

基于此，本文提出**控制式无分类器引导（Control Classifier-Free Guidance, C²FG）**，一种训练无关、即插即用的方法。C²FG用一个时间依赖的指数衰减控制函数 $\omega(t) = \omega_0 \exp(\lambda (1 - t/t_{\max}))$ 替代固定权重，使引导强度自适应地匹配评分差异的衰减趋势，从而在理论保证下更有效地融合条件信息。

## 核心方法与创新机理

C²FG 的核心创新在于将标准无分类器引导（CFG）中的**固定引导权重 ω** 替换为一个**时间依赖的指数衰减控制函数 ω(t)**，使引导强度与扩散过程的内在动态特性相匹配。

### 问题根源：评分差异的指数衰减

CFG 的生成过程依赖于条件评分与无条件评分之间的差异来注入条件信息。标准 CFG 使用固定的引导权重 ω 对这一差异进行线性缩放：

$$\hat { \epsilon } ( x _ { t } , t , y ) = \omega \left[ \epsilon _ { \theta } ( x _ { t } , t , y ) - \epsilon _ { \theta } ( x _ { t } , t , \mathcal { D } ) \right] + \epsilon _ { \theta } ( x _ { t } , t , \mathcal { D } )$$

然而，C²FG 通过严格的理论分析揭示了这一设计的根本缺陷：**条件评分与无条件评分之间的均方误差（MSE）随扩散时间呈指数级衰减**。具体而言，在 VP-SDE 框架下，评分差异的上界为：

$$\| \nabla \log p ( x , t ) - \nabla \log \tilde { p } ( x , t ) \| \leq \frac { \alpha ( t ) } { \sigma ^ { 2 } ( t ) } C$$

经重参数化后，该上界进一步简化为 $\mathcal{O}(e^{-t})$ 的指数衰减形式。VE-SDE 框架下的理论分析得出了类似结论。这意味着：在逆向生成过程的早期（高噪声阶段），条件与无条件评分差异显著，条件信息丰富；而在晚期（清晰阶段），评分差异趋于消失，条件信号几乎枯竭。

固定权重 ω 完全忽略了这一动态特性——早期可能引导过强导致失真，晚期则引导不足无法充分利用剩余条件信息。

### 解决方案：指数衰减引导调度

C²FG 提出将引导权重设计为与评分差异衰减规律对齐的时变函数：

$$\omega ( t ) = \omega _ { 0 } \exp { \Big ( \lambda \Big ( 1 - \frac { t } { t _ { \operatorname* { m a x } } } \Big ) \Big ) }$$

其中 $\omega_0$ 为初始引导强度，$\lambda$ 控制衰减速率，$t_{\max}$ 为总扩散步数。该函数在生成早期（$t \approx 0$）取最大值 $\omega_0 e^\lambda$，随 $t$ 增大指数衰减至 $\omega_0$，精确匹配了评分差异的衰减趋势。

将此动态权重代入噪声预测更新式，得到 C²FG 的核心生成规则：

$$\hat { \epsilon } _ { c } ^ { \omega } ( x _ { t } ) = \hat { \epsilon } _ { \mathcal { Q } } ( x _ { t } ) + \omega ( t ) \big [ \hat { \epsilon } _ { c } ( x _ { t } ) - \hat { \epsilon } _ { \mathcal { Q } } ( x _ { t } ) \big ]$$

### 与基线方法的本质差异

| 方法 | 引导权重策略 | 核心机制 |
|------|-------------|---------|
| **CFG** (Ho, NeurIPS 2022) | 固定标量 ω | 全程等强度引导 |
| **Interval Guidance** (Kynkäänniemi et al., NeurIPS 2024) | 分段常数 ω(t) | 仅在选定区间内激活引导 |
| **β-CFG** (Malarz et al., arXiv 2025) | 时变但非指数衰减 | 启发式时间依赖 |
| **C²FG** (本文) | 指数衰减 ω(t) | 理论上界驱动的自适应衰减 |

C²FG 的关键优势在于：其衰减函数形式直接源自评分差异的理论上界分析，而非经验调参。这使得方法具有**训练无关（training-free）**和**即插即用（plug-in）**的特性——无需修改网络结构或重新训练，仅需在推理时替换引导调度即可集成到任意扩散框架中，且不增加额外的模型评估开销。

### 理论支撑的实证验证

图 1 的实验结果直接验证了理论分析的可靠性：(a) 条件与无条件评分的 MSE 随前向时间 $t \to +\infty$ 趋近于零，与理论上界一致；(b) 两者的归一化余弦相似度在逆向过程中持续下降，表明评分方向逐渐分化，进一步佐证了晚期引导需求降低的合理性。

C²FG 的整体 pipeline 建立在标准扩散模型采样流程之上，仅对推理阶段的引导权重调度进行改造，完全保持训练无关（training‑free）和即插即用（plug‑in）的特性。其核心模块关系与数据流如下。

**1. 去噪网络（Denoising Network）**  
给定当前噪声样本 $x_t$ 和时间步 $t$，去噪网络 $\epsilon_\theta$ 同时接收条件输入 $c$（如类别标签、文本嵌入）和无条件输入 $\varnothing$，分别输出条件噪声预测 $\hat{\epsilon}_c(x_t)$ 和无条件噪声预测 $\hat{\epsilon}_{\varnothing}(x_t)$。该模块在 C²FG 中不做任何修改，直接复用预训练模型。

**2. 引导插值模块（Guidance Interpolation）**  
这是 C²FG 的核心创新点。与标准 CFG 使用固定标量权重 $\omega$ 进行线性插值不同，C²FG 引入时间依赖的控制函数 $\omega(t)$：

$$\hat{\epsilon}_c^{\omega}(x_t) = \hat{\epsilon}_{\varnothing}(x_t) + \omega(t)\big[\hat{\epsilon}_c(x_t) - \hat{\epsilon}_{\varnothing}(x_t)\big]$$

其中 $\omega(t)$ 采用指数衰减调度：

$$\omega(t) = \omega_0 \exp\Big(\lambda\Big(1 - \frac{t}{t_{\max}}\Big)\Big)$$

该设计的理论依据来自对扩散过程评分差异（score discrepancy）的分析：定理 1 和定理 2 分别证明了 VP‑SDE 和 VE‑SDE 下条件评分与无条件评分的均方误差上界随时间呈指数衰减（式 8、式 11），图 1 进一步从实验上验证了 MSE 随前向时间指数增长、余弦相似度逐渐降低的规律。因此，在逆向生成过程中，引导强度应从高噪声阶段（早期）向清晰阶段（晚期）逐渐减弱，以匹配评分差异的内在衰减趋势。

**3. 采样调度器（Sampling Scheduler）**  
将引导后的噪声估计 $\hat{\epsilon}_c^{\omega}(x_t)$ 代入逆向 SDE 或 ODE，逐步去噪生成最终样本。该模块同样保持原样，C²FG 仅改变输入其中的噪声预测值。

**4. 与区间引导的协同**  
C²FG 可进一步与区间引导（Interval Guidance，Kynkäänniemi et al., NeurIPS 2024）结合。区间引导在生成早期和末期将 $\omega(t)$ 固定为 1，仅在中间区间施加引导；C²FG 则在整个时间轴上提供指数衰减的动态权重。两者叠加可在减少模型评估开销的同时保持或提升生成质量。

**输入输出流总结**  
- **输入**：噪声样本 $x_T$（或 latent 表示）、条件信息 $c$  
- **每个时间步**：网络前传两次（条件 + 无条件）→ 引导插值（动态 $\omega(t)$）→ 采样器更新 $x_{t-1}$  
- **输出**：条件生成样本 $x_0$

整个流程不引入额外模型评估，计算开销与标准 CFG 完全一致。

![[assets/figures/papers/paper_list_l29_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_C2FG_Control_Class/figures/003_Figure_2.jpg]]
*Figure 2: Noise to Image Process of*

### 3.1 评分差异的理论分析

C²FG 的核心洞察源于对扩散过程前向动态的严格数学分析：**条件评分与无条件评分之间的差异（score discrepancy）随时间呈指数衰减**。这一发现为设计时间依赖的引导策略提供了理论根基。

论文将前向扩散过程统一建模为 Ornstein–Uhlenbeck (OU) 过程：

$$\mathrm{d} x_t = f(t) x_t \mathrm{d}t + g(t) \mathrm{d} w_t$$

针对两种主流 SDE 参数化，分别给出了评分均方误差（MSE）的严格上界。

**VP-SDE 场景**（Theorem 1）：取 $f(t) = -\frac{1}{2}\beta_t$，$g(t) = \sqrt{\beta_t}$，条件与无条件评分函数的 MSE 满足：

$$\| \nabla \log p(x, t) - \nabla \log \tilde{p}(x, t) \| \leq \frac{\alpha(t)}{\sigma^2(t)} C$$

其中 $\alpha(t)$ 和 $\sigma(t)$ 分别为信号系数和噪声标准差，$C$ 为与时间无关的常数。经重参数化 $t' = -\log \alpha(t)$ 后，该上界可进一步简化为：

$$\| \nabla \log p(x, t) - \nabla \log p(x, t \mid y) \| \leq \frac{e^{-t'}}{1 - e^{-2t'}} C \sim \mathcal{O}(e^{-t'})$$

**VE-SDE 场景**（Theorem 2）：取 $f(t) = 0$，$g(t) = \sqrt{\frac{\mathrm{d}\sigma^2(t)}{\mathrm{d}t}}$，评分 MSE 上界为：

$$\| \nabla \log p(x, t) - \nabla \log \tilde{p}(x, t) \| \leq \frac{C}{\sigma^2(t)}$$

该上界同样随 $t \to +\infty$（即噪声增大）而趋于零。

为支撑上述理论，论文进一步引入了 **Harnack 型不等式**（Theorem 3 和 Theorem 4），分别给出了 VP-SDE 和 VE-SDE 下概率密度函数在不同时刻之间的指数型控制关系。这些不等式保证了在早期（低噪声阶段）密度估计的困难性，从偏微分方程角度解释了评分差异的衰减机制。

**实验验证**：图 1 在真实扩散模型上验证了理论预测——条件与无条件评分的 MSE 随前向时间指数增长（即逆向生成时指数衰减），同时归一化余弦相似度随逆向时间逐步降低，表明两者方向在生成后期逐渐分叉。

### 3.2 C²FG 引导调度设计

基于上述理论分析，论文提出将标准 CFG 中的固定引导权重 $\omega$ 替换为时间依赖的控制函数 $\omega(t)$，使其与评分差异的指数衰减规律对齐：

$$\omega(t) = \omega_0 \exp\left(\lambda \left(1 - \frac{t}{t_{\max}}\right)\right)$$

其中：
- $\omega_0$：初始引导强度，控制生成初期的条件对齐程度；
- $\lambda$：衰减速率，调节引导强度随时间的下降速度；
- $t_{\max}$：扩散过程的最大时间步；
- $t$ 从 $t_{\max}$（纯噪声）递减至 $0$（清晰图像）。

将该动态权重嵌入 CFG 的噪声预测更新式，得到 C²FG 的核心生成规则：

$$\hat{\epsilon}_c^\omega(x_t) = \hat{\epsilon}_\emptyset(x_t) + \omega(t) \left[\hat{\epsilon}_c(x_t) - \hat{\epsilon}_\emptyset(x_t)\right]$$

其中 $\hat{\epsilon}_c(x_t)$ 和 $\hat{\epsilon}_\emptyset(x_t)$ 分别为条件和无条件噪声预测。该更新式随后被代入逆向 SDE/ODE 采样器完成逐步去噪。

**设计直觉**：在高噪声的生成早期（$t$ 接近 $t_{\max}$），条件与无条件评分差异较大，需要较强的引导以注入条件信息；随着去噪进行（$t \to 0$），评分差异指数衰减，过强的引导反而会引入偏差，因此 $\omega(t)$ 应同步衰减。指数衰减形式直接匹配了理论推导中 $\mathcal{O}(e^{-t})$ 的评分差异趋势。

### 3.3 与现有动态引导策略的关系

C²FG 可与 **Interval Guidance**（Kynkäänniemi et al., NeurIPS 2024）无缝结合。Interval Guidance 采用分段常数调度——在选定区间 $[t_l, t_h]$ 内使用固定 $\omega_0 > 1$，区间外回退至 $\omega = 1$。C²FG 在其基础上将区间内的固定权重替换为指数衰减函数，进一步精细化引导强度的时变特性。实验表明，这种组合可在减少模型评估开销的同时保持或提升生成质量。

## 实验与关键发现

### 核心瓶颈与设计动机

扩散模型的条件生成中，固定的或无启发式的动态引导权重忽略了评分函数的内在动态特性。本文的理论分析揭示了一个关键瓶颈：在扩散前向过程中，条件分布与无条件分布之间的评分差异（score discrepancy）随时间呈指数级衰减。具体而言，在VP-SDE参数化下，该差异的上界为 $\frac{e^{-t}}{1-e^{-2t}}C \sim \mathcal{O}(e^{-t})$；在VE-SDE下，上界为 $\frac{C}{\sigma^2(t)}$。这意味着在逆向生成过程的早期（高噪声阶段），条件信息与无条件信息的评分差异较大，此时需要较强的引导信号；而随着去噪进行，评分差异迅速缩小，强引导不再必要，甚至可能引入偏差。固定权重策略未能匹配这一衰减趋势，导致早期引导过强或后期引导不足，从而限制了生成质量。

基于此洞察，**C²FG** 提出将引导强度建模为扩散时间 $t$ 的函数：

$$\omega(t) = \omega_0 \exp\left(\lambda\left(1 - \frac{t}{t_{\max}}\right)\right)$$

该指数衰减控制函数在生成早期赋予较大的引导权重，随时间逐步衰减，从而更有效地结合条件信息。更新后的噪声预测规则为：

$$\hat{\epsilon}_c^{\omega}(x_t) = \hat{\epsilon}_{\emptyset}(x_t) + \omega(t) \left[\hat{\epsilon}_c(x_t) - \hat{\epsilon}_{\emptyset}(x_t)\right]$$

C²FG 是训练无关（training-free）的即插即用方法，无需额外训练或增加模型评估开销，可无缝集成到多种扩散框架中。

### 主要结果

**Class-Conditional ImageNet 256×256 基准。** 在 DiT-XL/2 和 SiT-XL/2 架构上，C²FG 均取得了显著且一致的性能提升（Table 1）。在 DiT-XL/2 上，FID 从 2.29 降至 2.07（提升 0.22）；在 SiT-XL/2 (REPA) 上，FID 从 1.80 降至 1.51（提升 0.29），同时 IS 分数也有明显增益。这表明 C²FG 的时间依赖引导策略在不同架构上均能有效改善生成质量。

**跨数据集与跨空间泛化。** 在 MS-COCO 文本到图像生成任务（U-ViT，潜空间）上，C²FG 将 FID 从 5.37 降至 5.28，CLIP-Score 从 31.8 提升至 31.9（Table 2）。在 ImageNet-64 像素空间（EDM2-S with autoguidance）上，FID 从 1.04 微降至 1.03。这些结果表明 C²FG 在文本条件生成和像素空间生成场景下同样有效，但像素空间上的增益相对有限，可能与 autoguidance 本身已经部分实现了类似的时间依赖机制有关。

**与区间引导的协同。** C²FG 可与区间引导策略（Interval Guidance，Kynkäänniemi et al., NeurIPS 2024）协同使用——在生成的首尾阶段固定 $\omega(t)=1$，仅在中间区间应用指数衰减引导。这一组合进一步减少了模型评估开销，同时保持或提升了性能。

### 消融分析

**采样器鲁棒性。** 在 SiT-XL/2 (REPA) 上分别使用 SDE 和 ODE 采样器进行消融（Table 3），C²FG 在两种采样器下均能提升 FID，表明该方法对采样器类型具有鲁棒性。

**推理步数影响。** 当推理步数从 250 步减少至 20 步时，C²FG 的优势更为显著。这是因为在少步数采样中，每一步的去噪幅度更大，时间依赖的引导权重能够更精确地匹配评分差异的动态变化，避免固定权重在粗粒度步骤中引入的偏差。

**超参数鲁棒性。** C²FG 对控制函数超参数 $\lambda$ 和 $\omega_0$ 具有较好的鲁棒性，无需复杂调参即可取得一致改进。文中在多个设置下验证了这一点，但具体的灵敏度曲线和最优参数搜索范围需要在论文中进一步确认。

### 定性分析

在二维分布玩具示例（Figure 3）中，C²FG 生成的样本更贴合目标分布，产生的离群点显著少于 EDM2（$\omega=1$）和 β-CFG（$\alpha=\beta=2, \omega=1$）。在 Class-Conditional ImageNet 的定性比较（Figure 4）中，C²FG 生成的样本在细节保真度和类别一致性上均表现出视觉上的改善。

![[assets/figures/papers/paper_list_l29_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_C2FG_Control_Class/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative Comparison. Qualitative comparison on Class-Conditional ImageNet datasets with different architectures and samplers. The sampler used and the number of inference steps are indicated in parentheses*

![[assets/figures/papers/paper_list_l29_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_C2FG_Control_Class/figures/004_Figure_3.jpg]]
*Figure 3: A two-dimensional distribution featuring two classes represented by gray and orange regions. Approximately 99% of the probability mass is inside the shown contours. (a) Ground truth samples from the orange class. (b) EDM2*

### 局限性与失败模式

1. **理论边界的奇异性。** 理论导出的评分差异上界在 $t \to 0$ 时趋于无穷，实际实现中使用了替代函数并忽略早期阶段，存在近似误差。这意味着在生成的最末期，C²FG 的引导强度可能偏离理论最优。

2. **继承 CFG 的局限性。** 作为 CFG 的插件，C²FG 继承了 CFG 本身的局限，包括依赖无条件和条件模型的联合训练，以及引导强度过大时可能导致的样本多样性下降。

3. **超参数仍需手动调节。** 尽管文中声称 $\lambda$ 和 $\omega_0$ 具有鲁棒性，但不同任务和架构下的最优值仍需要实验搜索，缺乏自适应的确定机制。

4. **像素空间增益有限。** 在 ImageNet-64 EDM2-S 上，C²FG 仅带来 0.01 的 FID 改善，表明当基线已经使用了 autoguidance 等高级引导技术时，C²FG 的边际增益可能受限。

![[assets/figures/papers/paper_list_l29_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_C2FG_Control_Class/figures/005_Table_1.jpg]]
*Table 1: Quantitative Comparison. Comparison of different evaluation metrics on Class-Conditional ImageNet datasets with different diffusion architectures and inference steps*

![[assets/figures/papers/paper_list_l29_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_C2FG_Control_Class/figures/006_Table_2.jpg]]
*Table 2: Evaluation of*

![[assets/figures/papers/paper_list_l29_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_C2FG_Control_Class/figures/008_Table_3.jpg]]
*Table 3: Ablation Comparison. Comparison of different evaluation metrics on Class-Conditional ImageNet datasets with different architectures and fewer timesteps*

## 定位与知识库关联

**C²FG** 的核心贡献在于为无分类器引导（Classifier-Free Guidance, CFG）提供了一个理论驱动的时变引导调度方案，而非重新设计扩散模型架构或训练范式。其方法定位可从以下几个维度展开：

### 与 CFG 及其变体的关系

**C²FG** 直接继承自 **CFG**（Ho & Salimans, NeurIPS 2022）的引导框架，即通过条件与无条件评分函数的线性插值来增强条件控制：

$$\hat { \epsilon } ( x _ { t } , t , y ) = \omega \left[ \epsilon _ { \theta } ( x _ { t } , t , y ) - \epsilon _ { \theta } ( x _ { t } , t , \mathcal { D } ) \right] + \epsilon _ { \theta } ( x _ { t } , t , \mathcal { D } )$$

CFG 使用固定标量 $\omega$，而 **C²FG** 将其替换为时间依赖的指数衰减函数 $\omega(t) = \omega_0 \exp(\lambda (1 - t/t_{\max}))$。这一替换的动机并非经验调参，而是基于对扩散过程内在动态特性的严格理论分析：条件评分与无条件评分的差异在正向时间中呈指数级衰减，因此在逆向生成过程中，引导强度应从高噪声阶段向清晰阶段逐步降低。

与 **C²FG** 形成直接对比的动态引导方法包括：

- **Interval Guidance**（Kynkäänniemi et al., NeurIPS 2024）：采用分段常数引导调度，在选定区间 $[t_l, t_h]$ 内使用固定 $\omega_0 > 1$，区间外恢复为 1。该方法的核心思想是仅在特定噪声水平施加引导，但缺乏对引导强度应如何连续变化的理论解释。**C²FG** 可与 Interval Guidance 结合使用，在区间内进一步施加指数衰减调度，从而在减少模型评估开销的同时保持或提升性能。

- **β-CFG**（Malarz et al., arXiv 2025）：同样探索时变引导权重，但其调度形式缺乏严格的理论推导。在二维分布玩具实验中（Figure 3），β-CFG 产生了更多离群样本，而 **C²FG** 更好地匹配了目标分布，表明指数衰减调度在理论上更为合理。

### 理论根基与知识来源

**C²FG** 的理论分析建立在扩散模型的随机微分方程（SDE）框架之上，核心定理包括：

1. **VP-SDE 评分误差界**（Theorem 1）：$\| \nabla \log p(x,t) - \nabla \log \tilde{p}(x,t) \| \leq \frac{\alpha(t)}{\sigma^2(t)} C$，表明条件与无条件评分的均方误差上界随时间递减。

2. **VE-SDE 评分误差界**（Theorem 2）：$\| \nabla \log p(x,t) - \nabla \log \tilde{p}(x,t) \| \leq \frac{C}{\sigma^2(t)}$，给出类似结论。

3. **Harnack 型不等式**（Theorem 3, 4）：为 VP-SDE 和 VE-SDE 分别建立了不同时间点概率密度的上界关系，进一步支撑了评分差异衰减的理论基础。

重参数化后，VP-SDE 的评分误差界可写为 $\frac{e^{-t}}{1-e^{-2t}} \cdot C \sim \mathcal{O}(e^{-t})$，直接揭示了指数衰减规律。Figure 1 通过实验验证了这一理论预测：评分 MSE 随正向时间指数增长（逆向时间则指数下降），同时归一化余弦相似度在逆向过程中逐渐降低，表明条件与无条件评分的方向差异在后期更加显著。

### 适用边界与技术约束

**C²FG** 作为训练无关（training-free）的即插即用方法，理论上可无缝集成到任何使用 CFG 的扩散框架中。论文验证的兼容架构包括 **DiT**、**SiT**、**U-ViT**、**EDM2** 和 **Stable Diffusion**，覆盖了像素空间和潜在空间的生成任务。

然而，其适用边界受以下因素制约：

- **理论奇异性**：评分误差界在 $t \to 0$ 时出现奇点（分母 $\sigma^2(t) \to 0$），实际实现中需使用替代函数并忽略早期阶段，引入近似误差。
- **CFG 继承局限**：**C²FG** 作为 CFG 的插件，继承了 CFG 本身的局限性，特别是依赖条件模型和无条件模型的联合训练。在无法获取无条件模型的场景（如某些预训练模型仅提供条件输出）中，该方法无法直接应用。
- **超参数敏感性**：尽管论文声称 $\lambda$ 和 $\omega_0$ 具有鲁棒性，但不同架构和数据集下的最优值仍需实验搜索，缺乏自动确定机制。

### 局限性与开放问题

**已识别的局限**：

1. **理论-实践差距**：Harnack 型不等式提示早期时间（高噪声阶段）的密度估计存在困难，当前实现通过忽略早期阶段来规避，但这可能损失部分引导效益。
2. **调度函数形式固定**：指数衰减形式虽由理论导出，但并非唯一可能的最优解。是否存在更优的函数族（如学习得到的调度器）仍是开放问题。
3. **与自引导的深度结合**：**C²FG** 在 EDM2 的自引导（autoguidance）框架上仅取得边际改进（FID 从 1.04 降至 1.03），表明其与更先进引导技术的协同效应尚未充分挖掘。

**开放问题**：

- 能否通过学习或更严格的理论推导，自适应地确定最优的 $\omega(t)$ 函数形式？
- Harnack 型不等式提示的早期时间密度估计困难是否可通过改进网络训练或正则化缓解？
- **C²FG** 与其他先进引导技术的更深入组合方式及其极限性能如何？

## 原文 PDF

![[paperPDFs/CVPR_2026/C_2FG_Control_Classifier_Free_Guidance_via_Score_Discrepancy_Analysis.pdf]]
