---
title: EnergyMoGen Compositional Human Motion Generation with Energy Based Diffusion Model in Latent Space
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/EnergyMoGen_Compositional_Human_Motion_Generation_with_Energy_Based_Diffusion_Model_in_Latent_Space.pdf
project_link: https://jiro-zhang.github.io/EnergyMoGen/
code_link: null
aliases:
- ECHMGEBDMLS
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将扩散过程重新解释为基于能量的采样，并引入潜在感知和语义感知两种能量模型，通过协同能量融合（SEF）动态平衡文本一致性与运动平滑度，实现多概念在潜在空间中的可组合生成。
primary_logic: 扩散模型可被视为能量模型，其去噪步等价于朗之万动力学中的梯度下降；利用能量函数的可加性，通过合取与否定算子组合简单概念的能量项，辅以能量化交叉注意力的自适应文本嵌入更新，即可生成复杂组合动作。
claims:
- 扩散模型被解释为能量模型后，能够通过组合能量项实现多概念动作生成。
- 语义感知的能量模型通过交叉注意力的自适应梯度下降显著提升了多概念动作生成的文本一致性。
- 协同能量融合（SEF）结合了潜在感知和语义感知的互补优势，有效缓解了文本错位与动作失真问题。
- HumanML3D 上 R-Precision Top-3 ↑ = 0.815 (ENERGYMOGEN)
---

# EnergyMoGen Compositional Human Motion Generation with Energy Based Diffusion Model in Latent Space

> [!tip] 核心洞察
> 扩散模型可被视为能量模型，其去噪步等价于朗之万动力学中的梯度下降；利用能量函数的可加性，通过合取与否定算子组合简单概念的能量项，辅以能量化交叉注意力的自适应文本嵌入更新，即可生成复杂组合动作。

| 字段 | 内容 |
|------|------|
| 中文题名 | EnergyMoGen：基于潜在空间能量扩散模型的组合人体动作生成 |
| 英文题名 | EnergyMoGen Compositional Human Motion Generation with Energy Based Diffusion Model in Latent Space |
| 会议/期刊 | CVPR 2025 |
| Links | [Project](https://jiro-zhang.github.io/EnergyMoGen/) · [paper](https://arxiv.org/abs/2412.14706) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | ENERGYMOGEN |
| Dataset | HumanML3D, KIT-ML, MTT |

> [!tip] 效果简介
> - HumanML3D 上，R-Precision Top-3 ↑ 0.815 (ENERGYMOGEN) vs 0.795 (ReMoDiffusion) (+0.020)；MM-Dist ↓ 2.915 (ENERGYMOGEN) vs 2.974 (ReMoDiffusion) (-0.059)。
> - KIT-ML 上，R-Precision Top-3 ↑ 0.772 (ENERGYMOGEN) vs 0.772 (FineMoGen) (0.000 (tied best))。
> - MTT (Compositional Generation) 上，R@3 ↑ 28.0 (Ours + SEF) vs 25.4 (Ours single-text baseline) (+2.6)。

## 概要

人体动作生成领域面临一个核心瓶颈：**潜在扩散模型在组合多个语义概念生成连贯动作时存在困难**。根本原因在于，现有方法将动作编码为固定数量的潜在向量，这些向量与动作帧之间缺乏显式对应关系，导致无法支持逐帧的组合操作——当文本描述包含“边走边挥手”或“坐下但不弯腰”等多概念指令时，模型难以在潜在空间中精确融合这些语义。

针对这一挑战，EnergyMoGen 提出了一项关键洞察：**扩散模型可被重新解释为基于能量的模型**，其去噪步等价于朗之万动力学中的梯度下降。利用能量函数的可加性，通过合取与否定算子组合简单概念的能量项，即可生成复杂的组合动作，而无需重新训练或设计专门的组合模块。

基于此，EnergyMoGen 构建了两种互补的能量模型谱系：**潜在感知能量模型**在去噪网络层面通过无分类器引导实现概念组合；**语义感知能量模型**则将交叉注意力操作重新定义为能量函数，通过自适应梯度下降更新文本嵌入以增强多概念对齐。为克服单一谱系带来的文本错位或动作失真，方法进一步引入了**协同能量融合**，动态加权整合两种谱系的分数，在文本一致性与运动平滑度之间取得平衡。

在 HumanML3D 和 KIT-ML 两个主流基准上，EnergyMoGen 在文本-动作对齐指标上达到领先水平：HumanML3D 上 R-Precision Top-3 达到 0.815，MM-Dist 降至 2.915；在专门评估组合生成能力的 MTT 数据集上，协同能量融合使 R@3 相比单文本基线提升 2.6 个百分点。消融实验证实，语义感知的自适应梯度下降贡献了 1.3% 的 Top-1 精度增益，而协同融合有效缓解了单独使用语义组合时引入的脚步滑动问题。

值得注意的是，该方法仍存在局限性：对训练中未见过的全新概念组合表现不佳；固定数量的潜在向量限制了更精细的逐帧组合操作；生成多样性在部分指标上尚未全面超越所有基线方法。



### 问题背景

文本驱动的三维人体动作生成旨在根据自然语言描述合成逼真的人体运动序列，这一任务在电影制作、虚拟现实和具身智能等领域具有重要应用价值。近年来，扩散模型凭借其稳定的训练过程和高质量的生成能力，已成为该领域的主流范式。然而，现有方法大多聚焦于单一文本描述的简单动作生成，难以应对真实世界中人类动作的复杂性——一个完整的动作序列往往同时包含多个语义概念，例如“一个人边走路边挥手”或“一个人走路但不弯腰”。

### 现有方法缺口

当前扩散模型在组合动作生成上面临两个层面的根本性困难。

**第一，潜在扩散模型的架构限制。** 为了降低计算开销，主流方法（如 **MLD**）将运动序列压缩为固定数量的潜在向量，再在潜在空间中进行扩散。然而，这种压缩丢弃了潜在向量与运动帧之间的显式对应关系（analysis_truth: real_bottleneck）。当需要组合多个语义概念时，缺乏逐帧对应意味着无法对不同概念对应的运动片段进行精确的空间-时间操控，只能对整个潜在表示进行粗粒度操作。

**第二，组合机制的缺失。** 大多数文本-动作生成模型仅支持单一文本条件输入，不具备将多个语义概念的能量分布进行组合的内在机制。即便将多概念文本拼接后输入模型，由于模型从未见过此类组合文本，生成的语义一致性和运动平滑度往往显著下降。现有的组合生成方法（如 **PriorMDM**）主要基于骨架空间的扩散模型，通过手工设计的组合规则在推理时融合多个模型的预测分数，但这类方法依赖于运动帧的显式结构，无法直接迁移到潜在扩散模型中。

### 核心洞察与动机

本文的核心洞察在于：**扩散模型本质上可以被解释为基于能量的模型（Energy-Based Model, EBM）**。具体而言，扩散模型的去噪步等价于朗之万动力学中的梯度下降过程，而能量函数天然具有可加性——多个概念的能量项可以通过简单的代数操作（如加法、减法）进行组合。这一视角为潜在空间中的组合动作生成提供了理论突破口：如果能在潜在扩散模型中建立多概念的能量函数，并利用能量可加性实现语义组合，就无需依赖潜在向量与运动帧的显式对应关系。

然而，单纯在潜在空间中组合能量分布面临**语义不一致**与**运动失真**的权衡：基于去噪网络的“潜在感知”能量组合能保持运动平滑度，但文本对齐能力有限；基于交叉注意力的“语义感知”能量组合能提升文本一致性，却容易引入脚步滑动和动作抖动。本文的动机正是通过协同融合这两种互补的能量谱系，在保持运动质量的同时实现多概念的精确语义组合。



## 核心方法与创新机理

ENERGYMOGEN 的核心创新在于将潜在扩散模型的去噪过程重新解释为基于能量的采样，并围绕这一视角构建了三个相互协同的关键机制，从而首次在连续潜在空间中实现了多语义概念的可组合人体动作生成。

### 1. 扩散模型到能量模型的范式转换

传统潜在扩散模型在组合多个语义概念时面临根本性困难：潜在向量与动作帧之间缺乏显式对应关系，且固定数量的潜在向量难以支持逐帧的组合操作。ENERGYMOGEN 的关键突破在于将扩散模型的去噪步等价为朗之万动力学中的梯度下降过程，从而将扩散模型解释为能量模型（Energy-Based Model, EBM）。这一视角转换使得能量函数的可加性得以利用——通过组合简单概念的能量项，即可生成复杂组合动作，而无需重新训练或修改模型架构。

### 2. 双谱系能量组合机制

基于上述范式转换，ENERGYMOGEN 提出了两种互补的能量模型谱系：

**潜在感知能量组合（Latent-aware Energy Composition）**：直接在潜在向量的去噪网络上操作，利用无分类器引导实现概念的合取与否定。合取操作通过累加各概念条件分数与无条件分数的差异实现（Equation 7），否定操作则通过减去指定概念的条件分数实现（Equation 8）。这种方式保持了动作的物理平滑性，但在复杂语义对齐上存在局限。

**语义感知能量组合（Semantic-aware Energy Composition）**：将交叉注意力重新解释为能量操作，通过自适应梯度下降（Adaptive Gradient Descent, AGD）在推理过程中动态更新文本嵌入（Equation 3-4），使多个概念的语义特征在注意力层面实现融合（Equation 9）。消融实验表明，AGD 将多概念生成的 R-Precision Top-1 和 Top-3 分别提升了 1.3% 和 0.9%（Table 3），显著增强了文本一致性，但单独使用时容易引入脚步滑动和动作抖动。

### 3. 协同能量融合（Synergistic Energy Fusion, SEF）

两种能量谱系存在互补与冲突：潜在感知组合保证动作平滑但语义对齐不足，语义感知组合提升文本一致性但引入运动失真。ENERGYMOGEN 通过 SEF 机制将两者统一，在每一步去噪过程中线性加权融合三种分数：潜在感知组合分数、语义感知组合分数以及多概念联合文本的预测分数（Equation 10）：

$$\hat{\epsilon}_\theta(z_t, t, \mathbb{C}, \mathbf{c}_{1,n}) = \lambda_l \epsilon_\theta^l(z_t, t, \mathbb{C}) + \lambda_s \epsilon_\theta^s(z_t, t, \mathbb{C}) + \lambda_m \epsilon_\theta(z_t, t, \mathbf{c}_{1,n})$$

消融实验确定最优权重为 $\lambda_l=0.1$, $\lambda_s=0.7$, $\lambda_m=0.2$（Table 7），该配置在文本对齐（R-Precision, TMR-Score）与动作平滑度（Transition distance）之间取得了最佳平衡。在 MTT 组合生成基准上，SEF 将 R@3 从单文本基线的 25.4 提升至 28.0（Table 3），同时将脚步滑动指标 PFC 从语义单独模式的 1.05 降至 0.51（Table 11），有效缓解了文本错位与动作失真的两难困境。

### 相对于基线方法的 Changed Slots

与现有方法相比，ENERGYMOGEN 在以下关键设计点上实现了根本性改变：

- **组合机制**：从仅支持单文本生成的基线（如 MDM、MLD、MotionDiffuse 等）转变为支持合取、否定及多概念联合的能量组合范式。
- **交叉注意力形式**：从标准 softmax 注意力转变为基于能量的交叉注意力，并引入自适应梯度下降在推理时优化文本嵌入。
- **能量项融合**：从单一能量项（仅无分类器引导）转变为 SEF 线性加权融合三种互补分数。
- **推理过程**：从标准 DDPM 逆向过程转变为基于能量的 MCMC 类采样，通过加权分数求和实现多概念协同生成。



ENERGYMOGEN 的整体 pipeline 由三个核心模块串联构成：**运动变分自编码器（Motion VAE）**、**基于能量化交叉注意力的潜在扩散模型（LDM）**，以及**协同能量融合（Synergistic Energy Fusion, SEF）**框架。Figure 2 给出了完整的架构示意。

![[assets/figures/papers/paper_list_l1857_EnergyMoGen_Compositional_Human_Motion_Generation_with_Energy_Based_Diff/figures/002_Figure_2.jpg]]
*Figure 2: Overview of ENERGYMOGEN. (a) Motion Variational Autoencoder (VAE) maps 3D human motion into N latent vectors. (b) We use cross-attention-based transformers as the denoising network in the Latent Diffusion Model (LDM)*

### 运动变分自编码器（Motion VAE）

该模块负责将 3D 人体运动序列压缩到连续潜在空间。编码器将原始运动映射为 $N$ 个潜在向量，解码器则从这些向量重建运动。训练目标为 $L_1$ 平滑损失与 KL 散度的组合。消融实验表明，$N=5$ 时文本到动作生成性能最佳，而纯重建任务以 $N=7$ 最优（Table 8）。编码器、解码器及后续的去噪自编码器均由 9 层 Transformer 块构成，维度 $d=256$。

### 基于能量化交叉注意力的潜在扩散模型（LDM）

扩散过程在 VAE 的潜在空间中执行。去噪网络采用交叉注意力 Transformer，其关键创新在于将交叉注意力重新解释为**能量操作**：通过最大后验估计（MAP），对文本嵌入 $\pmb{c}$ 执行自适应梯度下降（AGD），使其向更符合当前潜在状态的方向更新：

$$\hat{\pmb{c}} = \pmb{c} + \gamma \nabla_{\pmb{K}} \log p(\pmb{K}|\pmb{Q})$$

其中梯度项 $\nabla_{\mathcal{K}} \log p(\mathcal{K}|\mathcal{Q})$ 由注意力映射项和正则化项组成（Equation 3）。这一设计使文本条件能够根据扩散过程中的中间潜在状态动态调整，为后续多概念组合奠定基础。消融实验证实，AGD 将 R-Precision Top1 提升 1.3%、Top3 提升 0.9%（Table 3）。

### 协同能量融合（SEF）

框架的核心在于将扩散模型统一解释为**基于能量的模型（EBM）**，并利用能量函数的可加性实现组合生成。ENERGYMOGEN 探索了两种 EBM 谱系：

- **潜在感知能量组合**：将去噪网络本身视为能量函数，通过无分类器引导实现概念的合取（累加各概念分数与无条件分数的差异）与否定（减去指定概念的条件分数）。
- **语义感知能量组合**：通过交叉注意力特征的加权平均实现多概念在语义层面的混合。

SEF 将上述两种谱系与多概念联合文本的预测进行线性加权融合，得到最终的去噪分数：

$$\hat{\epsilon}_\theta(z_t, t, \mathbb{C}, \mathbf{c}_{1,n}) = \lambda_l \epsilon_\theta^l(z_t, t, \mathbb{C}) + \lambda_s \epsilon_\theta^s(z_t, t, \mathbb{C}) + \lambda_m \epsilon_\theta(z_t, t, \mathbf{c}_{1,n})$$

其中 $\lambda_l$、$\lambda_s$、$\lambda_m$ 为超参数。消融实验确定 $\lambda_l=0.1$、$\lambda_s=0.7$、$\lambda_m=0.2$ 时在文本对齐（R-Precision、TMR-Score）与运动平滑度（Transition distance）之间取得最佳平衡（Table 7）。SEF 有效缓解了单独使用潜在感知组合时的文本错位问题，以及单独使用语义感知组合时引入的脚步滑动和动作抖动（PFC 指标从语义单独模式的 1.05 降至 SEF 的 0.51，Table 11）。

### 数据流总览

1. 原始运动序列 $\to$ Motion VAE 编码器 $\to$ $N$ 个潜在向量 $z_0$
2. $z_0$ 经前向扩散加噪 $\to$ $z_t$，同时多概念文本经 CLIP 编码为嵌入 $\pmb{c}_i$
3. 去噪 Transformer 在每一步对 $z_t$ 和文本嵌入执行能量化交叉注意力，AGD 自适应更新文本嵌入
4. SEF 融合潜在感知、语义感知及联合文本三路能量分数，输出组合去噪预测 $\hat{\epsilon}_\theta$
5. 经完整逆向扩散过程得到去噪潜在向量 $\to$ Motion VAE 解码器 $\to$ 最终运动序列

### 补充图表

![[assets/figures/papers/paper_list_l1857_EnergyMoGen_Compositional_Human_Motion_Generation_with_Energy_Based_Diff/figures/018_Figure_7.jpg]]
*Figure 7: Visual results of energy distributions. For a clear illustration, energy distributions are calculated with interpolation and Gaussian smoothing and then visualized as contour maps. (a) Concept 1, (b) Concept 2, (c) Compositional motion generation, (d) Multiconcept motion generation. Similar regions are highlighted in red*



### 3.1 运动变分自编码器（Motion VAE）

ENERGYMOGEN 的整体框架首先通过一个运动变分自编码器将 3D 人体运动序列压缩到连续潜在空间。该 VAE 由运动编码器和运动解码器组成，各包含 9 层 Transformer 块，维度 $d=256$。编码器将原始运动序列映射为 $N$ 个潜在向量，解码器则从这些潜在向量重建运动。训练时使用 L1 平滑损失和 KL 散度进行重建约束。消融实验表明，$N=5$ 个潜在向量在文本到动作生成任务上取得最佳性能，而纯重建任务的最优值为 $N=7$（Table 8）。

### 3.2 基于能量的潜在扩散模型

在潜在空间中，扩散模型的标准优化目标为去噪自编码器的 MSE 损失：

$$\mathbb{E}_{z,c,\epsilon,t} \Big[ || \epsilon - \epsilon_{\theta}(z_t, t, c) ||_2^2 \Big]$$

扩散模型的核心洞察在于：**去噪过程可被重新解释为基于能量的采样**。具体而言，当将能量函数 $E_\theta(z_t, c)$ 通过去噪自编码器 $\epsilon_\theta$ 表示时，扩散模型的去噪步等价于朗之万动力学中梯度步长为 $\eta=1$ 的梯度下降（Section 3.2, Equation 5-6）。这一解释为后续的能量组合操作奠定了理论基础。

### 3.3 能量化交叉注意力与自适应文本嵌入更新

在潜在扩散模型的去噪网络中，交叉注意力被重新解释为一种基于能量的操作。给定查询 $\mathcal{Q}$ 和键 $\mathcal{K}$，交叉注意力的能量梯度可表示为：

$$\nabla_{\mathcal{K}} \log p(\mathcal{K}|\mathcal{Q}) = \left[ \operatorname{SFM}(\alpha K \mathcal{Q}^{\top}) \mathcal{Q} - \mathcal{M}(\operatorname{SFM}(\mathcal{K}')) \mathcal{K} \right] W_K$$

该梯度由两部分组成：注意力映射项驱动文本特征向运动查询对齐，正则化项 $\mathcal{M}$ 则约束文本嵌入不过度偏离原始分布。基于此梯度，文本嵌入通过自适应梯度下降（Adaptive Gradient Descent, AGD）进行更新：

$$\hat{\pmb{c}} = \pmb{c} + \gamma \nabla_{\pmb{K}} \log p(\pmb{K}|\pmb{Q})$$

其中 $\gamma$ 为步长。消融实验表明，$\gamma_{\text{attn}}=0.001$ 和 $\gamma_{\text{reg}}=0.002$ 的设置取得最佳结果，而较大的步长（$\geq 0.1$）会显著降低性能（Table 9）。AGD 在 MTT 数据集上将多概念生成的 R-Precision Top-1 提升了 1.3%，Top-3 提升了 0.9%（Table 3），验证了其在增强多概念文本对齐方面的有效性。

### 3.4 潜在感知能量组合

基于扩散模型作为能量模型的解释，潜在感知组合利用无分类器引导（classifier-free guidance）在潜在空间中直接组合多个概念的分布。对于概念合取（conjunction），其组合分数为各概念条件分数与无条件分数差异的加权累加：

$$\epsilon_\theta^l(z_t, t, \mathbb{C}) = \epsilon_\theta(z_t, t) + \sum_{i=1}^n w_i^l (\epsilon_\theta(z_t, t, \pmb{c}_i) - \epsilon_\theta(z_t, t))$$

对于概念否定（negation），则通过减去指定概念的条件分数实现：

$$\epsilon_\theta^l(z_t, t, \mathbb{C}) = \epsilon_\theta(z_t, t) + w^l (\epsilon_\theta(z_t, t, c_i) - \epsilon_\theta(z_t, t, c_j))$$

这种组合方式直接操作潜在向量的整体分布，但缺乏对逐帧语义的细粒度控制。

### 3.5 语义感知能量组合

语义感知组合在交叉注意力层面进行。多个概念的交叉注意力特征通过加权平均进行融合（Equation 9），实现语义层面的混合。这种方式能够更好地保持文本语义一致性，但单独使用时容易引入脚步滑动和动作抖动——PFC 指标显示语义单独模式为 1.05，而融合后降至 0.51（Table 11）。

### 3.6 协同能量融合（Synergistic Energy Fusion, SEF）

为解决潜在感知组合的文本错位问题与语义感知组合的运动失真问题，SEF 将三种分数进行线性加权融合，得到最终的去噪预测：

$$\hat{\epsilon}_\theta(z_t, t, \mathbb{C}, \mathbf{c}_{1,n}) = \lambda_l \epsilon_\theta^l(z_t, t, \mathbb{C}) + \lambda_s \epsilon_\theta^s(z_t, t, \mathbb{C}) + \lambda_m \epsilon_\theta(z_t, t, \mathbf{c}_{1,n})$$

其中：
- $\epsilon_\theta^l$：潜在感知组合分数（Equation 7-8）
- $\epsilon_\theta^s$：语义感知组合分数（Equation 9）
- $\epsilon_\theta(z_t, t, \mathbf{c}_{1,n})$：多概念联合文本的条件分数
- $\lambda_l, \lambda_s, \lambda_m$：平衡文本一致性与运动平滑度的超参数

消融实验表明，$\lambda_l=0.1, \lambda_s=0.7, \lambda_m=0.2$ 的设置能在文本对齐（R-Precision, TMR-Score）和运动平滑度（Transition distance）之间取得最佳平衡（Table 7）。随着 $\lambda_s$ 权重增加，生成结果更贴合文本描述；而较大的 $\lambda_l$ 则产生更平滑的运动轨迹。

### 补充图表

![[assets/figures/papers/paper_list_l1857_EnergyMoGen_Compositional_Human_Motion_Generation_with_Energy_Based_Diff/figures/005_Table_2.jpg]]
*Table 2: Comparison with the state-of-the-art diffusion models on the KIT-ML [52] test set*

![[assets/figures/papers/paper_list_l1857_EnergyMoGen_Compositional_Human_Motion_Generation_with_Energy_Based_Diff/figures/008_Figure_5.jpg]]
*Figure 5: Analysis of the latent distribution. For a clear illustration, energy distributions are calculated with interpolation and Gaussian smoothing, then visualized as contour maps. Motions in the 4th row are generated from texts, i.e., “a person is walking forward and waving both arms” and “a person is walking to the right”, which is created by composing the multiple concepts into a single text via (a) Conjunction and (b) Negation. Similar regions are highlighted in red*



## 实验与关键发现

### 核心性能对比

ENERGYMOGEN 在标准文本到动作生成基准上展现了具有竞争力的性能。在 HumanML3D 测试集上，其 R-Precision Top-3 达到 **0.815**，相较最强基线 ReMoDiffusion 的 0.795 提升了 2.0 个百分点；MM-Dist 降至 **2.915**，优于 ReMoDiffusion 的 2.974（Table 1）。在 KIT-ML 测试集上，R-Precision Top-3 为 **0.772**，与 FineMoGen 并列最优（Table 2）。定性对比（Figure 3）显示，MLD 和 FineMoGen 在“sits down in a chair”等动作上出现文本不一致，ReMoDiffuse 则遗漏了“gets back up”的动作片段，而 ENERGYMOGEN 能更好地匹配文本描述。

![[assets/figures/papers/paper_list_l1857_EnergyMoGen_Compositional_Human_Motion_Generation_with_Energy_Based_Diff/figures/003_Table_1.jpg]]
*Table 1: Comparison with the state-of-the-art diffusion models on the HumanML3D [19] test set. We repeat the evaluation 20 times for each metric and report the average with a 95% confidence interval. Bold and underlined indicate the best and second-best results. Methods based on the latent diffusion model are marked with ∗*

在组合生成任务上，方法展现出更显著的优势。在 MTT 数据集的组合生成（Compositional Generation）设置下，配备协同能量融合（SEF）的 ENERGYMOGEN 将 R@3 从单文本基线的 25.4 提升至 **28.0**（+2.6）；在多概念生成（Multi-concept Generation）设置下，配备自适应梯度下降（AGD）的版本将 R@3 提升至 **26.3**（+0.9）（Table 3）。这表明能量组合框架能够有效融合多个语义概念。

![[assets/figures/papers/paper_list_l1857_EnergyMoGen_Compositional_Human_Motion_Generation_with_Energy_Based_Diff/figures/007_Table_3.jpg]]
*Table 3: Quantitative comparison on MTT [50]. We compute metrics following STMC [50]. ‘AGD’ and ‘SEF’ denote the adaptive gradient descent and synergistic energy fusion*

### 消融实验的关键发现

**协同能量融合（SEF）的权重平衡**是方法有效性的核心调节机制。Table 7 的消融表明，当 $\lambda_l=0.1$、$\lambda_s=0.7$、$\lambda_m=0.2$ 时，模型在文本对齐（R-Precision、TMR-Score）与运动平滑度（Transition distance）之间达到最佳平衡。具体而言，增大语义感知权重 $\lambda_s$ 会提升文本一致性，但可能引入运动失真；增大潜在感知权重 $\lambda_l$ 则使运动更平滑，但可能牺牲语义对齐精度。这一权衡在脚步滑动指标上尤为明显：单独使用语义感知组合时 PFC 为 1.05，而 SEF 将其降至 **0.51**（Table 11），验证了融合策略对运动质量的改善。

**自适应梯度下降（AGD）** 对多概念文本对齐有显著贡献。在 MTT 数据集上，AGD 将 R-Precision Top1 提升 1.3%，Top3 提升 0.9%（Table 3，Section 5.5 Q1）。其背后的机制是通过能量化交叉注意力对文本嵌入进行梯度更新（Equation 3-4），使去噪过程中的条件信号更精确地反映多概念语义。Table 9 的步长消融显示，$\gamma_{attn}=0.001$ 和 $\gamma_{reg}=0.002$ 为最优设置，步长过大（≥0.1）会导致性能显著退化。

**潜在向量数量 N** 对生成质量存在非单调影响。Table 8 表明，N=5 在文本到动作生成任务上取得最佳性能，而纯重建任务的最优值为 N=7。这暗示生成任务需要比重建更强的信息压缩，以在潜在空间中形成更有利于组合操作的表示。

### 组合机制的有效性证据

Figure 5 通过能量分布的可视化揭示了组合生成的内在机制。对于“a person is walking forward and waving both arms”与“a person is walking to the right”两个概念，合取操作（Conjunction）和否定操作（Negation）分别生成的能量分布等高线图在相似区域（红色高亮）呈现出与目标组合动作一致的能量模式。这表明潜在感知的能量组合能够隐式地操纵潜在分布，使生成结果同时满足多个概念的约束。

Figure 4 展示了四种组合设置下的定性结果：概念合取、概念否定、合取+否定，以及多概念生成。模型能够精确捕捉各概念的细节并组合成复杂动作序列，例如同时执行“行走”与“挥手”的合取，或排除特定动作的否定。

![[assets/figures/papers/paper_list_l1857_EnergyMoGen_Compositional_Human_Motion_Generation_with_Energy_Based_Diff/figures/006_Figure_4.jpg]]
*Figure 4: Compositional motion generation. We use the pre-trained model on HumanML3D [19] for compositional motion generation. Our approach can accurately capture the details in concepts and compose complex motions. (a) conjunction, (b) negation, (c) conjunction + negation, (d) multi-concept generation. More visual results and comparisons can be found on the project page*

### 失败模式与局限性

Figure 8 揭示了方法的一个关键失败模式：**无法处理训练中完全未见过的概念组合**。当要求组合两个在训练数据中从未共现的概念时，生成质量会出现明显下降。这一局限源于潜在扩散模型的固有特性——固定数量的潜在向量缺乏与动作帧的显式对应关系，使得模型难以对全新组合进行逐帧的精确推理。

![[assets/figures/papers/paper_list_l1857_EnergyMoGen_Compositional_Human_Motion_Generation_with_Energy_Based_Diff/figures/019_Figure_8.jpg]]
*Figure 8: Failure case*

此外，尽管 SEF 缓解了语义感知组合带来的运动失真问题，但在 HumanML3D 上的 FID 指标仍高于 ReMoDiffusion，表明生成动作的整体分布质量尚有提升空间。语义感知组合单独使用时容易引入脚步滑动和动作抖动，这一现象在 Table 11 中得到量化印证。

![[assets/figures/papers/paper_list_l1857_EnergyMoGen_Compositional_Human_Motion_Generation_with_Energy_Based_Diff/figures/016_Table_11.jpg]]
*Table 11: Evaluation of Foot Sliding. ‘PFC’ denotes the Physical Foot Contact score*

### 框架泛化性

Table 4 和 Table 6 分别展示了将能量组合方法应用于骨架级扩散模型的结果。在 HumanML3D 和 MTT 数据集上，骨架级版本同样取得了具有竞争力的性能，验证了能量组合框架不依赖于特定的潜在空间设计，具备跨架构的泛化能力。Table 10 的推理时间对比显示，作为基于 Transformer 的模型，ENERGYMOGEN 的推理效率与同类方法相当。

### 补充图表

![[assets/figures/papers/paper_list_l1857_EnergyMoGen_Compositional_Human_Motion_Generation_with_Energy_Based_Diff/figures/012_Table_7.jpg]]
*Table 7: Ablation of hyper-parameters in Synergistic Energy Fusion on MTT [50]. We find that as the weight of*

![[assets/figures/papers/paper_list_l1857_EnergyMoGen_Compositional_Human_Motion_Generation_with_Energy_Based_Diff/figures/013_Table_8.jpg]]
*Table 8: Study on the number of latent vectors in motion VAE on the HumanML3D [19] test set*

![[assets/figures/papers/paper_list_l1857_EnergyMoGen_Compositional_Human_Motion_Generation_with_Energy_Based_Diff/figures/014_Table_9.jpg]]
*Table 9: Ablation of step size in Adaptive Gradient Descent on MTT [50]*



## 定位与知识库关联

### 1. 方法谱系：从骨架扩散到潜在空间能量组合

ENERGYMOGEN 处于文本驱动人体动作生成（text-to-motion generation）这一快速演进的方法谱系中。该领域的核心范式经历了从骨架空间扩散模型到潜在空间扩散模型的迁移，而 ENERGYMOGEN 在此基础上进一步引入了能量模型（EBM）视角，开辟了组合动作生成的新路径。

**骨架空间扩散模型**构成了早期基线。**MDM** 首次将扩散模型应用于人体动作生成，直接在原始骨架表示上进行去噪。**MotionDiffuse** 引入了文本驱动的细粒度控制，**ReMoDiffusion** 则通过检索增强机制提升了生成质量。**FineMoGen** 借助时空注意力进一步优化了动作的时空一致性。这些方法在单文本生成任务上表现强劲，但均不具备组合多个语义概念的能力——其推理过程仅接受单一文本条件，无法对“走路并挥手”这类合取概念进行显式建模。

**潜在空间扩散模型**通过将动作压缩到低维潜在空间来降低计算开销。**MLD** 率先采用这一范式，**MotionMamba** 则用 Mamba 架构替代了 Transformer 作为去噪骨干。然而，潜在扩散模型面临一个结构性瓶颈：动作被编码为固定数量（如 N=5）的潜在向量，这些向量与具体动作帧之间缺乏显式对应关系。这使得逐帧的组合操作在潜在空间中无法直接实现，成为组合生成的根本障碍。

**组合动作生成**方向的工作相对稀缺。**PriorMDM** 是少数直接处理组合生成的基线，但其方法仍局限于骨架空间，且组合机制较为初步。ENERGYMOGEN 的关键突破在于将扩散模型的去噪过程重新解释为基于能量的朗之万动力学采样——去噪步等价于能量函数梯度下降的一个特例（η=1）。这一视角的转换带来了一个核心能力：**能量函数的可加性**。通过合取算子（累加各概念条件分数与无条件分数的差异）和否定算子（减去指定概念的条件分数），ENERGYMOGEN 可以在不重新训练模型的情况下，将多个简单概念的能量项组合成复杂动作的生成分布。

### 2. 知识库定位：双谱系能量模型与协同融合

ENERGYMOGEN 的知识贡献可定位于三个相互关联的模块，它们共同构成了潜在空间中的可组合生成框架。

**潜在感知能量模型（Latent-aware EBM）** 将去噪网络本身视为能量函数。其核心操作是分类器无关引导（classifier-free guidance）的泛化：对于概念集合 C={c₁,...,cₙ}，合取组合的分数为：

$$\epsilon_\theta^l(z_t, t, \mathbb{C}) = \epsilon_\theta(z_t, t) + \sum_{i=1}^n w_i^l (\epsilon_\theta(z_t, t, \pmb{c}_i) - \epsilon_\theta(z_t, t))$$

否定组合则通过减法实现：

$$\epsilon_\theta^l(z_t, t, \mathbb{C}) = \epsilon_\theta(z_t, t) + w^l (\epsilon_\theta(z_t, t, c_i) - \epsilon_\theta(z_t, t, c_j))$$

这一谱系的优势在于能够保持动作的物理平滑性，但单独使用时文本一致性较弱——因为能量操作发生在潜在向量的全局层面，缺乏对语义细节的细粒度感知。

**语义感知能量模型（Semantic-aware EBM）** 将交叉注意力操作重新解释为能量函数。其核心创新是能量化交叉注意力与自适应梯度下降（AGD）：将文本嵌入 c 的更新建模为基于 MAP 估计的梯度下降过程，梯度由注意力映射项和正则化项组成：

$$\nabla_{\mathcal{K}} \log p(\mathcal{K}|\mathcal{Q}) = \left[ \operatorname{SFM}(\alpha K \mathcal{Q}^{\top}) \mathcal{Q} - \mathcal{M}(\operatorname{SFM}(\mathcal{K}')) \mathcal{K} \right] W_K$$

$$\hat{\pmb{c}} = \pmb{c} + \gamma \nabla_{\pmb{K}} \log p(\pmb{K}|\pmb{Q})$$

该谱系通过交叉注意力层面的特征加权平均实现多概念融合，显著提升了文本一致性（R-Precision Top1 提升 1.3%，Top3 提升 0.9%），但单独使用时容易引入脚步滑动和动作抖动——物理脚接触分数（PFC）在语义单独模式下为 1.05，表明明显的足部滑移问题。

**协同能量融合（SEF）** 是连接两个谱系的桥梁。最终的去噪分数通过线性加权融合三种预测：

$$\hat{\epsilon}_\theta(z_t, t, \mathbb{C}, \mathbf{c}_{1,n}) = \lambda_l \epsilon_\theta^l(z_t, t, \mathbb{C}) + \lambda_s \epsilon_\theta^s(z_t, t, \mathbb{C}) + \lambda_m \epsilon_\theta(z_t, t, \mathbf{c}_{1,n})$$

其中 λₗ 控制潜在感知组合的权重（影响动作平滑度），λₛ 控制语义感知组合的权重（影响文本一致性），λₘ 控制多概念联合文本的权重。实验确定的最优配置为 λₗ=0.1, λₛ=0.7, λₘ=0.2，此时 PFC 降至 0.51，表明协同融合有效缓解了语义单独模式下的物理失真问题。

### 3. 适用边界与关键局限

ENERGYMOGEN 的组合生成能力存在明确的适用边界：

**训练分布内的组合泛化**。该方法的核心机制是在预训练模型的能量函数上进行代数操作，而非学习新的生成能力。这意味着它擅长组合训练中已见的概念（如“走路”+“挥手”），但无法处理完全新颖的概念对——Figure 8 的失败案例直接展示了这一局限。

**固定数量潜在向量的结构约束**。由于动作 VAE 将任意长度动作压缩为固定 N 个潜在向量，逐帧的组合操作在架构层面不可行。当前的组合只能通过能量函数对整体潜在向量进行全局操作，无法实现“前 30 帧走路、后 30 帧跑步”这类时序组合。这是潜在扩散模型相对于骨架空间方法的固有折衷。

**语义对齐与物理真实性的张力**。SEF 的超参数调优揭示了一个根本性的权衡：增大 λₛ 提升文本一致性（R-Precision 和 TMR-Score 上升），但以动作平滑度为代价（Transition distance 增大）；增大 λₗ 则相反。当前的手动设定（λₗ=0.1, λₛ=0.7）是一个经验折衷，而非自适应解。

**生成多样性的局部劣势**。在 HumanML3D 基准上，ENERGYMOGEN 的 FID 仍高于 ReMoDiffusion，表明其生成分布与真实分布的差距尚未在所有维度上超越最强基线。

### 4. 开放问题

1. **潜在-帧对应关系的建立**：能否在潜在扩散模型中引入结构化潜在编码（如时序位置编码），使每个潜在向量显式对应特定帧段，从而支持逐帧的组合操作？这将从根本上突破当前“全局操作”的限制。

2. **逻辑操作的扩展**：当前的能量组合仅支持合取与否定。能否将框架扩展到异或、顺序组合（“先 A 后 B”）、条件组合（“如果 A 则 B”）等更复杂的逻辑操作？这需要重新设计能量函数的代数结构。

3. **自适应融合权重的学习**：当前 λₗ、λₛ、λₘ 是手动设定的全局超参数。能否通过元学习或强化学习，根据输入概念集合的特征动态调节融合系数？这将缓解语义-物理的固定折衷。

4. **更大规模组合数据的泛化验证**：当前组合生成评估主要在 MTT 数据集上进行，其概念组合的规模和多样性有限。该方法在更大规模、更复杂的组合动作数据集上的泛化能力尚待验证。

5. **语义感知组合的物理约束注入**：能否在语义感知的能量函数中显式嵌入物理约束（如足部接触、关节限制），从梯度层面抑制脚步滑动和动作抖动，而非仅依赖 SEF 的事后融合？



## 原文 PDF

![[paperPDFs/CVPR_2025/EnergyMoGen_Compositional_Human_Motion_Generation_with_Energy_Based_Diffusion_Model_in_Latent_Space.pdf]]
