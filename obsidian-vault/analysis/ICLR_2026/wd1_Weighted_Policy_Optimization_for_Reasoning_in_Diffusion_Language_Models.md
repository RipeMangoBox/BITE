---
title: "wd1: Weighted Policy Optimization for Reasoning in Diffusion Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/wd1_Weighted_Policy_Optimization_for_Reasoning_in_Diffusion_Language_Models.pdf
openreview_forum_id: L2rfd2Czbj
aliases:
- WW
- wd1
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "提出无比率（ratio-free）的加权对数似然策略优化目标，完全摒弃对旧策略和参考策略似然的估计，仅依赖单一当前策略似然近似，并引入负样本惩罚项，从根本上消除了比率估计的误差。"
primary_logic: "将加权对数似然RL目标等价解释为优势引导的能量引导离散扩散训练加负样本遗忘（数据反学习），从而在理论上保证模型学习到高优势生成分布，同时实现高效和稳定的训练。"
claims:
- "wd1在Sudoku上准确率达76.4%，超过d1的17.6%达58.8个百分点，无需SFT。"
- "wd1++在MATH500和GSM8K上分别达到44.2%和84.5%，仅用20步RL且rollout减少10倍，超越所有并发方法。"
- "wd1每步训练成本（81.16秒）低于d1（103.5秒），并完全消除了SFT阶段，FLOPs降低11%。"
- "移除负样本惩罚（w−）使GSM8K性能从80.8%骤降至65.7%，证实负样本处理是关键设计。"
---

# wd1: Weighted Policy Optimization for Reasoning in Diffusion Language Models

> [!tip] 核心洞察
> 将加权对数似然RL目标等价解释为优势引导的能量引导离散扩散训练加负样本遗忘（数据反学习），从而在理论上保证模型学习到高优势生成分布，同时实现高效和稳定的训练。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | wd1：面向扩散语言模型推理的加权策略优化 |
| 英文题名 | wd1: Weighted Policy Optimization for Reasoning in Diffusion Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=L2rfd2Czbj); [GitHub](https://github.com/xiaohangt/wd1) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | wd1（及扩展wd1++） |
| Dataset | Sudoku (256 tokens), Countdown (256 tokens), GSM8K (wd1++ full), MATH500 (wd1++ full) |

> [!tip] 效果简介
> - Sudoku (256 tokens) 上，测试准确率 (%) 为 76.4，对比 17.6 (d1)，变化 +58.8。
> - Countdown (256 tokens) 上，测试准确率 (%) 为 51.2，对比 25.8 (d1)，变化 +25.4。
> - GSM8K (wd1++ full) 上，测试准确率 (%) 为 84.5，对比 83.4 (MDPO full)，变化 +1.1。

## 概述

扩散语言模型（dLLM）在推理任务中展现出潜力，但其强化学习（RL）微调面临一个根本性瓶颈：**似然函数不可解**。与自回归模型不同，dLLM 无法直接计算序列的精确对数似然，迫使现有方法（如 d1）在策略优化中依赖近似似然来估计策略比率（policy ratio）。然而，这种比率估计存在**高方差**问题，且近似误差在重要性采样过程中被**指数级放大**，严重损害训练效率和稳定性（见 Figure 1）。

针对这一瓶颈，本文提出 **wd1**（Weighted Policy Optimization for Diffusion Language Models），核心思想是**完全摒弃策略比率估计**，将 RL 目标重构为无比率（ratio-free）的加权对数似然（WLL）优化。具体而言，wd1 仅需对当前策略似然进行单次近似，权重由组相对优势（group-relative advantage）决定——正优势样本被增强，负优势样本被主动惩罚（即负样本遗忘）。作者从理论上证明，该目标等价于**优势引导的能量引导离散扩散训练**，从而保证模型收敛到高优势生成分布。

在方法论定位上，wd1 直接解决了 d1（Zhao et al., 2025）等扩散 GRPO 方法的根本缺陷：后者依赖三次似然估计（当前、旧、参考策略）来计算比率并施加裁剪约束，而 wd1 将计算复杂度降至**单次似然估计**，且无需 SFT 预热阶段。

实验证据充分支撑了上述主张：

- **Sudoku 任务**：wd1 达到 76.4% 准确率，较 d1 的 17.6% 提升 **+58.8 个百分点**，且无需 SFT（Table 1）。
- **数学推理**：扩展版本 wd1++ 在 MATH500 和 GSM8K 上分别达到 44.2% 和 84.5%，仅用 **20 步 RL 训练**且 rollout 数量减少 10 倍，超越所有并发方法（Table 3）。
- **训练效率**：wd1 每步训练成本（81.16 秒）低于 d1（103.5 秒），FLOPs 降低 11%，并完全消除了 SFT 阶段（Table 2）。
- **消融实验**：移除负样本惩罚（$w^-$）使 GSM8K 性能从 80.8% 骤降至 65.7%，证实负样本处理是方法的关键设计（Table 4）。

wd1 的局限性在于：当采样组内所有样本获得相同奖励时，正负权重相等，训练可能停滞；当前框架仅适用于文本推理，扩展到多模态场景仍需探索；所用似然近似虽然高效，但引入了偏差，需在高精度场景下权衡。

## 背景与动机

### 扩散语言模型的推理困境

扩散语言模型（dLLM）作为一种新兴的生成范式，通过迭代去噪过程生成文本，在数学推理、规划等任务中展现出潜力。然而，将强化学习（RL）应用于dLLM微调面临一个根本性瓶颈：**似然函数不可解**。

具体而言，掩码离散扩散模型的似然本质上是一个高维积分，无法直接计算：

$$p_\theta(\boldsymbol{x}_0) = \int p_\theta(\boldsymbol{x}_{0:T}) \, d\boldsymbol{x}_{1:T}$$

这迫使现有方法依赖近似。以首个专为dLLM设计的RL方法**d1**（Zhao et al., 2025）为例，其采用基于ELBO的似然近似来计算策略比率（policy ratio），用于GRPO式的重要性采样。但这一近似引入了两个严重问题：

- **高方差**：ELBO近似本身具有较大方差，导致策略比率估计不稳定（见Figure 1）。
- **指数级误差放大**：在策略优化过程中，当前策略与旧策略的差异通过比率相乘累积，近似误差被指数级放大，严重损害训练效率和稳定性。

Figure 1直观展示了这一问题：在GSM8K上经过一次策略更新后，d1使用ELBO近似计算的策略比率值出现剧烈波动，且存在系统性偏差，使得信赖域约束形同虚设。

### 现有方法的缺口

当前面向dLLM的RL微调方法存在以下结构性缺陷：

1. **对策略比率的依赖**：无论是d1还是并发的diffu-GRPO，其目标函数都包含形如 $\frac{\pi_\theta(o|q)}{\pi_{\text{old}}(o|q)}$ 的比率项，需要同时估计当前策略、旧策略和参考策略的似然。这不仅增加了计算开销（每次更新需多次前向传播），更关键的是，**比率计算将近似误差从似然估计传播到梯度更新中，造成训练信号失真**。

2. **负样本处理缺失**：现有方法对低优势样本仅给予较小权重或直接截断，缺乏主动抑制机制。这导致模型可能保留不良生成模式，降低采样效率。

3. **SFT预热需求**：d1等方法需要先进行监督微调（SFT）热身，增加了训练流程的复杂度和总计算成本。

### 本文动机

针对上述瓶颈，本文提出一个核心问题：**能否设计一种完全不依赖策略比率估计的RL目标，从根本上消除近似误差的放大效应？**

直觉上，如果可以直接对当前策略的似然进行加权优化，而无需与旧策略对比，就能绕过比率估计的难题。这要求将RL目标重新表述为“优势引导的加权对数似然”，其中权重仅由优势函数决定，不涉及任何策略比率。

进一步地，如果能将负样本的惩罚自然地融入同一框架，形成“正样本增强+负样本遗忘”的统一目标，就能在保证训练稳定性的同时提升生成质量。这正是**wd1**方法的核心动机。

## 核心创新

### 瓶颈定位：扩散策略优化的比率估计困境

扩散语言模型（dLLM）的强化学习微调面临一个根本性障碍：**似然函数不可解**。与自回归模型不同，掩码离散扩散模型的序列生成概率 $p_\theta(o|q)$ 缺乏闭式表达，迫使策略优化方法依赖近似估计。当前主流方法（如 d1 中的扩散 GRPO）采用以下流程：

1. 使用 ELBO 或高效近似（d1 近似）估计当前策略 $\pi_\theta$ 和旧策略 $\pi_{\text{old}}$ 的逐 token 对数似然；
2. 计算策略比率 $r_i^k(\theta) \approx \pi_\theta(o_i^k) / \pi_{\text{old}}(o_i^k)$ 进行重要性采样；
3. 对比率施加裁剪（clipping）以控制更新幅度。

这一范式存在两个致命缺陷：

- **高方差**：ELBO 近似的方差在策略更新后急剧放大。Figure 1（见原文）显示，在 GSM8K 上经过一次策略更新后，ELBO 估计的策略比率在 $[1-\epsilon, 1+\epsilon]$（$\epsilon=0.5$）区间内剧烈波动，而 d1 近似则引入系统性偏差，使比率显著偏离 ELBO 真值。
- **误差指数放大**：比率计算将两个近似误差相乘并指数化，导致训练信号严重失真，损害收敛效率和稳定性。

### 核心机制：无比率的加权对数似然优化

wd1 的根本创新在于**完全摒弃策略比率**，将 RL 目标重构为纯粹的加权对数似然最小化。其推导路径如下：

**Step 1：反向 KL 约束优化**。从带反向 KL 惩罚和参考策略正则化的策略优化目标出发：

$$\max_\theta \mathbb{E}_{q, o\sim\pi_\theta}\left[A^{\pi_{\text{old}}}(q,o) - \lambda D_{\text{KL}}(\pi_\theta\|\pi_{\text{old}}) - \beta D_{\text{KL}}(\pi_\theta\|\pi_{\text{ref}})\right]$$

该问题的解析最优策略具有封闭形式：

$$\pi^*(\cdot|q) \propto \pi_{\text{old}}(\cdot|q)^{\lambda/(\lambda+\beta)} \cdot \pi_{\text{ref}}(\cdot|q)^{\beta/(\lambda+\beta)} \cdot \exp\left(\frac{A^{\pi_{\text{old}}}(q,\cdot)}{\lambda+\beta}\right)$$

**Step 2：投影为加权对数似然**。将当前策略 $\pi_\theta$ 向最优策略 $\pi^*$ 投影，等价于在旧策略与参考策略的几何混合分布 $\pi_{\text{old}}^{\text{ref}}$ 下，最小化以优势为权重的负对数似然：

$$\mathcal{L}_{\text{WLL}}(\theta) = \mathbb{E}_{o \sim \pi_{\text{old}}^{\text{ref}}(\cdot|q)}\left[-\exp(\psi A^{\pi_{\text{old}}}(q,o)) \cdot \log \pi_\theta(o|q)\right]$$

**关键性质**：该目标仅需估计**当前策略** $\pi_\theta$ 的似然，完全消除了对旧策略和参考策略似然的依赖，从根本上规避了比率估计的误差放大问题。

**Step 3：负样本惩罚（wd1 完整目标）**。WLL 仅增强高优势样本，对低优势样本仅分配趋近于零的权重，造成信息浪费。wd1 引入对称的负权重项，主动压制低优势样本的生成概率：

$$\mathcal{L}_{wd1}(\theta) = \mathbb{E}_{q, \{o_i\}\sim\pi_{\text{old}}^{\text{ref}}}\left[\frac{1}{G}\sum_{i=1}^{G}\big(-w^+(q,o_i) + w^-(q,o_i)\big) \cdot \log \pi_\theta(o_i|q)\right]$$

其中权重基于组相对优势 $\hat{A}_i = R(q, o_i) - \text{mean}(R(q, o_{1:G}))$ 经 softmax 归一化：

$$w^+(q, o_i) = \frac{\exp(\psi \hat{A}_i)}{\sum_{j=1}^{G}\exp(\psi \hat{A}_j)}, \quad w^-(q, o_i) = \frac{\exp(-\psi \hat{A}_i)}{\sum_{j=1}^{G}\exp(-\psi \hat{A}_j)}$$

$w^+$ 增大高优势样本的似然（正向强化），$w^-$ 减小低优势样本的似然（负向遗忘），二者通过 $(-w^+ + w^-)$ 的组合实现平衡的梯度信号。

### 理论等价性：能量引导扩散与数据反学习

wd1 不仅是一个工程优化，更具有深刻的理论解释（Section 4）：

- **WLL 等价于能量引导扩散训练**：优势加权的对数似然目标在数学上等价于训练一个以优势函数 $A(x_0)$ 为能量函数的引导扩散模型，即 $p_{0|t}^*(x_0|x_t) \propto p_{0|t}'(x_0|x_t) \cdot \exp(A(x_0))$。这保证了模型学习到的分布向高优势区域偏移。
- **负样本惩罚等价于数据反学习**：$w^-$ 项可解释为对低优势样本执行 ELBO 最小化的数据反学习（unlearning），主动遗忘不良生成模式。

### 与 baseline 的关键差异总结

| 创新维度 | d1（baseline） | wd1（本文） |
|---------|---------------|-----------|
| **策略优化目标** | 依赖策略比率的 GRPO，需估计 $\pi_\theta$、$\pi_{\text{old}}$、$\pi_{\text{ref}}$ 三个策略的似然 | 无比率的加权对数似然，仅需 $\pi_\theta$ 单一似然近似 |
| **负样本处理** | 无显式惩罚，低优势样本权重趋于零但未被压制 | 引入 $w^-$ 主动最小化低优势样本似然，实现负样本遗忘 |
| **计算复杂度** | 每步 RL 需 3 次似然估计（$\mu+2$ 次前向传播） | 每步 RL 仅需 1 次似然估计（$\mu$ 次前向传播） |
| **SFT 预热** | 必需 SFT 阶段热身 | 无需 SFT，可直接从 base 模型开始 RL 微调 |

### 消融验证的关键发现

- **负样本惩罚的决定性作用**：移除 $w^-$（仅保留 $w^+$ 的 WLL）使 GSM8K 256 token 性能从 80.8% 骤降至 65.7%（Table 4），证实负样本处理是 wd1 性能增益的核心来源。
- **SFT 的负面效应**：加入 SFT 预热对 Sudoku 和 GSM8K 无益，甚至损害 Countdown 性能（51.2% → 43.4%），表明 wd1 的优化机制与 SFT 存在冲突，直接 RL 微调更为有效。
- **权重平衡的敏感性**：正负权重的等比例混合（$\lambda=0.5$）获得最高训练奖励，偏向正样本（$\lambda=0.8$）或负样本（$\lambda=0.0$）均导致奖励下降（Figure 2, Table 9）。温度系数 $\psi$ 过大（如 10）会导致极端权重分配，损害性能（Figure 4 Left）。

## 整体框架

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_L2rfd2Czbj/figures/001_Figure_1.jpg]]
*Figure 1: Example policy ratio value $r _ { i } ^ { k }$ computed using ELBO and approximated likelihood in d1 on GSM8K after a policy update. Ratio’s unclipped interval is [ 1 - $\epsilon$ , 1 + $\epsilon$ ] , where $\epsilon$ = 0 . 5 ELBO-based likelihood approximation yields high-variance ratio estimates; d1 induces a biased ratio that can deviate substantially from ELBO. Both methods suffer from efficiently and accurately compute ratios

wd1 的整体训练流程围绕**无比率（ratio‑free）加权对数似然优化**展开，从根本上规避了扩散语言模型（dLLM）中因似然函数不可解而导致的策略比率估计高方差问题。其核心思路是：将强化学习的目标重新构造为仅依赖当前策略似然近似的加权损失，从而在保持理论等价性的同时大幅降低计算开销和估计误差。

### 模块关系与数据流

wd1 的训练循环由五个紧密耦合的模块构成，数据流如下：

1. **几何混合策略采样**  
   从旧策略 $\pi_{\mathrm{old}}$ 与参考策略 $\pi_{\mathrm{ref}}$ 的几何混合分布中，为每个问题 $q$ 采样一组 $G$ 个完成序列 $\{o_i\}_{i=1}^G$。该混合分布起到平滑探索的作用，避免策略在早期训练中过度偏离。

2. **组相对优势计算**  
   对每个采样组，利用奖励函数 $R(q, o_i)$ 计算组内相对优势：
   $$\hat{A}_i = R(q, o_i) - \mathrm{mean}\big(R(q, o_{1:G})\big)$$
   这种组归一化方式替代了需要价值函数估计的真实优势，是 GRPO 框架的标准做法。

3. **正负权重计算**  
   基于相对优势，计算归一化的正权重 $w^+$ 和负权重 $w^-$：
   $$w^{+}(q, o_i) = \frac{\exp(\psi \hat{A}_i)}{\sum_{j=1}^{G} \exp(\psi \hat{A}_j)}, \quad w^{-}(q, o_i) = \frac{\exp(-\psi \hat{A}_i)}{\sum_{j=1}^{G} \exp(-\psi \hat{A}_j)}$$
   其中 $\psi$ 为温度系数，控制权重分布的尖锐程度。正权重提升高优势样本的似然，负权重则主动惩罚低优势样本——这是 wd1 区别于仅使用正权重的 WLL 损失的关键设计。

4. **似然近似**  
   采用与 d1 相同的高效近似方法，估计当前策略 $\pi_\theta$ 对每个完成序列的逐 token 对数似然。该近似避免了扩散模型精确似然估计的高昂成本，但引入了可接受的偏差。

5. **加权对数似然最小化**  
   将正负权重组合为最终损失并更新策略参数：
   $$\mathcal{L}_{wd1}(\theta) = \mathbb{E}_{q,\{o_i\}\sim\pi_{\mathrm{old}}^{\mathrm{ref}}(\cdot|q)} \Big[ \frac{1}{G} \sum_{i=1}^{G} \big( -w^{+}(q, o_i) + w^{-}(q, o_i) \big) \cdot \log \pi_{\theta}(o_i|q) \Big]$$
   该目标仅需**一次**当前策略的似然估计（即 $\mu$ 次前向传播），而 d1 等基于比率的方法需要三次似然估计（当前、旧、参考策略）。这一简化直接带来了约 22% 的每步训练时间缩减（wd1 81.16 秒 vs d1 103.5 秒，Table 2），并完全消除了 SFT 预热阶段。

### 关键设计决策

- **无比率构造**：通过将反向 KL 惩罚的约束优化问题解析求解，得到最优策略的闭合形式，进而推导出无需策略比率的加权对数似然目标（Equation 6）。这从根本上消除了 d1 中策略比率估计的高方差和指数级近似误差放大问题（Figure 1 展示了 d1 比率估计的严重偏差）。

- **负样本惩罚**：在 WLL 基础上引入 $w^-$ 项，等价于对低优势样本执行数据反学习（data unlearning），防止模型强化劣质生成。消融实验（Table 4）证实，移除 $w^-$ 使 GSM8K 性能从 80.8% 骤降至 65.7%，验证了该设计的必要性。

- **无需 SFT**：由于 wd1 不依赖旧策略的精确似然，可直接从 base 模型启动 RL 微调。实验表明，加入 SFT 预热对 Sudoku 和 GSM8K 无益，甚至损害 Countdown 性能（51.2% → 43.4%，Table 4）。

### wd1++ 的扩展

wd1++ 将加权对数似然目标扩展为**去噪步级（denoising‑stepwise）**形式，利用扩散解码过程中产生的中间干净完成序列，对每个去噪步骤施加优势加权损失。这使得模型能在更细粒度上学习高优势生成分布，在 MATH500 和 GSM8K 上分别达到 44.2% 和 84.5%，仅需 20 步 RL 训练（Table 3）。

## 核心模块与公式推导

### 3.1 从策略比率到加权对数似然：WLL 损失

扩散语言模型（dLLM）的似然函数不可解，迫使基于 GRPO 的策略优化必须依赖近似。现有方法（如 d1）在重要性采样中需要计算策略比率：

$$r_i^k(\theta) = \frac{\pi_\theta(o_i^k)}{\pi_{\mathrm{old}}(o_i^k)}$$

该比率涉及当前策略、旧策略、参考策略三者的似然估计，近似误差在指数级放大后导致高方差和训练不稳定（Figure 1 展示了 d1 中比率估计的严重偏差）。

wd1 的核心洞察是：**通过反向 KL 惩罚的约束优化，可将策略优化目标转化为无需比率的加权对数似然形式**。具体地，从带反向 KL 惩罚和参考策略正则化的优化问题出发：

$$\max_\theta \mathbb{E}_{q \in \mathcal{D}, o \sim \pi_\theta(\cdot|q)} \left[ A^{\pi_{\mathrm{old}}}(q, o) - \lambda D_{\mathrm{KL}}(\pi_\theta(\cdot|q) \| \pi_{\mathrm{old}}(\cdot|q)) - \beta D_{\mathrm{KL}}(\pi_\theta(\cdot|q) \| \pi_{\mathrm{ref}}(\cdot|q)) \right]$$

该问题存在解析形式的最优策略：

$$\pi^*(\cdot|q) \propto \pi_{\mathrm{old}}(\cdot|q)^{\lambda/(\lambda+\beta)} \cdot \pi_{\mathrm{ref}}(\cdot|q)^{\beta/(\lambda+\beta)} \cdot \exp\left(\frac{A^{\pi_{\mathrm{old}}}(q,\cdot)}{\lambda+\beta}\right)$$

通过将最优策略投影回参数空间（最小化反向 KL 散度），可导出**加权对数似然（WLL）损失**：

$$\mathcal{L}_{\mathrm{WLL}}(\theta) = \mathbb{E}_{o \sim \pi_{\mathrm{old}}^{\mathrm{ref}}(\cdot|q)} \Big[ - \exp\big(\psi A^{\pi_{\mathrm{old}}}(q, o)\big) \cdot \log \pi_\theta(o|q) \Big]$$

其中 $\psi = 1/(\lambda+\beta)$ 为温度系数。**该损失仅需当前策略 $\pi_\theta$ 的似然近似，完全消除了对旧策略和参考策略似然的依赖，从根本上规避了比率估计的误差放大问题。**

### 3.2 wd1 完整目标：正负权重平衡

WLL 损失仅增强高优势样本的似然，但低优势样本（奖励极低）仅获得接近零的权重，未能被主动抑制。wd1 引入**负样本惩罚项**，形成完整的加权对数似然目标：

$$\mathcal{L}_{wd1}(\theta) = \mathbb{E}_{q,\{o_i\}\sim\pi_{\mathrm{old}}^{\mathrm{ref}}(\cdot|q)} \Big[ \frac{1}{G} \sum_{i=1}^{G} \big( -w^{+}(q, o_i) + w^{-}(q, o_i) \big) \cdot \log \pi_{\theta}(o_i|q) \Big]$$

其中正、负权重基于组相对优势计算并归一化：

$$\hat{A}_i = R(q, o_i) - \mathrm{mean}(R(q, o_{1:G}))$$

$$w^{+}(q, o_i) = \frac{\exp(\psi \hat{A}_i)}{\sum_{j=1}^{G} \exp(\psi \hat{A}_j)}, \quad w^{-}(q, o_i) = \frac{\exp(-\psi \hat{A}_i)}{\sum_{j=1}^{G} \exp(-\psi \hat{A}_j)}$$

**变量含义**：
- $q$：输入问题
- $o_i$：第 $i$ 个生成完成序列
- $G$：每组样本数
- $R(q, o_i)$：奖励函数（不限于验证器）
- $\hat{A}_i$：组内相对优势，通过减去组平均奖励得到
- $\psi$：温度系数，控制权重分布的尖锐程度
- $w^{+}$：正权重，$\propto \exp(\psi \hat{A})$，增强高优势样本的似然
- $w^{-}$：负权重，$\propto \exp(-\psi \hat{A})$，抑制低优势样本的似然

**关键机制**：正权重项最大化高优势样本的对数似然（强化学习），负权重项最小化低优势样本的对数似然（数据反学习/负样本遗忘）。两者通过相加组合（$-w^+ + w^-$），当 $\hat{A}_i > 0$ 时整体权重为负（提升概率），当 $\hat{A}_i < 0$ 时整体权重为正（降低概率）。

### 3.3 wd1++：去噪步级加权优化

wd1++ 将加权对数似然目标扩展为**去噪步级（denoising-stepwise）形式**，利用解码过程中产生的中间干净完成序列进行更细粒度的优化。其损失基于去噪交叉熵（DCE）：

$$\mathcal{L}_{wd1++}(\theta) = \mathbb{E}_{\{o_i\} \sim \pi_{\mathrm{old}}^{\mathrm{ref}}(\cdot|q), \ell \sim \mathrm{Uniform}\{1,\ldots,L\}} \Big[ \frac{1}{G} \sum_{i=1}^{G} \big( -w^{+}(q, o_i) + w^{-}(q, o_i) \big) \cdot \mathcal{L}_{\mathrm{DCE}}(o_i^\ell) \Big]$$

其中 $o_i^\ell$ 表示第 $i$ 个样本在去噪步 $\ell$ 的中间干净序列，$\mathcal{L}_{\mathrm{DCE}}$ 为掩码扩散模型的去噪交叉熵损失：

$$\mathcal{L}_{\mathrm{DCE}}(\boldsymbol{x}_0) = -\mathbb{E}_{t\sim\mathcal{U}[0,1], \boldsymbol{x}_t\sim p_{t\mid 0}(\boldsymbol{x}_t|\boldsymbol{x}_0)}\left[\frac{1}{t}\sum_{k=1}^{K}\mathbf{1}(\boldsymbol{x}_t^k=[\mathbf{mask}])\log\pi_\theta(\boldsymbol{x}_0^k\mid\boldsymbol{x}_t)\right]$$

### 3.4 训练流程

wd1 的训练流程（Algorithm 1）包含以下关键模块：

1. **几何混合策略采样**：从旧策略与参考策略的几何混合分布 $\pi_{\mathrm{old}}^{\mathrm{ref}}$ 中采样生成 $G$ 个完成序列
2. **组相对优势计算**：根据奖励函数 $R$ 计算各样本的 $\hat{A}_i$
3. **正负权重计算**：利用 $\hat{A}_i$ 和温度 $\psi$ 计算归一化的 $w^+$ 和 $w^-$
4. **似然近似**：采用 d1 的高效近似方法估计当前策略 $\pi_\theta$ 的逐 token 对数似然
5. **加权对数似然最小化**：结合正负权重计算 $\mathcal{L}_{wd1}$ 并更新策略参数

### 3.5 与能量引导扩散训练的理论等价性

wd1 的 WLL 目标在理论上等价于训练能量引导的离散扩散模型。具体地，优势加权的去噪交叉熵（AW-DCE）：

$$\mathcal{L}_{\mathrm{AW-DCE}} = \mathbb{E}_{x_0\sim p_0'(\cdot)} \Big[ \exp(A(x_0)) \cdot \mathbb{E}_{t\sim[0,T], p_{t|0}'(x_t|x_0)} \big[ \sum_{x_t^i=[\mathrm{mask}]} -\frac{1}{t}\log p_{\theta}(x_0^i|x_t^{\mathrm{UM}}) \big] \Big]$$

等价于训练一个以 $\exp(A(x_0))$ 为能量引导权重的扩散模型，使模型学习采样自高优势分布。同时，负样本惩罚项可解释为通过最小化 ELBO 进行数据反学习（data unlearning）。这一等价性为 wd1 的有效性提供了理论保证。

## 实验与分析

### 核心结果：wd1在规划与数学推理任务上显著超越d1

wd1在Sudoku和Countdown两项结构化推理任务上取得了对d1的压倒性优势。在Sudoku（256 tokens）上，wd1达到**76.4%**的测试准确率，而d1仅为17.6%，提升幅度高达**58.8个百分点**（Table 1）。在Countdown（256 tokens）上，wd1同样以51.2%对25.8%领先25.4个百分点。值得注意的是，wd1完全无需SFT预热阶段，直接基于base模型进行RL微调即获得此结果，而d1依赖SFT+diffu-GRPO的两阶段流程。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_L2rfd2Czbj/figures/002_Table_1.jpg]]
*Table 1: Test Accuracy (%) of wd1 and d1. We reproduce d1 and vary completion length. Our approach without SFT, demonstrates particularly higher accuracy on Sudoku2and Countdown*

在数学推理任务GSM8K和MATH500上，wd1同样展现出稳定的性能提升，但其优势幅度小于规划任务。这一差异暗示：**扩散语言模型在需要精确约束满足的规划任务中，策略比率估计的方差问题更为致命**，而wd1通过消除比率估计从根本上解决了这一瓶颈。

### 训练效率：消除SFT与降低单步成本

Table 2的系统性成本分析揭示了wd1的双重效率优势：

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_L2rfd2Czbj/figures/003_Table_2.jpg]]
*Table 2: Comparison of Training Cost on 4×A100. We show SFT cost, average training time, FLOPs evaluated by DeepSpeed Flops Profiler, and theoretical NFEs per training step which includes $\mu$ = 8 gradient steps. wd1 removes SFT and has less cost per-step in RL than d1*

- **SFT成本归零**：d1需要2.01小时的SFT预热，wd1直接跳过该阶段。
- **单步RL训练加速**：wd1每步训练仅需**81.16秒**，低于d1的103.5秒，加速约21.6%。这一加速源于wd1仅需一次当前策略似然估计（μ次前向传播），而d1需三次（μ+2次）。
- **总计算量降低**：FLOPs从9.955×10¹⁵降至8.887×10¹⁵，降幅约**11%**。

效率提升的因果链条清晰：比率消除 → 似然估计次数减少 → 前向传播次数减半 → 训练时间与计算量同步下降。

### 并发方法对比：wd1++以极低成本实现最优性能

Table 3将扩展方法wd1++与并发RL微调方法（SDPO、TCR、MDPO）在LLaDA-8B-Instruct上进行对比。wd1++在GSM8K上达到**84.5%**，在MATH500上达到**44.2%**，均略微超越最强基线MDPO（full）的83.4%和43.4%。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_L2rfd2Czbj/figures/004_Table_3.jpg]]
*Table 3: Left: Extended method wd1++ compared to concurrent RL methods to fine-tune LLaDA-8B-Instruct. Methods denoted by “(full)” perform full fine-tuning. Right: Training cost to obtain the best model on GSM8K and MATH500. We count the total number of steps of policy iteration (model weights update), and the number of rollouts used for training (see Table 8 for details on counting)*

**关键效率数据**（Table 3右栏）：wd1++仅需**20步策略迭代**和**3840次rollout**即获得最优模型，而MDPO需要150步/14400次rollout，TCR需要7500步/240000次rollout。wd1++的rollout消耗仅为MDPO的**26.7%**、TCR的**1.6%**。这一数量级差异表明，wd1的无比率设计不仅降低了单步成本，更通过稳定训练大幅减少了收敛所需的总交互次数。

### 消融实验：负样本惩罚是性能核心支柱

Table 4的消融实验直接验证了wd1两大设计选择的必要性：

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_L2rfd2Czbj/figures/006_Table_4.jpg]]
*Table 4: Ablation on SFT and Negative Samples Weight (w−). We conduct wd1 training after SFT (wd1-SFT) and with only w ^ { + } (namely wd1-P or WLL defined in Equation ( 6 ) ) ^ { 3 } Results show that wd1 performs better without SFT on planning and math tasks. Removing negative sample reinforcement (w−) significantly hurts performance, highlighting its importance*

- **移除负样本权重（w⁻）**：在GSM8K（256 tokens）上，仅使用正权重w⁺的WLL变体（wd1-P）性能从80.8%骤降至**65.7%**，下降15.1个百分点。在Sudoku上同样出现显著退化（76.4%→68.8%）。这证实了**低优势样本的主动遗忘（data unlearning）是wd1成功的关键机制**，单纯加权提升高优势样本概率远不足够。
- **加入SFT预热**：wd1-SFT在Countdown上反而从51.2%降至**43.4%**，在Sudoku和GSM8K上也无增益。这表明SFT预热对wd1不必要，甚至可能因引入与RL目标不一致的分布偏差而损害性能。

### 权重配置敏感性分析

正负权重的混合比例λ对训练有显著影响（Figure 2, Table 9）。平衡配置（λ=0.5）在Sudoku上获得最高训练奖励，偏向正样本（λ=0.8）或负样本（λ=0.0）均导致奖励下降。这进一步印证了正负样本协同作用的必要性——仅强化正样本或仅惩罚负样本都无法达到最优。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_L2rfd2Czbj/figures/007_Figure_2.jpg]]
*Figure 2: Training rewards of wd1 under different combined weights on Sudoku*

温度系数ψ控制权重分配的集中度（Figure 4左）。较大的ψ（如10）导致极端权重分配，使少数样本主导梯度更新，引起性能下降。论文建议使用较小的ψ以保持权重分布的适度平滑。

### 失败模式与局限性

1. **组内奖励均匀时的训练停滞**：当采样组内所有样本获得相同奖励时（如数据集过简单或过困难），wd1的正负权重相等，损失梯度趋于零，训练可能停滞。这是基于组相对优势的方法的固有脆弱性。

2. **MATH500早期训练不稳定**：Figure 4右显示，使用不同随机种子时，MATH500早期奖励的骤降现象消失，表明训练动态对随机种子有一定敏感性，可能与初始采样分布有关。

3. **似然近似的偏差-方差权衡**：wd1继承了d1的高效似然近似方法，虽降低了计算成本，但引入了偏差。在高精度场景下，这一偏差可能成为性能瓶颈，但当前实验未直接量化其影响。

## 方法谱系与知识库定位

### 1. 问题定位：扩散语言模型RL微调中的似然比估计瓶颈

扩散语言模型（dLLM）的似然函数不可解，迫使基于策略优化的RL微调方法依赖似然近似进行重要性采样。现有方法的核心瓶颈在于**策略比率（policy ratio）计算**：需要同时估计当前策略、旧策略和参考策略的似然，并以比率形式进行重要性加权。这一过程面临两个致命问题：

- **高方差**：ELBO近似与高效近似（d1近似）之间的偏差导致比率估计方差极大，Figure 1展示了单步策略更新后比率值可严重偏离无偏的ELBO估计。
- **误差指数级放大**：比率在序列维度上累积相乘，微小近似误差被指数级放大，严重损害训练效率和稳定性。

这一瓶颈直接限制了dLLM在推理任务上的RL微调性能，表现为训练不稳定、收敛缓慢、计算开销大。

### 2. 方法谱系：从扩散GRPO到无比率加权优化

#### 2.1 基线方法：基于比率的扩散GRPO

**d1**（Zhao et al., 2025）是首个专为掩码离散扩散LLM设计的RL方法。其核心流程为：先进行SFT预热，再应用扩散GRPO（Group Relative Policy Optimization）进行RL微调。d1的损失函数依赖策略比率进行重要性采样：

$$\mathbb{E}_{o_{1:G}\sim\pi_{\mathrm{old}}(\cdot|q)}\left[\frac{1}{GK}\sum_{i=1}^{G}\sum_{k=1}^{K}\min(r_i^k(\theta)\hat{A}_i, \text{clip}(r_i^k(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_i) - \lambda D_{\mathrm{KL}}\right]$$

其中策略比率 $r_i^k(\theta) \approx \pi_\theta(o_i^k)/\pi_{\mathrm{old}}(o_i^k)$ 需通过三个策略的似然近似计算。这一设计导致：
- 每步训练需三次似然估计（$\mu+2$次前向传播）
- 比率估计的高方差和偏差
- 必须依赖SFT阶段预热模型

**diffu-GRPO** 是直接将扩散GRPO应用于LLaDA的基线，无SFT，性能显著弱于d1。

#### 2.2 并发方法：多样化探索

与wd1同期的并发dLLM RL微调方法包括：

- **SDPO**（Han et al., 2025）：采用不同的策略优化范式
- **TCR**（Wang et al., 2025d）：探索替代训练策略
- **MDPO**（He et al., 2025）：复现时使用官方实现，在GSM8K（83.4%）和MATH500（43.4%）上达到较强性能

这些方法均在不同程度上依赖策略比率或类似的重要性采样机制，未从根本上解决似然比估计的瓶颈。

#### 2.3 本文方法：无比率加权策略优化

**wd1** 的核心创新在于**完全摒弃策略比率**，将RL目标重构为加权对数似然（Weighted Log-Likelihood, WLL）目标：

$$\mathcal{L}_{wd1}(\theta) = \mathbb{E}_{q,\{o_i\}\sim\pi_{\mathrm{old}}^{\mathrm{ref}}(\cdot|q)}\left[\frac{1}{G}\sum_{i=1}^{G}\big(-w^{+}(q, o_i) + w^{-}(q, o_i)\big) \cdot \log\pi_{\theta}(o_i|q)\right]$$

其中权重仅依赖组相对优势：

$$w^{+}(q, o_i) = \frac{\exp(\psi\hat{A}_i)}{\sum_{j=1}^{G}\exp(\psi\hat{A}_j)}, \quad w^{-}(q, o_i) = \frac{\exp(-\psi\hat{A}_i)}{\sum_{j=1}^{G}\exp(-\psi\hat{A}_j)}$$

**wd1++** 进一步将加权对数似然扩展为逐步去噪形式，利用解码过程中的中间完成序列进行逐步策略优化。

### 3. 关键设计变更与因果机制

#### 3.1 从比率依赖到权重引导

| 设计维度 | d1（基线） | wd1（本文） |
|---------|-----------|-----------|
| 策略优化目标 | 依赖策略比率的GRPO目标 | 无比率的加权对数似然目标 |
| 似然估计次数 | 三次（当前+旧+参考策略） | 一次（仅当前策略） |
| 负样本处理 | 未明确惩罚低优势样本 | 引入 $w^{-}$ 主动最小化低优势样本似然 |
| SFT预热 | 必需 | 无需，可直接RL微调 |
| 计算复杂度 | $\mu+2$次前向传播/步 | $\mu$次前向传播/步 |

这一设计变更的因果机制在于：wd1的目标函数等价于**优势引导的能量引导离散扩散训练**加**负样本遗忘（数据反学习）**。正权重 $w^{+}$ 提高高优势样本的生成概率，负权重 $w^{-}$ 降低低优势样本的生成概率，从而在理论上保证模型学习到高优势生成分布。

#### 3.2 负样本惩罚的关键作用

消融实验（Table 4）提供了决定性证据：移除负样本权重 $w^{-}$（即仅使用 $w^{+}$ 的WLL）使GSM8K 256性能从80.8%骤降至65.7%，降幅达15.1个百分点。这表明**负样本遗忘是wd1性能的核心支柱**，单纯的正样本强化不足以实现有效训练。

### 4. 适用边界与局限

#### 4.1 已知局限

1. **奖励均匀时的训练停滞**：当采样组内所有样本获得相同奖励时，$w^{+}=w^{-}$，正负权重相等，训练信号消失。这可能在数据集过于简单（所有样本均正确）或过于困难（所有样本均错误）时发生。

2. **似然近似的偏差-方差权衡**：wd1虽消除了比率估计，但仍依赖d1的高效似然近似方法。该近似引入偏差，在高精度场景下可能影响性能。论文未探索更准确的ELBO估计是否能进一步提升wd1的性能。

3. **模态限制**：当前wd1框架仅适用于文本推理任务，扩展到多模态推理或统一扩散模型是未来工作方向。

#### 4.2 适用场景

wd1特别适用于以下场景：
- **规划与推理密集型任务**：Sudoku（+58.8pp）、Countdown（+25.4pp）上的巨大提升表明wd1在需要多步推理和规划的任务上优势显著
- **计算资源受限场景**：消除SFT阶段、降低每步RL训练成本（81.16秒 vs 103.5秒/步）、FLOPs降低11%
- **快速RL微调**：wd1++仅需20步RL训练即可达到SOTA性能，rollout数量减少10倍

### 5. 开放问题

1. **多模态扩展**：如何将wd1的无比率加权优化框架有效扩展到图文推理等多模态场景？

2. **似然近似改进**：能否通过更准确的似然近似（如改进的ELBO估计）在保持计算效率的同时进一步降低偏差？

3. **奖励均匀问题**：当组内奖励均匀时，如何设计奖励函数或采样策略以避免训练停滞？课程学习或动态权重调整是否是可行方案？

4. **超参数鲁棒性**：温度系数 $\psi$ 和混合权重 $\lambda$ 的消融表明存在最优区间（$\lambda=0.5$平衡混合，较小 $\psi$ 更稳定），但其任务依赖性尚需系统研究。

5. **与AR模型RL方法的统一**：wd1的无比率加权目标是否可迁移至自回归LLM的RL微调，形成统一的策略优化框架？

## 原文 PDF

![[paperPDFs/ICLR_2026/wd1_Weighted_Policy_Optimization_for_Reasoning_in_Diffusion_Language_Models.pdf]]
