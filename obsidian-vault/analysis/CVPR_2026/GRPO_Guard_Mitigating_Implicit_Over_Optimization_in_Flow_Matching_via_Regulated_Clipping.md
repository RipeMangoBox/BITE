---
title: "GRPO-Guard: Mitigating Implicit Over-Optimization in Flow Matching via Regulated Clipping"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GRPO_Guard_Mitigating_Implicit_Over_Optimization_in_Flow_Matching_via_Regulated_Clipping.pdf
project_link: null
code_link: null
aliases:
- GG
- GRPO-Guard
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 标准化重要性比率分布（RatioNorm）消除均值偏移与方差差异，并结合梯度重加权策略均衡不同去噪步的梯度贡献，从而恢复合理的裁剪行为。
primary_logic: 流匹配模型采用高斯概率计算log概率，导致重要性比率出现依赖于时间步的负偏差，而现有GRPO直接沿用LLM的离散设定未做适配；引入比率归一化和梯度均衡即可修复裁剪功能，以极小额外成本有效抑制过优化。
claims:
- 在原始 Flow-GRPO 中，重要性比率的均值低于 1 且方差随去噪步变化，导致正优势样本从未进入上裁剪界，下裁剪仅发生在末尾步。
- RatioNorm 使对数比率标准化至均值为零、方差一致，恢复裁剪上下界的正常触发，稳定训练。
- 梯度幅度在不同时间步的差异从约 20× 降至约 2.5×，防止单步主导优化。
- 在三个代理任务上，GRPO-Guard 在可比的代理得分下显著提升了复合黄金得分（HPSv2、ImageReward、UnifiedReward 归一化平均）。
---

# GRPO-Guard: Mitigating Implicit Over-Optimization in Flow Matching via Regulated Clipping

> [!tip] 核心洞察
> 流匹配模型采用高斯概率计算log概率，导致重要性比率出现依赖于时间步的负偏差，而现有GRPO直接沿用LLM的离散设定未做适配；引入比率归一化和梯度均衡即可修复裁剪功能，以极小额外成本有效抑制过优化。

| 字段 | 内容 |
|------|------|
| 中文题名 | GRPO-Guard：通过调节裁剪缓解流匹配中的隐式过优化 |
| 英文题名 | GRPO-Guard: Mitigating Implicit Over-Optimization in Flow Matching via Regulated Clipping |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.22319) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | GRPO-Guard |
| Dataset | GenEval, PickScore, TextRender |

> [!tip] 效果简介
> - GenEval (SD3.5-M + Flow-GRPO) 上，Average Gold Score (normalized) 0.89 vs 0.84 (+0.05)。
> - PickScore (SD3.5-M + Flow-GRPO) 上，Average Gold Score (normalized) 1.20 vs 1.16 (+0.04)。
> - TextRender (SD3.5-M + Flow-GRPO) 上，Average Gold Score (normalized) 0.99 vs 0.88 (+0.11)。

## 概要

**问题**：在基于 GRPO 的流匹配（Flow Matching）文本到图像生成中，现有方法直接将为大语言模型设计的 PPO 式裁剪机制迁移到连续扩散框架，却忽略了流匹配特有的高斯对数概率结构。这导致重要性比率（importance ratio）的分布出现系统性的均值左移与跨时间步方差不一致，使正优势样本几乎从未触发上裁剪边界，裁剪机制形同虚设，策略模型迅速滑入隐式过优化（reward hacking）——代理得分持续攀升而真实质量（黄金得分）不断下降。

**核心结论**：GRPO-Guard 通过两个低成本的介入——**RatioNorm**（比率归一化）与**梯度重加权**——修复了上述失效的裁剪行为。RatioNorm 将每个去噪步的对数重要性比率标准化至均值为零、方差一致，使上下裁剪边界恢复正常功能；梯度重加权则均衡不同时间步的梯度贡献，防止单一步主导优化。两者协同，以极小额外开销在保持代理得分提升的同时，显著抑制了过优化，稳定乃至提升了黄金得分。

**方法定位**：GRPO-Guard 属于**GRPO 训练框架内的自适应正则化方法**，不引入 KL 惩罚等额外约束项，亦不改变骨干模型架构或采样器设计。它仅修正了重要性比率的计算方式与策略损失的加权方案，可无缝嵌入 Flow-GRPO（Liu et al., 2025）与 DanceGRPO（Xue et al., 2025）等主流变体，适用于 SD3.5-M、Flux.1-dev 等不同流匹配骨干。

**主要结果**：在 GenEval、PickScore、TextRender 三个代理任务上，GRPO-Guard 相较 Flow-GRPO 和 DanceGRPO 基线均实现了复合黄金得分（HPSv2、ImageReward、UnifiedReward 归一化平均）的显著提升。例如，在 SD3.5-M + Flow-GRPO 设置下，GenEval 的 Average Gold 从 0.84 升至 0.89，TextRender 从 0.88 升至 0.99；在 Flux.1-dev + DanceGRPO 设置下，GenEval 的 Average Gold 从 0.88 升至 1.02。消融实验证实，仅修正比率均值已能大幅缓解黄金得分下降，而完整的 RatioNorm + 梯度重加权组合在代理得分提升与质量保持之间取得了最佳平衡。



### 流匹配与强化学习微调的交汇

扩散模型已成为文本到图像生成的主流范式，其中**流匹配（Flow Matching）** 通过直接预测速度场，在生成质量和采样效率之间取得了优良平衡。给定噪声样本 $x_t = (1 - t) x_0 + t x_1$，模型学习最小化速度预测误差：

$$\mathcal{L}(\theta) = \mathbb{E}_{t, x_0, x_1} [\| v - v_\theta(x_t, t) \|^2]$$

然而，仅凭预训练模型难以精确满足复杂的用户意图（如文本渲染、空间关系、人体比例等）。为此，研究者开始将**组相对策略优化（GRPO）**引入流匹配模型，利用奖励模型对生成样本进行偏好对齐。代表性工作包括 **Flow-GRPO**（Liu et al., 2025）和 **DanceGRPO**（Xue et al., 2025），二者均采用 SDE 采样器引入随机性，并通过组内标准化优势函数驱动策略更新：

$$\hat{A}_t^i = \frac{R(x_0^i) - \mathrm{mean}(R(x_0^i)_{i=1}^G)}{\mathrm{std}(R(x_0^i)_{i=1}^G)}$$

### 隐式过优化：一个被忽视的机制性缺陷

尽管 GRPO 在流匹配中展现出快速的代理得分提升，但一个关键问题被普遍忽视：**代理得分（proxy score）持续上升的同时，真实质量（gold score）却在下降**——这是典型的奖励黑客（reward hacking）或过优化（over-optimization）现象。如 Figure 1 所示，FlowGRPO 在训练过程中代理得分不断攀升，但黄金得分迅速进入下降通道，生成图像出现多样性丧失、细节退化、图文一致性下降等严重问题。

本文揭示了这一现象的**机制性根源**，而非简单的超参失调。核心瓶颈在于：流匹配模型采用**高斯概率**计算状态转移的对数概率，导致重要性比率（importance ratio）出现系统性的分布偏移。

具体而言，对数重要性比率的完整表达式为：

$$\log r_t(\theta) = - \frac{\| \Delta \mu_\theta \|^2}{2\sigma_t^2 dt} - \frac{\Delta \mu_\theta \cdot \epsilon}{\sigma_t \sqrt{dt}}$$

其中二次偏差项 $-\frac{\| \Delta \mu_\theta \|^2}{2\sigma_t^2 dt} \leq 0$ 导致比率分布的**均值始终低于 1**，且方差随去噪步 $t$ 显著变化。如 Figure 2(b) 所示，在低噪声步（$t$ 接近 1），方差急剧增大，分布严重左移。

### PPO 裁剪机制的失效

GRPO 的核心设计继承了 PPO 的裁剪机制，期望通过 $\mathrm{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)$ 限制策略更新幅度。然而，当重要性比率均值系统性低于 1 时：

- **正优势样本**从未触及上裁剪界 $1+\epsilon$，失去了应有的正向引导；
- **下裁剪**仅在末尾步（高方差区域）被触发，导致梯度信号严重失衡。

Figure 12 的裁剪百分比统计直接证实了这一诊断：FlowGRPO 中 $r(\theta) > 1+\epsilon$ 的裁剪几乎为零，而 $r(\theta) < 1-\epsilon$ 的裁剪集中在末尾步。这意味着模型实际上在**无约束地追逐代理奖励**，进入了隐式过优化状态。

### 梯度失衡的叠加效应

问题不止于比率分布。如 Figure 3 所示，FlowGRPO 中不同去噪步的**梯度幅度差异高达约 20 倍**，低噪声步的梯度主导了整体优化方向。这种失衡与比率偏移相互叠加，使得少数步的奖励信号足以扭曲整个策略更新，进一步加剧了过优化。

### 现有方法的局限

值得注意的是，该问题并非 GRPO 独有，而是**流匹配与高斯似然结合的结构性后果**。LLM 中的 GRPO 使用离散 token 的 log 概率，天然具有稳定的比率分布；而流匹配的连续高斯设定引入了依赖于时间步的噪声系数 $\sigma_t \sqrt{dt}$，使比率分布产生负偏差。直接将 LLM 的 GRPO 范式迁移到流匹配，必然导致裁剪机制形同虚设。

**TempFlowGRPO**（He et al., 2025）尝试通过梯度重加权来均衡不同步的贡献，但仅解决梯度失衡而忽略比率偏移，反而可能加速过优化（如消融实验 Figure 9 所示）。这进一步表明，**比率归一化与梯度均衡必须协同作用**，才能从根本上恢复裁剪机制的功能。



## 核心方法与创新机理

GRPO-Guard 的核心创新在于识别并修复了 GRPO 在流匹配（Flow Matching）模型中因高斯概率假设而引入的**隐式过优化（implicit over-optimization）**问题。与 LLM 中离散 token 的设定不同，流匹配模型使用连续高斯概率计算对数概率，导致重要性比率（importance ratio）分布出现**依赖于时间步的均值左移与方差不一致**。这一系统性偏差使得 PPO 式裁剪机制完全失效——正优势样本从未触及上裁剪界，负优势样本仅在末尾步被下裁剪，策略模型在代理得分持续上升的同时，真实生成质量（黄金得分）却不断下降。

为解决此瓶颈，GRPO-Guard 提出了两个相互配合的关键技术：

**1. 比率归一化（RatioNorm）**  
从流匹配的高斯对数概率出发，推导出对数重要性比率的完整表达式：

$$\log r_t(\theta) = -\frac{\|\Delta \mu_\theta\|^2}{2\sigma_t^2 dt} - \frac{\Delta \mu_\theta \cdot \epsilon}{\sigma_t \sqrt{dt}}$$

其中二次项 $-\frac{\|\Delta \mu_\theta\|^2}{2\sigma_t^2 dt}$ 是导致均值左移的根源，其期望为负且依赖于时间步 $t$ 和噪声系数 $\sigma_t$。RatioNorm 通过减去该偏差项并乘以 $\sigma_t\sqrt{dt}$，将比率标准化为：

$$\log \hat{r}_t(\theta) = \sigma_t \sqrt{dt} \left( \log r_t(\theta) + \frac{\|\Delta \mu_\theta\|^2}{2\sigma_t^2 dt} \right) = -\Delta \mu_\theta \cdot \epsilon$$

标准化后的比率均值为零、方差一致，裁剪上下界恢复正常功能（Figure 2(c)）。

**2. 梯度重加权**  
流匹配中不同去噪步的梯度幅度差异可达约 20×（Figure 3），导致末尾低噪声步主导优化，加剧过拟合。GRPO-Guard 在策略损失中引入步重加权因子 $\delta$：对 Flow-GRPO 采用 $\delta = 1/dt$，对 DanceGRPO 采用 $\delta = \beta/dt$（其中 $\beta = 1 + \eta^2(1-t)/(2t)$），将梯度幅度差异压缩至约 2.5×，均衡各步的梯度贡献。

两项技术以极小额外计算成本协同工作：RatioNorm 恢复裁剪机制的正确触发条件，梯度重加权防止单步主导更新，共同抑制了隐式过优化，使策略模型在代理得分提升的同时保持黄金得分的稳定。



GRPO-Guard 是一个即插即用的训练框架，旨在修复流匹配（Flow Matching）模型中 GRPO 训练时因重要性比率分布异常而引发的隐式过优化（implicit over-optimization）。该框架由三个核心模块构成：**SDE 采样器**、**RatioNorm 比率标准化**、以及**带梯度重加权的 PPO 式裁剪**，三者串联形成完整的策略更新管线。

### 管线总览

整个训练管线遵循“采样—评分—标准化—重加权—裁剪更新”的闭环流程：

1. **SDE 采样器（SDE Sampler）**  
   给定当前策略模型 $p_\theta$，从随机噪声 $x_1 \sim \mathcal{N}(0, I)$ 出发，按离散化的逆向 SDE 逐步去噪生成样本 $x_0$。采样过程引入随机性以支持探索，其递推公式为：
   $$x_{t+dt} = x_t + \left[ v_\theta(x_t, t) + \frac{\sigma_t^2}{2t}\left(x_t + (1-t)v_\theta(x_t, t)\right) \right]dt + \sigma_t \sqrt{dt}\,\epsilon$$
   其中 $v_\theta$ 为策略模型预测的速度场，$\sigma_t$ 为噪声调度参数。该模块为后续的策略更新提供完整的去噪轨迹 $\{x_t\}_{t=0}^{T-1}$。

2. **奖励评估与组相对优势计算**  
   对每组 $G$ 个生成样本，使用代理奖励模型（如 ImageReward、UnifiedReward 等）计算标量奖励 $R(x_0^i)$，并在组内进行标准化得到优势函数：
   $$\hat{A}_t^i = \frac{R(x_0^i) - \text{mean}(\{R(x_0^i)\}_{i=1}^G)}{\text{std}(\{R(x_0^i)\}_{i=1}^G)}$$
   组相对优势替代了传统 PPO 中的价值函数估计，消除了对额外 critic 网络的依赖。

3. **RatioNorm 比率标准化**  
   这是 GRPO-Guard 的核心创新模块。原始 Flow-GRPO 中，重要性对数比率 $\log r_t(\theta)$ 存在依赖于时间步 $t$ 的负偏差（由高斯对数概率中的二次项 $\|\Delta\mu_\theta\|^2/(2\sigma_t^2 dt)$ 引起），导致其均值低于 1 且方差随去噪步剧烈变化。RatioNorm 通过减去该偏差并乘以缩放因子 $\sigma_t\sqrt{dt}$，得到标准化对数比率：
   $$\log \hat{r}_t(\theta) = \sigma_t \sqrt{dt} \left( \log r_t(\theta) + \frac{\|\Delta\mu_\theta\|^2}{2\sigma_t^2 dt} \right) = -\Delta\mu_\theta \cdot \epsilon$$
   标准化后的比率 $\hat{r}_t(\theta)$ 均值为零、方差在各时间步上保持一致，使得 PPO 式裁剪的上下界能够正常触发（见图 2(b) vs 图 2(c)）。

4. **梯度重加权与 PPO 式裁剪**  
   尽管 RatioNorm 消除了比率分布的偏移，不同去噪步的梯度幅度仍存在显著差异（在 FlowGRPO 中可达约 20×）。为此，GRPO-Guard 在策略损失中引入步重加权因子 $\delta$，最终目标函数为：
   $$\mathcal{T}_{\text{policy}}(\theta) = \frac{1}{G} \sum_{i=1}^G \frac{1}{T} \sum_{t=0}^{T-1} \delta \cdot \min\left( \hat{r}_t^i(\theta) \hat{A}_t^i,\ \text{clip}(\hat{r}_t^i(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t^i \right)$$
   其中 $\delta = 1/dt$（对应 Flow-GRPO 设置）或 $\delta = \beta/dt$（对应 DanceGRPO 设置，$\beta = 1 + \eta^2(1-t)/(2t)$），用于抵消采样步长 $dt$ 引入的梯度缩放差异。经此处理后，梯度幅度变异从约 20× 压缩至约 2.5×（见图 3），防止单一步主导优化方向。

### 模块关系与数据流

上述模块之间的数据流关系可概括为：**SDE 采样器**输出完整去噪轨迹 → **奖励模型**对终端样本 $x_0$ 评分并计算组内优势 → **RatioNorm** 对每个时间步的对数重要性比率进行标准化 → **梯度重加权 + 裁剪**模块综合标准化比率与步权重计算策略损失，反向传播更新模型参数。整个过程无需额外的 KL 惩罚项，也无需训练 critic 网络，保持了与原始 Flow-GRPO 相同的计算开销量级。

### 方法谱系与知识库定位

GRPO-Guard 处于 **RLHF 微调扩散模型** 与 **PPO 式裁剪机制适配连续生成模型** 的交叉点上。其直接改进的基线包括：
- **Flow-GRPO**（Liu et al., 2025）：将 GRPO 直接应用于流匹配模型，但未考虑重要性比率的分布偏移问题。
- **DanceGRPO**（Xue et al., 2025）：采用恒定噪声调度的 GRPO 变体，同样存在裁剪失效和梯度失衡问题。
- **TempFlowGRPO**（He et al., 2025）：仅使用基于 $\sigma_t\sqrt{dt}$ 的重加权策略，虽能加速优化但增加了过优化风险（消融实验证实，见 §4.3）。

与上述方法相比，GRPO-Guard 的独特贡献在于首次揭示了流匹配中重要性比率分布的系统性偏差是导致 PPO 裁剪失效的根本原因，并通过 RatioNorm 与梯度重加权的组合以极小额外成本恢复了裁剪机制的正常功能。该框架可即插即用于不同的 GRPO 变体和扩散骨干网络，在三个代理任务上均显著提升了复合黄金得分（HPSv2、ImageReward、UnifiedReward 归一化平均），同时保持了与 KL-free 基线相当的收敛速度。

> **注意**：本文未提供与基于 KL 惩罚的 GRPO 变体（如带 KL 散度约束的原始 GRPO 实现）的定量对比，因此 GRPO-Guard 在 KL 正则化场景下的相对表现需要手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l2682_https_arxiv_org_abs_2510_22319/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between FlowGRPO and GRPO-Guard under over-optimization. Left: The proxy score and gold score trends during training. As the proxy score increases, FlowGRPO rapidly enters an over-optimization phase, where the gold score continuously declines. Right: A visual comparison between FlowGRPO and GRPO-Guard. Due to severe reward hacking, FlowGRPO suffers from a drastic degradation in diversity, detail richness, visual quality, and text-image consistency (bottom part). In contrast, GRPO-Guard maintains a stable gold score and high visual quality under a comparable proxy score, as shown in the upper part of the figure*



### 问题根源：重要性比率的分布异常

在 Flow-GRPO 与 DanceGRPO 中，策略更新的核心依赖于重要性比率 $r_t(\theta) = \frac{p_\theta(x_{t-1}|x_t)}{p_{\theta_{\text{old}}}(x_{t-1}|x_t)}$。流匹配模型使用高斯分布计算状态转移的对数概率：

$$\log p_\theta(x_{t-1}|x_t, c) = - \frac{\|x_{t-1} - \mu_\theta(x_t, t)\|^2}{2\sigma_t^2 dt} - C_t \tag{6}$$

将新旧策略的对数概率相减，可推导出对数重要性比率的完整表达式：

$$\log r_t(\theta) = - \frac{\|\Delta \mu_\theta\|^2}{2\sigma_t^2 dt} - \frac{\Delta \mu_\theta \cdot \epsilon}{\sigma_t \sqrt{dt}} \tag{7}$$

其中 $\Delta \mu_\theta = \mu_\theta(x_t, t) - \mu_{\theta_{\text{old}}}(x_t, t)$，$\epsilon \sim \mathcal{N}(0, I)$ 为采样噪声。

该表达式揭示了两个关键异常（见 Figure 2(b)）：
- **均值左移**：二次项 $-\frac{\|\Delta \mu_\theta\|^2}{2\sigma_t^2 dt}$ 始终为负，使 $\mathbb{E}[\log r_t(\theta)] < 0$，即比率均值低于 1。这导致正优势样本几乎永远不会触发上裁剪界 $1+\epsilon$，PPO 式裁剪机制在正样本上完全失效。
- **方差不一致**：噪声点积项 $\frac{\Delta \mu_\theta \cdot \epsilon}{\sigma_t \sqrt{dt}}$ 的方差与 $\sigma_t \sqrt{dt}$ 相关，随去噪步变化显著，使裁剪行为在不同时间步上极不均衡。

![[assets/figures/papers/paper_list_l2682_https_arxiv_org_abs_2510_22319/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of r(θ) distributions between FlowGRPO and GRPO-Guard across timesteps. (a) Ideally, the ratio distribution should have a mean near 1 and stable variance across timesteps to ensure effective clipping. (b) Under FlowGRPO, the distribution exhibits a leftward mean shift and increasing variance at low-noise timesteps, causing the clipping mechanism to fail—particularly for trajectories with positive advantages. In contrast, GRPO-Guard with RatioNorm preserves a balanced mean and consistent variance (c), enabling proper clipping and stable policy updates across all timesteps*

### RatioNorm：标准化重要性比率

为修复上述分布异常，GRPO-Guard 提出 **RatioNorm**，对对数比率进行两步处理：先减去均值偏移（二次项），再乘以缩放因子消除方差差异：

$$\log \hat{r}_t(\theta) = \sigma_t \sqrt{dt} \left( \log r_t(\theta) + \frac{\|\Delta \mu_\theta\|^2}{2\sigma_t^2 dt} \right) = -\Delta \mu_\theta \cdot \epsilon \tag{8}$$

标准化后的比率 $\hat{r}_t(\theta)$ 具有以下性质：
- **均值为零**：$\mathbb{E}[\log \hat{r}_t(\theta)] = 0$，使正/负优势样本均能正常触发上/下裁剪界。
- **方差一致**：去除了 $\sigma_t \sqrt{dt}$ 的影响，各时间步的比率分布方差趋于稳定。

如 Figure 2(c) 所示，经过 RatioNorm 后，裁剪上下界 $1 \pm \epsilon$ 能够有效约束梯度更新，恢复了 PPO 式裁剪的正常功能。

### 梯度重加权：均衡去噪步贡献

即使比率分布得到修复，不同去噪步的梯度幅度仍存在巨大差异。Flow-GRPO 的策略梯度可写为：

$$\nabla_\theta \mathcal{I}(\theta) = \sum_{t=0}^{T-1} \mathbb{E}_\epsilon \left[ \beta \frac{\Delta \mu_\theta + \sigma_t \sqrt{dt} \epsilon}{\sigma_t^2} \hat{A}_t r_t(\theta) \nabla_\theta \Delta \mu_\theta \right]$$

其中系数 $\beta$ 与噪声调度相关。在 Flow-GRPO 中，梯度幅度在不同时间步的差异可达约 **20×**（见 Figure 3），导致低噪声步主导优化，加剧过优化风险。

![[assets/figures/papers/paper_list_l2682_https_arxiv_org_abs_2510_22319/figures/004_Figure_3.jpg]]
*Figure 3: Gradient magnitude differences across timesteps. In FlowGRPO, gradient magnitudes vary by roughly 20× across timesteps, reflecting the large differences in gradient scale. GRPO-Guard substantially reduces this imbalance, limiting the variation to about 2.5× and preventing over-optimization under any single noise condition*

GRPO-Guard 在策略损失中引入重加权因子 $\delta$，与 $dt$（及调度参数 $\beta$）相抵消：

$$\mathcal{T}_{\text{policy}}(\theta) = \frac{1}{G} \sum_{i=1}^G \frac{1}{T} \sum_{t=0}^{T-1} \delta \cdot \min\left( \hat{r}_t^i(\theta) \hat{A}_t^i, \text{clip}(\hat{r}_t^i(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t^i \right) \tag{12}$$

其中 $\delta = 1/dt$（Flow-GRPO 情况）或 $\delta = \beta/dt$（DanceGRPO 情况，$\beta = 1 + \frac{\eta^2(1-t)}{2t}$）。该重加权将梯度幅度差异从约 20× 压缩至约 **2.5×**，防止任一步骤单独主导优化过程。

### 模块串联

GRPO-Guard 的完整流程由以下模块构成：
1. **SDE 采样器**：依据策略模型生成多步去噪轨迹 $x_0^i$。
2. **奖励评估与组相对优势**：计算组内标准化优势 $\hat{A}_t^i = \frac{R(x_0^i) - \text{mean}(R)}{\text{std}(R)}$。
3. **RatioNorm**：按式 (8) 标准化每个去噪步的对数比率，消除均值偏移与方差差异。
4. **PPO 式裁剪**：对 $\hat{r}_t(\theta)$ 应用 $\text{clip}(\cdot, 1-\epsilon, 1+\epsilon)$。
5. **梯度重加权**：乘以 $\delta$ 因子均衡各步梯度贡献，形成最终策略损失。

### 补充图表

![[assets/figures/papers/paper_list_l2682_https_arxiv_org_abs_2510_22319/figures/015_Figure_12.jpg]]
*Figure 12: Clipping percentage of*



## 实验与关键发现

### 主结果：复合黄金得分与代理得分趋势

GRPO-Guard 的核心目标并非单纯提升代理得分（proxy score），而是在保持代理得分提升的同时，抑制过优化导致的真实质量（gold score）退化。Table 1 报告了不同代理任务下，各方法在三个黄金评估器（HPSv2、ImageReward、UnifiedReward）上的归一化平均得分。

![[assets/figures/papers/paper_list_l2682_https_arxiv_org_abs_2510_22319/figures/005_Table_1.jpg]]
*Table 1: Comparison of composite gold scores across different proxy tasks. [·] marks the proxy task associated with each row. ImR denotes ImageReward, UniR denotes UnifiedReward, and Average represents the mean value after normalizing the three gold scores relative to the base model (set to 1)*

在 SD3.5-M 骨干上，以 Flow-GRPO（Liu et al., 2025）为基线，GRPO-Guard 在所有三个代理任务上均实现了黄金得分的显著提升：
- **GenEval 代理任务**：平均黄金得分从 0.84 提升至 0.89（+0.05）
- **PickScore 代理任务**：平均黄金得分从 1.16 提升至 1.20（+0.04）
- **TextRender 代理任务**：平均黄金得分从 0.88 提升至 0.99（+0.11）

在 Flux.1-dev 骨干上，以 DanceGRPO（Xue et al., 2025）为基线，GRPO-Guard 同样展现出稳定的增益：
- **GenEval 代理任务**：平均黄金得分从 0.88 提升至 1.02（+0.14）
- **TextRender 代理任务**：平均黄金得分从 0.96 提升至 1.02（+0.06）

Figure 4 的验证曲线进一步揭示了训练动态：Flow-GRPO 和 DanceGRPO 的代理得分持续上升，但黄金得分在达到峰值后快速下降，呈现典型的过优化特征；而 GRPO-Guard 在代理得分保持相似上升趋势的同时，黄金得分维持稳定甚至继续改善。这表明 RatioNorm 与梯度重加权机制有效恢复了 PPO 式裁剪的约束功能，防止策略模型通过利用奖励模型的漏洞来“欺骗”代理得分。

![[assets/figures/papers/paper_list_l2682_https_arxiv_org_abs_2510_22319/figures/006_Figure_4.jpg]]
*Figure 4: Validation curves of proxy scores and gold scores across different training tasks and baseline methods*

**证据强度**：Table 1 的实验设置与基线完全一致（相同骨干、LoRA 配置、数据集和验证集），仅改变比率计算与损失函数，结果的可归因性较高。但需注意，黄金得分本身受限于奖励模型的评估能力，无法完全等同于人类感知质量。

---

### 消融研究：RatioNorm 与梯度重加权的贡献

Table 2 和 Figure 9 报告了主要组件的消融结果，揭示了各机制对过优化抑制的独立与协同效应。

![[assets/figures/papers/paper_list_l2682_https_arxiv_org_abs_2510_22319/figures/011_Figure_9.jpg]]
*Figure 9: Training curves of the ablation study*

![[assets/figures/papers/paper_list_l2682_https_arxiv_org_abs_2510_22319/figures/012_Table_2.jpg]]
*Table 2: Ablation study on major components*

**仅修正比率均值（Mean-revised）**：单独修正重要性比率的负偏差（即减去二次项 $\|\Delta\mu_\theta\|^2/(2\sigma_t^2 dt)$）已能显著缓解黄金得分的下降趋势。这验证了核心瓶颈——均值左移导致正优势样本无法触发上裁剪——是过优化的主要驱动因素。然而，仅做均值修正仍存在残差过优化，因为方差在不同时间步的不一致性未得到解决。

**RatioNorm 完整标准化**：在均值修正的基础上，通过乘以 $\sigma_t\sqrt{dt}$ 消除噪声系数带来的方差差异，使所有时间步的比率分布均值为零、方差一致。Figure 2(c) 显示，标准化后裁剪上下界（$1\pm\varepsilon$）能够正常触发，正优势样本重新进入上裁剪区域，负优势样本的下裁剪也不再局限于末尾步。这一配置在代理得分提升与黄金得分稳定之间取得了最佳平衡。

**梯度重加权**：仅使用基于 $\sigma_t\sqrt{dt}$ 的重加权（类似 TempFlowGRPO，He et al., 2025）虽能加速优化，但 Figure 9 显示其增加了过优化风险——原因在于重加权放大了低噪声步的梯度贡献，而这些步恰好是奖励黑客最容易发生的区域。GRPO-Guard 将梯度重加权与 RatioNorm 结合，在均衡各步梯度贡献（Figure 3，梯度幅度变异从约 20× 降至约 2.5×）的同时，通过标准化比率恢复了裁剪的对称性，从而在加速收敛与抑制过优化之间实现平衡。

**证据强度**：消融实验在受控条件下进行，各配置仅改变所研究的组件，结论可信度较高。但消融曲线（Figure 9）的具体数值需从原文图表中读取以确认精确差异。

---

### 失败模式与可视化分析

尽管 GRPO-Guard 显著抑制了过优化，论文也明确指出其局限性：**无法完全消除由奖励模型自身局限所导致的奖励黑客**。当代理得分与黄金得分之间存在系统性偏差时，策略模型仍可能找到绕过裁剪约束的路径。论文将此归因于奖励模型的规模不足，并指出扩大奖励模型会带来显著的计算开销，延长 GRPO 所需的采样与评分过程。

可视化对比（Figure 5–7）揭示了基线方法的典型失败模式：
- **Flow-GRPO**（Figure 5, 7）：出现严重的多样性退化、细节丢失、人体比例失真和面部多样性降低，指令跟随能力显著下降。
- **DanceGRPO**（Figure 6）：生成图像出现明显的水平和垂直条纹伪影，这是奖励黑客的典型视觉特征。
- **GRPO-Guard**：在可比代理得分下保持了稳定的视觉质量、文本生成准确性和指令遵循能力。

![[assets/figures/papers/paper_list_l2682_https_arxiv_org_abs_2510_22319/figures/007_Figure_5.jpg]]
*Figure 5: Visual comparison between FlowGRPO and GRPO-Guard. FlowGRPO exhibits clear signs of reward hacking, leading to a significant decline in both image quality and instruction-following ability. In contrast, GRPO-Guard maintains comparable visual quality while demonstrating stronger text generation accuracy and better adherence to instructions*

![[assets/figures/papers/paper_list_l2682_https_arxiv_org_abs_2510_22319/figures/008_Figure_6.jpg]]
*Figure 6: Visual comparison between DanceGRPO and GRPO-Guard. It is clearly observed that DanceGRPO suffers from severe reward hacking, where the generated images exhibit distinct horizontal and vertical stripe artifacts*

Figure 11 进一步分析了过优化模型与原始模型在不同去噪步的表现差异，揭示了过优化主要集中在特定的噪声条件区间，这与 Figure 3 中梯度幅度不平衡的观察一致——低噪声步的梯度主导了优化过程，导致模型在这些步上过度适应代理奖励。

![[assets/figures/papers/paper_list_l2682_https_arxiv_org_abs_2510_22319/figures/014_Figure_11.jpg]]
*Figure 11: Performance differences between the hacking model and the original model across different denoising steps*

**证据强度**：可视化结果直观展示了过优化的视觉表现，但定性比较受限于样本选择偏差。人类评估（Figure 10）提供了补充证据，但具体胜率数据需从原文图表中确认。

---

### 重要图表结论总结

| 图表 | 核心结论 |
|------|----------|
| Table 1 | GRPO-Guard 在三个代理任务、两个骨干模型上均实现黄金得分的稳定提升 |
| Figure 2 | RatioNorm 将重要性比率分布从均值左移、方差不一致修复为均值接近零、方差一致，恢复裁剪功能 |
| Figure 3 | 梯度重加权将不同时间步的梯度幅度变异从约 20× 降至约 2.5× |
| Figure 4 | GRPO-Guard 的代理得分与黄金得分同步上升，而基线方法出现黄金得分下降 |
| Table 2 & Figure 9 | RatioNorm 是抑制过优化的核心组件，梯度重加权在此基础上进一步均衡优化 |
| Figure 5–7 | 基线方法的过优化表现为多样性退化、条纹伪影和人体比例失真；GRPO-Guard 保持稳定质量 |

**总体评估**：GRPO-Guard 以极小的额外计算成本（仅修改比率计算和损失重加权，无需额外网络或推理步骤），在多个 GRPO 变体和骨干模型上一致地抑制了隐式过优化。其有效性源于对重要性比率分布异常的精确诊断和针对性修复，而非引入外部正则化或增大模型容量。但彻底解决奖励黑客仍需奖励模型本身的改进，这是一个开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l2682_https_arxiv_org_abs_2510_22319/figures/013_Figure_10.jpg]]
*Figure 10: Human evaluation results*



## 定位与知识库关联

### 与基线方法的关系

GRPO-Guard 并非引入全新的强化学习框架，而是在现有流匹配 GRPO（Group Relative Policy Optimization）变体的基础上，针对**重要性比率（importance ratio）的分布异常**与**梯度尺度失衡**进行结构性修复。其直接对比与改进的基线包括：

- **Flow-GRPO**（Liu et al., 2025）：标准 GRPO 在流匹配上的直接应用，未引入 KL 惩罚。GRPO-Guard 在此基线上叠加 RatioNorm 与梯度重加权，解决了其裁剪机制失效导致的隐式过优化。
- **DanceGRPO**（Xue et al., 2025）：采用恒定噪声调度的 GRPO 变体，同样存在重要性比率均值左移与方差不一致的问题。GRPO-Guard 通过适配的梯度重加权因子 $\delta = \beta/dt$（其中 $\beta = 1 + \eta^2(1-t)/(2t)$）对该变体进行修复。
- **TempFlowGRPO**（He et al., 2025）：仅基于 $\sigma_t\sqrt{dt}$ 进行梯度重加权的工作。消融实验（Fig. 9）表明，该策略虽能加速代理得分优化，但单独使用会**增加过优化风险**；GRPO-Guard 将重加权与 RatioNorm 结合，在加速收敛与抑制过优化之间取得了更优的平衡。

从方法谱系上看，GRPO-Guard 处于 **PPO 式裁剪在扩散/流匹配模型中的适配与修复** 这一节点。其核心贡献在于揭示了：当状态转移概率为高斯分布时，对数重要性比率天然包含一个与时间步相关的**负二次偏差项**，使得沿用 LLM 离散设定（比率均值约等于 1）的裁剪机制在流匹配中系统性失效。这一发现将“过优化”问题从奖励模型的局限性拓展到了**优化器本身的数学结构缺陷**。

### 适用边界

GRPO-Guard 的有效性已在以下条件下得到验证（Table 1, Fig. 4）：

- **骨干模型**：SD3.5-M、Flux.1-dev（均为 Rectified Flow 架构）。
- **GRPO 变体**：Flow-GRPO、DanceGRPO。
- **代理任务**：GenEval、PickScore、TextRender。
- **评估指标**：复合黄金得分（HPSv2、ImageReward、UnifiedReward 的归一化平均）。

方法的适用边界存在以下约束：

1. **依赖高斯概率假设**：RatioNorm 的推导基于流匹配中状态转移的高斯对数概率形式（Equation 6）。若底层生成模型采用非高斯概率建模（如离散扩散、分类分布），偏差项的形式将不同，标准化策略需重新推导。
2. **未解决奖励模型自身偏差**：论文明确指出（§Limitations），GRPO-Guard 无法消除由奖励模型局限性（代理得分与黄金得分之间的固有差距）导致的奖励黑客。当奖励模型本身存在系统性偏差时，即使裁剪机制正常工作，策略仍可能学到利用奖励模型弱点的生成模式。
3. **计算开销未显著增加**：RatioNorm 与梯度重加权均为后处理操作，不引入额外网络前传或采样步骤。但论文未在极端低步数（如 $T < 5$）或极高分辨率场景下验证该方法的稳定性。

### 局限与开放问题

**已确认的局限**：

- **奖励模型规模瓶颈**：论文指出，彻底解决奖励黑客需要扩大奖励模型规模，但这会显著增加 GRPO 采样与评分过程的计算开销。当前 GRPO-Guard 在“代理得分提升”与“黄金得分稳定”之间取得了平衡，但无法保证在更强代理任务下不出现新的过优化模式。
- **无法完全消除过优化**：消融实验（Fig. 9）显示，即使使用完整的 GRPO-Guard，黄金得分在训练后期仍可能出现轻微下降趋势，表明 RatioNorm + 梯度重加权是**缓解而非根除**过优化。

**开放问题**：

1. **高效对齐奖励模型的设计**：如何构建一个计算高效且能精准对齐代理得分与真实质量（黄金得分）的奖励模型，以在不显著增加成本的前提下进一步抑制奖励黑客？这是论文明确提出的未来挑战。
2. **跨架构泛化性**：当前验证限于 Rectified Flow 架构。该方法在 DDPM、DDIM 等扩散变体，以及非图像模态（如视频、音频生成）中的适用性尚待验证。
3. **裁剪阈值 $\epsilon$ 的敏感性**：论文未系统研究 RatioNorm 后裁剪阈值 $\epsilon$ 的最优取值。标准化后的比率分布均值为零、方差一致，但 $\epsilon$ 的选择是否需要在不同任务或骨干模型间调整，缺乏消融证据。
4. **与 KL 惩罚的协同**：GRPO-Guard 在无 KL 惩罚的设定下验证（与 Flow-GRPO、DanceGRPO 保持一致）。若与 KL 惩罚结合，RatioNorm 是否仍能提供额外增益，或 KL 惩罚本身已能部分纠正比率分布偏移，尚未探索。



## 原文 PDF

![[paperPDFs/CVPR_2026/GRPO_Guard_Mitigating_Implicit_Over_Optimization_in_Flow_Matching_via_Regulated_Clipping.pdf]]
