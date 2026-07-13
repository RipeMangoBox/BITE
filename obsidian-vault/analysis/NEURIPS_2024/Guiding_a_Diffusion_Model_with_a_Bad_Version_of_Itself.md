---
title: Guiding a Diffusion Model with a Bad Version of Itself
type: paper
paper_level: A
venue: NEURIPS
year: 2024
pdf_ref: paperPDFs/NeurIPS_2024/Guiding_a_Diffusion_Model_with_a_Bad_Version_of_Itself.pdf
project_link: null
code_link: https://github.com/NVlabs/edm2
aliases:
- GDMBVI
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 引导模型的质量退化程度（通过减少容量和训练时间实现）
primary_logic: 利用一个能力较弱但任务相同的模型作为引导，可以识别并纠正主模型在低概率区域的拟合不足，从而在不牺牲多样性的情况下提高生成质量。本质是通过模型间的预测差异检测欠拟合区域，并将样本拉回数据流形的高概率核心。
claims:
- 在 ImageNet-512 上，使用 EDM2-S 时，autoguidance 将 FID 从 2.56 降至 1.34，创造了新的纪录。
- 在 ImageNet-64 上，autoguidance 将 FID 从 1.58 降至 1.01。
- 2D 玩具示例表明，autoguidance 消除了离群点，同时保留了分布的所有分支，而 CFG 则丢弃了整个分支。
- 仅当主模型和引导模型受到相同类型的退化时，autoguidance 才有效。例如，dropout 的引导模型必须对应 dropout 的主模型，否则无效。
---

# Guiding a Diffusion Model with a Bad Version of Itself

> [!tip] 核心洞察
> 利用一个能力较弱但任务相同的模型作为引导，可以识别并纠正主模型在低概率区域的拟合不足，从而在不牺牲多样性的情况下提高生成质量。本质是通过模型间的预测差异检测欠拟合区域，并将样本拉回数据流形的高概率核心。

| 字段 | 内容 |
|------|------|
| 中文题名 | 利用较差版本自身引导扩散模型 |
| 英文题名 | Guiding a Diffusion Model with a Bad Version of Itself |
| 会议/期刊 | NEURIPS 2024 |
| Links | [paper](https://openreview.net/forum?id=bg6fVPVs3s) · [Code](https://github.com/NVlabs/edm2) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Autoguidance |
| Dataset | ImageNet-512 with EDM2-S, ImageNet-512 with EDM2-XXL, ImageNet-64 with EDM2-S, ImageNet-512 Unconditional with EDM2-S |

> [!tip] 效果简介
> - ImageNet-512 with EDM2-S 上，FID 1.34 vs 2.56 (-1.22)。
> - ImageNet-512 with EDM2-XXL 上，FID 1.25 vs 1.91 (-0.66)。
> - ImageNet-64 with EDM2-S 上，FID 1.01 vs 1.58 (-0.57)。

## 概要

扩散模型在图像生成中面临一个核心瓶颈：分数匹配训练倾向于覆盖整个数据分布，导致模型在低概率区域产生不切实际的离群样本。这些区域由于训练数据稀疏，模型无法准确学习真实密度，从而生成质量低下的图像。现有的 Classifier-Free Guidance（CFG，Ho & Salimans, NIPS 2022）通过引入无条件模型作为引导信号，虽能消除离群点并提升图像质量，但代价是牺牲生成多样性——CFG 倾向于丢弃数据分布中的整个分支，使样本过度集中于类别核心。

本文提出 **Autoguidance**，一种解耦图像质量与多样性的引导方法。其核心洞察是：利用一个能力较弱但任务相同的模型作为引导，可以识别并纠正主模型在低概率区域的拟合不足，从而在不牺牲多样性的情况下提高生成质量。具体而言，该方法使用主模型的一个较差版本（通过减少容量和/或训练时间获得）作为引导模型，保持条件信息不变，通过两个模型预测差异的外推，将样本拉回数据流形的高概率核心。

该方法的本质机制在于：引导产生的额外力来源于两个模型隐含密度的比值梯度，该梯度指向数据流形的核心区域。与 CFG 依赖于条件模型与无条件模型之间的任务差异不同，Autoguidance 利用的是同一任务下模型质量差异所揭示的欠拟合区域。

在 ImageNet-512 上，Autoguidance 将 EDM2-S 的 FID 从 2.56 降至 1.34，创造了新的纪录；在 ImageNet-64 上，FID 从 1.58 降至 1.01。二维玩具示例直观展示了 Autoguidance 的优势：它消除了离群点，同时保留了分布的所有分支，而 CFG 则丢弃了整个分支。

### 扩散模型的内在困境：低概率区域的离群样本

扩散模型通过概率流常微分方程（Probability Flow ODE）从纯噪声逐步演化生成数据样本：

$$
\mathrm{d}\mathbf{x}_\sigma = -\sigma \nabla_{\mathbf{x}_\sigma} \log p(\mathbf{x}_\sigma; \sigma) \mathrm{d}\sigma
$$

该方程定义了一条从高噪声到低噪声的确定性反向轨迹，理论上维持每一步的边际分布。然而，实际训练中，去噪网络 $D_\theta$ 通过最小化均方误差来学习分数函数：

$$
\theta = \arg\min_\theta \mathbb{E}_{\mathbf{y}\sim p_{\mathrm{data}}, \sigma\sim p_{\mathrm{train}}, \mathbf{n}\sim\mathcal{N}(\mathbf{0},\sigma^2\mathbf{I})} \|D_\theta(\mathbf{y}+\mathbf{n};\sigma) - \mathbf{y}\|_2^2
$$

这一训练目标本质上是一个回归任务，倾向于在整个数据分布上均匀覆盖。**核心瓶颈在于**：数据分布的低概率区域天然缺乏足够的训练样本，模型在这些区域无法准确学习分数函数，导致采样轨迹漂移到这些欠拟合区域时，会生成不切实际的离群样本。这些离群样本严重损害了生成图像的整体质量，成为扩散模型在追求高保真度生成时面临的根本性挑战。

### 现有引导方法的局限：质量与多样性的两难

**Classifier-Free Guidance（CFG）**（Ho & Salimans, NIPS 2022）是目前最广泛采用的引导技术。它通过外推条件模型和无条件模型的预测差异来增强生成质量：

- **机制**：CFG 利用无条件去噪模型作为引导信号，将条件模型的预测向远离无条件分布的方向外推。
- **效果**：显著提升了类别对齐度和图像质量，成为文本到图像生成系统的标配组件。
- **根本问题**：CFG 同时混合了两种效应——**图像质量的提升**和**类别对齐的增强**。这两种效应无法解耦，导致在追求高质量时不可避免地牺牲多样性。如论文的二维玩具示例（Figure 1）所示，CFG 在消除离群点的同时，会完全丢弃数据分布的某些分支，使生成结果趋向模板化。此外，CFG 在无条件生成场景下完全无法使用，因为无条件模型和条件模型之间的“任务差异”在无条件设定下不存在。

**Guidance Interval**（Kynkäänniemi et al., 2024）作为 CFG 的变体，尝试通过限制引导仅作用于特定噪声水平区间来缓解多样性的损失，但本质上仍受限于 CFG 的固有问题——质量与多样性的耦合。

朴素的**分数截断**技巧则通过均匀放缩所有分数向量的模长来增强引导强度，缺乏对数据流形结构的感知，容易在提升质量的同时引入新的伪影。

### 核心动机：解耦质量提升与多样性保持

本文的核心洞察是：**图像质量的提升与类别对齐的增强是两种不同的效应，应该被解耦处理**。CFG 之所以陷入两难，根源在于引导模型（无条件模型）与主模型（条件模型）之间存在任务差异——前者建模无条件分布，后者建模条件分布。这种差异使得外推方向同时包含了质量提升和类别对齐两个分量。

一个自然的替代方案是：**使用一个与主模型任务完全相同但能力较弱的模型作为引导**。该弱模型在低概率区域同样存在拟合不足，但其预测与强模型的差异恰好揭示了这些欠拟合区域的位置。通过外推两个模型之间的差异，可以将样本从数据流形的边缘拉回高概率核心，同时不偏向任何特定类别或模态，从而在保持完整多样性的前提下提升图像质量。

这种“用较差版本自身引导自身”的思路，为扩散模型的质量控制提供了一种全新的范式：不需要额外的条件信号，不需要任务转换，仅通过模型容量和训练程度的退化即可获得解耦的质量提升。

## 核心方法与创新机理

Autoguidance 的核心创新在于**重新定义了扩散模型引导信号的来源**：将传统 CFG 中使用的“无条件模型”替换为一个**能力较差的同任务模型**（即主模型自身的“劣化版本”）。这一改变看似简单，却从根本上解决了 CFG 长期存在的任务偏差（task discrepancy）问题。

### 问题根源：CFG 的任务偏差

在 CFG 中，引导信号来源于条件模型 $D_\theta(\mathbf{x}; \sigma, \mathbf{c})$ 与无条件模型 $D_\theta(\mathbf{x}; \sigma, \emptyset)$ 之间的外推。由于无条件模型的任务（无条件生成）与条件模型的任务（条件生成）本质不同，两者在低概率区域的拟合偏差并不一致。这导致 CFG 的引导力 $\nabla_{\mathbf{x}} \log \frac{p_1(\mathbf{x}|\mathbf{c};\sigma)}{p_0(\mathbf{x}|\mathbf{c};\sigma)}$ 在提升图像质量的同时，会系统性地丢弃数据分布中的某些分支（Figure 1c），从而损害多样性。

### 关键洞察：同任务劣化模型作为引导

Autoguidance 的核心洞察是：**图像质量的提升可以通过比较同一任务上两个不同质量模型的预测差异来实现**。具体而言，使用一个容量更小和/或训练更少的“劣化版”模型 $D_0$ 作为引导模型，与高质量主模型 $D_1$ 进行外推：

$$D_w(\mathbf{x};\sigma,\mathbf{c}) = w D_1(\mathbf{x};\sigma,\mathbf{c}) + (1-w) D_0(\mathbf{x};\sigma,\mathbf{c})$$

其中 $w > 1$ 强调 $D_1$ 的预测。此时引导力变为：

$$\nabla_{\mathbf{x}} \log p_w(\mathbf{x}|\mathbf{c};\sigma) = \nabla_{\mathbf{x}} \log p_1(\mathbf{x}|\mathbf{c};\sigma) + (w-1) \nabla_{\mathbf{x}} \log \frac{p_1(\mathbf{x}|\mathbf{c};\sigma)}{p_0(\mathbf{x}|\mathbf{c};\sigma)}$$

由于 $D_0$ 和 $D_1$ 共享相同的任务和条件，两者在数据流形核心区域（高概率区域）的预测高度一致，引导力在此处趋近于零；而在低概率的欠拟合区域，$D_0$ 的误差显著大于 $D_1$，引导力会将样本拉回高概率核心。这实现了**对图像质量的解耦控制**——在消除离群样本的同时，不牺牲多样性的任何分支（Figure 1e）。

### 劣化兼容性：autoguidance 有效的充要条件

论文通过实验揭示了一个关键约束：**引导模型必须受到与主模型相同类型的劣化**。当主模型 $D_1$ 使用 5% dropout 训练时，只有同样使用 dropout（如 10%）训练的 $D_0$ 才能产生有效的 autoguidance；若 $D_0$ 的劣化来自输入噪声而非 dropout，则引导完全无效，最佳 FID 出现在 $w=1$（即无引导）。这表明 autoguidance 的本质是利用**同源误差的放大**来检测和纠正欠拟合区域，而非简单的模型集成。

### 与 CFG 的本质区别

| 维度 | CFG | Autoguidance |
|------|-----|-------------|
| 引导模型 | 无条件去噪器（任务不同） | 同任务劣化模型（任务相同） |
| 引导力来源 | 条件与无条件的密度比梯度 | 高质量与低质量模型的密度比梯度 |
| 对多样性的影响 | 丢弃低概率分支 | 保留所有分支，仅消除离群点 |
| 任务偏差 | 存在（条件 vs. 无条件） | 不存在（任务完全一致） |

这一创新使得 autoguidance 在 ImageNet-512 上将 EDM2-S 的 FID 从 2.56 降至 1.34，创造了新的纪录，同时 FDDINOv2 从 68.64 降至 36.67，表明生成质量与多样性的双重提升。

Autoguidance 的核心思想是利用一个质量较差的模型版本作为引导信号，对高质量主模型的生成过程进行校正。其整体 pipeline 围绕扩散模型的概率流 ODE 展开，通过线性外推两个去噪器的输出来实现引导。

### 模块构成与数据流

整个生成框架由四个关键模块串联而成，数据流从纯噪声逐步演化为最终图像：

1. **主去噪网络 D₁**：这是负责生成最终图像的高质量扩散模型，通常具有较大的容量（如 EDM2-S 或 EDM2-XXL）并经过充分训练。它接收带噪图像 x、噪声水平 σ 以及条件信息 c（如类别标签），输出对干净图像的预测。

2. **引导去噪网络 D₀**：一个质量较差的辅助模型，与 D₁ 共享完全相同的任务、条件格式和数据分布，但受到特定的退化处理——通常是通过减小模型容量（如从 S 降至 XS）和/或大幅缩短训练时间（如仅训练 1/16 的迭代次数）来实现。D₀ 不直接参与最终图像的生成，而是提供参考信号。

3. **引导外推模块**：这是 autoguidance 的核心运算单元。在每个去噪步骤中，将 D₁ 和 D₀ 的输出进行线性组合：

   $$D_w(\mathbf{x};\sigma,\mathbf{c}) = w D_1(\mathbf{x};\sigma,\mathbf{c}) + (1-w) D_0(\mathbf{x};\sigma,\mathbf{c})$$

   其中 $w > 1$ 是引导权重，用于强调 D₁ 相对于 D₀ 的优势。当 $w=1$ 时退化为无引导的 D₁ 单独工作；$w$ 越大，引导力越强。这一外推操作等价于对一个重新加权的密度进行采样：

   $$D_w(\mathbf{x};\sigma,\mathbf{c}) \approx \mathbf{x} + \sigma^2 \nabla_{\mathbf{x}} \log \left( p_0(\mathbf{x}|\mathbf{c};\sigma) \left[ \frac{p_1(\mathbf{x}|\mathbf{c};\sigma)}{p_0(\mathbf{x}|\mathbf{c};\sigma)} \right]^w \right)$$

   其对应的分数函数可分解为：

   $$\nabla_{\mathbf{x}} \log p_w(\mathbf{x}|\mathbf{c};\sigma) = \nabla_{\mathbf{x}} \log p_1(\mathbf{x}|\mathbf{c};\sigma) + (w-1) \nabla_{\mathbf{x}} \log \frac{p_1(\mathbf{x}|\mathbf{c};\sigma)}{p_0(\mathbf{x}|\mathbf{c};\sigma)}$$

   第一项是主模型 D₁ 的条件分数，第二项是引导力——它正比于两个模型隐含密度比值的梯度，方向指向 D₁ 相对于 D₀ 拟合更好的区域，即数据流形的高概率核心。

4. **ODE 求解器**：使用 Heun 二阶确定性求解器，沿概率流 ODE 从高噪声向低噪声方向逐步演化：

   $$\mathrm{d}\mathbf{x}_\sigma = -\sigma \nabla_{\mathbf{x}_\sigma} \log p(\mathbf{x}_\sigma; \sigma) \mathrm{d}\sigma$$

   在每个噪声水平 σ 上，用引导外推后的 $D_w$ 输出来估计分数 $\nabla_{\mathbf{x}} \log p$，从而确定下一步的演化方向。

### 工作机制：为什么有效

引导力 $(w-1) \nabla_{\mathbf{x}} \log \frac{p_1}{p_0}$ 的本质是检测并纠正主模型 D₁ 的拟合不足区域。当 D₁ 和 D₀ 对某个样本的预测一致时，比值梯度接近零，引导力微乎其微；当两者预测出现分歧时——这通常发生在数据稀疏的低概率区域，D₁ 的拟合也不可靠——引导力会将样本拉回两个模型都更有把握的区域，即数据流形的核心。

这一机制在 2D 玩具示例（Figure 1e）中得到了直观验证：autoguidance 消除了无引导扩散产生的离群点，同时完整保留了分布的所有分支；相比之下，CFG（Figure 1c）虽然也消除了离群点，但过度强调类别特征，导致整个分支被丢弃。

### 退化兼容性：关键约束

Autoguidance 有效的前提是 D₁ 和 D₀ 必须受到**相同类型**的退化。论文通过对照实验验证了这一约束：当 D₁ 使用 5% dropout 而 D₀ 使用 10% dropout（同类型退化）时，autoguidance 在 $w=2.25$ 时可将 FID 恢复至 2.55（接近基线 2.56）；但当 D₁ 使用 dropout 退化而 D₀ 使用输入噪声退化（不匹配退化）时，autoguidance 完全无效，最佳 FID 出现在 $w=1$（即不使用引导）。这表明引导模型必须与主模型“同病相怜”——容量不足和训练不充分正是实践中被验证有效的兼容退化方式。

### 与 CFG 的混合使用

Autoguidance 可以与 CFG 结合使用，以同时获得质量提升和类别对齐增强。推广后的多模型引导公式为：

$$D_w(\mathbf{x};\sigma,\mathbf{c}) := D_{\mathrm{m}}(\mathbf{x};\sigma,\mathbf{c}) + \sum_{i\in\{\mathrm{u},\mathrm{c}\}} (w_i - 1) \big( D_{\mathrm{m}}(\mathbf{x};\sigma,\mathbf{c}) - D_i(\mathbf{x};\sigma,\mathbf{c}) \big)$$

其中 $D_{\mathrm{m}}$ 是主模型，$D_{\mathrm{c}}$ 和 $D_{\mathrm{u}}$ 分别是条件和无条件引导模型，$w_i$ 为各自的引导权重。这为灵活调节图像质量与文本/类别对齐提供了统一的框架。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_bg6fVPVs3s/figures/002_Figure_1.jpg]]
*Figure 1: A fractal-like 2D distribution with two classes indicated with gray and orange regions. Approximately 99% of the probability mass is inside the shown contours. (a) Ground truth samples drawn directly from the orange class distribution. (b) Conditional sampling using a small denoising diffusion model generates outliers. (c) Classifier-free guidance*

### 问题背景：扩散模型的基础框架

Autoguidance 建立在连续时间扩散模型的概率流 ODE 框架之上。设数据分布为 $p_{\mathrm{data}}$，加噪过程定义为 $\mathbf{x}_\sigma = \mathbf{y} + \mathbf{n}$，其中 $\mathbf{y} \sim p_{\mathrm{data}}$，$\mathbf{n} \sim \mathcal{N}(\mathbf{0}, \sigma^2\mathbf{I})$。反向去噪过程由以下概率流 ODE 描述：

$$\mathrm{d}\mathbf{x}_\sigma = -\sigma \nabla_{\mathbf{x}_\sigma} \log p(\mathbf{x}_\sigma; \sigma) \mathrm{d}\sigma$$

其中 $\nabla_{\mathbf{x}_\sigma} \log p(\mathbf{x}_\sigma; \sigma)$ 是 score function，在给定噪声水平 $\sigma$ 下指向数据密度增长最快的方向。实际中，score function 通过去噪网络 $D_\theta$ 来参数化，训练目标为最小化去噪误差：

$$\theta = \arg\min_\theta \mathbb{E}_{\mathbf{y}\sim p_{\mathrm{data}}, \sigma\sim p_{\mathrm{train}}, \mathbf{n}\sim\mathcal{N}(\mathbf{0},\sigma^2\mathbf{I})} \|D_\theta(\mathbf{y}+\mathbf{n};\sigma) - \mathbf{y}\|_2^2$$

### 核心模块一：引导外推机制

Autoguidance 的核心操作是将两个去噪网络的输出进行线性外推。设 $D_1$ 为高质量主模型，$D_0$ 为质量较差的引导模型（容量更小或训练更少），两者接受完全相同的条件输入 $\mathbf{c}$。引导后的去噪输出定义为：

$$D_w(\mathbf{x};\sigma,\mathbf{c}) = w D_1(\mathbf{x};\sigma,\mathbf{c}) + (1-w) D_0(\mathbf{x};\sigma,\mathbf{c})$$

其中 $w > 1$ 为引导权重。当 $w=1$ 时，退化为仅使用主模型 $D_1$ 的无引导生成；$w$ 越大，对主模型与引导模型差异的放大程度越强。

**变量含义**：
- $\mathbf{x}$：当前噪声样本
- $\sigma$：当前噪声水平
- $\mathbf{c}$：条件信息（如类别标签或文本嵌入）
- $D_1$：高质量主去噪网络
- $D_0$：低质量引导去噪网络（与 $D_1$ 任务相同、条件相同、数据分布相同，但存在容量不足或训练不充分的退化）
- $w$：引导权重，控制外推强度

### 核心模块二：引导模型的退化构造

引导模型 $D_0$ 的构造是 autoguidance 有效性的关键。论文采用两种退化方式的组合：

1. **容量退化**：使用更小的模型架构。例如，当主模型为 EDM2-S 时，引导模型使用 XS 容量。
2. **训练时间退化**：引导模型仅接受主模型训练迭代数的一小部分。例如，在 ImageNet-512 上，引导模型仅训练主模型 $1/16$ 的迭代次数（记为 T/16）。

消融实验表明，两种退化方式的效果存在差异：
- **仅减少训练时间**（保持相同容量）：FID 从 2.56 降至 1.51，贡献了大部分收益。
- **仅减少容量**（训练充足）：FID 仅改善至 2.13，容量退化是次要但有益的补充。

### 核心模块三：独立 EMA 长度

主模型和引导模型使用独立的指数移动平均（EMA）长度是进一步提升性能的关键设计。消融实验表明，允许两个模型使用各自最优的 EMA 长度，将 FID 从 1.53 进一步降低到 1.34。这表明引导模型的最优平滑程度与主模型不同，独立调优可以更精确地控制引导信号的特性。

### 核心公式推导：引导的密度解释

将引导后的去噪输出代入 score function 的关系 $D(\mathbf{x};\sigma) \approx \mathbf{x} + \sigma^2 \nabla_{\mathbf{x}} \log p(\mathbf{x};\sigma)$，可以得到 autoguidance 隐含的采样密度：

$$D_w(\mathbf{x};\sigma,\mathbf{c}) \approx \mathbf{x} + \sigma^2 \nabla_{\mathbf{x}} \log \left( p_0(\mathbf{x}|\mathbf{c};\sigma) \left[ \frac{p_1(\mathbf{x}|\mathbf{c};\sigma)}{p_0(\mathbf{x}|\mathbf{c};\sigma)} \right]^w \right)$$

这表明 autoguidance 等价于从一个重新加权的密度中采样，其中 $p_1$ 和 $p_0$ 分别是主模型和引导模型隐含的密度估计。对应的 score function 可分解为：

$$\nabla_{\mathbf{x}} \log p_w(\mathbf{x}|\mathbf{c};\sigma) = \nabla_{\mathbf{x}} \log p_1(\mathbf{x}|\mathbf{c};\sigma) + (w-1) \nabla_{\mathbf{x}} \log \frac{p_1(\mathbf{x}|\mathbf{c};\sigma)}{p_0(\mathbf{x}|\mathbf{c};\sigma)}$$

**公式含义**：
- 第一项 $\nabla_{\mathbf{x}} \log p_1$ 是主模型的标准条件 score，负责将样本推向数据流形。
- 第二项 $(w-1) \nabla_{\mathbf{x}} \log (p_1/p_0)$ 是**引导力**，其方向指向 $p_1$ 与 $p_0$ 密度比值增大的方向。

**引导力的物理意义**：当主模型 $D_1$ 与引导模型 $D_0$ 的预测一致时，$p_1/p_0 \approx 1$，梯度接近零，引导力微弱，样本不受显著扰动。当两模型预测存在显著差异时（通常发生在数据稀疏的低概率区域，引导模型因退化而拟合更差），$p_1/p_0$ 的梯度产生一个将样本拉回高概率核心区域的力。这解释了 autoguidance 消除离群样本同时保留分布多样性的机理——它只在模型不确定的区域施加纠正力，而非像 CFG 那样系统性地偏向某个条件。

### 与 CFG 的公式对比

CFG 的引导外推形式与 autoguidance 相同，但 $D_0$ 是无条件模型（接受空条件 $\varnothing$）。CFG 的引导力为 $(w-1) \nabla_{\mathbf{x}} \log p(\mathbf{c}|\mathbf{x};\sigma)$（由贝叶斯规则导出），其方向指向提升条件 $\mathbf{c}$ 与样本 $\mathbf{x}$ 对齐程度的方向。这同时提升了图像质量和条件对齐度，但代价是丢弃了数据分布中与条件关联较弱的模式（如 Figure 1c 中整个分支的消失）。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_bg6fVPVs3s/figures/003_Figure_2.jpg]]
*Figure 2: Closeup of the region highlighted in Figure 1c. (a) The implied learned density*

Autoguidance 通过保持 $D_0$ 的条件与 $D_1$ 完全一致，将引导力的方向从“条件对齐”切换为“质量提升”，从而实现了质量与多样性的解耦控制。

### 多模型引导的推广形式

论文在附录中给出了将 autoguidance 与 CFG 结合的通用公式。设 $D_{\mathrm{m}}$ 为主条件模型，$D_{\mathrm{u}}$ 为无条件引导模型（用于 CFG），$D_{\mathrm{c}}$ 为较差的条件引导模型（用于 autoguidance），则组合引导的去噪输出为：

$$D_w(\mathbf{x};\sigma,\mathbf{c}) := D_{\mathrm{m}}(\mathbf{x};\sigma,\mathbf{c}) + \sum_{i\in\{\mathrm{u},\mathrm{c}\}} (w_i - 1) \big( D_{\mathrm{m}}(\mathbf{x};\sigma,\mathbf{c}) - D_i(\mathbf{x};\sigma,\mathbf{c}) \big)$$

其中 $w_{\mathrm{u}}$ 和 $w_{\mathrm{c}}$ 分别控制 CFG 和 autoguidance 的引导强度。该公式允许在单个采样过程中同时利用两种引导机制的优势。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_bg6fVPVs3s/figures/011_Figure_9.jpg]]
*Figure 9: Progression of implied learned densities during sampling over various σ in a setup similar to Figure 2. Contours of the corresponding ground truth distributions are also shown. (a) Main model density*

## 实验与关键发现

### 核心实验结果

Autoguidance 在 ImageNet-512 和 ImageNet-64 两个标准基准上均取得了显著的性能提升，刷新了公开模型的最佳 FID 记录。Table 1 汇总了主要定量结果。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_bg6fVPVs3s/figures/004_Table_1.jpg]]
*Table 1: Results on ImageNet-512 and ImageNet-64. The parameters of autoguidance refer to the capacity and amount training received by the guiding model. The latter is given relative to the number of training images shown to the main model (T ). The columns*

在 **ImageNet-512** 上，以 EDM2-S 作为主模型时，autoguidance 将 FID 从无引导的 2.56 大幅降至 **1.34**，降幅达 1.22；FDDINOv2 则从 68.64 降至 **36.67**，降幅近 32 个点。当主模型升级为更大容量的 EDM2-XXL 时，FID 进一步降至 **1.25**，创造了该分辨率下的新纪录。在无条件生成设置下，autoguidance 同样表现优异：EDM2-S 的 FID 从 11.67 降至 **3.86**，降幅高达 7.81，表明该方法对图像质量的提升独立于条件信息。

在 **ImageNet-64** 上，EDM2-S 配合 autoguidance 将 FID 从 1.58 降至 **1.01**，同样刷新了该分辨率的记录。

这些结果表明，autoguidance 在不同模型容量和分辨率下均能稳定地、大幅度地提升生成质量，且收益远超 CFG 等现有方法。

### 消融实验：引导模型的退化方式

Autoguidance 的核心设计在于引导模型的退化方式。消融实验揭示了不同退化策略的贡献权重：

- **仅减少训练时间**（保持引导模型容量与主模型相同）：FID 可降至 1.51。这表明大部分性能增益来源于训练不充分带来的模型质量差距。
- **仅减少容量**（保持引导模型训练充足）：FID 仅改善至 2.13。容量退化带来的增益相对有限，但仍有正面作用。
- **同时减少容量与训练时间**：即完整方案，FID 达到最优的 1.34。

这一消融表明，**训练不足是 autoguidance 有效性的主要驱动力**，容量缩减作为辅助手段可进一步扩大模型间的质量差距，从而增强引导信号。

### 退化兼容性的关键发现

Autoguidance 对退化类型具有严格的兼容性要求。当主模型和引导模型受到**不同类型**的退化时，方法完全失效：

- 若主模型使用 5% dropout 训练、引导模型使用 10% dropout 训练（**相同退化类型**），autoguidance 在 w=2.25 时可恢复至与无引导主模型相当的 FID（2.55 vs 2.56）。
- 若主模型使用 5% dropout 训练、引导模型使用 20% 输入噪声训练（**不匹配的退化类型**），则最佳 FID 出现在 w=1 时——即引导完全无效，任何外推都会损害质量。

这一发现揭示了 autoguidance 的本质机制：**引导信号来源于两个模型在相同任务上的系统性预测差异，而非任意形式的模型差异**。只有当引导模型的误差模式与主模型一致、仅程度更严重时，两者预测之差才能有效指示主模型的欠拟合区域。

### 超参数灵敏度分析

Figure 3 系统扫描了 autoguidance 的关键超参数（基于 EDM2-S，ImageNet-512）：

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_bg6fVPVs3s/figures/005_Figure_3.jpg]]
*Figure 3: Sensitivity w.r.t. autoguidance parameters, using EDM2-S on ImageNet-512. The shaded regions indicate the min/max FID over 3 evaluations. (a) Sweep over guidance weight w while keeping all other parameters unchanged. The curves correspond to how much the guiding model was trained relative to the number of images shown to the main model. (b) Sweep over guidance weight for different guiding model capacities. (c) Sweep over the two EMA length parameters for our best configuration, denoted with ⋆ in (a) and (b)*

- **引导权重 w**：存在明显的最优区间。w 过小则引导不足，过大则导致过饱和失真。最优 w 值与引导模型的退化程度相关——退化越严重，最优 w 值通常越小。
- **引导模型容量**：从 S 降至 XS 可获得最佳 FID；进一步降至 XXS 仍然有效，但对 w 的敏感度增加，最优区间变窄。
- **独立 EMA 长度**：允许主模型和引导模型使用各自最优的 EMA 衰减长度，可将 FID 从 1.53 进一步降至 1.34。这表明两个模型在训练动态上的差异需要被独立对待，共享 EMA 参数会限制引导信号的精确性。

### 定性分析：多样性保持

与 CFG 相比，autoguidance 最显著的优势在于**保持生成多样性**。

在 2D 玩具示例（Figure 1）中，CFG 虽然消除了离群点，但完全丢弃了分布中的某些分支（如某一类别），导致模式坍缩。而 autoguidance 在消除离群点的同时，保留了分布的所有分支，样本被均匀地拉向各自分支的高概率核心区域。

在 ImageNet-512 的实际生成中（Figure 4、Figure 8），CFG 在高引导权重下趋向于产生模板化的输出——同一类别的不同样本之间变化极小。而 autoguidance 即使在较高引导权重下，仍能保持丰富的类内变化。例如在“树蛙”类别中，CFG 生成的样本姿态和背景高度相似，而 autoguidance 则保留了多样的姿态、光照和构图。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_bg6fVPVs3s/figures/006_Figure_4.jpg]]
*Figure 4: Example results for the Tree frog, Palace, Mushroom, Castle classes of ImageNet-512 using EDM2-S. Guidance weight increases to the right; rows are classifier-free guidance and our method*

### 与 CFG 的混合使用

Autoguidance 与 CFG 可以协同工作。在 DeepFloyd IF 文本到图像模型上的实验（Figure 5）表明，两种引导可以按不同权重混合：CFG 主要提升文本对齐度，autoguidance 主要提升图像质量。混合使用可在保持文本一致性的同时，进一步增强视觉质量。多模型引导的推广公式见附录 B.2。

### 方法的局限性

尽管 autoguidance 在实验中表现优异，但仍存在以下局限：

1. **额外训练成本**：需要单独训练一个引导模型。尽管通过缩小容量和减少训练可大幅降低成本（例如本文中仅增加约 11% 的训练开销），但对于资源受限的场景仍是一笔额外投入。
2. **退化兼容性约束**：引导模型必须与主模型受到同类型的退化。若退化类型不匹配，方法完全无效。这限制了引导模型获取方式的灵活性。
3. **超参数需手动调优**：引导权重 w、独立 EMA 长度等参数目前需要通过网格搜索确定，缺乏自动选择机制。
4. **验证范围有限**：目前仅在 EDM2 架构和 DeepFloyd IF 上进行了验证，尚未在其他扩散模型架构或更大规模的文本到图像系统上进行广泛测试。
5. **理论分析不足**：对 autoguidance 有效性的解释依赖于隐式假设和直观分析，缺乏严格的数学证明。

## 定位与知识库关联

### 与 Classifier-Free Guidance 的关系

Autoguidance 的核心动机直接源于对 **Classifier-Free Guidance (CFG)**（Ho & Salimans, NeurIPS 2022）机制的解剖与再设计。CFG 通过外推条件模型与无条件模型的分数差来同时提升图像质量和条件对齐度，但这两种效应不可解耦——无条件模型因缺乏类别信息而天然对数据分布拟合更差，导致引导力将样本拉向类条件密度的高似然比区域，从而在提升质量的同时系统性丢弃分布的低概率分支（如图 1c 所示，CFG 在 2D 玩具示例中完全抹除了整个分布分支）。

Autoguidance 的改进逻辑是**将引导信号的来源从“任务不同的模型”替换为“任务相同但质量更差的模型”**。具体而言，CFG 的引导力来源于 $\nabla_{\mathbf{x}} \log \frac{p_1(\mathbf{x}|\mathbf{c};\sigma)}{p_0(\mathbf{x}|\mathbf{c};\sigma)}$，其中 $p_0$ 是无条件密度；而 autoguidance 将 $p_0$ 替换为较差条件模型的隐含密度，使得引导力仅响应模型间的质量差异，而非任务差异。这一替换消除了 CFG 中固有的“任务差异问题”（task discrepancy problem），使引导效应专注于将样本从欠拟合的低概率区域拉回数据流形的核心，而不会系统性偏向某一类别或模式。

在实现层面，两者共享相同的外推公式 $D_w = w D_1 + (1-w) D_0$（$w>1$），但 $D_0$ 的含义发生了根本变化。CFG 的 $D_0$ 是无条件去噪器（通常通过随机丢弃类别标签实现），而 autoguidance 的 $D_0$ 是保持相同条件输入但容量更小和/或训练更少的模型。

### 与其他引导/截断方法的区别

**朴素截断（Naive truncation）** 通过均匀放大所有分数向量的模长（即 $w>1$ 时直接缩放分数）来提升图像质量。论文的 2D 实验（图 1d）表明，这种各向同性的放大虽然能消除离群点，但会过度压缩分布的支撑集，导致多样性丧失。Autoguidance 与朴素截断的本质区别在于：引导力是**各向异性的**——它仅在两个模型预测不一致的区域（即主模型欠拟合的区域）施加显著修正，而在模型共识区域几乎不产生扰动。

**Guidance Interval**（Kynkäänniemi et al., 2024）是 CFG 的变体，通过将引导限制在特定噪声水平区间来缓解 CFG 的过饱和问题。该方法仍沿用无条件模型作为引导源，因此无法根本解决任务差异问题。Autoguidance 与之正交——前者控制引导的**作用时机**，后者改变引导的**信号来源**。

### 适用边界与退化兼容性条件

Autoguidance 有效性的一个关键约束是**退化兼容性**：主模型 $D_1$ 和引导模型 $D_0$ 必须受到**相同类型**的退化。论文通过对照实验严格验证了这一点：

- 当 $D_1$ 使用 5% dropout、$D_0$ 使用 10% dropout 时，autoguidance 在 $w=2.25$ 处将 FID 恢复至 2.55（基模型为 2.56），完全有效。
- 当 $D_1$ 使用 +10% 输入噪声、$D_0$ 使用 +20% 输入噪声时，autoguidance 在 $w=2.00$ 处将 FID 恢复至 2.56，同样有效。
- 但当 $D_1$ 的退化来自 dropout、$D_0$ 的退化来自输入噪声时，autoguidance 完全失效，最佳 FID 出现在 $w=1$（即不使用引导）。

这一发现揭示了 autoguidance 的深层机制：引导力来源于两个模型在**相同特征空间中的系统性预测偏差**。当退化类型不匹配时，模型间的差异反映的是不同性质的误差，外推这些差异无法产生指向数据流形核心的有意义梯度。

### 训练开销与实用性定位

Autoguidance 需要额外训练一个引导模型，这引入了计算开销。但论文通过两种退化策略将额外成本控制在较低水平：

- **减少训练时间**：引导模型仅训练主模型 $1/16$ 的迭代次数（记为 T/16），这是收益的主要来源——仅此一项就将 FID 从 2.56 降至 1.51。
- **减少模型容量**：使用更小的模型配置（如从 S 降至 XS），这是次要但有益的补充——仅减少容量只能改善 FID 至 2.13。

综合使用 XS 容量和 T/16 训练时，额外训练开销约为主模型的 11%。考虑到 FID 从 2.56 降至 1.34 的显著收益，这一开销在追求极致生成质量的场景中是可接受的。此外，引导模型可在训练主模型时同步从早期检查点获取，无需独立的完整训练流程。

### 局限与开放问题

**当前局限**：

1. **退化类型依赖**：引导模型必须与主模型共享相同的退化模式，这限制了退化策略的设计空间。目前验证的有效退化仅包括容量缩减、训练不足、dropout 增强和输入噪声增强，其他退化方式（如剪枝、量化）的有效性尚未验证。

2. **超参数敏感性**：引导权重 $w$、引导模型的独立 EMA 长度等超参数需要针对具体设置进行网格搜索。论文的消融实验（图 3c）表明，允许主模型和引导模型使用独立的 EMA 长度将 FID 从 1.53 进一步降至 1.34，但最优配置依赖于模型组合。

3. **架构验证范围有限**：所有主要实验基于 EDM2（Karras et al., 2024）框架，仅在 DeepFloyd IF 上进行了文本条件生成的定性验证。尚未在其他扩散架构（如 DiT、MDT）或更大规模的文本到图像系统上进行系统验证。

4. **理论不完备**：论文对 autoguidance 有效性的解释依赖于“较差模型在低概率区域欠拟合”的直觉和 2D 可视化证据，缺乏对引导力场性质的严格数学刻画，也未能给出最优退化程度的理论指导。

**开放问题**：

- 能否从理论上证明 autoguidance 带来益处的充要条件，特别是退化兼容性的严格数学定义？
- 如何自动选择最佳的引导模型容量和训练量，以避免繁琐的网格搜索？是否存在与模型规模、数据复杂度相关的缩放律？
- 退化的“兼容性”能否被更精确地度量和预测？是否存在一个退化空间中的距离度量，使得兼容退化之间的距离小于不兼容退化？
- autoguidance 的引导思想能否推广到其他生成范式（如 GAN、VAE、flow-based models）？在这些框架中，“较差版本”应如何定义？
- 除了降低容量和训练时间，是否还有其他更有效的退化方式（如结构化剪枝、权重量化、知识蒸馏的中间产物）？
- 能否设计一种**无需训练额外模型的自引导方法**，例如通过在推理时注入噪声、腐蚀权重或使用早期去噪步的预测作为引导信号？

## 原文 PDF

![[paperPDFs/NeurIPS_2024/Guiding_a_Diffusion_Model_with_a_Bad_Version_of_Itself.pdf]]
