---
title: "CADS: Unleashing the Diversity of Diffusion Models through Condition-Annealed Sampling"
type: paper
paper_level: A
venue: ICLR
year: 2024
pdf_ref: paperPDFs/ICLR_2024/CADS_Unleashing_the_Diversity_of_Diffusion_Models_through_Condition_Annealed_Sampling.pdf
project_link: http://probml.github.io/book2
code_link: https://github.com/CompVis/latent-diffusion
aliases:
- CCADS
- CADS
tags:
- ICLR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 向条件向量添加随时间衰减的高斯噪声，以控制条件信号在采样过程中的强度。
primary_logic: 通过退火条件信号，可以平滑条件分布，从而在保持高图像质量的同时大幅提高生成多样性，且无需对预训练扩散模型进行重新训练。
claims:
- 在 ImageNet 256×256 类条件生成中，CADS 将 FID 从 20.83 (DDPM) 降低到 9.47
- CADS 在 ImageNet 256×256 上实现了新的最先进 FID 1.70，在 512×512 上实现了 2.31
- CADS 不需要任何模型重新训练，且可集成到任何扩散采样器中
- 在 DeepFashion 姿态到图像生成中，CADS 将 Recall 从 0.02 (DDPM) 提高到 0.48
---

# CADS: Unleashing the Diversity of Diffusion Models through Condition-Annealed Sampling

> [!tip] 核心洞察
> 通过退火条件信号，可以平滑条件分布，从而在保持高图像质量的同时大幅提高生成多样性，且无需对预训练扩散模型进行重新训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | CADS：通过条件退火采样释放扩散模型的多样性 |
| 英文题名 | CADS: Unleashing the Diversity of Diffusion Models through Condition-Annealed Sampling |
| 会议/期刊 | ICLR 2024 |
| Links | [paper](https://openreview.net/forum?id=zMoNrajk2X) · [paper](http://arxiv.org/abs/1406.2661) · [Project](http://probml.github.io/book2) · [Code](https://github.com/CompVis/latent-diffusion) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | CADS (Condition-Annealed Diffusion Sampler) |
| Dataset | DeepFashion pose-to-image, ImageNet 256×256 class-conditional, ImageNet 512×512 class-conditional |

> [!tip] 效果简介
> - DeepFashion pose-to-image 上，FID 7.73 vs 16.36 (DDPM) (-8.63)；Recall 0.48 vs 0.02 (+0.46)。
> - ImageNet 256×256 class-conditional 上，FID 9.47 vs 20.83 (DDPM) (-11.36)。
> - ImageNet 512×512 class-conditional 上，FID 9.81 vs 23.10 (DDPM) (-13.29)。

## 概要

条件扩散模型在推理时面临一个根本性的瓶颈：当使用高无分类器引导（CFG）尺度或在有限数据集上训练时，条件分布会变得异常尖锐，导致生成样本高度趋同，多样性严重不足。**CADS（Condition-Annealed Diffusion Sampler）** 针对这一问题提出了一个简洁而高效的解决方案——在采样过程中向条件向量添加随时间衰减的高斯噪声，通过“退火”条件信号的强度来平滑条件分布，从而在保持高图像质量的同时大幅释放生成多样性。

CADS 的核心优势体现在三个层面：
- **即插即用**：无需对预训练扩散模型进行任何重新训练或微调，计算开销极小（仅涉及加法操作），可无缝集成到任意扩散采样器中。
- **质量-多样性再平衡**：在多个条件生成任务上，CADS 一致地打破了传统采样器在高质量与高多样性之间的固有权衡。
- **实证效果显著**：在 ImageNet 256×256 类条件生成中，CADS 将 FID 从 DDPM 的 20.83 降至 9.47；结合 DiT-XL/2 后更达到新的最先进水平（FID 1.70 @ 256×256，2.31 @ 512×512）。在 DeepFashion 姿态到图像生成任务中，Recall 从 0.02 跃升至 0.48，提升超过 20 倍。

方法上，CADS 通过在采样循环的每一步对条件向量执行“加噪-退火-重缩放”三步操作（式 1-4），以分段线性调度函数 γ(t) 控制噪声强度的单调衰减，并通过混合因子 ψ 调节原始条件与重缩放条件之间的平衡。该方法可视为在推理阶段对条件分布进行可控平滑的一种通用策略，与 Dynamic CFG 等直接调制引导权重的方案形成互补。

需要指出的是，CADS 目前依赖手动调节场景相关的超参数（噪声尺度 s、退火阈值 τ₁/τ₂、混合因子 ψ），在更复杂的条件模态（如密集语义分割掩码）上的适用性仍有待验证。



### 扩散模型的条件生成困境

扩散模型（Diffusion Models）已成为图像生成领域的核心范式，其通过逐步去噪从高斯噪声中恢复数据分布的机制，在无条件生成和条件生成任务中均展现出卓越性能。然而，**条件扩散模型在推理阶段存在一个被长期忽视的瓶颈：多样性崩溃**。

这一问题的根源在于条件分布的尖锐性（peaked conditional distribution）。当使用无分类器引导（Classifier-Free Guidance, CFG）时，为了提升生成质量，通常需要设置较高的引导权重 $w_{\mathrm{CFG}}$。然而，高引导尺度会使条件分布过度集中于少数模式，导致模型反复生成构图相似、姿态雷同的样本——即使底层数据分布本身具有丰富的多样性。这种现象在小数据集上训练的模型中尤为严重：例如，在 DeepFashion 姿态到图像生成任务中，标准 DDPM 采样器（Ho et al., NeurIPS 2020）生成的样本几乎完全丧失多样性，Recall 指标仅为 0.02（Table 1）。

### 现有方法的局限

已有的扩散模型改进工作主要聚焦于三个方面：

1. **模型架构与训练策略优化**：如 DiT、MDT 等通过改进 Transformer 骨干网络或训练范式提升生成质量，但这些方法需要在训练阶段进行修改，无法直接应用于已部署的预训练模型。
2. **采样器设计**：DDIM（Song et al., ICLR 2021）等确定性采样器加速了生成过程，但并未解决高引导尺度下的多样性丧失问题。
3. **引导策略调整**：动态调整引导权重（Dynamic CFG）的尝试虽然能够在一定程度上缓解多样性问题，但其效果有限，且在高引导尺度下往往不如直接对条件信号本身进行干预（Table 4）。

**核心缺口在于**：现有方法缺乏一种**无需重新训练、可即插即用**的推理阶段多样性增强机制，能够在保持高图像质量的同时，有效平滑条件分布、释放生成多样性。

### 本文动机：条件退火的核心洞察

CADS（Condition-Annealed Diffusion Sampler）的提出源于一个关键洞察：**通过向条件向量添加随时间衰减的高斯噪声，可以控制条件信号在采样过程中的强度，从而平滑条件分布**。

这一思想的直觉来源是：在采样的早期阶段，噪声水平较高，模型对条件的依赖应当较弱，以允许生成过程探索更广泛的模式空间；随着采样的推进，条件信号应逐渐增强，引导生成结果向目标条件收敛。这种“退火”机制与扩散模型本身从噪声到结构的生成过程自然契合。

CADS 的核心优势在于：
- **零训练成本**：作为纯推理阶段技术，可直接集成到任意预训练扩散模型和采样器中，无需任何微调或重新训练。
- **计算开销极小**：仅涉及条件向量的加性噪声注入和重缩放操作（Algorithm 1）。
- **质量-多样性权衡的突破**：在 ImageNet 256×256 类条件生成中，CADS 将 FID 从 DDPM 的 20.83 降至 9.47（Table 1），并在 DiT-XL/2 上达到新的最先进 FID 1.70（Table 2），同时显著提升了 Recall 和 Vendi Score 等多样性指标。



## 核心方法与创新机理

CADS 的核心创新在于**将条件信号视为一个可退火的变量**，而非扩散模型推理过程中固定不变的输入。这一视角转换催生了一个极其轻量却高效的采样策略，其关键创新点可归纳为三个相互关联的“changed slots”。

### 1. 条件信号的噪声注入与退火调度

标准扩散采样器（如 **DDPM** (Ho et al., NeurIPS 2020)）在每一步都使用干净的条件向量 ${\pmb y}$。当无分类器引导（CFG）权重较高或训练数据有限时，条件分布 $p({\pmb x}|{\pmb y})$ 会变得尖锐，导致生成样本坍缩至少数模式。

CADS 的核心操作为：在采样的每一步 $t$，向条件向量注入高斯噪声，且噪声强度随时间单调递减：

$$\widehat{\pmb y} = \sqrt{\gamma(t)} \, {\pmb y} + s \sqrt{1 - \gamma(t)} \, {\pmb n}, \quad {\pmb n} \sim \mathcal{N}(0, {\pmb I})$$

其中：
- $s$ 控制噪声的总尺度；
- $\gamma(t)$ 是一个从 1 衰减到 0 的分段线性退火函数（Eq. 2），由截断阈值 $\tau_1$ 和 $\tau_2$ 参数化。

这一操作的**因果机制**是：在采样早期（$t$ 较大），$\gamma(t)$ 接近 1，噪声分量几乎为零，条件信号保持完整，确保生成过程沿正确的语义方向启动；在采样中期，$\gamma(t)$ 逐渐减小，噪声分量增大，条件信号被“模糊化”，使得采样过程能够探索条件分布中更广阔的区域；在采样末期，$\gamma(t)$ 归零，条件完全被噪声淹没，模型依赖已建立的图像结构完成生成。这种“先锚定、后探索”的策略，平滑了原本尖锐的条件分布，从而在保持条件对齐的同时大幅提升多样性。

### 2. 受污染条件的重缩放与混合

直接使用被噪声污染的条件向量可能导致数值不稳定或条件信息过度丢失。CADS 引入了两步后处理：

$${\hat{\pmb y}}_{\text{rescaled}} = \frac{{\hat{\pmb y}} - \operatorname{mean}({\hat{\pmb y}})}{\operatorname{std}({\hat{\pmb y}})} \sigma_{\text{in}} + \mu_{\text{in}}$$

$${\hat{\pmb y}}_{\text{final}} = \psi \, {\hat{\pmb y}}_{\text{rescaled}} + (1 - \psi) \, {\hat{\pmb y}}$$

第一步将受污染条件重新缩放至原始条件向量的均值和标准差（$\mu_{\text{in}}, \sigma_{\text{in}}$），防止其统计特性漂移；第二步通过混合因子 $\psi \in [0,1]$ 在“重缩放后的污染条件”与“原始污染条件”之间插值，为控制多样性-质量的权衡提供了额外的调节旋钮。消融实验（Table 6c）表明，$\psi=1$ 可显著改善图像质量（FID 从 12.18 降至更低），但会轻微牺牲多样性（Recall 从 0.78 降至 0.55）。

### 3. 零训练成本的即插即用设计

CADS 最显著的优势在于**无需对预训练扩散模型进行任何重新训练或微调**。它仅修改采样循环中的条件向量，计算开销仅为一次加法操作（噪声注入），可无缝集成到任何扩散采样器中（Table 3 验证了与 DDPM、DDIM 等主流采样器的兼容性）。这一特性使其区别于需要重新训练的条件增强方法，也区别于仅调整引导权重的 Dynamic CFG 策略——后者虽然也使用 $\gamma(t)$ 调制 $w_{\text{CFG}}$，但无法像 CADS 那样直接平滑条件分布本身，因此在多样性和 FID 上均不如 CADS（Table 4：CADS FID 9.47 vs Dynamic CFG FID 18.42）。

### 创新总结

| 创新维度 | baseline 做法 | CADS 做法 | 作用机制 |
|---------|-------------|----------|---------|
| 条件信号处理 | 干净条件向量 | 退火高斯噪声注入 + 重缩放混合 | 平滑条件分布，释放多样性 |
| 噪声调度 | 无 | 分段时间线性衰减 $\gamma(t)$ | 控制探索-利用节奏 |
| 模型依赖 | 依赖特定采样器 | 零训练、即插即用 | 通用性，无额外训练成本 |

这三个创新点的协同作用，使得 CADS 能够在保持甚至提升图像质量的前提下，将 DeepFashion 姿态生成任务的 Recall 从 0.02 提升至 0.48，将 ImageNet 256×256 类条件生成的 FID 从 20.83 降至 9.47，并在 DiT-XL/2 上取得 FID 1.70 的新 SOTA。



CADS（Condition-Annealed Diffusion Sampler）是一种即插即用的推理时采样策略，其核心思想是通过在扩散模型的采样循环中逐步衰减（退火）条件信号的强度，来平滑尖锐的条件分布，从而在保持生成质量的同时大幅提升样本多样性。整个框架无需对预训练扩散模型进行任何重新训练，也无需修改模型权重或架构，仅需在标准采样循环中插入一个轻量级的**条件退火模块**。

该模块的输入输出流如下：在扩散采样的每一时间步 $t$，原始的条件向量 $\pmb{y}$（例如类别标签的嵌入向量、姿态关键点编码等）首先经过**条件污染**步骤，按照式（1）加入由退火调度控制的高斯噪声，得到受污染的条件向量 $\widehat{\pmb{y}}$：

$$
\widehat{\pmb{y}} = \sqrt{\gamma(t)} \, \pmb{y} + s \sqrt{1 - \gamma(t)} \, \pmb{n}
$$

其中 $\pmb{n} \sim \mathcal{N}(0, I)$ 为标准高斯噪声，$s$ 为噪声尺度，$\gamma(t)$ 为随时间单调递减的退火函数。随后，受污染的条件向量经过**重缩放与混合**（式3、式4），先将其标准化至原始条件向量的均值和方差，再通过混合因子 $\psi$ 与原始受污染向量进行线性混合，以防止采样过程发散并控制多样性-质量平衡：

$$
\widehat{\pmb{y}}_{\text{rescaled}} = \frac{\widehat{\pmb{y}} - \text{mean}(\widehat{\pmb{y}})}{\text{std}(\widehat{\pmb{y}})} \sigma_{\text{in}} + \mu_{\text{in}}, \quad
\widehat{\pmb{y}}_{\text{final}} = \psi \, \widehat{\pmb{y}}_{\text{rescaled}} + (1 - \psi) \, \widehat{\pmb{y}}
$$

最终，处理后的条件向量 $\widehat{\pmb{y}}_{\text{final}}$ 替代原始条件输入扩散模型去噪网络 $D_\theta$，并与无分类器引导（CFG）结合使用，完成该时间步的去噪预测。

**退火调度**（式2）采用分段线性函数，由两个阈值 $\tau_1$ 和 $\tau_2$ 控制：在 $t \leq \tau_1$ 时 $\gamma(t) = 1$（不添加噪声，保留完整条件信号以保证条件对齐）；在 $t \geq \tau_2$ 时 $\gamma(t) = 0$（噪声强度最大，最大化多样性）；中间区域线性过渡。消融实验（Table 10）表明，分段线性调度在所有多项式退火方案中表现最优。

整个 CADS 模块可无缝嵌入到任何扩散采样器（如 DDPM、DDIM、DPM-Solver 等）中，其计算开销极小，仅涉及一次加法操作。Algorithm 1 和 Figure 15 给出了完整的采样循环伪代码及流程图。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_zMoNrajk2X/figures/015_Figure_7.jpg]]
*Figure 7: Visual illustration of how different hyperparameters affect CADS*



CADS 的核心思想是在扩散模型的推理采样过程中，向条件向量注入随时间衰减的高斯噪声，从而平滑尖锐的条件分布，在保持生成质量的同时大幅提升多样性。该方法无需对预训练扩散模型进行任何重新训练，且计算开销极小，仅涉及加法操作。

### 条件噪声注入

CADS 在采样循环的每一步对条件向量 $\pmb{y}$ 进行污染，其核心操作为：

$$\widehat{\pmb{y}} = \sqrt{\gamma(t)} \pmb{y} + s \sqrt{1 - \gamma(t)} \pmb{n}$$

其中各变量含义如下：
- $\pmb{y}$：原始条件向量（如类别嵌入、姿态关键点编码等）
- $\pmb{n} \sim \mathcal{N}(0, \mathbf{I})$：标准高斯噪声
- $s$：噪声尺度，控制注入噪声的总体强度
- $\gamma(t)$：退火函数，随时间步 $t$ 单调递减，控制条件信号与噪声的混合比例
- $\widehat{\pmb{y}}$：污染后的条件向量，用于替换原始条件输入扩散模型

该公式实现了条件信号从纯净到噪声的平滑过渡：当 $\gamma(t) = 1$ 时，$\widehat{\pmb{y}} = \pmb{y}$，条件保持完整；当 $\gamma(t) = 0$ 时，$\widehat{\pmb{y}} = s \pmb{n}$，条件完全被噪声替代。

### 分段线性退火调度

退火函数 $\gamma(t)$ 采用分段线性形式，由两个阈值 $\tau_1$ 和 $\tau_2$ 控制：

$$\gamma(t) = \begin{cases}
1, & t \leq \tau_1, \\[6pt]
\dfrac{\tau_2 - t}{\tau_2 - \tau_1}, & \tau_1 < t < \tau_2, \\[10pt]
0, & t \geq \tau_2.
\end{cases}$$

该调度策略的设计逻辑是：在采样早期（$t \leq \tau_1$），保持完整条件信号以确保生成结构的基本正确；在中间阶段（$\tau_1 < t < \tau_2$），逐步减弱条件强度以引入多样性；在采样后期（$t \geq \tau_2$），完全移除条件信号，让扩散模型自由填充细节。消融实验证实，分段线性退火在所有多项式退火变体（不同阶数 $d$）中表现最优（Table 10）。

### 重缩放与混合

直接使用受污染的条件向量可能导致数值不稳定或条件漂移。CADS 引入重缩放和混合两步后处理：

$$\widehat{\pmb{y}}_{\text{rescaled}} = \frac{\widehat{\pmb{y}} - \text{mean}(\widehat{\pmb{y}})}{\text{std}(\widehat{\pmb{y}})} \sigma_{\text{in}} + \mu_{\text{in}}$$

$$\widehat{\pmb{y}}_{\text{final}} = \psi \widehat{\pmb{y}}_{\text{rescaled}} + (1 - \psi) \widehat{\pmb{y}}$$

其中：
- $\mu_{\text{in}}$、$\sigma_{\text{in}}$：原始条件向量的均值和标准差
- $\psi \in [0, 1]$：混合因子，控制重缩放条件与原始污染条件的混合比例

重缩放步骤将污染后的条件向量重新对齐到原始条件的统计分布，防止条件信号在退火过程中发生均值偏移或方差膨胀。混合因子 $\psi$ 则提供了额外的控制手柄：$\psi = 1$ 时完全使用重缩放条件，可显著改善图像质量（FID 从 ψ=0 时的较差水平提升至 12.18），但会轻微降低多样性（Recall 从 0.78 降至 0.55）（Table 6c）。

### 与无分类器引导的集成

CADS 可与标准的无分类器引导（Classifier-Free Guidance, CFG）无缝集成。CFG 的预测公式为：

$$\hat{D}_\theta(z_t, t, y) = D_\theta(z_t, t, y_{\text{null}}) + w_{\text{CFG}} (D_\theta(z_t, t, y) - D_\theta(z_t, t, y_{\text{null}}))$$

在 CADS 框架中，只需将污染后的条件 $\widehat{\pmb{y}}_{\text{final}}$ 替换原始条件 $y$ 即可。此外，CADS 还可与 Dynamic CFG 结合，后者使用退火函数动态缩放引导权重：

$$\hat{w}_{\text{CFG}} = \gamma(t) w_{\text{CFG}}$$

实验表明，两者结合在高引导尺度（$w_{\text{CFG}} = 5$）时有益（FID 8.14 vs 9.47），但在低引导尺度（$w_{\text{CFG}} = 2.5$）时反而恶化（FID 5.43 vs 5.02）（Table 8），说明两种策略存在一定的功能重叠。

### 关键超参数总结

CADS 的核心可控参数包括：

| 参数 | 作用 | 典型取值 |
|------|------|----------|
| $s$ | 噪声尺度，控制多样性强度 | 0.05–0.1 |
| $\tau_1$ | 条件保持阶段的结束时间步 | 0.6 |
| $\tau_2$ | 条件完全退火的起始时间步 | 1.0 |
| $\psi$ | 重缩放混合因子 | 0–1 |

消融实验表明，$s$ 从 0.025 增大到 0.1 可改善 FID 和 Recall，但 $s = 0.25$ 会严重损害质量（FID 升至 42.58）（Table 6a）；$\tau_1 = 0.6$ 在质量和多样性之间达到最佳平衡（Table 6b）；CADS 对噪声分布类型（高斯、拉普拉斯、伽马）不敏感，仅标准差影响结果（Table 11）。



## 实验与关键发现

### 核心瓶颈与实验动机

条件扩散模型在推理时面临一个尖锐的困境：高无分类器引导尺度（CFG）能提升图像质量，却导致条件分布过于尖锐，使生成样本集中在少数模式上，多样性急剧下降。这一现象在小数据集（如DeepFashion）上尤为严重，即使扩大训练数据规模也只能部分缓解（Figure 2）。CADS正是针对这一“质量-多样性失衡”瓶颈而设计的推理时采样策略。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_zMoNrajk2X/figures/002_Figure_2.jpg]]
*Figure 2: Low diversity issue in the pose-to-image generation task. (a) The model trained on DeepFashion generates strongly similar outputs. (b) Training on the larger SHHQ dataset only partially solves the issue. (c) Sampling with CADS significantly reduces output similarity*

### 主实验结果

**Table 1** 汇总了CADS与DDPM在多个条件生成任务上的定量对比。在DeepFashion姿态到图像生成任务中，CADS将FID从DDPM的16.36大幅降至7.73，同时将Recall从0.02提升至0.48——后者是一个数量级的改善，直接反映了模式覆盖能力的跃升。在ImageNet 256×256类条件生成中，CADS将FID从20.83降至9.47；在512×512分辨率下，FID从23.10降至9.81。MSS（平均成对相似度）和Vendi Score等多样性指标同样一致指向CADS的显著优势。

**Table 2** 展示了CADS在ImageNet类条件生成上的最前沿基准。将CADS集成到DiT-XL/2模型中，在w_CFG=2的高引导尺度下，256×256分辨率达到FID 1.70，512×512分辨率达到FID 2.31，均超越了先前的最优方法（如MDT-G的1.79），且无需对底层扩散模型进行任何重新训练。

**Figure 5** 揭示了关键的行为模式：随着引导尺度增大，DDPM的FID先降后升（过高的引导损害多样性从而恶化FID），而CADS在整个引导尺度范围内保持更优的FID-Recall平衡，证明了其在不同引导强度下的鲁棒性。

### 条件对齐与多样性验证

一个自然的担忧是：增加多样性是否会牺牲条件对齐？**Table 5** 给出了否定答案。在姿态到图像任务中，CADS与DDPM的MPJPE（姿态误差）均为0.02；在文本到图像任务中，CLIP-Score均为0.31。类别条件生成的Top-1分类准确率仅从0.98微降至0.96。这表明条件退火在释放多样性的同时，并未实质性损害条件信号的保真度。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_zMoNrajk2X/figures/010_Table_5.jpg]]
*Table 5: Condition alignment of different methods after using CADS*

### 与Dynamic CFG的对比

Dynamic CFG通过退火函数直接缩放引导权重（$\hat{w}_{\mathrm{CFG}} = \gamma(t) w_{\mathrm{CFG}}$），是一个自然的消融基线。**Table 4** 显示，在ImageNet类条件生成中，CADS的FID为9.47、Recall为0.62，而Dynamic CFG的FID为18.42、Recall仅0.39。**Figure 6** 的定性对比进一步证实：虽然两者都能提升多样性，但CADS提供的样本变化更为丰富。这说明对条件向量本身进行退火（而非仅调整引导权重）是更根本的解决方案。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_zMoNrajk2X/figures/009_Table_4.jpg]]
*Table 4: Comparison between CADS and Dynamic CFG on class-conditional ImageNet generation*

### 消融实验

**Table 6** 系统剖析了CADS的三个核心超参数：

- **噪声尺度 s**（Table 6a）：s从0.025增大到0.1时，FID和Recall同步改善；但s=0.25时FID急剧恶化至42.58，表明过强的噪声会破坏生成质量。
- **截断阈值 τ₁**（Table 6b）：τ₁=0.6在质量（FID 15.79）和多样性（Recall 0.52）之间达到最佳平衡。τ₁过小（0.2）损害质量，过大（0.9）则多样性提升不足。
- **重缩放因子 ψ**（Table 6c）：ψ=1（完全重缩放）显著改善图像质量（FID从ψ=0时的12.18进一步优化），但会轻微降低多样性（Recall从0.78降至0.55），验证了重缩放-混合机制在稳定采样中的关键作用。

**Table 10** 对比了分段线性退火与多项式退火调度：在所有多项式阶数d下，分段线性函数均表现更优，支持了论文的调度选择。

**Table 11** 验证了CADS对噪声分布类型（高斯、拉普拉斯、伽马）不敏感，仅噪声标准差影响结果，说明方法具有良好的分布鲁棒性。

### 采样器兼容性

**Table 3** 展示了CADS与主流扩散采样器的集成效果。在DiT-XL/2类条件ImageNet模型上，CADS增强了DDPM、DDIM、DPM-Solver等所有测试采样器的样本多样性，证实了其作为即插即用模块的通用性。

### 失败模式与局限性

1. **超参数敏感性**：CADS的性能依赖于手动选择场景相关的超参数（s、τ₁、τ₂、ψ），目前缺乏自动调参机制。不同任务和模型需要独立调整，增加了使用门槛。
2. **密集空间条件挑战**：将CADS应用于具有密集空间语义的条件（如语义分割掩码）仍然具有挑战性，论文明确将此列为开放问题。
3. **高引导尺度下的强噪声需求**：在高w_CFG下，CADS需要较强的噪声来有效平滑条件分布，这可能不适用于某些高度结构化的条件任务。
4. **Dynamic CFG结合的稳定性**：**Table 8** 显示，在高w_CFG=5时结合Dynamic CFG有益（FID 8.14 vs 9.47），但在w_CFG=2.5时反而恶化（FID 5.43 vs 5.02），说明联合使用并非普遍有效，需要谨慎调参。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_zMoNrajk2X/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison between samples generated with DDPM and CADS for a fixed high guidance scale. CADS consistently improves the diversity of the outputs across different tasks as reflected in improved FID, recall, and similarity scores*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_zMoNrajk2X/figures/006_Table_2.jpg]]
*Table 2: Benchmark for class-conditional generation on ImageNet 256×256 and 512×512. Sampling with CADS improves the FID of DiT-XL/2 to the state-of-the-art at both resolutions while using a higher guidance value and without any retraining of the underlying diffusion model*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_zMoNrajk2X/figures/007_Figure_5.jpg]]
*Figure 5: The behavior of the evaluation metrics across different guidance scales. CADS exhibits superior ability to balance quality and diversity, evidenced by better performance in FID and Recall*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_zMoNrajk2X/figures/008_Table_3.jpg]]
*Table 3: Impact of integrating CADS with popular diffusion samplers using the class-conditional ImageNet model (DiT-XL/2). CADS enhances sample diversity across all samplers*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_zMoNrajk2X/figures/012_Table_6.jpg]]
*Table 6: Ablation study examining various design elements in CADS*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_zMoNrajk2X/figures/020_Figure_10.jpg]]
*Figure 10: Comparing DDPM with CADS on a pose-to-image model trained on noisy pose images. Training on noisy images does not solve the issue of low-diversity by default, and sampling with CADS is still needed to achieve better diversity*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_zMoNrajk2X/figures/030_Table_10.jpg]]
*Table 10: Comparing different choices of*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_zMoNrajk2X/figures/032_Table_11.jpg]]
*Table 11: Comparing different noise distributions for n in Equation (1) on class-conditional ImageNet generation with*



## 定位与知识库关联

### 主要基线对比与谱系关系

CADS 的核心定位是**推理时采样策略**，而非新的扩散模型架构或训练范式。其直接对比的基线包括：

- **DDPM**（Ho et al., NeurIPS 2020）：标准扩散概率模型采样器，是 CADS 的主要基线。在条件生成任务中，DDPM 在高无分类器引导尺度下虽然能提升图像质量，但会导致生成样本严重集中在少数模式上，多样性急剧下降。CADS 通过在推理时向条件向量注入退火噪声，在不重新训练模型的前提下显著缓解了这一问题。

- **DDIM**（Song et al., ICLR 2021）：确定性快速采样器。CADS 被证明可无缝集成到 DDIM 中，同样能提升其生成多样性（见 Table 3），表明 CADS 的适用性不限于随机采样器。

- **Dynamic CFG**：动态调整无分类器引导权重的消融基线。其核心操作是将引导权重 $w_{\mathrm{CFG}}$ 乘以退火函数 $\gamma(t)$，即 $\hat{w}_{\mathrm{CFG}} = \gamma(t) w_{\mathrm{CFG}}$。实验表明，虽然 Dynamic CFG 也能提高多样性，但 CADS 在 FID 和 Recall 上均显著优于 Dynamic CFG（ImageNet 256×256 类条件生成：CADS 的 FID 为 9.47、Recall 为 0.62，而 Dynamic CFG 的 FID 为 18.42、Recall 为 0.39，见 Table 4）。值得注意的是，在高引导尺度（$w_{\mathrm{CFG}}=5$）下将 Dynamic CFG 与 CADS 结合使用是有益的（FID 从 9.47 降至 8.14），但在低引导尺度（$w_{\mathrm{CFG}}=2.5$）下反而恶化（FID 从 5.02 升至 5.43，见 Table 8），说明两者结合并非在所有场景下都稳定有效。

从方法谱系来看，CADS 属于**条件信号调制**类方法，与以下方向形成互补或对比：

- **训练时条件噪声注入**：实验表明，仅在训练时向条件图像（如姿态图）添加噪声并不能解决推理时的低多样性问题，CADS 在推理时仍然必要（见 Figure 10）。这验证了 CADS 的瓶颈在于推理时条件分布过于尖锐，而非训练数据不足。

- **引导尺度调度**：Dynamic CFG 通过调度引导权重来间接影响条件强度，而 CADS 直接作用于条件向量本身。实验证明直接条件退火比引导权重调度更有效。

- **多样性促进采样器**：CADS 与多种主流扩散采样器（DDPM、DDIM、DPM-Solver 等）兼容（Table 3），表明其作为即插即用模块的通用性。

### 适用边界与局限

**适用场景**：

- 条件扩散模型在推理时使用高无分类器引导尺度（$w_{\mathrm{CFG}} \geq 2.5$）的场景，此时 DDPM 等标准采样器会出现严重的模式坍塌。
- 小数据集训练的条件模型（如 DeepFashion），条件分布本身较为尖锐，CADS 的多样性提升尤为显著。
- 类条件生成、姿态到图像生成、身份条件人脸合成等任务，CADS 在保持条件对齐的同时大幅提升多样性。

**局限与挑战**：

1. **超参数依赖手动选择**：CADS 的核心超参数包括噪声尺度 $s$、截断阈值 $\tau_1$ 和 $\tau_2$、混合因子 $\psi$，这些参数对任务场景敏感。消融实验显示：$s$ 从 0.025 增大到 0.1 可改善多样性，但 $s=0.25$ 会严重损害质量（FID 升至 42.58）；$\tau_1=0.6$ 在质量与多样性之间达到最佳平衡；$\psi=1$ 显著改善质量但轻微降低多样性（Table 6）。目前缺乏针对不同任务的自动调参机制，这是一个待解决的实际问题。

2. **密集空间语义条件的挑战**：将 CADS 应用于具有密集空间语义的条件（如语义分割图、深度图）仍然具有挑战性。这类条件的高维结构化特性使得简单的噪声注入和重缩放策略可能不足以平衡多样性与条件对齐。

3. **高引导尺度下的强噪声需求**：在高引导尺度下，CADS 需要较强的噪声（较大的 $s$）才能有效提升多样性，这可能不适用于某些高度结构化的条件任务，因为强噪声可能破坏条件的语义完整性。

4. **极低采样步数下的有效性未充分验证**：在极低 NFE（Number of Function Evaluations）设置下，退火调度应如何调整才能保持有效性，目前缺乏系统的实验分析。

### 开放问题

- **自动超参数优化**：如何针对不同任务自动优化 $\tau_1$、$\tau_2$、$s$ 和 $\psi$，以实现最优的多样性-质量权衡？是否可以通过学习或启发式方法从条件分布的特性中推断合适的退火参数？

- **复杂条件模态的扩展**：CADS 在更复杂的条件模态（如语义分割图、深度图、文本嵌入的中间层表示）上的表现如何？是否需要针对不同模态设计特定的噪声注入和重缩放策略？

- **与 Dynamic CFG 的协同机制**：Dynamic CFG 与 CADS 结合使用在某些引导尺度下有益，但在其他尺度下有害，其背后的机制是什么？是否存在更优的结合方式？

- **退火调度的理论最优性**：当前的分段线性退火调度是经验选择（实验表明其优于多项式退火，见 Table 10），是否存在理论上的最优退火形式？退火速率与条件分布尖锐度之间的关系是什么？

- **评估指标的局限性**：论文指出 IS 和 Precision 在评估多样性时存在局限性，会对 DDPM 给出虚高的值（Table 12），而 FID 更能综合反映真实性和多样性。这一发现对扩散模型生成质量的评估体系有更广泛的启示，需要进一步研究。



## 原文 PDF

![[paperPDFs/ICLR_2024/CADS_Unleashing_the_Diversity_of_Diffusion_Models_through_Condition_Annealed_Sampling.pdf]]
