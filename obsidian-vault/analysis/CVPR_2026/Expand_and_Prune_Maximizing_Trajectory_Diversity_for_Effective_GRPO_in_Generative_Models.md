---
title: "Expand and Prune: Maximizing Trajectory Diversity for Effective GRPO in Generative Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Expand_and_Prune_Maximizing_Trajectory_Diversity_for_Effective_GRPO_in_Generative_Models.pdf
code_link: null
aliases:
- PG
- EPMTDEGGM
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在生成过程的中间时间步，利用潜在特征进行单步 ODE 投影以预测终态奖励，并通过 Optimal Variance Filtering (OVF) 动态剪枝掉奖励集中、优势信号微弱的轨迹，从而在扩大初始采样组以增强多样性的同时，仅保留高方差子集进入后续去噪与梯度更新。
primary_logic: 奖励聚类现象表明大量采样轨迹对优化的贡献微乎其微；通过最大化奖励方差的子集选择（OVF），可以用更少的轨迹实现更强的优化信号。借助“先扩展后剪枝”（Expand-and-Prune）策略，在采样阶段提前终止冗余轨迹，使探索广度与优化成本解耦，实现性能与效率的双重提升。
claims:
- GRPO 采样中普遍存在奖励聚类现象，大量轨迹的奖励集中在组均值附近，导致归一化优势接近零，对梯度更新贡献极小。
- 通过最大化奖励方差的子集选择（OVF），可以在仅使用部分轨迹（k < G）的情况下获得优于全部轨迹（G）的优化性能，验证了“少即是多”的假设。
- Pro-GRPO 通过动态潜在剪枝提前终止奖励聚类轨迹，在保持或提升性能的同时大幅降低 FLOPS，实现 1.26×–1.41× 的加速。
- 在流匹配模型（SD3.5）和扩散模型（SD-v1.4）上，Pro-GRPO 在所有主要指标上一致优于基线 GRPO 方法（Flow-GRPO, DanceGRPO），并具备更好的泛化能力。
---

# Expand and Prune: Maximizing Trajectory Diversity for Effective GRPO in Generative Models

> [!tip] 核心洞察
> 奖励聚类现象表明大量采样轨迹对优化的贡献微乎其微；通过最大化奖励方差的子集选择（OVF），可以用更少的轨迹实现更强的优化信号。借助“先扩展后剪枝”（Expand-and-Prune）策略，在采样阶段提前终止冗余轨迹，使探索广度与优化成本解耦，实现性能与效率的双重提升。

| 字段 | 内容 |
|------|------|
| 中文题名 | 扩展与剪枝：最大化轨迹多样性以实现生成模型中高效GRPO |
| 英文题名 | Expand and Prune: Maximizing Trajectory Diversity for Effective GRPO in Generative Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.15347) |
| Topic | #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | Pro-GRPO |
| Dataset | DrawBench, GenEval, PickScore evaluation training cost |

> [!tip] 效果简介
> - DrawBench (Flow-based SD3.5, PickScore reward) 上，PickScore (In-Domain) 24.008 vs 23.322 (+0.686)；Aesthetic Score (In-Domain) 6.046 vs 5.912 (+0.134)。
> - GenEval (Flow-based SD3.5, PickScore reward) 上，Overall Score 0.726 vs 0.719 (Flow-GRPO) (+0.007)。
> - PickScore evaluation training cost 上，Total FLOPs reduction / Speedup Standard: 335627 T (1.26×); Flash: 267366 T (1.41×) vs 453474 T (1.0×, Flow-GRPO) (Standard -26%, Flash -41%)。

## 概述

生成式模型的对齐微调中，GRPO（Group Relative Policy Optimization）已成为主流在线强化学习范式，但其面临一个关键瓶颈：**大采样组带来的高计算成本与“奖励聚类”（Reward Clustering）导致的大量轨迹优势信号稀释之间的冲突**。具体而言，当采样组大小 $G$ 增大以增强探索多样性时，大量轨迹的奖励会聚集在组均值附近，使得归一化优势趋近于零，对梯度更新的贡献几乎可忽略（Eq. (7)(8)，Figure 1(a)）。这意味着在固定计算预算下，探索效率受到严重制约——简单增加采样量并不能带来成比例的优化收益。

针对这一困境，本文提出 **Pro-GRPO（Proactive GRPO）**，其核心洞察是：**奖励聚类现象表明大量采样轨迹对优化贡献微乎其微；通过最大化奖励方差的子集选择，可以用更少的轨迹实现更强的优化信号**。Pro-GRPO 采用“先扩展后剪枝”（Expand-and-Prune）策略：在采样阶段以较大的初始组 $G_{\max}$ 扩展探索广度，随后在去噪过程的中间时间步，利用潜在特征进行单步 ODE 投影以预测终态奖励，并通过 **最优方差过滤（Optimal Variance Filtering, OVF）** 动态剪枝掉奖励集中、优势信号微弱的轨迹，仅保留高方差子集 $K$ 进入后续去噪与梯度更新。这一机制使探索广度与优化成本解耦，实现性能与效率的双重提升。

在方法定位上，Pro-GRPO 区别于现有 GRPO 基线（如 **Flow-GRPO**（Liu et al., 2025）和 **DanceGRPO**（Xue et al., 2025））的关键在于：它将轨迹选择从“无选择地使用全部采样”转变为“在采样过程中基于潜在特征进行主动剪枝”，并将优势估计范围从完整采样组 $G$ 收缩至最终幸存子集 $K$。

实验结果表明，在流匹配模型（SD3.5-Medium）和扩散模型（SD-v1.4）上，Pro-GRPO 在所有主要指标上一致优于基线方法：在 DrawBench 上 PickScore 提升 +0.686（Table 1），在 GenEval 上 Overall Score 达到 0.726（Table 3），同时实现 1.26×–1.41× 的加速（Table 4）。消融实验进一步验证了扩展初始组大小和合理设置剪枝检查点对性能的正向影响（Table 5, Table 6）。

## 背景与动机

文本到图像（T2I）生成模型近年来取得了显著进展，但如何使其输出与复杂、主观的人类偏好对齐仍是一个核心挑战。基于人类反馈的强化学习（RLHF）已成为对齐大语言模型的主流范式，而在生成模型中，**GRPO（Group Relative Policy Optimization）** 作为一种在线 RL 方法，通过无需额外价值网络的组归一化优势估计，在扩散模型和流匹配模型的微调中展现出强大的潜力。

然而，GRPO 在生成模型中的应用面临一个关键瓶颈：**奖励聚类（Reward Clustering）现象**。当采样组大小 G 增大时，大量轨迹的奖励值高度集中于组均值 $\mu_G$ 附近。从形式上看，对于聚类区域 $C_{\delta} = \{ i : |R_i - \mu_G| \le \delta \sigma_G \}$ 内的轨迹，其归一化优势被严格约束在 $|A_i| \le \delta$ 的范围内。由于每条轨迹对梯度的贡献与其优势成比例（$g_i \propto A_i \nabla_{\theta} \log \pi_{\theta}(\tau_i)$），这些轨迹提供的学习信号微乎其微，几乎不参与有效的策略更新。

这一现象在现有方法中造成了**探索效率与计算成本之间的尖锐矛盾**。一方面，较大的采样组 G 有利于增加轨迹多样性、覆盖更广泛的奖励分布，从而提升探索质量；另一方面，G 的增大不仅直接推高去噪与优化过程的 FLOPs 开销，更使得大部分计算资源被浪费在优势信号微弱的聚类轨迹上。简单的缓解策略——如随机均匀子采样（Uniform Subsampling）——仅等比例地缩小样本量，却无法打破奖励分布的内在聚类结构，因此无法从根本上恢复有效的学习信号。

本文的核心动机正是解耦这一矛盾：**能否在扩大初始探索多样性的同时，仅保留对优化真正有贡献的轨迹子集，从而在不牺牲甚至提升性能的前提下大幅降低计算成本？** 为此，我们提出 Pro-GRPO（Proactive GRPO），通过“先扩展后剪枝”（Expand-and-Prune）的策略，在采样过程中动态识别并提前终止奖励聚类轨迹，使有效优化成本与幸存子集大小 K 而非初始扩展组大小 $G_{\max}$ 成正比，实现了探索广度与计算效率的双重优化。

## 核心创新

Pro-GRPO 的核心创新在于将“先扩展后剪枝”（Expand-and-Prune）策略引入 GRPO 的在线采样过程，通过动态潜在剪枝解耦了探索广度与优化成本之间的耦合关系，从而在固定计算预算下同时提升性能与效率。

### 创新动机：奖励聚类与优势稀释

GRPO 依赖组归一化优势信号驱动策略更新。然而，本文揭示了一个普遍存在的**奖励聚类（Reward Clustering）**现象：在大采样组中，大量轨迹的奖励值集中在组均值 $\mu_G$ 附近，形成低方差聚集区 $C_{\delta} = \{ i : |R_i - \mu_G| \le \delta \sigma_G \}$。对于聚集区内的轨迹，其归一化优势被严格界住（$|A_i| \le \delta$），导致这些轨迹对梯度更新的贡献微乎其微（$g_i \propto A_i \nabla_{\theta} \log \pi_{\theta}(\tau_i)$）。这意味着在标准 GRPO 中，大量计算资源被浪费在几乎不提供学习信号的冗余轨迹上。

### 核心机制：最优方差过滤（OVF）

针对奖励聚类问题，Pro-GRPO 提出了**最优方差过滤（Optimal Variance Filtering, OVF）**策略。OVF 的核心思想是：从大小为 $G$ 的候选轨迹集中，选择大小为 $k$ 的子集 $\mathcal{K}^{\star}$，使得该子集的奖励方差最大化：

$$\mathcal{K}^{\star} = \arg\max_{\substack{\mathcal{K}\subseteq\{1,\ldots,G\} \\ |\mathcal{K}|=k}} \sigma^2(\mathcal{K})$$

这一选择机制刻意保留奖励分布的极值样本（高奖励与低奖励轨迹），从而主动缓解奖励聚类，使幸存子集的优势信号更加显著。实验表明，均匀子采样无法缓解聚类，而 OVF 则使奖励分布向两端扩散，并在训练全程维持更高的奖励方差。

### 关键设计：动态潜在剪枝与 Expand-and-Prune 调度

Pro-GRPO 将 OVF 嵌入去噪过程的中间时间步，形成**动态潜在剪枝（Dynamic Latent Pruning）**机制。具体而言：

1. **代理奖励预测**：在预设的剪枝检查点 $S_i$，对每个活跃轨迹的当前潜在变量执行单步 ODE 投影，预测终态潜在变量，经 VAE 解码和奖励模型得到近似的终态奖励 $\hat{R}_i$。
2. **多步 OVF 剪枝**：基于代理奖励，在检查点上应用 OVF 选择高方差子集继续去噪，其余轨迹被提前终止。剪枝路径从初始扩展组 $G_{\max}$ 逐步收窄至最终幸存集 $K$。
3. **剪枝后 GRPO 目标**：仅对最终幸存轨迹计算沿时间步累积的 clipped 重要性采样损失与 KL 正则项，进行策略更新。

这一设计带来了关键的 **changed slots**：

| 设计维度 | 基线方法 | Pro-GRPO |
|---------|---------|----------|
| 轨迹采样组大小 | 固定 $G$（如 24） | 初始扩展至 $G_{\max}$（如 32 或 64），经多步 OVF 剪枝至 $K$（如 8） |
| 轨迹选择方式 | 无选择，全部参与去噪与优化 | 在中间时间步基于潜在特征预测代理奖励，OVF 选取高方差子集，提前终止其余轨迹 |
| 优势估计范围 | 基于完整采样组 $G$ 计算组归一化优势 | 仅基于最终幸存子集 $K$ 计算优势 |

### 效率-性能解耦

Expand-and-Prune 策略的核心洞察在于：通过将初始采样组临时扩展至 $G_{\max}$ 以最大化探索多样性，随后通过多步剪枝将计算量收敛至幸存集 $K$。由于只有幸存集进入后续去噪与反向传播，**有效优化成本与 $K$ 成正比，而非 $G_{\max}$**。这使得 Pro-GRPO 能够在不增加优化成本的前提下享受更大初始多样性带来的性能增益——消融实验证实，将 $G_{\max}$ 从 32 提升至 64 时，In-Domain HPSv2.1 从 0.386 提升至 0.393。同时，Pro-GRPO-Flash 实现了 1.41× 的加速，而 Pro-GRPO Standard 在 1.26× 加速下取得了最佳整体性能。

## 整体框架

Pro-GRPO 的整体设计围绕一个核心矛盾展开：**大采样组带来的探索多样性收益，与奖励聚类（Reward Clustering）导致的优势信号稀释和计算成本膨胀之间的冲突**。为解决这一矛盾，Pro-GRPO 引入“先扩展后剪枝”（Expand-and-Prune）的动态调度策略，在去噪过程内部对轨迹进行选择性提前终止，从而将探索广度与优化成本解耦。

### 框架总览

Pro-GRPO 的 pipeline 由以下关键阶段串联构成（参见 Figure 3）：

![[assets/figures/papers/paper_list_l2676_https_arxiv_org_abs_2512_15347/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the Pro-GRPO. Pro-GRPO runs a dynamic expand-and-prune schedule inside the T -step denoising. We begin with an expanded group*

1. **扩展采样（Expand）**：在每个训练迭代中，以远超常规的初始组大小 $G_{\max}$（例如 32 或 64）采样一批轨迹，最大化探索多样性。
2. **动态潜在剪枝（Dynamic Latent Pruning）**：在去噪过程的预设中间时间步（检查点 $S_i$），对每个活跃轨迹执行单步 ODE 投影，预测其终态代理奖励，并通过最优方差过滤（OVF）选取高方差子集继续去噪，其余轨迹被提前终止。
3. **幸存轨迹优化（Pruned GRPO）**：仅对最终幸存集 $\mathcal{K}_{I+1}$（大小为 $K$）中的轨迹计算组归一化优势与 clipped 重要性采样损失，进行策略更新。

这一设计的因果杠杆在于：**优化成本仅与最终幸存集大小 $K$ 成正比，而非初始扩展组大小 $G_{\max}$**，从而在固定计算预算下实现了“用更少的轨迹获得更强的优化信号”。

### 模块关系与数据流

Pro-GRPO 的模块间数据流如下：

```
扩展采样 (G_max 条轨迹)
    │
    ▼
去噪过程 (T 步)
    │
    ├── 检查点 S_1: 代理奖励预测 ──► OVF 剪枝 ──► 幸存集 K_1
    │
    ├── 检查点 S_2: 代理奖励预测 ──► OVF 剪枝 ──► 幸存集 K_2
    │
    └── ... ──► 最终幸存集 K_{I+1} = K
                    │
                    ▼
              Pro-GRPO 目标优化
```

**代理奖励预测模块**的核心机制是：在检查点 $t_i$，利用当前潜在变量 $\mathbf{x}_{t_i}^{(g)}$ 和 ODE 漂移项 $b_\theta$ 执行单步确定性投影到终态 $T$，得到近似终态潜在变量，再经 VAE 解码和奖励模型获得代理奖励 $\hat{R}_i^{(g)}$。这一步的计算开销远低于完整去噪，是实现高效剪枝的关键。

**多步 OVF 模块**在每个检查点应用最优方差过滤，从当前活跃集中选出奖励方差最大的子集。与随机均匀子采样不同，OVF 倾向于保留奖励分布的极值样本（高奖励和低奖励轨迹），从而有效缓解奖励聚类、保持优势信号的强度。这一效果在 Figure 1(c) 中得到了直观验证：OVF 选取的子集奖励分布呈现“去聚类”特征，向两端扩散。

**Pro-GRPO 目标函数**仅针对最终幸存轨迹集计算：

$$\mathcal{I}_{\mathrm{Pro-GRPO}}(\theta) = \mathbb{E}_{c} \Bigg[ \frac{1}{K} \sum_{g\in\mathcal{K}_{I+1}} \frac{1}{T} \sum_{t=0}^{T-1} \min\Big( r_t^{(g)}(\theta)\widehat{A}^{(g)}, \mathrm{clip}(r_t^{(g)}(\theta), 1-\varepsilon, 1+\varepsilon)\widehat{A}^{(g)} \Big) - \beta D_{\mathrm{KL}}\big(\pi_{\theta}\parallel\pi_{\mathrm{ref}}\big) \Bigg]$$

其中优势 $\widehat{A}^{(g)}$ 基于幸存集 $K$ 的均值和标准差进行组归一化，而非原始全组 $G$。这一设计确保了优势估计不受已被剪枝的冗余轨迹污染。

### 与基线方法的本质差异

Pro-GRPO 与现有 GRPO 基线方法（**Flow-GRPO**, Liu et al., 2025; **DanceGRPO**, Xue et al., 2025）的根本区别不在于目标函数的形式，而在于**采样与优化的耦合方式**：

- 基线方法对所有采样轨迹一视同仁，全部参与完整的去噪和梯度更新，计算成本与 $G$ 线性相关。
- Pro-GRPO 在采样阶段即动态识别并终止奖励聚类轨迹，使有效优化集 $K$ 远小于初始探索集 $G_{\max}$，实现了“探索广度”与“优化深度”的分离。

这种设计使得 Pro-GRPO 能够在扩大初始探索范围（$G_{\max} > G$）的同时，保持甚至降低总计算量，最终在多个基准上实现性能与效率的双重提升（如 Table 1 所示，Pro-GRPO-Flash 达到 1.41× 加速同时超越 Flow-GRPO 基线）。

## 核心模块与公式推导

### 奖励聚类与优势稀释

在 GRPO 的在线采样过程中，给定条件 $c$，策略 $\pi_\theta$ 生成一组 $G$ 条轨迹并获取奖励 $\{R_1, \dots, R_G\}$。Pro-GRPO 首先揭示了一个被现有方法忽视的瓶颈：**奖励聚类（Reward Clustering）**。

设组均值为 $\mu_G = \frac{1}{G}\sum R_i$，标准差为 $\sigma_G$。聚类区域定义为：

$$C_{\delta} = \{ i : |R_i - \mu_G| \le \delta \sigma_G \}$$

落入该区域的轨迹，其组归一化优势被严格限制：

$$|A_i| \le \delta$$

由于各轨迹对梯度的贡献与其优势成比例：

$$g_i \propto A_i \nabla_{\theta} \log \pi_{\theta}(\tau_i)$$

当 $\delta$ 较小时，聚类区域内的轨迹对梯度更新的贡献微乎其微，却消耗了完整的去噪与反向传播计算。图 1(a) 展示了 $G=24$ 时奖励高度集中于均值附近的现象，图 1(b) 进一步表明简单的均匀子采样（$k=12$）无法打破这一聚类结构。

### 最优方差过滤（OVF）

为缓解奖励聚类，Pro-GRPO 提出 **最优方差过滤（Optimal Variance Filtering, OVF）**，从 $G$ 条轨迹中选出大小为 $k$ 的子集 $\mathcal{K}$，使得子集奖励方差最大化：

$$K^{\star} = \arg\max_{\substack{\mathcal{K}\subseteq\{1,\ldots,G\} \\ |\mathcal{K}|=k}} \sigma^2(\mathcal{K})$$

OVF 的核心直觉是：通过选择奖励极值（高奖励与低奖励）样本，打破聚类结构，使子集内的奖励分布向两端扩散（图 1(c)），从而为策略更新提供更强的优势信号。图 2 的训练动态表明，OVF 在训练全程维持更高的奖励标准差，并最终收敛到更高的 PickScore 水平。

### 统一逆向时间 SDE

Pro-GRPO 的剪枝机制依赖于对终态奖励的预测，这建立在扩散与流匹配模型的统一逆向采样框架之上。统一逆向时间 SDE 表述为：

$$\mathrm{d}\mathbf{x}_t = b_{\theta}(\mathbf{x}_t, t)\mathrm{d}t + \sigma_t \mathrm{d}\mathbf{w}_t$$

其中漂移项 $b_{\theta}$ 根据模型类型切换：对于扩散模型，$b_{\theta}$ 包含分数函数 $\nabla_{\mathbf{x}} \log p_t(\mathbf{x}_t)$；对于流匹配模型，$b_{\theta}$ 直接参数化速度场。该统一形式使得后续的代理奖励预测与动态剪枝可同时适用于两类生成模型。

### 代理奖励预测

在去噪过程的预设检查点 $t_i$，Pro-GRPO 对每个活跃轨迹执行单步确定性 ODE 投影，以近似其终态奖励。投影公式为：

$$\hat{\mathbf{x}}_T^{(g)} = \mathbf{x}_{t_i}^{(g)} + \int_{t_i}^{T} b_{\theta}(\mathbf{x}_s, s) \mathrm{d}s \approx \mathbf{x}_{t_i}^{(g)} + b_{\theta}(\mathbf{x}_{t_i}^{(g)}, t_i) \cdot (T - t_i)$$

随后将 $\hat{\mathbf{x}}_T^{(g)}$ 经 VAE 解码得到代理图像，输入奖励模型获得代理奖励 $\hat{R}_i^{(g)}$。该单步近似避免了完整去噪的高昂成本，使剪枝决策的计算开销可忽略。

### 多步 OVF 动态剪枝

在每个检查点 $S_i$，Pro-GRPO 利用代理奖励对当前活跃集 $\mathcal{K}_i$（大小为 $K_i$）执行 OVF，选取高方差子集进入下一阶段：

$$\mathcal{K}_{i+1} = \arg\max_{\substack{\mathcal{K}\subseteq\{1,\ldots,K_i\} \\ |\mathcal{K}|=K_{i+1}}} \frac{1}{K_{i+1}} \sum_{g\in\mathcal{K}} (R_i^{(g)} - \mu_{\mathcal{K}})^2$$

未被选中的轨迹被提前终止（图 3 中的红色叉号），不再参与后续去噪与优化。经过 $I$ 个检查点的逐步剪枝，轨迹数量从初始扩展组 $G_{\max}$ 收敛至最终幸存集 $\mathcal{K}_{I+1}$（大小为 $K$）。

### Pruned GRPO 目标

Pro-GRPO 的策略更新仅基于最终幸存轨迹。首先在幸存集上计算组归一化优势：

$$\widehat{A}^{(g)} = \frac{R(\mathbf{x}_T^{(g)}, c) - \mu_{\mathcal{K}}}{\sigma_{\mathcal{K}} + \epsilon}$$

其中 $\mu_{\mathcal{K}}$ 和 $\sigma_{\mathcal{K}}$ 为幸存集内奖励的均值与标准差。随后沿去噪时间步累积 clipped 重要性采样损失，并附加 KL 正则项：

$$\mathcal{I}_{\mathrm{Pro-GRPO}}(\theta) = \mathbb{E}_{c} \Bigg[ \frac{1}{K} \sum_{g\in\mathcal{K}_{I+1}} \frac{1}{T} \sum_{t=0}^{T-1} \min\Big( r_t^{(g)}(\theta)\widehat{A}^{(g)}, \mathrm{clip}(r_t^{(g)}(\theta), 1-\varepsilon, 1+\varepsilon)\widehat{A}^{(g)} \Big) - \beta D_{\mathrm{KL}}\big(\pi_{\theta}\parallel\pi_{\mathrm{ref}}\big) \Bigg]$$

其中 $r_t^{(g)}(\theta) = \frac{\pi_{\theta}(\mathbf{a}_t^{(g)} \mid \mathbf{s}_t^{(g)})}{\pi_{\mathrm{old}}(\mathbf{a}_t^{(g)} \mid \mathbf{s}_t^{(g)})}$ 为逐步重要性比率。由于只有 $K$ 条轨迹参与反向传播，优化成本与 $K$ 而非 $G_{\max}$ 成正比，实现了探索广度与计算成本的解耦。

### 扩展与剪枝调度

Pro-GRPO 的“先扩展后剪枝”（Expand-and-Prune）策略将上述模块整合为统一调度：初始采样时使用较大的 $G_{\max}$（如 32 或 64）以最大化轨迹多样性，随后通过多步 OVF 剪枝将计算量收敛至 $K$（如 8）。消融实验表明，$G_{\max}$ 从 32 提升至 64 时，域内 HPSv2.1 从 0.386 提升至 0.393，验证了更大初始多样性对优化的益处（Table 5）；在 $T=50$、剪枝路径 $32 \to 8$ 的设置下，检查点 $\{30, 40\}$ 获得最佳性能（Table 6）。

### 补充图表

![[assets/figures/papers/paper_list_l2676_https_arxiv_org_abs_2512_15347/figures/001_Figure_1.jpg]]
*Figure 1: Reward clustering Phenomenon and OVF effects. (a) A full group (G = 24) exhibits pronounced reward clustering. (b) Uniform subsampling (k = 12) preserves the clustering. (c) Our OVF (k = 12) alleviates reward clustering by selecting from the reward extremes*

![[assets/figures/papers/paper_list_l2676_https_arxiv_org_abs_2512_15347/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of training dynamics on PickScore. We compare the Baseline*

## 实验与分析

### 核心瓶颈与设计逻辑

GRPO 在生成模型微调中面临一个关键矛盾：扩大采样组规模以增强探索多样性，会带来高昂的计算开销；然而，直接使用较小的固定组又会导致**奖励聚类（Reward Clustering）**——大量轨迹的奖励集中在组均值附近，归一化优势信号被严重稀释，梯度更新效率低下。Pro-GRPO 的“扩展与剪枝”（Expand-and-Prune）策略正是针对这一瓶颈设计：在采样阶段临时扩展初始轨迹池以最大化多样性，随后通过动态潜在剪枝提前终止奖励集中的冗余轨迹，使最终参与优化的幸存子集保持高奖励方差。这一机制将探索广度与优化成本解耦，实现了性能与效率的双重提升。

### 主实验结果

**流匹配模型（SD3.5-Medium）上的表现。** Table 1 展示了以 PickScore 和 HPSv2 为奖励信号的定量对比。Pro-GRPO（Standard）在 DrawBench 的域内 PickScore 上达到 24.008，较 Flow-GRPO 基线（23.322）提升 +0.686；域内 Aesthetic Score 从 5.912 提升至 6.046（+0.134）。在域外泛化指标上，Pro-GRPO 同样一致优于基线。值得注意的是，Pro-GRPO-Flash 在实现 1.41× 加速的同时，仍全面超越 Flow-GRPO，验证了剪枝策略在效率与性能之间的有效平衡。

**扩散模型（SD-v1.4）上的表现。** Table 2 报告了在单目标（HPSv2.1）和多目标（HPSv2.1 & CLIP）奖励下的结果。Pro-GRPO 在所有域内和域外指标上均优于 DanceGRPO 基线。在多目标设置中，Pro-GRPO 的域外 ImageReward 达到 1.140，域外 Aesthetic 达到 5.852，展现出更强的多目标优化能力和泛化性。

**GenEval 基准测试。** Table 3 显示，在以 PickScore 微调的条件下，Pro-GRPO 的 Overall Score 达到 0.726，高于 Flow-GRPO（0.719）和基模型 SD3.5-M（0.700），在细粒度准确性上也保持领先。

**训练动态。** Figure 5 的奖励轨迹表明，无论是流匹配模型（SD3.5, PickScore）还是扩散模型（SD-v1.4, HPSv2.1），Pro-GRPO 均比各自基线收敛更快、收敛平台更高。在多目标扩散设置中，Pro-GRPO 始终保持稳定的优势边际。

### 计算效率分析

Table 4 的 FLOPs 分解揭示了效率提升的来源。基线 Flow-GRPO 每 epoch 总计算量为 453,474 TFLOPs；Pro-GRPO（Standard）降至 335,627 T（1.26× 加速），Pro-GRPO-Flash 进一步降至 267,366 T（1.41× 加速）。加速的核心机制在于：Pro-GRPO 在采样阶段提前终止奖励聚类轨迹，使得后续去噪和反向传播的计算仅作用于幸存子集 K，而非完整的初始扩展组 G_max。优化成本与 K 而非 G_max 成正比，这是效率增益的根本原因。

![[assets/figures/papers/paper_list_l2676_https_arxiv_org_abs_2512_15347/figures/011_Table_4.jpg]]
*Table 4: Computational efficiency analysis. We report the FLOPs (in Tera) and relative speedup. The top section lists the cost of atomic operations. The bottom section compares the total computational cost of a full epoch, including trajectory sampling and policy optimization. Pro-GRPO reduces the aggregate FLOPs by early-terminating reward-clustered trajectories during the sampling phase*

### 消融实验

**初始扩展组规模 G_max。** Table 5 显示，在 SD-v1.4 + HPSv2.1 的设置下，将 G_max 从 32 扩展至 64 时，域内 HPSv2.1 从 0.386 提升至 0.393。更大的初始采样池带来了更丰富的探索多样性，为后续 OVF 选择高方差子集提供了更优质的候选空间。

**剪枝检查点配置。** Table 6 在 T=50、剪枝路径 32→8 的条件下，对比了不同检查点位置的影响。检查点 {30, 40} 获得最佳域内 HPSv2.1（0.391），表明在去噪过程的中后期进行剪枝最为有效——此时潜在特征已包含足够的终态信息，代理奖励预测更准确，同时仍有足够时间步让幸存轨迹完成高质量去噪。

### 定性分析

Figure 4 的定性对比显示，Pro-GRPO 生成的图像在视觉质量和提示遵循度上均优于 SD3.5-M 基模型和 Flow-GRPO 基线，进一步佐证了剪枝策略在保持高奖励方差子集方面的有效性。

![[assets/figures/papers/paper_list_l2676_https_arxiv_org_abs_2512_15347/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison between SD3.5-M, Flow-GRPO and Pro-GRPO with Pickscore as reward on DrawBench prompts*

### 失败模式与局限

论文未明确报告失败案例或负面结果。从方法设计推断，潜在风险包括：代理奖励预测的准确性依赖于 ODE 投影的质量，若中间时间步的潜在特征不足以可靠预测终态奖励，OVF 可能错误地剪除高潜力轨迹。此外，多步剪枝的超参数（检查点位置、剪枝比例）需要针对不同模型和奖励函数进行调优，泛化到全新设置时可能需要额外的验证成本。这些点需要在实际部署中手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l2676_https_arxiv_org_abs_2512_15347/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison on flow-based text-to-image generation (SD3.5-Medium). We compare Pro-GRPO against the base model and the Flow-GRPO baseline. Note that Pro-GRPO-Flash achieves significant speedup while surpassing the baseline, and Pro-GRPO (Standard) achieves the best overall performance with moderate acceleration. Bold indicates the best result*

![[assets/figures/papers/paper_list_l2676_https_arxiv_org_abs_2512_15347/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison on diffusion-based T2I generation (SD-v1.4). We compare Pro-GRPO against DanceGRPO under single-objective (HPSv2.1) and multi-objective (HPSv2.1 & CLIP) rewards. “In-Domain” refers to the metric used during optimization (HPSv2.1 & CLIP), while “Out-of-Domain” metrics assess generalization. Bold indicates the best performance*

![[assets/figures/papers/paper_list_l2676_https_arxiv_org_abs_2512_15347/figures/009_Table_3.jpg]]
*Table 3: Quantitative evaluation on GenEval benchmark. All models are fine-tuned using the PickScore reward. We report the Overall score and fine-grained accuracies*

![[assets/figures/papers/paper_list_l2676_https_arxiv_org_abs_2512_15347/figures/006_Figure_5.jpg]]
*Figure 5: Training dynamics. Reward trajectories during optimization. (a) Flow-based (SD3.5, PickScore): Pro-GRPO (blue) and Pro-GRPO-Flash (green) converge faster and reach higher plateaus than Flow-GRPO (orange). (b) Diffusion-based (SD-v1.4, HPSv2.1): Pro-GRPO consistently outperforms DanceGRPO throughout training. (c) Diffusion-based (SD-v1.4, HPSv2.1 & CLIP): Pro-GRPO maintains a stable margin, indicating stronger multi-objective optimization*

![[assets/figures/papers/paper_list_l2676_https_arxiv_org_abs_2512_15347/figures/008_Table_5.jpg]]
*Table 5: Ablation study on scaling initial group size*

![[assets/figures/papers/paper_list_l2676_https_arxiv_org_abs_2512_15347/figures/010_Table_6.jpg]]
*Table 6: Ablation study on pruning checkpoints. Experiments are conducted on SD-v1.4*

## 方法谱系与知识库定位

### 1. 问题定位：GRPO 中的奖励聚类与计算瓶颈

Pro-GRPO 的出发点源于对在线强化学习微调生成模型（特别是 GRPO 范式）中两个相互纠缠的瓶颈的观察。第一个瓶颈是**奖励聚类（Reward Clustering）** 现象：在 GRPO 的采样阶段，大量轨迹的奖励值会高度集中在组均值附近，导致其归一化优势 $A_i$ 趋近于零（由 $|A_i| \le \delta$ 严格界住，见 Eq. (8)）。由于各轨迹对梯度的贡献与其优势成比例（$g_i \propto A_i \nabla_{\theta} \log \pi_{\theta}(\tau_i)$），这些奖励聚类的轨迹对策略更新的贡献微乎其微，实质上造成了计算资源的浪费。

第二个瓶颈是**探索与计算成本的冲突**：为了增强探索的多样性，直觉上需要扩大采样组大小 $G$，但这会直接推高去噪采样与反向传播的计算开销。在固定计算预算下，这两个需求构成了根本性的矛盾——更大的 $G$ 带来更多样化的候选轨迹，但其中大量轨迹会因奖励聚类而沦为“无效样本”。

### 2. 与基线方法的关系

**Flow-GRPO**（Liu et al., arXiv 2025）与 **DanceGRPO**（Xue et al., arXiv 2025）分别代表了将 GRPO 应用于流匹配模型和扩散模型的标准在线 RL 微调范式。二者的共同特点是：在采样阶段使用固定大小的轨迹组 $G$，所有采样轨迹均完整经历去噪过程并参与梯度更新，不做任何中途筛选。这一“全量采样-全量优化”的策略直接继承了 GRPO 的原始设计，未对奖励聚类问题做出任何响应。

Pro-GRPO 与上述基线的核心差异在于**在采样过程中引入了主动的轨迹选择机制**。它并不改变 GRPO 的优化目标形式（依然采用 clipped 重要性采样 + KL 正则化），而是通过“先扩展后剪枝”（Expand-and-Prune）的策略重构了采样阶段的轨迹流：

- **初始扩展**：将采样组从固定的 $G$（如 24）扩展至更大的 $G_{\max}$（如 32 或 64），以最大化初始探索的多样性。
- **动态剪枝**：在去噪过程的中间时间步（检查点 $S_i$），对每个活跃轨迹执行单步 ODE 投影以预测终态奖励，并通过**最优方差过滤（Optimal Variance Filtering, OVF）** 选择奖励方差最大的子集继续去噪，其余轨迹提前终止。
- **成本解耦**：由于只有最终幸存子集 $K$ 进入反向传播，优化成本与 $K$ 而非 $G_{\max}$ 成正比，实现了探索广度与优化成本的结构性解耦。

一个简单的对照基线是**均匀子采样（Uniform Subsampling）**——从全组中随机选取 $k$ 条轨迹。实验表明，均匀子采样无法缓解奖励聚类（Figure 1(b)），其训练动态与全量基线几乎一致，而 OVF 则能持续维持更高的奖励方差（Figure 2(a)），从而获得更优的收敛效果。这说明 Pro-GRPO 的增益并非简单来自“使用更少轨迹”，而是源于**有选择地保留高方差子集**这一因果机制。

### 3. 方法谱系中的位置

从方法论角度看，Pro-GRPO 处于**在线 RL 微调生成模型**与**基于中间表示的轨迹筛选**两条线索的交汇点。

在在线 RL 微调生成模型的谱系中，GRPO（Group Relative Policy Optimization）本身是对 PPO 的简化变体，通过组内归一化优势替代了价值网络，降低了训练开销。Flow-GRPO 和 DanceGRPO 将 GRPO 分别适配到流匹配和扩散模型，但在采样效率上延续了“全量采样”的朴素策略。Pro-GRPO 在这一谱系上的推进在于：它揭示了 GRPO 中奖励分布的结构性特征（聚类），并利用这一特征设计了一个与去噪过程耦合的剪枝调度，使采样效率成为可优化的维度。

在轨迹筛选的线索上，Pro-GRPO 的 OVF 机制与主动学习中的不确定性采样、以及演化算法中的锦标赛选择有形式上的相似性——都是基于某种打分函数选择信息量最大的子集。但 Pro-GRPO 的关键创新在于将筛选嵌入到生成过程的中间时间步，利用**潜在空间中的 ODE 投影**在去噪尚未完成时预测终态奖励，从而实现了“提前终止”——这是传统后验筛选方法无法做到的。

### 4. 适用边界与局限

Pro-GRPO 的设计依赖于以下几个前提条件，这些条件也划定了其适用边界：

1. **奖励模型的快速评估能力**：OVF 需要在每个剪枝检查点对当前活跃轨迹进行代理奖励预测。这要求奖励模型（如 PickScore、HPSv2.1）的推理速度足够快，否则剪枝本身的计算开销可能抵消其收益。论文中 Pro-GRPO-Flash 变体通过进一步优化注意力计算来压缩这一开销，说明在奖励模型较重时仍需额外工程适配。

2. **奖励聚类现象的普遍性**：OVF 的有效性建立在“大量轨迹的奖励集中在均值附近”这一观察之上。如果奖励分布本身较为均匀（例如奖励模型区分度低，或任务本身导致奖励方差天然较大），则 OVF 的筛选增益可能减弱。论文未在奖励分布显著不同的任务上进行验证，这一点需要进一步确认。

3. **检查点位置的敏感性**：消融实验（Table 6）表明，剪枝检查点的位置对最终性能有显著影响——在 $T=50$、剪枝路径 $32 \to 8$ 的设置下，检查点 $\{30, 40\}$ 获得最佳 HPSv2.1（0.391），而其他配置可能导致性能下降。这意味着 Pro-GRPO 的超参数（检查点位置、剪枝比例）可能需要针对不同的去噪步数和模型架构进行调优，缺乏自适应的机制。

4. **未验证的场景**：论文的实验集中在文本到图像生成的流匹配模型（SD3.5-Medium）和扩散模型（SD-v1.4）上，使用 PickScore 和 HPSv2.1/CLIP 作为奖励模型。对于其他模态（如视频生成、音频生成）、其他奖励模型类型（如基于视觉-语言模型的细粒度评估），以及更大规模的模型（如 SD3.5-Large），Pro-GRPO 的表现尚待验证。

### 5. 开放问题

- **自适应剪枝调度**：当前 Pro-GRPO 的检查点位置和剪枝比例是预先设定的超参数。是否可能根据奖励分布的实时特征（如方差变化率、聚类程度）动态决定剪枝时机和保留比例，从而减少对手动调参的依赖？

- **与离线偏好优化的结合**：GRPO 是在线方法，需要持续的采样和奖励评估。Pro-GRPO 通过剪枝降低了采样成本，但奖励评估仍是线上进行的。是否可以将 OVF 的方差最大化思想引入离线偏好优化（如 DPO）的数据筛选阶段，在训练前构建高信息量的偏好对？

- **奖励聚类的理论刻画**：论文从实验上展示了奖励聚类现象，但未给出其产生的理论条件。奖励聚类是 GRPO 组归一化的必然结果，还是特定奖励模型与提示分布下的产物？对其理论根源的理解可能导向更根本的解决方案。

- **更大规模模型的扩展性**：Pro-GRPO 在 SD3.5-Medium（约 2.5B 参数）上验证了加速效果。当模型规模进一步增大时，单步 ODE 投影的相对开销是否会变化？Expand-and-Prune 策略在更大规模模型上的收益-开销比需要进一步量化。

## 原文 PDF

![[paperPDFs/CVPR_2026/Expand_and_Prune_Maximizing_Trajectory_Diversity_for_Effective_GRPO_in_Generative_Models.pdf]]
