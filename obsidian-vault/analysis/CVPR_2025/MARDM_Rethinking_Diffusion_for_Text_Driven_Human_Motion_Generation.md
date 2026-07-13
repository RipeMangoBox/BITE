---
title: "MARDM: Rethinking Diffusion for Text-Driven Human Motion Generation"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/MARDM_Rethinking_Diffusion_for_Text_Driven_Human_Motion_Generation.pdf
project_link: https://neu-vi.github.io/MARDM/
code_link: null
aliases:
- MARDM
tags:
- CVPR_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "通过移除冗余维度、仅保留必要条件，结合确定性 AutoEncoder 投影和掩码自回归扩散生成，可以根本解决上述瓶颈。"
primary_logic: "消除运动表示中的冗余特征并采用掩码自回归扩散架构，使扩散模型能够克服传统限制，达到与 VQ 方法相媲美甚至更优的性能。"
claims:
- "VQ 方法受益于冗余特征，冗余维度充当数据级别正则化，提升重建和生成质量。"
- "扩散模型预测噪声时因标准差比率导致错误放大，预测原始 x0 效果更好。"
- "评估器对冗余维度过于敏感，导致不公平评价；去除冗余后 VQ 与扩散方法性能差距缩小。"
- "移除冗余表示并引入掩码自回归扩散后，FID 显著降低，R-Precision 大幅提升。"
---

# MARDM: Rethinking Diffusion for Text-Driven Human Motion Generation

> [!tip] 核心洞察
> 消除运动表示中的冗余特征并采用掩码自回归扩散架构，使扩散模型能够克服传统限制，达到与 VQ 方法相媲美甚至更优的性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | MARDM: 重新思考扩散模型用于文本驱动的人体动作生成 |
| 英文题名 | MARDM: Rethinking Diffusion for Text-Driven Human Motion Generation |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2311.17009) · [Project](https://neu-vi.github.io/MARDM/) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | MARDM |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，FID 为 0.114 (Ours-SiT)，对比 0.335 (T2M-GPT)，变化 -0.221。
> - HumanML3D 上，R-Precision Top-1 为 0.500 (Ours-SiT)，对比 0.470 (T2M-GPT)，变化 +0.030。
> - HumanML3D 上，R-Precision Top-3 为 0.795 (Ours-SiT)，对比 0.758 (T2M-GPT)，变化 +0.037。

## 概要

文本驱动的人体运动生成领域长期存在一个看似矛盾的现象：基于向量量化（VQ）的方法（如 **T2M-GPT**、**MoMask**）在生成质量上持续领先基于扩散的方法（如 **MDM**、**MotionDiffuse**、**MLD**），尽管扩散模型在图像、视频等其他生成任务中已展现出强大的能力。本文通过系统性的诊断分析，揭示了这一现象背后的三个根本瓶颈：

1. **运动数据表示中的冗余维度带来了维度分布失配**：当前运动表示包含关节旋转、局部速度、足部接触等冗余特征组，这些特征组的标准差差异巨大，导致扩散模型需要拟合一个远离标准正态分布的复杂分布，增加了训练难度。而 VQ 方法反而受益于这种冗余——冗余维度充当了数据级别的正则化，使码本使用更均衡，从而提升了重建和生成质量（**Table 1**）。

2. **噪声预测目标导致误差放大**：扩散模型在预测噪声 ε 时，由于不同特征组的标准差比率，预测误差会被放大；而预测原始信号 x₀ 则可以避免这一问题（**Table 2**：MDM 预测 x₀ 的 FID 为 0.518，而预测 ε 的 FID 高达 31.265）。

3. **现有评估器对冗余维度过度敏感**：传统评估器使用全部特征进行评价，对扩散方法在冗余维度上的微小波动施加了不成比例的惩罚，导致不公平的比较（**Table 3**：将冗余维度替换为噪声时 FID 飙升至 38.167，而仅替换必要维度时 FID 为 15.164）。

基于上述诊断，本文提出 **MARDM**（Masked Autoregressive Diffusion Model），核心思路是：**移除运动表示中的冗余维度，仅保留必要条件（根速度、根线性速度、根高度、局部关节位置），通过确定性 1D ResNet AutoEncoder 将必要特征投影到紧凑的潜空间，并采用掩码自回归扩散架构进行生成。** 同时，本文提出仅使用必要特征训练的新评估框架，确保公平比较。

在 HumanML3D 和 KIT-ML 数据集（统计见[[../../references/T2M_Common_Datasets|T2M Common Datasets]]）上的实验表明，MARDM 取得了最优性能：在新评估器下，FID 降至 0.114，R-Precision Top-1 达到 0.500，Top-3 达到 0.795，显著优于 T2M-GPT（FID 0.335，Top-1 0.470，Top-3 0.758），并展现出良好的模型可扩展性（**Figure 1**）。消融实验证实，移除表示重构和去除掩码自回归建模分别导致 FID 增加 2.080 和 0.435，验证了各模块的必要性（**Table 6**）。



### 文本驱动人体动作生成的范式分裂

文本驱动的人体动作生成旨在根据自然语言描述合成逼真的 3D 人体运动序列，在虚拟人、游戏、影视等领域具有广泛应用。当前该领域的主流方法可归为两大范式：**基于矢量量化（VQ）的自回归/掩码生成方法**，如 **T2M-GPT**、**MoMask**、**MMM**；以及**基于扩散模型的生成方法**，如 **MDM**、**MotionDiffuse**、**MLD**、**ReMoDiffuse**。

然而，这两种范式之间存在显著的性能鸿沟。在 HumanML3D 和 KIT-ML 等标准基准上，VQ 方法长期占据 FID 和 R-Precision 等关键指标的领先地位，而扩散方法尽管在图像、视频等连续域生成中表现卓越，在运动生成任务上却始终难以匹敌。这一现象构成了本文的核心研究动机：**扩散模型在运动生成中是否被不公平地低估？其性能瓶颈的本质是什么？**

### 三个被忽视的系统性瓶颈

通过对运动数据表示、生成建模和评估体系的系统诊断，本文揭示了三个相互关联的瓶颈，它们共同构成了扩散方法在运动生成中的“玻璃天花板”。

#### 瓶颈一：运动数据表示中的冗余维度与分布失配

当前运动数据通常包含多组异构特征——关节旋转、局部速度、足部接触标签等。这些特征组并非同等重要：其中一部分是定义人体姿态的**必要条件**（如根速度、局部关节位置），其余则为**冗余维度**。冗余维度的存在带来了两个连锁问题。

**第一，维度间标准差分布严重不匹配。** 标准扩散模型的前向过程假设各维度服从相近的噪声尺度，但冗余维度与必要维度的标准差比率经特征偏差项 $\gamma$ 调整后，可表示为：

$$\phi^{\prime \mathbf{x}} = \gamma \times \frac{\sigma^{\mathbf{x}\prime}}{\sigma^{\mathbf{x}}}$$

其中 $\sigma^{\mathbf{x}\prime} = \frac{\sum_{i=0}^{D-1} \sigma_i^{\mathbf{x}}}{D}$ 为特征组内平均标准差。这种分布失配使得扩散模型难以用统一的噪声调度同时覆盖所有维度。

**第二，噪声预测目标导致误差放大。** 当扩散模型预测噪声 $\epsilon$ 而非原始数据 $\mathbf{x}_0$ 时，原始数据域的预测误差与噪声域误差之间存在如下缩放关系：

$$\delta_{\mathbf{x}_0} \times \phi_i^{\prime} = \left(\frac{\sqrt{1-\bar{\alpha}_t}}{\sqrt{\bar{\alpha}_t}}\right)^2 \delta_{\epsilon}$$

该公式表明，噪声预测误差 $\delta_{\epsilon}$ 经标准差比率 $\phi_i^{\prime}$ 的平方放大后，会转化为更大的 $\mathbf{x}_0$ 重建误差。实验证据有力地支持了这一分析：**Table 2** 显示，MDM 在预测 $\mathbf{x}_0$ 时 FID 为 0.518，而预测 $\epsilon$（Cosine 调度）时 FID 飙升至 31.265，R-Precision Top-1 从 0.440 骤降至 0.054。这直接证实了噪声预测模式下的误差放大效应。

#### 瓶颈二：冗余维度对 VQ 方法的“隐性补贴”

与扩散方法形成鲜明对比的是，VQ 方法反而从冗余维度中**受益**。本文将 VQ-VAE 的重建损失分解为：

$$L_r^{\mathrm{rec}} = \mathcal{L}(\mathbf{x}_e^{GT} - \mathbf{x}_e^{pred} + \mathbf{x}_{r-e}^{GT} - \mathbf{x}_{r-e}^{pred}) = L_e^{rec} + \mathcal{L}(\mathbf{x}_{r-e}^{GT} - \mathbf{x}_{r-e}^{pred})$$

该分解揭示：冗余维度的重建项 $\mathcal{L}(\mathbf{x}_{r-e}^{GT} - \mathbf{x}_{r-e}^{pred})$ 充当了**数据级别的正则化项**，帮助 VQ-VAE 学习更均衡的码本使用模式。**Table 1** 的消融实验证实了这一点：T2M-GPT 在含冗余特征时重建 FID 为 0.081，去除后升至 0.095；MoMask 同样从 0.029 升至 0.030。**Figure 2** 进一步显示，含冗余训练的 VQ-VAE 码本使用分布更加均衡，这得益于每个离散码对应的 Voronoi 胞腔：

$$V_k = \{z \in \mathbb{R}^d \mid \|z - e_k\|_2 \leq \|z - e_j\|_2\}, \forall j \neq k$$

使得生成误差在不同维度间更一致。换言之，冗余维度为 VQ 方法提供了“免费午餐”，而扩散方法不仅无法享受这一红利，反而受其拖累。

#### 瓶颈三：评估器对冗余维度的过度敏感

现有评估器（如 T2M 提出的运动特征提取器）在全部特征维度上进行训练和评估，而其对冗余维度的依赖程度远超预期。**Table 3** 的敏感性分析表明：当冗余维度被替换为噪声时，FID 飙升至 38.167；而仅替换必要维度时，FID 仅为 15.164。这说明评估器对冗余维度的微小波动极度敏感，会系统性地惩罚扩散方法在冗余维度上的自然预测误差，导致不公平评价。

这一偏差在 **Table 4** 中得到进一步验证：在传统全维度评估下，T2M-GPT（VQ 方法）的 FID 为 0.115，而 MDM（扩散方法）为 0.481，差距悬殊；但当评估器仅使用必要维度训练时，T2M-GPT 的 FID 变为 0.335，MDM 为 0.518，两者差距大幅缩小，且 MDM 在 R-Precision 上与 T2M-GPT 已十分接近。这表明**扩散方法的真实能力被冗余维度和有偏评估器共同掩盖**。

### 本文动机与核心思路

上述诊断指向一个清晰的结论：扩散模型在运动生成中的劣势并非方法本身的固有缺陷，而是**数据表示、噪声建模目标和评估体系**三个环节的系统性失配所致。这自然引出本文的核心思路：

1. **重构运动表示**：移除冗余维度，仅保留必要条件（根速度、根线性速度、根高度、局部关节位置），使数据分布更适合扩散建模；
2. **引入掩码自回归扩散**：将全序列一次性生成分解为逐块掩码潜变量的条件生成，简化优化目标并利用上下文信息；
3. **重建公平评估框架**：仅使用必要维度训练评估器，消除冗余维度带来的评价偏差。

通过这些设计，MARDM 旨在证明：**连续扩散模型在运动生成中可以达到甚至超越 VQ 方法的性能**，从而弥合两大范式之间的鸿沟。



## 核心方法与创新机理

### 创新动机：扩散模型在运动生成中的三重瓶颈

MARDM 的核心创新源于对当前文本驱动人体动作生成范式的系统性诊断。作者识别出制约扩散模型性能的三重瓶颈：

1. **运动数据表示的维度分布失配**：当前广泛使用的运动表示（如 HumanML3D 的 263 维特征）包含大量冗余维度（关节旋转、局部速度、足部接触等），这些维度的统计分布与标准正态分布存在显著偏差。扩散模型的前向过程假设数据服从高斯分布，这种失配导致去噪网络需要同时拟合异构分布，增加了优化难度。

2. **噪声预测的误差放大效应**：扩散模型在预测噪声 ε 时，由于不同特征组的标准差比率差异，微小的噪声预测误差会被放大。如公式 (5) 所示：
   $$\delta_{\mathbf{x}_0} \times \phi_i^{\prime} = \left(\frac{\sqrt{1-\bar{\alpha}_t}}{\sqrt{\bar{\alpha}_t}}\right)^2 \delta_{\epsilon}$$
   其中 $\phi_i^{\prime}$ 为调整后的标准差比率。这意味着预测 ε 时，误差会随标准差比率被二次放大，而预测原始 $\mathbf{x}_0$ 则不受此影响。

3. **评估器对冗余维度的过度敏感**：现有评估器（基于 T2M 框架）在全部特征维度上计算 FID，对冗余维度的微小波动过度敏感，导致扩散方法受到不公平惩罚。

### 关键洞察：冗余特征的双面性

作者揭示了一个关键发现：**冗余特征对 VQ 方法和扩散方法具有截然不同的影响**。

- **VQ 方法受益于冗余**：冗余维度充当数据级别的隐式正则化，使 VQ-VAE 的码本使用更均衡（Figure 2），从而提升重建和生成质量。Table 1 显示，**T2M-GPT** 带冗余特征时 FID 为 0.081，去除冗余后升至 0.095；**MoMask** 带冗余 FID 为 0.029，去除后为 0.030。

- **扩散方法受害于冗余**：冗余维度引入的分布失配和误差放大效应严重制约扩散模型的生成质量。Table 2 表明，**MDM** 预测 $\mathbf{x}_0$ 时 FID 为 0.518，而预测 ε（Cosine schedule）时 FID 飙升至 31.265。

这一洞察直接催生了 MARDM 的设计哲学：**消除冗余特征，让扩散模型在纯净的必要特征空间上发挥优势**。

### Changed Slots：相对 Baseline 的五个关键改造

MARDM 相对现有方法进行了五个核心改造（changed slots），每个改造都直接针对上述瓶颈：

| 改造维度 | Baseline 做法 | MARDM 做法 | 针对的瓶颈 |
|---------|-------------|-----------|-----------|
| **运动数据表示** | 包含冗余维度（263 维） | 仅保留必要条件：根速度、根线性速度、根高度、局部关节位置（#joints × 3 + 1 维） | 维度分布失配 |
| **隐空间映射** | VQ-VAE / RVQ-VAE 离散量化 | 确定性 1D ResNet AutoEncoder（AE）连续投影 | 离散量化损失 + 分布失配 |
| **扩散预测目标** | 预测 $\mathbf{x}_0$ 或 ε | 预测速度 $\mathbf{v}(\mathbf{x}, t)$（连续时间插值） | 误差放大效应 |
| **生成模式** | 一次性生成整个序列 | 掩码自回归扩散，逐块预测掩码潜变量 | 长序列优化困难 |
| **评估器** | 使用全部特征（含冗余维度） | 仅使用必要条件训练评估器 | 不公平评估 |

### 创新一：运动表示重构与确定性 AutoEncoder 投影

MARDM 首先对运动数据表示进行根本性重构。作者识别出运动特征中的**必要特征组**（根速度、根线性速度、根高度、局部关节位置）和**冗余特征组**（关节旋转、局部速度、足部接触等），仅保留前者。这一改造消除了维度分布失配的根源。

随后，必要特征通过**确定性 1D ResNet AutoEncoder** 投影到紧凑的连续潜空间。与 VQ-VAE 的离散量化不同，确定性 AE 避免了码本坍缩和 Voronoi 胞腔限制，使潜空间更细粒度、更适合扩散建模。AE 的训练损失为 L1 重建损失：
$$\mathcal{L}_{\mathrm{ae}} = \|\mathbf{X}^{0:N} - \mathbf{X}'^{0:N}\|_1$$

### 创新二：掩码自回归扩散架构

MARDM 的生成过程采用**掩码自回归扩散**范式，将全序列生成分解为条件概率链：
$$p(\mathbf{x}'^{1:n}|c) = p(\mathbf{m}|c) \prod_{j=1}^{k} p(\mathbf{m}|\mathbf{um})$$

具体架构由三个模块协同工作（Figure 3）：

1. **Motion AutoEncoder（1D ResNet）**：将必要运动特征编码到紧凑潜空间并解码回运动特征。

2. **Masked Autoregressive Transformer**：接收已生成的未掩码潜变量，为扩散分支提供上下文条件 $\mathbf{z}$。

3. **Diffusion MLPs**：在每个扩散时间步，基于条件 $\mathbf{z}$ 对掩码位置的潜变量进行去噪：
   $$\mathbf{x}_{t-1}^{\prime i} \sim p(\mathbf{x}_{t-1}^{\prime i} \mid \mathbf{x}_{t}^{\prime i}, t, z^{i})$$

这一架构将自回归的序列建模能力与扩散的高质量生成能力相结合，同时通过掩码策略简化了训练目标。

### 创新三：速度预测与连续时间扩散

MARDM 在潜空间中采用连续时间扩散框架，预测速度 $\mathbf{v}(\mathbf{x}, t)$ 而非噪声 ε 或 $\mathbf{x}_0$：
$$\mathbf{v}(\mathbf{x}, t) = \dot{\alpha}_t \mathbb{E}[\mathbf{x}_0 \mid \mathbf{x}_t = \mathbf{x}] + \dot{\sigma}_t \mathbb{E}[\epsilon \mid \mathbf{x}_t = \mathbf{x}]$$

速度预测结合了 $\mathbf{x}_0$ 预测和 ε 预测的优势，避免了噪声预测中的误差放大问题。消融实验（Table A2）显示，速度预测（FID 0.114）优于 $\mathbf{x}_0$ 预测（FID 0.135）。

### 创新四：公平评估框架

MARDM 提出仅使用必要特征训练评估器，消除冗余维度对评估结果的干扰。Table 4 显示，在必要维度评估下，**MDM** 与 **T2M-GPT** 的 R-Precision 差距显著缩小，验证了传统评估器的不公平性。

### 消融验证：创新组件的贡献

Table 6 的消融实验量化了各创新组件的贡献：

- **移除表示重构**（仍使用冗余表示和原始扩散）：FID 从 0.116 升至 2.196，Top-3 R-Precision 从 0.790 降至 0.703，降幅约 8.7%。
- **去除掩码自回归**（普通扩散）：FID 从 0.116 升至 0.551，Top-3 R-Precision 从 0.790 降至 0.732，降幅约 5.8%。

这表明表示重构和掩码自回归对性能提升均有显著贡献，且前者贡献更大。

### 模型可扩展性

MARDM 展现出良好的模型可扩展性。Table A5 显示，将模型从 S 扩展到 XL（增大 Transformer 和 MLP 规模），FID 从 0.278 稳定降至 0.116，验证了架构设计的可扩展性。



MARDM 的整体设计围绕一个核心洞察展开：**消除运动表示中的冗余特征，并引入掩码自回归扩散架构，使扩散模型能够克服传统限制，达到与 VQ 方法相媲美甚至更优的性能**。其 pipeline 由三个紧密协作的模块构成，如 Figure 3 所示。

![[assets/figures/papers/paper_list_l28_MARDM_Rethinking_Diffusion_for_Text_Driven_Human_Motion_Generation/figures/007_Figure_3.jpg]]
*Figure 3: Method Overview. (a) The reformed motion sequence is projected into a compact fine-grained latent space through a Motion AutoEncoder. (b) The motion latents $\mathbf { x } ^ { 0 : 3 }$ are processed through a Masked Autoregressive Transformer, where they are either randomly masked (in training) or appended (in inference) with a learnable mask vector (yellow-colored latents). The transformer provides a condition z for the masked positions to the Diffusion MLPs to produce clean latent $\mathbf { x } ^ { \mathrm { { 3 : 4 } } }$ from the noised input. (c) A visual illustration of motion masked autoregressive where masked latents (yellow-colored) can be reordered into a pseudo-position allowing p (...

### 1. 运动 AutoEncoder：从必要特征到紧凑潜空间

传统运动数据表示包含大量冗余维度（如关节旋转、局部速度、足部接触等），这些冗余维度导致扩散模型面临**维度分布失配**和**噪声预测误差放大**两个根本性问题。MARDM 首先对运动表示进行重构：**仅保留必要条件**，即前 `#joints × 3 + 1` 维（根速度、根线性速度、根高度、局部关节位置），从而移除冗余信息对扩散过程的干扰。

随后，这些必要特征通过一个**确定性 1D ResNet AutoEncoder (AE)** 被投影到一个紧凑且细粒度的连续潜空间中。与 VQ 方法使用的 VQ-VAE 或 RVQ-VAE 离散量化不同，该 AE 采用 L1 重建损失进行训练：

$$\mathcal{L}_{\mathrm{ae}} = \|\mathbf{X}^{0:N} - \mathbf{X}'^{0:N}\|_1$$

这种确定性映射避免了离散量化带来的信息损失，同时 1D ResNet 架构保证了逐帧平滑性。Table A1 的重建实验表明，该 AE 在重建精度上优于基线方法所使用的潜变量编码器。

### 2. 掩码自回归 Transformer：提供逐位置条件

经 AE 编码后得到的运动潜变量序列 $\mathbf{x}'^{1:n}$ 进入**掩码自回归 Transformer**。该模块的核心思想是将全序列生成分解为条件概率链：

$$p(\mathbf{x}'^{1:n}|c) = p(\mathbf{m}|c) \prod_{j=1}^{k} p(\mathbf{m}|\mathbf{um})$$

其中 $\mathbf{m}$ 表示被掩码的潜变量，$\mathbf{um}$ 表示已生成的未掩码潜变量。Transformer 接收已生成的运动潜变量作为上下文，为扩散分支中的每个掩码位置产生条件向量 $z^i$，指导后续的去噪过程。

这种设计与传统扩散方法“一次性生成整个序列”的模式形成鲜明对比：传统方法直接建模 $p(\mathbf{x}^{1:n}|c)$，优化难度大且难以捕捉序列内部的依赖关系；掩码自回归则将问题分解为多个条件生成子任务，显著简化了训练目标。

### 3. 扩散 MLP：基于条件去噪生成

在每个扩散时间步，**扩散 MLP** 接收 Transformer 提供的条件 $z^i$，对掩码位置的潜变量进行去噪：

$$\mathbf{x}_{t-1}^{\prime i} \sim p(\mathbf{x}_{t-1}^{\prime i} \mid \mathbf{x}_{t}^{\prime i}, t, z^{i})$$

扩散过程采用连续时间插值框架，训练目标为预测速度 $\mathbf{v}(\mathbf{x}, t)$ 或噪声 $\epsilon$，而非直接预测 $\mathbf{x}_0$。速度预测的定义为：

$$\mathbf{v}(\mathbf{x}, t) = \dot{\alpha}_t \mathbb{E}[\mathbf{x}_0 \mid \mathbf{x}_t = \mathbf{x}] + \dot{\sigma}_t \mathbb{E}[\epsilon \mid \mathbf{x}_t = \mathbf{x}]$$

这一选择基于论文在诊断阶段的发现：传统扩散方法预测噪声 $\epsilon$ 时，由于运动数据各维度标准差比率不同，误差会被放大（见公式 $\delta_{\mathbf{x}_0} \times \phi_i^{\prime} = \left(\frac{\sqrt{1-\bar{\alpha}_t}}{\sqrt{\bar{\alpha}_t}}\right)^2 \delta_{\epsilon}$），而预测 $\mathbf{x}_0$ 或速度则不受此影响。

### 4. 数据流与模块交互

整个 pipeline 的数据流可以概括为：

1. **输入**：文本条件 $c$ 和重构后的必要运动特征 $\mathbf{X}^{0:N}$。
2. **编码**：AE 编码器将 $\mathbf{X}^{0:N}$ 压缩为潜变量序列 $\mathbf{x}'^{1:n}$。
3. **自回归条件生成**：掩码自回归 Transformer 根据已生成的未掩码潜变量 $\mathbf{um}$ 产生条件 $z^i$。
4. **扩散去噪**：扩散 MLP 在每个时间步基于 $z^i$ 对掩码潜变量进行去噪，逐步恢复完整序列。
5. **解码**：AE 解码器将生成的潜变量还原为运动特征。
6. **评估**：新评估器仅基于必要维度计算指标，避免传统评估器对冗余维度的过度敏感导致的不公平比较（Table 3 显示冗余维度替换为噪声时 FID 高达 38.167，而必要维度替换仅为 15.164）。

### 5. 关键设计决策的证据支撑

消融实验（Table 6）强有力地验证了框架设计的必要性：
- **移除表示重构**（即仍使用冗余表示和原始扩散）：FID 从 0.116 恶化至 2.196，Top-3 R-Precision 从 0.790 下降至 0.703，证实了冗余维度是扩散模型性能瓶颈的根本原因。
- **去除掩码自回归**（改为普通扩散）：FID 从 0.116 上升至 0.551，Top-3 R-Precision 从 0.790 下降至 0.732，表明自回归分解对生成质量有显著贡献。

此外，模型规模实验（Table A5）显示增大 Transformer 和 MLP 规模可稳定提升性能（S→XL FID 从 0.278 降至 0.116），验证了框架的可扩展性。



### 3.1 运动表示重构与确定性自编码器

MARDM 的核心设计起点是对运动数据表示的根本性重构。传统方法使用的运动特征（如关节旋转、局部速度、足部接触等）包含大量冗余维度，这些冗余维度导致两个关键问题：其一，不同特征组的方差分布严重失配，使扩散模型难以学习统一的数据分布；其二，冗余维度在评估中占据过大权重，导致对扩散方法的系统性不公平。MARDM 的解决方案是仅保留**必要特征组**——即前 `#joints × 3 + 1` 个维度（根速度、根线性速度、根高度、局部关节位置），从根本上消除维度分布失配问题。

在此基础上，MARDM 引入一个**确定性 1D ResNet AutoEncoder (AE)**，将必要特征投影到紧凑且细粒度的潜空间中：

$$
\mathcal{L}_{\mathrm{ae}} = \|\mathbf{X}^{0:N} - \mathbf{X}'^{0:N}\|_1
$$

其中 $\mathbf{X}^{0:N}$ 为原始运动序列，$\mathbf{X}'^{0:N}$ 为重建序列，使用 L1 距离最小化重建误差。与 VQ-VAE 的离散量化不同，该 AE 采用确定性映射，避免了码本坍缩和 Voronoi 胞腔边界带来的量化误差，同时保留了潜空间的连续性，为后续扩散生成提供更平滑的优化目标。

### 3.2 连续时间扩散与速度预测

在重构后的潜空间中，MARDM 采用连续时间扩散框架。前向过程通过线性插值将潜变量与高斯噪声混合：

$$
\mathbf{x}_t = \alpha_t \mathbf{x}_0 + \sigma_t \boldsymbol{\epsilon} = (1-t)\mathbf{x}_0 + t\boldsymbol{\epsilon}
$$

其中 $t \in [0,1]$ 为连续时间步，$\alpha_t = 1-t$ 和 $\sigma_t = t$ 定义了从数据到噪声的线性路径。与传统 DDPM 预测噪声 $\epsilon$ 或原始数据 $\mathbf{x}_0$ 不同，MARDM 的核心创新在于预测**速度场** $\mathbf{v}(\mathbf{x}, t)$：

$$
\mathbf{v}(\mathbf{x}, t) = \dot{\alpha}_t \mathbb{E}[\mathbf{x}_0 \mid \mathbf{x}_t = \mathbf{x}] + \dot{\sigma}_t \mathbb{E}[\boldsymbol{\epsilon} \mid \mathbf{x}_t = \mathbf{x}]
$$

速度预测的关键优势在于它统一了 $\mathbf{x}_0$ 预测和 $\epsilon$ 预测两种范式：当 $\alpha_t$ 和 $\sigma_t$ 满足特定关系时，速度场等价于分数函数，避免了噪声预测中因标准差比率 $\phi_i'$ 导致的误差放大问题（见诊断部分公式 (5) 的分析）。论文中的消融实验（Table A2）证实，速度预测（FID 0.114）优于直接预测 $\mathbf{x}_0$（FID 0.135）。

### 3.3 掩码自回归扩散生成

传统扩散方法一次性生成整个运动序列 $p(\mathbf{x}^{1:n}|c)$，难以捕捉帧间的长程依赖。MARDM 将其分解为**掩码自回归**形式：

$$
p(\mathbf{x}'^{1:n}|c) = p(\mathbf{m}|c) \prod_{j=1}^{k} p(\mathbf{m}|\mathbf{um})
$$

其中 $\mathbf{m}$ 表示被掩码的潜变量组，$\mathbf{um}$ 表示已生成的未掩码潜变量。这一分解将全序列生成转化为逐块的条件生成问题，每个扩散步骤仅需预测当前掩码位置的潜变量。

具体实现包含两个协同模块：

- **掩码自回归 Transformer**：接收已生成的潜变量序列，为扩散分支提供上下文条件 $\mathbf{z}$。Transformer 的自注意力机制能够有效建模已生成帧之间的时序依赖，为当前掩码位置提供丰富的上下文信息。

- **扩散 MLPs**：在每个扩散时间步，基于 Transformer 提供的条件 $\mathbf{z}^i$ 对掩码位置的潜变量进行去噪：

$$
\mathbf{x}_{t-1}^{\prime i} \sim p(\mathbf{x}_{t-1}^{\prime i} \mid \mathbf{x}_{t}^{\prime i}, t, \mathbf{z}^i)
$$

这种设计将扩散模型的生成能力与自回归模型的序列建模能力有机结合：Transformer 负责全局时序结构规划，扩散 MLPs 负责局部细节填充。消融实验（Table 6）表明，去除自回归建模后 FID 从 0.116 升至 0.551，验证了掩码自回归策略对生成质量的关键作用。

### 3.4 评估框架重构

为消除评估偏差，MARDM 提出仅使用必要维度训练评估器（T2M 结构 + CLIP 评估器）。Table 4 显示，在必要维度评估下，扩散方法（MDM）与 VQ 方法（T2M-GPT）的 R-Precision 差距显著缩小，验证了传统评估器对冗余维度的过度依赖是扩散方法被低估的重要原因。



## 实验与关键发现

### 核心瓶颈的诊断验证

MARDM 的实验设计遵循“诊断—重构—验证”的逻辑链，首先通过一系列控制实验验证了三个核心瓶颈假设。

**冗余特征对 VQ 方法的正则化效应。** Table 1 给出了关键证据：T2M-GPT 在保留冗余特征时重建 FID 为 0.081，生成 FID 为 0.335；移除冗余后重建 FID 升至 0.095，生成 FID 升至 0.418。MoMask 同样呈现此趋势（重建 FID 0.029→0.030，生成 FID 0.116→0.200）。Figure 2 进一步揭示了机制：含冗余训练的 VQ-VAE 码本利用率更均衡，冗余维度充当了数据级正则化，通过公式 (3) 的损失分解 $L_r^{\mathrm{rec}} = L_e^{rec} + \mathcal{L}(\mathbf{x}_{r-e}^{GT} - \mathbf{x}_{r-e}^{pred})$ 体现为额外的正则项。

**扩散模型的噪声预测误差放大。** Table 2 的对比极具说服力：MDM 在 HumanML3D 上预测原始 $x_0$ 时 FID 为 0.518，而预测噪声 $\epsilon$ 时 FID 飙升至 31.265，R-Precision Top-1 从 0.440 骤降至 0.054。公式 (5) 给出了理论解释：$\delta_{\mathbf{x}_0} \times \phi_i^{\prime} = \left(\frac{\sqrt{1-\bar{\alpha}_t}}{\sqrt{\bar{\alpha}_t}}\right)^2 \delta_{\epsilon}$，即噪声预测误差被标准差比率放大，而 $x_0$ 预测不受此影响。

**评估器对冗余维度的过度敏感。** Table 3 显示，将冗余维度替换为噪声导致 FID 升至 38.167，而仅替换必要维度时 FID 为 15.164，表明评估器对冗余维度的微小波动惩罚过重。Table 4 进一步揭示：在全部维度评估下，T2M-GPT（FID 0.115）大幅优于 MDM（FID 0.481）；但切换至仅必要维度的评估器后，MDM 的 R-Precision 已接近 T2M-GPT，性能差距显著缩小。

### 主要定量结果

Table 5 报告了 HumanML3D 和 KIT-ML 数据集上的全面对比。在 HumanML3D 上，MARDM-SiT（速度预测变体）取得了 FID 0.114、R-Precision Top-1 0.500、Top-3 0.795 的结果，全面超越 T2M-GPT（FID 0.335, Top-1 0.470, Top-3 0.758）和 MoMask（FID 0.116, Top-1 0.483, Top-3 0.775）。Figure 1 以气泡图形式展示了各方法的 FID 与模型规模关系，MARDM 在更小的模型体积下实现了最优 FID，并展现出良好的可扩展性趋势。Figure 4 的定性对比显示 MARDM 生成的运动会更准确地遵循文本描述的细粒度细节。

![[assets/figures/papers/paper_list_l28_MARDM_Rethinking_Diffusion_for_Text_Driven_Human_Motion_Generation/figures/008_Table_5.jpg]]
*Table 5: Quantitative evaluation on HumanML3D and KIT-ML datasets. We repeat the evaluation 20 times and report the average with 95% confidence interval. For our methods, we report both method results trained to predict noise (DDPM[32]) and velocity (SiT[62]). We use Bold face to indicate the best result and underscore to present the second best*

![[assets/figures/papers/paper_list_l28_MARDM_Rethinking_Diffusion_for_Text_Driven_Human_Motion_Generation/figures/001_Figure_1.jpg]]
*Figure 1: The FID results on HumanML3D dataset. The bubble size is proportional to the model size. We achieve superior performance and demonstrate model scalability*

### 消融实验

Table 6 的消融实验量化了两个核心设计选择的贡献：

![[assets/figures/papers/paper_list_l28_MARDM_Rethinking_Diffusion_for_Text_Driven_Human_Motion_Generation/figures/010_Table_6.jpg]]
*Table 6: Ablation study results comparing our method to variations without reform data representation and distribution and without autoregression. The study is conducted on the HumanML3D dataset*

- **移除表示重构**（即保留冗余表示和原始扩散管线）：FID 从 0.116 升至 2.196（增加 2.080），Top-3 R-Precision 从 0.795 降至 0.703（下降约 8.7%），验证了精简数据表示是性能提升的根本前提。
- **移除掩码自回归建模**（退化为普通扩散）：FID 从 0.116 升至 0.551（增加 0.435），Top-3 R-Precision 从 0.795 降至 0.732（下降约 5.8%），证明掩码自回归分解有效简化了生成目标的优化难度。

Table A2 的进一步消融显示，速度预测（Velocity, FID 0.114）略优于 $x_0$ 预测（FID 0.135），验证了连续时间插值中速度预测目标的优势。Table A3 表明，仅将 MDM 的输入替换为必要维度即可将 FID 从 1.574 降至 0.753，进一步投影到潜空间（MDM-Latent）后 FID 降至 0.327，说明表示重构对扩散基线的提升具有普适性。Table A5 的模型缩放实验显示，模型从 S 增至 XL 时 FID 从 0.278 持续降至 0.116，验证了方法的可扩展性。

![[assets/figures/papers/paper_list_l28_MARDM_Rethinking_Diffusion_for_Text_Driven_Human_Motion_Generation/figures/011_Table.jpg]]
*Table: A3. Training Baseline Methods with Reformed Motion Data Representation and Distribution, Linear schedule and ϵ-prediction Table A4. Original Evaluator Results on HumanML3D. Table A5. Model Scaling results of our model. Increasing model size results in better overall performance on HumanML3D*

![[assets/figures/papers/paper_list_l28_MARDM_Rethinking_Diffusion_for_Text_Driven_Human_Motion_Generation/figures/012_Table.jpg]]
*Table: A1. Reconstruction Results of latent encoders in our method vs baseline methods on HumanML3D data. The AutoEncoder in our method exhibits better reconstruction results. Table A2. Further Ablation Study and Optimization Routine*

### 失败模式与局限

**推理速度瓶颈。** Table A6 显示 MARDM 平均推理时间为 2.4s，显著慢于 MoMask（0.04s）和 T2M-GPT（0.18s），这源于扩散去噪步骤与自回归生成的串行叠加。如何在保持生成质量的前提下加速推理，是当前方法的一个明确短板。

**评估器兼容性问题。** Table A4 的原始评估器结果显示，MARDM 需将输出关节点逆映射回含冗余的表示格式，此转换步骤可能引入额外误差，导致在传统评估器下的性能优势被部分稀释。论文建议社区采用仅关注必要维度的新评估框架以保证公平比较。

**复杂场景未验证。** 当前实验局限于单人文本驱动运动生成，尚未在大规模双人运动、人-物交互等复杂任务上验证连续扩散先验的优越性，这限制了结论的泛化边界。

### 补充图表

![[assets/figures/papers/paper_list_l28_MARDM_Rethinking_Diffusion_for_Text_Driven_Human_Motion_Generation/figures/004_Figure_2.jpg]]
*Figure 2: Code Usage of VQ-VAEs trained with redundancy are more balanced than VQ-VAEs trained with only essential features*

![[assets/figures/papers/paper_list_l28_MARDM_Rethinking_Diffusion_for_Text_Driven_Human_Motion_Generation/figures/002_Table_2.jpg]]
*Table 2: The results of MDM on humanML3D dataset. We report the results of MDM with original $\mathbf { x } _ { \mathrm { 0 } }$ prediction vs. with ϵ prediction. Training to predict $\mathbf { x } _ { 0 }$ leads to better results

![[assets/figures/papers/paper_list_l28_MARDM_Rethinking_Diffusion_for_Text_Driven_Human_Motion_Generation/figures/003_Table_1.jpg]]
*Table 1: Impact of redundant features on VQ-based models. VQ-based methods, T2M-GPT and MoMask, trained with redundant features exhibit better reconstruction performance and lead to better generation quality on the HumanML3D dataset*

![[assets/figures/papers/paper_list_l28_MARDM_Rethinking_Diffusion_for_Text_Driven_Human_Motion_Generation/figures/005_Table_3.jpg]]
*Table 3: The result with existing evaluator on HumanML3D dataset. We alter data by adding noise or replacing it with noise in essential and redundant dimensions. The result shows the evaluator heavily emphasizes redundant dimensions during evaluation*

![[assets/figures/papers/paper_list_l28_MARDM_Rethinking_Diffusion_for_Text_Driven_Human_Motion_Generation/figures/006_Table_4.jpg]]
*Table 4: The evaluation results using evaluators trained on all vs. essential dimensions on HumanML3D. VQ-based models significantly outperform diffusion-based models under alldimension evaluation, but gap closes under essential evaluation*

![[assets/figures/papers/paper_list_l28_MARDM_Rethinking_Diffusion_for_Text_Driven_Human_Motion_Generation/figures/014_Table.jpg]]
*Table: A6. Average Inference Time Results Comparison between our method and baseline methods*



## 定位与知识库关联

### 一、与 VQ 式生成方法的对比与继承

MARDM 的出发点直接源于对 VQ 式方法成功原因的逆向诊断。**T2M-GPT** 与 **MoMask** 等基于 VQ-VAE 或 RVQ-VAE 的离散化方法长期在 HumanML3D 和 KIT-ML 上占据 SOTA，但论文通过消融实验（Table 1）揭示了一个关键事实：VQ 方法的优越性并非完全来自离散表示本身，而是部分源于运动数据中**冗余维度的正则化效应**。

具体而言，当仅使用必要特征训练 VQ-VAE 时，T2M-GPT 的生成 FID 从 0.335 恶化至 0.418，MoMask 的生成 FID 从 0.116 恶化至 0.200。论文将这一现象形式化为重建损失的分解：

$$L_r^{\mathrm{rec}} = \mathcal{L}(\mathbf{x}_e^{GT} - \mathbf{x}_e^{pred} + \mathbf{x}_{r-e}^{GT} - \mathbf{x}_{r-e}^{pred}) = L_e^{rec} + \mathcal{L}(\mathbf{x}_{r-e}^{GT} - \mathbf{x}_{r-e}^{pred})$$

其中 $L_e^{rec}$ 为必要维度的重建损失，$\mathcal{L}(\mathbf{x}_{r-e}^{GT} - \mathbf{x}_{r-e}^{pred})$ 为冗余维度引入的**数据级正则项**。该正则项使 VQ-VAE 的码本使用更加均衡（Figure 2），并间接提升了生成质量。此外，VQ 的离散化机制通过 Voronoi 胞腔约束：

$$V_k = \{z \in \mathbb{R}^d \mid \|z - e_k\|_2 \leq \|z - e_j\|_2\}, \forall j \neq k$$

使得生成误差在不同维度间保持一致性，避免了扩散模型面临的维度间误差失配问题。

MARDM 的回应是**从根本上消除冗余维度**，而非依赖冗余来获得隐式正则化。这一决策使 MARDM 与 VQ 方法在数据表示层面形成根本分歧：VQ 方法受益于冗余，MARDM 则主动移除冗余，转而通过掩码自回归扩散架构来补偿生成质量。

### 二、与扩散式生成方法的对比与改进

在扩散式运动生成方法中，**MDM**、**MotionDiffuse**、**MLD** 和 **ReMoDiffuse** 是主要基线。MARDM 的诊断分析（Table 2）表明，现有扩散方法在运动生成任务中表现不佳的根本原因有二：

**第一，维度分布失配。** 当前运动数据包含关节旋转、局部速度、足部接触等冗余维度，其分布不满足标准正态假设，导致扩散模型的前向加噪与反向去噪过程出现系统性偏差。

**第二，噪声预测误差放大。** 当扩散模型预测噪声 $\epsilon$ 而非 $\mathbf{x}_0$ 时，预测误差会因标准差比率而被放大：

$$\delta_{\mathbf{x}_0} \times \phi_i^{\prime} = \left(\frac{\sqrt{1-\bar{\alpha}_t}}{\sqrt{\bar{\alpha}_t}}\right)^2 \delta_{\epsilon}$$

其中 $\phi_i^{\prime} = \gamma \times \frac{\sigma^{\mathbf{x}\prime}}{\sigma^{\mathbf{x}}}$ 为调整后的标准差比率。实验证据极为明确：MDM 预测 $\epsilon$ 时 FID 高达 31.265，而预测 $\mathbf{x}_0$ 时 FID 降至 0.518（Table 2）。

MARDM 继承了扩散方法中预测 $\mathbf{x}_0$ 或速度 $\mathbf{v}(\mathbf{x}, t)$ 的策略，但在此基础上进行了三项根本性改造：

1. **表示层面**：仅保留根速度、根线性速度、根高度、局部关节位置等必要条件，移除所有冗余维度。
2. **潜空间层面**：使用确定性 1D ResNet AutoEncoder 替代 VQ-VAE，将必要特征投影到紧凑且细粒度的连续潜空间。
3. **生成模式层面**：引入掩码自回归扩散，将全序列生成分解为 $p(\mathbf{x}'^{1:n}|c) = p(\mathbf{m}|c) \prod p(\mathbf{m}|\mathbf{um})$，而非一次性生成整个序列。

消融实验（Table 6）验证了每项改造的贡献：移除表示重构使 FID 从 0.116 恶化至 2.196，移除自回归使 FID 恶化至 0.551。

### 三、评估框架的重新设计

MARDM 的一个重要贡献是揭示了现有评估器的系统性偏差。论文通过实验（Table 3）证明，当冗余维度被替换为噪声时，FID 飙升至 38.167，而必要维度被替换时 FID 仅为 15.164，表明**评估器对冗余维度的敏感度远超必要维度**。这导致扩散方法因在冗余维度上的微小波动而受到不公平惩罚。

在仅使用必要维度训练的新评估器下，MDM 的 R-Precision 表现与 T2M-GPT 接近（Table 4），验证了“扩散方法并非天生不适合运动生成，而是被冗余维度拖累”的核心论断。MARDM 采用新评估器后，在 HumanML3D 上取得了 FID 0.114（Ours-SiT）和 Top-3 R-Precision 0.795 的 SOTA 结果（Table 5）。

### 四、适用边界与局限

**适用边界：**
- MARDM 适用于以文本为条件的单人全身运动生成任务（HumanML3D、KIT-ML 规模）。
- 其掩码自回归扩散架构天然支持时间编辑任务（prefix、in-between、suffix editing，见 Figure A1），在交互式应用场景中具有灵活性。
- 模型规模可扩展：从 S 到 XL，FID 从 0.278 持续下降至 0.116（Table A5），显示出良好的 scaling 特性。

**明确局限：**
1. **推理速度**：平均推理时间约 2.4s（Table A6），显著慢于 MoMask 的 0.04s，限制了实时应用场景。
2. **评估器兼容性**：在原始评估器下，MARDM 需要将潜空间输出转换为关节点再逆映射回冗余表示，可能引入额外误差并导致评估偏差。论文建议采用新评估器，但社区采纳需要时间。
3. **任务泛化未验证**：目前未在大规模双人运动、人‑物交互、语音驱动运动、风格化运动等复杂任务上验证连续扩散先验的优越性。

### 五、开放问题

1. **推理加速**：如何通过蒸馏、缓存或采样步数优化，将标准反向扩散与自回归过程的推理时间压缩至亚秒级？
2. **冗余维度的下游价值**：移除冗余特征后，是否会影响某些需要精细旋转或接触信息的运动下游任务（如物理仿真、运动重定向）？
3. **多模态扩展**：掩码自回归扩散的生成范式能否推广到语音驱动运动、音乐驱动运动或风格化运动生成？
4. **交互场景中的连续先验**：是否可以在更多样化的人‑物、人‑人交互场景中利用连续扩散先验，实现比离散 VQ 方法更自然的运动生成与实时控制？
5. **评估标准的社区共识**：新评估器仅关注必要维度，如何在社区内推动评估标准的更新，以避免因评估框架不一致导致的“苹果与橙子”式比较？



## 原文 PDF

![[paperPDFs/CVPR_2025/MARDM_Rethinking_Diffusion_for_Text_Driven_Human_Motion_Generation.pdf]]
