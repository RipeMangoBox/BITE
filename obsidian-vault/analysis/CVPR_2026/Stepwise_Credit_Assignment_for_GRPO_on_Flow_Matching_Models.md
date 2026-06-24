---
title: Stepwise Credit Assignment for GRPO on Flow-Matching Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Stepwise_Credit_Assignment_for_GRPO_on_Flow_Matching_Models.pdf
project_link: "https://stepwiseflowgrpo.com"
code_link: null
aliases:
- SFG
- SCAGFMM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "逐步增益（stepwise gain）g_t^i = r_{t-1}^i - r_t^i，通过Tweedie公式从中间噪声状态估计清洁图像并计算奖励，使每个步骤获得与其对奖励的边际改进成正比的信用。"
primary_logic: 利用中间奖励估计将全局信用分解为每步的边际贡献，使强化学习策略能够感知扩散过程的时间层次，重点优化对最终质量影响大的早期步骤，从而提高样本效率和收敛速度。
claims:
- Stepwise-Flow-GRPO在PickScore、ImageReward、UnifiedReward等不同奖励函数及数据集上，训练奖励与收敛速度均一致优于Flow-GRPO。
- 早期步骤的增益量级更大，表明构图决策驱动了大部分奖励改进，统一信用分配忽略了这一现象。
- 在GenEval基准上经过400 GPU小时扩展训练后，Stepwise-Flow-GRPO达到0.87总分，显著优于Flow-GRPO（0.72），甚至超过GPT-4o（0.84）。
- 联合归一化（所有步骤和轨迹共享统计量）相比逐步归一化，保留了早期增益的自然量级，显著加速了收敛。
---

# Stepwise Credit Assignment for GRPO on Flow-Matching Models

> [!tip] 核心洞察
> 利用中间奖励估计将全局信用分解为每步的边际贡献，使强化学习策略能够感知扩散过程的时间层次，重点优化对最终质量影响大的早期步骤，从而提高样本效率和收敛速度。

| 字段 | 内容 |
|------|------|
| 中文题名 | 流匹配模型中GRPO的逐步信用分配方法 |
| 英文题名 | Stepwise Credit Assignment for GRPO on Flow-Matching Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.28718) · [Project](https://stepwiseflowgrpo.com) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Stepwise-Flow-GRPO |
| Dataset | GenEval, Multiple, UnifiedReward-7B on GenEval, OCR Text Rendering |

> [!tip] 效果简介
> - GenEval (PickScore reward, cfg=4.5) 上，Overall Accuracy 0.71 vs 0.68 (Flow-GRPO) (+0.03)。
> - GenEval (Extended Training, 400 GPU hrs) 上，Overall Accuracy 0.87 vs 0.72 (Flow-GRPO) (+0.15)。
> - Multiple (GenEval & PickScore datasets, 3 reward functions) 上，Training Reward per Iteration Consistently higher and faster convergence across all settings vs Flow-GRPO (N/A (visual))。

## 概述

流匹配（Flow Matching）模型在文本到图像生成中展现出竞争力，但其强化学习微调方法 **Flow-GRPO**（Liu et al., 2024）存在一个关键瓶颈：**统一信用分配**。Flow-GRPO 将最终图像的标量奖励均匀地分配给所有去噪步骤，忽略了扩散生成过程固有的时间层次结构——早期步骤决定构图与布局，后期步骤细化纹理细节。这种统一分配可能奖励早期错误，或无法给予关键步骤足够的强化信号。

本文提出 **Stepwise-Flow-GRPO**，核心洞察是：利用中间奖励估计将全局信用分解为每步的**边际贡献**（逐步增益 $g_t^i = r_{t-1}^i - r_t^i$），使强化学习策略能够感知扩散过程的时间层次，重点优化对最终质量影响大的早期步骤。具体而言，方法通过 Tweedie 公式从中间噪声状态估计清洁图像并计算奖励，将逐步增益经联合归一化后转化为组相对优势，用于 GRPO 策略更新；同时引入 DDIM 启发式 SDE 以在保持探索的同时生成更清洁的样本。

主要结果：
- **样本效率与收敛速度**：在 PickScore、ImageReward、UnifiedReward 等不同奖励函数及数据集上，Stepwise-Flow-GRPO 的训练奖励与收敛速度均一致优于 Flow-GRPO（Figure 4），且壁钟效率更高（Figure 5）。
- **扩展训练性能**：经过 400 GPU 小时扩展训练后，Stepwise-Flow-GRPO 在 GenEval 基准上达到 **0.87** 总分，显著优于 Flow-GRPO（0.72），甚至超过 GPT-4o（0.84）（Table 3）。
- **训练稳定性**：在 UnifiedReward 等具有挑战性的奖励函数下，Stepwise-Flow-GRPO 可稳定训练，而 Flow-GRPO 发散（Figure 13）。
- **关键设计验证**：联合归一化保留了早期增益的自然量级，显著加速收敛（Figure 9）；方法对中间估计的去噪子步数具有鲁棒性（Figure 10）。

方法定位：Stepwise-Flow-GRPO 属于**扩散模型强化学习微调**范畴，通过**逐步信用分配**改进 GRPO 框架，与基于最终奖励的统一分配方法形成对比。其信用分配策略独立于采样改进，两者互补（Figure 6）。

## 背景与动机

### 流匹配与强化微调

流匹配模型（Flow-Matching Models）通过学习连续时间归一化流来生成高质量图像，其核心训练目标为最小化预测速度场与真实速度场之间的均方误差：

$$\mathcal{L}(\theta) = \mathbb{E}_{t, x_0, x_1} \left[ \| \dot{x}_t - v_\theta(x_t, t, c) \|^2 \right]$$

这类模型通常使用确定性常微分方程（ODE）进行采样，生成过程可逆且高效。然而，预训练的流匹配模型在组合性生成、属性绑定和空间推理等任务上仍存在不足，难以直接满足人类偏好。

为将强化学习引入流匹配微调，**Flow-GRPO**（Liu et al., 2024）提出将确定性ODE转换为保持边缘分布的随机微分方程（SDE）：

$$d x_t = \left[ v_t(x_t) \pm \frac{\sigma_t^2}{2t} \hat{x}_1 \right] dt + \sigma_t dw_t$$

这一转换使采样过程具备随机探索能力，从而可以应用组相对策略优化（Group Relative Policy Optimization, GRPO）进行端到端的奖励驱动微调。

### 统一信用分配的核心缺陷

Flow-GRPO的奖励机制存在一个关键的结构性盲点：**它仅对最终生成的图像计算奖励，并将该全局奖励统一分配给所有去噪步骤**。具体而言，对于同一提示词下的$N$条生成轨迹，Flow-GRPO基于最终奖励进行组内标准化，计算统一的组相对优势$A_i$，所有步骤共享同一优势信号。

这种统一分配策略忽略了扩散生成过程的**时间层次结构**。从频域角度理解，扩散过程遵循从低频到高频的生成顺序——早期步骤（高噪声水平）决定图像的全局构图与布局，后期步骤（低噪声水平）细化纹理细节。频域信噪比的理论分析表明：

$$\mathrm{SNR}_t(k) = \left( \frac{1-t}{t} \right)^2 \frac{1}{|k|^\alpha}$$

其中$t$越接近0（早期步骤），低频成分的信噪比越高；$t$越接近1（后期步骤），高频细节逐渐显现。这一时间结构意味着不同步骤对最终生成质量的贡献存在本质差异。

统一信用分配带来的问题体现在两个层面：

1. **奖励非单调性**：如图1所示，两条针对同一提示词的生成轨迹展现出截然不同的奖励演化路径。一条轨迹在中间步骤获得高奖励后下降，另一条则持续改善。统一分配无法区分这些差异，可能奖励导致最终质量下降的早期错误决策，或无法给予关键转折步骤足够的强化信号。

2. **增益量级失衡**：实证分析（图2）表明，早期步骤的平均增益量级$\mathbb{E}_i[|g_t^i|]$显著大于后期步骤。这意味着构图决策驱动了大部分奖励改进，而统一信用分配完全忽视了这一现象，导致优化效率低下。

### 本文动机与解决思路

针对上述问题，本文提出**Stepwise-Flow-GRPO**，核心思想是**利用中间奖励估计将全局信用分解为每步的边际贡献**。具体而言：

- 使用**Tweedie公式**从中间噪声状态$x_t$估计清洁图像$\hat{x}_0(t) := \mathbb{E}[x_0 | x_t]$，并调用奖励模型计算中间奖励$r_t$；
- 定义**逐步增益**$g_t = r_{t-1} - r_t$，衡量每个去噪步骤对奖励的边际改进；
- 基于逐步增益计算每步的独立优势信号，使强化学习策略能够感知扩散过程的时间层次，重点优化对最终质量影响大的早期步骤。

这一设计旨在实现两个目标：**提高样本效率**（更少的训练迭代即可收敛）和**加速收敛速度**（在壁钟时间上更快达到更优性能）。同时，本文还引入受DDIM启发的改进SDE采样器，在保持随机探索的同时生成更清洁的中间样本，进一步提升信用分配的质量。

## 核心创新

Stepwise-Flow-GRPO 的核心创新在于将扩散生成过程的**时间层次结构**显式编码到强化学习的信用分配机制中，解决了 Flow-GRPO 中统一奖励信号无法区分不同去噪步骤贡献的根本缺陷。

### 问题诊断：统一信用分配的结构性盲区

Flow-GRPO 对所有去噪步骤使用相同的最终图像奖励计算组相对优势，这一设计隐含假设每一步对最终质量的贡献是均等的。然而，扩散生成过程具有内在的频率层次结构——频域信噪比
$$\mathrm{SNR}_t(k) = \left( \frac{1-t}{t} \right)^2 \frac{1}{|k|^\alpha}$$
表明低频成分（决定构图与布局）在早期步骤中率先涌现，而高频纹理细节在后期才逐步清晰。统一信用分配因此产生两类系统性错误：（1）**奖励早期错误**——若某轨迹在 $t \approx 1$ 时做出错误决策（如物体颜色错误），但后续步骤将其纠正，最终高奖励会无差别地强化所有步骤，包括早期错误；（2）**低估关键步骤**——对最终质量影响最大的构图决策步骤无法获得与其贡献匹配的强化信号。

实证证据（Figure 2）直接验证了这一诊断：在 256 个 GenEval 提示词上使用 PickScore 测量各步骤的平均绝对增益 $\mathbb{E}_i[|g_t^i|]$，早期步骤的增益量级显著更大，表明构图决策驱动了大部分奖励改进，而统一信用分配完全忽略了这一现象。

### 核心机制：逐步增益与边际信用分解

Stepwise-Flow-GRPO 的核心操作是将全局奖励分解为每步的**边际贡献**。具体而言，定义逐步增益
$$g_t^i = r_{t-1}^i - r_t^i$$
该值衡量第 $t$ 步对奖励的边际改进：正值表示该步骤提升了图像质量，应被奖励；负值表示该步骤降低了质量，应被惩罚。这一分解的关键前提是能够获得中间步骤的奖励估计 $r_t^i$——论文利用 Tweedie 公式
$$\hat{x}_0(t) := \mathbb{E}[x_0 | x_t] = x_t - t \hat{x}_1$$
从每个带噪状态 $x_t$ 一步预测清洁图像，再通过多步 ODE（$T'=5$ 子步）精炼后调用奖励模型计算 $r_t^i = R(\hat{x}_0(t), c)$。

### 优势计算：联合归一化保留时间结构

将增益转换为策略梯度所需的优势信号时，归一化策略的选择至关重要。逐步归一化（每步独立计算均值和标准差）会抹除早期步骤增益量级自然较大的时间结构信息。Stepwise-Flow-GRPO 采用**联合归一化**——对所有 $N \times T$ 个增益计算全局均值和标准差：
$$\tilde{A}_t^i = \frac{g_t^i - \text{mean}}{\text{std}}, \quad \text{mean} = \frac{1}{NT} \sum_{j,k} g_k^j$$
联合归一化保留了早期增益的量级优势，使优化过程能够自然聚焦于对最终质量影响更大的早期步骤。消融实验（Figure 9）表明，联合归一化在所有步骤和轨迹上均显著优于逐步归一化，收敛速度明显加快。

### 互补改进：DDIM 启发式 SDE 采样器

除信用分配外，论文还引入了一项互补改进——受 DDIM 启发的 SDE 采样器。原始 Flow-GRPO SDE 虽能保留边缘分布以提供探索，但产生的样本噪声较大，不利于奖励模型准确评估。改进后的采样规则
$$x_{t-\Delta t} = \left(1 - (t - \Delta t)\right) \hat{x}_0(t) + \sqrt{(t - \Delta t)^2 - \sigma_t^2} \hat{x}_1 + \sigma_t \epsilon$$
使用方差保持的噪声调度 $\sigma_t = \eta (t-\Delta t)\sqrt{1-t}$，在保持随机探索的同时生成更清洁的样本。当 $\sigma_t = 0$ 时，该规则退化为确定性 ODE。实验（Figure 6）表明，当两个方法均使用改进 SDE 时，Stepwise-Flow-GRPO 仍保持样本效率优势，证明信用分配改进与采样改进是**互补而非重叠**的。

### 与基线的 changed slots 总结

| 组件 | Flow-GRPO（基线） | Stepwise-Flow-GRPO（本文） |
|------|-------------------|---------------------------|
| 信用分配 | 基于最终奖励的统一组相对优势 $A_i$ | 基于逐步增益 $g_t^i = r_{t-1}^i - r_t^i$ 的每步优势 $\tilde{A}_t^i$ |
| 中间奖励估计 | 无 | Tweedie 公式 + 多步 ODE 从 $x_t$ 估计 $\hat{x}_0(t)$ |
| 优势归一化 | 组内 $N$ 个最终奖励标准化 | 全部 $N \times T$ 个增益联合标准化，保留早期量级优势 |
| 采样过程 | 原始 Flow-GRPO SDE（导数噪声大） | DDIM 启发式 SDE，方差保持噪声调度，样本更清洁 |

## 整体框架

Stepwise-Flow-GRPO 的核心思想是将全局奖励信号按时间维度分解为每个去噪步骤的边际贡献，从而让强化学习策略感知扩散过程的层次化生成结构。整体框架由五个关键模块串联而成，形成“采样—估计—增益计算—优势转换—策略更新”的闭环。

**输入**：一个文本提示 $c$，一个预训练的流匹配模型 $v_\theta$（骨干为 SD3.5-Medium），以及一个可微或不可微的奖励模型 $R$（如 PickScore、ImageReward、UnifiedReward）。

**Pipeline 流程**：

1. **DDIM 启发式 SDE 采样器**：从纯噪声 $x_1 \sim \mathcal{N}(0, I)$ 出发，使用受 DDIM 启发的随机微分方程（Eq. 8）沿时间轴反向采样，生成 $T=10$ 个离散步骤的轨迹 $\{x_t^i\}_{t=1}^{0}$。该采样器在保留策略梯度所需随机探索的同时，产生比原始 Flow-GRPO SDE（Eq. 1）更清洁的中间样本，为后续奖励估计提供更可靠的输入。方差保持的噪声调度 $\sigma_t = \eta (t-\Delta t)\sqrt{1-t}$ 确保探索幅度随去噪进程自适应衰减。

2. **中间奖励估计模块**：对轨迹中每个带噪状态 $x_t^i$，利用 Tweedie 公式 $\hat{x}_0(t) := \mathbb{E}[x_0 | x_t] = x_t - t \hat{x}_1$ 一步预测对应的清洁图像，再通过一个 $T'=5$ 步的确定性 ODE 进一步精炼该估计，最终调用奖励模型计算中间奖励 $r_t^i = R(\hat{x}_0^i(t), c)$。这一模块将原本仅在最终图像上评估的奖励信号扩展为覆盖整个生成过程的时间序列 $\{r_t^i\}_{t=0}^{T}$。

3. **逐步增益计算**：对每个轨迹计算相邻步骤的奖励差分 $g_t^i = r_{t-1}^i - r_t^i$，衡量第 $t$ 步对最终奖励的边际改进。正值表示该步骤提升了图像质量，负值表示该步骤引入了退化。这一设计直接回应了统一信用分配的核心缺陷——早期步骤决定构图与布局，其增益量级显著大于后期纹理细化步骤（Figure 2），而 Flow-GRPO 的全局奖励无法区分这种时间层次。

4. **增益优势转换与联合归一化**：将所有 $N$ 条轨迹、$T$ 个步骤的增益集合 $\{g_t^i\}$ 进行联合标准化，计算组相对优势 $\tilde{A}_t^i = \frac{g_t^i - \text{mean}}{\text{std}}$，其中 mean 和 std 是全局均值和标准差。相比逐步骤独立归一化，联合归一化保留了早期步骤增益的自然量级优势，使优化过程能够聚焦于对最终质量影响最大的构图决策阶段（Figure 9）。

5. **GRPO 策略更新**：将逐步优势 $\tilde{A}_t^i$ 代入 PPO 风格的剪切目标函数，同时加入 KL 散度正则化项约束策略偏离参考模型的程度：
   $$J(\theta) = \frac{1}{NT} \sum_{i=1}^N \sum_{t=0}^{T-1} \left[ \ell(\rho_t^i(\theta), \tilde{A}_t^i) - \beta D_{\mathrm{KL}}^{i,t}(\pi_\theta || \pi_{\mathrm{ref}}) \right]$$
   其中 $\rho_t^i(\theta)$ 为当前策略与旧策略的概率比，$\ell$ 为剪切函数。梯度反向传播更新流匹配模型的速度场参数 $\theta$。

**输出**：经过强化学习微调的流匹配模型，在保持生成多样性的同时，显著提升了对齐奖励信号的样本效率与收敛速度。

**模块间关系**：中间奖励估计模块是逐步增益计算的前提，其准确性直接影响信用分配的质量；DDIM 启发式 SDE 采样器与信用分配策略相互独立但互补——当两个方法同时使用改进 SDE 时，Stepwise-Flow-GRPO 仍保持样本效率优势（Figure 6），表明增益来自信用分配机制的改进而非单纯的采样质量提升；联合归一化作为优势计算的最后一步，决定了不同时间步骤的相对优化权重，是保留扩散过程时间结构的关键设计选择。

## 核心模块与公式推导

### 问题形式化：流匹配与统一信用分配的局限

流匹配模型通过最小化速度场预测误差来学习连续时间归一化流：

$$
\mathcal{L}(\theta) = \mathbb{E}_{t, x_0, x_1} \left[ \| \dot{x}_t - v_\theta(x_t, t, c) \|^2 \right]
$$

其中 $x_t = (1-t)x_0 + t x_1$ 沿线性路径插值，$\dot{x}_t = x_1 - x_0$ 为真实速度。Flow-GRPO 将此确定性 ODE 转化为随机微分方程以引入探索：

$$
d x_t = \left[ v_t(x_t) \pm \frac{\sigma_t^2}{2t} \hat{x}_1 \right] dt + \sigma_t dw_t
$$

该 SDE 保留了原始 ODE 的边缘分布，但策略梯度仅依赖最终图像奖励 $R(\hat{x}_0(T), c)$ 计算组相对优势，导致**瓶颈**：对所有去噪步骤施加统一信用，忽略了扩散过程的时间层次结构。频域信噪比揭示了这一结构的物理本质：

$$
\mathrm{SNR}_t(k) = \left( \frac{1-t}{t} \right)^2 \frac{1}{|k|^\alpha}
$$

低频成分（构图、布局）在早期步骤（$t \to 1$）即获得高 SNR 并率先涌现，高频纹理在后期逐步细化。统一信用分配将决定布局的关键步骤与锐化边缘的微小调整等同视之，甚至可能奖励早期错误（如错误物体颜色）——只要后续步骤将其纠正。

### 核心模块一：中间奖励估计

Stepwise-Flow-GRPO 的核心创新在于为每个去噪步骤 $t$ 估计中间奖励 $r_t^i$。利用 Tweedie 公式从带噪状态 $x_t$ 一步预测清洁图像：

$$
\hat{x}_0(t) := \mathbb{E}[x_0 | x_t] = x_t - t \hat{x}_1
$$

其中 $\hat{x}_1 = v_\theta(x_t, t, c)$ 为模型预测的速度场。为获得更准确的奖励估计，论文采用一个短确定性 ODE 轨迹（$T'=5$ 子步）从 $x_t$ 进一步去噪，得到 $\hat{x}_0^i(t)$ 后调用奖励模型 $R(\cdot, c)$ 计算 $r_t^i$。消融实验表明该方法对 $T' \in \{2,5,8\}$ 具有鲁棒性（Figure 10）。

![[assets/figures/papers/paper_list_l2703_https_arxiv_org_abs_2603_28718/figures/016_Figure_10.jpg]]
*Figure 10: Stepwise-Flow-GRPO is robust to the number of denoising substeps. Reward vs. training iteration (top) and GPU Hours (bottom) for different numbers of substeps*

### 核心模块二：逐步增益与联合归一化优势

定义**逐步增益**为相邻步骤奖励的边际改进：

$$
g_t^i = r_{t-1}^i - r_t^i
$$

$g_t^i > 0$ 表示该步骤提升了奖励，应被强化；$g_t^i < 0$ 表示该步骤损害了奖励，应被惩罚。实证分析（Figure 2）显示早期步骤的平均增益量级显著更大，验证了构图决策驱动大部分奖励改进的假设。

![[assets/figures/papers/paper_list_l2703_https_arxiv_org_abs_2603_28718/figures/003_Figure_2.jpg]]
*Figure 2: Gain magnitudes across steps. Mean absolute gain*

为保留这一自然量级差异，采用**联合归一化**计算组相对优势：

$$
\tilde{A}_t^i = \frac{g_t^i - \text{mean}}{\text{std}}, \quad \text{mean} = \frac{1}{NT} \sum_{j,k} g_k^j
$$

其中均值和标准差在所有 $N$ 条轨迹和 $T$ 个步骤上联合计算。消融实验（Figure 9）证明联合归一化相比逐步归一化（每步独立标准化）显著加速收敛，因为它保留了早期增益的天然量级优势，使优化能聚焦于信息量更大的早期步骤。

![[assets/figures/papers/paper_list_l2703_https_arxiv_org_abs_2603_28718/figures/015_Figure_9.jpg]]
*Figure 9: Joint normalization preserves temporal structure and accelerates convergence. Reward vs. training iteration comparing joint normalization (global mean/std across all steps and trajectories) against per-step normalization (separate mean/std for each step)*

### 核心模块三：逐步策略梯度目标

将逐步优势融入 GRPO 框架，得到每步的策略梯度目标：

$$
J(\theta) = \frac{1}{NT} \sum_{i=1}^N \sum_{t=0}^{T-1} \left[ \ell(\rho_t^i(\theta), \tilde{A}_t^i) - \beta D_{\mathrm{KL}}^{i,t}(\pi_\theta || \pi_{\mathrm{ref}}) \right]
$$

其中 $\rho_t^i(\theta) = \frac{\pi_\theta(x_{t-\Delta t}^i | x_t^i, c)}{\pi_{\text{old}}(x_{t-\Delta t}^i | x_t^i, c)}$ 为概率比，$\ell$ 为 PPO 风格的剪切损失，$\beta$ 控制 KL 散度正则化强度。该目标将 GRPO 从轨迹级信用分配自然扩展到逐步信用分配。

### 核心模块四：DDIM 启发式 SDE 采样器

为在保持随机探索的同时生成更清洁的样本用于奖励评估，论文采用受 DDIM 启发的采样规则：

$$
x_{t-\Delta t} = \left(1 - (t - \Delta t)\right) \hat{x}_0(t) + \sqrt{(t - \Delta t)^2 - \sigma_t^2} \hat{x}_1 + \sigma_t \epsilon
$$

其中 $\sigma_t = \eta (t-\Delta t) \sqrt{1-t}$ 采用方差保持的噪声调度，$\epsilon \sim \mathcal{N}(0, I)$。当 $\sigma_t = 0$ 时退化为确定性 ODE。该模块与逐步信用分配相互独立——当两个方法均使用此 SDE 时，Stepwise-Flow-GRPO 仍保持样本效率优势（Figure 6），证明信用分配改进与采样改进是互补的。

### 补充图表

![[assets/figures/papers/paper_list_l2703_https_arxiv_org_abs_2603_28718/figures/012_Figure_7.jpg]]
*Figure 7: Design variation comparison. Reward vs. training iteration for different formulations of stepwise credit assignment on GenEval with PickScore reward. The standard gain formulation from the main paper matches all alternatives, demonstrating that preserving the natural temporal structure of diffusion gains is the most effective credit assignment*

## 实验与分析

### 核心瓶颈与动机验证

本文的核心假设是：流匹配的生成过程具有明确的时间层次——早期步骤决定构图与布局，后期步骤细化纹理细节——但Flow-GRPO的统一信用分配完全忽略了这一结构。Figure 2 提供了关键实证：在256个GenEval提示上使用PickScore测量各步骤的平均绝对增益 $\mathbb{E}_i[|g_t^i|]$，早期步骤的增益量级显著更大，表明构图决策驱动了大部分奖励改进。统一信用分配的两个具体失败模式在Section 4中被明确识别：(1) 它可能奖励早期错误（例如错误的对象颜色），只要后续步骤纠正了这些错误；(2) 它无法给予关键早期步骤足够的强化信号，导致优化效率低下。频域信噪比分析 $\mathrm{SNR}_t(k) = \left(\frac{1-t}{t}\right)^2 \frac{1}{|k|^\alpha}$ 从理论上解释了这一现象：低频（构图）在早期 $t$ 具有更高SNR，因此更早从噪声中浮现。

### 主要实验结果

**样本效率与收敛速度。** Figure 4 展示了在不同奖励函数（PickScore、ImageReward、UnifiedReward）和数据集（GenEval、PickScore prompts）上的训练奖励曲线。Stepwise-Flow-GRPO在所有设置下均一致优于Flow-GRPO，在4个设置中的3个达到了更高的最终性能。Figure 5 进一步验证了壁钟效率：尽管每训练迭代的生成时间约为Flow-GRPO的1.8-2.4倍（Table 2），但由于更少的迭代次数即可收敛，壁钟时间总体更快（大多数设置下快20-40%）。

**GenEval基准评估。** Table 1 报告了在GenEval上的组合生成性能。在cfg=4.5设置下，Stepwise-Flow-GRPO达到0.71总分，优于Flow-GRPO的0.68（+0.03），在多个子任务上表现更优。经过400 GPU小时扩展训练后（Figure 12），Stepwise-Flow-GRPO达到0.87总分，显著优于Flow-GRPO的0.72（+0.15），甚至超过GPT-4o的0.84。Table 3 的完整数据显示，这一性能差距随着训练时间扩大而持续拉大。

**训练稳定性。** 在使用UnifiedReward-7B作为奖励模型时（Figure 13），Flow-GRPO搭配标准SDE出现发散，而Stepwise-Flow-GRPO稳定训练，60 GPU小时后达到0.74 GenEval分数。在OCR文本渲染任务中（Figure 11），使用80% OCR + 20% PickScore的组合奖励，Flow-GRPO在约500步后发散，而Stepwise-Flow-GRPO持续改进并达到更高平台。

**定性结果。** Figure 3 展示了Stepwise-Flow-GRPO在空间推理、属性绑定和计数性能上的定性优势。Figure 15和Figure 16的扩展定性比较进一步显示，在训练步骤60时差距最为明显，本文方法展现出更好的计数准确性、更合理的构图和更高的图像质量。

### 消融实验

**联合归一化 vs. 逐步归一化。** Figure 9 对比了联合归一化（所有步骤和轨迹共享统计量）与逐步归一化（每步独立标准化）的收敛速度。联合归一化保留了早期增益的自然量级，使优化能够聚焦于量级更大的早期步骤，显著加速了收敛。这一结果支持了核心设计选择：标准化方式直接影响模型对时间层次结构的感知能力。

**中间估计的鲁棒性。** Figure 10 显示，去噪子步数 $T' \in \{2, 5, 8\}$ 对最终性能影响很小，方法对该超参数具有鲁棒性。这降低了实际部署中的调参负担。

**增益公式设计选择。** Figure 7 比较了标准增益公式 $g_t^i = r_{t-1}^i - r_t^i$ 与EMA基线、GAE和ODE蒸馏等替代设计。标准公式性能相当或更优，验证了其作为最有效设计选择的地位。

**信用分配与采样改进的互补性。** Figure 6 展示了当两个方法均使用DDIM启发式SDE（Section 5.5）时的训练曲线。Stepwise-Flow-GRPO仍然保持样本效率优势，表明信用分配改进独立于采样改进，两者是互补的优化方向。

### 计算开销与公平性

Table 2 提供了每训练迭代的时间分解。Stepwise-Flow-GRPO的主要额外开销来自中间奖励估计（需对每个 $x_t$ 运行多步ODE并调用奖励模型），导致生成时间约为Flow-GRPO的1.8-2.4倍。然而，由于样本效率的提升，壁钟时间总体更快。所有实验均在SD3.5-Medium骨干模型上、使用8张NVIDIA A100 GPU进行，两个方法在相同的离散时间步（T=10）、批尺寸和优化器设置下公平比较。对于UnifiedReward等重模型，使用额外GPU分离服务以公平计时。

![[assets/figures/papers/paper_list_l2703_https_arxiv_org_abs_2603_28718/figures/017_Table_2.jpg]]
*Table 2: Per-iteration timing breakdown in seconds per training iteration, averaged over multiple runs*

### 失败模式与局限性

尽管Stepwise-Flow-GRPO在多数设置下表现优异，仍需注意以下局限：(1) 当使用大型VLM奖励模型（如7B UnifiedReward）时，中间奖励估计的计算成本显著增加；(2) 仅在SD3.5-Medium和10步去噪设置下验证，尚未测试更少步骤或更大模型（如SDXL、Flux）的效果；(3) 逐步奖励估计依赖Tweedie公式和多步ODE的准确性，在极端噪声水平下可能引入系统偏差；(4) 目前仅最大化单一标量奖励，未明确处理多个质量指标（如保真度与语义对齐）之间的潜在权衡；(5) 未探索长期RLHF训练中的遗忘问题。

### 补充图表

![[assets/figures/papers/paper_list_l2703_https_arxiv_org_abs_2603_28718/figures/008_Figure_4.jpg]]
*Figure 4: Sample efficiency across reward functions. Stepwise-Flow-GRPO consistently outperforms Flow-GRPO in reward per training step across all settings, achieving both faster convergence and superior final performance in 3 out of 4 settings*

![[assets/figures/papers/paper_list_l2703_https_arxiv_org_abs_2603_28718/figures/010_Figure_5.jpg]]
*Figure 5: Wall-clock efficiency matches sample efficiency gains. Reward versus wall-clock time for the same settings as Fig. 4. Despite additional computational cost for intermediate denoising, Stepwise-Flow-GRPO converges faster in wall-clock time, achieving visibly superior performance in 3 out of 4 settings*

![[assets/figures/papers/paper_list_l2703_https_arxiv_org_abs_2603_28718/figures/011_Table_1.jpg]]
*Table 1: Final model quality on GenEval. Compositional generation performance for models trained with PickScore reward. Both methods substantially improve over the base model, with our method matching Flow-GRPO at cfg=1.0 and outperforming it across most categories at cfg=4.5, particularly in counting and spatial positioning*

![[assets/figures/papers/paper_list_l2703_https_arxiv_org_abs_2603_28718/figures/019_Figure_12.jpg]]
*Figure 12: Extended GenEval training. GenEval overall score vs. wall-clock time for 400 GPU hour runs. Stepwise-Flow-GRPO achieves 0.87, substantially outperforming Flow-GRPO (0.72) and approaching state-of-the-art autoregressive models. The widening performance gap demonstrates that stepwise credit assignment provides increasing benefits at high performance levels*

![[assets/figures/papers/paper_list_l2703_https_arxiv_org_abs_2603_28718/figures/020_Figure_13.jpg]]
*Figure 13: UnifiedReward training. Reward vs. wall-clock time for 60 GPU hour run on GenEval using UnifiedReward-7b-v1.5. Stepwise-Flow-GRPO trains stably while Flow-GRPO diverges with this reward function, demonstrating superior robustness with complex VLM-based rewards*

![[assets/figures/papers/paper_list_l2703_https_arxiv_org_abs_2603_28718/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative results. We compare our Stepwise-Flow-GRPO with Flow-GRPO and observe better spatial reasoning, attribute binding, and counting performance*

![[assets/figures/papers/paper_list_l2703_https_arxiv_org_abs_2603_28718/figures/009_Figure_6.jpg]]
*Figure 6: Stepwise credit assignment remains effective with improved SDE. Reward versus training step when both methods use the DDIM-inspired SDE from Sec. 5.5. Stepwise-Flow-GRPO retains its sample efficiency advantage, demonstrating that the improvements in credit assignment and sampling are complementary*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

**Stepwise-Flow-GRPO** 建立在 **Flow-GRPO**（Liu et al., 2024）的基础上，后者首次将组相对策略优化（GRPO）引入流匹配模型的微调。Flow-GRPO 的核心贡献是将流匹配的确定性 ODE 转化为具有匹配边缘分布的随机微分方程（SDE），从而为策略梯度提供探索能力。然而，其信用分配机制存在一个关键瓶颈：仅基于最终生成图像的奖励计算统一的组相对优势 $A_i$，完全忽略了扩散生成过程的时间层次结构。

本文的根本改进在于将全局信用分配**分解为逐步信用分配**。具体而言，Flow-GRPO 对所有去噪步骤赋予相同的权重，而 Stepwise-Flow-GRPO 通过引入逐步增益 $g_t^i = r_{t-1}^i - r_t^i$，使每个步骤获得与其对奖励的边际改进成正比的信用。这一改变直接回应了频域分析所揭示的现象——早期步骤（高 $t$ 值）决定图像的构图与布局，后期步骤仅细化纹理细节，但统一信用分配无法区分这两类贡献的质与量。

在采样策略上，本文进一步引入了受 **DDIM**（Song et al., ICLR 2021）启发的 SDE 采样器。原始的 Flow-GRPO SDE 虽能保持边缘分布，但产生的样本噪声较大，不利于奖励模型的准确评估。新的采样规则在保留策略梯度所需随机探索的同时，生成更清洁的中间样本，且当噪声项 $\sigma_t = 0$ 时自然退化为确定性 ODE。消融实验表明，当两个方法均使用改进的 SDE 时，Stepwise-Flow-GRPO 仍然保持样本效率优势，证明信用分配改进与采样改进是**互补的独立贡献**。

### 2. 方法适用边界

**已验证的适用条件：**
- **骨干模型**：SD3.5-Medium（流匹配架构），10 步去噪设置（$T=10$）。
- **奖励函数**：PickScore、ImageReward、UnifiedReward-7B 等标量奖励模型均表现出一致的优势。
- **评估基准**：GenEval 组合生成基准、PickScore 数据集、OCR 文本渲染任务。
- **训练规模**：从数十 GPU 小时到 400 GPU 小时的扩展训练均保持稳定。

**未验证的边界（需谨慎外推）：**
- 更少去噪步骤（如 $T=5$ 或更少）下，中间奖励估计的准确性可能下降，影响信用分配质量。
- 更大规模模型（如 SDXL、Flux）上的效果尚未测试，方法是否随模型容量扩展而保持优势未知。
- 多维度奖励信号（如保真度与语义对齐的显式权衡）下，单一标量增益是否足以捕捉复杂的质量结构尚无证据。

### 3. 局限性与已知问题

**计算开销：** 每训练迭代的生成时间约为 Flow-GRPO 的 1.8–2.4 倍，主要源于中间奖励估计需要额外的去噪子步骤（$T'=5$）。当使用大型 VLM 奖励模型（如 7B 参数的 UnifiedReward）时，这一开销进一步放大。不过，由于所需训练迭代次数显著减少，壁钟时间总体更快（多数设置下快 20–40%）。

**中间估计偏差：** 逐步奖励估计依赖 Tweedie 公式和多步 ODE 从带噪状态 $\hat{x}_0(t)$ 恢复清洁图像。在极端噪声水平（$t$ 接近 1）下，该估计可能引入系统偏差，导致早期步骤的增益信号不够可靠。消融实验显示方法对去噪子步数 $T'$ 具有鲁棒性，但未系统分析不同噪声水平下的估计误差分布。

**遗忘问题未探索：** 长期 RLHF 训练可能导致模型遗忘原有的生成能力。本文未设置保留预训练分布的约束或评估遗忘程度，这在实际部署中是重要考量。

**单一奖励信号：** 方法目前仅最大化一个标量奖励，未显式处理多个质量维度（如保真度、多样性、语义对齐）之间的潜在权衡。在多目标场景下，逐步信用分配是否能有效区分不同维度的贡献仍是开放问题。

### 4. 开放问题

1. **课程学习与自适应加权：** 能否利用每个提示的增益方差作为难度指标，实现自动课程学习？是否可以对步骤进行自适应加权，将优化集中在增益方差大的信息丰富区域？

2. **自我纠正机制：** 能否让模型在生成过程中检测到不好的中间状态（负增益），并主动重试或回溯，实现类似推理模型的自我纠正能力？

3. **跨模态与跨范式推广：** 该方法如何推广到其他生成范例（如视频生成中的时序扩散、3D 生成中的多视图扩散）？在更基础的政策梯度方法（如 PPO、REINFORCE）中，逐步信用分配是否同样有效？

4. **多维度奖励分解：** 在组合式外部环境或多维度人类反馈下，逐步信用分配的收益是否持续？能否将增益向量化以分别追踪不同质量维度的贡献？

5. **与对抗训练的结合：** 逐步信用分配本质上提供了更细粒度的训练信号，是否可与对抗性奖励模型或判别器结合，进一步提升生成质量的上限？

## 原文 PDF

![[paperPDFs/CVPR_2026/Stepwise_Credit_Assignment_for_GRPO_on_Flow_Matching_Models.pdf]]