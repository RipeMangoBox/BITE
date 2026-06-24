---
title: "From Sketch to Fresco: Efficient Diffusion Transformer with Progressive Resolution"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/From_Sketch_to_Fresco_Efficient_Diffusion_Transformer_with_Progressive_Resolution.pdf
project_link: null
code_link: null
aliases:
- FSFEDTPR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 统一噪声场（为每个令牌分配固定坐标噪声）与基于令牌时间方差的渐进式上采样策略。
primary_logic: 通过在低分辨率下快速建立全局结构，并仅对语义稳定的区域分配高分辨率计算资源，可以在保持生成质量的同时大幅降低计算量；统一噪声场保证了跨阶段轨迹的连续性。
claims:
- Fresco在FLUX.1-dev上以30 NFE计算，相比原始50 NFE实现2.81倍加速，同时ImageReward提升8.13%。
- 统一重噪声在理论上严格优于独立阶段重噪声，轨迹偏离的期望平方误差更小，且有不可约下界。
- 消融实验中，基于方差的令牌选择策略在随机、边缘、注意力等策略中取得了最好的速度-质量平衡。
- FLUX.1-dev (text-to-image) 上 ImageReward = 1.0527
---

# From Sketch to Fresco: Efficient Diffusion Transformer with Progressive Resolution

> [!tip] 核心洞察
> 通过在低分辨率下快速建立全局结构，并仅对语义稳定的区域分配高分辨率计算资源，可以在保持生成质量的同时大幅降低计算量；统一噪声场保证了跨阶段轨迹的连续性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 从草图到壁画：基于渐进分辨率的高效扩散Transformer |
| 英文题名 | From Sketch to Fresco: Efficient Diffusion Transformer with Progressive Resolution |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.07462) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Fresco |
| Dataset | FLUX.1-dev, HunyuanVideo, FLUX.1-schnell |

> [!tip] 效果简介
> - FLUX.1-dev (text-to-image) 上，ImageReward 1.0527 vs 0.9736 (+8.13%)。
> - HunyuanVideo (text-to-video) 上，Total Score 81.10 vs 80.12 (+1.22%)。
> - FLUX.1-schnell (distilled) 上，Speedup 22.10× vs 1.00× (+22.10×)。

## 概述

扩散Transformer（DiT）已成为高分辨率图像与视频生成的主流架构，但其推理计算开销巨大。现有加速方法中，动态分辨率采样通过先在低分辨率下生成结构再上采样细化来降低计算量，但存在一个关键瓶颈：**每次分辨率切换时独立注入新噪声，破坏了跨阶段的语义一致性，导致去噪轨迹重置并引入伪影**。同时，不加区分地一次性上采样整个潜在空间，忽略了不同令牌的收敛状态差异，在未收敛区域过早分配高分辨率计算资源会放大误差。

针对上述问题，本文提出**Fresco**——一种无需训练的由粗到精采样框架。其核心思想是：**在低分辨率下快速建立全局结构，并仅对语义稳定的区域分配高分辨率计算资源**。Fresco通过两个关键机制实现这一目标：

1. **统一噪声场（Unified Noise Field）**：为每个令牌分配一个基于其空间坐标和特征索引的固定噪声向量，跨分辨率阶段共享。这保证了去噪轨迹的连续性，理论上严格优于独立阶段重噪声策略（Proposition 1 给出了轨迹偏离的期望平方误差上界）。

2. **基于令牌时间方差的渐进式上采样**：跟踪每个令牌在不同时间步的方差，将其作为语义收敛的指标。仅当令牌的方差低于阈值时，才通过Hadamard正交变换将其扩展为四个子令牌，进入高分辨率细化阶段；未收敛的令牌则继续在低分辨率下处理。

实验表明，Fresco在**FLUX.1-dev**上以30个函数评估步数（NFE）实现**2.81倍加速**，同时ImageReward提升**8.13%**；在**HunyuanVideo**上以23 NFE实现**3.51倍加速**，质量总分提升**1.22%**。Fresco可与步长蒸馏和特征缓存等方法正交叠加：与蒸馏结合可达**22倍加速**，与特征缓存结合可达**9倍训练无关加速**。消融研究证实，基于方差的令牌选择策略在随机、边缘、注意力等多种策略中取得了最佳的速度-质量平衡（4.51倍加速）。

## 背景与动机

扩散Transformer（Diffusion Transformer, DiT）已成为文本到图像与文本到视频生成的主流架构，其核心优势在于通过Transformer的自注意力机制建模全局上下文，从而生成高保真、语义一致的视觉内容。然而，DiT的推理过程需要在完整分辨率下执行数十步去噪迭代，每一步都涉及对全部令牌的Transformer前向传播，导致极高的计算开销。以**FLUX.1-dev**（Black Forest Labs, 2024）为例，生成一张1024×1024图像通常需要50个NFE（Number of Function Evaluations），在消费级GPU上耗时数十秒，严重制约了其在实际部署中的可用性。

为缓解这一瓶颈，研究者提出了两类主流的免训练加速策略。第一类是**特征缓存**方法，如**TaylorSeer**（Liu et al., 2025），通过缓存相邻时间步的Transformer中间特征来跳过部分计算，但这类方法通常以牺牲细节保真度为代价。第二类是**动态分辨率采样**方法，如**Bottleneck Sampling**（Tian et al., 2025）和**RALU**（Jeong et al., 2025），其核心思想是在低分辨率下完成大部分去噪步骤，仅在最后阶段上采样至高分辨率进行细节细化，从而大幅降低总计算量。

然而，现有动态分辨率方法存在两个根本性缺陷，构成了本工作的核心动机。

**第一个缺陷在于重噪声（re-noising）策略的独立性假设。** 如图1所示，标准采样（图1a）仅在初始时刻注入一次噪声，而传统动态分辨率方法（图1b）在每次分辨率切换时独立采样新的高斯噪声并注入潜在空间。这种做法虽看似自然，实则破坏了跨阶段的语义连续性：新注入的噪声与前一阶段已建立的全局结构完全无关，导致去噪轨迹被强制重置，引发混叠伪影和语义漂移。从理论角度看，这种独立阶段重噪声策略的轨迹偏离存在不可约下界（见Proposition 1），即无论后续如何优化，其与目标轨迹的期望平方误差始终大于统一重噪声策略。

**第二个缺陷在于上采样策略的粗粒度性。** 现有方法在分辨率切换时，不加区分地对整个潜在空间执行一次性上采样——无论某个令牌是否已经收敛到稳定语义，都被强制提升到高分辨率。这带来了双重问题：一方面，尚未收敛的令牌（对应图像中语义模糊或结构未定的区域）在高分辨率下被过早细化，导致伪影扩散；另一方面，已经收敛的令牌（对应背景、大面积纯色等区域）在低分辨率下被重复计算，浪费了本可用于关键区域的计算资源。

上述两个缺陷共同指向一个深层瓶颈：**现有方法缺乏对令牌级收敛状态的感知能力，以及跨分辨率阶段的轨迹连续性保证。** 换言之，它们将动态分辨率视为粗粒度的阶段切换问题，而非细粒度的令牌级调度问题。

Fresco的动机正是从这两个缺口切入：通过构建**统一噪声场**（Token-Encoded Unified Noise Field）来保证跨阶段轨迹的数学连续性，同时引入**基于令牌时间方差的渐进式上采样**策略，使计算资源精准聚焦于语义尚未稳定的令牌。这种设计使得Fresco能够在低分辨率下快速建立全局结构（如同绘制草图），然后仅对语义稳定的区域逐步分配高分辨率计算资源（如同细化壁画细节），从而在显著加速的同时保持甚至提升生成质量。

## 核心创新

Fresco的核心创新在于**将动态分辨率采样从“阶段性独立噪声注入”重构为“跨阶段统一的随机轨迹”**，并引入**基于令牌收敛状态的渐进式上采样**，从而在加速扩散Transformer的同时保持甚至提升生成质量。

### 问题根因：独立重噪声的轨迹断裂

现有动态分辨率方法（如 **Bottleneck Sampling**（Tian et al., 2025）和 **RALU**（Jeong et al., 2025））在每次分辨率切换时独立采样新噪声并注入潜在空间。这一操作等价于在去噪中途重置随机轨迹，导致两个关键失效模式：

1. **语义一致性破坏**：新噪声与低分辨率阶段已建立的全局结构无关，高分辨率细化被迫从“偏离的起点”重新开始，引入伪影和混叠。
2. **理论不可约下界**：Proposition 1 严格证明了独立阶段重噪声的期望平方误差存在不可约下界，而统一重噪声的轨迹偏离更小（$\mathbb{E}[\|\widehat{X}_e - X(t_e)\|^2] \leq \mathbb{E}[\|\widetilde{X}_e - X(t_e)\|^2]$）。

### 创新一：统一噪声场（Unified Noise Field）

Fresco将噪声视为令牌的**固有属性**而非阶段依赖的随机扰动。具体而言，为每个潜在令牌分配一个由其空间坐标和特征索引确定的固定高斯噪声向量：

$$\epsilon_{y,x,d} = \mathcal{N}(0,1; \mathrm{seed}=h(y,x,d))$$

在分辨率过渡时，不再独立采样新噪声，而是利用统一噪声场对潜在状态进行更新：

$$\mathbf{z}^{(s+1)} = \beta_s \mathbf{z}^{(s)} + \alpha_s \epsilon_{y,x,d}$$

这一设计保证了跨阶段随机轨迹的连续性——高分辨率细化是在低分辨率已建立的语义结构基础上进行的**自然延续**，而非重新开始。

### 创新二：基于令牌时间方差的渐进式上采样

传统方法一次性上采样整个潜在空间，忽略了不同令牌的收敛速度差异。Fresco引入**令牌时间方差**作为语义收敛的代理指标：

$$v_i = \mathrm{Var}_t(\mathbf{z}_i^{(t)})$$

方差较小的令牌表示其语义结构已趋于稳定，可以提前上采样至高分辨率进行细节细化；方差较大的令牌则继续在低分辨率下处理。这一策略将计算资源精准分配给“最需要细节”的区域，避免了在尚未收敛的令牌上浪费高分辨率计算。

上采样操作本身也经过精心设计：使用4×4 Hadamard正交变换将父令牌扩展为四个子令牌，并注入受控正交扰动以丰富细节：

$$[ \mathbf{z}_1, \mathbf{z}_2, \mathbf{z}_3, \mathbf{z}_4 ] = H_4 \cdot [ \mathbf{z}_{\mathrm{parent}}, \epsilon_1, \epsilon_2, \epsilon_3 ]$$

### 创新对比总结

| 设计维度 | 现有动态分辨率方法 | Fresco |
|---------|------------------|--------|
| 重噪声策略 | 每阶段独立采样新噪声 | 统一噪声场，跨阶段共享 |
| 上采样时机 | 一次性上采样全部令牌 | 基于令牌方差渐进上采样 |
| 上采样操作 | 标准插值（如双线性） | Hadamard正交扩展+正交扰动 |
| 轨迹连续性 | 断裂，存在不可约误差下界 | 连续，理论误差更小 |

消融实验证实了每个创新的独立贡献：基于方差的令牌选择策略在随机、边缘、注意力等策略中取得了最佳的速度-质量平衡（4.51×加速），验证了“收敛状态驱动计算分配”这一核心直觉的合理性。

## 整体框架

Fresco 的核心管线围绕两个关键机制展开：**统一噪声场**（Token‑Encoded Unified Noise Field）与**基于令牌时间方差的渐进式上采样**（Progressive Variance‑Guided Upsampling）。整个生成过程从低分辨率开始，逐步将收敛的令牌提升到高分辨率进行细化，从而在保持语义一致性的同时大幅降低计算开销。

### 管线总览

1. **低分辨率初始化**  
   采样从降低后的分辨率（如 512×512）起步。每个潜在令牌根据其空间坐标 $(y, x)$ 和特征维度索引 $d$ 通过哈希函数获得一个固定的高斯噪声向量，构成统一噪声场：
   $$\epsilon_{y,x,d} = \mathcal{N}(0,1; \mathrm{seed}=h(y,x,d))$$
   该噪声场在整个生成过程中跨阶段共享，确保随机演化轨迹的连续性。

2. **令牌时间方差估计**  
   在渐进采样过程中，系统持续追踪每个令牌在不同时间步的状态，计算其时间方差：
   $$v_i = \mathrm{Var}_t(\mathbf{z}_i^{(t)})$$
   方差小的令牌表示其语义结构已趋于稳定，方差大的令牌则仍需在低分辨率下继续去噪。

3. **阈值驱动的选择性上采样**  
   设定方差阈值 $\tau$：满足 $v_i \leq \tau$ 的令牌被视为“已收敛”，提前进行上采样。上采样操作采用 **Hadamard 正交变换**，将父令牌 $\mathbf{z}_{\mathrm{parent}}$ 与三个独立高斯扰动 $\epsilon_1, \epsilon_2, \epsilon_3$ 通过 $4\times4$ Hadamard 矩阵 $H_4$ 扩展为四个子令牌：
   $$[ \mathbf{z}_1, \mathbf{z}_2, \mathbf{z}_3, \mathbf{z}_4 ] = H_4 \cdot [ \mathbf{z}_{\mathrm{parent}}, \epsilon_1, \epsilon_2, \epsilon_3 ]$$
   该变换保证了子令牌间的正交性，在注入细节扰动的同时不破坏已建立的语义结构。

4. **高分辨率细化**  
   上采样后的令牌进入高分辨率阶段（如 1024×1024），继续执行去噪步骤以细化纹理和细节。未收敛的令牌则保持在低分辨率下处理，直到其方差降至阈值以下。

### 跨阶段噪声衔接

在分辨率切换时，传统动态分辨率方法会独立采样新噪声并注入，导致去噪轨迹重置和语义断裂。Fresco 则利用统一噪声场进行状态更新：
$$\mathbf{z}^{(s+1)} = \beta_s \mathbf{z}^{(s)} + \alpha_s \epsilon_{y,x,d}$$
其中 $\alpha_s, \beta_s$ 为与当前时间步相关的系数。该更新方式在理论上保证了轨迹偏离的期望平方误差严格小于独立阶段重噪声（Proposition 1），且后者存在不可约下界。

### 模块关系总结

| 模块 | 功能 | 输入 | 输出 |
|------|------|------|------|
| 统一噪声场初始化 | 为每个令牌分配固定坐标噪声 | 令牌坐标 $(y,x,d)$ | 噪声向量 $\epsilon_{y,x,d}$ |
| 令牌时间方差估计 | 评估令牌收敛状态 | 令牌历史状态序列 | 方差 $v_i$ |
| 阈值驱动选择性上采样 | 对收敛令牌进行 Hadamard 扩展 | 父令牌 $\mathbf{z}_{\mathrm{parent}}$ | 四个子令牌 $[\mathbf{z}_1,\mathbf{z}_2,\mathbf{z}_3,\mathbf{z}_4]$ |
| 高分辨率细化 | 对上采样后的令牌继续去噪 | 高分辨率令牌 | 最终生成图像/视频 |

该框架的核心优势在于：**低分辨率阶段快速建立全局结构，高分辨率计算资源仅分配给语义已稳定的区域**。消融实验表明，基于方差的令牌选择策略在随机、边缘、注意力等策略中取得了最佳的速度‑质量平衡，实现 4.51× 加速（Table 4）。

### 补充图表

![[assets/figures/papers/paper_list_l877_https_arxiv_org_abs_2601_07462/figures/001_Figure_1.jpg]]
*Figure 1: Overview of re-noising strategies. (a) Standard Sampling: one initial noise with no re-noise during process. (b) Traditional Dynamic Resolution: inject stage-specific noise independently at every resolution change, disrupting semantic and reset denoising trajectory, causing aliasing and artifacts. (c) Unified renoise (ours): all stages query the same noise field, ensuring stable refinement and clean results*

![[assets/figures/papers/paper_list_l877_https_arxiv_org_abs_2601_07462/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the Fresco framework. Fresco starts sampling at a reduced resolution while assigning each token a fixed coordinatebound noise vector from a unified noise field. During generation, Fresco tracks each token’s temporal variance: tokens with small variance, indicating stable semantics, are upsampled for high-resolution refinement, whereas unstable tokens remain at low resolution for further denoising. This unified-noise, variance-guided process enables smooth and efficient coarse-to-fine generation*

## 核心模块与公式推导

Fresco 框架围绕两个核心机制展开：**统一噪声场（Unified Noise Field）** 与 **基于令牌时间方差的渐进式上采样（Progressive Variance-Guided Upsampling）**。前者解决跨分辨率阶段语义一致性问题，后者实现计算资源的非均匀分配。

---

### 统一噪声场

现有动态分辨率采样方法（如 Bottleneck Sampling、RALU）在每次分辨率切换时独立注入新噪声，导致去噪轨迹重置和语义破坏。Fresco 的核心创新在于为每个潜在令牌分配一个**固定坐标噪声向量**，该向量在全部分辨率阶段共享，形成统一的随机参考场。

**定义**：对于位于空间坐标 $(y, x)$、特征维度索引为 $d$ 的令牌，其噪声向量通过哈希函数确定性地生成：

$$\epsilon_{y,x,d} = \mathcal{N}(0,1; \ \mathrm{seed}=h(y,x,d)) \tag{3}$$

其中 $h(\cdot)$ 将令牌的时空坐标映射为伪随机种子，保证同一令牌在所有阶段查询到完全相同的噪声实现。

**跨阶段状态更新**：当从阶段 $s$ 过渡到阶段 $s+1$ 时，潜在状态不重新初始化，而是利用统一噪声场进行受控更新：

$$\mathbf{z}^{(s+1)} = \beta_s \mathbf{z}^{(s)} + \alpha_s \epsilon_{y,x,d} \tag{4}$$

其中 $\alpha_s$ 和 $\beta_s$ 为与当前时间步相关的噪声调度系数。这一更新保持了去噪轨迹的连续性——令牌的语义结构在低分辨率阶段建立后，不会因分辨率切换而被重置。

**理论保证**：论文通过 Proposition 1 证明，统一重噪声的期望轨迹偏离严格小于独立阶段重噪声。具体地，令 $\widehat{X}_e$ 和 $\widetilde{X}_e$ 分别为统一和独立策略下的最终状态，则：

$$\mathbb{E}[\|\widehat{X}_e - X(t_e)\|^2] \leq \mathbb{E}[\|\widetilde{X}_e - X(t_e)\|^2] \tag{5-6}$$

且独立策略存在不可约下界，意味着其轨迹误差无法通过增加计算量来消除。

---

### 令牌时间方差与渐进式上采样

统一噪声场解决了轨迹连续性问题，但计算效率仍需提升。Fresco 的第二个关键机制是**基于收敛状态的选择性上采样**：并非所有令牌都需要高分辨率处理——语义已稳定的区域可以提前上采样并细化，而未收敛区域继续在低分辨率下完成结构构建。

**令牌时间方差**：在渐进采样过程中，Fresco 跟踪每个令牌 $\mathbf{z}_i$ 在不同时间步的状态变化，计算其时序方差作为收敛指标：

$$v_i = \mathrm{Var}_t(\mathbf{z}_i^{(t)}) \tag{7}$$

低方差表明令牌的语义结构已趋于稳定（如背景、均匀纹理区域），适合提前上采样以细化细节；高方差则表明令牌仍处于剧烈的语义构建阶段（如物体边界、复杂结构），应继续在低分辨率下处理以节省计算。

**阈值驱动的选择性上采样**：设定方差阈值 $\tau$，满足 $v_i \leq \tau$ 的令牌被视为“已收敛”，触发上采样操作；未满足条件的令牌保持当前分辨率继续去噪。这一机制使计算资源从“均匀分配”转变为“按需分配”，在保持生成质量的同时大幅降低浮点运算量。

---

### Hadamard 正交扩展

传统上采样（如双线性插值）简单地将低分辨率令牌映射到高分辨率网格，缺乏对细节的主动注入。Fresco 采用 **Hadamard 正交变换** 将父令牌扩展为四个子令牌，同时注入受控的正交扰动以丰富局部细节：

$$[ \mathbf{z}_1, \mathbf{z}_2, \mathbf{z}_3, \mathbf{z}_4 ] = H_4 \cdot [ \mathbf{z}_{\mathrm{parent}}, \epsilon_1, \epsilon_2, \epsilon_3 ] \tag{8}$$

其中 $H_4$ 为 $4 \times 4$ Hadamard 矩阵（元素为 $\pm 1$，行向量相互正交），$\epsilon_1, \epsilon_2, \epsilon_3$ 为三个独立的高斯噪声向量。Hadamard 变换保证子令牌之间保持正交性，避免引入冗余信息；同时，噪声扰动为子令牌注入差异化细节，使高分辨率细化阶段有足够的局部变化可供建模。

---

### 模块协同与流程总结

Fresco 的完整采样流程可概括为四个协同模块：

1. **统一噪声场初始化**：在采样开始时为每个令牌分配固定坐标噪声，跨阶段共享。
2. **令牌时间方差估计**：在低分辨率阶段持续跟踪每个令牌的方差，评估收敛状态。
3. **阈值驱动的选择性上采样**：收敛令牌通过 Hadamard 扩展提升分辨率，未收敛令牌保持低分辨率处理。
4. **高分辨率细化**：上采样后的令牌在高分辨率下继续去噪，完成细节生成。

这一流程使 Fresco 在无需额外训练的前提下，实现了对现有扩散 Transformer 模型（如 FLUX、HunyuanVideo）的即插即用加速。

## 实验与分析

### 核心定量结果

Fresco 在两个主流生成模型上均实现了显著的质量-速度联合提升。在 **FLUX.1-dev**（Black Forest Labs, 2024）文本生成图像任务上，Fresco 以 30 NFE 计算达到 2.81 倍加速，同时 **ImageReward** 从基线的 0.9736 提升至 1.0527（+8.13%），CLIP Score 也小幅提升 0.36%（Table 1）。在 **HunyuanVideo**（Sun et al., 2024）文本生成视频任务上，Fresco 以 23 NFE 实现 3.51 倍加速，**Total Score** 从 80.12 提升至 81.10（+1.22%），Quality Score 提升 1.47%（Table 2）。

![[assets/figures/papers/paper_list_l877_https_arxiv_org_abs_2601_07462/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison of text-to-image generation on FLUX.1-dev*

![[assets/figures/papers/paper_list_l877_https_arxiv_org_abs_2601_07462/figures/004_Table_2.jpg]]
*Table 2: Quantitative comparison of text-to-video generation on HunyuanVideo*

这一“加速且提质”的反常现象源于 Fresco 的两项设计：统一噪声场保证了跨分辨率阶段的轨迹连续性，避免了独立重噪声造成的语义破坏；渐进式上采样则将高分辨率计算集中于已收敛的令牌，使模型在有限步数内更高效地细化细节，而非在噪声主导的全局区域浪费算力。

### 与加速方法的兼容性

Fresco 与现有加速范式高度互补。当与步长蒸馏方法 **FLUX.1-schnell**（Black Forest Labs, 2024）结合时，Fresco 实现 **22.10 倍**加速（Figure 5）。与特征缓存方法 **TaylorSeer**（Liu et al., 2025）结合时，Fresco 实现 **9 倍**无训练加速。这表明 Fresco 的动态分辨率策略与蒸馏、缓存等方法作用于不同的计算瓶颈，叠加后产生接近乘性的加速效果。

![[assets/figures/papers/paper_list_l877_https_arxiv_org_abs_2601_07462/figures/010_Figure_5.jpg]]
*Figure 5: Compatibility with other acceleration methods. Fresco achieves 22× speedup when combined with step distillation and 9× training-free acceleration when paired with feature caching, while preserving high visual fidelity*

### 消融研究：令牌选择策略

令牌上采样时机的选择策略是 Fresco 性能的关键。Table 4 对比了四种策略：

![[assets/figures/papers/paper_list_l877_https_arxiv_org_abs_2601_07462/figures/008_Table_4.jpg]]
*Table 4: Ablation study on token selection methods*

- **随机选择（Random）**：无信息引导，速度提升有限且质量不稳定。
- **边缘选择（Edge）**：优先上采样边缘区域的令牌，假设边缘需要更多细节，但忽略了语义收敛状态。
- **注意力选择（Attention）**：基于注意力图选择重要令牌，计算开销较大。
- **方差选择（Variance，Fresco 默认）**：基于令牌时间方差 $v_i = \mathrm{Var}_t(\mathbf{z}_i^{(t)})$ 评估收敛状态，仅对稳定令牌提前上采样。

结果表明，方差策略取得了最佳的速度-质量平衡，实现 **4.51 倍**加速。其因果机制在于：低方差意味令牌的语义结构已基本确定，此时上采样并注入正交扰动（Hadamard 扩展）可以有效丰富细节，而不会破坏已建立的全局结构；高方差令牌继续在低分辨率下去噪，避免了在高分辨率下对未收敛噪声进行无效计算。

### 分辨率可扩展性

Table 5 展示了 Fresco 在不同分辨率下的加速效果。随着分辨率从 1024×1024 提升至 2048×2048，加速比从 4.51 倍增长至 **5.68 倍**。这一趋势符合预期：分辨率越高，低分辨率阶段节省的计算量越大，且全局结构在低分辨率下即可有效建立，高分辨率仅需处理细节细化。

![[assets/figures/papers/paper_list_l877_https_arxiv_org_abs_2601_07462/figures/009_Table_5.jpg]]
*Table 5: Acceleration on different resolutions*

### 视觉质量分析

Figure 3 和 Figure 4 分别展示了 FLUX.1-dev 和 HunyuanVideo 上的生成样本对比。与传统动态分辨率方法 **Bottleneck Sampling**（Tian et al., 2025）和 **RALU**（Jeong et al., 2025）相比，Fresco 生成的图像和视频在语义一致性和细节真实性上均表现更优。传统方法因独立重噪声导致跨阶段语义破坏，常出现伪影和纹理错位；Fresco 的统一噪声场有效抑制了这一问题，使生成结果更加干净。

![[assets/figures/papers/paper_list_l877_https_arxiv_org_abs_2601_07462/figures/005_Figure_3.jpg]]
*Figure 3: Visualization of the image generated by different methods on FLUX.1-dev. Fresco delivers the most realistic and semantically faithful results while achieving the fastest speed (4.72×), outperforming all dynamic resolution and feature caching baselines*

![[assets/figures/papers/paper_list_l877_https_arxiv_org_abs_2601_07462/figures/007_Figure_4.jpg]]
*Figure 4: Visualization of different acceleration methods on HunyuanVideo. Fresco achieves the best visual quality, semantic accuracy, and highest speedup ratio 4.92× among all methods, demonstrating strong generalization ability on video generation models*

Figure 6 进一步展示了 Fresco 在极低步数下的快速收敛能力：在仅 6 步低分辨率采样后（50→44 步），Fresco 已草拟出清晰的全局结构，而原始 FLUX.1-dev 模型在相同步数下仍被噪声主导。这验证了“低分辨率快速建立全局结构”的核心设计假设。

![[assets/figures/papers/paper_list_l877_https_arxiv_org_abs_2601_07462/figures/011_Figure_6.jpg]]
*Figure 6: Fast convergence with fewer steps. Fresco drafts the global structure within the first few low-resolution steps (50→44), while the original model remains dominated by noise*

### 关键证据强度总结

| 声明 | 证据锚点 | 置信度 |
|------|----------|--------|
| Fresco 在 FLUX.1-dev 上 2.81× 加速 + 8.13% ImageReward 提升 | Table 1 定量数据 | 0.99 |
| 统一重噪声理论上严格优于独立阶段重噪声 | Proposition 1 数学证明 | 0.98 |
| 方差策略在令牌选择消融中取得最佳平衡（4.51×） | Table 4 消融数据 | 0.95 |
| Fresco 与步长蒸馏结合达 22× 加速 | Figure 5 兼容性实验 | 0.95 |
| 加速比随分辨率提升而增长（4.51×→5.68×） | Table 5 分辨率实验 | 0.95 |

### 补充图表

![[assets/figures/papers/paper_list_l877_https_arxiv_org_abs_2601_07462/figures/006_Table_3.jpg]]
*Table 3: Quantitative comparison of text-to-image generation with other accleration methods*

## 方法谱系与知识库定位

### 1. 问题背景与现有方法瓶颈

扩散Transformer（Diffusion Transformer, DiT）在高分辨率图像与视频生成中面临巨大的计算开销，其核心瓶颈在于对所有潜在令牌（latent tokens）施加等量的去噪计算，而忽略了令牌间收敛速度的差异。现有的加速策略主要分为三类：步长蒸馏、特征缓存和动态分辨率采样。步长蒸馏（如**FLUX.1-schnell**, Black Forest Labs, 2024）通过减少总采样步数实现加速，但需要额外的训练成本且可能牺牲生成多样性。特征缓存方法（如**TaylorSeer**, Liu et al., 2025）通过复用中间特征减少计算，但缓存策略的设计高度依赖模型架构。

动态分辨率采样是近年来兴起的无训练加速范式，其核心思想是在低分辨率下完成主体结构生成，再切换至高分辨率进行细节细化。然而，现有方法（如**Bottleneck Sampling**, Tian et al., 2025；**RALU**, Jeong et al., 2025）存在两个关键缺陷：

1. **独立阶段重噪声（Independent Stage Re-noising）**：在每次分辨率切换时，独立采样新的高斯噪声并注入潜在空间。这一操作破坏了跨阶段的语义连续性，导致去噪轨迹被重置，引发混叠伪影和语义漂移。
2. **无差别上采样**：对所有令牌同时执行上采样操作，忽略了令牌的收敛状态。尚未收敛的令牌在高分辨率下被迫继续去噪，浪费计算资源；同时，简单插值上采样无法为子令牌注入足够的细节信息。

### 2. Fresco的方法定位与核心创新

Fresco针对上述瓶颈，提出了两个协同工作的核心机制，形成了一套完整的渐进式分辨率生成框架：

**统一噪声场（Token-Encoded Unified Noise Field）**：Fresco为每个潜在令牌分配一个基于其空间坐标和特征索引的固定高斯噪声向量，通过哈希函数 $\epsilon_{y,x,d} = \mathcal{N}(0,1; \mathrm{seed}=h(y,x,d))$ 确定。该噪声场在所有分辨率阶段共享，在分辨率切换时通过 $\mathbf{z}^{(s+1)} = \beta_s \mathbf{z}^{(s)} + \alpha_s \epsilon_{y,x,d}$ 更新潜在状态。理论分析（Proposition 1）证明，统一重噪声的期望轨迹偏离平方误差严格小于独立阶段重噪声，且后者存在不可约下界，从理论上保证了跨阶段语义一致性。

**基于令牌时间方差的渐进式上采样（Progressive Variance-Guided Upsampling）**：Fresco跟踪每个令牌在不同时间步的方差 $v_i = \mathrm{Var}_t(\mathbf{z}_i^{(t)})$，以此作为语义收敛的代理指标。当令牌的方差低于预设阈值 $\tau$ 时，认为其语义结构已稳定，通过Hadamard正交变换 $[ \mathbf{z}_1, \mathbf{z}_2, \mathbf{z}_3, \mathbf{z}_4 ] = H_4 \cdot [ \mathbf{z}_{\mathrm{parent}}, \epsilon_1, \epsilon_2, \epsilon_3 ]$ 将其扩展为四个子令牌，注入受控的正交扰动以丰富细节。未收敛的令牌则继续在低分辨率下去噪，避免无效计算。

### 3. 与现有方法的谱系关系

Fresco属于**无训练的动态分辨率加速方法**，与以下方法族形成互补或替代关系：

- **相对于步长蒸馏方法（如FLUX.1-schnell）**：Fresco无需额外训练，可直接应用于预训练模型。更重要的是，Fresco与步长蒸馏具有正交兼容性——实验表明，将Fresco与FLUX.1-schnell结合可实现22倍加速（Figure 5），远超单独使用任一方法的效果。
- **相对于特征缓存方法（如TaylorSeer）**：Fresco通过空间分辨率的分层处理减少计算，与特征缓存在机制上互补。论文指出Fresco与基于预测的特征缓存方法特别兼容，联合使用可实现9倍无训练加速（Figure 5）。
- **相对于传统动态分辨率方法（如Bottleneck Sampling, RALU）**：Fresco的核心改进在于统一噪声场和渐进上采样策略，解决了独立重噪声导致的语义断裂和伪影问题。Table 1和Table 2的定量对比显示，Fresco在ImageReward和CLIP Score上均显著优于这些基线，同时实现了更高的加速比。

### 4. 适用边界与局限

尽管Fresco在实验中展现了显著的加速效果和质量提升，其方法设计仍存在若干边界条件：

1. **架构依赖性**：Fresco的令牌方差估计和Hadamard扩展操作基于DiT的序列化令牌表示设计。论文未验证该方法在U-Net架构扩散模型上的适用性，U-Net的特征图不具备明确的令牌语义，方差估计的有效性需要进一步研究。
2. **方差阈值的手动调节**：令牌上采样的阈值 $\tau$ 目前需要针对不同模型和分辨率手动设定，缺乏自适应机制。这限制了Fresco在未见过的模型或极端分辨率下的开箱即用能力。
3. **极高分辨率下的效率衰减**：虽然Table 5显示加速比从1024分辨率下的4.51倍提升至2048分辨率下的5.68倍，但随着分辨率进一步升高（如4K及以上），令牌数量的急剧增加可能导致方差估计的计算开销显著增长，渐进上采样的边际收益可能递减。

### 5. 开放问题

Fresco的工作为动态分辨率生成开辟了若干值得探索的方向：

- **自适应阈值学习**：能否通过轻量级网络或元学习方法，使方差阈值 $\tau$ 根据生成内容和当前去噪进度自适应调整，消除手动调节的需求？
- **跨架构泛化**：统一噪声场和渐进上采样的思想是否可以推广到非Transformer架构（如U-Net）的扩散模型中？这需要重新定义U-Net特征图上的“令牌”概念和方差度量。
- **训练阶段的嵌入**：统一噪声场目前仅用于推理阶段的采样过程。如果将其嵌入到训练过程中，能否使模型学会利用这种跨分辨率一致性，从而进一步提升生成质量或加速训练收敛？
- **与其他加速范式的深度融合**：Fresco已初步展示了与步长蒸馏和特征缓存的兼容性，但三者的联合优化策略（如动态分配步长、缓存和分辨率）仍有待系统研究，可能催生更高效的混合加速框架。

## 原文 PDF

![[paperPDFs/CVPR_2026/From_Sketch_to_Fresco_Efficient_Diffusion_Transformer_with_Progressive_Resolution.pdf]]
