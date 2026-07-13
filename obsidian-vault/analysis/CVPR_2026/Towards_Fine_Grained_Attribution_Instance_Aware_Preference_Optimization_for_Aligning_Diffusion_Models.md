---
title: "Towards Fine-Grained Attribution: Instance-Aware Preference Optimization for Aligning Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Towards_Fine_Grained_Attribution_Instance_Aware_Preference_Optimization_for_Aligning_Diffusion_Models.pdf
project_link: null
code_link: null
aliases:
- IIAPO
- TFGAIAPOADM
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 实例级信用分配机制：通过构建首个大规模实例级偏好数据集，为每个实例对标注细粒度偏好标签，并在训练中引入动态重加权掩码，对不同实例区域施加差异化损失权重（对与全局偏好冲突的劣质实例降低权重），从而实现精确的空间信用分配。
primary_logic: 将扩散模型对齐从图像级推进到实例级，利用视觉语言模型和检测模型的自动标注管线生成大规模细粒度偏好数据，并通过空间自适应重加权损失实现精准的信用分配，同时大幅提升生成质量与训练效率。
claims:
- 约46.3%的实例对存在全局偏好与实例级偏好冲突，揭示图像级监督的严重歧义。
- 在HPD v2基准上，IAPO微调的SD1.5相比原始模型Aesthetic Score提高0.4923，PickScore提高1.1803，HPS提高1.7575。
- IAPO训练效率比InPO高3.27倍，比Diffusion-DPO高11.64倍。
- 消融实验表明，降低冲突实例的权重w_neg能持续提升Aesthetic、PickScore和HPS。
---

# Towards Fine-Grained Attribution: Instance-Aware Preference Optimization for Aligning Diffusion Models

> [!tip] 核心洞察
> 将扩散模型对齐从图像级推进到实例级，利用视觉语言模型和检测模型的自动标注管线生成大规模细粒度偏好数据，并通过空间自适应重加权损失实现精准的信用分配，同时大幅提升生成质量与训练效率。

| 字段 | 内容 |
|------|------|
| 中文题名 | 走向细粒度归因：用于对齐扩散模型的实例感知偏好优化 |
| 英文题名 | Towards Fine-Grained Attribution: Instance-Aware Preference Optimization for Aligning Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Sun_Towards_Fine-Grained_Attribution_Instance-Aware_Preference_Optimization_for_Aligning_Diffusion_Models_CVPR_2026_paper.html) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | IAPO (Instance-Aware Preference Optimization) |
| Dataset | HPD v2, Training Efficiency |

> [!tip] 效果简介
> - HPD v2 上，Aesthetic Score (mean) IAPO-SD1.5 (5.7270) vs SD1.5 base (5.2347) (+0.4923)；PickScore (mean) IAPO-SD1.5 (22.5803) vs SD1.5 base (21.40) (+1.1803)；HPS (mean) IAPO-SD1.5 (29.1575) vs SD1.5 base (27.40) (+1.7575)。
> - Training Efficiency (Pick-a-Pic v2) 上，相对训练速度（倍） IAPO (17.6 H800 hours) vs InPO (57.5 hours) (3.27× faster)；相对训练速度（倍） IAPO vs Diffusion-DPO (11.64× faster)；相对训练速度（倍） IAPO vs KTO (60.0× faster)。

## 概要

### 问题背景

现有扩散模型对齐方法（如 Diffusion-DPO、InPO、KTO）普遍采用**图像级偏好监督**：为整幅图像赋予一个全局的“胜/负”标签，并将奖励或惩罚信号均匀传播至图像中的所有像素。这种粗粒度的信用分配机制存在根本性缺陷——它无法区分图像中不同实例的质量差异，导致全局偏好与局部实例质量之间出现严重歧义。例如，一幅在整体构图、光照上更优的图像，其某个具体实例（如一只鹰的爪子数量）可能明显劣于对应负样本中的同一实例，但图像级监督仍会不加区分地奖励该劣质实例、惩罚优质实例，使优化轨迹扭曲且训练效率低下。

### 核心方法

本文提出 **IAPO（Instance-Aware Preference Optimization）**，将扩散模型对齐从图像级推进到**实例级**。核心思路是引入**实例级信用分配**，包含两个关键组件：

1. **大规模实例级偏好数据集**：通过 Planner（VLM 识别共同实例）、Detector（开放集检测模型定位边界框）和 Judge（VLM 对比裁剪后的实例块）三阶段自动标注管线，在 Pick-a-Pic v2 上为 959,040 个图像对生成细粒度实例偏好标注，共获得 1,205,593 个实例偏好对。
2. **实例感知 DPO 损失**：在训练中引入动态重加权掩码，根据实例级偏好标签对图像空间进行差异化调制——对与全局偏好冲突的劣质实例区域施加降低的权重 $w_{\text{neg}}$，抑制其学习信号；其他区域保持正常权重。

### 关键发现

- **全局偏好与实例级偏好存在大规模冲突**：约 **46.3%** 的实例对（558,352 对）的实例级偏好与图像级全局偏好不一致，定量揭示了图像级监督的严重歧义。
- **实例级信用分配显著提升生成质量**：在 HPD v2 基准上，IAPO 微调的 SD1.5 相比原始模型在 Aesthetic Score 上提升 **+0.4923**，PickScore 提升 **+1.1803**，HPS 提升 **+1.7575**。
- **训练效率大幅领先现有方法**：IAPO 的训练速度比 InPO 快 **3.27 倍**，比 Diffusion-DPO 快 **11.64 倍**，比 KTO 快 **60.0 倍**。
- **消融实验验证重加权机制有效性**：随着冲突实例权重 $w_{\text{neg}}$ 从 1.0 降至 0.0，Aesthetic、PickScore 和 HPS 均单调提升，当 $w_{\text{neg}}=0$（即完全屏蔽冲突实例的学习信号）时取得最优结果。

### 方法定位

IAPO 属于**基于偏好优化的扩散模型对齐方法**，与 InPO（Lu et al., CVPR 2025）、Diffusion-DPO（Wallace et al., CVPR 2023）、KTO（Li et al., NeurIPS 2024）等方法共享 Bradley-Terry 偏好建模框架。其核心差异在于将信用分配从**图像空间**分解到**实例空间**，通过空间自适应重加权损失实现精细化的学习信号调制，而非对整幅图像施加均匀的奖励/惩罚。这一思路在方法谱系上开创了“细粒度偏好对齐”的新方向，为后续研究将信用分配进一步细化到像素级或时空级提供了基础框架。

### 扩散模型对齐：从图像级偏好到实例级信用分配

近年来，基于人类偏好的扩散模型对齐方法取得了显著进展。以 **Diffusion-DPO**（Wallace et al., CVPR 2023）为代表的方法将直接偏好优化引入扩散模型，利用图像级偏好对（即整体“胜/负”标签）引导模型生成更符合人类审美的高质量图像。随后，**InPO**（Lu et al., CVPR 2025）和 **KTO**（Li et al., NeurIPS 2024）等方法分别从逆转效率和效用最大化角度进一步推动了该范式的发展。

然而，这些方法的共同基础——图像级偏好监督——存在一个根本性的缺陷：**奖励信号在空间维度上均匀传播，无法区分图像中不同实例的质量差异**。如图1所示，现有方法将整幅图像视为一个不可分割的整体，对所有像素施加相同的奖励或惩罚，而忽略了图像内部不同语义区域之间的质量异质性。

这一缺陷的后果是严重的。当一幅“获胜”图像在整体构图、光照等方面表现优异，但其中某个具体实例（如一只鹰的爪子数量错误）存在明显瑕疵时，全局偏好仍然会奖励该劣质实例；反之，“失败”图像中表现良好的实例则被错误地惩罚。这种**全局偏好与局部实例质量的不一致**导致优化轨迹扭曲，模型在提升整体质量的同时，可能无意中强化了局部缺陷，训练效率也因此低下。

### 核心瓶颈：偏好冲突的普遍性与信用分配的缺失

本文通过大规模数据分析揭示了这一问题的严重程度。在基于 Pick-a-Pic v2 数据集构建的实例级偏好数据集中，**约46.3%的实例对存在全局偏好与实例级偏好冲突**（558,352/1,205,593），这意味着近半数的训练样本都包含歧义信号。当模型试图同时满足全局偏好和局部实例质量时，这些冲突信号会相互抵消，导致收敛缓慢且优化方向不明确。

这一发现指向了扩散模型对齐领域的核心瓶颈：**缺乏实例级的信用分配机制**。信用分配（credit assignment）是强化学习中的经典问题，指如何将全局奖励信号正确地归因到各个局部行为。在图像生成中，这意味着需要精确识别每个实例对整体偏好的贡献，并对优质实例和劣质实例施加差异化的学习信号。

### 本文动机：走向细粒度归因

针对上述瓶颈，本文提出 **IAPO（Instance-Aware Preference Optimization）**，将扩散模型对齐从图像级推进到实例级。核心思路是双重的：

1. **构建实例级偏好数据集**：利用视觉语言模型和检测模型的自动标注管线，为图像对中的每个匹配实例生成细粒度偏好标签，使模型能够感知全局偏好与局部实例质量之间的冲突。
2. **设计空间自适应重加权损失**：在训练过程中，通过动态重加权掩码对不同实例区域施加差异化损失权重——对与全局偏好冲突的劣质实例降低学习信号强度，从而抑制歧义信号对优化过程的干扰，实现精准的空间信用分配。

这一框架不仅解决了偏好冲突导致的优化扭曲问题，还在显著提升生成质量的同时大幅提高了训练效率——IAPO的训练速度比InPO快3.27倍，比Diffusion-DPO快11.64倍，充分证明了细粒度信用分配在扩散模型对齐中的关键价值。

## 核心方法与创新机理

IAPO 的核心创新在于将扩散模型偏好对齐从**图像级**推进到**实例级**，通过两个紧密耦合的 changed slot 解决图像级监督固有的空间歧义问题。

### 创新动因：图像级偏好监督的空间歧义

现有扩散模型对齐方法（如 **Diffusion-DPO** (Wallace et al., CVPR 2023)、**InPO** (Lu et al., CVPR 2025)、**KTO** (Li et al., NeurIPS 2024)）均采用图像级偏好对（整体胜/负标签）进行训练，奖励信号在空间维度上均匀传播至所有像素。这导致一个严重问题：**全局偏好与局部实例质量不一致**。例如，一张图像因整体构图优秀而被标注为“获胜”，但其中某个实例（如一只鹰）却存在明显异常（如四只爪子），而“失败”图像中的同一实例反而生成正确。图像级监督无法区分这种差异，会错误地奖励劣质实例区域、惩罚优质实例区域，扭曲优化轨迹。

IAPO 通过构建首个大规模实例级偏好数据集，首次量化了这一问题的严重性：在自动标注的 1,205,593 个实例对中，**约 46.3%（558,352 对）存在全局偏好与实例级偏好的冲突**，充分揭示了图像级监督的深层歧义。

### Changed Slot 1：从图像级偏好到实例级偏好数据集

**Baseline 做法**：仅使用图像级偏好标签（整体胜/负），缺乏对图像内部不同实例的细粒度质量信号。

**IAPO 做法**：构建了一个自动标注管线，为 Pick-a-Pic v2 中的每个图像对生成实例级偏好标注。数据集格式为：

$$\mathcal{D} = \{ (\pmb{x}_0^w, \pmb{x}_0^l, \pmb{c}, \{ (\pmb{b}_n^w, \pmb{b}_n^l, \rho_n) \}_{n=1}^N ) \}$$

其中 $\pmb{b}_n^w$ 和 $\pmb{b}_n^l$ 分别为获胜和失败图像中第 $n$ 个共同实例的边界框，$\rho_n \in \{0, 1\}$ 表示该实例对的偏好是否与全局偏好冲突（$\rho_n=1$ 表示冲突，即失败图像中的该实例实际更优）。

该自动标注管线由三个角色协同完成：
- **Planner**：利用 VLM 识别图像对中的共同实例；
- **Detector**：使用开放集检测模型（Grounding DINO）定位实例边界框；
- **Judge**：利用 VLM 对比裁剪后的实例块，判定实例级偏好。

最终从 Pick-a-Pic v2 的 959,040 个图像对中自动标注了 1,205,593 个实例偏好对，为细粒度对齐提供了数据基础。

### Changed Slot 2：从均匀损失到实例感知 DPO 损失

**Baseline 做法**：标准 DPO/Diffusion-DPO 损失对整幅图像的所有像素均匀施加奖励或惩罚信号，无法区分不同实例区域。

**IAPO 做法**：设计了**动态重加权掩码**机制，在空间上调制损失函数，实现精确的实例级信用分配。核心机制如下：

首先，为每个实例生成权重掩码，对与全局偏好冲突的实例区域（$\rho_n=1$）赋予权重 $w_{\text{neg}} \in [0, 1]$，其余区域保持权重 1：

$$M _ { n } ^ { * } ( i , j ) = \left\{ { \begin{array} { l l } { w _ { \mathrm { n e g } } } & { { \mathrm { i f } } \ ( i , j ) \in b _ { n } ^ { * } \ { \mathrm { a n d } } \ \rho _ { n } = 1 } \\ { 1 } & { { \mathrm { o t h e r w i s e } } } \end{array} } \right.$$

然后，将所有实例的权重掩码平均并归一化到单位均值，避免因实例数量差异导致损失尺度偏移：

$$M ^ { * } = \frac { 1 } { N } \sum _ { n = 1 } ^ { N } M _ { n } ^ { * }, \quad M ^ { * } = \frac { M ^ { * } } { \mathbb { E } [ M ^ { * } ] }$$

最终，将动态掩码 $\pmb{M}^w$ 和 $\pmb{M}^l$ 集成到 DPO 损失中，对胜/败图像的噪声预测误差进行空间加权，抑制冲突实例区域的学习信号：

$$\mathcal { L } ( \theta ) = - \mathbb { E } \log \sigma \left( - \beta T \omega \big ( \lambda _ { t } \big ) \big ( \big ( \| \epsilon ^ { w } - \epsilon _ { \theta } ( \pmb { x } _ { t } ^ { w } , t ) \| _ { 2 } ^ { 2 } - \| \epsilon ^ { w } - \epsilon _ { \mathrm { r e f } } ( \pmb { x } _ { t } ^ { w } , t ) \| _ { 2 } ^ { 2 } \big ) \odot \pmb { M } ^ { w } - \left( \| \epsilon ^ { l } - \epsilon _ { \theta } ( \pmb { x } _ { t } ^ { l } , t ) \| _ { 2 } ^ { 2 } - \| \epsilon ^ { l } - \epsilon _ { \mathrm { r e f } } ( \pmb { x } _ { t } ^ { l } , t ) \| _ { 2 } ^ { 2 } \right) \odot \pmb { M } ^ { l } \big ) \right)$$

消融实验（Table 3）强有力地验证了这一设计的有效性：随着 $w_{\text{neg}}$ 从 1.0 降至 0.0（即逐步减弱冲突实例区域的学习信号），Aesthetic Score、PickScore 和 HPS 均单调提升，在 $w_{\text{neg}}=0$ 时取得最佳结果。这表明完全忽略冲突实例区域的学习信号反而能获得最优对齐效果，从实证角度证明了实例级信用分配的必要性。

### 创新带来的效率增益

实例级信用分配不仅提升了生成质量，还带来了显著的训练效率提升。由于动态重加权掩码使模型专注于学习关键实例区域、避免在歧义信号上浪费优化步数，IAPO 的训练速度比 InPO 快 **3.27 倍**，比 Diffusion-DPO 快 **11.64 倍**，比 KTO 快 **60.0 倍**（基于单块 H800 GPU 的 GPU 小时数对比，见 Table 2）。这种“质量-效率双赢”的特性源于信用分配精度的根本性提升，而非简单的工程优化。

IAPO（Instance-Aware Preference Optimization）的整体设计围绕一个核心洞察展开：**图像级偏好监督在空间维度上奖励稀疏，无法区分图像中不同实例的质量差异**。当获胜图像整体被偏好但其内部某个实例异常（例如鹰多了一只爪子）时，全局偏好会错误地奖励该劣质实例而惩罚失败图像中对应的高质量实例，导致优化轨迹扭曲。为解决这一问题，IAPO将扩散模型对齐从图像级推进到实例级，构建了一个**两阶段框架**（见 Figure 3）：

![[assets/figures/papers/paper_list_l2706_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_Towards_Fine_Grain/figures/003_Figure_3.jpg]]
*Figure 3: Overview of IAPO. We first construct a high-quality instance-level preference dataset based on Pick-a-Pic v2 [13] by utilizing VLMs to detect corresponding instances across image pairs and reassign their preference labels. Leveraging this dataset, we design instance alignment loss to amplify learning signals from critical instances while suppressing the influence of distracting ones*

1. **实例级偏好数据集自动标注管线**：基于 Pick-a-Pic v2 中的图像对，利用视觉语言模型（VLM）和开放集检测模型自动识别匹配实例、定位边界框并重新标注实例级偏好标签，最终生成包含 959,040 个图像对、1,205,593 个实例偏好对的大规模数据集。
2. **实例感知偏好优化训练**：利用上述数据集，通过动态重加权掩码在空间上调制 DPO 损失，对与全局偏好冲突的实例区域施加差异化权重，实现细粒度的信用分配。

### 数据流与模块关系

整个 pipeline 的数据流如下：

**输入** → Pick-a-Pic v2 中的图像对 $(x_0^w, x_0^l, c)$，其中 $x_0^w$ 为获胜图像，$x_0^l$ 为失败图像，$c$ 为文本提示。

**阶段一：实例级偏好标注**

自动标注管线由三个角色依次协作完成：

- **Planner（规划器）**：利用 VLM（如 Qwen2.5-VL）分析图像对，识别两幅图像中共同出现的语义实例（如“鹰”“树枝”“月亮”），输出实例列表。这一步解决了“哪些实例需要对比”的问题。
- **Detector（检测器）**：基于 Planner 输出的实例名称，调用开放集检测模型（如 Grounding DINO）在获胜和失败图像中分别定位每个实例的边界框 $(b_n^w, b_n^l)$。这一步提供了空间定位信息。
- **Judge（评判器）**：将检测到的实例区域裁剪后，再次利用 VLM 对每对匹配实例进行细粒度质量比较，输出实例级偏好标签 $\rho_n$：$\rho_n = 0$ 表示获胜图像的该实例确实优于失败图像（与全局偏好一致），$\rho_n = 1$ 表示失败图像的该实例反而更优（与全局偏好冲突）。

最终构建的数据集格式为：

$$\mathcal{D} = \{ (x_0^w, x_0^l, c, \{ (b_n^w, b_n^l, \rho_n) \}_{n=1}^N ) \}$$

其中 $N$ 为该图像对中匹配实例的数量。统计分析显示，约 **46.3%** 的实例对存在全局偏好与实例级偏好的冲突（558,352 / 1,205,593），这从数据层面验证了图像级监督的严重歧义性。

**阶段二：实例感知偏好优化**

将标注好的数据集 $\mathcal{D}$ 送入训练流程，核心模块包括：

- **DDIM 逆变模块**：对获胜和失败图像分别执行少步（<10 步）DDIM 逆变，获得近似的中间噪声状态 $x_t^w$、$x_t^l$ 及其对应的噪声 $\epsilon^w$、$\epsilon^l$。这一步避免了全步计算，是训练效率提升的关键（相比 Diffusion-DPO 快 11.64 倍）。

- **动态重加权掩码生成**：根据实例级偏好标签 $\rho_n$ 和边界框 $b_n^*$，为每个实例生成权重掩码 $M_n^*$：

$$M_n^*(i, j) = \begin{cases} w_{\text{neg}}, & \text{if } (i, j) \in b_n^* \text{ and } \rho_n = 1 \\ 1, & \text{otherwise} \end{cases}$$

其中 $w_{\text{neg}} \leq 1$ 是控制冲突区域学习信号强度的超参数。当实例偏好与全局偏好冲突（$\rho_n = 1$）时，该实例边界框内的像素被赋予降低的权重 $w_{\text{neg}}$，从而抑制劣质实例对优化目标的干扰。所有实例掩码平均后归一化到单位均值，避免因不同图像中实例数量差异导致的损失尺度偏移：

$$M^* = \frac{1}{N} \sum_{n=1}^N M_n^*, \quad M^* = \frac{M^*}{\mathbb{E}[M^*]}$$

- **实例感知 DPO 损失**：将动态掩码 $M^w$、$M^l$ 与标准 Diffusion-DPO 的噪声预测误差进行逐元素乘法，实现空间维度的信用分配：

$$\mathcal{L}(\theta) = -\mathbb{E} \log \sigma \left( -\beta T \omega(\lambda_t) \left( \left( \|\epsilon^w - \epsilon_\theta(x_t^w, t)\|_2^2 - \|\epsilon^w - \epsilon_{\text{ref}}(x_t^w, t)\|_2^2 \right) \odot M^w - \left( \|\epsilon^l - \epsilon_\theta(x_t^l, t)\|_2^2 - \|\epsilon^l - \epsilon_{\text{ref}}(x_t^l, t)\|_2^2 \right) \odot M^l \right) \right)$$

**输出** → 优化后的扩散模型参数 $\theta$，该模型在推理时无需任何额外开销，即可生成实例质量更优、与文本提示更精确对齐的图像。

### 关键设计决策

整个框架的设计决策围绕一个因果旋钮展开：**实例级信用分配**。与 InPO（Lu et al., CVPR 2025）和 Diffusion-DPO（Wallace et al., CVPR 2023）等基线方法对整幅图像均匀施加奖励/惩罚不同，IAPO 通过以下机制实现了精确的空间信用分配：

- **冲突感知**：自动识别并量化全局偏好与实例偏好的不一致性（46.3% 冲突率）。
- **差异化加权**：对冲突实例区域施加 $w_{\text{neg}}$ 权重以抑制其学习信号，而非冲突区域保持全权重。
- **归一化保障**：通过单位均值归一化确保不同图像对之间的损失尺度一致。

消融实验（Table 3）证实，随着 $w_{\text{neg}}$ 从 1.0 降至 0.0（即逐渐减弱冲突实例区域的学习信号），Aesthetic、PickScore 和 HPS 均单调提升，$w_{\text{neg}} = 0$ 时取得最佳结果，验证了动态重加权策略的有效性。

![[assets/figures/papers/paper_list_l2706_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_Towards_Fine_Grain/figures/001_Figure_1.jpg]]
*Figure 1: Instance-Level Credit Assignment. While existing methods uniformly propagate reward signals across all pixels, our work enables fine-grained, instance-specific modulation of the learning signal, achieving fine-grained credit assignment*

IAPO 的核心创新在于将扩散模型的对齐从图像级推进到实例级，通过两个紧密耦合的模块实现：**实例级偏好数据集的自动构建**和**实例感知的 DPO 损失函数**。以下分别阐述其关键设计与公式。

---

### 实例级偏好数据集构建管线

现有扩散模型对齐方法（如 **Diffusion-DPO** (Wallace et al., CVPR 2023)、**InPO** (Lu et al., CVPR 2025)）依赖图像级偏好对 $(x_0^w, x_0^l, c)$，其中 $x_0^w$ 和 $x_0^l$ 分别表示获胜和失败的生成图像，$c$ 为文本提示。这种监督信号在空间维度上均匀施加奖励/惩罚，无法区分图像中不同实例的质量差异。

IAPO 通过一个三阶段自动标注管线，将 Pick-a-Pic v2 数据集中的图像级偏好对扩展为实例级偏好数据集：

$$\mathcal{D} = \{ (x_0^w, x_0^l, c, \{ (b_n^w, b_n^l, \rho_n) \}_{n=1}^N ) \}$$

其中 $b_n^w$ 和 $b_n^l$ 分别表示第 $n$ 个共同实例在胜/败图像中的边界框，$\rho_n \in \{0, 1\}$ 为实例级偏好标签（$\rho_n = 1$ 表示该实例偏好与图像级偏好冲突，即获胜图像中的该实例质量反而不如失败图像中的对应实例）。

管线包含三个角色：
- **Planner**：利用 VLM 识别图像对中的共同实例。
- **Detector**：基于开集检测模型（如 Grounding DINO）定位每个实例的边界框。
- **Judge**：利用 VLM 对比裁剪后的实例块，为每对实例标注细粒度偏好标签。

最终数据集包含 959,040 个图像对，共 1,205,593 个实例偏好对。其中约 **46.3%**（558,352 对）存在全局偏好与实例级偏好的冲突，揭示了图像级监督的严重歧义。

---

### 动态重加权掩码生成

为在训练中对不同实例区域施加差异化损失权重，IAPO 设计了动态重加权掩码。对于第 $n$ 个实例，其权重掩码定义为：

$$M_n^*(i, j) = \begin{cases} w_{\text{neg}} & \text{if } (i, j) \in b_n^* \text{ and } \rho_n = 1 \\ 1 & \text{otherwise} \end{cases}$$

其中 $w_{\text{neg}} \in [0, 1]$ 是控制冲突实例区域学习信号强度的超参数。当实例偏好与全局偏好冲突（$\rho_n = 1$）时，该实例边界框内的像素权重被降低为 $w_{\text{neg}}$，从而抑制劣质实例获得错误奖励。

所有实例的权重掩码通过平均整合为统一的监督信号：

$$M^* = \frac{1}{N} \sum_{n=1}^{N} M_n^*$$

为避免不同图像中实例数量差异导致损失尺度偏移，整合后的掩码被显式归一化到单位均值：

$$M^* = \frac{M^*}{\mathbb{E}[M^*]}$$

---

### DDIM 逆变近似

为提高训练效率，IAPO 采用少步 DDIM 逆变来近似扩散过程中的中间状态，避免全步计算：

$$x_t^* = \sqrt{\frac{\alpha_t}{\alpha_{t-1}}} x_{t-1}^* + \left( \sqrt{\frac{1 - \alpha_t}{\alpha_t}} - \sqrt{\frac{1 - \alpha_{t-1}}{\alpha_{t-1}}} \right) \epsilon_\theta^{t-1}(x_{t-1}^*)$$

该方法仅需少于 10 步即可获得精确的近似，显著降低了训练开销。

---

### 实例感知 DPO 损失

最终的实例感知 DPO 损失将动态重加权掩码与 DDIM 逆变的降噪分数结合，实现空间细粒度的信用分配：

$$\mathcal{L}(\theta) = -\mathbb{E}_{(x_0^w, x_0^l) \sim \mathcal{D}, t \sim \mathcal{U}(0, T), x_t^w \sim q(x_t^w | x_0^w), x_t^l \sim q(x_t^l | x_0^l)} \log \sigma \left( -\beta T \omega(\lambda_t) \left( \left( \| \epsilon^w - \epsilon_\theta(x_t^w, t) \|_2^2 - \| \epsilon^w - \epsilon_{\text{ref}}(x_t^w, t) \|_2^2 \right) \odot M^w - \left( \| \epsilon^l - \epsilon_\theta(x_t^l, t) \|_2^2 - \| \epsilon^l - \epsilon_{\text{ref}}(x_t^l, t) \|_2^2 \right) \odot M^l \right) \right)$$

其中各变量含义：
- $\epsilon_\theta$：当前优化的去噪网络，$\epsilon_{\text{ref}}$：参考模型（冻结的预训练模型）。
- $\epsilon^w$、$\epsilon^l$：获胜/失败图像对应的真实噪声。
- $M^w$、$M^l$：获胜/失败图像对应的动态重加权掩码。
- $\beta$：控制偏好优化强度的温度参数。
- $\omega(\lambda_t)$：信噪比相关的加权函数。
- $\sigma$：sigmoid 函数，将隐式奖励差异映射为偏好概率。

该损失的核心机制是：对于与全局偏好冲突的实例区域（$w_{\text{neg}} < 1$），其噪声预测误差对总损失的贡献被抑制，从而避免模型错误地奖励劣质实例或惩罚优质实例。消融实验证实，随着 $w_{\text{neg}}$ 从 1.0 降至 0.0，Aesthetic Score、PickScore 和 HPS 均单调提升，$w_{\text{neg}} = 0$ 时取得最佳结果，验证了实例级偏好数据和动态重加权损失的有效性。

## 实验与关键发现

### 核心量化结果

IAPO 在三个主流基准（Parti-Prompts、HPD v2、Pick-a-Pic v2 测试集）上对 SD1.5 和 SDXL 两个基座模型进行了全面评估，评估指标覆盖 Aesthetic Score、PickScore、HPS 和 CLIP Score 的均值与中位数。**Table 1** 汇总了所有方法在多个评估器下的得分，IAPO 在绝大多数指标上取得最优或次优结果。

![[assets/figures/papers/paper_list_l2706_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_Towards_Fine_Grain/figures/005_Table_1.jpg]]
*Table 1: We conduct a comprehensive evaluation of IAPO against baseline methods using prompts from Parti-Prompts, HPDv2, and Picka-Pic v2 test set. Performance is reported using both mean and median scores across multiple evaluators, with the highest score in each metric bolded and the second highest underlined*

以 HPD v2 基准上 SD1.5 的结果为例：相比原始 SD1.5，IAPO 微调后 Aesthetic Score 提升 **0.4923**（从 5.2347 到 5.7270），PickScore 提升 **1.1803**（从 21.40 到 22.5803），HPS 提升 **1.7575**（从 27.40 到 29.1575）。在 SDXL 基座上，IAPO 同样全面超越 **InPO**（Lu et al., CVPR 2025），Parti-Prompts 上 Aesthetic Score 均值达到 **5.9503**。

### 训练效率对比

**Table 2** 报告了各方法在 Pick-a-Pic v2 数据集上达到可比性能所需的单卡 H800 GPU 小时数。IAPO 仅需 **17.6 小时**，而 InPO 需 57.5 小时，**Diffusion-DPO**（Wallace et al., CVPR 2023）需约 205 小时，**KTO**（Li et al., NeurIPS 2024）需约 1056 小时。IAPO 的训练速度分别是 InPO 的 **3.27 倍**、Diffusion-DPO 的 **11.64 倍**、KTO 的 **60.0 倍**。这一效率优势来源于两方面：一是少步（<10 步）DDIM 逆变近似扩散中间态，避免了全步计算；二是实例感知损失通过动态重加权掩码抑制了冲突实例区域的无效梯度，使优化轨迹更直接。

### 消融实验：冲突实例权重 w_neg

**Table 3** 展示了超参数 w_neg 的消融结果。w_neg 控制与全局偏好冲突的实例区域在损失中的权重——w_neg = 1.0 等价于不做实例级区分，w_neg = 0.0 则完全忽略冲突区域。实验表明，随着 w_neg 从 1.0 降至 0.0，Aesthetic、PickScore 和 HPS 三个指标**单调提升**，w_neg = 0 时取得最佳结果。这一趋势直接验证了两个核心主张：

1. **实例级偏好数据具有真实信息量**：约 46.3% 的实例对存在全局偏好与实例级偏好冲突（558,352 对 / 1,205,593 对），若不加区分地传播全局奖励信号，会错误地奖励劣质实例；
2. **动态重加权机制有效实现了细粒度信用分配**：降低冲突区域的权重等价于将优化信号集中于真正优质的实例区域，从而提升整体生成质量。

### 定性分析与失败模式

**Figure 4** 提供了 IAPO 与 InPO 在 SD1.5 和 SDXL 上的视觉对比。IAPO 生成的实例在细节忠实度和与文本的对齐度上均有明显改善——例如“mystical owl”的羽毛纹理、“cat like eyes”的面部结构等关键实例区域更加精细且符合描述。**Figure 2** 进一步展示了 IAPO 优化前后 SDXL 在相同噪声条件下的输出差异，优化后图像的实例完整性和构图质量显著提升。

**已知局限与潜在失败模式：**

- **自动标注噪声**：实例偏好标签由 VLM（Qwen2.5-VL）自动生成，检测边界框由 Grounding DINO 提供。论文未对检测置信度阈值或 VLM 提示鲁棒性进行消融，因此当检测模型漏检或误检实例时，重加权掩码可能错误地抑制或放大某些区域的学习信号。该点需在实际部署中结合具体检测模型性能进行验证。
- **权重策略单一**：当前仅通过标量 w_neg 统一调节所有冲突实例的权重，未考虑实例面积、空间位置或冲突程度等因素。对于大面积冲突实例与微小冲突实例，等权重处理可能导致优化偏差，但论文未探索更复杂的空间加权函数（如高斯衰减）。
- **泛化性未充分验证**：实验限于 SD1.5 和 SDXL 两个 UNet 架构的文本到图像模型，方法在 DiT 等新型架构或多模态生成任务上的表现尚不明确。

### 图表结论要点

- **Figure 5**：在 Pick-a-Pic v2 上以图像质量（PickScore）为纵轴、训练 GPU 小时数为横轴的散点图显示，IAPO 位于左上角区域，即高质量-低训练成本的帕累托前沿，显著优于所有基线方法。
- **Table 1**：IAPO 在三个基准上对 SD1.5 和 SDXL 的 Aesthetic、PickScore、HPS 均值均取得最优，CLIP Score 与基线持平或略优，表明实例级对齐在提升美学质量和人类偏好对齐度的同时未牺牲图文一致性。
- **Table 3**：w_neg 消融曲线单调递增，提供了实例级信用分配有效性的最直接因果证据。

![[assets/figures/papers/paper_list_l2706_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_Towards_Fine_Grain/figures/007_Table_3.jpg]]
*Table 3: We perform an ablation study on the hyperparameter*

![[assets/figures/papers/paper_list_l2706_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_Towards_Fine_Grain/figures/006_Figure_5.jpg]]
*Figure 5: A comparative evaluation of image quality and training efficiency between IAPO and baselines of SD1.5 on Pick-a-Pic v2*

![[assets/figures/papers/paper_list_l2706_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_Towards_Fine_Grain/figures/008_Table_2.jpg]]
*Table 2: We compare the training GPU hours (on H800) of IAPO against the baselines with the highest score in each metric bolded*

## 定位与知识库关联

### 核心问题定位：从图像级到实例级的信用分配

现有扩散模型对齐方法（如 **Diffusion-DPO** (Wallace et al., CVPR 2023)、**InPO** (Lu et al., CVPR 2025)、**KTO** (Li et al., NeurIPS 2024)）均采用图像级偏好监督：对整幅图像赋予单一的胜/负标签，并将奖励或惩罚信号均匀传播至所有像素。这种粗粒度信用分配在空间维度上奖励稀疏，无法区分图像中不同实例的质量差异。IAPO 通过构建首个大规模实例级偏好数据集，揭示了这一瓶颈的严重性：**约 46.3% 的实例对存在全局偏好与实例级偏好冲突**（558,352 / 1,205,593），即获胜图像中某实例异常却被全局偏好奖励，而失败图像中的优质实例却被惩罚。这种歧义导致优化轨迹扭曲，错误地奖励劣质实例而惩罚优质实例，训练效率低下。

### 方法沿革与 IAPO 的定位

IAPO 的方法论定位是将扩散模型对齐从图像级推进到实例级，其关键创新在于两个相互耦合的模块：

**1. 实例级偏好数据集的自动标注管线。** 与依赖人工标注或仅使用图像级偏好标签的现有工作不同，IAPO 设计了一套基于 VLM 和检测模型的三阶段自动标注流程——Planner（识别共同实例）、Detector（定位边界框）、Judge（对比裁剪后的实例块）——在 Pick-a-Pic v2 数据集上自动为 959,040 个图像对生成了 1,205,593 个实例偏好对。这一管线使得大规模细粒度监督成为可能，无需昂贵的人工标注。

**2. 实例感知 DPO 损失与动态重加权掩码。** 在标准 DPO 损失的基础上，IAPO 引入空间调制的权重掩码 $M^w$ 和 $M^l$：

$$M _ { n } ^ { * } ( i , j ) = \left\{ { \begin{array} { l l } { w _ { \mathrm { n e g } } } & { { \mathrm { i f } } \ ( i , j ) \in b _ { n } ^ { * } \ { \mathrm { a n d } } \rho _ { n } = 1 } \\ { 1 } & { { \mathrm { o t h e r w i s e } } } \end{array} } \right.$$

该掩码对与全局偏好冲突的实例区域施加权重 $w_{\text{neg}} \leq 1$，抑制其学习信号；所有实例掩码平均后归一化到单位均值（$M^{*} = \frac{M^{*}}{\mathbb{E}[M^{*}]}$），避免大小实例的权重偏差。最终的实例感知 DPO 损失通过空间加权实现精确的信用分配：

$$\mathcal { L } ( \theta ) = - \mathbb { E } \log \sigma \left( - \beta T \omega \big ( \lambda _ { t } \big ) \big ( \big ( \| \epsilon ^ { w } - \epsilon _ { \theta } ( \pmb { x } _ { t } ^ { w } , t ) \| _ { 2 } ^ { 2 } - \| \epsilon ^ { w } - \epsilon _ { \mathrm { r e f } } ( \pmb { x } _ { t } ^ { w } , t ) \| _ { 2 } ^ { 2 } \big ) \odot \pmb { M } ^ { w } - \left( \| \epsilon ^ { l } - \epsilon _ { \theta } ( \pmb { x } _ { t } ^ { l } , t ) \| _ { 2 } ^ { 2 } - \| \epsilon ^ { l } - \epsilon _ { \mathrm { r e f } } ( \pmb { x } _ { t } ^ { l } , t ) \| _ { 2 } ^ { 2 } \right) \odot \pmb { M } ^ { l } ) \right)$$

### 适用边界与局限

**1. 自动标注管线的质量依赖。** 实例级偏好数据集的构建依赖 VLM（如 Qwen2.5-VL）和开集检测模型（Grounding DINO）的性能，可能引入实例识别错误或偏好标签噪声。论文未对检测置信度阈值、VLM 提示鲁棒性进行深入消融，标签准确度未经过严格的人工验证。这在实际部署中可能构成风险：若 VLM 系统性误判实例偏好（例如对特定类别存在偏见），则数据集中的冲突标注可能反而引入新的噪声。

**2. 模型架构与任务的泛化性未验证。** 实验主要基于 SD1.5 和 SDXL 两个 UNet 架构的文本到图像扩散模型，尚未验证方法在 DiT 等新型生成架构或多模态生成任务上的有效性。实例级信用分配的核心思想——空间重加权——在原理上可迁移，但其具体实现（DDIM 逆变、边界框级掩码）可能需要针对不同架构调整。

**3. 重加权策略的单一性。** 动态重加权仅通过单一超参数 $w_{\text{neg}}$ 调节，未探索更复杂的空间加权函数（如高斯衰减、基于实例面积的权重、软边界过渡）。消融实验表明 $w_{\text{neg}}=0$ 时性能最优，这暗示当前策略可能过于激进——完全忽略冲突实例区域的学习信号，而非对其进行精细调制。

**4. 偏好标签的粒度上限。** 当前实例偏好标签为二值（$\rho_n \in \{0, 1\}$），且实例定位为边界框级而非像素级掩码。结合更强大的开集分割模型（如 SAM）将边界框升级为像素级掩码，以及引入连续偏好强度标注，可能进一步提升细粒度对齐精度。

### 开放问题

1. **时空联合的细粒度优化。** 当前 IAPO 仅处理空间维度的信用分配，而扩散模型的对齐还涉及时间步维度的信用分配（不同去噪步对最终质量的影响不同）。将实例感知掩码与时步感知加权统一为时空联合的优化框架，是一个自然且有价值的扩展方向。

2. **跨模态与跨任务的扩展。** 实例级信用分配的核心思想——识别冲突区域并差异化调制学习信号——能否扩展到视频生成（时序维度上的实例跟踪与偏好标注）或三维生成（多视角一致性下的实例级评估）？这需要解决标注管线的可扩展性问题。

3. **自动标注与人工标注的协同。** 当前完全依赖 VLM 自动标注，未来可引入主动学习或人在回路（human-in-the-loop）机制：优先将 VLM 置信度低的实例对提交人工审核，以最小的人工成本提升标签质量并减少系统性偏差。

4. **冲突实例的因果归因。** 46.3% 的冲突率揭示了图像级偏好的严重歧义，但论文未深入分析冲突的成因分布——是由于 VLM 的标注错误、图像级偏好的内在噪声，还是由于某些实例类别（如人手、文字）本身难以生成？理解冲突的因果结构有助于设计更有针对性的重加权策略。

## 原文 PDF

![[paperPDFs/CVPR_2026/Towards_Fine_Grained_Attribution_Instance_Aware_Preference_Optimization_for_Aligning_Diffusion_Models.pdf]]
