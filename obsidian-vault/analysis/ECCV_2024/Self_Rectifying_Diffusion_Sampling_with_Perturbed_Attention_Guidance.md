---
title: Self-Rectifying Diffusion Sampling with Perturbed-Attention Guidance
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/Self_Rectifying_Diffusion_Sampling_with_Perturbed_Attention_Guidance.pdf
aliases:
- PAGP
- SRDSPAG
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将扩散 U-Net 中选定自注意力图（Softmax(QK^T/sqrt(d))）替换为单位矩阵 I，破坏全局结构信息而保留局部外观，从而产生结构退化的“不良”样本作为引导负例。
primary_logic: 通过仅扰动自注意力的结构部分，生成结构退化但外观保留的样本，充当隐式判别器的负例，引导去噪过程远离结构崩塌方向，无需额外训练或外部模型。
claims:
- PAG 通过将扩散 U-Net 中选定的自注意力图替换为单位矩阵来生成退化样本。
- PAG 引导去噪过程远离这些退化样本，逐步改善样本结构。
- PAG 无需额外训练或外部模块即可工作。
- 扰动自注意力避免了直接扰动输入图像或条件导致的分布外（OOD）问题，修改注意力图对模型输出影响轻微。
---

# Self-Rectifying Diffusion Sampling with Perturbed-Attention Guidance

> [!tip] 核心洞察
> 通过仅扰动自注意力的结构部分，生成结构退化但外观保留的样本，充当隐式判别器的负例，引导去噪过程远离结构崩塌方向，无需额外训练或外部模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于扰动注意力引导的自校正扩散采样 |
| 英文题名 | Self-Rectifying Diffusion Sampling with Perturbed-Attention Guidance |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2403.17377) · [Project](https://ku-cvlab.github.io/Perturbed-Attention-Guidance) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Perturbed-Attention Guidance (PAG) |
| Dataset | ImageNet 256x256 unconditional generation, ImageNet 256x256 conditional generation, Stable Diffusion v1.5 unconditional generation, Stable Diffusion v1.5 text-to-image |

> [!tip] 效果简介
> - ImageNet 256x256 unconditional generation (ADM) 上，FID↓ 16.23 vs 26.21 (No guidance) (-9.98)。
> - ImageNet 256x256 conditional generation (ADM) 上，FID↓ 6.32 vs 10.94 (No guidance) (-4.62)。
> - Stable Diffusion v1.5 unconditional generation 上，FID↓ 47.57 vs 53.13 (No guidance) (-5.56)。

## 概述

扩散模型在无条件生成或缺乏外部条件（如类别标签、文本提示）时，去噪过程容易产生结构崩塌的样本，导致生成质量严重下降。主流的分类器无引导（Classifier‑Free Guidance, CFG）虽然能有效缓解这一问题，但其本质依赖于联合训练的条件/无条件模型对，在纯无条件场景中无法使用，且需要额外的训练开销。因此，**如何在无需外部条件、无需额外训练的前提下，为扩散模型提供有效的结构引导，成为该领域的一个关键瓶颈**。

本文提出 **扰动注意力引导（Perturbed‑Attention Guidance, PAG）**，以一种即插即用的方式解决上述问题。其核心洞察是：扩散 U‑Net 中的自注意力图 $A_t = \mathrm{Softmax}(Q_t K_t^T / \sqrt{d})$ 编码了图像块之间的全局结构关系，而值矩阵 $V_t$ 保留了局部外观信息。通过将选定层的自注意力图替换为单位矩阵 $I$，可以生成结构退化但外观保留的“不良”样本，这些样本充当隐式判别器的负例，引导去噪过程远离结构崩塌的方向。

PAG 的引导公式为：

$$\tilde{\epsilon}_{\theta}(x_t) = \epsilon_{\theta}(x_t) + s(\epsilon_{\theta}(x_t) - \hat{\epsilon}_{\theta}(x_t))$$

其中 $\epsilon_{\theta}(x_t)$ 为原始噪声预测，$\hat{\epsilon}_{\theta}(x_t)$ 为扰动自注意力后的噪声预测，$s$ 为引导尺度。该方法无需额外训练、无需外部模型，仅通过修改推理时的自注意力计算即可实现。

**主要结果**：在 ImageNet 256×256 无条件生成任务上，PAG 将 ADM 的 FID 从 26.21 降至 16.23（↓9.98）；在 Stable Diffusion v1.5 无条件生成中，FID 从 53.13 降至 47.57（↓5.56）。在条件生成场景中，PAG 可与 CFG 叠加使用，在 MS‑COCO 文本到图像任务上将 FID 从 15.00 进一步降至 10.08（↓4.92）。在下游逆问题（inpainting、deblurring）中，PAG 同样带来显著增益，例如在 FFHQ 的运动去模糊任务上，PSLD+PAG 的 FID 从 93.39 降至 40.26（↓53.13）。消融实验证实，以单位矩阵替换自注意力图的扰动策略在所有备选方案中效果最优，且在 U‑Net 较深层施加扰动效果更好。

**方法定位**：PAG 属于扩散模型推理时引导方法，与 CFG 形成互补——CFG 利用条件信息在早期阶段提供粗粒度引导，而 PAG 在中后期持续提供细粒度结构修正。与早期的自注意力引导（SAG）相比，PAG 对引导尺度不敏感，即使在高尺度下仍能保持物体形状和细节，不产生明显伪影。

## 背景与动机

### 扩散模型的生成瓶颈

扩散模型通过逐步去噪将随机噪声转化为高保真图像，已成为生成建模的主流范式。其训练目标为最小化噪声预测误差：

$$\mathcal { L } = \mathbb { E } _ { x _ { 0 } , t , \epsilon \sim \mathcal { N } ( 0 , I ) } \left[ \left\| \epsilon - \epsilon _ { \theta } ( x _ { t } , t ) \right\| _ { 2 } ^ { 2 } \right]$$

然而，当扩散模型在无条件生成或缺乏外部条件（如类别标签、文本提示）时，容易产生**结构崩塌**的样本——语义结构混乱、关键特征缺失（如面部五官残缺），严重制约了其在无监督场景中的实用性。

### 现有引导技术的局限

为解决结构崩塌问题，**Classifier-Free Guidance (CFG)** 通过在去噪过程中外推条件预测与无条件预测的差异来强化条件特征：

$$\tilde { \epsilon } _ { \theta } ( x _ { t } , c ) = ( 1 + s ) \epsilon _ { \theta } ( x _ { t } , c ) - s \epsilon _ { \theta } ( x _ { t } )$$

CFG 的核心机制在于：无条件模型作为“不良路径”，其预测与条件预测的差异 $\Delta_t = \epsilon_\theta(x_t, c) - \epsilon_\theta(x_t, \phi)$ 放大了与提示相关的特征，使生成样本与条件对齐（Fig. 2）。但 CFG 存在两个根本性限制：

1. **依赖条件与联合训练**：CFG 需要同时具备条件模型和无条件模型，且两者必须联合训练。若使用分别训练的条件和无条件模型直接组合，生成质量会显著下降（Fig. 41），说明其效果并非简单的分数外推，而是依赖于训练过程中的隐式协同。
2. **无条件场景不可用**：在无文本提示的 ControlNet 生成、无条件图像合成、逆问题求解（如修复、去模糊）等场景中，CFG 无法发挥作用，模型完全失去结构引导。

早期的无条件引导尝试如 **Self-Attention Guidance (SAG)** 通过对输入图像施加对抗性模糊来构造“不良”样本，但直接扰动输入会导致分布外（OOD）问题，且在高引导尺度下产生明显伪影和过平滑（Fig. 46）。

### 核心动机

本文的核心动机在于：**能否在不依赖外部条件、不引入额外训练或外部模块的前提下，为扩散模型提供一种通用的结构引导机制？** 这需要构造一个“不良”生成路径，使其在结构上退化但仍保持在模型的知识分布内，从而作为隐式判别器的负例，引导去噪过程远离结构崩塌方向。

## 核心创新

PAG 的核心创新在于**将扩散模型中的自注意力机制重新解释为一种隐式判别器的负例生成源**，从而在完全无需额外训练、无需外部条件或模型的前提下，为扩散采样提供结构引导。

### 关键改动：从标准自注意力到扰动自注意力

标准扩散 U-Net 中的自注意力模块可分解为结构分量与外观分量：

$$ \mathrm{SA}(Q_t, K_t, V_t) = \mathrm{Softmax}\left(\frac{Q_t K_t^T}{\sqrt{d}}\right) V_t = \mathbf{A}_t V_t $$

其中 $\mathbf{A}_t = \mathrm{Softmax}(Q_t K_t^T / \sqrt{d})$ 编码了图像块之间的**全局结构关系**，而 $V_t$ 保留了**局部外观信息**。PAG 的改动极为简洁——仅将选定的自注意力图替换为单位矩阵 $\mathbf{I}$：

$$ \mathrm{PSA}(Q_t, K_t, V_t) = \mathbf{I} V_t = V_t $$

这一操作（称为 Perturbed Self-Attention, PSA）**消除了 Query-Key 交互所承载的结构信息**，同时完整保留了 Value 中的外观信息。由此产生的噪声预测 $\hat{\epsilon}_\theta(x_t)$ 对应着一个“结构退化但外观合理”的不良样本，充当隐式判别器的负例。

### 引导机制：线性外推远离结构崩塌

获得扰动预测后，PAG 通过线性组合原始预测与扰动预测形成最终引导信号：

$$ \tilde{\epsilon}_{\theta}(x_t) = \epsilon_{\theta}(x_t) + s \big( \epsilon_{\theta}(x_t) - \hat{\epsilon}_{\theta}(x_t) \big) $$

其中 $s$ 为引导尺度。这一公式的实质是**将去噪方向推离结构退化的方向**：差值 $\epsilon_{\theta}(x_t) - \hat{\epsilon}_{\theta}(x_t)$ 捕获了“良好结构”与“崩塌结构”之间的差异，沿此方向外推即可强化样本的语义连贯性。该机制与 Classifier-Free Guidance (CFG) 在形式上同构（CFG 使用无条件预测作为负例），但**PAG 的负例完全由扰动自注意力在线生成，不依赖联合训练的无条件模型**。

### 与 CFG 的本质区别

CFG 依赖条件信号（如类别标签、文本提示）来区分“有条件”与“无条件”预测，因此在无条件生成场景中**无法使用**。PAG 则通过自注意力的结构扰动来模拟“不良”样本，使得引导信号**仅依赖于模型内部的结构感知能力**，无需任何外部条件。这一差异使得 PAG 成为首个可在无条件生成、ControlNet 空提示、逆问题求解等广泛下游任务中即插即用的通用引导方法。

### 为什么扰动自注意力而非其他组件？

文中验证了多种扰动策略的替代方案（见消融实验），结果表明：
- **扰动输入图像或条件**会导致分布外（OOD）问题，使模型输出严重失真；
- **扰动外观分量**（如将 $V_t$ 替换为空间均值）或**完全跳过自注意力**的效果均显著弱于结构扰动；
- **仅替换自注意力图为 $\mathbf{I}$** 对模型输出影响轻微（因为自注意力通常以残差方式学习），却能精确剥离结构信息，生成理想的负例。

这一设计的精妙之处在于：它利用了扩散 U-Net 中自注意力的**结构-外观解耦特性**，以最小侵入性的方式构建了一个隐式判别器，实现了“自校正”的扩散采样。

## 整体框架

PAG 的整体采样框架建立在标准扩散去噪过程之上，通过引入一条“结构退化”的辅助路径来构造隐式引导信号，其核心由三个模块串联构成。

**1. 预训练扩散 U‑Net（基础去噪网络）**  
框架直接复用预训练的扩散 U‑Net，无需任何额外训练或外部模块。该网络同时承担两项职责：在每一去噪步 $t$，对当前噪声潜在变量 $x_t$ 执行一次标准前向传播，产生原始噪声预测 $\epsilon_{\theta}(x_t)$；随后，在选定的自注意力层中替换注意力图，再次前向传播产生扰动噪声预测 $\hat{\epsilon}_{\theta}(x_t)$（见 Alg. 1）。两次前向传播共享同一网络权重，仅在自注意力计算路径上存在差异。

**2. 扰动自注意力模块（PSA，Perturbed Self-Attention）**  
这是 PAG 区别于其他引导方法的关键模块。标准自注意力计算为：
$$
\mathrm{SA}(Q_t, K_t, V_t) = \mathrm{Softmax}\!\left(\frac{Q_t K_t^T}{\sqrt{d}}\right) V_t = \mathbf{A}_t V_t
$$
其中 Softmax 项 $\mathbf{A}_t$ 编码了图像块之间的全局结构关系，而 $V_t$ 承载局部外观信息。PSA 将选定的自注意力图 $\mathbf{A}_t$ 替换为单位矩阵 $\mathbf{I}$：
$$
\mathrm{PSA}(Q_t, K_t, V_t) = \mathbf{I} V_t = V_t
$$
这一操作仅破坏结构信息，完整保留外观信息，从而生成结构退化但外观合理的“不良”样本。消融实验证实，单位矩阵替换（FID 32.34）显著优于随机 mask（40.20）、非对角线 mask（39.49）和加性噪声（62.83），验证了仅移除结构信息的优越性（Fig. 36, Table 9）。作者指出，扰动策略不限于 PSA，可在通用扰动引导框架内替换为其他方案（Sec. 4.2），但当前工作仅探索了单位矩阵替换这一种形式。

**3. 线性组合引导模块**  
将原始预测与扰动预测按下式线性组合，得到最终用于去噪的噪声估计：
$$
\tilde{\epsilon}_{\theta}(x_t) = \epsilon_{\theta}(x_t) + s\big(\epsilon_{\theta}(x_t) - \hat{\epsilon}_{\theta}(x_t)\big)
$$
其中 $s$ 为引导尺度，控制远离退化方向的程度。该组合随后被送入标准 DDIM 采样步骤以更新 $x_{t-1}$。在条件生成场景中，PAG 可与 CFG 联合使用：
$$
\tilde{\epsilon}_{\theta}(x_t, c) = \epsilon_{\theta}(x_t, c) + w\big(\epsilon_{\theta}(x_t, c) - \epsilon_{\theta}(x_t, \phi)\big) + s\big(\epsilon_{\theta}(x_t, c) - \hat{\epsilon}_{\theta}(x_t, c)\big)
$$
其中 $w$ 为 CFG 尺度，$c$ 为条件，$\phi$ 为空条件（Eq. 14, Appendix A.2）。

**输入输出流**  
- **输入**：当前时间步 $t$ 的噪声潜在变量 $x_t$，以及可选的条件 $c$（如文本提示、类别标签）。  
- **处理**：  
  1. 标准前向传播 → $\epsilon_{\theta}(x_t)$（或 $\epsilon_{\theta}(x_t, c)$）；  
  2. 在 U‑Net 选定层中执行 PSA → 扰动前向传播 → $\hat{\epsilon}_{\theta}(x_t)$；  
  3. 线性组合 → $\tilde{\epsilon}_{\theta}(x_t)$。  
- **输出**：引导后的噪声预测 $\tilde{\epsilon}_{\theta}(x_t)$，用于 DDIM 采样更新 $x_{t-1}$，迭代直至 $t=0$ 得到最终图像 $x_0$。

**与 CFG 的概念对比**  
CFG 依赖联合训练的无条件模型作为“不良”路径，在无条件生成场景中无法使用；PAG 则通过扰动自注意力（单位矩阵）在推理时动态构造结构退化的负例路径，无需额外训练或外部条件，使其在无条件生成、ControlNet 空提示、逆问题求解等缺乏条件的场景中同样有效（Fig. 4）。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2403_17377/figures/004_Figure_4.jpg]]
*Figure 4: Conceptual comparison between CFG [18] and PAG. CFG [18] employs jointly trained unconditional model as the undesirable path, whereas PAG utilizes perturbed self-attention for the same purpose*

**计算开销**  
PAG 每步需两次前向传播，计算成本与 CFG 相近但高于无引导采样。文中指出可通过批量处理优化，但未报告实际推理延迟的直接对比（Table 6）。

## 核心模块与公式推导

### 方法总览

PAG 的核心思想是在扩散模型的去噪过程中，通过扰动 U-Net 内的自注意力图来生成结构退化但外观保留的“不良”样本，然后将原始噪声预测与扰动噪声预测线性组合，引导采样远离结构崩塌方向。该方法无需额外训练或外部模块，可直接应用于任意预训练扩散模型。

图 4 给出了 PAG 与 CFG 的概念对比：CFG 依赖联合训练的无条件模型作为不良路径，而 PAG 利用扰动自注意力达到同样目的。

### 关键模块

PAG 的完整采样流程由以下三个模块构成（见 Algorithm 1）：

1. **预训练扩散 U‑Net（含自注意力层）**  
   作为基础去噪网络，在每个时间步 $t$ 同时提供原始噪声预测 $\epsilon_{\theta}(x_t)$ 和扰动噪声预测 $\hat{\epsilon}_{\theta}(x_t)$。U‑Net 中的自注意力层是扰动操作的作用点。

2. **扰动自注意力模块（Perturbed Self-Attention, PSA）**  
   将 U‑Net 中选定层的自注意力图替换为单位矩阵 $\mathbf{I}$，从而消除 token 间的结构关系，仅保留各 token 自身的外观信息。该模块是生成“不良”样本的核心机制。

3. **线性组合引导模块**  
   将原始预测与扰动预测按下式组合得到最终噪声：
   $$
   \tilde{\epsilon}_{\theta}(x_t) = \epsilon_{\theta}(x_t) + s\big(\epsilon_{\theta}(x_t) - \hat{\epsilon}_{\theta}(x_t)\big)
   $$
   其中 $s$ 为引导尺度，控制远离退化样本的强度。该组合形式直接源于将采样引导解释为隐式判别器梯度的理论框架（第 4.1 节）。

### 核心公式推导

#### 3.1 标准自注意力与结构‑外观解耦

扩散 U‑Net 中的标准自注意力计算为：
$$
\mathrm{SA}(Q_t, K_t, V_t) = \mathrm{Softmax}\!\left(\frac{Q_t K_t^T}{\sqrt{d}}\right) V_t = \mathbf{A}_t V_t
\tag{Eq. 12}
$$
其中：
- $Q_t, K_t, V_t \in \mathbb{R}^{N \times d}$ 分别为查询、键、值矩阵，$N$ 为 token 数量，$d$ 为通道维度。
- $\mathbf{A}_t = \mathrm{Softmax}(Q_t K_t^T / \sqrt{d}) \in \mathbb{R}^{N \times N}$ 为注意力图，编码 token 之间的**结构关系**（哪些图像块应相互关注）。
- $V_t$ 为值矩阵，编码每个 token 的**外观信息**（纹理、颜色等局部特征）。

这一解耦是 PAG 设计的理论基础：结构信息集中在 $\mathbf{A}_t$ 中，外观信息集中在 $V_t$ 中。

#### 3.2 扰动自注意力（PSA）

PAG 通过将注意力图替换为单位矩阵来仅破坏结构信息：
$$
\mathrm{PSA}(Q_t, K_t, V_t) = \mathbf{I} \, V_t = V_t
\tag{Eq. 13}
$$
其中 $\mathbf{I} \in \mathbb{R}^{N \times N}$ 为单位矩阵。该操作的含义是：
- 每个 token 仅关注自身（对角线为 1），不再与其他 token 交互。
- 全局结构信息完全丧失，导致模型无法正确组织物体的空间布局和语义结构。
- 但每个 token 的外观信息（$V_t$）被完整保留，因此扰动后的输出仍处于模型的数据分布内，避免了直接扰动输入图像或条件导致的分布外（OOD）问题。

消融实验（Fig. 36, Table 9）验证了该策略的优越性：替换为单位矩阵的 FID 为 32.34，显著优于随机 mask（40.20）、非对角线 mask（39.49）和加性噪声（62.83）。

#### 3.3 引导信号的形成

基于第 4.1 节的隐式判别器框架，采样引导可视为梯度方向：
$$
\nabla_{x_t} \mathcal{L}_{\mathcal{G}} = -\nabla_{x_t}\big(\log p(x_t|y) - \log p(x_t|\hat{y})\big)
$$
其中 $y$ 表示“良好”样本，$\hat{y}$ 表示“不良”样本。在扩散模型中，该梯度可通过噪声预测的差值近似，从而得到引导采样公式（Eq. 10）：
$$
\tilde{\epsilon}_{\theta}(x_t) = \epsilon_{\theta}(x_t) + s\big(\epsilon_{\theta}(x_t) - \hat{\epsilon}_{\theta}(x_t)\big)
$$
其中：
- $\epsilon_{\theta}(x_t)$ 为原始 U‑Net 的噪声预测（对应“良好”方向）。
- $\hat{\epsilon}_{\theta}(x_t)$ 为经 PSA 扰动后的噪声预测（对应“不良”方向）。
- $s \ge 0$ 为引导尺度，控制修正强度。消融实验（Fig. 34, Fig. 35）表明 $s=1.0$ 时 FID 最优，$s=2.0$ 时 IS 最优，呈现质量‑多样性权衡；过高尺度会导致过饱和和纹理平滑。

#### 3.4 与 CFG 的联合使用

PAG 可与 CFG 叠加用于文本到图像生成，联合引导公式为（Appendix A.2, Eq. 14）：
$$
\tilde{\epsilon}_{\theta}(x_t, c) = \epsilon_{\theta}(x_t, c) + w\big(\epsilon_{\theta}(x_t, c) - \epsilon_{\theta}(x_t, \phi)\big) + s\big(\epsilon_{\theta}(x_t, c) - \hat{\epsilon}_{\theta}(x_t, c)\big)
$$
其中 $w$ 为 CFG 尺度，$c$ 为文本条件，$\phi$ 为空条件。该组合在 Stable Diffusion v1.5 的 MS‑COCO 文本到图像任务上，将仅用 CFG 的 FID 从 15.00 降至 10.08（Table 2），并有效修正结构错误（如补全缺失的眼睛或消除多余肢体，Fig. 7）。

### 扰动层选择

消融研究（Fig. 38, Fig. 40, Table 10）表明，在 U‑Net 较深层（尤其靠近瓶颈层）施加扰动通常效果更好。对于 ADM，最佳层为分辨率最低的块；对于 Stable Diffusion，最佳扰动位置为中块（mid‑block）。这一现象可解释为：深层自注意力负责全局结构组织，扰动这些层能最有效地生成结构退化样本作为引导负例。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2403_17377/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of reverse process*

## 实验与分析

### 主实验结果

PAG 在多个基准模型和任务上均展现出显著的性能提升，覆盖无条件生成、文本条件生成以及逆问题求解。

**ADM (ImageNet 256×256)。** 在无条件生成任务中，PAG 将 FID 从无引导基线的 26.21 降至 **16.23**（降幅 9.98），IS 亦有大幅提升（Table 1）。在条件生成任务中，PAG 将 FID 从 10.94 降至 **6.32**（降幅 4.62），优于 SAG 等早期无条件引导方法。定性对比（Fig. 5）显示，PAG 生成的样本结构语义显著优于 SAG，伪影更少。

**Stable Diffusion v1.5。** 在无条件生成中，PAG 将 FID 从 53.13 降至 **47.57**（Table 2）。在 MS-COCO 文本到图像任务中，将 PAG 与 CFG 联合使用（CFG+PAG），FID 从 CFG 单独的 15.00 进一步降至 **10.08**。定性结果（Fig. 7）表明，联合应用可有效修正结构错误——例如补全猫缺失的眼睛或消除斑马多余的腿。此外，PAG 在每提示多样性指标（IS 和 LPIPS）上均高于 CFG（Table 3），说明 PAG 在提升结构质量的同时保持了样本多样性。

**SDXL 无条件生成。** 定性展示（Fig. 6）表明，PAG 引导的 SDXL 样本具备语义连贯的结构和高感知质量。但需注意，该结果目前仅以定性形式呈现，缺乏大规模定量指标评估，其结论强度有待进一步验证。

**逆问题求解。** 在 FFHQ 256×256 数据集上，将 PAG 嵌入基于扩散的逆问题求解器 PSLD 后，各项指标均大幅提升（Table 4）：
- 方块修复：FID 从 43.11 降至 **21.13**（降幅 21.98）；
- 运动去模糊：FID 从 93.39 降至 **40.26**（降幅 53.13）；
- 高斯去模糊（DPS+PAG）：FID 从 44.05 降至 **29.42**（Table 8，降幅 14.63）；
- 超分辨率（×8）：LPIPS 从 0.52 降至 **0.38**。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2403_17377/figures/032_Table_8.jpg]]
*Table 8: Quantitative results of DPS [6] on FFHQ [27] 256×256 1K validation set [27]*

定性结果（Fig. 8）进一步证实，PAG 能有效消除逆问题求解中的伪影和模糊，恢复更真实的图像细节。

**ControlNet（无文本提示）。** 当 ControlNet 以姿态或深度为条件但无文本提示时，PAG 引导的样本展现出更真实的结构和更少的伪影（Fig. 9），验证了 PAG 在缺乏语言条件时的结构增强能力。

---

### 消融实验

**扰动策略。** 在 ADM ImageNet 256×256 无条件模型上，将自注意力图替换为单位矩阵（即结构扰动）的 FID 为 **32.34**，显著优于随机 mask（40.20）、非对角线 mask（39.49）和加性噪声（62.83）（Table 9, Fig. 36）。若扰动外观分量（将 $V_t$ 替换为空间均值）或完全跳过自注意力，效果均不及结构扰动（Fig. 42）。这验证了“仅移除结构信息、保留外观”策略的优越性。

**扰动施加层位。** 在 U-Net 的较深层（尤其靠近瓶颈层）施加扰动通常比浅层效果更好。ADM 中，最佳扰动层为输入块的深层（Table 10, Fig. 38）；Stable Diffusion 中，最佳扰动位置为中块（mid-block）（Fig. 40）。这一规律与深层自注意力负责全局结构聚合的直觉一致。

**引导尺度。** 引导尺度 $s$ 在 1.0 时 FID 最佳，在 2.0 时 IS 最佳，呈现质量‑多样性权衡（Fig. 34, Fig. 35）。过高尺度会导致过饱和和纹理平滑，与 CFG 的高尺度问题类似。但与 SAG 相比，PAG 对引导尺度不敏感——即使在高尺度（如 $s=63$）下仍能保持物体形状和细节，不产生明显伪影（Fig. 46），显示出更强的鲁棒性。

**CFG 联合训练的必要性。** 若使用分别训练的条件和无条件模型实现 CFG，其效果远不如联合训练的 CFG，而 PAG 无需联合训练即可达到甚至超越 CFG 的结构增强效果（Fig. 41），进一步凸显了 PAG 的无训练优势。

---

### 计算开销与公平性

PAG 每个采样步骤需执行两次 U-Net 前向传播（原始预测 + 扰动预测），计算成本约为无引导采样的两倍，与 CFG 相当（Table 6）。文中指出可通过批量处理优化，但未报告实际推理延迟的直接对比，该点需手动验证。

---

### 失败模式与局限

1. **高尺度过饱和**：引导尺度过高时，样本出现过度饱和伪影，类似于 CFG 的已知问题，需仔细校准尺度。
2. **计算开销**：每步两次前向传播使推理成本高于无引导采样，在资源受限场景中可能成为瓶颈。
3. **扰动策略单一**：目前仅探索了以单位矩阵替换自注意力图这一种扰动方式，未研究其他可能更优的扰动策略。
4. **新模型评估不足**：对 SDXL 等新模型仅在定性上展示，缺乏大规模定量指标评估，结论的泛化性有待进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2403_17377/figures/005_Table_1.jpg]]
*Table 1: Quantitative results on ADM [10]. The best values are in bold*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2403_17377/figures/006_Table_2.jpg]]
*Table 2: Quantitative results on Stable Diffusion [47]. The results were obtained using Stable Diffusion v1.5. Sampling was conducted for each with 30K images, and the results were measured accordingly. For text-to-image tasks, 30k prompts were randomly selected from the MS-COCO 2014 validation set [37]*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2403_17377/figures/011_Table_4.jpg]]
*Table 4: Quantitative results of PSLD [50] on FFHQ [27] 256×256 1K validation set*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2403_17377/figures/048_Table_9.jpg]]
*Table 9: Ablation study on perturbations. We sampled 5K images from the ADM [10] ImageNet [9] 256×256 unconditional model. Perturbations are applied to the same layer (input.13) and the same guidance scale (s = 1.0) is used*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2403_17377/figures/053_Table_10.jpg]]
*Table 10: Layer ablation on ADM. We evaluate the FID [16] of 5K samples from ImageNet [9] 256×256 unconditional model using DDIM [54] 25 step sampling*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2403_17377/figures/050_Figure_38.jpg]]
*Figure 38: Ablation study on which layer to apply perturbation with ADM [10]*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2403_17377/figures/052_Figure_40.jpg]]
*Figure 40: Ablation study on which layer to apply perturbation with Stable Diffusion [47]*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2403_17377/figures/059_Figure_46.jpg]]
*Figure 46: Comparison of samples with SAG [20] and PAG for different guidance scales. Samples are generated by ADM [10] conditional ImageNet $256\times 256$ model, showcasing the impact of incrementally increasing the guidance scale from 0.0 to 63.0, from the top to the bottom of the figure. (a): Samples generated with a high guidance scale using SAG exhibit artifacts and over-smoothness due to excessive perturbation, specifically blurring on the input, with the outlines of the blur mask clearly visible. (b): Compared to SAG, samples generated with higher scale PAG display high-quality results, characterized by well-structured shape and high detail. Within each group, from left to right, the classes are...*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2403_17377/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison between SAG [20] and PAG. Images are sampled from the ImageNet $256\times 256$ unconditional model using the same seed sequence. Compared to samples guided by SAG, those guided by PAG exhibit significantly improved semantic structures with artifacts removed*

## 方法谱系与知识库定位

### 1. 与现有引导方法的谱系关系

Perturbed-Attention Guidance (PAG) 属于扩散模型**采样引导（sampling guidance）**技术家族。该家族的核心思想是在去噪过程中引入一个“不良”预测作为负例，通过线性组合将生成推向更优方向。PAG 在这一谱系中的定位可从三个维度理解：

**（1）与 Classifier-Free Guidance (CFG) 的关系：继承框架，突破条件依赖**

CFG（Ho & Salimans, NeurIPS 2022）是该领域的事实标准，其引导公式为：

$$\tilde{\epsilon}_{\theta}(x_t, c) = \epsilon_{\theta}(x_t, c) + w(\epsilon_{\theta}(x_t, c) - \epsilon_{\theta}(x_t, \varnothing))$$

CFG 将联合训练的无条件预测 $\epsilon_{\theta}(x_t, \varnothing)$ 作为“不良”路径。PAG 完全继承了这一线性组合框架（Eq. 10），但**将“不良”路径的来源从“联合训练的无条件模型”替换为“扰动自注意力产生的退化预测”**（Fig. 4）。这一替换带来了根本性突破：PAG 不再需要条件 $c$，因此可在无条件生成、无文本提示的 ControlNet、逆问题求解等 CFG 完全无法使用的场景中工作。

**（2）与 Self-Attention Guidance (SAG) 的关系：同属无条件引导，但扰动策略根本不同**

SAG（Hong et al., NeurIPS 2023）是 PAG 之前少有的无条件引导方法。SAG 通过对输入图像施加对抗性模糊来生成退化样本，然后用注意力图作为 mask 进行引导。PAG 与 SAG 的关键差异在于**扰动位置**：

- SAG 扰动**输入图像**（像素空间），容易导致分布外（OOD）问题，在高引导尺度下产生明显的模糊伪影和过平滑（Fig. 46）。
- PAG 扰动**自注意力图**（特征空间），仅将 Softmax 注意力矩阵替换为单位矩阵 $\mathbf{I}$，保留 $V_t$ 中的外观信息。这种扰动对模型输出的影响轻微，避免了 OOD 问题（Sec. 4.2）。

实验表明，PAG 在 ImageNet 256×256 无条件生成上 FID 达到 16.23，远优于 SAG 的 18.32 和无引导基线的 26.21（Table 1）。更重要的是，PAG 对引导尺度不敏感，在 $s=63$ 的极端尺度下仍能保持物体形状和细节，而 SAG 在此尺度下已产生严重伪影（Fig. 46）。

**（3）与逆问题求解方法的集成关系：即插即用的增强模块**

PAG 可作为即插即用模块与现有逆问题求解器集成。在 FFHQ 256×256 上：

- **PSLD**（Rout et al., CVPR 2024）：PSLD+PAG 在 box inpainting 上将 FID 从 43.11 降至 21.13（↓21.98），在 motion deblur 上从 93.39 降至 40.26（↓53.13）（Table 4）。
- **DPS**（Chung et al., CVPR 2023）：DPS+PAG 在 Gaussian deblur 上将 FID 从 44.05 降至 29.42（↓14.63）（Table 8）。

这种集成能力源于 PAG 不修改基础模型架构，仅在采样循环中增加一次额外的前向传播。

### 2. 适用边界

**适用场景：**

- **无条件生成**：PAG 最核心的优势场景。当无类别标签、文本提示等任何条件时，CFG 完全不可用，PAG 是唯一有效的引导方法。
- **弱条件生成**：如 ControlNet 配合空文本提示（Fig. 9），此时 CFG 的条件分支退化为无意义输入，PAG 可填补结构引导的空白。
- **逆问题求解**：与 PSLD、DPS 等求解器集成，在 inpainting、deblurring、super-resolution 等任务中显著减少伪影和模糊（Fig. 8）。
- **与 CFG 联合使用**：在文本到图像生成中，PAG 与 CFG 可同时作用（Eq. 14），在 MS-COCO 上将 FID 从 CFG-only 的 15.00 进一步降至 10.08（Table 2），并能修正结构错误（如补全缺失的眼睛、消除多余腿，Fig. 7）。

**不适用或需谨慎的场景：**

- **极低计算预算**：PAG 每步需两次前向传播，计算开销约为无引导采样的 2 倍（与 CFG 相近，Table 6）。在实时生成等严格延迟约束下可能不适用。
- **高引导尺度下的过饱和**：当引导尺度 $s$ 过高时，样本可能出现过度饱和（类似 CFG 的过饱和问题），需要仔细校准尺度。消融实验显示 $s=1.0$ 时 FID 最佳，$s=2.0$ 时 IS 最佳，表现出质量-多样性权衡（Fig. 34, Fig. 35）。

### 3. 局限与开放问题

**已知局限：**

1. **计算开销**：每步需两次前向传播，计算成本高于无引导采样。文中指出可通过批量处理优化，但未报告实际推理延迟的直接对比。
2. **扰动策略单一**：目前仅探索了以单位矩阵替换自注意力图这一种扰动方式，未研究其他可能更优的扰动策略（如部分结构保留、自适应扰动强度等）。
3. **新模型评估不足**：对 SDXL 等新模型仅在定性上展示（Fig. 6），缺乏大规模定量指标评估。
4. **人类评估细节缺失**：人类偏好评估的参与者数量和统计细节未完全披露，可能存在选择偏差。

**开放问题：**

1. **高效扰动策略**：能否设计更高效的扰动策略，在保持引导效果的同时减少计算开销？例如，是否可以共享原始前向传播和扰动前向传播的部分计算？
2. **自适应扰动**：是否存在针对不同任务和模型的自适应扰动方法，替代简单的单位矩阵替换？消融实验表明，在 U-Net 较深层（尤其靠近瓶颈层）施加扰动效果更好（Fig. 38, Fig. 40），但最优层选择目前依赖手动调参。
3. **自动尺度校准**：如何自动校准引导尺度 $s$，避免高尺度下的过饱和伪影？当前 $s$ 是全局固定超参数，不同任务和模型需要独立调参（Table 5）。
4. **训练结合**：PAG 是否可以与训练结合（例如微调扰动分支）以进一步提升稳定性与多样性？目前 PAG 是纯推理时方法，训练阶段完全未涉及。
5. **理论分析**：PAG 的隐式判别器框架（Eq. 11）提供了理论直觉，但缺乏严格的收敛性分析或与能量模型的等价性证明。这部分理论缺口可能限制了对引导行为更深入的理解。

## 原文 PDF

![[paperPDFs/ECCV_2024/Self_Rectifying_Diffusion_Sampling_with_Perturbed_Attention_Guidance.pdf]]
