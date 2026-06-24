---
title: "GLASS Flows: Efficient Inference for Reward Alignment of Flow and Diffusion Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/GLASS_Flows_Efficient_Inference_for_Reward_Alignment_of_Flow_and_Diffusion_Models.pdf
openreview_forum_id: vH7OAPZ2dR
aliases:
- GF
- GFEIRAFDM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入可调节的相关性参数ρ和控制转移核，构建内部ODE流匹配模型（GLASS流）来高效采样转移，同时通过随机初始条件保持随机性。"
primary_logic: "通过重参数化去噪模型并利用充分统计量，将多个相关高斯测量合成一个等效测量，从而利用预训练的ODE模型模拟SDE转移，无需重新训练。"
claims:
- "GLASS流在低采样步数下相较于DDPM采样显著降低FID。"
- "GLASS流结合Feynman-Kac引导在文本到图像生成中取得了新的最佳性能。"
- "GLASS流消除了ODE与SDE之间的效率-随机性权衡，在SiT和GenEval上实现了与ODE同等性能。"
- "GenEval 上 Overall = 0.6357"
---

# GLASS Flows: Efficient Inference for Reward Alignment of Flow and Diffusion Models

> [!tip] 核心洞察
> 通过重参数化去噪模型并利用充分统计量，将多个相关高斯测量合成一个等效测量，从而利用预训练的ODE模型模拟SDE转移，无需重新训练。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | GLASS流：流动与扩散模型奖励对齐的高效推理方法 |
| 英文题名 | GLASS Flows: Efficient Inference for Reward Alignment of Flow and Diffusion Models |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=vH7OAPZ2dR) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | GLASS Flows |
| Dataset | GenEval, SiT, GenEval (with ImageReward) |

> [!tip] 效果简介
> - GenEval 上，Overall 为 0.6357，对比 0.4435，变化 +0.1922。
> - SiT 上，FID 为 2.58，对比 4.36，变化 -1.78。
> - GenEval (with ImageReward) 上，GenEval score 为 64.7，对比 63.8，变化 +0.9。

## 概述

### 问题瓶颈

扩散模型与流匹配模型在文本到图像生成中取得了卓越的样本质量，但其推理时奖励对齐（reward alignment）——即在不重新训练的前提下，将采样过程导向高奖励区域——面临一个根本性的效率-随机性权衡。现有的奖励对齐算法（如序贯蒙特卡洛 Feynman-Kac 引导和搜索方法）普遍依赖基于随机微分方程（SDE）的 DDPM 采样来模拟马尔可夫转移核 $p_{t'|t}(x_{t'}|x_t)$。这种 SDE 采样虽然提供了必要的随机性，但需要大量离散化步骤才能准确模拟转移，导致推理成本极高。相反，流匹配模型对应的常微分方程（ODE）采样虽然高效确定，却无法产生随机转移，因而不能直接用于需要探索多样性的奖励对齐任务。

### 核心方法

**GLASS 流**（GLASS Flows）通过引入一个**内部 ODE 流匹配模型**来采样转移核，从根本上化解了上述权衡。其核心洞察是：利用充分统计量将两个相关的高斯测量合成为一个等效测量，从而将预训练的流匹配模型转化为一个内部条件速度场 $u_s(\bar{x}_s | x_t, t)$。该速度场驱动一个从随机高斯噪声初始化的内部 ODE，在 $s=1$ 时产生服从目标转移核 $p_{t'|t}(\cdot|x_t)$ 的样本。方法的关键控制旋钮是可调节的**相关性参数 $\rho$**，它决定了转移核中当前状态与下一状态之间的相关程度：$\rho$ 越小，转移的随机性越强，采样多样性越高。

GLASS 流可无缝集成到任何基于 SDE 的推理时对齐算法中，无需额外训练或微调。其内部 ODE 的构造仅需预训练模型的速度场 $u_t$ 和噪声调度参数，计算开销极低。

### 主要结果

在多个基准上的实验验证了 GLASS 流的有效性：

- **后验采样效率**：在从噪声图像恢复原始图像的后验采样任务中，GLASS 流在低采样步数（$M \leq 8$）下相比 DDPM 采样显著降低了 FID（Figure 2, Figure 4），同时在价值函数 $V_t(x)$ 的估计上实现了更高的相关性（Figure 2, Figure 5）。

- **Feynman-Kac 引导**：将 GLASS 流与 FKS-SDE 结合（FKS-GLASS），在 GenEval 基准上取得了新的最佳性能。以 ImageReward 为奖励模型时，FKS-GLASS（$\rho=0.4$）的 GenEval 综合得分达到 **0.6357**，远超 FKS-SDE（DDPM）的 0.4435（Table 1, Table 3）。

- **采样质量与多样性**：在 SiT 和 FLUX 模型上，GLASS 流以 50 次神经网络评估（NFEs）实现了与 ODE 采样相当的图像质量（SiT FID: **2.58** vs. DDPM 4.36），同时保持了与 DDPM 相似的样本多样性（Table 4, Figure 6），消除了 ODE 与 SDE 之间的效率-随机性权衡。

- **奖励引导**：GLASS 流在奖励引导任务中同时提升了目标奖励分数和 GenEval 综合得分，而传统 ODE 引导则导致 GenEval 性能下降（Table 5）。

### 方法定位

GLASS 流在方法谱系中处于**高效 ODE 采样**与**随机 SDE 采样**的交汇点。它概括了 DDIM（当内部步数 $M=1$ 时退化为 DDIM），同时通过可调节的 $\rho$ 参数扩展了转移核空间。与需要重新训练或微调的奖励对齐方法不同，GLASS 流是一种纯推理时技术，可即插即用于任何预训练的流匹配或扩散模型。

## 背景与动机

### 流匹配与扩散模型的推理瓶颈

流匹配（Flow Matching）和扩散模型已成为生成式建模的核心范式，其标准推理过程可概括为：从高斯噪声 $X_0 \sim p_0$ 出发，沿学到的边际向量场 $u_t(x_t)$ 模拟常微分方程（ODE）$\frac{\mathrm{d}}{\mathrm{d}t} X_t = u_t(X_t)$，最终得到 $X_1 \sim p_{\text{data}}$。该过程是**确定性的**——给定初始噪声，ODE 采样产生唯一输出。

然而，许多关键应用要求对生成过程施加**推理时控制**，其中最具代表性的是**奖励对齐**（reward alignment）：将预训练模型的采样分布向高奖励区域倾斜，形式化为从奖励倾斜分布中采样：

$$p^{r}(z) = \frac{1}{Z^{r}} p_{\text{data}}(z) \exp(r(z))$$

其中 $r(z)$ 为奖励函数（如美学评分、图文匹配度）。实现这一目标的现有方法——包括序贯蒙特卡洛（SMC）和搜索方法——都依赖一个共同的操作：**从马尔可夫转移核 $p_{t'|t}(x_{t'}|x_t)$ 中采样**，即给定当前状态 $x_t$，生成下一时间步的状态 $x_{t'}$。

### 效率-随机性的根本权衡

这里暴露出一个根本性的瓶颈。转移核 $p_{t'|t}$ 的采样有两种选择：

- **SDE 采样（DDPM）**：通过模拟时间反转随机微分方程（SDE）实现，具有天然的随机性，能够探索不同的生成路径。但其效率极低——需要大量离散化步骤才能获得高质量样本，每一步都需要完整的神经网络评估。
- **ODE 采样（流基线）**：通过模拟确定性 ODE 实现，效率极高——只需少量步骤即可生成高质量图像。但它**无法采样随机转移**，因为 ODE 路径是确定性的，丧失了推理时控制所需的探索能力。

这一矛盾构成了现有方法的**效率-随机性权衡**：SDE 提供随机性但效率低下，ODE 提供效率但缺乏随机性。以 Feynman-Kac 引导（FKS-SDE, Singhal et al., 2025）为代表的 SMC 方法虽能有效实现奖励对齐，但受限于 DDPM 采样的高昂计算成本；而纯 ODE 方法虽快，却无法支撑需要随机转移的推理时控制算法。

### 核心动机：用 ODE 采样随机转移

本文的核心动机直指这一矛盾：**能否设计一种方法，用高效的 ODE 来采样随机马尔可夫转移，从而消除效率与随机性之间的权衡？**

具体而言，需要解决两个紧密关联的问题：
1. **如何用 ODE 高效模拟 $p_{t'|t}$ 的采样**，使其既保持 ODE 的少步数优势，又具备 SDE 的随机探索能力？
2. **如何扩展转移核的空间**，使其超越 DDPM 采样的固定相关性结构，为奖励对齐提供更灵活的探索机制？

### 关键洞察：充分统计量与去噪器重参数化

GLASS 流的解决方案源于一个理论洞察：在高斯条件概率路径 $p_t(x_t|z) = \mathcal{N}(x_t; \alpha_t z, \sigma_t^2 I_d)$ 的框架下，转移核 $p_{t'|t}$ 的采样可以分解为两个相关高斯测量的条件期望计算。通过引入**充分统计量** $S(\mathbf{x}) = \frac{\mu^T \Sigma^{-1} \mathbf{x}}{\mu^T \Sigma^{-1} \mu}$，可以将两个相关测量 $(x_t, \bar{x}_s)$ 合成为一个等效测量，从而利用预训练流匹配模型的去噪器 $D_t(x)$ 来计算条件期望，**无需任何额外训练**。

这一洞察使得在 ODE 内部构建一个“流匹配子模型”成为可能：该子模型以随机高斯噪声为初始条件（保证随机性），通过一个精心构造的 GLASS 速度场 $u_s(\bar{x}_s | x_t, t)$ 进行演化（保证效率），最终输出转移样本 $x_{t'}$。通过引入可调节的相关性参数 $\rho$，GLASS 流还超越了 DDPM 采样的固定相关性结构，为不同任务提供了灵活的探索空间。

## 核心创新

GLASS流的核心创新在于**用预训练ODE模型高效采样SDE转移核**，从而消除了现有奖励对齐方法中“效率-随机性”的根本权衡。具体而言，该方法通过三个关键机制实现了这一突破。

### 可调节的转移核：从固定SDE到参数化联合分布

传统方法在采样时间反转SDE的转移核 $p_{t'|t}(x_{t'}|x_t)$ 时，只能使用DDPM采样（Ho et al., 2020）所隐含的固定相关性结构，而ODE采样（Song et al., 2021）则完全丧失了随机性。GLASS流引入了一个**可调节的相关性参数 $\rho$**，将转移核重新定义为具有自由度的联合高斯分布：

$$X \sim p_{t,t'}(X|z) = \prod_{j=1}^{d} \mathcal{N}((X_t^j, X_{t'}^j); z^j \mu, \Sigma)$$

其中协方差矩阵 $\Sigma$ 中的相关系数 $\rho$ 可以自由设定。这一参数化具有两个关键性质：(1) 当 $\rho = \alpha_t \sigma_{t'} / (\sigma_t \alpha_{t'})$ 时，GLASS转移退化为标准DDPM转移（命题1），表明DDPM是GLASS流的一个特例；(2) 通过调节 $\rho$，可以在确定性与完全随机之间平滑插值，为不同任务选择最优的随机性水平。

### 内部ODE流匹配：用确定性模拟实现随机转移采样

GLASS流的核心技术突破在于**将随机转移采样转化为确定性ODE模拟**。该方法构造了一个“内部流匹配模型”，其速度场 $u_s(\bar{x}_s | x_t, t)$ 由预训练模型变换得到，无需任何重新训练或微调。采样过程分为两步：

1. **随机初始条件**：从高斯分布中采样内部ODE的起点 $\bar{X}_0 \sim \mathcal{N}(\bar{\gamma} x_t, \bar{\sigma}_0^2 I_d)$，这提供了转移所需的随机性。
2. **确定性演化**：沿内部ODE轨迹 $\frac{\mathrm{d}}{\mathrm{d}s} \bar{X}_s = u_s(\bar{X}_s | x_t, t)$ 从 $s=0$ 积分到 $s=1$，终点 $\bar{X}_1$ 即为转移样本。

这一设计的精妙之处在于：随机性仅由初始条件引入，而后续演化完全由高效的ODE求解器完成，从而在保持SDE转移随机性的同时，获得了ODE采样的效率优势。

### 充分统计量驱动的模型变换：零训练成本的核心

GLASS流能够直接利用预训练模型的关键，在于**通过充分统计量将两个相关高斯测量合成为一个等效测量**。给定条件点 $x_t$ 和内部状态 $\bar{x}_s$，GLASS去噪器需要计算条件期望 $D_{\mu,\Sigma}(x_t, \bar{x}_s) = \int z \, p(z|x_t, \bar{x}_s) \, \mathrm{d}z$。通过引入充分统计量：

$$S(\mathbf{x}) = \frac{\mu^T \Sigma^{-1} \mathbf{x}}{\mu^T \Sigma^{-1} \mu}$$

将向量 $(x_t, \bar{x}_s)$ 压缩为一个标量，使得双测量条件期望等价于单测量条件期望：$D_{\mu,\Sigma}(\mathbf{x}) = D_{t^*}(S(\mathbf{x}))$，其中 $D_{t^*}$ 是预训练去噪器在某个等效时间 $t^*$ 上的输出。这意味着**GLASS流的每次内部ODE步仅需一次预训练模型的前向传播**，计算成本与标准ODE采样相当。

最终，GLASS速度场被构造为三项的加权和：

$$u_s(\bar{x}_s | x_t, t) = w_1(s) \bar{x}_s + w_2(s) D_{\mu(s),\Sigma(s)}(x_t, \bar{x}_s) + w_3(s) x_t$$

其中权重 $w_1, w_2, w_3$ 由噪声调度 $\alpha_t, \sigma_t$ 及其导数解析给出（定理1）。整个算法（算法1）的计算复杂度由模拟步数 $M$ 控制，默认设置 $K=6$ 个等距转移，每个转移使用 $M=10$ 步内部ODE积分。

### 创新总结

GLASS流通过三个环环相扣的创新——可调节转移核、内部ODE流匹配、充分统计量变换——实现了对现有方法的系统性改进：用预训练ODE模型高效采样SDE转移，消除了效率与随机性之间的根本权衡。该方法可无缝集成到任何基于SDE的推理时对齐算法中（如序贯蒙特卡洛、价值函数估计、奖励引导），无需额外训练成本。

## 整体框架

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_vH7OAPZ2dR/figures/001_Figure_1.jpg]]
*Figure 1: GLASS Flows overview. Left: Sampling transition $p _ { t ^ { \prime } | t } ( x _ { t ^ { \prime } } | x _ { t }$ ) with GLASS Flows. Initial Gaussian samples $\bar { x } _ { s = 0 }$ are evolved from inner time s = 0 to s = 1 via the velocity field $u _ { s } ( \bar { x } _ { s } | x _ { t }$ , t ) that is obtained by transforming a pre-trained flow matching model. Right: Reward alignment with GLASS Flows improves text-image alignment

GLASS流（GLASS Flows）的核心目标是为预训练流匹配和扩散模型提供一种高效的转移采样方法，以替代传统基于随机微分方程（SDE）的马尔可夫转移采样。其整体框架围绕一个关键思想展开：**通过构造一个内部流匹配模型，利用确定性常微分方程（ODE）模拟随机转移，从而消除ODE的效率与SDE的随机性之间的传统权衡**。

### 框架总览

GLASS流的pipeline由以下主要阶段构成，如图1所示：

1. **输入条件**：给定当前状态 $x_t$（时间 $t$ 的噪声样本）和目标时间 $t'$，需要从转移核 $p_{t'|t}(x_{t'}|x_t)$ 中采样。
2. **内部ODE构造**：利用预训练流匹配模型的速度场 $u_t(x)$，通过去噪器重参数化和充分统计量合成，构造一个内部ODE的速度场 $u_s(\bar{x}_s | x_t, t)$。该内部ODE定义了从内部时间 $s=0$ 到 $s=1$ 的确定性演化。
3. **随机初始条件**：内部ODE的初始条件 $\bar{X}_0$ 从高斯分布中随机采样，引入转移所需的随机性。这是GLASS流实现“ODE效率 + SDE随机性”的关键机制。
4. **内部ODE积分**：通过数值积分（如欧拉方法）模拟内部ODE，生成转移样本 $\bar{X}_1 \sim p_{t'|t}(\cdot | X_t = x_t)$。
5. **下游应用**：将GLASS转移采样无缝集成到现有的推理时奖励对齐算法中，包括序贯蒙特卡洛（SMC）、价值函数估计和奖励引导。

### 核心模块与数据流

GLASS流的pipeline由以下五个关键模块组成，数据在各模块间依次流动：

| 模块 | 输入 | 输出 | 功能 |
|------|------|------|------|
| **去噪器重参数化** | 预训练速度场 $u_t$ | 去噪器 $D_t(x)$ | 将速度场转换为条件期望估计器（eq. (14)） |
| **充分统计量计算** | 两个相关测量 $(x_t, \bar{x}_s)$ | 等效测量 $S(\mathbf{x})$ | 将两个相关高斯观测汇总为单一统计量 |
| **GLASS去噪器** | $S(\mathbf{x})$、预训练去噪器 | 条件期望 $\hat{z}$ | 利用预训练模型单次前向传播计算联合后验期望（eq. (19), Proposition 2） |
| **GLASS速度场构造** | $\bar{x}_s$, $x_t$, GLASS去噪器 | 速度场 $u_s$ | 构造内部ODE的速度场，作为三者的加权和（Theorem 1, eq. (19)） |
| **内部ODE积分** | $u_s$, 随机初始条件 $\bar{X}_0$ | 转移样本 $\bar{X}_1$ | 模拟确定性ODE生成转移样本（eq. (22), Algorithm 1） |

### 关键设计选择

GLASS流框架引入了两个核心的可调节机制：

- **相关性参数 $\rho$**：控制转移核 $p_{t'|t}$ 中 $X_t$ 与 $X_{t'}$ 之间的相关性。当 $\rho = \alpha_t \sigma_{t'} / (\sigma_t \alpha_{t'})$ 时，GLASS转移退化为标准DDPM转移（Proposition 1）；当 $\rho$ 取其他值时，可灵活调节转移的随机程度。实验表明，对于FLUX模型，恒定 $\rho=0.4$ 在GenEval上性能最佳（Figure 7）。
- **转移步数 $K$**：将整个时间区间划分为 $K$ 个等距转移，每个转移内部使用 $M$ 步ODE模拟。默认设置 $K=6$，在效率与性能之间取得平衡。当 $M=1$ 时，GLASS流特例化为DDIM采样（Appendix B.2）。

### 与现有方法的对比

GLASS流通过上述框架，在以下维度上区别于基线方法：

| 维度 | ODE采样（Flow baseline） | SDE采样（DDPM） | GLASS流 |
|------|-------------------------|-----------------|---------|
| 转移采样方式 | 确定性ODE（无转移） | 随机微分方程 | 内部ODE + 随机初始条件 |
| 相关性控制 | 无 | 固定DDPM相关性 | 可调节 $\rho$ |
| 转移数量 | 1（全步） | 连续SDE | $K$ 个等距转移 |
| 效率-随机性权衡 | 高效但确定性 | 随机但低效 | 同时具备高效与随机性 |

### 应用集成

GLASS流可以无缝嵌入三类推理时奖励对齐方法，仅需将原有的SDE采样替换为GLASS转移采样：

- **序贯蒙特卡洛（SMC）**：用GLASS流演化粒子，替代FKS-SDE中的DDPM采样（Singhal et al., 2025）。
- **价值函数估计**：用GLASS流从后验 $p_{1|t}$ 采样，估计搜索方法中使用的价值函数 $V_t(x_t)$。
- **奖励引导**：在GLASS速度场上添加适当缩放的奖励梯度项，实现无需重新训练的奖励引导。

所有应用均无需额外训练，仅使用预训练模型的前向传播，且总神经网络评估次数（NFEs）与基线方法保持公平可比。

## 核心模块与公式推导

### 方法总览

GLASS流的核心思想是将扩散模型的随机转移采样转化为**内部ODE流匹配**问题：通过重参数化预训练的去噪模型，并利用充分统计量将两个相关的高斯测量合成为一个等效测量，从而用确定性ODE模拟SDE转移。整个过程无需重新训练或微调，仅需调节一个相关性参数 $\rho$ 来控制转移的随机程度。

### 关键公式与变量定义

**转移核定义**（时间 $t$ 到 $t'$ 的条件分布）：

$$p_{t'|t}(x_{t'}|x_t) = \mathbb{P}[X_{t'}=x_{t'} \mid X_t=x_t], \quad 0 \leq t < t' \leq 1$$

这是所有奖励对齐算法（序贯蒙特卡洛、搜索方法）中粒子演化或价值函数估计所依赖的核心概率对象。

**高斯条件概率路径**（从数据 $z$ 到噪声的插值）：

$$x_t = \alpha_t z + \sigma_t \epsilon, \quad \epsilon \sim \mathcal{N}(0, I_d) \quad \Leftrightarrow \quad p_t(x_t \mid z) = \mathcal{N}(x_t; \alpha_t z, \sigma_t^2 I_d)$$

其中 $\alpha_t$ 和 $\sigma_t$ 定义了信号与噪声的调度，是流匹配与扩散模型的共同基础。

**边际向量场**（流匹配模型学习的核心对象）：

$$u_t(x_t) = \int u_t(x_t \mid z) \, p_{1|t}(z \mid x_t) \, \mathrm{d}z$$

该向量场通过ODE $\mathrm{d}X_t/\mathrm{d}t = u_t(X_t)$ 驱动采样，从初始噪声 $X_0 \sim p_0$ 演化至数据分布 $X_1 \sim p_{\text{data}}$。

**去噪器重参数化**（从速度场到去噪器的等变换）：

$$D_t(x) = \int z \, p_{1|t}(z \mid x) \, \mathrm{d}z = \frac{1}{\dot{\alpha}_t \sigma_t - \alpha_t \dot{\sigma}_t} (\sigma_t u_t(x_t) - \dot{\sigma}_t x_t)$$

该公式是GLASS流构建的基石——它允许从预训练的速度场 $u_t$ 直接获得去噪器 $D_t$，无需额外训练。

### 核心模块

**模块1：充分统计量计算**

给定两个相关的含噪观测 $x_t$ 和 $\bar{x}_s$（来自GLASS转移的联合分布），其联合分布为高斯，均值与协方差由 $\alpha_t, \sigma_t$ 及可调相关性参数 $\rho$ 决定。充分统计量将这两个测量汇总为一个等效的标量测量：

$$S(\mathbf{x}) = \frac{\mu^T \Sigma^{-1} \mathbf{x}}{\mu^T \Sigma^{-1} \mu}$$

其中 $\mathbf{x} = (x_t, \bar{x}_s)$，$\mu$ 和 $\Sigma$ 为联合分布的均值向量与协方差矩阵。这一汇总操作使得原本需要同时条件于两个测量的问题退化为条件于单个等效测量的问题。

**模块2：GLASS去噪器**

基于充分统计量，GLASS去噪器定义为给定两个测量的后验期望：

$$D_{\mu,\Sigma}(\mathbf{x}) = \int z \, p(Z=z \mid \mathbf{X}=\mathbf{x}) \, \mathrm{d}z$$

关键性质：该去噪器可通过**单次**预训练去噪器 $D_t$ 的函数评估获得（见Algorithm 1），无需重新训练。

**模块3：GLASS速度场**

内部ODE的速度场 $u_s(\bar{x}_s \mid x_t, t)$ 构造为当前状态 $\bar{x}_s$、GLASS去噪器输出、以及条件点 $x_t$ 的加权和：

$$u_s(\bar{x}_s \mid x_t, t) = w_1(s) \bar{x}_s + w_2(s) D_{\mu(s),\Sigma(s)}(x_t, \bar{x}_s) + w_3(s) x_t$$

其中权重 $w_1, w_2, w_3$ 由调度参数 $\bar{\alpha}_s, \bar{\sigma}_s$ 及其导数解析给出，$\bar{\alpha}_s, \bar{\sigma}_s$ 定义了内部时间 $s \in [0,1]$ 上的等效噪声调度。

**模块4：内部ODE积分**

转移采样通过模拟以下ODE完成（Algorithm 1）：

$$\bar{X}_0 \sim \mathcal{N}(\bar{\gamma} x_t, \bar{\sigma}_0^2 I_d), \quad \frac{\mathrm{d}}{\mathrm{d}s} \bar{X}_s = u_s(\bar{X}_s \mid x_t, t) \quad \Rightarrow \bar{X}_1 \sim p_{t'|t}(\cdot \mid X_t = x_t)$$

随机性来自初始条件 $\bar{X}_0$ 的高斯采样，而后续演化是确定性的ODE积分。$\bar{\gamma}$ 由相关性参数 $\rho$ 决定，控制转移的随机程度。

### 可调相关性参数 $\rho$

GLASS转移的核心自由度是相关性参数 $\rho$，它控制 $X_t$ 与 $X_{t'}$ 之间的统计依赖强度。DDPM采样是GLASS流的一个特例（Proposition 1）：当 $\rho = \alpha_t \sigma_{t'} / (\sigma_t \alpha_{t'})$ 时，GLASS转移退化为标准DDPM转移核。调节 $\rho$ 可以打破这一固定关系，在保持边际分布不变的前提下改变转移的随机性-确定性权衡。

### 与奖励对齐的接口

GLASS流通过三个接口服务于推理时奖励对齐：
- **序贯蒙特卡洛**：用GLASS流替代DDPM采样作为粒子提议分布 $p_{t'|t}$
- **价值函数估计**：用GLASS流从后验 $p_{1|t}$ 采样以估计 $V_t(x_t) = \log \mathbb{E}_{z \sim p_{1|t}(\cdot|x_t)}[\exp(r(z))]$
- **奖励引导**：在GLASS速度场上叠加奖励函数的梯度项，实现引导采样

## 实验与分析

### 核心性能验证

GLASS流在三个关键维度上展现了相对于现有方法的显著优势：采样效率、奖励对齐性能和通用生成质量。

**低步数下的采样效率优势**。在后验采样实验中，GLASS流在低模拟步数（M）下相比DDPM采样（SDE）显著降低了FID（Figure 2 Middle，Figure 4）。当时间步t较小时（如t=0.05、0.15），后验分布不确定性大，DDPM采样需要大量步数才能获得合理重建，而GLASS流在M=2或M=4时即可实现低FID（Figure 11，Figure 12）。当t接近1时（如t=0.7），后验不确定性低，两种方法均表现良好，但GLASS流在极低步数下仍保持优势（Figure 13）。这一结果直接验证了核心主张：GLASS流消除了ODE与SDE之间的效率-随机性权衡。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_vH7OAPZ2dR/figures/012_Figure_4.jpg]]
*Figure 4: Detailed results for fig. 2 (Middle). Comparing the performance of sampling the posterior p _ { 1 | t } via GLASS Flows (Ours) and SDE (DDPM) sampling. Ablate over different times t and sampling steps. GLASS Flows achieve significantly lower FID for lower number of sampling steps than DDPM sampling*

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_vH7OAPZ2dR/figures/024_Figure_11.jpg]]
*Figure 11: Posterior recovery for t = 0 . 0 5 for various number of simulation steps M . As one can see, GLASS Flows achieve significantly better performance for low M than the SDE/DDPM sampling. 32*

**价值函数估计的准确性**。在价值函数$V_t(x)$估计任务中，GLASS流在低步数下与真实值（200个蒙特卡洛样本，M=200）的相关性显著高于DDPM采样（Figure 2 Right，Figure 5）。这表明GLASS流生成的转移样本更准确地反映了后验分布的结构，为后续的搜索类奖励对齐方法提供了更可靠的价值估计基础。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_vH7OAPZ2dR/figures/013_Figure_5.jpg]]
*Figure 5: Detailed results for fig. 2 (Right). Comparing the performance of estimating the value function V _ { t } ( x ) via sampling the posterior p _ { 1 | t } via GLASS Flows (Ours) and SDE (DDPM) sampling via correlation. Experiment performed for different times t and sampling steps M . GLASS Flows achieve significantly higher correlation for lower number of steps than DDPM sampling. Ground truth is measured via 200 samples with 200 simulation steps of ODE/SDE*

**Feynman-Kac引导的序贯蒙特卡洛性能**。Table 1展示了GLASS流结合Feynman-Kac引导（FKS）在多个奖励模型上的表现。FKS-GLASS（ρ=0.4）在CLIP、Pick、HPSv2和ImageReward四个奖励模型上均取得了最高或次高的奖励分数，同时在GenEval benchmark上也获得最优综合得分。值得注意的是，所有方法使用相同粒子数N=8和400次神经网络评估（NFEs），确保了公平比较。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_vH7OAPZ2dR/figures/008_Table_1.jpg]]
*Table 1: Sequential Monte Carlo via Feynman-Kac steering (FKS). Every reward model defines a new experiment whose samples we evaluate on the same reward model and the GenEval benchmark. We set N = 8 (number of particles). NFEs=400 for all rows except flow baseline (50 NFEs). BoN: Best-of-N. FKS: Feynman-Kac Steering*

### 通用生成质量评估

在无奖励引导的标准采样场景下，GLASS流同样展现了优越的生成质量。

**SiT和FLUX模型上的采样性能**。Table 4报告了在50 NFEs和5个转移（每个转移10个模拟步）设定下的评估结果。GLASS流在SiT模型上取得FID=2.58，显著优于DDPM采样的4.36；在FLUX模型上，GLASS流在GenEval Overall指标上达到0.6357，远超DDPM采样的0.4435（Table 3）。Figure 3的定性对比显示，DDPM采样产生的图像更模糊、质量更低，而GLASS流生成的图像细节更丰富、文本对齐更好。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_vH7OAPZ2dR/figures/014_Table_3.jpg]]
*Table 3: GenEval results*

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_vH7OAPZ2dR/figures/015_Table_4.jpg]]
*Table 4: Sampling evaluation for SiT and FLux models using various sampling algorithms introduced in this work. We use 50 total neural network evaluations for all experiments and 5 transitions (i.e. 10 simulation steps for each transition)*

**与ODE基线的对比**。GLASS流在GenEval上实现了与ODE采样同等甚至更优的性能（Table 3），同时保持了SDE采样的随机性。这证实了GLASS流成功打破了ODE（确定性、高效但缺乏随机性）与SDE（随机但低效）之间的传统权衡。

### 奖励引导实验

Table 5展示了奖励引导的实验结果。GLASS引导在四个奖励模型（CLIP、Pick、HPSv2、ImageReward）上均同时提升了GenEval分数和目标奖励值，而传统的流引导（flow guidance）在提升奖励的同时导致GenEval性能下降。Figure 8进一步揭示了引导强度变化下的性能权衡：在相同ImageReward值下，GLASS流始终获得更高的GenEval Overall分数，表明GLASS引导在奖励对齐与通用生成质量之间实现了更好的平衡。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_vH7OAPZ2dR/figures/019_Table_5.jpg]]
*Table 5: Reward guidance results on GenEval prompts. N = 50 simulation steps. The best value in each column is bolded, and the second best is underlined. Reward guidance with GLASS Flows improves both GenEval score and the reward of interest, while flow guidance leads to decreased performance on GenEval*

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_vH7OAPZ2dR/figures/020_Figure_8.jpg]]
*Figure 8: Varying reward guidance strength across different methods on GenEval benchmark with reward ImageReward. By increasing the guidance strength, we can increase ImageReward. GLASS Flows has higher performance on GenEval performance for the same ImageReward value. High guidance strengths lead to image artifacts that are not properly captured by our metrics*

### 消融研究

**相关性参数ρ的影响**。Figure 7展示了相关性调度ρ的消融实验。对于FLUX模型，恒定ρ=0.4在所有过渡中取得了最佳GenEval性能。当时变相关性调度采用$\rho = (\alpha_t \sigma_{t'} / (\sigma_t \alpha_{t'}))^\kappa$形式时，κ=1对应DDPM调度（Proposition 1），但κ≈2时GenEval分数和多样性同时达到峰值，表明DDPM的默认相关性并非最优，GLASS流的可调节ρ参数提供了额外的性能空间。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_vH7OAPZ2dR/figures/018_Figure_7.jpg]]
*Figure 7: Ablation experiment of correlation schedule $\rho$ . Left: Constant correlation $\rho$ across all transitions. Right: Time-dependent correlation schedule given by $\begin{array} { r } { \rho = \Big ( \frac { \alpha _ { t } \sigma _ { t ^ { \prime } } } { \sigma _ { t } \alpha _ { t ^ { \prime } } } \Big ) ^ { \kappa } } \end{array}$ - note that $\kappa$ = 1 corresponds to the DDPM schedule (see proposition 1)

**采样步数M的消融**。Figure 4和Figure 5的系统消融表明，GLASS流在M=1时特例化为DDIM采样（Appendix B.2），验证了GLASS流对DDIM的概括性。随着M增加，两种方法的性能差距缩小，但GLASS流在M≤8的范围内始终保持显著优势。

**样本多样性评估**。Figure 6显示DDPM、ODE和GLASS三种采样方案在多样性指标上表现相似，符合理论预期——GLASS流通过随机初始条件保持了SDE的随机性，同时通过确定性内部ODE实现了高效采样。

### 失败模式与局限

尽管GLASS流展现了全面的性能优势，仍需注意以下局限：

1. **相关性参数ρ的手动选择**：最优ρ值依赖于具体模型和任务（Figure 7），目前缺乏自动选取机制，这增加了实际部署的调参成本。

2. **奖励引导的显存约束**：当奖励引导需要反向传播计算梯度时（如Table 2中的梯度引导实验），大分辨率图像生成仍面临显存限制。

3. **离散化误差**：理论推导假设无离散化误差和完美训练，实际应用中低步数极端情况下离散化误差可能影响性能，尽管GLASS流对此表现出较强的鲁棒性。

4. **任务范围验证有限**：当前实验仅限于文本到图像生成任务，在视频生成、分子设计等其他模态上的适用性有待验证。

### 补充图表

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_vH7OAPZ2dR/figures/009_Table_2.jpg]]
*Table 2: Improving GLASS-FKS using gradient guidance. ImageReward (IR) and GenEval results. Note: benchmarks are slightly different to table 1 as image resolution was decreased*

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_vH7OAPZ2dR/figures/022_Figure_9.jpg]]
*Figure 9: Inference-time reward alignment results on PartiPrompts benchmark. For each reward model (Clip, Pick, HPSv2, ImageReward), we run reward alignment with difference methods and evaluate across all reward models (i.e. this gives us 16 = 4 × 4 values). Left: We take the 16 values, rank the methods, and take the average rank. Right: We take the average normalized reward value (normalized via min and max observed)*

## 方法谱系与知识库定位

### 1. 与基线方法的谱系关系

GLASS流的核心贡献在于**重新定义了扩散/流模型的转移采样范式**，其方法谱系可从三个维度定位。

**采样效率维度：ODE vs SDE 的折中解。** 传统的**ODE采样**（Song et al., 2021）以确定性轨迹生成样本，效率高但缺乏随机性，无法直接用于需要随机转移的奖励对齐算法。**DDPM采样**（Ho et al., 2020）基于时间反转SDE提供了随机性，但马尔可夫转移的每一步都需要完整的SDE模拟，计算开销大。GLASS流通过构建内部ODE流匹配模型，在保持随机性（通过随机初始条件）的同时实现了高效的ODE积分，消除了这一效率-随机性权衡。当内部模拟步数M=1时，GLASS流特例化为DDIM采样（见消融实验），表明其概括了确定性采样的极限情况。

**奖励对齐维度：对FKS-SDE的继承与超越。** 在推理时奖励对齐方法中，**FKS-SDE**（Singhal et al., 2025）使用DDPM采样作为序贯蒙特卡洛的提议分布，是此前最先进的SMC方法。GLASS流的核心改进在于将提议分布中的DDPM采样替换为GLASS转移，并引入可调节的相关性参数ρ来扩展转移核空间。实验表明（Table 1），FKS-GLASS（ρ=0.4）在CLIP、PickScore、HPSv2、ImageReward四个奖励模型上均超越了FKS-SDE，并在GenEval基准上取得了新的最佳性能（0.6357 vs 0.4435，+0.1922）。这一提升的因果机制在于：GLASS流在低采样步数下对后验分布$p_{1|t}$的估计具有显著更高的相关性（Figure 2 Right），从而为SMC提供了更准确的粒子演化。

**搜索方法维度：价值函数估计的加速器。** 基于搜索的奖励对齐方法（如Best-of-N）依赖价值函数$V_t(x_t) = \log \mathbb{E}_{z \sim p_{1|t}(\cdot|x_t)}[\exp(r(z))]$来评估节点。传统方法使用DDPM采样估计该期望，在低步数下估计精度差。GLASS流通过高效的内部ODE模拟，在相同或更少的神经网络评估次数（NFEs）下提供了更准确的价值函数估计（Figure 5），可直接嵌入现有搜索框架。

### 2. 方法适用的技术边界

**适用条件。** GLASS流适用于任何具有预训练速度场$u_t(x)$的流匹配或扩散模型，无需重新训练或微调。其核心假设是模型遵循高斯条件概率路径$x_t = \alpha_t z + \sigma_t \epsilon$，这涵盖了当前主流的扩散模型（DDPM、DDIM）和流匹配模型（SiT、FLUX）。方法对模型架构无特殊要求，可无缝集成分类器自由引导（CFG），只需将CFG向量场视为真实速度场即可。

**不适用场景。** 当预训练模型不提供速度场参数化，或速度场无法通过公式$D_t(x) = \frac{1}{\dot{\alpha}_t \sigma_t - \alpha_t \dot{\sigma}_t} (\sigma_t u_t(x_t) - \dot{\sigma}_t x_t)$转换为去噪器时，GLASS流无法直接应用。此外，方法假设无离散化误差和完美训练，在极端低步数（如M=1或2）的离散化场景下，理论保证可能减弱。

### 3. 局限性与开放问题

**已识别的局限性。** （1）相关性参数ρ需要手动选择，最优值依赖于模型和任务：FLUX模型上恒定ρ=0.4表现最佳（Figure 7），但尚无自动选取机制。（2）奖励引导方法涉及梯度反向传播时面临显存瓶颈，限制了大分辨率图像的直接应用。（3）当前仅在文本到图像生成任务上验证，在其他模态（视频生成、分子设计）上的适用性未知。（4）理论基础假设完美训练和零离散化误差，实际中离散化误差可能影响性能，尤其在极端低步数下。

**开放问题。** （1）能否自动学习或动态调整GLASS转移的相关性参数ρ，使其适应不同任务和数据分布？（2）GLASS流能否应用于其他依赖SDE采样的下游任务，如奖励微调（reward fine-tuning）或图像编辑？（3）在视频生成、分子构象采样等更复杂的数据类型上，GLASS流的有效性如何？（4）能否将GLASS流与更复杂的搜索方法（如树搜索、蒙特卡洛树搜索）深度结合，形成端到端可优化的推理时对齐方案？（5）GLASS流的充分统计量构造依赖于高斯假设，对于非高斯条件路径的模型，如何扩展该方法？

## 原文 PDF

![[paperPDFs/ICLR_2026/GLASS_Flows_Efficient_Inference_for_Reward_Alignment_of_Flow_and_Diffusion_Models.pdf]]
