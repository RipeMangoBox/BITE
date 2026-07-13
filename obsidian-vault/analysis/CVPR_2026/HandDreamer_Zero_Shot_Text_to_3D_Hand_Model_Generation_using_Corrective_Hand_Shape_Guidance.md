---
title: "HandDreamer: Zero-Shot Text to 3D Hand Model Generation using Corrective Hand Shape Guidance"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HandDreamer_Zero_Shot_Text_to_3D_Hand_Model_Generation_using_Corrective_Hand_Shape_Guidance.pdf
project_link: null
code_link: null
aliases:
- HandDreamer
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过手部骨架条件控制网络（ControlNet）减少每个视角的概率模式歧义；使用 MANO 手部模型进行低分数初始化，使初始模型在语义和几何上接近理想一致状态；并引入纠正手部形状（CHS）损失进行持续的模式校正，防止侧视角因自遮挡导致的几何退化。
primary_logic: 利用手部骨架嵌入视角和姿态信息作为扩散模型条件，缩小概率分布的模式数量；结合参数化手部模型先验进行初始化和约束，使得 SDS 优化过程在保持视图一致性的同时生成高保真、几何准确的三维手部模型。
claims:
- 定理1表明，理想初始化应最小化初始模型与潜在真实模型的编码距离，从而降低绝对分数值，避免不同视角收敛到不同模式。
- 梯度可视化（图2）证实，MANO 初始化在低时间步和高时间步均能产生一致的梯度，而随机初始化则产生多样化梯度导致视图不一致。
- 消融实验（表2）表明，移除任何核心组件（骨架控制网、MANO 初始化或 CHS 损失）均导致 CLIP 分数下降或几何失真，验证了每个模块的必要性。
- Custom test set (45 prompts, 5400 views) 上 CLIP L14↑ = 28.63
---

# HandDreamer: Zero-Shot Text to 3D Hand Model Generation using Corrective Hand Shape Guidance

> [!tip] 核心洞察
> 利用手部骨架嵌入视角和姿态信息作为扩散模型条件，缩小概率分布的模式数量；结合参数化手部模型先验进行初始化和约束，使得 SDS 优化过程在保持视图一致性的同时生成高保真、几何准确的三维手部模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | HandDreamer：基于纠正手部形状引导的零样本文本到三维手部模型生成 |
| 英文题名 | HandDreamer: Zero-Shot Text to 3D Hand Model Generation using Corrective Hand Shape Guidance |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.04425) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | HandDreamer |
| Dataset | Custom test set |

> [!tip] 效果简介
> - Custom test set (45 prompts, 5400 views) 上，CLIP L14↑ 28.63 vs 26.62 (CFD) (+2.01)；FID↓ 254.62 vs 262.83 (CFD) (-8.21)；HPSv2↑ 0.241 vs 0.223 (CFD) (+0.018)。

## 概要

**问题瓶颈**：现有的基于分数蒸馏采样（SDS）的文本到三维生成方法，在处理人手这类高度可动关节结构时，面临根本性困难。由于文本提示所定义的概率图景中存在大量可能的生成模式，不同视角的优化过程容易收敛到互不一致的模式，进而产生 Janus 伪影（多面人效应）、手指数量错误和几何细节丢失。

**核心思路**：HandDreamer 通过三条因果路径解决上述瓶颈。其一，引入手部骨架条件控制网络（ControlNet），将三维骨架的二维投影作为扩散模型的条件信号，从源头压缩每个视角的概率模式歧义。其二，利用 MANO 参数化手部模型进行低分数初始化，使初始三维表征在语义和几何上接近理想的视角一致状态，避免优化过程陷入错误模式。其三，提出纠正手部形状（CHS）损失，在 SDS 优化过程中持续约束 NeRF 不透明度与 MANO 轮廓的一致性，防止侧视角因自遮挡导致的几何退化。

**方法定位**：HandDreamer 是首个面向零样本文本到手部三维模型生成的方法。它在分数蒸馏采样范式下，将参数化手部模型先验、骨架条件扩散模型与纠正性几何约束有机整合，形成两阶段生成流程——手部形状初始化与骨架引导的 SDS 优化。

**主要结果**：在包含 45 个提示词、5400 个渲染视角的自定义测试集上，HandDreamer 在 CLIP L14（28.63）、FID（254.62）和 HPSv2（0.241）三项指标上均优于现有最优方法 CFD（CLIP 26.62、FID 262.83、HPSv2 0.223）。消融实验证实，移除骨架控制网络、MANO 初始化或 CHS 损失中的任一组件，均会导致 CLIP 分数下降或几何失真，验证了每个模块的必要性。



### 文本到三维生成的核心瓶颈：关节结构的视图一致性

基于分数蒸馏采样（Score Distillation Sampling, SDS）的文本到三维生成方法（如 DreamFusion、LatentNerf、Fantasia3D、ProlificDreamer 等）已在通用物体生成上取得显著进展，但其核心缺陷在处理高度可动关节结构时暴露无遗。手部作为人体最具表达力的关节部位，拥有超过 20 个自由度，其三维结构在不同视角下呈现出剧烈变化的轮廓和自遮挡模式。现有 SDS 方法的根本问题在于：**文本提示定义的概率图景中存在大量可能的模式，不同视角的优化过程会收敛到互不一致的模式**，导致经典的 Janus 伪影（多面神问题）——例如从正面看是手掌、从侧面看却出现另一组手指的几何错乱。

图 2 直观揭示了这一机制：同一视点下存在多个概率模式（Figure 2a），随机初始化使得不同视角的 SDS 梯度在高时间步发散到不同模式（Figure 2d），最终生成视图不一致的几何结构（Figure 2b）。已有方法如 HiFA、ESD 在生成手部时均出现严重的 Janus 伪影和手指缺失（Figure 1g），而文本到人体方法（DreamAvatar、HumanNorm、DreamWaltz）生成的手部细节严重不足。

### 现有方法的三个结构性缺口

**第一，扩散条件缺乏视角与姿态信息。** 现有方法仅使用文本提示作为扩散模型的条件，每个视角的生成过程完全独立，缺乏跨视角的一致性约束。对于手部这类自遮挡严重的结构，纯文本条件无法区分“握拳的正面”与“伸展的背面”，导致每个视角各自解释文本提示。

**第二，三维表示初始化缺乏几何先验。** 主流方法采用随机初始化或高斯球初始化，初始 NeRF 模型在语义和几何上与目标手部结构毫无关联。论文的理论分析（Theorem 1）表明，理想初始化应最小化初始模型与潜在真实模型的编码距离，从而降低绝对分数值，避免不同视角收敛到不同模式。随机初始化使得低时间步的梯度信息量不足（Figure 2c），进一步加剧了模式发散。

**第三，优化过程缺乏持续的几何校正。** SDS 损失本身不包含任何显式的几何约束，侧视角下严重的自遮挡会导致 NeRF 的不透明度场逐渐偏离正确的手部形状，产生几何退化。现有方法缺少在优化过程中持续纠正几何偏差的机制。

### HandDreamer 的动机与设计思路

针对上述缺口，HandDreamer 提出三条正交的解决路径：（1）**手部骨架条件控制网络**——将三维手部骨架的二维投影作为 ControlNet 条件注入扩散模型，为每个视角嵌入视角和姿态信息，缩小概率分布的模式数量；（2）**MANO 手部模型初始化**——利用参数化手部模型 MANO 提供强几何先验，使初始 NeRF 在语义和几何上接近理想一致状态；（3）**纠正手部形状损失**——在 SDS 优化过程中持续惩罚 NeRF 不透明度与 MANO 轮廓的偏差，防止侧视角几何退化。三者协同作用，使得 SDS 优化过程在保持视图一致性的同时生成高保真、几何准确的三维手部模型。



## 核心方法与创新机理

HandDreamer 的核心创新在于针对文本到三维生成中**高度可动关节的视图一致性问题**，提出了一套系统性的解决方案。与现有基于分数蒸馏采样（SDS）的方法（如 DreamFusion、LatentNerf、ProlificDreamer 等）不同，HandDreamer 通过三个紧密耦合的“changed slots”从根本上改变了优化的初始条件、条件信号和约束机制。

### 1. 从随机初始化到 MANO 参数化先验初始化

现有 SDS 方法通常采用随机球体或高斯初始化三维表示。这在生成简单物体时可行，但对于手部这类具有复杂拓扑和高度可动关节的结构，随机初始化会导致不同视角收敛到概率图景中的不同模式，产生 Janus 伪影和几何错误。HandDreamer 将初始化策略替换为 **MANO 手部模型初始化**：通过最小化 NeRF 体积密度与 MANO 网格轮廓之间的不透明度差异，使初始模型在语义和几何上接近理想的一致状态。

这一设计的理论依据在于：SDS 优化本质上沿着最小化估计绝对分数值的路径进行，而理想初始化应最小化初始模型与潜在真实模型的编码距离，从而降低绝对分数值，避免不同视角收敛到不同模式。梯度可视化（Figure 2）证实了这一点——MANO 初始化在低时间步和高时间步均能产生一致的梯度，而随机初始化则产生多样化梯度，直接导致视图不一致。

### 2. 从纯文本条件到手部骨架条件扩散

传统 SDS 方法仅使用文本提示作为扩散模型的条件信号。然而，对于手部而言，文本提示定义的概率图景中存在大量可能模式（不同手指数量、姿态、视角等），单一文本条件无法有效消除视角间的模式歧义。HandDreamer 引入了**手部骨架条件控制网络（Skeleton-guided ControlNet）**：将三维手部骨架投影为二维骨架图，作为 Stable Diffusion 的额外条件信号，与文本提示共同约束扩散过程。

这一设计将每个视角的概率模式数量从“文本定义的全集”缩小到“文本+骨架联合定义的小子集”，显著降低了模式歧义。骨架条件嵌入的视角和姿态信息，使得扩散模型能够为每个特定视角提供更具判别力的梯度信号，从而促进视图一致性。

### 3. 从单一 SDS 损失到多损失联合约束

基线方法通常仅依赖 SDS 损失（或辅以最小正则化）进行优化。HandDreamer 在此基础上引入了三个关键损失组件：

- **纠正手部形状（CHS）损失**：计算 NeRF 不透明度与 MANO 真实轮廓之间的 L2 距离，并根据时间步进行退火加权。该损失持续校正优化过程，防止侧视角因自遮挡导致的几何退化。
- **图像损失**：稳定训练过程。
- **Z 方差损失**：锐化表面几何。

其中 CHS 损失是 HandDreamer 提出的全新组件。其权重采用线性退火策略，在优化早期施加较大权重以稳定几何结构，随后逐渐减小，让 SDS 损失主导细节生成。消融实验（Table 2）表明，移除 CHS 损失后，侧视角出现明显的几何失真，验证了该组件在维持视图一致性几何中的关键作用。

### 创新点总结

三处“changed slots”并非孤立设计，而是形成了因果闭环：MANO 初始化提供接近一致的初始状态，骨架条件控制网在每个视角缩小模式搜索空间，CHS 损失持续纠正优化过程中的几何漂移。这一组合使得 HandDreamer 成为首个能够从文本提示零样本生成高保真、几何准确的三维手部模型的方法。



HandDreamer 的整体流程分为两个阶段：**手部形状初始化**和**手部模型生成**，如图 3 所示。该方法以文本提示和 MANO 手部模型姿态参数为输入，输出具有视图一致性几何和精细纹理的三维手部模型。

### 第一阶段：手部形状初始化

该阶段利用 MANO 参数化手部模型为 NeRF 表示提供强几何先验。具体而言，给定目标手部姿态参数，渲染 MANO 网格在各视角下的二值轮廓图；随后优化 NeRF 的体积密度，使其渲染的不透明度与 MANO 轮廓一致。像素 $\mathbf{p}$ 的不透明度定义为：

$$O_{v, \mathbf{p}} = \sum_{i=1}^{T} \left( \prod_{j=1}^{i-1} \exp(-\sigma_j \delta_j) \right) \left( 1 - \exp(-\sigma_i \delta_i) \right)$$

通过最小化 $O_{v, \mathbf{p}}$ 与 MANO 轮廓 $\boldsymbol{M}_v$ 之间的 L2 距离，将 NeRF 的初始密度分布约束在 MANO 手部形状附近。该初始化过程约需 15 分钟，且对同一姿态可复用于任意文本提示。

### 第二阶段：手部模型生成

在 MANO 初始化的基础上，进行骨架引导的分数蒸馏采样（SDS）优化，生成与文本描述一致的纹理和几何细节。该阶段的核心模块包括：

1. **骨架条件扩散模型**：将三维手部骨架投影到二维，作为 ControlNet 的条件输入，与文本提示共同引导 Stable Diffusion 的去噪过程。SDS 梯度更新公式为：

   $$\nabla_{\boldsymbol{\theta}} \mathcal{L}_{SDS} = \mathbb{E}_{t,\epsilon} \left[ w(t) (\epsilon_{\boldsymbol{\phi}}(\mathbf{I}_t; \boldsymbol{y}, t, S) - \epsilon) \frac{\partial \mathbf{I}}{\partial \boldsymbol{\theta}} \right]$$

   其中 $S$ 为骨架投影条件，$\boldsymbol{y}$ 为文本提示。骨架条件嵌入视角和姿态信息，有效缩小了每个视角下扩散模型概率分布的模式数量，从而缓解 Janus 伪影。

2. **纠正手部形状损失（CHS Loss）**：在 SDS 优化过程中持续约束 NeRF 的不透明度与 MANO 轮廓一致，防止侧视角因自遮挡导致的几何退化。CHS 损失定义为：

   $$\mathcal{L}_{chs}(t) = \lambda_t^{chs} \cdot \frac{1}{|\mathcal{V}|} \sum_{v \in \mathcal{V}} \| \boldsymbol{O}_v - \boldsymbol{M}_v \|_2$$

   权重 $\lambda_t^{chs}$ 随时间步 $t$ 线性退火，早期施加较大权重以稳定几何结构，后期逐步减弱以允许细节生成：

   $$\lambda_t = \lambda_{max}^{chs} \left[ \frac{t - t_{min}}{t_{max} - t_{min}} \right] + \lambda_{min}^{chs} \left[ \frac{t_{max} - t}{t_{max} - t_{min}} \right]$$

3. **辅助损失**：额外引入图像损失和 z 方差损失以稳定训练并锐化表面。

最终训练损失为上述各项的加权组合：

$$\mathcal{L} = \lambda_{sds} \cdot \mathcal{L}_{sds} + \lambda_t^{chs} \cdot \mathcal{L}_{chs}(t) + \lambda_{img} \cdot \mathcal{L}_{img} + \lambda_{zvar} \cdot \mathcal{L}_{zvar}$$

该阶段约需 8000 次迭代（约 45 分钟）收敛，GPU 内存消耗约 30 GB。

### 输入输出流总结

**输入**：文本提示 + MANO 姿态参数 → **阶段一**：MANO 轮廓监督的密度初始化 → 初始 NeRF → **阶段二**：骨架条件 SDS + CHS 损失 + 辅助损失 → **输出**：具有视图一致性几何和精细纹理的三维手部 NeRF 模型。导出的网格可进一步进行骨骼绑定以实现姿态驱动动画（图 7）。

### 补充图表

![[assets/figures/papers/paper_list_l2519_https_arxiv_org_abs_2604_04425/figures/003_Figure_3.jpg]]
*Figure 3: Overview of HandDreamer. Our method generates 3D hand models from text prompts in 2 stages: (a) Hand shape initialization using MANO mesh; (b) Hand model generation using skeleton and Corrective Hand Shape (CHS) guidance loss*



### 问题形式化与SDS梯度

HandDreamer 的核心目标是从文本提示 $\boldsymbol{y}$ 生成三维手部模型，模型由 NeRF 参数 $\boldsymbol{\theta}$ 表示。基础框架沿用分数蒸馏采样（SDS），其梯度为：

$$
\nabla_{\boldsymbol{\theta}} \mathcal{L}_{SDS} = \mathbb{E}_{t,\epsilon} \left[ w(t) (\epsilon_{\boldsymbol{\phi}}(\mathbf{I}_t; \boldsymbol{y}, t, S) - \epsilon) \frac{\partial \mathbf{I}}{\partial \boldsymbol{\theta}} \right]
$$

其中 $\mathbf{I}_t$ 为加噪后的渲染图像，$\epsilon_{\boldsymbol{\phi}}$ 为扩散模型预测的噪声，$S$ 为手部骨架条件。与传统 SDS 的关键区别在于，HandDreamer 在扩散条件中显式注入了视角相关的骨架投影 $S$，以缩小每个视角下的概率模式歧义。

然而，论文通过定理1（详见原文 Section 4 及 Appendix A.1）指出：SDS 优化本质上沿着最小化估计绝对分数值的方向进行。若初始三维模型与理想一致模型的编码距离过大，不同视角将收敛到互不一致的模式，这正是 Janus 伪影和手指数量错误的根源。

### 三大核心模块

**模块一：MANO 手部形状初始化**

在 NeRF 训练前，使用参数化手部模型 MANO 初始化体积密度。具体而言，对每个像素 $\mathbf{p}$ 沿光线采样 $T$ 个点，计算 NeRF 不透明度：

$$
O_{v, \mathbf{p}} = \sum_{i=1}^{T} \left( \prod_{j=1}^{i-1} \exp(-\sigma_j \delta_j) \right) \left( 1 - \exp(-\sigma_i \delta_i) \right)
$$

初始化过程通过最小化 $O_{v, \mathbf{p}}$ 与 MANO 网格投影轮廓之间的差异，使 NeRF 在语义和几何上接近理想一致的手部模型。这一步从源头降低了绝对分数值，避免后续 SDS 发散到错误模式。

**模块二：骨架引导扩散条件**

在 SDS 优化阶段，每个视角渲染图像的同时，将三维手部骨架投影为二维骨架图，作为 ControlNet 的条件输入 $\epsilon_{\boldsymbol{\phi}}(\mathbf{I}_t; \boldsymbol{y}, t, S)$。骨架条件显式编码了视角和姿态信息，使扩散模型在每个视角下可匹配的概率模式数量大幅减少，从而保证多视角一致性。

**模块三：纠正手部形状损失**

即使有骨架引导，侧视角因自遮挡严重仍可能出现几何退化。为此引入纠正手部形状（CHS）损失，直接约束 NeRF 不透明度与 MANO 真实轮廓的一致性：

$$
\mathcal{L}_{chs}(t) = \lambda_t^{chs} \cdot \frac{1}{|\mathcal{V}|} \sum_{v \in \mathcal{V}} \| \boldsymbol{O}_v - \boldsymbol{M}_v \|_2
$$

其中 $\boldsymbol{O}_v$ 为视角 $v$ 下所有像素的 NeRF 不透明度，$\boldsymbol{M}_v$ 为对应的 MANO 二值轮廓。权重 $\lambda_t^{chs}$ 采用线性退火策略，在训练早期施加较强约束以稳定几何，后期逐渐放松以释放纹理细节：

$$
\lambda_t = \lambda_{max}^{chs} \left[ \frac{t - t_{min}}{t_{max} - t_{min}} \right] + \lambda_{min}^{chs} \left[ \frac{t_{max} - t}{t_{max} - t_{min}} \right]
$$

### 总损失函数

最终训练损失整合四个组件：

$$
\mathcal{L} = \lambda_{sds} \cdot \mathcal{L}_{sds} + \lambda_t^{chs} \cdot \mathcal{L}_{chs}(t) + \lambda_{img} \cdot \mathcal{L}_{img} + \lambda_{zvar} \cdot \mathcal{L}_{zvar}
$$

其中 $\mathcal{L}_{img}$ 为图像重建损失，$\mathcal{L}_{zvar}$ 为 z 方差损失，二者共同稳定训练并锐化表面。消融实验（Table 2, Figure 9）证实，移除任一模块均导致 CLIP 分数下降或几何失真，验证了三个核心模块的因果必要性。

### 补充图表

![[assets/figures/papers/paper_list_l2519_https_arxiv_org_abs_2604_04425/figures/002_Figure_2.jpg]]
*Figure 2: Convergence into wrong modes. (a) Probable modes for same view point. (b) Random initialization can converge into different modes for same viewpoints leading to Janus artifacts. (c,d) Visualization of gradients for the same viewpoint with multiple timesteps (t). Random initialization leads to less informative gradients at lower t and diverse gradients leading to view-inconsistencies at higher t. MANO initialization yields consistent gradients at lower and higher t*



## 实验与关键发现

### 主结果定量对比

HandDreamer 在自建测试集（45 个提示词，5400 张渲染视图）上与现有文本到三维方法进行了系统比较。如表 1 所示，该方法在所有三项指标上均取得最优：CLIP L14 达到 28.63，较次优方法 CFD 的 26.62 提升 **+2.01**；FID 降至 254.62，较 CFD 的 262.83 降低 **-8.21**；HPSv2 达到 0.241，较 CFD 的 0.223 提升 **+0.018**。所有对比方法均使用作者公开代码在同一测试集上评估，确保公平性。

### 定性对比分析

与现有文本到三维方法的视觉对比如图 5 所示。基线方法普遍存在 **Janus 伪影**（HiFA、ESD 等在不同视角生成不一致的面部/手指结构）和手指数量错误。文本到人体方法（DreamAvatar、HumanNorm、DreamWaltz）虽能生成整体人体，但手部细节严重缺失。HandDreamer 得益于骨架条件控制网络和 MANO 初始化，在不同视角下保持几何一致性和纹理细节。与单次图像手部生成方法 OHTA 的对比（图 6）进一步表明，HandDreamer 在纹理质量和几何多样性上均占优势。

### 消融研究

表 2 和图 9 系统消融了三个核心组件的贡献：

| 配置 | CLIP L14↑ | 现象 |
|------|-----------|------|
| 移除所有组件（仅文本 SDS） | 26.40 | 严重 Janus 伪影，无法生成手部结构 |
| 仅加骨架 ControlNet | 26.67 | 手指数量错误，几何不正确 |
| 骨架 CN + MANO 初始化，无 CHS | 28.48 | 侧视角度出现几何扭曲 |
| **完整方法** | **28.63** | 视图一致，几何保真度最高 |

消融结果表明：**(1)** 骨架 ControlNet 通过注入视角和姿态信息，有效减少了每个视角的概率模式歧义，但单独使用无法保证手指数量正确；**(2)** MANO 初始化提供了强几何先验，使初始模型在语义和几何上接近理想一致状态，显著提升 CLIP 分数；**(3)** 纠正手部形状（CHS）损失在侧视角下防止自遮挡导致的几何退化，是完整方法达到最优的关键。

### 用户偏好研究

图 8 展示了用户偏好研究结果。参与者在多个维度上对 HandDreamer 的评分显著高于对比方法，验证了该方法在感知质量上的优势。

### 失败模式与局限

尽管 HandDreamer 在手部生成任务上表现优异，仍存在以下局限：
- **极端侧视角度**：CHS 损失在严重自遮挡情况下可能不足以完全纠正几何退化，需进一步研究视角校正机制。
- **泛化能力**：方法依赖 MANO 参数化模型进行初始化和约束，对非人手虚构生物手部结构的生成能力未经验证。
- **骨骼绑定自动化**：优化后的三维手部模型需人工调整才能生成动画，自动化 rigging 流程仍是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l2519_https_arxiv_org_abs_2604_04425/figures/009_Table_1.jpg]]
*Table 1: Quantitative comparisons. Our method outperforms the other methods on all the metrics*

![[assets/figures/papers/paper_list_l2519_https_arxiv_org_abs_2604_04425/figures/013_Figure_9.jpg]]
*Figure 9: Ablation studies. (a) Removing all components fails to generate hand structure. (b) Using only CN causes incorrect geometry. (c) Removing CHS causes distortions in side views. (d) Using all components generates best results*

![[assets/figures/papers/paper_list_l2519_https_arxiv_org_abs_2604_04425/figures/010_Table.jpg]]

![[assets/figures/papers/paper_list_l2519_https_arxiv_org_abs_2604_04425/figures/005_Figure_5.jpg]]
*Figure 5: Comparison against state-of-the-art text-to-3D methods. Janus artifacts and inconsistent fingers shown in red arrows and circle (a-c). Text-to-human methods (d-f) generates hands with very less details. Our method generates better 3D hand models with consistent geometry and details*

![[assets/figures/papers/paper_list_l2519_https_arxiv_org_abs_2604_04425/figures/011_Figure_8.jpg]]
*Figure 8: User preference study. Higher value is better. Our method scores highest compared to the other methods*

![[assets/figures/papers/paper_list_l2519_https_arxiv_org_abs_2604_04425/figures/001_Figure_1.jpg]]
*Figure 1: We propose HandDreamer: the first method for zero-shot 3D hand generation from text prompts. Our method generates highfidelity, geometrically accurate 3D hand models with diverse articulations from text prompts. Existing methods generate Janus artifacts (HiFA, ESD) and fewer details (OHTA, DreamDPO, HumanNorm) (g). Surface maps provided inset*

![[assets/figures/papers/paper_list_l2519_https_arxiv_org_abs_2604_04425/figures/004_Figure_4.jpg]]
*Figure 4: Our method generates 3D hand models with detailed texture and view-consistent geometry. Surface maps provided inset*

![[assets/figures/papers/paper_list_l2519_https_arxiv_org_abs_2604_04425/figures/006_Figure_6.jpg]]
*Figure 6: Comparison against one-shot method OHTA. Our method generates better textures and diverse geometry*

![[assets/figures/papers/paper_list_l2519_https_arxiv_org_abs_2604_04425/figures/007_Figure_7.jpg]]
*Figure 7: Our method supports hand articulations for diverse hand poses.(a) Obtained using different MANO parameters. (b) Obtained using rigging of exported mesh*

![[assets/figures/papers/paper_list_l2519_https_arxiv_org_abs_2604_04425/figures/015_Table_3.jpg]]
*Table 3: Quantitative comparisons. Our method outperforms the other methods on all the metrics while generating results in low standard deviation*



## 定位与知识库关联

**问题定位**：现有基于分数蒸馏采样（SDS）的文本到三维生成方法（如 DreamFusion、LatentNeRF、Fantasia3D、ProlificDreamer 等）在生成一般物体时表现良好，但当目标为高度可动关节结构（如人手）时，面临根本性困难。文本提示定义的概率图景中存在大量可能模式，导致不同视角的 SDS 优化收敛到不同模式，产生经典的 Janus 伪影、手指数量错误和几何细节丢失。文本到人体生成方法（如 DreamAvatar、HumanNorm、DreamWaltz）虽能生成全身化身，但手部区域细节严重不足。单次图像重建方法（如 OHTA）则受限于输入视角，无法生成多样化姿态和完整几何。

**核心创新点**：HandDreamer 首次将零样本文本到手部三维生成问题形式化，并提出三项协同创新：
1. **MANO 手部模型初始化**：利用参数化手部模型 MANO 对 NeRF 的体积密度进行初始化，使初始三维表征在语义和几何上接近理想的视图一致手部模型。理论分析（定理 1）表明，这种初始化最小化了初始模型与潜在真实模型的编码距离，从而降低绝对分数值，避免不同视角收敛到不同模式。
2. **手部骨架条件扩散**：将三维手部骨架投影到二维，通过 ControlNet 作为 Stable Diffusion 的附加条件，在每个视角有效缩小概率分布的模式数量，减少视角间的模式歧义。
3. **纠正手部形状（CHS）损失**：在 SDS 优化过程中持续惩罚 NeRF 不透明度与 MANO 轮廓之间的偏差，防止侧视角因自遮挡导致的几何退化。CHS 损失采用时间步退火加权策略，在优化早期施加较强约束以稳定几何结构。

**方法谱系**：HandDreamer 继承并扩展了 SDS 范式（DreamFusion 系列），其技术路线可定位于“参数化模型先验 + 条件扩散引导”的混合框架。与同样引入人体先验的 DreamAvatar 和 HumanNorm 相比，HandDreamer 将先验粒度从全身细化到手部，并通过骨架条件网络和 CHS 损失实现了更高保真度的几何一致性。与 OHTA 等单次重建方法相比，HandDreamer 不依赖输入图像，支持从任意文本提示生成多样化手部姿态。

**适用边界与局限**：
- **MANO 模型依赖**：方法强依赖 MANO 手部模型的参数化先验进行初始化和约束。对于非人手的虚构生物手部结构（如卡通手、外星人手），MANO 的拓扑和姿态空间可能无法覆盖，泛化能力受限。此点需要手动验证。
- **极端视角退化**：尽管 CHS 损失缓解了侧视角的几何退化，但对于极端自遮挡情况，该约束是否足够仍需进一步研究。
- **计算资源**：手部形状初始化阶段约需 15 分钟，CHS 引导的 SDS 阶段约需 45 分钟收敛，消耗约 30 GB GPU 显存（Section 6.1），对硬件有一定要求。

**开放问题**：
1. 如何为优化后的三维手部模型自动化生成骨骼绑定和动画（rigging/articulation），而不需人工调整？论文展示了通过 MANO 参数和网格绑定实现姿态变化的能力（Figure 7），但自动化管线尚未完全闭环。
2. 如何将 HandDreamer 扩展到全身三维化身生成，同时保持手部细节的质量？这需要在多粒度先验融合和计算效率之间取得平衡。
3. 对于极端侧视角度由自遮挡造成的几何退化，CHS 损失是否足够，是否需要引入基于多视图一致性或神经渲染的进一步视图校正机制？



## 原文 PDF

![[paperPDFs/CVPR_2026/HandDreamer_Zero_Shot_Text_to_3D_Hand_Model_Generation_using_Corrective_Hand_Shape_Guidance.pdf]]
