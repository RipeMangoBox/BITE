---
title: "Accelerating Diffusion Model Training under Minimal Budgets: A Condensation-Based Perspective"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Accelerating_Diffusion_Model_Training_under_Minimal_Budgets_A_Condensation_Based_Perspective.pdf
project_link: null
code_link: null
aliases:
- DCDDC
- ADMTUMBCBP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/benchmarks_datasets_evaluation
core_operator: 训练子集的组成（通过选择真实样本实现的信息性与多样性）以及每个样本附加的语义/视觉条件信号的强度。
primary_logic: 通过构建一个紧凑而信息密集的压缩数据集，可以大幅加速扩散模型训练：首先利用扩散难度分数和间隔采样选择一组具有多样性和可学习性的真实样本子集，然后用预训练模型提取的语义文本嵌入和视觉表征来增强每个样本。
claims:
- D²C 在 10K 图像上仅用 40K 步就在 SiT-XL/2 上达到 gFID 4.23，比 REPA 加速 100×以上。
- 在 4% 数据预算(50K)下，D²C 配合 CFG=1.5 在 180K 步达到 FID 2.78。
- D²C 在 ImageNet 256×256 上 0.8%–8% 数据预算下全面超过随机采样、K-Center 和 Herding。
- 仅使用 Select 阶段即可将 gFID 从 37.07 降至 14.96。
---

# Accelerating Diffusion Model Training under Minimal Budgets: A Condensation-Based Perspective

> [!tip] 核心洞察
> 通过构建一个紧凑而信息密集的压缩数据集，可以大幅加速扩散模型训练：首先利用扩散难度分数和间隔采样选择一组具有多样性和可学习性的真实样本子集，然后用预训练模型提取的语义文本嵌入和视觉表征来增强每个样本。

| 字段 | 内容 |
|------|------|
| 中文题名 | 极小预算下加速扩散模型训练：基于压缩的视角 |
| 英文题名 | Accelerating Diffusion Model Training under Minimal Budgets: A Condensation-Based Perspective |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2507.05914) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/benchmarks_datasets_evaluation |
| Method | D²C (Diffusion Dataset Condensation) |
| Dataset | ImageNet 256×256, ImageNet 512×512, CIFAR-10 |

> [!tip] 效果简介
> - ImageNet 256×256 上，gFID-50K ↓ 3.98 (SiT-L/2, 10K, 100k steps) vs 4.35 (Random, SiT-L/2, 10K, 100k steps) (-0.37)；gFID-50K ↓ 4.23 (SiT-XL/2, 10K, 40k steps) vs REPA 需 4M 步达到可比性能 (>100× 加速)；gFID-50K ↓ 2.78 (SiT-XL/2, 50K, 180k steps, CFG=1.5) vs Vanilla SiT 需 >7M 步 (≈100–233× 加速)。
> - ImageNet 512×512 上，gFID ↓ 5.8 (DiT-L/2, 10K, 300k steps) vs 17.1 (Random, DiT-L/2, 10K, 300k steps) (-11.3)。
> - CIFAR-10 上，gFID-50K ↓ 3.95 (1K budget, 100k steps) vs 9.72 (Random) (-5.77)。

## 概述

扩散模型在高分辨率图像生成中取得了显著成功，但其从零开始的训练过程极其依赖大规模数据和计算资源——典型配置需要数百万张图像和数百个 GPU 日的训练量。这一高昂成本严重制约了资源受限场景下的研究与部署。现有加速方法主要从模型侧入手（如特征对齐正则化 REPA），但鲜有工作从数据侧出发，为生成式模型构建紧凑而高效的训练集。

本文提出 **D²C（Diffusion Dataset Condensation）**，一种面向扩散模型的数据集压缩框架。其核心洞察在于：通过构建一个紧凑而信息密集的压缩数据集，可以在极小数据预算下大幅加速扩散模型训练。D²C 采用两阶段流程——**Select** 与 **Attach**：Select 阶段利用扩散难度分数和间隔采样策略，从原始数据中筛选出一组兼具多样性与可学习性的真实样本子集；Attach 阶段则通过预训练模型提取的语义文本嵌入和视觉表征来增强每个样本的条件信号。

**核心结论：**
- 在仅使用 **0.8% ImageNet 数据（10K 图像）** 的条件下，D²C 配合 SiT-XL/2 在 **40K 训练步**即达到 gFID 4.23，相比 REPA 加速超过 **100 倍**，相比 vanilla SiT-XL/2 加速超过 **233 倍**（Figure 1b，Table 3）。
- 在 **4% 数据预算（50K 图像）** 下，D²C 进一步在 180K 步达到 **FID 2.78**（CFG=1.5），逼近全数据训练的生成质量（Figure 1c，Table 3）。
- 在 ImageNet 256×256 上 0.8%–8% 数据预算范围内，D²C 全面超越随机采样、K-Center 和 Herding 等数据选择基线（Table 1）。
- 仅使用 Select 阶段即可将 gFID 从 37.07 降至 14.96，验证了数据选择本身的有效性（Table 5）。

**方法定位：** D²C 属于数据侧加速范式，与模型侧加速方法（如 REPA）正交互补。其压缩数据集构建过程引入一次性额外计算开销（通过预训练扩散模型计算难度分数），但换取了训练阶段的大幅加速。方法主要在类到图像生成任务上验证，文本到图像生成的扩展已做初步探索（Figure 7），但尚未充分评估。

## 背景与动机

扩散模型已成为视觉生成领域的主流范式，在图像合成、视频生成等任务上展现出前所未有的质量。然而，这一能力的代价极其高昂：从零开始训练一个扩散模型通常依赖数百万张图像和数百个GPU日的计算资源。以ImageNet 256×256上的代表性工作为例，**DiT**（Peebles & Xie, ICCV 2023）和**SiT**（Ma et al., ECCV 2024）等基于Transformer的扩散模型在完整数据集（1.28M图像）上需要数百万次迭代才能收敛，这对资源受限的研究者构成了极高的准入门槛。

### 现有加速路径及其局限

为缓解训练成本问题，现有工作主要沿着两条路径展开：

**模型侧加速**。以**REPA**（Yu et al., 2024）为代表的方法通过引入预训练视觉编码器对扩散模型中间特征进行对齐正则化，在不改变数据的前提下加速收敛。然而，这类方法仍然依赖完整数据集，其加速效果受限于数据本身的冗余性——REPA在SiT-XL/2上仍需约4M步才能达到可比的生成质量。

**数据侧压缩**。另一条路径试图从数据端入手，通过构建更小的训练集来降低计算开销。传统的数据选择方法如随机采样（Random Sampling）、K-Center和Herding，虽然简单直观，但并非为生成模型设计：它们或完全忽略样本的可学习性，或仅关注特征空间的几何覆盖，无法保证所选子集对扩散模型训练的信息密度。更关键的是，现有的数据集蒸馏方法（如**SRe²L**和**RDED**）专为分类任务设计，其优化目标聚焦于类别判别性特征，在生成任务上表现不佳——Table 4显示，用这些方法合成的数据集训练扩散模型，其生成质量甚至不如简单的随机采样。

### 核心瓶颈与本文动机

上述分析揭示了一个根本性瓶颈：**现有数据驱动方法未能直接为生成式模型构建紧凑而高效的训练集**。具体而言，一个理想的训练子集需要同时满足两个条件：

1. **信息性**：每个样本对扩散模型的去噪学习具有足够的“难度”，避免包含大量模型已能轻松处理的冗余样本；
2. **多样性**：子集需覆盖原始数据分布的各个模式，防止模型在有限数据上发生过拟合或模式坍塌。

这两个目标之间存在天然张力——高难度样本往往集中在特定分布区域，而纯多样性采样可能引入大量低信息密度的简单样本。如何系统性地平衡二者，并在极低数据预算（如原始数据的0.8%–4%）下实现高质量生成，构成了本文的核心研究问题。

D²C正是在这一背景下被提出：它从“数据集压缩”的视角重新审视扩散模型训练，将问题分解为**选择**（Select）和**增强**（Attach）两个阶段，在不修改模型架构的前提下，仅通过优化训练数据的组成和条件信号，实现了超过100×的训练加速。

## 核心创新

D²C 的核心创新在于**将扩散模型训练从“模型侧加速”切换为“数据侧压缩”**。传统加速方法（如 REPA）专注于在完整数据集上修改训练目标或模型结构，而 D²C 提出：通过构建一个紧凑而信息密集的压缩数据集，可以从根本上减少训练所需的数据量和迭代步数。这一视角转换带来了三个关键的 **changed slots**：

### 1. 训练数据：从完整数据集到压缩信息子集

**Baseline**：在完整 ImageNet（1.28M 图像）上从零训练扩散模型，依赖海量数据的统计覆盖。

**D²C**：通过 Select 阶段构建一个仅含 10K–100K 图像的紧凑子集。具体而言，首先利用预训练扩散模型计算每张图像的**扩散难度分数** $s_{\mathrm{diff}}(\mathbf{x}) = - \mathbb{E}_{\epsilon,t} [\|\epsilon-\epsilon_{\theta}(\mathbf{x}_t, t, \mathbf{c})\|_2^2]$，量化其去噪可学习性；随后在每个类别内按难度排序，以固定间隔 $k$ 进行**间隔采样**（Interval Sampling），同时保留低难度（结构清晰）和高难度（语境丰富）的样本，在可学习性与多样性之间取得平衡（Figure 3）。这一数据压缩策略是 D²C 加速的根基——仅使用 Select 阶段即可将 gFID 从 37.07 降至 14.96（Table 5）。

### 2. 条件嵌入：从单热类嵌入到语义增强的 DC-Embedding

**Baseline**：使用从零训练的单热类嵌入作为扩散模型的条件信号，缺乏语义先验，在小数据下难以泛化。

**D²C**：在 Attach 阶段引入 **DC-Embedding**（Figure 4），将预训练 T5 文本编码器提取的类别语义嵌入 $t_c$ 与可学习类嵌入 $e_c$ 通过残差 MLP 融合：

$$
\tilde{t}_c = \mathrm{Conv1d}(t_c \times t_{\mathrm{mask}}), \quad y_{\mathrm{text}} = \mathbf{MLP}(\tilde{t}_c) + \tilde{t}_c + e_c
$$

这一设计使得每个训练样本都携带了来自语言模型的丰富语义先验，显著弥补了数据量不足带来的信息缺失。消融实验表明，同时使用文本嵌入和类嵌入优于单独使用任一种（Figure 6 Right）。

### 3. 训练目标：从纯去噪损失到去噪-语义对齐联合优化

**Baseline**：仅使用去噪损失 $\mathcal{L}_{\mathrm{diff}}$ 训练扩散模型。

**D²C**：在去噪损失基础上，额外引入**语义对齐损失** $\mathcal{L}_{\mathrm{proj}}$，将扩散模型中间层输出与冻结 DINOv2 提取的 patch 级视觉表示 $y_{\mathrm{vis}}$ 进行对齐：

$$
\mathcal{L}_{\mathrm{proj}} = -\frac{1}{h} \sum_{i=1}^{h} \frac{\phi(h_i)}{\|\phi(h_i)\|} \cdot \frac{v_i}{\|v_i\|}
$$

最终训练目标为 $\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{diff}} + \lambda \mathbb{E} [\mathcal{L}_{\mathrm{proj}}]$，其中 $\lambda=0.5$。该损失迫使模型在去噪过程中学习与预训练视觉编码器一致的语义表征，增强了生成图像的局部真实感和结构一致性。

### 创新本质：因果杠杆的转移

这三个 changed slots 共同体现了一个核心洞察：**在极小数据预算下，训练子集的组成（信息性与多样性的平衡）和每个样本附加的语义/视觉条件信号的强度，是控制扩散模型训练效率的关键因果杠杆**。D²C 将加速的着力点从“如何在完整数据上更快收敛”转移到“如何让有限数据携带更多有效信息”，从而在 0.8% 数据预算（10K）下仅用 40K 步即达到 gFID 4.23，相对 REPA 实现超过 100× 的加速（Table 3, Figure 1(b)）。

## 整体框架

D²C 采用 **Select–Attach** 两阶段管线，将原始大规模数据集压缩为一个信息密集的紧凑子集，并在其上训练扩散模型。图 2 给出了整体流程。

**阶段一：Select（数据选择）**
目标是从完整数据集中识别一个**多样且可学习**的真实图像子集。该阶段首先利用预训练扩散模型为每张图像计算扩散难度分数 $s_{\mathrm{diff}}(\mathbf{x})$，随后在每个类别内按分数排序并以固定间隔 $k$ 进行间隔采样，从而在“过于简单”与“过于困难”的样本之间取得平衡——前者缺乏信息量，后者可能引入噪声。

**阶段二：Attach（信息增强）**
对选定的每张图像附加丰富的语义与视觉条件信号，以弥补小数据集天然的信息稀疏性。具体包含两个子模块：
- **DC-Embedding**：将预训练文本编码器（T5）提取的类别描述嵌入 $t_c$ 与可学习的类嵌入 $e_c$ 通过残差 MLP 融合，形成最终的文本条件嵌入 $y_{\mathrm{text}}$（图 4）。
- **视觉信息注入**：使用冻结的 DINOv2 提取图像的 patch 级视觉表示 $y_{\mathrm{vis}}$，作为额外的语义先验。

**训练阶段**
压缩数据集构建完成后，扩散模型在标准的去噪损失 $\mathcal{L}_{\mathrm{diff}}$ 之上，额外引入语义对齐损失 $\mathcal{L}_{\mathrm{proj}}$，将扩散模型中间层特征与 $y_{\mathrm{vis}}$ 对齐，以增强局部真实感。总损失为：
$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{diff}} + \lambda \mathbb{E} [\mathcal{L}_{\mathrm{proj}}], \quad \lambda=0.5$$

**输入输出流**
- **输入**：完整数据集（如 ImageNet 1.28M 图像）及类别标签。
- **Select 输出**：经间隔采样得到的紧凑子集（10K–100K 图像）。
- **Attach 输出**：每张图像附加的 $y_{\mathrm{text}}$ 和 $y_{\mathrm{vis}}$。
- **训练输出**：在压缩数据集上训练完成的扩散模型，可在极小训练步数内达到与全数据训练可比的生成质量。

> **关键设计理念**：Select 解决“哪些样本值得学”，Attach 解决“每个样本怎么学得更充分”。二者协同使得扩散模型在 0.8%–4% 的数据预算下实现 100× 以上的训练加速（见表 3 和图 1）。

### 补充图表

![[assets/figures/papers/paper_list_l833_https_arxiv_org_abs_2507_05914/figures/001_Figure_1.jpg]]

## 核心模块与公式推导

D²C 框架由 **Select（选择）** 与 **Attach（附加）** 两个阶段构成（Figure 2）。Select 阶段从完整数据集中筛选紧凑而信息密集的子集，Attach 阶段为每个选中样本注入语义与视觉先验，从而在极小数据预算下实现扩散模型的高效训练。

### 3.1 Select 阶段：扩散难度分数与间隔采样

Select 阶段的核心目标是兼顾子集的**可学习性**与**多样性**。为此，作者提出两个关键机制：

**扩散难度分数（Diffusion Difficulty Score）** 利用一个预训练的类条件扩散模型，对每张图像 $x$ 计算其去噪损失的负期望值：

$$s_{\mathrm{diff}}(\mathbf{x}) = - \mathbb{E}_{\epsilon,t} \left[\|\epsilon-\epsilon_{\theta}(\mathbf{x}_t, t, \mathbf{c})\|_2^2\right] \quad \text{(Eq. 7)}$$

其中 $\epsilon$ 为真实噪声，$\epsilon_{\theta}$ 为模型预测噪声，$\mathbf{x}_t$ 为加噪后的图像，$t$ 为时间步，$\mathbf{c}$ 为类别条件。分数越高，表示该样本对预训练模型而言去噪难度越大。这一度量将“可学习性”量化为模型在该样本上的重建误差——低分样本结构清晰、易于生成，高分样本则包含复杂纹理或罕见姿态，学习难度更高。

**间隔采样（Interval Sampling）** 在每个类别内部，将样本按扩散难度分数升序排列，然后以固定间隔 $k$ 选取样本。这一策略的关键在于：较小的 $k$ 倾向于选取低分（易学习）样本，较大的 $k$ 则使分数分布趋近于随机采样（Figure 3 左）。通过调节 $k$，可在结构清晰度与上下文丰富度之间取得平衡（Figure 3 右）。消融实验表明，对于 50K 预算，$k=16$ 实现了学习性与多样性的最优权衡（Figure 6 左，Figure 8 左）。

### 3.2 Attach 阶段：语义与视觉信息注入

Select 阶段仅确定了“哪些样本”参与训练，Attach 阶段则决定“如何更好地利用每个样本”。其核心思路是用预训练模型提取的冻结表征来增强条件信号和训练监督。

**DC-Embedding 模块**（Figure 4）将文本语义与可学习类嵌入融合为富信息条件向量。首先，用预训练文本编码器（T5）将类别描述模板 $P(c)$ 编码为文本嵌入 $t_c$ 和掩码 $t_{\mathrm{mask}}$：

$$t_c, t_{\mathrm{mask}} = f_{\mathrm{text}}(P(c)) \quad \text{(Eq. 8)}$$

随后，通过 1D 卷积压缩掩码后的文本嵌入，再经残差 MLP 与可学习类嵌入 $e_c$ 融合：

$$\tilde{t}_c = \mathrm{Conv1d}(t_c \times t_{\mathrm{mask}}), \quad y_{\mathrm{text}} = \mathbf{MLP}(\tilde{t}_c) + \tilde{t}_c + e_c \quad \text{(Eq. 9)}$$

残差连接保证了文本先验不会在训练初期被 MLP 完全覆盖，而可学习类嵌入则保留了类别特异性。对比仅使用类嵌入的基线，DC-Embedding 带来显著的 gFID 改善（Figure 6 右），其根本原因在于文本嵌入天然具备语义聚类结构——T5 嵌入空间中语义相近的类别自然聚集，而单热类嵌入则完全不具备此性质（Figure 9）。

**视觉信息注入** 使用冻结的 DINOv2 编码器 $f_{\mathrm{vis}}$ 提取图像的 patch 级视觉表示：

$$y_{\mathrm{vis}} = f_{\mathrm{vis}}(x) \in \mathbb{R}^{N \times d_{\mathrm{text}}} \quad \text{(Eq. 10)}$$

这些表示捕捉了局部纹理和结构信息，将在训练阶段作为语义对齐目标使用。

### 3.3 联合训练目标

在压缩数据集上，扩散模型的去噪损失被修正为同时接受 DC-Embedding 条件：

$$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{\mathbf{x}_0, \epsilon, t} \left[\|\epsilon - \epsilon_{\theta}(\mathbf{x}_t, t, y, y_{\mathrm{text}})\|_2^2\right]$$

此外，引入**语义对齐损失** $\mathcal{L}_{\mathrm{proj}}$，将扩散模型中间层输出的投影与视觉表示 $y_{\mathrm{vis}}$ 对齐：

$$\mathcal{L}_{\mathrm{proj}} = -\frac{1}{h} \sum_{i=1}^{h} \frac{\phi(h_i)}{\|\phi(h_i)\|} \cdot \frac{v_i}{\|v_i\|} \quad \text{(Eq. 11)}$$

其中 $\phi(h_i)$ 为模型隐藏状态 $h_i$ 的线性投影，$v_i$ 为对应的 DINOv2 patch 表示，$h$ 为 patch 数量。该损失实质上是余弦相似度的最大化，强制扩散模型在去噪过程中学习与视觉编码器一致的局部语义结构。

最终训练目标为两者的加权组合：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{diff}} + \lambda \mathbb{E} [\mathcal{L}_{\mathrm{proj}}], \quad \lambda=0.5 \quad \text{(Eq. 12)}$$

消融实验（Table 5）验证了各模块的独立贡献：仅使用 Select 阶段即可将 gFID 从 37.07 降至 14.96；同时使用 DC-Embedding 和视觉嵌入达到最佳 gFID 7.62，超过单独任一种配置。视觉编码器消融（Table 7）进一步表明 DINOv2-L 在语义对齐任务上优于其他编码器。

### 补充图表

![[assets/figures/papers/paper_list_l833_https_arxiv_org_abs_2507_05914/figures/003_Figure_3.jpg]]
*Figure 3: Left: Distribution of diffusion difficulty scores under different interval values k. Smaller intervals (e.g., 1, 2) favor low-loss samples, while larger intervals (e.g., 64, 128) result in a distribution closer to random sampling, thus approximating the original data distribution. Moderate intervals (e.g., 16) provide balanced coverage across difficulty levels. Right: Representative samples selected by three strategies: Min (lowest score), Max (highest score), and Interval (our proposed strategy). Interval sampling achieves a balance between structural clarity and contextual richness*

![[assets/figures/papers/paper_list_l833_https_arxiv_org_abs_2507_05914/figures/004_Figure_4.jpg]]
*Figure 4: Overview of DC-Embedding*

## 实验与分析

### 主结果：极小预算下的加速与生成质量

D²C 的核心主张——通过压缩数据集实现扩散模型训练的极致加速——在 ImageNet 256×256 和 512×512 上得到了系统性验证。实验以 gFID-50K 为主要评判指标，覆盖了从 0.8%（10K）到 8%（100K）的多种数据预算。

**与数据集压缩方法的对比。** 在 DiT-L/2 和 SiT-L/2 两种架构下，D²C 在所有预算档位均显著超过随机采样、K-Center 和 Herding 等经典选择策略（Table 1）。以 SiT-L/2 在 10K 预算、100K 训练步为例，D²C 的 gFID-50K 达到 3.98，而随机采样基线为 4.35。当预算放宽到 50K 时，D²C 在 SiT-L/2 上的 gFID-50K 进一步降至 2.99，展现出随数据量增加而稳定提升的趋势。

**与加速算法的对比。** Table 3 集中体现了 D²C 的加速能力。在仅使用 10K 图像（0.8% 数据）的极端设置下，D²C 训练 SiT-XL/2 仅需 40K 步即可达到 gFID 4.23，而 REPA——一种基于预训练视觉编码器特征对齐的模型侧正则化方法——需要 4M 步才能达到可比性能，加速比超过 100×。与 vanilla SiT-XL/2 相比，加速比更是高达 233× 以上。当数据预算提升至 50K（4% 数据）并配合 CFG=1.5 时，D²C 在 180K 步达到 FID 2.78，而 vanilla SiT 需要超过 7M 步。

**高分辨率场景。** 在 ImageNet 512×512 上（Table 2），仅使用 10K 图像的 D²C 在 DiT-L/2 上达到 gFID 5.8，而随机采样基线高达 17.1，差距达 11.3 个 FID 点。这验证了压缩数据集策略在高分辨率生成任务中同样有效。

**与合成数据集方法的对比。** 论文还将 D²C 与两类面向分类任务的数据集蒸馏方法 SRe²L 和 RDED 进行了对比（Table 4）。SRe²L 是像素级蒸馏方法，RDED 是图像级压缩方法。在 10K 数据预算下，D²C 训练的扩散模型生成质量远超这两种方法——SRe²L 和 RDED 生成的合成图像本身质量有限，在其上训练的扩散模型 gFID 分别为 14.79 和 9.74，而 D²C 仅 4.23。这揭示了一个关键洞察：为分类任务设计的压缩方法无法直接迁移到生成任务，因为生成模型对图像的细粒度结构和语义完整性要求更高。

**跨数据集泛化。** 在 CIFAR-10 上（Table 8），D²C 在 1K 预算、100K 步下达到 gFID 3.95，而随机采样为 9.72，优势同样显著，说明该方法不局限于大规模数据集。

### 消融实验：Select 与 Attach 的贡献分解

Table 5 对 D²C 的两阶段进行了系统消融。基线（无 Select 无 Attach）的 gFID 为 37.07。仅启用 Select 阶段（扩散难度分数 + 间隔采样），gFID 骤降至 14.96，降幅超过 22 个点，证明**数据子集的选择是性能提升的首要瓶颈**。在此基础上，单独添加 DC-Embedding 或视觉嵌入均能进一步将 gFID 降至 10.44 和 10.91。当两者同时启用时，gFID 达到最优的 7.62，显示出语义文本条件与视觉先验之间存在互补增益。

![[assets/figures/papers/paper_list_l833_https_arxiv_org_abs_2507_05914/figures/011_Table_5.jpg]]
*Table 5: Ablation studies on the Select and Attach phases. Sel.: Select. Vis.: Vision*

**间隔采样参数 k 的影响。** Figure 6（左）和 Figure 8（左）联合揭示了 k 的调节规律。较小的 k 值（如 k=1、2）倾向于选择低难度样本，训练初期收敛更快，但最终 gFID 受限于多样性不足。较大的 k 值（如 k=64、128）使难度分布趋近于随机采样，丧失了可学习性筛选的优势。在 50K 预算下，k=16 实现了可学习性与多样性的最佳平衡，取得最优 gFID-10K。这一最优 k 值与数据预算大致呈比例缩放关系——10K 预算下最优 k=96。

**DC-Embedding 内部消融。** Figure 6（右）显示，同时使用 T5 文本嵌入和可学习类嵌入的 DC-Embedding 显著优于仅使用类嵌入的基线。Figure 9 的 t-SNE 可视化从几何角度解释了这一优势：one-hot 类嵌入在特征空间中无任何语义结构，而 T5 文本嵌入天然地将语义相近的类别（如不同犬种）聚集在一起，为扩散模型提供了更丰富的条件信号。

**视觉编码器选择。** Table 7 消融了 DINOv2-L、DINOv2-G、CLIP-L 和 MAE-L 四种视觉编码器。DINOv2-L 取得最佳 FID 7.62，表明其 patch 级语义表征与扩散模型中间层特征的对齐效果最优。

### 计算开销分析

Table 6 给出了 D²C 各子流程的计算开销分解。主要的一次性开销来自扩散难度分数计算（需对每张候选图像执行完整的去噪前向过程）和视觉特征提取。论文指出这些开销仅发生在压缩数据集构建阶段，一旦数据集构建完成，后续的扩散模型训练无需额外开销。与从零开始训练完整数据集所需的数百 GPU 日相比，这一预处理开销是可接受的。

### 定性分析

Figure 5 展示了在 10K 和 50K 数据预算下，D²C 与随机采样的生成效果对比。在 10K 极端预算下，随机采样的生成图像出现明显的结构扭曲和语义错误，而 D²C 能够保持合理的物体形态和纹理。在 50K 预算下，D²C 的生成质量进一步接近全数据训练的视觉效果。Figure 11 至 Figure 21 展示了在 ImageNet 512×512 上使用 D²C 训练的 SiT-L/2 在多个类别上的生成样本，涵盖金刚鹦鹉、北极狼、美洲豹、水獭、小熊猫、大熊猫、消防车、芝士汉堡、湖岸和火山等类别，验证了方法在多样化语义类别上的泛化能力。

![[assets/figures/papers/paper_list_l833_https_arxiv_org_abs_2507_05914/figures/005_Figure_5.jpg]]

### 失败模式与局限性

论文明确指出的局限性包括：（1）压缩数据集构建依赖一个预训练扩散模型来计算难度分数，引入一次性额外计算开销；（2）方法主要在类到图像生成任务上验证，文本到图像生成的扩展仅做了初步讨论（Figure 7 展示了在 LAION 文本-图像对上计算的难度分数分布，与类条件分布相似，暗示了扩展可能性，但尚未充分评估）；（3）最优间隔参数 k 依赖具体数据集和预算，需要针对每个场景调优。这些点需要读者在实际应用中注意。

### 补充图表

![[assets/figures/papers/paper_list_l833_https_arxiv_org_abs_2507_05914/figures/006_Table_1.jpg]]
*Table 1: Comparison of gFID-50K across various dataset condensation methods and data budgets using DiT-L/2 and SiT-L/2 on ImageNet 256×256. We use CFG=1.5 for evaluation*

![[assets/figures/papers/paper_list_l833_https_arxiv_org_abs_2507_05914/figures/008_Table_3.jpg]]
*Table 3: Comparison of acceleration algorithms on ImageNet-1K*

![[assets/figures/papers/paper_list_l833_https_arxiv_org_abs_2507_05914/figures/009_Table_2.jpg]]
*Table 2: Comparison with a strict data budget 0.8% (10K) on ImageNet 512×512. We use CFG=1.5 for evaluation*

![[assets/figures/papers/paper_list_l833_https_arxiv_org_abs_2507_05914/figures/007_Figure_6.jpg]]
*Figure 6: Left: Interval-sampling ablation. Small k speeds early training. The best final gFID-10K appears at k=96 for the 10K budget and k=16 for the 50K budget, roughly scaling with data size. Right: DC-Embedding ablation at 10K. Combining text and class embeddings outperforms either alone; “Only Class” denotes the baseline that injects class embeddings only*

![[assets/figures/papers/paper_list_l833_https_arxiv_org_abs_2507_05914/figures/014_Figure_8.jpg]]
*Figure 8: Left: gFID-10K across training steps under different interval values k for a 50K data budget. Moderate intervals (e.g., k = 16) achieve superior performance by balancing learnability and diversity. Right: Distributional discrepancy (gFID-10K) between ranked training subsets and the validation set. Both extremely low and high diffusion difficulty score lead to higher FID, while mid-range segments show better alignment*

![[assets/figures/papers/paper_list_l833_https_arxiv_org_abs_2507_05914/figures/017_Table_7.jpg]]
*Table 7: Ablation of the visual encoder*

![[assets/figures/papers/paper_list_l833_https_arxiv_org_abs_2507_05914/figures/010_Table_4.jpg]]

## 方法谱系与知识库定位

### 问题定位：从“模型加速”到“数据压缩”的视角转换

扩散模型训练的核心瓶颈在于**数据需求与计算开销的双重爆炸**：从零训练一个高质量的类条件扩散模型（如 DiT-XL/2）通常需要数百万图像和数百 GPU·日的算力投入。现有加速策略主要从**模型侧**入手，包括架构改进、训练目标重设计、蒸馏、以及利用预训练视觉编码器进行表示对齐（如 **REPA**）。然而，这些方法仍然依赖完整数据集，并未触及“是否可以用更少的数据训练出同等质量的模型”这一根本问题。

D²C 的关键视角转换在于：**将扩散模型训练的瓶颈从模型优化转移到数据集构建**。这一思路与分类任务中的数据集蒸馏（Dataset Distillation / Condensation）一脉相承——通过合成或选择紧凑的信息密集子集来替代完整训练集。但扩散模型的数据集压缩面临独特挑战：生成任务要求子集不仅覆盖类别分布，还需保留足够的视觉细节和语义信息以支撑高分辨率图像的生成。

### 方法谱系：D²C 在数据压缩与加速研究中的位置

#### 相对于数据选择基线

D²C 的 **Select 阶段**直接对标三类经典数据选择方法：

- **Random Sampling**：朴素基线，按均匀分布随机选取固定数量样本。在极小数据预算（如 0.8%）下，随机采样无法保证覆盖尾部类别和困难样本，导致生成质量急剧下降（gFID 高达 37.07）。
- **K-Center**：基于多样性的贪心选择，迭代选取最大最小距离的样本以保证特征空间覆盖。其局限在于倾向于选择离群点，可能引入噪声样本而损害可学习性。
- **Herding**：基于特征空间几何平均的选择方法，旨在选取代表性样本。与 K-Center 类似，该方法仅考虑多样性而忽略了样本对扩散模型训练的可学习性。

D²C 的核心创新在于引入**扩散难度分数**（Diffusion Difficulty Score）作为可学习性度量，并通过**间隔采样**（Interval Sampling）在可学习性与多样性之间建立可控的权衡机制。这一设计的因果逻辑是：仅选择低难度样本会导致多样性不足（模型过拟合简单模式），仅选择高难度样本会引入噪声和异常值（模型难以收敛），而间隔采样通过均匀覆盖难度谱的各个区间，同时保证了子集的多样性和可学习性。

#### 相对于数据集蒸馏方法

D²C 与像素级数据集蒸馏方法（如 **SRe²L**）和图像级压缩方法（如 **RDED**）存在本质差异：

- **SRe²L** 等方法通过梯度匹配或轨迹匹配合成全新的“蒸馏图像”，这些图像在像素空间中可能不自然，但包含丰富的训练信号。然而，对于扩散模型而言，合成图像的分布偏移会引入额外的域差异，损害生成质量（Table 4 显示 SRe²L 在 ImageNet 256×256 上 gFID 显著劣于 D²C）。
- **RDED** 等方法通过分割引导选择真实图像区域进行拼接，保留了像素真实性，但缺乏对扩散模型特定训练需求的适配。

D²C 采取**“选择+增强”的混合策略**：Select 阶段保留真实图像的像素真实性，Attach 阶段通过注入预训练模型的语义和视觉先验来弥补子集规模缩减带来的信息损失。这种设计使得 D²C 既避免了合成图像的域偏移问题，又超越了纯选择方法的信息瓶颈。

#### 相对于模型侧加速方法

在加速扩散模型训练的谱系中，D²C 与 **REPA** 等方法形成互补而非替代关系：

- **REPA** 通过在训练过程中对齐扩散模型内部表示与预训练视觉编码器（如 DINOv2）的特征来加速收敛，但仍在完整数据集上训练。
- D²C 的 **Attach 阶段**借鉴了类似的表示对齐思想（通过 $\mathcal{L}_{\mathrm{proj}}$ 将扩散模型中间层输出与 DINOv2 patch 特征对齐），但将其应用于压缩数据集场景。关键区别在于：D²C 的对齐损失是在极小数据预算下发挥作用的，其效果与 Select 阶段形成协同——优质子集为表示对齐提供了更干净的训练信号。

从加速效果看，D²C 在 SiT-XL/2 上仅用 40K 步即达到 gFID 4.23，而 REPA 需要约 4M 步才能达到可比性能，加速比超过 100×。这验证了**数据侧压缩与模型侧加速可以产生乘数效应**。

### 适用边界与关键依赖

D²C 的有效性建立在以下前提之上，这些前提也划定了其适用边界：

1. **预训练模型的可用性**：Select 阶段依赖预训练扩散模型计算难度分数，Attach 阶段依赖预训练文本编码器（T5）和视觉编码器（DINOv2）。这些预训练模型引入了一次性额外计算开销（Table 6 给出了详细分解），但作者论证该开销可通过训练加速得到充分补偿。在缺乏合适预训练模型的领域（如医学图像、科学数据），D²C 的直接适用性需要进一步验证。

2. **类别条件的结构化**：当前方法针对类到图像（C2I）生成任务设计，DC-Embedding 利用类别名称通过 T5 提取文本嵌入。对于无类别标签或类别结构模糊的数据集，需要重新设计条件信号的构建方式。Figure 7 初步展示了在 LAION 文本-图像对上计算的难度分数分布与 C2I 场景相似，暗示了向文本到图像（T2I）生成扩展的可行性，但尚未充分验证。

3. **间隔参数 k 的数据依赖性**：消融实验（Figure 6 Left, Figure 8 Left）表明，最优间隔 k 依赖于数据预算和数据集特性——10K 预算下 k=96 最优，50K 预算下 k=16 最优。目前缺乏自动确定 k 的机制，需要针对每个场景进行网格搜索，这在实际部署中增加了调参成本。

### 局限性与开放问题

#### 已验证的局限性

1. **一次性计算开销**：压缩数据集的构建需要完整的预训练扩散模型前向传播来计算难度分数，以及 T5 和 DINOv2 的推理来提取语义和视觉嵌入。虽然总开销可通过训练加速补偿，但对于极小规模实验或资源极度受限的场景，这一前置成本可能成为障碍。

2. **任务泛化验证不足**：当前实验集中在 ImageNet 类条件生成（256×256 和 512×512）和 CIFAR-10 上。文本到图像生成的扩展仅做了难度分数分布的初步分析（Figure 7），缺乏端到端的训练实验和生成质量评估。

3. **超参数敏感性**：间隔 k、对齐损失权重 λ（固定为 0.5）、视觉编码器选择（DINOv2-L 在消融中表现最佳）等关键超参数需要针对不同设置调整，目前缺乏自适应机制。

#### 开放研究问题

1. **大规模 T2I 扩展**：如何将 D²C 高效且全自动地扩展到 SDXL 等大规模文本到图像生成模型？这需要解决文本条件的多样性建模、大规模数据集的难度分数高效计算、以及文本-图像对的多样性保持等挑战。

2. **难度分数的理论保障**：扩散难度分数作为子集选择标准的有效性已在实验中得到验证，但缺乏理论层面的支撑——例如，能否建立难度分数分布与模型泛化误差之间的界限？这关系到方法在分布外场景下的可靠性。

3. **压缩数据集的可复用性**：D²C 构建的压缩数据集是否可复用于其他下游任务（如图像编辑、反演、定制化生成）？如果压缩数据集具有任务通用性，其价值将远超单次训练加速。

4. **自动化间隔确定**：是否存在基于数据集难度分布统计特性（如偏度、峰度、模态数）的自动化 k 确定方法？这将是方法从研究走向实际部署的关键一步。

5. **与模型侧方法的深度融合**：D²C 的 Attach 阶段已初步展示了数据压缩与表示对齐的协同效应。是否存在更紧密的耦合方式——例如，让 Select 阶段的难度分数感知 Attach 阶段的表示对齐强度，或者联合优化子集选择与模型训练目标？这可能在极小预算下进一步突破当前性能上限。

## 原文 PDF

![[paperPDFs/CVPR_2026/Accelerating_Diffusion_Model_Training_under_Minimal_Budgets_A_Condensation_Based_Perspective.pdf]]