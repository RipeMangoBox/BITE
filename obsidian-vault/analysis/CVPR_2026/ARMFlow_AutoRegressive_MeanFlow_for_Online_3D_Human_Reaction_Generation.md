---
title: "ARMFlow: AutoRegressive MeanFlow for Online 3D Human Reaction Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ARMFlow_AutoRegressive_MeanFlow_for_Online_3D_Human_Reaction_Generation.pdf
project_link: null
code_link: "https://github.com/ZenGengChin/armflow"
aliases:
- ARMFlow
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 全局因果上下文编码器（完整历史）结合BSCE训练策略，使模型在单步推理中既能利用全局长程信息，又能抑制自回归误差累积。
primary_logic: 利用MeanFlow的单步生成特性，构建因果上下文编码器以保留全局语义，并通过BSCE训练强制模型适应生成历史，从而在实时在线环境下实现高保真、高一致的反应生成。
claims:
- ARMFlow的在线单步生成在InterHuman和InterX数据集上的FID指标比现有在线方法提升约30%，且与离线SOTA性能相当。
- BSCE训练策略显著优于传统的真实上下文编码（GTE）和HumanX的渐进滚动策略，有效抑制了自回归误差累积。
- 因果上下文编码器通过因果掩码编码完整运动历史，避免了固定窗口导致的信息丢失，保证了长期语义一致性。
- InterHuman (online) 上 FID↓ = 2.178±.054
---

# ARMFlow: AutoRegressive MeanFlow for Online 3D Human Reaction Generation

> [!tip] 核心洞察
> 利用MeanFlow的单步生成特性，构建因果上下文编码器以保留全局语义，并通过BSCE训练强制模型适应生成历史，从而在实时在线环境下实现高保真、高一致的反应生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | ARMFlow：面向在线3D人体反应生成的自回归均值流 |
| 英文题名 | ARMFlow: AutoRegressive MeanFlow for Online 3D Human Reaction Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.16234) · [Code](https://github.com/ZenGengChin/armflow) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | ARMFlow |
| Dataset | InterHuman, InterX |

> [!tip] 效果简介
> - InterHuman (online) 上，FID↓ 2.178±.054 vs 3.029±.077 (ReGenNet) (约-0.851（相对提升28%）)；R-Precision@1↑ 0.441±.005 vs 0.393±.005 (ReGenNet) (+0.048)。
> - InterX (online) 上，FID↓ 0.042±.003 vs 0.093±.005 (ReGenNet) (-0.051)。
> - InterHuman (offline, ReMFlow) 上，FID↓ 2.433±.042 vs 2.930±.033 (ReGenNet) (-0.497)。

## 概要

**核心问题**：在线3D人体反应生成需要在实时交互中，根据演员动作即时生成反应者的运动序列。现有方法面临一个根本性瓶颈——难以同时满足高保真度、低延迟和长程上下文一致性。固定窗口上下文编码（如**ReGenNet**，Xu et al., CVPR 2024）导致历史信息丢失和语义漂移；而多步扩散或流匹配模型（如**CAMDM**，Chen et al., ACM SIGGRAPH 2024；**HumanX**，Ji et al., arXiv 2025）的计算成本高昂，限制了实时性能。

**核心方法**：本文提出**ARMFlow**（AutoRegressive MeanFlow），将MeanFlow的单步生成特性与自回归框架结合。其关键设计包括：（1）基于DiT的全局因果上下文编码器，通过因果掩码编码完整运动历史，避免固定窗口的信息丢失；（2）轻量级MLP速度预测器，实现单步推理生成；（3）Bootstrap Contextual Encoding（BSCE）训练策略，在训练阶段用模型自身生成的历史替代真实历史，有效抑制自回归误差累积。

**方法定位**：ARMFlow在生成范式上区别于多步扩散方法，采用MeanFlow的单步平均速度预测；在上下文建模上区别于固定窗口编码，引入全历史因果编码；在训练策略上区别于真实历史编码（GTE）和渐进滚动（HumanX），提出BSCE自举式训练。这一组合使ARMFlow成为首个同时满足在线、实时、长上下文和自回归四个维度的人体反应生成方法。

**主要结果**：在InterHuman和InterX数据集上，ARMFlow的在线单步生成在FID指标上比现有在线方法提升约30%，且性能与离线SOTA相当。具体而言，在InterHuman在线设定下FID达到2.178，对比ReGenNet的3.029（相对提升28%）；在InterX上FID为0.042，对比ReGenNet的0.093。BSCE训练策略在消融实验中显著优于GTE和HumanX的渐进滚动策略，验证了其对自回归误差累积的抑制效果。

### 问题背景：在线3D人体反应生成

在虚拟现实、人机交互和社交机器人等场景中，智能体需要根据人类动作实时生成自然、语义一致的反应动作。这一任务被称为**在线3D人体反应生成**（Online 3D Human Reaction Generation），其核心挑战在于：模型必须在接收到演员动作的每个时间步立即输出反应动作，而不能等待完整序列。这要求方法同时满足三个相互制约的目标——**高保真度**（动作质量与多样性）、**低延迟**（实时推理）和**长程上下文一致性**（反应与历史行为保持语义连贯）。

### 现有方法的瓶颈

当前主流方法在解决上述三元悖论时面临两个关键瓶颈：

**瓶颈一：固定窗口上下文导致语义漂移。** 多数在线方法（如基于扩散模型的**ReGenNet**（Xu et al., CVPR 2024）和自回归扩散模型**CAMDM**（Chen et al., ACM SIGGRAPH 2024））仅编码固定长度的历史窗口作为条件输入。当交互序列超出窗口长度时，早期语义信息被截断，导致反应与全局上下文脱节——例如长时间交互后出现动作语义不匹配或穿透现象。**R2R**（Cen et al., ICLR 2025）虽尝试编码全历史，但其设计并未与高效生成范式深度耦合。

**瓶颈二：多步生成范式限制实时性能。** 扩散模型和流匹配（Flow Matching）方法通常需要多次推理步骤（如DDIM的数十步迭代）才能生成单帧反应，这在高帧率在线场景中造成显著延迟。即便**HumanX**（Ji et al., arXiv 2025）等实时自回归扩散方法通过渐进滚动策略优化了推理效率，其本质仍依赖多步去噪，计算成本限制了大规模部署。

### 本文动机

上述瓶颈的根源在于：**现有方法将“长程上下文建模”与“单步高效生成”视为不可兼得的对立目标**。本文的核心动机是打破这一假设——通过引入**MeanFlow**的单步生成特性，结合**因果上下文编码器**保留全局语义，并设计**BSCE训练策略**抑制自回归误差累积，从而在实时在线环境下实现高保真、高一致的反应生成。具体而言，ARMFlow在InterHuman和InterX数据集上的在线单步生成FID指标比现有在线方法提升约30%，且与离线SOTA性能相当（见Table 2），验证了该技术路线的可行性。

## 核心方法与创新机理

ARMFlow 的核心创新围绕一个关键矛盾展开：**在线人体反应生成需同时满足高保真、低延迟与长程语义一致性，而现有方法在这三者之间难以兼得**。固定窗口上下文导致信息丢失和语义漂移，多步扩散/流模型则带来高昂的计算成本，限制了实时性能。ARMFlow 通过三个相互耦合的“changed slots”系统性地解决了这一瓶颈，其因果链条可概括为：**以 MeanFlow 的单步生成特性为效率基础，以全局因果上下文编码器为语义保障，以 BSCE 训练策略为自回归鲁棒性支撑**。

### 从多步生成到单步 MeanFlow：效率与保真度的基础

现有在线方法普遍依赖多步扩散或流匹配模型（如 ReGenNet 基于 DDIM，CAMDM 基于自回归扩散，HumanX 基于实时自回归扩散），每次生成需数十步推理，延迟通常在 35–78 ms 以上（Figure 1）。ARMFlow 将生成范式切换为 **MeanFlow**——一种建模轨迹全局平均速度的单步生成框架。MeanFlow 的核心思想是将从噪声到数据的整个扩散路径压缩为一次速度预测：

$$u ( z _ { t } , r , t ) = \frac { 1 } { t - r } \int _ { r } ^ { t } v ( z _ { \tau } , \tau ) d \tau$$

模型直接预测该平均速度 $u_\theta$，并通过单步积分从 $r=0$（纯噪声）到 $t=1$（数据）生成样本。训练目标为：

$$\mathcal { L } ( \theta ) = \mathbb { E } \big \| u _ { \theta } ( z _ { t } , r , t ) - \mathrm { s g } ( u _ { \mathrm { t g t } } ) \big \| _ { 2 } ^ { 2 }$$

这一范式转换使得 ARMFlow 在每次在线推理时仅需**一次前向传播**，从根本上解决了实时性瓶颈。同时，MeanFlow 本身在建模能力上并不逊色——配合 DiT 骨干网络和 CFG（Classifier-Free Guidance）训练，其离线版本 ReMFlow 在 InterHuman 和 InterX 数据集上的 FID 已超越现有离线 SOTA（Table 3），为在线版本提供了坚实的质量基础。

### 全局因果上下文编码器：打破固定窗口的信息瓶颈

效率问题解决后，在线生成的真正难点在于**如何在仅看历史信息的约束下保持长期语义一致性**。现有方法或完全不编码历史，或仅使用固定窗口的历史片段（如 HumanX），这导致窗口外的交互信息永久丢失，在长序列中产生语义漂移。

ARMFlow 的应对方案是引入**基于 DiT 的因果上下文编码器**（DiT Context Encoder），用因果掩码（causal masking）编码**完整的运动历史**。该编码器接收 CNN-VAE 压缩后的演员与反应者隐变量序列，以及通过 CLIP 文本编码器注入的语义条件，输出一个融合了全局长程交互信息的上下文表示。因果掩码保证了每个时间步只能访问当前及过去的信息，满足在线约束；而完整历史的编码则防止了信息截断，使得模型能够捕捉远距离的交互依赖（如“演员先挥手，反应者数秒后才躲避”的长程因果链）。

### BSCE 训练策略：对抗自回归误差累积的“免疫接种”

拥有全局上下文编码器后，自回归生成仍面临一个经典困境：训练时模型看到的是真实历史（Ground-Truth Encoding, GTE），而推理时只能使用自己生成的历史，这种分布偏移会导致误差逐步累积。HumanX 提出的渐进滚动（Rollout）策略部分缓解了这一问题，但 ARMFlow 的实验表明其效果仍不理想。

ARMFlow 的 **BSCE（Bootstrap Contextual Encoding）** 策略采取了更激进的方案：**从训练一开始就用模型自身生成的历史替换真实历史**，并逐步增加自回归的迭代次数。这相当于让模型在训练阶段就“接种”了生成误差的疫苗，迫使上下文编码器和速度预测器学会在噪声输入下保持鲁棒。消融实验（Table 6）证实，BSCE 在在线设定下的 FID、R-Precision 等指标上显著优于 GTE 和 Rollout 策略，是 ARMFlow 在线性能接近离线水平的关键因素。

### 创新协同：为什么三个 slot 缺一不可

这三个 changed slot 形成了紧密的因果闭环：**MeanFlow 提供了单步生成的效率基础，使得因果上下文编码器可以在不增加延迟的前提下处理完整历史；BSCE 则为这一自回归架构提供了误差抑制机制，确保长程上下文信息不会被累积误差污染**。消融实验（Table 4）表明，移除因果上下文编码或 BSCE 均会导致在线性能显著下降，验证了各模块的必要性。

值得注意的是，这一设计也存在固有局限：由于 MeanFlow 的单步特性，模型不支持事后分类器引导（post-hoc classifier guidance），无法在生成后对结果进行基于优化的细化修正；此外，当前实现未提供弹性延迟处理机制，在多代理交互场景下可能产生轻微异步行为。这些限制指向了未来工作的潜在方向，但并不削弱 ARMFlow 在“效率-保真度-一致性”三角矛盾中所取得的突破。

ARMFlow的整体架构围绕“单步生成 + 全局因果上下文”这一核心思想构建，通过三个关键模块的协同，实现在线3D人体反应生成的高保真度与低延迟。图2展示了完整的pipeline。

### 运动压缩：CNN-VAE隐空间编码

原始的人体运动序列维度高、时序依赖复杂。ARMFlow首先利用一个**CNN-VAE**将演员（actor）和反应者（reactor）的运动序列压缩到连续隐空间，降低后续建模的计算负担，同时保留时序结构。VAE的编码器采用与T2M-GPT相同的设计：隐藏维度256，两个残差卷积下采样块，每块三个隐藏层。其训练目标为标准的证据下界（ELBO），结合重构对数似然与KL散度正则项：

$$\mathcal { L } _ { \mathrm { V A E } } = \mathbb { E } _ { q ( \boldsymbol { z } | \boldsymbol { x } ) } [ \log p ( \boldsymbol { x } | \boldsymbol { z } ) ] - \mathrm { K L } ( q ( \boldsymbol { z } | \boldsymbol { x } ) \| p ( \boldsymbol { z } ) )$$

其中先验 $p(\boldsymbol{z})$ 为标准高斯分布。压缩后的隐变量成为后续生成模块的输入。

### 生成核心：MeanFlow单步预测范式

ARMFlow的生成能力建立在**MeanFlow**框架之上。与需要多步去噪的扩散模型（如DDIM）或流匹配模型不同，MeanFlow直接建模从纯噪声（$r=0$）到数据（$t=1$）整个轨迹上的**平均速度** $u(z_t, r, t)$：

$$u ( z _ { t } , r , t ) = \frac { 1 } { t - r } \int _ { r } ^ { t } v ( z _ { \tau } , \tau ) d \tau$$

训练时，模型以目标平均速度 $u_{\mathrm{tgt}}$ 作为监督信号，通过均方误差进行优化：

$$\mathcal { L } ( \theta ) = \mathbb { E } \big \| u _ { \theta } ( z _ { t } , r , t ) - \mathrm { s g } ( u _ { \mathrm { t g t } } ) \big \| _ { 2 } ^ { 2 }$$

这一设计的直接收益是：推理时仅需**单步积分**即可从噪声生成完整运动片段，从根本上消除了多步扩散模型的高延迟瓶颈。图1的对比显示，ARMFlow每步仅需单次推理，而ReGenNet需35–78 ms、CAMDM需45 ms。

### 在线生成：因果上下文编码器 + MLP速度预测器

ARMFlow的在线生成模块包含两个子组件，遵循MAR的架构精神：

1. **DiT因果上下文编码器**：基于DiT backbone（512隐藏维度，7层Transformer，8个注意力头，带跳跃连接），通过**因果掩码**编码完整的运动历史。与固定窗口上下文（如HumanX）不同，因果掩码确保每个时刻只能看到过去的信息，同时保留全部历史，避免了窗口外信息丢失导致的语义漂移。文本条件通过CLIP文本编码器提取后，与时间步嵌入融合为全局条件向量，经自适应层归一化（AdaLN）注入DiT。

2. **MLP速度预测器**：轻量级MLP网络，接收上下文编码器输出的全局条件表示和当前隐变量，直接预测平均速度，实现单步生成。CFG（无分类器引导）通过速度混合公式控制条件强度：

   $$\tilde { v } _ { t } = \omega v _ { t } + ( 1 - \omega ) u _ { \theta } ^ { \mathrm { c f g } } ( z _ { t } , t , t )$$

### 训练策略：BSCE自举上下文编码

自回归生成的核心难点是误差累积——训练时使用真实历史（GTE），推理时却使用生成历史，导致分布偏移。ARMFlow提出**BSCE（Bootstrap Contextual Encoding）**策略：从训练初期就用模型自身生成的运动片段替换演员和反应者的历史，并逐步增加自回归迭代次数。这使得上下文编码器在训练阶段就适应了生成历史的质量特征，显著抑制了在线推理中的误差累积。消融实验（Table 6）证实，BSCE在在线设定下明显优于GTE和HumanX的渐进滚动策略。

### 离线变体：ReMFlow

作为ARMFlow的离线对应版本，ReMFlow同样基于DiT backbone和MeanFlow范式，但无需因果掩码和自回归机制，可直接利用完整序列进行双向注意力建模。两者共享CNN-VAE隐空间和DiT基础架构，保证了在线/离线场景下的方法一致性。

![[assets/figures/papers/paper_list_l962_https_arxiv_org_abs_2512_16234/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the proposed architecture for online and offline reaction generation. The framework consists of a CNN-based encoder to learn a compact latent space for the actor and the reactor. The ReMFlow is for offline generation based on the DiT architecture, and ARMFlow is the autoregressive online model consisting of a DiT context encoder and an MLP velocity predictor. A BSCE strategy is employed during online training progressively to reduce accumulated error in the autoregression*

ARMFlow 的整体架构由四个核心模块构成，围绕 MeanFlow 单步生成范式组织，如图 Figure 2 所示。

### 3.1 MeanFlow 单步生成范式

传统扩散/流匹配模型需要多步采样才能从噪声生成数据，这直接限制了在线场景的实时性。ARMFlow 采用 MeanFlow 框架，其核心思想是直接建模从噪声到数据的**平均速度**，从而将生成过程压缩为单步积分。

定义从时间 `r` 到 `t` 的平均速度：

$$u ( z _ { t } , r , t ) = \frac { 1 } { t - r } \int _ { r } ^ { t } v ( z _ { \tau } , \tau ) d \tau$$

其中 `v(z_τ, τ)` 是瞬时速度场。通过预测该平均速度 `u_θ`，模型可以从 `r=0`（纯噪声）到 `t=1`（数据）进行单步积分生成样本，避免了多步迭代的计算开销。

训练目标为预测速度与目标速度之间的 L2 损失：

$$\mathcal { L } ( \theta ) = \mathbb { E } \big \| u _ { \theta } ( z _ { t } , r , t ) - \mathrm { s g } ( u _ { \mathrm { t g t } } ) \big \| _ { 2 } ^ { 2 }$$

其中目标速度 `u_tgt` 通过莱布尼茨规则导出：

$$u _ { \mathrm { t g t } } = v ( z _ { t } , t ) - ( t - r ) \big ( v ( z _ { t } , t ) \partial _ { z } u _ { \theta } + \partial _ { t } u _ { \theta } \big )$$

为增强条件控制鲁棒性，引入无分类器引导（CFG），训练目标扩展为：

$$\mathcal { L } ( \theta ) = \mathbb { E } \big \lVert u _ { \theta } ^ { \mathrm { c f g } } ( z _ { t } , r , t \mid c ) - \mathrm { s g } ( u _ { \mathrm { t g t } } ) \big \rVert _ { 2 } ^ { 2 }$$

推理时通过速度混合公式调节条件信号强度（`ω` 为引导权重）：

$$\tilde { v } _ { t } = \omega v _ { t } + ( 1 - \omega ) u _ { \theta } ^ { \mathrm { c f g } } ( z _ { t } , t , t )$$

### 3.2 CNN-VAE 运动压缩

原始人体运动序列维度高、时序依赖复杂。ARMFlow 首先使用 CNN-VAE 将演员和反应者的运动序列压缩到连续隐空间，降低后续模块的计算负担。

VAE 的损失函数为：

$$\mathcal { L } _ { \mathrm { V A E } } = \mathbb { E } _ { q ( \boldsymbol { z } | \boldsymbol { x } ) } [ \log p ( \boldsymbol { x } | \boldsymbol { z } ) ] - \mathrm { K L } ( q ( \boldsymbol { z } | \boldsymbol { x } ) \| p ( \boldsymbol { z } ) )$$

其中第一项为重构对数似然，第二项为隐变量后验分布与标准高斯先验 `p(z)` 之间的 KL 散度正则项。编码器采用隐藏维度 256、两个残差卷积下采样块、每块三层隐藏层的结构设计（参见 Implementation Details）。

### 3.3 DiT 因果上下文编码器

在线生成的核心挑战是如何高效利用运动历史。现有方法多采用**固定窗口历史编码**（如 HumanX），窗口外的信息被直接丢弃，导致长程语义漂移。

ARMFlow 采用基于 DiT 的**因果上下文编码器**，通过因果掩码（causal masking）编码完整的运动历史序列。该设计确保当前时刻的生成仅依赖过去信息，同时保留了全局时间语义。文本提示通过 CLIP 文本编码器提取特征，与时间步嵌入融合为全局条件向量，经自适应层归一化（AdaLN）注入 DiT 各层。

### 3.4 MLP 速度预测器

在上下文编码器提取全局条件表示后，ARMFlow 使用一个轻量级 MLP 网络作为速度预测器。该 MLP 以当前隐变量和上下文条件为输入，直接输出预测的平均速度，实现单步生成。相比 DiT 骨干网络，MLP 预测器在保持表达能力的同时显著降低了推理延迟。

### 3.5 BSCE 自回归训练策略

自回归生成的核心难点是**误差累积**：训练时使用真实历史（Ground-Truth Encoding, GTE），推理时却必须使用模型自身生成的历史，二者分布不匹配导致误差逐步放大。

BSCE（Bootstrap Contextual Encoding）策略从训练初期就用模型生成的历史替换真实历史，并逐步增加自回归迭代次数。这与 HumanX 的渐进滚动（Rollout）策略形成对比——BSCE 在训练起始阶段即引入生成历史，使模型更早适应自回归推理的分布偏移。消融实验（Table 6）证实 BSCE 在 FID 等指标上显著优于 GTE 和 Rollout 策略。

## 实验与关键发现

### 实验设置与评估协议

所有实验均在公开的 **InterHuman** 和 **InterX** 数据集上进行，采用统一的数据划分和评估协议。在线生成设定下，模型在每一时间步仅接收当前及历史观测，需实时输出反应动作；离线设定则允许访问完整序列。评估指标涵盖生成质量（**FID↓**）、语义对齐（**R-Precision@1↑**）、动作多样性（**Diversity→**）以及肢体接触合理性（**Penetration↓**）等维度。

### 在线生成主结果

ARMFlow 在在线设定下展现出显著优势。如 Table 2 所示，在 InterHuman 数据集上，ARMFlow 的 FID 达到 **2.178±.054**，相比最强在线基线 ReGenNet（3.029±.077）相对提升约 28%，相比同样采用全历史编码的 R2R 也有明显优势。在 InterX 数据集上，ARMFlow 的 FID 进一步降至 **0.042±.003**，远超 ReGenNet（0.093±.005）和 HumanX（0.135±.005）。语义对齐指标 R-Precision@1 同样领先：InterHuman 上达到 **0.441±.005**（ReGenNet 为 0.393±.005），验证了因果上下文编码器对全局语义一致性的有效保留。

![[assets/figures/papers/paper_list_l962_https_arxiv_org_abs_2512_16234/figures/004_Table_2.jpg]]
*Table 2: Comparison of online methods on InterHuman and InterX datasets*

Table 1 从能力维度对比了当前主流方法：ARMFlow 是唯一同时满足**在线、实时、长上下文建模、自回归生成**四项要求的方法。ReGenNet 和 CAMDM 虽支持在线生成，但依赖多步扩散推理，实时性能受限；HumanX 通过渐进滚动策略实现实时自回归，但固定窗口上下文导致信息丢失；R2R 虽编码完整历史，却未采用自回归范式。

![[assets/figures/papers/paper_list_l962_https_arxiv_org_abs_2512_16234/figures/002_Table_1.jpg]]
*Table 1: Current reaction generation models. AR: Autoregression*

### 离线生成主结果

在离线设定下，ARMFlow 的对应版本 **ReMFlow** 同样表现优异。Table 3 显示，ReMFlow 在 InterHuman 上的 FID 为 **2.433±.042**，优于 ReGenNet（2.930±.033）和 InterMask（3.453±.034）；在 InterX 上 FID 为 **0.058±.005**，同样领先。值得注意的是，ARMFlow 的在线性能（FID 2.178）甚至超越了 ReMFlow 的离线性能（FID 2.433），表明 BSCE 训练策略不仅弥补了在线-离线差距，还带来了额外的生成质量增益。

![[assets/figures/papers/paper_list_l962_https_arxiv_org_abs_2512_16234/figures/005_Table_3.jpg]]
*Table 3: Comparison of offline methods on InterHuman and InterX datasets*

### 定性分析

Figure 3 展示了 ARMFlow 与 ReGenNet 在 InterHuman 数据集上的定性对比。红色虚线标注了 ReGenNet 生成结果中的典型失败模式：肢体穿透（penetration）和语义错位（如演员挥手但反应者未做出相应避让）。ARMFlow 在相同场景下生成了物理合理、语义一致的反应动作（绿色虚线标注），验证了因果上下文编码器在长程交互建模中的优势。

![[assets/figures/papers/paper_list_l962_https_arxiv_org_abs_2512_16234/figures/006_Figure_3.jpg]]
*Figure 3: Qualitative comparison with ReGenNet on InterHuman dataset. The problematic interactions are marked with red dashed lines, including penetrations and semantic misalignment, and the correct ones are marked with green*

### 消融实验

**训练策略消融。** Table 6 对比了三种自回归训练策略：真实上下文编码（GTE）、HumanX 的渐进滚动策略（Rollout）以及本文提出的 BSCE。结果表明，BSCE 在所有指标上显著优于前两者。GTE 由于训练-推理不一致导致严重的误差累积；Rollout 虽引入生成历史，但渐进式增加迭代次数的方式收敛缓慢。BSCE 从训练初期即用模型自身生成的历史替换真实历史，使模型充分适应自回归误差分布，从而在在线推理时保持鲁棒。

**模块消融。** Table 4（在线）和 Table 5（离线）分别验证了各模块的必要性。移除因果上下文编码器后，模型退化为无历史条件生成，FID 显著上升；移除 BSCE 策略后，在线性能大幅下降，表现为动作抖动和语义漂移。离线消融中，去除 DiT 的文本条件注入或 AdaLN 归一化同样导致生成质量下降，证实了多模态条件融合设计的有效性。

### 推理效率

ARMFlow 的核心效率优势源于 MeanFlow 的单步生成特性。如 Figure 1 所示，ARMFlow 每实时步仅需一次推理，而 ReGenNet 需 35-78 ms 的多步扩散，CAMDM 需约 45 ms。单步推理使 ARMFlow 在保持高保真度的同时满足实时交互的延迟要求，为在线人机交互场景提供了可行方案。

### 局限与失败模式

尽管 ARMFlow 在主要指标上表现优异，仍存在两个已知局限：（1）当前实现未提供自回归小窗口的弹性延迟处理机制，在多代理交互时可能产生轻微异步行为；（2）MeanFlow 的单步生成特性使其不支持事后分类器引导（post-hoc classifier guidance），无法对已生成结果进行基于优化的细化修正。在需要精细约束控制的应用场景中，这一限制需要额外关注。

![[assets/figures/papers/paper_list_l962_https_arxiv_org_abs_2512_16234/figures/007_Table_4.jpg]]
*Table 4: Ablation study for online generation on methods*

## 定位与知识库关联

### 1. 方法谱系：从离线扩散到在线单步生成

ARMFlow 的提出建立在两条方法脉络的交汇处：**人体运动生成中的扩散/流模型**与**在线自回归生成架构**。

**离线生成基线。** 在人体反应生成领域，早期工作以离线范式为主，即给定完整的演员运动序列，一次性生成完整的反应者序列。代表性方法包括：
- **ReGenNet** (Xu et al., CVPR 2024)：基于扩散模型的离线反应生成方法，采用多步去噪过程，推理需 35–78 ms/步。
- **InterMask** (Javed et al., ICLR 2025)：基于掩码建模的离线方法，通过掩码预测实现运动生成。

ARMFlow 的离线版本 **ReMFlow** 直接与上述方法对比。在 InterHuman 数据集上，ReMFlow 的 FID 为 2.433±.042，优于 ReGenNet 的 2.930±.033 和 InterMask 的 3.453（Table 3），验证了 MeanFlow 单步生成范式在离线场景下的竞争力。

**在线生成基线。** 在线生成要求模型在每个时间步根据已观测的历史生成下一帧反应，对延迟和上下文一致性提出更高要求：
- **ReGenNet** (Xu et al., CVPR 2024)：虽为离线设计，但在在线设定中通过滑动窗口方式运行，成为主要对比基线。
- **CAMDM** (Chen et al., ACM SIGGRAPH 2024)：自回归扩散模型，每步需约 45 ms 推理。
- **HumanX** (Ji et al., arXiv 2025)：实时自回归扩散方法，引入渐进滚动（Rollout）策略缓解误差累积。
- **R2R** (Cen et al., ICLR 2025)：全历史编码的在线方法，通过编码完整交互历史保持长程一致性。

ARMFlow 在在线设定下与上述方法全面对比（Table 2），在 InterHuman 上 FID 达 2.178±.054，较 ReGenNet 的 3.029±.077 相对提升约 28%，较 R2R 亦有显著优势。

### 2. 核心改进槽位：三个关键设计选择

ARMFlow 相对于基线方法的改进可归纳为三个“可替换槽位”，每个槽位对应一个具体的设计决策：

**槽位一：上下文编码架构（固定窗口 → 全局因果编码）。** 现有在线方法普遍采用固定窗口编码历史（如 HumanX）或无历史编码，导致窗口外的语义信息丢失，引发长程语义漂移。ARMFlow 引入基于 DiT 的**因果上下文编码器**，通过因果掩码编码完整运动历史，在保持自回归因果性的前提下保留全局时序语义。这一设计使模型在生成当前帧时能“看到”从交互开始到当前时刻的全部历史，从根本上解决了信息截断问题。

**槽位二：生成范式（多步扩散/流匹配 → MeanFlow 单步预测）。** 扩散模型和传统流匹配模型需要多步迭代推理（通常 10–50 步），计算成本高，难以满足在线实时需求。ARMFlow 采用 **MeanFlow** 框架，直接建模从噪声到数据的平均速度 $u(z_t, r, t) = \frac{1}{t-r} \int_r^t v(z_\tau, \tau) d\tau$，实现真正的单步生成。推理时仅需一次前向传播，延迟大幅降低（Figure 1 展示了与 ReGenNet 35–78 ms、CAMDM 45 ms 的对比优势）。

**槽位三：自回归训练策略（真实历史编码 → BSCE）。** 自回归模型的标准训练方式使用真实历史作为上下文（Ground-Truth Encoding, GTE），但推理时模型接收的是自身生成的历史，导致训练-推理分布偏移，误差逐步累积。HumanX 提出的 Rollout 策略部分缓解了这一问题，但仍保留真实历史作为初始上下文。ARMFlow 提出的 **Bootstrap Contextual Encoding (BSCE)** 从训练初期就用模型自身生成的历史替换真实历史，并逐步增加自回归迭代次数，强制模型学会在“不完美历史”条件下生成。消融实验（Table 6）表明，BSCE 在在线设定下显著优于 GTE 和 Rollout 策略。

### 3. 知识库定位：在自回归生成与流模型交叉点的贡献

ARMFlow 的核心贡献在于将 **MeanFlow 的单步生成能力**与**自回归在线推理**有机结合，并通过因果编码和 BSCE 训练策略解决了这一结合带来的挑战。其在知识库中的定位可概括为：

- **相对于扩散/流模型文献**：ARMFlow 证明了 MeanFlow 在在线自回归场景下的可行性和优势，拓展了流模型从离线生成到实时交互生成的应用边界。
- **相对于自回归生成文献**：ARMFlow 提供了“完整历史因果编码 + 生成历史自举训练”的范式，为自回归运动生成中的误差累积问题提供了新的解决思路。
- **相对于人体反应生成文献**：ARMFlow 首次在在线设定下实现了与离线 SOTA 相当的生成质量，弥合了在线效率与离线质量之间的长期鸿沟。

### 4. 适用边界与局限

**适用边界。** ARMFlow 的设计假设交互双方的运动已通过 CNN-VAE 压缩到连续隐空间，且文本描述（如动作标签）可作为条件信号。方法适用于双人交互场景（如 InterHuman、InterX 数据集所涵盖的握手、拥抱、打斗等动作），理论上可扩展到更多代理的交互，但论文未提供多代理实验验证。

**已知局限。**
1. **多代理异步问题**：当前实现未提供自回归小窗口的弹性延迟处理机制，在多代理交互场景下可能产生轻微的异步行为。这一局限源于自回归框架本身对严格因果顺序的依赖。
2. **不支持事后优化**：由于 MeanFlow 的单步生成特性，模型不支持事后分类器引导（post-hoc classifier guidance），无法在生成后对结果进行基于优化的细化修正。这意味着生成质量完全依赖训练阶段学到的分布，缺乏推理时的灵活控制能力。
3. **实时性能的量化证据缺失**：论文通过 Figure 1 定性展示了单步推理的效率优势，但未提供 ARMFlow 在具体硬件上的端到端延迟测量（如毫秒级推理时间），实时性能的量化比较需要手动验证。

### 5. 开放问题

论文未明确列出开放问题。基于方法设计和局限，可识别以下值得关注的方向：
- **多代理扩展**：如何将因果上下文编码和 BSCE 策略扩展到三人及以上的交互场景，同时保持线性计算复杂度？
- **条件控制的灵活性**：在无法使用事后分类器引导的约束下，如何增强模型对细粒度条件（如情感强度、交互风格）的响应能力？
- **长序列稳定性**：BSCE 策略在极长序列（如数分钟连续交互）下的自回归稳定性尚未验证，误差累积的上界和衰减特性值得进一步分析。

## 原文 PDF

![[paperPDFs/CVPR_2026/ARMFlow_AutoRegressive_MeanFlow_for_Online_3D_Human_Reaction_Generation.pdf]]
