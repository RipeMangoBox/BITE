---
title: "Align Your Gaussians: Text-to-4D with Dynamic 3D Gaussians and Composed Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/Align_Your_Gaussians_Text_to_4D_with_Dynamic_3D_Gaussians_and_Composed_Diffusion_Models.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/AlignYourGaussians/
code_link: null
aliases:
- AYGA
- AYGT4D3GCDM
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过组合文本到视频和文本到图像扩散模型的分数蒸馏梯度，引入基于JSD的高斯分布正则化和运动放大机制，可以解开动态学习与视觉质量保持之间的冲突，从而稳定优化过程并诱导丰富多样的运动。"
primary_logic: "动态3D高斯结合显式变形场的4D表示，配合多扩散模型组合的分数蒸馏框架，能够解耦3D外观与4D动态的生成，实现在保持高视觉质量的同时生成逼真且可组合的动态场景。"
claims:
- "在28个文本提示的用户研究中，AYG在总体质量上以53.6%的偏好率显著优于MAV3D（38.8%），证明了其生成动态场景的优越性。"
- "移除JSD正则化导致4D序列运动极小，仅出现缓慢的全局平移，验证了该正则化对学习复杂局部运动的必要性。"
- "移除运动放大器显著降低了运动量，用户偏好明显下降，表明运动放大对于增强动态表现至关重要。"
- "在4D阶段同时使用图像和视频模型比仅使用视频模型更受偏爱，尤其在3D外观和文本对齐方面，证实组合分数蒸馏有助于维持视觉质量。"
---

# Align Your Gaussians: Text-to-4D with Dynamic 3D Gaussians and Composed Diffusion Models

> [!tip] 核心洞察
> 动态3D高斯结合显式变形场的4D表示，配合多扩散模型组合的分数蒸馏框架，能够解耦3D外观与4D动态的生成，实现在保持高视觉质量的同时生成逼真且可组合的动态场景。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 对齐你的高斯：面向文本到4D的动态3D高斯与组合扩散模型 |
| 英文题名 | Align Your Gaussians: Text-to-4D with Dynamic 3D Gaussians and Composed Diffusion Models |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2312.13763) · [Project](https://research.nvidia.com/labs/toronto-ai/AlignYourGaussians/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Align Your Gaussians (AYG) |
| Dataset | 28 user study prompts (text-to-4D), 28 user study prompts, 300 text prompts (R-Precision, 4D stage) |

> [!tip] 效果简介
> - 28 user study prompts (text-to-4D) 上，Overall Quality Preference 为 53.6%，对比 38.8% (MAV3D)，变化 +14.8%。
> - 28 user study prompts 上，3D Appearance Preference 为 47.4%，对比 37.2% (MAV3D)，变化 +10.2%。
> - 28 user study prompts 上，Motion Amount Preference 为 45.9%，对比 38.8% (MAV3D)，变化 +7.1%。

## 概要

### 问题与瓶颈

从文本描述生成动态3D场景（Text-to-4D）面临一个核心张力：在缺乏强正则化时，动态3D高斯表示倾向于学习简单的全局平移而非复杂的局部运动；同时，单独使用视频扩散模型进行分数蒸馏会损害逐帧的视觉质量和3D一致性。这些瓶颈使得同时维持高视觉质量与生成逼真、丰富的运动变得困难。

### 核心方法

**Align Your Gaussians (AYG)** 通过三个关键设计解决上述问题：

1. **动态3D高斯与变形场解耦表示**：以静态3D高斯Splatting为基础，引入MLP参数化的变形场 $\Delta_{\Phi}(x, y, z, \tau)$ 建模时间动态，将外观与运动解耦。
2. **组合分数蒸馏框架**：在两阶段优化中组合文本到视频、文本到图像和3D感知多视图扩散模型的梯度，分别负责静态3D资产生成（阶段一）和动态4D序列蒸馏（阶段二），从而在引入运动的同时保持逐帧视觉质量。
3. **JSD正则化与运动放大**：基于Jensen-Shannon散度的高斯分布正则化约束3D高斯位置在时间上的均值和方差，防止运动退化为全局漂移；运动放大器通过放大逐帧得分差异增强运动表现。

### 方法定位

AYG属于基于分数蒸馏采样（SDS）的文本到4D生成方法，直接对标 **MAV3D**（基于HexPlane-NeRF表示与单一视频模型SDS）。AYG将表示从NeRF替换为动态3D高斯，将蒸馏框架从单一视频模型扩展为多模型组合，并引入正则化与运动增强机制。

### 主要结果

- 在28个文本提示的用户研究中，AYG以 **53.6%** 的总体质量偏好率显著优于MAV3D的 **38.8%**（Table 1），在3D外观（47.4% vs 37.2%）和运动量（45.9% vs 38.8%）上也均占优。
- 消融实验证实：移除JSD正则化导致运动退化为缓慢全局平移（总体质量偏好从45.8降至13.3）；移除运动放大器使运动量偏好从45.1%降至23.6%；在4D阶段仅使用视频模型则严重损害3D外观和整体质量（Table 2）。
- AYG支持自回归扩展和循环动画，可将多个动态4D对象组合为大型动态场景。

### 文本到3D生成的兴起与静态瓶颈

近年来，基于分数蒸馏采样（Score Distillation Sampling, SDS）的文本到3D生成取得了显著进展。**DreamFusion**（Poole et al., 2022）率先提出利用预训练的文本到图像扩散模型作为可微分的图像先验，通过SDS损失将2D扩散模型的监督信号反传至可微3D表示（如NeRF），实现了从文本描述直接优化3D资产。这一范式迅速催生了大量后续工作，它们通过改进3D表示、优化策略和扩散先验的质量，不断提升静态3D生成的视觉保真度和几何一致性。

然而，**静态3D资产的生成能力已趋于成熟，现实世界中的视觉内容本质上是动态的**——火焰跳动、水流涌动、人物行走，这些时间维度的变化是视觉真实感的核心组成部分。将文本到3D的生成范式扩展到时间维度，即**文本到4D生成**，成为一个自然而迫切的研究方向。

### 现有文本到4D方法的局限

**MAV3D**（Singer et al., 2023）是首个将文本到4D生成作为独立任务提出的工作。它采用HexPlane-NeRF作为4D表示，并利用单个文本到视频扩散模型进行分数蒸馏，为动态场景生成奠定了基础。然而，MAV3D及其后续工作在以下关键方面存在明显不足：

1. **运动退化为全局平移**：在缺乏强正则化的情况下，动态表示倾向于学习简单的全局平移而非复杂的局部运动。这是因为对于扩散模型而言，全局平移是一种容易满足其先验分布的“捷径”，但生成的动态场景缺乏真实的局部变形和运动多样性。

2. **视觉质量与动态学习的冲突**：单独使用视频扩散模型进行分数蒸馏时，虽然能够引入时间动态，但会严重损害逐帧的视觉质量和3D一致性。视频模型在建模单帧细节方面天然弱于图像扩散模型，导致生成的动态场景在纹理清晰度、几何精度上明显劣化。

3. **4D表示的表达能力受限**：HexPlane-NeRF等隐式表示虽然能够编码时空信息，但在渲染效率和显式几何控制方面存在局限，不利于后续的编辑、组合和物理仿真。

### 核心动机与解决思路

AYG的核心动机在于**解耦3D外观与4D动态的生成过程**，从而在保持高视觉质量的同时生成逼真且可组合的动态场景。这一动机源于以下关键洞察：

- **多模型组合可以互补优势**：文本到视频扩散模型擅长建模时间动态，但逐帧质量不足；文本到图像扩散模型擅长生成高保真单帧，但缺乏时间感知。将两者的分数蒸馏梯度进行组合，有望同时获得丰富动态和高视觉质量。

- **显式4D表示需要针对性正则化**：动态3D高斯配合变形场MLP提供了显式且可微的4D表示，但高斯点在时间维度上的演化缺乏内在约束。通过引入基于Jensen-Shannon散度（JSD）的分布正则化，强制高斯点集的均值和方差在时间上保持稳定，可以有效防止运动退化为全局平移，诱导丰富的局部运动。

- **运动信号需要主动增强**：在分数蒸馏过程中，扩散模型对运动的梯度信号可能较弱。通过运动放大机制，显式增强每帧得分与平均得分的差异，可以进一步鼓励模型学习更显著的动态行为。

基于上述动机，AYG提出了一种两阶段的文本到4D合成框架：**第一阶段**利用多视图扩散模型和文本到图像模型生成高质量静态3D资产；**第二阶段**在冻结的3D外观基础上，通过组合视频和图像扩散模型的分数蒸馏梯度，配合JSD正则化和运动放大，优化变形场以生成动态4D序列。这一设计使得3D外观与4D动态的生成得以分离，从而在根本上解决了视觉质量与动态学习之间的冲突。

## 核心方法与创新机理

AYG 提出了一套针对文本到 4D 动态场景生成的技术方案，其核心创新围绕**动态 3D 高斯表示**、**组合式分数蒸馏框架**以及**4D 优化的正则化与运动增强机制**展开，旨在解决现有方法（如 MAV3D）在运动质量和视觉保真度上的不足。

### 1. 动态 3D 高斯表示

AYG 采用**动态 3D 高斯泼溅（Dynamic 3D Gaussian Splatting）** 作为 4D 表示，将静态场景的几何与外观（3D 高斯的位置、尺度、不透明度、颜色）与时间动态解耦。具体而言，场景的运动由一个**变形场 MLP**（Deformation Field MLP）建模，该网络以 3D 坐标 $(x, y, z)$ 和时间 $\tau$ 为输入，输出每个高斯的位移 $(\Delta x, \Delta y, \Delta z)$。通过时间缩放函数 $\xi(\tau) = \tau^{0.35}$，确保在 $\tau=0$ 时位移为零，$\tau=1$ 时达到完整变形。相比 MAV3D 使用的 HexPlane-NeRF 表示，动态 3D 高斯提供了更高效的渲染和更清晰的运动建模。

### 2. 组合式分数蒸馏框架

AYG 将文本到 4D 的生成建模为**组合生成（Compositional Generation）** 问题，通过最小化渲染分布与多个扩散模型先验分布乘积之间的**反向 KL 散度**来实现：

- **阶段一（静态 3D 合成）**：组合 **MVDream**（3D 感知多视图扩散模型）和 **Stable Diffusion**（文本到图像模型）的分数蒸馏梯度，生成静态 3D 场景。
- **阶段二（动态 4D 合成）**：在静态 3D 场景基础上，仅优化变形场 $\Phi$，同时组合**文本到视频扩散模型**和**文本到图像扩散模型**的梯度。视频模型提供时序运动监督，图像模型则维持逐帧的视觉质量。

该框架的关键在于**解耦 3D 外观与 4D 动态的生成**，并利用多模型组合的梯度来平衡运动学习与视觉质量保持。相比 MAV3D 仅使用单一视频扩散模型的标准 SDS，AYG 的组合式 CSD（Classifier Score Distillation）梯度为：

$$
\nabla_{\Phi} \mathcal{L}_{\mathrm{CSD}}^{\mathrm{AYG}} = \mathbb{E}_{t, \epsilon^{\mathrm{vid}}, \epsilon^{\mathrm{im}}} \bigg[ w(t) \bigg\{ \omega_{\mathrm{vid}} \big[ \hat{\epsilon}^{\mathrm{vid}}(\mathbf{Z}, v, t) - \hat{\epsilon}^{\mathrm{vid}}(\mathbf{Z}, t) \big] + \omega_{\mathrm{im}} \big[ \hat{\epsilon}^{\mathrm{im}}(\tilde{\mathbf{Z}}, v, t) - \hat{\epsilon}^{\mathrm{im}}(\tilde{\mathbf{Z}}, t) \big] \bigg\} \frac{\partial \{ \mathbf{x} \}}{\partial \Phi} \bigg]
$$

### 3. 4D 优化的正则化与运动增强

AYG 引入了两项关键机制来稳定 4D 优化并增强运动表现：

- **基于 JSD 的高斯分布正则化**：计算不同时刻 $\tau$ 下全体 3D 高斯位置的均值 $\nu_\tau$ 和对角协方差 $\Gamma_\tau$，并通过修正的 Jensen-Shannon 散度 $\mathrm{JSD}(\mathcal{N}(\nu_0, \Gamma_0) \| \mathcal{N}(\nu_\tau, \Gamma_\tau))$ 进行正则化。该正则化防止 3D 高斯随时间发生全局漂移，迫使网络学习复杂的局部运动，而非退化为简单的全局平移。消融实验证实，移除该正则化后运动几乎消失，仅剩缓慢的全局平移。

- **运动放大器（Motion Amplifier）**：通过放大每帧得分与平均得分的差异 $\delta_{\mathrm{cls}~i}^{\mathrm{vid}} \leftarrow \delta_{\mathrm{cls}~i}^{\mathrm{vid}} + \omega_{\mathrm{ma}} (\delta_{\mathrm{cls}~i}^{\mathrm{vid}} - \overline{\delta_{\mathrm{cls}~i}^{\mathrm{vid}}})$，增强视频模型提供的运动信号，从而诱导更丰富多样的动态效果。消融实验表明，移除运动放大器后运动量显著降低，用户偏好大幅下降。

此外，AYG 还支持**自回归扩展**：通过在重叠区域插值两个 4D 序列的变形场 $\Delta_{\Phi_{12}}^{\mathrm{interpol}} = (1 - \chi(\tau)) \Delta_{\Phi_{1}} + \chi(\tau) \Delta_{\Phi_{2}}$，可生成更长的动态序列，并允许在扩展过程中切换文本提示，实现动作的组合与衔接。

**Align Your Gaussians (AYG)** 是一种文本到4D动态场景的生成系统，其核心设计遵循一个解耦的两阶段流水线：首先合成高质量的静态3D资产，再为其注入时间动态以生成4D序列。这一设计的关键优势在于，4D阶段的动态学习方法可以独立于3D资产的来源，未来可泛化至其他3D生成系统或合成资产。

### 两阶段流水线

**阶段一：静态3D高斯生成。** 系统首先从文本提示出发，利用3D高斯泼溅（3D Gaussian Splatting）表示静态场景的几何与外观（包含位置 $\mu_i$、尺度 $\sigma_i$、不透明度 $\eta_i$ 和颜色 $\ell_i$）。该阶段通过组合分数蒸馏（Compositional Score Distillation）框架进行优化，同时利用多视图扩散模型（MVDream）和文本到图像扩散模型（Stable Diffusion）的梯度信号。具体而言，优化目标是最小化渲染分布 $q_\theta$ 与多视图先验 $p_{3\mathrm{D}}$ 和图像先验 $p_{\mathrm{im}}$ 乘积之间的反向KL散度。此阶段还引入了**视点引导（View Guidance）**，通过构造方向相关的文本提示增强项来改善规范姿态的生成质量。

**阶段二：动态4D序列生成。** 在静态场景的基础上，AYG冻结所有3D高斯参数，仅优化一个由MLP参数化的**变形场（Deformation Field）** $\Delta_{\Phi}(x, y, z, \tau) = (\Delta x, \Delta y, \Delta z)$，它为每个3D位置和时间 $\tau$ 预测位移量。变形场通过时间缩放函数 $\xi(\tau) = \tau^{0.35}$ 确保 $\tau=0$ 时位移为零，$\tau=1$ 时为完整变形。此阶段再次运用组合分数蒸馏，但将组合对象切换为文本到视频扩散模型和文本到图像扩散模型——视频模型提供跨帧的运动一致性梯度，图像模型则逐帧维持视觉质量，从而解开动态学习与外观保持之间的冲突。

### 关键模块与数据流

整个流水线的数据流可概括为：文本提示 → 阶段一（多视图+图像扩散模型蒸馏）→ 静态3D高斯 → 阶段二（视频+图像扩散模型蒸馏，仅优化变形场）→ 动态4D序列。其中，阶段二的梯度通过可微渲染过程反向传播至变形场，驱动3D高斯在时间轴上的位移。

为实现稳定且富有表现力的运动生成，AYG在阶段二中嵌入了三个关键机制：

- **JSD正则化（JSD-based Regularization）**：计算不同时刻 $\tau$ 下全体3D高斯位置的均值 $\nu_\tau$ 和对角协方差矩阵 $\Gamma_\tau$，通过修正的Jensen-Shannon散度约束这些统计量在时间上保持稳定，防止运动退化为简单的全局平移。
- **运动放大器（Motion Amplifier）**：对视频模型提供的逐帧分类器得分差异进行放大，公式为 $\delta_{\mathrm{cls}~i}^{\mathrm{vid}} \leftarrow \delta_{\mathrm{cls}~i}^{\mathrm{vid}} + \omega_{\mathrm{ma}} (\delta_{\mathrm{cls}~i}^{\mathrm{vid}} - \overline{\delta_{\mathrm{cls}~i}^{\mathrm{vid}}})$，以增强学习到的运动幅度。
- **自回归扩展（Autoregressive Extension）**：通过在重叠区域对两个4D序列的变形场进行插值 $\Delta_{\Phi_{12}}^{\mathrm{interpol}} = (1 - \chi(\tau)) \Delta_{\Phi_{1}} + \chi(\tau) \Delta_{\Phi_{2}}$，并结合插值正则化损失，实现长序列生成，且支持在扩展过程中切换文本提示（如从“走路”变为“跑步”）。

### 输入输出规范

- **输入**：描述动态场景的文本提示（如“A dog wearing a Superhero outfit with red cape flying through the sky”），以及可选的负向提示（如“low motion, static statue, not moving, no motion”）。
- **输出**：以动态3D高斯表示的4D序列，可在任意视点和时间步下渲染为RGB图像。系统还支持将多个独立生成的动态对象组合到同一大场景中，以及创建循环动画。

### 4D表示：动态3D高斯与变形场

AYG的4D表示采用**动态3D高斯泼溅**与**变形场**的组合，将3D外观与时间动态解耦表示。静态场景由一组3D高斯表示，每个高斯具有位置均值 $\mu_i$、尺度 $\sigma_i$、不透明度 $\eta_i$ 和颜色 $\ell_i$。像素颜色通过沿射线的alpha合成计算：

$$
\mathcal{C}(\mathbf{p}) = \sum_{i=1}^{N} \ell_i \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j)
$$

其中每个投影2D高斯对像素 $\mathbf{p}$ 的不透明度贡献为：

$$
\alpha_i = \eta_i \exp\left[-\frac{1}{2}(\mathbf{p} - \hat{\pmb{\mu}}_i)^{\top} \hat{\Sigma}_i^{-1} (\mathbf{p} - \hat{\pmb{\mu}}_i)\right]
$$

场景动态由一个**MLP参数化的变形场**建模，对任意3D位置 $(x,y,z)$ 和时间 $\tau$ 预测位移：

$$
\Delta_{\Phi}(x, y, z, \tau) = (\Delta x, \Delta y, \Delta z)
$$

为确保在 $\tau=0$ 时变形为零、$\tau=1$ 时为完整变形，引入时间缩放函数 $\xi(\tau) = \tau^{0.35}$。

### 组合分数蒸馏框架

AYG将文本到4D生成形式化为**组合生成**问题，通过最小化渲染分布与多个扩散模型分布乘积之间的反向KL散度实现。

**阶段1（3D合成）**：组合MVDream多视图扩散模型和Stable Diffusion文本到图像模型，目标为：

$$
\mathrm{KL}\Bigg( q_{\pmb\theta} \left( \left\{ \mathbf{z}^{c_i} \right\}_4, \left\{ \tilde{\mathbf{z}}^{\tilde{c}_j} \right\}_K \right) \Bigg| \Bigg| p_{3\mathrm{D}}^{\alpha} \left( \left\{ \mathbf{z}^{c_i} \right\}_4 \right) \prod_{j=1}^{K} p_{\mathrm{im}}^{\beta} \left( \tilde{\mathbf{z}}^{\tilde{c}_j} \right) \Bigg )
$$

**阶段2（4D合成）**：组合文本到视频扩散模型和文本到图像扩散模型，仅优化变形场参数 $\Phi$：

$$
\mathrm{KL}( q_{\Phi} ( \{ \mathbf{z}_{\tau_i}^{c_i} \}_F, \{ \tilde{\mathbf{z}}_{\tilde{\tau}_j}^{\tilde{c}_j} \}_M ) \; p_{\mathrm{vid}}^{\gamma} ( \{ \mathbf{z}_{\tau_i}^{c_i} \}_F ) \prod_{j=1}^{M} p_{\mathrm{im}}^{\kappa} ( \tilde{\mathbf{z}}_{\tilde{\tau}_j}^{\tilde{c}_j} ) )
$$

### 分类器分数蒸馏梯度

阶段2的实际优化采用简化后的**分类器分数蒸馏**梯度，去除噪声控制变量：

$$
\nabla_{\Phi} \mathcal{L}_{\mathrm{CSD}}^{\mathrm{AYG}} = \mathbb{E}_{t, \epsilon^{\mathrm{vid}}, \epsilon^{\mathrm{im}}} \bigg[ w(t) \bigg\{ \omega_{\mathrm{vid}} \big[ \hat{\epsilon}^{\mathrm{vid}}(\mathbf{Z}, v, t) - \hat{\epsilon}^{\mathrm{vid}}(\mathbf{Z}, t) \big] + \omega_{\mathrm{im}} \big[ \hat{\epsilon}^{\mathrm{im}}(\tilde{\mathbf{Z}}, v, t) - \hat{\epsilon}^{\mathrm{im}}(\tilde{\mathbf{Z}}, t) \big] \bigg\} \frac{\partial \{ \mathbf{x} \}}{\partial \Phi} \bigg]
$$

其中 $\omega_{\mathrm{vid}}$ 和 $\omega_{\mathrm{im}}$ 分别控制视频模型和图像模型的梯度权重，$v$ 为文本提示条件。该梯度通过可微渲染过程反向传播至变形场参数。

### JSD正则化

为防止4D高斯在优化中退化为简单的全局平移，AYG引入基于**Jensen-Shannon散度**的正则化。对每个时间 $\tau$，计算所有动态3D高斯的3D均值 $\nu_\tau$ 和对角协方差矩阵 $\Gamma_\tau$，正则化其与初始状态 $\tau=0$ 的分布差异。简化后的损失函数为：

$$
\mathcal{L}_{\mathrm{JSD-Reg.}} = \sum_{i \in \{x,y,z\}} \left[ -\frac{1}{2}\log[2] + \frac{1}{2}\log[\Gamma_0^i + \Gamma_\tau^i] - \frac{1}{4}\log[\Gamma_0^i] - \frac{1}{4}\log[\Gamma_\tau^i] + \frac{1}{4}\frac{(\nu_\tau^i - \nu_0^i)^2}{\Gamma_0^i + \Gamma_\tau^i} \right]
$$

该正则化同时约束高斯集合的均值漂移和方差膨胀，迫使模型学习局部、多样化的运动模式。

### 运动放大机制

为进一步增强动态表现，AYG对视频模型输出的逐帧分类器得分差异进行放大：

$$
\delta_{\mathrm{cls}~i}^{\mathrm{vid}} \leftarrow \delta_{\mathrm{cls}~i}^{\mathrm{vid}} + \omega_{\mathrm{ma}} (\delta_{\mathrm{cls}~i}^{\mathrm{vid}} - \overline{\delta_{\mathrm{cls}~i}^{\mathrm{vid}}})
$$

其中 $\overline{\delta_{\mathrm{cls}~i}^{\mathrm{vid}}}$ 为所有帧得分的均值，$\omega_{\mathrm{ma}}$ 为放大系数。该操作增大了帧间得分差异，从而诱导更显著的运动。

### 自回归扩展

为生成长序列，AYG在两个4D序列的重叠区域对变形场进行平滑插值：

$$
\Delta_{\Phi_{12}}^{\mathrm{interpol}} = (1 - \chi(\tau)) \Delta_{\Phi_{1}} + \chi(\tau) \Delta_{\Phi_{2}}
$$

其中 $\chi(\tau)$ 为平滑混合系数，并通过插值正则化损失 $\mathcal{L}_{\mathrm{Interpol-Reg.}} = ||\Delta_{\Phi_{1}} - \Delta_{\Phi_{12}}^{\mathrm{interpol}}||_{2}^{2}$ 约束第二个变形场在重叠区域接近第一个。

## 实验与关键发现

### 主实验结果与基线对比

AYG在文本到4D合成任务上与先前方法**MAV3D**进行了系统对比。由于4D动态场景缺乏标准化的自动评估指标，作者将用户研究作为主要评判手段，同时补充了R-Precision指标以对齐MAV3D的评估协议。

在28个文本提示的用户研究中（Table 1），AYG在所有六个评估维度上均优于MAV3D：

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2312_13763/figures/009_Table_1.jpg]]
*Table 1: Comparison to MAV3D [79] by user study on synthesized 4D scenes with 28 text prompts. Numbers are percentages*

- **总体质量（Overall Quality）**：AYG获得53.6%的偏好率，MAV3D为38.8%（差距+14.8%，另有7.6%的参与者选择“无偏好”）。这是最核心的综合指标，表明用户对AYG生成的动态场景整体满意度显著更高。
- **3D外观（3D Appearance）**：AYG以47.4%对37.2%领先（差距+10.2%），验证了组合分数蒸馏中图像扩散模型对维持逐帧视觉质量的关键作用。
- **3D文本对齐（3D Text Alignment）**：AYG以50.5%对36.2%领先（差距+14.3%），说明静态3D资产生成阶段的多视图扩散模型与视点引导机制有效提升了语义一致性。
- **运动量（Motion Amount）**：AYG以45.9%对38.8%领先（差距+7.1%），验证了运动放大器和JSD正则化在诱导丰富运动方面的效果。
- **运动文本对齐（Motion Text Alignment）**：AYG以47.4%对33.7%领先（差距+13.7%），表明视频扩散模型的组合蒸馏能更好地捕捉文本描述中的动态语义。
- **运动真实感（Motion Realism）**：AYG以47.4%对36.7%领先（差距+10.7%），说明JSD正则化有效抑制了不自然的全局漂移，使运动更加逼真。

值得注意的是，在R-Precision指标上（Table 5），AYG得分为81.7，略低于MAV3D的83.7（差距-2.0）。但作者明确指出，R-Precision仅衡量静态3D质量（通过CLIP评估单帧渲染与文本的匹配度），完全不捕捉动态信息，因此用户研究才是评估4D生成的主要且更有效的方式。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2312_13763/figures/014_Table_5.jpg]]
*Table 5: R-Precision comparison to MAV3D [79] with the 300 text prompts also used by Singer et al. [78] and Singer et al. [79]*

定性对比（Figure 8, Figure 14）进一步支撑了定量结论：在“A dog wearing a Superhero outfit with red cape flying through the sky”等复杂动态提示下，AYG生成的序列展现出更丰富的局部运动（如披风飘动），而MAV3D的运动趋于缓慢的全局平移。

### 消融实验

在30个文本提示上进行的消融用户研究（Table 2）系统验证了AYG各核心组件的贡献。每项消融将完整AYG与移除特定组件的变体进行配对比较。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2312_13763/figures/010_Table_2.jpg]]
*Table 2: Ablation study by user study on synthesized 4D scenes with 30 text prompts. For each pair of numbers, the left number is the percentage that the full AYG model is preferred and the right number indicates preference percentage for ablated model as described in left column. The numbers do not add up to 100 and the difference is due to users voting “no preference” (details in Supp. Material)*

**JSD正则化（w/o JSD-based regularization）**：移除该正则化后，总体质量偏好从完整模型的45.8%骤降至消融模型的13.3%（差距+32.5%）。如Appendix F.2所述，消融模型的4D序列运动极小，仅出现缓慢的全局平移，3D高斯分布随时间发生不受控的漂移。这直接验证了JSD正则化对学习复杂局部运动的必要性——它通过约束高斯分布在时间维度上的均值和方差稳定性，迫使变形场学习有意义的局部变形而非简单的整体位移。

**运动放大器（w/o motion amplifier）**：移除运动放大器后，运动量维度的用户偏好从完整模型的45.1%降至消融模型的23.6%（差距+21.5%）。总体质量偏好也从50.0%降至16.7%（差距+33.3%）。该结果证实了运动放大机制——通过放大每帧得分与平均得分的差异$\delta_{\mathrm{cls}~i}^{\mathrm{vid}} \leftarrow \delta_{\mathrm{cls}~i}^{\mathrm{vid}} + \omega_{\mathrm{ma}} (\delta_{\mathrm{cls}~i}^{\mathrm{vid}} - \overline{\delta_{\mathrm{cls}~i}^{\mathrm{vid}}})$——能有效增强动态表现，使生成的4D序列更具视觉冲击力。

**4D阶段的图像扩散模型（w/o image DM score in 4D stage）**：仅使用视频扩散模型进行4D蒸馏时，总体质量偏好从完整模型的48.3%降至消融模型的13.3%（差距+35.0%）。3D外观维度也出现严重劣化（完整模型40.0%对消融模型16.7%）。这强有力地证明了组合分数蒸馏的核心设计理念：视频模型负责提供时序动态信息，而图像模型维持逐帧的视觉质量和3D一致性，二者缺一不可。

**视频模型fps采样策略**：分别仅使用fps=4或fps=12的视频模型时，完整AYG（使用多fps采样）在运动量和总体质量上均被显著偏好。这与Figure 15-17的定性观察一致：低fps条件生成更大运动幅度但时序一致性较差，高fps条件生成平滑但运动较小的视频——多fps采样策略有效平衡了运动量与一致性。

**4D阶段引入MVDream（4D stage with MVDream）**：在4D阶段额外加入MVDream多视图扩散模型后，总体质量偏好从完整模型的55.0%降至消融模型的15.0%（差距+40.0%）。作者分析这可能是因为MVDream的梯度与视频模型梯度产生冲突，导致运动异常或整体运动减少。

**视点引导消融（Table 7）**：在静态3D阶段移除视点引导后，完整AYG在3D外观上以40.0%对20.0%被显著偏好，验证了方向性文本提示增强对改善规范姿态质量的有效性。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2312_13763/figures/016_Table_7.jpg]]
*Table 7: Ablation study on view guidance by user study on synthesized static 3D scenes from AYG’s initial 3D stage. We used 30 text prompts, the same as in the other ablation studies. Numbers are percentages*

### 失败模式与局限性

尽管AYG在文本到4D合成上取得了领先性能，论文明确指出了以下局限性：

1. **拓扑变化困难**：当前方法难以生成动态对象的拓扑变化（如物体分裂或合并），因为变形场本质上是一个连续映射，无法自然地表示拓扑结构的突变。

2. **对象中心生成限制**：方法目前局限于以对象为中心的生成场景，扩展到包含复杂背景的大场景仍具挑战。虽然Figure 1展示了多动态对象组合的初步结果，但背景（如地面）仍需单独处理。

3. **个性化4D合成未探索**：论文未研究将AYG与DreamBooth或图像到3D方法结合以支持个性化4D资产生成。

4. **计算开销**：依赖多个预训练扩散模型（MVDream、Stable Diffusion、自训练的视频扩散模型）进行分数蒸馏，计算开销较大。此外，视频模型的基础序列长度限制了单次生成的4D序列长度，需借助自回归扩展方案。

5. **评估协议的主观性**：用户研究虽为4D评估提供了有效手段，但存在固有的主观性——参与者的判断可能受视觉呈现方式、个人偏好等因素影响。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2312_13763/figures/011_Table_3.jpg]]
*Table 3: Hyperparameters for the first stage (3D synthesis)*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2312_13763/figures/015_Table_6.jpg]]
*Table 6: Ablation study by user study on synthesized 4D scenes with 30 text prompts. For each pair of numbers, the left number is the percentage that the full AYG model is preferred and the right number indicates preference percentage for ablated model as described in left column. The numbers do not add up to 100 and the difference is due to users voting “no preference” (table copied here from main paper for extended discussion in Appendix F.2)*

## 定位与知识库关联

### 与前驱工作的关系

AYG 直接对标的前驱工作是 **MAV3D**（Singer et al.），后者首次将文本到视频扩散模型的分数蒸馏采样（SDS）引入文本到4D生成，采用 HexPlane-NeRF 作为4D表示。AYG 在以下关键维度上进行了系统性改进：

1.  **4D 表示替换**：将 MAV3D 的 HexPlane-NeRF 替换为动态 3D 高斯泼溅（Dynamic 3D Gaussian Splatting）加变形场 MLP。这一替换不仅提升了渲染效率，更重要的是实现了静态外观与动态形变的显式解耦——这是 AYG 两阶段组合生成框架的基础。

2.  **分数蒸馏框架升级**：MAV3D 仅使用单一文本到视频扩散模型进行 SDS。AYG 将其扩展为**组合分类器分数蒸馏（Compositional CSD）**，在4D阶段同时组合视频扩散模型和图像扩散模型的梯度。其核心动机来自一个关键观察：单独使用视频模型蒸馏会损害逐帧视觉质量和3D一致性，而图像模型的加入可以维持高视觉质量。

3.  **优化正则化引入**：MAV3D 未使用显式的运动正则化。AYG 发现，在缺乏强正则化时，动态 3D 高斯倾向于学习简单的全局平移而非复杂的局部运动。为此，AYG 引入了基于 Jensen-Shannon 散度（JSD）的高斯分布正则化，约束 3D 高斯集合在时间维度上的均值和方差保持稳定，从而诱导丰富多样的局部运动。

4.  **运动增强机制**：AYG 提出运动放大器（Motion Amplifier），通过放大逐帧分数差异来增强学习到的运动幅度。这是 MAV3D 完全不具备的能力。

在更广泛的谱系中，AYG 继承并融合了以下技术路线：
-   **3D 高斯泼溅**（Kerbl et al., 2023）：提供高效的显式3D表示和可微渲染。
-   **分数蒸馏采样**（Poole et al., DreamFusion, 2022）：将扩散模型先验蒸馏到3D表示的范式。
-   **多视图扩散模型**（MVDream, Shi et al., 2023）：在3D阶段提供3D一致性先验。
-   **变形场**（如 Nerfies, Park et al., 2021；D-NeRF, Pumarola et al., 2021）：为静态3D表示注入时间动态。

### 适用边界与局限

AYG 的适用边界和已知局限包括：

-   **拓扑变化困难**：当前方法难以生成动态对象的拓扑变化（如物体分裂或合并）。变形场 MLP 本质上是连续形变建模，不适合处理拓扑结构的突变。
-   **对象中心化生成**：方法目前局限于以对象为中心的动态场景生成，扩展到包含复杂背景的大场景仍具挑战。论文展示了多个动态对象的组合，但每个对象仍需独立生成。
-   **计算开销**：依赖多个预训练扩散模型（MVDream、Stable Diffusion、自训练视频扩散模型），计算开销较大。视频模型的基础序列长度（16帧）限制了单次生成的4D序列长度，需通过自回归扩展来延长。
-   **视频模型与多视图模型的梯度冲突**：消融实验表明，在4D阶段加入 MVDream 会导致运动异常或整体运动减少，用户偏好降低。这说明视频模型与多视图模型的梯度在4D阶段存在冲突，如何高效平衡二者仍是开放问题。
-   **个性化生成未探索**：未研究个性化4D合成，例如结合 DreamBooth 或图像到3D的初始资产生成。

### 开放问题

论文明确列出或隐含的开放问题包括：

1.  **个性化4D生成**：能否将 AYG 扩展到个性化4D生成，如结合 DreamBooth3D 或图像引导的3D方法，从用户提供的图像生成特定对象的动态场景？
2.  **角色动画结合**：能否将 AYG 与角色动画模型结合，使生成的对象遵循预定义的合成运动轨迹？
3.  **物理仿真资产提取**：能否从合成的4D场景中提取可直接用于物理仿真的动画资产（如带蒙皮的网格）？
4.  **正则化距离探索**：探索其他分布距离（如 Wasserstein 距离）作为4D高斯正则化是否比 JSD 更有效。
5.  **梯度平衡优化**：如何高效地平衡视频模型与多视图模型在4D阶段的梯度，避免冲突，从而同时获得高质量运动和多视图一致性？
6.  **视频模型扩展**：在更大规模数据集上训练视频扩散模型是否能进一步提升4D蒸馏性能，并支持更长的序列生成？

## 原文 PDF

![[paperPDFs/CVPR_2024/Align_Your_Gaussians_Text_to_4D_with_Dynamic_3D_Gaussians_and_Composed_Diffusion_Models.pdf]]
