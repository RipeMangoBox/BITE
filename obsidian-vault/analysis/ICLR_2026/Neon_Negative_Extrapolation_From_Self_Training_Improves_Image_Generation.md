---
title: "Neon: Negative Extrapolation From Self-Training Improves Image Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Neon_Negative_Extrapolation_From_Self_Training_Improves_Image_Generation.pdf
openreview_forum_id: kpLRYtPGt3
aliases:
- NNEFST
- Neon
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "负向外推强度 w（控制基模型参数远离自训练退化参数的程度），在自回归模型中常与 CFG 尺度 γ 联合优化。"
primary_logic: "自训练导致的参数退化方向与无限真实数据上的总体梯度呈反方向对齐（anti‑aligned），通过反转这一退化方向（即负向外推），可以更准确地逼近真实数据分布，实现模型性能提升。"
claims:
- "Neon 将 xAR‑L 在 ImageNet‑256 上的 FID 从 1.28 提升至 1.02，仅使用 0.36% 的额外训练计算。"
- "自训练退化梯度与真实数据总体梯度呈反方向对齐（anti‑aligned），而非随机噪声。"
- "模式寻找（mode‑seeking）采样器（如温度 τ<1，top‑k，top‑p，有限步 ODE 求解器）保证梯度反对齐（cos φ < 0），从而确保 Neon 有效。"
- "Neon 无需额外真实数据、辅助模型或推理修改，仅通过简单的后验参数合并即可实现改进。"
---

# Neon: Negative Extrapolation From Self-Training Improves Image Generation

> [!tip] 核心洞察
> 自训练导致的参数退化方向与无限真实数据上的总体梯度呈反方向对齐（anti‑aligned），通过反转这一退化方向（即负向外推），可以更准确地逼近真实数据分布，实现模型性能提升。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Neon：通过自我训练负向外推改进图像生成 |
| 英文题名 | Neon: Negative Extrapolation From Self-Training Improves Image Generation |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=kpLRYtPGt3); [GitHub](https://github.com/VITA-Group/Neon) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Neon (Negative Extrapolation from Self‑Training) |
| Dataset | CIFAR‑10 (EDM‑VP, unconditional), FFHQ‑64 (EDM‑VP, CIFAR‑10 (Flow Matching, ImageNet‑256 (xAR‑L, autoregressive) |

> [!tip] 效果简介
> - CIFAR‑10 (EDM‑VP, unconditional) 上，FID 为 1.38，对比 1.78，变化 −0.40。
> - FFHQ‑64 (EDM‑VP, unconditional) 上，FID 为 1.12，对比 2.39，变化 −1.27。
> - CIFAR‑10 (Flow Matching, unconditional) 上，FID 为 2.32，对比 3.50，变化 −1.18。

## 概述

高质量真实训练数据的稀缺是当前生成模型面临的核心瓶颈。朴素的自训练（self-training）——让模型在自身合成的数据上继续训练——通常会导致模型退化而非提升。然而，Neon 发现了一个反直觉的关键洞察：**自训练导致的参数退化方向并非随机噪声，而是一个与无限真实数据上的总体梯度呈反方向对齐（anti‑aligned）的强信号**。通过反转这一退化方向（即负向外推），可以更准确地逼近真实数据分布，实现模型性能的显著提升。

基于这一洞察，Neon 提出了一种极其简洁的后处理方案：首先生成少量合成数据，在其上对基模型进行极短时间的微调以获得退化参数，然后通过参数合并公式将基模型参数沿退化方向的反方向外推。整个过程无需任何额外真实数据、辅助模型或推理阶段的修改，仅消耗原训练计算预算的不到 1%。

Neon 在扩散模型、流匹配模型、自回归模型和少步生成模型等多个模型家族上均实现了一致的 FID 改善。在 ImageNet‑256 上，Neon 将自回归模型 **xAR‑L**（Ren et al., 2025）的 FID 从 1.28 提升至 1.02，达到该基准的当前最优水平，而额外计算开销仅为原训练的 0.36%。理论分析进一步表明，模式寻找（mode‑seeking）采样器（如温度 τ<1、top‑k、top‑p 等）能够保证合成梯度与真实梯度的反对齐（cos φ < 0），从而确保 Neon 的有效性。

## 背景与动机

### 生成模型的数据瓶颈与自训练的退化悖论

当前最先进的生成模型——无论是扩散模型、流匹配模型还是自回归模型——其性能高度依赖大规模、高质量的真实训练数据。然而，获取此类数据的成本极高，且在许多领域（如医学影像、专业摄影）本身就极度稀缺。这一瓶颈催生了一个自然的替代方案：**自训练（self-training）**——让模型在自身合成的数据上进行微调，期望通过“自我教学”实现迭代提升。

遗憾的是，实践经验反复表明，朴素的自我训练往往导致模型退化而非改进。模型在合成数据上微调后，生成质量不升反降，这一现象在生成建模领域已成为一个公认的困境。传统视角将这种退化视为需要避免的噪声或有害副作用，因此现有方法要么依赖额外的真实数据来“校正”退化，要么引入辅助模型来约束合成数据的分布偏移。

### 核心洞察：退化方向是蕴含改进信息的强信号

本文提出了一个颠覆性的认知反转：**自训练导致的退化并非无意义的噪声，而是一个蕴含改进信息的强信号**。具体而言，作者发现自训练引起的参数退化方向与无限真实数据上的总体梯度方向呈**反方向对齐**（anti-aligned）——即模型在合成数据上“学坏”的方向，恰好指向远离真实数据分布的方向。这一洞察的关键推论是：如果能够反转这一退化方向，即沿着退化方向的反方向更新模型参数，就有可能更准确地逼近真实数据分布，从而实现模型性能的提升。

这一思想可以用一个简单的二维高斯玩具示例直观说明（Figure 2）：在参数空间中，沿合成数据微调方向（$w_s>0$）移动会导致模型与真实数据分布之间的 Wasserstein 距离急剧增大；而沿该方向的反方向（$w_s<0$）移动，则能实现与使用四倍真实数据微调相当的改进效果。合成退化与真实改进在参数空间中指向相反的方向。

### 现有方法的缺口

当前主流的生成模型改进策略存在明显局限：

- **数据驱动方法**：依赖额外真实数据的采集或增强，成本高昂且不可扩展。
- **模型驱动方法**：引入辅助判别器、教师模型或复杂训练策略（如对抗训练、知识蒸馏），增加了训练复杂度和计算开销。
- **自训练方法**：尽管直觉上有吸引力，但直接应用通常导致模型崩溃或质量退化，缺乏有效的利用方式。

这些方法均未能利用自训练退化方向中蕴含的结构化信息。Neon 的提出正是为了填补这一缺口：**通过一个简单的后验参数合并操作，将自训练的“副作用”转化为模型的“改进动力”**，无需任何额外真实数据、辅助模型或推理阶段的修改。

## 核心创新

### 1. 瓶颈反转：从模型退化中提取改进信号

高质量真实训练数据的稀缺性是当前生成模型面临的核心瓶颈。朴素的自训练（self-training）——即模型在自己的合成数据上继续训练——已被广泛观察到会导致模型退化（model degradation），表现为性能指标（如 FID）显著恶化。**Neon 的核心洞察在于：这一退化并非随机噪声，而是一个蕴含强改进信号的方向**——自训练导致的参数退化方向与无限真实数据上的总体梯度呈**反方向对齐**（anti-aligned）。

具体而言，设基模型参数为 $\theta_r$，在合成数据集 $S$ 上微调后得到的退化参数为 $\theta_s$，则退化方向为 $\theta_s - \theta_r$。Neon 证明，当使用模式寻找（mode-seeking）采样器生成合成数据时，该退化方向与真实数据总体梯度方向满足：

$$s := \langle r_d, P r_s \rangle < 0$$

其中 $r_d$ 为真实数据风险梯度，$r_s$ 为合成数据风险梯度，$P$ 为预条件矩阵。**$s < 0$ 意味着两个梯度方向相反**——这正是 Neon 能够通过反转退化方向来改善模型的理论基础。

### 2. 负向外推：简单而高效的参数合并机制

基于上述洞察，Neon 提出了一个极其简洁的参数更新公式——**负向外推**（negative extrapolation）：

$$\theta_{\mathrm{Neon}} = \theta_r - w(\theta_s - \theta_r) = (1+w)\theta_r - w\theta_s, \quad w > 0$$

其中 $w$ 为负向外推强度，控制基模型参数远离自训练退化参数的程度。**这一操作仅需一次简单的后验参数合并（post-hoc parameter merge），无需任何额外真实数据、辅助模型或推理阶段的修改**。

Neon 的完整流程仅包含三个步骤（Algorithm 1）：
1. **合成数据生成**：使用基模型的推断程序生成固定大小的合成数据集 $S$；
2. **退化微调**：在合成数据集 $S$ 上以极低学习率微调基模型，获得退化参数 $\theta_s$；
3. **负向外推合并**：通过上述公式合并基模型与退化模型，得到最终模型 $\theta_{\mathrm{Neon}}$。

### 3. 模式寻找采样器：保证梯度反对齐的充分条件

Neon 有效性的关键前提是合成梯度与真实梯度呈反方向对齐（$s < 0$）。论文从理论上证明，**模式寻找采样器是保证这一反对齐的充分条件**。

定义模式寻找采样器为对模型密度进行单调非递减重加权的采样过程：

$$q(x) \propto f(\log p_{\theta_r}(x)) \, p_{\theta_r}(x), \quad f \text{ 非递减}$$

此类采样器包括实践中广泛使用的**低温采样（$\tau < 1$）、top-k 采样、top-p 采样以及有限步 ODE 求解器**。理论分析表明（Theorem 2），当采样器为模式寻找时，在 Hessian 诱导的几何空间中，模型误差 $\varepsilon$ 与采样器偏差 $b$ 之间的夹角余弦满足：

$$\cos \varphi < 0$$

这直接保证了 $s < 0$，从而确保 Neon 的负向外推能够降低真实数据风险。实验验证（Figure B.2–B.3）进一步确认：模式寻找采样器（$\zeta > 1$）的最优 $w > 0$（Neon 有效），而多样性寻找采样器（$\zeta < 1$）的最优 $w < 0$（此时自训练本身有益）。

### 4. 与基线方法的关键差异

| 变更维度 | 基线方法 | Neon |
|---------|---------|------|
| **参数更新方向** | 标准梯度下降：沿合成损失梯度方向 $\theta_s - \theta_r$ | 负向外推：沿合成损失梯度的反方向 $-w(\theta_s - \theta_r), w > 0$ |
| **数据依赖** | 依赖大量高质量真实数据 | 仅需基模型自身合成的数据，无需额外真实数据 |
| **计算开销** | 完整训练流程 | 仅需极小额外计算（通常 $<1\%$ 原训练预算） |
| **模型架构** | 单一架构 | 支持跨架构合成数据迁移（Figure 8） |

### 5. 自回归模型中的联合优化

在自回归模型中，Neon 的外推强度 $w$ 与无分类器引导（CFG）尺度 $\gamma$ 存在互补关系：$w$ 增加召回但牺牲精度，$\gamma$ 则相反。因此，Neon 在自回归模型上采用 **$(w, \gamma)$ 联合优化**策略，通过网格搜索找到最优组合。实验表明，单独调整任一参数均无法达到最佳 FID（Figure 6），联合优化是释放 Neon 全部潜力的关键。

## 整体框架

Neon 的核心流程极其简洁，仅由三个顺序模块构成，无需额外真实数据、无需辅助模型、无需修改推理过程。其整体管线如下：

### 合成数据生成

使用基模型 $G_{\theta_r}$ 的**标准推断程序**（包括其默认的采样器配置，如无分类器引导尺度、温度、ODE 求解器步数等），生成一个固定大小的合成数据集 $\mathcal{S}$。该数据集是后续所有操作的唯一数据来源——Neon 全程不接触任何真实数据。

### 退化微调

在合成数据集 $\mathcal{S}$ 上，以**极低学习率**对基模型进行短暂微调（通常仅需原训练预算的 $<1\%$），获得退化参数 $\theta_s$。这一步骤的目的并非让模型在合成数据上表现良好，而是**精确提取自训练导致的参数退化方向**。该退化方向 $\theta_s - \theta_r$ 是 Neon 方法的核心信号载体。

### 负向外推合并

通过简单的后验参数合并公式，将基模型参数沿退化方向的**反方向**进行外推：

$$\theta_{\mathrm{Neon}} = \theta_r - w(\theta_s - \theta_r) = (1+w)\theta_r - w\theta_s, \quad w > 0$$

其中 $w$ 为**负向外推强度**，控制基模型远离退化参数的程度。当 $w=0$ 时恢复基模型；$w>0$ 时进入 Neon 的有效外推区域；$w=-1$ 则退化为直接使用自训练模型 $\theta_s$。

### 关键因果机制

Neon 有效的根本原因在于一个被实验和理论双重验证的**反对齐（anti-alignment）现象**：自训练导致的参数退化方向 $\theta_s - \theta_r$ 与无限真实数据上的总体梯度方向呈**反方向对齐**（即 $\cos\varphi < 0$）。这意味着，反转退化方向等价于沿真实数据改进方向更新参数。论文通过泰勒展开证明了这一点：

$$\mathcal{R}_{\mathrm{data}}(\theta_{\mathrm{Neon}}) = \mathcal{R}_{\mathrm{data}}(\theta_r) + w\alpha s + \frac{(w\alpha)^2}{2} r_s^{\top} P^{\top} \nabla^2 \mathcal{R}_{\mathrm{data}}(\theta_r) P r_s + O((w\alpha)^3)$$

其中对齐量 $s := \langle r_d, P r_s \rangle$ 为真实数据梯度与合成梯度的预条件内积。当 $s < 0$ 时，线性项为负，对于较小的 $w>0$ 即可保证真实风险下降。

### 模式寻找采样器的保证

反对齐并非偶然现象。论文在 Theorem 2 中证明：当采样器是**模式寻找（mode‑seeking）**的——即采样分布可写为 $q(x) \propto f(\log p_{\theta_r}(x)) p_{\theta_r}(x)$，其中 $f$ 为非递减函数——时，模型误差 $\varepsilon$ 与采样器偏差 $b$ 在 Hessian 诱导几何中的夹角满足 $\cos\varphi < 0$，从而保证 $s < 0$，Neon 有效。实践中，温度 $\tau < 1$、top‑k、top‑p 采样、有限步 ODE 求解器、无分类器引导等常用技术均自然满足这一条件。

### 自回归模型的联合优化

对于自回归生成模型（如 **xAR**，Ren et al., 2025；**VAR**，Tian et al., 2024），Neon 需与无分类器引导尺度 $\gamma$ 联合优化。这是因为 $w$ 通过牺牲精度换取召回来改善 FID，而 $\gamma$ 的作用方向恰好相反（提升精度、降低召回）。两者协同调节可实现单一参数无法达到的最优精度‑召回平衡点。

### 输入输出总结

- **输入**：已训练好的基模型 $G_{\theta_r}$（及其标准推断配置）
- **中间产物**：合成数据集 $\mathcal{S}$，退化模型 $\theta_s$
- **输出**：Neon 增强模型 $\theta_{\mathrm{Neon}}$，可直接用于推理，无需任何额外修改
- **可调超参数**：外推强度 $w$（以及自回归模型中的 CFG 尺度 $\gamma$），通常通过小范围网格搜索确定

## 核心模块与公式推导

Neon 的核心流程由三个顺序执行的模块构成，整体计算开销极低（通常小于原始训练预算的 1%），且无需额外真实数据或辅助模型。

**模块一：合成数据生成**

使用基模型 $ \theta_r $ 的推断程序，采样生成一个固定大小的合成数据集 $ \mathcal{S} $。该步骤的关键约束在于采样器必须是**模式寻找（mode‑seeking）**类型——即倾向于生成模型已有把握的样本，而非探索低概率区域。实践中，这对应于使用无分类器引导（CFG）尺度 $ \gamma > 1 $、温度 $ \tau < 1 $、top‑k/top‑p 截断，或有限步 ODE 求解器等策略。这一约束是 Neon 有效性的理论前提：模式寻找采样器保证了合成梯度与真实数据总体梯度的**反方向对齐**（anti‑alignment），使得后续的负向外推能够真正逼近真实分布。

**模块二：退化微调**

在合成数据集 $ \mathcal{S} $ 上，以极低学习率对基模型 $ \theta_r $ 进行短暂微调，获得退化参数 $ \theta_s $。微调预算 $ B $（以百万张图像计）通常极小——例如 EDM‑VP 上 $ B \leq 3\text{M} $，仅占基模型训练计算的 $ \leq 2\% $。微调产生的参数位移 $ \theta_s - \theta_r $ 并非随机噪声，而是沿合成损失梯度方向的确定性退化。理论分析表明，在短时微调近似下：

$$ \theta_s = \theta_r - \alpha P r_s + O(\alpha^2) $$

其中 $ \alpha $ 为学习率，$ P $ 为预条件矩阵，$ r_s $ 为合成数据上的梯度。该退化方向正是 Neon 后续利用的核心信号。

**模块三：负向外推合并**

通过简单的后验参数合并公式，将基模型参数沿退化方向的反方向外推：

$$ \theta_{\mathrm{Neon}} = \theta_r - w(\theta_s - \theta_r) = (1+w)\theta_r - w\theta_s, \quad w > 0 $$

其中 $ w $ 为**负向外推强度**，是 Neon 的核心调控旋钮。当 $ w = 0 $ 时退化为基模型；$ w = -1 $ 时等价于直接使用退化模型 $ \theta_s $；$ w > 0 $ 时进入负向外推区间，Neon 在此区间实现性能提升。

**关键公式：真实数据风险的泰勒展开**

为理解 $ w > 0 $ 为何有效，将 Neon 合并后的真实数据风险在 $ \theta_r $ 处展开：

$$ \mathcal{R}_{\mathrm{data}}(\theta_{\mathrm{Neon}}) = \mathcal{R}_{\mathrm{data}}(\theta_r) + w\alpha s + \frac{(w\alpha)^2}{2} r_s^{\top} P^{\top} \nabla^2 \mathcal{R}_{\mathrm{data}}(\theta_r) P r_s + O((w\alpha)^3) $$

其中**梯度对齐量** $ s := \langle r_d, P r_s \rangle $ 是决定性的量。$ r_d $ 为真实数据梯度，$ r_s $ 为合成数据梯度。当 $ s < 0 $（即反方向对齐）时，线性项 $ w\alpha s $ 为负，对于足够小的 $ w > 0 $，该负项主导展开式，保证风险严格下降。这正是 Neon 有效性的数学根源。

**对齐量的几何解释**

在 Hessian 矩阵 $ H_d = \nabla^2 \mathcal{R}_{\mathrm{data}}(\theta_r) $ 诱导的几何空间中，对齐量 $ s $ 的符号由模型误差 $ \varepsilon = \theta_r - \theta^* $ 与采样器偏差 $ b $ 之间的夹角决定：

$$ \cos \varphi := \frac{\langle \varepsilon, H_d^{-1} b \rangle_{H_d}}{\|\varepsilon\|_{H_d} \|H_d^{-1} b\|_{H_d}} \in [-1,1] $$

模式寻找采样器（如 CFG $ \gamma > 1 $）保证 $ \cos \varphi < 0 $，从而确保 $ s < 0 $，Neon 有效。反之，多样性寻找采样器（如温度 $ \tau > 1 $）会导致 $ \cos \varphi > 0 $，此时需切换为插值（$ w < 0 $）才能受益，但此类采样器在实践中极少使用。

**自回归模型中的联合优化**

对于自回归生成模型（如 xAR、VAR），Neon 的外推强度 $ w $ 与 CFG 尺度 $ \gamma $ 存在互补关系：$ w $ 通过牺牲精度换取召回提升，而 $ \gamma $ 的作用恰好相反。因此，评估时需对 $ (w, \gamma) $ 进行联合网格搜索以达到最优 FID。这是 Neon 在自回归模型上的唯一额外调优需求，其余流程与扩散/流模型完全一致。

## 实验与分析

### 核心结果：跨架构、跨范式的普适提升

Neon 在扩散模型、流匹配模型、自回归模型和少步生成模型上均表现出稳定的 FID 改善，且所需额外计算开销极小。图 3 和表 A.1 汇总了主要基准结果。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_kpLRYtPGt3/figures/003_Figure_3.jpg]]
*Figure 3: Neon consistently improves FID with minimal self-training overhead. Minimum FID (optimized over extrapolation strength w) vs. self-training budget B (millions of images seen during fine-tuning on S) for varying synthetic dataset sizes |S|, on EDM-VP (CIFAR-10/FFHQ-64) and flow matching (CIFAR-10). Optimal gains use B $\leq$ 3 ${ \mathrm { M i } }$ \ K 2% of base model training compute for $\mathrm { E D M }$ ; < 3 \% for flow), confirming Neon’s efficiency. $\mathbf { A } \mathbf { t }$ \ $\boldsymbol { B }$ = 0 , , FID reflects the base model (no Neon)

**扩散与流匹配模型。** 在 CIFAR‑10 无条件生成任务上，Neon 将 EDM‑VP（Karras et al., 2022）的 FID 从 1.78 降至 1.38（仅使用 6k 合成样本，额外训练计算量约 1.75%）；在 FFHQ‑64 上，FID 从 2.39 降至 1.12（18k 样本，额外计算约 0.85%）。对于 Flow Matching 基线（Tong et al., 2023/2024），CIFAR‑10 上的 FID 从 3.50 降至 2.32（25k 样本，额外计算约 3.2%）。值得注意的是，最优 FID 通常在微调预算 $B \leq 3$M（即基模型训练计算量的 ≤2%）时即可达到，验证了 Neon 的高效性。

**自回归模型。** 在 ImageNet‑256 上，Neon 将 xAR‑L（Ren et al., 2025）的 FID 从 1.28 推至 1.02，达到当时最优水平，额外计算仅占原训练的 0.36%（图 1、图 5）。xAR‑B 的 FID 从 1.72 降至 1.31。对于 VAR‑d16（Tian et al., 2024），FID 从 3.30 降至 2.01；在 ImageNet‑512 上，VAR‑d30 同样获得显著改善。自回归模型中，Neon 需联合优化外推强度 $w$ 和 CFG 尺度 $\gamma$：$w$ 通过牺牲精度换取召回提升，而 $\gamma$ 的作用相反，二者互补才能达到最优 FID（图 6）。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_kpLRYtPGt3/figures/005_Figure_5.jpg]]
*Figure 5: Neon consistently improves autoregressive models across architectures and resolutions. We plot the minimum FID (optimized over merge weight w and CFG scale γ) versus the fine-tuning budget B for various synthetic dataset sizes |S|. From left: xAR-B and xAR-L on ImageNet-256 (with xAR-L achieving a state-of-the-art 1.02 FID), VAR-d16 on ImageNet-256, and VAR-d30 on ImageNet-512*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_kpLRYtPGt3/figures/006_Figure_6.jpg]]
*Figure 6: Optimal precision-recall trade-offs for VAR-d16 as a function of w and $\gamma$ . Left: Heatmaps for FID, precision, and recall on ImageNet-256 (|S|=750k, B=1.25Mi) from a grid search over w and $\gamma$ . The star marks the best FID ( $w ^ { * } { \approx }$ 1 . 0 , $\bar { \gamma } ^ { * } { \approx }$ 2 . 7 ) achieving FID 2.01, unreachable by either parameter alone. Right: Asymptotic precision-recall curves showing expanded behavioral range through joint tuning

**少步生成模型。** 在 IMM（Zhou et al., 2025a）的 ImageNet‑256 少步推理任务中，Neon 使 4 步推理的 FID 降至 1.69，接近基模型 8 步推理的质量（FID 1.98→1.46），而额外计算开销不足原训练的 0.005%（图 7）。这一结果表明 Neon 可以有效补偿推理步数减少带来的质量损失。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_kpLRYtPGt3/figures/007_Figure_7.jpg]]
*Figure 7: Neon dramatically improves few-step inference for IMM on ImageNet-256. Minimum FID (optimized over w and γ) vs. fine-tuning budget B for different |S|. Synthetic data were generated using T { = } 8 , $\gamma { = }$ 1 . 5 From left: T { = } 1 , 2 , 4 , $\delta$ inference steps. Neon achieves substantial FID reductions with near-zero additional compute (< 0.005% of IMM’s training), with Neon improved model with 4-step nearly matching base model with 8-step generation quality

### 精度‑召回权衡：Neon 为何有效

图 4 揭示了 Neon 改善 FID 的内在机制：随着外推强度 $w$ 从 0 增加，精度单调下降，而召回呈倒 U 形曲线并在 FID 最优处附近达到峰值。这表明 Neon 通过将概率质量从过度表达的模态重新分配到覆盖不足的模态，以精度换取召回，从而实现净 FID 改善。该模式在 EDM‑VP（CIFAR‑10/FFHQ‑64）和 Flow Matching 上一致出现（图 D.1）。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_kpLRYtPGt3/figures/004_Figure_4.jpg]]
*Figure 4: Neon trades precision for recall, yielding net FID improvement. For the EDM-VP model trained on CIFAR-10, we plot the FID, precision, and recall vs. negative extrapolation strength w for various training budgets B. w = - 1 corresponds to the model directly trained on synthetic data, i.e., $\theta _ { \mathrm { N e o n } } = \theta _ { s }$ w = 0 corresponds to the base model, i.e., $\theta _ { \mathrm { N e o n } } = \theta _ { r }$ . w > 0 corresponds to the negative extrapolation regime where Neon demonstrates its improvement capability. In each case, ${ \bf \hat { \alpha } } | { \cal$ S } | = 6 ${ \bf$ k }

### 消融研究：鲁棒性与可迁移性

**跨架构合成数据迁移。** Neon 的退化方向信号具有跨架构可迁移性：使用 IMM 或 Flow Matching 模型生成的合成数据微调 EDM‑VP，仍能有效改善后者，FID 分别达到 1.80 和 1.59（自架构为 1.38，图 8）。这表明退化方向捕捉的是数据分布层面的偏差，而非特定架构的产物。

**基模型质量鲁棒性。** 即使在远未收敛的基模型上（例如仅用 30k 真实样本训练的 EDM‑VP），Neon 仍能带来显著提升，使其 FID 接近使用 50k 真实样本训练的基线水平（图 9）。这说明 Neon 不要求基模型接近最优。

**合成数据质量鲁棒性。** 当用于生成合成数据的 CFG 尺度在 [1, 3] 范围内变化时，Neon 的最终 FID 稳定在 1.30–1.31（图 10）。即使合成数据质量差异显著，Neon 仍能从中提取有效的反方向校正信号。

### 失败模式与边界条件

1. **多样性寻找采样器下失效。** 理论分析和验证实验（图 B.2、B.3）表明，当使用多样性寻找采样器（如温度 $\tau > 1$ 的自回归采样）时，合成梯度与真实梯度呈正向对齐（$\cos\varphi > 0$），此时 Neon 的负向外推（$w > 0$）反而有害，最优策略变为正向插值（$w < 0$，即普通自训练）。好在实践中绝大多数生成模型默认使用模式寻找采样器。

2. **合成数据集大小的 U 形特性。** 实验显示 FID 与合成数据集大小 $|S|$ 呈 U 形关系：过小的 $|S|$ 受方差限制，退化方向估计噪声大；过大的 $|S|$ 则放大曲率效应，导致外推越过最优解。不同模型的最优 $|S|$ 需小幅搜索，通常在数千到数十万样本量级。

3. **外推强度 $w$ 需调优。** 尽管 $w$ 的 U 形性能曲线使最优值易于定位，但当前仍需进行小范围网格搜索或联合优化（自回归模型中还需联合优化 $\gamma$）。尚未实现完全自动的最优参数确定。

4. **模态限制。** 所有实验均在图像生成任务上完成，Neon 在文本、音频等其他模态的有效性尚未验证，需进一步研究。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_kpLRYtPGt3/figures/011_Table.jpg]]
*Table: (a) Results on CIFAR-10. (b) Results on FFHQ-64×64. (c) Results on ImageNet-256×256. (d) Results on ImageNet-512×512*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_kpLRYtPGt3/figures/016_Figure.jpg]]
*Figure: D.1: Neon’s precision-recall trade-off across diffusion and flow matching architectures. FID, precision, and recall as functions of merge weight w for EDM-VP on FFHQ-64 with | \mathcal { S } | = 1 8 \mathrm { k } (top row) and Flow Matching on CIFAR-10 with | \bar { \cal S } | = 2 5 \mathrm { k } (bottom row), shown across different fine-tuning budgets B. Both architectures exhibit the characteristic pattern: FID reaches a minimum at intermediate w values, precision monotonically decreases, and recall follows an inverted-U curve peaking near the FID optimum*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_kpLRYtPGt3/figures/014_Figure.jpg]]
*Figure: B.2: FID vs. Merge Weight (w) validation. For the mode-seeking sampler ( \zeta = 1 . 1 ) , the optimal FID is at w > 0 (Neon helps). For the diversity-seeking sampler ( \zeta = 0 . 9 ) , the optimum is at w < 0 (self-training helps)*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_kpLRYtPGt3/figures/021_Figure.jpg]]
*Figure: w= - 1.0 w= 0.0 w= 1.0 w=2.0 w= 3.0 w= 4.0 w= 5.0 Figure H.2: Effect of negative extrapolation weight w and CFG scale γ on IMM generation quality for ImageNet class 980 (valley). Each 2×2 grid shows four random samples for a given (w, γ) configuration for snapshot of model at B = 1.95 (Mi) for |S| = 30k. w=-1.0 w= 0.0 w=1.0 w=2.0 w=3.0 w=5.0 Figure H.3: Effect of negative extrapolation weight w and CFG scale γ on IMM generation quality for ImageNet class 14 (indigo bunting). Each 2×2 grid shows four random samples for a given (w, γ) configuration for snapshot of model at B = 1.95 (Mi) for |S| = 30k*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_kpLRYtPGt3/figures/022_Figure.jpg]]
*Figure: w= - 1.0 w= 0.0 w= 1.0 w=2.0 w= 3.0 w= 4.0 w= 5.0 Figure H.4: Effect of negative extrapolation weight w and CFG scale γ on IMM generation quality for ImageNet class 281 (tabby cat). Each 2×2 grid shows four random samples for a given (w, γ) configuration for snapshot of model at B = 1.95 (Mi) for |S| = 30k. Figure H.5: Effect of negative extrapolation weight w and CFG scale γ on IMM generation quality for ImageNet class 511 (container ship). Each 2×2 grid shows four random samples for a given (w, γ) configuration for snapshot of model at B = 1.95 (Mi) for | S | = 3 0 \mathbf { k }*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_kpLRYtPGt3/figures/023_Figure.jpg]]
*Figure: w=2.0 Figure H.6: Effect of negative extrapolation weight w and CFG scale γ on IMM generation quality for ImageNet class 928 (ice cream). Each 2×2 grid shows four random samples for a given (w, γ) configuration for snapshot of model at B = 1.95 (Mi) for |S| = 30k. Figure H.7: Effect of negative extrapolation weight w and CFG scale γ on IMM generation quality for ImageNet class 404 (airliner). Each 2×2 grid shows four random samples for a given (w, γ) configuration for snapshot of model at B = 1.95 (Mi) for | S | = 3 0 \mathbf { k }*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_kpLRYtPGt3/figures/025_Figure.jpg]]
*Figure: w = 0.5 w = 0.0 w = 0.25 w = 0.5 w = 0.75 w = 1 Figure I.2: Effect of negative extrapolation weight w and CFG scale γ on VAR-d36-s generation quality for ImageNet class 609 (jeep). Each 2×2 grid shows four random samples for a given (w, γ) configuration for snapshot of model at B = 1.20 (Mi) for |S| = 90k. Figure I.3: Effect of negative extrapolation weight w and CFG scale γ on VAR-d36-s generation quality for ImageNet class 113 (snail). Each 2×2 grid shows four random samples for a given (w, γ) configuration for snapshot of model at B = 1.20 (Mi) for |S| = 90k*

## 方法谱系与知识库定位

### 与基线的关系

Neon 并非一个独立的生成模型，而是一种**后验参数修正策略**，可叠加于现有生成模型之上。其核心操作对象是基模型参数 $\theta_r$ 和自训练退化参数 $\theta_s$，通过公式 $\theta_{\mathrm{Neon}} = (1+w)\theta_r - w\theta_s$（$w>0$）完成负向外推合并。这一机制决定了 Neon 与以下基线方法的关系：

**扩散模型基线。** Neon 在 **EDM-VP**（Karras et al., 2022）上进行了验证：CIFAR-10 无条件生成 FID 从 1.78 降至 1.38，FFHQ-64 从 2.39 降至 1.12。Neon 不修改 EDM-VP 的扩散过程或采样器，仅在参数层面进行后验合并，额外计算开销仅为原训练预算的 0.85%–1.75%。

**流匹配基线。** 在 **Flow Matching**（Tong et al., 2023/2024）上，CIFAR-10 FID 从 3.50 降至 2.32，额外计算开销约 3.2%。Neon 对连续归一化流同样有效，表明其机制不依赖扩散模型特有的去噪目标。

**自回归模型基线。** 在 **xAR**（Ren et al., 2025）和 **VAR**（Tian et al., 2024）上，Neon 需联合优化外推强度 $w$ 和 CFG 尺度 $\gamma$。xAR-L 在 ImageNet-256 上 FID 从 1.28 降至 1.02（SOTA），仅消耗 0.36% 额外训练计算；VAR-d16 从 3.30 降至 2.01。这类模型中，$w$ 和 $\gamma$ 形成互补的精度‑召回调节杠杆：$w$ 牺牲精度换取召回，$\gamma$ 则相反，联合优化是达到最优 FID 的关键。

**少步生成基线。** 在 **IMM**（Zhou et al., 2025a）上，Neon 使 4 步推理的 FID（1.69）接近原 8 步推理质量（1.98），额外计算开销低于 0.005% 原训练预算。这表明 Neon 的退化方向信号对蒸馏类模型同样有效。

### 方法谱系定位

Neon 在生成模型改进方法的谱系中占据一个独特位置，其定位可从以下维度理解：

**数据增强 vs. 参数外推。** 传统方法通过获取更多真实数据或利用合成数据增强训练集来提升模型。朴素自训练（直接使用合成数据微调）因模型误差与采样偏差的相互作用导致退化。Neon 的洞察在于：**退化方向本身并非噪声，而是与真实数据总体梯度呈反方向对齐（anti-aligned）的强信号**。通过反转这一方向（即负向外推），Neon 将退化转化为改进，无需任何额外真实数据。

**辅助模型 vs. 单模型自举。** 许多生成模型改进方案依赖辅助判别器、教师模型或多模型集成。Neon 仅需基模型自身及其自训练退化版本，不引入任何辅助模型，也不修改推理过程。这是一种极简的自举式改进策略。

**模式寻找采样器的理论保证。** Neon 有效性的理论前提是使用模式寻找（mode-seeking）采样器——包括低温采样（$\tau<1$）、top-k、top-p 以及有限步 ODE 求解器。Theorem 2 证明：当采样器满足 $q(x) \propto f(\log p_{\theta_r}(x)) p_{\theta_r}(x)$ 且 $f$ 非递减时，模型误差 $\varepsilon$ 与采样器偏差 $b$ 在 Hessian 诱导几何中的夹角满足 $\cos\varphi < 0$，从而保证梯度反对齐（$s < 0$）。该定理将 Neon 的有效性条件与采样器的模式寻找特性建立了因果联系。

**与普通自训练的对称性。** 当采样器为多样性寻找（diversity-seeking，如 $\tau>1$）时，$\cos\varphi > 0$，梯度正向对齐，此时普通自训练（$w<0$ 的插值）反而有益。这一对称性在验证实验中得到确认（Figure B.2）：$\zeta=1.1$（模式寻找）时最优 $w>0$（Neon 有效），$\zeta=0.9$（多样性寻找）时最优 $w<0$（自训练有效）。由于实践中生成模型几乎普遍采用模式寻找采样器，Neon 的默认设置（$w>0$）具有广泛适用性。

### 适用边界与局限

**采样器类型约束。** Neon 的理论保证和实验验证均基于模式寻找采样器。对于多样性寻找采样器，需切换为 $w<0$ 的插值策略才能受益，但此类采样器在实践中极少出现。这一约束并非 Neon 的固有缺陷，而是其理论框架的边界条件。

**模态局限。** 所有实验均在图像生成任务上完成（CIFAR-10、FFHQ-64、ImageNet-256/512），涵盖扩散、流匹配、自回归、少步生成四种架构家族。Neon 在文本、音频等其他模态中的有效性尚未验证，跨模态迁移是待探索的开放问题。

**超参数调优需求。** 外推强度 $w$（以及自回归模型中的 CFG 尺度 $\gamma$）仍需进行小范围网格搜索。尽管 $w$ 与 FID 之间呈现 U 形关系，可通过少量评估快速定位最优值，但尚未实现完全自动化的超参数确定方法。

**极端基模型质量。** 虽然 Neon 对基模型质量表现出较强鲁棒性（Figure 9 显示，仅用 30k 真实样本训练的远未收敛模型仍能从中显著受益），但极端糟糕的基模型（例如随机初始化附近的模型）可能无法提供有意义的退化方向信号，改善幅度有限。

**合成数据规模的 U 形特性。** 实验揭示合成数据集大小 $|S|$ 与最终性能之间呈 U 形关系：过小的 $|S|$ 受方差限制，过大的 $|S|$ 放大曲率效应。这一特性意味着 $|S|$ 需要根据具体模型和任务进行适度选择，而非越大越好。

### 开放问题

1. **多样性寻找采样器的主动设计。** 能否设计出使合成梯度与真实梯度正向对齐（$s>0$）的采样器，从而使普通自训练本身变得有益？这将翻转 Neon 的逻辑，从“反转退化”变为“利用增强”。

2. **最优劣质数据集的主动合成。** 当前 Neon 使用基模型的标准采样程序生成合成数据。是否可能主动合成“最优劣质”数据集，使其诱导的退化方向能最大化对真实风险的校正信号？这涉及对采样器偏差 $b$ 的主动操控。

3. **跨模态与跨任务推广。** Neon 的负向外推思想能否推广到文本、音频等非图像生成任务，或扩展到判别模型？核心挑战在于验证“自训练退化方向与真实数据梯度反对齐”这一现象在其他模态中是否成立。

4. **无显式微调的退化方向提取。** 在超大规模预训练模型的背景下，是否可以不进行显式的合成数据微调，而是通过分析已有检查点或训练轨迹直接提取退化方向？这将进一步降低 Neon 的计算开销。

5. **统一的自动超参数确定方法。** 对于不同架构家族（扩散/流/自回归/少步生成），是否存在统一的自动确定最优 $w$、$|S|$ 和微调预算 $B$ 的方法？当前这些参数仍需针对每个模型进行独立搜索。

## 原文 PDF

![[paperPDFs/ICLR_2026/Neon_Negative_Extrapolation_From_Self_Training_Improves_Image_Generation.pdf]]
