---
title: "dMLLM-TTS: Self-Verified and Efficient Test-Time Scaling for Diffusion Multi-Modal Large Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/dMLLM_TTS_Self_Verified_and_Efficient_Test_Time_Scaling_for_Diffusion_Multi_Modal_Large_Language_Models.pdf
project_link: null
code_link: "https://github.com/Alpha-VLLM/Lumina-DiMOO"
aliases:
- DT
- dMLLM-TTS
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 自验证反馈（SVF）引导的分层轨迹搜索（HTS），通过自适应计算分配将复杂度从 O(NT) 降至 O(N+T)，并消除外部验证器。
primary_logic: 利用dMLLM内在的图像理解能力实现自验证反馈，并通过分层搜索在早期粗生成阶段修剪低潜力轨迹，将计算资源集中在高潜力轨迹的精细优化上，从而高效提升图文对齐质量。
claims:
- dMLLM-TTS 在 GenEval 基准上显著提升三个代表 dMLLM 的生成质量。
- 分层轨迹搜索（HTS）实现近线性复杂度，效率最高可达线性搜索的6倍。
- 自验证反馈（SVF）复用模型自身理解能力评估生成图像，排除了外部验证器。
- HTS 通过自适应修剪和几何衰减调度，理论计算成本可近似为 O(N+T)。
---

# dMLLM-TTS: Self-Verified and Efficient Test-Time Scaling for Diffusion Multi-Modal Large Language Models

> [!tip] 核心洞察
> 利用dMLLM内在的图像理解能力实现自验证反馈，并通过分层搜索在早期粗生成阶段修剪低潜力轨迹，将计算资源集中在高潜力轨迹的精细优化上，从而高效提升图文对齐质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | dMLLM-TTS：扩散多模态大语言模型的自验证高效测试时扩展 |
| 英文题名 | dMLLM-TTS: Self-Verified and Efficient Test-Time Scaling for Diffusion Multi-Modal Large Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.19433) · [Code](https://github.com/Alpha-VLLM/Lumina-DiMOO) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | dMLLM-TTS |
| Dataset | GenEval |

> [!tip] 效果简介
> - GenEval 上，Overall (平均准确率) 0.92 (Lumina-DiMOO + dMLLM-TTS HTS, N=32, T=32, K=8) vs 0.78 (Lumina-DiMOO, 无 TTS, N=1, T=8) (+17.9%)；Overall 0.66 (MMaDA + dMLLM-TTS HTS) vs 0.51 (MMaDA, 无 TTS) (+29.4%)；Overall 0.67 (Muddit + dMLLM-TTS HTS) vs 0.53 (Muddit, 无 TTS) (+26.4%)。
> - GenEval (效率对比) 上，推理速度提升 HTS 比 LTS 快 5×（Lumina-DiMOO）、6×（MMaDA、Muddit） vs 线性搜索（LTS） (5× - 6×)。

## 概述

扩散多模态大语言模型（dMLLMs）在文本到图像生成中展现出潜力，但其测试时计算扩展（Test-Time Scaling, TTS）面临两个核心瓶颈：**线性搜索策略导致 O(NT) 的高昂计算成本**，以及**依赖外部验证器带来的额外资源开销**。针对这些问题，本文提出 **dMLLM-TTS** 框架，通过两个关键机制实现高效且自验证的测试时扩展：

1. **自验证反馈（Self-Verified Feedback, SVF）**：复用 dMLLM 内在的多模态理解能力，以模型输出“是”的 logit 概率作为图文对齐分数，从而消除对外部验证器（如 **VILA-Judge**（Xie et al., ICML 2025）、**GPT-4o**（Jaech et al., arXiv 2024））的依赖。

2. **分层轨迹搜索（Hierarchical Trajectory Search, HTS）**：采用粗到细的三阶段搜索策略——初始随机探索、分层瘦身（基于 SVF 评分修剪低潜力轨迹）和最终细化——将计算复杂度从线性搜索的 O(NT) 降至 O(N+T)，实现自适应计算分配。

在 GenEval 基准上，dMLLM-TTS 应用于三个代表模型（Lumina-DiMOO、MMaDA、Muddit）后，总体生成质量分别提升 **+17.9%、+29.4%、+26.4%**，同时 HTS 的推理效率最高可达线性搜索的 **6 倍**。自验证反馈在 Lumina-DiMOO 上表现与 VILA-Judge 相当，但弱于 GPT-4o，表明当前 dMLLM 的视觉理解能力仍有提升空间。该框架的局限性在于仅验证于扩散多模态大语言模型，对连续扩散模型或自回归模型的适用性尚待探索。

## 背景与动机

### 扩散多模态大语言模型的生成瓶颈

扩散多模态大语言模型（dMLLMs）将文本到图像生成建模为离散标记空间中的逐步去噪过程：从全掩码序列 $Z_0 = ( [Mask], [Mask], ..., [Mask] )$ 出发，每一步 $t$ 对所有掩码位置预测标记，逐步填充为置信预测（Figure 2）。这种范式天然支持多模态理解与生成的统一，但其生成质量高度依赖于采样过程中的随机探索与迭代细化。

然而，dMLLMs 的推理阶段面临一个核心矛盾：单次采样的随机性导致生成结果不稳定，而简单增加采样轨迹数或去噪步数又会带来高昂的计算开销。现有测试时扩展（Test-Time Scaling, TTS）方法试图通过搜索多条生成轨迹来提升图文对齐质量，但在 dMLLMs 上存在两个关键缺陷。

### 现有方法的双重缺口

**搜索效率瓶颈。** 当前主流的线性轨迹搜索（Linear Trajectory Search, LTS）对所有 $N$ 条轨迹均分配等量的 $T$ 步推理计算，复杂度为 $O(NT)$。这种均匀分配策略忽略了不同轨迹在生成早期的质量分化——大量计算被浪费在低潜力轨迹的完整运行上。

**外部验证器依赖。** 现有 TTS 方法依赖外部视觉-语言模型（如 CLIP、VILA-Judge、GPT-4o）作为验证器来评估图文对齐质量。这不仅引入额外的模型部署与推理成本，还割裂了 dMLLM 自身理解能力与生成过程的内在联系。

### 本文动机：自验证与高效搜索的统一

本文的核心观察是：dMLLM 本身具备内在的多模态理解能力，应当能够评估自己生成图像与文本提示的对齐程度。基于这一洞察，dMLLM-TTS 提出两个互补的解决方案：

1. **自验证反馈（Self-Verified Feedback, SVF）**：复用 dMLLM 的内在理解能力，以“是/否”问答的 logit 概率作为图文对齐分数，消除对外部验证器的依赖。
2. **分层轨迹搜索（Hierarchical Trajectory Search, HTS）**：通过三阶段粗到细搜索——初始随机探索、分层瘦身、最终细化——将计算资源从低潜力轨迹重新分配到高潜力轨迹，将复杂度从 $O(NT)$ 降至 $O(N+T)$。

这两个机制协同工作：SVF 提供无外部依赖的轨迹质量信号，HTS 利用该信号实现自适应计算分配，从而在显著提升生成质量的同时实现最高 6 倍的推理加速。

## 核心创新

dMLLM-TTS 的核心创新在于将扩散多模态大语言模型（dMLLM）的测试时扩展重新定义为一个**自适应轨迹搜索问题**，并通过两个相互协同的 changed slots 实现高效、自验证的图文生成优化。

### 从外部验证到自验证反馈（SVF）

现有测试时缩放方法普遍依赖外部视觉-语言模型作为验证器，如 **VILA-Judge**（Xie et al., ICML 2025）或 **GPT-4o**（Jaech et al., arXiv 2024），这引入了额外的模型部署成本和通信开销。dMLLM-TTS 的核心突破在于**自验证反馈（Self-Verified Feedback, SVF）**机制：直接复用 dMLLM 内在的多模态理解能力来评估生成图像与文本的对齐程度。

具体而言，SVF 将图文对齐评估转化为一个“是/否”问答任务——模型接收生成图像与原始文本提示，输出“是”的 logit 概率作为对齐分数：

$$\Phi_{\mathrm{SVF}} = \mathrm{logit}_{\mathrm{yes}}(\mathcal{G}_{\theta}(Z_t, C))$$

这一设计的深层洞察在于：dMLLM 本身具备理解图像内容的能力，只是此前未被用于自评估。SVF 消除了对外部验证器的依赖，将验证过程内化为模型推理的一部分，实现了闭环的自验证生成。

### 从线性搜索到分层轨迹搜索（HTS）

传统测试时缩放采用**线性轨迹搜索（LTS）**策略：对所有 $N$ 条生成轨迹均分配完整的 $T$ 步去噪计算，导致 $\mathcal{O}(NT)$ 的二次级计算复杂度。这种均匀分配策略忽视了轨迹间的质量差异——大量计算被浪费在低潜力轨迹上。

dMLLM-TTS 提出的**分层轨迹搜索（Hierarchical Trajectory Search, HTS）**从根本上改变了计算分配逻辑。HTS 将生成过程划分为三个阶段：

$$\mathrm{HTS} \Rightarrow \begin{cases} \mathrm{Initial~Stochastic~Exploration}, & t \leq T_s \\ \mathrm{Hierarchical~Thinning}, & T_s < t \leq T_r \\ \mathrm{Final~Refinement}, & T_r < t \leq T \end{cases}$$

在**初始随机探索**阶段，系统以较低的去噪步数并行探索 $N$ 条轨迹，快速获取各轨迹的 SVF 评分。进入**分层瘦身**阶段后，系统根据几何衰减调度逐步修剪低评分轨迹，将计算资源集中到高潜力轨迹上：

$$W_t = \max\bigl(\lfloor N d^{-(t-T_s)}\rfloor, K\bigr), \quad d > 1$$

其中 $d$ 为衰减系数，$K$ 为最小保留轨迹数。最终在**细化阶段**，仅对保留的 $K$ 条轨迹进行完整的精细去噪。

这种“早期广泛探索—中期快速修剪—晚期集中细化”的策略，将总计算成本从 $\mathcal{O}(NT)$ 降至近似 $\mathcal{O}(N+T)$：

$$C_{\mathrm{HTS}} = \mathcal{O}\left(N T_s + \frac{N - dK}{d - 1} + K(T - T_r)\right) \approx \mathcal{O}(N + T)$$

### 两轴协同扩展

dMLLM-TTS 的完整框架在两个互补维度上扩展推理计算：**轨迹探索扩展**（增加 $N$）拓宽假设空间多样性，**迭代细化扩展**（增加 $T$）提升单条轨迹的生成稳定性。SVF 作为统一的评分信号，同时引导两个维度的资源分配，而 HTS 则确保这种扩展不会导致计算成本的线性增长。

这一设计实现了效率与质量的双赢：实验表明，HTS 在达到同等或更高生成质量的前提下，推理速度可达线性搜索的 **5–6 倍**（Lumina-DiMOO 上 5×，MMaDA 和 Muddit 上 6×），同时 Lumina-DiMOO 的 GenEval 总分从 0.78 提升至 0.92（+17.9%）。

## 整体框架

dMLLM-TTS 将测试时扩展（Test-Time Scaling, TTS）形式化为一个 **自适应轨迹搜索问题**，其核心由三个组件定义：

$$
\mathrm{TTS} = \langle \mathcal{G}_{\boldsymbol{\theta}}, \mathcal{V}, f \rangle
$$

其中 $\mathcal{G}_{\boldsymbol{\theta}}$ 为扩散多模态大语言模型（dMLLM）生成器，$\mathcal{V}$ 为验证器，$f$ 为搜索策略。该框架沿两条互补的扩展轴运作，并由一个内在的自验证机制统一调度。

### 两轴扩展架构

**轨迹探索扩展（Trajectory Exploration Scaling）** 通过并行采样 $N$ 条随机初始化轨迹来拓宽假设空间。每条轨迹从完全掩码的 token 序列 $Z_0 = ([\text{Mask}], \dots, [\text{Mask}])$ 出发，经过逐步去噪生成最终图像。增加 $N$ 可显著提升生成多样性，尤其对初始性能较弱的模型增益更为明显。

**迭代细化扩展（Iterative Refinement Scaling）** 沿每条轨迹增加去噪步数 $T$，单步操作为：

$$
Z_{t+1} = \mathcal{G}_{\boldsymbol{\theta}}(Z_t, C, t), \quad t = 1, \ldots, T-1
$$

更多细化步数使模型有更充足的计算预算逐步填充离散多模态 token 空间，从而提升生成稳定性和细节质量。最优步数与文本提示的复杂度相关。

### 自验证反馈（Self-Verified Feedback, SVF）

SVF 是连接两轴扩展与搜索策略的核心纽带。它**复用 dMLLM 内在的多模态理解能力**来评估生成图像与文本的对齐程度，无需依赖外部验证器（如 CLIP、VILA-Judge 或 GPT-4o）。具体而言，SVF 以“是/否”问答形式向模型提问，取输出“是”的 logit 概率作为对齐分数：

$$
\Phi_{\mathrm{SVF}} = \mathrm{logit}_{\mathrm{yes}}(\mathcal{G}_{\theta}(Z_t, C))
$$

该分数在搜索过程中实时引导计算资源的分配方向。

### 分层轨迹搜索（Hierarchical Trajectory Search, HTS）

HTS 是框架的搜索策略核心，实现从粗到细的三阶段生成过程：

$$
HTS \Rightarrow \left\{ \begin{array}{ll} 
\mathrm{Initial~Stochastic~Exploration}, & t \leq T_s \\ 
\mathrm{Hierarchical~Thinning}, & T_s < t \leq T_r \\ 
\mathrm{Final~Refinement}, & T_r < t \leq T 
\end{array} \right.
$$

- **初始随机探索**（$t \leq T_s$）：以全量 $N$ 条轨迹并行探索，快速覆盖生成空间。
- **分层瘦身**（$T_s < t \leq T_r$）：依据 SVF 评分对轨迹池进行几何衰减收缩，保留高潜力轨迹并可能进行局部分支：

  $$
  W_t = \max\bigl(\lfloor N d^{-(t-T_s)}\rfloor, K\bigr), \quad d > 1
  $$

  其中 $d$ 为衰减系数，$K$ 为最小保留轨迹数（$K \ll N$）。此阶段将计算资源从低潜力轨迹中抽离。
- **最终细化**（$T_r < t \leq T$）：仅对保留的 $K$ 条高潜力轨迹进行精细去噪，集中计算预算于最有前景的生成方向。

### 复杂度优势

HTS 的总前向计算成本为：

$$
C_{\mathrm{HTS}} = \mathcal{O}\left(N T_s + \frac{N - dK}{d - 1} + K(T - T_r)\right)
$$

当 $K \ll N$ 且 $T_s \ll T$ 时，可近似为 $\mathcal{O}(N + T)$。这与线性搜索（LTS）所有轨迹均运行完整 $T$ 步的 $\mathcal{O}(NT)$ 复杂度形成鲜明对比——HTS 通过自适应计算分配，将早期广泛探索的算力在中期迅速收拢至紧凑轨迹集，实现了近线性的推理效率。

### 输入输出流

整个 pipeline 的输入为文本提示 $C$，输出为经 SVF 评分筛选的最优生成图像。流程如下：$C$ 同时送入生成器 $\mathcal{G}_{\boldsymbol{\theta}}$ 和 SVF 验证器；生成器沿 $N$ 条轨迹、最多 $T$ 步迭代去噪；SVF 在搜索过程中持续评估中间状态 $Z_t$ 的对齐分数；HTS 根据分数动态调整轨迹池宽度，最终返回评分最高的完整生成结果。

### 补充图表

![[assets/figures/papers/paper_list_l860_https_arxiv_org_abs_2512_19433/figures/003_Figure_3.jpg]]
*Figure 3: Overview of dMLLM-TTS framework. (a) dMLLM-TTS scales compute along two axes: trajectory exploration and iterative refinement, guided by Self-Verified Feedback for text–image alignment evaluation. (b) Hierarchical Trajectory Search (HTS) performs coarse-to-fine generation by starting with broad exploration, pruning low-potential trajectories, and refining high-potential trajectories*

![[assets/figures/papers/paper_list_l860_https_arxiv_org_abs_2512_19433/figures/001_Figure_1.jpg]]
*Figure 1: dMLLM-TTS: We present the generative effects and performance improvements achieved by applying Test-Time Scaling (TTS) to dMLLMs. Images generated with TTS exhibit higher quality and stronger prompt alignment than those generated without TTS*

## 核心模块与公式推导

### 3.1 扩散多模态大语言模型的生成范式

dMLLM 的图像生成过程可形式化为一个逐步去噪的离散标记预测问题。初始状态 $Z_0$ 为全掩码序列：

$$Z_0 = ([\text{Mask}], [\text{Mask}], \dots, [\text{Mask}])$$

在每个去噪步 $t$，模型 $\mathcal{G}_{\boldsymbol{\theta}}$ 根据当前状态 $Z_t$ 和文本条件 $C$ 预测所有掩码位置的标记，逐步填充离散多模态标记空间：

$$Z_{t+1} = \mathcal{G}_{\boldsymbol{\theta}}(Z_t, C, t), \quad t = 1, \ldots, T-1$$

其中 $T$ 为总去噪步数。生成过程从全灰掩码开始，逐步产生置信度递增的预测（蓝色标记），最终收敛为完整图像。

### 3.2 测试时扩展的形式化定义

dMLLM-TTS 将测试时扩展形式化为自适应轨迹搜索问题，定义为一个三元组：

$$\text{TTS} = \langle \mathcal{G}_{\boldsymbol{\theta}}, \mathcal{V}, f \rangle$$

其中 $\mathcal{G}_{\boldsymbol{\theta}}$ 为生成器（dMLLM），$\mathcal{V}$ 为验证器，$f$ 为搜索函数。框架沿两个互补轴扩展计算：

- **轨迹探索扩展（Trajectory Exploration Scaling）**：通过采样 $N$ 条随机初始化轨迹 $Z_1 \sim p_{\text{init}}$ 拓宽假设空间。
- **迭代细化扩展（Iterative Refinement Scaling）**：增加每条轨迹的去噪步数 $T$，提升生成稳定性和细节质量。

### 3.3 自验证反馈（Self-Verified Feedback, SVF）

SVF 的核心创新在于复用 dMLLM 内在的多模态理解能力进行图文对齐评估，从而消除对外部验证器的依赖。其评分函数定义为模型对“是/否”问答输出“是”的 logit 概率：

$$\Phi_{\text{SVF}} = \text{logit}_{\text{yes}}(\mathcal{G}_{\theta}(Z_t, C))$$

该机制将验证过程内化于模型自身，避免了引入外部 VLM（如 **VILA-Judge** (Xie et al., ICML 2025)、**GPT-4o** (Jaech et al., arXiv 2024)）带来的额外计算开销和架构耦合。

### 3.4 分层轨迹搜索（Hierarchical Trajectory Search, HTS）

HTS 通过三阶段粗到细搜索实现从 $\mathcal{O}(NT)$ 到 $\mathcal{O}(N+T)$ 的复杂度降阶，由转移步数 $T_s$ 和 $T_r$ 控制阶段切换：

$$\text{HTS} \Rightarrow \begin{cases}
\text{Initial Stochastic Exploration}, & t \leq T_s \\
\text{Hierarchical Thinning}, & T_s < t \leq T_r \\
\text{Final Refinement}, & T_r < t \leq T
\end{cases}$$

**阶段一：初始随机探索**。在 $t \leq T_s$ 期间，所有 $N$ 条轨迹并行执行去噪，以低成本广泛探索假设空间。

**阶段二：分层瘦身**。在 $T_s < t \leq T_r$ 期间，轨迹池宽度按几何衰减调度收缩：

$$W_t = \max\bigl(\lfloor N d^{-(t-T_s)}\rfloor, K\bigr), \quad d > 1$$

其中 $d$ 为衰减系数，$K$ 为最小保留轨迹数。每步依据 SVF 评分进行评分、选择和局部分支，将计算资源集中于高潜力轨迹。

**阶段三：最终细化**。在 $T_r < t \leq T$ 期间，仅保留前 $K$ 条最优轨迹进行精细去噪，确保高质量收敛。

### 3.5 复杂度分析

HTS 的总前向成本由三部分组成：

$$C_{\text{HTS}} = \mathcal{O}\left(N T_s + \frac{N - dK}{d - 1} + K(T - T_r)\right)$$

当 $K \ll N$ 且 $T_s \ll T$ 时，可近似简化为：

$$C_{\text{HTS}} \approx \mathcal{O}(N + T)$$

相比之下，线性轨迹搜索（LTS）的复杂度为 $\mathcal{O}(NT)$。HTS 通过早期广泛探索后快速修剪至紧凑集合（$K \ll N$），实现了计算资源从早期探索到晚期细化的自适应重分配，从根本上规避了 LTS 的二次成本瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l860_https_arxiv_org_abs_2512_19433/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of the image generation process in dMLLMs. The first row shows the input latent masks at each step, and the second row depicts the corresponding outputs. Sampling begins with fully masked tokens (gray) and gradually fills the discrete multimodal token space with increasingly confident predictions (blue)*

## 实验与分析

### 核心实验结果

dMLLM-TTS 在 GenEval 基准上对三个代表性 dMLLM 均实现了生成质量的显著提升。**Table 1** 汇总了不同 dMLLM 与测试时扩展设置下的定量对比，关键结果如下：

![[assets/figures/papers/paper_list_l860_https_arxiv_org_abs_2512_19433/figures/004_Table_1.jpg]]
*Table 1: Quantitative performance comparison on GenEval across various d-MLLMs and test-time scaling settings*

- **Lumina-DiMOO**：GenEval 总分从 0.78（无 TTS，N=1, T=8）提升至 **0.92**（HTS，N=32, T=32, K=8），增幅 **+17.9%**。
- **MMaDA**：总分从 0.51 提升至 **0.66**，增幅 **+29.4%**。
- **Muddit**：总分从 0.53 提升至 **0.67**，增幅 **+26.4%**。

值得注意的是，基础模型性能越弱，TTS 带来的相对增益越大——MMaDA 和 Muddit 的初始得分远低于 Lumina-DiMOO，但提升幅度反而更高。这表明测试时扩展对低资源或弱对齐模型具有更强的补偿效应。

从提示复杂度维度看，**Figure 4** 展示了 TTS 在不同 GenEval 评估维度（如颜色、纹理、空间关系等）上的改进比例。TTS 在所有维度上均带来正向提升，尤其在需要精细视觉理解的复杂提示场景中改进更为明显。

![[assets/figures/papers/paper_list_l860_https_arxiv_org_abs_2512_19433/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative improvement ratio in TTS performance across various text prompt complexities examined through diverse dMLLMs on GenEval benchmark dimensions. TTS markedly enhances performance across all measured dimensions*

### 效率分析：分层搜索 vs 线性搜索

**Figure 5** 对比了线性轨迹搜索（LTS）与分层轨迹搜索（HTS）的计算消耗-得分曲线。核心发现：

- **HTS 在同等推理计算量下持续收敛到更高的总分**。在 Lumina-DiMOO 上，HTS 达到与 LTS 相同得分所需的推理计算量减少约 **5 倍**；在 MMaDA 和 Muddit 上，加速比达 **6 倍**。
- 红色曲线（LTS）呈线性增长后趋于饱和，蓝色曲线（HTS）在早期即快速攀升，虚线部分为基于几何衰减的预测趋势。曲线拟合表明两者最终趋近同一上限，但 HTS 的收敛效率远优于 LTS。

这一效率优势源于 HTS 的自适应计算分配机制：早期广泛探索（N 条轨迹），中期通过 SVF 评分快速修剪至紧凑集合（K ≪ N），后期将计算集中投入高潜力轨迹的精细优化。理论上前向成本从 LTS 的 $\mathcal{O}(NT)$ 降至 HTS 的 $\mathcal{O}(N+T)$。

### 消融实验

**Figure 6** 分别展示了轨迹探索扩展（左）与迭代细化扩展（右）的消融结果。

**轨迹探索扩展（N=1→32）**：
- 在所有三个 dMLLM 上，增加探索轨迹数持续提升 GenEval 总分。
- 增益幅度与模型初始得分负相关：MMaDA +20.2%，Muddit +16.8%，Lumina-DiMOO +8.8%。
- 收益曲线在 N=32 时尚未完全饱和，暗示更大规模的探索可能带来进一步增益。

**迭代细化扩展（T=8→64）**：
- 增加去噪步数在所有模型上稳定提升总分，但边际收益递减。
- 最优步数取决于文本提示的复杂度：简单提示在 T=16 时即接近饱和，复杂提示则持续受益至 T=64。
- 这一发现揭示了提示自适应调度 T 的潜在需求。

### 验证器对比

**Table 2** 对比了自验证反馈（SVF）与外部验证器的性能。在 Lumina-DiMOO 上，SVF（0.92）与 VILA-Judge（0.90）表现相当，但弱于 GPT-4o（0.95）。在 MMaDA 和 Muddit 上，SVF 与外部验证器的差距略有扩大。

这一差距反映了当前 dMLLM 视觉理解能力的内在局限：模型自身的“是/否”问答 logit 概率虽可作为有效对齐信号，但其判别精度仍不及专门的强视觉-语言模型。**这是 SVF 机制的核心失败模式——当生成图像存在细微的语义偏差时，dMLLM 的自评估可能无法准确捕捉，导致修剪阶段误保留次优轨迹。**

### 定性分析

**Figure 7** 展示了有无 dMLLM-TTS 的生成过程对比。基线模型在复杂提示下产生不满意的结果（如对象缺失、属性错误），而引入 TTS 策略后，生成过程在早期即展现出更准确的语义对齐，并在细化阶段逐步修正细节偏差。这直观验证了 HTS 粗到细搜索策略的有效性：早期修剪淘汰明显偏离提示的轨迹，后期集中优化高潜力候选。

### 实验公平性说明

所有实验均基于相同的 GenEval 基准和评估指标，比较的基线使用相同的基础模型架构与训练数据。推理时的总采样步数与轨迹数在对应对比中保持一致，确保性能差异仅归因于搜索策略和验证机制的变化。

### 补充图表

![[assets/figures/papers/paper_list_l860_https_arxiv_org_abs_2512_19433/figures/006_Figure_5.jpg]]
*Figure 5: Comparison between linear and hierarchical trajectory search. The red curve illustrates linear trajectory search, while the blue curve depicts hierarchical trajectory search, with a dashed line indicating predictions based on a geometric series decay approximation. Curve fitting shows that similar subsequent trends tend to converge towards an upper limit*

![[assets/figures/papers/paper_list_l860_https_arxiv_org_abs_2512_19433/figures/007_Figure_6.jpg]]
*Figure 6: Trajectory Exploration Scaling (Left) and Iterative Refinement Scaling (Right). Increasing the number of explored trajectories (N = 1→32) refinement steps (T = 8→64) consistently improves performance across all dMLLMs*

![[assets/figures/papers/paper_list_l860_https_arxiv_org_abs_2512_19433/figures/009_Table_2.jpg]]
*Table 2: Comparison results of various verifiers*

![[assets/figures/papers/paper_list_l860_https_arxiv_org_abs_2512_19433/figures/008_Figure_7.jpg]]
*Figure 7: Image Generation Process without (Top) and with (Bottom) dMLLM-TTS. The baseline models produce unsatisfactory text-to-image results. However, by incorporating our TTS strategies, the generation process is significantly improved*

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

现有测试时缩放（TTS）方法在扩散多模态大语言模型（dMLLMs）上存在两个结构性瓶颈：（1）**线性搜索的高计算成本**——线性轨迹搜索（LTS, Xie et al., ICML 2025）对所有轨迹分配等量推理计算，复杂度为 O(NT)，随轨迹数 N 和细化步数 T 呈二次增长；（2）**依赖外部验证器的资源开销**——现有方法需引入外部视觉-语言模型（如 VILA-Judge, Xie et al., ICML 2025；GPT-4o, Jaech et al., arXiv 2024）评估图文对齐质量，这不仅增加推理成本，还引入了额外的模型依赖与部署复杂度。

dMLLM-TTS 的核心洞察在于：**利用 dMLLM 内在的图像理解能力实现自验证反馈，并通过分层搜索在早期粗生成阶段修剪低潜力轨迹，将计算资源集中在高潜力轨迹的精细优化上**。这一设计同时解决了验证器外部依赖和搜索效率两个问题。

### 方法谱系中的位置

dMLLM-TTS 位于以下三条研究脉络的交汇点：

**1. 扩散多模态大语言模型（dMLLMs）**

该方法建立在离散扩散多模态大语言模型的生成范式之上，代表性工作包括 Lumina-DiMOO、MMaDA 和 Muddit。这类模型将图像生成建模为从全掩码序列逐步去噪填充的过程（见 Figure 2），其核心操作可形式化为迭代细化步骤：

$$Z_{t+1} = \mathcal{G}_{\boldsymbol{\theta}}(Z_t, C, t), \quad t = 1, \ldots, T-1$$

其中 $Z_t$ 为第 t 步的离散多模态 token 状态，$C$ 为文本条件。dMLLM-TTS 在此范式基础上引入测试时计算扩展，不改变模型参数 $\boldsymbol{\theta}$。

**2. 测试时缩放（Test-Time Scaling）**

测试时缩放是近年来在 LLM 推理领域兴起的技术方向，通过增加推理计算量提升生成质量。dMLLM-TTS 将 TTS 形式化为自适应轨迹搜索问题，定义为三元组：

$$\mathrm{TTS} = \langle \mathcal{G}_{\boldsymbol{\theta}}, \mathcal{V}, f \rangle$$

其中 $\mathcal{G}_{\boldsymbol{\theta}}$ 为生成器，$\mathcal{V}$ 为验证器，$f$ 为搜索函数。相比 LTS 的均匀计算分配策略，dMLLM-TTS 在两个维度上进行了根本性改进：

- **搜索算法**：从线性搜索（所有轨迹等量计算，复杂度 O(NT)）升级为分层轨迹搜索（HTS），通过自适应修剪将复杂度降至 O(N+T)。HTS 包含三个阶段——初始随机探索（$t \leq T_s$）、分层瘦身（$T_s < t \leq T_r$）和最终细化（$T_r < t \leq T$），轨迹池宽度按几何衰减调度收缩：

$$W_t = \max\bigl(\lfloor N d^{-(t-T_s)}\rfloor, K\bigr), \quad d > 1$$

总前向成本可近似为：

$$C_{\mathrm{HTS}} \approx \mathcal{O}(N + T)$$

- **验证器**：从外部 VLM（CLIP、VILA-Judge、GPT-4o）替换为自验证反馈（SVF），复用 dMLLM 内在的多模态理解能力，以“是/否”问答的 logit 概率作为图文对齐分数：

$$\Phi_{\mathrm{SVF}} = \mathrm{logit}_{\mathrm{yes}}(\mathcal{G}_{\theta}(Z_t, C))$$

**3. 计算分配策略**

dMLLM-TTS 的计算分配策略与 Best-of-N 采样、树搜索等方法形成对比。Best-of-N 在最终步骤进行选择，缺乏中间修剪机制；树搜索（如 MCTS）需要维护复杂的状态空间。HTS 采用“早期广泛探索—中期修剪—晚期集中细化”的三阶段策略，在保持搜索多样性的同时实现近线性计算扩展。

### 适用边界与局限

**已验证的适用范围**：

- 实验在 GenEval 基准上覆盖三个代表性 dMLLM（Lumina-DiMOO、MMaDA、Muddit），均取得显著提升（+17.9% 至 +29.4%），效率提升达 5×–6×。这表明该方法对离散扩散多模态大语言模型具有良好的泛化性。

**明确的局限性**：

1. **自验证反馈的性能上限**：SVF 在 Lumina-DiMOO 上表现与 VILA-Judge 相当（0.92 vs 0.90），但弱于 GPT-4o（0.95）。在 MMaDA 和 Muddit 上，SVF 与外部验证器的差距更为明显（SVF 0.66/0.67，GPT-4o 0.71/0.74）。这反映出当前 dMLLM 的视觉理解能力仍有较大提升空间，SVF 尚不能完全替代强外部验证器。

2. **模型范式的适用性未验证**：所提框架仅在离散扩散 dMLLMs 上验证，对于基于连续扩散模型（如 Stable Diffusion、Flux）或自回归生成模型的适用性尚未探讨。HTS 的分层修剪策略依赖于扩散过程的时间结构，在自回归范式中需要重新设计。

### 开放问题

1. **自适应参数选择**：如何依据文本提示的复杂度自动适配最优的轨迹探索数量 N 与细化步数 T？当前实验表明细化步数的最优值取决于提示复杂度，但缺乏自动化的选择机制。

2. **自验证能力的增强**：能否通过微调或偏好优化（如 DPO）进一步提升 dMLLM 的自验证准确率，从而完全替代外部验证器？这涉及模型内在理解能力与生成能力的联合优化。

3. **训练时与测试时扩展的联合优化**：该测试时扩展框架与训练时扩展（模型参数量、数据规模）之间的关系如何？是否存在“计算最优”分配策略，在给定总计算预算下平衡训练与推理的投入？

4. **更广泛生成任务的迁移**：HTS 的分层搜索策略是否适用于其他需要多轨迹探索的生成任务（如文本生成、代码生成）？其核心假设——早期步骤的低成本粗评估可有效预测最终质量——在不同模态中是否成立？

## 原文 PDF

![[paperPDFs/CVPR_2026/dMLLM_TTS_Self_Verified_and_Efficient_Test_Time_Scaling_for_Diffusion_Multi_Modal_Large_Language_Models.pdf]]
