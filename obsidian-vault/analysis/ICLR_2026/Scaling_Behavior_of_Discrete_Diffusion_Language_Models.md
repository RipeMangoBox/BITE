---
title: "Scaling Behavior of Discrete Diffusion Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Scaling_Behavior_of_Discrete_Diffusion_Language_Models.pdf
project_link: null
code_link: https://github.com/dvruette/gidd-easydel
openreview_forum_id: GDYaNzxt9T
aliases:
- SBDDLM
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "扩散噪声类型（掩码、均匀、混合）以及批次大小、学习率的精心调节是影响缩放行为的关键因果杠杆；尤其是最优批次大小和学习率服从可预测的幂律，使缩放规律外推成为可能。"
primary_logic: "均匀扩散在数据受限（token-constrained）场景下缩放表现更优，所有噪声类型在计算受限（compute-bound）时收敛至相近损失。离散扩散模型相比自回归模型更重参数缩放（模型规模占比更高），在计算最优状态下更具竞争力。最优批次大小随训练 token 数呈近似线性增长（指数0.82），最优学习率随最优批次大小呈幂律增长（指数0.34），且这些规律对模型规模与噪声类型不敏感。"
claims:
- "均匀扩散在 token 受限条件下缩放优于其他噪声类型，计算受限时所有噪声类型收敛。"
- "最优批次大小随训练 token 数量呈幂律缩放，指数约0.82，几乎线性。"
- "学习率退火（annealing）带来约 2.45% 的恒定损失改善，且不改变最优超参数。"
- "在 3B 和 10B 参数规模上的实测损失准确符合从小规模模型外推的缩放趋势。"
---

# Scaling Behavior of Discrete Diffusion Language Models

> [!tip] 核心洞察
> 均匀扩散在数据受限（token-constrained）场景下缩放表现更优，所有噪声类型在计算受限（compute-bound）时收敛至相近损失。离散扩散模型相比自回归模型更重参数缩放（模型规模占比更高），在计算最优状态下更具竞争力。最优批次大小随训练 token 数呈近似线性增长（指数0.82），最优学习率随最优批次大小呈幂律增长（指数0.34），且这些规律对模型规模与噪声类型不敏感。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 离散扩散语言模型的缩放行为 |
| 英文题名 | Scaling Behavior of Discrete Diffusion Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=GDYaNzxt9T) · [GitHub](https://github.com/dvruette/gidd-easydel) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | 基于信噪比（SNR）的广义插值离散扩散模型与通用混合噪声分布 |
| Dataset | 计算约束缩放定律（sq. fit, Method 1）, 下游任务精度（GSM8k, 自适应采样 T=256） |

> [!tip] 效果简介
> - 计算约束缩放定律（sq. fit, Method 1） 上，α_M（模型规模指数） 为 0.589（均匀扩散），对比 0.566（掩码扩散），变化 +0.023。
> - 计算约束缩放定律（sq. fit, Method 1） 上，α_D（数据集规模指数） 为 0.411（均匀扩散），对比 0.434（掩码扩散），变化 -0.023。
> - 计算约束缩放定律（sq. fit, Method 1） 上，α_L（损失指数） 为 -0.0522（均匀扩散），对比 -0.0496（掩码扩散），变化 -0.0026。

## 概要

### 问题与瓶颈

离散扩散语言模型（DLMs）作为自回归模型（ALMs）之外的另一条生成范式，其缩放行为此前尚未被充分刻画。既有工作存在两个关键盲区：一是局限于掩码扩散（masked diffusion），未系统比较不同噪声类型（尤其是均匀扩散）在缩放场景下的表现差异；二是关键超参数（批次大小、学习率）未做系统优化，导致无法准确刻画计算最优的缩放曲面。本文的核心瓶颈正在于填补这一空白——在统一的实验框架下，对掩码、均匀及混合扩散进行受控缩放实验，并揭示超参数自身的缩放规律。

### 核心结论

1. **噪声类型的分化与收敛**：在数据受限（token-constrained）场景下，均匀扩散的缩放表现显著优于掩码扩散（数据集规模指数 $\alpha_D$ 分别为 0.411 与 0.434）；而在计算受限（compute-bound）场景下，所有噪声类型的损失缩放趋于收敛（均匀 $\alpha_L = -0.0522$，掩码 $\alpha_L = -0.0496$）。这一发现将噪声类型确立为影响缩放行为的关键因果杠杆。

2. **超参数的幂律缩放**：最优批次大小 $B^*$ 随训练 token 数呈近似线性增长（指数 0.82），最优学习率 $\eta^*$ 随 $B^*$ 呈幂律增长（指数 0.34），且这些规律对模型规模和噪声类型不敏感。这意味着超参数本身可以被外推预测，无需对每个规模重新搜索。

3. **DLMs 更重参数缩放**：与自回归模型的 Chinchilla 缩放定律（Hoffmann et al., 2022）和 DeepSeek 缩放定律（Bi et al., 2024）相比，离散扩散模型在计算最优配置下更倾向于分配更多算力给模型规模而非训练数据量，即“参数偏重”的缩放特性。

4. **外推验证**：基于小规模模型（≤1B 参数）拟合的缩放定律，在 3B 和 10B 参数规模、最高 50 倍计算预算的外推实验中保持了准确的预测能力，证实了缩放规律的可靠性。

### 方法定位

本文提出的方法在离散扩散模型谱系中占据一个承上启下的位置。它以广义插值离散扩散（GIDD）为理论框架，通过信噪比（SNR）重参数化实现噪声调度不变性，并在此基础上构建通用混合噪声分布 $\pi_\lambda = \sigma(a\lambda+b)\mathbf{u} + (1-\sigma(a\lambda+b))\mathbf{m}$，使掩码与均匀扩散之间的平滑过渡成为可能。这一设计既统一了现有离散扩散的噪声类型，又为未来探索更复杂的噪声调度提供了接口。

在知识库定位上，本文与以下基线形成明确对比：
- **Chinchilla 缩放定律**（Hoffmann et al., 2022）与 **DeepSeek 缩放定律**（Bi et al., 2024）：作为自回归模型的计算最优缩放基线，本文揭示了 DLM 与 ALM 在 token-参数配比上的系统性差异。
- **MDM 缩放定律**（Nie et al., 2025a; Ni et al., 2025）：作为已有的掩码扩散缩放研究，本文在噪声类型覆盖和超参数优化深度上均有显著扩展，且部分消融了文献间关于掩码扩散缩放方向的分歧。

### 主要结果概览

| 维度 | 关键发现 | 证据锚点 |
|------|---------|---------|
| 噪声类型缩放 | 均匀扩散 token-constrained 更优；compute-bound 收敛 | Figure 4, Table 1 |
| 超参数缩放 | $B^* \propto (\text{tokens})^{0.82}$，$\eta^* \propto (B^*)^{0.34}$ | Figure 3, Table 6 |
| 外推验证 | 3B/10B 模型实测损失准确符合外推趋势 | Figure 1, Figure 4 |
| 学习率退火 | 带来约 2.45% 的恒定改善，不改变最优超参数 | Figure 5 |
| 下游任务 | 均匀扩散 + 自适应采样在 GSM8k 上优于掩码扩散 | Table 3 |

**注意**：上述缩放系数基于 Nemotron-CC 数据集（未经质量过滤）和特定 FLOP 估计方法（Method 1），对不同数据集和 FLOP 计算方式的敏感性已在附录中讨论（Figure 10, Table 7），但跨数据集的泛化性仍需进一步验证。



### 离散扩散语言模型的兴起与瓶颈

自回归语言模型（ALMs）长期主导大语言模型领域，其计算最优缩放定律（如 **Chinchilla** 由 Hoffmann et al., 2022 提出，**DeepSeek** 由 Bi et al., 2024 提出）为训练资源配置提供了成熟指导。然而，离散扩散语言模型（DLMs）作为一类生成范式，凭借其并行解码和灵活的条件生成能力，正逐渐成为有竞争力的替代方案。

当前 DLM 缩放研究存在一个核心瓶颈：**先前工作未充分探索不同噪声类型（特别是均匀扩散与混合扩散）对缩放行为的影响，同时关键超参数（批次大小、学习率）缺乏系统优化**。这导致现有 DLM 缩放定律（如 **MDM** 的掩码扩散缩放，Nie et al., 2025a；Ni et al., 2025）无法准确刻画计算最优的模型规模与数据规模配置，也难以可靠外推至更大规模训练。

### 现有方法的三重缺口

1. **噪声类型探索不足**：现有 DLM 缩放研究几乎全部聚焦于掩码扩散（masked diffusion），均匀扩散（uniform diffusion）在大规模下的行为仍是开放问题。有限的消融实验规模过小，无法揭示不同噪声类型在计算受限（compute-bound）与数据受限（token-constrained）两种场景下的缩放差异。

2. **超参数优化缺位**：批次大小和学习率通常被视为固定或经验选择，未纳入缩放定律的优化框架。这导致无法回答“在给定计算预算下，最优批次大小和学习率应如何随模型规模和数据量变化”这一关键问题。

3. **方法论框架不统一**：传统 GIDD（Generalized Interpolating Discrete Diffusion）ELBO 基于时间参数化，噪声调度与损失形式耦合紧密，难以灵活实现掩码与均匀噪声的平滑插值，也阻碍了混合噪声类型的系统性缩放研究。

### 本文动机与核心思路

针对上述缺口，本文旨在建立**离散扩散语言模型的计算最优缩放定律**，并系统比较不同噪声类型的缩放行为。核心思路包含三个层面：

- **方法论层面**：提出基于信噪比（SNR）的 GIDD ELBO 重参数化（Proposition 1），实现噪声调度不变性，并在此基础上构建通用混合噪声分布，通过 sigmoid 函数平滑过渡掩码与均匀扩散。

- **超参数层面**：将批次大小和学习率纳入缩放优化的核心变量，揭示其与训练 token 数的幂律关系，使最优配置可预测、可外推。

- **实证层面**：在高达 10B 参数、1022 FLOPs 的计算规模上验证缩放定律的外推准确性，并比较 DLM 与 ALM 在计算最优状态下的竞争力。



## 核心方法与创新机理

### 基于信噪比的广义插值离散扩散统一框架

本工作将离散扩散语言模型（DLM）的缩放行为研究建立在一个统一的**广义插值离散扩散（GIDD）**框架之上。核心创新在于对 GIDD 的证据下界（ELBO）进行**信噪比重参数化**，并据此构造**通用混合噪声分布**，从而系统性地揭示了噪声类型对缩放行为的因果影响。

#### 信噪比重参数化：从时间到 λ 的范式转换

传统 GIDD 的 ELBO 以时间 $t$ 为变量（Eq. 2），其形式为：

$$-\log p_\theta(x) \leq \mathbb{E}_{t\sim\mathcal{U}(0,1), z\sim q_t(x)} [ w_t(x)_z \{ D_{KL}(q_t(x)\|q_t(x_\theta)) + D_{IS}(q_t(x)_z\|q_t(x_\theta)_z) \} ] + C_s$$

本文提出以**对数信噪比 λ** 替代时间 $t$ 作为扩散过程的基本变量（Proposition 1），将 ELBO 重写为对 λ 的重要性采样形式：

$$-\log p(x) \le \mathbb{E}_{\lambda, z} [ \frac{w_\lambda(x)_z}{p(\lambda)} \{ D_{KL}(q_\lambda(x)\|q_\lambda(x_\theta)) + D_{IS}(q_\lambda(x)_z\|q_\lambda(x_\theta)_z) \} ] + C$$

这一重参数化具有两个关键优势。**其一**，它揭示了插值离散扩散与连续扩散一样具有**噪声调度不变性**——扩散过程的定义不再依赖于特定的时间参数化，而是由信噪比的变化轨迹唯一决定。**其二**，它使得混合噪声分布的实现变得极为简洁：只需计算混合先验 $\pi_\lambda$ 对 λ 的导数 $\pi_\lambda'$，即可完成损失函数的计算，无需对时间调度做任何额外适配。

#### 通用混合噪声分布：掩码与均匀扩散的平滑过渡

基于 SNR 参数化的 ELBO，本文提出**通用混合噪声分布**（Eq. 6）：

$$\pmb{\pi}_\lambda = \sigma(a\lambda + b) \pmb{u} + (1 - \sigma(a\lambda + b)) \pmb{m}$$

该分布通过 sigmoid 函数在**掩码向量 m** 与**均匀向量 u** 之间实现平滑过渡。参数 $a$ 控制过渡的陡峭程度，$b$ 控制过渡点在信噪比轴上的位置。这一设计使得研究者可以灵活地在纯掩码扩散（$a \to -\infty$）、纯均匀扩散（$a \to +\infty$）及其任意中间态之间进行插值，从而为系统比较不同噪声类型的缩放行为提供了统一的实验平台。

### 超参数缩放定律的发现与利用

本工作另一项关键创新在于**将批次大小和学习率从固定超参数提升为可预测的缩放变量**，而非像先前工作那样将其视为需独立搜索的常数。

#### 最优批次大小的幂律缩放

通过对不同模型规模、噪声类型和训练 token 数进行系统网格搜索，本文发现**最优批次大小 $B^*$ 随训练 token 数呈近似线性幂律缩放**，指数约为 0.82（Figure 3 左，Table 6 总体斜率 $0.8225 \pm 0.0104$）。这一规律对模型规模和噪声类型不敏感——尽管均匀噪声倾向于略大的最优批次（斜率 0.8787 vs 掩码 0.7759），但整体趋势高度一致。更重要的是，$B^*$ 与训练 FLOPs、模型大小或目标损失之间**不存在**同样清晰的幂律关系，说明训练 token 数量才是驱动批次大小选择的核心变量。

#### 最优学习率对批次大小的幂律依赖

在批次大小已被设为最优的前提下，**最优学习率 $\eta^*$ 与最优批次大小之间服从幂律**，指数约为 0.34（Figure 3 右）。这一关系同样对噪声类型和模型规模具有鲁棒性，意味着一旦确定了给定训练 token 数下的 $B^*$，即可通过幂律外推得到对应的 $\eta^*$，无需额外搜索。

#### 舍弃学习率退火的策略选择

与主流做法不同，本文在缩放实验中**统一省略了学习率退火**，代之以预热后恒定的学习率调度。这一策略使得单次训练运行即可覆盖所有训练时间点的损失记录，大幅降低了计算最优曲面估计的成本。消融实验（Figure 5）表明，退火仅带来约 **2.45% ± 0.138%** 的常数级损失改善，且**不影响最优超参数的取值**——该改善在 3B 和 10B 参数规模上保持恒定，验证了“无退火”范式在缩放定律研究中的有效性。

### 训练目标的简化：非加权 ELBO 作为代理损失

本文在训练中采用**非加权 ELBO**（将 Eq. 5 中的 $p(\lambda)$ 设为 1）作为代理损失，而非直接优化完整的加权 ELBO。这一简化在实践中带来了更好的收敛性，且由于 SNR 重参数化已消除了时间调度对损失权重的影响，非加权 ELBO 在理论上也是合理的选择。

### 创新点的因果链条

上述创新构成了一个紧密的因果链条：**SNR 重参数化**使得混合噪声分布的实现成为可能，进而支持对掩码、均匀及混合噪声的系统缩放比较；**超参数缩放定律**的发现使得批次大小和学习率可从训练 token 数直接预测，大幅降低了计算最优配置的搜索成本；**舍弃退火**和**非加权 ELBO** 则进一步简化了训练流程，使缩放定律的估计更加高效可靠。这一整套方法论使得本文能够在仅使用小规模模型（最大 1B 参数）拟合缩放定律后，准确外推至 3B 和 10B 参数、计算预算扩大 50 倍的实验设置（Figure 1, Figure 4）。



![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_GDYaNzxt9T/figures/036_Figure_10.jpg]]
*Figure 10: The fitted scaling coefficients differ systematically between FLOP estimation techniques: Method 1 uses the FLOP estimation technique proposed by Bi et al. (2024) whereas method 2 uses the classic approach by Hoffmann et al. (2022). Furthermore, fitting on interpolated data (squared fit) produces tighter confidence bounds and better scaling exponents. Shaded regions denote 95% confidence intervals obtained via standard bootstrapping on the aggregated data points*

本文构建了一套完整的离散扩散语言模型（DLM）缩放定律研究框架，其核心 pipeline 由三个紧密耦合的模块组成：**信噪比（SNR）参数化的广义插值离散扩散（GIDD）前向过程**、**通用混合噪声分布**，以及**面向缩放定律的超参数优化与推理策略**。整个框架的输入为大规模文本语料（Nemotron-CC），输出为不同噪声类型和模型规模下的计算最优缩放系数及下游任务性能。

### Pipeline 模块关系与数据流

**1. SNR‑参数化的 GIDD 前向过程**

该模块是整个框架的理论基础。传统 GIDD 以时间 $t$ 定义加噪过程，其 ELBO 形式为：

$$-\log p_\theta(x) \leq \mathbb{E}_{t\sim\mathcal{U}(0,1), z\sim q_t(x)} [ w_t(x)_z \{ D_{KL}(q_t(x)\|q_t(x_\theta)) + D_{IS}(q_t(x)_z\|q_t(x_\theta)_z) \} ] + C_s$$

本文将其重参数化为对数信噪比 $\lambda$ 的函数（Proposition 1），使 ELBO 转变为对 $\lambda \sim p(\lambda)$ 的重要性采样期望：

$$-\log p(x) \le \mathbb{E}_{\lambda, z} [ \frac{w_\lambda(x)_z}{p(\lambda)} \{ D_{KL}(q_\lambda(x)\|q_\lambda(x_\theta)) + D_{IS}(q_\lambda(x)_z\|q_\lambda(x_\theta)_z) \} ] + C$$

这一重参数化实现了**噪声调度不变性**——扩散过程的行为不再依赖具体的时间调度函数，仅由 SNR 决定。这为后续混合噪声分布的统一实现扫清了理论障碍，同时简化了训练损失的实现。

**2. 通用混合噪声分布**

在 SNR 参数化基础上，本文提出一个统一的混合先验分布，通过 sigmoid 函数在掩码向量 $\pmb{m}$ 和均匀向量 $\pmb{u}$ 之间平滑过渡：

$$\pmb{\pi}_\lambda = \sigma(a\lambda + b) \pmb{u} + (1 - \sigma(a\lambda + b)) \pmb{m}$$

其中参数 $a$ 控制过渡速度，$b$ 控制过渡点。该分布在高 SNR（低噪声）区域退化为掩码扩散，在低 SNR（高噪声）区域退化为均匀扩散，中间区域实现平滑插值。这一设计使得单一框架即可覆盖纯掩码、纯均匀及任意混合态，为系统比较不同噪声类型的缩放行为提供了统一的实验平台。

**3. 面向缩放定律的超参数优化与训练/推理策略**

该模块接收前两个模块定义的损失函数，执行大规模网格搜索以确定计算最优配置。具体流程为：

- **架构与优化器**：采用 CompleteP（µP 变体）实现跨宽度和深度的学习率迁移，配合 SquaredReLU 激活、RMSNorm、QK‑norm、soft‑capping 和 attention sinks 等组件构建 Transformer 骨干网络。使用 LaProp 优化器以获得更广范围内 $\beta_2$ 和 $\epsilon$ 的稳定性。
- **损失函数**：实际训练使用**非加权 ELBO**（设 $p(\lambda):=1$）作为代理损失，相比原始加权 ELBO 具有更好的收敛性。
- **学习率调度**：采用预热 2000 步后保持恒定的调度，**省略学习率退火**。这一关键设计使得单次训练即可捕获所有训练时间步的损失信息，大幅降低了超参数搜索的计算开销。后续消融实验证实，退火仅带来约 2.45% 的恒定损失改善，不影响最优超参数的确定。
- **超参数幂律外推**：通过网格搜索发现，最优批次大小 $B^*$ 随训练 token 数呈近似线性幂律增长（指数约 0.82），最优学习率 $\eta^*$ 随 $B^*$ 呈幂律增长（指数约 0.34），且这些规律对模型规模和噪声类型不敏感。这使得从小规模实验外推大规模最优配置成为可能。
- **推理策略**：采用扩散强制（Diffusion Forcing）进行条件 prompt 完成，配合自适应置信度采样（confidence‑based adaptive sampling），根据 token 置信度动态分配去噪步数，均匀扩散模型在此策略下尤为受益。

整个 pipeline 的输出流为：在给定计算预算下，不同噪声类型（掩码、均匀、混合）的**计算最优缩放系数**（$\alpha_M$、$\alpha_D$、$\alpha_L$）及对应的**下游任务性能**。这些系数通过幂律 $A C^\alpha$（其中 $C = M D$）拟合得到，并经 3B 和 10B 参数规模的实测验证，证实了从小模型外推的准确性。



### SNR‑参数化的广义插值离散扩散 (GIDD)

本文的方法基础建立在 **广义插值离散扩散模型 (GIDD)** 之上。GIDD 的前向加噪过程定义了一族插值分类分布：

$$q_t(x) = \alpha_t x + \beta_t \pi_t, \quad q_{t|s}(z_s) = \alpha_{t|s} z_s + \beta_{t|s} \pi_{t|s}$$

其中 $x$ 为原始数据的 one‑hot 向量，$\pi_t$ 为与时间相关的先验分布向量，$\alpha_t$ 和 $\beta_t$ 控制信号保留与噪声注入的比例。原始 GIDD 的负 ELBO 为：

$$-\log p_\theta(x) \leq \mathbb{E}_{t\sim\mathcal{U}(0,1), z\sim q_t(x)} [ w_t(x)_z \{ D_{KL}(q_t(x)\|q_t(x_\theta)) + D_{IS}(q_t(x)_z\|q_t(x_\theta)_z) \} ] + C_s$$

其中 $D_{KL}$ 为 KL 散度，$D_{IS}$ 为 Itakura‑Saito 散度，权重向量 $w_t(x)$ 由下式定义：

$$w_t(x) = \frac{1}{q_t(x)} \left( \beta_t \pi_t' - \frac{\alpha_t'}{\alpha_t} \pi_t \right)$$

该权重向量的计算依赖于先验分布 $\pi_t$ 及其导数 $\pi_t'$ 的具体形式，这使得不同噪声类型（掩码、均匀）的实现需要单独处理。

**核心创新：基于信噪比 (SNR) 的重参数化。** 作者将上述过程从时间 $t$ 重参数化为对数信噪比 $\lambda = \log(\alpha_t / \beta_t)$，得到前向过程：

$$q_\lambda(x) = \sigma(\lambda) x + \sigma(-\lambda) \pi_\lambda$$

其中 $\sigma(\cdot)$ 为 sigmoid 函数。**命题 1** 表明，GIDD ELBO 可表达为在 $\lambda \sim p(\lambda)$ 上的重要性采样期望：

$$-\log p(x) \le \mathbb{E}_{\lambda, z} \left[ \frac{w_\lambda(x)_z}{p(\lambda)} \{ D_{KL}(q_\lambda(x) \| q_\lambda(x_\theta)) + D_{IS}(q_\lambda(x)_z \| q_\lambda(x_\theta)_z) \} \right] + C$$

这一重参数化带来了两个关键性质：
1. **噪声调度不变性**：ELBO 不再显式依赖于时间参数化，与连续扩散模型一致，理论上更自然。
2. **实现简化**：不同噪声类型的差异被压缩至 $\pi_\lambda$ 及其导数 $\pi_\lambda'$ 中，为统一处理混合噪声提供了基础。

在实际训练中，作者并未直接最小化上述 ELBO，而是采用 **非加权 ELBO**（设 $p(\lambda) := 1$）作为代理损失函数，获得了更好的收敛性。

### 通用混合噪声分布

基于 SNR 参数化框架，作者提出了 **通用混合噪声分布**，通过 sigmoid 函数在掩码噪声向量 $m$ 和均匀噪声向量 $u$ 之间平滑过渡：

$$\pi_\lambda = \sigma(a\lambda + b) u + (1 - \sigma(a\lambda + b)) m$$

其中：
- $a$ 控制过渡的陡峭程度（transition speed），
- $b$ 控制过渡发生的 $\lambda$ 位置（transition point）。

当 $a \to \infty$ 时，该分布在某个临界 $\lambda$ 处从纯掩码噪声突变为纯均匀噪声；当 $a$ 取有限值时，分布平滑地融合两种噪声类型。该混合分布的导数具有简洁的解析形式：

$$\pi_{\lambda}^{\prime} = a \sigma^{\prime}(a \lambda + b)(u - m)$$

这使得损失函数中权重向量 $w_\lambda(x)$ 的计算可以统一处理，无需为每种噪声类型单独实现。该设计覆盖了纯掩码扩散、纯均匀扩散以及任意中间混合态，为系统比较不同噪声类型的缩放行为提供了统一的实验平台。

### 架构与优化配置

模型架构采用 **CompleteP** 参数化策略，确保最优学习率可跨模型宽度和深度迁移。具体配置包括：
- **激活函数**：MLP 层使用 Squared ReLU。
- **归一化层**：每个注意力和 MLP 块前使用 RMSNorm（无偏置），同时对键和查询施加 QK‑norm。
- **优化器**：采用 LaProp 替代 Adam，在更宽的 $\beta_2$ 和 $\epsilon$ 范围内具有更好的稳定性。
- **学习率调度**：前 2000 步预热至目标学习率，之后保持恒定，**不采用退火**。这一选择使得单次训练运行即可捕获所有训练时长的损失轨迹，是后续超参数缩放定律分析的关键前提。

通过网格搜索在 25M 和 50M 参数模型上确定了最优初始化方差（$\sigma_{\text{base}} = 0.4$, $\sigma_{\text{aux}} = 0.02$）和基础学习率（$\eta_{\text{base}} = 0.3$, $\eta_{\text{aux}} = 0.02 \cdot \eta_{\text{base}}$，批次大小为 64 时）。



## 实验与关键发现

### 核心缩放定律与最优超参数

本文通过系统性的超参数网格搜索（Table 5），在 25M 至 10B 参数规模、不同噪声类型（掩码、均匀、混合）下，建立了离散扩散语言模型（DLM）的计算最优缩放定律。关键发现如下：


![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_GDYaNzxt9T/figures/018_Table_5.jpg]]
*Table 5: List of key hyperparameters for our grid search. The parameters that are swept over are noise type, model size (Tab. 4), batch size, and learning rate*

**计算约束缩放定律（Compute‑constrained scaling laws）**：采用幂律形式 $A C^\alpha$（其中 $C = M D$ 为计算量）拟合各噪声类型的损失、模型规模和数据集规模缩放指数。Table 1 和 Table 7 汇总了完整系数。均匀扩散在所有噪声类型中表现最优：其损失指数 $\alpha_L = -0.0522$ 略优于掩码扩散的 $\alpha_L = -0.0496$；模型规模指数 $\alpha_M = 0.589$ 高于掩码扩散的 $0.566$，表明均匀扩散更倾向于将计算预算分配给模型参数而非训练 token。相应地，均匀扩散的数据集规模指数 $\alpha_D = 0.411$ 低于掩码扩散的 $0.434$。这一趋势在 Figure 4（左）中得到直观呈现：计算受限场景下各噪声类型的损失曲线趋于收敛，但均匀扩散始终保持微弱优势。


![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_GDYaNzxt9T/figures/007_Table_1.jpg]]

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_GDYaNzxt9T/figures/037_Table_7.jpg]]
*Table 7: Compute-constrained scaling coefficients for all noise types, metrics, and methodologies, obtained by fitting the power law A $C ^ { \ l \alpha }$ (where C = M D ) to the observed data. Method 1 uses the FLOP/tok estimation from Bi et al. (2024) while method 2 uses the classic M = 6 P approximation (Hoffmann et al., 2022). ‘raw’ interpolation refers to taking the optimal observed value for a given iso-FLOP target (i.e. no interpolation), whereas the ‘sq. fit’ data is obtained by fitting a parabola to the observed values and taking the optimum thereof. Smallest scaling coefficients are bolded*

**Token 约束缩放定律（Token‑constrained scaling laws）**：在固定训练 token 数的条件下，均匀扩散的优势更为显著。Figure 4（右）显示，均匀扩散的损失曲线在 token 受限时明显低于掩码和混合扩散，且这一优势随计算预算增大而持续。这一定性结论与计算约束下的定量系数差异相互印证：均匀扩散更“参数密集型”，在数据有限时能更有效地利用模型容量。

**最优批次大小与学习率的幂律关系**：Figure 3 揭示了两个对缩放实践至关重要的规律。首先，最优批次大小 $B^*$ 随训练 token 数呈近似线性的幂律缩放，整体斜率为 $0.8225 \pm 0.0104$（Table 6），而非随目标损失或模型规模变化。其次，最优学习率 $\eta^*$ 随最优批次大小呈幂律增长，指数约为 $0.34$。Table 6 进一步按噪声类型分解了这些斜率：均匀扩散的批次大小斜率（$0.8787$）高于掩码扩散（$0.7759$），表明均匀噪声倾向于需要更大的最优批次；而学习率对噪声类型不敏感。这些幂律关系对模型规模具有鲁棒性，使得从小模型外推最优超参数成为可能。


![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_GDYaNzxt9T/figures/019_Table_6.jpg]]
*Table 6: Optimal batch size $B ^ { * }$ Optimal learning rate $\eta ^ { * }$*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_GDYaNzxt9T/figures/020_Table_6.jpg]]
*Table 6: Slope and R ^ { 2 } values for optimal batch size vs. training tokens and optimal learning rate vs. (optimal) batch size, grouped by noise type and model size. While model size does not have a strong effect on the optimal batch size, there is a consistent pattern of higher proportions of uniform noise requiring larger batch sizes to reach optimal performance. For the optimal learning rate, neither model size nor noise type appear to have a significant effect*

### 缩放定律的外推验证

为验证缩放定律的可靠性，本文在 3B 和 10B 参数模型上进行了外推测试，训练计算量达到拟合所用最大计算预算的 50 倍。Figure 1 和 Figure 4 的外推结果表明，从小规模模型（最大约 1B 参数）拟合的缩放定律准确预测了大规模模型的损失。这一验证覆盖了掩码扩散（3B）和均匀扩散（3B 与 10B），证实了缩放定律的泛化性。此外，Figure 5(c) 显示，学习率退火带来的约 2.45% 恒定损失改善同样准确外推至 3B 和 10B 运行，进一步增强了外推的可信度。

### 学习率退火的消融

本文默认采用无退火的预热‑恒定学习率调度，以单次运行捕获所有训练时长下的损失。Section 4.4 的消融实验（Figure 5）系统评估了退火的影响：

- **对最优超参数的影响**：Figure 5(a) 对比了有无 20% 冷却（cooldown）退火下的最优批次大小和最优学习率。结果表明，退火不改变最优超参数值，仅带来约 $2.45\% \pm 0.138\%$ 的恒定损失改善。
- **对不同训练时长的影响**：Figure 5(b) 显示，该恒定改善在不同训练 token 数下保持一致，不随训练时长变化。
- **外推稳定性**：如前所述，这一恒定改善在 3B 和 10B 模型上依然成立。

因此，省略退火在简化实验设计的同时，不影响缩放定律的估计，且退火带来的收益可作为常数因子后验补偿。

### 批次大小与步数的双曲线关系

Section 4.5 揭示了在固定损失下，批次大小 $B$ 与训练步数 $S$ 之间存在紧密的双曲线关系（Figure 6），可由以下方程描述：

$$\left( \left[ \frac{S}{S_{\min}} \right]^{\alpha} - 1 \right) \left( \left[ \frac{B}{B_{\min}} \right]^{\alpha} - 1 \right) = 1$$

其中 $S_{\min}$ 和 $B_{\min}$ 分别为渐近最小步数和最小批次大小，$\alpha$ 为“刚度”参数。基于此关系，可推导出 token 最优的 $(B^*, S^*)$ 配置：

$$B^* = 2^{1/\alpha} B_{\min}, \quad S^* = 2^{1/\alpha} S_{\min}, \quad D^* = 4^{1/\alpha} B_{\min} S_{\min}$$

这一关系为在固定计算预算下选择批次大小和训练步数提供了理论依据，且与前述最优批次大小的幂律规律相互补充。

### 下游任务性能验证

Table 2 展示了缩放模型在多个下游任务上的性能。总体上，下游表现与 ELBO 趋势正相关，但存在噪声类型间的细微差异：3B 掩码模型在平均得分上略优于 3B 均匀模型，尽管均匀扩散的 ELBO 更优。这表明 ELBO 改善并非在所有任务上线性转化为精度提升。


![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_GDYaNzxt9T/figures/012_Table_2.jpg]]
*Table 2: Downstream performance of our scaled models generally correlates with ELBO, with the 3B masked model slightly outperforming the 3B uniform model on average*

Table 3 聚焦于 GSM8k 数学推理任务，对比了不同推理策略。自适应置信度采样（confidence‑based adaptive sampling）对所有模型均带来显著精度提升。更重要的是，均匀扩散在任何推理设置下均优于掩码扩散，且可通过增加去噪步数 $T$ 进一步提升精度：在 $T=256$ 时，均匀 10B 模型达到 $2.43\%$ 的准确率，显著高于掩码 3B 的 $1.67\%$。这揭示了均匀扩散在推理时具有更强的“计算换精度”能力。


![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_GDYaNzxt9T/figures/013_Table_3.jpg]]
*Table 3: Confidence-based, or adaptive, sampling improves accuracy on GSM8k noticeably for all models. Furthermore, uniform diffusion outperforms masked diffusion in any setting and is able to further improve accuracy by investing more denoising steps T*

### FLOP 估计方法与插值的影响

附录中的 Figure 10 和 Table 7 系统分析了 FLOP 估计方法对缩放系数的影响。Method 1（Bi et al., 2024 的 $M = 6P + 12LDN$）与 Method 2（Hoffmann et al., 2022 的 $M = 6P$）产生系统性差异，但插值平滑后趋势一致。Figure 11 和 Figure 12 进一步对比了插值数据（squared fit）与原始观测值的拟合效果：插值有效平滑了噪声，产生更紧的置信区间和更优的拟合优度（Table 8）。Table 9 显示，加入不可约项 $E$ 的拟合中 $E \approx 0$，验证了纯幂律形式的充分性。


![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_GDYaNzxt9T/figures/040_Table_8.jpg]]
*Table 8: Goodness of fit (as per R ^ { 2 } ) for all noise types, metrics, and methodologies. Interpolated values (‘sq. fit’) generally yield a better fit due to the smoothing effect of interpolation, with the exception for the loss, where ‘raw’ values are already rather smooth*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_GDYaNzxt9T/figures/041_Table_9.jpg]]
*Table 9: Scaling coefficients with intercept, obtained by fitting the power law A $C ^ { \alpha }$ + E to the data. The fits almost always have E $\approx$ 0 , except for the uninterpolated loss values $\scriptstyle ( \mathbf { \dot { r a w } }$ ) , leading us to conclude that setting E = 0 is a valid assumption for our setting

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_GDYaNzxt9T/figures/038_Figure_11.jpg]]
*Figure 11: Compute-optimal scaling laws fitted to interpolated values (squared fit). The FLOP estimation methodologies by Bi et al. (2024) (Method 1) and Hoffmann et al. (2022) (Method 2) differ significantly since the FLOP-approximation used by Hoffmann et al. (2022) ( M = 6 P ) systematically underestimates the total number of FLOPs executed during training*

### 局限性与开放问题

尽管缩放定律在 10B 规模上得到验证，但以下局限需注意：所有实验基于 Nemotron‑CC 数据集（未做质量过滤），缩放系数对数据集组成敏感；实验仅覆盖英语文本，未验证多语言或代码场景；与业界数千亿参数的自回归模型仍有差距，外推存在不确定性。开放问题包括：临界批次大小在更大规模下是否会饱和；如何将最优超参数的幂律关系纳入自动化调参框架（如 µTransfer）；均匀扩散在 token 受限场景下的优势能否通过更先进的混合噪声调度进一步放大。

### 补充图表

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_GDYaNzxt9T/figures/017_Table_4.jpg]]
*Table 4: Overview of the five different model sizes that were used in our experiments. Parameter counts refer to non-embedding parameters*




## 定位与知识库关联

### 在扩散语言模型谱系中的位置

本文工作建立在广义插值离散扩散（Generalized Interpolating Discrete Diffusion, GIDD）框架之上，通过信噪比（SNR）重参数化将 GIDD ELBO 表达为对对数信噪比的重要性采样过程（Proposition 1），从而获得噪声调度不变性。这一理论改造使得掩码扩散（masked diffusion）与均匀扩散（uniform diffusion）可以在统一的 SNR 参数空间内被描述，并自然地引出通用混合噪声分布——通过 sigmoid 函数在掩码向量与均匀向量之间平滑过渡。从方法谱系看，该工作位于离散扩散模型从“固定噪声类型、固定调度”走向“噪声类型可插值、调度可自适应”的关键节点。

与已有离散扩散缩放研究的对比：

- **MDM scaling law (Nie et al., 2025a)** 与 **MDM scaling law (Ni et al., 2025)** 均仅针对掩码扩散进行缩放定律拟合，且二者在计算最优 token‑参数比上存在明显分歧：前者预测更重参数缩放，后者预测更重 token 缩放。本文在相同掩码噪声设定下复现了这一分歧（Figure 2），并指出可能源于数据集、FLOP 估计方法和超参数搜索范围的差异。
- 本文首次将均匀扩散和混合扩散纳入系统缩放研究，发现均匀扩散在 token 受限场景下缩放指数更优（α_D = 0.411 vs 掩码的 0.434，Table 1），而在计算受限场景下所有噪声类型趋于收敛。这一发现填补了先前工作仅关注掩码噪声的空白。

### 与自回归语言模型缩放定律的关系

本文明确将离散扩散语言模型（DLMs）的计算最优缩放行为与自回归语言模型（ALMs）的经典缩放定律进行对比：

- **Chinchilla scaling law (Hoffmann et al., 2022)** 和 **DeepSeek scaling law (Bi et al., 2024)** 作为 ALM 计算最优缩放基线，均倾向于更高的 token‑参数比（即更重 token 缩放）。相比之下，本文发现 DLMs——尤其是均匀扩散——在计算最优状态下更重参数缩放（模型规模指数 α_M = 0.589，高于 ALM 典型值），这意味着在相同计算预算下，DLMs 应分配更多资源给模型容量而非训练数据量。
- 尽管如此，在计算受限的外推中，DLMs 的损失曲线与 ALMs 逐渐接近（Figure 1），表明大规模下两类模型可能具有竞争力。这一结论需谨慎对待：本文最大模型为 10B 参数，与当前工业界数千亿参数的 ALM 仍有数量级差距，外推不确定性不可忽略。

### 关键超参数缩放规律的发现与意义

本文的核心方法论贡献之一是系统揭示了 DLMs 训练中两个关键超参数的幂律缩放关系：

- **最优批次大小 B\*** 随训练 token 数呈近似线性增长（指数 0.8225 ± 0.0104，Figure 3 left, Table 6），且这一关系对模型规模和噪声类型不敏感（尽管均匀噪声的斜率 0.8787 略高于掩码噪声的 0.7759）。
- **最优学习率 η\*** 随最优批次大小呈幂律增长（指数 0.34，Figure 3 right），同样对噪声类型稳健。

这两条幂律使得超参数外推成为可能：给定目标训练 token 数，可直接预测最优批次大小和学习率，无需针对每个模型规模重新进行昂贵的网格搜索。这一发现与 ALM 领域对临界批次大小的研究形成对照——本文未观察到 10⁶ tokens 以内的批次大小饱和现象，暗示 DLMs 的临界批次可能出现在更大规模。

此外，**批次大小与训练步数的双曲线 iso‑loss 关系**（Eq. 7）为 token 最优配置提供了闭式解：在固定损失下，步数 S 与批次大小 B 服从双曲约束，token 最优对 (B\*, S\*) 位于双曲线的“拐点”处。这一关系将批次大小选择从启发式规则提升为可解析优化的决策。

### 学习率退火的角色

本文有意省略了学习率退火（annealing），以简化缩放定律的估计。消融实验表明（Figure 5）：

- 学习率退火带来约 **2.45% ± 0.138%** 的恒定损失改善，且这一改善对模型规模和训练预算保持稳定，甚至在 3B/10B 模型上准确外推。
- 退火不影响最优批次大小和学习率的选择，因此省略退火不会扭曲缩放系数的估计。

这意味着本文报告的缩放定律可视为“无退火”范式下的计算最优关系；若实际训练中加入退火，损失将整体下移一个常数因子，但计算最优的模型/数据配比不变。

### 适用边界与局限

1. **数据集依赖性**：所有缩放系数基于 Nemotron‑CC 数据集（未经质量过滤）拟合。数据集组成（如领域分布、重复度）对缩放指数有系统性影响，本文结果未必直接迁移至其他语料（如代码、多语言文本）。
2. **语言与模态限制**：实验仅覆盖英语文本，未验证多语言或代码数据的缩放行为。离散扩散在结构化数据上的噪声类型偏好可能与自然语言不同。
3. **模型规模上限**：最大验证规模为 10B 参数、10²² FLOPs，与当前 ALM 的数百亿至数千亿参数规模存在差距。外推至更大规模时，缩放指数的稳定性尚未得到验证。
4. **训练策略交互**：本文采用“无退火、恒定学习率”范式以简化分析，但未探索多轮退火、课程学习、数据重复等精细化策略与缩放规律的交互效应。
5. **下游任务泛化**：虽然下游性能与 ELBO 趋势总体一致（Table 2），但并非所有任务上均匀扩散均优于掩码扩散（例如 3B 掩码模型在部分任务上略优）。任务特定的缩放行为仍需进一步研究。
6. **FLOP 估计方法的影响**：消融显示（Figure 10, Table 7），采用 Bi et al. (2024) 的 FLOP 估计（M = 6P + 12LDN）与 Hoffmann et al. (2022) 的经典估计（M = 6P）会系统性地改变拟合的缩放系数。尽管插值平滑后趋势一致，但在与 ALM 缩放定律直接对比时需注意这一方法学差异。

### 开放问题

- **临界批次大小的饱和点**：本文在 10⁶ tokens 范围内未观察到最优批次大小的饱和，DLMs 的临界批次大小是否在更大规模下出现，以及是否与噪声类型相关，仍待探索。
- **自动化超参数缩放**：最优批次大小和学习率的幂律关系为无搜索缩放（如 µTransfer）提供了理论锚点，但如何将这两条幂律嵌入自动化框架以实现“零调参”的大规模训练，尚需工程化验证。
- **混合噪声的进一步优化**：本文的混合噪声分布采用 sigmoid 单调过渡，均匀扩散在 token 受限场景下的优势能否通过更复杂的非单调调度（如在特定 SNR 区间侧重掩码、其他区间侧重均匀）进一步放大，是值得研究的方向。
- **推理效率的定量比较**：扩散模型与自回归模型在相同计算预算下的实际下游任务效率（如推理延迟、吞吐量、生成长度控制）尚未系统对比，这直接关系到 DLMs 在部署场景中的竞争力。



## 原文 PDF

![[paperPDFs/ICLR_2026/Scaling_Behavior_of_Discrete_Diffusion_Language_Models.pdf]]
