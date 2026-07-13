---
title: "LaDiR: Latent Diffusion Enhances LLMs for Text Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/LaDiR_Latent_Diffusion_Enhances_LLMs_for_Text_Reasoning.pdf
project_link: null
code_link: null
openreview_forum_id: z5cPEZ4n6i
aliases:
- LaDiR
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "通过将推理步骤编码为连续潜在思维token，并利用潜在扩散模型进行块级迭代去噪，实现语义层面的推理自我修正与多样性探索。"
primary_logic: "在由变分自编码器构建的连续潜在空间中，应用块级双向注意力的扩散模型对推理过程进行建模，实现了从离散token到语义级潜在表示的转变，结合训练-推理不一致缓解及多样性引导，使模型能够进行可解释、可迭代修正且多样化的潜在推理。"
claims:
- "LaDiR在7个数学推理基准上平均Pass@1超过当前最强潜在推理基线TaH+约1.5%"
- "在Countdown-4任务上，LaDiR将Pass@1从LLaMA 8B SFT的46.7%提升至76.6%，Pass@100提升至96.4%"
- "增加去噪步数从5步到10步，在7个数学基准上平均准确率提升+11.7个百分点"
- "移除第二阶段训练导致数学推理平均Pass@1从43.5%骤降至27.9%，证明其对缓解误差累积至关重要"
---

# LaDiR: Latent Diffusion Enhances LLMs for Text Reasoning

> [!tip] 核心洞察
> 在由变分自编码器构建的连续潜在空间中，应用块级双向注意力的扩散模型对推理过程进行建模，实现了从离散token到语义级潜在表示的转变，结合训练-推理不一致缓解及多样性引导，使模型能够进行可解释、可迭代修正且多样化的潜在推理。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | LaDiR：潜在扩散增强大语言模型的文本推理 |
| 英文题名 | LaDiR: Latent Diffusion Enhances LLMs for Text Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=z5cPEZ4n6i) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | LaDiR |
| Dataset | Math (7 benchmarks avg.), Code (4 benchmarks avg.), Countdown-4 |

> [!tip] 效果简介
> - Math (7 benchmarks avg.) 上，Pass@1 为 43.5，对比 42.0 (TaH+)，变化 +1.5。
> - Math (7 benchmarks avg.) 上，Pass@100 为 52.0，对比 45.4 (CoT SFT α=0.7)，变化 +6.6。
> - Code (4 benchmarks avg.) 上，Pass@1 为 74.5，对比 69.3 (AR SFT)，变化 +5.2。

## 概要

大语言模型在数学推理、代码生成等任务中展现出强大能力，但其主导的自回归解码范式存在一个根本瓶颈：token一旦生成便无法从全局角度进行修正，导致推理过程的自我修正效率低下，且难以系统性地探索多种可能解。现有潜在推理方法（如Coconut、TaH+）虽尝试在连续空间中进行推理，但仍沿用逐token的顺序生成模式，未能充分利用扩散模型的迭代优化能力。

LaDiR针对上述瓶颈，提出了一种新的推理范式：**将文本推理步骤编码为连续潜在思维token，并利用潜在扩散模型进行块级迭代去噪，在语义层面实现推理的自我修正与多样性探索**。其核心洞察在于——通过变分自编码器（VAE）构建的连续潜在空间，配合块级双向注意力的扩散模型，将推理从离散token的逐词预测转变为语义级潜在表示的全局优化过程。该方法结合两阶段训练（教师强制与自生成展开训练）以缓解训练-推理不一致，并引入基于排斥力场的多样性引导机制。

实验表明，LaDiR在7个数学推理基准上的平均Pass@1达到43.5%，超过当前最强潜在推理基线TaH+约1.5个百分点；在Countdown-4规划任务上，Pass@1从LLaMA 8B SFT的46.7%跃升至76.6%，Pass@100高达96.4%。代码生成任务上，HumanEval+的Pass@1达到84.2%，较自回归SFT基线提升7.7个百分点。消融实验进一步揭示，增加去噪步数从5步到10步可带来平均+11.7个百分点的准确率提升，而去除第二阶段训练则导致数学推理平均Pass@1从43.5%骤降至27.9%，验证了训练-推理一致性对齐的关键作用。

在方法谱系中，LaDiR区别于三类主流基线：**自回归思维链**（LLaMA 3.1 8B CoT SFT, Dubey et al., 2024）受限于单向解码；**遮蔽扩散模型**（LLaDA 8B, Nie et al., 2025）在离散token空间操作，缺乏语义级迭代能力；**潜在推理方法**（Coconut, Hao et al., 2024; TaH+, Fu et al., 2025; CODI, Shen et al., 2025a）虽引入连续表示，但未采用扩散去噪机制进行块级修正。LaDiR首次将流匹配扩散与块级潜在推理相结合，在表示形式、推理过程、多样性机制和训练策略四个维度上实现了系统性改进。



大语言模型在复杂推理任务上的突破，很大程度上得益于思维链（Chain-of-Thought, CoT）的引入——模型将推理过程分解为一系列离散文本步骤，以自回归方式逐token生成。然而，这种自回归解码范式存在一个结构性瓶颈：模型一旦生成某个token，便无法从全局角度对其进行修正。这导致推理过程的自我修正效率低下，且模型难以探索多种可能的解路径，限制了推理的鲁棒性与多样性。

近年来，研究者尝试将推理过程从离散文本空间迁移至连续潜在空间，以期获得更强的全局建模与迭代修正能力。例如，**Coconut**（Hao et al., 2024）和**CODI**（Shen et al., 2025a）等方法将部分推理步骤替换为连续潜在token，但它们在推理时仍采用自回归生成方式，未能充分利用扩散模型在连续空间中迭代去噪、逐步精炼的核心优势。另一方面，**LD4LG**（Lovelace et al., 2024）和**PLANNER**（Zhang et al., 2023）等工作虽将潜在扩散应用于文本生成，但其目标在于生成流畅文本，而非优化推理轨迹以导向正确答案，且缺乏对推理过程的可解释性设计。

上述方法共同面临三个关键缺口：其一，推理过程缺乏语义层面的可解释迭代修正机制；其二，训练与推理之间存在不一致——训练时依赖教师强制（teacher forcing），推理时却需自生成潜在token，导致误差累积；其三，多样性探索手段单一，仅依赖解码时的温度采样，难以在保持精度的同时有效拓展解空间。

针对这些缺口，本文提出**LaDiR**（Latent Diffusion Enhances LLMs for Text Reasoning），核心动机在于：将推理步骤编码为由变分自编码器（VAE）构建的连续潜在思维token块，并利用潜在扩散模型进行块级迭代去噪，从而在语义层面实现推理的自我修正与多样性探索。该方法通过两阶段训练缓解训练-推理不一致，并引入基于排斥力场的多样性引导机制，使模型能够进行可解释、可迭代修正且多样化的潜在推理。



## 核心方法与创新机理

LaDiR的核心创新在于将大语言模型的推理过程从**离散token空间迁移至连续潜在空间**，通过潜在扩散模型的迭代去噪能力实现语义层面的推理自我修正与多样性探索。相较于传统自回归思维链（CoT）和现有潜在推理方法，LaDiR在三个关键维度上实现了系统性突破。

### 推理表示形式：从离散Token到结构化潜在思维块

传统自回归方法将推理过程建模为离散文本token的逐词生成，而LaDiR采用**变分自编码器（VAE）**构建结构化的潜在推理空间。具体而言，VAE编码器从微调后的预训练LLM初始化，将CoT文本按句子级分割为推理块（block），每个块对应一组连续的潜在思维token $\mathbf{Z}^{(b)} = \{z_1^{(b)}, ..., z_{L_h}^{(b)}\}$。这种块级潜在表示（**changed slot: 推理表示形式**）使得推理过程从离散符号操作转变为连续语义向量的操控，为后续的迭代修正和多样性探索提供了连续空间的灵活度。

### 推理过程：从无全局修正的自回归解码到块级双向扩散去噪

自回归解码的核心瓶颈在于**无法从全局角度修正早期生成的token**，导致错误一旦产生便难以回溯修正。LaDiR将推理过程重新定义为**块级潜在扩散去噪**（**changed slot: 推理过程**）：在每个推理块内部，模型采用双向注意力掩码，通过流匹配（flow matching）目标迭代去噪潜在token，使得模型能够同时关注块内所有位置的信息，实现语义层面的自我修正。表4（Table 4）的定性示例展示了这一过程——随着去噪时间步 $t$ 的递减，VAE解码器重建的推理文本从粗糙或不完整的算术表达式逐步修正为逻辑一致的方程。

这种块级扩散机制的关键优势在于**可扩展的计算投入**：增加去噪步数从5步到10步，在7个数学基准上平均准确率提升+11.7个百分点；进一步增至50步可获得总计+9.8个百分点的增益（Figure 4）。这表明LaDiR能够在推理时通过增加计算量来持续提升推理质量，而自回归方法在单次解码中不具备这种迭代精炼能力。

### 多样性机制：从温度采样到噪声注入与排斥力场引导

自回归方法的多样性主要依赖解码时的温度采样，这种方式在潜在空间中缺乏结构化的探索引导。LaDiR引入**双重多样性引导机制**（**changed slot: 多样性机制**）：一方面通过增大初始高斯噪声的方差 $\tilde{\sigma}^2$ 来增加推理轨迹的起点多样性；另一方面在去噪过程中施加**排斥力场**：

$$\mathbf{F}(z_i) = \sum_{j \neq i} 2 \left(1 - \frac{\|z_i - z_j\|_2^2}{\sigma^2}\right) \exp\left(-\frac{\|z_i - z_j\|_2^2}{\sigma^2}\right) (z_i - z_j)$$

该力场推动同一批次内的潜在轨迹相互远离，鼓励模型探索不同的推理路径。消融实验（Figure 3）表明，适度的初始噪声（$\tilde{\sigma}^2=2$）和中等排斥强度（$\gamma_{max}=0.3\text{--}0.5$）能够在多样性与准确率之间取得最佳平衡。在Countdown-4任务上，这一机制使得LaDiR的Pass@1从LLaMA 8B SFT的46.7%提升至76.6%，Pass@100更达到96.4%（Table 3），显著超越所有基线方法。

### 训练-推理一致性：从单一教师强制到两阶段展开训练

潜在扩散模型面临的核心挑战是**训练-推理不一致**：训练时使用VAE编码器产生的oracle潜在块（教师强制），而推理时模型需从纯噪声生成自身的潜在块，这种分布偏移会导致误差累积。LaDiR通过**两阶段训练**（**changed slot: 训练-推理一致性**）解决这一问题：第一阶段采用标准教师强制训练；第二阶段引入展开训练（rollout training），让模型使用更少的去噪步数（从50步降至10步）生成自身的潜在表示，并基于这些自生成潜在块进行训练。消融实验（Table 1）的对比结果极具说服力——移除第二阶段训练导致数学推理平均Pass@1从43.5%骤降至27.9%，降幅超过15个百分点，充分证明了展开训练对缓解误差累积的关键作用。

### 与现有潜在推理方法的本质差异

相较于Coconut（Hao et al., 2024）和TaH+（Fu et al., 2025）等现有潜在推理方法，LaDiR的核心差异在于：前者仍采用**自回归方式**逐块生成连续潜在token，缺乏对已生成潜在表示的全局修正能力；而LaDiR在每个推理块内部使用**双向注意力的扩散去噪**，使得模型能够迭代精炼语义表示。此外，LaDiR通过VAE构建了显式的潜在-文本映射，使得推理过程可解码为可读文本（Table 10展示了GSM8K上的语义级自我修正示例），相较于Coconut等方法的隐式潜在状态具有更强的可解释性。



![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_z5cPEZ4n6i/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of our block-wise latent reasoning framework. A question Q is first input as condition to generate latent blocks, each delimited by <BOT> and <EOT>. For each block, the model iteratively denoises latent tokens $\hat { \mathbf { Z } } ^ { ( b ) }$ across timesteps, with bidirectional attention inside a block and causal attention across blocks. The reasoning process terminates when the model emits the <SOA> token, after which the model generates the answer text autoregressively

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_z5cPEZ4n6i/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of reasoning paradigms: autoregressive CoT and latent CoT generate discrete or continuous tokens sequentially; diffusion LMs iteratively convert [MASK] tokens to discrete text tokens in parallel in a semi-autoregressive way; and our proposed method LaDiR reasons over latent thought tokens via diffusion, enabling iterative refinement at semantic level and diverse exploration*

LaDiR 的核心设计理念是将推理过程从最终答案生成中解耦，通过构建一个结构化的连续潜在推理空间，使模型能够在语义层面进行迭代修正与多样性探索。其整体流水线由三个关键阶段串联而成：**潜在空间构建**、**块级扩散推理**与**答案生成**，并在训练与推理环节分别引入缓解分布偏移的机制与多样性引导策略。

### 流水线总览

整个框架的输入为问题文本 $q$，输出为最终答案文本 $y$。处理流程如下：

1. **问题编码与条件注入**：输入问题 $q$ 首先被送入推理扩散模型作为全局条件，贯穿后续所有潜在块的生成过程（见 Figure 2）。
2. **块级潜在推理生成**：模型以自回归方式逐块生成潜在思维 token。每个推理块以 `<BOT>`（begin-of-thought）起始、以 `<EOT>`（end-of-thought）结束。对于第 $b$ 个块，模型从纯高斯噪声出发，在块内双向注意力机制的约束下，通过 $T$ 步流匹配去噪迭代生成潜在表示 $\hat{\mathbf{Z}}^{(b)}$。
3. **推理终止判定**：在每个 `<EOT>` 位置，一个特殊的二分类头预测下一个块应以 `<SOA>`（start-of-answer）还是 `<BOT>` 开始。若预测为 `<SOA>`，推理过程终止；否则继续生成下一个潜在块。
4. **答案自回归解码**：当推理终止后，模型以所有去噪后的潜在块 $\mathbf{Z}^{(\leq B)}$ 为条件，自回归地生成最终答案 token 序列。

### 核心模块与功能

LaDiR 的流水线由以下模块协同完成：

| 模块 | 功能 | 关键设计 |
|------|------|----------|
| **Blockization（块化）** | 将思维链文本分割为句子级块，每个块对应一组固定数量的潜在 token | 每块 $L_b$ 个潜在 token，块内双向注意力，块间因果注意力 |
| **VAE 编码器** | 从微调 LLM 初始化，将推理块文本编码为潜在 token 的均值与方差 | 引入 $L_b$ 个可学习嵌入，通过线性投影从最后隐藏状态获得 $\mu$ 和 $\sigma$ |
| **VAE 解码器** | 冻结的预训练 LLM，以采样得到的潜在 token 为条件重建原始文本 | 教师强制模式下重建，确保潜在空间保留语义信息 |
| **推理扩散模型** | 基于相同 LLM 主干的流匹配模型，通过块级扩散去噪生成潜在推理块 | 采用混合注意力掩码（块内双向 + 跨块因果），使用 u-prediction 目标 |
| **答案生成头** | 基于去噪后的潜在块，自回归预测答案 token | 与推理模型共享 Transformer 主干，通过 LM head 输出 |
| **特殊 token 预测器** | 预测 `<EOT>` 之后下一块的类型 | 二分类头，控制推理链长度 |
| **多样性引导** | 通过增加初始噪声与排斥力场，推动批次内潜在轨迹相互远离 | 初始噪声尺度与最大排斥强度 $\gamma_{\max}$ 可调 |

### 训练-推理一致性设计

LaDiR 面临的核心挑战是**训练-推理分布偏移**：第一阶段教师强制训练使用 VAE 编码器产生的 oracle 潜在块，而推理时模型需从纯噪声出发自生成潜在块，这种差异会导致误差累积。为此，LaDiR 采用两阶段训练策略：

- **第一阶段（教师强制训练）**：模型以 VAE 编码器产生的真实潜在块 $\mathbf{Z}^{(1:B)}$ 为条件，联合优化流匹配损失 $\mathcal{L}_{\mathrm{FM}}$、答案生成损失 $\mathcal{L}_{\mathrm{Ans}}$ 和特殊 token 预测损失 $\mathcal{L}_{\mathrm{Spec}}$，整体目标为：
  $$\mathcal{L} = \lambda_{\mathrm{FM}} \mathcal{L}_{\mathrm{FM}} + \lambda_{\mathrm{Ans}} \mathcal{L}_{\mathrm{Ans}} + \lambda_{\mathrm{Spec}} \mathcal{L}_{\mathrm{Spec}}$$

- **第二阶段（展开训练）**：模型使用自身生成的潜在 token 进行训练，并将去噪步数从 50 步降至 10 步（遵循 FlowGRPO 的设置），使训练条件更贴近推理场景。消融实验表明，移除第二阶段训练会导致数学推理平均 Pass@1 从 43.5% 骤降至 27.9%（Table 1），验证了该阶段对缓解误差累积的关键作用。

### 推理时的多样性机制

在推理阶段，LaDiR 引入两种互补的多样性增强机制：

1. **增加初始噪声**：将初始高斯噪声的方差从标准 $\mathcal{N}(0,1)$ 放大至更大尺度，为扩散过程提供更丰富的起始点。
2. **多样性梯度引导**：在去噪的每一步，对批次内的潜在 token 施加排斥力场：
   $$\mathbf{F}(z_i) = \sum_{j \neq i} 2 \left(1 - \frac{\|z_i - z_j\|_2^2}{\sigma^2}\right) \exp\left(-\frac{\|z_i - z_j\|_2^2}{\sigma^2}\right) (z_i - z_j)$$
   去噪预测更新为 $\hat{z}_{t-1} = f_{\psi}(\mathbf{x}_t, t, x) + \gamma_t \mathbf{F}(z)$，其中 $\gamma_t$ 随时间步衰减。

实验表明，适度增加初始噪声（尺度从 1 到 2）和中等多样性引导强度（$\gamma_{\max}$ 在 0.3–0.5）能在多样性与准确率之间取得最佳平衡（Figure 3）。

### 输入输出流总结

```
输入: 问题文本 q
  │
  ├─→ [推理扩散模型] ──→ 潜在块 Z^(1) ──→ ... ──→ 潜在块 Z^(B)
  │       ↑                    ↑                    ↑
  │   初始噪声 N(0,σ²I)    块内双向注意力      <EOT> 后判定
  │       + 排斥力场        T 步流匹配去噪      <SOA>/<BOT>
  │
  └─→ [答案生成头] ──→ 自回归解码 → 最终答案 y
          ↑
     条件: q + Z^(≤B)
```

该框架的核心优势在于：潜在块内的双向注意力使模型能够在语义层面进行全局一致的迭代修正，而块间的因果注意力保留了推理步骤的逻辑递进关系，从而在保持推理可解释性的同时，赋予模型超越传统自回归解码的自我修正与多样性探索能力。



LaDiR 的核心架构由三个功能组件构成：**变分自编码器（VAE）** 负责构建连续潜在推理空间，**推理扩散模型** 在潜在空间中执行块级迭代去噪，**答案生成与特殊token预测头** 将去噪后的潜在表示转化为最终答案并控制推理块数量。

### 3.1 变分自编码器与潜在空间构建

VAE 的作用是将离散的思维链（CoT）文本步骤编码为连续的潜在思维token块，并确保这些潜在表示能够被重建回原始文本。编码器从预训练 LLM 初始化并进行全参数微调，同时引入 $L_b$ 个可学习的嵌入向量；解码器则冻结预训练 LLM 参数，以教师强制（teacher forcing）方式从采样得到的潜在token重建对应文本块。

训练目标采用 $\beta$-VAE 损失，在重建精度与先验正则化之间进行权衡：

$$\mathcal{L}_{\beta\mathrm{-VAE}} = \mathbb{E}_{q_{\phi}(z|x)}[-\log p_{\theta}(x|z)] + \beta \mathrm{KL}(q_{\phi}(z|x)\|p(z))$$

其中 $q_{\phi}(z|x)$ 为编码器输出的近似后验分布，$p_{\theta}(x|z)$ 为解码器的重建分布，$\beta$ 控制 KL 正则化项的权重。编码器从最后一个隐藏状态经线性投影得到均值 $\mu$ 和方差 $\sigma^2$，潜在token $\tilde{z}_i$ 通过重参数化技巧从 $\mathcal{N}(\mu, \sigma^2)$ 中采样。

### 3.2 推理扩散模型与流匹配

推理扩散模型基于与 VAE 编码器相同的 LLM 主干，采用**流匹配（Flow Matching）** 目标进行训练。流匹配的核心思想是学习一个速度场 $u_{\boldsymbol{\theta}}(z_t, t)$，使其逼近从数据分布 $p_{\mathrm{data}}$ 到标准高斯分布 $\mathcal{N}(0, I)$ 的最优传输路径上的目标速度场 $u^{\star}(z_t, t)$：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{t\sim\mathcal{U}(0,1), z_0\sim p_{\mathrm{data}}, z_1\sim\mathcal{N}(0,I)} \left[ \| u_{\boldsymbol{\theta}}(z_t, t) - u^{\star}(z_t, t) \|^2 \right]$$

在推理阶段，模型从纯噪声 $z_1 \sim \mathcal{N}(0, I)$ 出发，通过常微分方程（ODE）求解器逐步去噪，最终得到 $t=0$ 时的干净潜在token块 $\hat{\mathbf{Z}}^{(b)}$。每个潜在块内部采用**双向注意力**，块与块之间以及问题条件 $q$ 则保持**因果注意力**，形成混合注意力掩码，使模型既能对当前块进行全局语义修正，又能保持跨块的条件依赖。

### 3.3 答案生成与推理终止控制

去噪完成后，模型通过两个并行的预测头完成最终输出：

**答案生成头** 以问题和所有去噪后的潜在推理块 $\mathbf{Z}^{(\leq B)}$ 为条件，自回归地预测答案文本 token $y_w$：

$$\mathcal{L}_{\mathrm{Ans}} = - \sum_{w=1}^{W} \log p_{\psi}(y_{w} \mid q, \mathbf{Z}^{(\leq B)}, y_{<w})$$

**特殊token预测头** 是一个二分类器，在每个 `<EOT>` 位置判断下一个块应以 `<SOA>`（开始答案）还是 `<BOT>`（继续推理）起始：

$$\mathcal{L}_{\mathrm{Spec}} = - \sum_{\tau \in \mathcal{T}_{\mathrm{EOT}}} \log p_{\psi}(s_{\tau} \mid q, \mathbf{Z}^{(\leq B)})$$

其中 $\mathcal{T}_{\mathrm{EOT}}$ 为所有 `<EOT>` token 的位置集合。当模型预测 `<SOA>` 时推理过程终止，随后进入答案生成阶段。

### 3.4 联合训练目标与两阶段策略

第一阶段采用教师强制训练，模型直接使用 VAE 编码器产生的 oracle 潜在块进行流匹配和答案预测，联合损失为：

$$\mathcal{L} = \lambda_{\mathrm{FM}} \mathcal{L}_{\mathrm{FM}} + \lambda_{\mathrm{Ans}} \mathcal{L}_{\mathrm{Ans}} + \lambda_{\mathrm{Spec}} \mathcal{L}_{\mathrm{Spec}}$$

第二阶段为**展开训练（rollout training）**，模型使用自身生成的潜在token（以较少去噪步数，如从50步降至10步）替代 oracle 潜在块，重新计算上述损失。这一设计直接针对训练-推理不一致问题：训练时模型接触的是精确的 oracle 潜在表示，而推理时只能依赖自身有噪的生成结果，误差会沿块链累积。消融实验证实，移除第二阶段训练导致数学推理平均 Pass@1 从 43.5% 骤降至 27.9%，验证了该机制对缓解误差传播的关键作用。

### 3.5 多样性引导机制

为增强推理的多样性探索能力，LaDiR 在推理去噪过程中引入**排斥力场**，推动同一批次内不同样本的潜在轨迹相互远离：

$$\mathbf{F}(z_i) = \sum_{j \neq i} 2 \left(1 - \frac{\|z_i - z_j\|_2^2}{\sigma^2}\right) \exp\left(-\frac{\|z_i - z_j\|_2^2}{\sigma^2}\right) (z_i - z_j)$$

该力场源自高斯核的梯度，当两个潜在token距离小于 $\sigma$ 时产生排斥力，超出 $\sigma$ 后迅速衰减。最终预测结合基础模型输出与排斥梯度：

$$\hat{z}_{t-1} = f_{\psi}(z_t, t, x) + \gamma_t \mathbf{F}(z)$$

其中 $\gamma_t$ 为随时间步衰减的引导强度。配合**增大初始噪声尺度**（将初始方差从 1 提升至 2），该机制在不损害收敛性的前提下显著提升了解决方案的多样性。实验表明，适中的多样性引导值（0.3–0.5）在 Countdown-4 任务上取得了多样性与准确率的最佳权衡。



## 实验与关键发现

### 主结果：数学推理

LaDiR 在 7 个数学推理基准上取得 43.5% 的平均 Pass@1，超越此前最强的潜在推理基线 **TaH+**（Fu et al., 2025）的 42.0%（+1.5 个百分点），同时大幅领先自回归 CoT SFT 基线的 39.3%。在 Pass@100 指标上，LaDiR 达到 52.0%，比 CoT SFT（α=0.7）的 45.4% 高出 6.6 个百分点，验证了潜在扩散在测试时扩展性与多样性探索上的优势。完整结果见 **Table 1**。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_z5cPEZ4n6i/figures/003_Table_1.jpg]]
*Table 1: Math reasoning results across in-domain and out-of-domain benchmarks. Each cell reports Pass@1 (left) / Pass@100 (right) accuracy. α is the decoding temperature of LLMs. ∗Results are taken from the original paper; missing Pass@100 results (denoted as “–”) indicate that the codebase is not open-sourced for reproduction*

值得注意的是，去除第二阶段训练（-w/o Stage 2）导致平均 Pass@1 从 43.5% 骤降至 27.9%，揭示了训练-推理不一致所造成的误差累积是该框架的关键瓶颈，而 rollout training 是缓解这一问题的核心机制。

### 主结果：代码生成与规划任务

在代码生成任务上，LaDiR 以 74.5% 的平均 Pass@1 超越自回归 SFT 基线的 69.3%（+5.2 个百分点），其中 HumanEval+ 上达到 84.2%，领先 AR SFT 达 7.7 个百分点（**Table 2**）。需注意，部分对比方法（如 **Qwen 2.5 Coder 7B**、**OpenCoder**）基于代码专用预训练模型，而 LaDiR 使用通用 Qwen3-8B-Base，直接比较可能受基础模型能力差异影响。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_z5cPEZ4n6i/figures/004_Table_2.jpg]]
*Table 2: Code generation performance on MBPP and HumanEval benchmarks (including their Plus versions). We report Pass@1 accuracy (%). The best results for each metric are highlighted in bold*

在 Countdown 规划任务上，LaDiR 展现出更显著的提升：Countdown-4 的 Pass@1 从 LLaMA 8B SFT 的 46.7% 提升至 76.6%（+29.9 个百分点），Pass@100 达到 96.4%；Countdown-5 从 8.9% 提升至 38.5%（+29.6 个百分点），同时多样性指标（100 次采样中发现的唯一有效解数量）也大幅领先（**Table 3**）。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_z5cPEZ4n6i/figures/005_Table_3.jpg]]
*Table 3: Results on Countdown tasks. We report Pass@1, Pass@100, and Diversity (Div.). Diversity is measured as the number of unique valid solutions discovered among 100 samples. Best results are in bold, and second-best are underlined. ∗Dream 7B Base refers to the open-sourced base model without finetuning on this task.†MGDM is a task-specific small discrete diffusion model rather than a general-purpose language model*

### 消融实验

**扩散目标选择**：在 Countdown-4 上，流匹配（u-prediction）目标达到 73.5%，显著优于 x-prediction（66.8%）和 v-prediction（68.1%），确立了流匹配作为潜在推理预测目标的优势（**Table 5**）。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_z5cPEZ4n6i/figures/010_Table_5.jpg]]
*Table 5: Ablation study on latent prediction objectives on the Countdown-4 dataset*

**去噪步数的影响**：将去噪步数从 5 步增加到 10 步，7 个数学基准上的平均准确率提升 +11.7 个百分点；继续增加至 30 步再获 +4.8 个百分点，至 50 步累计增益达 +9.8 个百分点。GSM8K 的收益最为显著，从 5 步的约 38% 跃升至 50 步的约 84% 后趋于饱和（**Figure 4**）。这表明 LaDiR 具备通过增加推理计算量来持续提升性能的扩展能力，但边际收益递减。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_z5cPEZ4n6i/figures/009_Figure_4.jpg]]
*Figure 4: Effect of number of denoising steps on downstream reasoning performance on the math reasoning tasks*

**VAE 鲁棒性增强**：在 VAE 编码时引入潜在高斯噪声（k=3）和输入符号替换（p=0.3），使 GSM8K 达到最佳性能 84.2%（**Table 6**）。这一结果表明，增强 VAE 对编码扰动的鲁棒性有助于提升下游推理质量。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_z5cPEZ4n6i/figures/012_Table_6.jpg]]
*Table 6: Ablation study on VAE robustness augmentations on GSM8K*

**块化策略**：每块 1 个句子、4 个潜在 token 的配置在 GSM8K 上实现 84.2% 准确率与 MATH 上 45.2% 的最佳平衡。过大的块（如每块 16 个潜在 token）虽能提升 VAE 重建精度至 100%，但下游准确率反而降至 66.3%，说明过度压缩会损害潜在表示的语义可区分性（**Table 7**、**Figure 5**）。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_z5cPEZ4n6i/figures/011_Figure_5.jpg]]
*Figure 5: Ablation analysis of block size on the GSM8K benchmark*

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_z5cPEZ4n6i/figures/013_Table_7.jpg]]
*Table 7: Ablation study on blockization strategy (sentences per block)*

**多样性引导参数**：初始噪声从尺度 1 增加到 2 可同时提升多样性与准确率，但尺度 3 的过度噪声虽带来更高多样性却损害收敛。排斥力场的最大强度在 0.3–0.5 之间取得最优的多样性-准确率权衡（**Figure 3**）。

### 定性分析：迭代自我修正

**Table 4** 和 **Table 10** 展示了 LaDiR 在去噪过程中的语义级自我修正能力。在 Countdown-4 任务中，随着去噪时间步 t 递减，解码文本从粗糙或不完整的算术表达式逐步修正为逻辑一致的方程。例如，模型最初产生近似关系 "2 = 1 + 1"，随后重建为正确的等式。在 GSM8K 上，推理过程随 t 减小而逐渐清晰，算术错误得到修正（**Table 10**）。此外，**Table 11** 的定性对比显示，LaDiR 生成的推理链（7 步）比 SFT 基线的简约推理（2 步，且答案错误）更为详尽和正确。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_z5cPEZ4n6i/figures/008_Table_4.jpg]]
*Table 4: Examples of iterative selfrefinement of decoded text from the VAE decoder on the Countdown-4 dataset across different denoising timesteps (t)*

### 推理效率

在 MATH 数据集上，LaDiR 使用 10 步去噪的推理延迟与自回归基线相当，但增加步数时计算成本线性增长（**Table 9**），限制了在极低延迟场景下的应用。

### 失败模式与局限

1. **训练复杂度**：两阶段训练流程较传统 SFT 更复杂，增加了计算开销。
2. **任务泛化性**：目前仅在数学推理、代码生成和 Countdown 规划任务上验证，对其他领域的有效性需进一步评估。
3. **超参数敏感性**：多样性引导机制引入初始噪声尺度和排斥强度两个额外超参数，需针对不同任务调整。
4. **VAE 重建瓶颈**：编码器的重建精度直接影响推理性能，在复杂上下文上可能面临重建损失与 KL 正则化的权衡。
5. **推理效率边界**：虽然 10 步扩散可匹配自回归延迟，但追求更高精度时计算成本线性增长，限制了在极低延迟场景的应用。

### 开放问题

- 如何根据查询难度自适应分配去噪步数，以最大化精度-计算量的权衡？
- 在更复杂的多跳推理任务上，潜在 token 的语义保真度是否仍能满足精确推理要求？
- 能否将多样性引导与最佳 N 采样策略结合，进一步利用更多样本提升覆盖率？
- 流匹配目标在更大规模模型和数据集上的扩展性及训练稳定性如何？

### 补充图表

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_z5cPEZ4n6i/figures/014_Figure_6.jpg]]
*Figure 6: Results for pass@k performance on Countdown-4 with k $\in \{$ 1 , 1 0 , 2 5 , 5 0 , 1 0 0 $\}$*



## 定位与知识库关联

### 1. 核心基线对比与谱系定位

LaDiR 处于**潜在推理**（latent reasoning）与**扩散语言模型**（diffusion language models）两条技术路线的交汇点。其直接对比的基线可分为三类：

**自回归推理基线。** 传统思维链（CoT）方法采用自回归解码逐 token 生成推理步骤，以 **LLaMA 3.1 8B CoT SFT**（Dubey et al., 2024）为代表。该范式在数学推理 7 基准上平均 Pass@1 为 40.1%（温度 0.7），但其根本瓶颈在于缺乏全局修正能力——早期生成的 token 一旦出错便无法回溯修改，导致错误在后续步骤中累积放大。

**潜在推理基线。** 这类方法将推理步骤编码为连续向量以绕过离散 token 的刚性约束，但保留了自回归的顺序生成模式。代表性工作包括：

- **Coconut**（Hao et al., 2024）：在推理链末端插入连续思维 token，但缺乏显式的语义级自我修正机制。
- **TaH+**（Fu et al., 2025）：此前最强的潜在推理方法，数学推理平均 Pass@1 为 42.0%。
- **CODI**（Shen et al., 2025a）、**Soft Thinking**（Zhang et al., 2025）：同样采用连续表示进行推理，但均受限于自回归解码的固有顺序性。

LaDiR 相较于上述潜在推理基线的关键突破在于：用**块级扩散去噪**替代了自回归生成，从而获得了迭代修正和多样性探索的能力。在数学推理 7 基准上，LaDiR 以 Pass@1 43.5% 超越 TaH+ 的 42.0%（+1.5 个百分点），Pass@100 更是达到 52.0%，远超 CoT SFT 的 45.4%（+6.6 个百分点）。

**离散扩散基线。** 以 **LLaDA 8B**（Nie et al., 2025）为代表的遮蔽扩散模型在离散 token 空间进行并行生成，但本质上仍是对 token 级 [MASK] 的填充，缺乏语义层面的潜在表示。在 Countdown-4 任务上，LLaDA SFT 的 Pass@1 为 36.5%，而 LaDiR 达到 76.6%。

**潜在扩散基线。** 在文本生成领域，**LD4LG**（Lovelace et al., 2024）和 **PLANNER**（Zhang et al., 2023）等早期工作探索了潜在扩散用于文本建模的可能性，但均未针对推理任务进行专门设计。LaDiR 首次将潜在扩散系统地应用于数学和代码推理场景。

**循环潜在推理基线。** **Ouro 2.6B**（Zhu et al., 2025b）采用循环机制在潜在空间中进行推理，在代码生成 MBPP 上取得 80.4% 的 Pass@1，但该方法基于更小的模型规模，且循环机制与扩散去噪的迭代修正机制存在本质差异。

### 2. 方法适用边界

**已验证的适用领域。** LaDiR 在以下任务上展现出显著的性能优势：

- **数学推理**：涵盖 MATH、GSM8K、College-Math、DeepMind-Math、OlympiaBench-Math、TheoremQA、Fresh-Gaokao-Math-2023 共 7 个基准，平均 Pass@1 43.5%，Pass@100 52.0%。
- **代码生成**：在 MBPP、MBPP+、HumanEval、HumanEval+ 四个基准上平均 Pass@1 74.5%，其中 HumanEval+ 达到 84.2%，超越自回归 SFT 基线 7.7 个百分点。
- **规划任务**：在 Countdown-4 上 Pass@1 76.6%（LLaMA 8B SFT 为 46.7%），Countdown-5 上 Pass@1 38.5%（基线 8.9%），且多样性指标（100 次采样中的唯一有效解数量）显著领先。

**适用边界与限制。**

1. **训练流程复杂性**：LaDiR 依赖两阶段训练（教师强制 + 自生成展开训练），相比传统 SFT 增加了训练开销。移除第二阶段训练会导致数学推理平均 Pass@1 从 43.5% 骤降至 27.9%（Table 1），证明该阶段对缓解训练-推理不一致和误差累积至关重要，但也意味着训练流程不可简化。

2. **推理延迟约束**：10 步扩散去噪可匹配自回归方法的推理延迟，但将步数增至 30 步时，7 基准平均准确率仅额外提升 +4.8 个百分点，增至 50 步累计提升 +9.8 个百分点（Figure 4）。这呈现边际收益递减趋势，在极低延迟场景下限制了去噪步数的扩展空间。

3. **VAE 重建精度的瓶颈**：VAE 编码器的重建精度直接影响下游推理性能。在 GSM8K 上，增大潜在高斯噪声（k=3）和输入符号替换（p=0.3）可将准确率提升至 84.2%（Table 6），但这也暗示了复杂上下文下重建损失与 KL 正则化之间存在权衡，可能影响语义保真度。

4. **多样性引导的超参数敏感性**：初始噪声尺度从 1 增至 2 可同时提升多样性和准确率，但增至 3 时虽多样性继续提高，准确率却因收敛困难而下降（Table 3）。最大多样性尺度 γ_max 在 0.3–0.5 之间取得最佳平衡（Figure 3），但最优值因任务而异，需要额外调参。

5. **领域泛化未验证**：当前评估仅覆盖数学推理、代码生成和 Countdown 规划任务，对其他推理密集型领域（如法律推理、科学推理、多跳问答）的泛化性尚需进一步验证。

### 3. 开放问题

1. **自适应去噪步数分配**：如何根据查询难度动态分配去噪步数，以最大化精度-计算量的权衡？当前固定步数策略在简单问题上浪费计算资源，在困难问题上可能不足。

2. **潜在 token 的语义保真度边界**：在更复杂的多跳推理任务上，潜在 token 的语义保真度是否仍能满足精确推理的要求？VAE 的压缩-重建是否会丢失关键的细粒度逻辑信息？

3. **多样性引导与最佳 N 采样的协同**：能否将多样性引导与最佳 N 采样策略相结合，进一步利用超出 Pass@100 的更多样本来提升覆盖率？当前多样性引导仅在批次内施加排斥力，与更大规模采样的协同潜力尚未探索。

4. **流匹配目标的大规模扩展性**：流匹配（u-prediction）目标在 Countdown-4 上达到 73.5%，显著优于其他扩散目标（Table 5），但在更大规模模型和数据集上的训练稳定性和扩展性如何，仍需验证。

5. **块化策略的自适应选择**：当前每块 1 句子、4 个潜在 token 的块化策略在 GSM8K 上取得最佳平衡（84.2% 准确率，Table 7），但不同任务的最优块大小和潜在 token 数可能不同，如何实现任务自适应的块化策略？



## 原文 PDF

![[paperPDFs/ICLR_2026/LaDiR_Latent_Diffusion_Enhances_LLMs_for_Text_Reasoning.pdf]]
