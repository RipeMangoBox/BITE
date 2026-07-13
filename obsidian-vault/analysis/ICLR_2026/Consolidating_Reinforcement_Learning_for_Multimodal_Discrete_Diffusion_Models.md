---
title: "Consolidating Reinforcement Learning for Multimodal Discrete Diffusion Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Consolidating_Reinforcement_Learning_for_Multimodal_Discrete_Diffusion_Models.pdf
project_link: null
code_link: https://github.com/martian422/MaskGRPO
openreview_forum_id: 9nxCJP4q0i
aliases:
- CRLMDDM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "针对语言和视觉的模态特异性设计：(1)重要性估计器——语言采用渐弱掩码(AR-like fading-out masking)，视觉采用高截断的随机掩码；(2)rollout采样器——语言使用半自回归解码，视觉使用概率性 emerge 采样器；(3)截断参数γ和时间步调度策略。"
primary_logic: "离散扩散模型在语言上表现出自回归偏差(AR-ness)，在视觉上具有全局 token 相关性，利用这些结构性先验可以设计出高效、稳定的重要性估计器和采样器，从而使 GRPO 策略优化在离散扩散上可行并显著提升性能。"
claims:
- "MaskGRPO在GSM8K(256 tokens)上Pass@1达到84.7，相较基模型提升+8.0，几乎使RL收益翻倍。"
- "在GenEval整体指标上，MaskGRPO将MMaDA从0.56提升至0.81(+0.25)，结合SFT后达到0.90。"
- "消融实验表明，AR-like reversing为GSM8K带来+3.1的单项最大提升。"
- "Emerge采样器在图像生成消融中为GenEval带来+0.25的增益。"
---

# Consolidating Reinforcement Learning for Multimodal Discrete Diffusion Models

> [!tip] 核心洞察
> 离散扩散模型在语言上表现出自回归偏差(AR-ness)，在视觉上具有全局 token 相关性，利用这些结构性先验可以设计出高效、稳定的重要性估计器和采样器，从而使 GRPO 策略优化在离散扩散上可行并显著提升性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向多模态离散扩散模型的强化学习整合方法 |
| 英文题名 | Consolidating Reinforcement Learning for Multimodal Discrete Diffusion Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=9nxCJP4q0i) · [GitHub](https://github.com/martian422/MaskGRPO) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | MaskGRPO |
| Dataset | GSM8K (seq_len=256), MATH500 (seq_len=512), MBPP (seq_len=256), GenEval |

> [!tip] 效果简介
> - GSM8K (seq_len=256) 上，Pass@1 为 84.7，对比 76.7 (LLaDA-8B-Instruct)，变化 +8.0。
> - MATH500 (seq_len=512) 上，Pass@1 为 41.5，对比 36.2 (LLaDA-8B-Instruct)，变化 +5.3。
> - MBPP (seq_len=256) 上，Pass@1 为 45.4，对比 39.0 (LLaDA-8B-Instruct)，变化 +6.4。

## 概要

**核心问题**：将 GRPO（Group Relative Policy Optimization）等强化学习方法扩展到离散扩散模型（Discrete Diffusion Models, DDMs）面临根本性障碍。DDM 的非自回归生成特性导致两个关键挑战：（1）token 级别的重要性采样不可处理，因为 DDM 在去噪过程中同时生成所有 token，破坏了自回归模型中的条件依赖关系；（2）rollout 生成过程复杂，现有方法要么依赖高计算代价的蒙特卡洛估计，要么因近似不当导致训练不稳定。这严重限制了 RL 在离散扩散模型上的应用效果。

**方法定位**：MaskGRPO 针对上述瓶颈，提出了面向语言和视觉的模态特异性设计。核心洞察在于：离散扩散模型在语言任务上表现出**自回归偏差（AR-ness）**——模型倾向于按从左到右的顺序生成 token；在视觉任务上则具有**全局 token 相关性**——图像 token 之间存在强局部和全局依赖。利用这些结构性先验，MaskGRPO 分别设计了高效的重要性估计器和 rollout 采样器，使 GRPO 策略优化在离散扩散模型上可行且稳定。

**主要贡献**：
- **语言侧**：提出 AR-like 渐弱掩码估计器（Alg. 1），逐步增加序列尾部 token 的掩码率，模拟自回归的条件依赖结构；配合半自回归采样器（Alg. 3）和截断参数 γ=0.6，实现稳定训练。
- **视觉侧**：采用高截断的随机掩码估计器（Alg. 2）和 Emerge 采样器（Alg. 4），让视觉 token 通过概率解码自然涌现，而非强制分块解码。
- **统一框架**：将上述组件整合为 MaskGRPO 优化循环（Alg. 5），包含多步内部梯度更新和线性时间步调度。

**关键结果**：
- 在数学推理基准 GSM8K（256 tokens）上，MaskGRPO 将基模型 LLaDA-8B-Instruct 的 Pass@1 从 76.7 提升至 **84.7（+8.0）**，几乎使 RL 收益翻倍（Table 1）。
- 在文本到图像生成基准 GenEval 上，MaskGRPO 将 MMaDA 的整体得分从 0.56 提升至 **0.81（+0.25）**；结合 SFT 后进一步提升至 **0.90**（Table 2）。
- 消融实验证实，AR-like reversing 为语言任务带来 +3.1 的单项最大提升（Table 4），Emerge 采样器为图像生成贡献 +0.25 的增益（Table 5）。

**方法谱系与知识库定位**：MaskGRPO 建立在离散扩散模型（LLaDA-8B-Instruct, Nie et al., 2025；MMaDA）和 GRPO 策略优化算法的基础上，与现有 DDM-RL 方法形成对比：**diffu-GRPO**（Zhao et al., 2025）采用基于掩码的重要性估计但缺乏位置偏差；**UniGRPO**（Yang et al., 2025）使用迭代掩码策略但未利用模态特异性先验；**TraceRL**（Wang et al., 2025b）基于轨迹的重要性估计计算开销较大。MaskGRPO 的关键区分点在于通过模态特异性设计实现了更高效、更稳定的重要性估计，同时使用更少的全局训练步数（500 步 vs diffu-GRPO 的 7000+ 步）。

### 离散扩散模型：自回归之外的生成范式

离散扩散模型（Discrete Diffusion Models, DDM）近年来作为自回归模型的替代方案受到广泛关注。其核心思想是通过前向过程逐步将离散 token 替换为 mask token，再通过逆向过程从噪声中恢复原始数据。形式上，给定干净数据 $x_0$，前向过程在时间 $t$ 产生带噪序列 $x_t$：

$$x_t \sim q(x_t | x_0, t), \quad q(x_t | x_0, t) = \mathbf{Cat}(x_t; \alpha_t x_0 + (1 - \alpha_t) \mathbf{m})$$

其中 $\mathbf{m}$ 为 mask token，$\alpha_t$ 为时间相关的噪声调度参数。模型 $\pi_\theta$ 通过最小化证据下界（ELBO）来学习逆向去噪过程：

$$\mathcal{L}_{\mathrm{DDM}} = -\mathbb{E}_{t, x_0, x_t} \left[\frac{1}{t} \sum_{i=1}^{L} \delta(x_{(t,i)}, \mathbf{m}) \log \pi_{\theta}(x_{(0,i)} | x_t)\right]$$

与自回归模型逐 token 生成不同，DDM 的非自回归特性使其能并行解码，在推理效率上具有天然优势。近年来，LLaDA（Nie et al., 2025）等工作已证明 DDM 在语言建模上可与自回归模型竞争，而 MMaDA 等模型进一步将离散扩散扩展到文本到图像生成领域。

### 强化学习对齐的困境：GRPO 为何难以直接迁移

在自回归语言模型中，GRPO（Group Relative Policy Optimization）已成为主流对齐方法。其核心机制是：对每个输入 $\mathbf{c}$，采样一组响应 $\{o_i\}_{i=1}^G$，计算组内标准化优势 $A_i$，然后通过 token 级重要性比率 $\rho_i^k$ 进行策略优化：

$$A_i = \frac{r_i - \mathrm{mean}(\{r_j\}_{j=1}^{G})}{\mathrm{std}(\{r_j\}_{j=1}^{G})}$$

$$\rho_i^k = \frac{\pi_{\theta}(o_i^k | \mathbf{c}, o_i^{<k})}{\pi_{\theta_{\mathrm{old}}}(o_i^k | \mathbf{c}, o_i^{<k})}$$

GRPO 最终优化目标为：

$$\max_{\theta} \mathbb{E}_{\mathbf{c}\sim\mathcal{D}, o_{1:G}\sim\pi_{\theta}(\cdot|\mathbf{c})} \left[R(\theta, \mathbf{c}) - \beta \mathbb{D}_{\mathrm{KL}}[\pi_{\theta}(\cdot|\mathbf{c}) || \pi_{\mathrm{ref}}(\cdot|\mathbf{c})]\right]$$

然而，当试图将 GRPO 迁移到 DDM 时，两个根本性障碍浮现：

1. **重要性采样不可处理**：自回归模型中 $\rho_i^k$ 基于条件概率链式法则自然定义，而 DDM 的生成过程涉及从完全掩码状态出发的多步去噪，不存在逐 token 的条件依赖结构。这使得 token 级重要性比率无法直接计算。

2. **Rollout 生成复杂**：DDM 的采样需要多步迭代去噪，每次生成都需要完整的逆向过程，计算代价远高于自回归模型的逐 token 解码。

现有工作尝试绕过这些障碍：diffu-GRPO（Zhao et al., 2025）采用基于掩码的重要性估计，UniGRPO（Yang et al., 2025）使用迭代掩码策略，TraceRL（Wang et al., 2025b）则引入 trace-based 重要性。但这些方法要么破坏了 DDM 的条件依赖关系，要么依赖高计算代价的蒙特卡洛估计，导致策略优化不稳定或效率低下。

### 核心洞察：利用模态特异性结构先验

本文的关键发现是：**离散扩散模型在不同模态上表现出截然不同的结构性先验，这些先验可以被利用来设计高效、稳定的强化学习策略**。

- **语言模态的自回归偏差（AR-ness）**：尽管 DDM 在训练时是非自回归的，但语言数据本身具有从左到右的因果结构。实验表明，在逆向掩码过程中，逐渐向序列末尾增加掩码比例（fading-out masking）能够更好地保持条件依赖关系，从而产生更可靠的重要性估计。

- **视觉模态的全局相关性**：图像 token 之间不存在严格的顺序依赖，但 token 的全局共现模式对生成质量至关重要。有效的重要性估计需要在高截断的掩码率下进行（$\gamma$ 接近 1），以捕捉有信息量的变化，同时避免过度破坏图像结构。

基于这些洞察，MaskGRPO 提出了一套模态特异性的设计：语言采用 AR-like 渐弱掩码估计器，视觉采用高截断随机掩码；语言 rollout 使用半自回归采样器，视觉使用 Emerge 概率涌现采样器。这些设计使得 GRPO 策略优化在离散扩散模型上首次实现稳定有效的训练，并在数学推理（GSM8K +8.0）、代码生成（MBPP +6.4）和图像生成（GenEval +0.25）等任务上取得显著提升，几乎使强化学习收益翻倍（Figure 1）。

## 核心方法与创新机理

MaskGRPO 的核心创新在于**针对离散扩散模型（DDM）的非自回归特性，为语言与视觉分别设计了模态特化的策略优化组件**，从而将 GRPO 强化学习首次稳定、高效地扩展到多模态离散扩散模型。其关键改进可归纳为以下三个 changed slots：

### 1. 重要性估计器：从随机掩码到结构感知掩码

原始 GRPO 的重要性比率 $\rho_i^k$ 依赖自回归的条件依赖关系（Eq. 5），这在 DDM 中不可直接处理。现有 DDM-RL 方法（如 **diffu-GRPO**（Zhao et al., 2025）的随机掩码估计）要么破坏条件依赖，要么依赖高计算代价的蒙特卡洛近似。

MaskGRPO 的解决方案是利用两类模态的结构性先验：
- **语言**：采用 **AR-like fading-out masking**（类自回归渐弱掩码），从序列前部向后部逐渐增加掩码概率（Alg. 1, Figure 2 左）。这利用了语言模型在离散扩散中表现出的“自回归偏差”（AR-ness），使重要性估计更贴近真实的 token 依赖关系。
- **视觉**：采用**高截断随机掩码**，在截断范围 $[\gamma, 1]$ 内（$\gamma=0.8$）进行均匀随机掩码（Alg. 2）。这是因为视觉 token 具有全局相关性，过低的掩码率无法捕获有效的变化信息，而高截断能集中计算预算于信息量最大的去噪阶段。

消融实验验证了这一设计的决定性作用：AR-like reversing 在 GSM8K 上带来 **+3.1** 的单项最大提升（Table 4），且有效控制了 KL 散度，避免过拟合（Figure 5 底部）。

### 2. Rollout 采样器：从强制解码到概率涌现

对于视觉生成的 rollout 采样，传统 MaskGIT 风格的置信度重掩码采样器强制规定每步解码数量，限制了生成多样性。MaskGRPO 提出 **Emerge 采样器**（Alg. 4），通过概率解码让 token 从掩码中自然涌现，不强制每步解码数量，从而更好地保留视觉 token 间的全局依赖关系（Figure 3 定性对比显示 Emerge 采样器生成图像的纹理和表现力显著优于 MaskGIT 风格采样器）。

消融实验中，Emerge 采样器为 GenEval 整体指标带来 **+0.25** 的增益（Table 5），是视觉 RL 训练中最大的单项提升。

对于语言生成，则沿用成熟的**半自回归采样器**（Alg. 3），采用分块低置信度重掩码策略，与 AR-like 重要性估计器形成协同。

### 3. 截断时间步调度与随机性管理

DDM 的反向过程在低时间步（高掩码率）时预测不确定性极高，直接纳入优化会导致梯度噪声过大。MaskGRPO 引入**截断参数 $\gamma$**，将重要性估计的采样范围从 $(0,1)$ 压缩至 $(\gamma, 1)$：语言任务 $\gamma=0.6$，视觉任务 $\gamma=0.8$（Section 3.1, 3.2）。消融显示 $\gamma=0.6$ 时训练最稳定，无截断（$\gamma=0$）或过度截断（$\gamma=0.8$）均导致性能下降（Figure 5a）。

此外，MaskGRPO 在反向过程中**管理每设备的独立随机种子**，确保重要性估计和 KL 计算的稳定性（Section 3.1），这一工程细节在消融中被证明对训练稳定性有实质贡献。

在优化层面，MaskGRPO 采用**多次内部梯度更新**（$\mu=12$）配合**线性时间步调度** $t_j = \gamma + (1-\gamma)j/\mu$（Alg. 5），将重要性比率和 KL 估计在多个时间步上累积（Eq. 11），相比单步估计显著提升了策略梯度的信噪比。

MaskGRPO 的整体框架围绕一个核心洞察展开：**离散扩散模型（DDM）在语言与视觉模态中呈现出截然不同的结构性先验**——语言序列具有自回归偏差（AR-ness），而视觉 token 则表现出全局相关性。利用这些先验，MaskGRPO 为 GRPO 策略优化中的两个关键瓶颈——**重要性估计**和**rollout 采样**——分别设计了模态特异性的高效方案，从而在无需昂贵蒙特卡洛估计的前提下，使离散扩散上的强化学习训练变得稳定且高效。

### 框架总览

图 1（右）给出了 MaskGRPO 的直观流程：给定一个基模型（语言任务使用 **LLaDA-8B-Instruct**（Nie et al., 2025），视觉任务使用 **MMaDA**），框架在 GRPO 的组内标准化优势（Eq. 4）驱动下，通过以下模块闭环运行：

| 模块 | 语言模态 | 视觉模态 | 核心功能 |
|------|----------|----------|----------|
| **逆向掩码（重要性估计器）** | AR-like 渐弱掩码（Alg. 1） | 高截断随机掩码（Alg. 2） | 生成部分掩码序列，用于估计策略比率 $\hat{\rho}_i^t$ |
| **Rollout 采样器** | 半自回归解码器（Alg. 3） | Emerge 概率涌现采样器（Alg. 4） | 从当前策略生成完整序列 $o_i$ |
| **奖励计算** | 数学/代码正确性奖励 | UnifiedReward + HPSv3 + CLIP Score | 为每个 rollout 计算标量奖励 $r_i$ |
| **策略梯度更新** | 多时间步内更新 $\mu=12$（Alg. 5） | 同左 | 累积重要性比率与 KL 散度，执行梯度下降 |

### 关键设计决策与数据流

**1. 截断时间步范围。** 所有逆向掩码操作均将采样范围从 $(0,1)$ 截断至 $(\gamma, 1)$，其中语言任务 $\gamma=0.6$，视觉任务 $\gamma=0.8$。这一设计将有限的时间步预算集中在高信息量的掩码区间，避免低掩码率下重要性估计的方差爆炸。消融实验（Figure 5a）表明，$\gamma=0.6$ 获得最佳训练稳定性，无截断（$\gamma=0$）或过度截断（$\gamma=0.8$）均导致性能下降。

**2. 模态特异性重要性估计。** 这是框架中最具决定性的设计选择：
- **语言（AR-like Reversing, Alg. 1）：** 利用语言模型的自回归偏差，对序列施加渐弱掩码——前部 token 掩码概率低，后部 token 掩码概率逐渐升高。这一策略使 KL 散度得到有效控制（Figure 5 底部），避免过拟合。消融实验（Table 4）显示，AR-like reversing 在 GSM8K 上带来 **+3.1** 的单项最大提升。
- **视觉（Random Reversing, Alg. 2）：** 由于视觉 token 具有全局相关性，低掩码率即可捕获足够的信息变化。因此采用高截断的随机掩码，在 $\gamma=0.8$ 的范围内均匀采样掩码位置。

**3. 模态特异性 Rollout 采样。**
- **语言（Semi-autoregressive Sampler, Alg. 3）：** 采用分块低置信度重掩码策略，在保持非自回归并行解码优势的同时，通过置信度引导逐步揭示 token。
- **视觉（Emerge Sampler, Alg. 4）：** 不强制规定每步解码数量，而是让 token 从掩码中按概率自然涌现。在 MMaDA（配备 8192 词表视觉 tokenizer）上，Emerge 采样器在图像生成消融中为 GenEval 带来 **+0.25** 的增益（Table 5），并在纹理和表现力上显著优于 MaskGIT 风格采样器（Figure 3）。

**4. 策略梯度更新循环（Alg. 5）。** 每个 rollout $o_i$ 经过 $\mu=12$ 次内更新，时间步按 $t_j = \gamma + (1-\gamma)j/\mu$ 线性调度。在每个时间步 $t_j$，构造掩码补全 $\hat{o}_{i,t_j}$，计算重要性估计 $\hat{\rho}_i^{t_j}$（Eq. 9）和 KL 估计 $\widehat{\mathbb{D}}_{\mathrm{KL}}^{i,t_j}$（Eq. 10），最终累积为 MaskGRPO 目标（Eq. 11）并执行梯度下降。

**5. 随机性管理。** 逆向过程中，每台设备管理独立的随机种子，确保重要性和 KL 计算在不同设备间稳定可复现。这一看似细微的设计被证明对训练稳定性至关重要。

### 输入输出流

- **输入：** 条件 $\mathbf{c}$（语言提示或文本描述）和基模型 $\pi_{\theta_{\text{old}}}$。
- **Rollout 生成：** 从当前策略 $\pi_\theta$ 采样 $G$ 个完整序列 $\{o_i\}_{i=1}^G$。
- **奖励与优势：** 计算每个序列的奖励 $r_i$，组内标准化得到优势 $A_i$（Eq. 4）。
- **策略评估：** 对每个序列在 $\mu$ 个时间步上构造掩码版本，计算重要性比率和 KL 散度。
- **输出：** 更新后的策略参数 $\theta$，在语言任务上实现推理准确率提升（GSM8K +8.0，MATH500 +5.3，MBPP +6.4），在视觉任务上实现生成质量和文本-图像对齐的显著改善（GenEval +0.25，HPSv3 +0.59）。

### 3.1 离散扩散模型基础

MaskGRPO 建立在连续时间离散扩散模型（DDM）之上。前向过程将原始 token 序列 $x_0$ 逐步替换为 mask token $\mathbf{m}$：

$$x_t \sim q(x_t | x_0, t), \quad q(x_t | x_0, t) = \mathbf{Cat}(x_t; \alpha_t x_0 + (1 - \alpha_t) \mathbf{m})$$

其中 $\alpha_t$ 是随 $t \in (0,1]$ 递减的噪声调度参数。模型 $\pi_\theta$ 的训练目标为证据下界（ELBO）：

$$\mathcal{L}_{\mathrm{DDM}} = -\mathbb{E}_{t, x_0, x_t} \left[\frac{1}{t} \sum_{i=1}^{L} \delta(x_{(t,i)}, \mathbf{m}) \log \pi_{\theta}(x_{(0,i)} | x_t)\right]$$

该损失仅在 mask 位置上计算预测分布与真实 token 的交叉熵。采样时，从完全 masked 序列 $x_1$ 出发，通过去噪转移规则逐步揭示 token：

$$p_{\theta}(x_s | x_t) = \begin{cases} 1, & \mathrm{if } x_s = x_t, x_t \neq \mathbf{m}, \\ \frac{1 - \alpha_s}{1 - \alpha_t}, & \mathrm{if } x_s = \mathbf{m}, x_t = \mathbf{m}, \\ \frac{\alpha_s - \alpha_t}{1 - \alpha_t} \pi_{\theta}(x_t), & \mathrm{if } x_s \neq \mathbf{m}, x_t = \mathbf{m}, \\ 0, & \mathrm{otherwise}. \end{cases}$$

核心约束在于：一旦 token 从 $\mathbf{m}$ 变为具体值，便不可再被掩码。这一非自回归特性构成了将 GRPO 迁移至 DDM 的根本性障碍。

### 3.2 GRPO 原始框架及其在 DDM 中的不适配

GRPO 通过组内标准化优势函数来优化策略。给定 $G$ 个 rollout 序列 $\{o_i\}_{i=1}^G$ 及其奖励 $\{r_i\}$，优势函数定义为：

$$A_i = \frac{r_i - \mathrm{mean}(\{r_j\}_{j=1}^{G})}{\mathrm{std}(\{r_j\}_{j=1}^{G})}$$

在自回归模型中，token 级别的重要性比率可直接计算：

$$\rho_i^k = \frac{\pi_{\theta}(o_i^k | \mathbf{c}, o_i^{<k})}{\pi_{\theta_{\mathrm{old}}}(o_i^k | \mathbf{c}, o_i^{<k})}$$

GRPO 的裁剪奖励项和目标函数分别为：

$$R(\theta, \mathbf{c}) = \frac{1}{G} \sum_{i=1}^{G} \frac{1}{|o_i|} \sum_{k=1}^{|o_i|} \min(\rho_i^k A_i, \mathrm{clip}(\rho_i^k, 1-\epsilon, 1+\epsilon) A_i)$$

$$\max_{\theta} \mathbb{E}_{\mathbf{c}\sim\mathcal{D}, o_{1:G}\sim\pi_{\theta}(\cdot|\mathbf{c})} \left[R(\theta, \mathbf{c}) - \beta \mathbb{D}_{\mathrm{KL}}[\pi_{\theta}(\cdot|\mathbf{c}) || \pi_{\mathrm{ref}}(\cdot|\mathbf{c})]\right]$$

**瓶颈**：DDM 的非自回归特性导致 $\rho_i^k$ 不可直接计算——token 之间不存在严格的条件依赖顺序，重要性采样在数学上不可处理。现有方法要么强行引入伪自回归顺序破坏条件依赖，要么依赖高计算代价的蒙特卡洛估计。

### 3.3 MaskGRPO 核心公式：重要性估计与 KL 散度

MaskGRPO 的核心创新在于绕过 token 级重要性，转而估计**子序列级**的重要性比率。给定 rollout 序列 $o_i$ 及其在时间步 $t$ 的掩码版本 $o_i^t$（由逆向过程生成），重要性估计器定义为新旧策略对完整序列预测差异的指数：

$$\hat{\rho}_i^t = \exp\left(\ell_{\pi_{\theta}}(o_i^t, o_i | \mathbf{c}) - \ell_{\pi_{\theta_{\mathrm{old}}}}(o_i^t, o_i | \mathbf{c})\right)$$

其中 $\ell_{\pi}(o_i^t, o_i | \mathbf{c})$ 表示策略 $\pi$ 在给定上下文 $\mathbf{c}$ 和掩码序列 $o_i^t$ 时，对原始序列 $o_i$ 的对数似然。这一设计利用了 DDM 的全局条件依赖特性：模型在任意时间步都能对整个序列做出预测。

KL 散度的近似估计采用类似思路：

$$\widehat{\mathbb{D}}_{\mathbf{KL}}^{i,t} = \exp\left(\ell_{\pi_{\theta_{\mathrm{rf}}}}(o_i^t, o_i | \mathbf{c}) - \ell_{\pi_{\theta}}(o_i^t, o_i | \mathbf{c})\right) - \left(\ell_{\pi_{\theta_{\mathrm{rf}}}}(o_i^t, o_i | \mathbf{c}) - \ell_{\pi_{\theta}}(o_i^t, o_i | \mathbf{c})\right) - 1$$

该估计器通过参考策略 $\pi_{\theta_{\mathrm{rf}}}$ 与当前策略的预测差异来约束策略更新幅度。

### 3.4 MaskGRPO 目标函数与优化流程

整合上述组件，MaskGRPO 的最终目标函数在每个时间步累加重要性和 KL 项：

$$\max_{\theta} \mathbb{E}_{\mathbf{c}\sim\mathcal{D}, o_{1:G}\sim\pi_{\theta}(\cdot|\mathbf{c})} \left[\frac{1}{G} \sum_{i=1}^{G} \frac{A_i}{|o_i|} \sum_{j=1}^{\mu} \left(\hat{\rho}_i^{t_j} - \beta \hat{\mathbb{D}}_{\mathrm{KL}}^{i,t_j}\right)\right]$$

其中 $\mu$ 为内部梯度更新次数（设为 12），时间步按线性调度分配：

$$t_j = \gamma + (1 - \gamma)\frac{j}{\mu}$$

$\gamma$ 为截断参数，将采样范围从 $(0,1)$ 压缩至 $(\gamma,1)$，避免低噪声区域的无信息梯度。消融实验表明，语言任务中 $\gamma=0.6$ 获得最佳训练稳定性（Figure 5a），无截断（$\gamma=0$）或过度截断（$\gamma=0.8$）均导致性能下降。

### 3.5 模态特异性设计：逆向过程与采样器

重要性估计的质量高度依赖于逆向掩码策略。针对语言和视觉的结构性差异，MaskGRPO 采用两套独立设计。

**语言：AR-like 渐弱掩码（Alg. 1）**  
利用语言模型的自回归偏差（AR-ness），对序列末端施加更高的掩码率，形成“渐弱”模式。具体而言，掩码概率矩阵 $M$ 由条件矩阵 $C$、随机矩阵 $R$ 和概率矩阵 $P$ 共同决定：

$$M \gets (\neg C) \land (R < P)$$

其中 $P$ 沿序列位置递增。消融实验表明，AR-like reversing 在 GSM8K 上带来 +3.1 的单项最大提升（Table 4），且能有效控制 KL 散度避免过拟合（Figure 5 bottom）。

**视觉：高截断随机掩码（Alg. 2）**  
视觉 token 具有全局相关性，低掩码率无法提供足够的变异信息。因此采用 $\gamma=0.8$ 的高截断随机掩码策略。

**文本 rollout：半自回归采样器（Alg. 3）**  
采用分块低置信度重掩码策略进行文本生成，平衡生成质量与多样性。

**图像 rollout：Emerge 采样器（Alg. 4）**  
不强制每步解码固定数量的 token，而是让 token 通过概率控制自然“涌现”。采样分布为：

$$q_s \gets \frac{\alpha_s - \alpha_t}{1 - \alpha_t} \cdot \pi + \delta_{\mathbf{m}} \cdot \frac{1 - \alpha_s}{1 - \alpha_t}$$

其中 $\pi$ 为模型预测分布，$\delta_{\mathbf{m}}$ 为 mask token 的指示分布。消融实验中，Emerge 采样器为 GenEval 带来 +0.25 的增益（Table 5），并在视觉质量上显著优于 MaskGIT 风格采样器（Figure 3）。

**随机性管理**：逆向过程中通过为每个设备分配独立随机种子，确保重要性和 KL 估计的稳定性（Section 3.1）。

## 实验与关键发现

### 核心瓶颈与验证

将 GRPO 等强化学习方法扩展到离散扩散模型（DDM）的核心瓶颈在于：非自回归生成特性导致 token 级别的重要性采样不可处理，rollout 生成过程复杂。现有方法要么破坏条件依赖关系，要么依赖高计算代价的蒙特卡洛估计，无法稳定有效地进行策略优化。MaskGRPO 针对这一瓶颈，利用语言和视觉的模态特异性结构先验——语言的自回归偏差（AR-ness）和视觉的全局 token 相关性——设计出高效、稳定的重要性估计器和采样器，使 GRPO 策略优化在离散扩散上可行。

**决定性证据**：
- MaskGRPO 在 GSM8K（256 tokens）上 Pass@1 达到 84.7，相较基模型提升 +8.0，几乎使 RL 收益翻倍（Table 1，置信度 0.95）。
- 在 GenEval 整体指标上，MaskGRPO 将 MMaDA 从 0.56 提升至 0.81（+0.25），结合 SFT 后达到 0.90（Table 2，置信度 0.95）。
- 消融实验表明，AR-like reversing 为 GSM8K 带来 +3.1 的单项最大提升（Table 4，置信度 0.95）。
- Emerge 采样器在图像生成消融中为 GenEval 带来 +0.25 的增益（Table 5，置信度 0.95）。
- 截断参数 γ=0.6 能使训练最稳定，无截断或过度截断均导致性能下降（Figure 5a，置信度 0.9）。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_9nxCJP4q0i/figures/005_Table_1.jpg]]
*Table 1: Evaluation on math reasoning and coding benchmarks. For fair comparison, we choose LLaDA-8B-Instruct as the initial point. All results are reported with Pass@1 metric. † refers to our re-implementation*

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_9nxCJP4q0i/figures/021_Table_4.jpg]]
*Table 4: Ablation on math reasoning*

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_9nxCJP4q0i/figures/022_Table_5.jpg]]
*Table 5: Ablation on image generation*

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_9nxCJP4q0i/figures/016_Figure_5.jpg]]
*Figure 5: Ablative results. a: ablation on timestep truncation in language tasks. b: ablation on reverse methods in language tasks. Bottom: KL divergence during RL training under different reverse strategies. See text for detailed explanation*

### 主实验结果

#### 数学推理与代码生成

Table 1 展示了在 LLaDA-8B-Instruct 基模型上的 RL 微调结果，所有结果均采用 Pass@1 指标。MaskGRPO 在所有基准和序列长度设置上均取得最优性能：

- **GSM8K（seq_len=256）**：MaskGRPO 达到 84.7，相较基模型（76.7）提升 +8.0，相较 diffu-GRPO（79.8）提升 +4.9。
- **MATH500（seq_len=512）**：MaskGRPO 达到 41.5，相较基模型（36.2）提升 +5.3。
- **MBPP（seq_len=256）**：MaskGRPO 达到 45.4，相较基模型（39.0）提升 +6.4。

值得注意的是，MaskGRPO 使用更少的全局训练步数（500 步 vs diffu-GRPO 的 7000+ 步），却实现了更大的性能增益。UniGRPO 的结果以 † 标注，为作者复现。

#### 文本到图像生成

Table 2 的 GenEval 基准评估显示，MaskGRPO 在离散扩散图像生成上带来显著提升：

- MaskGRPO 单独使用将 MMaDA 的 GenEval 整体得分从 0.56 提升至 0.81（+0.25）。
- 在 BLIP3-o 数据集上进行 SFT 后，SFT+MaskGRPO 进一步提升至 0.90（+0.34），接近连续扩散模型的顶级水平。

Table 7 的 DPG-Bench 评估进一步验证了这一趋势：MaskGRPO 将 MMaDA 的 Overall 得分从 0.71 提升至 0.75（+0.04），SFT+MaskGRPO 达到 0.82（+0.11）。

#### 人类偏好与构图生成

Table 3 展示了在 DPG-Bench 提示词生成样本上的人类偏好评分：

- HPSv3：MaskGRPO 从 8.81 提升至 9.40（+0.59），SFT+MaskGRPO 达到 9.63（+0.82）。
- ImageReward：从 0.93 提升至 1.18（+0.25），SFT+MaskGRPO 达到 1.30（+0.37）。
- DeQA：从 3.99 提升至 4.10（+0.11），SFT+MaskGRPO 达到 4.18（+0.19）。

Figure 4 的定性对比进一步证实，MaskGRPO 在艺术风格、摄影细节和整体氛围等美学质量维度上带来实质性改善。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_9nxCJP4q0i/figures/013_Figure_4.jpg]]
*Figure 4: Qualitative comparison. Results are generated with identical sampling parameters and shown in {original, w/ RL} pairs. MaskGRPO demonstrates substantial improvement on the aesthetic quality of generated images, in terms of artistic style, photographic details and overall atmosphere. We strongly recommend that the readers view more portrait samples at Fig. 10. Table 3: Evaluation on compositional generation and human preference metrics. We calculate the Preference Scores on samples generated by DPG-Bench prompts*

### 消融实验

#### 数学推理消融

Table 4 的消融实验逐层拆解了 MaskGRPO 各组件的贡献。从 diffu-GRPO 基线（79.8）开始：

- 管理随机种子（Managed Randomness）：+0.6，达到 80.4，验证了重要性估计稳定性的重要性。
- AR-like reversing：**+3.1**，达到 83.5，这是单项最大提升，证实了利用语言自回归偏差进行掩码策略设计的关键作用。
- 截断与其他优化：+1.2，达到最终 84.7。

Figure 5b 进一步对比了不同逆向方法，AR-like reversing 在所有设置下均优于 TraceRL。Figure 5（bottom）显示，使用 AR-like reverse 时 KL 散度得到有效控制，避免了过拟合。

#### 图像生成消融

Table 5 的消融从 UniGRPO 基线（GenEval 0.63）开始：

- 添加截断技术：+0.12，达到 0.75。
- 添加 Emerge 采样器：**+0.06**，达到 0.81。

Emerge 采样器贡献了 +0.25 的总增益中的关键部分。Figure 3 的视觉对比显示，在相同采样参数下，Emerge 采样器生成的图像在纹理和表现力上明显优于 MaskGIT 风格采样器。

#### 截断参数敏感性

Figure 5a 的消融表明，截断参数 γ 对训练稳定性有显著影响：

- γ=0.6 获得最佳性能，训练过程最稳定。
- γ=0（无截断）或 γ=0.8（过度截断）均导致性能下降。

这一发现验证了合理分配时间步预算对有效重要性估计的必要性。

### 失败模式与局限性

尽管 MaskGRPO 在主要基准上表现优异，但仍存在以下局限：

1. **图像编辑能力有限**：MMaDA 未经过大规模编辑训练，Table 6 的 PIE-Bench 结果显示编辑性能有限，仅进行了初步研究。
2. **模态特异性设计**：方法需要针对语言和视觉分别设计重要性估计器和采样器，尚未实现完全统一的跨模态 RL 框架。
3. **超参数敏感性**：训练对截断超参数 γ 敏感，需人工调整，缺乏自适应机制。
4. **采样器依赖性**：视觉生成的高保真度依赖于 Emerge 采样器，在大词汇量 tokenizer 下的泛化性需进一步验证。
5. **数据依赖性**：SFT 数据能显著提升性能（GenEval 从 0.81 提升至 0.90），但数据依赖可能限制纯 RL 场景的适用性。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_9nxCJP4q0i/figures/025_Table_6.jpg]]
*Table 6: Quantitative results for Image Editing on PIE-Bench*

### 公平性说明

实验设计中采取了多项公平性措施：
- 针对 MBPP，明确规定了一套标准化评测协议，以消除文献中因参数不一致导致的结果差异。
- MMaDA 的 MixCoT 检查点因在数学/代码任务上性能极低（GSM8K 仅 48%），未被用作基线，所有语言任务均从 LLaDA-8B-Instruct 开始。
- 图像生成中 UniGRPO 的 RL 结果直接引用其报告最终性能，因其未公布训练配置。
- 所有模型使用可比较的资源和训练步数；MaskGRPO 使用更少的全局步数（500 步 vs diffu-GRPO 的 7000+ 步）。

## 定位与知识库关联

### 核心问题与突破点

将强化学习（RL）扩展到离散扩散模型（DDM）的根本瓶颈在于其**非自回归生成特性**：DDM 的生成过程是并行去噪，而非逐 token 左到右解码，这导致标准 GRPO 中依赖的 token 级别重要性比率 $ρ_i^k$ 无法直接计算——重要性采样在 DDM 中不可处理，rollout 生成也需要处理整个序列的联合分布。现有方法要么通过逐 token 独立近似**破坏了条件依赖关系**，要么依赖高计算代价的蒙特卡洛估计，无法稳定有效地进行策略优化。MaskGRPO 的核心洞察是：**离散扩散模型在不同模态上表现出结构性先验**——语言上的自回归偏差（AR-ness）和视觉上的全局 token 相关性——利用这些先验可以设计出高效、稳定的重要性估计器和采样器，使 GRPO 在离散扩散上可行。

### 与现有 RL-for-DDM 方法的关系

在 MaskGRPO 之前，已有若干工作尝试将策略优化引入离散扩散模型，但均存在显著局限：

- **diffu-GRPO**（Zhao et al., 2025）采用基于掩码的重要性估计，但使用随机均匀掩码，未考虑语言序列的位置偏置，导致重要性估计噪声大、训练不稳定。
- **UniGRPO**（Yang et al., 2025）使用迭代掩码策略，试图统一语言和视觉的 RL 流程，但其重要性估计未利用模态特异性，在数学推理等任务上性能有限（GSM8K 仅 79.1，见 Table 1）。
- **TraceRL**（Wang et al., 2025b）采用基于轨迹的重要性估计，在消融实验中（Table 4, Figure 5b）被 MaskGRPO 的 AR-like reversing 方法**一致超越**，表明简单的轨迹级估计不如利用自回归偏差的渐弱掩码策略有效。
- **wd1**（Tang et al., 2025）作为另一 RL 基线，其具体实现细节未在论文中展开，但在 Table 1 的对比中性能低于 MaskGRPO。

MaskGRPO 与上述方法的本质区别在于**模态感知的专一化设计**：不追求统一的跨模态方案，而是针对语言和视觉分别构建重要性估计器和采样器。这一策略的合理性在消融实验中得到验证——AR-like reversing 为 GSM8K 带来 +3.1 的单项最大提升（Table 4），Emerge 采样器为 GenEval 带来 +0.25 的增益（Table 5）。

### 技术谱系中的位置

MaskGRPO 处于三个技术方向的交汇点：

1. **离散扩散模型**：继承自 DDM 的连续时间掩码扩散框架（Eq. 1-3），基模型为 **LLaDA-8B-Instruct**（Nie et al., 2025）用于语言任务，**MMaDA** 用于视觉任务。MaskGRPO 不修改 DDM 的前向/反向过程本身，而是在其之上构建 RL 优化层。

2. **GRPO 策略优化**：直接继承 DeepSeek 团队的 GRPO 框架（Eq. 4-7），包括组内标准化优势函数和 KL 散度约束。MaskGRPO 的核心贡献是将 GRPO 的 token 级重要性比率 $\rho_i^k$（Eq. 5）替换为子序列级估计器 $\hat{\rho}_i^t$（Eq. 9），通过模型在时间步 $t$ 的预测差异来近似完整序列的重要性。

3. **模态特异性采样**：语言端采用**半自回归采样器**（Alg. 3），视觉端采用**Emerge 采样器**（Alg. 4）。Emerge 采样器的设计哲学与 MaskGIT 风格的置信度重掩码采样器形成对比——后者强制每步解码固定数量的 token，而 Emerge 通过概率解码让 token 自然涌现，在视觉质量上表现更优（Figure 3）。

### 方法适用边界

**有效场景**：
- 语言任务：数学推理（GSM8K, MATH500）和代码生成（MBPP），序列长度 256-512 tokens，使用 AR-like fading-out masking 作为重要性估计器。
- 视觉任务：文本到图像生成（GenEval, DPG-Bench）和构图生成，使用高截断随机掩码（$\gamma=0.8$）和 Emerge 采样器。
- 可与 SFT 结合：在 SFT 后应用 MaskGRPO 可进一步提升性能（GenEval 从 0.56 到 0.90，Table 2）。

**已知局限**：
- **模态分离**：语言和视觉需要分别设计重要性估计器和采样器，尚未实现完全统一的跨模态 RL 框架。
- **超参数敏感**：截断参数 $\gamma$ 对训练稳定性影响显著，$\gamma=0.6$ 为语言任务最优，$\gamma=0$ 或 $\gamma=0.8$ 均导致性能下降（Figure 5a），需要人工调整。
- **视觉泛化性**：Emerge 采样器的高保真度依赖于 8192-vocab 的视觉 tokenizer（Xie et al., 2024），在更大规模模型或不同 tokenizer 下的表现需进一步验证。
- **数据依赖**：SFT 数据（BLIP3-o）能显著提升性能，纯 RL 场景下的适用性受限。
- **编辑能力有限**：图像编辑仅在 PIE-Bench 上进行了初步研究（Table 6），MMaDA 未经过大规模编辑训练，性能有限。

### 开放问题

1. **统一重要性估计**：能否设计跨模态统一的重要性估计方法，减少对手动模态适配的依赖？当前 AR-like reversing 和随机掩码的策略差异较大，是否存在一个统一的数学框架来表征不同模态下的最优掩码策略？

2. **Emerge 采样器的扩展性**：Emerge 采样器在更大规模视觉模型或不同 tokenizer（如 MAGVIT-v2, OmniTokenizer）上的表现如何？其概率解码机制是否会在大词汇量下引入额外的随机性噪声？

3. **跨模态迁移**：该框架是否适用于其他离散扩散应用，如音频生成（基于 EnCodec tokenizer）、视频生成（时空离散 token）？这些模态是否具有类似的结构性先验可以利用？

4. **自适应截断**：能否自动调整截断参数 $\gamma$ 以适配不同任务和训练阶段？当前的手动调整策略限制了方法的即插即用性。

5. **奖励模型集成**：MaskGRPO 当前使用 UnifiedReward、HPSv3 和 CLIP Score 的组合作为视觉奖励函数，能否与更先进的奖励模型（如 ImageReward-v2, PickScore）结合，进一步提升对齐质量？

## 原文 PDF

![[paperPDFs/ICLR_2026/Consolidating_Reinforcement_Learning_for_Multimodal_Discrete_Diffusion_Models.pdf]]
