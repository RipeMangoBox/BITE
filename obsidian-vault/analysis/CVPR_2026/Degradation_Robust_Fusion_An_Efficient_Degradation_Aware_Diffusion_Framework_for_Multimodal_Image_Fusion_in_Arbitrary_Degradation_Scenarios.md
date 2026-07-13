---
title: "Degradation-Robust Fusion: An Efficient Degradation-Aware Diffusion Framework for Multimodal Image Fusion in Arbitrary Degradation Scenarios"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Degradation_Robust_Fusion_An_Efficient_Degradation_Aware_Diffusion_Framework_for_Multimodal_Image_Fusion_in_Arbitrary_Degradation_Scenarios.pdf
project_link: null
code_link: "https://github.com/YShi-cool/DRFusion"
aliases:
- DRFEDADFMIFA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 以直接回归融合图像替代显式噪声预测，并引入联合观测模型校正机制，使得扩散框架能够以少量步骤同时满足退化约束和融合一致性，是实现高效退化鲁棒融合的关键。
primary_logic: 通过隐式去噪回归和联合伪逆校正，将扩散模型从单域目标分布学习中解放出来，构建了一个既保持扩散模型结构化推断优势、又兼具端到端灵活性的退化感知融合框架。
claims:
- "所提方法在 M3FD 数据集上噪声、模糊和复合退化三种场景下的 QMI、QNCIE、Q^{AB/F}、Q_P、Q_W 等指标均取得最佳或次佳结果，显著优于级联式恢复+融合方法。"
- 去除联合观测约束校正导致融合图像噪声增加、细节模糊和边缘伪影加剧，客观指标全面下降（Table 3, Figure 7, Figure 8）。
- 扩散步数 T=3 时性能最佳，继续增加步数不再提升，且推理时间呈线性增长（Table 5）。
- 在下游目标检测任务中，所提方法以 0.9108 的 mAP@0.5 优于所有比较方法（Table 4）。
---

# Degradation-Robust Fusion: An Efficient Degradation-Aware Diffusion Framework for Multimodal Image Fusion in Arbitrary Degradation Scenarios

> [!tip] 核心洞察
> 通过隐式去噪回归和联合伪逆校正，将扩散模型从单域目标分布学习中解放出来，构建了一个既保持扩散模型结构化推断优势、又兼具端到端灵活性的退化感知融合框架。

| 字段 | 内容 |
|------|------|
| 中文题名 | 退化鲁棒融合：面向任意退化场景的高效退化感知扩散多模态图像融合框架 |
| 英文题名 | Degradation-Robust Fusion: An Efficient Degradation-Aware Diffusion Framework for Multimodal Image Fusion in Arbitrary Degradation Scenarios |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.08922) · [Code](https://github.com/YShi-cool/DRFusion) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DRFusion |
| Dataset | M3FD, Harvard PET-MRI |

> [!tip] 效果简介
> - M3FD (红外-可见光融合) 上，QMI 0.3505 (Noise), 0.4477 (Blur), 0.3732 (Composite) vs 最佳基线 0.3021 (RFfusion, Noise) (相对提升显著)；Q^{AB/F} 0.4083 (Noise), 0.3698 (Blur), 0.2199 (Composite) vs 最佳基线 (Noise) 0.4056 (IFCNN) (在Blur和Composite上优势明显)。
> - Harvard PET-MRI 上，Q^{AB/F} 在三个退化场景中取得最高 vs 所有比较方法 (定性定量均占优)。
> - M3FD (目标检测) 上，mAP@0.5 0.9108 vs IFCNN 0.8906 (+0.0202)。

## 概要

**核心问题**：真实世界中多模态图像融合（如红外‑可见光、PET‑MRI）面临噪声、模糊、低分辨率等复杂退化，而现有融合方法几乎都假设源图像是干净的。当退化存在时，主流策略是“先恢复、后融合”，但这种级联方式无法保证恢复过程对融合任务友好，且扩散模型虽具备强生成能力，却依赖单一目标分布训练，缺乏自然融合真值，难以直接用于退化融合。

**核心思路**：本文提出 **DRFusion**——一个退化感知的扩散融合框架。它抛弃了标准扩散模型中显式预测噪声的范式，转而**直接回归融合图像**，隐式完成去噪；同时设计了一个**联合观测模型校正机制**，在采样过程中同时施加退化约束与融合约束，通过解析伪逆将估计结果投影到约束超平面上，从而在极少的扩散步数内生成满足一致性的融合结果。

**方法定位**：DRFusion 既保留了扩散模型的结构化推断优势，又具备了端到端网络的灵活性。与需要数百步的标准扩散模型不同，它仅需 **3 步**即可完成推理，且训练完全自监督——直接优化源图像重建损失与任务相关的融合损失，无需伪标签或成对融合真值。

**主要结果**：
- 在 **M3FD**（红外‑可见光）和 **Harvard PET‑MRI** 两个数据集上，覆盖噪声、模糊、复合退化三种场景，DRFusion 在 QMI、Q<sup>AB/F</sup>、Q<sub>P</sub>、Q<sub>W</sub> 等多项指标上取得**最佳或次佳**，显著优于级联式恢复+融合方法（Table 1、Table 2）。
- 消融实验证实：**移除联合约束校正**后，融合图像噪声增加、细节模糊、边缘伪影加剧，所有客观指标全面下降（Table 3、Figure 7、Figure 8）。
- 扩散步数消融表明：T=3 时性能达到峰值，继续增加步数不再提升，且推理时间线性增长（Table 5）。
- 在下游目标检测任务中，DRFusion 以 **mAP@0.5 = 0.9108** 优于所有比较方法（Table 4），验证了融合质量对高层视觉任务的有效支撑。



### 多模态图像融合的现实困境

多模态图像融合旨在将不同传感器捕获的互补信息整合为单一、信息丰富的图像，在自动驾驶、医学诊断、夜间监控等场景中扮演关键角色。红外图像提供热辐射信息，不受光照影响；可见光图像则保留丰富的纹理与色彩细节。然而，真实世界的成像过程远非理想——源图像常常同时遭受**噪声污染、运动模糊、低分辨率**等多种退化。这种退化叠加使得融合任务从“如何融合”升级为“如何在退化中融合”。

当前主流融合方法——无论是基于 CNN 的 **IFCNN**、**U2Fusion**、**MURF**，还是基于扩散模型的 **DDFM**、**Text-DiFuse**、**RFfusion**——几乎都假设输入源图像是干净的。当面对退化图像时，这些方法只能采取“**先恢复，后融合**”的级联策略：先用去噪、去模糊或超分算法处理退化，再执行融合。这种级联范式存在两个根本缺陷：其一，恢复过程与融合过程相互独立，恢复阶段引入的伪影或信息丢失会直接污染后续融合结果；其二，恢复算法本身在极端退化下性能有限，级联误差会逐级放大。

### 扩散模型的潜力与瓶颈

扩散模型（Diffusion Models）近年来在图像生成领域展现出强大的结构化推断能力。其核心机制是通过逐步去噪将随机噪声映射到目标数据分布，这一过程天然具备处理退化的潜力。然而，将扩散模型直接应用于退化融合面临三重障碍：

1. **训练目标依赖单一分布**：标准扩散模型（如 DDPM）需要从目标分布中采样训练数据，但自然图像融合不存在真实的“融合图像”分布，无法直接构建训练对。
2. **推理效率低下**：传统扩散模型需要数百步（DDPM）甚至数十步（DDIM）迭代采样，难以满足实时融合需求。
3. **退化约束缺失**：扩散采样过程仅受噪声预测引导，缺乏将退化模型与融合约束注入推理的机制，导致生成结果可能与退化观测不一致。

### 本文动机：退化感知的扩散融合框架

针对上述缺口，本文提出 **DRFusion**——一个面向任意退化场景的高效退化感知扩散融合框架。核心动机可概括为三个层面：

- **从“先恢复后融合”到“直接融合”**：摒弃级联范式，直接从退化源图像重建高质量融合结果，避免中间恢复步骤的信息损失。
- **从“噪声预测”到“隐式去噪回归”**：不显式预测噪声，而是直接回归融合图像，使扩散框架摆脱对单一目标分布的依赖，同时大幅减少所需采样步数。
- **从“无约束生成”到“联合约束校正”**：设计联合观测模型，将退化约束与融合约束统一为线性方程组，在每步扩散采样后通过解析伪逆校正，确保输出同时满足退化一致性和融合一致性。

这三个设计共同指向一个目标：**在保持扩散模型结构化推断优势的前提下，构建一个既高效、又鲁棒、且能灵活适配不同融合任务的退化感知框架**。



## 核心方法与创新机理

DRFusion 针对真实场景下多模态图像融合面临噪声、模糊、低分辨率等复杂退化，而现有方法普遍假设源图像无退化的瓶颈，提出了一套退化感知的扩散框架。其核心创新可归纳为四个相互耦合的“changed slots”，共同实现了从标准扩散范式到退化鲁棒融合范式的关键跃迁。

### 扩散建模目标：从显式噪声预测到隐式去噪回归

标准扩散模型（DDPM/DDIM）以预测噪声为核心目标，训练依赖单一目标分布，难以直接适配缺乏自然融合真值的多模态融合任务。DRFusion 丢弃了显式噪声预测步骤，改为**直接回归融合图像**，将扩散过程转化为一个受约束的端到端映射。具体而言，网络输出被重新定义为“伪噪声” $\varepsilon_\theta$，并通过 DDIM 框架从当前噪声样本 $\hat{\mathbf{x}}_t$ 估计干净图像：

$$\hat{\mathbf{x}}_{0\mid t} = \hat{\mathbf{x}}_t - \sqrt{1-\bar{\alpha}_t}\,\varepsilon_\theta(\hat{\mathbf{x}}_t, t)$$

这一设计使得扩散模型在架构上更接近端到端神经网络，同时保留了扩散过程的结构化推断优势，为后续联合约束校正提供了可微分的估计量。

### 观测约束：从单图约束到联合观测模型校正

现有扩散逆问题方法（如 DDNM）通常仅对单幅图像施加退化约束，无法同时处理两幅退化源图像的融合一致性。DRFusion 的核心突破在于构建了一个**联合观测模型**，将两幅源图像的退化约束与线性融合约束统一为单个线性方程组：

$$\begin{bmatrix} \mathbf{y}_1 \\ \mathbf{y}_2 \\ \mathbf{0} \end{bmatrix} = \begin{bmatrix} \mathbf{A}_1 & 0 & 0 \\ 0 & \mathbf{A}_2 & 0 \\ -\mathbf{W}_1 & -\mathbf{W}_2 & \mathbf{I} \end{bmatrix} \begin{bmatrix} \mathbf{X}_1 \\ \mathbf{X}_2 \\ \mathbf{X}_f \end{bmatrix}$$

其中 $\mathbf{A}_1, \mathbf{A}_2$ 为退化矩阵（模糊核、下采样等），$\mathbf{W}_1, \mathbf{W}_2$ 为融合权重图。通过求解该系统的 Moore-Penrose 伪逆 $\hat{\mathbf{A}}^{\dagger}$，得到解析形式的联合校正步骤：

$$\bar{\mathbf{x}}_{0\mid t} = \hat{\mathbf{x}}_{0\mid t} - \hat{\mathbf{A}}^{\dagger}(\hat{\mathbf{A}}\hat{\mathbf{x}}_{0\mid t} - \mathbf{y})$$

该步骤将 DDIM 估计的融合图像投影到退化约束与融合约束的交集超平面上，确保输出同时满足数据一致性和跨模态互补性。消融实验（Table 3, Figure 7, Figure 8）表明，移除该机制会导致融合图像噪声增加、细节模糊、边缘伪影加剧，所有客观指标全面下降。

### 训练方式：从目标分布依赖到自监督任务导向优化

现有扩散融合方法通常依赖目标分布训练（监督或伪标签），而 DRFusion 采用**自监督训练**，直接优化源图像重建损失与任务相关的融合损失。总损失函数为：

$$\mathcal{L}_{total} = \mathcal{L}_{rec} + \lambda \mathcal{L}_f$$

其中 $\mathcal{L}_{rec}$ 为源图像重建损失（L1），$\mathcal{L}_f$ 则根据融合任务灵活组合：红外-可见光融合采用最大选择策略约束强度和梯度（Eq. 23），医学图像融合则结合 L1 和 SSIM 保持结构一致性（Eq. 24）。这种任务导向的损失设计使框架无需依赖融合真值即可适应不同模态组合。

### 扩散步数与效率：从数百步到仅需 3 步

标准扩散模型通常需要数百步（DDPM）或数十步（DDIM）推理，而 DRFusion 通过隐式去噪回归与联合校正的结合，将有效推理步数压缩至 **T=3**。Table 5 的消融显示，步数从 1 增至 3 时指标持续提升，T=3 达到峰值；T>3 后性能饱和甚至略降，且推理时间线性增长。这一特性使 DRFusion 在保持扩散模型生成质量的同时，推理效率显著优于同类扩散融合方法（Figure 5）。



DRFusion 的整体框架围绕一个核心矛盾展开：**真实世界多模态融合必须同时应对源图像的退化（噪声、模糊、低分辨率等）与跨模态信息互补，但标准扩散模型依赖单一目标分布且缺乏自然融合数据，无法直接适配这一需求。** 该框架通过三个关键设计将扩散模型从单域目标分布学习中解放出来，构建了一个既保持扩散模型结构化推断优势、又兼具端到端灵活性的退化感知融合系统。

### 框架总览

如 Figure 2 所示，DRFusion 接收两幅任意退化类型的源图像 $y_1$、$y_2$，以及描述各自退化过程的观测矩阵 $A_1$、$A_2$，直接输出满足退化约束与融合一致性的融合图像 $X_f$。整个推理过程仅需 $T$ 步（默认 $T=3$）扩散反向迭代，每步包含三个阶段：**预测、校正、采样**。这一设计与传统的“先恢复后融合”级联策略（Figure 1a）和现有扩散融合方法（Figure 1b）形成鲜明对比——DRFusion 不再依赖独立的复原网络，也不要求源图像无退化或目标分布已知，而是将退化处理与融合统一在同一个扩散推理回路中。

![[assets/figures/papers/paper_list_l2731_https_arxiv_org_abs_2604_08922/figures/002_Figure_2.jpg]]
*Figure 2: The proposed framework for multimodal image fusion under various degradation scenarios in this work*

### 核心模块与数据流

框架由三个紧密耦合的模块构成，数据流沿时间步 $t = T, T-1, \dots, 1$ 单向推进：

1. **多任务 U-Net 噪声/权重预测器**  
   在每个时间步 $t$，该模块接收当前噪声估计 $\hat{x}_t$ 和退化信息，同时输出两项内容：  
   - **“伪噪声”** $\varepsilon_\theta(\hat{x}_t, t)$，用于 DDIM 反向过程中估计干净图像 $\hat{x}_{0|t}$（Eq. (16)）；  
   - **融合权重图** $W_1$，用于构建联合观测模型中的线性融合约束（$W_2 = I - W_1$）。  
   这里预测的是“伪噪声”而非标准扩散中的真实噪声——因为训练目标已从噪声预测转向直接回归融合图像（见 3.1 节），噪声预测器实际上隐式编码了去噪过程，为后续校正提供结构化先验。

2. **退化感知联合校正模块**  
   这是框架实现退化鲁棒融合的关键。该模块将两个源图像的退化约束 $y_i = A_i X_i + n_i$ 与线性融合约束 $X_f = W_1 X_1 + W_2 X_2$ 统一为一个联合线性方程组（Eq. (12)），并求解其 Moore-Penrose 伪逆 $\hat{A}^\dagger$（Eq. (15)）。随后，对 DDIM 估计的干净图像 $\hat{x}_{0|t}$ 执行解析投影校正：
   $$\bar{x}_{0|t} = \hat{x}_{0|t} - \hat{A}^\dagger(\hat{A}\hat{x}_{0|t} - y)$$
   这一步将估计结果投影到退化约束与融合约束的交集超平面上，强制生成满足物理一致性的修正图像。消融实验（Table 3, Figure 7, Figure 8）表明，移除该校正机制会导致融合结果噪声增加、细节模糊、边缘伪影加剧，所有客观指标全面下降——例如 M3FD 噪声场景下 QMI 从 0.3505 跌至 0.3322，$Q^{AB/F}$ 从 0.4083 跌至 0.3759。

3. **迭代扩散推理模块**  
   执行有限的 $T$ 步 DDIM 反向迭代（Algorithm 1），每步依次完成：  
   - 利用多任务预测器估计 $\hat{x}_{0|t}$；  
   - 通过联合校正模块投影得到 $\bar{x}_{0|t}$；  
   - 采样下一步噪声状态 $\hat{x}_{t-1}$。  
   扩散步数 $T=3$ 时性能达到峰值，继续增加步数不再提升且推理时间线性增长（Table 5），验证了框架在极少步数下即可收敛的设计优势。

### 训练与损失设计

训练阶段采用自监督策略，不依赖任何融合真值或伪标签。总损失由两部分组成（Eq. (20)）：
$$L_{total} = L_{rec} + \lambda L_f$$
其中 $L_{rec}$ 为源图像重建损失（L1），确保网络能够从退化观测中恢复源图像；$L_f$ 为任务相关融合损失，根据融合场景灵活组合——红外-可见光融合采用最大选择策略约束强度与梯度（Eq. (23)），医学图像融合则通过 L1 与 SSIM 约束结构一致性（Eq. (24)）。这种任务导向的损失设计使同一框架能够适配多种融合场景，而无需改变网络结构。

### 框架优势的因果机制

DRFusion 的性能优势源于一个因果闭环：**直接回归融合图像（隐式去噪）→ 降低对目标分布的依赖 → 联合伪逆校正注入退化与融合约束 → 少量扩散步即可生成满足物理一致性的融合结果。** 这解释了为何该框架在 M3FD 和 Harvard PET-MRI 数据集上，无论噪声、模糊还是复合退化场景，均能以 3 步扩散取得最优或次优的 QMI、$Q^{AB/F}$、$Q_P$ 等指标（Table 1, Table 2），并在下游目标检测任务中以 0.9108 的 mAP@0.5 优于所有比较方法（Table 4）。

### 补充图表

![[assets/figures/papers/paper_list_l2731_https_arxiv_org_abs_2604_08922/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of fusion strategies under different degradation scenarios: (a) methods based on neural networks; (b) existing diffusion-based methods; (c) the proposed degradation-aware diffusion framework from this work*



### 模块一：面向融合的隐式去噪扩散框架

DRFusion 对标准扩散模型进行了根本性改造：**丢弃显式噪声预测，仅保留逆向过程，将扩散模型重塑为端到端的融合回归架构**（Section 3.1）。其核心逻辑如下：

**前向扩散过程**（仅作为理论铺垫，不参与实际推理）：
$$p ( \mathbf { x _ { t } } | \mathbf { x _ { 0 } } ) = \mathcal { N } ( \mathbf { x _ { t } } ; \sqrt { \bar { \alpha } _ { \mathbf { t } } } \cdot \mathbf { x _ { 0 } } , ( \mathbf { 1 } - \bar { \alpha } _ { \mathbf { t } } ) \cdot \mathbf { I } )$$
其中 $\mathbf{x}_0$ 为干净融合图像，$\mathbf{x}_t$ 为时间步 $t$ 处的噪声版本，$\bar{\alpha}_t$ 为累积噪声调度参数。

**隐式去噪回归**：不同于标准扩散中预测噪声 $\varepsilon_\theta(\mathbf{x}_t, t)$ 再逐步去噪，DRFusion 直接利用多任务 U-Net 估计当前步的干净融合图像 $\hat{\mathbf{x}}_{0\mid t}$：
$$\hat { \mathbf { x } } _ { 0 \mid t } = \hat { \mathbf { x } } _ { t } - \sqrt { 1 - \bar { \alpha } _ { t } } \varepsilon _ { \theta } \big ( \hat { \mathbf { x } } _ { t } , t \big )$$
此处 $\varepsilon_\theta$ 的输出被重新解释为“伪噪声”，其实际作用是作为回归残差，驱动 $\hat{\mathbf{x}}_{0\mid t}$ 向真实融合图像收敛。该设计使扩散模型在架构上更接近端到端网络，且仅需 $T=3$ 步即可完成推理（Table 5 证实 $T>3$ 后性能饱和）。

---

### 模块二：退化感知联合校正机制

这是 DRFusion 的核心创新，解决了多模态退化融合中“退化约束”与“融合约束”的耦合难题（Section 3.2）。

**单图退化模型**：观测图像 $\mathbf{y}$ 与干净图像 $\mathbf{X}$ 的关系为：
$$\mathbf{y} = \mathbf{A} \mathbf{X} + \mathbf{n}$$
其中 $\mathbf{A}$ 为退化矩阵（噪声、模糊、下采样等），$\mathbf{n}$ 为加性噪声。

**联合观测模型**：将两幅源图像的退化约束与线性融合约束统一为联合线性方程组：
$$\left[ \begin{array} { l } { \mathbf { y } _ { 1 } } \\ { \mathbf { y } _ { 2 } } \\ { \mathbf { 0 } } \end{array} \right] = \left[ \begin{array} { l l l } { \mathbf { A } _ { 1 } } & { 0 } & { 0 } \\ { 0 } & { \mathbf { A } _ { 2 } } & { 0 } \\ { - \mathbf { W } _ { 1 } } & { - \mathbf { W } _ { 2 } } & { \mathbf { I } } \end{array} \right] \left[ \begin{array} { l } { \mathbf { X } _ { 1 } } \\ { \mathbf { X } _ { 2 } } \\ { \mathbf { X } _ { f } } \end{array} \right]$$
其中 $\mathbf{W}_1$、$\mathbf{W}_2$ 为融合权重图（由多任务 U-Net 同时预测），$\mathbf{X}_f$ 为融合图像。第三行约束 $\mathbf{X}_f = \mathbf{W}_1\mathbf{X}_1 + \mathbf{W}_2\mathbf{X}_2$，确保融合结果在退化校正后仍保持源图间的线性组合关系。

**解析伪逆校正**：对联合观测矩阵求 Moore-Penrose 伪逆，得到闭式解：
$$\hat { \mathbf { A } } ^ { \dagger } = \left[ \begin{array} { c c c } { \mathbf { A _ { 1 } } ^ { \dagger } } & { 0 } & { 0 } \\ { 0 } & { \mathbf { A _ { 2 } } ^ { \dagger } } & { 0 } \\ { \mathbf { W _ { 1 } A _ { 1 } } ^ { \dagger } } & { \mathbf { W _ { 2 } A _ { 2 } } ^ { \dagger } } & { \mathbf { I } } \end{array} \right]$$
利用该伪逆矩阵，将 DDIM 估计的 $\hat{\mathbf{x}}_{0\mid t}$ 投影到退化与融合约束的交集超平面上：
$$\bar { \bf x } _ { 0 \mid t } = \hat { \bf x } _ { 0 \mid t } - \hat { \bf A } ^ { \dagger } ( \hat { \bf A } \hat { \bf x } _ { 0 \mid t } - { \bf y } )$$
$\bar{\mathbf{x}}_{0\mid t}$ 即为同时满足退化一致性与融合一致性的校正图像。

**因果机制**：该模块将扩散采样中的去噪估计强制投影到联合约束流形上，避免了级联式“先恢复后融合”策略中误差累积的瓶颈。消融实验（Table 3, Figure 7, Figure 8）证实：移除该机制后，M3FD 噪声场景下 QMI 从 0.3505 降至 0.3322，$Q^{AB/F}$ 从 0.4083 降至 0.3759，且融合结果出现噪声增加、边缘伪影加剧等退化。

---

### 模块三：任务导向的损失函数设计

DRFusion 采用自监督训练，总损失由源图像重建损失与融合损失加权组合（Section 3.3）：
$$L _ { t o t a l } = L _ { r e c } + \lambda L _ { f }$$
其中 $L_{rec}$ 为源图像 $L_1$ 重建损失，$\lambda$ 为平衡系数。

**红外-可见光融合损失**：采用最大选择策略，约束融合图像在强度和梯度两个层面保留两源图中的显著信息：
$$L _ { f } = | | \mathbf { X } _ { f } - \operatorname* { m a x } ( \bar { \mathbf { X } } _ { 1 } , \bar { \mathbf { X } } _ { 2 } ) | | _ { 1 } + \gamma | | \nabla { \mathbf { X } } _ { f } - \operatorname* { m a x } ( \nabla \bar { \mathbf { X } } _ { 1 } , \nabla \bar { \mathbf { X } } _ { 2 } ) | | _ { 1 }$$
其中 $\bar{\mathbf{X}}_1$、$\bar{\mathbf{X}}_2$ 为退化校正后的源图像，$\nabla$ 为梯度算子，$\gamma$ 为梯度项权重。

**医学图像融合损失**：强调融合结果与各源图的结构一致性：
$${ \cal L } _ { f } = \sum _ { i = 1 } ^ { 2 } | | \mathbf { X } _ { f } - \bar { \mathbf { X } } _ { i } | | _ { 1 } + \phi ( 1 - \mathrm { S S I M } ( \mathbf { X } _ { f } , \bar { \mathbf { X } } _ { i } ) )$$
其中 SSIM 为结构相似性指标，$\phi$ 为平衡系数。该设计使 DRFusion 可根据任务灵活切换损失函数，实现任务导向优化，而非被单一噪声预测目标所束缚。



## 实验与关键发现

### 核心实验设置

本文在两种典型多模态融合任务上评估 DRFusion：红外-可见光融合（M3FD 数据集）和医学图像 PET-MRI 融合（Harvard 数据集）。实验覆盖三种退化场景——噪声（Noise）、模糊（Blur）和复合退化（Composite，同时含噪声、模糊与低分辨率），全面检验方法的退化鲁棒性。所有对比方法均采用“先恢复后融合”的级联策略：先用对应恢复算法（去噪、去模糊、超分）处理退化源图像，再执行融合，确保评估基准统一。对比基线包括基于 CNN 的融合方法 **IFCNN**、**U2Fusion**、**MURF**，以及基于扩散模型的融合方法 **DDFM**、**Text-DiFuse**、**VDMUFusion**、**RFfusion** 和 **Mask-DiFuser**。

评估指标覆盖信息论（QMI、QNCIE）、结构相似（Q^{AB/F}）、边缘保持（Q_P）、对比度（Q_CB）和视觉质量（Q_W）等多维度。推理时间比较在相同硬件环境下进行，扩散模型方法均采用 DDIM 加速采样。

### 主要定量结果

**红外-可见光融合（M3FD）**：Table 1 给出了各方法在三种退化场景下的客观指标对比。DRFusion 在绝大多数指标上取得最优或次优结果。在噪声场景下，QMI 达到 0.3505，显著优于最佳基线 RFfusion 的 0.3021；Q^{AB/F} 为 0.4083，与 IFCNN 的 0.4056 基本持平。在模糊和复合退化场景下，DRFusion 的优势更为明显，Q^{AB/F} 分别达到 0.3698 和 0.2199，大幅领先所有对比方法。QNCIE 在三个场景下均取得最优（0.8052/0.8068/0.8055），表明融合图像与源图的信息相关性保持最佳。

**医学图像融合（Harvard PET-MRI）**：Table 2 显示 DRFusion 在三个退化场景下均取得最高的 Q^{AB/F} 值，定性结果（Figure 4）也表明其融合图像在结构保真度和细节保持方面优于所有对比方法，尤其在复合退化场景下优势突出。

**下游任务验证**：Table 4 报告了基于各方法融合图像的目标检测性能。DRFusion 以 0.9108 的 mAP@0.5 优于所有对比方法（IFCNN 为 0.8906），证明退化鲁棒融合对下游视觉任务具有实际增益。

### 消融实验

**联合约束校正机制**：Table 3 给出了移除联合观测约束校正后的性能变化。在 M3FD 噪声场景下，QMI 从 0.3505 降至 0.3322，Q^{AB/F} 从 0.4083 降至 0.3759；所有场景下所有指标均出现全面下降。Figure 7 和 Figure 8 的可视化对比显示，无校正机制时融合结果噪声增加、细节模糊、边缘出现伪影，直接验证了联合校正对退化约束和融合一致性的关键作用。

**扩散步数 T**：Table 5 展示了扩散步数从 1 到 5 的消融结果。T=1 时性能已有竞争力，T 增至 3 时各项指标达到峰值；T>3 后性能饱和甚至略有下降，而推理时间呈线性增长。这表明 DRFusion 仅需 3 步即可实现最优融合，显著优于标准扩散模型所需的数十至数百步。

### 效率分析

Figure 5 对比了各方法的推理时间和参数量。DRFusion 在保持较少参数量的同时，推理速度显著优于大多数扩散模型基线。这得益于其直接回归融合图像的设计和仅需 3 步扩散迭代的高效采样策略，使得退化鲁棒融合在实际部署中具有可行性。

![[assets/figures/papers/paper_list_l2731_https_arxiv_org_abs_2604_08922/figures/007_Figure_5.jpg]]
*Figure 5: Comparison of time efficiency and model parameters across different fusion methods*

### 关键图表结论

- **Table 1**：DRFusion 在 M3FD 三类退化场景下全面领先，QMI 和 QNCIE 优势尤为显著。
- **Table 2**：Harvard 数据集上 Q^{AB/F} 三项最优，验证跨任务泛化能力。
- **Table 3 + Figure 7/8**：联合校正机制是性能核心支柱，移除后指标全面下降且视觉质量恶化。
- **Table 4**：融合质量提升直接转化为下游检测精度增益（mAP@0.5 达 0.9108）。
- **Table 5**：T=3 为效率-性能最优平衡点，更多步数无益且增加计算开销。

![[assets/figures/papers/paper_list_l2731_https_arxiv_org_abs_2604_08922/figures/004_Table_1.jpg]]
*Table 1: Objective fusion metrics of various methods under different degradation scenarios on the M3FD dataset (Bold and gray background: best result in each column; underline: second best)*

![[assets/figures/papers/paper_list_l2731_https_arxiv_org_abs_2604_08922/figures/006_Table_2.jpg]]
*Table 2: Objective fusion metrics of various methods under different degradation scenarios on the Harvard dataset (Bold and gray background: best result in each column; underline: second best)*

![[assets/figures/papers/paper_list_l2731_https_arxiv_org_abs_2604_08922/figures/011_Table_3.jpg]]
*Table 3: Ablation results for M3FD and PET-MRI datasets under different degradation scenarios. The best values for each metric are highlighted in light gray*

![[assets/figures/papers/paper_list_l2731_https_arxiv_org_abs_2604_08922/figures/009_Figure_7.jpg]]
*Figure 7: Results with and without the joint constraint correction mechanism under different degradation scenarios on M3FD dataset*

![[assets/figures/papers/paper_list_l2731_https_arxiv_org_abs_2604_08922/figures/014_Table_5.jpg]]
*Table 5: Quantitative comparison of different T values*

![[assets/figures/papers/paper_list_l2731_https_arxiv_org_abs_2604_08922/figures/013_Table_4.jpg]]
*Table 4: Detection performance comparison on M3FD dataset*

### 补充图表

![[assets/figures/papers/paper_list_l2731_https_arxiv_org_abs_2604_08922/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative results of different fusion methods on M3FD dataset. For the comparison methods, we first use corresponding restoration algorithms (e.g., denoising, deblurring, super-resolution) to restore the images, and then apply the respective fusion methods. The proposed method directly reconstructs the fusion results from the degraded source images. In the third degradation scenario, the infrared image is of low resolution and we have enlarged it, the original image is shown in the top-left corner*

![[assets/figures/papers/paper_list_l2731_https_arxiv_org_abs_2604_08922/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison of different fusion methods on the Harvard dataset. For the comparison methods, we first apply the corresponding restoration algorithms (e.g., denoising, deblurring, super-resolution) to process the images, and then perform fusion. The proposed method directly reconstructs the fusion results from the degraded source images. In the third degradation scenario, the PET image is of low resolution and we have enlarged it, the original image is shown in the top-left corner*

![[assets/figures/papers/paper_list_l2731_https_arxiv_org_abs_2604_08922/figures/010_Figure_8.jpg]]
*Figure 8: Results with and without the joint constraint correction mechanism under different degradation scenarios on PET-MRI dataset*



## 定位与知识库关联

### 退化鲁棒融合问题的技术谱系

DRFusion 所面对的核心问题——在源图像存在噪声、模糊、低分辨率等退化条件下实现多模态图像融合——传统上被拆解为“先恢复、后融合”的级联范式。该范式下，融合方法本身并不感知退化过程，其性能上限受限于前端恢复算法的质量。DRFusion 的定位在于打破这一级联依赖，将退化约束与融合约束统一纳入生成过程，形成端到端的退化感知融合框架。

从技术谱系看，与 DRFusion 相关的工作可分为三条脉络：

**（1）基于 CNN 的融合方法。** 这类方法以端到端网络直接学习从源图像到融合图像的映射，代表性工作包括 IFCNN、U2Fusion、MURF 等。它们在无退化场景下表现良好，但训练目标中缺乏对退化过程的显式建模，因此在噪声、模糊等退化条件下性能急剧下降。DRFusion 与这类方法的本质区别在于：前者将融合视为一个确定性前馈映射，而 DRFusion 将其重新定义为带约束的生成式逆向问题，通过扩散框架的结构化推断能力来应对退化不确定性。

**（2）基于扩散模型的融合方法。** 这是 DRFusion 最直接的方法论前驱，包括 DDFM、Text-DiFuse、VDMUFusion、RFfusion、Mask-DiFuser 等。这些方法将扩散模型的生成能力引入图像融合，但其设计存在两个关键局限：其一，它们依赖目标分布进行训练（如监督信号或伪标签），而自然图像融合缺乏成对的真值数据；其二，它们本质上是为无退化源图像设计的，当源图像含有退化时，扩散模型被强制去拟合一个与其训练分布不匹配的输入。DRFusion 对这一脉络的突破体现在两个维度：在训练范式上，从依赖目标分布转向自监督的源图像重建与融合损失联合优化；在推理机制上，引入联合观测模型校正，使扩散过程同时满足退化约束和融合一致性约束。

**（3）基于逆问题求解的扩散方法。** 在更广泛的逆问题领域，DDNM 等工作提出了在扩散采样过程中施加观测约束的方法，通过将估计结果投影到约束超平面来保证一致性。DRFusion 的联合校正模块在数学形式上继承了这一思路，但做出了关键扩展：将单幅图像的退化约束扩展为多幅源图像的联合退化约束，并在线性融合假设下将融合约束也纳入同一线性方程组，从而实现了“退化+融合”的联合约束投影。这一扩展使得原本面向单一图像恢复的伪逆校正机制，能够直接应用于多模态融合场景。

### 核心设计决策的差异化分析

DRFusion 与前述方法谱系的关键分岔点可归纳为三个设计决策：

**决策一：隐式去噪回归 vs. 显式噪声预测。** 标准扩散模型（如 DDPM）在每一步预测噪声 $\varepsilon_\theta$，然后通过重参数化间接估计干净图像。DRFusion 放弃显式噪声预测，改为直接回归融合图像 $\mathbf{X}_f$，将去噪过程隐式编码在网络输出中。这一改变使扩散框架在架构上更接近端到端网络，同时避免了噪声预测目标与融合任务目标之间的不一致——融合任务关心的不是噪声本身的精确估计，而是最终融合图像的质量。该设计的代价在于：网络需要同时承担“去噪”和“融合”两个隐含任务，对模型容量和训练策略提出了更高要求。

**决策二：联合观测校正 vs. 无约束/单图约束。** 现有扩散融合方法（如 DDFM、RFfusion）在采样过程中不施加显式的退化约束，完全依赖网络从噪声输入中生成融合结果。DDNM 等方法虽引入了观测约束，但仅针对单幅图像。DRFusion 的联合观测模型将两个源图像的退化约束与线性融合约束统一为方程组：

$$\begin{bmatrix} \mathbf{y}_1 \\ \mathbf{y}_2 \\ \mathbf{0} \end{bmatrix} = \begin{bmatrix} \mathbf{A}_1 & 0 & 0 \\ 0 & \mathbf{A}_2 & 0 \\ -\mathbf{W}_1 & -\mathbf{W}_2 & \mathbf{I} \end{bmatrix} \begin{bmatrix} \mathbf{X}_1 \\ \mathbf{X}_2 \\ \mathbf{X}_f \end{bmatrix}$$

并通过解析伪逆 $\hat{\mathbf{A}}^{\dagger}$ 实现高效投影校正。消融实验（Table 3, Figure 7, Figure 8）表明，移除该机制会导致融合图像噪声增加、细节模糊和边缘伪影加剧，客观指标全面下降——这直接验证了联合约束校正的因果作用。

**决策三：少步迭代 vs. 多步采样。** 标准扩散模型通常需要数百步（DDPM）或数十步（DDIM）采样。DRFusion 仅需 $T=3$ 步即可达到最佳性能，继续增加步数不再提升（Table 5）。这一效率优势源于两个因素的叠加：隐式去噪回归减少了每步的估计误差累积，联合校正机制在每步强制投影到约束超平面，加速了收敛。与同样采用加速采样的扩散融合方法（如 DDFM 使用 DDIM）相比，DRFusion 的少步特性使其推理效率显著优于级联式“恢复+融合”方法（Figure 5）。

### 适用边界与局限

DRFusion 的设计依赖于若干假设，这些假设也划定了其适用边界：

1. **退化过程需已知或可估计。** 联合观测模型要求退化矩阵 $\mathbf{A}_1$、$\mathbf{A}_2$ 是已知的（如高斯模糊核、下采样因子）或可通过盲估计获得。当退化类型未知或难以参数化时（如复杂非均匀退化），联合约束的施加将面临困难。论文未讨论盲退化场景下的性能。

2. **融合约束采用线性形式。** 联合观测模型中，融合约束被表达为 $\mathbf{X}_f = \mathbf{W}_1\mathbf{X}_1 + \mathbf{W}_2\mathbf{X}_2$ 的线性形式。这一假设简化了伪逆推导，但对于需要非线性融合策略的任务（如某些多曝光融合场景），该约束可能过于刚性。论文中权重图 $\mathbf{W}_1$ 由网络动态预测，部分缓解了该问题，但约束的线性本质未变。

3. **训练依赖退化模拟。** DRFusion 的自监督训练通过在干净源图像上施加模拟退化来构造训练对。当真实退化与模拟退化存在分布偏移时，模型的退化感知能力可能下降。论文未报告在真实退化数据上的泛化实验。

4. **多任务预测器的容量限制。** 噪声/权重预测器同时承担“伪噪声”预测和权重图 $\mathbf{W}_1$ 生成两个任务。在退化类型增多或源图像模态差异增大时，这一共享架构可能面临容量瓶颈。论文未对预测器的多任务设计进行消融分析。

### 待验证的开放问题

基于上述分析，以下问题值得进一步探索：

- **退化未知场景的扩展：** 当退化参数不可知时，能否将退化估计与融合过程联合优化，形成盲退化融合框架？这需要重新设计联合观测模型中的约束施加方式。
- **非线性融合约束的泛化：** 能否将线性融合约束替换为更一般的可微约束（如基于注意力的融合），同时保持解析伪逆的计算效率？
- **真实退化数据的验证：** 在真实噪声、真实模糊场景下的性能表现如何？模拟退化与真实退化之间的性能差距需要实验量化。
- **更大规模多模态扩展：** 当源图像数量超过两幅或模态类型增加（如近红外、热红外、深度图同时融合）时，联合观测模型的矩阵构造和伪逆计算是否仍能保持高效？



## 原文 PDF

![[paperPDFs/CVPR_2026/Degradation_Robust_Fusion_An_Efficient_Degradation_Aware_Diffusion_Framework_for_Multimodal_Image_Fusion_in_Arbitrary_Degradation_Scenarios.pdf]]
