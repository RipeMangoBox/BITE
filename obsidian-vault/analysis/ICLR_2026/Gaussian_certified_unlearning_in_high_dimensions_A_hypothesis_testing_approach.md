---
title: "Gaussian certified unlearning in high dimensions: A hypothesis testing approach"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Gaussian_certified_unlearning_in_high_dimensions_A_hypothesis_testing_approach.pdf
openreview_forum_id: 0FJYicpOj0
aliases:
- GCUHDHTA
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/privacy_preserving_statistics_and_machine_learning
core_operator: "采用 ε-Gaussian 认证遗忘框架 (GPAR) 和单一牛顿步加高斯噪声的遗忘算法，通过高斯权衡曲线精准校准噪声方差。"
primary_logic: "在高维环境中，高斯认证遗忘是自然的最优认证概念；单步牛顿更新结合精确校准的高斯噪声即可同时实现隐私保护和模型精度，揭示 (φ,ε)-可认证遗忘的次优性。"
claims:
- "单一牛顿更新与精心校准的高斯噪声即可实现 ε-Gaussian 可认证性和渐近消失的泛化误差分化。"
- "噪声方差设置为 R/ε 时，遗忘算法满足 (φ_n, ε)-GPAR。"
- "Zou et al. (2025) 的 (φ,ε)-认证遗忘框架需要至少两步牛顿，而本工作只需一步，揭示了该定义与噪声机制的次优性。"
- "数值实验表明，高斯认证遗忘在 GED 和 UED 上均优于拉普拉斯噪声和 (φ,ε,δ)-认证，特别是在高维 IMDb 数据上。"
---

# Gaussian certified unlearning in high dimensions: A hypothesis testing approach

> [!tip] 核心洞察
> 在高维环境中，高斯认证遗忘是自然的最优认证概念；单步牛顿更新结合精确校准的高斯噪声即可同时实现隐私保护和模型精度，揭示 (φ,ε)-可认证遗忘的次优性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 高维高斯认证遗忘：一种假设检验方法 |
| 英文题名 | Gaussian certified unlearning in high dimensions: A hypothesis testing approach |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=0FJYicpOj0) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/privacy_preserving_statistics_and_machine_learning |
| Method | 基于单步牛顿和高斯噪声的认证遗忘算法 |
| Dataset | synthetic data with ridge logistic regression, IMDb (real-world high-dimensional text data), p=3161, n=1579 |

> [!tip] 效果简介
> - synthetic data with ridge logistic regression 上，GED (Generalization Error Divergence) 为 Gaussian: slopes -0.47, -0.54, -0.51 for m=1,5,10，对比 Laplace: higher slopes，变化 Gaussian GED decays faster and is uniformly lower than Laplace。
> - IMDb (real-world high-dimensional text data), p=3161, n=1579 上，GED 为 Gaussian: lower GED across ε，对比 Laplace and (φ,ε,δ)-certified: higher GED，变化 Gaussian noise yields best accuracy in high-dimensional real data。

## 概述

在高维比例区域（$p \sim n$）中，机器学习遗忘面临一个根本性瓶颈：传统的优化假设——每样本损失的强凸性与光滑性——在该区域中不再成立，而现有的可认证遗忘定义（如 $(\varepsilon,\delta)$-遗忘、Rényi 遗忘和 $(\varphi,\varepsilon)$-遗忘）与高斯噪声机制不相容，导致过度噪声注入和精度损失。本文的核心洞察是：在高维环境中，高斯认证遗忘是最优的自然认证概念。作者提出 $\varepsilon$-Gaussian 认证遗忘框架（GPAR），并证明仅需**单步牛顿更新**结合**精确校准的高斯噪声**，即可同时实现可认证的隐私保护与渐近可忽略的泛化误差退化。

该方法的关键在于高斯权衡曲线 $f_{G,\varepsilon}(\alpha) = \Phi(\Phi^{-1}(1-\alpha)-\varepsilon)$ 的维度无关性：在高维各向同性高斯噪声下，假设检验的难度仅取决于标准化欧氏距离 $\varepsilon$，而与维度 $p$ 无关。这一性质使得噪声方差的校准变得精准——将噪声半径设为 $R/\varepsilon$ 即可满足 $(\varphi_n, \varepsilon)$-GPAR 认证。相比之下，Zou et al. (2025) 的 $(\varphi,\varepsilon)$-认证遗忘框架需要至少两步牛顿更新才能兼顾隐私与精度，而本文揭示该差异源于 $(\varphi,\varepsilon)$-认证定义与噪声机制的次优性，$\varepsilon$-Gaussian 认证能够最优地克服这一局限。

数值实验验证了理论结论：在合成数据和真实高维 IMDb 数据集（$p=3161$, $n=1579$）上，高斯认证遗忘的泛化误差分化（GED）和遗忘数据误差分化（UED）均优于拉普拉斯噪声和 $(\varphi,\varepsilon,\delta)$-认证遗忘，且 GED 随维度 $p$ 增长以 $p^{-0.5}$ 阶衰减，随隐私参数 $\varepsilon$ 增大单调下降。

## 背景与动机

机器学习模型在实际部署中常常需要“遗忘”特定训练样本——例如，当用户依据 GDPR 或 CCPA 等法规要求删除个人数据时。最直接的方式是完全重训练，但在大规模模型上计算代价过高。因此，研究者提出了多种“机器遗忘”算法，试图在不重训练的前提下，从已训练模型中移除指定数据的影响。

然而，可认证遗忘在高维场景下存在一个根本性的瓶颈。现有可认证遗忘定义——包括 (ε,δ)-遗忘 (Sekhari et al. 2021)、Rényi 遗忘 (Allouah et al. 2025b) 以及 (φ,ε)-遗忘 (Zou et al. 2025)——都依赖于一个核心假设：每个样本的损失函数同时满足 µ-强凸性和 L-光滑性，即 Hessian 满足 $\mu I_p \preceq \nabla^2 f(\beta, \mathbf{z}_i) \preceq L I_p$，且 µ=Ω(1)、L=O(1)。在比例高维区域 p∼n 中，这一假设几乎必然失效。以岭正则化最小二乘为例，其 Hessian 为 $2 X^{\top} X + 2 \lambda I_p$；当 p 与 n 同阶时，$X^{\top} X$ 的特征值分布在宏观尺度上不再有常数上下界，使得强凸性与光滑性条件无法同时成立。

这一假设失效带来了严重的后果。Zou et al. (2025) 的 (φ,ε)-认证遗忘框架要求至少两步牛顿更新才能同时保证隐私与精度，而拉普拉斯噪声机制在注入扰动时缺乏维度无关的校准依据，导致高维下噪声过度注入、泛化性能显著退化。问题的因果链可以概括为：**高维比例区域打破了传统优化假设 → 现有认证定义与噪声机制不兼容 → 遗忘算法面临隐私-精度的次优权衡**。

本文的核心动机正是针对这一瓶颈，提出一种在高维环境中自然最优的认证遗忘框架。核心思路是采用 **ε-Gaussian 认证遗忘 (GPAR)** 替代传统的 (φ,ε)-认证，利用高斯噪声机制与假设检验中高斯权衡曲线的维度无关性，实现精准的噪声校准。理论分析表明，仅需**单步牛顿更新**配合精心校准的高斯噪声，即可同时达到 ε-Gaussian 可认证性和渐近消失的泛化误差分化——这一结果揭示了 (φ,ε)-可认证遗忘在高维场景下的次优性，并为实际部署提供了简洁高效的遗忘方案。

## 核心创新

本工作的核心创新在于提出并验证了一种适用于高维比例区域 ($p \sim n$) 的 **ε-Gaussian 认证遗忘框架 (GPAR)**，并证明仅需 **单步牛顿更新配合精确校准的高斯噪声** 即可同时实现隐私认证与渐近消失的泛化误差分化。这一框架在认证定义、噪声机制和算法效率三个关键维度上突破了已有工作的瓶颈。

### 认证定义的根本性改进

已有可认证遗忘定义与高斯噪声机制存在根本性不兼容。具体而言：
- **(ε,δ)-认证遗忘** (Sekhari et al., 2021) 和 **Rényi 认证遗忘** (Allouah et al., 2025b) 在 $p \sim n$ 的高维区域中，因传统优化假设 (同时强凸性与光滑性，即 $\mu I_p \preceq \nabla^2 f(\beta, \mathbf{z}_i) \preceq L I_p$ 且 $\mu = \Omega(1), L = O(1)$) 失效而无法有效运作。
- **(φ,ε)-认证遗忘** (Zou et al., 2025) 虽采用了贸易函数框架，但其定义导致至少需要两步牛顿更新才能同时保证隐私与精度。

本工作提出的 **(φ,ε)-Gaussian 认证遗忘** (Definition 2) 将贸易函数 $f$ 替换为高斯最优贸易曲线

$$f_{G,\varepsilon}(\alpha) = \Phi(\Phi^{-1}(1-\alpha)-\varepsilon),$$

该曲线刻画了比较 $N(0,1)$ 与 $N(\varepsilon,1)$ 时的最小第二类错误。关键性质在于**维度无关性** (Lemma 1)：

$$T(\mu_1+\sigma N(0,\mathbb{I}_p), \mu_2+\sigma N(0,\mathbb{I}_p)) \equiv T(N(0,1), N(\varepsilon,1)), \quad \varepsilon = \frac{\|\mu_1-\mu_2\|_2}{\sigma}.$$

这一定义与高斯噪声机制天然兼容，无需像 (φ,ε)-认证那样依赖次优的噪声注入策略。表 1 系统对比了各认证定义与假设条件，本框架在高维比例区域中具有最优可实现性。

### 算法效率的质变：从两步到一步

Zou et al. (2025) 在 (φ,ε)-认证框架下得出结论：至少需要两步牛顿更新才能同时确保隐私与精度。本工作揭示了这一差异的根源在于 **(φ,ε)-认证定义与噪声注入机制的次优性**，而 ε-Gaussian 认证能够最优地克服这一限制。

具体地，本工作提出的遗忘算法仅包含三个模块：
1. **RERM 训练器**：在完整数据集上求解正则化经验风险最小化得到原始模型 $\hat{\beta}$ (Equation 1)；
2. **牛顿单步近似**：利用 Hessian 和梯度计算
   $$\hat{\beta}_{\backslash \mathcal{M}}^{(1)} = \hat{\beta} - \mathbf{G}(L_{\backslash \mathcal{M}})^{-1}(\hat{\beta}) \nabla L_{\backslash \mathcal{M}}(\hat{\beta})$$
   (Equation 13)；
3. **高斯噪声注入**：添加各向同性高斯噪声 $\boldsymbol{b} \sim N(0, (R/\varepsilon)^2 \mathbb{I}_p)$，其中
   $$R = C_1(n) \sqrt{\frac{C_2(n) m^3}{2 \lambda \nu n}}$$
   (Equation 14, Theorem 2)。

理论证明 (Theorem 3)，当噪声方差设置为 $R/\varepsilon$ 时，该算法以高概率满足 $(\phi_n, \varepsilon)$-GPAR，且泛化误差分化 (GED) 满足

$$\mathrm{GED}(\tilde{\beta}_{\backslash \mathcal{M}}, \hat{\beta}_{\backslash \mathcal{M}}) \leq C_1(n) \sqrt{C_2(n)} \left( \frac{1}{\varepsilon} + \frac{1}{\sqrt{p}} \right) \sqrt{ \frac{m^3 (m+2)}{\lambda \nu n} } \cdot \mathrm{polylog}(n),$$

即 $\mathrm{GED} = O_p(m^2 \mathrm{polylog}(n) / \sqrt{n})$，在高维极限下趋于零。

### 假设条件的实质性放松

已有工作普遍要求每样本损失函数同时满足 **μ-强凸性与 L-光滑性**，且 $\mu = \Omega(1), L = O(1)$。这一条件在高维比例区域中因 Hessian 谱展宽而失效——以岭正则化最小二乘为例，其 Hessian 为 $2 X^{\top} X + 2 \lambda I_p$，当 $p/n \to \gamma$ 时条件数发散。

本工作在 Assumptions (A1)–(A4) 下仅要求：
- 可分离正则化器
- 损失函数凸且导数具有多项式增长
- **不要求**每样本损失同时强凸与光滑

这一放松使得理论能够覆盖高维比例区域中的实际模型族。

### 实验验证的关键优势

数值实验从多个维度验证了高斯认证遗忘的优越性：
- **维度扩展性** (Figure 1)：高斯噪声的 GED 随维度 $p$ 以约 $p^{-0.5}$ 阶衰减 (斜率 -0.47 至 -0.54)，始终低于拉普拉斯噪声，与 Theorem 3 的理论预测一致。
- **隐私预算响应** (Figure 2)：GED 随 $\varepsilon$ 增大单调下降，高斯噪声在所有 $\varepsilon$ 取值下均优于拉普拉斯。
- **删除规模影响** (Figure 3)：GED 随 $m$ 以约 $m^{1.5}$ 阶增长，高斯噪声仍保持优势。
- **大维度对比** (Figure 4)：在 $p = 1000$ 至 $10000$ 范围内，高斯认证遗忘的 GED 和 UED 均显著低于 (φ,ε,δ)-认证遗忘。
- **真实高维数据** (Figure 5)：在 IMDb 数据集 ($p=3161, n=1579$) 上，高斯框架的优越性能尤为突出，验证了其在高维实际场景中的有效性。

### 需人工核实的关键点

以下结论依赖于论文中的理论推导，建议读者参考原文验证：
1. 理论常数 $C_1(n), C_2(n)$ 的紧致性尚未经过数值验证，实际应用中需通过蒙特卡洛方法近似积分 Hessian。
2. 删除规模须满足 $m = o(n^{1/4}/\mathrm{polylog}(n))$，大规模删除场景下的精度退化风险需进一步评估。
3. 特征次高斯分布假设在现实数据中可能偏离，对厚尾特征的鲁棒性尚未探索。

## 整体框架

![[assets/figures/papers/iclr26_0009_0FJYicpOj0_Gaussian_certified_unlearning_in_high_dimensions/figures/001_Table_1.jpg]]
*Table 1: Summary of prior certified unlearning notions and per-example loss assumptions, compared to our proposed ( $\varphi , \varepsilon$ ) -Gaussian certifiability framework (Def. 2). Our notion is optimally achievable with practical Gaussian noise mechanisms in the proportional high-dimensional regime, and it relies on relaxed convex per-example loss assumptions that remain valid in this setting (Sec. 4.2)

### 问题设定

考虑一个包含 $n$ 个样本的训练数据集 $\mathcal{D}_n = \{\mathbf{z}_i\}_{i=1}^n$，学习算法 $A$ 通过正则化经验风险最小化（RERM）得到原始模型：

$$\hat{\beta} = A(\mathcal{D}_n) = \arg\min_\beta\; \lambda r(\beta) + \sum_{i=1}^n \ell(y_i \mid \boldsymbol{x}_i^\top \beta)$$

当一组用户请求删除其数据 $\mathcal{D}_{\mathcal{M}}$（规模为 $m = |\mathcal{M}|$）时，遗忘算法 $\bar{A}$ 需基于原始模型 $\hat{\beta}$、删除集 $\mathcal{D}_{\mathcal{M}}$、辅助统计量 $T(\mathcal{D}_n)$ 和随机噪声 $b$，输出遗忘模型 $\tilde{\beta}_{\setminus\mathcal{M}}$，使其在统计上无法与理想重训练模型 $\hat{\beta}_{\setminus\mathcal{M}} = A(\mathcal{D}_{\setminus\mathcal{M}})$ 区分。

### 核心瓶颈与设计动机

在高维比例区域（$p \sim n$）中，传统优化假设——每样本损失 $f(\beta, \mathbf{z}_i)$ 同时满足 $\mu$-强凸和 $L$-光滑（$\mu I_p \preceq \nabla^2 f \preceq L I_p$）——必然失效。例如，岭回归的 Hessian 为 $2X^\top X + 2\lambda I_p$，当 $p > n$ 时其最小特征值趋于零，强凸性不再成立。同时，现有可认证遗忘定义（$(\varepsilon,\delta)$-遗忘、Rényi 遗忘、$(\varphi,\varepsilon)$-遗忘）与高斯噪声机制不兼容，导致过度噪声注入和精度损失。

本工作的核心洞察是：**在高维环境中，高斯认证遗忘是自然的最优认证概念**；单步牛顿更新结合精确校准的高斯噪声即可同时实现隐私保护和模型精度，且维度的影响被标准化欧氏距离 $\varepsilon$ 完全吸收。

### Pipeline 模块

整个遗忘流程由三个模块串联构成：

**模块 1：RERM 训练器。** 在完整数据集上求解正则化经验风险最小化，得到原始模型 $\hat{\beta}$。该步骤是确定性的，给定数据后输出唯一。

**模块 2：牛顿单步近似。** 从 $\hat{\beta}$ 出发，利用 Hessian 和梯度执行一步牛顿更新，逼近删除 $\mathcal{M}$ 后的最优解：

$$\hat{\beta}_{\setminus\mathcal{M}}^{(1)} = \hat{\beta} - \mathbf{G}(L_{\setminus\mathcal{M}})^{-1}(\hat{\beta})\, \nabla L_{\setminus\mathcal{M}}(\hat{\beta})$$

其中 $\mathbf{G}(L_{\setminus\mathcal{M}})$ 为删除后损失函数的 Hessian，$\nabla L_{\setminus\mathcal{M}}$ 为对应梯度。这一步利用辅助统计量 $T(\mathcal{D}_n)$ 中预存的 Hessian 信息，避免重新计算完整 Hessian。

**模块 3：高斯噪声注入。** 向牛顿近似解添加零均值各向同性高斯噪声，得到最终遗忘模型：

$$\tilde{\beta}_{\setminus\mathcal{M}} = \hat{\beta}_{\setminus\mathcal{M}}^{(1)} + \boldsymbol{b}, \quad \boldsymbol{b} \sim \mathcal{N}(0, \sigma^2 I_p)$$

噪声方差 $\sigma^2 = R^2/\varepsilon^2$ 由理论精准校准，其中半径参数 $R$ 取决于数据维度和删除规模：

$$R = C_1(n) \sqrt{\frac{C_2(n) m^3}{2 \lambda \nu n}}$$

### 输入输出流

| 阶段 | 输入 | 输出 | 关键参数 |
|------|------|------|----------|
| 训练 | $\mathcal{D}_n$ | $\hat{\beta}$ | $\lambda$（正则化强度） |
| 遗忘请求 | $\mathcal{M}$（删除集索引） | — | $m = \vert\mathcal{M}\vert$ |
| 牛顿近似 | $\hat{\beta}$, $T(\mathcal{D}_n)$, $\mathcal{D}_{\mathcal{M}}$ | $\hat{\beta}_{\setminus\mathcal{M}}^{(1)}$ | Hessian 预计算 |
| 噪声注入 | $\hat{\beta}_{\setminus\mathcal{M}}^{(1)}$ | $\tilde{\beta}_{\setminus\mathcal{M}}$ | $\varepsilon$（认证强度） |

### 认证与精度度量

框架采用 $(\varphi_n, \varepsilon)$-高斯认证遗忘（GPAR）作为隐私度量，其核心是高斯权衡函数：

$$f_{G,\varepsilon}(\alpha) = \Phi(\Phi^{-1}(1-\alpha) - \varepsilon)$$

该函数比较 $\mathcal{N}(0,1)$ 与 $\mathcal{N}(\varepsilon,1)$ 的最优假设检验权衡，且具有维度无关性：在高维各向同性高斯噪声下，两个 $p$ 维分布间的权衡函数仅依赖于标准化欧氏距离 $\varepsilon = \|\mu_1 - \mu_2\|/\sigma$，与维度 $p$ 无关。

精度度量采用泛化误差分化（Generalization Error Divergence, GED），衡量遗忘模型与理想重训练模型在测试样本上的期望绝对损失差异：

$$\mathrm{GED}_{\ell}(A, \bar{A}; \mathcal{M}, \mathcal{D}_n) := \mathbb{E}\left[\left|\ell(y_0 \mid x_0^\top A(\mathcal{D}_{\setminus\mathcal{M}})) - \ell(y_0 \mid x_0^\top \bar{A}(A(\mathcal{D}_n), \mathcal{D}_{\mathcal{M}}, T(\mathcal{D}_n), b))\right| \;\middle|\; \mathcal{D}_n\right]$$

### 与先前框架的关键差异

Table 1 系统比较了本框架与先前认证遗忘定义的差异。Zou et al. (2025) 的 $(\varphi,\varepsilon)$-认证遗忘需要至少两步牛顿更新才能同时保证隐私与精度，而本工作证明单步即可——这一差距揭示了 $(\varphi,\varepsilon)$-认证定义与噪声机制的次优性，而 $(\varphi,\varepsilon)$-高斯认证遗忘能够最优地解决该问题。同时，本框架放松了每样本损失的强凸-光滑联合假设，仅要求可分离正则化器、凸性和多项式增长的导数，使其在高维比例区域中依然有效。

## 核心模块与公式推导

### 核心模块

本工作的认证遗忘算法由三个顺序模块构成：

1. **RERM 训练器**：在完整数据集 $\mathcal{D}_n$ 上求解正则化经验风险最小化，得到原始模型 $\hat{\beta}$（公式 1）。
2. **牛顿单步近似**：利用 Hessian 和梯度信息，从 $\hat{\beta}$ 出发执行一步牛顿更新，得到去除子集 $\mathcal{M}$ 的近似估计 $\hat{\beta}_{\setminus \mathcal{M}}^{(1)}$（公式 13）。
3. **高斯噪声注入**：向 $\hat{\beta}_{\setminus \mathcal{M}}^{(1)}$ 添加零均值各向同性高斯噪声 $\boldsymbol{b} \sim N(0, \sigma^2 I_p)$，得到最终遗忘模型 $\tilde{\beta}_{\setminus \mathcal{M}}$（公式 14）。

整个流程的因果机制是：单步牛顿更新提供对理想重训练模型的高质量近似，而精心校准的高斯噪声则提供可认证的隐私保护。两者结合使得算法在高维比例区域 $p \sim n$ 中同时实现认证遗忘和渐近消失的泛化误差分化。

### 关键公式

**RERM 目标函数**

$$\hat{\beta} = \arg\min_\beta \lambda r(\beta) + \sum_{i=1}^n \ell(y_i \mid \boldsymbol{x}_i^\top \beta) \tag{1}$$

其中 $\lambda$ 为正则化强度，$r(\beta)$ 为强凸正则化器，$\ell$ 为凸损失函数。

**单步牛顿更新**

$$\hat{\beta}_{\setminus \mathcal{M}}^{(1)} = \hat{\beta} - \mathbf{G}(L_{\setminus \mathcal{M}})^{-1}(\hat{\beta}) \nabla L_{\setminus \mathcal{M}}(\hat{\beta}) \tag{13}$$

其中 $\mathbf{G}(L_{\setminus \mathcal{M}})$ 为去除子集 $\mathcal{M}$ 后损失函数的 Hessian（或广义 Jacobian），$\nabla L_{\setminus \mathcal{M}}$ 为对应梯度。这一步利用了牛顿法在根附近二次收敛的性质，以极低的计算代价逼近理想重训练模型。

**噪声注入输出**

$$\tilde{\beta}_{\setminus \mathcal{M}} = \hat{\beta}_{\setminus \mathcal{M}}^{(1)} + \boldsymbol{b} \tag{14}$$

其中 $\boldsymbol{b} \sim N(0, (R/\varepsilon)^2 I_p)$。噪声方差 $\sigma^2 = R^2/\varepsilon^2$ 由定理 2 中的半径参数 $R$ 和认证参数 $\varepsilon$ 确定。

**高斯权衡曲线**

$$f_{G,\varepsilon}(\alpha) = \Phi(\Phi^{-1}(1-\alpha)-\varepsilon) \tag{9}$$

这是比较 $N(0,1)$ 与 $N(\varepsilon,1)$ 的最优权衡函数，用于定义 $(\varphi, \varepsilon)$-高斯认证遗忘（GPAR）。其关键性质是维度无关性：对于两个各向同性高斯分布，权衡函数仅依赖于标准化的欧氏距离 $\varepsilon$，与维度 $p$ 无关（引理 1）：

$$T(\mu_1+\sigma N(0,\mathbb{I}_p), \mu_2+\sigma N(0,\mathbb{I}_p)) \equiv T(N(0,1), N(\varepsilon,1)) \tag{10}$$

**噪声半径参数**

$$R = C_1(n) \sqrt{\frac{C_2(n) m^3}{2 \lambda \nu n}}$$

其中 $m$ 为删除样本数，$\lambda$ 为正则化强度，$\nu$ 与数据分布相关，$C_1(n), C_2(n)$ 为与样本量 $n$ 相关的对数因子。该参数保证算法满足 $(\varphi_n, \varepsilon)$-GPAR（定理 2）。

**泛化误差分化上界**

$$\mathrm{GED}(\tilde{\beta}_{\setminus \mathcal{M}}, \hat{\beta}_{\setminus \mathcal{M}}) \leq C_1(n) \sqrt{C_2(n)} \left( \frac{1}{\varepsilon} + \frac{1}{\sqrt{p}} \right) \sqrt{ \frac{m^3 (m+2)}{\lambda \nu n} } \cdot \mathrm{polylog}(n)$$

该上界揭示了 GED 随 $n$ 增大以 $O_p(m^2 \mathrm{polylog}(n)/\sqrt{n})$ 速率衰减（定理 3），在 $m = o(n^{1/4}/\mathrm{polylog}(n))$ 条件下保证渐近消失的精度损失。

### 与基线方法的关键差异

| 模块/假设 | 基线 (Zou et al. 2025) | 本工作 |
|-----------|------------------------|--------|
| 认证概念 | $(\varphi,\varepsilon)$-可认证遗忘 | $(\varphi,\varepsilon)$-GPAR |
| 噪声机制 | 未明确或拉普拉斯噪声 | 高斯噪声 $\sigma^2 = R^2/\varepsilon^2$ |
| 牛顿步数 | 至少两步 | 一步即可 |
| 损失假设 | $\mu$-强凸且 $L$-光滑，$\mu=\Omega(1), L=O(1)$ | 放松假设：可分离正则化器、凸损失、多项式增长导数，无需逐样本强凸性和光滑性同时成立 |

核心瓶颈在于：传统 $(\varphi,\varepsilon)$-认证遗忘定义与高斯噪声机制不兼容，导致过度噪声注入和精度损失，而 GPAR 通过高斯权衡曲线精准校准噪声方差，在高维比例区域中实现了最优的隐私-精度权衡。

## 实验与分析

### 主结果：高斯认证遗忘的精度优势

实验在合成数据与真实数据集上系统比较了高斯噪声与拉普拉斯噪声遗忘、以及 (φ,ε,δ)-认证遗忘的泛化误差分化 (GED)。核心发现是：高斯噪声机制在全部设置下均取得更低的 GED，且优势在高维场景中尤为显著。

**维度缩放行为 (Figure 1)。** 在合成 ridge logistic 回归任务中，固定隐私预算 ε=5、正则化参数 λ=0.5，考察维度 p 从 100 增长至 10000 时 GED 的变化。高斯遗忘的 GED 以约 p^{-0.5} 的速率衰减 (m=1,5,10 时斜率分别为 -0.47, -0.54, -0.51)，与 Theorem 3 的理论上界一致。相比之下，拉普拉斯噪声的 GED 衰减更慢且绝对值更高。这一结果直接验证了高斯权衡函数 $f_{G,\varepsilon}$ 的维度无关性 (Lemma 1)：在高维比例区域中，高斯噪声的隐私-精度权衡仅依赖于标准化欧氏距离 ε，而拉普拉斯机制无法实现这种维度自由的校准。


![[assets/figures/papers/iclr26_0009_0FJYicpOj0_Gaussian_certified_unlearning_in_high_dimensions/figures/004_Figure_1.jpg]]
*Figure 1: Comparison of unlearned estimators on new test data: mean GED (with 3 SD error bars) across the dimension p (both in log scale) for Laplace (in red) vs. Gaussian (in cyan). We set $\lambda$ = 0 . 5*

**隐私预算 ε 的影响 (Figure 2, Figure 5)。** 固定 p=500、m=5，随 ε 从 0.5 增大至 10，高斯遗忘的 GED 单调下降且始终低于拉普拉斯。在真实数据集上这一优势更加突出：在低维 MNIST (p=784, n=1200) 上高斯与拉普拉斯的差距较小，但在高维 IMDb 文本数据 (p=3161, n=1579) 上，高斯框架的优势显著——GED 在 ε=0.5 时即低于拉普拉斯在 ε=10 时的水平。这直接支撑了核心主张：**高斯认证遗忘在高维真实数据上具有最优的隐私-精度权衡**。


![[assets/figures/papers/iclr26_0009_0FJYicpOj0_Gaussian_certified_unlearning_in_high_dimensions/figures/007_Figure_2.jpg]]
*Figure 2: Comparison of GED (plotted in log scale) across different values of ε for Laplace noise (in red) vs. Gaussian noise (in cyan). We set $\lambda$ = 0 . 5*

![[assets/figures/papers/iclr26_0009_0FJYicpOj0_Gaussian_certified_unlearning_in_high_dimensions/figures/014_Figure_5.jpg]]
*Figure 5: Comparison of mean GED (with 3 SD error bars) across ε for (left) low-dimensional MNIST data with p = 7 8 4 , n = 1 2 0 0 and (right) high dimensional IMDb data with p = 3 1 6 1 , n = 1 5 7 9 We set $\lambda$ = 0 . 0 1 . Experiments were repeated 20 times across random draws of the test set*

**删除规模 m 的敏感性 (Figure 3)。** 固定 p=500,1500,2500，GED 随 m 增加按约 m^{1.5} 阶上升 (斜率 1.37–1.44)，与理论界中 $O(m^{1.5}/\sqrt{n})$ 的依赖关系吻合。高斯噪声在所有 m 取值下均优于拉普拉斯，且优势不随 m 增大而消失。


![[assets/figures/papers/iclr26_0009_0FJYicpOj0_Gaussian_certified_unlearning_in_high_dimensions/figures/010_Figure_3.jpg]]
*Figure 3: Comparison of mean GED (with 3 SD error bars) across the unlearning size m (both in log scale) for Laplace noise (in red) vs. Gaussian noise (in cyan). We set $\lambda$ = 0 . 5*

**与 (φ,ε,δ)-认证遗忘的对比 (Figure 4)。** 在大维度设置 (p=1000 至 10000) 下，高斯认证遗忘的 GED 和 UED (Unlearned Error Divergence) 均低于 (φ,ε,δ)-认证遗忘框架 (Sekhari et al. 2021)。这从实验上揭示了 (φ,ε,δ)-认证定义与高斯噪声机制的次优兼容性——该框架在大维度下需要过度噪声注入来满足认证条件，导致不必要的精度损失。


![[assets/figures/papers/iclr26_0009_0FJYicpOj0_Gaussian_certified_unlearning_in_high_dimensions/figures/012_Figure_4.jpg]]
*Figure 4: Comparison of mean GED and UED (with 3 SD error bars) across the dimension p when the dimension is large, in that it varies from 1000 to 10000. We set $\lambda$ = 0 . 1*

### 消融分析

**噪声机制选择。** 所有实验一致表明：在相同的 ε 下，各向同性高斯噪声 $b \sim N(0, (R/\varepsilon)^2 I_p)$ 的 GED 始终低于拉普拉斯噪声。这并非偶然——高斯噪声的协方差结构与高维数据下 Hessian 的渐近谱分布相匹配，而拉普拉斯噪声的独立分量假设无法利用这一结构。

**维度效应。** GED 随 p 增大而下降的现象 (Figure 1) 验证了 Theorem 3 中 $1/\sqrt{p}$ 项的贡献。在高维比例区域 p∼n 中，这一项的衰减与 $1/\varepsilon$ 项共同决定了精度退化的渐近速率。当 p 较小时 (如 MNIST 的 p=784)，高斯与拉普拉斯的差距有限；当 p 增大至 3161 (IMDb) 时，高斯机制的优势被维度效应放大。

**正则化参数 λ。** 实验固定 λ=0.5 (合成数据) 或 λ=0.01 (真实数据)。较小的 λ 会增大 Hessian 的条件数，理论上会放大 GED 上界中的 $1/\sqrt{\lambda}$ 因子。实验未系统探索 λ 的影响，这一点需要后续验证。

### 失败模式与局限性

1. **大规模删除的退化。** 理论要求 $m = o(n^{1/4}/\mathrm{polylog}(n))$，当 m 接近此上界时，GED 以 $m^{1.5}$ 阶增长，精度退化可能不可接受。实验仅在 m≤10 的范围内验证，更大规模删除的行为未经验证。

2. **数据分布假设。** 理论依赖特征的次高斯分布假设 (Assumption A2)。在 IMDb 等文本数据上，虽然实验表现良好，但严格来说文本特征可能具有厚尾特性，此时高斯噪声的校准可能偏离最优。

3. **非凸扩展未验证。** 实验仅覆盖凸损失 (logistic 回归)，未涉及非凸模型。框架向深度网络或 transformers 的推广仍是开放问题。

4. **常数紧致性。** Theorem 3 中的常数 $C_1(n), C_2(n)$ 包含 $\mathrm{polylog}(n)$ 因子，实验未验证这些常数的实际紧致性。实际部署时，噪声方差 $R^2/\varepsilon^2$ 中的 R 需要通过蒙特卡洛方法近似积分 Hessian，引入额外近似误差。

### 重要图表结论

- **Table 1** 从理论上定位了本工作的创新：已有 (ε,δ)-遗忘和 Rényi 遗忘定义与高斯噪声机制不兼容，在高维比例区域中失效；而 (φ,ε)-高斯认证遗忘 (GPAR) 通过高斯权衡曲线 $f_{G,\varepsilon}$ 实现了最优校准，且只需放松的凸性假设。

- **Figure 5 (右)** 是整篇论文最具说服力的实验证据：在高维 IMDb 数据 (p>n) 上，高斯认证遗忘的 GED 在所有 ε 下均显著低于拉普拉斯和 (φ,ε,δ)-认证遗忘，直接验证了“高斯认证遗忘在高维环境中是自然的最优认证概念”这一核心洞察。

## 方法谱系与知识库定位

### 与已有认证遗忘定义的继承与突破

本文提出的 (φ, ε)-Gaussian 认证遗忘框架 (GPAR) 直接回应了高维比例区域 $p \sim n$ 中已有认证遗忘定义的失效问题。Table 1 系统对比了本工作与 Guo et al. (2020)、Sekhari et al. (2021)、Allouah et al. (2025b) 以及 Zou et al. (2025) 的认证概念差异。核心分歧在于：传统 $(ε,δ)$-遗忘和 Rényi 遗忘要求假设检验的 trade-off 函数被常数界控制，而该要求在 $p \sim n$ 的高维设定下与高斯噪声机制不兼容，导致要么无法认证，要么需注入过量噪声而牺牲模型精度。

将认证定义从常数界松弛为 trade-off 函数界 $f$ 是 Zou et al. (2025) 引入 (φ, ε)-认证遗忘的关键贡献，但该工作仍沿用 Laplace 噪声机制，并得出至少需要两步牛顿更新才能同时保证隐私与精度的结论。本文揭示了该结论的根源在于 (φ, ε)-认证遗忘定义本身的次优性：当噪声机制为高斯时，最优 trade-off 曲线 $f_{G,\varepsilon}(\alpha) = \Phi(\Phi^{-1}(1-\alpha)-\varepsilon)$ 与 Laplace 噪声对应的曲线存在本质差异，前者在尾部区域提供更强的区分保证。因此，本文只需**单步**牛顿更新即可同时实现认证性与渐近消失的泛化误差分化，这在概念上澄清了“两步必要”并非算法本质，而是定义-机制匹配的次优性所致。

从假设检验视角看，(φ, ε)-Gaussian 认证遗忘继承了 Dong et al. (2022) 的 $f$-差分隐私框架，利用 trade-off 函数精确刻画 Blackwell 序，从而保证后处理下的最优行为。与差分隐私文献中广泛使用的 $f_{G,\varepsilon}$ 曲线不同，本文将这一工具首次引入机器遗忘场景，并证明了维度无关性引理 (Lemma 1)：对于各向同性高斯噪声，trade-off 函数仅依赖于标准化欧氏距离 $\varepsilon = \|\mu_1 - \mu_2\|_2 / \sigma$，与维度 $p$ 无关。该性质是高斯认证遗忘在高维下保持紧致性的理论基础。

### 优化假设的松弛与适用边界

已有认证遗忘工作（Sekhari et al. 2021; Allouah et al. 2025b）普遍要求每个样本的损失函数同时满足 $\mu$-强凸性和 $L$-光滑性，且 $\mu = \Omega(1)$、$L = O(1)$。该假设在高维比例区域 $p \sim n$ 中系统性地失效——以岭正则化最小二乘为例，其 Hessian 为 $2X^\top X + 2\lambda I_p$，当 $p/n \to \gamma > 0$ 时，条件数发散，无法同时满足 $\mu = \Omega(1)$ 和 $L = O(1)$。

本文在假设 (A1)–(A4) 下工作，仅要求：
- 正则化器 $r(\beta)$ 为强凸（如 $\ell_2$ 正则化）；
- 每个样本损失 $\ell(\cdot)$ 为凸且具有多项式增长的导数；
- 不再要求每个样本损失同时强凸和光滑。

这一松弛使得理论覆盖了高维比例区域中实际可用的模型族（如岭逻辑回归），但同时也划定了适用边界：**非凸损失函数（如深度网络中的交叉熵）不在当前理论覆盖范围内**。此外，数据特征需满足次高斯分布假设，对于厚尾特征的实际数据，理论保证可能退化。

### 删除规模与维度的限制

定理 2 和定理 3 给出的认证性与 GED 上界依赖于删除规模 $m$ 满足 $m = o(n^{1/4} / \mathrm{polylog}(n))$。这意味着同时删除请求的数量受到严格限制：当 $m$ 增大至与 $n^{1/4}$ 同阶时，噪声半径 $R = C_1(n) \sqrt{C_2(n) m^3 / (2\lambda \nu n)}$ 将不再保证 GED 趋于零。数值实验 (Figure 3) 表明 GED 随 $m$ 以约 $m^{1.5}$ 阶增长，与理论界中 $m^3$ 的主导项定性一致，但常数紧致性尚未验证。

该限制的根源在于牛顿单步近似的误差界依赖 $m$ 的高阶项。开放问题之一是将删除规模提升至 $m^3 = o(n)$，这可能需要更精细的 Hessian 近似或二阶修正。

### 算法模块的普适性与局限

本工作的遗忘算法由三个模块串联构成：

1. **RERM 训练器**：在完整数据上求解 $\hat{\beta} = \arg\min_\beta \lambda r(\beta) + \sum_{i=1}^n \ell(y_i \mid \boldsymbol{x}_i^\top \beta)$，提供原始模型。
2. **牛顿单步近似**：利用 Hessian 和梯度计算 $\hat{\beta}_{\setminus \mathcal{M}}^{(1)} = \hat{\beta} - \mathbf{G}(L_{\setminus \mathcal{M}})^{-1}(\hat{\beta}) \nabla L_{\setminus \mathcal{M}}(\hat{\beta})$，近似重训练模型。
3. **高斯噪声注入**：添加 $\boldsymbol{b} \sim \mathcal{N}(0, (R/\varepsilon)^2 \mathbb{I}_p)$ 得到最终遗忘模型。

该流水线的适用范围受限于：
- **模型族**：仅适用于正则化经验风险最小化框架，未扩展至更复杂的模型族（如深度网络、集成模型）。
- **二阶信息获取**：需要计算并求逆完整 Hessian 矩阵，在高维下计算成本为 $O(p^3)$。实际应用中需通过蒙特卡洛或共轭梯度等方法近似积分 Hessian，近似二阶方法（如拟牛顿法）对认证性的影响是开放问题。
- **删除模式**：仅处理批量删除，未涵盖在线遗忘（连续到达的删除请求）或分布遗忘（修改数据分布而非删除特定样本）场景。

### 与差分隐私和机器遗忘文献的交叉定位

本文的 (φ, ε)-Gaussian 认证遗忘与差分隐私存在深层联系。附录 C.1 证明：Gaussian 认证遗忘（容忍度 $\phi$）等价于一组 $(ε,δ)$-遗忘扩展，且转换是无损的。这意味着满足 GPAR 的算法自动满足适当参数下的 $(ε,δ)$-遗忘定义。但反过来不成立：$(ε,δ)$-遗忘定义在高维下过于宽松，无法区分 Laplace 和高斯噪声的优劣，而 GPAR 通过 trade-off 函数精确捕捉了这一差异。

从机器遗忘的算法范式看，本工作属于**基于影响的遗忘**（influence-based unlearning）谱系，与 Guo et al. (2020) 的 Newton 步删除和 Sekhari et al. (2021) 的扰动梯度下降共享核心思想。区别在于：本工作首次在高维比例区域中给出了端到端的认证性-精度权衡分析，并证明了单步牛顿加高斯噪声是该区域的最优组合。

### 开放问题

1. **数据分布假设**：能否将次高斯特征假设放松至厚尾分布（如仅为有限二阶矩），同时保持认证性？
2. **非凸损失扩展**：对于 transformers 或 MLPs 等非凸损失函数，能否建立类似的 Gaussian 认证遗忘理论？
3. **近似二阶方法**：拟牛顿法（如 L-BFGS）或 Hessian-free 方法对认证性和 GED 界的影响是什么？
4. **删除规模提升**：能否将 $m = o(n^{1/4})$ 的条件改进为 $m^3 = o(n)$，以支持更大规模的批量删除？
5. **在线与分布遗忘**：该框架是否适用于删除请求连续到达的在线场景，或修改数据分布而非删除特定样本的分布遗忘场景？
6. **常数紧致性**：理论界的常数因子是否可进一步收紧，以指导实际噪声方差的选择？

## 原文 PDF

![[paperPDFs/ICLR_2026/Gaussian_certified_unlearning_in_high_dimensions_A_hypothesis_testing_approach.pdf]]
