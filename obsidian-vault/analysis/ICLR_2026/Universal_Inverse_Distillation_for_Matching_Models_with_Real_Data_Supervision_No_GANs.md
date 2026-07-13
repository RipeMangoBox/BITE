---
title: "Universal Inverse Distillation for Matching Models with Real-Data Supervision (No GANs)"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Universal_Inverse_Distillation_for_Matching_Models_with_Real_Data_Supervision_No_GANs.pdf
project_link: null
code_link: https://github.com/David-cripto/RealUID
openreview_forum_id: 8NuN5UzXLC
aliases:
- RUIDRD
- UIDMMRDSNG
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "通过系数 α, β 将真实数据项直接嵌入蒸馏损失（RealUM loss），并以 min-max 优化替代传统单步最小化，从而在不引入 GAN 的前提下有效利用真实数据，同时统一了不同匹配模型的蒸馏。"
primary_logic: "利用线性化技巧将学生与教师函数间的 ℓ₂ 距离转化为可处理的 min-max 目标，并借助逆优化视角将多种蒸馏方法（FGM, SiD, IBMD）统一为同一个通用框架；在此基础上，通过拆分损失项为生成数据与真实数据部分并加权，实现了天然的、无对抗的真实数据融入。"
claims:
- "RealUID 是第一个无需 GAN 就能无缝地将真实数据融入匹配模型蒸馏的通用框架。"
- "RealUID 统一了先前的 FGM、SiD 和 IBMD 方法，并提供了基于线性化技术的简洁理论解释。"
- "通过系数 β/α ≠ 1 能够有效利用真实数据，且实验中 β/α = 0.98 或 1.02 显著优于不使用真实数据的基线。"
- "CIFAR-10 (无条件生成) 上 FID = 1.98 (RealUID, 微调)"
---

# Universal Inverse Distillation for Matching Models with Real-Data Supervision (No GANs)

> [!tip] 核心洞察
> 利用线性化技巧将学生与教师函数间的 ℓ₂ 距离转化为可处理的 min-max 目标，并借助逆优化视角将多种蒸馏方法（FGM, SiD, IBMD）统一为同一个通用框架；在此基础上，通过拆分损失项为生成数据与真实数据部分并加权，实现了天然的、无对抗的真实数据融入。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通用逆蒸馏：无GAN的真实数据监督匹配模型 |
| 英文题名 | Universal Inverse Distillation for Matching Models with Real-Data Supervision (No GANs) |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=8NuN5UzXLC) · [GitHub](https://github.com/David-cripto/RealUID) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | RealUID (Universal Inverse Distillation with Real Data) |
| Dataset | CIFAR-10 (无条件生成), CIFAR-10 (条件生成), CelebA (无条件生成) |

> [!tip] 效果简介
> - CIFAR-10 (无条件生成) 上，FID 为 1.98 (RealUID, 微调)，对比 2.58 (UID 无真实数据)，变化 -0.60。
> - CIFAR-10 (无条件生成) 上，FID 为 2.23 (RealUID, 无微调)，对比 2.58 (UID 无真实数据)，变化 -0.35。
> - CIFAR-10 (条件生成) 上，FID 为 1.87 (RealUID, 微调)，对比 2.12 (UID+GAN 微调)，变化 -0.25。

## 概要

**核心问题**：扩散模型、流匹配模型和桥匹配模型等现代生成模型虽然生成质量高，但多步采样的推理代价极大。为将其压缩为一步生成器，研究者提出了多种蒸馏方法——如面向流匹配的 **FGM**（Huang et al., 2024）、面向扩散的 **SiD**（Zhou et al., 2024b）和面向桥匹配的 **IBMD**（Gushchin et al., 2025）——但这些方法各自针对特定框架设计，缺乏统一的理论基础。更关键的是，它们天然无法利用真实数据：若强行引入真实数据，必须借助额外的对抗训练（GAN）和判别器（如 **UID+GAN**，Zhou et al., 2024a），这显著增加了训练复杂度和不稳定性。

**核心方法**：本文提出 **RealUID（Universal Inverse Distillation with Real Data）**，一个无需 GAN 即可无缝融入真实数据的通用蒸馏框架。其核心创新在于两点：

1. **统一的理论框架**：利用线性化技巧 $\\|a\\|^2 = \\max_b \\{ -\\|b\\|^2 + 2\\langle b, a\\rangle \\}$ 将学生与教师函数间的 ℓ₂ 距离转化为可处理的 min-max 优化目标，并借助逆优化视角将 FGM、SiD、IBMD 等方法统一为同一个通用框架。

2. **无对抗的真实数据融入**：通过系数 α, β 将生成数据与真实数据项直接嵌入蒸馏损失（RealUM loss），以 min-max 优化替代传统单步最小化。当 β/α ≠ 1 时，真实数据自然参与训练，无需任何判别器或对抗损失。

**核心结论**：

- RealUID 是首个无需 GAN 就能在所有匹配模型中无缝融入真实数据的通用蒸馏框架。
- 在 CIFAR-10 无条件生成上，RealUID 达到 FID **1.98**（微调后），显著优于无真实数据的 UID 基线（2.58）和 UID+GAN（2.12）；在 CelebA 上达到 FID **0.89**，与 UID+GAN（0.87）相当。
- 系数比 β/α 是性能的关键控制变量：β/α = 0.98 或 1.02 显著优于 β/α = 1（不使用真实数据），且 RealUID 的收敛速度约为 UID 基线的 3 倍。
- 采用轻量架构的 RealUID 在推理速度上达到 FGM/SiD 约 2 倍的加速，同时参数规模和显存占用更低。

**局限与展望**：当前实验限于 CIFAR-10 和 CelebA 等小型数据集及轻量 UNet 架构，尚未在 ImageNet 或更大模型（如 DiT）上验证；系数 α, β 的最优值依赖网格搜索，缺乏自适应机制；桥匹配和随机插值模型的 RealUID 蒸馏尚未进行实验验证。

### 匹配模型的蒸馏困境

扩散模型、流匹配和桥匹配等匹配模型（matching models）已成为生成建模的主流范式。这些模型通过模拟数据分布与先验噪声之间的连续变换来生成高质量样本，但其推理过程需要反复求解常微分方程或随机微分方程，导致数百次网络前向计算（NFE），严重制约了实际部署效率。为此，知识蒸馏技术被引入，旨在将多步采样的教师模型压缩为一步生成器。

然而，现有蒸馏方法面临两个根本性瓶颈：

**第一，框架碎片化。** 针对流匹配的 **FGM**（Huang et al., 2024）、针对扩散模型的 **SiD**（Zhou et al., 2024b）和针对桥匹配的 **IBMD**（Gushchin et al., 2025）各自独立设计，分别面向特定概率路径和条件向量场形式，缺乏统一的理论基础。这种碎片化意味着每出现一种新的匹配模型变体，就需要重新推导和实现一套蒸馏方案，知识无法跨框架迁移。

**第二，真实数据利用的天然障碍。** 上述方法本质上都是“无数据”（data-free）蒸馏——它们仅依赖学生生成器自身的合成样本来计算蒸馏损失，完全忽视了真实训练数据的分布信息。若想融入真实数据，现有唯一途径是引入对抗训练（GAN），即 **UID+GAN** 方案（Zhou et al., 2024a）。但这带来了额外成本：需要设计判别器网络来区分真实数据与生成数据的加噪过程，并精心平衡对抗损失与蒸馏损失的权重。判别器的训练不稳定、超参数敏感，且增加了显存和计算开销。

### 核心动机：能否无对抗地统一利用真实数据？

本文的核心动机源于一个简洁的观察：真实数据天然携带教师模型的分布先验，若能将其直接注入蒸馏损失，理论上可以弥补学生生成器在分布覆盖上的盲区，提升生成质量。问题在于，如何在不引入判别器、不增加对抗训练复杂度的前提下，实现这一目标？

这引出了两个紧密关联的研究问题：

1. **统一性**：能否找到一个通用的蒸馏理论框架，将 FGM、SiD、IBMD 等方法统一为同一形式，使后续扩展只需在框架内调整参数，而非重新设计？
2. **真实数据融入**：能否在该统一框架内，通过损失函数的天然结构——而非外部对抗模块——实现真实数据的无缝接入？

本文的 **RealUID**（Universal Inverse Distillation with Real Data）正是围绕这两个问题展开。它通过线性化技巧将学生与教师函数间的 ℓ₂ 距离转化为可处理的 min-max 目标，并借助逆优化视角统一了先前的无数据蒸馏方法。在此基础上，通过将蒸馏损失拆分为生成数据项与真实数据项并引入系数 α、β 加权，RealUID 实现了无 GAN 的真实数据监督——这是该方向的首个通用方案。

### 方法定位

RealUID 并非另起炉灶，而是在逆蒸馏（Inverse Distillation）范式下的自然延伸。它与 UID+GAN 共享利用真实数据的动机，但采取了根本不同的技术路线：后者依赖外挂判别器的对抗博弈，前者则通过损失函数内部的系数调节实现数据平衡。这一差异使得 RealUID 在结构简洁性、训练稳定性和计算效率上具备天然优势，同时保持了与多种匹配模型框架的兼容性。

## 核心方法与创新机理

RealUID 的核心创新在于**将真实数据以自然、无对抗的方式融入匹配模型的通用蒸馏框架**，从根本上改变了此前蒸馏方法对真实数据的利用方式。其关键突破可归纳为以下三个维度。

### 1. 无 GAN 的真实数据融入机制

现有匹配模型蒸馏方法面临一个结构性瓶颈：无论是面向流匹配的 **FGM**（Huang et al., 2024）、面向扩散的 **SiD**（Zhou et al., 2024b），还是面向桥匹配的 **IBMD**（Gushchin et al., 2025），本质上都是完全 data-free 的——它们仅在学生生成器自身产出的合成数据上计算蒸馏损失，天然无法利用真实数据分布的信息。若强行引入真实数据，此前唯一可行的路径是附加对抗训练（GAN），即引入额外的判别器网络和对抗损失项（**UID+GAN**，Zhou et al., 2024a），这显著增加了训练复杂度与不稳定性。

RealUID 通过重新设计通用匹配损失（Universal Matching loss），将真实数据**直接嵌入蒸馏目标函数**，从根本上消除了对判别器的依赖。具体而言，其提出的 RealUM 损失 $\mathcal{L}_{\mathrm{R-UM}}^{\alpha,\beta}$ 定义为生成数据项与真实数据项的加权和：

$$\mathcal{L}_{\mathrm{R-UM}}^{\alpha,\beta}(f, p_0^\theta) = \alpha \cdot \mathbb{E}_{t, x_0^\theta, x_t^\theta} \left[ \| f_t(x_t^\theta) - \frac{\beta}{\alpha} f^\theta(x_t^\theta|x_0^\theta) \|^2 \right] + (1-\alpha) \cdot \mathbb{E}_{t, x_0^*, x_t^*} \left[ \| f_t(x_t^*) - \frac{1-\beta}{1-\alpha} f_t^*(x_t^*|x_0^*) \|^2 \right]$$

其中 $\alpha, \beta \in (0,1]$ 分别控制生成数据与真实数据项的贡献权重。当 $\alpha=\beta=1$ 时，该损失退化为纯生成数据的 UM 损失；当 $\beta/\alpha \neq 1$ 时，真实数据开始发挥实质作用。这一设计使 RealUID 成为**首个无需 GAN 即可无缝利用真实数据的通用蒸馏框架**。

### 2. 从单步最小化到 min-max 优化：线性化技巧驱动的统一理论

RealUID 的第二个关键创新在于对蒸馏优化目标形式的根本性改造。此前的方法（FGM、SiD 等）本质上都在执行单步最小化：直接最小化学生生成器在自身分布上定义的某个损失。RealUID 则通过**线性化技巧**，将学生与教师函数间的 $\ell_2$ 距离转化为可处理的 min-max 目标：

$$\min_{\theta} \max_{f} \left\{ \mathcal{L}_{\mathrm{R-UID}}^{\alpha,\beta}(f, p_0^\theta) := \mathcal{L}_{\mathrm{R-UM}}^{\alpha,\beta}(f^*, p_0^\theta) - \mathcal{L}_{\mathrm{R-UM}}^{\alpha,\beta}(f, p_0^\theta) \right\}$$

这一转化的核心在于恒等式 $\|a\|^2 = \max_{b} \{ -\|b\|^2 + 2\langle b, a\rangle \}$，它将原本不可直接计算的平方范数距离表达为关于“虚假模型” $f$ 的线性内积最大化问题。内层最大化恢复教师与学生间的加权 $\ell_2$ 距离，外层最小化该距离以训练生成器。这种 min-max 结构不仅使蒸馏损失在数学上可处理，还揭示了该方法与**逆优化**的深层联系——RealUID 本质上是在寻找一个生成器参数 $\theta$，使得教师函数 $f^*$ 成为该生成器分布下 UM 损失的最优解。

### 3. 统一多框架的通用性

RealUID 的第三个创新在于其框架的**通用性**。通过将 FGM、SiD 和 IBMD 等先前方法统一到同一个 UID 框架下，RealUID 不再局限于单一匹配模型类型，而是同时覆盖流匹配、扩散模型、桥匹配及随机插值模型。这种统一性源于其核心损失函数对条件函数 $f_t^{p_0}(x_t|x_0)$ 的抽象——无论是流匹配中的条件漂移、扩散中的条件分数，还是桥匹配中的条件向量场，均可纳入同一数学形式。实验验证了该框架在流匹配模型下的完整流程，并为扩散模型的 RealSiD 扩展提供了初步探索。

### 创新总结

| 创新维度 | 基线方法 | RealUID 方案 | 关键证据 |
|---------|---------|-------------|---------|
| 真实数据利用 | 完全 data-free 或依赖 GAN 判别器 | 通过系数 $\alpha,\beta$ 直接嵌入蒸馏损失，无需判别器 | RealUM loss (Eq.16)；$\beta/\alpha \neq 1$ 时真实数据生效 |
| 优化目标形式 | 单步最小化生成器损失 | 关于虚假模型和生成器的 min-max 优化 | Theorem 2 (Eq.17)；线性化恒等式 |
| 框架通用性 | 各自针对一种模型（仅流/扩散/桥） | 统一涵盖流匹配、扩散、桥匹配及随机插值 | 统一 FGM、SiD、IBMD 的理论推导 |

实验结果表明，仅通过调整 $\beta/\alpha$ 的微小偏移（如 0.98 或 1.02），RealUID 即可在 CIFAR-10 上将 FID 从 2.58（无真实数据 UID 基线）降至 2.23，经微调后进一步降至 1.98，且收敛速度约为基线的 3 倍。这些增益完全来自损失函数的内在设计，无需任何额外的网络模块或对抗训练。

RealUID 是一个无需 GAN 即可将真实数据融入匹配模型蒸馏的通用框架。其核心流程围绕四个模块展开：冻结的教师模型 $f^*$、学生生成器 $G_\theta$、可训练的虚假模型 $f$，以及带有真实数据的通用匹配损失 $\mathcal{L}_{\mathrm{R-UM}}^{\alpha,\beta}$。

**数据流与模块交互**（参见 Figure 1）：

1. **生成路径**：学生生成器 $G_\theta$ 从噪声 $z$ 出发，一步映射到数据空间，产生生成样本 $x_0^\theta \sim p_0^\theta$。随后，$x_0^\theta$ 经过前向加噪过程得到中间状态 $x_t^\theta \sim p_t^\theta(\cdot|x_0^\theta)$。
2. **真实数据路径**：真实样本 $x_0^* \sim p_0^*$ 同样经过前向加噪过程，产生 $x_t^* \sim p_t^*(\cdot|x_0^*)$。
3. **教师监督**：冻结的教师模型 $f^*$ 为生成路径和真实数据路径提供条件函数 $f_t^*(x_t^\theta|x_0^\theta)$ 和 $f_t^*(x_t^*|x_0^*)$，作为蒸馏的 ground-truth 信号。
4. **虚假模型**：可训练的虚假模型 $f$（或等价地表示为差值 $\delta = f^* - f$）接收来自两条路径的加噪样本，输出预测的函数值。

**训练循环**：RealUID 采用 min-max 优化范式，交替更新虚假模型和生成器：

- **虚假模型更新（内层最大化）**：固定生成器 $\theta$，最大化 RealUID 损失 $\mathcal{L}_{\mathrm{R-UID}}^{\alpha,\beta}(f, p_0^\theta)$。该损失定义为教师与虚假模型在 RealUM 损失上的差值：
  $$\mathcal{L}_{\mathrm{R-UID}}^{\alpha,\beta}(f, p_0^\theta) := \mathcal{L}_{\mathrm{R-UM}}^{\alpha,\beta}(f^*, p_0^\theta) - \mathcal{L}_{\mathrm{R-UM}}^{\alpha,\beta}(f, p_0^\theta)$$
  内层最大化等价于恢复教师与学生函数间的加权 $\ell_2$ 距离（Lemma 2）。为保证训练稳定性，虚假模型每轮更新多次（通常 5 次），而生成器仅更新一次。

- **生成器更新（外层最小化）**：固定虚假模型 $f$，最小化 $\mathcal{L}_{\mathrm{R-UID}}^{\alpha,\beta}(f, p_0^\theta)$ 以更新生成器参数 $\theta$，从而缩小学生分布与教师分布之间的差异。

**RealUM 损失**：框架的核心损失函数 $\mathcal{L}_{\mathrm{R-UM}}^{\alpha,\beta}$ 通过系数 $\alpha, \beta \in (0,1]$ 将生成数据和真实数据统一在同一目标中：
$$\mathcal{L}_{\mathrm{R-UM}}^{\alpha,\beta}(f, p_0^\theta) = \alpha \cdot \mathbb{E}_{t, x_0^\theta, x_t^\theta} \left[ \| f_t(x_t^\theta) - \frac{\beta}{\alpha} f^\theta(x_t^\theta|x_0^\theta) \|^2 \right] + (1-\alpha) \cdot \mathbb{E}_{t, x_0^*, x_t^*} \left[ \| f_t(x_t^*) - \frac{1-\beta}{1-\alpha} f_t^*(x_t^*|x_0^*) \|^2 \right]$$

- 当 $\alpha = \beta = 1$ 时，损失退化为纯生成数据的 UM 损失，等价于不使用真实数据的 UID 基线。
- 当 $\beta/\alpha \neq 1$ 时，真实数据项被有效激活，且无需引入额外的判别器或对抗损失。

**关键设计决策**：系数比 $\beta/\alpha$ 是控制真实数据贡献的核心旋钮。实验表明，$\beta/\alpha = 0.98$ 或 $1.02$ 等微小偏离 $1$ 的取值即可显著提升性能（Table 1, Table 7），验证了该机制的有效性。整个框架通过线性化技巧将原本不可处理的 $\ell_2$ 距离转化为可优化的 min-max 目标，实现了对 FGM、SiD、IBMD 等先前蒸馏方法的统一。

### 3.1 统一逆蒸馏（UID）框架

RealUID 的理论基础建立在**统一逆蒸馏（Universal Inverse Distillation, UID）**框架之上。该框架首先将 FGM、SiD 和 IBMD 等先前针对不同匹配模型分别设计的无数据蒸馏方法统一为同一形式。

蒸馏的核心目标是训练一个单步生成器 $G_\theta$，使其生成的分布 $p_0^\theta$ 尽可能接近教师模型 $f^*$ 所表征的数据分布。直观上，这等价于最小化教师函数与学生函数之间的加权 $\ell_2$ 距离。然而，学生函数 $f^\theta$ 本身无法直接计算，导致该距离不可直接优化。

UID 的关键洞察在于利用以下**线性化恒等式**将平方范数转化为可处理的形式：

$$
\|a\|^2 = \operatorname*{max}_{b \in \mathbb{R}^D} \{ -\|b\|^2 + 2\langle b, a\rangle \}
$$

通过引入一个可训练的**虚假模型 $f$**（或等效的参数化 $\delta = f^* - f$），UID 将蒸馏问题转化为一个 min-max 优化问题：

$$
\operatorname*{min}_{\theta} \operatorname*{max}_{f} \left\{ \mathcal{L}_{\text{UID}}(f, p_0^\theta) := \mathcal{L}_{\text{UM}}(f^*, p_0^\theta) - \mathcal{L}_{\text{UM}}(f, p_0^\theta) \right\}
$$

其中 $\mathcal{L}_{\text{UM}}(f, p_0)$ 是通用匹配损失（Universal Matching loss），定义为：

$$
\mathcal{L}_{\text{UM}}(f, p_0) := \mathbb{E}_{t \sim [0,T]} \mathbb{E}_{x_0 \sim p_0, x_t \sim p_t(\cdot|x_0)} \left[ \| f_t(x_t) - f_t^{p_0}(x_t|x_0) \|^2 \right]
$$

**引理 1** 给出了该 min-max 优化的理论保证：最大化步骤精确恢复了教师与学生函数在学生生成分布上的 $\ell_2$ 距离：

$$
\operatorname*{max}_{f} \mathcal{L}_{\text{UID}}(f, p_0^\theta) = \mathbb{E}_{t \sim [0,T]} \mathbb{E}_{x_t^\theta \sim p_t^\theta} \left[ \| f_t^*(x_t^\theta) - f_t^\theta(x_t^\theta) \|^2 \right]
$$

### 3.2 真实数据融入：RealUM 损失

UID 框架天然是**无数据**的——其损失函数仅依赖于生成器自身的输出。为了在不引入 GAN 判别器的情况下利用真实数据，RealUID 重新设计了匹配损失，提出了**RealUM 损失**（Real-data Universal Matching loss）：

$$
\begin{aligned}
\mathcal{L}_{\mathrm{R\text{-}UM}}^{\alpha,\beta}(f, p_0^\theta) = 
& \alpha \cdot \mathbb{E}_{t\sim[0,T]} \mathbb{E}_{x_0^\theta\sim p_0^\theta, x_t^\theta\sim p_t^\theta(\cdot|x_0^\theta)} \left[ \left\| f_t(x_t^\theta) - \frac{\beta}{\alpha} f^\theta(x_t^\theta|x_0^\theta) \right\|^2 \right] \\
+ & (1-\alpha) \cdot \mathbb{E}_{t\sim[0,T]} \mathbb{E}_{x_0^*\sim p_0^*, x_t^*\sim p_t^*(\cdot|x_0^*)} \left[ \left\| f_t(x_t^*) - \frac{1-\beta}{1-\alpha} f_t^*(x_t^*|x_0^*) \right\|^2 \right]
\end{aligned}
$$

**变量含义**：
- $f_t(x_t)$：待训练的函数（虚假模型），在 min-max 优化中执行最大化步骤
- $p_0^\theta$：学生生成器的输出分布
- $p_0^*$：真实数据分布
- $f_t^*(x_t|x_0)$：冻结的教师模型提供的条件函数
- $f^\theta(x_t|x_0)$：学生生成器的条件函数
- $\alpha, \beta \in (0, 1]$：控制生成数据与真实数据贡献比例的核心超参数

**关键性质**：
1. 当 $\alpha = \beta = 1$ 时，第二项消失，RealUM 退化为纯生成数据的 UM 损失，等价于无数据的 UID 基线。
2. 当输入为真实数据分布 $p_0^*$ 时，RealUM 损失的最优解仍然是教师 $f^*$，保证了损失函数的一致性。
3. 系数比 $\beta/\alpha$ 是决定真实数据利用效果的**核心控制旋钮**：$\beta/\alpha \neq 1$ 时真实数据项被激活；$\beta/\alpha = 1$ 时真实数据项退化为常数，不产生有效梯度。

### 3.3 RealUID 的 min-max 优化目标

将 RealUM 损失代入 UID 的 min-max 框架，即得到 **RealUID 损失**（定理 2）：

$$
\operatorname*{min}_{\theta} \operatorname*{max}_{f} \left\{ \mathcal{L}_{\mathrm{R\text{-}UID}}^{\alpha,\beta}(f, p_0^\theta) := \mathcal{L}_{\mathrm{R\text{-}UM}}^{\alpha,\beta}(f^*, p_0^\theta) - \mathcal{L}_{\mathrm{R\text{-}UM}}^{\alpha,\beta}(f, p_0^\theta) \right\}
$$

**引理 2** 揭示了该目标隐式最小化的量——最大化步骤后，RealUID 损失等价于学生与教师函数在真实数据分布上的加权 $\ell_2$ 距离：

$$
\operatorname*{max}_{f} \mathcal{L}_{\mathrm{R\text{-}UID}}^{\alpha,\beta}(f, p_0^\theta) = \mathbb{E}_{t\sim[0,T]} \left[ \left\| \frac{\beta}{\alpha} \cdot [p_t^*(x_t^*) f_t^*(x_t^*) - p_t^\theta(x_t^*) f_t^\theta(x_t^*)] + (p_t^\theta(x_t^*) - p_t^*(x_t^*)) \cdot f_t^*(x_t^*) \right\|^2 \right]
$$

这一形式表明：$\beta/\alpha$ 直接加权了教师与学生函数的差异项，而 $\alpha$ 本身仅起到整体缩放作用。当 $\beta/\alpha \neq 1$ 时，真实数据的分布信息通过 $p_t^*(x_t^*)$ 项被有效注入优化过程，从而在不依赖对抗训练的前提下实现了真实数据的自然融入。

### 3.4 训练流程

RealUID 的训练采用交替优化策略（见 Algorithm 1）：

1. **虚假模型更新**（内层最大化）：固定生成器 $\theta$，对虚假模型 $f$ 进行多次梯度上升，最大化 $\mathcal{L}_{\mathrm{R\text{-}UID}}^{\alpha,\beta}$，以逼近教师与学生间的加权 $\ell_2$ 距离。
2. **生成器更新**（外层最小化）：固定虚假模型 $f$，对生成器参数 $\theta$ 进行一次梯度下降，最小化 $\mathcal{L}_{\mathrm{R\text{-}UID}}^{\alpha,\beta}$，使学生分布向教师分布靠拢。

该流程的四个核心模块为：冻结的教师模型 $f^*$（提供蒸馏目标）、学生生成器 $G_\theta$（一步映射噪声到数据）、虚假模型 $f$（近似学生函数，用于最大化步骤）、以及 RealUM 损失（在生成数据和真实数据上加权计算匹配损失）。

## 实验与关键发现

### 主实验结果

RealUID 在 CIFAR-10 和 CelebA 数据集上均取得了优于无真实数据基线 UID 的生成质量，且无需引入 GAN 判别器。

**CIFAR-10 无条件生成**（Table 1, Table 2）：在无微调设定下，RealUID 的最优配置（α=0.88, β/α=0.98）达到 FID 2.23，显著低于 UID 基线的 2.58（Δ=-0.35）。经过额外微调阶段后，FID 进一步降至 1.98（Δ=-0.60），接近教师模型（100 NFE）的性能水平。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_8NuN5UzXLC/figures/002_Table_1.jpg]]
*Table 1: As shown in the table, the ratio $\beta / \alpha$ has the largest impact on the final metrics, while α only adjusts them. Using real data with $\beta / \alpha \stackrel { \cdot } { = }$ 1 or with large values outside the range [0.98, 1.02] consistently degrades performance. In contrast, values $\beta / \alpha \stackrel { - } { = }$ 0 . 9 8 or $\beta / \alpha$ = 1 . 0 2 outperform the baseline for a majority of α. Note that these practical results match the theoretical description in (§3.4)


![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_8NuN5UzXLC/figures/004_Table_2.jpg]]
*Table 2: This table presents the results of ablation study of our RealUID framework, evaluated using the FID metric under both unconditional and conditional generation setups. The Teacher Flow model with 100 NFE is reported as a reference. The performance of the UID (FGM) baseline without real-data incorporation is indicated in italic. For emphasis, we underline the two counterparts that incorporate real data: the GAN-based and our RealUID methods. The best-performing configurations, obtained via an additional fine-tuning stage, are highlighted in bold. Qualitative results are presented in Appendix D.5.1*

**CIFAR-10 条件生成**（Table 2）：微调后的 RealUID 达到 FID 1.87，优于同样经过微调的 UID+GAN 方法（FID 2.12, Δ=-0.25），表明 RealUID 在条件生成场景下同样有效且不依赖对抗训练。

**CelebA 无条件生成**（Table 8）：经过 160 万次迭代的长微调后，RealUID（α=0.88, β=0.90）达到 FID 0.89，优于 UID 基线的 0.96（Δ=-0.07），与 UID+GAN 的 0.87 性能相当。这表明 RealUID 可以在不引入判别器额外复杂度的前提下，达到与 GAN 增强方法相近的生成质量。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_8NuN5UzXLC/figures/019_Table_8.jpg]]
*Table 8: This table presents the results of ablation study of our RealUID framework, evaluated using the FID metric on CelebA dataset, 1,600,000 iterations. The Teacher Flow model with 100 NFE is reported as a reference. The performance of the UID (FGM) baseline without real-data incorporation is indicated in italic. For emphasis, we underline the two counterparts that incorporate real data: the GAN-based and our RealUID methods. The best-performing configuration is highlighted in bold. Qualitative results are presented in Appendix D.5.2*

**推理效率**（Table 5）：得益于基于 Tong et al., 2024 的轻量架构，RealUID 在推理速度上相比 FGM/SiD 方法实现约 2× 加速，同时参数量和显存占用均更低。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_8NuN5UzXLC/figures/014_Table_5.jpg]]
*Table 5: Efficiency comparison. In terms of efficiency, RealUID leverages a lightweight architecture based on (Tong et al., 2024). Therefore, as summarized in Table 5, it achieves nearly 2 $\times$ faster inference, lower memory usage, and reduced model size compared to recent distillation approaches (Zhou et al., 2024b;a; Huang et al., 2024). Table 5: Inference complexity on an Ascend 910B3 (65 GB) NPU. All methods require only 1 NFE. For each method, we report (i) the mean inference time per image (bs=1, fp32), averaged over 10,000 iterations; (ii) the total number of parameters (Millions); and (iii) peak NPU memory usage (maximum allocated and reserved, in MB). Best values are bolded*

### 消融实验

**系数 α 与 β/α 的影响**（Table 1, Table 7）：消融实验表明，系数比 β/α 是影响性能的最关键因素。当 β/α = 1（即不使用真实数据）时，性能与 UID 基线持平；当 β/α 偏离 1 至 0.98 或 1.02 时，FID 显著改善。α 的绝对值主要起微调作用，对最终指标影响较小。β/α 取值过大或过小（超出 [0.98, 1.02] 范围）则会导致性能退化。

**微调阶段的敏感性**（Table 6, Figure 2）：微调阶段同样高度依赖 β_FT/α_FT 的选择。在 CIFAR-10 上，β_FT/α_FT = 0.98 或 1.02 的配置在多数 α 下均优于基线，与预训练阶段的规律一致。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_8NuN5UzXLC/figures/015_Table_6.jpg]]
*Table 6: Ablation of the fine-tuning parameters $\begin{array} { r } { ( \alpha _ { \mathrm { F T } } , \frac { \beta _ { \mathrm { F T } } } { \alpha _ { \mathrm { F T } } } ) } \end{array}$ for our RealUID and fine-tuning scales ( $\lambda _ { \mathrm { F T } } ^ { G _ { \theta } } , \lambda _ { \mathrm { F T } } ^ { D }$ ) for GANs for unconditional (left) and conditional (right) generation. All values report FID ↓, where lower is better. The mark “–” indicates that configuration is infeasible, and the mark “–” shows that the method did not converge. Best results for each method are bolded

**收敛速度**（Figure 2）：RealUID 的 FID 演化曲线显示其在约 100k 次迭代后即趋于饱和，而 UID 基线需要约 300k 次迭代。引入真实数据显著加速了蒸馏过程的收敛。

### 失败模式与局限性

1. **扩散模型的通用性不平整**：对于 RealSiD 扩展，当 α_SiD=1.2 时引入真实数据可能导致训练不稳定或性能下降，说明 RealUID 框架在扩散模型上的通用性并非完全平滑，需要针对特定模型调整系数。

2. **系数选择依赖网格搜索**：α 和 β 的最优值在不同数据集和任务间需要重新搜索，缺少自适应机制。当前实验仅在 CIFAR-10 和 CelebA 上进行了验证，扩展到新数据集时需要额外的调参成本。

3. **受限于教师模型能力**：RealUID 学到的生成器质量上限由教师模型决定，在教师覆盖不足的数据区域改进有限。这解释了为何 RealUID 无法超越教师模型的 FID。

4. **实验规模受限**：当前实验仅在较小数据集（CIFAR-10, CelebA）和轻量 UNet 架构上验证，尚未在 ImageNet 等大规模数据集或 DiT/U-ViT 等大主干网络上测试。桥匹配和随机插值模型的 RealUID 蒸馏也尚未进行实验验证，其实际训练稳定性和提升幅度有待确认。

### 关键图表结论

- **Table 1**：β/α 是控制真实数据利用的核心旋钮，β/α = 0.98 或 1.02 在多数 α 配置下均显著优于不使用真实数据的基线（β/α = 1）。
- **Table 2**：RealUID 在无条件和条件生成下均优于 UID 基线，且微调后的 RealUID 在条件生成上超越了 UID+GAN。
- **Figure 2**：RealUID 的收敛速度明显快于 UID 基线，约 3× 加速达到饱和。
- **Table 5**：RealUID 在推理速度、参数量和显存占用上均优于 FGM/SiD，体现了轻量架构的效率优势。
- **Table 8**：在 CelebA 长微调设定下，RealUID 达到与 UID+GAN 相当的 FID，验证了无 GAN 真实数据融入的有效性。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_8NuN5UzXLC/figures/008_Table_3.jpg]]
*Table 3: Comparison of unconditional generation on CIFAR-10. The best method under the FID metric in each section is highlighted with bold. Table 4: Comparison of conditional generation on CIFAR-10. The best method under the FID metric in each section is highlighted with bold*

## 定位与知识库关联

### 1. 匹配模型蒸馏的演进脉络

RealUID 的提出建立在两条相互交织的研究线索之上：**匹配模型的统一理论**与**无数据蒸馏方法的相继出现**。

**匹配模型的统一视角。** 扩散模型、流匹配和桥匹配虽起源于不同动机，但在数学上共享一个通用框架：它们都通过构造从数据分布 $p_0$ 到噪声分布 $p_T$ 的概率路径 $p_t$，并学习一个条件函数 $f_t^{p_0}(x_t|x_0)$ 来近似该路径的动力学。论文将这一框架形式化为 **Universal Matching (UM) loss**（定义见 §2.2），使得分数函数、条件向量场和桥匹配的漂移项均可被统一表示为同一个损失函数的最小化问题。这一统一视角构成了后续所有蒸馏方法可被纳入同一理论框架的基石。

**数据自由蒸馏方法的相继出现。** 在匹配模型的多步采样推理成本问题驱动下，一系列针对特定模型框架的蒸馏方法被提出：

- **FGM (Flow Generator Matching)**（Huang et al., 2024）面向流匹配模型，将教师的条件向量场 $u_t^*$ 蒸馏到单步生成器 $G_\theta$ 中，其核心是最小化教师与学生函数在学生生成分布 $p_t^\theta$ 上的 $\ell_2$ 距离。该方法完全依赖学生自身生成的数据，不使用真实数据。

- **SiD (Score Identity Distillation)**（Zhou et al., 2024b）面向扩散模型，通过引入参数 $\alpha_{\text{SiD}}$ 将分数蒸馏损失转化为可处理的形式，本质上也是在学生生成分布上最小化教师分数 $s_t^*$ 与学生分数 $s_t^\theta$ 的加权 $\ell_2$ 距离。

- **IBMD (Inverse Bridge Matching Distillation)**（Gushchin et al., 2025）将类似思路扩展到桥匹配模型，同样遵循数据自由范式。

这三类方法的共同瓶颈是：**蒸馏过程完全封闭在学生自身的生成分布中，无法触及真实数据分布**。当学生分布与真实数据分布存在偏差时，教师函数在真实数据区域的知识无法被有效传递。

**GAN 增强路线的代价。** 为突破上述瓶颈，**UID + GAN**（Zhou et al., 2024a）在 FGM/SiD 的蒸馏损失上附加了对抗训练分支：引入一个时间条件判别器 $D_t$ 来区分真实数据与生成数据在加噪过程中的分布差异，并将对抗损失 $\mathcal{L}_{\text{adv}}$ 与蒸馏损失线性组合。这一方案确实能利用真实数据，但代价是引入了额外的判别器网络、对抗损失权重调优以及 GAN 训练固有的不稳定性。

### 2. RealUID 在谱系中的定位：统一与超越

RealUID 的核心贡献并非在现有方法之外另起炉灶，而是通过**理论统一**与**机制创新**实现了对前述所有方法的涵盖与超越。

**理论统一：逆优化视角与线性化技巧。** RealUID 首先揭示了 FGM、SiD、IBMD 在数学上的同源性。论文利用恒等式 $\|a\|^2 = \max_b \{-\|b\|^2 + 2\langle b, a\rangle\}$ 将原本不可直接计算的教师-学生 $\ell_2$ 距离转化为可处理的 min-max 优化问题：

$$\min_\theta \max_f \left\{ \mathcal{L}_{\text{UID}}(f, p_0^\theta) := \mathcal{L}_{\text{UM}}(f^*, p_0^\theta) - \mathcal{L}_{\text{UM}}(f, p_0^\theta) \right\}$$

其中 $f$ 作为可训练的“虚假模型”在最大化步骤中恢复教师与学生函数的距离（Lemma 1），而生成器 $\theta$ 在最小化步骤中缩小该距离。这一形式不仅统一了前述三种方法（它们均可视为 UID 在特定参数化下的特例），还揭示了这些方法与**逆优化**（inverse optimization）的深层联系：蒸馏本质上是在寻找一个生成器参数 $\theta^*$，使得教师函数 $f^*$ 成为该生成分布下 UM loss 的最优解。

**机制创新：无需 GAN 的真实数据融入。** 在 UID 框架下，RealUID 通过重新设计 UM loss 实现了天然的真实数据利用。核心是引入两个系数 $\alpha, \beta \in (0, 1]$，将损失拆分为生成数据项与真实数据项的加权和——即 **RealUM loss**（公式 16）。当 $\alpha = \beta = 1$ 时，RealUM 退化为纯生成数据的 UM loss；当 $\beta/\alpha \neq 1$ 时，真实数据项被激活。将 RealUM 代入 UID 的 min-max 形式即得到 **RealUID loss**（Theorem 2）：

$$\min_\theta \max_f \left\{ \mathcal{L}_{\text{R-UID}}^{\alpha,\beta}(f, p_0^\theta) := \mathcal{L}_{\text{R-UM}}^{\alpha,\beta}(f^*, p_0^\theta) - \mathcal{L}_{\text{R-UM}}^{\alpha,\beta}(f, p_0^\theta) \right\}$$

最大化后的损失等价于学生与教师函数在真实数据分布上的加权 $\ell_2$ 距离（Lemma 2），且权重由 $\beta/\alpha$ 控制。这意味着 **RealUID 在不引入任何判别器或对抗损失的情况下，通过损失函数本身的代数结构实现了真实数据的有效利用**——这是其与 UID+GAN 路线的本质区别。

**方法谱系中的位置总结。** 若以“是否使用真实数据”和“是否依赖 GAN”为坐标轴，现有方法可被清晰定位：

| 方法 | 使用真实数据 | 依赖 GAN | 适用模型 |
|------|:----------:|:-------:|----------|
| FGM (Huang et al., 2024) | ✗ | ✗ | 流匹配 |
| SiD (Zhou et al., 2024b) | ✗ | ✗ | 扩散模型 |
| IBMD (Gushchin et al., 2025) | ✗ | ✗ | 桥匹配 |
| UID + GAN (Zhou et al., 2024a) | ✓ | ✓ | 流匹配/扩散模型 |
| **RealUID (本文)** | **✓** | **✗** | **所有匹配模型** |

RealUID 占据了此前空白的关键位置：同时具备通用性、真实数据利用能力和无需对抗训练的简洁性。

### 3. 适用边界与局限

尽管 RealUID 在理论和实验上展现出优势，其适用性仍存在明确边界：

**数据集与模型规模的验证缺口。** 当前实验仅限于 CIFAR-10（32×32）和 CelebA（64×64）两个较小规模数据集，且采用轻量 UNet 架构（基于 Tong et al., 2024）。论文未在 ImageNet 等更大规模、更高分辨率的数据集上进行验证，也未在 DiT、U-ViT 等现代主干网络上测试。因此，RealUID 在大模型蒸馏场景下的有效性和稳定性尚待证实。

**跨模型类型的实验不完整。** 论文仅完整实现了流匹配模型下的 RealUID 蒸馏流程。对于扩散模型的 RealSiD 扩展，实验显示当 $\alpha_{\text{SiD}} = 1.2$ 时引入真实数据反而可能导致不稳定或性能下降（Figure 5），表明通用性并非完全平整——不同底层模型的动力学差异会影响真实数据融入的效果。桥匹配和随机插值模型的 RealUID 蒸馏尚未进行实验验证。

**系数 $\alpha, \beta$ 的选择依赖网格搜索。** $\beta/\alpha$ 被证明是影响性能的最关键因素（Table 1 消融实验），但其最优值（如 CIFAR-10 上的 0.98 或 1.02）需要通过网格搜索确定，且不同数据集和任务可能需要重新调整。论文未提供自动或自适应的系数选择机制，这在实际部署中增加了调参成本。

**教师模型的能力上限约束。** RealUID 本质上是在教师函数 $f^*$ 的监督下训练学生生成器。若教师模型本身存在系统性误差（例如在数据分布的低密度区域预测不准确），蒸馏得到的学生生成器也将继承这些缺陷。论文在 1D 高斯实验中展示了教师存在偏差时 RealUID 的表现（Figure 4），但未给出更一般的理论保证。

**与基于 KL 散度的方法的互补性未探索。** 以 DMD（Distribution Matching Distillation）为代表的另一类蒸馏方法通过最小化学生与教师分布间的 KL 散度（或其近似）来训练生成器，与 RealUID 基于 $\ell_2$ 函数距离的范式形成互补。两种路线的结合是否可能带来进一步增益，仍是开放问题。

### 4. 开放问题

1. **大规模扩展。** 如何在 DiT、U-ViT 等现代主干网络上实现 RealUID，并验证其在 ImageNet 等高分辨率图像生成任务上的有效性？

2. **自适应系数机制。** 能否设计一种在线调整 $\alpha, \beta$ 的策略，根据训练过程中的分布偏移动态平衡真实数据与生成数据的贡献，从而消除网格搜索的需求？

3. **桥匹配与随机插值模型的验证。** RealUID 在这些模型上的实际训练稳定性、收敛速度和性能提升幅度如何？是否需要针对其特定的条件路径设计调整系数策略？

4. **教师误差下的理论保证。** 当教师模型存在严重误差时，$\beta/\alpha$ 的选择规律是否可以给出更严格的理论刻画，以指导鲁棒的系数设计？

5. **与 DMD 系列方法的融合。** RealUID 的 min-max $\ell_2$ 蒸馏范式与 DMD 的分布匹配范式是否存在统一的视角？二者的结合能否在保持 RealUID 简洁性的同时进一步提升生成质量？

## 原文 PDF

![[paperPDFs/ICLR_2026/Universal_Inverse_Distillation_for_Matching_Models_with_Real_Data_Supervision_No_GANs.pdf]]
