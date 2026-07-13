---
title: "A Sharp KL Convergence Analysis for Diffusion Models under Minimal Assumptions"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Sharp_KL_Convergence_Analysis_for_Diffusion_Models_under_Minimal_Assumptions.pdf
project_link: null
code_link: null
aliases:
- OSNSA1
- SKCADMUMA
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/sampling_and_optimization
core_operator: "将生成过程建模为反向ODE步后接一个较小的前向加噪步的组合，利用ODE步控制Wasserstein型误差，再通过加噪步将其转换为KL误差，从而获得更好的步长依赖。"
primary_logic: "通过引入Benton et al. (2023)随机局部化论证的ODE对应物，并发展新的证明技术来界定得分函数的二阶空间导数（拉普拉斯项），实现了KL散度收敛在维度d上的线性依赖，同时将精度ε的依赖从二次改进为线性。"
claims:
- "算法在KL散度上达到Õ(d log^{3/2}(1/δ)/ε)步的迭代复杂度，优于先前最优的Õ(d log^2(1/δ)/ε²)步。"
- "KL散度最终上界为KL(p_{t1} || hat{p}_{t1}) ≲ (d + m_2) e^{-T} + d^2 c^3 K + T ε_score^2。"
- "离散化误差通过重缩放过程z(t)=e^t x(t)和指数积分器离散化，得到E[||z_{k-0.5} - tilde{z}_{k-0.5}||_2^2] ≤ 1/2 (h_k + h_{k-1})^3 ∫ e^{4t} E[||s_r'(t,z(t))||_2^2] dt，实现了O(h_k^3)的步长依赖。"
- "通过Fokker-Planck方程将得分函数的时间导数转化为空间导数，并利用新引理（Lemma A.16, A.17）界定拉普拉斯项，最终得到E[||s_r'(t,z)||_2^2] ≲ d^2 e^{4t}/(e^{2t}-1)^3 - ...，实现了线性d依赖。"
---

# A Sharp KL Convergence Analysis for Diffusion Models under Minimal Assumptions

> [!tip] 核心洞察
> 通过引入Benton et al. (2023)随机局部化论证的ODE对应物，并发展新的证明技术来界定得分函数的二阶空间导数（拉普拉斯项），实现了KL散度收敛在维度d上的线性依赖，同时将精度ε的依赖从二次改进为线性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 最小假设下扩散模型 KL 收敛的紧致分析 |
| 英文题名 | A Sharp KL Convergence Analysis for Diffusion Models under Minimal Assumptions |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=c8Ft3246KD) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/sampling_and_optimization |
| Method | ODE-step + noise-step 生成算法（Algorithm 1） |
| Dataset | 理论分析（无特定数据集） |

> [!tip] 效果简介
> - 理论分析（无特定数据集） 上，KL散度 为 Õ(d log^{3/2}(1/δ)/ε)，对比 Õ(d log^2(1/δ)/ε²) (Benton et al., 2024)，变化 ε依赖从二次改进为线性。
> - 理论分析（无特定数据集） 上，迭代步数K 为 Θ(d (log(1/δ))^{3/2} / ε_score)，对比 Θ(d log^2(1/δ) / ε_score^2) (Benton et al., 2024)，变化 改进因子1/ε。

## 概要

本文针对扩散模型的KL散度收敛分析，提出了一种新的生成算法和证明技术。在仅需得分估计精度和有限二阶矩的最小假设下，本文将KL散度收敛的迭代复杂度从先前最优的 $\tilde{O}(d \log^2(1/\delta)/\varepsilon^2)$ 步（Benton et al., 2024）改进为 $\tilde{O}(d \log^{3/2}(1/\delta)/\varepsilon)$ 步（Corollary 3.2）。核心创新在于将生成过程建模为反向ODE步后接一个较小的前向加噪步的组合，并发展新的证明技术来界定得分函数的二阶空间导数（拉普拉斯项），从而实现了KL散度收敛在维度 $d$ 上的线性依赖，同时将精度 $\varepsilon$ 的依赖从二次改进为线性。



扩散模型的生成过程通常基于反向随机微分方程（SDE）或概率流常微分方程（ODE）。先前基于最小假设的KL散度收敛分析（Benton et al., 2024）在精度 $\varepsilon$ 上呈二次依赖（$O(1/\varepsilon^2)$），且需要处理SDE离散化中出现的二阶空间导数项，这些项在之前的扩散模型分析中未出现且无法用现有技术处理。同时，直接适配Li & Cai (2024) 的分析虽然改进了 $\varepsilon$ 依赖，但导致维度依赖变差为 $\tilde{O}(d^{3/2}/\varepsilon)$。因此，在最小假设下同时实现KL散度的线性 $\varepsilon$ 依赖和线性 $d$ 依赖是一个非平凡的问题。



## 核心方法与创新机理

本文的核心创新包括：

1. **生成过程建模创新**：将生成过程建模为反向ODE步后接一个较小的前向加噪步的组合（Algorithm 1）。利用ODE步控制Wasserstein型误差，再通过加噪步将其转换为KL误差，从而获得更好的步长依赖。

2. **证明技术创新**：引入Benton et al. (2023)随机局部化论证的ODE对应物，并发展新的证明技术来界定得分函数的二阶空间导数（拉普拉斯项）。通过Fokker-Planck方程将得分函数的时间导数转化为空间导数，并利用新引理（Lemma A.16, A.17）界定拉普拉斯项，最终实现了线性 $d$ 依赖。

3. **离散化方案创新**：使用指数积分器（Exponential Integrator）离散化经验概率流ODE，步长选择 $h_k = c \min\{1, t_k\}$，实现了 $O(h_k^3)$ 的误差依赖，优于先前SDE方法的 $O(h_k^2)$ 依赖。



![[assets/figures/papers/iclr26_0004_c8Ft3246KD_A_Sharp_KL_Convergence_Analysis_for_Diffusion_Mo/figures/001_Figure_1.jpg]]
*Figure 1: Demonstrating the two updates: (a) along the generation process using sˆ(·) and (b) the forward noising process ( $\mathcal { N } ( \cdot$ ) ) ), of our proposed scheme.

本文提出的生成算法（Algorithm 1）包含两个核心模块：

1. **反向ODE步（生成步）**：使用指数积分器离散化经验概率流ODE，从 $x_k$ 生成 $x_{k-0.5}$，控制Wasserstein型误差。
2. **前向加噪步**：沿前向过程添加小噪声，将Wasserstein误差转换为KL误差。

整体框架如图1所示：

**Figure 1**: Demonstrating the two updates: (a) along the generation process using sˆ(·) and (b) the forward noising process ( $\mathcal { N } ( \cdot ) ) ), of our proposed scheme.



### 5.1 前向过程与反向过程

前向OU过程的解为：

$$
x(t) = e^{-t} y + \sqrt{1 - e^{-2t}} \cdot \epsilon(t), \quad \epsilon(t) \sim \mathcal{N}(0, I_d) \quad \text{(Equation 1)}
$$

反向SDE为：

$$
dx(t) = -x(t) dt - 2 \nabla \ln p_t(x(t)) dt + \sqrt{2} d\bar{w}_t \quad \text{(Equation 2)}
$$

概率流ODE为：

$$
dx(t) = -x(t) dt - s(t, x(t)) dt \quad \text{(Equation 3)}
$$

经验ODE（离散化）为：

$$
d\hat{x}(t) = -\hat{x}(t) dt - \hat{s}(t_k, \hat{x}_k) dt \quad \text{(Equation 4)}
$$

### 5.2 KL散度分解

通过数据处理不等式和链式法则，总KL散度可分解为初始化误差和逐区间条件KL误差之和（Lemma A.2）：

$$
\mathrm{KL}(p_{t_1} \| \hat{p}_{t_1}) \le \mathrm{KL}(p_{t_{K+1}} \| \hat{p}_{t_{K+1}}) + \mathbb{E}_{p_{t_1,\ldots,t_{K+1}}}\left[\sum_{k=2}^{K+1} \mathrm{KL}(p_{t_{k-1}|t_k}(\cdot|x_k) \| \hat{p}_{t_{k-1}|t_k}(\cdot|x_k))\right]
$$

### 5.3 逐区间KL到Wasserstein转换

条件KL散度可转换为按步长缩放的Wasserstein型平方距离（Lemma A.1, Equation 10）：

$$
\mathrm{KL}(p_{t_{k-1}|t_k}(\cdot|x_k) \| \hat{p}_{t_{k-1}|t_k}(\cdot|x_k)) = e^{-2h_{k-1}} \frac{\|x_{k-0.5} - \hat{x}_{k-0.5}\|_2^2}{2(1 - e^{-2h_{k-1}})}
$$

### 5.4 离散化误差界

通过重缩放过程 $z(t)=e^t x(t)$ 和指数积分器离散化，得到离散化误差界（Lemma A.4）：

$$
\mathbb{E}[\|z_{k-0.5} - \tilde{z}_{k-0.5}\|_2^2] \leq \frac{1}{2} (h_k + h_{k-1})^3 \int_{t_{k-2}}^{t_k} e^{4t} \mathbb{E}[\|s_r'(t,z(t))\|_2^2] dt
$$

### 5.5 得分函数时间导数到空间导数转换

通过Fokker-Planck方程将得分函数的时间导数转换为拉普拉斯和雅可比项（Lemma A.9）：

$$
\partial_t s_r(t,z) = e^{2t} \Delta s_r(t,z) + 2 e^{2t} \nabla s_r(t,z)^\top s_r(t,z)
$$

### 5.6 得分导数最终界

重缩放过程得分函数全时间导数的期望平方范数的上界（Lemma A.17）：

$$
\mathbb{E}_{q_t}[\|s_r'(t,z)\|_2^2] \lesssim \frac{d^2 e^{4t}}{(e^{2t}-1)^3} - \frac{e^{2t} d}{(e^{2t}-1)} \frac{d}{dt} \mathbb{E}_{q_t}[\|s_r(t,z)\|^2] - e^{2t} \left( \frac{d}{dt} \mathbb{E}_{q_t}[\|\nabla s_r(t,z)\|_F^2] + \frac{d}{dt} \mathbb{E}_{q_t}[\|s_r(t,z)\|^4] \right)
$$

### 5.7 KL散度最终界

生成分布与真实分布之间KL散度的最终上界（Theorem 3.1, Equation 6）：

$$
\mathrm{KL}(p_{t_1} \| \hat{p}_{t_1}) \lesssim (d + m_2) e^{-T} + d^2 c^3 K + T \varepsilon_{\mathrm{score}}^2
$$



## 实验与关键发现

### 6.1 主要理论结果

| 基准 | 指标 | 本文结果 | 先前最优结果 | 改进 | 锚点 |
|------|------|----------|--------------|------|------|
| 理论分析 | KL散度 | $\tilde{O}(d \log^{3/2}(1/\delta)/\varepsilon)$ | $\tilde{O}(d \log^2(1/\delta)/\varepsilon^2)$ (Benton et al., 2024) | $\varepsilon$ 依赖从二次改进为线性 | Corollary 3.2 |
| 理论分析 | 迭代步数 $K$ | $\Theta(d (\log(1/\delta))^{3/2} / \varepsilon_{\mathrm{score}})$ | $\Theta(d \log^2(1/\delta) / \varepsilon_{\mathrm{score}}^2)$ (Benton et al., 2024) | 改进因子 $1/\varepsilon$ | Corollary 3.2 |

### 6.2 消融分析

1. **ODE步 vs SDE步**：使用ODE步而非SDE步可获得更好的步长依赖 $O(h_k^3)$ 而非 $O(h_k^2)$。这是因为SDE离散化中出现的二阶空间导数项在之前的扩散模型分析中未出现且无法用现有技术处理。

2. **维度依赖改进**：直接适配Li & Cai (2024) 的分析会导致 $d^{3/2}$ 依赖，而本文通过新引理（Lemma A.16, A.17）实现线性 $d$ 依赖。

### 6.3 公平性说明

- 本文为纯理论分析，未在具体数据集上进行实验验证。
- 结果依赖于得分估计精度假设（Assumption 2.1），实际应用中得分估计误差可能影响收敛性。
- 分析针对高斯扰动后的目标分布，而非原始数据分布。



## 定位与知识库关联

本文的方法谱系定位如下：

- **基线方法**：
  - Benton et al. (2024)：先前最优KL收敛结果，基于反向SDE，迭代复杂度 $\tilde{O}(d/\varepsilon^2)$
  - Li & Yan (2024)：TV距离收敛结果，迭代复杂度 $O(d/\varepsilon)$
  - Li & Cai (2024)：二阶离散化分析，改进 $\varepsilon$ 依赖但 $d$ 依赖变差为 $\tilde{O}(d^{3/2}/\varepsilon)$
  - Chen et al. (2023b)：预测-校正采样，使用ODE步和Langevin动力学加噪

- **关键变化**：
  1. **生成过程建模**：从直接模拟反向SDE或概率流ODE变为反向ODE步 + 前向加噪步的组合
  2. **离散化方案**：从标准指数积分器用于SDE或ODE变为指数积分器用于ODE，步长选择 $h_k = c \min\{1, t_k\}$，实现 $O(h_k^3)$ 误差依赖
  3. **误差分析技术**：从利用随机局部化或直接分析SDE离散化误差变为引入ODE对应的随机局部化论证，并发展新引理界定得分函数的拉普拉斯项
  4. **假设条件**：从需要得分函数光滑性或数据分布有界支撑等额外假设变为仅需得分估计精度假设（Assumption 2.1）和有限二阶矩（Assumption 2.2）

- **开放问题**：
  1. 如何在实际应用中精确选择步长参数 $c$ 以平衡误差项？
  2. 本文的KL收敛界是否能推广到其他噪声调度（如方差爆炸过程）？
  3. 能否进一步改进 $\log(1/\delta)$ 项的指数（当前为 $3/2$）？
  4. 本文的证明技术是否能用于分析其他ODE-based采样器（如DPM-Solver）？
  5. 在有限样本情况下，得分估计误差对实际KL散度的影响如何量化？



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Sharp_KL_Convergence_Analysis_for_Diffusion_Models_under_Minimal_Assumptions.pdf

![[paperPDFs/ICLR_2026/A_Sharp_KL_Convergence_Analysis_for_Diffusion_Models_under_Minimal_Assumptions.pdf]]
