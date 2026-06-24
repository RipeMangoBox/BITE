---
title: "Improving Reasoning for Diffusion Language Models via Group Diffusion Policy Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Improving_Reasoning_for_Diffusion_Language_Models_via_Group_Diffusion_Policy_Optimization.pdf
openreview_forum_id: JaqvespRBP
aliases:
- GDPOG
- IRDLMGDPO
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "半确定性蒙特卡洛（Semi-deterministic Monte Carlo, SDMC）积分方案：通过固定时间点、使用高斯求积并减少内层蒙特卡洛采样，显著降低 ELBO 估计的方差和偏差。"
primary_logic: "ELBO 方差主要由随机时间采样主导，而非随机掩码；损失函数随时间变化呈现平滑、可预测的简单形态，因此适合用确定性数值积分近似以抑制方差。"
claims:
- "随机时间主导 ELBO 方差"
- "SDMC 估计器比双蒙特卡洛具有更低的偏差和方差"
- "GDPO 在数学、推理和编码基准上显著优于 diffu-GRPO"
- "仅需 2–3 个求积点即可获得大部分收益"
---

# Improving Reasoning for Diffusion Language Models via Group Diffusion Policy Optimization

> [!tip] 核心洞察
> ELBO 方差主要由随机时间采样主导，而非随机掩码；损失函数随时间变化呈现平滑、可预测的简单形态，因此适合用确定性数值积分近似以抑制方差。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过分组扩散策略优化提升扩散语言模型的推理能力 |
| 英文题名 | Improving Reasoning for Diffusion Language Models via Group Diffusion Policy Optimization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=JaqvespRBP) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Group Diffusion Policy Optimization (GDPO) |
| Dataset | GSM8K (512 tokens), MATH500 (512 tokens), Countdown (512 tokens), Sudoku (512 tokens) |

> [!tip] 效果简介
> - GSM8K (512 tokens) 上，准确率 (%) 为 84.99 (+SFT+GDPO, N=3)，对比 81.9 (+diffu-GRPO)，变化 +3.09。
> - MATH500 (512 tokens) 上，准确率 (%) 为 41.4 (+SFT+GDPO, N=3)，对比 39.2 (+diffu-GRPO)，变化 +2.2。
> - Countdown (512 tokens) 上，准确率 (%) 为 80.86 (+SFT+GDPO, N=3)，对比 37.1 (+diffu-GRPO)，变化 +43.76。

## 概述

扩散语言模型（DLMs）在推理任务上的强化学习（RL）微调面临一个关键瓶颈：**序列级似然函数难以精确计算**，导致无法直接估计重要性权重。现有方法（如 diffu-GRPO）退而求其次，采用 token 级的均值场近似，但牺牲了训练信号的保真度。若强行使用序列级 ELBO，传统双蒙特卡洛估计又会因**随机时间采样的高方差**而失效。

本文的核心发现是：**ELBO 的方差主要由随机时间采样主导，而非随机掩码**（Figure 2a）。损失函数随时间变化呈现平滑、可预测的简单形态（Figure 2b），这使得用确定性数值积分替代随机时间采样成为可能。

基于此，作者提出 **Group Diffusion Policy Optimization (GDPO)**，其核心创新是**半确定性蒙特卡洛（SDMC）积分方案**：外层用固定时间点的高斯求积替代随机采样，内层保留单次蒙特卡洛估计。该方案在仅需 2–3 个求积点的条件下，即可显著降低 ELBO 估计的偏差和方差（Figure 3），使序列级似然估计在计算上可行。

GDPO 将重要性权重从 token 级提升至**序列级**，配合组相对策略优化框架，在数学推理（GSM8K: +3.09%, MATH500: +2.2%）、规划（Countdown: +43.76%, Sudoku: +15.17%）和编码（MBPP: +10.2%）等基准上，一致且显著地超越了 LLaDA 基线和 diffu-GRPO 等先前 RL 方法（Table 2, Table 3, Figure 1）。

**方法定位**：GDPO 属于扩散语言模型的后训练强化学习范式，在方法谱系中位于 **diffu-GRPO**（Zhao et al., 2025）的改进位置——保留其组相对优化的框架，但将似然估计从 token 级均值场近似替换为序列级 SDMC-ELBO 估计。与 coupled-GRPO 等使用互补时间步对的变体相比，GDPO 通过确定性数值积分实现了更优的方差控制。

**主要局限**：GDPO 对学习率敏感，需要比 diffu-GRPO 更小的学习率以避免发散；在 HumanEval 512 令牌设置下性能（39.0）略低于 diffu-GRPO（45.5），表明 token 级方法在特定编码任务上可能仍有优势。

## 背景与动机

### 扩散语言模型的推理瓶颈

扩散语言模型（Diffusion Language Models, DLMs）作为一种新兴的生成范式，通过逐步去噪生成文本，天然支持非自回归解码和灵活的生成顺序。然而，这类模型在复杂推理任务上的表现仍显著落后于自回归模型（Autoregressive Models, ARMs）。一个根本性的瓶颈在于：**DLMs 的序列似然 $\log \pi(y|q)$ 无法精确计算**，这使得将成熟的强化学习（RL）微调范式直接移植到扩散模型上变得极为困难。

在自回归模型中，序列似然可以通过链式法则分解为 token 级条件概率的乘积，从而为近端策略优化（PPO）或组相对策略优化（GRPO）等方法提供精确的重要性权重。但在扩散模型中，生成过程是顺序无关的（order-agnostic），不存在这样的自然分解。现有方法不得不依赖于对似然的近似估计，而这一近似过程恰恰是性能损失的根源。

### 现有 RL 方法的缺口：token 级近似与方差爆炸

当前针对扩散语言模型的 RL 微调方法主要沿两条路径展开：

**路径一：token 级均值场近似。** 以 **diffu-GRPO**（Zhao et al., 2025）为代表，该方法将 GRPO 适配到掩码扩散模型中，通过一步去掩码的均值场网络评估来近似 token 级似然。具体而言，它使用 $\log \pi_\theta(y^i | y_t, q)$ 作为 token $y^i$ 的似然代理，其中 $y_t$ 是单次采样的噪声序列。这种近似虽然计算高效，但存在两个结构性缺陷：（1）token 级粒度天然保留了生成顺序的偏差，无法提供序列整体的忠实训练信号；（2）单步去掩码的均值场近似本身是对真实似然的有偏估计。

**路径二：序列级 ELBO 估计。** 理论上更优的方案是使用证据下界（ELBO）作为序列似然的代理：

$$\mathcal{L}_{\mathrm{ELBO}}(y|q) = \mathbb{E}_{t\sim\mathcal{U}[0,1]} \mathbb{E}_{y_t\sim\pi(\cdot|y)} \left[ \frac{1}{t} \sum_{i=1}^L \mathbf{1}[y_t^i=M] \log \pi_\theta(y^i|y_t, q) \right] \le \log \pi(y|q)$$

然而，直接使用双蒙特卡洛（Double Monte Carlo）采样来估计该期望——外层随机采样时间 $t$，内层随机掩码生成 $y_t$——会遭遇严重的**方差爆炸**问题。这一高方差使得 ELBO 估计在 RL 训练中极不稳定，甚至可能导致策略更新方向错误。

### 方差来源的关键洞察

本文通过系统性的方差分解实验，揭示了 ELBO 估计方差的真正来源。在 1000 个 OpenWeb 数据集的提示上，对损失函数各成分的均值和方差随噪声水平 $t$ 的变化进行分析（Figure 2），得到了一个决定性发现：

**绝大部分方差来源于随机时间采样，而非随机掩码操作。** 具体表现为：
- 损失函数 $g(t) = \mathbb{E}_{y_t}[Z_t]$ 作为时间 $t$ 的函数，呈现出平滑、可预测的简单形态（Figure 2b）；
- 方差在时间轴两端（$t \to 0$ 和 $t \to 1$）较高，但在大部分中间区域保持稳定（Figure 2c）；
- 随机掩码引入的方差相对较小，不是主导因素。

这一洞察直接指向了解决方案：**用确定性数值积分替代外层的时间随机采样，仅在必要时保留内层的蒙特卡洛采样**——即半确定性蒙特卡洛（Semi-deterministic Monte Carlo, SDMC）方案的核心思想。

### 本文动机：低方差序列级 RL 微调

基于上述分析，本文的核心动机可以概括为：

1. **从 token 级到序列级**：将重要性权重的粒度从 token 级提升到序列级，消除生成顺序偏差，提供更忠实的训练信号。

2. **从双随机到半确定**：通过固定时间点的高斯求积（Gaussian Quadrature）替代外层随机采样，将 ELBO 估计的方差从 $\mathcal{O}(1/NK)$ 降至 $\mathcal{O}(1/N^2K)$（在平滑性假设下），同时将偏差从 $\mathcal{O}(1/N)$ 降至 $\mathcal{O}(1/N^2)$ 或更低（Table 1）。

3. **计算效率与性能的平衡**：仅需 2–3 个求积点即可捕获大部分相对真实 ELBO 的增益（Figure 3），使得序列级 RL 微调在计算上可行，同时在数学推理、规划和编码任务上显著超越现有方法（Figure 1）。

这一动机催生了本文的核心方法——**分组扩散策略优化（Group Diffusion Policy Optimization, GDPO）**，它将 SDMC 估计器嵌入 GRPO 框架，在保持组内相对优势估计优势的同时，实现了低方差、高保真度的序列级策略更新。

## 核心创新

GDPO 的核心创新在于**将扩散语言模型（DLM）强化学习微调中的似然估计从 token 级提升到序列级**，并通过**半确定性蒙特卡洛（SDMC）方案**解决了序列级 ELBO 估计方差爆炸的瓶颈。

### 从 token 级到序列级的重要性权重

现有方法 **diffu-GRPO**（Zhao et al., 2025）沿用自回归模型的 GRPO 框架，在 token 级别计算重要性权重和优势估计。这种 token 级粒度天然适配自回归模型的逐 token 生成范式，但在 DLM 中面临根本性矛盾：DLM 的生成过程是顺序无关的（order-agnostic），不存在固定的从左到右的生成顺序，因此 token 级似然缺乏明确的因果结构支撑。

GDPO 将重要性权重的粒度从 token 级**重新构造为序列级**（整个回答），即用序列的 ELBO 指数比值定义重要性权重：

$$r_g(x) = \frac{\exp(\mathcal{L}_{\mathrm{ELBO}}(y_g|x))}{\exp(\mathcal{L}_{\mathrm{ELBO}}^{\mathrm{old}}(y_g|x))}$$

这一改变使得训练信号更忠实于 DLM 的生成特性，因为序列级目标不对 token 位置施加顺序偏好，从而在整个序列上产生更均匀的改进。

### 半确定性蒙特卡洛：打破方差瓶颈

序列级似然估计的核心障碍在于 DLM 的似然不可精确计算，必须依赖 ELBO 近似。传统方法使用**双蒙特卡洛（Double MC）**——外层随机采样时间 $t$，内层随机掩码——来估计 ELBO，但这种方式方差极大且计算成本高昂。

GDPO 的关键洞察来自对方差来源的分解分析（Figure 2a）：**ELBO 方差主要由随机时间采样主导，而非随机掩码**。此外，损失函数随时间 $t$ 呈现平滑、可预测的简单形态（Figure 2b）。这两个发现意味着：外层时间积分适合用确定性数值求积替代随机采样，从而大幅抑制方差。

基于此，GDPO 设计了 SDMC 方案：
- **外层**：固定时间点 $\{t_n\}$ 的高斯求积（Gaussian quadrature），权重 $\{w_n\}$
- **内层**：单次蒙特卡洛采样估计给定时间点的期望损失 $\ell(\pi_\theta; y, q, t_n)$

$$\mathcal{L}_{\mathrm{ELBO}}(y|q) \approx \sum_{n=1}^N w_n \, \ell(\pi_\theta; y, q, t_n)$$

与 diffu-GRPO 使用的 token 级均值场近似（一步去掩码）相比，SDMC 在三个维度上实现了根本性改变：

| 维度 | diffu-GRPO | GDPO |
|------|-----------|------|
| 似然估计方式 | token 级均值场近似 | 序列级 ELBO via SDMC |
| 重要性权重粒度 | token 级 | 序列级 |
| 时间积分方法 | 双蒙特卡洛（随机时间+随机掩码） | 固定时间点高斯求积+单次 MC 内层 |

### 效率与精度的双重收益

SDMC 的收益在极少的求积点下即可兑现：**仅需 N=2–3 个求积点就能捕获大部分相对真实 ELBO 的增益**（Figure 3），同时保持比双蒙特卡洛更低的偏差和方差。在 Countdown 数据集上，SDMC-3 估计器甚至显著优于使用更多函数评估次数的朴素蒙特卡洛估计器（Figure 4），验证了“更准确的 ELBO 估计带来更好的 RL 训练提升”这一因果链条。

值得注意的是，GDPO 对学习率敏感，通常需要比 diffu-GRPO 更小的学习率，否则可能导致模型发散（Appendix D.1）。这一敏感性可能源于序列级重要性权重引入了更大的梯度方差，需要在实践中仔细调参。

## 整体框架

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_JaqvespRBP/figures/009_Figure_3.jpg]]
*Figure 3: Estimation error and variance for Double Monte Carlo vs our Semi-deterministic Monte Carlo method. SD-MC achieves lower bias and variance, with most benefits obtained using only 2–3 points*

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_JaqvespRBP/figures/010_Table_1.jpg]]
*Table 1: Asymptotic Error Bounds in relation to Integration Points N and Monte Carlo Samples K*

GDPO 的整体 pipeline 围绕“序列级似然估计”这一核心瓶颈展开，将扩散语言模型的强化学习微调解耦为四个顺序模块：**生成 → 奖励与优势估计 → ELBO 估计 → 策略更新**。其关键创新在于用**半确定性蒙特卡洛（SDMC）**替换了传统双蒙特卡洛估计，从而在保持计算效率的同时大幅降低了 ELBO 估计的方差与偏差。

### 模块关系与数据流

```
┌──────────────┐    {y₁,...,y_G}    ┌──────────────────┐    {R_g}, {A_g}
│  生成模块     │ ─────────────────▶ │ 奖励与优势估计    │ ─────────────────▶
│  (Generation) │                    │ (Reward & Adv.)  │
└──────────────┘                    └──────────────────┘
       │                                    │
       │ π_θ_old                            │ {y_g}, {A_g}
       ▼                                    ▼
┌─────────────────────────────────────────────────────────────┐
│                   ELBO 估计器 (SDMC)                         │
│  ┌──────────────────┐    ┌──────────────────────────────┐   │
│  │ 固定时间点 {t_n}  │───▶│ 单次 MC 内层估计 ℓ(π_θ; y_g, t_n) │   │
│  │ (高斯求积节点)    │    │ (K 个掩码样本)                │   │
│  └──────────────────┘    └──────────────────────────────┘   │
│                                    │                        │
│              L_ELBO(y_g|q) ≈ Σ w_n · ℓ(...)                 │
│              r_g = exp(L_ELBO) / exp(L_ELBO^old)            │
└─────────────────────────────────────────────────────────────┘
       │
       │ {r_g} (序列级重要性权重)
       ▼
┌──────────────────┐
│  策略更新模块     │
│  (Policy Update) │  ──▶ π_θ (AdamW, 带裁剪 + KL 正则)
└──────────────────┘
```

### 各模块职责

**1. 生成模块（Generation）**
从旧策略 $\pi_{\theta_{\text{old}}}$ 中采样 $G$ 个完整回答序列 $y_1,\dots,y_G$，作为后续优势估计和重要性加权的候选池。这一步骤与标准 GRPO 一致，但 GDPO 的后续处理全部在序列粒度上进行。

**2. 奖励与优势估计（Reward & Advantage）**
对每个序列 $y_g$ 计算奖励 $R_g$（由任务奖励函数给出），然后在组内做归一化得到未归一化优势 $A_g = R_g - \text{mean}(\{R_g\})$。与 token 级 GRPO 不同，这里的优势是序列级的标量。

**3. ELBO 估计器（SDMC 方案）—— 核心创新**
这是 GDPO 区别于 diffu-GRPO 等 token 级方法的关键模块。传统双蒙特卡洛估计在 ELBO 的期望中同时对时间 $t$ 和掩码 $y_t$ 做随机采样，导致方差爆炸。SDMC 将这一过程解耦：

- **外层（确定性）**：用高斯求积选取 $N$ 个固定时间点 $\{t_n\}_{n=1}^N$ 及对应权重 $\{w_n\}_{n=1}^N$，消除随机时间采样引入的方差。
- **内层（随机性保留）**：在每个固定时间点 $t_n$ 上，仅对掩码模式做 $K$ 次蒙特卡洛采样，得到该点的损失估计 $\ell(\pi_\theta; y_g, q, t_n)$。

最终 ELBO 近似为加权和：
$$\mathcal{L}_{\mathrm{ELBO}}(y_g|q) \approx \sum_{n=1}^N w_n \cdot \ell(\pi_\theta; y_g, q, t_n)$$

序列级重要性权重由 ELBO 指数的比值定义：
$$r_g(x) = \frac{\exp(\mathcal{L}_{\mathrm{ELBO}}(y_g|x))}{\exp(\mathcal{L}_{\mathrm{ELBO}}^{\mathrm{old}}(y_g|x))}$$

**关键证据**：Figure 2(a) 表明 ELBO 方差主要由随机时间采样主导，而非随机掩码；Figure 3 显示 SDMC 在仅需 2–3 个求积点时即可获得大部分方差降低收益，偏差和方差均显著低于双蒙特卡洛。Table 1 给出了 SDMC 的渐近误差界：在满足光滑性假设时，方差为 $O(1/N^2K)$，偏差平方为 $O(1/N^4)$。

**4. 策略更新（Policy Update）**
基于序列级重要性权重 $r_g$ 和优势 $A_g$，通过带裁剪和 KL 正则的 GDPO 损失函数更新策略参数 $\theta$：
$$\mathcal{L}^{\mathrm{GDPO}}(\theta) = \mathbb{E}_x \mathbb{E}_{y_g\sim\pi_{\mathrm{dd}}} \left[ \frac{1}{G} \sum_{g=1}^G \frac{1}{|y_g|} \min\left(r_g A_g,\ \mathrm{clip}(r_g, 1-\epsilon, 1+\epsilon) A_g\right) - \beta\ \mathrm{KL}(\pi_\theta \| \pi_{\mathrm{ref}}) \right]$$

优化器使用 AdamW。需注意：GDPO 对学习率敏感，通常需要比 diffu-GRPO 更小的学习率，否则可能导致训练发散（Appendix D.1）。

### 与基线方法的关键差异

| 维度 | diffu-GRPO (Zhao et al., 2025) | GDPO (本文) |
|------|-------------------------------|-------------|
| 似然估计方式 | token 级均值场近似（一步去掩码） | 序列级 ELBO 通过 SDMC 估计 |
| 重要性权重粒度 | token 级 | 序列级（整个回答） |
| 时间积分方法 | 双蒙特卡洛（随机采样时间 + 随机掩码） | 固定时间点的高斯求积 + 单次 MC 内层估计 |
| 方差来源控制 | 未显式控制 | 消除随机时间采样的主导方差 |

这一框架的核心洞察在于：损失函数随时间 $t$ 呈现平滑、可预测的简单形态（Figure 2(b)），因此适合用确定性数值积分近似以抑制方差。SDMC 以极小的计算开销（$N=2\sim3$ 个求积点）实现了对 ELBO 的高效低方差估计，为序列级强化学习微调扩散语言模型铺平了道路。

## 核心模块与公式推导

### 3.1 问题背景：扩散语言模型的似然估计瓶颈

扩散语言模型（DLMs）的生成过程以任意顺序逐步去掩码，导致序列的精确似然 $\log \pi(y|q)$ 难以直接计算。在强化学习微调中，策略梯度方法需要序列级似然来构建重要性权重，但 DLMs 只能提供证据下界（ELBO）作为代理：

$$
\mathcal{L}_{\mathrm{ELBO}}(y|q) = \mathbb{E}_{t\sim\mathcal{U}[0,1]} \mathbb{E}_{y_t\sim\pi(\cdot|y)} \left[ \frac{1}{t} \sum_{i=1}^L \mathbf{1}[y_t^i=M] \log \pi_\theta(y^i|y_t, q) \right] \le \log \pi(y|q)
$$

该 ELBO 包含两层随机性：外层对时间 $t$ 的均匀采样，内层对掩码位置 $y_t$ 的随机采样。传统做法采用**双蒙特卡洛**（Double MC）同时估计这两层期望，但引入的方差极大且计算成本高昂——这是将 RL 方法迁移到 DLMs 的核心瓶颈。

### 3.2 方差分解与确定性时间积分

作者首先对 ELBO 的方差来源进行解耦分析（Figure 2）。将损失函数 $\ell(\pi_\theta; y, q, t)$ 视为时间 $t$ 的函数后发现：

- **随机时间主导方差**：Figure 2(a) 表明，ELBO 估计的绝大部分方差来自随机采样时间 $t$，而非随机掩码。
- **损失函数形态简单可预测**：Figure 2(b) 显示，损失函数随 $t$ 变化呈现平滑、可预测的简单曲线，且在不同 prompt 间形态一致。

基于此核心洞察，作者提出将 ELBO 重写为时间积分形式，消除外层随机时间采样：

$$
\mathcal{L}_{\mathrm{ELBO}}(y|q) = \int_0^1 \mathbb{E}_{y_t \sim \pi_t(\cdot|y)} \left[ \frac{1}{t} \sum_{i=1}^L \mathbf{1}[y_t^i = M] \log \pi_\theta(y^i | y_t, q) \right] dt
$$

### 3.3 半确定性蒙特卡洛（SDMC）估计器

由于损失函数在时间维度上足够平滑，外层积分适合用**数值求积**（numerical quadrature）替代蒙特卡洛采样。SDMC 方案将两层估计分离：

- **外层（确定性）**：使用 $N$ 个固定时间点 $\{t_n\}_{n=1}^N$ 和对应求积权重 $\{w_n\}_{n=1}^N$（采用高斯求积），消除随机时间的方差。
- **内层（随机）**：在每个时间点 $t_n$ 上，仅用 $K$ 次蒙特卡洛采样估计条件期望。

SDMC 的近似形式为：

$$
\mathcal{L}_{\mathrm{ELBO}}(y|q) \approx \sum_{n=1}^N w_n \underbrace{\sum_{k=1}^K \left[ \frac{1}{t_n} \sum_{i=1}^L \mathbf{1}[ (y_{t_n}^{[k]})^i = M ] \log \pi_\theta(y^i | y_{t_n}^{[k]}, q) \right]}_{\ell(\pi_\theta; y, q, t_n)}
$$

**理论保证**（Table 1）：在损失函数满足光滑性假设时，求积方案的方差为 $O(1/N^2K)$、偏差平方为 $O(1/N^4)$，显著优于普通黎曼和的 $O(1/NK)$ 方差和 $O(1/N^2)$ 偏差平方。

**实证验证**（Figure 3）：SDMC 在相同函数评估次数（NFE）下，偏差和方差均显著低于 Double MC，且仅需 $N=2\sim3$ 个求积点即可捕获大部分收益。

### 3.4 GDPO 损失函数

GDPO 将 GRPO 的 token 级重要性权重重新表述为序列级，利用 SDMC 高效估计 ELBO 作为似然代理。核心公式如下：

**序列级重要性权重**：

$$
r_g(x) = \frac{\exp(\mathcal{L}_{\mathrm{ELBO}}(y_g|x))}{\exp(\mathcal{L}_{\mathrm{ELBO}}^{\mathrm{old}}(y_g|x))}
$$

其中 $\mathcal{L}_{\mathrm{ELBO}}(y_g|x)$ 由 SDMC 估计器计算，$\mathcal{L}_{\mathrm{ELBO}}^{\mathrm{old}}$ 为旧策略下的缓存值。

**组内优势估计**：对于 $G$ 个补全 $\{y_g\}_{g=1}^G$，基于奖励 $R_g$ 计算未归一化优势：

$$
A_g = R_g - \frac{1}{G}\sum_{g'=1}^G R_{g'}
$$

**GDPO 目标函数**：

$$
\mathcal{L}^{\mathrm{GDPO}}(\theta) = \mathbb{E}_x \mathbb{E}_{y_g\sim\pi_{\mathrm{dd}}} \left[ \frac{1}{G} \sum_{g=1}^G \frac{1}{|y_g|} \min \left( r_g A_g, \mathrm{clip}(r_g, 1-\epsilon, 1+\epsilon) A_g \right) - \beta \mathrm{KL}(\pi_\theta || \pi_{\mathrm{ref}}) \right]
$$

该损失包含三部分：裁剪的重要性加权优势（稳定策略更新）、序列长度归一化 $1/|y_g|$（消除长度偏差）、KL 正则项（防止策略偏离参考模型过远）。

### 3.5 与基线方法的关键差异

| 设计维度 | diffu-GRPO (Zhao et al., 2025) | GDPO (本文) |
|---------|-------------------------------|------------|
| 似然估计方式 | token 级均值场近似（一步去掩码） | 序列级 ELBO 通过 SDMC 估计 |
| 重要性权重粒度 | token 级 | 序列级 |
| 时间积分方法 | 双蒙特卡洛（随机时间 + 随机掩码） | 固定时间点高斯求积 + 单次内层 MC |
| 方差控制 | 无显式机制 | 确定性外层消除主导方差源 |

### 3.6 训练流程模块

GDPO 的训练管线包含四个核心模块：

1. **生成模块**：从旧策略 $\pi_{\theta_{\text{old}}}$ 中为每个问题 $x$ 生成 $G$ 个补全 $\{y_g\}$。
2. **奖励与优势估计**：基于组内统计计算序列级奖励 $R_g$ 和未归一化优势 $A_g$。
3. **ELBO 估计器（SDMC）**：对每个补全 $y_g$，通过 $N$ 个固定时间点的高斯求积和 $K$ 次内层蒙特卡洛采样，计算 $\mathcal{L}_{\mathrm{ELBO}}(y_g|x)$ 作为重要性权重的基础。
4. **策略优化**：使用 AdamW 优化器，根据 GDPO 目标函数更新策略参数 $\theta$。

## 实验与分析

### 核心瓶颈与因果机制

扩散语言模型（DLM）的强化学习微调面临一个根本性难题：序列级似然函数 $\pi(y|q)$ 无法精确计算，因为 DLM 的生成范式是顺序无关的（order-agnostic），不存在自回归模型那样的链式法则分解。这迫使现有方法（如 **diffu-GRPO**，Zhao et al., 2025）退而求其次，使用 token 级均值场近似来估计似然，但这种方法引入的偏差可能损害训练信号的忠实度。

本文通过方差分解实验揭示了一个关键洞察：ELBO 估计的方差**主要来自随机时间采样，而非随机掩码**。Figure 2(a) 显示，控制掩码比例的随机时间步 $t$ 主导了 ELBO 的方差波动。进一步地，Figure 2(b) 表明损失函数随时间 $t$ 的变化呈现出平滑、可预测的简单形态——这一性质为用确定性数值积分替代随机时间采样提供了理论依据。


![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_JaqvespRBP/figures/008_Figure_2.jpg]]
*Figure 2: We plot the mean and variance of the loss functions as a function of the noise level t. (a) We observe that most of the variance comes from picking the random time (b) The loss function follows a simple, predictable shape across many prompts. (c) The loss variance varies highly at the end but stabilizes for most times*

基于此，GDPO 采用**半确定性蒙特卡洛（SDMC）**方案：外层在固定时间点 $\{t_n\}_{n=1}^N$ 上使用高斯求积（权重 $w_n$），内层仅对掩码进行蒙特卡洛采样。这从根本上改变了方差结构——Table 1 的理论分析表明，求积方案将方差从 $O(1/NK)$ 降至 $O(1/N^2K)$，偏差平方从 $O(1/N^2)$ 降至 $O(1/N^4)$。

### 主实验结果

Table 2 和 Table 3 汇总了 GDPO 在数学推理、规划和编码任务上的表现（均使用 $N=3$ 个求积点）。


![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_JaqvespRBP/figures/011_Table_2.jpg]]
*Table 2: Model performance on Mathematics and Planning Benchmarks based on N \ = \ 3 quadrature points. Green is the best performing model*

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_JaqvespRBP/figures/012_Table_3.jpg]]
*Table 3: Model performance on Coding with N = 3 quadrature points. Green is best*

**数学与规划基准（Table 2）：**

| 基准测试 | 序列长度 | +SFT+GDPO (N=3) | +diffu-GRPO | 提升 |
|---------|---------|-----------------|-------------|------|
| GSM8K | 512 | **84.99** | 81.9 | +3.09 |
| MATH500 | 512 | **41.4** | 39.2 | +2.2 |
| Countdown | 512 | **80.86** | 37.1 | **+43.76** |
| Sudoku | 512 | **26.17** | 11.0 | **+15.17** |

在 Countdown 和 Sudoku 这类需要多步规划的复杂推理任务上，GDPO 的优势尤为显著——Countdown 上提升超过 43 个百分点，Sudoku 上提升超过 15 个百分点。作者将这归因于序列级似然估计促进了跨 token 位置的均匀改进，而 token 级方法保留了生成顺序偏差。

**编码基准（Table 3）：**

| 基准测试 | 序列长度 | +GDPO (N=3) | LLaDA-8B-Instruct | 提升 |
|---------|---------|-------------|-------------------|------|
| MBPP | 512 | **50.6** | 40.4 | +10.2 |
| HumanEval | 256 | **56.1** | 48.2 | +7.9 |

GDPO 在 MBPP 上取得了 10.2 个百分点的显著提升，且无需 SFT 预热阶段。Figure 1 进一步显示，在使用 128/256/512 次生成的最佳结果（best-of-N）评估下，GDPO 在所有任务类别上均显著优于 LLaDA 基线和 diffu-GRPO。

### 消融实验：ELBO 估计器质量的影响

Figure 4 在 Countdown 数据集上对比了不同 ELBO 估计器对训练效果的影响，核心发现包括：


![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_JaqvespRBP/figures/013_Figure_4.jpg]]
*Figure 4: Test accuracy with different training iterations and ELBO estimators on the Countdown dataset*

1. **估计器准确性与性能正相关**：更准确的 ELBO 估计器带来更好的 RL 训练提升。SDMC-3 的测试准确率曲线始终高于朴素蒙特卡洛估计器。
2. **效率优势显著**：SDMC-3 仅需 3 次函数评估（NFE），却能显著优于使用更多评估次数的朴素蒙特卡洛估计器。这表明方差降低带来的收益远超增加采样数量的补偿效应。
3. **求积点数量与收益的关系**：Figure 3 显示，仅需 $N=2$ 或 $N=3$ 个求积点即可捕获大部分相对真实 ELBO 的增益。SDMC 在 NFE=2 时估计误差即急剧下降，此后保持低方差稳定。这与 Table 5 的训练效率数据一致：GDPO (N=3) 仅需 3500 次迭代（每次 3 NFE），而 diffu-GRPO 需要 4500 次迭代（每次 1 NFE），总训练时间均为 6 小时。

### 失败模式与限制

1. **学习率敏感性**：GDPO 对学习率要求严格，通常需要比 diffu-GRPO 更小的学习率（Table 4 显示为 $5\times10^{-7}$ 至 $1\times10^{-6}$），否则可能导致模型发散（Appendix D.1）。这一敏感性可能源于序列级重要性权重的方差特性。

2. **HumanEval 512 令牌设置下的劣势**：在 HumanEval 512 令牌配置下，GDPO 的准确率为 39.0，低于 diffu-GRPO 的 45.5（Table 3）。这表明在某些编码任务的长序列场景中，token 级方法可能仍具有优势——可能因为序列级 ELBO 估计在极长序列上的累积误差抵消了其方差优势。此点需手动验证是否与具体任务的数据分布有关。

3. **与 coupled-GRPO 的对比**：Table 7 显示 GDPO 在 Countdown 和 Sudoku 上全面优于 coupled-GRPO（使用互补时间步对的 GRPO 变体），但 coupled-GRPO 的论文引用信息缺失，无法确认其具体实现细节。

### 计算效率

所有训练在 2–8 张 H100 GPU 上完成（Table 4）。GDPO 虽然每次迭代需要更多 NFE（2–3 vs 1），但因收敛更快，总迭代次数更少，实际训练时间与 diffu-GRPO 相当（Table 5）。这种效率优势源于 SDMC 估计器的低方差特性，使得每次梯度更新包含更高质量的信号。

## 方法谱系与知识库定位

### 问题定位：扩散语言模型强化学习微调的似然估计瓶颈

扩散语言模型（DLMs）在推理任务上的强化学习（RL）微调面临一个根本性瓶颈：**序列级似然函数无法精确计算**。与自回归模型不同，DLMs 的生成过程不遵循固定的 token 顺序，因此无法通过链式法则直接分解和评估序列概率。这一特性使得主流的 RL 微调方法（如 PPO、GRPO）难以直接迁移——这些方法依赖 token 级或序列级的似然比来计算重要性权重，而 DLMs 中唯一可用的代理是证据下界（ELBO）。

然而，ELBO 的朴素估计——双蒙特卡洛采样（Double MC）——存在严重的方差爆炸问题。具体而言，ELBO 需要对外层时间 $t \sim \mathcal{U}[0,1]$ 和内层掩码 $y_t \sim \pi_t(\cdot|y)$ 进行双重随机采样。论文的核心发现是：**ELBO 的方差主要由随机时间采样主导，而非随机掩码**（Figure 2(a)）。损失函数随时间 $t$ 呈现平滑、可预测的简单形态（Figure 2(b)），这意味着外层时间积分适合用确定性数值方法近似，从而大幅抑制方差。

### 方法谱系：从 token 级到序列级的演化

**基线方法一：diffu-GRPO**（Zhao et al., 2025）是首个将 GRPO 适配到扩散语言模型的工作。其核心策略是使用均值场近似，通过一步去掩码（single-step unmasking）来估计 token 级似然，从而避免序列级似然的计算困难。然而，这种 token 级近似存在两个局限：（1）均值场假设忽略了 token 间的依赖关系，导致似然估计有偏；（2）token 级的重要性权重保留了生成顺序的偏差，与 DLMs 的 order-agnostic 特性不匹配。

**基线方法二：coupled-GRPO** 尝试通过使用互补时间步对（complementary time-step pairs）来改进 token 级似然估计，但本质上仍停留在 token 级粒度。

**GDPO 的关键改进**是将重要性权重的粒度从 token 级提升到序列级。具体而言，GDPO 使用序列级 ELBO 的指数比作为重要性权重：

$$r_g(x) = \frac{\exp(\mathcal{L}_{\mathrm{ELBO}}(y_g|x))}{\exp(\mathcal{L}_{\mathrm{ELBO}}^{\mathrm{old}}(y_g|x))}$$

这一设计使得整个回答作为整体被评估和优化，与 DLMs 的生成范式一致。论文指出，序列级似然“promote more uniform improvements across token positions”，避免了 token 级方法中生成顺序偏差的问题。

**半确定性蒙特卡洛（SDMC）方案**是实现序列级估计的关键使能技术。SDMC 将 ELBO 的估计分解为两层：
- **外层**：使用固定时间点的高斯求积（Gaussian quadrature）替代随机时间采样，权重 $w_n$ 和时间点 $t_n$ 预先确定；
- **内层**：在每个固定时间点 $t_n$ 上，使用少量蒙特卡洛样本（$K$ 次）估计条件期望。

这一方案将双蒙特卡洛的方差 $\mathcal{O}(1/NK)$ 降低到 $\mathcal{O}(1/N^2K)$（在平滑性假设下，Table 1），且仅需 $N = 2\text{--}3$ 个求积点即可捕获大部分收益（Figure 3）。

### 与相关工作的关系

| 维度 | diffu-GRPO | coupled-GRPO | **GDPO（本方法）** |
|------|-----------|-------------|-------------------|
| 似然估计方式 | token 级均值场近似 | token 级互补时间对 | 序列级 ELBO（SDMC 估计） |
| 重要性权重粒度 | token 级 | token 级 | 序列级 |
| 时间积分方法 | 一步去掩码（隐式） | 互补时间对 | 固定点高斯求积 |
| 方差控制 | 无显式控制 | 有限改善 | 确定性外层 + 减少内层采样 |
| 计算效率 | 高（单步） | 中等 | 高（$N=3$, $K=1$ 即可） |

GDPO 在方法论上可视为对 diffu-GRPO 的序列级泛化：两者都使用 GRPO 的组相对优势估计框架，但 GDPO 通过 SDMC 方案实现了更准确的序列级似然估计，从而提供更忠实的训练信号。

### 适用边界与局限

**适用场景**：GDPO 在数学推理（GSM8K: +3.09%, MATH500: +2.2%）、规划任务（Countdown: +43.76%, Sudoku: +15.17%）和编码任务（MBPP: +10.2%）上均展现出对 diffu-GRPO 的显著优势，尤其在需要全局一致性的规划任务上增益最大。

**已知局限**：
1. **学习率敏感性**：GDPO 需要比 diffu-GRPO 更小的学习率，否则可能导致模型发散（Appendix D.1）。这可能是由于序列级权重的方差虽已降低，但仍高于 token 级均值场近似。
2. **编码任务上的局部劣势**：在 HumanEval 512 令牌设置下，GDPO 的性能（39.0）略低于 diffu-GRPO（45.5）（Table 3），表明在某些编码任务上 token 级方法可能仍有优势——这可能是因为编码任务中 token 级的局部正确性比全局一致性更关键。
3. **ELBO 作为似然代理的固有偏差**：ELBO 仅是序列似然的下界，其紧致程度取决于模型质量。在模型训练初期或复杂任务上，ELBO 与真实似然之间的 gap 可能影响重要性权重的准确性。

### 开放问题

1. **数据驱动求积方案**：当前 SDMC 使用固定权重的高斯求积，能否设计数据驱动或自适应的求积权重和位置，以进一步降低方差？
2. **方差-偏差权衡的泛化性**：ELBO 估计的方差-偏差权衡在数学推理任务上得到了验证，但在更复杂的开放式文本生成任务中是否依然成立？
3. **采样点扩展**：GDPO 当前使用 $N=3$ 个求积点，是否可以扩展到更多采样点（类似 coupled-GRPO 的思路）以进一步改进？Table 1 的理论界表明增加 $N$ 可降低偏差，但实际收益需要验证。
4. **高效低方差估计器的设计**：论文明确指出“designing estimators that are both efficient and low-variance remains an open problem”，这指向了扩散模型 RL 微调中一个根本性的方法论挑战。

## 原文 PDF

![[paperPDFs/ICLR_2026/Improving_Reasoning_for_Diffusion_Language_Models_via_Group_Diffusion_Policy_Optimization.pdf]]
