---
title: "AC-Sampler: Accelerate and Correct Diffusion Sampling with Metropolis-Hastings Algorithm"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AC-Sampler_Accelerate_and_Correct_Diffusion_Sampling_with_Metropolis-Hastings_Algorithm.pdf
aliases:
- AC-Sampler
acceptance: accepted
tags:
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 不从纯噪声开始逐步去噪，而是在中间时间步直接构建MALA马尔可夫链，利用Metropolis-Hastings校正使样本逼近该时间步的真实边缘分布，从而跳过大量去噪步骤。
primary_logic: 通过定理4.1将密度比分解为可计算项，并训练时间依赖的判别器估计似然比，使得在任意时间步均可计算MH接受概率，从而将加速与误差校正统一在一个无需微调扩散模型的框架中。
claims:
- 在CIFAR‑10无条件生成任务上，AC‑Sampler仅用15.8 NFE就实现FID 2.38，而基础采样器在17 NFE下FID为3.23。
- 在CelebA‑HQ 256×256上，AC‑Sampler以98.3 NFE取得FID 6.6，远低于基线。
- 定理4.3证明，使用最优判别器时，AC‑Sampler生成的分布与真实分布的KL散度不大于原始模型分布的KL散度。
- AC‑Sampler可以与现有加速和校正方法（如DPM‑v3、DG）结合，进一步改善FID和NFE。
paradigm: 通过定理4.1将密度比分解为可计算项，并训练时间依赖的判别器估计似然比，使得在任意时间步均可计算MH接受概率，从而将加速与误差校正统一在一个无需微调扩散模型的框架中。
---

# AC-Sampler: Accelerate and Correct Diffusion Sampling with Metropolis-Hastings Algorithm

> [!tip] 核心洞察
> 通过定理4.1将密度比分解为可计算项，并训练时间依赖的判别器估计似然比，使得在任意时间步均可计算MH接受概率，从而将加速与误差校正统一在一个无需微调扩散模型的框架中。

| 字段 | 内容 |
|------|------|
| 中文题名 | AC-Sampler：利用Metropolis-Hastings算法加速并校正扩散采样 |
| 英文题名 | AC-Sampler: Accelerate and Correct Diffusion Sampling with Metropolis-Hastings Algorithm |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=kWl13kRJTQ) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | AC‑Sampler |
| Dataset | unconditional CIFAR‑10, unconditional CIFAR‑10, unconditional CIFAR‑10 (EDM Heun), unconditional CIFAR‑10 (EDM Heun) |

> [!tip] 效果简介
> - unconditional CIFAR‑10 上，FID 为 2.38，对比 3.23，变化 -0.85。
> - unconditional CIFAR‑10 上，NFE 为 15.8，对比 17，变化 -1.2。
> - unconditional CIFAR‑10 (EDM Heun) 上，FID 为 1.97，对比 2.01，变化 -0.04。

## 概述

扩散模型在图像生成等任务中展现出强大能力，但其迭代去噪过程通常需要数百个时间步，导致采样速度缓慢；同时，反向过程的近似误差会沿时间步累积，使生成分布偏离真实数据分布。AC‑Sampler 针对这一瓶颈，提出了一种无需微调扩散模型的加速与校正框架。核心思路是：不再从纯噪声开始逐步去噪，而是在一个中间时间步启动基于 Metropolis‑Hastings（MH）校正的 Metropolis‑调整 Langevin（MALA）马尔可夫链，利用训练好的时间依赖判别器估计任意时间步的真实边缘密度比，从而可计算 MH 接受概率；通过接受/拒绝机制，使样本分布向该时间步的真实边缘分布收敛，同时跳过大量前置去噪步骤，将加速与误差校正统一起来。

理论分析（定理 4.3）表明，使用最优判别器时，AC‑Sampler 生成分布与真实分布的 KL 散度不大于原始模型，且每增加一次 MALA 校正即可单调降低该 KL 散度（定理 4.4），从理论上保障了校正效果。

在实验上，AC‑Sampler 以更少的时间步（NFE）取得优于或持平基线的质量：CIFAR‑10 无条件生成仅用 15.8 NFE 达到 FID 2.38（基线 17 NFE 下 FID 3.23）；CelebA‑HQ 256×256 无条件生成以 98.3 NFE 取得 FID 6.6；与 EDM 等基础采样器结合后，FID 进一步降至 1.97（NFE 26.19 vs 基线 35）。该方法可与 DPM‑v3、DG 等加速和校正方法兼容，在 ImageNet 条件生成及 Stable Diffusion 文生图等任务中均稳定提升采样效率与样本保真度。

## 背景与动机

扩散模型通过迭代去噪将高斯噪声逐步转换为数据样本，已经成为高保真生成的主流范式。然而，这种逐步反向采样在实用中面临两个紧耦合的瓶颈：**采样效率低**——通常需要成百上千个时间步才能获得逼真图像；**分布偏移**——反向过程的近似误差会沿轨迹累积，使最终生成分布偏离真实的边缘分布，表现为模式坍塌或伪影。现有方法通常将加速与校正视为独立任务分别处理：加速器（如DDIM、DPM++/DPM‑v3）利用 ODE 离散化跳过中间步，但以牺牲精度为代价；校正器（如DG、DiffRS、Restart）通过判别器引导或拒绝采样改善分布对齐，却往往需要额外的训练开销或与加速策略不兼容，未能将两者统一在一个理论框架下。

针对这一缺口，本文的核心动机是**将加速与误差校正统一在 Metropolis‑Hastings（MH）框架中**，实现从“先加速、后校正”到“边加速、边校正”的范式转变。其关键因果机制在于：不从纯噪声开始逐步去噪，而是在一个中间时间步 $\tau$ 处直接启动 **MALA（Metropolis‑adjusted Langevin algorithm）马尔可夫链**，利用预训练的得分网络提出候选样本，并通过 MH 接受概率决定是否接受该候选。在这个设计中，跳过 $\tau$ 之后的早期去噪步带来了加速；而 MH 校正使链的稳态分布逼近该时间步的真实边缘分布 $q_\tau$，从而消除了累积的离散化误差。

实现上述机制的障碍是，MH 接受概率中的真实边缘密度比 $q_t(\tilde{\mathbf{x}}_t)/q_t(\mathbf{x}_t)$ 无法直接计算。本文通过定理4.1将密度比分解为三项：前向噪声项、时间依赖的似然比项、以及反向转移核项。前向项和反向项均可由扩散过程的已知结构给出，而似然比项则由一个**时间依赖判别器**估计。该判别器仅需区分模型生成的中间样本与真实中间样本，训练成本远低于扩散模型本身，且无需对扩散模型进行微调。基于此，在任何时间步均可计算可用的 MH 接受概率（Eq. 9），从而将采样加速与统计校正统一在可计算的 MH 链中。

实验证据初步表明这一动机的合理性：在无条件 CIFAR‑10 生成上，AC‑Sampler 仅用 15.8 NFE 实现了 FID 2.38，而基础采样器在 17 NFE 时 FID 为 3.23（Abstract）；与高阶加速器 EDM Heun 结合时，进一步将 FID 从 2.01 降至 1.97 且 NFE 从 35 降至 26.19（Table 1）。此类结果暗示，通过 MH 校正，中间步采样不仅可行，而且能在更少计算量下修复采样器的固有偏差。同时，理论分析（Theorem 4.3）证明：使用最优判别器时，AC‑Sampler 生成分布与真实数据分布的 KL 散度不大于原始模型分布的 KL 散度，为校正增益提供了严格保证。

综上，AC‑Sampler 的提出源自三个观察：（1）扩散采样的速度瓶颈源于对早期纯噪声步的冗余计算；（2）现有加速方法因忽略累积误差而需要额外的校正后处理；（3）MH 算法天然适合在中间步构造稳态分布，但需解决密度比估计问题。通过引入时间依赖判别器和定理4.1的密度比分解，本文使得“加速＋校正”成为一套无需微调、正交于其他加速器的通用解法。

## 核心创新

AC‑Sampler针对扩散模型采样速度慢、反向过程近似误差累积两大瓶颈，提出**中间时间步直接启动MALA链 + Metropolis‑Hastings校正**的统一框架，无需对预训练扩散模型做任何微调。核心思想可归纳为一个因果调节旋钮：不从纯噪声开始逐步去噪，而是在中间时间步$\tau$处构造基于分数的Langevin提案分布，利用MH接受/拒绝机制将样本修正到该时间步的真实边缘分布$q_\tau$，从而跳过大段去噪步骤，同时消除分布偏移。

与传统采样器相比，AC‑Sampler改变了以下关键设计槽（changed slots），构成其创新的结构化支撑：

- **采样起始点**：基线从$t=T$的高斯先验出发，逐步去噪至$t=0$；AC‑Sampler从$t=T$快速（少量NFE）去噪至目标时间步$\tau$，在此处启动MALA链（Figure 1）。这直接缩短了后续去噪路径，提供加速增益。
- **提案分布**：在$\tau$处不再依赖预训练的去噪转移核作为唯一提案来源，而是采用基于得分网络的Langevin提案分布$p_{\text{proposal}}^\theta(\cdot|\mathbf{x}_\tau) = \mathcal{N}\big(\mathbf{x}_\tau + \frac{\eta}{2}\mathbf{s}^\theta(\mathbf{x}_\tau,\tau), \eta \mathbf{I}\big)$（Eq. 5）。该分布与后续去噪步骤共享同一得分输出，避免了额外网络评估。
- **接受/拒绝机制**：基线采样无校正步骤，误差随去噪过程累积。AC‑Sampler引入MH校正，但核心难点在于真实边缘分布$q_\tau$的密度比不可直接计算。通过定理4.1（Eq. 6）将$q_\tau$的两个样本之间的密度比分解为前向项、似然比项和反向转移核项，并选择特定$\hat{\mathbf{x}}_{\tau-1}$使反向项抵消，得到可计算的接受概率$\hat{\alpha}$（Eq. 9）。其关键是**时间依赖判别器**：以加权二元交叉熵（Eq. 8）训练判别器估计似然比$L_\tau(\mathbf{x}_\tau,\tau)$，使得MH接受概率在任意时间步均可计算。
- **链设计**：不同于传统MH保留拒绝状态的做法，AC‑Sampler采用“propose‑until‑accept”设计（Algorithm 1），重复提案直到一个样本被接受，从而鼓励链探索新区域，提高多样性与保真度。

上述设计使加速与校正统一在一个框架中。理论保证方面，定理4.3（Eq. 11）证明：当使用最优判别器时，AC‑Sampler生成分布与真实分布的KL散度不大于原始模型分布的KL散度；定理4.4（Eq. 12）进一步表明每增加一次MALA校正，KL散度单调不增。这些结论为校正提供了严格上界。

实验证据强烈支撑了这一创新有效性：在CIFAR‑10无条件生成上，AC‑Sampler仅用15.8 NFE即取得FID 2.38，而基础采样器在17 NFE下FID为3.23；在CelebA‑HQ 256×256上，以98.3 NFE实现FID 6.6（远低于基线）。更重要的是，AC‑Sampler能与现有加速（如DPM‑v3）和校正（如DG）方法正交叠加，进一步改善指标（Table 1, Table 2）。消融研究证实，去除MH校正会导致FID显著恶化，且propose‑until‑accept设计相比传统MH提升了召回率和保真度（Table 7, Figure 5）。

需注意的局限：该方法需额外训练一个时间依赖判别器，超参数（如$\tau$、信噪比SNR）需针对任务手动调节；理论分析依赖最优判别器与无限链长假设，实际中只能近似满足。尽管存在这些成本，AC‑Sampler通过改变采样起始点、引入可计算密度比的判别器、施加MH校正，成功将扩散采样加速与分布校正融为一体，展现出明晰的创新逻辑和实证收益。

## 整体框架

![[obsidian-vault/assets/figures/papers/repair_max_kWl13kRJTQ_AC_Sampler/figures/001_Figure_1.jpg]]
*Figure 1: Overall figure of AC-Sampler*

AC‑Sampler 是一种无需微调扩散模型即可同时实现采样加速与分布校正的架构。其核心思想是：不从纯噪声开始执行数百步去噪迭代，而是先将样本快速推至某个中间时间步 $\tau$，在该截面上构造一条 **Metropolis‑Adjusted Langevin Algorithm (MALA)** 马尔可夫链，利用 **Metropolis‑Hastings (MH)** 校正使链的稳态分布逼近该时间步的真实边缘分布 $q_\tau$，从而跳过大量低效的去噪步骤，并矫正由反向过程近似误差累积导致的分布偏移。

### 整体流程

AC‑Sampler 的管线由五个模块顺次组成，其输入为预训练的扩散得分网络 $\mathbf{s}^{\theta}(\mathbf{x}_t, t)$ 及额外训练的时间依赖判别器 $d^{\phi}(\mathbf{x}_t, t)$，输出为最终清洁样本 $\mathbf{x}_0$。流程如下（参考 Figure 1）：

1. **初始快速去噪至 $\tau$**  
   从标准高斯先验 $\mathbf{x}_T \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 出发，使用基础采样器（如 EDM Heun、DDIM、DPM‑v3 等）以极少的函数评价次数（NFE）快速降噪至选定的中间时间步 $\tau$。这一步将样本从几乎纯噪声的区域推进到尚含大量结构的中间区域，为后续马尔可夫链提供一个较好的起点，并显著缩短了从 $T$ 到 $0$ 的完整路径。

2. **MALA 提案分布**  
   在时间步 $\tau$ 处，不再继续沿确定性的逆扩散轨迹推进，而是基于当前样本 $\mathbf{x}_\tau$ 和预训练得分网络构造一个高斯提案分布：
   $$p_{\mathrm{proposal},\tau}^{\theta}(\cdot|\mathbf{x}_\tau) = \mathcal{N}\Big(\mathbf{x}_\tau + \frac{\eta}{2}\,\mathbf{s}^{\theta}(\mathbf{x}_\tau, \tau),\; \eta \mathbf{I}\Big).$$
   该分布源自 Euler–Maruyama 离散化下的过阻尼 Langevin 动力学，其中步长 $\eta$ 通过自适应保持恒定信噪比（SNR）来调节扰动强度。每次提案仅需一次额外的得分网络评估，因此新增 NFE 极为有限。

3. **时间依赖判别器计算似然比**  
   为了计算 MH 接受概率中的密度比 $q_\tau(\tilde{\mathbf{x}}_\tau) / q_\tau(\mathbf{x}_\tau)$，AC‑Sampler 引入一个与时间步 $t$ 相关的判别器 $d^{\phi}(\mathbf{x}_t, t)$。该判别器通过时间加权的二元交叉熵损失训练，用于区分来自真实前向扩散的样本与由模型反向过程生成的样本：
   $$\mathcal{L}_{\mathrm{BCE}}(\phi) = \int \lambda(t)\Bigl[ \mathbb{E}_{\mathbf{x}_t \sim q_t}[-\log d^{\phi}(\mathbf{x}_t, t)] + \mathbb{E}_{\mathbf{x}_t \sim p^{\theta}_t}[-\log(1-d^{\phi}(\mathbf{x}_t, t))] \Bigr] dt.$$
   当判别器达到最优时，其输出与似然比存在一一对应关系，从而可以给出 $L_t(\mathbf{x}_t,t) \triangleq \frac{d^{\phi}(\mathbf{x}_t,t)}{1-d^{\phi}(\mathbf{x}_t,t)}$ 作为密度比的估计。**定理 4.1** 进一步将任意两个样本的边缘密度比分解为三个可计算项：前向转移核比值、似然比比值和反向转移核比值。通过特定选择中间变量 $\hat{\mathbf{x}}_{t-1}$，反向核项可以抵消，最终得到一个完全可计算的 MH 接受概率（公式 9）：
   $$\hat{\alpha} = \min\!\left(1,\; \frac{q_{\tau|\tau-1}(\tilde{\mathbf{x}}_\tau|\hat{\mathbf{x}}_{\tau-1})}{q_{\tau|\tau-1}(\mathbf{x}_\tau|\hat{\mathbf{x}}_{\tau-1})} \cdot \frac{\tilde{L}}{L} \cdot \frac{p_{\mathrm{proposal},\tau}^{\theta}(\mathbf{x}_\tau|\tilde{\mathbf{x}}_\tau)}{p_{\mathrm{proposal},\tau}^{\theta}(\tilde{\mathbf{x}}_\tau|\mathbf{x}_\tau)}\right).$$

4. **MH 校正（accept/reject）**  
   对于从提案分布中抽取的候选样本 $\tilde{\mathbf{x}}_\tau$，根据上述接受概率决定接受或拒绝。AC‑Sampler 采用 **propose‑until‑accept** 设计：反复产生提案直到某个候选被接受，并仅记录被接受的样本（算法 1）。这种做法避免了传统 MH 中因拒绝而停滞在同一状态的问题，有助于提升样本多样性和模式覆盖。在理论上，每增加一次 MALA 校正步，生成分布与真实分布的 KL 散度单调不增（定理 4.4），且在最优判别器下，校正后的分布与真实分布的 KL 散度不大于原始模型（定理 4.3）。

5. **最终去噪至 0**  
   从时间步 $\tau$ 经 MH 校正后得到的样本 $\mathbf{x}_\tau^*$ 被送入基础采样器，继续从 $\tau$ 快速去噪到 $t=0$，产生最终图像。这一段路径极短，几乎不引入额外误差。

### 模块关系与正交性

上述流程中，初始快速去噪和最终去噪保留了预训练扩散模型本身的所有结构；MALA 提案与 MH 校正则是在中间截面施加的最小侵入性干预。判别器独立训练于扩散模型之外，其训练代价远低于扩散模型本身。更重要的是，AC‑Sampler 整体上 **正交** 于现有的加速采样器（如 DPM‑v3、DDIM）和校正方法（如 DG、Restart）。实证中，将 AC‑Sampler 直接加载到 EDM Heun、ScoreSDE KAR1/KAR2 或 Stable Diffusion 之上，均能稳定降低 FID 并减少 NFE，无需任何微调（见表 1‑5）。

### 输入输出抽象

- **输入**：预训练的得分网络 $\mathbf{s}^{\theta}$（或等价的去噪模型）；时间依赖判别器 $d^{\phi}$；用户指定的目标时间步 $\tau$ 和信噪比 SNR；基础采样器的配置（如阶数、步长策略）。
- **输出**：经过加速与校正的生成样本 $\mathbf{x}_0$，以及与仅使用基础采样器相比更低的 FID、更少的 NFE。
- **跨方法适配**：AC‑Sampler 只需要目标扩散模型提供 `score(x, t)` 接口，判别器需要预提取的图像特征（对于潜在扩散则使用随机初始化特征提取器）；对文本条件模型则通过条件维度注入实现，整体改动极小。

综上，AC‑Sampler 通过“**快进→中间截面 MALA 链 + MH 校正→快出**”的架构，将扩散采样的加速与误差校正统一在单一框架内，无需对原扩散模型重新训练，并与现行主流的加速和校正策略高度兼容。

## 核心模块与公式推导

AC‑Sampler 的核心思想是跳过从高斯先验 $t = T$ 逐步去噪至 $t = 0$ 的低效过程，改为**在中间时间步 $\tau$ 启动 Metropolis‑Hastings (MH) 校正的 Markov 链**，使生成样本直接逼近该时间步的真实边缘分布 $q_{\tau}(\mathbf{x}_{\tau})$，随后再用少量去噪步转换到图像空间。整个框架包含以下联动模块（Figure 1）：

1. **初始快速去噪**：从纯噪声 $\mathbf{x}_T$ 使用少步 ODE/SDE 采样器快速推进到目标时间步 $\tau$，大幅缩短后续路径长度。
2. **MALA 提案分布**：在 $\tau$ 处利用预训练得分网络 $\mathbf{s}^\theta(\mathbf{x}_t, t)$ 构造 Langevin 动力学的高斯提案。该提案不仅可高效探索空间，而且与去噪步**共享同一得分输出**，避免了额外网络评估（NFE）。
3. **时间依赖判别器**：为计算 MH 接受概率中不可直接获取的似然比 $q_t(\mathbf{x}_t)/p_t^\theta(\mathbf{x}_t)$，训练一个判别器 $d^\phi(\mathbf{x}_t, t)$，通过二元交叉熵损失区分真实边缘样本与模型生成样本。
4. **MH 校正 (accept/reject)**：基于密度比分解定理（Theorem 4.1）将接受概率转化为仅由前向项、提案项和判别器似然比构成的**可计算形式**。采用 propose‑until‑accept 设计（Algorithm 1），反复抽取候选样本直至接受，仅保留接受样本，从而提升多样性与保真度。
5. **最终去噪**：从校正后的 $\mathbf{x}_\tau$ 继续去噪至 $t = 0$ 得到最终图像。

下面逐项解析关键公式及其变量含义。

### 1. 提案分布（MALA 步）

在时间步 $t$，给定当前样本 $\mathbf{x}_t$，AC‑Sampler 的提案分布为：

$$ p_{\mathrm{proposal},t}^{\theta}(\cdot|\mathbf{x}_t) = \mathcal{N}\left(\mathbf{x}_t + \frac{\eta}{2} \mathbf{s}^{\theta}(\mathbf{x}_t, t), \eta \mathbf{I}\right) \tag{Eq. 5} $$

式中：
- $\mathbf{s}^\theta(\mathbf{x}_t, t)$：预训练得分网络输出的得分函数；
- $\eta$：步长，根据目标时步的信噪比 (SNR) 动态调整以保持恒定 SNR；
- 该分布是 overdamped Langevin 动力学的 Euler–Maruyama 离散形式，其均值为沿得分方向移动，协方差为 $\eta\mathbf{I}$。

### 2. 密度比分解与接受概率

为了在没有 $q_t$ 显式表达式的前提下计算 MH 接受概率，Theorem 4.1 将任意两个样本在时间步 $t$ 的真实边缘分布密度比分解为可计算项：

$$ \frac{q_t(\tilde{\mathbf{x}}_t)}{q_t(\mathbf{x}_t)} = \frac{q_{t|t-1}(\tilde{\mathbf{x}}_t|\mathbf{x}_{t-1})}{q_{t|t-1}(\mathbf{x}_t|\mathbf{x}_{t-1})} \cdot \frac{L_t(\tilde{\mathbf{x}}_t, t)}{L_t(\mathbf{x}_t, t)} \cdot \frac{p_{t-1|t}^{\theta}(\mathbf{x}_{t-1}|\mathbf{x}_t)}{p_{t-1|t}^{\theta}(\mathbf{x}_{t-1}|\tilde{\mathbf{x}}_t)} \tag{Theorem 4.1} $$

其中：
- 第一个分式是**前向扩散转移核**之比，可直接由高斯分布算出；
- 第二个分式是**似然比** $L_t(\mathbf{x},t) := q_t(\mathbf{x})/p_t^\theta(\mathbf{x})$，该项由判别器估计；
- 第三个分式是**反向去噪转移核**之比，当选择特定的 $\hat{\mathbf{x}}_{t-1}$（如从当前样本反向估计的期望）时，该项可被约去，从而简化接受概率。

结合提案分布和判别器输出的似然比估计 $\tilde{L} = d^\phi/(1-d^\phi)$（或类似形式），MH 接受概率被构造为如下的全可计算形式：

$$ \hat{\alpha}(\mathbf{x}_t, \tilde{\mathbf{x}}_t, \mathbf{s}, \tilde{\mathbf{s}}, L, \tilde{L}) = \min\left(1, \frac{q_{t|t-1}(\tilde{\mathbf{x}}_t|\hat{\mathbf{x}}_{t-1})}{q_{t|t-1}(\mathbf{x}_t|\hat{\mathbf{x}}_{t-1})} \cdot \frac{\tilde{L}}{L} \cdot \frac{p_{\mathrm{proposal},t}^{\theta}(\mathbf{x}_t|\tilde{\mathbf{x}}_t)}{p_{\mathrm{proposal},t}^{\theta}(\tilde{\mathbf{x}}_t|\mathbf{x}_t)}\right) \tag{Eq. 9} $$

此处的 $\hat{\mathbf{x}}_{t-1}$ 可由当前样本 $\mathbf{x}_t$ 通过预训练模型的单步反向转移估计得到，使得最终接受概率仅依赖于前向项（解析可算）、判别器似然比（网络输出）和提案比（对称或可算）。

### 3. 判别器训练

为获得似然比，AC‑Sampler 训练一个时间依赖的判别器 $d^\phi(\mathbf{x}_t, t)$，其损失函数为时间加权的二元交叉熵：

$$ \mathcal{L}_{\mathrm{BCE}}(\phi) = \int \lambda(t) \left[ \mathbb{E}_{\mathbf{x}_t \sim q_t} [-\log d^{\phi}(\mathbf{x}_t, t)] + \mathbb{E}_{\mathbf{x}_t \sim p_t^{\theta}} [-\log (1-d^{\phi}(\mathbf{x}_t, t))] \right] dt \tag{Eq. 8} $$

- $\lambda(t)$：时间相关的权重，用于平衡不同噪声尺度的训练信号；
- 训练样本来自真实分布 $q_t$ 和当前模型边缘分布 $p_t^\theta$；
- 最优判别器满足 $d^\phi \approx \frac{q_t}{q_t + p_t^\theta}$，从而可以恢复似然比 $L_t$。

### 4. 理论保证

AC‑Sampler 在最优判别器下的分布质量有严格保证。令 $p_0^{\theta}$ 为原始模型生成的分布，$p_0^{\theta,\phi^*}$ 为使用最优判别器校正后的分布，则有：

$$ D_{KL}(q_0(\mathbf{x}_0) || p_0^{\theta,\phi^*}(\mathbf{x}_0)) \leq D_{KL}(q_0(\mathbf{x}_0) || p_0^{\theta}(\mathbf{x}_0)) \tag{Theorem 4.3, Eq. 11} $$

即校正后的分布与真实分布的 KL 散度不高于原始模型，表明 AC‑Sampler **不会损害生成质量**。

进一步，每增加一次 MALA 校正步，KL 散度单调不增：

$$ D_{KL}(q_0 || p_0^{\theta,\phi^*,(l+1)}) \leq D_{KL}(q_0 || p_0^{\theta,\phi^*,(l)}) \tag{Theorem 4.4, Eq. 12} $$

这证明了迭代 MH 校正的收敛性质，为 propose‑until‑accept 多次采样提供了理论支持。

综上，AC‑Sampler 通过**密度比分解 + 判别器估计 + MALA 提案**将扩散采样的加速与校正统一在无需微调扩散模型的框架下，使得在有限 NFE 下同时实现速度提升和分布对齐成为可能。

## 实验与分析

![[obsidian-vault/assets/figures/papers/repair_max_kWl13kRJTQ_AC_Sampler/figures/003_Table_1.jpg]]
*Table 1: Performance on unconditional CIFAR-10 generation. Values that are better compared to the baseline are highlighted in bold*

![[obsidian-vault/assets/figures/papers/repair_max_kWl13kRJTQ_AC_Sampler/figures/004_Table_2.jpg]]
*Table 2: Performance on unconditional CIFAR-10 generation with (Top) correction and (Bottom) acceleration methods*

![[obsidian-vault/assets/figures/papers/repair_max_kWl13kRJTQ_AC_Sampler/figures/005_Table_3.jpg]]
*Table 3: FID and NFE on unconditional CelebA-HQ 256 generation*

![[obsidian-vault/assets/figures/papers/repair_max_kWl13kRJTQ_AC_Sampler/figures/002_Figure_2.jpg]]
*Figure 2: FID–NFE graph on uncond. CIFAR-10: (Top) Correction methods (Bottom) Acceleration methods*

![[obsidian-vault/assets/figures/papers/repair_max_kWl13kRJTQ_AC_Sampler/figures/012_Figure_5.jpg]]
*Figure 5: Effect of an Figure 6: Mode cover MH correction on AC- with different τ in 25- Sampler. Gaussian toy experiment*

AC‑Sampler 的核心主张是通过中间时间步的 MH 校正同时实现采样加速与分布校正，且无需微调扩散模型。下面从多类基准的主结果出发，分析性能增益的来源、消融证据以及当前方法的局限。

### 主要结果：加速与校正的协同增益

**无条件 CIFAR‑10（32×32）**
在低分辨率的经典基准上，AC‑Sampler 对多种基础采样器均产生一致的改进。以 EDM（Heun）为基础时，FID 由 2.01（35 NFE）降至 **1.97（26.19 NFE）**（Table 1）；当与校正方法 DG 组合后，FID 进一步降至 **1.84**，NFE 反而略减（Table 1、Table 2）。在极低 NFE 区间，AC‑Sampler 将基础 ScoreSDE（KAR1）的 FID 从 3.23（17 NFE）大幅压缩至 **2.38（15.8 NFE）**——这直接证明了跳过大量去噪步并通过 MH 校正在中间时间步修复分布偏差的有效性。

**无条件 CelebA‑HQ 256×256**
在更高分辨率的人脸生成上，以 ScoreSDE（KAR2）为基线的 FID 从 29.74（198 NFE）骤降至 **6.60（98.3 NFE）**（Table 3），降幅达 77.8%。同时支持 marginal 与 joint 两种 MALA 模式（Table 9），其中 joint 模式下的 NFE 更少但 FID 略有回升，体现了空间‑时间联合提案带来的额外加速。

**条件 ImageNet 64×64 与 256×256**
在条件生成场景下，AC‑Sampler 仍保持了温和但一致的 FID 改善（例如 64×64 上 FID 2.30→2.25，NFE 61→58.75；256×256 也呈现相似趋势，Table 4）。由于训练分类器引导的扩散模型本身已经达到了较高保真度，此处 AC 的边际增益主要来自 NFE 的缩减，说明加速机制对条件扩散同样适用。

**文本到图像生成（Stable Diffusion v1.5）**
在大型潜在扩散模型上，AC‑Sampler 以 DDIM 采样器为基线，将 FID 从 24.34 降至 **23.16**，CLIP Score 和 GenEval Overall Score 也有小幅提升（Table 5）。这些定量收益与图 3 中的定性对比一致：红框标出的基线结构错误（如肢体畸形）在 AC‑Sampler 的生成结果中得到修正，表明 MH 校正在隐空间同样有效。

综合以上实验结果，AC‑Sampler 的核心增益可归因于两点：**加速增益**（从 τ 处直接采样减小 NFE）与**校正增益**（通过辨别器驱动的 MH 步将样本拉近真实边缘分布 $q_\tau$）。二者叠加使得在几乎不牺牲甚至提升生成质量的前提下大幅削减计算开销。图 2 的 FID–NFE 曲线进一步强调了这一正交性：AC‑Sampler 的 Pareto 前沿系统地优于纯加速方法（如 DPM‑v3）、纯校正方法（如 DG）及其它拒绝/重启类方法。

### 消融研究：关键组件的因果证据

**MH 校正的必要性。** 移除 MH 接受/拒绝步骤后，FID 显著恶化（图 5），说明单纯在 τ 处执行 Langevin 提案而不做校正无法得到 $q_\tau$ 的良好近似，进而污染后续去噪。这正是理论分析中密度比分解定理（Theorem 4.1）的实证映照：辨别器提供的似然比是接受概率中不可或缺的项。

**Propose‑until‑accept 设计。** 与传统 MH（保留拒绝状态）相比，算法 1 的“提议直到接受”策略在 FID、NFE 和 Recall 上均有提升（Table 7）。传统 MH 容易在哑铃状分布中滞留于某个模式；重复提议则迫使链的跳跃，提高模式覆盖。这在 25‑高斯试玩实验（图 8）中得到生动印证：DDPM 基准平均漏掉约 1.5 个模式，而 AC‑Sampler 覆盖了全部 25 个模式。

**判别器质量与训练轮次。** 判别器训练 epoch 增加持续改善 FID，但即使不完美的判别器仍能带来收益（Table 25）。这表明只要似然比估计大致可靠，MH 步就能将分布向 $q_\tau$ 推动。附录中还显示，使用预训练特征提取器对像素空间扩散十分关键；潜在扩散模型（如 SD）因缺乏现成提取器，随机初始化的特征提取可能限制判别力，成为潜在的一大瓶颈。

**超参数 τ 与 SNR。** Table 8 与 Table 10 的网格搜索表明，最优 τ 通常落在总步数的 1/2 至 3/4 区间，SNR 在 0.1–0.25 附近。偏离这些区间会导致接受率过低或提案方差过大，拉低效率。这一敏感性说明目前仍需手动调参，缺乏自动化的最优选择机制。

### 与其他加速/校正方法的正交性

AC‑Sampler 设计为插拔式模块，可与现有加速（DPM‑v3）和校正（DG）方法直接融合。例如，在 CIFAR‑10 上 AC 结合 DG 取得 FID 1.84、NFE 26.19，优于任何单一方法。这种正交性源于 AC‑Sampler 修改的是中间时间步的采样策略，而其他方法修改的是两端路径或整体调度，因此双方不冲突。这为未来搭建多层次采样方案提供了参照。

### 失败模式与当前限制

尽管实验表现强劲，但方法存在若干结构性局限：
1. **额外训练成本。** 时间依赖辨别器的训练虽然远低于扩散模型，但仍引入了独立的前期训练阶段，对快速部署不友好。
2. **潜在扩散中的判别器质量限制。** 在 Stable Diffusion 等隐空间模型上，无法直接使用成熟的像素分类器特征提取器，只能用随机初始化骨干，制约了似然比估计的上限。
3. **超参数敏感性。** τ 与 SNR 的选择对性能影响较大，且不同任务/模型间最优值不通用，需要逐个调参。
4. **理论假设的近似性。** 理论界基于最优辨别器和无限链长，实际中只能逼近，且 propose‑until‑accept 虽实用但会引入微小的稳态偏差。
5. **高分辨率下的可扩展性。** 现有实验限于 CIFAR‑10 到 CelebA‑HQ 256 和 ImageNet 256，在更大规模（如 1024×1024）下的资源消耗和效率平衡尚未验证。

这些局限并非根本性缺陷，但指出了后续研究的几个明确方向：自监督或轻量级判别器训练、自动选参机制，以及为隐空间模型定制特征提取骨干等。

综上所述，AC‑Sampler 通过引入一个简洁的 MH 校正环，在多个生成基准上实现了采样加速与分布精度的同步提升。消融实验明确了 MH 校正、propose‑until‑accept 和判别器质量对最终性能的关键作用，同时局限性分析为其工程化落地和进一步改进提供了切入点。

## 方法谱系与知识库定位

AC-Sampler 处于扩散模型采样加速与分布校正两条路线的交叉位置，但并非简单的增量改造，而是通过 Metropolis-Hastings (MH) 校正将两者统一为一个 **无需微调扩散模型** 的插件式框架。在方法谱系上，它既不属于纯 ODE/SDE 加速器（DDIM、DPM++、DPM-v3、EDM），也不属于纯校正器（DG、DiffRS、Restart），而是作为 **第三极**：利用中间时间步的 MALA 马尔可夫链，借助时间依赖判别器估计的密度比，同时对采样轨迹进行“跳步加速”与“误差校正”。这种设计使得 AC-Sampler 可以与现有加速/校正器正交叠加，如 Table 1 和 Table 2 所示，在 EDM Heun、DPM-v3、DG 等基线上均稳定提升 FID 并降低 NFE，具备广泛的即插即用能力。

### 与 baseline/follow-up 的关系

**纯加速方法**（DDIM、DPM++、DPM-v3、EDM Heun）通过优化数值求解器或跳步策略来降低 NFE，但缺乏对中间步分布漂移的校正机制。AC-Sampler 在加速基础上引入 MH 校正，使得在相同 NFE 下分布比肩甚至超越原模型。例如在无条件 CIFAR-10 上，EDM Heun 以 35 NFE 达到 FID 2.01，而 AC-Sampler 以 26.19 NFE 即取得 1.97（Table 1），且 NFE 越少相对增益越显著（Table 2）。这说明 AC-Sampler 与加速器不是竞争关系，而是 **互补关系**：加速器提供初始去噪至 τ 的高效路径，AC-Sampler 再通过 MALA 链校正中间分布。

**纯校正方法**（DG、DiffRS、Restart）通常沿原有去噪路径重采样或判别器修正，但未改变采样起始点。DG 用判别器微调扩散模型；DiffRS 用拒绝采样在每一步修正；Restart 反复执行前进-后退步。AC-Sampler 与之不同：它不是在整个轨迹上做细粒度修正，而是 **跳至中间时间步 τ 直接构建目标分布对齐的马尔可夫链**，利用 MH 接受概率将校正集中在信息丰富但分布偏差严重的中间阶段。这种“空间换质量”的思路既减少了总 NFE，又放宽了对每一步反向转移核精确性的依赖。实验中，AC-Sampler 在 CIFAR-10 上与 DG 组合后 FID 从 1.93 降至 1.84，NFE 从 27 降至 26.19（Table 1），进一步验证了正交性。

**潜在扩散模型（如 Stable Diffusion）** 上的表现显示方法泛化能力：AC-Sampler 在 SD-v1.5 上将 FID 从 24.34 降至 23.16，GenEval 总分从 0.4219 升至 0.4453（Table 5）。然而，由于缺乏预训练的分类器特征提取器，SD 实验中使用随机初始化提取器，可能限制判别器质量，这暗示该方法对判别器训练的依赖会在非图像域或特征提取有限的场景下构成约束。

### 适用边界

基于现有实验，AC-Sampler 在以下条件下收益明显：
- **无条件或条件像素级生成**（CIFAR-10、CelebA-HQ、ImageNet 64×64/256×256），FID 降幅在 0.04~0.85 之间，NFE 降幅可达数十步（Table 1-4）；
- **低 NFE 预算场景**：在 NFE 受限（如 15~30）时，校正带来的分布改善远大于少量的额外 NFE，FID 降幅可达 0.8 以上（Abstract）；
- **需要保留原模型参数不允许微调的场景**：AC-Sampler 仅需训练判别器，扩散模型本身冻结，适配成本远低于重新训练。

其性能对超参数敏感：τ（目标时间步）和信噪比 SNR 是核心旋钮，τ 在 T/2 至 3T/4、SNR 在 0.1‑0.25 时最优（Table 8, appendix）。τ 过小则校正过早（信息不足），过大则路径缩短有限，均会导致 FID 回升。这表明对每个任务需要一定的人工调参成本，自动化 τ/SNR 选择机制尚不存在。

判别器质量是另一关键：即便不完美训练的判别器也能带来正向增益（Table 25 显示判别器 epoch 增加持续改善 FID），但最优判别器存在理论保证（Theorem 4.3）。在潜在扩散模型中因特征提取器问题，判别器表现可能打折扣，这可能是潜在空间方法推广的主要阻力之一。

### 局限

1. **额外训练开销**：需为每个预训练扩散模型训练时间依赖判别器，虽然成本远低于扩散模型训练，但仍增加了部署前的准备步骤。
2. **潜在空间模型的适配难度**：在 Stable Diffusion 等潜在扩散模型中，像素级特征提取器不可用，随机初始化的提取器会限制似然比估计精度。
3. **超参数敏感性**：τ 和 SNR 等关键参数依赖任务手动搜索，尚无法自适应确定。
4. **理论假设与实际差距**：Theorem 4.3 的 KL 散度上界依赖于最优判别器和无限链长，实践中只能近似；propose‑until‑accept 设计虽提升了多样性（Table 7），但可能偏离严格意义上的 MCMC 稳态分布，偏差量化尚不充分。
5. **高分辨率下的可扩展性**：在 ImageNet 256×256 和更大尺度上，报告的数据（Table 4）存在但相对稀少，且判别器训练开销和 NFE 效率是否线性缩放需更多验证。

### 开放问题

- **在线/自监督判别器训练**：能否通过学生‑教师范式的自监督方式减少对预训练特征提取器的依赖，尤其在潜在空间或非图像模态？
- **τ 和 SNR 的自动选择**：能否基于模型噪声尺度或数据特性设计自适应策略，甚至与采样过程耦合？
- **连续时间流程模型的兼容性**：AC-Sampler 在 Flow Matching 等无扩散前向过程的模型中是否适用，密度比分解如何修改？
- **大规模下的资源‑质量平衡**：在更大的数据集和更高分辨率下，判别器训练和 MALA 链条数的能耗/延迟如何优化，是否能保持与 FID 收益相当的 wall‑clock 提升？
- **propose‑until‑accept 的分布偏差**：该设计将传统 MH 过程改造为有偏链以提高效率，能否从理论上给出偏差上界，抑或证明其在某种意义下等价于某种加速的 MCMC 变体？

以上问题表明，AC-Sampler 作为将 MCMC 校正引入扩散采样的先行框架，其“跳步+校正”的核心思路仍存在大量优化空间，尤其在自动化、跨模态迁移以及理论完备性方面，值得后续工作探索。

## 原文 PDF

## 相关样本

- [[obsidian-vault/analysis/ICLR_2026/Adaptive_Moments_are_Surprisingly_Effective_for_Plug-and-Play_Diffusion_Sampling.md|Adaptive Moments]]：同属 diffusion sampling 样本，可对照 MCMC 校正与梯度矩估计稳定化。

![[obsidian-vault/paperPDFs/ICLR_2026/AC-Sampler_Accelerate_and_Correct_Diffusion_Sampling_with_Metropolis-Hastings_Algorithm.pdf]]
